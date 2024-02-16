local socket = require("socket")
local json = require('json')
local math = require('math')
require("common")


local zones = {
	0x189c, "ST0", 0x8704, "ARE", 0xb6d4, "CAT", 0x0e7C, "CEN", 0xdea4, "CHI", 0x5fb8, "DAI", 0x6fc0, "DRE", 0xf160, "LIB", 0x37B8, "NO0", 0x1a20, "NO1", 0x8744, "NO2", 0x187c, "NO3", 0x90ec, "NP3", 0xa620, "NO4",
	0x9504, "NZ0", 0xc710, "NZ1", 0xd660, "TOP", 0x8218, "WRP", 0x6b70, "RARE",0x3f80, "RCAT", 0x049c, "RCEN", 0xac24, "RCHI", 0x465c, "RDAI", 0x2b90, "RLIB", 0x7354, "RNO0", 0x9ccc, "RNO1", 0x6d20, "RNO2", 0x3ee0, "RNO3",
	0xA214, "RNO4", 0xcc34, "RNZ0", 0xced0, "RNZ1", 0x2524, "RTOP", 0xa198, "RWRP", 0xc10c, "BO0", 0x55d0, "BO1", 0x76a0, "BO2", 0x6734, "BO3", 0x69ec, "BO4", 0x6be4, "BO5", 0x9b84, "BO6", 0x6678, "BO7", 0xa094, "RBO0", 0x5174, "RBO1",
	0x1ab0, "RBO2", 0x31c8, "RBO3", 0x8e3c, "RBO4", 0x5920, "RBO5", 0x54ec, "RBO6", 0x5f04, "RBO7", 0x9dc8, "RBO8",
}

-- id, name, address
local allItems = {1, "Monster vial 1", 0x09798B, 2, "Monster vial 2", 0x09798C, 3, "Monster vial 3", 0x09798D, 4, "Shield rod", 0x09798E, 5, "Leather shield", 0x09798F, 6, "Knight shield", 0x097990, 7, "Iron shield", 0x097991, 8, "AxeLord shield", 0x097992, 9, "Herald shield", 0x097993,
				10, "Dark shield", 0x097994, 11, "Goddess shield", 0x097995, 12, "Shaman shield", 0x097996, 13, "Medusa shield", 0x097997, 14, "Skull shield", 0x097998, 15, "Fire shield", 0x097999, 16, "Alucard shield", 0x09799A, 17, "Sword of dawn", 0x09799B,
				18, "Basilard", 0x09799C, 19, "Short sword", 0x09799D, 20, "Combat knife", 0x09799E, 21, "Nunchaku", 0x09799F, 22, "Were bane", 0x0979A0, 23, "Rapier", 0x0979A1, 24, "Karma coin", 0x0979A2, 25, "Magic missile", 0x0979A3, 26, "Red rust", 0x0979A4,
				27, "Takemitsu", 0x0979A5, 28, "Shotel", 0x0979A6, 29, "Orange", 0x0979A7, 30, "Apple", 0x0979A8, 31, "Banana", 0x0979A9, 32, "Grapes", 0x0979AA, 33, "Strawberry", 0x0979AB, 34, "Pineapple", 0x0979AC, 35, "Peanuts", 0x0979AD,
				36, "Toadstool", 0x0979AE, 37, "Shiitake", 0x0979AF, 38, "Cheesecake", 0x0979B0, 39, "Shortcake", 0x0979B1, 40, "Tart", 0x0979B2, 41, "Parfait", 0x0979B3, 42, "Pudding", 0x0979B4,	43, "Ice cream", 0x0979B5, 44, "Frankfurter", 0x0979B6,
				45, "Hamburger", 0x0979B7, 46, "Pizza", 0x0979B8, 47, "Cheese", 0x0979B9, 48, "Ham and eggs", 0x0979BA, 49, "Omelette", 0x0979BB, 50, "Morning set", 0x0979BC, 51, "Lunch A", 0x0979BD, 52, "Lunch B", 0x0979BE, 53, "Curry rice", 0x0979BF,
				54, "Gyros plate", 0x0979C0, 55, "Spaghetti", 0x0979C1, 56, "Grape juice", 0x0979C2, 57, "Barley tea", 0x0979C3, 58, "Green tea", 0x0979C4, 59, "Natou", 0x0979C5, 60, "Ramen", 0x0979C6, 61, "Miso soup", 0x0979C7, 62, "Sushi", 0x0979C8,
				63, "Pork bun", 0x0979C9, 64, "Red bean bun", 0x0979CA, 65, "Chinese bun", 0x0979CB, 66, "Dim sum set", 0x0979CC, 67, "Pot roast", 0x0979CD, 68, "Sirloin", 0x0979CE, 69, "Turkey", 0x0979CF, 70, "Meal ticket", 0x0979D0, 71, "Neutron bomb", 0x0979D1,
				72, "Power of Sire", 0x0979D2, 73, "Pentagram", 0x0979D3, 74, "Bat Pentagram", 0x0979D4, 75, "Shuriken", 0x0979D5, 76, "Cross shuriken", 0x0979D6, 77, "Buffalo star", 0x0979D7, 78, "Flame star", 0x0979D8, 79, "TNT", 0x0979D9,
				80, "Bwaka knife", 0x0979DA, 81, "Boomerang", 0x0979DB, 82, "Javelin", 0x0979DC, 83, "Tyrfing", 0x0979DD, 84, "Namakura", 0x0979DE, 85, "Knuckle duster", 0x0979DF, 86, "Gladius", 0x0979E0, 87, "Scimitar", 0x0979E1, 88, "Cutlass", 0x0979E2,
				89, "Saber", 0x0979E3, 90, "Falchion", 0x0979E4, 91, "Broadsword", 0x0979E5, 92, "Bekatowa", 0x0979E6, 93, "Damascus sword", 0x0979E7, 94, "Hunter sword", 0x0979E8, 95, "Estoc", 0x0979E9, 96, "Bastard sword", 0x0979EA, 97, "Jewel knuckles", 0x0979EB,
				98, "Claymore", 0x0979EC, 99, "Talwar", 0x0979ED, 100, "Katana", 0x0979EE, 101, "Flamberge", 0x0979EF, 102, "Iron Fist", 0x0979F0, 103, "Zwei hander", 0x0979F1, 104, "Sword of hador", 0x0979F2, 105, "Luminus", 0x0979F3, 106, "Harper", 0x0979F4,
				107, "Obsidian sword", 0x0979F5, 108, "Gram", 0x0979F6, 109, "Jewel sword", 0x0979F7, 110, "Mormegil", 0x0979F8, 111, "Firebrand", 0x0979F9, 112, "Thunderbrand", 0x0979FA, 113, "Icebrand", 0x0979FB, 114, "Stone sword", 0x0979FC,
				115, "Holy sword", 0x0979FD, 116, "Terminus est", 0x0979FE, 117, "Marsil", 0x0979FF, 118, "Dark blade", 0x097A00, 119, "Heaven sword", 0x097A01, 120, "Fist of Tulkas", 0x097A02, 121, "Gurthang", 0x097A03, 122, "Mourneblade", 0x097A04,
				123, "Alucard sword", 0x097A05, 124, "Mablung sword", 0x097A06, 125, "Badelaire", 0x097A07,	126, "Sword familiar", 0x097A08, 127, "Great sword", 0x097A09, 128, "Mace", 0x097A0A, 129, "Morningstar", 0x097A0B, 130, "Holy rod", 0x097A0C,
				131, "Star flail", 0x097A0D, 132, "Moon rod", 0x097A0E, 133, "Chakram", 0x097A0F, 134, "Fire boomerang", 0x097A10, 135, "Iron ball", 0x097A11, 136, "Holbein dagger", 0x097A12, 137, "Blue knuckles", 0x097A13, 138, "Dynamite", 0x097A14,
				139, "Osafune katana", 0x097A15, 140, "Masamune", 0x097A16, 141, "Muramasa", 0x097A17, 142, "Heart refresh", 0x097A18, 143, "Runesword", 0x097A19, 144, "Antivenom", 0x097A1A, 145, "Uncurse", 0x097A1B, 146, "Life apple", 0x097A1C,
				147, "Hammer", 0x097A1D, 148, "Str. potion", 0x097A1E, 149, "Luck potion", 0x097A1F, 150, "Smart potion", 0x097A20, 151, "Attack potion", 0x097A21, 152, "Shield potion", 0x097A22,	153, "Resist fire", 0x097A23, 154, "Resist thunder", 0x097A24,
				155, "Resist ice", 0x097A25, 156, "Resist stone", 0x097A26, 157, "Resist holy", 0x097A27, 158, "Resist dark", 0x097A28, 159, "Potion", 0x097A29, 160, "High potion", 0x097A2A, 161, "Elixir", 0x097A2B, 162, "Manna prism", 0x097A2C,
				163, "Vorpal blade", 0x097A2D, 164, "Crissaegrim", 0x097A2E, 165, "Yasutsuna", 0x097A2F, 166, "Library card", 0x097A30, 167, "Alucart shield", 0x097A31, 168, "Alucart sword", 0x097A32, 170, "Cloth tunic", 0x097A34, 171, "Hide cuirass", 0x097A35,
				172, "Bronze cuirass", 0x097A36, 173, "Iron cuirass", 0x097A37, 174, "Steel cuirass", 0x097A38, 175, "Silver plate", 0x097A39, 176, "Gold plate", 0x097A3A, 177, "Platinum mail", 0x097A3B, 178, "Diamond plate", 0x097A3C, 179, "Fire mail", 0x097A3D,
				180, "Lightning mail", 0x097A3E, 181, "Ice mail", 0x097A3F, 182, "Mirror cuirass", 0x097A40, 183, "Spike breaker", 0x097A41, 184, "Alucard mail", 0x097A42,	185, "Dark armor", 0x097A43, 186, "Healing mail", 0x097A44, 187, "Holy mail", 0x097A45,
				188, "Walk armor", 0x097A46, 189, "Brilliant mail", 0x097A47, 190, "Mojo mail", 0x097A48, 191, "Fury plate", 0x097A49, 192, "Dracula tunic", 0x097A4A, 193, "God's garb", 0x097A4B, 194, "Axe Lord armor", 0x097A4C, 196, "Sunglasses", 0x097A4E,
				197, "Ballroom mask", 0x097A4F, 198, "Bandanna", 0x097A50, 199, "Felt hat", 0x097A51, 200, "Velvet hat", 0x097A52, 201, "Goggles", 0x097A53, 202, "Leather hat", 0x097A54, 203, "Holy glasses", 0x097A55, 204, "Steel helm", 0x097A56,
				205, "Stone mask", 0x097A57, 206, "Circlet", 0x097A58, 207, "Gold circlet", 0x097A59, 208, "Ruby circlet", 0x097A5A, 209, "Opal circlet", 0x097A5B, 210, "Topaz circlet", 0x097A5C, 211, "Beryl circlet", 0x097A5D, 212, "Cat-eye circl.", 0x097A5E,
				213, "Coral circlet", 0x097A5F, 214, "Dragon helm", 0x097A60, 215, "Silver crown", 0x097A61, 216, "Wizard hat", 0x097A62, 218, "Cloth cape", 0x097A64, 219, "Reverse cloak", 0x097A65, 220, "Elven cloak", 0x097A66, 221, "Crystal cloak", 0x097A67,
				222, "Royal cloak", 0x097A68, 223, "Blood cloak", 0x097A69, 224, "Joseph's cloak", 0x097A6A, 225, "Twilight cloak", 0x097A6B, 227, "Moonstone", 0x097A6D, 228, "Sunstone", 0x097A6E, 229, "Bloodstone", 0x097A6F, 230, "Staurolite", 0x097A70,
				231, "Ring of pales", 0x097A71, 232, "Zircon", 0x097A72, 233, "Aquamarine", 0x097A73, 234, "Turquoise", 0x097A74, 235, "Onyx", 0x097A75, 236, "Garnet", 0x097A76, 237, "Opal", 0x097A77, 238, "Diamond", 0x097A78, 239, "Lapis lazuli", 0x097A79,
				240, "Ring of ares", 0x097A7A, 241, "Gold ring", 0x097A7B, 242, "Silver ring", 0x097A7C, 243, "Ring of varda", 0x097A7D, 244, "Ring of arcana", 0x097A7E, 245, "Mystic pendant", 0x097A7F, 246, "Heart broach", 0x097A80, 247, "Necklace of j", 0x097A81,
				248, "Gauntlet", 0x097A82, 249, "Ankh of life", 0x097A83, 250, "Ring of feanor", 0x097A84, 251, "Medal", 0x097A85, 252, "Talisman", 0x097A86, 253, "Duplicator", 0x097A87, 254, "King's stone", 0x097A88, 255, "Covenant stone", 0x097A89,
				256, "Nauglamir", 0x097A8A,	257, "Secret boots", 0x097A8B, 258, "Alucart mail", 0x097a8c, 300, "Soul of bat", 0x097964, 301, "Fire of bat", 0x097965, 302, "Echo of bat", 0x097966, 303, "Force of echo", 0x097967, 304, "Soul of wolf", 0x097968,
				305, "Power of wolf", 0x097969,	306, "Skill of wolf", 0x09796A, 307, "Form of mist", 0x09796B, 308, "Power of mist", 0x09796C, 309, "Gas cloud", 0x09796D, 310, "Cube of zoe", 0x09796E, 311, "Spirit orb", 0x09796F, 312, "Gravity boots", 0x097970,
				313, "Leap stone", 0x097971, 314, "Holy symbol", 0x097972, 315, "Faerie scroll", 0x097973, 316, "Jewel of open", 0x097974, 317, "Merman statue", 0x097975, 318, "Bat card", 0x097976, 319, "Ghost card", 0x097977, 320, "Faerie card", 0x097978,
				321, "Demon card", 0x097979, 322, "Sword card", 0x09797A, 325, "Heart of vlad", 0x09797D, 326, "Tooth of vlad", 0x09797E, 327, "Rib of vlad", 0x09797F, 328, "Ring of vlad", 0x097980, 329, "Eye of vlad", 0x097981, 412, "Heart Vessel", 0x000001,
				423, "Life Vessel", 0x000001,
}

local cur_zone = "ST0"
local cur_zoneid = 1
local last_zone = "ST0"
local last_zoneid = 1
local dracula_dead = false
local dracula_timer = 0
local bosses_dead = 0
local just_died = false
local first_connect = true
local got_data = true
local last_status = 0  -- 1 game connect / 2 in-game / 4 on Richter / 8 just left STO / 10 Alucard / 20 just died
local goal_met = false


local player_name = ""
local seed = ""

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local SCRIPT_VERSION = 1

local ItemsReceived = {}
local ItemsReceivedQueue = {}
local MsgReceived = {}
local last_item_processed = 1
local last_processed_read = 1024
local num_item_processed = 0
local start_item_drawing = 0
local misplaced_drawing = 0
local num_misplaced_processed = 0
local delay_timer = 0
local checked_locations = {}
local all_location_table = {}
local bosses = {}
local misplaced_items = {}
local misplaced_items_queue = {}
local misplaced_read = {}
local last_misplaced_save = 0
local last_misplaced_processed = 0
local item1 = ""
local item2 = ""
local item3 = ""
local item4 = ""
local m_item1 = ""
local m_item2 = ""
local m_item3 = ""
local m_item4 = ""

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local sotnSocket = nil
local frame = 0

-- TODO: I guess there is a bug when the client try to send an item with a pause screen active
-- Display msg had some issues when items are sent on misplaced locations
-- Looks like there is a bug when granting a item and you have one equipped
-- While drawing the misplaced received. grant misplaced stop working. Maybe implement a queue

function getCurrZone()
	local z = mainmemory.read_u16_le(0x180000)
	local size = table.getn(zones)

	if z == zones[cur_zoneid] then return end

	for i = 1, size, 2 do
		if zones[i] == z then
			last_zoneid = cur_zoneid
			last_zone = cur_zone
			cur_zoneid = i
			cur_zone = zones[i + 1]
			break
		end
	end
end

function checkVictory(f)
	if dracula_timer == 0 then
		dracula_timer = f
	end
	if dracula_timer > 0 and f - dracula_timer > 500 then -- Shaft/Dracula share hp. Give some time to Dracula HP is loaded on memory
		local cur_hp = mainmemory.read_u16_le(0x076ed6)
		if cur_hp == 0 or cur_hp > 60000 then
			dracula_dead = true
		end
	end
end

function grant_item_byid(num_id)
	if num_id == nil then
		console.log("Error num_id is nil")
		return
	end
	size = table.getn(allItems)
	local address = 0
	local itemqty = 0
	local itemid = 0
	if type(num_id) == "string" then itemid = tonumber(num_id)
	else itemid = num_id end

	for i = 1, size, 3 do
		if allItems[i] == itemid then
			address = allItems[i+2]
			name = allItems[i+1]
			break
		end
	end
	if address ~= 0 then
		if itemid >= 300 and itemid < 400 then
			if mainmemory.read_u8(address) == 0 then
				if itemid >= 318 and itemid <= 322 then mainmemory.write_u8(address, 1)
				else mainmemory.write_u8(address, 3) end
			end
		elseif itemid > 400 then
			if itemid == 423 then
				max_hp = mainmemory.read_u32_le(0x097ba4)
				max_hp = max_hp + 5
				mainmemory.write_u32_le(0x097ba4, max_hp)
			elseif itemid == 412 then
				max_heart = mainmemory.read_u32_le(0x097bac)
				max_heart = max_heart + 5
				mainmemory.write_u32_le(0x097bac, max_heart)
			end
		else
			itemqty = mainmemory.read_u8(address)
			if itemqty < 255 then itemqty = itemqty + 1 end
			if itemqty == 1 then
				organize_inventory(itemid)
			end
			mainmemory.write_u8(address, itemqty)
		end
	else
		if itemid ~= nil then console.log("Item " .. num_id .. " not found!")
		else console.log("Item nil not found!") end
	end
	return name
end

function organize_inventory(item_id)
	max_index = 0
	start_address = 0
	item_offset = 0
	start_byte = 0x00

	if item_id > 0 and item_id <= 168 then --hand
		start_address = 0x097a8d
		qty_start_address = 0x09798a
		max_index = 168
	elseif (item_id > 168 and item_id <= 194) or item_id == 258 then --chest 258 Alucart mail
		start_address = 0x097b36
		qty_start_address = 0x097a33
		max_index = 27
		item_offset = 169
	elseif item_id > 195 and item_id <= 216 then --helm
		start_address = 0x097b50
		qty_start_address = 0x097a4d
		max_index = 21
		item_offset = 195
		start_byte = 0x1a
	elseif item_id > 217 and item_id <= 225 then --cloak
		start_address = 0x097b66
		qty_start_address = 0x097a63
		max_index = 8
		item_offset = 217
		start_byte = 0x30
	elseif item_id > 226 and item_id <= 257 then --trinket
		start_address = 0x097b6f
		qty_start_address = 0x097a6c
		max_index = 31
		item_offset = 226
		start_byte = 0x39
	end

	-- Find the first empty slot
	for i = 1, max_index, 1 do
		address = start_address + i
		old_byte = mainmemory.read_u8(address)
		qty_address = qty_start_address + old_byte - start_byte

		if mainmemory.read_u8(qty_address) == 0 then
			new_value = item_id - item_offset + start_byte
			for j = i, max_index, 1 do
				new_address = start_address + j
				if mainmemory.read_u8(new_address) == new_value then
					mainmemory.write_u8(address, new_value)
					mainmemory.write_u8(new_address, old_byte)
					break
				end
			end
			break
		end
	end
end

function on_loadstate()
	all_location_table = checkAllLocations()
	first_connect = false
	just_died = false
	dracula_timer = 0
	console.log("Load stated. TODO")
end

function check_death()
	hp = mainmemory.read_u32_le(0x097ba0)
	if not just_died and hp <= 0 then
		just_died = true
	end
end

function processBlock(block)
	if block == nil then
        return
    end
    local block_identified = 0
    local msgBlock = block['messages']
    if msgBlock ~= nil and next(msgBlock) ~= nil then
        block_identified = 1
        for i, v in pairs(msgBlock) do
			table.insert(MsgReceived, v)
        end
    end
    local itemsBlock = block["items"]
    if itemsBlock ~= nil and next(itemsBlock) ~= nil then
        block_identified = 1
		if start_item_drawing ~= 0 or misplaced_drawing ~= 0 then
			ItemsReceivedQueue = itemsBlock
		else
			ItemsReceived = itemsBlock
		end
    end
	local checkedLocationsBlock = block["checked_locations"]
	if checkedLocationsBlock ~= nil and next(checkedLocationsBlock) ~= nil then
        block_identified = 1
		checked_locations = checkedLocationsBlock
    end
	local misplacedBlock = block["misplaced"]
	if misplacedBlock ~= nil and next(misplacedBlock) ~= nil then
		block_identified = 1
		local item = 0
		local item_exist = false
		-- We received an item. Check if the last one on misplaced_items is the same and add it.
		if misplacedBlock[#misplacedBlock] ~= misplaced_items[#misplaced_items] then
			local received = tonumber(misplacedBlock[#misplacedBlock])
			if start_item_drawing ~= 0 or misplaced_drawing ~= 0 then
				if misplace_items_queue[#misplaced_items_queue] ~= received then
					table.insert(misplaced_items_queue, received)
				end
			else
				table.insert(misplaced_items, received)
			end
		end
	end
	local playerBlock = block["player"]
	if playerBlock ~= nil then
		block_identified = 1
		player_name = tostring(playerBlock)
	end
	local seedBlock = block["seed_name"]
	if seedBlock ~= nil then
		block_identified = 1
		seed = tostring(seedBlock)
	end

    if( block_identified == 0 ) then
        print("unidentified block")
        print(block)
    end
end

function receive()
    l, e = sotnSocket:receive()

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

    local retTable = {}
    retTable["scriptVersion"] = SCRIPT_VERSION
	retTable["locations"] = all_location_table
	retTable["bosses"] = bosses


    msg = json.encode(retTable).."\n"
    local ret, error = sotnSocket:send(msg)
    if ret == nil then
        print(error)
    elseif curstate == STATE_INITIAL_CONNECTION_MADE then
        curstate = STATE_TENTATIVELY_CONNECTED
    elseif curstate == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        curstate = STATE_OK
    end
end

function checkARE()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf06)
	checks["ARE - Heart Vessel"] = bit.check(flag, 0)
	checks["ARE - Shield rod"] = bit.check(flag, 1)
	checks["ARE - Blood cloak"] = bit.check(flag, 3)
	checks["ARE - Knight shield(Chapel passage)"] = bit.check(flag, 4)
	checks["ARE - Library card"] = bit.check(flag, 5)
	checks["ARE - Green tea"] = bit.check(flag, 6)
	checks["ARE - Holy sword(Hidden attic)"] = bit.check(flag, 7)
	if mainmemory.read_u16_le(0x03ca38) ~= 0 then
		bosses["Minotaurus/Werewolf"] = true
	else
		bosses["Minotaurus/Werewolf"] = false
	end
	if cur_zone == "ARE" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x2e90 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 222)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 135)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Form of Mist"] = true end
		end
	end

	return checks
end

function checkCAT()
	local checks = {}
	--local flag = mainmemory.read_u32_le(0x03befc)
	local flag = mainmemory.read_u24_le(0x03befc)
	checks["CAT - Cat-eye circl."] = bit.check(flag, 0)
	checks["CAT - Icebrand"] = bit.check(flag, 1)
	checks["CAT - Walk armor"] = bit.check(flag, 2)
	checks["CAT - Mormegil"] = bit.check(flag, 3)
	checks["CAT - Library card(Spike breaker)"] = bit.check(flag, 4)
	checks["CAT - Heart Vessel(Ballroom mask)"] = bit.check(flag, 6)
	checks["CAT - Ballroom mask"] = bit.check(flag, 7)
	checks["CAT - Bloodstone"] = bit.check(flag, 8)
	checks["CAT - Life Vessel(Crypt)"] = bit.check(flag, 9)
	checks["CAT - Heart Vessel(Crypt)"] = bit.check(flag, 10)
	checks["CAT - Cross shuriken 1(Spike breaker)"] = bit.check(flag, 11)
	checks["CAT - Cross shuriken 2(Spike breaker)"] = bit.check(flag, 12)
	checks["CAT - Karma coin 1(Spike breaker)"] = bit.check(flag, 13)
	checks["CAT - Karma coin 2(Spike breaker)"] = bit.check(flag, 14)
	checks["CAT - Pork bun"] = bit.check(flag, 15)
	checks["CAT - Spike breaker"] = bit.check(flag, 16)
	checks["CAT - Monster vial 3 1(Sarcophagus)"] = bit.check(flag, 17)
	checks["CAT - Monster vial 3 2(Sarcophagus)"] = bit.check(flag, 18)
	checks["CAT - Monster vial 3 3(Sarcophagus)"] = bit.check(flag, 19)
	checks["CAT - Monster vial 3 4(Sarcophagus)"] = bit.check(flag, 20)
	if mainmemory.read_u16_le(0x03ca34) ~= 0 then
		bosses["Legion"] = true
	else
		bosses["Legion"] = false
	end

	return checks
end

function checkCHI()
	local checks = {}
	-- local flag = mainmemory.read_u32_le(0x03bf02)
	local flag = mainmemory.read_u16_le(0x03bf02)
	checks["CHI - Power of sire(Demon)"] = bit.check(flag, 0)
	checks["CHI - Karma coin"] = bit.check(flag, 1)
	checks["CHI - Ring of ares"] = bit.check(flag, 4)
	checks["CHI - Combat knife"] = bit.check(flag, 5)
	checks["CHI - Shiitake 1"] = bit.check(flag, 6)
	checks["CHI - Shiitake 2"] = bit.check(flag, 7)
	checks["CHI - Barley tea(Demon)"] = bit.check(flag, 8)
	checks["CHI - Peanuts 1(Demon)"] = bit.check(flag, 9)
	checks["CHI - Peanuts 2(Demon)"] = bit.check(flag, 10)
	checks["CHI - Peanuts 3(Demon)"] = bit.check(flag, 11)
	checks["CHI - Peanuts 4(Demon)"] = bit.check(flag, 12)
	checks["CHI - Turkey(Demon)"] = bit.check(mainmemory.readbyte(0x03be3d), 0)
	if mainmemory.read_u16_le(0x03ca5c) ~= 0 then
		bosses["Cerberos"] = true
	else
		bosses["Cerberos"] = false
	end
	if cur_zone == "CHI" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x19b8 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 88)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Demon Card"] = true end
		end
	end

	return checks
end

function checkDAI()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03beff)
	checks["DAI - Ankh of life(Stairs)"] = bit.check(flag, 0)
	checks["DAI - Morningstar"] = bit.check(flag, 1)
	checks["DAI - Silver ring"] = bit.check(flag, 2)
	checks["DAI - Aquamarine(Stairs)"] = bit.check(flag, 3)
	checks["DAI - Mystic pendant"] = bit.check(flag, 4)
	checks["DAI - Magic missile(Stairs)"] = bit.check(flag, 5)
	checks["DAI - Shuriken(Stairs)"] = bit.check(flag, 6)
	checks["DAI - TNT(Stairs)"] = bit.check(flag, 7)
	checks["DAI - Boomerang(Stairs)"] = bit.check(flag, 8)
	checks["DAI - Goggles"] = bit.check(flag, 9)
	checks["DAI - Silver plate"] = bit.check(flag, 10)
	checks["DAI - Str. potion(Bell)"] = bit.check(flag, 11)
	checks["DAI - Life Vessel(Bell)"] = bit.check(flag, 12)
	checks["DAI - Zircon"] = bit.check(flag, 13)
	checks["DAI - Cutlass"] = bit.check(flag, 14)
	checks["DAI - Potion"] = bit.check(flag, 15)
	if mainmemory.read_u16_le(0x03ca44) ~= 0 then
		bosses["Hippogryph"] = true
	else
		bosses["Hippogryph"] = false
	end

	return checks
end

function checkLIB()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03befa)
	checks["LIB - Stone mask"] = bit.check(flag, 1)
	checks["LIB - Holy rod"] = bit.check(flag, 2)
	checks["LIB - Bronze cuirass"] = bit.check(flag, 4)
	checks["LIB - Takemitsu"] = bit.check(flag, 5)
	checks["LIB - Onyx"] = bit.check(flag, 6)
	checks["LIB - Frankfurter"] = bit.check(flag, 7)
	checks["LIB - Potion"] = bit.check(flag, 8)
	checks["LIB - Antivenom"] = bit.check(flag, 9)
	checks["LIB - Topaz circlet"] = bit.check(flag, 10)
	if mainmemory.read_u16_le(0x03ca6c) ~= 0 then
		bosses["Lesser Demon"] = true
	else
		bosses["Lesser Demon"] = false
	end
	if cur_zone == "LIB" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x2ec4 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 1051)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 919)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= 5 then checks["Soul of Bat"] = true end
		end
		if room == 0x2f0c then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 1681)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 80 -- Increased offset
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Faerie Scroll"] = true end
		end
		if room == 0x2ee4 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 230)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 135)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Jewel of Open"] = true end
		end
		if room == 0x2efc then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 48)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Faerie Card"] = true end
		end
	end

	return checks
end

function checkNO0()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03beec)
	checks["NO0 - Life Vessel(Left clock)"] = bit.check(flag, 0)
	checks["NO0 - Alucart shield"] = bit.check(flag, 1)
	checks["NO0 - Heart Vessel(Right clock)"] = bit.check(flag, 2)
	checks["NO0 - Life apple(Middle clock)"] = bit.check(flag, 3)
	checks["NO0 - Hammer(Middle clock)"] = bit.check(flag, 4)
	checks["NO0 - Potion(Middle clock)"] = bit.check(flag, 5)
	checks["NO0 - Alucart mail"] = bit.check(flag, 6)
	checks["NO0 - Alucart sword"] = bit.check(flag, 7)
	checks["NO0 - Life Vessel(Inside)"] = bit.check(flag, 8)
	checks["NO0 - Heart Vessel(Inside)"] = bit.check(flag, 9)
	checks["NO0 - Library card(Jewel)"] = bit.check(flag, 10)
	checks["NO0 - Attack potion(Jewel)"] = bit.check(flag, 11)
	checks["NO0 - Hammer(Spirit)"] = bit.check(flag, 12)
	checks["NO0 - Str. potion"] = bit.check(flag, 13)
	checks["NO0 - Holy glasses"] = bit.check(mainmemory.read_u8(0x03bec4), 0)
	if cur_zone == "NO0" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x27f4 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 130)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 1080)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Spirit Orb"] = true end
		end
		if room == 0x2884 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 1170)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Gravity Boots"] = true end
		end
	end

	return checks
end

function checkNO1()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03beee)
	checks["NO1 - Jewel knuckles"] = bit.check(flag, 0)
	checks["NO1 - Mirror cuirass"] = bit.check(flag, 1)
	checks["NO1 - Heart Vessel"] = bit.check(flag, 2)
	checks["NO1 - Garnet"] = bit.check(flag, 3)
	checks["NO1 - Gladius"] = bit.check(flag, 4)
	checks["NO1 - Life Vessel"] = bit.check(flag, 5)
	checks["NO1 - Zircon"] = bit.check(flag, 6)
	checks["NO1 - Pot Roast"] = bit.check(mainmemory.readbyte(0x03bdfe), 0)
	if mainmemory.read_u16_le(0x03ca30) ~= 0 then
		bosses["Doppleganger 10"] = true
	else
		bosses["Doppleganger 10"] = false
	end
	if cur_zone == "NO1" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x34f4 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 360)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 807)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Soul of Wolf"] = true end
		end
	end

	return checks
end

function checkNO2()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bef0)
	checks["NO2 - Heart Vessel"] = bit.check(flag, 1)
	checks["NO2 - Broadsword"] = bit.check(flag, 4)
	checks["NO2 - Onyx"] = bit.check(flag, 5)
	checks["NO2 - Cheese"] = bit.check(flag, 6)
	checks["NO2 - Manna prism"] = bit.check(flag, 7)
	checks["NO2 - Resist fire"] = bit.check(flag, 8)
	checks["NO2 - Luck potion"] = bit.check(flag, 9)
	checks["NO2 - Estoc"] = bit.check(flag, 10)
	checks["NO2 - Iron ball"] = bit.check(flag, 11)
	checks["NO2 - Garnet"] = bit.check(flag, 12)
	if mainmemory.read_u16_le(0x03ca2c) ~= 0 then
		bosses["Olrox"] = true
	else
		bosses["Olrox"] = false
	end
	if cur_zone == "NO2" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x330c then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 130)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 135)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Echo of Bat"] = true end
		end
		if room == 0x3314 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 367)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 135)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Sword Card"] = true end
		end
	end

	return checks
end

function checkNO3()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bef2)

	checks["NO3 - Heart Vessel (Above Death)"] = bit.check(flag, 0)
	checks["NO3 - Life Vessel (Bellow shield potion)"] = bit.check(flag, 1)
	checks["NO3 - Life Apple (Hidden room)"] = bit.check(flag, 2)
	checks["NO3 - Shield Potion"] = bit.check(flag, 4)
	checks["NO3 - Holy mail"] = bit.check(flag, 5)
	checks["NO3 - Life Vessel (UC exit)"] = bit.check(flag, 6)
	checks["NO3 - Heart Vessel (Teleport exit)"] = bit.check(flag, 7)
	checks["NO3 - Life Vessel (Above entry)"] = bit.check(flag, 8)
	checks["NO3 - Jewel sword"] = bit.check(flag, 9)
	checks["NO3 - Pot Roast"] = bit.check(mainmemory.readbyte(0x03be1f), 0)
	checks["NO3 - Turkey"] = bit.check(mainmemory.readbyte(0x03be24), 0)
	if cur_zone == "NO3" or cur_zone == "NP3" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x3d40 or room == 0x3af8 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 270)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 103)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Cube of Zoe"] = true end
		end
		if room == 0x3cc8 or room == 0x3a80 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 245)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 183)
			-- NP3 seens a bit offset
			local x2 = math.abs(mainmemory.read_u16_le(0x0973f0) - 270)
			local o = 10
			if (x >= 0 and x <= o and y >= 0 and y <= o) or (x2 >= 0 and x2 <= o and y >= 0 and y <= o) then checks["Power of Wolf"] = true end
		end
	end

	return checks
end

function checkNO4()
	local checks = {}
	local flag = mainmemory.read_u32_le(0x03bef4)
	-- local flag2 = mainmemory.read_u16_le(0x03bef8)
	local flag2 = mainmemory.read_u8(0x03bef8)
	checks["NO4 - Heart Vessel(0)"] = bit.check(flag, 0)
	checks["NO4 - Life Vessel(1)"] = bit.check(flag, 1)
	checks["NO4 - Crystal cloak"] = bit.check(flag, 2)
	checks["NO4 - Antivenom(Underwater)"] = bit.check(flag, 4)
	checks["NO4 - Life Vessel(Underwater)"] = bit.check(flag, 5)
	checks["NO4 - Life Vessel(Behind waterfall)"] = bit.check(flag, 6)
	checks["NO4 - Herald Shield"] = bit.check(flag, 7)
	checks["NO4 - Zircon"] = bit.check(flag, 9)
	checks["NO4 - Bandanna"] = bit.check(flag, 11)
	checks["NO4 - Shiitake(12)"] = bit.check(flag, 12)
	checks["NO4 - Claymore"] = bit.check(flag, 13)
	checks["NO4 - Meal ticket 1(Succubus)"] = bit.check(flag, 14)
	checks["NO4 - Meal ticket 2(Succubus)"] = bit.check(flag, 15)
	checks["NO4 - Meal ticket 3(Succubus)"] = bit.check(flag, 16)
	checks["NO4 - Meal ticket 4(Succubus)"] = bit.check(flag, 17)
	checks["NO4 - Moonstone"] = bit.check(flag, 18)
	checks["NO4 - Scimitar"] = bit.check(flag, 19)
	checks["NO4 - Resist ice"] = bit.check(flag, 20)
	checks["NO4 - Pot roast"] = bit.check(flag, 21)
	checks["NO4 - Onyx(Holy)"] = bit.check(flag, 22)
	checks["NO4 - Knuckle duster(Holy)"] = bit.check(flag, 23)
	checks["NO4 - Life Vessel(Holy)"] = bit.check(flag, 24)
	checks["NO4 - Elixir(Holy)"] = bit.check(flag, 25)
	checks["NO4 - Toadstool(26)"] = bit.check(flag, 26)
	checks["NO4 - Shiitake(27)"] = bit.check(flag, 27)
	checks["NO4 - Life Vessel(Bellow bridge)"] = bit.check(flag, 28)
	checks["NO4 - Heart Vessel(Bellow bridge)"] = bit.check(flag, 29)
	checks["NO4 - Pentagram"] = bit.check(flag, 30)
	checks["NO4 - Secret boots"] = bit.check(flag, 31)
	checks["NO4 - Shiitake(Waterfall)"] = bit.check(flag2, 0)
	checks["NO4 - Toadstool(Waterfall)"] = bit.check(flag2, 1)
	checks["NO4 - Shiitake(Near entrance passage)"] = bit.check(flag2, 3)
	checks["NO4 - Nunchaku"] = bit.check(flag2, 4)
	if mainmemory.read_u16_le(0x03ca4c) ~= 0 then -- Succubus kill, TODO: Look for gold ring looted flag
		checks["NO4 - Gold Ring"] = true
	else
		checks["NO4 - Gold Ring"] = false
	end
	if mainmemory.read_u16_le(0x03ca3c) ~= 0 then
		bosses["Scylla"] = true
	else
		bosses["Scylla"] = false
	end
	if cur_zone == "NO4" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x315c then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 141)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Holy Symbol"] = true end
		end
		if room == 0x319c then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 92)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Merman Statue"] = true end
		end
	end

	return checks
end

function checkNZ0()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf0b)
	checks["NZ0 - Hide cuirass"] = bit.check(flag, 0)
	checks["NZ0 - Heart Vessel"] = bit.check(flag, 1)
	checks["NZ0 - Cloth cape"] = bit.check(flag, 2)
	checks["NZ0 - Life Vessel"] = bit.check(flag, 3)
	checks["NZ0 - Sunglasses"] = bit.check(flag, 6)
	checks["NZ0 - Resist thunder"] = bit.check(flag, 7)
	checks["NZ0 - Leather shield"] = bit.check(flag, 8)
	checks["NZ0 - Basilard"] = bit.check(flag, 9)
	checks["NZ0 - Potion"] = bit.check(flag, 10)
	if mainmemory.read_u16_le(0x03ca40) ~= 0 then
		-- That doens't trigger Boss Token
		checks["NZ0 - Slogra and Gaibon kill"] = true
		bosses["Slogra and Gaibon"] = true
	else
		checks["NZ0 - Slogra and Gaibon kill"] = false
		bosses["Slogra and Gaibon"] = false
	end
	if cur_zone == "NZ0" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x2770 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 120)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 25
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Skill of Wolf"] = true end
		end
		if room == 0x2730 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 114)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 25
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Bat Card"] = true end
		end
	end

	return checks
end

function checkNZ1()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf0d)
	checks["NZ1 - Magic missile"] = bit.check(flag, 0)
	checks["NZ1 - Pentagram"] = bit.check(flag, 1)
	checks["NZ1 - Star flail"] = bit.check(flag, 3)
	checks["NZ1 - Gold plate"] = bit.check(flag, 4)
	checks["NZ1 - Steel helm"] = bit.check(flag, 5)
	checks["NZ1 - Healing mail"] = bit.check(flag, 6)
	checks["NZ1 - Bekatowa"] = bit.check(flag, 7)
	checks["NZ1 - Shaman shield"] = bit.check(flag, 8)
	checks["NZ1 - Ice mail"] = bit.check(flag, 9)
	checks["NZ1 - Life Vessel(Gear train)"] = bit.check(flag, 10)
	checks["NZ1 - Heart Vessel(Gear train)"] = bit.check(flag, 11)
	checks["NZ1 - Bwaka knife"] = bit.check(mainmemory.readbyte(0x03be8f), 2)
	checks["NZ1 - Pot roast"] = bit.check(mainmemory.readbyte(0x03be8f), 0)
	checks["NZ1 - Shuriken"] = bit.check(mainmemory.readbyte(0x03be8f), 1)
	checks["NZ1 - TNT"] = bit.check(mainmemory.readbyte(0x03be8f), 3)
	if mainmemory.read_u16_le(0x03ca50) ~= 0 then
		bosses["Karasuman"] = true
	else
		bosses["Karasuman"] = false
	end
	if cur_zone == "NZ1" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x23a0 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 198)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 183)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Fire of Bat"] = true end
		end
	end

	return checks
end

function checkTOP()
	local checks = {}
	local flag = mainmemory.read_u32_le(0x03bf08)
	checks["TOP - Turquoise"] = bit.check(flag, 0)
	checks["TOP - Turkey(Behind wall)"] = bit.check(flag, 1)
	checks["TOP - Fire mail(Behind wall)"] = bit.check(flag, 2)
	checks["TOP - Tyrfing"] = bit.check(flag, 3)
	checks["TOP - Sirloin(Above Richter)"] = bit.check(flag, 4)
	checks["TOP - Turkey(Above Richter)"] = bit.check(flag, 5)
	checks["TOP - Pot roast(Above Richter)"] = bit.check(flag, 6)
	checks["TOP - Frankfurter(Above Richter)"] = bit.check(flag, 7)
	checks["TOP - Resist stone(Above Richter)"] = bit.check(flag, 8)
	checks["TOP - Resist dark(Above Richter)"] = bit.check(flag, 9)
	checks["TOP - Resist holy(Above Richter)"] = bit.check(flag, 10)
	checks["TOP - Platinum mail(Above Richter)"] = bit.check(flag, 11)
	checks["TOP - Falchion"] = bit.check(flag, 12)
	checks["TOP - Life Vessel 1(Viewing room)"] = bit.check(flag, 13)
	checks["TOP - Life Vessel 2(Viewing room)"] = bit.check(flag, 14)
	checks["TOP - Heart Vessel 1(Viewing room)"] = bit.check(flag, 15)
	checks["TOP - Heart Vessel 2(Viewing room)"] = bit.check(flag, 16)
	checks["TOP - Heart Vessel(Before Richter)"] = bit.check(flag, 18)
	if cur_zone == "TOP" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x1b8c then
			local xl = math.abs(mainmemory.read_u16_le(0x0973f0) - 424)
			local yl = math.abs(mainmemory.read_u16_le(0x0973f4) - 1815)
			local xm = math.abs(mainmemory.read_u16_le(0x0973f0) - 417)
			local ym = math.abs(mainmemory.read_u16_le(0x0973f4) - 1207)
			local o = 10
			if xl >= 0 and xl <= o and yl >= 0 and yl <= o then checks["Leap Stone"] = true end
			if xm >= 0 and xm <= o and ym >= 0 and ym <= o then checks["Power of Mist"] = true end
		end
		if room == 0x1b94 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 350)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 663)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Ghost Card"] = true end
		end
	end

	return checks
end

function checkRARE()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf3b)
	checks["RARE - Fury plate(Hidden floor)"] = bit.check(flag, 0)
	checks["RARE - Zircon"] = bit.check(flag, 1)
	checks["RARE - Buffalo star"] = bit.check(flag, 2)
	checks["RARE - Gram"] = bit.check(flag, 3)
	checks["RARE - Aquamarine"] = bit.check(flag, 4)
	checks["RARE - Heart Vessel(5)"] = bit.check(flag, 5)
	checks["RARE - Life Vessel"] = bit.check(flag, 6)
	checks["RARE - Heart Vessel(7)"] = bit.check(flag, 7)
	if mainmemory.read_u16_le(0x03ca54) ~= 0 then
		bosses["Fake Trevor/Grant/Sypha"] = true
	else
		bosses["Fake Trevor/Grant/Sypha"] = false
	end

	return checks
end

function checkRCAT()
	local checks = {}
	local flag = mainmemory.read_u32_le(0x03bf2b)
	checks["RCAT - Magic missile"] = bit.check(flag, 0)
	checks["RCAT - Buffalo star"] = bit.check(flag, 1)
	checks["RCAT - Resist thunder"] = bit.check(flag, 2)
	checks["RCAT - Resist fire"] = bit.check(flag, 3)
	checks["RCAT - Karma coin(4)(Spike breaker)"] = bit.check(flag, 4)
	checks["RCAT - Karma coin(5)(Spike breaker)"] = bit.check(flag, 5)
	checks["RCAT - Red bean bun"] = bit.check(flag, 6)
	checks["RCAT - Elixir"] = bit.check(flag, 7)
	checks["RCAT - Library card"] = bit.check(flag, 8)
	checks["RCAT - Life Vessel(9)"] = bit.check(flag, 9)
	checks["RCAT - Heart Vessel(10)"] = bit.check(flag, 10)
	checks["RCAT - Shield potion"] = bit.check(flag, 11)
	checks["RCAT - Attack potion"] = bit.check(flag, 12)
	checks["RCAT - Necklace of j"] = bit.check(flag, 13)
	checks["RCAT - Diamond"] = bit.check(flag, 14)
	checks["RCAT - Heart Vessel(After Galamoth)"] = bit.check(flag, 15)
	checks["RCAT - Life Vessel(After Galamoth)"] = bit.check(flag, 16)
	checks["RCAT - Ruby circlet"] = bit.check(flag, 17)
	if mainmemory.read_u16_le(0x03ca7c) ~= 0 then
		bosses["Galamoth"] = true
	else
		bosses["Galamoth"] = false
	end
	if cur_zone == "RCAT" or cur_zone == "RBO8" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x2429 or room == 0x2490 then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 38)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 173)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Gas Cloud"] = true end
		end
	end

	return checks
end

function checkRCEN()
	local checks = {}
	bosses["Dracula"] = dracula_dead

	return checks
end

function checkRCHI()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf33)
	checks["RCHI - Power of Sire(Demon)"] = bit.check(flag, 0)
	checks["RCHI - Life apple(Demon)"] = bit.check(flag, 1)
	checks["RCHI - Alucard sword"] = bit.check(flag, 2)
	checks["RCHI - Green tea(Demon)"] = bit.check(flag, 3)
	checks["RCHI - Power of Sire"] = bit.check(flag, 4)
	checks["RCHI - Shiitake 1(6)"] = bit.check(flag, 6)
	checks["RCHI - Shiitake 2(7)"] = bit.check(flag, 7)
	if mainmemory.read_u16_le(0x03ca58) ~= 0 then
		bosses["Death"] = true
		checks["Eye of Vlad"] = true
	else
		bosses["Death"] = false
		checks["Eye of Vlad"] = false
	end

	return checks
end

function checkRDAI()
	local checks = {}
	local flag = mainmemory.read_u32_le(0x03bf2f)
	checks["RDAI - Fire boomerang"] = bit.check(flag, 2)
	checks["RDAI - Diamond"] = bit.check(flag, 3)
	checks["RDAI - Zircon"] = bit.check(flag, 4)
	checks["RDAI - Heart Vessel(5)"] = bit.check(flag, 5)
	checks["RDAI - Shuriken"] = bit.check(flag, 6)
	checks["RDAI - TNT"] = bit.check(flag, 7)
	checks["RDAI - Boomerang"] = bit.check(flag, 8)
	checks["RDAI - Javelin"] = bit.check(flag, 9)
	checks["RDAI - Manna prism"] = bit.check(flag, 10)
	checks["RDAI - Smart potion"] = bit.check(flag, 11)
	checks["RDAI - Life Vessel"] = bit.check(flag, 12)
	checks["RDAI - Talwar"] = bit.check(flag, 13)
	checks["RDAI - Bwaka knife"] = bit.check(flag, 14)
	checks["RDAI - Magic missile"] = bit.check(flag, 15)
	checks["RDAI - Twilight cloak"] = bit.check(flag, 16)
	checks["RDAI - Heart Vessel(17)"] = bit.check(flag, 17)
	if mainmemory.read_u16_le(0x03ca64) ~= 0 then
		bosses["Medusa"] = true
		checks["Heart of Vlad"] = true
	else
		bosses["Medusa"] = false
		checks["Heart of Vlad"] = false
	end

	return checks
end

function checkRLIB()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf27)
	checks["RLIB - Turquoise"] = bit.check(flag, 0)
	checks["RLIB - Opal"] = bit.check(flag, 1)
	checks["RLIB - Library card"] = bit.check(flag, 2)
	checks["RLIB - Resist fire"] = bit.check(flag, 3)
	checks["RLIB - Resist ice"] = bit.check(flag, 4)
	checks["RLIB - Resist stone"] = bit.check(flag, 5)
	checks["RLIB - Neutron bomb"] = bit.check(flag, 6)
	checks["RLIB - Badelaire"] = bit.check(flag, 7)
	checks["RLIB - Staurolite"] = bit.check(flag, 8)

	return checks
end

function checkRNO0()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf13)
	checks["RNO0 - Library card"] = bit.check(flag, 0)
	checks["RNO0 - Potion"] = bit.check(flag, 1)
	checks["RNO0 - Antivenom"] = bit.check(flag, 2)
	checks["RNO0 - Life Vessel(Middle clock)"] = bit.check(flag, 3)
	checks["RNO0 - Heart Vessel(Middle clock)"] = bit.check(flag, 4)
	checks["RNO0 - Resist dark(Left clock)"] = bit.check(flag, 5)
	checks["RNO0 - Resist holy(Left clock)"] = bit.check(flag, 6)
	checks["RNO0 - Resist thunder(Left clock)"] = bit.check(flag, 7)
	checks["RNO0 - Resist fire(Left clock)"] = bit.check(flag, 8)
	checks["RNO0 - Meal ticket"] = bit.check(flag, 9)
	checks["RNO0 - Iron ball"] = bit.check(flag, 10)
	checks["RNO0 - Heart Refresh(Inside clock)"] = bit.check(flag, 11)

	if cur_zone == "RNO0" and last_zone ~= "RNO0" then
		last_zone = cur_zone
		last_zoneid = cur_zoneid
		-- goal = mainmemory.read_u8(0x180f98) on index 12
		goal = mainmemory.read_u8(0x180f8b) -- index -1
		checkBosses()
		if bosses_dead >= goal then
			goal_met = true
		end
	end

	return checks
end

function checkRNO1()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf17)
	checks["RNO1 - Heart Vessel"] = bit.check(flag, 0)
	checks["RNO1 - Shotel"] = bit.check(flag, 1)
	checks["RNO1 - Hammer"] = bit.check(flag, 2)
	checks["RNO1 - Life Vessel"] = bit.check(flag, 3)
	checks["RNO1 - Luck potion"] = bit.check(flag, 4)
	checks["RNO1 - Shield potion"] = bit.check(flag, 5)
	checks["RNO1 - High potion"] = bit.check(flag, 6)
	checks["RNO1 - Garnet"] = bit.check(flag, 7)
	checks["RNO1 - Dim Sum set"] = bit.check(mainmemory.readbyte(0x03be04), 0)
	if mainmemory.read_u16_le(0x03ca68) ~= 0 then
		bosses["Creature"] = true
		checks["Tooth of Vlad"] = true
	else
		bosses["Creature"] = false
		checks["Tooth of Vlad"] = false
	end

	return checks
end

function checkRNO2()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf1b)
	checks["RNO2 - Opal"] = bit.check(flag, 0)
	checks["RNO2 - Sword of hador"] = bit.check(flag, 1)
	checks["RNO2 - High potion"] = bit.check(flag, 2)
	checks["RNO2 - Shield potion"] = bit.check(flag, 3)
	checks["RNO2 - Luck potion"] = bit.check(flag, 4)
	checks["RNO2 - Manna prism"] = bit.check(flag, 5)
	checks["RNO2 - Aquamarine"] = bit.check(flag, 6)
	checks["RNO2 - Alucard mail"] = bit.check(flag, 7)
	checks["RNO2 - Life Vessel"] = bit.check(flag, 8)
	checks["RNO2 - Heart Refresh"] = bit.check(flag, 9)
	checks["RNO2 - Shuriken"] = bit.check(flag, 10)
	checks["RNO2 - Heart Vessel"] = bit.check(flag, 11)
	if mainmemory.read_u16_le(0x03ca74) ~= 0 then
		bosses["Akmodan II"] = true
		checks["Rib of Vlad"] = true
	else
		bosses["Akmodan II"] = false
		checks["Rib of Vlad"] = false
	end

	return checks
end

function checkRNO3()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf1f)
	checks["RNO3 - Hammer"] = bit.check(flag, 0)
	checks["RNO3 - Antivenom"] = bit.check(flag, 1)
	checks["RNO3 - High potion"] = bit.check(flag, 2)
	checks["RNO3 - Heart Vessel"] = bit.check(flag, 3)
	checks["RNO3 - Zircon"] = bit.check(flag, 4)
	checks["RNO3 - Opal"] = bit.check(flag, 5)
	checks["RNO3 - Beryl circlet"] = bit.check(flag, 6)
	checks["RNO3 - Fire boomerang"] = bit.check(flag, 7)
	checks["RNO3 - Life Vessel"] = bit.check(flag, 8)
	checks["RNO3 - Talisman"] = bit.check(flag, 9)
	checks["RNO3 - Pot roast"] = bit.check(mainmemory.readbyte(0x03be27), 0)

	return checks
end

function checkRNO4()
	local checks = {}
	local flag = mainmemory.read_u32_le(0x03bf23)
	checks["RNO4 - Alucard shield"] = bit.check(flag, 0)
	checks["RNO4 - Shiitake 1(Near entrance passage)"] = bit.check(flag, 1)
	checks["RNO4 - Toadstool(Waterfall)"] = bit.check(flag, 2)
	checks["RNO4 - Shiitake 2(Waterfall)"] = bit.check(flag, 3)
	checks["RNO4 - Garnet"] = bit.check(flag, 4)
	checks["RNO4 - Bat Pentagram"] = bit.check(flag, 5)
	checks["RNO4 - Life Vessel(Underwater)"] = bit.check(flag, 6)
	checks["RNO4 - Heart Vessel(Air pocket)"] = bit.check(flag, 7)
	checks["RNO4 - Potion(Underwater)"] = bit.check(flag, 8)
	checks["RNO4 - Shiitake 3(Near air pocket)"] = bit.check(flag, 9)
	checks["RNO4 - Shiitake 4(Near air pocket)"] = bit.check(flag, 10)
	checks["RNO4 - Opal"] = bit.check(flag, 11)
	checks["RNO4 - Life Vessel"] = bit.check(flag, 12)
	checks["RNO4 - Diamond"] = bit.check(flag, 13)
	checks["RNO4 - Zircon(Vase)"] = bit.check(flag, 14)
	checks["RNO4 - Heart Vessel(Succubus side)"] = bit.check(flag, 15)
	checks["RNO4 - Meal ticket 1(Succubus side)"] = bit.check(flag, 16)
	checks["RNO4 - Meal ticket 2(Succubus side)"] = bit.check(flag, 17)
	checks["RNO4 - Meal ticket 3(Succubus side)"] = bit.check(flag, 18)
	checks["RNO4 - Meal ticket 4(Succubus side)"] = bit.check(flag, 19)
	checks["RNO4 - Meal ticket 5(Succubus side)"] = bit.check(flag, 20)
	checks["RNO4 - Zircon(Doppleganger)"] = bit.check(flag, 21)
	checks["RNO4 - Pot roast(Doppleganger)"] = bit.check(flag, 22)
	checks["RNO4 - Dark Blade"] = bit.check(flag, 23)
	checks["RNO4 - Manna prism"] = bit.check(flag, 24)
	checks["RNO4 - Elixir"] = bit.check(flag, 25)
	checks["RNO4 - Osafune katana"] = bit.check(flag, 26)
	if mainmemory.read_u16_le(0x03ca70) ~= 0 then
		bosses["Doppleganger40"] = true
	else
		bosses["Doppleganger40"] = false
	end
	if cur_zone == "RNO4" then
		local room = mainmemory.read_u16_le(0x1375bc)
		if room == 0x2c6c then
			local x = math.abs(mainmemory.read_u16_le(0x0973f0) - 110)
			local y = math.abs(mainmemory.read_u16_le(0x0973f4) - 167)
			local o = 10
			if x >= 0 and x <= o and y >= 0 and y <= o then checks["Force of Echo"] = true end
		end
	end

	return checks
end

function checkRNZ0()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf43)
	checks["RNZ0 - Heart Vessel"] = bit.check(flag, 1)
	checks["RNZ0 - Life Vessel"] = bit.check(flag, 2)
	checks["RNZ0 - Goddess shield"] = bit.check(flag, 3)
	checks["RNZ0 - Manna prism"] = bit.check(flag, 4)
	checks["RNZ0 - Katana"] = bit.check(flag, 5)
	checks["RNZ0 - High potion"] = bit.check(flag, 6)
	checks["RNZ0 - Turquoise"] = bit.check(flag, 7)
	checks["RNZ0 - Ring of Arcana"] = bit.check(flag, 8)
	checks["RNZ0 - Resist dark"] = bit.check(flag, 9)
	if mainmemory.read_u16_le(0x03ca48) ~= 0 then
		bosses["Beezelbub"] = true
	else
		bosses["Beezelbub"] = false
	end

	return checks
end

function checkRNZ1()
	local checks = {}
	local flag = mainmemory.read_u16_le(0x03bf47)
	checks["RNZ1 - Magic missile"] = bit.check(flag, 0)
	checks["RNZ1 - Karma coin"] = bit.check(flag, 1)
	checks["RNZ1 - Str. potion"] = bit.check(flag, 2)
	checks["RNZ1 - Luminus"] = bit.check(flag, 3)
	checks["RNZ1 - Smart potion"] = bit.check(flag, 4)
	checks["RNZ1 - Dragon helm"] = bit.check(flag, 5)
	checks["RNZ1 - Diamond(Hidden room)"] = bit.check(flag, 6)
	checks["RNZ1 - Life apple(Hidden room)"] = bit.check(flag, 7)
	checks["RNZ1 - Sunstone(Hidden room)"] = bit.check(flag, 8)
	checks["RNZ1 - Life Vessel"] = bit.check(flag, 9)
	checks["RNZ1 - Heart Vessel"] = bit.check(flag, 10)
	checks["RNZ1 - Moon rod"] = bit.check(flag, 11)
	checks["RNZ1 - Bwaka knife"] = bit.check(mainmemory.readbyte(0x03be97), 2)
	checks["RNZ1 - Turkey"] = bit.check(mainmemory.readbyte(0x03be97), 0)
	checks["RNZ1 - Shuriken"] = bit.check(mainmemory.readbyte(0x03be97), 1)
	checks["RNZ1 - TNT"] = bit.check(mainmemory.readbyte(0x03be97), 3)
	if mainmemory.read_u16_le(0x03ca78) ~= 0 then
		bosses["Darkwing bat"] = true
		checks["Ring of Vlad"] = true
	else
		bosses["Darkwing bat"] = false
		checks["Ring of Vlad"] = false
	end

	return checks
end

function checkRTOP()
	local checks = {}
	local flag = mainmemory.read_u32_le(0x03bf3f)
	checks["RTOP - Sword of dawn"] = bit.check(flag, 0)
	checks["RTOP - Iron ball(Above Richter)"] = bit.check(flag, 1)
	checks["RTOP - Zircon"] = bit.check(flag, 2)
	checks["RTOP - Bastard sword"] = bit.check(flag, 4)
	checks["RTOP - Life Vessel 1"] = bit.check(flag, 5)
	checks["RTOP - Heart Vessel 1"] = bit.check(flag, 6)
	checks["RTOP - Life Vessel 2"] = bit.check(flag, 7)
	checks["RTOP - Heart Vessel 2"] = bit.check(flag, 8)
	checks["RTOP - Life Vessel 3"] = bit.check(flag, 9)
	checks["RTOP - Heart Vessel 4"] = bit.check(flag, 10)
	checks["RTOP - Royal cloak"] = bit.check(flag, 11)
	checks["RTOP - Resist fire(Viewing room)"] = bit.check(flag, 17)
	checks["RTOP - Resist ice(Viewing room)"] = bit.check(flag, 18)
	checks["RTOP - Resist thunder(Viewing room)"] = bit.check(flag, 19)
	checks["RTOP - Resist stone(Viewing room)"] = bit.check(flag, 20)
	checks["RTOP - High potion(Viewing room)"] = bit.check(flag, 21)
	checks["RTOP - Garnet"] = bit.check(flag, 22)
	checks["RTOP - Lightning mail"] = bit.check(flag, 23)
	checks["RTOP - Library card"] = bit.check(flag, 24)

	return checks
end

function checkAllLocations()
	local location_checks = {}

	-- Normal Castle
	for k,v in pairs(checkARE()) do location_checks[k] = v end
	for k,v in pairs(checkCAT()) do location_checks[k] = v end
	for k,v in pairs(checkCHI()) do location_checks[k] = v end
	for k,v in pairs(checkDAI()) do location_checks[k] = v end
	for k,v in pairs(checkLIB()) do location_checks[k] = v end
	for k,v in pairs(checkNO0()) do location_checks[k] = v end
	for k,v in pairs(checkNO1()) do location_checks[k] = v end
	for k,v in pairs(checkNO2()) do location_checks[k] = v end
	for k,v in pairs(checkNO3()) do location_checks[k] = v end
	for k,v in pairs(checkNO4()) do location_checks[k] = v end
	for k,v in pairs(checkNZ0()) do location_checks[k] = v end
	for k,v in pairs(checkNZ1()) do location_checks[k] = v end
	for k,v in pairs(checkTOP()) do location_checks[k] = v end

	-- Reverse Castle
	for k,v in pairs(checkRARE()) do location_checks[k] = v end
	for k,v in pairs(checkRCAT()) do location_checks[k] = v end
	for k,v in pairs(checkRCEN()) do location_checks[k] = v end
	for k,v in pairs(checkRCHI()) do location_checks[k] = v end
	for k,v in pairs(checkRDAI()) do location_checks[k] = v end
	for k,v in pairs(checkRLIB()) do location_checks[k] = v end
	for k,v in pairs(checkRNO0()) do location_checks[k] = v end
	for k,v in pairs(checkRNO1()) do location_checks[k] = v end
	for k,v in pairs(checkRNO2()) do location_checks[k] = v end
	for k,v in pairs(checkRNO3()) do location_checks[k] = v end
	for k,v in pairs(checkRNO4()) do location_checks[k] = v end
	for k,v in pairs(checkRNZ0()) do location_checks[k] = v end
	for k,v in pairs(checkRNZ1()) do location_checks[k] = v end
	for k,v in pairs(checkRTOP()) do location_checks[k] = v end

	return location_checks
end

function checkOneLocation()
	local current_table = {}

	-- Normal Castle
	if cur_zone == "ARE" or cur_zone == "BO2" then current_table = checkARE() end
	if cur_zone == "CAT" or cur_zone == "BO1" then current_table = checkCAT() end
	if cur_zone == "CHI" or cur_zone == "BO7" then current_table = checkCHI() end
	if cur_zone == "DAI" or cur_zone == "BO5" then current_table = checkDAI() end
	if cur_zone == "LIB" then current_table = checkLIB() end
	if cur_zone == "NO0" or cur_zone == "CEN" then current_table = checkNO0() end
	if cur_zone == "NO1" or cur_zone == "BO4" then current_table = checkNO1() end
	if cur_zone == "NO2" or cur_zone == "BO0" then current_table = checkNO2() end
	if cur_zone == "NO3" then current_table = checkNO3() end
	if cur_zone == "NP3" then current_table = checkNO3() end
	if cur_zone == "NO4" or cur_zone == "BO3" then current_table = checkNO4() end
	if cur_zone == "BO3" then current_table = checkNO4() end
	if cur_zone == "NZ0" then current_table = checkNZ0() end
	if cur_zone == "NZ1" then current_table = checkNZ1() end
	if cur_zone == "TOP" then current_table = checkTOP() end

	-- Reverse Castle
	if cur_zone == "RARE" or cur_zone == "RBO0" then current_table = checkRARE() end
	if cur_zone == "RCAT" or cur_zone == "RBO8" then current_table = checkRCAT() end
	if cur_zone == "RCEN" or cur_zone == "RBO6" then current_table = checkRCEN() end
	if cur_zone == "RCHI" or cur_zone == "RBO2" then current_table = checkRCHI() end
	if cur_zone == "RDAI" or cur_zone == "RBO3" then current_table = checkRDAI() end
	if cur_zone == "RLIB" then current_table = checkRLIB() end
	if cur_zone == "RNO0" then current_table = checkRNO0() end
	if cur_zone == "RNO1" or cur_zone == "RBO4" then current_table = checkRNO1() end
	if cur_zone == "RNO2" or cur_zone == "RBO7" then current_table = checkRNO2() end
	if cur_zone == "RNO3" then current_table = checkRNO3() end
	if cur_zone == "RNO4" or cur_zone == "RBO5" then current_table = checkRNO4() end
	if cur_zone == "RNZ0" or cur_zone == "RBO1" then current_table = checkRNZ0() end
	if cur_zone == "RNZ1" then current_table = checkRNZ1() end
	if cur_zone == "RTOP" then current_table = checkRTOP() end

	-- Check if the main table needs update
	if next(current_table) ~= nil then
		for k, v in pairs(current_table) do
			if all_location_table[k] ~= current_table[k] then
				all_location_table[k] = v
			end
		end
	end
end

function checkBosses()
	bosses_dead = 0
	if mainmemory.read_u16_le(0x03ca78) ~= 0 then
		bosses["Darkwing bat"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Darkwing bat"] = false
	end
	if mainmemory.read_u16_le(0x03ca48) ~= 0 then
		bosses["Beezelbub"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Beezelbub"] = false
	end
	if mainmemory.read_u16_le(0x03ca70) ~= 0 then
		bosses["Doppleganger40"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Doppleganger40"] = false
	end
	if mainmemory.read_u16_le(0x03ca74) ~= 0 then
		bosses["Akmodan II"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Akmodan II"] = false
	end
	if mainmemory.read_u16_le(0x03ca68) ~= 0 then
		bosses["Creature"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Creature"] = false
	end
	if mainmemory.read_u16_le(0x03ca64) ~= 0 then
		bosses["Medusa"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Medusa"] = false
	end
	if mainmemory.read_u16_le(0x03ca58) ~= 0 then
		bosses["Death"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Death"] = false
	end
	if mainmemory.read_u16_le(0x03ca7c) ~= 0 then
		bosses["Galamoth"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Galamoth"] = false
	end
	if mainmemory.read_u16_le(0x03ca54) ~= 0 then
		bosses["Fake Trevor/Grant/Sypha"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Fake Trevor/Grant/Sypha"] = false
	end
	if mainmemory.read_u16_le(0x03ca50) ~= 0 then
		bosses["Karasuman"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Karasuman"] = false
	end
	if mainmemory.read_u16_le(0x03ca40) ~= 0 then
		bosses["Slogra and Gaibon"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Slogra and Gaibon"] = false
	end
	if mainmemory.read_u16_le(0x03ca3c) ~= 0 then
		bosses["Scylla"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Scylla"] = false
	end
	if mainmemory.read_u16_le(0x03ca2c) ~= 0 then
		bosses["Olrox"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Olrox"] = false
	end
	if mainmemory.read_u16_le(0x03ca30) ~= 0 then
		bosses["Doppleganger 10"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Doppleganger 10"] = false
	end
	if mainmemory.read_u16_le(0x03ca6c) ~= 0 then
		bosses["Lesser Demon"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Lesser Demon"] = false
	end
	if mainmemory.read_u16_le(0x03ca44) ~= 0 then
		bosses["Hippogryph"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Hippogryph"] = false
	end
	if mainmemory.read_u16_le(0x03ca5c) ~= 0 then
		bosses["Cerberos"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Cerberos"] = false
	end
	if mainmemory.read_u16_le(0x03ca34) ~= 0 then
		bosses["Legion"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Legion"] = false
	end
	if mainmemory.read_u16_le(0x03ca38) ~= 0 then
		bosses["Minotaurus/Werewolf"] = true
		bosses_dead = bosses_dead + 1
	else
		bosses["Minotaurus/Werewolf"] = false
	end
end

function process_items(f)
	local table_size = table.getn(ItemsReceived)
	if start_item_drawing == 0 and table_size >= last_item_processed then
		start_item_drawing = f
		item1 = grant_item_byid(ItemsReceived[last_item_processed])
		num_item_processed = 1
		if last_item_processed + 1 <= table_size then
			item2 = grant_item_byid(ItemsReceived[last_item_processed + 1])
			num_item_processed = num_item_processed + 1
		end
		if last_item_processed + 2 <= table_size then
			item3 = grant_item_byid(ItemsReceived[last_item_processed + 2])
			num_item_processed = num_item_processed + 1
		end
		if last_item_processed + 3 <= table_size then
			item4 = grant_item_byid(ItemsReceived[last_item_processed + 3])
			num_item_processed = num_item_processed + 1
		end
	end
	if start_item_drawing ~= 0 then
		if f - start_item_drawing < 900 then
			gui.drawText(0, 0, item1, "red")
			if item2 ~= "" then gui.drawText(0, 10, item2, "blue") end
			if item3 ~= "" then gui.drawText(0, 20, item3, "red") end
			if item4 ~= "" then gui.drawText(0, 30, item4, "blue") end
		else
			gui.clearGraphics()
			start_item_drawing = 0
			item1 = ""
			item2 = ""
			item3 = ""
			item4 = ""
			last_item_processed = last_item_processed + num_item_processed
			num_item_processed = 0

			write_last_processed(last_item_processed)
		end
	end
end

function read_last_processed()
	local first = mainmemory.read_u8(0x03bef3) -- 4 bits
	local second = mainmemory.read_u8(0x03bf0c) -- 3 bits
	local third = mainmemory.read_u8(0x03befe) -- 3 bits
	local sum = 0
	if bit.check(third, 5) then sum = 1 end
	if bit.check(third, 6) then sum = sum + 2 end
	if bit.check(third, 7) then sum = sum + 4 end
	if bit.check(second, 5) then sum = sum + 8 end
	if bit.check(second, 6) then sum = sum + 16 end
	if bit.check(second, 7) then sum = sum + 32 end
	if bit.check(first, 4) then sum = sum + 64 end
	if bit.check(first, 5) then sum = sum + 128 end
	if bit.check(first, 6) then sum = sum + 256 end
	if bit.check(first, 7) then sum = sum + 512 end

	return sum
end

function write_last_processed(l_processed)
	local bits = {}
	local num = l_processed
	local first = mainmemory.read_u8(0x03bef3) -- 4 bits
	local second = mainmemory.read_u8(0x03bf0c) -- 3 bits
	local third = mainmemory.read_u8(0x03befe) -- 3 bits
	local t_f = 0
	local t_s = 0
	local t_t = 0

	if l_processed > 1023 then
		console.log("Number to big to write on 10 bits!")
		return
	end

	while num > 0 do
		rest = math.fmod(num, 2)
		bits[#bits+1] = rest
		num = (num - rest) / 2
	end

	if bit.check(third, 0) then t_t = t_t + 1 end
	if bit.check(third, 1) then t_t = t_t + 2 end
	if bit.check(third, 2) then t_t = t_t + 4 end
	if bit.check(third, 3)  then t_t = t_t + 8 end
	if bit.check(third, 4) then t_t = t_t + 16 end

	if bit.check(second, 0) then t_s = t_s + 1 end
	if bit.check(second, 1) then t_s = t_s + 2 end
	if bit.check(second, 2) then t_s = t_s + 4 end
	if bit.check(second, 3)  then t_s = t_s + 8 end
	if bit.check(second, 4) then t_s = t_s + 16 end

	if bit.check(first, 0) then t_f = t_f + 1 end
	if bit.check(first, 1) then t_f = t_f + 2 end
	if bit.check(first, 2) then t_f = t_f + 4 end
	if bit.check(first, 4) then t_f = t_f + 8 end

	if bits[1] == 1 then t_t = t_t + 32	end
	if bits[2] == 1 then t_t = t_t + 64 end
	if bits[3] == 1 then t_t = t_t + 128 end
	if bits[4] == 1 then t_s = t_s + 32 end
	if bits[5] == 1 then t_s = t_s + 64 end
	if bits[6] == 1 then t_s = t_s + 128 end
	if bits[7] == 1 then t_f = t_f + 16 end
	if bits[8] == 1 then t_f = t_f + 32 end
	if bits[9] == 1 then t_f = t_f + 64 end
	if bits[10] == 1 then t_f = t_f + 128 end

	mainmemory.write_u8(0x03bef3, t_f)
	mainmemory.write_u8(0x03bf0c, t_s)
	mainmemory.write_u8(0x03befe, t_t)
end

function file_exists()
	if seed == "" or player_name == "" then return end
	local filename = seed .. "_" .. player_name .. ".txt"
	local f = io.open(filename, "r")
	if f ~= nil then
		for line in io.lines(filename) do
			table.insert(misplaced_read, line)
		end
		io.close(f)
		last_misplaced_save = table.getn(misplaced_read)
		console.log("Save file found on file_exists!")
		return true
	else
		return false
	end
end

function handle_misplaced(f)
	if seed == "" or player_name == "" then return end
	local filename = seed .. "_" .. player_name .. ".txt"
	local added = 0

	if next(misplaced_read) == nil then
		local file, err = io.open(filename, "w")
		for k, v in ipairs(misplaced_items) do
			file:write(v, "\n")
			-- First misplaced. Add to the list to prevent entering the loop endless
			table.insert(misplaced_read, v)
		end
		last_misplaced_save = table.getn(misplaced_items)
		file:close()
	else
		-- There are a save file
		local size = table.getn(misplaced_items)
		local size_r = table.getn(misplaced_read)

		if size > size_r then
			-- We have more items than saved on file. Update
			local file, err = io.open(filename, "a")

			for i = last_misplaced_save + 1, size, 1 do
				file:write(misplaced_items[i], "\n")
				added = added + 1
			end
			last_misplaced_save = last_misplaced_save + added
			file:close()
		end
	end

	process_misplaced(f)
end

function process_misplaced(f)
	-- Misplaced items doesn't persist thru connections on the server so we handle it separately and for now we assume the player didn't die or loadstate
	-- I have no ideia how to handle those. So far we gonna give whaever is on the save file everytime this function is called
	-- Graphics might be clear before timer
	local table_size = table.getn(misplaced_items)
	local table_size_r = table.getn(misplaced_read)

	if table_size == 0 and table_size_r > 0 then
		-- We have misplaced_read but no misplaced_items Due fresh connect? Add to the table
		for k, v in ipairs(misplaced_read) do
			table.insert(misplaced_items, v)
		end
		-- Try to find a relic received on misplaced table
		local ret_pos = check_for_misplaced_relic()
		if ret_pos ~= 0 then last_misplaced_processed = ret_pos + 1 end
	end

	if misplaced_drawing == 0 and table_size >= last_misplaced_processed then
		misplaced_drawing = f
		m_item1 = grant_item_byid(misplaced_items[tonumber(last_misplaced_processed)])
		num_misplaced_processed = 1
		if last_misplaced_processed + 1 <= table_size then
			m_item2 = grant_item_byid(misplaced_items[tonumber(last_misplaced_processed) + 1])
			num_misplaced_processed = num_misplaced_processed +1
		end
		if last_misplaced_processed + 2 <= table_size then
			m_item3 = grant_item_byid(misplaced_items[tonumber(last_misplaced_processed) + 2])
			num_misplaced_processed = num_misplaced_processed +1
		end
		if last_misplaced_processed + 3 <= table_size then
			m_item4 = grant_item_byid(misplaced_items[tonumber(last_misplaced_processed) + 3])
			num_misplaced_processed = num_misplaced_processed +1
		end
	end
	if misplaced_drawing ~= 0 then
		if f - misplaced_drawing < 900 then
			gui.drawText(0, 40, m_item1, "red")
			if m_item2 ~= "" then gui.drawText(0, 50, m_item2, "red") end
			if m_item3 ~= "" then gui.drawText(0, 60, m_item3, "red") end
			if m_item4 ~= "" then gui.drawText(0, 70, m_item4, "red") end
		else
			gui.clearGraphics()
			misplaced_drawing = 0
			m_item1 = ""
			m_item2 = ""
			m_item3 = ""
			m_item4 = ""
			last_misplaced_processed = last_misplaced_processed + num_misplaced_processed
			num_misplaced_processed = 0
		end
	end
end

function check_for_misplaced_relic()
	for i = #misplaced_items, 1, -1 do
		local item = tonumber(misplaced_items[i])
		-- It's better to keep sword card out
		if item >= 300 and item <= 329 and item ~= 322 then
			if has_relic(item) then
				console.log("Found misplaced relic")
				return i
			end
		end
	end
	return 0
end

function has_relic(relic_id)
	local relic_name
	local relic_address

	relic_name, relic_address = find_item(relic_id)
	if mainmemory.read_u8(relic_address) > 0 then return true
	else return false end
end

function find_item(item_id)
	local size = table.getn(allItems)
	for i = 1, size, 3 do
		if allItems[i] == item_id then
			return allItems[i+1], allItems[i+2]
		end
	end
	console.log("Something went wrong!")
	return 0
end

function main()
    if not checkBizHawkVersion() then
        return
    end
    local port = 17242
    print("Using port: "..tostring(port))
    server, error = socket.bind('localhost', port)
    if( error ~= nil ) then
        print(error)
    end

	event.onloadstate(on_loadstate)

    while true do
        frame = frame + 1
        if not (curstate == prevstate) then
            print("Current state: "..curstate)
            prevstate = curstate
        end
		if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 5 == 0) then
				receive()
				getCurrZone()

				-- printing for testing reasons
				--gui.drawText(200, 0, mainmemory.read_u16_le(0x0973f0))
				--gui.drawText(200, 10, mainmemory.read_u16_le(0x0973f4))
				--gui.drawText(200, 20, mainmemory.read_u16_le(0x1375bc))
				--last_processed_read = read_last_processed()
				--gui.drawText(200, 30, bosses_dead)
				--gui.drawText(300, 0, last_status)
				--gui.drawText(300, 10, last_item_processed .. " - " .. last_processed_read)


				if first_connect then
					console.log("Just connect!")
					first_connect = false
					last_status = 1
				end

				if last_status == 1 then
					if cur_zone ~= "UNKNOWN" then last_status = 2 end
				end
				if last_status == 2 then
					-- We are connected. At Richter?
					if cur_zone == "ST0" then last_status = 4 end
					-- At Alucard?
					if cur_zone ~= "ST0" and cur_zone ~= "UNKNOWN" then
						-- We just connected and already on Alucard. Loaded game?.
						last_status = 10
						checkAllLocations()
						checkBosses()
						misplaced_items = {}
						misplaced_read = {}
						last_misplaced_save = 0
						last_misplaced_processed = 0
						file_exists()
						-- Do we have a last location flag on memory?
						last_processed_read = read_last_processed()
						if last_processed_read == 0 and last_processed_read < 1024 then last_item_processed = 1
						else last_item_processed = last_processed_read end
					end
				end
				if last_status == 4 then
					-- We are at Richter. Game takes a bit to actually start, after defeating Dracula
					if cur_zone ~= "ST0" then last_status = 8 end
				end
				if last_status == 8 then
					-- Just changed to NO3
					if delay_timer == 0 then delay_timer = frame end
					-- Assume 60fps, give 15 seconds to load and Alucard enter the castle
					if frame - delay_timer >= 900 then
						last_status = 10
						checkBosses()
						misplaced_items = {}
						misplaced_read = {}
						last_misplaced_save = 0
						last_misplaced_processed = 0
						-- fresh game. No item granted yet
						last_item_processed = 1
						file_exists()
						delay_timer = 0
					end
				end

				if last_status == 10 then

					if got_data and seed ~= "" and player_name ~= "" then
						console.log("Got seed and player name")
						if got_data then
							if file_exists() then
								-- We just started and have misplaced_items give it to player
								process_misplaced(frame)
							end
							got_data = false
						end
					end

					if cur_zone == "RBO6" then
						checkVictory(frame)
					end

					if mainmemory.readbyte(0x09794c) == 2 then
						if next(ItemsReceived) ~= nil then
							process_items(frame)
						end
						if next(misplaced_items) ~= nil then
							handle_misplaced(frame)
						end
						if next(ItemsReceivedQueue) ~= nil and start_item_drawing == 0 and misplaced_drawing == 0 then
							for k, v in ipairs(ItemsReceivedQueue) do
								table.insert(ItemsReceived, v)
								table.remove(ItemsReceivedQueue, k)
							end
						end
						if next(misplaced_items_queue) ~= nil and start_item_drawing == 0 and misplaced_drawing == 0 then
							for k, v in ipairs(misplaced_items_queue) do
								table.insert(misplaced_items, v)
								table.remove(misplaced_items_queue, k)
							end
						end
					end

					if just_died then
						console.log("We just died. TODO: Deal with items we need to receive again")
						just_died = false
					end

					if goal_met and cur_zone == "RNO0" then
						if delay_timer == 0 then delay_timer = frame end
						if delay_timer ~=0 and frame - delay_timer >= 900 then
							-- Give some time to zone load before patching
							memory.write_s32_le(0x801c132c, 0x14400118, "System Bus")
						end
					end

					check_death()
					checkOneLocation()
				end
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            if  (frame % 60 == 0) then

                print("Waiting for client.")

                emu.frameadvance()
                server:settimeout(2)
                print("Attempting to connect")
				last_status = 0
                local client, timeout = server:accept()
                if timeout == nil then
                    print("Initial connection made")
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    sotnSocket = client
                    sotnSocket:settimeout(0)
					last_status = 1
                end
            end
        end
        emu.frameadvance()
    end
end

main()



