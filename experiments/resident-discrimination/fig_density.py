#!/usr/bin/env python3
"""Aggregate replacement for the raw scatter (fig1): per-agent KDE density
contours in (I, phi). Shows the distributional story -- Lumen separates,
software residents overlap -- WITHOUT plotting individual production states.
Output is smoothed density (aggregate), not raw rows."""
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

HERE = __file__.rsplit("/", 1)[0]
df = pd.read_csv(f"{HERE}/resident_states.csv").dropna(subset=["i", "phi"])
colors = {"Lumen": "#d1495b", "Sentinel": "#30638e",
          "Watcher": "#00798c", "Vigil": "#edae49"}

xx, yy = np.mgrid[0.55:0.90:200j, -0.05:0.28:200j]
grid = np.vstack([xx.ravel(), yy.ravel()])
fig, ax = plt.subplots(figsize=(6, 5))
for ag in ["Lumen", "Sentinel", "Watcher", "Vigil"]:
    g = df[df.agent == ag]
    k = gaussian_kde(np.vstack([g.i, g.phi]))
    z = k(grid).reshape(xx.shape)
    # tight high-density CORE (densest region) so separation is visible
    lv = np.quantile(z[z > 0], 0.92)
    ax.contourf(xx, yy, z, levels=[lv, z.max()], colors=[colors[ag]], alpha=0.30)
    ax.contour(xx, yy, z, levels=[lv], colors=[colors[ag]], linewidths=1.4)
    ax.plot(g.i.mean(), g.phi.mean(), "o", color=colors[ag], ms=7,
            mec="white", mew=1.2)
    ax.plot([], [], color=colors[ag], lw=6, alpha=0.5, label=ag)  # legend proxy
ax.set_xlabel("Integrity (I)"); ax.set_ylabel("phi")
ax.set_title("Marginal state densities overlap (I vs phi)\n"
             "agents are NOT separable by location — discrimination needs\n"
             "temporal/joint structure (dots = per-agent means)")
ax.legend(framealpha=0.9)
fig.tight_layout(); fig.savefig(f"{HERE}/fig1b_density.png", dpi=140)
print("wrote fig1b_density.png (aggregate KDE; no individual rows plotted)")
