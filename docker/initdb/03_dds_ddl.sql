CREATE TABLE IF NOT EXISTS dds.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    day INTEGER,
    weekday_name TEXT
);


CREATE TABLE IF NOT EXISTS dds.dim_time (
    time_key INTEGER PRIMARY KEY,
    full_time TIME NOT NULL UNIQUE,
    hour INTEGER,
    minute INTEGER,
    second INTEGER
);


CREATE TABLE IF NOT EXISTS dds.dim_store (
    store_key BIGSERIAL PRIMARY KEY,
    branch_code TEXT NOT NULL,
    city TEXT NOT NULL,
    UNIQUE (branch_code, city)
);


CREATE TABLE IF NOT EXISTS dds.dim_product_line (
    product_line_key BIGSERIAL PRIMARY KEY,
    product_line_name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS dds.dim_customer_segment (
    customer_segment_key BIGSERIAL PRIMARY KEY,
    customer_segment_name TEXT NOT NULL UNIQUE
);


CREATE TABLE IF NOT EXISTS dds.dim_payment_method (
    payment_method_key BIGSERIAL PRIMARY KEY,
    payment_method_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS dds.fct_sales (
    sale_key BIGSERIAL PRIMARY KEY,

    invoice_id TEXT NOT NULL UNIQUE,

    date_key INTEGER NOT NULL REFERENCES dds.dim_date(date_key),
    time_key INTEGER NOT NULL REFERENCES dds.dim_time(time_key),
    store_key BIGINT NOT NULL REFERENCES dds.dim_store(store_key),
    product_line_key BIGINT NOT NULL REFERENCES dds.dim_product_line(product_line_key),
    customer_segment_key BIGINT NOT NULL REFERENCES dds.dim_customer_segment(customer_segment_key),
    payment_method_key BIGINT NOT NULL REFERENCES dds.dim_payment_method(payment_method_key),

    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    tax_amount NUMERIC(12,4),
    total_amount NUMERIC(12,4),
    cogs NUMERIC(12,4),
    gross_income NUMERIC(12,4),
    rating NUMERIC(4,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE INDEX IF NOT EXISTS idx_fct_sales_invoice_id
ON dds.fct_sales(invoice_id);


CREATE INDEX IF NOT EXISTS idx_fct_sales_date_key
ON dds.fct_sales(date_key);