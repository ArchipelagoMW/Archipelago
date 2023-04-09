
from BaseClasses import Tutorial, ItemClassification
import logging

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


# noinspection PyUnresolvedReferences
class KH2World(World):
    """
    Kingdom Hearts II is an action role-playing game developed and published by Square Enix and released in 2005.
    It is the sequel to Kingdom Hearts and Kingdom Hearts: Chain of Memories, and like the two previous games,
    focuses on Sora and his friends' continued battle against the Darkness.
    """
    game: str = "Kingdom Hearts 2"
    web = KingdomHearts2Web()
    data_version = 1
    option_definitions = KH2_Options
    item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    location_name_to_id = {item_name: data.code for item_name, data in all_locations.items() if data.code}
    item_name_groups = item_groups

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.BountiesRequired = None
        self.BountiesAmount = None
        self.hitlist = None
        self.LocalItems = {}
        self.RandomSuperBoss = list()
        self.filler_items = list()
        self.item_quantity_dict = {}
        self.donald_ability_pool = list()
        self.goofy_ability_pool = list()
        self.sora_keyblade_ability_pool = list()
        self.keyblade_slot_copy = list(Locations.Keyblade_Slots.keys())
        self.keyblade_slot_copy.remove(LocationName.KingdomKeySlot)
        self.totalLocations = len(all_locations.items())
        self.growth_list = list()
        for x in range(4):
            self.growth_list.extend(Movement_Table.keys())
        self.visitlocking_dict = Progression_Dicts["AllVisitLocking"]

    def fill_slot_data(self) -> dict:
        return {"hitlist": self.hitlist,
                "LocalItems": self.LocalItems,
                "Goal": self.multiworld.Goal[self.player].value,
                "FinalXemnas": self.multiworld.FinalXemnas[self.player].value,
                "LuckyEmblemsRequired":  self.multiworld.LuckyEmblemsRequired[self.player].value,
                "BountyRequired": self.multiworld.BountyRequired[self.player].value}

    def create_item(self, name: str, ) -> Item:
        data = item_dictionary_table[name]
        if name in Progression_Dicts["Progression"]:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.filler

        created_item = KH2Item(name, item_classification, data.code, self.player)

        return created_item

    def generate_early(self) -> None:
        # Item Quantity dict because Abilities can be a problem for KH2's Software.
        for item, data in item_dictionary_table.items():
            self.item_quantity_dict[item] = data.quantity

        if self.multiworld.KeybladeAbilities[self.player] == "support":
            self.sora_keyblade_ability_pool.extend(SupportAbility_Table.keys())
        elif self.multiworld.KeybladeAbilities[self.player] == "action":
            self.sora_keyblade_ability_pool.extend(ActionAbility_Table.keys())
        else:
            # both action and support on keyblades.
            # TODO: make option to just exclude scom
            self.sora_keyblade_ability_pool.extend(ActionAbility_Table.keys())
            self.sora_keyblade_ability_pool.extend(SupportAbility_Table.keys())

        for item, value in self.multiworld.start_inventory[self.player].value.items():
            if item in ActionAbility_Table.keys() or item in SupportAbility_Table.keys() or exclusionItem_table["StatUps"]:
                # cannot have more than the quantity for abilties
                if value > item_dictionary_table[item].quantity:
                    logging.info(f"{self.multiworld.get_file_safe_player_name(self.player)} cannot have more than {item_dictionary_table[item].quantity} of {item}"
                                 f"Changing the amount to the max amount")
                    value = item_dictionary_table[item].quantity
                self.item_quantity_dict[item] -= value

        # Option to turn off Promise Charm Item
        if not self.multiworld.Promise_Charm[self.player]:
            self.item_quantity_dict[ItemName.PromiseCharm] = 0

        for ability in self.multiworld.BlacklistKeyblade[self.player].value:
            if ability in self.sora_keyblade_ability_pool:
                self.sora_keyblade_ability_pool.remove(ability)

        # Option to turn off all superbosses. Can do this individually but its like 20+ checks
        if not self.multiworld.SuperBosses[self.player] and not self.multiworld.Goal[self.player] == "hitlist":
            for superboss in exclusion_table["Datas"]:
                self.multiworld.exclude_locations[self.player].value.add(superboss)
            for superboss in exclusion_table["SuperBosses"]:
                self.multiworld.exclude_locations[self.player].value.add(superboss)

        # Option to turn off Olympus Colosseum Cups.
        if self.multiworld.Cups[self.player] == "no_cups":
            for cup in exclusion_table["Cups"]:
                self.multiworld.exclude_locations[self.player].value.add(cup)
        # exclude only hades paradox. If cups and hades paradox then nothing is excluded
        elif self.multiworld.Cups[self.player] == "cups":
            self.multiworld.exclude_locations[self.player].value.add(LocationName.HadesCupTrophyParadoxCups)

        if self.multiworld.Goal[self.player] == "lucky_emblem_hunt":
            luckyemblemamount = self.multiworld.LuckyEmblemsAmount[self.player].value
            luckyemblemrequired = self.multiworld.LuckyEmblemsRequired[self.player].value
            if luckyemblemamount < luckyemblemrequired:
                logging.info(f"Lucky Emblem Amount {self.multiworld.LuckyEmblemsAmount[self.player].value} is less than required "
                             f"{self.multiworld.LuckyEmblemsRequired[self.player].value} for player {self.multiworld.get_file_safe_player_name(self.player)}."
                             f" Setting amount to {self.multiworld.LuckyEmblemsRequired[self.player].value}")
                luckyemblemamount = max(luckyemblemamount, luckyemblemrequired)
                self.multiworld.LuckyEmblemsAmount[self.player].value = luckyemblemamount

            self.item_quantity_dict[ItemName.LuckyEmblem] = item_dictionary_table[ItemName.LuckyEmblem].quantity + luckyemblemamount
            # give this proof to unlock the final door once the player has the amount of lucky emblem required
            self.item_quantity_dict[ItemName.ProofofNonexistence] = 0

        # hitlist
        elif self.multiworld.Goal[self.player] == "hitlist":
            self.RandomSuperBoss.extend(exclusion_table["Hitlist"])
            self.BountiesAmount = self.multiworld.BountyAmount[self.player].value
            self.BountiesRequired = self.multiworld.BountyRequired[self.player].value

            for location in self.multiworld.exclude_locations[self.player].value:
                if location in self.RandomSuperBoss:
                    self.RandomSuperBoss.remove(location)
            #  Testing if the player has the right amount of Bounties for Completion.
            if len(self.RandomSuperBoss) < self.BountiesAmount:
                logging.info(f"{self.multiworld.get_file_safe_player_name(self.player)} has too many bounties than bosses."
                             f" Setting total bounties to {len(self.RandomSuperBoss)}")
                self.BountiesAmount = len(self.RandomSuperBoss)
                self.multiworld.BountyAmount[self.player].value = self.BountiesAmount

            if len(self.RandomSuperBoss) < self.BountiesRequired:
                logging.info(f"{self.multiworld.get_file_safe_player_name(self.player)} has too many required bounties."
                             f" Setting required bounties to {len(self.RandomSuperBoss)}")
                self.BountiesRequired = len(self.RandomSuperBoss)
                self.multiworld.BountyRequired[self.player].value = self.BountiesRequired

            if self.BountiesAmount < self.BountiesRequired:
                logging.info(f"Bounties Amount {self.multiworld.BountyAmount[self.player].value} is less than required "
                             f"{self.multiworld.BountyRequired[self.player].value} for player {self.multiworld.get_file_safe_player_name(self.player)}."
                             f" Setting amount to {self.multiworld.BountyRequired[self.player].value}")
                self.BountiesAmount = max(self.BountiesAmount, self.BountiesRequired)
                self.multiworld.BountyAmount[self.player].value = self.BountiesAmount

            self.multiworld.start_hints[self.player].value.add(ItemName.Bounty)
            self.item_quantity_dict[ItemName.ProofofNonexistence] = 0

        while len(self.sora_keyblade_ability_pool) < len(self.keyblade_slot_copy):
            self.sora_keyblade_ability_pool.append(
                self.multiworld.per_slot_randoms[self.player].choice(list(SupportAbility_Table.keys())))

        for item in DonaldAbility_Table.keys():
            data = self.item_quantity_dict[item]
            for _ in range(data):
                self.donald_ability_pool.append(item)
            self.item_quantity_dict[item] = 0
            # 32 is the amount of donald abilities
        while len(self.donald_ability_pool) < 32:
            self.donald_ability_pool.append(self.multiworld.per_slot_randoms[self.player].choice(self.donald_ability_pool))

        for item in GoofyAbility_Table.keys():
            data = self.item_quantity_dict[item]
            for _ in range(data):
                self.goofy_ability_pool.append(item)
            self.item_quantity_dict[item] = 0
            # 32 is the amount of goofy abilities
        while len(self.goofy_ability_pool) < 33:
            self.goofy_ability_pool.append(self.multiworld.per_slot_randoms[self.player].choice(self.goofy_ability_pool))

    def generate_basic(self):
        itempool: typing.List[KH2Item] = []

        self.hitlist = list()
        self.filler_items.extend(item_groups["Filler"])

        if self.multiworld.FinalXemnas[self.player]:
            self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(
                    self.create_item(ItemName.Victory))
        else:
            self.multiworld.get_location(LocationName.FinalXemnas, self.player).place_locked_item(
                    self.create_item(self.multiworld.per_slot_randoms[self.player].choice(self.filler_items)))
        self.totalLocations -= 1

        if self.multiworld.Goal[self.player] == "hitlist":
            for bounty in range(self.BountiesAmount):
                randomBoss = self.multiworld.per_slot_randoms[self.player].choice(self.RandomSuperBoss)
                self.multiworld.get_location(randomBoss, self.player).place_locked_item(
                        self.create_item(ItemName.Bounty))
                self.hitlist.append(self.location_name_to_id[randomBoss])
                self.RandomSuperBoss.remove(randomBoss)
                self.totalLocations -= 1

        #  Kingdom Key cannot have No Experience so plandoed here instead of checking 26 times if its kingdom key
        random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.sora_keyblade_ability_pool)
        while random_ability == ItemName.NoExperience:
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.sora_keyblade_ability_pool)
        self.multiworld.get_location(LocationName.KingdomKeySlot, self.player).place_locked_item(self.create_item(random_ability))
        self.item_quantity_dict[random_ability] -= 1
        self.sora_keyblade_ability_pool.remove(random_ability)
        self.totalLocations -= 1

        # plando keyblades because they can only have abilities
        for keyblade in self.keyblade_slot_copy:
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.sora_keyblade_ability_pool)
            self.multiworld.get_location(keyblade, self.player).place_locked_item(self.create_item(random_ability))
            self.item_quantity_dict[random_ability] -= 1
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

        if self.multiworld.Schmovement[self.player] != "level_0":
            for _ in range(self.multiworld.Schmovement[self.player].value):
                for name in {ItemName.HighJump, ItemName.QuickRun, ItemName.DodgeRoll, ItemName.AerialDodge,
                             ItemName.Glide}:
                    self.item_quantity_dict[name] -= 1
                    self.growth_list.remove(name)
                    self.multiworld.push_precollected(self.create_item(name))

        if self.multiworld.RandomGrowth[self.player] != 0:
            max_growth = min(self.multiworld.RandomGrowth[self.player].value, len(self.growth_list))
            for _ in range(max_growth):
                random_growth = self.multiworld.per_slot_randoms[self.player].choice(self.growth_list)
                self.item_quantity_dict[random_growth] -= 1
                self.growth_list.remove(random_growth)
                self.multiworld.push_precollected(self.create_item(random_growth))

        # no visit locking
        if self.multiworld.Visitlocking[self.player] == "no_visit_locking":
            for item, amount in Progression_Dicts["AllVisitLocking"].items():
                for _ in range(amount):
                    self.multiworld.push_precollected(self.create_item(item))
                    self.item_quantity_dict[item] -= 1
                    if self.visitlocking_dict[item] == 0:
                        self.visitlocking_dict.pop(item)
                    self.visitlocking_dict[item] -= 1

        # first and second visit locking
        elif self.multiworld.Visitlocking[self.player] == "second_visit_locking":
            for item in Progression_Dicts["2VisitLocking"]:
                self.item_quantity_dict[item] -= 1
                self.visitlocking_dict[item] -= 1
                if self.visitlocking_dict[item] == 0:
                    self.visitlocking_dict.pop(item)
                self.multiworld.push_precollected(self.create_item(item))

        for _ in range(self.multiworld.RandomVisitLockingItem[self.player].value):
            if sum(self.visitlocking_dict.values()) <= 0:
                break
            visitlocking_set = list(self.visitlocking_dict.keys())
            item = self.multiworld.per_slot_randoms[self.player].choice(visitlocking_set)
            self.item_quantity_dict[item] -= 1
            self.visitlocking_dict[item] -= 1
            if self.visitlocking_dict[item] == 0:
                self.visitlocking_dict.pop(item)
            self.multiworld.push_precollected(self.create_item(item))

        # there are levels but level 1 is there to keep code clean
        if self.multiworld.LevelDepth[self.player] == "level_99_sanity":
            # level 99 sanity
            self.totalLocations -= 1
        elif self.multiworld.LevelDepth[self.player] == "level_50_sanity":
            # level 50 sanity
            self.totalLocations -= 50
        elif self.multiworld.LevelDepth[self.player] == "level_1":
            # level 1. No checks on levels
            self.totalLocations -= 99
        else:
            # level 50/99 since they contain the same amount of levels
            self.totalLocations -= 76

        for item in item_dictionary_table:
            data = self.item_quantity_dict[item]
            for _ in range(data):
                itempool.append(self.create_item(item))

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
