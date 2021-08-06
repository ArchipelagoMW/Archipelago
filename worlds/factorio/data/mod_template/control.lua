{% from "macros.lua" import dict_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require "lib"
require "util"

FREE_SAMPLES = {{ free_samples }}
SLOT_NAME = "{{ slot_name }}"
SEED_NAME = "{{ seed_name }}"
FREE_SAMPLE_BLACKLIST = {{ dict_to_lua(free_sample_blacklist) }}
TRAP_EVO_FACTOR = {{ evolution_trap_increase }} / 100

{% if not imported_blueprints -%}
function set_permissions()
    local group = game.permissions.get_group("Default")
    group.set_allows_action(defines.input_action.open_blueprint_library_gui, false)
    group.set_allows_action(defines.input_action.import_blueprint, false)
    group.set_allows_action(defines.input_action.import_blueprint_string, false)
    group.set_allows_action(defines.input_action.import_blueprints_filtered, false)
end
{%- endif %}


function check_spawn_silo(force)
    if force.players and #force.players > 0 and force.get_entity_count("rocket-silo") < 1 then
        local surface = game.get_surface(1)
        local spawn_position = force.get_spawn_position(surface)
        spawn_entity(surface, force, "rocket-silo", spawn_position.x, spawn_position.y, 80, true)
    end
end

function check_despawn_silo(force)
    if not force.players or #force.players < 1 and force.get_entity_count("rocket-silo") > 0 then
        local surface = game.get_surface(1)
        local spawn_position = force.get_spawn_position(surface)
        local x1 = spawn_position.x - 41
        local x2 = spawn_position.x + 41
        local y1 = spawn_position.y - 41
        local y2 = spawn_position.y + 41
        local silos = surface.find_entities_filtered{area = { {x1, y1}, {x2, y2} },
                                                     name = "rocket-silo",
                                                     force = force}
        for i,silo in ipairs(silos) do
            silo.destructible = true
            silo.destroy()
        end
    end
end


-- Initialize force data, either from it being created or already being part of the game when the mod was added.
function on_force_created(event)
    local force = event.force
    if type(event.force) == "string" then  -- should be of type LuaForce
        force = game.forces[force]
    end
    force.research_queue_enabled = true
    local data = {}
    data['earned_samples'] = {{ dict_to_lua(starting_items) }}
    data["victory"] = 0
    global.forcedata[event.force] = data
{%- if silo == 2 %}
    check_spawn_silo(force)
{%- endif %}
end
script.on_event(defines.events.on_force_created, on_force_created)

-- Destroy force data.  This doesn't appear to be currently possible with the Factorio API, but here for completeness.
function on_force_destroyed(event)
{%- if silo == 2 %}
    check_despawn_silo(event.force)
{%- endif %}
    global.forcedata[event.force.name] = nil
end

-- Initialize player data, either from them joining the game or them already being part of the game when the mod was
-- added.`
function on_player_created(event)
    local player = game.players[event.player_index]
    -- FIXME: This (probably) fires before any other mod has a chance to change the player's force
    -- For now, they will (probably) always be on the 'player' force when this event fires.
    local data = {}
    data['pending_samples'] = table.deepcopy(global.forcedata[player.force.name]['earned_samples'])
    global.playerdata[player.index] = data
    update_player(player.index)  -- Attempt to send pending free samples, if relevant.
{%- if silo == 2 %}
    check_spawn_silo(game.players[event.player_index].force)
{%- endif %}
end
script.on_event(defines.events.on_player_created, on_player_created)

-- Create/destroy silo for force if player switched force
function on_player_changed_force(event)
{%- if silo == 2 %}
    check_despawn_silo(event.force)
    check_spawn_silo(game.players[event.player_index].force)
{%- endif %}
end
script.on_event(defines.events.on_player_changed_force, on_player_changed_force)

function on_player_removed(event)
    global.playerdata[event.player_index] = nil
end
script.on_event(defines.events.on_player_removed, on_player_removed)

function on_rocket_launched(event)
    global.forcedata[event.rocket.force.name]['victory'] = 1
    dumpInfo(event.rocket.force)
end
script.on_event(defines.events.on_rocket_launched, on_rocket_launched)

-- Updates a player, attempting to send them any pending samples (if relevant)
function update_player(index)
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

end

-- Update players upon them connecting, since updates while they're offline are suppressed.
script.on_event(defines.events.on_player_joined_game, function(event) update_player(event.player_index) end)

function update_player_event(event)
    update_player(event.player_index)
end

script.on_event(defines.events.on_player_main_inventory_changed, update_player_event)

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
    {% if not imported_blueprints %}set_permissions(){% endif %}
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

-- hook into researches done
script.on_event(defines.events.on_research_finished, function(event)
    local technology = event.research
    if technology.researched and string.find(technology.name, "ap%-") == 1 then
        dumpInfo(technology.force) --is sendable
    else
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
                        if FREE_SAMPLE_BLACKLIST[name] ~= 1 then
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
        end
    end
end)


function dumpInfo(force)
    log("Archipelago Bridge Data available for game tick ".. game.tick .. ".") -- notifies client
end


function chain_lookup(table, ...)
    for _, k in ipairs{...} do
        table = table[k]
        if not table then
            return nil
        end
    end
    return table
end


function spawn_entity(surface, force, name, x, y, radius, randomize)
    local prototype = game.entity_prototypes[name]
    local args = {  -- For can_place_entity and place_entity
        name = prototype.name,
        position = {x = x, y = y},
        force = force.name,
        build_check_type = defines.build_check_type.blueprint_ghost,
        forced = true
    }

    local box = prototype.selection_box
    local dims = {
        w = box.right_bottom.x - box.left_top.x,
        h = box.right_bottom.y - box.left_top.y
    }
    local entity_radius = math.ceil(math.max(dims.w, dims.h) / math.sqrt(2) / 2)
    local bounds = {
        xmin = math.ceil(x - (radius - dims.w/2)),
        xmax = math.floor(x + (radius - dims.w/2)),
        ymin = math.ceil(y - (radius - dims.h/2)),
        ymax = math.floor(y + (radius - dims.h/2))
    }

    local entity = nil
    local attempts = 1000
    for i = 1,attempts do  -- Try multiple times
        -- Find a position
        if (randomize and i < attempts-3) or (not randomize and i ~= 1) then
            args.position.x = math.random(bounds.xmin, bounds.xmax)
            args.position.y = math.random(bounds.ymin, bounds.ymax)
        elseif randomize then
            args.position.x = x + (i + 3 - attempts) * dims.w
            args.position.y = y + (i + 3 - attempts) * dims.h
        end
        -- Generate required chunks
        local x1 = args.position.x + box.left_top.x
        local x2 = args.position.x + box.right_bottom.x
        local y1 = args.position.y + box.left_top.y
        local y2 = args.position.y + box.right_bottom.y
        if not surface.is_chunk_generated({x = x1, y = y1}) or
           not surface.is_chunk_generated({x = x2, y = y1}) or
           not surface.is_chunk_generated({x = x1, y = y2}) or
           not surface.is_chunk_generated({x = x2, y = y2}) then
            --player.print("Generating chunk at " .. serpent.line(args.position) .. ", radius=" .. entity_radius)
            surface.request_to_generate_chunks(args.position, entity_radius)
            surface.force_generate_chunk_requests()
        end
        -- Try to place entity
        if surface.can_place_entity(args) then
            -- Can hypothetically place this entity here.  Destroy everything underneath it.
            local collision_area = {
                {
                    args.position.x + prototype.collision_box.left_top.x,
                    args.position.y + prototype.collision_box.left_top.x
                },
                {
                    args.position.x + prototype.collision_box.right_bottom.x,
                    args.position.y + prototype.collision_box.right_bottom.x
                }
            }
            local entities = surface.find_entities_filtered {
                area = collision_area,
                collision_mask = prototype.collision_mask
            }
            local has_invalid_entities = false
            for _, entity in pairs(entities) do
                if entity.force and (entity.force.name ~= 'neutral') then
                    has_invalid_entities = true
                end
            end
            if not has_invalid_entities then
                for _, entity in pairs(entities) do
                    entity.destroy({do_cliff_correction=true, raise_destroy=true})
                end
                args.build_check_type = defines.build_check_type.script
                args.create_build_effect_smoke = false
                entity = surface.create_entity(args)
                if entity then
                    entity.destructible = false
                    entity.minable = false
                    entity.rotatable = false
                    break
                end
            end
        end
    end
    if entity == nil then
        force.print("Failed to place " .. args.name .. " in " .. serpent.line({x = x, y = y, radius = radius}))
    end
end


-- add / commands
commands.add_command("ap-sync", "Used by the Archipelago client to get progress information", function(call)
    local force
    if call.player_index == nil then
        force = game.forces.player
    else
        force = game.players[call.player_index].force
    end
    local research_done = {}
    local data_collection = {
        ["research_done"] = research_done,
        ["victory"] = chain_lookup(global, "forcedata", force.name, "victory"),
        }

    for tech_name, tech in pairs(force.technologies) do
        if tech.researched and string.find(tech_name, "ap%-") == 1 then
            research_done[tech_name] = tech.researched
        end
    end
    rcon.print(game.table_to_json({["slot_name"] = SLOT_NAME, ["seed_name"] = SEED_NAME, ["info"] = data_collection}))
end)

commands.add_command("ap-print", "Used by the Archipelago client to print messages", function (call)
    game.print(call.parameter)
end)

commands.add_command("ap-get-technology", "Grant a technology, used by the Archipelago Client.", function(call)
    if global.index_sync == nil then
        global.index_sync = {}
    end
    local tech
    local force = game.forces["player"]
    chunks = split(call.parameter, "\t")
    local item_name = chunks[1]
    local index = chunks[2]
    local source = chunks[3] or "Archipelago"
    if index == -1 then -- for coop sync and restoring from an older savegame
        tech = force.technologies[item_name]
        if tech.researched ~= true then
            game.print({"", "Received [technology=" .. tech.name .. "] as it is already checked.")
            game.play_sound({path="utility/research_completed"})
            tech.researched = true
            return
        end
    elif progressive_technologies[item_name] ~= nil then
        if global.index_sync[index] == nil then -- not yet received prog item
            global.index_sync[index] = item_name
            local tech_stack = progressive_technologies[item_name]
            for _, item_name in ipairs(tech_stack) do
                tech = force.technologies[item_name]
                if tech.researched ~= true then
                    game.print({"", "Received [technology=" .. tech.name .. "] from ", source})
                    game.play_sound({path="utility/research_completed"})
                    tech.researched = true
                    return
                end
            end
        end
    elseif force.technologies[item_name] ~= nil then
        tech = force.technologies[item_name]
        if tech ~= nil then
            if global.index_sync[index] ~= nil and global.index_sync[index] ~= tech then
                game.print("Warning: Desync Detected. Duplicate/Missing items may occur.")
            end
            global.index_sync[index] = tech
            if tech.researched ~= true then
                game.print({"", "Received [technology=" .. tech.name .. "] from ", source})
                game.play_sound({path="utility/research_completed"})
                tech.researched = true
            end
        end
    elseif item_name == "Attack Trap" then
        if global.index_sync[index] == nil then -- not yet received trap
            game.print({"", "Received Attack Trap from ", source})
            global.index_sync[index] = item_name
            local spawn_position = force.get_spawn_position(game.get_surface(1))
            game.surfaces["nauvis"].build_enemy_base(spawn_position, 25)
        end
    elseif item_name == "Evolution Trap" then
        if global.index_sync[index] == nil then -- not yet received trap
            global.index_sync[index] = item_name
            game.forces["enemy"].evolution_factor = game.forces["enemy"].evolution_factor + TRAP_EVO_FACTOR
            game.print({"", "Received Evolution Trap from ", source, ". New factor:", game.forces["enemy"].evolution_factor})
        end
    else
        game.print("Unknown Item " .. item_name)
    end
end)


commands.add_command("ap-rcon-info", "Used by the Archipelago client to get information", function(call)
    rcon.print(game.table_to_json({["slot_name"] = SLOT_NAME, ["seed_name"] = SEED_NAME}))
end)


{% if allow_cheats -%}
commands.add_command("ap-spawn-silo", "Attempts to spawn a silo around 0,0", function(call)
    spawn_entity(game.player.surface, game.player.force, "rocket-silo", 0, 0, 80, true)
end)
{% endif -%}


-- data
progressive_technologies = {{ dict_to_lua(progressive_technology_table) }}
