local socket = require("socket")
local json = require("json")

local GBA_PORT = 43053

local STATE_UNINITIALIZED = 0
local STATE_INITIAL_CONNECTION_MADE = 1
local STATE_TENTATIVELY_CONNECTED = 2
local STATE_OK = 3

local ap_socket = nil
local current_state = STATE_UNINITIALIZED
local previous_state = STATE_UNINITIALIZED

-- Offsets and sizes
local iwram_offset = 0x3000000
local ewram_offset = 0x2000000
local flags_offset = 0x13B0
local flags_size = 0x12C

-- IWRAM Addresses
local save_block_ptr_address = 0x5D8C

-- EWRAM Addresses
local archipelago_received_item_address = 0x39F88

local received_items = {}

function process_data (data)
    if (data == nil) then
        return
    end

    if (data["items"] ~= nil) then
        received_items = data["items"]
    end
end

function create_message ()
    local data = {}

    local save_block_address = memory.read_u32_le(save_block_ptr_address, "IWRAM") - ewram_offset

    local flag_bytes = memory.read_bytes_as_array(save_block_address + flags_offset, flags_size, "EWRAM")
    data["flag_bytes"] = flag_bytes

    return json.encode(data).."\n"
end

function send_receive ()
    local message, err = ap_socket:receive()

    -- Handle errors
    if (err == "closed") then
        if (current_state == STATE_OK) then
            print("Connection closed")
        end
        current_state = STATE_UNINITIALIZED
        return
    elseif (err == "timeout") then
        return
    elseif e ~= nil then
        print(e)
        current_state = STATE_UNINITIALIZED
        return
    end

    -- Process received data
    if (message ~= nil) then
        process_data(json.decode(message))
    end

    -- Send data
    local result, err ap_socket:send(create_message())

    if (result == nil) then
        print(err)
    elseif (current_state == STATE_INITIAL_CONNECTION_MADE) then
        current_state = STATE_TENTATIVELY_CONNECTED
    elseif (current_state == STATE_TENTATIVELY_CONNECTED) then
        print("Connected!")
        current_state = STATE_OK
    end
end

function main ()
    if ((is23Or24Or25 or is26To28) == false) then
        print("Must use a version of bizhawk 2.3.1 or higher")
        return
    end

    local frame = 0

    local server, err = socket.bind("localhost", GBA_PORT)
    if (err ~= nil) then
        print(err)
        return
    end

    while true do
        frame = frame + 1

        if not (current_state == previous_state) then
            print("Current state: "..current_state)
            previous_state = current_state
        end

        if (current_state == STATE_UNINITIALIZED) then
            if (frame % 60 == 0) then
                print("Trying to connect to client...")
                emu.frameadvance() -- To flush print message

                server:settimeout(2)
                local client, timeout = server:accept()
                if (timeout == nil) then
                    current_state = STATE_INITIAL_CONNECTION_MADE
                    ap_socket = client
                    ap_socket:settimeout(0)
                end
            end
        else
            if (frame % 5 == 0) then
                send_receive()
            end
        end

        emu.frameadvance()
    end
end

main()
