-- Glover Connector Lua
-- Created by Mike Jackson (jjjj12212) and Smg065

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

local GLV_SOCK = nil

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

-------------- GARIB LOGIC -----------

local GARIB_GROUPS = false
local GARIB_ORDER = {}

-------------- TOTALS VARS -----------
local TOTAL_LIVES = 0;
local TOTAL_SINGLE_GARIBS = 0;
local TOTAL_WORLD_GARIBS = {
	['AP_ATLANTIS_L1_GARIBS'] = 0,
	['AP_ATLANTIS_L2_GARIBS'] = 0,
	['AP_ATLANTIS_L3_GARIBS'] = 0,
	['AP_ATLANTIS_BONUS_GARIBS'] = 0,
	['AP_CARNIVAL_L1_GARIBS'] = 0,
	['AP_CARNIVAL_L2_GARIBS'] = 0,
	['AP_CARNIVAL_L3_GARIBS'] = 0,
	['AP_CARNIVAL_BONUS_GARIBS'] = 0,
	['AP_PIRATES_L1_GARIBS'] = 0,
	['AP_PIRATES_L2_GARIBS'] = 0,
	['AP_PIRATES_L3_GARIBS'] = 0,
	['AP_PIRATES_BONUS_GARIBS'] = 0,
	['AP_PREHISTORIC_L1_GARIBS'] = 0,
	['AP_PREHISTORIC_L2_GARIBS'] = 0,
	['AP_PREHISTORIC_L3_GARIBS'] = 0,
	['AP_PREHISTORIC_BONUS_GARIBS'] = 0,
	['AP_FORTRESS_L1_GARIBS'] = 0,
	['AP_FORTRESS_L2_GARIBS'] = 0,
	['AP_FORTRESS_L3_GARIBS'] = 0,
	['AP_FORTRESS_BONUS_GARIBS'] = 0,
	['AP_SPACE_L1_GARIBS'] = 0,
	['AP_SPACE_L2_GARIBS'] = 0,
	['AP_SPACE_L3_GARIBS'] = 0,
	['AP_SPACE_BONUS_GARIBS'] = 0
};
local MAX_WORLD_GARIBS = {
	['AP_ATLANTIS_L1_GARIBS'] = 50,
	['AP_ATLANTIS_L2_GARIBS'] = 60,
	['AP_ATLANTIS_L3_GARIBS'] = 80,
	['AP_ATLANTIS_BONUS_GARIBS'] = 25,
	['AP_CARNIVAL_L1_GARIBS'] = 65,
	['AP_CARNIVAL_L2_GARIBS'] = 80,
	['AP_CARNIVAL_L3_GARIBS'] = 80,
	['AP_CARNIVAL_BONUS_GARIBS'] = 20,
	['AP_PIRATES_L1_GARIBS'] = 70,
	['AP_PIRATES_L2_GARIBS'] = 60,
	['AP_PIRATES_L3_GARIBS'] = 80,
	['AP_PIRATES_BONUS_GARIBS'] = 50,
	['AP_PREHISTORIC_L1_GARIBS'] = 80,
	['AP_PREHISTORIC_L2_GARIBS'] = 80,
	['AP_PREHISTORIC_L3_GARIBS'] = 80,
	['AP_PREHISTORIC_BONUS_GARIBS'] = 60,
	['AP_FORTRESS_L1_GARIBS'] = 60,
	['AP_FORTRESS_L2_GARIBS'] = 60,
	['AP_FORTRESS_L3_GARIBS'] = 70,
	['AP_FORTRESS_BONUS_GARIBS'] = 56,
	['AP_SPACE_L1_GARIBS'] = 50,
	['AP_SPACE_L2_GARIBS'] = 50,
	['AP_SPACE_L3_GARIBS'] = 80,
	['AP_SPACE_BONUS_GARIBS'] = 50
};


--------------- DEATH LINK ----------------------
local DEATH_LINK_TRIGGERED = false;
local DEATH_LINK = true

--------------- TAG LINK ------------------------
local TAG_LINK_TRIGGERED = false
local TAG_LINK = true

local checked_map = { -- [ap_id] = location_id; -- Stores locations you've already checked
	["NA"] = "NA"
}

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
    "AP_RUBBER_BALL",
    "AP_BOWLING_BALL",
    "AP_POWER_BALL",
    "AP_BEARING_BALL",
    "AP_CRYSTAL_BALL",
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
    "AP_SPEED_POTION",
    "AP_STICKY_POTION",
    "AP_FROG_POTION",
    "AP_BOOMERANG_POTION",
    "AP_HELICOPTER_POTION",
    "AP_ATLANTIS_L1_GATE",
    "AP_ATLANTIS_L2_RAISE_WATER",
    "AP_ATLANTIS_L2_WATER_DRAIN",
    "AP_ATLANTIS_L2_GATE",
    "AP_ATLANTIS_L3_SPIN_WHEEL",
    "AP_ATLANTIS_L3_CAVE",
    "AP_CARNIVAL_L1_CONVEYOR",
    "AP_CARNIVAL_L1_GATE",
    "AP_CARNIVAL_L1_DOORA",
    "AP_CARNIVAL_L1_DOORB",
    "AP_CARNIVAL_L1_DOORC",
    "AP_CARNIVAL_L1_ROCKET_RAMP",
    "AP_CARNIVAL_L2_TEETH",
    "AP_CARNIVAL_L2_FAN",
    "AP_MAX_ITEM",
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
    "AP_TRAINING_WORLD",
    "AP_MAX_WORLDS"
};

for index, item in pairs(ROM_WORLDS_TABLE)
do
    WORLDS_TABLE[item] = index
end


-- Address Map for Glover
local ADDRESS_MAP = {
	["AP_ATLANTIS_L1"] = {
		["GOAL"] = "66",
		["GARIBS"] = {
			["1"] = {
				['id'] = 0x001,
				['offset'] = 0,
			},
			["2"] = {
				['id'] = 0x002,
				['offset'] = 1,
			},
			["3"] = {
				['id'] = 0x003,
				['offset'] = 2,
			},
			["4"] = {
				['id'] = 0x004,
				['offset'] = 3,
			},
			["5"] = {
				['id'] = 0x005,
				['offset'] = 4,
			},
			["6"] = {
				['id'] = 0x006,
				['offset'] = 5,
			},
			["7"] = {
				['id'] = 0x007,
				['offset'] = 6,
			},
			["8"] = {
				['id'] = 0x008,
				['offset'] = 7,
			},
			["9"] = {
				['id'] = 0x009,
				['offset'] = 8,
			},
			["10"] = {
				['id'] = 0x00A,
				['offset'] = 9,
			},
			["11"] = {
				['id'] = 0x00B,
				['offset'] = 10,
			},
			["12"] = {
				['id'] = 0x00C,
				['offset'] = 11,
			},
			["13"] = {
				['id'] = 0x00D,
				['offset'] = 12,
			},
			["14"] = {
				['id'] = 0x00E,
				['offset'] = 13,
			},
			["15"] = {
				['id'] = 0x00F,
				['offset'] = 14,
			},
			["16"] = {
				['id'] = 0x010,
				['offset'] = 15,
			},
			["17"] = {
				['id'] = 0x011,
				['offset'] = 16,
			},
			["18"] = {
				['id'] = 0x012,
				['offset'] = 17,
			},
			["19"] = {
				['id'] = 0x013,
				['offset'] = 18,
			},
			["20"] = {
				['id'] = 0x014,
				['offset'] = 19,
			},
			["21"] = {
				['id'] = 0x015,
				['offset'] = 20,
			},
			["22"] = {
				['id'] = 0x016,
				['offset'] = 21,
			},
			["23"] = {
				['id'] = 0x017,
				['offset'] = 22,
			},
			["24"] = {
				['id'] = 0x018,
				['offset'] = 23,
			},
			["25"] = {
				['id'] = 0x019,
				['offset'] = 24,
			},
			["26"] = {
				['id'] = 0x01A,
				['offset'] = 25,
			},
			["27"] = {
				['id'] = 0x01B,
				['offset'] = 26,
			},
			["28"] = {
				['id'] = 0x01C,
				['offset'] = 27,
			},
			["29"] = {
				['id'] = 0x01D,
				['offset'] = 28,
			},
			["30"] = {
				['id'] = 0x01E,
				['offset'] = 29,
			},
			["31"] = {
				['id'] = 0x01F,
				['offset'] = 30,
			},
			["32"] = {
				['id'] = 0x020,
				['offset'] = 31,
			},
			["33"] = {
				['id'] = 0x021,
				['offset'] = 32,
			},
			["34"] = {
				['id'] = 0x022,
				['offset'] = 33,
			},
			["35"] = {
				['id'] = 0x023,
				['offset'] = 34,
			},
			["36"] = {
				['id'] = 0x024,
				['offset'] = 35,
			},
			["37"] = {
				['id'] = 0x025,
				['offset'] = 36,
			},
			["38"] = {
				['id'] = 0x026,
				['offset'] = 37,
			},
			["39"] = {
				['id'] = 0x027,
				['offset'] = 38,
			},
			["40"] = {
				['id'] = 0x028,
				['offset'] = 39,
			},
			["41"] = {
				['id'] = 0x029,
				['offset'] = 40,
			},
			["42"] = {
				['id'] = 0x02A,
				['offset'] = 41,
			},
			["43"] = {
				['id'] = 0x02B,
				['offset'] = 42,
			},
			["44"] = {
				['id'] = 0x02C,
				['offset'] = 43,
			},
			["45"] = {
				['id'] = 0x02D,
				['offset'] = 44,
			},
			["46"] = {
				['id'] = 0x02E,
				['offset'] = 45,
			},
			["47"] = {
				['id'] = 0x02F,
				['offset'] = 46,
			},
			["48"] = {
				['id'] = 0x030,
				['offset'] = 47,
			},
			["49"] = {
				['id'] = 0x031,
				['offset'] = 48,
			},
		},
		["ENEMY_GARIBS"] = {
			["50"] = {
				['id'] = 0x032,
				['offset'] = 49,
				['object_id'] = 0x033,
			},
		},
		["ENEMIES"] = {
			["51"] = {
				['id'] = 0x033,
				['offset'] = 0,
			},
			["52"] = {
				['id'] = 0x034,
				['offset'] = 1,
			},
			["53"] = {
				['id'] = 0x035,
				['offset'] = 2,
			},
			["54"] = {
				['id'] = 0x036,
				['offset'] = 3,
			},
		},
		["LIFE"] = {
			["55"] = {
				['id'] = 0x037,
				['offset'] = 0,
			},
			["56"] = {
				['id'] = 0x038,
				['offset'] = 1,
			},
			["57"] = {
				['id'] = 0x039,
				['offset'] = 2,
			},
		},
		["TIP"] = {
			["58"] = {
				['id'] = 0x03A,
				['offset'] = 0,
			},
			["59"] = {
				['id'] = 0x03B,
				['offset'] = 1,
			},
			["60"] = {
				['id'] = 0x03C,
				['offset'] = 2,
			},
			["61"] = {
				['id'] = 0x03D,
				['offset'] = 3,
			},
			["62"] = {
				['id'] = 0x03E,
				['offset'] = 4,
			},
		},
		["CHECKPOINT"] = {
			["63"] = {
				['id'] = 0x03F,
				['offset'] = 0,
			},
			["64"] = {
				['id'] = 0x040,
				['offset'] = 1,
			},
		},
		["SWITCH"] = {
			["65"] = {
				['id'] = 0x041,
				['offset'] = 0,
			},
		},
	},
	["AP_ATLANTIS_L2"] = {
		["GOAL"] = "141",
		["GARIBS"] = {
			["67"] = {
				['id'] = 0x043,
				['offset'] = 0,
			},
			["68"] = {
				['id'] = 0x044,
				['offset'] = 1,
			},
			["69"] = {
				['id'] = 0x045,
				['offset'] = 2,
			},
			["70"] = {
				['id'] = 0x046,
				['offset'] = 3,
			},
			["71"] = {
				['id'] = 0x047,
				['offset'] = 4,
			},
			["72"] = {
				['id'] = 0x048,
				['offset'] = 5,
			},
			["73"] = {
				['id'] = 0x049,
				['offset'] = 6,
			},
			["74"] = {
				['id'] = 0x04A,
				['offset'] = 7,
			},
			["75"] = {
				['id'] = 0x04B,
				['offset'] = 8,
			},
			["76"] = {
				['id'] = 0x04C,
				['offset'] = 9,
			},
			["77"] = {
				['id'] = 0x04D,
				['offset'] = 10,
			},
			["78"] = {
				['id'] = 0x04E,
				['offset'] = 11,
			},
			["79"] = {
				['id'] = 0x04F,
				['offset'] = 12,
			},
			["80"] = {
				['id'] = 0x050,
				['offset'] = 13,
			},
			["81"] = {
				['id'] = 0x051,
				['offset'] = 14,
			},
			["82"] = {
				['id'] = 0x052,
				['offset'] = 15,
			},
			["83"] = {
				['id'] = 0x053,
				['offset'] = 16,
			},
			["84"] = {
				['id'] = 0x054,
				['offset'] = 17,
			},
			["85"] = {
				['id'] = 0x055,
				['offset'] = 18,
			},
			["86"] = {
				['id'] = 0x056,
				['offset'] = 19,
			},
			["87"] = {
				['id'] = 0x057,
				['offset'] = 20,
			},
			["88"] = {
				['id'] = 0x058,
				['offset'] = 21,
			},
			["89"] = {
				['id'] = 0x059,
				['offset'] = 22,
			},
			["90"] = {
				['id'] = 0x05A,
				['offset'] = 23,
			},
			["91"] = {
				['id'] = 0x05B,
				['offset'] = 24,
			},
			["92"] = {
				['id'] = 0x05C,
				['offset'] = 25,
			},
			["93"] = {
				['id'] = 0x05D,
				['offset'] = 26,
			},
			["94"] = {
				['id'] = 0x05E,
				['offset'] = 27,
			},
			["95"] = {
				['id'] = 0x05F,
				['offset'] = 28,
			},
			["96"] = {
				['id'] = 0x060,
				['offset'] = 29,
			},
			["97"] = {
				['id'] = 0x061,
				['offset'] = 30,
			},
			["98"] = {
				['id'] = 0x062,
				['offset'] = 31,
			},
			["99"] = {
				['id'] = 0x063,
				['offset'] = 32,
			},
			["100"] = {
				['id'] = 0x064,
				['offset'] = 33,
			},
			["101"] = {
				['id'] = 0x065,
				['offset'] = 34,
			},
			["102"] = {
				['id'] = 0x066,
				['offset'] = 35,
			},
			["103"] = {
				['id'] = 0x067,
				['offset'] = 36,
			},
			["104"] = {
				['id'] = 0x068,
				['offset'] = 37,
			},
			["105"] = {
				['id'] = 0x069,
				['offset'] = 38,
			},
			["106"] = {
				['id'] = 0x06A,
				['offset'] = 39,
			},
			["107"] = {
				['id'] = 0x06B,
				['offset'] = 40,
			},
			["108"] = {
				['id'] = 0x06C,
				['offset'] = 41,
			},
			["109"] = {
				['id'] = 0x06D,
				['offset'] = 42,
			},
			["110"] = {
				['id'] = 0x06E,
				['offset'] = 43,
			},
			["111"] = {
				['id'] = 0x06F,
				['offset'] = 44,
			},
			["112"] = {
				['id'] = 0x070,
				['offset'] = 45,
			},
			["113"] = {
				['id'] = 0x071,
				['offset'] = 46,
			},
			["114"] = {
				['id'] = 0x072,
				['offset'] = 47,
			},
			["115"] = {
				['id'] = 0x073,
				['offset'] = 48,
			},
			["116"] = {
				['id'] = 0x074,
				['offset'] = 49,
			},
			["117"] = {
				['id'] = 0x075,
				['offset'] = 50,
			},
			["118"] = {
				['id'] = 0x076,
				['offset'] = 51,
			},
			["119"] = {
				['id'] = 0x077,
				['offset'] = 52,
			},
			["120"] = {
				['id'] = 0x078,
				['offset'] = 53,
			},
		},
		["ENEMY_GARIBS"] = {
			["121"] = {
				['id'] = 0x079,
				['offset'] = 54,
				['object_id'] = 0x07F,
			},
			["122"] = {
				['id'] = 0x07A,
				['offset'] = 55,
				['object_id'] = 0x080,
			},
			["123"] = {
				['id'] = 0x07B,
				['offset'] = 56,
				['object_id'] = 0x081,
			},
			["124"] = {
				['id'] = 0x07C,
				['offset'] = 57,
				['object_id'] = 0x082,
			},
			["125"] = {
				['id'] = 0x07D,
				['offset'] = 58,
				['object_id'] = 0x083,
			},
			["126"] = {
				['id'] = 0x07E,
				['offset'] = 59,
				['object_id'] = 0x084,
			},
		},
		["ENEMIES"] = {
			["127"] = {
				['id'] = 0x07F,
				['offset'] = 0,
			},
			["128"] = {
				['id'] = 0x080,
				['offset'] = 1,
			},
			["129"] = {
				['id'] = 0x081,
				['offset'] = 2,
			},
			["130"] = {
				['id'] = 0x082,
				['offset'] = 3,
			},
			["131"] = {
				['id'] = 0x083,
				['offset'] = 4,
			},
			["132"] = {
				['id'] = 0x084,
				['offset'] = 5,
			},
		},
		["LIFE"] = {
			["133"] = {
				['id'] = 0x085,
				['offset'] = 0,
			},
		},
		["TIP"] = {
			["134"] = {
				['id'] = 0x086,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			["135"] = {
				['id'] = 0x087,
				['offset'] = 0,
			},
			["136"] = {
				['id'] = 0x088,
				['offset'] = 1,
			},
			["137"] = {
				['id'] = 0x089,
				['offset'] = 2,
			},
		},
		["SWITCH"] = {
			["138"] = {
				['id'] = 0x08A,
				['offset'] = 0,
			},
			["139"] = {
				['id'] = 0x08B,
				['offset'] = 1,
			},
			["140"] = {
				['id'] = 0x08C,
				['offset'] = 2,
			},
		},
		["POTIONS"] = {
			["142"] = {
				['id'] = 0x08E,
				['offset'] = 0,
			},
		},
	},
	["AP_ATLANTIS_L3"] = {
		["GOAL"] = "248",
		["GARIBS"] = {
			["143"] = {
				['id'] = 0x08F,
				['offset'] = 0,
			},
			["144"] = {
				['id'] = 0x090,
				['offset'] = 1,
			},
			["145"] = {
				['id'] = 0x091,
				['offset'] = 2,
			},
			["146"] = {
				['id'] = 0x092,
				['offset'] = 3,
			},
			["147"] = {
				['id'] = 0x093,
				['offset'] = 4,
			},
			["148"] = {
				['id'] = 0x094,
				['offset'] = 5,
			},
			["149"] = {
				['id'] = 0x095,
				['offset'] = 6,
			},
			["150"] = {
				['id'] = 0x096,
				['offset'] = 7,
			},
			["151"] = {
				['id'] = 0x097,
				['offset'] = 8,
			},
			["152"] = {
				['id'] = 0x098,
				['offset'] = 9,
			},
			["153"] = {
				['id'] = 0x099,
				['offset'] = 10,
			},
			["154"] = {
				['id'] = 0x09A,
				['offset'] = 11,
			},
			["155"] = {
				['id'] = 0x09B,
				['offset'] = 12,
			},
			["156"] = {
				['id'] = 0x09C,
				['offset'] = 13,
			},
			["157"] = {
				['id'] = 0x09D,
				['offset'] = 14,
			},
			["158"] = {
				['id'] = 0x09E,
				['offset'] = 15,
			},
			["159"] = {
				['id'] = 0x09F,
				['offset'] = 16,
			},
			["160"] = {
				['id'] = 0x0A0,
				['offset'] = 17,
			},
			["161"] = {
				['id'] = 0x0A1,
				['offset'] = 18,
			},
			["162"] = {
				['id'] = 0x0A2,
				['offset'] = 19,
			},
			["163"] = {
				['id'] = 0x0A3,
				['offset'] = 20,
			},
			["164"] = {
				['id'] = 0x0A4,
				['offset'] = 21,
			},
			["165"] = {
				['id'] = 0x0A5,
				['offset'] = 22,
			},
			["166"] = {
				['id'] = 0x0A6,
				['offset'] = 23,
			},
			["167"] = {
				['id'] = 0x0A7,
				['offset'] = 24,
			},
			["168"] = {
				['id'] = 0x0A8,
				['offset'] = 25,
			},
			["169"] = {
				['id'] = 0x0A9,
				['offset'] = 26,
			},
			["170"] = {
				['id'] = 0x0AA,
				['offset'] = 27,
			},
			["171"] = {
				['id'] = 0x0AB,
				['offset'] = 28,
			},
			["172"] = {
				['id'] = 0x0AC,
				['offset'] = 29,
			},
			["173"] = {
				['id'] = 0x0AD,
				['offset'] = 30,
			},
			["174"] = {
				['id'] = 0x0AE,
				['offset'] = 31,
			},
			["175"] = {
				['id'] = 0x0AF,
				['offset'] = 32,
			},
			["176"] = {
				['id'] = 0x0B0,
				['offset'] = 33,
			},
			["177"] = {
				['id'] = 0x0B1,
				['offset'] = 34,
			},
			["178"] = {
				['id'] = 0x0B2,
				['offset'] = 35,
			},
			["179"] = {
				['id'] = 0x0B3,
				['offset'] = 36,
			},
			["180"] = {
				['id'] = 0x0B4,
				['offset'] = 37,
			},
			["181"] = {
				['id'] = 0x0B5,
				['offset'] = 38,
			},
			["182"] = {
				['id'] = 0x0B6,
				['offset'] = 39,
			},
			["183"] = {
				['id'] = 0x0B7,
				['offset'] = 40,
			},
			["184"] = {
				['id'] = 0x0B8,
				['offset'] = 41,
			},
			["185"] = {
				['id'] = 0x0B9,
				['offset'] = 42,
			},
			["186"] = {
				['id'] = 0x0BA,
				['offset'] = 43,
			},
			["187"] = {
				['id'] = 0x0BB,
				['offset'] = 44,
			},
			["188"] = {
				['id'] = 0x0BC,
				['offset'] = 45,
			},
			["189"] = {
				['id'] = 0x0BD,
				['offset'] = 46,
			},
			["190"] = {
				['id'] = 0x0BE,
				['offset'] = 47,
			},
			["191"] = {
				['id'] = 0x0BF,
				['offset'] = 48,
			},
			["192"] = {
				['id'] = 0x0C0,
				['offset'] = 49,
			},
			["193"] = {
				['id'] = 0x0C1,
				['offset'] = 50,
			},
			["194"] = {
				['id'] = 0x0C2,
				['offset'] = 51,
			},
			["195"] = {
				['id'] = 0x0C3,
				['offset'] = 52,
			},
			["196"] = {
				['id'] = 0x0C4,
				['offset'] = 53,
			},
			["197"] = {
				['id'] = 0x0C5,
				['offset'] = 54,
			},
			["198"] = {
				['id'] = 0x0C6,
				['offset'] = 55,
			},
			["199"] = {
				['id'] = 0x0C7,
				['offset'] = 56,
			},
			["200"] = {
				['id'] = 0x0C8,
				['offset'] = 57,
			},
			["201"] = {
				['id'] = 0x0C9,
				['offset'] = 58,
			},
			["202"] = {
				['id'] = 0x0CA,
				['offset'] = 59,
			},
			["203"] = {
				['id'] = 0x0CB,
				['offset'] = 60,
			},
			["204"] = {
				['id'] = 0x0CC,
				['offset'] = 61,
			},
			["205"] = {
				['id'] = 0x0CD,
				['offset'] = 62,
			},
			["206"] = {
				['id'] = 0x0CE,
				['offset'] = 63,
			},
			["207"] = {
				['id'] = 0x0CF,
				['offset'] = 64,
			},
			["208"] = {
				['id'] = 0x0D0,
				['offset'] = 65,
			},
			["209"] = {
				['id'] = 0x0D1,
				['offset'] = 66,
			},
			["210"] = {
				['id'] = 0x0D2,
				['offset'] = 67,
			},
			["211"] = {
				['id'] = 0x0D3,
				['offset'] = 68,
			},
		},
		["ENEMY_GARIBS"] = {
			["212"] = {
				['id'] = 0x0D4,
				['offset'] = 69,
				['object_id'] = 0x0DF,
			},
			["213"] = {
				['id'] = 0x0D5,
				['offset'] = 70,
				['object_id'] = 0x0E0,
			},
			["214"] = {
				['id'] = 0x0D6,
				['offset'] = 71,
				['object_id'] = 0x0E1,
			},
			["215"] = {
				['id'] = 0x0D7,
				['offset'] = 72,
				['object_id'] = 0x0E5,
			},
			["216"] = {
				['id'] = 0x0D8,
				['offset'] = 73,
				['object_id'] = 0x0E6,
			},
			["217"] = {
				['id'] = 0x0D9,
				['offset'] = 74,
				['object_id'] = 0x0E7,
			},
			["218"] = {
				['id'] = 0x0DA,
				['offset'] = 75,
				['object_id'] = 0x0E8,
			},
			["219"] = {
				['id'] = 0x0DB,
				['offset'] = 76,
				['object_id'] = 0x0E9,
			},
			["220"] = {
				['id'] = 0x0DC,
				['offset'] = 77,
				['object_id'] = 0x0EA,
			},
			["221"] = {
				['id'] = 0x0DD,
				['offset'] = 78,
				['object_id'] = 0x0EB,
			},
			["222"] = {
				['id'] = 0x0DE,
				['offset'] = 79,
				['object_id'] = 0x0EC,
			},
		},
		["ENEMIES"] = {
			["223"] = {
				['id'] = 0x0DF,
				['offset'] = 0,
			},
			["224"] = {
				['id'] = 0x0E0,
				['offset'] = 1,
			},
			["225"] = {
				['id'] = 0x0E1,
				['offset'] = 2,
			},
			["226"] = {
				['id'] = 0x0E2,
				['offset'] = 3,
			},
			["227"] = {
				['id'] = 0x0E3,
				['offset'] = 4,
			},
			["228"] = {
				['id'] = 0x0E4,
				['offset'] = 5,
			},
			["229"] = {
				['id'] = 0x0E5,
				['offset'] = 6,
			},
			["230"] = {
				['id'] = 0x0E6,
				['offset'] = 7,
			},
			["231"] = {
				['id'] = 0x0E7,
				['offset'] = 8,
			},
			["232"] = {
				['id'] = 0x0E8,
				['offset'] = 9,
			},
			["233"] = {
				['id'] = 0x0E9,
				['offset'] = 10,
			},
			["234"] = {
				['id'] = 0x0EA,
				['offset'] = 11,
			},
			["235"] = {
				['id'] = 0x0EB,
				['offset'] = 12,
			},
			["236"] = {
				['id'] = 0x0EC,
				['offset'] = 13,
			},
		},
		["LIFE"] = {
			["237"] = {
				['id'] = 0x0ED,
				['offset'] = 0,
			},
			["238"] = {
				['id'] = 0x0EE,
				['offset'] = 1,
			},
			["239"] = {
				['id'] = 0x0EF,
				['offset'] = 2,
			},
			["240"] = {
				['id'] = 0x0F0,
				['offset'] = 3,
			},
			["241"] = {
				['id'] = 0x0F1,
				['offset'] = 4,
			},
		},
		["CHECKPOINT"] = {
			["242"] = {
				['id'] = 0x0F2,
				['offset'] = 0,
			},
			["243"] = {
				['id'] = 0x0F3,
				['offset'] = 1,
			},
			["244"] = {
				['id'] = 0x0F4,
				['offset'] = 2,
			},
		},
		["SWITCH"] = {
			["245"] = {
				['id'] = 0x0F5,
				['offset'] = 0,
			},
			["246"] = {
				['id'] = 0x0F6,
				['offset'] = 1,
			},
			["247"] = {
				['id'] = 0x0F7,
				['offset'] = 2,
			},
		},
		["POTIONS"] = {
			["249"] = {
				['id'] = 0x0F9,
				['offset'] = 0,
			},
			["250"] = {
				['id'] = 0x0FA,
				['offset'] = 1,
			},
		},
	},
	["AP_ATLANTIS_BOSS"] = {
		["GOAL"] = "251",
	},
	["AP_ATLANTIS_BONUS"] = {
		["GOAL"] = "281",
		["GARIBS"] = {
			["252"] = {
				['id'] = 0x0FC,
				['offset'] = 0,
			},
			["253"] = {
				['id'] = 0x0FD,
				['offset'] = 1,
			},
			["254"] = {
				['id'] = 0x0FE,
				['offset'] = 2,
			},
			["255"] = {
				['id'] = 0x0FF,
				['offset'] = 3,
			},
			["256"] = {
				['id'] = 0x100,
				['offset'] = 4,
			},
			["257"] = {
				['id'] = 0x101,
				['offset'] = 5,
			},
			["258"] = {
				['id'] = 0x102,
				['offset'] = 6,
			},
			["259"] = {
				['id'] = 0x103,
				['offset'] = 7,
			},
			["260"] = {
				['id'] = 0x104,
				['offset'] = 8,
			},
			["261"] = {
				['id'] = 0x105,
				['offset'] = 9,
			},
			["262"] = {
				['id'] = 0x106,
				['offset'] = 10,
			},
			["263"] = {
				['id'] = 0x107,
				['offset'] = 11,
			},
			["264"] = {
				['id'] = 0x108,
				['offset'] = 12,
			},
			["265"] = {
				['id'] = 0x109,
				['offset'] = 13,
			},
			["266"] = {
				['id'] = 0x10A,
				['offset'] = 14,
			},
			["267"] = {
				['id'] = 0x10B,
				['offset'] = 15,
			},
			["268"] = {
				['id'] = 0x10C,
				['offset'] = 16,
			},
			["269"] = {
				['id'] = 0x10D,
				['offset'] = 17,
			},
			["270"] = {
				['id'] = 0x10E,
				['offset'] = 18,
			},
			["271"] = {
				['id'] = 0x10F,
				['offset'] = 19,
			},
			["272"] = {
				['id'] = 0x110,
				['offset'] = 20,
			},
			["273"] = {
				['id'] = 0x111,
				['offset'] = 21,
			},
			["274"] = {
				['id'] = 0x112,
				['offset'] = 22,
			},
			["275"] = {
				['id'] = 0x113,
				['offset'] = 23,
			},
			["276"] = {
				['id'] = 0x114,
				['offset'] = 24,
			},
		},
		["ENEMIES"] = {
			["277"] = {
				['id'] = 0x115,
				['offset'] = 0,
			},
			["278"] = {
				['id'] = 0x116,
				['offset'] = 1,
			},
			["279"] = {
				['id'] = 0x117,
				['offset'] = 2,
			},
		},
		["LIFE"] = {
			["280"] = {
				['id'] = 0x118,
				['offset'] = 0,
			},
		},
	},
	["AP_CARNIVAL_L1"] = {
		["GOAL"] = "382",
		["GARIBS"] = {
			["283"] = {
				['id'] = 0x11B,
				['offset'] = 0,
			},
			["284"] = {
				['id'] = 0x11C,
				['offset'] = 1,
			},
			["285"] = {
				['id'] = 0x11D,
				['offset'] = 2,
			},
			["286"] = {
				['id'] = 0x11E,
				['offset'] = 3,
			},
			["287"] = {
				['id'] = 0x11F,
				['offset'] = 4,
			},
			["288"] = {
				['id'] = 0x120,
				['offset'] = 5,
			},
			["289"] = {
				['id'] = 0x121,
				['offset'] = 6,
			},
			["290"] = {
				['id'] = 0x122,
				['offset'] = 7,
			},
			["291"] = {
				['id'] = 0x123,
				['offset'] = 8,
			},
			["292"] = {
				['id'] = 0x124,
				['offset'] = 9,
			},
			["293"] = {
				['id'] = 0x125,
				['offset'] = 10,
			},
			["294"] = {
				['id'] = 0x126,
				['offset'] = 11,
			},
			["295"] = {
				['id'] = 0x127,
				['offset'] = 12,
			},
			["296"] = {
				['id'] = 0x128,
				['offset'] = 13,
			},
			["297"] = {
				['id'] = 0x129,
				['offset'] = 14,
			},
			["298"] = {
				['id'] = 0x12A,
				['offset'] = 15,
			},
			["299"] = {
				['id'] = 0x12B,
				['offset'] = 16,
			},
			["300"] = {
				['id'] = 0x12C,
				['offset'] = 17,
			},
			["301"] = {
				['id'] = 0x12D,
				['offset'] = 18,
			},
			["302"] = {
				['id'] = 0x12E,
				['offset'] = 19,
			},
			["303"] = {
				['id'] = 0x12F,
				['offset'] = 20,
			},
			["304"] = {
				['id'] = 0x130,
				['offset'] = 21,
			},
			["305"] = {
				['id'] = 0x131,
				['offset'] = 22,
			},
			["306"] = {
				['id'] = 0x132,
				['offset'] = 23,
			},
			["307"] = {
				['id'] = 0x133,
				['offset'] = 24,
			},
			["308"] = {
				['id'] = 0x134,
				['offset'] = 25,
			},
			["309"] = {
				['id'] = 0x135,
				['offset'] = 26,
			},
			["310"] = {
				['id'] = 0x136,
				['offset'] = 27,
			},
			["311"] = {
				['id'] = 0x137,
				['offset'] = 28,
			},
			["312"] = {
				['id'] = 0x138,
				['offset'] = 29,
			},
			["313"] = {
				['id'] = 0x139,
				['offset'] = 30,
			},
			["314"] = {
				['id'] = 0x13A,
				['offset'] = 31,
			},
			["315"] = {
				['id'] = 0x13B,
				['offset'] = 32,
			},
			["316"] = {
				['id'] = 0x13C,
				['offset'] = 33,
			},
			["317"] = {
				['id'] = 0x13D,
				['offset'] = 34,
			},
			["318"] = {
				['id'] = 0x13E,
				['offset'] = 35,
			},
			["319"] = {
				['id'] = 0x13F,
				['offset'] = 36,
			},
			["320"] = {
				['id'] = 0x140,
				['offset'] = 37,
			},
			["321"] = {
				['id'] = 0x141,
				['offset'] = 38,
			},
			["322"] = {
				['id'] = 0x142,
				['offset'] = 39,
			},
			["323"] = {
				['id'] = 0x143,
				['offset'] = 40,
			},
			["324"] = {
				['id'] = 0x144,
				['offset'] = 41,
			},
			["325"] = {
				['id'] = 0x145,
				['offset'] = 42,
			},
			["326"] = {
				['id'] = 0x146,
				['offset'] = 43,
			},
			["327"] = {
				['id'] = 0x147,
				['offset'] = 44,
			},
			["328"] = {
				['id'] = 0x148,
				['offset'] = 45,
			},
			["329"] = {
				['id'] = 0x149,
				['offset'] = 46,
			},
			["330"] = {
				['id'] = 0x14A,
				['offset'] = 47,
			},
			["331"] = {
				['id'] = 0x14B,
				['offset'] = 48,
			},
			["332"] = {
				['id'] = 0x14C,
				['offset'] = 49,
			},
			["333"] = {
				['id'] = 0x14D,
				['offset'] = 50,
			},
			["334"] = {
				['id'] = 0x14E,
				['offset'] = 51,
			},
			["335"] = {
				['id'] = 0x14F,
				['offset'] = 52,
			},
			["336"] = {
				['id'] = 0x150,
				['offset'] = 53,
			},
			["337"] = {
				['id'] = 0x151,
				['offset'] = 54,
			},
			["338"] = {
				['id'] = 0x152,
				['offset'] = 55,
			},
		},
		["ENEMY_GARIBS"] = {
			["339"] = {
				['id'] = 0x153,
				['offset'] = 56,
				['object_id'] = 0x160,
			},
			["340"] = {
				['id'] = 0x154,
				['offset'] = 57,
				['object_id'] = 0x161,
			},
			["341"] = {
				['id'] = 0x155,
				['offset'] = 58,
				['object_id'] = 0x162,
			},
			["342"] = {
				['id'] = 0x156,
				['offset'] = 59,
				['object_id'] = 0x163,
			},
			["343"] = {
				['id'] = 0x157,
				['offset'] = 60,
				['object_id'] = 0x164,
			},
			["344"] = {
				['id'] = 0x158,
				['offset'] = 61,
				['object_id'] = 0x165,
			},
			["345"] = {
				['id'] = 0x159,
				['offset'] = 62,
				['object_id'] = 0x166,
			},
			["346"] = {
				['id'] = 0x15A,
				['offset'] = 63,
				['object_id'] = 0x167,
			},
			["347"] = {
				['id'] = 0x15B,
				['offset'] = 64,
				['object_id'] = 0x168,
			},
		},
		["ENEMIES"] = {
			["348"] = {
				['id'] = 0x15C,
				['offset'] = 0,
			},
			["349"] = {
				['id'] = 0x15D,
				['offset'] = 1,
			},
			["350"] = {
				['id'] = 0x15E,
				['offset'] = 2,
			},
			["351"] = {
				['id'] = 0x15F,
				['offset'] = 3,
			},
			["352"] = {
				['id'] = 0x160,
				['offset'] = 4,
			},
			["353"] = {
				['id'] = 0x161,
				['offset'] = 5,
			},
			["354"] = {
				['id'] = 0x162,
				['offset'] = 6,
			},
			["355"] = {
				['id'] = 0x163,
				['offset'] = 7,
			},
			["356"] = {
				['id'] = 0x164,
				['offset'] = 8,
			},
			["357"] = {
				['id'] = 0x165,
				['offset'] = 9,
			},
			["358"] = {
				['id'] = 0x166,
				['offset'] = 10,
			},
			["359"] = {
				['id'] = 0x167,
				['offset'] = 11,
			},
			["360"] = {
				['id'] = 0x168,
				['offset'] = 12,
			},
		},
		["LIFE"] = {
			["361"] = {
				['id'] = 0x169,
				['offset'] = 0,
			},
			["362"] = {
				['id'] = 0x16A,
				['offset'] = 1,
			},
			["363"] = {
				['id'] = 0x16B,
				['offset'] = 2,
			},
			["364"] = {
				['id'] = 0x16C,
				['offset'] = 3,
			},
		},
		["TIP"] = {
			["365"] = {
				['id'] = 0x16D,
				['offset'] = 0,
			},
			["366"] = {
				['id'] = 0x16E,
				['offset'] = 1,
			},
			["367"] = {
				['id'] = 0x16F,
				['offset'] = 2,
			},
			["368"] = {
				['id'] = 0x170,
				['offset'] = 3,
			},
		},
		["CHECKPOINT"] = {
			["369"] = {
				['id'] = 0x171,
				['offset'] = 0,
			},
			["370"] = {
				['id'] = 0x172,
				['offset'] = 1,
			},
			["371"] = {
				['id'] = 0x173,
				['offset'] = 2,
			},
			["372"] = {
				['id'] = 0x174,
				['offset'] = 3,
			},
		},
		["SWITCH"] = {
			["373"] = {
				['id'] = 0x175,
				['offset'] = 0,
			},
			["374"] = {
				['id'] = 0x176,
				['offset'] = 1,
			},
			["375"] = {
				['id'] = 0x177,
				['offset'] = 2,
			},
			["376"] = {
				['id'] = 0x178,
				['offset'] = 3,
			},
			["377"] = {
				['id'] = 0x179,
				['offset'] = 4,
			},
			["378"] = {
				['id'] = 0x17A,
				['offset'] = 5,
			},
			["379"] = {
				['id'] = 0x17B,
				['offset'] = 6,
			},
			["380"] = {
				['id'] = 0x17C,
				['offset'] = 7,
			},
			["381"] = {
				['id'] = 0x17D,
				['offset'] = 8,
			},
		},
		["POTIONS"] = {
			["383"] = {
				['id'] = 0x17F,
				['offset'] = 0,
			},
			["384"] = {
				['id'] = 0x180,
				['offset'] = 1,
			},
		},
	},
	["AP_CARNIVAL_L2"] = {
		["GOAL"] = "484",
		["GARIBS"] = {
			["385"] = {
				['id'] = 0x181,
				['offset'] = 0,
			},
			["386"] = {
				['id'] = 0x182,
				['offset'] = 1,
			},
			["387"] = {
				['id'] = 0x183,
				['offset'] = 2,
			},
			["388"] = {
				['id'] = 0x184,
				['offset'] = 3,
			},
			["389"] = {
				['id'] = 0x185,
				['offset'] = 4,
			},
			["390"] = {
				['id'] = 0x186,
				['offset'] = 5,
			},
			["391"] = {
				['id'] = 0x187,
				['offset'] = 6,
			},
			["392"] = {
				['id'] = 0x188,
				['offset'] = 7,
			},
			["393"] = {
				['id'] = 0x189,
				['offset'] = 8,
			},
			["394"] = {
				['id'] = 0x18A,
				['offset'] = 9,
			},
			["395"] = {
				['id'] = 0x18B,
				['offset'] = 10,
			},
			["396"] = {
				['id'] = 0x18C,
				['offset'] = 11,
			},
			["397"] = {
				['id'] = 0x18D,
				['offset'] = 12,
			},
			["398"] = {
				['id'] = 0x18E,
				['offset'] = 13,
			},
			["399"] = {
				['id'] = 0x18F,
				['offset'] = 14,
			},
			["400"] = {
				['id'] = 0x190,
				['offset'] = 15,
			},
			["401"] = {
				['id'] = 0x191,
				['offset'] = 16,
			},
			["402"] = {
				['id'] = 0x192,
				['offset'] = 17,
			},
			["403"] = {
				['id'] = 0x193,
				['offset'] = 18,
			},
			["404"] = {
				['id'] = 0x194,
				['offset'] = 19,
			},
			["405"] = {
				['id'] = 0x195,
				['offset'] = 20,
			},
			["406"] = {
				['id'] = 0x196,
				['offset'] = 21,
			},
			["407"] = {
				['id'] = 0x197,
				['offset'] = 22,
			},
			["408"] = {
				['id'] = 0x198,
				['offset'] = 23,
			},
			["409"] = {
				['id'] = 0x199,
				['offset'] = 24,
			},
			["410"] = {
				['id'] = 0x19A,
				['offset'] = 25,
			},
			["411"] = {
				['id'] = 0x19B,
				['offset'] = 26,
			},
			["412"] = {
				['id'] = 0x19C,
				['offset'] = 27,
			},
			["413"] = {
				['id'] = 0x19D,
				['offset'] = 28,
			},
			["414"] = {
				['id'] = 0x19E,
				['offset'] = 29,
			},
			["415"] = {
				['id'] = 0x19F,
				['offset'] = 30,
			},
			["416"] = {
				['id'] = 0x1A0,
				['offset'] = 31,
			},
			["417"] = {
				['id'] = 0x1A1,
				['offset'] = 32,
			},
			["418"] = {
				['id'] = 0x1A2,
				['offset'] = 33,
			},
			["419"] = {
				['id'] = 0x1A3,
				['offset'] = 34,
			},
			["420"] = {
				['id'] = 0x1A4,
				['offset'] = 35,
			},
			["421"] = {
				['id'] = 0x1A5,
				['offset'] = 36,
			},
			["422"] = {
				['id'] = 0x1A6,
				['offset'] = 37,
			},
			["423"] = {
				['id'] = 0x1A7,
				['offset'] = 38,
			},
			["424"] = {
				['id'] = 0x1A8,
				['offset'] = 39,
			},
			["425"] = {
				['id'] = 0x1A9,
				['offset'] = 40,
			},
			["426"] = {
				['id'] = 0x1AA,
				['offset'] = 41,
			},
			["427"] = {
				['id'] = 0x1AB,
				['offset'] = 42,
			},
			["428"] = {
				['id'] = 0x1AC,
				['offset'] = 43,
			},
			["429"] = {
				['id'] = 0x1AD,
				['offset'] = 44,
			},
			["430"] = {
				['id'] = 0x1AE,
				['offset'] = 45,
			},
			["431"] = {
				['id'] = 0x1AF,
				['offset'] = 46,
			},
			["432"] = {
				['id'] = 0x1B0,
				['offset'] = 47,
			},
			["433"] = {
				['id'] = 0x1B1,
				['offset'] = 48,
			},
			["434"] = {
				['id'] = 0x1B2,
				['offset'] = 49,
			},
			["435"] = {
				['id'] = 0x1B3,
				['offset'] = 50,
			},
			["436"] = {
				['id'] = 0x1B4,
				['offset'] = 51,
			},
			["437"] = {
				['id'] = 0x1B5,
				['offset'] = 52,
			},
			["438"] = {
				['id'] = 0x1B6,
				['offset'] = 53,
			},
			["439"] = {
				['id'] = 0x1B7,
				['offset'] = 54,
			},
			["440"] = {
				['id'] = 0x1B8,
				['offset'] = 55,
			},
			["441"] = {
				['id'] = 0x1B9,
				['offset'] = 56,
			},
			["442"] = {
				['id'] = 0x1BA,
				['offset'] = 57,
			},
			["443"] = {
				['id'] = 0x1BB,
				['offset'] = 58,
			},
			["444"] = {
				['id'] = 0x1BC,
				['offset'] = 59,
			},
			["445"] = {
				['id'] = 0x1BD,
				['offset'] = 60,
			},
			["446"] = {
				['id'] = 0x1BE,
				['offset'] = 61,
			},
			["447"] = {
				['id'] = 0x1BF,
				['offset'] = 62,
			},
			["448"] = {
				['id'] = 0x1C0,
				['offset'] = 63,
			},
			["449"] = {
				['id'] = 0x1C1,
				['offset'] = 64,
			},
			["450"] = {
				['id'] = 0x1C2,
				['offset'] = 65,
			},
			["451"] = {
				['id'] = 0x1C3,
				['offset'] = 66,
			},
			["452"] = {
				['id'] = 0x1C4,
				['offset'] = 67,
			},
			["453"] = {
				['id'] = 0x1C5,
				['offset'] = 68,
			},
			["454"] = {
				['id'] = 0x1C6,
				['offset'] = 69,
			},
			["455"] = {
				['id'] = 0x1C7,
				['offset'] = 70,
			},
			["456"] = {
				['id'] = 0x1C8,
				['offset'] = 71,
			},
			["457"] = {
				['id'] = 0x1C9,
				['offset'] = 72,
			},
			["458"] = {
				['id'] = 0x1CA,
				['offset'] = 73,
			},
			["459"] = {
				['id'] = 0x1CB,
				['offset'] = 74,
			},
			["460"] = {
				['id'] = 0x1CC,
				['offset'] = 75,
			},
		},
		["ENEMY_GARIBS"] = {
			["461"] = {
				['id'] = 0x1CD,
				['offset'] = 76,
				['object_id'] = 0x1D1,
			},
			["462"] = {
				['id'] = 0x1CE,
				['offset'] = 77,
				['object_id'] = 0x1D3,
			},
			["463"] = {
				['id'] = 0x1CF,
				['offset'] = 78,
				['object_id'] = 0x1D6,
			},
			["464"] = {
				['id'] = 0x1D0,
				['offset'] = 79,
				['object_id'] = 0x1D7,
			},
		},
		["ENEMIES"] = {
			["465"] = {
				['id'] = 0x1D1,
				['offset'] = 0,
			},
			["466"] = {
				['id'] = 0x1D2,
				['offset'] = 1,
			},
			["467"] = {
				['id'] = 0x1D3,
				['offset'] = 2,
			},
			["468"] = {
				['id'] = 0x1D4,
				['offset'] = 3,
			},
			["469"] = {
				['id'] = 0x1D5,
				['offset'] = 4,
			},
			["470"] = {
				['id'] = 0x1D6,
				['offset'] = 5,
			},
			["471"] = {
				['id'] = 0x1D7,
				['offset'] = 6,
			},
		},
		["LIFE"] = {
			["472"] = {
				['id'] = 0x1D8,
				['offset'] = 0,
			},
			["473"] = {
				['id'] = 0x1D9,
				['offset'] = 1,
			},
			["474"] = {
				['id'] = 0x1DA,
				['offset'] = 2,
			},
		},
		["TIP"] = {
			["475"] = {
				['id'] = 0x1DB,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			["476"] = {
				['id'] = 0x1DC,
				['offset'] = 0,
			},
			["477"] = {
				['id'] = 0x1DD,
				['offset'] = 1,
			},
			["478"] = {
				['id'] = 0x1DE,
				['offset'] = 2,
			},
			["479"] = {
				['id'] = 0x1DF,
				['offset'] = 3,
			},
			["480"] = {
				['id'] = 0x1E0,
				['offset'] = 4,
			},
		},
		["SWITCH"] = {
			["481"] = {
				['id'] = 0x1E1,
				['offset'] = 0,
			},
			["482"] = {
				['id'] = 0x1E2,
				['offset'] = 1,
			},
			["483"] = {
				['id'] = 0x1E3,
				['offset'] = 2,
			},
		},
		["POTIONS"] = {
			["485"] = {
				['id'] = 0x1E5,
				['offset'] = 0,
			},
			["486"] = {
				['id'] = 0x1E6,
				['offset'] = 1,
			},
			["487"] = {
				['id'] = 0x1E7,
				['offset'] = 2,
			},
		},
	},
	["AP_CARNIVAL_L3"] = {
		["GOAL"] = "598",
		["GARIBS"] = {
			["488"] = {
				['id'] = 0x1E8,
				['offset'] = 0,
			},
			["489"] = {
				['id'] = 0x1E9,
				['offset'] = 1,
			},
			["490"] = {
				['id'] = 0x1EA,
				['offset'] = 2,
			},
			["491"] = {
				['id'] = 0x1EB,
				['offset'] = 3,
			},
			["492"] = {
				['id'] = 0x1EC,
				['offset'] = 4,
			},
			["493"] = {
				['id'] = 0x1ED,
				['offset'] = 5,
			},
			["494"] = {
				['id'] = 0x1EE,
				['offset'] = 6,
			},
			["495"] = {
				['id'] = 0x1EF,
				['offset'] = 7,
			},
			["496"] = {
				['id'] = 0x1F0,
				['offset'] = 8,
			},
			["497"] = {
				['id'] = 0x1F1,
				['offset'] = 9,
			},
			["498"] = {
				['id'] = 0x1F2,
				['offset'] = 10,
			},
			["499"] = {
				['id'] = 0x1F3,
				['offset'] = 11,
			},
			["500"] = {
				['id'] = 0x1F4,
				['offset'] = 12,
			},
			["501"] = {
				['id'] = 0x1F5,
				['offset'] = 13,
			},
			["502"] = {
				['id'] = 0x1F6,
				['offset'] = 14,
			},
			["503"] = {
				['id'] = 0x1F7,
				['offset'] = 15,
			},
			["504"] = {
				['id'] = 0x1F8,
				['offset'] = 16,
			},
			["505"] = {
				['id'] = 0x1F9,
				['offset'] = 17,
			},
			["506"] = {
				['id'] = 0x1FA,
				['offset'] = 18,
			},
			["507"] = {
				['id'] = 0x1FB,
				['offset'] = 19,
			},
			["508"] = {
				['id'] = 0x1FC,
				['offset'] = 20,
			},
			["509"] = {
				['id'] = 0x1FD,
				['offset'] = 21,
			},
			["510"] = {
				['id'] = 0x1FE,
				['offset'] = 22,
			},
			["511"] = {
				['id'] = 0x1FF,
				['offset'] = 23,
			},
			["512"] = {
				['id'] = 0x200,
				['offset'] = 24,
			},
			["513"] = {
				['id'] = 0x201,
				['offset'] = 25,
			},
			["514"] = {
				['id'] = 0x202,
				['offset'] = 26,
			},
			["515"] = {
				['id'] = 0x203,
				['offset'] = 27,
			},
			["516"] = {
				['id'] = 0x204,
				['offset'] = 28,
			},
			["517"] = {
				['id'] = 0x205,
				['offset'] = 29,
			},
			["518"] = {
				['id'] = 0x206,
				['offset'] = 30,
			},
			["519"] = {
				['id'] = 0x207,
				['offset'] = 31,
			},
			["520"] = {
				['id'] = 0x208,
				['offset'] = 32,
			},
			["521"] = {
				['id'] = 0x209,
				['offset'] = 33,
			},
			["522"] = {
				['id'] = 0x20A,
				['offset'] = 34,
			},
			["523"] = {
				['id'] = 0x20B,
				['offset'] = 35,
			},
			["524"] = {
				['id'] = 0x20C,
				['offset'] = 36,
			},
			["525"] = {
				['id'] = 0x20D,
				['offset'] = 37,
			},
			["526"] = {
				['id'] = 0x20E,
				['offset'] = 38,
			},
			["527"] = {
				['id'] = 0x20F,
				['offset'] = 39,
			},
			["528"] = {
				['id'] = 0x210,
				['offset'] = 40,
			},
			["529"] = {
				['id'] = 0x211,
				['offset'] = 41,
			},
			["530"] = {
				['id'] = 0x212,
				['offset'] = 42,
			},
			["531"] = {
				['id'] = 0x213,
				['offset'] = 43,
			},
			["532"] = {
				['id'] = 0x214,
				['offset'] = 44,
			},
			["533"] = {
				['id'] = 0x215,
				['offset'] = 45,
			},
			["534"] = {
				['id'] = 0x216,
				['offset'] = 46,
			},
			["535"] = {
				['id'] = 0x217,
				['offset'] = 47,
			},
			["536"] = {
				['id'] = 0x218,
				['offset'] = 48,
			},
			["537"] = {
				['id'] = 0x219,
				['offset'] = 49,
			},
			["538"] = {
				['id'] = 0x21A,
				['offset'] = 50,
			},
			["539"] = {
				['id'] = 0x21B,
				['offset'] = 51,
			},
			["540"] = {
				['id'] = 0x21C,
				['offset'] = 52,
			},
			["541"] = {
				['id'] = 0x21D,
				['offset'] = 53,
			},
			["542"] = {
				['id'] = 0x21E,
				['offset'] = 54,
			},
			["543"] = {
				['id'] = 0x21F,
				['offset'] = 55,
			},
			["544"] = {
				['id'] = 0x220,
				['offset'] = 56,
			},
			["545"] = {
				['id'] = 0x221,
				['offset'] = 57,
			},
			["546"] = {
				['id'] = 0x222,
				['offset'] = 58,
			},
			["547"] = {
				['id'] = 0x223,
				['offset'] = 59,
			},
			["548"] = {
				['id'] = 0x224,
				['offset'] = 60,
			},
			["549"] = {
				['id'] = 0x225,
				['offset'] = 61,
			},
			["550"] = {
				['id'] = 0x226,
				['offset'] = 62,
			},
			["551"] = {
				['id'] = 0x227,
				['offset'] = 63,
			},
			["552"] = {
				['id'] = 0x228,
				['offset'] = 64,
			},
			["553"] = {
				['id'] = 0x229,
				['offset'] = 65,
			},
			["554"] = {
				['id'] = 0x22A,
				['offset'] = 66,
			},
			["555"] = {
				['id'] = 0x22B,
				['offset'] = 67,
			},
			["556"] = {
				['id'] = 0x22C,
				['offset'] = 68,
			},
			["557"] = {
				['id'] = 0x22D,
				['offset'] = 69,
			},
			["558"] = {
				['id'] = 0x22E,
				['offset'] = 70,
			},
			["559"] = {
				['id'] = 0x22F,
				['offset'] = 71,
			},
			["560"] = {
				['id'] = 0x230,
				['offset'] = 72,
			},
			["561"] = {
				['id'] = 0x231,
				['offset'] = 73,
			},
		},
		["ENEMY_GARIBS"] = {
			["562"] = {
				['id'] = 0x232,
				['offset'] = 74,
				['object_id'] = 0x23F,
			},
			["563"] = {
				['id'] = 0x233,
				['offset'] = 75,
				['object_id'] = 0x240,
			},
			["564"] = {
				['id'] = 0x234,
				['offset'] = 76,
				['object_id'] = 0x241,
			},
			["565"] = {
				['id'] = 0x235,
				['offset'] = 77,
				['object_id'] = 0x243,
			},
			["566"] = {
				['id'] = 0x236,
				['offset'] = 78,
				['object_id'] = 0x244,
			},
			["567"] = {
				['id'] = 0x237,
				['offset'] = 79,
				['object_id'] = 0x245,
			},
		},
		["ENEMIES"] = {
			["568"] = {
				['id'] = 0x238,
				['offset'] = 0,
			},
			["569"] = {
				['id'] = 0x239,
				['offset'] = 1,
			},
			["570"] = {
				['id'] = 0x23A,
				['offset'] = 2,
			},
			["571"] = {
				['id'] = 0x23B,
				['offset'] = 3,
			},
			["572"] = {
				['id'] = 0x23C,
				['offset'] = 4,
			},
			["573"] = {
				['id'] = 0x23D,
				['offset'] = 5,
			},
			["574"] = {
				['id'] = 0x23E,
				['offset'] = 6,
			},
			["575"] = {
				['id'] = 0x23F,
				['offset'] = 7,
			},
			["576"] = {
				['id'] = 0x240,
				['offset'] = 8,
			},
			["577"] = {
				['id'] = 0x241,
				['offset'] = 9,
			},
			["578"] = {
				['id'] = 0x242,
				['offset'] = 10,
			},
			["579"] = {
				['id'] = 0x243,
				['offset'] = 11,
			},
			["580"] = {
				['id'] = 0x244,
				['offset'] = 12,
			},
			["581"] = {
				['id'] = 0x245,
				['offset'] = 13,
			},
		},
		["LIFE"] = {
			["582"] = {
				['id'] = 0x246,
				['offset'] = 0,
			},
			["583"] = {
				['id'] = 0x247,
				['offset'] = 1,
			},
			["584"] = {
				['id'] = 0x248,
				['offset'] = 2,
			},
			["585"] = {
				['id'] = 0x249,
				['offset'] = 3,
			},
			["586"] = {
				['id'] = 0x24A,
				['offset'] = 4,
			},
			["587"] = {
				['id'] = 0x24B,
				['offset'] = 5,
			},
			["588"] = {
				['id'] = 0x24C,
				['offset'] = 6,
			},
			["589"] = {
				['id'] = 0x24D,
				['offset'] = 7,
			},
			["590"] = {
				['id'] = 0x24E,
				['offset'] = 8,
			},
			["591"] = {
				['id'] = 0x24F,
				['offset'] = 9,
			},
		},
		["CHECKPOINT"] = {
			["592"] = {
				['id'] = 0x250,
				['offset'] = 0,
			},
			["593"] = {
				['id'] = 0x251,
				['offset'] = 1,
			},
			["594"] = {
				['id'] = 0x252,
				['offset'] = 2,
			},
			["595"] = {
				['id'] = 0x253,
				['offset'] = 3,
			},
		},
		["SWITCH"] = {
			["596"] = {
				['id'] = 0x254,
				['offset'] = 0,
			},
			["597"] = {
				['id'] = 0x255,
				['offset'] = 1,
			},
		},
		["POTIONS"] = {
			["599"] = {
				['id'] = 0x257,
				['offset'] = 0,
			},
			["600"] = {
				['id'] = 0x258,
				['offset'] = 1,
			},
		},
	},
	["AP_CARNIVAL_BOSS"] = {
		["GOAL"] = "601",
	},
	["AP_CARNIVAL_BONUS"] = {
		["GOAL"] = "624",
		["GARIBS"] = {
			["602"] = {
				['id'] = 0x25A,
				['offset'] = 0,
			},
			["603"] = {
				['id'] = 0x25B,
				['offset'] = 1,
			},
			["604"] = {
				['id'] = 0x25C,
				['offset'] = 2,
			},
			["605"] = {
				['id'] = 0x25D,
				['offset'] = 3,
			},
			["606"] = {
				['id'] = 0x25E,
				['offset'] = 4,
			},
			["607"] = {
				['id'] = 0x25F,
				['offset'] = 5,
			},
			["608"] = {
				['id'] = 0x260,
				['offset'] = 6,
			},
			["609"] = {
				['id'] = 0x261,
				['offset'] = 7,
			},
			["610"] = {
				['id'] = 0x262,
				['offset'] = 8,
			},
			["611"] = {
				['id'] = 0x263,
				['offset'] = 9,
			},
			["612"] = {
				['id'] = 0x264,
				['offset'] = 10,
			},
			["613"] = {
				['id'] = 0x265,
				['offset'] = 11,
			},
			["614"] = {
				['id'] = 0x266,
				['offset'] = 12,
			},
			["615"] = {
				['id'] = 0x267,
				['offset'] = 13,
			},
			["616"] = {
				['id'] = 0x268,
				['offset'] = 14,
			},
			["617"] = {
				['id'] = 0x269,
				['offset'] = 15,
			},
			["618"] = {
				['id'] = 0x26A,
				['offset'] = 16,
			},
			["619"] = {
				['id'] = 0x26B,
				['offset'] = 17,
			},
			["620"] = {
				['id'] = 0x26C,
				['offset'] = 18,
			},
			["621"] = {
				['id'] = 0x26D,
				['offset'] = 19,
			},
		},
		["LIFE"] = {
			["622"] = {
				['id'] = 0x26E,
				['offset'] = 0,
			},
			["623"] = {
				['id'] = 0x26F,
				['offset'] = 1,
			},
		},
	},
	["AP_PIRATES_L1"] = {
		["GOAL"] = "723",
		["GARIBS"] = {
			["626"] = {
				['id'] = 0x272,
				['offset'] = 0,
			},
			["627"] = {
				['id'] = 0x273,
				['offset'] = 1,
			},
			["628"] = {
				['id'] = 0x274,
				['offset'] = 2,
			},
			["629"] = {
				['id'] = 0x275,
				['offset'] = 3,
			},
			["630"] = {
				['id'] = 0x276,
				['offset'] = 4,
			},
			["631"] = {
				['id'] = 0x277,
				['offset'] = 5,
			},
			["632"] = {
				['id'] = 0x278,
				['offset'] = 6,
			},
			["633"] = {
				['id'] = 0x279,
				['offset'] = 7,
			},
			["634"] = {
				['id'] = 0x27A,
				['offset'] = 8,
			},
			["635"] = {
				['id'] = 0x27B,
				['offset'] = 9,
			},
			["636"] = {
				['id'] = 0x27C,
				['offset'] = 10,
			},
			["637"] = {
				['id'] = 0x27D,
				['offset'] = 11,
			},
			["638"] = {
				['id'] = 0x27E,
				['offset'] = 12,
			},
			["639"] = {
				['id'] = 0x27F,
				['offset'] = 13,
			},
			["640"] = {
				['id'] = 0x280,
				['offset'] = 14,
			},
			["641"] = {
				['id'] = 0x281,
				['offset'] = 15,
			},
			["642"] = {
				['id'] = 0x282,
				['offset'] = 16,
			},
			["643"] = {
				['id'] = 0x283,
				['offset'] = 17,
			},
			["644"] = {
				['id'] = 0x284,
				['offset'] = 18,
			},
			["645"] = {
				['id'] = 0x285,
				['offset'] = 19,
			},
			["646"] = {
				['id'] = 0x286,
				['offset'] = 20,
			},
			["647"] = {
				['id'] = 0x287,
				['offset'] = 21,
			},
			["648"] = {
				['id'] = 0x288,
				['offset'] = 22,
			},
			["649"] = {
				['id'] = 0x289,
				['offset'] = 23,
			},
			["650"] = {
				['id'] = 0x28A,
				['offset'] = 24,
			},
			["651"] = {
				['id'] = 0x28B,
				['offset'] = 25,
			},
			["652"] = {
				['id'] = 0x28C,
				['offset'] = 26,
			},
			["653"] = {
				['id'] = 0x28D,
				['offset'] = 27,
			},
			["654"] = {
				['id'] = 0x28E,
				['offset'] = 28,
			},
			["655"] = {
				['id'] = 0x28F,
				['offset'] = 29,
			},
			["656"] = {
				['id'] = 0x290,
				['offset'] = 30,
			},
			["657"] = {
				['id'] = 0x291,
				['offset'] = 31,
			},
			["658"] = {
				['id'] = 0x292,
				['offset'] = 32,
			},
			["659"] = {
				['id'] = 0x293,
				['offset'] = 33,
			},
			["660"] = {
				['id'] = 0x294,
				['offset'] = 34,
			},
			["661"] = {
				['id'] = 0x295,
				['offset'] = 35,
			},
			["662"] = {
				['id'] = 0x296,
				['offset'] = 36,
			},
			["663"] = {
				['id'] = 0x297,
				['offset'] = 37,
			},
			["664"] = {
				['id'] = 0x298,
				['offset'] = 38,
			},
			["665"] = {
				['id'] = 0x299,
				['offset'] = 39,
			},
			["666"] = {
				['id'] = 0x29A,
				['offset'] = 40,
			},
			["667"] = {
				['id'] = 0x29B,
				['offset'] = 41,
			},
			["668"] = {
				['id'] = 0x29C,
				['offset'] = 42,
			},
			["669"] = {
				['id'] = 0x29D,
				['offset'] = 43,
			},
			["670"] = {
				['id'] = 0x29E,
				['offset'] = 44,
			},
			["671"] = {
				['id'] = 0x29F,
				['offset'] = 45,
			},
			["672"] = {
				['id'] = 0x2A0,
				['offset'] = 46,
			},
			["673"] = {
				['id'] = 0x2A1,
				['offset'] = 47,
			},
			["674"] = {
				['id'] = 0x2A2,
				['offset'] = 48,
			},
			["675"] = {
				['id'] = 0x2A3,
				['offset'] = 49,
			},
			["676"] = {
				['id'] = 0x2A4,
				['offset'] = 50,
			},
			["677"] = {
				['id'] = 0x2A5,
				['offset'] = 51,
			},
			["678"] = {
				['id'] = 0x2A6,
				['offset'] = 52,
			},
			["679"] = {
				['id'] = 0x2A7,
				['offset'] = 53,
			},
			["680"] = {
				['id'] = 0x2A8,
				['offset'] = 54,
			},
			["681"] = {
				['id'] = 0x2A9,
				['offset'] = 55,
			},
			["682"] = {
				['id'] = 0x2AA,
				['offset'] = 56,
			},
			["683"] = {
				['id'] = 0x2AB,
				['offset'] = 57,
			},
			["684"] = {
				['id'] = 0x2AC,
				['offset'] = 58,
			},
			["685"] = {
				['id'] = 0x2AD,
				['offset'] = 59,
			},
			["686"] = {
				['id'] = 0x2AE,
				['offset'] = 60,
			},
			["687"] = {
				['id'] = 0x2AF,
				['offset'] = 61,
			},
			["688"] = {
				['id'] = 0x2B0,
				['offset'] = 62,
			},
			["689"] = {
				['id'] = 0x2B1,
				['offset'] = 63,
			},
			["690"] = {
				['id'] = 0x2B2,
				['offset'] = 64,
			},
			["691"] = {
				['id'] = 0x2B3,
				['offset'] = 65,
			},
		},
		["ENEMY_GARIBS"] = {
			["692"] = {
				['id'] = 0x2B4,
				['offset'] = 66,
				['object_id'] = 0x2BE,
			},
			["693"] = {
				['id'] = 0x2B5,
				['offset'] = 67,
				['object_id'] = 0x2C0,
			},
			["694"] = {
				['id'] = 0x2B6,
				['offset'] = 68,
				['object_id'] = 0x2C1,
			},
			["695"] = {
				['id'] = 0x2B7,
				['offset'] = 69,
				['object_id'] = 0x2C2,
			},
		},
		["ENEMIES"] = {
			["696"] = {
				['id'] = 0x2B8,
				['offset'] = 0,
			},
			["697"] = {
				['id'] = 0x2B9,
				['offset'] = 1,
			},
			["698"] = {
				['id'] = 0x2BA,
				['offset'] = 2,
			},
			["699"] = {
				['id'] = 0x2BB,
				['offset'] = 3,
			},
			["700"] = {
				['id'] = 0x2BC,
				['offset'] = 4,
			},
			["701"] = {
				['id'] = 0x2BD,
				['offset'] = 5,
			},
			["702"] = {
				['id'] = 0x2BE,
				['offset'] = 6,
			},
			["703"] = {
				['id'] = 0x2BF,
				['offset'] = 7,
			},
			["704"] = {
				['id'] = 0x2C0,
				['offset'] = 8,
			},
			["705"] = {
				['id'] = 0x2C1,
				['offset'] = 9,
			},
			["706"] = {
				['id'] = 0x2C2,
				['offset'] = 10,
			},
		},
		["LIFE"] = {
			["707"] = {
				['id'] = 0x2C3,
				['offset'] = 0,
			},
			["708"] = {
				['id'] = 0x2C4,
				['offset'] = 1,
			},
			["709"] = {
				['id'] = 0x2C5,
				['offset'] = 2,
			},
			["710"] = {
				['id'] = 0x2C6,
				['offset'] = 3,
			},
		},
		["TIP"] = {
			["711"] = {
				['id'] = 0x2C7,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			["712"] = {
				['id'] = 0x2C8,
				['offset'] = 0,
			},
			["713"] = {
				['id'] = 0x2C9,
				['offset'] = 1,
			},
			["714"] = {
				['id'] = 0x2CA,
				['offset'] = 2,
			},
		},
		["SWITCH"] = {
			["715"] = {
				['id'] = 0x2CB,
				['offset'] = 0,
			},
			["716"] = {
				['id'] = 0x2CC,
				['offset'] = 1,
			},
			["717"] = {
				['id'] = 0x2CD,
				['offset'] = 2,
			},
			["718"] = {
				['id'] = 0x2CE,
				['offset'] = 3,
			},
			["719"] = {
				['id'] = 0x2CF,
				['offset'] = 4,
			},
			["720"] = {
				['id'] = 0x2D0,
				['offset'] = 5,
			},
			["721"] = {
				['id'] = 0x2D1,
				['offset'] = 6,
			},
			["722"] = {
				['id'] = 0x2D2,
				['offset'] = 7,
			},
		},
	},
	["AP_PIRATES_L2"] = {
		["GOAL"] = "803",
		["GARIBS"] = {
			["724"] = {
				['id'] = 0x2D4,
				['offset'] = 0,
			},
			["725"] = {
				['id'] = 0x2D5,
				['offset'] = 1,
			},
			["726"] = {
				['id'] = 0x2D6,
				['offset'] = 2,
			},
			["727"] = {
				['id'] = 0x2D7,
				['offset'] = 3,
			},
			["728"] = {
				['id'] = 0x2D8,
				['offset'] = 4,
			},
			["729"] = {
				['id'] = 0x2D9,
				['offset'] = 5,
			},
			["730"] = {
				['id'] = 0x2DA,
				['offset'] = 6,
			},
			["731"] = {
				['id'] = 0x2DB,
				['offset'] = 7,
			},
			["732"] = {
				['id'] = 0x2DC,
				['offset'] = 8,
			},
			["733"] = {
				['id'] = 0x2DD,
				['offset'] = 9,
			},
			["734"] = {
				['id'] = 0x2DE,
				['offset'] = 10,
			},
			["735"] = {
				['id'] = 0x2DF,
				['offset'] = 11,
			},
			["736"] = {
				['id'] = 0x2E0,
				['offset'] = 12,
			},
			["737"] = {
				['id'] = 0x2E1,
				['offset'] = 13,
			},
			["738"] = {
				['id'] = 0x2E2,
				['offset'] = 14,
			},
			["739"] = {
				['id'] = 0x2E3,
				['offset'] = 15,
			},
			["740"] = {
				['id'] = 0x2E4,
				['offset'] = 16,
			},
			["741"] = {
				['id'] = 0x2E5,
				['offset'] = 17,
			},
			["742"] = {
				['id'] = 0x2E6,
				['offset'] = 18,
			},
			["743"] = {
				['id'] = 0x2E7,
				['offset'] = 19,
			},
			["744"] = {
				['id'] = 0x2E8,
				['offset'] = 20,
			},
			["745"] = {
				['id'] = 0x2E9,
				['offset'] = 21,
			},
			["746"] = {
				['id'] = 0x2EA,
				['offset'] = 22,
			},
			["747"] = {
				['id'] = 0x2EB,
				['offset'] = 23,
			},
			["748"] = {
				['id'] = 0x2EC,
				['offset'] = 24,
			},
			["749"] = {
				['id'] = 0x2ED,
				['offset'] = 25,
			},
			["750"] = {
				['id'] = 0x2EE,
				['offset'] = 26,
			},
			["751"] = {
				['id'] = 0x2EF,
				['offset'] = 27,
			},
			["752"] = {
				['id'] = 0x2F0,
				['offset'] = 28,
			},
			["753"] = {
				['id'] = 0x2F1,
				['offset'] = 29,
			},
			["754"] = {
				['id'] = 0x2F2,
				['offset'] = 30,
			},
			["755"] = {
				['id'] = 0x2F3,
				['offset'] = 31,
			},
			["756"] = {
				['id'] = 0x2F4,
				['offset'] = 32,
			},
			["757"] = {
				['id'] = 0x2F5,
				['offset'] = 33,
			},
			["758"] = {
				['id'] = 0x2F6,
				['offset'] = 34,
			},
			["759"] = {
				['id'] = 0x2F7,
				['offset'] = 35,
			},
			["760"] = {
				['id'] = 0x2F8,
				['offset'] = 36,
			},
			["761"] = {
				['id'] = 0x2F9,
				['offset'] = 37,
			},
			["762"] = {
				['id'] = 0x2FA,
				['offset'] = 38,
			},
			["763"] = {
				['id'] = 0x2FB,
				['offset'] = 39,
			},
			["764"] = {
				['id'] = 0x2FC,
				['offset'] = 40,
			},
			["765"] = {
				['id'] = 0x2FD,
				['offset'] = 41,
			},
			["766"] = {
				['id'] = 0x2FE,
				['offset'] = 42,
			},
			["767"] = {
				['id'] = 0x2FF,
				['offset'] = 43,
			},
			["768"] = {
				['id'] = 0x300,
				['offset'] = 44,
			},
			["769"] = {
				['id'] = 0x301,
				['offset'] = 45,
			},
			["770"] = {
				['id'] = 0x302,
				['offset'] = 46,
			},
			["771"] = {
				['id'] = 0x303,
				['offset'] = 47,
			},
			["772"] = {
				['id'] = 0x304,
				['offset'] = 48,
			},
			["773"] = {
				['id'] = 0x305,
				['offset'] = 49,
			},
			["774"] = {
				['id'] = 0x306,
				['offset'] = 50,
			},
			["775"] = {
				['id'] = 0x307,
				['offset'] = 51,
			},
		},
		["ENEMY_GARIBS"] = {
			["776"] = {
				['id'] = 0x308,
				['offset'] = 52,
				['object_id'] = 0x310,
			},
			["777"] = {
				['id'] = 0x309,
				['offset'] = 53,
				['object_id'] = 0x311,
			},
			["778"] = {
				['id'] = 0x30A,
				['offset'] = 54,
				['object_id'] = 0x312,
			},
			["779"] = {
				['id'] = 0x30B,
				['offset'] = 55,
				['object_id'] = 0x313,
			},
			["780"] = {
				['id'] = 0x30C,
				['offset'] = 56,
				['object_id'] = 0x314,
			},
			["781"] = {
				['id'] = 0x30D,
				['offset'] = 57,
				['object_id'] = 0x316,
			},
			["782"] = {
				['id'] = 0x30E,
				['offset'] = 58,
				['object_id'] = 0x317,
			},
			["783"] = {
				['id'] = 0x30F,
				['offset'] = 59,
				['object_id'] = 0x319,
			},
		},
		["ENEMIES"] = {
			["784"] = {
				['id'] = 0x310,
				['offset'] = 0,
			},
			["785"] = {
				['id'] = 0x311,
				['offset'] = 1,
			},
			["786"] = {
				['id'] = 0x312,
				['offset'] = 2,
			},
			["787"] = {
				['id'] = 0x313,
				['offset'] = 3,
			},
			["788"] = {
				['id'] = 0x314,
				['offset'] = 4,
			},
			["789"] = {
				['id'] = 0x315,
				['offset'] = 5,
			},
			["790"] = {
				['id'] = 0x316,
				['offset'] = 6,
			},
			["791"] = {
				['id'] = 0x317,
				['offset'] = 7,
			},
			["792"] = {
				['id'] = 0x318,
				['offset'] = 8,
			},
			["793"] = {
				['id'] = 0x319,
				['offset'] = 9,
			},
		},
		["LIFE"] = {
			["794"] = {
				['id'] = 0x31A,
				['offset'] = 0,
			},
			["795"] = {
				['id'] = 0x31B,
				['offset'] = 1,
			},
			["796"] = {
				['id'] = 0x31C,
				['offset'] = 2,
			},
		},
		["CHECKPOINT"] = {
			["797"] = {
				['id'] = 0x31D,
				['offset'] = 0,
			},
			["798"] = {
				['id'] = 0x31E,
				['offset'] = 1,
			},
			["799"] = {
				['id'] = 0x31F,
				['offset'] = 2,
			},
		},
		["SWITCH"] = {
			["800"] = {
				['id'] = 0x320,
				['offset'] = 0,
			},
			["801"] = {
				['id'] = 0x321,
				['offset'] = 1,
			},
			["802"] = {
				['id'] = 0x322,
				['offset'] = 2,
			},
		},
	},
	["AP_PIRATES_L3"] = {
		["GOAL"] = "909",
		["GARIBS"] = {
			["804"] = {
				['id'] = 0x324,
				['offset'] = 0,
			},
			["805"] = {
				['id'] = 0x325,
				['offset'] = 1,
			},
			["806"] = {
				['id'] = 0x326,
				['offset'] = 2,
			},
			["807"] = {
				['id'] = 0x327,
				['offset'] = 3,
			},
			["808"] = {
				['id'] = 0x328,
				['offset'] = 4,
			},
			["809"] = {
				['id'] = 0x329,
				['offset'] = 5,
			},
			["810"] = {
				['id'] = 0x32A,
				['offset'] = 6,
			},
			["811"] = {
				['id'] = 0x32B,
				['offset'] = 7,
			},
			["812"] = {
				['id'] = 0x32C,
				['offset'] = 8,
			},
			["813"] = {
				['id'] = 0x32D,
				['offset'] = 9,
			},
			["814"] = {
				['id'] = 0x32E,
				['offset'] = 10,
			},
			["815"] = {
				['id'] = 0x32F,
				['offset'] = 11,
			},
			["816"] = {
				['id'] = 0x330,
				['offset'] = 12,
			},
			["817"] = {
				['id'] = 0x331,
				['offset'] = 13,
			},
			["818"] = {
				['id'] = 0x332,
				['offset'] = 14,
			},
			["819"] = {
				['id'] = 0x333,
				['offset'] = 15,
			},
			["820"] = {
				['id'] = 0x334,
				['offset'] = 16,
			},
			["821"] = {
				['id'] = 0x335,
				['offset'] = 17,
			},
			["822"] = {
				['id'] = 0x336,
				['offset'] = 18,
			},
			["823"] = {
				['id'] = 0x337,
				['offset'] = 19,
			},
			["824"] = {
				['id'] = 0x338,
				['offset'] = 20,
			},
			["825"] = {
				['id'] = 0x339,
				['offset'] = 21,
			},
			["826"] = {
				['id'] = 0x33A,
				['offset'] = 22,
			},
			["827"] = {
				['id'] = 0x33B,
				['offset'] = 23,
			},
			["828"] = {
				['id'] = 0x33C,
				['offset'] = 24,
			},
			["829"] = {
				['id'] = 0x33D,
				['offset'] = 25,
			},
			["830"] = {
				['id'] = 0x33E,
				['offset'] = 26,
			},
			["831"] = {
				['id'] = 0x33F,
				['offset'] = 27,
			},
			["832"] = {
				['id'] = 0x340,
				['offset'] = 28,
			},
			["833"] = {
				['id'] = 0x341,
				['offset'] = 29,
			},
			["834"] = {
				['id'] = 0x342,
				['offset'] = 30,
			},
			["835"] = {
				['id'] = 0x343,
				['offset'] = 31,
			},
			["836"] = {
				['id'] = 0x344,
				['offset'] = 32,
			},
			["837"] = {
				['id'] = 0x345,
				['offset'] = 33,
			},
			["838"] = {
				['id'] = 0x346,
				['offset'] = 34,
			},
			["839"] = {
				['id'] = 0x347,
				['offset'] = 35,
			},
			["840"] = {
				['id'] = 0x348,
				['offset'] = 36,
			},
			["841"] = {
				['id'] = 0x349,
				['offset'] = 37,
			},
			["842"] = {
				['id'] = 0x34A,
				['offset'] = 38,
			},
			["843"] = {
				['id'] = 0x34B,
				['offset'] = 39,
			},
			["844"] = {
				['id'] = 0x34C,
				['offset'] = 40,
			},
			["845"] = {
				['id'] = 0x34D,
				['offset'] = 41,
			},
			["846"] = {
				['id'] = 0x34E,
				['offset'] = 42,
			},
			["847"] = {
				['id'] = 0x34F,
				['offset'] = 43,
			},
			["848"] = {
				['id'] = 0x350,
				['offset'] = 44,
			},
			["849"] = {
				['id'] = 0x351,
				['offset'] = 45,
			},
			["850"] = {
				['id'] = 0x352,
				['offset'] = 46,
			},
			["851"] = {
				['id'] = 0x353,
				['offset'] = 47,
			},
			["852"] = {
				['id'] = 0x354,
				['offset'] = 48,
			},
			["853"] = {
				['id'] = 0x355,
				['offset'] = 49,
			},
			["854"] = {
				['id'] = 0x356,
				['offset'] = 50,
			},
			["855"] = {
				['id'] = 0x357,
				['offset'] = 51,
			},
			["856"] = {
				['id'] = 0x358,
				['offset'] = 52,
			},
			["857"] = {
				['id'] = 0x359,
				['offset'] = 53,
			},
			["858"] = {
				['id'] = 0x35A,
				['offset'] = 54,
			},
			["859"] = {
				['id'] = 0x35B,
				['offset'] = 55,
			},
			["860"] = {
				['id'] = 0x35C,
				['offset'] = 56,
			},
			["861"] = {
				['id'] = 0x35D,
				['offset'] = 57,
			},
			["862"] = {
				['id'] = 0x35E,
				['offset'] = 58,
			},
			["863"] = {
				['id'] = 0x35F,
				['offset'] = 59,
			},
			["864"] = {
				['id'] = 0x360,
				['offset'] = 60,
			},
			["865"] = {
				['id'] = 0x361,
				['offset'] = 61,
			},
			["866"] = {
				['id'] = 0x362,
				['offset'] = 62,
			},
			["867"] = {
				['id'] = 0x363,
				['offset'] = 63,
			},
			["868"] = {
				['id'] = 0x364,
				['offset'] = 64,
			},
			["869"] = {
				['id'] = 0x365,
				['offset'] = 65,
			},
			["870"] = {
				['id'] = 0x366,
				['offset'] = 66,
			},
			["871"] = {
				['id'] = 0x367,
				['offset'] = 67,
			},
			["872"] = {
				['id'] = 0x368,
				['offset'] = 68,
			},
			["873"] = {
				['id'] = 0x369,
				['offset'] = 69,
			},
			["874"] = {
				['id'] = 0x36A,
				['offset'] = 70,
			},
			["875"] = {
				['id'] = 0x36B,
				['offset'] = 71,
			},
			["876"] = {
				['id'] = 0x36C,
				['offset'] = 72,
			},
			["877"] = {
				['id'] = 0x36D,
				['offset'] = 73,
			},
		},
		["ENEMY_GARIBS"] = {
			["878"] = {
				['id'] = 0x36E,
				['offset'] = 74,
				['object_id'] = 0x377,
			},
			["879"] = {
				['id'] = 0x36F,
				['offset'] = 75,
				['object_id'] = 0x379,
			},
			["880"] = {
				['id'] = 0x370,
				['offset'] = 76,
				['object_id'] = 0x37A,
			},
			["881"] = {
				['id'] = 0x371,
				['offset'] = 77,
				['object_id'] = 0x37B,
			},
			["882"] = {
				['id'] = 0x372,
				['offset'] = 78,
				['object_id'] = 0x37C,
			},
			["883"] = {
				['id'] = 0x373,
				['offset'] = 79,
				['object_id'] = 0x37D,
			},
		},
		["ENEMIES"] = {
			["884"] = {
				['id'] = 0x374,
				['offset'] = 0,
			},
			["885"] = {
				['id'] = 0x375,
				['offset'] = 1,
			},
			["886"] = {
				['id'] = 0x376,
				['offset'] = 2,
			},
			["887"] = {
				['id'] = 0x377,
				['offset'] = 3,
			},
			["888"] = {
				['id'] = 0x378,
				['offset'] = 4,
			},
			["889"] = {
				['id'] = 0x379,
				['offset'] = 5,
			},
			["890"] = {
				['id'] = 0x37A,
				['offset'] = 6,
			},
			["891"] = {
				['id'] = 0x37B,
				['offset'] = 7,
			},
			["892"] = {
				['id'] = 0x37C,
				['offset'] = 8,
			},
			["893"] = {
				['id'] = 0x37D,
				['offset'] = 9,
			},
		},
		["LIFE"] = {
			["894"] = {
				['id'] = 0x37E,
				['offset'] = 0,
			},
			["895"] = {
				['id'] = 0x37F,
				['offset'] = 1,
			},
			["896"] = {
				['id'] = 0x380,
				['offset'] = 2,
			},
			["897"] = {
				['id'] = 0x381,
				['offset'] = 3,
			},
			["898"] = {
				['id'] = 0x382,
				['offset'] = 4,
			},
			["899"] = {
				['id'] = 0x383,
				['offset'] = 5,
			},
		},
		["TIP"] = {
			["900"] = {
				['id'] = 0x384,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			["901"] = {
				['id'] = 0x385,
				['offset'] = 0,
			},
			["902"] = {
				['id'] = 0x386,
				['offset'] = 1,
			},
			["903"] = {
				['id'] = 0x387,
				['offset'] = 2,
			},
			["904"] = {
				['id'] = 0x388,
				['offset'] = 3,
			},
		},
		["SWITCH"] = {
			["905"] = {
				['id'] = 0x389,
				['offset'] = 0,
			},
			["906"] = {
				['id'] = 0x38A,
				['offset'] = 1,
			},
			["907"] = {
				['id'] = 0x38B,
				['offset'] = 2,
			},
			["908"] = {
				['id'] = 0x38C,
				['offset'] = 3,
			},
		},
		["POTIONS"] = {
			["910"] = {
				['id'] = 0x38E,
				['offset'] = 0,
			},
			["911"] = {
				['id'] = 0x38F,
				['offset'] = 1,
			},
		},
	},
	["AP_PIRATES_BOSS"] = {
		["GOAL"] = "912",
	},
	["AP_PIRATES_BONUS"] = {
		["GOAL"] = "968",
		["GARIBS"] = {
			["913"] = {
				['id'] = 0x391,
				['offset'] = 0,
			},
			["914"] = {
				['id'] = 0x392,
				['offset'] = 1,
			},
			["915"] = {
				['id'] = 0x393,
				['offset'] = 2,
			},
			["916"] = {
				['id'] = 0x394,
				['offset'] = 3,
			},
			["917"] = {
				['id'] = 0x395,
				['offset'] = 4,
			},
			["918"] = {
				['id'] = 0x396,
				['offset'] = 5,
			},
			["919"] = {
				['id'] = 0x397,
				['offset'] = 6,
			},
			["920"] = {
				['id'] = 0x398,
				['offset'] = 7,
			},
			["921"] = {
				['id'] = 0x399,
				['offset'] = 8,
			},
			["922"] = {
				['id'] = 0x39A,
				['offset'] = 9,
			},
			["923"] = {
				['id'] = 0x39B,
				['offset'] = 10,
			},
			["924"] = {
				['id'] = 0x39C,
				['offset'] = 11,
			},
			["925"] = {
				['id'] = 0x39D,
				['offset'] = 12,
			},
			["926"] = {
				['id'] = 0x39E,
				['offset'] = 13,
			},
			["927"] = {
				['id'] = 0x39F,
				['offset'] = 14,
			},
			["928"] = {
				['id'] = 0x3A0,
				['offset'] = 15,
			},
			["929"] = {
				['id'] = 0x3A1,
				['offset'] = 16,
			},
			["930"] = {
				['id'] = 0x3A2,
				['offset'] = 17,
			},
			["931"] = {
				['id'] = 0x3A3,
				['offset'] = 18,
			},
			["932"] = {
				['id'] = 0x3A4,
				['offset'] = 19,
			},
			["933"] = {
				['id'] = 0x3A5,
				['offset'] = 20,
			},
			["934"] = {
				['id'] = 0x3A6,
				['offset'] = 21,
			},
			["935"] = {
				['id'] = 0x3A7,
				['offset'] = 22,
			},
			["936"] = {
				['id'] = 0x3A8,
				['offset'] = 23,
			},
			["937"] = {
				['id'] = 0x3A9,
				['offset'] = 24,
			},
			["938"] = {
				['id'] = 0x3AA,
				['offset'] = 25,
			},
			["939"] = {
				['id'] = 0x3AB,
				['offset'] = 26,
			},
			["940"] = {
				['id'] = 0x3AC,
				['offset'] = 27,
			},
			["941"] = {
				['id'] = 0x3AD,
				['offset'] = 28,
			},
			["942"] = {
				['id'] = 0x3AE,
				['offset'] = 29,
			},
			["943"] = {
				['id'] = 0x3AF,
				['offset'] = 30,
			},
			["944"] = {
				['id'] = 0x3B0,
				['offset'] = 31,
			},
			["945"] = {
				['id'] = 0x3B1,
				['offset'] = 32,
			},
			["946"] = {
				['id'] = 0x3B2,
				['offset'] = 33,
			},
			["947"] = {
				['id'] = 0x3B3,
				['offset'] = 34,
			},
			["948"] = {
				['id'] = 0x3B4,
				['offset'] = 35,
			},
			["949"] = {
				['id'] = 0x3B5,
				['offset'] = 36,
			},
			["950"] = {
				['id'] = 0x3B6,
				['offset'] = 37,
			},
			["951"] = {
				['id'] = 0x3B7,
				['offset'] = 38,
			},
			["952"] = {
				['id'] = 0x3B8,
				['offset'] = 39,
			},
			["953"] = {
				['id'] = 0x3B9,
				['offset'] = 40,
			},
			["954"] = {
				['id'] = 0x3BA,
				['offset'] = 41,
			},
			["955"] = {
				['id'] = 0x3BB,
				['offset'] = 42,
			},
			["956"] = {
				['id'] = 0x3BC,
				['offset'] = 43,
			},
			["957"] = {
				['id'] = 0x3BD,
				['offset'] = 44,
			},
			["958"] = {
				['id'] = 0x3BE,
				['offset'] = 45,
			},
			["959"] = {
				['id'] = 0x3BF,
				['offset'] = 46,
			},
			["960"] = {
				['id'] = 0x3C0,
				['offset'] = 47,
			},
			["961"] = {
				['id'] = 0x3C1,
				['offset'] = 48,
			},
			["962"] = {
				['id'] = 0x3C2,
				['offset'] = 49,
			},
		},
		["ENEMIES"] = {
			["963"] = {
				['id'] = 0x3C3,
				['offset'] = 0,
			},
		},
		["LIFE"] = {
			["964"] = {
				['id'] = 0x3C4,
				['offset'] = 0,
			},
			["965"] = {
				['id'] = 0x3C5,
				['offset'] = 1,
			},
			["966"] = {
				['id'] = 0x3C6,
				['offset'] = 2,
			},
			["967"] = {
				['id'] = 0x3C7,
				['offset'] = 3,
			},
		},
	},
	["AP_PREHISTORIC_L1"] = {
		["GOAL"] = "1059",
		["GARIBS"] = {
			["970"] = {
				['id'] = 0x3CA,
				['offset'] = 0,
			},
			["971"] = {
				['id'] = 0x3CB,
				['offset'] = 1,
			},
			["972"] = {
				['id'] = 0x3CC,
				['offset'] = 2,
			},
			["973"] = {
				['id'] = 0x3CD,
				['offset'] = 3,
			},
			["974"] = {
				['id'] = 0x3CE,
				['offset'] = 4,
			},
			["975"] = {
				['id'] = 0x3CF,
				['offset'] = 5,
			},
			["976"] = {
				['id'] = 0x3D0,
				['offset'] = 6,
			},
			["977"] = {
				['id'] = 0x3D1,
				['offset'] = 7,
			},
			["978"] = {
				['id'] = 0x3D2,
				['offset'] = 8,
			},
			["979"] = {
				['id'] = 0x3D3,
				['offset'] = 9,
			},
			["980"] = {
				['id'] = 0x3D4,
				['offset'] = 10,
			},
			["981"] = {
				['id'] = 0x3D5,
				['offset'] = 11,
			},
			["982"] = {
				['id'] = 0x3D6,
				['offset'] = 12,
			},
			["983"] = {
				['id'] = 0x3D7,
				['offset'] = 13,
			},
			["984"] = {
				['id'] = 0x3D8,
				['offset'] = 14,
			},
			["985"] = {
				['id'] = 0x3D9,
				['offset'] = 15,
			},
			["986"] = {
				['id'] = 0x3DA,
				['offset'] = 16,
			},
			["987"] = {
				['id'] = 0x3DB,
				['offset'] = 17,
			},
			["988"] = {
				['id'] = 0x3DC,
				['offset'] = 18,
			},
			["989"] = {
				['id'] = 0x3DD,
				['offset'] = 19,
			},
			["990"] = {
				['id'] = 0x3DE,
				['offset'] = 20,
			},
			["991"] = {
				['id'] = 0x3DF,
				['offset'] = 21,
			},
			["992"] = {
				['id'] = 0x3E0,
				['offset'] = 22,
			},
			["993"] = {
				['id'] = 0x3E1,
				['offset'] = 23,
			},
			["994"] = {
				['id'] = 0x3E2,
				['offset'] = 24,
			},
			["995"] = {
				['id'] = 0x3E3,
				['offset'] = 25,
			},
			["996"] = {
				['id'] = 0x3E4,
				['offset'] = 26,
			},
			["997"] = {
				['id'] = 0x3E5,
				['offset'] = 27,
			},
			["998"] = {
				['id'] = 0x3E6,
				['offset'] = 28,
			},
			["999"] = {
				['id'] = 0x3E7,
				['offset'] = 29,
			},
			["1000"] = {
				['id'] = 0x3E8,
				['offset'] = 30,
			},
			["1001"] = {
				['id'] = 0x3E9,
				['offset'] = 31,
			},
			["1002"] = {
				['id'] = 0x3EA,
				['offset'] = 32,
			},
			["1003"] = {
				['id'] = 0x3EB,
				['offset'] = 33,
			},
			["1004"] = {
				['id'] = 0x3EC,
				['offset'] = 34,
			},
			["1005"] = {
				['id'] = 0x3ED,
				['offset'] = 35,
			},
			["1006"] = {
				['id'] = 0x3EE,
				['offset'] = 36,
			},
			["1007"] = {
				['id'] = 0x3EF,
				['offset'] = 37,
			},
			["1008"] = {
				['id'] = 0x3F0,
				['offset'] = 38,
			},
			["1009"] = {
				['id'] = 0x3F1,
				['offset'] = 39,
			},
			["1010"] = {
				['id'] = 0x3F2,
				['offset'] = 40,
			},
			["1011"] = {
				['id'] = 0x3F3,
				['offset'] = 41,
			},
			["1012"] = {
				['id'] = 0x3F4,
				['offset'] = 42,
			},
			["1013"] = {
				['id'] = 0x3F5,
				['offset'] = 43,
			},
			["1014"] = {
				['id'] = 0x3F6,
				['offset'] = 44,
			},
			["1015"] = {
				['id'] = 0x3F7,
				['offset'] = 45,
			},
			["1016"] = {
				['id'] = 0x3F8,
				['offset'] = 46,
			},
			["1017"] = {
				['id'] = 0x3F9,
				['offset'] = 47,
			},
			["1018"] = {
				['id'] = 0x3FA,
				['offset'] = 48,
			},
			["1019"] = {
				['id'] = 0x3FB,
				['offset'] = 49,
			},
			["1020"] = {
				['id'] = 0x3FC,
				['offset'] = 50,
			},
			["1021"] = {
				['id'] = 0x3FD,
				['offset'] = 51,
			},
			["1022"] = {
				['id'] = 0x3FE,
				['offset'] = 52,
			},
			["1023"] = {
				['id'] = 0x3FF,
				['offset'] = 53,
			},
			["1024"] = {
				['id'] = 0x400,
				['offset'] = 54,
			},
			["1025"] = {
				['id'] = 0x401,
				['offset'] = 55,
			},
			["1026"] = {
				['id'] = 0x402,
				['offset'] = 56,
			},
			["1027"] = {
				['id'] = 0x403,
				['offset'] = 57,
			},
			["1028"] = {
				['id'] = 0x404,
				['offset'] = 58,
			},
			["1029"] = {
				['id'] = 0x405,
				['offset'] = 59,
			},
			["1030"] = {
				['id'] = 0x406,
				['offset'] = 60,
			},
			["1031"] = {
				['id'] = 0x407,
				['offset'] = 61,
			},
			["1032"] = {
				['id'] = 0x408,
				['offset'] = 62,
			},
			["1033"] = {
				['id'] = 0x409,
				['offset'] = 63,
			},
			["1034"] = {
				['id'] = 0x40A,
				['offset'] = 64,
			},
			["1035"] = {
				['id'] = 0x40B,
				['offset'] = 65,
			},
			["1036"] = {
				['id'] = 0x40C,
				['offset'] = 66,
			},
			["1037"] = {
				['id'] = 0x40D,
				['offset'] = 67,
			},
			["1038"] = {
				['id'] = 0x40E,
				['offset'] = 68,
			},
			["1039"] = {
				['id'] = 0x40F,
				['offset'] = 69,
			},
			["1040"] = {
				['id'] = 0x410,
				['offset'] = 70,
			},
			["1041"] = {
				['id'] = 0x411,
				['offset'] = 71,
			},
			["1042"] = {
				['id'] = 0x412,
				['offset'] = 72,
			},
			["1043"] = {
				['id'] = 0x413,
				['offset'] = 73,
			},
			["1044"] = {
				['id'] = 0x414,
				['offset'] = 74,
			},
			["1045"] = {
				['id'] = 0x415,
				['offset'] = 75,
			},
			["1046"] = {
				['id'] = 0x416,
				['offset'] = 76,
			},
			["1047"] = {
				['id'] = 0x417,
				['offset'] = 77,
			},
			["1048"] = {
				['id'] = 0x418,
				['offset'] = 78,
			},
		},
		["ENEMY_GARIBS"] = {
			["1049"] = {
				['id'] = 0x419,
				['offset'] = 79,
				['object_id'] = 0x41B,
			},
		},
		["ENEMIES"] = {
			["1050"] = {
				['id'] = 0x41A,
				['offset'] = 0,
			},
			["1051"] = {
				['id'] = 0x41B,
				['offset'] = 1,
			},
		},
		["LIFE"] = {
			["1052"] = {
				['id'] = 0x41C,
				['offset'] = 0,
			},
			["1053"] = {
				['id'] = 0x41D,
				['offset'] = 1,
			},
			["1054"] = {
				['id'] = 0x41E,
				['offset'] = 2,
			},
			["1055"] = {
				['id'] = 0x41F,
				['offset'] = 3,
			},
		},
		["CHECKPOINT"] = {
			["1056"] = {
				['id'] = 0x420,
				['offset'] = 0,
			},
			["1057"] = {
				['id'] = 0x421,
				['offset'] = 1,
			},
			["1058"] = {
				['id'] = 0x422,
				['offset'] = 2,
			},
		},
	},
	["AP_PREHISTORIC_L2"] = {
		["GOAL"] = "1159",
		["GARIBS"] = {
			["1060"] = {
				['id'] = 0x424,
				['offset'] = 0,
			},
			["1061"] = {
				['id'] = 0x425,
				['offset'] = 1,
			},
			["1062"] = {
				['id'] = 0x426,
				['offset'] = 2,
			},
			["1063"] = {
				['id'] = 0x427,
				['offset'] = 3,
			},
			["1064"] = {
				['id'] = 0x428,
				['offset'] = 4,
			},
			["1065"] = {
				['id'] = 0x429,
				['offset'] = 5,
			},
			["1066"] = {
				['id'] = 0x42A,
				['offset'] = 6,
			},
			["1067"] = {
				['id'] = 0x42B,
				['offset'] = 7,
			},
			["1068"] = {
				['id'] = 0x42C,
				['offset'] = 8,
			},
			["1069"] = {
				['id'] = 0x42D,
				['offset'] = 9,
			},
			["1070"] = {
				['id'] = 0x42E,
				['offset'] = 10,
			},
			["1071"] = {
				['id'] = 0x42F,
				['offset'] = 11,
			},
			["1072"] = {
				['id'] = 0x430,
				['offset'] = 12,
			},
			["1073"] = {
				['id'] = 0x431,
				['offset'] = 13,
			},
			["1074"] = {
				['id'] = 0x432,
				['offset'] = 14,
			},
			["1075"] = {
				['id'] = 0x433,
				['offset'] = 15,
			},
			["1076"] = {
				['id'] = 0x434,
				['offset'] = 16,
			},
			["1077"] = {
				['id'] = 0x435,
				['offset'] = 17,
			},
			["1078"] = {
				['id'] = 0x436,
				['offset'] = 18,
			},
			["1079"] = {
				['id'] = 0x437,
				['offset'] = 19,
			},
			["1080"] = {
				['id'] = 0x438,
				['offset'] = 20,
			},
			["1081"] = {
				['id'] = 0x439,
				['offset'] = 21,
			},
			["1082"] = {
				['id'] = 0x43A,
				['offset'] = 22,
			},
			["1083"] = {
				['id'] = 0x43B,
				['offset'] = 23,
			},
			["1084"] = {
				['id'] = 0x43C,
				['offset'] = 24,
			},
			["1085"] = {
				['id'] = 0x43D,
				['offset'] = 25,
			},
			["1086"] = {
				['id'] = 0x43E,
				['offset'] = 26,
			},
			["1087"] = {
				['id'] = 0x43F,
				['offset'] = 27,
			},
			["1088"] = {
				['id'] = 0x440,
				['offset'] = 28,
			},
			["1089"] = {
				['id'] = 0x441,
				['offset'] = 29,
			},
			["1090"] = {
				['id'] = 0x442,
				['offset'] = 30,
			},
			["1091"] = {
				['id'] = 0x443,
				['offset'] = 31,
			},
			["1092"] = {
				['id'] = 0x444,
				['offset'] = 32,
			},
			["1093"] = {
				['id'] = 0x445,
				['offset'] = 33,
			},
			["1094"] = {
				['id'] = 0x446,
				['offset'] = 34,
			},
			["1095"] = {
				['id'] = 0x447,
				['offset'] = 35,
			},
			["1096"] = {
				['id'] = 0x448,
				['offset'] = 36,
			},
			["1097"] = {
				['id'] = 0x449,
				['offset'] = 37,
			},
			["1098"] = {
				['id'] = 0x44A,
				['offset'] = 38,
			},
			["1099"] = {
				['id'] = 0x44B,
				['offset'] = 39,
			},
			["1100"] = {
				['id'] = 0x44C,
				['offset'] = 40,
			},
			["1101"] = {
				['id'] = 0x44D,
				['offset'] = 41,
			},
			["1102"] = {
				['id'] = 0x44E,
				['offset'] = 42,
			},
			["1103"] = {
				['id'] = 0x44F,
				['offset'] = 43,
			},
			["1104"] = {
				['id'] = 0x450,
				['offset'] = 44,
			},
			["1105"] = {
				['id'] = 0x451,
				['offset'] = 45,
			},
			["1106"] = {
				['id'] = 0x452,
				['offset'] = 46,
			},
			["1107"] = {
				['id'] = 0x453,
				['offset'] = 47,
			},
			["1108"] = {
				['id'] = 0x454,
				['offset'] = 48,
			},
			["1109"] = {
				['id'] = 0x455,
				['offset'] = 49,
			},
			["1110"] = {
				['id'] = 0x456,
				['offset'] = 50,
			},
			["1111"] = {
				['id'] = 0x457,
				['offset'] = 51,
			},
			["1112"] = {
				['id'] = 0x458,
				['offset'] = 52,
			},
			["1113"] = {
				['id'] = 0x459,
				['offset'] = 53,
			},
			["1114"] = {
				['id'] = 0x45A,
				['offset'] = 54,
			},
			["1115"] = {
				['id'] = 0x45B,
				['offset'] = 55,
			},
			["1116"] = {
				['id'] = 0x45C,
				['offset'] = 56,
			},
			["1117"] = {
				['id'] = 0x45D,
				['offset'] = 57,
			},
			["1118"] = {
				['id'] = 0x45E,
				['offset'] = 58,
			},
			["1119"] = {
				['id'] = 0x45F,
				['offset'] = 59,
			},
			["1120"] = {
				['id'] = 0x460,
				['offset'] = 60,
			},
			["1121"] = {
				['id'] = 0x461,
				['offset'] = 61,
			},
			["1122"] = {
				['id'] = 0x462,
				['offset'] = 62,
			},
			["1123"] = {
				['id'] = 0x463,
				['offset'] = 63,
			},
			["1124"] = {
				['id'] = 0x464,
				['offset'] = 64,
			},
			["1125"] = {
				['id'] = 0x465,
				['offset'] = 65,
			},
			["1126"] = {
				['id'] = 0x466,
				['offset'] = 66,
			},
			["1127"] = {
				['id'] = 0x467,
				['offset'] = 67,
			},
			["1128"] = {
				['id'] = 0x468,
				['offset'] = 68,
			},
			["1129"] = {
				['id'] = 0x469,
				['offset'] = 69,
			},
			["1130"] = {
				['id'] = 0x46A,
				['offset'] = 70,
			},
			["1131"] = {
				['id'] = 0x46B,
				['offset'] = 71,
			},
			["1132"] = {
				['id'] = 0x46C,
				['offset'] = 72,
			},
			["1133"] = {
				['id'] = 0x46D,
				['offset'] = 73,
			},
			["1134"] = {
				['id'] = 0x46E,
				['offset'] = 74,
			},
			["1135"] = {
				['id'] = 0x46F,
				['offset'] = 75,
			},
			["1136"] = {
				['id'] = 0x470,
				['offset'] = 76,
			},
		},
		["ENEMY_GARIBS"] = {
			["1137"] = {
				['id'] = 0x471,
				['offset'] = 77,
				['object_id'] = 0x475,
			},
			["1138"] = {
				['id'] = 0x472,
				['offset'] = 78,
				['object_id'] = 0x478,
			},
			["1139"] = {
				['id'] = 0x473,
				['offset'] = 79,
				['object_id'] = 0x47A,
			},
		},
		["ENEMIES"] = {
			["1140"] = {
				['id'] = 0x474,
				['offset'] = 0,
			},
			["1141"] = {
				['id'] = 0x475,
				['offset'] = 1,
			},
			["1142"] = {
				['id'] = 0x476,
				['offset'] = 2,
			},
			["1143"] = {
				['id'] = 0x477,
				['offset'] = 3,
			},
			["1144"] = {
				['id'] = 0x478,
				['offset'] = 4,
			},
			["1145"] = {
				['id'] = 0x479,
				['offset'] = 5,
			},
			["1146"] = {
				['id'] = 0x47A,
				['offset'] = 6,
			},
		},
		["LIFE"] = {
			["1147"] = {
				['id'] = 0x47B,
				['offset'] = 0,
			},
			["1148"] = {
				['id'] = 0x47C,
				['offset'] = 1,
			},
			["1149"] = {
				['id'] = 0x47D,
				['offset'] = 2,
			},
			["1150"] = {
				['id'] = 0x47E,
				['offset'] = 3,
			},
			["1151"] = {
				['id'] = 0x47F,
				['offset'] = 4,
			},
		},
		["CHECKPOINT"] = {
			["1152"] = {
				['id'] = 0x480,
				['offset'] = 0,
			},
			["1153"] = {
				['id'] = 0x481,
				['offset'] = 1,
			},
			["1154"] = {
				['id'] = 0x482,
				['offset'] = 2,
			},
			["1155"] = {
				['id'] = 0x483,
				['offset'] = 3,
			},
		},
		["SWITCH"] = {
			["1156"] = {
				['id'] = 0x484,
				['offset'] = 0,
			},
			["1157"] = {
				['id'] = 0x485,
				['offset'] = 1,
			},
			["1158"] = {
				['id'] = 0x486,
				['offset'] = 2,
			},
		},
	},
	["AP_PREHISTORIC_L3"] = {
		["GOAL"] = "1260",
		["GARIBS"] = {
			["1160"] = {
				['id'] = 0x488,
				['offset'] = 0,
			},
			["1161"] = {
				['id'] = 0x489,
				['offset'] = 1,
			},
			["1162"] = {
				['id'] = 0x48A,
				['offset'] = 2,
			},
			["1163"] = {
				['id'] = 0x48B,
				['offset'] = 3,
			},
			["1164"] = {
				['id'] = 0x48C,
				['offset'] = 4,
			},
			["1165"] = {
				['id'] = 0x48D,
				['offset'] = 5,
			},
			["1166"] = {
				['id'] = 0x48E,
				['offset'] = 6,
			},
			["1167"] = {
				['id'] = 0x48F,
				['offset'] = 7,
			},
			["1168"] = {
				['id'] = 0x490,
				['offset'] = 8,
			},
			["1169"] = {
				['id'] = 0x491,
				['offset'] = 9,
			},
			["1170"] = {
				['id'] = 0x492,
				['offset'] = 10,
			},
			["1171"] = {
				['id'] = 0x493,
				['offset'] = 11,
			},
			["1172"] = {
				['id'] = 0x494,
				['offset'] = 12,
			},
			["1173"] = {
				['id'] = 0x495,
				['offset'] = 13,
			},
			["1174"] = {
				['id'] = 0x496,
				['offset'] = 14,
			},
			["1175"] = {
				['id'] = 0x497,
				['offset'] = 15,
			},
			["1176"] = {
				['id'] = 0x498,
				['offset'] = 16,
			},
			["1177"] = {
				['id'] = 0x499,
				['offset'] = 17,
			},
			["1178"] = {
				['id'] = 0x49A,
				['offset'] = 18,
			},
			["1179"] = {
				['id'] = 0x49B,
				['offset'] = 19,
			},
			["1180"] = {
				['id'] = 0x49C,
				['offset'] = 20,
			},
			["1181"] = {
				['id'] = 0x49D,
				['offset'] = 21,
			},
			["1182"] = {
				['id'] = 0x49E,
				['offset'] = 22,
			},
			["1183"] = {
				['id'] = 0x49F,
				['offset'] = 23,
			},
			["1184"] = {
				['id'] = 0x4A0,
				['offset'] = 24,
			},
			["1185"] = {
				['id'] = 0x4A1,
				['offset'] = 25,
			},
			["1186"] = {
				['id'] = 0x4A2,
				['offset'] = 26,
			},
			["1187"] = {
				['id'] = 0x4A3,
				['offset'] = 27,
			},
			["1188"] = {
				['id'] = 0x4A4,
				['offset'] = 28,
			},
			["1189"] = {
				['id'] = 0x4A5,
				['offset'] = 29,
			},
			["1190"] = {
				['id'] = 0x4A6,
				['offset'] = 30,
			},
			["1191"] = {
				['id'] = 0x4A7,
				['offset'] = 31,
			},
			["1192"] = {
				['id'] = 0x4A8,
				['offset'] = 32,
			},
			["1193"] = {
				['id'] = 0x4A9,
				['offset'] = 33,
			},
			["1194"] = {
				['id'] = 0x4AA,
				['offset'] = 34,
			},
			["1195"] = {
				['id'] = 0x4AB,
				['offset'] = 35,
			},
			["1196"] = {
				['id'] = 0x4AC,
				['offset'] = 36,
			},
			["1197"] = {
				['id'] = 0x4AD,
				['offset'] = 37,
			},
			["1198"] = {
				['id'] = 0x4AE,
				['offset'] = 38,
			},
			["1199"] = {
				['id'] = 0x4AF,
				['offset'] = 39,
			},
			["1200"] = {
				['id'] = 0x4B0,
				['offset'] = 40,
			},
			["1201"] = {
				['id'] = 0x4B1,
				['offset'] = 41,
			},
			["1202"] = {
				['id'] = 0x4B2,
				['offset'] = 42,
			},
			["1203"] = {
				['id'] = 0x4B3,
				['offset'] = 43,
			},
			["1204"] = {
				['id'] = 0x4B4,
				['offset'] = 44,
			},
			["1205"] = {
				['id'] = 0x4B5,
				['offset'] = 45,
			},
			["1206"] = {
				['id'] = 0x4B6,
				['offset'] = 46,
			},
			["1207"] = {
				['id'] = 0x4B7,
				['offset'] = 47,
			},
			["1208"] = {
				['id'] = 0x4B8,
				['offset'] = 48,
			},
			["1209"] = {
				['id'] = 0x4B9,
				['offset'] = 49,
			},
			["1210"] = {
				['id'] = 0x4BA,
				['offset'] = 50,
			},
			["1211"] = {
				['id'] = 0x4BB,
				['offset'] = 51,
			},
			["1212"] = {
				['id'] = 0x4BC,
				['offset'] = 52,
			},
			["1213"] = {
				['id'] = 0x4BD,
				['offset'] = 53,
			},
			["1214"] = {
				['id'] = 0x4BE,
				['offset'] = 54,
			},
			["1215"] = {
				['id'] = 0x4BF,
				['offset'] = 55,
			},
			["1216"] = {
				['id'] = 0x4C0,
				['offset'] = 56,
			},
			["1217"] = {
				['id'] = 0x4C1,
				['offset'] = 57,
			},
			["1218"] = {
				['id'] = 0x4C2,
				['offset'] = 58,
			},
			["1219"] = {
				['id'] = 0x4C3,
				['offset'] = 59,
			},
			["1220"] = {
				['id'] = 0x4C4,
				['offset'] = 60,
			},
			["1221"] = {
				['id'] = 0x4C5,
				['offset'] = 61,
			},
			["1222"] = {
				['id'] = 0x4C6,
				['offset'] = 62,
			},
			["1223"] = {
				['id'] = 0x4C7,
				['offset'] = 63,
			},
			["1224"] = {
				['id'] = 0x4C8,
				['offset'] = 64,
			},
			["1225"] = {
				['id'] = 0x4C9,
				['offset'] = 65,
			},
			["1226"] = {
				['id'] = 0x4CA,
				['offset'] = 66,
			},
			["1227"] = {
				['id'] = 0x4CB,
				['offset'] = 67,
			},
			["1228"] = {
				['id'] = 0x4CC,
				['offset'] = 68,
			},
			["1229"] = {
				['id'] = 0x4CD,
				['offset'] = 69,
			},
			["1230"] = {
				['id'] = 0x4CE,
				['offset'] = 70,
			},
			["1231"] = {
				['id'] = 0x4CF,
				['offset'] = 71,
			},
			["1232"] = {
				['id'] = 0x4D0,
				['offset'] = 72,
			},
			["1233"] = {
				['id'] = 0x4D1,
				['offset'] = 73,
			},
			["1234"] = {
				['id'] = 0x4D2,
				['offset'] = 74,
			},
			["1235"] = {
				['id'] = 0x4D3,
				['offset'] = 75,
			},
			["1236"] = {
				['id'] = 0x4D4,
				['offset'] = 76,
			},
		},
		["ENEMY_GARIBS"] = {
			["1237"] = {
				['id'] = 0x4D5,
				['offset'] = 77,
				['object_id'] = 0x4D8,
			},
			["1238"] = {
				['id'] = 0x4D6,
				['offset'] = 78,
				['object_id'] = 0x4D9,
			},
			["1239"] = {
				['id'] = 0x4D7,
				['offset'] = 79,
				['object_id'] = 0x4DA,
			},
		},
		["ENEMIES"] = {
			["1240"] = {
				['id'] = 0x4D8,
				['offset'] = 0,
			},
			["1241"] = {
				['id'] = 0x4D9,
				['offset'] = 1,
			},
			["1242"] = {
				['id'] = 0x4DA,
				['offset'] = 2,
			},
			["1243"] = {
				['id'] = 0x4DB,
				['offset'] = 3,
			},
		},
		["LIFE"] = {
			["1244"] = {
				['id'] = 0x4DC,
				['offset'] = 0,
			},
			["1245"] = {
				['id'] = 0x4DD,
				['offset'] = 1,
			},
			["1246"] = {
				['id'] = 0x4DE,
				['offset'] = 2,
			},
		},
		["CHECKPOINT"] = {
			["1247"] = {
				['id'] = 0x4DF,
				['offset'] = 0,
			},
			["1248"] = {
				['id'] = 0x4E0,
				['offset'] = 1,
			},
			["1249"] = {
				['id'] = 0x4E1,
				['offset'] = 2,
			},
			["1250"] = {
				['id'] = 0x4E2,
				['offset'] = 3,
			},
		},
		["SWITCH"] = {
			["1251"] = {
				['id'] = 0x4E3,
				['offset'] = 0,
			},
			["1252"] = {
				['id'] = 0x4E4,
				['offset'] = 1,
			},
			["1253"] = {
				['id'] = 0x4E5,
				['offset'] = 2,
			},
			["1254"] = {
				['id'] = 0x4E6,
				['offset'] = 3,
			},
			["1255"] = {
				['id'] = 0x4E7,
				['offset'] = 4,
			},
			["1256"] = {
				['id'] = 0x4E8,
				['offset'] = 5,
			},
			["1257"] = {
				['id'] = 0x4E9,
				['offset'] = 6,
			},
			["1258"] = {
				['id'] = 0x4EA,
				['offset'] = 7,
			},
			["1259"] = {
				['id'] = 0x4EB,
				['offset'] = 8,
			},
		},
		["POTIONS"] = {
			["1261"] = {
				['id'] = 0x4ED,
				['offset'] = 0,
			},
			["1262"] = {
				['id'] = 0x4EE,
				['offset'] = 1,
			},
			["1263"] = {
				['id'] = 0x4EF,
				['offset'] = 2,
			},
		},
	},
	["AP_PREHISTORIC_BOSS"] = {
		["GOAL"] = "1264",
	},
	["AP_PREHISTORIC_BONUS"] = {
		["GOAL"] = "1329",
		["GARIBS"] = {
			["1265"] = {
				['id'] = 0x4F1,
				['offset'] = 0,
			},
			["1266"] = {
				['id'] = 0x4F2,
				['offset'] = 1,
			},
			["1267"] = {
				['id'] = 0x4F3,
				['offset'] = 2,
			},
			["1268"] = {
				['id'] = 0x4F4,
				['offset'] = 3,
			},
			["1269"] = {
				['id'] = 0x4F5,
				['offset'] = 4,
			},
			["1270"] = {
				['id'] = 0x4F6,
				['offset'] = 5,
			},
			["1271"] = {
				['id'] = 0x4F7,
				['offset'] = 6,
			},
			["1272"] = {
				['id'] = 0x4F8,
				['offset'] = 7,
			},
			["1273"] = {
				['id'] = 0x4F9,
				['offset'] = 8,
			},
			["1274"] = {
				['id'] = 0x4FA,
				['offset'] = 9,
			},
			["1275"] = {
				['id'] = 0x4FB,
				['offset'] = 10,
			},
			["1276"] = {
				['id'] = 0x4FC,
				['offset'] = 11,
			},
			["1277"] = {
				['id'] = 0x4FD,
				['offset'] = 12,
			},
			["1278"] = {
				['id'] = 0x4FE,
				['offset'] = 13,
			},
			["1279"] = {
				['id'] = 0x4FF,
				['offset'] = 14,
			},
			["1280"] = {
				['id'] = 0x500,
				['offset'] = 15,
			},
			["1281"] = {
				['id'] = 0x501,
				['offset'] = 16,
			},
			["1282"] = {
				['id'] = 0x502,
				['offset'] = 17,
			},
			["1283"] = {
				['id'] = 0x503,
				['offset'] = 18,
			},
			["1284"] = {
				['id'] = 0x504,
				['offset'] = 19,
			},
			["1285"] = {
				['id'] = 0x505,
				['offset'] = 20,
			},
			["1286"] = {
				['id'] = 0x506,
				['offset'] = 21,
			},
			["1287"] = {
				['id'] = 0x507,
				['offset'] = 22,
			},
			["1288"] = {
				['id'] = 0x508,
				['offset'] = 23,
			},
			["1289"] = {
				['id'] = 0x509,
				['offset'] = 24,
			},
			["1290"] = {
				['id'] = 0x50A,
				['offset'] = 25,
			},
			["1291"] = {
				['id'] = 0x50B,
				['offset'] = 26,
			},
			["1292"] = {
				['id'] = 0x50C,
				['offset'] = 27,
			},
			["1293"] = {
				['id'] = 0x50D,
				['offset'] = 28,
			},
			["1294"] = {
				['id'] = 0x50E,
				['offset'] = 29,
			},
			["1295"] = {
				['id'] = 0x50F,
				['offset'] = 30,
			},
			["1296"] = {
				['id'] = 0x510,
				['offset'] = 31,
			},
			["1297"] = {
				['id'] = 0x511,
				['offset'] = 32,
			},
			["1298"] = {
				['id'] = 0x512,
				['offset'] = 33,
			},
			["1299"] = {
				['id'] = 0x513,
				['offset'] = 34,
			},
			["1300"] = {
				['id'] = 0x514,
				['offset'] = 35,
			},
			["1301"] = {
				['id'] = 0x515,
				['offset'] = 36,
			},
			["1302"] = {
				['id'] = 0x516,
				['offset'] = 37,
			},
			["1303"] = {
				['id'] = 0x517,
				['offset'] = 38,
			},
			["1304"] = {
				['id'] = 0x518,
				['offset'] = 39,
			},
			["1305"] = {
				['id'] = 0x519,
				['offset'] = 40,
			},
			["1306"] = {
				['id'] = 0x51A,
				['offset'] = 41,
			},
			["1307"] = {
				['id'] = 0x51B,
				['offset'] = 42,
			},
			["1308"] = {
				['id'] = 0x51C,
				['offset'] = 43,
			},
			["1309"] = {
				['id'] = 0x51D,
				['offset'] = 44,
			},
			["1310"] = {
				['id'] = 0x51E,
				['offset'] = 45,
			},
			["1311"] = {
				['id'] = 0x51F,
				['offset'] = 46,
			},
			["1312"] = {
				['id'] = 0x520,
				['offset'] = 47,
			},
			["1313"] = {
				['id'] = 0x521,
				['offset'] = 48,
			},
			["1314"] = {
				['id'] = 0x522,
				['offset'] = 49,
			},
			["1315"] = {
				['id'] = 0x523,
				['offset'] = 50,
			},
			["1316"] = {
				['id'] = 0x524,
				['offset'] = 51,
			},
			["1317"] = {
				['id'] = 0x525,
				['offset'] = 52,
			},
			["1318"] = {
				['id'] = 0x526,
				['offset'] = 53,
			},
			["1319"] = {
				['id'] = 0x527,
				['offset'] = 54,
			},
			["1320"] = {
				['id'] = 0x528,
				['offset'] = 55,
			},
			["1321"] = {
				['id'] = 0x529,
				['offset'] = 56,
			},
			["1322"] = {
				['id'] = 0x52A,
				['offset'] = 57,
			},
			["1323"] = {
				['id'] = 0x52B,
				['offset'] = 58,
			},
			["1324"] = {
				['id'] = 0x52C,
				['offset'] = 59,
			},
		},
		["LIFE"] = {
			["1325"] = {
				['id'] = 0x52D,
				['offset'] = 0,
			},
			["1326"] = {
				['id'] = 0x52E,
				['offset'] = 1,
			},
			["1327"] = {
				['id'] = 0x52F,
				['offset'] = 2,
			},
			["1328"] = {
				['id'] = 0x530,
				['offset'] = 3,
			},
		},
	},
	["AP_FORTRESS_L1"] = {
		["GOAL"] = "1407",
		["GARIBS"] = {
			["1331"] = {
				['id'] = 0x533,
				['offset'] = 0,
			},
			["1332"] = {
				['id'] = 0x534,
				['offset'] = 1,
			},
			["1333"] = {
				['id'] = 0x535,
				['offset'] = 2,
			},
			["1334"] = {
				['id'] = 0x536,
				['offset'] = 3,
			},
			["1335"] = {
				['id'] = 0x537,
				['offset'] = 4,
			},
			["1336"] = {
				['id'] = 0x538,
				['offset'] = 5,
			},
			["1337"] = {
				['id'] = 0x539,
				['offset'] = 6,
			},
			["1338"] = {
				['id'] = 0x53A,
				['offset'] = 7,
			},
			["1339"] = {
				['id'] = 0x53B,
				['offset'] = 8,
			},
			["1340"] = {
				['id'] = 0x53C,
				['offset'] = 9,
			},
			["1341"] = {
				['id'] = 0x53D,
				['offset'] = 10,
			},
			["1342"] = {
				['id'] = 0x53E,
				['offset'] = 11,
			},
			["1343"] = {
				['id'] = 0x53F,
				['offset'] = 12,
			},
			["1344"] = {
				['id'] = 0x540,
				['offset'] = 13,
			},
			["1345"] = {
				['id'] = 0x541,
				['offset'] = 14,
			},
			["1346"] = {
				['id'] = 0x542,
				['offset'] = 15,
			},
			["1347"] = {
				['id'] = 0x543,
				['offset'] = 16,
			},
			["1348"] = {
				['id'] = 0x544,
				['offset'] = 17,
			},
			["1349"] = {
				['id'] = 0x545,
				['offset'] = 18,
			},
			["1350"] = {
				['id'] = 0x546,
				['offset'] = 19,
			},
			["1351"] = {
				['id'] = 0x547,
				['offset'] = 20,
			},
			["1352"] = {
				['id'] = 0x548,
				['offset'] = 21,
			},
			["1353"] = {
				['id'] = 0x549,
				['offset'] = 22,
			},
			["1354"] = {
				['id'] = 0x54A,
				['offset'] = 23,
			},
			["1355"] = {
				['id'] = 0x54B,
				['offset'] = 24,
			},
			["1356"] = {
				['id'] = 0x54C,
				['offset'] = 25,
			},
			["1357"] = {
				['id'] = 0x54D,
				['offset'] = 26,
			},
			["1358"] = {
				['id'] = 0x54E,
				['offset'] = 27,
			},
			["1359"] = {
				['id'] = 0x54F,
				['offset'] = 28,
			},
			["1360"] = {
				['id'] = 0x550,
				['offset'] = 29,
			},
			["1361"] = {
				['id'] = 0x551,
				['offset'] = 30,
			},
			["1362"] = {
				['id'] = 0x552,
				['offset'] = 31,
			},
			["1363"] = {
				['id'] = 0x553,
				['offset'] = 32,
			},
			["1364"] = {
				['id'] = 0x554,
				['offset'] = 33,
			},
			["1365"] = {
				['id'] = 0x555,
				['offset'] = 34,
			},
			["1366"] = {
				['id'] = 0x556,
				['offset'] = 35,
			},
			["1367"] = {
				['id'] = 0x557,
				['offset'] = 36,
			},
			["1368"] = {
				['id'] = 0x558,
				['offset'] = 37,
			},
			["1369"] = {
				['id'] = 0x559,
				['offset'] = 38,
			},
			["1370"] = {
				['id'] = 0x55A,
				['offset'] = 39,
			},
			["1371"] = {
				['id'] = 0x55B,
				['offset'] = 40,
			},
			["1372"] = {
				['id'] = 0x55C,
				['offset'] = 41,
			},
			["1373"] = {
				['id'] = 0x55D,
				['offset'] = 42,
			},
			["1374"] = {
				['id'] = 0x55E,
				['offset'] = 43,
			},
			["1375"] = {
				['id'] = 0x55F,
				['offset'] = 44,
			},
			["1376"] = {
				['id'] = 0x560,
				['offset'] = 45,
			},
			["1377"] = {
				['id'] = 0x561,
				['offset'] = 46,
			},
			["1378"] = {
				['id'] = 0x562,
				['offset'] = 47,
			},
			["1379"] = {
				['id'] = 0x563,
				['offset'] = 48,
			},
			["1380"] = {
				['id'] = 0x564,
				['offset'] = 49,
			},
			["1381"] = {
				['id'] = 0x565,
				['offset'] = 50,
			},
			["1382"] = {
				['id'] = 0x566,
				['offset'] = 51,
			},
			["1383"] = {
				['id'] = 0x567,
				['offset'] = 52,
			},
			["1384"] = {
				['id'] = 0x568,
				['offset'] = 53,
			},
			["1385"] = {
				['id'] = 0x569,
				['offset'] = 54,
			},
			["1386"] = {
				['id'] = 0x56A,
				['offset'] = 55,
			},
			["1387"] = {
				['id'] = 0x56B,
				['offset'] = 56,
			},
			["1388"] = {
				['id'] = 0x56C,
				['offset'] = 57,
			},
			["1389"] = {
				['id'] = 0x56D,
				['offset'] = 58,
			},
		},
		["ENEMY_GARIBS"] = {
			["1390"] = {
				['id'] = 0x56E,
				['offset'] = 59,
				['object_id'] = 0x573,
			},
		},
		["ENEMIES"] = {
			["1391"] = {
				['id'] = 0x56F,
				['offset'] = 0,
			},
			["1392"] = {
				['id'] = 0x570,
				['offset'] = 1,
			},
			["1393"] = {
				['id'] = 0x571,
				['offset'] = 2,
			},
			["1394"] = {
				['id'] = 0x572,
				['offset'] = 3,
			},
			["1395"] = {
				['id'] = 0x573,
				['offset'] = 4,
			},
		},
		["LIFE"] = {
			["1396"] = {
				['id'] = 0x574,
				['offset'] = 0,
			},
			["1397"] = {
				['id'] = 0x575,
				['offset'] = 1,
			},
			["1398"] = {
				['id'] = 0x576,
				['offset'] = 2,
			},
			["1399"] = {
				['id'] = 0x577,
				['offset'] = 3,
			},
		},
		["CHECKPOINT"] = {
			["1400"] = {
				['id'] = 0x578,
				['offset'] = 0,
			},
			["1401"] = {
				['id'] = 0x579,
				['offset'] = 1,
			},
			["1402"] = {
				['id'] = 0x57A,
				['offset'] = 2,
			},
		},
		["SWITCH"] = {
			["1403"] = {
				['id'] = 0x57B,
				['offset'] = 0,
			},
			["1404"] = {
				['id'] = 0x57C,
				['offset'] = 1,
			},
			["1405"] = {
				['id'] = 0x57D,
				['offset'] = 2,
			},
			["1406"] = {
				['id'] = 0x57E,
				['offset'] = 3,
			},
		},
		["POTIONS"] = {
			["1408"] = {
				['id'] = 0x580,
				['offset'] = 0,
			},
			["1409"] = {
				['id'] = 0x581,
				['offset'] = 1,
			},
			["1410"] = {
				['id'] = 0x582,
				['offset'] = 2,
			},
			["1411"] = {
				['id'] = 0x583,
				['offset'] = 3,
			},
			["1412"] = {
				['id'] = 0x584,
				['offset'] = 4,
			},
			["1413"] = {
				['id'] = 0x585,
				['offset'] = 5,
			},
		},
	},
	["AP_FORTRESS_L2"] = {
		["GOAL"] = "1488",
		["GARIBS"] = {
			["1415"] = {
				['id'] = 0x587,
				['offset'] = 0,
			},
			["1416"] = {
				['id'] = 0x588,
				['offset'] = 1,
			},
			["1417"] = {
				['id'] = 0x589,
				['offset'] = 2,
			},
			["1418"] = {
				['id'] = 0x58A,
				['offset'] = 3,
			},
			["1419"] = {
				['id'] = 0x58B,
				['offset'] = 4,
			},
			["1420"] = {
				['id'] = 0x58C,
				['offset'] = 5,
			},
			["1421"] = {
				['id'] = 0x58D,
				['offset'] = 6,
			},
			["1422"] = {
				['id'] = 0x58E,
				['offset'] = 7,
			},
			["1423"] = {
				['id'] = 0x58F,
				['offset'] = 8,
			},
			["1424"] = {
				['id'] = 0x590,
				['offset'] = 9,
			},
			["1425"] = {
				['id'] = 0x591,
				['offset'] = 10,
			},
			["1426"] = {
				['id'] = 0x592,
				['offset'] = 11,
			},
			["1427"] = {
				['id'] = 0x593,
				['offset'] = 12,
			},
			["1428"] = {
				['id'] = 0x594,
				['offset'] = 13,
			},
			["1429"] = {
				['id'] = 0x595,
				['offset'] = 14,
			},
			["1430"] = {
				['id'] = 0x596,
				['offset'] = 15,
			},
			["1431"] = {
				['id'] = 0x597,
				['offset'] = 16,
			},
			["1432"] = {
				['id'] = 0x598,
				['offset'] = 17,
			},
			["1433"] = {
				['id'] = 0x599,
				['offset'] = 18,
			},
			["1434"] = {
				['id'] = 0x59A,
				['offset'] = 19,
			},
			["1435"] = {
				['id'] = 0x59B,
				['offset'] = 20,
			},
			["1436"] = {
				['id'] = 0x59C,
				['offset'] = 21,
			},
			["1437"] = {
				['id'] = 0x59D,
				['offset'] = 22,
			},
			["1438"] = {
				['id'] = 0x59E,
				['offset'] = 23,
			},
			["1439"] = {
				['id'] = 0x59F,
				['offset'] = 24,
			},
			["1440"] = {
				['id'] = 0x5A0,
				['offset'] = 25,
			},
			["1441"] = {
				['id'] = 0x5A1,
				['offset'] = 26,
			},
			["1442"] = {
				['id'] = 0x5A2,
				['offset'] = 27,
			},
			["1443"] = {
				['id'] = 0x5A3,
				['offset'] = 28,
			},
			["1444"] = {
				['id'] = 0x5A4,
				['offset'] = 29,
			},
			["1445"] = {
				['id'] = 0x5A5,
				['offset'] = 30,
			},
			["1446"] = {
				['id'] = 0x5A6,
				['offset'] = 31,
			},
			["1447"] = {
				['id'] = 0x5A7,
				['offset'] = 32,
			},
			["1448"] = {
				['id'] = 0x5A8,
				['offset'] = 33,
			},
			["1449"] = {
				['id'] = 0x5A9,
				['offset'] = 34,
			},
			["1450"] = {
				['id'] = 0x5AA,
				['offset'] = 35,
			},
			["1451"] = {
				['id'] = 0x5AB,
				['offset'] = 36,
			},
			["1452"] = {
				['id'] = 0x5AC,
				['offset'] = 37,
			},
			["1453"] = {
				['id'] = 0x5AD,
				['offset'] = 38,
			},
			["1454"] = {
				['id'] = 0x5AE,
				['offset'] = 39,
			},
			["1455"] = {
				['id'] = 0x5AF,
				['offset'] = 40,
			},
			["1456"] = {
				['id'] = 0x5B0,
				['offset'] = 41,
			},
			["1457"] = {
				['id'] = 0x5B1,
				['offset'] = 42,
			},
			["1458"] = {
				['id'] = 0x5B2,
				['offset'] = 43,
			},
			["1459"] = {
				['id'] = 0x5B3,
				['offset'] = 44,
			},
			["1460"] = {
				['id'] = 0x5B4,
				['offset'] = 45,
			},
			["1461"] = {
				['id'] = 0x5B5,
				['offset'] = 46,
			},
			["1462"] = {
				['id'] = 0x5B6,
				['offset'] = 47,
			},
			["1463"] = {
				['id'] = 0x5B7,
				['offset'] = 48,
			},
			["1464"] = {
				['id'] = 0x5B8,
				['offset'] = 49,
			},
			["1465"] = {
				['id'] = 0x5B9,
				['offset'] = 50,
			},
			["1466"] = {
				['id'] = 0x5BA,
				['offset'] = 51,
			},
			["1467"] = {
				['id'] = 0x5BB,
				['offset'] = 52,
			},
			["1468"] = {
				['id'] = 0x5BC,
				['offset'] = 53,
			},
			["1469"] = {
				['id'] = 0x5BD,
				['offset'] = 54,
			},
			["1470"] = {
				['id'] = 0x5BE,
				['offset'] = 55,
			},
			["1471"] = {
				['id'] = 0x5BF,
				['offset'] = 56,
			},
			["1472"] = {
				['id'] = 0x5C0,
				['offset'] = 57,
			},
			["1473"] = {
				['id'] = 0x5C1,
				['offset'] = 58,
			},
		},
		["ENEMY_GARIBS"] = {
			["1474"] = {
				['id'] = 0x5C2,
				['offset'] = 59,
				['object_id'] = 0x5C4,
			},
		},
		["ENEMIES"] = {
			["1475"] = {
				['id'] = 0x5C3,
				['offset'] = 0,
			},
			["1476"] = {
				['id'] = 0x5C4,
				['offset'] = 1,
			},
		},
		["LIFE"] = {
			["1477"] = {
				['id'] = 0x5C5,
				['offset'] = 0,
			},
			["1478"] = {
				['id'] = 0x5C6,
				['offset'] = 1,
			},
			["1479"] = {
				['id'] = 0x5C7,
				['offset'] = 2,
			},
			["1480"] = {
				['id'] = 0x5C8,
				['offset'] = 3,
			},
			["1481"] = {
				['id'] = 0x5C9,
				['offset'] = 4,
			},
		},
		["TIP"] = {
			["1482"] = {
				['id'] = 0x5CA,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			["1483"] = {
				['id'] = 0x5CB,
				['offset'] = 0,
			},
			["1484"] = {
				['id'] = 0x5CC,
				['offset'] = 1,
			},
			["1485"] = {
				['id'] = 0x5CD,
				['offset'] = 2,
			},
		},
		["SWITCH"] = {
			["1486"] = {
				['id'] = 0x5CE,
				['offset'] = 0,
			},
			["1487"] = {
				['id'] = 0x5CF,
				['offset'] = 1,
			},
		},
	},
	["AP_FORTRESS_L3"] = {
		["GOAL"] = "1582",
		["GARIBS"] = {
			["1491"] = {
				['id'] = 0x5D3,
				['offset'] = 0,
			},
			["1492"] = {
				['id'] = 0x5D4,
				['offset'] = 1,
			},
			["1493"] = {
				['id'] = 0x5D5,
				['offset'] = 2,
			},
			["1494"] = {
				['id'] = 0x5D6,
				['offset'] = 3,
			},
			["1495"] = {
				['id'] = 0x5D7,
				['offset'] = 4,
			},
			["1496"] = {
				['id'] = 0x5D8,
				['offset'] = 5,
			},
			["1497"] = {
				['id'] = 0x5D9,
				['offset'] = 6,
			},
			["1498"] = {
				['id'] = 0x5DA,
				['offset'] = 7,
			},
			["1499"] = {
				['id'] = 0x5DB,
				['offset'] = 8,
			},
			["1500"] = {
				['id'] = 0x5DC,
				['offset'] = 9,
			},
			["1501"] = {
				['id'] = 0x5DD,
				['offset'] = 10,
			},
			["1502"] = {
				['id'] = 0x5DE,
				['offset'] = 11,
			},
			["1503"] = {
				['id'] = 0x5DF,
				['offset'] = 12,
			},
			["1504"] = {
				['id'] = 0x5E0,
				['offset'] = 13,
			},
			["1505"] = {
				['id'] = 0x5E1,
				['offset'] = 14,
			},
			["1506"] = {
				['id'] = 0x5E2,
				['offset'] = 15,
			},
			["1507"] = {
				['id'] = 0x5E3,
				['offset'] = 16,
			},
			["1508"] = {
				['id'] = 0x5E4,
				['offset'] = 17,
			},
			["1509"] = {
				['id'] = 0x5E5,
				['offset'] = 18,
			},
			["1510"] = {
				['id'] = 0x5E6,
				['offset'] = 19,
			},
			["1511"] = {
				['id'] = 0x5E7,
				['offset'] = 20,
			},
			["1512"] = {
				['id'] = 0x5E8,
				['offset'] = 21,
			},
			["1513"] = {
				['id'] = 0x5E9,
				['offset'] = 22,
			},
			["1514"] = {
				['id'] = 0x5EA,
				['offset'] = 23,
			},
			["1515"] = {
				['id'] = 0x5EB,
				['offset'] = 24,
			},
			["1516"] = {
				['id'] = 0x5EC,
				['offset'] = 25,
			},
			["1517"] = {
				['id'] = 0x5ED,
				['offset'] = 26,
			},
			["1518"] = {
				['id'] = 0x5EE,
				['offset'] = 27,
			},
			["1519"] = {
				['id'] = 0x5EF,
				['offset'] = 28,
			},
			["1520"] = {
				['id'] = 0x5F0,
				['offset'] = 29,
			},
			["1521"] = {
				['id'] = 0x5F1,
				['offset'] = 30,
			},
			["1522"] = {
				['id'] = 0x5F2,
				['offset'] = 31,
			},
			["1523"] = {
				['id'] = 0x5F3,
				['offset'] = 32,
			},
			["1524"] = {
				['id'] = 0x5F4,
				['offset'] = 33,
			},
			["1525"] = {
				['id'] = 0x5F5,
				['offset'] = 34,
			},
			["1526"] = {
				['id'] = 0x5F6,
				['offset'] = 35,
			},
			["1527"] = {
				['id'] = 0x5F7,
				['offset'] = 36,
			},
			["1528"] = {
				['id'] = 0x5F8,
				['offset'] = 37,
			},
			["1529"] = {
				['id'] = 0x5F9,
				['offset'] = 38,
			},
			["1530"] = {
				['id'] = 0x5FA,
				['offset'] = 39,
			},
			["1531"] = {
				['id'] = 0x5FB,
				['offset'] = 40,
			},
			["1532"] = {
				['id'] = 0x5FC,
				['offset'] = 41,
			},
			["1533"] = {
				['id'] = 0x5FD,
				['offset'] = 42,
			},
			["1534"] = {
				['id'] = 0x5FE,
				['offset'] = 43,
			},
			["1535"] = {
				['id'] = 0x5FF,
				['offset'] = 44,
			},
			["1536"] = {
				['id'] = 0x600,
				['offset'] = 45,
			},
			["1537"] = {
				['id'] = 0x601,
				['offset'] = 46,
			},
			["1538"] = {
				['id'] = 0x602,
				['offset'] = 47,
			},
			["1539"] = {
				['id'] = 0x603,
				['offset'] = 48,
			},
			["1540"] = {
				['id'] = 0x604,
				['offset'] = 49,
			},
			["1541"] = {
				['id'] = 0x605,
				['offset'] = 50,
			},
			["1542"] = {
				['id'] = 0x606,
				['offset'] = 51,
			},
			["1543"] = {
				['id'] = 0x607,
				['offset'] = 52,
			},
			["1544"] = {
				['id'] = 0x608,
				['offset'] = 53,
			},
			["1545"] = {
				['id'] = 0x609,
				['offset'] = 54,
			},
			["1546"] = {
				['id'] = 0x60A,
				['offset'] = 55,
			},
			["1547"] = {
				['id'] = 0x60B,
				['offset'] = 56,
			},
			["1548"] = {
				['id'] = 0x60C,
				['offset'] = 57,
			},
			["1549"] = {
				['id'] = 0x60D,
				['offset'] = 58,
			},
			["1550"] = {
				['id'] = 0x60E,
				['offset'] = 59,
			},
			["1551"] = {
				['id'] = 0x60F,
				['offset'] = 60,
			},
			["1552"] = {
				['id'] = 0x610,
				['offset'] = 61,
			},
			["1553"] = {
				['id'] = 0x611,
				['offset'] = 62,
			},
			["1554"] = {
				['id'] = 0x612,
				['offset'] = 63,
			},
			["1555"] = {
				['id'] = 0x613,
				['offset'] = 64,
			},
			["1556"] = {
				['id'] = 0x614,
				['offset'] = 65,
			},
			["1557"] = {
				['id'] = 0x615,
				['offset'] = 66,
			},
		},
		["ENEMY_GARIBS"] = {
			["1558"] = {
				['id'] = 0x616,
				['offset'] = 67,
				['object_id'] = 0x61A,
			},
			["1559"] = {
				['id'] = 0x617,
				['offset'] = 68,
				['object_id'] = 0x61E,
			},
			["1560"] = {
				['id'] = 0x618,
				['offset'] = 69,
				['object_id'] = 0x61F,
			},
		},
		["ENEMIES"] = {
			["1561"] = {
				['id'] = 0x619,
				['offset'] = 0,
			},
			["1562"] = {
				['id'] = 0x61A,
				['offset'] = 1,
			},
			["1563"] = {
				['id'] = 0x61B,
				['offset'] = 2,
			},
			["1564"] = {
				['id'] = 0x61C,
				['offset'] = 3,
			},
			["1565"] = {
				['id'] = 0x61D,
				['offset'] = 4,
			},
			["1566"] = {
				['id'] = 0x61E,
				['offset'] = 5,
			},
			["1567"] = {
				['id'] = 0x61F,
				['offset'] = 6,
			},
		},
		["LIFE"] = {
			["1568"] = {
				['id'] = 0x620,
				['offset'] = 0,
			},
			["1569"] = {
				['id'] = 0x621,
				['offset'] = 1,
			},
			["1570"] = {
				['id'] = 0x622,
				['offset'] = 2,
			},
			["1571"] = {
				['id'] = 0x623,
				['offset'] = 3,
			},
			["1572"] = {
				['id'] = 0x624,
				['offset'] = 4,
			},
			["1573"] = {
				['id'] = 0x625,
				['offset'] = 5,
			},
			["1574"] = {
				['id'] = 0x626,
				['offset'] = 6,
			},
		},
		["CHECKPOINT"] = {
			["1575"] = {
				['id'] = 0x627,
				['offset'] = 0,
			},
			["1576"] = {
				['id'] = 0x628,
				['offset'] = 1,
			},
			["1577"] = {
				['id'] = 0x629,
				['offset'] = 2,
			},
			["1578"] = {
				['id'] = 0x62A,
				['offset'] = 3,
			},
			["1579"] = {
				['id'] = 0x62B,
				['offset'] = 4,
			},
		},
		["SWITCH"] = {
			["1580"] = {
				['id'] = 0x62C,
				['offset'] = 0,
			},
			["1581"] = {
				['id'] = 0x62D,
				['offset'] = 1,
			},
		},
		["POTIONS"] = {
			["1583"] = {
				['id'] = 0x62F,
				['offset'] = 0,
			},
		},
	},
	["AP_FORTRESS_BOSS"] = {
		["GOAL"] = "1584",
	},
	["AP_FORTRESS_BONUS"] = {
		["GOAL"] = "1642",
		["GARIBS"] = {
			["1585"] = {
				['id'] = 0x631,
				['offset'] = 0,
			},
			["1586"] = {
				['id'] = 0x632,
				['offset'] = 1,
			},
			["1587"] = {
				['id'] = 0x633,
				['offset'] = 2,
			},
			["1588"] = {
				['id'] = 0x634,
				['offset'] = 3,
			},
			["1589"] = {
				['id'] = 0x635,
				['offset'] = 4,
			},
			["1590"] = {
				['id'] = 0x636,
				['offset'] = 5,
			},
			["1591"] = {
				['id'] = 0x637,
				['offset'] = 6,
			},
			["1592"] = {
				['id'] = 0x638,
				['offset'] = 7,
			},
			["1593"] = {
				['id'] = 0x639,
				['offset'] = 8,
			},
			["1594"] = {
				['id'] = 0x63A,
				['offset'] = 9,
			},
			["1595"] = {
				['id'] = 0x63B,
				['offset'] = 10,
			},
			["1596"] = {
				['id'] = 0x63C,
				['offset'] = 11,
			},
			["1597"] = {
				['id'] = 0x63D,
				['offset'] = 12,
			},
			["1598"] = {
				['id'] = 0x63E,
				['offset'] = 13,
			},
			["1599"] = {
				['id'] = 0x63F,
				['offset'] = 14,
			},
			["1600"] = {
				['id'] = 0x640,
				['offset'] = 15,
			},
			["1601"] = {
				['id'] = 0x641,
				['offset'] = 16,
			},
			["1602"] = {
				['id'] = 0x642,
				['offset'] = 17,
			},
			["1603"] = {
				['id'] = 0x643,
				['offset'] = 18,
			},
			["1604"] = {
				['id'] = 0x644,
				['offset'] = 19,
			},
			["1605"] = {
				['id'] = 0x645,
				['offset'] = 20,
			},
			["1606"] = {
				['id'] = 0x646,
				['offset'] = 21,
			},
			["1607"] = {
				['id'] = 0x647,
				['offset'] = 22,
			},
			["1608"] = {
				['id'] = 0x648,
				['offset'] = 23,
			},
			["1609"] = {
				['id'] = 0x649,
				['offset'] = 24,
			},
			["1610"] = {
				['id'] = 0x64A,
				['offset'] = 25,
			},
			["1611"] = {
				['id'] = 0x64B,
				['offset'] = 26,
			},
			["1612"] = {
				['id'] = 0x64C,
				['offset'] = 27,
			},
			["1613"] = {
				['id'] = 0x64D,
				['offset'] = 28,
			},
			["1614"] = {
				['id'] = 0x64E,
				['offset'] = 29,
			},
			["1615"] = {
				['id'] = 0x64F,
				['offset'] = 30,
			},
			["1616"] = {
				['id'] = 0x650,
				['offset'] = 31,
			},
			["1617"] = {
				['id'] = 0x651,
				['offset'] = 32,
			},
			["1618"] = {
				['id'] = 0x652,
				['offset'] = 33,
			},
			["1619"] = {
				['id'] = 0x653,
				['offset'] = 34,
			},
			["1620"] = {
				['id'] = 0x654,
				['offset'] = 35,
			},
			["1621"] = {
				['id'] = 0x655,
				['offset'] = 36,
			},
			["1622"] = {
				['id'] = 0x656,
				['offset'] = 37,
			},
			["1623"] = {
				['id'] = 0x657,
				['offset'] = 38,
			},
			["1624"] = {
				['id'] = 0x658,
				['offset'] = 39,
			},
			["1625"] = {
				['id'] = 0x659,
				['offset'] = 40,
			},
			["1626"] = {
				['id'] = 0x65A,
				['offset'] = 41,
			},
			["1627"] = {
				['id'] = 0x65B,
				['offset'] = 42,
			},
			["1628"] = {
				['id'] = 0x65C,
				['offset'] = 43,
			},
			["1629"] = {
				['id'] = 0x65D,
				['offset'] = 44,
			},
			["1630"] = {
				['id'] = 0x65E,
				['offset'] = 45,
			},
			["1631"] = {
				['id'] = 0x65F,
				['offset'] = 46,
			},
			["1632"] = {
				['id'] = 0x660,
				['offset'] = 47,
			},
			["1633"] = {
				['id'] = 0x661,
				['offset'] = 48,
			},
			["1634"] = {
				['id'] = 0x662,
				['offset'] = 49,
			},
			["1635"] = {
				['id'] = 0x663,
				['offset'] = 50,
			},
			["1636"] = {
				['id'] = 0x664,
				['offset'] = 51,
			},
			["1637"] = {
				['id'] = 0x665,
				['offset'] = 52,
			},
			["1638"] = {
				['id'] = 0x666,
				['offset'] = 53,
			},
			["1639"] = {
				['id'] = 0x667,
				['offset'] = 54,
			},
			["1640"] = {
				['id'] = 0x668,
				['offset'] = 55,
			},
		},
		["LIFE"] = {
			["1641"] = {
				['id'] = 0x669,
				['offset'] = 0,
			},
		},
	},
	["AP_SPACE_L1"] = {
		["GOAL"] = "1709",
		["GARIBS"] = {
			["1644"] = {
				['id'] = 0x66C,
				['offset'] = 0,
			},
			["1645"] = {
				['id'] = 0x66D,
				['offset'] = 1,
			},
			["1646"] = {
				['id'] = 0x66E,
				['offset'] = 2,
			},
			["1647"] = {
				['id'] = 0x66F,
				['offset'] = 3,
			},
			["1648"] = {
				['id'] = 0x670,
				['offset'] = 4,
			},
			["1649"] = {
				['id'] = 0x671,
				['offset'] = 5,
			},
			["1650"] = {
				['id'] = 0x672,
				['offset'] = 6,
			},
			["1651"] = {
				['id'] = 0x673,
				['offset'] = 7,
			},
			["1652"] = {
				['id'] = 0x674,
				['offset'] = 8,
			},
			["1653"] = {
				['id'] = 0x675,
				['offset'] = 9,
			},
			["1654"] = {
				['id'] = 0x676,
				['offset'] = 10,
			},
			["1655"] = {
				['id'] = 0x677,
				['offset'] = 11,
			},
			["1656"] = {
				['id'] = 0x678,
				['offset'] = 12,
			},
			["1657"] = {
				['id'] = 0x679,
				['offset'] = 13,
			},
			["1658"] = {
				['id'] = 0x67A,
				['offset'] = 14,
			},
			["1659"] = {
				['id'] = 0x67B,
				['offset'] = 15,
			},
			["1660"] = {
				['id'] = 0x67C,
				['offset'] = 16,
			},
			["1661"] = {
				['id'] = 0x67D,
				['offset'] = 17,
			},
			["1662"] = {
				['id'] = 0x67E,
				['offset'] = 18,
			},
			["1663"] = {
				['id'] = 0x67F,
				['offset'] = 19,
			},
			["1664"] = {
				['id'] = 0x680,
				['offset'] = 20,
			},
			["1665"] = {
				['id'] = 0x681,
				['offset'] = 21,
			},
			["1666"] = {
				['id'] = 0x682,
				['offset'] = 22,
			},
			["1667"] = {
				['id'] = 0x683,
				['offset'] = 23,
			},
			["1668"] = {
				['id'] = 0x684,
				['offset'] = 24,
			},
			["1669"] = {
				['id'] = 0x685,
				['offset'] = 25,
			},
			["1670"] = {
				['id'] = 0x686,
				['offset'] = 26,
			},
			["1671"] = {
				['id'] = 0x687,
				['offset'] = 27,
			},
			["1672"] = {
				['id'] = 0x688,
				['offset'] = 28,
			},
			["1673"] = {
				['id'] = 0x689,
				['offset'] = 29,
			},
			["1674"] = {
				['id'] = 0x68A,
				['offset'] = 30,
			},
			["1675"] = {
				['id'] = 0x68B,
				['offset'] = 31,
			},
			["1676"] = {
				['id'] = 0x68C,
				['offset'] = 32,
			},
			["1677"] = {
				['id'] = 0x68D,
				['offset'] = 33,
			},
			["1678"] = {
				['id'] = 0x68E,
				['offset'] = 34,
			},
			["1679"] = {
				['id'] = 0x68F,
				['offset'] = 35,
			},
			["1680"] = {
				['id'] = 0x690,
				['offset'] = 36,
			},
			["1681"] = {
				['id'] = 0x691,
				['offset'] = 37,
			},
			["1682"] = {
				['id'] = 0x692,
				['offset'] = 38,
			},
			["1683"] = {
				['id'] = 0x693,
				['offset'] = 39,
			},
			["1684"] = {
				['id'] = 0x694,
				['offset'] = 40,
			},
			["1685"] = {
				['id'] = 0x695,
				['offset'] = 41,
			},
			["1686"] = {
				['id'] = 0x696,
				['offset'] = 42,
			},
			["1687"] = {
				['id'] = 0x697,
				['offset'] = 43,
			},
			["1688"] = {
				['id'] = 0x698,
				['offset'] = 44,
			},
		},
		["ENEMY_GARIBS"] = {
			["1689"] = {
				['id'] = 0x699,
				['offset'] = 45,
				['object_id'] = 0x69E,
			},
			["1690"] = {
				['id'] = 0x69A,
				['offset'] = 46,
				['object_id'] = 0x69F,
			},
			["1691"] = {
				['id'] = 0x69B,
				['offset'] = 47,
				['object_id'] = 0x6A0,
			},
			["1692"] = {
				['id'] = 0x69C,
				['offset'] = 48,
				['object_id'] = 0x6A1,
			},
			["1693"] = {
				['id'] = 0x69D,
				['offset'] = 49,
				['object_id'] = 0x6A2,
			},
		},
		["ENEMIES"] = {
			["1694"] = {
				['id'] = 0x69E,
				['offset'] = 0,
			},
			["1695"] = {
				['id'] = 0x69F,
				['offset'] = 1,
			},
			["1696"] = {
				['id'] = 0x6A0,
				['offset'] = 2,
			},
			["1697"] = {
				['id'] = 0x6A1,
				['offset'] = 3,
			},
			["1698"] = {
				['id'] = 0x6A2,
				['offset'] = 4,
			},
			["1699"] = {
				['id'] = 0x6A3,
				['offset'] = 5,
			},
		},
		["LIFE"] = {
			["1700"] = {
				['id'] = 0x6A4,
				['offset'] = 0,
			},
			["1701"] = {
				['id'] = 0x6A5,
				['offset'] = 1,
			},
		},
		["CHECKPOINT"] = {
			["1702"] = {
				['id'] = 0x6A6,
				['offset'] = 0,
			},
			["1703"] = {
				['id'] = 0x6A7,
				['offset'] = 1,
			},
		},
		["SWITCH"] = {
			["1704"] = {
				['id'] = 0x6A8,
				['offset'] = 0,
			},
			["1705"] = {
				['id'] = 0x6A9,
				['offset'] = 1,
			},
			["1706"] = {
				['id'] = 0x6AA,
				['offset'] = 2,
			},
			["1707"] = {
				['id'] = 0x6AB,
				['offset'] = 3,
			},
			["1708"] = {
				['id'] = 0x6AC,
				['offset'] = 4,
			},
		},
	},
	["AP_SPACE_L2"] = {
		["GOAL"] = "1771",
		["GARIBS"] = {
			["1710"] = {
				['id'] = 0x6AE,
				['offset'] = 0,
			},
			["1711"] = {
				['id'] = 0x6AF,
				['offset'] = 1,
			},
			["1712"] = {
				['id'] = 0x6B0,
				['offset'] = 2,
			},
			["1713"] = {
				['id'] = 0x6B1,
				['offset'] = 3,
			},
			["1714"] = {
				['id'] = 0x6B2,
				['offset'] = 4,
			},
			["1715"] = {
				['id'] = 0x6B3,
				['offset'] = 5,
			},
			["1716"] = {
				['id'] = 0x6B4,
				['offset'] = 6,
			},
			["1717"] = {
				['id'] = 0x6B5,
				['offset'] = 7,
			},
			["1718"] = {
				['id'] = 0x6B6,
				['offset'] = 8,
			},
			["1719"] = {
				['id'] = 0x6B7,
				['offset'] = 9,
			},
			["1720"] = {
				['id'] = 0x6B8,
				['offset'] = 10,
			},
			["1721"] = {
				['id'] = 0x6B9,
				['offset'] = 11,
			},
			["1722"] = {
				['id'] = 0x6BA,
				['offset'] = 12,
			},
			["1723"] = {
				['id'] = 0x6BB,
				['offset'] = 13,
			},
			["1724"] = {
				['id'] = 0x6BC,
				['offset'] = 14,
			},
			["1725"] = {
				['id'] = 0x6BD,
				['offset'] = 15,
			},
			["1726"] = {
				['id'] = 0x6BE,
				['offset'] = 16,
			},
			["1727"] = {
				['id'] = 0x6BF,
				['offset'] = 17,
			},
			["1728"] = {
				['id'] = 0x6C0,
				['offset'] = 18,
			},
			["1729"] = {
				['id'] = 0x6C1,
				['offset'] = 19,
			},
			["1730"] = {
				['id'] = 0x6C2,
				['offset'] = 20,
			},
			["1731"] = {
				['id'] = 0x6C3,
				['offset'] = 21,
			},
			["1732"] = {
				['id'] = 0x6C4,
				['offset'] = 22,
			},
			["1733"] = {
				['id'] = 0x6C5,
				['offset'] = 23,
			},
			["1734"] = {
				['id'] = 0x6C6,
				['offset'] = 24,
			},
			["1735"] = {
				['id'] = 0x6C7,
				['offset'] = 25,
			},
			["1736"] = {
				['id'] = 0x6C8,
				['offset'] = 26,
			},
			["1737"] = {
				['id'] = 0x6C9,
				['offset'] = 27,
			},
			["1738"] = {
				['id'] = 0x6CA,
				['offset'] = 28,
			},
			["1739"] = {
				['id'] = 0x6CB,
				['offset'] = 29,
			},
			["1740"] = {
				['id'] = 0x6CC,
				['offset'] = 30,
			},
			["1741"] = {
				['id'] = 0x6CD,
				['offset'] = 31,
			},
			["1742"] = {
				['id'] = 0x6CE,
				['offset'] = 32,
			},
			["1743"] = {
				['id'] = 0x6CF,
				['offset'] = 33,
			},
			["1744"] = {
				['id'] = 0x6D0,
				['offset'] = 34,
			},
			["1745"] = {
				['id'] = 0x6D1,
				['offset'] = 35,
			},
			["1746"] = {
				['id'] = 0x6D2,
				['offset'] = 36,
			},
			["1747"] = {
				['id'] = 0x6D3,
				['offset'] = 37,
			},
			["1748"] = {
				['id'] = 0x6D4,
				['offset'] = 38,
			},
			["1749"] = {
				['id'] = 0x6D5,
				['offset'] = 39,
			},
			["1750"] = {
				['id'] = 0x6D6,
				['offset'] = 40,
			},
			["1751"] = {
				['id'] = 0x6D7,
				['offset'] = 41,
			},
			["1752"] = {
				['id'] = 0x6D8,
				['offset'] = 42,
			},
			["1753"] = {
				['id'] = 0x6D9,
				['offset'] = 43,
			},
		},
		["ENEMY_GARIBS"] = {
			["1754"] = {
				['id'] = 0x6DA,
				['offset'] = 44,
				['object_id'] = 0x6E0,
			},
			["1755"] = {
				['id'] = 0x6DB,
				['offset'] = 45,
				['object_id'] = 0x6E1,
			},
			["1756"] = {
				['id'] = 0x6DC,
				['offset'] = 46,
				['object_id'] = 0x6E2,
			},
			["1757"] = {
				['id'] = 0x6DD,
				['offset'] = 47,
				['object_id'] = 0x6E3,
			},
			["1758"] = {
				['id'] = 0x6DE,
				['offset'] = 48,
				['object_id'] = 0x6E4,
			},
			["1759"] = {
				['id'] = 0x6DF,
				['offset'] = 49,
				['object_id'] = 0x6E5,
			},
		},
		["ENEMIES"] = {
			["1760"] = {
				['id'] = 0x6E0,
				['offset'] = 0,
			},
			["1761"] = {
				['id'] = 0x6E1,
				['offset'] = 1,
			},
			["1762"] = {
				['id'] = 0x6E2,
				['offset'] = 2,
			},
			["1763"] = {
				['id'] = 0x6E3,
				['offset'] = 3,
			},
			["1764"] = {
				['id'] = 0x6E4,
				['offset'] = 4,
			},
			["1765"] = {
				['id'] = 0x6E5,
				['offset'] = 5,
			},
		},
		["LIFE"] = {
			["1766"] = {
				['id'] = 0x6E6,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			["1767"] = {
				['id'] = 0x6E7,
				['offset'] = 0,
			},
		},
		["SWITCH"] = {
			["1768"] = {
				['id'] = 0x6E8,
				['offset'] = 0,
			},
			["1769"] = {
				['id'] = 0x6E9,
				['offset'] = 1,
			},
			["1770"] = {
				['id'] = 0x6EA,
				['offset'] = 2,
			},
		},
		["POTIONS"] = {
			["1772"] = {
				['id'] = 0x6EC,
				['offset'] = 0,
			},
		},
	},
	["AP_SPACE_L3"] = {
		["GOAL"] = "1867",
		["GARIBS"] = {
			["1773"] = {
				['id'] = 0x6ED,
				['offset'] = 0,
			},
			["1774"] = {
				['id'] = 0x6EE,
				['offset'] = 1,
			},
			["1775"] = {
				['id'] = 0x6EF,
				['offset'] = 2,
			},
			["1776"] = {
				['id'] = 0x6F0,
				['offset'] = 3,
			},
			["1777"] = {
				['id'] = 0x6F1,
				['offset'] = 4,
			},
			["1778"] = {
				['id'] = 0x6F2,
				['offset'] = 5,
			},
			["1779"] = {
				['id'] = 0x6F3,
				['offset'] = 6,
			},
			["1780"] = {
				['id'] = 0x6F4,
				['offset'] = 7,
			},
			["1781"] = {
				['id'] = 0x6F5,
				['offset'] = 8,
			},
			["1782"] = {
				['id'] = 0x6F6,
				['offset'] = 9,
			},
			["1783"] = {
				['id'] = 0x6F7,
				['offset'] = 10,
			},
			["1784"] = {
				['id'] = 0x6F8,
				['offset'] = 11,
			},
			["1785"] = {
				['id'] = 0x6F9,
				['offset'] = 12,
			},
			["1786"] = {
				['id'] = 0x6FA,
				['offset'] = 13,
			},
			["1787"] = {
				['id'] = 0x6FB,
				['offset'] = 14,
			},
			["1788"] = {
				['id'] = 0x6FC,
				['offset'] = 15,
			},
			["1789"] = {
				['id'] = 0x6FD,
				['offset'] = 16,
			},
			["1790"] = {
				['id'] = 0x6FE,
				['offset'] = 17,
			},
			["1791"] = {
				['id'] = 0x6FF,
				['offset'] = 18,
			},
			["1792"] = {
				['id'] = 0x700,
				['offset'] = 19,
			},
			["1793"] = {
				['id'] = 0x701,
				['offset'] = 20,
			},
			["1794"] = {
				['id'] = 0x702,
				['offset'] = 21,
			},
			["1795"] = {
				['id'] = 0x703,
				['offset'] = 22,
			},
			["1796"] = {
				['id'] = 0x704,
				['offset'] = 23,
			},
			["1797"] = {
				['id'] = 0x705,
				['offset'] = 24,
			},
			["1798"] = {
				['id'] = 0x706,
				['offset'] = 25,
			},
			["1799"] = {
				['id'] = 0x707,
				['offset'] = 26,
			},
			["1800"] = {
				['id'] = 0x708,
				['offset'] = 27,
			},
			["1801"] = {
				['id'] = 0x709,
				['offset'] = 28,
			},
			["1802"] = {
				['id'] = 0x70A,
				['offset'] = 29,
			},
			["1803"] = {
				['id'] = 0x70B,
				['offset'] = 30,
			},
			["1804"] = {
				['id'] = 0x70C,
				['offset'] = 31,
			},
			["1805"] = {
				['id'] = 0x70D,
				['offset'] = 32,
			},
			["1806"] = {
				['id'] = 0x70E,
				['offset'] = 33,
			},
			["1807"] = {
				['id'] = 0x70F,
				['offset'] = 34,
			},
			["1808"] = {
				['id'] = 0x710,
				['offset'] = 35,
			},
			["1809"] = {
				['id'] = 0x711,
				['offset'] = 36,
			},
			["1810"] = {
				['id'] = 0x712,
				['offset'] = 37,
			},
			["1811"] = {
				['id'] = 0x713,
				['offset'] = 38,
			},
			["1812"] = {
				['id'] = 0x714,
				['offset'] = 39,
			},
			["1813"] = {
				['id'] = 0x715,
				['offset'] = 40,
			},
			["1814"] = {
				['id'] = 0x716,
				['offset'] = 41,
			},
			["1815"] = {
				['id'] = 0x717,
				['offset'] = 42,
			},
			["1816"] = {
				['id'] = 0x718,
				['offset'] = 43,
			},
			["1817"] = {
				['id'] = 0x719,
				['offset'] = 44,
			},
			["1818"] = {
				['id'] = 0x71A,
				['offset'] = 45,
			},
			["1819"] = {
				['id'] = 0x71B,
				['offset'] = 46,
			},
			["1820"] = {
				['id'] = 0x71C,
				['offset'] = 47,
			},
			["1821"] = {
				['id'] = 0x71D,
				['offset'] = 48,
			},
			["1822"] = {
				['id'] = 0x71E,
				['offset'] = 49,
			},
			["1823"] = {
				['id'] = 0x71F,
				['offset'] = 50,
			},
			["1824"] = {
				['id'] = 0x720,
				['offset'] = 51,
			},
			["1825"] = {
				['id'] = 0x721,
				['offset'] = 52,
			},
			["1826"] = {
				['id'] = 0x722,
				['offset'] = 53,
			},
			["1827"] = {
				['id'] = 0x723,
				['offset'] = 54,
			},
			["1828"] = {
				['id'] = 0x724,
				['offset'] = 55,
			},
			["1829"] = {
				['id'] = 0x725,
				['offset'] = 56,
			},
			["1830"] = {
				['id'] = 0x726,
				['offset'] = 57,
			},
			["1831"] = {
				['id'] = 0x727,
				['offset'] = 58,
			},
			["1832"] = {
				['id'] = 0x728,
				['offset'] = 59,
			},
			["1833"] = {
				['id'] = 0x729,
				['offset'] = 60,
			},
			["1834"] = {
				['id'] = 0x72A,
				['offset'] = 61,
			},
			["1835"] = {
				['id'] = 0x72B,
				['offset'] = 62,
			},
			["1836"] = {
				['id'] = 0x72C,
				['offset'] = 63,
			},
			["1837"] = {
				['id'] = 0x72D,
				['offset'] = 64,
			},
			["1838"] = {
				['id'] = 0x72E,
				['offset'] = 65,
			},
			["1839"] = {
				['id'] = 0x72F,
				['offset'] = 66,
			},
			["1840"] = {
				['id'] = 0x730,
				['offset'] = 67,
			},
			["1841"] = {
				['id'] = 0x731,
				['offset'] = 68,
			},
			["1842"] = {
				['id'] = 0x732,
				['offset'] = 69,
			},
			["1843"] = {
				['id'] = 0x733,
				['offset'] = 70,
			},
			["1844"] = {
				['id'] = 0x734,
				['offset'] = 71,
			},
			["1845"] = {
				['id'] = 0x735,
				['offset'] = 72,
			},
			["1846"] = {
				['id'] = 0x736,
				['offset'] = 73,
			},
			["1847"] = {
				['id'] = 0x737,
				['offset'] = 74,
			},
			["1848"] = {
				['id'] = 0x738,
				['offset'] = 75,
			},
			["1849"] = {
				['id'] = 0x739,
				['offset'] = 76,
			},
			["1850"] = {
				['id'] = 0x73A,
				['offset'] = 77,
			},
			["1851"] = {
				['id'] = 0x73B,
				['offset'] = 78,
			},
			["1852"] = {
				['id'] = 0x73C,
				['offset'] = 79,
			},
		},
		["ENEMIES"] = {
			["1853"] = {
				['id'] = 0x73D,
				['offset'] = 0,
			},
			["1854"] = {
				['id'] = 0x73E,
				['offset'] = 1,
			},
			["1855"] = {
				['id'] = 0x73F,
				['offset'] = 2,
			},
		},
		["LIFE"] = {
			["1856"] = {
				['id'] = 0x740,
				['offset'] = 0,
			},
		},
		["CHECKPOINT"] = {
			["1857"] = {
				['id'] = 0x741,
				['offset'] = 0,
			},
			["1858"] = {
				['id'] = 0x742,
				['offset'] = 1,
			},
			["1859"] = {
				['id'] = 0x743,
				['offset'] = 2,
			},
			["1860"] = {
				['id'] = 0x744,
				['offset'] = 3,
			},
		},
		["SWITCH"] = {
			["1861"] = {
				['id'] = 0x745,
				['offset'] = 0,
			},
			["1862"] = {
				['id'] = 0x746,
				['offset'] = 1,
			},
			["1863"] = {
				['id'] = 0x747,
				['offset'] = 2,
			},
			["1864"] = {
				['id'] = 0x748,
				['offset'] = 3,
			},
			["1865"] = {
				['id'] = 0x749,
				['offset'] = 4,
			},
			["1866"] = {
				['id'] = 0x74A,
				['offset'] = 5,
			},
		},
		["POTIONS"] = {
			["1868"] = {
				['id'] = 0x74C,
				['offset'] = 0,
			},
		},
	},
	["AP_SPACE_BOSS"] = {
		["GOAL"] = "1869",
	},
	["AP_SPACE_BONUS"] = {
		["GOAL"] = "1926",
		["GARIBS"] = {
			["1870"] = {
				['id'] = 0x74E,
				['offset'] = 0,
			},
			["1871"] = {
				['id'] = 0x74F,
				['offset'] = 1,
			},
			["1872"] = {
				['id'] = 0x750,
				['offset'] = 2,
			},
			["1873"] = {
				['id'] = 0x751,
				['offset'] = 3,
			},
			["1874"] = {
				['id'] = 0x752,
				['offset'] = 4,
			},
			["1875"] = {
				['id'] = 0x753,
				['offset'] = 5,
			},
			["1876"] = {
				['id'] = 0x754,
				['offset'] = 6,
			},
			["1877"] = {
				['id'] = 0x755,
				['offset'] = 7,
			},
			["1878"] = {
				['id'] = 0x756,
				['offset'] = 8,
			},
			["1879"] = {
				['id'] = 0x757,
				['offset'] = 9,
			},
			["1880"] = {
				['id'] = 0x758,
				['offset'] = 10,
			},
			["1881"] = {
				['id'] = 0x759,
				['offset'] = 11,
			},
			["1882"] = {
				['id'] = 0x75A,
				['offset'] = 12,
			},
			["1883"] = {
				['id'] = 0x75B,
				['offset'] = 13,
			},
			["1884"] = {
				['id'] = 0x75C,
				['offset'] = 14,
			},
			["1885"] = {
				['id'] = 0x75D,
				['offset'] = 15,
			},
			["1886"] = {
				['id'] = 0x75E,
				['offset'] = 16,
			},
			["1887"] = {
				['id'] = 0x75F,
				['offset'] = 17,
			},
			["1888"] = {
				['id'] = 0x760,
				['offset'] = 18,
			},
			["1889"] = {
				['id'] = 0x761,
				['offset'] = 19,
			},
			["1890"] = {
				['id'] = 0x762,
				['offset'] = 20,
			},
			["1891"] = {
				['id'] = 0x763,
				['offset'] = 21,
			},
			["1892"] = {
				['id'] = 0x764,
				['offset'] = 22,
			},
			["1893"] = {
				['id'] = 0x765,
				['offset'] = 23,
			},
			["1894"] = {
				['id'] = 0x766,
				['offset'] = 24,
			},
			["1895"] = {
				['id'] = 0x767,
				['offset'] = 25,
			},
			["1896"] = {
				['id'] = 0x768,
				['offset'] = 26,
			},
			["1897"] = {
				['id'] = 0x769,
				['offset'] = 27,
			},
			["1898"] = {
				['id'] = 0x76A,
				['offset'] = 28,
			},
			["1899"] = {
				['id'] = 0x76B,
				['offset'] = 29,
			},
			["1900"] = {
				['id'] = 0x76C,
				['offset'] = 30,
			},
			["1901"] = {
				['id'] = 0x76D,
				['offset'] = 31,
			},
			["1902"] = {
				['id'] = 0x76E,
				['offset'] = 32,
			},
			["1903"] = {
				['id'] = 0x76F,
				['offset'] = 33,
			},
			["1904"] = {
				['id'] = 0x770,
				['offset'] = 34,
			},
			["1905"] = {
				['id'] = 0x771,
				['offset'] = 35,
			},
			["1906"] = {
				['id'] = 0x772,
				['offset'] = 36,
			},
			["1907"] = {
				['id'] = 0x773,
				['offset'] = 37,
			},
			["1908"] = {
				['id'] = 0x774,
				['offset'] = 38,
			},
			["1909"] = {
				['id'] = 0x775,
				['offset'] = 39,
			},
			["1910"] = {
				['id'] = 0x776,
				['offset'] = 40,
			},
			["1911"] = {
				['id'] = 0x777,
				['offset'] = 41,
			},
			["1912"] = {
				['id'] = 0x778,
				['offset'] = 42,
			},
			["1913"] = {
				['id'] = 0x779,
				['offset'] = 43,
			},
			["1914"] = {
				['id'] = 0x77A,
				['offset'] = 44,
			},
			["1915"] = {
				['id'] = 0x77B,
				['offset'] = 45,
			},
			["1916"] = {
				['id'] = 0x77C,
				['offset'] = 46,
			},
			["1917"] = {
				['id'] = 0x77D,
				['offset'] = 47,
			},
			["1918"] = {
				['id'] = 0x77E,
				['offset'] = 48,
			},
			["1919"] = {
				['id'] = 0x77F,
				['offset'] = 49,
			},
		},
		["LIFE"] = {
			["1920"] = {
				['id'] = 0x780,
				['offset'] = 0,
			},
			["1921"] = {
				['id'] = 0x781,
				['offset'] = 1,
			},
			["1922"] = {
				['id'] = 0x782,
				['offset'] = 2,
			},
			["1923"] = {
				['id'] = 0x783,
				['offset'] = 3,
			},
			["1924"] = {
				['id'] = 0x784,
				['offset'] = 4,
			},
			["1925"] = {
				['id'] = 0x785,
				['offset'] = 5,
			},
		},
		["POTIONS"] = {
			["1927"] = {
				['id'] = 0x787,
				['offset'] = 0,
			},
			["1928"] = {
				['id'] = 0x788,
				['offset'] = 1,
			},
			["1929"] = {
				['id'] = 0x789,
				['offset'] = 2,
			},
			["1930"] = {
				['id'] = 0x78A,
				['offset'] = 3,
			},
			["1931"] = {
				['id'] = 0x78B,
				['offset'] = 4,
			},
			["1932"] = {
				['id'] = 0x78C,
				['offset'] = 5,
			},
			["1933"] = {
				['id'] = 0x78D,
				['offset'] = 6,
			},
			["1934"] = {
				['id'] = 0x78E,
				['offset'] = 7,
			},
			["1935"] = {
				['id'] = 0x78F,
				['offset'] = 8,
			},
		},
	},
	["AP_TRAINING_WORLD"] = {
		["GOAL"] = "1965",
		["TIP"] = {
			["1947"] = {
				['id'] = 0x79B,
				['offset'] = 0,
			},
			["1948"] = {
				['id'] = 0x79C,
				['offset'] = 1,
			},
			["1949"] = {
				['id'] = 0x79D,
				['offset'] = 2,
			},
			["1950"] = {
				['id'] = 0x79E,
				['offset'] = 3,
			},
			["1951"] = {
				['id'] = 0x79F,
				['offset'] = 4,
			},
			["1952"] = {
				['id'] = 0x7A0,
				['offset'] = 5,
			},
			["1953"] = {
				['id'] = 0x7A1,
				['offset'] = 6,
			},
			["1954"] = {
				['id'] = 0x7A2,
				['offset'] = 7,
			},
			["1955"] = {
				['id'] = 0x7A3,
				['offset'] = 8,
			},
			["1956"] = {
				['id'] = 0x7A4,
				['offset'] = 9,
			},
			["1957"] = {
				['id'] = 0x7A5,
				['offset'] = 10,
			},
			["1958"] = {
				['id'] = 0x7A6,
				['offset'] = 11,
			},
			["1959"] = {
				['id'] = 0x7A7,
				['offset'] = 12,
			},
			["1960"] = {
				['id'] = 0x7A8,
				['offset'] = 13,
			},
			["1961"] = {
				['id'] = 0x7A9,
				['offset'] = 14,
			},
		},
		["SWITCH"] = {
			["1962"] = {
				['id'] = 0x7AA,
				['offset'] = 0,
			},
			["1963"] = {
				['id'] = 0x7AB,
				['offset'] = 1,
			},
			["1964"] = {
				['id'] = 0x7AC,
				['offset'] = 2,
			},
		},
	}
}

local GARIB_GROUPS_MAP = {
	["AP_ATLANTIS_L1"] = {
		["Arch Garibs"] = {
			["id"] = "10001",
			["garibs"] = {
				"1",
				"2",
				"3",
				"4",
				"5",
				"6"
			}
		},
		["Block Garibs"] = {
			["id"] = "10007",
			["garibs"] = {
				"7",
				"8"
			}
		},
		["Checkers Garibs"] = {
			["id"] = "10009",
			["garibs"] = {
				"9",
				"10"
			}
		},
		["Pillar Garibs"] = {
			["id"] = "10011",
			["garibs"] = {
				"11",
				"12",
				"13"
			}
		},
		["Platform A Garibs"] = {
			["id"] = "10014",
			["garibs"] = {
				"14",
				"15",
				"16",
				"17"
			}
		},
		["Platform B Garibs"] = {
			["id"] = "10018",
			["garibs"] = {
				"18",
				"19",
				"20",
				"21"
			}
		},
		["Platform C Garibs"] = {
			["id"] = "10022",
			["garibs"] = {
				"22",
				"23",
				"24",
				"25"
			}
		},
		["Platform D Garibs"] = {
			["id"] = "10026",
			["garibs"] = {
				"26",
				"27",
				"28",
				"29"
			}
		},
		["Platform E Garibs"] = {
			["id"] = "10030",
			["garibs"] = {
				"30",
				"31",
				"32",
				"33"
			}
		},
		["Pool Edge Garibs"] = {
			["id"] = "10034",
			["garibs"] = {
				"34",
				"35",
				"36",
				"37",
				"38"
			}
		},
		["Shark Garibs"] = {
			["id"] = "10039",
			["garibs"] = {
				"39",
				"40",
				"41",
				"42",
				"43",
				"44",
				"45",
				"46",
				"47"
			}
		},
		["Waterspout Garibs"] = {
			["id"] = "10048",
			["garibs"] = {
				"48",
				"49"
			}
		},
		["Bull Garibs"] = {
			["id"] = "10050",
			["garibs"] = {
				"50"
			}
		},
	},
	["AP_ATLANTIS_L2"] = {
		["Arch Garibs"] = {
			["id"] = "10067",
			["garibs"] = {
				"67",
				"68",
				"69",
				"70",
				"71"
			}
		},
		["Bridge A Garibs"] = {
			["id"] = "10072",
			["garibs"] = {
				"72",
				"73",
				"74",
				"75",
				"76"
			}
		},
		["Bridge B Garibs"] = {
			["id"] = "10077",
			["garibs"] = {
				"77",
				"78",
				"79",
				"80",
				"81"
			}
		},
		["Clifftop Garibs"] = {
			["id"] = "10082",
			["garibs"] = {
				"82",
				"83",
				"84",
				"85",
				"86",
				"87",
				"88"
			}
		},
		["Mesa Garibs"] = {
			["id"] = "10089",
			["garibs"] = {
				"89",
				"90",
				"91"
			}
		},
		["Mesa Jar"] = {
			["id"] = "10092",
			["garibs"] = {
				"92"
			}
		},
		["Pool Edge Garibs"] = {
			["id"] = "10093",
			["garibs"] = {
				"93",
				"94",
				"95",
				"96"
			}
		},
		["Roof Garibs"] = {
			["id"] = "10097",
			["garibs"] = {
				"97",
				"98",
				"99",
				"100",
				"101"
			}
		},
		["Shark Jars"] = {
			["id"] = "10102",
			["garibs"] = {
				"102",
				"103"
			}
		},
		["Under Roof Garibs"] = {
			["id"] = "10104",
			["garibs"] = {
				"104",
				"105",
				"106",
				"107",
				"108"
			}
		},
		["Vault Garibs"] = {
			["id"] = "10109",
			["garibs"] = {
				"109",
				"110",
				"111",
				"112",
				"113",
				"114",
				"115",
				"116",
				"117",
				"118"
			}
		},
		["Waterfall Garibs"] = {
			["id"] = "10119",
			["garibs"] = {
				"119",
				"120"
			}
		},
		["Bull Garibs"] = {
			["id"] = "10121",
			["garibs"] = {
				"121",
				"122",
				"123"
			}
		},
		["Wind-Up Garibs"] = {
			["id"] = "10124",
			["garibs"] = {
				"124",
				"125",
				"126"
			}
		},
	},
	["AP_ATLANTIS_L3"] = {
		["Alcove Garibs"] = {
			["id"] = "10143",
			["garibs"] = {
				"143",
				"144",
				"145"
			}
		},
		["Balcony Garibs"] = {
			["id"] = "10146",
			["garibs"] = {
				"146",
				"147",
				"148",
				"149",
				"150",
				"151"
			}
		},
		["Cave Garibs"] = {
			["id"] = "10152",
			["garibs"] = {
				"152",
				"153",
				"154",
				"155",
				"156"
			}
		},
		["Ceiling Garibs"] = {
			["id"] = "10157",
			["garibs"] = {
				"157",
				"158",
				"159",
				"160",
				"161",
				"162",
				"163",
				"164"
			}
		},
		["Cliff Garibs"] = {
			["id"] = "10165",
			["garibs"] = {
				"165",
				"166",
				"167",
				"168",
				"169",
				"170",
				"171",
				"172"
			}
		},
		["Island Garibs"] = {
			["id"] = "10173",
			["garibs"] = {
				"173",
				"174",
				"175",
				"176",
				"177",
				"178",
				"179",
				"180"
			}
		},
		["Path Garibs"] = {
			["id"] = "10181",
			["garibs"] = {
				"181",
				"182",
				"183",
				"184"
			}
		},
		["Pool Garibs"] = {
			["id"] = "10185",
			["garibs"] = {
				"185",
				"186",
				"187",
				"188",
				"189",
				"190",
				"191",
				"192",
				"193"
			}
		},
		["Slide Cliff Garibs"] = {
			["id"] = "10194",
			["garibs"] = {
				"194",
				"195",
				"196",
				"197"
			}
		},
		["Stairs Garibs"] = {
			["id"] = "10198",
			["garibs"] = {
				"198",
				"199",
				"200",
				"201",
				"202"
			}
		},
		["Under Waterfall Garibs"] = {
			["id"] = "10203",
			["garibs"] = {
				"203",
				"204",
				"205",
				"206"
			}
		},
		["Waterfall Garibs"] = {
			["id"] = "10207",
			["garibs"] = {
				"207",
				"208",
				"209",
				"210",
				"211"
			}
		},
		["Cave Wind-Up Garibs"] = {
			["id"] = "10212",
			["garibs"] = {
				"212",
				"213"
			}
		},
		["Cliff Wind-Up Garibs"] = {
			["id"] = "10214",
			["garibs"] = {
				"214"
			}
		},
		["Path Wind-Up Garibs"] = {
			["id"] = "10215",
			["garibs"] = {
				"215"
			}
		},
		["Speed Wind-Up Garibs"] = {
			["id"] = "10216",
			["garibs"] = {
				"216",
				"217",
				"218",
				"219"
			}
		},
		["Waterfall Wind-Up Garibs"] = {
			["id"] = "10220",
			["garibs"] = {
				"220",
				"221",
				"222"
			}
		},
	},
	["AP_ATLANTIS_BONUS"] = {
		["Garibs A"] = {
			["id"] = "10252",
			["garibs"] = {
				"252",
				"253",
				"254",
				"255",
				"256"
			}
		},
		["Garibs B"] = {
			["id"] = "10257",
			["garibs"] = {
				"257",
				"258",
				"259",
				"260",
				"261"
			}
		},
		["Garibs C"] = {
			["id"] = "10262",
			["garibs"] = {
				"262",
				"263",
				"264",
				"265",
				"266"
			}
		},
		["Garibs D"] = {
			["id"] = "10267",
			["garibs"] = {
				"267",
				"268",
				"269",
				"270",
				"271"
			}
		},
		["Garibs E"] = {
			["id"] = "10272",
			["garibs"] = {
				"272",
				"273",
				"274",
				"275",
				"276"
			}
		},
	},
	["AP_CARNIVAL_L1"] = {
		["Chicken Garibs"] = {
			["id"] = "10283",
			["garibs"] = {
				"283",
				"284",
				"285",
				"286",
				"287",
				"288",
				"289",
				"290"
			}
		},
		["Dennis Garibs"] = {
			["id"] = "10291",
			["garibs"] = {
				"291",
				"292",
				"293",
				"294"
			}
		},
		["Plinko Garibs"] = {
			["id"] = "10295",
			["garibs"] = {
				"295",
				"296",
				"297",
				"298",
				"299",
				"300",
				"301",
				"302",
				"303",
				"304",
				"305"
			}
		},
		["Pregate Garibs"] = {
			["id"] = "10306",
			["garibs"] = {
				"306",
				"307",
				"308",
				"309"
			}
		},
		["Rocket Garibs"] = {
			["id"] = "10310",
			["garibs"] = {
				"310",
				"311",
				"312",
				"313",
				"314",
				"315",
				"316"
			}
		},
		["Slide Garibs"] = {
			["id"] = "10317",
			["garibs"] = {
				"317",
				"318",
				"319",
				"320",
				"321",
				"322",
				"323",
				"324"
			}
		},
		["Slots Garibs"] = {
			["id"] = "10325",
			["garibs"] = {
				"325",
				"326",
				"327",
				"328",
				"329",
				"330",
				"331",
				"332",
				"333",
				"334"
			}
		},
		["Strongman Garibs"] = {
			["id"] = "10335",
			["garibs"] = {
				"335",
				"336",
				"337",
				"338"
			}
		},
		["Spawn Wind-Up Garibs"] = {
			["id"] = "10339",
			["garibs"] = {
				"339"
			}
		},
		["Whack-A-Mole Wind-Up Garibs"] = {
			["id"] = "10340",
			["garibs"] = {
				"340",
				"341",
				"342",
				"343",
				"344",
				"345",
				"346",
				"347"
			}
		},
	},
	["AP_CARNIVAL_L2"] = {
		["After Coaster Garibs"] = {
			["id"] = "10385",
			["garibs"] = {
				"385",
				"386",
				"387",
				"388"
			}
		},
		["Before Coaster Garibs"] = {
			["id"] = "10389",
			["garibs"] = {
				"389",
				"390",
				"391",
				"392"
			}
		},
		["Big Top Garibs"] = {
			["id"] = "10393",
			["garibs"] = {
				"393",
				"394",
				"395",
				"396",
				"397",
				"398",
				"399",
				"400"
			}
		},
		["Checkered Tilt Garibs"] = {
			["id"] = "10401",
			["garibs"] = {
				"401",
				"402",
				"403",
				"404",
				"405",
				"406"
			}
		},
		["Chicken Garibs"] = {
			["id"] = "10407",
			["garibs"] = {
				"407",
				"408",
				"409",
				"410",
				"411",
				"412",
				"413",
				"414",
				"415",
				"416",
				"417",
				"418"
			}
		},
		["Clown Teeth Garibs"] = {
			["id"] = "10419",
			["garibs"] = {
				"419",
				"420",
				"421",
				"422"
			}
		},
		["Fan Garibs"] = {
			["id"] = "10423",
			["garibs"] = {
				"423",
				"424",
				"425",
				"426"
			}
		},
		["Flying Garibs"] = {
			["id"] = "10427",
			["garibs"] = {
				"427",
				"428",
				"429"
			}
		},
		["Red Tilt Garibs"] = {
			["id"] = "10430",
			["garibs"] = {
				"430",
				"431",
				"432",
				"433",
				"434",
				"435"
			}
		},
		["Teacups Garibs"] = {
			["id"] = "10436",
			["garibs"] = {
				"436",
				"437",
				"438",
				"439",
				"440",
				"441"
			}
		},
		["Tent Garib"] = {
			["id"] = "10442",
			["garibs"] = {
				"442"
			}
		},
		["Tent Tilt Garibs"] = {
			["id"] = "10443",
			["garibs"] = {
				"443",
				"444",
				"445",
				"446",
				"447",
				"448",
				"449",
				"450",
				"451",
				"452"
			}
		},
		["Underwater Garibs"] = {
			["id"] = "10453",
			["garibs"] = {
				"453",
				"454",
				"455",
				"456",
				"457",
				"458",
				"459",
				"460"
			}
		},
		["After Coaster Wind-Up Garibs"] = {
			["id"] = "10461",
			["garibs"] = {
				"461"
			}
		},
		["Before Coaster Wind-Up Garibs"] = {
			["id"] = "10462",
			["garibs"] = {
				"462"
			}
		},
		["Conveyor Wind-Up Garibs"] = {
			["id"] = "10463",
			["garibs"] = {
				"463",
				"464"
			}
		},
	},
	["AP_CARNIVAL_L3"] = {
		["Bee Garibs"] = {
			["id"] = "10488",
			["garibs"] = {
				"488",
				"489",
				"490",
				"491"
			}
		},
		["Cutout Garibs"] = {
			["id"] = "10492",
			["garibs"] = {
				"492",
				"493",
				"494",
				"495",
				"496",
				"497"
			}
		},
		["Dennis Platform Garibs"] = {
			["id"] = "10498",
			["garibs"] = {
				"498",
				"499",
				"500",
				"501"
			}
		},
		["Funnel Garibs"] = {
			["id"] = "10502",
			["garibs"] = {
				"502",
				"503",
				"504",
				"505",
				"506",
				"507",
				"508",
				"509",
				"510"
			}
		},
		["Left Pool Garibs"] = {
			["id"] = "10511",
			["garibs"] = {
				"511",
				"512",
				"513",
				"514"
			}
		},
		["Lower Spintop Garibs"] = {
			["id"] = "10515",
			["garibs"] = {
				"515",
				"516",
				"517",
				"518",
				"519",
				"520",
				"521",
				"522"
			}
		},
		["Portal Garibs"] = {
			["id"] = "10523",
			["garibs"] = {
				"523",
				"524",
				"525",
				"526"
			}
		},
		["Right Pool Garibs"] = {
			["id"] = "10527",
			["garibs"] = {
				"527",
				"528",
				"529",
				"530"
			}
		},
		["Ships Garibs"] = {
			["id"] = "10531",
			["garibs"] = {
				"531",
				"532",
				"533"
			}
		},
		["Slide A Garibs"] = {
			["id"] = "10534",
			["garibs"] = {
				"534",
				"535",
				"536"
			}
		},
		["Slide B Garibs"] = {
			["id"] = "10537",
			["garibs"] = {
				"537",
				"538",
				"539"
			}
		},
		["Slide C Garibs"] = {
			["id"] = "10540",
			["garibs"] = {
				"540",
				"541",
				"542"
			}
		},
		["Slide D Garibs"] = {
			["id"] = "10543",
			["garibs"] = {
				"543",
				"544",
				"545",
				"546"
			}
		},
		["Tent Garibs"] = {
			["id"] = "10547",
			["garibs"] = {
				"547",
				"548",
				"549"
			}
		},
		["Upper Spintop Garibs"] = {
			["id"] = "10550",
			["garibs"] = {
				"550",
				"551",
				"552",
				"553",
				"554",
				"555",
				"556",
				"557",
				"558",
				"559",
				"560",
				"561"
			}
		},
		["Fenced Wind-Up Garibs"] = {
			["id"] = "10562",
			["garibs"] = {
				"562",
				"563"
			}
		},
		["Hands Wind-Up Garibs"] = {
			["id"] = "10564",
			["garibs"] = {
				"564"
			}
		},
		["Spinning Wind-Up Garibs"] = {
			["id"] = "10565",
			["garibs"] = {
				"565",
				"566",
				"567"
			}
		},
	},
	["AP_CARNIVAL_BONUS"] = {
		["Inner Garibs"] = {
			["id"] = "10602",
			["garibs"] = {
				"602",
				"603",
				"604",
				"605",
				"606",
				"607",
				"608",
				"609",
				"610",
				"611",
				"612",
				"613"
			}
		},
		["Outer Garibs"] = {
			["id"] = "10614",
			["garibs"] = {
				"614",
				"615",
				"616",
				"617",
				"618",
				"619",
				"620",
				"621"
			}
		},
	},
	["AP_PIRATES_L1"] = {
		["Beach Garibs"] = {
			["id"] = "10626",
			["garibs"] = {
				"626",
				"627",
				"628",
				"629",
				"630",
				"631",
				"632",
				"633"
			}
		},
		["Box Garibs"] = {
			["id"] = "10634",
			["garibs"] = {
				"634",
				"635",
				"636",
				"637",
				"638",
				"639",
				"640"
			}
		},
		["Bridge Garibs"] = {
			["id"] = "10641",
			["garibs"] = {
				"641",
				"642",
				"643",
				"644"
			}
		},
		["Cannon House Garibs"] = {
			["id"] = "10645",
			["garibs"] = {
				"645",
				"646",
				"647",
				"648"
			}
		},
		["Flying Ship A Garibs"] = {
			["id"] = "10649",
			["garibs"] = {
				"649",
				"650",
				"651",
				"652",
				"653"
			}
		},
		["Flying Ship B Garibs"] = {
			["id"] = "10654",
			["garibs"] = {
				"654",
				"655",
				"656",
				"657"
			}
		},
		["Lighthouse Garibs"] = {
			["id"] = "10658",
			["garibs"] = {
				"658",
				"659",
				"660",
				"661",
				"662",
				"663"
			}
		},
		["Ramp Garibs"] = {
			["id"] = "10664",
			["garibs"] = {
				"664",
				"665",
				"666",
				"667",
				"668",
				"669"
			}
		},
		["Spawn Garibs"] = {
			["id"] = "10670",
			["garibs"] = {
				"670",
				"671",
				"672",
				"673"
			}
		},
		["Sunken Ship Garibs"] = {
			["id"] = "10674",
			["garibs"] = {
				"674",
				"675",
				"676",
				"677"
			}
		},
		["Tilt Garibs A"] = {
			["id"] = "10678",
			["garibs"] = {
				"678",
				"679",
				"680",
				"681"
			}
		},
		["Tilt Garibs B"] = {
			["id"] = "10682",
			["garibs"] = {
				"682",
				"683",
				"684",
				"685"
			}
		},
		["Tip House Garibs"] = {
			["id"] = "10686",
			["garibs"] = {
				"686",
				"687",
				"688",
				"689",
				"690",
				"691"
			}
		},
		["Lighthouse Lobster Garibs"] = {
			["id"] = "10692",
			["garibs"] = {
				"692"
			}
		},
		["Lighthouse Wind-Up Garibs"] = {
			["id"] = "10693",
			["garibs"] = {
				"693"
			}
		},
		["Shore Wind-Up Garibs"] = {
			["id"] = "10694",
			["garibs"] = {
				"694"
			}
		},
		["Underwater Lobster Garibs"] = {
			["id"] = "10695",
			["garibs"] = {
				"695"
			}
		},
	},
	["AP_PIRATES_L2"] = {
		["Falling Bridge Garibs"] = {
			["id"] = "10724",
			["garibs"] = {
				"724",
				"725",
				"726",
				"727",
				"728",
				"729",
				"730",
				"731",
				"732",
				"733",
				"734",
				"735"
			}
		},
		["Glover Switch Garibs"] = {
			["id"] = "10736",
			["garibs"] = {
				"736",
				"737",
				"738",
				"739"
			}
		},
		["Goal Garibs"] = {
			["id"] = "10740",
			["garibs"] = {
				"740",
				"741",
				"742",
				"743"
			}
		},
		["Left Bridge Garibs"] = {
			["id"] = "10744",
			["garibs"] = {
				"744",
				"745",
				"746",
				"747"
			}
		},
		["Mini Platform Garibs"] = {
			["id"] = "10748",
			["garibs"] = {
				"748",
				"749",
				"750",
				"751",
				"752",
				"753",
				"754",
				"755",
				"756"
			}
		},
		["Moving Plank Garibs"] = {
			["id"] = "10757",
			["garibs"] = {
				"757",
				"758",
				"759",
				"760",
				"761",
				"762",
				"763",
				"764"
			}
		},
		["Spawn Garibs"] = {
			["id"] = "10765",
			["garibs"] = {
				"765",
				"766",
				"767"
			}
		},
		["Stairs Garibs"] = {
			["id"] = "10768",
			["garibs"] = {
				"768",
				"769",
				"770",
				"771"
			}
		},
		["Water Edge Garibs"] = {
			["id"] = "10772",
			["garibs"] = {
				"772",
				"773",
				"774",
				"775"
			}
		},
		["Conveyor Wind-Up Garibs"] = {
			["id"] = "10776",
			["garibs"] = {
				"776"
			}
		},
		["Glover Switch Wind-Up Garibs"] = {
			["id"] = "10777",
			["garibs"] = {
				"777"
			}
		},
		["Moving Plank Wind-Up Garibs"] = {
			["id"] = "10778",
			["garibs"] = {
				"778",
				"779"
			}
		},
		["Platform Lobster Garibs"] = {
			["id"] = "10780",
			["garibs"] = {
				"780"
			}
		},
		["Spawn Lobster Garibs"] = {
			["id"] = "10781",
			["garibs"] = {
				"781"
			}
		},
		["Spawn Wind-Up Garibs"] = {
			["id"] = "10782",
			["garibs"] = {
				"782"
			}
		},
		["Zig-Zag Wind-Up Garibs"] = {
			["id"] = "10783",
			["garibs"] = {
				"783"
			}
		},
	},
	["AP_PIRATES_L3"] = {
		["Arch Garibs"] = {
			["id"] = "10804",
			["garibs"] = {
				"804",
				"805"
			}
		},
		["Barrel Garibs"] = {
			["id"] = "10806",
			["garibs"] = {
				"806",
				"807",
				"808",
				"809"
			}
		},
		["Bridge Garibs"] = {
			["id"] = "10810",
			["garibs"] = {
				"810",
				"811",
				"812",
				"813"
			}
		},
		["Cave Garibs"] = {
			["id"] = "10814",
			["garibs"] = {
				"814",
				"815",
				"816",
				"817",
				"818",
				"819",
				"820",
				"821"
			}
		},
		["Cave Mouth Garibs"] = {
			["id"] = "10822",
			["garibs"] = {
				"822",
				"823"
			}
		},
		["Cracked Wall Garibs"] = {
			["id"] = "10824",
			["garibs"] = {
				"824",
				"825"
			}
		},
		["Dead End Garibs"] = {
			["id"] = "10826",
			["garibs"] = {
				"826",
				"827",
				"828",
				"829"
			}
		},
		["High House Garibs"] = {
			["id"] = "10830",
			["garibs"] = {
				"830",
				"831",
				"832"
			}
		},
		["Lobstervator Garibs"] = {
			["id"] = "10833",
			["garibs"] = {
				"833",
				"834"
			}
		},
		["Post-Stair Garibs"] = {
			["id"] = "10835",
			["garibs"] = {
				"835",
				"836",
				"837"
			}
		},
		["Push Crate Garibs"] = {
			["id"] = "10838",
			["garibs"] = {
				"838",
				"839",
				"840",
				"841"
			}
		},
		["Push Plank Garibs"] = {
			["id"] = "10842",
			["garibs"] = {
				"842",
				"843"
			}
		},
		["Ramp Garibs"] = {
			["id"] = "10844",
			["garibs"] = {
				"844",
				"845",
				"846",
				"847",
				"848",
				"849"
			}
		},
		["Stone Path Garibs"] = {
			["id"] = "10850",
			["garibs"] = {
				"850",
				"851",
				"852",
				"853"
			}
		},
		["Tilted Cliff Garibs"] = {
			["id"] = "10854",
			["garibs"] = {
				"854",
				"855",
				"856",
				"857"
			}
		},
		["Trampoline Garibs"] = {
			["id"] = "10858",
			["garibs"] = {
				"858",
				"859",
				"860",
				"861",
				"862",
				"863",
				"864",
				"865",
				"866",
				"867",
				"868",
				"869",
				"870",
				"871",
				"872",
				"873"
			}
		},
		["Warp House Garibs"] = {
			["id"] = "10874",
			["garibs"] = {
				"874",
				"875",
				"876",
				"877"
			}
		},
		["Cliff Lobster Garibs"] = {
			["id"] = "10878",
			["garibs"] = {
				"878"
			}
		},
		["Dead End Wind-Up Garibs"] = {
			["id"] = "10879",
			["garibs"] = {
				"879"
			}
		},
		["Stairs Wind-Up Garibs"] = {
			["id"] = "10880",
			["garibs"] = {
				"880",
				"881",
				"882"
			}
		},
		["Trampoline Lobster Garibs"] = {
			["id"] = "10883",
			["garibs"] = {
				"883"
			}
		},
	},
	["AP_PIRATES_BONUS"] = {
		["Barrel A Garibs"] = {
			["id"] = "10913",
			["garibs"] = {
				"913",
				"914",
				"915"
			}
		},
		["Barrel B Garibs"] = {
			["id"] = "10916",
			["garibs"] = {
				"916",
				"917",
				"918"
			}
		},
		["Barrel C Garibs"] = {
			["id"] = "10919",
			["garibs"] = {
				"919",
				"920",
				"921"
			}
		},
		["Barrel D Garibs"] = {
			["id"] = "10922",
			["garibs"] = {
				"922",
				"923",
				"924"
			}
		},
		["Barrel E Garibs"] = {
			["id"] = "10925",
			["garibs"] = {
				"925",
				"926",
				"927"
			}
		},
		["Barrel F Garibs"] = {
			["id"] = "10928",
			["garibs"] = {
				"928",
				"929",
				"930"
			}
		},
		["Barrel G Garibs"] = {
			["id"] = "10931",
			["garibs"] = {
				"931",
				"932",
				"933"
			}
		},
		["Barrel H Garibs"] = {
			["id"] = "10934",
			["garibs"] = {
				"934",
				"935",
				"936"
			}
		},
		["Center Column Garibs"] = {
			["id"] = "10937",
			["garibs"] = {
				"937",
				"938",
				"939",
				"940",
				"941"
			}
		},
		["Floating A Garibs"] = {
			["id"] = "10942",
			["garibs"] = {
				"942",
				"943",
				"944"
			}
		},
		["Floating B Garibs"] = {
			["id"] = "10945",
			["garibs"] = {
				"945",
				"946",
				"947"
			}
		},
		["Floating C Garibs"] = {
			["id"] = "10948",
			["garibs"] = {
				"948",
				"949",
				"950"
			}
		},
		["Floating D Garibs"] = {
			["id"] = "10951",
			["garibs"] = {
				"951",
				"952",
				"953"
			}
		},
		["Floating E Garibs"] = {
			["id"] = "10954",
			["garibs"] = {
				"954",
				"955",
				"956"
			}
		},
		["Floating F Garibs"] = {
			["id"] = "10957",
			["garibs"] = {
				"957",
				"958",
				"959"
			}
		},
		["Top Garibs"] = {
			["id"] = "10960",
			["garibs"] = {
				"960",
				"961",
				"962"
			}
		},
	},
	["AP_PREHISTORIC_L1"] = {
		["Alcove Garibs"] = {
			["id"] = "10970",
			["garibs"] = {
				"970",
				"971",
				"972",
				"973",
				"974",
				"975",
				"976",
				"977",
				"978",
				"979",
				"980",
				"981"
			}
		},
		["Big Island Garibs"] = {
			["id"] = "10982",
			["garibs"] = {
				"982",
				"983",
				"984",
				"985",
				"986",
				"987",
				"988",
				"989"
			}
		},
		["Cliff Bottom Garibs"] = {
			["id"] = "10990",
			["garibs"] = {
				"990",
				"991",
				"992"
			}
		},
		["Dino Garibs"] = {
			["id"] = "10993",
			["garibs"] = {
				"993",
				"994",
				"995",
				"996",
				"997",
				"998"
			}
		},
		["Double Ice Wall Garibs"] = {
			["id"] = "10999",
			["garibs"] = {
				"999",
				"1000"
			}
		},
		["Frozen Ball Garibs"] = {
			["id"] = "11001",
			["garibs"] = {
				"1001",
				"1002",
				"1003"
			}
		},
		["Goal Garibs"] = {
			["id"] = "11004",
			["garibs"] = {
				"1004",
				"1005"
			}
		},
		["Hanging Garibs"] = {
			["id"] = "11006",
			["garibs"] = {
				"1006",
				"1007",
				"1008"
			}
		},
		["Ice Bridge Garibs"] = {
			["id"] = "11009",
			["garibs"] = {
				"1009",
				"1010",
				"1011",
				"1012",
				"1013",
				"1014",
				"1015",
				"1016"
			}
		},
		["Ice Cave Garibs"] = {
			["id"] = "11017",
			["garibs"] = {
				"1017",
				"1018",
				"1019",
				"1020",
				"1021",
				"1022",
				"1023",
				"1024"
			}
		},
		["Ice Face Garibs"] = {
			["id"] = "11025",
			["garibs"] = {
				"1025",
				"1026",
				"1027"
			}
		},
		["Lake Path Garibs"] = {
			["id"] = "11028",
			["garibs"] = {
				"1028",
				"1029"
			}
		},
		["Left Below Ice Garibs"] = {
			["id"] = "11030",
			["garibs"] = {
				"1030",
				"1031",
				"1032"
			}
		},
		["Lower Cliffside Garibs"] = {
			["id"] = "11033",
			["garibs"] = {
				"1033",
				"1034"
			}
		},
		["Right Below Ice Garibs"] = {
			["id"] = "11035",
			["garibs"] = {
				"1035",
				"1036",
				"1037"
			}
		},
		["Small Island Garibs"] = {
			["id"] = "11038",
			["garibs"] = {
				"1038",
				"1039",
				"1040",
				"1041",
				"1042"
			}
		},
		["Snowball Hill Garibs"] = {
			["id"] = "11043",
			["garibs"] = {
				"1043",
				"1044",
				"1045",
				"1046"
			}
		},
		["Upper Cliffside Garibs"] = {
			["id"] = "11047",
			["garibs"] = {
				"1047",
				"1048"
			}
		},
		["Wind-Up Garibs"] = {
			["id"] = "11049",
			["garibs"] = {
				"1049"
			}
		},
	},
	["AP_PREHISTORIC_L2"] = {
		["After Valley Garibs"] = {
			["id"] = "11060",
			["garibs"] = {
				"1060",
				"1061",
				"1062",
				"1063"
			}
		},
		["Bottom Avalanche Garibs"] = {
			["id"] = "11064",
			["garibs"] = {
				"1064",
				"1065",
				"1066"
			}
		},
		["Island Garibs"] = {
			["id"] = "11067",
			["garibs"] = {
				"1067",
				"1068",
				"1069",
				"1070"
			}
		},
		["Lavafall Garib"] = {
			["id"] = "11071",
			["garibs"] = {
				"1071"
			}
		},
		["Middle Avalanche Garibs"] = {
			["id"] = "11072",
			["garibs"] = {
				"1072",
				"1073",
				"1074"
			}
		},
		["Nook Garibs"] = {
			["id"] = "11075",
			["garibs"] = {
				"1075",
				"1076"
			}
		},
		["Push Wall Garibs"] = {
			["id"] = "11077",
			["garibs"] = {
				"1077",
				"1078",
				"1079",
				"1080",
				"1081"
			}
		},
		["Raptor Garibs"] = {
			["id"] = "11082",
			["garibs"] = {
				"1082",
				"1083",
				"1084",
				"1085",
				"1086",
				"1087",
				"1088",
				"1089"
			}
		},
		["Raptor Tree Garibs"] = {
			["id"] = "11090",
			["garibs"] = {
				"1090",
				"1091",
				"1092",
				"1093"
			}
		},
		["Sign Garibs"] = {
			["id"] = "11094",
			["garibs"] = {
				"1094",
				"1095",
				"1096",
				"1097"
			}
		},
		["Skull Garib"] = {
			["id"] = "11098",
			["garibs"] = {
				"1098"
			}
		},
		["Slope Garibs"] = {
			["id"] = "11099",
			["garibs"] = {
				"1099",
				"1100",
				"1101",
				"1102"
			}
		},
		["Spawn Garibs"] = {
			["id"] = "11103",
			["garibs"] = {
				"1103",
				"1104",
				"1105",
				"1106",
				"1107"
			}
		},
		["Switches Garibs"] = {
			["id"] = "11108",
			["garibs"] = {
				"1108",
				"1109",
				"1110",
				"1111",
				"1112"
			}
		},
		["Tilt Garibs"] = {
			["id"] = "11113",
			["garibs"] = {
				"1113",
				"1114",
				"1115",
				"1116",
				"1117"
			}
		},
		["Top Avalanche Garibs"] = {
			["id"] = "11118",
			["garibs"] = {
				"1118",
				"1119",
				"1120"
			}
		},
		["Tracey Garibs"] = {
			["id"] = "11121",
			["garibs"] = {
				"1121",
				"1122",
				"1123",
				"1124"
			}
		},
		["Trees Garib"] = {
			["id"] = "11125",
			["garibs"] = {
				"1125"
			}
		},
		["Valley Garibs"] = {
			["id"] = "11126",
			["garibs"] = {
				"1126",
				"1127",
				"1128",
				"1129",
				"1130",
				"1131",
				"1132",
				"1133",
				"1134",
				"1135",
				"1136"
			}
		},
		["Slope Wind-Up Garibs"] = {
			["id"] = "11137",
			["garibs"] = {
				"1137"
			}
		},
		["Traceys Wind-Up Garibs"] = {
			["id"] = "11138",
			["garibs"] = {
				"1138"
			}
		},
		["Valley Wind-Up Garibs"] = {
			["id"] = "11139",
			["garibs"] = {
				"1139"
			}
		},
	},
	["AP_PREHISTORIC_L3"] = {
		["Cave Garibs"] = {
			["id"] = "11160",
			["garibs"] = {
				"1160",
				"1161",
				"1162",
				"1163",
				"1164",
				"1165",
				"1166"
			}
		},
		["Circle Lava Garibs"] = {
			["id"] = "11167",
			["garibs"] = {
				"1167",
				"1168",
				"1169",
				"1170",
				"1171",
				"1172",
				"1173",
				"1174"
			}
		},
		["Flying Lava Garibs"] = {
			["id"] = "11175",
			["garibs"] = {
				"1175",
				"1176",
				"1177"
			}
		},
		["Grass Ring Garibs"] = {
			["id"] = "11178",
			["garibs"] = {
				"1178",
				"1179",
				"1180",
				"1181",
				"1182",
				"1183",
				"1184",
				"1185",
				"1186",
				"1187",
				"1188",
				"1189",
				"1190",
				"1191",
				"1192"
			}
		},
		["Lava Ledge Garibs"] = {
			["id"] = "11193",
			["garibs"] = {
				"1193",
				"1194",
				"1195",
				"1196",
				"1197",
				"1198",
				"1199",
				"1200",
				"1201",
				"1202"
			}
		},
		["Love Tree Garibs"] = {
			["id"] = "11203",
			["garibs"] = {
				"1203",
				"1204",
				"1205",
				"1206",
				"1207",
				"1208",
				"1209",
				"1210"
			}
		},
		["Lower Grass Ledge Garibs"] = {
			["id"] = "11211",
			["garibs"] = {
				"1211",
				"1212"
			}
		},
		["Tracey Garibs"] = {
			["id"] = "11213",
			["garibs"] = {
				"1213",
				"1214",
				"1215",
				"1216",
				"1217",
				"1218",
				"1219",
				"1220",
				"1221",
				"1222",
				"1223",
				"1224",
				"1225",
				"1226",
				"1227",
				"1228"
			}
		},
		["Turning Stones Garibs"] = {
			["id"] = "11229",
			["garibs"] = {
				"1229",
				"1230",
				"1231",
				"1232",
				"1233"
			}
		},
		["Upper Grass Ledge Garibs"] = {
			["id"] = "11234",
			["garibs"] = {
				"1234",
				"1235",
				"1236"
			}
		},
		["Grass Ring Wind-Up Garibs"] = {
			["id"] = "11237",
			["garibs"] = {
				"1237"
			}
		},
		["Monolith Wind-Up Garibs"] = {
			["id"] = "11238",
			["garibs"] = {
				"1238",
				"1239"
			}
		},
	},
	["AP_PREHISTORIC_BONUS"] = {
		["Archway Garibs"] = {
			["id"] = "11265",
			["garibs"] = {
				"1265",
				"1266",
				"1267",
				"1268",
				"1269",
				"1270",
				"1271",
				"1272",
				"1273",
				"1274"
			}
		},
		["Fossil Garibs"] = {
			["id"] = "11275",
			["garibs"] = {
				"1275",
				"1276",
				"1277",
				"1278",
				"1279",
				"1280",
				"1281",
				"1282",
				"1283",
				"1284"
			}
		},
		["Goal Garibs"] = {
			["id"] = "11285",
			["garibs"] = {
				"1285",
				"1286",
				"1287",
				"1288",
				"1289",
				"1290",
				"1291",
				"1292",
				"1293",
				"1294"
			}
		},
		["Lava Garibs"] = {
			["id"] = "11295",
			["garibs"] = {
				"1295",
				"1296",
				"1297",
				"1298",
				"1299",
				"1300",
				"1301",
				"1302",
				"1303",
				"1304"
			}
		},
		["Sharp Turn Garibs"] = {
			["id"] = "11305",
			["garibs"] = {
				"1305",
				"1306",
				"1307",
				"1308",
				"1309",
				"1310",
				"1311",
				"1312",
				"1313",
				"1314"
			}
		},
		["Spawn Garibs"] = {
			["id"] = "11315",
			["garibs"] = {
				"1315",
				"1316",
				"1317",
				"1318",
				"1319",
				"1320",
				"1321",
				"1322",
				"1323",
				"1324"
			}
		},
	},
	["AP_FORTRESS_L1"] = {
		["Above Electric Garib"] = {
			["id"] = "11331",
			["garibs"] = {
				"1331"
			}
		},
		["Beachball Garibs"] = {
			["id"] = "11332",
			["garibs"] = {
				"1332",
				"1333",
				"1334",
				"1335",
				"1336"
			}
		},
		["Cleets Garibs"] = {
			["id"] = "11337",
			["garibs"] = {
				"1337",
				"1338",
				"1339",
				"1340",
				"1341",
				"1342"
			}
		},
		["Coffin Garibs"] = {
			["id"] = "11343",
			["garibs"] = {
				"1343",
				"1344",
				"1345",
				"1346",
				"1347",
				"1348"
			}
		},
		["Dirt Hill Garibs"] = {
			["id"] = "11349",
			["garibs"] = {
				"1349",
				"1350",
				"1351"
			}
		},
		["Dropdown Garibs"] = {
			["id"] = "11352",
			["garibs"] = {
				"1352",
				"1353",
				"1354",
				"1355"
			}
		},
		["Electric Garibs"] = {
			["id"] = "11356",
			["garibs"] = {
				"1356",
				"1357",
				"1358",
				"1359"
			}
		},
		["Ghost Garibs"] = {
			["id"] = "11360",
			["garibs"] = {
				"1360",
				"1361",
				"1362",
				"1363",
				"1364",
				"1365",
				"1366",
				"1367"
			}
		},
		["Glover Switch Garibs"] = {
			["id"] = "11368",
			["garibs"] = {
				"1368",
				"1369"
			}
		},
		["Large Plank Garibs"] = {
			["id"] = "11370",
			["garibs"] = {
				"1370",
				"1371",
				"1372",
				"1373",
				"1374"
			}
		},
		["Left Ghost Ledge Garibs"] = {
			["id"] = "11375",
			["garibs"] = {
				"1375",
				"1376",
				"1377"
			}
		},
		["Left Tower Garib"] = {
			["id"] = "11378",
			["garibs"] = {
				"1378"
			}
		},
		["Right Ghost Ledge Garibs"] = {
			["id"] = "11379",
			["garibs"] = {
				"1379",
				"1380",
				"1381"
			}
		},
		["Right Tower Garib"] = {
			["id"] = "11382",
			["garibs"] = {
				"1382"
			}
		},
		["Sky Platform Garibs"] = {
			["id"] = "11383",
			["garibs"] = {
				"1383",
				"1384",
				"1385",
				"1386"
			}
		},
		["Small Plank Garibs"] = {
			["id"] = "11387",
			["garibs"] = {
				"1387",
				"1388",
				"1389"
			}
		},
		["Wind-Up Garibs"] = {
			["id"] = "11390",
			["garibs"] = {
				"1390"
			}
		},
	},
	["AP_FORTRESS_L2"] = {
		["Carpet Garibs"] = {
			["id"] = "11415",
			["garibs"] = {
				"1415",
				"1416",
				"1417",
				"1418",
				"1419"
			}
		},
		["Collapsing Garibs"] = {
			["id"] = "11420",
			["garibs"] = {
				"1420",
				"1421",
				"1422",
				"1423",
				"1424",
				"1425"
			}
		},
		["Dropdown Garibs"] = {
			["id"] = "11426",
			["garibs"] = {
				"1426",
				"1427",
				"1428",
				"1429",
				"1430",
				"1431",
				"1432"
			}
		},
		["Electric Garibs"] = {
			["id"] = "11433",
			["garibs"] = {
				"1433",
				"1434",
				"1435",
				"1436",
				"1437",
				"1438",
				"1439",
				"1440",
				"1441",
				"1442"
			}
		},
		["Gate Garibs"] = {
			["id"] = "11443",
			["garibs"] = {
				"1443",
				"1444"
			}
		},
		["Left Rooftop Garibs"] = {
			["id"] = "11445",
			["garibs"] = {
				"1445",
				"1446",
				"1447",
				"1448",
				"1449"
			}
		},
		["Mummy Garibs"] = {
			["id"] = "11450",
			["garibs"] = {
				"1450",
				"1451",
				"1452"
			}
		},
		["Pillar Garibs"] = {
			["id"] = "11453",
			["garibs"] = {
				"1453",
				"1454",
				"1455",
				"1456",
				"1457"
			}
		},
		["Right Rooftop Garibs"] = {
			["id"] = "11458",
			["garibs"] = {
				"1458",
				"1459",
				"1460",
				"1461",
				"1462"
			}
		},
		["Samtex Garibs"] = {
			["id"] = "11463",
			["garibs"] = {
				"1463",
				"1464",
				"1465"
			}
		},
		["Swinging Garibs"] = {
			["id"] = "11466",
			["garibs"] = {
				"1466",
				"1467",
				"1468"
			}
		},
		["Wood Garibs"] = {
			["id"] = "11469",
			["garibs"] = {
				"1469",
				"1470",
				"1471",
				"1472",
				"1473"
			}
		},
		["Wind-Up Garibs"] = {
			["id"] = "11474",
			["garibs"] = {
				"1474"
			}
		},
	},
	["AP_FORTRESS_L3"] = {
		["Beachball Garibs"] = {
			["id"] = "11491",
			["garibs"] = {
				"1491",
				"1492",
				"1493",
				"1494"
			}
		},
		["Coffin Garibs"] = {
			["id"] = "11495",
			["garibs"] = {
				"1495",
				"1496",
				"1497",
				"1498"
			}
		},
		["Crumbling Garibs"] = {
			["id"] = "11499",
			["garibs"] = {
				"1499",
				"1500"
			}
		},
		["Electric Garibs"] = {
			["id"] = "11501",
			["garibs"] = {
				"1501",
				"1502",
				"1503",
				"1504",
				"1505",
				"1506",
				"1507",
				"1508"
			}
		},
		["Electric Roof Garibs"] = {
			["id"] = "11509",
			["garibs"] = {
				"1509",
				"1510",
				"1511",
				"1512",
				"1513",
				"1514",
				"1515",
				"1516"
			}
		},
		["Gate Garibs"] = {
			["id"] = "11517",
			["garibs"] = {
				"1517",
				"1518"
			}
		},
		["Guillotine Garibs"] = {
			["id"] = "11519",
			["garibs"] = {
				"1519",
				"1520",
				"1521"
			}
		},
		["L Roof Garibs"] = {
			["id"] = "11522",
			["garibs"] = {
				"1522",
				"1523",
				"1524",
				"1525",
				"1526",
				"1527"
			}
		},
		["Left U Roof Garibs"] = {
			["id"] = "11528",
			["garibs"] = {
				"1528",
				"1529",
				"1530"
			}
		},
		["Path Lip Garibs"] = {
			["id"] = "11531",
			["garibs"] = {
				"1531",
				"1532",
				"1533",
				"1534",
				"1535"
			}
		},
		["Right U Roof Garibs"] = {
			["id"] = "11536",
			["garibs"] = {
				"1536",
				"1537",
				"1538"
			}
		},
		["Slant Ring Garibs"] = {
			["id"] = "11539",
			["garibs"] = {
				"1539",
				"1540",
				"1541",
				"1542",
				"1543",
				"1544",
				"1545",
				"1546",
				"1547",
				"1548"
			}
		},
		["Stone Garibs"] = {
			["id"] = "11549",
			["garibs"] = {
				"1549",
				"1550"
			}
		},
		["Swinging Garibs"] = {
			["id"] = "11551",
			["garibs"] = {
				"1551",
				"1552",
				"1553",
				"1554"
			}
		},
		["Wood Slant Garibs"] = {
			["id"] = "11555",
			["garibs"] = {
				"1555",
				"1556",
				"1557"
			}
		},
		["Electric Wind-Up Garibs"] = {
			["id"] = "11558",
			["garibs"] = {
				"1558"
			}
		},
		["Stone Wind-Up Garibs"] = {
			["id"] = "11559",
			["garibs"] = {
				"1559",
				"1560"
			}
		},
	},
	["AP_FORTRESS_BONUS"] = {
		["Garibs A"] = {
			["id"] = "11585",
			["garibs"] = {
				"1585",
				"1586",
				"1587",
				"1588",
				"1589",
				"1590",
				"1591",
				"1592",
				"1593",
				"1594",
				"1595",
				"1596",
				"1597",
				"1598"
			}
		},
		["Garibs B"] = {
			["id"] = "11599",
			["garibs"] = {
				"1599",
				"1600",
				"1601",
				"1602",
				"1603",
				"1604",
				"1605",
				"1606",
				"1607",
				"1608",
				"1609",
				"1610",
				"1611",
				"1612"
			}
		},
		["Garibs C"] = {
			["id"] = "11613",
			["garibs"] = {
				"1613",
				"1614",
				"1615",
				"1616",
				"1617",
				"1618",
				"1619",
				"1620",
				"1621",
				"1622",
				"1623",
				"1624",
				"1625",
				"1626"
			}
		},
		["Garibs D"] = {
			["id"] = "11627",
			["garibs"] = {
				"1627",
				"1628",
				"1629",
				"1630",
				"1631",
				"1632",
				"1633",
				"1634",
				"1635",
				"1636",
				"1637",
				"1638",
				"1639",
				"1640"
			}
		},
	},
	["AP_SPACE_L1"] = {
		["Alone Fan Garibs"] = {
			["id"] = "11644",
			["garibs"] = {
				"1644",
				"1645",
				"1646"
			}
		},
		["Atop UFO Garibs"] = {
			["id"] = "11647",
			["garibs"] = {
				"1647",
				"1648",
				"1649",
				"1650",
				"1651",
				"1652",
				"1653",
				"1654",
				"1655",
				"1656"
			}
		},
		["Bridge Garibs"] = {
			["id"] = "11657",
			["garibs"] = {
				"1657",
				"1658"
			}
		},
		["Flying Platform Garibs"] = {
			["id"] = "11659",
			["garibs"] = {
				"1659",
				"1660",
				"1661",
				"1662"
			}
		},
		["Inside UFO Garibs"] = {
			["id"] = "11663",
			["garibs"] = {
				"1663",
				"1664",
				"1665",
				"1666",
				"1667",
				"1668",
				"1669",
				"1670",
				"1671",
				"1672",
				"1673",
				"1674",
				"1675",
				"1676",
				"1677",
				"1678"
			}
		},
		["Large Fan Garibs"] = {
			["id"] = "11679",
			["garibs"] = {
				"1679",
				"1680",
				"1681"
			}
		},
		["Medium Fan Garibs"] = {
			["id"] = "11682",
			["garibs"] = {
				"1682",
				"1683",
				"1684"
			}
		},
		["Sign Garib"] = {
			["id"] = "11685",
			["garibs"] = {
				"1685"
			}
		},
		["Small Fan Garibs"] = {
			["id"] = "11686",
			["garibs"] = {
				"1686",
				"1687",
				"1688"
			}
		},
		["Alone Fan Wind-Up Garibs"] = {
			["id"] = "11689",
			["garibs"] = {
				"1689"
			}
		},
		["Glover Switch Wind-Up Garibs"] = {
			["id"] = "11690",
			["garibs"] = {
				"1690"
			}
		},
		["Large Fan Wind-Up Garibs"] = {
			["id"] = "11691",
			["garibs"] = {
				"1691"
			}
		},
		["Medium Fan Wind-Up Garibs"] = {
			["id"] = "11692",
			["garibs"] = {
				"1692"
			}
		},
		["Small Fan Wind-Up Garibs"] = {
			["id"] = "11693",
			["garibs"] = {
				"1693"
			}
		},
	},
	["AP_SPACE_L2"] = {
		["Above Mashers Garibs"] = {
			["id"] = "11710",
			["garibs"] = {
				"1710",
				"1711",
				"1712",
				"1713",
				"1714"
			}
		},
		["Before Mashers Garibs"] = {
			["id"] = "11715",
			["garibs"] = {
				"1715",
				"1716",
				"1717",
				"1718"
			}
		},
		["Behind Spawn Garibs"] = {
			["id"] = "11719",
			["garibs"] = {
				"1719",
				"1720",
				"1721"
			}
		},
		["Metal Walkway Garibs"] = {
			["id"] = "11722",
			["garibs"] = {
				"1722",
				"1723"
			}
		},
		["Pyramid Garibs"] = {
			["id"] = "11724",
			["garibs"] = {
				"1724",
				"1725",
				"1726",
				"1727",
				"1728",
				"1729",
				"1730",
				"1731",
				"1732",
				"1733",
				"1734",
				"1735"
			}
		},
		["Race Bridge Garibs"] = {
			["id"] = "11736",
			["garibs"] = {
				"1736",
				"1737",
				"1738",
				"1739",
				"1740",
				"1741"
			}
		},
		["Ramp Jump Arch Garibs"] = {
			["id"] = "11742",
			["garibs"] = {
				"1742",
				"1743",
				"1744",
				"1745",
				"1746"
			}
		},
		["Spike Wall Garibs"] = {
			["id"] = "11747",
			["garibs"] = {
				"1747",
				"1748",
				"1749"
			}
		},
		["Under Spike Garibs"] = {
			["id"] = "11750",
			["garibs"] = {
				"1750",
				"1751",
				"1752",
				"1753"
			}
		},
		["Crusher Wind-Up Garibs"] = {
			["id"] = "11754",
			["garibs"] = {
				"1754",
				"1755"
			}
		},
		["Slope Wind-Up Garibs"] = {
			["id"] = "11756",
			["garibs"] = {
				"1756",
				"1757",
				"1758",
				"1759"
			}
		},
	},
	["AP_SPACE_L3"] = {
		["Above Fan Garibs"] = {
			["id"] = "11773",
			["garibs"] = {
				"1773",
				"1774",
				"1775",
				"1776",
				"1777",
				"1778",
				"1779",
				"1780",
				"1781"
			}
		},
		["Conveyor Island Garibs"] = {
			["id"] = "11782",
			["garibs"] = {
				"1782",
				"1783",
				"1784"
			}
		},
		["First Conveyor Garibs"] = {
			["id"] = "11785",
			["garibs"] = {
				"1785",
				"1786",
				"1787",
				"1788"
			}
		},
		["Glass Pyramids Garibs"] = {
			["id"] = "11789",
			["garibs"] = {
				"1789",
				"1790",
				"1791",
				"1792",
				"1793",
				"1794"
			}
		},
		["Last Conveyor Garibs"] = {
			["id"] = "11795",
			["garibs"] = {
				"1795",
				"1796",
				"1797",
				"1798"
			}
		},
		["Left Guard Rail Garibs"] = {
			["id"] = "11799",
			["garibs"] = {
				"1799",
				"1800",
				"1801",
				"1802",
				"1803"
			}
		},
		["Middle Conveyor Garibs"] = {
			["id"] = "11804",
			["garibs"] = {
				"1804",
				"1805",
				"1806",
				"1807"
			}
		},
		["Pinwheel Garibs"] = {
			["id"] = "11808",
			["garibs"] = {
				"1808",
				"1809",
				"1810",
				"1811",
				"1812",
				"1813",
				"1814",
				"1815",
				"1816",
				"1817",
				"1818",
				"1819"
			}
		},
		["Ramp Garibs"] = {
			["id"] = "11820",
			["garibs"] = {
				"1820",
				"1821",
				"1822",
				"1823",
				"1824",
				"1825",
				"1826"
			}
		},
		["Right Guard Rail Garibs"] = {
			["id"] = "11827",
			["garibs"] = {
				"1827",
				"1828",
				"1829",
				"1830",
				"1831"
			}
		},
		["Split Path Left Garibs"] = {
			["id"] = "11832",
			["garibs"] = {
				"1832",
				"1833",
				"1834",
				"1835",
				"1836",
				"1837",
				"1838"
			}
		},
		["Split Path Right Garibs"] = {
			["id"] = "11839",
			["garibs"] = {
				"1839",
				"1840",
				"1841",
				"1842",
				"1843",
				"1844"
			}
		},
		["Walkway Corner Garibs"] = {
			["id"] = "11845",
			["garibs"] = {
				"1845",
				"1846",
				"1847",
				"1848",
				"1849",
				"1850",
				"1851",
				"1852"
			}
		},
	},
	["AP_SPACE_BONUS"] = {
		["Bottom Ring Garibs"] = {
			["id"] = "11870",
			["garibs"] = {
				"1870",
				"1871",
				"1872",
				"1873",
				"1874",
				"1875"
			}
		},
		["Column A Garibs"] = {
			["id"] = "11876",
			["garibs"] = {
				"1876",
				"1877",
				"1878",
				"1879",
				"1880",
				"1881",
				"1882",
				"1883"
			}
		},
		["Column B Garibs"] = {
			["id"] = "11884",
			["garibs"] = {
				"1884",
				"1885",
				"1886",
				"1887",
				"1888",
				"1889",
				"1890",
				"1891"
			}
		},
		["Column C Garibs"] = {
			["id"] = "11892",
			["garibs"] = {
				"1892",
				"1893",
				"1894",
				"1895",
				"1896",
				"1897",
				"1898",
				"1899"
			}
		},
		["Column D Garibs"] = {
			["id"] = "11900",
			["garibs"] = {
				"1900",
				"1901",
				"1902",
				"1903",
				"1904",
				"1905",
				"1906",
				"1907"
			}
		},
		["Middle Ring Garibs"] = {
			["id"] = "11908",
			["garibs"] = {
				"1908",
				"1909",
				"1910",
				"1911",
				"1912",
				"1913"
			}
		},
		["Top Ring Garibs"] = {
			["id"] = "11914",
			["garibs"] = {
				"1914",
				"1915",
				"1916",
				"1917",
				"1918",
				"1919"
			}
		},
	}
}

GLOVERHACK = {
    RDRAMBase = 0x80000000,
    RDRAMSize = 0x800000,

        base_pointer = 0x400000,
    pc = 0x0,
    ap_items = 0x9B,
    ap_world = 0x734,
      hub_entrance = 0x0,
      door_number = 0x1,
      garib_locations = 0x4,
        garib_id = 0x4,
        garib_collected = 0x6,
        garib_object_id = 0x8,
      garib_size = 0xC,
      garib_all_collected = 0x3C4,
      enemy_locations = 0x3C8,
        enemy_id = 0x4,
        enemy_collected = 0x6,
      enemy_size = 0x8,
      life_locations = 0x440,
        life_id = 0x4,
        life_collected = 0x6,
      life_size = 0x8,
      tip_locations = 0x490,
        tip_id = 0x4,
        tip_collected = 0x6,
      tip_size = 0x8,
      checkpoint_locations = 0x4B8,
        checkpoint_id = 0x4,
        checkpoint_collected = 0x6,
      checkpoint_size = 0xC,
      switch_locations = 0x4F4,
        switch_id = 0x4,
        switch_collected = 0x6,
      switch_size = 0xC,
      potion_locations = 0x56C,
        potion_id = 0x4,
        potion_collected = 0x6,
      potion_size = 0x8,
      goal = 0x59C,
    ap_world_offset = 0x5A0,
    ap_hub_order = 0x0,
    garib_totals = 0xE,
    settings = 0x96,
      garib_logic = 0x0,
      randomize_checkpoints = 0x1,
      randomize_switches = 0x2,
      deathlink = 0x3,
      taglink = 0x4,
    hub_map = 0x8,
    world_map = 0x9,
    pc_deathlink = 0x6EC,
    n64_deathlink = 0x6EF,
    pc_taglink = 0x6ED,
    n64_taglink = 0x6F0,
    ROM_MAJOR_VERSION = 0x730,
    ROM_MINOR_VERSION = 0x731,
    ROM_PATCH_VERSION = 0x732
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
    elseif type == "enemy"
    then
        offset_size = self.enemy_size
    elseif type == "potion"
    then
        offset_size = self.enemy_size
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
    elseif type == "enemy"
    then
        local offset_location = GLOVERHACK:getOffsetLocation(self.enemy_locations, offset, type)
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.enemy_id)
        if check_id ~= item_id then
            print("ENEMY Item ID DOES NOT MATCH! CHECK OFFSET FOR ID")
            print(item_id)
        end
        local check_value = mainmemory.readbyte(world_address + offset_location + self.enemy_collected)
        if check_value == 0x0
        then
            return false
        else
            return true
        end
    elseif type == "potion"
    then
        local offset_location = GLOVERHACK:getOffsetLocation(self.potion_locations, offset, type)
        local check_id = mainmemory.read_u16_be(world_address + offset_location + self.potion_id)
        if check_id ~= item_id then
            print("POTION Item ID DOES NOT MATCH! CHECK OFFSET FOR ID")
            print(item_id)
        end
        local check_value = mainmemory.readbyte(world_address + offset_location + self.potion_collected)
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

-- function GLOVERHACK:setGaribSorting(gsort)
--     mainmemory.writebyte(self.garib_sorting + GLOVERHACK:getSettingPointer(), gsort);
-- end

function GLOVERHACK:setRandomizeSwitches(switch)
    mainmemory.writebyte(self.randomize_switches + GLOVERHACK:getSettingPointer(), switch);
end

function GLOVERHACK:setRandomizeCheckpoint(checkpoint)
    mainmemory.writebyte(self.randomize_checkpoints + GLOVERHACK:getSettingPointer(), checkpoint);
end

function GLOVERHACK:setDeathlinkEnabled(newState)
	if newState
	then
		mainmemory.writebyte(self.deathlink + GLOVERHACK:getSettingPointer(), 1);
	else
		mainmemory.writebyte(self.deathlink + GLOVERHACK:getSettingPointer(), 0);
	end
    
end

function GLOVERHACK:setTaglinkEnabled(newState)
	if newState
	then
		mainmemory.writebyte(self.taglink + GLOVERHACK:getSettingPointer(), 1);
	else
		mainmemory.writebyte(self.taglink + GLOVERHACK:getSettingPointer(), 0);
	end
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

function GLOVERHACK:getPCDeath()
	local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    return mainmemory.readbyte(hackPointerIndex + self.pc_deathlink);
end

function GLOVERHACK:getPCTag()
	local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    return mainmemory.readbyte(hackPointerIndex + self.pc_taglink);
end

function GLOVERHACK:setPCDeath(DEATH_COUNT)
	local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    mainmemory.writebyte(hackPointerIndex + self.pc_deathlink, DEATH_COUNT);
end

function GLOVERHACK:setPCTag(TAG_COUNT)
	local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    mainmemory.writebyte(hackPointerIndex + self.pc_taglink, TAG_COUNT);
end

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

function GLOVERHACK:getNLocalDeath()
	local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
    return mainmemory.readbyte(self.n64_deathlink + hackPointerIndex);
end

function GLOVERHACK:getNLocalTag()
	local hackPointerIndex = GLOVERHACK:dereferencePointer(self.base_pointer);
   return mainmemory.readbyte(hackPointerIndex + self.n64_taglink);
end

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

function garib_group_contruction()
    local checks = {}
    if GARIB_GROUPS == true and GARIB_GROUPS_MAP[WORLD_NAME] ~= nil
    then
        for group_name,group_info in pairs(GARIB_GROUPS_MAP[WORLD_NAME])
        do
            local all_pass = true
            for _,garib_id in pairs(GARIB_GROUPS_MAP[WORLD_NAME][group_name]["garibs"])
            do
                if ADDRESS_MAP[WORLD_NAME]["GARIBS"][garib_id] ~= nil
                    then
                    local offset = ADDRESS_MAP[WORLD_NAME]["GARIBS"][garib_id]["offset"]
                    local num_id = ADDRESS_MAP[WORLD_NAME]["GARIBS"][garib_id]["id"]
                    if GVR:checkLocationFlag(WORLD_ID, "garib", offset, num_id) == false
                    then
                        all_pass = false
                    end
                elseif ADDRESS_MAP[WORLD_NAME]["ENEMY_GARIBS"][garib_id] ~= nil
                then
                    local offset_list = {}
                    for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["ENEMY_GARIBS"])
                    do
                        offset_list[loc_id] = locationTable["offset"]
                    end
                    local object_id = ADDRESS_MAP[WORLD_NAME]["ENEMY_GARIBS"][garib_id]['object_id']
                    if GVR:checkEnemyGaribLocationFlag(WORLD_ID, offset_list, object_id) == false
                    then
                        all_pass = false
                    end
                end
            end
            checks[group_info["id"]] = all_pass
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

function enemy_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["ENEMIES"] ~= nil
            then
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["ENEMIES"])
                do
                    checks[loc_id] = GVR:checkLocationFlag(WORLD_ID, "enemy", locationTable['offset'], locationTable['id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function potion_check()
    local checks = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["POTIONS"] ~= nil
            then
                for loc_id,locationTable in pairs(ADDRESS_MAP[WORLD_NAME]["POTIONS"])
                do
                    checks[loc_id] = GVR:checkLocationFlag(WORLD_ID, "potion", locationTable['offset'], locationTable['id'])
                    -- print(loc_id..":"..tostring(checks[loc_id]))
                end
            end
        end
    return checks
end

function goal_check()
    local check = {}
        if ADDRESS_MAP[WORLD_NAME] ~= nil
        then
            if ADDRESS_MAP[WORLD_NAME]["GOAL"] ~= nil
            then
    			local hackPointerIndex = GLOVERHACK:dereferencePointer(GVR.base_pointer);
    			local world_address = hackPointerIndex + GVR:getWorldOffset(WORLD_ID)
				local goal_address = world_address + GVR.goal
    			local check_value = mainmemory.readbyte(goal_address)
    			check[ADDRESS_MAP[WORLD_NAME]["GOAL"]] = check_value ~= 0x0
			end
		end
	return check
end

function received_garibs(itemId)
    --Decoupled Garib Groups and Garibsanity
	if 6510000 <= itemId and itemId <= 6519999 then
		updateDecoupledGaribs(itemId - 6510000)
    elseif 6520000 <= itemId and itemId <= 6529999 then
		--Level Garibsanity
		--Index of the world the garibs coming from
		GARIB_WORLD_INDEX = getDigit(itemId, 2) * 5
		--Index of the level the garibs coming from
		GARIB_LEVEL_INDEX = itemId % 10
		--Name of the specific garibs
		GARIB_WORLD_NAME = ROM_WORLDS_TABLE[GARIB_WORLD_INDEX + GARIB_LEVEL_INDEX] .. "_GARIBS"
        TOTAL_WORLD_GARIBS[GARIB_WORLD_NAME] = TOTAL_WORLD_GARIBS[GARIB_WORLD_NAME] + 1
        GVR:setItem(ITEM_TABLE[GARIB_WORLD_NAME], TOTAL_WORLD_GARIBS[GARIB_WORLD_NAME])
	elseif 6530000 <= itemId and itemId <= 6539999 then
		--Level Garib Groups
		--Index of the world the garibs coming from
		GARIB_WORLD_INDEX = getDigit(itemId, 4) * 5
		--Index of the level the garibs coming from
		GARIB_LEVEL_INDEX = getDigit(itemId, 3)
		--Name of the specific garibs
		GARIB_WORLD_NAME = ROM_WORLDS_TABLE[GARIB_WORLD_INDEX + GARIB_LEVEL_INDEX] .. "_GARIBS"
		--Amount the garibs increase by
		TOTAL_ADDED_GARIBS = itemId % 100
		--Apply it
		TOTAL_WORLD_GARIBS[GARIB_WORLD_NAME] = TOTAL_WORLD_GARIBS[GARIB_WORLD_NAME] + TOTAL_ADDED_GARIBS
		GVR:setItem(ITEM_TABLE[GARIB_WORLD_NAME], TOTAL_WORLD_GARIBS[GARIB_WORLD_NAME])
	end
end

function updateDecoupledGaribs(incoming_garibs)
	TOTAL_SINGLE_GARIBS = TOTAL_SINGLE_GARIBS + incoming_garibs
	-- How many garibs are left to fill into worlds
	local garib_fill_counter = TOTAL_SINGLE_GARIBS
	-- What garib level index you are at
	local garib_level_index = 0
	while garib_fill_counter > 0 do
		-- If you have less garibs than the total needed to fill the world
		local garib_world = GARIB_ORDER[tostring(garib_level_index)]
		if garib_world == nil
		then
			-- If you're out of worlds, don't fill anything else
			garib_fill_counter = 0
		else
			-- If you have more garibs than the max of this world
			if garib_fill_counter > MAX_WORLD_GARIBS[garib_world]
			then
				-- Set it to the max and go to the next garib level
				garib_fill_counter = garib_fill_counter - MAX_WORLD_GARIBS[garib_world]
				TOTAL_WORLD_GARIBS[garib_world] = MAX_WORLD_GARIBS[garib_world]
				GVR:setItem(ITEM_TABLE[garib_world], TOTAL_WORLD_GARIBS[garib_world])
				garib_level_index = garib_level_index + 1
			else
				-- Otherwise, the remaining garibs go to this world
				TOTAL_WORLD_GARIBS[garib_world] = garib_fill_counter
				GVR:setItem(ITEM_TABLE[garib_world], TOTAL_WORLD_GARIBS[garib_world])
				garib_fill_counter = 0
			end
		end
	end
end

function received_moves(itemId)
    if itemId == 6500329 then
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
    --elseif itemId == 6500343 then
    --    GVR:setItem(ITEM_TABLE["AP_BEACHBALL_POTION"], 1)
    --elseif itemId == 6500344 then
    --    GVR:setItem(ITEM_TABLE["AP_DEATH_POTION"], 1)
    elseif itemId == 6500345 then
        GVR:setItem(ITEM_TABLE["AP_HELICOPTER_POTION"], 1)
    --elseif itemId == 6500346 then
    --    GVR:setItem(ITEM_TABLE["AP_FROG_POTION"], 1)
    elseif itemId == 6500347 then
        GVR:setItem(ITEM_TABLE["AP_BOOMERANG_POTION"], 1)
    elseif itemId == 6500348 then
        GVR:setItem(ITEM_TABLE["AP_SPEED_POTION"], 1)
    elseif itemId == 6500349 then
        GVR:setItem(ITEM_TABLE["AP_STICKY_POTION"], 1)
    elseif itemId == 6500350 then
        GVR:setItem(ITEM_TABLE["AP_HERCULES_POTION"], 1)
    --elseif itemId == 6500351 then
    --    GVR:setItem(ITEM_TABLE["AP_GRAB"], 1)
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
    --if itemId == 6500358 then
    --    GVR:setItem(ITEM_TABLE["AP_CHICKEN_SOUND"], TOTAL_LIVES)
    if itemId == 6500359 then
        TOTAL_LIVES = TOTAL_LIVES + 1
        GVR:setItem(ITEM_TABLE["AP_LIFE_UP"], TOTAL_LIVES)
    --elseif itemId == 6500360 then
    --    GVR:setItem(ITEM_TABLE["AP_BOOMERANG_SPELL"], TOTAL_LIVES)
    --elseif itemId == 6500361 then
    --    GVR:setItem(ITEM_TABLE["AP_BEACHBALL_SPELL"], TOTAL_LIVES)
    --elseif itemId == 6500362 then
    --    GVR:setItem(ITEM_TABLE["AP_HERCULES_SPELL"], TOTAL_LIVES)
    --elseif itemId == 6500363 then
    --    GVR:setItem(ITEM_TABLE["AP_HELICOPTER_SPELL"], TOTAL_LIVES)
    --elseif itemId == 6500364 then
    --    GVR:setItem(ITEM_TABLE["AP_SPEED_SPELL"], TOTAL_LIVES)
    --elseif itemId == 6500365 then
    --    GVR:setItem(ITEM_TABLE["AP_FROG_SPELL"], TOTAL_LIVES)
    --elseif itemId == 6500366 then
    --    GVR:setItem(ITEM_TABLE["AP_DEATH_SPELL"], TOTAL_LIVES)
    --elseif itemId == 6500367 then
    --    GVR:setItem(ITEM_TABLE["AP_STICKY_SPELL"], TOTAL_LIVES)
    end
end

function received_traps(itemId)
	--if itemId == 6500368 then
    --    GVR:setItem(ITEM_TABLE["Frog Trap"], TOTAL_LIVES)
    --elseif itemId == 6500369 then
    --    GVR:setItem(ITEM_TABLE["Cursed Ball Trap"], TOTAL_LIVES)
    --elseif itemId == 6500370 then
    --    GVR:setItem(ITEM_TABLE["Instant Crystal Trap"], TOTAL_LIVES)
    --elseif itemId == 6500371 then
    --    GVR:setItem(ITEM_TABLE["Camera Rotate Trap"], TOTAL_LIVES)
    --elseif itemId == 6500372 then
    --    GVR:setItem(ITEM_TABLE["Tip Trap"], TOTAL_LIVES)
    --end
end

function received_events(itemId)
    if itemId == 6500009 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GATE"], 1)
    elseif itemId == 6500010 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L2_RAISE_WATER"], 1)
    elseif itemId == 6500011 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L2_WATER_DRAIN"], 1)
    elseif itemId == 6500012 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L2_GATE"], 1)
    elseif itemId == 6500013 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L3_SPIN_WHEEL"], 1)
    elseif itemId == 6500014 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L3_CAVE"], 1)
	elseif itemId == 6500024 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_ELEVATOR"], 1)
	elseif itemId == 6500025 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_GATE"], 1)
	elseif itemId == 6500026 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_DOOR_A"], 1)
	elseif itemId == 6500027 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_DOOR_B"], 1)
	elseif itemId == 6500028 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_DOOR_C"], 1)
	elseif itemId == 6500029 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_ROCKET_1"], 1)
	elseif itemId == 6500030 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_ROCKET_2"], 1)
	elseif itemId == 6500031 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L1_ROCKET_3"], 1)
	elseif itemId == 6500032 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L2_DROP_GARIBS"], 1)
	elseif itemId == 6500033 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L2_FAN"], 1)
	elseif itemId == 6500034 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L3_SPIN_DOOR"], 1)
	elseif itemId == 6500035 then
	    GVR:setItem(ITEM_TABLE["AP_CARNIVAL_L3_HANDS"], 1)
	elseif itemId == 6500045 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_RAISE_BEACH"], 1)
	elseif itemId == 6500046 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_ELEVATOR"], 1)
	elseif itemId == 6500047 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_CHEST"], 1)
	elseif itemId == 6500048 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_SANDPILE"], 1)
	elseif itemId == 6500049 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_WATERSPOUT"], 1)
	elseif itemId == 6500050 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_LIGHTHOUSE"], 1)
	elseif itemId == 6500051 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_RAISE_SHIP"], 1)
	elseif itemId == 6500052 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L1_BRIDGE"], 1)
	elseif itemId == 6500053 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L2_LOWER_WATER"], 1)
	elseif itemId == 6500054 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L2_RAMP"], 1)
	elseif itemId == 6500055 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L2_GATE"], 1)
	elseif itemId == 6500056 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L3_PLATFORM_SPIN"], 1)
	elseif itemId == 6500057 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L3_TRAMPOLINE"], 1)
	elseif itemId == 6500058 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L3_STAIRS"], 1)
	elseif itemId == 6500059 then
	    GVR:setItem(ITEM_TABLE["AP_PIRATES_L3_ELEVATOR"], 1)
	elseif itemId == 6500069 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L1_LIFE_DROP"], 1)
	elseif itemId == 6500070 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L2_PLATFORM_1"], 1)
	elseif itemId == 6500071 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L2_PLATFORM_2"], 1)
	elseif itemId == 6500072 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L2_LOWER_BALL_SWITCH"], 1)
	elseif itemId == 6500073 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_DROP_GARIBS"], 1)
	elseif itemId == 6500074 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_SPIN_STONES"], 1)
	elseif itemId == 6500075 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_PROGRESSIVE_LOWER_MONOLITH_1"], 1)
	elseif itemId == 6500076 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_PROGRESSIVE_LOWER_MONOLITH_2"], 1)
	elseif itemId == 6500077 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_PROGRESSIVE_LOWER_MONOLITH_3"], 1)
	elseif itemId == 6500078 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_PROGRESSIVE_LOWER_MONOLITH_4"], 1)
	elseif itemId == 6500079 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_FLOATING_PLATFORMS"], 1)
	elseif itemId == 6500089 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_LAVA_SPINNING"], 1)
	elseif itemId == 6500081 then
	    GVR:setItem(ITEM_TABLE["AP_PREHISTORIC_L3_DIRT_ELEVATOR"], 1)
	elseif itemId == 6500091 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L1_COFFIN"], 1)
	elseif itemId == 6500092 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L1_DOORWAY"], 1)
	elseif itemId == 6500093 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L1_DRAWBRIDGE"], 1)
	elseif itemId == 6500094 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L2_GARIBS_FALL"], 1)
	elseif itemId == 6500095 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L2_CHECKPOINT_GATES"], 1)
	elseif itemId == 6500096 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L2_MUMMY_GATE"], 1)
	elseif itemId == 6500097 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L3_GATE"], 1)
	elseif itemId == 6500098 then
	    GVR:setItem(ITEM_TABLE["AP_FORTRESS_L3_SPIKES"], 1)
	elseif itemId == 6500108 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L1_ALIENS"], 1)
	elseif itemId == 6500109 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L1_FANS"], 1)
	elseif itemId == 6500110 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L1_FLYING_PLATFORMS"], 1)
	elseif itemId == 6500111 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L1_GOO_PLATFORMS"], 1)
	elseif itemId == 6500112 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L1_UFO"], 1)
	elseif itemId == 6500113 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L1_MISSILE"], 1)
	elseif itemId == 6500114 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L2_MASHERS"], 1)
	elseif itemId == 6500115 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L2_RAMP"], 1)
	elseif itemId == 6500116 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L3_HAZARD_GATE"], 1)
	elseif itemId == 6500117 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L3_SIGN"], 1)
	elseif itemId == 6500118 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L3_FAN"], 1)
	elseif itemId == 6500119 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L3_BRIDGE"], 1)
	elseif itemId == 6500120 then
	    GVR:setItem(ITEM_TABLE["AP_SPACE_L3_GLASS_GATE"], 1)
	elseif itemId == 6500127 then
	    GVR:setItem(ITEM_TABLE["AP_TRAINING_WORLD_SANDPIT"], 1)
	elseif itemId == 6500128 then
	    GVR:setItem(ITEM_TABLE["AP_TRAINING_WORLD_LOWER_TARGET"], 1)
	elseif itemId == 6500129 then
	    GVR:setItem(ITEM_TABLE["AP_TRAINING_WORLD_STAIRS"], 1)
    end
end

---------------------------------- MAP FUNCTIONS -----------------------------------

function set_map(map)
    WORLD_ID = WORLDS_TABLE[map]
    WORLD_NAME = map
end

function map_handler()
    if CURRENT_MAP == 0x09 then
        set_map("AP_TRAINING_WORLD")
    elseif CURRENT_MAP == 0x0A then
        set_map("AP_ATLANTIS_L1")
    elseif CURRENT_MAP == 0x0B then
        set_map("AP_ATLANTIS_L2")
    elseif CURRENT_MAP == 0x0C then
        set_map("AP_ATLANTIS_L3")
    elseif CURRENT_MAP == 0x0D then
        set_map("AP_ATLANTIS_BOSS")
    elseif CURRENT_MAP == 0x0E then
        set_map("AP_ATLANTIS_BONUS")

    elseif CURRENT_MAP == 0x0F then
        set_map("AP_CARNIVAL_L1")
    elseif CURRENT_MAP == 0x10 then
        set_map("AP_CARNIVAL_L2")
    elseif CURRENT_MAP == 0x11 then
        set_map("AP_CARNIVAL_L3")
    elseif CURRENT_MAP == 0x12 then
        set_map("AP_CARNIVAL_BOSS")
    elseif CURRENT_MAP == 0x13 then
        set_map("AP_CARNIVAL_BONUS")
    
    elseif CURRENT_MAP == 0x14 then
        set_map("AP_PIRATES_L1")
    elseif CURRENT_MAP == 0x15 then
        set_map("AP_PIRATES_L2")
    elseif CURRENT_MAP == 0x16 then
        set_map("AP_PIRATES_L3")
    elseif CURRENT_MAP == 0x17 then
        set_map("AP_PIRATES_BOSS")
    elseif CURRENT_MAP == 0x18 then
        set_map("AP_PIRATES_BONUS")

    elseif CURRENT_MAP == 0x19 then
        set_map("AP_PREHISTOIC_L1")
    elseif CURRENT_MAP == 0x1A then
        set_map("AP_PREHISTOIC_L2")
    elseif CURRENT_MAP == 0x1B then
        set_map("AP_PREHISTOIC_L3")
    elseif CURRENT_MAP == 0x1C then
        set_map("AP_PREHISTOIC_BOSS")
    elseif CURRENT_MAP == 0x1D then
        set_map("AP_PREHISTOIC_BONUS")

    elseif CURRENT_MAP == 0x1E then
        set_map("AP_FORTRESS_L1")
    elseif CURRENT_MAP == 0x1F then
        set_map("AP_FORTRESS_L2")
    elseif CURRENT_MAP == 0x20 then
        set_map("AP_FORTRESS_L3")
    elseif CURRENT_MAP == 0x21 then
        set_map("AP_FORTRESS_BOSS")
    elseif CURRENT_MAP == 0x22 then
        set_map("AP_FORTRESS_BONUS")

    elseif CURRENT_MAP == 0x23 then
        set_map("AP_SPACE_L1")
    elseif CURRENT_MAP == 0x24 then
        set_map("AP_SPACE_L2")
    elseif CURRENT_MAP == 0x25 then
        set_map("AP_SPACE_L3")
    elseif CURRENT_MAP == 0x26 then
        set_map("AP_SPACE_BOSS")
    elseif CURRENT_MAP == 0x29 then
        set_map("AP_SPACE_BONUS")
    end
end

function setRandomizedWorlds(WORLD_LOOKUP)
	for world_names, loading_zone_info in pairs(WORLD_LOOKUP)
	do
		local hub_number = getDigit(loading_zone_info, 2)
		local door_number = loading_zone_info % 10
		local world_id = WORLDS_TABLE[world_names]
		if world_id == nil
		then
			print("!" .. world_names .. "!")
		end
		setWorldInfo(world_id, hub_number, door_number)
	end
end

function setWorldInfo(world_id, hub_number, door_number)
    local hackPointerIndex = GLOVERHACK:dereferencePointer(GLOVERHACK.base_pointer);
    local world_address = hackPointerIndex + GLOVERHACK:getWorldOffset(world_id)
	local hub_address = world_address + GLOVERHACK.hub_entrance
	local door_address = world_address + GLOVERHACK.door_number
	mainmemory.writebyte(hub_address, hub_number)
	mainmemory.writebyte(door_address, door_number)
end

---------------------- ARCHIPELAGO FUNCTIONS -------------

function processAGIItem(item_list)
    for ap_id, memlocation in pairs(item_list) -- Items unrelated to AGI_MAP like Consumables
    do
        -- print(receive_map)
        if receive_map[tostring(ap_id)] == nil
        then
            if(6510000 <= memlocation and memlocation <= 6539999) -- Garibs
            then
                received_garibs(memlocation)
            elseif(6500190 <= memlocation and memlocation <= 6501906) -- Moves and Balls
            then
                received_moves(memlocation)
            elseif(6500358 <= memlocation and memlocation <= 6500367) -- Misc
            then
                received_misc(memlocation)
            elseif(6500368 <= memlocation and memlocation <= 6500372) -- Traps
            then
                received_traps(memlocation)
            elseif(6500000 <= memlocation and memlocation <= 6500129) -- Events
            then
                received_events(memlocation)
            end
            receive_map[tostring(ap_id)] = tostring(memlocation)
        end
    end
end

function flagCheckedLocations(location_list)
	for ap_id, memlocation in pairs(location_list)
	do
		-- Update any checked locations to be remembered
		if checked_map[tostring(ap_id)] == nil
		then
			--
			print("AP ID: " .. tostring(ap_id))
			print("Memlocation: " .. tostring(memlocation))
			--
        	checked_map[tostring(ap_id)] = tostring(memlocation)
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
	if block['triggerDeath'] ~= nil
	then
    	if block['triggerDeath'] == true and DEATH_LINK == true
    	then
    	    local death = GVR:getPCDeath()
    	    GVR:setPCDeath(death + 1)
    	end
	end
    if block['triggerTag'] ~= nil
	then
		if block['triggerTag'] == true and TAG_LINK == true
    	then
    	    local tag = GVR:getPCTag()
    	    GVR:setPCTag(tag + 1)
    	end
	end
end

function SendToClient()
    local retTable = {}
    local detect_death = false
    local detect_tag = false
	local deathAp = GVR:getPCDeath()
	local death64 = GVR:getNLocalDeath()
	-- Send the deathlink only when you're the cause
    if death64 > deathAp
    then
		if DEATH_LINK == true
		then
			if DEATH_LINK_TRIGGERED == false
			then
				detect_death = true
            	GVR:setPCDeath(deathAp + 1)
            	DEATH_LINK_TRIGGERED = true
			end
		else
			DEATH_LINK_TRIGGERED = false
            local died = GVR:getPCDeath()
            GVR:setPCDeath(died + 1)
		end
    else
        DEATH_LINK_TRIGGERED = false
    end

	
    if GVR:getPCTag() ~= GVR:getNLocalTag()
    then
		if TAG_LINK == true
		then
			if TAG_LINK_TRIGGERED == false
			then
        		detect_tag = true
        		local tag = GVR:getPCTag()
        		GVR:setPCTag(tag + 1)
        		TAG_LINK_TRIGGERED = true
			else
        		TAG_LINK_TRIGGERED = false
			end
		else
        	local tag = GVR:getPCTag()
        	GVR:setPCTag(tag + 1)
        	TAG_LINK_TRIGGERED = false
		end
	else
        TAG_LINK_TRIGGERED = false
    end
    retTable["scriptVersion"] = SCRIPT_VERSION;
    retTable["playerName"] = PLAYER;
    retTable["deathlinkActive"] = DEATH_LINK;
    retTable["taglinkActive"] = TAG_LINK;
    retTable["isDead"] = detect_death;
    retTable["isTag"] = detect_tag;
    retTable["garibs"] = garib_check()
    retTable["garib_groups"] =  garib_group_contruction()
    retTable["life"] = life_check()
    retTable["tip"] = tip_check()
    retTable["checkpoint"] = checkpoint_check()
    retTable["switch"] = switch_check()
    retTable["enemy_garibs"] = enemy_garib_check()
    retTable["enemy"] = enemy_check()
    retTable["potions"] = potion_check()
	retTable["goal"] = goal_check()

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
    local ret, error = GLV_SOCK:send(msg)
    if ret == nil then
        print(error)
    elseif CUR_STATE == STATE_INITIAL_CONNECTION_MADE then
        CUR_STATE = STATE_TENTATIVELY_CONNECTED
    elseif CUR_STATE == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        PRINT_GOAL = true;
        CUR_STATE = STATE_OK
    end
end

function receive()
    if PLAYER == "" and SEED == 0
    then
        getSlotData()
		GVR:setDeathlinkEnabled(true)
    	GVR:setTaglinkEnabled(true)
    else
        -- Send the message
        SendToClient()

        l, e = GLV_SOCK:receive()
        -- Handle incoming message
        if e == 'closed' then
            if CUR_STATE == STATE_OK then
                print("Connection closed")
            end
            CUR_STATE = STATE_UNINITIALIZED
            return
        elseif e == 'timeout' then
            AP_TIMEOUT_COUNTER = AP_TIMEOUT_COUNTER + 1
            if AP_TIMEOUT_COUNTER == 5
            then
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
    local ret, error = GLV_SOCK:send(msg)
    l, e = GLV_SOCK:receive()
    -- Handle incoming message
    if e == 'closed' then
        if CUR_STATE == STATE_OK then
            print("Connection closed")
        end
        CUR_STATE = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        AP_TIMEOUT_COUNTER = AP_TIMEOUT_COUNTER + 1
        if AP_TIMEOUT_COUNTER == 10
        then
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
        if block['slot_garib_logic'] == 1
        then
            GARIB_GROUPS = true
        end
    end
    --if block['slot_garib_sorting'] ~= nil
    --then
    --    GVR:setGaribSorting(block['slot_garib_sorting'])
    --end
	if block['slot_garib_order'] ~= nil
	then
		GARIB_ORDER = block['slot_garib_order']
	end
	if block['slot_world_lookup'] ~= nil
	then
		setRandomizedWorlds(block['slot_world_lookup'])
	end
    if block['slot_switches'] ~= nil and block['slot_switches'] ~= 0
    then
        GVR:setRandomizeSwitches(block['slot_switches'])
    end
    -- if block['slot_checkpoints'] ~= nil and block['slot_checkpoints'] ~= 0
    -- then
    --     GVR:setRandomizeCheckpoint(block['slot_checkpoints'])
    -- end
	if block['checkedLocations'] ~= nil then
		flagCheckedLocations(block['checkedLocations'])
	end
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

function getDigit(number, digit)
	return number % (10^digit) // (10^(digit - 1))
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
                    GLV_SOCK = client
                    GLV_SOCK:settimeout(0)
                end
            end
        end
        emu.frameadvance()
    end
end

main()
