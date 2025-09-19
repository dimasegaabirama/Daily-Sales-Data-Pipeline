{% snapshot dim_supplier_snapshot %}

{{
    config(
      target_schema="snapshot",
      unique_key="supplier_id",
      strategy="check",
      check_cols="all"
    )
}}

SELECT 
   supplier_id, 
   supplier_name, 
   contact_name, 
   contact_email
FROM {{ ref("dim_suppliers") }}

{% endsnapshot %}