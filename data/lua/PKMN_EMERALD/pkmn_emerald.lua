local socket = require("socket")
local json = require("json")

local STATE_OK = "OK"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local ap_received_item_address = 0x2037344
local save_block_ptr_address = 0x3005d8c

local prevstate = ""
local current_state = STATE_UNINITIALIZED
local pkeSocket = nil
local frame = 0

function receive()
    l, error = pkeSocket:receive()

    -- Handle incoming message
    if error == "closed" then
        if current_state == STATE_OK then
            print("Connection closed")
        end
        current_state = STATE_UNINITIALIZED
        return
    elseif error == "timeout" then
        print("Timeout")
        return
    elseif error ~= nil then
        print(e)
        current_state = STATE_UNINITIALIZED
        return
    end

    process_block(json.decode(l))

    -- Determine message to send back
    local return_table = {}
    return_table["playerName"] = get_player_name()
    return_table["scriptVersion"] = script_version
    return_table["deathlinkActive"] = deathlink_enabled()
    if InSafeState() then
        return_table["locations"] = check_all_locations(master_quest_table_address)
        return_table["collectibles"] = check_collectibles()
        return_table["isDead"] = get_death_state()
        return_table["gameComplete"] = is_game_complete()
    end

    -- Send the message
    msg = json.encode(return_table).."\n"
    local response, error = pkeSocket:send(msg)
    if response == nil then
        print(error)
    elseif current_state == STATE_INITIAL_CONNECTION_MADE then
        current_state = STATE_TENTATIVELY_CONNECTED
    elseif current_state == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        current_state = STATE_OK
    end
end

function main()
    if (is23Or24Or25 or is26To27) == false then
        print("Must use a version of bizhawk 2.3.1 or higher")
        return
    end
    server, error = socket.bind("localhost", 28921)

    while true do
        frame = frame + 1
        if not (current_state == prevstate) then
            prevstate = current_state
        end
        if (current_state == STATE_OK) or (current_state == STATE_INITIAL_CONNECTION_MADE) or (current_state == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 30 == 0) then
                receive()
            end
        elseif (current_state == STATE_UNINITIALIZED) then
            if  (frame % 60 == 0) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    current_state = STATE_INITIAL_CONNECTION_MADE
                    pkeSocket = client
                    pkeSocket:settimeout(0)
                else
                    print('Connection failed, ensure OoTClient is running and rerun oot_connector.lua')
                    return
                end
            end
        end
        emu.frameadvance()
    end
end

main()
