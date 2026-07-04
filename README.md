# Commercial Loan Underwriting & Credit Risk Decision Platform

> End-to-end commercial banking credit analysis platform simulating the full workflow 
> of a Credit Analyst at a US commercial bank — built with Excel, SQL, Python, and Power BI.

---

## Project Summary

This project evaluates a **$8,000,000 term loan request** from **Midwest Precision Parts LLC**, 
a mid-market auto parts manufacturer in Dayton, Ohio facing revenue headwinds from the 
EV industry transition. The analysis covers the complete underwriting lifecycle — from 
financial statement spreading to credit committee recommendation.

**Final Decision: Conditional Approval**  
**Risk Rating: 5/10 — Moderate Risk**  
**DSCR: 1.18x | Debt/EBITDA: 4.2x | Interest Coverage: 3.6x**  
**Expected Loss: $523,600 | PD: 18.7% | LGD: 35%**

---

## Key Risk Factors Identified

- DSCR of 1.18x sits 8 basis points above the 1.10x covenant floor — limited buffer
- Revenue declining 8% YoY due to EV transition reducing demand for ICE components
- Customer concentration risk — 64% of revenue from 2 customers
- Collateral coverage ratio of 0.95x — loan slightly undercollateralized
- Sensitivity analysis confirms covenant breach at -15% revenue decline (DSCR drops to 0.97x)

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| Microsoft Excel | Financial statement modeling, ratio analysis, sensitivity analysis, credit scorecard |
| SQLite (DB Browser) | Commercial loan portfolio database — 25 borrowers, 4 tables |
| Python | PD modeling (logistic regression), Expected Loss (Basel II), portfolio concentration (HHI) |
| Power BI | 5 interactive dashboards — overview, heatmap, borrower analysis, concentration, watchlist |

---

## Project Structure
commercial-loan-underwriting-platform/
│
├── excel/
│   └── Midwest_Precision_Parts_Credit_Analysis.xlsx
│       ├── Tab 1 — Financial Statements (IS, BS, CF — FY2022 to FY2024)
│       ├── Tab 2 — Ratio Analysis (DSCR, Debt/EBITDA, ICR, Current Ratio)
│       ├── Tab 3 — Credit Scorecard (8-factor weighted model → Rating 5/10)
│       ├── Tab 4 — Loan Structure ($8M, 7yr, 6.75% fixed, 3 covenants)
│       ├── Tab 5 — Collateral Analysis (LTV 105.3%, Coverage 0.95x)
│       ├── Tab 6 — Amortization Schedule (84 months, PMT formula)
│       ├── Tab 7 — Sensitivity Analysis (DSCR breach at -15% revenue)
│       └── Tab 8 — Credit Committee Summary (Decision memo)
│
├── sql/
│   ├── credit_risk_portfolio.db
│   └── analysis_queries.sql
│
├── python/
│   ├── script1_financial_ratio_engine.py
│   ├── script2_credit_risk_scoring_model.py
│   ├── script3_probability_of_default_model.py
│   ├── script4_portfolio_concentration_analysis.py
│   ├── script5_expected_loss_model.py
│   ├── data/
│   │   └── borrowers_data.csv
│   └── outputs/
│       ├── ratio_summary.csv
│       ├── risk_scores.csv
│       ├── pd_model_output.csv
│       ├── portfolio_concentration.csv
│       ├── expected_loss_output.csv
│       └── (5 chart PNG files)
│
├── powerbi/
│   └── Credit_Risk_Dashboards.pbix
│
└── screenshots/
└── (20 screenshots — Python charts, SQL queries, Power BI dashboards)

---

## Excel Model — 8 Tabs

**Tab 1 — Financial Statements**  
Three years of Income Statement, Balance Sheet, and Cash Flow for Midwest Precision Parts LLC. Revenue declining from $32.5M (FY2022) to $27.5M (FY2024) — an 8% YoY decline driven by EV transition headwinds in the auto parts sector.

**Tab 2 — Ratio Analysis**  
Eight credit ratios calculated with cross-sheet formulas, 3-year trend analysis, industry benchmarks, and conditional formatting (green/amber/red). DSCR trends from 1.18x to declining — flagged as Watch.

**Tab 3 — Credit Scorecard**  
Weighted scoring across 8 risk factors including financial strength, industry risk, customer concentration, collateral quality, and management. Output: Risk Rating 5/10 → Moderate Risk → Conditional Approval.

**Tab 5 — Collateral Analysis**  
Asset-specific haircuts applied: Equipment 40%, Real Estate 20%, Inventory 50%. Total collateral value $7.6M against $8.0M loan — LTV 105.3%, Coverage 0.95x. Covenants required.

**Tab 7 — Sensitivity Analysis**  
Two-way table: revenue decline (0% to -25%) vs EBITDA margin (10% to 18%). At -15% revenue decline, DSCR drops to 0.97x — below the 1.10x covenant floor, triggering default review.

---

## SQL Database

**4 Tables | 25 Borrowers | $250.7M Portfolio**

```sql
-- Borrowers: 25 companies across 6 industries
-- Loans: Active, Watchlist, Defaulted status
-- Risk Ratings: 1-10 scale with analyst notes  
-- Financial Metrics: 3-year DSCR trend for watchlist borrowers
```

**Query Highlights:**
- Watchlist query — identifies borrowers with DSCR below 1.20x
- Concentration query — Manufacturing at 32.5% of portfolio (HHI: 2,126)
- DSCR trend query — 4 borrowers with deteriorating coverage 2022→2024
- Expected Loss query — 9 high-risk borrowers flagged (rating ≥ 6)

---

## Python Models

**Script 1 — Financial Ratio Engine**  
Recalculates DSCR, Debt/EBITDA, ICR, and Current Ratio from raw financials. Flags each borrower as BREACH / WATCH / PASS against covenant thresholds.

**Script 2 — Credit Risk Scoring Model**  
Weighted scorecard across 7 factors — mirrors the Excel Tab 3 logic but automated across all 25 borrowers simultaneously.

**Script 3 — Probability of Default Model**  
Logistic regression using DSCR, Debt/EBITDA, Interest Coverage, and Current Ratio as features. MPP PD: 18.7%. Classifies borrowers into Low / Moderate / High / Critical risk tiers.

**Script 4 — Portfolio Concentration Analysis**  
HHI score: 2,126 — Moderately Concentrated. Manufacturing flagged as overweight at 32.5% of total exposure.

**Script 5 — Expected Loss Model (Basel II)**
EL = PD × LGD × EAD
MPP: 18.7% × 35% × $8,000,000 = $523,600
Portfolio Total EL: $14.3M (5.71% of $250.7M exposure)

---

## Power BI Dashboards

**Dashboard 1 — Commercial Banking Overview**  
Portfolio KPIs: $250.7M total exposure, 25 borrowers, $20.5M defaulted, avg risk rating 4.96. Bar chart by industry, donut by loan status.

**Dashboard 2 — Credit Risk Heatmap**  
Scatter plot: DSCR vs Debt/EBITDA with reference lines at covenant floor (1.10x) and leverage ceiling (5.0x). Table with conditional formatting on DSCR column.

**Dashboard 3 — Borrower Portfolio Dashboard**  
Interactive slicer — select any borrower to filter all visuals. Shows DSCR, risk rating, loan amount, watchlist status, and decision label per borrower.

**Dashboard 4 — Industry Concentration Analysis**  
Treemap + bar chart showing exposure by industry. HHI score card: 2,126 (Moderately Concentrated). Full HHI breakdown table with component scores.

**Dashboard 5 — Watchlist & Early Warning**  
9 borrowers on watchlist, 6 covenant breaches, avg PD 51.29%, $53.2M watchlist exposure. Filtered bar chart and table showing only High Risk and Watchlist borrowers.

---

## How to Run the Python Scripts

```bash
# Install dependencies
pip install pandas numpy matplotlib scikit-learn openpyxl

# Run in order
python script1_financial_ratio_engine.py
python script2_credit_risk_scoring_model.py
python script3_probability_of_default_model.py
python script4_portfolio_concentration_analysis.py
python script5_expected_loss_model.py
```

All outputs saved to `/outputs/` folder automatically.

---

## Credit Decision Summary

| Metric | Value | Benchmark | Status |
|--------|-------|-----------|--------|
| DSCR | 1.18x | > 1.25x | ⚠ Watch |
| Debt / EBITDA | 4.2x | < 4.0x | ⚠ Elevated |
| Interest Coverage | 3.6x | > 3.0x | ✓ Adequate |
| Current Ratio | 1.4x | > 1.5x | ⚠ Tight |
| Collateral Coverage | 0.95x | > 1.0x | ⚠ Deficient |
| Probability of Default | 18.7% | < 10% | ⚠ Moderate |
| Expected Loss | $523,600 | < $500K | ⚠ Moderate |

**Covenants Required:**
1. DSCR ≥ 1.10x — tested quarterly
2. Debt/EBITDA ≤ 5.0x — tested annually  
3. No single customer > 40% of revenue — annual certification

---

## Skills Demonstrated

`Credit Analysis` `DSCR` `Debt/EBITDA` `Interest Coverage` `Covenant Testing`  
`Collateral Analysis` `LTV` `Sensitivity Analysis` `Probability of Default`  
`Loss Given Default` `Expected Loss` `Basel II` `Logistic Regression`  
`HHI Concentration Analysis` `SQL JOINs` `Power BI DAX` `Financial Modeling`

---

*Built as a flagship MBA portfolio project targeting Credit Risk Analyst, 
Commercial Banking Analyst, and Underwriting internship roles at US banks.*
