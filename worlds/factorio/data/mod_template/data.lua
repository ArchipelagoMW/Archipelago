{% from "macros.lua" import dict_to_lua %}
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
energy_bridge_item.localised_name = "Archipelago EnergyLink Bridge"
energy_bridge_item.place_result = energy_bridge.name
tint_icon(energy_bridge_item, energy_bridge_tint())
data.raw["item"]["ap-energy-bridge"] = energy_bridge_item

local energy_bridge_recipe = table.deepcopy(data.raw["recipe"]["accumulator"])
energy_bridge_recipe.name = "ap-energy-bridge"
energy_bridge_recipe.results = { {type = "item", name = energy_bridge_item.name, amount = 1} }
energy_bridge_recipe.energy_required = 1
energy_bridge_recipe.enabled = {% if energy_link %}true{% else %}false{% endif %}
energy_bridge_recipe.localised_name = "Archipelago EnergyLink Bridge"
data.raw["recipe"]["ap-energy-bridge"] = energy_bridge_recipe

data.raw["map-gen-presets"].default["archipelago"] = {{ dict_to_lua({"default": False, "order": "a", "basic_settings": world_gen["basic"], "advanced_settings": world_gen["advanced"]}) }}
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
{% if max_science_pack == 6 -%}
    weights["space-science-pack"] = 1
{%- endif %}
{% for key in allowed_science_packs -%}
    weights["{{key}}"] = 1
{% endfor %}
    SNI.setWeights(weights)
end
