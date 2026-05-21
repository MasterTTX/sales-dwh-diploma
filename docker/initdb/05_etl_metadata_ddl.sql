CREATE TABLE IF NOT EXISTS etl.etl_runs (
    run_id UUID PRIMARY KEY,
    pipeline_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,
    error_message TEXT
);


CREATE TABLE IF NOT EXISTS etl.etl_run_steps (
    step_id BIGSERIAL PRIMARY KEY,
    run_id UUID REFERENCES etl.etl_runs(run_id),
    step_name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP,
    rows_processed INTEGER,
    error_message TEXT
);


CREATE TABLE IF NOT EXISTS etl.dq_rejected_records (
    rejected_id BIGSERIAL PRIMARY KEY,
    run_id UUID,
    layer_name TEXT NOT NULL,
    table_name TEXT NOT NULL,
    reason TEXT NOT NULL,
    record_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);