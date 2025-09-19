{% test validate_id_date(model, column_name, column_date_target) %}

 SELECT {{ column_name }} 
 FROM {{ model }} WHERE {{ column_name }} != TO_VARCHAR({{ column_date_target }}, 'YYYYMMDD')

{% endtest %}

{% test dim_date_max_current_date(model, column_name) %}

with max_val as (
    select max({{ column_name }}) as max_date_id
    from {{ model }}
)

select mv.max_date_id
from max_val mv
join {{ ref('dim_date') }} dd
    on mv.max_date_id = dd.id
where dd.dt != '{{ var("run_date") }}'
   or mv.max_date_id is null

{% endtest %}