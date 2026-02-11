import struct
from dataclasses import dataclass
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from settings import get_settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes

from .constants import EXTERNAL_ITEM_MAP, WIND_CRESTS, TMCEvent, TMCFlagGroup, TMCItem, TMCLocation
from .flags import GLOBAL_FLAGS, OVERWORLD_FLAGS, flag_group_by_name, flag_table_by_name
from .items import item_table
from .locations import LocationData, location_table_by_name
from .options import Biggoron, DHCAccess, FusionAccess, Goal, PedReward, ShuffleElements

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
    options = world.options

    # Bake player name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000600, world.multiworld.player_name[world.player].encode("UTF-8"))

    # Bake seed name into ROM
    patch.write_token(APTokenTypes.WRITE, 0x000620, world.multiworld.seed_name.encode("UTF-8"))

    if world.options.remote_items.value:
        # Write remote items flag, causes the remote item pickup to be skipped.
        # Otherwise it would cause the pickup animation will play twice, once for the remote item, then the actual item.
        patch.write_token(APTokenTypes.WRITE, 0x000710, bytes([0x01]))
        # Skip chest opening delay, required otherwise the player's input is awkwardly locked in front of chests with
        # remote items in them... all of them
        patch.write_token(APTokenTypes.WRITE, 0x0A74E2, bytes([0x00, 0x20, 0x00, 0x20]))

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
        # Remove DHC Boss Door in favor of DHC Blocker
        boss_door = flag_table_by_name[TMCEvent.DHC_BOSS_DOOR_OPEN]
        patch.write_token(APTokenTypes.OR_8, boss_door.offset, boss_door.data)

    # Goal Settings
    write_bits(patch, 0xFE0000, [world.options.goal.value == Goal.option_vaati, world.options.dhc_access == DHCAccess.option_open])

    # Pedestal Settings
    if 0 <= world.options.ped_elements.value <= 4:
        patch.write_token(APTokenTypes.WRITE, 0xFE0001, bytes([world.options.ped_elements.value]))
    if 0 <= world.options.ped_swords.value <= 5:
        patch.write_token(APTokenTypes.WRITE, 0xFE0002, bytes([world.options.ped_swords.value]))
    if 0 <= world.options.ped_dungeons.value <= 6:
        patch.write_token(APTokenTypes.WRITE, 0xFE0003, bytes([world.options.ped_dungeons.value]))
    if 0 <= world.options.ped_figurines.value <= 136:
        patch.write_token(APTokenTypes.WRITE, 0xFE0004, bytes([world.options.ped_figurines.value]))

    # Other Toggles
    write_bits(patch, 0xFE0005, [bool(options.boots_on_l.value), bool(options.ocarina_on_select.value)])

    # Disable ezlo for Ocarina on Select
    if options.ocarina_on_select.value:
        patch.write_token(APTokenTypes.WRITE, 0x05270A, bytes([0x80, 0x42]))

    # Big Octorok Manip
    if options.big_octo_manipulation.value:
        # Disable Ink
        patch.write_token(APTokenTypes.WRITE, 0x0CE850, bytes([0x4a, 0xe8, 0x0c, 0x08, 0x4a, 0xe8, 0x0c, 0x08, 0x4a,
                                                               0xe8, 0x0c, 0x08, 0x4a, 0xe8, 0x0c, 0x08]))
        # Disable Charge
        patch.write_token(APTokenTypes.WRITE, 0x036DD2, bytes([0xc0, 0x46]))

    # Boots As Minish
    if options.boots_as_minish.value:
        # Enable
        patch.write_token(APTokenTypes.WRITE, 0x11B694, bytes([1]))

    # Replica Boss Door
    if options.replica_tod_boss_door.value:
        patch.write_token(APTokenTypes.WRITE, 0x0E3950, bytes([0x06, 0x0F, 0x39, 0, 0, 0, 0, 0, 0x08, 0x01, 0x28, 0x00, 0xFF, 0xFF, 0x2C, 0x00]))

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

    # Figurines
    if options.ped_figurines.value > 0:
        patch.write_token(APTokenTypes.WRITE, flag_group_by_name[TMCFlagGroup.FIGURINE_COLLECTED_FLAGS], bytes([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]))

    if options.ped_reward.value == PedReward.option_none:
        patch.write_token(APTokenTypes.WRITE, 0xFF002C, bytes([0, 0]))

    # Biggoron
    if options.shuffle_biggoron.value == Biggoron.option_disabled:
        patch.write_token(APTokenTypes.WRITE, 0x9404, bytes([0x00, 0x04, 0x00, 0x04]))
    else:
        patch.write_token(APTokenTypes.WRITE, 0x9404, bytes([0x03, 0x08]))
        biggoron_item = world.get_location(TMCLocation.FALLS_BIGGORON).item
        biggoron_item_byte, _ = get_item_bytes(world, biggoron_item)
        patch.write_token(APTokenTypes.WRITE, 0x095b26, bytes([biggoron_item_byte, 0x21]))

    if options.shuffle_biggoron.value == Biggoron.option_mirror_shield:
        # Normal shield doesn't matter
        patch.write_token(APTokenTypes.WRITE, 0x943E, bytes([0x00, 0x04, 0x00, 0x04]))

    # Write Fusion flags
    fusions = flag_group_by_name[TMCFlagGroup.COMPLETED_FUSIONS]
    no_fusions_requests = []
    if (options.gold_fusion_access.value == FusionAccess.option_open):
        tornado = GLOBAL_FLAGS[TMCEvent.CLOUD_TOPS_TORNADO]
        patch.write_token(APTokenTypes.OR_8, tornado.offset, tornado.data)
        patch.write_token(APTokenTypes.OR_8, fusions, 0xFE)
        patch.write_token(APTokenTypes.OR_8, fusions + 1, 0x03)
        patch.write_token(APTokenTypes.WRITE, 0x07E4AE, bytes([0xBD, 0x00]))
    elif (options.gold_fusion_access.value == FusionAccess.option_closed):
        patch.write_token(APTokenTypes.OR_8, fusions, 0x3E)
        patch.write_token(APTokenTypes.WRITE, 0x07E4AE, bytes([0xBD, 0x00]))
    else:
        patch.write_token(APTokenTypes.WRITE, fusions, bytes([0x00]))

    red_fusion_requests = [0x2061, 0x2077, 0x2085, 0x208C, 0x2093, 0x215A, 0x21B6, 0x21BD, 0x2208, 0x2238, 0x2240, 0x2241, 0x2248, 0x2249, 0x2250, 0x2251, 0x2270, 0x2296, 0x2297, 0x229E, 0x22C8, 0x22E6, 0x22ED, 0x2310, 0x238B]
    if (options.red_fusion_access.value == FusionAccess.option_open):
        crenel_beanstalk = OVERWORLD_FLAGS[TMCEvent.CRENEL_BEANSTALK]
        ruins_beanstalk = OVERWORLD_FLAGS[TMCEvent.RUINS_BEANSTALK]
        patch.write_token(APTokenTypes.OR_8, crenel_beanstalk.offset, crenel_beanstalk.data)
        patch.write_token(APTokenTypes.OR_8, ruins_beanstalk.offset, ruins_beanstalk.data)
        patch.write_token(APTokenTypes.OR_8, fusions + 1, 0xFC)
        patch.write_token(APTokenTypes.WRITE, fusions + 2, bytes([0xFF, 0xFF]))
        patch.write_token(APTokenTypes.OR_8, fusions + 4, 0x03)
    if (options.red_fusion_access.value == FusionAccess.option_closed or options.red_fusion_access.value == FusionAccess.option_open):
        no_fusions_requests.extend(red_fusion_requests)

    blue_fusion_requests = [0x2127, 0x213E, 0x2199, 0x21FF, 0x2225, 0x2226, 0x2227, 0x2228, 0x2229, 0x222A, 0x2258, 0x2259, 0x22C1, 0x22D6, 0x22F4, 0x2348, 0x2349, 0x234A, 0x234B, 0x234C, 0x234D, 0x2354, 0x2355, 0x2356, 0x2357, 0x2358, 0x2359, 0x2360, 0x2361, 0x2362, 0x2363, 0x2364, 0x2365, 0x236C, 0x236D, 0x236E, 0x236F, 0x23F0, 0x23F1, 0x2378, 0x2379, 0x237A, 0x237B, 0x237C, 0x237D, 0x2384, 0x2399]
    if (options.green_fusion_access.value == FusionAccess.option_open):
        hylia_beanstalk = OVERWORLD_FLAGS[TMCEvent.LAKE_BEANSTALK]
        hills_beanstalk = OVERWORLD_FLAGS[TMCEvent.HILLS_BEANSTALK]
        woods_beanstalk = OVERWORLD_FLAGS[TMCEvent.WESTERN_BEANSTALK]
        gina_grave = OVERWORLD_FLAGS[TMCEvent.VALLEY_GRAVE_RIGHT]
        patch.write_token(APTokenTypes.OR_8, hylia_beanstalk.offset, hylia_beanstalk.data)
        patch.write_token(APTokenTypes.OR_8, hills_beanstalk.offset, hills_beanstalk.data)
        patch.write_token(APTokenTypes.OR_8, woods_beanstalk.offset, woods_beanstalk.data)
        patch.write_token(APTokenTypes.OR_8, gina_grave.offset, gina_grave.data)
        patch.write_token(APTokenTypes.OR_8, fusions + 4, 0xFC)
        patch.write_token(APTokenTypes.WRITE, fusions + 5, bytes([0xFF]))
        patch.write_token(APTokenTypes.OR_8, fusions + 6, 0x0F)
    if (options.blue_fusion_access.value == FusionAccess.option_closed or options.blue_fusion_access.value == FusionAccess.option_open):
        no_fusions_requests.extend(blue_fusion_requests)

    green_fusion_requests = [0x2062, 0x20AC, 0x20DD, 0x212E, 0x212F, 0x2130, 0x21C4, 0x21CB, 0x21D2, 0x21D3, 0x21DA, 0x21DB, 0x2200, 0x2207, 0x220F, 0x2216, 0x221D, 0x221E, 0x2231, 0x2260, 0x2261, 0x2285, 0x2286, 0x2287, 0x22A5, 0x22AC, 0x22B3, 0x22BA, 0x22CF, 0x22DD, 0x22DE, 0x22DF, 0x22FB, 0x2302, 0x2309, 0x233A, 0x23A0, 0x23A1, 0x23A8]
    if (options.green_fusion_access.value == FusionAccess.option_open):
        patch.write_token(APTokenTypes.OR_8, fusions + 6, 0xF0)
        patch.write_token(APTokenTypes.WRITE, fusions + 7, bytes([0xFF, 0xFF, 0xFF, 0xFF, 0xFF]))
        patch.write_token(APTokenTypes.OR_8, fusions + 0xC, 0x1F)
    if (options.green_fusion_access.value == FusionAccess.option_closed or options.green_fusion_access.value == FusionAccess.option_open):
        no_fusions_requests.extend(green_fusion_requests)

    for request in no_fusions_requests:
        patch.write_token(APTokenTypes.WRITE, request, bytes([0xF2]))

    # Cucco/Goron Rounds
    cucco_complete = int(world.options.cucco_rounds.value == 0)
    cucco_skipped = 10 - world.options.cucco_rounds.value if world.options.cucco_rounds.value > 0 else 9
    flags_2ca5 = 0b0000_0110  # Exited Link's House / Spoke to Minish to get to fountain
    patch.write_token(APTokenTypes.WRITE, 0xFF1265, bytes([cucco_complete << 7 | cucco_skipped << 3 | flags_2ca5]))
    patch.write_token(APTokenTypes.WRITE, 0xFF0116, bytes([world.options.goron_sets.value]))

    if world.options.goron_jp_prices.value:
        patch.write_token(APTokenTypes.WRITE, 0x1112F0, struct.pack(
            "<HHHHHHHHHHHHHHH", *[x for _ in range(0, 5) for x in [300, 200, 50]]))

    # Health
    starting_hp = world.options.starting_hearts * 8
    patch.write_token(APTokenTypes.WRITE, flag_group_by_name[TMCFlagGroup.LINKS_CURRENT_HEALTH], bytes([starting_hp]))
    patch.write_token(APTokenTypes.WRITE, flag_group_by_name[TMCFlagGroup.LINKS_MAX_HEALTH], bytes([starting_hp]))

    # Patch Items into Locations
    for location_name, loc in location_table_by_name.items():
        if loc.rom_addr is None:
            continue
        if location_name in world.disabled_locations and (
                loc.vanilla_item is None or loc.vanilla_item in item_table and
                item_table[loc.vanilla_item].classification != ItemClassification.filler):
            if loc.rom_addr[0] is None:
                continue
            if location_name == TMCLocation.PEDESTAL_REQUIREMENT_REWARD:
                continue
            if location_name == TMCLocation.TOWN_SHOP_EXTRA_600_ITEM and not world.options.extra_shop_item:
                patch.write_token(APTokenTypes.WRITE, 0xFF00D0, bytes([0] * 0x20))
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
    item_byte_first, item_byte_second = get_item_bytes(world, item)

    if hasattr(location.rom_addr[0], "__iter__") and hasattr(location.rom_addr[1], "__iter__"):
        for loc1, loc2 in zip(location.rom_addr[0], location.rom_addr[1]):
            write_single_byte(patch, loc1, item_byte_first)
            if item_byte_first == 0x67:
                write_single_byte(patch, loc2 or loc1 + 1, world.figurines_placed)
                world.figurines_placed = world.figurines_placed + 1
            else:
                write_single_byte(patch, loc2 or loc1 + 1, item_byte_second)
    else:
        loc2 = location.rom_addr[1] or location.rom_addr[0] + 1
        write_single_byte(patch, location.rom_addr[0], item_byte_first)
        if item_byte_first == 0x67:
            write_single_byte(patch, loc2, world.figurines_placed)
            world.figurines_placed = world.figurines_placed + 1
        else:
            write_single_byte(patch, loc2, item_byte_second)


def get_item_bytes(world: "MinishCapWorld", item: Item) -> (int, int):
    # item_byte_first = 0x00
    item_byte_second = 0x00
    if item.player == world.player and not world.options.remote_items.value:
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

    return (item_byte_first, item_byte_second)


def write_single_byte(patch: MinishCapProcedurePatch, address: int, byte: int):
    if address is None:
        return
    if byte is None:
        byte = 0x00
    patch.write_token(APTokenTypes.WRITE, address, bytes([byte]))

def write_bits(patch: MinishCapProcedurePatch, address: int, setting_bits: list[bool]):
    setting_value = 0
    for i, setting in enumerate(setting_bits, 0):
        if setting:
            setting_value |= 2 ** i
    patch.write_token(APTokenTypes.WRITE, address, bytes([setting_value]))
