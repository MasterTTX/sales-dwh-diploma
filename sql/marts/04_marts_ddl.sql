CREATE OR REPLACE VIEW marts.v_sales_analytics AS
SELECT
    d.full_date AS sale_date,
    d.year,
    d.quarter,
    d.month,
    d.weekday_name,

    s.branch_code AS branch,
    s.city,

    p.product_line_name AS product_line,
    c.customer_segment_name AS customer_segment,
    pm.payment_method_name AS payment_method,

    COUNT(DISTINCT f.invoice_id) AS sales_count,

    SUM(f.quantity) AS total_quantity,
    SUM(f.total_amount) AS revenue,
    SUM(f.gross_income) AS gross_income,

    SUM(f.total_amount)
        / NULLIF(COUNT(DISTINCT f.invoice_id), 0)
        AS avg_check,

    AVG(f.rating) AS avg_rating

FROM dds.fct_sales f

JOIN dds.dim_date d
    ON f.date_key = d.date_key

JOIN dds.dim_store s
    ON f.store_key = s.store_key

JOIN dds.dim_product_line p
    ON f.product_line_key = p.product_line_key

JOIN dds.dim_customer_segment c
    ON f.customer_segment_key = c.customer_segment_key

JOIN dds.dim_payment_method pm
    ON f.payment_method_key = pm.payment_method_key

GROUP BY
    d.full_date,
    d.year,
    d.quarter,
    d.month,
    d.weekday_name,
    s.branch_code,
    s.city,
    p.product_line_name,
    c.customer_segment_name,
    pm.payment_method_name;