SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) FILTER (WHERE status = 'completed') AS completed_orders,
    SUM(total_amount) FILTER (WHERE status = 'completed') AS total_revenue,
    ROUND(
        AVG(total_amount) FILTER (WHERE status = 'completed'), 2
    ) AS avg_order_value,
    ROUND(
        COUNT(*) FILTER (WHERE status = 'completed') * 100.0 / COUNT(*), 2
    ) AS completion_rate_pct
FROM orders
GROUP BY DATE_TRUNC('month', created_at)
ORDER BY month;


SELECT
    DATE_TRUNC('month', o.created_at) AS month,
    c.name AS category,
    SUM(oi.quantity * oi.unit_price) AS category_revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
JOIN products p ON p.id = oi.product_id
JOIN categories c ON c.id = p.category_id
WHERE o.status = 'completed'
GROUP BY DATE_TRUNC('month', o.created_at), c.name
ORDER BY month, category_revenue DESC;


SELECT
    source,
    COUNT(*) AS total_sessions,
    COUNT(*) FILTER (WHERE converted = TRUE) AS conversions,
    ROUND(
        COUNT(*) FILTER (WHERE converted = TRUE) * 100.0 / COUNT(*), 2
    ) AS conversion_rate_pct
FROM sessions
GROUP BY source
ORDER BY conversion_rate_pct DESC;
