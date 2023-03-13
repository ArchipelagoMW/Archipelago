local socket = require("socket")
local json = require("json")

local GBA_PORT = 43053

local STATE_UNINITIALIZED = 0
local STATE_INITIAL_CONNECTION_MADE = 1
local STATE_TENTATIVELY_CONNECTED = 2
local STATE_OK = 3

local GAME_STATE_UNSAFE = 0
local GAME_STATE_SAFE = 1

local ap_socket = nil
local current_state = STATE_UNINITIALIZED
local previous_state = STATE_UNINITIALIZED

local current_game_state = GAME_STATE_UNSAFE

-- Offsets and sizes
local iwram_offset = 0x3000000
local ewram_offset = 0x2000000
local flags_offset = 0x13B0
local flags_size = 0x12C
local archipelago_flags_offset = 0x36D8
local archipelago_flags_size = 0x180

-- IWRAM Addresses
local save_block_ptr_address = 0x5D8C
local cb2_address = 0x22C0 + 4

-- EWRAM Addresses
local archipelago_received_item_address = 0x39F88

-- ROM addresses
local cb2_overworld_address = 0x8085dd0 + 1

local received_items = {}
local acknowledged_items = {}

function check_game_state ()
    local cb2_value = memory.read_u32_le(cb2_address, "IWRAM")
    if (cb2_value == cb2_overworld_address) then
        current_game_state = GAME_STATE_SAFE
    else
        current_game_state = GAME_STATE_UNSAFE
    end
end

function process_data (data)
    if (data == nil) then
        return
    end

    if (data["items"] ~= nil) then
        received_items = data["items"]
    end
end

function update_acknowledged_items ()
    if (current_game_state == GAME_STATE_SAFE) then
        local save_block_address = memory.read_u32_le(save_block_ptr_address, "IWRAM") - ewram_offset

        local archipelago_flag_bytes = memory.read_bytes_as_array(save_block_address + archipelago_flags_offset, archipelago_flags_size, "EWRAM")
        for byte_i, byte in ipairs(archipelago_flag_bytes) do
            for i = 0,8,1 do
                if (bit.check(byte, i) == 1) then
                    flag_id = (byte_i * 8) + i
                    acknowledged_items[flag_id] = true
                end
            end
        end
    end
end

function try_write_item ()
    local is_filled = memory.read_u8(archipelago_received_item_address + 4, "EWRAM")
    
    if (is_filled) then return end

    unacknowledged_item = nil
    for _, item in ipairs(received_items) do
        print("Items: "..item[0]..item[1])
        if (acknowledged_items[item[1]] ~= true) then
            unacknowledged_item = item
            break
        end
    end

    if (unacknowledged_item ~= nil) then
        memory.write_u16_le(archipelago_received_item_address + 0, unacknowledged_item[0], "EWRAM")
        memory.write_u16_le(archipelago_received_item_address + 2, unacknowledged_item[1], "EWRAM")
        memory.write_u8(archipelago_received_item_address + 4, 1, "EWRAM")
    end
end

function create_message ()
    local data = {}

    data["script_version"] = 1

    if (current_game_state == GAME_STATE_SAFE) then
        local save_block_address = memory.read_u32_le(save_block_ptr_address, "IWRAM") - ewram_offset

        local flag_bytes = memory.read_bytes_as_array(save_block_address + flags_offset, flags_size, "EWRAM")
        data["flag_bytes"] = flag_bytes
    end

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
                    print("Connected!")
                    current_state = STATE_INITIAL_CONNECTION_MADE
                    ap_socket = client
                    ap_socket:settimeout(0)
                end
            end
        else
            if (frame % 5 == 0) then
                send_receive()
                update_acknowledged_items()
                try_write_item()
            end
        end

        emu.frameadvance()
    end
end

main()
