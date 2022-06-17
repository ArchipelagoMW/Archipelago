from __future__ import annotations

import logging
import typing
from collections import Counter

logger = logging.getLogger("Hollow Knight")

from .Items import item_table, lookup_type_to_names, item_name_groups
from .Regions import create_regions
from .Rules import set_rules
from .Options import hollow_knight_options, hollow_knight_randomize_options, disabled, Goal, WhitePalace
from .ExtractedData import locations, starts, multi_locations, location_to_region_lookup, \
    event_names, item_effects, connectors, one_ways
from .Charms import names as charm_names

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, RegionType, LocationProgressType, Tutorial, ItemClassification
from ..AutoWorld import World, LogicMixin, WebWorld

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


class HKWeb(WebWorld):
    tutorials = [Tutorial(
        "Mod Setup and Use Guide",
        "A guide to playing Hollow Knight with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Ijwu"]
    )]


class HKWorld(World):
    """Beneath the fading town of Dirtmouth sleeps a vast, ancient kingdom. Many are drawn beneath the surface, 
    searching for riches, or glory, or answers to old secrets.

    As the enigmatic Knight, you’ll traverse the depths, unravel its mysteries and conquer its evils.
    """  # from https://www.hollowknight.com
    game: str = "Hollow Knight"
    options = hollow_knight_options

    web = HKWeb()

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location_name: location_id for location_id, location_name in
                           enumerate(locations, start=0x1000000)}
    item_name_groups = item_name_groups

    ranges: typing.Dict[str, typing.Tuple[int, int]]
    shops: typing.Dict[str, str] = {
        "Egg_Shop": "Egg",
        "Grubfather": "Grub",
        "Seer": "Essence",
        "Salubra_(Requires_Charms)": "Charm"
    }
    charm_costs: typing.List[int]
    data_version = 2

    def __init__(self, world, player):
        super(HKWorld, self).__init__(world, player)
        self.created_multi_locations: typing.Dict[str, int] = Counter()
        self.ranges = {}

    def generate_early(self):
        world = self.world
        charm_costs = world.RandomCharmCosts[self.player].get_costs(world.random)
        self.charm_costs = world.PlandoCharmCosts[self.player].get_costs(charm_costs)
        # world.exclude_locations[self.player].value.update(white_palace_locations)
        world.local_items[self.player].value.add("Mimic_Grub")
        for vendor, unit in self.shops.items():
            mini = getattr(world, f"Minimum{unit}Price")[self.player]
            maxi = getattr(world, f"Maximum{unit}Price")[self.player]
            # if minimum > maximum, set minimum to maximum
            mini.value = min(mini.value, maxi.value)
            self.ranges[unit] = mini.value, maxi.value
        world.push_precollected(HKItem(starts[world.StartLocation[self.player].current_key],
                                       True, None, "Event", self.player))
        for option_name in disabled:
            getattr(world, option_name)[self.player].value = 0

    def white_palace_exclusions(self):
        exclusions = set()
        wp = self.world.WhitePalace[self.player]
        if wp <= WhitePalace.option_nopathofpain:
            exclusions.update(path_of_pain_locations)
        if wp <= WhitePalace.option_kingfragment:
            exclusions.update(white_palace_checks)
        if wp == WhitePalace.option_exclude and self.world.RandomizeCharms[self.player]:
            # Ensure KF location is still reachable if charms are non-randomized
            exclusions.update(white_palace_transitions)
            exclusions.update(white_palace_events)
            exclusions.add("King_Fragment")
        return exclusions

    def create_regions(self):
        menu_region: Region = create_region(self.world, self.player, 'Menu')
        self.world.regions.append(menu_region)
        wp_exclusions = self.white_palace_exclusions()

        # Link regions
        for event_name in event_names:
            if event_name in wp_exclusions:
                continue
            loc = HKLocation(self.player, event_name, None, menu_region)
            loc.place_locked_item(HKItem(event_name,
                                         event_name not in wp_exclusions,
                                         None, "Event", self.player))
            menu_region.locations.append(loc)
        for entry_transition, exit_transition in connectors.items():
            if entry_transition in wp_exclusions:
                continue
            if exit_transition:
                # if door logic fulfilled -> award vanilla target as event
                loc = HKLocation(self.player, entry_transition, None, menu_region)
                loc.place_locked_item(HKItem(exit_transition,
                                             exit_transition not in wp_exclusions,
                                             None, "Event", self.player))
                menu_region.locations.append(loc)

    def create_items(self):
        # Generate item pool and associated locations (paired in HK)
        pool: typing.List[HKItem] = []
        geo_replace: typing.Set[str] = set()
        if self.world.RemoveSpellUpgrades[self.player]:
            geo_replace.add("Abyss_Shriek")
            geo_replace.add("Shade_Soul")
            geo_replace.add("Descending_Dark")

        wp_exclusions = self.white_palace_exclusions()
        for option_key, option in hollow_knight_randomize_options.items():
            if getattr(self.world, option_key)[self.player]:
                for item_name, location_name in zip(option.items, option.locations):
                    if location_name in wp_exclusions:
                        continue
                    if item_name in geo_replace:
                        item_name = "Geo_Rock-Default"
                    item = self.create_item(item_name)
                        # self.create_location(location_name).place_locked_item(item)
                    if location_name == "Start":
                        self.world.push_precollected(item)
                    else:
                        self.create_location(location_name)
                        pool.append(item)
            # elif option_key not in logicless_options:
            else:
                for item_name, location_name in zip(option.items, option.locations):
                    if location_name in wp_exclusions and location_name != 'King_Fragment':
                        continue
                    item = self.create_item(item_name)
                    if location_name == "Start":
                        self.world.push_precollected(item)
                    else:
                        self.create_location(location_name).place_locked_item(item)
        for i in range(self.world.EggShopSlots[self.player].value):
            self.create_location("Egg_Shop")
            pool.append(self.create_item("Geo_Rock-Default"))
        self.world.itempool += pool

        for shopname in self.shops:
            prices: typing.List[int] = []
            locations: typing.List[HKLocation] = []
            for x in range(1, self.created_multi_locations[shopname]+1):
                loc = self.world.get_location(self.get_multi_location_name(shopname, x), self.player)
                locations.append(loc)
                prices.append(loc.cost)
            prices.sort()
            for loc, price in zip(locations, prices):
                loc.cost = price

    def set_rules(self):
        world = self.world
        player = self.player
        if world.logic[player] != 'nologic':
            goal = world.Goal[player]
            if goal == Goal.option_siblings:
                world.completion_condition[player] = lambda state: state._hk_siblings_ending(player)
            elif goal == Goal.option_radiance:
                world.completion_condition[player] = lambda state: state._hk_can_beat_radiance(player)
            else:
                # Hollow Knight or Any goal.
                world.completion_condition[player] = lambda state: state._hk_can_beat_thk(player)

        set_rules(self)

    def fill_slot_data(self):
        slot_data = {}

        options = slot_data["options"] = {}
        for option_name in self.options:
            option = getattr(self.world, option_name)[self.player]
            try:
                optionvalue = int(option.value)
            except TypeError:
                pass  # C# side is currently typed as dict[str, int], drop what doesn't fit
            else:
                options[option_name] = optionvalue

        # 32 bit int
        slot_data["seed"] = self.world.slot_seeds[self.player].randint(-2147483647, 2147483646)

        for shop, unit in self.shops.items():
            slot_data[f"{unit}_costs"] = {
                f"{shop}_{i}":
                    self.world.get_location(f"{shop}_{i}", self.player).cost
                for i in range(1, 1 + self.created_multi_locations[shop])
            }

        slot_data["notch_costs"] = self.charm_costs

        return slot_data

    def create_item(self, name: str) -> HKItem:
        item_data = item_table[name]
        return HKItem(name, item_data.advancement, item_data.id, item_data.type, self.player)

    def create_location(self, name: str) -> HKLocation:
        unit = self.shops.get(name, None)
        if unit:
            cost = self.world.random.randint(*self.ranges[unit])
        else:
            cost = 0
        if name in multi_locations:
            self.created_multi_locations[name] += 1
            name = self.get_multi_location_name(name, self.created_multi_locations[name])

        region = self.world.get_region("Menu", self.player)
        loc = HKLocation(self.player, name, self.location_name_to_id[name], region)
        if unit:
            loc.unit = unit
            loc.cost = cost
        region.locations.append(loc)
        return loc

    def collect(self, state, item: HKItem) -> bool:
        change = super(HKWorld, self).collect(state, item)
        if change:
            for effect_name, effect_value in item_effects.get(item.name, {}).items():
                state.prog_items[effect_name, item.player] += effect_value

        return change

    def remove(self, state, item: HKItem) -> bool:
        change = super(HKWorld, self).remove(state, item)

        if change:
            for effect_name, effect_value in item_effects.get(item.name, {}).items():
                if state.prog_items[effect_name, item.player] == effect_value:
                    del state.prog_items[effect_name, item.player]
                state.prog_items[effect_name, item.player] -= effect_value

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
            for shop_name, unit_name in cls.shops.items():
                for x in range(1, hk_world.created_multi_locations[shop_name]+1):
                    loc = world.get_location(hk_world.get_multi_location_name(shop_name, x), player)
                    spoiler_handle.write(f"\n{loc}: {loc.item} costing {loc.cost} {unit_name}")

    def get_multi_location_name(self, base: str, i: typing.Optional[int]) -> str:
        if i is None:
            i = self.created_multi_locations[base]
        assert 0 < i < 18, "limited number of multi location IDs reserved."
        return f"{base}_{i}"


def create_region(world: MultiWorld, player: int, name: str, location_names=None, exits=None) -> Region:
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if location_names:
        for location in location_names:
            loc_id = HKWorld.location_name_to_id.get(location, None)
            location = HKLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))
    return ret


class HKLocation(Location):
    game: str = "Hollow Knight"
    cost: int = 0
    unit: typing.Optional[str] = None

    def __init__(self, player: int, name: str, code=None, parent=None):
        super(HKLocation, self).__init__(player, name, code if code else None, parent)


class HKItem(Item):
    game = "Hollow Knight"

    def __init__(self, name, advancement, code, type, player: int = None):
        if name == "Mimic_Grub":
            classification = ItemClassification.trap
        elif type in ("Grub", "DreamWarrior", "Root", "Egg"):
            classification = ItemClassification.progression_skip_balancing
        elif type == "Charm" and name not in progression_charms:
            classification = ItemClassification.progression_skip_balancing
        elif advancement:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler
        super(HKItem, self).__init__(name, classification, code if code else None, player)
        self.type = type


class HKLogicMixin(LogicMixin):
    world: MultiWorld

    def _hk_notches(self, player: int, *notches: int) -> int:
        return sum(self.world.worlds[player].charm_costs[notch] for notch in notches)

    def _hk_option(self, player: int, option_name: str) -> int:
        return getattr(self.world, option_name)[player].value

    def _hk_start(self, player, start_location: str) -> bool:
        return self.world.StartLocation[player] == start_location

    def _hk_nail_combat(self, player: int) -> bool:
        return self.has_any({'LFFTSLASH', 'RIGHTSLASH', 'UPSLASH'}, player)

    def _hk_can_beat_thk(self, player: int) -> bool:
        return (
            self.has('Opened_Black_Egg_Temple', player)
            and (self.count('FIREBALL', player) + self.count('SCREAM', player) + self.count('QUAKE', player)) > 1
            and self._hk_nail_combat(player)
            and (
                self.has_any({'LEFTDASH', 'RIGHTDASH'}, player)
                or self._hk_option(player, 'ProficientCombat')
            )
        )

    def _hk_siblings_ending(self, player: int) -> bool:
        return self._hk_can_beat_thk(player) and self.has('WHITEFRAGMENT', player, 3)

    def _hk_can_beat_radiance(self, player: int) -> bool:
        return (
            self._hk_siblings_ending(player)
            and self.has('DREAMNAIL', player, 1)
            and (
                (self.has('LEFTCLAW', player) and self.has('RIGHTCLAW', player))
                or self.has('WINGS', player)
            )
            and (
                self.count('FIREBALL', player) + self.count('SCREAM', player)
                + self.count('QUAKE', player)
            ) > 1
            and (
                (self.has('LEFTDASH', player, 2) and self.has('RIGHTDASH', player, 2))  # Both Shade Cloaks
                or (self._hk_option(player, 'ProficientCombat') and self.has('QUAKE', player))  # or Dive
            )
        )
