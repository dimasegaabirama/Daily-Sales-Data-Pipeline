SELECT
    s.SaleID,
    s.SaleDate,
    s.ProductID,
    s.Quantity,
    s.TotalAmount
FROM RETAIL_SUPPLY_CHAIN.Sales s 
WHERE s.SaleDate BETWEEN '{ prev_ds }' AND '{ ds }'