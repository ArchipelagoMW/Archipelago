

local general = require("Archipelago/general")
local library = require("libs/lib")
local util = require("util")


TRAP_TABLE = {
["Attack Trap"] = function ()
        game.surfaces["nauvis"].build_enemy_base(game.forces["player"].get_spawn_position(game.get_surface(1)), 25)
    end,
["Evolution Trap"] = function ()
        local new_factor = game.forces["enemy"].get_evolution_factor("nauvis") +
            (general.traps.evo_increase * (1 - game.forces["enemy"].get_evolution_factor("nauvis")))
        game.forces["enemy"].set_evolution_factor(new_factor, "nauvis")
        game.print({"", "New evolution factor:", new_factor})
    end,
["Teleport Trap"] = function()
        for _, player in ipairs(game.forces["player"].players) do
            if player.character then
                library.attempt_teleport_player(player, 1)
            end
        end
    end,
["Grenade Trap"] = function ()
        library.fire_entity_at_players("grenade", 0.1)
    end,
["Cluster Grenade Trap"] = function ()
        library.fire_entity_at_players("cluster-grenade", 0.1)
    end,
["Artillery Trap"] = function ()
        library.fire_entity_at_players("artillery-projectile", 1)
    end,
["Atomic Rocket Trap"] = function ()
        library.fire_entity_at_players("atomic-rocket", 0.1)
    end,
["Atomic Cliff Remover Trap"] = function ()
        local cliffs = game.surfaces["nauvis"].find_entities_filtered{type = "cliff"}

        if #cliffs > 0 then
            library.fire_entity_at_entities("atomic-rocket", {cliffs[math.random(#cliffs)]}, 0.1)
        end
    end,
["Inventory Spill Trap"] = function ()
        for _, player in ipairs(game.forces["player"].players) do
            library.spill_character_inventory(player.character)
        end
    end,
}

general.technologies.progressive = general.technologies.progressive()
local function receive_item(item_name, source)
    for _, force in pairs(library.get_all_ap_forces()) do
        if general.technologies.progressive[item_name] ~= nil then
            local tech_stack = general.technologies.progressive[item_name]
                for _, item_name in ipairs(tech_stack) do
                    local tech = force.technologies[item_name]
                    if tech.researched ~= true then
                        force.print({"archipelago.receive-ap-item", "[technology=" .. tech.name .. "]", source})
                        force.play_sound({path="utility/research_completed"})
                        tech.researched = true
                        return
                    end
                end
        elseif force.technologies[item_name] ~= nil then
            for _, force in pairs(library.get_all_ap_forces()) do
                local tech = force.technologies[item_name]
                if tech.researched ~= true then --if not true, so it only tells you about new technologies.
                    force.print({"archipelago.receive-ap-item", "[technology=" .. tech.name .. "]", source})
                    force.play_sound({path="utility/research_completed"})
                    tech.researched = true
                end
            end
        elseif TRAP_TABLE[item_name] ~= nil then
            force.print({"archipelago.receive-ap-item", item_name, source})
            TRAP_TABLE[item_name]()
        else
            force.print("Unknown Item " .. item_name)
        end
    end
end

local function remote_unlock(item_name, index, source)
    if storage.index_sync[index] ~= item_name then -- not yet received prog item
        storage.index_sync[index] = item_name
        receive_item(item_name, source)
    end
end

local function local_unlock(item_name)
    receive_item(item_name, general.slot_name)
end

local function update_player(index)
    local player = game.players[index]
    if not player or not player.valid then     -- Do nothing if we reference an invalid player somehow
        return
    end
    local character = player.character or player.cutscene_character
    if not character or not character.valid then
        return
    end
    local data = storage.playerdata[index]
    local samples = data['pending_samples']
    local sent
    --player.print(serpent.block(data['pending_samples']))
    local stack = {}

    for name, count in pairs(samples) do
        stack.name = name
        stack.count = count
        if script.active_mods["quality"] then
            stack.quality = general.free_samples.quality
        end
        if prototypes.item[name] and prototypes.item[name].subgroup == "science-pack" then
            samples[name] = nil -- remove science-pack from the list
        elseif stack.count > 0 and prototypes.item[name] then
            if character.can_insert(stack) then
                sent = character.insert(stack)
            else
                sent = 0
            end
            if sent > 0 then
                player.print({"archipelago.recieve-sample-item", sent, "[item=" .. name .. ",quality="..general.free_samples.quality.."]"})
                data.suppress_full_inventory_message = false
            end
            if sent ~= count then               -- Couldn't full send.
                if not data.suppress_full_inventory_message then
                    player.print({"archipelago.sample-inventory-full"}, {r=1, g=1, b=0.25})
                end
                data.suppress_full_inventory_message = true -- Avoid spamming them with repeated full inventory messages.
                samples[name] = count - sent    -- Buffer the remaining items
                break                           -- Stop trying to send other things
            else
                samples[name] = nil             -- Remove from the list
            end
        elseif stack.count > 0 then
            player.print({"archipelago.sample-error", count, name})
            samples[name] = nil
        end
    end
end

local function add_samples(force, name, count)
    local function add_to_table(t)
        if count <= 0 then
            -- Fixes a bug with single craft, if a recipe gives 0 of a given item.
            return
        end
        t[name] = (t[name] or 0) + count
    end
    if prototypes.item[name] then
        count = math.min(count, prototypes.item[name].stack_size)
        -- check if been given before
        if storage.forcedata[force.name]['earned_samples'][name] ~= nil then
            count = count - storage.forcedata[force.name]['earned_samples'][name]
            if count <= 0 then
                return
            end
        end
        -- Add to storage table of earned samples for future new players
        add_to_table(storage.forcedata[force.name]['earned_samples'])
        -- Add to existing players
        for _, player in pairs(force.players) do
            add_to_table(storage.playerdata[player.index]['pending_samples'])
            update_player(player.index)
        end
    end
end

local function update_player_event(event)
    update_player(event.player_index)
end

local function on_player_created(event)
    local player = game.players[event.player_index]
    storage.playerdata[player.index] = storage.playerdata[player.index] or {}
    storage.playerdata[player.index]['pending_samples'] = util.table.deepcopy(storage.forcedata[player.force.name]['earned_samples'])
    update_player(player.index)  -- Attempt to send pending free samples, if relevant.
    library.dump_info()
end

local function on_player_removed(event)
    storage.playerdata[event.player_index] = nil
end

-- Initialize force data, either from it being created or already being part of the game when the mod was added.
local function on_force_created(event)
    local force = event.force
    storage.forcedata[force.name] = storage.forcedata[force.name] or {}
    storage.forcedata[force.name]["earned_samples"] = general.free_samples.get_starter_items()
end

-- hook into researches done
general.free_samples.get_black_list = general.free_samples.get_black_list()
general.technologies.local_items = general.technologies.local_items
local function on_research_finished(event)
    local technology = event.research
    if library.is_valid_ap_force(technology.force) == false then
        --Don't acknowledge any forces that are not signed up as an AP valid force.
        return
    end
    if technology.researched and string.find(technology.name, "ap%-") == 1 then
        -- check if it came from the server anyway, then we don't need to double send.
        library.dump_info() --is sendable
        local corrosponding_item = general.technologies.local_items()[technology.name]
        if corrosponding_item then
            local_unlock(corrosponding_item)
        end
    else
        if general.free_samples.state == 0 then
            return  -- Nothing else to do
        end
        if not technology.prototype.effects then
            return  -- No technology effects, so nothing to do.
        end
        for _, effect in pairs(technology.prototype.effects) do
            if effect.type == "unlock-recipe" then
                local recipe = prototypes.recipe[effect.recipe]
                for _, result in pairs(recipe.products) do
                    if result.type == "item" and result.amount then
                        local name = result.name
                        if general.free_samples.get_black_list[name] ~= true then
                            local count
                            if general.free_samples.state == 1 then
                                count = result.amount
                            else
                                count = library.get_any_stack_size(result.name)
                                if general.free_samples.state == 2 then
                                    count = math.ceil(count / 2)
                                end
                            end
                            add_samples(technology.force, name, count)
                        end
                    end
                end
            end
        end
    end
end


local function on_init()
    storage.playerdata = storage.playerdata or {}
    storage.forcedata = storage.forcedata or {}

    -- Fire dummy events for all currently existing forces.
    for name, force in pairs(game.forces) do
        on_force_created({force = force})
    end

    -- Fire dummy events for all currently existing players.
    for index, _ in pairs(game.players) do
        on_player_created({player_index = index})
    end
end



commands.add_command("ap-get-technology", "Grant a technology, used by the Archipelago Client.", function(call)
    if storage.index_sync == nil then
        storage.index_sync = {}
    end
    local tech
    local force = game.forces["player"]
    if call.parameter == nil then
        game.print("ap-get-technology is only to be used by the Archipelago Factorio Client")
        return
    end
    local chunks = library.split(call.parameter, "\t")
    local item_name = chunks[1]
    local index = chunks[2]
    local source = chunks[3] or "Archipelago"
    if index == nil then
        game.print("ap-get-technology is only to be used by the Archipelago Factorio Client")
        return
    elseif index == "-1" then -- for coop sync and restoring from an older savegame
        tech = force.technologies[item_name]
        if tech.researched ~= true then
            game.print({"archipelago.receive-ap-catchup", "[technology=" .. tech.name .. "]"})
            game.play_sound({path="utility/research_completed"})
            tech.researched = true
        end
        return
    else
        remote_unlock(item_name, index, source)
    end
end)

local lib = {}
lib.events = {
    --[defines.events.on_tick] = on_tick,
    [defines.events.on_research_finished] = on_research_finished,
    [defines.events.on_force_created] = on_force_created,
    [defines.events.on_player_created] = on_player_created,
    [defines.events.on_player_removed] = on_player_removed,

    [defines.events.on_player_joined_game] = update_player_event,
    [defines.events.on_player_main_inventory_changed] = update_player_event,
    [defines.events.on_cutscene_cancelled] = update_player_event,
    [defines.events.on_cutscene_finished] = update_player_event,

    --[defines.events.on_surface_created] = on_surface_created,
    --[defines.events.on_surface_created] = on_surface_created,
    --[defines.events.on_surface_created] = on_surface_created,


    [defines.events.on_script_path_request_finished] = library.handle_teleport_attempt
}
lib.on_init = on_init
--lib.on_configuration_changed = on_configuration_changed

return lib