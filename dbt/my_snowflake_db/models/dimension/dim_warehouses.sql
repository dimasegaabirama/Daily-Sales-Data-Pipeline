{{ 
config(
    materialized="incremental",
    unique_key="warehouse_id"
)
}}

SELECT 
   ABS(warehouse_id) as warehouse_id, 
   LOWER(TRIM(location)) as location, 
   ABS(capacity) as capacity
FROM {{ source("staging","warehouses") }}