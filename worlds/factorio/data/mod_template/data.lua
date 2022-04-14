{% from "macros.lua" import dict_to_lua %}
local energy_bridge = table.deepcopy(data.raw["accumulator"]["accumulator"])
energy_bridge.name = "ap-energy-bridge"
energy_bridge.minable.result = "ap-energy-bridge"
energy_bridge.localised_name = "Archipelago EnergyLink Bridge"
energy_bridge.energy_source.buffer_capacity = "5MJ"
energy_bridge.energy_source.input_flow_limit = "1MW"
energy_bridge.energy_source.output_flow_limit = "1MW"
data.raw["accumulator"]["ap-energy-bridge"] = energy_bridge

local energy_bridge_item = table.deepcopy(data.raw["item"]["accumulator"])
energy_bridge_item.name = "ap-energy-bridge"
energy_bridge_item.localised_name = "Archipelago EnergyLink Bridge"
energy_bridge_item.place_result = energy_bridge.name
data.raw["item"]["ap-energy-bridge"] = energy_bridge_item

local energy_bridge_recipe = table.deepcopy(data.raw["recipe"]["accumulator"])
energy_bridge_recipe.name = "ap-energy-bridge"
energy_bridge_recipe.result = energy_bridge_item.name
energy_bridge_recipe.energy_required = 1
energy_bridge_recipe.enabled = {{ energy_link }}
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
