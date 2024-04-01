import logging
from typing import Dict, Any, Iterable, Optional, Union, List, TextIO

from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, MultiWorld
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from . import rules
from .bundles.bundle_room import BundleRoom
from .bundles.bundles import get_all_bundles
from .early_items import setup_early_items
from .items import item_table, create_items, ItemData, Group, items_by_group, get_all_filler_items, remove_limited_amount_packs
from .locations import location_table, create_locations, LocationData, locations_by_tag
from .options import StardewValleyOptions, SeasonRandomization, Goal, BundleRandomization, BundlePrice, NumberOfLuckBuffs, NumberOfMovementBuffs, \
    BackpackProgression, BuildingProgression, ExcludeGingerIsland, TrapItems, EntranceRandomization
from .presets import sv_options_presets
from .regions import create_regions
from .rules import set_rules
from .stardew_rule import True_, StardewRule, HasProgressionPercent
from .strings.ap_names.event_names import Event
from .strings.entrance_names import Entrance as EntranceName
from .strings.goal_names import Goal as GoalName
from .strings.region_names import Region as RegionName

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
    options_presets = sv_options_presets

    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to playing Stardew Valley with Archipelago.",
            "English",
            "setup_en.md",
            "setup/en",
            ["KaitoKid", "Jouramie", "Witchybun (Mod Support)", "Exempt-Medic (Proofreading)"]
        )]


class StardewValleyWorld(World):
    """
    Stardew Valley is an open-ended country-life RPG. You can farm, fish, mine, fight, complete quests,
    befriend villagers, and uncover dark secrets.
    """
    game = "Stardew Valley"
    topology_present = False

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in location_table.items()}

    item_name_groups = {
        group.name.replace("_", " ").title() + (" Group" if group.name.replace("_", " ").title() in item_table else ""):
            [item.name for item in items] for group, items in items_by_group.items()
    }
    location_name_groups = {
        group.name.replace("_", " ").title() + (" Group" if group.name.replace("_", " ").title() in locations_by_tag else ""):
            [location.name for location in locations] for group, locations in locations_by_tag.items()
    }

    data_version = 3
    required_client_version = (0, 4, 0)

    options_dataclass = StardewValleyOptions
    options: StardewValleyOptions

    web = StardewWebWorld()
    modified_bundles: List[BundleRoom]
    randomized_entrances: Dict[str, str]

    # all_progression_items: Dict[str, int] # If you need to debug total_progression_items, uncommenting this will help tremendously

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.filler_item_pool_names = []

    def generate_early(self):
        self.force_change_options_if_incompatible()

    def force_change_options_if_incompatible(self):
        logging.warning(f"A player is about to play Stardew. Get ready for a lot of BK!")

    def create_regions(self):
        def create_region(name: str, exits: Iterable[str]) -> Region:
            region = Region(name, self.player, self.multiworld)
            region.exits = [Entrance(self.player, exit_name, region) for exit_name in exits]
            return region

        world_regions, world_entrances, self.randomized_entrances = create_regions(create_region, self.random, self.options)

        self.modified_bundles = get_all_bundles(self.random,
                                                self.options)

        def add_location(name: str, code: Optional[int], region: str):
            region = world_regions[region]
            location = StardewLocation(self.player, name, code, region)
            region.locations.append(location)

        create_locations(add_location, self.modified_bundles, self.options, self.random)
        self.multiworld.regions.extend(world_regions.values())

    def create_items(self):
        self.precollect_starting_season()
        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]
                            if not item_table[excluded_items.name].has_any_group(Group.RESOURCE_PACK,
                                                                                 Group.FRIENDSHIP_PACK)]

        if self.options.season_randomization == SeasonRandomization.option_disabled:
            items_to_exclude = [item for item in items_to_exclude
                                if item_table[item.name] not in items_by_group[Group.SEASON]]

        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if not location.event])

        created_items = create_items(self.create_item, self.delete_item, locations_count, items_to_exclude, self.options,
                                     self.random)

        self.multiworld.itempool += created_items

        setup_early_items(self.multiworld, self.options, self.player, self.random)
        self.setup_player_events()
        self.setup_victory()

    def precollect_starting_season(self):
        # Well, damn, Jackie. I can't control the weather!
        pass

    def setup_player_events(self):
        # Don't worry, the canon events always happenn
        pass

    def setup_victory(self):
        # Look we all know the community center is the only valid goal
        self.create_event_location(location_table[GoalName.community_center],
                                   True_(),
                                   Event.victory)

        self.multiworld.completion_condition[self.player] = lambda state: state.has(Event.victory, self.player)

    def get_all_location_names(self) -> List[str]:
        return list(location.name for location in self.multiworld.get_locations(self.player))

    def create_item(self, item: Union[str, ItemData], override_classification: ItemClassification = None) -> StardewItem:
        if isinstance(item, str):
            item = item_table[item]

        # It's probably fine
        override_classification = ItemClassification.filler

        return StardewItem(item.name, override_classification, item.code, self.player)

    def delete_item(self, item: Item):
        # alwaysintreble — 25/03/2024 22:54
        # I don't understand why you're doing it this way it sounds backwards
        pass

    def create_event_location(self, location_data: LocationData, rule: StardewRule = None, item: Optional[str] = None):
        if rule is None:
            rule = True_()
        if item is None:
            item = location_data.name

        region = self.multiworld.get_region(location_data.region, self.player)
        location = StardewLocation(self.player, location_data.name, None, region)
        location.access_rule = rule
        region.locations.append(location)
        location.place_locked_item(self.create_item(item))

    def set_rules(self):
        set_rules(self)

    def generate_basic(self):
        # Go to your nearest Starbucks, you'll find plenty
        pass

    def get_filler_item_name(self) -> str:
        return "Time to break ItemLinks"

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler header. If individual it's right at the end of that player's options,
        if as stage it's right under the common header before per-player options."""
        self.add_entrances_to_spoiler_log(spoiler_handle)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler "middle", this is after the per-player options and before locations,
        meant for useful or interesting info."""
        self.add_bundles_to_spoiler_log(spoiler_handle)

    def add_bundles_to_spoiler_log(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"Ask the Wizard smh")

    def add_entrances_to_spoiler_log(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"https://www.google.ca/maps")

    def fill_slot_data(self) -> Dict[str, Any]:
        bundles = dict()
        for room in self.modified_bundles:
            bundles[room.name] = dict()
            for bundle in room.bundles:
                bundles[room.name][bundle.name] = {"number_required": bundle.number_required}
                for i, item in enumerate(bundle.items):
                    bundles[room.name][bundle.name][i] = f"{item.item_name}|{item.amount}|{item.quality}"

        excluded_options = [BundleRandomization, NumberOfMovementBuffs, NumberOfLuckBuffs]
        excluded_option_names = [option.internal_name for option in excluded_options]
        generic_option_names = [option_name for option_name in PerGameCommonOptions.type_hints]
        excluded_option_names.extend(generic_option_names)
        included_option_names: List[str] = [option_name for option_name in self.options_dataclass.type_hints if option_name not in excluded_option_names]
        slot_data = self.options.as_dict(*included_option_names)
        slot_data.update({
            "seed": self.random.randrange(1000000000),  # Seed should be max 9 digits
            "randomized_entrances": self.randomized_entrances,
            "modified_bundles": bundles,
            "client_version": "5.0.0",
            "Difficulty": "Good Luck"
        })

        return slot_data
