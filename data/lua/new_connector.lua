local POLYEMU_DEVICE_PORT = 43031
local polyemu_socket = nil

local platform = nil
local memory_domains = nil

local message_buffer = console:createBuffer("Archipelago Connector")

local function bytes_to_hex_str(str)
    return (str:gsub(".", function(c) return string.format("%02X ", string.byte(c)) end)):sub(1, -2)
end

local function bytes_to_int(str, start_index, length)
    local value = 0
    for i = 0, length - 1 do
        value = value * 256 + str:byte(start_index + i)
    end
    return value
end

local function int_to_bytes(num, length)
    local str = ""
    for i = length - 1, 0, -1 do
        str = str .. string.char((num >> (i * 8)) & 0xFF)
    end
    return str
end

local function consume_str(data, size)
    return data:sub(1, size), data:sub(size + 1)
end

local function consume_int(data, size)
    local n, remaining = consume_str(data, size)
    return bytes_to_int(n, 1, size), remaining
end

local request_handlers = {
    [0x00] = function (msg, dry)
        if dry then
            return "", msg
        end

        return string.char(0x80), msg
    end,
    [0x01] = function (msg, dry)
        local domain, address, size, data
        domain, msg = consume_int(msg, 1)
        address, msg = consume_int(msg, 8)
        size, msg = consume_int(msg, 2)

        if dry then
            return "", msg
        end

        data = memory_domains[domain]:readRange(address, size)

        return string.char(0x81) .. data, msg
    end,
    [0x02] = function (msg, dry)
        local domain, address, size, data
        domain, msg = consume_int(msg, 1)
        address, msg = consume_int(msg, 8)
        size, msg = consume_int(msg, 2)
        data, msg = consume_str(msg, size)

        if dry then
            return "", msg
        end

        for i, byte in ipairs(data) do
            memory_domains[domain]:write8(address + (i - 1), byte:byte())
        end

        return string.char(0x82), msg
    end,
    [0x03] = function (msg, dry)
        local domain, address, size, expected_data, actual_data
        domain, msg = consume_int(msg, 1)
        address, msg = consume_int(msg, 8)
        size, msg = consume_int(msg, 2)
        expected_data, msg = consume_str(msg, size)

        if dry then
            return "", msg
        end

        actual_data = memory_domains[domain]:readRange(address, size)

        local data_is_validated = 1
        if expected_data ~= actual_data then
            data_is_validated = 0
        end

        return string.char(0x83) .. string.char(data_is_validated), msg
    end,
}

local function received()
    local size, msg, err
    if not polyemu_socket then return end

    size, err = polyemu_socket:receive(2)
    if not size then
        if err ~= socket.ERRORS.AGAIN then
            polyemu_socket:close()
            polyemu_socket = nil
        end
    end


    msg, err = polyemu_socket:receive(bytes_to_int(size, 1, 2))
    if not msg then
        if err ~= socket.ERRORS.AGAIN then
            polyemu_socket:close()
            polyemu_socket = nil
        end
    end

    console:log("Message Received: " .. bytes_to_hex_str(msg))

    local header, requests = consume_str(msg, 1)
    local response_buffer = ""
    local guard_failure_response = nil

    repeat
        local request_header, response
        request_header, requests = consume_str(requests, 1)
        response, requests = request_handlers[request_header:byte(1)](requests, guard_failure_response ~= nil)

        if guard_failure_response ~= nil then
            response = guard_failure_response
        elseif request_header:byte(1) == 0x03 then
            if response:byte(2) == 0 then
                guard_failure_response = response
            end
        end

        response_buffer = response_buffer..response
    until requests == ""

    polyemu_socket:send(int_to_bytes(#response_buffer, 2) .. response_buffer)
end

local function handle_error()
    console:log("ERROR")
end

local function tick()
    if platform ~= emu:platform() then
        platform = emu:platform()

        if platform == C.PLATFORM.GB then
            -- memory_domains = {
            --     ["ROM"] = emu.memory.cart0,
            --     ["VRAM"] = emu.memory.vram,
            --     ["SRAM"] = emu.memory.sram,
            --     ["WRAM"] = emu.memory.wram,
            --     ["OAM"] = emu.memory.oam,
            --     ["IO"] = emu.memory.io,
            --     ["HRAM"] = emu.memory.hram,
            --     ["System Bus"] = emu
            -- }
        else
            memory_domains = {
                [0x00] = emu,
                [0x01] = emu.memory.bios,
                [0x02] = emu.memory.iwram,
                [0x03] = emu.memory.wram,
                [0x04] = emu.memory.cart0,
                [0x05] = emu.memory.vram,
                [0x06] = emu.memory.oam,
                [0x07] = emu.memory.cart0,
                [0x08] = emu.memory.cart0,
                -- ["Combined WRAM"] = emu.memory.wram,
            }
        end
    end

    if polyemu_socket == nil then
        polyemu_socket = socket:tcp()
        local result, err = polyemu_socket:connect("127.0.0.1", POLYEMU_DEVICE_PORT)
        if result == nil or err then
            console:log("Failed to connect: " .. tostring(err))
            polyemu_socket = nil
            return
        end
        console:log("Connected to broker")
        polyemu_socket:add("received", received)
        polyemu_socket:add("error", handle_error)
    end
end

callbacks:add("frame", tick)
