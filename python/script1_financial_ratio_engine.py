import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# ── Load data ──────────────────────────────────────────────
df = pd.read_csv("data/borrowers_data.csv")
os.makedirs("outputs", exist_ok=True)

# ── Recalculate all ratios from raw financials ──────────────
df["dscr_calc"]     = (df["cash_from_ops"] / df["annual_debt_service"]).round(2)
df["debt_ebitda"]   = (df["total_debt"] / df["ebitda"]).round(2)
df["icr"]           = (df["ebitda"] / df["interest_expense"]).round(2)
df["curr_ratio"]    = (df["current_assets"] / df["current_liabilities"]).round(2)
df["gross_margin"]  = ((df["revenue"] - df["revenue"] * 0.65) / df["revenue"]).round(4)
df["net_margin"]    = (df["net_income"] / df["revenue"]).round(4)

# ── Flag pass/fail vs thresholds ────────────────────────────
df["dscr_flag"]       = df["dscr_calc"].apply(
    lambda x: "BREACH"      if x < 1.10 else
              "WATCH"       if x < 1.25 else "PASS")
df["leverage_flag"]   = df["debt_ebitda"].apply(
    lambda x: "HIGH"        if x > 5.0  else
              "ELEVATED"    if x > 4.0  else "ACCEPTABLE")
df["icr_flag"]        = df["icr"].apply(
    lambda x: "INSUFFICIENT" if x < 2.0 else
              "MARGINAL"     if x < 3.0 else "ADEQUATE")

# ── Summary output ───────────────────────────────────────────
output_cols = [
    "company_name", "industry",
    "dscr_calc", "dscr_flag",
    "debt_ebitda", "leverage_flag",
    "icr", "icr_flag",
    "curr_ratio", "risk_rating", "loan_status"
]
summary = df[output_cols].sort_values("dscr_calc")
summary.to_csv("outputs/ratio_summary.csv", index=False)
print("✓ Ratio summary saved → outputs/ratio_summary.csv")
print(summary.to_string(index=False))

# ── Chart: DSCR across portfolio ─────────────────────────────
colors = summary["dscr_flag"].map(
    {"BREACH": "#E24B4A", "WATCH": "#EF9F27", "PASS": "#63B179"})

fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(summary["company_name"], summary["dscr_calc"],
               color=colors, edgecolor="white", linewidth=0.5)

ax.axvline(x=1.10, color="#A32D2D", linestyle="--", linewidth=1.5,
           label="Covenant floor (1.10x)")
ax.axvline(x=1.25, color="#854F0B", linestyle="--", linewidth=1.5,
           label="Benchmark (1.25x)")

ax.set_xlabel("DSCR", fontsize=11)
ax.set_title("Portfolio DSCR — Midwest Commercial Banking Portfolio\nFY 2024",
             fontsize=13, fontweight="bold", pad=15)
ax.set_facecolor("#F9F9F9")
fig.patch.set_facecolor("white")

legend_handles = [
    mpatches.Patch(color="#E24B4A", label="BREACH (<1.10x)"),
    mpatches.Patch(color="#EF9F27", label="WATCH (1.10–1.25x)"),
    mpatches.Patch(color="#63B179", label="PASS (>1.25x)"),
]
ax.legend(handles=legend_handles + [
    plt.Line2D([0],[0], color="#A32D2D", linestyle="--", label="Covenant floor (1.10x)"),
    plt.Line2D([0],[0], color="#854F0B", linestyle="--", label="Benchmark (1.25x)")
], loc="lower right", fontsize=9)

for bar, val in zip(bars, summary["dscr_calc"]):
    ax.text(val + 0.03, bar.get_y() + bar.get_height() / 2,
            f"{val:.2f}x", va="center", fontsize=8.5)

plt.tight_layout()
plt.savefig("outputs/chart_dscr_portfolio.png", dpi=150, bbox_inches="tight")
plt.show()
print("✓ Chart saved → outputs/chart_dscr_portfolio.png")