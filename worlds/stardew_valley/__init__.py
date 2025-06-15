import logging
import typing
from random import Random
from typing import Dict, Any, Optional, List, TextIO

import entrance_rando
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from Options import PerGameCommonOptions
from worlds.AutoWorld import World, WebWorld
from .bundles.bundle_room import BundleRoom
from .bundles.bundles import get_all_bundles
from .content import StardewContent, create_content
from .early_items import setup_early_items
from .items import item_table, ItemData, Group, items_by_group
from .items.item_creation import create_items, get_all_filler_items, remove_limited_amount_packs, \
    generate_filler_choice_pool
from .locations import location_table, create_locations, LocationData, locations_by_tag
from .logic.logic import StardewLogic
from .options import StardewValleyOptions, SeasonRandomization, Goal, BundleRandomization, EnabledFillerBuffs, \
    NumberOfMovementBuffs, BuildingProgression, EntranceRandomization, FarmType
from .options.forced_options import force_change_options_if_incompatible
from .options.option_groups import sv_option_groups
from .options.presets import sv_options_presets
from .options.worlds_group import apply_most_restrictive_options
from .regions import create_regions, prepare_mod_data
from .rules import set_rules
from .stardew_rule import True_, StardewRule, HasProgressionPercent
from .strings.ap_names.event_names import Event
from .strings.goal_names import Goal as GoalName

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

    @classmethod
    def create_group(cls, multiworld: MultiWorld, new_player_id: int, players: set[int]) -> World:
        world_group = super().create_group(multiworld, new_player_id, players)

        group_options = typing.cast(StardewValleyOptions, world_group.options)
        worlds_options = [typing.cast(StardewValleyOptions, multiworld.worlds[player].options) for player in players]
        apply_most_restrictive_options(group_options, worlds_options)

        return world_group

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
        force_change_options_if_incompatible(self.options, self.player, self.player_name)
        self.content = create_content(self.options)

    def create_regions(self):
        def create_region(name: str) -> Region:
            return Region(name, self.player, self.multiworld)

        world_regions = create_regions(create_region, self.options, self.content)

        self.logic = StardewLogic(self.player, self.options, self.content, world_regions.keys())
        self.modified_bundles = get_all_bundles(self.random, self.logic, self.content, self.options)

        def add_location(name: str, code: Optional[int], region: str):
            region: Region = world_regions[region]
            location = StardewLocation(self.player, name, code, region)
            region.locations.append(location)

        create_locations(add_location, self.modified_bundles, self.options, self.content, self.random)
        self.multiworld.regions.extend(world_regions.values())

    def create_items(self):
        self.precollect_starting_season()
        self.precollect_building_items()
        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]
                            if item_table[excluded_items.name].has_any_group(Group.MAXIMUM_ONE)
                            or not item_table[excluded_items.name].has_any_group(Group.RESOURCE_PACK, Group.FRIENDSHIP_PACK)]

        if self.options.season_randomization == SeasonRandomization.option_disabled:
            items_to_exclude = [item for item in items_to_exclude
                                if item_table[item.name] not in items_by_group[Group.SEASON]]

        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if location.address is not None])

        created_items = create_items(self.create_item, locations_count, items_to_exclude, self.options, self.content, self.random)

        self.multiworld.itempool += created_items

        setup_early_items(self.multiworld, self.options, self.content, self.player, self.random)
        self.setup_logic_events()
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
                self.multiworld.push_precollected(self.create_item(season))
            return

        if [item for item in self.multiworld.precollected_items[self.player]
            if item.name in {season.name for season in items_by_group[Group.SEASON]}]:
            return

        if self.options.season_randomization == SeasonRandomization.option_randomized_not_winter:
            season_pool = [season for season in season_pool if season.name != "Winter"]

        starting_season = self.create_item(self.random.choice(season_pool))
        self.multiworld.push_precollected(starting_season)

    def precollect_building_items(self):
        building_progression = self.content.features.building_progression
        # Not adding items when building are vanilla because the buildings are already placed in the world.
        if not building_progression.is_progressive:
            return

        # starting_buildings is a set, so sort for deterministic order.
        for building in sorted(building_progression.starting_buildings):
            item, quantity = building_progression.to_progressive_item(building)
            for _ in range(quantity):
                self.multiworld.push_precollected(self.create_item(item))

    def setup_logic_events(self):
        def register_event(name: str, region: str, rule: StardewRule):
            event_location = LocationData(None, region, name)
            self.create_event_location(event_location, rule, name)

        self.logic.setup_events(register_event)

    def setup_victory(self):
        if self.options.goal == Goal.option_community_center:
            self.create_event_location(location_table[GoalName.community_center],
                                       self.logic.goal.can_complete_community_center(),
                                       Event.victory)
        elif self.options.goal == Goal.option_grandpa_evaluation:
            self.create_event_location(location_table[GoalName.grandpa_evaluation],
                                       self.logic.goal.can_finish_grandpa_evaluation(),
                                       Event.victory)
        elif self.options.goal == Goal.option_bottom_of_the_mines:
            self.create_event_location(location_table[GoalName.bottom_of_the_mines],
                                       self.logic.goal.can_complete_bottom_of_the_mines(),
                                       Event.victory)
        elif self.options.goal == Goal.option_cryptic_note:
            self.create_event_location(location_table[GoalName.cryptic_note],
                                       self.logic.goal.can_complete_cryptic_note(),
                                       Event.victory)
        elif self.options.goal == Goal.option_master_angler:
            self.create_event_location(location_table[GoalName.master_angler],
                                       self.logic.goal.can_complete_master_angler(),
                                       Event.victory)
        elif self.options.goal == Goal.option_complete_collection:
            self.create_event_location(location_table[GoalName.complete_museum],
                                       self.logic.goal.can_complete_complete_collection(),
                                       Event.victory)
        elif self.options.goal == Goal.option_full_house:
            self.create_event_location(location_table[GoalName.full_house],
                                       self.logic.goal.can_complete_full_house(),
                                       Event.victory)
        elif self.options.goal == Goal.option_greatest_walnut_hunter:
            self.create_event_location(location_table[GoalName.greatest_walnut_hunter],
                                       self.logic.goal.can_complete_greatest_walnut_hunter(),
                                       Event.victory)
        elif self.options.goal == Goal.option_protector_of_the_valley:
            self.create_event_location(location_table[GoalName.protector_of_the_valley],
                                       self.logic.goal.can_complete_protector_of_the_valley(),
                                       Event.victory)
        elif self.options.goal == Goal.option_full_shipment:
            self.create_event_location(location_table[GoalName.full_shipment],
                                       self.logic.goal.can_complete_full_shipment(self.get_all_location_names()),
                                       Event.victory)
        elif self.options.goal == Goal.option_gourmet_chef:
            self.create_event_location(location_table[GoalName.gourmet_chef],
                                       self.logic.goal.can_complete_gourmet_chef(),
                                       Event.victory)
        elif self.options.goal == Goal.option_craft_master:
            self.create_event_location(location_table[GoalName.craft_master],
                                       self.logic.goal.can_complete_craft_master(),
                                       Event.victory)
        elif self.options.goal == Goal.option_legend:
            self.create_event_location(location_table[GoalName.legend],
                                       self.logic.goal.can_complete_legend(),
                                       Event.victory)
        elif self.options.goal == Goal.option_mystery_of_the_stardrops:
            self.create_event_location(location_table[GoalName.mystery_of_the_stardrops],
                                       self.logic.goal.can_complete_mystery_of_the_stardrop(),
                                       Event.victory)
        elif self.options.goal == Goal.option_allsanity:
            self.create_event_location(location_table[GoalName.allsanity],
                                       self.logic.goal.can_complete_allsanity(),
                                       Event.victory)
        elif self.options.goal == Goal.option_perfection:
            self.create_event_location(location_table[GoalName.perfection],
                                       self.logic.goal.can_complete_perfection(),
                                       Event.victory)

        self.multiworld.completion_condition[self.player] = lambda state: state.has(Event.victory, self.player)

    def get_all_location_names(self) -> List[str]:
        return list(location.name for location in self.multiworld.get_locations(self.player))

    def create_item(self, item: str | ItemData, override_classification: ItemClassification = None) -> StardewItem:
        if isinstance(item, str):
            item = item_table[item]

        if override_classification is None:
            override_classification = item.classification

        return StardewItem(item.name, override_classification, item.code, self.player)

    def create_event_location(self, location_data: LocationData, rule: StardewRule, item: str):
        region = self.multiworld.get_region(location_data.region, self.player)
        region.add_event(location_data.name, item, rule, StardewLocation, StardewItem)

    def set_rules(self):
        set_rules(self)

    def connect_entrances(self) -> None:
        no_target_groups = {0: [0]}
        placement = entrance_rando.randomize_entrances(self, coupled=True, target_group_lookup=no_target_groups)
        self.randomized_entrances = prepare_mod_data(placement)

    def generate_basic(self):
        pass

    def get_filler_item_name(self) -> str:
        if not self.filler_item_pool_names:
            self.filler_item_pool_names = generate_filler_choice_pool(self.options)
        return self.random.choice(self.filler_item_pool_names)

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

        player_state = state.prog_items[self.player]

        received_progression_count = player_state[Event.received_progression_item]
        received_progression_count += 1
        if self.total_progression_items:
            # Total progression items is not set until all items are created, but collect will be called during the item creation when an item is precollected.
            # We can't update the percentage if we don't know the total progression items, can't divide by 0.
            player_state[Event.received_progression_percent] = received_progression_count * 100 // self.total_progression_items
        player_state[Event.received_progression_item] = received_progression_count

        walnut_amount = self.get_walnut_amount(item.name)
        if walnut_amount:
            player_state[Event.received_walnuts] += walnut_amount

        return True

    def remove(self, state: CollectionState, item: StardewItem) -> bool:
        change = super().remove(state, item)
        if not change:
            return False

        player_state = state.prog_items[self.player]

        received_progression_count = player_state[Event.received_progression_item]
        received_progression_count -= 1
        if self.total_progression_items:
            # We can't update the percentage if we don't know the total progression items, can't divide by 0.
            player_state[Event.received_progression_percent] = received_progression_count * 100 // self.total_progression_items
        player_state[Event.received_progression_item] = received_progression_count

        walnut_amount = self.get_walnut_amount(item.name)
        if walnut_amount:
            player_state[Event.received_walnuts] -= walnut_amount

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
