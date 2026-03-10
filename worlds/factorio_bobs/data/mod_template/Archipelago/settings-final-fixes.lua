{%- for mod, settings in mod_settings.items() %}
{%- for setting_name, info in settings.items() %}
data.raw["{{info['type']}}"]["{{setting_name}}"].hidden = true
{%- if info['type'] == "bool-setting" or info['type'] == "color-setting" %}
data.raw["{{info['type']}}"]["{{setting_name}}"].forced_value = {{info['value'] | lower}}
data.raw["{{info['type']}}"]["{{setting_name}}"].default_value = {{info['value'] | lower}}
{%- else %}
{%- if info['type'] == "string-setting" %}
data.raw["{{info['type']}}"]["{{setting_name}}"].allowed_values = { "{{info['value']}}" }
data.raw["{{info['type']}}"]["{{setting_name}}"].default_value = "{{info['value']}}"
{%- else %}
data.raw["{{info['type']}}"]["{{setting_name}}"].allowed_values = { {{info['value']}} }
data.raw["{{info['type']}}"]["{{setting_name}}"].default_value = {{info['value']}}
{% endif -%}
{% endif -%}
{% endfor -%}
{% endfor -%}