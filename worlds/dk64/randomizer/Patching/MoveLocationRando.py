"""Randomize Move Locations."""

from enum import IntEnum, auto

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import MicrohintsEnabled, MoveRando
from randomizer.Enums.Types import Types
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Lists.Item import ItemList
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Generic import setItemReferenceName
from randomizer.CompileHints import getHelmProgItems

# /* 0x0A8 */ unsigned char dk_crankymoves[7]; // First 4 bits indicates the moves type, 0 = Moves, 1 = Slam, 2 = Guns, 3 = Ammo Belt, 4 = Instrument, 0xF = No Upgrade. Last 4 bits indicate move level (eg. 1 = Baboon Blast, 2 = Strong Kong, 3 = Gorilla Grab). Each item in the array indicates the level it is given (eg. 1st slot is purchased in Japes, 2nd for Aztec etc.)
# /* 0x0AF */ unsigned char diddy_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0B6 */ unsigned char lanky_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0BD */ unsigned char tiny_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0C4 */ unsigned char chunky_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0CB */ unsigned char dk_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0D2 */ unsigned char diddy_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0D9 */ unsigned char lanky_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0E0 */ unsigned char tiny_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0E7 */ unsigned char chunky_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0EE */ unsigned char dk_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x0F5 */ unsigned char diddy_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x0FC */ unsigned char lanky_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x103 */ unsigned char tiny_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x10A */ unsigned char chunky_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi

moveRandoOffset = 0x0A7

dk_crankymoves = []
diddy_crankymoves = []
lanky_crankymoves = []
tiny_crankymoves = []
chunky_crankymoves = []
dk_funkymoves = []
diddy_funkymoves = []
lanky_funkymoves = []
tiny_funkymoves = []
chunky_funkymoves = []
dk_candymoves = []
diddy_candymoves = []
lanky_candymoves = []
tiny_candymoves = []
chunky_candymoves = []

level_names = [
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
    "DK Isles",
]

kong_names = {
    Kongs.donkey: "Donkey Kong",
    Kongs.diddy: "Diddy",
    Kongs.lanky: "Lanky",
    Kongs.tiny: "Tiny",
    Kongs.chunky: "Chunky",
    Kongs.any: "Any Kong",
}


class MoveMicrohintItemData:
    """Information about the microhint move."""

    def __init__(self, subtype: str, index: int, kong: Kongs):
        """Initialize with given parameters."""
        self.subtype = subtype
        self.index = index
        self.kong = kong


move_info_data = {
    Items.BaboonBlast: MoveMicrohintItemData("special", 0, Kongs.donkey),
    Items.StrongKong: MoveMicrohintItemData("special", 1, Kongs.donkey),
    Items.GorillaGrab: MoveMicrohintItemData("special", 2, Kongs.donkey),
    Items.ChimpyCharge: MoveMicrohintItemData("special", 0, Kongs.diddy),
    Items.RocketbarrelBoost: MoveMicrohintItemData("special", 1, Kongs.diddy),
    Items.SimianSpring: MoveMicrohintItemData("special", 2, Kongs.diddy),
    Items.Orangstand: MoveMicrohintItemData("special", 0, Kongs.lanky),
    Items.BaboonBalloon: MoveMicrohintItemData("special", 1, Kongs.lanky),
    Items.OrangstandSprint: MoveMicrohintItemData("special", 2, Kongs.lanky),
    Items.MiniMonkey: MoveMicrohintItemData("special", 0, Kongs.tiny),
    Items.PonyTailTwirl: MoveMicrohintItemData("special", 1, Kongs.tiny),
    Items.Monkeyport: MoveMicrohintItemData("special", 2, Kongs.tiny),
    Items.HunkyChunky: MoveMicrohintItemData("special", 0, Kongs.chunky),
    Items.PrimatePunch: MoveMicrohintItemData("special", 1, Kongs.chunky),
    Items.GorillaGone: MoveMicrohintItemData("special", 2, Kongs.chunky),
    Items.ProgressiveSlam: MoveMicrohintItemData("slam", 1, Kongs.any),
    Items.Bongos: MoveMicrohintItemData("instrument", 0, Kongs.donkey),
    Items.Guitar: MoveMicrohintItemData("instrument", 0, Kongs.diddy),
    Items.Trombone: MoveMicrohintItemData("instrument", 0, Kongs.lanky),
    Items.Saxophone: MoveMicrohintItemData("instrument", 0, Kongs.tiny),
    Items.Triangle: MoveMicrohintItemData("instrument", 0, Kongs.chunky),
    Items.Coconut: MoveMicrohintItemData("gun", 0, Kongs.donkey),
    Items.Peanut: MoveMicrohintItemData("gun", 0, Kongs.diddy),
    Items.Grape: MoveMicrohintItemData("gun", 0, Kongs.lanky),
    Items.Feather: MoveMicrohintItemData("gun", 0, Kongs.tiny),
    Items.Pineapple: MoveMicrohintItemData("gun", 0, Kongs.chunky),
}


class MoveMicrohints:
    """Information about microhints."""

    def __init__(self, item: Items, file: int, enabled_hint_settings: list):
        """Initialize with given parameters."""
        self.item = item
        self.move = None
        if item in list(move_info_data.keys()):
            self.move = move_info_data[item]
        self.file = file
        self.enabled_hint_settings = enabled_hint_settings


def pushItemMicrohints(spoiler, move_dict: dict, level: int, kong: int, slot: int):
    """Push hint for the micro-hints system."""
    if spoiler.settings.microhints_enabled != MicrohintsEnabled.off:
        if kong != Kongs.any or slot == 0:
            move = None  # Using no item for the purpose of a default
            helm_prog_items = getHelmProgItems(spoiler)
            hinted_items = [
                # Key = Item, Value = Textbox index in text file 19
                MoveMicrohints(helm_prog_items[0], 26, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
                MoveMicrohints(helm_prog_items[1], 25, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
                MoveMicrohints(Items.Bongos, 27, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Triangle, 28, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Saxophone, 29, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Trombone, 30, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Guitar, 31, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.ProgressiveSlam, 33, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
            ]
            for item_data in hinted_items:
                move_data = item_data.move
                if (move_dict["move_type"] == move_data.subtype and move_dict["move_lvl"] == move_data.index and move_dict["move_kong"] == move_data.kong) or (
                    move_dict["move_type"] == move_data.subtype and move_data.subtype == "slam"
                ):
                    if spoiler.settings.microhints_enabled in list(item_data.enabled_hint_settings):
                        move = item_data
            if move is not None:
                data = {
                    "textbox_index": move.file,
                    "mode": "replace_whole",
                    "target": spoiler.microhints[ItemList[move.item].name],
                }
                if 19 in spoiler.text_changes:
                    spoiler.text_changes[19].append(data)
                else:
                    spoiler.text_changes[19] = [data]


def writeMoveDataToROM(ROM_COPY: LocalROM, arr: list, enable_hints: bool, spoiler, kong_slot: int, kongs: list, level_override=None):
    """Write move data to ROM."""
    for xi, x in enumerate(arr):
        if x["move_type"] == "flag":
            flag_dict = {
                "dive": 0x182,
                "orange": 0x184,
                "barrel": 0x185,
                "vine": 0x183,
                "camera": 0x2FD,
                "shockwave": 0x179,
                "climbing": 0x297,
                "camera_shockwave": 0xFFFE,
            }
            flag_index = 0xFFFF
            if x["flag"] in flag_dict:
                flag_index = flag_dict[x["flag"]]
            ROM_COPY.writeMultipleBytes(MoveTypes.Flag, 2)
            ROM_COPY.writeMultipleBytes(flag_index, 2)
            ROM_COPY.writeMultipleBytes(0, 1)
            ROM_COPY.writeMultipleBytes(x["price"], 1)
        elif x["move_type"] is None:
            ROM_COPY.writeMultipleBytes(MoveTypes.Nothing, 2)
            ROM_COPY.writeMultipleBytes(0, 2)
            ROM_COPY.writeMultipleBytes(0, 1)
            ROM_COPY.writeMultipleBytes(0, 1)
        else:
            move_types = ["special", "slam", "gun", "ammo_belt", "instrument"]
            price_var = 0
            if isinstance(x["price"], list):
                price_var = 0
            else:
                price_var = x["price"]
            ROM_COPY.writeMultipleBytes(move_types.index(x["move_type"]), 2)
            ROM_COPY.writeMultipleBytes(x["move_lvl"], 2)
            ROM_COPY.writeMultipleBytes(x["move_kong"], 1)
            ROM_COPY.writeMultipleBytes(price_var, 1)
        if enable_hints:
            if level_override is not None:
                pushItemMicrohints(spoiler, x, level_override, kongs[xi], kong_slot)
            else:
                pushItemMicrohints(spoiler, x, xi, kongs[xi], kong_slot)


def dictEqual(dict1: dict, dict2: dict) -> bool:
    """Determine if two dictionaries are equal."""
    if len(dict1) != len(dict2):
        return False
    else:
        for i in dict1:
            if dict1.get(i) != dict2.get(i):
                return False
    return True


def randomize_moves(spoiler, ROM_COPY: LocalROM):
    """Randomize Move locations based on move_data from spoiler."""
    varspaceOffset = spoiler.settings.rom_data
    movespaceOffset = spoiler.settings.move_location_data
    hint_enabled = True
    if spoiler.settings.shuffle_items and Types.Shop in spoiler.settings.valid_locations:
        hint_enabled = False
    if spoiler.settings.move_rando != MoveRando.off and spoiler.move_data is not None:
        # Take a copy of move_data before modifying
        move_arrays = spoiler.move_data.copy()

        dk_crankymoves = move_arrays[0][0][0]
        diddy_crankymoves = move_arrays[0][0][1]
        lanky_crankymoves = move_arrays[0][0][2]
        tiny_crankymoves = move_arrays[0][0][3]
        chunky_crankymoves = move_arrays[0][0][4]
        dk_funkymoves = move_arrays[0][1][0]
        diddy_funkymoves = move_arrays[0][1][1]
        lanky_funkymoves = move_arrays[0][1][2]
        tiny_funkymoves = move_arrays[0][1][3]
        chunky_funkymoves = move_arrays[0][1][4]
        dk_candymoves = move_arrays[0][2][0]
        diddy_candymoves = move_arrays[0][2][1]
        lanky_candymoves = move_arrays[0][2][2]
        tiny_candymoves = move_arrays[0][2][3]
        chunky_candymoves = move_arrays[0][2][4]

        training_moves = move_arrays[1]
        bfi_move = move_arrays[2]

        kong_lists = []
        for shop in range(3):
            shop_lst = []
            for kong in range(5):
                kong_lst = []
                for level in range(8):
                    kong_lst.append([])
                shop_lst.append(kong_lst)
            kong_lists.append(shop_lst)
        for shop in range(3):
            for level in range(8):
                is_shared = True
                default = 0
                for kong in range(5):
                    if kong == 0:
                        default = move_arrays[0][shop][kong][level]
                    if not dictEqual(default, move_arrays[0][shop][kong][level]):
                        is_shared = False
                for kong in range(5):
                    applied_kong = kong
                    if is_shared:
                        applied_kong = Kongs.any
                    kong_lists[shop][kong][level] = applied_kong
        ROM_COPY.seek(movespaceOffset)
        writeMoveDataToROM(ROM_COPY, dk_crankymoves, hint_enabled, spoiler, 0, kong_lists[0][0])
        writeMoveDataToROM(ROM_COPY, diddy_crankymoves, hint_enabled, spoiler, 1, kong_lists[0][1])
        writeMoveDataToROM(ROM_COPY, lanky_crankymoves, hint_enabled, spoiler, 2, kong_lists[0][2])
        writeMoveDataToROM(ROM_COPY, tiny_crankymoves, hint_enabled, spoiler, 3, kong_lists[0][3])
        writeMoveDataToROM(ROM_COPY, chunky_crankymoves, hint_enabled, spoiler, 4, kong_lists[0][4])
        writeMoveDataToROM(ROM_COPY, dk_funkymoves, hint_enabled, spoiler, 0, kong_lists[1][0])
        writeMoveDataToROM(ROM_COPY, diddy_funkymoves, hint_enabled, spoiler, 1, kong_lists[1][1])
        writeMoveDataToROM(ROM_COPY, lanky_funkymoves, hint_enabled, spoiler, 2, kong_lists[1][2])
        writeMoveDataToROM(ROM_COPY, tiny_funkymoves, hint_enabled, spoiler, 3, kong_lists[1][3])
        writeMoveDataToROM(ROM_COPY, chunky_funkymoves, hint_enabled, spoiler, 4, kong_lists[1][4])
        writeMoveDataToROM(ROM_COPY, dk_candymoves, hint_enabled, spoiler, 0, kong_lists[2][0])
        writeMoveDataToROM(ROM_COPY, diddy_candymoves, hint_enabled, spoiler, 1, kong_lists[2][1])
        writeMoveDataToROM(ROM_COPY, lanky_candymoves, hint_enabled, spoiler, 2, kong_lists[2][2])
        writeMoveDataToROM(ROM_COPY, tiny_candymoves, hint_enabled, spoiler, 3, kong_lists[2][3])
        writeMoveDataToROM(ROM_COPY, chunky_candymoves, hint_enabled, spoiler, 4, kong_lists[2][4])
        writeMoveDataToROM(ROM_COPY, training_moves, hint_enabled, spoiler, 0, [Kongs.any, Kongs.any, Kongs.any, Kongs.any], 7)
        writeMoveDataToROM(ROM_COPY, bfi_move, hint_enabled, spoiler, 0, [Kongs.tiny], 7)


def getNextSlot(spoiler, ROM_COPY: LocalROM, item: Items) -> int:
    """Get slot for progressive item with pre-given moves."""
    slots = []
    if item == Items.ProgressiveAmmoBelt:
        slots = [0x1C, 0x1D]
    elif item == Items.ProgressiveInstrumentUpgrade:
        slots = [0x20, 0x21, 0x22]
    elif item == Items.ProgressiveSlam:
        slots = [0xF, 0x10, 0x11]
    if len(slots) == 0:
        return None
    for slot in slots:
        offset = int(slot >> 3)
        check = int(slot % 8)
        ROM_COPY.seek(spoiler.settings.rom_data + 0xD5 + offset)
        val = int.from_bytes(ROM_COPY.readBytes(1), "big")
        if (val & (0x80 >> check)) == 0:
            return slot
    return None


def place_pregiven_moves(spoiler, ROM_COPY: LocalROM):
    """Place pre-given moves."""
    item_order = [
        Items.BaboonBlast,
        Items.StrongKong,
        Items.GorillaGrab,
        Items.ChimpyCharge,
        Items.RocketbarrelBoost,
        Items.SimianSpring,
        Items.Orangstand,
        Items.BaboonBalloon,
        Items.OrangstandSprint,
        Items.MiniMonkey,
        Items.PonyTailTwirl,
        Items.Monkeyport,
        Items.HunkyChunky,
        Items.PrimatePunch,
        Items.GorillaGone,
        Items.ProgressiveSlam,
        Items.ProgressiveSlam,
        Items.ProgressiveSlam,
        Items.Coconut,
        Items.Peanut,
        Items.Grape,
        Items.Feather,
        Items.Pineapple,
        Items.Bongos,
        Items.Guitar,
        Items.Trombone,
        Items.Saxophone,
        Items.Triangle,
        Items.ProgressiveAmmoBelt,
        Items.ProgressiveAmmoBelt,
        Items.HomingAmmo,
        Items.SniperSight,
        Items.ProgressiveInstrumentUpgrade,
        Items.ProgressiveInstrumentUpgrade,
        Items.ProgressiveInstrumentUpgrade,
        Items.Swim,
        Items.Oranges,
        Items.Barrels,
        Items.Vines,
        Items.Camera,
        Items.Shockwave,
        Items.Climbing,
    ]
    progressives = (Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveSlam)
    name_str = "Extra Training"
    for item in spoiler.pregiven_items:
        # print(item)
        if item is not None and item != Items.NoItem:
            new_slot = None
            if item in progressives:
                new_slot = getNextSlot(spoiler, ROM_COPY, item)
            elif item in item_order:
                new_slot = item_order.index(item)
            elif item == Items.CameraAndShockwave:
                new_slot = None  # Setting is handled by the code below
                for index in [item_order.index(Items.Camera), item_order.index(Items.Shockwave)]:
                    offset = int(index >> 3)
                    check = int(index % 8)
                    ROM_COPY.seek(spoiler.settings.rom_data + 0xD5 + offset)
                    val = int.from_bytes(ROM_COPY.readBytes(1), "big")
                    val |= 0x80 >> check
                    ROM_COPY.seek(spoiler.settings.rom_data + 0xD5 + offset)
                    ROM_COPY.writeMultipleBytes(val, 1)
            if new_slot is not None:
                offset = int(new_slot >> 3)
                check = int(new_slot % 8)
                ROM_COPY.seek(spoiler.settings.rom_data + 0xD5 + offset)
                val = int.from_bytes(ROM_COPY.readBytes(1), "big")
                val |= 0x80 >> check
                ROM_COPY.seek(spoiler.settings.rom_data + 0xD5 + offset)
                ROM_COPY.writeMultipleBytes(val, 1)
        if item == Items.ProgressiveAmmoBelt:
            setItemReferenceName(spoiler, item, new_slot - 0x1C, name_str)
        elif item == Items.ProgressiveInstrumentUpgrade:
            setItemReferenceName(spoiler, item, new_slot - 0x20, name_str)
        elif item == Items.ProgressiveSlam:
            setItemReferenceName(spoiler, item, new_slot - 0xF, name_str)
        else:
            setItemReferenceName(spoiler, item, 0, name_str)


class MoveDataSection(IntEnum):
    """Move Data Section enum."""

    cranky = auto()
    candy = auto()
    funky = auto()
    training = auto()
    bfi = auto()
    first_move = auto()


class MoveDataRequest(IntEnum):
    """Move Data Request Enum."""

    price = auto()
    flag = auto()
    move_type = auto()
    move_level = auto()
    move_kong = auto()
    move_no_kong = auto()


def getMoveSlot(vendor: MoveDataSection, kong: Kongs, level: int) -> int:
    """Get move slot in the global move array."""
    global_index = None
    shop_offsets = {
        MoveDataSection.cranky: 0,
        MoveDataSection.candy: 80,
        MoveDataSection.funky: 40,
    }
    if vendor in (MoveDataSection.cranky, MoveDataSection.candy, MoveDataSection.funky):
        global_index = shop_offsets[vendor] + (int(kong) * 8) + level
    elif vendor == MoveDataSection.training:
        global_index = 120 + level
    elif vendor == MoveDataSection.bfi:
        global_index = 124
    elif vendor == MoveDataSection.first_move:
        global_index = 125
    if global_index is None:
        raise Exception(f"Invalid global index for {vendor}")
    return global_index


def readMoveData(ROM_COPY: LocalROM, move_data: int, vendor: MoveDataSection, kong: Kongs, level: int, data_request: MoveDataRequest) -> int:
    """Acquire data from move block."""
    slot_address = move_data + (6 * getMoveSlot(vendor, kong, level))
    if data_request == MoveDataRequest.price:
        ROM_COPY.seek(slot_address + 5)
        return int.from_bytes(ROM_COPY.readBytes(1), "big")
    elif data_request in (MoveDataRequest.flag, MoveDataRequest.move_level):
        ROM_COPY.seek(slot_address + 2)
        return int.from_bytes(ROM_COPY.readBytes(2), "big")
    elif data_request == MoveDataRequest.move_type:
        ROM_COPY.seek(slot_address)
        return int.from_bytes(ROM_COPY.readBytes(2), "big")
    elif data_request == MoveDataRequest.move_no_kong:
        ROM_COPY.seek(slot_address)
        return int.from_bytes(ROM_COPY.readBytes(4), "big")
    elif data_request == MoveDataRequest.move_kong:
        ROM_COPY.seek(slot_address + 4)
        return int.from_bytes(ROM_COPY.readBytes(1), "big")
    raise Exception(f"Invalid data request: {data_request}")


def getSharedStatus(type_value: int) -> int:
    """Get shared status of vendor."""
    if (type_value > 2) and (type_value < 5):
        return type_value - 1
    elif type_value != 1:
        return 0
    return 1


def filterMoveType(ROM_COPY: LocalROM, move_data: int, section: MoveDataSection, kong: Kongs, level: int) -> int:
    """Filter move type for the purpose of writing to ROM."""
    move_type = readMoveData(ROM_COPY, move_data, section, kong, level, MoveDataRequest.move_type)
    move_level = readMoveData(ROM_COPY, move_data, section, kong, level, MoveDataRequest.move_level)
    if move_type == MoveTypes.Nothing:
        return -1
    if move_type == MoveTypes.Instruments:  # Instrument
        index = move_level + 1
        if index > 1:
            return MoveTypes.Flag  # Flag
    elif move_type in (MoveTypes.Slam, MoveTypes.AmmoBelt):  # Slam, Belt
        return MoveTypes.Flag  # Flag
    return move_type


def filterMoveIndex(
    ROM_COPY: LocalROM,
    move_data: int,
    section: MoveDataSection,
    kong: Kongs,
    level: int,
    slam_flag: int,
    belt_flag: int,
    ins_flag: int,
) -> tuple:
    """Filter move index for the purpose of writing to ROM."""
    filtered_type = filterMoveType(ROM_COPY, move_data, section, kong, level)
    index = readMoveData(ROM_COPY, move_data, section, kong, level, MoveDataRequest.move_level) + 1
    original_item_type = readMoveData(ROM_COPY, move_data, section, kong, level, MoveDataRequest.move_type)
    if original_item_type == MoveTypes.Slam:  # Slam
        return slam_flag + 1, belt_flag, ins_flag, slam_flag
    if original_item_type == MoveTypes.AmmoBelt:  # Ammo Belt
        return slam_flag, belt_flag + 1, ins_flag, belt_flag
    if original_item_type == MoveTypes.Instruments:  # Instrument
        if index > 1:
            return slam_flag, belt_flag, ins_flag + 1, ins_flag
    if filtered_type in (5, 6) or filtered_type > 7:
        new_index = readMoveData(ROM_COPY, move_data, section, kong, level, MoveDataRequest.flag)
        return slam_flag, belt_flag, ins_flag, new_index
    return slam_flag, belt_flag, ins_flag, index


def parseMoveBlock(spoiler, ROM_COPY: LocalROM):
    """Parse move block and writes a section of ROM which will be copied to RAM."""
    slam_flag = 0x3BF  # FLAG_SHOPMOVE_SLAM_0
    belt_flag = 0x299  # FLAG_SHOPMOVE_BELT_0
    ins_flag = 0x29B  # FLAG_SHOPMOVE_INS_0
    move_data = spoiler.settings.move_location_data
    write_data = []
    for _ in range(126):
        write_data.append({"move_type": 0, "move_level": 0, "move_kong": 0, "price": 0, "flag": -1})
    for i in range(8):  # LEVEL_COUNT
        stored_slam = slam_flag
        stored_belt = belt_flag
        stored_ins = ins_flag
        dk_cranky_type = readMoveData(ROM_COPY, move_data, MoveDataSection.cranky, Kongs.donkey, i, MoveDataRequest.move_type)
        dk_funky_type = readMoveData(ROM_COPY, move_data, MoveDataSection.funky, Kongs.donkey, i, MoveDataRequest.move_type)
        dk_candy_type = readMoveData(ROM_COPY, move_data, MoveDataSection.candy, Kongs.donkey, i, MoveDataRequest.move_type)
        cranky_shared = getSharedStatus(dk_cranky_type)
        funky_shared = getSharedStatus(dk_funky_type)
        candy_shared = getSharedStatus(dk_candy_type)
        cranky_targ_data = readMoveData(ROM_COPY, move_data, MoveDataSection.cranky, Kongs.donkey, i, MoveDataRequest.move_no_kong)
        cranky_targ_flag = readMoveData(ROM_COPY, move_data, MoveDataSection.cranky, Kongs.donkey, i, MoveDataRequest.flag)
        funky_targ_data = readMoveData(ROM_COPY, move_data, MoveDataSection.funky, Kongs.donkey, i, MoveDataRequest.move_no_kong)
        funky_targ_flag = readMoveData(ROM_COPY, move_data, MoveDataSection.funky, Kongs.donkey, i, MoveDataRequest.flag)
        candy_targ_data = readMoveData(ROM_COPY, move_data, MoveDataSection.candy, Kongs.donkey, i, MoveDataRequest.move_no_kong)
        candy_targ_flag = readMoveData(ROM_COPY, move_data, MoveDataSection.candy, Kongs.donkey, i, MoveDataRequest.flag)
        for kong in (Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky):
            cranky_local_data = readMoveData(ROM_COPY, move_data, MoveDataSection.cranky, kong, i, MoveDataRequest.move_no_kong)
            cranky_local_flag = readMoveData(ROM_COPY, move_data, MoveDataSection.cranky, kong, i, MoveDataRequest.flag)
            funky_local_data = readMoveData(ROM_COPY, move_data, MoveDataSection.funky, kong, i, MoveDataRequest.move_no_kong)
            funky_local_flag = readMoveData(ROM_COPY, move_data, MoveDataSection.funky, kong, i, MoveDataRequest.flag)
            candy_local_data = readMoveData(ROM_COPY, move_data, MoveDataSection.candy, kong, i, MoveDataRequest.move_no_kong)
            candy_local_flag = readMoveData(ROM_COPY, move_data, MoveDataSection.candy, kong, i, MoveDataRequest.flag)
            if (cranky_local_data != cranky_targ_data) or (cranky_local_flag != cranky_targ_flag):
                cranky_shared = 0
            if (funky_local_data != funky_targ_data) or (funky_local_flag != funky_targ_flag):
                funky_shared = 0
            if (candy_local_data != candy_targ_data) or (candy_local_flag != candy_targ_flag):
                candy_shared = 0
        for j in range(5):
            if (cranky_shared == 1) or (funky_shared == 1) or (candy_shared == 1):
                slam_flag = stored_slam
            if (cranky_shared == 2) or (funky_shared == 2) or (candy_shared == 2):
                belt_flag = stored_belt
            if (cranky_shared == 3) or (funky_shared == 3) or (candy_shared == 3):
                ins_flag = stored_ins
            for vendor in (MoveDataSection.cranky, MoveDataSection.candy, MoveDataSection.funky):
                slot = getMoveSlot(vendor, j, i)
                write_data[slot]["move_type"] = filterMoveType(ROM_COPY, move_data, vendor, j, i)
                write_data[slot]["move_kong"] = readMoveData(ROM_COPY, move_data, vendor, j, i, MoveDataRequest.move_kong)
                slam_flag, belt_flag, ins_flag, write_data[slot]["move_level"] = filterMoveIndex(ROM_COPY, move_data, vendor, j, i, slam_flag, belt_flag, ins_flag)
                write_data[slot]["price"] = readMoveData(ROM_COPY, move_data, vendor, j, i, MoveDataRequest.price)
    for i in range(4):
        # Training Barrels
        slot = getMoveSlot(MoveDataSection.training, 0, i)
        write_data[slot]["move_type"] = filterMoveType(ROM_COPY, move_data, MoveDataSection.training, 0, i)
        write_data[slot]["move_kong"] = readMoveData(ROM_COPY, move_data, MoveDataSection.training, 0, i, MoveDataRequest.move_kong)
        slam_flag, belt_flag, ins_flag, write_data[slot]["move_level"] = filterMoveIndex(ROM_COPY, move_data, MoveDataSection.training, 0, i, slam_flag, belt_flag, ins_flag)
    for extra_item in (MoveDataSection.bfi, MoveDataSection.first_move):
        slot = getMoveSlot(extra_item, 0, 0)
        write_data[slot]["move_type"] = filterMoveType(ROM_COPY, move_data, extra_item, 0, 0)
        write_data[slot]["move_kong"] = readMoveData(ROM_COPY, move_data, extra_item, 0, 0, MoveDataRequest.move_kong)
        slam_flag, belt_flag, ins_flag, write_data[slot]["move_level"] = filterMoveIndex(ROM_COPY, move_data, extra_item, 0, 0, slam_flag, belt_flag, ins_flag)
    for index, item in enumerate(write_data):
        item_head = 0x1FEF800 + (6 * index)
        ROM_COPY.seek(item_head)
        ROM_COPY.writeMultipleBytes(item.get("move_type", 7), 2)
        ROM_COPY.writeMultipleBytes(item.get("move_level", 1), 2)
        ROM_COPY.writeMultipleBytes(item.get("move_kong", 0), 1)
        ROM_COPY.writeMultipleBytes(item.get("price", 0), 1)
