CREATE TABLE IF NOT EXISTS nds.branches (
    branch_id BIGSERIAL PRIMARY KEY,
    branch_code TEXT NOT NULL UNIQUE,
    city TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS nds.product_lines (
    product_line_id BIGSERIAL PRIMARY KEY,
    product_line_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS nds.customer_segments (
    customer_segment_id BIGSERIAL PRIMARY KEY,
    customer_segment_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS nds.payment_methods (
    payment_method_id BIGSERIAL PRIMARY KEY,
    payment_method_name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);