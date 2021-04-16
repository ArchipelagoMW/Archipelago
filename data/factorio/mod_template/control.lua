require "lib"
require "util"

FREE_SAMPLES = {{ free_samples }}
--SUPPRESS_INVENTORY_EVENTS = false

-- Initialize force data, either from it being created or already being part of the game when the mod was added.
function on_force_created(event)
    game.forces[event.force].research_queue_enabled = true
    local data = {}
    if FREE_SAMPLES ~= 0 then
        data['earned_samples'] = {
            ["burner-mining-drill"] = 19,
            ["stone-furnace"] = 19
        }
    end
    global.forcedata[event.force] = data
end
script.on_event(defines.events.on_force_created, on_force_created)

-- Destroy force data.  This doesn't appear to be currently possible with the Factorio API, but here for completeness.
function on_force_destroyed(event)
    global.forcedata[event.force] = nil
end

-- Initialize player data, either from them joining the game or them already being part of the game when the mod was
-- added.`
function on_player_created(event)
    local player = game.players[event.player_index]
    -- FIXME: This (probably) fires before any other mod has a chance to change the player's force
    -- For now, they will (probably) always be on the 'player' force when this event fires.
    local data = {}
    if FREE_SAMPLES ~= 0 then
        data['pending_samples'] = table.deepcopy(global.forcedata[player.force.name]['earned_samples'])
    end
    global.playerdata[player.index] = data
    update_player(player.index)  -- Attempt to send pending free samples, if relevant.
end
script.on_event(defines.events.on_player_created, on_player_created)

function on_player_removed(event)
    global.playerdata[event.player_index] = nil
end
script.on_event(defines.events.on_player_removed, on_player_removed)

-- Updates a player, attempting to send them any pending samples (if relevant)
function update_player(index)
    if FREE_SAMPLES == 0 then  -- This is effectively a noop
        return
    end
    local player = game.players[index]
    if not player or not player.valid then     -- Do nothing if we reference an invalid player somehow
        return
    end
    local character = player.character or player.cutscene_character
    if not character or not character.valid then
        return
    end
    local data = global.playerdata[index]
    local samples = data['pending_samples']
    local sent
    --player.print(serpent.block(data['pending_samples']))
    local stack = {}
    --SUPPRESS_INVENTORY_EVENTS = true
    for name, count in pairs(samples) do
        stack.name = name
        stack.count = count
        if character.can_insert(stack) then
            sent = character.insert(stack)
        else
            sent = 0
        end
        if sent > 0 then
            player.print("Received " .. sent .. "x [item=" .. name .. "]")
            data.suppress_full_inventory_message = false
        end
        if sent ~= count then               -- Couldn't full send.
            if not data.suppress_full_inventory_message then
                player.print("Additional items will be sent when inventory space is available.", {r=1, g=1, b=0.25})
            end
            data.suppress_full_inventory_message = true -- Avoid spamming them with repeated full inventory messages.
            samples[name] = count - sent    -- Buffer the remaining items
            break                           -- Stop trying to send other things
        else
            samples[name] = nil             -- Remove from the list
        end
    end
    --SUPPRESS_INVENTORY_EVENTS = false
end

-- Update players upon them connecting, since updates while they're offline are suppressed.
script.on_event(defines.events.on_player_joined_game, function(event) update_player(event.player_index) end)

function update_player_event(event)
    --if not SUPPRESS_INVENTORY_EVENTS then
    update_player(event.player_index)
    --end
end

if FREE_SAMPLES then
    script.on_event(defines.events.on_player_main_inventory_changed, update_player_event)
end

function add_samples(force, name, count)
    local function add_to_table(t)
        t[name] = (t[name] or 0) + count
    end
    -- Add to global table of earned samples for future new players
    add_to_table(global.forcedata[force.name]['earned_samples'])
    -- Add to existing players
    for _, player in pairs(force.players) do
        add_to_table(global.playerdata[player.index]['pending_samples'])
        update_player(player.index)
    end
end

script.on_init(function()
    global.forcedata = {}
    global.playerdata = {}
    -- Fire dummy events for all currently existing forces.
    local e = {}
    for name, _ in pairs(game.forces) do
        e.force = name
        on_force_created(e)
    end
    e.force = nil

    -- Fire dummy events for all currently existing players.
    for index, _ in pairs(game.players) do
        e.player_index = index
        on_player_created(e)
    end
end)

-- for testing
script.on_event(defines.events.on_tick, function(event)
    if event.tick%600 == 0 then
        dumpTech(game.forces["player"])
    end
end)

-- hook into researches done
script.on_event(defines.events.on_research_finished, function(event)
    local technology = event.research
    dumpTech(technology.force)
    if FREE_SAMPLES == 0 then
        return  -- Nothing else to do
    end
    if not technology.effects then
        return  -- No technology effects, so nothing to do.
    end
    for _, effect in pairs(technology.effects) do
        if effect.type == "unlock-recipe" then
            local recipe = game.recipe_prototypes[effect.recipe]
            for _, result in pairs(recipe.products) do
                if result.type == "item" and result.amount then
                    local name = result.name
                    local count
                    if FREE_SAMPLES == 1 then
                        count = result.amount
                    else
                        count = get_any_stack_size(result.name)
                        if FREE_SAMPLES == 2 then
                            count = math.ceil(count / 2)
                        end
                    end
                    add_samples(technology.force, name, count)
                end
            end
        end
    end
end)

function dumpTech(force)
    local research_done = {}
    local data_collection = {["research_done"] = research_done}

    for tech_name, tech in pairs(force.technologies) do
        if tech.researched and string.find(tech_name, "ap%-") == 1 then
            research_done[tech_name] = tech.researched
        end
    end
    game.write_file("ap_bridge.json", game.table_to_json(data_collection), false, 0)
    -- game.write_file("research_done.json", game.table_to_json(data_collection), false, 0)
    -- game.print("Sent progress to Archipelago.")
end



-- add / commands

commands.add_command("ap-sync", "Run manual Research Sync with Archipelago.", function(call)
    dumpTech(game.players[call.player_index].force)
    game.print("Wrote bridge file.")
end)

commands.add_command("ap-get-technology", "Grant a technology, used by the Archipelago Client.", function(call)
    local force = game.forces["player"]
    chunks = {}
    for substring in call.parameter:gmatch("%S+") do -- split on " "
        table.insert(chunks, substring)
    end
    local tech_name = chunks[1]
    local source = chunks[2] or "Archipelago"
    local tech = force.technologies[tech_name]
    if tech ~= nil then
        if tech.researched ~= true then
            game.print({"", "Received [technology=" .. tech.name .. "] from ", source})
            game.play_sound({path="utility/research_completed"})
            tech.researched = true
        end
    else
        game.print("Unknown Technology " .. tech_name)
    end
end)