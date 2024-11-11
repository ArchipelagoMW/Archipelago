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
    for _, player in ipairs(game.forces["player"].players) do
        current_character = player.character
        if current_character ~= nil then
            current_character.surface.create_entity{name=entity_name,
                position=random_offset_position(current_character.position, 128),
                target=current_character, speed=speed}
        end
    end
end
