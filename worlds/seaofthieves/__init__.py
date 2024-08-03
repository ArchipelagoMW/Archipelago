import os
import random

import Utils
import json
import typing

from .Items.Items import Items, SOTItem
from .Items.ItemCollection import ItemCollection
from .Items.ItemDetail import ItemDetail
from .Options import SOTOptions
from .Rules import set_rules
from BaseClasses import Location
from worlds.seaofthieves.Regions.Regions import create_regions
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from BaseClasses import Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Locations.LocationCollection import LocationDetailsCollection
from .Locations.LocationOptions import LocationOptions
from Fill import fill_restrictive
from .Regions.Regions import RegionAdder
from .Locations.Seals import Seals
from .Configurations import SotOptionsDerived
from .Locations.Menu import QuestMenu
import collections
from .ClientInput import ClientInput
from .Items.ItemAdder import create_items
from .Regions.RegionDetails import Regions
from .MultiworldHints import MultiworldHints
from .Website import SotWebWorld
from .Items.ItemCollection import ItemCollection
from .Hint import Hint, HintLibrary, hint_from_location
from .Client.Launcher.SotLauncherComponent import add_sot_to_client_laucher
import subprocess
import asyncio
import pickle

add_sot_to_client_laucher()


class SOTWorld(World):
    """ 
    A pirate game made by Rare
    """

    MAX_ISLANDS = 20  # number of hints
    game = "Sea of Thieves"
    topology_present = False

    web = SotWebWorld.SotWebWorld()

    sotOptionsDerived: SotOptionsDerived.SotOptionsDerived

    item_name_to_id = ItemCollection().getDict()

    # locationOptions: LocationOptions = LocationOptions()
    locationCollection = LocationDetailsCollection()
    locationCollection.random = random.Random()
    locationCollection.addAll()
    location_name_to_id = locationCollection.toDict()

    # location_name_to_id = {}
    data_version = 1
    options_dataclass = SOTOptions
    regionAdder: RegionAdder

    clientInputs: ClientInput = ClientInput()

    def generate_early(self) -> None:

        self.sotOptionsDerived = SotOptionsDerived.SotOptionsDerived(self.options)

        self.itemCollection = ItemCollection()
        self.itemCollection.getDict()  # loads the item collection

        self.sotOptionsDerived.player_name = self.multiworld.player_name[self.player]
        self.locationCollection = LocationDetailsCollection()
        self.locationCollection.applyOptions(self.sotOptionsDerived, self.random)
        self.locationCollection.addAll()
        # self.location_name_to_id = {} #self.locationCollection.toDict()

        return

    def pre_fill(self) -> None:
        self.pre_fill_sail()
        self.pre_fill_seals()

        return

    def create_regions(self):
        self.regionAdder: RegionAdder = create_regions(self.multiworld, self.sotOptionsDerived, self.player,
                                                       self.locationCollection)
        self.regionAdder.link_regions_and_locations()

    def set_rules(self):
        self.region_rules = set_rules(self.multiworld, self.sotOptionsDerived, self.player, self.regionAdder)

    def create_item(self, name: str) -> Item:
        item_id = self.item_name_to_id[name]
        item = SOTItem(name, ItemClassification.progression, item_id, self.player)
        return item

    def create_items(self):
        create_items(self.multiworld, len(self.location_name_to_id.keys()), self.sotOptionsDerived, self.itemCollection,
                     self.player)

    def get_filler_item_name(self) -> str:
        return self.itemCollection.getFillerItemName()

    def post_fill(self) -> None:
        pass




    def generate_output(self, output_directory: str):
        client_file = f"{self.multiworld.get_out_file_name_base(self.player)}.apsot"
        output_file_and_directory = os.path.join(output_directory, client_file)

        #Uses self.random based on function generate_output's comment
        self.clientInputs.sotOptionsDerived = self.sotOptionsDerived
        self.clientInputs.regionRules = self.region_rules
        self.clientInputs.shopWarehouse = self.locationCollection.shops
        self.clientInputs.shopWarehouse.remove_non_pickle_members()
        self.clientInputs.hintLibrary = self.buildHintLibrary().getStringLibrary(self.random)
        self.clientInputs.multiworldHints = MultiworldHints(self.multiworld, self.player, self.random, 50)
        self.clientInputs.to_file(output_file_and_directory)

    def pre_fill_seals(self) -> int:

        # right now we just have seals, so this works, but it wont soon

        seal_items = [
            SOTItem(Items.seal_gh.name, Items.seal_gh.classification, Items.seal_gh.id, self.player),
            SOTItem(Items.seal_ma.name, Items.seal_ma.classification, Items.seal_ma.id, self.player),
            SOTItem(Items.seal_af.name, Items.seal_af.classification, Items.seal_af.id, self.player),
            SOTItem(Items.seal_rb.name, Items.seal_rb.classification, Items.seal_rb.id, self.player),
            SOTItem(Items.seal_oos.name, Items.seal_oos.classification, Items.seal_oos.id, self.player)
        ]
        seal_locations = [
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_GH_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_MA_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_OOS_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_AF_TOTAL, self.player),
            self.multiworld.get_location(Seals.Seals.L_VOYAGE_COMP_RB_TOTAL, self.player)
        ]

        for i in seal_items:
            self.item_name_to_id[i.name] = i.code

        all_state = self.multiworld.get_all_state(use_cache=True)

        self.random.shuffle(seal_locations)

        fill_restrictive(self.multiworld, all_state, seal_locations, seal_items, True, lock=True,
                         name="SOT Seals")

        fod_location = self.multiworld.get_location(QuestMenu.MenuQuestAll.L_PIRATE_FOD, self.player)
        self.item_name_to_id[Items.pirate_legend.name] = Items.pirate_legend.id
        itm = self.create_item(Items.pirate_legend.name)
        fill_restrictive(self.multiworld, all_state, [fod_location], [itm], True, lock=True,
                         name="SOT Seals")

        return 5 + 1

    def buildHintLibrary(self) -> HintLibrary:
        hl = HintLibrary()
        for location in self.multiworld.get_locations(self.player):
            hint: Hint = hint_from_location(location)
            classification: HintLibrary.Type = HintLibrary.Type.PROGRESSIVE
            if location.item.classification == ItemClassification.filler:
                classification = HintLibrary.Type.FILLER
            elif location.item.classification == ItemClassification.trap:
                classification = HintLibrary.Type.TRAP
            hl.add(hint, classification)
        return hl
    def pre_fill_sail(self) -> int:

        itm = SOTItem(Items.sail.name, Items.sail.classification, Items.sail.id, self.player)
        sail_item_list: typing.List[SOTItem] = [itm]

        locs = []
        for loc in self.multiworld.get_locations(self.player):
            locs.append(loc)

        all_state = self.multiworld.get_all_state(use_cache=True)
        self.random.shuffle(locs)

        fill_restrictive(self.multiworld, all_state, locs, sail_item_list, True, lock=True,
                         name="SOT Sail")

        return 1
