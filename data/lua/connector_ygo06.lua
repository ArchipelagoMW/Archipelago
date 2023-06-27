local socket = require("socket")
local json = require('json')
local math = require('math')

require("common")
local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local SCRIPT_VERSION = 1

local LocationAddress = 0x52e8
local ItemAddress = 0x5307

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
	memDomain["wram"] = function() memory.usememorydomain("EWRAM") end
	return memDomain
end

local memDomain = defineMemoryFunctions()
function readArray(address, bytes)
	data = memory.read_bytes_as_array(address, bytes + 1)
	return data
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

function generateLocationsChecked()
	memDomain.wram()
	locationBytes = readArray(LocationAddress, 0x1F)
	locationBytes[0] = nil

    return locationBytes
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
    local playerName = readArray(0x30, 0x11)
    playerName[0] = nil
    local retTable = {}
    retTable["scriptVersion"] = SCRIPT_VERSION
    retTable["playerName"] = playerName
    memDomain.wram()
    if (u8(0) == 0x59) then
        retTable["locations"] = generateLocationsChecked()
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
    if (is23Or24Or25 or is26To28) == false then
        print("Must use a version of bizhawk 2.3.1 or higher")
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
            if (frame % 15 == 0) then
                receive()
                if (ItemsReceived ~= nil and u8(0) == 0x59) then
                    memDomain.wram()
                    for i, item in ipairs(ItemsReceived) do
                        if (item ~=nil) then
                            local current_item = u8(ItemAddress + i)
                            wU8(ItemAddress + i, bit.bor(current_item, item))
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
