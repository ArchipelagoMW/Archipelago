local general = require("Archipelago/general")
local library = require("libs/lib")

local function add_action_to_tick (tick, action_name, action)
    storage.on_tick[tick] = storage.on_tick[tick] or {}
    storage.on_tick[tick][action_name] = action
end

local function remove_action_from_tick (tick, action_name)
    storage.on_tick[tick][action_name] = nil
    if  storage.on_tick[tick] == {} then
        storage.on_tick[tick] = nil
    end
end


local function random_offset_position (position, offset)
    return {x=position.x+math.random(-offset, offset), y=position.y+math.random(-offset, offset)}
end

local function fire_entity_at_entities (entity_name, entities, speed)
    if not prototypes.entity[entity_name] then return end
    if not prototypes.entity[entity_name].valid then return end
    for _, current_entity in ipairs(entities) do
        local target = current_entity
        if target.health == nil then
            target = target.position
        end
        current_entity.surface.create_entity{name=entity_name,
            position=random_offset_position(current_entity.position, 128),
            target=target, speed=speed}
    end
end

local function fire_entity_at_players (entity_name, speed)
    if not prototypes.entity[entity_name] then return end
    if not prototypes.entity[entity_name].valid then return end
    local entities = {}
    for force_name, force in pairs(game.forces) do
        if library.is_valid_ap_force(force) then
            for _, player in ipairs(game.forces[force_name].players) do
                if player.character ~= nil then
                    table.insert(entities, player.character)
                end
            end
        end
    end
    return fire_entity_at_entities(entity_name, entities, speed)
end

local teleport_requests = {}
local teleport_attempts = {}
local max_attempts = 100

local function attempt_teleport_player (player, attempt)
    -- global attempt storage as metadata can't be stored
    if attempt == nil then
        attempt = teleport_attempts[player.index]
    else
        teleport_attempts[player.index] = attempt
    end

    if attempt > max_attempts then
        player.print("Teleport failed: No valid position found after " .. max_attempts .. " attempts!")
        teleport_attempts[player.index] = 0
        return
    end

    local surface = player.character.surface
    local prototype_name = player.character.prototype.name
    local original_position = player.character.position
    local candidate_position = random_offset_position(original_position, 1024)

    local non_colliding_position = surface.find_non_colliding_position(
        prototype_name, candidate_position, 0, 1
    )

    if non_colliding_position then
        -- Request pathfinding asynchronously
        local path_id = surface.request_path{
            bounding_box = player.character.prototype.collision_box,
            collision_mask = { layers = { ["player"] = true } },
            start = original_position,
            goal = non_colliding_position,
            force = player.force.name,
            radius = 1,
            pathfind_flags = {cache = true, low_priority = true, allow_paths_through_own_entities = true},
        }

        -- Store the request with the player index as the key
        teleport_requests[player.index] = path_id
    else
        attempt_teleport_player(player, attempt + 1)
    end
end

local function handle_teleport_attempt (event)
    for player_index, path_id in pairs(teleport_requests) do
        -- Check if the event matches the stored path_id
        if path_id == event.id then
            local player = game.players[player_index]

            if event.path then
                if player.character then
                    player.character.teleport(event.path[#event.path].position)  -- Teleport to the last point in the path
                    -- Clear the attempts for this player
                    teleport_attempts[player_index] = 0
                    return
                end
                return
            end

            attempt_teleport_player(player, nil)
            break
        end
    end
end

local function spill_character_inventory (character)
    if not (character and character.valid) then
        return false
    end

    -- grab attrs once pre-loop
    local position = character.position
    local surface = character.surface

    local inventories_to_spill = {
        defines.inventory.character_main, -- Main inventory
        defines.inventory.character_trash, -- Logistic trash slots
    }

    for _, inventory_type in pairs(inventories_to_spill) do
        local inventory = character.get_inventory(inventory_type)
        if inventory and inventory.valid then
            -- Spill each item stack onto the ground
            for i = 1, #inventory do
                local stack = inventory[i]
                if stack and stack.valid_for_read then
                    local spilled_items = surface.spill_item_stack{
                        position = position,
                        stack = stack,
                        enable_looted = false, -- do not mark for auto-pickup
                        force = nil, -- do not mark for auto-deconstruction
                        allow_belts = true, -- do mark for putting it onto belts
                    }
                    if #spilled_items > 0 then
                        stack.clear() -- only delete if spilled successfully
                    end
                end
            end
        end
    end
end

local function undo_peekaboo_trap()
    for name, data in pairs(storage.trap_memory.peekaboo.force) do
        for _, tech in pairs(data.temp_hidden_tech) do
            game.forces[name].technologies[tech].enabled = true
        end
        game.forces[name].research_queue = data.temp_hidden_queue
    end
    storage.trap_memory.peekaboo.active = false
end

local function set_energy_spiral(number)
    if number == 0 then
        game.print({"spiral-0"})
    elseif number == 1 then
        game.print({"spiral-1"})
    elseif number == 2 then
        game.print({"spiral-2"})
    elseif number == 3 then
        game.print({"spiral-3"})
    elseif number == 4 then
        game.print({"spiral-4"})
    else
        game.print({"spiral-last"})
    end

    for _, surface in pairs(game.surfaces) do
        surface.global_effect = {
            consumption = (number * 2),
            pollution = (number * 1),
        }
    end
end

local function undo_energy_spiral()
    storage.trap_memory.spirals = storage.trap_memory.spirals - 1
    set_energy_spiral(storage.trap_memory.spirals)
end

--##### ####   ###  ####        ##### #   # #   #  ###  #####  ###   ###  #   #  #### 
--  #   #   # #   # #   #       #     #   # ##  # #   #   #     #   #   # ##  # #     
--  #   ####  ##### ####        ###   #   # # # # #       #     #   #   # # # #  ###  
--  #   #   # #   # #           #     #   # #  ## #   #   #     #   #   # #  ##     # 
--  #   #   # #   # #           #      #### #   #  ###    #    ###   ###  #   # ####  

local function attack_trap()
    game.surfaces["nauvis"].build_enemy_base(game.forces["player"].get_spawn_position(game.get_surface(1)), 25)
end

local function evolution_trap ()
    local new_factor = game.forces["enemy"].get_evolution_factor("nauvis") +
        (general.traps.evo_increase * (1 - game.forces["enemy"].get_evolution_factor("nauvis")))
    game.forces["enemy"].set_evolution_factor(new_factor, "nauvis")
    game.print({"", "New evolution factor:", new_factor})
end

local function teleport_trap()
    for _, player in ipairs(game.forces["player"].players) do
        if player.character then
            attempt_teleport_player(player, 1)
        end
    end
end

local function grenade_trap ()
    fire_entity_at_players("grenade", 0.1)
end

local function cluster_grenade_trap ()
    fire_entity_at_players("cluster-grenade", 0.1)
end

local function artillery_trap ()
    fire_entity_at_players("artillery-projectile", 1)
end

local function atomic_rocket_trap ()
    fire_entity_at_players("atomic-rocket", 0.1)
end

local function atomic_cliff_remover()
    local cliffs = game.surfaces["nauvis"].find_entities_filtered{type = "cliff"}

    if #cliffs > 0 then
        fire_entity_at_entities("atomic-rocket", {cliffs[math.random(#cliffs)]}, 0.1)
    end
end

local function inventory_spill_trap()
    for _, player in ipairs(game.forces["player"].players) do
        spill_character_inventory(player.character)
    end
end

local function hide_technology_trap()
    -- TODO: Make this compatiable with tech obscurity.
    storage.trap_memory.peekaboo = storage.trap_memory.peekaboo or {reveal_tech_tick = 0, force = {}}
    if storage.trap_memory.peekaboo.reveal_tech_tick > game.tick then
        remove_action_from_tick(storage.trap_memory.peekaboo.reveal_tech_tick, "undo-peekaboo-trap")
        storage.trap_memory.peekaboo.reveal_tech_tick = storage.trap_memory.peekaboo.reveal_tech_tick + general.traps.hide_tech_time / 2
        add_action_to_tick(storage.trap_memory.peekaboo.reveal_tech_tick, "undo-peekaboo-trap", undo_peekaboo_trap)
    else
        for _, force in pairs(library.get_all_ap_forces()) do
            storage.trap_memory.peekaboo.force[force.name] = storage.trap_memory.peekaboo.force[force.name] or {}
            storage.trap_memory.peekaboo.force[force.name].temp_hidden_tech = {}
            storage.trap_memory.peekaboo.force[force.name].temp_hidden_queue = force.research_queue
            force.research_queue = nil
            for _, tech in pairs(force.technologies) do
                if tech.enabled and (not tech.researched) and (tech.name ~= "crash-prevention") then
                    storage.trap_memory.peekaboo.force[force.name].temp_hidden_tech[tech.name] = tech.name
                    tech.enabled = false
                end
            end
        end
        storage.trap_memory.peekaboo.active = true
        storage.trap_memory.peekaboo.reveal_tech_tick = game.tick + general.traps.hide_tech_time
        add_action_to_tick(storage.trap_memory.peekaboo.reveal_tech_tick, "undo-peekaboo-trap", undo_peekaboo_trap)
    end
end

local function reset_technology_progress_trap()
    for _, force in pairs(library.get_all_ap_forces()) do
        force.research_progress = 0
        for _, tech in pairs(force.technologies) do
            tech.saved_progress = 0
        end
    end
end

local function clear_map_trap()
    for _, force in pairs(library.get_all_ap_forces()) do
        force.clear_chart()
    end
end

local function energy_spiral_trap()
    local clear_effect = game.tick + general.traps.energy_pollution_duration
    repeat
        clear_effect = clear_effect + 1
    until (storage.on_tick[clear_effect] == nil or storage.on_tick[clear_effect] ~= nil and storage.on_tick[clear_effect]["undo-energy-spiral-trap"] == nil)

    if storage.trap_memory.spirals == nil then
        storage.trap_memory.spirals = 0
    end
    storage.trap_memory.spirals = storage.trap_memory.spirals + 1

    set_energy_spiral(storage.trap_memory.spirals)

    add_action_to_tick(clear_effect, "undo-energy-spiral-trap", undo_energy_spiral)
end

local trap_table = {
    ["Attack Trap"] = attack_trap,
    ["Evolution Trap"] = evolution_trap,
    ["Teleport Trap"] = teleport_trap,
    ["Grenade Trap"] = grenade_trap,
    ["Cluster Grenade Trap"] = cluster_grenade_trap,
    ["Artillery Trap"] = artillery_trap,
    ["Atomic Rocket Trap"] = atomic_rocket_trap,
    ["Atomic Cliff Remover Trap"] = atomic_cliff_remover,
    ["Inventory Spill Trap"] =  inventory_spill_trap,
    ["Peek a Tech Trap"] =  hide_technology_trap,
    ["Tech Reset Trap"] =  reset_technology_progress_trap,
    ["Reset Map Info Trap"] =  clear_map_trap,
    ["Energy Spiral Trap"] = energy_spiral_trap
}

--##### ####   ###  ####   ####       #   #  ###  ####  ##### 
--  #   #   # #   # #   # #           ## ## #   # #   # #     
--  #   ####  ##### ####   ###        # # # ##### #   # ###   
--  #   #   # #   # #         #       #   # #   # #   # #     
--  #   #   # #   # #     ####        #   # #   # ####  ##### 

local function is_trap(trap_name)
    if trap_table[trap_name] ~= nil then
        return true
    end
    return false
end

local function run_trap(trap_name)
    if is_trap(trap_name) then
        trap_table[trap_name]()
    end
end

local function on_tick(event)
    if not storage.on_tick[game.tick] then return end --there is nothing to do.
    for _, action in pairs(storage.on_tick[game.tick]) do
        action()
    end
    storage.on_tick[game.tick] = nil
end

local function on_init()
    storage.on_tick = storage.on_tick or {} --will contain a list of actions on each tick.
    storage.trap_memory = storage.trap_memory or {} --will information about traps that needs to be remembered.
end

commands.add_command("activate-AP-trap", "sends an AP trap", function(call)
    if call.parameter == nil then
        game.print("please enter an name")
        return
    end
    game.print("recieved command: "..serpent.line(call))
    run_trap(call.parameter)
end)

local lib = {}

lib.events = {
    [defines.events.on_tick] = on_tick,
    --[defines.events.on_research_finished] = on_research_finished,
    --[defines.events.on_force_created] = on_force_created,
    --[defines.events.on_player_created] = on_player_created,
    --[defines.events.on_player_removed] = on_player_removed,

    --[defines.events.on_player_joined_game] = update_player_event,
    --[defines.events.on_player_main_inventory_changed] = update_player_event,
    --[defines.events.on_cutscene_cancelled] = update_player_event,
    --[defines.events.on_cutscene_finished] = update_player_event,

    --[defines.events.on_surface_created] = on_surface_created,
    --[defines.events.on_surface_created] = on_surface_created,
    --[defines.events.on_surface_created] = on_surface_created,


    [defines.events.on_script_path_request_finished] = handle_teleport_attempt
}
lib.on_init = on_init
--lib.on_configuration_changed = on_configuration_changed

lib.is_trap = is_trap
lib.run_trap = run_trap

return lib