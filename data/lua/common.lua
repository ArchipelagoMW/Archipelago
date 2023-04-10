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

function arrayEqual(a1, a2)
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
local isUntestedBizhawk = bizhawk_major > 2 or (bizhawk_major == 2 and bizhawk_minor > 9)
local untestedBizhawkMessage = "Warning: this version of bizhawk is newer than we know about. If it doesn't work, consider downgrading to 2.9"

u8 = memory.read_u8
wU8 = memory.write_u8
u16 = memory.read_u16_le

function getMaxMessageLength()
  if is23Or24Or25 then
      return client.screenwidth()/11
  elseif isGreaterOrEqualTo26 then
      return client.screenwidth()/12
  end
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

function checkBizhawkVersion()
  if not is23Or24Or25 and not isGreaterOrEqualTo26 then
    print("Must use a version of bizhawk 2.3.1 or higher")
    return false
  elseif isUntestedBizhawk then
    print(untestedBizhawkMessage)
  end
  return true
end