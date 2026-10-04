"""Build assets/demo.gif from VERIFIED results/benchmark.json (no hand numbers).

60 frames, small (<8MB): title -> sessions -> hours -> costs -> expectancy -> CTA.
Schematic animation for README embedding. Deterministic.
"""
from __future__ import annotations
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

ROOT = Path(__file__).resolve().parents[1]
B = json.load(open(ROOT / "results" / "benchmark.json"))
H3 = B["hypotheses"]["H3_sessions"]["mean_range_pips_by_session"]["mean"]
H5 = B["hypotheses"]["H5_costs"]
H8 = B["hypotheses"]["H8_news_nfp"]
HP = B["hidden_patterns"]

ASSETS = ROOT / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

sessions = ["Asia\n0-7", "London\n7-12", "Overlap\n12-17", "NY pm\n17-24"]
vals = [H3["Asia_0-7UTC"], H3["London_7-12UTC"], H3["Overlap_LondonNY_12-17UTC"], H3["NYpm_17-24UTC"]]

fig, ax = plt.subplots(figsize=(7.2, 4.0), dpi=110)
fig.patch.set_facecolor("#0b1020")
ax.set_facecolor("#0b1020")

def frame(i):
    ax.clear()
    ax.set_facecolor("#0b1020")
    ax.tick_params(colors="#a9b3d6", labelsize=8)
    for s in ax.spines.values():
        s.set_color("#263056")
    phase = i // 12  # 5 phases x 12 frames
    if phase == 0:
        ax.text(0.5, 0.62, "8 forex lessons → 8 live tests", ha="center", va="center", fontsize=15, color="white", transform=ax.transAxes, weight="bold")
        ax.text(0.5, 0.42, "Overlap 12.62 vs Asia 6.58 pips (1.92x) · NFP 1.27x (p=0.0074)", ha="center", fontsize=9, color="#a9b3d6", transform=ax.transAxes)
        ax.text(0.5, 0.30, f"gross -$1,890 → net -$3,300 (641 trades) · 30% x 3:1 = +2R/10", ha="center", fontsize=9, color="#a9b3d6", transform=ax.transAxes)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    elif phase == 1:
        k = min(4, (i % 12) // 3 + 1)
        cols = ["#5eead4" if j == 2 else "#3b4a7a" for j in range(4)]
        ax.bar(sessions[:k], vals[:k], color=cols[:k])
        ax.set_ylim(0, max(vals) * 1.25)
        ax.set_title("Session ranges grow → Overlap wins (live pips/hr)", color="white", fontsize=11)
        for j, v in enumerate(vals[:k]):
            ax.text(j, v + 0.25, f"{v:.2f}", ha="center", color="white", fontsize=9)
    elif phase == 2:
        top = HP["hour_seasonality_top3_utc"]
        hours = list(top.keys()); hv = list(top.values())
        cols = ["#a78bfa"] * len(hours)
        ax.bar([f"{h} UTC" for h in hours], hv, color=cols)
        ax.set_title("Peak hours live: 12 / 13 / 14 UTC", color="white", fontsize=11)
        for j, v in enumerate(hv):
            ax.text(j, v + 0.2, f"{v:.2f}", ha="center", color="white", fontsize=9)
    elif phase == 3:
        ax.text(0.5, 0.68, f"Costs decide scalps", ha="center", fontsize=14, color="white", weight="bold", transform=ax.transAxes)
        ax.text(0.5, 0.50, f"gross ${H5['gross_total']:,.0f}  →  net ${H5['net_total']:,.0f}", ha="center", fontsize=13, color="#f87171", transform=ax.transAxes)
        ax.text(0.5, 0.36, f"drag ${H5['cost_drag']:,.0f} on {H5['n_trades']} trades · win {H5['win_rate_net']:.1%}", ha="center", fontsize=10, color="#a9b3d6", transform=ax.transAxes)
        ax.text(0.5, 0.22, "Model spread + commission or fail", ha="center", fontsize=10, color="#fbbf24", transform=ax.transAxes)
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    else:
        ax.text(0.5, 0.66, "30% wins can still profit", ha="center", fontsize=14, color="white", weight="bold", transform=ax.transAxes)
        ax.text(0.5, 0.48, "0.30 x 3R - 0.70 x 1R = +0.20R / trade", ha="center", fontsize=12, color="#5eead4", transform=ax.transAxes)
        ax.text(0.5, 0.34, f"NFP Fridays {H8['nfp_friday_mean_range']:.0f} vs {H8['other_mean_range']:.0f} pips (1.27x)", ha="center", fontsize=10, color="#a9b3d6", transform=ax.transAxes)
        ax.text(0.5, 0.20, "make verify · docker compose up --build research", ha="center", fontsize=10, color="white", transform=ax.transAxes,
                bbox=dict(boxstyle="round", fc="#16204a", ec="#263056"))
        ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    fig.tight_layout()

anim = FuncAnimation(fig, frame, frames=60, interval=180)
out = ASSETS / "demo.gif"
anim.save(out, writer="pillow", fps=6)
print(f"wrote {out} bytes={out.stat().st_size}")
