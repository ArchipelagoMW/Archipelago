local socket = require("socket")
local json = require('json')
local math = require('math')
require("common")

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local ITEM_INDEX = 0x03
local WEAPON_INDEX = 0x07
local ARMOR_INDEX = 0x0B

local goldLookup = {
    [0x16C] = 10,
    [0x16D] = 20,
    [0x16E] = 25,
    [0x16F] = 30,
    [0x170] = 55,
    [0x171] = 70,
    [0x172] = 85,
    [0x173] = 110,
    [0x174] = 135,
    [0x175] = 155,
    [0x176] = 160,
    [0x177] = 180,
    [0x178] = 240,
    [0x179] = 255,
    [0x17A] = 260,
    [0x17B] = 295,
    [0x17C] = 300,
    [0x17D] = 315,
    [0x17E] = 330,
    [0x17F] = 350,
    [0x180] = 385,
    [0x181] = 400,
    [0x182] = 450,
    [0x183] = 500,
    [0x184] = 530,
    [0x185] = 575,
    [0x186] = 620,
    [0x187] = 680,
    [0x188] = 750,
    [0x189] = 795,
    [0x18A] = 880,
    [0x18B] = 1020,
    [0x18C] = 1250,
    [0x18D] = 1455,
    [0x18E] = 1520,
    [0x18F] = 1760,
    [0x190] = 1975,
    [0x191] = 2000,
    [0x192] = 2750,
    [0x193] = 3400,
    [0x194] = 4150,
    [0x195] = 5000,
    [0x196] = 5450,
    [0x197] = 6400,
    [0x198] = 6720,
    [0x199] = 7340,
    [0x19A] = 7690,
    [0x19B] = 7900,
    [0x19C] = 8135,
    [0x19D] = 9000,
    [0x19E] = 9300,
    [0x19F] = 9500,
    [0x1A0] = 9900,
    [0x1A1] = 10000,
    [0x1A2] = 12350,
    [0x1A3] = 13000,
    [0x1A4] = 13450,
    [0x1A5] = 14050,
    [0x1A6] = 14720,
    [0x1A7] = 15000,
    [0x1A8] = 17490,
    [0x1A9] = 18010,
    [0x1AA] = 19990,
    [0x1AB] = 20000,
    [0x1AC] = 20010,
    [0x1AD] = 26000,
    [0x1AE] = 45000,
    [0x1AF] = 65000
}

local extensionConsumableLookup = {
    [432] = 0x3C,
    [436] = 0x3C,
    [440] = 0x3C,
    [433] = 0x3D,
    [437] = 0x3D,
    [441] = 0x3D,
    [434] = 0x3E,
    [438] = 0x3E,
    [442] = 0x3E,
    [435] = 0x3F,
    [439] = 0x3F,
    [443] = 0x3F
}

local noOverworldItemsLookup = {
    [499] = 0x2B,
    [500] = 0x12,
}

local consumableStacks = nil
local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local ff1Socket = nil
local frame = 0

local isNesHawk = false


--Sets correct memory access functions based on whether NesHawk or QuickNES is loaded
local function defineMemoryFunctions()
	local memDomain = {}
	local domains = memory.getmemorydomainlist()
	if domains[1] == "System Bus" then
		--NesHawk
		isNesHawk = true
		memDomain["systembus"] = function() memory.usememorydomain("System Bus") end
		memDomain["saveram"]   = function() memory.usememorydomain("Battery RAM") end
		memDomain["rom"]       = function() memory.usememorydomain("PRG ROM") end
	elseif domains[1] == "WRAM" then
		--QuickNES
		memDomain["systembus"] = function() memory.usememorydomain("System Bus") end
		memDomain["saveram"]   = function() memory.usememorydomain("WRAM") end
		memDomain["rom"]       = function() memory.usememorydomain("PRG ROM") end
	end
	return memDomain
end

local memDomain = defineMemoryFunctions()

local function StateOKForMainLoop()
    memDomain.saveram()
    local A = u8(0x102) -- Party Made
    local B = u8(0x0FC)
    local C = u8(0x0A3)
    return A ~= 0x00 and not (A== 0xF2 and B == 0xF2 and C == 0xF2)
end

function generateLocationChecked()
    memDomain.saveram()
    data = uRange(0x01FF, 0x101)
    data[0] = nil
    return data
end

function setConsumableStacks()
    memDomain.rom()
    consumableStacks = {}
    -- In order shards, tent, cabin, house, heal, pure, soft, ext1, ext2, ext3, ex4
    consumableStacks[0x35] = 1
    consumableStacks[0x36] = u8(0x47400) + 1
    consumableStacks[0x37] = u8(0x47401) + 1
    consumableStacks[0x38] = u8(0x47402) + 1
    consumableStacks[0x39] = u8(0x47403) + 1
    consumableStacks[0x3A] = u8(0x47404) + 1
    consumableStacks[0x3B] = u8(0x47405) + 1
    consumableStacks[0x3C] = u8(0x47406) + 1
    consumableStacks[0x3D] = u8(0x47407) + 1
    consumableStacks[0x3E] = u8(0x47408) + 1
    consumableStacks[0x3F] = u8(0x47409) + 1
end

function getEmptyWeaponSlots()
    memDomain.saveram()
    ret = {}
    count = 1
    slot1 = uRange(0x118, 0x4)
    slot2 = uRange(0x158, 0x4)
    slot3 = uRange(0x198, 0x4)
    slot4 = uRange(0x1D8, 0x4)
    for i,v in pairs(slot1) do
        if v == 0 then
            ret[count] = 0x118 + i
            count = count + 1
        end
    end
    for i,v in pairs(slot2) do
        if v == 0 then
            ret[count] = 0x158 + i
            count = count + 1
        end
    end
    for i,v in pairs(slot3) do
        if v == 0 then
            ret[count] = 0x198 + i
            count = count + 1
        end
    end
    for i,v in pairs(slot4) do
        if v == 0 then
            ret[count] = 0x1D8 + i
            count = count + 1
        end
    end
    return ret
end

function getEmptyArmorSlots()
    memDomain.saveram()
    ret = {}
    count = 1
    slot1 = uRange(0x11C, 0x4)
    slot2 = uRange(0x15C, 0x4)
    slot3 = uRange(0x19C, 0x4)
    slot4 = uRange(0x1DC, 0x4)
    for i,v in pairs(slot1) do
        if v == 0 then
            ret[count] = 0x11C + i
            count = count + 1
        end
    end
    for i,v in pairs(slot2) do
        if v == 0 then
            ret[count] = 0x15C + i
            count = count + 1
        end
    end
    for i,v in pairs(slot3) do
        if v == 0 then
            ret[count] = 0x19C + i
            count = count + 1
        end
    end
    for i,v in pairs(slot4) do
        if v == 0 then
            ret[count] = 0x1DC + i
            count = count + 1
        end
    end
    return ret
end
local function slice (tbl, s, e)
    local pos, new = 1, {}
    for i = s + 1, e do
        new[pos] = tbl[i]
        pos = pos + 1
    end
    return new
end
function processBlock(block)
    local msgBlock = block['messages']
    if msgBlock ~= nil then
        for i, v in pairs(msgBlock) do
            if itemMessages[i] == nil then
                local msg = {TTL=450, message=v, color=0xFFFF0000}
                itemMessages[i] = msg
            end
        end
    end
    local itemsBlock = block["items"]
    memDomain.saveram()
    isInGame = u8(0x102)
    if itemsBlock ~= nil and isInGame ~= 0x00 then
        if consumableStacks == nil then
            setConsumableStacks()
        end
        memDomain.saveram()
--         print('ITEMBLOCK: ')
--         print(itemsBlock)
        itemIndex = u8(ITEM_INDEX)
--         print('ITEMINDEX: '..itemIndex)
        for i, v in pairs(slice(itemsBlock, itemIndex, #itemsBlock)) do
            -- Minus the offset and add to the correct domain
            local memoryLocation = v
            if v >= 0x100 and v <= 0x114 then
                -- This is a key item
                memoryLocation = memoryLocation - 0x0E0
                wU8(memoryLocation, 0x01)
            elseif v >= 0x1E0 and v <= 0x1F2 then
                -- This is a movement item
                -- Minus Offset (0x100) - movement offset (0xE0)
                memoryLocation = memoryLocation - 0x1E0
                -- Canal is a flipped bit
                if memoryLocation == 0x0C then
                    wU8(memoryLocation, 0x00)
                else
                    wU8(memoryLocation, 0x01)
                end
            elseif v >= 0x1F3 and v <= 0x1F4 then
                -- NoOverworld special items
                memoryLocation = noOverworldItemsLookup[v]
                wU8(memoryLocation, 0x01)
            elseif v >= 0x16C and v <= 0x1AF then
                -- This is a gold item
                amountToAdd = goldLookup[v]
                biggest = u8(0x01E)
                medium = u8(0x01D)
                smallest = u8(0x01C)
                currentValue = 0x10000 * biggest + 0x100 * medium + smallest
                newValue = currentValue + amountToAdd
                newBiggest = math.floor(newValue / 0x10000)
                newMedium = math.floor(math.fmod(newValue, 0x10000) / 0x100)
                newSmallest = math.floor(math.fmod(newValue, 0x100))
                wU8(0x01E, newBiggest)
                wU8(0x01D, newMedium)
                wU8(0x01C, newSmallest)
            elseif v >= 0x115 and v <= 0x11B then
                -- This is a regular consumable OR a shard
                -- Minus Offset (0x100) + item offset (0x20)
                memoryLocation = memoryLocation - 0x0E0
                currentValue = u8(memoryLocation)
                amountToAdd = consumableStacks[memoryLocation]
                if currentValue < 99 then
                    wU8(memoryLocation, currentValue + amountToAdd)
                end
            elseif v >= 0x1B0  and v <= 0x1BB then
                -- This is an extension consumable
                memoryLocation = extensionConsumableLookup[v]
                currentValue = u8(memoryLocation)
                amountToAdd = consumableStacks[memoryLocation]
                if currentValue < 99 then
                    value = currentValue + amountToAdd
                    if value > 99 then
                        value = 99
                    end
                    wU8(memoryLocation, value)
                end
            end
        end
        if #itemsBlock > itemIndex then
            wU8(ITEM_INDEX, #itemsBlock)
        end

        memDomain.saveram()
        weaponIndex = u8(WEAPON_INDEX)
        emptyWeaponSlots = getEmptyWeaponSlots()
        lastUsedWeaponIndex = weaponIndex
--         print('WEAPON_INDEX: '.. weaponIndex)
        memDomain.saveram()
        for i, v in pairs(slice(itemsBlock, weaponIndex, #itemsBlock)) do
            if v >= 0x11C and v <= 0x143 then
                -- Minus the offset and add to the correct domain
                local itemValue = v - 0x11B
                if #emptyWeaponSlots > 0 then
                    slot = table.remove(emptyWeaponSlots, 1)
                    wU8(slot, itemValue)
                    lastUsedWeaponIndex = weaponIndex + i
                else
                    break
                end
            end
        end
        if lastUsedWeaponIndex ~= weaponIndex then
            wU8(WEAPON_INDEX, lastUsedWeaponIndex)
        end
        memDomain.saveram()
        armorIndex = u8(ARMOR_INDEX)
        emptyArmorSlots = getEmptyArmorSlots()
        lastUsedArmorIndex = armorIndex
--         print('ARMOR_INDEX: '.. armorIndex)
        memDomain.saveram()
        for i, v in pairs(slice(itemsBlock, armorIndex, #itemsBlock)) do
            if v >= 0x144 and v <= 0x16B then
                -- Minus the offset and add to the correct domain
                local itemValue = v - 0x143
                if #emptyArmorSlots > 0 then
                    slot = table.remove(emptyArmorSlots, 1)
                    wU8(slot, itemValue)
                    lastUsedArmorIndex = armorIndex + i
                else
                    break
                end
            end
        end
        if lastUsedArmorIndex ~= armorIndex then
            wU8(ARMOR_INDEX, lastUsedArmorIndex)
        end
    end
end

function receive()
    l, e = ff1Socket:receive()
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
    processBlock(json.decode(l))

    -- Determine Message to send back
    memDomain.rom()
    local playerName = uRange(0x7BCBF, 0x41)
    playerName[0] = nil
    local retTable = {}
    retTable["playerName"] = playerName
    if StateOKForMainLoop() then
        retTable["locations"] = generateLocationChecked()
    end
    msg = json.encode(retTable).."\n"
    local ret, error = ff1Socket:send(msg)
    if ret == nil then
        print(error)
    elseif curstate == STATE_INITIAL_CONNECTION_MADE then
        curstate = STATE_TENTATIVELY_CONNECTED
    elseif curstate == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        itemMessages["(0,0)"] = {TTL=240, message="Connected", color="green"}
        curstate = STATE_OK
    end
end

function main()
    if not checkBizHawkVersion() then
        return
    end
    server, error = socket.bind('localhost', 52980)

    while true do
        gui.drawEllipse(248, 9, 6, 6, "Black", "Yellow")
        frame = frame + 1
        drawMessages()
        if not (curstate == prevstate) then
            -- console.log("Current state: "..curstate)
            prevstate = curstate
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 60 == 0) then
                gui.drawEllipse(248, 9, 6, 6, "Black", "Blue")
                receive()
            else
                gui.drawEllipse(248, 9, 6, 6, "Black", "Green")
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            gui.drawEllipse(248, 9, 6, 6, "Black", "White")
            if  (frame % 60 == 0) then
                gui.drawEllipse(248, 9, 6, 6, "Black", "Yellow")

                drawText(5, 8, "Waiting for client", 0xFFFF0000)
                drawText(5, 32, "Please start FF1Client.exe", 0xFFFF0000)

                -- Advance so the messages are drawn
                emu.frameadvance()
                server:settimeout(2)
                print("Attempting to connect")
                local client, timeout = server:accept()
                if timeout == nil then
                    -- print('Initial Connection Made')
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    ff1Socket = client
                    ff1Socket:settimeout(0)
                end
            end
        end
        emu.frameadvance()
    end
end

main()
