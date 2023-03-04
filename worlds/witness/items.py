"""
Defines progression, junk and event items for The Witness
"""
import copy
from collections import defaultdict
from typing import Dict, NamedTuple, Optional, Set

from BaseClasses import Item, MultiWorld
from . import StaticWitnessLogic, WitnessPlayerLocations, WitnessPlayerLogic
from .Options import get_option_value, is_option_enabled, the_witness_options
from fractions import Fraction


class ItemData(NamedTuple):
    """
    ItemData for an item in The Witness
    """
    code: Optional[int]
    progression: bool
    event: bool = False
    trap: bool = False
    never_exclude: bool = False


class WitnessItem(Item):
    """
    Item from the game The Witness
    """
    game: str = "The Witness"


class StaticWitnessItems:
    """
    Class that handles Witness items independent of world settings
    """

    ALL_ITEM_TABLE: Dict[str, ItemData] = {}

    ITEM_NAME_GROUPS: Dict[str, Set[str]] = dict()

    # These should always add up to 1!!!
    BONUS_WEIGHTS = {
        "Speed Boost": Fraction(1, 1),
    }

    # These should always add up to 1!!!
    TRAP_WEIGHTS = {   
        "Slowness": Fraction(8, 10),
        "Power Surge": Fraction(2, 10),
    }

    ALL_JUNK_ITEMS = set(BONUS_WEIGHTS.keys()) | set(TRAP_WEIGHTS.keys())

    ITEM_ID_TO_DOOR_HEX_ALL = dict()

    def __init__(self):
        item_tab = dict()

        for item in StaticWitnessLogic.ALL_SYMBOL_ITEMS:
            if item[0] == "11 Lasers" or item == "7 Lasers":
                continue

            item_tab[item[0]] = ItemData(158000 + item[1], True, False)

            self.ITEM_NAME_GROUPS.setdefault("Symbols", set()).add(item[0])

        for progressive, item_list in StaticWitnessLogic.PROGRESSIVE_TO_ITEMS.items():
            if not item_list:
                continue

            if item_list[0] in self.ITEM_NAME_GROUPS.setdefault("Symbols", set()):
                self.ITEM_NAME_GROUPS.setdefault("Symbols", set()).add(progressive)

        for item in StaticWitnessLogic.ALL_DOOR_ITEMS:
            item_tab[item[0]] = ItemData(158000 + item[1], True, False)

            # 1500 - 1510 are the laser items, which are handled like doors but should be their own separate group.
            if item[1] in range(1500, 1511):
                self.ITEM_NAME_GROUPS.setdefault("Lasers", set()).add(item[0])
            else:
                self.ITEM_NAME_GROUPS.setdefault("Doors", set()).add(item[0])

        for item in StaticWitnessLogic.ALL_TRAPS:
            item_tab[item[0]] = ItemData(
                158000 + item[1], False, False, True
            )

        for item in StaticWitnessLogic.ALL_BOOSTS:
            item_tab[item[0]] = ItemData(158000 + item[1], False, False)

        for item in StaticWitnessLogic.ALL_USEFULS:
            item_tab[item[0]] = ItemData(158000 + item[1], False, False, False, item[2])

        item_tab = dict(sorted(
            item_tab.items(),
            key=lambda single_item: single_item[1].code
            if isinstance(single_item[1].code, int) else 0)
        )

        for key, item in item_tab.items():
            self.ALL_ITEM_TABLE[key] = item

        for door in StaticWitnessLogic.ALL_DOOR_ITEMS:
            self.ITEM_ID_TO_DOOR_HEX_ALL[door[1] + 158000] = {int(door_hex, 16) for door_hex in door[2]}


class WitnessPlayerItems:
    """
    Class that defines Items for a single world
    """

    @staticmethod
    def code(item_name: str):
        return StaticWitnessItems.ALL_ITEM_TABLE[item_name].code

    @staticmethod
    def is_progression(item_name: str, multiworld: MultiWorld, player: int):
        useless_doors = {
            "River Monastery Shortcut (Door)",
            "Jungle & River Shortcuts",
            "Monastery Shortcut (Door)",
            "Orchard Second Gate (Door)",
        }

        if item_name in useless_doors:
            return False

        ep_doors = {
            "Monastery Garden Entry (Door)",
            "Monastery Shortcuts",
        }

        if item_name in ep_doors:
            return get_option_value(multiworld, player, "shuffle_EPs") != 0

        return True

    def __init__(self, locat: WitnessPlayerLocations, multiworld: MultiWorld, player: int, logic: WitnessPlayerLogic):
        """Adds event items after logic changes due to options"""
        self.EVENT_ITEM_TABLE = dict()
        self.ITEM_TABLE = copy.copy(StaticWitnessItems.ALL_ITEM_TABLE)

        self.PROGRESSION_TABLE = dict()

        self.ITEM_ID_TO_DOOR_HEX = dict()
        self.DOORS = set()

        self.PROG_ITEM_AMOUNTS = defaultdict(lambda: 1)

        self.SYMBOLS_NOT_IN_THE_GAME = set()

        self.EXTRA_AMOUNTS = {
            "Functioning Brain": 1,
            "Puzzle Skip": get_option_value(multiworld, player, "puzzle_skip_amount")
        }

        for k, v in self.ITEM_TABLE.items():
            if v.progression and not self.is_progression(k, multiworld, player):
                self.ITEM_TABLE[k] = ItemData(v.code, False, False, never_exclude=True)

        for item in StaticWitnessLogic.ALL_SYMBOL_ITEMS.union(StaticWitnessLogic.ALL_DOOR_ITEMS):
            if item[0] not in logic.PROG_ITEMS_ACTUALLY_IN_THE_GAME:
                del self.ITEM_TABLE[item[0]]
                if item in StaticWitnessLogic.ALL_SYMBOL_ITEMS:
                    self.SYMBOLS_NOT_IN_THE_GAME.add(StaticWitnessItems.ALL_ITEM_TABLE[item[0]].code)
            else:
                if item[0] in StaticWitnessLogic.PROGRESSIVE_TO_ITEMS:
                    self.PROG_ITEM_AMOUNTS[item[0]] = len(logic.MULTI_LISTS[item[0]])

                self.PROGRESSION_TABLE[item[0]] = self.ITEM_TABLE[item[0]]

        self.MULTI_LISTS_BY_CODE = dict()

        for item in self.PROG_ITEM_AMOUNTS:
            multi_list = logic.MULTI_LISTS[item]
            self.MULTI_LISTS_BY_CODE[self.code(item)] = [self.code(single_item) for single_item in multi_list]

        for entity_hex, items in logic.DOOR_ITEMS_BY_ID.items():
            entity_hex_int = int(entity_hex, 16)

            self.DOORS.add(entity_hex_int)

            for item in items:
                item_id = StaticWitnessItems.ALL_ITEM_TABLE[item].code
                self.ITEM_ID_TO_DOOR_HEX.setdefault(item_id, set()).add(entity_hex_int)

        symbols = is_option_enabled(multiworld, player, "shuffle_symbols")

        if "shuffle_symbols" not in the_witness_options.keys():
            symbols = True

        doors = get_option_value(multiworld, player, "shuffle_doors")

        self.GOOD_ITEMS = []

        if symbols:
            self.GOOD_ITEMS = [
                "Dots", "Black/White Squares", "Stars",
                "Shapers", "Symmetry"
            ]

            if doors:
                self.GOOD_ITEMS = [
                    "Dots", "Black/White Squares", "Symmetry"
                ]

            if is_option_enabled(multiworld, player, "shuffle_discarded_panels"):
                if get_option_value(multiworld, player, "puzzle_randomization") == 1:
                    self.GOOD_ITEMS.append("Arrows")
                else:
                    self.GOOD_ITEMS.append("Triangles")

            self.GOOD_ITEMS = [
                StaticWitnessLogic.ITEMS_TO_PROGRESSIVE.get(item, item) for item in self.GOOD_ITEMS
            ]

        for event_location in locat.EVENT_LOCATION_TABLE:
            location = logic.EVENT_ITEM_PAIRS[event_location]
            self.EVENT_ITEM_TABLE[location] = ItemData(None, True, True)
            self.ITEM_TABLE[location] = ItemData(None, True, True)

        trap_percentage = get_option_value(multiworld, player, "trap_percentage")

        self.JUNK_WEIGHTS = dict()

        if trap_percentage != 0:
            # I'm sure there must be some super "pythonic" way of doing this :D

            for trap_name, trap_weight in StaticWitnessItems.TRAP_WEIGHTS.items():
                self.JUNK_WEIGHTS[trap_name] = (trap_weight * trap_percentage) / 100

        if trap_percentage != 100:
            for bonus_name, bonus_weight in StaticWitnessItems.BONUS_WEIGHTS.items():
                self.JUNK_WEIGHTS[bonus_name] = (bonus_weight * (100 - trap_percentage)) / 100

        self.JUNK_WEIGHTS = {
            key: value for (key, value)
            in self.JUNK_WEIGHTS.items()
            if key in self.ITEM_TABLE.keys()
        }

        # JUNK_WEIGHTS will add up to 1 if the boosts weights and the trap weights each add up to 1 respectively.

        for junk_item in StaticWitnessItems.ALL_JUNK_ITEMS:
            if junk_item not in self.JUNK_WEIGHTS.keys():
                del self.ITEM_TABLE[junk_item]
