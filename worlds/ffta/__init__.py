"""
Archipelago World definition for Final Fantasy Tactics Advance
"""

import os
from typing import ClassVar, Dict, Any, Union, Tuple, Optional
from itertools import chain
import settings
import sys
import logging
from Utils import visualize_regions
from random import Random

from .client import FFTAClient

from BaseClasses import ItemClassification, MultiWorld, Tutorial, Item
from worlds.AutoWorld import WebWorld, World
from .data import (get_random_job, JobID, attacker_jobs, magic_jobs, support_jobs, human_abilities, bangaa_abilities,
                   nu_mou_abilities, viera_abilities, moogle_abilities, monster_abilities)
from .regions import create_regions
from .rules import set_rules
from .fftaabilities import (human_abilities_bitflags, bangaa_abilities_bitflags, nu_mou_abilities_bitflags,
                            viera_abilities_bitflags, moogle_abilities_bitflags)

from .options import (FFTAOptions, StartingUnits, StartingUnitEquip, StartingAbilitiesMastered, JobUnlockReq,
                      RandomEnemies, EnemyScaling, StartingGil, GateNumber, GatePaths, DispatchMissions,
                      DispatchRandom, GateUnlock, MissionOrder, FinalMission, Goal, QuickOptions,
                      ForceRecruitment, ProgressiveGateItems, AbilityRandom)
from .items import (create_item_label_to_code_map, AllItems, item_table, FFTAItem, WeaponBlades,
                    WeaponSabers, WeaponKatanas, WeaponBows, WeaponGreatBows, WeaponRods, WeaponStaves, WeaponKnuckles,
                    WeaponMaces, WeaponInstruments, WeaponSouls, WeaponRapiers, WeaponGuns, WeaponKnives, ItemData,
                    EquipArmor, EquipRobes, EquipClothing, MissionUnlockItems, TotemaUnlockItems,
                    SoldierWeapons, PaladinWeapons, WarriorWeapons, DefenderWeapons, TemplarWeapons, AssassinWeapons,
                    DragoonWeapons, itemGroups, JobUnlocks, LawCards)
from .locations import (create_location_label_to_id_map)
from .rom import FFTAProcedurePatch, generate_output


class FFTAWebWorld(WebWorld):
    """
    Webhost info for Final Fantasy Tactics Advance
    """
    theme = "grass"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Final Fantasy Tactics Advance with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Spicynun"]
    )

    tutorials = [setup_en]


class FFTASettings(settings.Group):
    class FFTARomFile(settings.UserFilePath):
        """File name of your Final Fantasy Tactics Advance ROM"""
        description = "Final Fantasy Tactics Advance ROM File"
        copy_to = "Final Fantasy Tactics Advance (USA).gba"
        md5s = [FFTAProcedurePatch.hash]

    rom_file: FFTARomFile = FFTARomFile(FFTARomFile.copy_to)


class FFTAWorld(World):
    """
    Final Fantasy Tactics Advance is a game
    """
    game = "Final Fantasy Tactics Advance"
    web = FFTAWebWorld()
    topology_present = False

    settings_key = "ffta_options"
    settings: ClassVar[FFTASettings]

    options_dataclass = FFTAOptions
    options: FFTAOptions

    required_client_version = (0, 4, 4)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()

    def __init__(self, multiworld, player):
        super(FFTAWorld, self).__init__(multiworld, player)
        self.randomized_jobs = []
        self.balanced_jobs = []
        self.randomized_judge = []
        self.judge_weapon = []
        self.judge_equip = []
        self.randomized_weapons = []
        self.randomized_equip = []
        self.basic_weapon = []
        self.basic_equip = []
        self.MissionGroups = []
        self.DispatchMissionGroups = []
        self.location_ids = []
        self.path1_length = []
        self.path2_length = []
        self.path3_length = []
        self.path_items = []
        self.shop_tiers = []
        self.human_ability_dict = {}
        self.bangaa_ability_dict = {}
        self.nu_mou_ability_dict = {}
        self.viera_ability_dict = {}
        self.moogle_ability_dict = {}
        self.human_abilities = []
        self.bangaa_abilities = []
        self.nu_mou_abilities = []
        self.viera_abilities = []
        self.moogle_abilities = []
        self.new_human_abilities = []
        self.new_bangaa_abilities = []
        self.new_nu_mou_abilities = []
        self.new_viera_abilities = []
        self.new_moogle_abilities = []
        self.all_abilities = []
        self.recruit_units = [0x03, 0x0f, 0x17, 0x20, 0x29]
        self.recruit_secret = [0x03, 0x0f, 0x17, 0x20, 0x29, 0x8a, 0x8c, 0x8e,
                               0x90, 0x92, 0x94, 0x96, 0x98, 0x9a, 0x9c, 0x9e]
        self.special_units = [0x04, 0x09, 0x0a, 0x0c, 0x0d, 0x5a, 0x5e]

        self.seed = getattr(multiworld, "re_gen_passthrough", {}).get("Final Fantasy Tactics Advance", self.random.getrandbits(64))
        self.random = Random(self.seed)

    def interpret_slot_data(self, slot_data: Dict[str, Any]) -> Optional[int]:
        seed = slot_data.get("universal_tracker_seed")
        if seed is None:
            print("This game was generated before Universal Tracker support")
        return seed

    def get_filler_item_name(self) -> str:
        filler = ["Potion", "Hi-Potion", "X-Potion", "Ether", "Elixir", "Antidote",
                  "Eye Drops", "Echo Screen", "Maiden's Kiss", "Soft", "Holy Water", "Bandage",
                  "Cureall", "Phoenix Down"]
        return self.random.choice(filler)

    def create_regions(self) -> None:
        create_regions(self, self.player)

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]) -> None:
        hint_data.update({self.player: {}})
        for location in self.multiworld.get_locations(self.player):
            if location.address is not None:
                hint_data[self.player][location.address] = location.parent_region.hint_text

    def create_items(self):

        required_items = self.get_required_items()

        # Count number of mission reward locations, account for totema goal
        gate_number = self.options.gate_num.value
        if gate_number > 30 and self.options.goal == Goal.option_totema:
            gate_number = 30

        dispatch_number = self.options.dispatch.value * self.options.mission_reward_num.value
        unfilled_locations = gate_number * self.options.mission_reward_num.value * 4 + gate_number * dispatch_number + 1

        # Add totema mission locations to unfilled location count
        if self.options.goal == Goal.option_totema:
            unfilled_locations += self.options.mission_reward_num.value * 5

        # Add extra locations for multiple gate paths
        unfilled_locations += self.options.mission_reward_num.value * (self.options.gate_paths.value - 1)

        items_remaining = unfilled_locations - len(required_items)

        path_index = 0
        paths = ["Progressive Path 1", "Progressive Path 2", "Progressive Path 3"]
        if self.options.gate_items.value == 2 and self.options.dispatch.value > 0:
            paths.append("Progressive Dispatch")

        # Prevent putting more items than locations into the pool with excess progressive items
        while items_remaining <= 0:
            index = required_items.index(paths[path_index])
            del required_items[index]
            if self.options.gate_items.value == 2 and path_index == 3:
                path_index = 0
            elif path_index == 2:
                path_index = 0
            else:
                path_index += 1
            items_remaining = unfilled_locations - len(required_items)

        # Adding required items to the pool first
        for itemName in required_items:
            self.multiworld.itempool.append(self.create_item(itemName))

        useful_items = []
        for item in AllItems:
            if item.progression == ItemClassification.useful:

                if self.options.law_cards.value == 0:
                    if item in LawCards:
                        continue

                #if self.options.job_unlock_req != JobUnlockReq.option_job_items:
                if item in JobUnlocks:
                    continue

                useful_items += [item.itemName]

        # Shuffle the useful items to be added to the pool based on the locations remaining
        self.random.shuffle(useful_items)

        for i in range(items_remaining - 1):
            if i > len(useful_items) - 1:
                self.multiworld.itempool.append(self.create_filler())
            else:
                self.multiworld.itempool.append(self.create_item(useful_items[i]))

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        # Setting the victory item at the victory location
        victory_event = FFTAItem('Victory', ItemClassification.progression, None, self.player)

        if self.options.final_mission == FinalMission.option_royal_valley:
            self.multiworld.get_location("Royal Valley", self.player)\
                .place_locked_item(victory_event)

        elif self.options.final_mission == FinalMission.option_decision_time:
            self.multiworld.get_location("Decision Time", self.player) \
                .place_locked_item(victory_event)

        self.multiworld.completion_condition[self.player] =\
            lambda state: state.has("Victory", self.player)

        if self.options.gate_paths.value > 1:
            for i in range(1, self.options.gate_paths.value + 1):
                path_complete = FFTAItem(f"Path {i} Complete", ItemClassification.progression, None, self.player)
                self.multiworld.get_location(f"Path {i} Completion", self.player) \
                    .place_locked_item(path_complete)

    def get_required_items(self):
        required_items = []

        item_index = 0
        req_gate_num = self.options.gate_num.value

        # Add progression items with multiple mission gate paths
        req_gate_num += self.options.gate_paths.value - 1

        if self.options.progressive_gates.value == ProgressiveGateItems.option_true:
            gates_per_path = [req_gate_num // self.options.gate_paths.value] * self.options.gate_paths.value
            if req_gate_num % self.options.gate_paths.value >= 1:
                gates_per_path[0] += 1
            if req_gate_num % self.options.gate_paths.value >= 2:
                gates_per_path[1] += 1

            for path in range(0, self.options.gate_paths.value):
                items_per_gate = 2 if self.options.gate_items == GateUnlock.option_two else 1
                progressives_required = [f"Progressive Path {path+1}"] * (gates_per_path[path] * items_per_gate +
                                                                          self.options.progressive_item_num.value)
                required_items.extend(progressives_required)

            if self.options.gate_items == GateUnlock.option_dispatch_gate and self.options.dispatch.value > 0:
                req_dispatch_gate_num = req_gate_num - (self.options.gate_paths.value - 1)
                progressives_required = ["Progressive Dispatch"] * (req_dispatch_gate_num +
                                                                    self.options.progressive_item_num.value)
                required_items.extend(progressives_required)

            self.set_progressive_lists(req_gate_num, gates_per_path)
        else:
            for i in range(0, req_gate_num):
                required_items.append(MissionUnlockItems[item_index].itemName)

                # Add second item for the gate unlock
                if self.options.gate_items == GateUnlock.option_two or \
                        (self.options.gate_items == GateUnlock.option_dispatch_gate and self.options.dispatch.value > 0):
                    required_items.append(MissionUnlockItems[item_index + 1].itemName)

                item_index += 2

        # Add totema unlock items to pool if option is selected
        if self.options.goal == Goal.option_totema:
            for i in range(0, len(TotemaUnlockItems)):
                required_items.append(TotemaUnlockItems[i].itemName)

        if self.options.progressive_shop.value == 1:
            self.get_progressive_shop_items(required_items)

        return required_items

    def get_progressive_shop_items(self, required_items):
        itemSet = set()
        # Go through lists in reverse so later values take priority
        item_groups = []
        random_items = []
        for i, tier in enumerate(self.options.progressive_shop_tiers.value):
            item_groups_tier = []
            random_items_tier = []
            tier_items = []
            for shop_item in tier:
                if shop_item[0] in itemGroups:
                    item_groups_tier.append(shop_item)
                    continue
                elif shop_item[0] == "random" or shop_item[0].startswith("random-"):
                    random_items_tier.append(shop_item)
                    continue
                new_item = self.prepare_shop_item(shop_item, itemSet)
                if new_item is not None:
                    tier_items.append(new_item)

            self.shop_tiers.append(tier_items)
            item_groups.append(item_groups_tier)
            random_items.append(random_items_tier)
            # No item for the first tier, and 2 less items if ProgressiveShopBattleUnlock is set to replace
            if i > 0 and \
                (self.options.progressive_shop_battle_unlock.value !=
                 self.options.progressive_shop_battle_unlock.option_replacing or i > 2):
                required_items.append("Progressive Shop")

        for index, tier in enumerate(item_groups):
            for group_name, group_price in tier:
                group_items = itemGroups.get(group_name)
                for item_name in group_items:
                    shop_item = (item_name, group_price)
                    new_item = self.prepare_shop_item(shop_item, itemSet)
                    if new_item is not None:
                        self.shop_tiers[index].append(new_item)

        for index, tier in enumerate(random_items):
            for item_name, item_price in tier:
                textsplit = item_name.split("-")
                random_group = set()
                random_range = []
                for arg in textsplit[1:]:
                    if arg in itemGroups:
                        random_group |= set(itemGroups.get(arg))
                    else:
                        try:
                            asInt = int(arg)
                        except ValueError:
                            raise ValueError(f"Invalid item group {arg}")
                        random_range.append(asInt)
                if len(random_range) > 2:
                    raise ValueError(f"Invalid random range {range}")
                elif len(random_range) == 2:
                    random_range.sort()
                    if random_range[0] < 1 or random_range[1] > len(random_group):
                        raise Exception(
                            f"{random_range[0]}-{random_range[1]} is outside allowed range "
                            f"{1}-{len(random_group)} in {item_name}")
                    choice_num = self.random.randint(random_range[0], random_range[1])
                else:
                    choice_num = random_range[0]

                random_group -= itemSet
                chosen_items = self.random.sample(list(random_group), choice_num)
                for chosen_item in chosen_items:
                    shop_item = (chosen_item, item_price)
                    new_item = self.prepare_shop_item(shop_item, itemSet)
                    if new_item is not None:
                        self.shop_tiers[index].append(new_item)

    def prepare_shop_item(self, shop_item, itemSet) -> Union[Tuple[ItemData, int], None]:
        try:
            item = item_table[shop_item[0]]
        except KeyError:
            raise KeyError(f"'{shop_item[0]}' not found")
        if shop_item[0] in itemSet:
            print(f"{shop_item[0]} already added")
            return None
        else:
            itemSet.add(shop_item[0])
        item_price = shop_item[1]
        if isinstance(item_price, str):

            if item_price.startswith("random-range-"):
                min_price, max_price = self.parse_range(item_price, 0x0001, 0xFFFF)

                price_split = item_price.split("-")
                if price_split[2] in ["low", "mid", "high"]:
                    item_price = f"random-{price_split[2]}"
                else:
                    item_price = "random"
            else:
                min_price, max_price = (0x0001, 0xFFFF)

            if item_price == "default":
                item_price = -1
            elif item_price == "random":
                item_price = self.random.randint(min_price, max_price)
            elif item_price == "random-low":
                item_price = self.random.triangular(min_price, max_price, min_price)
            elif item_price == "random-high":
                item_price = self.random.triangular(min_price, max_price, max_price)
            elif item_price == "random-middle":
                item_price = self.random.triangular(min_price, max_price)
            item_price = int(round(item_price))

        return (item, item_price)

    def parse_range(self, text, range_start, range_end):
        textsplit = text.split("-")
        try:
            random_range = [int(textsplit[len(textsplit) - 2]), int(textsplit[len(textsplit) - 1])]
        except ValueError:
            raise ValueError(f"Invalid random range {text}")
        random_range.sort()
        if random_range[0] < range_start or random_range[1] > range_end:
            raise Exception(
                f"{random_range[0]}-{random_range[1]} is outside allowed range "
                f"{range_start}-{range_end}")
        return random_range[0], random_range[1]

    def fill_slot_data(self) -> Dict[str, Any]:

        slot_data = self.options.as_dict(
            "final_mission",
            "job_unlock_req",
            "progressive_gates",
            "progressive_shop",
            "progressive_shop_tiers",
            "law_cards"
        )

        slot_data["universal_tracker_seed"] = self.seed

        return slot_data

    def create_item(self, name: str) -> Item:
        item = item_table[name]
        # Maybe remove this later
        offset = 41234532
        return FFTAItem(item.itemName, item.progression, item.itemID + offset, self.player)

    def set_progressive_lists(self, req_gate_num, gates_per_path):
        # path_items must have 4 arrays, unused paths are simply empty. 4th element is for Dispatch path
        self.path_items = [[], [], [], []]
        for path in range(0, self.options.gate_paths.value):
            item_index = path*2
            path_items = []
            for i in range(0, gates_per_path[path]):
                path_items.append(MissionUnlockItems[item_index])
                if self.options.gate_items == GateUnlock.option_two:
                    path_items.append(MissionUnlockItems[item_index+1])
                item_index += self.options.gate_paths.value*2
            self.path_items[path] = path_items
            #self.path_items.append(path_items)

        if self.options.gate_items == GateUnlock.option_dispatch_gate and self.options.dispatch.value > 0:
            req_dispatch_gate_num = req_gate_num - (self.options.gate_paths.value - 1)
            item_index = 1
            path_items = []
            for i in range(0, req_dispatch_gate_num):
                if item_index >= len(MissionUnlockItems):
                    break
                path_items.append(MissionUnlockItems[item_index])
                item_index += 2
            self.path_items[3] = path_items
            #self.path_items.append(path_items)

    def generate_output(self, output_directory: str) -> None:
        # Import this from data instead
        human = 0
        bangaa = 1
        mou = 2
        viera = 3
        moogle = 4
        monster = 5
        all = 6
        all_with_monster = 7

        if self.options.starting_units == StartingUnits.option_starting_balanced:
            self.balanced_jobs.append(self.random.choice(attacker_jobs))
            self.balanced_jobs.append(self.random.choice(attacker_jobs))
            self.balanced_jobs.append(self.random.choice(magic_jobs))
            self.balanced_jobs.append(self.random.choice(magic_jobs))
            self.balanced_jobs.append(self.random.choice(support_jobs))
            self.balanced_jobs.append(self.random.choice(support_jobs))
            self.random.shuffle(self.balanced_jobs)

        def randomize_starting(random_choice: int):

            # Randomize job for Marche

            # Add balanced job if selected
            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[0])

            # Prevent Marche from being rolled into a monster
            elif self.options.starting_units == StartingUnits.option_random_monster:
                self.randomized_jobs.append(get_random_job(self.random, all))

            # Account for vanilla soldier job
            elif self.options.starting_units == StartingUnits.option_starting_vanilla:
                self.randomized_jobs.append(JobID.soldier)

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[0]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[0]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[0]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[0]))

            # Randomize job for Montblanc

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[1])

            # Prevent Montblanc from being rolled into a monster
            elif self.options.starting_units == StartingUnits.option_random_monster:
                self.randomized_jobs.append(get_random_job(self.random, all))

            # Account for vanilla job
            elif self.options.starting_units == StartingUnits.option_starting_vanilla:
                self.randomized_jobs.append(JobID.blackmagemog)

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:

                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[1]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[1]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[1]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[1]))

            # Randomize job for third clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[2])

            elif self.options.starting_units == StartingUnits.option_starting_vanilla:
                self.randomized_jobs.append(JobID.soldier)

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[2]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[2]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[2]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[2]))

            # Randomize job for fourth clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[3])

            elif self.options.starting_units == StartingUnits.option_starting_vanilla:
                self.randomized_jobs.append(JobID.whitemonk)

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[3]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[3]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[3]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[3]))

            # Randomize job for fifth clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[4])

            elif self.options.starting_units == StartingUnits.option_starting_vanilla:
                self.randomized_jobs.append(JobID.whitemagemou)

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[4]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[4]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[4]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[4]))

            # Randomize job for sixth clan member

            if self.options.starting_units == StartingUnits.option_starting_balanced:
                self.randomized_jobs.append(self.balanced_jobs[5])

            elif self.options.starting_units == StartingUnits.option_starting_vanilla:
                self.randomized_jobs.append(JobID.archervra)

            else:
                self.randomized_jobs.append(get_random_job(self.random, random_choice))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[5]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[5]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[5]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[5]))

        def get_valid_weapon(job: int):

            weapon: ItemData

            # Soldier
            if job == JobID.soldier:
                weapon = self.random.choice(SoldierWeapons)
                return weapon.itemID

            # Paladin
            elif job == JobID.paladin:
                weapon = self.random.choice(PaladinWeapons)
                return weapon.itemID

            # Fighter
            elif job == JobID.fighter:
                weapon = self.random.choice(WeaponBlades)
                return weapon.itemID

            # Thief
            elif job == JobID.thiefhum or job == JobID.thiefmog or job == JobID.juggler:
                weapon = self.random.choice(WeaponKnives)
                return weapon.itemID

            # Ninja and assassins
            elif job == JobID.ninja:
                weapon = self.random.choice(WeaponKatanas)
                return weapon.itemID

            # White mage
            elif job == JobID.whitemagehum or job == JobID.whitemagemou or job == JobID.whitemagevra or job == JobID.summoner:
                weapon = self.random.choice(WeaponStaves)
                return weapon.itemID

            # Rod users
            elif job == JobID.blackmagehum or job == JobID.illusionisthum or job == JobID.blackmagemou \
                    or job == JobID.timemagemou or job == JobID.illusionistmou or job == JobID.blackmagemog or job == JobID.timemagemog:
                weapon = self.random.choice(WeaponRods)
                return weapon.itemID

            # Blue mage
            elif job == JobID.bluemage:
                weapon = self.random.choice(WeaponSabers)
                return weapon.itemID

            # Archer
            elif job == JobID.archerhum or job == JobID.archervra:
                weapon = self.random.choice(WeaponBows)
                return weapon.itemID

            # Hunter or Snipers
            elif job == JobID.hunter or job == JobID.sniper:
                weapon = self.random.choice(WeaponGreatBows)
                return weapon.itemID

            # Warrior
            elif job == JobID.warrior:
                weapon = self.random.choice(WarriorWeapons)
                return weapon.itemID

            # Dragoon
            elif job == JobID.dragoon:
                weapon = self.random.choice(DragoonWeapons)
                return weapon.itemID

            # Defender
            elif job == JobID.defender:
                weapon = self.random.choice(DefenderWeapons)
                return weapon.itemID

            # Gladiator and Mog Knight
            elif job == JobID.gladiator or job == JobID.mogknight:
                weapon = self.random.choice(WeaponBlades)
                return weapon.itemID

            # White monk and gadgeteer
            elif job == JobID.whitemonk or job == JobID.gadgeteer:
                weapon = self.random.choice(WeaponKnuckles)
                return weapon.itemID

            # Bishop
            elif job == JobID.bishop:
                weapon = self.random.choice(WeaponStaves)
                return weapon.itemID

            # Templar
            elif job == JobID.templar:
                weapon = self.random.choice(TemplarWeapons)
                return weapon.itemID

            # Alchemist and sage
            elif job == JobID.alchemist or job == JobID.sage:
                weapon = self.random.choice(WeaponMaces)
                return weapon.itemID

            # Beasmaster or animist
            elif job == JobID.beastmaster or job == JobID.animist:
                weapon = self.random.choice(WeaponInstruments)
                return weapon.itemID

            # Morpher
            elif job == JobID.morpher:
                weapon = self.random.choice(WeaponSouls)
                return weapon.itemID

            # Fencer, red mage and Elementalist
            elif job == JobID.fencer or job == JobID.elementalist or job == JobID.redmage:
                weapon = self.random.choice(WeaponRapiers)
                return weapon.itemID

            # Assassin
            elif job == JobID.assassin:
                weapon = self.random.choice(AssassinWeapons)
                return weapon.itemID

            # Gunner
            elif job == JobID.gunner:
                weapon = self.random.choice(WeaponGuns)
                return weapon.itemID

            else:
                weapon = 0
                return weapon

        def get_basic_weapon(job: int):

            weapon: ItemData

            # Soldier
            if job == JobID.soldier:
                return SoldierWeapons[0].itemID

            # Paladin
            elif job == JobID.paladin:
                return PaladinWeapons[0].itemID

            # Fighter
            elif job == JobID.fighter:
                return WeaponBlades[0].itemID

            # Thief
            elif job == JobID.thiefhum or job == JobID.thiefmog or job == JobID.juggler:
                return WeaponKnives[0].itemID

            # Ninja
            elif job == JobID.ninja:
                return WeaponKatanas[0].itemID

            # White mage
            elif job == JobID.whitemagehum or job == JobID.whitemagemou or job == JobID.whitemagevra or job == JobID.summoner:
                return WeaponStaves[0].itemID

            # Rod users
            elif job == JobID.blackmagehum or job == JobID.illusionisthum or job == JobID.blackmagemou \
                    or job == JobID.timemagemou or job == JobID.illusionistmou or job == JobID.blackmagemog or job == JobID.timemagemog:
                return WeaponRods[0].itemID

            # Blue mage
            elif job == JobID.bluemage:
                return WeaponSabers[0].itemID

            # Archer
            elif job == JobID.archerhum or job == JobID.archervra:
                return WeaponBows[0].itemID

            # Hunter or Snipers
            elif job == JobID.hunter or job == JobID.sniper:
                return WeaponGreatBows[0].itemID

            # Warrior
            elif job == JobID.warrior:
                return WarriorWeapons[0].itemID

            # Dragoon
            elif job == JobID.dragoon:
                return DragoonWeapons[0].itemID

            # Defender
            elif job == JobID.defender:
                return DefenderWeapons[0].itemID

            # Gladiator and Mog Knight
            elif job == JobID.gladiator or job == JobID.mogknight:
                return WeaponBlades[0].itemID

            # White monk and gadgeteer
            elif job == JobID.whitemonk or job == JobID.gadgeteer:
                return WeaponKnuckles[0].itemID

            # Bishop
            elif job == JobID.bishop:
                return WeaponStaves[0].itemID

            # Templar
            elif job == JobID.templar:
                return TemplarWeapons[0].itemID

            # Alchemist and sage
            elif job == JobID.alchemist or job == JobID.sage:
                return WeaponMaces[0].itemID

            # Beasmaster or animist
            elif job == JobID.beastmaster or job == JobID.animist:
                return WeaponInstruments[0].itemID

            # Morpher
            elif job == JobID.morpher:
                return WeaponSouls[0].itemID

            # Fencer, red mage and Elementalist
            elif job == JobID.fencer or job == JobID.elementalist or job == JobID.redmage:
                return WeaponRapiers[0].itemID

            # Assassin
            elif job == JobID.assassin:
                return AssassinWeapons[0].itemID

            # Gunner
            elif job == JobID.gunner:
                return WeaponGuns[0].itemID

            else:
                weapon = 0
                return weapon

        def get_valid_equip(job: int):
            equip: ItemData

            armor_valid_jobs = [JobID.soldier, JobID.paladin, JobID.warrior, JobID.templar, JobID.dragoon,
                                JobID.defender, JobID.mogknight]

            robe_valid_jobs = [JobID.paladin, JobID.whitemagehum, JobID.whitemagevra, JobID.whitemagevra,
                               JobID.blackmagehum, JobID.blackmagemou, JobID.blackmagemog, JobID.illusionisthum,
                               JobID.illusionistmou, JobID.bluemage, JobID.defender,
                               JobID.bishop, JobID.templar, JobID.timemagemou, JobID.timemagemog, JobID.morpher,
                               JobID.sage, JobID.elementalist, JobID.redmage, JobID.summoner]

            for x in armor_valid_jobs:
                if job == x:
                    equip = self.random.choice(EquipArmor)
                    return equip.itemID

            for x in robe_valid_jobs:
                if job == x:
                    equip = self.random.choice(EquipRobes)
                    return equip.itemID

            if job < 0x2B:
                equip = self.random.choice(EquipClothing)
                return equip.itemID

            else:
                equip = 0
                return equip

        def get_basic_equip(job: int):
            equip: ItemData

            armor_valid_jobs = [JobID.soldier, JobID.paladin, JobID.warrior, JobID.templar, JobID.dragoon,
                                JobID.defender, JobID.mogknight]

            robe_valid_jobs = [JobID.paladin, JobID.whitemagehum, JobID.whitemagevra, JobID.whitemagevra,
                               JobID.blackmagehum, JobID.blackmagemou, JobID.blackmagemog, JobID.illusionisthum,
                               JobID.illusionistmou, JobID.bluemage, JobID.defender,
                               JobID.bishop, JobID.templar, JobID.timemagemou, JobID.timemagemog, JobID.morpher,
                               JobID.sage, JobID.elementalist, JobID.redmage, JobID.summoner]

            for x in armor_valid_jobs:
                if job == x:
                    return EquipArmor[0].itemID

            for x in robe_valid_jobs:
                if job == x:
                    return EquipRobes[0].itemID

            if job < 0x2B:
                return EquipClothing[0].itemID

            else:
                equip = 0
                return equip

        # Append randomized units even if randomization is turned off to allow for random enemies to work
        if self.options.starting_units == StartingUnits.option_starting_vanilla or \
           self.options.starting_units == StartingUnits.option_starting_random or \
           self.options.starting_units == StartingUnits.option_starting_balanced:
            randomize_starting(all)

        # Shuffle starting unit jobs within their race
        elif self.options.starting_units == StartingUnits.option_starting_shuffle:
            self.randomized_jobs.append(get_random_job(self.random, human))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[0]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[0]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[0]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[0]))

            # Randomize job for Montblanc
            self.randomized_jobs.append(get_random_job(self.random, moogle))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[1]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[1]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[1]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[1]))

            # Randomize job for third clan member
            self.randomized_jobs.append(get_random_job(self.random, human))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[2]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[2]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[2]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[2]))

            # Randomize job for fourth clan member
            self.randomized_jobs.append(get_random_job(self.random, bangaa))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[3]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[3]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[3]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[3]))

            # Randomize job for fifth clan member
            self.randomized_jobs.append(get_random_job(self.random, mou))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[4]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[4]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[4]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[4]))

            # Randomize job for sixth clan member
            self.randomized_jobs.append(get_random_job(self.random, viera))

            if self.options.starting_unit_equip == StartingUnitEquip.option_equip_basic:
                self.basic_weapon.append(get_basic_weapon(self.randomized_jobs[5]))
                self.basic_equip.append(get_basic_equip(self.randomized_jobs[5]))

            self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[5]))
            self.randomized_equip.append(get_valid_equip(self.randomized_jobs[5]))

        elif self.options.starting_units.value == StartingUnits.option_random_monster:
            randomize_starting(all_with_monster)

        if self.options.randomize_enemies.value == 1:
            for index in range(6, 0xA46):
                self.randomized_jobs.append(get_random_job(self.random, all_with_monster))
                self.randomized_weapons.append(get_valid_weapon(self.randomized_jobs[index]))
                self.randomized_equip.append(get_valid_equip(self.randomized_jobs[index]))

        # Always randomize the judge encounters for now
        for index in range(0, 5):
            self.randomized_judge.append(get_random_job(self.random, all))
            self.judge_weapon.append(get_valid_weapon(self.randomized_judge[index]))
            self.judge_equip.append(get_valid_equip(self.randomized_judge[index]))

        # print(self.random_data.all_abilities)
        # self.random.shuffle(self.random_data.all_abilities)

        self.location_ids = [0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x09, 0x0a, 0x0b, 0x0c,
                             0x0d, 0x0e, 0x0f, 0x10, 0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18,
                             0x19, 0x1a, 0x1b, 0x1c, 0x1d]

        # Randomize location nodes on map
        self.random.shuffle(self.location_ids)

        # Add Ambervale to the end
        self.location_ids.append(0x08)

        # Visualize regions
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "ffta.puml", show_entrance_names=True)

        # Get player names from the multiworld
        player_names = list(self.multiworld.player_name.values())
        player_names.remove(self.multiworld.player_name[self.player])

        self.human_abilities = human_abilities.copy()
        self.bangaa_abilities = bangaa_abilities.copy()
        self.nu_mou_abilities = nu_mou_abilities.copy()
        self.viera_abilities = viera_abilities.copy()
        self.moogle_abilities = moogle_abilities.copy()

        # Randomize abilities
        if self.options.randomize_abilities == AbilityRandom.option_race:
            self.random.shuffle(self.human_abilities)
            self.random.shuffle(self.bangaa_abilities)
            self.random.shuffle(self.nu_mou_abilities)
            self.random.shuffle(self.viera_abilities)
            self.random.shuffle(self.moogle_abilities)

        self.all_abilities = list(chain(self.human_abilities, self.bangaa_abilities, self.nu_mou_abilities,
                                        self.viera_abilities, self.moogle_abilities))

        length_abilities = len(self.all_abilities)

        if self.options.randomize_abilities == AbilityRandom.option_random_with_special:
            self.all_abilities += monster_abilities

            # Remove duplicate abilities
            self.all_abilities = set(map(tuple, self.all_abilities))
            self.all_abilities = list(map(list, self.all_abilities))
            self.random.shuffle(self.all_abilities)

            # Add random duplicate abilities to fill out ability list
            while len(self.all_abilities) < length_abilities:
                self.all_abilities.append(self.random.choice(self.all_abilities))

        elif self.options.randomize_abilities == AbilityRandom.option_randomized:
            self.random.shuffle(self.all_abilities)

        last_index = 0
        for i in range(0, len(human_abilities)):
            self.new_human_abilities.append(self.all_abilities[last_index])
            last_index += 1

        for i in range(0, len(bangaa_abilities)):
            self.new_bangaa_abilities.append(self.all_abilities[last_index])
            last_index += 1

        for i in range(0, len(nu_mou_abilities)):
            self.new_nu_mou_abilities.append(self.all_abilities[last_index])
            last_index += 1

        for i in range(0, len(viera_abilities)):
            self.new_viera_abilities.append(self.all_abilities[last_index])
            last_index += 1

        for i in range(0, len(moogle_abilities)):
            self.new_moogle_abilities.append(self.all_abilities[last_index])
            last_index += 1

        self.human_ability_dict = {human_abilities_bitflags[i]: self.new_human_abilities[i] for i in
                                   range(len(human_abilities_bitflags))}

        self.bangaa_ability_dict = {bangaa_abilities_bitflags[i]: self.new_bangaa_abilities[i] for i in
                                    range(len(bangaa_abilities_bitflags))}

        self.nu_mou_ability_dict = {nu_mou_abilities_bitflags[i]: self.new_nu_mou_abilities[i] for i in
                                    range(len(nu_mou_abilities_bitflags))}

        self.viera_ability_dict = {viera_abilities_bitflags[i]: self.new_viera_abilities[i] for i in
                                    range(len(viera_abilities_bitflags))}

        self.moogle_ability_dict = {moogle_abilities_bitflags[i]: self.new_moogle_abilities[i] for i in
                                   range(len(moogle_abilities_bitflags))}

        generate_output(self, self.player, output_directory, player_names)
