{% from "macros.lua" import dict_to_recipe %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require('lib')
data.raw["rocket-silo"]["rocket-silo"].fluid_boxes = {
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { type = "input", position = { 0, 5 } },
            { type = "input", position = { 0, -5 } },
            { type = "input", position = { 5, 0 } },
            { type = "input", position = { -5, 0 } }
        }
    },
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { type = "input", position = { -3, 5 } },
            { type = "input", position = { -3, -5 } },
            { type = "input", position = { 5, -3 } },
            { type = "input", position = { -5, -3 } }
        }
    },
    {
        production_type = "input",
        pipe_picture = assembler2pipepictures(),
        pipe_covers = pipecoverspictures(),
        base_area = 10,
        base_level = -1,
        pipe_connections = {
            { type = "input", position = { 3, 5 } },
            { type = "input", position = { 3, -5 } },
            { type = "input", position = { 5, 3 } },
            { type = "input", position = { -5, 3 } }
        }
    },
    off_when_no_fluid_recipe = true
}

{%- for recipe_name, recipe in custom_recipes.items() %}
data.raw["recipe"]["{{recipe_name}}"].category = "{{recipe.category}}"
data.raw["recipe"]["{{recipe_name}}"].ingredients = {{ dict_to_recipe(recipe.ingredients, liquids) }}
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

{%- if max_science_pack < 6 %}
    technologies["space-science-pack"].effects = {}
    {%- if max_science_pack == 0 %}
        table.insert (technologies["automation"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 1 %}
        table.insert (technologies["logistic-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 2 %}
        table.insert (technologies["military-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 3 %}
        table.insert (technologies["chemical-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 4 %}
        table.insert (technologies["production-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {%- elif max_science_pack == 5 %}
        table.insert (technologies["utility-science-pack"].effects, {type = "unlock-recipe", recipe = "satellite"})
    {% endif %}
{% endif %}
{%- if silo == 2 %}
    data.raw["recipe"]["rocket-silo"].enabled = true
{% endif %}

function prep_copy(new_copy, old_tech)
    old_tech.hidden = true
    local ingredient_filter = allowed_ingredients[old_tech.name]
    if ingredient_filter ~= nil then
	    if mods["science-not-invited"] then
			local weights = {
				["automation-science-pack"] =   0, -- Red science
				["logistic-science-pack"]   =   0, -- Green science
				["military-science-pack"]   =   0, -- Black science
				["chemical-science-pack"]   =   0, -- Blue science
				["production-science-pack"] =   0, -- Purple science
				["utility-science-pack"]    =   0, -- Yellow science
				["space-science-pack"]      =   0  -- Space science
			}
			for key, value in pairs(ingredient_filter) do
				weights[key] = value
			end
			SNI.setWeights(weights)
            -- Just in case an ingredient is being added to an existing tech. Found the root cause of the 9.223e+18 problem.
            -- Turns out science-not-invited was ultimately dividing by zero, due to it being unaware of there being added ingredients.
            old_tech.unit.ingredients = add_ingredients(old_tech.unit.ingredients, ingredient_filter)
			SNI.sendInvite(old_tech)
			-- SCIENCE-not-invited could potentially make tech cost 9.223e+18.
			old_tech.unit.count = math.min(100000, old_tech.unit.count)
		end
		new_copy.unit = table.deepcopy(old_tech.unit)
		new_copy.unit.ingredients = filter_ingredients(new_copy.unit.ingredients, ingredient_filter)
		new_copy.unit.ingredients = add_ingredients(new_copy.unit.ingredients, ingredient_filter)
    else
        new_copy.unit = table.deepcopy(old_tech.unit)
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
