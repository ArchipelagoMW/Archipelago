{% macro dict_to_lua(dict) -%}
{
{%- for key, value in dict.items() -%}
    ["{{ key }}"] = {{ variable_to_lua(value) }}{% if not loop.last %},{% endif %}
{% endfor -%}
}
{% endmacro %}
{% macro list_to_lua(list) -%}
{
{%- for key in list -%}
    {{ variable_to_lua(key) }}{% if not loop.last %},{% endif %}
{% endfor -%}
}
{%- endmacro %}
{%- macro variable_to_lua(value) %}
{%- if value is mapping -%}{{ dict_to_lua(value) }}
{%- elif value is boolean -%}{{ value | string | lower }}
{%- elif value is string -%}"{{ value | safe }}"
{%- elif value is iterable -%}{{ list_to_lua(value) }}
{%- else -%} {{ value | safe }}
{%- endif -%}
{%- endmacro -%}
{% macro dict_to_recipe(dict, liquids) -%}
{
{%- for key, value in dict.items() -%}
    {type = {% if key in liquids %}"fluid"{% else %}"item"{% endif %}, name = "{{ key }}", amount = {{ value | safe }}}{% if not loop.last %},{% endif %}
{% endfor -%}
}
{%- endmacro %}
