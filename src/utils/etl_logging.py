import uuid
from datetime import datetime

from sqlalchemy import text

from src.utils.db import get_engine


engine = get_engine()


def start_etl_run(pipeline_name: str) -> str:
    run_id = str(uuid.uuid4())

    query = text("""
        INSERT INTO etl.etl_runs (
            run_id,
            pipeline_name,
            status,
            started_at
        )
        VALUES (
            :run_id,
            :pipeline_name,
            'RUNNING',
            :started_at
        )
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "run_id": run_id,
                "pipeline_name": pipeline_name,
                "started_at": datetime.utcnow()
            }
        )

    return run_id


def finish_etl_run(run_id: str, status: str = "SUCCESS", error_message: str = None):

    query = text("""
        UPDATE etl.etl_runs
        SET
            status = :status,
            finished_at = :finished_at,
            error_message = :error_message
        WHERE run_id = :run_id
    """)

    with engine.begin() as conn:
        conn.execute(
            query,
            {
                "run_id": run_id,
                "status": status,
                "finished_at": datetime.utcnow(),
                "error_message": error_message
            }
        )