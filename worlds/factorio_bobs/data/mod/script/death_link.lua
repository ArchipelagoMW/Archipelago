
local general = require("Archipelago.general")
local library = require("libs/lib")

local death_link_setting = settings.global[general.mod_setting_names.death_link]
if settings.global[general.mod_setting_names.death_link].value then
    DEATH_LINK = 1
else
    DEATH_LINK = 0
end

local death_lock = 0

local function on_runtime_mod_setting_changed(event)
    if event.setting == death_link_setting.name then
        local force
        if event.player_index == nil then
            force = game.forces.player
        else
            force = game.players[event.player_index].force
        end
        if death_link_setting.value then
            DEATH_LINK = 1
        else
            DEATH_LINK = 0
        end
        if force ~= nil then
            library.dumpInfo()
        end
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

local function on_entity_died(event)
    if DEATH_LINK == 0 then
        return
    end
    if death_lock == 1 then -- don't re-trigger on same event
        return
    end

    local force = event.entity.force
    storage.forcedata[force.name].death_link_tick = game.tick
    dumpInfo(force)
    kill_players(force)
end

local function on_force_created(event)
    local force = event.force
    local data = {}
    data["death_link_tick"] = 0
    storage.forcedata[force.name] = data
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
    game.print("Death was granted by " .. source)
end)

local lib = {}
lib.events = {
    [defines.events.on_runtime_mod_setting_changed] = on_runtime_mod_setting_changed,
    --[defines.events.on_research_finished] = on_research_finished,
    [defines.events.on_force_created] = on_force_created,
    [defines.events.on_player_created] = on_player_created,
}
lib.filtered_events{
    [defines.events.on_entity_died] = {on_entity_died, {LuaEntityDiedEventFilter = {["filter"] = "name", ["name"] = "character"}} }
}
lib.on_init = on_init

return lib