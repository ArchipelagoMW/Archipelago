local socket = require("socket")
local json = require('json')
local math = require('math')

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

local itemMessages = {}
local consumableStacks = nil
local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local ff1Socket = nil
local frame = 0

local u8 = nil
local wU8 = nil
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
u8 = memory.read_u8
wU8 = memory.write_u8
uRange = memory.readbyterange

local function StateOKForMainLoop()
    memDomain.saveram()
    local A = u8(0x102) -- Party Made
    local B = u8(0x0FC)
    local C = u8(0x0A3)
    return A ~= 0x00 and not (A== 0xF2 and B == 0xF2 and C == 0xF2)
end

function table.empty (self)
    for _, _ in pairs(self) do
        return false
    end
    return true
end

function slice (tbl, s, e)
    local pos, new = 1, {}
    for i = s + 1, e do
        new[pos] = tbl[i]
        pos = pos + 1
    end
    return new
end

local bizhawk_version = client.getversion()
local is23Or24Or25 = (bizhawk_version=="2.3.1") or (bizhawk_version:sub(1,3)=="2.4") or (bizhawk_version:sub(1,3)=="2.5")
local is26To28 =  (bizhawk_version:sub(1,3)=="2.6") or (bizhawk_version:sub(1,3)=="2.7") or (bizhawk_version:sub(1,3)=="2.8")

local function getMaxMessageLength()
    if is23Or24Or25 then
        return client.screenwidth()/11
    elseif is26To28 then
        return client.screenwidth()/12
    end
end

local function drawText(x, y, message, color)
    if is23Or24Or25 then
        gui.addmessage(message)
    elseif is26To28 then
        gui.drawText(x, y, message, color, 0xB0000000, 18, "Courier New", nil, nil, nil, "client")
    end
end

local function clearScreen()
    if is23Or24Or25 then
        return
    elseif is26To28 then
        drawText(0, 0, "", "black")
    end
end

local function drawMessages()
    if table.empty(itemMessages) then
        clearScreen()
        return
    end
    local y = 10
    found = false
    maxMessageLength = getMaxMessageLength()
    for k, v in pairs(itemMessages) do
        if v["TTL"] > 0 then
            message = v["message"]
            while true do
                drawText(5, y, message:sub(1, maxMessageLength), v["color"])
                y = y + 16

                message = message:sub(maxMessageLength + 1, message:len())
                if message:len() == 0 then
                    break
                end
            end
            newTTL = 0
            if is26To28 then
                newTTL = itemMessages[k]["TTL"] - 1
            end
            itemMessages[k]["TTL"] = newTTL
            found = true
        end
    end
    if found == false then
        clearScreen()
    end
end

function generateLocationChecked()
    memDomain.saveram()
    data = uRange(0x01FF, 0x101)
    data[0] = nil
    return data
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
        memDomain.saveram()
--         print('ITEMBLOCK: ')
--         print(itemsBlock)
--         print('ITEMINDEX: '..itemIndex)

        memDomain.saveram()
        if lastUsedWeaponIndex ~= weaponIndex then
            wU8(WEAPON_INDEX, lastUsedWeaponIndex)
        end
        memDomain.saveram()
        armorIndex = u8(ARMOR_INDEX)
        lastUsedArmorIndex = armorIndex
--         print('ARMOR_INDEX: '.. armorIndex)
        memDomain.saveram()
        if lastUsedArmorIndex ~= armorIndex then
            wU8(ARMOR_INDEX, lastUsedArmorIndex)
        end
    end
end

function difference(a, b)
    local aa = {}
    for k,v in pairs(a) do aa[v]=true end
    for k,v in pairs(b) do aa[v]=nil end
    local ret = {}
    local n = 0
    for k,v in pairs(a) do
        if aa[v] then n=n+1 ret[n]=v end
    end
    return ret
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
    if (is23Or24Or25 or is26To28) == false then
        print("Must use a version of bizhawk 2.3.1 or higher")
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
