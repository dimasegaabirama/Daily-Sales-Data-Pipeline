{% test validate_fact_inventory_arrays(model) %}

SELECT
    m.warehouse_id,
    m.snapshotdate_id,
    ARRAY_SIZE(COALESCE(m.product_id_array, ARRAY_CONSTRUCT())) AS len_product_id,
    ARRAY_SIZE(COALESCE(m.stock_array, ARRAY_CONSTRUCT())) AS len_product_stocks,
    COALESCE(SUM(f.value::NUMBER), 0) AS sum_product_stocks,
    m.total_stock
FROM {{ model }} AS m,
     LATERAL FLATTEN(input => COALESCE(m.stock_array, ARRAY_CONSTRUCT())) f
GROUP BY m.warehouse_id, m.snapshotdate_id, m.total_stock, m.product_id_array, m.stock_array
HAVING ARRAY_SIZE(COALESCE(m.product_id_array, ARRAY_CONSTRUCT())) 
           != ARRAY_SIZE(COALESCE(m.stock_array, ARRAY_CONSTRUCT()))
    OR COALESCE(SUM(f.value::NUMBER), 0) != m.total_stock

{% endtest %}

{% test validate_arrays_ref_other_table(model, column_name, ref_table, ref_column) %}

WITH exploded AS (
    SELECT 
        f.value AS ref_value
    FROM {{ model }} m,
         LATERAL FLATTEN(input => m.{{ column_name }}) f
)

SELECT e.ref_value
FROM exploded e
LEFT JOIN {{ ref_table }} r
    ON e.ref_value = r.{{ ref_column }}
WHERE r.{{ ref_column }} IS NULL

{% endtest %}

{% test validate_arrays_negative(model, column_name) %}

WITH exploded AS (
    SELECT f.value::NUMBER AS element_value
    FROM {{ model }} AS m,
         LATERAL FLATTEN(input => m.{{ column_name }}) AS f
)

SELECT element_value
FROM exploded
WHERE element_value < 0

{% endtest %}