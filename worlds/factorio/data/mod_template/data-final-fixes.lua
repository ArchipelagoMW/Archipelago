{% from "macros.lua" import dict_to_recipe, variable_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require('lib')
data.raw["item"]["rocket-part"].hidden = false
data.raw["rocket-silo"]["rocket-silo"].fluid_boxes = {
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { flow_direction = "input", direction = defines.direction.south, position = { 0, 4.2 } },
            { flow_direction = "input", direction = defines.direction.north, position = { 0, -4.2 } },
            { flow_direction = "input", direction = defines.direction.east, position = { 4.2, 0 } },
            { flow_direction = "input", direction = defines.direction.west, position = { -4.2, 0 } }
        }
    },
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { flow_direction = "input", direction = defines.direction.south, position = { -3, 4.2 } },
            { flow_direction = "input", direction = defines.direction.north, position = { -3, -4.2 } },
            { flow_direction = "input", direction = defines.direction.east, position = { 4.2, -3 } },
            { flow_direction = "input", direction = defines.direction.west, position = { -4.2, -3 } }
        }
    },
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        volume = 1000,
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { flow_direction = "input", direction = defines.direction.south, position = { 3, 4.2 } },
            { flow_direction = "input", direction = defines.direction.north, position = { 3, -4.2 } },
            { flow_direction = "input", direction = defines.direction.east, position = { 4.2, 3 } },
            { flow_direction = "input", direction = defines.direction.west, position = { -4.2, 3 } }
        }
    }
}
data.raw["rocket-silo"]["rocket-silo"].fluid_boxes_off_when_no_fluid_recipe = true

{%- for recipe_name, recipe in custom_recipes.items() %}
data.raw["recipe"]["{{recipe_name}}"].category = "{{recipe.category}}"
data.raw["recipe"]["{{recipe_name}}"].ingredients = {{ dict_to_recipe(recipe.ingredients, liquids) }}
{%- endfor %}

local technologies = data.raw["technology"]
local new_tree_copy

local template_tech = table.deepcopy(technologies["automation"])
{#-  ensure the copy unlocks nothing #}
template_tech.unlocks = {}
template_tech.upgrade = false
template_tech.effects = {}
template_tech.prerequisites = {}

{%- if silo == 2 %}
    data.raw["recipe"]["rocket-silo"].enabled = true
{% endif %}

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

function set_energy(recipe_name, energy)
    local recipe = data.raw.recipe[recipe_name]

    if (recipe.normal ~= nil) then
        recipe.normal.energy_required = energy
    end
    if (recipe.expensive ~= nil) then
        recipe.expensive.energy_required = energy
    end
    if (recipe.expensive == nil and recipe.normal == nil) then
        recipe.energy_required = energy
    end
end

data.raw["assembling-machine"]["assembling-machine-1"].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
data.raw["assembling-machine"]["assembling-machine-2"].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
data.raw["assembling-machine"]["assembling-machine-1"].fluid_boxes = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-2"].fluid_boxes)
if mods["factory-levels"] then
    -- Factory-Levels allows the assembling machines to get faster (and depending on settings), more productive at crafting products, the more the
    -- assembling machine crafts the product.  If the machine crafts enough, it may auto-upgrade to the next tier.
    for i = 1, 25, 1 do
        data.raw["assembling-machine"]["assembling-machine-1-level-" .. i].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
        data.raw["assembling-machine"]["assembling-machine-1-level-" .. i].fluid_boxes = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-2"].fluid_boxes)
    end
    for i = 1, 50, 1 do
        data.raw["assembling-machine"]["assembling-machine-2-level-" .. i].crafting_categories = table.deepcopy(data.raw["assembling-machine"]["assembling-machine-3"].crafting_categories)
    end
end

data.raw["ammo"]["artillery-shell"].stack_size = 10

{# each randomized tech gets set to be invisible, with new nodes added that trigger those #}
{%- for original_tech_name in base_tech_table -%}
technologies["{{ original_tech_name }}"].hidden = true
technologies["{{ original_tech_name }}"].hidden_in_factoriopedia = true
{% endfor %}
{%- for location, item in locations %}
{#- the tech researched by the local player #}
new_tree_copy = table.deepcopy(template_tech)
new_tree_copy.name = "ap-{{ location.address }}-"{# use AP ID #}
{% if location.crafted_item is not none %}
new_tree_copy.research_trigger = {
    type = "{{ 'craft-fluid' if location.crafted_item in liquids else 'craft-item' }}",
    {{ 'fluid' if location.crafted_item in liquids else 'item' }} = {{ variable_to_lua(location.crafted_item) }}
}
new_tree_copy.unit = nil
{% else %}
new_tree_copy.unit.count = {{ location.count }}
new_tree_copy.unit.ingredients = {{ variable_to_lua(location.factorio_ingredients) }}
{% endif %}
{%- if location.revealed and item.name in base_tech_table -%}
{#- copy Factorio Technology Icon #}
copy_factorio_icon(new_tree_copy, "{{ item.name }}")
{%- if item.name == "rocket-silo" and item.player == location.player %}
{%- for ingredient in custom_recipes["rocket-part"].ingredients %}
table.insert(new_tree_copy.effects, {type = "nothing", effect_description = "Ingredient {{ loop.index }}: {{ ingredient }}"})
{% endfor -%}
{% endif -%}
{%- elif location.revealed and item.name in progressive_technology_table -%}
copy_factorio_icon(new_tree_copy, "{{ progressive_technology_table[item.name][0] }}")
{%- else -%}
{#- use default AP icon if no Factorio graphics exist -#}
{% if item.advancement or not tech_tree_information %}set_ap_icon(new_tree_copy){% else %}set_ap_unimportant_icon(new_tree_copy){% endif %}
{%- endif -%}
{#- connect Technology  #}
{%- if location in tech_tree_layout_prerequisites %}
{%- for prerequisite in tech_tree_layout_prerequisites[location] %}
table.insert(new_tree_copy.prerequisites, "ap-{{ prerequisite.address }}-")
{% endfor %}
{% endif -%}
{#- add new Technology to game #}
data:extend{new_tree_copy}
{% endfor %}
{#- Recipe Rando #}
{% if recipe_time_scale %}
{%- for recipe_name, recipe in recipes.items() %}
{%- if recipe.category not in ("basic-solid", "basic-fluid") %}
adjust_energy("{{ recipe_name }}", {{ flop_random(*recipe_time_scale) }})
{%- endif %}
{%- endfor -%}
{% elif recipe_time_range %}
{%- for recipe_name, recipe in recipes.items() %}
{%- if recipe.category not in ("basic-solid", "basic-fluid") %}
set_energy("{{ recipe_name }}", {{ flop_random(*recipe_time_range) }})
{%- endif %}
{%- endfor -%}
{% endif %}

{%- if silo==2 %}
-- disable silo research for pre-placed silo
technologies["rocket-silo"].enabled = false
technologies["rocket-silo"].visible_when_disabled = false
{%- endif %}
