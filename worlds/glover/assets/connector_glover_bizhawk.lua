-- Glover Connector Lua
-- Created by Mike Jackson (jjjj12212)

local socket_loaded, socket = pcall(require, "socket")
if not socket_loaded then
  print("Please place this file in the 'Archipelago/data/lua' directory. Use the Archipelago Launcher's 'Browse Files' button to find the Archipelago directory.")
  return
end
local json = require('json')
local math = require('math')
require('common')

local SCRIPT_VERSION = 1
local GVR_VERSION = "V0.1"
local PLAYER = ""
local SEED = 0

local BT_SOCK = nil

local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"
local PREV_STATE = ""
local CUR_STATE =  STATE_UNINITIALIZED
local FRAME = 0
local VERROR = false
local CLIENT_VERSION = false
local GOAL_PRINTED = false

local AP_TIMEOUT_COUNTER = 0


-------------- MAP VARS -------------
local CURRENT_MAP = nil;
local CURRENT_HUB = nil;
local WORLD_ID = 99;
local WORLD_NAME = "";

-------------- TOTALS VARS -----------
local TOTAL_LIVES = 0;
local TOTAL_SINGLE_GARIBS = 0;
local TOTAL_ATLANTIS_1_GARIBS = 0;
local TOTAL_ATLANTIS_2_GARIBS = 0;
local TOTAL_ATLANTIS_3_GARIBS = 0;
local TOTAL_ATLANTIS_BONUS_GARIBS = 0;
local TOTAL_CARNIVAL_1_GARIBS = 0;
local TOTAL_CARNIVAL_2_GARIBS = 0;
local TOTAL_CARNIVAL_3_GARIBS = 0;
local TOTAL_CARNIVAL_BONUS_GARIBS = 0;
local TOTAL_PIRATES_1_GARIBS = 0;
local TOTAL_PIRATES_2_GARIBS = 0;
local TOTAL_PIRATES_3_GARIBS = 0;
local TOTAL_PIRATES_BONUS_GARIBS = 0;
local TOTAL_PREHISTORIC_1_GARIBS = 0;
local TOTAL_PREHISTORIC_2_GARIBS = 0;
local TOTAL_PREHISTORIC_3_GARIBS = 0;
local TOTAL_PREHISTORIC_BONUS_GARIBS = 0;
local TOTAL_FORTRESS_1_GARIBS = 0;
local TOTAL_FORTRESS_2_GARIBS = 0;
local TOTAL_FORTRESS_3_GARIBS = 0;
local TOTAL_FORTRESS_BONUS_GARIBS = 0;
local TOTAL_SPACE_1_GARIBS = 0;
local TOTAL_SPACE_2_GARIBS = 0;
local TOTAL_SPACE_3_GARIBS = 0;
local TOTAL_SPACE_BONUS_GARIBS = 0;

--------------- DEATH LINK ----------------------
local DEATH_LINK_TRIGGERED = false;
local DEATH_LINK = false

--------------- TAG LINK ------------------------
local TAG_LINK_TRIGGERED = false
local TAG_LINK = false



local receive_map = { -- [ap_id] = item_id; --  Required for Async Items
    ["NA"] = "NA"
}

local ITEM_TABLE = {}; -- reverses ROM_ITEM so the key is the Item
local ROM_ITEM_TABLE = {
    "AP_JUMP",
    "AP_DOUBLE_JUMP",
    "AP_CARTWHEEL",
    "AP_CRAWL",
    "AP_FISTSLAM",
    "AP_PUSH",
    "AP_LOCATE_BALL",
    "AP_LEDGEGRAB",
    "AP_LOCATE_GARIB",
    "AP_DRIBBLE",
    "AP_QUICKSWAP",
    "AP_SLAP",
    "AP_THROW",
    "AP_TOSS",
    "AP_BALLUP",
    "AP_RUBBER_BALL",
    "AP_BOWLING_BALL",
    "AP_POWER_BALL",
    "AP_BEARING_BALL",
    "AP_CRYSTAL_BALL",
    "AP_SINGLE_GARIB",
    "AP_ATLANTIS_L1_GARIBS",
    "AP_ATLANTIS_L2_GARIBS",
    "AP_ATLANTIS_L3_GARIBS",
    "AP_ATLANTIS_BONUS_GARIBS",
    "AP_CARNIVAL_L1_GARIBS",
    "AP_CARNIVAL_L2_GARIBS",
    "AP_CARNIVAL_L3_GARIBS",
    "AP_CARNIVAL_BONUS_GARIBS",
    "AP_PIRATES_L1_GARIBS",
    "AP_PIRATES_L2_GARIBS",
    "AP_PIRATES_L3_GARIBS",
    "AP_PIRATES_BONUS_GARIBS",
    "AP_PREHISTORIC_L1_GARIBS",
    "AP_PREHISTORIC_L2_GARIBS",
    "AP_PREHISTORIC_L3_GARIBS",
    "AP_PREHISTORIC_BONUS_GARIBS",
    "AP_FORTRESS_L1_GARIBS",
    "AP_FORTRESS_L2_GARIBS",
    "AP_FORTRESS_L3_GARIBS",
    "AP_FORTRESS_BONUS_GARIBS",
    "AP_SPACE_L1_GARIBS",
    "AP_SPACE_L2_GARIBS",
    "AP_SPACE_L3_GARIBS",
    "AP_SPACE_BONUS_GARIBS",
    "AP_LIFE_UP",
    "AP_HERCULES_POTION",
    "AP_ATLANTIS_L1_GATE",
    "AP_ATLANTIS_L2_RAISE_WATER",
    "AP_ATLANTIS_L2_WATER_DRAIN",
    "AP_ATLANTIS_L2_GATE",
    "AP_MAX_ITEM"
};

for index, item in pairs(ROM_ITEM_TABLE)
do
    ITEM_TABLE[item] = index - 1
end

local WORLDS_TABLE = {}; -- reverses ROM_ITEM so the key is the Item
local ROM_WORLDS_TABLE = {
    "AP_ATLANTIS_L1",
    "AP_ATLANTIS_L2",
    "AP_ATLANTIS_L3",
    "AP_ATLANTIS_BOSS",
    "AP_ATLANTIS_BONUS",
    "AP_CARNIVAL_L1",
    "AP_CARNIVAL_L2",
    "AP_CARNIVAL_L3",
    "AP_CARNIVAL_BOSS",
    "AP_CARNIVAL_BONUS",
    "AP_PIRATES_L1",
    "AP_PIRATES_L2",
    "AP_PIRATES_L3",
    "AP_PIRATES_BOSS",
    "AP_PIRATES_BONUS",
    "AP_PREHISTORIC_L1",
    "AP_PREHISTORIC_L2",
    "AP_PREHISTORIC_L3",
    "AP_PREHISTORIC_BOSS",
    "AP_PREHISTORIC_BONUS",
    "AP_FORTRESS_L1",
    "AP_FORTRESS_L2",
    "AP_FORTRESS_L3",
    "AP_FORTRESS_BOSS",
    "AP_FORTRESS_BONUS",
    "AP_SPACE_L1",
    "AP_SPACE_L2",
    "AP_SPACE_L3",
    "AP_SPACE_BOSS",
    "AP_SPACE_BONUS",
    "AP_MAX_WORLDS"
};

for index, item in pairs(ROM_WORLDS_TABLE)
do
    WORLDS_TABLE[item] = index - 1
end


-- Address Map for Glover
local ADDRESS_MAP = {
    ["AP_ATLANTIS_L1"] = {
        ["GARIBS"] = {
            ["1"] = {
                ['id'] = 0x01,
                ['offset'] = 0,
            },
            ["2"] = {
                ['id'] = 0x02,
                ['offset'] = 1,
            },
            ["3"] = {
                ['id'] = 0x03,
                ['offset'] = 2,
            },
            ["4"] = {
                ['id'] = 0x04,
                ['offset'] = 3,
            },
            ["5"] = {
                ['id'] = 0x05,
                ['offset'] = 4,
            },
            ["6"] = {
                ['id'] = 0x06,
                ['offset'] = 5,
            },
            ["7"] = {
                ['id'] = 0x07,
                ['offset'] = 6,
            },
            ["8"] = {
                ['id'] = 0x08,
                ['offset'] = 7,
            },
            ["9"] = {
                ['id'] = 0x09,
                ['offset'] = 8,
            },
            ["10"] = {
                ['id'] = 0x0A,
                ['offset'] = 9,
            },
            ["11"] = {
                ['id'] = 0x0B,
                ['offset'] = 10,
            },
            ["12"] = {
                ['id'] = 0x0C,
                ['offset'] = 11,
            },
            ["13"] = {
                ['id'] = 0x0D,
                ['offset'] = 12,
            },
            ["14"] = {
                ['id'] = 0x0E,
                ['offset'] = 13,
            },
            ["15"] = {
                ['id'] = 0x0F,
                ['offset'] = 14,
            },
            ["16"] = {
                ['id'] = 0x10,
                ['offset'] = 15,
            },
            ["17"] = {
                ['id'] = 0x11,
                ['offset'] = 16,
            },
            ["18"] = {
                ['id'] = 0x12,
                ['offset'] = 17,
            },
            ["19"] = {
                ['id'] = 0x13,
                ['offset'] = 18,
            },
            ["20"] = {
                ['id'] = 0x14,
                ['offset'] = 19,
            },
            ["21"] = {
                ['id'] = 0x15,
                ['offset'] = 20,
            },
            ["22"] = {
                ['id'] = 0x16,
                ['offset'] = 21,
            },
            ["23"] = {
                ['id'] = 0x17,
                ['offset'] = 22,
            },
            ["24"] = {
                ['id'] = 0x18,
                ['offset'] = 23,
            },
            ["25"] = {
                ['id'] = 0x19,
                ['offset'] = 24,
            },
            ["26"] = {
                ['id'] = 0x1A,
                ['offset'] = 25,
            },
            ["27"] = {
                ['id'] = 0x1B,
                ['offset'] = 26,
            },
            ["28"] = {
                ['id'] = 0x1C,
                ['offset'] = 27,
            },
            ["29"] = {
                ['id'] = 0x1D,
                ['offset'] = 28,
            },
            ["30"] = {
                ['id'] = 0x1E,
                ['offset'] = 29,
            },
            ["31"] = {
                ['id'] = 0x1F,
                ['offset'] = 30,
            },
            ["32"] = {
                ['id'] = 0x20,
                ['offset'] = 31,
            },
            ["33"] = {
                ['id'] = 0x21,
                ['offset'] = 32,
            },
            ["34"] = {
                ['id'] = 0x22,
                ['offset'] = 33,
            },
            ["35"] = {
                ['id'] = 0x23,
                ['offset'] = 34,
            },
            ["36"] = {
                ['id'] = 0x24,
                ['offset'] = 35,
            },
            ["37"] = {
                ['id'] = 0x25,
                ['offset'] = 36,
            },
            ["38"] = {
                ['id'] = 0x26,
                ['offset'] = 37,
            },
            ["39"] = {
                ['id'] = 0x27,
                ['offset'] = 38,
            },
            ["40"] = {
                ['id'] = 0x28,
                ['offset'] = 39,
            },
            ["41"] = {
                ['id'] = 0x29,
                ['offset'] = 40,
            },
            ["42"] = {
                ['id'] = 0x2A,
                ['offset'] = 41,
            },
            ["43"] = {
                ['id'] = 0x2B,
                ['offset'] = 42,
            },
            ["44"] = {
                ['id'] = 0x2C,
                ['offset'] = 43,
            },
            ["45"] = {
                ['id'] = 0x2D,
                ['offset'] = 44,
            },
            ["46"] = {
                ['id'] = 0x2E,
                ['offset'] = 45,
            },
            ["47"] = {
                ['id'] = 0x2F,
                ['offset'] = 46,
            },
            ["48"] = {
                ['id'] = 0x30,
                ['offset'] = 47,
            },
            ["49"] = {
                ['id'] = 0x31,
                ['offset'] = 48,
            }
        },
        ["ENEMY_GARIBS"] = {
            ["50"] = {
                ['id'] = 0x32,
                ['offset'] = 49,
                ['object_id'] = 0x3E,
            },
        },
        ["LIFE"] = {
            ["51"] = {
                ["id"] = 0x33,
                ['offset'] = 0,
            },
            ["52"] = {
                ["id"] = 0x34,
                ['offset'] = 1,
            },
            ["53"] = {
                ["id"] = 0x35,
                ['offset'] = 2,
            },
        },
        ["TIP"] = {
            ["54"] = {
                ["id"] = 0x36,
                ['offset'] = 0,
            },
            ["55"] = {
                ["id"] = 0x37,
                ['offset'] = 1,
            },
            ["56"] = {
                ["id"] = 0x38,
                ['offset'] = 2,
            },
            ["57"] = {
                ["id"] = 0x39,
                ['offset'] = 3,
            },
            ["58"] = {
                ["id"] = 0x3A,
                ['offset'] = 4,
            },
        },
        ["CHECKPOINT"] = {
            ["59"] = {
                ["id"] = 0x3B,
                ['offset'] = 0,
            },
            ["60"] = {
                ["id"] = 0x3C,
                ['offset'] = 1,
            }
        }
    },
	["AP_ATLANTIS_L2"] = {
		["GARIBS"] = {
			[1] = {
				['id'] = 0x3F,
				['offset'] = 0,
			},
			[2] = {
				['id'] = 0x40,
				['offset'] = 1,
			},
			[3] = {
				['id'] = 0x41,
				['offset'] = 2,
			},
			[4] = {
				['id'] = 0x42,
				['offset'] = 3,
			},
			[5] = {
				['id'] = 0x43,
				['offset'] = 4,
			},
			[6] = {
				['id'] = 0x44,
				['offset'] = 5,
			},
			[7] = {
				['id'] = 0x45,
				['offset'] = 6,
			},
			[8] = {
				['id'] = 0x46,
				['offset'] = 7,
			},
			[9] = {
				['id'] = 0x47,
				['offset'] = 8,
			},
			[10] = {
				['id'] = 0x48,
				['offset'] = 9,
			},
			[11] = {
				['id'] = 0x49,
				['offset'] = 10,
			},
			[12] = {
				['id'] = 0x4A,
				['offset'] = 11,
			},
			[13] = {
				['id'] = 0x4B,
				['offset'] = 12,
			},
			[14] = {
				['id'] = 0x4C,
				['offset'] = 13,
			},
			[15] = {
				['id'] = 0x4D,
				['offset'] = 14,
			},
			[16] = {
				['id'] = 0x4E,
				['offset'] = 15,
			},
			[17] = {
				['id'] = 0x4F,
				['offset'] = 16,
			},
			[18] = {
				['id'] = 0x50,
				['offset'] = 17,
			},
			[19] = {
				['id'] = 0x51,
				['offset'] = 18,
			},
			[20] = {
				['id'] = 0x52,
				['offset'] = 19,
			},
			[21] = {
				['id'] = 0x53,
				['offset'] = 20,
			},
			[22] = {
				['id'] = 0x54,
				['offset'] = 21,
			},
			[23] = {
				['id'] = 0x55,
				['offset'] = 22,
			},
			[24] = {
				['id'] = 0x56,
				['offset'] = 23,
			},
			[25] = {
				['id'] = 0x57,
				['offset'] = 24,
			},
			[26] = {
				['id'] = 0x58,
				['offset'] = 25,
			},
			[27] = {
				['id'] = 0x59,
				['offset'] = 26,
			},
			[28] = {
				['id'] = 0x5A,
				['offset'] = 27,
			},
			[29] = {
				['id'] = 0x5B,
				['offset'] = 28,
			},
			[30] = {
				['id'] = 0x5C,
				['offset'] = 29,
			},
			[31] = {
				['id'] = 0x5D,
				['offset'] = 30,
			},
			[32] = {
				['id'] = 0x5E,
				['offset'] = 31,
			},
			[33] = {
				['id'] = 0x5F,
				['offset'] = 32,
			},
			[34] = {
				['id'] = 0x60,
				['offset'] = 33,
			},
			[35] = {
				['id'] = 0x61,
				['offset'] = 34,
			},
			[36] = {
				['id'] = 0x62,
				['offset'] = 35,
			},
			[37] = {
				['id'] = 0x63,
				['offset'] = 36,
			},
			[38] = {
				['id'] = 0x64,
				['offset'] = 37,
			},
			[39] = {
				['id'] = 0x65,
				['offset'] = 38,
			},
			[40] = {
				['id'] = 0x66,
				['offset'] = 39,
			},
			[41] = {
				['id'] = 0x67,
				['offset'] = 40,
			},
			[42] = {
				['id'] = 0x68,
				['offset'] = 41,
			},
			[43] = {
				['id'] = 0x69,
				['offset'] = 42,
			},
			[44] = {
				['id'] = 0x6A,
				['offset'] = 43,
			},
			[45] = {
				['id'] = 0x6B,
				['offset'] = 44,
			},
			[46] = {
				['id'] = 0x6C,
				['offset'] = 45,
			},
			[47] = {
				['id'] = 0x6D,
				['offset'] = 46,
			},
			[48] = {
				['id'] = 0x6E,
				['offset'] = 47,
			},
			[49] = {
				['id'] = 0x6F,
				['offset'] = 48,
			},
			[50] = {
				['id'] = 0x70,
				['offset'] = 49,
			},
			[51] = {
				['id'] = 0x71,
				['offset'] = 50,
			},
			[52] = {
				['id'] = 0x72,
				['offset'] = 51,
			},
			[53] = {
				['id'] = 0x73,
				['offset'] = 52,
			},
			[54] = {
				['id'] = 0x74,
				['offset'] = 53,
			},
		},
		["ENEMY_GARIBS"] = {
			[55] = {
				['id'] = 0x75,
				['offset'] = 54,
				['object_id'] = 0x83,
			},
			[56] = {
				['id'] = 0x76,
				['offset'] = 55,
				['object_id'] = 0x84,
			},
			[57] = {
				['id'] = 0x77,
				['offset'] = 56,
				['object_id'] = 0x85,
			},
			[58] = {
				['id'] = 0x78,
				['offset'] = 57,
				['object_id'] = 0x86,
			},
			[59] = {
				['id'] = 0x79,
				['offset'] = 58,
				['object_id'] = 0x87,
			},
			[60] = {
				['id'] = 0x7A,
				['offset'] = 59,
				['object_id'] = 0x88,
			},
		},
		["LIFE"] = {
			[61] = {
				['id'] = 0x7B,
				['offset'] = 0,
			},
		},
		["TIP"] = {
			[62] = {
				['id'] = 0x7C,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			[63] = {
				['id'] = 0x7D,
				['offset'] = 0,
			},
			[64] = {
				['id'] = 0x7E,
				['offset'] = 1,
			},
			[65] = {
				['id'] = 0x7F,
				['offset'] = 2,
			}
		}
	}
}


local MESSAGE_TABLE = {}


GLOVERHACK = {
    RDRAMBase = 0x80000000,
    RDRAMSize = 0x800000,

        base_pointer = 0x400000,
    pc = 0x0,
    text_size = 27,
    ap_items = 0x0,
    ap_world = 0x54,
      hub_entrance = 0x0,
      door_number = 0x1,
      garib_locations = 0x4,
        garib_id = 0x4,
        garib_collected = 0x6,
        garib_object_id = 0x8,
      garib_size = 0xC,
      garib_all_collected = 0x3C4,
      life_locations = 0x3C8,
        life_id = 0x4,
        life_collected = 0x6,
      life_size = 0x8,
      tip_locations = 0x418,
        tip_id = 0x4,
        tip_collected = 0x6,
      tip_size = 0x8,
      checkpoint_locations = 0x440,
        checkpoint_id = 0x4,
        checkpoint_collected = 0x6,
      checkpoint_size = 0xC,
      switch_locations = 0x47C,
        switch_id = 0x4,
        switch_collected = 0x6,
      switch_size = 0xC,
      goals = 0x4E8,
    ap_world_offset = 0x4F0,
    ap_hub_order = 0x9474,
    garib_totals = 0x947A,
    settings = 0x94F2,
      garib_logic = 0x0,
      garib_sorting = 0x1,
    hub_map = 0x94F6,
    world_map = 0x94F7,
    ROM_MAJOR_VERSION = 0x9502,
    ROM_MINOR_VERSION = 0x9503,
    ROM_PATCH_VERSION = 0x9504,

    txt_queue = 0
}

function GLOVERHACK:new(t)
    t = t or {}
    setmetatable(t, self)
    self.__index = self
   return self
end

function GLOVERHACK:isPointer(value)
    return type(value) == "number" and value >= self.RDRAMBase and value < self.RDRAMBase + self.RDRAMSize;
end

function GLOVERHACK:dereferencePointer(addr)
    if type(addr) == "number" and addr >= 0 and addr < (self.RDRAMSize - 4) then
        local address = mainmemory.read_u32_be(addr);
        if GLOVERHACK:isPointer(address) then
            return address - self.RDRAMBase;
        else
            print("Failed to Defref:")
            print(address)
            return nil;
        end
    end
end

function GLOVERHACK:getWorldOffset(world_id)
    if world_id == 0
    then
        return self.ap_world
    elseif world_id == 1
    then 
        return self.ap_world + self.ap_world_offset
    else
        return self.ap_world + (self.ap_world_offset * world_id)
    end
end

function GLOVERHACK:getOffsetLocation(location_addr, offset, type)
    local offset_size = 0
    if type == "garib"
    then
        offset_size = self.garib_size
    elseif type == "life"
    then
        offset_size = self.life_size

    elseif type == "checkpoint"
    then
        offset_size = self.checkpoint_size

    elseif type == "switch"
    then
        offset_size = self.switch_size

    elseif type == "tip"
    then
        offset_size = self.tip_size
    end

    if offset == 0
    then
        return location_addr
    elseif offset == 1
    then 
        return location_addr + offset_size
    else
        return location_addr + (offset_size * offset)
    end
end

function GLOVERHACK:checkRealFlag(offset, byte)
    -- print("Checking Real Flags")
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
	local realptr = GLOVERHACK:dereferencePointer(self.real_flags + hackPointerIndex);
    -- if realptr == nil
    -- then
    --     return false
    -- end
    local currentValue = mainmemory.readbyte(realptr + offset);
    if bit.check(currentValue, byte) then
        return true;
    end
    return false;
end

function GLOVERHACK:checkLocationFlag(world_id, type, offset, item_id)
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    local world_address = hackPointerIndex + GLOVERHACK:getWorldOffset(world_id)
    if type == "garib"
    then
        local offset_location = GLOVERHACK:getOffsetLocation(self.garib_locations, offset, type)
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.garib_id)
        if check_id ~= item_id then
            print("GARIB Item ID DOES NOT MATCH! CHECK OFFSET FOR ID")
            print(item_id)
            print(check_id)
        end
        local check_value = mainmemory.readbyte(world_address + offset_location + self.garib_collected)
        if check_value == 0x0
        then
            return false
        else
            return true
        end
    elseif type == "life"
    then
        local offset_location = GLOVERHACK:getOffsetLocation(self.life_locations, offset, type)
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.life_id)
        if check_id ~= item_id then
            print("LIFE Item ID DOES NOT MATCH! CHECK OFFSET FOR ID")
            print(item_id)
        end
        local check_value = mainmemory.readbyte(world_address + offset_location + self.life_collected)
        if check_value == 0x0
        then
            return false
        else
            return true
        end
    elseif type == "checkpoint"
    then
        local offset_location = GLOVERHACK:getOffsetLocation(self.checkpoint_locations, offset, type)
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.checkpoint_id)
        if check_id ~= item_id then
            print("CHECKPOINT Item ID DOES NOT MATCH! CHECK OFFSET FOR ID")
            print(item_id)
        end
        local check_value = mainmemory.readbyte(world_address + offset_location + self.checkpoint_collected)
        if check_value == 0x0
        then
            return false
        else
            return true
        end
    elseif type == "switch"
    then
        local offset_location = GLOVERHACK:getOffsetLocation(self.switch_locations, offset, type)
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.switch_id)
        if check_id ~= item_id then
            print("SWITCH Item ID DOES NOT MATCH! CHECK OFFSET FOR ID")
            print(item_id)
        end
        local check_value = mainmemory.readbyte(world_address + offset_location + self.switch_collected)
        if check_value == 0x0
        then
            return false
        else
            return true
        end
    elseif type == "tip"
    then
        local offset_location = GLOVERHACK:getOffsetLocation(self.tip_locations, offset, type)
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.tip_id)
        if check_id ~= item_id then
            print("TIP Item ID DOES NOT MATCH! CHECK OFFSET FOR ID")
            print(item_id)
        end
        local check_value = mainmemory.readbyte(world_address + offset_location + self.tip_collected)
        if check_value == 0x0
        then
            return false
        else
            return true
        end
    end
end

function GLOVERHACK:checkEnemyGaribLocationFlag(world_id, offset_list, ap_id)
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    local world_address = hackPointerIndex + GLOVERHACK:getWorldOffset(world_id)
    for _, offset in pairs(offset_list)
    do
        local offset_location = GLOVERHACK:getOffsetLocation(self.garib_locations, offset, "garib")
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.garib_object_id)
        if check_id == ap_id then
             local check_value = mainmemory.readbyte(world_address + offset_location + self.garib_collected)
            if check_value ~= 0x0
            then
                return true
            end
        end
    end
    return false
end

function GLOVERHACK:getSettingPointer()
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    if hackPointerIndex == nil
    then
        return
    end
	return self.settings + hackPointerIndex;
end

function GLOVERHACK:setGaribLogic(glogic)
    mainmemory.writebyte(self.garib_logic + GLOVERHACK:getSettingPointer(), glogic);
end

function GLOVERHACK:setGaribSorting(gsort)
    mainmemory.writebyte(self.garib_sorting + GLOVERHACK:getSettingPointer(), gsort);
end

function GLOVERHACK:getItemsPointer()
    -- print("Checking Items Flags")
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
	return self.ap_items + hackPointerIndex;
end

function GLOVERHACK:getItem(index)
    return mainmemory.readbyte(index + self:getItemsPointer());
end

function GLOVERHACK:setItem(index, value)
    mainmemory.writebyte(index + self:getItemsPointer(), value);
end

function GLOVERHACK:getWorldMap()
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    if hackPointerIndex == nil
    then
        return 0x0
    end
    return mainmemory.readbyte(hackPointerIndex + self.world_map)
end

function GLOVERHACK:getHubMap()
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    if hackPointerIndex == nil
    then
        return 0x0
    end
    return mainmemory.readbyte(hackPointerIndex + self.hub_map)
end

function GLOVERHACK:getPCPointer()
    -- print("GetPCPtr")
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    if hackPointerIndex == nil
    then
        return nil
    end
	return GLOVERHACK:dereferencePointer(hackPointerIndex);
end

-- function GLOVERHACK:getPCMsgPointer()
--     local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
--     if hackPointerIndex == nil
--     then
--         return nil
--     end
-- 	return GLOVERHACK:dereferencePointer(self.pc_messages + hackPointerIndex);
-- end

-- function GLOVERHACK:getPCDeath()
--     return mainmemory.readbyte(self:getPCPointer() + self.pc_death_us);
-- end

-- function GLOVERHACK:getPCTag()
--     return mainmemory.readbyte(self:getPCPointer() + self.pc_tag_us);
-- end

-- function GLOVERHACK:setPCDeath(DEATH_COUNT)
--     mainmemory.writebyte(self:getPCPointer() + self.pc_death_us, DEATH_COUNT);
-- end

-- function GLOVERHACK:setPCTag(TAG_COUNT)
--     mainmemory.writebyte(self:getPCPointer() + self.pc_tag_us, TAG_COUNT);
-- end

-- function GLOVERHACK:getAPDeath()
--    return mainmemory.readbyte(self:getPCPointer() + self.pc_death_ap);
-- end

-- function GLOVERHACK:getAPTag()
--    return mainmemory.readbyte(self:getPCPointer() + self.pc_tag_ap);
-- end

-- function GLOVERHACK:setAPDeath(DEATH_COUNT)
--     mainmemory.writebyte(self:getPCPointer() + self.pc_death_ap, DEATH_COUNT);
-- end

-- function GLOVERHACK:setAPTag(TAG_COUNT)
--     mainmemory.writebyte(self:getPCPointer() + self.pc_tag_ap, TAG_COUNT);
-- end

-- function GLOVERHACK:getNPointer()
--     local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
--     if hackPointerIndex == nil
--     then
--         return
--     end
-- 	return GLOVERHACK:dereferencePointer(self.n64 + hackPointerIndex);
-- end

-- function GLOVERHACK:getNLocalDeath()
--    return mainmemory.readbyte(GLOVERHACK:getNPointer() + self.n64_death_us);
-- end

-- function GLOVERHACK:getNLocalTag()
--    return mainmemory.readbyte(GLOVERHACK:getNPointer() + self.n64_tag_us);
-- end

-- function GLOVERHACK:setTextQueue(icon_id)
--     self.txt_queue = self.txt_queue + 1
--     GLOVERHACK:setSettingDialogCharacter(icon_id)
--     mainmemory.writebyte(self:getPCPointer() + self.pc_show_txt, self.txt_queue);
-- end

-- function GLOVERHACK:getCurrentQueue()
--     local ptr = self:getNPointer()
--     if ptr == nil
--     then
--         return 0
--     end
--     return mainmemory.readbyte(ptr + self.n64_show_text);
-- end

-- function GLOVERHACK:getPCQueue()
--     return self.txt_queue
-- end

-- function GLOVERHACK:setDialog(message, icon_id)
--     uppcase_text = string.upper(message)
--     local overflow = false
--     local last_char = 0
--     for idx = 0, string.len(uppcase_text)-1 do
--         if idx == 507
--         then
--             overflow = true
--             mainmemory.writebyte(self:getPCMsgPointer() + idx, 0);
--             break;
--         end
--         last_char = last_char + 1;
--         mainmemory.writebyte(self:getPCMsgPointer() + idx, uppcase_text:byte(idx + 1));
--     end
--     if overflow == false
--     then
--         mainmemory.writebyte(self:getPCMsgPointer() + last_char, 0);
--     end
--     self:setTextQueue(icon_id)
-- end

function GLOVERHACK:getRomVersion()
    local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    if hackPointerIndex == nil
    then
        return "0"
    end
	major = mainmemory.readbyte(self.ROM_MAJOR_VERSION + hackPointerIndex);
    minor = mainmemory.readbyte(self.ROM_MINOR_VERSION + hackPointerIndex);
    patch = mainmemory.readbyte(self.ROM_PATCH_VERSION + hackPointerIndex);
    if major == 0 and minor == 0 then
        return "0"
    end
    if patch == 0
    then
        return "V"..tostring(major).."."..tostring(minor)
    else
        return "V"..tostring(major).."."..tostring(minor).."."..tostring(patch)
    end
end

function garib_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["GARIBS"] ~= nil
            then
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["GARIBS"])
                do
                    checks[loc_id] = GVR:checkLocationFlag(WORLD_ID, "garib", locationTable['offset'], locationTable['id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function enemy_garib_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["ENEMY_GARIBS"] ~= nil
            then
                local offset_list = {};
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["ENEMY_GARIBS"])
                do
                    offset_list[loc_id] = locationTable["offset"]
                end
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["ENEMY_GARIBS"])
                do
                    checks[loc_id] = GVR:checkEnemyGaribLocationFlag(WORLD_ID, offset_list, locationTable['object_id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function life_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["LIFE"] ~= nil
            then
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["LIFE"])
                do
                    checks[loc_id] = GVR:checkLocationFlag(WORLD_ID, "life", locationTable['offset'], locationTable['id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function checkpoint_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["CHECKPOINT"] ~= nil
            then
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["CHECKPOINT"])
                do
                    checks[loc_id] = GVR:checkLocationFlag(WORLD_ID, "checkpoint", locationTable['offset'], locationTable['id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function switch_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["SWITCH"] ~= nil
            then
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["SWITCH"])
                do
                    checks[loc_id] = GVR:checkLocationFlag(WORLD_ID, "switch", locationTable['offset'], locationTable['id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function tip_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["TIP"] ~= nil
            then
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["TIP"])
                do
                    checks[loc_id] = GVR:checkLocationFlag(WORLD_ID, "tip", locationTable['offset'], locationTable['id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function received_garibs(itemId)
    if 6501001 <= itemId and itemId <= 6501009 then
        TOTAL_SINGLE_GARIBS = TOTAL_SINGLE_GARIBS + (itemId - 6501000)
        GVR:setItem(ITEM_TABLE["AP_SINGLE_GARIB"], TOTAL_SINGLE_GARIBS)
    elseif itemId == 6510001 then
        TOTAL_SINGLE_GARIBS = TOTAL_SINGLE_GARIBS + 1
        GVR:setItem(ITEM_TABLE["AP_SINGLE_GARIB"], TOTAL_SINGLE_GARIBS)
    elseif itemId == 6502001 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 1
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
    elseif itemId == 6500190 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 1
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
    elseif itemId == 6500191 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 2
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
    elseif itemId == 6500192 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 3
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
    elseif itemId == 6500193 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 4
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
    elseif itemId == 6500194 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 5
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
    elseif itemId == 6500195 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 6
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
    elseif itemId == 6500196 then
        TOTAL_ATLANTIS_1_GARIBS = TOTAL_ATLANTIS_1_GARIBS + 9
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GARIBS"], TOTAL_ATLANTIS_1_GARIBS)
        GVR:setItem(ITEM_TABLE["AP_ITEM_BBOMB"], 1)
    end
end

function received_moves(itemId)
    if itemId == 6500329 then
        -- print("Got Jump")
        GVR:setItem(ITEM_TABLE["AP_JUMP"], 1)
    elseif itemId == 6500330 then
        GVR:setItem(ITEM_TABLE["AP_CARTWHEEL"], 1)
    elseif itemId == 6500331 then
        GVR:setItem(ITEM_TABLE["AP_CRAWL"], 1)
    elseif itemId == 6500332 then
        GVR:setItem(ITEM_TABLE["AP_DOUBLE_JUMP"], 1)
    elseif itemId == 6500333 then
        GVR:setItem(ITEM_TABLE["AP_FISTSLAM"], 1)
    elseif itemId == 6500334 then
        GVR:setItem(ITEM_TABLE["AP_LEDGEGRAB"], 1)
    elseif itemId == 6500335 then
        GVR:setItem(ITEM_TABLE["AP_PUSH"], 1)
    elseif itemId == 6500336 then
        GVR:setItem(ITEM_TABLE["AP_LOCATE_GARIB"], 1)
    elseif itemId == 6500337 then
        GVR:setItem(ITEM_TABLE["AP_LOCATE_BALL"], 1)
    elseif itemId == 6500338 then
        GVR:setItem(ITEM_TABLE["AP_DRIBBLE"], 1)
    elseif itemId == 6500339 then
        GVR:setItem(ITEM_TABLE["AP_QUICKSWAP"], 1)
    elseif itemId == 6500340 then
        GVR:setItem(ITEM_TABLE["AP_SLAP"], 1)
    elseif itemId == 6500341 then
        GVR:setItem(ITEM_TABLE["AP_THROW"], 1)
    elseif itemId == 6500342 then
        GVR:setItem(ITEM_TABLE["AP_TOSS"], 1)
        
    elseif itemId == 6500352 then
        GVR:setItem(ITEM_TABLE["AP_RUBBER_BALL"], 1)
    elseif itemId == 6500353 then
        GVR:setItem(ITEM_TABLE["AP_BOWLING_BALL"], 1)
    elseif itemId == 6500354 then
        GVR:setItem(ITEM_TABLE["AP_BEARING_BALL"], 1)
    elseif itemId == 6500355 then
        GVR:setItem(ITEM_TABLE["AP_CRYSTAL_BALL"], 1)
    elseif itemId == 6500356 then
        GVR:setItem(ITEM_TABLE["AP_POWER_BALL"], 1)
    end
end

function received_misc(itemId)
    if itemId == 6500357 then
        TOTAL_LIVES = TOTAL_LIVES + 1
        GVR:setItem(ITEM_TABLE["AP_LIFE_UP"], TOTAL_LIVES)
    end
end

---------------------------------- MAP FUNCTIONS -----------------------------------

function set_map(map)
    WORLD_ID = WORLDS_TABLE[map]
    WORLD_NAME = map
end

function map_handler()
    if CURRENT_HUB == 0x06 then
        if CURRENT_MAP == 0x10 then 
            set_map("AP_ATLANTIS_L1")
        elseif CURRENT_MAP == 0x11 then set_map("AP_ATLANTIS_L2")
        elseif CURRENT_MAP == 0x12 then set_map("AP_ATLANTIS_L3") 
        elseif CURRENT_MAP == 0x13 then set_map("AP_ATLANTIS_BOSS")
        elseif CURRENT_MAP == 0x14 then set_map("AP_ATLANTIS_BONUS") 
        end
    elseif CURRENT_HUB == 0x07 then
        if CURRENT_MAP == 0x10 then set_map("AP_CARNIVAL_L1")
        elseif CURRENT_MAP == 0x11 then set_map("AP_CARNIVAL_L2")
        elseif CURRENT_MAP == 0x12 then set_map("AP_CARNIVAL_L3") 
        elseif CURRENT_MAP == 0x13 then set_map("AP_CARNIVAL_BOSS")
        elseif CURRENT_MAP == 0x14 then set_map("AP_CARNIVAL_BONUS") 
        end
    elseif CURRENT_HUB == 0x08 then
        if CURRENT_MAP == 0x10 then set_map("AP_PIRATES_L1")
        elseif CURRENT_MAP == 0x11 then set_map("AP_PIRATES_L2")
        elseif CURRENT_MAP == 0x12 then set_map("AP_PIRATES_L3") 
        elseif CURRENT_MAP == 0x13 then set_map("AP_PIRATES_BOSS")
        elseif CURRENT_MAP == 0x14 then set_map("AP_PIRATES_BONUS") 
        end
    elseif CURRENT_HUB == 0x09 then
        if CURRENT_MAP == 0x10 then set_map("AP_PREHISTORIC_L1")
        elseif CURRENT_MAP == 0x11 then set_map("AP_PREHISTORIC_L2")
        elseif CURRENT_MAP == 0x12 then set_map("AP_PREHISTORIC_L3") 
        elseif CURRENT_MAP == 0x13 then set_map("AP_PREHISTORIC_BOSS")
        elseif CURRENT_MAP == 0x14 then set_map("AP_PREHISTORIC_BONUS") 
        end
    elseif CURRENT_HUB == 0x0A then
        if CURRENT_MAP == 0x10 then set_map("AP_FORTRESS_L1")
        elseif CURRENT_MAP == 0x11 then set_map("AP_FORTRESS_L2")
        elseif CURRENT_MAP == 0x12 then set_map("AP_FORTRESS_L3") 
        elseif CURRENT_MAP == 0x13 then set_map("AP_FORTRESS_BOSS")
        elseif CURRENT_MAP == 0x14 then set_map("AP_FORTRESS_BONUS") 
        end
    elseif CURRENT_HUB == 0x0B then
        if CURRENT_MAP == 0x10 then set_map("AP_SPACE_L1")
        elseif CURRENT_MAP == 0x11 then set_map("AP_SPACE_L2")
        elseif CURRENT_MAP == 0x12 then set_map("AP_SPACE_L3") 
        elseif CURRENT_MAP == 0x13 then set_map("AP_SPACE_BOSS")
        elseif CURRENT_MAP == 0x14 then set_map("AP_SPACE_BONUS") 
        end
    end
end

---------------------------------- ITEM GET MESSAGES ----------------------------------


-- function display_item_message(msg_table)
--     -- Cancel if not for this player
--     if msg_table["to_player"] ~= PLAYER
--     then
--         return
--     end
--     -- Select item for current level of progressive move upgrades
--     convert_progressive_move_message(msg_table)

--     -- Select text depending on item id
--     local msg_text = get_item_message_text(msg_table["item_id"], msg_table["item"], msg_table["player"])
--     if not msg_text then return end

--     -- Select character icon depending on item id
--     local msg_icon = get_item_message_char(msg_table["item_id"]);
--     if not msg_icon then return end

--     table.insert(MESSAGE_TABLE, {msg_text, msg_icon});
-- end

-- function convert_progressive_move_message(msg_table)
--     local item_id = msg_table["item_id"]
--     if item_id == 1230828 -- Progressive Beak Buster
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_BDRILL"]) == 1
--         then
--             msg_table["item_id"] = 1230757
--             msg_table["item"] = "Bill Drill"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_BBUST"]) == 1
--         then
--             msg_table["item_id"] = 1230820
--             msg_table["item"] = "Beak Buster"
--         end
--     elseif item_id == 1230829 -- Progressive Eggs
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_CEGGS"]) == 1
--         then
--             msg_table["item_id"] = 1230767
--             msg_table["item"] = "Clockwork Eggs"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_IEGGS"]) == 1
--         then
--             msg_table["item_id"] = 1230763
--             msg_table["item"] = "Ice Eggs"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_GEGGS"]) == 1
--         then
--             msg_table["item_id"] = 1230759
--             msg_table["item"] = "Grenade Eggs"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_FEGGS"]) == 1
--         then
--             msg_table["item_id"] = 1230756
--             msg_table["item"] = "Fire Eggs"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_BEGGS"]) == 1
--         then
--             msg_table["item_id"] = 1230823
--             msg_table["item"] = "Blue Eggs"
--         end
--     elseif item_id == 1230830 -- Progressive Shoes
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_CLAWBTS"]) == 1
--         then
--             msg_table["item_id"] = 1230773
--             msg_table["item"] = "Claw Clamber Boots"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_SPRINGB"]) == 1
--         then
--             msg_table["item_id"] = 1230768
--             msg_table["item"] = "Springy Step Shoes"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_TTRAIN"]) == 1
--         then
--             msg_table["item_id"] = 1230821
--             msg_table["item"] = "Turbo Trainers"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_SSTRIDE"]) == 1
--         then
--             msg_table["item_id"] = 1230826
--             msg_table["item"] = "Stilt Stride"
--         end
--     elseif item_id == 1230831 -- Progressive Water Training
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_FSWIM"]) == 1
--         then
--             msg_table["item_id"] = 1230777
--             msg_table["item"] = "Fast Swimming"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_DAIR"]) == 1
--         then
--             msg_table["item_id"] = 1230778
--             msg_table["item"] = "Double Air"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_DIVE"]) == 1
--         then
--             msg_table["item_id"] = 1230810
--             msg_table["item"] = "Dive"
--         end
--     elseif item_id == 1230832 -- Progressive Bash Attack
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_BBASH"]) == 1
--         then
--             msg_table["item_id"] = 1230800
--             msg_table["item"] = "Breegull Bash"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_GRAT"]) == 1
--         then
--             msg_table["item_id"] = 1230824
--             msg_table["item"] = "Ground Rat-a-tat Rap"
--         end
--     elseif item_id == 1230782 -- Progressive Flight
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_AIREAIM"]) == 1
--         then
--             msg_table["item_id"] = 1230760
--             msg_table["item"] = "Airborne Egg Aiming"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_BBOMB"]) == 1
--         then
--             msg_table["item_id"] = 1230827
--             msg_table["item"] = "Beak Bomb"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_FPAD"]) == 1
--         then
--             msg_table["item_id"] = 1230811
--             msg_table["item"] = "Flight Pad"
--         end
--     elseif item_id == 1230783 -- Progressive Egg Aim
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_EGGAIM"]) == 1
--         then
--             msg_table["item_id"] = 1230755
--             msg_table["item"] = "Egg Aim"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"]) == 1
--         then
--             msg_table["item_id"] = 1230813
--             msg_table["item"] = "Third Person Egg Shooting"
--         end
--     elseif item_id == 1230784 -- Progressive Adv Water Training
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_FSWIM"]) == 1
--         then
--             msg_table["item_id"] = 1230777
--             msg_table["item"] = "Fast Swimming"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_DAIR"]) == 1
--         then
--             msg_table["item_id"] = 1230778
--             msg_table["item"] = "Double Air"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_TTORP"]) == 1
--         then
--             msg_table["item_id"] = 1230765
--             msg_table["item"] = "Talon Torpedo"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_AUQAIM"]) == 1
--         then
--             msg_table["item_id"] = 1230766
--             msg_table["item"] = "Sub-Aqua Egg Aiming"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_DIVE"]) == 1
--         then
--             msg_table["item_id"] = 1230810
--             msg_table["item"] = "Dive"
--         end
--     elseif item_id == 1230785 -- Progressive Adv Egg Aim
--     then
--         if GVR:getItem(ITEM_TABLE["AP_ITEM_BBLASTER"]) == 1
--         then
--             msg_table["item_id"] = 1230754
--             msg_table["item"] = "Breegull Blaster"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_EGGAIM"]) == 1
--         then
--             msg_table["item_id"] = 1230755
--             msg_table["item"] = "Egg Aim"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_AMAZEOGAZE"]) == 1
--         then
--             msg_table["item_id"] = 1230779
--             msg_table["item"] = "Amaze-O-Gaze"
--         elseif GVR:getItem(ITEM_TABLE["AP_ITEM_EGGSHOOT"]) == 1
--         then
--             msg_table["item_id"] = 1230813
--             msg_table["item"] = "Third Person Egg Shooting"
--         end
--     end
-- end

-- function get_item_message_text(item_id, item, player)
--     local own = player == PLAYER

--     if (1230753 <= item_id and item_id <= 1230780) -- BT Moves
--         or (1230810 <= item_id and item_id <= 1230827) -- BK Moves
--         or (1230782 <= item_id and item_id <= 1230785) -- Progessive Moves 1
--         or (1230828 <= item_id and item_id <= 1230832) -- Progressive Moves 2
--         or (item_id == 1230800 or item_id == 1230802) -- Stop'n'Swap Moves
--     then
--         return own
--             and string.format("You can now use %s.", item)
--             or string.format("%s taught you how to use %s.", player, item)
--     elseif 1230944 <= item_id and item_id <= 1230952 -- Worlds
--     then
--         return own
--             and string.format("%s is now open!", item)
--             or string.format("%s has just opened %s!", player, item)
--     elseif item_id == 1230796 -- Chuffy
--     then
--         local special = ENABLE_AP_CHUFFY and "\nDon't forget that you can call Chuffy at any unlocked station." or ""
--         return own
--             and string.format("You can now use %s.%s", item, special)
--             or string.format("%s has just repaired %s.%s", player, item, special)
--     elseif 1230790 <= item_id and item_id <= 1230795 -- Stations
--     then
--         return own
--             and string.format("You can now use the %s.", station_names[item_id])
--             or string.format("%s has just opened the %s.", player, station_names[item_id])
--     elseif 1230855 <= item_id and item_id <= 1230863 -- Mumbo Magic
--     then
--         if DIALOG_CHARACTER == 110 or DIALOG_CHARACTER == 8
--         then
--             -- Mumbo flavor text
--             return own
--                 and string.format("Mumbo now use mighty %s spell. Bear go visit Mumbo to try.", magic_names[item_id])
--                 or string.format("%s told Mumbo mighty %s spell. Bear go visit Mumbo to try.", player, magic_names[item_id])
--         else
--             -- Basic text
--             return own
--                 and string.format("Mumbo can now use the %s spell.", magic_names[item_id])
--                 or string.format("%s has just unlocked Mumbo's %s spell.", player, magic_names[item_id])
--         end
--     elseif 1230174 <= item_id and item_id <= 1230182 -- Humba Transformations
--     then
--         if DIALOG_CHARACTER == 110 or DIALOG_CHARACTER == 37
--         then
--             -- Humba flavor text
--             return own
--                 and string.format("Wumba now make bear %s. Very %s!", transformation_names[item_id]["name"], transformation_names[item_id]["attribute"])
--                 or string.format("%s told Wumba how to make bear %s. Very %s!", player, transformation_names[item_id]["name"], transformation_names[item_id]["attribute"])
--         else
--             -- Basic text
--             return own
--                 and string.format("Banjo can now be transformed into a %s.", transformation_names[item_id]["name"])
--                 or string.format("%s has just unlocked the %s transformation.", player, transformation_names[item_id]["name"])
--         end
--     elseif 1230870 <= item_id and item_id <= 1230876 -- Silos
--     then
--         return own
--             and string.format("%s is now open!", item)
--             or string.format("%s has just opened the %s!", player, item)
--     elseif 1230877 <= item_id and item_id <= 1230915 -- Warppads
--     then
--         return own
--             and string.format("You can now use the %s.", item)
--             or string.format("%s has just unlocked the %s.", player, item)
--     elseif 1230917 <= item_id and item_id <= 1230921 -- Cheats
--     then
--         return own
--             and string.format("You can now use the %s.", cheat_names[item_id])
--             or string.format("%s has just sent you the %s.", player, cheat_names[item_id])
--     end

--     return nil
-- end

-- function get_item_message_char(item_id)
--     -- Default character is used depending on the item
--     if DIALOG_CHARACTER == 110
--     then
--         if 1230753 <= item_id and item_id <= 1230776 -- BT Moves
--         then
--             return 17 -- Jamjars
--         elseif item_id == 1230779 -- Amaze O' Gaze
--         then
--             return 99 -- Goggles
--         elseif item_id == 1230780 -- Roar
--         then
--             return 50 -- Bargasaurus
--         elseif item_id == 1230800 or item_id == 1230802 -- Stop'n'Swap Moves
--         then
--             return 109 -- Heggy
--         elseif 1230810 <= item_id and item_id <= 1230827 -- BK Moves
--         then
--             return 7 -- Bottles
--         elseif (1230777 <= item_id and item_id <= 1230778)
--             or (item_id == 1230831) -- Water Moves
--         then
--             return 56 -- Roysten
--         elseif (1230828 <= item_id and item_id <= 1230830)
--             or (item_id == 1230832)
--             or (1230782 <= item_id and item_id <= 1230785) -- Progressive Moves
--         then
--             return 7 -- Bottles
--         elseif item_id == 1230944 -- Mayahem Temple
--         then
--             return 100 -- Targitzan
--         elseif item_id == 1230945 -- Glitter Gulch Mine
--         then
--             return 39 -- Old King Coal
--         elseif item_id == 1230946 or item_id == 1230795 -- Witchy World
--         then
--             return 31 -- Mr Patch
--         elseif item_id == 1230947 -- Jolly Roger's Lagoon
--         then
--             return 102 -- Lord Woo Fak Fak
--         elseif item_id == 1230948 or item_id == 1230791 -- Terrydactyland
--         then
--             return 49 -- Terry
--         elseif item_id == 1230949 or item_id == 1230790 -- Grunty Industries
--         then
--             return 103 -- Weldar
--         elseif item_id == 1230950 or item_id == 1230793 -- Hailfire Peaks
--         then
--             return 65 -- Chilly Willy
--         elseif item_id == 1230792
--         then
--             return 66
--         elseif item_id == 1230951 -- Cloud Cuckooland
--         then
--             return 27 -- Canary Mary
--         elseif item_id == 1230952 -- Cauldron Keep
--         then
--             return 71 -- Klungo
--         elseif item_id == 1230794 -- Isle O' Hags Station
--         then
--             return 8 -- Mumbo
--         elseif item_id == 1230796 -- Chuffy
--         then
--             return 39 -- Old King Coal
--         elseif 1230855 <= item_id and item_id <= 1230863 -- Mumbo Magic
--         then
--             return 8 -- Mumbo
--         elseif 1230174 <= item_id and item_id <= 1230182 -- Humba Transformations
--         then
--             return 37 -- Humba
--         elseif 1230870 <= item_id and item_id <= 1230876 -- Silos
--         then
--             return 17 -- Jamjars
--         elseif 1230877 <= item_id and item_id <= 1230881 -- Warppad MT
--         then
--             return 100 -- Targitzan
--         elseif 1230882 <= item_id and item_id <= 1230886 -- Warppad GM
--         then
--             return 39 -- Old King Coal
--         elseif 1230887 <= item_id and item_id <= 1230891 -- Warppad WW
--         then
--             return 31 -- Mr Patch
--         elseif 1230892 <= item_id and item_id <= 1230896 -- Warppad JR
--         then
--             return 102 -- Lord Woo Fak Fak
--         elseif 1230897 <= item_id and item_id <= 1230901 -- Warppad TD
--         then
--             return 49 -- Terry
--         elseif 1230902 <= item_id and item_id <= 1230906 -- Warppad GI
--         then
--             return 103 -- Weldar
--         elseif 1230907 <= item_id and item_id <= 1230911 -- Warppad HP
--         then
--             return 65 -- Chilly Willy
--         elseif 1230912 <= item_id and item_id <= 1230915 -- Warppad CC
--         then
--             return 27 -- Canary
--         elseif 1230917 <= item_id and item_id <= 1230921 -- Cheats
--         then
--             return 28 -- Cheato
--         else -- Default
--             return 7 -- Bottles
--         end

--     -- Completely random character
--     elseif DIALOG_CHARACTER == 255
--     then
--         return math.random(0, 109)

--     -- Fixed dialog character has been selected
--     else
--         return DIALOG_CHARACTER
--     end
-- end

-- function messageQueue()
--     local processed = -1;
--     if GVR:getCurrentQueue() == GVR:getPCQueue()
--     then
--         for id, message in pairs(MESSAGE_TABLE)
--         do
--             GVR:setDialog(message[1], message[2])
--             processed = id
--             break
--         end
--         if processed ~= -1
--         then
--             table.remove(MESSAGE_TABLE, processed)
--         else
--             GVR:setSettingDialogCharacter(DIALOG_CHARACTER)
--         end
--     end
-- end

---------------------- ARCHIPELAGO FUNCTIONS -------------

function processAGIItem(item_list)
    for ap_id, memlocation in pairs(item_list) -- Items unrelated to AGI_MAP like Consumables
    do
        -- print(receive_map)
        if receive_map[tostring(ap_id)] == nil
        then
            if(6501001 <= memlocation and memlocation <= 6501009) -- Single Garibs
            then
                received_garibs(memlocation)
            elseif memlocation == 6510001 then -- Garibsanity
                received_garibs(memlocation)
            elseif(memlocation == 6502001) -- Atlantis 1 Single Garibs
            then
                received_garibs(memlocation)
            elseif(6500190 <= memlocation and memlocation <= 6500196) -- Atlantis 1 Garib Packs
            then
                received_garibs(memlocation)
            elseif(6500190 <= memlocation and memlocation <= 6501906) -- Moves and Balls
            then
                received_moves(memlocation)
            elseif(6500357 <= memlocation and memlocation <= 6500357) -- Misc
            then
                received_misc(memlocation)
            end
            receive_map[tostring(ap_id)] = tostring(memlocation)
        end
    end
end

function process_block(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    if block['slot_player'] ~= nil
    then
        return
    end
    if next(block['items']) ~= nil
    then
        processAGIItem(block['items'])
    end
    -- if next(block['messages']) ~= nil
    -- then
    --     local msg = ""
    --     for k, msg_table in pairs(block['messages'])
    --     do
    --         display_item_message(msg_table)
    --     end
    -- end
    -- if block['triggerDeath'] == true and DEATH_LINK == true
    -- then
    --     local death = GVR:getAPDeath()
    --     GVR:setAPDeath(death + 1)
    --     local randomDeathMsg = DEATH_MESSAGES[math.random(1, #DEATH_MESSAGES)]["message"]
    --     table.insert(MESSAGE_TABLE, {randomDeathMsg, 15})
    -- end
    -- if block['triggerTag'] == true and TAG_LINK == true
    -- then
    --     local tag = GVR:getAPTag()
    --     GVR:setAPTag(tag + 1)
    -- end
end

function SendToClient()
    local retTable = {}
    local detect_death = false
    local detect_tag = false
    -- print(GVR:getNLocalDeath())
    -- print(GVR:getPCDeath())
    -- if GVR:getPCDeath() ~= GVR:getNLocalDeath() and DEATH_LINK == false
    -- then
    --     local randomDeathMsg = DEATH_MESSAGES[math.random(1, #DEATH_MESSAGES)]["message"]
    --     table.insert(MESSAGE_TABLE, {randomDeathMsg, 15})
    --     local died = GVR:getPCDeath()
    --     GVR:setPCDeath(died + 1)
    -- end
    -- if GVR:getPCDeath() ~= GVR:getNLocalDeath() and DEATH_LINK == true and DEATH_LINK_TRIGGERED == false
    -- then
    --     detect_death = true
    --     local died = GVR:getPCDeath()
    --     GVR:setPCDeath(died + 1)
    --     DEATH_LINK_TRIGGERED = true
    --     local randomDeathMsg = DEATH_MESSAGES[math.random(1, #DEATH_MESSAGES)]["message"]
    --     table.insert(MESSAGE_TABLE, {randomDeathMsg, 15})
    -- else
    --     DEATH_LINK_TRIGGERED = false
    -- end

    -- if GVR:getPCTag() ~= GVR:getNLocalTag() and TAG_LINK == false
    -- then
    --     local tag = GVR:getPCTag()
    --     GVR:setPCTag(tag + 1)
    -- end
    -- if GVR:getPCTag() ~= GVR:getNLocalTag() and TAG_LINK == true and TAG_LINK_TRIGGERED == false
    -- then
    --     detect_tag = true
    --     local tag = GVR:getPCTag()
    --     GVR:setPCTag(tag + 1)
    --     TAG_LINK_TRIGGERED = true
    -- else
    --     TAG_LINK_TRIGGERED = false
    -- end
    retTable["scriptVersion"] = SCRIPT_VERSION;
    retTable["playerName"] = PLAYER;
    retTable["deathlinkActive"] = DEATH_LINK;
    retTable["taglinkActive"] = TAG_LINK;
    retTable["isDead"] = detect_death;
    retTable["isTag"] = detect_tag;
    retTable["garibs"] = garib_check()
    retTable["life"] = life_check()
    retTable["tip"] = tip_check()
    retTable["checkpoint"] = checkpoint_check()
    retTable["switch"] = switch_check()
    retTable["enemy_garibs"] = enemy_garib_check()

    retTable["DEMO"] = false;
    retTable["sync_ready"] = "true"

    if CURRENT_MAP == nil
    then
        retTable["glover_world"] = 0x0;
        retTable["glover_hub"] = 0x0D;
    else
        retTable["glover_world"] = CURRENT_MAP;
        retTable["glover_hub"] = CURRENT_HUB;
    end

    local msg = json.encode(retTable).."\n"
    local ret, error = BT_SOCK:send(msg)
    if ret == nil then
        print(error)
    elseif CUR_STATE == STATE_INITIAL_CONNECTION_MADE then
        CUR_STATE = STATE_TENTATIVELY_CONNECTED
    elseif CUR_STATE == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        PRINT_GOAL = true;
        CUR_STATE = STATE_OK
    end
    -- if DETECT_DEATH == true
    -- then
    --     DETECT_DEATH = false
    -- end
end

function receive()
    if PLAYER == "" and SEED == 0
    then
        getSlotData()
    else
        -- Send the message
        SendToClient()

        l, e = BT_SOCK:receive()
        -- Handle incoming message
        if e == 'closed' then
            if CUR_STATE == STATE_OK then
                table.insert(MESSAGE_TABLE, {"Archipelago Connection Closed", 86});
                print("Connection closed")
            end
            CUR_STATE = STATE_UNINITIALIZED
            return
        elseif e == 'timeout' then
            AP_TIMEOUT_COUNTER = AP_TIMEOUT_COUNTER + 1
            if AP_TIMEOUT_COUNTER == 5
            then
                table.insert(MESSAGE_TABLE, {"Archipelago Timeout", 86});
                AP_TIMEOUT_COUNTER = 0
            end
            print("timeout")
            return
        elseif e ~= nil then
            -- print(e)
            CUR_STATE = STATE_UNINITIALIZED
            return
        end
        AP_TIMEOUT_COUNTER = 0
        process_block(json.decode(l))
    end
end

function getSlotData()
    local retTable = {}
    retTable["getSlot"] = true;
    local msg = json.encode(retTable).."\n"
    local ret, error = BT_SOCK:send(msg)
    l, e = BT_SOCK:receive()
    -- Handle incoming message
    if e == 'closed' then
        if CUR_STATE == STATE_OK then
            table.insert(MESSAGE_TABLE, {"Archipelago Connection Closed", 86});
            print("Connection closed")
        end
        CUR_STATE = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        AP_TIMEOUT_COUNTER = AP_TIMEOUT_COUNTER + 1
        if AP_TIMEOUT_COUNTER == 10
        then
            table.insert(MESSAGE_TABLE, {"Archipelago Timeout", 86});
            AP_TIMEOUT_COUNTER = 0
        end
        print("timeout")
        return
    elseif e ~= nil then
        -- print(e)
        CUR_STATE = STATE_UNINITIALIZED
        return
    end
    AP_TIMEOUT_COUNTER = 0
    process_slot(json.decode(l))
end

function process_slot(block)
    if block['slot_player'] ~= nil and block['slot_player'] ~= ""
    then
        PLAYER = block['slot_player']
    end
    if block['slot_seed'] ~= nil and block['slot_seed'] ~= ""
    then
        SEED = block['slot_seed']
    end
    if block['slot_garib_logic'] ~= nil
    then
        GVR:setGaribLogic(block['slot_garib_logic'])
    end
    if block['slot_garib_sorting'] ~= nil
    then
        GVR:setGaribSorting(block['slot_garib_sorting'])
    end
    -- if block['slot_deathlink'] ~= nil and block['slot_deathlink'] ~= 0
    -- then
    --     DEATH_LINK = true
    -- end
    -- if block['slot_taglink'] ~= nil and block['slot_taglink'] ~= 0
    -- then
    --     TAG_LINK = true
    -- end
    if block['slot_version'] ~= nil and block['slot_version'] ~= ""
    then
        CLIENT_VERSION = block['slot_version']
        if CLIENT_VERSION ~= GVR_VERSION
        then
            VERROR = true
            return false
        end
        local checked = false
        while(checked == false)
        do
            local ROMversion = GVR:getRomVersion()
            if ROMversion ~= "0"
            then
                if ROMversion ~= CLIENT_VERSION
                then
                    VERROR = true
                    return false
                end
                checked = true
            end
            emu.frameadvance()
        end
    end
    return true
end

---------------------- MAIN LUA LOOP -------------------------

function main()
    local bizhawk_version = client.getversion()
    local bizhawk_major, bizhawk_minor, bizhawk_patch = bizhawk_version:match("(%d+)%.(%d+)%.?(%d*)")
    bizhawk_major = tonumber(bizhawk_major)
    bizhawk_minor = tonumber(bizhawk_minor)
    if bizhawk_major == 2 and bizhawk_minor <= 9
    then
        print("We only support Bizhawk Version 2.10 and newer. Please download Bizhawk version 2.10")
        return
    end
    print("Glover Archipelago Version " .. GVR_VERSION)
    GVR = GLOVERHACK:new(nil)
    local check = 0
    while GLOVERHACK:getSettingPointer() == nil
    do
        check = check + 1
        if(check == 275 and GVR:getRomVersion() == "0")
        then
            print("This is the vanilla rom. Please use the patched version of Glover-AP.")
            return
        end
        emu.frameadvance()
    end
    server, error = socket.bind('localhost', 21223)
    local changed_map = 0x0
    while true do
        FRAME = FRAME + 1
        if not (CUR_STATE == PREV_STATE) then
            PREV_STATE = CUR_STATE
        end
        if (CUR_STATE == STATE_OK) or (CUR_STATE == STATE_INITIAL_CONNECTION_MADE) or (CUR_STATE == STATE_TENTATIVELY_CONNECTED) then
            if (FRAME % 30 == 1) then
                CURRENT_MAP = GVR:getWorldMap()
                CURRENT_HUB = GVR:getHubMap()
                map_handler();
                receive();
                --messageQueue();
                if VERROR == true
                then
                    print("ERROR: version mismatch. Please obtain the same version for everything")
                    print("The versions that you are currently using are:")
                    print("Connector Version: " .. GVR_VERSION)
                    print("Client Version: " .. CLIENT_VERSION)
                    print("ROM Version: " .. GVR:getRomVersion())
                    return
                end
                if changed_map ~= CURRENT_MAP
                then
                    client.saveram()
                    changed_map = CURRENT_MAP
                end
            end
        elseif (CUR_STATE == STATE_UNINITIALIZED) then
            if  (FRAME % 60 == 1) then
                server:settimeout(0)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    CUR_STATE = STATE_INITIAL_CONNECTION_MADE
                    BT_SOCK = client
                    BT_SOCK:settimeout(0)
                end
            end
        end
        emu.frameadvance()
    end
end

main()
