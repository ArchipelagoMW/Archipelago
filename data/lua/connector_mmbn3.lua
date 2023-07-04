local socket = require("socket")
local json = require('json')
local math = require('math')
require('common')

local last_modified_date = '2023-31-05' -- Should be the last modified date
local script_version = 4

local bizhawk_version = client.getversion()
local bizhawk_major, bizhawk_minor, bizhawk_patch = bizhawk_version:match("(%d+)%.(%d+)%.?(%d*)")
bizhawk_major = tonumber(bizhawk_major)
bizhawk_minor = tonumber(bizhawk_minor)
if bizhawk_patch == "" then
  bizhawk_patch = 0
else
  bizhawk_patch = tonumber(bizhawk_patch)
end

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local mmbn3Socket = nil
local frame = 0

-- States
local ITEMSTATE_NONINITIALIZED = "Game Not Yet Started" -- Game has not yet started
local ITEMSTATE_NONITEM = "Non-Itemable State" -- Do not send item now. RAM is not capable of holding
local ITEMSTATE_IDLE = "Item State Ready" -- Ready for the next item if there are any
local ITEMSTATE_SENT = "Item Sent Not Claimed" -- The ItemBit is set, but the dialog has not been closed yet
local itemState = ITEMSTATE_NONINITIALIZED

local itemQueued = nil
local itemQueueCounter = 120

local debugEnabled = false
local game_complete = false

local backup_bytes = nil

local itemsReceived  = {}
local previousMessageBit = 0x00

local key_item_start_address = 0x20019C0

-- The Canary Byte is a flag byte that is intentionally left unused. If this byte is FF, then we know the flag
-- data cannot be trusted, so we don't send checks.
local canary_byte = 0x20001A9

local charDict = {
    [' ']=0x00,['0']=0x01,['1']=0x02,['2']=0x03,['3']=0x04,['4']=0x05,['5']=0x06,['6']=0x07,['7']=0x08,['8']=0x09,['9']=0x0A,
    ['A']=0x0B,['B']=0x0C,['C']=0x0D,['D']=0x0E,['E']=0x0F,['F']=0x10,['G']=0x11,['H']=0x12,['I']=0x13,['J']=0x14,['K']=0x15,
    ['L']=0x16,['M']=0x17,['N']=0x18,['O']=0x19,['P']=0x1A,['Q']=0x1B,['R']=0x1C,['S']=0x1D,['T']=0x1E,['U']=0x1F,['V']=0x20,
    ['W']=0x21,['X']=0x22,['Y']=0x23,['Z']=0x24,['a']=0x25,['b']=0x26,['c']=0x27,['d']=0x28,['e']=0x29,['f']=0x2A,['g']=0x2B,
    ['h']=0x2C,['i']=0x2D,['j']=0x2E,['k']=0x2F,['l']=0x30,['m']=0x31,['n']=0x32,['o']=0x33,['p']=0x34,['q']=0x35,['r']=0x36,
    ['s']=0x37,['t']=0x38,['u']=0x39,['v']=0x3A,['w']=0x3B,['x']=0x3C,['y']=0x3D,['z']=0x3E,['-']=0x3F,['×']=0x40,[']=']=0x41,
    [':']=0x42,['+']=0x43,['÷']=0x44,['※']=0x45,['*']=0x46,['!']=0x47,['?']=0x48,['%']=0x49,['&']=0x4A,[',']=0x4B,['⋯']=0x4C,
    ['.']=0x4D,['・']=0x4E,[';']=0x4F,['\'']=0x50,['\"']=0x51,['~']=0x52,['/']=0x53,['(']=0x54,[')']=0x55,['「']=0x56,['」']=0x57,
    ["[V2]"]=0x58,["[V3]"]=0x59,["[V4]"]=0x5A,["[V5]"]=0x5B,['@']=0x5C,['♥']=0x5D,['♪']=0x5E,["[MB]"]=0x5F,['■']=0x60,['_']=0x61,
    ["[circle1]"]=0x62,["[circle2]"]=0x63,["[cross1]"]=0x64,["[cross2]"]=0x65,["[bracket1]"]=0x66,["[bracket2]"]=0x67,["[ModTools1]"]=0x68,
    ["[ModTools2]"]=0x69,["[ModTools3]"]=0x6A,['Σ']=0x6B,['Ω']=0x6C,['α']=0x6D,['β']=0x6E,['#']=0x6F,['…']=0x70,['>']=0x71,
    ['<']=0x72,['エ']=0x73,["[BowneGlobal1]"]=0x74,["[BowneGlobal2]"]=0x75,["[BowneGlobal3]"]=0x76,["[BowneGlobal4]"]=0x77,
    ["[BowneGlobal5]"]=0x78,["[BowneGlobal6]"]=0x79,["[BowneGlobal7]"]=0x7A,["[BowneGlobal8]"]=0x7B,["[BowneGlobal9]"]=0x7C,
    ["[BowneGlobal10]"]=0x7D,["[BowneGlobal11]"]=0x7E,['\n']=0xE8
}

local TableConcat = function(t1,t2)
   for i=1,#t2 do
      t1[#t1+1] = t2[i]
   end
   return t1
end
local int32ToByteList_le = function(x)
    bytes = {}
    hexString = string.format("%08x", x)
    for i=#hexString, 1, -2 do
      hbyte = hexString:sub(i-1, i)
      table.insert(bytes,tonumber(hbyte,16))
    end
    return bytes
end
local int16ToByteList_le = function(x)
    bytes = {}
    hexString = string.format("%04x", x)
    for i=#hexString, 1, -2 do
      hbyte = hexString:sub(i-1, i)
      table.insert(bytes,tonumber(hbyte,16))
    end
    return bytes
end

local IsInMenu = function()
    return bit.band(memory.read_u8(0x0200027A),0x10) ~= 0
end
local IsInTransition = function()
    return bit.band(memory.read_u8(0x02001880), 0x10) ~= 0
end
local IsInDialog = function()
    return bit.band(memory.read_u8(0x02009480),0x01) ~= 0
end
local IsInBattle = function()
    return memory.read_u8(0x020097F8) == 0x08
end
local IsItemQueued = function()
    return memory.read_u8(0x2000224) == 0x01
end

-- This function actually determines when you're on ANY full-screen menu (navi cust, link battle, etc.) but we
-- don't want to check any locations there either so it's fine.
local IsOnTitle = function()
    return bit.band(memory.read_u8(0x020097F8),0x04) == 0
end
local IsItemable = function()
    return not IsInMenu() and not IsInTransition() and not IsInDialog() and not IsInBattle() and not IsOnTitle() and not IsItemQueued()
end

local is_game_complete = function()
    if IsOnTitle() or itemState == ITEMSTATE_NONINITIALIZED then return game_complete end

    -- If the game is already marked complete, do not read memory
    if game_complete then return true end
    local is_alpha_defeated = bit.band(memory.read_u8(0x2000433), 0x01) ~= 0

    if (is_alpha_defeated) then
        game_complete = true
        return true
    end

    -- Game is still ongoing
    return false
end

local saveItemIndexToRAM = function(newIndex)
    memory.write_s16_le(0x20000AE,newIndex)
end

local loadItemIndexFromRAM = function()
    last_index = memory.read_s16_le(0x20000AE)
    if (last_index < 0) then
        last_index = 0
        saveItemIndexToRAM(0)
    end
    return last_index
end

local loadPlayerNameFromROM = function()
    return memory.read_bytes_as_array(0x7FFFC0,63,"ROM")
end

local check_all_locations = function()
    local location_checks = {}
    -- Title Screen should not check items
    if itemState == ITEMSTATE_NONINITIALIZED or IsInTransition() then
        return location_checks
    end
    if memory.read_u8(canary_byte) == 0xFF then
        return location_checks
    end
    for k,v in pairs(memory.read_bytes_as_dict(0x02000000, 0x434)) do
        str_k = string.format("%x", k)
        location_checks[str_k] = v
    end
    return location_checks
end

local Check_Progressive_Undernet_ID = function()
    ordered_offsets = { 0x020019DB,0x020019DC,0x020019DD,0x020019DE,0x020019DF,0x020019E0,0x020019FA,0x020019E2 }
    for i=1,#ordered_offsets do
        offset=ordered_offsets[i]

        if memory.read_u8(offset) == 0 then
            return i
        end
    end
    return 9
end
local GenerateTextBytes = function(message)
    bytes = {}
    for i = 1, #message do
        local c = message:sub(i,i)
        table.insert(bytes, charDict[c])
    end
    return bytes
end

-- Item Message Generation functions
local Next_Progressive_Undernet_ID = function(index)
    ordered_IDs = { 27,28,29,30,31,32,58,34}
    if index > #ordered_IDs then
        --It shouldn't reach this point, but if it does, just give another GigFreez I guess
        return 34
    end
    item_index=ordered_IDs[index]
    return item_index
end
local Extra_Progressive_Undernet = function()
    fragBytes = int32ToByteList_le(20)
    bytes = {
        0xF6, 0x50, fragBytes[1], fragBytes[2], fragBytes[3], fragBytes[4], 0xFF, 0xFF, 0xFF
    }
    bytes = TableConcat(bytes, GenerateTextBytes("The extra data\ndecompiles into:\n\"20 BugFrags\"!!"))
    return bytes
end

local GenerateChipGet = function(chip, code, amt)
    chipBytes = int16ToByteList_le(chip)
    bytes = {
        0xF6, 0x10, chipBytes[1], chipBytes[2], code, amt,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict[' '], charDict['c'], charDict['h'], charDict['i'], charDict['p'], charDict[' '], charDict['f'], charDict['o'], charDict['r'], charDict['\n'],

    }
    if chip < 256 then
        bytes = TableConcat(bytes, {
            charDict['\"'], 0xF9,0x00,chipBytes[1],0x01,0x00,0xF9,0x00,code,0x03, charDict['\"'],charDict['!'],charDict['!']
        })
    else
        bytes = TableConcat(bytes, {
            charDict['\"'], 0xF9,0x00,chipBytes[1],0x02,0x00,0xF9,0x00,code,0x03, charDict['\"'],charDict['!'],charDict['!']
        })
    end
    return bytes
end
local GenerateKeyItemGet = function(item, amt)
    bytes = {
        0xF6, 0x00, item, amt,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict['\n'],
        charDict['\"'], 0xF9, 0x00, item, 0x00, charDict['\"'],charDict['!'],charDict['!']
    }
    return bytes
end
local GenerateSubChipGet = function(subchip, amt)
    -- SubChips have an extra bit of trouble. If you have too many, they're supposed to skip to another text bank that doesn't give you the item
    -- Instead, I'm going to just let it get eaten
    bytes = {
        0xF6, 0x20, subchip, amt, 0xFF, 0xFF, 0xFF,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict['\n'],
        charDict['S'], charDict['u'], charDict['b'], charDict['C'], charDict['h'], charDict['i'], charDict['p'], charDict[' '], charDict['f'], charDict['o'], charDict['r'], charDict['\n'],
        charDict['\"'], 0xF9, 0x00, subchip, 0x00, charDict['\"'],charDict['!'],charDict['!']
    }
    return bytes
end
local GenerateZennyGet = function(amt)
    zennyBytes = int32ToByteList_le(amt)
    bytes = {
        0xF6, 0x30, zennyBytes[1], zennyBytes[2], zennyBytes[3], zennyBytes[4], 0xFF, 0xFF, 0xFF,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict['\n'], charDict['\"']
    }
    -- The text needs to be added one char at a time, so we need to convert the number to a string then iterate through it
    zennyStr = tostring(amt)
    for i = 1, #zennyStr do
        local c = zennyStr:sub(i,i)
        table.insert(bytes, charDict[c])
    end
    bytes = TableConcat(bytes, {
        charDict[' '], charDict['Z'], charDict['e'], charDict['n'], charDict['n'], charDict['y'], charDict['s'], charDict['\"'],charDict['!'],charDict['!']
    })
    return bytes
end
local GenerateProgramGet = function(program, color, amt)
    bytes = {
        0xF6, 0x40, (program * 4), amt, color,
        charDict['G'], charDict['o'], charDict['t'], charDict[' '], charDict['a'], charDict[' '], charDict['N'], charDict['a'], charDict['v'], charDict['i'], charDict['\n'],
        charDict['C'], charDict['u'], charDict['s'], charDict['t'], charDict['o'], charDict['m'], charDict['i'], charDict['z'], charDict['e'], charDict['r'], charDict[' '], charDict['P'], charDict['r'], charDict['o'], charDict['g'], charDict['r'], charDict['a'], charDict['m'], charDict[':'], charDict['\n'],
        charDict['\"'], 0xF9, 0x00, program, 0x05, charDict['\"'],charDict['!'],charDict['!']
    }

    return bytes
end
local GenerateBugfragGet = function(amt)
    fragBytes = int32ToByteList_le(amt)
    bytes = {
        0xF6, 0x50, fragBytes[1], fragBytes[2], fragBytes[3], fragBytes[4], 0xFF, 0xFF, 0xFF,
        charDict['G'], charDict['o'], charDict['t'], charDict[':'], charDict['\n'], charDict['\"']
    }
    -- The text needs to be added one char at a time, so we need to convert the number to a string then iterate through it
    bugFragStr = tostring(amt)
    for i = 1, #bugFragStr do
        local c = bugFragStr:sub(i,i)
        table.insert(bytes, charDict[c])
    end
    bytes = TableConcat(bytes, {
        charDict[' '], charDict['B'], charDict['u'], charDict['g'], charDict['F'], charDict['r'], charDict['a'], charDict['g'], charDict['s'], charDict['\"'],charDict['!'],charDict['!']
    })
    return bytes
end
local GenerateGetMessageFromItem = function(item)
    --Special case for progressive undernet
    if item["type"] == "undernet" then
        undernet_id = Check_Progressive_Undernet_ID()
        if undernet_id > 8 then
            return Extra_Progressive_Undernet()
        end
        return GenerateKeyItemGet(Next_Progressive_Undernet_ID(undernet_id),1)
    elseif item["type"] == "chip" then
        return GenerateChipGet(item["itemID"], item["subItemID"], item["count"])
    elseif item["type"] == "key" then
        return GenerateKeyItemGet(item["itemID"], item["count"])
    elseif item["type"] == "subchip" then
        return GenerateSubChipGet(item["itemID"], item["count"])
    elseif item["type"] == "zenny" then
        return GenerateZennyGet(item["count"])
    elseif item["type"] == "program" then
        return GenerateProgramGet(item["itemID"], item["subItemID"], item["count"])
    elseif item["type"] == "bugfrag" then
        return GenerateBugfragGet(item["count"])
    end

    return GenerateTextBytes("Empty Message")
end

local GetMessage = function(item)
    startBytes = {0x02, 0x00}
    playerLockBytes = {0xF8,0x00, 0xF8, 0x10}
    msgOpenBytes = {0xF1, 0x02}
    textBytes = GenerateTextBytes("Receiving\ndata from\n"..item["sender"]..".")
    dotdotWaitBytes = {0xEA,0x00,0x0A,0x00,0x4D,0xEA,0x00,0x0A,0x00,0x4D}
    continueBytes = {0xEB, 0xE9}
    -- continueBytes = {0xE9}
    playReceiveAnimationBytes = {0xF8,0x04,0x18}
    chipGiveBytes = GenerateGetMessageFromItem(item)
    playerFinishBytes = {0xF8, 0x0C}
    playerUnlockBytes={0xEB, 0xF8, 0x08}
    -- playerUnlockBytes={0xF8, 0x08}
    endMessageBytes = {0xF8, 0x10, 0xE7}

    bytes = {}
    bytes = TableConcat(bytes,startBytes)
    bytes = TableConcat(bytes,playerLockBytes)
    bytes = TableConcat(bytes,msgOpenBytes)
    bytes = TableConcat(bytes,textBytes)
    bytes = TableConcat(bytes,dotdotWaitBytes)
    bytes = TableConcat(bytes,continueBytes)
    bytes = TableConcat(bytes,playReceiveAnimationBytes)
    bytes = TableConcat(bytes,chipGiveBytes)
    bytes = TableConcat(bytes,playerFinishBytes)
    bytes = TableConcat(bytes,playerUnlockBytes)
    bytes = TableConcat(bytes,endMessageBytes)
    return bytes
end

local getChipCodeIndex = function(chip_id, chip_code)
    chipCodeArrayStartAddress = 0x8011510 + (0x20 * chip_id)
    for i=1,6 do
        currentCode = memory.read_u8(chipCodeArrayStartAddress + (i-1))
        if currentCode == chip_code then
            return i-1
        end
    end
    return 0
end

local getProgramColorIndex = function(program_id, program_color)
    -- The general case, most programs use white pink or yellow. This is the values the enums already have
    if program_id >= 20 and program_id <= 47 then
        return program_color-1
    end
    --The final three programs only have a color index 0, so just return those
    if program_id > 47 then
        return 0
    end
    --BrakChrg as an AP item only comes in orange, index 0
    if program_id == 3 then
        return 0
    end
    -- every other AP obtainable program returns only color index 3
    return 3
end

local addChip = function(chip_id, chip_code, amount)
    chipStartAddress = 0x02001F60
    chipOffset = 0x12 * chip_id
    chip_code_index = getChipCodeIndex(chip_id, chip_code)
    currentChipAddress = chipStartAddress + chipOffset + chip_code_index
    currentChipCount = memory.read_u8(currentChipAddress)
    memory.write_u8(currentChipAddress,currentChipCount+amount)
end

local addProgram = function(program_id, program_color, amount)
    programStartAddress = 0x02001A80
    programOffset = 0x04 * program_id
    program_code_index = getProgramColorIndex(program_id, program_color)
    currentProgramAddress = programStartAddress + programOffset + program_code_index
    currentProgramCount = memory.read_u8(currentProgramAddress)
    memory.write_u8(currentProgramAddress, currentProgramCount+amount)
end

local addSubChip = function(subchip_id, amount)
    subChipStartAddress = 0x02001A30
    --SubChip indices start after the key items, so subtract 112 from the index to get the actual subchip index
    currentSubChipAddress = subChipStartAddress + (subchip_id - 112)
    currentSubChipCount = memory.read_u8(currentSubChipAddress)
    --TODO check submem, reject if number too big
    memory.write_u8(currentSubChipAddress, currentSubChipCount+amount)
end

local changeZenny = function(val)
	if val == nil then
		return 0
	end
	if memory.read_u32_le(0x20018F4) <= math.abs(tonumber(val)) and tonumber(val) < 0 then
		memory.write_u32_le(0x20018f4, 0)
		val = 0
		return "empty"
	end
	memory.write_u32_le(0x20018f4, memory.read_u32_le(0x20018F4) + tonumber(val))
	if memory.read_u32_le(0x20018F4) > 999999 then
		memory.write_u32_le(0x20018F4, 999999)
	end
	return val
end

local changeFrags = function(val)
	if val == nil then
		return 0
	end
	if memory.read_u16_le(0x20018F8) <= math.abs(tonumber(val)) and tonumber(val) < 0 then
		memory.write_u16_le(0x20018f8, 0)
		val = 0
		return "empty"
	end
	memory.write_u16_le(0x20018f8, memory.read_u16_le(0x20018F8) + tonumber(val))
	if memory.read_u16_le(0x20018F8) > 9999 then
		memory.write_u16_le(0x20018F8, 9999)
	end
	return val
end

-- Fix Health Pools
local fix_hp = function()
	-- Current Health fix
	if IsInBattle() and not (memory.read_u16_le(0x20018A0) == memory.read_u16_le(0x2037294)) then
		memory.write_u16_le(0x20018A0, memory.read_u16_le(0x2037294))
	end

	-- Max Health Fix
	if IsInBattle() and not (memory.read_u16_le(0x20018A2) == memory.read_u16_le(0x2037296)) then
		memory.write_u16_le(0x20018A2, memory.read_u16_le(0x2037296))
	end
end

local changeRegMemory = function(amt)
    regMemoryAddress = 0x02001897
    currentRegMem = memory.read_u8(regMemoryAddress)
    memory.write_u8(regMemoryAddress, currentRegMem + amt)
end

local changeMaxHealth = function(val)
	fix_hp()
	if val == nil then
		fix_hp()
		return 0
	end
	if math.abs(tonumber(val)) >= memory.read_u16_le(0x20018A2) and tonumber(val) < 0 then
		memory.write_u16_le(0x20018A2, 0)
		if IsInBattle() then
			memory.write_u16_le(0x2037296, memory.read_u16_le(0x20018A2))
			if memory.read_u16_le(0x2037296) >= memory.read_u16_le(0x20018A2) then
				memory.write_u16_le(0x2037296, memory.read_u16_le(0x20018A2))
			end
		end
		fix_hp()
		return "lethal"
	end
	memory.write_u16_le(0x20018A2, memory.read_u16_le(0x20018A2) + tonumber(val))
	if memory.read_u16_le(0x20018A2) > 9999 then
		memory.write_u16_le(0x20018A2, 9999)
	end
	if IsInBattle() then
		memory.write_u16_le(0x2037296, memory.read_u16_le(0x20018A2))
	end
	fix_hp()
	return val
end

local SendItem = function(item)
    if item["type"] == "undernet" then
        undernet_id = Check_Progressive_Undernet_ID()
        if undernet_id > 8 then
            -- Generate Extra BugFrags
            changeFrags(20)
            gui.addmessage("Receiving extra Undernet Rank from "..item["sender"]..", +20 BugFrags")
            -- print("Receiving extra Undernet Rank from "..item["sender"]..", +20 BugFrags")
        else
            itemAddress = key_item_start_address + Next_Progressive_Undernet_ID(undernet_id)

            itemCount = memory.read_u8(itemAddress)
            itemCount = itemCount + item["count"]
            memory.write_u8(itemAddress, itemCount)
            gui.addmessage("Received Undernet Rank from player "..item["sender"])
            -- print("Received Undernet Rank from player "..item["sender"])
        end
    elseif item["type"] == "chip" then
        addChip(item["itemID"], item["subItemID"], item["count"])
        gui.addmessage("Received Chip "..item["itemName"].." from player "..item["sender"])
        -- print("Received Chip "..item["itemName"].." from player "..item["sender"])
    elseif item["type"] == "key" then
        itemAddress = key_item_start_address + item["itemID"]
        itemCount = memory.read_u8(itemAddress)
        itemCount = itemCount + item["count"]
        memory.write_u8(itemAddress, itemCount)
        -- HPMemory will increase the internal counter but not actually increase the HP. If the item is one of those, do that
        if item["itemID"] == 96 then
            changeMaxHealth(20)
        end
        -- Same for the RegUps, but there's three of those
        if item["itemID"] == 98 then
            changeRegMemory(1)
        end
        if item["itemID"] == 99 then
            changeRegMemory(2)
        end
        if item["itemID"] == 100 then
            changeRegMemory(3)
        end
        gui.addmessage("Received Key Item "..item["itemName"].." from player "..item["sender"])
        -- print("Received Key Item "..item["itemName"].." from player "..item["sender"])
    elseif item["type"] == "subchip" then
        addSubChip(item["itemID"], item["count"])
        gui.addmessage("Received SubChip "..item["itemName"].." from player "..item["sender"])
        -- print("Received SubChip "..item["itemName"].." from player "..item["sender"])
    elseif item["type"] == "zenny" then
        changeZenny(item["count"])
        gui.addmessage("Received "..item["count"].."z from "..item["sender"])
        -- print("Received "..item["count"].."z from "..item["sender"])
    elseif item["type"] == "program" then
        addProgram(item["itemID"], item["subItemID"], item["count"])
        gui.addmessage("Received Program "..item["itemName"].." from player "..item["sender"])
        -- print("Received Program "..item["itemName"].." from player "..item["sender"])
    elseif item["type"] == "bugfrag" then
        changeFrags(item["count"])
        gui.addmessage("Received "..item["count"].." BugFrag(s) from "..item["sender"])
        -- print("Received "..item["count"].." BugFrag(s) from "..item["sender"])
    end
end

-- Set the flags for opening the shortcuts as soon as the Cybermetro passes are received to save having to check email
local OpenShortcuts = function()
    if (memory.read_u8(key_item_start_address + 92) > 0) then
        memory.write_u8(0x2000032, bit.bor(memory.read_u8(0x2000032),0x10))
    end
    -- if CSciPass
    if (memory.read_u8(key_item_start_address + 93) > 0) then
        memory.write_u8(0x2000032, bit.bor(memory.read_u8(0x2000032),0x08))
    end
    if (memory.read_u8(key_item_start_address + 94) > 0) then
        memory.write_u8(0x2000032, bit.bor(memory.read_u8(0x2000032),0x20))
    end
    if (memory.read_u8(key_item_start_address + 95) > 0) then
       memory.write_u8(0x2000032, bit.bor(memory.read_u8(0x2000032),0x40))
    end
end

local RestoreItemRam = function()
    if backup_bytes ~= nil then
        memory.write_bytes_as_array(0x203fe10, backup_bytes)
    end
    backup_bytes = nil
end

local process_block = function(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    debugEnabled = block['debug']
    -- Queue item for receiving, if one exists
    if (itemsReceived ~= block['items']) then
        itemsReceived = block['items']
    end
    return
end

local itemStateMachineProcess = function()
    if itemState == ITEMSTATE_NONINITIALIZED then
        itemQueueCounter = 120
        -- Only exit this state the first time a dialog window pops up. This way we know for sure that we're ready to receive
        if not IsInMenu() and (IsInDialog() or IsInTransition()) then
            itemState = ITEMSTATE_NONITEM
        end
    elseif itemState == ITEMSTATE_NONITEM then
        itemQueueCounter = 120
        -- Always attempt to restore the previously stored memory in this state
        -- Exit this state whenever the game is in an itemable status
        if IsItemable() then
            itemState = ITEMSTATE_IDLE
        end
    elseif itemState == ITEMSTATE_IDLE then
        -- Remain Idle until an item is sent or we enter a non itemable status
        if not IsItemable() then
            itemState = ITEMSTATE_NONITEM
        end
        if itemQueueCounter == 0 then
            if #itemsReceived > loadItemIndexFromRAM() and not IsItemQueued() then
                itemQueued = itemsReceived[loadItemIndexFromRAM()+1]
                SendItem(itemQueued)
                itemState = ITEMSTATE_SENT
            end
        else
            itemQueueCounter = itemQueueCounter - 1
        end
    elseif itemState == ITEMSTATE_SENT then
        -- Once the item is sent, wait for the dialog to close. Then clear the item bit and be ready for the next item.
        if IsInTransition() or IsInMenu() or IsOnTitle() then
            itemState = ITEMSTATE_NONITEM
            itemQueued = nil
            RestoreItemRam()
        elseif not IsInDialog() then
            itemState = ITEMSTATE_IDLE
            saveItemIndexToRAM(itemQueued["itemIndex"])
            itemQueued = nil
            RestoreItemRam()
        end
    end
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
end

local send = function()
    -- Determine message to send back
    local retTable = {}
    retTable["playerName"] = loadPlayerNameFromROM()
    retTable["scriptVersion"] = script_version
    retTable["locations"] = check_all_locations()
    retTable["gameComplete"] = is_game_complete()

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
    if (bizhawk_major > 2 or (bizhawk_major == 2 and bizhawk_minor >= 7)==false) then
        print("Must use a version of bizhawk 2.7.0 or higher")
        return
    end
    server, error = socket.bind('localhost', 28922)

    while true do
        frame = frame + 1

        if not (curstate == prevstate) then
            prevstate = curstate
        end

        itemStateMachineProcess()

        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            -- If we're connected and everything's fine, receive and send data from the network
            if (frame % 60 == 0) then
                receive()
                send()
                -- Perform utility functions which read and write data but aren't directly related to checks
                OpenShortcuts()
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            -- If we're uninitialized, attempt to make the connection.
            if (frame % 120 == 0) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    mmbn3Socket = client
                    mmbn3Socket:settimeout(0)
                else
                    print('Connection failed, ensure MMBN3Client is running and rerun connector_mmbn3.lua')
                    return
                end
            end
        end

        -- Handle the debug data display
        gui.cleartext()
        if debugEnabled then
            -- gui.text(0,0,"Item Queued: "..tostring(IsItemQueued()))
            -- gui.text(0,16,"In Battle: "..tostring(IsInBattle()))
            -- gui.text(0,32,"In Dialog: "..tostring(IsInDialog()))
            -- gui.text(0,48,"In Menu: "..tostring(IsInMenu()))
            gui.text(0,48,"Item Wait Time: "..tostring(itemQueueCounter))
            gui.text(0,64,itemState)
            if itemQueued == nil then
                gui.text(0,80,"No item queued")
            else
                gui.text(0,80,itemQueued["type"].." "..itemQueued["itemID"])
            end
            gui.text(0,96,"Item Index: "..loadItemIndexFromRAM())
        end

        emu.frameadvance()
    end
end

main()