local socket = require("socket")
local json = require('json')
local math = require('math')
require("common")
local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local SCRIPT_VERSION = 3

local APIndex = 0x1A6E
local APDeathLinkAddress = 0x00FD
local APItemAddress = 0x00FF
local EventFlagAddress = 0x1735
local MissableAddress = 0x161A
local HiddenItemsAddress = 0x16DE
local RodAddress = 0x1716
local DexSanityAddress = 0x1A71
local InGameAddress = 0x1A84
local ClientCompatibilityAddress = 0xFF00

local ItemsReceived = nil
local playerName = nil
local seedName = nil

local deathlink_rec = nil
local deathlink_send = false

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local gbSocket = nil
local frame = 0

local compat = nil

local function defineMemoryFunctions()
	local memDomain = {}
	local domains = memory.getmemorydomainlist()
	memDomain["rom"] = function() memory.usememorydomain("ROM") end
	memDomain["wram"] = function() memory.usememorydomain("WRAM") end
	return memDomain
end

local memDomain = defineMemoryFunctions()
u8 = memory.read_u8
wU8 = memory.write_u8
u16 = memory.read_u16_le
function uRange(address, bytes)
	data = memory.readbyterange(address - 1, bytes + 1)
	data[0] = nil
	return data
end

function generateLocationsChecked()
	memDomain.wram()
	events = uRange(EventFlagAddress, 0x140)
	missables = uRange(MissableAddress, 0x20)
	hiddenitems = uRange(HiddenItemsAddress, 0x0E)
	rod = {u8(RodAddress)}
	dexsanity = uRange(DexSanityAddress, 19)
	

	data = {}

    categories = {events, missables, hiddenitems, rod}
    if compat > 1 then
        table.insert(categories, dexsanity)
    end
    for _, category in ipairs(categories) do
        for _, v in ipairs(category) do 
            table.insert(data, v) 
        end
    end

    return data
end

local function arrayEqual(a1, a2)
    if #a1 ~= #a2 then
      return false
    end
  
    for i, v in ipairs(a1) do
      if v ~= a2[i] then
        return false
      end
    end
  
    return true
end

function receive()
    l, e = gbSocket:receive()
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
        block = json.decode(l)
        if block ~= nil then
            local itemsBlock = block["items"]
            if itemsBlock ~= nil then
                ItemsReceived = itemsBlock
            end
            deathlink_rec = block["deathlink"]

        end
    end
    -- Determine Message to send back
    memDomain.rom()
    newPlayerName = uRange(0xFFF0, 0x10)
    newSeedName = uRange(0xFFDB, 21)
    if (playerName ~= nil and not arrayEqual(playerName, newPlayerName)) or (seedName ~= nil and not arrayEqual(seedName, newSeedName)) then
        print("ROM changed, quitting")
        curstate = STATE_UNINITIALIZED
        return
    end
    playerName = newPlayerName
    seedName = newSeedName
    local retTable = {}
    retTable["scriptVersion"] = SCRIPT_VERSION

    if compat == nil then
        compat = u8(ClientCompatibilityAddress)
        if compat < 2 then
            InGameAddress = 0x1A71
        end
    end

    retTable["clientCompatibilityVersion"] = compat
    retTable["playerName"] = playerName
    retTable["seedName"] = seedName
    memDomain.wram()

    in_game = u8(InGameAddress)
    if in_game == 0x2A or in_game == 0xAC then
        retTable["locations"] = generateLocationsChecked()
    elseif in_game ~= 0 then
        print("Game may have crashed")
        curstate = STATE_UNINITIALIZED
        return
    end

    retTable["deathLink"] = deathlink_send
    deathlink_send = false

    msg = json.encode(retTable).."\n"
    local ret, error = gbSocket:send(msg)
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
    if not checkBizHawkVersion() then
        return
    end
    server, error = socket.bind('localhost', 17242)

    while true do
        frame = frame + 1
        if not (curstate == prevstate) then
            print("Current state: "..curstate)
            prevstate = curstate
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 5 == 0) then
                receive()
                in_game = u8(InGameAddress)
                if in_game == 0x2A or in_game == 0xAC then
                    if u8(APItemAddress) == 0x00 then
                        ItemIndex = u16(APIndex)
                        if deathlink_rec == true then
                            wU8(APDeathLinkAddress, 1)
                        elseif u8(APDeathLinkAddress) == 3 then
                            wU8(APDeathLinkAddress, 0)
                            deathlink_send = true
                        end
                        if ItemsReceived[ItemIndex + 1] ~= nil then
                            item_id = ItemsReceived[ItemIndex + 1] - 172000000
                            if item_id > 255 then
                                item_id = item_id - 256
                            end
                            wU8(APItemAddress, item_id)
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
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    gbSocket = client
                    gbSocket:settimeout(0)
                end
            end
        end
        emu.frameadvance()
    end
end

main()
