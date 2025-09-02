WITH base AS (
    SELECT
        DATE(service_date) as d,
        practice_id, 
        SUM(charge_amount) AS charges,
        SUM(paid_amount) AS paid,
        COUNT(*) AS claims,
        SUM(denial_flag) AS denied
    FROM claims
    GROUP BY 1, 2
),
joined AS (
    SELECT b.*, c.month, c.year, c.is_holiday, c.flu_season_flag
    FROM base b LEFT JOIN calendar c ON c.date = b.d
)
SELECT
    d,
    practice_id,
    charges,
    paid,
    claims,
    denied,
    (1.0 * denied) / NULLIF(claims, 0) AS denial_rate,
    month, 
    year, 
    is_holiday, 
    flu_season_flag
FROM joined
ORDER BY d, practice_id;