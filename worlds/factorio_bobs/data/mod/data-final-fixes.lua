
local general = require("Archipelago/general")
require("Archipelago/locations")
require("Archipelago/custom_recipes")

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

if general.silo == 2 then
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
    data.raw["lab"][lab].inputs = general.science_packs.ordered
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

for _, name in pairs(general.recipes.enable_productivity()) do
    if data.raw["recipe"][name] == nil then
        error(name .." could not be found. This should be a recipe that is present at this point in the loading stage. This recipe is present in the list of recipes that get their productivity enabled.")
    end
    data.raw["recipe"][name].allow_productivity = true
end


for name, info in pairs(general.recipes.tool_tips()) do
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

if general.recipes.type == "scale" then
    for name, adjustment in pairs(general.recipes.time_adjustments()) do
        adjust_energy(name, adjustment)
    end
end
if general.recipes.type == "range" then
    for name, adjustment in pairs(general.recipes.time_adjustments()) do
        set_energy(name, adjustment)
    end
end

local technologies = data.raw["technology"]

for _, name in pairs(general.technologies.hide_from_player()) do
    if technologies[name] == nil then
        error(name .." could not be found. This should be a technology that is present at this point in the loading stage. This is present in the list of technologies that need to be hidden from the player, but not in the game.")
    end
    technologies[name].hidden = true
    technologies[name].hidden_in_factoriopedia = false
    technologies[name].unit = nil
    technologies[name].research_trigger = {type = "scripted", localised_description = {"technology-description.ap-technology-script-trigger"}}
end
