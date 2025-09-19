{{
config(
    materialized="incremental",
    unique_key="id"
)
}}

WITH params AS (
    SELECT 
        DATE('2025-01-01') AS start_date,
        DATE('2026-12-31') AS end_date,
        DATEDIFF(day, DATE('2025-01-01'), DATE('2026-12-31')) + 1 AS num_days
),
date_range AS (
    SELECT 
        DATEADD(day, seq4(), p.start_date) AS dt
    FROM params p,
         TABLE(GENERATOR(ROWCOUNT => 730)) -- manual max row
    WHERE seq4() < p.num_days
)
SELECT 
   TO_VARCHAR(dt, 'YYYYMMDD') AS id,
   dt,
   EXTRACT(YEAR FROM dt) AS year,
   EXTRACT(MONTH FROM dt) AS month,
   EXTRACT(DAY FROM dt) AS day,
   EXTRACT(QUARTER FROM dt) AS quarter,
   LOWER(TRIM(TO_VARCHAR(dt, 'MMMM'))) AS month_name,
   LOWER(TRIM(TO_VARCHAR(dt, 'DY'))) AS weekday_name,  
   CASE 
      WHEN DAYOFWEEK(dt) IN (1, 7) THEN 'weekend'
      ELSE 'weekday'
   END AS day_type,
   DAY(LAST_DAY(dt)) AS days_in_month
FROM date_range

{% if is_incremental() %}
WHERE dt > (SELECT max(dt) FROM {{ this }})
{% endif %}