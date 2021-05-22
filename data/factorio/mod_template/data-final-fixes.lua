-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require('lib')

data.raw["recipe"]["rocket-part"].ingredients = {{ rocket_recipe | safe }}

local technologies = data.raw["technology"]
local original_tech
local new_tree_copy
allowed_ingredients = {}
{%- for tech_name, technology in custom_data["custom_technologies"].items() %}
allowed_ingredients["{{ tech_name }}"] = {
{%- for ingredient in technology.ingredients %}
["{{ingredient}}"] = 1,
{%- endfor %}
}
{% endfor %}
local template_tech = table.deepcopy(technologies["automation"])
{#-  ensure the copy unlocks nothing #}
template_tech.unlocks = {}
template_tech.upgrade = false
template_tech.effects = {}
template_tech.prerequisites = {}

function prep_copy(new_copy, old_tech)
    old_tech.enabled = false
    new_copy.unit = table.deepcopy(old_tech.unit)
    local ingredient_filter = allowed_ingredients[old_tech.name]
    if ingredient_filter ~= nil then
        new_copy.unit.ingredients = filter_ingredients(new_copy.unit.ingredients, ingredient_filter)
    end
end

function set_ap_icon(tech)
    tech.icon = "__{{ mod_name }}__/graphics/icons/ap.png"
    tech.icons = nil
    tech.icon_size = 128
end

function copy_factorio_icon(tech, tech_source)
    tech.icon = table.deepcopy(technologies[tech_source].icon)
    tech.icons = table.deepcopy(technologies[tech_source].icons)
    tech.icon_size = table.deepcopy(technologies[tech_source].icon_size)
end

table.insert(data.raw["assembling-machine"]["assembling-machine-1"].crafting_categories, "crafting-with-fluid")

{# each randomized tech gets set to be invisible, with new nodes added that trigger those #}
{%- for original_tech_name, item_name, receiving_player in locations %}
original_tech = technologies["{{original_tech_name}}"]
{#- the tech researched by the local player #}
new_tree_copy = table.deepcopy(template_tech)
new_tree_copy.name = "ap-{{ tech_table[original_tech_name] }}-"{# use AP ID #}
prep_copy(new_tree_copy, original_tech)
{% if tech_cost != 1 %}
new_tree_copy.unit.count = math.max(1, math.floor(new_tree_copy.unit.count * {{ tech_cost_scale }}))
{% endif %}
{%- if item_name in tech_table and visibility -%}
{#- copy Factorio Technology Icon -#}
copy_factorio_icon(new_tree_copy, "{{ item_name }}")
{%- else -%}
{#- use default AP icon if no Factorio graphics exist -#}
set_ap_icon(new_tree_copy)
{%- endif -%}
{#- connect Technology  #}
{%- if original_tech_name in tech_tree_layout_prerequisites %}
{%- for prerequesite in tech_tree_layout_prerequisites[original_tech_name] %}
table.insert(new_tree_copy.prerequisites, "ap-{{ tech_table[prerequesite] }}-")
{% endfor %}
{% endif -%}
{#- add new Technology to game #}
data:extend{new_tree_copy}

{% endfor %}