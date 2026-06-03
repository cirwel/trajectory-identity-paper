#!/usr/bin/env python3
"""
Synthetic, distribution-preserving reproducibility artifact.

Goal: let a reviewer re-run the §6.5 discrimination pipeline WITHOUT access to
production rows. We fit a per-agent VAR(1) model to each resident's real
(E,I,S,V,phi) series and simulate a synthetic series of the same length. A VAR(1)
preserves exactly the structure the reduced signature reads:
  x_t - mu = A (x_{t-1} - mu) + e_t,  e_t ~ N(0, Sigma_e)
  -> stationary mean (alpha center), stationary covariance (alpha spread + Delta
     correlations), and lag-1 autocovariance A*Cov (rho autocorrelation).

HONEST SCOPE: this validates the PIPELINE (a reviewer reproduces the qualitative
result on data we can release), NOT the empirical claim. Because per-agent VAR(1)
params differ, discriminability is partly built in by construction; the synthetic
artifact is a reproducibility aid, the real numbers (§6.5) stay anchored to private
production data. VAR(1) is Gaussian/linear and will not reproduce the multimodality
visible in the real densities -- a deliberate, stated limitation.

Outputs:  synthetic_states.csv  (RELEASABLE -- no production rows)
          fig7_synthetic_check.png
Self-validates by re-running the discrimination check on the synthetic data.
"""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import f_classif
from sklearn.metrics import accuracy_score
import warnings; warnings.filterwarnings("ignore")

RNG = 20260603
DIMS = ["e", "i", "s", "v", "phi"]
ORDER = ["Lumen", "Sentinel", "Watcher", "Vigil"]
SOFTWARE = ["Sentinel", "Watcher", "Vigil"]
HERE = __file__.rsplit("/", 1)[0]
rng = np.random.default_rng(RNG)


def fit_var1(X):
    """Least-squares VAR(1): returns mu, A (5x5), chol(Sigma_e)."""
    mu = X.mean(0)
    Xc = X - mu
    P, Fu = Xc[:-1], Xc[1:]                       # past, future
    A = np.linalg.lstsq(P, Fu, rcond=None)[0].T   # Fu ~ A P  -> A = (P\Fu)^T
    # stability clamp: scale spectral radius below 1 if needed
    ev = np.max(np.abs(np.linalg.eigvals(A)))
    if ev >= 0.999:
        A *= 0.98 / ev
    resid = Fu - Xc[:-1] @ A.T
    Sig = np.cov(resid.T)
    L = np.linalg.cholesky(Sig + 1e-9 * np.eye(5))
    return mu, A, L


def simulate(mu, A, L, n):
    X = np.zeros((n, 5)); x = np.zeros(5)
    for t in range(n):
        x = A @ x + L @ rng.standard_normal(5)
        X[t] = mu + x
    return X


# ---- fit + simulate per agent ------------------------------------------
real = pd.read_csv(f"{HERE}/resident_states.csv").dropna(subset=DIMS)
rows = []
for ag in ORDER:
    g = real[real.agent == ag].sort_values("recorded_at")
    X = g[DIMS].to_numpy(float)
    mu, A, L = fit_var1(X)
    Xs = simulate(mu, A, L, len(X))
    for r in Xs:
        rows.append([ag, *r])
syn = pd.DataFrame(rows, columns=["agent", *DIMS])
syn.to_csv(f"{HERE}/synthetic_states.csv", index=False)
print(f"wrote synthetic_states.csv: {len(syn)} rows "
      f"({', '.join(f'{a}={int((syn.agent==a).sum())}' for a in ORDER)})")

# ---- fidelity: compare real vs synthetic moments -----------------------
print("\nmoment fidelity (real -> synthetic), per agent:")
for ag in ORDER:
    r = real[real.agent == ag][DIMS]; s = syn[syn.agent == ag][DIMS]
    print(f"  {ag:9s} mean Δ={np.abs(r.mean()-s.mean()).mean():.3f} "
          f"std Δ={np.abs(r.std()-s.std()).mean():.3f} "
          f"ar1(I) {r.i.autocorr(1):.2f}->{s.i.autocorr(1):.2f}")

# ---- self-validate: discrimination pipeline on SYNTHETIC ----------------
W = 150
def lag1(x):
    x=np.asarray(x,float)
    if x.std()<1e-9 or len(x)<3: return 0.0
    a,b=x[:-1],x[1:]
    return float(np.corrcoef(a,b)[0,1]) if a.std()>1e-9 and b.std()>1e-9 else 0.0
def sig(w):
    c=np.nan_to_num(np.corrcoef(w.T),nan=0.0); iu=np.triu_indices(5,1)
    return np.concatenate([w.mean(0),w.std(0),[lag1(w[:,k]) for k in range(5)],c[iu]])
def build(df):
    S,L=[],[]
    for ag in ORDER:
        X=df[df.agent==ag][DIMS].to_numpy(float)
        for j in range(len(X)//W): S.append(sig(X[j*W:(j+1)*W])); L.append(ag)
    return np.array(S),np.array(L)
def nc(Ztr,ytr,Zte,w):
    ks=[a for a in ORDER if (ytr==a).any()]; C=np.array([Ztr[ytr==a].mean(0) for a in ks])
    d=np.sqrt(((Zte[:,None]-C[None])**2*w[None,None]).sum(2)); return np.array(ks)[d.argmin(1)]
def sub(y,p):
    m=np.isin(y,SOFTWARE); return accuracy_score(y,p),accuracy_score(y[m],p[m])

S,L=build(syn); Z=StandardScaler().fit_transform(S)
# temporal-style split: first 70% windows per agent train
tr,te=[],[]
for ag in ORDER:
    idx=np.where(L==ag)[0]; cut=int(len(idx)*0.7); tr+=list(idx[:cut]); te+=list(idx[cut:])
tr,te=np.array(tr),np.array(te); ytr,yte=L[tr],L[te]
F,_=f_classif(Z[tr],ytr); F=np.nan_to_num(F)
a4e,a3e=sub(yte,nc(Z[tr],ytr,Z[te],np.ones(Z.shape[1])))
a4f,a3f=sub(yte,nc(Z[tr],ytr,Z[te],F/F.sum()*len(F)))
print(f"\nSYNTHETIC reproduction ({len(te)} test windows):")
print(f"  equal-weight centroid : 4-way {a4e:.0%} | software {a3e:.0%}")
print(f"  Fisher-weight centroid: 4-way {a4f:.0%} | software {a3f:.0%}")
print(f"  -> reproduces: discrimination works ({a3e:.0%}>chance 33%) AND equal>Fisher ({a3e:.0%}>{a3f:.0%})"
      if a3e>0.45 and a3e>a3f else "  -> DID NOT cleanly reproduce; inspect")

# ---- releasable figure (synthetic only) --------------------------------
colors={"Lumen":"#d1495b","Sentinel":"#30638e","Watcher":"#00798c","Vigil":"#edae49"}
fig,ax=plt.subplots(figsize=(6,5))
for ag in ORDER:
    s=syn[syn.agent==ag].sample(min(1200,(syn.agent==ag).sum()),random_state=RNG)
    ax.scatter(s.i,s.phi,s=5,alpha=0.3,color=colors[ag],label=ag)
ax.set_xlabel("Integrity (I)"); ax.set_ylabel("phi")
ax.set_title("SYNTHETIC resident states (VAR(1), releasable)\n"
             "reproducibility artifact — not production data")
lg=ax.legend(markerscale=2)
for h in lg.legend_handles: h.set_alpha(1)
fig.tight_layout(); fig.savefig(f"{HERE}/fig7_synthetic_check.png",dpi=140)
print("\nwrote fig7_synthetic_check.png (synthetic; fully releasable)")
