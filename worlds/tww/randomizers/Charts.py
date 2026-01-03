from typing import TYPE_CHECKING

from ..Enums import SectorName
from ..Items import ISLAND_NUMBER_TO_CHART_NAME
from ..Locations import TWWFlag, TWWLocation

if TYPE_CHECKING:
    from .. import TWWWorld

ISLAND_NUMBER_TO_NAME: dict[int, str] = {
    1: SectorName.FORSAKEN_FORTRESS_SECTOR.value,
    2: SectorName.STAR_ISLAND.value,
    3: SectorName.NORTHERN_FAIRY_ISLAND.value,
    4: SectorName.GALE_ISLE.value,
    5: SectorName.CRESCENT_MOON_ISLAND.value,
    6: SectorName.SEVEN_STAR_ISLES.value,
    7: SectorName.OVERLOOK_ISLAND.value,
    8: SectorName.FOUR_EYE_REEF.value,
    9: SectorName.MOTHER_AND_CHILD_ISLES.value,
    10: SectorName.SPECTACLE_ISLAND.value,
    11: SectorName.WINDFALL_ISLAND.value,
    12: SectorName.PAWPRINT_ISLE.value,
    13: SectorName.DRAGON_ROOST_ISLAND.value,
    14: SectorName.FLIGHT_CONTROL_PLATFORM.value,
    15: SectorName.WESTERN_FAIRY_ISLAND.value,
    16: SectorName.ROCK_SPIRE_ISLE.value,
    17: SectorName.TINGLE_ISLAND.value,
    18: SectorName.NORTHERN_TRIANGLE_ISLAND.value,
    19: SectorName.EASTERN_FAIRY_ISLAND.value,
    20: SectorName.FIRE_MOUNTAIN.value,
    21: SectorName.STAR_BELT_ARCHIPELAGO.value,
    22: SectorName.THREE_EYE_REEF.value,
    23: SectorName.GREATFISH_ISLE.value,
    24: SectorName.CYCLOPS_REEF.value,
    25: SectorName.SIX_EYE_REEF.value,
    26: SectorName.TOWER_OF_THE_GODS_SECTOR.value,
    27: SectorName.EASTERN_TRIANGLE_ISLAND.value,
    28: SectorName.THORNED_FAIRY_ISLAND.value,
    29: SectorName.NEEDLE_ROCK_ISLE.value,
    30: SectorName.ISLET_OF_STEEL.value,
    31: SectorName.STONE_WATCHER_ISLAND.value,
    32: SectorName.SOUTHERN_TRIANGLE_ISLAND.value,
    33: SectorName.PRIVATE_OASIS.value,
    34: SectorName.BOMB_ISLAND.value,
    35: SectorName.BIRD_S_PEAK_ROCK.value,
    36: SectorName.DIAMOND_STEPPE_ISLAND.value,
    37: SectorName.FIVE_EYE_REEF.value,
    38: SectorName.SHARK_ISLAND.value,
    39: SectorName.SOUTHERN_FAIRY_ISLAND.value,
    40: SectorName.ICE_RING_ISLE.value,
    41: SectorName.FOREST_HAVEN.value,
    42: SectorName.CLIFF_PLATEAU_ISLES.value,
    43: SectorName.HORSESHOE_ISLAND.value,
    44: SectorName.OUTSET_ISLAND.value,
    45: SectorName.HEADSTONE_ISLAND.value,
    46: SectorName.TWO_EYE_REEF.value,
    47: SectorName.ANGULAR_ISLES.value,
    48: SectorName.BOATING_COURSE.value,
    49: SectorName.FIVE_STAR_ISLES.value,
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

    def setup_progress_sunken_treasure_locations(self, skip_randomization: bool = False) -> None:
        """
        Create the locations for sunken treasure locations and update them as progression and non-progression
        appropriately. If the option is enabled, randomize which charts point to which sector.

        :param skip_randomization: If True, skip chart randomization (used during UT restoration).
        """
        options = self.world.options

        original_item_names = list(self.island_number_to_chart_name.values())

        # Shuffles the list of island numbers if charts are randomized.
        # The shuffled island numbers determine which sector each chart points to.
        # However, if skip_randomization is True, the charts remain in their pre-loaded state.
        shuffled_island_numbers = list(self.island_number_to_chart_name.keys())
        if options.randomize_charts and not skip_randomization:
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
