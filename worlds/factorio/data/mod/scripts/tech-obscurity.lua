
-- assumptions:
-- all the techs that need to be obscured are still show when the game loads into the world.
--      the on_init in this file needs it to know what techs need to be relevealed at some point.
--      As well as what techs need to hide permanently
-- trigger techs have no prerequisites.
-- inbound hints will result in the tech in question to be revealed as set to a disabled tech
--      disabled techs will be enabled when the tech tree reaches/reveal that tech.
--      Meaning that when the tech becomes in range/achievable it should become a normal tech again. 
-- out bound hints will reveal a techs when they are visable to atleast one player.
--      if you are playing with two forces (for whatever reason) only one needs to know where the tech is for the hint to be send.
--      hints will only be send once. Unless an achipelago command demands the whole list.

--to do:
--depth: functions settings and AP side
--hints inbound: command and AP side
--hints outbound:  AP side
--tech tree trigger: functions

local function send_hint(technology)
    if storage.hinted_techs[technology.name] == false then
        storage.hinted_techs[technology.name] = true

        -- send a hint to the archipelago server here.
        log("Player gives hint for:"+technology.name) -- notifies client

    end
end

local function depth_check(technology)
    -- checks if the tech is close enough in depth to another tech.
    -- so that you only reveal techs when you are only one or two layers away from it.
    -- might be more fun and hints will be more spread out.

    return true --currently this check does not work.
end

local function receive_hint(tech_name)
    -- receive a hint from the achipelago server.
    for name, tech in pairs(technologies) do--fix this
        if name == tech_name then
            for name, force in pairs(forces) do --fix this
                if force.technology[tech_name].hidden then --fix this
                    force.technology[tech_name].hidden = false --fix this
                    force.technology[tech_name].disabled = true --fix this
                end
            end
        end
    end
end

local function update_science_tech_tree(force)
    --update the entire science part of the tech tree. With hidden and not hidden things.
    technologies = game.forces[force].technologies --fix this
    hidden_science_tech = storage[force.name].hidden_science_tech
    science_packs = storage[force.name].science_packs

    for name, tech in pairs(technologies) do
        if hidden_science_tech[tech.name] then
            is_revealed = true
            for _, ingredient in tech.ingredients do
                if science_packs[ingredient[0]].crafted == false then
                    is_revealed = false
                end
            end
            if is_revealed or setting_layer_obscurity == false then -- fix this
                if depth_check(tech) then
                    send_hint (tech)
                    tech.hidden = false
                    tech.disabled = false
                end
            end
        end
    end
end

local function update_trigger_tech_tree(force, technology)
    --update the entire trigger part of the tech tree. With hidden and not hidden things.
    technologies = game.forces[force].technologies --fix this
    hidden_trigger_tech = storage[force.name].hidden_trigger_tech
    triggers = storage[force.name].triggers

    to_check = {}
    for _, recipe in pairs(technology.unlocks) do --fix this mainly, check recipe structures in runtime.
        if recipe.result then
            to_check[recipe.result] = recipe.result
        end
        for name, result in pairs(recipe.results) do
            to_check[name] = name
        end
    end
    for _ name in pairs(to_check) do
        if triggers[to_check] then
            
        end
    end
end

local function setup_storage(force)
    --setup all the information needed for later
    storage[force.name].science_packs = {} --make a list of science packs.
    storage[force.name].triggers = {} --make a list of all triggers in the game
    storage[force.name].hidden_science_tech = {} --list all the newly hidden science techs
    storage[force.name].hidden_crafting_tech = {} --list all the newly hidden trigger techs

    science_packs = storage[force.name].science_packs
    triggers = storage[force.name].triggers
    hidden_science_tech = storage[force.name].hidden_science_tech
    hidden_crafting_tech = storage[force.name].hidden_crafting_tech

    done_packs = {}
    done_triggers = {}
    
    for name, tech in pairs(force.technologies) do --fix this
        if tech is research do --fix this
            hidden_science_tech[tech.name] = true
            for _, packs in pairs(tech.ingredients) do
                if done_packs[packs[0]] ~= true then
                    science_packs[packs[0]] = {name = packs[0], science = true, crafted = false}
                end
            end
        end
        if tech is trigger do  --fix this
            hidden_trigger_tech[tech.name] = true
            for _, items in pairs(tech.ingredients) do
                if done_triggers[triggers[0]] ~= true then
                    if triggers[items[0]] == null then
                        triggers[items[0]] = {name = items[0], unlocked_triggered = false, technologies = {tech.name}}
                    else
                        triggers[items[0]].technologies --finish this
                    end
                end
            end
        end
    end
end

local function on_tick(event)
    for force_name, force in pairs(game.forces) do
        science_num = game.tick % len(storage[force_name].science_packs)
        science_check = storage[force_name].science_packs[science_num] --check one science pack per tick.

        if storage[force_name].science_packs.crafted == false then
            if sience_pack_production > 0 then --if this science_pack is made then update the three
                -- fix this (steal fomr milestones.)
                storage[force_name].science_packs.crafted = true --ensure one update per pack extra crafted
                update_science_tech_tree(force)
            end
        end
    end
end

local function on_research_finished(event)
    update_science_tech_tree(event.force)
    update_trigger_tech_tree(event.force, event.technology) --verify this
end

local function on_force_created(event)
    setup_storage(event.force)
end

local function on_init()
    storage.hinted_techs = {} --will ensure hints are only send once.
    for name, tech in pairs(technologies) do --fix this
        storage.hinted_techs[name] = tech.hidden
    end
    for _, force in pairs(forces) do --fix this
        setup_storage(force)
    end
end

local function on_configuration_changed()
    game.print("I see that you have changed your configuration.\n But as I was not asked I am going to ignore anything extra. And probably give errors on removed techs.\n~~the tech obscurity of the archipelago mod")
end

local events = {
    [defines.on_tick] = on_tick,
    [defines.on_research_finished] = on_research_finished,
    [defines.on_force_created] = on_force_created,
}

for name, loc_fun in pairs(events) do
    script.on_event(name, loc_fun)
end

script.on_init(on_init)
script.on_configuration_changed(on_configuration_changed)

commands.add_command("ap-receive-hint", "Used by the Archipelago client to manage the tech tree hints", function(call)

    tech_name = call.parameter or "failed"
    if tech_name == "failed" then --take care of errors
        log("failure has occured")
        game.print("a failure with recieving a hint has occured")
    end

    -- give hint to all forces
    for name, force in pairs(forces) do --fix this
        if storage[force.name].hidden_science_tech[tech_name] then
            --is hinted so no longer hidden but disabled.
            force.technologies[tech_name].hidden = false
            force.technologies[tech_name].disabled = true
        end
        if storage[force.name].hidden_trigger_tech[tech_name] then
            --is hinted so no longer hidden but disabled.
            force.technologies[tech_name].hidden = false
            force.technologies[tech_name].disabled = true
        end
    end

end)
