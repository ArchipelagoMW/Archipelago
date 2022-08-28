local socket = require("socket")
local json = require('json')
local math = require('math')

local last_modified_date = '2022-08-21' -- Should be the last modified date
local script_version = 1

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local mmbn3Socket = nil
local frame = 0

local acdc_bmd_checks = function()
    local checks ={}
    checks["ACDC 1 Southwest BMD"] = memory.read_u8(0x020001d0)
    checks["ACDC 1 Northeast BMD"] = memory.read_u8(0x020001d0)
    checks["ACDC 2 Center BMD"] = memory.read_u8(0x020001d1)
    checks["ACDC 2 North BMD"] = memory.read_u8(0x020001d1)
    checks["ACDC 3 Southwest BMD"] = memory.read_u8(0x020001d2)
    checks["ACDC 3 Northeast BMD"] = memory.read_u8(0x020001d2)
    return checks
end

local sci_bmd_checks = function()
    local checks ={}
    checks["SciLab 1 WWW BMD"] = memory.read_u8(0x20001d8)
    checks["SciLab 1 East BMD"] = memory.read_u8(0x20001d8)
    checks["SciLab 2 West BMD"] = memory.read_u8(0x20001d9)
    checks["SciLab 2 South BMD"] = memory.read_u8(0x20001d9)
            return checks
end

local yoka_bmd_checks = function()
    local checks ={}
    checks["Yoka 1 North MBD"] = memory.read_u8(0x20001e0)
    checks["Yoka 1 WWW BMD"] = memory.read_u8(0x20001e0)
    checks["Yoka 2 Upper BMD"] = memory.read_u8(0x20001e1)
    checks["Yoka 2 Lower BMD"] = memory.read_u8(0x20001e1)
            return checks
end

local beach_bmd_checks = function()
    local checks ={}
    checks["Beach 1 BMD"] = memory.read_u8(0x20001e8)
    checks["Beach 2 West BMD"] = memory.read_u8(0x20001e9)
    checks["Beach 2 East BMD"] = memory.read_u8(0x20001e9)
            return checks
end

local undernet_bmd_checks = function()
    local checks ={}
    checks["Undernet 1 South BMD"] = memory.read_u8(0x20001f0)
    checks["Undernet 1 WWW BMD"] = memory.read_u8(0x20001f0)
    checks["Undernet 2 Upper BMD"] = memory.read_u8(0x20001f1)
    checks["Undernet 2 Lower BMD"] = memory.read_u8(0x20001f1)
    checks["Undernet 3 South BMD"] = memory.read_u8(0x20001f2)
    checks["Undernet 3 Central BMD"] = memory.read_u8(0x20001f2)
    checks["Undernet 4 Bottom Pillar BMD"] = memory.read_u8(0x2000161)
    checks["Undernet 4 Bottom West BMD"] = memory.read_u8(0x20001f3)
    checks["Undernet 4 Top Pillar BMD"] = memory.read_u8(0x20001f3)
    checks["Undernet 4 Top North BMD"] = memory.read_u8(0x20001f3)
    checks["Undernet 5 Upper BMD"] = memory.read_u8(0x20001f4)
    checks["Undernet 5 Lower BMD"] = memory.read_u8(0x20001f4)
    checks["Undernet 6 East BMD"] = memory.read_u8(0x20001f5)
    checks["Undernet 6 Central BMD"] = memory.read_u8(0x20001f5)
    checks["Undernet 6 TV BMD"] = memory.read_u8(0x20001f5)
    checks["Undernet 7 West BMD"] = memory.read_u8(0x20001f6)
    checks["Undernet 7 Northwest BMD"] = memory.read_u8(0x20001f6)
    checks["Undernet 7 Northeast BMD"] = memory.read_u8(0x20001f6)
            return checks
end

local secret_bmd_checks = function()
    local checks ={}
    checks["Secret 1 South BMD"] = memory.read_u8(0x2000200)
    checks["Secret 1 Northeast BMD"] = memory.read_u8(0x2000200)
    checks["Secret 1 Northwest BMD"] = memory.read_u8(0x2000200)
    checks["Secret 2 Upper BMD"] = memory.read_u8(0x2000201)
    checks["Secret 2 Lower BMD"] = memory.read_u8(0x2000201)
    checks["Secret 2 Island BMD"] = memory.read_u8(0x2000201)
    checks["Secret 3 South BMD"] = memory.read_u8(0x2000202)
    checks["Secret 3 Island BMD"] = memory.read_u8(0x2000202)
    checks["Secret 3 BugFrag BMD"] = memory.read_u8(0x2000202)
            return checks
end

local school_bmd_checks = function()
    local checks ={}
    checks["School 1 Entrance BMD"] = memory.read_u8(0x2000208)
    checks["School 1 North Central BMD"] = memory.read_u8(0x2000208)
    checks["School 1 Far West BMD 2"] = memory.read_u8(0x2000208)
    checks["School 2 Entrance BMD"] = memory.read_u8(0x2000209)
    checks["School 2 South BMD"] = memory.read_u8(0x2000209)
    checks["School 2 Mainframe BMD"] = memory.read_u8(0x2000209)
            return checks
end

local zoo_bmd_checks = function()
    local checks ={}
    checks["Zoo 1 East BMD"] = memory.read_u8(0x2000210)
    checks["Zoo 1 Central BMD"] = memory.read_u8(0x2000210)
    checks["Zoo 1 North BMD"] = memory.read_u8(0x2000210)
    checks["Zoo 2 East BMD"] = memory.read_u8(0x2000211)
    checks["Zoo 2 Central BMD"] = memory.read_u8(0x2000211)
    checks["Zoo 2 West BMD"] = memory.read_u8(0x2000211)
    checks["Zoo 3 North BMD"] = memory.read_u8(0x2000212)
    checks["Zoo 3 Central BMD"] = memory.read_u8(0x2000212)
    checks["Zoo 3 Path BMD"] = memory.read_u8(0x2000212)
    checks["Zoo 3 Northwest BMD"] = memory.read_u8(0x2000212)
    checks["Zoo 4 West BMD"] = memory.read_u8(0x2000213)
    checks["Zoo 4 Northwest BMD"] = memory.read_u8(0x2000213)
    checks["Zoo 4 Southeast BMD"] = memory.read_u8(0x2000213)
            return checks
end

local hades_bmd_checks = function()
    local checks ={}
    checks["Hades South BMD"] = memory.read_u8(0x20001eb)
    return checks
end

local hospital_bmd_checks = function()
    local checks ={}
    checks["Hospital 1 Center BMD"] = memory.read_u8(0x2000218)
    checks["Hospital 1 West BMD"] = memory.read_u8(0x2000218)
    checks["Hospital 1 North BMD"] = memory.read_u8(0x2000218)
    checks["Hospital 2 Southwest BMD"] = memory.read_u8(0x2000219)
    checks["Hospital 2 Central BMD"] = memory.read_u8(0x2000219)
    checks["Hospital 2 Island BMD"] = memory.read_u8(0x2000219)
    checks["Hospital 3 Central BMD"] = memory.read_u8(0x200021a)
    checks["Hospital 3 West BMD"] = memory.read_u8(0x200021a)
    checks["Hospital 3 Northwest BMD"] = memory.read_u8(0x200021a)
    checks["Hospital 4 Central BMD"] = memory.read_u8(0x200021b)
    checks["Hospital 4 Southeast BMD"] = memory.read_u8(0x200021b)
    checks["Hospital 4 North BMD"] = memory.read_u8(0x200021b)
    checks["Hospital 5 Southwest BMD"] = memory.read_u8(0x200021c)
    checks["Hospital 5 Northeast BMD"] = memory.read_u8(0x200021c)
    checks["Hospital 5 Island BMD"] = memory.read_u8(0x200021c)
            return checks
end

local www_bmd_checks = function()
    local checks ={}
    checks["WWW 1 Central BMD"] = memory.read_u8(0x2000220)
    checks["WWW 1 West BMD"] = memory.read_u8(0x2000220)
    checks["WWW 1 East BMD"] = memory.read_u8(0x2000220)
    checks["WWW 2 East BMD"] = memory.read_u8(0x2000221)
    checks["WWW 2 Northwest BMD"] = memory.read_u8(0x2000221)
    checks["WWW 3 East BMD"] = memory.read_u8(0x2000222)
    checks["WWW 3 North BMD"] = memory.read_u8(0x2000222)
    checks["WWW 4 Northwest BMD"] = memory.read_u8(0x2000223)
    checks["WWW 4 Central BMD"] = memory.read_u8(0x2000223)
            return checks
end

local misc_bmd_checks = function()
    local checks ={}
    checks["ACDC Dog House BMD"] = memory.read_u8(0x2000240)
    checks["ACDC Lan's TV BMD"] = memory.read_u8(0x2000242)
    checks["ACDC Yai's Phone BMD"] = memory.read_u8(0x2000244)
    checks["ACDC NumberMan Display BMD"] = memory.read_u8(0x2000248)
    checks["ACDC Tank BMD 1"] = memory.read_u8(0x2000247)
    checks["ACDC Tank BMD 2"] = memory.read_u8(0x2000247)
    checks["ACDC School Server BMD 1"] = memory.read_u8(0x2000242)
    checks["ACDC School Server BMD 2"] = memory.read_u8(0x2000242)
    checks["ACDC School Blackboard BMD"] = memory.read_u8(0x2000240)
    checks["SciLab Vending Machine BMD"] = memory.read_u8(0x2000241)
    checks["SciLab Virus Lab BMD"] = memory.read_u8(0x2000249)
    checks["SciLab Computer BMD"] = memory.read_u8(0x2000241)
    checks["Yoka Armor BMD"] = memory.read_u8(0x2000248)
    checks["Yoka TV BMD"] = memory.read_u8(0x2000247)
    checks["Yoka Hot Spring BMD"] = memory.read_u8(0x200024b)
    checks["Yoka Ticket Machine BMD"] = memory.read_u8(0x2000246)
    checks["Yoka Giraffe BMD"] = memory.read_u8(0x200024b)
    checks["Yoka Panda BMD"] = memory.read_u8(0x2000249)
    checks["Beach Hospital Bed BMD"] = memory.read_u8(0x2000245)
    checks["Beach TV BMD"] = memory.read_u8(0x2000245)
    checks["Beach Vending Machine BMD"] = memory.read_u8(0x2000246)
    checks["Beach News Van BMD"] = memory.read_u8(0x2000243)
    checks["Beach Battle Console BMD"] = memory.read_u8(0x2000243)
    checks["Beach Security System BMD"] = memory.read_u8(0x2000244)
    checks["Beach Broadcast Computer BMD"] = memory.read_u8(0x200024b)
    checks["Hades Gargoyle BMD"] = memory.read_u8(0x200024b)
    checks["WWW Wall BMD"] = memory.read_u8(0x200024a)
    checks["Mayl's HP BMD"] = memory.read_u8(0x2000239)
    checks["Yai's HP BMD 1"] = memory.read_u8(0x200023b)
    checks["Yai's HP BMD 2"] = memory.read_u8(0x200023b)
    checks["Dex's HP BMD 1"] = memory.read_u8(0x200023a)
    checks["Dex's HP BMD 2"] = memory.read_u8(0x200023a)
    checks["Tamako's HP BMD"] = memory.read_u8(0x200023c)
            return checks
end

local story_bmd_checks = function()
    local checks ={}
    checks["Undernet 7 Upper BMD"] = memory.read_u8(0x20001f6)
    checks["School 1 KeyData A BMD"] = memory.read_u8(0x2000208)
    checks["School 1 KeyDataB BMD"] = memory.read_u8(0x2000208)
    checks["School 1 KeyDataC BMD"] = memory.read_u8(0x2000208)
    checks["School 2 CodeC BMD"] = memory.read_u8(0x2000209)
    checks["School 2 CodeA BMD"] = memory.read_u8(0x2000209)
    checks["School 2 CodeB BMD"] = memory.read_u8(0x2000209)
    checks["Hades HadesKey BMD"] = memory.read_u8(0x20001eb)
    checks["WWW 1 South BMD"] = memory.read_u8(0x2000220)
    checks["WWW 2 West BMD"] = memory.read_u8(0x2000221)
    checks["WWW 3 South BMD"] = memory.read_u8(0x2000222)
    checks["WWW 4 East BMD"] = memory.read_u8(0x2000223)
    return checks
end

local pmd_checks = function()
    local checks ={}
    checks["ACDC 1 PMD"] = memory.read_u8(0x020001d0)
    checks["Yoka 1 PMD"] = memory.read_u8(0x20001e0)
    checks["Beach 1 PMD"] = memory.read_u8(0x20001e8)
    checks["Undernet 7 PMD"] = memory.read_u8(0x20001f6)
    checks["Mayl's HP PMD"] = memory.read_u8(0x2000239)
    checks["SciLab Computer PMD"] = memory.read_u8(0x2000241)
    checks["Zoo Panda PMD"] = memory.read_u8(0x2000249)
    checks["DNN Security Panel PMD"] = memory.read_u8(0x2000244)
    checks["DNN Main Console PMD"] = memory.read_u8(0x200024b)
    checks["Tamako's HP PMD"] = memory.read_u8(0x200023c)
    return checks
end

local overworld_checks = function()
    local checks ={}
    checks["Yoka Quiz Master"] = memory.read_u8(0x200005f)
    checks["Hospital Quiz Queen"] = memory.read_u8(0x200005f)
    checks["Hades Quiz King"] = memory.read_u8(0x2000164)
    checks["ACDC SonicWav W Trade"] = memory.read_u8(0x2000162)
    checks["ACDC Bubbler C Trade"] = memory.read_u8(0x2000162)
    checks["ACDC Recov120 S Trade"] = memory.read_u8(0x2000163)
    checks["SciLab Shake1 S Trade"] = memory.read_u8(0x2000163)
    checks["Yoka FireSwrd P Trade"] = memory.read_u8(0x2000162)
    checks["Hospital DynaWav V Trade"] = memory.read_u8(0x2000163)
    checks["DNN WideSwrd C Trade"] = memory.read_u8(0x2000162)
    checks["DNN HoleMetr H Trade"] = memory.read_u8(0x2000164)
    checks["DNN Shadow J Trade"] = memory.read_u8(0x2000163)
    checks["Hades GrabBack K Trade"] = memory.read_u8(0x2000164)
    checks["Comedian"] = memory.read_u8(0x200024d)
    checks["Villain"] = memory.read_u8(0x200024d)
    --checks["Mod Tools Guy"] = memory.read_u8(
    checks["ACDC School Desk"] = memory.read_u8(0x200024c)
    checks["ACDC Class 5B Blackboard"] = memory.read_u8(0x200024c)
    checks["SciLab Garbage Can"] = memory.read_u8(0x200024c)
    checks["Yoka Inn TV"] = memory.read_u8(0x200024c)
    checks["Yoka Zoo Garbage"] = memory.read_u8(0x200024d)
    checks["Beach Department Store"] = memory.read_u8(0x2000161)
    checks["Beach Hospital Vent"] = memory.read_u8(0x200024c)
    checks["Beach Hospital Pink Door"] = memory.read_u8(0x200024d)
    checks["Beach Hospital Tree"] = memory.read_u8(0x200024c)
    checks["Beach Hospital Hidden Conversation"] = memory.read_u8(0x2000162)
    checks["Beach Hospital Girl"] = memory.read_u8(0x2000160)
    checks["Beach DNN Tamako"] = memory.read_u8(0x200024e)
    checks["Beach DNN Boxes"] = memory.read_u8(0x200024c)
    checks["Beach DNN Poster"] = memory.read_u8(0x200024d)
    checks["Hades Boat Dock"] = memory.read_u8(0x200024c)
    checks["WWW Control Room 1 Screen"] = memory.read_u8(0x200024d)
    checks["WWW Wily's Desk"] = memory.read_u8(0x200024d)
    return checks
end

local numberman_checks = function()
    local checks ={}
    checks["Numberman Code 01"] = memory.read_u8(0x2000430)
    checks["Numberman Code 02"] = memory.read_u8(0x2000430)
    checks["Numberman Code 03"] = memory.read_u8(0x2000430)
    checks["Numberman Code 04"] = memory.read_u8(0x2000430)
    checks["Numberman Code 05"] = memory.read_u8(0x2000430)
    checks["Numberman Code 06"] = memory.read_u8(0x2000430)
    checks["Numberman Code 07"] = memory.read_u8(0x2000430)
    checks["Numberman Code 08"] = memory.read_u8(0x2000430)
    checks["Numberman Code 09"] = memory.read_u8(0x2000431)
    checks["Numberman Code 10"] = memory.read_u8(0x2000431)
    checks["Numberman Code 11"] = memory.read_u8(0x2000431)
    checks["Numberman Code 12"] = memory.read_u8(0x2000431)
    checks["Numberman Code 13"] = memory.read_u8(0x2000431)
    checks["Numberman Code 14"] = memory.read_u8(0x2000431)
    checks["Numberman Code 15"] = memory.read_u8(0x2000431)
    checks["Numberman Code 16"] = memory.read_u8(0x2000432)
    checks["Numberman Code 17"] = memory.read_u8(0x2000432)
    checks["Numberman Code 18"] = memory.read_u8(0x2000432)
    checks["Numberman Code 19"] = memory.read_u8(0x2000432)
    checks["Numberman Code 20"] = memory.read_u8(0x2000432)
    checks["Numberman Code 21"] = memory.read_u8(0x2000432)
    checks["Numberman Code 22"] = memory.read_u8(0x2000432)
    checks["Numberman Code 23"] = memory.read_u8(0x2000432)
    checks["Numberman Code 24"] = memory.read_u8(0x2000433)
    checks["Numberman Code 25"] = memory.read_u8(0x2000433)
    checks["Numberman Code 26"] = memory.read_u8(0x2000433)
    checks["Numberman Code 27"] = memory.read_u8(0x2000433)
    checks["Numberman Code 28"] = memory.read_u8(0x2000433)
    checks["Numberman Code 29"] = memory.read_u8(0x2000433)
    checks["Numberman Code 30"] = memory.read_u8(0x2000433)
    checks["Numberman Code 31"] = memory.read_u8(0x2000433)
    return checks
end

local jobs_checks = function()
    local checks ={}
    checks["Job: Please deliver this"] = memory.read_u8(0x2000300)
    checks["Job: My Navi is sick"] = memory.read_u8(0x2000300)
    checks["Job: Help me with my son!"] = memory.read_u8(0x2000300)
    checks["Job: Transmission error"] = memory.read_u8(0x2000300)
    checks["Job: Chip Prices"] = memory.read_u8(0x2000301)
    checks["Job: I'm broke?!"] = memory.read_u8(0x2000301)
    checks["Job: Rare chips for cheap!"] = memory.read_u8(0x2000301)
    checks["Job: Be my boyfriend"] = memory.read_u8(0x2000301)
    checks["Job: Will you deliver?"] = memory.read_u8(0x2000301)
    checks["Job: Look for friends (Tora)"] = memory.read_u8(0x2000300)
    checks["Job: Stuntmen wanted! (Tora)"] = memory.read_u8(0x2000300)
    checks["Job: Riot stopped (Tora)"] = memory.read_u8(0x2000300)
    checks["Job: Gathering Data (Tora)"] = memory.read_u8(0x2000300)
    checks["Job: Somebody, please help!"] = memory.read_u8(0x2000301)
    checks["Job: Looking for condor"] = memory.read_u8(0x2000301)
    checks["Job: Help with rehab"] = memory.read_u8(0x2000301)
    checks["Job: Old Master"] = memory.read_u8(0x2000302)
    checks["Job: Catching gang members"] = memory.read_u8(0x2000302)
    checks["Job: Please adopt a virus!"] = memory.read_u8(0x2000302)
    checks["Job: Legendary Tomes"] = memory.read_u8(0x2000302)
    checks["Job: Legendary Tomes - Treasure"] = memory.read_u8(0x200024e)
    checks["Job: Hide and seek! First Child"] = memory.read_u8(0x2000188)
    checks["Job: Hide and seek! Second Child"] = memory.read_u8(0x2000188)
    checks["Job: Hide and seek! Third Child"] = memory.read_u8(0x2000188)
    checks["Job: Hide and seek! Fourth Child"] = memory.read_u8(0x2000189)
    checks["Job: Hide and seek! Fifth Child"] = memory.read_u8(0x2000302)
    checks["Job: Finding the blue Navi"] = memory.read_u8(0x2000031)
    checks["Job: Give your support"] = memory.read_u8(0x2000302)
    checks["Job: Stamp collecting"] = memory.read_u8(0x2000302)
    checks["Job: Help with a will"] = memory.read_u8(0x2000303)
    return checks
end

local check_all_locations = function()
    local location_checks = {}
    for name,checked in pairs(acdc_bmd_checks()) do location_checks[name] = checked end

    return location_checks
end

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
    return true
    --return game_modes[get_current_game_mode()].loaded
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

local get_player_name = function()
    -- MMBN3 doesn't have a player name, so this will probably need to be changed so it doesn't autheticate on it
    -- local rom_name_bytes = mainmemory.readbyterange(rom_name_location, 16)
    -- return bytes_to_string(rom_name_bytes)
    return "MegaMan"
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

local process_block = function(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    if block ~= nil then
        return
    end
    -- Write player names on first connect or after reset (N64 logo, title screen, file select)
    cur_mode = get_current_game_mode()
    if (first_connect or cur_mode == 0 or cur_mode == 1 or cur_mode == 2) and (#block['playerNames'] > 0) then
        first_connect = false
        local index = 1
        while (index <= #block['playerNames']) and (index < 255) do
            setPlayerName(index, block['playerNames'][index])
            index = index + 1
        end
        setPlayerName(255, 'APPlayer')
    end

    -- Queue item for receiving, if one exists
    item_queue = block['items']
    --received_items_count = mainmemory.read_u16_be(internal_count_addr)
    if received_items_count < #item_queue then
        -- There are items to send: remember lua tables are 1-indexed!
        if item_receivable() then
            --mainmemory.write_u16_be(incoming_player_addr, 0x00)
            --mainmemory.write_u16_be(incoming_item_addr, item_queue[received_items_count+1])
        end
    end
    return
end

local receive = function()
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
        retTable["locations"] = check_all_locations()
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