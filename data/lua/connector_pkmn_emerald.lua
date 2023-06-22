local socket = require("socket")
local json = require("json")
require("common")

local SOCKET_PORT = 43053

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

local received_items = {}

-- TODO: Addresses may change any time the base rom is updated.
-- Could pull addresses from extracted_data.json, but would have to rely
-- on relative paths. Could have client send address info in payload, but
-- that's a lot of wasted data. Could have client send address info on first
-- connection, but lazy. Could deal with it and wait for generalized SNI to replace this.

-- Offsets and sizes
local iwram_start = 0x3000000
local ewram_start = 0x2000000

local last_received_item_index_offset = 0x3778
local trade_pokemon_offset = 0x377A
local flags_offset = 0x1450
local flags_size = 0x12C

-- IWRAM Addresses
local save_block_ptr_address = 0x5D8C              -- gSaveBlock1Ptr
local cb2_address = 0x22C0 + 4                     -- gMain + offset

-- EWRAM Addresses
local archipelago_received_item_address = 0x3A02C  -- gArchipelagoReceivedItem

-- ROM addresses
local slot_name_address = 0x59A3CC                 -- gArchipelagoInfo

-- Bus addresses
local cb2_overworld_func_address = 0x808605C + 1   -- CB2_Overworld + 1

local bizhawk_version = client.getversion()
local bizhawk_major, bizhawk_minor, bizhawk_patch = bizhawk_version:match("(%d+)%.(%d+)%.?(%d*)")
bizhawk_major = tonumber(bizhawk_major)
bizhawk_minor = tonumber(bizhawk_minor)

-- Set us as safe if we're in the overworld and player has control
function check_game_state ()
    local cb2_value = memory.read_u32_le(cb2_address, "IWRAM")

    if (cb2_value == cb2_overworld_func_address) then
        current_game_state = GAME_STATE_SAFE
    else
        current_game_state = GAME_STATE_UNSAFE
    end
end

-- Process data received from AP client
function process_data (data)
    if (data == nil) then
        return
    end

    if (data["items"] ~= nil) then
        received_items = data["items"]
    end

    if (data["received_trade_pokemon"] ~= nil) then
        local save_block_address = memory.read_u32_le(save_block_ptr_address, "IWRAM") - ewram_start
        memory.write_bytes_as_array(save_block_address + trade_pokemon_offset, data["received_trade_pokemon"], "EWRAM")
    end
end

-- Try to fill the received item struct with the next item
function try_write_next_item ()
    if (current_game_state == GAME_STATE_SAFE) then
        local is_filled = memory.read_u8(archipelago_received_item_address + 4, "EWRAM")

        if (is_filled ~= 0) then return end -- Currently filled item still not consumed

        local save_block_address = memory.read_u32_le(save_block_ptr_address, "IWRAM") - ewram_start
        local last_received_item_index = memory.read_u16_le(save_block_address + last_received_item_index_offset, "EWRAM")

        next_item = received_items[last_received_item_index + 1]
        if (next_item ~= nil) then
            memory.write_u16_le(archipelago_received_item_address + 0, next_item[1],                 "EWRAM")
            memory.write_u16_le(archipelago_received_item_address + 2, last_received_item_index + 1, "EWRAM")
            memory.write_u8(    archipelago_received_item_address + 4, 1,                            "EWRAM")
            memory.write_u8(    archipelago_received_item_address + 5, next_item[2],                 "EWRAM")
        end
    end
end

-- Send relevant data to AP client (flags indicating checked locations)
-- AP client will deterimine which flags are important
function create_message ()
    local data = {}

    data["script_version"] = 1

    local slot_name = memory.read_bytes_as_array(slot_name_address, 64, "ROM")
    data["slot_name"] = slot_name

    if (current_game_state == GAME_STATE_SAFE) then
        local save_block_address = memory.read_u32_le(save_block_ptr_address, "IWRAM") - ewram_start

        local flag_bytes = memory.read_bytes_as_array(save_block_address + flags_offset, flags_size, "EWRAM")
        data["flag_bytes"] = flag_bytes

        local current_trade_pokemon = memory.read_bytes_as_array(save_block_address + trade_pokemon_offset, 80, "EWRAM")
        data["current_trade_pokemon"] = current_trade_pokemon
    end

    return json.encode(data).."\n"
end

-- Receive data from AP client and send message back
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
    elseif err ~= nil then
        print(err)
        current_state = STATE_UNINITIALIZED
        return
    end

    -- Process received data
    if (message ~= nil and message ~= "") then
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
    if (bizhawk_major < 2 or (bizhawk_major == 2 and bizhawk_minor < 7)) then
        print("Must use a version of bizhawk 2.7.0 or higher")
        return
    elseif (isUntestedBizhawk) then
        print(untestedBizhawkMessage)
    end

    local frame = 0

    local server, err = socket.bind("localhost", SOCKET_PORT)
    if (err ~= nil) then
        print(err)
        return
    end

    while true do
        frame = frame + 1

        if not (current_state == previous_state) then
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
            if (frame % 10 == 0) then
                check_game_state()
                send_receive()
                try_write_next_item()
            end
        end

        emu.frameadvance()
    end
end

main()
