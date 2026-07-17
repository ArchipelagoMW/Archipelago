from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar
from enum import IntEnum

from dataclasses import dataclass
from BaseClasses import Item, ItemClassification as IC

from . import constants
from .constants import Items

if TYPE_CHECKING:
    from .world import TombaWorld


class ItemBehavior(IntEnum):
    RANDOMIZED = 0  # Archipelago choose when this item is retrieved
    LOCKED = 1  # Archipelago put that item in a pre-determined location
    ORIGINAL = 2  # Archipelago does not handle this item at all


@dataclass
class ItemData:
    _id_counter: ClassVar[int] = 1  # ID 0 is reserved

    game_id: int
    classification: IC
    name: str
    # Affects how it is given to the player (inventory stack management)
    countable: bool
    # How many are required in the game
    amount: int

    def __init__(
        self,
        game_id: int,
        classification: IC,
        name: str,
        countable: bool = False,
        amount: int = 1,
        behavior: ItemBehavior = ItemBehavior.RANDOMIZED,
    ):
        self.id = ItemData._id_counter
        ItemData._id_counter += 1

        self.game_id = game_id
        self.classification = classification
        self.name = name
        self.countable = countable
        self.amount = amount
        self.behavior = behavior

    def __repr__(self) -> str:
        return self.name


class ItemHandler:
    item_table: list[ItemData] = [
        ItemData(0x00, IC.progression, Items.CHICK, True, 4),
        ItemData(0x01, IC.filler, Items.FROG, behavior=ItemBehavior.ORIGINAL),
        ItemData(0x02, IC.filler, Items.LOST_DWARF),
        ItemData(0x03, IC.filler, Items.BANANAS, True),
        ItemData(0x04, IC.progression, Items.FURIOUS_TORNADO, behavior=ItemBehavior.LOCKED),
        ItemData(0x05, IC.filler, Items.HUNDRED_YEAR_OLD_BELL),
        ItemData(0x06, IC.progression, Items.HUNDRED_YEAR_OLD_KEY),
        ItemData(0x07, IC.filler, Items.CHARITY_WINGS, True),
        ItemData(0x08, IC.filler, Items.BITTING_PLANT_FLOWER, True),
        ItemData(0x09, IC.filler, Items.HEALING_MUSHROOM, True),
        ItemData(0x0A, IC.progression, Items.BUCKET),
        ItemData(0x0B, IC.filler, Items.TELESCOPE),
        ItemData(0x0C, IC.filler, Items.TEAR_JAR),
        ItemData(0x0D, IC.filler, Items.FLOWER_TEARS),
        ItemData(0x0E, IC.filler, Items.BARON),
        ItemData(0x0F, IC.filler, Items.BAKED_YAM),
        ItemData(0x10, IC.progression, Items.LEAF_BUTTERFLY, True, 29),
        ItemData(0x11, IC.filler, Items.TORCH),
        ItemData(0x12, IC.progression, Items.BUCKET_OF_WATER),
        ItemData(0x13, IC.filler, Items.DIRTY_MIRROR),
        ItemData(0x14, IC.filler, Items.FUNKY_PARASOL),
        ItemData(0x15, IC.filler, Items.WOOD_BOOMERANG),
        ItemData(0x16, IC.filler, Items.STONE_BOOMERANG),
        ItemData(0x17, IC.filler, Items.IRON_BOOMERANG),
        ItemData(0x18, IC.filler, Items.DASHING_PANTS),
        # ItemData(0x19, IC.filler, Items.MAP),
        ItemData(0x1A, IC.filler, Items.BROKEN_VASE),
        ItemData(0x1B, IC.filler, Items.BLACKJACK),
        ItemData(0x1C, IC.filler, Items.FLASH_PANTS),
        ItemData(0x1D, IC.filler, Items.JUMPING_PANTS),
        ItemData(0x1E, IC.filler, Items.LUNCH_BOX, True),
        ItemData(0x1F, IC.filler, Items.LARGE_LUNCH_BOX, True),
        ItemData(0x20, IC.deprioritized, Items.NORMAL_PANTS),
        ItemData(0x21, IC.filler, Items.GRAPPLE),
        ItemData(0x22, IC.filler, Items.GRAPPLEJACK),
        ItemData(0x23, IC.filler, Items.BABY_PIG),
        ItemData(0x24, IC.progression, Items.THOUSAND_YEAR_OLD_KEY),
        ItemData(0x25, IC.filler, Items.RED_EVIL_PIG_BAG),
        ItemData(0x26, IC.filler, Items.ORANGE_EVIL_PIG_BAG),
        ItemData(0x27, IC.filler, Items.YELLOW_EVIL_PIG_BAG),
        ItemData(0x28, IC.filler, Items.GREEN_EVIL_PIG_BAG),
        ItemData(0x29, IC.filler, Items.BLUE_EVIL_PIG_BAG),
        ItemData(0x2A, IC.filler, Items.NAVY_EVIL_PIG_BAG),
        ItemData(0x2B, IC.filler, Items.PINK_EVIL_PIG_BAG),
        ItemData(0x2C, IC.progression, Items.TEN_THOUSAND_YEAR_OLD_KEY),
        ItemData(0x2D, IC.progression, Items.MILLION_YEAR_OLD_KEY),
        ItemData(0x2E, IC.filler, Items.LARGE_KEY_PANEL_1),
        ItemData(0x2F, IC.filler, Items.LARGE_KEY_PANEL_2),
        ItemData(0x30, IC.filler, Items.LARGE_KEY_PANEL_3),
        ItemData(0x31, IC.filler, Items.LARGE_KEY_PANEL_4),
        ItemData(0x32, IC.filler, Items.LARGE_KEY_PANEL_5),
        ItemData(0x33, IC.filler, Items.FUEL_BAR),
        # ItemData(0x34, IC.filler, Items.RAIN_ESSENCE),
        ItemData(0x35, IC.filler, Items.BIG_KEY),
        ItemData(0x36, IC.filler, Items.SMALL_KEY),
        ItemData(0x37, IC.filler, Items.CHEESE, True),
        ItemData(0x38, IC.filler, Items.MAGIC_MIRROR),
        # ItemData(0x39, IC.filler, Items.TORN_MAP_1),
        # ItemData(0x3A, IC.filler, Items.TORN_MAP_2),
        ItemData(0x3B, IC.filler, Items.RUBBER_GLOVES),
        ItemData(0x3C, IC.filler, Items.BOMB),
        # ItemData(0x3D, IC.filler, Items.IRON),
        # ItemData(0x3E, IC.filler, Items.IRON_WHEEL),
        ItemData(0x3F, IC.filler, Items.FLOWER_SEEDS),
        ItemData(0x40, IC.filler, Items.PIPE),
        ItemData(0x41, IC.filler, Items.WINE),
        ItemData(0x42, IC.filler, Items.BUNK_FLOWER, True),
        ItemData(0x43, IC.filler, Items.MATH_BEAD_1),
        ItemData(0x44, IC.filler, Items.MATH_BEAD_2),
        ItemData(0x45, IC.filler, Items.MATH_BEAD_3),
        ItemData(0x46, IC.filler, Items.MATH_BEAD_4),
        ItemData(0x47, IC.filler, Items.MATH_BEAD_5),
        ItemData(0x48, IC.filler, Items.MATH_BEAD_6),
        ItemData(0x49, IC.filler, Items.MATH_BEAD_7),
        ItemData(0x4A, IC.filler, Items.MATH_BEAD_8),
        ItemData(0x4B, IC.filler, Items.MATH_BEAD_9),
        ItemData(0x4C, IC.filler, Items.MATH_BEAD_10),
        # ItemData(0x4D, IC.filler, Items.ITEM),
        # ItemData(0x4E, IC.filler, Items.ITEM),
        # ItemData(0x4F, IC.filler, Items.ITEM),
        # ItemData(0x50, IC.filler, Items.ITEM),
        # ItemData(0x51, IC.filler, Items.ITEM),
        # ItemData(0x52, IC.filler, Items.ITEM),
        # ItemData(0x53, IC.filler, Items.ITEM),
        # ItemData(0x54, IC.filler, Items.ITEM),
        # ItemData(0x55, IC.filler, Items.ITEM),
        # ItemData(0x56, IC.filler, Items.ITEM),
        ItemData(0x57, IC.filler, Items.BRONZE_MEDAL),
        ItemData(0x58, IC.filler, Items.SILVER_MEDAL),
        ItemData(0x59, IC.filler, Items.GOLD_MEDAL),
        # ItemData(0x5A, IC.filler, Items.LETTER),
        # ItemData(0x5B, IC.filler, Items.WOOD),
        ItemData(0x5C, IC.filler, Items.RAFT),
        ItemData(0x5D, IC.filler, Items.GOLDEN_LEAF_BUTTERFLY),
        ItemData(0x5E, IC.filler, Items.GOLDEN_FRUIT),
        ItemData(0x5F, IC.filler, Items.GOLD_FLOWER),
        ItemData(0x60, IC.filler, Items.PSYCHIC_FISH),
        # ItemData(0x61, IC.filler, Items.SHOVEL),
        ItemData(0x62, IC.filler, Items.JEWEL_OF_FIRE),
        ItemData(0x63, IC.filler, Items.JEWEL_OF_WATER),
        ItemData(0x64, IC.filler, Items.JEWEL_OF_WIND),
        ItemData(0x65, IC.filler, Items.MIGHTY_FISH),
        ItemData(0x66, IC.filler, Items.SILVER_POWDER),
        ItemData(0x67, IC.filler, Items.MOLASSES),
        ItemData(0x68, IC.filler, Items.KOKKA_CLAW, True),
        ItemData(0x69, IC.filler, Items.BUTAMUSHI_THORN, True),
        ItemData(0x6A, IC.filler, Items.NEEDLEGATOR_TEETH, True),
        # ItemData(0x6B, IC.filler, Items.ITEM),
        # ItemData(0x6C, IC.filler, Items.ELECTRIC_EEL),
        # ItemData(0x6D, IC.filler, Items.BLACK_WATER),
        # ItemData(0x6E, IC.filler, Items.RED_CANDY, True),
        # ItemData(0x6F, IC.filler, Items.BLUE_CANDY, True),
        # ItemData(0x70, IC.filler, Items.GREEN_CANDY, True),
        # ItemData(0x71, IC.filler, Items.BLACK_CANDY, True),
        # ItemData(0x72, IC.filler, Items.SILVER_CANDY, True),
        ItemData(0x73, IC.filler, Items.GOLD_CANDY),
        # ItemData(0x74, IC.filler, Items.FORBIDDEN_MUSHROOM),
        ItemData(0x75, IC.filler, Items.BLUE_POWDER),
        # ItemData(0x76, IC.filler, Items.COCONUTS, True),
        ItemData(0x77, IC.filler, Items.FUNGA_LEATHER),
        # ItemData(0x78, IC.filler, Items.GRANDPAS_BRACELET),
        ItemData(0x79, IC.filler, Items.WEED_KILLER),
        # ItemData(0x7A, IC.filler, Items.FUNGA_TREE),
        # ItemData(0x7B, IC.filler, Items.FUNGA_SAP),
        ItemData(0x7C, IC.filler, Items.THOUSAND_YEAR_OLD_BELL),
        ItemData(0x7D, IC.filler, Items.FUNGA_DRUM),
        ItemData(0x7E, IC.filler, Items.MIGHTY_FISH_FOOD),
        # ItemData(0x7F, IC.filler, Items.UNUSUAL_KEY),
        # ItemData(0x80, IC.filler, Items.CHUCKLING_MUSHROOM),
        # ItemData(0x81, IC.filler, Items.WEEPING_MUSHROOM),
        ItemData(0x82, IC.filler, Items.MYSTERIOUS_MUSHROOM),
        # ItemData(0x83, IC.filler, Items.ITEM),
        ItemData(0x84, IC.filler, Items.SACRED_FISH),
        # ItemData(0x85, IC.filler, Items.CHICK),
        # ItemData(0x86, IC.filler, Items.CHICK),
        ItemData(0x87, IC.filler, Items.GOLDEN_BOWL),
        # ItemData(0x88, IC.filler, Items.FLOWER_TEARS),
        # ItemData(0x89, IC.filler, Items.ITEM),
        ItemData(0x8A, IC.filler, Items.RISE_AND_SHINE_POWDER),
        ItemData(0x8B, IC.filler, Items.BANANA_JUICE),
        # ItemData(0x8C, IC.filler, Items.ITEM),
        ItemData(0x8D, IC.filler, Items.CHARLES_PANTS),
        ItemData(0x8E, IC.filler, Items.THREE_CRYSTAL_BALLS),
        ItemData(0x8F, IC.filler, Items.WHAT_THE_THIEF_LOST),
        ItemData(0x90, IC.filler, Items.WHAT_THE_THIEF_FORGOT),
        ItemData(0x91, IC.filler, Items.BOSS_JEWEL),
        ItemData(0x92, IC.filler, Items.ORDINARY_MUSHROOM, behavior=ItemBehavior.ORIGINAL),
        # ItemData(0x93, IC.filler, Items.ITEM),
        ItemData(0x94, IC.filler, Items.SEASHELL_NECKLACE),
        ItemData(0x95, IC.filler, Items.THIEFS_WIRE),
        ItemData(0x96, IC.filler, Items.STRONG_WIRE),
        ItemData(0x97, IC.filler, Items.TEN_THOUSAND_YEAR_OLD_BELL),
        ItemData(0x98, IC.filler, Items.MILLION_YEAR_OLD_BELL),
        ItemData(0x99, IC.filler, Items.COLD_MEDECINE),
        ItemData(0x9A, IC.filler, Items.YANS_LUNCH_BOX),
        ItemData(0x9B, IC.filler, Items.KEY_TO_OL_POND),
        ItemData(0x9C, IC.filler, Items.HEALING_HERBS),
        ItemData(0x9D, IC.filler, Items.KNOWLEDGE_FRUIT),
        ItemData(0x9E, IC.filler, Items.SEAWEED),
        ItemData(0x9F, IC.filler, Items.MINERS_HAT),
        # Tomba! does not handle items above 0x9F
    ]

    by_name: dict[str, ItemData] = {}
    by_id: dict[int, ItemData] = {}
    by_game_id: dict[int, ItemData] = {}
    name_to_id = {}

    for item in item_table:
        by_name[item.name] = item
        by_id[item.id] = item
        by_game_id[item.game_id] = item
        name_to_id[item.name] = item.id

    @staticmethod
    def get_random_filler_item_name(world: TombaWorld) -> str:
        return Items.CHARITY_WINGS

    @staticmethod
    def create_item(world: TombaWorld, name: str) -> TombaItem:
        item = ItemHandler.by_name[name]

        return TombaItem(name, item.classification, item.id, world.player)

    @staticmethod
    def create_all_items(world: TombaWorld) -> None:
        itempool: list[Item] = []

        for item in ItemHandler.item_table:
            if item.behavior is ItemBehavior.RANDOMIZED:
                for _ in range(item.amount):
                    itempool.append(world.create_item(item.name))

        number_of_items = len(itempool)
        number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))
        needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

        itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

        world.multiworld.itempool += itempool


class TombaItem(Item):
    game = constants.GAME
