require "lib"
-- for testing
script.on_event(defines.events.on_tick, function(event)
    if event.tick%600 == 0 then
        dumpTech(game.forces["player"])
    end
end)

-- hook into researches done
script.on_event(defines.events.on_research_finished, function(event)
    local technology = event.research
    dumpTech(technology.force)
    {% if free_samples %}
    local players = technology.force.players
    if technology.effects then
        for _, effect in pairs(technology.effects) do
            if effect.type == "unlock-recipe" then
                local recipe = game.recipe_prototypes[effect.recipe]
                for _, result in pairs(recipe.products) do
                    if result.type == "item" and result.amount then
                        {% if free_samples == 1 %}
                        local new = {count=result.amount, name=result.name}
                        {% elif free_samples == 2 %}
                        local new = {count=get_any_stack_size(result.name) * 0.5, name=result.name}
                        {% else %}
                        local new = {count=get_any_stack_size(result.name), name=result.name}
                        {% endif %}
                        for _, player in pairs(players) do
                            player.insert(new)
                        end
                    end
                end
            end
        end
    end
    {% endif %}

end)

function dumpTech(force)
    local data_collection = {}
    for tech_name, tech in pairs(force.technologies) do
        if tech.researched and string.find(tech_name, "ap-") == 1 then
            data_collection[tech_name] = tech.researched
        end
    end
    game.write_file("research_done.json", game.table_to_json(data_collection), false)
    -- game.write_file("research_done.json", game.table_to_json(data_collection), false, 0)
    -- game.print("Sent progress to Archipelago.")
end

function dumpGameInfo()
    -- dump Game Information that the Archipelago Randomizer needs.
    local data_collection = {}
    local force = game.forces["player"]
    for tech_name, tech in pairs(force.technologies) do
        if tech.enabled and tech.research_unit_count_formula == nil then
            local tech_data = {}
            local unlocks = {}
            tech_data["unlocks"] = unlocks
            local requires = {}
            tech_data["requires"] = requires
            local ingredients = {}
            tech_data["ingredients"] = ingredients
            for tech_requirement, _ in pairs(tech.prerequisites) do
                table.insert(requires, tech_requirement)
            end
            for _, modifier in pairs(tech.effects) do
                if modifier.type == "unlock-recipe" then
                    table.insert(unlocks, modifier.recipe)
                end
            end
            for _, ingredient in pairs(tech.research_unit_ingredients) do
                table.insert(ingredients, ingredient.name)
            end
            data_collection[tech_name] = tech_data

        end
        game.write_file("techs.json", game.table_to_json(data_collection), false)
        game.print("Exported Tech Data")
    end
    data_collection = {}
    for recipe_name, recipe in pairs(force.recipes) do
        local recipe_data = {}
        recipe_data["ingredients"] = {}
        recipe_data["products"] = {}
        recipe_data["category"] = recipe.category
        for _, ingredient in pairs(recipe.ingredients) do
            table.insert(recipe_data["ingredients"], ingredient.name)
        end
        for _, product in pairs(recipe.products) do
            table.insert(recipe_data["products"], product.name)
        end
        data_collection[recipe_name] = recipe_data
    end
    game.write_file("recipes.json", game.table_to_json(data_collection), false)
    game.print("Exported Recipe Data")
    -- data.raw can't be accessed from control.lua, need to find a better method
    -- data_collection = {}
    -- for machine_name, machine in pairs(data.raw["assembling_machine"]) do
    --     local machine_data = {}
    --     machine_data["categories"] = table.deepcopy(machine.crafting_categories)
    --     data_collection[machine.name] = machine_data
    -- end
    -- game.write_file("machines.json", game.table_to_json(data_collection), false)
    -- game.print("Exported Machine Data")
end

-- add / commands

commands.add_command("ap-get-info-dump", "Dump Game Info, used by Archipelago.", function(call)
    dumpGameInfo()
end)

commands.add_command("ap-sync", "Run manual Research Sync with Archipelago.", function(call)
    dumpTech()
end)

commands.add_command("ap-get-technology", "Grant a technology, used by the Archipelago Client.", function(call)
    local force = game.forces["player"]
    local tech_name = call.parameter
    local tech = force.technologies[tech_name]
    if tech ~= nil then
        if tech.researched ~= true then
            tech.researched = true
            game.print({"", "Received ", tech.localised_name, " from Archipelago"})
            game.play_sound({path="utility/research_completed"})
        end
    else
        game.print("Unknown Technology " .. tech_name)
    end
end)