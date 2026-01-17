import hashlib
import io
import os
from typing import TYPE_CHECKING, Any, Dict, List, Iterable, TypedDict, Callable

import json
import pathlib
import pkgutil
import settings
import Utils
from Utils import read_snes_rom, snes_to_pc
from worlds.Files import APProcedurePatch, APPatchExtension

from .ips import IPS_Patch
if TYPE_CHECKING:
    from . import SMMapRandoWorld

SMJUHASH = '21f3e98df4780ee1c667b84e57d88675'
SMMR_ROM_MAX_PLAYERID = 65535
SMMR_ROM_PLAYERDATA_COUNT = 202

class SMMapRandoProcedurePatch(APProcedurePatch):
    hash = SMJUHASH
    game = "Super Metroid Map Rando"
    patch_file_ending = ".apsmmr"
    result_file_ending = ".sfc"

    procedure = [
        ("patch_rom", ["rando_data.json"]),
        ("apply_ips", []),
        ("write_crc", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

class SMMapRandoPatchExtensions(APPatchExtension):
    game = "Super Metroid Map Rando"

    @staticmethod
    def patch_rom(caller: SMMapRandoProcedurePatch, rom: bytes, rando_data_file: str) -> bytes:
        from Generate import roll_settings
        from pysmmaprando import CustomizeRequest, customize_seed_ap, validate_settings_ap
        from . import map_rando_app_data

        randomizer_data = json.loads(caller.get_file(rando_data_file).decode("utf-8"))

        wrapped_options = {
            "name": caller.player_name,
            "game": "Super Metroid Map Rando",
            "Super Metroid Map Rando": randomizer_data["customize_settings"]
        }

        customize_settings = roll_settings(wrapped_options)
        customize_request = CustomizeRequest(
            rom,
            "",
            f"{customize_settings.etank_color_red.value:02X}{customize_settings.etank_color_green.value:02X}{customize_settings.etank_color_blue.value:02X}",
            current_key_pascal(customize_settings.item_dot_change),
            customize_settings.transition_letters == 1,
            bool(customize_settings.reserve_hud_style.value),
            customize_settings.room_palettes.current_key,
            current_key_pascal(customize_settings.tile_theme),
            customize_settings.door_colors.current_key,
            customize_settings.music.current_key,
            bool(customize_settings.disable_beeping.value),
            customize_settings.screen_shaking.current_key.title(),
            customize_settings.screen_flashing.current_key.title(),
            bool(customize_settings.screw_attack_animation.value),
            bool(customize_settings.room_names.value),
            customize_settings.shot.current_key.title(),
            customize_settings.jump.current_key.title(),
            customize_settings.dash.current_key.title(),
            customize_settings.item_select.current_key.title(),
            customize_settings.item_cancel.current_key.title(),
            customize_settings.angle_up.current_key.title(),
            customize_settings.angle_down.current_key.title(),
            "on" if "Left" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "Right" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "Up" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "Down" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "X" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "Y" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "A" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "B" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "L" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "R" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "Select" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "Start" in customize_settings.spin_lock_buttons.value else "off",
            "on" if "Left" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "Right" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "Up" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "Down" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "X" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "Y" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "A" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "B" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "L" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "R" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "Select" in customize_settings.quick_reload_buttons.value else "off",
            "on" if "Start" in customize_settings.quick_reload_buttons.value else "off",
            bool(customize_settings.moonwalk.value)
        )

        patched_rom_bytes = customize_seed_ap(
            customize_request,
            map_rando_app_data,
            validate_settings_ap(json.dumps(randomizer_data["map_rando_settings"]), map_rando_app_data),
            randomizer_data["randomization"]
        )
        return patched_rom_bytes

    @staticmethod
    def apply_ips(caller: SMMapRandoProcedurePatch, rom: bytes, *ips_patches: str) -> bytes:
        basepatch_ips = IPS_Patch.load("/".join(("data", "SMBasepatch_prebuilt", "multiworld-basepatch.ips")))
        patched_rom_bytes = basepatch_ips.apply(rom)

        for ips in [IPS_Patch.decode(io.BytesIO(caller.get_file(f"{patch}.ips"))) for patch in ips_patches]:
            patched_rom_bytes = ips.apply(patched_rom_bytes)

        return patched_rom_bytes

    @staticmethod
    def write_crc(caller: SMMapRandoProcedurePatch, rom: bytes) -> bytes:
        def checksum_mirror_sum(start, length, mask = 0x800000):
            while not(length & mask) and mask:
                mask >>= 1

            part1 = sum(start[:mask]) & 0xFFFF
            part2 = 0

            next_length = length - mask
            if next_length:
                part2 = checksum_mirror_sum(start[mask:], next_length, mask >> 1)

                while (next_length < mask):
                    next_length += next_length
                    part2 += part2

            return (part1 + part2) & 0xFFFF

        def write_bytes(buffer, startaddress: int, values):
            buffer[startaddress:startaddress + len(values)] = values

        buffer = bytearray(rom)
        crc = checksum_mirror_sum(buffer, len(buffer))
        inv = crc ^ 0xFFFF
        write_bytes(buffer, 0x7FDC, [inv & 0xFF, (inv >> 8) & 0xFF, crc & 0xFF, (crc >> 8) & 0xFF])
        return bytes(buffer)

class ByteEdit(TypedDict):
    sym: Dict[str, Any]
    offset: int
    values: Iterable[int]

def make_ips_patches(world: "SMMapRandoWorld", match_item: Callable) -> dict[str, IPS_Patch]:
    from . import locations_start_id, items_start_id, required_pysmmaprando_version
    patches = dict()
    symbols = get_sm_symbols("/".join(("data", "SMBasepatch_prebuilt", "sm-basepatch-symbols.json")))

    # gather all player ids and names relevant to this rom, then write player name and player id data tables
    playerIdSet: Set[int] = {0}  # 0 is for "Archipelago" server
    for itemLoc in world.multiworld.get_locations():
        assert itemLoc.item, f"World of player '{world.multiworld.player_name[itemLoc.player]}' has a loc.item " + \
                             f"that is {itemLoc.item} during generate_output"
        # add each playerid who has a location containing an item to send to us *or* to an item_link we're part of
        if itemLoc.item.player == world.player or \
                (itemLoc.item.player in world.multiworld.groups and
                 world.player in world.multiworld.groups[itemLoc.item.player]['players']):
            playerIdSet |= {itemLoc.player}
        # add each playerid, including item link ids, that we'll be sending items to
        if itemLoc.player == world.player:
            playerIdSet |= {itemLoc.item.player}
    if len(playerIdSet) > SMMR_ROM_PLAYERDATA_COUNT:
        # max 202 entries, but it's possible for item links to add enough replacement items for us, that are placed
        # in worlds that otherwise have no relation to us, that the 2*location count limit is exceeded
        logger.warning("SMMR is interacting with too many players to fit in ROM. "
                       f"Removing the highest {len(playerIdSet) - SMMR_ROM_PLAYERDATA_COUNT} ids to fit")
        playerIdSet = set(sorted(playerIdSet)[:SMMR_ROM_PLAYERDATA_COUNT])
    otherPlayerIndex: Dict[int, int] = {}  # ap player id -> rom-local player index
    playerNameData: List[ByteEdit] = []
    playerIdData: List[ByteEdit] = []
    # sort all player data by player id so that the game can look up a player's data reasonably quickly when
    # the client sends an ap playerid to the game
    for i, playerid in enumerate(sorted(playerIdSet)):
        playername = world.multiworld.player_name[playerid] if playerid != 0 else "Archipelago"
        playerIdForRom = playerid
        if playerid > SMMR_ROM_MAX_PLAYERID:
            # note, playerIdForRom = 0 is not unique so the game cannot look it up.
            # instead it will display the player received-from as "Archipelago"
            playerIdForRom = 0
            if playerid == world.player:
                raise Exception(f"SM rom cannot fit enough bits to represent self player id {playerid}")
            else:
                logger.warning(f"SM rom cannot fit enough bits to represent player id {playerid}, setting to 0 in rom")
        otherPlayerIndex[playerid] = i
        playerNameData.append({"sym": symbols["rando_player_name_table"],
                               "offset": i * 16,
                               "values": playername[:16].upper().center(16).encode()})
        playerIdData.append({"sym": symbols["rando_player_id_table"],
                             "offset": i * 2,
                             "values": getWordArray(playerIdForRom)})

    multiWorldLocations: List[ByteEdit] = []
    multiWorldItems: List[ByteEdit] = []
    idx = 0
    vanillaItemTypesCount = 23
    locations_nothing = bytearray(20)
    for itemLoc in world.multiworld.get_locations():
        if itemLoc.player != world.player:
            continue

        # item to place in this SMMR world: write full item data to tables
        if itemLoc.item.player == world.player:
            matched_item_code = itemLoc.item.code
        else:
            matched_item_code = match_item(world, itemLoc.item)
        matched_item_code -= items_start_id

        if matched_item_code < vanillaItemTypesCount:
            if matched_item_code == world.nothing_item_id:
                locations_nothing[(itemLoc.address - locations_start_id)//8] |= 1 << (itemLoc.address % 8)
            itemId = matched_item_code
        else:
            itemId = world.item_name_to_id['ArchipelagoItem'] - items_start_id + idx
            multiWorldItems.append({"sym": symbols["message_item_names"],
                                    "offset": (vanillaItemTypesCount + idx)*64,
                                    "values": convertToROMItemName(itemLoc.item.name)})
            idx += 1

        if itemLoc.item.player == world.player:
            itemDestinationType = 0  # dest type 0 means 'regular old SM item' per itemtable.asm
        elif itemLoc.item.player in world.multiworld.groups and \
                world.player in world.multiworld.groups[itemLoc.item.player]['players']:
            # dest type 2 means 'SM item link item that sends to the current player and others'
            # per itemtable.asm (groups are synonymous with item_links, currently)
            itemDestinationType = 2
        else:
            itemDestinationType = 1  # dest type 1 means 'item for entirely someone else' per itemtable.asm

        [w0, w1] = getWordArray(itemDestinationType)
        [w2, w3] = getWordArray(itemId)
        [w4, w5] = getWordArray(otherPlayerIndex[itemLoc.item.player] if itemLoc.item.player in
                                     otherPlayerIndex else 0)
        [w6, w7] = getWordArray(0 if itemLoc.item.advancement else 1)
        multiWorldLocations.append({"sym": symbols["rando_item_table"],
                                    "offset": (itemLoc.address - locations_start_id)*8,
                                    "values": [w0, w1, w2, w3, w4, w5, w6, w7]})

    itemSprites = [{"fileName":          "off_world_prog_item.bin",
                    "paletteSymbolName": "prog_item_eight_palette_indices",
                    "dataSymbolName":    "offworld_graphics_data_progression_item"},

                   {"fileName":          "off_world_item.bin",
                    "paletteSymbolName": "nonprog_item_eight_palette_indices",
                    "dataSymbolName":    "offworld_graphics_data_item"}]
    idx = 0
    offworldSprites: List[ByteEdit] = []
    for itemSprite in itemSprites:
        buffer = bytearray(pkgutil.get_data(__name__, "/".join(("data", "custom_sprite", itemSprite["fileName"]))))
        offworldSprites.append({"sym": symbols[itemSprite["paletteSymbolName"]],
                                "offset": 0,
                                "values": buffer[0:8]})
        offworldSprites.append({"sym": symbols[itemSprite["dataSymbolName"]],
                                "offset": 0,
                                "values": buffer[8:264]})
        idx += 1

    deathLink: List[ByteEdit] = [{
        "sym": symbols["config_deathlink"],
        "offset": 0,
        "values": [world.options.death_link.value]
    }]
    remoteItem: List[ByteEdit] = [{
        "sym": symbols["config_remote_items"],
        "offset": 0,
        "values": getWordArray(0b001 + (0b010 if world.options.remote_items else 0b000))
    }]
    ownPlayerId: List[ByteEdit] = [{
        "sym": symbols["config_player_id"],
        "offset": 0,
        "values": getWordArray(world.player)
    }]

    location_nothing: List[ByteEdit] = [{
        "sym": symbols["locations_nothing"],
        "offset": 0,
        "values": locations_nothing
    }]

    patchDict = {   'MultiWorldLocations': multiWorldLocations,
                    'MultiWorldItems': multiWorldItems,
                    'offworldSprites': offworldSprites,
                    'deathLink': deathLink,
                    'remoteItem': remoteItem,
                    'ownPlayerId': ownPlayerId,
                    'playerNameData':  playerNameData,
                    'playerIdData':  playerIdData,
                    'location_nothing': location_nothing}

    # convert an array of symbolic byte_edit dicts like {"sym": symobj, "offset": 0, "values": [1, 0]}
    # to a single rom patch dict like {0x438c: [1, 0], 0xa4a5: [0, 0, 0]}
    def resolve_symbols_to_file_offset_based_dict(byte_edits_arr: List[ByteEdit]) -> Dict[int, Iterable[int]]:
        this_patch_as_dict: Dict[int, Iterable[int]] = {}
        for byte_edit in byte_edits_arr:
            offset_within_rom_file: int = byte_edit["sym"]["offset_within_rom_file"] + byte_edit["offset"]
            this_patch_as_dict[offset_within_rom_file] = byte_edit["values"]
        return this_patch_as_dict

    for patchname, byte_edits_arr in patchDict.items():
        patches[patchname] = IPS_Patch(resolve_symbols_to_file_offset_based_dict(byte_edits_arr))

    # set rom name
    # 21 bytes
    from Main import __version__
    world.romName = bytearray(f'SMMR{__version__.replace(".", "")[0:3]}{required_pysmmaprando_version.replace(".", "").split("+")[0]}{world.player}{world.multiworld.seed:8}', 'utf8')[:21]
    world.romName.extend([0] * (21 - len(world.romName)))
    world.rom_name = world.romName
    # clients should read from 0x7FC0, the location of the rom title in the SNES header.
    patches["romName"] = IPS_Patch({0x007FC0 : world.romName})

    # array for each item: (must match Map Rando's new_game_extra.asm !initial_X addresses)
    #  offset within ROM of this item"s info (starting status)
    #  item bitmask or amount per pickup (BVOB = base value or bitmask),
    #  offset within ROM of this item"s info (starting maximum/starting collected items)
    #
    #                                 current  BVOB   max
    #                                 -------  ----   ---
    startItemROMDict = {"ETank":        [ snes_to_pc(0xB5FE52), 0x64, snes_to_pc(0xB5FE54)],
                        "Missile":      [ snes_to_pc(0xB5FE5C),  0x5, snes_to_pc(0xB5FE5E)],
                        "Super":        [ snes_to_pc(0xB5FE60),  0x5, snes_to_pc(0xB5FE62)],
                        "PowerBomb":    [ snes_to_pc(0xB5FE64),  0x5, snes_to_pc(0xB5FE66)],
                        "ReserveTank":  [ snes_to_pc(0xB5FE56), 0x64, snes_to_pc(0xB5FE58)],
                        "Morph":        [ snes_to_pc(0xB5FE04),  0x4, snes_to_pc(0xB5FE06)],
                        "Bombs":        [ snes_to_pc(0xB5FE05), 0x10, snes_to_pc(0xB5FE07)],
                        "SpringBall":   [ snes_to_pc(0xB5FE04),  0x2, snes_to_pc(0xB5FE06)],
                        "HiJump":       [ snes_to_pc(0xB5FE05),  0x1, snes_to_pc(0xB5FE07)],
                        "Varia":        [ snes_to_pc(0xB5FE04),  0x1, snes_to_pc(0xB5FE06)],
                        "Gravity":      [ snes_to_pc(0xB5FE04), 0x20, snes_to_pc(0xB5FE06)],
                        "SpeedBooster": [ snes_to_pc(0xB5FE05), 0x20, snes_to_pc(0xB5FE07)],
                        "SpaceJump":    [ snes_to_pc(0xB5FE05),  0x2, snes_to_pc(0xB5FE07)],
                        "ScrewAttack":  [ snes_to_pc(0xB5FE04),  0x8, snes_to_pc(0xB5FE06)],
                        "Charge":       [ snes_to_pc(0xB5FE09), 0x10, snes_to_pc(0xB5FE0B)],
                        "Ice":          [ snes_to_pc(0xB5FE08),  0x2, snes_to_pc(0xB5FE0A)],
                        "Wave":         [ snes_to_pc(0xB5FE08),  0x1, snes_to_pc(0xB5FE0A)],
                        "Spazer":       [ snes_to_pc(0xB5FE08),  0x4, snes_to_pc(0xB5FE0A)],
                        "Plasma":       [ snes_to_pc(0xB5FE08),  0x8, snes_to_pc(0xB5FE0A)],
                        "Grapple":      [ snes_to_pc(0xB5FE05), 0x40, snes_to_pc(0xB5FE07)],
                        "XRayScope":    [ snes_to_pc(0xB5FE05), 0x80, snes_to_pc(0xB5FE07)]

    # BVOB = base value or bitmask
                        }
    mergedData = {}
    hasETank = False
    hasSpazer = False
    hasPlasma = False
    for startItem in world.startItems:
        item = startItem
        if item == "ETank": hasETank = True
        if item == "Spazer": hasSpazer = True
        if item == "Plasma": hasPlasma = True
        if (item in ["ETank", "Missile", "Super", "PowerBomb", "Reserve"]):
            (currentValue, amountPerItem, maxValue) = startItemROMDict[item]
            if currentValue in mergedData:
                mergedData[currentValue] += amountPerItem
                mergedData[maxValue] += amountPerItem
            else:
                mergedData[currentValue] = amountPerItem
                mergedData[maxValue] = amountPerItem
        else:
            (collected, bitmask, equipped) = startItemROMDict[item]
            if collected in mergedData:
                mergedData[collected] |= bitmask
                mergedData[equipped] |= bitmask
            else:
                mergedData[collected] = bitmask
                mergedData[equipped] = bitmask

    if hasETank:
        # we are overwriting the starting energy, so add up the E from 99 (normal starting energy) rather than from 0
        mergedData[snes_to_pc(0xB5FE52)] += 99
        mergedData[snes_to_pc(0xB5FE54)] += 99

    if hasSpazer and hasPlasma:
        # de-equip spazer.
        # otherwise, firing the unintended spazer+plasma combo would cause massive game glitches and crashes
        mergedData[snes_to_pc(0xB5FE0A)] &= ~0x4

    for key, value in mergedData.items():
        if (key > snes_to_pc(0xB5FE0B)):
            [w0, w1] = getWordArray(value)
            mergedData[key] = [w0, w1]
        else:
            mergedData[key] = [value]

    patches["startInventory"] = IPS_Patch(mergedData)

    return patches

def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if SMJUHASH != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for Japan+US release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["sm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name

def get_sm_symbols(sym_json_path) -> dict:
    symbols = json.loads(pkgutil.get_data(__name__, sym_json_path).decode("utf-8"))
    symboltable = {}
    for name, sixdigitaddr in symbols.items():
        (bank, addr_within_bank) = sixdigitaddr.split(":")
        bank = int(bank, 16)
        addr_within_bank = int(addr_within_bank, 16)
        # categorize addresses using snes lorom mapping:
        # (reference: https://en.wikibooks.org/wiki/Super_NES_Programming/SNES_memory_map)
        if (bank >= 0x70 and bank <= 0x7d):
            offset_within_rom_file = None
            # SRAM is not continuous, but callers may want it in continuous terms
            # SRAM @ data bank $70-$7D, addr_within_bank $0000-$7FFF
            #
            # symbol aka snes    offestwithincontinuousSRAM
            # ---------------    --------------------------
            # $70:0000-7FFF   ->  0x0000- 7FFF
            # $71:0000-7FFF   ->  0x8000- FFFF
            # $72:0000-7FFF   -> 0x10000-17FFF
            # etc...
            offset_within_continuous_sram = (bank - 0x70) * 0x8000 + addr_within_bank
            offset_within_wram = None
        elif bank == 0x7e or bank == 0x7f or (bank == 0x00 and addr_within_bank <= 0x1fff):
            offset_within_rom_file = None
            offset_within_continuous_sram = None
            offset_within_wram = addr_within_bank
            if bank == 0x7f:
                offset_within_wram += 0x10000
        elif bank >= 0x80:
            offset_within_rom_file = ((bank - 0x80) * 0x8000) + (addr_within_bank % 0x8000)
            offset_within_continuous_sram = None
            offset_within_wram = None
        else:
            offset_within_rom_file = None
            offset_within_continuous_sram = None
            offset_within_wram = None
        symboltable[name] = {"bank": bank,
                             "addr_within_bank": addr_within_bank,
                             "offset_within_rom_file": offset_within_rom_file,
                             "offset_within_continuous_sram": offset_within_continuous_sram,
                             "offset_within_wram": offset_within_wram
                            }
    return symboltable

def getWordArray(w: int) -> List[int]:
    """ little-endian convert a 16-bit number to an array of numbers <= 255 each """
    return [w & 0x00FF, (w & 0xFF00) >> 8]

def convertToROMItemName(itemName):
    charMap = { "A" : 0x2CC0,
                "B" : 0x2CC1,
                "C" : 0x2CC2,
                "D" : 0x2CC3,
                "E" : 0x2CC4,
                "F" : 0x2CC5,
                "G" : 0x2CC6,
                "H" : 0x2CC7,
                "I" : 0x2CC8,
                "J" : 0x2CC9,
                "K" : 0x2CCA,
                "L" : 0x2CCB,
                "M" : 0x2CCC,
                "N" : 0x2CCD,
                "O" : 0x2CCE,
                "P" : 0x2CCF,
                "Q" : 0x2CD0,
                "R" : 0x2CD1,
                "S" : 0x2CD2,
                "T" : 0x2CD3,
                "U" : 0x2CD4,
                "V" : 0x2CD5,
                "W" : 0x2CD6,
                "X" : 0x2CD7,
                "Y" : 0x2CD8,
                "Z" : 0x2CD9,
                " " : 0x2C0F,
                "!" : 0x2CDF,
                "?" : 0x2CDE,
                "'" : 0x2CDD,
                "," : 0x2CDA,
                "." : 0x2CDA,
                "-" : 0x2CDD,
                "_" : 0x000F,
                "1" : 0x2C01,
                "2" : 0x2C02,
                "3" : 0x2C03,
                "4" : 0x2C04,
                "5" : 0x2C05,
                "6" : 0x2C06,
                "7" : 0x2C07,
                "8" : 0x2C08,
                "9" : 0x2C09,
                "0" : 0x2C00,
                "%" : 0x2C0A}
    data = []

    itemName = itemName.upper()[:26]
    itemName = itemName.strip()
    itemName = itemName.center(26, " ")
    itemName = "___" + itemName + "___"

    for char in itemName:
        [w0, w1] = getWordArray(charMap.get(char, 0x2CDE))
        data.append(w0)
        data.append(w1)
    return data

def current_key_pascal(option):
    """Converts a snake_case string to PascalCase."""
    # Replace underscores with spaces
    temp_string = option.current_key.replace("_", " ")
    # Capitalize the first letter of each word
    titled_string = temp_string.title()
    # Remove spaces to form PascalCase
    pascal_case_string = titled_string.replace(" ", "")
    return pascal_case_string
