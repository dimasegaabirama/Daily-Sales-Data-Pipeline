{% test validate_id_date(model, column_name, column_date_target) %}

 SELECT {{ column_name }} 
 FROM {{ model }} WHERE {{ column_name }} != TO_VARCHAR({{ column_date_target }}, 'YYYYMMDD')

{% endtest %}

{% test no_future_dates(model, column_name) %}

with max_val as (
    select max({{ column_name }}) as max_date_id
    from {{ model }}
)

select mv.max_date_id
from max_val mv
left join {{ ref('dim_date') }} dd
    on mv.max_date_id = dd.id
where mv.max_date_id is not null
  and dd.dt > '{{ var("run_date") }}'

{% endtest %}