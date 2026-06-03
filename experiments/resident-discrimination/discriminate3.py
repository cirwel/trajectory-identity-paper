#!/usr/bin/env python3
"""
Part 3: pin down the two surprising results from part 2 before trusting them.

  (i)  naive equal-weight nearest-centroid BEAT both RandomForest and the
       informativeness-weighted centroid. Is the "weighting hurts" result an
       artifact of one aggressive F-stat scheme, or robust across weightings?
  (ii) the 4-way RF number was NOT significant vs a permutation null (p=.073,
       inflated by Lumen's majority), but software-only WAS (p<.001). Re-run
       the null for the WINNING method (equal-weight centroid) so the headline
       number carries its own p-value, and break out per-agent recall.

Weighting variants (all fit on TRAIN windows only -> leakage-free):
  equal           : w = 1                       (naive similarity primitive)
  sqrt-F          : w = sqrt(F-stat)            (gentle informativeness)
  F               : w = F-stat                  (paper's Fisher proposal, linear)
  inv-within-var  : w = 1/within-agent variance (paper's deployable heuristic)
"""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import f_classif
from sklearn.metrics import accuracy_score, confusion_matrix
import warnings; warnings.filterwarnings("ignore")

RNG = 20260602; W = 150
DIMS = ["e", "i", "s", "v", "phi"]
SOFTWARE = ["Sentinel", "Watcher", "Vigil"]; ORDER = ["Lumen","Sentinel","Watcher","Vigil"]
HERE = __file__.rsplit("/", 1)[0]


def lag1(x):
    x=np.asarray(x,float)
    if x.std()<1e-9 or len(x)<3: return 0.0
    a,b=x[:-1],x[1:]
    if a.std()<1e-9 or b.std()<1e-9: return 0.0
    return float(np.corrcoef(a,b)[0,1])

def sig(win):
    c=np.nan_to_num(np.corrcoef(win.T),nan=0.0); iu=np.triu_indices(5,1)
    return np.concatenate([win.mean(0),win.std(0),
        [lag1(win[:,k]) for k in range(5)], c[iu]])

def windows(df,W):
    S,L,T=[],[],[]
    for ag,g in df.groupby("agent"):
        g=g.sort_values("recorded_at"); X=g[DIMS].to_numpy(float); t=g["recorded_at"].to_numpy()
        for j in range(len(X)//W): S.append(sig(X[j*W:(j+1)*W])); L.append(ag); T.append(t[j*W])
    return np.array(S),np.array(L),np.array(T)

def split(L,T,frac=.70):
    tr,te=[],[]
    for ag in ORDER:
        idx=np.where(L==ag)[0]; idx=idx[np.argsort(T[idx])]; cut=int(len(idx)*frac)
        tr+=list(idx[:cut]); te+=list(idx[cut:])
    return np.array(tr),np.array(te)

def nc(Ztr,ytr,Zte,w):
    ks=[a for a in ORDER if (ytr==a).any()]; C=np.array([Ztr[ytr==a].mean(0) for a in ks])
    d=np.sqrt(((Zte[:,None,:]-C[None])**2*w[None,None]).sum(2)); return np.array(ks)[d.argmin(1)]

def sub(y,p):
    m=np.isin(y,SOFTWARE); return accuracy_score(y,p),(accuracy_score(y[m],p[m]) if m.any() else np.nan)

def main():
    df=pd.read_csv(f"{HERE}/resident_states.csv").dropna(subset=DIMS)
    S,L,T=windows(df,W); Z=StandardScaler().fit_transform(S)
    tr,te=split(L,T); ytr,yte=L[tr],L[te]
    F,_=f_classif(Z[tr],ytr); F=np.nan_to_num(F,nan=0.0)
    wvar=1.0/np.array([Z[tr][ytr==a].var(0) for a in ORDER]).mean(0).clip(1e-6)

    schemes={"equal":np.ones(Z.shape[1]),
             "sqrt-F":np.sqrt(F), "F":F, "inv-within-var":wvar}
    print(f"[i] nearest-centroid by weighting scheme (W={W}, {len(te)} test windows):")
    res={}
    for name,w in schemes.items():
        w=w/ w.sum()*len(w) if w.sum()>0 else w
        a4,a3=sub(yte,nc(Z[tr],ytr,Z[te],w)); res[name]=(a4,a3)
        tag=" <- paper Fisher" if name=="F" else (" <- paper heuristic" if name=="inv-within-var" else "")
        print(f"   {name:14s}: 4-way {a4:.0%} | software {a3:.0%}{tag}")

    # permutation null for the WINNER (equal-weight centroid)
    weq=np.ones(Z.shape[1])
    a4o,a3o=sub(yte,nc(Z[tr],ytr,Z[te],weq))
    rs=np.random.RandomState(RNG); n4,n3=[],[]
    for _ in range(2000):
        yp=rs.permutation(L)
        a4,a3=sub(yte,nc(Z[tr],yp[tr],Z[te],weq)); n4.append(a4)
        if not np.isnan(a3): n3.append(a3)
    n4,n3=np.array(n4),np.array(n3)
    print(f"\n[ii] permutation null (2000 shuffles) for equal-weight centroid:")
    print(f"   4-way    observed {a4o:.0%} vs null {n4.mean():.0%}±{n4.std():.0%}  p={(n4>=a4o).mean():.4f}")
    print(f"   software observed {a3o:.0%} vs null {n3.mean():.0%}±{n3.std():.0%}  p={(np.array(n3)>=a3o).mean():.4f}")

    # per-agent recall under equal-weight centroid
    p=nc(Z[tr],ytr,Z[te],weq); cm=confusion_matrix(yte,p,labels=ORDER)
    print("\n   per-agent recall (equal-weight centroid):")
    for i,a in enumerate(ORDER):
        tot=cm[i].sum(); rec=cm[i,i]/tot if tot else np.nan
        print(f"     {a:9s} {cm[i,i]}/{tot} = {rec:.0%}   test windows={tot}")

    # figure: weighting schemes
    fig,ax=plt.subplots(figsize=(6.4,4.2)); x=np.arange(len(schemes))
    ax.bar(x-0.18,[res[k][0]*100 for k in schemes],0.36,label="4-way")
    ax.bar(x+0.18,[res[k][1]*100 for k in schemes],0.36,label="software-only")
    ax.axhline(25,ls=":",c="gray"); ax.axhline(33.3,ls=":",c="gray")
    ax.set_xticks(x); ax.set_xticklabels(list(schemes),rotation=15)
    ax.set_ylabel("held-out accuracy %")
    ax.set_title("Naive vs informativeness-weighted similarity\n(equal weight wins; the paper's §4.1 weightings do not help)")
    ax.legend(); fig.tight_layout(); fig.savefig(f"{HERE}/fig6_weighting.png",dpi=140)
    print("\nSUMMARY",{k:(round(v[0],3),round(v[1],3)) for k,v in res.items()},
          "| perm_p software=",round(float((np.array(n3)>=a3o).mean()),4))

if __name__=="__main__": main()
