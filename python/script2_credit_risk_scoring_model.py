import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

df = pd.read_csv("data/borrowers_data.csv")
os.makedirs("outputs", exist_ok=True)

def calculate_risk_score(row):
    """
    Weighted scorecard — 7 factors, weights sum to 1.0
    Each factor scored 1 (best) to 10 (worst).
    """
    scores = {}

    # Factor 1: DSCR (weight 25%)
    d = row["dscr"]
    scores["dscr"] = (1 if d >= 2.0 else 3 if d >= 1.50 else
                      5 if d >= 1.25 else 7 if d >= 1.10 else 9)

    # Factor 2: Debt/EBITDA (weight 20%)
    de = row["debt_to_ebitda"]
    scores["debt_ebitda"] = (1 if de <= 2.0 else 3 if de <= 3.0 else
                              5 if de <= 4.0 else 7 if de <= 5.0 else 9)

    # Factor 3: Interest Coverage (weight 15%)
    ic = row["interest_coverage"]
    scores["icr"] = (1 if ic >= 5.0 else 3 if ic >= 4.0 else
                     5 if ic >= 3.0 else 7 if ic >= 2.0 else 9)

    # Factor 4: Current Ratio (weight 10%)
    cr = row["current_ratio"]
    scores["curr_ratio"] = (1 if cr >= 2.0 else 3 if cr >= 1.5 else
                             5 if cr >= 1.2 else 7 if cr >= 1.0 else 9)

    # Factor 5: Industry Risk (weight 15%)
    industry_risk = {
        "Healthcare": 2, "Technology": 4, "Real Estate": 4,
        "Logistics": 5, "Retail": 6, "Manufacturing": 7
    }
    scores["industry"] = industry_risk.get(row["industry"], 5)

    # Factor 6: Loan Status (weight 10%)
    status_risk = {"Active": 3, "Watchlist": 7, "Defaulted": 10}
    scores["loan_status"] = status_risk.get(row["loan_status"], 5)

    # Factor 7: Net Margin (weight 5%)
    nm = row["net_income"] / row["revenue"] if row["revenue"] > 0 else 0
    scores["net_margin"] = (1 if nm >= 0.10 else 3 if nm >= 0.06 else
                             5 if nm >= 0.03 else 7 if nm > 0 else 10)

    weights = {
        "dscr": 0.25, "debt_ebitda": 0.20, "icr": 0.15,
        "curr_ratio": 0.10, "industry": 0.15,
        "loan_status": 0.10, "net_margin": 0.05
    }

    weighted = sum(scores[k] * weights[k] for k in scores)
    return round(weighted, 2)

df["model_score"]  = df.apply(calculate_risk_score, axis=1)
df["model_rating"] = df["model_score"].round(0).astype(int)
df["risk_class"]   = df["model_rating"].apply(
    lambda x: "Low Risk"      if x <= 3 else
              "Moderate Risk" if x <= 6 else
              "High Risk"     if x <= 8 else "Critical Risk")
df["decision"] = df["model_rating"].apply(
    lambda x: "Approve"              if x <= 3 else
              "Conditional Approval" if x <= 6 else
              "Escalate"             if x <= 8 else "Decline")

out = df[["company_name","industry","model_score","model_rating",
          "risk_class","decision","loan_status"]].sort_values("model_score", ascending=False)
out.to_csv("outputs/risk_scores.csv", index=False)
print("✓ Risk scores saved → outputs/risk_scores.csv")

# ── Chart ──────────────────────────────────────────────────
color_map = {
    "Low Risk": "#63B179", "Moderate Risk": "#EF9F27",
    "High Risk": "#E88040", "Critical Risk": "#E24B4A"
}
colors = out["risk_class"].map(color_map)
fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(out["company_name"], out["model_score"],
               color=colors, edgecolor="white", linewidth=0.4)
ax.set_xlabel("Risk Score (1 = Safest, 10 = Riskiest)", fontsize=11)
ax.set_title("Credit Risk Scorecard — Portfolio Risk Rating\nFY 2024",
             fontsize=13, fontweight="bold", pad=15)
ax.set_facecolor("#F9F9F9")
fig.patch.set_facecolor("white")
handles = [mpatches.Patch(color=v, label=k) for k, v in color_map.items()]
ax.legend(handles=handles, loc="lower right", fontsize=9)
for bar, val in zip(bars, out["model_score"]):
    ax.text(val + 0.05, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}", va="center", fontsize=8.5)
plt.tight_layout()
plt.savefig("outputs/chart_risk_scores.png", dpi=150, bbox_inches="tight")
plt.show()
print("✓ Chart saved → outputs/chart_risk_scores.png")