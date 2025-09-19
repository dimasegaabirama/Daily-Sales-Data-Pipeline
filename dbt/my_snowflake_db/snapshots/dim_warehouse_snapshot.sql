{% snapshot dim_warehouse_snapshot %}

{{
    config(
      target_schema="snapshot",
      unique_key="warehouse_id",
      strategy="check",
      check_cols="all"
    )
}}

SELECT 
   warehouse_id, 
   location, 
   capacity
FROM {{ ref("dim_warehouses") }}

{% endsnapshot %}