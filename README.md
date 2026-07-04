# Commercial Loan Underwriting & Credit Risk Decision Platform

> End-to-end commercial banking credit analysis platform simulating the full workflow of a Credit Analyst at a US commercial bank — built with Excel, SQL, Python, and Power BI.

---

## Project Summary

This project evaluates a **$8,000,000 term loan request** from **Midwest Precision Parts LLC**, a mid-market auto parts manufacturer in Dayton, Ohio. The company is facing accelerating revenue pressure from the EV industry transition, which is reducing demand for its internal combustion engine components. The analysis covers the complete underwriting lifecycle — from financial statement spreading and ratio analysis through collateral assessment, covenant structuring, and final credit committee recommendation.

**Final Decision: Conditional Approval**
**Risk Rating: 5/10 — Moderate Risk**
**DSCR: 1.18x | Debt/EBITDA: 4.2x | Interest Coverage: 3.6x**
**Expected Loss: $523,600 | PD: 18.7% | LGD: 35% | EAD: $8,000,000**

---

## Key Risk Factors

- DSCR of 1.18x provides only an 8 basis point buffer above the 1.10x covenant floor
- Revenue has declined 8% YoY for two consecutive years driven by EV transition headwinds
- Two customers account for 64% of total revenue — significant concentration risk
- Collateral coverage ratio of 0.95x means the loan is slightly undercollateralized
- Sensitivity analysis shows covenant breach at a 15% revenue decline (DSCR falls to 0.97x)
- Deferred tax assets growing as EV transition losses create increasing timing differences

---

## Tools Used

| Tool | Purpose |
|------|---------|
| Microsoft Excel | Financial statement modeling, ratio analysis, credit scorecard, sensitivity analysis |
| SQLite | Commercial loan portfolio database — 25 borrowers across 6 industries |
| Python | Logistic regression PD model, Expected Loss (Basel II), HHI concentration analysis |
| Power BI | 5 interactive dashboards — portfolio overview, risk heatmap, borrower drill-down, concentration, watchlist |

---

## Project Structure

```
commercial-loan-underwriting-platform/
│
├── excel/
│   └── Midwest_Precision_Parts_Credit_Analysis.xlsx
│       ├── Tab 1 — Financial Statements (IS, BS, CF — FY2022 to FY2024)
│       ├── Tab 2 — Ratio Analysis (DSCR, Debt/EBITDA, ICR, Current Ratio)
│       ├── Tab 3 — Credit Scorecard (8-factor weighted model — Rating 5/10)
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
│       ├── chart_dscr_portfolio.png
│       ├── chart_risk_scores.png
│       ├── chart_pd_model.png
│       ├── chart_concentration.png
│       └── chart_expected_loss.png
│
├── powerbi/
│   └── Credit_Risk_Dashboards.pbix
│
└── screenshots/
    └── (20 screenshots — Python charts, SQL tables, SQL queries, Power BI dashboards)
```

---

## Excel Workbook — 8 Tabs

**Tab 1 — Financial Statements**
Three years of Income Statement, Balance Sheet, and Cash Flow Statement for Midwest Precision Parts LLC (FY2022–FY2024). Revenue declined from $32.5M to $27.5M — an 8% YoY drop reflecting reduced demand for ICE auto components. Balance sheet includes growing deferred tax assets reflecting EV transition timing differences. All formulas are cross-linked across statements.

**Tab 2 — Ratio Analysis**
Eight credit ratios calculated using cross-sheet formulas, with a 3-year trend column, industry benchmark comparisons, and conditional formatting (green/amber/red thresholds). DSCR flagged as Watch at 1.18x. Debt/EBITDA elevated at 4.2x against a 4.0x benchmark.

**Tab 3 — Credit Scorecard**
Weighted scoring model across 8 risk factors: financial strength, industry risk, management quality, customer concentration, collateral quality, cash flow consistency, leverage structure, and loan status. Final output: Risk Rating 5/10 — Moderate Risk — Conditional Approval.

**Tab 4 — Loan Structure**
Full loan terms including PMT formula for monthly payment calculation, origination and maturity dates, prepayment penalty schedule, and collateral description. Three financial covenants defined with testing frequency and breach consequences.

**Tab 5 — Collateral Analysis**
Asset-specific haircuts applied to each collateral category: Equipment 40%, Real Estate 20%, Inventory 50%. Total collateral value $7.6M against $8.0M loan exposure. LTV: 105.3%. Collateral Coverage Ratio: 0.95x. Conclusion: covenants required to compensate for thin collateral support.

**Tab 6 — Amortization Schedule**
Full 84-month amortization table built with PMT, EDATE, and cross-referenced input cells. Shows beginning balance, monthly payment, principal allocation, interest allocation, and ending balance for each of the 84 months. Totals row confirms full loan repayment.

**Tab 7 — Sensitivity Analysis**
Two-way sensitivity table: revenue decline (0% to -25%) against EBITDA margin (10% to 18%). Conditional formatting identifies cells where DSCR breaches the 1.10x covenant floor. At -15% revenue decline, DSCR drops to 0.97x — triggering covenant breach and loan default review.

**Tab 8 — Credit Committee Summary**
One-page executive memo formatted as a real bank credit committee document. Pulls live data from all other tabs via cross-sheet references. Includes borrower background, key financial metrics vs benchmarks, credit decision matrix, covenant terms, and final analyst recommendation with supporting rationale.

---

## SQL Database

**4 Tables | 25 Borrowers | $250.7M Total Portfolio**

```sql
-- Table 1: borrowers     — 25 companies across 6 industries, 8 states
-- Table 2: loans         — loan amount, rate, tenor, status, collateral type
-- Table 3: risk_ratings  — rating 1-10, risk level, analyst notes
-- Table 4: financial_metrics — 3-year DSCR trend for watchlist borrowers
```

**4 Analysis Queries:**

**Query 1 — Watchlist Identification**
Returns all borrowers with DSCR below 1.20x in FY2024, joined across borrowers, financial metrics, risk ratings, and loans. Returns 4 borrowers including Midwest Precision Parts at 1.05x.

**Query 2 — Portfolio Concentration**
Calculates total loan exposure and percentage share by industry using aggregation and a subquery for portfolio total. Manufacturing flags at 32.51% — the largest sector.

**Query 3 — Deteriorating DSCR Trend**
Pivot query using conditional aggregation to show DSCR across 2022, 2023, and 2024 side by side. HAVING clause filters to borrowers where FY2024 DSCR is below FY2022 DSCR. Returns 4 borrowers all showing consistent decline.

**Query 4 — Expected Loss Flag**
Calculates estimated expected loss (loan amount × 0.143 × 0.35) for all borrowers with risk rating of 6 or above. Returns 9 high-risk borrowers sorted by estimated loss descending.

---

## Python Scripts

**Script 1 — Financial Ratio Engine**
Reads `borrowers_data.csv` and recalculates DSCR, Debt/EBITDA, ICR, Current Ratio, Gross Margin, and Net Margin from raw financial inputs. Flags each borrower as BREACH, WATCH, or PASS against defined thresholds. Outputs `ratio_summary.csv` and a color-coded horizontal bar chart.

**Script 2 — Credit Risk Scoring Model**
Applies a 7-factor weighted scorecard (DSCR, leverage, interest coverage, current ratio, industry risk, loan status, net margin) across all 25 borrowers. Assigns a model risk rating and decision label (Approve / Conditional Approval / Escalate / Decline). Outputs `risk_scores.csv` and a color-coded bar chart.

**Script 3 — Probability of Default Model**
Builds a logistic regression model using DSCR, Debt/EBITDA, Interest Coverage, and Current Ratio as features. Binary default label assigned based on risk rating threshold. Predicts PD percentage for each borrower. MPP PD: 18.7%. Outputs `pd_model_output.csv` and a bar chart with threshold lines.

**Script 4 — Portfolio Concentration Analysis**
Calculates industry-level loan exposure and portfolio percentage share. Computes Herfindahl-Hirschman Index (HHI) to quantify concentration risk. HHI: 2,126 — Moderately Concentrated. Manufacturing flagged as overweight at 32.5%. Outputs `portfolio_concentration.csv` and a dual chart (donut + bar).

**Script 5 — Expected Loss Model (Basel II)**

```
EL = PD × LGD × EAD

Midwest Precision Parts LLC:
PD  = 18.7%
LGD = 35% (Moderate risk, active loan)
EAD = $8,000,000
EL  = $523,600

Portfolio Total EL  = $14,314,140
Portfolio EL %      = 5.71% of $250.7M exposure
```

Merges PD model output with borrower data. Applies tiered LGD based on loan status and risk rating. Classifies borrowers by EL tier. Outputs `expected_loss_output.csv` and dual charts showing EL by borrower and by industry.

---

## Power BI Dashboards

**Dashboard 1 — Commercial Banking Overview**
Four KPI cards: $250.7M total portfolio exposure, 25 borrowers, $20.5M defaulted exposure, average risk rating 4.96. Bar chart of loan exposure by industry and donut chart showing portfolio split by loan status (Active 82.97%, Watchlist 8.86%, Defaulted 8.18%).

**Dashboard 2 — Credit Risk Heatmap**
Scatter plot of DSCR vs Debt/EBITDA with bubble size representing loan amount and color representing industry. Three reference lines: covenant floor at 1.10x DSCR (red), benchmark at 1.25x DSCR (amber), leverage ceiling at 5.0x Debt/EBITDA (red). Table with conditional background color on DSCR column — red for breach, yellow for watch, green for pass.

**Dashboard 3 — Borrower Portfolio Dashboard**
Dropdown slicer allows selection of any individual borrower — all visuals filter dynamically. Table shows industry, company, loan amount, DSCR, leverage, risk rating, loan status, watchlist status, and decision label for all 25 borrowers. Bar chart shows DSCR by borrower sorted ascending.

**Dashboard 4 — Industry Concentration Analysis**
Treemap showing portfolio share by industry. Bar chart showing total loan exposure by industry in dollars. HHI score card: 2,126 — Moderately Concentrated. Full HHI breakdown table showing borrowers, exposure, portfolio percentage, and HHI component score per industry. Manufacturing HHI component: 1,056 — highest in portfolio.

**Dashboard 5 — Watchlist & Early Warning**
Four alert KPIs: 9 borrowers on watchlist, 6 covenant breaches (DSCR below 1.10x), average PD of 51.29% across watchlist borrowers, $53.2M total watchlist exposure. Bar chart filtered to High Risk and Watchlist borrowers only. Detail table showing DSCR, risk rating, loan amount, loan status, watchlist status, and decision label for each flagged borrower.

---

## How to Run

```bash
# Step 1 — Install dependencies
pip install pandas numpy matplotlib scikit-learn openpyxl

# Step 2 — Run scripts in order (Script 5 depends on Script 3 output)
python script1_financial_ratio_engine.py
python script2_credit_risk_scoring_model.py
python script3_probability_of_default_model.py
python script4_portfolio_concentration_analysis.py
python script5_expected_loss_model.py
```

All CSV outputs and chart images are saved automatically to the `/outputs/` folder.

---

## Credit Decision Summary

| Metric | FY2024 Value | Benchmark | Assessment |
|--------|-------------|-----------|------------|
| DSCR | 1.18x | > 1.25x | ⚠ Watch — limited covenant buffer |
| Debt / EBITDA | 4.2x | < 4.0x | ⚠ Elevated |
| Interest Coverage | 3.6x | > 3.0x | ✓ Adequate |
| Current Ratio | 1.4x | > 1.5x | ⚠ Tight |
| Collateral Coverage | 0.95x | > 1.0x | ⚠ Deficient — covenants required |
| Probability of Default | 18.7% | < 10% | ⚠ Moderate |
| Expected Loss | $523,600 | < $500K | ⚠ Moderate |

**Three covenants required as conditions of approval:**

1. DSCR must remain at or above 1.10x — tested quarterly; breach triggers loan review and potential acceleration
2. Debt/EBITDA must not exceed 5.0x — tested annually at fiscal year-end
3. No single customer may exceed 40% of total revenue — annual borrower certification required

**Rationale:** The borrower presents a viable credit with positive cash flow and an experienced management team pursuing a defensible retooling strategy for EV battery components. However, the thin DSCR buffer, customer concentration, and slightly deficient collateral position justify conditional approval with active covenant monitoring rather than a clean approval.

---

## Skills Demonstrated

`Credit Analysis` `DSCR` `Debt/EBITDA` `Interest Coverage Ratio` `Covenant Testing`
`Collateral Analysis` `Loan-to-Value` `Sensitivity Analysis` `Amortization Modeling`
`Probability of Default` `Loss Given Default` `Expected Loss` `Basel II Framework`
`Logistic Regression` `HHI Concentration Analysis` `Portfolio Risk Monitoring`
`SQL JOINs` `Conditional Aggregation` `Power BI DAX` `Financial Statement Spreading`

---

*Built as a flagship MBA portfolio project targeting Credit Risk Analyst, Commercial Banking Analyst, and Underwriting internship and full-time roles at US commercial banks and financial institutions.*
