{{ 
config(
    materialized="incremental",
    unique_key=["sale_id"]
)
}}

SELECT
	SaleID AS sale_id,
	ProductID AS product_id,
	Quantity AS quantity,
	CAST(TotalAmount AS decimal(10,2)) AS total_amount,
	d.id AS saledate_id
FROM {{ source("staging","sales") }} s 
LEFT JOIN {{ ref("dim_date") }} d ON s.saledate = d.dt

{% if is_incremental() %}
WHERE d.id >= (SELECT COALESCE(MAX(saledate_id), 0) FROM {{ this }})
{% endif %}

