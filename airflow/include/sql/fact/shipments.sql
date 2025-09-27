WITH cte_shipment AS (
    SELECT
        shipment_id,
        supplier_id,
        warehouse_id,
        shipment_date
    FROM retail_supply_chain.shipments
    WHERE shipment_date BETWEEN '{prev_ds}' AND '{ds}'
)
SELECT
    shipment_id,
    supplier_id,
    warehouse_id,
    shipment_date
FROM cte_shipment;
