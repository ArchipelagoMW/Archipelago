{% from "macros.lua" import dict_to_recipe, dict_to_lua, variable_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template

local general = {}


--general information
general.slot_name = "{{ slot_name }}" -- actual name: "factorio1" will not Alias.
general.slot_id = {{ slot_player }} -- int for which player this slot belongs to.
general.mod_name = "{{ mod_name }}" -- exact name of this mod. "AP-91831735932242911797-P1-factorio1_0.6.6.zip"
general.goal = {{ goal }} -- 0 = rocket and 1 == satelite
general.silo = {{ silo }} -- 0 = normal silo, 1 = random recipe, 2 = spawned at the start of the game.


-- mod setting names
general.mod_setting_names = {}
general.mod_setting_names.death_link = "archipelago-death-link-{{ slot_player }}-{{ seed_name }}"
general.mod_setting_names.energy_link = "archipelago-energy-link-{{ slot_player }}-{{ seed_name }}"

-- energy_link
general.energy_link = {}
general.energy_link.efficiency = 0.75
general.energy_link.mod_setting = general.mod_setting_names.energy_link -- yes, I duplicated this. But just seemed logical to have in two spots.
general.energy_link.enabled = {% if energy_link %}true{% else %}false{% endif %}

-- science_packs
general.science_packs = {}
general.science_packs.ordered = {{ variable_to_lua(ordered_science_packs) }}
general.science_packs.allowed = {{ variable_to_lua(allowed_science_packs) }}

-- free samples
general.free_samples = {}
general.free_samples.quality = "{{ free_sample_quality_name }}"

general.free_samples.get_black_list = function ()--returns a big list of all items. false / nil is whitelist and true is blacklisted.
    return {{ variable_to_lua(free_sample_blacklist) }}
end


--technologies
general.technologies = {}
general.technologies.hide_from_player = function () -- returns a list of all the technologies to disable research of and hide.
    --has an test in data-final-fixes that will throw out the name of the place it is erroring at.
    return {
    {%- for original_tech_name in base_tech_table -%}
        "{{ original_tech_name }}",
    {% endfor %}
    }
end
general.technologies.progressive = function ()
    --has an test in final-fixes that will throw out the name of the place it is erroring at.
    return {{ variable_to_lua(progressive_technology_table) }}
end

--recipes
general.recipes = {}
{% if recipe_time_scale %}
general.recipes.type = "scale" --scale means that is gets x lower to y higher.
{% elif recipe_time_range %}
general.recipes.type = "range" --means new values from x to y.
{% endif %}
general.recipes.time_adjustments = function ()
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

general.recipes.tool_tips = function ()
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

general.recipes.custom_recipes = function ()
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
general.recipes.enable_productivity = function ()
    return {
    {%- for recipe_name, recipe in recipes.items() %}
    {%- if (recipe.source.value != 2 and recipe.productivity != None) %}
        "{{recipe_name}}",
    {%- endif %}
    {%- endfor %}
    }
end

--map generation
general.map_preset = {{ dict_to_lua({"default": False, "order": "a", "basic_settings": world_gen_settings["basic"], "advanced_settings": world_gen_settings["advanced"]}) }}

return general