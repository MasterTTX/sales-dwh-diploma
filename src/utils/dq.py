import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from sqlalchemy import text

from src.utils.db import get_engine
from src.utils.etl_logging import start_etl_run, finish_etl_run


def run_query_check(conn, check_name: str, query: str):
    result = conn.execute(text(query))
    failed_count = result.scalar()

    if failed_count and failed_count > 0:
        print(f"[FAILED] {check_name}: {failed_count}")
    else:
        print(f"[OK] {check_name}")

    return failed_count or 0


def run_staging_dq(conn):
    checks = {
        "staging_null_invoice_id": """
            SELECT COUNT(*) FROM staging.sales_raw
            WHERE invoice_id IS NULL
        """,
        "staging_duplicate_invoice_id": """
            SELECT COUNT(*) FROM (
                SELECT invoice_id
                FROM staging.sales_raw
                GROUP BY invoice_id
                HAVING COUNT(*) > 1
            ) t
        """,
        "staging_invalid_quantity": """
            SELECT COUNT(*) FROM staging.sales_raw
            WHERE quantity IS NULL OR quantity <= 0
        """,
        "staging_invalid_unit_price": """
            SELECT COUNT(*) FROM staging.sales_raw
            WHERE unit_price IS NULL OR unit_price < 0
        """,
        "staging_invalid_total": """
            SELECT COUNT(*) FROM staging.sales_raw
            WHERE total IS NULL OR total < 0
        """
    }

    for check_name, query in checks.items():
        run_query_check(conn, check_name, query)


def run_nds_dq(conn):
    checks = {
        "nds_sales_without_branch": """
            SELECT COUNT(*)
            FROM nds.sales s
            LEFT JOIN nds.branches b
                ON s.branch_id = b.branch_id
            WHERE b.branch_id IS NULL
        """,
        "nds_sales_without_product_line": """
            SELECT COUNT(*)
            FROM nds.sales s
            LEFT JOIN nds.product_lines p
                ON s.product_line_id = p.product_line_id
            WHERE p.product_line_id IS NULL
        """,
        "nds_sales_duplicate_invoice_id": """
            SELECT COUNT(*) FROM (
                SELECT invoice_id
                FROM nds.sales
                GROUP BY invoice_id
                HAVING COUNT(*) > 1
            ) t
        """
    }

    for check_name, query in checks.items():
        run_query_check(conn, check_name, query)


def run_dds_dq(conn):
    checks = {
        "dds_fact_without_date": """
            SELECT COUNT(*)
            FROM dds.fct_sales f
            LEFT JOIN dds.dim_date d
                ON f.date_key = d.date_key
            WHERE d.date_key IS NULL
        """,
        "dds_fact_without_store": """
            SELECT COUNT(*)
            FROM dds.fct_sales f
            LEFT JOIN dds.dim_store s
                ON f.store_key = s.store_key
            WHERE s.store_key IS NULL
        """,
        "dds_fact_duplicate_invoice_id": """
            SELECT COUNT(*) FROM (
                SELECT invoice_id
                FROM dds.fct_sales
                GROUP BY invoice_id
                HAVING COUNT(*) > 1
            ) t
        """
    }

    for check_name, query in checks.items():
        run_query_check(conn, check_name, query)


def main(layer: str):
    run_id = start_etl_run(f"dq_{layer}")

    engine = get_engine()

    try:
        with engine.begin() as conn:
            if layer == "staging":
                run_staging_dq(conn)
            elif layer == "nds":
                run_nds_dq(conn)
            elif layer == "dds":
                run_dds_dq(conn)
            else:
                raise ValueError("Layer must be one of: staging, nds, dds")

        finish_etl_run(run_id, "SUCCESS")

    except Exception as error:
        finish_etl_run(run_id, "FAILED", str(error))
        raise


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Usage: python src/utils/dq.py staging|nds|dds")

    main(sys.argv[1])