import logging
from random import Random
from typing import Dict, Any, Iterable, Optional, Union, List, TextIO

from BaseClasses import Region, Entrance, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from Options import PerGameCommonOptions, Accessibility
from worlds.AutoWorld import World, WebWorld
from . import rules
from .bundles.bundle_room import BundleRoom
from .bundles.bundles import get_all_bundles
from .content import content_packs, StardewContent, unpack_content, create_content
from .early_items import setup_early_items
from .items import item_table, create_items, ItemData, Group, items_by_group, get_all_filler_items, remove_limited_amount_packs
from .locations import location_table, create_locations, LocationData, locations_by_tag
from .logic.bundle_logic import BundleLogic
from .logic.logic import StardewLogic
from .logic.time_logic import MAX_MONTHS
from .option_groups import sv_option_groups
from .options import StardewValleyOptions, SeasonRandomization, Goal, BundleRandomization, BundlePrice, EnabledFillerBuffs, NumberOfMovementBuffs, \
    BackpackProgression, BuildingProgression, ExcludeGingerIsland, TrapItems, EntranceRandomization, FarmType, Walnutsanity
from .presets import sv_options_presets
from .regions import create_regions
from .rules import set_rules
from .stardew_rule import True_, StardewRule, HasProgressionPercent, true_
from .strings.ap_names.event_names import Event
from .strings.entrance_names import Entrance as EntranceName
from .strings.goal_names import Goal as GoalName
from .strings.metal_names import Ore
from .strings.region_names import Region as RegionName, LogicRegion

logger = logging.getLogger(__name__)

STARDEW_VALLEY = "Stardew Valley"
UNIVERSAL_TRACKER_SEED_PROPERTY = "ut_seed"

client_version = 0


class StardewLocation(Location):
    game: str = STARDEW_VALLEY


class StardewItem(Item):
    game: str = STARDEW_VALLEY


class StardewWebWorld(WebWorld):
    theme = "dirt"
    bug_report_page = "https://github.com/agilbert1412/StardewArchipelago/issues/new?labels=bug&title=%5BBug%5D%3A+Brief+Description+of+bug+here"
    options_presets = sv_options_presets
    option_groups = sv_option_groups

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
    game = STARDEW_VALLEY
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

    required_client_version = (0, 4, 0)

    options_dataclass = StardewValleyOptions
    options: StardewValleyOptions
    content: StardewContent
    logic: StardewLogic

    web = StardewWebWorld()
    modified_bundles: List[BundleRoom]
    randomized_entrances: Dict[str, str]

    total_progression_items: int
    excluded_from_total_progression_items: List[str] = [Event.received_walnuts]

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.filler_item_pool_names = []
        self.total_progression_items = 0

        # Taking the seed specified in slot data for UT, otherwise just generating the seed.
        self.seed = getattr(multiworld, "re_gen_passthrough", {}).get(STARDEW_VALLEY, self.random.getrandbits(64))
        self.random = Random(self.seed)

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Optional[int]:
        # If the seed is not specified in the slot data, this mean the world was generated before Universal Tracker support.
        seed = slot_data.get(UNIVERSAL_TRACKER_SEED_PROPERTY)
        if seed is None:
            logger.warning(f"World was generated before Universal Tracker support. Tracker might not be accurate.")
        return seed

    def generate_early(self):
        self.force_change_options_if_incompatible()
        self.content = create_content(self.options)

    def force_change_options_if_incompatible(self):
        goal_is_walnut_hunter = self.options.goal == Goal.option_greatest_walnut_hunter
        goal_is_perfection = self.options.goal == Goal.option_perfection
        goal_is_island_related = goal_is_walnut_hunter or goal_is_perfection
        exclude_ginger_island = self.options.exclude_ginger_island == ExcludeGingerIsland.option_true

        if goal_is_island_related and exclude_ginger_island:
            self.options.exclude_ginger_island.value = ExcludeGingerIsland.option_false
            goal_name = self.options.goal.current_key
            logger.warning(
                f"Goal '{goal_name}' requires Ginger Island. Exclude Ginger Island setting forced to 'False' for player {self.player} ({self.player_name})")

        if exclude_ginger_island and self.options.walnutsanity != Walnutsanity.preset_none:
            self.options.walnutsanity.value = Walnutsanity.preset_none
            logger.warning(
                f"Walnutsanity requires Ginger Island. Ginger Island was excluded from {self.player} ({self.player_name})'s world, so walnutsanity was force disabled")

        if goal_is_perfection and self.options.accessibility == Accessibility.option_minimal:
            self.options.accessibility.value = Accessibility.option_full
            logger.warning(
                f"Goal 'Perfection' requires full accessibility. Accessibility setting forced to 'Full' for player {self.player} ({self.player_name})")

        elif self.options.goal == Goal.option_allsanity and self.options.accessibility == Accessibility.option_minimal:
            self.options.accessibility.value = Accessibility.option_full
            logger.warning(
                f"Goal 'Allsanity' requires full accessibility. Accessibility setting forced to 'Full' for player {self.player} ({self.player_name})")

    def create_regions(self):
        def create_region(name: str, exits: Iterable[str]) -> Region:
            region = Region(name, self.player, self.multiworld)
            region.exits = [Entrance(self.player, exit_name, region) for exit_name in exits]
            return region

        world_regions, world_entrances, self.randomized_entrances = create_regions(create_region, self.random, self.options, self.content)

        self.logic = StardewLogic(self.player, self.options, self.content, world_regions.keys())
        self.modified_bundles = get_all_bundles(self.random,
                                                self.logic,
                                                self.content,
                                                self.options)

        def add_location(name: str, code: Optional[int], region: str):
            region = world_regions[region]
            location = StardewLocation(self.player, name, code, region)
            region.locations.append(location)

        create_locations(add_location, self.modified_bundles, self.options, self.content, self.random)
        self.multiworld.regions.extend(world_regions.values())

    def create_items(self):
        self.precollect_starting_season()
        self.precollect_farm_type_items()
        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]
                            if not item_table[excluded_items.name].has_any_group(Group.RESOURCE_PACK,
                                                                                 Group.FRIENDSHIP_PACK)]

        if self.options.season_randomization == SeasonRandomization.option_disabled:
            items_to_exclude = [item for item in items_to_exclude
                                if item_table[item.name] not in items_by_group[Group.SEASON]]

        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if location.address is not None])

        created_items = create_items(self.create_item, locations_count, items_to_exclude, self.options, self.content, self.random)

        self.multiworld.itempool += created_items

        setup_early_items(self.multiworld, self.options, self.content, self.player, self.random)
        self.setup_player_events()
        self.setup_victory()

        # This is really a best-effort to get the total progression items count. It is mostly used to spread grinds across spheres are push back locations that
        # only become available after months or years in game. In most cases, not having the exact count will not impact the logic.
        #
        # The actual total can be impacted by the start_inventory_from_pool, when items are removed from the pool but not from the total. The is also a bug
        # with plando where additional progression items can be created without being accounted for, which impact the real amount of progression items. This can
        # ultimately create unwinnable seeds where some items (like Blueberry seeds) are locked in Shipsanity: Blueberry, but world is deemed winnable as the
        # winning rule only check the count of collected progression items.
        self.total_progression_items += sum(1 for i in self.multiworld.precollected_items[self.player] if i.advancement)
        self.total_progression_items += sum(1 for i in self.multiworld.get_filled_locations(self.player) if i.advancement)
        self.total_progression_items += sum(1 for i in created_items if i.advancement)
        self.total_progression_items -= 1  # -1 for the victory event

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

    def precollect_farm_type_items(self):
        if self.options.farm_type == FarmType.option_meadowlands and self.options.building_progression & BuildingProgression.option_progressive:
            self.multiworld.push_precollected(self.create_starting_item("Progressive Coop"))

    def setup_player_events(self):
        self.setup_action_events()
        self.setup_logic_events()

    def setup_action_events(self):
        spring_farming = LocationData(None, LogicRegion.spring_farming, Event.spring_farming)
        self.create_event_location(spring_farming, true_, Event.spring_farming)
        summer_farming = LocationData(None, LogicRegion.summer_farming, Event.summer_farming)
        self.create_event_location(summer_farming, true_, Event.summer_farming)
        fall_farming = LocationData(None, LogicRegion.fall_farming, Event.fall_farming)
        self.create_event_location(fall_farming, true_, Event.fall_farming)
        winter_farming = LocationData(None, LogicRegion.winter_farming, Event.winter_farming)
        self.create_event_location(winter_farming, true_, Event.winter_farming)

    def setup_logic_events(self):
        def register_event(name: str, region: str, rule: StardewRule):
            event_location = LocationData(None, region, name)
            self.create_event_location(event_location, rule, name)

        self.logic.setup_events(register_event)

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
                                       self.logic.fishing.can_catch_every_fish_for_fishsanity(),
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
                                       self.logic.walnut.has_walnut(130),
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

        return StardewItem(item.name, override_classification, item.code, self.player)

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
        location.place_locked_item(StardewItem(item, ItemClassification.progression, None, self.player))

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
                    spoiler_handle.write(f"\t\t{item.amount}x {item.get_item()}{quality}\n")

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
                    bundles[room.name][bundle.name][i] = f"{item.get_item()}|{item.amount}|{item.quality}"

        excluded_options = [BundleRandomization, NumberOfMovementBuffs, EnabledFillerBuffs]
        excluded_option_names = [option.internal_name for option in excluded_options]
        generic_option_names = [option_name for option_name in PerGameCommonOptions.type_hints]
        excluded_option_names.extend(generic_option_names)
        included_option_names: List[str] = [option_name for option_name in self.options_dataclass.type_hints if option_name not in excluded_option_names]
        slot_data = self.options.as_dict(*included_option_names)
        slot_data.update({
            UNIVERSAL_TRACKER_SEED_PROPERTY: self.seed,
            "seed": self.random.randrange(1000000000),  # Seed should be max 9 digits
            "randomized_entrances": self.randomized_entrances,
            "modified_bundles": bundles,
            "client_version": "6.0.0",
        })

        return slot_data

    def collect(self, state: CollectionState, item: StardewItem) -> bool:
        change = super().collect(state, item)
        if not change:
            return False

        walnut_amount = self.get_walnut_amount(item.name)
        if walnut_amount:
            state.prog_items[self.player][Event.received_walnuts] += walnut_amount

        return True

    def remove(self, state: CollectionState, item: StardewItem) -> bool:
        change = super().remove(state, item)
        if not change:
            return False

        walnut_amount = self.get_walnut_amount(item.name)
        if walnut_amount:
            state.prog_items[self.player][Event.received_walnuts] -= walnut_amount

        return True

    @staticmethod
    def get_walnut_amount(item_name: str) -> int:
        if item_name == "Golden Walnut":
            return 1
        if item_name == "3 Golden Walnuts":
            return 3
        if item_name == "5 Golden Walnuts":
            return 5
        return 0
