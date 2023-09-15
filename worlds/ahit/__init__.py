from BaseClasses import Item, ItemClassification, LocationProgressType, Tutorial
from .Items import HatInTimeItem, item_table, create_item, relic_groups, act_contracts, create_itempool
from .Regions import create_regions, randomize_act_entrances, chapter_act_info, create_events, get_shuffled_region
from .Locations import location_table, contract_locations, is_location_valid, get_location_names, get_tasksanity_start_id
from .Rules import set_rules
from .Options import ahit_options, slot_data_options, adjust_options
from .Types import HatType, ChapterIndex
from .DeathWishLocations import create_dw_regions, dw_classes, death_wishes
from .DeathWishRules import set_dw_rules, create_enemy_events
from worlds.AutoWorld import World, WebWorld
from typing import List, Dict, TextIO

hat_craft_order: Dict[int, List[HatType]] = {}
hat_yarn_costs: Dict[int, Dict[HatType, int]] = {}
chapter_timepiece_costs: Dict[int, Dict[ChapterIndex, int]] = {}
excluded_dws: Dict[int, List[str]] = {}
excluded_bonuses: Dict[int, List[str]] = {}
dw_shuffle: Dict[int, List[str]] = {}
nyakuza_thug_items: Dict[int, Dict[str, int]] = {}
badge_seller_count: Dict[int, int] = {}


class AWebInTime(WebWorld):
    theme = "partyTime"
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
    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()

    option_definitions = ahit_options
    act_connections: Dict[str, str] = {}
    shop_locs: List[str] = []
    item_name_groups = relic_groups
    web = AWebInTime()

    def generate_early(self):
        adjust_options(self)

        if self.multiworld.StartWithCompassBadge[self.player].value > 0:
            self.multiworld.push_precollected(self.create_item("Compass Badge"))

        if self.is_dw_only():
            return

        # If our starting chapter is 4 and act rando isn't on, force hookshot into inventory
        # If starting chapter is 3 and painting shuffle is enabled, and act rando isn't, give one free painting unlock
        start_chapter: int = self.multiworld.StartingChapter[self.player].value

        if start_chapter == 4 or start_chapter == 3:
            if self.multiworld.ActRandomizer[self.player].value == 0:
                if start_chapter == 4:
                    self.multiworld.push_precollected(self.create_item("Hookshot Badge"))

                if start_chapter == 3 and self.multiworld.ShuffleSubconPaintings[self.player].value > 0:
                    self.multiworld.push_precollected(self.create_item("Progressive Painting Unlock"))

    def create_regions(self):
        excluded_dws[self.player] = []
        excluded_bonuses[self.player] = []
        dw_shuffle[self.player] = []
        nyakuza_thug_items[self.player] = {}
        badge_seller_count[self.player] = 0
        self.shop_locs = []
        self.topology_present = self.multiworld.ActRandomizer[self.player].value

        create_regions(self)

        if self.multiworld.EnableDeathWish[self.player].value > 0:
            create_dw_regions(self)

        if self.is_dw_only():
            return

        create_events(self)
        if self.is_dw():
            if "Snatcher's Hit List" not in self.get_excluded_dws() \
               or "Camera Tourist" not in self.get_excluded_dws():
                create_enemy_events(self)

        # place default contract locations if contract shuffle is off so logic can still utilize them
        if self.multiworld.ShuffleActContracts[self.player].value == 0:
            for name in contract_locations.keys():
                self.multiworld.get_location(name, self.player).place_locked_item(create_item(self, name))
        else:
            # The bag trap contract check needs to be excluded, because if the player has the Subcon Well contract,
            # the trap will not activate, locking the player out of the check permanently
            self.multiworld.get_location("Snatcher's Contract - The Subcon Well",
                                         self.player).progress_type = LocationProgressType.EXCLUDED

    def create_items(self):
        hat_yarn_costs[self.player] = {HatType.SPRINT: -1, HatType.BREWING: -1, HatType.ICE: -1,
                                       HatType.DWELLER: -1, HatType.TIME_STOP: -1}

        hat_craft_order[self.player] = [HatType.SPRINT, HatType.BREWING, HatType.ICE,
                                        HatType.DWELLER, HatType.TIME_STOP]

        if self.multiworld.HatItems[self.player].value == 0 and self.multiworld.RandomizeHatOrder[self.player].value > 0:
            self.random.shuffle(hat_craft_order[self.player])
            if self.multiworld.RandomizeHatOrder[self.player].value == 2:
                hat_craft_order[self.player].remove(HatType.TIME_STOP)
                hat_craft_order[self.player].append(HatType.TIME_STOP)

        self.multiworld.itempool += create_itempool(self)

    def set_rules(self):
        self.act_connections = {}
        chapter_timepiece_costs[self.player] = {ChapterIndex.MAFIA: -1,
                                                ChapterIndex.BIRDS: -1,
                                                ChapterIndex.SUBCON: -1,
                                                ChapterIndex.ALPINE: -1,
                                                ChapterIndex.FINALE: -1,
                                                ChapterIndex.CRUISE: -1,
                                                ChapterIndex.METRO: -1}

        if self.is_dw_only():
            # we already have all items if this is the case, no need for rules
            self.multiworld.push_precollected(HatInTimeItem("Death Wish Only Mode", ItemClassification.progression,
                                              None, self.player))

            self.multiworld.completion_condition[self.player] = lambda state: state.has("Death Wish Only Mode",
                                                                                        self.player)

            if self.multiworld.DWEnableBonus[self.player].value == 0:
                for name in death_wishes:
                    if name == "Snatcher Coins in Nyakuza Metro" and not self.is_dlc2():
                        continue

                    if self.multiworld.DWShuffle[self.player].value > 0 and name not in self.get_dw_shuffle():
                        continue

                    full_clear = self.multiworld.get_location(f"{name} - All Clear", self.player)
                    full_clear.address = None
                    full_clear.place_locked_item(HatInTimeItem("Nothing", ItemClassification.filler, None, self.player))
                    full_clear.show_in_spoiler = False

            return

        if self.multiworld.ActRandomizer[self.player].value > 0:
            randomize_act_entrances(self)

        set_rules(self)

        if self.multiworld.EnableDeathWish[self.player].value > 0:
            set_dw_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {"Chapter1Cost": chapter_timepiece_costs[self.player][ChapterIndex.MAFIA],
                           "Chapter2Cost": chapter_timepiece_costs[self.player][ChapterIndex.BIRDS],
                           "Chapter3Cost": chapter_timepiece_costs[self.player][ChapterIndex.SUBCON],
                           "Chapter4Cost": chapter_timepiece_costs[self.player][ChapterIndex.ALPINE],
                           "Chapter5Cost": chapter_timepiece_costs[self.player][ChapterIndex.FINALE],
                           "Chapter6Cost": chapter_timepiece_costs[self.player][ChapterIndex.CRUISE],
                           "Chapter7Cost": chapter_timepiece_costs[self.player][ChapterIndex.METRO],
                           "BadgeSellerItemCount": badge_seller_count[self.player],
                           "SeedNumber": self.multiworld.seed}  # For shop prices

        if self.multiworld.HatItems[self.player].value == 0:
            slot_data.setdefault("SprintYarnCost", hat_yarn_costs[self.player][HatType.SPRINT])
            slot_data.setdefault("BrewingYarnCost", hat_yarn_costs[self.player][HatType.BREWING])
            slot_data.setdefault("IceYarnCost", hat_yarn_costs[self.player][HatType.ICE])
            slot_data.setdefault("DwellerYarnCost", hat_yarn_costs[self.player][HatType.DWELLER])
            slot_data.setdefault("TimeStopYarnCost", hat_yarn_costs[self.player][HatType.TIME_STOP])
            slot_data.setdefault("Hat1", int(hat_craft_order[self.player][0]))
            slot_data.setdefault("Hat2", int(hat_craft_order[self.player][1]))
            slot_data.setdefault("Hat3", int(hat_craft_order[self.player][2]))
            slot_data.setdefault("Hat4", int(hat_craft_order[self.player][3]))
            slot_data.setdefault("Hat5", int(hat_craft_order[self.player][4]))

        if self.multiworld.ActRandomizer[self.player].value > 0:
            for name in self.act_connections.keys():
                slot_data[name] = self.act_connections[name]

        if self.is_dlc2() and not self.is_dw_only():
            for name in nyakuza_thug_items[self.player].keys():
                slot_data[name] = nyakuza_thug_items[self.player][name]

        if self.is_dw():
            i: int = 0
            for name in excluded_dws[self.player]:
                if self.multiworld.EndGoal[self.player].value == 3 and name == "Seal the Deal":
                    continue

                slot_data[f"excluded_dw{i}"] = dw_classes[name]
                i += 1

            i = 0
            if self.multiworld.DWAutoCompleteBonuses[self.player].value == 0:
                for name in excluded_bonuses[self.player]:
                    if name in excluded_dws[self.player]:
                        continue

                    slot_data[f"excluded_bonus{i}"] = dw_classes[name]
                    i += 1

            if self.multiworld.DWShuffle[self.player].value > 0:
                shuffled_dws = self.get_dw_shuffle()
                for i in range(len(shuffled_dws)):
                    slot_data[f"dw_{i}"] = dw_classes[shuffled_dws[i]]

        for option_name in slot_data_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        if self.is_dw_only() or self.multiworld.ActRandomizer[self.player].value == 0:
            return

        new_hint_data = {}
        alpine_regions = ["The Birdhouse", "The Lava Cake", "The Windmill", "The Twilight Bell", "Alpine Skyline Area"]
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
            elif data.region in chapter_act_info.keys():
                region_name = location.parent_region.name
            else:
                continue

            new_hint_data[location.address] = get_shuffled_region(self, region_name)

        if self.is_dlc1() and self.multiworld.Tasksanity[self.player].value > 0:
            ship_shape_region = get_shuffled_region(self, "Ship Shape")
            id_start: int = get_tasksanity_start_id()
            for i in range(self.multiworld.TasksanityCheckCount[self.player].value):
                new_hint_data[id_start+i] = ship_shape_region

        hint_data[self.player] = new_hint_data

    def write_spoiler_header(self, spoiler_handle: TextIO):
        for i in self.get_chapter_costs():
            spoiler_handle.write("Chapter %i Cost: %i\n" % (i, self.get_chapter_costs()[ChapterIndex(i)]))

        for hat in hat_craft_order[self.player]:
            spoiler_handle.write("Hat Cost: %s: %i\n" % (hat, hat_yarn_costs[self.player][hat]))

    def set_chapter_cost(self, chapter: ChapterIndex, cost: int):
        chapter_timepiece_costs[self.player][chapter] = cost

    def get_chapter_cost(self, chapter: ChapterIndex) -> int:
        return chapter_timepiece_costs[self.player][chapter]

    def get_hat_craft_order(self):
        return hat_craft_order[self.player]

    def get_hat_yarn_costs(self):
        return hat_yarn_costs[self.player]

    def get_chapter_costs(self):
        return chapter_timepiece_costs[self.player]

    def is_dlc1(self) -> bool:
        return self.multiworld.EnableDLC1[self.player].value > 0

    def is_dlc2(self) -> bool:
        return self.multiworld.EnableDLC2[self.player].value > 0

    def is_dw(self) -> bool:
        return self.multiworld.EnableDeathWish[self.player].value > 0

    def is_dw_only(self) -> bool:
        return self.is_dw() and self.multiworld.DeathWishOnly[self.player].value > 0

    def get_excluded_dws(self):
        return excluded_dws[self.player]

    def get_excluded_bonuses(self):
        return excluded_bonuses[self.player]

    def is_dw_excluded(self, name: str) -> bool:
        # don't exclude Seal the Deal if it's our goal
        if self.multiworld.EndGoal[self.player].value == 3 and name == "Seal the Deal" \
           and f"{name} - Main Objective" not in self.multiworld.exclude_locations[self.player]:
            return False

        if name in excluded_dws[self.player]:
            return True

        return f"{name} - Main Objective" in self.multiworld.exclude_locations[self.player]

    def is_bonus_excluded(self, name: str) -> bool:
        if self.is_dw_excluded(name) or name in excluded_bonuses[self.player]:
            return True

        return f"{name} - All Clear" in self.multiworld.exclude_locations[self.player]

    def get_dw_shuffle(self):
        return dw_shuffle[self.player]

    def set_dw_shuffle(self, shuffle: List[str]):
        dw_shuffle[self.player] = shuffle

    def get_badge_seller_count(self) -> int:
        return badge_seller_count[self.player]

    def set_badge_seller_count(self, value: int):
        badge_seller_count[self.player] = value

    def get_nyakuza_thug_items(self):
        return nyakuza_thug_items[self.player]

    def set_nyakuza_thug_items(self, items: Dict[str, int]):
        nyakuza_thug_items[self.player] = items
