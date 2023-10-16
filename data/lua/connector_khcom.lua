console.clear()

local socket = require("socket")
local json = require('json')
require("common")

function hex2bin(str)
    local map = {
        ['0'] = '0000',
        ['1'] = '0001',
        ['2'] = '0010',
        ['3'] = '0011',
        ['4'] = '0100',
        ['5'] = '0101',
        ['6'] = '0110',
        ['7'] = '0111',
        ['8'] = '1000',
        ['9'] = '1001',
        ['A'] = '1010',
        ['B'] = '1011',
        ['C'] = '1100',
        ['D'] = '1101',
        ['E'] = '1110',
        ['F'] = '1111'
    }
    return str:gsub('[0-9A-F]', map)
end

function bin2hex(str)
    local map = {
        ['0000'] = '0',
        ['0001'] = '1',
        ['0010'] = '2',
        ['0011'] = '3',
        ['0100'] = '4',
        ['0101'] = '5',
        ['0110'] = '6',
        ['0111'] = '7',
        ['1000'] = '8',
        ['1001'] = '9',
        ['1010'] = 'A',
        ['1011'] = 'B',
        ['1100'] = 'C',
        ['1101'] = 'D',
        ['1110'] = 'E',
        ['1111'] = 'F',
        [' '] = ' '
    }
    local mystr = ""
    local i = 0
    while i < string.len(str) do
        local e = 0
        local temptemp = ""
        while e < 4 do
            i = i + 1
            local c = str:sub(i,i)
            if c ~= " " then
                temptemp = temptemp..c
                e = e + 1
            else
                mystr = mystr.." "
            end
        end
        mystr = mystr..map[temptemp]
    end
    return mystr
end

function strhex2array(str)
    local myarr = {}
    local i = 0
    local e = 1
    local temptemp = ""
    while i < string.len(str) do
        i = i + 1
        local c = str:sub(i,i)
        if c ~= " " then
            temptemp = temptemp..c
        else
            myarr[e] = tonumber(temptemp, 16)
            e = e + 1
            temptemp = ""
        end
    end
    myarr[e] = tonumber(temptemp, 16)
    e = e + 1
    temptemp = ""
    return myarr
end

function replace_str_ind(str, ind, char)
    return str:sub(1,ind-1)..char..str:sub(ind+1)
end

--Define min and max values for all battle cards
battle_cards = {}
battle_cards["Kingdom Key"] = {0x000, 0x009}
battle_cards["Three Wishes"] = {0x00A, 0x013}
battle_cards["Crabclaw"] = {0x014, 0x01D}
battle_cards["Pumpkinhead"] = {0x01E, 0x027}
battle_cards["Fairy Harp"] = {0x028, 0x031}
battle_cards["Wishing Star"] = {0x032, 0x03B}
battle_cards["Spellbinder"] = {0x03C, 0x045}
battle_cards["Metal Chocobo"] = {0x046, 0x04F}
battle_cards["Olympia"] = {0x050, 0x059}
battle_cards["Lionheart"] = {0x05A, 0x063}
battle_cards["Lady Luck"] = {0x064, 0x06D}
battle_cards["Divine Rose"] = {0x06E, 0x077}
battle_cards["Oathkeeper"] = {0x078, 0x081}
battle_cards["Oblivion"] = {0x082, 0x08B}
battle_cards["Diamond Dust"] = {0x08C, 0x095}
battle_cards["One Winged Angel"] = {0x096, 0x09F}
battle_cards["Ultima Weapon"] = {0x0A0, 0x0A9}
battle_cards["Fire"] = {0x0AA, 0x0B3}
battle_cards["Blizzard"] = {0x0B4, 0x0BD}
battle_cards["Thunder"] = {0x0BE, 0x0C7}
battle_cards["Cure"] = {0x0C8, 0x0D1}
battle_cards["Gravity"] = {0x0D2, 0x0DB}
battle_cards["Stop"] = {0x0DC, 0x0E5}
battle_cards["Aero"] = {0x0E6, 0x0EF}
battle_cards["Simba"] = {0x104, 0x10D}
battle_cards["Genie"] = {0x10E, 0x117}
battle_cards["Bambi"] = {0x118, 0x121}
battle_cards["Dumbo"] = {0x122, 0x12B}
battle_cards["Tinker Bell"] = {0x12C, 0x135}
battle_cards["Mushu"] = {0x136, 0x13F}
battle_cards["Cloud"] = {0x140, 0x149}
battle_cards["Potion"] = {0x17C, 0x185}
battle_cards["Hi-Potion"] = {0x186, 0x18F}
battle_cards["Mega-Potion"] = {0x190, 0x199}
battle_cards["Ether"] = {0x19A, 0x1A3}
battle_cards["Mega-Ether"] = {0x1A4, 0x1AD}
battle_cards["Elixir"] = {0x1AE, 0x1B7}
battle_cards["Megalixir"] = {0x1B8, 0x1C1}
battle_cards["Guard Armor"] = {0x21D, 0x21D}
battle_cards["Parasite Cage"] = {0x21E, 0x21E}
battle_cards["Trickmaster"] = {0x21F, 0x21F}
battle_cards["Darkside"] = {0x220, 0x220}
battle_cards["Hades"] = {0x227, 0x227}
battle_cards["Jafar"] = {0x228, 0x228}
battle_cards["Oogie Boogie"] = {0x229, 0x229}
battle_cards["Ursula"] = {0x22A, 0x22A}
battle_cards["Hook"] = {0x22B, 0x22B}
battle_cards["Dragon Malificent"] = {0x22C, 0x22C}
battle_cards["Shadow"] = {0x1C2, 0x1C4}
battle_cards["Soldier"] = {0x1C5, 0x1C7}
battle_cards["Large Body"] = {0x1C8, 0x1CA}
battle_cards["Red Nocturne"] = {0x1CB, 0x1CD}
battle_cards["Blue Rhapsody"] = {0x1CE, 0x1D0}
battle_cards["Yellow Opera"] = {0x1D1, 0x1D3}
battle_cards["Green Requiem"] = {0x1D4, 0x1D6}
battle_cards["Powerwild"] = {0x1D7, 0x1D9}
battle_cards["Bouncywild"] = {0x1DA, 0x1DC}
battle_cards["Air Soldier"] = {0x1DD, 0x1DF}
battle_cards["Bandit"] = {0x1E0, 0x1E2}
battle_cards["Fat Bandit"] = {0x1E3, 0x1E5}
battle_cards["Barrel Spider"] = {0x1E6, 0x1E8}
battle_cards["Search Ghost"] = {0x1E9, 0x1EB}
battle_cards["Sea Neon"] = {0x1EC, 0x1EE}
battle_cards["Screwdriver"] = {0x1EF, 0x1F1}
battle_cards["Aquatank"] = {0x1F2, 0x1F4}
battle_cards["Wight Knight"] = {0x1F5, 0x1F7}
battle_cards["Gargoyle"] = {0x1F8, 0x1FA}
battle_cards["Pirate"] = {0x1FB, 0x1FD}
battle_cards["Air Pirate"] = {0x1FE, 0x200}
battle_cards["Darkball"] = {0x201, 0x203}
battle_cards["Defender"] = {0x204, 0x206}
battle_cards["Wyvern"] = {0x207, 0x209}
battle_cards["Wizard"] = {0x20A, 0x20C}
battle_cards["Neoshadow"] = {0x20D, 0x20F}
battle_cards["White Mushroom"] = {0x210, 0x210}
battle_cards["Black Fungus"] = {0x211, 0x213}
battle_cards["Creeper Plant"] = {0x214, 0x216}
battle_cards["Tornado Step"] = {0x217, 0x219}
battle_cards["Crescendo"] = {0x21A, 0x21C}
battle_cards["Card Soldier (Red)"] = {0x221, 0x223}
battle_cards["Card Soldier (Black)"] = {0x224, 0x226}
battle_cards["Riku"] = {0x22D, 0x22D}
battle_cards["Axel"] = {0x22E, 0x22E}
battle_cards["Larxene"] = {0x22F, 0x22F}
battle_cards["Vexen"] = {0x230, 0x230}
battle_cards["Marluxia"] = {0x231, 0x231}
battle_cards["Lexaeus"] = {0x233, 0x233}
battle_cards["Ansem"] = {0x234, 0x234}

win_conditions = {}
win_conditions["Donald"] = {0x0F1, 0x0F1}
win_conditions["Goofy"] = {0x0FB, 0x0FB}
win_conditions["Aladdin"] = {0x14B, 0x14B}
win_conditions["Ariel"] = {0x155, 0x155}
win_conditions["Jack"] = {0x15F, 0x15F}
win_conditions["Peter Pan"] = {0x169, 0x169}
win_conditions["Beast"] = {0x173, 0x173}

--Addresses
gold_map_cards_addresses = {}
gold_map_cards_addresses["Key of Beginnings"] = 0x0203A99C
gold_map_cards_addresses["Key of Guidance"] = 0x0203A9A6
gold_map_cards_addresses["Key to Truth"] = 0x0203A9B0
gold_map_cards_addresses["Key to Rewards"] = 0x0203A9BA
floor_number_address = 0x02039BBE
battle_cards_address = 0x0203A080
time_played_address = 0x02039D8C
highest_warp_floor_address = 0x0203C590
deck_card_pointers_addresses = {0x02039DE0, 0x02039EC0, 0x02039FA0}
world_card_addresses = {0x0203C590, 0x02039D31}
world_card_values = {{0x00,0x02}, {0x08,0x00}, {0x04,0x00}, {0x10,0x00}, {0x01,0x00}, {0x20,0x00}
       ,{0x02,0x00}, {0x40,0x00}, {0x80,0x00}, {0x00,0x04}, {0x00,0x08}, {0x00,0x01}, {0x00,0x10}}

bronze_pack_attack_cards = {"Kingdom Key", "Three Wishes", "Pumpkinhead", "Olympia", "Wishing Star", "Lady Luck"}
bronze_pack_magic_cards = {"Fire", "Blizzard", "Thunder", "Simba", "Genie", "Cloud", "Dumbo"}
bronze_pack_item_cards = {"Potion", "Hi-Potion", "Ether"}
bronze_pack_enemy_cards = {"Shadow", "Soldier", "Large Body", "Card Soldier (Red)", "Card Soldier (Black)", "Red Nocturne", "Blue Rhapsody", "Yellow Opera", "Green Requiem"
                            ,"Powerwild", "Bouncywild", "Air Soldier", "Bandit", "Fat Bandit", "Barrel Spider", "Search Ghost", "Sea Neon"
                            ,"Screwdriver", "Aquatank", "Wight Knight", "Gargoyle", "Pirate", "Air Pirate", "Darkball", "Defender", "Wyvern"
                            ,"Wizard"}

silver_pack_attack_cards = {"Lionheart", "Metal Chocobo", "Spellbinder", "Divine Rose", "Crabclaw"}
silver_pack_magic_cards = {"Stop", "Gravity", "Aero", "Bambi", "Mushu", "Tinker Bell"}
silver_pack_item_cards = {"Mega-Potion", "Elixir", "Mega-Ether"}
silver_pack_enemy_cards = {"Guard Armor", "Trickmaster", "Hades", "Parasite Cage", "Jafar", "Oogie Boogie", "Ursula", "Hook", "Dragon Malificent"}

gold_pack_attack_cards = {"Oathkeeper", "Oblivion", "Diamond Dust", "One-Winged Angel", "Ultima Weapon"}
gold_item_cards = {"Megalixir"}
gold_enemy_cards = {"Riku", "Axel", "Larxene", "Vexen", "Marluxia", "Lexaeus", "Ansem"}

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local zeldaSocket = nil

function save_or_savestate_loaded(past_playtime, current_playtime)
    if current_playtime >= past_playtime then
        if (current_playtime - past_playtime) < 3 then
            return false
        end
    end
    return true
end

function get_floor_number()
    local floor_number = memory.readbyte(floor_number_address) + 1
    return floor_number
end

function get_current_gold_card_qty(gold_card_type)
    local num_of_gold_cards = memory.readbyte(gold_map_cards_addresses[gold_card_type] + 0x01)
    return num_of_gold_cards
end

function get_battle_card(offset)
    local battle_card = memory.read_u16_le(0x0203A080 + (2 * offset))
    return battle_card
end

function get_battle_cards()
    i = 0
    j = 1
    local battle_cards = {}
    while i < 915 do
        local battle_card = get_battle_card(i)
        if battle_card ~= 0x0FFF then
            battle_cards[j] = battle_card
        end
        j = j + 1
        i = i + 1
    end
    return battle_cards
end

function get_battle_card_type(battle_card_value)
    battle_card_value = battle_card_value % 0x8000
    for k,v in pairs(battle_cards) do
        if battle_card_value >= v[1] and battle_card_value <= v[2] then
            return k
        end
    end
    return "Not Found"
end

function get_playtime()
    local playtime = memory.read_u24_le(time_played_address)
    return playtime
end

function get_stored_gold_cards(key_type, floor_number)
    local num_of_gold_cards = memory.readbyte(gold_map_cards_addresses[key_type] + (floor_number - 1))
    if floor_number >= 10 then
        if num_of_gold_cards == 2 or num_of_gold_cards == 3 then
            num_of_gold_cards = 1
        else
            num_of_gold_cards = 0
        end
    elseif floor_number <= 4 then
        if num_of_gold_cards == 1 or num_of_gold_cards == 3 then
            num_of_gold_cards = 1
        else
            num_of_gold_cards = 0
        end
    end
    return num_of_gold_cards
end

function get_highest_warp_floor()
    local highest_warp_floor = memory.readbyte(highest_warp_floor_address) / 2 + 1
    return highest_warp_floor
end

function get_deck_pointer(deck_number, offset)
    local deck_pointer = memory.read_u16_le(deck_card_pointers_addresses[deck_number] + 2*offset)
end

function get_deck_pointers()
	local deck_pointers = {}
	i = 1
	while (i <= 3) do
		deck_pointers[i] = {}
		j = 1
		k = 1
		finished = false
		while not finished and k < 100 do
			local deck_pointer = get_deck_pointer(i, j-1)
			if deck_pointer == 0xFFFF then
				finished = true
			else
				deck_pointers[i][j] = deck_pointer
				j = j+1
			end
			k = k + 1
		end
		i = i+1
	end
	return deck_pointers
end

function set_deck_pointer(deck_number, offset, value)
    memory.write_u16_le(deck_card_pointers_addresses[deck_number] + 2*offset, value)
end

function set_starting_deck()
    memory.write_u16_le(battle_cards_address, 0x0008) --Kingdom Key 8
    memory.write_u16_le(battle_cards_address, 0x0007) --Kingdom Key 7
    memory.write_u16_le(battle_cards_address, 0x0006) --Kingdom Key 6
    memory.write_u16_le(battle_cards_address, 0x0005) --Kingdom Key 5
    memory.write_u16_le(battle_cards_address, 0x00B9) --Blizzard 5
    memory.write_u16_le(battle_cards_address, 0x0181) --Potion 5
    local i = 7
    while i <= 15 do
        memory.write_u16_le(battle_cards_address + 2*(i-1), 0x0FFF)
        set_deck_pointer(1, i-1, 0xFFFF)
        i = i + 1
    end
end

function update_current_gold_card_qty(current_floor)
    memory.writebyte(gold_map_cards_addresses["Key of Beginnings"] + 0x1, get_stored_gold_cards("Key of Beginnings", current_floor))
    if get_stored_gold_cards("Key of Beginnings", current_floor) < 1 then
        memory.writebyte(gold_map_cards_addresses["Key of Guidance"] + 0x1, 0x0)
    else
        memory.writebyte(gold_map_cards_addresses["Key of Guidance"] + 0x1, get_stored_gold_cards("Key of Guidance", current_floor))
    end
    if get_stored_gold_cards("Key of Beginnings", current_floor) < 1 or get_stored_gold_cards("Key of Guidance", current_floor) < 1 then
        memory.writebyte(gold_map_cards_addresses["Key to Truth"] + 0x1, 0x0)
    else
        memory.writebyte(gold_map_cards_addresses["Key to Truth"] + 0x1, get_stored_gold_cards("Key to Truth", current_floor))
    end
    memory.writebyte(gold_map_cards_addresses["Key to Rewards"] + 0x1, get_stored_gold_cards("Key to Rewards", current_floor))
end

function update_world_cards(current_floor)
    if get_stored_gold_cards("Key of Beginnings", current_floor) > 0 then
        writebyte(world_card_addresses[1], world_card_values[floor_num][1])
        writebyte(world_card_addresses[2], world_card_values[floor_num][2])
    end
end

function update_highest_warp_floor(past_highest_warp_floor, current_highest_warp_floor)
    if current_highest_warp_floor < 13 then
        memory.writebyte(highest_warp_floor_address, 0x0C)
    end
    if current_highest_warp_floor > 12 and past_highest_warp_floor < 13 and current_floor() > 12 then
        memory.writebyte(highest_warp_floor_address, 0x0D)
    else
        memory.writebyte(highest_warp_floor_address, 0x0C)
    end
end

function remove_battle_card(card_value)
    if card_value < 0x9000 then
        i = 0
        while get_battle_card(i) ~= 0xFFFF do
            if card_value == get_battle_card(i) then
                memory.write_u16_le(battle_cards_address + (2 * offset), 0x0FFF)
                return
            end
        end
    end
end

function reassign_deck_pointers(old_deck_pointers)
	for k,v in pairs(old_deck_pointers) do
		for ik,iv in pairs(v) do
			set_deck_pointer(k, ik-1, iv)
		end
	end
end

function find_new_keys(old_keys, current_keys, gold_card_type, floor_number)
    local new_keys = {}
    if current_keys > old_keys then
        if floor_number < 10 then
            new_key = gold_card_type .. "F0" .. floor_number
        else
            new_key = gold_card_type .. "F" .. floor_number
        end
        set_current_gold_card_qty(gold_card_type, get_current_gold_card_qty(gold_card_type) - 1, floor_number)
        write_to_output("khcom_to_check.txt", new_key)
    end
end

function find_new_battle_cards(old_battle_cards, current_battle_cards)
    j = 1
    new_battle_card_types = {}
    old_battle_card_counts = {}
    current_battle_card_counts = {}
    for k,v in pairs(old_battle_cards) do
        old_battle_card_counts[v] = 0
        current_battle_card_counts[v] = 0
    end
    for k,v in pairs(current_battle_cards) do
        old_battle_card_counts[v] = 0
        current_battle_card_counts[v] = 0
    end
    for k,v in pairs(old_battle_cards) do
        old_battle_card_counts[v] = old_battle_card_counts[v] + 1
    end
    for k,v in pairs(current_battle_cards) do
        current_battle_card_counts[v] = current_battle_card_counts[v] + 1
    end
    for k,v in pairs(current_battle_card_counts) do
        if v > old_battle_card_counts[k] then
            i = 0
            while i < v - old_battle_card_counts[k] do
                remove_battle_card(k)
            end
            write_to_output("khcom_to_check.txt", get_battle_card_type(k))
        end
    end
end

function write_to_output(file_name, location_name)
    file = io.open("../../worlds/khcom/" .. file_name, "a")
    io.output(file)
    io.write(location_name)
    io.close(file)
end

function main_loop(last_variables)
    local current_playtime = get_playtime()
    if current_playtime == 1 then
        set_starting_deck()
        last_variables["last_battle_cards"] = get_battle_cards()
    end
    if not save_or_savestate_loaded(last_variables["Last Playtime"], current_playtime) then
        local current_floor = get_floor_number()
        if current_floor ~= last_variables["last_floor"] then
            update_current_gold_card_qty(current_floor)
            update_world_cards(current_floor)
            update_highest_warp_floor(last_variables["Last Highest Warp Floor"], get_highest_warp_floor())
            last_variables["Last Key of Beginnings"] = get_current_gold_card_qty("Key of Beginnings")
            last_variables["Last Key of Guidance"] = get_current_gold_card_qty("Key of Guidance")
            last_variables["Last Key to Truth"] = get_current_gold_card_qty("Key to Truth")
            last_variables["Last Key to Rewards"] = get_current_gold_card_qty("Key to Rewards")
        end
        local current_key_of_beginnings = get_current_gold_card_qty("Key of Beginnings")
        local current_key_of_guidance = get_current_gold_card_qty("Key of Guidance")
        local current_key_to_truth = get_current_gold_card_qty("Key to Truth")
        local current_key_to_rewards = get_current_gold_card_qty("Key to Rewards")
        local new_key_of_beginnings = find_new_keys(last_variables["Last Key of Beginnings"], current_key_of_beginnings, "Key of Beginnings", current_floor)
        find_new_keys(last_variables["Last Key of Guidance"], current_key_of_guidance, "Key of Guidance", current_floor)
        find_new_keys(last_variables["Last Key to Truth"], current_key_to_truth, "Key to Truth", current_floor)
        find_new_keys(last_variables["Last Key to Rewards"], current_key_to_rewards, "Key to Rewards", current_floor)
        local current_battle_cards = get_battle_cards()
        last_deck_pointers = get_deck_pointers()
        find_new_battle_cards(last_variables["Last Battle Cards"], current_battle_cards)
        reassign_deck_pointers(last_deck_pointers)
    end
end

function main()
    server, error = socket.bind('localhost', 52987)
    local last_variables = {}
    last_variables["Last Floor"] = get_floor_number()
    last_variables["Last Key of Beginnings"] = get_current_gold_card_qty("Key of Beginnings")
    last_variables["Last Key of Guidance"] = get_current_gold_card_qty("Key of Guidance")
    last_variables["Last Key to Truth"] = get_current_gold_card_qty("Key to Truth")
    last_variables["Last Key to Rewards"] = get_current_gold_card_qty("Key to Rewards")
    last_variables["Last Battle Cards"] = get_battle_cards()
    last_variables["Last Playtime"] = get_playtime()
    last_variables["Last Highest Warp Floor"] = get_highest_warp_floor()
    while true do
        local frame = emu.framecount()
        if frame % 20 == 0 then
            local success,err = pcall(main_loop, last_variables)
            if not success then
                print(err)
                client.pause()
                return
            end
        end
        if not (curstate == prevstate) then
            prevstate = curstate
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            
        elseif (curstate == STATE_UNINITIALIZED) then
            if  (frame % 60 == 0) then
                server:settimeout(2)
                print("Attempting to connect")
                local client, timeout = server:accept()
                if timeout == nil then
                    -- print('Initial Connection Made')
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    zeldaSocket = client
                    zeldaSocket:settimeout(0)
                end
            end
        end
        emu.frameadvance()
    end
end

main()