from typing import Dict, Any, Iterable, Optional, Union

from BaseClasses import Region, Entrance, Location, Item, Tutorial
from worlds.AutoWorld import World, WebWorld
from . import rules, logic, options
from .bundles import get_all_bundles, Bundle
from .items import item_table, create_items, ItemData, Group
from .locations import location_table, create_locations, LocationData
from .logic import StardewLogic, StardewRule, _True, _And
from .options import stardew_valley_options, StardewOptions, fetch_options
from .regions import create_regions
from .rules import set_rules

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
    Stardew Valley farming simulator game where the objective is basically to spend the least possible time on your farm.
    """
    game = "Stardew Valley"
    option_definitions = stardew_valley_options
    topology_present = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    data_version = 1
    required_client_version = (0, 3, 9)

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
        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if not location.event])
        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]
                            if not item_table[excluded_items.name].has_any_group(Group.RESOURCE_PACK,
                                                                                 Group.FRIENDSHIP_PACK)]
        created_items = create_items(self.create_item, locations_count + len(items_to_exclude), self.options,
                                     self.multiworld.random)
        self.multiworld.itempool += created_items

        for item in items_to_exclude:
            self.multiworld.itempool.remove(item)

        self.setup_season_events()
        self.setup_victory()

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options, self.logic, self.modified_bundles)

    def create_item(self, item: Union[str, ItemData]) -> StardewItem:
        if isinstance(item, str):
            item = item_table[item]

        return StardewItem(item.name, item.classification, item.code, self.player)

    def setup_season_events(self):
        self.multiworld.push_precollected(self.create_item("Spring"))
        self.create_event_location(location_table["Summer"], self.logic.received("Spring"), "Summer")
        self.create_event_location(location_table["Fall"], self.logic.received("Summer"), "Fall")
        self.create_event_location(location_table["Winter"], self.logic.received("Fall"), "Winter")
        self.create_event_location(location_table["Year Two"], self.logic.received("Winter"), "Year Two")

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

        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_event_location(self, location_data: LocationData, rule: StardewRule, item: str):
        region = self.multiworld.get_region(location_data.region, self.player)
        location = StardewLocation(self.player, location_data.name, None, region)
        location.access_rule = rule
        region.locations.append(location)
        location.place_locked_item(self.create_item(item))

    def get_filler_item_name(self) -> str:
        return "Joja Cola"

    def fill_slot_data(self) -> Dict[str, Any]:

        modified_bundles = {}
        for bundle_key in self.modified_bundles:
            key, value = self.modified_bundles[bundle_key].to_pair()
            modified_bundles[key] = value

        return {
            "starting_money": self.options[options.StartingMoney],
            "entrance_randomization": self.options[options.EntranceRandomization],
            "backpack_progression": self.options[options.BackpackProgression],
            "tool_progression": self.options[options.ToolProgression],
            "elevator_progression": self.options[options.TheMinesElevatorsProgression],
            "skill_progression": self.options[options.SkillProgression],
            "building_progression": self.options[options.BuildingProgression],
            "arcade_machine_progression": self.options[options.ArcadeMachineLocations],
            "help_wanted_locations": self.options[options.HelpWantedLocations],
            "fishsanity": self.options[options.Fishsanity],
            "death_link": self.options["death_link"],
            "goal": self.options[options.Goal],
            "seed": self.multiworld.per_slot_randoms[self.player].randrange(1000000000),  # Seed should be max 9 digits
            "multiple_day_sleep_enabled": self.options[options.MultipleDaySleepEnabled],
            "multiple_day_sleep_cost": self.options[options.MultipleDaySleepCost],
            "experience_multiplier": self.options[options.ExperienceMultiplier],
            "debris_multiplier": self.options[options.DebrisMultiplier],
            "quick_start": self.options[options.QuickStart],
            "gifting": self.options[options.Gifting],
            "gift_tax": self.options[options.GiftTax],
            "modified_bundles": modified_bundles,
            "randomized_entrances": self.randomized_entrances,
            "client_version": "2.2.2",
        }
