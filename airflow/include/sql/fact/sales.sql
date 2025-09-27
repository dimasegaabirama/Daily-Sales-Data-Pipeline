SELECT
    s.sale_id,
    s.sale_date,
    s.product_id,
    s.quantity,
    s.total_amount
FROM retail_supply_chain.sales s
WHERE s.sale_date BETWEEN '{prev_ds}' AND '{ds}';