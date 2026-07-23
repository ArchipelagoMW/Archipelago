
--re organized the file; at the top are local functions. At the bottom are functions in the lib.
--This flows better with the best practices I know of factorio mod dev.

local function random_offset_position(position, offset)
    return {x=position.x+math.random(-offset, offset), y=position.y+math.random(-offset, offset)}
end


local lib = {}

lib.get_any_stack_size = function (name)
    local item = prototypes.item[name]
    if item ~= nil then
        return item.stack_size
    end
    item = prototypes.equipment[name]
    if item ~= nil then
        return item.stack_size
    end
    -- failsafe
    return 1
end

-- from https://stackoverflow.com/a/40180465
-- split("a,b,c", ",") => {"a", "b", "c"}
lib.split = function (s, sep)
    local fields = {}

    sep = sep or " "
    local pattern = string.format("([^%s]+)", sep)
    string.gsub(s, pattern, function(c) fields[#fields + 1] = c end)

    return fields
end



lib.fire_entity_at_entities = function(entity_name, entities, speed)
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


lib.fire_entity_at_players = function(entity_name, speed)
    local entities = {}
    for _, player in ipairs(game.forces["player"].players) do
        if player.character ~= nil then
            table.insert(entities, player.character)
        end
    end
    return lib.fire_entity_at_entities(entity_name, entities, speed)
end



local teleport_requests = {}
local teleport_attempts = {}
local max_attempts = 100

lib.attempt_teleport_player = function(player, attempt)
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
        lib.attempt_teleport_player(player, attempt + 1)
    end
end

lib.handle_teleport_attempt = function(event)
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

            lib.attempt_teleport_player(player, nil)
            break
        end
    end
end


lib.spill_character_inventory = function(character)
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

return lib
