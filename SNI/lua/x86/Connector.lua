-- original file found in a GPLv3 code repository, unclear if this is the intended license nor who the authors are
-- SNI modifications by Berserker, jsd1982; modifications licensed under MIT License
-- version 3 changes Read response from JSON to HEX

if not event then
    is_snes9x = true
    memory.usememorydomain = function()
        -- snes9x always uses "System Bus" domain, which cannot be switched
    end
    memory.read_u8 = memory.readbyte
    memory.read_s8 = memory.readbytesigned
    memory.read_u16_le = memory.readword
    memory.read_s16_le = memory.readwordsigned
    memory.read_u32_le = memory.readdword
    memory.read_s32_le = memory.readdwordsigned
    memory.read_u16_be = function(addr) return bit.rshift(bit.bswap(memory.read_u16_le(addr)),16) end
else
    if emu.getsystemid() ~= "SNES" then
        print("Connector only for BSNES Core within Bizhawk, sorry.")
    end
end


function readbyterange(addr, length, domain)
    local mtable;
    local mstart = 0;
    local mend = length - 1;
    if is_snes9x then
        mtable = memory.readbyterange(addr, length);
        mstart = 1
        mend = length
    else
        -- jsd: wrap around address by domain size:
        local domainsize = memory.getmemorydomainsize(domain)
        while addr >= domainsize do
            addr = addr - domainsize
        end
        mtable = memory.readbyterange(addr, length, domain)
        mstart = 0;
        mend = length - 1;
    end

    -- jsd: format output in 2-char hex per byte:
    local toret = {};
    for i=mstart, mend do
        table.insert(toret, string.format("%02x", mtable[i]))
    end
    return toret
end
function writebyte(addr, value, domain)
  if is_snes9x then
    memory.writebyte(addr, value)
  else
    -- jsd: wrap around address by domain size:
    local domainsize = memory.getmemorydomainsize(domain)
    while addr >= domainsize do
        addr = addr - domainsize
    end
    memory.writebyte(addr, value, domain)
  end
end

local socket = require("socket.core")

local connection
local host = '127.0.0.1'
local port = 65398
local connected = false
local stopped = false
local name = "Unnamed"

memory.usememorydomain("System Bus")

local function onMessage(s)
    local parts = {}
    for part in string.gmatch(s, '([^|]+)') do
        parts[#parts + 1] = part
    end
    if parts[1] == "Read" then
        local adr = tonumber(parts[2])
        local length = tonumber(parts[3])
        local domain
        if is_snes9x ~= true then
          domain = parts[4]
        end
        local byteRange = readbyterange(adr, length, domain)
        connection:send(table.concat(byteRange) .. "\n")
    elseif parts[1] == "Write" then
        local adr = tonumber(parts[2])
        local domain
        local offset = 2
        if is_snes9x ~= true then
          domain = parts[3]
          offset = 3
        end
        for k, v in pairs(parts) do
            if k > offset then
                writebyte(adr + k - offset - 1, tonumber(v), domain)
            end
        end
    elseif parts[1] == "SetName" then
        name = parts[2]
        print("My name is " .. name .. "!")
    elseif parts[1] == "Message" then
        print(parts[2])
    elseif parts[1] == "Exit" then
        print("Lua script stopped, to restart the script press \"Restart\"")
        stopped = true
    elseif parts[1] == "Version" then
        if is_snes9x then
            connection:send("Version|SNI Connector|3|Snes9x\n")
        else
            connection:send("Version|SNI Connector|3|Bizhawk\n")
        end
    elseif is_snes9x ~= true then
        if parts[1] == "Reset" then
            print("Rebooting core...")
            client.reboot_core()
        elseif parts[1] == "Pause" then
            print("Pausing...")
            client.pause()
        elseif parts[1] == "Unpause" then
            print("Unpausing...")
            client.unpause()
        elseif parts[1] == "PauseToggle" then
            print("Toggling pause...")
            client.togglepause()
        end
    end
end


local main = function()
    if stopped then
        return nil
    end

    if not connected then
        print('Connecting to SNI at ' .. host .. ':' .. port)
        connection, err = socket:tcp()
        if err ~= nil then
            emu.print(err)
            return
        end

        local returnCode, errorMessage = connection:connect(host, port)
        if (returnCode == nil) then
            print("Error while connecting: " .. errorMessage)
            stopped = true
            connected = false
            print("Please press \"Restart\" to try to reconnect to SNI, make sure it's running.")
            return
        end

        connection:settimeout(0)
        connected = true
        print('Connected to SNI')
        return
    end
    local s, status = connection:receive('*l')
    if s then
        onMessage(s)
    end
    if status == 'closed' then
        print('Connection to SNI is closed')
        connection:close()
        connected = false
        return
    end
end

if is_snes9x then
    emu.registerbefore(main)
else
    while true do
        main()
        emu.frameadvance()
    end
end
