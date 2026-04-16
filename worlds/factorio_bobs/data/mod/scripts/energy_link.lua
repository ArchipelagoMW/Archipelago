
local general = require("Archipelago/general")
local library = require("libs/lib")

if settings.global[general.mod_setting_names.energy_link].value then
    ENERGY_INCREMENT = 10000000
else
    ENERGY_INCREMENT = 0
end

local function on_runtime_mod_setting_changed(event)
    if event.setting == general.mod_setting_names.energy_link then

        if settings.global[general.mod_setting_names.energy_link].value then
            ENERGY_INCREMENT = 10000000
            for _, force in pairs(general.player_forces) do
                if game.forces[force] then
                    game.forces[force].recipes["ap-energy-bridge"].enabled = true
                end
            end
        else
            ENERGY_INCREMENT = 0
            for _, force in pairs(general.player_forces) do
                if game.forces[force] then
                    game.forces[force].recipes["ap-energy-bridge"].enabled = false
                end
            end
        end
        library.dump_info()
    end
end

local function validate_energy_link_bridge(unit_number, entity)
    if not entity then
        if storage.energy_link_bridges[unit_number] == nil then return false end
        storage.energy_link_bridges[unit_number] = nil
        return false
    end
    if not entity.valid then
        if storage.energy_link_bridges[unit_number] == nil then return false end
        storage.energy_link_bridges[unit_number] = nil
        return false
    end
    return true
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

local function on_check_energy_link(event)
    --- assuming 1 MJ increment and 5MJ battery:
    --- first 2 MJ request fill, last 2 MJ push energy, middle 1 MJ does nothing
    if event.tick % 60 == 30 and ENERGY_INCREMENT then
        local force = "player"
        local bridges = storage.energy_link_bridges
        local bridgecount = count_energy_bridges()
        storage.forcedata[force].energy_bridges = bridgecount
        if storage.forcedata[force].energy == nil then
            storage.forcedata[force].energy = 0
        end
        if storage.forcedata[force].energy < ENERGY_INCREMENT * bridgecount * 5 then
            for i, bridge in pairs(bridges) do
                if validate_energy_link_bridge(i, bridge) then
                    local energy_increment = get_energy_increment(bridge)
                    if bridge.energy > energy_increment*3 then
                        storage.forcedata[force].energy = storage.forcedata[force].energy + (energy_increment * general.energy_link.efficiency)
                        bridge.energy = bridge.energy - energy_increment
                    end
                end
            end
        end
        for i, bridge in pairs(bridges) do
            if validate_energy_link_bridge(i, bridge) then
                local energy_increment = get_energy_increment(bridge)
                if storage.forcedata[force].energy < energy_increment and bridge.quality.level == 0 then
                    break
                end
                if bridge.energy < energy_increment*2 and storage.forcedata[force].energy > energy_increment then
                    storage.forcedata[force].energy = storage.forcedata[force].energy - energy_increment
                    bridge.energy = bridge.energy + energy_increment
                end
            end
        end
    end
end

local function on_energy_bridge_constructed(entity)
    if entity and entity.valid then
        if library.string_starts_with(entity.prototype.name, "ap-energy-bridge") then
            storage.energy_link_bridges[entity.unit_number] = entity
        end
    end
end

local function on_energy_bridge_removed(entity)
    if library.string_starts_with(entity.prototype.name, "ap-energy-bridge") then
        if storage.energy_link_bridges[entity.unit_number] == nil then return end
        storage.energy_link_bridges[entity.unit_number] = nil
    end
end

local function on_player_created(event)
    local player = game.players[event.player_index]
    -- FIXME: This (probably) fires before any other mod has a chance to change the player's force
    -- For now, they will (probably) always be on the 'player' force when this event fires.
    if settings.global[general.mod_setting_names.energy_link].value then
        player.force.recipes["ap-energy-bridge"].enabled=true
    else
        player.force.recipes["ap-energy-bridge"].enabled=false
    end
end

local function on_force_created(event)
    local force = event.force
    storage.forcedata[force.name] = storage.forcedata[force.name] or {}
    storage.forcedata[force.name]["energy"] = storage.forcedata[force.name]["energy"] or 0
    storage.forcedata[force.name]["energy_bridges"] = storage.forcedata[force.name]["energy_bridges"] or 0
    if settings.global[general.mod_setting_names.energy_link].value then
        force.recipes["ap-energy-bridge"].enabled=true
    else
        force.recipes["ap-energy-bridge"].enabled=false
    end
end

local function on_entity_cloned(event)
    on_energy_bridge_constructed(event.destination)
end

local function on_built_entity(event)
    on_energy_bridge_constructed(event.entity)
end

local function on_entity_died(event)
    on_energy_bridge_removed(event.entity)
end

local function on_init()
    storage.forcedata = storage.forcedata or {} --ensure this list exists.
    storage.energy_link_bridges = storage.energy_link_bridges or {}
    -- Fire dummy events for all currently existing forces.
    for name, force in pairs(game.forces) do
        on_force_created({force = force})
    end

    --This feels redundent. all that happens within this function also happens within on_force_created.
    --for index, _ in pairs(game.players) do
    --    e.player_index = index
    --    on_player_created(e)
    --end
end

commands.add_command("ap-energylink", "Used by the Archipelago client to manage Energy Link", function(call)
    local change = tonumber(call.parameter or "0")
    local force = "player"
    storage.forcedata[force].energy = storage.forcedata[force].energy + change
end)

commands.add_command("energy-link", "Print the status of the Archipelago energy link.", function(call)
    log("Player command energy-link") -- notifies client
end)

local lib = {}
lib.events = {
    [defines.events.on_runtime_mod_setting_changed] = on_runtime_mod_setting_changed,
    [defines.events.on_tick] = on_check_energy_link,
    [defines.events.on_force_created] = on_force_created,
    --[defines.events.on_force_reset] = on_force_created, --currently unneeded.
    --[defines.events.on_forces_merging] = on_forces_merging, --currently unneeded.

    --[defines.events.on_player_created] = on_player_created, --the only thing that happens within this function also happens in on_force_created.

    [defines.events.on_built_entity] = on_built_entity,
    [defines.events.on_robot_built_entity] = on_built_entity,
    [defines.events.on_entity_cloned] = on_entity_cloned,

    [defines.events.script_raised_revive] = on_built_entity,
    [defines.events.script_raised_built] = on_built_entity,

    --[defines.events.on_entity_died] = on_entity_died, --is filtered down below.
    [defines.events.on_player_mined_entity] = on_entity_died,
    [defines.events.on_robot_mined_entity] = on_entity_died,
}
lib.filtered_events = {
    [defines.events.on_entity_died] = {on_entity_died, {LuaEntityDiedEventFilter = {["filter"] = "name", ["name"] = "ap-energy-bridge"}} } --replaced with the one below.
}

lib.on_init = on_init
--lib.on_configuration_changed = on_configuration_changed

return lib