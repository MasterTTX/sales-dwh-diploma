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

CREATE TABLE IF NOT EXISTS nds.sales (
    sale_id BIGSERIAL PRIMARY KEY,

    invoice_id TEXT NOT NULL UNIQUE,

    branch_id BIGINT NOT NULL REFERENCES nds.branches(branch_id),
    product_line_id BIGINT NOT NULL REFERENCES nds.product_lines(product_line_id),
    customer_segment_id BIGINT NOT NULL REFERENCES nds.customer_segments(customer_segment_id),
    payment_method_id BIGINT NOT NULL REFERENCES nds.payment_methods(payment_method_id),

    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(12,2) NOT NULL CHECK (unit_price >= 0),
    tax_amount NUMERIC(12,4),
    total_amount NUMERIC(12,4),
    cogs NUMERIC(12,4),
    gross_income NUMERIC(12,4),
    rating NUMERIC(4,2),

    sale_date DATE NOT NULL,
    sale_time TIME NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);