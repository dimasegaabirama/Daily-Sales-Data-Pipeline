WITH cte_shipment AS (
    SELECT
        ShipmentID,
        SupplierID,
        WarehouseID,
        ShipmentDate
    FROM RETAIL_SUPPLY_CHAIN.Shipments 
    WHERE ShipmentDate BETWEEN '{ prev_ds }' AND '{ ds }'
    )

SELECT
    ShipmentID,
    SupplierID,
    WarehouseID,
    ShipmentDate
FROM cte_shipment