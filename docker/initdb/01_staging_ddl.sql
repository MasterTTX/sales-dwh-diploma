CREATE TABLE IF NOT EXISTS staging.sales_raw (
    raw_id BIGSERIAL PRIMARY KEY,

    invoice_id TEXT,
    branch TEXT,
    city TEXT,
    customer_type TEXT,
    gender TEXT,
    product_line TEXT,
    unit_price NUMERIC(12, 2),
    quantity INTEGER,
    tax_5 NUMERIC(12, 4),
    total NUMERIC(12, 4),
    sale_date DATE,
    sale_time TIME,
    payment TEXT,
    cogs NUMERIC(12, 4),
    gross_margin_percentage NUMERIC(12, 6),
    gross_income NUMERIC(12, 4),
    rating NUMERIC(4, 2),

    load_id UUID,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source_file_name TEXT,
    source_row_number INTEGER,
    row_hash TEXT
);