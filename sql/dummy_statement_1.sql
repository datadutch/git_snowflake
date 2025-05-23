-- Dummy SQL statement for testing deployment
CREATE OR REPLACE TABLE dummy_table (
    id INT,
    name STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (id),
    member char(10)
) COMMENT = 'Dummy table for testing deployment'
;
