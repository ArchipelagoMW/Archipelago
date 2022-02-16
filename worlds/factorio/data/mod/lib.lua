function filter_ingredients(ingredients, ingredient_filter)
    local new_ingredient_list = {}
    for _, ingredient_table in pairs(ingredients) do
        if ingredient_filter[ingredient_table[1]] then -- name of ingredient_table
            table.insert(new_ingredient_list, ingredient_table)
        end
    end

    return new_ingredient_list
end

function add_ingredients(ingredients, added_ingredients)
    local new_ingredient_list = table.deepcopy(ingredients)
    for new_ingredient, count in pairs(added_ingredients) do
        local found = false
        for _, old_ingredient in pairs(ingredients) do
            if old_ingredient[1] == new_ingredient then
                found = true
                break
            end
        end
        if not found then
            table.insert(new_ingredient_list, {new_ingredient, count})
        end
    end

    return new_ingredient_list
end

function get_any_stack_size(name)
    local item = game.item_prototypes[name]
    if item ~= nil then
        return item.stack_size
    end
    item = game.equipment_prototypes[name]
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