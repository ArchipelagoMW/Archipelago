{% macro dict_to_lua(dict) -%}
{
{%- for key, value in dict.items() -%}
    ["{{ key }}"] = {{ variable_to_lua(value) }}{% if not loop.last %},{% endif %}
{% endfor -%}
}
{%- endmacro %}
{%- macro variable_to_lua(value) %}
{%- if value is mapping -%}{{ dict_to_lua(value) }}
{%- elif value is boolean -%}{{ value | string | lower }}
{%- elif value is string -%} "{{ value | safe }}"
{%- else -%} {{ value | safe }}
{%- endif -%}
{%- endmacro -%}
{% macro dict_to_recipe(dict) -%}
{
{%- for key, value in dict.items() -%}
    {"{{ key }}", {{ value | safe }}}{% if not loop.last %},{% endif %}
{% endfor -%}
}
{%- endmacro %}