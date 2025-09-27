{{ 
config(
    materialized="incremental",
    unique_key=["shipmentitem_id"]
)
}}

SELECT
   ABS(si.shipment_item_id) AS shipmentitem_id,
   ABS(s.supplier_id) AS supplier_id,
   ABS(s.warehouse_id) AS warehouse_id,
   ABS(si.product_id) AS product_id,
   ABS(si.quantity) AS quantity,
   d.id AS shipmentdate_id
FROM {{ source("staging", "shipments") }} s INNER JOIN {{ source("staging", "shipment_items") }} si 
ON s.shipment_id = si.shipment_id LEFT JOIN {{ ref("dim_date") }} d ON s.shipment_date = d.dt

{% if is_incremental() %}
WHERE d.id >= (SELECT COALESCE(MAX(shipmentdate_id), 0) FROM {{ this }})
{% endif %}