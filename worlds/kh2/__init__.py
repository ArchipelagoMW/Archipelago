from .Options import KH2_Options
import random
import typing
from ..AutoWorld import World, WebWorld
from BaseClasses import Item, Tutorial, ItemClassification
from .Items import  KH2Item, item_dictionary_table
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
    totallocations=len(all_locations.items())

    #multiworld locations that are checked in the client using the save anchor
    StationOfCalling_locations= list()
     
    def _get_slot_data(self):
        return {
            "StationOfCalling_locations":self.StationOfCalling_locations,
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in KH2_Options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value
        return slot_data
    



    def create_item(self, name: str,) -> Item:
        data = item_dictionary_table[name]
        if name in Items.Progression_Table or name in Items.Movement_Table or name in Items.Forms_Table or name in Items.Magic_Table or name == ItemName.Victory:
            item_classification = ItemClassification.progression
        elif name in Items.SupportAbility_Table or name in Items.ActionAbility_Table:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        created_item = KH2Item(name, item_classification, data.code, self.player)

        return created_item

        

    def generate_basic(self):
        itempool: typing.List[KH2Item] = []
        self.exclude = {"Victory", "Nothing"}
        self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(
            self.create_item(ItemName.Victory))
        self.totallocations -= 1



        fillerItems = [ItemName.Potion, ItemName.HiPotion, ItemName.Ether, ItemName.Elixir, 
                       ItemName.Megalixir, ItemName.Tent, ItemName.DriveRecovery,
                       ItemName.HighDriveRecovery, ItemName.PowerBoost,
                       ItemName.MagicBoost, ItemName.DefenseBoost, ItemName.APBoost]
        ItemQuantityDict={}


        donaldItemPool=list()
        goofyItemPool=list()
        SoraKeybladeAbilityPool=list()


        if self.multiworld.Keyblade_Abilities[self.player].value==0:
            SoraKeybladeAbilityPool.extend(Items.SupportAbility_Table.keys())
        elif self.multiworld.Keyblade_Abilities[self.player].value==1:
            SoraKeybladeAbilityPool.extend(Items.ActionAbility_Table.keys())
        else:
            SoraKeybladeAbilityPool.extend(Items.ActionAbility_Table.keys())
            SoraKeybladeAbilityPool.extend(Items.SupportAbility_Table.keys())
        for ability in self.multiworld.BlacklistKeyblade[self.player].value:
            if ability in SoraKeybladeAbilityPool:
                SoraKeybladeAbilityPool.remove(ability)
        for item,data in Items.item_dictionary_table.items():
            ItemQuantityDict.update({item:data.quantity})     
        #add level balanceing
        for item in self.multiworld.start_inventory[self.player].value:
            data=item_dictionary_table[item]
            ItemQuantityDict.update({item:Items.item_dictionary_table[item].quantity-1})

        for item in Items.DonaldAbility_Table.keys():
            data=ItemQuantityDict[item]
            for x in range(data):
                donaldItemPool.append(item)
            self.exclude.add(item)
        while len(donaldItemPool)<len(Locations.Donald_Checks.keys()):
            donaldItemPool.append(self.multiworld.random.choice(donaldItemPool))

        for item in Items.GoofyAbility_Table.keys():
            data=ItemQuantityDict[item]
            for x in range(data):
                goofyItemPool.append(item)
            self.exclude.add(item)
        while len(goofyItemPool)<len(Items.GoofyAbility_Table.keys()):
            donaldItemPool.append(self.multiworld.random.choice(donaldItemPool))

        #probably could add these into generate early but its fine here currently
        #creats a copy of the lists so the tests are okay with running them twice even though they would never be ran twice
         
        KeyBladeSlotCopy=list(Locations.Keyblade_Slots.keys())
        while len(SoraKeybladeAbilityPool)<len(KeyBladeSlotCopy):
            SoraKeybladeAbilityPool.append(self.multiworld.random.choice(list(Items.SupportAbility_Table.keys())))
        for keyblade in KeyBladeSlotCopy:
            randomAbility = self.multiworld.random.choice(SoraKeybladeAbilityPool)
            self.multiworld.get_location(keyblade, self.player).place_locked_item(self.create_item(randomAbility))
            ItemQuantityDict.update({randomAbility:Items.item_dictionary_table[randomAbility].quantity-1})
            SoraKeybladeAbilityPool.remove(randomAbility)
            self.totallocations -= 1


        #Placing Donald Abilities on donald locations
        for donaldlocation in Locations.Donald_Checks.keys():
            randomAbility = self.multiworld.random.choice(donaldItemPool)
            self.multiworld.get_location(donaldlocation, self.player).place_locked_item(self.create_item(randomAbility))
            self.totallocations -= 1 
            donaldItemPool.remove(randomAbility)


        # Placing Goofy Abilites on goofy locaitons
        for goofyLocation in Locations.Goofy_Checks.keys():
            randomAbility = self.multiworld.random.choice(goofyItemPool)
            self.multiworld.get_location(goofyLocation, self.player).place_locked_item(self.create_item(randomAbility))
            self.totallocations -= 1 
            goofyItemPool.remove(randomAbility)

        if self.multiworld.Level_Depth[self.player].value == 4:
            ItemQuantityDict.update({ItemName.NoExperience:Items.item_dictionary_table[ItemName.NoExperience].quantity-1})
            self.multiworld.push_precollected(self.create_item(ItemName.NoExperience))


        # Option to turn off Promise Charm Item
        if self.multiworld.Promise_Charm[self.player].value == 0:
            self.exclude.add(ItemName.PromiseCharm)

        
        if self.multiworld.Visit_locking[self.player]==0:
            for item in {ItemName.BattlefieldsofWar ,ItemName.SwordoftheAncestor,ItemName.BeastsClaw,ItemName.BoneFist,ItemName.ProudFang,
                         ItemName.SkillandCrossbones,ItemName.Scimitar,ItemName.MembershipCard,ItemName.IceCream,ItemName.Picture,ItemName.WaytotheDawn,
                         ItemName.IdentityDisk, ItemName.Poster,ItemName.NamineSketches}:
                self.exclude.add(item)
                self.multiworld.push_precollected(self.create_item(item))

        # Option to turn off all superbosses. Can do this individually but its like 20+ checks
        if self.multiworld.Super_Bosses[self.player].value == 0:
            for superboss in exclusion_table["Datas"]:
                self.multiworld.get_location(superboss, self.player).place_locked_item(
                    self.create_item(random.choice(fillerItems)))
                self.totallocations -= 1
            for superboss in exclusion_table["SuperBosses"]:
                self.multiworld.get_location(superboss, self.player).place_locked_item(
                    self.create_item(random.choice(fillerItems)))
                self.totallocations -= 1

        # These checks are missable
        self.multiworld.get_location(LocationName.JunkChampionBelt, self.player).place_locked_item(
            self.create_item(random.choice(fillerItems)))
        self.multiworld.get_location(LocationName.JunkMedal, self.player).place_locked_item(
            self.create_item(random.choice(fillerItems)))
        self.totallocations -= 2
        #Makeing a copy of the total growth pool
        GrowthList=list()
        for x in range(4):
            GrowthList.extend(Items.Movement_Table.keys())

        if self.multiworld.Schmovement[self.player].value !=0:
               for x in range(self.multiworld.Schmovement[self.player].value):
                    for name in {ItemName.HighJump,ItemName.QuickRun,ItemName.DodgeRoll,ItemName.AerialDodge,ItemName.Glide}:
                        ItemQuantityDict.update({name:Items.item_dictionary_table[name].quantity-1})
                        GrowthList.remove(name)
                        self.multiworld.push_precollected(self.create_item(name))
        if self.multiworld.RandomGrowth[self.player].value!=0:
           for x in range(self.multiworld.RandomGrowth[self.player].value):
               #try catch in the instance of the user having max movement and wants too much growth
               try:
                   randomGrowth=self.multiworld.random.choice(GrowthList)
                   ItemQuantityDict.update({name:Items.item_dictionary_table[name].quantity-1})
                   GrowthList.remove(randomGrowth)
                   self.multiworld.push_precollected(self.create_item(name))
               except:
                   break

        



        #there are levels but level 1 is there to keep code clean
        if self.multiworld.Level_Depth[self.player].value == 2:
            #level 99 sanity
            self.totallocations-=1
        elif self.multiworld.Level_Depth[self.player].value == 3:
            #level 50 sanity
            self.totallocations-=50
        elif self.multiworld.Level_Depth[self.player].value == 4:
            #level 1. No checks on levels
            self.totallocations-=99
        else:
            #level 50/99 since they contain the same amount of levels
            self.totallocations-=76

                    
        for item in item_dictionary_table:
            if item not in self.exclude:
                data=ItemQuantityDict[item]
                for x in range(data):
                    itempool.append(self.create_item(item))
                    ItemQuantityDict.update({item:Items.item_dictionary_table[item].quantity-1})

        # Creating filler for unfilled locations
        while len(itempool) < self.totallocations:
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

