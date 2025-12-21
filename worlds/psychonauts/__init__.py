from typing import Mapping, Any, ClassVar, Dict, Set

import settings
from BaseClasses import Item
from BaseClasses import Tutorial, ItemClassification, MultiWorld
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths
from . import Regions
from . import Rules
from .ItemUtils import repeated_item_names_gen
from .Items import (
    ITEM_DICTIONARY,
    MINDS,
    BRAIN_JARS,
    BAGGAGE,
    BAGGAGE_TAGS,
    LOCAL_SET,
    PROGRESSION_SET,
    USEFUL_SET,
    ITEM_GROUPS,
    ITEM_COUNT,
    AP_ITEM_OFFSET,
    BASE_ITEM_CLASSIFICATIONS,
    SKIP_BALANCING_FOR_DUPLICATES,
)
from .Locations import ALL_LOCATIONS, AP_LOCATION_OFFSET, DEEP_ARROWHEAD_LOCATIONS, MENTAL_COBWEB_LOCATIONS, RANK_LOCATIONS
from .Names import ItemName, LocationName
from .Options import Goal, PsychonautsOptions, SLOT_DATA_OPTIONS
from .PsychoSeed import gen_psy_seed
from .Subclasses import PSYItem


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="PsychonautsClient")


components.append(Component("Psychonauts Client", 
                            func=launch_client, 
                            component_type=Type.CLIENT, 
                            icon="AP_Merit_Badge"))

icon_paths["AP_Merit_Badge"] = f"ap:{__name__}/Icons/AP_Merit_Badge.png"


class PsychonautsSettings(settings.Group):
    class RootDirectory(settings.UserFolderPath):
        """
        Locate the Psychonauts root directory on your system.
        This is used by the Psychonauts client, so it knows where to send communication files to
        """
        description = "Psychonauts root directory"

    root_directory: RootDirectory = RootDirectory(r"C:\\Program Files (x86)\\Steam\\steamapps\\common\\Psychonauts")


class PsychonautsWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Psychonauts with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Akashortstack"]
    )]


class PSYWorld(World):
    """
    Psychonauts is a third-person action platformer game developed by Double Fine Productions, published by Majesco Entertainment, and released in 2005.
    The player follows Razputin, a young boy gifted with psychic abilities. After sneaking into Whispering Rock Psychic Summer Camp, it's up to Raz to explore 
    the minds of other characters in order to save his fellow psychic campers, and the world, from an evil threat.
    
    """
    game = "Psychonauts"
    web = PsychonautsWeb()

    settings: ClassVar[PsychonautsSettings]
    required_client_version = (0, 4, 6)
    options_dataclass = PsychonautsOptions
    options: PsychonautsOptions

    item_name_to_id = {item: id + AP_ITEM_OFFSET for item, id in ITEM_DICTIONARY.items()}

    item_name_groups = ITEM_GROUPS

    location_name_to_id = {item: id + AP_LOCATION_OFFSET for item, id in ALL_LOCATIONS.items()}

    item_classifications: Dict[str, ItemClassification]

    skip_balancing_if_duplicate: Set[str]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.item_classifications = BASE_ITEM_CLASSIFICATIONS.copy()
        # Tracks created items where additional created items with the same name should skip progression balancing.
        self.skip_balancing_if_duplicate = set()

    def generate_early(self) -> None:
        """
        Using this to make Baggage local only and determine item classifications that depend on options.
        """
        for item in LOCAL_SET:
            self.options.local_items.value.add(item)

        # Set item classifications that depend on options.
        item_classifications = self.item_classifications
        goal = self.options.Goal

        # Set brains to Progression, when the Brain Hunt goal is enabled.
        # Skip balancing because Brains are macguffins and are only required for the goal.
        if goal == Goal.option_brain_hunt or goal == Goal.option_asylum_brain_tank_and_brain_hunt:
            for name in BRAIN_JARS:
                item_classifications[name] = ItemClassification.progression_skip_balancing

        # Set Birthday Cake to Filler, when the Brain Tank goal is not enabled.
        if goal == Goal.option_brain_hunt:
            item_classifications[ItemName.Cake] = ItemClassification.filler

        # Set Baggage and Baggage Tags to Progression if Progessive Baggage enabled
        # Skip balancing because Baggage is all local, tags can be anywhere.
        if self.options.ProgressiveBaggage and self.options.MaximumProgressiveBaggage !=0:
            for name in BAGGAGE:
                item_classifications[name] = ItemClassification.progression_skip_balancing
            for name in BAGGAGE_TAGS:
                item_classifications[name] = ItemClassification.progression_skip_balancing

    def create_item(self, name: str) -> Item:
        """
        Returns created PSYItem
        """
        # If an item does not have a classification defined, default to Filler.
        item_classification = self.item_classifications.get(name, ItemClassification.filler)

        # Some duplicates of Progression items should skip progression balancing because the duplicates are only
        # required to access very few or no locations.
        if item_classification == ItemClassification.progression and name in SKIP_BALANCING_FOR_DUPLICATES:
            if name in self.skip_balancing_if_duplicate:
                item_classification = ItemClassification.progression_skip_balancing
            else:
                self.skip_balancing_if_duplicate.add(name)

        return PSYItem(name, item_classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return ItemName.PsiCard

    def create_event_item(self, name: str) -> Item:
        created_item = PSYItem(name, ItemClassification.progression, None, self.player)
        return created_item

    @staticmethod
    def _add_deep_arrowhead_shuffle_items(item_counts: Dict[str, int]):
        # The Dowsing Rod is added to the item pool.
        item_counts[ItemName.DowsingRod] += 1

        # Additional small and large arrowhead bundles are added to the pool.
        # Each deep arrowhead has a specific worth of arrowheads given to the player when dug up, the total is 2696.
        # There are currently 49 Deep Arrowhead locations, so the average worth of a deep arrowhead is currently 55.02,
        # more than a small arrowhead bundle (25), but less than a large arrowhead bundle (100).
        # 29 * 25 + 20 * 100 = 2725
        small_count = 29
        large_count = 20
        # To find the optimal combination of small and large arrowhead bundles:
        # # Start with all large bundles and find how many need to be replaced with small bundles to reach the total.
        # total_deep_arrowhead_worth = 2696
        # small_ah_bundle_worth = 25
        # large_ah_bundle_worth = 100
        # # Each time a large bundle is replaced with a small bundle, the total decreases by this much.
        # bundle_difference = large_ah_bundle_worth - small_ah_bundle_worth
        #
        # num_deep_arrowhead_locations = len(deep_arrowhead_locations)
        # excess_arrowheads = large_ah_bundle_worth * num_deep_arrowhead_locations - total_deep_arrowhead_worth
        #
        # # Truncating any remainder using integer division means that when there is not a whole number, the total
        # # worth of arrowheads from added bundles will be slightly more than `total_deep_arrowhead_worth`.
        # small_count = excess_arrowheads // bundle_difference
        # large_count = num_deep_arrowhead_locations - small_count

        # Adjust how many of each item to add to the item pool.
        item_counts[ItemName.AHSmall] += small_count
        item_counts[ItemName.AHLarge] += large_count

    @staticmethod
    def _add_mental_cobweb_shuffle_items(item_counts: Dict[str, int]):
        # A single Mental Cobweb can normally be turned into a PSI Card at the loom in Ford's Sanctuary, so add as many
        # PSI Cards to the pool as Mental Cobweb Locations.
        item_counts[ItemName.PsiCard] += len(MENTAL_COBWEB_LOCATIONS)

    @staticmethod
    def _add_rank_sanity_items(item_counts: Dict[str, int]):
        # Add PSI Cards to the pool to fill empty ranks
        extra_rank_count = 80
        item_counts[ItemName.PsiCard] += extra_rank_count

    @staticmethod
    def _add_figment_percentage_items(item_counts: Dict[str, int], maxpercent: int):
        # Add PSI Cards to the pool to fill figment percentage checks
        # Multiplied by the FigmentPercentageChecks option value
        percentage_count = maxpercent*10
        item_counts[ItemName.PsiCard] += percentage_count

    @staticmethod
    def _add_progressive_baggage_items(item_counts: Dict[str, int], maxvalue: int):
        # Add PSIChallengeMarkers to the pool to fill progressive baggage checks
        # Multiplied by the MaximumProgressiveBaggage option value
        baggage_count = maxvalue*5
        item_counts[ItemName.ChallengeMarker] += baggage_count


    def create_items(self):
        """
        Fills ItemPool 
        """
        num_locations_to_fill = len(self.multiworld.get_unfilled_locations(self.player))

        adjusted_item_counts = ITEM_COUNT.copy()

        # remove start_inventory items from our adjusted_item_counts
        # start_inventory is StartInventoryPool, removes items from pool as well
        for item_name, value in self.options.start_inventory.items():
            adjusted_item_counts[item_name] -= value

        # Pre-collect starting minds and remove them from the item pool.
        num_starting_minds = self.options.RandomStartingMinds.value
        if num_starting_minds > 0:
            mind_unlocks = list(MINDS)
            # If start_inventory contains any minds or sasha's button, remove from MINDS list first
            for item_name, value in self.options.start_inventory.items():
                if item_name in mind_unlocks:
                    mind_unlocks.remove(item_name)

            # make sure num_starting_minds is never greater than mind_unlocks list
            # can happen if using start_inventory and starting minds is high
            num_starting_minds = min(num_starting_minds, len(mind_unlocks))

            for _ in range(num_starting_minds):
                # Pop a random mind from the list.
                item = mind_unlocks.pop(self.random.randrange(len(mind_unlocks)))
                # Reduce the number to add to the pool.
                adjusted_item_counts[item] -= 1
                self.multiworld.push_precollected(self.create_item(item))

        # Pre-collect the Cobweb Duster when starting with it.
        if self.options.StartingCobwebDuster:
            # Reduce the count to add to the item pool.
            adjusted_item_counts[ItemName.CobwebDuster] -= 1
            self.multiworld.push_precollected(self.create_item(ItemName.CobwebDuster))

        # Pre-collect one Progressive Levitation when starting with it.
        if self.options.StartingLevitation:
            # Reduce the count to add to the item pool.
            adjusted_item_counts[ItemName.Levitation] -= 1
            self.multiworld.push_precollected(self.create_item(ItemName.Levitation))

        # Add items for DeepArrowheadShuffle
        if self.options.DeepArrowheadShuffle:
            self._add_deep_arrowhead_shuffle_items(adjusted_item_counts)

        # Add items for MentalCobwebShuffle
        if self.options.MentalCobwebShuffle:
            self._add_mental_cobweb_shuffle_items(adjusted_item_counts)
        
        # Add items for RankSanity
        if self.options.RankSanity:
            self._add_rank_sanity_items(adjusted_item_counts)

        # Add items for FigmentPercentageChecks
        # add 10 items to the pool for every 20 percent required, maximum 50
        if self.options.FigmentPercentageChecks.value >= 1:
            self._add_figment_percentage_items(adjusted_item_counts, self.options.FigmentPercentageChecks.value)

        # Add items for MaximumProgressiveBaggage
        # Passes the value for MaximumProgressiveBaggage Option, adds value multiplied by 5
        # Maximum 50
        if self.options.ProgressiveBaggage and self.options.MaximumProgressiveBaggage.value !=0:
            self._add_progressive_baggage_items(adjusted_item_counts, self.options.MaximumProgressiveBaggage.value)

        # Create the initial item pool.
        item_pool = list(map(self.create_item, repeated_item_names_gen(ITEM_DICTIONARY, adjusted_item_counts)))

        assert len(item_pool) <= num_locations_to_fill, ("The initial item pool cannot be larger than the number of"
                                                         " unfilled locations.")
        num_locations_to_fill -= len(item_pool)

        # Create filler for the remaining locations.
        item_pool.extend(self.create_filler() for _ in range(num_locations_to_fill))

        self.multiworld.itempool += item_pool

    def create_regions(self):
        """
        Creates the Regions and Connects them.
        """
        Regions.create_psyregions(self.multiworld, self.player)
        Regions.connect_regions(self.multiworld, self.player)
        Regions.place_events(self)

        if self.options.FigmentPercentageChecks.value >= 1:
            Regions.create_figments_20_locations(self.multiworld, self.player)
        if self.options.FigmentPercentageChecks.value >= 2:
            Regions.create_figments_40_locations(self.multiworld, self.player)
        if self.options.FigmentPercentageChecks.value >= 3:
            Regions.create_figments_60_locations(self.multiworld, self.player)
        if self.options.FigmentPercentageChecks.value >= 4:
            Regions.create_figments_80_locations(self.multiworld, self.player)
        if self.options.FigmentPercentageChecks.value == 5:
            Regions.create_figments_100_locations(self.multiworld, self.player)
        if self.options.ProgressiveBaggage and self.options.MaximumProgressiveBaggage.value !=0:
            Regions.create_progressive_baggage_locations(self.multiworld, self.player, self.options.MaximumProgressiveBaggage.value)
        if self.options.DeepArrowheadShuffle:
            Regions.create_deep_arrowhead_locations(self.multiworld, self.player)
        if self.options.MentalCobwebShuffle:
            Regions.create_mental_cobweb_locations(self.multiworld, self.player)
        if self.options.RankSanity:
            Regions.create_100_rank_locations(self.multiworld, self.player)
        else:
            Regions.create_20_rank_locations(self.multiworld, self.player)

    def set_rules(self):
        """
        Sets the Logic for the Regions and Locations.
        """
        universal_logic = Rules.PsyRules(self)
        universal_logic.set_psy_rules()

    def generate_output(self, output_directory: str):
        """
        Generates the seed file for Randomizer Scripts folder 
        """
        # Creates RandoSeed.lua file for Randomizer Mod
        # Example found in /docs
        gen_psy_seed(self, output_directory)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(*SLOT_DATA_OPTIONS)
