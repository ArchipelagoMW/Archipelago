-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
local technologies = data.raw["technology"]
local original_tech
local new_tree_copy
allowed_ingredients = {}
{%- for ingredient in allowed_science_packs %}
allowed_ingredients["{{ingredient}}"]= 1
{% endfor %}
local template_tech = table.deepcopy(technologies["automation"])
{#-  ensure the copy unlocks nothing #}
template_tech.unlocks = {}
template_tech.upgrade = false
template_tech.effects = {}
template_tech.prerequisites = {}

function filter_ingredients(ingredients)
    local new_ingredient_list = {}
    for _, ingredient_table in pairs(ingredients) do
        if allowed_ingredients[ingredient_table[1]] then -- name of ingredient_table
            table.insert(new_ingredient_list, ingredient_table)
        end
    end

    return new_ingredient_list
end

function prep_copy(new_copy, old_tech)
    old_tech.enabled = false
    new_copy.unit = table.deepcopy(old_tech.unit)
    new_copy.unit.ingredients = filter_ingredients(new_copy.unit.ingredients)
    local new_effects = {}
    log(serpent.block(old_tech.effects))
    if old_tech.effects then
        for _, effect in pairs(old_tech.effects) do
            if effect.type == "unlock-recipe" then
                local recipe = data.raw["recipe"][effect.recipe]
                local results
                if recipe.normal then
                    if recipe.normal.result then
                        results = { {type = "item", amount= recipe.normal.result_count, name=recipe.normal.result} }
                    else
                        results = recipe.normal.results
                    end
                elseif recipe.result then
                    results = { {type = "item", amount= recipe.result_count, name=recipe.result} }
                else
                    results = recipe.results
                end
                for _, result in pairs(results) do
                    if result.type == "item" then
                        local new = {type="give-item", count=result.amount, item=result.name}
                        table.insert(new_effects, new)
                    end
                end
            end
        end
    end
    for _, effect in pairs(new_effects) do
        table.insert(old_tech.effects, effect)
    end
end


{# each randomized tech gets set to be invisible, with new nodes added that trigger those #}
{%- for original_tech_name, item_name, receiving_player in locations %}
original_tech = technologies["{{original_tech_name}}"]
{#- the tech researched by the local player #}
new_tree_copy = table.deepcopy(template_tech)
new_tree_copy.name = "ap-{{ tech_table[original_tech_name] }}-"{# use AP ID #}
prep_copy(new_tree_copy, original_tech)
{% if tech_cost != 1 %}
if new_tree_copy.unit.count then
    new_tree_copy.unit.count = math.max(1, math.floor(new_tree_copy.unit.count * {{ tech_cost }}))
end
{% endif %}
{% if item_name in tech_table %}
{#- copy Factorio Technology Icon #}
new_tree_copy.icon = table.deepcopy(technologies["{{ item_name }}"].icon)
new_tree_copy.icons = table.deepcopy(technologies["{{ item_name }}"].icons)
new_tree_copy.icon_size = table.deepcopy(technologies["{{ item_name }}"].icon_size)
{% else %}
{#- use default AP icon if no Factorio graphics exist #}
new_tree_copy.icon = "__{{ mod_name }}__/graphics/icons/ap.png"
new_tree_copy.icons = nil
new_tree_copy.icon_size = 512
{% endif %}
{#- add new technology to game #}
data:extend{new_tree_copy}

{% endfor %}