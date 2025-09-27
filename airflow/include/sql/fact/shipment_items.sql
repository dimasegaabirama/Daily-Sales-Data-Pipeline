WITH cte_shipment AS 
( 
    SELECT shipment_id 
    FROM retail_supply_chain.shipments 
    WHERE shipment_date BETWEEN '{prev_ds}' AND '{ds}'
) 
SELECT 
    si.shipment_item_id, 
    si.shipment_id, 
    si.product_id, 
    si.quantity 
FROM retail_supply_chain.shipment_items si 
WHERE EXISTS ( 
    SELECT 1 
    FROM cte_shipment cs 
    WHERE cs.shipment_id = si.shipment_id
);
