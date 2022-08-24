local socket = require("socket")
local json = require('json')
local math = require('math')

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local mmbn3Socket = nil
local frame = 0

function receive()
    print(mainmemory.read_u32_be(0x0))
end

function main()
    if (is23Or24Or25 or is26To27) == false then
        print("Must use a version of bizhawk 2.3.1 or higher")
        return
    end
    server, error = socket.bind('localhost', 28922)

    while true do
        frame = frame + 1
        if not (curstate == prevstate) then
            prevstate = curstate
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 60 == 0) then
                receive()
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            if (frame % 60 == 0) then
                server:settimeout(2)
                print("Attempting to connect")
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    mmbn3Socket = client
                    mmbn3Socket:settimeout(0)
                else
                    print('Connection failed, ensure MMBN3Client is running and rerun mmbn3_connector.lua')
                     return
                end
            end
        end
        emu.frameadvance()
    end
end

main()