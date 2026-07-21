
local general = require("Archipelago/general")
local library = require("libs/lib")

if settings.global[general.mod_setting_names.death_link].value then
    DEATH_LINK = 1
else
    DEATH_LINK = 0
end

local death_lock = 0

local function on_runtime_mod_setting_changed(event)
    if event.setting == general.mod_setting_names.death_link then
        if settings.global[general.mod_setting_names.death_link].value then
            DEATH_LINK = 1
        else
            DEATH_LINK = 0
        end
        library.dump_info()
    end
end


local function kill_players(force)
    death_lock = 1
    local current_character = nil
    for _, player in ipairs(force.players) do
        current_character = player.character
        if current_character ~= nil then
            current_character.die()
        end
    end
    death_lock = 0
end

local function on_player_died(event)
    if DEATH_LINK == 0 then
        return
    end
    if death_lock == 1 then -- don't re-trigger on same event
        return
    end
    local player = game.get_player(event.player_index)
    local force = player.force
    storage.forcedata[force.name].death_link_tick = game.tick
    library.dump_info()
    kill_players(force)
end

local function on_force_created(event)
    local force = event.force
    storage.forcedata[force.name] = storage.forcedata[force.name] or {}
    storage.forcedata[force.name]["death_link_tick"] = storage.forcedata[force.name]["death_link_tick"] or 0
end

local function on_init()
    storage.forcedata = storage.forcedata or {} --ensure this list exists.

    -- Fire dummy events for all currently existing forces.
    for name, force in pairs(game.forces) do
        on_force_created({force = force})
    end
end

commands.add_command("ap-deathlink", "Kill all players", function(call)
    local force = game.forces["player"]
    local source = call.parameter or "Archipelago"
    kill_players(force)
    game.print({"archipelago.death-link",source})
end)

local lib = {}
lib.events = {
    [defines.events.on_runtime_mod_setting_changed] = on_runtime_mod_setting_changed,
    [defines.events.on_force_created] = on_force_created,
    --[defines.events.on_force_reset] = on_force_created, --currently unneeded.
    [defines.events.on_player_created] = on_player_created,
    [defines.events.on_player_died] = on_player_died, --replaced with the one below.
}
lib.filtered_events = {
    --[defines.events.on_entity_died] = {on_entity_died, {LuaEntityDiedEventFilter = {["filter"] = "name", ["name"] = "character"}} --replaced with the one below.
}
--lib.on_entity_died = {type = "character"} --a list of all names that need to be filtered for the on_entity_died event changed to on_player_died
--lib.on_entity_died_function = on_entity_died --a list of all names that need to be filtered for the on_entity_died event

lib.on_init = on_init
--lib.on_configuration_changed = on_configuration_changed

return lib