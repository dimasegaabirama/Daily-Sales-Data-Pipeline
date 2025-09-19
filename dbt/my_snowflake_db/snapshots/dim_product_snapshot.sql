{% snapshot dim_product_snapshot %}

{{
    config(
      target_schema="snapshot",
      unique_key="product_id",
      strategy="check",
      check_cols="all"
    )
}}

SELECT 
   product_id, 
   product_name, 
   category,
   price
FROM {{ ref("dim_products") }}

{% endsnapshot %}