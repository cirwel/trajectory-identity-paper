#!/usr/bin/env python3
"""
Resident-discrimination pilot for the trajectory-identity framework.

Question: can a reduced trajectory signature, computed from the shared
governance EISV+phi state series, distinguish four heterogeneous resident
agents (Lumen, Sentinel, Watcher, Vigil) -- and in particular the three
*software* residents whose marginal state distributions overlap?

State per check-in: [E, I, S, V, phi]  (coherence dropped -- degenerate,
~0.49 +/- 0.006 across all agents). Reduced signature per window:
  alpha (attractor basin) : per-dim mean (5) + per-dim std (5)
  rho   (recovery profile): per-dim lag-1 autocorrelation (5)
  Delta (relational disp.): upper-triangle of the 5x5 corr matrix (10)
-> 25-D window signature.

Two discriminability tests:
  1. within- vs between-agent separation in signature space (silhouette,
     distance-ratio) + a windows x windows distance heatmap.
  2. held-out classifier with a TEMPORAL split (train = first 70% of each
     agent's windows, test = last 30%) so adjacent-window leakage and
     same-period memorization cannot inflate the score. Confusion matrix +
     per-class accuracy, reported for all-4 and for the 3 software residents.

Honest scope: four agents, all from one operator's fleet, all governance
metrics -- a within-ecosystem pilot, not an external-population validation.
"""
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, silhouette_score

RNG = 20260602
W = 200                         # window size (consecutive check-ins)
DIMS = ["e", "i", "s", "v", "phi"]
SOFTWARE = ["Sentinel", "Watcher", "Vigil"]
HERE = __file__.rsplit("/", 1)[0]


def lag1_autocorr(x):
    x = np.asarray(x, float)
    if x.std() < 1e-9 or len(x) < 3:
        return 0.0
    a, b = x[:-1], x[1:]
    if a.std() < 1e-9 or b.std() < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def window_signature(win):
    """win: (W, 5) array -> 25-D signature [mean5, std5, ar1_5, corr10]."""
    mean = win.mean(0)                      # alpha center
    std = win.std(0)                        # alpha spread
    ar1 = np.array([lag1_autocorr(win[:, k]) for k in range(win.shape[1])])  # rho
    c = np.corrcoef(win.T)                  # Delta
    c = np.nan_to_num(c, nan=0.0)
    iu = np.triu_indices(win.shape[1], k=1)
    corr = c[iu]
    return np.concatenate([mean, std, ar1, corr])


def build_windows(df):
    sigs, labels, times = [], [], []
    for ag, g in df.groupby("agent"):
        g = g.sort_values("recorded_at")
        X = g[DIMS].to_numpy(float)
        t = g["recorded_at"].to_numpy()
        n = (len(X) // W)
        for j in range(n):
            seg = X[j * W:(j + 1) * W]
            sigs.append(window_signature(seg))
            labels.append(ag)
            times.append(t[j * W])           # window start time
    return np.array(sigs), np.array(labels), np.array(times)


def main():
    df = pd.read_csv(f"{HERE}/resident_states.csv")
    df = df.dropna(subset=DIMS)
    print(f"loaded {len(df)} rows; per-agent: "
          + ", ".join(f"{a}={len(g)}" for a, g in df.groupby('agent')))

    sigs, labels, times = build_windows(df)
    print(f"\n{len(sigs)} windows of {W} check-ins  ("
          + ", ".join(f"{a}={int((labels==a).sum())}" for a in sorted(set(labels))) + ")")

    # standardize signature features (global)
    Z = StandardScaler().fit_transform(sigs)

    # ---- Test 1: within- vs between-agent separation -------------------
    sil = silhouette_score(Z, labels)
    # distance ratio
    from scipy.spatial.distance import pdist, squareform
    D = squareform(pdist(Z))
    same = labels[:, None] == labels[None, :]
    np.fill_diagonal(same, False)
    within = D[same].mean()
    between = D[(~same)].mean()
    print(f"\n[Test 1] silhouette (agent labels) = {sil:.3f}   "
          f"(0=overlapping, 1=cleanly separated)")
    print(f"         mean within-agent signature distance  = {within:.2f}")
    print(f"         mean between-agent signature distance = {between:.2f}")
    print(f"         between/within ratio = {between/within:.2f}  (>1 = discriminable)")

    # ---- Test 2: held-out classifier, TEMPORAL split -------------------
    tr_idx, te_idx = [], []
    for ag in sorted(set(labels)):
        idx = np.where(labels == ag)[0]
        idx = idx[np.argsort(times[idx])]
        cut = int(len(idx) * 0.70)
        tr_idx += list(idx[:cut]); te_idx += list(idx[cut:])
    tr_idx, te_idx = np.array(tr_idx), np.array(te_idx)

    clf = RandomForestClassifier(n_estimators=400, class_weight="balanced",
                                 random_state=RNG)
    clf.fit(Z[tr_idx], labels[tr_idx])
    pred = clf.predict(Z[te_idx])
    ytrue = labels[te_idx]

    order = ["Lumen", "Sentinel", "Watcher", "Vigil"]
    acc4 = accuracy_score(ytrue, pred)
    # 3-software-resident sub-accuracy (rows whose TRUE label is software)
    sw = np.isin(ytrue, SOFTWARE)
    acc3 = accuracy_score(ytrue[sw], pred[sw]) if sw.any() else float("nan")
    print(f"\n[Test 2] held-out (train=first70%/test=last30% by time): "
          f"{len(te_idx)} test windows")
    print(f"         4-way accuracy   = {acc4:.1%}  (chance 25%)")
    print(f"         3-software-resident accuracy (true in {SOFTWARE}) "
          f"= {acc3:.1%}  (chance 33%)")
    cm = confusion_matrix(ytrue, pred, labels=order)
    print("\n         confusion (rows=true, cols=pred):")
    print("         " + " ".join(f"{o[:4]:>6}" for o in order))
    for i, o in enumerate(order):
        print(f"  {o:>9} " + " ".join(f"{v:6d}" for v in cm[i]))

    # ---- Figures -------------------------------------------------------
    colors = {"Lumen": "#d1495b", "Sentinel": "#30638e",
              "Watcher": "#00798c", "Vigil": "#edae49"}

    # Fig 1: state-space (phi vs I), subsampled
    fig, ax = plt.subplots(figsize=(6, 5))
    for ag, g in df.groupby("agent"):
        gs = g.sample(min(1500, len(g)), random_state=RNG)
        ax.scatter(gs["i"], gs["phi"], s=4, alpha=0.25, label=ag,
                   color=colors.get(ag, "gray"))
    ax.set_xlabel("Integrity (I)"); ax.set_ylabel("phi")
    ax.set_title("Resident state distributions (I vs phi)\nLumen separates; "
                 "software residents overlap")
    lg = ax.legend(markerscale=3, framealpha=0.9)
    for h in lg.legend_handles: h.set_alpha(1)
    fig.tight_layout(); fig.savefig(f"{HERE}/fig1_state_space.png", dpi=140)

    # Fig 2: windows x windows signature-distance heatmap, sorted by agent
    sort = np.argsort([order.index(l) for l in labels])
    fig, ax = plt.subplots(figsize=(6, 5.2))
    im = ax.imshow(D[np.ix_(sort, sort)], cmap="viridis_r")
    # agent block boundaries
    cnts = [int((labels == o).sum()) for o in order]
    b = np.cumsum(cnts)
    for x in b[:-1]:
        ax.axhline(x - .5, color="w", lw=.6); ax.axvline(x - .5, color="w", lw=.6)
    pos = [ (b[i] + (b[i-1] if i else 0))/2 - .5 for i in range(len(order)) ]
    ax.set_xticks(pos); ax.set_xticklabels([o[:4] for o in order])
    ax.set_yticks(pos); ax.set_yticklabels(order)
    ax.set_title("Window signature distances (sorted by agent)\n"
                 "block-diagonal = within-agent windows are closer")
    fig.colorbar(im, label="signature distance"); fig.tight_layout()
    fig.savefig(f"{HERE}/fig2_distance_matrix.png", dpi=140)

    # Fig 3: confusion matrix (row-normalized)
    cmn = cm / cm.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(5.2, 4.6))
    im = ax.imshow(cmn, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(4)); ax.set_xticklabels(order, rotation=30, ha="right")
    ax.set_yticks(range(4)); ax.set_yticklabels(order)
    for i in range(4):
        for j in range(4):
            ax.text(j, i, f"{cmn[i,j]:.0%}", ha="center", va="center",
                    color="white" if cmn[i, j] > .5 else "black", fontsize=9)
    ax.set_xlabel("predicted"); ax.set_ylabel("true")
    ax.set_title(f"Held-out classification (temporal split)\n"
                 f"4-way {acc4:.0%} (chance 25%) | software-only {acc3:.0%} (chance 33%)")
    fig.colorbar(im, label="row-normalized"); fig.tight_layout()
    fig.savefig(f"{HERE}/fig3_confusion.png", dpi=140)

    print(f"\nfigures written to {HERE}/fig1_state_space.png, fig2_distance_matrix.png, fig3_confusion.png")
    # machine-readable summary
    print("\nSUMMARY", {"windows": len(sigs), "silhouette": round(sil, 3),
                         "between_within_ratio": round(between/within, 2),
                         "acc4": round(acc4, 3), "acc3_software": round(acc3, 3)})


if __name__ == "__main__":
    main()
