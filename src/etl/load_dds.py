import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from sqlalchemy import text

from src.utils.db import get_engine
from src.utils.etl_logging import start_etl_run, finish_etl_run


def load_dds():
    run_id = start_etl_run("load_dds")
    engine = get_engine()

    try:
        with engine.begin() as conn:

            conn.execute(text("""
                INSERT INTO dds.dim_date (
                    date_key,
                    full_date,
                    year,
                    quarter,
                    month,
                    day,
                    weekday_name
                )
                SELECT DISTINCT
                    TO_CHAR(sale_date, 'YYYYMMDD')::INTEGER AS date_key,
                    sale_date AS full_date,
                    EXTRACT(YEAR FROM sale_date)::INTEGER AS year,
                    EXTRACT(QUARTER FROM sale_date)::INTEGER AS quarter,
                    EXTRACT(MONTH FROM sale_date)::INTEGER AS month,
                    EXTRACT(DAY FROM sale_date)::INTEGER AS day,
                    TO_CHAR(sale_date, 'Day') AS weekday_name
                FROM nds.sales
                ON CONFLICT (date_key) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO dds.dim_time (
                    time_key,
                    full_time,
                    hour,
                    minute,
                    second
                )
                SELECT DISTINCT
                    TO_CHAR(sale_time, 'HH24MISS')::INTEGER AS time_key,
                    sale_time AS full_time,
                    EXTRACT(HOUR FROM sale_time)::INTEGER AS hour,
                    EXTRACT(MINUTE FROM sale_time)::INTEGER AS minute,
                    EXTRACT(SECOND FROM sale_time)::INTEGER AS second
                FROM nds.sales
                ON CONFLICT (time_key) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO dds.dim_store (
                    branch_code,
                    city
                )
                SELECT DISTINCT
                    branch_code,
                    city
                FROM nds.branches
                ON CONFLICT (branch_code, city) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO dds.dim_product_line (product_line_name)
                SELECT DISTINCT product_line_name
                FROM nds.product_lines
                ON CONFLICT (product_line_name) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO dds.dim_customer_segment (customer_segment_name)
                SELECT DISTINCT customer_segment_name
                FROM nds.customer_segments
                ON CONFLICT (customer_segment_name) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO dds.dim_payment_method (payment_method_name)
                SELECT DISTINCT payment_method_name
                FROM nds.payment_methods
                ON CONFLICT (payment_method_name) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO dds.fct_sales (
                    invoice_id,
                    date_key,
                    time_key,
                    store_key,
                    product_line_key,
                    customer_segment_key,
                    payment_method_key,
                    quantity,
                    unit_price,
                    tax_amount,
                    total_amount,
                    cogs,
                    gross_income,
                    rating
                )
                SELECT
                    s.invoice_id,
                    TO_CHAR(s.sale_date, 'YYYYMMDD')::INTEGER AS date_key,
                    TO_CHAR(s.sale_time, 'HH24MISS')::INTEGER AS time_key,
                    ds.store_key,
                    dpl.product_line_key,
                    dcs.customer_segment_key,
                    dpm.payment_method_key,
                    s.quantity,
                    s.unit_price,
                    s.tax_amount,
                    s.total_amount,
                    s.cogs,
                    s.gross_income,
                    s.rating
                FROM nds.sales s
                JOIN nds.branches b
                    ON s.branch_id = b.branch_id
                JOIN nds.product_lines pl
                    ON s.product_line_id = pl.product_line_id
                JOIN nds.customer_segments cs
                    ON s.customer_segment_id = cs.customer_segment_id
                JOIN nds.payment_methods pm
                    ON s.payment_method_id = pm.payment_method_id
                JOIN dds.dim_store ds
                    ON b.branch_code = ds.branch_code
                   AND b.city = ds.city
                JOIN dds.dim_product_line dpl
                    ON pl.product_line_name = dpl.product_line_name
                JOIN dds.dim_customer_segment dcs
                    ON cs.customer_segment_name = dcs.customer_segment_name
                JOIN dds.dim_payment_method dpm
                    ON pm.payment_method_name = dpm.payment_method_name
                ON CONFLICT (invoice_id) DO NOTHING;
            """))

        finish_etl_run(run_id, "SUCCESS")
        print("DDS loaded successfully")

    except Exception as error:
        finish_etl_run(run_id, "FAILED", str(error))
        raise


if __name__ == "__main__":
    load_dds()