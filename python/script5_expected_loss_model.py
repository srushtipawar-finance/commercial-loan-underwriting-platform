import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

df = pd.read_csv("data/borrowers_data.csv")
pd_df = pd.read_csv("outputs/pd_model_output.csv")
os.makedirs("outputs", exist_ok=True)

# ── Merge PD into main data ──────────────────────────────────
df = df.merge(pd_df[["company_name","pd_pct"]], on="company_name", how="left")

# ── Parameters ──────────────────────────────────────────────
# LGD: Loss Given Default — varies by collateral quality
def get_lgd(row):
    if row["loan_status"] == "Defaulted":
        return 0.55  # higher loss in default
    elif row["risk_rating"] >= 7:
        return 0.40
    elif row["risk_rating"] >= 5:
        return 0.35
    else:
        return 0.25

df["lgd"]           = df.apply(get_lgd, axis=1)
df["pd_decimal"]    = df["pd_pct"] / 100
df["ead"]           = df["loan_amount"]  # EAD = full outstanding balance
df["expected_loss"] = (df["pd_decimal"] * df["lgd"] * df["ead"]).round(0)

# ── Risk classification by EL ────────────────────────────────
df["el_class"] = df["expected_loss"].apply(
    lambda x: "Low EL (<$100K)"       if x < 100000 else
              "Moderate EL ($100K–$500K)" if x < 500000 else
              "High EL (>$500K)")

# ── Output ───────────────────────────────────────────────────
out_cols = ["company_name","industry","loan_amount","pd_pct","lgd",
            "ead","expected_loss","el_class","risk_rating","loan_status"]
out = df[out_cols].sort_values("expected_loss", ascending=False)
out.to_csv("outputs/expected_loss_output.csv", index=False)

print("=" * 70)
print("EXPECTED LOSS MODEL — COMMERCIAL BANKING PORTFOLIO")
print("Basel II Framework: EL = PD × LGD × EAD")
print("=" * 70)
print(f"\nPortfolio Total EAD:            ${df['ead'].sum():>15,.0f}")
print(f"Portfolio Total Expected Loss:  ${df['expected_loss'].sum():>15,.0f}")
print(f"EL as % of Portfolio:           {df['expected_loss'].sum()/df['ead'].sum()*100:.2f}%")
print(f"\nAnchor Borrower (Midwest Precision Parts LLC):")
mpp = df[df["company_name"] == "Midwest Precision Parts LLC"].iloc[0]
print(f"  PD:             {mpp['pd_pct']:.1f}%")
print(f"  LGD:            {mpp['lgd']*100:.0f}%")
print(f"  EAD:            ${mpp['ead']:,.0f}")
print(f"  Expected Loss:  ${mpp['expected_loss']:,.0f}")
print("=" * 70)
print(out.to_string(index=False))

# ── Chart 1: EL by borrower ──────────────────────────────────
color_map = {
    "Low EL (<$100K)": "#63B179",
    "Moderate EL ($100K–$500K)": "#EF9F27",
    "High EL (>$500K)": "#E24B4A"
}
colors = out["el_class"].map(color_map)
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

bars = axes[0].barh(out["company_name"], out["expected_loss"] / 1000,
                    color=colors, edgecolor="white", linewidth=0.4)
axes[0].set_xlabel("Expected Loss ($000s)", fontsize=10)
axes[0].set_title("Expected Loss by Borrower\nEL = PD × LGD × EAD",
                  fontsize=11, fontweight="bold")
axes[0].set_facecolor("#F9F9F9")
for bar, val in zip(bars, out["expected_loss"]):
    axes[0].text(val/1000 + 1, bar.get_y() + bar.get_height()/2,
                 f"${val/1000:.0f}K", va="center", fontsize=8)
handles = [mpatches.Patch(color=v, label=k) for k, v in color_map.items()]
axes[0].legend(handles=handles, loc="lower right", fontsize=8)

# ── Chart 2: EL by industry ──────────────────────────────────
el_ind = df.groupby("industry")["expected_loss"].sum().sort_values(ascending=True)
ind_colors = ["#E24B4A" if v > 500000 else "#EF9F27" if v > 200000
              else "#63B179" for v in el_ind.values]
bars2 = axes[1].barh(el_ind.index, el_ind.values / 1000,
                     color=ind_colors, edgecolor="white")
axes[1].set_xlabel("Total Expected Loss ($000s)", fontsize=10)
axes[1].set_title("Expected Loss by Industry\n($000s)", fontsize=11, fontweight="bold")
axes[1].set_facecolor("#F9F9F9")
for bar, val in zip(bars2, el_ind.values):
    axes[1].text(val/1000 + 1, bar.get_y() + bar.get_height()/2,
                 f"${val/1000:.0f}K", va="center", fontsize=9)

fig.patch.set_facecolor("white")
plt.suptitle("Expected Loss Analysis — Basel II Framework | FY 2024",
             fontsize=13, fontweight="bold")
plt.tight_layout()
plt.savefig("outputs/chart_expected_loss.png", dpi=150, bbox_inches="tight")
plt.show()
print("✓ EL chart saved → outputs/chart_expected_loss.png")