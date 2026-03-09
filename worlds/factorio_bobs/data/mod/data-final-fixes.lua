
local archipelago = require("Archipelago")
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

if archipelago.silo == 2 then
    data.raw["recipe"]["rocket-silo"].enabled = true
    technologies["rocket-silo"].enabled = false
    technologies["rocket-silo"].visible_when_disabled = false
end

data.raw["ammo"]["artillery-shell"].stack_size = 10

-- I am thinking that we might need to replace this entire function with one that will do all of this for ALL assembling machines that get made in any step of the process.
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

-- add all science packs to all labs
for lab in pairs(data.raw["lab"]) do
    data.raw["lab"][lab].inputs = archipelago.science_packs.ordered
end

function add_normal_custom_recipe(name, category, energy, ingredients, products, productivity)
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

function add_custom_tooltip_field(item, localised_name, localised_string, show_in_tooltip, order)
    if item.custom_tooltip_fields == nil then
        item.custom_tooltip_fields = { {
            name = localised_name,
            value = localised_string,
            show_in_tooltip = show_in_tooltip,
            order = order,
        } }
    else
        table.insert(item.custom_tooltip_fields, {
            name = localised_name,
            value = localised_string,
            show_in_tooltip = show_in_tooltip,
            order = order,
        })
    end
end

for name, info in pairs(archipelago.recipes.custom_recipes()) do
    --could even be changed to the function taking all the entire dict and working from there.
    add_normal_custom_recipe(info.name, info.category, info.energy, info.ingredients, info.products, info.productivity)
end

for _, name in pairs(archipelago.recipes.enable_productivity()) do
    data.raw["recipe"][name].allow_productivity = true
end


for name, info in pairs(archipelago.recipes.tool_tips()) do
    if data.raw["recipe"][name] then
        for _, category in pairs(info.catergories) do
            add_custom_tooltip_field(data.raw["recipe"][name], {"","recipe_unlock"}, {"",category}, false, 200)
        end
    end
end

-- Beserker note: This got complex, but seems to be required to hit all corner cases
local function adjust_energy(recipe_name, factor)
    local recipe = data.raw.recipe[recipe_name]
    if recipe == nil then return end

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

local function set_energy(recipe_name, energy)
    local recipe = data.raw.recipe[recipe_name]
    if recipe == nil then return end

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

if archipelago.recipes.type == "scale" then
    for name, adjustment in pairs(archipelago.recipes.time_adjustments()) do
        adjust_energy(name, adjustment)
    end
end
if archipelago.recipes.type == "range" then
    for name, adjustment in pairs(archipelago.recipes.time_adjustments()) do
        set_energy(name, adjustment)
    end
end

local technologies = data.raw["technology"]

local template_tech = { --making one from scratch, ensure that absolutely nothing can go wrong.
    type = "technology",
    --name = "this-is-required" --this should be getting overwritten at every AP location. if it does not this is a good as any error to notify us.
    --all other values either are default or are overwritten.
}

-- I will assume these functions need to be replaced by my multi icon functions later on.
local function set_ap_icon(tech)
    tech.icon = "__{{ mod_name }}__/graphics/icons/ap.png"
    tech.icons = nil
    tech.icon_size = 128
end

local function set_ap_unimportant_icon(tech)
    tech.icon = "__{{ mod_name }}__/graphics/icons/ap_unimportant.png"
    tech.icons = nil
    tech.icon_size = 128
end

local function copy_factorio_icon(tech, tech_sources)
    tech.icon = table.deepcopy(technologies[tech_sources[1]].icon)
    tech.icons = table.deepcopy(technologies[tech_sources[1]].icons)
    tech.icon_size = table.deepcopy(technologies[tech_sources[1]].icon_size)
end
-- end of the functions that will need to be replaced

for _, name in pairs(archipelago.technologies.hide_from_player()) do
    technologies[name].hidden = true
    technologies[name].hidden_in_factoriopedia = false
    technologies[name].unit = nil
    technologies[name].research_trigger = {type = "scripted", localised_description = {"technology-description.ap-technology-script-trigger"}}
end

archipelago.technologies.progressive = archipelago.technologies.progressive()

for name, info in pairs(archipelago.technologies.locations()) do
    local new_location = table.deepcopy(template_tech)
    new_location.name = info.name
    new_location.unit = info.unit
    new_location.unit.time = 10
    if info.information.revealed then
        new_location.localised_name = {"technology-name.ap-technology-full", info.information.player_name, info.information.item_name, info.location_name}
        if info.information.type == "filler" or info.information.type == "unknown" then
            new_location.localised_description  = {"technology-description.ap-technology-full",  {info.information.item_name}, {info.information.player_name}, ""}
        end
        new_location.localised_description  = {"technology-description.ap-technology-full",  {info.information.item_name}, {info.information.player_name}, {"technology-description.ap-technology-item-" .. info.information.type}}
        if archipelago.technologies.progressive[info.information.item_name] then
            copy_factorio_icon(new_location, archipelago.technologies.progressive[info.information.item_name])
        elseif technologies[info.information.item_name] then
            copy_factorio_icon(new_location, {info.information.item_name})
        elseif info.information.type == "advancement" then
            set_ap_icon(new_location)
        else
            set_ap_unimportant_icon(new_location)
        end
    else
        new_location.localised_name = {"technology-name.ap-technology-hidden", info.location_name}
        if info.information.type == "filler" or info.information.type == "unknown" then
            new_location.localised_description  = {"technology-description.ap-technology-hidden", ""}
        else
            new_location.localised_description  = {"technology-description.ap-technology-hidden", {"technology-description.ap-technology-item-" .. info.information.type}}
        end
        if info.information.type == "advancement" or info.information.type == "unknown" then
            set_ap_icon(new_location)
        else
            set_ap_unimportant_icon(new_location)
        end
    end
    new_location.prerequisites = info.prerequisites
    data:extend({new_location})
end


