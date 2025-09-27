{{
config(
    materialized="incremental",
    unique_key=["warehouse_id","snapshotdate_id"]
)
}}

WITH latest AS (
    {% if is_incremental() %}
        SELECT COALESCE(MAX(snapshotdate_id), 0) AS max_snapshot FROM {{ this }}
    {% else %}
        SELECT 0 AS max_snapshot
    {% endif %}
),
stock_agg AS (
    SELECT
        ABS(s.warehouse_id) AS warehouse_id,
        ABS(s.product_id) AS product_id,
        SUM(s.quantity) AS total_stock,
        d.id AS snapshotdate_id
    FROM {{ source("staging", "stock") }} s
    JOIN {{ ref("dim_date") }} d
        ON d.dt = TO_DATE('{{ var("run_date") }}','YYYY-MM-DD')
    CROSS JOIN latest
    {% if is_incremental() %}
    WHERE d.id > latest.max_snapshot
    {% endif %}
    GROUP BY s.warehouse_id, s.product_id, d.id
)

SELECT
    warehouse_id,
    ARRAY_AGG(product_id) AS product_id_array,
    ARRAY_AGG(total_stock) AS stock_array,
    SUM(total_stock) AS total_stock,
    snapshotdate_id
FROM stock_agg
GROUP BY warehouse_id, snapshotdate_id
ORDER BY snapshotdate_id, warehouse_id