
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
--hints inbound: AP side
--hints outbound:  AP side

local function send_hint(technology)
    if storage.hinted_techs[technology.name] == false then
        storage.hinted_techs[technology.name] = true

        -- send a hint to the archipelago server here.
        log("Obscurity gives hint for:" .. technology.name) -- notifies client

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

local function depth_check(technology)
    -- checks if the tech is close enough in depth to another tech.
    -- so that you only reveal techs when you are only one or two layers away from it.
    -- might be more fun and hints will be more spread out.

    return true --currently this check does not work.
end

local function update_science_tech_tree(force)
    --update the entire science part of the tech tree. With hidden and not hidden things.
    technologies = force.technologies --fix this
    hidden_science_tech = storage.forces[force.name].hidden_science_tech
    science_packs_name = storage.forces[force.name].science_packs_name

    for name, tech in pairs(technologies) do
        if hidden_science_tech[tech.name] then
            is_revealed = true
            for _, ingredient in pairs(tech.research_unit_ingredients) do
                if science_packs_name[ingredient.name].crafted == false then
                    is_revealed = false
                end
            end
            if is_revealed or settings.global["archipelago-tech-layer-obscurity"] == false then -- fix this
                if depth_check(tech) then
                    send_hint (tech)
                    tech.enabled = true
                    tech.visible_when_disabled = false
                end
            end
        end
    end
end

local function update_trigger_tech_tree(force, technology)
    --update the entire trigger part of the tech tree. With hidden and not hidden things.
    local technologies = game.forces[force].technologies --fix this
    local hidden_trigger_tech = storage.forces[force.name].hidden_trigger_tech
    local triggers = storage.forces[force.name].triggers

    local to_check = {}
    for _, recipe in pairs(technology.unlocks) do --fix this mainly, check recipe structures in runtime.
        if recipe.result then
            to_check[recipe.result] = recipe.result
        end
        for name, result in pairs(recipe.results) do
            to_check[name] = name
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
                hidden_trigger_tech[tech.name] = true
                if done_triggers[tech.prototype.research_trigger.name] ~= true then
                    if triggers[tech.prototype.research_trigger.name] == nil then
                        triggers[tech.prototype.research_trigger.name] = {name = tech.prototype.research_trigger.name, unlocked_triggered = false, technologies = {tech.name}}
                    else
                        table.insert(triggers[tech.prototype.research_trigger.name].technologies, tech.name)
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
    update_science_tech_tree(event.force)
    update_trigger_tech_tree(event.force, event.technology) --verify this
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

local lib = {}
lib.get_events = function() return events end
lib.on_init = on_init
lib.on_configuration_changed = on_configuration_changed

return lib