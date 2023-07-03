from BaseClasses import Tutorial, ItemClassification
import logging

from .Rules import *
from .Items import *
from .Locations import all_locations, exclusion_table, AllWeaponSlot
from .Names import ItemName, LocationName
from .OpenKH import patch_kh2
from .Options import KH2_Options
from .Regions import create_regions, connect_regions
# from .Rules import set_rules
from ..AutoWorld import World, WebWorld


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
    game = "Kingdom Hearts 2"
    web = KingdomHearts2Web()
    data_version = 1
    required_client_version = (0, 4, 0)
    option_definitions = KH2_Options
    # item_name_to_id = {name: data.code for name, data in item_dictionary_table.items()}
    # base_offset = 0x130000
    item_name_to_id = {item: item_id
                       for item_id, item in enumerate(item_dictionary_table.keys(), 0x130000)}
    location_name_to_id = {item: location
                           for location, item in enumerate(all_locations.keys(), 0x130000)}
    item_name_groups = item_groups

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.valid_abilities = None
        self.visitlocking_dict = None
        self.plando_locations = None
        self.luckyemblemamount = None
        self.luckyemblemrequired = None
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
        self.slotDataDuping = set()
        self.localItems = dict()

    def fill_slot_data(self) -> dict:
        # localItems filling done here for the unit test.
        for values in CheckDupingItems.values():
            if isinstance(values, set):
                self.slotDataDuping = self.slotDataDuping.union(values)
            else:
                for inner_values in values.values():
                    self.slotDataDuping = self.slotDataDuping.union(inner_values)
        self.LocalItems = {location.address: self.item_name_to_id[location.item.name]
                           for location in self.multiworld.get_filled_locations(self.player)
                           if location.item.player == self.player
                           and location.item.name in self.slotDataDuping
                           and location.name not in AllWeaponSlot}

        return {
            "hitlist":              self.hitlist,
            "LocalItems":           self.LocalItems,
            "Goal":                 self.multiworld.Goal[self.player].value,
            "FinalXemnas":          self.multiworld.FinalXemnas[self.player].value,
            "LuckyEmblemsRequired": self.multiworld.LuckyEmblemsRequired[self.player].value,
            "BountyRequired":       self.multiworld.BountyRequired[self.player].value
        }

    def create_item(self, name: str, ) -> Item:
        """
        Returns created KH2Item
        """
        # data = item_dictionary_table[name]
        if name in ItemClassification_Dict["Progression"]:
            item_classification = ItemClassification.progression
        else:
            item_classification = ItemClassification.filler

        created_item = KH2Item(name, item_classification, self.item_name_to_id[name], self.player)

        return created_item

    def create_items(self) -> None:
        """
        Fills ItemPool and manages schmovement, random growth, visit locking and random starting visit locking.
        """
        self.visitlocking_dict = visit_locking_dict["AllVisitLocking"].copy()
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

        if self.multiworld.Visitlocking[self.player] == "no_visit_locking":
            for item, amount in visit_locking_dict["AllVisitLocking"].items():
                for _ in range(amount):
                    self.multiworld.push_precollected(self.create_item(item))
                    self.item_quantity_dict[item] -= 1
                    self.visitlocking_dict[item] -= 1
                    if self.visitlocking_dict[item] == 0:
                        self.visitlocking_dict.pop(item)

        elif self.multiworld.Visitlocking[self.player] == "second_visit_locking":
            for item in visit_locking_dict["2VisitLocking"]:
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

        itempool = [self.create_item(item) for item, data in self.item_quantity_dict.items() for _ in range(data)]

        # Creating filler for unfilled locations
        itempool += [self.create_filler()
                     for _ in range(self.totalLocations - len(itempool))]
        self.multiworld.itempool += itempool

    def generate_early(self) -> None:
        """
        Determines the quantity of items and maps plando locations to items.
        """
        # Item Quantity Map
        self.item_quantity_dict = {item: data.quantity for item, data in item_dictionary_table.items()}
        # Dictionary to mark locations with their plandoed item
        # Example. Final Xemnas: Victory
        self.plando_locations = dict()
        self.starting_invo_verify()

        # Option to turn off Promise Charm Item
        if not self.multiworld.Promise_Charm[self.player]:
            self.item_quantity_dict[ItemName.PromiseCharm] = 0

        self.set_excluded_locations()

        if self.multiworld.Goal[self.player] == "lucky_emblem_hunt":
            self.luckyemblemamount = self.multiworld.LuckyEmblemsAmount[self.player].value
            self.luckyemblemrequired = self.multiworld.LuckyEmblemsRequired[self.player].value
            self.emblem_verify()

        # hitlist
        elif self.multiworld.Goal[self.player] == "hitlist":
            self.hitlist = []
            self.RandomSuperBoss.extend(exclusion_table["Hitlist"])
            self.BountiesAmount = self.multiworld.BountyAmount[self.player].value
            self.BountiesRequired = self.multiworld.BountyRequired[self.player].value

            self.hitlist_verify()

            for bounty in range(self.BountiesAmount):
                randomBoss = self.multiworld.per_slot_randoms[self.player].choice(self.RandomSuperBoss)
                self.plando_locations[randomBoss] = ItemName.Bounty
                self.hitlist.append(self.location_name_to_id[randomBoss])
                self.RandomSuperBoss.remove(randomBoss)
                self.totalLocations -= 1

        self.donald_fill()
        self.goofy_fill()
        self.keyblade_fill()

        if self.multiworld.FinalXemnas[self.player]:
            self.plando_locations[LocationName.FinalXemnas] = ItemName.Victory
        else:
            self.plando_locations[LocationName.FinalXemnas] = self.create_filler().name

        # By imitating remote this doesn't have to be plandoded filler anymore
        #  random_stt_item = self.create_filler().name
        #  for location in {LocationName.JunkMedal, LocationName.JunkMedal}:
        #    self.plando_locations[location] = random_stt_item
        self.level_subtraction()

        # subtraction from final xemnas
        self.totalLocations -= 2

    def pre_fill(self):
        """
        Plandoing Items to their locations.
        """
        for location, item in self.plando_locations.items():
            self.multiworld.get_location(location, self.player).place_locked_item(
                    self.create_item(item))

    def create_regions(self):
        """
        Creates the Regions and Connects them.
        """
        create_regions(self.multiworld, self.player, self.location_name_to_id)
        connect_regions(self.multiworld, self.player)

    def set_rules(self):
        """
        Sets the Logic for the Regions and Locations.
        """
        universal_logic = Rules.KH2Rules(self)
        form_logic = Rules.KH2FormRules(self)
        yourmom = Rules.KH2FightRules(self)
        yourmom.set_kh2_fight_rules()
        universal_logic.set_kh2_rules()
        form_logic.set_kh2_form_rules()

        # logic = self.multiworld.logic_level[self.player]
        # if logic == Logic.option_normal:
        #    Rules.MessengerRules(self).set_messenger_rules()
        # elif logic == Logic.option_hard:
        #    Rules.MessengerHardRules(self).set_messenger_rules()
        # elif logic == Logic.option_challenging:
        #    Rules.MessengerChallengeRules(self).set_messenger_rules()
        # else:
        #    Rules.MessengerOOBRules(self).set_messenger_rules()
        # set_rules(self.multiworld, self.player)

    def generate_output(self, output_directory: str):
        """
        Generates the .zip for OpenKH (The KH Mod Manager)
        """
        patch_kh2(self, output_directory)

    def donald_fill(self):
        """
        Removes donald locations from the location pool maps random donald items to be plandoded.
        """
        for item in DonaldAbility_Table:
            data = self.item_quantity_dict[item]
            for _ in range(data):
                self.donald_ability_pool.append(item)
            self.item_quantity_dict[item] = 0
            # 32 is the amount of donald abilities
        while len(self.donald_ability_pool) < 32:
            self.donald_ability_pool.append(
                    self.multiworld.per_slot_randoms[self.player].choice(self.donald_ability_pool))
            # Placing Donald Abilities on donald locations
        for donaldLocation in Locations.Donald_Checks.keys():
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.donald_ability_pool)
            self.plando_locations[donaldLocation] = random_ability
            self.totalLocations -= 1
            self.donald_ability_pool.remove(random_ability)

    def goofy_fill(self):
        """
        Removes donald locations from the location pool maps random donald items to be plandoded.
        """
        for item in GoofyAbility_Table.keys():
            data = self.item_quantity_dict[item]
            for _ in range(data):
                self.goofy_ability_pool.append(item)
            self.item_quantity_dict[item] = 0
            # 33 is the amount of goofy abilities
        while len(self.goofy_ability_pool) < 33:
            self.goofy_ability_pool.append(
                    self.multiworld.per_slot_randoms[self.player].choice(self.goofy_ability_pool))
        # Placing Goofy Abilities on goofy locations
        for goofyLocation in Locations.Goofy_Checks.keys():
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.goofy_ability_pool)
            self.plando_locations[goofyLocation] = random_ability
            self.totalLocations -= 1
            self.goofy_ability_pool.remove(random_ability)

    def keyblade_fill(self):
        """
        Fills keyblade slots with abilities determined on player's setting
        """
        if self.multiworld.KeybladeAbilities[self.player] == "support":
            self.sora_keyblade_ability_pool = {
                **{item: data for item, data in self.item_quantity_dict.items() if item in SupportAbility_Table},
                **{
                    ItemName.NegativeCombo: 1, ItemName.AirComboPlus: 1, ItemName.ComboPlus: 1,
                    ItemName.FinishingPlus: 1
                }
            }

        elif self.multiworld.KeybladeAbilities[self.player] == "action":
            self.sora_keyblade_ability_pool = {item: data for item, data in self.item_quantity_dict.items() if
                                               item in ActionAbility_Table}
            # there are too little action abilities so 2 random support abilities are placed
            for _ in range(3):
                randomSupportAbility = self.multiworld.per_slot_randoms[self.player].choice(
                        list(SupportAbility_Table.keys()))
                while randomSupportAbility in self.sora_keyblade_ability_pool:
                    randomSupportAbility = self.multiworld.per_slot_randoms[self.player].choice(
                            list(SupportAbility_Table.keys()))
                self.sora_keyblade_ability_pool[randomSupportAbility] = 1
        else:
            # both action and support on keyblades.
            # TODO: make option to just exclude scom
            self.sora_keyblade_ability_pool = {
                **{item: data for item, data in self.item_quantity_dict.items() if item in SupportAbility_Table},
                **{item: data for item, data in self.item_quantity_dict.items() if item in ActionAbility_Table},
                **{
                    ItemName.NegativeCombo: 1, ItemName.AirComboPlus: 1, ItemName.ComboPlus: 1,
                    ItemName.FinishingPlus: 1
                }
            }

        for ability in self.multiworld.BlacklistKeyblade[self.player].value:
            if ability in self.sora_keyblade_ability_pool:
                self.sora_keyblade_ability_pool.pop(ability)

        # magic number for amount of keyblades
        if sum(self.sora_keyblade_ability_pool.values()) < 28:
            raise Exception(
                    f"{self.multiworld.get_file_safe_player_name(self.player)} has too little Keyblade Abilities in the Keyblade Pool")

        self.valid_abilities = list(self.sora_keyblade_ability_pool.keys())
        #  Kingdom Key cannot have No Experience so plandoed here instead of checking 26 times if its kingdom key
        random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.valid_abilities)
        while random_ability == ItemName.NoExperience:
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.valid_abilities)
        self.plando_locations[LocationName.KingdomKeySlot] = random_ability
        self.item_quantity_dict[random_ability] -= 1
        self.sora_keyblade_ability_pool[random_ability] -= 1
        if self.sora_keyblade_ability_pool[random_ability] == 0:
            self.valid_abilities.remove(random_ability)
            self.sora_keyblade_ability_pool.pop(random_ability)

        # plando keyblades because they can only have abilities
        for keyblade in self.keyblade_slot_copy:
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(self.valid_abilities)
            self.plando_locations[keyblade] = random_ability
            self.item_quantity_dict[random_ability] -= 1
            self.sora_keyblade_ability_pool[random_ability] -= 1
            if self.sora_keyblade_ability_pool[random_ability] == 0:
                self.valid_abilities.remove(random_ability)
                self.sora_keyblade_ability_pool.pop(random_ability)
            self.totalLocations -= 1

    def starting_invo_verify(self):
        """
        Making sure the player doesn't put too many abilities in their starting inventory.
        """
        for item, value in self.multiworld.start_inventory[self.player].value.items():
            if item in ActionAbility_Table \
                    or item in SupportAbility_Table or exclusion_item_table["StatUps"] \
                    or item in DonaldAbility_Table or item in GoofyAbility_Table:
                # cannot have more than the quantity for abilties
                if value > item_dictionary_table[item].quantity:
                    logging.info(
                            f"{self.multiworld.get_file_safe_player_name(self.player)} cannot have more than {item_dictionary_table[item].quantity} of {item}"
                            f"Changing the amount to the max amount")
                    value = item_dictionary_table[item].quantity
                self.item_quantity_dict[item] -= value

    def emblem_verify(self):
        """
        Making sure lucky emblems have amount>=required.
        """
        if self.luckyemblemamount < self.luckyemblemrequired:
            logging.info(
                    f"Lucky Emblem Amount {self.multiworld.LuckyEmblemsAmount[self.player].value} is less than required "
                    f"{self.multiworld.LuckyEmblemsRequired[self.player].value} for player {self.multiworld.get_file_safe_player_name(self.player)}."
                    f" Setting amount to {self.multiworld.LuckyEmblemsRequired[self.player].value}")
            luckyemblemamount = max(self.luckyemblemamount, self.luckyemblemrequired)
            self.multiworld.LuckyEmblemsAmount[self.player].value = luckyemblemamount

        self.item_quantity_dict[ItemName.LuckyEmblem] = self.multiworld.LuckyEmblemsAmount[self.player].value
        # give this proof to unlock the final door once the player has the amount of lucky emblem required
        self.item_quantity_dict[ItemName.ProofofNonexistence] = 0

    def hitlist_verify(self):
        """
        Making sure hitlist have amount>=required.
        """
        for location in self.multiworld.exclude_locations[self.player].value:
            if location in self.RandomSuperBoss:
                self.RandomSuperBoss.remove(location)

        #  Testing if the player has the right amount of Bounties for Completion.
        if len(self.RandomSuperBoss) < self.BountiesAmount:
            logging.info(
                    f"{self.multiworld.get_file_safe_player_name(self.player)} has more bounties than bosses."
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

    def set_excluded_locations(self):
        """
        Fills excluded_locations from player's settings.
        """
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

    def level_subtraction(self):
        """
        Determine how many locations are on sora's levels.
        """
        # there are levels but level 1 is there for the yamls
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

    def get_filler_item_name(self) -> str:
        """
        Returns random filler item name.
        """
        return self.multiworld.random.choice(
                [ItemName.PowerBoost, ItemName.MagicBoost, ItemName.DefenseBoost, ItemName.APBoost])
