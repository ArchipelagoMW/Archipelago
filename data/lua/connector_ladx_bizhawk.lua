-- SPDX-FileCopyrightText: 2023 Wilhelm Schürmann <wimschuermann@googlemail.com>
--
-- SPDX-License-Identifier: MIT

-- This script attempts to implement the basic functionality needed in order for
-- the LADXR Archipelago client to be able to talk to EmuHawk instead of RetroArch
-- by reproducing the RetroArch API with EmuHawk's Lua interface.
--
-- RetroArch UDP API: https://github.com/libretro/RetroArch/blob/master/command.c
--
-- Only
--  VERSION
--  GET_STATUS
--  READ_CORE_MEMORY
--  WRITE_CORE_MEMORY
-- commands are supported right now.
--
-- USAGE:
--  Load this script in EmuHawk ("Tools" -> "Lua Console" -> "Script" -> "Open Script", or drag+drop)
--
-- All inconsistencies (like missing newlines for some commands) of the RetroArch
-- UDP API (network_cmd_enable) are reproduced as-is in order for clients written to work with
-- RetroArch's current API to "just work"(tm).
--
-- This script has only been tested on GB(C). If you have made sure it works for N64 or other
-- cores supported by EmuHawk, please let me know. Note that GET_STATUS, at the very least, will
-- have to be adjusted.
--
--
-- NOTE:
--  EmuHawk's Lua API is very trigger-happy on throwing exceptions.
--  Emulation will continue fine, but the RetroArch API layer will stop working. This
--  is indicated only by an exception visible in the Lua console, which most players
--  will probably not have in the foreground.
--
--  pcall(), the usual way to catch exceptions in Lua, doesn't appear to be supported at all,
--  meaning that error/exception handling is not easily possible.
--
--  This means that a lot more error checking would need to happen before e.g. reading/writing
--  memory. Since the end goal, according to AP's Discord, seems to be SNI integration of GB(C),
--  no further fault-proofing has been done on this.
--


local socket = require("socket")
udp = socket.socket.udp()
require('common')

udp:setsockname('127.0.0.1', 55355)
udp:settimeout(0)

function on_vblank()
    -- Attempt to lessen the CPU load by only polling the UDP socket every x frames.
    -- x = 10 is entirely arbitrary, very little thought went into it.
    -- We could try to make use of client.get_approx_framerate() here, but the values returned
    -- seemed more or less arbitrary as well.
    --
    -- NOTE: Never mind the above, the LADXR Archipelago client appears to run into problems with
    --       interwoven GET_STATUS calls, leading to stopped communication.
    --       For GB(C), polling the socket on every frame is OK-ish, so we just do that.
    --
    --while emu.framecount() % 10 ~= 0 do
    --    emu.frameadvance()
    --end

    local data, msg_or_ip, port_or_nil = udp:receivefrom()
    if data then
        -- "data" format is "COMMAND [PARAMETERS] [...]"
        local command = string.match(data, "%S+")
        if command == "VERSION" then
            -- 1.14 is the latest RetroArch release at the time of writing this, no other reason
            -- for choosing this here.
            udp:sendto("1.14.0\n", msg_or_ip, port_or_nil)
        elseif command == "GET_STATUS" then
            local status = "PLAYING"
            if client.ispaused() then
                status = "PAUSED"
            end

            if emu.getsystemid() == "GBC" then
                -- Actual reply from RetroArch's API:
                -- "GET_STATUS PLAYING game_boy,AP_62468482466172374046_P1_Lonk,crc32=3ecb7b6f"
                -- CRC32 isn't readily available through the Lua API. We could calculate
                -- it ourselves, but since LADXR doesn't make use of this field it is
                -- simply replaced by the hash that EmuHawk _does_ make available.

                udp:sendto(
                    "GET_STATUS " .. status .. " game_boy," ..
                    string.gsub(gameinfo.getromname(), "[%s,]", "_") ..
                    ",romhash=" ..
                    gameinfo.getromhash() .. "\n",
                    msg_or_ip, port_or_nil
                )
            else -- No ROM loaded
                -- NOTE: No newline is intentional here for 1:1 RetroArch compatibility
                udp:sendto("GET_STATUS CONTENTLESS", msg_or_ip, port_or_nil)
            end
        elseif command == "READ_CORE_MEMORY" then
            local _, address, length = string.match(data, "(%S+) (%S+) (%S+)")
            address = stripPrefix(address, "0x")
            address = tonumber(address, 16)
            length = tonumber(length)

            -- NOTE: mainmemory.read_bytes_as_array() would seem to be the obvious choice
            --       here instead, but it isn't. At least for Sameboy and Gambatte, the "main"
            --       memory differs (ROM vs WRAM).
            --       Using memory.read_bytes_as_array() and explicitly using the System Bus
            --       as the active memory domain solves this incompatibility, allowing us
            --       to hopefully use whatever GB(C) emulator we want.
            local mem = memory.read_bytes_as_array(address, length, "System Bus")
            local hex_string = ""
            for _, v in ipairs(mem) do
                hex_string = hex_string .. string.format("%02X ", v)
            end

            hex_string = hex_string:sub(1, -2) -- Hang head in shame, remove last " "
            local reply = string.format("%s %02x %s\n", command, address, hex_string)
            udp:sendto(reply, msg_or_ip, port_or_nil)
        elseif command == "WRITE_CORE_MEMORY" then
            local _, address = string.match(data, "(%S+) (%S+)")
            address = stripPrefix(address, "0x")
            address = tonumber(address, 16)

            local to_write = {}
            local i = 1
            for byte_str in string.gmatch(data, "%S+") do
                if i > 2 then
                    byte_str = stripPrefix(byte_str, "0x")
                    table.insert(to_write, tonumber(byte_str, 16))
                end
                i = i + 1
            end

            memory.write_bytes_as_array(address, to_write, "System Bus")
            local reply = string.format("%s %02x %d\n", command, address, i - 3)
            udp:sendto(reply, msg_or_ip, port_or_nil)
        end
    end
end

event.onmemoryexecute(on_vblank, 0x40, "ap_connector_vblank")

while true do
    emu.yield()
end
