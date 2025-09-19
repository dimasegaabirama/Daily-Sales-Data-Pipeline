{{ 
config(
    materialized="incremental",
    unique_key="supplier_id"
)
}}

SELECT 
   SupplierID as supplier_id,
   LOWER(TRIM(Name)) as supplier_name, 
   LOWER(TRIM(ContactName)) as contact_name, 
   LOWER(TRIM(ContactEmail)) as contact_email
FROM {{ source("staging", "suppliers") }}