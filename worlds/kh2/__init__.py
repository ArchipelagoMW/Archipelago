from .Options import FinalEXP, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,KH2_Options,Stats
from Utils import get_options, output_path
import json
import os
from msilib import Table
import typing
from ..AutoWorld import World, WebWorld
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from ..generic.Rules import set_rule, add_rule, forbid_item, add_item_rule, item_in_locations
<<<<<<< HEAD
<<<<<<< HEAD
from .Items import ActionAbility_Table, KH2Item, ItemData, item_dictionary_table, exclusionItem_table
from .Locations import all_locations, setup_locations,exclusion_table, corChecks
=======
from .Items import ActionAbility_Table, KH2Item, ItemData, item_dictionary_table
from .Locations import all_locations, setup_locations,exclusion_table
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
=======
from .Items import ActionAbility_Table, KH2Item, ItemData, item_dictionary_table
from .Locations import all_locations, setup_locations,exclusion_table
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
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
    option_definitions = KH2_Options
    data_version = 0
<<<<<<< HEAD
<<<<<<< HEAD
    #ItemName = {}
    #ChestLocation = {}
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = False 
    remote_start_inventory: bool = True
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    location_name_to_id={item_name: data.code for item_name, data in all_locations.items() if data.code}
    item_name_to_kh2id={name:data.kh2id for name,data in item_dictionary_table.items()}
    
    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in KH2_Options:
            option = getattr(self.multiworld, option_name)[self.player]
=======
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
    ItemName = {}
    ChestLocation = {}
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = False 
    remote_start_inventory: bool = False
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    location_name_to_id={item_name: data.code for item_name, data in all_locations.items() if data.code}
    item_name_to_kh2id={name:data.kh2id for name,data in item_dictionary_table.items()}
    def _get_slot_data(self):
        return {
            "FinalEXP": self.world.Final_Form_Level[self.player].value,
            "MasterEXP": self.world.Master_Form_Level[self.player].value,
            "WisdomEXP": self.world.Wisdom_Form_Level[self.player].value,
            "ValorEXP": self.world.Valor_Form_Level[self.player].value,
            "LimitEXP": self.world.Limit_Form_Level[self.player].value,
            "Schmovement":self.world.Schmovement[self.player].value,
            "Keyblade_Stats":self.world.Keyblade[self.player].value,
            "Visit_locking":self.world.Visit_locking[self.player].value,
            "Super_Bosses":self.world.Super_Bosses[self.player].value,
            "Level_Depth":self.world.Level_Depth[self.player].value,
        }
    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in KH2_Options:
            option = getattr(self.world, option_name)[self.player]
<<<<<<< HEAD
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
            slot_data[option_name] = option.value
        print(slot_data)
        return slot_data


    def _create_items(self, name: str):
<<<<<<< HEAD
<<<<<<< HEAD
        data = item_dictionary_table[name]
        return [self.create_item(name)]*data.quantity
    
    def create_event(self, event: str):
    # while we are at it, we can also add a helper to create events
        return KH2Item(event, ItemClassification.progression,True, self.player)

    def create_item(self, name: str,) -> Item:
       data = item_dictionary_table[name]
       if name in Items.Progression_Table or name in Items.Movement_Table or name in Items.Forms_Table or name in Items.Magic_Table or name=="Victory":
            item_classification = ItemClassification.progression
=======
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        
        data = item_dictionary_table[name]
        return [self.create_item(name)]*data.quantity
    

    def create_item(self, name: str,) -> Item:
       data = item_dictionary_table[name]

       if name in Items.Progression_Table or name in Items.Movement_Table or name in Items.Forms_Table or name in Items.Magic_Table:
            item_classification = ItemClassification.progression
       elif name in Items.Items_Table or name in Items.Reports_Table:
           item_classification = ItemClassification.filler
<<<<<<< HEAD
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
       else:
            item_classification = ItemClassification.filler

       created_item = KH2Item(name, item_classification, data, self.player)

       return  created_item
    
    

    def generate_basic(self):
        itempool: typing.List[KH2Item] = []
        #print(exclusion_table.Level50)
<<<<<<< HEAD
<<<<<<< HEAD
        self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(self.create_item(ItemName.Victory))
        #if self.multiworld.Level_Depth[self.player].value==1:
        #    for x in range(len(exclusion_table.popups)):
        #        self.multiworld.get_location(exclusion_table.level50, self.player).place_locked_item(self.create_item(ItemName.Potion))
        #self.multiworld.get_location(LocationName.Valorlvl7,self.player).place_located_item(self.create_item(ItemName.ProofofPeace))
        #for x in range(46):
        #    itempool+=[self.create_item(ItemName.Potion)]
        #for x in range(2):
        #    itempool += [self.create_item(ItemName.Ether)]
        #for x in range(4):
        #    itempool += [self.create_item(ItemName.MagicBoost)]
        #for x in range(35):
        #    itempool += [self.create_item(ItemName.DefenseBoost)]
        #    itempool += [self.create_item(ItemName.DriveRecovery)]
        #    itempool += [self.create_item(ItemName.PowerBoost)]
        #for x in range(60):
        #    itempool += [self.create_item(ItemName.APBoost)]          
        #for x in range(5):
        #    itempool += [self.create_item(ItemName.HighDriveRecovery)]
        #    itempool +=[self.create_item(ItemName.Megalixir)]
        #    itempool += [self.create_item(ItemName.Elixir)]
        #    itempool +=[self.create_item(ItemName.Tent)]
        #    itempool += [self.create_item(ItemName.ItemSlotUp)]
        #for x in range(20):
        #    itempool += [self.create_item(ItemName.MaxHPUp)]     
        #for x in range(4):
        #    itempool += [self.create_item(ItemName.MaxMPUp)]     
        #for x in range(6):
        #    itempool += [self.create_item(ItemName.DriveGaugeUp)]  
=======
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        print(self.world.Visit_locking[self.player].value)
        #if self.world.Level_Depth[self.player].value==1:
        #    for x in range(len(exclusion_table.popups)):
        #        self.world.get_location(exclusion_table.level50, self.player).place_locked_item(self.create_item(ItemName.Potion))
        #self.world.get_location(LocationName.Valorlvl7,self.player).place_located_item(self.create_item(ItemName.ProofofPeace))
        for x in range(46):
            itempool+=[self.create_item(ItemName.Potion)]
        for x in range(2):
            itempool += [self.create_item(ItemName.Ether)]
        for x in range(4):
            itempool += [self.create_item(ItemName.MagicBoost)]
        for x in range(35):
            itempool += [self.create_item(ItemName.DefenseBoost)]
            itempool += [self.create_item(ItemName.DriveRecovery)]
            itempool += [self.create_item(ItemName.PowerBoost)]
        for x in range(60):
            itempool += [self.create_item(ItemName.APBoost)]          
        for x in range(5):
            itempool += [self.create_item(ItemName.HighDriveRecovery)]
            itempool +=[self.create_item(ItemName.Megalixir)]
            itempool += [self.create_item(ItemName.Elixir)]
            itempool +=[self.create_item(ItemName.Tent)]
            itempool += [self.create_item(ItemName.ItemSlotUp)]
        for x in range(20):
            itempool += [self.create_item(ItemName.MaxHPUp)]     
        for x in range(4):
            itempool += [self.create_item(ItemName.MaxMPUp)]     
        for x in range(6):
            itempool += [self.create_item(ItemName.DriveGaugeUp)]  
<<<<<<< HEAD
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        for x in range(3):
            itempool += [self.create_item(ItemName.ArmorSlotUp)]  
            itempool += [self.create_item(ItemName.AccessorySlotUp)]
            itempool +=[self.create_item(ItemName.FireElement)]
            itempool +=[self.create_item(ItemName.BlizzardElement)]
            itempool +=[self.create_item(ItemName.ThunderElement)]
            itempool +=[self.create_item(ItemName.CureElement)]
            itempool +=[self.create_item(ItemName.MagnetElement)]
            itempool +=[self.create_item(ItemName.ReflectElement)]     
<<<<<<< HEAD
<<<<<<< HEAD
        exclude = [item for item in self.multiworld.KH2StartingItems[self.player].value]
        #if self.multiworld.Schmovement[self.player].value:
        #    exclude+=exclusionItem_table["Schmovement"]
        
        #For keyblade location
        #place locked item (random ablity)
        #place random ability in exclude

        print(exclude)
        print(corChecks)
        #print(self.multiworld.precollected_items)
        #print(exclusion_table["Level50"])    
        #self.multiworld.get_location(LocationName.CoRMineshaftUpperLevelAPBoost,self.player).place_locked_item(self.create_item(ItemName.ProofofPeace))
        for item in item_dictionary_table:
            if item =="Victory":
                #self.multiworld.get_location(LocationName.AbuEscort, self.player).place_locked_item(self.create_item(item))
                print(item)
            else:
                itempool += self._create_items(item)
        
        
        
        
        self.multiworld.itempool += itempool
        print(self.multiworld.get_filled_locations)
        print(self.multiworld.itempool)
    
        
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
            "KH2StartItems":self.multiworld.KH2StartingItems[self.player].value
        }

    def create_regions(self):
        location_table = setup_locations(self, self.player)
        create_regions(self, self.player, location_table)
        connect_regions(self, self.player,self)
        


    def set_rules(self):
        set_rules(self.multiworld, self.player)
        
    def generate_output(self, output_directory: str):
            world = self.multiworld
            player = self.player

            patch_kh2(self.multiworld, self.player,self,output_directory)   
=======
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
        
            
        for item in item_dictionary_table:
            itempool += self._create_items(item)

        
        
        
        self.world.itempool += itempool
     

    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)
        connect_regions(self.world, self.player,self)
        #region=self.world.get_region(LocationName.Ag2_Region,self.player)
        #print(self.world.get_entrance("Twlight Town",self.player))


    def set_rules(self):
        set_rules(self.world, self.player)
        
    def generate_output(self, output_directory: str):
            world = self.world
            player = self.player

            patch_kh2(self.world, self.player,self,output_directory)   
<<<<<<< HEAD
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
=======
>>>>>>> afa4bd2938ef788289864842bbffb250d8ac4b0a
            

        #except:
        #    raise
        #finally:
        #    if os.path.exists(rompath):
        #        os.unlink(rompath)
        #    self.rom_name_available_event.set() # make sure threading continues and errors are collected
         
        
    

    