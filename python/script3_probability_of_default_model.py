import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import os

df = pd.read_csv("data/borrowers_data.csv")
os.makedirs("outputs", exist_ok=True)

# ── Create binary default label ─────────────────────────────
# 1 = default risk (rating 7+), 0 = performing
df["default_label"] = (df["risk_rating"] >= 7).astype(int)

# ── Features ────────────────────────────────────────────────
features = ["dscr", "debt_to_ebitda", "interest_coverage", "current_ratio"]
X = df[features].fillna(df[features].median())
y = df["default_label"]

# ── Scale + fit ──────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LogisticRegression(random_state=42)
model.fit(X_scaled, y)

# ── Predict PD for each borrower ────────────────────────────
df["pd_probability"] = model.predict_proba(X_scaled)[:, 1]
df["pd_pct"]         = (df["pd_probability"] * 100).round(1)

# ── Classification ───────────────────────────────────────────
df["pd_class"] = df["pd_pct"].apply(
    lambda x: "Low (<10%)"       if x < 10 else
              "Moderate (10–25%)" if x < 25 else
              "High (25–50%)"    if x < 50 else "Critical (>50%)")

out = df[["company_name","industry","pd_pct","pd_class",
          "risk_rating","loan_status","loan_amount"]].sort_values("pd_pct", ascending=False)
out.to_csv("outputs/pd_model_output.csv", index=False)
print("✓ PD model output → outputs/pd_model_output.csv")
print(out.to_string(index=False))

# ── Chart ──────────────────────────────────────────────────
color_map = {
    "Low (<10%)": "#63B179", "Moderate (10–25%)": "#EF9F27",
    "High (25–50%)": "#E88040", "Critical (>50%)": "#E24B4A"
}
colors = out["pd_class"].map(color_map)
fig, ax = plt.subplots(figsize=(14, 7))
bars = ax.barh(out["company_name"], out["pd_pct"],
               color=colors, edgecolor="white", linewidth=0.4)
ax.axvline(x=25, color="#A32D2D", linestyle="--", linewidth=1.5,
           label="High risk threshold (25%)")
ax.axvline(x=10, color="#854F0B", linestyle="--", linewidth=1.5,
           label="Moderate risk threshold (10%)")
ax.set_xlabel("Probability of Default (%)", fontsize=11)
ax.set_title("Probability of Default (PD) Model — Portfolio\nLogistic Regression | FY 2024",
             fontsize=13, fontweight="bold", pad=15)
ax.set_facecolor("#F9F9F9")
fig.patch.set_facecolor("white")
handles = [mpatches.Patch(color=v, label=k) for k, v in color_map.items()]
ax.legend(handles=handles, loc="lower right", fontsize=9)
for bar, val in zip(bars, out["pd_pct"]):
    ax.text(val + 0.5, bar.get_y() + bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=8.5)
plt.tight_layout()
plt.savefig("outputs/chart_pd_model.png", dpi=150, bbox_inches="tight")
plt.show()
print("✓ Chart saved → outputs/chart_pd_model.png")