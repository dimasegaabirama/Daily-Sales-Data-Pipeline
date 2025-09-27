{{ 
config(
    materialized="incremental",
    unique_key="supplier_id"
)
}}

SELECT 
   ABS(supplier_id) as supplier_id,
   LOWER(TRIM(name)) as supplier_name, 
   LOWER(TRIM(contact_name)) as contact_name, 
   LOWER(TRIM(contact_email)) as contact_email
FROM {{ source("staging", "suppliers") }}