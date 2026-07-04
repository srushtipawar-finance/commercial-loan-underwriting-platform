import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

df = pd.read_csv("data/borrowers_data.csv")
os.makedirs("outputs", exist_ok=True)

# ── Industry concentration ──────────────────────────────────
conc = df.groupby("industry").agg(
    num_borrowers=("company_name", "count"),
    total_exposure=("loan_amount", "sum")
).reset_index()
conc["pct_of_portfolio"] = (conc["total_exposure"] /
                             conc["total_exposure"].sum() * 100).round(1)

# ── HHI Score ───────────────────────────────────────────────
shares = conc["pct_of_portfolio"] / 100
hhi = round((shares ** 2).sum() * 10000, 0)
hhi_label = ("Highly Concentrated" if hhi > 2500 else
             "Moderately Concentrated" if hhi > 1500 else "Diversified")
print(f"\nHerfindahl-Hirschman Index (HHI): {hhi:.0f} — {hhi_label}")

conc.to_csv("outputs/portfolio_concentration.csv", index=False)
print("✓ Concentration analysis → outputs/portfolio_concentration.csv")
print(conc.to_string(index=False))

# ── Chart 1: Portfolio by Industry (Donut) ─────────────────
colors = ["#1F4E79","#2E75B6","#5BA3C9","#70B8D4","#A8D4E6","#C5E3F0"]
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

wedges, texts, autotexts = axes[0].pie(
    conc["total_exposure"],
    labels=conc["industry"],
    autopct="%1.1f%%",
    colors=colors,
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
    pctdistance=0.82
)
for t in autotexts:
    t.set_fontsize(9)
    t.set_fontweight("bold")

# Draw donut hole
centre_circle = plt.Circle((0, 0), 0.65, fc="white")
axes[0].add_patch(centre_circle)
axes[0].set_title("Portfolio Concentration by Industry\n(% of Total Exposure)",
                  fontsize=11, fontweight="bold")
axes[0].text(0, 0, f"HHI\n{hhi:.0f}", ha="center", va="center",
             fontsize=12, fontweight="bold", color="#1F4E79")

# ── Chart 2: Exposure bar ───────────────────────────────────
conc_sorted = conc.sort_values("total_exposure", ascending=True)
bar_colors = ["#E24B4A" if p > 30 else "#EF9F27" if p > 20 else "#63B179"
              for p in conc_sorted["pct_of_portfolio"]]
bars = axes[1].barh(conc_sorted["industry"],
                    conc_sorted["total_exposure"] / 1e6,
                    color=bar_colors, edgecolor="white")
axes[1].set_xlabel("Total Exposure ($M)", fontsize=10)
axes[1].set_title("Loan Exposure by Industry ($M)\nRed = Overweight (>30%)",
                  fontsize=11, fontweight="bold")
axes[1].set_facecolor("#F9F9F9")
for bar, val in zip(bars, conc_sorted["total_exposure"]):
    axes[1].text(val/1e6 + 0.3, bar.get_y() + bar.get_height()/2,
                 f"${val/1e6:.1f}M", va="center", fontsize=9)

fig.patch.set_facecolor("white")
plt.suptitle("Portfolio Concentration Analysis — HHI Risk Assessment",
             fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("outputs/chart_concentration.png", dpi=150, bbox_inches="tight")
plt.show()
print("✓ Chart saved → outputs/chart_concentration.png")