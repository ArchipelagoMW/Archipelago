
local general = require("Archipelago/general")


-- TODO: Replace the tinting code with an actual rendered picture of the energy bridge icon.
-- This tint is so that one is less likely to accidentally mass-produce energy-bridges, then wonder why their rocket is not building.
function energy_bridge_tint()
    return { r = 0, g = 1, b = 0.667, a = 1}
end
function tint_icon(obj, tint)
    obj.icons = { {icon = obj.icon, icon_size = obj.icon_size, icon_mipmaps = obj.icon_mipmaps, tint = tint} }
    obj.icon = nil
    obj.icon_size = nil
    obj.icon_mipmaps = nil
end
local energy_bridge = table.deepcopy(data.raw["accumulator"]["accumulator"])
energy_bridge.name = "ap-energy-bridge"
energy_bridge.minable.result = "ap-energy-bridge"
energy_bridge.localised_name = "Archipelago EnergyLink Bridge"
energy_bridge.energy_source.buffer_capacity = "50MJ"
energy_bridge.energy_source.input_flow_limit = "10MW"
energy_bridge.energy_source.output_flow_limit = "10MW"
tint_icon(energy_bridge, energy_bridge_tint())
energy_bridge.chargable_graphics.picture.layers[1].tint = energy_bridge_tint()
energy_bridge.chargable_graphics.charge_animation.layers[1].layers[1].tint = energy_bridge_tint()
energy_bridge.chargable_graphics.discharge_animation.layers[1].layers[1].tint = energy_bridge_tint()
data.raw["accumulator"]["ap-energy-bridge"] = energy_bridge

local energy_bridge_item = table.deepcopy(data.raw["item"]["accumulator"])
energy_bridge_item.name = "ap-energy-bridge"
energy_bridge_item.place_result = energy_bridge.name
tint_icon(energy_bridge_item, energy_bridge_tint())
data.raw["item"]["ap-energy-bridge"] = energy_bridge_item

local energy_bridge_recipe = table.deepcopy(data.raw["recipe"]["accumulator"])
energy_bridge_recipe.name = "ap-energy-bridge"
energy_bridge_recipe.results = { {type = "item", name = energy_bridge_item.name, amount = 1} }
energy_bridge_recipe.energy_required = 1
energy_bridge_recipe.enabled = general.energy_link.enabled --might need change to the setting of energyLink? So that it can be made if the setting is turned on.
data.raw["recipe"]["ap-energy-bridge"] = energy_bridge_recipe

data.raw["map-gen-presets"].default["archipelago"] = general.map_preset

local function create_trigger_science_pack(pack)
    local pack_item = data.raw.tool[pack]
    if pack_item == nil then
        pack_item = data.raw.item[pack]
    end
    local pack_localised_name = pack_item.localised_name or {"item-name."..pack_item.name} or pack
    local pack_trigger = {
        type           = "technology",
        name           = "achipellago-trigger-"..pack,
        localised_name = {"technology-name.crafted-science-pack", pack_localised_name},
        icon           = pack_item.icon,
        icons          = pack_item.icons,
        icon_size      = pack_item.icon_size,
        hidden         = true,
        research_trigger = {
            type = "craft-item",
            item = pack,
        },
    }
    data:extend{pack_trigger}
end

for _, pack in pairs(general.science_packs.ordered) do
    create_trigger_science_pack(pack)
end

if mods["science-not-invited"] then
    --this should make these mods still compatiable.
    local weights = {}
    for _, name in pairs(general.science_packs.ordered) do
        weights[name] = 0
    end
    for _, name in pairs(general.science_packs.allowed) do
        weights[name] = 1
    end
    SNI.setWeights(weights)
end



data:extend({{
        type           = "technology",
        name           = "crash-prevention",
        icon           = "__base__/graphics/icons/small-scorchmark.png",
        icon_size      = 64,
        research_trigger = {
            type = "scripted",
        },
        prerequisites = {"crash-prevention-lock"}
    },
    {
        type           = "technology",
        name           = "crash-prevention-lock",
        hidden         = true,
        icon           = "__base__/graphics/icons/small-scorchmark.png",
        icon_size      = 64,
        research_trigger = {
            type = "scripted",
        },
    },
})
