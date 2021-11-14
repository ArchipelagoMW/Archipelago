local socket = require("socket")
local json = require('json')

itemMessages = {}
pastLocations = nil
itemsReceived = {}
frame = 0

local u8 = nil
local wU8 = nil
local isNesHawk = false

--Sets correct memory access functions based on whether NesHawk or QuickNES is loaded
local function defineMemoryFunctions()
	local memDomain = {}
	local domains = memory.getmemorydomainlist()
	if domains[1] == "System Bus" then
		--NesHawk
		isNesHawk = true;
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
    local B = u8(0x0FC) -- Not in Battle
    local C = u8(0x0A3)
    return A ~= 0x00 and B ~= 0x0B and B ~= 0x0C and not (A== 0xF2 and B == 0xF2 and C == 0xF2)
end

function table.empty (self)
    for _, _ in pairs(self) do
        return false
    end
    return true
end
local bizhawk_version = client.getversion()
local is23Or24 = (bizhawk_version=="2.3.0") or (bizhawk_version=="2.3.1") or (bizhawk_version:sub(1,3)=="2.4")
local is25To27 = (bizhawk_version:sub(1,3)=="2.5") or (bizhawk_version:sub(1,3)=="2.6") or (bizhawk_version:sub(1,3)=="2.7")

local function getMaxMessageLength()
    if is23Or24 then
        return client.screenwidth()/11
    elseif is25To27 then
        return client.screenwidth()/12
    end
end

local function drawText(x, y, message, color)
    if is23Or24 then
        gui.addmessage(message)
    elseif is25To27 then
        gui.drawText(x, y, message, color, 0xB0000000, 18, "Courier New", nil, nil, nil, "client");
    end
end

local function clearScreen()
    if is23Or24 then
        return
    elseif is25To27 then
        drawText(0, 0, "", "black")
    end
end

local function drawMessages()
    if table.empty(itemMessages) then
        clearScreen()
        return
    end
    local y = 10;
    found = false
    maxMessageLength = getMaxMessageLength()
    for k, v in pairs(itemMessages) do
        if v["TTL"] > 0 then
            message = v["message"]
            while true do
                drawText(5, y, message:sub(1, maxMessageLength), v["color"])
                y = y + 16;

                message = message:sub(maxMessageLength + 1, message:len())
                if message:len() == 0 then
                    break
                end
            end
            newTTL = 0
            if is25To27 then
                newTTL = itemMessages[k]["TTL"] - 1;
            end
            itemMessages[k]["TTL"] = newTTL
            found = true
        end
    end
    if found == false then
        clearScreen()
    end
end


local prevstate = ""
local curstate =  "Uninitialized"
local statusColor = ""
local ff1Socket = nil;

function generateLocationChecked()
    memDomain.saveram()
    data = uRange(0x01FF, 0x101)
    data[0] = nil
    return data
end

function processBlock(block)
    local msg_block = block['messages'];
    if msg_block ~= nil then
        for i, v in pairs(msg_block) do
            if itemMessages[i] == nil then
                local msg = {TTL=450, message=v, color=0xFFFF0000};
                itemMessages[i] = msg;
            end
        end
    end
    local items_block = block["items"]
    if items_block ~= nil then
        for i, v in pairs(items_block) do
            -- Minus the offset and add to the correct domain
            local memory_location = v
            memDomain.saveram();
            if v > 0x1E0 then
                -- This is a regular key item
                memory_location = memory_location - 0x1E0
            else
                -- This is a movement item
                memory_location = memory_location - 0x0E0
            end
            if itemsReceived[memory_location] == nil then
                itemsReceived[memory_location] = memory_location;
                value = 0x01
                -- Canal is a flipped bit
                if memory_location == 0x0C then
                    value = 0x00
                end
                itemsReceived[memory_location] = value
                wU8(memory_location, value)
            elseif u8(memory_location) ~= itemsReceived[memory_location] then
                wU8(memory_location, itemsReceived[memory_location])
            end
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
        print("Connection closed")
        curstate = "Uninitialized"
        return
    elseif e == 'timeout' then
        print("timeout")
        return
    elseif e ~= nil then
        print(e);
        curstate = "Uninitialized";
        return
    end
    processBlock(json.decode(l))
    memDomain.systembus()
    local hasWon = u8(0x62FE);
    local hasWonFlag = bit.band(hasWon, 0x02)
    local msg = "\n"
    locations = generateLocationChecked()
    if hasWonFlag > 0 and #difference(locations, pastLocations) <= 3 then
        -- VICTORY!
        msg = "TERMINATED_CHAOS\n";
        pastLocations = locations
    else
        if pastLocations == nil or #difference(locations, pastLocations) <= 3 then
            msg = json.encode(locations).."\n"
            pastLocations = locations
        end
    end
    local ret, error = ff1Socket:send(msg)
    if ret == nil then
        print(error)
    end
end

function receiveKeepAliveOrVictory()
    l, e = ff1Socket:receive()
    if e == 'closed' then
        print("Connection closed")
        curstate = "Uninitialized"
        return
    elseif e == 'timeout' then
        print("timeout")
        return
    elseif e ~= nil then
        print(e);
        curstate = "Uninitialized";
        return
    end
    processBlock(json.decode(l))
    local msg = '\n'
    local ret, error = ff1Socket:send(msg);
    if ret == nil then
        print(error);
    end
end

server = nil

function close_server()
    if server ~= nil then
        print("CLOSING SERVER")
        server:close()
    end
end

function main()
    if (is23Or24 or is25To27) == false then
        print("Must use a version of bizhawk higher than 2.3.0")
        return
    end
    server, error = socket.bind('localhost', 52980)

    while true do
        gui.drawEllipse(248, 9, 6, 6, "Black", "Yellow");
        frame = frame + 1;
        drawMessages();
        if not (curstate == prevstate) then
            console.log("Current state: "..curstate)
            prevstate = curstate
        end
        if (curstate == "OK") then
            if StateOKForMainLoop() then
                if (frame % 60 == 0) then
                    gui.drawEllipse(248, 9, 6, 6, "Black", "Blue");
                    receive()
                else
                    gui.drawEllipse(248, 9, 6, 6, "Black", "Green");
                end
            else
                gui.drawEllipse(248, 9, 6, 6, "Black", "Green");
                if (frame % 60 == 0) then
                    gui.drawEllipse(248, 9, 6, 6, "Black", "Blue");
                    receiveKeepAliveOrVictory()
                end
            end
        elseif (curstate == "Error") then
            gui.drawEllipse(248, 9, 6, 6, "Black", "Red");
        elseif (curstate == "Uninitialized") then
            gui.drawEllipse(248, 9, 6, 6, "Black", "White");
            if  (frame % 60 == 0) then
                gui.drawEllipse(248, 9, 6, 6, "Black", "Yellow");

                drawText(5, 8, "Waiting for client", 0xFFFF0000);
                drawText(5, 32, "Please start FF1Client.exe", 0xFFFF0000);

                -- Advance so the messages are drawn
                emu.frameadvance()
                server:settimeout(2)
                print("Attempting to connect")
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Connection established')
                    itemMessages["(0,0)"] = {TTL=240, message="Connected", color="green"};
                    curstate = "OK"
                    ff1Socket = client
                    ff1Socket:settimeout(0)
                end
            end
        end
        --debug_log(string.format("whole loop executed in %.3f ms", os.clock() - lc))
        emu.frameadvance();
    end
end

event.unregisterbyname("ff1-socket-onexit")
event.onexit(close_server, "ff1-socket-onexit")
main()
