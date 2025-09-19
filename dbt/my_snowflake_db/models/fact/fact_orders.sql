{{
config(
    materialized="incremental",
    unique_key=["orderitem_id"]
)
}}

SELECT
    oi.OrderItemID as orderitem_id,
    LOWER(TRIM(o.CustomerName)) as customer_name,
    LOWER(TRIM(o.CustomerAddress)) as customer_address,
    oi.ProductID as product_id,
    oi.Quantity as quantity, 
    CAST(oi.price AS decimal(10,2)) as price, 
    d.id AS orderdate_id
FROM {{ source("staging","orders") }} o 
INNER JOIN {{ source("staging","orderitems") }} oi ON o.OrderID  = oi.OrderID 
LEFT JOIN {{ ref("dim_date") }} d ON d.dt = o.OrderDate

{% if is_incremental() %}
WHERE d.id >= (SELECT COALESCE(MAX(orderdate_id), 0) FROM {{ this }})
{% endif %}
