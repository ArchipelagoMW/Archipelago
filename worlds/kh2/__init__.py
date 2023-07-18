from BaseClasses import Tutorial, ItemClassification
import logging

from Fill import fill_restrictive
from .Rules import *
from .Items import *
from .Locations import *
from .Names import ItemName, LocationName
from .OpenKH import patch_kh2
from .Options import KH2_Options
from .Regions import create_regions, connect_regions
# from .Rules import set_rules
from worlds.AutoWorld import World, WebWorld


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
    data_version = 0
    # TODO: remove this before release
    # topology_present = True

    required_client_version = (0, 4, 2)
    option_definitions = KH2_Options
    item_name_to_id = {item: item_id
                       for item_id, item in enumerate(item_dictionary_table.keys(), 0x130000)}
    location_name_to_id = {item: location
                           for location, item in enumerate(all_locations.keys(), 0x130000)}
    item_name_groups = item_groups

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)
        self.keyblade_ability_pool = None
        self.goofy_get_bonus_abilities = None
        self.goofy_weapon_abilities = None
        self.donald_get_bonus_abilities = None
        self.donald_weapon_abilities = None

        self.valid_abilities = None
        self.visitlocking_dict = None
        self.plando_locations = None
        self.lucky_emblem_amount = None
        self.lucky_emblem_required = None
        self.bounties_required = None
        self.bounties_amount = None
        self.hitlist = None
        self.random_super_boss_list = list()
        self.filler_items = list()
        self.item_quantity_dict = {}

        self.sora_keyblade_ability_pool = list()
        self.keyblade_slot_copy = list(Locations.Keyblade_Slots.keys())
        self.keyblade_slot_copy.remove(LocationName.KingdomKeySlot)
        self.total_locations = len(all_locations.keys())
        self.growth_list = list()
        for x in range(4):
            self.growth_list.extend(Movement_Table.keys())
        self.slot_data_duping = set()
        self.local_items = dict()

    def fill_slot_data(self) -> dict:
        # localItems filling done here for the unit test.
        for values in CheckDupingItems.values():
            if isinstance(values, set):
                self.slot_data_duping = self.slot_data_duping.union(values)
            else:
                for inner_values in values.values():
                    self.slot_data_duping = self.slot_data_duping.union(inner_values)
        self.local_items = {location.address: self.item_name_to_id[location.item.name]
                            for location in self.multiworld.get_filled_locations(self.player)
                            if location.item.player == self.player
                            and location.item.name in self.slot_data_duping
                            and location.name not in all_weapon_slot}

        return {
            "hitlist":              self.hitlist,
            "LocalItems":           self.local_items,
            "Goal":                 self.multiworld.Goal[self.player].value,
            "FinalXemnas":          self.multiworld.FinalXemnas[self.player].value,
            "LuckyEmblemsRequired": self.multiworld.LuckyEmblemsRequired[self.player].value,
            "BountyRequired":       self.multiworld.BountyRequired[self.player].value
        }

    def create_item(self, name: str) -> Item:
        """
        Returns created KH2Item
        """
        # data = item_dictionary_table[name]
        if name in progression_set:
            item_classification = ItemClassification.progression
        elif name in useful_set:
            item_classification = ItemClassification.useful
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
                for name in Movement_Table.keys():
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
                     for _ in range(self.total_locations - len(itempool))]
        self.multiworld.itempool += itempool

    def generate_early(self) -> None:
        """
        Determines the quantity of items and maps plando locations to items.
        """
        # Item: Quantity Map
        # Example. Quick Run: 4
        self.item_quantity_dict = {item: data.quantity for item, data in item_dictionary_table.items()}
        # Dictionary to mark locations with their plandoed item
        # Example. Final Xemnas: Victory
        self.plando_locations = dict()
        self.starting_invo_verify()

        # Option to turn off Promise Charm Item
        if not self.multiworld.Promise_Charm[self.player]:
            self.item_quantity_dict[ItemName.PromiseCharm] = 0

        self.set_excluded_locations()

        if self.multiworld.Goal[self.player] not in ["hitlist", "three_proofs"]:
            self.lucky_emblem_amount = self.multiworld.LuckyEmblemsAmount[self.player].value
            self.lucky_emblem_required = self.multiworld.LuckyEmblemsRequired[self.player].value
            self.emblem_verify()

        # hitlist
        if self.multiworld.Goal[self.player] not in ["lucky_emblem_hunt", "three_proofs"]:
            self.random_super_boss_list.extend(exclusion_table["Hitlist"])
            self.bounties_amount = self.multiworld.BountyAmount[self.player].value
            self.bounties_required = self.multiworld.BountyRequired[self.player].value

            self.hitlist_verify()
            prio_hitlist = [location for location in self.multiworld.priority_locations[self.player].value if location in self.random_super_boss_list]
            for bounty in range(self.bounties_amount):
                if prio_hitlist:
                    randomBoss = self.multiworld.per_slot_randoms[self.player].choice(prio_hitlist)
                    prio_hitlist.remove(randomBoss)
                else:
                    randomBoss = self.multiworld.per_slot_randoms[self.player].choice(self.random_super_boss_list)
                self.plando_locations[randomBoss] = ItemName.Bounty
                self.random_super_boss_list.remove(randomBoss)
                self.total_locations -= 1

        self.donald_gen_early()
        self.goofy_gen_early()
        self.keyblade_gen_early()

        if self.multiworld.FinalXemnas[self.player]:
            self.plando_locations[LocationName.FinalXemnas] = ItemName.Victory
        else:
            self.plando_locations[LocationName.FinalXemnas] = self.create_filler().name

        if self.multiworld.WeaponSlotStartHint[self.player]:
            for location in all_weapon_slot:
                self.multiworld.start_location_hints[self.player].value.add(location)
        # By imitating remote this doesn't have to be plandoded filler anymore
        #  for location in {LocationName.JunkMedal, LocationName.JunkMedal}:
        #    self.plando_locations[location] = random_stt_item
        self.level_subtraction()

    def pre_fill(self):
        """
        Plandoing Events and Fill_Restrictive for donald,goofy and sora
        """
        self.donald_pre_fill()
        self.goofy_pre_fill()
        self.keyblade_pre_fill()
        # self.item_name_to_id.update({event_name: None for event_name in Events_Table})
        for location, item in self.plando_locations.items():
            self.multiworld.get_location(location, self.player).place_locked_item(
                    self.create_item(item))

    def create_regions(self):
        """
        Creates the Regions and Connects them.
        """
        create_regions(self.multiworld, self.player, self.location_name_to_id)
        self.item_name_to_id.update({event_name: None for event_name in Events_Table})
        for location, item in event_location_to_item.items():
            self.multiworld.get_location(location, self.player).place_locked_item(
                    self.create_item(item))
        connect_regions(self.multiworld, self.player)

    def set_rules(self):
        """
        Sets the Logic for the Regions and Locations.
        """
        universal_logic = Rules.KH2Rules(self)
        form_logic = Rules.KH2FormRules(self)
        fight_rules = Rules.KH2FightRules(self)
        fight_rules.set_kh2_fight_rules()
        universal_logic.set_kh2_rules()
        form_logic.set_kh2_form_rules()

    def generate_output(self, output_directory: str):
        """
        Generates the .zip for OpenKH (The KH Mod Manager)
        """
        patch_kh2(self, output_directory)

    def donald_gen_early(self):
        random_prog_ability = self.multiworld.per_slot_randoms[self.player].choice([ItemName.Fantasia, ItemName.FlareForce])
        donald_master_ability = [donald_ability for donald_ability in DonaldAbility_Table.keys() for _ in range(self.item_quantity_dict[donald_ability]) if donald_ability != random_prog_ability]
        self.donald_weapon_abilities = []
        self.donald_get_bonus_abilities = []
        # fill goofy weapons first
        for _ in range(15):
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(donald_master_ability)
            donald_master_ability.remove(random_ability)
            self.donald_weapon_abilities += [self.create_item(random_ability)]
            self.item_quantity_dict[random_ability] -= 1

        if not self.multiworld.DonaldGoofyStatsanity[self.player]:
            # pre plando donald get bonuses
            self.total_locations -= 31
            self.donald_get_bonus_abilities += [self.create_item(random_prog_ability)]
            for item_name in donald_master_ability:
                self.donald_get_bonus_abilities += [self.create_item(item_name)]
                self.item_quantity_dict[item_name] -= 1
        else:
            self.total_locations -= 16

    def goofy_gen_early(self):
        random_prog_ability = self.multiworld.per_slot_randoms[self.player].choice([ItemName.Teamwork, ItemName.TornadoFusion])
        goofy_master_ability = [goofy_ability for goofy_ability in GoofyAbility_Table.keys() for _ in range(self.item_quantity_dict[goofy_ability]) if goofy_ability != random_prog_ability]
        self.goofy_weapon_abilities = []
        self.goofy_get_bonus_abilities = []
        # fill goofy weapons first
        for _ in range(15):
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(goofy_master_ability)
            goofy_master_ability.remove(random_ability)
            self.goofy_weapon_abilities += [self.create_item(random_ability)]
            self.item_quantity_dict[random_ability] -= 1

        if not self.multiworld.DonaldGoofyStatsanity[self.player]:
            # pre plando goofy get bonuses
            self.total_locations -= 32
            self.goofy_get_bonus_abilities += [self.create_item(random_prog_ability)]
            for item_name in goofy_master_ability:
                self.goofy_get_bonus_abilities += [self.create_item(item_name)]
                self.item_quantity_dict[item_name] -= 1
        else:
            self.total_locations -= 16

        if len(self.goofy_weapon_abilities) <= 3:
            raise Exception("uh oh")

    def keyblade_gen_early(self):
        keyblade_master_ability = [ability for ability in SupportAbility_Table.keys() if ability not in progression_set for _ in range(self.item_quantity_dict[ability])]
        self.keyblade_ability_pool = []
        for _ in range(len(Keyblade_Slots)):
            random_ability = self.multiworld.per_slot_randoms[self.player].choice(keyblade_master_ability)
            keyblade_master_ability.remove(random_ability)
            self.keyblade_ability_pool += [self.create_item(random_ability)]
            self.item_quantity_dict[random_ability] -= 1
        self.total_locations -= 27

    def goofy_pre_fill(self):
        """
        Removes donald locations from the location pool maps random donald items to be plandoded.
        """
        goofy_weapon_location_list = [self.multiworld.get_location(location, self.player) for location in Goofy_Checks.keys() if Goofy_Checks[location].yml == "Keyblade"]

        # take one of the 2 out
        # randomize the list with only
        state = self.multiworld.get_all_state(False)
        fill_restrictive(self.multiworld, state, goofy_weapon_location_list, self.goofy_weapon_abilities, True, True, allow_excluded=True)
        if not self.multiworld.DonaldGoofyStatsanity:
            # plando goofy get bonuses
            goofy_get_bonus_location_pool = [self.multiworld.get_location(location, self.player) for location in Goofy_Checks.keys() if Goofy_Checks[location].yml != "Keyblade"]
            state2 = self.multiworld.get_all_state(False)
            fill_restrictive(self.multiworld, state2, goofy_get_bonus_location_pool, self.goofy_get_bonus_abilities, True, True)

    def donald_pre_fill(self):
        donald_weapon_location_list = [self.multiworld.get_location(location, self.player) for location in Donald_Checks.keys() if Donald_Checks[location].yml == "Keyblade"]

        # take one of the 2 out
        # randomize the list with only
        state = self.multiworld.get_all_state(False)
        fill_restrictive(self.multiworld, state, donald_weapon_location_list, self.donald_weapon_abilities, allow_excluded=True)
        if not self.multiworld.DonaldGoofyStatsanity:
            # plando goofy get bonuses
            donald_get_bonus_location_pool = [self.multiworld.get_location(location, self.player) for location in Donald_Checks.keys() if Donald_Checks[location].yml != "Keyblade"]
            state2 = self.multiworld.get_all_state(False)
            fill_restrictive(self.multiworld, state2, donald_get_bonus_location_pool, self.donald_get_bonus_abilities, True, True)

    def keyblade_pre_fill(self):
        """
        Fills keyblade slots with abilities determined on player's setting
        """
        keyblade_locations = [self.multiworld.get_location(location, self.player) for location in Keyblade_Slots.keys()]
        state = self.multiworld.get_all_state(False)
        fill_restrictive(self.multiworld, state, keyblade_locations, self.keyblade_ability_pool, True, True)

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
        if self.lucky_emblem_amount < self.lucky_emblem_required:
            logging.info(
                    f"Lucky Emblem Amount {self.multiworld.LuckyEmblemsAmount[self.player].value} is less than required "
                    f"{self.multiworld.LuckyEmblemsRequired[self.player].value} for player {self.multiworld.get_file_safe_player_name(self.player)}."
                    f" Setting amount to {self.multiworld.LuckyEmblemsRequired[self.player].value}")
            luckyemblemamount = max(self.lucky_emblem_amount, self.lucky_emblem_required)
            self.multiworld.LuckyEmblemsAmount[self.player].value = luckyemblemamount

        self.item_quantity_dict[ItemName.LuckyEmblem] = self.multiworld.LuckyEmblemsAmount[self.player].value
        # give this proof to unlock the final door once the player has the amount of lucky emblem required
        self.item_quantity_dict[ItemName.ProofofNonexistence] = 0

    def hitlist_verify(self):
        """
        Making sure hitlist have amount>=required.
        """
        for location in self.multiworld.exclude_locations[self.player].value:
            if location in self.random_super_boss_list:
                self.random_super_boss_list.remove(location)

        #  Testing if the player has the right amount of Bounties for Completion.
        if len(self.random_super_boss_list) < self.bounties_amount:
            logging.info(
                    f"{self.multiworld.get_file_safe_player_name(self.player)} has more bounties than bosses."
                    f" Setting total bounties to {len(self.random_super_boss_list)}")
            self.bounties_amount = len(self.random_super_boss_list)
            self.multiworld.BountyAmount[self.player].value = self.bounties_amount

        if len(self.random_super_boss_list) < self.bounties_required:
            logging.info(f"{self.multiworld.get_file_safe_player_name(self.player)} has too many required bounties."
                         f" Setting required bounties to {len(self.random_super_boss_list)}")
            self.bounties_required = len(self.random_super_boss_list)
            self.multiworld.BountyRequired[self.player].value = self.bounties_required

        if self.bounties_amount < self.bounties_required:
            logging.info(f"Bounties Amount is less than required for player {self.multiworld.get_file_safe_player_name(self.player)}."
                         f"Swapping Amount and Required")
            temp = self.multiworld.BountyRequired[self.player].value
            self.multiworld.BountyRequired[self.player].value = self.multiworld.BountyAmount[self.player].value
            self.multiworld.BountyRequired[self.player].value = temp

        if self.multiworld.BountyStartingHintToggle[self.player]:
            self.multiworld.start_hints[self.player].value.add(ItemName.Bounty)

        self.item_quantity_dict[ItemName.ProofofNonexistence] = 0

    def set_excluded_locations(self):
        """
        Fills excluded_locations from player's settings.
        """
        # Option to turn off all superbosses. Can do this individually but its like 20+ checks
        if not self.multiworld.SuperBosses[self.player]:
            for superboss in exclusion_table["SuperBosses"]:
                self.multiworld.exclude_locations[self.player].value.add(superboss)

        # Option to turn off Olympus Colosseum Cups.
        if self.multiworld.Cups[self.player] == "no_cups":
            for cup in exclusion_table["Cups"]:
                self.multiworld.exclude_locations[self.player].value.add(cup)
        # exclude only hades paradox. If cups and hades paradox then nothing is excluded
        elif self.multiworld.Cups[self.player] == "cups":
            self.multiworld.exclude_locations[self.player].value.add(LocationName.HadesCupTrophyParadoxCups)

        if not self.multiworld.AtlanticaToggle[self.player]:
            for loc in exclusion_table["Atlantica"]:
                self.multiworld.exclude_locations[self.player].value.add(loc)

    def level_subtraction(self):
        """
        Determine how many locations are on sora's levels.
        """
        if self.multiworld.LevelDepth[self.player] == "level_50_sanity":
            # level 50 sanity
            self.total_locations -= 49
        elif self.multiworld.LevelDepth[self.player] == "level_1":
            # level 1. No checks on levels
            self.total_locations -= 98
        elif self.multiworld.LevelDepth[self.player] != "level_99_sanity":
            # level 50/99 since they contain the same amount of levels
            self.total_locations -= 75

    def get_filler_item_name(self) -> str:
        """
        Returns random filler item name.
        """
        return self.multiworld.random.choice([ItemName.PowerBoost, ItemName.MagicBoost, ItemName.DefenseBoost, ItemName.APBoost,
                                              ItemName.Potion, ItemName.HiPotion, ItemName.Ether, ItemName.Elixir, ItemName.Megalixir,
                                              ItemName.Tent, ItemName.DriveRecovery, ItemName.HighDriveRecovery,
                                              ])
