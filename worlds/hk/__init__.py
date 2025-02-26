from __future__ import annotations

import logging
import typing
from copy import deepcopy
import itertools
import operator
from collections import defaultdict, Counter

from .Items import item_table, item_name_groups
from .Rules import set_rules, cost_terms, _hk_can_beat_thk, _hk_siblings_ending, _hk_can_beat_radiance
from .Options import hollow_knight_options, hollow_knight_randomize_options, Goal, WhitePalace, CostSanity, \
    shop_to_option, HKOptions, GrubHuntGoal
from .ExtractedData import locations, starts, multi_locations, event_names, item_effects, connectors, \
    vanilla_shop_costs, vanilla_location_costs
from .Charms import names as charm_names

from BaseClasses import Region, Location, MultiWorld, Item, LocationProgressType, Tutorial, ItemClassification, \
    CollectionState
from worlds.AutoWorld import World, LogicMixin, WebWorld

from settings import Group, Bool

logger = logging.getLogger("Hollow Knight")


class HollowKnightSettings(Group):
    class DisableMapModSpoilers(Bool):
        """Disallows the APMapMod from showing spoiler placements."""

    disable_spoilers: typing.Union[DisableMapModSpoilers, bool] = False


path_of_pain_locations = {
    "Soul_Totem-Path_of_Pain_Below_Thornskip",
    "Lore_Tablet-Path_of_Pain_Entrance",
    "Soul_Totem-Path_of_Pain_Left_of_Lever",
    "Soul_Totem-Path_of_Pain_Hidden",
    "Soul_Totem-Path_of_Pain_Entrance",
    "Soul_Totem-Path_of_Pain_Final",
    "Soul_Totem-Path_of_Pain_Below_Lever",
    "Soul_Totem-Path_of_Pain_Second",
    "Journal_Entry-Seal_of_Binding",
    "Warp-Path_of_Pain_Complete",
    "Defeated_Path_of_Pain_Arena",
    "Completed_Path_of_Pain",
    # Path of Pain transitions
    "White_Palace_17[right1]", "White_Palace_17[bot1]",
    "White_Palace_18[top1]", "White_Palace_18[right1]",
    "White_Palace_19[left1]", "White_Palace_19[top1]",
    "White_Palace_20[bot1]",
}

white_palace_transitions = {
    # Event-Transitions:
    # "Grubfather_2",
    "White_Palace_01[left1]", "White_Palace_01[right1]", "White_Palace_01[top1]",
    "White_Palace_02[left1]",
    "White_Palace_03_hub[bot1]", "White_Palace_03_hub[left1]", "White_Palace_03_hub[left2]",
    "White_Palace_03_hub[right1]", "White_Palace_03_hub[top1]",
    "White_Palace_04[right2]", "White_Palace_04[top1]",
    "White_Palace_05[left1]", "White_Palace_05[left2]", "White_Palace_05[right1]", "White_Palace_05[right2]",
    "White_Palace_06[bot1]", "White_Palace_06[left1]", "White_Palace_06[top1]", "White_Palace_07[bot1]",
    "White_Palace_07[top1]", "White_Palace_08[left1]", "White_Palace_08[right1]",
    "White_Palace_09[right1]",
    "White_Palace_11[door2]",
    "White_Palace_12[bot1]", "White_Palace_12[right1]",
    "White_Palace_13[left1]", "White_Palace_13[left2]", "White_Palace_13[left3]", "White_Palace_13[right1]",
    "White_Palace_14[bot1]", "White_Palace_14[right1]",
    "White_Palace_15[left1]", "White_Palace_15[right1]", "White_Palace_15[right2]",
    "White_Palace_16[left1]", "White_Palace_16[left2]",
}

white_palace_checks = {
    "Soul_Totem-White_Palace_Final",
    "Soul_Totem-White_Palace_Entrance",
    "Lore_Tablet-Palace_Throne",
    "Soul_Totem-White_Palace_Left",
    "Lore_Tablet-Palace_Workshop",
    "Soul_Totem-White_Palace_Hub",
    "Soul_Totem-White_Palace_Right"
}

white_palace_events = {
    "White_Palace_03_hub",
    "White_Palace_13",
    "White_Palace_01",
    "Palace_Entrance_Lantern_Lit",
    "Palace_Left_Lantern_Lit",
    "Palace_Right_Lantern_Lit",
    "Palace_Atrium_Gates_Opened",
    "Warp-White_Palace_Atrium_to_Palace_Grounds",
    "Warp-White_Palace_Entrance_to_Palace_Grounds",
}

progression_charms = {
    # Baldur Killers
    "Grubberfly's_Elegy", "Weaversong", "Glowing_Womb",
    # Spore Shroom spots in fungal wastes and elsewhere
    "Spore_Shroom",
    # Tuk gives egg,
    "Defender's_Crest",
    # Unlocks Grimm Troupe
    "Grimmchild1", "Grimmchild2"
}

# Vanilla placements of the following items have no impact on logic, thus we can avoid creating these items and
# locations entirely when the option to randomize them is disabled.
logicless_options = {
    "RandomizeVesselFragments", "RandomizeGeoChests", "RandomizeJunkPitChests", "RandomizeRelics",
    "RandomizeMaps", "RandomizeJournalEntries", "RandomizeGeoRocks", "RandomizeBossGeo",
    "RandomizeLoreTablets", "RandomizeSoulTotems",
}

# Options that affect vanilla starting items
randomizable_starting_items: typing.Dict[str, typing.Tuple[str, ...]] = {
    "RandomizeFocus": ("Focus",),
    "RandomizeSwim": ("Swim",),
    "RandomizeNail": ('Upslash', 'Leftslash', 'Rightslash')
}

# Shop cost types.
shop_cost_types: typing.Dict[str, typing.Tuple[str, ...]] = {
    "Egg_Shop": ("RANCIDEGGS",),
    "Grubfather": ("GRUBS",),
    "Seer": ("ESSENCE",),
    "Salubra_(Requires_Charms)": ("CHARMS", "GEO"),
    "Sly": ("GEO",),
    "Sly_(Key)": ("GEO",),
    "Iselda": ("GEO",),
    "Salubra": ("GEO",),
    "Leg_Eater": ("GEO",),
}


class HKWeb(WebWorld):
    rich_text_options_doc = True

    setup_en = Tutorial(
        "Mod Setup and Use Guide",
        "A guide to playing Hollow Knight with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ijwu"]
    )

    setup_pt_br = Tutorial(
        setup_en.tutorial_name,
        setup_en.description,
        "Português Brasileiro",
        "setup_pt_br.md",
        "setup/pt_br",
        ["JoaoVictor-FA"]
    )

    tutorials = [setup_en, setup_pt_br]

    bug_report_page = "https://github.com/Ijwu/Archipelago.HollowKnight/issues/new?assignees=&labels=bug%2C+needs+investigation&template=bug_report.md&title="


class HKWorld(World):
    """Beneath the fading town of Dirtmouth sleeps a vast, ancient kingdom. Many are drawn beneath the surface,
    searching for riches, or glory, or answers to old secrets.

    As the enigmatic Knight, you’ll traverse the depths, unravel its mysteries and conquer its evils.
    """  # from https://www.hollowknight.com
    game: str = "Hollow Knight"
    options_dataclass = HKOptions
    options: HKOptions
    settings: typing.ClassVar[HollowKnightSettings]

    web = HKWeb()

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location_name: location_id for location_id, location_name in
                           enumerate(locations, start=0x1000000)}
    item_name_groups = item_name_groups

    ranges: typing.Dict[str, typing.Tuple[int, int]]
    charm_costs: typing.List[int]
    cached_filler_items = {}
    grub_count: int
    grub_player_count: typing.Dict[int, int]

    def __init__(self, multiworld, player):
        super(HKWorld, self).__init__(multiworld, player)
        self.created_multi_locations: typing.Dict[str, typing.List[HKLocation]] = {
            location: list() for location in multi_locations
        }
        self.ranges = {}
        self.created_shop_items = 0
        self.vanilla_shop_costs = deepcopy(vanilla_shop_costs)

    def generate_early(self):
        options = self.options
        charm_costs = options.RandomCharmCosts.get_costs(self.random)
        self.charm_costs = options.PlandoCharmCosts.get_costs(charm_costs)
        # options.exclude_locations.value.update(white_palace_locations)
        for term, data in cost_terms.items():
            mini = getattr(options, f"Minimum{data.option}Price")
            maxi = getattr(options, f"Maximum{data.option}Price")
            # if minimum > maximum, set minimum to maximum
            mini.value = min(mini.value, maxi.value)
            self.ranges[term] = mini.value, maxi.value
        self.multiworld.push_precollected(HKItem(starts[options.StartLocation.current_key],
                                          True, None, "Event", self.player))

        # defaulting so completion condition isn't incorrect before pre_fill
        self.grub_count = (
            46 if options.GrubHuntGoal == GrubHuntGoal.special_range_names["all"]
            else options.GrubHuntGoal.value
            )
        self.grub_player_count = {self.player: self.grub_count}

    def white_palace_exclusions(self):
        exclusions = set()
        wp = self.options.WhitePalace
        if wp <= WhitePalace.option_nopathofpain:
            exclusions.update(path_of_pain_locations)
        if wp <= WhitePalace.option_kingfragment:
            exclusions.update(white_palace_checks)
        if wp == WhitePalace.option_exclude:
            exclusions.add("King_Fragment")
            if self.options.RandomizeCharms:
                # If charms are randomized, this will be junk-filled -- so transitions and events are not progression
                exclusions.update(white_palace_transitions)
                exclusions.update(white_palace_events)
        return exclusions

    def create_regions(self):
        menu_region: Region = create_region(self.multiworld, self.player, 'Menu')
        self.multiworld.regions.append(menu_region)

        # check for any goal that godhome events are relevant to
        all_event_names = event_names.copy()
        if self.options.Goal in [Goal.option_godhome, Goal.option_godhome_flower, Goal.option_any]:
            from .GodhomeData import godhome_event_names
            all_event_names.update(set(godhome_event_names))

        # Link regions
        for event_name in sorted(all_event_names):
            loc = HKLocation(self.player, event_name, None, menu_region)
            loc.place_locked_item(HKItem(event_name,
                                         True,
                                         None, "Event", self.player))
            menu_region.locations.append(loc)
        for entry_transition, exit_transition in connectors.items():
            if exit_transition:
                # if door logic fulfilled -> award vanilla target as event
                loc = HKLocation(self.player, entry_transition, None, menu_region)
                loc.place_locked_item(HKItem(exit_transition,
                                             True,
                                             None, "Event", self.player))
                menu_region.locations.append(loc)

    def create_items(self):
        unfilled_locations = 0
        # Generate item pool and associated locations (paired in HK)
        pool: typing.List[HKItem] = []
        wp_exclusions = self.white_palace_exclusions()
        junk_replace: typing.Set[str] = set()
        if self.options.RemoveSpellUpgrades:
            junk_replace.update(("Abyss_Shriek", "Shade_Soul", "Descending_Dark"))

        randomized_starting_items = set()
        for attr, items in randomizable_starting_items.items():
            if getattr(self.options, attr):
                randomized_starting_items.update(items)

        # noinspection PyShadowingNames
        def _add(item_name: str, location_name: str, randomized: bool):
            """
            Adds a pairing of an item and location, doing appropriate checks to see if it should be vanilla or not.
            """
            nonlocal unfilled_locations

            vanilla = not randomized
            excluded = False

            if not vanilla and location_name in wp_exclusions:
                if location_name == 'King_Fragment':
                    excluded = True
                else:
                    vanilla = True

            if item_name in junk_replace:
                item_name = self.get_filler_item_name()

            item = (self.create_item(item_name)
                    if not vanilla or location_name == "Start" or self.options.AddUnshuffledLocations
                    else self.create_event(item_name)
                    )

            if location_name == "Start":
                if item_name in randomized_starting_items:
                    if item_name == "Focus":
                        self.create_location("Focus")
                        unfilled_locations += 1
                    pool.append(item)
                else:
                    self.multiworld.push_precollected(item)
                return

            if vanilla:
                location = self.create_vanilla_location(location_name, item)
            else:
                pool.append(item)
                if location_name in multi_locations:  # Create shop locations later.
                    return
                location = self.create_location(location_name)
                unfilled_locations += 1
            if excluded:
                location.progress_type = LocationProgressType.EXCLUDED

        for option_key, option in hollow_knight_randomize_options.items():
            randomized = getattr(self.options, option_key)
            if all([not randomized, option_key in logicless_options, not self.options.AddUnshuffledLocations]):
                continue
            for item_name, location_name in zip(option.items, option.locations):
                if item_name in junk_replace:
                    item_name = self.get_filler_item_name()

                if (item_name == "Crystal_Heart" and self.options.SplitCrystalHeart) or \
                        (item_name == "Mothwing_Cloak" and self.options.SplitMothwingCloak):
                    _add("Left_" + item_name, location_name, randomized)
                    _add("Right_" + item_name, "Split_" + location_name, randomized)
                    continue
                if item_name == "Mantis_Claw" and self.options.SplitMantisClaw:
                    _add("Left_" + item_name, "Left_" + location_name, randomized)
                    _add("Right_" + item_name, "Right_" + location_name, randomized)
                    continue
                if item_name == "Shade_Cloak" and self.options.SplitMothwingCloak:
                    if self.random.randint(0, 1):
                        item_name = "Left_Mothwing_Cloak"
                    else:
                        item_name = "Right_Mothwing_Cloak"
                if item_name == "Grimmchild2" and self.options.RandomizeGrimmkinFlames and self.options.RandomizeCharms:
                    _add("Grimmchild1", location_name, randomized)
                    continue

                _add(item_name, location_name, randomized)

        if self.options.RandomizeElevatorPass:
            randomized = True
            _add("Elevator_Pass", "Elevator_Pass", randomized)

        for shop, shop_locations in self.created_multi_locations.items():
            for _ in range(len(shop_locations), getattr(self.options, shop_to_option[shop]).value):
                self.create_location(shop)
                unfilled_locations += 1

        # Balance the pool
        item_count = len(pool)
        additional_shop_items = max(item_count - unfilled_locations, self.options.ExtraShopSlots.value)

        # Add additional shop items, as needed.
        if additional_shop_items > 0:
            shops = [shop for shop, shop_locations in self.created_multi_locations.items() if len(shop_locations) < 16]
            if not self.options.EggShopSlots:  # No eggshop, so don't place items there
                shops.remove('Egg_Shop')

            if shops:
                for _ in range(additional_shop_items):
                    shop = self.random.choice(shops)
                    self.create_location(shop)
                    unfilled_locations += 1
                    if len(self.created_multi_locations[shop]) >= 16:
                        shops.remove(shop)
                        if not shops:
                            break

        # Create filler items, if needed
        if item_count < unfilled_locations:
            pool.extend(self.create_item(self.get_filler_item_name()) for _ in range(unfilled_locations - item_count))
        self.multiworld.itempool += pool
        self.apply_costsanity()
        self.sort_shops_by_cost()

    def sort_shops_by_cost(self):
        for shop, shop_locations in self.created_multi_locations.items():
            randomized_locations = [loc for loc in shop_locations if not loc.vanilla]
            prices = sorted(
                (loc.costs for loc in randomized_locations),
                key=lambda costs: (len(costs),) + tuple(costs.values())
            )
            for loc, costs in zip(randomized_locations, prices):
                loc.costs = costs

    def apply_costsanity(self):
        setting = self.options.CostSanity.value
        if not setting:
            return  # noop

        def _compute_weights(weights: dict, desc: str) -> typing.Dict[str, int]:
            if all(x == 0 for x in weights.values()):
                logger.warning(
                    f"All {desc} weights were zero for {self.multiworld.player_name[self.player]}."
                    f" Setting them to one instead."
                )
                weights = {k: 1 for k in weights}

            return {k: v for k, v in weights.items() if v}

        random = self.random
        hybrid_chance = getattr(self.options, "CostSanityHybridChance").value
        weights = {
            data.term: getattr(self.options, f"CostSanity{data.option}Weight").value
            for data in cost_terms.values()
        }
        weights_geoless = dict(weights)
        del weights_geoless["GEO"]

        weights = _compute_weights(weights, "CostSanity")
        weights_geoless = _compute_weights(weights_geoless, "Geoless CostSanity")

        if hybrid_chance > 0:
            if len(weights) == 1:
                logger.warning(
                    f"Only one cost type is available for CostSanity in {self.multiworld.player_name[self.player]}'s world."
                    f" CostSanityHybridChance will not trigger."
                )
            if len(weights_geoless) == 1:
                logger.warning(
                    f"Only one cost type is available for CostSanity in {self.multiworld.player_name[self.player]}'s world."
                    f" CostSanityHybridChance will not trigger in geoless locations."
                )

        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                if location.vanilla:
                    continue
                if not location.costs:
                    continue
                if location.name == "Vessel_Fragment-Basin":
                    continue
                if setting == CostSanity.option_notshops and location.basename in multi_locations:
                    continue
                if setting == CostSanity.option_shopsonly and location.basename not in multi_locations:
                    continue
                if location.basename in {'Grubfather', 'Seer', 'Egg_Shop'}:
                    our_weights = dict(weights_geoless)
                else:
                    our_weights = dict(weights)

                rolls = 1
                if random.randrange(100) < hybrid_chance:
                    rolls = 2

                if rolls > len(our_weights):
                    terms = list(our_weights.keys())  # Can't randomly choose cost types, using all of them.
                else:
                    terms = []
                    for _ in range(rolls):
                        term = random.choices(list(our_weights.keys()), list(our_weights.values()))[0]
                        del our_weights[term]
                        terms.append(term)

                location.costs = {term: random.randint(*self.ranges[term]) for term in terms}
                location.sort_costs()

    def set_rules(self):
        multiworld = self.multiworld
        player = self.player
        goal = self.options.Goal
        if goal == Goal.option_hollowknight:
            multiworld.completion_condition[player] = lambda state: _hk_can_beat_thk(state, player)
        elif goal == Goal.option_siblings:
            multiworld.completion_condition[player] = lambda state: _hk_siblings_ending(state, player)
        elif goal == Goal.option_radiance:
            multiworld.completion_condition[player] = lambda state: _hk_can_beat_radiance(state, player)
        elif goal == Goal.option_godhome:
            multiworld.completion_condition[player] = lambda state: state.count("Defeated_Pantheon_5", player)
        elif goal == Goal.option_godhome_flower:
            multiworld.completion_condition[player] = lambda state: state.count("Godhome_Flower_Quest", player)
        elif goal == Goal.option_grub_hunt:
            multiworld.completion_condition[player] = lambda state: self.can_grub_goal(state)
        else:
            # Any goal
            multiworld.completion_condition[player] = lambda state: _hk_siblings_ending(state, player) and \
                _hk_can_beat_radiance(state, player) and state.count("Godhome_Flower_Quest", player) and \
                self.can_grub_goal(state)

        set_rules(self)

    def can_grub_goal(self, state: CollectionState) -> bool:
        return all(state.has("Grub", owner, count) for owner, count in self.grub_player_count.items())

    @classmethod
    def stage_pre_fill(cls, multiworld: "MultiWorld"):
        worlds = [world for world in multiworld.get_game_worlds(cls.game) if world.options.Goal in ["any", "grub_hunt"]]
        if worlds:
            grubs = [item for item in multiworld.get_items() if item.name == "Grub"]
        all_grub_players = [
            world.player
            for world in worlds
            if world.options.GrubHuntGoal == GrubHuntGoal.special_range_names["all"]
            ]

        if all_grub_players:
            group_lookup = defaultdict(set)
            for group_id, group in multiworld.groups.items():
                for player in group["players"]:
                    group_lookup[group_id].add(player)

            grub_count_per_player = Counter()
            per_player_grubs_per_player = defaultdict(Counter)

            for grub in grubs:
                player = grub.player
                if player in group_lookup:
                    for real_player in group_lookup[player]:
                        per_player_grubs_per_player[real_player][player] += 1
                else:
                    per_player_grubs_per_player[player][player] += 1

                if grub.location and grub.location.player in group_lookup.keys():
                    # will count the item linked grub instead
                    pass
                elif player in group_lookup:
                    for real_player in group_lookup[player]:
                        grub_count_per_player[real_player] += 1
                else:
                    # for non-linked grubs
                    grub_count_per_player[player] += 1

            for player, count in grub_count_per_player.items():
                multiworld.worlds[player].grub_count = count

            for player, grub_player_count in per_player_grubs_per_player.items():
                if player in all_grub_players:
                    multiworld.worlds[player].grub_player_count = grub_player_count

        for world in worlds:
            if world.player not in all_grub_players:
                world.grub_count = world.options.GrubHuntGoal.value
                player = world.player
                world.grub_player_count = {player: world.grub_count}

    def fill_slot_data(self):
        slot_data = {}

        options = slot_data["options"] = {}
        for option_name in hollow_knight_options:
            option = getattr(self.options, option_name)
            try:
                # exclude more complex types - we only care about int, bool, enum for player options; the client
                # can get them back to the necessary type.
                optionvalue = int(option.value)
                options[option_name] = optionvalue
            except TypeError:
                pass

        # 32 bit int
        slot_data["seed"] = self.random.randint(-2147483647, 2147483646)

        # HKAP 0.1.0 and later cost data.
        location_costs = {}
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                if location.costs:
                    location_costs[location.name] = location.costs
        slot_data["location_costs"] = location_costs

        slot_data["notch_costs"] = self.charm_costs

        slot_data["grub_count"] = self.grub_count

        slot_data["is_race"] = self.settings.disable_spoilers or self.multiworld.is_race

        return slot_data

    def create_item(self, name: str) -> HKItem:
        item_data = item_table[name]
        return HKItem(name, item_data.advancement, item_data.id, item_data.type, self.player)

    def create_event(self, name: str) -> HKItem:
        item_data = item_table[name]
        return HKItem(name, item_data.advancement, None, item_data.type, self.player)

    def create_location(self, name: str, vanilla=False) -> HKLocation:
        costs = None
        basename = name
        if name in shop_cost_types:
            costs = {
                term: self.random.randint(*self.ranges[term])
                for term in shop_cost_types[name]
            }
        elif name in vanilla_location_costs:
            costs = vanilla_location_costs[name]

        multi = self.created_multi_locations.get(name)

        if multi is not None:
            i = len(multi) + 1
            name = f"{name}_{i}"

        region = self.multiworld.get_region("Menu", self.player)

        if vanilla and not self.options.AddUnshuffledLocations:
            loc = HKLocation(self.player, name,
                             None, region, costs=costs, vanilla=vanilla,
                             basename=basename)
        else:
            loc = HKLocation(self.player, name,
                             self.location_name_to_id[name], region, costs=costs, vanilla=vanilla,
                             basename=basename)

        if multi is not None:
            multi.append(loc)

        region.locations.append(loc)
        return loc

    def create_vanilla_location(self, location: str, item: Item):
        costs = self.vanilla_shop_costs.get((location, item.name))
        location = self.create_location(location, vanilla=True)
        location.place_locked_item(item)
        if costs:
            location.costs = costs.pop()
        return location

    def collect(self, state, item: HKItem) -> bool:
        change = super(HKWorld, self).collect(state, item)
        if change:
            for effect_name, effect_value in item_effects.get(item.name, {}).items():
                state.prog_items[item.player][effect_name] += effect_value
            if item.name in {"Left_Mothwing_Cloak", "Right_Mothwing_Cloak"}:
                if state.prog_items[item.player].get('RIGHTDASH', 0) and \
                        state.prog_items[item.player].get('LEFTDASH', 0):
                    (state.prog_items[item.player]["RIGHTDASH"], state.prog_items[item.player]["LEFTDASH"]) = \
                        ([max(state.prog_items[item.player]["RIGHTDASH"], state.prog_items[item.player]["LEFTDASH"])] * 2)
        return change

    def remove(self, state, item: HKItem) -> bool:
        change = super(HKWorld, self).remove(state, item)

        if change:
            for effect_name, effect_value in item_effects.get(item.name, {}).items():
                if state.prog_items[item.player][effect_name] == effect_value:
                    del state.prog_items[item.player][effect_name]
                else:
                    state.prog_items[item.player][effect_name] -= effect_value

        return change

    @classmethod
    def stage_write_spoiler(cls, multiworld: MultiWorld, spoiler_handle):
        hk_players = multiworld.get_game_players(cls.game)
        spoiler_handle.write('\n\nCharm Notches:')
        for player in hk_players:
            name = multiworld.get_player_name(player)
            spoiler_handle.write(f'\n{name}\n')
            hk_world: HKWorld = multiworld.worlds[player]
            for charm_number, cost in enumerate(hk_world.charm_costs):
                spoiler_handle.write(f"\n{charm_names[charm_number]}: {cost}")

        spoiler_handle.write('\n\nShop Prices:')
        for player in hk_players:
            name = multiworld.get_player_name(player)
            spoiler_handle.write(f'\n{name}\n')
            hk_world: HKWorld = multiworld.worlds[player]

            if hk_world.options.CostSanity:
                for loc in sorted(
                    (
                        loc for loc in itertools.chain(*(region.locations for region in multiworld.get_regions(player)))
                        if loc.costs
                    ), key=operator.attrgetter('name')
                ):
                    spoiler_handle.write(f"\n{loc}: {loc.item} costing {loc.cost_text()}")
            else:
                for shop_name, shop_locations in hk_world.created_multi_locations.items():
                    for loc in shop_locations:
                        spoiler_handle.write(f"\n{loc}: {loc.item} costing {loc.cost_text()}")

    def get_multi_location_name(self, base: str, i: typing.Optional[int]) -> str:
        if i is None:
            i = len(self.created_multi_locations[base]) + 1
        assert 1 <= 16, "limited number of multi location IDs reserved."
        return f"{base}_{i}"

    def get_filler_item_name(self) -> str:
        if self.player not in self.cached_filler_items:
            fillers = ["One_Geo", "Soul_Refill"]
            exclusions = self.white_palace_exclusions()
            for group in (
                    'RandomizeGeoRocks', 'RandomizeSoulTotems', 'RandomizeLoreTablets', 'RandomizeJunkPitChests',
                    'RandomizeRancidEggs'
            ):
                if getattr(self.options, group):
                    fillers.extend(item for item in hollow_knight_randomize_options[group].items if item not in
                                   exclusions)
            self.cached_filler_items[self.player] = fillers
        return self.random.choice(self.cached_filler_items[self.player])


def create_region(multiworld: MultiWorld, player: int, name: str, location_names=None) -> Region:
    ret = Region(name, player, multiworld)
    if location_names:
        for location in location_names:
            loc_id = HKWorld.location_name_to_id.get(location, None)
            location = HKLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    return ret


class HKLocation(Location):
    game: str = "Hollow Knight"
    costs: typing.Dict[str, int] = None
    unit: typing.Optional[str] = None
    vanilla = False
    basename: str

    def sort_costs(self):
        if self.costs is None:
            return
        self.costs = {k: self.costs[k] for k in sorted(self.costs.keys(), key=lambda x: cost_terms[x].sort)}

    def __init__(
            self, player: int, name: str, code=None, parent=None,
            costs: typing.Dict[str, int] = None, vanilla: bool = False, basename: str = None
    ):
        self.basename = basename or name
        super(HKLocation, self).__init__(player, name, code if code else None, parent)
        self.vanilla = vanilla
        if costs:
            self.costs = dict(costs)
            self.sort_costs()

    def cost_text(self, separator=" and "):
        if self.costs is None:
            return None
        return separator.join(
            f"{value} {cost_terms[term].singular if value == 1 else cost_terms[term].plural}"
            for term, value in self.costs.items()
        )


class HKItem(Item):
    game = "Hollow Knight"
    type: str

    def __init__(self, name, advancement, code, type: str, player: int = None):
        if name == "Mimic_Grub":
            classification = ItemClassification.trap
        elif name == "Godtuner":
            classification = ItemClassification.progression
        elif type in ("Grub", "DreamWarrior", "Root", "Egg", "Dreamer"):
            classification = ItemClassification.progression_skip_balancing
        elif type == "Charm" and name not in progression_charms:
            classification = ItemClassification.progression_skip_balancing
        elif type in ("Map", "Journal"):
            classification = ItemClassification.filler
        elif type in ("Ore", "Vessel"):
            classification = ItemClassification.useful
        elif advancement:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
        super(HKItem, self).__init__(name, classification, code if code else None, player)
        self.type = type


class HKLogicMixin(LogicMixin):
    multiworld: MultiWorld

    def _hk_notches(self, player: int, *notches: int) -> int:
        return sum(self.multiworld.worlds[player].charm_costs[notch] for notch in notches)

    def _hk_option(self, player: int, option_name: str) -> int:
        return getattr(self.multiworld.worlds[player].options, option_name).value

    def _hk_start(self, player, start_location: str) -> bool:
        return self.multiworld.worlds[player].options.StartLocation == start_location
