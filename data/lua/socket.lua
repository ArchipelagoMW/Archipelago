-----------------------------------------------------------------------------
-- LuaSocket helper module
-- Author: Diego Nehab
-- RCS ID: $Id: socket.lua,v 1.22 2005/11/22 08:33:29 diego Exp $
-----------------------------------------------------------------------------

-----------------------------------------------------------------------------
-- Declare module and import dependencies
-----------------------------------------------------------------------------
local base = _G
local string = require("string")
local math = require("math")

function get_lua_version()
    local major, minor = _VERSION:match("Lua (%d+)%.(%d+)")
    assert(tonumber(major) == 5)
    if tonumber(minor) >= 4 then
        return "5-4"
    end
    return "5-1"
end

function get_os()
    local the_os, ext, arch
    if package.config:sub(1,1) == "\\" then
        the_os, ext = "windows", "dll"
        arch = os.getenv"PROCESSOR_ARCHITECTURE"
    else
        -- TODO: macos?
        the_os, ext = "linux", "so"
        arch = "x86_64" -- TODO: read ELF header from /proc/$PID/exe to get arch
    end

    if arch:find("64") ~= nil then
        arch = "x64"
    else
        arch = "x86"
    end

    return the_os, ext, arch
end

function get_socket_path()
    local the_os, ext, arch = get_os()
    -- for some reason ./ isn't working, so use a horrible hack to get the pwd
    local pwd = (io.popen and io.popen("cd"):read'*l') or "."
	return pwd .. "/" .. arch .. "/socket-" .. the_os .. "-" .. get_lua_version() .. "." .. ext
end
local lua_version = get_lua_version()
local socket_path = get_socket_path()
local socket = assert(package.loadlib(socket_path, "luaopen_socket_core"))()
local event = event
-- http://lua-users.org/wiki/ModulesTutorial
local M = {}
if setfenv then
	setfenv(1, M) -- for 5.1
else
	_ENV = M -- for 5.2
end

M.socket = socket
-- Bizhawk <= 2.8 has an issue where resetting the lua doesn't close the socket
-- ...to get around this, we register an exit handler to close the socket first
if lua_version == '5-1' then
    local old_udp = socket.udp
    function udp(self)
        s = old_udp(self)
        function close_socket(self)
            s:close()
        end
        event.onexit(close_socket)
        return s
    end
    socket.udp = udp
end

-----------------------------------------------------------------------------
-- Exported auxiliar functions
-----------------------------------------------------------------------------
function connect(address, port, laddress, lport)
    local sock, err = socket.tcp()
    if not sock then return nil, err end
    if laddress then
        local res, err = sock:bind(laddress, lport, -1)
        if not res then return nil, err end
    end
    local res, err = sock:connect(address, port)
    if not res then return nil, err end
    return sock
end

function bind(host, port, backlog)
    local sock, err = socket.tcp()
    if not sock then return nil, err end
    sock:setoption("reuseaddr", true)
    local res, err = sock:bind(host, port)
    if not res then return nil, err end
    res, err = sock:listen(backlog)
    if not res then return nil, err end
    return sock
end

try = socket.newtry()

function choose(table)
    return function(name, opt1, opt2)
        if base.type(name) ~= "string" then
            name, opt1, opt2 = "default", name, opt1
        end
        local f = table[name or "nil"]
        if not f then base.error("unknown key (".. base.tostring(name) ..")", 3)
        else return f(opt1, opt2) end
    end
end

-----------------------------------------------------------------------------
-- Socket sources and sinks, conforming to LTN12
-----------------------------------------------------------------------------
-- create namespaces inside LuaSocket namespace
sourcet = {}
sinkt = {}

BLOCKSIZE = 2048

sinkt["close-when-done"] = function(sock)
    return base.setmetatable({
        getfd = function() return sock:getfd() end,
        dirty = function() return sock:dirty() end
    }, {
        __call = function(self, chunk, err)
            if not chunk then
                sock:close()
                return 1
            else return sock:send(chunk) end
        end
    })
end

sinkt["keep-open"] = function(sock)
    return base.setmetatable({
        getfd = function() return sock:getfd() end,
        dirty = function() return sock:dirty() end
    }, {
        __call = function(self, chunk, err)
            if chunk then return sock:send(chunk)
            else return 1 end
        end
    })
end

sinkt["default"] = sinkt["keep-open"]

sink = choose(sinkt)

sourcet["by-length"] = function(sock, length)
    return base.setmetatable({
        getfd = function() return sock:getfd() end,
        dirty = function() return sock:dirty() end
    }, {
        __call = function()
            if length <= 0 then return nil end
            local size = math.min(socket.BLOCKSIZE, length)
            local chunk, err = sock:receive(size)
            if err then return nil, err end
            length = length - string.len(chunk)
            return chunk
        end
    })
end

sourcet["until-closed"] = function(sock)
    local done
    return base.setmetatable({
        getfd = function() return sock:getfd() end,
        dirty = function() return sock:dirty() end
    }, {
        __call = function()
            if done then return nil end
            local chunk, err, partial = sock:receive(socket.BLOCKSIZE)
            if not err then return chunk
            elseif err == "closed" then
                sock:close()
                done = 1
                return partial
            else return nil, err end
        end
    })
end


sourcet["default"] = sourcet["until-closed"]

source = choose(sourcet)

return M
