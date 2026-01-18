

local function is_perma_hidden (technology)
    -- determain if a technology should be revealed
    --if string.find(technology.name, "ap%-") == 1 then -- unsure on how I wanna make this work.
    --    return false
    --end
    return false
end

local function send_hint(technology)
    -- send a hint to the archipelago server.
end

local function on_tick(event)
    for force_name, storage_force_force in pairs(game.forces) do
        if game.tick % 10 == 6 then
        
        end
    end
end

local function setup_storage()
    storage.science_packs = {}
    storage.on_craft = {}
    
end

local function on_init()
    setup_storage()
end

local function on_configuration_changed()

end

local events = {
    [defines.on_tick] = on_tick,
    [defines.on_research_finished] = on_research_finished,
    [defines.] = on_research_finished,
}

for name, loc_fun in pairs(events) do
    script.on_event(name, loc_fun)
end

script.on_init(on_init)
script.on_configuration_changed(on_configuration_changed)