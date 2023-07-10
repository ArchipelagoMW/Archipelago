local socket = require("socket")
local json = require("json")

-- Set to log incoming requests
-- Will cause lag due to large console output
local DEBUG = false

local SOCKET_PORT = 43055

local STATE_NOT_CONNECTED = 0
local STATE_CONNECTED = 1

local client_socket = nil

local current_state = STATE_NOT_CONNECTED

local timeout_timer = 0
local message_timer = 0
local message_interval = 0
local prev_time = 0
local current_time = 0

local locked = false

local rom_hash = nil

local lua_major, lua_minor = _VERSION:match("Lua (%d+)%.(%d+)")
lua_major = tonumber(lua_major)
lua_minor = tonumber(lua_minor)

if lua_major > 5 or (lua_major == 5 and lua_minor >= 3) then
    require("lua_5_3_compat")
end

local bizhawk_version = client.getversion()
local bizhawk_major, bizhawk_minor, bizhawk_patch = bizhawk_version:match("(%d+)%.(%d+)%.?(%d*)")
bizhawk_major = tonumber(bizhawk_major)
bizhawk_minor = tonumber(bizhawk_minor)
if bizhawk_patch == "" then
    bizhawk_patch = 0
else
    bizhawk_patch = tonumber(bizhawk_patch)
end

function queue_push (self, value)
    self[self.right] = value
    self.right = self.right + 1
end

function queue_is_empty (self)
    return self.right == self.left
end

function queue_shift (self)
    value = self[self.left]
    self[self.left] = nil
    self.left = self.left + 1
    return value
end

function new_queue ()
    new_queue = {left = 1, right = 1}
    return setmetatable(new_queue, {__index = {is_empty = queue_is_empty, push = queue_push, shift = queue_shift}})
end

local message_queue = new_queue()

function lock ()
    locked = true
    client_socket:settimeout(2)
end

function unlock ()
    locked = false
    client_socket:settimeout(0)
end

function process_request (req)
    local res = {}
    if req["type"] == "PING" then
        res["type"] = "PONG"
    elseif req["type"] == "SYSTEM" then
        res["type"] = "SYSTEM_RESPONSE"
        res["value"] = emu.getsystemid()
    elseif req["type"] == "HASH" then
        res["type"] = "HASH_RESPONSE"
        res["value"] = rom_hash
    elseif req["type"] == "LOCK" then
        res["type"] = "LOCKED"
        lock()
    elseif req["type"] == "UNLOCK" then
        res["type"] = "UNLOCKED"
        unlock()
    elseif req["type"] == "READ" then
        res["type"] = "READ_RESPONSE"
        res["value"] = memory.read_bytes_as_array(req["address"], req["size"], req["domain"])
    elseif req["type"] == "WRITE" then
        res["type"] = "WRITE_RESPONSE"
        memory.write_bytes_as_array(req["address"], req["value"], req["domain"])
    elseif req["type"] == "DISPLAY_MESSAGE" then
        res["type"] = "DISPLAY_MESSAGE_RESPONSE"
        message_queue:push(req["message"])
    elseif req["type"] == "SET_MESSAGE_INTERVAL" then
        res["type"] = "SET_MESSAGE_INTERVAL_RESPONSE"
        message_interval = req["value"]
    else
        res["type"] = "ERROR"
        res["err"] = "Unknown command: "..req["type"]
    end

    return res
end

-- Receive data from AP client and send message back
function send_receive ()
    local message, err = client_socket:receive()

    -- Handle errors
    if (err == "closed") then
        if (current_state == STATE_CONNECTED) then
            print("Connection to client closed")
        end
        current_state = STATE_NOT_CONNECTED
        return
    elseif (err == "timeout") then
        unlock()
        return
    elseif err ~= nil then
        print(err)
        current_state = STATE_NOT_CONNECTED
        unlock()
        return
    end

    -- Reset timeout timer
    timeout_timer = 5

    -- Process received data
    if DEBUG then
        print("Received Message ["..emu.framecount().."]: "..'"'..message..'"')
    end

    local data = json.decode(message)
    local res = {}
    for i, req in ipairs(data) do
        -- An error is more likely to cause an NLua exception than to return an error here
        local status, response = pcall(process_request, req)
        if (status) then
            res[i] = response
        else
            res[i] = {type = "ERROR", err = response}
        end
    end

    local result, err client_socket:send(json.encode(res).."\n")
end

function main ()
    if (bizhawk_major < 2 or (bizhawk_major == 2 and bizhawk_minor < 7)) then
        print("Must use a version of bizhawk 2.7.0 or higher")
        return
    elseif (bizhawk_major > 2 or (bizhawk_major == 2 and bizhawk_minor > 9)) then
        print("Warning: This version of BizHawk is newer than this script. If it doesn't work, consider downgrading to 2.9.")
    end

    local server, err = socket.bind("localhost", SOCKET_PORT)
    if (err ~= nil) then
        print(err)
        return
    end

    function onexit ()
        server:close()
    end

    event.onexit(onexit)

    local printed_no_rom_message = false
    if (emu.getsystemid() == "NULL") then
        print("No ROM is loaded. Please load a ROM.")
        while (emu.getsystemid() == "NULL") do
            emu.frameadvance()
        end
    end

    rom_hash = gameinfo.getromhash()

    while true do
        current_time = socket.socket.gettime()
        timeout_timer = timeout_timer - (current_time - prev_time)
        message_timer = message_timer - (current_time - prev_time)
        prev_time = current_time

        if (message_timer <= 0 and not message_queue:is_empty()) then
            gui.addmessage(message_queue:shift())
            message_timer = message_interval
        end

        if (current_state == STATE_NOT_CONNECTED) then
            if (emu.framecount() % 60 == 0) then
                print("Waiting for client to connect...")
                emu.frameadvance() -- To flush print message

                server:settimeout(2)
                local client, timeout = server:accept()
                if (timeout == nil) then
                    print("Client connected")
                    current_state = STATE_CONNECTED
                    client_socket = client
                    client_socket:settimeout(0)
                end
            end
        else
            repeat
                send_receive()
            until not locked

            if (timeout_timer <= 0) then
                print("Client timed out")
                current_state = STATE_NOT_CONNECTED
            end
        end

        emu.frameadvance()
    end
end

main()
