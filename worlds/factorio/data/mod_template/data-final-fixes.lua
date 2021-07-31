{% from "macros.lua" import dict_to_recipe %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require('lib')

{%- for recipe_name, recipe in custom_recipes.items() %}
data.raw["recipe"]["{{recipe_name}}"].ingredients = {{ dict_to_recipe(recipe.ingredients) }}
{%- endfor %}

local technologies = data.raw["technology"]
local original_tech
local new_tree_copy
allowed_ingredients = {}
{%- for tech_name, technology in custom_technologies.items() %}
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
    old_tech.hidden = true
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

function set_ap_unimportant_icon(tech)
    tech.icon = "__{{ mod_name }}__/graphics/icons/ap_unimportant.png"
    tech.icons = nil
    tech.icon_size = 128
end

function copy_factorio_icon(tech, tech_source)
    tech.icon = table.deepcopy(technologies[tech_source].icon)
    tech.icons = table.deepcopy(technologies[tech_source].icons)
    tech.icon_size = table.deepcopy(technologies[tech_source].icon_size)
end

{# This got complex, but seems to be required to hit all corner cases #}
function adjust_energy(recipe_name, factor)
    local recipe = data.raw.recipe[recipe_name]
    local energy = recipe.energy_required

    if (recipe.normal ~= nil) then
        if (recipe.normal.energy_required == nil) then
            energy = 0.5
        else
            energy = recipe.normal.energy_required
        end
        recipe.normal.energy_required = energy * factor
    end
    if (recipe.expensive ~= nil) then
        if (recipe.expensive.energy_required == nil) then
            energy = 0.5
        else
            energy = recipe.expensive.energy_required
        end
        recipe.expensive.energy_required = energy * factor
    end
    if (energy ~= nil) then
        data.raw.recipe[recipe_name].energy_required = energy * factor
    elseif (recipe.expensive == nil and recipe.normal == nil) then
        data.raw.recipe[recipe_name].energy_required = 0.5 * factor
    end
end

data.raw["assembling-machine"]["assembling-machine-1"].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
data.raw["assembling-machine"]["assembling-machine-2"].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
data.raw["assembling-machine"]["assembling-machine-1"].fluid_boxes = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-2"].fluid_boxes)
data.raw["ammo"]["artillery-shell"].stack_size = 10

{# each randomized tech gets set to be invisible, with new nodes added that trigger those #}
{%- for original_tech_name, item_name, receiving_player, advancement in locations %}
original_tech = technologies["{{original_tech_name}}"]
{#- the tech researched by the local player #}
new_tree_copy = table.deepcopy(template_tech)
new_tree_copy.name = "ap-{{ tech_table[original_tech_name] }}-"{# use AP ID #}
prep_copy(new_tree_copy, original_tech)
{% if tech_cost_scale != 1 %}
new_tree_copy.unit.count = math.max(1, math.floor(new_tree_copy.unit.count * {{ tech_cost_scale }}))
{% endif %}
{%- if (tech_tree_information == 2 or original_tech_name in static_nodes) and item_name in base_tech_table -%}
{#- copy Factorio Technology Icon -#}
copy_factorio_icon(new_tree_copy, "{{ item_name }}")
{%- if original_tech_name == "rocket-silo" and original_tech_name in static_nodes %}
{%- for ingredient in custom_recipes["rocket-part"].ingredients %}
table.insert(new_tree_copy.effects, {type = "nothing", effect_description = "Ingredient {{ loop.index }}: {{ ingredient }}"})
{% endfor -%}
{% endif -%}
{%- elif (tech_tree_information == 2 or original_tech_name in static_nodes) and item_name in progressive_technology_table -%}
copy_factorio_icon(new_tree_copy, "{{ progressive_technology_table[item_name][0] }}")
{%- else -%}
{#- use default AP icon if no Factorio graphics exist -#}
{% if advancement or not tech_tree_information %}set_ap_icon(new_tree_copy){% else %}set_ap_unimportant_icon(new_tree_copy){% endif %}
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
{% if recipe_time_scale %}
{%- for recipe_name, recipe in recipes.items() %}
{%- if recipe.category != "mining" %}
adjust_energy("{{ recipe_name }}", {{ flop_random(*recipe_time_scale) }})
{%- endif %}
{%- endfor -%}
{% endif %}

{%- if silo==2 %}
-- disable silo research for pre-placed silo
technologies["rocket-silo"].hidden = true
{%- endif %}
