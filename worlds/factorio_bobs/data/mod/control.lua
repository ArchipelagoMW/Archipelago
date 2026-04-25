local handler = require("event_handler")

-- used the build in event handler in the core to assigned the events.
local libs = {
    death_link = require("scripts/death_link"), --handles all death link related things.
    energy_link = require("scripts/energy_link"), --handles all energy link related things.
    item_handling = require("scripts/item_handling"), -- handles all AP items, sending, recieving. And samples.
    miscellaneous = require("scripts/miscellaneous"), -- handles most AP related comminucation, and other things like setting perms, rocket silo, and victory.
    --trap_handling = require("scripts/trap_handling.lua"), --does not yet exist
    tech_obscurity = require("scripts/tech_obscurity.lua"), --I am hopefull. But first getting this refactoring approved before adding this shit.
    trap_handling = require("scripts/trap_handling.lua"), --does not yet exist
    --main = require("scripts/main.lua"), --will probably be removed.
    --tech_obscurity = require("scripts/tech-obscurity.lua"), --I am hopefull. But first getting this refactoring approved before adding this shit.
    control = {} --for all events that get compiled in this file.
}

-- was split up in on_player_died and on_entity_died

--local on_entity_died_filter = {}
--local on_entity_died_functions = {}
--for name, lib in pairs(libs) do
--    if lib.on_entity_died then
--        for filter, name in pairs(lib.on_entity_died) do
--            table.insert(on_entity_died_filter, {filter = filter, [filter] = name, mode = "or"})
--        end
--        on_entity_died_functions[name] = lib.on_entity_died_function
--    end
--end
--
--local function on_entity_died(event)
--    log("running the control.lua on_entity_died for "..serpent.line(event.entity))
--    game.print("running the control.lua on_entity_died "..serpent.line(event.entity))
--    for _, action in pairs(on_entity_died_functions) do
--        action(event)
--    end
--end

--libs.control.filtered_events = {on_entity_died = {on_entity_died, on_entity_died_filter}}

local dupes = false
local all_events = {}
local filtered_events = {}
for name, lib in pairs(libs) do
    handler.add_lib(lib)
    if lib.filtered_events then
        for event, data in pairs(lib.filtered_events) do
            script.on_event(event, data[1], data[2]) --register events with filter.
            if all_events[event] then
                dupes = true
            end
            all_events[event] = true
            filtered_events[event] = true
        end
    end
    if lib.events then
        for event, data in pairs(lib.events) do
            if filtered_events[event] then
                dupes = true
            end
            all_events[event] = true
        end
    end
end


if dupes then
    local error_message = ""
    for name, lib in pairs(libs) do
        if lib.filtered_events then
            --test to see if an filtered event has a duplicate.
            for no_dupe, error_handling in pairs(libs) do
                if error_handling.events then
                    for testing, _ in pairs(error_handling.events) do
                        if testing == event then
                            error_message = error_message..event.." from "..name.." has a duplicate normal event in "..no_dupe..".\n"
                        end
                    end
                end
                if no_dupe ~= name and error_handling.filtered_events then
                    for testing, _ in pairs(error_handling.filtered_events) do
                        if testing == event then
                            error_message = error_message..event.." from "..name.." has a duplicate filtered event in "..no_dupe..".\n"
                        end
                    end
                end
            end
        end
    end
    if error_message ~= "" then
        error(error_message)
    end
end
