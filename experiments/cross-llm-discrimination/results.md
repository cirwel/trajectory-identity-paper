# Cross-LLM discrimination experiment — results memo

**Date:** 2026-05-09
**Subjects:** gpt-5.5 at three reasoning-effort levels (low, medium, xhigh), treated as distinct "agents" for the discrimination test.
**Note on scope:** the original design called for cross-model discrimination across gpt-5.5, claude-sonnet-4-6, and claude-haiku-4-5. The Anthropic API key had $0 credit at run time, so the experiment was scoped down to a within-Codex effort-level discrimination test. Results below should be read with that caveat — this is *not* a direct test of cross-model trajectory-identity discrimination.

## Method

- **5 prompts** (subset of `prompts.json`): math reasoning, code, open-ended, structured JSON, conversation.
- **3 effort levels** (Codex `model_reasoning_effort` config): low, medium, xhigh.
- **2 runs per (effort, prompt) cell** to estimate within-cell run-to-run variance.
- **30 Codex calls total**, ~4-minute wall-clock.
- Behavioral features (13-dim) extracted deterministically from each response: char/word counts, type-token ratio, sentence/question counts, punctuation density, code-block / list-item / heading presence, first-person and hedging counts, refusal indicator.
- Pooled-data z-score normalization, then Euclidean distance in feature space.

## Headline result

**Discrimination ratio between/within = 0.87.** The 13-dim feature space does *not* cleanly discriminate effort levels. Within-model run-to-run variance is comparable to or larger than between-effort distance.

## Per-cell numbers

**Within-model distance (z-score units, averaged over prompts):**

| Effort | Within-cell run-to-run distance |
|--------|---------------------------------|
| low | 2.028 |
| medium | 1.586 |
| xhigh | 1.018 |

**Within-model variance shrinks with effort.** Low-effort Codex is more stochastic; xhigh-effort is nearly deterministic. This is itself a reportable finding — effort settings affect not just *what* the model says but *how consistent* it is.

**Between-effort distance (averaged over prompts):**

| Pair | Distance |
|------|----------|
| low vs medium | 0.489 |
| low vs xhigh | 1.874 |
| medium vs xhigh | 1.669 |

**Low vs medium is much smaller than low vs xhigh.** Low and medium effort produce nearly indistinguishable behavioral signatures (0.489 z-score units); xhigh is clearly different from both (~1.7-1.9 units). Effort discrimination is monotonic-ish in effort level, but only when the gap is large.

**The within-low variance (2.028) is bigger than the between-low-vs-xhigh distance (1.874).** This is the headline failure mode: stochasticity at low effort swamps the between-effort signal.

## Per-feature contribution to between-model variance

```
list_item_count       0.378
first_person_count    0.171
ttr (type-token)      0.097
punct_density         0.081
avg_word_len          0.078
sentence_count        0.062
char_count            0.051
word_count            0.047
question_count        0.000  (constant)
has_code_block        0.000  (constant)
heading_count         0.000  (constant)
hedging_count         0.000  (constant)
refusal_score         0.000  (constant)
```

Only two features (list-item count, first-person pronoun count) carry meaningful between-effort signal in this prompt corpus. Five features were constant (no variance across runs), reducing the effective discriminative dimension to 8 — and most of those 8 contribute < 0.1 z-units. The framework's behavioral fingerprint, applied to LLM outputs through this feature set, is **information-poor** relative to the within-cell noise.

## What this tells us about the framework's claims

1. **Trajectory identity for LLM agents is not free.** The §3 framework was developed and validated for an embodied agent (Lumen) with continuous, slowly-drifting state and clear perturbation/recovery dynamics. Applied naively to LLM agents — with stochastic discrete outputs and no homeostatic state — the discrimination signal is weak relative to within-cell stochastic noise.

2. **Per-prompt feature means likely need more samples per cell.** With $N = 2$ runs per (effort, prompt) cell, the standard error on the cell's mean is $\sigma / \sqrt{2}$. To shrink within-cell distance from $\approx 2.0$ to $\approx 0.5$ z-units (where between-low-vs-xhigh would clearly dominate), we'd need $N \approx 16$ runs per cell — 8× the data. That's feasible but expensive.

3. **The natural dimensions for LLM trajectory signatures are not text-surface features.** Char counts, lexical density, and structural indicators don't carry enough signal. More promising candidates for §7.3 cross-platform validation:
   - Token-level distributional features (logprob entropy, top-k mass)
   - Embedding-space centroid and dispersion of responses
   - Tool-use patterns (when applicable)
   - Refusal rate on adversarial probes
   - Latency under controlled prompt complexity (compute-time signature)

4. **Within-agent stability claims work even where between-agent claims don't.** Note that within-cell variance for xhigh is ~1.0 z-units and for low is ~2.0. The framework's *within-agent* observation — characteristic noise level per "agent" — is recoverable from this data. Just not the *between-agent* discrimination.

5. **Low effort and medium effort are operationally the same agent in this feature space.** Their behavioral signatures are 0.489 z-units apart, well within the within-cell noise. From the framework's perspective, these would be classified as "operationally continuous." Whether this is correct depends on what the deployer cares about — if low-vs-medium is a meaningful distinction for downstream behavior, the framework misses it.

## Honest scope: what this experiment is NOT

- **Not a cross-model discrimination test.** All three "agents" are gpt-5.5 with different inference compute. A real cross-model test (Codex vs Claude vs Gemini, say) would likely produce stronger between-agent signal — different model architectures and training corpora produce more divergent outputs than same-model-different-effort.
- **Not a refutation of the §3 framework.** The framework is defined for embodied agents with continuous state. This experiment is a stress test of the *naive transposition* of the framework to LLM-output features. A properly-adapted framework for LLM agents (with appropriate state-space and signature definitions) might recover discrimination.
- **Not large enough to be conclusive.** $3 \times 5 \times 2 = 30$ data points is enough to see qualitative patterns but not enough to put confidence intervals on the discrimination ratio.

## What this informs for v0.12 of the paper

§7.3 (Cross-Platform Validation) should be expanded to acknowledge:

> *Naive transposition of the trajectory-signature framework — using surface text features as the per-response feature vector — does not produce strong discrimination for stochastic LLM agents at small sample sizes (n ≤ 2 per cell). Within-agent stochastic variance can be comparable to between-agent distance. Cross-platform validation requires either (a) larger per-agent sample sizes (we estimate $N \gtrsim 16$ runs per cell from a small pilot study, results.md), or (b) signature features that exploit the LLM-specific state space — token logprobs, embedding centroids, latency profiles — rather than text-surface features. The framework's within-agent stability claims do reproduce on LLM agents at this scale; the between-agent discrimination claims do not.*

## Reproducing this

```bash
cd ~/projects/trajectory-identity-paper
python3 experiments/cross-llm-discrimination/run_experiment.py \
  --runs 2 \
  --models gpt-5.5_effort-low,gpt-5.5_effort-medium,gpt-5.5_effort-xhigh \
  --prompts p01_math,p03_code,p05_open,p06_json,p10_conversation
python3 experiments/cross-llm-discrimination/extract_features.py
python3 experiments/cross-llm-discrimination/analyze.py
```

Outputs cached at `experiments/cross-llm-discrimination/outputs/`. Re-running skips cached responses.

## Open follow-ups

- **Run the full 3-model cross-LLM test** once the Anthropic API key has credit. Reuses all the infrastructure; just change `--models`.
- **Increase $N$ per cell** to 16+ to drive down within-cell variance and see whether between-effort discrimination clears within-noise.
- **Add token-level features** (requires logprob-aware backends; Anthropic API supports `logprobs` in newer model versions).
- **Run a sensitivity analysis** on which prompts contribute most to discrimination — different prompt categories may load differently.
