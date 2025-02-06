--[[
This is a beta version of a connector script that will allow mGBA to
communicate with Archipelago's BizHawk Client (yes, the name, I know).

Requires mGBA version 0.10.0 or newer.

Place it in the same directory as the normal BizHawk connector
(`Archipelago/data/lua/`). Open your ROM in mGBA, and open
`Tools > Scripting...` in the menus. Then `File > Load script...` in the new
Scripting window and select this file.

Everything should now work just as it does with BizHawk with one exception:

You can only have one instance of mGBA running this script at a time.

Multiple instances of mGBA won't detect each other and will attempt to
communicate over the same port. So you won't be able to have more than one
game connected at a time through mGBA. Still looking for a solution.
]]

local SCRIPT_VERSION = 1
local DEBUG = false

--[[
Copyright (c) 2023-2024 Zunawe

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
]]

local base64 = require("base64")
local json = require("json")

local SOCKET_PORT_FIRST = 43055
local SOCKET_PORT_RANGE_SIZE = 5
local SOCKET_PORT_LAST = SOCKET_PORT_FIRST + SOCKET_PORT_RANGE_SIZE

local STATE_NOT_CONNECTED = 0
local STATE_CONNECTED = 1

local current_state = STATE_NOT_CONNECTED

local message_buffer = console:createBuffer("Archipelago Connector")

local server = nil
local client = nil

local last_activity

local locked = false
local platform = nil
local memory_domains = nil

function lock()
    locked = true
end

function unlock()
    locked = false
end

request_handlers = {
    ["PING"] = function (req)
        return {
            ["type"] = "PONG",
        }
    end,

    ["SYSTEM"] = function (req)
        local res = {
            ["type"] = "SYSTEM_RESPONSE",
        }

        if emu:platform() == C.PLATFORM.GB then
            if emu.memory.cart0:read8(0x143) == 0xC0 then
                res["value"] = "GBC"
            else
                res["value"] = "GB"
            end
        elseif emu:platform() == C.PLATFORM.GBA then
            res["value"] = "GBA"
        end

        return res
    end,

    ["PREFERRED_CORES"] = function (req)
        return {
            ["type"] = "PREFERRED_CORES_RESPONSE",
            ["value"] = {},
        }
    end,

    ["HASH"] = function (req)
        local checksum = 0
        for i, v in ipairs({emu:checksum(C.CHECKSUM.CRC32):byte(1, 4)}) do
            checksum = checksum * 256 + v
        end

        return {
            ["type"] = "HASH_RESPONSE",
            ["value"] = string.format("%x", checksum),
        }
    end,

    ["MEMORY_SIZE"] = function (req)
        local res = {}

        res["type"] = "MEMORY_SIZE_RESPONSE"
        res["value"] = memory_domains[req["domain"]]:bound() - memory_domains[req["domain"]]:base()

        return res
    end,

    ["GUARD"] = function (req)
        local expected_data = base64.decode(req["expected_data"])

        local s = memory_domains[req["domain"]]:readRange(req["address"], #expected_data)
        local actual_data = {}
        for i = 1, #s do
            actual_data[i] = s:byte(i)
        end

        local data_is_validated = true
        for i, byte in ipairs(actual_data) do
            if byte ~= expected_data[i] then
                data_is_validated = false
                break
            end
        end

        return {
            ["type"] = "GUARD_RESPONSE",
            ["address"] = req["address"],
            ["value"] = data_is_validated,
        }
    end,

    ["LOCK"] = function (req)
        lock()

        return {
            ["type"] = "LOCKED",
        }
    end,

    ["UNLOCK"] = function (req)
        unlock()

        return {
            ["type"] = "UNLOCKED",
        }
    end,

    ["READ"] = function (req)
        local s = memory_domains[req["domain"]]:readRange(req["address"], req["size"])
        local d = {}
        for i = 1, #s do
            d[i] = s:byte(i)
        end

        return {
            ["type"] = "READ_RESPONSE",
            ["value"] = base64.encode(d),
        }
    end,

    ["WRITE"] = function (req)
        for i, byte in ipairs(base64.decode(req["value"])) do
            memory_domains[req["domain"]]:write8(req["address"] + (i - 1), byte)
        end

        return {
            ["type"] = "WRITE_RESPONSE",
        }
    end,

    ["DISPLAY_MESSAGE"] = function (req)
        message_buffer:print(req["message"].."\n")

        return {
            ["type"] = "DISPLAY_MESSAGE_RESPONSE",
        }
    end,

    ["default"] = function (req)
        return {
            ["type"] = "ERROR",
            ["err"] = "Unknown command: "..req["type"],
        }
    end,
}

function process_request (req)
    if request_handlers[req["type"]] then
        local success, res = pcall(request_handlers[req["type"]], req)

        if not success then
            res = {
                ["type"] = "ERROR",
                ["err"] = res
            }
        end

        return res
    else
        return request_handlers["default"](req)
    end
end

function received()
    local buffer = ""

    if not client then return end

    while true do
        local piece, err = client:receive(1024)
        if piece then
            buffer = buffer..piece
        else
            if err ~= socket.ERRORS.AGAIN then
                client:close()
            end

            break
        end
    end

    last_activity = os.time()

    for line in string.gmatch(buffer, "[^\n]+") do
        if DEBUG then
            console:log("Received: "..line)
        end

        if line == "VERSION" then
            if DEBUG then
                console:log("Response: "..tostring(SCRIPT_VERSION))
            end

            client:send(tostring(SCRIPT_VERSION).."\n")
        else
            local res = {}
            local data = json.decode(line)
            local failed_guard_response = nil
            for i, req in ipairs(data) do
                if failed_guard_response ~= nil then
                    res[i] = failed_guard_response
                else
                    res[i] = process_request(req)
                    if res[i]["type"] == "GUARD_RESPONSE" and not res[i]["value"] then
                        failed_guard_response = res[i]
                    end
                end
            end

            if DEBUG then
                console:log("Response: "..json.encode(res))
            end

            client:send(json.encode(res).."\n")
        end
    end
end

function error()
    client = nil
    console:log("Client disconnected")
end

function accept()
    console:log("")  -- Black Magic: Printing something here allows recovery from a timeout due to last_activity.
                     -- Removing this causes a timeout to be unrecoverable. The client never appears to connect.

    local err = nil
    local data = nil

    if client == nil then
        client, err = server:accept()
        if err then
            console:error(err)
            return
        end
        console:log("Connected")

        client:add("received", received)
        client:add("error", function() error() end)

        server:close()
        server = nil
    end
end

function tick()
    if platform ~= emu:platform() then
        platform = emu:platform()

        if platform == C.PLATFORM.GB then
            memory_domains = {
                ["ROM"] = emu.memory.cart0,
                ["VRAM"] = emu.memory.vram,
                ["SRAM"] = emu.memory.sram,
                ["WRAM"] = emu.memory.wram,
                ["OAM"] = emu.memory.oam,
                ["IO"] = emu.memory.io,
                ["HRAM"] = emu.memory.hram,
                ["System Bus"] = emu
            }
        else
            memory_domains = {
                ["BIOS"] = emu.memory.bios,
                ["ROM"] = emu.memory.cart0,
                ["EWRAM"] = emu.memory.wram,
                ["IWRAM"] = emu.memory.iwram,
                ["VRAM"] = emu.memory.vram,
                ["OAM"] = emu.memory.oam,
                ["Combined WRAM"] = emu.memory.wram,
                ["System Bus"] = emu,
                -- ["SRAM"] = emu.memory.cart0,
                -- ["PALRAM"] = emu.memory.cart0,
            }
        end
    end

    if client == nil then
        if server == nil then
            create_server()
        end
    else
        if last_activity ~= nil and os.time() - last_activity > 5 then
            console:log("Client timed out")
            client:close()
            client = nil
            last_activity = nil
        else
            while locked do
                client:poll()
            end
        end
    end
end

function create_server()
    local result, err

    server, err = socket.tcp()
    if err then
        console:log(err)
    end

    local port = SOCKET_PORT_FIRST

    while result == nil and port <= SOCKET_PORT_LAST do
        result, err = server:bind("127.0.0.1", port)

        if result == nil then  -- Two instances of mGBA don't conflict in this way. Unsure how to solve.
            port = port + 1
        end
    end

    result, err = server:listen(0)
    if err then
        console:log(err)
    end

    console:log("Waiting for client to connect...")

    server:add("received", accept)
end

callbacks:add("frame", tick)
