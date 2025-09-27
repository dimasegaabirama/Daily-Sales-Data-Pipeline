WITH cte_order AS (
    SELECT 
        order_id,
        order_date,
        customer_name,
        customer_address
    FROM retail_supply_chain.orders o
    WHERE order_date BETWEEN '{prev_ds}' AND '{ds}'
)
SELECT
    order_id,
    order_date,
    customer_name,
    customer_address
FROM cte_order;