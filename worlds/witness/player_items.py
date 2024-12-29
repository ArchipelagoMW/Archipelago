"""
Defines progression, junk and event items for The Witness
"""
import copy
from typing import TYPE_CHECKING, Dict, Iterable, List

from BaseClasses import Item, ItemClassification, MultiWorld

from .data import static_items as static_witness_items
from .data import static_logic as static_witness_logic
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
            if ItemClassification.progression not in data.classification
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
            if ItemClassification.progression in data.classification
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

        # Determine which items should be progression + useful, if they exist in some capacity.
        # Note: Some of these may need to be updated for the "independent symbols" PR.
        self._proguseful_items = {
            "Dots", "Stars", "Shapers", "Black/White Squares",
            "Caves Shortcuts", "Caves Mountain Shortcut (Door)", "Caves Swamp Shortcut (Door)",
            "Boat",
        }

        if self._world.options.shuffle_EPs == "individual":
            self._proguseful_items |= {
                "Town Obelisk Key",  # Most checks
                "Monastery Obelisk Key",  # Most sphere 1 checks, and also super dense ("Jackpot" vibes)}
            }

        if self._world.options.shuffle_discarded_panels:
            # Discards only give a moderate amount of checks, but are very spread out and a lot of them are in sphere 1.
            # Thus, you really want to have the discard-unlocking item as quickly as possible.

            if self._world.options.puzzle_randomization in ("none", "sigma_normal"):
                self._proguseful_items.add("Triangles")
            elif self._world.options.puzzle_randomization == "sigma_expert":
                self._proguseful_items.add("Arrows")
            # Discards require two symbols in Variety, so the "sphere 1 unlocking power" of Arrows is not there.
        if self._world.options.puzzle_randomization == "sigma_expert":
            self._proguseful_items.add("Triangles")
            self._proguseful_items.add("Full Dots")
            self._proguseful_items.add("Stars + Same Colored Symbol")
            self._proguseful_items.discard("Stars")  # Stars are not that useful on their own.
        if self._world.options.puzzle_randomization == "umbra_variety":
            self._proguseful_items.add("Triangles")

        # This needs to be improved when the improved independent&progressive symbols PR is merged
        for item in list(self._proguseful_items):
            self._proguseful_items.add(static_witness_logic.get_parent_progressive_item(item))

        for item_name, item_data in self.item_data.items():
            if item_name in self._proguseful_items:
                item_data.classification |= ItemClassification.useful


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

    def get_early_items(self, existing_items: Iterable[str]) -> Dict[str, List[str]]:
        """
        Returns items that are ideal for placing on extremely early checks, like the tutorial gate.
        """
        output: Dict[str, List[str]] = {}

        existing_items_lookup = set(existing_items)

        if "Symbol" in self._world.options.early_good_items.value:
            good_symbols = ["Dots", "Black/White Squares", "Symmetry", "Shapers", "Stars"]

            if self._world.options.shuffle_discarded_panels:
                if self._world.options.puzzle_randomization == "sigma_expert":
                    good_symbols.append("Arrows")
                else:
                    good_symbols.append("Triangles")

            # Replace progressive items with their parents.
            good_symbols = [
                static_witness_logic.get_parent_progressive_item(item) for item in good_symbols
            ]

            output["Symbol"] = [symbol for symbol in good_symbols if symbol in existing_items_lookup]

        if "Door / Door Panel" in self._world.options.early_good_items.value:
            good_doors = [
                "Desert Doors & Elevator", "Keep Hedge Maze Doors", "Keep Pressure Plates Doors",
                "Shadows Lower Doors", "Tunnels Doors", "Quarry Stoneworks Doors",

                "Keep Tower Shortcut (Door)", "Shadows Timed Door", "Tunnels Town Shortcut (Door)",
                "Quarry Stoneworks Roof Exit (Door)",

                "Desert Panels", "Keep Hedge Maze Panels",

                "Shadows Door Timer (Panel)",
            ]

            # While Caves Shortcuts don't unlock anything in symbol shuffle, you'd still rather have them early.
            # But, we need to do some special handling for them.

            if self._world.options.shuffle_doors in ("doors", "mixed"):
                # Caves Shortcuts might exist in vanilla/panel doors because of "early caves: add to pool".
                # But if the player wanted them early, they would have chosen "early caves: starting inventory".
                # This is why we make sure these are "natural" Caves Shortcuts.
                good_doors.append("Caves Shortcuts")

            # These two doors are logically equivalent, so we choose a random one as to not give them twice the chance.
            good_doors.append(
                self._world.random.choice(["Caves Mountain Shortcut (Door)", "Caves Swamp Shortcut (Door)"])
            )

            if self._world.options.shuffle_vault_boxes and not self._world.options.disable_non_randomized_puzzles:
                good_doors.append("Windmill & Theater Doors")
                if not self._world.options.shuffle_symbols:
                    good_doors += [
                        "Windmill & Theater Panels",

                        "Windmill & Theater Control Panels",
                    ]

            if self._world.options.shuffle_doors == "doors":  # It's not as good in mixed doors because of Light Control
                good_doors.append("Desert Light Room Entry (Door)")

            if not self._world.options.shuffle_symbols:
                good_doors += [
                    "Bunker Doors", "Swamp Doors", "Glass Factory Doors", "Town Doors",

                    "Bunker Entry (Door)", "Glass Factory Entry (Door)", "Symmetry Island Lower (Door)",

                    "Bunker Panels", "Swamp Panels", "Quarry Outside Panels", "Glass Factory Panels"

                    "Glass Factory Entry (Panel)",
                ]

            existing_doors = [door for door in good_doors if door in existing_items_lookup]

            # On some options combinations with doors, there just aren't a lot of doors that unlock much early.
            # In this case, we add some doors that aren't great, but are at least guaranteed to unlock 1 location.

            fallback_doors = [
                "Keep Shadows Shortcut (Door)",  # Always Keep Shadows Shortcut Panel
                "Keep Shortcuts",  # -"-
                "Keep Pressure Plates Doors",  # -"-
                "Keep Hedge Maze 1 (Panel)",  # Always Hedge 1
                "Town Maze Stairs (Panel)",  # Always Maze Panel
                "Shadows Laser Room Doors",  # Always Shadows Laser Panel
                "Swamp Laser Shortcut (Door)",  # Always Swamp Laser
                "Town Maze Panels",  # Always Town Maze Panel
                "Town Doors",  # Always Town Church Lattice
                "Town Church Entry (Door)",  # -"-
                "Town Tower Doors",  # Always Town Laser
            ]
            self._world.random.shuffle(fallback_doors)

            while len(existing_doors) < 4 and fallback_doors:
                fallback_door = fallback_doors.pop()
                if fallback_door in existing_items_lookup and fallback_door not in existing_doors:
                    existing_doors.append(fallback_door)

            output["Door"] = existing_doors

        if "Obelisk Key" in self._world.options.early_good_items.value:
            obelisk_keys = [
                "Desert Obelisk Key", "Town Obelisk Key", "Quarry Obelisk Key",
                "Treehouse Obelisk Key", "Monastery Obelisk Key", "Mountainside Obelisk Key"
            ]
            output["Obelisk Key"] = [key for key in obelisk_keys if key in existing_items_lookup]

        assert all(item in self._world.item_names for sublist in output.values() for item in sublist), (
            [item for sublist in output.values() for item in sublist if item not in self._world.item_names]
        )

        # Cull empty lists
        return {item_type: item_list for item_type, item_list in output.items() if item_list}

    def get_door_item_ids_in_pool(self) -> List[int]:
        """
        Returns the ids of all door items that exist in the pool.
        """

        return [
            cast_not_none(item_data.ap_code) for item_data in self.item_data.values()
            if isinstance(item_data.definition, DoorItemDefinition)
        ]

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
