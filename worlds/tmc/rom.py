from dataclasses import dataclass
import struct
from typing import TYPE_CHECKING
from BaseClasses import Item, ItemClassification
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from .constants import DUNGEON_ABBR, EXTERNAL_ITEM_MAP, TMCEvent, TMCItem, TMCLocation, WIND_CRESTS
from .flags import flag_table_by_name
from .items import item_table
from .locations import location_table_by_name, LocationData
from .options import DHCAccess, Goal, ShuffleElements


if TYPE_CHECKING:
    from . import MinishCapWorld


class MinishCapProcedurePatch(APProcedurePatch, APTokenMixin):
    game = "The Minish Cap"
    hash = "2af78edbe244b5de44471368ae2b6f0b"
    patch_file_ending = ".aptmc"
    result_file_ending = ".gba"

    procedure = [("apply_bsdiff4", ["base_patch.bsdiff4"]), ("apply_tokens", ["token_data.bin"])]

    @classmethod
    def get_source_data(cls) -> bytes:
        with open(get_settings().tmc_options.rom_file, "rb") as infile:
            base_rom_bytes = bytes(infile.read())

        return base_rom_bytes


@dataclass
class Transition:
    start_x: int
    start_y: int
    end_x: int
    end_y: int
    area_id: int
    room_id: int
    warp_type: int = 0
    subtype: int = 0
    shape: int = 0
    height: int = 1
    transition_type: int = 0
    facing_direction: int = 0

    def serialize(self) -> bytes:
        return struct.pack("<BBHHHHBBBBBB", self.warp_type, self.subtype, self.start_x, self.start_y, self.end_x,
                           self.end_y, self.shape, self.area_id, self.room_id, self.height, self.transition_type,
                           self.facing_direction)


def write_tokens(world: "MinishCapWorld", patch: MinishCapProcedurePatch) -> None:
    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000600, world.multiworld.player_name[world.player].encode("UTF-8"))

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000620, world.multiworld.seed_name.encode("UTF-8"))

    # Sanctuary fix
    if world.options.goal.value == Goal.option_vaati:
        # Skip stained-glass scene
        patch.write_token(APTokenTypes.WRITE, 0x0532F6, bytes([0x10, 0x23]))
    else:
        # Jump to credits on the stained-glass scene
        func = [0x00, 0x22, 0x05, 0x48, 0x04, 0x23, 0x03, 0x70, 0x42, 0x70, 0x82, 0x70, 0x01, 0x23, 0x8B, 0x71, 0x00,
                0x24, 0x78, 0x20, 0x01, 0x4B, 0x00, 0x00, 0x02, 0x10, 0x00, 0x03, 0xFF, 0x32, 0x05, 0x08]
        patch.write_token(APTokenTypes.WRITE, 0x0532F4, bytes(func))
        # Patch the stained-glass scene so that it's repeatable
        no_op = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        patch.write_token(APTokenTypes.WRITE, 0x04EB12, bytes(no_op))
        if world.options.dhc_access.value == DHCAccess.option_open:
            visit_move_guards = flag_table_by_name[TMCEvent.DWS_VISIT_00]
            patch.write_token(APTokenTypes.WRITE, visit_move_guards.offset, bytes([visit_move_guards.data]))

    # Goal Settings
    setting_bits = [world.options.goal.value == Goal.option_vaati, world.options.dhc_access == DHCAccess.option_open]
    setting_value = 0
    for setting, i in enumerate(setting_bits, 0):
        if setting:
            setting_value |= 2 ** i
    patch.write_token(APTokenTypes.WRITE, 0xFE0000, bytes([setting_value]))

    # Pedestal Settings
    if 0 <= world.options.ped_elements.value <= 4:
        patch.write_token(APTokenTypes.WRITE, 0xFE0001, bytes([world.options.ped_elements.value]))
    if 0 <= world.options.ped_swords.value <= 5:
        patch.write_token(APTokenTypes.WRITE, 0xFE0002, bytes([world.options.ped_swords.value]))
    if 0 <= world.options.ped_dungeons.value <= 6:
        patch.write_token(APTokenTypes.WRITE, 0xFE0003, bytes([world.options.ped_dungeons.value]))
    # if 0 <= world.options.ped_figurines.value <= 136:
    #     patch.write_token(APTokenTypes.WRITE, 0xFE0004, bytes([world.options.ped_figurines.value]))

    # Element map update
    if world.options.shuffle_elements.value == ShuffleElements.option_dungeon_prize:
        # Pack 1 = world map x pos: u8, world map y pos: u8,
        # Skip 1 byte in between (the ui element icon)
        # Pack 2 = region map x pos: u16, region map y pos: u16
        prize_locs = {TMCLocation.DEEPWOOD_PRIZE: [[0xB2, 0x7A], [0x0D6C, 0x0AC0]],
                      TMCLocation.COF_PRIZE: [[0x3B, 0x1B], [0x01E8, 0x0178]],
                      TMCLocation.FORTRESS_PRIZE: [[0x4B, 0x77], [0x0378, 0x0A78]],
                      TMCLocation.DROPLETS_PRIZE: [[0xB5, 0x4B], [0x0DB8, 0x0638]],
                      TMCLocation.CRYPT_PRIZE: [[0x5A, 0x15], [0x04DC, 0x0148]],
                      TMCLocation.PALACE_PRIZE: [[0xB5, 0x1B], [0x0D88, 0x00E8]]}
        element_address = {TMCItem.EARTH_ELEMENT: 0x128699,
                           TMCItem.FIRE_ELEMENT: 0x1286A1,
                           TMCItem.WIND_ELEMENT: 0x1286A9,
                           TMCItem.WATER_ELEMENT: 0x1286B1}
        for loc, data in prize_locs.items():
            placed_item = world.get_location(loc).item.name
            if element_address.get(placed_item, 0) == 0:
                continue
            patch.write_token(APTokenTypes.WRITE, element_address[placed_item], struct.pack("<BB", *data[0]))
            patch.write_token(APTokenTypes.WRITE, element_address[placed_item] + 3, struct.pack("<HH", *data[1]))
    elif world.options.shuffle_elements.value != ShuffleElements.option_vanilla:
        patch.write_token(APTokenTypes.WRITE, 0x128673, bytes([0x0, 0xF, 0x0, 0xF, 0x0, 0xF, 0x0]))

    # DHC Skip
    if world.options.dhc_access.value == DHCAccess.option_closed and world.options.goal.value == Goal.option_vaati:
        patch.write_token(APTokenTypes.WRITE, 0x127649, bytes([0x1D]))  # Change locationIndex of sanctuary to match DHC
        ped_to_altar = Transition(warp_type=1, start_x=0xE8, start_y=0x28, end_x=0x78, end_y=0x168,
                                  area_id=0x89, room_id=0)
        patch.write_token(APTokenTypes.WRITE, 0x139E80, ped_to_altar.serialize())

    # Wind Crests
    crest_value = 0x0
    crest_settings = world.options.as_dict(*WIND_CRESTS.keys())
    enabled_crests = [WIND_CRESTS[crest] for (crest, enabled) in crest_settings.items() if enabled]
    enabled_crests.extend([0x08, 0x10])  # Hyrule Town & Lake Hylia wind crest
    for crest in enabled_crests:
        crest_value |= crest
    patch.write_token(APTokenTypes.WRITE, flag_table_by_name[TMCEvent.MINISH_CREST].offset, bytes([crest_value]))

    # Dungeon Warps
    dungeon_offset = {
        "DWS": TMCEvent.DWS_BLUE_WARP,
        "CoF": TMCEvent.COF_BLUE_WARP,
        "FoW": TMCEvent.FOW_BLUE_WARP,
        "ToD": TMCEvent.TOD_BLUE_WARP,
        "PoW": TMCEvent.POW_BLUE_WARP,
        "DHC": TMCEvent.DHC_BLUE_WARP,
    }
    extra_flags = {
        "DWS": {
            "Blue": {TMCEvent.DWS_1F_BLUE_WARP_SWITCH},
            "Red": {TMCEvent.DWS_B1_RED_WARP_SWITCH},
        },
        "CoF": {
            "Blue": {TMCEvent.COF_B1_BLUE_WARP_SWITCH},
            "Red": {TMCEvent.COF_B2_RED_WARP_SWITCH},
        },
        "FoW": {
            "Blue": {},  # Currently leave doors closed to force fight
            "Red": {TMCEvent.FOW_RED_WARP_SWITCH},
        },
        "ToD": {
            "Blue": {},  # Currently leave doors closed to force fight
            "Red": {TMCEvent.TOD_RED_WARP_SWITCH},
        },
        "PoW": {
            "Blue": {},  # Currently leave bridge closed to force fight
            "Red": {TMCEvent.POW_RED_WARP_SWITCH, TMCEvent.POW_2ND_HALF_4F_LEFT_TORCH,
                    TMCEvent.POW_2ND_HALF_4F_RIGHT_TORCH},
        },
        "DHC": {
            "Blue": {},  # Currently leave doors closed to force fight
            "Red": {}  # Currently leave doors closed to force fight
        }
    }
    # logging.debug(f"Flag table: {flag_table_by_name.items()}")
    # for flag,address in flag_table_by_name.items():
    #     if flag is not "None":
    #         logging.debug(f'Name: {flag}, Address: {hex(address.offset)}, Flag: {hex(address.data)}')

    # Get dungeon warp settings from the 6 dungeon abbreviations
    warp_setting_keys = [f"dungeon_warp_{key.lower()}" for key in dungeon_offset]
    warp_settings = world.options.as_dict(*warp_setting_keys)
    for dungeon_abbr, event in dungeon_offset.items():
        warp_bits = warp_settings[f"dungeon_warp_{dungeon_abbr.lower()}"]
        offset = flag_table_by_name.get(dungeon_offset[dungeon_abbr]).offset
        # logging.debug(f'Write Warps: {dungeon}, Address: {hex(offset)}, bits: {bytes([warp_bits])}')
        patch.write_token(APTokenTypes.WRITE, offset, bytes([warp_bits]))
        if warp_bits & 1:
            for flag in extra_flags[dungeon_abbr]["Blue"]:
                romdata = flag_table_by_name.get(flag)
                offset_extra, bit = romdata.offset, romdata.data
                patch.write_token(APTokenTypes.OR_8, offset_extra, bit)
        if warp_bits & 2:
            for flag in extra_flags[dungeon_abbr]["Red"]:
                romdata = flag_table_by_name.get(flag)
                offset_extra, bit = romdata.offset, romdata.data
                patch.write_token(APTokenTypes.OR_8, offset_extra, bit)

    # Cucco/Goron Rounds
    cucco_complete = int(world.options.cucco_rounds.value == 0)
    cucco_skipped = 10 - world.options.cucco_rounds.value if world.options.cucco_rounds.value > 0 else 9
    flags_2ca5 = 0b0000_0110  # Exited Link's House / Spoke to Minish to get to fountain
    patch.write_token(APTokenTypes.WRITE, 0xFF1265, bytes([cucco_complete << 7 | cucco_skipped << 3 | flags_2ca5]))
    patch.write_token(APTokenTypes.WRITE, 0xFF00F6, bytes([world.options.goron_sets.value]))

    if world.options.goron_jp_prices.value:
        patch.write_token(APTokenTypes.WRITE, 0x1112F0, struct.pack(
            "<HHHHHHHHHHHHHHH", *[x for _ in range(0, 5) for x in [300, 200, 50]]))

    # Patch Items into Locations
    for location_name, loc in location_table_by_name.items():
        if loc.rom_addr is None:
            continue
        if location_name in world.disabled_locations and (
                loc.vanilla_item is None or loc.vanilla_item in item_table and
                item_table[loc.vanilla_item].classification != ItemClassification.filler):
            if loc.rom_addr[0] is None:
                continue
            item_inject(world, patch, location_table_by_name[location_name], world.create_item(TMCItem.RUPEES_1))
            continue
        if location_name in world.disabled_locations:
            continue
        location = world.get_location(location_name)
        item = location.item
        # Temporary if statement until I fill in all the rom addresses for each location
        if loc.rom_addr is not None and loc.rom_addr[0] is not None:
            item_inject(world, patch, location_table_by_name[location.name], item)

    patch.write_file("token_data.bin", patch.get_token_binary())


def item_inject(world: "MinishCapWorld", patch: MinishCapProcedurePatch, location: LocationData, item: Item):
    # item_byte_first = 0x00
    item_byte_second = 0x00

    if item.player == world.player:
        # The item belongs to this player's world, it should use local item ids
        item_byte_first = item_table[item.name].byte_ids[0]
        item_byte_second = item_table[item.name].byte_ids[1]
    elif item.classification not in EXTERNAL_ITEM_MAP:
        # The item belongs to an external player's world but we don't recognize the classification
        # default to green clock sprite, also used for progression item
        item_byte_first = 0x18
    else:
        # The item belongs to an external player's world, use the given classification to choose the item sprite
        item_byte_first = EXTERNAL_ITEM_MAP[item.classification](world.random)

    if hasattr(location.rom_addr[0], "__iter__") and hasattr(location.rom_addr[1], "__iter__"):
        for loc1, loc2 in zip(location.rom_addr[0], location.rom_addr[1]):
            write_single_byte(patch, loc1, item_byte_first)
            write_single_byte(patch, loc2 or loc1 + 1, item_byte_second)
    else:
        loc2 = location.rom_addr[1] or location.rom_addr[0] + 1
        write_single_byte(patch, location.rom_addr[0], item_byte_first)
        write_single_byte(patch, loc2, item_byte_second)


def write_single_byte(patch: MinishCapProcedurePatch, address: int, byte: int):
    if address is None:
        return
    if byte is None:
        byte = 0x00
    patch.write_token(APTokenTypes.WRITE, address, bytes([byte]))
