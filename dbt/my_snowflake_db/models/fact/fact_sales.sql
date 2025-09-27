{{ 
config(
    materialized="incremental",
    unique_key=["sale_id"]
)
}}

SELECT
	ABS(sale_id) AS sale_id,
	ABS(product_id) AS product_id,
	ABS(quantity) AS quantity,
	CAST(total_amount AS decimal(10,2)) AS total_amount,
	d.id AS saledate_id
FROM {{ source("staging","sales") }} s 
LEFT JOIN {{ ref("dim_date") }} d ON s.sale_date = d.dt

{% if is_incremental() %}
WHERE d.id >= (SELECT COALESCE(MAX(saledate_id), 0) FROM {{ this }})
{% endif %}

