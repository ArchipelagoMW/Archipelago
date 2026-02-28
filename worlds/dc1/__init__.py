import json
import pkgutil
import typing
from typing import Mapping, Any, Optional

from BaseClasses import Region, LocationProgressType, Item, CollectionState, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import set_rule

from .data import (NoruneGeoItems, MatatakiGeoItems, QueensGeoItems,
                   MuskaGeoItems, FactoryGeoItems, DHCGeoItems)
from . import Rules
from .Items import DarkCloudItem, ItemData
from .Location import DarkCloudLocation
from .Options import DarkCloudOptions
from .data.MiracleChest import MiracleChest
from .game_id import dc1_name

geo_funcs = [NoruneGeoItems.create_norune_atla, MatatakiGeoItems.create_matataki_atla,
             QueensGeoItems.create_queens_atla, MuskaGeoItems.create_muska_atla,
             FactoryGeoItems.create_factory_atla, DHCGeoItems.create_castle_atla]
geo_class = [NoruneGeoItems, MatatakiGeoItems, QueensGeoItems, MuskaGeoItems, FactoryGeoItems, DHCGeoItems]

dungeon_locations = json.loads(pkgutil.get_data(__name__, "data/atla_locations.json").decode())

# TODO webworld implementation as we get closer to completion.
class DarkCloudWeb(WebWorld):
    theme = "jungle"
    bug_report_page = ""
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Dark Cloud 1 for Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["EdricY"]
    )]

class DarkCloudWorld(World):
    """
    Two great continents, one an advanced civilization driven by progress and technology the other, where nature is the center of all existence and everyone lives harmoniously side by side. Two cultures that have never had contact with each other…until now.

    An ancient evil has been unleashed.
    Journey on a quest through time to unravel the mysterious tale of the Dark Cloud.
    """
    game = dc1_name
    required_client_version = (0, 6, 1)
    options_dataclass = Options.DarkCloudOptions
    options: Options.DarkCloudOptions
    topology_present = True
    web = DarkCloudWeb()

    item_name_to_id = {}
    location_name_to_id = {}
    item_name_to_classification = {}
    filler_item_names = []

    # Parse inventory item data
    item_data = [[],[],[],[],[]]
    reader = pkgutil.get_data(__name__, "data/item_data.csv").decode().splitlines()
    for line in reader:
        row = line.split(",")
        item_name_to_id.update({row[0]: int(row[1])})
        classification = ItemClassification(int(row[2]))
        if classification == ItemClassification.filler:
            filler_item_names.append(row[0])

        # [3]-[7] are counts if an item should be added for a given town 0-5.
        counts = []
        for i in range(3, 8):
            if row[i]:
                counts.append(int(row[i]))
            else:
                counts.append(0)

        item_data[0].append(ItemData(row[0], int(row[1]), classification, counts))

        item_name_to_classification[row[0]] = classification


    for i in geo_class:
        item_name_to_id.update(i.ids)
        item_name_to_classification.update(i.classifications)

    for i in dungeon_locations:
        location_name_to_id.update(i)

    # Parse in the miracle chest data
    mc_data = [[], [], [], [], []]
    reader = pkgutil.get_data(__name__, "data/miracle_locations.csv").decode().splitlines()
    for line in reader:
        row = line.split(",")
        mc_data[int(row[2])].append(MiracleChest(row[0], row[1], row[2], row[3], row[4]))

    for i in mc_data:
        for j in i:
            location_name_to_id.update({str(j.name): int(j.ap_id)})

    origin_region_name = "Norune"

    def create_items(self):
        for i in range(self.options.boss_goal):
            self.multiworld.itempool.extend(geo_funcs[i](self.options, self.player))

        if self.options.miracle_sanity:
            for i in range(min(5, int(self.options.boss_goal))):
                for item in self.item_data[i]:
                    self.multiworld.itempool.extend(item.to_items(self.player, self))

    # Set up progressive items
    def collect_item(self, state: "CollectionState", item: "Item", remove: bool = False) -> Optional[str]:
        if not item.advancement:
            return None
        name = item.name
        if name.startswith("Progressive "):
            prog_table = Items.progressive_item_list[name]
            if remove:
                for item_name in reversed(prog_table):
                    if state.has(item_name, item.player):
                        return item_name
            else:
                for item_name in prog_table:
                    if not state.has(item_name, item.player):
                        return item_name

        return super(DarkCloudWorld, self).collect_item(state, item, remove)

    def create_regions(self):
        regions: typing.Dict[str, Region] = {}

        # Towns
        norune = Region("Norune", self.player, self.multiworld)
        matataki = Region("Matataki", self.player, self.multiworld)
        queens = Region("Queens", self.player, self.multiworld)
        muska = Region("Muska", self.player, self.multiworld)
        factory = Region("Factory", self.player, self.multiworld)
        dhc = Region("DHC", self.player, self.multiworld)

        # Dungeons
        dbc1 = Region("DBC1", self.player, self.multiworld)
        dbc2 = Region("DBC2", self.player, self.multiworld)
        wof1 = Region("WOF1", self.player, self.multiworld)
        wof2 = Region("WOF2", self.player, self.multiworld)
        sr1 = Region("SR1", self.player, self.multiworld)
        sr2 = Region("SR2", self.player, self.multiworld)
        smt1 = Region("SMT1", self.player, self.multiworld)
        smt2 = Region("SMT2", self.player, self.multiworld)
        ms1 = Region("MS1", self.player, self.multiworld)
        ms2 = Region("MS2", self.player, self.multiworld)
        got = Region("GOT", self.player, self.multiworld)

        towns = [norune, matataki, queens, muska, factory, dhc]
        dungeons = [dbc1, dbc2, wof1, wof2, sr1, sr2, smt1, smt2, ms1, ms2, got]

        for town in towns:
            regions[town.name] = town

        for dungeon in dungeons:
            regions[dungeon.name] = dungeon

        # Only add locations for the relevant dungeons
        for i in range(min(len(dungeons), self.options.boss_goal * 2)):
            dun = dungeons[i]
            dun_locs = dungeon_locations[i]

            # Create locations, then add to the dungeons
            for key in dun_locs:
                loc = DarkCloudLocation(self.player, key, dun_locs[key], LocationProgressType.DEFAULT, dun)
                dun.locations.append(loc)

        if self.options.miracle_sanity:
            for i in range(min(5, int(self.options.boss_goal))):
                mcs = self.mc_data[i]
                for chest in mcs:
                    loc = DarkCloudLocation(self.player, str(chest.name), int(chest.ap_id),
                                            LocationProgressType.DEFAULT, towns[i])
                    loc.access_rule = lambda state, a=chest.req_char, b=chest.req_geo: Rules.chest_test(state,
                                                                                                        self.player, a,
                                                                                                        b)
                    towns[i].locations.append(loc)

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            regions[from_region].connect(regions[to_region])

        create_connection("Norune", "Matataki")
        create_connection("Norune", "Queens")
        create_connection("Norune", "Muska")
        create_connection("Norune", "Factory")
        create_connection("Norune", "DHC")

        create_connection("Norune", "DBC1")
        create_connection("Norune", "DBC2")

        create_connection("Matataki", "WOF1")
        create_connection("Matataki", "WOF2")

        create_connection("Queens", "SR1")
        create_connection("Queens", "SR2")

        create_connection("Muska", "SMT1")
        create_connection("Muska", "SMT2")

        create_connection("Factory", "MS1")
        create_connection("Factory", "MS2")

        create_connection("DHC", "GOT")

        self.multiworld.regions.extend(towns)
        self.multiworld.regions.extend(dungeons)

    def set_rules(self):

        set_rule(self.multiworld.get_entrance("Norune -> DBC1", self.player), lambda state: True)

        if hasattr(self.multiworld, "generation_is_fake"):  # UT doesn't need the shop for its logic
            set_rule(self.multiworld.get_entrance("Norune -> DBC2", self.player),
                     lambda state: Rules.xiao_available_ut(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Matataki", self.player),
                     lambda state: Rules.xiao_available_ut(state, self.player))
            set_rule(self.multiworld.get_entrance("Matataki -> WOF1", self.player),
                     lambda state: Rules.xiao_available_ut(state, self.player))
        else:
            set_rule(self.multiworld.get_entrance("Norune -> DBC2", self.player),
                     lambda state: Rules.xiao_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Matataki", self.player),
                     lambda state: Rules.xiao_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Matataki -> WOF1", self.player),
                     lambda state: Rules.xiao_available(state, self.player))

        if self.options.miracle_sanity and not hasattr(self.multiworld, "generation_is_fake"):
            set_rule(self.multiworld.get_entrance("Matataki -> WOF2", self.player),
                     lambda state: Rules.goro_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Queens", self.player),
                     lambda state: Rules.goro_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Queens -> SR1", self.player),
                     lambda state: Rules.goro_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Queens -> SR2", self.player),
                     lambda state: Rules.ruby_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Muska", self.player),
                     lambda state: Rules.ruby_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Muska -> SMT1", self.player),
                     lambda state: Rules.ruby_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Muska -> SMT2", self.player),
                     lambda state: Rules.ungaga_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Factory", self.player),
                     lambda state: Rules.ungaga_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Factory -> MS1", self.player),
                     lambda state: Rules.ungaga_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Factory -> MS2", self.player),
                     lambda state: Rules.osmond_available_items(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> DHC", self.player),
                     lambda state: Rules.got_accessible_items(state, self.player))
            set_rule(self.multiworld.get_entrance("DHC -> GOT", self.player),
                     lambda state: Rules.got_accessible_items(state, self.player))
        else:
            set_rule(self.multiworld.get_entrance("Matataki -> WOF2", self.player),
                     lambda state: Rules.goro_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Queens", self.player),
                     lambda state: Rules.goro_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Queens -> SR1", self.player),
                     lambda state: Rules.goro_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Queens -> SR2", self.player),
                     lambda state: Rules.ruby_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Muska", self.player),
                     lambda state: Rules.ruby_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Muska -> SMT1", self.player),
                     lambda state: Rules.ruby_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Muska -> SMT2", self.player),
                     lambda state: Rules.ungaga_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> Factory", self.player),
                     lambda state: Rules.ungaga_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Factory -> MS1", self.player),
                     lambda state: Rules.ungaga_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Factory -> MS2", self.player),
                     lambda state: Rules.osmond_available(state, self.player))
            set_rule(self.multiworld.get_entrance("Norune -> DHC", self.player),
                     lambda state: Rules.got_accessible(state, self.player))
            set_rule(self.multiworld.get_entrance("DHC -> GOT", self.player),
                     lambda state: Rules.got_accessible(state, self.player))

        # Set up completion goal
        match self.options.boss_goal:
            case 2:
                if self.options.all_bosses:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.two_bosses_items(state,
                                                                                                           self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.two_bosses(state,
                                                                                                           self.player)
                else:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.utan_access(state,
                                                                                                            self.player)\
                            and Rules.goro_available_items(state, self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.utan_access(state,
                                                                                                            self.player)\
                            and Rules.goro_available(state, self.player)
            case 3:
                if self.options.all_bosses:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.three_bosses_items(state,
                                                                                                             self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.three_bosses(state,
                                                                                                             self.player)
                else:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.saia_access(state,
                                                                                                            self.player)\
                                                        and Rules.ruby_available_items(state, self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.saia_access(state,
                                                                                                            self.player)\
                                                        and Rules.ruby_available(state, self.player)
            case 4:
                if self.options.all_bosses:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.four_bosses_items(state,
                                                                                                            self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.four_bosses(state,
                                                                                                            self.player)
                else:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.curse_access(state,
                                                                                                             self.player)\
                                                and Rules.ungaga_available_items(state, self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.curse_access(state,
                                                                                                             self.player)\
                                                and Rules.ungaga_available(state, self.player)
            case 5:
                if self.options.all_bosses:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.five_bosses_items(state,
                                                                                                            self.player)
                    else:

                        self.multiworld.completion_condition[self.player] = lambda state: Rules.five_bosses(state,
                                                                                                        self.player)
                else:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.joe_access(state,
                                                                                                       self.player)\
                                                                                          and Rules.osmond_available_items(
                            state, self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.joe_access(state,
                                                                                                       self.player)\
                                                                                          and Rules.osmond_available(
                            state, self.player)
            case 6:
                if self.options.all_bosses:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.six_bosses_items(state,
                                                                                                           self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.six_bosses(state,
                                                                                                           self.player)
                else:
                    if self.options.miracle_sanity:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.genie_access(state,
                                                                                                         self.player) \
                                                                                      and Rules.osmond_available_items(
                                                                                                state, self.player)
                    else:
                        self.multiworld.completion_condition[self.player] = lambda state: Rules.genie_access(state,
                                                                                                         self.player) \
                                                                                      and Rules.osmond_available(
                                                                                                state, self.player)
    def create_item(self, name:str) -> DarkCloudItem:
        classification = self.item_name_to_classification[name]
        return DarkCloudItem(name, classification, self.item_name_to_id[name], self.player)

    def get_filler_item_name(self) -> str:
        return self.filler_item_names[self.random.randint(0, len(self.filler_item_names) - 1)]

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = {
            "options": {
                "goal": self.options.boss_goal.value,
                "all_bosses": self.options.all_bosses.value,
                "open_dungeon": self.options.open_dungeon.value,
                "starter_weapons": self.options.starter_weapons.value,
                "abs_multiplier": self.options.abs_multiplier.value,
                "attach_multiplier": self.options.attach_multiplier.value,
                "attach_mult_config": self.options.attach_mult_config.value,
                "auto_build": self.options.auto_build.value,
                "miracle_sanity": self.options.miracle_sanity.value,
                "death_link": self.options.death_link.value,
            },
        }

        return slot_data
