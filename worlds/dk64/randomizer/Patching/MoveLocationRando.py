"""Randomize Move Locations."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import MicrohintsEnabled, MoveRando
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.Generic import setItemReferenceName
from randomizer.Patching.Library.Assets import CompTextFiles, ItemPreview
from randomizer.Patching.Library.ItemRando import pregiven_item_order
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
                MoveMicrohints(helm_prog_items[0], ItemPreview.PortMicro, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
                MoveMicrohints(helm_prog_items[1], ItemPreview.GoneMicro, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
                MoveMicrohints(Items.Bongos, ItemPreview.BongosMicro, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Triangle, ItemPreview.TriangleMicro, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Saxophone, ItemPreview.SaxMicro, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Trombone, ItemPreview.TromboneMicro, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.Guitar, ItemPreview.GuitarMicro, [MicrohintsEnabled.all]),
                MoveMicrohints(Items.ProgressiveSlam, ItemPreview.SlamMicro, [MicrohintsEnabled.base, MicrohintsEnabled.all]),
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
                for file in [CompTextFiles.PreviewsFlavor, CompTextFiles.PreviewsNormal]:
                    if file in spoiler.text_changes:
                        spoiler.text_changes[file].append(data)
                    else:
                        spoiler.text_changes[file] = [data]


def writeMoveDataToROM(ROM_COPY: LocalROM, arr: list, enable_hints: bool, spoiler, kong_slot: int, kongs: list, level_override=None):
    """Write move data to ROM."""
    for xi, x in enumerate(arr):
        if x["move_type"] == "flag":
            ROM_COPY.writeMultipleBytes(2, 1)
            if x["flag"] == "climbing":
                ROM_COPY.writeMultipleBytes(11, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
            else:
                flag_dict = {
                    "dive": 0,
                    "orange": 1,
                    "barrel": 2,
                    "vine": 3,
                    "camera": 4,
                    "shockwave": 5,
                    "camera_shockwave": 4,
                }
                ROM_COPY.writeMultipleBytes(10, 1)
                ROM_COPY.writeMultipleBytes(flag_dict.get(x["flag"], 0), 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
            ROM_COPY.writeMultipleBytes(x["price"], 1)
        elif x["move_type"] is None:
            for _ in range(6):
                ROM_COPY.writeMultipleBytes(0, 1)
        else:
            price_var = 0
            if isinstance(x["price"], list):
                price_var = 0
            else:
                price_var = x["price"]
            ROM_COPY.writeMultipleBytes(2, 1)
            if x["move_type"] == "special":
                ROM_COPY.writeMultipleBytes(x["move_lvl"], 1)
                ROM_COPY.writeMultipleBytes(x["move_kong"], 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
            elif x["move_type"] == "slam":
                ROM_COPY.writeMultipleBytes(3, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
            elif x["move_type"] == "gun":
                if x["move_lvl"] == 0:
                    ROM_COPY.writeMultipleBytes(4, 1)
                    ROM_COPY.writeMultipleBytes(x["move_kong"], 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                else:
                    ROM_COPY.writeMultipleBytes(x["move_lvl"] + 4, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
            elif x["move_type"] == "ammo_belt":
                ROM_COPY.writeMultipleBytes(7, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
                ROM_COPY.writeMultipleBytes(0, 1)
            elif x["move_type"] == "instrument":
                if x["move_lvl"] == 0:
                    ROM_COPY.writeMultipleBytes(8, 1)
                    ROM_COPY.writeMultipleBytes(x["move_kong"], 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                else:
                    ROM_COPY.writeMultipleBytes(9, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
                    ROM_COPY.writeMultipleBytes(0, 1)
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
    progressives = (Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveSlam)
    name_str = "Extra Training"
    for item in spoiler.pregiven_items:
        # print(item)
        if item is not None and item != Items.NoItem:
            new_slot = None
            if item in progressives:
                new_slot = getNextSlot(spoiler, ROM_COPY, item)
            elif item in pregiven_item_order:
                new_slot = pregiven_item_order.index(item)
            elif item == Items.CameraAndShockwave:
                new_slot = None  # Setting is handled by the code below
                for index in [pregiven_item_order.index(Items.Camera), pregiven_item_order.index(Items.Shockwave)]:
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
            setItemReferenceName(spoiler, item, new_slot - 0x1C, name_str, 0)
        elif item == Items.ProgressiveInstrumentUpgrade:
            setItemReferenceName(spoiler, item, new_slot - 0x20, name_str, 0)
        elif item == Items.ProgressiveSlam:
            setItemReferenceName(spoiler, item, new_slot - 0xF, name_str, 0)
        else:
            setItemReferenceName(spoiler, item, 0, name_str, 0)
