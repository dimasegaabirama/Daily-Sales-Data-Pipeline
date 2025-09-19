{% test validate_in_set(model, column_name, value) %}

 SELECT {{ column_name }} 
 FROM {{ model }} WHERE {{ column_name }} NOT IN {{ value }} OR {{ column_name }} IS NULL 

{% endtest %}

{% test check_trim_lower(model, column_name) %}

SELECT {{ column_name }}
FROM {{ model }} WHERE {{ column_name }} != LOWER(TRIM({{ column_name }}))

{% endtest %}


