socket = require("socket")
local json = require('json')

MAX_MESSAGE_LEN = 40
item_messages = {};
past_locations = nil
items_received = {};
frame = 0;

local u8 = nil
local w_u8 = nil


--Sets correct memory access functions based on whether NesHawk or QuickNES is loaded
local function defineMemoryFunctions()
	local mem_domain = {}
	local domains = memory.getmemorydomainlist();
	if domains[1] == "System Bus" then
		--NesHawk
		mem_domain["systembus"] = function() memory.usememorydomain("System Bus") end
		mem_domain["saveram"]   = function() memory.usememorydomain("Battery RAM") end
		mem_domain["rom"]       = function() memory.usememorydomain("PRG ROM") end
	elseif domains[1] == "WRAM" then
		--QuickNES
		mem_domain["systembus"] = function() memory.usememorydomain("System Bus") end
		mem_domain["saveram"]   = function() memory.usememorydomain("WRAM") end
		mem_domain["rom"]       = function() memory.usememorydomain("PRG ROM") end
	end
	return mem_domain
end

local mem_domain = defineMemoryFunctions()
u8 = memory.read_u8;
w_u8 = memory.write_u8;
u_range = memory.readbyterange;
mem_domain["rom"]()
mem_domain["systembus"]()


local function StateOKForMainLoop()
  local A = u8(0x6102) -- Party Made
  local B = u8(0x60FC) -- Not in Battle
  local C = u8(0x60A3)
  return A ~= 0x00 and B ~= 0x0B and B ~= 0x0C and not (A== 0xF2 and B == 0xF2 and C == 0xF2)
end

function table.empty (self)
    for _, _ in pairs(self) do
        return false
    end
    return true
end

local function drawMessages()
    if table.empty(item_messages) then
        return
    end
    local y = 10;
    for k, v in pairs(item_messages) do
        if v["TTL"] > 0 then
            message = v["message"]
            while true do
                gui.pixelText(5, y, message:sub(1, MAX_MESSAGE_LEN), v["color"], 0xB0000000, 0);
                y = y + 10;
                item_messages[k]["TTL"] = item_messages[k]["TTL"] - 1;
                message = message:sub(MAX_MESSAGE_LEN + 1, message:len())
                if message:len() == 0 then
                    break
                end
            end
        end
    end
end

local prevstate = ""
local curstate =  "Uninitialized"
local statusColor = ""
local ff1_socket = nil;

function generateLocationChecked()
    data = u_range(0x61FF, 0x101)
    data[0] = nil
    return data
end

function processBlock(block)
    local msg_block = block['messages'];
    if msg_block ~= nil then
        for i, v in pairs(msg_block) do
            if item_messages[i] == nil then
                local msg = {TTL=450, message=v, color=0xFFFF0000};
                item_messages[i] = msg;
            end
        end
    end
    local items_block = block["items"]
    if items_block ~= nil then
        for i, v in pairs(items_block) do
            -- Minus the offset and add to the correct domain
            local memory_location = v + 0x6000
            if v > 0x1E0 then
                memory_location = memory_location - 0x1E0
            else
                memory_location = memory_location - 0x0E0
            end
            if items_received[memory_location] == nil then
                items_received[memory_location] = memory_location;
                value = 0x01
                -- Canal is a flipped bit
                if memory_location == 0x600C then
                    value = 0x00
                end
                items_received[memory_location] = value
                w_u8(memory_location, value)
            elseif u8(memory_location) ~= items_received[memory_location] then
                w_u8(memory_location, items_received[memory_location])
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
    l, e = ff1_socket:receive()
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
    local hasWon = u8(0x62FE);
    local msg = "\n"
    if hasWon == 0x03 or hasWon == 0x02 then
        -- VICTORY!
        msg = "TERMINATED_CHAOS\n";
    else
        locations = generateLocationChecked()
        if past_locations == nil or #difference(locations, past_locations) <= 5 then
            msg = json.encode(locations).."\n"
            past_locations = locations
        end
    end
    local ret, error = ff1_socket:send(msg)
    if ret == nil then
        print(error)
    end
end

function receiveKeepAliveOrVictory()
    l, e = ff1_socket:receive()
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
    local ret, error = ff1_socket:send(msg);
    if ret == nil then
        print(error);
    end
end

server = nil

function main()
    server, error = socket.bind('localhost', 43885)

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
                if (frame % 60 == 0) then
                    receiveKeepAliveOrVictory()
                end
            end
        elseif (curstate == "Error") then
            gui.drawEllipse(248, 9, 6, 6, "Black", "Red");
        elseif (curstate == "Uninitialized") then
            gui.drawEllipse(248, 9, 6, 6, "Black", "White");
            if  (frame % 60 == 0) then
                server:settimeout(2)
                print("Attempting to connect")
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Connection established')
                    curstate = "OK"
                    ff1_socket = client
                    ff1_socket:settimeout(0)
                end
            end
        end
        --debug_log(string.format("whole loop executed in %.3f ms", os.clock() - lc))
        emu.frameadvance();
    end
end

main()
