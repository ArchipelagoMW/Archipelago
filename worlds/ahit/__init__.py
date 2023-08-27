from BaseClasses import Item, ItemClassification, Region, LocationProgressType

from .Items import HatInTimeItem, item_table, item_frequencies, item_dlc_enabled, junk_weights,\
    create_item, create_multiple_items, create_junk_items, relic_groups, act_contracts, alps_hooks, \
    get_total_time_pieces

from .Regions import create_region, create_regions, connect_regions, randomize_act_entrances, chapter_act_info, \
    create_events, chapter_regions, act_chapters

from .Locations import HatInTimeLocation, location_table, get_total_locations, contract_locations, is_location_valid, \
    get_location_names

from .Types import HatDLC, HatType, ChapterIndex
from .Options import ahit_options, slot_data_options, adjust_options
from worlds.AutoWorld import World
from .Rules import set_rules
import typing


class HatInTimeWorld(World):
    """
    A Hat in Time is a cute-as-heck 3D platformer featuring a little girl who stitches hats for wicked powers!
    Freely explore giant worlds and recover Time Pieces to travel to new heights!
    """

    game = "A Hat in Time"
    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = get_location_names()

    option_definitions = ahit_options

    hat_craft_order: typing.List[HatType]
    hat_yarn_costs: typing.Dict[HatType, int]
    chapter_timepiece_costs: typing.Dict[ChapterIndex, int]
    act_connections: typing.Dict[str, str] = {}
    nyakuza_thug_items: typing.Dict[str, int] = {}
    shop_locs: typing.List[str] = []
    item_name_groups = relic_groups
    badge_seller_count: int = 0

    def generate_early(self):
        adjust_options(self)

        # If our starting chapter is 4 and act rando isn't on, force hookshot into inventory
        # If starting chapter is 3 and painting shuffle is enabled, and act rando isn't, give one free painting unlock
        start_chapter: int = self.multiworld.StartingChapter[self.player].value

        if start_chapter == 4 or start_chapter == 3:
            if self.multiworld.ActRandomizer[self.player].value == 0:
                if start_chapter == 4:
                    self.multiworld.push_precollected(self.create_item("Hookshot Badge"))

                if start_chapter == 3 and self.multiworld.ShuffleSubconPaintings[self.player].value > 0:
                    self.multiworld.push_precollected(self.create_item("Progressive Painting Unlock"))

        if self.multiworld.StartWithCompassBadge[self.player].value > 0:
            self.multiworld.push_precollected(self.create_item("Compass Badge"))

    def create_regions(self):
        self.nyakuza_thug_items = {}
        self.shop_locs = []
        create_regions(self)

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
        self.hat_yarn_costs = {HatType.SPRINT: -1, HatType.BREWING: -1, HatType.ICE: -1,
                               HatType.DWELLER: -1, HatType.TIME_STOP: -1}

        self.hat_craft_order = [HatType.SPRINT, HatType.BREWING, HatType.ICE,
                                HatType.DWELLER, HatType.TIME_STOP]

        self.topology_present = self.multiworld.ActRandomizer[self.player].value

        # Item Pool
        itempool: typing.List[Item] = []
        self.calculate_yarn_costs()
        yarn_pool: typing.List[Item] = create_multiple_items(self, "Yarn", self.multiworld.YarnAvailable[self.player].value)

        # 1/5 is progression balanced
        for i in range(len(yarn_pool) // 5):
            yarn_pool[i].classification = ItemClassification.progression

        itempool += yarn_pool

        if self.multiworld.RandomizeHatOrder[self.player].value > 0:
            self.multiworld.random.shuffle(self.hat_craft_order)

        for name in item_table.keys():
            if name == "Yarn":
                continue

            if not item_dlc_enabled(self, name):
                continue

            item_type: ItemClassification = item_table.get(name).classification
            if item_type is ItemClassification.filler or item_type is ItemClassification.trap:
                continue

            if name in act_contracts.keys() and self.multiworld.ShuffleActContracts[self.player].value == 0:
                continue

            if name in alps_hooks.keys() and self.multiworld.ShuffleAlpineZiplines[self.player].value == 0:
                continue

            if name == "Progressive Painting Unlock" \
               and self.multiworld.ShuffleSubconPaintings[self.player].value == 0:
                continue

            if name == "Time Piece":
                tp_count: int = 40
                max_extra: int = 0
                if self.multiworld.EnableDLC1[self.player].value > 0:
                    max_extra += 6

                if self.multiworld.EnableDLC2[self.player].value > 0:
                    max_extra += 10

                tp_count += min(max_extra, self.multiworld.MaxExtraTimePieces[self.player].value)
                tp_list: typing.List[Item] = create_multiple_items(self, name, tp_count)

                # 1/5 is progression balanced
                for i in range(len(tp_list) // 5):
                    tp_list[i].classification = ItemClassification.progression

                itempool += tp_list
                continue

            itempool += create_multiple_items(self, name, item_frequencies.get(name, 1))

        create_events(self)
        total_locations: int = get_total_locations(self)
        itempool += create_junk_items(self, total_locations-len(itempool))
        self.multiworld.itempool += itempool

    def set_rules(self):
        self.act_connections = {}
        self.chapter_timepiece_costs = {ChapterIndex.MAFIA: -1,
                                        ChapterIndex.BIRDS: -1,
                                        ChapterIndex.SUBCON: -1,
                                        ChapterIndex.ALPINE: -1,
                                        ChapterIndex.FINALE: -1,
                                        ChapterIndex.CRUISE: -1,
                                        ChapterIndex.METRO: -1}

        if self.multiworld.ActRandomizer[self.player].value > 0:
            randomize_act_entrances(self)

        set_rules(self)

    def create_item(self, name: str) -> Item:
        return create_item(self, name)

    def fill_slot_data(self) -> dict:
        slot_data: dict = {"SprintYarnCost": self.hat_yarn_costs[HatType.SPRINT],
                           "BrewingYarnCost": self.hat_yarn_costs[HatType.BREWING],
                           "IceYarnCost": self.hat_yarn_costs[HatType.ICE],
                           "DwellerYarnCost": self.hat_yarn_costs[HatType.DWELLER],
                           "TimeStopYarnCost": self.hat_yarn_costs[HatType.TIME_STOP],
                           "Chapter1Cost": self.chapter_timepiece_costs[ChapterIndex.MAFIA],
                           "Chapter2Cost": self.chapter_timepiece_costs[ChapterIndex.BIRDS],
                           "Chapter3Cost": self.chapter_timepiece_costs[ChapterIndex.SUBCON],
                           "Chapter4Cost": self.chapter_timepiece_costs[ChapterIndex.ALPINE],
                           "Chapter5Cost": self.chapter_timepiece_costs[ChapterIndex.FINALE],
                           "Chapter6Cost": self.chapter_timepiece_costs[ChapterIndex.CRUISE],
                           "Chapter7Cost": self.chapter_timepiece_costs[ChapterIndex.METRO],
                           "Hat1": int(self.hat_craft_order[0]),
                           "Hat2": int(self.hat_craft_order[1]),
                           "Hat3": int(self.hat_craft_order[2]),
                           "Hat4": int(self.hat_craft_order[3]),
                           "Hat5": int(self.hat_craft_order[4]),
                           "BadgeSellerItemCount": self.badge_seller_count,
                           "SeedNumber": self.multiworld.seed}  # For shop prices

        if self.multiworld.ActRandomizer[self.player].value > 0:
            for name in self.act_connections.keys():
                slot_data[name] = self.act_connections[name]

        if self.multiworld.EnableDLC2[self.player].value > 0:
            for name in self.nyakuza_thug_items.keys():
                slot_data[name] = self.nyakuza_thug_items[name]

        for option_name in slot_data_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        new_hint_data = {}
        alpine_regions = ["The Birdhouse", "The Lava Cake", "The Windmill", "The Twilight Bell"]
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

            new_hint_data[location.address] = self.get_shuffled_region(region_name)

        if self.multiworld.EnableDLC1[self.player].value > 0 and self.multiworld.Tasksanity[self.player].value > 0:
            ship_shape_region = self.get_shuffled_region("Ship Shape")
            id_start: int = 300204
            for i in range(self.multiworld.TasksanityCheckCount[self.player].value):
                new_hint_data[id_start+i] = ship_shape_region

        hint_data[self.player] = new_hint_data

    def write_spoiler_header(self, spoiler_handle: typing.TextIO):
        for i in self.chapter_timepiece_costs.keys():
            spoiler_handle.write("Chapter %i Cost: %i\n" % (i, self.chapter_timepiece_costs[ChapterIndex(i)]))

        for hat in self.hat_craft_order:
            spoiler_handle.write("Hat Cost: %s: %i\n" % (hat, self.hat_yarn_costs[hat]))

    def calculate_yarn_costs(self):
        mw = self.multiworld
        p = self.player
        min_yarn_cost = int(min(mw.YarnCostMin[p].value, mw.YarnCostMax[p].value))
        max_yarn_cost = int(max(mw.YarnCostMin[p].value, mw.YarnCostMax[p].value))

        max_cost: int = 0
        for i in range(5):
            cost = mw.random.randint(min(min_yarn_cost, max_yarn_cost), max(max_yarn_cost, min_yarn_cost))
            self.hat_yarn_costs[HatType(i)] = cost
            max_cost += cost

        available_yarn = mw.YarnAvailable[p].value
        if max_cost > available_yarn:
            mw.YarnAvailable[p].value = max_cost
            available_yarn = max_cost

        # make sure we always have at least 8 extra
        if max_cost + 8 > available_yarn:
            mw.YarnAvailable[p].value += (max_cost + 8) - available_yarn

    def set_chapter_cost(self, chapter: ChapterIndex, cost: int):
        self.chapter_timepiece_costs[chapter] = cost

    def get_chapter_cost(self, chapter: ChapterIndex) -> int:
        return self.chapter_timepiece_costs.get(chapter)

    # Sets an act entrance in slot data by specifying the Hat_ChapterActInfo, to be used in-game
    def update_chapter_act_info(self, original_region: Region, new_region: Region):
        original_act_info = chapter_act_info[original_region.name]
        new_act_info = chapter_act_info[new_region.name]
        self.act_connections[original_act_info] = new_act_info

    def get_shuffled_region(self, region: str) -> str:
        ci: str = chapter_act_info[region]
        for key, val in self.act_connections.items():
            if val == ci:
                for name in chapter_act_info.keys():
                    if chapter_act_info[name] == key:
                        return name
