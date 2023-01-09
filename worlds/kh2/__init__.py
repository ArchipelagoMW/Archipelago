from .Options import KH2_Options
from Utils import get_options, output_path
import json
import os
from msilib import Table
import random
import typing
import worlds.Files
from ..AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from ..generic.Rules import set_rule, add_rule, forbid_item, add_item_rule, item_in_locations
from .Items import ActionAbility_Table, KH2Item, item_dictionary_table, exclusionItem_table, \
    keybladeAbilities, donaldAbility, goofyAbility,lookup_id_to_name
from .Locations import all_locations, setup_locations, exclusion_table, lookup_id_to_Location
from .Rules import set_rules
from .logic import KH2Logic
from .Names import ItemName, LocationName
from .Regions import create_regions, connect_regions
from .OpenKH import patch_kh2


import unittest
from worlds.AutoWorld import AutoWorldRegister
from test.general import setup_default_world

class KingdomHearts2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokemon Red and Blue with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Alchav"]
    )]



class KH2World(World):
    game: str = "Kingdom Hearts 2"

    data_version  = 0
    option_definitions = KH2_Options
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = False
    #player = world.player
    #multiworld = world.multiworld
    remote_start_inventory: bool = False
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    lookup_id_to_Location: typing.Dict[int, str] = {data.code: item_name for item_name, data in all_locations.items() if
                                                data.code}
    location_name_to_id = {item_name: data.code for item_name, data in all_locations.items() if data.code}
    totallocations=629
    #multiworld locations that are checked in the client using the B10 anchor
    bt10multiworld_locaions= list()
    #multiworld locations that are checked in the client using the save anchor
    savemultiworld_locations= list()
      
    def _get_slot_data(self):
        return {
            "bt10multiworld_lociations":self.bt10multiworld_locaions,
            "sysmultiworld_locaitions":self.savemultiworld_locations,
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in KH2_Options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value
        return slot_data

    def _create_items(self, name: str):

        data = item_dictionary_table[name]
        return [self.create_item(name)] * data.quantity

    def create_item(self, name: str, ) -> Item:
        data = item_dictionary_table[name]
        if name in Items.Progression_Table or name in Items.Movement_Table or name in Items.Forms_Table or name in Items.Magic_Table or name == ItemName.Victory:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.filler

        created_item = KH2Item(name, item_classification, data, self.player)

        return created_item
    def pre_fill(self):
        # Placing Abilitys on keyblades
        # Just support abilities not action
        soraabilitycopy=keybladeAbilities.copy()
        for keyblade in exclusion_table["KeybladeSlot"]:
            randomAbility = self.multiworld.random.choice(soraabilitycopy)
            self.multiworld.get_location(keyblade, self.player).place_locked_item(self.create_item(randomAbility))
            self.exclude.add(randomAbility)
            soraabilitycopy.remove(randomAbility)
            self.totallocations -= 1

         #Goofy and Donald locaitons/abilites are static and always local.
         #So no self.totallocations-=1 for them

         #Placing Donald Abilities on donald locations
        donaldabilitycopy=donaldAbility.copy()
        for DonaldLoc in exclusion_table["DonaldLoc"]:
            randomAbility = self.multiworld.random.choice(donaldabilitycopy)
            self.multiworld.get_location(DonaldLoc, self.player).place_locked_item(self.create_item(randomAbility))
            self.exclude.add(randomAbility)
            donaldabilitycopy.remove(randomAbility)
#
        # Placing Goofy Abilites on goofy locaitons
        goofyabilitycopy=keybladeAbilities.copy()
        for GoofyLoc in exclusion_table["GoofyLoc"]:
            randomAbility = self.multiworld.random.choice(goofyabilitycopy)
            self.multiworld.get_location(GoofyLoc, self.player).place_locked_item(self.create_item(randomAbility))
            self.exclude.add(randomAbility)
            goofyabilitycopy.remove(randomAbility)
#
        # there is no such thing as lvl 1 but there needs to be a "location" for mod writing reasons
        for lvl in {LocationName.Valorlvl1, LocationName.Wisdomlvl1, LocationName.Limitlvl1, LocationName.Masterlvl1,
                    LocationName.Finallvl1}:
            self.multiworld.get_location(lvl, self.player).place_locked_item(self.create_item(ItemName.Nothing))
            self.totallocations -= 1
            

    def generate_basic(self):
        itempool: typing.List[KH2Item] = []

        
        fillerItems = [ItemName.Potion, ItemName.HiPotion, ItemName.Ether, ItemName.Elixir, 
                       ItemName.Megalixir, ItemName.Tent, ItemName.DriveRecovery,
                       ItemName.HighDriveRecovery, ItemName.PowerBoost,
                       ItemName.MagicBoost, ItemName.DefenseBoost, ItemName.APBoost]

        self.exclude = {"Victory", "Nothing"}
        self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(
            self.create_item(ItemName.Victory))
        self.totallocations -= 1

        # Option to turn off Promise Charm Item
        if self.multiworld.Promise_Charm[self.player].value == 0:
            self.exclude.add(ItemName.PromiseCharm)

        

        # Option to turn off all superbosses. Can do this individually but its like 20+ checks
        if self.multiworld.Super_Bosses[self.player].value == 0:
            for superboss in exclusion_table["SuperBosses"] and exclusion_table["Datas"]:
                self.multiworld.get_location(superboss, self.player).place_locked_item(
                    self.create_item(random.choice(fillerItems)))
                self.totallocations -= 1

        # Thse checks are missable
        self.multiworld.get_location(LocationName.JunkChampionBelt, self.player).place_locked_item(
            self.create_item(random.choice(fillerItems)))
        self.multiworld.get_location(LocationName.JunkMedal, self.player).place_locked_item(
            self.create_item(random.choice(fillerItems)))

        # starting with level 1 of all growth in the starting
        if self.multiworld.Schmovement[self.player].value == 1:
            for name in {ItemName.HighJump, ItemName.QuickRun, ItemName.DodgeRoll, ItemName.AerialDodge,
                         ItemName.Glide}:
                self.exclude.add(name)
                self.multiworld.push_precollected(self.create_item(name))

        # if option to have level checks up to level 50 place nothing on checks past 50

        if self.multiworld.Level_Depth[self.player].value == 1:
            exclustiontbl = exclusion_table["Level50"]
        else:
            exclustiontbl = exclusion_table["Level99"]

        for name in Locations.SoraLevels:
            if name not in exclustiontbl:
                self.multiworld.get_location(name, self.player).place_locked_item(self.create_item(ItemName.Nothing))
                self.totallocations -= 1

        # Creating the progression/ stat increases
        for x in range(4):
            itempool += [self.create_item(ItemName.TornPages)]
        for x in range(4):
            itempool += [self.create_item(ItemName.ItemSlotUp)]
        for x in range(19):
            itempool += [self.create_item(ItemName.MaxHPUp)]
        for x in range(3):
            itempool += [self.create_item(ItemName.MaxMPUp)]
        for x in range(5):
            itempool += [self.create_item(ItemName.DriveGaugeUp)]
        for x in range(2):
            itempool += [self.create_item(ItemName.ArmorSlotUp)]
            itempool += [self.create_item(ItemName.AccessorySlotUp)]
        for x in range(2):
            itempool += [self.create_item(ItemName.FireElement)]
            itempool += [self.create_item(ItemName.BlizzardElement)]
            itempool += [self.create_item(ItemName.ThunderElement)]
            itempool += [self.create_item(ItemName.CureElement)]
            itempool += [self.create_item(ItemName.MagnetElement)]
            itempool += [self.create_item(ItemName.ReflectElement)]

        for item in item_dictionary_table:
            if item not in self.exclude:
                itempool += self._create_items(item)

        # Creating filler for unfilled locations

        while len(itempool) - 1 <= self.totallocations:
            item = random.choice(fillerItems)
            itempool += [self.create_item(item)]
        self.multiworld.itempool += itempool

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)
        connect_regions(self.multiworld, self.player, self)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str):
        patch_kh2(self,output_directory)



#onframe

#loc>0 or whatever
#if location is picked up and location is in list of dummy14 stuff from slot data then send that check