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
from .logic.bundle_logic import BundleLogic
from .logic.logic import StardewLogic
from .logic.time_logic import MAX_MONTHS
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
    logic: StardewLogic

    web = StardewWebWorld()
    modified_bundles: List[BundleRoom]
    randomized_entrances: Dict[str, str]
    total_progression_items: int

    # all_progression_items: Dict[str, int] # If you need to debug total_progression_items, uncommenting this will help tremendously

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.filler_item_pool_names = []
        self.total_progression_items = 0
        # self.all_progression_items = dict()

    def generate_early(self):
        self.force_change_options_if_incompatible()

    def force_change_options_if_incompatible(self):
        goal_is_walnut_hunter = self.options.goal == Goal.option_greatest_walnut_hunter
        goal_is_perfection = self.options.goal == Goal.option_perfection
        goal_is_island_related = goal_is_walnut_hunter or goal_is_perfection
        exclude_ginger_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true
        if goal_is_island_related and exclude_ginger_island:
            self.options.exclude_ginger_island.value = ExcludeGingerIsland.option_false
            goal_name = self.options.goal.current_key
            player_name = self.multiworld.player_name[self.player]
            logging.warning(
                f"Goal '{goal_name}' requires Ginger Island. Exclude Ginger Island setting forced to 'False' for player {self.player} ({player_name})")

    def create_regions(self):
        def create_region(name: str, exits: Iterable[str]) -> Region:
            region = Region(name, self.player, self.multiworld)
            region.exits = [Entrance(self.player, exit_name, region) for exit_name in exits]
            return region

        world_regions, world_entrances, self.randomized_entrances = create_regions(create_region, self.random, self.options)

        self.logic = StardewLogic(self.player, self.options, world_regions.keys())
        self.modified_bundles = get_all_bundles(self.random,
                                                self.logic,
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
        if self.options.season_randomization == SeasonRandomization.option_progressive:
            return

        season_pool = items_by_group[Group.SEASON]

        if self.options.season_randomization == SeasonRandomization.option_disabled:
            for season in season_pool:
                self.multiworld.push_precollected(self.create_starting_item(season))
            return

        if [item for item in self.multiworld.precollected_items[self.player]
            if item.name in {season.name for season in items_by_group[Group.SEASON]}]:
            return

        if self.options.season_randomization == SeasonRandomization.option_randomized_not_winter:
            season_pool = [season for season in season_pool if season.name != "Winter"]

        starting_season = self.create_starting_item(self.random.choice(season_pool))
        self.multiworld.push_precollected(starting_season)

    def setup_player_events(self):
        self.setup_construction_events()
        self.setup_quest_events()
        self.setup_action_events()

    def setup_construction_events(self):
        can_construct_buildings = LocationData(None, RegionName.carpenter, Event.can_construct_buildings)
        self.create_event_location(can_construct_buildings, True_(), Event.can_construct_buildings)

    def setup_quest_events(self):
        start_dark_talisman_quest = LocationData(None, RegionName.railroad, Event.start_dark_talisman_quest)
        self.create_event_location(start_dark_talisman_quest, self.logic.wallet.has_rusty_key(), Event.start_dark_talisman_quest)

    def setup_action_events(self):
        can_ship_event = LocationData(None, RegionName.shipping, Event.can_ship_items)
        self.create_event_location(can_ship_event, True_(), Event.can_ship_items)
        can_shop_pierre_event = LocationData(None, RegionName.pierre_store, Event.can_shop_at_pierre)
        self.create_event_location(can_shop_pierre_event, True_(), Event.can_shop_at_pierre)

    def setup_victory(self):
        if self.options.goal == Goal.option_community_center:
            self.create_event_location(location_table[GoalName.community_center],
                                       self.logic.bundle.can_complete_community_center,
                                       Event.victory)
        elif self.options.goal == Goal.option_grandpa_evaluation:
            self.create_event_location(location_table[GoalName.grandpa_evaluation],
                                       self.logic.can_finish_grandpa_evaluation(),
                                       Event.victory)
        elif self.options.goal == Goal.option_bottom_of_the_mines:
            self.create_event_location(location_table[GoalName.bottom_of_the_mines],
                                       True_(),
                                       Event.victory)
        elif self.options.goal == Goal.option_cryptic_note:
            self.create_event_location(location_table[GoalName.cryptic_note],
                                       self.logic.quest.can_complete_quest("Cryptic Note"),
                                       Event.victory)
        elif self.options.goal == Goal.option_master_angler:
            self.create_event_location(location_table[GoalName.master_angler],
                                       self.logic.fishing.can_catch_every_fish_in_slot(self.get_all_location_names()),
                                       Event.victory)
        elif self.options.goal == Goal.option_complete_collection:
            self.create_event_location(location_table[GoalName.complete_museum],
                                       self.logic.museum.can_complete_museum(),
                                       Event.victory)
        elif self.options.goal == Goal.option_full_house:
            self.create_event_location(location_table[GoalName.full_house],
                                       (self.logic.relationship.has_children(2) & self.logic.relationship.can_reproduce()),
                                       Event.victory)
        elif self.options.goal == Goal.option_greatest_walnut_hunter:
            self.create_event_location(location_table[GoalName.greatest_walnut_hunter],
                                       self.logic.has_walnut(130),
                                       Event.victory)
        elif self.options.goal == Goal.option_protector_of_the_valley:
            self.create_event_location(location_table[GoalName.protector_of_the_valley],
                                       self.logic.monster.can_complete_all_monster_slaying_goals(),
                                       Event.victory)
        elif self.options.goal == Goal.option_full_shipment:
            self.create_event_location(location_table[GoalName.full_shipment],
                                       self.logic.shipping.can_ship_everything_in_slot(self.get_all_location_names()),
                                       Event.victory)
        elif self.options.goal == Goal.option_gourmet_chef:
            self.create_event_location(location_table[GoalName.gourmet_chef],
                                       self.logic.cooking.can_cook_everything,
                                       Event.victory)
        elif self.options.goal == Goal.option_craft_master:
            self.create_event_location(location_table[GoalName.craft_master],
                                       self.logic.crafting.can_craft_everything,
                                       Event.victory)
        elif self.options.goal == Goal.option_legend:
            self.create_event_location(location_table[GoalName.legend],
                                       self.logic.money.can_have_earned_total(10_000_000),
                                       Event.victory)
        elif self.options.goal == Goal.option_mystery_of_the_stardrops:
            self.create_event_location(location_table[GoalName.mystery_of_the_stardrops],
                                       self.logic.has_all_stardrops(),
                                       Event.victory)
        elif self.options.goal == Goal.option_allsanity:
            self.create_event_location(location_table[GoalName.allsanity],
                                       HasProgressionPercent(self.player, 100),
                                       Event.victory)
        elif self.options.goal == Goal.option_perfection:
            self.create_event_location(location_table[GoalName.perfection],
                                       HasProgressionPercent(self.player, 100),
                                       Event.victory)

        self.multiworld.completion_condition[self.player] = lambda state: state.has(Event.victory, self.player)

    def get_all_location_names(self) -> List[str]:
        return list(location.name for location in self.multiworld.get_locations(self.player))

    def create_item(self, item: Union[str, ItemData], override_classification: ItemClassification = None) -> StardewItem:
        if isinstance(item, str):
            item = item_table[item]

        if override_classification is None:
            override_classification = item.classification

        if override_classification == ItemClassification.progression and item.name != Event.victory:
            self.total_progression_items += 1
            # if item.name not in self.all_progression_items:
            #     self.all_progression_items[item.name] = 0
            # self.all_progression_items[item.name] += 1
        return StardewItem(item.name, override_classification, item.code, self.player)

    def delete_item(self, item: Item):
        if item.classification & ItemClassification.progression:
            self.total_progression_items -= 1
            # if item.name in self.all_progression_items:
            #     self.all_progression_items[item.name] -= 1

    def create_starting_item(self, item: Union[str, ItemData]) -> StardewItem:
        if isinstance(item, str):
            item = item_table[item]

        return StardewItem(item.name, item.classification, item.code, self.player)

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
        pass

    def get_filler_item_name(self) -> str:
        if not self.filler_item_pool_names:
            self.generate_filler_item_pool_names()
        return self.random.choice(self.filler_item_pool_names)

    def generate_filler_item_pool_names(self):
        include_traps, exclude_island = self.get_filler_item_rules()
        available_filler = get_all_filler_items(include_traps, exclude_island)
        available_filler = remove_limited_amount_packs(available_filler)
        self.filler_item_pool_names = [item.name for item in available_filler]

    def get_filler_item_rules(self):
        if self.player in self.multiworld.groups:
            link_group = self.multiworld.groups[self.player]
            include_traps = True
            exclude_island = False
            for player in link_group["players"]:
                player_options = self.multiworld.worlds[player].options
                if self.multiworld.game[player] != self.game:
                    continue
                if player_options.trap_items == TrapItems.option_no_traps:
                    include_traps = False
                if player_options.exclude_ginger_island == ExcludeGingerIsland.option_true:
                    exclude_island = True
            return include_traps, exclude_island
        else:
            return self.options.trap_items != TrapItems.option_no_traps, self.options.exclude_ginger_island == ExcludeGingerIsland.option_true

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler header. If individual it's right at the end of that player's options,
        if as stage it's right under the common header before per-player options."""
        self.add_entrances_to_spoiler_log()

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        """Write to the spoiler "middle", this is after the per-player options and before locations,
        meant for useful or interesting info."""
        self.add_bundles_to_spoiler_log(spoiler_handle)

    def add_bundles_to_spoiler_log(self, spoiler_handle: TextIO):
        if self.options.bundle_randomization == BundleRandomization.option_vanilla:
            return
        player_name = self.multiworld.get_player_name(self.player)
        spoiler_handle.write(f"\n\nCommunity Center ({player_name}):\n")
        for room in self.modified_bundles:
            for bundle in room.bundles:
                spoiler_handle.write(f"\t[{room.name}] {bundle.name} ({bundle.number_required} required):\n")
                for i, item in enumerate(bundle.items):
                    if "Basic" in item.quality:
                        quality = ""
                    else:
                        quality = f" ({item.quality.split(' ')[0]})"
                    spoiler_handle.write(f"\t\t{item.amount}x {item.item_name}{quality}\n")

    def add_entrances_to_spoiler_log(self):
        if self.options.entrance_randomization == EntranceRandomization.option_disabled:
            return
        for original_entrance, replaced_entrance in self.randomized_entrances.items():
            self.multiworld.spoiler.set_entrance(original_entrance, replaced_entrance, "entrance", self.player)

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
        })

        return slot_data
