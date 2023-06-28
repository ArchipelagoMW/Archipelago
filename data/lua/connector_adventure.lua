local socket = require("socket")
local json = require('json')
local math = require('math')
require("common")

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local SCRIPT_VERSION = 1

local APItemValue = 0xA2
local APItemRam = 0xE7
local BatAPItemValue = 0xAB
local BatAPItemRam = 0xEA
local PlayerRoomAddr = 0x8A -- if in number room, we're not in play mode
local WinAddr = 0xDE -- if not 0 (I think if 0xff specifically), we won (and should update once, immediately)

-- If any of these are 2, that dragon ate the player (should send update immediately
-- once, and reset that when none of them are 2 again)

local DragonState = {0xA8, 0xAD, 0xB2}
local last_dragon_state = {0, 0, 0}
local carryAddress = 0x9D -- uses rom object table
local batRoomAddr = 0xCB
local batCarryAddress = 0xD0 -- uses ram object location
local batInvalidCarryItem = 0x78
local batItemCheckAddr = 0xf69f
local batMatrixLen = 11 -- number of pairs
local last_carry_item = 0xB4
local frames_with_no_item = 0
local ItemTableStart = 0xfe9d
local PlayerSlotAddress = 0xfff9

local nullObjectId = 0xB4
local ItemsReceived = nil
local sha256hash = nil
local foreign_items = nil
local foreign_items_by_room = {}
local bat_no_touch_locations_by_room = {}
local bat_no_touch_items = {}
local autocollect_items = {}
local localItemLocations = {}

local prev_bat_room = 0xff
local prev_player_room = 0
local prev_ap_room_index = nil

local pending_foreign_items_collected = {}
local pending_local_items_collected = {}
local rendering_foreign_item = nil
local skip_inventory_items = {}

local inventory = {}
local next_inventory_item = nil

local input_button_address = 0xD7

local deathlink_rec = nil
local deathlink_send = 0

local deathlink_sent = false

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local atariSocket = nil
local frame = 0

local ItemIndex = 0

local yorgle_speed_address = 0xf725
local grundle_speed_address = 0xf740
local rhindle_speed_address = 0xf70A

local read_switch_a = 0xf780
local read_switch_b = 0xf764

local yorgle_speed = nil
local grundle_speed = nil
local rhindle_speed = nil

local slow_yorgle_id = tostring(118000000 + 0x103)
local slow_grundle_id = tostring(118000000 + 0x104)
local slow_rhindle_id = tostring(118000000 + 0x105)

local yorgle_dead = false
local grundle_dead = false
local rhindle_dead = false

local diff_a_locked = false
local diff_b_locked = false

local bat_logic = 0

local is_dead = 0
local freeincarnates_available = 0
local send_freeincarnate_used = false
local current_bat_ap_item = nil

local was_in_number_room = false

function uRangeRam(address, bytes)
	data = memory.read_bytes_as_array(address, bytes, "Main RAM")
	return data
end
function uRangeRom(address, bytes)
	data = memory.read_bytes_as_array(address+0xf000, bytes, "System Bus")
	return data
end
function uRangeAddress(address, bytes)
	data = memory.read_bytes_as_array(address, bytes, "System Bus")
	return data
end

local function createForeignItemsByRoom()
    foreign_items_by_room = {}
    if foreign_items == nil then
        return
    end
    for _, foreign_item in pairs(foreign_items) do
        if foreign_items_by_room[foreign_item.room_id] == nil then
            foreign_items_by_room[foreign_item.room_id] = {}
        end
        new_foreign_item = {}
        new_foreign_item.room_id = foreign_item.room_id
        new_foreign_item.room_x = foreign_item.room_x
        new_foreign_item.room_y = foreign_item.room_y
        new_foreign_item.short_location_id = foreign_item.short_location_id

        table.insert(foreign_items_by_room[foreign_item.room_id], new_foreign_item)
    end
end

function debugPrintNoTouchLocations()
    for room_id, list in pairs(bat_no_touch_locations_by_room) do
        for index, notouch_location in ipairs(list) do
            print("ROOM "..tostring(room_id).. "["..tostring(index).."]: "..tostring(notouch_location.short_location_id))
        end
    end
end

function processBlock(block)
    if block == nil then
        return
    end
    local block_identified = 0
    local msgBlock = block['messages']
    if msgBlock ~= nil then
        block_identified = 1
        for i, v in pairs(msgBlock) do
            if itemMessages[i] == nil then
                local msg = {TTL=450, message=v, color=0xFFFF0000}
                itemMessages[i] = msg
            end
        end
    end
    local itemsBlock = block["items"]
    if itemsBlock ~= nil then
        block_identified = 1
	    ItemsReceived = itemsBlock
    end
    local apItemsBlock = block["foreign_items"]
    if apItemsBlock ~= nil then
        block_identified = 1
        print("got foreign items block")
        foreign_items = apItemsBlock
        createForeignItemsByRoom()
    end
    local autocollectItems = block["autocollect_items"]
    if autocollectItems ~= nil then
        block_identified = 1
        autocollect_items = {}
        for _, acitem in pairs(autocollectItems) do
            if autocollect_items[acitem.room_id] == nil then
                autocollect_items[acitem.room_id] = {}
            end
            table.insert(autocollect_items[acitem.room_id], acitem)
        end
    end
    local localLocalItemLocations = block["local_item_locations"]
    if localLocalItemLocations ~= nil then
        block_identified = 1
        localItemLocations = localLocalItemLocations
        print("got local item locations")
    end
    local checkedLocationsBlock = block["checked_locations"]
    if checkedLocationsBlock ~= nil then
        block_identified = 1
        for room_id, foreign_item_list in pairs(foreign_items_by_room) do
            for i, foreign_item in pairs(foreign_item_list) do
                short_id = foreign_item.short_location_id
                for j, checked_id in pairs(checkedLocationsBlock) do
                    if checked_id == short_id then
                        table.remove(foreign_item_list, i)
                        break
                    end
                end
            end
        end
        if foreign_items ~= nil then
            for i, foreign_item in pairs(foreign_items) do
                short_id = foreign_item.short_location_id
                for j, checked_id in pairs(checkedLocationsBlock) do
                    if checked_id == short_id then
                        foreign_items[i] = nil
                        break
                    end
                end
            end
        end
    end
    local dragon_speeds_block = block["dragon_speeds"]
    if dragon_speeds_block ~= nil then
        block_identified = 1
        yorgle_speed = dragon_speeds_block[slow_yorgle_id]
        grundle_speed = dragon_speeds_block[slow_grundle_id]
        rhindle_speed = dragon_speeds_block[slow_rhindle_id]
    end
    local diff_a_block = block["difficulty_a_locked"]
    if diff_a_block ~= nil then
        block_identified = 1
        diff_a_locked = diff_a_block
    end
    local diff_b_block = block["difficulty_b_locked"]
    if diff_b_block ~= nil then
        block_identified = 1
        diff_b_locked = diff_b_block
    end
    local freeincarnates_available_block = block["freeincarnates_available"]
    if freeincarnates_available_block ~= nil then
        block_identified = 1
        if freeincarnates_available ~= freeincarnates_available_block then
            freeincarnates_available = freeincarnates_available_block
            local msg = {TTL=450, message="freeincarnates: "..tostring(freeincarnates_available), color=0xFFFF0000}
            itemMessages[-2] = msg
        end
    end
    local bat_logic_block = block["bat_logic"]
    if bat_logic_block ~= nil then
        block_identified = 1
        bat_logic = bat_logic_block
    end
    local bat_no_touch_locations_block = block["bat_no_touch_locations"]
    if bat_no_touch_locations_block ~= nil then
        block_identified = 1
        for _, notouch_location in pairs(bat_no_touch_locations_block) do
            local room_id = tonumber(notouch_location.room_id)
            if bat_no_touch_locations_by_room[room_id] == nil then
                bat_no_touch_locations_by_room[room_id] = {}
            end
            table.insert(bat_no_touch_locations_by_room[room_id], notouch_location)

            if notouch_location.local_item ~= nil and notouch_location.local_item ~= 255 then
                bat_no_touch_items[tonumber(notouch_location.local_item)] = true
                -- print("no touch: "..tostring(notouch_location.local_item))
            end
        end
        -- debugPrintNoTouchLocations()
    end
    deathlink_rec = deathlink_rec or block["deathlink"]
    if( block_identified == 0 ) then
        print("unidentified block")
        print(block)
    end
end

function getAllRam()
    uRangeRAM(0,128);
    return data
end

local function alive_mode()
    return (u8(PlayerRoomAddr) ~= 0x00 and u8(WinAddr) == 0x00)
end

local function generateLocationsChecked()
    list_of_locations = {}
    for s, f in pairs(pending_foreign_items_collected) do
        table.insert(list_of_locations, f.short_location_id + 118000000)
    end
    for s, f in pairs(pending_local_items_collected) do
        table.insert(list_of_locations, f + 118000000)
    end
    return list_of_locations
end

function receive()
    l, e = atariSocket:receive()
    if e == 'closed' then
        if curstate == STATE_OK then
            print("Connection closed")
        end
        curstate = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        return
    elseif e ~= nil then
        print(e)
        curstate = STATE_UNINITIALIZED
        return
    end
    if l ~= nil then
        processBlock(json.decode(l))
    end
    -- Determine Message to send back

    newSha256 = memory.hash_region(0xF000, 0x1000, "System Bus")
    if (sha256hash ~= nil and sha256hash ~= newSha256) then
        print("ROM changed, quitting")
        curstate = STATE_UNINITIALIZED
        return
    end
    sha256hash = newSha256
    local retTable = {}
    retTable["scriptVersion"] = SCRIPT_VERSION
    retTable["romhash"] = sha256hash
    if (alive_mode()) then
        retTable["locations"] = generateLocationsChecked()
    end
    if (u8(WinAddr) ~= 0x00) then
        retTable["victory"] = 1
    end
    if( deathlink_sent or deathlink_send == 0 ) then
        retTable["deathLink"] = 0
    else
        print("Sending deathlink "..tostring(deathlink_send))
        retTable["deathLink"] = deathlink_send
        deathlink_sent = true
    end
    deathlink_send = 0

    if send_freeincarnate_used == true then
        print("Sending freeincarnate used")
        retTable["freeincarnate"] = true
        send_freeincarnate_used = false
    end

    msg = json.encode(retTable).."\n"
    local ret, error = atariSocket:send(msg)
    if ret == nil then
        print(error)
    elseif curstate == STATE_INITIAL_CONNECTION_MADE then
        curstate = STATE_TENTATIVELY_CONNECTED
    elseif curstate == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        curstate = STATE_OK
    end
end

function AutocollectFromRoom()
    if autocollect_items ~= nil and autocollect_items[prev_player_room] ~= nil then
        for _, item in pairs(autocollect_items[prev_player_room]) do
            pending_foreign_items_collected[item.short_location_id] = item
        end
    end
end

function SetYorgleSpeed()
    if yorgle_speed ~= nil then
        emu.setregister("A", yorgle_speed);
    end
end

function SetGrundleSpeed()
    if grundle_speed ~= nil then
        emu.setregister("A", grundle_speed);
    end
end

function SetRhindleSpeed()
    if rhindle_speed ~= nil then
        emu.setregister("A", rhindle_speed);
    end
end

function SetDifficultySwitchB()
    if diff_b_locked then
        local a = emu.getregister("A")
        if a < 128 then
            emu.setregister("A", a + 128)
        end
    end
end

function SetDifficultySwitchA()
    if diff_a_locked then
        local a = emu.getregister("A")
        if (a > 128 and a < 128 + 64) or (a < 64) then
            emu.setregister("A", a + 64)
        end
    end
end

function TryFreeincarnate()
    if freeincarnates_available > 0 then
        freeincarnates_available = freeincarnates_available - 1
        for index, state_addr in pairs(DragonState) do
            if last_dragon_state[index] == 1 then
                send_freeincarnate_used = true
                memory.write_u8(state_addr, 1, "System Bus")
                local msg = {TTL=450, message="used freeincarnate", color=0xFF00FF00}
                itemMessages[-1] = msg
            end
        end

    end
end

function GetLinkedObject()
    if emu.getregister("X") == batRoomAddr then
        bat_interest_item = emu.getregister("A")
        -- if the bat can't touch that item, we'll switch it to the number item, which should never be
        -- in the same room as the bat.
        if bat_no_touch_items[bat_interest_item] ~= nil then
            emu.setregister("A", 0xDD )
            emu.setregister("Y", 0xDD )
        end
    end
end

function CheckCollectAPItem(carry_item, target_item_value, target_item_ram, rendering_foreign_item)
    if( carry_item == target_item_value and rendering_foreign_item ~= nil ) then
        memory.write_u8(carryAddress, nullObjectId, "System Bus")
        memory.write_u8(target_item_ram, 0xFF, "System Bus")
        pending_foreign_items_collected[rendering_foreign_item.short_location_id] = rendering_foreign_item
        for index, fi in pairs(foreign_items_by_room[rendering_foreign_item.room_id]) do
            if( fi.short_location_id == rendering_foreign_item.short_location_id ) then
                table.remove(foreign_items_by_room[rendering_foreign_item.room_id], index)
                break
            end
        end
        for index, fi in pairs(foreign_items) do
            if( fi.short_location_id == rendering_foreign_item.short_location_id ) then
                foreign_items[index] = nil
                break
            end
        end
        prev_ap_room_index = 0
        return true
    end
    return false
end

function BatCanTouchForeign(foreign_item, bat_room)
    if bat_no_touch_locations_by_room[bat_room] == nil or bat_no_touch_locations_by_room[bat_room][1] == nil then
        return true
    end

    for index, location in ipairs(bat_no_touch_locations_by_room[bat_room]) do
        if location.short_location_id == foreign_item.short_location_id then
            return false
        end
    end
    return true;
end

function main()
    memory.usememorydomain("System Bus")
    if not checkBizHawkVersion() then
        return
    end
    local playerSlot = memory.read_u8(PlayerSlotAddress)
    local port = 17242 + playerSlot
    print("Using port"..tostring(port))
    server, error = socket.bind('localhost', port)
    if( error ~= nil ) then
        print(error)
    end
    event.onmemoryexecute(SetYorgleSpeed, yorgle_speed_address);
    event.onmemoryexecute(SetGrundleSpeed, grundle_speed_address);
    event.onmemoryexecute(SetRhindleSpeed, rhindle_speed_address);
    event.onmemoryexecute(SetDifficultySwitchA, read_switch_a)
    event.onmemoryexecute(SetDifficultySwitchB, read_switch_b)
    event.onmemoryexecute(GetLinkedObject, batItemCheckAddr)
    -- TODO: Add an onmemoryexecute event to intercept the bat reading item rooms, and don't 'see' an item in the
    -- room if it is in bat_no_touch_locations_by_room.  Although realistically, I may have to handle this in the rom
    -- for it to be totally reliable, because it won't work before the script connects (I might have to reset them?)
    -- TODO: Also remove those items from the bat_no_touch_locations_by_room if they have been collected
    while true do
        frame = frame + 1
        drawMessages()
        if not (curstate == prevstate) then
            print("Current state: "..curstate)
            prevstate = curstate
        end

        local current_player_room = u8(PlayerRoomAddr)
        local bat_room = u8(batRoomAddr)
        local bat_carrying_item = u8(batCarryAddress)
        local bat_carrying_ap_item = (BatAPItemRam == bat_carrying_item)

        if current_player_room == 0x1E then
            if u8(PlayerRoomAddr + 1) > 0x4B then
                memory.write_u8(PlayerRoomAddr + 1, 0x4B)
            end
        end

        if current_player_room == 0x00 then
            if not was_in_number_room then
                print("reset "..tostring(bat_carrying_ap_item).." "..tostring(bat_carrying_item))
                memory.write_u8(batCarryAddress, batInvalidCarryItem)
                memory.write_u8(batCarryAddress+ 1, 0)
                createForeignItemsByRoom()
                memory.write_u8(BatAPItemRam, 0xff)
                memory.write_u8(APItemRam, 0xff)
                prev_ap_room_index = 0
                prev_player_room = 0
                rendering_foreign_item = nil
                was_in_number_room = true
            end
        else
            was_in_number_room = false
        end

        if bat_room ~= prev_bat_room then
            if bat_carrying_ap_item then
                if foreign_items_by_room[prev_bat_room] ~= nil then
                    for r,f in pairs(foreign_items_by_room[prev_bat_room]) do
                        if f.short_location_id == current_bat_ap_item.short_location_id then
                            -- print("removing item from "..tostring(r).." in "..tostring(prev_bat_room))
                            table.remove(foreign_items_by_room[prev_bat_room], r)
                            break
                        end
                    end
                end
                if foreign_items_by_room[bat_room] == nil then
                    foreign_items_by_room[bat_room] = {}
                end
                -- print("adding item to "..tostring(bat_room))
                table.insert(foreign_items_by_room[bat_room], current_bat_ap_item)
            else
                -- set AP item room and position for new room, or to invalid room
                if foreign_items_by_room[bat_room] ~= nil and foreign_items_by_room[bat_room][1] ~= nil
                            and BatCanTouchForeign(foreign_items_by_room[bat_room][1], bat_room) then
                    if current_bat_ap_item ~= foreign_items_by_room[bat_room][1] then
                        current_bat_ap_item = foreign_items_by_room[bat_room][1]
                        -- print("Changing bat item to "..tostring(current_bat_ap_item.short_location_id))
                    end
                    memory.write_u8(BatAPItemRam, bat_room)
                    memory.write_u8(BatAPItemRam + 1, current_bat_ap_item.room_x)
                    memory.write_u8(BatAPItemRam + 2, current_bat_ap_item.room_y)
                else
                    memory.write_u8(BatAPItemRam, 0xff)
                    if current_bat_ap_item ~= nil then
                        -- print("clearing bat item")
                    end
                    current_bat_ap_item = nil
                end
            end
        end
        prev_bat_room = bat_room

        -- update foreign_items_by_room position and room id for bat item if bat carrying an item
        if bat_carrying_ap_item then
            -- this is setting the item using the bat's position, which is somewhat wrong, but I think
            -- there will be more problems with the room not matching sometimes if I use the actual item position
            current_bat_ap_item.room_id = bat_room
            current_bat_ap_item.room_x = u8(batRoomAddr + 1)
            current_bat_ap_item.room_y = u8(batRoomAddr + 2)
        end

        if (alive_mode()) then
            if (current_player_room ~= prev_player_room) then
                memory.write_u8(APItemRam, 0xFF, "System Bus")
                prev_ap_room_index = 0
                prev_player_room = current_player_room
                AutocollectFromRoom()
            end
            local carry_item = memory.read_u8(carryAddress, "System Bus")
            bat_no_touch_items[carry_item] = nil
            if (next_inventory_item ~= nil) then
                if ( carry_item == nullObjectId and last_carry_item == nullObjectId ) then
                    frames_with_no_item = frames_with_no_item + 1
                    if (frames_with_no_item > 10) then
                        frames_with_no_item = 10
                        local input_value = memory.read_u8(input_button_address, "System Bus")
                        if( input_value >= 64 and input_value < 128 ) then -- high bit clear, second highest bit set
                            memory.write_u8(carryAddress, next_inventory_item)
                            local item_ram_location = memory.read_u8(ItemTableStart + next_inventory_item)
                            if( memory.read_u8(batCarryAddress) ~= 0x78 and
                                    memory.read_u8(batCarryAddress) == item_ram_location) then
                                memory.write_u8(batCarryAddress, batInvalidCarryItem)
                                memory.write_u8(batCarryAddress+ 1, 0)
                                memory.write_u8(item_ram_location, current_player_room)
                                memory.write_u8(item_ram_location + 1, memory.read_u8(PlayerRoomAddr + 1))
                                memory.write_u8(item_ram_location + 2, memory.read_u8(PlayerRoomAddr + 2))
                            end
                            ItemIndex = ItemIndex + 1
                            next_inventory_item = nil
                        end
                    end
                else
                    frames_with_no_item = 0
                end
            end
            if( carry_item ~= last_carry_item ) then
                if ( localItemLocations ~= nil and localItemLocations[tostring(carry_item)] ~= nil ) then
                    pending_local_items_collected[localItemLocations[tostring(carry_item)]] =
                        localItemLocations[tostring(carry_item)]
                    localItemLocations[tostring(carry_item)] = nil
                    skip_inventory_items[carry_item] = carry_item
                end
            end
            last_carry_item = carry_item

            CheckCollectAPItem(carry_item, APItemValue, APItemRam, rendering_foreign_item)
            if CheckCollectAPItem(carry_item, BatAPItemValue, BatAPItemRam, current_bat_ap_item) and bat_carrying_ap_item then
                memory.write_u8(batCarryAddress, batInvalidCarryItem)
                memory.write_u8(batCarryAddress+ 1, 0)
            end


            rendering_foreign_item = nil
            if( foreign_items_by_room[current_player_room] ~= nil ) then
                if( foreign_items_by_room[current_player_room][prev_ap_room_index] ~= nil ) and memory.read_u8(APItemRam) ~= 0xff then
                    foreign_items_by_room[current_player_room][prev_ap_room_index].room_x = memory.read_u8(APItemRam + 1)
                    foreign_items_by_room[current_player_room][prev_ap_room_index].room_y = memory.read_u8(APItemRam + 2)
                end
                prev_ap_room_index = prev_ap_room_index + 1
                local invalid_index = -1
                if( foreign_items_by_room[current_player_room][prev_ap_room_index] == nil ) then
                    prev_ap_room_index = 1
                end
                if( foreign_items_by_room[current_player_room][prev_ap_room_index] ~= nil and current_bat_ap_item ~= nil and
                    foreign_items_by_room[current_player_room][prev_ap_room_index].short_location_id == current_bat_ap_item.short_location_id) then
                    invalid_index = prev_ap_room_index
                    prev_ap_room_index = prev_ap_room_index + 1
                    if( foreign_items_by_room[current_player_room][prev_ap_room_index] == nil ) then
                        prev_ap_room_index = 1
                    end
                end

                if( foreign_items_by_room[current_player_room][prev_ap_room_index] ~= nil and prev_ap_room_index ~= invalid_index ) then
                    memory.write_u8(APItemRam, current_player_room)
                    rendering_foreign_item = foreign_items_by_room[current_player_room][prev_ap_room_index]
                    memory.write_u8(APItemRam + 1, rendering_foreign_item.room_x)
                    memory.write_u8(APItemRam + 2, rendering_foreign_item.room_y)
                else
                    memory.write_u8(APItemRam, 0xFF, "System Bus")
                end
            end
            if is_dead == 0 then
                dragons_revived = false
                player_dead = false
                new_dragon_state = {0,0,0}
                for index, dragon_state_addr in pairs(DragonState) do
                    new_dragon_state[index] = memory.read_u8(dragon_state_addr, "System Bus" )
                    if last_dragon_state[index] == 1 and new_dragon_state[index] ~= 1 then
                        dragons_revived = true
                    elseif last_dragon_state[index] ~= 1 and new_dragon_state[index] == 1 then
                        dragon_real_index = index - 1
                        print("Killed dragon: "..tostring(dragon_real_index))
                        local dragon_item = {}
                        dragon_item["short_location_id"] = 0xD0 + dragon_real_index
                        pending_foreign_items_collected[dragon_item.short_location_id] = dragon_item
                    end
                    if new_dragon_state[index] == 2 then
                        player_dead = true
                    end
                end
                if dragons_revived and player_dead == false then
                    TryFreeincarnate()
                end
                last_dragon_state = new_dragon_state
            end
        elseif (u8(PlayerRoomAddr) == 0x00) then -- not alive mode, in number room
            ItemIndex = 0  -- reset our inventory
            next_inventory_item = nil
            skip_inventory_items = {}
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 5 == 0) then
                receive()
                if alive_mode() then
                    local was_dead = is_dead
                    is_dead = 0
                    for index, dragonStateAddr in pairs(DragonState) do
                        local dragonstateval = memory.read_u8(dragonStateAddr, "System Bus")
                        if ( dragonstateval == 2) then
                            is_dead = index
                        end
                    end
                    if was_dead ~= 0 and is_dead == 0 then
                        TryFreeincarnate()
                    end
                    if deathlink_rec == true and is_dead == 0 then
                        print("setting dead from deathlink")
                        deathlink_rec = false
                        deathlink_sent = true
                        is_dead = 1
                        memory.write_u8(carryAddress, nullObjectId, "System Bus")
                        memory.write_u8(DragonState[1], 2, "System Bus")
                    end
                    if (is_dead > 0 and deathlink_send == 0 and not deathlink_sent) then
                        deathlink_send = is_dead
                        print("setting deathlink_send to "..tostring(is_dead))
                    elseif (is_dead == 0) then
                        deathlink_send = 0
                        deathlink_sent = false
                    end
                    if ItemsReceived ~= nil and ItemsReceived[ItemIndex + 1] ~= nil then
                        while ItemsReceived[ItemIndex + 1] ~= nil and skip_inventory_items[ItemsReceived[ItemIndex + 1]] ~= nil do
                            print("skip")
                            ItemIndex = ItemIndex + 1
                        end
                        local static_id = ItemsReceived[ItemIndex + 1]
                        if static_id ~= nil then
                            inventory[static_id] = 1
                            if next_inventory_item == nil then
                                next_inventory_item = static_id
                            end
                        end
                    end
                end
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            if  (frame % 60 == 0) then

                print("Waiting for client.")

                emu.frameadvance()
                server:settimeout(2)
                print("Attempting to connect")
                local client, timeout = server:accept()
                if timeout == nil then
                    print("Initial connection made")
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    atariSocket = client
                    atariSocket:settimeout(0)
                end
            end
        end
        emu.frameadvance()
    end
end

main()
