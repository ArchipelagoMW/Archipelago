{% from "macros.lua" import dict_to_lua %}

local constants = {}

constants.FREE_SAMPLES = {{ free_samples }}
constants.SLOT_NAME = "{{ slot_name }}"
constants.SEED_NAME = "{{ seed_name }}"
constants.FREE_SAMPLE_BLACKLIST = {{ dict_to_lua(free_sample_blacklist) }}
constants.TRAP_EVO_FACTOR = {{ evolution_trap_increase }} / 100
constants.MAX_SCIENCE_PACK = {{ max_science_pack }}
constants.GOAL = {{ goal }}
constants.goal_science_pack = "space-science-pack"
constants.ENERGY_INCREMENT = {{ energy_link * 10000000 }}
constants.ENERGY_LINK_EFFICIENCY = 0.75

constants.hint_tech_list = {{dict_to_lua(techs_to_hint)}}

constants.setting_names = {}
constants.setting_names.death_link = "archipelago-death-link-{{ slot_player }}-{{ seed_name }}"
constants.setting_names.layer_obscurity = "archipelago-tech-layer-obscurity-{{ slot_player }}-{{ seed_name }}"
constants.setting_names.depth_obscurity = "archipelago-tech-depth-obscurity-{{ slot_player }}-{{ seed_name }}"
constants.setting_names.craft_obscurity = "archipelago-tech-craft-obscurity-{{ slot_player }}-{{ seed_name }}"

constants.science_packs = {
    "automation-science-pack",
    "logistic-science-pack",
    "military-science-pack",
    "chemical-science-pack",
    "production-science-pack",
    "utility-science-pack",
    "space-science-pack",
}

if constants.GOAL == 1 then
    local is_in = false
    for _, pack in pairs(constants.science_packs) do
        if constants.goal_science_pack == pack then
            is_in = true
        end
    end
    if is_in == false then
        error("victory condition is crafting a science pack ("..constants.goal_science_pack.."), but it was not found in the list of science packs.")
    end
end

return constants

