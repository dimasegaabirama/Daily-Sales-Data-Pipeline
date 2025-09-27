WITH cte_order AS (
    SELECT order_id
    FROM retail_supply_chain.orders
    WHERE order_date BETWEEN '{prev_ds}' AND '{ds}'
)
SELECT
    oi.order_item_id,
    oi.order_id,
    oi.product_id,
    oi.quantity,
    oi.price
FROM retail_supply_chain.order_items oi
WHERE oi.order_id IN (SELECT order_id FROM cte_order);
