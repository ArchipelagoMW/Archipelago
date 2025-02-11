function get_any_stack_size(name)
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
function split(s, sep)
    local fields = {}

    sep = sep or " "
    local pattern = string.format("([^%s]+)", sep)
    string.gsub(s, pattern, function(c) fields[#fields + 1] = c end)

    return fields
end

function random_offset_position(position, offset)
    return {x=position.x+math.random(-offset, offset), y=position.y+math.random(-offset, offset)}
end

function fire_entity_at_players(entity_name, speed)
    local entities = {}
    for _, player in ipairs(game.forces["player"].players) do
        if player.character ~= nil then
            table.insert(entities, player.character)
        end
    end
    return fire_entity_at_entities(entity_name, entities, speed)
end

function fire_entity_at_entities(entity_name, entities, speed)
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

function spill_character_inventory(character)
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
