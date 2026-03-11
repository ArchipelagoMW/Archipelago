local handler = require("event_handler")

-- used the build in event handler in the core to assigned the events.
local libs = {
    death_link = require("scripts/death_link"),
    energy_link = require("scripts/energy_link"),
    item_handling = require("scripts/item_handling"),
    --trap_handling = require("scripts/trap_handling.lua"), --does not yet exist
    --main = require("scripts/main.lua"), --will probably be removed.
    --tech_obscurity = require("scripts/tech-obscurity.lua"), --I am hopefull. But first getting this refactoring approved before adding this shit.
}

local error_message = nil
for name, lib in pairs(libs) do
    handler.add_lib(lib)
    if lib.filtered_events then
        for event, data in pairs(lib.filtered_events) do
            script.on_event(event, data[1], data[2]) --register events with filter.

            --test to see if an filtered event has a duplicate.
            for no_dupe, error_handling in pairs(libs) do
                for testing, _ in pairs(error_handling.events) do
                    if testing == event then
                        error_message = error_message..event.." from "..name.." has a duplicate normal event in "..no_dupe..".\n"
                    end
                end
                if no_dupe ~= name then
                    for testing, _ in pairs(error_handling.filtered_events) do
                        if testing == event then
                            error_message = error_message..event.." from "..name.." has a duplicate filtered event in "..no_dupe..".\n"
                        end
                    end
                end
            end
            --end of testing for duplicates.
        end
    end
end
if error_message ~= nil then
    error(error_message)
end
