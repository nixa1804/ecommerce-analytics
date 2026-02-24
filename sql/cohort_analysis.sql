WITH cohorts AS (
    SELECT
        u.id AS user_id,
        DATE_TRUNC('month', u.created_at) AS cohort_month
    FROM users u
),
user_orders AS (
    SELECT
        o.user_id,
        DATE_TRUNC('month', o.created_at) AS order_month
    FROM orders o
    WHERE o.status = 'completed'
),
cohort_data AS (
    SELECT
        c.cohort_month,
        EXTRACT(EPOCH FROM (uo.order_month - c.cohort_month)) / 2592000 AS period_number,
        COUNT(DISTINCT c.user_id) AS users
    FROM cohorts c
    JOIN user_orders uo ON uo.user_id = c.user_id
    GROUP BY c.cohort_month, period_number
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(user_id) AS cohort_size
    FROM cohorts
    GROUP BY cohort_month
)
SELECT
    cd.cohort_month,
    cs.cohort_size,
    cd.period_number::INT AS months_since_signup,
    cd.users AS active_users,
    ROUND(cd.users * 100.0 / cs.cohort_size, 2) AS retention_rate_pct
FROM cohort_data cd
JOIN cohort_sizes cs ON cs.cohort_month = cd.cohort_month
WHERE cd.period_number >= 0
ORDER BY cd.cohort_month, cd.period_number;


WITH first_orders AS (
    SELECT
        user_id,
        MIN(created_at) AS first_order_date
    FROM orders
    WHERE status = 'completed'
    GROUP BY user_id
),
repeat_buyers AS (
    SELECT
        fo.user_id,
        COUNT(o.id) AS total_orders
    FROM first_orders fo
    JOIN orders o ON o.user_id = fo.user_id AND o.status = 'completed'
    GROUP BY fo.user_id
)
SELECT
    DATE_TRUNC('month', fo.first_order_date) AS cohort_month,
    COUNT(rb.user_id) AS total_buyers,
    COUNT(rb.user_id) FILTER (WHERE rb.total_orders > 1) AS repeat_buyers,
    ROUND(
        COUNT(rb.user_id) FILTER (WHERE rb.total_orders > 1) * 100.0 / COUNT(rb.user_id), 2
    ) AS repeat_purchase_rate_pct
FROM first_orders fo
JOIN repeat_buyers rb ON rb.user_id = fo.user_id
GROUP BY DATE_TRUNC('month', fo.first_order_date)
ORDER BY cohort_month;
