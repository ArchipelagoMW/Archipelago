{% from "macros.lua" import dict_to_recipe, dict_to_lua, variable_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template

local archipelago = {}


--general information
archipelago.slot_name = "{{ slot_name }}" -- actual name: "factorio1" will not Alias.
archipelago.slot_id = {{ slot_player }} -- int for which player this slot belongs to.
archipelago.mod_name = "{{ mod_name }}" -- exact name of this mod. "AP-91831735932242911797-P1-factorio1_0.6.6.zip"
archipelago.goal = {{ goal }} -- 0 = rocket and 1 == satelite
archipelago.silo = {{ silo }} -- 0 = normal silo, 1 = random recipe, 2 = spawned at the start of the game.


-- mod setting names
archipelago.mod_setting_names = {}
archipelago.mod_setting_names.death_link = "archipelago-death-link-{{ slot_player }}-{{ seed_name }}"
archipelago.mod_setting_names.energy_link = "archipelago-energy-link-{{ slot_player }}-{{ seed_name }}"

-- energy_link
archipelago.energy_link = {}
archipelago.energy_link.efficiency = 0.75
archipelago.energy_link.mod_setting = archipelago.mod_setting_names.energy_link -- yes, I duplicated this. But just seemed logical to have in two spots.

-- science_packs
archipelago.science_packs = {}
archipelago.science_packs.ordered = {{ variable_to_lua(ordered_science_packs) }}

-- free samples
archipelago.free_samples = {}
archipelago.free_samples.quality = "{{ free_sample_quality_name }}"

archipelago.free_samples.get_black_list = function ()--returns a big list of all items. false / nil is whitelist and true is blacklisted.
    return {{ variable_to_lua(free_sample_blacklist) }}
end


--technologies
archipelago.technologies = {}
archipelago.technologies.hide_from_player = function () -- returns a list of all the technologies to disable research of and hide.
    return {
    {%- for original_tech_name in base_tech_table -%}
        "{{ original_tech_name }}",
    {% endfor %}
    }
end
archipelago.technologies.locations = function () -- returns a list of all the technologies that AP adds in the game.
    return {
        {%- for location, item in locations %}
        {#- the tech researched by the local player #}
        ["ap-{{ location.address }}-"] = {
            location = {{ location.address }}, --ap location
            name = "ap-{{ location.address }}-", --factorio name
            location_name = "{{location.name}}", --ap name for the location.
            unit = {
                count = {{ location.count }},
                ingredients = {{ variable_to_lua(location.factorio_ingredients) }},
            },
            information = {
                {%- if (location.revealed) -%}
                revealed = true, --if the tech is known.
                --type is 1 of the five types. might be used for making the icons and/or description. "advancement", "useful", "trap", "filler", "unknown"
                type = {% if item.advancement %}"advancement"{% elif item.useful %}"useful"{% elif item.trap %}"trap"{% else %}"filler"{% endif %},
                item_name = "{{ item.name }}", --ap name for the item.
                player_name = "{{ player_names[item.player] }}", --ap name for player who owns the item.
                {%- else  %}
                revealed = false,
                type = {% if item.advancement and tech_tree_information == 1 %}"advancement"{% elif tech_tree_information == 1 %}"filler"{% else %}"unknown"{% endif %},
                {% endif %}
            },
            prerequisites = {
                {%- if location in tech_tree_layout_prerequisites %}
                {{ variable_to_lua(tech_tree_layout_prerequisites[location]) }}
                {% endif -%}

            },
        },
        {% endfor %}
    }
end
archipelago.technologies.progressive = function ()
    return {{ variable_to_lua(progressive_technology_table) }}
end

--recipes
archipelago.recipes = {}
{% if recipe_time_scale %}
archipelago.recipes.type = "scale" --scale means that is gets x lower to y higher.
{% elif recipe_time_range %}
archipelago.recipes.type = "range" --means new values from x to y.
{% endif %}
archipelago.recipes.time_adjustments = function ()
    return {
        {% if recipe_time_scale %}
        {%- for recipe_name, recipe in recipes.items() %}
        {%- if recipe.category not in ("basic-solid", "basic-fluid", "water") %}
        ["{{ recipe_name }}"] = {{ flop_random(*recipe_time_scale) }}
        {%- endif %}
        {%- endfor -%}
        {% elif recipe_time_range %}
        {%- for recipe_name, recipe in recipes.items() %}
        {%- if recipe.category not in ("basic-solid", "basic-fluid", "water") %}
        ["{{ recipe_name }}"] =  {{ flop_random(*recipe_time_range) }}
        {%- endif %}
        {%- endfor -%}
        {% endif %}
    }
end

archipelago.recipes.tool_tips = function ()
    return {
        {%- for recipe_name, recipe in recipes.items() %}
        ["{{recipe_name}}"] = {
            name = "{{recipe_name}}",
            catergories = {
            {%- for techCat in recipe.technologies %}
                 "{{techCat.tech.name}}",
            {%- endfor %}
            }
        },
        {%- endfor %}
    }
end
archipelago.recipes.custom_recipes = function ()
    return {
        {%- for recipe_name, recipe in recipes.items() %}
        {%- if recipe.source.value == 2 %}
        ["{{recipe_name}}"] = {
            name = "{{recipe_name}}",
            category = "{{recipe.category.name}}",
            energy = {{recipe.energy}},
            ingredients = {{dict_to_recipe(recipe.ingredients)}},
            products = {{dict_to_recipe(recipe.products)}},
            productivity = {{recipe.productivity}},
        },
        {%- endif %}
        {%- endfor %}
        {%- for recipe_name, recipe in custom_recipes.items() %}
        {# todo add check for non-standard recipe categories #}
        ["{{recipe_name}}"] = {
            name = "{{recipe_name}}",
            category = "{{recipe.category.name}}",
            energy = {{recipe.energy}},
            ingredients = {{dict_to_recipe(recipe.ingredients)}},
            products = {{dict_to_recipe(recipe.products)}},
            productivity = {{recipe.productivity}},
        },
        {%- endfor %}
    }
end
archipelago.recipes.enable_productivity = function ()
    return {
    {%- for recipe_name, recipe in recipes.items() %}
    {%- if (recipe.source.value != 2 and recipe.productivity != None) %}
        "{{recipe_name}}",
    {%- endif %}
    {%- endfor %}
    }
end

return archipelago