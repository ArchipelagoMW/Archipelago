from typing import TYPE_CHECKING

from ..Items import ISLAND_NUMBER_TO_CHART_NAME
from ..Locations import TWWFlag, TWWLocation

if TYPE_CHECKING:
    from .. import TWWWorld

ISLAND_NUMBER_TO_NAME: dict[int, str] = {
    1: "Forsaken Fortress Sector",
    2: "Star Island",
    3: "Northern Fairy Island",
    4: "Gale Isle",
    5: "Crescent Moon Island",
    6: "Seven-Star Isles",
    7: "Overlook Island",
    8: "Four-Eye Reef",
    9: "Mother and Child Isles",
    10: "Spectacle Island",
    11: "Windfall Island",
    12: "Pawprint Isle",
    13: "Dragon Roost Island",
    14: "Flight Control Platform",
    15: "Western Fairy Island",
    16: "Rock Spire Isle",
    17: "Tingle Island",
    18: "Northern Triangle Island",
    19: "Eastern Fairy Island",
    20: "Fire Mountain",
    21: "Star Belt Archipelago",
    22: "Three-Eye Reef",
    23: "Greatfish Isle",
    24: "Cyclops Reef",
    25: "Six-Eye Reef",
    26: "Tower of the Gods Sector",
    27: "Eastern Triangle Island",
    28: "Thorned Fairy Island",
    29: "Needle Rock Isle",
    30: "Islet of Steel",
    31: "Stone Watcher Island",
    32: "Southern Triangle Island",
    33: "Private Oasis",
    34: "Bomb Island",
    35: "Bird's Peak Rock",
    36: "Diamond Steppe Island",
    37: "Five-Eye Reef",
    38: "Shark Island",
    39: "Southern Fairy Island",
    40: "Ice Ring Isle",
    41: "Forest Haven",
    42: "Cliff Plateau Isles",
    43: "Horseshoe Island",
    44: "Outset Island",
    45: "Headstone Island",
    46: "Two-Eye Reef",
    47: "Angular Isles",
    48: "Boating Course",
    49: "Five-Star Isles",
}


class ChartRandomizer:
    """
    This class handles the randomization of charts.
    Each chart points to a specific island on the map, and this randomizer shuffles these mappings.

    :param world: The Wind Waker game world.
    """

    def __init__(self, world: "TWWWorld") -> None:
        self.world = world
        self.multiworld = world.multiworld

        self.island_number_to_chart_name = ISLAND_NUMBER_TO_CHART_NAME.copy()

    def setup_progress_sunken_treasure_locations(self) -> None:
        """
        Create the locations for sunken treasure locations and update them as progression and non-progression
        appropriately. If the option is enabled, randomize which charts point to which sector.
        """
        options = self.world.options

        original_item_names = list(self.island_number_to_chart_name.values())

        # Shuffles the list of island numbers if charts are randomized.
        # The shuffled island numbers determine which sector each chart points to.
        shuffled_island_numbers = list(self.island_number_to_chart_name.keys())
        if options.randomize_charts:
            self.world.random.shuffle(shuffled_island_numbers)

        for original_item_name in reversed(original_item_names):
            # Assign each chart to its new island.
            shuffled_island_number = shuffled_island_numbers.pop()
            self.island_number_to_chart_name[shuffled_island_number] = original_item_name

            # Additionally, determine if that location is a progress location or not.
            island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
            island_location = f"{island_name} - Sunken Treasure"
            if options.progression_triforce_charts or options.progression_treasure_charts:
                if original_item_name.startswith("Triforce Chart "):
                    if options.progression_triforce_charts:
                        self.world.progress_locations.add(island_location)
                        self.world.nonprogress_locations.remove(island_location)
                else:
                    if options.progression_treasure_charts:
                        self.world.progress_locations.add(island_location)
                        self.world.nonprogress_locations.remove(island_location)
            else:
                self.world.nonprogress_locations.add(island_location)

    def update_chart_location_flags(self) -> None:
        """
        Update the flags for sunken treasure locations based on the current chart mappings.
        """
        for shuffled_island_number, item_name in self.island_number_to_chart_name.items():
            island_name = ISLAND_NUMBER_TO_NAME[shuffled_island_number]
            island_location_str = f"{island_name} - Sunken Treasure"

            if island_location_str in self.world.progress_locations:
                island_location = self.world.get_location(island_location_str)
                assert isinstance(island_location, TWWLocation)
                if item_name.startswith("Triforce Chart "):
                    island_location.flags = TWWFlag.TRI_CHT
                else:
                    island_location.flags = TWWFlag.TRE_CHT
