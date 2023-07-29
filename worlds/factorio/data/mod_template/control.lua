{% from "macros.lua" import dict_to_lua %}
-- this file gets written automatically by the Archipelago Randomizer and is in its raw form a Jinja2 Template
require "lib"
require "util"

FREE_SAMPLES = {{ free_samples }}
SLOT_NAME = "{{ slot_name }}"
SEED_NAME = "{{ seed_name }}"
FREE_SAMPLE_BLACKLIST = {{ dict_to_lua(free_sample_blacklist) }}
TRAP_EVO_FACTOR = {{ evolution_trap_increase }} / 100
MAX_SCIENCE_PACK = {{ max_science_pack }}
GOAL = {{ goal }}
ARCHIPELAGO_DEATH_LINK_SETTING = "archipelago-death-link-{{ slot_player }}-{{ seed_name }}"
ENERGY_INCREMENT = {{ energy_link * 10000000 }}
ENERGY_LINK_EFFICIENCY = 0.75

if settings.global[ARCHIPELAGO_DEATH_LINK_SETTING].value then
    DEATH_LINK = 1
else
    DEATH_LINK = 0
end

CURRENTLY_DEATH_LOCK = 0

{% if chunk_shuffle %}
LAST_POSITIONS = {}
GENERATOR = nil
NORTH = 1
EAST = 2
SOUTH = 3
WEST = 4
ER_COLOR = {1, 1, 1, 0.2}
ER_SEED = {{ random.randint(4294967295, 2*4294967295)}}
CURRENTLY_MOVING = false
ER_FRAMES = {}
CHUNK_OFFSET = {
[NORTH] = {0, 1},
[EAST] = {1, 0},
[SOUTH] = {0, -1},
[WEST] = {-1, 0}
}


function on_player_changed_position(event)
    if CURRENTLY_MOVING == true then
        return
    end
    local player_id = event.player_index
    local player = game.get_player(player_id)
    local character = player.character -- can be nil, such as spectators

    if character == nil then
        return
    end
    local last_position = LAST_POSITIONS[player_id]
    if last_position == nil then
        LAST_POSITIONS[player_id] = character.position
        return
    end

    last_x_chunk = math.floor(last_position.x / 32)
    current_x_chunk = math.floor(character.position.x / 32)
    last_y_chunk = math.floor(last_position.y / 32)
    current_y_chunk = math.floor(character.position.y / 32)
    if (ER_FRAMES[player_id] ~= nil and rendering.is_valid(ER_FRAMES[player_id])) then
        rendering.destroy(ER_FRAMES[player_id])
    end
    ER_FRAMES[player_id] = rendering.draw_rectangle{
        color=ER_COLOR, width=1, filled=false, left_top = {current_x_chunk*32, current_y_chunk*32},
        right_bottom={current_x_chunk*32+32, current_y_chunk*32+32}, players={player}, time_to_live=60,
        draw_on_ground= true, only_in_alt_mode = true, surface=character.surface}
    if current_x_chunk == last_x_chunk and current_y_chunk == last_y_chunk then -- nothing needs doing
        return
    end
    if ((last_position.x - character.position.x) ^ 2 + (last_position.y - character.position.y) ^ 2) > 4000 then
        -- distance too high, death or other teleport took place
        LAST_POSITIONS[player_id] = character.position
        return
    end
    -- we'll need a deterministic random state
    if GENERATOR == nil or not GENERATOR.valid then
        GENERATOR = game.create_random_generator()
    end

    -- sufficiently random pattern
    GENERATOR.re_seed((ER_SEED + (last_x_chunk * 1730000000) + (last_y_chunk * 97000)) % 4294967295)
    -- we now need all 4 exit directions deterministically shuffled to the 4 outgoing directions.
    local exit_table = {
    [1] = 1,
    [2] = 2,
    [3] = 3,
    [4] = 4
    }
    exit_table = fisher_yates_shuffle(exit_table)
    if current_x_chunk > last_x_chunk then -- going right/east
        outbound_direction = EAST
    elseif current_x_chunk < last_x_chunk then -- going left/west
        outbound_direction = WEST
    end

    if current_y_chunk > last_y_chunk then -- going down/south
        outbound_direction = SOUTH
    elseif current_y_chunk < last_y_chunk then -- going up/north
        outbound_direction = NORTH
    end
    local target_direction = exit_table[outbound_direction]

	local target_position = {(CHUNK_OFFSET[target_direction][1] + last_x_chunk) * 32 + 16,
							 (CHUNK_OFFSET[target_direction][2] + last_y_chunk) * 32 + 16}
    target_position = character.surface.find_non_colliding_position(character.prototype.name,
                                                                    target_position, 32, 0.5)
    if target_position ~= nil then
        rendering.draw_circle{color = ER_COLOR, radius = 1, filled = true,
                              target = {character.position.x, character.position.y}, surface = character.surface,
                              time_to_live = 300, draw_on_ground = true}
        rendering.draw_line{color = ER_COLOR, width = 3, gap_length = 0.5, dash_length = 0.5,
                            from = {character.position.x, character.position.y}, to = target_position,
                            surface = character.surface,
                            time_to_live = 300, draw_on_ground = true}
        CURRENTLY_MOVING = true -- prevent recursive event
        character.teleport(target_position)
        CURRENTLY_MOVING = false
    end
    LAST_POSITIONS[player_id] = character.position
end

function fisher_yates_shuffle(tbl)
    for i = #tbl, 2, -1 do
        local j = GENERATOR(i)
        tbl[i], tbl[j] = tbl[j], tbl[i]
    end
    return tbl
end

script.on_event(defines.events.on_player_changed_position, on_player_changed_position)
{% endif %}

function on_check_energy_link(event)
    --- assuming 1 MJ increment and 5MJ battery:
    --- first 2 MJ request fill, last 2 MJ push energy, middle 1 MJ does nothing
    if event.tick % 60 == 30 then
        local surface = game.get_surface(1)
        local force = "player"
        local bridges = surface.find_entities_filtered({name="ap-energy-bridge", force=force})
        local bridgecount = table_size(bridges)
        global.forcedata[force].energy_bridges = bridgecount
        if global.forcedata[force].energy == nil then
            global.forcedata[force].energy = 0
        end
        if global.forcedata[force].energy < ENERGY_INCREMENT * bridgecount * 5 then
            for i, bridge in ipairs(bridges) do
                if bridge.energy > ENERGY_INCREMENT*3 then
                    global.forcedata[force].energy = global.forcedata[force].energy + (ENERGY_INCREMENT * ENERGY_LINK_EFFICIENCY)
                    bridge.energy = bridge.energy - ENERGY_INCREMENT
                end
            end
        end
        for i, bridge in ipairs(bridges) do
            if global.forcedata[force].energy < ENERGY_INCREMENT then
                break
            end
            if bridge.energy < ENERGY_INCREMENT*2 and global.forcedata[force].energy > ENERGY_INCREMENT then
                global.forcedata[force].energy = global.forcedata[force].energy - ENERGY_INCREMENT
                bridge.energy = bridge.energy + ENERGY_INCREMENT
            end
        end
    end
end
if (ENERGY_INCREMENT) then
    script.on_event(defines.events.on_tick, on_check_energy_link)
end

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
        spawn_entity(surface, force, "rocket-silo", spawn_position.x, spawn_position.y, 80, true, true)
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
    data["death_link_tick"] = 0
    data["energy"] = 0
    data["energy_bridges"] = 0
    global.forcedata[event.force] = data
{%- if silo == 2 %}
    check_spawn_silo(force)
{%- endif %}
{%- for tech_name in useless_technologies %}
    force.technologies.{{ tech_name }}.researched = true
{%- endfor %}
end
script.on_event(defines.events.on_force_created, on_force_created)

-- Destroy force data.  This doesn't appear to be currently possible with the Factorio API, but here for completeness.
function on_force_destroyed(event)
{%- if silo == 2 %}
    check_despawn_silo(event.force)
{%- endif %}
    global.forcedata[event.force.name] = nil
end

function on_runtime_mod_setting_changed(event)
    local force
    if event.player_index == nil then
        force = game.forces.player
    else
        force = game.players[event.player_index].force
    end

    if event.setting == ARCHIPELAGO_DEATH_LINK_SETTING then
        if settings.global[ARCHIPELAGO_DEATH_LINK_SETTING].value then
            DEATH_LINK = 1
        else
            DEATH_LINK = 0
        end
        if force ~= nil then
            dumpInfo(force)
        end
    end
end
script.on_event(defines.events.on_runtime_mod_setting_changed, on_runtime_mod_setting_changed)

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
    dumpInfo(player.force)
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
    if event.rocket and event.rocket.valid and global.forcedata[event.rocket.force.name]['victory'] == 0 then
        if event.rocket.get_item_count("satellite") > 0 or GOAL == 0 then
            global.forcedata[event.rocket.force.name]['victory'] = 1
            dumpInfo(event.rocket.force)
            game.set_game_state
            {
                game_finished = true,
                player_won = true,
                can_continue = true,
                victorious_force = event.rocket.force
            }
        end
    end
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
        if game.item_prototypes[name] then
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
        else
            player.print("Unable to receive " .. count .. "x [item=" .. name .. "] as this item does not exist.")
            samples[name] = nil
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
        if count <= 0 then
            -- Fixes a bug with single craft, if a recipe gives 0 of a given item.
            return
        end
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

    if remote.interfaces["silo_script"] then
        remote.call("silo_script", "set_no_victory", true)
    end
end)

-- hook into researches done
script.on_event(defines.events.on_research_finished, function(event)
    local technology = event.research
    if string.find(technology.force.name, "EE_TESTFORCE") == 1 then
        --Don't acknowledge AP research as an Editor Extensions test force
        --Also no need for free samples in the Editor extensions testing surfaces, as these testing surfaces
        --are worked on exclusively in editor mode.
        return
    end
    if technology.researched and string.find(technology.name, "ap%-") == 1 then
        -- check if it came from the server anyway, then we don't need to double send.
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

function kill_players(force)
    CURRENTLY_DEATH_LOCK = 1
    local current_character = nil
    for _, player in ipairs(force.players) do
        current_character = player.character
        if current_character ~= nil then
            current_character.die()
        end
    end
    CURRENTLY_DEATH_LOCK = 0
end

function spawn_entity(surface, force, name, x, y, radius, randomize, avoid_ores)
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
        xmin = math.ceil(x - radius - box.left_top.x),
        xmax = math.floor(x + radius - box.right_bottom.x),
        ymin = math.ceil(y - radius - box.left_top.y),
        ymax = math.floor(y + radius - box.right_bottom.y)
    }

    local new_entity = nil
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
            surface.request_to_generate_chunks(args.position, entity_radius)
            surface.force_generate_chunk_requests()
        end
        -- Try to place entity
        if surface.can_place_entity(args) then
            -- Can hypothetically place this entity here.  Destroy everything underneath it.
            local collision_area = {
                {
                    args.position.x + prototype.collision_box.left_top.x,
                    args.position.y + prototype.collision_box.left_top.y
                },
                {
                    args.position.x + prototype.collision_box.right_bottom.x,
                    args.position.y + prototype.collision_box.right_bottom.y
                }
            }
            local entities = surface.find_entities_filtered {
                area = collision_area,
                collision_mask = prototype.collision_mask
            }
            local can_place = true
            for _, entity in pairs(entities) do
                if entity.force and entity.force.name ~= 'neutral' then
                    can_place = false
                    break
                end
            end
            local allow_placement_on_resources = not avoid_ores or i > attempts/2
            if can_place and not allow_placement_on_resources then
                local resources = surface.find_entities_filtered {
                    area = collision_area,
                    type = 'resource'
                }
                can_place = (next(resources) == nil)
            end
            if can_place then
                for _, entity in pairs(entities) do
                    entity.destroy({do_cliff_correction=true, raise_destroy=true})
                end
                args.build_check_type = defines.build_check_type.script
                args.create_build_effect_smoke = false
                new_entity = surface.create_entity(args)
                if new_entity then
                    new_entity.destructible = false
                    new_entity.minable = false
                    new_entity.rotatable = false
                    break
                end
            end
        end
    end
    if new_entity == nil then
        force.print("Failed to place " .. args.name .. " in " .. serpent.line({x = x, y = y, radius = radius}))
    end
end


script.on_event(defines.events.on_entity_died, function(event)
    if DEATH_LINK == 0 then
        return
    end
    if CURRENTLY_DEATH_LOCK == 1 then -- don't re-trigger on same event
        return
    end

    local force = event.entity.force
    global.forcedata[force.name].death_link_tick = game.tick
    dumpInfo(force)
    kill_players(force)
end, {LuaEntityDiedEventFilter = {["filter"] = "name", ["name"] = "character"}})


-- add / commands
commands.add_command("ap-sync", "Used by the Archipelago client to get progress information", function(call)
    local force
    if call.player_index == nil then
        force = game.forces.player
    else
        force = game.players[call.player_index].force
    end
    local research_done = {}
    local forcedata = chain_lookup(global, "forcedata", force.name)
    local data_collection = {
        ["research_done"] = research_done,
        ["victory"] = chain_lookup(forcedata, "victory"),
        ["death_link_tick"] = chain_lookup(forcedata, "death_link_tick"),
        ["death_link"] = DEATH_LINK,
        ["energy"] = chain_lookup(forcedata, "energy"),
        ["energy_bridges"] = chain_lookup(forcedata, "energy_bridges"),
        ["multiplayer"] = #game.players > 1,
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

TRAP_TABLE = {
["Attack Trap"] = function ()
    game.surfaces["nauvis"].build_enemy_base(game.forces["player"].get_spawn_position(game.get_surface(1)), 25)
end,
["Evolution Trap"] = function ()
    game.forces["enemy"].evolution_factor = game.forces["enemy"].evolution_factor + (TRAP_EVO_FACTOR * (1 - game.forces["enemy"].evolution_factor))
    game.print({"", "New evolution factor:", game.forces["enemy"].evolution_factor})
end,
["Teleport Trap"] = function ()
    for _, player in ipairs(game.forces["player"].players) do
        current_character = player.character
        if current_character ~= nil then
            current_character.teleport(current_character.surface.find_non_colliding_position(
                current_character.prototype.name, random_offset_position(current_character.position, 1024), 0, 1))
        end
    end
end,
["Grenade Trap"] = function ()
    fire_entity_at_players("grenade", 0.1)
end,
["Cluster Grenade Trap"] = function ()
    fire_entity_at_players("cluster-grenade", 0.1)
end,
["Artillery Trap"] = function ()
    fire_entity_at_players("artillery-projectile", 1)
end,
["Atomic Rocket Trap"] = function ()
    fire_entity_at_players("atomic-rocket", 0.1)
end,
}

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
            game.print({"", "Received [technology=" .. tech.name .. "] as it is already checked."})
            game.play_sound({path="utility/research_completed"})
            tech.researched = true
        end
        return
    elseif progressive_technologies[item_name] ~= nil then
        if global.index_sync[index] ~= item_name then -- not yet received prog item
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
            global.index_sync[index] = tech
            if tech.researched ~= true then
                game.print({"", "Received [technology=" .. tech.name .. "] from ", source})
                game.play_sound({path="utility/research_completed"})
                tech.researched = true
            end
        end
    elseif TRAP_TABLE[item_name] ~= nil then
        if global.index_sync[index] ~= item_name then -- not yet received trap
            global.index_sync[index] = item_name
            game.print({"", "Received ", item_name, " from ", source})
            TRAP_TABLE[item_name]()
        end
    else
        game.print("Unknown Item " .. item_name)
    end
end)


commands.add_command("ap-rcon-info", "Used by the Archipelago client to get information", function(call)
    rcon.print(game.table_to_json({
        ["slot_name"] = SLOT_NAME,
        ["seed_name"] = SEED_NAME,
        ["death_link"] = DEATH_LINK,
        ["energy_link"] = ENERGY_INCREMENT
    }))
end)


{% if allow_cheats -%}
commands.add_command("ap-spawn-silo", "Attempts to spawn a silo around 0,0", function(call)
    spawn_entity(game.player.surface, game.player.force, "rocket-silo", 0, 0, 80, true, true)
end)
{% endif -%}


commands.add_command("ap-deathlink", "Kill all players", function(call)
    local force = game.forces["player"]
    local source = call.parameter or "Archipelago"
    kill_players(force)
    game.print("Death was granted by " .. source)
end)

commands.add_command("ap-energylink", "Used by the Archipelago client to manage Energy Link", function(call)
    local change = tonumber(call.parameter or "0")
    local force = "player"
    global.forcedata[force].energy = global.forcedata[force].energy + change
end)

commands.add_command("energy-link", "Print the status of the Archipelago energy link.", function(call)
    log("Player command energy-link") -- notifies client
end)

commands.add_command("toggle-ap-send-filter", "Toggle filtering of item sends that get displayed in-game to only those that involve you.", function(call)
    log("Player command toggle-ap-send-filter") -- notifies client
end)

commands.add_command("toggle-ap-chat", "Toggle sending of chat messages from players on the Factorio server to Archipelago.", function(call)
    log("Player command toggle-ap-chat") -- notifies client
end)

-- data
progressive_technologies = {{ dict_to_lua(progressive_technology_table) }}
