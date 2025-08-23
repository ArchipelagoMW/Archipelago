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

-------------- GARIB LOGIC -----------

local GARIB_GROUPS = false

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
local DEATH_LINK = true

--------------- TAG LINK ------------------------
local TAG_LINK_TRIGGERED = false
local TAG_LINK = true



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
    "AP_SPEED_POTION",
    "AP_STICKY_POTION",
    "AP_ATLANTIS_L1_GATE",
    "AP_ATLANTIS_L2_RAISE_WATER",
    "AP_ATLANTIS_L2_WATER_DRAIN",
    "AP_ATLANTIS_L2_GATE",
    "AP_ATLANTIS_L3_SPIN_WHEEL",
    "AP_ATLANTIS_L3_CAVE",
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
				['object_id'] = 0xC7,
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
				['object_id'] = 0x012E,
			},
			["122"] = {
				['id'] = 0x07A,
				['offset'] = 55,
				['object_id'] = 0x0107,
			},
			["123"] = {
				['id'] = 0x07B,
				['offset'] = 56,
				['object_id'] = 0x0116,
			},
			["124"] = {
				['id'] = 0x07C,
				['offset'] = 57,
				['object_id'] = 0x0146,
			},
			["125"] = {
				['id'] = 0x07D,
				['offset'] = 58,
				['object_id'] = 0x0151,
			},
			["126"] = {
				['id'] = 0x07E,
				['offset'] = 59,
				['object_id'] = 0x0165,
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
				['object_id'] = 0x20D,
			},
			["213"] = {
				['id'] = 0x0D5,
				['offset'] = 70,
				['object_id'] = 0x21D,
			},
			["214"] = {
				['id'] = 0x0D6,
				['offset'] = 71,
				['object_id'] = 0x238,
			},
			["215"] = {
				['id'] = 0x0D7,
				['offset'] = 72,
				['object_id'] = 0x290,
			},
			["216"] = {
				['id'] = 0x0D8,
				['offset'] = 73,
				['object_id'] = 0x1AF,
			},
			["217"] = {
				['id'] = 0x0D9,
				['offset'] = 74,
				['object_id'] = 0x1DA,
			},
			["218"] = {
				['id'] = 0x0DA,
				['offset'] = 75,
				['object_id'] = 0x1BA,
			},
			["219"] = {
				['id'] = 0x0DB,
				['offset'] = 76,
				['object_id'] = 0x1CA,
			},
			["220"] = {
				['id'] = 0x0DC,
				['offset'] = 77,
				['object_id'] = 0x248,
			},
			["221"] = {
				['id'] = 0x0DD,
				['offset'] = 78,
				['object_id'] = 0x258,
			},
			["222"] = {
				['id'] = 0x0DE,
				['offset'] = 79,
				['object_id'] = 0x268,
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
	}
}

GLOVERHACK = {
    RDRAMBase = 0x80000000,
    RDRAMSize = 0x800000,

    base_pointer = 0x400000,
    pc = 0x0,
    ap_items = 0x92,
    ap_world = 0x718,
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
      potion_locations = 0x530,
        potion_id = 0x4,
        potion_collected = 0x6,
      potion_size = 0x8,
      goal = 0x560,
    ap_world_offset = 0x564,
    ap_hub_order = 0x0,
    garib_totals = 0xC,
    settings = 0x8C,
      garib_logic = 0x0,
      garib_sorting = 0x1,
      randomize_checkpoints = 0x2,
      randomize_switches = 0x3,
      deathlink = 0x4,
      taglink = 0x5,
    hub_map = 0x6,
    world_map = 0x7,
    pc_deathlink = 0x6DA,
    n64_deathlink = 0x6DD,
    pc_taglink = 0x6DB,
    n64_taglink = 0x6DE,
    ROM_MAJOR_VERSION = 0x715,
    ROM_MINOR_VERSION = 0x716,
    ROM_PATCH_VERSION = 0x717,
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

function GLOVERHACK:setGaribSorting(gsort)
    mainmemory.writebyte(self.garib_sorting + GLOVERHACK:getSettingPointer(), gsort);
end

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

function received_events(itemId)
    if itemId == 6500009 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L1_GATE"], 1)
    elseif itemId == 6500010 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L2_RAISE_WATER"], 1)
    elseif itemId == 6500011 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L2_WATER_DRAIN"], 1)
    elseif itemId == 6500012 then
        GVR:setItem(ITEM_TABLE["AP_ATLANTIS_L2_GATE"], 1)
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
            elseif(6500000 <= memlocation and memlocation <= 6500129) -- Events
            then
                received_events(memlocation)
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
    if deathAp ~= death64
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
    if detect_death == true
    then
        detect_death = false
    end
	if detect_tag == true
	then
		detect_tag = false
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

        l, e = BT_SOCK:receive()
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
    local ret, error = BT_SOCK:send(msg)
    l, e = BT_SOCK:receive()
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
    if block['slot_garib_sorting'] ~= nil
    then
        GVR:setGaribSorting(block['slot_garib_sorting'])
    end
    if block['slot_switches'] ~= nil and block['slot_switches'] ~= 0
    then
        GVR:setRandomizeSwitches(block['slot_switches'])
    end
    -- if block['slot_checkpoints'] ~= nil and block['slot_checkpoints'] ~= 0
    -- then
    --     GVR:setRandomizeCheckpoint(block['slot_checkpoints'])
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
