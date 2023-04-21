from typing import Dict, Any, Iterable, Optional, Union

from BaseClasses import Region, Entrance, Location, Item, Tutorial, CollectionState
from worlds.AutoWorld import World, WebWorld
from . import rules, logic, options
from .bundles import get_all_bundles, Bundle
from .items import item_table, create_items, ItemData, Group, items_by_group
from .locations import location_table, create_locations, LocationData
from .logic import StardewLogic, StardewRule, True_
from .options import stardew_valley_options, StardewOptions, fetch_options
from .regions import create_regions
from .rules import set_rules
from ..generic.Rules import set_rule

client_version = 0


class StardewLocation(Location):
    game: str = "Stardew Valley"

    def __init__(self, player: int, name: str, address: Optional[int], parent=None):
        super().__init__(player, name, address, parent)
        self.event = not address


class StardewItem(Item):
    game: str = "Stardew Valley"


class StardewWebWorld(WebWorld):
    theme = "dirt"
    bug_report_page = "https://github.com/agilbert1412/StardewArchipelago/issues/new?labels=bug&title=%5BBug%5D%3A+Brief+Description+of+bug+here"

    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Stardew Valley with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["KaitoKid", "Jouramie"]
    )]


class StardewValleyWorld(World):
    """
    Stardew Valley is an open-ended country-life RPG. You can farm, fish, mine, fight, complete quests,
    befriend villagers, and uncover dark secrets.
    """
    game = "Stardew Valley"
    option_definitions = stardew_valley_options
    topology_present = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    data_version = 2
    required_client_version = (0, 4, 0)

    options: StardewOptions
    logic: StardewLogic

    web = StardewWebWorld()
    modified_bundles: Dict[str, Bundle]
    randomized_entrances: Dict[str, str]

    def generate_early(self):
        self.options = fetch_options(self.multiworld, self.player)
        self.logic = StardewLogic(self.player, self.options)
        self.modified_bundles = get_all_bundles(self.multiworld.random,
                                                self.logic,
                                                self.options[options.BundleRandomization],
                                                self.options[options.BundlePrice])

    def create_regions(self):
        def create_region(name: str, exits: Iterable[str]) -> Region:
            region = Region(name, self.player, self.multiworld)
            region.exits = [Entrance(self.player, exit_name, region) for exit_name in exits]
            return region

        world_regions, self.randomized_entrances = create_regions(create_region, self.multiworld.random, self.options)
        self.multiworld.regions.extend(world_regions)

        def add_location(name: str, code: Optional[int], region: str):
            region = self.multiworld.get_region(region, self.player)
            location = StardewLocation(self.player, name, code, region)
            location.access_rule = lambda _: True
            region.locations.append(location)

        create_locations(add_location, self.options, self.multiworld.random)

    def create_items(self):
        self.precollect_starting_season()
        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]
                            if not item_table[excluded_items.name].has_any_group(Group.RESOURCE_PACK,
                                                                                 Group.FRIENDSHIP_PACK)]

        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_disabled:
            items_to_exclude = [item for item in items_to_exclude
                                if item_table[item.name] not in items_by_group[Group.SEASON]]

        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if not location.event])

        created_items = create_items(self.create_item, locations_count, items_to_exclude, self.options,
                                     self.multiworld.random)

        self.multiworld.itempool += created_items

        self.setup_early_items()
        self.setup_month_events()
        self.setup_victory()

    def precollect_starting_season(self) -> Optional[StardewItem]:
        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_progressive:
            return

        season_pool = items_by_group[Group.SEASON]

        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_disabled:
            for season in season_pool:
                self.multiworld.push_precollected(self.create_item(season))
            return

        if [item for item in self.multiworld.precollected_items[self.player]
            if item.name in {season.name for season in items_by_group[Group.SEASON]}]:
            return

        if self.options[options.SeasonRandomization] == options.SeasonRandomization.option_randomized_not_winter:
            season_pool = [season for season in season_pool if season.name != "Winter"]

        starting_season = self.create_item(self.multiworld.random.choice(season_pool))
        self.multiworld.push_precollected(starting_season)

    def setup_early_items(self):
        if (self.options[options.BuildingProgression] ==
                options.BuildingProgression.option_progressive_early_shipping_bin):
            self.multiworld.early_items[self.player]["Shipping Bin"] = 1

        if self.options[options.BackpackProgression] == options.BackpackProgression.option_early_progressive:
            self.multiworld.early_items[self.player]["Progressive Backpack"] = 1

    def setup_month_events(self):
        for i in range(0, 8):
            month_end = LocationData(None, "Stardew Valley", f"Month End {i + 1}")
            if i == 0:
                self.create_event_location(month_end, True_(), "Month End")
                continue

            self.create_event_location(month_end, self.logic.received("Month End", i).simplify(), "Month End")

    def setup_victory(self):
        if self.options[options.Goal] == options.Goal.option_community_center:
            self.create_event_location(location_table["Complete Community Center"],
                                       self.logic.can_complete_community_center().simplify(),
                                       "Victory")
        elif self.options[options.Goal] == options.Goal.option_grandpa_evaluation:
            self.create_event_location(location_table["Succeed Grandpa's Evaluation"],
                                       self.logic.can_finish_grandpa_evaluation().simplify(),
                                       "Victory")
        elif self.options[options.Goal] == options.Goal.option_bottom_of_the_mines:
            self.create_event_location(location_table["Reach the Bottom of The Mines"],
                                       self.logic.can_mine_to_floor(120).simplify(),
                                       "Victory")
        elif self.options[options.Goal] == options.Goal.option_cryptic_note:
            self.create_event_location(location_table["Complete Quest Cryptic Note"],
                                       self.logic.can_complete_quest("Cryptic Note").simplify(),
                                       "Victory")
        elif self.options[options.Goal] == options.Goal.option_master_angler:
            self.create_event_location(location_table["Catch Every Fish"],
                                       self.logic.can_catch_every_fish().simplify(),
                                       "Victory")
        elif self.options[options.Goal] == options.Goal.option_complete_collection:
            self.create_event_location(location_table["Complete the Museum Collection"],
                                       self.logic.can_complete_museum().simplify(),
                                       "Victory")
        elif self.options[options.Goal] == options.Goal.option_full_house:
            self.create_event_location(location_table["Full House"],
                                       self.logic.can_have_two_children().simplify(),
                                       "Victory")

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_item(self, item: Union[str, ItemData]) -> StardewItem:
        if isinstance(item, str):
            item = item_table[item]

        return StardewItem(item.name, item.classification, item.code, self.player)

    def create_event_location(self, location_data: LocationData, rule: StardewRule, item: Optional[str] = None):
        if item is None:
            item = location_data.name

        region = self.multiworld.get_region(location_data.region, self.player)
        location = StardewLocation(self.player, location_data.name, None, region)
        location.access_rule = rule
        region.locations.append(location)
        location.place_locked_item(self.create_item(item))

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options, self.logic, self.modified_bundles)
        self.force_first_month_once_all_early_items_are_found()

    def force_first_month_once_all_early_items_are_found(self):
        """
        The Fill algorithm sweeps all event when calculating the early location. This causes an issue where
        location only locked behind event are considered early, which they are not really...

        This patches the issue, by adding a dependency to the first month end on all early items, so all the locations
        that depends on it will not be considered early. This requires at least one early item to be progression, or
        it just won't work...
        """

        early_items = []
        for player, item_count in self.multiworld.early_items.items():
            for item, count in item_count.items():
                if self.multiworld.worlds[player].create_item(item).advancement:
                    early_items.append((player, item, count))

        for item, count in self.multiworld.local_early_items[self.player].items():
            if self.create_item(item).advancement:
                early_items.append((self.player, item, count))

        def first_month_require_all_early_items(state: CollectionState) -> bool:
            for player, item, count in early_items:
                if not state.has(item, player, count):
                    return False

            return True

        first_month_end = self.multiworld.get_location("Month End 1", self.player)
        set_rule(first_month_end, first_month_require_all_early_items)

    def generate_basic(self):
        pass

    def get_filler_item_name(self) -> str:
        return "Joja Cola"

    def fill_slot_data(self) -> Dict[str, Any]:

        modified_bundles = {}
        for bundle_key in self.modified_bundles:
            key, value = self.modified_bundles[bundle_key].to_pair()
            modified_bundles[key] = value

        excluded_options = [options.ResourcePackMultiplier, options.BundleRandomization, options.BundlePrice,
                            options.NumberOfPlayerBuffs]
        slot_data = dict(self.options.options)
        for option in excluded_options:
            slot_data.pop(option.internal_name)
        slot_data.update({
            "seed": self.multiworld.per_slot_randoms[self.player].randrange(1000000000),  # Seed should be max 9 digits
            "randomized_entrances": self.randomized_entrances,
            "modified_bundles": modified_bundles,
            "client_version": "3.0.0",
        })

        return slot_data
