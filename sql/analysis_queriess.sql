-- Query 1: All watchlist borrowers (DSCR below 1.20x)
SELECT 
    b.company_name,
    b.industry,
    fm.fiscal_year,
    fm.dscr,
    fm.debt_to_ebitda,
    rr.risk_rating,
    rr.risk_level,
    l.loan_status
FROM borrowers b
JOIN financial_metrics fm ON b.borrower_id = fm.borrower_id
JOIN risk_ratings rr ON b.borrower_id = rr.borrower_id
JOIN loans l ON b.borrower_id = l.borrower_id
WHERE fm.dscr < 1.20 AND fm.fiscal_year = 2024
ORDER BY fm.dscr ASC;

-- Query 2: Portfolio concentration by industry
SELECT 
    b.industry,
    COUNT(b.borrower_id) AS num_borrowers,
    SUM(l.loan_amount) AS total_exposure,
    ROUND(SUM(l.loan_amount) * 100.0 / (SELECT SUM(loan_amount) FROM loans), 2) AS pct_of_portfolio
FROM borrowers b
JOIN loans l ON b.borrower_id = l.borrower_id
GROUP BY b.industry
ORDER BY total_exposure DESC;

-- Query 3: Borrowers with deteriorating DSCR (2022 to 2024)
SELECT 
    b.company_name,
    MAX(CASE WHEN fm.fiscal_year = 2022 THEN fm.dscr END) AS dscr_2022,
    MAX(CASE WHEN fm.fiscal_year = 2023 THEN fm.dscr END) AS dscr_2023,
    MAX(CASE WHEN fm.fiscal_year = 2024 THEN fm.dscr END) AS dscr_2024,
    rr.risk_rating
FROM borrowers b
JOIN financial_metrics fm ON b.borrower_id = fm.borrower_id
JOIN risk_ratings rr ON b.borrower_id = rr.borrower_id
GROUP BY b.company_name, rr.risk_rating
HAVING dscr_2024 < dscr_2022
ORDER BY dscr_2024 ASC;

-- Query 4: Expected Loss flag — high-risk borrowers
SELECT 
    b.company_name,
    b.industry,
    l.loan_amount AS ead,
    rr.risk_rating,
    l.loan_status,
    ROUND(l.loan_amount * 0.143 * 0.35, 0) AS estimated_expected_loss
FROM borrowers b
JOIN loans l ON b.borrower_id = l.borrower_id
JOIN risk_ratings rr ON b.borrower_id = rr.borrower_id
WHERE rr.risk_rating >= 6
ORDER BY estimated_expected_loss DESC;