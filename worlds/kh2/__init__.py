import typing

from BaseClasses import Item, Tutorial, ItemClassification

from .Items import *
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
    """
    Kingdom Hearts II is an action role-playing game developed and published by Square Enix and released in 2005.
    It is the sequel to Kingdom Hearts and Kingdom Hearts: Chain of Memories, and like the two previous games,
    focuses on Sora and his friends' continued battle against the Darkness.
    """
    game: str = "Kingdom Hearts 2"
    web = KingdomHearts2Web()
    data_version = 0
    option_definitions = KH2_Options
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    location_name_to_id = {item_name: data.code for item_name, data in all_locations.items() if data.code}
    item_name_groups = item_groups

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.BountiesRequired = None
        self.BountiesAmount = None
        self.hitlist = None
        self.RandomSuperBoss = list()
        self.filler_items = list()
        self.item_quantity_dict = {}
        self.donald_ability_pool = list()
        self.goofy_ability_pool = list()
        self.sora_keyblade_ability_pool = list()
        self.keyblade_slot_copy = list(Locations.Keyblade_Slots.keys())
        self.totalLocations = len(all_locations.items())
        self.growth_list = list()
        for x in range(4):
            self.growth_list.extend(Movement_Table.keys())
        self.visitlockingitem = list()
        self.visitlockingitem.extend(exclusionItem_table["AllVisitLocking"])

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
        if name in ProgressionItems or name in Misc_Table or name in Staffs_Table or name in Shields_Table:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.filler

        created_item = KH2Item(name, item_classification, data.code, self.player)

        return created_item

    def generate_early(self) -> None:
        # Item Quantity dict because Abilities can be a problem for KH2's Software.
        for item, data in item_dictionary_table.items():
            self.item_quantity_dict.update({item: data.quantity})

        if self.multiworld.KeybladeAbilities[self.player].value == 0:
            self.sora_keyblade_ability_pool.extend(SupportAbility_Table.keys())
        elif self.multiworld.KeybladeAbilities[self.player].value == 1:
            self.sora_keyblade_ability_pool.extend(ActionAbility_Table.keys())
        else:
            self.sora_keyblade_ability_pool.extend(ActionAbility_Table.keys())
            self.sora_keyblade_ability_pool.extend(SupportAbility_Table.keys())

        for item, value in self.multiworld.start_inventory[self.player].value.items():
            if item in ActionAbility_Table.keys() or item in SupportAbility_Table.keys():
                # cannot have more than the quantity for abilties
                if value > item_dictionary_table[item].quantity:
                    print(
                        f"{self.multiworld.get_file_safe_player_name(self.player)} cannot have more than {item_dictionary_table[item].quantity} of {item}")
                self.item_quantity_dict.update({item: item_dictionary_table[item].quantity - 1})

        # Option to turn off Promise Charm Item
        if self.multiworld.Promise_Charm[self.player].value == 0:
            self.item_quantity_dict.update({ItemName.PromiseCharm: 0})

        for ability in self.multiworld.BlacklistKeyblade[self.player].value:
            if ability in self.sora_keyblade_ability_pool:
                self.sora_keyblade_ability_pool.remove(ability)


        # Option to turn off all superbosses. Can do this individually but its like 20+ checks
        if self.multiworld.SuperBosses[self.player].value == 0 and not self.multiworld.Goal[self.player].value == 2:
            for superboss in exclusion_table["Datas"]:
                self.multiworld.exclude_locations[self.player].value.add(superboss)
            for superboss in exclusion_table["SuperBosses"]:
                self.multiworld.exclude_locations[self.player].value.add(superboss)

        # Option to turn off Olympus Colosseum Cups.
        if self.multiworld.Cups[self.player].value == 0:
            for cup in exclusion_table["Cups"]:
                self.multiworld.exclude_locations[self.player].value.add(cup)
        elif self.multiworld.Cups[self.player].value == 1:
            self.multiworld.exclude_locations[self.player].value.add(LocationName.HadesCupTrophyParadoxCups)

        if self.multiworld.Goal[self.player].value == 1:
            luckyemblemamount = self.multiworld.LuckyEmblemsAmount[self.player].value
            luckyemblemrequired = self.multiworld.LuckyEmblemsRequired[self.player].value
            if luckyemblemamount < luckyemblemrequired:
                luckyemblemamount = max(luckyemblemamount, luckyemblemrequired)
                print(f"Lucky Emblem Amount {self.multiworld.LuckyEmblemsAmount[self.player].value} is less than required \
            {self.multiworld.LuckyEmblemsRequired[self.player].value} for player {self.multiworld.get_file_safe_player_name(self.player)}")
            self.item_quantity_dict.update(
                    {ItemName.LuckyEmblem: item_dictionary_table[ItemName.LuckyEmblem].quantity + luckyemblemamount})
            # give this proof to unlock the final door once the player has the amount of lucky emblem required
            self.item_quantity_dict.update({ItemName.ProofofNonexistence: 0})

        # hitlist
        elif self.multiworld.Goal[self.player].value == 2:
            self.RandomSuperBoss.extend(exclusion_table["Hitlist"])
            self.BountiesAmount = self.multiworld.BountyAmount[self.player].value
            self.BountiesRequired = self.multiworld.BountyRequired[self.player].value

            for location in self.multiworld.exclude_locations[self.player].value:
                if location in self.RandomSuperBoss:
                    self.RandomSuperBoss.remove(location)
            #  Testing if the player has the right amount of Bounties for Completion.
            if len(self.RandomSuperBoss) < self.BountiesAmount:
                print(f"{self.multiworld.get_file_safe_player_name(self.player)} has too many bounties than bosses")
                self.BountiesAmount = len(self.RandomSuperBoss)
                self.multiworld.BountyAmount[self.player].value = len(self.RandomSuperBoss)

            if len(self.RandomSuperBoss) < self.BountiesRequired:
                print(f"{self.multiworld.get_file_safe_player_name(self.player)} has too many required bounties")
                self.BountiesRequired = len(self.RandomSuperBoss)
                self.multiworld.BountyRequired[self.player].value = len(self.RandomSuperBoss)

            if self.BountiesAmount < self.BountiesRequired:
                self.BountiesAmount = max(self.BountiesAmount, self.BountiesRequired)
                print(f"Bounties Amount {self.multiworld.BountyAmount[self.player].value} is less than required \
                        {self.multiworld.BountyRequired[self.player].value} for player {self.multiworld.get_file_safe_player_name(self.player)}")
            self.multiworld.start_hints[self.player].value.add(ItemName.Bounty)
            self.item_quantity_dict.update({ItemName.ProofofNonexistence: 0})

        while len(self.sora_keyblade_ability_pool) < len(self.keyblade_slot_copy):
            self.sora_keyblade_ability_pool.append(
                self.multiworld.per_slot_randoms[self.player].choice(list(SupportAbility_Table.keys())))

        for item in DonaldAbility_Table.keys():
            data = self.item_quantity_dict[item]
            for x in range(data):
                self.donald_ability_pool.append(item)
            self.item_quantity_dict.update({item: 0})
        while len(self.donald_ability_pool) < len(Locations.Donald_Checks.keys()):
            self.donald_ability_pool.append(
                    self.multiworld.per_slot_randoms[self.player].choice(self.donald_ability_pool))

        for item in GoofyAbility_Table.keys():
            data = self.item_quantity_dict[item]
            for x in range(data):
                self.goofy_ability_pool.append(item)
            self.item_quantity_dict.update({item: 0})
        while len(self.goofy_ability_pool) < len(GoofyAbility_Table.keys()):
            self.goofy_ability_pool.append(
                self.multiworld.per_slot_randoms[self.player].choice(self.goofy_ability_pool))

    def generate_basic(self):
        itempool: typing.List[KH2Item] = []

        self.hitlist = list()
        self.filler_items.extend(exclusionItem_table["Filler"])

        if self.multiworld.FinalXemnas[self.player].value == 1:
            self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(
                    self.create_item(ItemName.Victory))
        else:
            self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(
                    self.create_item(self.multiworld.per_slot_randoms[self.player].choice(self.filler_items)))
        self.totalLocations -= 1

        if self.multiworld.Goal[self.player].value == 2:
            for bounty in range(self.BountiesAmount):
                randomBoss = self.multiworld.per_slot_randoms[self.player].choice(self.RandomSuperBoss)
                self.multiworld.get_location(randomBoss, self.player).place_locked_item(
                        self.create_item(ItemName.Bounty))
                self.hitlist.append(self.location_name_to_id[randomBoss])
                self.RandomSuperBoss.remove(randomBoss)
                self.totalLocations -= 1

        # plando keyblades because they can only have abilities
        for keyblade in self.keyblade_slot_copy:
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.sora_keyblade_ability_pool)
            self.multiworld.get_location(keyblade, self.player).place_locked_item(self.create_item(random_ability))
            self.item_quantity_dict.update({random_ability: item_dictionary_table[random_ability].quantity - 1})
            self.sora_keyblade_ability_pool.remove(random_ability)
            self.totalLocations -= 1

        # Placing Donald Abilities on donald locations
        for donaldLocation in Locations.Donald_Checks.keys():
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.donald_ability_pool)
            self.multiworld.get_location(donaldLocation, self.player).place_locked_item(
                self.create_item(random_ability))
            self.totalLocations -= 1
            self.donald_ability_pool.remove(random_ability)

        # Placing Goofy Abilities on goofy locations
        for goofyLocation in Locations.Goofy_Checks.keys():
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.goofy_ability_pool)
            self.multiworld.get_location(goofyLocation, self.player).place_locked_item(self.create_item(random_ability))
            self.totalLocations -= 1
            self.goofy_ability_pool.remove(random_ability)

        # same item placed because you can only get one of these 2 locations
        # they are both under the same flag so the player gets both locations just one of the two items
        random_stt_item = self.multiworld.per_slot_randoms[self.player].choice(self.filler_items)
        self.multiworld.get_location(LocationName.JunkChampionBelt, self.player).place_locked_item(
                self.create_item(random_stt_item))
        self.multiworld.get_location(LocationName.JunkMedal, self.player).place_locked_item(
                self.create_item(random_stt_item))
        self.totalLocations -= 2

        if self.multiworld.Schmovement[self.player].value != 0:
            for x in range(self.multiworld.Schmovement[self.player].value):
                for name in {ItemName.HighJump, ItemName.QuickRun, ItemName.DodgeRoll, ItemName.AerialDodge,
                             ItemName.Glide}:
                    self.item_quantity_dict.update({name: item_dictionary_table[name].quantity - 1})
                    self.growth_list.remove(name)
                    self.multiworld.push_precollected(self.create_item(name))

        if self.multiworld.RandomGrowth[self.player].value != 0:
            for x in range(self.multiworld.RandomGrowth[self.player].value):
                # try catch in the instance of the user having max movement and wants too much growth
                if not len(self.growth_list) == 0:
                    random_growth = self.multiworld.per_slot_randoms[self.player].choice(self.growth_list)
                    self.item_quantity_dict.update({random_growth: item_dictionary_table[random_growth].quantity - 1})
                    self.growth_list.remove(random_growth)
                    self.multiworld.push_precollected(self.create_item(random_growth))

        # no visit locking
        if self.multiworld.Visitlocking[self.player].value == 0:
            for item in self.visitlockingitem:
                self.multiworld.push_precollected(self.create_item(item))
                self.item_quantity_dict.update({item: item_dictionary_table[item].quantity - 1})
                self.visitlockingitem.remove(item)

        # first and second visit locking
        elif self.multiworld.Visitlocking[self.player].value in {1}:
            for item in exclusionItem_table["2VisitLocking"]:
                self.item_quantity_dict.update({item: item_dictionary_table[item].quantity - 1})
                self.multiworld.push_precollected(self.create_item(item))
                self.visitlockingitem.remove(item)

        for x in range(self.multiworld.RandomVisitLockingItem[self.player].value):
            if len(self.visitlockingitem) <= 0:
                break
            item = self.multiworld.per_slot_randoms[self.player].choice(self.visitlockingitem)
            self.item_quantity_dict.update({item: item_dictionary_table[item].quantity - 1})
            self.multiworld.push_precollected(self.create_item(item))
            self.visitlockingitem.remove(item)

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
            data = self.item_quantity_dict[item]
            for x in range(data):
                itempool.append(self.create_item(item))
                self.item_quantity_dict.update({item: item_dictionary_table[item].quantity - 1})

        # Creating filler for unfilled locations
        while len(itempool) < self.totalLocations:
            item = self.multiworld.per_slot_randoms[self.player].choice(self.filler_items)
            itempool += [self.create_item(item)]
        self.multiworld.itempool += itempool

    def create_regions(self):
        location_table = setup_locations()
        create_regions(self.multiworld, self.player, location_table)
        connect_regions(self.multiworld, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str):
        patch_kh2(self, output_directory)
