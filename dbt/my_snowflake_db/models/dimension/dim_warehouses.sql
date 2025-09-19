{{ 
config(
    materialized="incremental",
    unique_key="warehouse_id"
)
}}

SELECT 
   WarehouseID as warehouse_id, 
   LOWER(TRIM(Location)) as location, 
   Capacity as capacity
FROM {{ source("staging","warehouses") }}