
local general = require("Archipelago/general")
local library = require("libs/lib")


local function set_permissions()
    local group = game.permissions.get_group("Default")
    group.set_allows_action(defines.input_action.open_blueprint_library_gui, false)
    group.set_allows_action(defines.input_action.import_blueprint, false)
    group.set_allows_action(defines.input_action.import_blueprint_string, false)
    group.set_allows_action(defines.input_action.import_blueprints_filtered, false)
end

local function spawn_entity(surface, force, name, x, y, radius, randomize, avoid_ores)
    local prototype = prototypes.entity[name]
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
                collision_mask = prototype.collision_mask.layers
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
                if script.active_mods["quality"] then
                    args.quality = general.free_samples.quality
                end
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

local function check_spawn_silo(force)
    if force.players and #force.players > 0 and force.get_entity_count("rocket-silo") < 1 then
        local surface = game.get_surface(1)
        local spawn_position = force.get_spawn_position(surface)
        spawn_entity(surface, force, "rocket-silo", spawn_position.x, spawn_position.y, 80, true, true)
        spawn_entity(surface, force, "cargo-landing-pad", spawn_position.x, spawn_position.y, 80, true, true)
    end
end

local function check_despawn_silo(force)
    if not force.players or #force.players < 1 then
        if force.get_entity_count("rocket-silo") > 0 then
            local surface = game.get_surface(1)
            local spawn_position = force.get_spawn_position(surface)
            local x1 = spawn_position.x - 41
            local x2 = spawn_position.x + 41
            local y1 = spawn_position.y - 41
            local y2 = spawn_position.y + 41
            local silos = surface.find_entities_filtered{area = { {x1, y1}, {x2, y2} },
                                                         name = "rocket-silo",
                                                         force = force}
            for i, silo in ipairs(silos) do
                silo.destructible = true
                silo.destroy()
            end
        end
        if force.get_entity_count("cargo-landing-pad") > 0 then
            local surface = game.get_surface(1)
            local spawn_position = force.get_spawn_position(surface)
            local x1 = spawn_position.x - 41
            local x2 = spawn_position.x + 41
            local y1 = spawn_position.y - 41
            local y2 = spawn_position.y + 41
            local pads = surface.find_entities_filtered{area = { {x1, y1}, {x2, y2} },
                                                        name = "cargo-landing-pad",
                                                        force = force}
            for i, pad in ipairs(pads) do
                pad.destructible = true
                pad.destroy()
            end
        end
    end
end

local function on_force_created(event)
    local force = event.force
    storage.forcedata[force.name] = storage.forcedata[force.name] or {}
    storage.forcedata[force.name]["victory"] = storage.forcedata[force.name]["victory"] or 0
    if general.silo == 2 then
        check_spawn_silo(force)
    end
    for _, name in pairs(general.technologies.removed_technologies()) do
        if force.technologies[name] then
            force.technologies[name].researched = true
        else
            log("Recoverable Error: No technology found for name "..name.." in removed_technologies")
        end
    end
end

local function on_force_destroyed(event)
    if general.silo == 2 then
        check_despawn_silo(event.force)
    end
    storage.forcedata[event.force.name] = nil --destroy all data related to a force that is about to no longer exist.
end

local function on_forces_merging(event)
    on_force_destroyed({force = event.source})
end

local function on_player_created(event)
    local player = game.players[event.player_index]
    --feels redundent as this also happens at force creation.
    if general.silo == 2 then
        check_spawn_silo(game.players[event.player_index].force)
    end
    library.dump_info()
end

local function on_player_changed_force(event)
    if general.silo == 2 then
        check_despawn_silo(event.force)
        check_spawn_silo(game.players[event.player_index].force)
    end
end

local function on_player_removed(event)
    if general.silo == 2 then
        check_despawn_silo(game.players[event.player_index].force)
    end
end

--Base factorio version, will not detect quality satalites. Is likely to be subject to change with the tech obscurity intergration. Will be left alone for now.
local function on_rocket_launched(event)
    if event.rocket and event.rocket.valid and storage.forcedata[event.rocket.force.name]['victory'] == 0 then
        local satellite_count = 0
        local cargo_pod = event.rocket.cargo_pod
        if cargo_pod then
            satellite_count = cargo_pod.get_item_count("satellite")
        end
        if satellite_count > 0 or general.goal == 0 then
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

local function on_pre_scenario_finished(event)
    if not event.player_won then return end
    for _, force in pairs(general.player_forces) do
        if game.forces[force] then
            storage.forcedata[force]['victory'] = 1
        end
    end
    library.dump_info()
end

local function chain_lookup(table, ...)
    for _, k in ipairs{...} do
        table = table[k]
        if not table then
            return nil
        end
    end
    return table
end

local function on_init()
    storage.forcedata = storage.forcedata or {}
    if general.allow_import_blueprints == false then
        set_permissions()
    end

    -- Fire dummy events for all currently existing forces.
    for name, force in pairs(game.forces) do
        on_force_created({force = force})
    end

    -- Fire dummy events for all currently existing players.
    for index, _ in pairs(game.players) do
        on_player_created({player_index = index})
    end

    --if general.goal == 1 then --only disable when we want satalites, is currently unneeded.
    if remote.interfaces["silo_script"] then
        remote.call("silo_script", "set_no_victory", true)
    end
end

commands.add_command("ap-sync", "Used by the Archipelago client to get progress information", function(call)
    local force
    if call.player_index == nil then
        force = game.forces.player
    else
        force = game.players[call.player_index].force
    end
    local research_done = {}
    local forcedata = chain_lookup(storage, "forcedata", force.name)
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
    rcon.print(helpers.table_to_json({["slot_name"] = general.slot_name, ["seed_name"] = general.seed_name, ["info"] = data_collection}))
end)

commands.add_command("ap-spawn-silo", "Attempts to spawn a silo and cargo landing pad around 0,0", function(call)
    if general.allow_cheats then
        spawn_entity(game.player.surface, game.player.force, "rocket-silo", 0, 0, 80, true, true)
        spawn_entity(game.player.surface, game.player.force, "cargo-landing-pad", 0, 0, 80, true, true)
    end
end)

commands.add_command("ap-rcon-info", "Used by the Archipelago client to get information", function(call)
    rcon.print(helpers.table_to_json({
        ["slot_name"] = general.slot_name,
        ["seed_name"] = general.seed_name,
        ["death_link"] = DEATH_LINK,
        ["energy_link"] = ENERGY_INCREMENT,
        ["local_item_handling"] = general.local_item_handling
    }))
end)

commands.add_command("ap-print", "Used by the Archipelago client to print messages", function (call)
    game.print(call.parameter)
end)

commands.add_command("toggle-ap-send-filter", "Toggle filtering of item sends that get displayed in-game to only those that involve you.", function(call)
    log("Player command toggle-ap-send-filter") -- notifies client
end)

commands.add_command("toggle-ap-chat", "Toggle sending of chat messages from players on the Factorio server to Archipelago.", function(call)
    log("Player command toggle-ap-chat") -- notifies client
end)

local lib = {}
lib.events = {
    [defines.events.on_forces_merging] = on_forces_merging,
    --[defines.events.on_tick] = on_tick,
    --[defines.events.on_research_finished] = on_research_finished,
    [defines.events.on_force_created] = on_force_created,
    [defines.events.on_player_created] = on_player_created,
    [defines.events.on_player_changed_force] = on_player_changed_force,
    [defines.events.on_player_removed] = on_player_removed,

    [defines.events.on_rocket_launched] = on_rocket_launched,
    [defines.events.on_pre_scenario_finished] = on_pre_scenario_finished,
    --[defines.events.on_surface_created] = on_surface_created,
}
lib.on_init = on_init
--lib.on_configuration_changed = on_configuration_changed

return lib