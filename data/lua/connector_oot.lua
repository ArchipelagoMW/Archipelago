local socket = require("socket")
local json = require('json')
local math = require('math')
require('common')

local last_modified_date = '2022-4-15' -- Should be the last modified date
local script_version = 3

--------------------------------------------------
-- Heavily modified form of RiptideSage's tracker
--------------------------------------------------

local NUM_BIG_POES_REQUIRED = 10

-- The offset constants are all from N64 RAM start. Offsets in the check statements are relative.
local save_context_offset = 0x11A5D0
local equipment_offset = save_context_offset + 0x70 -- 0x11A640
local scene_flags_offset = save_context_offset + 0xD4 --0x11A6A4
local shop_context_offset = save_context_offset + 0x5B4 --0x11AB84
local skulltula_flags_offset = save_context_offset + 0xE9C --0x11B46C
local event_context_offset = save_context_offset + 0xED4 --0x11B4A4
local big_poe_points_offset =  save_context_offset + 0xEBC -- 0x11B48C
local fishing_context_offset = save_context_offset + 0xEC0 --0x11B490
local item_get_inf_offset = save_context_offset + 0xEF0 --0x11B4C0
local inf_table_offset = save_context_offset + 0xEF8 -- 0x11B4C8

local temp_context = nil

local collectibles_overrides = nil
local collectible_offsets = nil

-- Offsets for scenes can be found here
-- https://wiki.cloudmodding.com/oot/Scene_Table/NTSC_1.0
-- Each scene is 0x1c bits long, chests at 0x0, switches at 0x4, collectibles at 0xc
local scene_check = function(scene_offset, bit_to_check, scene_data_offset)
    local local_scene_offset = scene_flags_offset + (0x1c * scene_offset) + scene_data_offset
    local nearby_memory = mainmemory.read_u32_be(local_scene_offset)
    return bit.check(nearby_memory,bit_to_check)
end

-- Whenever a check is opened, values are written to 0x40002C.
-- We can use this to send checks before they are written to the main save context.
-- [0] should always be 0x00 when a non-local multiworld item is checked
-- [1] is the scene id
-- [2] is the location type, which varies as input to the function
-- [3] is the location id within the scene, and represents the bit which was checked
-- REORDERED IN 7.0 TO scene id - location type - 0x00 - location id
-- Note that temp_context is 0-indexed and expected_values is 1-indexed, because consistency.
local check_temp_context = function(expected_values)
    -- if temp_context[0] ~= 0x00 then return false end
    -- for i=1,3 do
    --     if temp_context[i] ~= expected_values[i] then return false end
    -- end
    if temp_context[0] ~= expected_values[1] then return false end
    if temp_context[1] ~= expected_values[2] then return false end
    if temp_context[3] ~= expected_values[3] then return false end
    return true
end

-- When checking locations, we check two spots:
-- First, we check the main save context. This is "permanent" memory.
-- If the main save context doesn't have the check recorded, we check the temporary context instead,
-- which holds the value of the last location checked. 
-- The main save context is written on loading zone or save,
-- but we can get checks sent faster using the temporary context.

local chest_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0x0)
        or check_temp_context({scene_offset, 0x01, bit_to_check})
end

local on_the_ground_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0xC)
        or check_temp_context({scene_offset, 0x02, bit_to_check})
end

local boss_item_check = function(scene_offset)
    return on_the_ground_check(scene_offset, 0x1F)
        or check_temp_context({scene_offset, 0x00, 0x4F})
end

-- NOTE: Scrubs are stored in the "unused" block of scene memory
-- These always write instantly to save context, so no need to check temp context
local scrub_sanity_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0x10)
end

-- Why is there an extra offset of 3 for temp context checks? Who knows.
local cow_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0xC)
        or check_temp_context({scene_offset, 0x00, bit_to_check - 0x03})
end

-- DMT and DMC fairies are weird, their temp context check is special-coded for them
local great_fairy_magic_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0x4)
        or check_temp_context({scene_offset, 0x05, bit_to_check})
end

-- Fire arrow location reports 0x00570058 to 0x40002C
local fire_arrows_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0x0)
        or check_temp_context({scene_offset, 0x00, 0x58})
end

-- Bean salesman reports 0x00540016 to 0x40002C
local bean_sale_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0xC)
        or check_temp_context({scene_offset, 0x00, 0x16})
end

-- Medigoron reports 0x00620028 to 0x40002C
local medigoron_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0xC)
        or check_temp_context({scene_offset, 0x00, 0x28})
end

-- Bombchu salesman reports 0x005E0003 to 0x40002C
local salesman_check = function(scene_offset, bit_to_check)
    return scene_check(scene_offset, bit_to_check, 0xC)
        or check_temp_context({scene_offset, 0x00, 0x03})
end

--Helper method to resolve skulltula lookup location
local function skulltula_scene_to_array_index(i)
    return  (i + 3) - 2 * (i % 4)
end

-- NOTE: The Rando LocationList offsets are bit masks not locations, so
-- 0x1 -> 0 offset, 0x2 -> 1 offset, 0x4 -> 2 offset, 0x8 -> 3 offset, etc.
-- NOTE:  8-bit array, scene_offsets are filled on [0x00,0x15] but use a lookup array above
local skulltula_check = function(scene_offset, bit_to_check)
    --For some reason the skulltula array isn't a straight mapping from the scene ID
    scene_offset = skulltula_scene_to_array_index(scene_offset)
    local local_skulltula_offset = skulltula_flags_offset + (scene_offset)
    local nearby_memory = mainmemory.read_u8(local_skulltula_offset)
    return bit.check(nearby_memory,bit_to_check)
end

-- Left shelf bit masks are:
-- 0x8    0x2
-- 0x4    0x1
local shop_check = function(shop_offset, item_offset)
    local local_shop_offset = shop_context_offset
    local nearby_memory = mainmemory.read_u32_be(local_shop_offset)
    local bitToCheck = shop_offset*4 + item_offset
    return bit.check(nearby_memory,bitToCheck)
end

-- NOTE: Getting the bit poe bottle isn't flagged directly, instead only the points on the card are saved and
-- checked on each big poe turn in.
local big_poe_bottle_check = function()
    local nearby_memory = mainmemory.read_u32_be(big_poe_points_offset)
    local points_required = 100*NUM_BIG_POES_REQUIRED
    return (nearby_memory >= points_required)
end

-- Offsets can be found at the OOT save context layout here:
-- https://wiki.cloudmodding.com/oot/Save_Format#event_chk_inf
local event_check = function(major_offset,bit_to_check)
    -- shifting over to the next 4 hex digits
    local event_address = event_context_offset + 0x2 * major_offset
    local u_16_event_row = mainmemory.read_u16_be(event_address)
    return bit.check(u_16_event_row,bit_to_check)
end

-- Used by the game to track some non-quest item event flags
local item_get_info_check = function(check_offset,bit_to_check)
    local local_offset = item_get_inf_offset + (check_offset)
    local nearby_memory = mainmemory.read_u8(local_offset)
    return bit.check(nearby_memory,bit_to_check)
end

-- Used by the game to track lots of misc information (Talking to people, getting items, etc.)
local info_table_check = function(check_offset,bit_to_check)
    local local_offset = inf_table_offset + (check_offset)
    local nearby_memory = mainmemory.read_u8(local_offset)
    return bit.check(nearby_memory,bit_to_check)
end

local membership_card_check = function(scene_offset,bit_to_check)
    -- These checks used to be part of Gerudo Fortress, but they are better used as an approximation for the
    -- membership card check. You will always have obtained the membership card if you have rescued all four carpenters.
    -- checks["Gerudo Fortress - Free North F1 Carpenter"] = event_check(0x9, 0x0)
    -- checks["Gerudo Fortress - Free North F2 Carpenter"] = event_check(0x9, 0x3)
    -- checks["Gerudo Fortress - Free South F1 Carpenter"] = event_check(0x9, 0x1)
    -- checks["Gerudo Fortress - Free South F2 Carpenter"] = event_check(0x9, 0x2)

    -- No need to save these checks in a table as they combine to create a conditional
    return event_check(0x9, 0x0) and event_check(0x9, 0x1) and event_check(0x9, 0x2) and event_check(0x9, 0x3)

    -- This is the old version of the membership card check, which is inaccurate and always returns true
    -- so long as a save context is loaded
    -- return scene_check(scene_offset, bit_to_check, 0x4)
end

-- The fishing records are intricate and in their own memory area
-- NOTE: Fishing in rando is patched and getting the adult reward first doesn't result in the "Golden scale glitch"
local fishing_check = function(isAdult)
    local bitToCheck = 10 --for child
    if(isAdult) then
        bitToCheck = 11 --for adult
    end

    local nearby_memory = mainmemory.read_u32_be(fishing_context_offset)
    return bit.check(nearby_memory,bitToCheck)
end

local big_goron_sword_check = function ()
    local nearby_memory = mainmemory.read_u32_be(equipment_offset)
    local bitToCheck = 0x8
    return bit.check(nearby_memory,bitToCheck)
end

local is_master_quest_dungeon = function(mq_table_address, dungeon_id)
    return mainmemory.readbyte(mq_table_address + dungeon_id) == 1
end

local read_kokiri_forest_checks = function()
    local checks = {}
    checks["KF Midos Top Left Chest"] = chest_check(0x28, 0x00)
    checks["KF Midos Top Right Chest"] = chest_check(0x28, 0x01)
    checks["KF Midos Bottom Left Chest"] = chest_check(0x28, 0x02)
    checks["KF Midos Bottom Right Chest"] = chest_check(0x28, 0x03)
    checks["KF Kokiri Sword Chest"] = chest_check(0x55, 0x00)
    checks["KF Storms Grotto Chest"] = chest_check(0x3E, 0x0C)
    checks["KF Links House Cow"] = cow_check(0x34, 0x18)

    checks["KF GS Know It All House"] = skulltula_check(0x0C, 0x1)
    checks["KF GS Bean Patch"] = skulltula_check(0x0C, 0x0)
    checks["KF GS House of Twins"] = skulltula_check(0x0C, 0x2)

    checks["KF Shop Item 5"] = shop_check(0x6, 0x0)
    checks["KF Shop Item 6"] = shop_check(0x6, 0x1)
    checks["KF Shop Item 7"] = shop_check(0x6, 0x2)
    checks["KF Shop Item 8"] = shop_check(0x6, 0x3)

    checks["KF Shop Blue Rupee"] = on_the_ground_check(0x2D, 0x1)
    return checks
end

local read_lost_woods_checks = function()
    local checks = {}
    checks["LW Gift from Saria"] = event_check(0xC, 0x1)
    checks["LW Ocarina Memory Game"] = item_get_info_check(0x3, 0x7)
    checks["LW Target in Woods"] = item_get_info_check(0x2, 0x5)
    checks["LW Near Shortcuts Grotto Chest"] = chest_check(0x3E, 0x14)
    checks["Deku Theater Skull Mask"] = item_get_info_check(0x2, 0x6)
    checks["Deku Theater Mask of Truth"] = item_get_info_check(0x2, 0x7)
    checks["LW Skull Kid"] = item_get_info_check(0x3, 0x6)

    -- This is the first of three deku scrubs which are always included in the item pool, not just in scrub-sanity
    checks["LW Deku Scrub Near Bridge"] = info_table_check(0x33, 0x2)
    if not checks["LW Deku Scrub Near Bridge"] then
        checks["LW Deku Scrub Near Bridge"] = scrub_sanity_check(0x5B, 0xA)
    end

    -- This is the second of three deku scrubs which are always included in the item pool, not just in scrub-sanity
    checks["LW Deku Scrub Grotto Front"] = info_table_check(0x33, 0x3)
    if not checks["LW Deku Scrub Grotto Front"] then
        checks["LW Deku Scrub Grotto Front"] = scrub_sanity_check(0x1F, 0xB)
    end

    checks["LW Deku Scrub Near Deku Theater Left"] = scrub_sanity_check(0x5B, 0x2)
    checks["LW Deku Scrub Near Deku Theater Right"] = scrub_sanity_check(0x5B, 0x1)
    checks["LW Deku Scrub Grotto Rear"] = scrub_sanity_check(0x1F, 0x4)

    checks["LW GS Bean Patch Near Bridge"] = skulltula_check(0x0D, 0x0)
    checks["LW GS Bean Patch Near Theater"] = skulltula_check(0x0D, 0x1)
    checks["LW GS Above Theater"] = skulltula_check(0x0D, 0x2)
    return checks
end

local read_sacred_forest_meadow_checks = function()
    local checks = {}
    checks["SFM Wolfos Grotto Chest"] = chest_check(0x3E, 0x11)
    checks["SFM Deku Scrub Grotto Front"] = scrub_sanity_check(0x18, 0x9)
    checks["SFM Deku Scrub Grotto Rear"] = scrub_sanity_check(0x18, 0x8)
    checks["SFM GS"] = skulltula_check(0x0D, 0x3)
    return checks
end

local read_deku_tree_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x0) then
        checks["Deku Tree Map Chest"] = chest_check(0x00, 0x3)
        checks["Deku Tree Slingshot Room Side Chest"] = chest_check(0x00, 0x5)
        checks["Deku Tree Slingshot Chest"] = chest_check(0x00, 0x1)
        checks["Deku Tree Compass Chest"] = chest_check(0x00, 0x2)
        checks["Deku Tree Compass Room Side Chest"] = chest_check(0x00, 0x6)
        checks["Deku Tree Basement Chest"] = chest_check(0x00, 0x4)

        checks["Deku Tree GS Compass Room"] = skulltula_check(0x0, 0x3)
        checks["Deku Tree GS Basement Vines"] = skulltula_check(0x0, 0x2)
        checks["Deku Tree GS Basement Gate"] = skulltula_check(0x0, 0x1)
        checks["Deku Tree GS Basement Back Room"] = skulltula_check(0x0, 0x0)
    else
        checks["Deku Tree MQ Map Chest"] = chest_check(0x00, 0x3)
        checks["Deku Tree MQ Slingshot Chest"] = chest_check(0x00, 0x6)
        checks["Deku Tree MQ Slingshot Room Back Chest"] = chest_check(0x00, 0x2)
        checks["Deku Tree MQ Compass Chest"] = chest_check(0x00, 0x1)
        checks["Deku Tree MQ Basement Chest"] = chest_check(0x00, 0x4)
        checks["Deku Tree MQ Before Spinning Log Chest"] = chest_check(0x00, 0x5)
        checks["Deku Tree MQ After Spinning Log Chest"] = chest_check(0x00, 0x0)

        checks["Deku Tree MQ Deku Scrub"] = scrub_sanity_check(0x00, 0x5)

        checks["Deku Tree MQ GS Lobby"] = skulltula_check(0x0, 0x1)
        checks["Deku Tree MQ GS Compass Room"] = skulltula_check(0x0, 0x3)
        checks["Deku Tree MQ GS Basement Graves Room"] = skulltula_check(0x0, 0x2)
        checks["Deku Tree MQ GS Basement Back Room"] = skulltula_check(0x0, 0x0)
    end

    checks["Deku Tree Queen Gohma Heart"] = boss_item_check(0x11)
    return checks
end

local read_forest_temple_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x3) then
        checks["Forest Temple First Room Chest"] = chest_check(0x3, 0x3)
        checks["Forest Temple First Stalfos Chest"] = chest_check(0x3, 0x0)
        checks["Forest Temple Raised Island Courtyard Chest"] = chest_check(0x3, 0x5)
        checks["Forest Temple Map Chest"] = chest_check(0x3, 0x1)
        checks["Forest Temple Well Chest"] = chest_check(0x3, 0x9)
        checks["Forest Temple Eye Switch Chest"] = chest_check(0x3, 0x4)
        checks["Forest Temple Boss Key Chest"] = chest_check(0x3, 0xE)
        checks["Forest Temple Floormaster Chest"] = chest_check(0x3, 0x2)
        checks["Forest Temple Red Poe Chest"] = chest_check(0x3, 0xD)
        checks["Forest Temple Bow Chest"] = chest_check(0x3, 0xC)
        checks["Forest Temple Blue Poe Chest"] = chest_check(0x3, 0xF)
        checks["Forest Temple Falling Ceiling Room Chest"] = chest_check(0x3, 0x7)
        checks["Forest Temple Basement Chest"] = chest_check(0x3, 0xB)

        checks["Forest Temple GS First Room"] = skulltula_check(0x03, 0x1)
        checks["Forest Temple GS Lobby"] = skulltula_check(0x03, 0x3)
        checks["Forest Temple GS Raised Island Courtyard"] = skulltula_check(0x03, 0x0)
        checks["Forest Temple GS Level Island Courtyard"] = skulltula_check(0x03, 0x2)
        checks["Forest Temple GS Basement"] = skulltula_check(0x03, 0x4)
    else
        checks["Forest Temple MQ First Room Chest"] = chest_check(0x3, 0x3)
        checks["Forest Temple MQ Wolfos Chest"] = chest_check(0x3, 0x0)
        checks["Forest Temple MQ Well Chest"] = chest_check(0x3, 0x9)
        checks["Forest Temple MQ Raised Island Courtyard Lower Chest"] = chest_check(0x3, 0x1)
        checks["Forest Temple MQ Raised Island Courtyard Upper Chest"] = chest_check(0x3, 0x5)
        checks["Forest Temple MQ Boss Key Chest"] = chest_check(0x3, 0xE)
        checks["Forest Temple MQ Redead Chest"] = chest_check(0x3, 0x2)
        checks["Forest Temple MQ Map Chest"] = chest_check(0x3, 0xD)
        checks["Forest Temple MQ Bow Chest"] = chest_check(0x3, 0xC)
        checks["Forest Temple MQ Compass Chest"] = chest_check(0x3, 0xF)
        checks["Forest Temple MQ Falling Ceiling Room Chest"] = chest_check(0x3, 0x6)
        checks["Forest Temple MQ Basement Chest"] = chest_check(0x3, 0xB)

        checks["Forest Temple MQ GS First Hallway"] = skulltula_check(0x3, 0x1)
        checks["Forest Temple MQ GS Raised Island Courtyard"] = skulltula_check(0x3, 0x0)
        checks["Forest Temple MQ GS Level Island Courtyard"] = skulltula_check(0x3, 0x2)
        checks["Forest Temple MQ GS Well"] = skulltula_check(0x3, 0x3)
        checks["Forest Temple MQ GS Block Push Room"] = skulltula_check(0x3, 0x4)
    end

    checks["Forest Temple Phantom Ganon Heart"] = boss_item_check(0x14)
    return checks
end

local read_hyrule_field_checks = function()
    local checks = {}
    checks["HF Ocarina of Time Item"] = event_check(0x4, 0x3)
    checks["HF Near Market Grotto Chest"] = chest_check(0x3E, 0x00)
    checks["HF Tektite Grotto Freestanding PoH"] = on_the_ground_check(0x3E, 0x01)
    checks["HF Southeast Grotto Chest"] = chest_check(0x3E, 0x02)
    checks["HF Open Grotto Chest"] = chest_check(0x3E, 0x03)
    checks["HF Cow Grotto Cow"] = cow_check(0x3E, 0x19)

    -- This is the third of three deku scrubs which are always included in the item pool, not just in scrub-sanity
    checks["HF Deku Scrub Grotto"] = item_get_info_check(0x0, 0x3)
    if not checks["HF Deku Scrub Grotto"] then
        checks["HF Deku Scrub Grotto"] = scrub_sanity_check(0x10, 0x3)
    end

    checks["HF GS Cow Grotto"] = skulltula_check(0x0A, 0x0)
    checks["HF GS Near Kak Grotto"] = skulltula_check(0x0A, 0x1)
    return checks
end

local read_lon_lon_ranch_checks = function()
    local checks = {}
    checks["LLR Talons Chickens"] = item_get_info_check(0x1, 0x2)
    checks["LLR Freestanding PoH"] = on_the_ground_check(0x4C, 0x01)
    checks["LLR Tower Left Cow"] = cow_check(0x4C, 0x19)
    checks["LLR Tower Right Cow"] = cow_check(0x4C, 0x18)

    -- checks["Lon Lon Ranch - Epona"] = event_check(0x1, 0x8)

    checks["LLR Deku Scrub Grotto Left"] = scrub_sanity_check(0x26, 0x1)
    checks["LLR Deku Scrub Grotto Center"] = scrub_sanity_check(0x26, 0x4)
    checks["LLR Deku Scrub Grotto Right"] = scrub_sanity_check(0x26, 0x6)

    checks["LLR Stables Left Cow"] = cow_check(0x36, 0x18)
    checks["LLR Stables Right Cow"] = cow_check(0x36, 0x19)

    checks["LLR GS House Window"] = skulltula_check(0x0B, 0x2)
    checks["LLR GS Tree"] = skulltula_check(0x0B, 0x3)
    checks["LLR GS Rain Shed"] = skulltula_check(0x0B, 0x1)
    checks["LLR GS Back Wall"] = skulltula_check(0x0B, 0x0)
    return checks
end

--NOTE Logic has bombchus from bomchu bowling here, but it's an endless drop so it is not printed
local read_market_checks = function()
    local checks = {}
    checks["Market Shooting Gallery Reward"] = item_get_info_check(0x0, 0x5)
    checks["Market Bombchu Bowling First Prize"] = item_get_info_check(0x3, 0x1)
    checks["Market Bombchu Bowling Second Prize"] = item_get_info_check(0x3, 0x2)
    checks["Market Treasure Chest Game Reward"] = item_get_info_check(0x2, 0x3)
    checks["Market Lost Dog"] = info_table_check(0x33, 0x1)
    checks["Market 10 Big Poes"] = big_poe_bottle_check()
    checks["ToT Light Arrows Cutscene"] = event_check(0xC, 0x4)

    checks["Market GS Guard House"] = skulltula_check(0x0E, 0x3)

    checks["Market Bazaar Item 5"] = shop_check(0x4, 0x0)
    checks["Market Bazaar Item 6"] = shop_check(0x4, 0x1)
    checks["Market Bazaar Item 7"] = shop_check(0x4, 0x2)
    checks["Market Bazaar Item 8"] = shop_check(0x4, 0x3)

    checks["Market Potion Shop Item 5"] = shop_check(0x8, 0x0)
    checks["Market Potion Shop Item 6"] = shop_check(0x8, 0x1)
    checks["Market Potion Shop Item 7"] = shop_check(0x8, 0x2)
    checks["Market Potion Shop Item 8"] = shop_check(0x8, 0x3)

    checks["Market Bombchu Shop Item 5"] = shop_check(0x1, 0x0)
    checks["Market Bombchu Shop Item 6"] = shop_check(0x1, 0x1)
    checks["Market Bombchu Shop Item 7"] = shop_check(0x1, 0x2)
    checks["Market Bombchu Shop Item 8"] = shop_check(0x1, 0x3)
    return checks
end

local read_hyrule_castle_checks = function()
    local checks = {}
    checks["HC Malon Egg"] = event_check(0x1, 0x2)
    checks["HC Zeldas Letter"] = event_check(0x4, 0x0)
    checks["HC Great Fairy Reward"] = item_get_info_check(0x2, 0x1)
    checks["HC GS Tree"] = skulltula_check(0xE, 0x2)
    checks["HC GS Storms Grotto"] = skulltula_check(0xE, 0x1)
    return checks
end

local read_kakariko_village_checks = function()
    local checks = {}
    checks["Kak Anju as Child"] = item_get_info_check(0x0, 0x4)
    checks["Kak Anju as Adult"] = item_get_info_check(0x4, 0x4)
    checks["Kak Impas House Freestanding PoH"] = on_the_ground_check(0x37, 0x1)
    checks["Kak Windmill Freestanding PoH"] = on_the_ground_check(0x48, 0x1)

    checks["Kak Man on Roof"] = item_get_info_check(0x3, 0x5)
    checks["Kak Open Grotto Chest"] = chest_check(0x3E, 0x08)
    checks["Kak Redead Grotto Chest"] = chest_check(0x3E, 0x0A)
    checks["Kak Shooting Gallery Reward"] = item_get_info_check(0x0, 0x6)
    checks["Kak 10 Gold Skulltula Reward"] = event_check(0xD, 0xA)
    checks["Kak 20 Gold Skulltula Reward"] = event_check(0xD, 0xB)
    checks["Kak 30 Gold Skulltula Reward"] = event_check(0xD, 0xC)
    checks["Kak 40 Gold Skulltula Reward"] = event_check(0xD, 0xD)
    checks["Kak 50 Gold Skulltula Reward"] = event_check(0xD, 0xE)
    checks["Kak Impas House Cow"] = cow_check(0x37, 0x18)

    checks["Kak GS Tree"] = skulltula_check(0x10, 0x5)
    checks["Kak GS Near Gate Guard"] = skulltula_check(0x10, 0x1)
    checks["Kak GS Watchtower"] = skulltula_check(0x10, 0x2)
    checks["Kak GS Skulltula House"] = skulltula_check(0x10, 0x4)
    checks["Kak GS House Under Construction"] = skulltula_check(0x10, 0x3)
    checks["Kak GS Above Impas House"] = skulltula_check(0x10, 0x6)

    --In rando these shops contain different items from market bazaar/potion
    checks["Kak Bazaar Item 5"] = shop_check(0x7, 0x0)
    checks["Kak Bazaar Item 6"] = shop_check(0x7, 0x1)
    checks["Kak Bazaar Item 7"] = shop_check(0x7, 0x2)
    checks["Kak Bazaar Item 8"] = shop_check(0x7, 0x3)

    checks["Kak Potion Shop Item 5"] = shop_check(0x3, 0x0)
    checks["Kak Potion Shop Item 6"] = shop_check(0x3, 0x1)
    checks["Kak Potion Shop Item 7"] = shop_check(0x3, 0x2)
    checks["Kak Potion Shop Item 8"] = shop_check(0x3, 0x3)
    return checks
end

local read_graveyard_checks = function()
    local checks = {}
    checks["Graveyard Shield Grave Chest"] = chest_check(0x40, 0x00)
    checks["Graveyard Heart Piece Grave Chest"] = chest_check(0x3F, 0x00)
    checks["Graveyard Royal Familys Tomb Chest"] = chest_check(0x41, 0x00)
    checks["Graveyard Freestanding PoH"] = on_the_ground_check(0x53, 0x4)
    checks["Graveyard Dampe Gravedigging Tour"] = on_the_ground_check(0x53, 0x8)
    checks["Graveyard Dampe Race Hookshot Chest"] = chest_check(0x48, 0x00)
    checks["Graveyard Dampe Race Freestanding PoH"] = on_the_ground_check(0x48, 0x7)

    checks["Graveyard GS Bean Patch"] = skulltula_check(0x10, 0x0)
    checks["Graveyard GS Wall"] = skulltula_check(0x10, 0x7)
    return checks
end

local read_bottom_of_the_well_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x8) then
        checks["Bottom of the Well Front Left Fake Wall Chest"] = chest_check(0x08, 0x08)
        checks["Bottom of the Well Front Center Bombable Chest"] = chest_check(0x08, 0x02)
        checks["Bottom of the Well Back Left Bombable Chest"] = chest_check(0x08, 0x04)
        checks["Bottom of the Well Underwater Left Chest"] = chest_check(0x08, 0x09)
        checks["Bottom of the Well Freestanding Key"] = on_the_ground_check(0x08, 0x01)
        checks["Bottom of the Well Compass Chest"] = chest_check(0x08, 0x01)
        checks["Bottom of the Well Center Skulltula Chest"] = chest_check(0x08, 0x0E)
        checks["Bottom of the Well Right Bottom Fake Wall Chest"] = chest_check(0x08, 0x05)
        checks["Bottom of the Well Fire Keese Chest"] = chest_check(0x08, 0x0A)
        checks["Bottom of the Well Like Like Chest"] = chest_check(0x08, 0x0C)
        checks["Bottom of the Well Map Chest"] = chest_check(0x08, 0x07)
        checks["Bottom of the Well Underwater Front Chest"] = chest_check(0x08, 0x10)
        checks["Bottom of the Well Invisible Chest"] = chest_check(0x08, 0x14)
        checks["Bottom of the Well Lens of Truth Chest"] = chest_check(0x08, 0x03)

        checks["Bottom of the Well GS West Inner Room"] = skulltula_check(0x08, 0x2)
        checks["Bottom of the Well GS East Inner Room"] = skulltula_check(0x08, 0x1)
        checks["Bottom of the Well GS Like Like Cage"] = skulltula_check(0x08, 0x0)
    else
        checks["Bottom of the Well MQ Map Chest"] = chest_check(0x8, 0x3)
        checks["Bottom of the Well MQ East Inner Room Freestanding Key"] = on_the_ground_check(0x8, 0x1)
        checks["Bottom of the Well MQ Compass Chest"] = chest_check(0x8, 0x2)
        checks["Bottom of the Well MQ Dead Hand Freestanding Key"] = on_the_ground_check(0x8, 0x2)
        checks["Bottom of the Well MQ Lens of Truth Chest"] = chest_check(0x8, 0x1)

        checks["Bottom of the Well MQ GS Coffin Room"] = skulltula_check(0x08, 0x2)
        checks["Bottom of the Well MQ GS West Inner Room"] = skulltula_check(0x08, 0x1)
        checks["Bottom of the Well MQ GS Basement"] = skulltula_check(0x08, 0x0)
    end

    return checks
end

local read_shadow_temple_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x7) then
        checks["Shadow Temple Map Chest"] = chest_check(0x07, 0x01)
        checks["Shadow Temple Hover Boots Chest"] = chest_check(0x07, 0x07)
        checks["Shadow Temple Compass Chest"] = chest_check(0x07, 0x03)
        checks["Shadow Temple Early Silver Rupee Chest"] = chest_check(0x07, 0x02)
        checks["Shadow Temple Invisible Blades Visible Chest"] = chest_check(0x07, 0x0C)
        checks["Shadow Temple Invisible Blades Invisible Chest"] = chest_check(0x07, 0x16)
        checks["Shadow Temple Falling Spikes Lower Chest"] = chest_check(0x07, 0x05)
        checks["Shadow Temple Falling Spikes Upper Chest"] = chest_check(0x07, 0x06)
        checks["Shadow Temple Falling Spikes Switch Chest"] = chest_check(0x07, 0x04)
        checks["Shadow Temple Invisible Spikes Chest"] = chest_check(0x07, 0x09)
        checks["Shadow Temple Freestanding Key"] = on_the_ground_check(0x07, 0x01)
        checks["Shadow Temple Wind Hint Chest"] = chest_check(0x07, 0x15)
        checks["Shadow Temple After Wind Enemy Chest"] = chest_check(0x07, 0x08)
        checks["Shadow Temple After Wind Hidden Chest"] = chest_check(0x07, 0x14)
        checks["Shadow Temple Spike Walls Left Chest"] = chest_check(0x07, 0x0A)
        checks["Shadow Temple Boss Key Chest"] = chest_check(0x07, 0x0B)
        checks["Shadow Temple Invisible Floormaster Chest"] = chest_check(0x07, 0x0D)

        checks["Shadow Temple GS Invisible Blades Room"] = skulltula_check(0x07, 0x3)
        checks["Shadow Temple GS Falling Spikes Room"] = skulltula_check(0x07, 0x1)
        checks["Shadow Temple GS Single Giant Pot"] = skulltula_check(0x07, 0x0)
        checks["Shadow Temple GS Near Ship"] = skulltula_check(0x07, 0x4)
        checks["Shadow Temple GS Triple Giant Pot"] = skulltula_check(0x07, 0x2)
    else
        checks["Shadow Temple MQ Early Gibdos Chest"] = chest_check(0x7, 0x3)
        checks["Shadow Temple MQ Map Chest"] = chest_check(0x7, 0x2)
        checks["Shadow Temple MQ Near Ship Invisible Chest"] = chest_check(0x7, 0xE)
        checks["Shadow Temple MQ Compass Chest"] = chest_check(0x7, 0x1)
        checks["Shadow Temple MQ Hover Boots Chest"] = chest_check(0x7, 0x7)
        checks["Shadow Temple MQ Invisible Blades Invisible Chest"] = chest_check(0x7, 0x16)
        checks["Shadow Temple MQ Invisible Blades Visible Chest"] = chest_check(0x7, 0xC)
        checks["Shadow Temple MQ Beamos Silver Rupees Chest"] = chest_check(0x7, 0xF)
        checks["Shadow Temple MQ Falling Spikes Lower Chest"] = chest_check(0x7, 0x5)
        checks["Shadow Temple MQ Falling Spikes Upper Chest"] = chest_check(0x7, 0x6)
        checks["Shadow Temple MQ Falling Spikes Switch Chest"] = chest_check(0x7, 0x4)
        checks["Shadow Temple MQ Invisible Spikes Chest"] = chest_check(0x7, 0x9)
        checks["Shadow Temple MQ Stalfos Room Chest"] = chest_check(0x7, 0x10)
        checks["Shadow Temple MQ Wind Hint Chest"] = chest_check(0x7, 0x15)
        checks["Shadow Temple MQ After Wind Hidden Chest"] = chest_check(0x7, 0x14)
        checks["Shadow Temple MQ After Wind Enemy Chest"] = chest_check(0x7, 0x8)
        checks["Shadow Temple MQ Boss Key Chest"] = chest_check(0x7, 0xB)
        checks["Shadow Temple MQ Spike Walls Left Chest"] = chest_check(0x7, 0xA)
        checks["Shadow Temple MQ Freestanding Key"] = on_the_ground_check(0x7, 0x6)
        checks["Shadow Temple MQ Bomb Flower Chest"] = chest_check(0x7, 0xD)

        checks["Shadow Temple MQ GS Falling Spikes Room"] = skulltula_check(0x7, 0x1)
        checks["Shadow Temple MQ GS Wind Hint Room"] = skulltula_check(0x7, 0x0)
        checks["Shadow Temple MQ GS After Wind"] = skulltula_check(0x7, 0x3)
        checks["Shadow Temple MQ GS After Ship"] = skulltula_check(0x7, 0x4)
        checks["Shadow Temple MQ GS Near Boss"] = skulltula_check(0x7, 0x2)
    end

    checks["Shadow Temple Bongo Bongo Heart"] = boss_item_check(0x18)
    return checks
end

local read_death_mountain_trail_checks = function()
    local checks = {}
    checks["DMT Freestanding PoH"] = on_the_ground_check(0x60, 0x1E)
    checks["DMT Chest"] = chest_check(0x60, 0x01)
    checks["DMT Storms Grotto Chest"] = chest_check(0x3E, 0x17)
    checks["DMT Great Fairy Reward"] = great_fairy_magic_check(0x3B, 0x18) or check_temp_context({0xFF, 0x05, 0x13})
    checks["DMT Biggoron"] = big_goron_sword_check()
    checks["DMT Cow Grotto Cow"] = cow_check(0x3E, 0x18)

    checks["DMT GS Near Kak"] = skulltula_check(0x0F, 0x2)
    checks["DMT GS Bean Patch"] = skulltula_check(0x0F, 0x1)
    checks["DMT GS Above Dodongos Cavern"] = skulltula_check(0x0F, 0x3)
    checks["DMT GS Falling Rocks Path"] = skulltula_check(0x0F, 0x4)
    return checks
end

local read_goron_city_checks = function()
    local checks = {}
    checks["GC Darunias Joy"] = event_check(0x3, 0x6)
    checks["GC Pot Freestanding PoH"] = on_the_ground_check(0x62, 0x1F)
    checks["GC Rolling Goron as Child"] = info_table_check(0x22, 0x6)
    checks["GC Rolling Goron as Adult"] = info_table_check(0x20, 0x1)
    checks["GC Medigoron"] = medigoron_check(0x62, 0x1)
    checks["GC Maze Left Chest"] = chest_check(0x62, 0x00)
    checks["GC Maze Right Chest"] = chest_check(0x62, 0x01)
    checks["GC Maze Center Chest"] = chest_check(0x62, 0x02)
    checks["GC Deku Scrub Grotto Left"] = scrub_sanity_check(0x25, 0x1)
    checks["GC Deku Scrub Grotto Center"] = scrub_sanity_check(0x25, 0x4)
    checks["GC Deku Scrub Grotto Right"] = scrub_sanity_check(0x25, 0x6)
    checks["GC GS Center Platform"] = skulltula_check(0x0F, 0x5)
    checks["GC GS Boulder Maze"] = skulltula_check(0x0F, 0x6)

    checks["GC Shop Item 5"] = shop_check(0x5, 0x0)
    checks["GC Shop Item 6"] = shop_check(0x5, 0x1)
    checks["GC Shop Item 7"] = shop_check(0x5, 0x2)
    checks["GC Shop Item 8"] = shop_check(0x5, 0x3)
    return checks
end

local read_death_mountain_crater_checks = function()
    local checks = {}
    checks["DMC Volcano Freestanding PoH"] = on_the_ground_check(0x61, 0x08)
    checks["DMC Wall Freestanding PoH"] = on_the_ground_check(0x61, 0x02)
    checks["DMC Upper Grotto Chest"] = chest_check(0x3E, 0x1A)
    checks["DMC Great Fairy Reward"] = great_fairy_magic_check(0x3B, 0x10) or check_temp_context({0xFF, 0x05, 0x14})

    checks["DMC Deku Scrub"] = scrub_sanity_check(0x61, 0x6)
    checks["DMC Deku Scrub Grotto Left"] = scrub_sanity_check(0x23, 0x1)
    checks["DMC Deku Scrub Grotto Center"] = scrub_sanity_check(0x23, 0x4)
    checks["DMC Deku Scrub Grotto Right"] = scrub_sanity_check(0x23, 0x6)

    checks["DMC GS Crate"] = skulltula_check(0x0F, 0x7)
    checks["DMC GS Bean Patch"] = skulltula_check(0x0F, 0x0)
    return checks
end

local read_dodongos_cavern_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x1) then
        checks["Dodongos Cavern Map Chest"] = chest_check(0x01, 0x8)
        checks["Dodongos Cavern Compass Chest"] = chest_check(0x01, 0x5)
        checks["Dodongos Cavern Bomb Flower Platform Chest"] = chest_check(0x01, 0x6)
        checks["Dodongos Cavern Bomb Bag Chest"] = chest_check(0x01, 0x4)
        checks["Dodongos Cavern End of Bridge Chest"] = chest_check(0x01, 0xA)

        checks["Dodongos Cavern Deku Scrub Lobby"] = scrub_sanity_check(0x1, 0x5)
        checks["Dodongos Cavern Deku Scrub Side Room Near Dodongos"] = scrub_sanity_check(0x1, 0x2)
        checks["Dodongos Cavern Deku Scrub Near Bomb Bag Left"] = scrub_sanity_check(0x1, 0x1)
        checks["Dodongos Cavern Deku Scrub Near Bomb Bag Right"] = scrub_sanity_check(0x1, 0x4)

        checks["Dodongos Cavern GS Side Room Near Lower Lizalfos"] = skulltula_check(0x01, 0x4)
        checks["Dodongos Cavern GS Scarecrow"] = skulltula_check(0x01, 0x1)
        checks["Dodongos Cavern GS Alcove Above Stairs"] = skulltula_check(0x01, 0x2)
        checks["Dodongos Cavern GS Vines Above Stairs"] = skulltula_check(0x01, 0x0)
        checks["Dodongos Cavern GS Back Room"] = skulltula_check(0x01, 0x3)
    else
        checks["Dodongos Cavern MQ Map Chest"] = chest_check(0x1, 0x0)
        checks["Dodongos Cavern MQ Bomb Bag Chest"] = chest_check(0x1, 0x4)
        checks["Dodongos Cavern MQ Torch Puzzle Room Chest"] = chest_check(0x1, 0x3)
        checks["Dodongos Cavern MQ Larvae Room Chest"] = chest_check(0x1, 0x2)
        checks["Dodongos Cavern MQ Compass Chest"] = chest_check(0x1, 0x5)
        checks["Dodongos Cavern MQ Under Grave Chest"] = chest_check(0x1, 0x1)

        checks["Dodongos Cavern MQ Deku Scrub Lobby Front"] = scrub_sanity_check(0x1, 0x4)
        checks["Dodongos Cavern MQ Deku Scrub Lobby Rear"] = scrub_sanity_check(0x1, 0x2)
        checks["Dodongos Cavern MQ Deku Scrub Side Room Near Lower Lizalfos"] = scrub_sanity_check(0x1, 0x8)
        checks["Dodongos Cavern MQ Deku Scrub Staircase"] = scrub_sanity_check(0x1, 0x5)

        checks["Dodongos Cavern MQ GS Scrub Room"] = skulltula_check(0x1, 0x1)
        checks["Dodongos Cavern MQ GS Larvae Room"] = skulltula_check(0x1, 0x4)
        checks["Dodongos Cavern MQ GS Lizalfos Room"] = skulltula_check(0x1, 0x2)
        checks["Dodongos Cavern MQ GS Song of Time Block Room"] = skulltula_check(0x1, 0x3)
        checks["Dodongos Cavern MQ GS Back Area"] = skulltula_check(0x1, 0x0)
    end

    -- Both of these are shared between vanilla and MQ
    checks["Dodongos Cavern Boss Room Chest"] = chest_check(0x12, 0x0)
    checks["Dodongos Cavern King Dodongo Heart"] = boss_item_check(0x12)
    return checks
end

local read_fire_temple_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x4) then
        checks["Fire Temple Near Boss Chest"] = chest_check(0x04, 0x01)
        checks["Fire Temple Flare Dancer Chest"] = chest_check(0x04, 0x00)
        checks["Fire Temple Boss Key Chest"] = chest_check(0x04, 0x0C)
        checks["Fire Temple Big Lava Room Lower Open Door Chest"] = chest_check(0x04, 0x04)
        checks["Fire Temple Big Lava Room Blocked Door Chest"] = chest_check(0x04, 0x02)
        checks["Fire Temple Boulder Maze Lower Chest"] = chest_check(0x04, 0x03)
        checks["Fire Temple Boulder Maze Side Room Chest"] = chest_check(0x04, 0x08)
        checks["Fire Temple Map Chest"] = chest_check(0x04, 0x0A)
        checks["Fire Temple Boulder Maze Shortcut Chest"] = chest_check(0x04, 0x0B)
        checks["Fire Temple Boulder Maze Upper Chest"] = chest_check(0x04, 0x06)
        checks["Fire Temple Scarecrow Chest"] = chest_check(0x04, 0x0D)
        checks["Fire Temple Compass Chest"] = chest_check(0x04, 0x07)
        checks["Fire Temple Megaton Hammer Chest"] = chest_check(0x04, 0x05)
        checks["Fire Temple Highest Goron Chest"] = chest_check(0x04, 0x09)

        checks["Fire Temple GS Boss Key Loop"] = skulltula_check(0x04, 0x1)
        checks["Fire Temple GS Song of Time Room"] = skulltula_check(0x04, 0x0)
        checks["Fire Temple GS Boulder Maze"] = skulltula_check(0x04, 0x2)
        checks["Fire Temple GS Scarecrow Climb"] = skulltula_check(0x04, 0x4)
        checks["Fire Temple GS Scarecrow Top"] = skulltula_check(0x04, 0x3)
    else
        checks["Fire Temple MQ Map Room Side Chest"] = chest_check(0x4, 0x2)
        checks["Fire Temple MQ Megaton Hammer Chest"] = chest_check(0x4, 0x0)
        checks["Fire Temple MQ Map Chest"] = chest_check(0x4, 0xC)
        checks["Fire Temple MQ Near Boss Chest"] = chest_check(0x4, 0x7)
        checks["Fire Temple MQ Big Lava Room Blocked Door Chest"] = chest_check(0x4, 0x1)
        checks["Fire Temple MQ Boss Key Chest"] = chest_check(0x4, 0x4)
        checks["Fire Temple MQ Lizalfos Maze Side Room Chest"] = chest_check(0x4, 0x8)
        checks["Fire Temple MQ Compass Chest"] = chest_check(0x4, 0xB)
        checks["Fire Temple MQ Lizalfos Maze Upper Chest"] = chest_check(0x4, 0x6)
        checks["Fire Temple MQ Lizalfos Maze Lower Chest"] = chest_check(0x4, 0x3)
        checks["Fire Temple MQ Freestanding Key"] = on_the_ground_check(0x4, 0x1C)
        checks["Fire Temple MQ Chest On Fire"] = chest_check(0x4, 0x5)

        checks["Fire Temple MQ GS Big Lava Room Open Door"] = skulltula_check(0x4, 0x0)
        checks["Fire Temple MQ GS Skull On Fire"] = skulltula_check(0x4, 0x2)
        checks["Fire Temple MQ GS Flame Maze Center"] = skulltula_check(0x4, 0x3)
        checks["Fire Temple MQ GS Flame Maze Side Room"] = skulltula_check(0x4, 0x4)
        checks["Fire Temple MQ GS Above Flame Maze"] = skulltula_check(0x4, 0x1)
    end

    checks["Fire Temple Volvagia Heart"] = boss_item_check(0x15)
    return checks
end

local read_zoras_river_checks = function()
    local checks = {}
    checks["ZR Magic Bean Salesman"] = bean_sale_check(0x54, 0x1)
    checks["ZR Open Grotto Chest"] = chest_check(0x3E, 0x09)
    checks["ZR Frogs in the Rain"] = event_check(0xD, 0x6)
    checks["ZR Frogs Ocarina Game"] = event_check(0xD, 0x0)
    checks["ZR Near Open Grotto Freestanding PoH"] = on_the_ground_check(0x54, 0x04)
    checks["ZR Near Domain Freestanding PoH"] = on_the_ground_check(0x54, 0x0B)
    checks["ZR Deku Scrub Grotto Front"] = scrub_sanity_check(0x15, 0x9)
    checks["ZR Deku Scrub Grotto Rear"] = scrub_sanity_check(0x15, 0x8)

    checks["ZR Frogs Zeldas Lullaby"] = event_check(0xD, 0x1)
    checks["ZR Frogs Eponas Song"] = event_check(0xD, 0x2)
    checks["ZR Frogs Suns Song"] = event_check(0xD, 0x3)
    checks["ZR Frogs Sarias Song"] = event_check(0xD, 0x4)
    checks["ZR Frogs Song of Time"] = event_check(0xD, 0x5)

    checks["ZR GS Tree"] = skulltula_check(0x11, 0x1)
    --NOTE: There is no GS in the soft soil. It's the only one that doesn't have one.
    checks["ZR GS Ladder"] = skulltula_check(0x11, 0x0)
    checks["ZR GS Near Raised Grottos"] = skulltula_check(0x11, 0x4)
    checks["ZR GS Above Bridge"] = skulltula_check(0x11, 0x3)
    return checks
end

local read_zoras_domain_checks = function()
    local checks = {}
    checks["ZD Diving Minigame"] = event_check(0x3, 0x8)
    checks["ZD Chest"] = chest_check(0x58, 0x00)
    checks["ZD King Zora Thawed"] = info_table_check(0x26, 0x1)
    checks["ZD GS Frozen Waterfall"] = skulltula_check(0x11, 0x6)

    checks["ZD Shop Item 5"] = shop_check(0x2, 0x0)
    checks["ZD Shop Item 6"] = shop_check(0x2, 0x1)
    checks["ZD Shop Item 7"] = shop_check(0x2, 0x2)
    checks["ZD Shop Item 8"] = shop_check(0x2, 0x3)
    return checks
end

local read_zoras_fountain_checks = function()
    local checks = {}
    checks["ZF Great Fairy Reward"] = item_get_info_check(0x2, 0x0)
    checks["ZF Iceberg Freestanding PoH"] = on_the_ground_check(0x59, 0x01)
    checks["ZF Bottom Freestanding PoH"] = on_the_ground_check(0x59, 0x14)
    checks["ZF GS Above the Log"] = skulltula_check(0x11, 0x2)
    checks["ZF GS Tree"] = skulltula_check(0x11, 0x7)
    checks["ZF GS Hidden Cave"] = skulltula_check(0x11, 0x5)
    return checks
end

local read_jabu_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x2) then
        checks["Jabu Jabus Belly Boomerang Chest"] = chest_check(0x02, 0x01)
        checks["Jabu Jabus Belly Map Chest"] = chest_check(0x02, 0x02)
        checks["Jabu Jabus Belly Compass Chest"] = chest_check(0x02, 0x04)
        checks["Jabu Jabus Belly Deku Scrub"] = scrub_sanity_check(0x02, 0x1)
        checks["Jabu Jabus Belly GS Water Switch Room"] = skulltula_check(0x02, 0x3)
        checks["Jabu Jabus Belly GS Lobby Basement Lower"] = skulltula_check(0x02, 0x0)
        checks["Jabu Jabus Belly GS Lobby Basement Upper"] = skulltula_check(0x02, 0x1)
        checks["Jabu Jabus Belly GS Near Boss"] = skulltula_check(0x02, 0x2)
    else
        checks["Jabu Jabus Belly MQ Map Chest"] = chest_check(0x2, 0x3)
        checks["Jabu Jabus Belly MQ First Room Side Chest"] = chest_check(0x2, 0x5)
        checks["Jabu Jabus Belly MQ Second Room Lower Chest"] = chest_check(0x2, 0x2)
        checks["Jabu Jabus Belly MQ Compass Chest"] = chest_check(0x2, 0x0)
        checks["Jabu Jabus Belly MQ Basement Near Switches Chest"] = chest_check(0x2, 0x8)
        checks["Jabu Jabus Belly MQ Basement Near Vines Chest"] = chest_check(0x2, 0x4)
        checks["Jabu Jabus Belly MQ Boomerang Room Small Chest"] = chest_check(0x2, 0x1)
        checks["Jabu Jabus Belly MQ Boomerang Chest"] = chest_check(0x2, 0x6)
        checks["Jabu Jabus Belly MQ Falling Like Like Room Chest"] = chest_check(0x2, 0x9)
        checks["Jabu Jabus Belly MQ Second Room Upper Chest"] = chest_check(0x2, 0x7)
        checks["Jabu Jabus Belly MQ Near Boss Chest"] = chest_check(0x2, 0xA)

        checks["Jabu Jabus Belly MQ Cow"] = cow_check(0x2, 0x18)

        checks["Jabu Jabus Belly MQ GS Boomerang Chest Room"] = skulltula_check(0x2, 0x0)
        checks["Jabu Jabus Belly MQ GS Tailpasaran Room"] = skulltula_check(0x2, 0x2)
        checks["Jabu Jabus Belly MQ GS Invisible Enemies Room"] = skulltula_check(0x2, 0x3)
        checks["Jabu Jabus Belly MQ GS Near Boss"] = skulltula_check(0x2, 0x1)
    end

    checks["Jabu Jabus Belly Barinade Heart"] = boss_item_check(0x13)
    return checks
end

local read_ice_cavern_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x9) then
        checks["Ice Cavern Map Chest"] = chest_check(0x09, 0x00)
        checks["Ice Cavern Compass Chest"] = chest_check(0x09, 0x01)
        checks["Ice Cavern Freestanding PoH"] = on_the_ground_check(0x09, 0x01)
        checks["Ice Cavern Iron Boots Chest"] = chest_check(0x09, 0x02)
        checks["Ice Cavern GS Spinning Scythe Room"] = skulltula_check(0x09, 0x1)
        checks["Ice Cavern GS Heart Piece Room"] = skulltula_check(0x09, 0x2)
        checks["Ice Cavern GS Push Block Room"] = skulltula_check(0x09, 0x0)
    else
        checks["Ice Cavern MQ Map Chest"] = chest_check(0x09, 0x01)
        checks["Ice Cavern MQ Compass Chest"] = chest_check(0x09, 0x00)
        checks["Ice Cavern MQ Freestanding PoH"] = on_the_ground_check(0x09, 0x01)
        checks["Ice Cavern MQ Iron Boots Chest"] = chest_check(0x09, 0x02)

        checks["Ice Cavern MQ GS Red Ice"] = skulltula_check(0x09, 0x1)
        checks["Ice Cavern MQ GS Ice Block"] = skulltula_check(0x09, 0x2)
        checks["Ice Cavern MQ GS Scarecrow"] = skulltula_check(0x09, 0x0)
    end
    return checks
end

local read_lake_hylia_checks = function()
    local checks = {}
    checks["LH Underwater Item"] = event_check(0x3, 0x1)
    checks["LH Child Fishing"] = fishing_check(false)
    checks["LH Adult Fishing"] = fishing_check(true)
    checks["LH Lab Dive"] = item_get_info_check(0x3, 0x0)
    checks["LH Freestanding PoH"] = on_the_ground_check(0x57, 0x1E)
    --It's not actually a chest, but it is marked in the chest section
    checks["LH Sun"] = fire_arrows_check(0x57, 0x0)
    checks["LH Deku Scrub Grotto Left"] = scrub_sanity_check(0x19, 0x1)
    checks["LH Deku Scrub Grotto Center"] = scrub_sanity_check(0x19, 0x4)
    checks["LH Deku Scrub Grotto Right"] = scrub_sanity_check(0x19, 0x6)

    checks["LH GS Lab Wall"] = skulltula_check(0x12, 0x2)
    checks["LH GS Bean Patch"] = skulltula_check(0x12, 0x0)
    checks["LH GS Small Island"] = skulltula_check(0x12, 0x1)
    checks["LH GS Lab Crate"] = skulltula_check(0x12, 0x3)
    checks["LH GS Tree"] = skulltula_check(0x12, 0x4)
    return checks
end

local read_water_temple_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x5) then
        checks["Water Temple Compass Chest"] = chest_check(0x05, 0x09)
        checks["Water Temple Map Chest"] = chest_check(0x05, 0x02)
        checks["Water Temple Cracked Wall Chest"] = chest_check(0x05, 0x00)
        checks["Water Temple Torches Chest"] = chest_check(0x05, 0x01)
        checks["Water Temple Boss Key Chest"] = chest_check(0x05, 0x05)
        checks["Water Temple Central Pillar Chest"] = chest_check(0x05, 0x06)
        checks["Water Temple Central Bow Target Chest"] = chest_check(0x05, 0x08)
        checks["Water Temple Longshot Chest"] = chest_check(0x05, 0x07)
        checks["Water Temple River Chest"] = chest_check(0x05, 0x03)
        checks["Water Temple Dragon Chest"] = chest_check(0x05, 0x0A)

        checks["Water Temple GS Behind Gate"] = skulltula_check(0x05, 0x0)
        checks["Water Temple GS Near Boss Key Chest"] = skulltula_check(0x05, 0x3)
        checks["Water Temple GS Central Pillar"] = skulltula_check(0x05, 0x2)
        checks["Water Temple GS Falling Platform Room"] = skulltula_check(0x05, 0x1)
        checks["Water Temple GS River"] = skulltula_check(0x05, 0x4)
    else
        checks["Water Temple MQ Longshot Chest"] = chest_check(0x5, 0x0)
        checks["Water Temple MQ Map Chest"] = chest_check(0x5, 0x2)
        checks["Water Temple MQ Compass Chest"] = chest_check(0x5, 0x1)
        checks["Water Temple MQ Central Pillar Chest"] = chest_check(0x5, 0x6)
        checks["Water Temple MQ Boss Key Chest"] = chest_check(0x5, 0x5)
        checks["Water Temple MQ Freestanding Key"] = on_the_ground_check(0x5, 0x1)

        checks["Water Temple MQ GS Lizalfos Hallway"] = skulltula_check(0x5, 0x0)
        checks["Water Temple MQ GS Before Upper Water Switch"] = skulltula_check(0x5, 0x2)
        checks["Water Temple MQ GS River"] = skulltula_check(0x5, 0x1)
        checks["Water Temple MQ GS Freestanding Key Area"] = skulltula_check(0x5, 0x3)
        checks["Water Temple MQ GS Triple Wall Torch"] = skulltula_check(0x5, 0x4)
    end

    checks["Water Temple Morpha Heart"] = boss_item_check(0x16)
    return checks
end

local read_gerudo_valley_checks = function()
    local checks = {}
    checks["GV Crate Freestanding PoH"] = on_the_ground_check(0x5A, 0x2)
    checks["GV Waterfall Freestanding PoH"] = on_the_ground_check(0x5A, 0x1)
    checks["GV Chest"] = chest_check(0x5A, 0x00)
    checks["GV Deku Scrub Grotto Front"] = scrub_sanity_check(0x1A, 0x9)
    checks["GV Deku Scrub Grotto Rear"] = scrub_sanity_check(0x1A, 0x8)
    checks["GV Cow"] = cow_check(0x5A, 0x18)

    checks["GV GS Small Bridge"] = skulltula_check(0x13, 0x1)
    checks["GV GS Bean Patch"] = skulltula_check(0x13, 0x0)
    checks["GV GS Behind Tent"] = skulltula_check(0x13, 0x3)
    checks["GV GS Pillar"] = skulltula_check(0x13, 0x2)
    return checks
end

local read_gerudo_fortress_checks = function()
    local checks = {}
    checks["Hideout 1 Torch Jail Gerudo Key"] = on_the_ground_check(0xC, 0xC)
    checks["Hideout 2 Torches Jail Gerudo Key"] = on_the_ground_check(0xC, 0xF)
    checks["Hideout 3 Torches Jail Gerudo Key"] = on_the_ground_check(0xC, 0xA)
    checks["Hideout 4 Torches Jail Gerudo Key"] = on_the_ground_check(0xC, 0xE)
    checks["Hideout Gerudo Membership Card"] = membership_card_check(0xC, 0x2)
    checks["GF Chest"] = chest_check(0x5D, 0x0)
    checks["GF HBA 1000 Points"] = info_table_check(0x33, 0x0)
    checks["GF HBA 1500 Points"] = item_get_info_check(0x0, 0x7)
    checks["GF GS Top Floor"] = skulltula_check(0x14, 0x1)
    checks["GF GS Archery Range"] = skulltula_check(0x14, 0x0)
    return checks
end

local read_gerudo_training_ground_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0xB) then
        checks["Gerudo Training Ground Lobby Left Chest"] = chest_check(0x0B, 0x13)
        checks["Gerudo Training Ground Lobby Right Chest"] = chest_check(0x0B, 0x07)
        checks["Gerudo Training Ground Stalfos Chest"] = chest_check(0x0B, 0x00)
        checks["Gerudo Training Ground Before Heavy Block Chest"] = chest_check(0x0B, 0x11)
        checks["Gerudo Training Ground Heavy Block First Chest"] = chest_check(0x0B, 0x0F)
        checks["Gerudo Training Ground Heavy Block Second Chest"] = chest_check(0x0B, 0x0E)
        checks["Gerudo Training Ground Heavy Block Third Chest"] = chest_check(0x0B, 0x14)
        checks["Gerudo Training Ground Heavy Block Fourth Chest"] = chest_check(0x0B, 0x02)
        checks["Gerudo Training Ground Eye Statue Chest"] = chest_check(0x0B, 0x03)
        checks["Gerudo Training Ground Near Scarecrow Chest"] = chest_check(0x0B, 0x04)
        checks["Gerudo Training Ground Hammer Room Clear Chest"] = chest_check(0x0B, 0x12)
        checks["Gerudo Training Ground Hammer Room Switch Chest"] = chest_check(0x0B, 0x10)
        checks["Gerudo Training Ground Freestanding Key"] = on_the_ground_check(0x0B, 0x1)
        checks["Gerudo Training Ground Maze Right Central Chest"] = chest_check(0x0B, 0x05)
        checks["Gerudo Training Ground Maze Right Side Chest"] = chest_check(0x0B, 0x08)
        checks["Gerudo Training Ground Underwater Silver Rupee Chest"] = chest_check(0x0B, 0x0D)
        checks["Gerudo Training Ground Beamos Chest"] = chest_check(0x0B, 0x01)
        checks["Gerudo Training Ground Hidden Ceiling Chest"] = chest_check(0x0B, 0x0B)
        checks["Gerudo Training Ground Maze Path First Chest"] = chest_check(0x0B, 0x06)
        checks["Gerudo Training Ground Maze Path Second Chest"] = chest_check(0x0B, 0x0A)
        checks["Gerudo Training Ground Maze Path Third Chest"] = chest_check(0x0B, 0x09)
        checks["Gerudo Training Ground Maze Path Final Chest"] = chest_check(0x0B, 0x0C)
    else
        checks["Gerudo Training Ground MQ Lobby Left Chest"] = chest_check(0xB, 0x13)
        checks["Gerudo Training Ground MQ Lobby Right Chest"] = chest_check(0xB, 0x7)
        checks["Gerudo Training Ground MQ First Iron Knuckle Chest"] = chest_check(0xB, 0x0)
        checks["Gerudo Training Ground MQ Before Heavy Block Chest"] = chest_check(0xB, 0x11)
        checks["Gerudo Training Ground MQ Heavy Block Chest"] = chest_check(0xB, 0x2)
        checks["Gerudo Training Ground MQ Eye Statue Chest"] = chest_check(0xB, 0x3)
        checks["Gerudo Training Ground MQ Ice Arrows Chest"] = chest_check(0xB, 0x4)
        checks["Gerudo Training Ground MQ Second Iron Knuckle Chest"] = chest_check(0xB, 0x12)
        checks["Gerudo Training Ground MQ Flame Circle Chest"] = chest_check(0xB, 0xE)
        checks["Gerudo Training Ground MQ Maze Right Central Chest"] = chest_check(0xB, 0x5)
        checks["Gerudo Training Ground MQ Maze Right Side Chest"] = chest_check(0xB, 0x8)
        checks["Gerudo Training Ground MQ Underwater Silver Rupee Chest"] = chest_check(0xB, 0xD)
        checks["Gerudo Training Ground MQ Dinolfos Chest"] = chest_check(0xB, 0x1)
        checks["Gerudo Training Ground MQ Hidden Ceiling Chest"] = chest_check(0xB, 0xB)
        checks["Gerudo Training Ground MQ Maze Path First Chest"] = chest_check(0xB, 0x6)
        checks["Gerudo Training Ground MQ Maze Path Third Chest"] = chest_check(0xB, 0x9)
        checks["Gerudo Training Ground MQ Maze Path Second Chest"] = chest_check(0xB, 0xA)
    end
    return checks
end

local read_haunted_wasteland_checks = function()
    local checks = {}
    checks["Wasteland Bombchu Salesman"] = salesman_check(0x5E, 0x01)
    checks["Wasteland Chest"] = chest_check(0x5E, 0x00)
    checks["Wasteland GS"] = skulltula_check(0x15, 0x1)
    return checks
end

local read_desert_colossus_checks = function()
    local checks = {}
    checks["Colossus Great Fairy Reward"] = item_get_info_check(0x2, 0x2)
    checks["Colossus Freestanding PoH"] = on_the_ground_check(0x5C, 0xD)
    checks["Colossus Deku Scrub Grotto Front"] = scrub_sanity_check(0x27, 0x9)
    checks["Colossus Deku Scrub Grotto Rear"] = scrub_sanity_check(0x27, 0x8)

    checks["Colossus GS Bean Patch"] = skulltula_check(0x15, 0x0)
    checks["Colossus GS Tree"] = skulltula_check(0x15, 0x3)
    checks["Colossus GS Hill"] = skulltula_check(0x15, 0x2)
    return checks
end

local read_spirit_temple_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0x6) then
        checks["Spirit Temple Child Bridge Chest"] = chest_check(0x06, 0x08)
        checks["Spirit Temple Child Early Torches Chest"] = chest_check(0x06, 0x00)
        checks["Spirit Temple Child Climb North Chest"] = chest_check(0x06, 0x06)
        checks["Spirit Temple Child Climb East Chest"] = chest_check(0x06, 0x0C)
        checks["Spirit Temple Map Chest"] = chest_check(0x06, 0x03)
        checks["Spirit Temple Sun Block Room Chest"] = chest_check(0x06, 0x01)
        checks["Spirit Temple Silver Gauntlets Chest"] = chest_check(0x5C, 0x0B)

        checks["Spirit Temple Compass Chest"] = chest_check(0x06, 0x04)
        checks["Spirit Temple Early Adult Right Chest"] = chest_check(0x06, 0x07)
        checks["Spirit Temple First Mirror Left Chest"] = chest_check(0x06, 0x0D)
        checks["Spirit Temple First Mirror Right Chest"] = chest_check(0x06, 0x0E)
        checks["Spirit Temple Statue Room Northeast Chest"] = chest_check(0x06, 0x0F)
        checks["Spirit Temple Statue Room Hand Chest"] = chest_check(0x06, 0x02)
        checks["Spirit Temple Near Four Armos Chest"] = chest_check(0x06, 0x05)
        checks["Spirit Temple Hallway Right Invisible Chest"] = chest_check(0x06, 0x14)
        checks["Spirit Temple Hallway Left Invisible Chest"] = chest_check(0x06, 0x15)
        checks["Spirit Temple Mirror Shield Chest"] = chest_check(0x5C, 0x09)

        checks["Spirit Temple Boss Key Chest"] = chest_check(0x06, 0x0A)
        checks["Spirit Temple Topmost Chest"] = chest_check(0x06, 0x12)

        checks["Spirit Temple GS Metal Fence"] = skulltula_check(0x06, 0x4)
        checks["Spirit Temple GS Sun on Floor Room"] = skulltula_check(0x06, 0x3)
        checks["Spirit Temple GS Hall After Sun Block Room"] = skulltula_check(0x06, 0x0)
        checks["Spirit Temple GS Lobby"] = skulltula_check(0x06, 0x2)
        checks["Spirit Temple GS Boulder Room"] = skulltula_check(0x06, 0x1)
    else
        checks["Spirit Temple MQ Entrance Front Left Chest"] = chest_check(0x6, 0x1A)
        checks["Spirit Temple MQ Entrance Back Right Chest"] = chest_check(0x6, 0x1F)
        checks["Spirit Temple MQ Entrance Front Right Chest"] = chest_check(0x6, 0x1B)
        checks["Spirit Temple MQ Entrance Back Left Chest"] = chest_check(0x6, 0x1E)
        checks["Spirit Temple MQ Map Chest"] = chest_check(0x6, 0x0)
        checks["Spirit Temple MQ Map Room Enemy Chest"] = chest_check(0x6, 0x8)
        checks["Spirit Temple MQ Child Climb North Chest"] = chest_check(0x6, 0x6)
        checks["Spirit Temple MQ Child Climb South Chest"] = chest_check(0x6, 0xC)
        checks["Spirit Temple MQ Compass Chest"] = chest_check(0x6, 0x3)
        checks["Spirit Temple MQ Silver Block Hallway Chest"] = chest_check(0x6, 0x1C)
        checks["Spirit Temple MQ Sun Block Room Chest"] = chest_check(0x6, 0x1)
        checks["Spirit Temple Silver Gauntlets Chest"] = chest_check(0x5C, 0xB)

        checks["Spirit Temple MQ Child Hammer Switch Chest"] = chest_check(0x6, 0x1D)
        checks["Spirit Temple MQ Statue Room Lullaby Chest"] = chest_check(0x6, 0xF)
        checks["Spirit Temple MQ Statue Room Invisible Chest"] = chest_check(0x6, 0x2)
        checks["Spirit Temple MQ Leever Room Chest"] = chest_check(0x6, 0x4)
        checks["Spirit Temple MQ Symphony Room Chest"] = chest_check(0x6, 0x7)
        checks["Spirit Temple MQ Beamos Room Chest"] = chest_check(0x6, 0x19)
        checks["Spirit Temple MQ Chest Switch Chest"] = chest_check(0x6, 0x18)
        checks["Spirit Temple MQ Boss Key Chest"] = chest_check(0x6, 0x5)
        checks["Spirit Temple Mirror Shield Chest"] = chest_check(0x5C, 0x9)
        checks["Spirit Temple MQ Mirror Puzzle Invisible Chest"] = chest_check(0x6, 0x12)

        checks["Spirit Temple MQ GS Sun Block Room"] = skulltula_check(0x6, 0x0)
        checks["Spirit Temple MQ GS Leever Room"] = skulltula_check(0x6, 0x1)
        checks["Spirit Temple MQ GS Symphony Room"] = skulltula_check(0x6, 0x3)
        checks["Spirit Temple MQ GS Nine Thrones Room West"] = skulltula_check(0x6, 0x2)
        checks["Spirit Temple MQ GS Nine Thrones Room North"] = skulltula_check(0x6, 0x4)
    end

    checks["Spirit Temple Twinrova Heart"] = boss_item_check(0x17)
    return checks
end

local read_ganons_castle_checks = function(mq_table_address)
    local checks = {}
    if not is_master_quest_dungeon(mq_table_address, 0xD) then
        checks["Ganons Castle Forest Trial Chest"] = chest_check(0x0D, 0x09)
        checks["Ganons Castle Water Trial Left Chest"] = chest_check(0x0D, 0x07)
        checks["Ganons Castle Water Trial Right Chest"] = chest_check(0x0D, 0x06)
        checks["Ganons Castle Shadow Trial Front Chest"] = chest_check(0x0D, 0x08)
        checks["Ganons Castle Shadow Trial Golden Gauntlets Chest"] = chest_check(0x0D, 0x05)
        checks["Ganons Castle Light Trial First Left Chest"] = chest_check(0x0D, 0x0C)
        checks["Ganons Castle Light Trial Second Left Chest"] = chest_check(0x0D, 0x0B)
        checks["Ganons Castle Light Trial Third Left Chest"] = chest_check(0x0D, 0x0D)
        checks["Ganons Castle Light Trial First Right Chest"] = chest_check(0x0D, 0x0E)
        checks["Ganons Castle Light Trial Second Right Chest"] = chest_check(0x0D, 0x0A)
        checks["Ganons Castle Light Trial Third Right Chest"] = chest_check(0x0D, 0x0F)
        checks["Ganons Castle Light Trial Invisible Enemies Chest"] = chest_check(0x0D, 0x10)
        checks["Ganons Castle Light Trial Lullaby Chest"] = chest_check(0x0D, 0x11)
        checks["Ganons Castle Spirit Trial Crystal Switch Chest"] = chest_check(0x0D, 0x12)
        checks["Ganons Castle Spirit Trial Invisible Chest"] = chest_check(0x0D, 0x14)

        checks["Ganons Castle Deku Scrub Left"] = scrub_sanity_check(0xD, 0x9)
        checks["Ganons Castle Deku Scrub Center-Left"] = scrub_sanity_check(0xD, 0x6)
        checks["Ganons Castle Deku Scrub Center-Right"] = scrub_sanity_check(0xD, 0x4)
        checks["Ganons Castle Deku Scrub Right"] = scrub_sanity_check(0xD, 0x8)
    else
        checks["Ganons Castle MQ Forest Trial Freestanding Key"] = on_the_ground_check(0xD, 0x1)
        checks["Ganons Castle MQ Forest Trial Eye Switch Chest"] = chest_check(0xD, 0x2)
        checks["Ganons Castle MQ Forest Trial Frozen Eye Switch Chest"] = chest_check(0xD, 0x3)
        checks["Ganons Castle MQ Water Trial Chest"] = chest_check(0xD, 0x1)
        checks["Ganons Castle MQ Shadow Trial Bomb Flower Chest"] = chest_check(0xD, 0x0)
        checks["Ganons Castle MQ Shadow Trial Eye Switch Chest"] = chest_check(0xD, 0x5)
        checks["Ganons Castle MQ Light Trial Lullaby Chest"] = chest_check(0xD, 0x4)
        checks["Ganons Castle MQ Spirit Trial First Chest"] = chest_check(0xD, 0xA)
        checks["Ganons Castle MQ Spirit Trial Invisible Chest"] = chest_check(0xD, 0x14)
        checks["Ganons Castle MQ Spirit Trial Sun Front Left Chest"] = chest_check(0xD, 0x9)
        checks["Ganons Castle MQ Spirit Trial Sun Back Left Chest"] = chest_check(0xD, 0x8)
        checks["Ganons Castle MQ Spirit Trial Sun Back Right Chest"] = chest_check(0xD, 0x7)
        checks["Ganons Castle MQ Spirit Trial Golden Gauntlets Chest"] = chest_check(0xD, 0x6)

        checks["Ganons Castle MQ Deku Scrub Left"] = scrub_sanity_check(0xD, 0x9)
        checks["Ganons Castle MQ Deku Scrub Center-Left"] = scrub_sanity_check(0xD, 0x6)
        checks["Ganons Castle MQ Deku Scrub Center"] = scrub_sanity_check(0xD, 0x4)
        checks["Ganons Castle MQ Deku Scrub Center-Right"] = scrub_sanity_check(0xD, 0x8)
        checks["Ganons Castle MQ Deku Scrub Right"] = scrub_sanity_check(0xD, 0x1)
    end

    checks["Ganons Tower Boss Key Chest"] = chest_check(0x0A, 0x0B)
    return checks
end

local read_outside_ganons_castle_checks = function()
    local checks = {}
    checks["OGC Great Fairy Reward"] = great_fairy_magic_check(0x3B, 0x8)
    checks["OGC GS"] = skulltula_check(0x0E, 0x0)
    return checks
end

local read_song_checks = function()
    local checks = {}
    checks["Song from Impa"] = event_check(0x5, 0x9) -- Zelda's Lullaby
    checks["Song from Malon"] = event_check(0x5, 0x8) -- Epona's Song
    checks["Song from Saria"] = event_check(0x5, 0x7) -- Saria's Song
    checks["Song from Royal Familys Tomb"] = event_check(0x5, 0xA) -- Sun's Song
    checks["Song from Ocarina of Time"] = event_check(0xA, 0x9) -- Song of Time
    checks["Song from Windmill"] = event_check(0x5, 0xB) -- Song of Storms
    checks["Sheik in Forest"] = event_check(0x5, 0x0) -- Minuet of Forest
    checks["Sheik in Crater"] = event_check(0x5, 0x1) -- Bolero of Fire
    checks["Sheik in Ice Cavern"] = event_check(0x5, 0x2) -- Serenade of Water
    checks["Sheik at Colossus"] = event_check(0xA, 0xC) -- Requiem of Spirit
    checks["Sheik in Kakariko"] = event_check(0x5, 0x4) -- Nocturne of Shadows
    checks["Sheik at Temple"] = event_check(0x5, 0x5) -- Prelude of Light
    return checks
end

local check_all_locations = function(mq_table_address)
-- TODO: make MQ better
    local location_checks = {}
    temp_context = mainmemory.readbyterange(0x40002C, 4)
    for k,v in pairs(read_kokiri_forest_checks()) do location_checks[k] = v end
    for k,v in pairs(read_lost_woods_checks()) do location_checks[k] = v end
    for k,v in pairs(read_sacred_forest_meadow_checks()) do location_checks[k] = v end
    for k,v in pairs(read_deku_tree_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_forest_temple_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_hyrule_field_checks()) do location_checks[k] = v end
    for k,v in pairs(read_lon_lon_ranch_checks()) do location_checks[k] = v end
    for k,v in pairs(read_market_checks()) do location_checks[k] = v end
    for k,v in pairs(read_hyrule_castle_checks()) do location_checks[k] = v end
    for k,v in pairs(read_kakariko_village_checks()) do location_checks[k] = v end
    for k,v in pairs(read_graveyard_checks()) do location_checks[k] = v end
    for k,v in pairs(read_bottom_of_the_well_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_shadow_temple_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_death_mountain_trail_checks()) do location_checks[k] = v end
    for k,v in pairs(read_goron_city_checks()) do location_checks[k] = v end
    for k,v in pairs(read_death_mountain_crater_checks()) do location_checks[k] = v end
    for k,v in pairs(read_dodongos_cavern_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_fire_temple_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_zoras_river_checks()) do location_checks[k] = v end
    for k,v in pairs(read_zoras_domain_checks()) do location_checks[k] = v end
    for k,v in pairs(read_zoras_fountain_checks()) do location_checks[k] = v end
    for k,v in pairs(read_jabu_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_ice_cavern_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_lake_hylia_checks()) do location_checks[k] = v end
    for k,v in pairs(read_water_temple_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_gerudo_valley_checks()) do location_checks[k] = v end
    for k,v in pairs(read_gerudo_fortress_checks()) do location_checks[k] = v end
    for k,v in pairs(read_gerudo_training_ground_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_haunted_wasteland_checks()) do location_checks[k] = v end
    for k,v in pairs(read_desert_colossus_checks()) do location_checks[k] = v end
    for k,v in pairs(read_spirit_temple_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_ganons_castle_checks(mq_table_address)) do location_checks[k] = v end
    for k,v in pairs(read_outside_ganons_castle_checks()) do location_checks[k] = v end
    for k,v in pairs(read_song_checks()) do location_checks[k] = v end
    -- write 0 to temp context values
    mainmemory.write_u32_be(0x40002C, 0)
    mainmemory.write_u32_be(0x400030, 0)
    return location_checks
end

local check_collectibles = function()
    local retval = {}
    if collectible_offsets ~= nil then
        for id, data in pairs(collectible_offsets) do
            local mem = mainmemory.readbyte(collectible_overrides + data[1] + bit.rshift(data[2], 3))
            retval[id] = bit.check(mem, data[2] % 8)
        end
    end
    return retval
end

-- convenience functions

-- invert a table (assumes values are unique)
local function invert_table(t)
    local inverted = {}
    for key,val in pairs(t) do
        inverted[val] = key
    end
    return inverted
end

-- a Layout describes how a section of memory is laid out
-- getting a specific data type should return its value,
-- getting a rescursive structure will return the structure with the layout (this is the default behavior)
local Layout = {
    rawget = function(pointer) return pointer.get(pointer) end,
    get = function(pointer) return pointer end,
    set = function(pointer, value) end
}
function Layout:create (l)
    setmetatable(l, self)
    self.__index = self
    return l
end

-- a Layout_Entry gives an offset within the Layout and, recursively, a Layout of memory at that offset
local function Layout_Entry(offset, layout)
    return { offset = offset, layout = layout }
end

local e = Layout_Entry

-- Pointer holds an absolute offset, and has a Layout as its type
local Pointer = {}
function Pointer:new (offset, layout)
    local p = { offset = offset, layout = layout }
    setmetatable(p, Pointer)
    return p
end
function Pointer:cast(layout)
    return Pointer:new(self.offset, layout)
end
function Pointer:rawget(key)
    if not self.layout[key] then
        return self.layout.rawget(self)
    end
    -- get the struct at this entry
    local inner = self.layout[key]
    -- update get the new offset and layout
    local offset = self.offset + inner.offset
    local layout = inner.layout
    -- create a new pointer
    return Pointer:new(offset, layout)
end
function Pointer:get() return self.layout.get(self) end
function Pointer:set(value) return self.layout.set(self, value) end
function Pointer.__index(pointer, key)
    if Pointer[key] then
        return Pointer[key]
    end
    -- get the pointer
    local p = pointer:rawget(key)
    -- resolve the pointer (if the layout is not concrete, it resolves to itself)
    return p:get()
end
function Pointer.__newindex(pointer, key, value)
    -- get the pointer
    local p = pointer:rawget(key)
    -- resolve the pointer (if the layout is not concrete, it resolves to itself)
    p:set(value)
end

-- CONCRETE TYPES

-- Int has a width in bytes to read
local function Int(width)
    local obj = Layout:create {}

    local gets = {
        [1] = function(p)return mainmemory.read_u8(p.offset) end,
        [2] = function(p) return mainmemory.read_u16_be(p.offset) end,
        [3] = function(p) return mainmemory.read_u24_be(p.offset) end,
        [4] = function(p) return mainmemory.read_u32_be(p.offset) end,
    }
    obj.get = gets[width]

    local sets = {
        [1] = function(p, value) mainmemory.write_u8(p.offset, value) end,
        [2] = function(p, value) mainmemory.write_u16_be(p.offset, value) end,
        [3] = function(p, value) mainmemory.write_u24_be(p.offset, value) end,
        [4] = function(p, value) mainmemory.write_u32_be(p.offset, value) end,
    }
    obj.set = sets[width]

    return obj
end

-- alias for types to save space by not creating them multiple times
local Int_8 = Int(1)
local Int_16 = Int(2)
local Int_24 = Int(3)
local Int_32 = Int(4)

-- Bit is a single flag at an address
-- values passed in and returned are booleans
local function Bit(pos)
    local obj = Layout:create {}

    function obj.get(p)
        return bit.check(mainmemory.read_u8(p.offset), pos)
    end

    function obj.set(p, value)
        local orig = mainmemory.readbyte(p.offset)
        local changed
        if value then
            changed = bit.set(orig, pos)
        else
            changed = bit.clear(orig, pos)
        end
        mainmemory.writebyte(p.offset, changed)
    end

    return obj
end

-- Bits is an int that is some mask of bits at the address
-- the range of bit positions is inclusive
local function Bits(start, ending)
    local obj = Layout:create {}

    local mask = 0x00
    for b = start, ending do
        mask = bit.set(mask, b)
    end

    function obj.get(p)
        return bit.rshift( bit.band(mainmemory.read_u8(p.offset), mask), start )
    end

    function obj.set(p, value)
        local orig = mainmemory.readbyte(p.offset)
        orig = bit.band( orig, bit.bnot(mask) )
        mainmemory.writebyte(p.offset, bit.bor(bit.lshift(value, start), orig) )
    end

    return obj
end

local function Value_Named_Layout(layout, lookup)
    local obj = Layout:create {}

    obj.lookup = lookup

    function obj.get(p)
        local value = layout.get(p)
        if lookup[value] then
            value = lookup[value]
        end
        return value
    end

    function obj.rawget(p)
        return layout.get(p)
    end

    local inverse_lookup = invert_table(lookup)

    function obj.set(p, value)
        if type(value) == "string" then
            if inverse_lookup[value] then
                value = inverse_lookup[value]
            else
                return
            end
        end
        layout.set(p, value)
    end

    return obj
end

-- RECURSIVE TYPES

-- holds a list of layouts of a given type, that can be indexed into
-- the Array can be given a list of names for each key to be used as an alternative lookup
local function Array(width, layout, keys)
    local obj = Layout:create {}

    obj.keys = keys

    setmetatable(obj, {
        __index = function(array, key)
            -- allows us to still call get and set
            if Layout[key] then
                return Layout[key]
            end
            -- compute the offset from the start of the array
            if type(key) == "string" then
                if keys[key] then
                    key = keys[key]
                else
                    key = 0
                end
            end
            local offset = key * width
            -- since this is a layout, we are expected to return a layout entry
            return Layout_Entry( offset, layout )
        end
    })

    return obj
end

-- holds a list of bit flags
-- the Bit_Array can be given a list of names for each key to be used as an alternative lookup
local function Bit_Array(bytes, keys)
    local obj = Layout:create {}

    obj.keys = keys

    setmetatable(obj, {
        __index = function(array, key)
            -- allows us to still call get and set
            if Layout[key] then
                return Layout[key]
            end
            -- compute the offset from the start of the array
            if type(key) == "string" then
                if keys[key] then
                    key = keys[key]
                else
                    key = 0
                end
            end
            local byte = bytes - math.floor(key / 8) - 1
            local bit = key % 8
            -- since this is a layout, we are expected to return a layout entry
            return Layout_Entry( byte, Bit(bit) )
        end
    })

    return obj
end

-- a pointer to a specific location in memory
local function Address(layout)
    local obj = Layout:create {}

    function obj.get(p)
        -- get the address
        local address = Int_32.get(p)
        address = bit.band(address, 0x00FFFFFF)
        -- return "Null" for address 0
        if address == 0 then
            return "Null"
        end
        -- create a pointer to it
        return Pointer:new( address, layout )
    end

    function obj.set(p, value)
        -- Null a pointer
        if value == "Null" then
            Int_32.set(p, 0)
            return
        end
        -- assume this is a Pointer
        if type(value) == "table" then
            value = value.offset
        end
        -- create address
        local address =  bit.bor(value, 0x80000000)
        Int_32.set(p, address)
    end

    return obj
end

-- OOT Structs

local scene_names = {
    deku_tree = 0x00,
    dodongos_cavern = 0x01,
    jabu_jabus_belly = 0x02,
    forest_temple = 0x03,
    fire_temple = 0x04,
    water_temple = 0x05,
    spirit_temple = 0x06,
    shadow_temple = 0x07,
    bottom_of_the_well = 0x08,
    ice_cavern = 0x09,
    ganons_tower = 0x0A,
    gerudo_training_ground = 0x0B,
    thieves_hideout = 0x0C,
    inside_ganons_castle = 0x0D,
    treasure_box_shop = 0x10,
}

local Global_Context = Layout:create {
    cur_scene =   Layout_Entry( 0x00A4, Value_Named_Layout(Int_16, invert_table(scene_names)) ),

    actor_table = Layout_Entry( 0x1C30, Array( 0x8, Actor_Table_Entry, actor_category ) ),

    switch_flags =      Layout_Entry( 0x1D28, Bit_Array( 0x4 ) ),
    temp_switch_flags = Layout_Entry( 0x1D2C, Bit_Array( 0x4 ) ),
    chest_flags =       Layout_Entry( 0x1D38, Bit_Array( 0x4 ) ),
    room_clear_flags =  Layout_Entry( 0x1D3C, Bit_Array( 0x4 ) ),
}

local Save_Context = Layout:create {
    time =                   Layout_Entry( 0x000C, Int_16 ),
    max_health =             Layout_Entry( 0x002E, Int_16 ),
    cur_health =             Layout_Entry( 0x0030, Int_16 ),
    magic_meter_level =      Layout_Entry( 0x0032, Int_8 ),
    cur_magic =              Layout_Entry( 0x0033, Int_8 ),
    rupees =                 Layout_Entry( 0x0034, Int_16 ),
    have_magic =             Layout_Entry( 0x003A, Bit(0) ),
    have_double_magic =      Layout_Entry( 0x003C, Bit(0) ),
    double_defense =         Layout_Entry( 0x003D, Bit(0) ),
    biggoron_sword_durable = Layout_Entry( 0x003E, Bit(0) ),

    stored_child_equips = Layout_Entry( 0x0040, Equips ),
    stored_adult_equips = Layout_Entry( 0x004A, Equips ),
    current_equips =      Layout_Entry( 0x0068, Equips ),

    inventory = Layout_Entry( 0x0074, Array( 1, Item, item_slot_names ) ),
    ammo =      Layout_Entry( 0x008C, Array( 1, Int_8, item_slot_names ) ),

    beans_purchased = Layout_Entry( 0x009B, Int_8 ),

    equipment =    Layout_Entry( 0x009C, Equipment ),
    heart_pieces = Layout_Entry( 0x00A4, Bits(4,5) ),
    quest_status = Layout_Entry( 0x00A5, Bit_Array( 0x3, quest_status_names ) ),

    dungeon_items = Layout_Entry( 0x00A8, Array( 0x1, Dungeon_Item, scene_names ) ),
    small_keys =    Layout_Entry( 0x00BC, Array( 0x1, Int_8, scene_names ) ),

    double_defense_hearts = Layout_Entry( 0x00CF, Int_8 ),
    gold_skulltulas =       Layout_Entry( 0x00D0, Int_16 ),

    scene_flags = Layout_Entry( 0x00D4, Array( 0x1C, Scene_Flags_Type, scene_names ) ),

    skulltula_flags = Layout_Entry( 0xE9C, Array( 0x1, Bit_Array( 0x1 ) ) ),

    events = Layout_Entry( 0xED4, Array( 0x2, Bit_Array( 0x2 ) ) ),

    magic_meter_size = Layout_Entry( 0x13F4, Int_16 ),

    -- ex: oot.sav.triforce_pieces = 0x01 - doesn't seem to work with decimal vals
    triforce_pieces = Layout_Entry( 0xD4 + 0x1C * 0x48 + 0x10, Int_32)

}

local save_context = Pointer:new( 0x11A5D0, Save_Context )
local global_context = Pointer:new( 0x1C84A0, Global_Context )


local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local ootSocket = nil
local frame = 0

-- Various useful values
local rando_context = mainmemory.read_u32_be(0x1C6E90 + 0x15D4) - 0x80000000
local coop_context = mainmemory.read_u32_be(rando_context + 0x0000) - 0x80000000

local player_id_addr        = coop_context + 4

local incoming_player_addr  = coop_context + 6
local incoming_item_addr    = coop_context + 8

local outgoing_key_addr     = coop_context + 12
local outgoing_item_addr    = coop_context + 16
local outgoing_player_addr  = coop_context + 18

local player_names_address  = coop_context + 20
local player_name_length    = 8 -- 8 bytes
local rom_name_location     = player_names_address + 0x800 + 0x5 -- 0x800 player names, 0x5 CFG_FILE_SELECT_HASH

-- TODO: load dynamically from slot data
local master_quest_table_address = rando_context + (mainmemory.read_u32_be(rando_context + 0x0E9F) - 0x03480000)

local save_context_addr = 0x11A5D0
local internal_count_addr = save_context_addr + 0x90
local item_queue = {}

local first_connect = true
local game_complete = false

NUM_BIG_POES_REQUIRED = mainmemory.read_u8(rando_context + 0x0EAD)

local bytes_to_string = function(bytes)
    local string = ''
    for i=0,#(bytes) do
        if bytes[i] == 0 then return string end
        string = string .. string.char(bytes[i])
    end
    return string
end

-- ROM reading and writing functions

-- Reading game state
local state_main = Pointer:new( 0x11B92F, Int(1) )
local state_sub = Pointer:new( 0x11B933, Int(1) )
local state_menu = Pointer:new( 0x1D8DD5, Int(1) )
local state_logo = Pointer:new( 0x11F200, Int(4) )
local state_link = Pointer:new( 0x1DB09C, Bit_Array( 0x8, {dying=0x27} ) )
local state_fairy_queued = Pointer:new( 0x1DB26F, Bit(0) )


local game_modes = {
    [-1]={name="Unknown", loaded=false},
    [0]={name="N64 Logo", loaded=false},
    [1]={name="Title Screen", loaded=false},
    [2]={name="File Select", loaded=false},
    [3]={name="Normal Gameplay", loaded=true},
    [4]={name="Cutscene", loaded=true},
    [5]={name="Paused", loaded=true},
    [6]={name="Dying", loaded=true},
    [7]={name="Dying Menu Start", loaded=false},
    [8]={name="Dead", loaded=false},
}

local function get_current_game_mode()
    local mode = -1
    local logo_state = state_logo:get()
    if logo_state == 0x802C5880 or logo_state == 0x00000000 then
        mode = 0
    else
        if state_main:get() == 1 then
            mode = 1
        elseif state_main:get() == 2 then
            mode = 2
        else
            local menu_state = state_menu:get()
            if menu_state == 0 then
                if state_link.dying or save_context.cur_health <= 0 then
                    mode = 6
                else
                    if state_sub:get() == 4 then
                        mode = 4
                    else
                        mode = 3
                    end
                end
            elseif (0 < menu_state and menu_state < 9) or menu_state == 13 then
                mode = 5
            elseif menu_state == 9 or menu_state == 0xB then
                mode = 7
            else
                mode = 8
            end
        end
    end
    return mode, game_modes[mode]
end

function InSafeState()
    return game_modes[get_current_game_mode()].loaded
end

function item_receivable()
    local shop_scenes = {[0x2C]=1, [0x2D]=1, [0x2E]=1, [0x2F]=1, [0x30]=1, [0x31]=1, [0x32]=1, [0x33]=1,
                         [0x42]=1, [0x4B]=1}
    local details
    local scene
    _, details = get_current_game_mode()
    scene = global_context:rawget('cur_scene'):rawget()

    local playerQueued = mainmemory.read_u16_be(incoming_player_addr)
    local itemQueued = mainmemory.read_u16_be(incoming_item_addr)

    -- Safe to receive an item if the scene is normal, player is not in a shop, and no item is already queued
    return details.name == "Normal Gameplay" and shop_scenes[scene] == nil and playerQueued == 0 and itemQueued == 0
end

function get_player_name()
    local rom_name_bytes = mainmemory.readbyterange(rom_name_location, 16)
    return bytes_to_string(rom_name_bytes)
end

function setPlayerName(id, name)
    local name_address = player_names_address + (id * player_name_length)
    local name_index = 0

    for _,c in pairs({string.byte(name, 1, 100)}) do
        if c >= string.byte('0') and c <= string.byte('9') then
            c = c - string.byte('0')
        elseif c >= string.byte('A') and c <= string.byte('Z') then
            c = c + 0x6A
        elseif c >= string.byte('a') and c <= string.byte('z') then
            c = c + 0x64
        elseif c == string.byte('.') then
            c = 0xEA
        elseif c == string.byte('-') then
            c = 0xE4
        elseif c == string.byte(' ') then
            c = 0xDF
        else
            c = nil
        end

        if c ~= nil then
            mainmemory.write_u8(name_address + name_index, c)

            name_index = name_index + 1
            if name_index >= 8 then
                break
            end
        end
    end

    for i = name_index, player_name_length - 1 do
        mainmemory.write_u8(name_address + i, 0xDF)
    end
end

function is_game_complete()
    -- If the game is complete, do not read memory
    if game_complete then return true end

    -- contains a pointer to the current scene
    local scene_pointer = mainmemory.read_u32_be(0x1CA208)

    local triforce_hunt_complete = 0x80383C10 -- pointer credits location set by completed triforce hunt
    local ganon_defeated = 0x80382720 -- pointer to cutscene when ganon is defeated

    -- If the game is complete, set the lib variable and report the game as completed
    if (scene_pointer == triforce_hunt_complete) or (scene_pointer == ganon_defeated) then
        game_complete = true
        return true
    end

    -- Game is still ongoing
    return false
end

function deathlink_enabled()
    local death_link_flag = mainmemory.readbyte(coop_context + 0xB)
    return death_link_flag > 0
end

function get_death_state()
    -- Load the current game mode
    local game_mode = get_current_game_mode()

    -- If the N64 Logo is loaded, Link isn't dead, he just doesn't exist
    if (game_mode == "N64 Logo" or game_mode == "File Select") then return false end

    -- Read Link's current HP value
    local hp_counter = mainmemory.read_u16_be(0x11A600)

    return (hp_counter == 0)
end

function kill_link()
    -- market entrance: 27/28/29
    -- outside ToT: 35/36/37.
    -- if killed on these scenes the game crashes, so we wait until not on this screen.
    local scene = global_context:rawget('cur_scene'):rawget()
    if scene == 27 or scene == 28 or scene == 29 or scene == 35 or scene == 36 or scene == 37 then return end
    mainmemory.write_u16_be(0x11A600, 0)
end

function process_block(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    -- Write player names on first connect or after reset (N64 logo, title screen, file select)
    cur_mode = get_current_game_mode()
    if (first_connect or cur_mode == 0 or cur_mode == 1 or cur_mode == 2) and (#block['playerNames'] > 0) then
        first_connect = false
        local index = 1
        while (index <= #block['playerNames']) and (index < 255) do
            setPlayerName(index, block['playerNames'][index])
            index = index + 1
        end
        setPlayerName(255, 'APPlayer')
    end
    -- Kill Link if needed
    if block['triggerDeath'] then
        kill_link()
    end
    -- Queue item for receiving, if one exists
    item_queue = block['items']
    received_items_count = mainmemory.read_u16_be(internal_count_addr)
    if received_items_count < #item_queue then
        -- There are items to send: remember lua tables are 1-indexed!
        if item_receivable() then
            mainmemory.write_u16_be(incoming_player_addr, 0x00)
            mainmemory.write_u16_be(incoming_item_addr, item_queue[received_items_count+1])
        end
    end
    -- Record collectible data if necessary
    if collectible_overrides == nil and block['collectibleOverrides'] ~= 0 then
        collectible_overrides = mainmemory.read_u32_be(rando_context + block['collectibleOverrides']) - 0x80000000
    end
    if collectible_offsets ~= block['collectibleOffsets'] then
        collectible_offsets = block['collectibleOffsets']
    end
    return
end

-- Main control handling: main loop and socket receive

function receive()
    l, e = ootSocket:receive()
    -- Handle incoming message
    if e == 'closed' then
        if curstate == STATE_OK then
            print("Connection closed")
        end
        curstate = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        print("timeout")
        return
    elseif e ~= nil then
        print(e)
        curstate = STATE_UNINITIALIZED
        return
    end
    process_block(json.decode(l))

    -- Determine message to send back
    local retTable = {}
    retTable["playerName"] = get_player_name()
    retTable["scriptVersion"] = script_version
    retTable["deathlinkActive"] = deathlink_enabled()
    if InSafeState() then
        retTable["locations"] = check_all_locations(master_quest_table_address)
        retTable["collectibles"] = check_collectibles()
        retTable["isDead"] = get_death_state()
        retTable["gameComplete"] = is_game_complete()
    end

    -- Send the message
    msg = json.encode(retTable).."\n"
    local ret, error = ootSocket:send(msg)
    if ret == nil then
        print(error)
    elseif curstate == STATE_INITIAL_CONNECTION_MADE then
        curstate = STATE_TENTATIVELY_CONNECTED
    elseif curstate == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        curstate = STATE_OK
    end

end

function main()
    if not checkBizHawkVersion() then
        return
    end
    server, error = socket.bind('localhost', 28921)

    while true do
        frame = frame + 1
        if not (curstate == prevstate) then
            prevstate = curstate
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 30 == 0) then
                receive()
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            if  (frame % 60 == 0) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    ootSocket = client
                    ootSocket:settimeout(0)
                else
                    print('Connection failed, ensure OoTClient is running and rerun connector_oot.lua')
                    return
                end
            end
        end
        emu.frameadvance()
    end
end

main()
