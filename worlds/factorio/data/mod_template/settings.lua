-- Find out if more than one AP mod is loaded, and if so, error out.

local constants = require("constants")

function mod_is_AP(str)
    -- lua string.match is way more restrictive than regex. Regex would be "^AP-W?\d{20}-P[1-9]\d*-.+$"
	local result = string.match(str, "^AP%-W?%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%d%-P[1-9]%d-%-.+$")
	if result ~= nil then
		log("Archipelago Mod: " .. result .. " is loaded.")
	end
	return result ~= nil
end
local ap_mod_count = 0
for name, _ in pairs(mods) do
    if mod_is_AP(name) then
        ap_mod_count = ap_mod_count + 1
        if ap_mod_count > 1 then
            error("More than one Archipelago Factorio mod is loaded.")
        end
    end
end
data:extend({
    {
        type = "bool-setting",
        name = constants.setting_names.death_link,
        setting_type = "runtime-global",
        {% if death_link %}
            default_value = true
        {% else %}
            default_value = false
        {% endif %}
    },
    {
        type = "bool-setting",
        name = constants.setting_names.layer_obscurity,
        localised_name = {"mod-setting-name.archipelago-tech-layer-obscurity"},
        localised_description = {"mod-setting-description.archipelago-tech-layer-obscurity"},
        setting_type = "runtime-global",
        {% if tech_layer_obscurity %}
            default_value = true
        {% else %}
            default_value = false
        {% endif %}
    },
    {
        type = "int-setting",
        name = constants.setting_names.depth_obscurity,
        localised_name = {"mod-setting-name.archipelago-tech-depth-obscurity"},
        localised_description = {"mod-setting-description.archipelago-tech-depth-obscurity"},
        setting_type = "runtime-global",
        minimum_value = 0,
        default_value = {{ tech_depth_obscurity }}
    },
    {
        type = "bool-setting",
        name = constants.setting_names.craft_obscurity,
        localised_name = {"mod-setting-name.archipelago-tech-craft-obscurity"},
        localised_description = {"mod-setting-description.archipelago-tech-craft-obscurity"},
        setting_type = "runtime-global",
        {% if tech_craft_obscurity %}
            default_value = true
        {% else %}
            default_value = false
        {% endif %}
    }
})
