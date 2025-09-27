{{
config(
    materialized="incremental",
    unique_key=["orderitem_id"]
)
}}

SELECT
    ABS(oi.order_item_id) as orderitem_id,
    ABS(o.order_id) as order_id,
    LOWER(TRIM(o.customer_name)) as customer_name,
    LOWER(TRIM(SUBSTRING(o.customer_address, 1, POSITION(',' IN o.customer_address) - 1))) AS address,
    LOWER(TRIM(SUBSTRING(o.customer_address FROM POSITION(',' IN o.customer_address) + 1))) AS city,
    ABS(oi.product_id) as product_id,
    ABS(oi.quantity) as quantity, 
    CAST(oi.price AS decimal(10,2)) as price, 
    d.id AS orderdate_id
FROM {{ source("staging","orders") }} o 
INNER JOIN {{ source("staging","order_items") }} oi ON o.order_id  = oi.order_id
LEFT JOIN {{ ref("dim_date") }} d ON d.dt = o.order_date

{% if is_incremental() %}
WHERE d.id >= (SELECT COALESCE(MAX(orderdate_id), 0) FROM {{ this }})
{% endif %}
