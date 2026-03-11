
local general = require("Archipelago.general")
local library = require("libs/lib")

local energy_link_setting = settings.global[general.mod_setting_names.death_link]
if settings.global[general.mod_setting_names.death_link].value then
    ENERGY_INCREMENT = 10000000
else
    ENERGY_INCREMENT = 0
end

local function on_runtime_mod_setting_changed(event)
    if event.setting == ARCHIPELAGO_ENERGY_LINK_SETTING then
        local force
        if event.player_index == nil then
            force = game.forces.player
        else
            force = game.players[event.player_index].force
        end

        if settings.global[ARCHIPELAGO_ENERGY_LINK_SETTING].value then
            ENERGY_INCREMENT = 10000000
            force.recipes["ap-energy-bridge"].enabled=true
        else
            ENERGY_INCREMENT = 0
            force.recipes["ap-energy-bridge"].enabled=false
        end
        if force ~= nil then
            library.dumpInfo()
        end
    end
end

local function count_energy_bridges()
    local count = 0
    for i, bridge in pairs(storage.energy_link_bridges) do
        if validate_energy_link_bridge(i, bridge) then
            count = count + 1 + (bridge.quality.level * 0.3)
        end
    end
    return count
end

local function get_energy_increment(bridge)
    return ENERGY_INCREMENT + (ENERGY_INCREMENT * 0.3 * bridge.quality.level)
end

local lib = {}
lib.events = {
    [defines.events.on_runtime_mod_setting_changed] = on_runtime_mod_setting_changed,
    --[defines.events.on_research_finished] = on_research_finished,
    --[defines.events.on_force_created] = on_force_created,
    --[defines.events.on_surface_created] = on_surface_created,
}
--lib.on_init = on_init
--lib.on_configuration_changed = on_configuration_changed

return lib