from .Options import KH2_Options
from Utils import get_options, output_path
import json
import os
from msilib import Table
import random
import typing
from ..AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from ..generic.Rules import set_rule, add_rule, forbid_item, add_item_rule, item_in_locations
from .Items import ActionAbility_Table, KH2Item, ItemData, item_dictionary_table ,exclusionItem_table, abilities
from .Locations import all_locations, setup_locations,exclusion_table
from .Rules import set_rules
from .logic import KH2Logic
from .Names import ItemName , LocationName
from .Regions import create_regions,connect_regions
from .OpenKH import patch_kh2
from .XPValues import formExp 


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
            "SoraEXP": self.multiworld.Sora_Level_EXP[self.player].value,
            "FinalEXP": self.multiworld.Final_Form_EXP[self.player].value,
            "MasterEXP": self.multiworld.Master_Form_EXP[self.player].value,
            "WisdomEXP": self.multiworld.Wisdom_Form_EXP[self.player].value,
            "ValorEXP": self.multiworld.Valor_Form_EXP[self.player].value,
            "LimitEXP": self.multiworld.Limit_Form_EXP[self.player].value,
            "SummonEXP": self.multiworld.Summon_EXP[self.player].value,
            "Schmovement":self.multiworld.Schmovement[self.player].value,
            "Keyblade_Min":self.multiworld.Keyblade_Minimum[self.player].value,
            "Keyblade_Max":self.multiworld.Keyblade_Maximum[self.player].value,
            "Visit_locking":self.multiworld.Visit_locking[self.player].value,
            "Super_Bosses":self.multiworld.Super_Bosses[self.player].value,
            "Level_Depth":self.multiworld.Level_Depth[self.player].value,
            "Max_Logic":self.multiworld.Max_Logic[self.player].value,
            "Starting_Items":self.multiworld.Starting_Items[self.player].value
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
    


    def generate_basic(self):
        itempool: typing.List[KH2Item] = []

        totallocations=656
        fillerItems=[ItemName.Potion,ItemName.HiPotion,ItemName.Ether,ItemName.Elixir,ItemName.MegaPotion,
            ItemName.MegaEther,ItemName.Megalixir,ItemName.Tent,ItemName.DriveRecovery,ItemName.HighDriveRecovery,ItemName.PowerBoost,
            ItemName.MagicBoost,ItemName.DefenseBoost,ItemName.APBoost]


        self.exclude={"Victory","Nothing"}
        self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(self.create_item(ItemName.Victory))
        totallocations-=1
        
        for keyblade in exclusion_table["KeybladeSlot"]:
            randomAbility=abilities[random.randint(0, len(abilities)-1)]
            self.multiworld.get_location(keyblade, self.player).place_locked_item(self.create_item(randomAbility))
            self.exclude.add(randomAbility)
            abilities.remove(randomAbility)
            totallocations-=1

        #there is no such thing as lvl 1 but there needs to be a "location" for mod writing reasons
        for lvl in {LocationName.Valorlvl1,LocationName.Wisdomlvl1,LocationName.Limitlvl1,LocationName.Masterlvl1,LocationName.Finallvl1}:
            self.multiworld.get_location(lvl, self.player).place_locked_item(self.create_item(ItemName.Nothing))
            totallocations-=1


        if self.multiworld.Super_Bosses[self.player].value==0:
            for superboss in exclusion_table["SuperBosses"] and exclusion_table["Datas"]:
                self.multiworld.get_location(superboss, self.player).place_locked_item(self.create_item(random.choice(fillerItems)))   
                totallocations-=1

        if self.multiworld.Schmovement[self.player].value==1:
            for name in{ItemName.HighJump,ItemName.QuickRun,ItemName.DodgeRoll,ItemName.AerialDodge,ItemName.Glide}:
                self.exclude.add(name)


        if self.multiworld.Level_Depth[self.player].value==1:             
            exclustiontbl=exclusion_table["Level50"]
        else:
            exclustiontbl=exclusion_table["Level99"]
        #if option to have level checks up to level 50 place nothing on checks past 50
        for name in Locations.SoraLevels:
            if name not in exclustiontbl:
               self.multiworld.get_location(name, self.player).place_locked_item(self.create_item(ItemName.Nothing))
               totallocations-=1



        #Creating the progression/ stat increases
        for x in range(7):
            itempool += [self.create_item(ItemName.ItemSlotUp)]
        for x in range(20):
            itempool += [self.create_item(ItemName.MaxHPUp)]     
        for x in range(4):
            itempool += [self.create_item(ItemName.MaxMPUp)]     
        for x in range(6):
            itempool += [self.create_item(ItemName.DriveGaugeUp)]  
        for x in range(3):
            itempool +=[self.create_item(ItemName.ArmorSlotUp)]  
            itempool +=[self.create_item(ItemName.AccessorySlotUp)]
        for x in range(2):
            itempool +=[self.create_item(ItemName.FireElement)]
            itempool +=[self.create_item(ItemName.BlizzardElement)]
            itempool +=[self.create_item(ItemName.ThunderElement)]
            itempool +=[self.create_item(ItemName.CureElement)]
            itempool +=[self.create_item(ItemName.MagnetElement)]
            itempool +=[self.create_item(ItemName.ReflectElement)]     
        
        for item in item_dictionary_table:
            if item not in self.exclude:
             itempool += self._create_items(item)
            


        #Creating filler for unfilled locations
        
        while len(itempool)-1<totallocations:
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
            


         
        


    