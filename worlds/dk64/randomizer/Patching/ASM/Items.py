"""Write ASM data for the item elements."""

from randomizer.Enums.Maps import Maps
from randomizer.Enums.Settings import MiscChangesSelected, FasterChecksSelected, ProgressiveHintItem
from randomizer.Enums.Types import Types
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.ASM import *
from randomizer.Patching.Library.Generic import IsDDMSSelected, ReqItems

FAIRY_LOAD_FIX = True


def writeSingleOwnership(ROM_COPY, index, kong):
    """Write the ownership of a particular item to a kong."""
    start = getSym("new_flag_mapping") + (index * 8) + 6
    writeValue(ROM_COPY, start, Overlay.Custom, kong + 2, {}, 1)


def writeKongItemOwnership(ROM_COPY, settings):
    """Write the item ownership for kong rando."""
    starting_kong = settings.starting_kong
    diddy_freer = settings.diddy_freeing_kong
    lanky_freer = settings.lanky_freeing_kong
    tiny_freer = settings.tiny_freeing_kong
    chunky_freer = settings.chunky_freeing_kong
    no_arcade_r1 = IsDDMSSelected(settings.faster_checks_selected, FasterChecksSelected.factory_arcade_round_1)
    writeSingleOwnership(ROM_COPY, 1, diddy_freer)
    writeSingleOwnership(ROM_COPY, 2, diddy_freer)
    writeSingleOwnership(ROM_COPY, 22, tiny_freer)
    writeSingleOwnership(ROM_COPY, 27, lanky_freer)
    writeSingleOwnership(ROM_COPY, 39, chunky_freer)
    writeSingleOwnership(ROM_COPY, 97, starting_kong)
    if no_arcade_r1:
        start = getSym("new_flag_mapping") + (41 * 8)
        writeValue(ROM_COPY, start, Overlay.Custom, Maps.FactoryBaboonBlast, {}, 1)
        writeValue(ROM_COPY, start + 2, Overlay.Custom, 0, {})


def collisionUpdates(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to item collision."""
    # Collision Adjustments
    COLLISION_START = getSym("object_collisions")
    COLLISION_COUNT = getVar("collision_limit")
    COLLISION_SIZE = 0x18

    if settings.free_trade_blueprints:
        for i in range(COLLISION_COUNT):
            obj_i = COLLISION_START + (i * COLLISION_SIZE)
            addr = getROMAddress(obj_i + 2, Overlay.Custom, offset_dict)
            ROM_COPY.seek(addr)
            collectable_type = int.from_bytes(ROM_COPY.readBytes(1), "big")
            if collectable_type == 12:  # Blueprint
                writeValue(ROM_COPY, obj_i + 0xC, Overlay.Custom, 0, offset_dict)
    collision_hi = getHi(COLLISION_START)
    collision_lo = getLo(COLLISION_START)
    writeValue(ROM_COPY, 0x806F48D2, Overlay.Static, collision_hi, offset_dict)
    writeValue(ROM_COPY, 0x806F48D6, Overlay.Static, collision_lo, offset_dict)
    writeValue(ROM_COPY, 0x806F4A8E, Overlay.Static, COLLISION_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x806F4E7E, Overlay.Static, collision_hi, offset_dict)
    writeValue(ROM_COPY, 0x806F4E8E, Overlay.Static, collision_lo, offset_dict)
    writeValue(ROM_COPY, 0x806F51C2, Overlay.Static, getHi(COLLISION_START + 0xC), offset_dict)
    writeValue(ROM_COPY, 0x806F51CE, Overlay.Static, getLo(COLLISION_START + 0xC), offset_dict)
    writeValue(ROM_COPY, 0x806F5556, Overlay.Static, getHi(COLLISION_START + 2), offset_dict)
    writeValue(ROM_COPY, 0x806F5562, Overlay.Static, getLo(COLLISION_START + 2), offset_dict)
    writeValue(ROM_COPY, 0x806F626E, Overlay.Static, collision_hi, offset_dict)
    writeValue(ROM_COPY, 0x806F627A, Overlay.Static, collision_lo, offset_dict)
    writeValue(ROM_COPY, 0x806F6AC6, Overlay.Static, collision_hi, offset_dict)
    writeValue(ROM_COPY, 0x806F6ACE, Overlay.Static, collision_lo, offset_dict)
    writeValue(ROM_COPY, 0x806F742A, Overlay.Static, collision_hi, offset_dict)
    writeValue(ROM_COPY, 0x806F744A, Overlay.Static, collision_lo, offset_dict)
    writeValue(ROM_COPY, 0x806F7996, Overlay.Static, getHi(COLLISION_START + (COLLISION_COUNT * COLLISION_SIZE)), offset_dict)
    writeValue(ROM_COPY, 0x806F799A, Overlay.Static, getLo(COLLISION_START + (COLLISION_COUNT * COLLISION_SIZE)), offset_dict)
    # Change new sizes
    writeValue(ROM_COPY, 0x806F4A92, Overlay.Static, COLLISION_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F4EAA, Overlay.Static, COLLISION_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F51B4, Overlay.Static, 0x240A0000 | COLLISION_SIZE, offset_dict, 4)  # addiu $t2, $zero (sizeof(collision_info))
    writeValue(ROM_COPY, 0x806F51B8, Overlay.Static, 0x01420019, offset_dict, 4)  # multu $t2, $v0
    writeValue(ROM_COPY, 0x806F51BC, Overlay.Static, 0x00004812, offset_dict, 4)  # mflo $t1
    writeValue(ROM_COPY, 0x806F5548, Overlay.Static, 0x240A0000 | COLLISION_SIZE, offset_dict, 4)  # addiu $t2, $zero (sizeof(collision_info))
    writeValue(ROM_COPY, 0x806F554C, Overlay.Static, 0x01420019, offset_dict, 4)  # multu $t2, $v0
    writeValue(ROM_COPY, 0x806F5550, Overlay.Static, 0x00005012, offset_dict, 4)  # mflo $t2
    writeValue(ROM_COPY, 0x806F6282, Overlay.Static, COLLISION_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F6ABE, Overlay.Static, COLLISION_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F799E, Overlay.Static, COLLISION_SIZE, offset_dict)

    # Collision fixes
    QUAD_SIZE = 100
    writeValue(ROM_COPY, 0x806F4ACA, Overlay.Static, QUAD_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F4BF0, Overlay.Static, 0x240A0000 | QUAD_SIZE, offset_dict, 4)  # addiu $t2, $zero, QUAD_SIZE
    writeValue(ROM_COPY, 0x806F4BF4, Overlay.Static, 0x01510019, offset_dict, 4)  # multu $t2, $s1
    writeValue(ROM_COPY, 0x806F4BF8, Overlay.Static, 0x00008812, offset_dict, 4)  # mflo $s1
    writeValue(ROM_COPY, 0x806F4BFC, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x806F4C00, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x806F4C16, Overlay.Static, QUAD_SIZE, offset_dict)
    writeValue(ROM_COPY, 0x806F4C52, Overlay.Static, QUAD_SIZE, offset_dict)

    writeFunction(ROM_COPY, 0x806F502C, Overlay.Static, "getCollisionSquare_New", offset_dict)  # Assigning hitbox to data table
    writeFunction(ROM_COPY, 0x806F5134, Overlay.Static, "getCollisionSquare_New", offset_dict)  # Assigning hitbox to data table
    writeFunction(ROM_COPY, 0x806F6A0C, Overlay.Static, "checkForValidCollision", offset_dict)  # Detecting if object is inside current quadrant
    writeFunction(ROM_COPY, 0x806F6A2C, Overlay.Static, "checkForValidCollision", offset_dict)  # Detecting if object is inside current quadrant


def raceCoinRandoASMChanges(ROM_COPY: LocalROM, settings, offset_dict: dict, spoiler):
    """All changes related to race coin item rando."""
    if settings.race_coin_rando:
        # Prevent wiping the counts
        writeValue(ROM_COPY, 0x80024388, Overlay.Bonus, 0, offset_dict, 4)
        writeValue(ROM_COPY, 0x800243A0, Overlay.Minecart, 0, offset_dict, 4)
        writeValue(ROM_COPY, 0x80025FB8, Overlay.Race, 0, offset_dict, 4)
        writeValue(ROM_COPY, 0x8002ECC8, Overlay.Race, 0, offset_dict, 4)
        # Squawks - Minecarts
        writeValue(ROM_COPY, 0x806C4544, Overlay.Static, 0x116D, offset_dict)  # Change this to checking for intro spawn trigger
        writeValue(ROM_COPY, 0x806C4428, Overlay.Static, 0xAFA40054, offset_dict, 4)  # Change not enough coins cs to be the intro cutscene
        writeValue(ROM_COPY, 0x806C45FE, Overlay.Static, 0x5C, offset_dict)  # Check for intro spawn trigger
        writeValue(ROM_COPY, 0x806C4806, Overlay.Static, 0x5C, offset_dict)  # Check for intro spawn trigger
        writeValue(ROM_COPY, 0x806C48A2, Overlay.Static, 0x5C, offset_dict)  # Check for intro spawn trigger
        writeValue(ROM_COPY, 0x806C48D4, Overlay.Static, 0, offset_dict, 4)  # Ditch the Try Again Prompt
        # Cutscenes
        writeValue(ROM_COPY, 0x806C492E, Overlay.Static, 3, offset_dict)  # Japes Minecart
        writeValue(ROM_COPY, 0x806C4972, Overlay.Static, 9, offset_dict)  # Forest Minecart
        writeValue(ROM_COPY, 0x806C49B6, Overlay.Static, 5, offset_dict)  # Castle Minecart

    # Race Coin Requirements
    race_offset_data = {
        Maps.CavesLankyRace: [0x800247C2],
        Maps.AztecTinyRace: [0x800247DA],
        Maps.FactoryTinyRace: [0x800285A2, 0x8002888E, 0x80028A0A],
        Maps.GalleonSealRace: [0x8002A232, 0x8002A08E],
        Maps.CastleTinyRace: [0x8002BAB6, 0x8002B6D6],
        Maps.JapesMinecarts: [0x806C4912],
        Maps.ForestMinecarts: [0x806C4956],
        Maps.CastleMinecarts: [0x806C499A],
    }
    static_overlay_races = [Maps.JapesMinecarts, Maps.ForestMinecarts, Maps.CastleMinecarts]
    for map_id in race_offset_data:
        if map_id in spoiler.coin_requirements:
            for addr in race_offset_data[map_id]:
                overlay = Overlay.Static if map_id in static_overlay_races else Overlay.Race
                writeValue(ROM_COPY, addr, overlay, spoiler.coin_requirements[map_id], offset_dict)


def grabUpdates(ROM_COPY: LocalROM, settings, offset_dict: dict, spoiler):
    """All changes related to item grabbing."""
    writeHook(ROM_COPY, 0x806A6708, Overlay.Static, "SpriteFix", offset_dict)
    writeFunction(ROM_COPY, 0x806A78A8, Overlay.Static, "getKongOwnershipFromFlag", offset_dict)  # Balloon: Kong Check
    # Pause: BP Get
    writeValue(ROM_COPY, 0x806AAB38, Overlay.Static, 0x24040000 | ReqItems.Blueprint, offset_dict, 4)
    writeValue(ROM_COPY, 0x806AAB40, Overlay.Static, 0x8FA5007C, offset_dict, 4)  # level as rotation
    writeValue(ROM_COPY, 0x806AAB30, Overlay.Static, 0x3C068075, offset_dict, 4)  # LUI $a2, hi(Character)
    writeValue(ROM_COPY, 0x806AAB34, Overlay.Static, 0x90C6E77C, offset_dict, 4)  # LBU $a2, lo(Character) ($a2)
    writeFunction(ROM_COPY, 0x806AAB3C, Overlay.Static, "getItemCount_new", offset_dict)
    # File Percentage: Keys
    writeValue(ROM_COPY, 0x806ABEFC, Overlay.Static, 0x24040000 | ReqItems.Key, offset_dict, 4)
    writeValue(ROM_COPY, 0x806ABF04, Overlay.Static, 0x2405FFFF, offset_dict, 4)  # Set arg1 to -1
    writeValue(ROM_COPY, 0x806ABF18, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806ABF1C, Overlay.Static, 0, offset_dict, 4)
    writeFunction(ROM_COPY, 0x806ABF00, Overlay.Static, "getItemCount_new", offset_dict)
    writeValue(ROM_COPY, 0x806ABF24, Overlay.Static, 0xA422C82C, offset_dict, 4)  # Store output to addr
    # File Percentage: Fairies
    writeValue(ROM_COPY, 0x806ABF2A, Overlay.Static, ReqItems.Fairy, offset_dict)
    writeFunction(ROM_COPY, 0x806ABF30, Overlay.Static, "getItemCount_new", offset_dict)
    # File Percentage: Medals
    writeValue(ROM_COPY, 0x806ABF42, Overlay.Static, ReqItems.Medal, offset_dict)
    writeFunction(ROM_COPY, 0x806ABF48, Overlay.Static, "getItemCount_new", offset_dict)
    # File Percentage: Crowns
    writeValue(ROM_COPY, 0x806ABF6C, Overlay.Static, 0x24040000 | ReqItems.Crown, offset_dict, 4)
    writeValue(ROM_COPY, 0x806ABF94, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806ABF98, Overlay.Static, 0, offset_dict, 4)
    writeFunction(ROM_COPY, 0x806ABF78, Overlay.Static, "getItemCount_new", offset_dict)
    writeValue(ROM_COPY, 0x806ABFA0, Overlay.Static, 0xA422C82A, offset_dict, 4)  # Store output to addr
    # File Percentage: NCoin
    writeValue(ROM_COPY, 0x806ABFA6, Overlay.Static, ReqItems.CompanyCoin, offset_dict)
    writeValue(ROM_COPY, 0x806ABFAC, Overlay.Static, 0x00003025, offset_dict, 4)  # Set arg2 to 0, this does leave arg1 undefined, but should be fine
    writeFunction(ROM_COPY, 0x806ABFA8, Overlay.Static, "getItemCount_new", offset_dict)
    # File Percentage: RCoin
    writeValue(ROM_COPY, 0x806ABFBA, Overlay.Static, ReqItems.CompanyCoin, offset_dict)
    writeValue(ROM_COPY, 0x806ABFC0, Overlay.Static, 0x24060001, offset_dict, 4)  # Set arg2 to 1, this does leave arg1 undefined, but should be fine
    writeFunction(ROM_COPY, 0x806ABFBC, Overlay.Static, "getItemCount_new", offset_dict)
    #
    writeFunction(ROM_COPY, 0x806AC00C, Overlay.Static, "getKongOwnershipFromFlag", offset_dict)  # File Percentage: Kongs
    # Key flag check: K Lumsy
    writeValue(ROM_COPY, 0x806BD308, Overlay.Static, 0x24040000 | ReqItems.Key, offset_dict, 4)
    writeValue(ROM_COPY, 0x806BD2BC, Overlay.Static, 0x02202825, offset_dict, 4)  # s1 (key iterator) as 2rd arg
    writeValue(ROM_COPY, 0x806BD2C4, Overlay.Static, 0x00003025, offset_dict, 4)  # 0 as 3rd arg
    writeFunction(ROM_COPY, 0x806BD304, Overlay.Static, "getItemCount_new", offset_dict)  # Key flag check: K. Lumsy
    #
    writeValue(ROM_COPY, 0x806F56F8, Overlay.Static, 0, offset_dict, 4)  # Disable Flag Set for blueprints
    writeFunction(ROM_COPY, 0x806A6CA8, Overlay.Static, "canItemPersist", offset_dict)  # Item Despawn Check
    writeValue(ROM_COPY, 0x806A741C, Overlay.Static, 0, offset_dict, 4)  # Prevent Key Twinkly Sound
    writeFunction(ROM_COPY, 0x80688714, Overlay.Static, "setupHook", offset_dict)  # Setup Load Hook
    # Fairy Adjustments
    writeFunction(ROM_COPY, 0x8072728C, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 1
    writeValue(ROM_COPY, 0x80727290, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
    writeFunction(ROM_COPY, 0x8072777C, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 2
    writeValue(ROM_COPY, 0x80727780, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
    writeFunction(ROM_COPY, 0x807277D0, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 3
    writeValue(ROM_COPY, 0x807277D4, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
    writeFunction(ROM_COPY, 0x80727B88, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 4
    writeValue(ROM_COPY, 0x80727B8C, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
    writeFunction(ROM_COPY, 0x80727C10, Overlay.Static, "spawnCharSpawnerActor", offset_dict)  # Spawn 4
    writeValue(ROM_COPY, 0x80727C14, Overlay.Static, 0x36050000, offset_dict, 4)  # ORI $a1, $s0, 0x0 -> Change second parameter to the spawner
    writeFunction(ROM_COPY, 0x806C5F04, Overlay.Static, "giveFairyItem", offset_dict)  # Fairy Flag Set
    # Rainbow Coins
    writeFunction(ROM_COPY, 0x806A2268, Overlay.Static, "spawnDirtPatchReward", offset_dict)  # Spawn Reward

    writeValue(ROM_COPY, 0x806C5C7C, Overlay.Static, 0, offset_dict, 4)  # Cancel out fairy draw distance reduction
    writeFunction(ROM_COPY, 0x806C63BC, Overlay.Static, "spawnRewardAtActor", offset_dict)  # Spawn Squawks Reward
    writeFunction(ROM_COPY, 0x806C4654, Overlay.Static, "spawnMinecartReward", offset_dict)  # Spawn Squawks Reward - Minecart
    writeFunction(ROM_COPY, 0x8002501C, Overlay.Bonus, "spawnCrownReward", offset_dict)  # Crown Spawn
    writeFunction(ROM_COPY, 0x80028650, Overlay.Boss, "spawnBossReward", offset_dict)  # Key Spawn

    writeFunction(ROM_COPY, 0x80027E68, Overlay.Critter, "fairyQueenCutsceneInit", offset_dict)  # BFI, Init Cutscene Setup
    writeFunction(ROM_COPY, 0x80028104, Overlay.Critter, "fairyQueenCutsceneCheck", offset_dict)  # BFI, Cutscene Play
    writeFunction(ROM_COPY, 0x80028014, Overlay.Critter, "fairyQueenCheckSpeedup", offset_dict)  # BFI, Cutscene Prep
    # Flag Stuff
    # Get blueprint count
    writeValue(ROM_COPY, 0x80024D06, Overlay.Menu, ReqItems.Blueprint, offset_dict)
    writeValue(ROM_COPY, 0x80024D08, Overlay.Menu, 0x2405FFFF, offset_dict, 4)  # All levels
    writeValue(ROM_COPY, 0x80024D10, Overlay.Menu, 0x00E03025, offset_dict, 4)  # OR $a2, $a3, $zero
    writeFunction(ROM_COPY, 0x80024D0C, Overlay.Menu, "getItemCount_new", offset_dict)  # Flag change to FLUT
    # Get blueprint status for gb giving
    writeValue(ROM_COPY, 0x8002483A, Overlay.Menu, ReqItems.Blueprint, offset_dict)
    writeValue(ROM_COPY, 0x800248D2, Overlay.Menu, ReqItems.Blueprint, offset_dict)
    writeFunction(ROM_COPY, 0x80024840, Overlay.Menu, "getItemCount_new", offset_dict)
    writeValue(ROM_COPY, 0x80024854, Overlay.Menu, 0x00801025, offset_dict, 4)  # OR $v0, $a0, $zero
    # Pause Stuff
    writeFunction(ROM_COPY, 0x806A9D50, Overlay.Static, "handleOutOfCounters", offset_dict)  # Print out of counter, depending on item rando state
    writeFunction(ROM_COPY, 0x806A9EFC, Overlay.Static, "handleOutOfCounters", offset_dict)  # Print out of counter, depending on item rando state
    writeValue(ROM_COPY, 0x806A9C80, Overlay.Static, 0, offset_dict, 4)  # Show counter on Helm Menu - Kong specific screeen
    writeValue(ROM_COPY, 0x806A9E54, Overlay.Static, 0, offset_dict, 4)  # Show counter on Helm Menu - All Kongs screen
    # writeValue(ROM_COPY, 0x806AA860, Overlay.Static, 0x31EF0007, offset_dict, 4) # ANDI $t7, $t7, 7 - Show GB (Kong Specific)
    # writeValue(ROM_COPY, 0x806AADC4, Overlay.Static, 0x33390007, offset_dict, 4) # ANDI $t9, $t9, 7 - Show GB (All Kongs)
    # writeValue(ROM_COPY, 0x806AADC8, Overlay.Static, 0xAFB90058, offset_dict, 4) # SW $t9, 0x58 ($sp) - Show GB (All Kongs)
    # Actors with special spawning conditions
    writeValue(ROM_COPY, 0x806B4E1A, Overlay.Static, 1, offset_dict)
    writeFunction(ROM_COPY, 0x806B4E40, Overlay.Static, "spawnWeirdReward", offset_dict)
    writeValue(ROM_COPY, 0x8069C266, Overlay.Static, 0, offset_dict)
    writeFunction(ROM_COPY, 0x8069C29C, Overlay.Static, "spawnWeirdReward0", offset_dict)
    # Melon Crates
    writeLabelValue(ROM_COPY, 0x80747EB0, Overlay.Static, "melonCrateItemHandler", offset_dict)
    # Grabbable Item Rando
    writeHook(ROM_COPY, 0x8069C210, Overlay.Static, "spawnHoldableObject", offset_dict)
    writeFunction(ROM_COPY, 0x8069BDE8, Overlay.Static, "renderBoulderSparkles", offset_dict)
    writeFunction(ROM_COPY, 0x8067BDA0, Overlay.Static, "updateKegIDs", offset_dict)
    # Jetpac Reward Text
    addr = getROMAddress(0x8002EABC, Overlay.Jetpac, offset_dict)
    ROM_COPY.seek(addr)
    ROM_COPY.writeBytes(bytes("REWARD COLLECTED\0", "ascii"))
    # Fairy count check
    writeValue(ROM_COPY, 0x806F8EBE, Overlay.Static, ReqItems.Fairy, offset_dict)
    writeFunction(ROM_COPY, 0x806F8EC4, Overlay.Static, "getItemCount_new", offset_dict)
    # Initialize fixed item scales
    writeFunction(ROM_COPY, 0x806F4918, Overlay.Static, "writeItemScale", offset_dict)  # Write scale to collision info
    writeValue(ROM_COPY, 0x806F491C, Overlay.Static, 0x87A40066, offset_dict, 4)  # LH $a0, 0x66 ($sp)
    # Kong
    writeFunction(ROM_COPY, 0x80683638, Overlay.Static, "giveKongFromFlag", offset_dict)

    writeValue(ROM_COPY, 0x806F4C6E, Overlay.Static, 0x20, offset_dict)  # Change size
    writeValue(ROM_COPY, 0x806F4C82, Overlay.Static, 0x20, offset_dict)  # Change size
    writeFunction(ROM_COPY, 0x806F515C, Overlay.Static, "writeItemActorScale", offset_dict)  # Write actor scale to collision info
    writeFunction(ROM_COPY, 0x80681910, Overlay.Static, "spawnBonusReward", offset_dict)  # Spawn Bonus Reward
    writeValue(ROM_COPY, 0x806C46AA, Overlay.Static, 0x4100, offset_dict)  # Bring squawks closer to the player for minecarts (X)
    writeValue(ROM_COPY, 0x806C46E2, Overlay.Static, 0x4100, offset_dict)  # Bring squawks closer to the player for minecarts (Z)
    writeValue(ROM_COPY, 0x806C45C2, Overlay.Static, 0x0013, offset_dict)  # Y Offset squawks reward
    # Flag Mapping
    flag_map_hi = getHiSym("new_flag_mapping")
    flag_map_lo = getLoSym("new_flag_mapping")
    flag_map_count = getVar("gb_dictionary_count")
    writeKongItemOwnership(ROM_COPY, settings)
    writeValue(ROM_COPY, 0x8073150A, Overlay.Static, flag_map_hi, offset_dict)
    writeValue(ROM_COPY, 0x8073151E, Overlay.Static, flag_map_lo, offset_dict)
    writeValue(ROM_COPY, 0x8073151A, Overlay.Static, flag_map_count, offset_dict)
    writeValue(ROM_COPY, 0x807315EA, Overlay.Static, flag_map_hi, offset_dict)
    writeValue(ROM_COPY, 0x807315FE, Overlay.Static, flag_map_lo, offset_dict)
    writeValue(ROM_COPY, 0x807315FA, Overlay.Static, flag_map_count, offset_dict)
    writeValue(ROM_COPY, 0x80731666, Overlay.Static, flag_map_hi, offset_dict)
    writeValue(ROM_COPY, 0x80731676, Overlay.Static, flag_map_lo, offset_dict)
    writeValue(ROM_COPY, 0x80731672, Overlay.Static, flag_map_count, offset_dict)
    writeHook(ROM_COPY, 0x8069840C, Overlay.Static, "VineCode", offset_dict)
    writeHook(ROM_COPY, 0x80698420, Overlay.Static, "VineShowCode", offset_dict)
    writeHook(ROM_COPY, 0x8063ED7C, Overlay.Static, "HandleSlamCheck", offset_dict)
    writeHook(ROM_COPY, 0x80648364, Overlay.Static, "ShopImageHandler", offset_dict)
    writeHook(ROM_COPY, 0x806F6EA0, Overlay.Static, "BarrelMovesFixes", offset_dict)
    writeHook(ROM_COPY, 0x806E4930, Overlay.Static, "ChimpyChargeFix", offset_dict)
    writeHook(ROM_COPY, 0x806E48AC, Overlay.Static, "OStandFix", offset_dict)
    writeHook(ROM_COPY, 0x8067ECB8, Overlay.Static, "HunkyChunkyFix2", offset_dict)
    # Decouple Camera from Shockwave
    FLAG_ABILITY_CAMERA = 0x2FD
    writeValue(ROM_COPY, 0x806E9812, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Usage
    writeFunction(ROM_COPY, 0x806E9814, Overlay.Static, "hasFlagMove", offset_dict)
    writeValue(ROM_COPY, 0x806AB0F6, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Isles Fairies Display
    writeFunction(ROM_COPY, 0x806AB0F8, Overlay.Static, "hasFlagMove", offset_dict)
    writeValue(ROM_COPY, 0x806AAFB6, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Other Fairies Display
    writeFunction(ROM_COPY, 0x806AAFB8, Overlay.Static, "hasFlagMove", offset_dict)
    writeValue(ROM_COPY, 0x806AA762, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Display
    writeFunction(ROM_COPY, 0x806AA764, Overlay.Static, "hasFlagMove", offset_dict)
    writeValue(ROM_COPY, 0x8060D986, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Refill
    writeFunction(ROM_COPY, 0x8060D988, Overlay.Static, "hasFlagMove", offset_dict)
    writeValue(ROM_COPY, 0x806F6F76, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film Refill
    writeFunction(ROM_COPY, 0x806F6F78, Overlay.Static, "hasFlagMove", offset_dict)
    writeValue(ROM_COPY, 0x806F916A, Overlay.Static, FLAG_ABILITY_CAMERA, offset_dict)  # Film max
    # writeFunction(ROM_COPY, 0x806F916C, Overlay.Static, "hasFlagMove", offset_dict)
    writeValue(ROM_COPY, 0x806F916C, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP (Skip this check, as the line below will render it obsolete)
    writeValue(ROM_COPY, 0x806F9174, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP (Skip setting film count to 0, to prevent that from happening)
    # Shockwave
    writeFunction(ROM_COPY, 0x806CA308, Overlay.Static, "hasFlagMove", offset_dict)
    writeFunction(ROM_COPY, 0x806F6EBC, Overlay.Static, "hasFlagMove", offset_dict)
    # Training
    writeFunction(ROM_COPY, 0x80698368, Overlay.Static, "hasFlagMove", offset_dict)  # Vines
    writeFunction(ROM_COPY, 0x8072F190, Overlay.Static, "hasFlagMove", offset_dict)  # Vines
    writeFunction(ROM_COPY, 0x806E4250, Overlay.Static, "hasFlagMove", offset_dict)  # Barrels
    writeFunction(ROM_COPY, 0x806E7718, Overlay.Static, "hasFlagMove", offset_dict)  # Dive
    writeFunction(ROM_COPY, 0x806E2D6C, Overlay.Static, "hasFlagMove", offset_dict)  # Oranges

    item_get_addrs = [
        0x806F64C8,
        0x806F6BA8,
        0x806F7740,
        0x806F7764,
        0x806F7774,
        0x806F7798,
        0x806F77B0,
        0x806F77C4,
        0x806F7804,
        0x806F781C,
    ]
    for addr in item_get_addrs:
        writeFunction(ROM_COPY, addr, Overlay.Static, "getItem", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x806F6350, Overlay.Static, "getObjectCollectability", offset_dict)  # Modify Function Call
    writeFunction(ROM_COPY, 0x8070E1F0, Overlay.Static, "handleDynamicItemText", offset_dict)  # Handle Dynamic Text Item Name
    writeFunction(ROM_COPY, 0x806A7AEC, Overlay.Static, "BalloonShoot", offset_dict)  # Balloon Shoot Hook
    # Rainbow Coins
    writeFunction(ROM_COPY, 0x806A222C, Overlay.Static, "getPatchFlag", offset_dict)  # Get Patch Flags
    writeFunction(ROM_COPY, 0x806A2058, Overlay.Static, "getPatchFlag", offset_dict)  # Get Patch Flags
    writeValue(ROM_COPY, 0x80688C8E, Overlay.Static, 0x30, offset_dict)  # Reduce scope of detecting if balloon or patch, so patches don't have dynamic flags
    writeFunction(ROM_COPY, 0x80680AE8, Overlay.Static, "alterBonusVisuals", offset_dict)  # Get Bonus Flag Check
    writeFunction(ROM_COPY, 0x806A206C, Overlay.Static, "getDirtPatchSkin", offset_dict)  # Get Dirt Flag Check
    writeFunction(ROM_COPY, 0x80681854, Overlay.Static, "getBonusFlag", offset_dict)  # Get Bonus Flag Check
    writeFunction(ROM_COPY, 0x806C63A8, Overlay.Static, "getBonusFlag", offset_dict)  # Get Bonus Flag Check
    # Medals
    writeHook(ROM_COPY, 0x806F9348, Overlay.Static, "banana_medal_handler", offset_dict)
    # Move Decoupling
    # Strong Kong
    writeValue(ROM_COPY, 0x8067ECFC, Overlay.Static, 0x30810002, offset_dict, 4)  # ANDI $at $a0 2
    writeValue(ROM_COPY, 0x8067ED00, Overlay.Static, 0x50200003, offset_dict, 4)  # BEQL $at $r0 3
    # Rocketbarrel
    writeValue(ROM_COPY, 0x80682024, Overlay.Static, 0x31810002, offset_dict, 4)  # ANDI $at $t4 2
    writeValue(ROM_COPY, 0x80682028, Overlay.Static, 0x50200006, offset_dict, 4)  # BEQL $at $r0 0x6
    # OSprint
    writeValue(ROM_COPY, 0x8067ECE0, Overlay.Static, 0x30810004, offset_dict, 4)  # ANDI $at $a0 4
    writeValue(ROM_COPY, 0x8067ECE4, Overlay.Static, 0x10200002, offset_dict, 4)  # BEQZ $at, 2
    # Mini Monkey
    writeValue(ROM_COPY, 0x8067EC80, Overlay.Static, 0x30830001, offset_dict, 4)  # ANDI $v1 $a0 1
    writeValue(ROM_COPY, 0x8067EC84, Overlay.Static, 0x18600002, offset_dict, 4)  # BLEZ $v1 2
    # Hunky Chunky (Not Dogadon)
    writeValue(ROM_COPY, 0x8067ECA0, Overlay.Static, 0x30810001, offset_dict, 4)  # ANDI $at $a0 1
    writeValue(ROM_COPY, 0x8067ECA4, Overlay.Static, 0x18200002, offset_dict, 4)  # BLEZ $at 2
    # PTT
    writeValue(ROM_COPY, 0x806E20F0, Overlay.Static, 0x31010002, offset_dict, 4)  # ANDI $at $t0 2
    writeValue(ROM_COPY, 0x806E20F4, Overlay.Static, 0x5020000F, offset_dict, 4)  # BEQL $at $r0 0xF
    # PPunch
    writeValue(ROM_COPY, 0x806E48F4, Overlay.Static, 0x31810002, offset_dict, 4)  # ANDI $at $t4 2
    writeValue(ROM_COPY, 0x806E48F8, Overlay.Static, 0x50200074, offset_dict, 4)  # BEQL $at $r0 0xF
    # Menu/Shop: Mystery
    move_levels = (1, 1, 3, 1, 7, 1, 1, 7)
    for index, value in enumerate(move_levels):
        writeValue(ROM_COPY, 0x80033938 + (8 * index) + 4, Overlay.Menu, value, offset_dict, 1)
    # Menu/Shop: Misc Shop Stuff
    writeHook(ROM_COPY, 0x800260E0, Overlay.Menu, "CrankyDecouple", offset_dict)
    writeHook(ROM_COPY, 0x800260A8, Overlay.Menu, "ForceToBuyMoveInOneLevel", offset_dict)
    writeValue(ROM_COPY, 0x80026160, Overlay.Menu, 0, offset_dict, 4)
    writeHook(ROM_COPY, 0x80026140, Overlay.Menu, "PriceKongStore", offset_dict)
    writeHook(ROM_COPY, 0x80025FC0, Overlay.Menu, "CharacterCollectableBaseModify", offset_dict)
    writeHook(ROM_COPY, 0x800260F0, Overlay.Menu, "SetMoveBaseBitfield", offset_dict)
    writeHook(ROM_COPY, 0x8002611C, Overlay.Menu, "SetMoveBaseProgressive", offset_dict)
    writeHook(ROM_COPY, 0x80026924, Overlay.Menu, "AlwaysCandyInstrument", offset_dict)
    writeValue(ROM_COPY, 0x80026072, Overlay.Menu, getHiSym("CrankyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002607A, Overlay.Menu, getLoSym("CrankyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002607E, Overlay.Menu, getHiSym("CandyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x80026086, Overlay.Menu, getLoSym("CandyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002608A, Overlay.Menu, getHiSym("FunkyMoves_New"), offset_dict)
    writeValue(ROM_COPY, 0x8002608E, Overlay.Menu, getLoSym("FunkyMoves_New"), offset_dict)
    # Menu/Shop: Cross Kong Purchases
    writeValue(ROM_COPY, 0x80025EA0, Overlay.Menu, 0x90850004, offset_dict, 4)  # Change target kong (Progressive) # LBU     a1, 0x4 (a0)
    writeValue(ROM_COPY, 0x80025E80, Overlay.Menu, 0x90850004, offset_dict, 4)  # Change target kong (Bitfield) # LBU    a1, 0x4 (a0)
    writeValue(ROM_COPY, 0x80025F70, Overlay.Menu, 0x93060005, offset_dict, 4)  # Change price deducted # LBU    a2, 0x5 (t8)
    writeValue(ROM_COPY, 0x80026200, Overlay.Menu, 0x90CF0005, offset_dict, 4)  # Change price check # LBU   t7, 0x5 (a2)
    writeValue(ROM_COPY, 0x80027AE0, Overlay.Menu, 0x910F0004, offset_dict, 4)  # Change Special Moves Text # LBU    t7, 0x4 (t0)
    writeValue(ROM_COPY, 0x80027BA0, Overlay.Menu, 0x91180004, offset_dict, 4)  # Change Gun Text # LBU  t8, 0x4 (t0)
    writeValue(ROM_COPY, 0x80027C14, Overlay.Menu, 0x910C0004, offset_dict, 4)  # Change Instrument Text # LBU   t4, 0x4 (t0)
    writeValue(ROM_COPY, 0x80026C08, Overlay.Menu, 0x91790011, offset_dict, 4)  # Fix post-special move text # LBU   t9, 0x11 (t3)
    writeValue(ROM_COPY, 0x80026C00, Overlay.Menu, 0x916D0004, offset_dict, 4)  # Fix post-special move text # LBU   t5, 0x4 (t3)
    # Menu/Shop: Move Bitfield
    writeValue(ROM_COPY, 0x80025E9C, Overlay.Menu, 0x0C009751, offset_dict, 4)  # Change writing of move to "write bitfield move" function call
    writeValue(ROM_COPY, 0x8002E266, Overlay.Menu, 7, offset_dict)  # Enguarde Arena Movement Write
    writeValue(ROM_COPY, 0x8002F01E, Overlay.Menu, 7, offset_dict)  # Rambi Arena Movement Write
    # Menu/Shop: Change move purchase
    writeFunction(ROM_COPY, 0x80026720, Overlay.Menu, "getNextMovePurchase", offset_dict)
    writeFunction(ROM_COPY, 0x8002683C, Overlay.Menu, "getNextMovePurchase", offset_dict)
    # Menu/Shop: Write Modified purchase move stuff
    writeFunction(ROM_COPY, 0x80027324, Overlay.Menu, "purchaseFirstMoveHandler", offset_dict)
    if not settings.fast_start_beginning_of_game:
        writeFunction(ROM_COPY, 0x80027150, Overlay.Menu, "checkFirstMovePurchase", offset_dict)
    writeFunction(ROM_COPY, 0x8002691C, Overlay.Menu, "purchaseMove", offset_dict)
    writeFunction(ROM_COPY, 0x800270B8, Overlay.Menu, "showPostMoveText", offset_dict)
    writeFunction(ROM_COPY, 0x80026508, Overlay.Menu, "canPlayJetpac", offset_dict)
    writeValue(ROM_COPY, 0x80026F64, Overlay.Menu, 0, offset_dict, 4)  # Disable check for whether you have a move before giving donation at shop
    writeValue(ROM_COPY, 0x80026F68, Overlay.Menu, 0, offset_dict, 4)  # Disable check for whether you have a move before giving donation at shop
    # Menu/Shop: Shop Hints
    if settings.enable_shop_hints:
        writeFunction(ROM_COPY, 0x8002661C, Overlay.Menu, "getMoveHint", offset_dict)
        writeFunction(ROM_COPY, 0x800265F0, Overlay.Menu, "getMoveHint", offset_dict)
    # TBarrel/BFI Rewards
    # writeValue(ROM_COPY, 0x80681CE2, Overlay.Static, 0, offset_dict)
    # writeValue(ROM_COPY, 0x80681CFA, Overlay.Static, 1, offset_dict)
    # writeValue(ROM_COPY, 0x80681D06, Overlay.Static, 2, offset_dict)
    # writeValue(ROM_COPY, 0x80681D12, Overlay.Static, 3, offset_dict)
    # writeValue(ROM_COPY, 0x80681C8A, Overlay.Static, 0, offset_dict)
    # writeValue(ROM_COPY, 0x800295F6, Overlay.Critter, 0, offset_dict)
    # writeValue(ROM_COPY, 0x80029606, Overlay.Critter, 1, offset_dict)
    # writeValue(ROM_COPY, 0x800295FE, Overlay.Critter, 3, offset_dict)
    # writeValue(ROM_COPY, 0x800295DA, Overlay.Critter, 2, offset_dict)
    writeValue(ROM_COPY, 0x80027F2A, Overlay.Critter, 4, offset_dict)
    writeValue(ROM_COPY, 0x80027E1A, Overlay.Critter, 4, offset_dict)
    # writeFunction(ROM_COPY, 0x80681D38, Overlay.Static, "getLocationStatus", offset_dict)  # Get TBarrels Move
    # writeFunction(ROM_COPY, 0x80681C98, Overlay.Static, "getLocationStatus", offset_dict)  # Get TBarrels Move
    # writeFunction(ROM_COPY, 0x80029610, Overlay.Critter, "setLocationStatus", offset_dict)  # Set TBarrels Move
    writeFunction(ROM_COPY, 0x80027F24, Overlay.Critter, "setLocationStatus", offset_dict)  # Set BFI Move
    writeFunction(ROM_COPY, 0x80027E20, Overlay.Critter, "getLocationStatus", offset_dict)  # Get BFI Move
    writeValue(ROM_COPY, 0x80681DE4, Overlay.Static, 0x5000, offset_dict)
    writeHook(ROM_COPY, 0x80680AD4, Overlay.Static, "expandTBarrelResponse", offset_dict)  # Allow Training Barrels to disappear if already beaten
    writeValue(ROM_COPY, 0x80681C16, Overlay.Static, 0xF, offset_dict)  # Disregard most special code from a bonus
    # Ice Trap Music
    writeFunction(ROM_COPY, 0x806C5F44, Overlay.Static, "playIceTrapSong", offset_dict)
    writeFunction(ROM_COPY, 0x806C5F54, Overlay.Static, "cancelIceTrapSong", offset_dict)  # Picture taken
    writeFunction(ROM_COPY, 0x80727E90, Overlay.Static, "cancelIceTrapSong", offset_dict)  # Out of range
    # Remove set flag for weird checks
    writeValue(ROM_COPY, 0x8002A490, Overlay.Race, 0, offset_dict, 4)  # Seal Race
    writeValue(ROM_COPY, 0x8002B8F0, Overlay.Race, 0, offset_dict, 4)  # Castle Car
    # Snide Rewards
    writeFunction(ROM_COPY, 0x80024CF0, Overlay.Menu, "getTurnedCount", offset_dict)
    writeValue(ROM_COPY, 0x80024CE6, Overlay.Menu, -1, offset_dict, 2, True)
    writeFunction(ROM_COPY, 0x80024D28, Overlay.Menu, "getTurnedCount", offset_dict)
    writeValue(ROM_COPY, 0x80024D20, Overlay.Menu, 0x00E02025, offset_dict, 4)  # Copy kong to arg0
    writeFunction(ROM_COPY, 0x80024980, Overlay.Menu, "turnedAllIn", offset_dict)
    writeValue(ROM_COPY, 0x8002498A, Overlay.Menu, 2, offset_dict)  # speed up lookup
    writeFunction(ROM_COPY, 0x800254A8, Overlay.Menu, "hasTurnedInAtLeast", offset_dict)


def fairyFix(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to fixing fairy behavior."""
    # Fix issues where multiple loaded fairies will only allow 1 fairy to be referenced
    if FAIRY_LOAD_FIX:
        # Paad Offset | Actor offset | var name
        # 038         | 1B0          | ScreenX
        # 03A         | 1B2          | ScreenY
        # 03C         | 1B4          | Dist
        # 03E         | 1B6          | In Range
        FAIRY_SCREEN_X = 0x1B0
        FAIRY_SCREEN_Y = 0x1B2
        FAIRY_SCREEN_DIST = 0x1B4
        FAIRY_SCREEN_RANGE = 0x1B6
        writeValue(ROM_COPY, 0x806C5DA0, Overlay.Static, 0x8D4CBB40, offset_dict, 4)  # lw $t4, 0xBB40 ($t2) - Get current actor pointer
        writeValue(ROM_COPY, 0x806C5DA4, Overlay.Static, 0x2550D580, offset_dict, 4)  # addiu $s0, $t2, 0xD580 - Get extra player pointer addr (Overwritten)
        writeValue(ROM_COPY, 0x806C5DA8, Overlay.Static, 0x8D4AC924, offset_dict, 4)  # lw $t2, 0xC924 ($t2) - Get char change pointer (overwritten)
        writeValue(ROM_COPY, 0x806C5DAC, Overlay.Static, 0x85820000 | FAIRY_SCREEN_X, offset_dict, 4)  # lh $v0, 0x01B0 ($t4) - Get screen X in fairy storage
        writeValue(ROM_COPY, 0x806C5DB0, Overlay.Static, 0xC5500284, offset_dict, 4)  # lwc1 $f16, 0x0284 ($t2) - Get some char spawner attr (Overwritten)
        # writeValue(ROM_COPY, 0x806C5DB8, Overlay.Static, 0xA5800000 | FAIRY_SCREEN_RANGE, offset_dict, 4)  # sh $zero, 0x1B6 ($t4) - Store fairy not in box
        writeValue(ROM_COPY, 0x806C5DB8, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP
        writeValue(ROM_COPY, 0x806C5DCC, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP
        writeValue(ROM_COPY, 0x806C5DD0, Overlay.Static, 0x85820000 | FAIRY_SCREEN_Y, offset_dict, 4)  # lh $v0, 0x01B2 ($t4) - Get screen Y in fairy storage
        if not IsDDMSSelected(settings.misc_changes_selected, MiscChangesSelected.better_fairy_camera):
            writeValue(ROM_COPY, 0x806C5DE4, Overlay.Static, 0x00000000, offset_dict, 4)  # NOP
            writeValue(ROM_COPY, 0x806C5DE8, Overlay.Static, 0x858B0000 | FAIRY_SCREEN_DIST, offset_dict, 4)  # lh $t3, 0x01B4 ($t4) - Get max dist in fairy storage
        writeValue(ROM_COPY, 0x806C5E00, Overlay.Static, 0x45000016, offset_dict, 4)  # bc1f 0x16 - Free up one slot so we can store the box addr
        writeValue(ROM_COPY, 0x806C5E08, Overlay.Static, 0x24010001, offset_dict, 4)  # li $at, 1 - Shift this one addr earlier
        writeValue(ROM_COPY, 0x806C5E0C, Overlay.Static, 0xA5810000 | FAIRY_SCREEN_RANGE, offset_dict, 4)  # sh $at, 0x1b6 ($t4) - Store fairy as in box
        writeValue(
            ROM_COPY, 0x806C5E10, Overlay.Static, 0x904D01EC, offset_dict, 4
        )  # lbu $t5 0x01EC ($v0) - Fix the reference address since we're no longer storing a copy of extra player pointer to t4
        # Storage
        writeHook(ROM_COPY, 0x806C5FA8, Overlay.Static, "storeFairyData", offset_dict)
        # Check
        writeValue(ROM_COPY, 0x806C5EA8, Overlay.Static, 0x3C108080, offset_dict, 4)  # lui $s0, 0x8080
        writeValue(ROM_COPY, 0x806C5EAC, Overlay.Static, 0x8E0ABB40, offset_dict, 4)  # lw $t2, 0xBB40 ($s0)
        writeValue(ROM_COPY, 0x806C5EB0, Overlay.Static, 0x854A0000 | FAIRY_SCREEN_RANGE, offset_dict, 4)  # lh $t2, 0x01B6 ($t2)
        writeValue(ROM_COPY, 0x806C5EB4, Overlay.Static, 0x1140001B, offset_dict, 4)  # beqz $t2, 0x1B
        # Face controllers
        writeHook(ROM_COPY, 0x806C5E88, Overlay.Static, "setSadFace", offset_dict)
        writeHook(ROM_COPY, 0x806C5E3C, Overlay.Static, "setHappyFace", offset_dict)
        writeFunction(ROM_COPY, 0x806CAAA0, Overlay.Static, "resetPictureStatus", offset_dict)

        # Thankfully currentactor is loaded into a0.
        # I don't think we can sneak in creating the other JALs necessary to calculate distance.
        # We could make this part of "better fairy camera"? This means those calcuations don't need to be made.


def dropTableUpdates(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to the drop table."""
    # Expand Enemy Drops Table
    writeValue(ROM_COPY, 0x806A5CA6, Overlay.Static, getHiSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CB6, Overlay.Static, getLoSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CBA, Overlay.Static, getHiSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CBE, Overlay.Static, getLoSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CD2, Overlay.Static, getHiSym("drops"), offset_dict, 2)
    writeValue(ROM_COPY, 0x806A5CD6, Overlay.Static, getLoSym("drops"), offset_dict, 2)
    # Drop Table
    REPLENISHABLES = (
        0x2F,  # Watermelon
        0x34,  # Orange
        0x33,  # Ammo Crate
        0x79,  # Crystal
    )
    if settings.no_melons and Types.Enemies not in settings.shuffled_location_types:
        DROP_TABLE = getSym("drops")
        for i in range(35):  # DROP_COUNT -  TODO: Hook this up with a var
            DROP_START = DROP_TABLE + (i * 6)
            drop_i = getROMAddress(DROP_START, Overlay.Custom, offset_dict)
            ROM_COPY.seek(drop_i)
            drop_source = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if drop_source != 0:
                ROM_COPY.seek(drop_i + 2)
                drop_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if drop_type in REPLENISHABLES:
                    writeValue(ROM_COPY, DROP_START, Overlay.Custom, 3, offset_dict)


def pauseUpdates(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to the pause menu and game HUD."""
    # HUD Reallocation
    writeFunction(ROM_COPY, 0x806F48C8, Overlay.Static, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x806C9C60, Overlay.Static, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x806C90A8, Overlay.Static, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x8002664C, Overlay.Menu, "allocateHUD", offset_dict)
    writeFunction(ROM_COPY, 0x806F97D8, Overlay.Static, "getHUDSprite_Complex", offset_dict)
    writeFunction(ROM_COPY, 0x806BE4E4, Overlay.Static, "getHUDSprite_Complex", offset_dict)
    writeFunction(ROM_COPY, 0x806AB588, Overlay.Static, "getHUDSprite_Complex", offset_dict)
    writeFunction(ROM_COPY, 0x806F98E4, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9A00, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9A78, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9BC0, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeFunction(ROM_COPY, 0x806F9D14, Overlay.Static, "initHUDDirection", offset_dict)  # HUD Direction
    writeHook(ROM_COPY, 0x80639F44, Overlay.Static, "disableRouletteNumbers", offset_dict)  # Disable Roulette numbers during pause
    writeHook(ROM_COPY, 0x806F93E0, Overlay.Static, "updateBarrierNumbers", offset_dict)  # Update barrier numbers
    # Change pause menu background design
    writeValue(ROM_COPY, 0x806A84F4, Overlay.Static, 0, offset_dict, 4)  # Enable framebuffer clear on pause menu
    writeValue(ROM_COPY, 0x806A90E8, Overlay.Static, 0, offset_dict, 4)  # Disable Screen Shake
    writeValue(ROM_COPY, 0x806AC056, Overlay.Static, 120, offset_dict)  # Changes darkness opacity
    # Fix Pause Menu
    writeValue(ROM_COPY, 0x806ABFF8, Overlay.Static, 0, offset_dict, 4)  # NOP (Write of first slot to 1)
    writeValue(ROM_COPY, 0x806AC002, Overlay.Static, 0x530, offset_dict)
    writeValue(ROM_COPY, 0x806AC006, Overlay.Static, 0x5B0, offset_dict)
    writeValue(ROM_COPY, 0x8075054D, Overlay.Static, 0xD7, offset_dict, 1)  # Change DK Q Mark to #FFD700
    writeValue(ROM_COPY, 0x806A9C80, Overlay.Static, 0, offset_dict, 4)  # Level check NOP
    writeValue(ROM_COPY, 0x806A9E54, Overlay.Static, 0, offset_dict, 4)  # Level check NOP
    # Pause Sprite Expansion / Carousel Init Functions
    # Sprites
    writeValue(ROM_COPY, 0x806AB35A, Overlay.Static, getHiSym("pause_items"), offset_dict)
    writeValue(ROM_COPY, 0x806AB35E, Overlay.Static, getLoSym("pause_items"), offset_dict)
    writeValue(ROM_COPY, 0x806AB364, Overlay.Static, 0x0010C8C0, offset_dict, 4)  # << 3 instead of << 2
    #
    writeValue(ROM_COPY, 0x806AB2CA, Overlay.Static, getHiSym("pause_items"), offset_dict)
    writeValue(ROM_COPY, 0x806AB2DA, Overlay.Static, getLoSym("pause_items"), offset_dict)
    writeValue(ROM_COPY, 0x806AB2DE, Overlay.Static, 6, offset_dict)  # Offset of count in struct
    writeValue(ROM_COPY, 0x806AB2E2, Overlay.Static, 8, offset_dict)  # strict size
    item_count_addr = getSym("pause_items") + 6
    writeValue(ROM_COPY, 0x806A9FC2, Overlay.Static, getHi(item_count_addr), offset_dict)
    writeValue(ROM_COPY, 0x806AA036, Overlay.Static, getLo(item_count_addr), offset_dict)
    #
    item_cap_addr = getSym("pause_items") + 4
    writeValue(ROM_COPY, 0x806AA00E, Overlay.Static, getHi(item_cap_addr), offset_dict)
    writeValue(ROM_COPY, 0x806AA032, Overlay.Static, getLo(item_cap_addr), offset_dict)
    writeValue(ROM_COPY, 0x806AA024, Overlay.Static, 0x000258C0, offset_dict, 4)  # << 3 instead of << 1
    #
    writeFunction(ROM_COPY, 0x806AB3C4, Overlay.Static, "updatePauseScreenWheel", offset_dict)  # Change Wheel to scroller
    writeValue(ROM_COPY, 0x806AB3B4, Overlay.Static, 0xAFB00018, offset_dict, 4)  # SW $s0, 0x18 ($sp). Change last param to index
    writeValue(ROM_COPY, 0x806AB3A0, Overlay.Static, 0xAFA90014, offset_dict, 4)  # SW $t1, 0x14 ($sp). Change 2nd-to-last param to local index
    writeValue(ROM_COPY, 0x806AB444, Overlay.Static, 0, offset_dict, 4)  # Prevent joystick sprite rendering
    writeValue(ROM_COPY, 0x806A8DB2, Overlay.Static, 0x0029, offset_dict)  # Swap left/right direction
    writeValue(ROM_COPY, 0x806A8DBA, Overlay.Static, 0xFFD8, offset_dict)  # Swap left/right direction
    writeValue(ROM_COPY, 0x806A8DB4, Overlay.Static, 0x5420, offset_dict)  # BEQL -> BNEL
    writeValue(ROM_COPY, 0x806A8DF0, Overlay.Static, 0x1020, offset_dict)  # BNE -> BEQ
    writeFunction(ROM_COPY, 0x806A9F74, Overlay.Static, "pauseScreen3And4ItemName", offset_dict)  # Item Name"
    # Check Screen
    writeFunction(ROM_COPY, 0x806A9F98, Overlay.Static, "pauseScreen3And4Header", offset_dict)  # Header
    writeFunction(ROM_COPY, 0x806AA03C, Overlay.Static, "pauseScreen3And4Counter", offset_dict)  # Counter
    writeFunction(ROM_COPY, 0x806A86BC, Overlay.Static, "changePauseScreen", offset_dict)  # Change screen hook
    writeFunction(ROM_COPY, 0x806A8D20, Overlay.Static, "changeSelectedLevel", offset_dict)  # Change selected level on checks screen
    writeFunction(ROM_COPY, 0x806A84F8, Overlay.Static, "checkItemDB", offset_dict)  # Populate Item Databases
    writeFunction(ROM_COPY, 0x806A9978, Overlay.Static, "displayHintRegion", offset_dict)  # Display hint region
    writeValue(ROM_COPY, 0x806AA018, Overlay.Static, 0x01E01025, offset_dict, 4)  # Remove MenuActivatedItems
    writeValue(ROM_COPY, 0x806A94CC, Overlay.Static, 0x2C610003, offset_dict, 4)  # SLTIU $at, $v1, 0x3 (Changes render check for <3 rather than == 3)
    writeValue(ROM_COPY, 0x806A94D0, Overlay.Static, 0x10200298, offset_dict, 4)  # BEQZ $at, 0x298 (Changes render check for <3 rather than == 3)
    writeValue(ROM_COPY, 0x806A932A, Overlay.Static, 12500, offset_dict)  # Increase memory allocated for displaying the Pause menu (fixes hints corrupting the heap)
    if settings.progressive_hint_item == ProgressiveHintItem.req_cb:
        writeFunction(ROM_COPY, 0x806AB4C4, Overlay.Static, "displayCBCount", offset_dict)
    # Pause Stuff
    # Prevent GBs being required to view extra screens
    writeValue(ROM_COPY, 0x806A8624, Overlay.Static, 0, offset_dict, 4)  # GBs doesn't lock other pause screens
    writeValue(ROM_COPY, 0x806AB468, Overlay.Static, 0, offset_dict, 4)  # Show R/Z Icon
    writeValue(ROM_COPY, 0x806AB318, Overlay.Static, 0x24060001, offset_dict, 4)  # ADDIU $a2, $r0, 1
    writeValue(ROM_COPY, 0x806AB31C, Overlay.Static, 0xA466C83C, offset_dict, 4)  # SH $a2, 0xC83C ($v1) | Overwrite trap func, Replace with overwrite of wheel segments
    writeValue(ROM_COPY, 0x8075056C, Overlay.Static, 201, offset_dict)  # Change GB Item cap to 201
    # In-Level IGT
    writeFunction(ROM_COPY, 0x8060DF28, Overlay.Static, "updateLevelIGT", offset_dict)
    # Modify Function Call
    writeFunction(ROM_COPY, 0x806ABB0C, Overlay.Static, "printLevelIGT", offset_dict)
    # Modify Function Call
    writeValue(ROM_COPY, 0x806ABB32, Overlay.Static, 106, offset_dict)  # Adjust kong name height
    # Disable Item Checks
    writeValue(ROM_COPY, 0x806AB2E8, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806AB360, Overlay.Static, 0, offset_dict, 4)
    writeValue(ROM_COPY, 0x806AB3E4, Overlay.Static, 0, offset_dict, 4)
    # Check blueprint count
    writeValue(ROM_COPY, 0x806ABFCE, Overlay.Static, ReqItems.Blueprint, offset_dict)
    writeValue(ROM_COPY, 0x806ABFD2, Overlay.Static, -1, offset_dict, 2, True)  # All levels
    writeValue(ROM_COPY, 0x806ABFD8, Overlay.Static, 0x2406FFFF, offset_dict, 4)  # All Kongs
    writeFunction(ROM_COPY, 0x806ABFD4, Overlay.Static, "getItemCount_new", offset_dict)
    #
    if IsDDMSSelected(settings.misc_changes_selected, MiscChangesSelected.fast_pause_transitions):
        writeFloat(ROM_COPY, 0x8075AC00, Overlay.Static, 1.3, offset_dict)  # Pause Menu Progression Rate
        writeValue(ROM_COPY, 0x806A901C, Overlay.Static, 4, offset_dict, 4)  # NOP - Remove thud
    writeFunction(ROM_COPY, 0x806A84C8, Overlay.Static, "updateFileVariables", offset_dict)  # Update file variables to transfer old locations to current
