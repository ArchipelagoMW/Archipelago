"""Write ASM data for the save file elements."""

import math
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.ASM import *

FileInfoSizes = [
    2,  # Melon Count
    1,  # File Populated
    0x16,  # IGT
    2,  # File Index
    0x18,  # Save Count
    8,  # DK BP
    8,  # Diddy BP
    8,  # Lanky BP
    8,  # Tiny BP
    8,  # Chunky BP
    8,  # DK Hints
    8,  # Diddy Hints
    8,  # Lanky Hints
    8,  # Tiny Hints
    8,  # Chunky Hints
    8,  # Keys
    8,  # Kongs
    8,  # Crown Count
    8,  # Special Items
    8,  # Medals
    8,  # Pearls
    8,  # Fairies
    8,  # Rainbow Coins
    16,  # Ice Traps
    16,  # Junk Items
    16,  # Race Coins
    8,  # Special Moves
    8,  # DK BP Turn-In
    8,  # Diddy BP Turn-In
    8,  # Lanky BP Turn-In
    8,  # Tiny BP Turn-In
    8,  # Chunky BP Turn-In
    16,  # AP Item Count
    22,  # IGT Japes
    22,  # IGT Aztec
    22,  # IGT Factory
    22,  # IGT Galleon
    22,  # IGT Fungi
    22,  # IGT Caves
    22,  # IGT Castle
    22,  # IGT Helm
    22,  # IGT Isles
    22,  # IGT DK
    22,  # IGT Diddy
    22,  # IGT Lanky
    22,  # IGT Tiny
    22,  # IGT Chunky
    22,  # Hurry IGT
    16,  # Tags
    12,  # Photos
    16,  # Kills
    12,  # Kaught
    12,  # Deaths
    12,  # Trapped
]


def expandSaveFile(ROM_COPY: LocalROM, static_expansion: int, actor_count: int, offset_dict: dict):
    """Expand Save file."""
    expansion = static_expansion + actor_count
    flag_block_size = 0x320 + expansion
    targ_gb_bits = 7  # Max 127
    GB_LEVEL_COUNT = 9
    COIN_BITS = 16
    added_bits = (targ_gb_bits - 3) * 8
    added_bits += targ_gb_bits + 7 + 7
    kong_var_size = 0xA1 + added_bits + (COIN_BITS - 8)
    file_info_location = flag_block_size + (5 * kong_var_size)
    file_default_size = file_info_location + 0x3F + sum(FileInfoSizes)
    # Flag Block Size
    writeValue(ROM_COPY, 0x8060E36A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060E31E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060E2C6, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D54A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D4A2, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D45E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D3C6, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D32E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060D23E, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060CF62, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060CC52, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060C78A, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060C352, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BF96, Overlay.Static, file_default_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BA7A, Overlay.Static, file_default_size, offset_dict)
    # Coin Bits
    writeValue(ROM_COPY, 0x8060BD5A, Overlay.Static, COIN_BITS, offset_dict)
    writeValue(ROM_COPY, 0x8060BD4E, Overlay.Static, COIN_BITS, offset_dict)

    writeValue(ROM_COPY, getSym("file_info_expansion"), Overlay.Custom, file_info_location, offset_dict)
    # Increase GB Storage Size
    writeValue(ROM_COPY, 0x8060BE12, Overlay.Static, targ_gb_bits, offset_dict)  # Bit Size
    writeValue(ROM_COPY, 0x8060BE06, Overlay.Static, targ_gb_bits * GB_LEVEL_COUNT, offset_dict)  # Allocation for all levels
    writeValue(ROM_COPY, 0x8060BE26, Overlay.Static, 0x40C0, offset_dict)  # SLL 2 -> SLL 3
    writeValue(ROM_COPY, 0x8060BCC0, Overlay.Static, 0x24090000 | kong_var_size, offset_dict, 4)  # ADDIU $t1, $r0, kong_var_size
    writeValue(ROM_COPY, 0x8060BCC4, Overlay.Static, 0x01C90019, offset_dict, 4)  # MULTU $t1, $t6
    writeValue(ROM_COPY, 0x8060BCC8, Overlay.Static, 0x00004812, offset_dict, 4)  # MFLO $t1
    writeValue(ROM_COPY, 0x8060BCCC, Overlay.Static, 0, offset_dict, 4)  # NOP
    writeValue(ROM_COPY, 0x8060BE3A, Overlay.Static, 7 * GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x8060BE6E, Overlay.Static, 7 * GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x8060DFDE, Overlay.Static, GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x8060DD42, Overlay.Static, GB_LEVEL_COUNT, offset_dict)
    writeValue(ROM_COPY, 0x806FB42E, Overlay.Static, int(math.ceil(GB_LEVEL_COUNT / 4) * 4), offset_dict)
    writeValue(ROM_COPY, 0x80029982, Overlay.Menu, int(math.ceil(GB_LEVEL_COUNT / 4) * 4), offset_dict)
    # Model 2 Start
    writeValue(ROM_COPY, 0x8060C2F2, Overlay.Static, flag_block_size, offset_dict)
    writeValue(ROM_COPY, 0x8060BCDE, Overlay.Static, flag_block_size, offset_dict)
    # Reallocate Balloons + Patches
    writeValue(ROM_COPY, 0x80688BCE, Overlay.Static, 0x320 + static_expansion, offset_dict)  # Reallocated to just before model 2 block
    # Shift save indexes
    save_index_offset = len(FileInfoSizes) - 5
    writeValue(ROM_COPY, 0x8060C386, Overlay.Static, 0x11 + save_index_offset, offset_dict)  # Check for index when reading params
    writeValue(ROM_COPY, 0x80024362, Overlay.Arcade, 0x15 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore
    writeValue(ROM_COPY, 0x8002437A, Overlay.Arcade, 0x12 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore Name 1
    writeValue(ROM_COPY, 0x80024396, Overlay.Arcade, 0x13 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore Name 2
    writeValue(ROM_COPY, 0x800243B2, Overlay.Arcade, 0x14 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore Name 3
    writeValue(ROM_COPY, 0x80024A5E, Overlay.Jetpac, 0x11 + save_index_offset, offset_dict)  # Save to File - Jetpac Hiscore
    writeValue(ROM_COPY, 0x8002D476, Overlay.Menu, 0x1E + save_index_offset, offset_dict)  # Save to File - Sound Type
    writeValue(ROM_COPY, 0x8002DAE6, Overlay.Menu, 0x1F + save_index_offset, offset_dict)  # Save to File - Language Type
    writeValue(ROM_COPY, 0x8002DB06, Overlay.Menu, 0x20 + save_index_offset, offset_dict)  # Save to File - Camera Type
    writeValue(ROM_COPY, 0x8002EE5A, Overlay.Menu, 0x19 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore
    writeValue(ROM_COPY, 0x8002EE72, Overlay.Menu, 0x16 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore Name 1
    writeValue(ROM_COPY, 0x8002EE8E, Overlay.Menu, 0x17 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore Name 2
    writeValue(ROM_COPY, 0x8002EEAA, Overlay.Menu, 0x18 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore Name 3
    writeValue(ROM_COPY, 0x8002EEC6, Overlay.Menu, 0x1D + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore
    writeValue(ROM_COPY, 0x8002EEE2, Overlay.Menu, 0x1A + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore Name 1
    writeValue(ROM_COPY, 0x8002EEFE, Overlay.Menu, 0x1B + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore Name 2
    writeValue(ROM_COPY, 0x8002EF1A, Overlay.Menu, 0x1C + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore Name 3
    writeValue(ROM_COPY, 0x8060C8DE, Overlay.Static, 0x11 + save_index_offset, offset_dict)  # Save to File - Jetpac Hiscore
    writeValue(ROM_COPY, 0x8060C91E, Overlay.Static, 0x15 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore
    writeValue(ROM_COPY, 0x8060C93A, Overlay.Static, 0x12 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore Name 1
    writeValue(ROM_COPY, 0x8060C956, Overlay.Static, 0x13 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore Name 2
    writeValue(ROM_COPY, 0x8060C972, Overlay.Static, 0x14 + save_index_offset, offset_dict)  # Save to File - Arcade Hiscore Name 3
    writeValue(ROM_COPY, 0x8060C9C2, Overlay.Static, 0x19 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore
    writeValue(ROM_COPY, 0x8060C9DA, Overlay.Static, 0x16 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore Name 1
    writeValue(ROM_COPY, 0x8060C9F6, Overlay.Static, 0x17 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore Name 2
    writeValue(ROM_COPY, 0x8060CA12, Overlay.Static, 0x18 + save_index_offset, offset_dict)  # Save to File - Rambi Hiscore Name 3
    writeValue(ROM_COPY, 0x8060CA7E, Overlay.Static, 0x1D + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore
    writeValue(ROM_COPY, 0x8060CA96, Overlay.Static, 0x1A + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore Name 1
    writeValue(ROM_COPY, 0x8060CAB2, Overlay.Static, 0x1B + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore Name 2
    writeValue(ROM_COPY, 0x8060CACE, Overlay.Static, 0x1C + save_index_offset, offset_dict)  # Save to File - Enguarde Hiscore Name 3
    writeValue(ROM_COPY, 0x8060CB12, Overlay.Static, 0x1E + save_index_offset, offset_dict)  # Save to File - Sound Type
    writeValue(ROM_COPY, 0x8060CB36, Overlay.Static, 0x1F + save_index_offset, offset_dict)  # Save to File - Language
    writeValue(ROM_COPY, 0x8060D046, Overlay.Static, 0x1F + save_index_offset, offset_dict)  # Save to File - Language
    writeValue(ROM_COPY, 0x8002444A, Overlay.Arcade, 0x15 + save_index_offset, offset_dict)  # Read from File - Arcade Hiscore
    writeValue(ROM_COPY, 0x8002445E, Overlay.Arcade, 0x12 + save_index_offset, offset_dict)  # Read from File - Arcade Hiscore Name 1
    writeValue(ROM_COPY, 0x80024476, Overlay.Arcade, 0x13 + save_index_offset, offset_dict)  # Read from File - Arcade Hiscore Name 2
    writeValue(ROM_COPY, 0x8002448E, Overlay.Arcade, 0x14 + save_index_offset, offset_dict)  # Read from File - Arcade Hiscore Name 3
    writeValue(ROM_COPY, 0x80024C06, Overlay.Jetpac, 0x11 + save_index_offset, offset_dict)  # Read from File - Jetpac Hiscore
    writeValue(ROM_COPY, 0x800251B2, Overlay.Jetpac, 0x11 + save_index_offset, offset_dict)  # Read from File - Jetpac Hiscore
    writeValue(ROM_COPY, 0x8002886E, Overlay.Menu, 0x1E + save_index_offset, offset_dict)  # Read from File - Sound Type
    writeValue(ROM_COPY, 0x8002D462, Overlay.Menu, 0x1E + save_index_offset, offset_dict)  # Read from File - Sound Type
    writeValue(ROM_COPY, 0x8002ED26, Overlay.Menu, 0x19 + save_index_offset, offset_dict)  # Read from File - Rambi Hiscore
    writeValue(ROM_COPY, 0x8002ED3A, Overlay.Menu, 0x16 + save_index_offset, offset_dict)  # Read from File - Rambi Hiscore Name 1
    writeValue(ROM_COPY, 0x8002ED52, Overlay.Menu, 0x17 + save_index_offset, offset_dict)  # Read from File - Rambi Hiscore Name 2
    writeValue(ROM_COPY, 0x8002ED6A, Overlay.Menu, 0x18 + save_index_offset, offset_dict)  # Read from File - Rambi Hiscore Name 3
    writeValue(ROM_COPY, 0x8060D006, Overlay.Static, 0x1F + save_index_offset, offset_dict)  # Read from File - Language
    writeValue(ROM_COPY, 0x8060D026, Overlay.Static, 0x20 + save_index_offset, offset_dict)  # Read from File - Camera Type
    # Offset clamping
    writeValue(ROM_COPY, 0x8060C432, Overlay.Static, -(0x11 + save_index_offset), offset_dict, 2, True)
    writeValue(ROM_COPY, 0x8060BFBA, Overlay.Static, -(0x11 + save_index_offset), offset_dict, 2, True)


def saveUpdates(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to a save file."""
    # Files
    balloon_patch_count = 150
    static_expansion = 0x140
    if settings.enemy_drop_rando:
        static_expansion += 428  # Total Enemies
    expandSaveFile(ROM_COPY, static_expansion, balloon_patch_count, offset_dict)
    # 1-File Fixes
    writeValue(ROM_COPY, 0x8060CF34, Overlay.Static, 0x240E0001, offset_dict, 4)  # Slot 1
    writeValue(ROM_COPY, 0x8060CF38, Overlay.Static, 0x240F0002, offset_dict, 4)  # Slot 2
    writeValue(ROM_COPY, 0x8060CF3C, Overlay.Static, 0x24180003, offset_dict, 4)  # Slot 3
    writeValue(ROM_COPY, 0x8060CF40, Overlay.Static, 0x240D0000, offset_dict, 4)  # Slot 0
    writeValue(ROM_COPY, 0x8060D3AC, Overlay.Static, 0, offset_dict, 4)  # Prevent EEPROM Shuffle
    writeValue(ROM_COPY, 0x8060DCE8, Overlay.Static, 0, offset_dict, 4)  # Prevent EEPROM Shuffle
    writeValue(ROM_COPY, 0x8060CD1A, Overlay.Static, 1, offset_dict)  # File Loop Cancel 2
    writeValue(ROM_COPY, 0x8060CE7E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 3
    writeValue(ROM_COPY, 0x8060CE5A, Overlay.Static, 1, offset_dict)  # File Loop Cancel 4
    writeValue(ROM_COPY, 0x8060CF0E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 5
    writeValue(ROM_COPY, 0x8060CF26, Overlay.Static, 1, offset_dict)  # File Loop Cancel 6
    writeValue(ROM_COPY, 0x8060D106, Overlay.Static, 1, offset_dict)  # File Loop Cancel 8
    writeValue(ROM_COPY, 0x8060D43E, Overlay.Static, 1, offset_dict)  # File Loop Cancel 8
    writeValue(ROM_COPY, 0x8060CD08, Overlay.Static, 0x26670000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060CE48, Overlay.Static, 0x26670000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060CF04, Overlay.Static, 0x26270000, offset_dict, 4)  # Save to File - File Index
    writeValue(ROM_COPY, 0x8060BFA4, Overlay.Static, 0x252A0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060E378, Overlay.Static, 0x258D0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D33C, Overlay.Static, 0x254B0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D470, Overlay.Static, 0x256C0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D4B0, Overlay.Static, 0x252A0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D558, Overlay.Static, 0x258D0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060CF74, Overlay.Static, 0x25090000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060D24C, Overlay.Static, 0x25AE0000, offset_dict, 4)  # Global Block after 1 file entry
    writeValue(ROM_COPY, 0x8060C84C, Overlay.Static, 0xA02067C8, offset_dict, 4)  # Force file 0
    writeValue(ROM_COPY, 0x8060C654, Overlay.Static, 0x24040000, offset_dict, 4)  # Force file 0 - Save
    writeValue(ROM_COPY, 0x8060C664, Overlay.Static, 0xAFA00034, offset_dict, 4)  # Force file 0 - Save
    writeValue(ROM_COPY, 0x8060C6C4, Overlay.Static, 0x24040000, offset_dict, 4)  # Force file 0 - Read
    writeValue(ROM_COPY, 0x8060C6D4, Overlay.Static, 0xAFA00034, offset_dict, 4)  # Force file 0 - Read
    writeValue(ROM_COPY, 0x8060D294, Overlay.Static, 0, offset_dict, 4)  # Cartridge EEPROM Wipe cancel
    # File Select
    writeValue(ROM_COPY, 0x80028CB0, Overlay.Menu, 0xA0600000, offset_dict, 4)  # SB $r0, 0x0 (v0) - Always view file index 0
    writeValue(ROM_COPY, 0x80028CC4, Overlay.Menu, 0, offset_dict, 4)  # Prevent file index overwrite
    writeValue(ROM_COPY, 0x80028F88, Overlay.Menu, 0, offset_dict, 4)  # File 2 render
    writeValue(ROM_COPY, 0x80028F60, Overlay.Menu, 0, offset_dict, 4)  # File 2 Opacity
    writeValue(ROM_COPY, 0x80028FCC, Overlay.Menu, 0, offset_dict, 4)  # File 3 render
    writeValue(ROM_COPY, 0x80028FA4, Overlay.Menu, 0, offset_dict, 4)  # File 3 Opacity
    writeValue(ROM_COPY, 0x80028DB8, Overlay.Menu, 0x1040000A, offset_dict, 4)  # BEQ $v0, $r0, 0xA - Change text signal
    writeValue(ROM_COPY, 0x80028CA6, Overlay.Menu, 5, offset_dict)  # Change selecting orange to delete confirm screen
    #
    writeHook(ROM_COPY, 0x8060DFF4, Overlay.Static, "SaveToFileFixes", offset_dict)
    # EEPROM Patch
    writeValue(ROM_COPY, 0x8060D588, Overlay.Static, 0, offset_dict, 4)  # NOP
    # TEMPORARY FIX FOR SAVE BUG
    writeValue(ROM_COPY, 0x8060D790, Overlay.Static, 0, offset_dict, 4)  # NOP

    writeFunction(ROM_COPY, 0x8060DD18, Overlay.Static, "readItemsFromFile", offset_dict)
    writeFunction(ROM_COPY, 0x8060C3C8, Overlay.Static, "GrabFileParameters_FileInfo", offset_dict)
    # Save updates for dyn flags
    writeHook(ROM_COPY, 0x80631E3C, Overlay.Static, "dynflagcheck_3", offset_dict)
    writeHook(ROM_COPY, 0x80632140, Overlay.Static, "dynflagcheck_2", offset_dict)
    writeHook(ROM_COPY, 0x806F4990, Overlay.Static, "dynflagcheck_1", offset_dict)
    writeHook(ROM_COPY, 0x806F49EC, Overlay.Static, "dynflagcheck_0", offset_dict)
