local DEBUG = false

local function log_info(message)
    print("[KirbyAM Connector] " .. message)
end

local function log_debug(message)
    if DEBUG then
        print("[KirbyAM Connector][debug] " .. message)
    end
end

local function current_script_dir()
    local source = debug.getinfo(1, "S").source
    if source:sub(1, 1) == "@" then
        source = source:sub(2)
    end
    return source:match("^(.*[\\/])") or ""
end

local function validate_environment()
    local system = emu.getsystemid()
    if system == "NULL" then
        log_info("No ROM appears to be loaded. Load Kirby & The Amazing Mirror and rerun this script.")
        return false
    end

    if system ~= "GBA" then
        log_info("Expected GBA system, got " .. tostring(system) .. ". Load Kirby & The Amazing Mirror and rerun this script.")
        return false
    end

    local rom_name = gameinfo.getromname()
    if rom_name == nil or rom_name == "" then
        log_info("No ROM appears to be loaded. Load Kirby & The Amazing Mirror and rerun this script.")
        return false
    end

    local lower_name = string.lower(rom_name)
    if string.find(lower_name, "kirby", 1, true) == nil or string.find(lower_name, "amazing mirror", 1, true) == nil then
        log_info("Loaded ROM does not look like Kirby & The Amazing Mirror: " .. rom_name)
        return false
    end

    log_info("ROM validation OK: " .. rom_name)
    return true
end

local function location_polling_hook()
    -- TODO(issue 51): KirbyAM-specific location polling/debug hooks can be inserted here
    -- without forking the generic BizHawk transport contract.
end

local function item_delivery_hook()
    -- TODO(issue 51): KirbyAM-specific item delivery/debug hooks can be inserted here
    -- without changing request/response framing.
end

local function message_helper_hook()
    -- TODO(issue 51): Optional in-emulator message/display helpers can be added here.
end

if not validate_environment() then
    return
end

location_polling_hook()
item_delivery_hook()
message_helper_hook()

local script_dir = current_script_dir()
local generic_connector_path = script_dir .. "connector_bizhawk_generic.lua"

log_debug("Delegating to generic connector at " .. generic_connector_path)
log_info("Starting generic BizHawk transport bridge for KirbyAM.")

local connector_chunk, load_error = loadfile(generic_connector_path)
if connector_chunk == nil then
    log_info("Failed to load generic connector: " .. tostring(load_error))
    return
end

connector_chunk()