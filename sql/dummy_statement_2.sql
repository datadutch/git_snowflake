-- Dummy SQL statement for testing deployment
CREATE OR REPLACE TABLE dummy_table_2 (
    id INT,
    name STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    PRIMARY KEY (id),
    description STRING,
) COMMENT = 'Dummy table for testing deployment'
;
