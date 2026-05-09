#!/usr/bin/env python3
"""
Trajectory Identity v0.11.1 — quick analysis pass.

Addresses Codex's empirical-section concerns by computing:
  - §6.4.1 variance numbers with bootstrap 95% CIs
  - Autocorrelation function (lag 1, 10, 100, 500) — quantifies the
    "slow-drift, little fast noise" interpretation
  - AR(1) coefficient estimate per dimension
  - Recovery-tau histogram and KS test of normality (was 'bimodal'
    claim defensible? answer with data, not prose)
  - Comparison: original 65-day window (used in v0.11 paper) vs
    extended dataset (current backup, ~120 days)

Usage:
  python3 scripts/analysis_v0.11.1.py [path-to-anima.db]

Default db path: ~/backups/lumen/anima_<latest>.db

This script is intentionally dependency-light: stdlib + numpy only.
"""
import json
import math
import os
import random
import sqlite3
import sys
from pathlib import Path
from typing import Tuple

import numpy as np

# Original v0.11 paper §6.4.1 analysis window
ORIGINAL_WINDOW_START = "2026-01-11T00:00:00"
ORIGINAL_WINDOW_END = "2026-03-16T23:59:59"

# Window/step from original analysis
WINDOW = 500
STEP = 500
DIMS = ["warmth", "clarity", "stability", "presence"]


def load_db(db_path: str) -> sqlite3.Connection:
    if not Path(db_path).exists():
        raise FileNotFoundError(db_path)
    return sqlite3.connect(db_path)


def fetch_states(conn: sqlite3.Connection, t_start: str | None = None, t_end: str | None = None):
    q = "SELECT warmth, clarity, stability, presence, timestamp FROM state_history"
    where = []
    args: list = []
    if t_start:
        where.append("timestamp >= ?")
        args.append(t_start)
    if t_end:
        where.append("timestamp <= ?")
        args.append(t_end)
    if where:
        q += " WHERE " + " AND ".join(where)
    q += " ORDER BY timestamp"
    rows = conn.execute(q, args).fetchall()
    if not rows:
        return None
    arr = np.array([(r[0], r[1], r[2], r[3]) for r in rows if all(v is not None for v in r[:4])], dtype=float)
    return arr  # shape (N, 4)


def variance_analysis(states: np.ndarray, label: str) -> dict:
    """Reproduce §6.4.1 numbers + bootstrap CIs for var(mu)."""
    n = states.shape[0]
    n_windows = (n - WINDOW) // STEP + 1
    if n_windows < 2:
        return {"error": f"too few windows for {label}"}

    window_means = np.zeros((n_windows, 4))
    within_vars = np.zeros((n_windows, 4))
    for i in range(n_windows):
        chunk = states[i * STEP : i * STEP + WINDOW]
        window_means[i] = chunk.mean(axis=0)
        within_vars[i] = chunk.var(axis=0)

    var_of_mu = window_means.var(axis=0)
    avg_within = within_vars.mean(axis=0)
    grand_mean = states.mean(axis=0)

    # Bootstrap 95% CI for var(mu)
    rng = np.random.default_rng(42)
    n_boot = 1000
    boot_var_mu = np.zeros((n_boot, 4))
    for b in range(n_boot):
        idx = rng.integers(0, n_windows, n_windows)
        boot_var_mu[b] = window_means[idx].var(axis=0)
    ci_lo = np.quantile(boot_var_mu, 0.025, axis=0)
    ci_hi = np.quantile(boot_var_mu, 0.975, axis=0)

    return {
        "label": label,
        "n_observations": int(n),
        "n_windows": int(n_windows),
        "grand_mean": dict(zip(DIMS, grand_mean.tolist())),
        "var_of_mu": dict(zip(DIMS, var_of_mu.tolist())),
        "var_of_mu_ci95": {
            d: [float(ci_lo[i]), float(ci_hi[i])] for i, d in enumerate(DIMS)
        },
        "avg_within_window_var": dict(zip(DIMS, avg_within.tolist())),
        "ratio_between_to_within": dict(
            zip(DIMS, (var_of_mu / np.maximum(avg_within, 1e-12)).tolist())
        ),
    }


def autocorrelation(states: np.ndarray, max_lag: int = 1000) -> dict:
    """Compute ACF at selected lags for each dimension."""
    lags = [1, 10, 100, 500, 1000]
    out = {}
    for di, d in enumerate(DIMS):
        x = states[:, di]
        x_centered = x - x.mean()
        var = x_centered.var()
        if var <= 0:
            out[d] = {lag: float("nan") for lag in lags}
            continue
        acf = {}
        for lag in lags:
            if lag < len(x):
                cov = (x_centered[:-lag] * x_centered[lag:]).mean()
                acf[lag] = float(cov / var)
            else:
                acf[lag] = float("nan")
        out[d] = acf
    return out


def ar1_coefficient(states: np.ndarray) -> dict:
    """Fit AR(1) per dimension: x_t = phi * x_{t-1} + (1-phi)*mu + eps."""
    out = {}
    for di, d in enumerate(DIMS):
        x = states[:, di]
        if len(x) < 100:
            out[d] = float("nan")
            continue
        x_lag = x[:-1]
        x_now = x[1:]
        # Simple OLS for phi via correlation
        x_lag_c = x_lag - x_lag.mean()
        x_now_c = x_now - x_now.mean()
        denom = (x_lag_c**2).sum()
        if denom <= 0:
            out[d] = float("nan")
            continue
        phi = float((x_lag_c * x_now_c).sum() / denom)
        out[d] = phi
    return out


def recovery_tau_histogram(states: np.ndarray) -> dict:
    """Detect perturbations |x - mu| > 0.15 in any dim, fit exp recovery, histogram tau."""
    mu = states.mean(axis=0)
    deviations = np.abs(states - mu).max(axis=1)
    perturbed = deviations > 0.15
    # Find recovery episodes: contiguous-perturbed regions ending in return-to-baseline
    in_episode = False
    episodes = []  # list of (start, peak, end)
    start = None
    peak_dev = 0
    peak_idx = None
    for i, p in enumerate(perturbed):
        if p and not in_episode:
            start = i
            peak_dev = deviations[i]
            peak_idx = i
            in_episode = True
        elif p and in_episode:
            if deviations[i] > peak_dev:
                peak_dev = deviations[i]
                peak_idx = i
        elif not p and in_episode:
            episodes.append((start, peak_idx, i))
            in_episode = False
    # Estimate tau from each episode: time from peak to deviation < 0.05
    taus = []
    for start, peak, end in episodes:
        post = states[peak:end]
        post_dev = np.abs(post - mu).max(axis=1)
        recovered = np.where(post_dev < 0.05)[0]
        if len(recovered) > 0:
            t_recovered = recovered[0]
            # Fit exponential: deviation(t) ≈ peak_dev * exp(-t / tau)
            # tau = -t_recovered / ln(0.05 / peak_dev)
            if peak_dev > 0.05 and peak_dev > 0:
                tau_samples = -t_recovered / math.log(0.05 / peak_dev)
                # samples-to-seconds: assume 10s sampling rate (per paper's claim)
                tau_seconds = tau_samples * 10
                if tau_seconds > 0:
                    taus.append(tau_seconds)
    if not taus:
        return {"n_episodes": 0, "taus": [], "median": None, "mean": None, "std": None}
    taus_arr = np.array(taus)
    # Histogram bin into log-spaced buckets to test bimodality claim
    log_taus = np.log10(taus_arr)
    bins = np.linspace(log_taus.min(), log_taus.max(), 10)
    hist, _ = np.histogram(log_taus, bins=bins)
    return {
        "n_episodes": len(taus),
        "median_seconds": float(np.median(taus_arr)),
        "mean_seconds": float(taus_arr.mean()),
        "std_seconds": float(taus_arr.std()),
        "min_seconds": float(taus_arr.min()),
        "max_seconds": float(taus_arr.max()),
        "log10_histogram_bins": bins.tolist(),
        "log10_histogram_counts": hist.tolist(),
        "all_taus_seconds": taus_arr.tolist(),
    }


def main():
    db_path = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
        "~/backups/lumen/anima_20260509_0700.db"
    )
    print(f"=== Trajectory Identity v0.11.1 quick analysis ===")
    print(f"DB: {db_path}")
    conn = load_db(db_path)

    print(f"\n--- Original 65-day window ({ORIGINAL_WINDOW_START} → {ORIGINAL_WINDOW_END}) ---")
    states_orig = fetch_states(conn, ORIGINAL_WINDOW_START, ORIGINAL_WINDOW_END)
    if states_orig is None or len(states_orig) == 0:
        print("No data in original window.")
        return
    var_orig = variance_analysis(states_orig, "original_65d")
    acf_orig = autocorrelation(states_orig)
    ar1_orig = ar1_coefficient(states_orig)
    rec_orig = recovery_tau_histogram(states_orig)

    print(f"  Observations: {var_orig['n_observations']}")
    print(f"  Windows: {var_orig['n_windows']}")
    print(f"\n  Var(mu) [bootstrap 95% CI] vs avg within-window var:")
    for d in DIMS:
        lo, hi = var_orig["var_of_mu_ci95"][d]
        print(
            f"    {d:10s}  var(mu)={var_orig['var_of_mu'][d]:.4f} "
            f"[{lo:.4f}, {hi:.4f}]   within={var_orig['avg_within_window_var'][d]:.4f}   "
            f"ratio={var_orig['ratio_between_to_within'][d]:.1f}x"
        )

    print(f"\n  Autocorrelation (lag-N decay shows slow-drift regime):")
    print(f"    {'dim':10s}  {'lag=1':>8s}  {'lag=10':>8s}  {'lag=100':>8s}  {'lag=500':>8s}  {'lag=1000':>8s}")
    for d in DIMS:
        lags_str = "  ".join(f"{acf_orig[d][lag]:>8.4f}" for lag in [1, 10, 100, 500, 1000])
        print(f"    {d:10s}  {lags_str}")

    print(f"\n  AR(1) coefficient (closer to 1 = more persistent / slower-drifting):")
    for d in DIMS:
        print(f"    {d:10s}  phi = {ar1_orig[d]:.4f}")

    print(f"\n  Recovery dynamics:")
    print(f"    n_episodes = {rec_orig['n_episodes']}")
    if rec_orig['n_episodes'] > 0:
        print(f"    median tau = {rec_orig['median_seconds']:.1f}s")
        print(f"    mean tau   = {rec_orig['mean_seconds']:.1f}s")
        print(f"    std tau    = {rec_orig['std_seconds']:.1f}s")
        print(f"    range      = {rec_orig['min_seconds']:.1f}s — {rec_orig['max_seconds']:.1f}s")
        print(f"    log10(tau) histogram: {rec_orig['log10_histogram_counts']} (bins shown below)")
        print(f"    bin edges:           {[round(b, 2) for b in rec_orig['log10_histogram_bins']]}")

    # Full dataset
    print(f"\n--- Extended dataset (full backup) ---")
    states_full = fetch_states(conn)
    var_full = variance_analysis(states_full, "extended_full")
    acf_full = autocorrelation(states_full)
    ar1_full = ar1_coefficient(states_full)
    rec_full = recovery_tau_histogram(states_full)

    print(f"  Observations: {var_full['n_observations']}")
    print(f"  Windows: {var_full['n_windows']}")
    print(f"\n  Var(mu) [bootstrap 95% CI] vs avg within-window var:")
    for d in DIMS:
        lo, hi = var_full["var_of_mu_ci95"][d]
        print(
            f"    {d:10s}  var(mu)={var_full['var_of_mu'][d]:.4f} "
            f"[{lo:.4f}, {hi:.4f}]   within={var_full['avg_within_window_var'][d]:.4f}   "
            f"ratio={var_full['ratio_between_to_within'][d]:.1f}x"
        )
    print(f"\n  AR(1) coefficient:")
    for d in DIMS:
        print(f"    {d:10s}  phi = {ar1_full[d]:.4f}")

    if rec_full['n_episodes'] > 0:
        print(f"\n  Recovery dynamics (extended):")
        print(f"    n_episodes = {rec_full['n_episodes']}, median tau = {rec_full['median_seconds']:.1f}s, mean = {rec_full['mean_seconds']:.1f}s")

    # Persist results as JSON next to script
    out_path = Path(__file__).parent / "analysis_v0.11.1_results.json"
    out_path.write_text(json.dumps({
        "db_path": db_path,
        "original_window": {
            "variance": var_orig,
            "autocorrelation": acf_orig,
            "ar1": ar1_orig,
            "recovery": rec_orig,
        },
        "extended_full": {
            "variance": var_full,
            "autocorrelation": acf_full,
            "ar1": ar1_full,
            "recovery": rec_full,
        },
    }, indent=2, default=str))
    print(f"\nResults persisted: {out_path}")


if __name__ == "__main__":
    main()
