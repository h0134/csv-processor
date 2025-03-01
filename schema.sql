-- Create the product_images table
CREATE TABLE IF NOT EXISTS product_images (
    id SERIAL PRIMARY KEY,
    serial_number VARCHAR(255) NOT NULL,
    request_id VARCHAR(255) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    input_image_urls TEXT,  -- Comma-separated URLs
    output_image_urls TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the product_images table
CREATE TABLE IF NOT EXISTS request_details (

    request_id VARCHAR(255) NOT NULL,
    request_status VARCHAR(255) NOT NULL
);
