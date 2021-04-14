require "lib"
script.on_event(defines.events.on_player_created, function(event)
    local player = game.players[event.player_index]
    player.force.research_queue_enabled = true
    {% if free_samples %}
    player.insert({count=19, name="burner-mining-drill"})
    player.insert({count=19, name="stone-furnace"})
    {% endif %}
end)

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
    local research_done = {}
    local data_collection = {["research_done"] = research_done}

    for tech_name, tech in pairs(force.technologies) do
        if tech.researched and string.find(tech_name, "ap-") == 1 then
            research_done[tech_name] = tech.researched
        end
    end
    game.write_file("ap_bridge.json", game.table_to_json(data_collection), false)
    -- game.write_file("research_done.json", game.table_to_json(data_collection), false, 0)
    -- game.print("Sent progress to Archipelago.")
end



-- add / commands

commands.add_command("ap-sync", "Run manual Research Sync with Archipelago.", function(call)
    dumpTech(game.players[call.player_index].force)
    game.print("Wrote bridge file.")
end)

commands.add_command("ap-get-technology", "Grant a technology, used by the Archipelago Client.", function(call)
    local force = game.forces["player"]
    chunks = {}
    for substring in call.parameter:gmatch("%S+") do -- split on " "
        table.insert(chunks, substring)
    end
    local tech_name = chunks[1]
    local source = chunks[2] or "Archipelago"
    local tech = force.technologies[tech_name]
    if tech ~= nil then
        if tech.researched ~= true then
            tech.researched = true
            game.print({"", "Received ", tech.localised_name, " from ", source})
            game.play_sound({path="utility/research_completed"})
        end
    else
        game.print("Unknown Technology " .. tech_name)
    end
end)