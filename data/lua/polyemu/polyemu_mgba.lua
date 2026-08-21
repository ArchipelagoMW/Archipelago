local DEBUG = false

local POLYEMU_DEVICE_PORT = 43031
local polyemu_socket = nil

local device_id = nil

local locked = false
local platform = nil
local memory_domains = nil

local message_buffer = console:createBuffer("Archipelago Connector")

local REQUEST_TYPES = {
    ["NO_OP"] = string.char(0x00),
    ["SUPPORTED_OPERATIONS"] = string.char(0x01),
    ["PLATFORM"] = string.char(0x02),
    ["MEMORY_SIZE"] = string.char(0x03),
    ["LIST_DEVICES"] = string.char(0x04),
    ["READ"] = string.char(0x10),
    ["WRITE"] = string.char(0x11),
    ["GUARD"] = string.char(0x12),
    ["LOCK"] = string.char(0x20),
    ["UNLOCK"] = string.char(0x21),
    ["DISPLAY_MESSAGE"] = string.char(0x22),
}

local RESPONSE_TYPES = {
    ["NO_OP"] = string.char(0x80),
    ["SUPPORTED_OPERATIONS"] = string.char(0x81),
    ["PLATFORM"] = string.char(0x82),
    ["MEMORY_SIZE"] = string.char(0x84),
    ["LIST_DEVICES"] = string.char(0x84),
    ["READ"] = string.char(0x90),
    ["WRITE"] = string.char(0x91),
    ["GUARD"] = string.char(0x92),
    ["LOCK"] = string.char(0xA0),
    ["UNLOCK"] = string.char(0xA1),
    ["DISPLAY_MESSAGE"] = string.char(0xA2),
    ["ERROR"] = string.char(0xFF),
}

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
    [REQUEST_TYPES["NO_OP"]] = function (msg, dry)
        if dry then
            return "", msg
        end

        return RESPONSE_TYPES["NO_OP"], msg
    end,

    [REQUEST_TYPES["SUPPORTED_OPERATIONS"]] = function (msg, dry)
        if dry then
            return "", msg
        end

        local response = ""
        for _, request_type in REQUEST_TYPES do
            response = response .. request_type
        end

        return RESPONSE_TYPES["SUPPORTED_OPERATIONS"] .. string.char(#response) .. response, msg
    end,

    [REQUEST_TYPES["PLATFORM"]] = function (msg, dry)
        local response

        if dry then
            return "", msg
        end

        if platform == C.PLATFORM.GB then
            if emu.memory.cart0:read8(0x143) == 0xC0 then
                response = 0x02
            else
                response = 0x01
            end
        else
            response = 0x03
        end

        return RESPONSE_TYPES["PLATFORM"] .. string.char(response), msg
    end,

    [REQUEST_TYPES["MEMORY_SIZE"]] = function (msg, dry)
        if dry then
            return "", msg
        end

        local response = RESPONSE_TYPES["MEMORY_SIZE"]
        for id, domain in pairs(memory_domains) do
            if id ~= 0 then
                response = response .. string.char(id) .. int_to_bytes(domain:bound() - domain:base(), 8)
            end
        end
        return response, msg
    end,

    [REQUEST_TYPES["LIST_DEVICES"]] = function (msg, dry)
        if dry then
            return "", msg
        end

        return RESPONSE_TYPES["LIST_DEVICES"] .. string.char(1) .. device_id, msg
    end,

    [REQUEST_TYPES["READ"]] = function (msg, dry)
        local domain, address, size, data
        domain, msg = consume_int(msg, 1)
        address, msg = consume_int(msg, 8)
        size, msg = consume_int(msg, 2)

        if dry then
            return "", msg
        end

        data = memory_domains[domain]:readRange(address, size)
        return RESPONSE_TYPES["READ"] .. int_to_bytes(size, 2) .. data, msg
    end,

    [REQUEST_TYPES["WRITE"]] = function (msg, dry)
        local domain, address, size, data
        domain, msg = consume_int(msg, 1)
        address, msg = consume_int(msg, 8)
        size, msg = consume_int(msg, 2)
        data, msg = consume_str(msg, size)

        if dry then
            return "", msg
        end

        for i = 1, #data do
            memory_domains[domain]:write8(address + (i - 1), data:byte(i))
        end

        return RESPONSE_TYPES["WRITE"], msg
    end,

    [REQUEST_TYPES["GUARD"]] = function (msg, dry)
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

        return RESPONSE_TYPES["GUARD"] .. string.char(data_is_validated), msg
    end,

    [REQUEST_TYPES["LOCK"]] = function (msg, dry)
        if dry then
            return "", msg
        end

        locked = true
        return RESPONSE_TYPES["LOCK"], msg
    end,

    [REQUEST_TYPES["UNLOCK"]] = function (msg, dry)
        if dry then
            return "", msg
        end

        locked = false
        return RESPONSE_TYPES["UNLOCK"], msg
    end,

    [REQUEST_TYPES["DISPLAY_MESSAGE"]] = function (msg, dry)
        local message_size, message
        message_size, msg = consume_int(msg, 1)
        message, msg = consume_str(msg, message_size)

        if dry then
            return "", msg
        end

        message_buffer:log(message)
        return RESPONSE_TYPES["DISPLAY_MESSAGE"], msg
    end,

    ["default"] = function (msg, dry)
        if dry then
            return "", ""
        end

        return RESPONSE_TYPES["ERROR"] .. string.char(0x01) .. int_to_bytes(0, 2), ""
    end,
}

local function handle_requests()
    local size, msg, err
    if not polyemu_socket then return end

    size, err = polyemu_socket:receive(2)
    if not size then
        if err ~= socket.ERRORS.AGAIN then
            polyemu_socket:close()
            polyemu_socket = nil
            return
        end
    end

    msg, err = polyemu_socket:receive(bytes_to_int(size, 1, 2))
    if not msg then
        if err ~= socket.ERRORS.AGAIN then
            polyemu_socket:close()
            polyemu_socket = nil
            return
        end
    end

    if DEBUG then
        console:log("Message Received: " .. bytes_to_hex_str(msg))
    end

    local header, requests = consume_str(msg, 8)
    local response_buffer = ""

    if header:sub(1, 8) ~= device_id and header:sub(1, 8) ~= int_to_bytes(0, 8) then
        response_buffer = RESPONSE_TYPES["ERROR"] .. string.char(0x02) .. int_to_bytes(16, 2) .. header:sub(1, 8) .. device_id
    else
        local guard_failure_response = nil

        repeat
            local request_header, response
            request_header, requests = consume_str(requests, 1)
            local request_type = request_header:sub(1, 1)

            if request_handlers[request_type] then
                response, requests = request_handlers[request_type](requests, guard_failure_response ~= nil)
            else
                response, requests = request_handlers["default"](requests, guard_failure_response ~= nil)
            end

            if guard_failure_response ~= nil then
                response = guard_failure_response
            elseif request_type == REQUEST_TYPES["GUARD"] then
                if response:sub(1, 1) == RESPONSE_TYPES["ERR"] then
                    -- Something went wrong with the guard, send the error response and stop processing requests
                    requests = ""
                elseif response:sub(1, 1) == RESPONSE_TYPES["GUARD"] and response:byte(2) == 0 then
                    guard_failure_response = response
                end
            end

            response_buffer = response_buffer..response
        until requests == ""
    end

    polyemu_socket:send(int_to_bytes(#response_buffer, 2) .. response_buffer)
end

local function handle_error()
    console:log("ERROR")
end

local function tick()
    device_id = "00000000" .. emu:checksum(C.CHECKSUM.CRC32)
    device_id = device_id:sub(-8)

    if platform ~= emu:platform() then
        platform = emu:platform()

        if platform == C.PLATFORM.GB then
            memory_domains = {
                [0x00] = emu,
                [0x01] = emu.memory.cart0,
                [0x02] = emu.memory.vram,
                [0x03] = emu.memory.sram,
                [0x04] = emu.memory.wram,
                [0x05] = emu.memory.oam,
                [0x06] = emu.memory.io,
                [0x07] = emu.memory.hram,
            }
        else
            memory_domains = {
                [0x00] = emu,
                [0x01] = emu.memory.bios,
                [0x02] = emu.memory.wram,
                [0x03] = emu.memory.iwram,
                [0x04] = emu.memory.io,
                [0x05] = emu.memory.palette,
                [0x06] = emu.memory.vram,
                [0x07] = emu.memory.oam,
                [0x08] = emu.memory.cart0,
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
        polyemu_socket:add("received", handle_requests)
        polyemu_socket:add("error", handle_error)
    else
        while locked do
            polyemu_socket:poll()
        end
    end
end

callbacks:add("frame", tick)
