FROM apache/airflow:2.9.1

WORKDIR /opt/airflow/project

COPY requirements.txt .

USER airflow

RUN pip install --no-cache-dir -r requirements.txt