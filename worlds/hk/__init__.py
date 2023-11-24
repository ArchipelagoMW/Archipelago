from __future__ import annotations

import logging
import typing
from copy import deepcopy
import itertools
import operator

logger = logging.getLogger("Hollow Knight")

from .Items import item_table, lookup_type_to_names, item_name_groups
from .Regions import create_regions
from .Rules import set_rules, cost_terms
from .Options import hollow_knight_options, hollow_knight_randomize_options, Goal, WhitePalace, CostSanity, \
    shop_to_option
from .ExtractedData import locations, starts, multi_locations, location_to_region_lookup, \
    event_names, item_effects, connectors, one_ways, vanilla_shop_costs, vanilla_location_costs
from .Charms import names as charm_names

from BaseClasses import Region, Location, MultiWorld, Item, LocationProgressType, Tutorial, ItemClassification
from worlds.AutoWorld import World, LogicMixin, WebWorld

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
    tutorials = [Tutorial(
        "Mod Setup and Use Guide",
        "A guide to playing Hollow Knight with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ijwu"]
    )]

    bug_report_page = "https://github.com/Ijwu/Archipelago.HollowKnight/issues/new?assignees=&labels=bug%2C+needs+investigation&template=bug_report.md&title="


class HKWorld(World):
    """Beneath the fading town of Dirtmouth sleeps a vast, ancient kingdom. Many are drawn beneath the surface, 
    searching for riches, or glory, or answers to old secrets.

    As the enigmatic Knight, you’ll traverse the depths, unravel its mysteries and conquer its evils.
    """  # from https://www.hollowknight.com
    game: str = "Hollow Knight"
    option_definitions = hollow_knight_options

    web = HKWeb()

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location_name: location_id for location_id, location_name in
                           enumerate(locations, start=0x1000000)}
    item_name_groups = item_name_groups

    ranges: typing.Dict[str, typing.Tuple[int, int]]
    charm_costs: typing.List[int]
    cached_filler_items = {}
    data_version = 2

    def __init__(self, world, player):
        super(HKWorld, self).__init__(world, player)
        self.created_multi_locations: typing.Dict[str, typing.List[HKLocation]] = {
            location: list() for location in multi_locations
        }
        self.ranges = {}
        self.created_shop_items = 0
        self.vanilla_shop_costs = deepcopy(vanilla_shop_costs)

    def generate_early(self):
        world = self.multiworld
        charm_costs = world.RandomCharmCosts[self.player].get_costs(world.random)
        self.charm_costs = world.PlandoCharmCosts[self.player].get_costs(charm_costs)
        # world.exclude_locations[self.player].value.update(white_palace_locations)
        for term, data in cost_terms.items():
            mini = getattr(world, f"Minimum{data.option}Price")[self.player]
            maxi = getattr(world, f"Maximum{data.option}Price")[self.player]
            # if minimum > maximum, set minimum to maximum
            mini.value = min(mini.value, maxi.value)
            self.ranges[term] = mini.value, maxi.value
        world.push_precollected(HKItem(starts[world.StartLocation[self.player].current_key],
                                       True, None, "Event", self.player))

    def white_palace_exclusions(self):
        exclusions = set()
        wp = self.multiworld.WhitePalace[self.player]
        if wp <= WhitePalace.option_nopathofpain:
            exclusions.update(path_of_pain_locations)
        if wp <= WhitePalace.option_kingfragment:
            exclusions.update(white_palace_checks)
        if wp == WhitePalace.option_exclude:
            exclusions.add("King_Fragment")
            if self.multiworld.RandomizeCharms[self.player]:
                # If charms are randomized, this will be junk-filled -- so transitions and events are not progression
                exclusions.update(white_palace_transitions)
                exclusions.update(white_palace_events)
        return exclusions

    def create_regions(self):
        menu_region: Region = create_region(self.multiworld, self.player, 'Menu')
        self.multiworld.regions.append(menu_region)
        # wp_exclusions = self.white_palace_exclusions()

        # Link regions
        for event_name in event_names:
            #if event_name in wp_exclusions:
            #    continue
            loc = HKLocation(self.player, event_name, None, menu_region)
            loc.place_locked_item(HKItem(event_name,
                                         True, #event_name not in wp_exclusions,
                                         None, "Event", self.player))
            menu_region.locations.append(loc)
        for entry_transition, exit_transition in connectors.items():
            #if entry_transition in wp_exclusions:
            #    continue
            if exit_transition:
                # if door logic fulfilled -> award vanilla target as event
                loc = HKLocation(self.player, entry_transition, None, menu_region)
                loc.place_locked_item(HKItem(exit_transition,
                                             True, #exit_transition not in wp_exclusions,
                                             None, "Event", self.player))
                menu_region.locations.append(loc)

    def create_items(self):
        unfilled_locations = 0
        # Generate item pool and associated locations (paired in HK)
        pool: typing.List[HKItem] = []
        wp_exclusions = self.white_palace_exclusions()
        junk_replace: typing.Set[str] = set()
        if self.multiworld.RemoveSpellUpgrades[self.player]:
            junk_replace.update(("Abyss_Shriek", "Shade_Soul", "Descending_Dark"))

        randomized_starting_items = set()
        for attr, items in randomizable_starting_items.items():
            if getattr(self.multiworld, attr)[self.player]:
                randomized_starting_items.update(items)

        # noinspection PyShadowingNames
        def _add(item_name: str, location_name: str):
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

            item = self.create_item(item_name)

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
            randomized = getattr(self.multiworld, option_key)[self.player]
            for item_name, location_name in zip(option.items, option.locations):
                if item_name in junk_replace:
                    item_name = self.get_filler_item_name()

                if (item_name == "Crystal_Heart" and self.multiworld.SplitCrystalHeart[self.player]) or \
                        (item_name == "Mothwing_Cloak" and self.multiworld.SplitMothwingCloak[self.player]):
                    _add("Left_" + item_name, location_name)
                    _add("Right_" + item_name, "Split_" + location_name)
                    continue
                if item_name == "Mantis_Claw" and self.multiworld.SplitMantisClaw[self.player]:
                    _add("Left_" + item_name, "Left_" + location_name)
                    _add("Right_" + item_name, "Right_" + location_name)
                    continue
                if item_name == "Shade_Cloak" and self.multiworld.SplitMothwingCloak[self.player]:
                    if self.multiworld.random.randint(0, 1):
                        item_name = "Left_Mothwing_Cloak"
                    else:
                        item_name = "Right_Mothwing_Cloak"

                _add(item_name, location_name)

        if self.multiworld.RandomizeElevatorPass[self.player]:
            randomized = True
            _add("Elevator_Pass", "Elevator_Pass")

        for shop, locations in self.created_multi_locations.items():
            for _ in range(len(locations), getattr(self.multiworld, shop_to_option[shop])[self.player].value):
                loc = self.create_location(shop)
                unfilled_locations += 1

        # Balance the pool
        item_count = len(pool)
        additional_shop_items = max(item_count - unfilled_locations, self.multiworld.ExtraShopSlots[self.player].value)

        # Add additional shop items, as needed.
        if additional_shop_items > 0:
            shops = list(shop for shop, locations in self.created_multi_locations.items() if len(locations) < 16)
            if not self.multiworld.EggShopSlots[self.player].value:  # No eggshop, so don't place items there
                shops.remove('Egg_Shop')

            if shops:
                for _ in range(additional_shop_items):
                    shop = self.multiworld.random.choice(shops)
                    loc = self.create_location(shop)
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
        for shop, locations in self.created_multi_locations.items():
            randomized_locations = list(loc for loc in locations if not loc.vanilla)
            prices = sorted(
                (loc.costs for loc in randomized_locations),
                key=lambda costs: (len(costs),) + tuple(costs.values())
            )
            for loc, costs in zip(randomized_locations, prices):
                loc.costs = costs

    def apply_costsanity(self):
        setting = self.multiworld.CostSanity[self.player].value
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

        random = self.multiworld.random
        hybrid_chance = getattr(self.multiworld, f"CostSanityHybridChance")[self.player].value
        weights = {
            data.term: getattr(self.multiworld, f"CostSanity{data.option}Weight")[self.player].value
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
                if location.basename in {'Grubfather', 'Seer', 'Eggshop'}:
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
        world = self.multiworld
        player = self.player
        if world.logic[player] != 'nologic':
            goal = world.Goal[player]
            if goal == Goal.option_hollowknight:
                world.completion_condition[player] = lambda state: state._hk_can_beat_thk(player)
            elif goal == Goal.option_siblings:
                world.completion_condition[player] = lambda state: state._hk_siblings_ending(player)
            elif goal == Goal.option_radiance:
                world.completion_condition[player] = lambda state: state._hk_can_beat_radiance(player)
            else:
                # Any goal
                world.completion_condition[player] = lambda state: state._hk_can_beat_thk(player) or state._hk_can_beat_radiance(player)

        set_rules(self)

    def fill_slot_data(self):
        slot_data = {}

        options = slot_data["options"] = {}
        for option_name in self.option_definitions:
            option = getattr(self.multiworld, option_name)[self.player]
            try:
                optionvalue = int(option.value)
            except TypeError:
                pass  # C# side is currently typed as dict[str, int], drop what doesn't fit
            else:
                options[option_name] = optionvalue

        # 32 bit int
        slot_data["seed"] = self.multiworld.per_slot_randoms[self.player].randint(-2147483647, 2147483646)

        # Backwards compatibility for shop cost data (HKAP < 0.1.0)
        if not self.multiworld.CostSanity[self.player]:
            for shop, terms in shop_cost_types.items():
                unit = cost_terms[next(iter(terms))].option
                if unit == "Geo":
                    continue
                slot_data[f"{unit}_costs"] = {
                    loc.name: next(iter(loc.costs.values()))
                    for loc in self.created_multi_locations[shop]
                }

        # HKAP 0.1.0 and later cost data.
        location_costs = {}
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                if location.costs:
                    location_costs[location.name] = location.costs
        slot_data["location_costs"] = location_costs

        slot_data["notch_costs"] = self.charm_costs

        return slot_data

    def create_item(self, name: str) -> HKItem:
        item_data = item_table[name]
        return HKItem(name, item_data.advancement, item_data.id, item_data.type, self.player)

    def create_location(self, name: str, vanilla=False) -> HKLocation:
        costs = None
        basename = name
        if name in shop_cost_types:
            costs = {
                term: self.multiworld.random.randint(*self.ranges[term])
                for term in shop_cost_types[name]
            }
        elif name in vanilla_location_costs:
            costs = vanilla_location_costs[name]

        multi = self.created_multi_locations.get(name)

        if multi is not None:
            i = len(multi) + 1
            name = f"{name}_{i}"

        region = self.multiworld.get_region("Menu", self.player)
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
                state.prog_items[item.player][effect_name] -= effect_value

        return change

    @classmethod
    def stage_write_spoiler(cls, world: MultiWorld, spoiler_handle):
        hk_players = world.get_game_players(cls.game)
        spoiler_handle.write('\n\nCharm Notches:')
        for player in hk_players:
            name = world.get_player_name(player)
            spoiler_handle.write(f'\n{name}\n')
            hk_world: HKWorld = world.worlds[player]
            for charm_number, cost in enumerate(hk_world.charm_costs):
                spoiler_handle.write(f"\n{charm_names[charm_number]}: {cost}")

        spoiler_handle.write('\n\nShop Prices:')
        for player in hk_players:
            name = world.get_player_name(player)
            spoiler_handle.write(f'\n{name}\n')
            hk_world: HKWorld = world.worlds[player]

            if world.CostSanity[player].value:
                for loc in sorted(
                    (
                        loc for loc in itertools.chain(*(region.locations for region in world.get_regions(player)))
                        if loc.costs
                    ), key=operator.attrgetter('name')
                ):
                    spoiler_handle.write(f"\n{loc}: {loc.item} costing {loc.cost_text()}")
            else:
                for shop_name, locations in hk_world.created_multi_locations.items():
                    for loc in locations:
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
                if getattr(self.multiworld, group):
                    fillers.extend(item for item in hollow_knight_randomize_options[group].items if item not in
                                   exclusions)
            self.cached_filler_items[self.player] = fillers
        return self.multiworld.random.choice(self.cached_filler_items[self.player])


def create_region(world: MultiWorld, player: int, name: str, location_names=None) -> Region:
    ret = Region(name, player, world)
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
        return getattr(self.multiworld, option_name)[player].value

    def _hk_start(self, player, start_location: str) -> bool:
        return self.multiworld.StartLocation[player] == start_location

    def _hk_nail_combat(self, player: int) -> bool:
        return self.has_any({'LEFTSLASH', 'RIGHTSLASH', 'UPSLASH'}, player)

    def _hk_can_beat_thk(self, player: int) -> bool:
        return (
            self.has('Opened_Black_Egg_Temple', player)
            and (self.count('FIREBALL', player) + self.count('SCREAM', player) + self.count('QUAKE', player)) > 1
            and self._hk_nail_combat(player)
            and (
                self.has_any({'LEFTDASH', 'RIGHTDASH'}, player)
                or self._hk_option(player, 'ProficientCombat')
            )
            and self.has('FOCUS', player)
        )

    def _hk_siblings_ending(self, player: int) -> bool:
        return self._hk_can_beat_thk(player) and self.has('WHITEFRAGMENT', player, 3)

    def _hk_can_beat_radiance(self, player: int) -> bool:
        return (
            self.has('Opened_Black_Egg_Temple', player)
            and self._hk_nail_combat(player)
            and self.has('WHITEFRAGMENT', player, 3)
            and self.has('DREAMNAIL', player)
            and (
                (self.has('LEFTCLAW', player) and self.has('RIGHTCLAW', player))
                or self.has('WINGS', player)
            )
            and (self.count('FIREBALL', player) + self.count('SCREAM', player) + self.count('QUAKE', player)) > 1
            and (
                (self.has('LEFTDASH', player, 2) and self.has('RIGHTDASH', player, 2))  # Both Shade Cloaks
                or (self._hk_option(player, 'ProficientCombat') and self.has('QUAKE', player))  # or Dive
            )
        )
