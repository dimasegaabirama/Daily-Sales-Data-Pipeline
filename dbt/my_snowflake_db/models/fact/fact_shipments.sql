{{ 
config(
    materialized="incremental",
    unique_key=["shipmentitem_id"]
)
}}

SELECT
   si.ShipmentItemID AS shipmentitem_id,
   s.SupplierID AS supplier_id,
   s.WarehouseID AS warehouse_id,
   si.ProductID AS product_id,
   si.Quantity AS quantity,
   d.id AS shipmentdate_id
FROM {{ source("staging", "shipments") }} s INNER JOIN {{ source("staging", "shipmentitems") }} si 
ON s.shipmentid = si.shipmentid LEFT JOIN {{ ref("dim_date") }} d ON s.shipmentdate = d.dt

{% if is_incremental() %}
WHERE d.id >= (SELECT COALESCE(MAX(shipmentdate_id), 0) FROM {{ this }})
{% endif %}