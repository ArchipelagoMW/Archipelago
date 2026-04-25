
local general = require("Archipelago/general")
local library = {}

function library.get_any_stack_size (name)
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
function library.split (s, sep)
    local fields = {}

    sep = sep or " "
    local pattern = string.format("([^%s]+)", sep)
    string.gsub(s, pattern, function(c) fields[#fields + 1] = c end)

    return fields
end

local last_dump = 0
function library.dump_info()
    if last_dump == game.tick then return end --prevent multiple calls in the same game tick.
    log("Archipelago Bridge Data available for game tick ".. game.tick .. ".") -- notifies client
    last_dump = game.tick
end

function library.string_starts_with(str, start)
    return str:sub(1, #start) == start
end

function library.is_valid_ap_force(force)
    for _, force_name in pairs(general.player_forces) do
        if force.name == force_name then
            return true
        end
    end
    return false
end

function library.get_all_ap_forces()
    local forces = game.forces
    local return_forces = {}
    for _, force_name in pairs(general.player_forces) do
        if forces[force_name] then
            table.insert(return_forces, forces[force_name])
        end
    end
    return return_forces
end

return library
