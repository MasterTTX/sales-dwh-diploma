import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from sqlalchemy import text

from src.utils.db import get_engine
from src.utils.etl_logging import start_etl_run, finish_etl_run


def validate_marts():
    run_id = start_etl_run("validate_marts")

    engine = get_engine()

    try:
        with engine.begin() as conn:

            result = conn.execute(text("""
                SELECT COUNT(*)
                FROM marts.v_sales_analytics
            """))

            row_count = result.scalar()

            print(f"marts.v_sales_analytics available. Rows: {row_count}")

        finish_etl_run(run_id, "SUCCESS")

    except Exception as error:
        finish_etl_run(run_id, "FAILED", str(error))
        raise


if __name__ == "__main__":
    validate_marts()