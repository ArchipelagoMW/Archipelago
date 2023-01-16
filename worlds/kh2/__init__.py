from .Options import KH2_Options
import random
import typing
from ..AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, ItemClassification
from .Items import  KH2Item, item_dictionary_table, \
    keybladeAbilities, donaldAbility, goofyAbility
from .Locations import all_locations, setup_locations, exclusion_table,Donald_Checks,Goofy_Checks,Keyblade_Slots
from .Rules import set_rules
from .logic import KH2Logic
from .Names import ItemName, LocationName
from .Regions import create_regions, connect_regions
from .OpenKH import patch_kh2


class KingdomHearts2Web(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Kingdom Hearts 2 Final Mix with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["JaredWeakStrike"]
    )]



class KH2World(World):
    game: str = "Kingdom Hearts 2"

    data_version  = 0
    option_definitions = KH2_Options
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = False
    remote_start_inventory: bool = False
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    location_name_to_id = {item_name: data.code for item_name, data in all_locations.items() if data.code}
    totallocations=len(all_locations.items())-78

    #multiworld locations that are checked in the client using the save anchor
    kh2multiworld_locations= list()
      
    def _get_slot_data(self):
        return {
            "kh2multiworld_locations":self.kh2multiworld_locations,
            #todo: add starting invo 
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in KH2_Options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value
        return slot_data


    def create_item(self, name: str, ) -> Item:
        data = item_dictionary_table[name]
        if name in Items.Progression_Table or name in Items.Movement_Table or name in Items.Forms_Table or name in Items.Magic_Table or name == ItemName.Victory:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.filler

        created_item = KH2Item(name, item_classification, data.code, self.player)

        return created_item

        

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

        #probably could add these into generate early but its fine here currently
        #creats a copy of the lists so the tests are okay with running them twice even though they would never be ran twice 
        soraabilitycopy=keybladeAbilities.copy()
        for keyblade in Keyblade_Slots:
            randomAbility = self.multiworld.random.choice(soraabilitycopy)
            self.multiworld.get_location(keyblade, self.player).place_locked_item(self.create_item(randomAbility))
            self.exclude.add(randomAbility)
            soraabilitycopy.remove(randomAbility)
            self.totallocations -= 1
         #Placing Donald Abilities on donald locations
        donaldabilitycopy=donaldAbility.copy()
        for DonaldLoc in Donald_Checks:
            randomAbility = self.multiworld.random.choice(donaldabilitycopy)
            self.multiworld.get_location(DonaldLoc, self.player).place_locked_item(self.create_item(randomAbility))
            self.exclude.add(randomAbility)
            donaldabilitycopy.remove(randomAbility)
            self.totallocations -= 1

        # Placing Goofy Abilites on goofy locaitons
        goofyabilitycopy=goofyAbility.copy()
        for GoofyLoc in Goofy_Checks:
            randomAbility = self.multiworld.random.choice(goofyabilitycopy)
            self.multiworld.get_location(GoofyLoc, self.player).place_locked_item(self.create_item(randomAbility))
            self.exclude.add(randomAbility)
            goofyabilitycopy.remove(randomAbility)
            self.totallocations -= 1    

        # there is no such thing as lvl 1 but there needs to be a "location" for mod writing reasons
        for lvl in {LocationName.Valorlvl1, LocationName.Wisdomlvl1, LocationName.Limitlvl1, LocationName.Masterlvl1,
                    LocationName.Finallvl1}:
            self.multiworld.get_location(lvl, self.player).place_locked_item(self.create_item(ItemName.Victory))
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

        # These checks are missable
        self.multiworld.get_location(LocationName.JunkChampionBelt, self.player).place_locked_item(
            self.create_item(random.choice(fillerItems)))
        self.multiworld.get_location(LocationName.JunkMedal, self.player).place_locked_item(
            self.create_item(random.choice(fillerItems)))
        self.totallocations -= 2

        # starting with level 1 of all growth in the starting
        if self.multiworld.Schmovement[self.player].value == 1:
            for name in {ItemName.HighJump, ItemName.QuickRun, ItemName.DodgeRoll, ItemName.AerialDodge,
                         ItemName.Glide}:
                self.exclude.add(name)
                self.multiworld.push_precollected(self.create_item(name))


        # if option to have level checks up to level 50 place nothing on checks past 50
        #if self.multiworld.Level_Depth[self.player].value == 1:
        #    exclustiontbl = exclusion_table["Level50"]
        #else:
        #    exclustiontbl = exclusion_table["Level99"]
        #
        #for name in Locations.SoraLevels:
        #    if name not in exclustiontbl:
        #        self.multiworld.get_location(name, self.player).place_locked_item(self.create_item(ItemName.Nothing))
        #        self.totallocations -= 1


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
                itempool.append(self.create_item(item)) 

        # Creating filler for unfilled locations
        while len(itempool) <= self.totallocations:
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

