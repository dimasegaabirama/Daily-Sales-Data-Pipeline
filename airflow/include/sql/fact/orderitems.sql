WITH cte_order AS (
    SELECT orderid
    FROM RETAIL_SUPPLY_CHAIN.Orders 
    WHERE orderdate BETWEEN '{ prev_ds }' AND '{ ds }'
    )
    
SELECT
    oi.OrderItemID,
    oi.OrderID,
    oi.ProductID,
    oi.Quantity,
    oi.Price
FROM RETAIL_SUPPLY_CHAIN.OrderItems oi 
WHERE oi.OrderID IN (SELECT orderid FROM cte_order)