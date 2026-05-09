#!/usr/bin/env python3
"""
Analyze cross-LLM discrimination from features.json.

Computes:
  - Per-(model, prompt) within-model run-to-run distance (where 2 runs exist)
  - Per-prompt between-model distances
  - Discrimination ratio: mean(between) / mean(within)
  - Per-feature contribution to discrimination

All distances computed in z-score-normalized feature space using
the pooled mean/std across (model, prompt, run).
"""
import itertools
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).parent
FEATURES_FILE = HERE / "features.json"
RESULTS_FILE = HERE / "analysis_results.json"

NUMERIC_FEATURES = [
    "char_count", "word_count", "ttr", "avg_word_len",
    "sentence_count", "question_count", "punct_density",
    "has_code_block", "list_item_count", "heading_count",
    "first_person_count", "hedging_count", "refusal_score",
]


def to_vec(feats: dict) -> np.ndarray:
    return np.array([feats[f] for f in NUMERIC_FEATURES], dtype=float)


def main():
    data = json.loads(FEATURES_FILE.read_text())

    # Collect all feature vectors for normalization
    all_vecs = []
    for model, prompts in data.items():
        for pid, runs in prompts.items():
            for run in runs:
                if run is None or "error" in run:
                    continue
                all_vecs.append(to_vec(run))
    all_vecs = np.array(all_vecs)
    mu = all_vecs.mean(axis=0)
    sigma = all_vecs.std(axis=0) + 1e-9
    print(f"Pooled features: n={len(all_vecs)}, dim={all_vecs.shape[1]}")
    print(f"Per-feature mean and std (used for z-score):")
    for f, m, s in zip(NUMERIC_FEATURES, mu, sigma):
        print(f"  {f:>22s}: mean={m:8.3f}  std={s:8.3f}")

    # Build z-scored feature dict: model -> prompt_id -> list of (run_idx, vec_z)
    z_data = {}
    for model, prompts in data.items():
        z_data[model] = {}
        for pid, runs in prompts.items():
            z_data[model][pid] = []
            for run_idx, run in enumerate(runs):
                if run is None or "error" in run:
                    continue
                v = (to_vec(run) - mu) / sigma
                z_data[model][pid].append((run_idx, v))

    models = list(z_data.keys())
    prompts_set = set()
    for m in models:
        prompts_set.update(z_data[m].keys())
    prompts = sorted(prompts_set)
    print(f"\nModels: {models}")
    print(f"Prompts: {prompts}")

    # WITHIN-model distance: per (model, prompt), mean pairwise distance over runs
    within_model_per_prompt = {}  # model -> prompt -> distance
    within_model_overall = {}  # model -> overall mean
    for m in models:
        within_model_per_prompt[m] = {}
        per_prompt_dists = []
        for p in prompts:
            runs = z_data[m].get(p, [])
            if len(runs) < 2:
                continue
            pair_dists = []
            for (_, v1), (_, v2) in itertools.combinations(runs, 2):
                pair_dists.append(float(np.linalg.norm(v1 - v2)))
            if pair_dists:
                d = float(np.mean(pair_dists))
                within_model_per_prompt[m][p] = d
                per_prompt_dists.append(d)
        within_model_overall[m] = float(np.mean(per_prompt_dists)) if per_prompt_dists else None

    # BETWEEN-model distance: per prompt, distance between models
    # Use the mean of run-vectors per (model, prompt) as the model's signature for that prompt
    between_per_pair = {}  # (m1, m2) -> per_prompt -> distance
    between_per_pair_overall = {}  # (m1, m2) -> overall
    for m1, m2 in itertools.combinations(models, 2):
        per_prompt = {}
        for p in prompts:
            r1 = z_data[m1].get(p, [])
            r2 = z_data[m2].get(p, [])
            if not r1 or not r2:
                continue
            mean1 = np.mean([v for _, v in r1], axis=0)
            mean2 = np.mean([v for _, v in r2], axis=0)
            per_prompt[p] = float(np.linalg.norm(mean1 - mean2))
        between_per_pair[(m1, m2)] = per_prompt
        between_per_pair_overall[(m1, m2)] = float(np.mean(list(per_prompt.values()))) if per_prompt else None

    # Discrimination ratio
    overall_within = float(np.mean([d for d in within_model_overall.values() if d is not None]))
    overall_between = float(np.mean([d for d in between_per_pair_overall.values() if d is not None]))
    discrimination = overall_between / overall_within if overall_within else None

    # Per-feature: which features contribute most to between-model variance?
    # Mean response vector per model (over all prompts and runs), then std of those means per feature
    model_means = {}
    for m in models:
        all_run_vecs = []
        for p, runs in z_data[m].items():
            for _, v in runs:
                all_run_vecs.append(v)
        if all_run_vecs:
            model_means[m] = np.mean(all_run_vecs, axis=0)
    if len(model_means) >= 2:
        means_arr = np.array(list(model_means.values()))
        between_model_feat_std = means_arr.std(axis=0).tolist()
    else:
        between_model_feat_std = None

    print("\n=== Within-model run-to-run distance (z-score units) ===")
    for m, d in within_model_overall.items():
        print(f"  {m:>30s}: {d:.3f}" if d is not None else f"  {m:>30s}: (no within-model pairs)")

    print("\n=== Between-model distance (z-score units), averaged over prompts ===")
    for (m1, m2), d in between_per_pair_overall.items():
        print(f"  {m1:>30s} vs {m2:<30s}: {d:.3f}" if d is not None else f"  {m1} vs {m2}: -")

    print(f"\n=== Discrimination ratio ===")
    print(f"  overall mean within-model distance:  {overall_within:.3f}")
    print(f"  overall mean between-model distance: {overall_between:.3f}")
    if discrimination is not None:
        print(f"  ratio between/within:                {discrimination:.2f}x")
        if discrimination > 1.5:
            print(f"  → Models are discriminable in this feature space.")
        elif discrimination > 1.1:
            print(f"  → Marginal discrimination signal.")
        else:
            print(f"  → No discrimination in this feature space (within ≈ between).")

    if between_model_feat_std:
        print("\n=== Per-feature contribution to between-model variance (z-score-std of model means) ===")
        ranked = sorted(zip(NUMERIC_FEATURES, between_model_feat_std), key=lambda x: -x[1])
        for f, s in ranked:
            print(f"  {f:>22s}: {s:.3f}")

    RESULTS_FILE.write_text(json.dumps({
        "models": models,
        "prompts": prompts,
        "within_model_per_prompt": {m: within_model_per_prompt[m] for m in models},
        "within_model_overall": within_model_overall,
        "between_pair_per_prompt": {f"{m1}__{m2}": d for (m1, m2), d in between_per_pair.items()},
        "between_pair_overall": {f"{m1}__{m2}": d for (m1, m2), d in between_per_pair_overall.items()},
        "overall_within": overall_within,
        "overall_between": overall_between,
        "discrimination_ratio": discrimination,
        "between_model_feature_std": dict(zip(NUMERIC_FEATURES, between_model_feat_std)) if between_model_feat_std else None,
    }, indent=2))
    print(f"\nResults: {RESULTS_FILE}")


if __name__ == "__main__":
    main()
