from .Options import FinalEXP, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,KH2_Options,Stats
from Utils import get_options, output_path
import json
import os
from msilib import Table
import random
import typing
from ..AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from ..generic.Rules import set_rule, add_rule, forbid_item, add_item_rule, item_in_locations
from .Items import ActionAbility_Table, KH2Item, ItemData, item_dictionary_table ,exclusionItem_table
from .Locations import all_locations, setup_locations,exclusion_table
from .Rules import set_rules
from .logic import KH2Logic
from .Names import ItemName , LocationName
from .Regions import create_regions,connect_regions
from .OpenKH import patch_kh2

class KingdomHearts2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago Kingdom Hearts 2 on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Marech"]
    )]

class KH2World(World):

    
    game: str="Kingdom Hearts 2"

    data_version = 0
    option_definitions = KH2_Options
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = False 
    remote_start_inventory: bool = False
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    location_name_to_id={item_name: data.code for item_name, data in all_locations.items() if data.code}
    item_name_to_kh2id={name:data.kh2id for name,data in item_dictionary_table.items()}

    def _get_slot_data(self):
        return {
            "FinalEXP": self.multiworld.Final_Form_Level[self.player].value,
            "MasterEXP": self.multiworld.Master_Form_Level[self.player].value,
            "WisdomEXP": self.multiworld.Wisdom_Form_Level[self.player].value,
            "ValorEXP": self.multiworld.Valor_Form_Level[self.player].value,
            "LimitEXP": self.multiworld.Limit_Form_Level[self.player].value,
            "Schmovement":self.multiworld.Schmovement[self.player].value,
            "Keyblade_Stats":self.multiworld.Keyblade[self.player].value,
            "Visit_locking":self.multiworld.Visit_locking[self.player].value,
            "Super_Bosses":self.multiworld.Super_Bosses[self.player].value,
            "Level_Depth":self.multiworld.Level_Depth[self.player].value,
            "Max_Logic":self.multiworld.Max_Logic[self.player].value,
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in KH2_Options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value
        return slot_data

    def _create_items(self, name: str):
        
        data = item_dictionary_table[name]
        return [self.create_item(name)]*data.quantity
    

    def create_item(self, name: str,) -> Item:
       data = item_dictionary_table[name]

       if name in Items.Progression_Table or name in Items.Movement_Table or name in Items.Forms_Table or name in Items.Magic_Table or name==ItemName.Victory:
            item_classification = ItemClassification.progression
       else:
            item_classification = ItemClassification.filler

       created_item = KH2Item(name, item_classification, data, self.player)

       return  created_item
    

        #for name in exclusionItem_table["Ability"]:
        #        self.multiworld.get_location(name, self.player).place_locked_item(self.create_item(ItemName.Nothing))
    def generate_basic(self):
        itempool: typing.List[KH2Item] = []
        #normally 626 but with Final Xemnas having Victory it is 625 
        #for some reason I have 2 to minus 2 so later I do not have surplus items
        totallocations=623


        self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(self.create_item(ItemName.Victory))
        self.exclude={"Victory","Nothing"}
        if self.multiworld.Schmovement[self.player].value==1:
            for name in{ItemName.HighJump,ItemName.QuickRun,ItemName.DodgeRoll,ItemName.AerialDodge,ItemName.Glide}:
                self.exclude.add(name)


        #if option to have level checks up to level 50 place nothing on checks past 50
        if self.multiworld.Level_Depth[self.player]:
            for name in exclusion_table["Level50"]:
                self.multiworld.get_location(name, self.player).place_locked_item(self.create_item(ItemName.Nothing))
                totallocations-=1
        #Creating the progression/ stat increases
        for x in range(5):
            itempool += [self.create_item(ItemName.ItemSlotUp)]
        for x in range(20):
            itempool += [self.create_item(ItemName.MaxHPUp)]     
        for x in range(4):
            itempool += [self.create_item(ItemName.MaxMPUp)]     
        for x in range(6):
            itempool += [self.create_item(ItemName.DriveGaugeUp)]  
        for x in range(2):
            itempool +=[self.create_item(ItemName.ArmorSlotUp)]  
            itempool +=[self.create_item(ItemName.AccessorySlotUp)]
            itempool +=[self.create_item(ItemName.FireElement)]
            itempool +=[self.create_item(ItemName.BlizzardElement)]
            itempool +=[self.create_item(ItemName.ThunderElement)]
            itempool +=[self.create_item(ItemName.CureElement)]
            itempool +=[self.create_item(ItemName.MagnetElement)]
            itempool +=[self.create_item(ItemName.ReflectElement)]     
        
        for item in item_dictionary_table:
            if item not in self.exclude:
                itempool += self._create_items(item)
            
        fillerItems=[ItemName.Potion,ItemName.HiPotion,ItemName.Ether,ItemName.Elixir,ItemName.MegaPotion,
            ItemName.MegaEther,ItemName.Megalixir,ItemName.Tent,ItemName.DriveRecovery,ItemName.HighDriveRecovery,ItemName.PowerBoost,
            ItemName.MagicBoost,ItemName.DefenseBoost,ItemName.APBoost]
        #Creating filler for unfilled locations
        while len(itempool)<=totallocations:
            item=random.choice(fillerItems)
            itempool+=[self.create_item(item)] 
        self.multiworld.itempool += itempool
         

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)
        connect_regions(self.multiworld, self.player,self)



    def set_rules(self):
        set_rules(self.multiworld, self.player)
        
    def generate_output(self, output_directory: str):
        patch_kh2(self.multiworld, self.player,self,output_directory)   
            


         
        


    