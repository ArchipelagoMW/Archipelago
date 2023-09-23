--Shamelessly based off the FF1 lua

local socket = require("socket")
local json = require('json')
local math = require('math')
require("common")
local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local consumableStacks = nil
local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local zeldaSocket = nil
local frame = 0
local gameMode = 0

local cave_index
local triforce_byte
local game_state

local isNesHawk = false

local shopsChecked = {}
local shopSlotLeft       = 0x0628
local shopSlotMiddle     = 0x0629
local shopSlotRight      = 0x062A

--N.B.: you won't find these in a RAM map. They're flag values that the base patch derives from the cave ID.
local blueRingShopBit       = 0x40
local potionShopBit         = 0x02
local arrowShopBit          = 0x08
local candleShopBit         = 0x10
local shieldShopBit         = 0x20
local takeAnyCaveBit        = 0x01


local sword                 = 0x0657
local bombs                 = 0x0658
local maxBombs              = 0x067C
local keys                  = 0x066E
local arrow                 = 0x0659
local bow                   = 0x065A
local candle                = 0x065B
local recorder              = 0x065C
local food                  = 0x065D
local waterOfLife           = 0x065E
local magicalRod            = 0x065F
local raft                  = 0x0660
local bookOfMagic           = 0x0661
local ring                  = 0x0662
local stepladder            = 0x0663
local magicalKey            = 0x0664
local powerBracelet         = 0x0665
local letter                = 0x0666
local clockItem             = 0x066C
local heartContainers       = 0x066F
local partialHearts         = 0x0670
local triforceFragments     = 0x0671
local boomerang             = 0x0674
local magicalBoomerang      = 0x0675
local magicalShield         = 0x0676
local rupeesToAdd           = 0x067D
local rupeesToSubtract      = 0x067E
local itemsObtained         = 0x0677
local takeAnyCavesChecked   = 0x0678
local localTriforce         = 0x0679
local bonusItemsObtained    = 0x067A
local itemsObtainedHigh     = 0x067B

itemAPids = {
    ["Boomerang"] = 7100,
    ["Bow"] = 7101,
    ["Magical Boomerang"] = 7102,
    ["Raft"] = 7103,
    ["Stepladder"] = 7104,
    ["Recorder"] = 7105,
    ["Magical Rod"] = 7106,
    ["Red Candle"] = 7107,
    ["Book of Magic"] = 7108,
    ["Magical Key"] = 7109,
    ["Red Ring"] = 7110,
    ["Silver Arrow"] = 7111,
    ["Sword"] = 7112,
    ["White Sword"] = 7113,
    ["Magical Sword"] = 7114,
    ["Heart Container"] = 7115,
    ["Letter"] = 7116,
    ["Magical Shield"] = 7117,
    ["Candle"] = 7118,
    ["Arrow"] = 7119,
    ["Food"] = 7120,
    ["Water of Life (Blue)"] = 7121,
    ["Water of Life (Red)"] = 7122,
    ["Blue Ring"] = 7123,
    ["Triforce Fragment"] = 7124,
    ["Power Bracelet"] = 7125,
    ["Small Key"] = 7126,
    ["Bomb"] = 7127,
    ["Recovery Heart"] = 7128,
    ["Five Rupees"] = 7129,
    ["Rupee"] = 7130,
    ["Clock"] = 7131,
    ["Fairy"] = 7132
}

itemCodes = {
    ["Boomerang"] = 0x1D,
    ["Bow"] = 0x0A,
    ["Magical Boomerang"] = 0x1E,
    ["Raft"] = 0x0C,
    ["Stepladder"] = 0x0D,
    ["Recorder"] = 0x05,
    ["Magical Rod"] = 0x10,
    ["Red Candle"] = 0x07,
    ["Book of Magic"] = 0x11,
    ["Magical Key"] = 0x0B,
    ["Red Ring"] = 0x13,
    ["Silver Arrow"] = 0x09,
    ["Sword"] = 0x01,
    ["White Sword"] = 0x02,
    ["Magical Sword"] = 0x03,
    ["Heart Container"] = 0x1A,
    ["Letter"] = 0x15,
    ["Magical Shield"] = 0x1C,
    ["Candle"] = 0x06,
    ["Arrow"] = 0x08,
    ["Food"] = 0x04,
    ["Water of Life (Blue)"] = 0x1F,
    ["Water of Life (Red)"] = 0x20,
    ["Blue Ring"] = 0x12,
    ["Triforce Fragment"] = 0x1B,
    ["Power Bracelet"] = 0x14,
    ["Small Key"] = 0x19,
    ["Bomb"] = 0x00,
    ["Recovery Heart"] = 0x22,
    ["Five Rupees"] = 0x0F,
    ["Rupee"] = 0x18,
    ["Clock"] = 0x21,
    ["Fairy"] = 0x23
}


--Sets correct memory access functions based on whether NesHawk or QuickNES is loaded
local function defineMemoryFunctions()
	local memDomain = {}
	local domains = memory.getmemorydomainlist()
	if domains[1] == "System Bus" then
		--NesHawk
		isNesHawk = true
		memDomain["systembus"] = function() memory.usememorydomain("System Bus") end
        memDomain["ram"]       = function() memory.usememorydomain("RAM") end
		memDomain["saveram"]   = function() memory.usememorydomain("Battery RAM") end
		memDomain["rom"]       = function() memory.usememorydomain("PRG ROM") end
	elseif domains[1] == "WRAM" then
		--QuickNES
		memDomain["systembus"] = function() memory.usememorydomain("System Bus") end
        memDomain["ram"]       = function() memory.usememorydomain("RAM") end
		memDomain["saveram"]   = function() memory.usememorydomain("WRAM") end
		memDomain["rom"]       = function() memory.usememorydomain("PRG ROM") end
	end
	return memDomain
end

local memDomain = defineMemoryFunctions()
u8 = memory.read_u8
wU8 = memory.write_u8
uRange = memory.readbyterange

itemIDNames = {}

for key, value in pairs(itemAPids) do
    itemIDNames[value] = key
end

local function getItemsObtained()
    return bit.bor(bit.lshift(u8(itemsObtainedHigh), 8), u8(itemsObtained))
end

local function setItemsObtained(value)
    wU8(itemsObtainedHigh, bit.rshift(value, 8))
    wU8(itemsObtained, bit.band(value, 0xFF))
end

local function determineItem(array)
    memdomain.ram()
    currentItemsObtained = getItemsObtained()
    
end

local function gotSword()
    local currentSword = u8(sword)
    wU8(sword, math.max(currentSword, 1))
end

local function gotWhiteSword()
    local currentSword = u8(sword)
    wU8(sword, math.max(currentSword, 2))
end

local function gotMagicalSword()
    wU8(sword, 3)
end

local function gotBomb()
    local currentBombs = u8(bombs)
    local currentMaxBombs = u8(maxBombs)
    wU8(bombs, math.min(currentBombs + 4, currentMaxBombs))
    wU8(0x505, 0x29) -- Fake bomb to show item get.
end

local function gotArrow()
    local currentArrow = u8(arrow)
    wU8(arrow, math.max(currentArrow, 1))
end

local function gotSilverArrow()
    wU8(arrow, 2)
end

local function gotBow()
    wU8(bow, 1)
end

local function gotCandle()
    local currentCandle = u8(candle)
    wU8(candle, math.max(currentCandle, 1))
end

local function gotRedCandle()
    wU8(candle, 2)
end

local function gotRecorder()
    wU8(recorder, 1)
end

local function gotFood()
    wU8(food, 1)
end

local function gotWaterOfLifeBlue()
    local currentWaterOfLife = u8(waterOfLife)
    wU8(waterOfLife, math.max(currentWaterOfLife, 1))
end

local function gotWaterOfLifeRed()
    wU8(waterOfLife, 2)
end

local function gotMagicalRod()
    wU8(magicalRod, 1)
end

local function gotBookOfMagic()
    wU8(bookOfMagic, 1)
end

local function gotRaft()
    wU8(raft, 1)
end

local function gotBlueRing()
    local currentRing = u8(ring)
    wU8(ring, math.max(currentRing, 1))
    memDomain.saveram()
    local currentTunicColor = u8(0x0B92)
    if currentTunicColor == 0x29 then 
        wU8(0x0B92, 0x32)
        wU8(0x0804, 0x32)
    end
end

local function gotRedRing()
    wU8(ring, 2)
    memDomain.saveram()
    wU8(0x0B92, 0x16)
    wU8(0x0804, 0x16)
end

local function gotStepladder()
    wU8(stepladder, 1)
end

local function gotMagicalKey()
    wU8(magicalKey, 1)
end

local function gotPowerBracelet()
    wU8(powerBracelet, 1)
end

local function gotLetter()
    wU8(letter, 1)
end

local function gotHeartContainer()
    local currentHeartContainers = bit.rshift(bit.band(u8(heartContainers), 0xF0), 4)
    if currentHeartContainers < 16 then
        currentHeartContainers = math.min(currentHeartContainers + 1, 16)
        local currentHearts = bit.band(u8(heartContainers), 0x0F) + 1
        wU8(heartContainers, bit.lshift(currentHeartContainers, 4) + currentHearts)
    end
end

local function gotTriforceFragment()
    local triforceByte = 0xFF
    local newTriforceCount = u8(localTriforce) + 1
    wU8(localTriforce, newTriforceCount)
end

local function gotBoomerang()
    wU8(boomerang, 1)
end

local function gotMagicalBoomerang()
    wU8(magicalBoomerang, 1)
end

local function gotMagicalShield()
    wU8(magicalShield, 1)
end

local function gotRecoveryHeart()
    local currentHearts = bit.band(u8(heartContainers), 0x0F)
    local currentHeartContainers = bit.rshift(bit.band(u8(heartContainers), 0xF0), 4)
    if currentHearts < currentHeartContainers then 
        currentHearts = currentHearts + 1 
    else
        wU8(partialHearts, 0xFF)
    end
    currentHearts = bit.bor(bit.band(u8(heartContainers), 0xF0), currentHearts)
    wU8(heartContainers, currentHearts)
end

local function gotFairy()
    local currentHearts = bit.band(u8(heartContainers), 0x0F)
    local currentHeartContainers = bit.rshift(bit.band(u8(heartContainers), 0xF0), 4)
    if currentHearts < currentHeartContainers then 
        currentHearts = currentHearts + 3
        if currentHearts > currentHeartContainers then
            currentHearts = currentHeartContainers
            wU8(partialHearts, 0xFF)
        end
    else
        wU8(partialHearts, 0xFF)
    end
    currentHearts = bit.bor(bit.band(u8(heartContainers), 0xF0), currentHearts)
    wU8(heartContainers, currentHearts)
end

local function gotClock()
    wU8(clockItem, 1)
end

local function gotFiveRupees()
    local currentRupeesToAdd = u8(rupeesToAdd)
    wU8(rupeesToAdd, math.min(currentRupeesToAdd + 5, 255))
end

local function gotSmallKey()
    wU8(keys, math.min(u8(keys) + 1, 9))
end

local function gotItem(item)
    --Write itemCode to itemToLift
    --Write 128 to itemLiftTimer
    --Write 4 to sound effect queue
    itemName = itemIDNames[item]
    itemCode = itemCodes[itemName]
    wU8(0x505, itemCode)
    wU8(0x506, 128)
    wU8(0x602, 4)
    numberObtained = getItemsObtained() + 1
    setItemsObtained(numberObtained)
    if itemName == "Boomerang" then gotBoomerang() end
    if itemName == "Bow" then gotBow() end
    if itemName == "Magical Boomerang" then gotMagicalBoomerang() end
    if itemName == "Raft" then gotRaft() end
    if itemName == "Stepladder" then gotStepladder() end
    if itemName == "Recorder" then gotRecorder() end
    if itemName == "Magical Rod" then gotMagicalRod() end
    if itemName == "Red Candle" then gotRedCandle() end
    if itemName == "Book of Magic" then gotBookOfMagic() end
    if itemName == "Magical Key" then gotMagicalKey() end
    if itemName == "Red Ring" then gotRedRing() end
    if itemName == "Silver Arrow" then gotSilverArrow() end
    if itemName == "Sword" then gotSword() end
    if itemName == "White Sword" then gotWhiteSword() end
    if itemName == "Magical Sword" then gotMagicalSword() end
    if itemName == "Heart Container" then gotHeartContainer() end
    if itemName == "Letter" then gotLetter() end
    if itemName == "Magical Shield" then gotMagicalShield() end
    if itemName == "Candle" then gotCandle() end
    if itemName == "Arrow" then gotArrow() end
    if itemName == "Food" then gotFood() end
    if itemName == "Water of Life (Blue)" then gotWaterOfLifeBlue() end
    if itemName == "Water of Life (Red)" then gotWaterOfLifeRed() end
    if itemName == "Blue Ring" then gotBlueRing() end
    if itemName == "Triforce Fragment" then gotTriforceFragment() end
    if itemName == "Power Bracelet" then gotPowerBracelet() end
    if itemName == "Small Key" then gotSmallKey() end
    if itemName == "Bomb" then gotBomb() end
    if itemName == "Recovery Heart" then gotRecoveryHeart() end
    if itemName == "Five Rupees" then gotFiveRupees() end
    if itemName == "Fairy" then gotFairy() end
    if itemName == "Clock" then gotClock() end
end


local function StateOKForMainLoop()
    memDomain.ram()
    local gameMode = u8(0x12) 
    return gameMode == 5 
end

local function checkCaveItemObtained()
    memDomain.ram() 
    local returnTable = {}
    returnTable["slot1"] = u8(shopSlotLeft)
    returnTable["slot2"] = u8(shopSlotMiddle)
    returnTable["slot3"] = u8(shopSlotRight)
    returnTable["takeAnys"] = u8(takeAnyCavesChecked)
    return returnTable
end

function generateOverworldLocationChecked()
    memDomain.ram()
    data = uRange(0x067E, 0x81)
    data[0] = nil
    return data
end

function getHCLocation()
    memDomain.rom()
    data = u8(0x1789A)
    return data
end

function getPBLocation()
    memDomain.rom()
    data = u8(0x10CB2)
    return data
end

function generateUnderworld16LocationChecked()
    memDomain.ram()
    data = uRange(0x06FE, 0x81)
    data[0] = nil
    return data
end

function generateUnderworld79LocationChecked()
    memDomain.ram()
    data = uRange(0x077E, 0x81)
    data[0] = nil
    return data
end

function updateTriforceFragments()
    memDomain.ram()
    local triforceByte = 0xFF
    totalTriforceCount = u8(localTriforce)
    local currentPieces = bit.rshift(triforceByte, 8 - math.min(8, totalTriforceCount))
    wU8(triforceFragments, currentPieces)
end

function processBlock(block)
    if block ~= nil then
        local msgBlock = block['messages']
        if msgBlock ~= nil then
            for i, v in pairs(msgBlock) do
                if itemMessages[i] == nil then
                    local msg = {TTL=450, message=v, color=0xFFFF0000}
                    itemMessages[i] = msg
                end
            end
        end
        local bonusItems = block["bonusItems"]
        if bonusItems ~= nil and isInGame then
            for i, item in ipairs(bonusItems) do
                memDomain.ram()
                if i > u8(bonusItemsObtained) then
                    if u8(0x505) == 0 then
                        gotItem(item)
                        setItemsObtained(getItemsObtained() - 1)
                        wU8(bonusItemsObtained, u8(bonusItemsObtained) + 1)
                    end
                end
            end
        end
        local itemsBlock = block["items"]
        memDomain.saveram()
        isInGame = StateOKForMainLoop()
        updateTriforceFragments()
        if itemsBlock ~= nil and isInGame then
            memDomain.ram()
            --get item from item code
            --get function from item
            --do function
            for i, item in ipairs(itemsBlock) do
                memDomain.ram()
                if u8(0x505) == 0 then
                    if i > getItemsObtained() then
                        gotItem(item)
                    end
                end
            end
        end
        local shopsBlock = block["shops"]
        if shopsBlock ~= nil then
            wU8(shopSlotLeft, bit.bor(u8(shopSlotLeft), shopsBlock["left"]))
            wU8(shopSlotMiddle, bit.bor(u8(shopSlotMiddle), shopsBlock["middle"]))
            wU8(shopSlotRight, bit.bor(u8(shopSlotRight), shopsBlock["right"]))
        end
    end
end

function receive()
    l, e = zeldaSocket:receive()
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
    local playerName = uRange(0x1F, 0x11)
    playerName[0] = nil
    local retTable = {}
    retTable["playerName"] = playerName
    if StateOKForMainLoop() then
        retTable["overworld"] = generateOverworldLocationChecked()
        retTable["underworld1"] = generateUnderworld16LocationChecked()
        retTable["underworld2"] = generateUnderworld79LocationChecked()
    end
    retTable["caves"] = checkCaveItemObtained()
    memDomain.ram()
    if gameMode ~= 19 then
        gameMode = u8(0x12)
    end
    retTable["gameMode"] = gameMode
    retTable["overworldHC"] = getHCLocation()
    retTable["overworldPB"] = getPBLocation()
    retTable["itemsObtained"] = getItemsObtained()
    msg = json.encode(retTable).."\n"
    local ret, error = zeldaSocket:send(msg)
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
                drawText(5, 32, "Please start Zelda1Client.exe", 0xFFFF0000)

                -- Advance so the messages are drawn
                emu.frameadvance()
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
