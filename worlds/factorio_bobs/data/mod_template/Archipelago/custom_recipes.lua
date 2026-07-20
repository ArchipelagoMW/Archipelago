{% from "macros.lua" import dict_to_recipe, dict_to_lua, variable_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Templates

local function add_normal_custom_recipe(name, category, energy, ingredients, products, productivity)
    if data.raw["recipe"][name] then
        recipe = data.raw["recipe"][name]
        recipe.category = category
        recipe.energy_required = energy
        recipe.ingredients = ingredients
        recipe.results = products
        if productivity then
            recipe.allow_productivity = productivity
        end
    else
        if productivity == nil then
            productivity = true -- enable productivity if new recipe and unspecified
        end
        data.raw["recipe"][name] = {
            type = "recipe",
            name = name,
            category = category,
            energy_required = energy,
            ingredients = ingredients,
            results = products,
            allow_productivity = productivity
        }
    end
end

{%- for recipe_name, recipe in recipes.items() %}
{%- if recipe.source.value == 2 %}
add_normal_custom_recipe(
    "{{recipe_name}}",
    "{{recipe.category.name}}",
    {{recipe.energy}},
    {{dict_to_recipe(recipe.ingredients)}},
    {{dict_to_recipe(recipe.products)}},
    {{variable_to_lua(recipe.productivity)}}
)
{%- endif %}
{%- endfor %}

{%- for recipe_name, recipe in custom_recipes.items() %}
add_normal_custom_recipe(
{# todo add check for non-standard recipe categories #}
    "{{recipe_name}}",
    "{{recipe.category.name}}",
    {{recipe.energy}},
    {{dict_to_recipe(recipe.ingredients)}},
    {{dict_to_recipe(recipe.products)}},
    {{variable_to_lua(recipe.productivity)}}
)
{%- endfor %}