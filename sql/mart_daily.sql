-- Daily paid/volume/denials by practice with calendar features
WITH daily AS (
    SELECT 
        DATE(service_date) AS d,
        practice_id,
        SUM(paid_amount) AS paid,
        COUNT(*) AS claims,
        AVG(denial_flag * 1.0) AS denial_rate
    FROM claims
    GROUP BY 1, 2
)
SELECT
    d,
    practice_id,
    paid,
    claims,
    denial_rate,
    c.month,
    c.year,
    c.is_weekend,
    c.is_holiday,
    c.flu_season_flag,
    c.end_of_month_flag
FROM daily
JOIN calendar c ON c.date = d
ORDER BY d, practice_id;