#!/usr/bin/env python3
"""
Cross-LLM discrimination experiment runner.

Runs each prompt through three model backends (gpt-5.5 via Codex,
claude-sonnet-4-6 via Anthropic API, claude-haiku-4-5 via Anthropic
API), 2 runs per (model, prompt) pair, saves raw outputs.

Total API calls per pass: 3 models × N prompts × 2 runs.
Resumable: skips outputs that already exist on disk.

Usage:
  python3 run_experiment.py [--runs N] [--models M1,M2,...]

Outputs:
  outputs/<model>/<prompt_id>__run<k>.txt        (raw response)
  outputs/<model>/<prompt_id>__run<k>.meta.json  (timing, token counts)
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

import requests

HERE = Path(__file__).parent
PROMPTS_FILE = HERE / "prompts.json"
OUTPUT_DIR = HERE / "outputs"

DEFAULT_MODELS = ["gpt-5.5", "claude-sonnet-4-6", "claude-haiku-4-5"]

# Codex effort levels exposed as pseudo-models for the effort-discrimination experiment
CODEX_EFFORT_MODELS = {
    "gpt-5.5_effort-low": "low",
    "gpt-5.5_effort-medium": "medium",
    "gpt-5.5_effort-xhigh": "xhigh",
}


def load_prompts():
    return json.loads(PROMPTS_FILE.read_text())["prompts"]


def call_anthropic(model_id: str, prompt: str, max_tokens: int = 800) -> dict:
    """Direct call to Anthropic API. Returns dict with text + meta."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    body = {
        "model": model_id,
        "max_tokens": max_tokens,
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    t0 = time.monotonic()
    resp = requests.post(
        "https://api.anthropic.com/v1/messages",
        json=body,
        headers=headers,
        timeout=120,
    )
    elapsed = time.monotonic() - t0
    if resp.status_code != 200:
        raise RuntimeError(f"Anthropic API HTTP {resp.status_code}: {resp.text[:300]}")
    data = resp.json()
    text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
    return {
        "text": text,
        "elapsed_s": elapsed,
        "input_tokens": data.get("usage", {}).get("input_tokens"),
        "output_tokens": data.get("usage", {}).get("output_tokens"),
        "stop_reason": data.get("stop_reason"),
    }


def call_codex(prompt: str, effort: Optional[str] = None) -> dict:
    """Run codex exec with prompt as input. Returns dict with text + meta."""
    cmd = ["codex", "exec", "--skip-git-repo-check"]
    if effort:
        cmd += ["-c", f'model_reasoning_effort="{effort}"']
    cmd.append(prompt)
    t0 = time.monotonic()
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=600,
    )
    elapsed = time.monotonic() - t0
    raw = proc.stdout
    # Codex output structure: header lines, then `user` block, then `codex` block(s) with response
    # Try to extract just the codex response (after last "codex" line, before "tokens used")
    text = _extract_codex_response(raw)
    return {
        "text": text,
        "elapsed_s": elapsed,
        "raw_stdout_len": len(raw),
        "exit_code": proc.returncode,
    }


def _extract_codex_response(raw: str) -> str:
    """Extract the assistant response from codex exec stdout."""
    lines = raw.split("\n")
    # Find lines between the last "^codex$" marker and either next "^codex$" or "^tokens used$"
    last_codex_idx = None
    for i, line in enumerate(lines):
        if line.strip() == "codex":
            last_codex_idx = i
    if last_codex_idx is None:
        return raw  # fallback: return everything
    end_idx = len(lines)
    for j in range(last_codex_idx + 1, len(lines)):
        if lines[j].strip() == "tokens used":
            end_idx = j
            break
        if lines[j].strip() == "codex" and j > last_codex_idx:
            break
    return "\n".join(lines[last_codex_idx + 1:end_idx]).strip()


def run_one(model: str, prompt_id: str, prompt_text: str, run_idx: int, output_dir: Path) -> Optional[dict]:
    """Run a single (model, prompt, run) combination, save output, return meta."""
    model_dir = output_dir / model.replace("/", "_")
    model_dir.mkdir(parents=True, exist_ok=True)
    out_text = model_dir / f"{prompt_id}__run{run_idx}.txt"
    out_meta = model_dir / f"{prompt_id}__run{run_idx}.meta.json"

    if out_text.exists() and out_meta.exists():
        print(f"  [skip-cache] {model} {prompt_id} run{run_idx}")
        return None

    print(f"  [run]      {model} {prompt_id} run{run_idx} ...", flush=True)
    try:
        if model in CODEX_EFFORT_MODELS:
            result = call_codex(prompt_text, effort=CODEX_EFFORT_MODELS[model])
        elif model == "gpt-5.5":
            result = call_codex(prompt_text)
        else:
            result = call_anthropic(model, prompt_text)
    except Exception as e:
        print(f"  [error]    {model} {prompt_id} run{run_idx}: {e}")
        out_meta.write_text(json.dumps({"error": str(e)}))
        return {"error": str(e)}

    out_text.write_text(result["text"])
    out_meta.write_text(json.dumps(result, indent=2))
    print(f"             text_len={len(result['text'])} elapsed={result['elapsed_s']:.1f}s")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--runs", type=int, default=2, help="Runs per (model, prompt) pair")
    parser.add_argument("--models", type=str, default=",".join(DEFAULT_MODELS))
    parser.add_argument("--prompts", type=str, default=None,
                        help="Comma-separated prompt IDs to run (default: all)")
    args = parser.parse_args()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    prompts = load_prompts()
    if args.prompts:
        wanted = set(args.prompts.split(","))
        prompts = [p for p in prompts if p["id"] in wanted]
    models = args.models.split(",")

    print(f"=== Cross-LLM discrimination experiment ===")
    print(f"models: {models}")
    print(f"prompts: {[p['id'] for p in prompts]}")
    print(f"runs per pair: {args.runs}")
    print(f"total calls (worst case): {len(models) * len(prompts) * args.runs}")
    print()

    for model in models:
        print(f"--- model: {model} ---")
        for prompt in prompts:
            for run_idx in range(args.runs):
                run_one(model, prompt["id"], prompt["text"], run_idx, OUTPUT_DIR)


if __name__ == "__main__":
    main()
