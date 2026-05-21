import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from sqlalchemy import text

from src.utils.db import get_engine
from src.utils.etl_logging import start_etl_run, finish_etl_run


def load_nds():
    run_id = start_etl_run("load_nds")

    engine = get_engine()

    try:
        with engine.begin() as conn:

            conn.execute(text("""
                INSERT INTO nds.branches (branch_code, city)
                SELECT DISTINCT
                    branch,
                    city
                FROM staging.sales_raw
                WHERE branch IS NOT NULL
                  AND city IS NOT NULL
                ON CONFLICT (branch_code) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO nds.product_lines (product_line_name)
                SELECT DISTINCT product_line
                FROM staging.sales_raw
                WHERE product_line IS NOT NULL
                ON CONFLICT (product_line_name) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO nds.customer_segments (customer_segment_name)
                SELECT DISTINCT customer_type
                FROM staging.sales_raw
                WHERE customer_type IS NOT NULL
                ON CONFLICT (customer_segment_name) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO nds.payment_methods (payment_method_name)
                SELECT DISTINCT payment
                FROM staging.sales_raw
                WHERE payment IS NOT NULL
                ON CONFLICT (payment_method_name) DO NOTHING;
            """))

            conn.execute(text("""
                INSERT INTO nds.sales (
                    invoice_id,
                    branch_id,
                    product_line_id,
                    customer_segment_id,
                    payment_method_id,
                    quantity,
                    unit_price,
                    tax_amount,
                    total_amount,
                    cogs,
                    gross_income,
                    rating,
                    sale_date,
                    sale_time
                )
                SELECT
                    sr.invoice_id,
                    b.branch_id,
                    pl.product_line_id,
                    cs.customer_segment_id,
                    pm.payment_method_id,
                    sr.quantity,
                    sr.unit_price,
                    sr.tax_5,
                    sr.total,
                    sr.cogs,
                    sr.gross_income,
                    sr.rating,
                    sr.sale_date,
                    sr.sale_time
                FROM staging.sales_raw sr
                JOIN nds.branches b
                    ON sr.branch = b.branch_code
                JOIN nds.product_lines pl
                    ON sr.product_line = pl.product_line_name
                JOIN nds.customer_segments cs
                    ON sr.customer_type = cs.customer_segment_name
                JOIN nds.payment_methods pm
                    ON sr.payment = pm.payment_method_name
                ON CONFLICT (invoice_id) DO NOTHING;
            """))

        finish_etl_run(run_id, "SUCCESS")
        print("NDS loaded successfully")

    except Exception as error:
        finish_etl_run(run_id, "FAILED", str(error))
        raise


if __name__ == "__main__":
    load_nds()