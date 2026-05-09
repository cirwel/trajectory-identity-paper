#!/usr/bin/env python3
"""
Extract behavioral features from raw responses.

Reads outputs/<model>/<prompt_id>__run<k>.txt files, computes
deterministic per-response feature vectors, writes features.json.

Features (deterministic, computed from text only):
  char_count            total characters
  word_count            whitespace-separated tokens
  ttr                   type-token ratio (unique words / total)
  avg_word_len          mean characters per word
  sentence_count        count of '.', '!', '?' (rough)
  question_count        count of '?'
  punct_density         non-alphanumeric non-space chars / total chars
  has_code_block        binary, presence of triple-backtick
  list_item_count       lines starting with '- ' or numbered
  heading_count         lines starting with '#'
  first_person_count    count of "i ", " i ", "i'm", "i've", "i'd", "my " (case-insensitive)
  hedging_count         "maybe", "perhaps", "might", "could", "possibly", "probably"
  refusal_score         binary, presence of refusal phrasing
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).parent
OUTPUT_DIR = HERE / "outputs"
FEATURES_FILE = HERE / "features.json"

REFUSAL_PHRASES = [
    "i can't", "i cannot", "i'm unable", "i won't", "i will not",
    "i'm not able", "as an ai", "i don't have the ability",
]
HEDGING_TOKENS = re.compile(
    r"\b(maybe|perhaps|might|could|possibly|probably|likely|unlikely|appears|seems|may)\b",
    re.IGNORECASE,
)
FIRST_PERSON = re.compile(r"\b(i|i'm|i've|i'd|i'll|me|my|myself)\b", re.IGNORECASE)
LIST_LINE = re.compile(r"^\s*(?:[-*]|\d+\.)\s+")
HEADING_LINE = re.compile(r"^\s*#{1,6}\s+")


def features(text: str) -> dict:
    if not text:
        text = ""
    lower = text.lower()
    chars = len(text)
    words = text.split()
    word_count = len(words)
    unique_words = len(set(w.lower() for w in words))
    ttr = unique_words / word_count if word_count else 0.0
    avg_word_len = sum(len(w) for w in words) / word_count if word_count else 0.0
    sentence_count = sum(text.count(c) for c in ".!?") or 1
    question_count = text.count("?")
    non_alpha = sum(1 for c in text if not c.isalnum() and not c.isspace())
    punct_density = non_alpha / chars if chars else 0.0
    has_code_block = 1 if "```" in text else 0
    lines = text.split("\n")
    list_item_count = sum(1 for line in lines if LIST_LINE.match(line))
    heading_count = sum(1 for line in lines if HEADING_LINE.match(line))
    first_person_count = len(FIRST_PERSON.findall(text))
    hedging_count = len(HEDGING_TOKENS.findall(text))
    refusal_score = 1 if any(p in lower for p in REFUSAL_PHRASES) else 0

    return {
        "char_count": chars,
        "word_count": word_count,
        "ttr": ttr,
        "avg_word_len": avg_word_len,
        "sentence_count": sentence_count,
        "question_count": question_count,
        "punct_density": punct_density,
        "has_code_block": has_code_block,
        "list_item_count": list_item_count,
        "heading_count": heading_count,
        "first_person_count": first_person_count,
        "hedging_count": hedging_count,
        "refusal_score": refusal_score,
    }


def main():
    out = {}  # model -> prompt_id -> [run0_features, run1_features, ...]
    for model_dir in sorted(OUTPUT_DIR.glob("*")):
        if not model_dir.is_dir():
            continue
        model = model_dir.name
        out[model] = {}
        for txt_file in sorted(model_dir.glob("*.txt")):
            stem = txt_file.stem  # p01_math__run0
            if "__run" not in stem:
                continue
            prompt_id, run_str = stem.split("__run")
            run_idx = int(run_str)
            text = txt_file.read_text()
            feats = features(text)
            feats["_text_preview"] = text[:120].replace("\n", " ")
            out[model].setdefault(prompt_id, [None, None, None])
            while len(out[model][prompt_id]) <= run_idx:
                out[model][prompt_id].append(None)
            out[model][prompt_id][run_idx] = feats

    FEATURES_FILE.write_text(json.dumps(out, indent=2))
    # Brief summary
    print(f"=== Feature extraction summary ===")
    for model, prompts in out.items():
        n_runs_total = sum(len([r for r in runs if r is not None]) for runs in prompts.values())
        print(f"  {model}: {len(prompts)} prompts, {n_runs_total} valid runs")
    print(f"Features written: {FEATURES_FILE}")


if __name__ == "__main__":
    main()
