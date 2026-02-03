
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
--hints inbound: AP side
--hints outbound:  AP side

local function send_hint(technology)
    if storage.hinted_techs[technology.name] == false then
        storage.hinted_techs[technology.name] = true

        -- send a hint to the archipelago server here.
        log("Obscurity gives hint for " .. technology.name) -- notifies client

    end
end

local function receive_hint(tech_name)
    -- receive a hint from the achipelago server.
    for name, tech in pairs(prototypes.technology) do
        if name == tech_name then
            for name, force in pairs(game.forces) do
                game.print(serpent.line(force.technologies[tech_name]))
                if prototypes.technology[tech_name].hidden == false then
                    force.technologies[tech_name].visible_when_disabled = true
                    force.technologies[tech_name].enabled = false
                end
            end
        end
    end
end

local function depth_check(force, in_layer)
    
    local technologies = force.technologies

    local in_depth = {} -- start with all already completed techs
    local second_pass = {}
    for _, tech in pairs(technologies) do
        if tech.researched then
            in_depth[tech.name] = true
        end
        local prerequisite = true
        for _, _ in pairs(tech.prerequisites) do
            prerequisite = false
            break
        end
        if prerequisite and tech.prototype.research_trigger == nil then
            second_pass[tech.name] = true
        end
    end

    local to_check = table.deepcopy(in_depth)
    local depth_measure = settings.global["archipelago-tech-depth-obscurity"].value
    local first_round = true
    while depth_measure > 0 do
        depth_measure = depth_measure - 1
        local new_revealed = {}
        if first_round then
            new_revealed = second_pass
            first_round = false
        end
        for name, _ in pairs(to_check) do
            local count = 0
            for _, tech in pairs(technologies[name].prerequisites) do
                count = count + 1
                if (not in_depth[tech.name]) and (not to_check[tech.name]) and in_layer[tech.name] then
                    new_revealed[tech.name] = true
                end
            end
            if count == 0 then new_revealed[name] = true end
            for _, tech in pairs(technologies[name].successors) do
                if (not in_depth[tech.name]) and (not to_check[tech.name]) and in_layer[tech.name] then
                    new_revealed[tech.name] = true
                end
            end
        end

        local nothing_new = true
        for _, _ in pairs(new_revealed) do
            nothing_new = false
            break
        end
        if nothing_new then
            break -- nothing new found. So no need to continue the search.
        end

        --set the next layer of techs at the ready. And mark all other techs for reveal.
        for name, _ in pairs(new_revealed) do
            to_check[name] = true
            in_depth[name] = true
        end
    end

    return in_depth
end

local function layer_check(force)
    
    local technologies = force.technologies
    local science_packs_name = storage.forces[force.name].science_packs_name
    local hidden_science_tech = storage.forces[force.name].hidden_science_tech

    local in_layers

    in_layers = {}
    for name, tech in pairs(technologies) do
        if hidden_science_tech[tech.name] then
            local is_revealed = true
            for _, ingredient in pairs(tech.research_unit_ingredients) do
                if science_packs_name[ingredient.name].crafted == false then
                    is_revealed = false
                end
            end
            if is_revealed then
                in_layers[tech.name] = true
            end
        end
    end

    return in_layers
end

local function update_science_tech_tree(force)
    --update the entire science part of the tech tree. With hidden and not hidden things.
    local technologies = force.technologies
    local hidden_science_tech = storage.forces[force.name].hidden_science_tech

    local to_reveal

    if settings.global["archipelago-tech-layer-obscurity"].value then
        to_reveal = layer_check(force)
    else
        to_reveal = table.deepcopy(hidden_science_tech) or {}
    end
    
    if settings.global["archipelago-tech-depth-obscurity"].value >=1 then
        to_reveal = depth_check(force, to_reveal)
    end

    for name, _ in pairs(to_reveal) do
        send_hint(technologies[name])
        technologies[name].enabled = true
        technologies[name].visible_when_disabled = false
    end

    -- in_layers either contains all still hidden sciences or contains 
end

local function update_trigger_tech_tree(force, technology)
    --update the entire trigger part of the tech tree. With hidden and not hidden things.
    local technologies = force.technologies
    local hidden_trigger_tech = storage.forces[force.name].hidden_trigger_tech
    local triggers = storage.forces[force.name].triggers

    local to_check = {}

    if technology == false then
        for _, tech in pairs(technologies) do
            if tech.researched then
                for _, effect in pairs(tech.prototype.effects) do
                    if effect.type == "unlock-recipe" then
                        local recipe = prototypes.recipe[effect.recipe]
                        for _, item_data in pairs(recipe.products) do
                            to_check[item_data.name] = item_data.name
                        end
                    end
                end
            end
        end
    else
        for _, effect in pairs(technology.prototype.effects) do
            if effect.type == "unlock-recipe" then
                local recipe = prototypes.recipe[effect.recipe]
                for _, item_data in pairs(recipe.products) do
                    to_check[item_data.name] = item_data.name
                end
            end
        end
    end
    for _, name in pairs(to_check) do
        if triggers[name] then 
            if triggers[name].unlocked_triggered == false then
                triggers[name].unlocked_triggered = true
                for _, tech_name in pairs(triggers[to_check].technologies) do
                    hidden_trigger_tech[tech_name] = false
                    force.technologies[tech_name].hidden = false
                    force.technologies[tech_name].disabled = false
                end
            end
        end
    end
end

local function setup_storage(force)
    --setup all the information needed for later
    storage.forces = storage.forces or {}
    storage.forces[force.name] = storage.forces[force] or {}
    storage.forces[force.name].science_packs_num = {} --make a list of science packs.
    storage.forces[force.name].science_packs_name = {} --make a list of science packs.
    storage.forces[force.name].triggers = {} --make a list of all triggers in the game
    storage.forces[force.name].hidden_science_tech = {} --list all the newly hidden science techs
    storage.forces[force.name].hidden_trigger_tech = {} --list all the newly hidden trigger techs

 
    local science_packs_num = storage.forces[force.name].science_packs_num
    local science_packs_name = storage.forces[force.name].science_packs_name
    local triggers = storage.forces[force.name].triggers
    local hidden_science_tech = storage.forces[force.name].hidden_science_tech
    local hidden_trigger_tech = storage.forces[force.name].hidden_trigger_tech

    local done_packs = {}
    local done_triggers = {}

    for name, tech in pairs(game.forces[force.name].technologies) do
        if tech.prototype.hidden == false then
            if tech.prototype.research_trigger == nil and (settings.global["archipelago-tech-layer-obscurity"] or settings.global["archipelago-tech-depth-obscurity"]>=1) then
                hidden_science_tech[tech.name] = true
                for _, packs in pairs(tech.research_unit_ingredients) do
                    if done_packs[packs.name] ~= true then
                        done_packs[packs.name] = true
                        table.insert(science_packs_num, {name = packs.name, crafted = false})
                        science_packs_name[packs.name] = {name = packs.name, crafted = false}
                    end
                end
                tech.enabled = false
            elseif (tech.prototype.research_trigger.type == "craft-item" or tech.prototype.research_trigger.type == "craft-fluid") and settings.global["archipelago-tech-craft-obscurity"] then
                
                local trigger_name
                if tech.prototype.research_trigger.type == "craft-item" then
                    trigger_name = tech.prototype.research_trigger.item
                else
                    trigger_name = tech.prototype.research_trigger.fluid
                end
                
                hidden_trigger_tech[tech.name] = true
                if done_triggers[trigger_name] ~= true then
                    if triggers[trigger_name] == nil then
                        triggers[trigger_name] = {name = trigger_name, unlocked_triggered = false, technologies = {tech.name}}
                    else
                        table.insert(triggers[trigger_name].technologies, tech.name)
                    end
                end
                tech.enabled = false
            end
        end
    end
end

local function get_item_count(item_name, force)
    local count = 0
    for surface_name, surface in pairs(game.surfaces) do
        local flowstatistics = force.get_item_production_statistics(surface)
        count = count + flowstatistics.get_input_count(item_name)
    end
    return count
end

local science_total
local function on_tick(event)
    if not science_total then
        for force_name, force in pairs(game.forces) do
            science_total = 0
            local counter = 0
            for _, _ in pairs(storage.forces[force_name].science_packs_num) do
                counter = counter + 1
            end
            if counter > science_total then
                science_total = counter
            end
        end
    end 
    for force_name, force in pairs(game.forces) do
        local science_check = game.tick % science_total --check one science pack per tick.
        local science_packs_num = storage.forces[force_name].science_packs_num
        if science_packs_num[science_check+1].crafted == false then
            if get_item_count(science_packs_num[science_check+1].name, force) > 0 then --if this science_pack is made then update the three
                -- fix this (steal fomr milestones.)
                game.print("you crafted a: "..science_packs_num[science_check+1].name)
                science_packs_num[science_check+1].crafted = true --ensure one update per pack extra crafted
                storage.forces[force_name].science_packs_name[science_packs_num[science_check+1].name].crafted  = true
                update_science_tech_tree(force)
            end
        end
    end
end


local function on_research_finished(event)
    update_science_tech_tree(event.research.force)
    update_trigger_tech_tree(event.research.force, event.research)
end

local function on_force_created(event)
    setup_storage(event.force)
end

local function on_init()
    storage.hinted_techs = {} --will ensure hints are only send once.
    for name, tech in pairs(prototypes.technology) do
        storage.hinted_techs[name] = tech.hidden
    end
    for _, force in pairs(game.forces) do
        setup_storage(force)
        update_trigger_tech_tree(force, false)
        
        local to_check = {}
        for _, recipe in pairs(prototypes.recipe) do
            if recipe.enabled then
                for _, item_data in pairs(recipe.products) do
                    to_check[item_data.name] = item_data.name
                end
            end
        end
        local hidden_trigger_tech = storage.forces[force.name].hidden_trigger_tech
        local triggers = storage.forces[force.name].triggers
        for _, name in pairs(to_check) do
            if triggers[name] then 
                if triggers[name].unlocked_triggered == false then
                    triggers[name].unlocked_triggered = true
                    for _, tech_name in pairs(triggers[to_check].technologies) do
                        send_hint(force.technologies[tech_name].hidden)
                        hidden_trigger_tech[tech_name] = false
                        force.technologies[tech_name].hidden = false
                        force.technologies[tech_name].disabled = false
                    end
                end
            end
        end
    end
end

local function on_configuration_changed()
    game.print("I see that you have changed your configuration.\n But as I was not asked I am going to ignore anything extra. And probably give errors on removed techs.\n~~the tech obscurity of the archipelago mod")
end

events = {
    [defines.events.on_tick] = on_tick,
    [defines.events.on_research_finished] = on_research_finished,
    [defines.events.on_force_created] = on_force_created,
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
    else
        receive_hint(tech_name) --from the perspective of factorio.
    end
end)

commands.add_command("ap-resend-all-hints", "Used by the Archipelago client to manage the tech tree hints", function(call)
    --sends all hints again, the order will be base factorio sorting.

    storage.hinted_techs = {} --will ensure hints are only send once.
    for name, tech in pairs(prototypes.technology) do
        storage.hinted_techs[name] = tech.hidden
    end
    for _, force in pairs(game.forces) do
        update_science_tech_tree(force)
        update_trigger_tech_tree(force, false)
    end
end)

local lib = {}
lib.get_events = function() return events end
lib.on_init = on_init
lib.on_configuration_changed = on_configuration_changed

return lib