WITH cte_order AS (
    SELECT 
        orderid,
        orderdate,
        customername,
        customeraddress
    FROM RETAIL_SUPPLY_CHAIN.Orders o 
    WHERE orderdate BETWEEN '{ prev_ds }' AND '{ ds }'
    )
        
SELECT
    orderid,
    orderdate,
    customername,
    customeraddress
FROM cte_order