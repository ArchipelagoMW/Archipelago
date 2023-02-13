import typing

from BaseClasses import Item, Tutorial, ItemClassification

from .Items import KH2Item, item_dictionary_table, exclusionItem_table, ProgressionItems
from .Locations import all_locations, setup_locations, exclusion_table
from .Names import ItemName, LocationName
from .OpenKH import patch_kh2
from .Options import KH2_Options
from .Regions import create_regions, connect_regions
from .Rules import set_rules
from ..AutoWorld import World, WebWorld
from .logic import KH2Logic


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
    web = KingdomHearts2Web()
    data_version = 0
    option_definitions = KH2_Options
    topology_present: bool = True  # show path to required location checks in spoiler
    remote_items: bool = False
    remote_start_inventory: bool = False
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    location_name_to_id = {item_name: data.code for item_name, data in all_locations.items() if data.code}
    totalLocations = len(all_locations.items())

    # hitlist for the bosses. This goes in slot data

    @staticmethod
    def _get_slot_data(self):
        return {"hitlist": self.hitlist}

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data(self)
        for option_name in KH2_Options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = option.value
        return slot_data

    def create_item(self, name: str, ) -> Item:
        data = item_dictionary_table[name]
        if name in ProgressionItems or name in Items.Misc_Table or name in Items.Staffs_Table or name in Items.Shields_Table:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.filler

        created_item = KH2Item(name, item_classification, data.code, self.player)

        return created_item

    def generate_early(self) -> None:
        # Option to turn off all superbosses. Can do this individually but its like 20+ checks
        if self.multiworld.SuperBosses[self.player].value == 0 and not self.multiworld.Goal[self.player].value == 2:
            for superboss in exclusion_table["Datas"]:
                self.multiworld.exclude_locations[self.player].value.add(superboss)
            for superboss in exclusion_table["SuperBosses"]:
                self.multiworld.exclude_locations[self.player].value.add(superboss)



        if self.multiworld.Cups[self.player].value == 1:
            for cup in exclusion_table["Cups"]:
                self.multiworld.exclude_locations[self.player].value.add(cup)


    def generate_basic(self):
        itempool: typing.List[KH2Item] = []
        self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(self.create_item(ItemName.Victory))
        self.totalLocations -= 1
        self.hitlist = list()
        RandomSuperBoss = list()
        filler_items = list()
        filler_items.extend(exclusionItem_table["Filler"])
        item_quantity_dict = {}
        donald_ability_pool = list()
        goofy_ability_pool = list()
        sora_keyblade_ability_pool = list()

        if self.multiworld.KeybladeAbilities[self.player].value == 0:
            sora_keyblade_ability_pool.extend(Items.SupportAbility_Table.keys())
        elif self.multiworld.KeybladeAbilities[self.player].value == 1:
            sora_keyblade_ability_pool.extend(Items.ActionAbility_Table.keys())
        else:
            sora_keyblade_ability_pool.extend(Items.ActionAbility_Table.keys())
            sora_keyblade_ability_pool.extend(Items.SupportAbility_Table.keys())

        for ability in self.multiworld.BlacklistKeyblade[self.player].value:
            if ability in sora_keyblade_ability_pool:
                sora_keyblade_ability_pool.remove(ability)
        for item, data in Items.item_dictionary_table.items():
            item_quantity_dict.update({item: data.quantity})

        if self.multiworld.Goal[self.player].value == 1:
            luckyemblemamount = self.multiworld.LuckyEmblemsAmount[self.player].value
            luckyemblemrequired = self.multiworld.LuckyEmblemsRequired[self.player].value
            if luckyemblemamount < luckyemblemrequired:
                luckyemblemamount = max(luckyemblemamount, luckyemblemrequired)
                print(f"Luckey Emblem Amount {self.multiworld.LuckyEmblemsAmount[self.player].value} is less than required \
            {(self.multiworld.LuckyEmblemsRequired[self.player].value)} for player {self.multiworld.get_file_safe_player_name(self.player)}")
            item_quantity_dict.update({ItemName.LuckyEmblem: Items.item_dictionary_table[ItemName.LuckyEmblem].quantity + luckyemblemamount})
            # give this proof to unlock the final door once the player has the amount of lucky emlblem required
            item_quantity_dict.update({ItemName.ProofofNonexistence: 0})
        # hitlist
        if self.multiworld.Goal[self.player].value == 2:
            RandomSuperBoss.extend(exclusion_table["Hitlist"])
            BountiesAmount =   self.multiworld.BountyAmount[self.player].value
            BountiesRequired = self.multiworld.BountyRequired[self.player].value

            for location in self.multiworld.exclude_locations[self.player].value:
                if location in RandomSuperBoss:
                    RandomSuperBoss.remove(location)

            if len(RandomSuperBoss) < BountiesAmount:
                print(f"{self.multiworld.get_file_safe_player_name(self.player)} has too many bounties than bosses")
                BountiesAmount=len(RandomSuperBoss)
                self.multiworld.BountyAmount[self.player].value=len(RandomSuperBoss)

            if len(RandomSuperBoss) < BountiesRequired:
                print(f"{self.multiworld.get_file_safe_player_name(self.player)} has too many required bounties")
                BountiesRequired=len(RandomSuperBoss)
                self.multiworld.BountyRequired[self.player].value=len(RandomSuperBoss)

            if BountiesAmount < BountiesRequired:
                BountiesAmount = max(BountiesAmount, BountiesRequired)
                print(f"Bounties Amount {self.multiworld.BountyAmount[self.player].value} is less than required \
                        {(self.multiworld.BountyRequired[self.player].value)} for player {self.multiworld.get_file_safe_player_name(self.player)}")

            for bounty in range(BountiesAmount):
                randomBoss = self.multiworld.per_slot_randoms[self.player].choice(RandomSuperBoss)
                self.multiworld.get_location(randomBoss, self.player).place_locked_item(
                        self.create_item(ItemName.Bounty))
                self.hitlist.append(self.location_name_to_id[randomBoss])
                RandomSuperBoss.remove(randomBoss)
                self.totalLocations -= 1
            self.multiworld.start_hints[self.player].value.add(ItemName.Bounty)
            item_quantity_dict.update({ItemName.ProofofNonexistence: 0})

        for item, value in self.multiworld.start_inventory[self.player].value.items():
            if item in Items.ActionAbility_Table.keys() or item in Items.SupportAbility_Table.keys():
                # cannot have more than the quantity for abilties
                if value > Items.item_dictionary_table[item].quantity:
                    print(f"{self.multiworld.get_file_safe_player_name(self.player)} cannot have more than {Items.item_dictionary_table[item].quantity} of {item}")
                item_quantity_dict.update({item: Items.item_dictionary_table[item].quantity - 1})

        for item in Items.DonaldAbility_Table.keys():
            data = item_quantity_dict[item]
            for x in range(data):
                donald_ability_pool.append(item)
            item_quantity_dict.update({item: 0})
        while len(donald_ability_pool) < len(Locations.Donald_Checks.keys()):
            donald_ability_pool.append(self.multiworld.per_slot_randoms[self.player].choice(donald_ability_pool))

        for item in Items.GoofyAbility_Table.keys():
            data = item_quantity_dict[item]
            for x in range(data):
                goofy_ability_pool.append(item)
            item_quantity_dict.update({item: 0})
        while len(goofy_ability_pool) < len(Items.GoofyAbility_Table.keys()):
            goofy_ability_pool.append(self.multiworld.per_slot_randoms[self.player].choice(goofy_ability_pool))

        # plando keyblades because they can only have abilites
        keyblade_slot_copy = list(Locations.Keyblade_Slots.keys())
        while len(sora_keyblade_ability_pool) < len(keyblade_slot_copy):
            sora_keyblade_ability_pool.append(
                    self.multiworld.per_slot_randoms[self.player].choice(list(Items.SupportAbility_Table.keys())))
        for keyblade in keyblade_slot_copy:
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(sora_keyblade_ability_pool)
            self.multiworld.get_location(keyblade, self.player).place_locked_item(self.create_item(random_ability))
            item_quantity_dict.update({random_ability: Items.item_dictionary_table[random_ability].quantity - 1})
            sora_keyblade_ability_pool.remove(random_ability)
            self.totalLocations -= 1

        # Placing Donald Abilities on donald locations
        for donaldLocation in Locations.Donald_Checks.keys():
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(donald_ability_pool)
            self.multiworld.get_location(donaldLocation, self.player).place_locked_item(
                    self.create_item(random_ability))
            self.totalLocations -= 1
            donald_ability_pool.remove(random_ability)

        # Placing Goofy Abilites on goofy locaitons
        for goofyLocation in Locations.Goofy_Checks.keys():
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(goofy_ability_pool)
            self.multiworld.get_location(goofyLocation, self.player).place_locked_item(self.create_item(random_ability))
            self.totalLocations -= 1
            goofy_ability_pool.remove(random_ability)

        # Option to turn off Promise Charm Item
        if self.multiworld.Promise_Charm[self.player].value == 0:
            item_quantity_dict.update({ItemName.PromiseCharm: 0})


        # same item placed because you can only get one of these 2 locations
        # they are both under the same flag so the player gets both locations just one of the two items
        random_stt_item = self.multiworld.per_slot_randoms[self.player].choice(filler_items)
        self.multiworld.get_location(LocationName.JunkChampionBelt, self.player).place_locked_item(
                self.create_item(random_stt_item))
        self.multiworld.get_location(LocationName.JunkMedal, self.player).place_locked_item(
                self.create_item(random_stt_item))
        self.totalLocations -= 2

        # Making a copy of the total growth pool
        growth_list = list()
        for x in range(4):
            growth_list.extend(Items.Movement_Table.keys())

        if self.multiworld.Schmovement[self.player].value != 0:
            for x in range(self.multiworld.Schmovement[self.player].value):
                for name in {ItemName.HighJump, ItemName.QuickRun, ItemName.DodgeRoll, ItemName.AerialDodge,
                             ItemName.Glide}:
                    item_quantity_dict.update({name: Items.item_dictionary_table[name].quantity - 1})
                    growth_list.remove(name)
                    self.multiworld.push_precollected(self.create_item(name))

        if self.multiworld.RandomGrowth[self.player].value != 0:
            for x in range(self.multiworld.RandomGrowth[self.player].value):
                # try catch in the instance of the user having max movement and wants too much growth
                if not len(growth_list) == 0:
                    random_growth = self.multiworld.per_slot_randoms[self.player].choice(growth_list)
                    item_quantity_dict.update({random_growth: Items.item_dictionary_table[random_growth].quantity - 1})
                    growth_list.remove(random_growth)
                    self.multiworld.push_precollected(self.create_item(random_growth))

        visitlockingitem = list()
        visitlockingitem.extend(exclusionItem_table["AllVisitLocking"])
        # no visit locking
        if self.multiworld.Visitlocking[self.player].value == 0:
            for item in visitlockingitem:
                self.multiworld.push_precollected(self.create_item(item))
                item_quantity_dict.update({item: Items.item_dictionary_table[item].quantity - 1})
                visitlockingitem.remove(item)
        # first and second visit locking
        elif self.multiworld.Visitlocking[self.player].value in {1}:
            for item in exclusionItem_table["2VisitLocking"]:
                item_quantity_dict.update({item: Items.item_dictionary_table[item].quantity - 1})
                self.multiworld.push_precollected(self.create_item(item))
                visitlockingitem.remove(item)

        for x in range(self.multiworld.RandomVisitLockingItem[self.player].value):
            if len(visitlockingitem) <= 0:
                break
            item = self.multiworld.per_slot_randoms[self.player].choice(visitlockingitem)
            item_quantity_dict.update({item: Items.item_dictionary_table[item].quantity - 1})
            self.multiworld.push_precollected(self.create_item(item))
            visitlockingitem.remove(item)


        # there are levels but level 1 is there to keep code clean
        if self.multiworld.LevelDepth[self.player].value == 3:
            # level 99 sanity
            self.totalLocations -= 1
        elif self.multiworld.LevelDepth[self.player].value == 2:
            # level 50 sanity
            self.totalLocations -= 50
        elif self.multiworld.LevelDepth[self.player].value == 4:
            # level 1. No checks on levels
            self.totalLocations -= 99
        else:
            # level 50/99 since they contain the same amount of levels
            self.totalLocations -= 76

        for item in item_dictionary_table:
            data = item_quantity_dict[item]
            for x in range(data):
                itempool.append(self.create_item(item))
                item_quantity_dict.update({item: Items.item_dictionary_table[item].quantity - 1})

        # Creating filler for unfilled locations
        while len(itempool) < self.totalLocations:
            item = self.multiworld.per_slot_randoms[self.player].choice(filler_items)
            itempool += [self.create_item(item)]
        self.multiworld.itempool += itempool

    def create_regions(self):
        location_table = setup_locations(self.multiworld, self.player)
        create_regions(self.multiworld, self.player, location_table)
        connect_regions(self.multiworld, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str):
        patch_kh2(self, output_directory)
