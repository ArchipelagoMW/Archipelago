from BaseClasses import Item, ItemClassification, Tutorial, Location, MultiWorld
from .Items import item_table, create_item, relic_groups, act_contracts, create_itempool, get_shop_trap_name, \
    calculate_yarn_costs, alps_hooks
from .Regions import create_regions, randomize_act_entrances, chapter_act_info, create_events, get_shuffled_region
from .Locations import location_table, contract_locations, is_location_valid, get_location_names, TASKSANITY_START_ID, \
    get_total_locations
from .Rules import set_rules, has_paintings
from .Options import AHITOptions, slot_data_options, adjust_options, RandomizeHatOrder, EndGoal, create_option_groups
from .Types import HatType, ChapterIndex, HatInTimeItem, hat_type_to_item, Difficulty
from .DeathWishLocations import create_dw_regions, dw_classes, death_wishes
from .DeathWishRules import set_dw_rules, create_enemy_events, hit_list, bosses
from worlds.AutoWorld import World, WebWorld, CollectionState
from worlds.generic.Rules import add_rule
from typing import List, Dict, TextIO
from worlds.LauncherComponents import Component, components, icon_paths, launch as launch_component, Type
from Utils import local_path


def launch_client():
    from .Client import launch
    launch_component(launch, name="AHITClient")


components.append(Component("A Hat in Time Client", "AHITClient", func=launch_client,
                            component_type=Type.CLIENT, icon='yatta'))

icon_paths['yatta'] = local_path('data', 'yatta.png')


class AWebInTime(WebWorld):
    theme = "partyTime"
    option_groups = create_option_groups()
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up A Hat in Time to be played in Archipelago.",
        "English",
        "ahit_en.md",
        "setup/en",
        ["CookieCat"]
    )]


class HatInTimeWorld(World):
    """
    A Hat in Time is a cute-as-peck 3D platformer featuring a little girl who stitches hats for wicked powers!
    Freely explore giant worlds and recover Time Pieces to travel to new heights!
    """

    game = "A Hat in Time"
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()
    options_dataclass = AHITOptions
    options: AHITOptions
    item_name_groups = relic_groups
    web = AWebInTime()

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.act_connections: Dict[str, str] = {}
        self.shop_locs: List[str] = []

        self.hat_craft_order: List[HatType] = [HatType.SPRINT, HatType.BREWING, HatType.ICE,
                                               HatType.DWELLER, HatType.TIME_STOP]

        self.hat_yarn_costs: Dict[HatType, int] = {HatType.SPRINT: -1, HatType.BREWING: -1, HatType.ICE: -1,
                                                   HatType.DWELLER: -1, HatType.TIME_STOP: -1}

        self.chapter_timepiece_costs: Dict[ChapterIndex, int] = {ChapterIndex.MAFIA: -1,
                                                                 ChapterIndex.BIRDS: -1,
                                                                 ChapterIndex.SUBCON: -1,
                                                                 ChapterIndex.ALPINE: -1,
                                                                 ChapterIndex.FINALE: -1,
                                                                 ChapterIndex.CRUISE: -1,
                                                                 ChapterIndex.METRO: -1}
        self.excluded_dws: List[str] = []
        self.excluded_bonuses: List[str] = []
        self.dw_shuffle: List[str] = []
        self.nyakuza_thug_items: Dict[str, int] = {}
        self.badge_seller_count: int = 0

    def generate_early(self):
        adjust_options(self)

        if self.options.StartWithCompassBadge:
            self.multiworld.push_precollected(self.create_item("Compass Badge"))

        if self.is_dw_only():
            return

        # Take care of some extremely restrictive starts in other chapters with act shuffle off
        if not self.options.ActRandomizer:
            start_chapter = self.options.StartingChapter
            if start_chapter == ChapterIndex.ALPINE:
                self.multiworld.push_precollected(self.create_item("Hookshot Badge"))
                if self.options.UmbrellaLogic:
                    self.multiworld.push_precollected(self.create_item("Umbrella"))

                if self.options.ShuffleAlpineZiplines:
                    ziplines = list(alps_hooks.keys())
                    ziplines.remove("Zipline Unlock - The Twilight Bell Path")  # not enough checks from this one
                    self.multiworld.push_precollected(self.create_item(self.random.choice(ziplines)))
            elif start_chapter == ChapterIndex.SUBCON:
                if self.options.ShuffleSubconPaintings:
                    self.multiworld.push_precollected(self.create_item("Progressive Painting Unlock"))
            elif start_chapter == ChapterIndex.BIRDS:
                if self.options.UmbrellaLogic:
                    if self.options.LogicDifficulty < Difficulty.EXPERT:
                        self.multiworld.push_precollected(self.create_item("Umbrella"))
                elif self.options.LogicDifficulty < Difficulty.MODERATE:
                    self.multiworld.push_precollected(self.create_item("Umbrella"))

    def create_regions(self):
        # noinspection PyClassVar
        self.topology_present = bool(self.options.ActRandomizer)

        create_regions(self)
        if self.options.EnableDeathWish:
            create_dw_regions(self)

        if self.is_dw_only():
            return

        create_events(self)
        if self.is_dw():
            if "Snatcher's Hit List" not in self.excluded_dws or "Camera Tourist" not in self.excluded_dws:
                create_enemy_events(self)

        # place vanilla contract locations if contract shuffle is off
        if not self.options.ShuffleActContracts:
            for name in contract_locations.keys():
                loc = self.get_location(name)
                loc.place_locked_item(create_item(self, name))
                if self.options.ShuffleSubconPaintings and loc.name != "Snatcher's Contract - The Subcon Well":
                    add_rule(loc, lambda state: has_paintings(state, self, 1))

    def create_items(self):
        if self.has_yarn():
            calculate_yarn_costs(self)

            if self.options.RandomizeHatOrder:
                self.random.shuffle(self.hat_craft_order)
                if self.options.RandomizeHatOrder == RandomizeHatOrder.option_time_stop_last:
                    self.hat_craft_order.remove(HatType.TIME_STOP)
                    self.hat_craft_order.append(HatType.TIME_STOP)

            # move precollected hats to the start of the list
            for i in range(5):
                hat = HatType(i)
                if self.is_hat_precollected(hat):
                    self.hat_craft_order.remove(hat)
                    self.hat_craft_order.insert(0, hat)

        self.multiworld.itempool += create_itempool(self)

    def set_rules(self):
        if self.is_dw_only():
            # we already have all items if this is the case, no need for rules
            self.multiworld.push_precollected(HatInTimeItem("Death Wish Only Mode", ItemClassification.progression,
                                              None, self.player))

            self.multiworld.completion_condition[self.player] = lambda state: state.has("Death Wish Only Mode",
                                                                                        self.player)

            if not self.options.DWEnableBonus:
                for name in death_wishes:
                    if name == "Snatcher Coins in Nyakuza Metro" and not self.is_dlc2():
                        continue

                    if self.options.DWShuffle and name not in self.dw_shuffle:
                        continue

                    full_clear = self.multiworld.get_location(f"{name} - All Clear", self.player)
                    full_clear.address = None
                    full_clear.place_locked_item(HatInTimeItem("Nothing", ItemClassification.filler, None, self.player))
                    full_clear.show_in_spoiler = False

            return

        if self.options.ActRandomizer:
            randomize_act_entrances(self)

        set_rules(self)

        if self.is_dw():
            set_dw_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {"Chapter1Cost": self.chapter_timepiece_costs[ChapterIndex.MAFIA],
                           "Chapter2Cost": self.chapter_timepiece_costs[ChapterIndex.BIRDS],
                           "Chapter3Cost": self.chapter_timepiece_costs[ChapterIndex.SUBCON],
                           "Chapter4Cost": self.chapter_timepiece_costs[ChapterIndex.ALPINE],
                           "Chapter5Cost": self.chapter_timepiece_costs[ChapterIndex.FINALE],
                           "Chapter6Cost": self.chapter_timepiece_costs[ChapterIndex.CRUISE],
                           "Chapter7Cost": self.chapter_timepiece_costs[ChapterIndex.METRO],
                           "BadgeSellerItemCount": self.badge_seller_count,
                           "SeedNumber": str(self.multiworld.seed),  # For shop prices
                           "SeedName": self.multiworld.seed_name,
                           "TotalLocations": get_total_locations(self)}

        if self.has_yarn():
            slot_data.setdefault("SprintYarnCost", self.hat_yarn_costs[HatType.SPRINT])
            slot_data.setdefault("BrewingYarnCost", self.hat_yarn_costs[HatType.BREWING])
            slot_data.setdefault("IceYarnCost", self.hat_yarn_costs[HatType.ICE])
            slot_data.setdefault("DwellerYarnCost", self.hat_yarn_costs[HatType.DWELLER])
            slot_data.setdefault("TimeStopYarnCost", self.hat_yarn_costs[HatType.TIME_STOP])
            slot_data.setdefault("Hat1", int(self.hat_craft_order[0]))
            slot_data.setdefault("Hat2", int(self.hat_craft_order[1]))
            slot_data.setdefault("Hat3", int(self.hat_craft_order[2]))
            slot_data.setdefault("Hat4", int(self.hat_craft_order[3]))
            slot_data.setdefault("Hat5", int(self.hat_craft_order[4]))

        if self.options.ActRandomizer:
            for name in self.act_connections.keys():
                slot_data[name] = self.act_connections[name]

        if self.is_dlc2() and not self.is_dw_only():
            for name in self.nyakuza_thug_items.keys():
                slot_data[name] = self.nyakuza_thug_items[name]

        if self.is_dw():
            i = 0
            for name in self.excluded_dws:
                if self.options.EndGoal.value == EndGoal.option_seal_the_deal and name == "Seal the Deal":
                    continue

                slot_data[f"excluded_dw{i}"] = dw_classes[name]
                i += 1

            i = 0
            if not self.options.DWAutoCompleteBonuses:
                for name in self.excluded_bonuses:
                    if name in self.excluded_dws:
                        continue

                    slot_data[f"excluded_bonus{i}"] = dw_classes[name]
                    i += 1

            if self.options.DWShuffle:
                shuffled_dws = self.dw_shuffle
                for i in range(len(shuffled_dws)):
                    slot_data[f"dw_{i}"] = dw_classes[shuffled_dws[i]]

        shop_item_names: Dict[str, str] = {}
        for name in self.shop_locs:
            loc: Location = self.multiworld.get_location(name, self.player)
            assert loc.item
            item_name: str
            if loc.item.classification is ItemClassification.trap and loc.item.game == "A Hat in Time":
                item_name = get_shop_trap_name(self)
            else:
                item_name = loc.item.name

            shop_item_names.setdefault(str(loc.address),
                                       f"{item_name} ({self.multiworld.get_player_name(loc.item.player)})")

        slot_data["ShopItemNames"] = shop_item_names

        for name, value in self.options.as_dict(*self.options_dataclass.type_hints).items():
            if name in slot_data_options:
                slot_data[name] = value

        return slot_data

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        if self.is_dw_only() or not self.options.ActRandomizer:
            return

        new_hint_data = {}
        alpine_regions = ["The Birdhouse", "The Lava Cake", "The Windmill",
                          "The Twilight Bell", "Alpine Skyline Area", "Alpine Skyline Area (TIHS)"]

        metro_regions = ["Yellow Overpass Station", "Green Clean Station", "Bluefin Tunnel", "Pink Paw Station"]

        for key, data in location_table.items():
            if not is_location_valid(self, key):
                continue

            location = self.multiworld.get_location(key, self.player)
            region_name: str

            if data.region in alpine_regions:
                region_name = "Alpine Free Roam"
            elif data.region in metro_regions:
                region_name = "Nyakuza Free Roam"
            elif "Dead Bird Studio - " in data.region:
                region_name = "Dead Bird Studio"
            elif data.region in chapter_act_info.keys():
                region_name = location.parent_region.name
            else:
                continue

            new_hint_data[location.address] = get_shuffled_region(self, region_name)

        if self.is_dlc1() and self.options.Tasksanity:
            ship_shape_region = get_shuffled_region(self, "Ship Shape")
            id_start: int = TASKSANITY_START_ID
            for i in range(self.options.TasksanityCheckCount):
                new_hint_data[id_start+i] = ship_shape_region

        hint_data[self.player] = new_hint_data

    def write_spoiler_header(self, spoiler_handle: TextIO):
        for i in self.chapter_timepiece_costs:
            spoiler_handle.write("Chapter %i Cost: %i\n" % (i, self.chapter_timepiece_costs[ChapterIndex(i)]))

        for hat in self.hat_craft_order:
            spoiler_handle.write("Hat Cost: %s: %i\n" % (hat, self.hat_yarn_costs[hat]))

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        old_count: int = state.count(item.name, self.player)
        change = super().collect(state, item)
        if change and old_count == 0:
            if "Stamp" in item.name:
                if "2 Stamp" in item.name:
                    state.prog_items[self.player]["Stamps"] += 2
                else:
                    state.prog_items[self.player]["Stamps"] += 1
            elif "(Zero Jumps)" in item.name:
                state.prog_items[self.player]["Zero Jumps"] += 1
            elif item.name in hit_list.keys():
                if item.name not in bosses:
                    state.prog_items[self.player]["Enemy"] += 1
                else:
                    state.prog_items[self.player]["Boss"] += 1

        return change

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        old_count: int = state.count(item.name, self.player)
        change = super().remove(state, item)
        if change and old_count == 1:
            if "Stamp" in item.name:
                if "2 Stamp" in item.name:
                    state.prog_items[self.player]["Stamps"] -= 2
                else:
                    state.prog_items[self.player]["Stamps"] -= 1
            elif "(Zero Jumps)" in item.name:
                state.prog_items[self.player]["Zero Jumps"] -= 1
            elif item.name in hit_list.keys():
                if item.name not in bosses:
                    state.prog_items[self.player]["Enemy"] -= 1
                else:
                    state.prog_items[self.player]["Boss"] -= 1

        return change

    def has_yarn(self) -> bool:
        return not self.is_dw_only() and not self.options.HatItems

    def is_hat_precollected(self, hat: HatType) -> bool:
        for item in self.multiworld.precollected_items[self.player]:
            if item.name == hat_type_to_item[hat]:
                return True

        return False

    def is_dlc1(self) -> bool:
        return bool(self.options.EnableDLC1)

    def is_dlc2(self) -> bool:
        return bool(self.options.EnableDLC2)

    def is_dw(self) -> bool:
        return bool(self.options.EnableDeathWish)

    def is_dw_only(self) -> bool:
        return self.is_dw() and bool(self.options.DeathWishOnly)

    def is_dw_excluded(self, name: str) -> bool:
        # don't exclude Seal the Deal if it's our goal
        if self.options.EndGoal.value == EndGoal.option_seal_the_deal and name == "Seal the Deal" \
           and f"{name} - Main Objective" not in self.options.exclude_locations:
            return False

        if name in self.excluded_dws:
            return True

        return f"{name} - Main Objective" in self.options.exclude_locations

    def is_bonus_excluded(self, name: str) -> bool:
        if self.is_dw_excluded(name) or name in self.excluded_bonuses:
            return True

        return f"{name} - All Clear" in self.options.exclude_locations
