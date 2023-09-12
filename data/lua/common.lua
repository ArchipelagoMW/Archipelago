print("Loading AP lua connector script")

local lua_major, lua_minor = _VERSION:match("Lua (%d+)%.(%d+)")
lua_major = tonumber(lua_major)
lua_minor = tonumber(lua_minor)
-- lua compat shims
if lua_major > 5 or (lua_major == 5 and lua_minor >= 3) then
  require("lua_5_3_compat")
end

function table.empty (self)
    for _, _ in pairs(self) do
        return false
    end
    return true
end

local bizhawk_version = client.getversion()
local bizhawk_major, bizhawk_minor, bizhawk_patch = bizhawk_version:match("(%d+)%.(%d+)%.?(%d*)")
bizhawk_major = tonumber(bizhawk_major)
bizhawk_minor = tonumber(bizhawk_minor)
if bizhawk_patch == "" then
  bizhawk_patch = 0
else
  bizhawk_patch = tonumber(bizhawk_patch)
end

local is23Or24Or25 = (bizhawk_version=="2.3.1") or (bizhawk_major == 2 and bizhawk_minor >= 3 and bizhawk_minor <= 5)
local isGreaterOrEqualTo26 = bizhawk_major > 2 or (bizhawk_major == 2 and bizhawk_minor >= 6)
local isUntestedBizHawk = bizhawk_major > 2 or (bizhawk_major == 2 and bizhawk_minor > 9)
local untestedBizHawkMessage = "Warning: this version of BizHawk is newer than we know about. If it doesn't work, consider downgrading to 2.9"

u8 = memory.read_u8
wU8 = memory.write_u8
u16 = memory.read_u16_le
uRange = memory.readbyterange

function getMaxMessageLength()
  local denominator = 12
  if is23Or24Or25 then
    denominator = 11
  end
  return math.floor(client.screenwidth()/denominator)
end

function drawText(x, y, message, color)
  if is23Or24Or25 then
      gui.addmessage(message)
  elseif isGreaterOrEqualTo26 then
      gui.drawText(x, y, message, color, 0xB0000000, 18, "Courier New", "middle", "bottom", nil, "client")
  end
end

function clearScreen()
  if is23Or24Or25 then
      return
  elseif isGreaterOrEqualTo26 then
      drawText(0, 0, "", "black")
  end
end

itemMessages = {}

function drawMessages()
  if table.empty(itemMessages) then
      clearScreen()
      return
  end
  local y = 10
  found = false
  maxMessageLength = getMaxMessageLength()
  for k, v in pairs(itemMessages) do
      if v["TTL"] > 0 then
          message = v["message"]
          while true do
              drawText(5, y, message:sub(1, maxMessageLength), v["color"])
              y = y + 16

              message = message:sub(maxMessageLength + 1, message:len())
              if message:len() == 0 then
                  break
              end
          end
          newTTL = 0
          if isGreaterOrEqualTo26 then
              newTTL = itemMessages[k]["TTL"] - 1
          end
          itemMessages[k]["TTL"] = newTTL
          found = true
      end
  end
  if found == false then
      clearScreen()
  end
end

function checkBizHawkVersion()
  if not is23Or24Or25 and not isGreaterOrEqualTo26 then
    print("Must use a version of BizHawk 2.3.1 or higher")
    return false
  elseif isUntestedBizHawk then
    print(untestedBizHawkMessage)
  end
  return true
end

function stripPrefix(s, p)
  return (s:sub(0, #p) == p) and s:sub(#p+1) or s
end
