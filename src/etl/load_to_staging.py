import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from datetime import datetime, UTC

import pandas as pd
from sqlalchemy import text

from src.utils.db import get_engine
from src.utils.etl_logging import start_etl_run, finish_etl_run


def to_snake_case(column_name: str) -> str:
    return (
        column_name.strip()
        .lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("-", "_")
    )


def load_csv_to_staging(csv_path: str):
    run_id = start_etl_run("load_csv_to_staging")

    try:
        source_file = Path(csv_path)

        df = pd.read_csv(source_file)

        df.columns = [to_snake_case(col) for col in df.columns]

        df = df.rename(
            columns={
                "date": "sale_date",
                "time": "sale_time",
                "tax_5%": "tax_5"
            }
        )

        df["load_id"] = run_id
        df["loaded_at"] = datetime.now(UTC)
        df["source_file_name"] = source_file.name
        df["source_row_number"] = range(1, len(df) + 1)

        df["row_hash"] = pd.util.hash_pandas_object(
            df.astype(str),
            index=False
        ).astype(str)

        engine = get_engine()

        with engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE staging.sales_raw;"))

        df.to_sql(
            "sales_raw",
            engine,
            schema="staging",
            if_exists="append",
            index=False
        )

        finish_etl_run(run_id, "SUCCESS")

        print(f"Loaded {len(df)} rows to staging.sales_raw")

    except Exception as error:
        finish_etl_run(run_id, "FAILED", str(error))
        raise


if __name__ == "__main__":
    load_csv_to_staging("data/raw/supermarket_sales.csv")