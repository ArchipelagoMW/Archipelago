import json
import pkgutil
import typing
from typing import Mapping, Any, Optional

from BaseClasses import Region, LocationProgressType, Item, CollectionState
from worlds.AutoWorld import World, WebWorld
from worlds.dc1.data import (NoruneGeoItems, MatatakiGeoItems, QueensGeoItems,
                             MuskaGeoItems, FactoryGeoItems, DHCGeoItems)
from worlds.generic.Rules import set_rule
from .Items import DarkCloudItem
from .Location import DarkCloudLocation
from .Options import DarkCloudOptions
from .Rules import RuleManager
from .game_id import dc1_name

geo_funcs = [NoruneGeoItems.create_norune_atla, MatatakiGeoItems.create_matataki_atla,
             QueensGeoItems.create_queens_atla, MuskaGeoItems.create_muska_atla,
             FactoryGeoItems.create_factory_atla, DHCGeoItems.create_castle_atla]
geo_class = [NoruneGeoItems, MatatakiGeoItems, QueensGeoItems, MuskaGeoItems, FactoryGeoItems, DHCGeoItems]

# TODO webworld implementation as we get closer to completion.
class DarkCloudWeb(WebWorld):
    theme = "partyTime"
    bug_report_page = ""


class DarkCloudWorld(World):
    """
    Dark Cloud 1
    """
    game = dc1_name
    required_client_version = (0, 6, 1)
    options_dataclass = DarkCloudOptions
    options: DarkCloudOptions
    topology_present = True
    web = DarkCloudWeb()

    item_name_to_id = {}
    location_name_to_id = {}

    for i in geo_class:
        item_name_to_id.update(i.ids)

    dungeon_locations = json.loads(pkgutil.get_data(__name__, "data/atla_locations.json").decode())
    for i in dungeon_locations:
        location_name_to_id.update(i)

    origin_region_name = "Norune"
  
    def generate_early(self) -> None:
        for i in range(self.options.boss_goal):
            self.multiworld.itempool.extend(geo_funcs[i](self.options, self.player))

    def create_items(self):
        pass

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

        dungeon_locations = json.loads(pkgutil.get_data(__name__, "data/atla_locations.json").decode())

        # Only add locations for the relevant dungeons
        for i in range(min(len(dungeons), self.options.boss_goal * 2)):
            dun = dungeons[i]
            dun_locs = dungeon_locations[i]

            # Create locations, then add to the dungeons
            for key in dun_locs:
                loc = DarkCloudLocation(self.player, key, dun_locs[key], LocationProgressType.DEFAULT, dun)
                dun.locations.append(loc)

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            # connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            # regions[from_region].exits.append(connection)
            regions[from_region].connect(regions[to_region])
            # connection.connect(regions[to_region])

         # TODO use create_connection?
        norune.connect(matataki)
        norune.connect(queens)
        norune.connect(muska)
        norune.connect(factory)
        norune.connect(dhc)

        norune.connect(dbc1)
        norune.connect(dbc2)

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
        rm = RuleManager()

        set_rule(self.multiworld.get_entrance("Norune -> DBC1", self.player), lambda state: True)
        set_rule(self.multiworld.get_entrance("Norune -> DBC2", self.player),
                 lambda state: rm.xiao_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Norune -> Matataki", self.player),
                 lambda state: rm.xiao_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Matataki -> WOF1", self.player),
                 lambda state: rm.xiao_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Matataki -> WOF2", self.player),
                 lambda state: rm.goro_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Norune -> Queens", self.player),
                 lambda state: rm.goro_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Queens -> SR1", self.player),
                 lambda state: rm.goro_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Queens -> SR2", self.player),
                 lambda state: rm.ruby_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Norune -> Muska", self.player),
                 lambda state: rm.ruby_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Muska -> SMT1", self.player),
                 lambda state: rm.ruby_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Muska -> SMT2", self.player),
                 lambda state: rm.ungaga_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Norune -> Factory", self.player),
                 lambda state: rm.ungaga_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Factory -> MS1", self.player),
                 lambda state: rm.ungaga_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Factory -> MS2", self.player),
                 lambda state: rm.osmond_available(state, self.player))
        set_rule(self.multiworld.get_entrance("Norune -> DHC", self.player),
                 lambda state: rm.got_accessible(state, self.player))
        set_rule(self.multiworld.get_entrance("DHC -> GOT", self.player),
                 lambda state: rm.got_accessible(state, self.player))

        # Set up completion goal
        #TODO put the options logic in the rule for each boss instead
        match self.options.boss_goal:
            case 2:
                if self.options.all_bosses:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.utan_accessible(state,
                                                                                                 self.player) and \
                                                                                      rm.dran_accessible(state,
                                                                                                 self.player)
                else:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.utan_accessible(state,
                                                                                                 self.player)
            case 3:
                if self.options.all_bosses:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.saia_accessible(state,
                                                                                                 self.player) and \
                                                                                      rm.utan_accessible(state,
                                                                                                 self.player) and \
                                                                                      rm.dran_accessible(state,
                                                                                                 self.player)
                else:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.saia_accessible(state,
                                                                                                 self.player)
            case 4:
                if self.options.all_bosses:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.curse_accessible(state,
                                                                                                 self.player) and \
                                                                                      rm.saia_accessible(state,
                                                                                                 self.player) and \
                                                                                      rm.utan_accessible(state,
                                                                                                 self.player) and \
                                                                                      rm.dran_accessible(state,
                                                                                                 self.player)
                else:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.curse_accessible(state,
                                                                                                 self.player)
            case 5:
                if self.options.all_bosses:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.joe_accessible(state,
                                                                                              self.player) and \
                                                                                      rm.curse_accessible(state,
                                                                                              self.player) and \
                                                                                      rm.saia_accessible(state,
                                                                                              self.player) and \
                                                                                      rm.utan_accessible(state,
                                                                                              self.player) and \
                                                                                      rm.dran_accessible(state,
                                                                                              self.player)
                else:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.joe_accessible(state,
                                                                                              self.player)
            case 6:
                if self.options.all_bosses:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.genie_accessible(state,
                                                                                              self.player) and \
                                                                    rm.joe_accessible(state,
                                                                                      self.player) and \
                                                                    rm.curse_accessible(state,
                                                                                        self.player) and \
                                                                    rm.saia_accessible(state,
                                                                                       self.player) and \
                                                                    rm.utan_accessible(state,
                                                                                       self.player) and \
                                                                    rm.dran_accessible(state,
                                                                                       self.player)
                else:
                    self.multiworld.completion_condition[self.player] = lambda state: rm.genie_accessible(state,
                                                                                              self.player)

    # TODO: ??
    def connect_entrances(self) -> None:
        pass

    def fill_slot_data(self) -> Mapping[str, Any]:

        slot_data = {
            "options": {
                "goal": self.options.boss_goal.value,
                "all_bosses": self.options.all_bosses.value,
                "open_dungeon": self.options.open_dungeon.value,
                "starter_weapons": self.options.starter_weapons.value,
                "abs_multiplier": self.options.abs_multiplier.value,
                "auto_build": self.options.auto_build.value,
            },
            "seed": self.multiworld.seed_name,
        }

        return slot_data

