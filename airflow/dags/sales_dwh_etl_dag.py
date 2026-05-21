from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator


PROJECT_DIR = "/opt/airflow/project"


default_args = {
    "owner": "data_engineer",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=3),
}


with DAG(
    dag_id="sales_dwh_etl_dag",
    default_args=default_args,
    description="ETL pipeline for sales DWH diploma project",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["dwh", "etl", "diploma"],
) as dag:

    load_to_staging = BashOperator(
        task_id="load_to_staging",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"PYTHONPATH={PROJECT_DIR} "
            f"python src/etl/load_to_staging.py"
        ),
    )

    run_staging_dq = BashOperator(
        task_id="run_staging_dq",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"PYTHONPATH={PROJECT_DIR} "
            f"python src/utils/dq.py staging"
        ),
    )

    load_nds = BashOperator(
        task_id="load_nds",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"PYTHONPATH={PROJECT_DIR} "
            f"python src/etl/load_nds.py"
        ),
    )

    run_nds_dq = BashOperator(
        task_id="run_nds_dq",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"PYTHONPATH={PROJECT_DIR} "
            f"python src/utils/dq.py nds"
        ),
    )

    load_dds = BashOperator(
        task_id="load_dds",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"PYTHONPATH={PROJECT_DIR} "
            f"python src/etl/load_dds.py"
        ),
    )

    run_dds_dq = BashOperator(
        task_id="run_dds_dq",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"PYTHONPATH={PROJECT_DIR} "
            f"python src/utils/dq.py dds"
        ),
    )

    load_marts = BashOperator(
        task_id="load_marts",
        bash_command=(
            f"cd {PROJECT_DIR} && "
            f"PYTHONPATH={PROJECT_DIR} "
            f"python src/etl/load_marts.py"
        ),
    )

    (
        load_to_staging
        >> run_staging_dq
        >> load_nds
        >> run_nds_dq
        >> load_dds
        >> run_dds_dq
        >> load_marts
    )