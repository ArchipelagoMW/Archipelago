"""
Defines progression, junk and event items for The Witness
"""
import copy
from typing import TYPE_CHECKING, Dict, List, Set

from BaseClasses import Item, ItemClassification, MultiWorld

from .data import static_items as static_witness_items
from .data.item_definition_classes import (
    DoorItemDefinition,
    ItemCategory,
    ItemData,
    ItemDefinition,
    ProgressiveItemDefinition,
    WeightedItemDefinition,
)
from .data.utils import build_weighted_int_list, cast_not_none
from .locations import WitnessPlayerLocations
from .player_logic import WitnessPlayerLogic

if TYPE_CHECKING:
    from . import WitnessWorld

NUM_ENERGY_UPGRADES = 4


class WitnessItem(Item):
    """
    Item from the game The Witness
    """
    game: str = "The Witness"


class WitnessPlayerItems:
    """
    Class that defines Items for a single world
    """

    def __init__(self, world: "WitnessWorld", player_logic: WitnessPlayerLogic,
                 player_locations: WitnessPlayerLocations) -> None:
        """Adds event items after logic changes due to options"""

        self._world: WitnessWorld = world
        self._multiworld: MultiWorld = world.multiworld
        self._player_id: int = world.player
        self._logic: WitnessPlayerLogic = player_logic
        self._locations: WitnessPlayerLocations = player_locations

        # Duplicate the static item data, then make any player-specific adjustments to classification.
        self.item_data: Dict[str, ItemData] = copy.deepcopy(static_witness_items.ITEM_DATA)

        # Remove all progression items that aren't actually in the game.
        self.item_data = {
            name: data for (name, data) in self.item_data.items()
            if data.classification not in
               {ItemClassification.progression, ItemClassification.progression_skip_balancing}
               or name in player_logic.PROGRESSION_ITEMS_ACTUALLY_IN_THE_GAME
        }

        # Downgrade door items
        for item_name, item_data in self.item_data.items():
            if not isinstance(item_data.definition, DoorItemDefinition):
                continue

            if all(not self._logic.solvability_guaranteed(e_hex) for e_hex in item_data.definition.panel_id_hexes):
                item_data.classification = ItemClassification.useful

        # Build the mandatory item list.
        self._mandatory_items: Dict[str, int] = {}

        # Add progression items to the mandatory item list.
        progression_dict = {
            name: data for (name, data) in self.item_data.items()
            if data.classification in {ItemClassification.progression, ItemClassification.progression_skip_balancing}
        }
        for item_name, item_data in progression_dict.items():
            if isinstance(item_data.definition, ProgressiveItemDefinition):
                num_progression = len(self._logic.PROGRESSIVE_LISTS[item_name])
                self._mandatory_items[item_name] = num_progression
            else:
                self._mandatory_items[item_name] = 1

        # Add setting-specific useful items to the mandatory item list.
        for item_name, item_data in {name: data for (name, data) in self.item_data.items()
                                     if data.classification == ItemClassification.useful}.items():
            if item_name in static_witness_items._special_usefuls:
                continue

            if item_name == "Energy Capacity":
                self._mandatory_items[item_name] = NUM_ENERGY_UPGRADES
            elif isinstance(item_data.classification, ProgressiveItemDefinition):
                self._mandatory_items[item_name] = len(item_data.mappings)
            else:
                self._mandatory_items[item_name] = 1

        # Add event items to the item definition list for later lookup.
        for event_location in self._locations.EVENT_LOCATION_TABLE:
            location_name = player_logic.EVENT_ITEM_PAIRS[event_location][0]
            self.item_data[location_name] = ItemData(None, ItemDefinition(0, ItemCategory.EVENT),
                                                     ItemClassification.progression, False)

    def get_mandatory_items(self) -> Dict[str, int]:
        """
        Returns the list of items that must be in the pool for the game to successfully generate.
        """
        return self._mandatory_items.copy()

    def get_filler_items(self, quantity: int) -> Dict[str, int]:
        """
        Generates a list of filler items of the given length.
        """
        if quantity <= 0:
            return {}

        output: Dict[str, int] = {}
        remaining_quantity = quantity

        # Add joke items.
        output.update({name: 1 for (name, data) in self.item_data.items()
                       if data.definition.category is ItemCategory.JOKE})
        remaining_quantity -= len(output)

        # Read trap configuration data.
        trap_weight = self._world.options.trap_percentage / 100
        trap_items = self._world.options.trap_weights.value

        if not sum(trap_items.values()):
            trap_weight = 0

        # Add filler items to the list.
        filler_weight = 1 - trap_weight

        filler_items: Dict[str, float]
        filler_items = {name: data.definition.weight if isinstance(data.definition, WeightedItemDefinition) else 1
                        for (name, data) in self.item_data.items() if data.definition.category is ItemCategory.FILLER}
        filler_items = {name: base_weight * filler_weight / sum(filler_items.values())
                        for name, base_weight in filler_items.items() if base_weight > 0}

        # Add trap items.
        if trap_weight > 0:
            filler_items.update({name: base_weight * trap_weight / sum(trap_items.values())
                                 for name, base_weight in trap_items.items() if base_weight > 0})

        # Get the actual number of each item by scaling the float weight values to match the target quantity.
        int_weights: List[int] = build_weighted_int_list(filler_items.values(), remaining_quantity)
        output.update(zip(filler_items.keys(), int_weights))

        return output

    def get_early_items(self) -> List[str]:
        """
        Returns items that are ideal for placing on extremely early checks, like the tutorial gate.
        """
        output: Set[str] = set()
        if self._world.options.shuffle_symbols:
            discards_on = self._world.options.shuffle_discarded_panels
            mode = self._world.options.puzzle_randomization.current_key

            output = static_witness_items.ALWAYS_GOOD_SYMBOL_ITEMS | static_witness_items.MODE_SPECIFIC_GOOD_ITEMS[mode]
            if discards_on:
                output |= static_witness_items.MODE_SPECIFIC_GOOD_DISCARD_ITEMS[mode]

        # Remove items that are mentioned in any plando options. (Hopefully, in the future, plando will get resolved
        #   before create_items so that we'll be able to check placed items instead of just removing all items mentioned
        #   regardless of whether or not they actually wind up being manually placed.
        for plando_setting in self._multiworld.plando_items[self._player_id]:
            if plando_setting.get("from_pool", True):
                for item_setting_key in [key for key in ["item", "items"] if key in plando_setting]:
                    if isinstance(plando_setting[item_setting_key], str):
                        output -= {plando_setting[item_setting_key]}
                    elif isinstance(plando_setting[item_setting_key], dict):
                        output -= {item for item, weight in plando_setting[item_setting_key].items() if weight}
                    else:
                        # Assume this is some other kind of iterable.
                        for inner_item in plando_setting[item_setting_key]:
                            if isinstance(inner_item, str):
                                output -= {inner_item}
                            elif isinstance(inner_item, dict):
                                output -= {item for item, weight in inner_item.items() if weight}

        # Sort the output for consistency across versions if the implementation changes but the logic does not.
        return sorted(output)

    def get_door_ids_in_pool(self) -> List[int]:
        """
        Returns the total set of all door IDs that are controlled by items in the pool.
        """
        output: List[int] = []
        for item_name, item_data in dict(self.item_data.items()).items():
            if not isinstance(item_data.definition, DoorItemDefinition):
                continue
            output += [int(hex_string, 16) for hex_string in item_data.definition.panel_id_hexes]

        return output

    def get_symbol_ids_not_in_pool(self) -> List[int]:
        """
        Returns the item IDs of symbol items that were defined in the configuration file but are not in the pool.
        """
        return [
            # data.ap_code is guaranteed for a symbol definition
            cast_not_none(data.ap_code) for name, data in static_witness_items.ITEM_DATA.items()
            if name not in self.item_data.keys() and data.definition.category is ItemCategory.SYMBOL
        ]

    def get_progressive_item_ids_in_pool(self) -> Dict[int, List[int]]:
        output: Dict[int, List[int]] = {}
        for item_name, quantity in dict(self._mandatory_items.items()).items():
            item = self.item_data[item_name]
            if isinstance(item.definition, ProgressiveItemDefinition):
                # Note: we need to reference the static table here rather than the player-specific one because the child
                # items were removed from the pool when we pruned out all progression items not in the options.
                output[cast_not_none(item.ap_code)] = [cast_not_none(static_witness_items.ITEM_DATA[child_item].ap_code)
                                                       for child_item in item.definition.child_item_names]
        return output


