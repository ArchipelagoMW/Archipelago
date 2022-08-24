local socket = require("socket")
local json = require('json')
local math = require('math')

local last_modified_date = '2022-08-21' -- Should be the last modified date
local script_version = 0


local temp_context = nil

local game_modes = {
    [-1]={name="Unknown", loaded=false},
    [0]={name="GBA Logo", loaded=false},
    [1]={name="Title Screen", loaded=false},
    [2]={name="Normal Gameplay", loaded=true},
    [3]={name="Battle Gameplay", loaded=true},
    [4]={name="Cutscene", loaded=true},
    [5]={name="Paused", loaded=true}
}

local function get_current_game_mode()
    local mode = -1
    local logo_state = state_logo:get()
    if logo_state == 0x802C5880 or logo_state == 0x00000000 then
        mode = 0
    else
        if state_main:get() == 1 then
            mode = 1
        else
            -- Here's where we determine if you're in a battle, cutscene, menu, or otherwise
            -- Gonna need to revisit this later
            --[[
            local menu_state = state_menu:get()
            if menu_state == 0 then
                    if state_sub:get() == 4 then
                        mode = 4
                    else
                        mode = 3
                    end
                end
            elseif (0 < menu_state and menu_state < 9) or menu_state == 13 then
                mode = 5
            elseif menu_state == 9 or menu_state == 0xB then
                mode = 7
            else
                mode = 8
            end
            --]]
        end
    end
    return mode, game_modes[mode]
end

function InSafeState()
    return game_modes[get_current_game_mode()].loaded
end

function item_receivable()
    -- Places you can't receive an item for whatever reason. Possibly unneeded
    local excluded_scenes = {}

    local details
    local scene
    _, details = get_current_game_mode()
    scene = global_context:rawget('cur_scene'):rawget()

    local playerQueued = mainmemory.read_u16_be(incoming_player_addr)
    local itemQueued = mainmemory.read_u16_be(incoming_item_addr)

    -- Safe to receive an item if the scene is normal, player is not in an excluded scene, and no item is already queued
    return details.name == "Normal Gameplay" and excluded_scenes[scene] == nil and playerQueued == 0 and itemQueued == 0
end

function get_player_name()
    -- MMBN3 doesn't have a player name, so this will probably need to be changed so it doesn't autheticate on it
    -- local rom_name_bytes = mainmemory.readbyterange(rom_name_location, 16)
    -- return bytes_to_string(rom_name_bytes)
end

function setPlayerName(id, name)
    -- Again, possibly unneeded. Double check this later
end

function is_game_complete()
    -- If the game is complete, do not read memory
    if is_game_complete then return true end

    -- contains a pointer to the current scene
    -- TODO actually find this memory address
    local scene_pointer = mainmemory.read_u32_be(0x00000000)

    -- Need a way to know what mode we're in
    local Alpha_Defeated = 0x00000000
    local Serenade_Defeated = 0x00000000
    local Alpha_Omega_Defeated = 0x00000000

    -- If the game is complete, set the lib variable and report the game as completed
    if (scene_pointer == Alpha_Defeated) or (scene_pointer == Serenade_Defeated) or (scene_pointer == Alpha_Omega_Defeated) then
        game_complete = true
        return true
    end

    -- Game is still ongoing
    return false
end

function process_blocks(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    -- Here is where the OOT code writes the player name which we might not need
    -- Here is where the OOT code handles death linking, which we are not doing yet

    -- Queue item for receiving if one exists
    item_queue = block['items']
    received_items_count = mainmemory.read_u16_be(internal_count_addr)
    if received_items_count < #item_queue then
        -- There are items to send: remember lua tables are 1-indexed!
        if item_receivable() then
            mainmemory.write_u16_be(incoming_player_addr, 0x00)
            mainmemory.write_u16_be(incoming_item_addr, item_queue[received_items_count+1])
        end
    end
    return
end

function receive()
    l, e = mmbn3Socket:receive()
    -- Handle incoming message
    if e == 'closed' then
        if curstate == STATE_OK then
            print("Connection closed")
        end
        curstate = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        print("timeout")
        return
    elseif e ~= nil then
        print(e)
        curstate = STATE_UNINITIALIZED
        return
    end
    process_block(json.decode(l))

    -- Determine message to send back
    local retTable = {}
    retTable["playerName"] = get_player_name()
    retTable["scriptVersion"] = script_version
    if InSafeState() then
        retTable["locations"] = check_all_locations(...)
        retTable["gameComplete"] = is_game_complete()
    end

    -- Send the message
    msg = json.encode(retTable).."\n"
    local ret, error = mmbn3Socket:send(msg)
    if ret == nil then
        print(error)
    elseif curstate == STATE_INITIAL_CONNECTION_MADE then
        curstate = STATE_TENTATIVELY_CONNECTED
    elseif curstate == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        curstate = STATE_OK
    end
end

function main()
    if (is23Or24Or25 or is26To27) == false then
        print("Must use a version of bizhawk 2.3.1 or higher")
        return
    end
    server, error = socket.bind('localhost', 28921)

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
            if (frame % 120 == 0) then
                server:settimeout(2)
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