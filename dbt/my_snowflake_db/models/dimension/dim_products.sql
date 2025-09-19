{{ 
config(
    materialized="incremental",
    unique_key="product_id"
)
}}

SELECT 
   ProductID as product_id, 
   LOWER(TRIM(Name)) as product_name, 
   LOWER(TRIM(Category)) as category,
   CAST(price AS decimal(10,2)) as price
FROM {{ source("staging", "products") }}
