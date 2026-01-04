import struct
import itertools
import re
import zlib
import zipfile
import os
import datetime
from collections import defaultdict
from functools import partial

from .Items import OOTItem
from .Location import DisableType
from .LocationList import business_scrubs
from .HintList import getHint
from .Hints import writeGossipStoneHints, buildAltarHints, \
        buildGanonText, getSimpleHintNoPrefix, HintArea, getItemGenericName, \
        buildMiscItemHints, buildMiscLocationHints
from .Utils import data_path
from .Messages import read_messages, update_message_by_id, read_shop_items, update_warp_song_text, \
        write_shop_items, remove_unused_messages, make_player_message, \
        add_item_messages, repack_messages, shuffle_messages, \
        get_message_by_id, Text_Code
from .MQ import patch_files, File, update_dmadata, insert_space, add_relocations
from .Rom import Rom
from .SaveContext import SaveContext, Scenes, FlagType
from .SceneFlags import get_alt_list_bytes, get_collectible_flag_table, get_collectible_flag_table_bytes, \
        get_collectible_flag_addresses
from .TextBox import character_table, NORMAL_LINE_WIDTH, rom_safe_text
from .texture_util import ci4_rgba16patch_to_ci8, rgba16_patch
from .Utils import __version__

from worlds.Files import APPatch
from Utils import __version__ as ap_version

AP_PROGRESSION = 0xD4
AP_JUNK = 0xD5


class OoTContainer(APPatch):
    game: str = 'Ocarina of Time'
    patch_file_ending = ".apz5"

    def __init__(self, patch_data: bytes, base_path: str, output_directory: str,
                 player = None, player_name: str = "", server: str = ""):
        self.patch_data = patch_data
        self.zpf_path = base_path + ".zpf"
        container_path = os.path.join(output_directory, base_path + ".apz5")
        super().__init__(container_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr(self.zpf_path, self.patch_data)
        super().write_contents(opened_zipfile)


# "Spoiler" argument deleted; can probably be replaced with calls to world.world
def patch_rom(world, rom):
    with open(data_path('generated/rom_patch.txt'), 'r') as stream:
        for line in stream:
            address, value = [int(x, 16) for x in line.split(',')]
            rom.write_int32(address, value)
    rom.scan_dmadata_update()

    # Write Randomizer title screen logo
    with open(data_path('title.bin'), 'rb') as stream:
        writeAddress = 0x01795300
        titleBytesComp = stream.read()
        titleBytesDiff = zlib.decompress(titleBytesComp)

        originalBytes = rom.original.buffer[writeAddress: writeAddress+ len(titleBytesDiff)]
        titleBytes = bytearray([a ^ b for a, b in zip(titleBytesDiff, originalBytes)])
        rom.write_bytes(writeAddress, titleBytes)

    # Fixes the typo of keatan mask in the item select screen
    with open(data_path('keaton.bin'), 'rb') as stream:
        writeAddress = 0x8A7C00
        keatonBytesComp = stream.read()
        keatonBytesDiff = zlib.decompress(keatonBytesComp)

        originalBytes = rom.original.buffer[writeAddress: writeAddress+ len(keatonBytesDiff)]
        keatonBytes = bytearray([a ^ b for a, b in zip(keatonBytesDiff, originalBytes)])
        rom.write_bytes(writeAddress, keatonBytes)

    # Load Triforce model into a file
    triforce_obj_file = File({ 'Name': 'object_gi_triforce' })
    triforce_obj_file.copy(rom)
    with open(data_path('Triforce.zobj'), 'rb') as stream:
        obj_data = stream.read()
        rom.write_bytes(triforce_obj_file.start, obj_data)
        triforce_obj_file.end = triforce_obj_file.start + len(obj_data)
    update_dmadata(rom, triforce_obj_file)
    # Add it to the extended object table
    add_to_extended_object_table(rom, 0x193, triforce_obj_file)

    # Build a Double Defense model from the Heart Container model
    dd_obj_file = File({
        'Name': 'object_gi_hearts',
        'Start': '014D9000',
        'End': '014DA590',
    })
    dd_obj_file.copy(rom)
    # Update colors for the Double Defense variant
    rom.write_bytes(dd_obj_file.start + 0x1294, [0xFF, 0xCF, 0x0F]) # Exterior Primary Color
    rom.write_bytes(dd_obj_file.start + 0x12B4, [0xFF, 0x46, 0x32]) # Exterior Env Color
    rom.write_int32s(dd_obj_file.start + 0x12A8, [0xFC173C60, 0x150C937F]) # Exterior Combine Mode
    rom.write_bytes(dd_obj_file.start + 0x1474, [0xFF, 0xFF, 0xFF]) # Interior Primary Color
    rom.write_bytes(dd_obj_file.start + 0x1494, [0xFF, 0xFF, 0xFF]) # Interior Env Color
    update_dmadata(rom, dd_obj_file)
    # Add it to the extended object table
    add_to_extended_object_table(rom, 0x194, dd_obj_file)

    # Load Key Ring model into a file
    keyring_obj_file = File({ 'Name': 'object_gi_keyring' })
    keyring_obj_file.copy(rom)
    with open(data_path('KeyRing.zobj'), 'rb') as stream:
        obj_data = stream.read()
        rom.write_bytes(keyring_obj_file.start, obj_data)
        keyring_obj_file.end = keyring_obj_file.start + len(obj_data)
    update_dmadata(rom, keyring_obj_file)
    # Add it to the extended object table
    add_to_extended_object_table(rom, 0x195, keyring_obj_file)

    # Create the textures for pots/crates. Note: No copyrighted material can be distributed w/ the randomizer. Because of this, patch files are used to create the new textures from the original texture in ROM.
    # Apply patches for custom textures for pots and crates and add as new files in rom
    # Crates are ci4 textures in the normal ROM but for pot/crate textures match contents were upgraded to ci8 to support more colors
    # Pot textures are rgba16
    # Get the texture table from rom (see textures.c)
    texture_table_start = rom.sym('texture_table') # Get the address of the texture table

    # texture list. See textures.h for texture IDs
    #   ID, texture_name,                   Rom Address    CI4 Pallet Addr  Size    Patching function                          Patch file (None for default)
    crate_textures = [
        (1, 'texture_pot_gold',             0x01738000,    None,            2048,   rgba16_patch,               'textures/pot/pot_gold_rgba16_patch.bin'),
        (2, 'texture_pot_key',              0x01738000,    None,            2048,   rgba16_patch,               'textures/pot/pot_key_rgba16_patch.bin'),
        (3, 'texture_pot_bosskey',          0x01738000,    None,            2048,   rgba16_patch,               'textures/pot/pot_bosskey_rgba16_patch.bin'),
        (4, 'texture_pot_skull',            0x01738000,    None,            2048,   rgba16_patch,               'textures/pot/pot_skull_rgba16_patch.bin'),
        (5, 'texture_crate_default',        0x18B6020,     0x018B6000,      4096,   ci4_rgba16patch_to_ci8,     None),
        (6, 'texture_crate_gold'   ,        0x18B6020,     0x018B6000,      4096,   ci4_rgba16patch_to_ci8,     'textures/crate/crate_gold_rgba16_patch.bin'),
        (7, 'texture_crate_key',            0x18B6020,     0x018B6000,      4096,   ci4_rgba16patch_to_ci8,     'textures/crate/crate_key_rgba16_patch.bin'),
        (8, 'texture_crate_skull',          0x18B6020,     0x018B6000,      4096,   ci4_rgba16patch_to_ci8,     'textures/crate/crate_skull_rgba16_patch.bin'),
        (9, 'texture_crate_bosskey',        0x18B6020,     0x018B6000,      4096,   ci4_rgba16patch_to_ci8,     'textures/crate/crate_bosskey_rgba16_patch.bin'),
        (10, 'texture_smallcrate_gold',     0xF7ECA0,      None,            2048,   rgba16_patch,               'textures/crate/smallcrate_gold_rgba16_patch.bin' ),
        (11, 'texture_smallcrate_key',      0xF7ECA0,      None,            2048,   rgba16_patch,               'textures/crate/smallcrate_key_rgba16_patch.bin'),
        (12, 'texture_smallcrate_skull',    0xF7ECA0,      None,            2048,   rgba16_patch,               'textures/crate/smallcrate_skull_rgba16_patch.bin'),
        (13, 'texture_smallcrate_bosskey',  0xF7ECA0,      None,            2048,   rgba16_patch,               'textures/crate/smallcrate_bosskey_rgba16_patch.bin')
    ]

    # Loop through the textures and apply the patch. Add the new texture as a new file in rom.
    for texture_id, texture_name, rom_address_base, rom_address_palette, size,func, patchfile in crate_textures:
        texture_file = File({'Name': texture_name}) # Create a new file for the texture
        texture_file.copy(rom) # Relocate this file to free space is the rom
        texture_data = func(rom, rom_address_base, rom_address_palette, size, data_path(patchfile) if patchfile else None) # Apply the texture patch. Resulting texture will be stored in texture_data as a bytearray
        rom.write_bytes(texture_file.start, texture_data) # write the bytes to our new file
        texture_file.end = texture_file.start + len(texture_data) # Get size of the new texture
        update_dmadata(rom, texture_file) # Update DMA table with new file

        # update the texture table with the rom addresses of the texture files
        entry = read_rom_texture(rom, texture_id)
        entry['file_vrom_start'] = texture_file.start
        entry['file_size'] = texture_file.end - texture_file.start
        write_rom_texture(rom, texture_id, entry)

    # Apply chest texture diffs to vanilla wooden chest texture for Chest Texture Matches Content setting
    # new texture, vanilla texture, num bytes
    textures = [(rom.sym('SILVER_CHEST_FRONT_TEXTURE'), 0xFEC798, 4096),
                (rom.sym('SILVER_CHEST_BASE_TEXTURE'), 0xFED798, 2048),
                (rom.sym('GILDED_CHEST_FRONT_TEXTURE'), 0xFEC798, 4096),
                (rom.sym('GILDED_CHEST_BASE_TEXTURE'), 0xFED798, 2048),
                (rom.sym('SKULL_CHEST_FRONT_TEXTURE'), 0xFEC798, 4096),
                (rom.sym('SKULL_CHEST_BASE_TEXTURE'), 0xFED798, 2048)]
    # Diff texture is the new texture minus the vanilla texture with byte overflow.
    # This is done to avoid distributing copyrighted material with the randomizer,
    # as the new textures are derivations of the wood chest textures.
    # The following rebuilds the texture from the diff.
    for diff_tex, vanilla_tex, size in textures:
        db = rom.read_bytes(diff_tex, size)
        vb = rom.read_bytes(vanilla_tex, size)
        # bytes are immutable in python, can't edit in place
        new_tex = bytearray(size)
        for i in range(len(vb)):
            new_tex[i] = (db[i] + vb[i]) & 0xFF
        rom.write_bytes(diff_tex, new_tex)

    # Create an option so that recovery hearts no longer drop by changing the code which checks Link's health when an item is spawned.
    if world.no_collectible_hearts:
        symbol = rom.sym('NO_COLLECTIBLE_HEARTS')
        rom.write_byte(symbol, 0x01)

    # Remove color commands inside certain object display lists
    rom.write_int32s(0x1455818, [0x00000000, 0x00000000, 0x00000000, 0x00000000]) # Small Key
    rom.write_int32s(0x14B9F20, [0x00000000, 0x00000000, 0x00000000, 0x00000000]) # Boss Key

    # Set default targeting option to Hold. I got fed up enough with this that I made it a main option
    if world.default_targeting == 'hold':
        rom.write_byte(0xB71E6D, 0x01)
    else:
        rom.write_byte(0xB71E6D, 0x00)

    # Force language to be English in the event a Japanese rom was submitted
    rom.write_byte(0x3E, 0x45)
    rom.force_patch.append(0x3E)

    # Increase the instance size of Bombchus prevent the heap from becoming corrupt when
    # a Dodongo eats a Bombchu. Does not fix stale pointer issues with the animation
    rom.write_int32(0xD6002C, 0x1F0)

    # Can always return to youth
    rom.write_byte(0xCB6844, 0x35)
    rom.write_byte(0x253C0E2, 0x03) # Moves sheik from pedestal

    # Fix Ice Cavern Alcove Camera
    if not world.dungeon_mq['Ice Cavern']:
        rom.write_byte(0x2BECA25,0x01)
        rom.write_byte(0x2BECA2D,0x01)

    # Fix GS rewards to be static
    rom.write_int32(0xEA3934, 0)
    rom.write_bytes(0xEA3940, [0x10, 0x00])

    # Fix horseback archery rewards to be static
    rom.write_byte(0xE12BA5, 0x00)
    rom.write_byte(0xE12ADD, 0x00)

    # Fix deku theater rewards to be static
    rom.write_bytes(0xEC9A7C, [0x00, 0x00, 0x00, 0x00]) #Sticks
    rom.write_byte(0xEC9CD5, 0x00) #Nuts

    # Fix deku scrub who sells stick upgrade
    rom.write_bytes(0xDF8060, [0x00, 0x00, 0x00, 0x00])

    # Fix deku scrub who sells nut upgrade
    rom.write_bytes(0xDF80D4, [0x00, 0x00, 0x00, 0x00])

    # Fix rolling goron as child reward to be static
    rom.write_bytes(0xED2960, [0x00, 0x00, 0x00, 0x00])

    # Fix proximity text boxes (Navi) (Part 1)
    rom.write_bytes(0xDF8B84, [0x00, 0x00, 0x00, 0x00])

    # Fix final magic bean to cost 99
    rom.write_byte(0xE20A0F, 0x63)
    rom.write_bytes(0x94FCDD, [0x08, 0x39, 0x39])

    # Remove locked door to Boss Key Chest in Fire Temple
    if not world.keysanity and not world.dungeon_mq['Fire Temple']:
        rom.write_byte(0x22D82B7, 0x3F)
    # Remove the unused locked door in water temple
    if not world.dungeon_mq['Water Temple']:
        rom.write_byte(0x25B8197, 0x3F)

    if world.bombchus_in_logic:
        rom.write_int32(rom.sym('BOMBCHUS_IN_LOGIC'), 1)

    # show seed info on file select screen
    def makebytes(txt, size):
        _bytes = list(ord(c) for c in txt[:size-1]) + [0] * size
        return _bytes[:size]

    def truncstr(txt, size):
        if len(txt) > size:
            txt = txt[:size-3] + "..."
        return txt

    line_len = 21
    version_str = "version " + __version__
    if len(version_str) > line_len:
        version_str = "ver. " + __version__
    rom.write_bytes(rom.sym('VERSION_STRING_TXT'), makebytes(version_str, 25))

    if world.multiworld.players > 1:
        world_str = f"{world.player} of {world.multiworld.players}"
    else:
        world_str = ""
    rom.write_bytes(rom.sym('WORLD_STRING_TXT'), makebytes(world_str, 12))

    time_str = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " UTC"
    rom.write_bytes(rom.sym('TIME_STRING_TXT'), makebytes(time_str, 25))

    rom.write_byte(rom.sym('CFG_SHOW_SETTING_INFO'), 0x01)

    msg = [f"Archipelago {ap_version}", world.multiworld.get_player_name(world.player)]
    for idx,part in enumerate(msg):
        part_bytes = list(ord(c) for c in part) + [0] * (line_len+1)
        part_bytes = part_bytes[:(line_len+1)]
        symbol = rom.sym('CFG_CUSTOM_MESSAGE_{}'.format(idx+1))
        rom.write_bytes(symbol, part_bytes)

    # Change graveyard graves to not allow grabbing on to the ledge
    rom.write_byte(0x0202039D, 0x20)
    rom.write_byte(0x0202043C, 0x24)


    # Fix Castle Courtyard to check for meeting Zelda, not Zelda fleeing, to block you
    rom.write_bytes(0xCD5E76, [0x0E, 0xDC])
    rom.write_bytes(0xCD5E12, [0x0E, 0xDC])

    # Cutscene for all medallions never triggers when leaving shadow or spirit temples(hopefully stops warp to colossus on shadow completion with boss reward shuffle)
    rom.write_byte(0xACA409, 0xAD)
    rom.write_byte(0xACA49D, 0xCE)

    # Speed Zelda's Letter scene
    rom.write_bytes(0x290E08E, [0x05, 0xF0])
    rom.write_byte(0xEFCBA7, 0x08)
    rom.write_byte(0xEFE7C7, 0x05)
    #rom.write_byte(0xEFEAF7, 0x08)
    #rom.write_byte(0xEFE7C7, 0x05)
    rom.write_bytes(0xEFE938, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xEFE948, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xEFE950, [0x00, 0x00, 0x00, 0x00])

    # Speed Zelda escaping from Hyrule Castle
    Block_code = [0x00, 0x00, 0x00, 0x01, 0x00, 0x21, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02]
    rom.write_bytes(0x1FC0CF8, Block_code)

    # songs as items flag
    songs_as_items = (world.shuffle_song_items != 'song') or world.songs_as_items

    if songs_as_items:
        rom.write_byte(rom.sym('SONGS_AS_ITEMS'), 1)

    # Speed learning Zelda's Lullaby
    rom.write_int32s(0x02E8E90C, [0x000003E8, 0x00000001]) # Terminator Execution
    if songs_as_items:
        rom.write_int16s(None, [0x0073, 0x001, 0x0002, 0x0002]) # ID, start, end, end
    else:
        rom.write_int16s(None, [0x0073, 0x003B, 0x003C, 0x003C]) # ID, start, end, end


    rom.write_int32s(0x02E8E91C, [0x00000013, 0x0000000C]) # Textbox, Count
    if songs_as_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x0017, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x00D4, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Sun's Song
    if songs_as_items:
        rom.write_int32(0x0332A4A4, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x0332A4A4, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x0332A868, [0x00000013, 0x00000008]) # Textbox, Count
    rom.write_int16s(None, [0x0018, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x00D3, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Saria's Song
    if songs_as_items:
        rom.write_int32(0x020B1734, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x020B1734, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x20B1DA8, [0x00000013, 0x0000000C]) # Textbox, Count
    rom.write_int16s(None, [0x0015, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x00D1, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x020B19C0, [0x0000000A, 0x00000006]) # Link, Count
    rom.write_int16s(0x020B19C8, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x020B19F8, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????
    rom.write_int32s(None,         [0x80000000,                          # ???
                                     0x00000000, 0x000001D4, 0xFFFFF731,  # start_XYZ
                                     0x00000000, 0x000001D4, 0xFFFFF712]) # end_XYZ

    # Speed learning Epona's Song
    rom.write_int32s(0x029BEF60, [0x000003E8, 0x00000001]) # Terminator Execution
    if songs_as_items:
        rom.write_int16s(None, [0x005E, 0x0001, 0x0002, 0x0002]) # ID, start, end, end
    else:
        rom.write_int16s(None, [0x005E, 0x000A, 0x000B, 0x000B]) # ID, start, end, end

    rom.write_int32s(0x029BECB0, [0x00000013, 0x00000002]) # Textbox, Count
    if songs_as_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0009, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x00D2, 0x0000, 0x0009, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0xFFFF, 0x000A, 0x003C, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Song of Time
    rom.write_int32s(0x0252FB98, [0x000003E8, 0x00000001]) # Terminator Execution
    if songs_as_items:
        rom.write_int16s(None, [0x0035, 0x0001, 0x0002, 0x0002]) # ID, start, end, end
    else:
        rom.write_int16s(None, [0x0035, 0x003B, 0x003C, 0x003C]) # ID, start, end, end

    rom.write_int32s(0x0252FC80, [0x00000013, 0x0000000C]) # Textbox, Count
    if songs_as_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x0019, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x00D5, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32(0x01FC3B84, 0xFFFFFFFF) # Other Header?: frame_count

    # Speed learning Song of Storms
    if songs_as_items:
        rom.write_int32(0x03041084, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x03041084, 0x0000000A) # Header: frame_count

    rom.write_int32s(0x03041088, [0x00000013, 0x00000002]) # Textbox, Count
    rom.write_int16s(None, [0x00D6, 0x0000, 0x0009, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0xFFFF, 0x00BE, 0x00C8, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    # Speed learning Minuet of Forest
    if songs_as_items:
        rom.write_int32(0x020AFF84, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x020AFF84, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x020B0800, [0x00000013, 0x0000000A]) # Textbox, Count
    rom.write_int16s(None, [0x000F, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0073, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x020AFF88, [0x0000000A, 0x00000005]) # Link, Count
    rom.write_int16s(0x020AFF90, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x020AFFC1, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x020B0488, [0x00000056, 0x00000001]) # Music Change, Count
    rom.write_int16s(None, [0x003F, 0x0021, 0x0022, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x020B04C0, [0x0000007C, 0x00000001]) # Music Fade Out, Count
    rom.write_int16s(None, [0x0004, 0x0000, 0x0000, 0x0000]) #action, start, end, ????

    # Speed learning Bolero of Fire
    if songs_as_items:
        rom.write_int32(0x0224B5D4, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x0224B5D4, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x0224D7E8, [0x00000013, 0x0000000A]) # Textbox, Count
    rom.write_int16s(None, [0x0010, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0074, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x0224B5D8, [0x0000000A, 0x0000000B]) # Link, Count
    rom.write_int16s(0x0224B5E0, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x0224B610, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x0224B7F0, [0x0000002F, 0x0000000E]) # Sheik, Count
    rom.write_int16s(0x0224B7F8, [0x0000]) #action
    rom.write_int16s(0x0224B828, [0x0000]) #action
    rom.write_int16s(0x0224B858, [0x0000]) #action
    rom.write_int16s(0x0224B888, [0x0000]) #action

    # Speed learning Serenade of Water
    if songs_as_items:
        rom.write_int32(0x02BEB254, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x02BEB254, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x02BEC880, [0x00000013, 0x00000010]) # Textbox, Count
    rom.write_int16s(None, [0x0011, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0075, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x02BEB258, [0x0000000A, 0x0000000F]) # Link, Count
    rom.write_int16s(0x02BEB260, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int16s(0x02BEB290, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x02BEB530, [0x0000002F, 0x00000006]) # Sheik, Count
    rom.write_int16s(0x02BEB538, [0x0000, 0x0000, 0x018A, 0x0000]) #action, start, end, ????
    rom.write_int32s(None,         [0x1BBB0000,                          # ???
                                     0xFFFFFB10, 0x8000011A, 0x00000330,  # start_XYZ
                                     0xFFFFFB10, 0x8000011A, 0x00000330]) # end_XYZ

    rom.write_int32s(0x02BEC848, [0x00000056, 0x00000001]) # Music Change, Count
    rom.write_int16s(None, [0x0059, 0x0021, 0x0022, 0x0000]) #action, start, end, ????

    # Speed learning Nocturne of Shadow
    rom.write_int32s(0x01FFE458, [0x000003E8, 0x00000001]) # Other Scene? Terminator Execution
    rom.write_int16s(None, [0x002F, 0x0001, 0x0002, 0x0002]) # ID, start, end, end

    rom.write_int32(0x01FFFDF4, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x02000FD8, [0x00000013, 0x0000000E]) # Textbox, Count
    if songs_as_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x0013, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0077, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x02000128, [0x000003E8, 0x00000001]) # Terminator Execution
    if songs_as_items:
        rom.write_int16s(None, [0x0032, 0x0001, 0x0002, 0x0002]) # ID, start, end, end
    else:
        rom.write_int16s(None, [0x0032, 0x003A, 0x003B, 0x003B]) # ID, start, end, end

    # Speed learning Requiem of Spirit
    rom.write_int32(0x0218AF14, 0x0000003C) # Header: frame_count

    rom.write_int32s(0x0218C574, [0x00000013, 0x00000008]) # Textbox, Count
    if songs_as_items:
        rom.write_int16s(None, [0xFFFF, 0x0000, 0x0010, 0xFFFF, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2
    else:
        rom.write_int16s(None, [0x0012, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0076, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x0218B478, [0x000003E8, 0x00000001]) # Terminator Execution
    if songs_as_items:
        rom.write_int16s(None, [0x0030, 0x0001, 0x0002, 0x0002]) # ID, start, end, end
    else:
        rom.write_int16s(None, [0x0030, 0x003A, 0x003B, 0x003B]) # ID, start, end, end

    rom.write_int32s(0x0218AF18, [0x0000000A, 0x0000000B]) # Link, Count
    rom.write_int16s(0x0218AF20, [0x0011, 0x0000, 0x0010, 0x0000]) #action, start, end, ????
    rom.write_int32s(None,         [0x40000000,                          # ???
                                     0xFFFFFAF9, 0x00000008, 0x00000001,  # start_XYZ
                                     0xFFFFFAF9, 0x00000008, 0x00000001,  # end_XYZ
                                     0x0F671408, 0x00000000, 0x00000001]) # normal_XYZ
    rom.write_int16s(0x0218AF50, [0x003E, 0x0011, 0x0020, 0x0000]) #action, start, end, ????

    # Speed learning Prelude of Light
    if songs_as_items:
        rom.write_int32(0x0252FD24, 0xFFFFFFFF) # Header: frame_count
    else:
        rom.write_int32(0x0252FD24, 0x0000004A) # Header: frame_count

    rom.write_int32s(0x02531320, [0x00000013, 0x0000000E]) # Textbox, Count
    rom.write_int16s(None, [0x0014, 0x0000, 0x0010, 0x0002, 0x088B, 0xFFFF]) # ID, start, end, type, alt1, alt2
    rom.write_int16s(None, [0x0078, 0x0011, 0x0020, 0x0000, 0xFFFF, 0xFFFF]) # ID, start, end, type, alt1, alt2

    rom.write_int32s(0x0252FF10, [0x0000002F, 0x00000009]) # Sheik, Count
    rom.write_int16s(0x0252FF18, [0x0006, 0x0000, 0x0000, 0x0000]) #action, start, end, ????

    rom.write_int32s(0x025313D0, [0x00000056, 0x00000001]) # Music Change, Count
    rom.write_int16s(None, [0x003B, 0x0021, 0x0022, 0x0000]) #action, start, end, ????

    # Speed scene after Deku Tree
    rom.write_bytes(0x2077E20, [0x00, 0x07, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0x2078A10, [0x00, 0x0E, 0x00, 0x1F, 0x00, 0x20, 0x00, 0x20])
    Block_code = [0x00, 0x80, 0x00, 0x00, 0x00, 0x1E, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
                  0xFF, 0xFF, 0x00, 0x1E, 0x00, 0x28, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    rom.write_bytes(0x2079570, Block_code)

    # Speed scene after Dodongo's Cavern
    rom.write_bytes(0x2221E88, [0x00, 0x0C, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0x2223308, [0x00, 0x81, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed scene after Jabu Jabu's Belly
    rom.write_bytes(0xCA3530, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x2113340, [0x00, 0x0D, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0x2113C18, [0x00, 0x82, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])
    rom.write_bytes(0x21131D0, [0x00, 0x01, 0x00, 0x00, 0x00, 0x3C, 0x00, 0x3C])

    # Speed scene after Forest Temple
    rom.write_bytes(0xD4ED68, [0x00, 0x45, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD4ED78, [0x00, 0x3E, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])
    rom.write_bytes(0x207B9D4, [0xFF, 0xFF, 0xFF, 0xFF])

    # Speed scene after Fire Temple
    rom.write_bytes(0x2001848, [0x00, 0x1E, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0xD100B4, [0x00, 0x62, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD10134, [0x00, 0x3C, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed scene after Water Temple
    rom.write_bytes(0xD5A458, [0x00, 0x15, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD5A3A8, [0x00, 0x3D, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])
    rom.write_bytes(0x20D0D20, [0x00, 0x29, 0x00, 0xC7, 0x00, 0xC8, 0x00, 0xC8])

    # Speed scene after Shadow Temple
    rom.write_bytes(0xD13EC8, [0x00, 0x61, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD13E18, [0x00, 0x41, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed scene after Spirit Temple
    rom.write_bytes(0xD3A0A8, [0x00, 0x60, 0x00, 0x3B, 0x00, 0x3C, 0x00, 0x3C])
    rom.write_bytes(0xD39FF0, [0x00, 0x3F, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00])

    # Speed Nabooru defeat scene
    rom.write_bytes(0x2F5AF84, [0x00, 0x00, 0x00, 0x05])
    rom.write_bytes(0x2F5C7DA, [0x00, 0x01, 0x00, 0x02])
    rom.write_bytes(0x2F5C7A2, [0x00, 0x03, 0x00, 0x04])
    rom.write_byte(0x2F5B369, 0x09)
    rom.write_byte(0x2F5B491, 0x04)
    rom.write_byte(0x2F5B559, 0x04)
    rom.write_byte(0x2F5B621, 0x04)
    rom.write_byte(0x2F5B761, 0x07)
    rom.write_bytes(0x2F5B840, [0x00, 0x05, 0x00, 0x01, 0x00, 0x05, 0x00, 0x05]) #shorten white flash

    # Speed scene with all medallions
    rom.write_bytes(0x2512680, [0x00, 0x74, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])

    # Speed collapse of Ganon's Tower
    rom.write_bytes(0x33FB328, [0x00, 0x76, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])

    # Speed Phantom Ganon defeat scene
    rom.write_bytes(0xC944D8, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC94548, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC94730, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC945A8, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xC94594, [0x00, 0x00, 0x00, 0x00])

    # Speed Twinrova defeat scene
    rom.write_bytes(0xD678CC, [0x24, 0x01, 0x03, 0xA2, 0xA6, 0x01, 0x01, 0x42])
    rom.write_bytes(0xD67BA4, [0x10, 0x00])

    # Speed scenes during final battle
    # Ganondorf battle end
    rom.write_byte(0xD82047, 0x09)
    # Zelda descends
    rom.write_byte(0xD82AB3, 0x66)
    rom.write_byte(0xD82FAF, 0x65)
    rom.write_int16s(0xD82D2E, [0x041F])
    rom.write_int16s(0xD83142, [0x006B])
    rom.write_bytes(0xD82DD8, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xD82ED4, [0x00, 0x00, 0x00, 0x00])
    rom.write_byte(0xD82FDF, 0x33)
    # After tower collapse
    rom.write_byte(0xE82E0F, 0x04)
    # Ganon intro
    rom.write_bytes(0xE83D28, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xE83B5C, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xE84C80, [0x10, 0x00])

    # Speed completion of the trials in Ganon's Castle
    rom.write_int16s(0x31A8090, [0x006B, 0x0001, 0x0002, 0x0002]) #Forest
    rom.write_int16s(0x31A9E00, [0x006E, 0x0001, 0x0002, 0x0002]) #Fire
    rom.write_int16s(0x31A8B18, [0x006C, 0x0001, 0x0002, 0x0002]) #Water
    rom.write_int16s(0x31A9430, [0x006D, 0x0001, 0x0002, 0x0002]) #Shadow
    rom.write_int16s(0x31AB200, [0x0070, 0x0001, 0x0002, 0x0002]) #Spirit
    rom.write_int16s(0x31AA830, [0x006F, 0x0001, 0x0002, 0x0002]) #Light

    # Speed obtaining Fairy Ocarina
    rom.write_bytes(0x2151230, [0x00, 0x72, 0x00, 0x3C, 0x00, 0x3D, 0x00, 0x3D])
    Block_code = [0x00, 0x4A, 0x00, 0x00, 0x00, 0x3A, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
                  0xFF, 0xFF, 0x00, 0x3C, 0x00, 0x81, 0xFF, 0xFF]
    rom.write_bytes(0x2151240, Block_code)
    rom.write_bytes(0x2150E20, [0xFF, 0xFF, 0xFA, 0x4C])

    if world.shuffle_ocarinas:
        symbol = rom.sym('OCARINAS_SHUFFLED')
        rom.write_byte(symbol,0x01)

    # Speed Zelda Light Arrow cutscene
    rom.write_bytes(0x2531B40, [0x00, 0x28, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0x2532FBC, [0x00, 0x75])
    rom.write_bytes(0x2532FEA, [0x00, 0x75, 0x00, 0x80])
    rom.write_byte(0x2533115, 0x05)
    rom.write_bytes(0x2533141, [0x06, 0x00, 0x06, 0x00, 0x10])
    rom.write_bytes(0x2533171, [0x0F, 0x00, 0x11, 0x00, 0x40])
    rom.write_bytes(0x25331A1, [0x07, 0x00, 0x41, 0x00, 0x65])
    rom.write_bytes(0x2533642, [0x00, 0x50])
    rom.write_byte(0x253389D, 0x74)
    rom.write_bytes(0x25338A4, [0x00, 0x72, 0x00, 0x75, 0x00, 0x79])
    rom.write_bytes(0x25338BC, [0xFF, 0xFF])
    rom.write_bytes(0x25338C2, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
    rom.write_bytes(0x25339C2, [0x00, 0x75, 0x00, 0x76])
    rom.write_bytes(0x2533830, [0x00, 0x31, 0x00, 0x81, 0x00, 0x82, 0x00, 0x82])

    # Speed Bridge of Light cutscene
    rom.write_bytes(0x292D644, [0x00, 0x00, 0x00, 0xA0])
    rom.write_bytes(0x292D680, [0x00, 0x02, 0x00, 0x0A, 0x00, 0x6C, 0x00, 0x00])
    rom.write_bytes(0x292D6E8, [0x00, 0x27])
    rom.write_bytes(0x292D718, [0x00, 0x32])
    rom.write_bytes(0x292D810, [0x00, 0x02, 0x00, 0x3C])
    rom.write_bytes(0x292D924, [0xFF, 0xFF, 0x00, 0x14, 0x00, 0x96, 0xFF, 0xFF])

    #Speed Pushing of All Pushable Objects
    rom.write_bytes(0xDD2B86, [0x40, 0x80])             #block speed
    rom.write_bytes(0xDD2D26, [0x00, 0x01])             #block delay
    rom.write_bytes(0xDD9682, [0x40, 0x80])             #milk crate speed
    rom.write_bytes(0xDD981E, [0x00, 0x01])             #milk crate delay
    rom.write_bytes(0xCE1BD0, [0x40, 0x80, 0x00, 0x00]) #amy puzzle speed
    rom.write_bytes(0xCE0F0E, [0x00, 0x01])             #amy puzzle delay
    rom.write_bytes(0xC77CA8, [0x40, 0x80, 0x00, 0x00]) #fire block speed
    rom.write_bytes(0xC770C2, [0x00, 0x01])             #fire block delay
    rom.write_bytes(0xCC5DBC, [0x29, 0xE1, 0x00, 0x01]) #forest basement puzzle delay
    rom.write_bytes(0xDBCF70, [0x2B, 0x01, 0x00, 0x00]) #spirit cobra mirror startup
    rom.write_bytes(0xDBCF70, [0x2B, 0x01, 0x00, 0x01]) #spirit cobra mirror delay
    rom.write_bytes(0xDBA230, [0x28, 0x41, 0x00, 0x19]) #truth spinner speed
    rom.write_bytes(0xDBA3A4, [0x24, 0x18, 0x00, 0x00]) #truth spinner delay

    #Speed Deku Seed Upgrade Scrub Cutscene
    rom.write_bytes(0xECA900, [0x24, 0x03, 0xC0, 0x00]) #scrub angle
    rom.write_bytes(0xECAE90, [0x27, 0x18, 0xFD, 0x04]) #skip straight to giving item
    rom.write_bytes(0xECB618, [0x25, 0x6B, 0x00, 0xD4]) #skip straight to digging back in
    rom.write_bytes(0xECAE70, [0x00, 0x00, 0x00, 0x00]) #never initialize cs camera
    rom.write_bytes(0xE5972C, [0x24, 0x08, 0x00, 0x01]) #timer set to 1 frame for giving item

    # Remove remaining owls
    rom.write_bytes(0x1FE30CE, [0x01, 0x4B])
    rom.write_bytes(0x1FE30DE, [0x01, 0x4B])
    rom.write_bytes(0x1FE30EE, [0x01, 0x4B])
    rom.write_bytes(0x205909E, [0x00, 0x3F])
    rom.write_byte(0x2059094, 0x80)

    # Darunia won't dance
    rom.write_bytes(0x22769E4, [0xFF, 0xFF, 0xFF, 0xFF])

    # Zora moves quickly
    rom.write_bytes(0xE56924, [0x00, 0x00, 0x00, 0x00])

    # Speed Jabu Jabu swallowing Link
    rom.write_bytes(0xCA0784, [0x00, 0x18, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])

    # Ruto no longer points to Zora Sapphire
    rom.write_bytes(0xD03BAC, [0xFF, 0xFF, 0xFF, 0xFF])

    # Ruto never disappears from Jabu Jabu's Belly
    rom.write_byte(0xD01EA3, 0x00)

    #Shift octorock in jabu forward
    rom.write_bytes(0x275906E, [0xFF, 0xB3, 0xFB, 0x20, 0xF9, 0x56])

    #Move fire/forest temple switches down 1 unit to make it easier to press
    rom.write_bytes(0x24860A8, [0xFC, 0xF4]) #forest basement 1
    rom.write_bytes(0x24860C8, [0xFC, 0xF4]) #forest basement 2
    rom.write_bytes(0x24860E8, [0xFC, 0xF4]) #forest basement 3
    rom.write_bytes(0x236C148, [0x11, 0x93]) #fire hammer room

    # Speed up Epona race start
    rom.write_bytes(0x29BE984, [0x00, 0x00, 0x00, 0x02])
    rom.write_bytes(0x29BE9CA, [0x00, 0x01, 0x00, 0x02])

    # Speed start of Horseback Archery
    #rom.write_bytes(0x21B2064, [0x00, 0x00, 0x00, 0x02])
    #rom.write_bytes(0x21B20AA, [0x00, 0x01, 0x00, 0x02])

    # Speed up Epona escape
    rom.write_bytes(0x1FC8B36, [0x00, 0x2A])

    # Speed up draining the well
    rom.write_bytes(0xE0A010, [0x00, 0x2A, 0x00, 0x01, 0x00, 0x02, 0x00, 0x02])
    rom.write_bytes(0x2001110, [0x00, 0x2B, 0x00, 0xB7, 0x00, 0xB8, 0x00, 0xB8])

    # Speed up opening the royal tomb for both child and adult
    rom.write_bytes(0x2025026, [0x00, 0x01])
    rom.write_bytes(0x2023C86, [0x00, 0x01])
    rom.write_byte(0x2025159, 0x02)
    rom.write_byte(0x2023E19, 0x02)

    #Speed opening of Door of Time
    rom.write_bytes(0xE0A176, [0x00, 0x02])
    rom.write_bytes(0xE0A35A, [0x00, 0x01, 0x00, 0x02])

    # Speed up Lake Hylia Owl Flight
    rom.write_bytes(0x20E60D2, [0x00, 0x01])

    # Speed up Death Mountain Trail Owl Flight
    rom.write_bytes(0x223B6B2, [0x00, 0x01])

    # Speed up magic arrow equips
    rom.write_int16(0xBB84CE, 0x0000) # Skips the initial growing glowing orb phase
    rom.write_byte(0xBB84B7, 0xFF) # Set glowing orb above magic arrow to be small sized immediately
    rom.write_byte(0xBB84CB, 0x01) # Sets timer for holding icon above magic arrow (1 frame)
    rom.write_byte(0xBB7E67, 0x04) # speed up magic arrow icon -> bow icon interpolation (4 frames)
    rom.write_byte(0xBB8957, 0x01) # Sets timer for holding icon above bow (1 frame)
    rom.write_byte(0xBB854B, 0x05) # speed up bow icon -> c button interpolation (5 frames)

    # Poacher's Saw no longer messes up Forest Stage
    rom.write_bytes(0xAE72CC, [0x00, 0x00, 0x00, 0x00])

    # Change Prelude CS to check for medallion
    rom.write_bytes(0x00C805E6, [0x00, 0xA6])
    rom.write_bytes(0x00C805F2, [0x00, 0x01])

    # Change Nocturne CS to check for medallions
    rom.write_bytes(0x00ACCD8E, [0x00, 0xA6])
    rom.write_bytes(0x00ACCD92, [0x00, 0x01])
    rom.write_bytes(0x00ACCD9A, [0x00, 0x02])
    rom.write_bytes(0x00ACCDA2, [0x00, 0x04])

    # Change King Zora to move even if Zora Sapphire is in inventory
    rom.write_bytes(0x00E55BB0, [0x85, 0xCE, 0x8C, 0x3C])
    rom.write_bytes(0x00E55BB4, [0x84, 0x4F, 0x0E, 0xDA])

    # Remove extra Forest Temple medallions
    rom.write_bytes(0x00D4D37C, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Fire Temple medallions
    rom.write_bytes(0x00AC9754, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x00D0DB8C, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Water Temple medallions
    rom.write_bytes(0x00D57F94, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Spirit Temple medallions
    rom.write_bytes(0x00D370C4, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0x00D379C4, [0x00, 0x00, 0x00, 0x00])

    # Remove extra Shadow Temple medallions
    rom.write_bytes(0x00D116E0, [0x00, 0x00, 0x00, 0x00])

    # Change Mido, Saria, and Kokiri to check for Deku Tree complete flag
    # bitwise pointer for 0x80
    kokiriAddresses = [0xE52836, 0xE53A56, 0xE51D4E, 0xE51F3E, 0xE51D96, 0xE51E1E, 0xE51E7E, 0xE51EDE, 0xE51FC6, 0xE51F96, 0xE293B6, 0xE29B8E, 0xE62EDA, 0xE630D6, 0xE633AA, 0xE6369E]
    for kokiri in kokiriAddresses:
        rom.write_bytes(kokiri, [0x8C, 0x0C])
    # Kokiri
    rom.write_bytes(0xE52838, [0x94, 0x48, 0x0E, 0xD4])
    rom.write_bytes(0xE53A58, [0x94, 0x49, 0x0E, 0xD4])
    rom.write_bytes(0xE51D50, [0x94, 0x58, 0x0E, 0xD4])
    rom.write_bytes(0xE51F40, [0x94, 0x4B, 0x0E, 0xD4])
    rom.write_bytes(0xE51D98, [0x94, 0x4B, 0x0E, 0xD4])
    rom.write_bytes(0xE51E20, [0x94, 0x4A, 0x0E, 0xD4])
    rom.write_bytes(0xE51E80, [0x94, 0x59, 0x0E, 0xD4])
    rom.write_bytes(0xE51EE0, [0x94, 0x4E, 0x0E, 0xD4])
    rom.write_bytes(0xE51FC8, [0x94, 0x49, 0x0E, 0xD4])
    rom.write_bytes(0xE51F98, [0x94, 0x58, 0x0E, 0xD4])
    # Saria
    rom.write_bytes(0xE293B8, [0x94, 0x78, 0x0E, 0xD4])
    rom.write_bytes(0xE29B90, [0x94, 0x68, 0x0E, 0xD4])
    # Mido
    rom.write_bytes(0xE62EDC, [0x94, 0x6F, 0x0E, 0xD4])
    rom.write_bytes(0xE630D8, [0x94, 0x4F, 0x0E, 0xD4])
    rom.write_bytes(0xE633AC, [0x94, 0x68, 0x0E, 0xD4])
    rom.write_bytes(0xE636A0, [0x94, 0x48, 0x0E, 0xD4])

    # Change adult Kokiri Forest to check for Forest Temple complete flag
    rom.write_bytes(0xE5369E, [0xB4, 0xAC])
    rom.write_bytes(0xD5A83C, [0x80, 0x49, 0x0E, 0xDC])

    # Change adult Goron City to check for Fire Temple complete flag
    rom.write_bytes(0xED59DC, [0x80, 0xC9, 0x0E, 0xDC])

    # Change Pokey to check DT complete flag
    rom.write_bytes(0xE5400A, [0x8C, 0x4C])
    rom.write_bytes(0xE5400E, [0xB4, 0xA4])
    if world.open_forest != 'closed':
        rom.write_bytes(0xE5401C, [0x14, 0x0B])

    # Fix Shadow Temple to check for different rewards for scene
    rom.write_bytes(0xCA3F32, [0x00, 0x00, 0x25, 0x4A, 0x00, 0x10])

    # Fix Spirit Temple to check for different rewards for scene
    rom.write_bytes(0xCA3EA2, [0x00, 0x00, 0x25, 0x4A, 0x00, 0x08])

    # Fix Biggoron to check a different flag.
    rom.write_byte(0xED329B, 0x72)
    rom.write_byte(0xED43E7, 0x72)
    rom.write_bytes(0xED3370, [0x3C, 0x0D, 0x80, 0x12])
    rom.write_bytes(0xED3378, [0x91, 0xB8, 0xA6, 0x42, 0xA1, 0xA8, 0xA6, 0x42])
    rom.write_bytes(0xED6574, [0x00, 0x00, 0x00, 0x00])

    # Remove the check on the number of days that passed for claim check.
    rom.write_bytes(0xED4470, [0x00, 0x00, 0x00, 0x00])
    rom.write_bytes(0xED4498, [0x00, 0x00, 0x00, 0x00])

    # Fixed reward order for Bombchu Bowling
    rom.write_bytes(0xE2E698, [0x80, 0xAA, 0xE2, 0x64])
    rom.write_bytes(0xE2E6A0, [0x80, 0xAA, 0xE2, 0x4C])
    rom.write_bytes(0xE2D440, [0x24, 0x19, 0x00, 0x00])

    # Offset kakariko carpenter starting position
    rom.write_bytes(0x1FF93A4, [0x01, 0x8D, 0x00, 0x11, 0x01, 0x6C, 0xFF, 0x92, 0x00, 0x00, 0x01, 0x78, 0xFF, 0x2E, 0x00, 0x00, 0x00, 0x03, 0xFD, 0x2B, 0x00, 0xC8, 0xFF, 0xF9, 0xFD, 0x03, 0x00, 0xC8, 0xFF, 0xA9, 0xFD, 0x5D, 0x00, 0xC8, 0xFE, 0x5F]) # re order the carpenter's path
    rom.write_byte(0x1FF93D0, 0x06) # set the path points to 6
    rom.write_bytes(0x20160B6, [0x01, 0x8D, 0x00, 0x11, 0x01, 0x6C]) # set the carpenter's start position

    # Give hp after first ocarina minigame round
    rom.write_bytes(0xDF2204, [0x24, 0x03, 0x00, 0x02])

    # Allow owl to always carry the kid down Death Mountain
    rom.write_bytes(0xE304F0, [0x24, 0x0E, 0x00, 0x01])

    # Fix Vanilla Dodongo's Cavern Gossip Stone to not use a permanent flag for the fairy
    if not world.dungeon_mq['Dodongos Cavern']:
        rom.write_byte(0x1F281FE, 0x38)

    # Fix "...???" textbox outside Child Colossus Fairy to use the right flag and disappear once the wall is destroyed
    rom.write_byte(0x21A026F, 0xDD)

    # Remove the "...???" textbox outside the Crater Fairy (change it to an actor that does nothing)
    rom.write_int16s(0x225E7DC, [0x00B5, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0xFFFF])

    # Forbid Sun's Song from a bunch of cutscenes
    Suns_scenes = [0x2016FC9, 0x2017219, 0x20173D9, 0x20174C9, 0x2017679, 0x20C1539, 0x20C15D9, 0x21A0719, 0x21A07F9, 0x2E90129, 0x2E901B9, 0x2E90249, 0x225E829, 0x225E939, 0x306D009]
    for address in Suns_scenes:
        rom.write_byte(address,0x01)

    # Allow Warp Songs in additional places
    rom.write_byte(0xB6D3D2, 0x00) # Gerudo Training Ground
    rom.write_byte(0xB6D42A, 0x00) # Inside Ganon's Castle

    #Tell Sheik at Ice Cavern we are always an Adult
    rom.write_int32(0xC7B9C0, 0x00000000)
    rom.write_int32(0xC7BAEC, 0x00000000)
    rom.write_int32(0xc7BCA4, 0x00000000)

    # Allow Farore's Wind in dungeons where it's normally forbidden
    rom.write_byte(0xB6D3D3, 0x00) # Gerudo Training Ground
    rom.write_byte(0xB6D42B, 0x00) # Inside Ganon's Castle

    # Remove disruptive text from Gerudo Training Ground and early Shadow Temple (vanilla)
    Wonder_text = [0x27C00BC, 0x27C00CC, 0x27C00DC, 0x27C00EC, 0x27C00FC, 0x27C010C, 0x27C011C, 0x27C012C, 0x27CE080,
                   0x27CE090, 0x2887070, 0x2887080, 0x2887090, 0x2897070, 0x28C7134, 0x28D91BC, 0x28A60F4, 0x28AE084,
                   0x28B9174, 0x28BF168, 0x28BF178, 0x28BF188, 0x28A1144, 0x28A6104, 0x28D0094]
    for address in Wonder_text:
        rom.write_byte(address, 0xFB)

    # Speed dig text for Dampe
    rom.write_bytes(0x9532F8, [0x08, 0x08, 0x08, 0x59])

    # Make item descriptions into a single box
    Short_item_descriptions = [0x92EC84, 0x92F9E3, 0x92F2B4, 0x92F37A, 0x92F513, 0x92F5C6, 0x92E93B, 0x92EA12]
    for address in Short_item_descriptions:
        rom.write_byte(address,0x02)

    et_original = rom.read_bytes(0xB6FBF0, 4 * 0x0614)

    exit_updates = []

    def copy_entrance_record(source_index, destination_index, count=4):
        ti = source_index * 4
        rom.write_bytes(0xB6FBF0 + destination_index * 4, et_original[ti:ti+(4 * count)])

    def generate_exit_lookup_table():
        # Assumes that the last exit on a scene's exit list cannot be 0000
        exit_table = {
            0x0028: [0xAC95C2] #Jabu with the fish is entered from a cutscene hardcode
            }

        def add_scene_exits(scene_start, offset = 0):
            current = scene_start + offset
            exit_list_start_off = 0
            exit_list_end_off = 0
            command = 0

            while command != 0x14:
                command = rom.read_byte(current)
                if command == 0x18: # Alternate header list
                    header_list = scene_start + (rom.read_int32(current + 4) & 0x00FFFFFF)
                    for alt_id in range(0,3):
                        header_offset = rom.read_int32(header_list) & 0x00FFFFFF
                        if header_offset != 0:
                            add_scene_exits(scene_start, header_offset)
                        header_list += 4
                if command == 0x13: # Exit List
                    exit_list_start_off = rom.read_int32(current + 4) & 0x00FFFFFF
                if command == 0x0F: # Lighting list, follows exit list
                    exit_list_end_off = rom.read_int32(current + 4) & 0x00FFFFFF
                current += 8

            if exit_list_start_off == 0 or exit_list_end_off == 0:
                return

            # calculate the exit list length
            list_length = (exit_list_end_off - exit_list_start_off) // 2
            last_id = rom.read_int16(scene_start + exit_list_end_off - 2)
            if last_id == 0:
                list_length -= 1

            # update
            addr = scene_start + exit_list_start_off
            for _ in range(0, list_length):
                index = rom.read_int16(addr)
                if index not in exit_table:
                    exit_table[index] = []
                exit_table[index].append(addr)
                addr += 2

        scene_table = 0x00B71440
        for scene in range(0x00, 0x65):
            scene_start = rom.read_int32(scene_table + (scene * 0x14))
            add_scene_exits(scene_start)

        return exit_table

    if (world.shuffle_bosses != 'off'):
        # Credit to rattus128 for this ASM block.
        # Gohma's save/death warp is optimized to use immediate 0 for the
        # deku tree respawn. Use the delay slot before the switch table
        # to hold Gohmas jump entrance as actual data so we can substitute
        # the entrance index later.
        rom.write_int32(0xB06290, 0x240E0000) #li t6, 0
        rom.write_int32(0xB062B0, 0xAE0E0000) #sw t6, 0(s0)
        rom.write_int32(0xBC60AC, 0x24180000) #li t8, 0
        rom.write_int32(0xBC6160, 0x24180000) #li t8, 0
        rom.write_int32(0xBC6168, 0xAD380000) #sw t8, 0(t1)

        # Credit to engineer124
        # Update the Jabu-Jabu Boss Exit to actually useful coordinates (and to load the correct room)
        rom.write_int16(0x273E08E, 0xF7F4)  # Z coordinate of Jabu Boss Door Spawn
        rom.write_byte(0x273E27B, 0x05)  # Set Spawn Room to be correct

    def set_entrance_updates(entrances):

        # Boss shuffle
        blue_warp_remaps = {}
        if (world.shuffle_bosses != 'off'):
            # Connect lake hylia fill exit to revisit exit
            rom.write_int16(0xAC995A, 0x060C)

            # First pass for boss shuffle
            # We'll need to iterate more than once, so make a copy so we can iterate more than once.
            entrances = list(entrances)
            for entrance in entrances:
                if entrance.type not in('ChildBoss', 'AdultBoss') or not entrance.replaces or 'patch_addresses' not in entrance.data:
                    continue
                if entrance == entrance.replaces:
                    # This can happen if something is plando'd vanilla.
                    continue

                new_boss = entrance.replaces.data
                original_boss = entrance.data

                # Fixup save/quit and death warping entrance IDs on bosses.
                for address in new_boss['patch_addresses']:
                    rom.write_int16(address, original_boss['dungeon_index'])

                # Update blue warps.
                # If dungeons are shuffled, we'll this in the next step -- that's fine.
                copy_entrance_record(original_boss['exit_index'], new_boss['exit_blue_warp'], 2)
                copy_entrance_record(original_boss['exit_blue_warp'] + 2, new_boss['exit_blue_warp'] + 2, 2)

                # If dungeons are shuffled but their bosses are moved, they're going to refer to the wrong blue warp
                # slots.  Create a table to remap them for later.
                blue_warp_remaps[original_boss['exit_blue_warp']] = new_boss['exit_blue_warp']
        # Boss shuffle done(?)

        for entrance in entrances:
            new_entrance = entrance.data
            replaced_entrance = entrance.replaces.data

            exit_updates.append((new_entrance['index'], replaced_entrance['index']))

            for address in new_entrance.get('addresses', []):
                rom.write_int16(address, replaced_entrance['index'])

            patch_value = replaced_entrance.get('patch_value')
            if patch_value is not None:
                for address in new_entrance['patch_addresses']:
                    rom.write_int16(address, patch_value)

            if "blue_warp" in new_entrance:
                blue_warp = new_entrance["blue_warp"]
                blue_warp = blue_warp_remaps.get(blue_warp, blue_warp)
                if "blue_warp" in replaced_entrance:
                    blue_out_data = replaced_entrance["blue_warp"]
                else:
                    blue_out_data = replaced_entrance["index"]
                # Blue warps have multiple hardcodes leading to them. The good news is
                # the blue warps (excluding deku sprout and lake fill special cases) each
                # have a nice consistent 4-entry in the table we can just shuffle. So just
                # catch all the hardcode with entrance table rewrite. This covers the
                # Forest temple and Water temple blue warp revisits. Deku sprout remains
                # vanilla as it never took you to the exit and the lake fill is handled
                # above by removing the cutscene completely. Child has problems with Adult
                # blue warps, so always use the return entrance if a child.
                copy_entrance_record(blue_out_data + 2, blue_warp + 2, 2)
                copy_entrance_record(replaced_entrance["index"], blue_warp, 2)

    exit_table = generate_exit_lookup_table()

    if world.disable_trade_revert:
        # Disable trade quest timers and prevent trade items from ever reverting
        rom.write_byte(rom.sym('DISABLE_TIMERS'), 0x01)
        rom.write_int16s(0xB6D460, [0x0030, 0x0035, 0x0036]) # Change trade items revert table to prevent all reverts

    if world.shuffle_overworld_entrances:
        rom.write_byte(rom.sym('OVERWORLD_SHUFFLED'), 1)

        # Prevent the ocarina cutscene from leading straight to hyrule field
        rom.write_byte(rom.sym('OCARINAS_SHUFFLED'), 1)

        # Combine all fence hopping LLR exits to lead to the main LLR exit
        for k in [0x028A, 0x028E, 0x0292]: # Southern, Western, Eastern Gates
            exit_table[0x01F9] += exit_table[k] # Hyrule Field entrance from Lon Lon Ranch (main land entrance)
            del exit_table[k]
        exit_table[0x01F9].append(0xD52722) # 0x0476, Front Gate

        # Combine the water exits between Hyrule Field and Zora River to lead to the land entrance instead of the water entrance
        exit_table[0x00EA] += exit_table[0x01D9] # Hyrule Field -> Zora River
        exit_table[0x0181] += exit_table[0x0311] # Zora River -> Hyrule Field
        del exit_table[0x01D9]
        del exit_table[0x0311]

        # Change Impa escorts to bring link at the hyrule castle grounds entrance from market, instead of hyrule field
        rom.write_int16(0xACAA2E, 0x0138) # 1st Impa escort
        rom.write_int16(0xD12D6E, 0x0138) # 2nd+ Impa escort

    if world.shuffle_dungeon_entrances:
        rom.write_byte(rom.sym('DUNGEONS_SHUFFLED'), 1)

        # Connect lake hylia fill exit to revisit exit
        rom.write_int16(0xAC995A, 0x060C)

        # Tell the well water we are always a child.
        rom.write_int32(0xDD5BF4, 0x00000000)

        # Make the Adult well blocking stone dissappear if the well has been drained by
        # checking the well drain event flag instead of links age. This actor doesn't need a
        # code check for links age as the stone is absent for child via the scene alternate
        # lists. So replace the age logic with drain logic.
        rom.write_int32(0xE2887C, rom.read_int32(0xE28870)) # relocate this to nop delay slot
        rom.write_int32(0xE2886C, 0x95CEB4B0) # lhu
        rom.write_int32(0xE28870, 0x31CE0080) # andi

        remove_entrance_blockers(rom)

        # Purge temp flags on entrance to spirit from colossus through the front door.
        rom.write_byte(0x021862E3, 0xC2)

    if (world.shuffle_overworld_entrances or world.shuffle_dungeon_entrances
        or world.shuffle_bosses != 'off'):
        # Remove deku sprout and drop player at SFM after forest completion
        rom.write_int16(0xAC9F96, 0x0608)

    if world.spawn_positions:
        # Fix save warping inside Link's House to not be a special case
        rom.write_int32(0xB06318, 0x00000000)

    # Set entrances to update, except grotto entrances which are handled on their own at a later point
    set_entrance_updates(filter(lambda entrance: entrance.type != 'Grotto', world.get_shuffled_entrances()))

    for k, v in [(k,v) for k, v in exit_updates if k in exit_table]:
        for addr in exit_table[k]:
            rom.write_int16(addr, v)

    # Fix text for Pocket Cucco.
    rom.write_byte(0xBEEF45, 0x0B)

    # Fix stupid alcove cameras in Ice Cavern -- thanks to krim and mzx for the help
    rom.write_byte(0x2BECA25,0x01)
    rom.write_byte(0x2BECA2D,0x01)

    configure_dungeon_info(rom, world)

    rom.write_bytes(rom.sym('CFG_FILE_SELECT_HASH'), world.file_hash)

    save_context = SaveContext()

    # Initial Save Data
    if not world.useful_cutscenes and ('Forest Temple' not in world.dungeon_shortcuts):
        save_context.write_bits(0x00D4 + 0x03 * 0x1C + 0x04 + 0x0, 0x08) # Forest Temple switch flag (Poe Sisters cutscene)

    if 'Deku Tree' in world.dungeon_shortcuts:
        # Deku Tree, flags are the same between vanilla/MQ
        save_context.write_permanent_flag(Scenes.DEKU_TREE, FlagType.SWITCH, 0x1, 0x01) # Deku Block down
        save_context.write_permanent_flag(Scenes.DEKU_TREE, FlagType.CLEAR,  0x2, 0x02) # Deku 231/312
        save_context.write_permanent_flag(Scenes.DEKU_TREE, FlagType.SWITCH, 0x3, 0x20) # Deku 1st Web
        save_context.write_permanent_flag(Scenes.DEKU_TREE, FlagType.SWITCH, 0x3, 0x40) # Deku 2nd Web

    if 'Dodongos Cavern' in world.dungeon_shortcuts:
        # Dodongo's Cavern, flags are the same between vanilla/MQ
        save_context.write_permanent_flag(Scenes.DODONGOS_CAVERN, FlagType.SWITCH, 0x3, 0x80) # DC Entrance Mud Wall
        save_context.write_permanent_flag(Scenes.DODONGOS_CAVERN, FlagType.SWITCH, 0x0, 0x04) # DC Mouth
        # Extra permanent flag in MQ for the child route
        if world.dungeon_mq['Dodongos Cavern']:
            save_context.write_permanent_flag(Scenes.DODONGOS_CAVERN, FlagType.SWITCH, 0x0, 0x02) # Armos wall switch

    if 'Jabu Jabus Belly' in world.dungeon_shortcuts:
        # Jabu
        if not world.dungeon_mq['Jabu Jabus Belly']:
            save_context.write_permanent_flag(Scenes.JABU_JABU, FlagType.SWITCH, 0x0, 0x20) # Jabu Pathway down
        else:
            save_context.write_permanent_flag(Scenes.JABU_JABU, FlagType.SWITCH, 0x1, 0x20) # Jabu Lobby Slingshot Door open
            save_context.write_permanent_flag(Scenes.JABU_JABU, FlagType.SWITCH, 0x0, 0x20) # Jabu Pathway down
            save_context.write_permanent_flag(Scenes.JABU_JABU, FlagType.CLEAR,  0x2, 0x01) # Jabu Red Slimy Thing defeated
            save_context.write_permanent_flag(Scenes.JABU_JABU, FlagType.SWITCH, 0x2, 0x08) # Jabu Red Slimy Thing not in front of boss lobby
            save_context.write_permanent_flag(Scenes.JABU_JABU, FlagType.SWITCH, 0x1, 0x10) # Jabu Boss Door Switch Activated
        
    if 'Forest Temple' in world.dungeon_shortcuts:
        # Forest, flags are the same between vanilla/MQ
        save_context.write_permanent_flag(Scenes.FOREST_TEMPLE, FlagType.SWITCH, 0x0, 0x10) # Forest Elevator up
        save_context.write_permanent_flag(Scenes.FOREST_TEMPLE, FlagType.SWITCH, 0x1, 0x01 + 0x02 + 0x04) # Forest Basement Puzzle Done

    if 'Fire Temple' in world.dungeon_shortcuts:
        # Fire, flags are the same between vanilla/MQ
        save_context.write_permanent_flag(Scenes.FIRE_TEMPLE, FlagType.SWITCH, 0x2, 0x40) # Fire Pillar down

    if 'Spirit Temple' in world.dungeon_shortcuts:
        # Spirit
        if not world.dungeon_mq['Spirit Temple']:
            save_context.write_permanent_flag(Scenes.SPIRIT_TEMPLE, FlagType.SWITCH, 0x1, 0x80) # Spirit Chains
            save_context.write_permanent_flag(Scenes.SPIRIT_TEMPLE, FlagType.SWITCH, 0x2, 0x02 + 0x08 + 0x10) # Spirit main room elevator (N block, Rusted Switch, E block)
            save_context.write_permanent_flag(Scenes.SPIRIT_TEMPLE, FlagType.SWITCH, 0x3, 0x10) # Spirit Face
        else:
            save_context.write_permanent_flag(Scenes.SPIRIT_TEMPLE, FlagType.SWITCH, 0x2, 0x10) # Spirit Bombchu Boulder
            save_context.write_permanent_flag(Scenes.SPIRIT_TEMPLE, FlagType.SWITCH, 0x2, 0x02) # Spirit Silver Block
            save_context.write_permanent_flag(Scenes.SPIRIT_TEMPLE, FlagType.SWITCH, 0x1, 0x80) # Spirit Chains
            save_context.write_permanent_flag(Scenes.SPIRIT_TEMPLE, FlagType.SWITCH, 0x3, 0x10) # Spirit Face
        
    if 'Shadow Temple' in world.dungeon_shortcuts:
        # Shadow
        if not world.dungeon_mq['Shadow Temple']:
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x0, 0x08) # Shadow Truthspinner
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x0, 0x20) # Shadow Boat Block
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x1, 0x01) # Shadow Bird Bridge
        else:
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x2, 0x08) # Shadow Truthspinner
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x3, 0x20) # Shadow Fire Arrow Platform
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x3, 0x80) # Shadow Spinning Blades room Skulltulas defeated
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.CLEAR,  0x3, 0x40) # Shadow Spinning Blades room Skulltulas defeated
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x0, 0x20) # Shadow Boat Block
            save_context.write_permanent_flag(Scenes.SHADOW_TEMPLE, FlagType.SWITCH, 0x1, 0x01) # Shadow Bird Bridge

    if world.region_has_shortcuts('King Dodongo Boss Room'):
        save_context.write_permanent_flag(Scenes.KING_DODONGO_LOBBY, FlagType.SWITCH, 0x3, 0x02) # DC Boss Floor

    set_spirit_shortcut_actors(rom) # Change elevator starting position to avoid waiting a half cycle from the temple entrance

    if world.plant_beans:
        save_context.write_permanent_flag(Scenes.GRAVEYARD, FlagType.SWITCH, 0x3, 0x08) # Plant Graveyard bean
        save_context.write_permanent_flag(Scenes.ZORAS_RIVER, FlagType.SWITCH, 0x3, 0x08) # Plant Zora's River bean
        save_context.write_permanent_flag(Scenes.KOKIRI_FOREST, FlagType.SWITCH, 0x2, 0x02) # Plant Kokiri Forest bean
        save_context.write_permanent_flag(Scenes.LAKE_HYLIA, FlagType.SWITCH, 0x3, 0x02) # Plant Lake Hylia bean
        save_context.write_permanent_flag(Scenes.GERUDO_VALLEY, FlagType.SWITCH, 0x3, 0x08) # Plant Gerudo Valley bean
        save_context.write_permanent_flag(Scenes.LOST_WOODS, FlagType.SWITCH, 0x3, 0x10) # Plant Lost Woods bridge bean
        save_context.write_permanent_flag(Scenes.LOST_WOODS, FlagType.SWITCH, 0x1, 0x04) # Plant Lost Woods theater bean
        save_context.write_permanent_flag(Scenes.DESERT_COLOSSUS, FlagType.SWITCH, 0x0, 0x1) # Plant Desert Colossus bean
        save_context.write_permanent_flag(Scenes.DEATH_MOUNTAIN_TRAIL, FlagType.SWITCH, 0x3, 0x40) # Plant Death Mountain Trail bean
        save_context.write_permanent_flag(Scenes.DEATH_MOUNTAIN_CRATER, FlagType.SWITCH, 0x3, 0x08) # Plant Death Mountain Crater bean

    save_context.write_bits(0x00D4 + 0x05 * 0x1C + 0x04 + 0x1, 0x01) # Water temple switch flag (Ruto)
    save_context.write_bits(0x00D4 + 0x51 * 0x1C + 0x04 + 0x2, 0x08) # Hyrule Field switch flag (Owl)
    save_context.write_bits(0x00D4 + 0x55 * 0x1C + 0x04 + 0x0, 0x80) # Kokiri Forest switch flag (Owl)
    save_context.write_bits(0x00D4 + 0x56 * 0x1C + 0x04 + 0x2, 0x40) # Sacred Forest Meadow switch flag (Owl)
    save_context.write_bits(0x00D4 + 0x5B * 0x1C + 0x04 + 0x2, 0x01) # Lost Woods switch flag (Owl)
    save_context.write_bits(0x00D4 + 0x5B * 0x1C + 0x04 + 0x3, 0x80) # Lost Woods switch flag (Owl)
    save_context.write_bits(0x00D4 + 0x5C * 0x1C + 0x04 + 0x0, 0x80) # Desert Colossus switch flag (Owl)
    save_context.write_bits(0x00D4 + 0x5F * 0x1C + 0x04 + 0x3, 0x20) # Hyrule Castle switch flag (Owl)

    save_context.write_bits(0x0ED4, 0x10) # "Met Deku Tree"
    save_context.write_bits(0x0ED5, 0x20) # "Deku Tree Opened Mouth"
    save_context.write_bits(0x0ED6, 0x08) # "Rented Horse From Ingo"
    save_context.write_bits(0x0ED6, 0x10) # "Spoke to Mido After Deku Tree's Death"
    save_context.write_bits(0x0EDA, 0x08) # "Began Nabooru Battle"
    save_context.write_bits(0x0EDC, 0x80) # "Entered the Master Sword Chamber"
    save_context.write_bits(0x0EDD, 0x20) # "Pulled Master Sword from Pedestal"
    save_context.write_bits(0x0EE0, 0x80) # "Spoke to Kaepora Gaebora by Lost Woods"
    save_context.write_bits(0x0EE7, 0x20) # "Nabooru Captured by Twinrova"
    save_context.write_bits(0x0EE7, 0x10) # "Spoke to Nabooru in Spirit Temple"
    save_context.write_bits(0x0EED, 0x20) # "Sheik, Spawned at Master Sword Pedestal as Adult"
    save_context.write_bits(0x0EED, 0x01) # "Nabooru Ordered to Fight by Twinrova"
    save_context.write_bits(0x0EED, 0x80) # "Watched Ganon's Tower Collapse / Caught by Gerudo"
    save_context.write_bits(0x0EF9, 0x01) # "Greeted by Saria"
    save_context.write_bits(0x0F0A, 0x04) # "Spoke to Ingo Once as Adult"
    save_context.write_bits(0x0F0F, 0x40) # "Met Poe Collector in Ruined Market"
    if not world.useful_cutscenes:
        save_context.write_bits(0x0F1A, 0x04) # "Met Darunia in Fire Temple"

    save_context.write_bits(0x0ED7, 0x01) # "Spoke to Child Malon at Castle or Market"
    save_context.write_bits(0x0ED7, 0x20) # "Spoke to Child Malon at Ranch"
    save_context.write_bits(0x0ED7, 0x40) # "Invited to Sing With Child Malon"
    save_context.write_bits(0x0F09, 0x10) # "Met Child Malon at Castle or Market"
    save_context.write_bits(0x0F09, 0x20) # "Child Malon Said Epona Was Scared of You"

    save_context.write_bits(0x0F21, 0x04) # "Ruto in JJ (M3) Talk First Time"
    save_context.write_bits(0x0F21, 0x02) # "Ruto in JJ (M2) Meet Ruto"

    save_context.write_bits(0x0EE2, 0x01) # "Began Ganondorf Battle"
    save_context.write_bits(0x0EE3, 0x80) # "Began Bongo Bongo Battle"
    save_context.write_bits(0x0EE3, 0x40) # "Began Barinade Battle"
    save_context.write_bits(0x0EE3, 0x20) # "Began Twinrova Battle"
    save_context.write_bits(0x0EE3, 0x10) # "Began Morpha Battle"
    save_context.write_bits(0x0EE3, 0x08) # "Began Volvagia Battle"
    save_context.write_bits(0x0EE3, 0x04) # "Began Phantom Ganon Battle"
    save_context.write_bits(0x0EE3, 0x02) # "Began King Dodongo Battle"
    save_context.write_bits(0x0EE3, 0x01) # "Began Gohma Battle"

    save_context.write_bits(0x0EE8, 0x01) # "Entered Deku Tree"
    save_context.write_bits(0x0EE9, 0x80) # "Entered Temple of Time"
    save_context.write_bits(0x0EE9, 0x40) # "Entered Goron City"
    save_context.write_bits(0x0EE9, 0x20) # "Entered Hyrule Castle"
    save_context.write_bits(0x0EE9, 0x10) # "Entered Zora's Domain"
    save_context.write_bits(0x0EE9, 0x08) # "Entered Kakariko Village"
    save_context.write_bits(0x0EE9, 0x02) # "Entered Death Mountain Trail"
    save_context.write_bits(0x0EE9, 0x01) # "Entered Hyrule Field"
    save_context.write_bits(0x0EEA, 0x04) # "Entered Ganon's Castle (Exterior)"
    save_context.write_bits(0x0EEA, 0x02) # "Entered Death Mountain Crater"
    save_context.write_bits(0x0EEA, 0x01) # "Entered Desert Colossus"
    save_context.write_bits(0x0EEB, 0x80) # "Entered Zora's Fountain"
    save_context.write_bits(0x0EEB, 0x40) # "Entered Graveyard"
    save_context.write_bits(0x0EEB, 0x20) # "Entered Jabu-Jabu's Belly"
    save_context.write_bits(0x0EEB, 0x10) # "Entered Lon Lon Ranch"
    save_context.write_bits(0x0EEB, 0x08) # "Entered Gerudo's Fortress"
    save_context.write_bits(0x0EEB, 0x04) # "Entered Gerudo Valley"
    save_context.write_bits(0x0EEB, 0x02) # "Entered Lake Hylia"
    save_context.write_bits(0x0EEB, 0x01) # "Entered Dodongo's Cavern"
    save_context.write_bits(0x0F08, 0x08) # "Entered Hyrule Castle"

    if world.dungeon_mq['Shadow Temple']:
        save_context.write_bits(0x019F, 0x80) # "Turn On Clear Wall Blocking Hover Boots Room"

    # Set the number of chickens to collect
    rom.write_byte(0x00E1E523, world.chicken_count)

    # Change Anju to always say how many chickens are needed
    # Does not affect text for collecting item or afterwards
    rom.write_int16(0x00E1F3C2, 0x5036)
    rom.write_int16(0x00E1F3C4, 0x5036)
    rom.write_int16(0x00E1F3C6, 0x5036)
    rom.write_int16(0x00E1F3C8, 0x5036)
    rom.write_int16(0x00E1F3CA, 0x5036)
    rom.write_int16(0x00E1F3CC, 0x5036)

    # Make the Kakariko Gate not open with the MS
    if world.open_kakariko != 'open':
        rom.write_int32(0xDD3538, 0x34190000) # li t9, 0
    if world.open_kakariko != 'closed':
        rom.write_byte(rom.sym('OPEN_KAKARIKO'), 1)

    if world.complete_mask_quest:
        rom.write_byte(rom.sym('COMPLETE_MASK_QUEST'), 1)

    if world.shuffle_child_trade == 'skip_child_zelda':
        save_context.give_item(world, 'Zeldas Letter')
        # Archipelago forces this item to be local so it can always be given to the player. Usually it's a song so it's no problem.
        item = world.get_location('Song from Impa').item
        save_context.give_item(world, item.name)
        if item.name == 'Slingshot':
            save_context.give_item(world, "Deku Seeds (30)")
        elif item.name == 'Bow': 
            save_context.give_item(world, "Arrows (30)")
        elif item.name == 'Bomb Bag': 
            save_context.give_item(world, "Bombs (20)")
        save_context.write_bits(0x0ED7, 0x04) # "Obtained Malon's Item"
        save_context.write_bits(0x0ED7, 0x08) # "Woke Talon in castle"
        save_context.write_bits(0x0ED7, 0x10) # "Talon has fled castle"
        save_context.write_bits(0x0EDD, 0x01) # "Obtained Zelda's Letter"
        save_context.write_bits(0x0EDE, 0x02) # "Learned Zelda's Lullaby"
        save_context.write_bits(0x00D4 + 0x5F * 0x1C + 0x04 + 0x3, 0x10) # "Moved crates to access the courtyard"
        if world.open_kakariko != 'closed':
            save_context.write_bits(0x0F07, 0x40) # "Spoke to Gate Guard About Mask Shop"
        if world.complete_mask_quest:
            save_context.write_bits(0x0F07, 0x80) # "Soldier Wears Keaton Mask"
            save_context.write_bits(0x0EF6, 0x8F) # "Sold Masks & Unlocked Masks" / "Obtained Mask of Truth"
            save_context.write_bits(0x0EE4, 0xF0) # "Paid Back Mask Fees"

    if world.zora_fountain == 'open':
        save_context.write_bits(0x0EDB, 0x08) # "Moved King Zora"
    elif world.zora_fountain == 'adult':
        rom.write_byte(rom.sym('MOVED_ADULT_KING_ZORA'), 1)

    # Make all chest opening animations fast
    rom.write_byte(rom.sym('FAST_CHESTS'), int(world.fast_chests))


    # Set up Rainbow Bridge conditions
    symbol = rom.sym('RAINBOW_BRIDGE_CONDITION')
    count_symbol = rom.sym('RAINBOW_BRIDGE_COUNT')
    if world.bridge == 'open':
        rom.write_int32(symbol, 0)
        save_context.write_bits(0xEDC, 0x20) # "Rainbow Bridge Built by Sages"
    elif world.bridge == 'medallions':
        rom.write_int32(symbol, 1)
        rom.write_int16(count_symbol, world.bridge_medallions)
    elif world.bridge == 'dungeons':
        rom.write_int32(symbol, 2)
        rom.write_int16(count_symbol, world.bridge_rewards)
    elif world.bridge == 'stones':
        rom.write_int32(symbol, 3)
        rom.write_int16(count_symbol, world.bridge_stones)
    elif world.bridge == 'vanilla':
        rom.write_int32(symbol, 4)
    elif world.bridge == 'tokens':
        rom.write_int32(symbol, 5)
        rom.write_int16(count_symbol, world.bridge_tokens)
    elif world.bridge == 'hearts':
        rom.write_int32(symbol, 6)
        rom.write_int16(count_symbol, world.bridge_hearts * 0x10)

    if world.triforce_hunt:
        rom.write_int16(rom.sym('TRIFORCE_PIECES_REQUIRED'), world.triforce_goal)
        rom.write_int16(rom.sym('TRIFORCE_HUNT_ENABLED'), 1)

    # Set up Ganon's Boss Key conditions.
    symbol = rom.sym('GANON_BOSS_KEY_CONDITION')
    count_symbol = rom.sym('GANON_BOSS_KEY_CONDITION_COUNT')
    if world.shuffle_ganon_bosskey == 'medallions':
        rom.write_byte(symbol, 1)
        rom.write_int16(count_symbol, world.ganon_bosskey_medallions)
    elif world.shuffle_ganon_bosskey == 'dungeons':
        rom.write_byte(symbol, 2)
        rom.write_int16(count_symbol, world.ganon_bosskey_rewards)
    elif world.shuffle_ganon_bosskey == 'stones':
        rom.write_byte(symbol, 3)
        rom.write_int16(count_symbol, world.ganon_bosskey_stones)
    elif world.shuffle_ganon_bosskey == 'tokens':
        rom.write_byte(symbol, 4)
        rom.write_int16(count_symbol, world.ganon_bosskey_tokens)
    elif world.shuffle_ganon_bosskey == 'hearts':
        rom.write_byte(symbol, 5)
        rom.write_int16(count_symbol, world.ganon_bosskey_hearts * 0x10)
    else:
        rom.write_byte(symbol, 0)
        rom.write_int16(count_symbol, 0)

    # Set up LACS conditions.
    symbol = rom.sym('LACS_CONDITION')
    count_symbol = rom.sym('LACS_CONDITION_COUNT')
    if world.lacs_condition == 'medallions':
        rom.write_int32(symbol, 1)
        rom.write_int16(count_symbol, world.lacs_medallions)
    elif world.lacs_condition == 'dungeons':
        rom.write_int32(symbol, 2)
        rom.write_int16(count_symbol, world.lacs_rewards)
    elif world.lacs_condition == 'stones':
        rom.write_int32(symbol, 3)
        rom.write_int16(count_symbol, world.lacs_stones)
    elif world.lacs_condition == 'tokens':
        rom.write_int32(symbol, 4)
        rom.write_int16(count_symbol, world.lacs_tokens)
    elif world.lacs_condition == 'hearts':
        rom.write_int32(symbol, 5)
        rom.write_int16(count_symbol, world.lacs_hearts * 0x10)
    else:
        rom.write_int32(symbol, 0)

    if world.open_forest == 'open':
        save_context.write_bits(0xED5, 0x10) # "Showed Mido Sword & Shield"

    if world.open_door_of_time:
        save_context.write_bits(0xEDC, 0x08) # "Opened the Door of Time"

    # "fast-ganon" stuff
    symbol = rom.sym('NO_ESCAPE_SEQUENCE')
    if world.no_escape_sequence:
        rom.write_bytes(0xD82A12, [0x05, 0x17]) # Sets exit from Ganondorf fight to entrance to Ganon fight
        rom.write_bytes(0xB139A2, [0x05, 0x17]) # Sets Ganon deathwarp back to Ganon
        rom.write_byte(symbol, 0x01)
    else:
        rom.write_byte(symbol, 0x00)
    if world.skipped_trials['Forest']:
        save_context.write_bits(0x0EEA, 0x08) # "Completed Forest Trial"
    if world.skipped_trials['Fire']:
        save_context.write_bits(0x0EEA, 0x40) # "Completed Fire Trial"
    if world.skipped_trials['Water']:
        save_context.write_bits(0x0EEA, 0x10) # "Completed Water Trial"
    if world.skipped_trials['Spirit']:
        save_context.write_bits(0x0EE8, 0x20) # "Completed Spirit Trial"
    if world.skipped_trials['Shadow']:
        save_context.write_bits(0x0EEA, 0x20) # "Completed Shadow Trial"
    if world.skipped_trials['Light']:
        save_context.write_bits(0x0EEA, 0x80) # "Completed Light Trial"
    if world.trials == 0:
        save_context.write_bits(0x0EED, 0x08) # "Dispelled Ganon's Tower Barrier"

    # open gerudo fortress
    if world.gerudo_fortress == 'open':
        if not world.shuffle_gerudo_card:
            save_context.write_bits(0x00A5, 0x40) # Give Gerudo Card
        save_context.write_bits(0x0EE7, 0x0F) # Free all 4 carpenters
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x04 + 0x1, 0x0F) # Thieves' Hideout switch flags (started all fights)
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x04 + 0x2, 0x01) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x04 + 0x3, 0xFE) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x0C + 0x2, 0xD4) # Thieves' Hideout collection flags (picked up keys, marks fights finished as well)
    elif world.gerudo_fortress == 'fast':
        save_context.write_bits(0x0EE7, 0x0E) # Free 3 carpenters
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x04 + 0x1, 0x0D) # Thieves' Hideout switch flags (started all fights)
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x04 + 0x2, 0x01) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x04 + 0x3, 0xDC) # Thieves' Hideout switch flags (heard yells/unlocked doors)
        save_context.write_bits(0x00D4 + 0x0C * 0x1C + 0x0C + 0x2, 0xC4) # Thieves' Hideout collection flags (picked up keys, marks fights finished as well)

    # Add a gate opening guard on the Wasteland side of the Gerudo Fortress' gate
    # Overrides the generic guard at the bottom of the ladder in Gerudo Fortress
    new_gate_opening_guard = [0x0138, 0xFAC8, 0x005D, 0xF448, 0x0000, 0x95B0, 0x0000, 0x0301]
    rom.write_int16s(0x21BD3EC, new_gate_opening_guard)  # Adult Day
    rom.write_int16s(0x21BD62C, new_gate_opening_guard)  # Adult Night

    # start with maps/compasses
    if world.shuffle_mapcompass == 'startwith':
        for dungeon in ['deku', 'dodongo', 'jabu', 'forest', 'fire', 'water', 'spirit', 'shadow', 'botw', 'ice']:
            save_context.addresses['dungeon_items'][dungeon]['compass'].value = True
            save_context.addresses['dungeon_items'][dungeon]['map'].value = True

    if world.shuffle_smallkeys == 'vanilla':
        if world.dungeon_mq['Spirit Temple']:
            save_context.addresses['keys']['spirit'].value = 3
        if 'Shadow Temple' in world.dungeon_shortcuts:
            save_context.addresses['keys']['shadow'].value = 2

    if world.start_with_rupees:
        rom.write_byte(rom.sym('MAX_RUPEES'), 0x01)

    # Set starting time of day
    if world.starting_tod != 'default':
        tod = {
             'sunrise':       0x4555,
             'morning':       0x6000,
             'noon':          0x8001,
             'afternoon':     0xA000,
             'sunset':        0xC001,
             'evening':       0xE000,
             'midnight':      0x0000,
             'witching-hour': 0x2000,

        }
        save_context.addresses['time_of_day'].value = tod[world.starting_tod]

    if world.starting_age == 'adult':
        save_context.addresses['link_age'].value = False                    # Set link's age to adult
        save_context.addresses['scene_index'].value = 0x43                  # Set the scene index to Temple of Time
        save_context.addresses['equip_items']['master_sword'].value = True  # Equip Master Sword by default
        save_context.addresses['equip_items']['kokiri_tunic'].value = True  # Equip Kokiri Tunic & Kokiri Boots by default
        save_context.addresses['equip_items']['kokiri_boots'].value = True  # (to avoid issues when going back child for the first time)
        save_context.write_byte(0x0F33, 0x00)                               # Unset Swordless Flag (to avoid issues with sword getting unequipped)

    # For Inventory_SwapAgeEquipment going child -> adult:
    # Change range in which items are read from slot instead of items
    # Extended to include hookshot and ocarina
    rom.write_byte(0xAE5867, 0x07) # >= ITEM_OCARINA_FAIRY
    rom.write_byte(0xAE5873, 0x0C) # <= ITEM_LONGSHOT
    rom.write_byte(0xAE587B, 0x14) # >= ITEM_BOTTLE

    # Revert change that Skips the Epona Race
    if not world.no_epona_race:
        rom.write_int32(0xA9E838, 0x03E00008)
    else:
        save_context.write_bits(0xF0E, 0x01) # Set talked to Malon flag

    # skip castle guard stealth sequence
    if world.no_guard_stealth:
        # change the exit at child/day crawlspace to the end of zelda's goddess cutscene
        rom.write_bytes(0x21F60DE, [0x05, 0xF0])

    # patch mq scenes
    mq_scenes = []
    if world.dungeon_mq['Deku Tree']:
        mq_scenes.append(0)
    if world.dungeon_mq['Dodongos Cavern']:
        mq_scenes.append(1)
    if world.dungeon_mq['Jabu Jabus Belly']:
        mq_scenes.append(2)
    if world.dungeon_mq['Forest Temple']:
        mq_scenes.append(3)
    if world.dungeon_mq['Fire Temple']:
        mq_scenes.append(4)
    if world.dungeon_mq['Water Temple']:
        mq_scenes.append(5)
    if world.dungeon_mq['Spirit Temple']:
        mq_scenes.append(6)
    if world.dungeon_mq['Shadow Temple']:
        mq_scenes.append(7)
    if world.dungeon_mq['Bottom of the Well']:
        mq_scenes.append(8)
    if world.dungeon_mq['Ice Cavern']:
        mq_scenes.append(9)
    # Scene 10 has no layout changes, so it doesn't need to be patched
    if world.dungeon_mq['Gerudo Training Ground']:
        mq_scenes.append(11)
    if world.dungeon_mq['Ganons Castle']:
        mq_scenes.append(13)

    patch_files(rom, mq_scenes)

    ### Load Shop File
    # Move shop actor file to free space
    shop_item_file = File({
            'Name':'En_GirlA',
            'Start':'00C004E0',
            'End':'00C02E00',
        })
    shop_item_file.relocate(rom)

    # Increase the shop item table size
    shop_item_vram_start = rom.read_int32(0x00B5E490 + (0x20 * 4) + 0x08)
    insert_space(rom, shop_item_file, shop_item_vram_start, 1, 0x3C + (0x20 * 50), 0x20 * 50)

    # Add relocation entries for shop item table
    new_relocations = []
    for i in range(50, 100):
        new_relocations.append(shop_item_file.start + 0x1DEC + (i * 0x20) + 0x04)
        new_relocations.append(shop_item_file.start + 0x1DEC + (i * 0x20) + 0x14)
        new_relocations.append(shop_item_file.start + 0x1DEC + (i * 0x20) + 0x1C)
    add_relocations(rom, shop_item_file, new_relocations)

    # update actor table
    rom.write_int32s(0x00B5E490 + (0x20 * 4),
        [shop_item_file.start,
        shop_item_file.end,
        shop_item_vram_start,
        shop_item_vram_start + (shop_item_file.end - shop_item_file.start)])

    # Update DMA Table
    update_dmadata(rom, shop_item_file)

    # Create 2nd Bazaar Room
    bazaar_room_file = File({
            'Name':'shop1_room_1',
            'Start':'028E4000',
            'End':'0290D7B0',
        })
    bazaar_room_file.copy(rom)

    # Add new Bazaar Room to Bazaar Scene
    rom.write_int32s(0x28E3030, [0x00010000, 0x02000058]) #reduce position list size
    rom.write_int32s(0x28E3008, [0x04020000, 0x02000070]) #expand room list size

    rom.write_int32s(0x28E3070, [0x028E4000, 0x0290D7B0,
                     bazaar_room_file.start, bazaar_room_file.end]) #room list
    rom.write_int16s(0x28E3080, [0x0000, 0x0001]) # entrance list
    rom.write_int16(0x28E4076, 0x0005) # Change shop to Kakariko Bazaar
    #rom.write_int16(0x3489076, 0x0005) # Change shop to Kakariko Bazaar

    # Load Message and Shop Data
    messages = read_messages(rom)
    remove_unused_messages(messages)
    shop_items = read_shop_items(rom, shop_item_file.start + 0x1DEC)

    # Set Big Poe count to get reward from buyer
    poe_points = world.big_poe_count * 100
    rom.write_int16(0xEE69CE, poe_points)
    # update dialogue
    new_message = "\x08Hey, young man. What's happening \x01today? If you have a \x05\x41Poe\x05\x40, I will \x01buy it.\x04\x1AIf you earn \x05\x41%d points\x05\x40, you'll\x01be a happy man! Heh heh.\x04\x08Your card now has \x05\x45\x1E\x01 \x05\x40points.\x01Come back again!\x01Heh heh heh!\x02" % poe_points
    update_message_by_id(messages, 0x70F5, new_message)
    if world.big_poe_count != 10:
        new_message = "\x1AOh, you brought a Poe today!\x04\x1AHmmmm!\x04\x1AVery interesting!\x01This is a \x05\x41Big Poe\x05\x40!\x04\x1AI'll buy it for \x05\x4150 Rupees\x05\x40.\x04On top of that, I'll put \x05\x41100\x01points \x05\x40on your card.\x04\x1AIf you earn \x05\x41%d points\x05\x40, you'll\x01be a happy man! Heh heh." % poe_points
        update_message_by_id(messages, 0x70f7, new_message)
        new_message = "\x1AWait a minute! WOW!\x04\x1AYou have earned \x05\x41%d points\x05\x40!\x04\x1AYoung man, you are a genuine\x01\x05\x41Ghost Hunter\x05\x40!\x04\x1AIs that what you expected me to\x01say? Heh heh heh!\x04\x1ABecause of you, I have extra\x01inventory of \x05\x41Big Poes\x05\x40, so this will\x01be the last time I can buy a \x01ghost.\x04\x1AYou're thinking about what I \x01promised would happen when you\x01earned %d points. Heh heh.\x04\x1ADon't worry, I didn't forget.\x01Just take this." % (poe_points, poe_points)
        update_message_by_id(messages, 0x70f8, new_message)

    # Update Child Anju's dialogue
    new_message = "\x08What should I do!?\x01My \x05\x41Cuccos\x05\x40 have all flown away!\x04You, little boy, please!\x01Please gather at least \x05\x41%d Cuccos\x05\x40\x01for me.\x02" % world.chicken_count
    update_message_by_id(messages, 0x5036, new_message)

    # Find an item location behind the Jabu boss door by searching regions breadth-first without going back into Jabu proper
    if world.logic_rules == 'glitched':
        location = world.get_location('Barinade')
    else:
        jabu_reward_regions = {world.get_entrance('Jabu Jabus Belly Boss Door -> Barinade Boss Room').connected_region}
        already_checked = set()
        location = None
        while jabu_reward_regions:
            locations = [
                loc
                for region in jabu_reward_regions
                for loc in region.locations
                if loc.item is not None
            ]
            if locations:
                # Location types later in the list will be preferred over earlier ones or ones not in the list.
                # This ensures that if the region behind the boss door is a boss arena, the medallion or stone will be used.
                priority_types = ("GS Token", "GrottoScrub", "Scrub", "Shop", "NPC", "Collectable", "Freestanding", "ActorOverride", "RupeeTower", "Pot", "Crate", "FlyingPot", "SmallCrate", "Beehive", "Chest", "Cutscene", "Song", "BossHeart", "Boss")
                best_type = max((location.type for location in locations), key=lambda type: priority_types.index(type) if type in priority_types else -1)
                location = world.hint_rng.choice(list(filter(lambda loc: loc.type == best_type, locations)))
                break
            already_checked |= jabu_reward_regions
            jabu_reward_regions = [
                exit.connected_region
                for region in jabu_reward_regions
                for exit in region.exits
                if exit.connected_region.dungeon != 'Jabu Jabus Belly' and exit.connected_region.name not in already_checked
            ]

    if location is None:
        jabu_item = None
        reward_text = None
    elif getattr(location.item, 'looks_like_item', None) is not None:
        jabu_item = location.item.looks_like_item
        reward_text = create_fake_name(getHint(getItemGenericName(location.item.looks_like_item), world.hint_rng, True).text)
    else:
        jabu_item = location.item
        reward_text = getHint(getItemGenericName(location.item), world.hint_rng, True).text

    # Update "Princess Ruto got the Spiritual Stone!" text before the midboss in Jabu
    if reward_text is None:
        new_message = f"\x08Princess Ruto got \x01\x05\x43nothing\x05\x40!\x01Well, that's disappointing...\x02"
    else:
        reward_texts = {
            'Kokiri Emerald':   "the \x05\x42Kokiri Emerald\x05\x40",
            'Goron Ruby':       "the \x05\x41Goron Ruby\x05\x40",
            'Zora Sapphire':    "the \x05\x43Zora Sapphire\x05\x40",
            'Forest Medallion': "the \x05\x42Forest Medallion\x05\x40",
            'Fire Medallion':   "the \x05\x41Fire Medallion\x05\x40",
            'Water Medallion':  "the \x05\x43Water Medallion\x05\x40",
            'Spirit Medallion': "the \x05\x46Spirit Medallion\x05\x40",
            'Shadow Medallion': "the \x05\x45Shadow Medallion\x05\x40",
            'Light Medallion':  "the \x05\x44Light Medallion\x05\x40",
        }
        reward_text = reward_texts.get(location.item.name, f'\x05\x43{reward_text}\x05\x40')
        new_message = f"\x08Princess Ruto got \x01{reward_text}!\x01But why Princess Ruto?\x02"
    update_message_by_id(messages, 0x4050, new_message)

    # Set Dungeon Reward Actor in Jabu Jabu to be accurate
    # Vanilla and MQ Jabu Jabu addresses are the same for this object and actor
    if location is not None: #TODO make actor invisible if no item?
        jabu_item = location.item
        jabu_stone_object = jabu_item.special['object_id']
        rom.write_int16(0x277D068, jabu_stone_object)
        rom.write_int16(0x277D168, jabu_stone_object)
        jabu_stone_type = jabu_item.special['actor_type']
        rom.write_byte(0x277D0BB, jabu_stone_type)
        rom.write_byte(0x277D19B, jabu_stone_type)
        jabu_actor_type = jabu_item.special['actor_type']
        set_jabu_stone_actors(rom, jabu_actor_type)
        # Also set the right object for the actor, since medallions and stones require different objects
        # MQ is handled separately, as we include both objects in the object list in mqu.json (Scene 2, Room 6)
        if not world.dungeon_mq['Jabu Jabus Belly']:
            rom.write_int16(0x277D068, jabu_stone_object)
            rom.write_int16(0x277D168, jabu_stone_object)

    # use faster jabu elevator
    if not world.dungeon_mq['Jabu Jabus Belly'] and world.shuffle_scrubs == 'off':
        symbol = rom.sym('JABU_ELEVATOR_ENABLE')
        rom.write_byte(symbol, 0x01)

    if world.skip_some_minigame_phases:
        save_context.write_bits(0x00D4 + 0x48 * 0x1C + 0x08 + 0x3, 0x10) # Beat First Dampe Race (& Chest Spawned)
        rom.write_byte(rom.sym('CHAIN_HBA_REWARDS'), 1)
        # Update the first horseback archery text to make it clear both rewards are available from the start
        update_message_by_id(messages, 0x6040, "Hey newcomer, you have a fine \x01horse!\x04I don't know where you stole \x01it from, but...\x04OK, how about challenging this \x01\x05\x41horseback archery\x05\x40?\x04Once the horse starts galloping,\x01shoot the targets with your\x01arrows. \x04Let's see how many points you \x01can score. You get 20 arrows.\x04If you can score \x05\x411,000 points\x05\x40, I will \x01give you something good! And even \x01more if you score \x05\x411,500 points\x05\x40!\x0B\x02")

    # Sets hooks for gossip stone changes

    symbol = rom.sym("GOSSIP_HINT_CONDITION")

    if world.hints == 'none':
        rom.write_int32(symbol, 0)
    else:
        writeGossipStoneHints(world, messages)

        if world.hints == 'mask':
            rom.write_int32(symbol, 0)
        elif world.hints == 'always':
            rom.write_int32(symbol, 2)
        else:
            rom.write_int32(symbol, 1)


    # build silly ganon lines
    if 'ganondorf' in world.misc_hints:
        buildGanonText(world, messages)

    # build misc. item hints
    buildMiscItemHints(world, messages)

    # build misc. location hints
    buildMiscLocationHints(world, messages)

    # Patch freestanding items
    if world.shuffle_freestanding_items:
    # Get freestanding item locations
        actor_override_locations = [location for location in world.get_locations() if location.disabled == DisableType.ENABLED and location.type == 'ActorOverride']
        rupeetower_locations = [location for location in world.get_locations() if location.disabled == DisableType.ENABLED and location.type == 'RupeeTower']

        for location in actor_override_locations:
            patch_actor_override(location, rom)
        for location in rupeetower_locations:
            patch_rupee_tower(location, rom)

    # Write flag table data
    collectible_flag_table, alt_list = get_collectible_flag_table(world)
    collectible_flag_table_bytes, num_collectible_flags = get_collectible_flag_table_bytes(collectible_flag_table)
    alt_list_bytes = get_alt_list_bytes(alt_list)
    if(len(collectible_flag_table_bytes) > 600):
        raise(RuntimeError(f'Exceeded collectible override table size: {len(collectible_flag_table_bytes)}'))
    rom.write_bytes(rom.sym('collectible_scene_flags_table'), collectible_flag_table_bytes)
    num_collectible_flags += num_collectible_flags % 8
    rom.write_bytes(rom.sym('num_override_flags'), num_collectible_flags.to_bytes(2, 'big'))
    if(len(alt_list) > 64):
        raise(RuntimeError(f'Exceeded alt override table size: {len(alt_list)}'))
    rom.write_bytes(rom.sym('alt_overrides'), alt_list_bytes)

    # Gather addresses and bitflags for client
    world.collectible_override_flags = rom.sym('collectible_override_flags') - rom.sym('RANDO_CONTEXT')
    world.collectible_flag_offsets = get_collectible_flag_addresses(world, collectible_flag_table_bytes)
    world.collectible_flags_available.set()

    # Write item overrides
    # check_location_dupes(world)
    override_table = get_override_table(world)
    if len(override_table) >= 1536:
        raise(RuntimeError(f'Exceeded override table size: {len(override_table)}'))
    rom.write_bytes(rom.sym('cfg_item_overrides'), get_override_table_bytes(override_table))
    rom.write_byte(rom.sym('PLAYER_ID'), min(world.player, 255)) # Write player ID
    rom.write_bytes(rom.sym('AP_PLAYER_NAME'), bytearray(world.connect_name, encoding='ascii'))

    if world.death_link:
        rom.write_byte(rom.sym('DEATH_LINK'), 0x01)

    rom.write_byte(rom.sym('MW_SEND_OWN_ITEMS'), 0x01)

    # Revert Song Get Override Injection
    if not songs_as_items:
        # general get song
        rom.write_int32(0xAE5DF8, 0x240200FF)
        rom.write_int32(0xAE5E04, 0xAD0F00A4)
        # requiem of spirit
        rom.write_int32s(0xAC9ABC, [0x3C010001, 0x00300821])
        # sun song -- commented for AP to always set the relevant bit in event_chk_inf
        # rom.write_int32(0xE09F68, 0x8C6F00A4)
        # rom.write_int32(0xE09F74, 0x01CFC024)
        # rom.write_int32(0xE09FB0, 0x240F0001)
        # song of time
        rom.write_int32(0xDB532C, 0x24050003)


    # Set damage multiplier
    if world.damage_multiplier == 'half':
        rom.write_byte(rom.sym('CFG_DAMAGE_MULTIPLYER'), 0xFF)
    if world.damage_multiplier == 'normal':
        rom.write_byte(rom.sym('CFG_DAMAGE_MULTIPLYER'), 0)
    if world.damage_multiplier == 'double':
        rom.write_byte(rom.sym('CFG_DAMAGE_MULTIPLYER'), 1)
    if world.damage_multiplier == 'quadruple':
        rom.write_byte(rom.sym('CFG_DAMAGE_MULTIPLYER'), 2)
    if world.damage_multiplier == 'ohko':
        rom.write_byte(rom.sym('CFG_DAMAGE_MULTIPLYER'), 3)

    if world.deadly_bonks != 'none':
        rom.write_int32(rom.sym('CFG_DEADLY_BONKS'), 1)
        if world.deadly_bonks == 'half':
            rom.write_int16(rom.sym('CFG_BONK_DAMAGE'), 0x0004)
        if world.deadly_bonks == 'normal':
            rom.write_int16(rom.sym('CFG_BONK_DAMAGE'), 0x0008)
        if world.deadly_bonks == 'double':
            rom.write_int16(rom.sym('CFG_BONK_DAMAGE'), 0x0010)
        if world.deadly_bonks == 'quadruple':
            rom.write_int16(rom.sym('CFG_BONK_DAMAGE'), 0x0020)
        if world.deadly_bonks == 'ohko':
            rom.write_int16(rom.sym('CFG_BONK_DAMAGE'), 0xFFFE)

    # Patch songs and boss rewards
    for location in world.multiworld.get_filled_locations(world.player):
        item = location.item
        special = item.special if item.game == 'Ocarina of Time' else {}  # this shouldn't matter hopefully
        locationaddress = location.address1
        secondaryaddress = location.address2

        if location.type == 'Song' and not songs_as_items:
            bit_mask_pointer = 0x8C34 + ((special['item_id'] - 0x65) * 4)
            rom.write_byte(locationaddress, special['song_id'])
            next_song_id = special['song_id'] + 0x0D
            rom.write_byte(secondaryaddress, next_song_id)
            if location.name == 'Song from Impa':
                rom.write_byte(0x0D12ECB, special['item_id'])
                rom.write_byte(0x2E8E931, special['text_id']) #Fix text box
            elif location.name == 'Song from Malon':
                rom.write_byte(rom.sym('MALON_TEXT_ID'), special['text_id'])
            elif location.name == 'Song from Royal Familys Tomb':
                rom.write_int16(0xE09F66, bit_mask_pointer)
                rom.write_byte(0x332A87D, special['text_id']) #Fix text box
            elif location.name == 'Song from Saria':
                rom.write_byte(0x0E2A02B, special['item_id'])
                rom.write_byte(0x20B1DBD, special['text_id']) #Fix text box
            elif location.name == 'Song from Ocarina of Time':
                rom.write_byte(0x252FC95, special['text_id']) #Fix text box
            elif location.name == 'Song from Windmill':
                rom.write_byte(rom.sym('WINDMILL_SONG_ID'), next_song_id)
                rom.write_byte(rom.sym('WINDMILL_TEXT_ID'), special['text_id'])
            elif location.name == 'Sheik in Forest':
                rom.write_byte(0x0C7BAA3, special['item_id'])
                rom.write_byte(0x20B0815, special['text_id']) #Fix text box
            elif location.name == 'Sheik at Temple':
                rom.write_byte(0x0C805EF, special['item_id'])
                rom.write_byte(0x2531335, special['text_id']) #Fix text box
            elif location.name == 'Sheik in Crater':
                rom.write_byte(0x0C7BC57, special['item_id'])
                rom.write_byte(0x224D7FD, special['text_id']) #Fix text box
            elif location.name == 'Sheik in Ice Cavern':
                rom.write_byte(0x0C7BD77, special['item_id'])
                rom.write_byte(0x2BEC895, special['text_id']) #Fix text box
            elif location.name == 'Sheik in Kakariko':
                rom.write_byte(0x0AC9A5B, special['item_id'])
                rom.write_byte(0x2000FED, special['text_id']) #Fix text box
            elif location.name == 'Sheik at Colossus':
                rom.write_byte(0x218C589, special['text_id']) #Fix text box
        elif location.type == 'Boss':
            if location.name == 'Links Pocket':
                save_context.give_item(world, item.name)
            else:
                rom.write_byte(locationaddress, special['item_id'])
                rom.write_byte(secondaryaddress, special['addr2_data'])
                bit_mask_hi = special['bit_mask'] >> 16
                bit_mask_lo = special['bit_mask'] & 0xFFFF
                if location.name == 'Bongo Bongo':
                    rom.write_int16(0xCA3F32, bit_mask_hi)
                    rom.write_int16(0xCA3F36, bit_mask_lo)
                elif location.name == 'Twinrova':
                    rom.write_int16(0xCA3EA2, bit_mask_hi)
                    rom.write_int16(0xCA3EA6, bit_mask_lo)

    # add a cheaper bombchu pack to the bombchu shop
    # describe
    update_message_by_id(messages, 0x80FE, '\x08\x05\x41Bombchu   (5 pieces)   60 Rupees\x01\x05\x40This looks like a toy mouse, but\x01it\'s actually a self-propelled time\x01bomb!\x09\x0A', 0x03)
    # purchase
    update_message_by_id(messages, 0x80FF, '\x08Bombchu    5 Pieces    60 Rupees\x01\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x09', 0x03)
    rbl_bombchu = shop_items[0x0018]
    rbl_bombchu.price = 60
    rbl_bombchu.pieces = 5
    rbl_bombchu.get_item_id = 0x006A
    rbl_bombchu.description_message = 0x80FE
    rbl_bombchu.purchase_message = 0x80FF

    # Reduce 10 Pack Bombchus from 100 to 99 Rupees
    shop_items[0x0015].price = 99
    shop_items[0x0019].price = 99
    shop_items[0x001C].price = 99
    update_message_by_id(messages, shop_items[0x001C].description_message, "\x08\x05\x41Bombchu  (10 pieces)  99 Rupees\x01\x05\x40This looks like a toy mouse, but\x01it's actually a self-propelled time\x01bomb!\x09\x0A")
    update_message_by_id(messages, shop_items[0x001C].purchase_message, "\x08Bombchu  10 pieces   99 Rupees\x09\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40")

    shuffle_messages.shop_item_messages = []

    # kokiri shop
    shop_locations = [location for location in world.get_region(
        'KF Kokiri Shop').locations if location.type == 'Shop'] # Need to filter because of the freestanding item in KF Shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        shop_locations, True)
    shop_objs |= {0x00FC, 0x00B2, 0x0101, 0x0102, 0x00FD, 0x00C5} # Shop objects
    rom.write_byte(0x2587029, len(shop_objs))
    rom.write_int32(0x258702C, 0x0300F600)
    rom.write_int16s(0x2596600, list(shop_objs))

    # kakariko bazaar
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        world.get_region('Kak Bazaar').locations)
    shop_objs |= {0x005B, 0x00B2, 0x00C5, 0x0107, 0x00C9, 0x016B} # Shop objects
    rom.write_byte(0x28E4029, len(shop_objs))
    rom.write_int32(0x28E402C, 0x03007A40)
    rom.write_int16s(0x28EBA40, list(shop_objs))

    # castle town bazaar
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        world.get_region('Market Bazaar').locations)
    shop_objs |= {0x005B, 0x00B2, 0x00C5, 0x0107, 0x00C9, 0x016B} # Shop objects
    rom.write_byte(bazaar_room_file.start + 0x29, len(shop_objs))
    rom.write_int32(bazaar_room_file.start + 0x2C, 0x03007A40)
    rom.write_int16s(bazaar_room_file.start + 0x7A40, list(shop_objs))

    # goron shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        world.get_region('GC Shop').locations)
    shop_objs |= {0x00C9, 0x00B2, 0x0103, 0x00AF} # Shop objects
    rom.write_byte(0x2D33029, len(shop_objs))
    rom.write_int32(0x2D3302C, 0x03004340)
    rom.write_int16s(0x2D37340, list(shop_objs))

    # zora shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        world.get_region('ZD Shop').locations)
    shop_objs |= {0x005B, 0x00B2, 0x0104, 0x00FE} # Shop objects
    rom.write_byte(0x2D5B029, len(shop_objs))
    rom.write_int32(0x2D5B02C, 0x03004B40)
    rom.write_int16s(0x2D5FB40, list(shop_objs))

    # kakariko potion shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        world.get_region('Kak Potion Shop Front').locations)
    shop_objs |= {0x0159, 0x00B2, 0x0175, 0x0122} # Shop objects
    rom.write_byte(0x2D83029, len(shop_objs))
    rom.write_int32(0x2D8302C, 0x0300A500)
    rom.write_int16s(0x2D8D500, list(shop_objs))

    # market potion shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        world.get_region('Market Potion Shop').locations)
    shop_objs |= {0x0159, 0x00B2, 0x0175, 0x00C5, 0x010C, 0x016B} # Shop objects
    rom.write_byte(0x2DB0029, len(shop_objs))
    rom.write_int32(0x2DB002C, 0x03004E40)
    rom.write_int16s(0x2DB4E40, list(shop_objs))

    # bombchu shop
    shop_objs = place_shop_items(rom, world, shop_items, messages,
        world.get_region('Market Bombchu Shop').locations)
    shop_objs |= {0x0165, 0x00B2} # Shop objects
    rom.write_byte(0x2DD8029, len(shop_objs))
    rom.write_int32(0x2DD802C, 0x03006A40)
    rom.write_int16s(0x2DDEA40, list(shop_objs))

    # Scrub text stuff.
    def update_scrub_text(message, text_replacement, default_price, price, item_name=None):
        scrub_strip_text = ["some ", "1 piece   ", "5 pieces   ", "30 pieces   "]
        for text in scrub_strip_text:
            message = message.replace(text.encode(), b'')
        message = message.replace(text_replacement[0].encode(), text_replacement[1].encode())
        message = message.replace(b'they are', b'it is')
        if default_price != price:
            message = message.replace(('%d Rupees' % default_price).encode(), ('%d Rupees' % price).encode())
        if item_name is not None:
            message = message.replace(b'mysterious item', item_name.encode())
        return message

    single_item_scrubs = {
        0x3E: world.get_location("HF Deku Scrub Grotto"),
        0x77: world.get_location("LW Deku Scrub Near Bridge"),
        0x79: world.get_location("LW Deku Scrub Grotto Front"),
    }

    scrub_message_dict = {}
    if world.shuffle_scrubs == 'off':
        # Revert Deku Scrubs changes
        rom.write_int32s(0xEBB85C, [
            0x24010002, # addiu at, zero, 2
            0x3C038012, # lui v1, 0x8012
            0x14410004, # bne v0, at, 0xd8
            0x2463A5D0, # addiu v1, v1, -0x5a30
            0x94790EF0])# lhu t9, 0xef0(v1)
        rom.write_int32(0xDF7CB0,
            0xA44F0EF0)  # sh t7, 0xef0(v0)

        # Replace scrub text for 3 default shuffled scrubs.
        for (scrub_item, default_price, text_id, text_replacement) in business_scrubs:
            if scrub_item not in single_item_scrubs.keys():
                continue
            scrub_message_dict[text_id] = update_scrub_text(get_message_by_id(messages, text_id).raw_text, text_replacement, default_price, default_price)
    else:
        # Rebuild Business Scrub Item Table
        rom.seek_address(0xDF8684)
        for (scrub_item, default_price, text_id, text_replacement) in business_scrubs:
            price = world.scrub_prices[scrub_item]
            rom.write_int16(None, price)       # Price
            rom.write_int16(None, 1)           # Count
            rom.write_int32(None, scrub_item)  # Item
            rom.write_int32(None, 0x80A74FF8)  # Can_Buy_Func
            rom.write_int32(None, 0x80A75354)  # Buy_Func

            scrub_message_dict[text_id] = update_scrub_text(get_message_by_id(messages, text_id).raw_text, text_replacement, default_price, price)

        # update actor IDs
        set_deku_salesman_data(rom)

    # Update scrub messages.
    shuffle_messages.scrubs_message_ids = []
    for text_id, message in scrub_message_dict.items():
        update_message_by_id(messages, text_id, message)
        if world.shuffle_scrubs == 'random':
            shuffle_messages.scrubs_message_ids.append(text_id)

    if world.shuffle_grotto_entrances:
        # Build the Grotto Load Table based on grotto entrance data
        for entrance in world.get_shuffled_entrances(type='Grotto'):
            if entrance.primary:
                load_table_pointer = rom.sym('GROTTO_LOAD_TABLE') + 4 * entrance.data['grotto_id']
                rom.write_int16(load_table_pointer, entrance.data['entrance'])
                rom.write_byte(load_table_pointer + 2, entrance.data['content'])

        # Update grotto actors based on their new entrance
        set_grotto_shuffle_data(rom, world)

    if world.shuffle_cows:
        rom.write_byte(rom.sym('SHUFFLE_COWS'), 0x01)
        # Move some cows because they are too close from each other in vanilla
        rom.write_bytes(0x33650CA, [0xFE, 0xD3, 0x00, 0x00, 0x00, 0x6E, 0x00, 0x00, 0x4A, 0x34]) # LLR Tower right cow
        rom.write_bytes(0x2C550AE, [0x00, 0x82]) # LLR Stable right cow
        set_cow_id_data(rom, world)

    if world.shuffle_beans:
        rom.write_byte(rom.sym('SHUFFLE_BEANS'), 0x01)
        # Update bean salesman messages to better fit the fact that he sells a randomized item
        update_message_by_id(messages, 0x405E, "\x1AChomp chomp chomp...\x01We have... \x05\x41a mysterious item\x05\x40! \x01Do you want it...huh? Huh?\x04\x05\x41\x0860 Rupees\x05\x40 and it's yours!\x01Keyahahah!\x01\x1B\x05\x42Yes\x01No\x05\x40\x02")
        update_message_by_id(messages, 0x4069, "You don't have enough money.\x01I can't sell it to you.\x01Chomp chomp...\x02")
        update_message_by_id(messages, 0x406C, "We hope you like it!\x01Chomp chomp chomp.\x02")
        # Change first magic bean to cost 60 (is used as the price for the one time item when beans are shuffled)
        rom.write_byte(0xE209FD, 0x3C)

    if world.shuffle_medigoron_carpet_salesman:
        rom.write_byte(rom.sym('SHUFFLE_CARPET_SALESMAN'), 0x01)
        # Update carpet salesman messages to better fit the fact that he sells a randomized item
        update_message_by_id(messages, 0x6077, "\x06\x41Well Come!\x04I am selling stuff, strange and \x01rare, from all over the world to \x01everybody.\x01Today's special is...\x04A mysterious item! \x01Intriguing! \x01I won't tell you what it is until \x01I see the money....\x04How about \x05\x41200 Rupees\x05\x40?\x01\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02")
        update_message_by_id(messages, 0x6078, "Thank you very much!\x04The mark that will lead you to\x01the Spirit Temple is the \x05\x41flag on\x01the left \x05\x40outside the shop.\x01Be seeing you!\x02")

        rom.write_byte(rom.sym('SHUFFLE_MEDIGORON'), 0x01)
        # Update medigoron messages to better fit the fact that he sells a randomized item
        update_message_by_id(messages, 0x304C, "I have something cool right here.\x01How about it...\x07\x30\x4F\x02")
        update_message_by_id(messages, 0x304D, "How do you like it?\x02")
        update_message_by_id(messages, 0x304F, "How about buying this cool item for \x01200 Rupees?\x01\x1B\x05\x42Buy\x01Don't buy\x05\x40\x02")

    if world.shuffle_pots != 'off': # Update the first BK door in ganon's castle to use a separate flag so it can be unlocked to get to the pots
        patch_ganons_tower_bk_door(rom, 0x15) # Using flag 0x15 for the door. GBK doors normally use 0x14.
    locked_doors = get_doors_to_unlock(rom, world)
    for _, [door_byte, door_bits] in locked_doors.items():
        save_context.write_bits(door_byte, door_bits)

    # Fix chest animations
    BROWN_CHEST = 0
    GOLD_CHEST = 2
    GILDED_CHEST = 12
    SILVER_CHEST = 13
    SKULL_CHEST_SMALL = 14
    SKULL_CHEST_BIG =  15
    if world.bombchus_in_logic or world.minor_items_as_major_chest:
        bombchu_ids = [0x6A, 0x03, 0x6B]
        for i in bombchu_ids:
            item = read_rom_item(rom, i)
            item['chest_type'] = GILDED_CHEST
            write_rom_item(rom, i, item)
    if world.bridge == 'tokens' or world.lacs_condition == 'tokens' or world.shuffle_ganon_bosskey == 'tokens':
        item = read_rom_item(rom, 0x5B)
        item['chest_type'] = SKULL_CHEST_BIG
        write_rom_item(rom, 0x5B, item)
    if world.bridge == 'hearts' or world.lacs_condition == 'hearts' or world.shuffle_ganon_bosskey == 'hearts':
        heart_ids = [0x3D, 0x3E, 0x76]
        for i in heart_ids:
            item = read_rom_item(rom, i)
            item['chest_type'] = GILDED_CHEST
            write_rom_item(rom, i, item)
    if world.minor_items_as_major_chest:
        # Deku
        item = read_rom_item(rom, 0x29)
        item['chest_type'] = GILDED_CHEST
        write_rom_item(rom, 0x29, item)
        # Hylian
        item = read_rom_item(rom, 0x2A)
        item['chest_type'] = GILDED_CHEST
        write_rom_item(rom, 0x2A, item)

    # Update chest type appearance
    if world.correct_chest_appearances == 'textures':
        symbol = rom.sym('CHEST_TEXTURE_MATCH_CONTENTS')
        rom.write_int32(symbol, 0x00000001)
    if world.correct_chest_appearances == 'classic':
        symbol = rom.sym('CHEST_SIZE_MATCH_CONTENTS')
        rom.write_int32(symbol, 0x00000001)
    if world.correct_chest_appearances == 'both':
        symbol = rom.sym('CHEST_SIZE_TEXTURE')
        rom.write_int32(symbol, 0x00000001)
        # Move Ganon's Castle's Zelda's Lullaby Chest back so is reachable if large
    if world.correct_chest_appearances == 'classic' or world.correct_chest_appearances == 'both':
        if not world.dungeon_mq['Ganons Castle']:
            chest_name = 'Ganons Castle Light Trial Lullaby Chest'
            location = world.get_location(chest_name)
            if not location.item.trap:
                if location.item.game == 'Ocarina of Time':
                    item = read_rom_item(rom, location.item.index)
                else:
                    item = read_rom_item(rom, AP_PROGRESSION if location.item.advancement else AP_JUNK)
            else:
                looks_like_index = get_override_entry(world, location)[5]
                item = read_rom_item(rom, looks_like_index)
            if item['chest_type'] in (GOLD_CHEST, GILDED_CHEST, SKULL_CHEST_BIG):
                rom.write_int16(0x321B176, 0xFC40) # original 0xFC48

        # Move Spirit Temple Compass Chest if it is a small chest so it is reachable with hookshot
        if not world.dungeon_mq['Spirit Temple']:
            chest_name = 'Spirit Temple Compass Chest'
            chest_address = 0x2B6B07C
            location = world.get_location(chest_name)
            if not location.item.trap:
                if location.item.game == 'Ocarina of Time':
                    item = read_rom_item(rom, location.item.index)
                else:
                    item = read_rom_item(rom, AP_PROGRESSION if location.item.advancement else AP_JUNK)
            else:
                looks_like_index = get_override_entry(world, location)[5]
                item = read_rom_item(rom, looks_like_index)
            if item['chest_type'] in (BROWN_CHEST, SILVER_CHEST, SKULL_CHEST_SMALL):
                rom.write_int16(chest_address + 2, 0x0190) # X pos
                rom.write_int16(chest_address + 6, 0xFABC) # Z pos

        # Move Silver Gauntlets chest if it is small so it is reachable from Spirit Hover Seam
        if world.logic_rules != 'glitchless':
            chest_name = 'Spirit Temple Silver Gauntlets Chest'
            chest_address_0 = 0x21A02D0  # Address in setup 0
            chest_address_2 = 0x21A06E4  # Address in setup 2
            location = world.get_location(chest_name)
            if not location.item.trap:
                if location.item.game == 'Ocarina of Time':
                    item = read_rom_item(rom, location.item.index)
                else:
                    item = read_rom_item(rom, AP_PROGRESSION if location.item.advancement else AP_JUNK)
            else:
                looks_like_index = get_override_entry(world, location)[5]
                item = read_rom_item(rom, looks_like_index)
            if item['chest_type'] in (BROWN_CHEST, SILVER_CHEST, SKULL_CHEST_SMALL):
                rom.write_int16(chest_address_0 + 6, 0x0172)  # Z pos
                rom.write_int16(chest_address_2 + 6, 0x0172)  # Z pos

    # Make all chests invisible
    if world.invisible_chests:
        symbol = rom.sym('CHEST_LENS_ONLY')
        rom.write_int32(symbol, 0x00000001)

    # Update pot type appearance
    ptmc_options = {
        'off': 0,
        'textures_content' : 1,
        'textures_unchecked': 2,
    }
    symbol = rom.sym('POTCRATE_TEXTURES_MATCH_CONTENTS')
    rom.write_byte(symbol, ptmc_options[world.correct_potcrate_appearances])

    # give dungeon items the correct messages
    add_item_messages(messages, shop_items, world)
    if world.enhance_map_compass:
        reward_list = {
            'Kokiri Emerald':   "\x05\x42Kokiri Emerald\x05\x40",
            'Goron Ruby':       "\x05\x41Goron Ruby\x05\x40",
            'Zora Sapphire':    "\x05\x43Zora Sapphire\x05\x40",
            'Forest Medallion': "\x05\x42Forest Medallion\x05\x40",
            'Fire Medallion':   "\x05\x41Fire Medallion\x05\x40",
            'Water Medallion':  "\x05\x43Water Medallion\x05\x40",
            'Spirit Medallion': "\x05\x46Spirit Medallion\x05\x40",
            'Shadow Medallion': "\x05\x45Shadow Medallion\x05\x40",
            'Light Medallion':  "\x05\x44Light Medallion\x05\x40",
        }
        dungeon_list = {
            #                      dungeon name                      boss name        compass map
            'Deku Tree':          ("the \x05\x42Deku Tree",          'Queen Gohma',   0x62, 0x88),
            'Dodongos Cavern':    ("\x05\x41Dodongo\'s Cavern",      'King Dodongo',  0x63, 0x89),
            'Jabu Jabus Belly':   ("\x05\x43Jabu Jabu\'s Belly",     'Barinade',      0x64, 0x8a),
            'Forest Temple':      ("the \x05\x42Forest Temple",      'Phantom Ganon', 0x65, 0x8b),
            'Fire Temple':        ("the \x05\x41Fire Temple",        'Volvagia',      0x7c, 0x8c),
            'Water Temple':       ("the \x05\x43Water Temple",       'Morpha',        0x7d, 0x8e),
            'Spirit Temple':      ("the \x05\x46Spirit Temple",      'Twinrova',      0x7e, 0x8f),
            'Ice Cavern':         ("the \x05\x44Ice Cavern",         None,            0x87, 0x92),
            'Bottom of the Well': ("the \x05\x45Bottom of the Well", None,            0xa2, 0xa5),
            'Shadow Temple':      ("the \x05\x45Shadow Temple",      'Bongo Bongo',   0x7f, 0xa3),
        }
        for dungeon in world.dungeon_mq:
            if dungeon in ['Thieves Hideout', 'Gerudo Training Ground', 'Ganons Castle']:
                pass
            elif dungeon in ['Bottom of the Well', 'Ice Cavern']:
                dungeon_name, boss_name, compass_id, map_id = dungeon_list[dungeon]
                if world.multiworld.players > 1:
                    map_message = "\x13\x76\x08\x05\x42\x0F\x05\x40 found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x09" % (dungeon_name)
                else:
                    map_message = "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x01It\'s %s!\x09" % (dungeon_name, "masterful" if world.dungeon_mq[dungeon] else "ordinary")

                if world.mq_dungeons_random or world.mq_dungeons_count != 0 and world.mq_dungeons_count != 12:
                    update_message_by_id(messages, map_id, map_message)
            else:
                dungeon_name, boss_name, compass_id, map_id = dungeon_list[dungeon]
                if world.multiworld.players > 1:
                    compass_message = "\x13\x75\x08\x05\x42\x0F\x05\x40 found the \x05\x41Compass\x05\x40\x01for %s\x05\x40!\x09" % (dungeon_name)
                elif world.shuffle_bosses != 'off':
                    vanilla_reward = world.get_location(boss_name).vanilla_item
                    vanilla_reward_location = world.multiworld.find_item(vanilla_reward, world.player) # hinted_dungeon_reward_locations[vanilla_reward.name]
                    area = HintArea.at(vanilla_reward_location).text(world.hint_rng, world.clearer_hints, preposition=True)
                    compass_message = "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for %s\x05\x40!\x01The %s can be found\x01%s!\x09" % (dungeon_name, vanilla_reward, area)
                else:
                    boss_location = next(filter(lambda loc: loc.type == 'Boss', world.get_entrance(f'{dungeon} Boss Door -> {boss_name} Boss Room').connected_region.locations))
                    dungeon_reward = reward_list[boss_location.item.name]
                    compass_message = "\x13\x75\x08You found the \x05\x41Compass\x05\x40\x01for %s\x05\x40!\x01It holds the %s!\x09" % (dungeon_name, dungeon_reward)
                update_message_by_id(messages, compass_id, compass_message)
                if world.mq_dungeons_random or world.mq_dungeons_count != 0 and world.mq_dungeons_count != 12:
                    if world.multiworld.players > 1:
                        map_message = "\x13\x76\x08\x05\x42\x0F\x05\x40 found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x09" % (dungeon_name)
                    else:
                        map_message = "\x13\x76\x08You found the \x05\x41Dungeon Map\x05\x40\x01for %s\x05\x40!\x01It\'s %s!\x09" % (dungeon_name, "masterful" if world.dungeon_mq[dungeon] else "ordinary")
                    update_message_by_id(messages, map_id, map_message)

    # Set hints on the altar inside ToT
    rom.write_int16(0xE2ADB2, 0x707A)
    rom.write_int16(0xE2ADB6, 0x7057)
    buildAltarHints(world, messages,
        include_rewards='altar' in world.misc_hints and not world.enhance_map_compass,
        include_wincons='altar' in world.misc_hints)

    # Fix Dead Hand spawn coordinates in vanilla shadow temple and bottom of the well to be the exact centre of the room
    # This prevents the extremely small possibility of Dead Hand spawning outside of collision
    if not world.dungeon_mq['Shadow Temple']:
        rom.write_int16(0x27DC0AE, 0xF67E) # x-coordinate spawn in shadow temple
        rom.write_int16(0x27DC0B2, 0xFE6B) # z-coordinate spawn in shadow temple
    if not world.dungeon_mq['Bottom of the Well']:
        rom.write_int16(0x32FB08E, 0x0500) # x-coordinate spawn in bottom of the well
        rom.write_int16(0x32FB092, 0x00D2) # z-coordinate spawn in bottom of the well

    # update happy mask shop to use new SOLD OUT text id
    rom.write_int16(shop_item_file.start + 0x1726, shop_items[0x26].description_message)

    # Add 3rd Wallet Upgrade
    rom.write_int16(0xB6D57E, 0x0003)
    rom.write_int16(0xB6EC52, 999)
    tycoon_message = "\x08\x13\x57You got a \x05\x43Tycoon's Wallet\x05\x40!\x01Now you can hold\x01up to \x05\x46999\x05\x40 \x05\x46Rupees\x05\x40."
    if world.multiworld.players > 1:
       tycoon_message = make_player_message(tycoon_message)
    update_message_by_id(messages, 0x00F8, tycoon_message, 0x23)

    write_shop_items(rom, shop_item_file.start + 0x1DEC, shop_items)

    # set end credits text to automatically fade without player input,
    # with timing depending on the number of lines in the text box
    for message_id in (0x706F, 0x7091, 0x7092, 0x7093, 0x7094, 0x7095):
        text_codes = []
        chars_in_section = 1
        for code in get_message_by_id(messages, message_id).text_codes:
            if code.code == 0x04: # box-break
                text_codes.append(Text_Code(0x0c, 80 + chars_in_section))
                chars_in_section = 1
            elif code.code == 0x02: # end
                text_codes.append(Text_Code(0x0e, 80 + chars_in_section))
                text_codes.append(code)
            else:
                chars_in_section += 1
                text_codes.append(code)
        update_message_by_id(messages, message_id, ''.join(code.get_string() for code in text_codes))

    permutation = None

    # text shuffle
    if world.text_shuffle == 'except_hints':
        permutation = shuffle_messages(messages, world.random, except_hints=True)
    elif world.text_shuffle == 'complete':
        permutation = shuffle_messages(messages, world.random, except_hints=False)

    # update warp song preview text boxes
    update_warp_song_text(messages, world)

    if world.blue_fire_arrows:
        rom.write_byte(0xC230C1, 0x29) #Adds AT_TYPE_OTHER to arrows to allow collision with red ice
        rom.write_byte(0xDB38FE, 0xEF) #disables ice arrow collision on secondary cylinder for red ice crystals
        rom.write_byte(0xC9F036, 0x10) #enable ice arrow collision on mud walls
        #increase cylinder radius/height for red ice sheets
        rom.write_byte(0xDB391B, 0x50)
        rom.write_byte(0xDB3927, 0x5A)

        bfa_message = "\x08\x13\x0CYou got the \x05\x43Blue Fire Arrow\x05\x40!\x01This is a cool arrow you can\x01use on red ice."
        if world.multiworld.players > 1:
            bfa_message = make_player_message(bfa_message)
        update_message_by_id(messages, 0x0071, bfa_message, 0x23)

        with open(data_path('blue_fire_arrow_item_name_eng.ia4'), 'rb') as stream:
            bfa_name_bytes = stream.read()
            rom.write_bytes(0x8a1c00, bfa_name_bytes)

    repack_messages(rom, messages, permutation)

    # output a text dump, for testing...
    #with open('keysanity_' + str(world.seed) + '_dump.txt', 'w', encoding='utf-16') as f:
    #     messages = read_messages(rom)
    #     f.write('item_message_strings = {\n')
    #     for m in messages:
    #        f.write("\t0x%04X: \"%s\",\n" % (m.id, m.get_python_string()))
    #     f.write('}\n')

    if world.free_scarecrow:
        # Played song as adult
        save_context.write_bits(0x0EE6, 0x10)
        # Direct scarecrow behavior
        symbol = rom.sym('FREE_SCARECROW_ENABLED')
        rom.write_byte(symbol, 0x01)

    # Enable MM-like Bunny Hood behavior (1.5× speed)
    if world.fast_bunny_hood:
        symbol = rom.sym('FAST_BUNNY_HOOD_ENABLED')
        rom.write_byte(symbol, 0x01)

    # actually write the save table to rom
    for (name, count) in world.starting_items.items():
        if count == 0:
            continue
        save_context.give_item(world, name, count)

    if world.fix_broken_drops:
        symbol = rom.sym('FIX_BROKEN_DROPS')
        rom.write_byte(symbol, 0x01)

        # Autocollect incoming_item_id for magic jars are swapped in vanilla code
        rom.write_int16(0xA88066, 0x0044) # Change GI_MAGIC_SMALL to GI_MAGIC_LARGE
        rom.write_int16(0xA88072, 0x0043) # Change GI_MAGIC_LARGE to GI_MAGIC_SMALL
    else:
        # Remove deku shield drop from spirit pot because it's "vanilla behavior"
        # Replace actor parameters in scene 06, room 27 actor list
        rom.write_int16(0x2BDC0C6, 0x603F)

    # Have the Gold Skulltula Count in the pause menu turn red when equal to the
    # available number of skulls in the world instead of 100.
    rom.write_int16(0xBB340E, world.available_tokens)

    # replace_songs(world, rom,
    #     frog=world.ocarina_songs in ('frog', 'all'),
    #     warp=world.ocarina_songs in ('warp', 'all'),
    # )

    # Sets the torch count to open the entrance to Shadow Temple
    if world.easier_fire_arrow_entry:
        torch_count = world.fae_torch_count
        rom.write_byte(0xCA61E3, torch_count)

    if world.blue_fire_arrows:
        rom.write_byte(0xC230C1, 0x29) #Adds AT_TYPE_OTHER to arrows to allow collision with red ice
        rom.write_byte(0xDB38FE, 0xEF) #disables ice arrow collision on secondary cylinder for red ice crystals
        rom.write_byte(0xC9F036, 0x10) #enable ice arrow collision on mud walls
        #increase cylinder radius/height for red ice sheets
        rom.write_byte(0xDB391B, 0x50)
        rom.write_byte(0xDB3927, 0x5A)

    if world.starting_age == 'adult':
        # When starting as adult, the pedestal doesn't handle child default equips when going back child the first time, so we have to equip them ourselves
        save_context.equip_default_items('child')
    save_context.equip_current_items(world.starting_age)
    save_context.write_save_table(rom)

    # Write numeric seed truncated to 32 bits for rng seeding
    # Overwritten with new seed every time a new rng value is generated
    rng_seed = world.random.getrandbits(32)
    rom.write_int32(rom.sym('RNG_SEED_INT'), rng_seed)
    # Static initial seed value for one-time random actions like the Hylian Shield discount
    rom.write_int32(rom.sym('RANDOMIZER_RNG_SEED'), rng_seed)

    # Write data into AP autotracking context
    rom.write_int32(rom.sym('DUNGEON_IS_MQ_ADDRESS'), rom.sym('CFG_DUNGEON_IS_MQ'))
    rom.write_int32(rom.sym('DUNGEON_REWARDS_ADDRESS'), rom.sym('CFG_DUNGEON_REWARDS'))
    rom.write_byte(rom.sym('BIG_POE_COUNT'), world.big_poe_count)
    if world.enhance_map_compass:
        rom.write_byte(rom.sym('ENHANCE_MAP_COMPASS'), 0x01)
    if world.enhance_map_compass or 'altar' in world.misc_hints:
        rom.write_byte(rom.sym('SHOW_DUNGEON_REWARDS'), 0x01)
    if world.shuffle_smallkeys == 'remove':
        rom.write_byte(rom.sym('SMALL_KEY_SHUFFLE'), 0x01)
    elif world.shuffle_smallkeys in ['overworld', 'any_dungeon', 'keysanity', 'regional']:
        rom.write_byte(rom.sym('SMALL_KEY_SHUFFLE'), 0x02)
    if world.shuffle_scrubs != 'off':
        rom.write_byte(rom.sym('SHUFFLE_SCRUBS'), 0x01)
    if world.open_forest == 'closed_deku':
        rom.write_byte(rom.sym('OPEN_FOREST'), 0x01)
    elif world.open_forest == 'closed':
        rom.write_byte(rom.sym('OPEN_FOREST'), 0x02)
    if world.zora_fountain == 'adult':
        rom.write_byte(rom.sym('OPEN_FOUNTAIN'), 0x01)
    elif world.zora_fountain == 'closed':
        rom.write_byte(rom.sym('OPEN_FOUNTAIN'), 0x02)

    rom.write_bytes(rom.sym('SHOP_SLOTS'), [
        sum(f'{shop} Item {idx}' in world.shop_prices for idx in ('7', '5', '8', '6'))
        for shop in ('KF Shop', 'Market Bazaar', 'Market Potion Shop', 'Market Bombchu Shop', 
            'Kak Bazaar', 'Kak Potion Shop', 'GC Shop', 'ZD Shop')
    ])

    return rom


NUM_VANILLA_OBJECTS = 0x192
def add_to_extended_object_table(rom, object_id, object_file):
    extended_id = object_id - NUM_VANILLA_OBJECTS - 1
    extended_object_table = rom.sym('EXTENDED_OBJECT_TABLE')
    rom.write_int32s(extended_object_table + extended_id * 8, [object_file.start, object_file.end])


item_row_struct = struct.Struct('>BBHHBBIIhhBxxx') # Match item_row_t in item_table.h
item_row_fields = [
    'base_item_id', 'action_id', 'text_id', 'object_id', 'graphic_id', 'chest_type',
    'upgrade_fn', 'effect_fn', 'effect_arg1', 'effect_arg2', 'collectible'
]


def read_rom_item(rom, item_id):
    addr = rom.sym('item_table') + (item_id * item_row_struct.size)
    row_bytes = rom.read_bytes(addr, item_row_struct.size)
    row = item_row_struct.unpack(row_bytes)
    return { item_row_fields[i]: row[i] for i in range(len(item_row_fields)) }


def write_rom_item(rom, item_id, item):
    addr = rom.sym('item_table') + (item_id * item_row_struct.size)
    row = [item[f] for f in item_row_fields]
    row_bytes = item_row_struct.pack(*row)
    rom.write_bytes(addr, row_bytes)


texture_struct = struct.Struct('>HBxxxxxII') # Match texture_t in textures.c
texture_fields = ['texture_id', 'file_buf', 'file_vrom_start', 'file_size']

def read_rom_texture(rom, texture_id):
    addr = rom.sym('texture_table') + (texture_id * texture_struct.size)
    row_bytes = rom.read_bytes(addr, texture_struct.size)
    row = texture_struct.unpack(row_bytes)
    return {texture_fields[i]: row[i] for i in range(len(texture_fields))}
def write_rom_texture(rom, texture_id, texture):
    addr = rom.sym('texture_table') + (texture_id * texture_struct.size)
    row = [texture[f] for f in texture_fields]
    row_bytes = texture_struct.pack(*row)
    rom.write_bytes(addr, row_bytes)


def get_override_table(world):
    return list(filter(lambda val: val != None, map(partial(get_override_entry, world), world.multiworld.get_filled_locations(world.player))))


override_struct = struct.Struct('>BBHHBB') # match override_t in get_items.c
def get_override_table_bytes(override_table):
    return b''.join(sorted(itertools.starmap(override_struct.pack, override_table)))


def get_override_entry(ootworld, location):
    # Don't add freestanding items, pots/crates, beehives to the override table if they're disabled. We use this check to determine how to draw and interact with them
    if location.type in ["ActorOverride", "Freestanding", "RupeeTower", "Pot", "Crate", "FlyingPot", "SmallCrate", "Beehive"] and location.disabled != DisableType.ENABLED:
        return None

    scene = location.scene
    default = location.default
    player_id = 0 if ootworld.player == location.item.player else min(location.item.player, 255)
    if location.item.game != 'Ocarina of Time': 
        # This is an AP sendable. It's guaranteed to not be None. 
        if location.item.advancement:
            item_id = AP_PROGRESSION
        else:
            item_id = AP_JUNK
    else: 
        item_id = location.item.index
        if None in [scene, default, item_id]:
            return None

    if location.item.trap:
        item_id = 0x7C  # Ice Trap ID, to get "X is a fool" message
        looks_like_item_id = ootworld.trap_appearances[location.address].index
    else:
        looks_like_item_id = 0

    if location.type in ['NPC', 'Scrub', 'BossHeart']:
        type = 0
    elif location.type == 'Chest':
        type = 1
        default &= 0x1F
    elif location.type in ['Freestanding', 'Pot', 'Crate', 'FlyingPot', 'SmallCrate', 'RupeeTower', 'Beehive']:
        type = 6
        if not (isinstance(location.default, list) or isinstance(location.default, tuple)):
            raise Exception("Not right")
        if(isinstance(location.default, list)):
            default = location.default[0]
        room, scene_setup, flag = default
        default = (room << 8) + (scene_setup << 14) + flag
    elif location.type in ['Collectable', 'ActorOverride']:
        type = 2
    elif location.type == 'GS Token':
        type = 3
    elif location.type == 'Shop' and not (isinstance(location.item, OOTItem) and location.item.type == 'Shop'):
        type = 0
    elif location.type == 'GrottoScrub' and not (isinstance(location.item, OOTItem) and location.item.type == 'Shop'):
        type = 4
    elif location.type in ['Song', 'Cutscene']:
        type = 5
    else:
        return None

    return (scene, type, default, item_id, player_id, looks_like_item_id)


chestTypeMap = {
        #    small   big     boss
    0x0000: [0x5000, 0x0000, 0x2000], #Large
    0x1000: [0x7000, 0x1000, 0x1000], #Large, Appears, Clear Flag
    0x2000: [0x5000, 0x0000, 0x2000], #Boss Key’s Chest
    0x3000: [0x8000, 0x3000, 0x3000], #Large, Falling, Switch Flag
    0x4000: [0x6000, 0x4000, 0x4000], #Large, Invisible
    0x5000: [0x5000, 0x0000, 0x2000], #Small
    0x6000: [0x6000, 0x4000, 0x4000], #Small, Invisible
    0x7000: [0x7000, 0x1000, 0x1000], #Small, Appears, Clear Flag
    0x8000: [0x8000, 0x3000, 0x3000], #Small, Falling, Switch Flag
    0x9000: [0x9000, 0x9000, 0x9000], #Large, Appears, Zelda's Lullaby
    0xA000: [0xA000, 0xA000, 0xA000], #Large, Appears, Sun's Song Triggered
    0xB000: [0xB000, 0xB000, 0xB000], #Large, Appears, Switch Flag
    0xC000: [0x5000, 0x0000, 0x2000], #Large
    0xD000: [0x5000, 0x0000, 0x2000], #Large
    0xE000: [0x5000, 0x0000, 0x2000], #Large
    0xF000: [0x5000, 0x0000, 0x2000], #Large
}


def room_get_actors(rom, actor_func, room_data, scene, alternate=None):
    actors = {}
    room_start = alternate if alternate else room_data
    command = 0
    while command != 0x14: # 0x14 = end header
        command = rom.read_byte(room_data)
        if command == 0x01: # actor list
            actor_count = rom.read_byte(room_data + 1)
            actor_list = room_start + (rom.read_int32(room_data + 4) & 0x00FFFFFF)
            for _ in range(0, actor_count):
                actor_id = rom.read_int16(actor_list)
                entry = actor_func(rom, actor_id, actor_list, scene)
                if entry:
                    actors[actor_list] = entry
                actor_list = actor_list + 16
        if command == 0x18: # Alternate header list
            header_list = room_start + (rom.read_int32(room_data + 4) & 0x00FFFFFF)
            for alt_id in range(0,3):
                header_data = room_start + (rom.read_int32(header_list) & 0x00FFFFFF)
                if header_data != 0 and not alternate:
                    actors.update(room_get_actors(rom, actor_func, header_data, scene, room_start))
                header_list = header_list + 4
        room_data = room_data + 8
    return actors


def scene_get_actors(rom, actor_func, scene_data, scene, alternate=None, processed_rooms=None):
    if processed_rooms == None:
        processed_rooms = []
    actors = {}
    scene_start = alternate if alternate else scene_data
    command = 0
    while command != 0x14: # 0x14 = end header
        command = rom.read_byte(scene_data)
        if command == 0x04: #room list
            room_count = rom.read_byte(scene_data + 1)
            room_list = scene_start + (rom.read_int32(scene_data + 4) & 0x00FFFFFF)
            for _ in range(0, room_count):
                room_data = rom.read_int32(room_list)

                if not room_data in processed_rooms:
                    actors.update(room_get_actors(rom, actor_func, room_data, scene))
                    processed_rooms.append(room_data)
                room_list = room_list + 8
        if command == 0x0E: #transition actor list
            actor_count = rom.read_byte(scene_data + 1)
            actor_list = scene_start + (rom.read_int32(scene_data + 4) & 0x00FFFFFF)
            for _ in range(0, actor_count):
                actor_id = rom.read_int16(actor_list + 4)
                entry = actor_func(rom, actor_id, actor_list, scene)
                if entry:
                    actors[actor_list] = entry
                actor_list = actor_list + 16
        if command == 0x18: # Alternate header list
            header_list = scene_start + (rom.read_int32(scene_data + 4) & 0x00FFFFFF)
            for alt_id in range(0,3):
                header_data = scene_start + (rom.read_int32(header_list) & 0x00FFFFFF)
                if header_data != 0 and not alternate:
                    actors.update(scene_get_actors(rom, actor_func, header_data, scene, scene_start, processed_rooms))
                header_list = header_list + 4

        scene_data = scene_data + 8
    return actors


def get_actor_list(rom, actor_func):
    actors = {}
    scene_table = 0x00B71440
    for scene in range(0x00, 0x65):
        scene_data = rom.read_int32(scene_table + (scene * 0x14))
        actors.update(scene_get_actors(rom, actor_func, scene_data, scene))
    return actors


def get_override_itemid(override_table, scene, type, flags):
    for entry in override_table:
        if entry[0] == scene and (entry[1] & 0x07) == type and entry[2] == flags:
            return entry[4]
    return None

def remove_entrance_blockers(rom):
    def remove_entrance_blockers_do(rom, actor_id, actor, scene):
        if actor_id == 0x014E and scene == 97:
            actor_var = rom.read_int16(actor + 14)
            if actor_var == 0xFF01:
                rom.write_int16(actor + 14, 0x0700)
    get_actor_list(rom, remove_entrance_blockers_do)

def set_cow_id_data(rom, world):
    def set_cow_id(rom, actor_id, actor, scene):
        nonlocal last_scene
        nonlocal cow_count
        nonlocal last_actor

        if actor_id == 0x01C6: #Cow
            if scene == last_scene and last_actor != actor:
                cow_count += 1
            else:
                cow_count = 1

            last_scene = scene
            last_actor = actor
            if world.dungeon_mq['Jabu Jabus Belly'] and scene == 2: #If its an MQ jabu cow
                rom.write_int16(actor + 0x8, 1 if cow_count == 17 else 0) #Give all wall cows ID 0, and set cow 11's ID to 1
            else:
                rom.write_int16(actor + 0x8, cow_count)

    last_actor = -1
    last_scene = -1
    cow_count = 1

    get_actor_list(rom, set_cow_id)


def set_grotto_shuffle_data(rom, world):
    def override_grotto_data(rom, actor_id, actor, scene):
        if actor_id == 0x009B: #Grotto
            actor_zrot = rom.read_int16(actor + 12)
            actor_var = rom.read_int16(actor + 14)
            grotto_type = (actor_var >> 8) & 0x0F
            grotto_actor_id = (scene << 8) + (actor_var & 0x00FF)

            rom.write_int16(actor + 12, grotto_entrances_override[grotto_actor_id])
            rom.write_byte(actor + 14, grotto_type + 0x20)

    # Build the override table based on shuffled grotto entrances
    grotto_entrances_override = {}
    for entrance in world.get_shuffled_entrances(type='Grotto'):
        if entrance.primary:
            grotto_actor_id = (entrance.data['scene'] << 8) + entrance.data['content']
            grotto_entrances_override[grotto_actor_id] = entrance.replaces.data['index']
        else:
            rom.write_int16(rom.sym('GROTTO_EXIT_LIST') + 2 * entrance.data['grotto_id'], entrance.replaces.data['index'])

    # Override grotto actors data with the new data
    get_actor_list(rom, override_grotto_data)


def set_deku_salesman_data(rom):
    def set_deku_salesman(rom, actor_id, actor, scene):
        if actor_id == 0x0195: #Salesman
            actor_var = rom.read_int16(actor + 14)
            if actor_var == 6:
                rom.write_int16(actor + 14, 0x0003)

    get_actor_list(rom, set_deku_salesman)


def set_jabu_stone_actors(rom, jabu_actor_type):
    def set_jabu_stone_actor(rom, actor_id, actor, scene):
        if scene == 2 and actor_id == 0x008B: # Demo_Effect in Jabu Jabu
            actor_type = rom.read_byte(actor + 15)
            if actor_type == 0x15:
                rom.write_byte(actor + 15, jabu_actor_type)

    get_actor_list(rom, set_jabu_stone_actor)


def set_spirit_shortcut_actors(rom):
    def set_spirit_shortcut(rom, actor_id, actor, scene):
        if actor_id == 0x018e and scene == 6: # raise initial elevator height
            rom.write_int16(actor + 4, 0x015E)

    get_actor_list(rom, set_spirit_shortcut)


# Gets a dict of doors to unlock based on settings
# Returns: dict with entries address: [byte_offset, bit]
# Where:    address = rom address of the door
#           byte_offset = the offset, in bytes, of the door flag in the SaveContext
#           bit = the bit offset within the byte for the door flag
# If small keys are set to remove, returns all small key doors
# If boss keys are set to remove, returns boss key doors
# If ganons boss key is set to remove, returns ganons boss key doors
# If pot/crate shuffle is enabled, returns the first ganon's boss key door so that it can be unlocked separately to allow access to the room w/ the pots..
def get_doors_to_unlock(rom, world):
    def get_door_to_unlock(rom, actor_id, actor, scene):
        actor_var = rom.read_int16(actor + 14)
        door_type = actor_var >> 6
        switch_flag = actor_var & 0x003F

        flag_id = (1 << switch_flag)
        flag_byte = 3 - (switch_flag >> 3)
        flag_bits = 1 << (switch_flag & 0x07)

        # Return small key doors that should be unlocked
        if world.shuffle_smallkeys == 'remove':
            if actor_id == 0x0009 and door_type == 0x02:
                return [0x00D4 + scene * 0x1C + 0x04 + flag_byte, flag_bits]
            if actor_id == 0x002E and door_type == 0x0B:
                return [0x00D4 + scene * 0x1C + 0x04 + flag_byte, flag_bits]

        # Return Boss Doors that should be unlocked
        if (world.shuffle_bosskeys == 'remove' and scene != 0x0A) or (world.shuffle_ganon_bosskey == 'remove' and scene == 0x0A) or (world.shuffle_pots and scene == 0x0A and switch_flag == 0x15):
            if actor_id == 0x002E and door_type == 0x05:
                return [0x00D4 + scene * 0x1C + 0x04 + flag_byte, flag_bits]

    return get_actor_list(rom, get_door_to_unlock)


# Too difficult to keep the censor around with arbitrary item names being passed in here.
def create_fake_name(item_name):
    return item_name + "???"


def place_shop_items(rom, world, shop_items, messages, locations, init_shop_id=False):
    if init_shop_id:
        world.current_shop_id = 0x32

    shop_objs = { 0x0148 } # "Sold Out" object
    for location in locations:
        if isinstance(location.item, OOTItem) and location.item.type == 'Shop':
            shop_objs.add(location.item.special['object'])
            rom.write_int16(location.address1, location.item.index)
        else:
            if location.item.trap:
                item_display = world.trap_appearances[location.address]
            else:
                item_display = location.item

            # bottles in shops should look like empty bottles
            # so that that are different than normal shop refils
            if location.item.trap or location.item.game == "Ocarina of Time":
                if 'shop_object' in item_display.special:
                    rom_item = read_rom_item(rom, item_display.special['shop_object'])
                else:
                    rom_item = read_rom_item(rom, item_display.index)
            else:
                display_index = AP_PROGRESSION if location.item.advancement else AP_JUNK
                rom_item = read_rom_item(rom, display_index)

            shop_objs.add(rom_item['object_id'])
            shop_id = world.current_shop_id
            rom.write_int16(location.address1, shop_id)
            shop_item = shop_items[shop_id]

            shop_item.object = rom_item['object_id']
            shop_item.model = rom_item['graphic_id'] - 1
            shop_item.price = location.price
            shop_item.pieces = 1
            shop_item.get_item_id = location.default
            shop_item.func1 = 0x808648CC
            shop_item.func2 = 0x808636B8
            shop_item.func3 = 0x00000000
            shop_item.func4 = 0x80863FB4

            message_id = (shop_id - 0x32) * 2
            shop_item.description_message = 0x8100 + message_id
            shop_item.purchase_message = 0x8100 + message_id + 1

            shuffle_messages.shop_item_messages.extend(
                [shop_item.description_message, shop_item.purchase_message])

            if getattr(item_display, 'dungeonitem', False) and location.item.game == "Ocarina of Time":
                split_item_name = item_display.name.split('(')
                split_item_name[1] = '(' + split_item_name[1]

                if location.item.name == 'Ice Trap':
                    split_item_name[0] = create_fake_name(split_item_name[0])

                if len(world.multiworld.worlds) > 1: # OOTWorld.MultiWorld.AutoWorld[]
                    description_text = '\x08\x05\x41%s  %d Rupees\x01%s\x01\x05\x42%s\x05\x40\x01Special deal! ONE LEFT!\x09\x0A\x02' % (split_item_name[0], location.price, split_item_name[1], rom_safe_text(world.multiworld.get_player_name(location.item.player)))
                else:
                    description_text = '\x08\x05\x41%s  %d Rupees\x01%s\x01\x05\x40Special deal! ONE LEFT!\x01Get it while it lasts!\x09\x0A\x02' % (split_item_name[0], location.price, split_item_name[1])
                purchase_text = '\x08%s  %d Rupees\x09\x01%s\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x02' % (split_item_name[0], location.price, split_item_name[1])
            else:
                if item_display.game == "Ocarina of Time":
                    shop_item_name = getSimpleHintNoPrefix(item_display, world.random)
                else:
                    shop_item_name = item_display.name

                if location.item.trap:
                    shop_item_name = create_fake_name(shop_item_name)

                if len(world.multiworld.worlds) > 1:
                    shop_item_name = rom_safe_text(shop_item_name)
                    do_line_break = sum(character_table[char] for char in f"{shop_item_name}  {location.price} Rupees") > NORMAL_LINE_WIDTH
                    description_text = '\x08\x05\x41%s%s%d Rupees\x01\x05\x42%s\x05\x40\x01Special deal! ONE LEFT!\x09\x0A\x02' % (shop_item_name, '\x01' if do_line_break else '  ', location.price, rom_safe_text(world.multiworld.get_player_name(location.item.player)))
                else:
                    description_text = '\x08\x05\x41%s  %d Rupees\x01\x05\x40Special deal! ONE LEFT!\x01Get it while it lasts!\x09\x0A\x02' % (shop_item_name, location.price)
                purchase_text = '\x08%s  %d Rupees\x09\x01\x01\x1B\x05\x42Buy\x01Don\'t buy\x05\x40\x02' % (shop_item_name, location.price)

            update_message_by_id(messages, shop_item.description_message, description_text, 0x03)
            update_message_by_id(messages, shop_item.purchase_message, purchase_text, 0x03)

        if any(filter(lambda c: c in location.name, {'5', '6', '7', '8'})):
            world.current_shop_id += 1

    return shop_objs


def boss_reward_index(item):
    code = item.special['item_id']
    if code >= 0x6C:
        return code - 0x6C
    else:
        return 3 + code - 0x66


def configure_dungeon_info(rom, world):
    mq_enable = (world.mq_dungeons_mode == 'random' or world.mq_dungeons_random or world.mq_dungeons_count != 0 and world.mq_dungeons_count != 12)
    enhance_map_compass = world.enhance_map_compass

    codes = ['Deku Tree', 'Dodongos Cavern', 'Jabu Jabus Belly', 'Forest Temple',
             'Fire Temple', 'Water Temple', 'Spirit Temple', 'Shadow Temple',
             'Bottom of the Well', 'Ice Cavern', 'Tower (N/A)',
             'Gerudo Training Ground', 'Hideout (N/A)', 'Ganons Castle']

    dungeon_rewards = [0xff] * 14
    dungeon_reward_areas = bytearray()
    for reward in ('Kokiri Emerald', 'Goron Ruby', 'Zora Sapphire', 'Light Medallion', 'Forest Medallion', 'Fire Medallion', 'Water Medallion', 'Shadow Medallion', 'Spirit Medallion'):
        location = next(filter(lambda loc: loc.item.name == reward, world.multiworld.get_filled_locations(player=world.player)))
        area = HintArea.at(location)
        dungeon_reward_areas += area.short_name.encode('ascii').ljust(0x16) + b'\0'
        if area.is_dungeon:
            dungeon_rewards[codes.index(area.dungeon_name)] = boss_reward_index(location.item)

    dungeon_is_mq = [1 if world.dungeon_mq.get(c) else 0 for c in codes]

    rom.write_int32(rom.sym('CFG_DUNGEON_INFO_ENABLE'), 2)
    rom.write_int32(rom.sym('CFG_DUNGEON_INFO_MQ_ENABLE'), int(mq_enable))
    rom.write_int32(rom.sym('CFG_DUNGEON_INFO_MQ_NEED_MAP'), int(enhance_map_compass))
    rom.write_int32(rom.sym('CFG_DUNGEON_INFO_REWARD_ENABLE'), int('altar' in world.misc_hints or enhance_map_compass))
    rom.write_int32(rom.sym('CFG_DUNGEON_INFO_REWARD_NEED_COMPASS'), (2 if False else 1) if enhance_map_compass else 0) #TODO set to 2 if boss reward shuffle and/or mixed pools bosses are on
    rom.write_int32(rom.sym('CFG_DUNGEON_INFO_REWARD_NEED_ALTAR'), int(not enhance_map_compass))
    # if hasattr(world, 'mix_entrance_pools'):
    #     rom.write_int32(rom.sym('CFG_DUNGEON_INFO_REWARD_SUMMARY_ENABLE'), int('Boss' not in world.mix_entrance_pools))
    rom.write_bytes(rom.sym('CFG_DUNGEON_REWARDS'), dungeon_rewards)
    rom.write_bytes(rom.sym('CFG_DUNGEON_IS_MQ'), dungeon_is_mq)
    rom.write_bytes(rom.sym('CFG_DUNGEON_REWARD_AREAS'), dungeon_reward_areas)

# Overwrite an actor in rom w/ the actor data from LocationList
def patch_actor_override(location, rom: Rom):
    addresses = location.address1
    patch = location.address2
    if addresses is not None and patch is not None:
        for address in addresses:
            rom.write_bytes(address, patch)

# Patch rupee towers (circular patterns of rupees) to include their flag in their actor initialization data z rotation.
# Also used for goron pot, shadow spinning pots
def patch_rupee_tower(location, rom: Rom):
    flag = location.default
    if(isinstance(location.default, tuple)):
        room, scene_setup, flag = location.default
    elif isinstance(location.default, list):
        room, scene_setup, flag = location.default[0]
    flag = flag + (room << 8)
    if location.address1:
        for address in location.address1:
            rom.write_bytes(address + 12, flag.to_bytes(2, byteorder='big'))

# Patch the first boss key door in ganons tower that leads to the room w/ the pots
def patch_ganons_tower_bk_door(rom: Rom, flag):
    var = (0x05 << 6) + (flag & 0x3F)
    bytes = [(var & 0xFF00) >> 8, var & 0xFF]
    rom.write_bytes(0x2EE30FE, bytes)
