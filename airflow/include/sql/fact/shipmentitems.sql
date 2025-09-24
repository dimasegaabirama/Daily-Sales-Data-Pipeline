WITH cte_shipment AS (
    SELECT ShipmentID
    FROM RETAIL_SUPPLY_CHAIN.Shipments 
    WHERE ShipmentDate BETWEEN '{ prev_ds }' AND '{ ds }'
)
SELECT 
    si.ShipmentItemID,
    si.ShipmentID,
    si.ProductID,
    si.Quantity
FROM RETAIL_SUPPLY_CHAIN.ShipmentItems si
WHERE EXISTS (
    SELECT 1
    FROM cte_shipment cs
    WHERE cs.ShipmentID = si.ShipmentID
);
