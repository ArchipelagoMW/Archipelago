

local handler = require("event_handler")

-- used the build in event handler in the core to assigned the events.
handler.add_lib(require("scripts/tech-obscurity.lua"))
handler.add_lib(require("scripts/main.lua"))
