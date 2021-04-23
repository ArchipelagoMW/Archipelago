function filter_ingredients(ingredients, ingredient_filter)
    local new_ingredient_list = {}
    for _, ingredient_table in pairs(ingredients) do
        if ingredient_filter[ingredient_table[1]] then -- name of ingredient_table
            table.insert(new_ingredient_list, ingredient_table)
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