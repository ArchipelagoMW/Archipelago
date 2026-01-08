"""Library functions for patching."""

from __future__ import annotations


from enum import IntEnum, auto
from typing import TYPE_CHECKING, Any, List, Union
from functools import lru_cache

import js
import math
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Enums.Items import Items
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Types import BarrierItems, Types
from randomizer.Enums.Settings import HardModeSelected, MiscChangesSelected, HelmDoorItem, IceTrapFrequency, ProgressiveHintItem
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames
from randomizer.Patching.Library.DataTypes import short_to_ushort

if TYPE_CHECKING:
    from randomizer.Lists.MapsAndExits import Maps


class MenuTextDim(IntEnum):
    """Definition of base size of image."""

    size_w32_h32 = auto()
    size_w32_h64 = auto()
    size_w64_h32 = auto()


class MenuTexture:
    """Class to store information regarding a texture compatible with the main menu background."""

    def __init__(self, name: str, dim: MenuTextDim, table: int = 25, weight: int = 100, is_color: bool = False):
        """Initialize with given parameters."""
        self.name = name
        self.dim = dim
        self.table = table
        self.weight = weight
        self.is_color = is_color


class CustomActors(IntEnum):
    """Custom Actors Enum."""

    NintendoCoin = 0x8000  # Starts at 0x8000
    RarewareCoin = auto()
    Null = auto()
    PotionDK = auto()
    PotionDiddy = auto()
    PotionLanky = auto()
    PotionTiny = auto()
    PotionChunky = auto()
    PotionAny = auto()
    KongDK = auto()
    KongDiddy = auto()
    KongLanky = auto()
    KongTiny = auto()
    KongChunky = auto()
    KongDisco = auto()
    KongKrusha = auto()
    Bean = auto()
    Pearl = auto()
    Fairy = auto()
    IceTrapBubble = auto()
    IceTrapReverse = auto()
    IceTrapSlow = auto()
    Medal = auto()
    JetpacItemOverlay = auto()
    CrankyItem = auto()
    FunkyItem = auto()
    CandyItem = auto()
    SnideItem = auto()
    ZingerFlamethrower = auto()
    Scarab = auto()
    HintItemDK = auto()
    KopDummy = auto()
    HintItemDiddy = auto()
    HintItemLanky = auto()
    HintItemTiny = auto()
    HintItemChunky = auto()
    ArchipelagoItem = auto()


compatible_background_textures = {
    0x47A: MenuTexture("Gold Tower Stack", MenuTextDim.size_w32_h64),
    0x9DD: MenuTexture("Book", MenuTextDim.size_w32_h64),
    0x5C8: MenuTexture("Bricks", MenuTextDim.size_w32_h64),
    0x76F: MenuTexture("Bricks", MenuTextDim.size_w32_h64),
    0xAAF: MenuTexture("Floodlights", MenuTextDim.size_w32_h64),
    0x33D: MenuTexture("Wooden Board", MenuTextDim.size_w32_h64),
    0x79C: MenuTexture("Grassy Brick", MenuTextDim.size_w32_h64),
    0x992: MenuTexture("Wooden Door", MenuTextDim.size_w32_h64),
    0x39B: MenuTexture("C Block", MenuTextDim.size_w32_h32, 25, 7),
    0x39C: MenuTexture("G Block", MenuTextDim.size_w32_h32, 25, 7),
    0x39D: MenuTexture("9 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x39F: MenuTexture("R Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A0: MenuTexture("S Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A1: MenuTexture("1 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A2: MenuTexture("F Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A3: MenuTexture("8 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A4: MenuTexture("7 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A5: MenuTexture("B Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A6: MenuTexture("4 Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A7: MenuTexture("N Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A8: MenuTexture("D Block", MenuTextDim.size_w32_h32, 25, 7),
    0x3A9: MenuTexture("Q Block", MenuTextDim.size_w32_h32, 25, 7),
    0x7B2: MenuTexture("Up Arrow", MenuTextDim.size_w32_h32, 25, 50),
    0x7B3: MenuTexture("Down Arrow", MenuTextDim.size_w32_h32, 25, 50),
    0xAC: MenuTexture("TNT", MenuTextDim.size_w32_h32),
    0x7CD: MenuTexture("Night Sign", MenuTextDim.size_w32_h32),
    0x3DE: MenuTexture("Color", MenuTextDim.size_w32_h32, 7, 50, True),
    0xF7: MenuTexture("Grass", MenuTextDim.size_w32_h32),
    0xA00: MenuTexture("Sand", MenuTextDim.size_w32_h32),
    0xA84: MenuTexture("Sand", MenuTextDim.size_w32_h32),
    0xB4D: MenuTexture("Leaf", MenuTextDim.size_w32_h32),
    0xB19: MenuTexture("Boxes", MenuTextDim.size_w32_h32),
    0xB24: MenuTexture("Pineapple Switch", MenuTextDim.size_w32_h32),
    0xB25: MenuTexture("Coconut Switch", MenuTextDim.size_w32_h32),
    0xB1E: MenuTexture("Peanut Switch", MenuTextDim.size_w32_h32),
    0xC80: MenuTexture("Feather Switch", MenuTextDim.size_w32_h32),
    0xC81: MenuTexture("Grape Switch", MenuTextDim.size_w32_h32),
    # 0xB27: MenuTexture("Boxes", MenuTextDim.size_w32_h32),
    0xCF1: MenuTexture("L Square", MenuTextDim.size_w32_h32),
    0xCF4: MenuTexture("R Square", MenuTextDim.size_w32_h32),
    0xE63: MenuTexture("Metallic Green", MenuTextDim.size_w32_h32),
    0x9F3: MenuTexture("Watery Blue", MenuTextDim.size_w32_h32),
    0x9F4: MenuTexture("Watery Yellow", MenuTextDim.size_w32_h32),
    0x83: MenuTexture("Beige Strips", MenuTextDim.size_w32_h32),
    0x788: MenuTexture("Beige Panels", MenuTextDim.size_w32_h32),
    0x789: MenuTexture("Blue Panels", MenuTextDim.size_w32_h32),
    0x792: MenuTexture("White Granite", MenuTextDim.size_w32_h32),
    0x1258: MenuTexture("Horizontal Metal Green", MenuTextDim.size_w32_h32),
    0x1260: MenuTexture("Red Light", MenuTextDim.size_w32_h32),
    0x1343: MenuTexture("Fluid Red", MenuTextDim.size_w32_h32),
    0x1344: MenuTexture("Fluid Green", MenuTextDim.size_w32_h32),
    0x1347: MenuTexture("Fluid Orange", MenuTextDim.size_w32_h32),
    0x1348: MenuTexture("Fluid Blue", MenuTextDim.size_w32_h32),
    0xCC: MenuTexture("Bathroom Wall", MenuTextDim.size_w32_h64),
    0xCD5: MenuTexture("Orange Barrel", MenuTextDim.size_w32_h64),
    0xCD6: MenuTexture("Green Barrel", MenuTextDim.size_w32_h64),
    0xCD7: MenuTexture("Purple Barrel", MenuTextDim.size_w32_h64),
    0xCD8: MenuTexture("Yellow Barrel", MenuTextDim.size_w32_h64),
    0xCD9: MenuTexture("Blue Barrel", MenuTextDim.size_w32_h64),
    0xCDA: MenuTexture("Red Barrel", MenuTextDim.size_w32_h64),
    0xE3A: MenuTexture("Light Fixing", MenuTextDim.size_w32_h64),
    0x8F5: MenuTexture("Metal Pillars", MenuTextDim.size_w32_h64),
    0x786: MenuTexture("Just Straight Dirt", MenuTextDim.size_w32_h64),
    0x1257: MenuTexture("Copper", MenuTextDim.size_w32_h64),
    # 0xC: MenuTexture("Shelf of Bananas", MenuTextDim.size_w64_h32),
    # 0xD: MenuTexture("Shelf of Books", MenuTextDim.size_w64_h32),
    # 0xE: MenuTexture("Shelf of Wine", MenuTextDim.size_w64_h32),
    0xA8F: MenuTexture("Grime Panels", MenuTextDim.size_w64_h32),
    0xA43: MenuTexture("Books", MenuTextDim.size_w64_h32),
    0xA53: MenuTexture("Dolphins", MenuTextDim.size_w64_h32),
    0xA70: MenuTexture("Way Out Sign", MenuTextDim.size_w64_h32),
    0xA72: MenuTexture("Banana Hoard Sign", MenuTextDim.size_w64_h32),
    0xA73: MenuTexture("Training Area Sign", MenuTextDim.size_w64_h32),
    0xA74: MenuTexture("Cranky's Lab Sign", MenuTextDim.size_w64_h32),
    # 0xA76: MenuTexture("DK's Sign", MenuTextDim.size_w64_h32),
    0xC14: MenuTexture("No Admittance Sign", MenuTextDim.size_w64_h32),
    0xC47: MenuTexture("Danger Sign", MenuTextDim.size_w64_h32),
    0xC64: MenuTexture("Accept Sign", MenuTextDim.size_w64_h32),
    0xCCF: MenuTexture("A Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD0: MenuTexture("B Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD1: MenuTexture("C Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD2: MenuTexture("D Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD3: MenuTexture("E Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xCD4: MenuTexture("F Sign", MenuTextDim.size_w64_h32, 25, 7),
    0xD3C: MenuTexture("Blessed", MenuTextDim.size_w64_h32),  # Beans
    0x8DA: MenuTexture("Museum Sign", MenuTextDim.size_w64_h32),
    0x8DB: MenuTexture("Ballroom Sign", MenuTextDim.size_w64_h32),
    0x8DE: MenuTexture("Library Sign", MenuTextDim.size_w64_h32),
    0x9DA: MenuTexture("Library Wall", MenuTextDim.size_w64_h32),
    0x79A: MenuTexture("Minecart Tracks", MenuTextDim.size_w64_h32),
    0x339: MenuTexture("Piano Keys", MenuTextDim.size_w64_h32),
    0x398: MenuTexture("4 and B Blocks", MenuTextDim.size_w64_h32, 25, 7),
    0x399: MenuTexture("C and Z Blocks", MenuTextDim.size_w64_h32, 25, 7),
    0x902: MenuTexture("Carpet", MenuTextDim.size_w64_h32),
}


class HelmDoorRandomInfo:
    """Store information regarding helm door random boundaries."""

    def __init__(self, min_bound: int, max_bound: int, selection_weight: float):
        """Initialize with given parameters."""
        self.min_bound = min_bound
        self.max_bound = max_bound
        self.selection_weight = selection_weight
        self.selected_amount = None

    def chooseAmount(self, rando) -> int:
        """Choose amount for the helm door."""
        raw_float = rando.triangular(self.min_bound, self.max_bound)
        self.selected_amount = round(raw_float)
        return self.selected_amount


class HelmDoorInfo:
    """Store information about helm door requirements."""

    def __init__(
        self,
        absolute_max: int,
        hard: HelmDoorRandomInfo = None,
        medium: HelmDoorRandomInfo = None,
        easy: HelmDoorRandomInfo = None,
    ):
        """Initialize with given parameters."""
        self.absolute_max = absolute_max
        self.hard = hard
        self.medium = medium
        self.easy = easy

    def getDifficultyInfo(self, difficulty: int) -> HelmDoorRandomInfo:
        """Get the random info pertaining to the difficulty."""
        if difficulty == 0:
            return self.easy
        if difficulty == 1:
            return self.medium
        if difficulty == 2:
            return self.hard
        return None


class PaletteFillType(IntEnum):
    """Palette Fill Type enum."""

    block = auto()
    patch = auto()
    sparkle = auto()
    checkered = auto()
    radial = auto()
    kong = auto()


class Overlay(IntEnum):
    """Overlay enum."""

    Boot = 0
    Static = 1
    Menu = 2
    Multiplayer = 3
    Minecart = 4
    Race = 5
    Critter = 6
    Boss = 7
    Bonus = 8
    Arcade = 9
    Jetpac = 10
    Custom = 11  # Fake overlay used for patching


def getNextFreeID(ROM_COPY: LocalROM, cont_map_id: Union[Maps, int], ignore: List[Union[Any, int]] = []) -> int:
    """Get next available Model 2 ID."""
    setup_table = getPointerLocation(TableNames.Setups, cont_map_id)
    ROM_COPY.seek(setup_table)
    model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    vacant_ids = list(range(0, 600))
    for item in range(model2_count):
        item_start = setup_table + 4 + (item * 0x30)
        ROM_COPY.seek(item_start + 0x2A)
        item_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        if item_id in vacant_ids:
            vacant_ids.remove(item_id)
    for id in range(0x220, 0x225):
        if id in vacant_ids:
            vacant_ids.remove(id)
    for id in ignore:
        if id in vacant_ids:
            vacant_ids.remove(id)
    if len(vacant_ids) > 0:
        return min(vacant_ids)
    return 0  # Shouldn't ever hit this. This is a case if there's no vacant IDs in range [0,599]


def addNewScript(ROM_COPY: LocalROM, cont_map_id: Union[Maps, int], item_ids: List[int], type: ScriptTypes) -> None:
    """Append a new script to the script database. Has to be just 1 execution and 1 endblock."""
    script_table = getPointerLocation(TableNames.InstanceScripts, cont_map_id)
    ROM_COPY.seek(script_table)
    script_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
    good_scripts = []
    # Construct good pre-existing scripts
    file_offset = 2
    for script_item in range(script_count):
        ROM_COPY.seek(script_table + file_offset)
        script_start = script_table + file_offset
        script_id = int.from_bytes(ROM_COPY.readBytes(2), "big")
        block_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        file_offset += 6
        for block_item in range(block_count):
            ROM_COPY.seek(script_table + file_offset)
            cond_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * cond_count)
            ROM_COPY.seek(script_table + file_offset)
            exec_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
            file_offset += 2 + (8 * exec_count)
        script_end = script_table + file_offset
        if script_id not in item_ids:
            script_data = []
            ROM_COPY.seek(script_start)
            for x in range(int((script_end - script_start) / 2)):
                script_data.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
            good_scripts.append(script_data)
    # Get new script data
    subscript_type = -100
    if type == ScriptTypes.Bananaport:
        subscript_type = -1
    elif type == ScriptTypes.Wrinkly:
        subscript_type = -2
    elif type == ScriptTypes.TnsPortal:
        subscript_type = -3
    elif type == ScriptTypes.TnsIndicator:
        subscript_type = -4
    elif type == ScriptTypes.CrownMain:
        subscript_type = -5
    elif type == ScriptTypes.CrownIsles2:
        subscript_type = -6
    elif type == ScriptTypes.MelonCrate:
        subscript_type = -13
    elif type == ScriptTypes.DeleteItem:
        subscript_type = -16
    for item_id in item_ids:
        script_arr = [
            item_id,
            1,  # Block Count
            0,  # Behav 9C, Not sure the purpose on this. 0 seems safe from prior knowledge
            0,  # Cond Count
            1,  # Exec Count
            7,  # Func Type (Run JALR)
            125,  # JALR Type (Points to our custom code)
            short_to_ushort(subscript_type),  # Subscript Type
            item_id,  # Item ID, for the purpose of our script to locate any required data
        ]
        good_scripts.append(script_arr)
    # Reconstruct File
    ROM_COPY.seek(script_table)
    ROM_COPY.writeMultipleBytes(len(good_scripts), 2)
    for script in good_scripts:
        for x in script:
            ROM_COPY.writeMultipleBytes(x, 2)


def getObjectAddress(ROM_COPY: LocalROM, map: int, id: int, object_type: str) -> int:
    """Get address of object in setup."""
    setup_start = getPointerLocation(TableNames.Setups, map)
    ROM_COPY.seek(setup_start)
    model_2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    if object_type == "modeltwo":
        for item in range(model_2_count):
            item_start = setup_start + 4 + (item * 0x30)
            ROM_COPY.seek(item_start + 0x2A)
            if int.from_bytes(ROM_COPY.readBytes(2), "big") == id:
                return item_start
    mystery_start = setup_start + 4 + (0x30 * model_2_count)
    ROM_COPY.seek(mystery_start)
    mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    actor_start = mystery_start + 4 + (0x24 * mystery_count)
    ROM_COPY.seek(actor_start)
    actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    if object_type == "actor":
        for item in range(actor_count):
            item_start = actor_start + 4 + (item * 0x38)
            ROM_COPY.seek(item_start + 0x34)
            if int.from_bytes(ROM_COPY.readBytes(2), "big") == id:
                return item_start
    return None


def getObjectAddressBrowser(ROM_COPY: ROM, map: int, id: int, object_type: str) -> int:
    """Get address of object in setup."""
    setup_start = getPointerLocation(TableNames.Setups, map)
    ROM_COPY.seek(setup_start)
    model_2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    if object_type == "modeltwo":
        for item in range(model_2_count):
            item_start = setup_start + 4 + (item * 0x30)
            ROM_COPY.seek(item_start + 0x2A)
            if int.from_bytes(ROM_COPY.readBytes(2), "big") == id:
                return item_start
    mystery_start = setup_start + 4 + (0x30 * model_2_count)
    ROM_COPY.seek(mystery_start)
    mystery_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    actor_start = mystery_start + 4 + (0x24 * mystery_count)
    ROM_COPY.seek(actor_start)
    actor_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
    if object_type == "actor":
        for item in range(actor_count):
            item_start = actor_start + 4 + (item * 0x38)
            ROM_COPY.seek(item_start + 0x34)
            if int.from_bytes(ROM_COPY.readBytes(2), "big") == id:
                return item_start
    return None


@lru_cache(maxsize=None)
def is_item_selected_cached(
    bool_setting: bool,
    multiselector_setting: tuple,  # Change the type here
    check: Union["HardModeSelected", "MiscChangesSelected"],
    result_if_empty: bool,
) -> bool:
    """Determine whether a multiselector setting is enabled."""
    if not bool_setting:
        return False
    if len(multiselector_setting) == 0:
        return result_if_empty
    return check in multiselector_setting


# Helper function to call the cached version
def IsItemSelected(
    bool_setting: bool,
    multiselector_setting: List[Union["MiscChangesSelected", Any]],
    check: Union["HardModeSelected", "MiscChangesSelected"],
    result_if_empty: bool = True,
) -> bool:
    """Determine whether a multiselector setting is enabled."""
    # Convert the list to a tuple before passing it to the cached function
    return is_item_selected_cached(bool_setting, tuple(multiselector_setting), check, result_if_empty)


class SpawnerChange:
    """Information regarding a spawner change."""

    def __init__(self, map: Maps, spawner_id: int):
        """Initialize with given variables."""
        self.map_target = map
        self.spawner_target = spawner_id
        self.new_enemy = None
        self.new_scale = None
        self.new_speed_0 = None
        self.new_speed_1 = None


def applyCharacterSpawnerChanges(ROM_COPY: ROM, changes: list[SpawnerChange], fence_speed_factor: float = None):
    """Apply a series of changes to character spawners."""
    formatted_changes = {}
    id_changes_in_map = {}
    for change in changes:
        if change.map_target not in formatted_changes:
            formatted_changes[change.map_target] = {}
            id_changes_in_map[change.map_target] = []
        formatted_changes[change.map_target][change.spawner_target] = change
        id_changes_in_map[change.map_target].append(change.spawner_target)
    for map_id in formatted_changes:
        file_start = getPointerLocation(TableNames.Spawners, map_id)
        ROM_COPY.seek(file_start)
        fence_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        offset = 2
        used_fence_ids = []
        if fence_count > 0:
            for x in range(fence_count):
                fence = []
                fence_start = file_start + offset
                ROM_COPY.seek(file_start + offset)
                point_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                offset += (point_count * 6) + 2
                ROM_COPY.seek(file_start + offset)
                point0_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
                if fence_speed_factor is not None:
                    for y in range(point0_count):
                        ROM_COPY.seek(file_start + offset + 2 + (y * 10) + 8)
                        old_value = int.from_bytes(ROM_COPY.readBytes(1), "big")
                        new_value = int(old_value * fence_speed_factor)
                        ROM_COPY.seek(file_start + offset + 2 + (y * 10) + 8)
                        ROM_COPY.write(new_value)
                offset += (point0_count * 10) + 6
                fence_finish = file_start + offset
                fence_size = fence_finish - fence_start
                ROM_COPY.seek(fence_finish - 4)
                used_fence_ids.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(fence_start)
                for y in range(int(fence_size / 2)):
                    fence.append(int.from_bytes(ROM_COPY.readBytes(2), "big"))
                ROM_COPY.seek(fence_finish)
        spawner_count_location = file_start + offset
        ROM_COPY.seek(spawner_count_location)
        spawner_count = int.from_bytes(ROM_COPY.readBytes(2), "big")
        offset += 2
        for x in range(spawner_count):
            # Parse spawners
            ROM_COPY.seek(file_start + offset + 0x13)
            enemy_index = int.from_bytes(ROM_COPY.readBytes(1), "big")
            init_offset = offset
            if enemy_index in id_changes_in_map[map_id]:
                change_data = formatted_changes[map_id][enemy_index]
                if change_data.new_enemy is not None:
                    ROM_COPY.seek(file_start + init_offset)
                    ROM_COPY.write(change_data.new_enemy)
                if change_data.new_scale is not None:
                    ROM_COPY.seek(file_start + init_offset + 0xF)
                    ROM_COPY.write(change_data.new_scale)
                if change_data.new_speed_0 is not None:
                    ROM_COPY.seek(file_start + init_offset + 0xC)
                    ROM_COPY.write(change_data.new_speed_0)
                if change_data.new_speed_1 is not None:
                    ROM_COPY.seek(file_start + init_offset + 0xD)
                    ROM_COPY.write(change_data.new_speed_1)
            ROM_COPY.seek(file_start + offset + 0x11)
            extra_count = int.from_bytes(ROM_COPY.readBytes(1), "big")
            offset += 0x16 + (extra_count * 2)


def camelCaseToWords(string: str):
    """Convert camel case string to separated words."""
    words = [[string[0]]]

    for c in string[1:]:
        if words[-1][-1].islower() and c.isupper():
            words.append(list(c))
        else:
            words[-1].append(c)

    return " ".join(["".join(word) for word in words])


def getItemNumberString(count: int, item_type: Types) -> str:
    """Get a string which displays the number of items and the item name."""
    names = {
        Types.Banana: "Golden Banana",
        Types.BlueprintBanana: "Golden Banana",
        Types.Shop: "Move",
        Types.Blueprint: "Blueprint",
        Types.Fairy: "Fairy",
        Types.Key: "Key",
        Types.Crown: "Crown",
        Types.Coin: "Company Coin",
        Types.TrainingBarrel: "Move",
        Types.Climbing: "Move",
        Types.Kong: "Kong",
        Types.Medal: "Medal",
        Types.Shockwave: "Move",
        Types.Bean: "Bean",
        Types.Pearl: "Pearl",
        Types.RainbowCoin: "Rainbow Coin",
        Types.FakeItem: "Ice Trap",
        Types.ToughBanana: "Golden Banana",
        Types.JunkItem: "Junk Item",
        Types.Hint: "Hint",
        Types.PreGivenMove: "Move",
        Types.Climbing: "Move",
        Types.NintendoCoin: "Nintendo Coin",
        Types.RarewareCoin: "Rareware Coin",
        Types.Cranky: "Cranky",
        Types.Funky: "Funky",
        Types.Candy: "Candy",
        Types.Snide: "Snide",
        Types.IslesMedal: "Medal",
        Types.ProgressiveHint: "Hint",
        Types.ArchipelagoItem: "Archipelago Item",
    }
    name = names.get(item_type, item_type.name)
    if count != 1:
        name = f"{name}s"
        if item_type == Types.Fairy:
            name = "Fairies"
    return f"{count} {name}"


def recalculatePointerJSON(ROM_COPY: ROM):
    """Recalculates the pointer tables."""
    TABLE_COUNT = 32
    POINTER_OFFSET = 0x101C50
    new_data = [None] * TABLE_COUNT
    for x in range(TABLE_COUNT):
        ROM_COPY.seek(POINTER_OFFSET + ((TABLE_COUNT + x) << 2))
        table_data = {"entries": []}
        count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        ROM_COPY.seek(POINTER_OFFSET + (x << 2))
        head = POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big")
        for y in range(count):
            ROM_COPY.seek(head + (y << 2))
            local_data = {
                "index": y,
                "pointing_to": POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big"),
            }
            next_file = POINTER_OFFSET + int.from_bytes(ROM_COPY.readBytes(4), "big")
            local_data["compressed_size"] = next_file - local_data["pointing_to"]
            table_data["entries"].append(local_data)
        new_data[x] = table_data
    js.pointer_addresses = new_data


def setItemReferenceName(spoiler, item: Items, index: int, new_name: str):
    """Set new name for a location of an item."""
    try:
        if item == Items.CameraAndShockwave:
            setItemReferenceName(spoiler, Items.Camera, index, new_name)
            setItemReferenceName(spoiler, Items.Shockwave, index, new_name)
        else:
            for loc in spoiler.location_references:
                if loc.item == item:
                    loc.setLocation(index, new_name)
    except Exception:
        pass


def DoorItemToBarrierItem(item: HelmDoorItem, is_coin_door: bool = False, is_crown_door: bool = False) -> BarrierItems:
    """Convert helm door item enum to barrier item enum."""
    if item == HelmDoorItem.vanilla:
        if is_coin_door:
            return BarrierItems.CompanyCoin
        elif is_crown_door:
            return BarrierItems.Crown
    converter = {
        HelmDoorItem.opened: BarrierItems.Nothing,
        HelmDoorItem.req_bean: BarrierItems.Bean,
        HelmDoorItem.req_bp: BarrierItems.Blueprint,
        HelmDoorItem.req_companycoins: BarrierItems.CompanyCoin,
        HelmDoorItem.req_crown: BarrierItems.Crown,
        HelmDoorItem.req_fairy: BarrierItems.Fairy,
        HelmDoorItem.req_gb: BarrierItems.GoldenBanana,
        HelmDoorItem.req_key: BarrierItems.Key,
        HelmDoorItem.req_medal: BarrierItems.Medal,
        HelmDoorItem.req_pearl: BarrierItems.Pearl,
        HelmDoorItem.req_rainbowcoin: BarrierItems.RainbowCoin,
    }
    return converter.get(item, BarrierItems.Nothing)


def getIceTrapCount(settings) -> int:
    """Get the amount of Ice Traps the game will attempt to place."""
    if settings.archipelago:
        return settings.ice_trap_count

    ice_trap_freqs = {
        IceTrapFrequency.rare: 4,
        IceTrapFrequency.mild: 10,
        IceTrapFrequency.common: 32,
        IceTrapFrequency.frequent: 64,
        IceTrapFrequency.pain: 100,
    }
    return ice_trap_freqs.get(settings.ice_trap_frequency, 16)


EXPONENT = 1.7
OFFSET_DIVISOR = 15


def getHintRequirement(slot: int, cap: int):
    """Get the hint requirement for a slot index."""
    if slot == 34:
        return cap
    offset = cap / OFFSET_DIVISOR
    hint_slot = slot & 0xFC
    multiplier = cap - offset
    final_offset = (cap + offset) / 2
    exp_result = 1 + (math.pow(hint_slot, EXPONENT) / math.pow(34, EXPONENT))
    z = math.pi * exp_result
    required_gb_count = int(multiplier * 0.5 * math.cos(z) + final_offset)
    if required_gb_count == 0:
        return 1
    return required_gb_count


def getHintRequirementBatch(batch: int, cap: int):
    """Get the hint requirement for a batch index."""
    slot = 34
    if batch < 9:
        slot = batch * 4
    return getHintRequirement(slot, cap)


def getProgHintBarrierItem(item: ProgressiveHintItem) -> BarrierItems:
    """Get the accompanying barrier item for the prog hint item."""
    barrier_bijection = {
        ProgressiveHintItem.req_gb: BarrierItems.GoldenBanana,
        ProgressiveHintItem.req_bp: BarrierItems.Blueprint,
        ProgressiveHintItem.req_key: BarrierItems.Key,
        ProgressiveHintItem.req_medal: BarrierItems.Medal,
        ProgressiveHintItem.req_crown: BarrierItems.Crown,
        ProgressiveHintItem.req_fairy: BarrierItems.Fairy,
        ProgressiveHintItem.req_rainbowcoin: BarrierItems.RainbowCoin,
        ProgressiveHintItem.req_bean: BarrierItems.Bean,
        ProgressiveHintItem.req_pearl: BarrierItems.Pearl,
        ProgressiveHintItem.req_cb: BarrierItems.ColoredBanana,
    }
    return barrier_bijection[item]


def getValueFromByteArray(ba: bytearray, offset: int, size: int) -> int:
    """Get value from byte array given an offset and size."""
    value = 0
    for x in range(size):
        local_value = ba[offset + x]
        value <<= 8
        value += local_value
    return value


class Holidays(IntEnum):
    """Holiday Enum."""

    no_holiday = 0
    Christmas = auto()
    Halloween = auto()
    Anniv25 = auto()


def getHolidaySetting(settings):
    """Get the holiday setting."""
    is_offseason = True
    if is_offseason:
        return settings.holiday_setting_offseason
    return settings.holiday_setting


def getHoliday(settings):
    """Get the holiday experienced."""
    if getHolidaySetting(settings):
        return Holidays.Christmas
    return Holidays.no_holiday


plando_colors = {
    "\x04": [
        "orange",
        "woth",
        "keys",
        "donkey",
        "aztec",
        "freekongs",
        "dogadon1",
    ],
    "\x05": [
        "red",
        "foolish",
        "diddy",
        "helm",
    ],
    "\x06": [
        "blue",
        "lanky",
        "galleon",
        "pufftoss",
    ],
    "\x07": [
        "purple",
        "tiny",
        "forest",
        "fungi",
        "dogadon2",
    ],
    "\x08": [
        "lightgreen",
        "chunky",
        "japes",
        "dillo1",
    ],
    "\x09": [
        "magenta",
        "castle",
        "kutout",
    ],
    "\x0a": [
        "cyan",
        "caves",
        "fridge",
        "dillo2",
    ],
    "\x0b": [
        "rust",
        "isles",
        "training",
    ],
    "\x0c": [
        "paleblue",
        "allkongs",
        "factory",
        "madjack",
    ],
    "\x0d": [
        "green",
        "jetpac",
    ],
}
