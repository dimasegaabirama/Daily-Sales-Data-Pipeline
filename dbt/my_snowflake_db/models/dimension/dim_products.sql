{{ 
config(
    materialized="incremental",
    unique_key="product_id"
)
}}

SELECT 
   ABS(product_id) as product_id, 
   LOWER(TRIM(name)) as product_name, 
   LOWER(TRIM(category)) as category,
   CAST(price AS decimal(10,2)) as price
FROM {{ source("staging", "products") }}
