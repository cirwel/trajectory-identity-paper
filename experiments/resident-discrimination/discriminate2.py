#!/usr/bin/env python3
"""
Resident-discrimination pilot, part 2: does the *similarity primitive* work?

Part 1 found: a trained RandomForest discriminates (60% 4-way / 52% software)
but naive distance does not (silhouette ~0). This script tests whether the
paper's OWN proposal -- weight signature components by informativeness
(sec 4.1) -- rescues the similarity primitive, and pins down significance and
which components carry the signal.

Adds over part 1:
  A. window-size robustness (W in {100,150,200,300}), RF temporal split.
  B. three discriminators at W=150, all with the SAME temporal split:
       - naive nearest-centroid (the unweighted similarity primitive)
       - informativeness-weighted nearest-centroid (weights = F-stat on TRAIN
         only -> leakage-free; this is the paper's proposed primitive)
       - RandomForest (supervised reference ceiling)
  C. permutation null (shuffle labels, refit) -> empirical p for acc4/acc3.
  D. top informative signature components (named).

Leakage discipline: all feature weights / centroids / scalers fit on TRAIN
windows only (train = each agent's earliest 70% by time).
"""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import f_classif
from sklearn.metrics import accuracy_score

RNG = 20260602
DIMS = ["e", "i", "s", "v", "phi"]
SOFTWARE = ["Sentinel", "Watcher", "Vigil"]
ORDER = ["Lumen", "Sentinel", "Watcher", "Vigil"]
HERE = __file__.rsplit("/", 1)[0]
np.random.seed(RNG)

FEAT_NAMES = ([f"mean_{d.upper()}" for d in DIMS] +
              [f"std_{d.upper()}" for d in DIMS] +
              [f"ar1_{d.upper()}" for d in DIMS] +
              [f"corr_{DIMS[a].upper()}{DIMS[b].upper()}"
               for a in range(5) for b in range(a + 1, 5)])


def lag1(x):
    x = np.asarray(x, float)
    if x.std() < 1e-9 or len(x) < 3: return 0.0
    a, b = x[:-1], x[1:]
    if a.std() < 1e-9 or b.std() < 1e-9: return 0.0
    return float(np.corrcoef(a, b)[0, 1])


def sig(win):
    mean, std = win.mean(0), win.std(0)
    ar1 = np.array([lag1(win[:, k]) for k in range(win.shape[1])])
    c = np.nan_to_num(np.corrcoef(win.T), nan=0.0)
    iu = np.triu_indices(win.shape[1], 1)
    return np.concatenate([mean, std, ar1, c[iu]])


def windows(df, W):
    S, L, T = [], [], []
    for ag, g in df.groupby("agent"):
        g = g.sort_values("recorded_at"); X = g[DIMS].to_numpy(float)
        t = g["recorded_at"].to_numpy()
        for j in range(len(X) // W):
            S.append(sig(X[j*W:(j+1)*W])); L.append(ag); T.append(t[j*W])
    return np.array(S), np.array(L), np.array(T)


def temporal_split(L, T, frac=0.70):
    tr, te = [], []
    for ag in ORDER:
        idx = np.where(L == ag)[0]; idx = idx[np.argsort(T[idx])]
        cut = int(len(idx) * frac); tr += list(idx[:cut]); te += list(idx[cut:])
    return np.array(tr), np.array(te)


def sub_acc(y, p):
    acc4 = accuracy_score(y, p)
    m = np.isin(y, SOFTWARE)
    acc3 = accuracy_score(y[m], p[m]) if m.any() else np.nan
    return acc4, acc3


def nearest_centroid(Ztr, ytr, Zte, w=None):
    w = np.ones(Ztr.shape[1]) if w is None else w
    cents = {a: Ztr[ytr == a].mean(0) for a in ORDER if (ytr == a).any()}
    keys = list(cents); C = np.array([cents[k] for k in keys])
    d = np.sqrt(((Zte[:, None, :] - C[None]) ** 2 * w[None, None]).sum(2))
    return np.array(keys)[d.argmin(1)]


def main():
    df = pd.read_csv(f"{HERE}/resident_states.csv").dropna(subset=DIMS)

    # ---- A. window-size robustness (RF) -------------------------------
    print("[A] window-size robustness (RF, temporal split):")
    sweep = {}
    for W in (100, 150, 200, 300):
        S, L, T = windows(df, W)
        sc = StandardScaler().fit(S); Z = sc.transform(S)
        tr, te = temporal_split(L, T)
        clf = RandomForestClassifier(400, class_weight="balanced", random_state=RNG)
        clf.fit(Z[tr], L[tr]); p = clf.predict(Z[te])
        a4, a3 = sub_acc(L[te], p)
        sweep[W] = (a4, a3, len(S), len(te))
        print(f"   W={W:3d}: {len(S):3d} win ({len(te)} test) | "
              f"4-way {a4:.0%} (chance 25%) | software {a3:.0%} (chance 33%)")

    # ---- pick W=150 for the head-to-head -------------------------------
    W = 150
    S, L, T = windows(df, W)
    sc = StandardScaler().fit(S); Z = sc.transform(S)
    tr, te = temporal_split(L, T)
    ytr, yte = L[tr], L[te]

    # informativeness weights from TRAIN only (F-stat per feature)
    F, _ = f_classif(Z[tr], ytr); F = np.nan_to_num(F, nan=0.0)
    w = F / F.sum() * len(F)            # normalized, mean ~1

    print(f"\n[B] discriminators at W={W} ({len(te)} test windows), same split:")
    # naive nearest-centroid (unweighted similarity primitive)
    p_nc = nearest_centroid(Z[tr], ytr, Z[te])
    a4_nc, a3_nc = sub_acc(yte, p_nc)
    # informativeness-weighted nearest-centroid (paper's primitive)
    p_wc = nearest_centroid(Z[tr], ytr, Z[te], w)
    a4_wc, a3_wc = sub_acc(yte, p_wc)
    # RF reference
    rf = RandomForestClassifier(400, class_weight="balanced", random_state=RNG)
    rf.fit(Z[tr], ytr); p_rf = rf.predict(Z[te])
    a4_rf, a3_rf = sub_acc(yte, p_rf)
    print(f"   naive nearest-centroid (unweighted) : 4-way {a4_nc:.0%} | software {a3_nc:.0%}")
    print(f"   informativeness-weighted centroid   : 4-way {a4_wc:.0%} | software {a3_wc:.0%}  <- paper's primitive")
    print(f"   RandomForest (supervised reference) : 4-way {a4_rf:.0%} | software {a3_rf:.0%}")

    # ---- C. permutation null (shuffle labels, refit RF) ---------------
    NPERM = 300
    null4, null3 = [], []
    rs = np.random.RandomState(RNG)
    for _ in range(NPERM):
        yp = rs.permutation(L)
        r = RandomForestClassifier(150, class_weight="balanced", random_state=0)
        r.fit(Z[tr], yp[tr]); pp = r.predict(Z[te])
        b4, b3 = sub_acc(yte, pp); null4.append(b4)
        if not np.isnan(b3): null3.append(b3)
    null4, null3 = np.array(null4), np.array(null3)
    p4 = (null4 >= a4_rf).mean(); p3 = (np.array(null3) >= a3_rf).mean()
    print(f"\n[C] permutation null ({NPERM} label shuffles, RF):")
    print(f"   4-way   observed {a4_rf:.0%} vs null {null4.mean():.0%}±{null4.std():.0%}  -> p={p4:.3f}")
    print(f"   software observed {a3_rf:.0%} vs null {null3.mean():.0%}±{null3.std():.0%}  -> p={p3:.3f}")

    # ---- D. top informative components --------------------------------
    top = np.argsort(F)[::-1][:10]
    print("\n[D] top-10 informative signature components (train F-stat):")
    for k in top:
        print(f"   {FEAT_NAMES[k]:12s} F={F[k]:6.1f}")

    # ---- figures -------------------------------------------------------
    Ws = list(sweep); a4s = [sweep[x][0] for x in Ws]; a3s = [sweep[x][1] for x in Ws]
    fig, ax = plt.subplots(figsize=(5.6, 4.2))
    ax.plot(Ws, [x*100 for x in a4s], "o-", label="4-way (chance 25%)")
    ax.plot(Ws, [x*100 for x in a3s], "s-", label="software-only (chance 33%)")
    ax.axhline(25, ls=":", c="gray"); ax.axhline(33.3, ls=":", c="gray")
    ax.set_xlabel("window size (check-ins)"); ax.set_ylabel("held-out accuracy %")
    ax.set_title("Discrimination accuracy vs window size (RF)"); ax.legend()
    fig.tight_layout(); fig.savefig(f"{HERE}/fig4_window_sweep.png", dpi=140)

    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    x = np.arange(3); methods = ["naive\ncentroid", "weighted\ncentroid", "RandomForest"]
    a4v = [a4_nc, a4_wc, a4_rf]; a3v = [a3_nc, a3_wc, a3_rf]
    ax.bar(x-0.18, [v*100 for v in a4v], 0.36, label="4-way")
    ax.bar(x+0.18, [v*100 for v in a3v], 0.36, label="software-only")
    ax.axhline(25, ls=":", c="gray"); ax.axhline(33.3, ls=":", c="gray")
    ax.set_xticks(x); ax.set_xticklabels(methods)
    ax.set_ylabel("held-out accuracy %")
    ax.set_title(f"Does the similarity primitive work? (W={W})")
    ax.legend(); fig.tight_layout(); fig.savefig(f"{HERE}/fig5_primitive.png", dpi=140)

    print("\nSUMMARY", {"sweep": {k: (round(v[0],3), round(v[1],3)) for k,v in sweep.items()},
        "naive_centroid": (round(a4_nc,3), round(a3_nc,3)),
        "weighted_centroid": (round(a4_wc,3), round(a3_wc,3)),
        "rf": (round(a4_rf,3), round(a3_rf,3)),
        "perm_p_4way": round(float(p4),3), "perm_p_software": round(float(p3),3)})


if __name__ == "__main__":
    main()
