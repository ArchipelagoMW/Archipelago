# -*- coding: utf-8 -*-
import random
import os, sys
THIS_FILEPATH = os.path.abspath(os.path.dirname(__file__))
sys.path.append(THIS_FILEPATH)
import logging
from .data_manager import DataManager
from .collectible import Item, Magic, Crystal, Ability, KeyItem, CollectibleManager
from .reward import Reward, RewardManager
from .shop import ShopManager
from .shop_price import ShopPriceManager
from .area import AreaManager
from .enemy import EnemyManager
from .formation import Formation, FormationManager
from .text_parser import TextParser
from .monster_in_a_box import MonsterInABoxManager
# from item_randomization import *
from .misc_features import randomize_default_abilities, randomize_learning_abilities, free_shop_prices
from typing import Dict
import patcher

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")

import logging
logger = logging.getLogger("Final Fantasy V Career Day")


adjust_mult = 6
RANK_EXP_REWARD = {0:50*adjust_mult,
1:75*adjust_mult,
2:101*adjust_mult,
3:289*adjust_mult,
4:655*adjust_mult,
5:1265*adjust_mult,
6:2184*adjust_mult,
7:3480*adjust_mult,
8:5218*adjust_mult,
9:7466*adjust_mult,
10:10289*adjust_mult,
11:11894*adjust_mult,
12:12578*adjust_mult,
13:14021*adjust_mult,
14:15369*adjust_mult,
15:16981*adjust_mult,
16:18112*adjust_mult,
17:19207*adjust_mult}

def b2i(byte):
    return int(byte,base=16)
def i2b(integer):
    return hex(integer).replace("0x","").upper()

ITEM_TYPE = "40"

ITEM_SHOP_TYPE = "01"
MAGIC_SHOP_TYPE = "00"
CRYSTAL_SHOP_TYPE = "07"
VERSION = "FFV Career Day Archipelago v1.0"

class Conductor():
    def __init__(self, random_engine, arch_options, arch_data = {}, player = 1, seed = None, placed_crystals = [], \
                                        placed_abilities = [], placed_magic = []):
        
        self.RE = random_engine
        self.arch_data = arch_data
        self.arch_options = arch_options
        self.player = player
        self.filename_randomized = None
        self.seed = seed
        self.fjf = arch_options['four_job']
        self.fjf_strict = True
        self.fjf_num_jobs = 4
        self.jobpalettes = arch_options['job_palettes']
        self.world_lock = 1
        self.tiering_config = True
        self.tiering_percentage = 90
        self.tiering_threshold = 10
        self.enforce_all_jobs = True
        self.battle_speed = 3
        self.red_color = 0
        self.blue_color = 0
        self.green_color = 0
        self.exp_mult = 4
        self.progressive_bosses = False
        self.place_all_rewards = True
        self.progressive_rewards = False
        self.item_randomization = False
        self.item_randomization_percent = 100
        self.boss_exp_percent = 100
        self.hints_flag = True
        self.setting_string = None
        self.learning_abilities = False
        self.default_abilities = False
        self.job_1 = "Random"
        self.job_2 = "Random"
        self.job_3 = "Random"
        self.job_4 = "Random"
        character_names = arch_options["character_names"]
        self.lenna_name = character_names['Lenna']
        self.galuf_name = character_names['Galuf']
        self.cara_name = character_names['Krile']
        self.faris_name = character_names['Faris']
        self.music_randomization = False
        self.free_shops = False
        self.extra_patches = True
        self.kuzar_credits_warp = False
        self.remove_ned = False
        self.key_items_in_mib = False
        self.free_tablets = 0
        self.remove_flashes = arch_options['remove_flashes']
        self.randomize_loot_setting = False
        self.loot_percent = 0
        self.portal_boss = "Random"
        self.placed_abilities = placed_abilities
        self.placed_crystals = placed_crystals
        self.placed_magic = placed_magic
            
        # Some configs set up for the managers 
        collectible_config = {'place_all_rewards':self.translateBool(self.place_all_rewards),
                              'progressive_rewards':self.translateBool(self.progressive_rewards),
                              'item_randomization':self.translateBool(self.item_randomization)
                              }
            
        logger.debug("Config assigned: FJF: %s Palettes: %s World_lock: %s Tiering_config: %s Tiering_percentage: %s Tiering_threshold: %s" % (str(self.fjf),str(self.jobpalettes),str(self.world_lock),str(self.tiering_config),str(self.tiering_percentage),str(self.tiering_threshold)))

        # Set up randomizer config
        self.config = {"PATHS" : {"data_table_path" : "tables/",
                             "text_table_path" : "tables/text_tables/",
                             "text_table_to_use" : "text_table_chest.csv"},
                  "CONDUCTOR" : {'STARTING_CRYSTAL_ADDRESS' : 'E79F00',
                                 'DEFAULT_POWER_CHANGE' : 1.75,
                                 'STAT_MULTIPLIER' : .25,
                                 'NUM_KEY_ITEMS' : 21,
                                 'STARTING_CRYSTAL_COUNT' : 8,
                                 'MINIMUM_ALLOWABLE_CRYSTAL_COUNT' : 4,
                                 'ITEM_RELEVANCE_WEIGHT_MODIFIER' : 3,
                                 'CRYSTAL_RELEVANCE_WEIGHT_MODIFIER' : 10000,
                                 'ABILITY_RELEVANCE_WEIGHT_MODIFIER' : 10,
                                 'MAGIC_RELEVANCE_WEIGHT_MODIFIER' : 10,
                                 'SHINRYUU_VANILLA' : True,
                                 'SHINRYUU_ADDRESS' : 'D135FA',
                                 'ITEM_SHOP_CHANCE' : .7,
                                 'MAGIC_SHOP_CHANCE' : .2,
                                 'CRYSTAL_SHOP_CHANCE' : .1,
                                 'BOSS_RANK_ADJUST_LOW' : .8,
                                 'BOSS_RANK_ADJUST_MED' : 1.0,
                                 'BOSS_RANK_ADJUST_HIGH' : 1.2}, 
                  
                  
                  'REQUIREDITEMS' : {'item_ids' : ['E0', 'E1', 'E2', 'E3',
                                                   'E4', 'E5', 'E6', 'E8',
                                                   'E9', 'EC', 'ED', 'F0',
                                                   'F1']},
                  
                  'BANNEDATODIN' : {'boss_names' : ['Gogo', 'Stalker', 'Sandworm', 'Golem']}
                  }
        
        
        
        
        
        
        self.conductor_config = self.config['CONDUCTOR']
        logger.debug("Init data tables...")
        # Set up data tables
        self.DM = DataManager(self.config)                            #Data manager loads all the csv's into memory and sets them up for processing
        logger.debug("Init CollectibleManager...")
        self.CM = CollectibleManager(self.DM, collectible_config)              #Set up collectibles (Includes Items, magic, crystals, and abilities)
        logger.debug("Init Reward Manager...")
        self.RM = RewardManager(self.CM, self.DM)          #Set up rewards (Includes chests and events)
        logger.debug("Init Shop Manager...")
        self.SM = ShopManager(self.CM, self.DM)            #Set up shops
        logger.debug("Init ShopPrice Manager...")
        self.SPM = ShopPriceManager(self.CM, self.DM)      #Set up shop prices
        logger.debug("Init Area Manager...")
        self.AM = AreaManager(self.DM, self.RE)            #Set up areas (Tule, The Void, etc)
        logger.debug("Init Enemy Manager...")
        self.EM = EnemyManager(self.DM)                    #Set up enemies and bosses
        logger.debug("Init Formation Manager...")
        self.FM = FormationManager(self.DM, self.EM)       #Set up battle formations
        logger.debug("Init MonsterInABox Manager...")
        self.MIBM = MonsterInABoxManager(self.DM, self.RE, self.key_items_in_mib) #Set up monsters in boxes
        logger.debug("Init TextParser...")
        self.TP = TextParser(self.config)                             #Set up Text Parser Utility Object

        # if self.item_randomization:
        #     logger.debug("Init WeaponManager...")
        #     self.WM = WeaponManager(self.DM, self.RE, self.item_randomization_percent)      #Set up Weapon Manager
        #     # remove the following from the pool of weapons:
        #     for _ in range(3):
        #         self.CM.add_to_placement_history(self.CM.get_by_name("Brave Blade"),"No")
        #         self.CM.add_to_placement_history(self.CM.get_by_name("Chicken Knife"),"No")
        #         self.CM.add_to_placement_history(self.CM.get_by_name("Excailbur"),"No")
        #         self.CM.add_to_placement_history(self.CM.get_by_name("Soot"),"No")
        
        logger.debug("Init misc setup...")
        # Misc setup 
        self.difficulty = self.RE.randint(1,10)
        crystals = self.get_crystals()
        self.starting_crystal = crystals[0]
        self.chosen_crystals = crystals[1]
        self.chosen_crystals_names = [x.reward_name for x in self.chosen_crystals]
        self.exdeath_patch = ""
        self.odin_location_fix_patch = ""
        self.superbosses_spoiler = ""
        self.code_of_the_void = ""
        logger.debug("Init weigh collectibles...")
        self.weigh_collectibles()
        logger.debug("Init finished.")
        
    def get_crystals(self):

        arch_crystals_names = [i.split(" ")[0] for i in self.arch_options['starting_crystals']]
        
        if self.fjf:
            self.job_1, self.job_2, self.job_3, self.job_4 = arch_crystals_names
        else:
            self.job_1 = arch_crystals_names[0]
        crystals = self.CM.get_all_of_type(Crystal)
        
        if self.fjf and self.job_1 != 'Random':
            logger.debug("First job assigned %s" % self.job_1)
            starting_crystal = [i for i in crystals if i.collectible_name == self.job_1][0]
        elif self.fjf and self.job_1 == 'Random':
            logger.debug("First job random, ensuring others chosen are not in pool")
            temp_crystals = [i for i in crystals if i.collectible_name not in [self.job_2,self.job_3,self.job_4]]
            starting_crystal = self.RE.choice(temp_crystals)
        else:
            starting_crystal = [i for i in crystals if i.collectible_name == self.job_1][0]

            # while starting_crystal.collectible_name == 'Mimic' or starting_crystal.collectible_name == 'Samurai':
            #     logger.debug("Rerolling starting crystal...")
            #     starting_crystal = self.RE.choice(crystals)
        
        self.CM.add_to_placement_history(starting_crystal,"No") #don't allow the starting crystal to appear anywhere in game
        if starting_crystal.starting_spell_list == ['']:
            starting_crystal.starting_spell = "None"
            starting_crystal.starting_spell_id = "FF"
        else:
            index = self.RE.randint(0, len(starting_crystal.starting_spell_list)-1)
            starting_crystal.starting_spell = starting_crystal.starting_spell_list[index]
            starting_crystal.starting_spell_id = starting_crystal.starting_spell_ids[index]

            
        if self.fjf and any([self.job_2 != 'Random', self.job_3 != 'Random', self.job_4 != 'Random']):

            logger.debug("Assigning 4 jobs manually: next jobs assigned %s, %s, %s" % (self.job_2,self.job_3,self.job_4))
            # crystals = [x for x in crystals if x != starting_crystal and x.collectible_name != "Freelancer"]
            full_crystals = crystals[:]
            crystals = [x for x in crystals if x != starting_crystal]
            self.RE.shuffle(crystals)
            
            
            if self.job_2 != "Random":
                try:
                    job_2 = [i for i in full_crystals if i.collectible_name == self.job_2][0]
                except:
                    logger.debug("Failure on job_2, choosing random")
                    job_2 = crystals.pop()
                crystals = [i for i in crystals if i != job_2]
            else:
                job_2 = crystals.pop()
                logger.debug("Job_2 assigned %s" % (job_2.collectible_name))



            if self.job_3 != "Random":
                try:
                    job_3 = [i for i in full_crystals if i.collectible_name == self.job_3][0]
                except:
                    logger.debug("Failure on job_3, choosing random")
                    job_3 = crystals.pop()
                crystals = [i for i in crystals if i != job_3]
            else:
                job_3 = crystals.pop()
                logger.debug("Job_3 assigned %s" % (job_3.collectible_name))
                
                
            if self.job_4 != "Random":
                try:
                    job_4 = [i for i in full_crystals if i.collectible_name == self.job_4][0]
                except:
                    logger.debug("Failure on job_4, choosing random")
                    job_4 = crystals.pop()
            else:
                job_4 = crystals.pop()
                logger.debug("Job_4 assigned %s" % (job_4.collectible_name))

            
            chosen_crystals = [job_2,job_3,job_4]
        else:
            crystals = [x for x in crystals if x != starting_crystal]
            if not self.fjf:
                crystal_count = self.RE.randint(int(self.conductor_config['STARTING_CRYSTAL_COUNT']), len(crystals))
                crystal_count = crystal_count - (self.difficulty // 3)
    
    
                if crystal_count < int(self.conductor_config['MINIMUM_ALLOWABLE_CRYSTAL_COUNT']):
                    crystal_count = int(self.conductor_config['MINIMUM_ALLOWABLE_CRYSTAL_COUNT'])
                    
                
            else:
                crystal_count = 3
            chosen_crystals = self.RE.sample(crystals, crystal_count)
            job_2 = chosen_crystals[0]
            job_3 = chosen_crystals[1]
            job_4 = chosen_crystals[2]
        
        
        # if less than normal amount of jobs are chosen for this, then change 
        if self.fjf:
            if self.fjf_num_jobs == 1:
                chosen_crystals = [starting_crystal,starting_crystal,starting_crystal]            
            if self.fjf_num_jobs == 2:
                chosen_crystals = [starting_crystal,job_2,job_2]
            if self.fjf_num_jobs == 3:
                chosen_crystals = [job_2,job_2,job_3]

            
            # Ensures for fjf that Freelancer is not included
            # Rerolls until true
    #         if self.fjf:
    #             while len([i for i in chosen_crystals if i.collectible_name == 'Freelancer']) >= 1:
    #                 chosen_crystals = self.RE.sample(crystals, crystal_count)
    #                 logger.debug("Failed on pulling Freelancer, re-rolling crystals for FJ mode")
    # #                logger.debug("New: ",chosen_crystals[0].collectible_name,chosen_crystals[1].collectible_name,chosen_crystals[2].collectible_name)


        #this pretends to have placed every job, so it won't try to place any more going forward
        if self.fjf:
            for crystal in [x for x in self.CM.get_all_of_type(Crystal) if x != starting_crystal]:
                self.CM.add_to_placement_history(crystal,"No")
                
                
        # the below used to call for self.fjf_strict but now it's default
            # For Four Job mode, mark all Abilities as unobtainable 
            for ability in [x for x in self.CM.get_all_of_type(Ability)]:
                if self.arch_options['ability_settings'] == 'only_for_available_jobs': #if abilities are set for only for available jobs
                    self.CM.add_to_placement_history(ability,"Yes")
                else:
                    self.CM.add_to_placement_history(ability,"No")

                    
                
                
        else:
            # this does something similar for regular seeds, where all non-chosen crystals are added to placement history
            # only if the setting for enforce all jobs is off
            if not self.enforce_all_jobs:
                for crystal in [x for x in self.CM.get_all_of_type(Crystal) if x not in chosen_crystals]:
                    self.CM.add_to_placement_history(crystal,"No")

            

        return (starting_crystal, chosen_crystals)


    def weigh_collectibles(self):
        for index, value in enumerate(self.CM.collectibles):
            related = [i for i in value.related_jobs if i in self.chosen_crystals_names]
            if len(related) > 0:
                increase_amount = int(self.conductor_config['ITEM_RELEVANCE_WEIGHT_MODIFIER'])
                if type(value) == Crystal:
                    increase_amount = int(self.conductor_config['CRYSTAL_RELEVANCE_WEIGHT_MODIFIER']) #all but guarantee crystals appear
                if type(value) == Ability:
                    increase_amount = int(self.conductor_config['ABILITY_RELEVANCE_WEIGHT_MODIFIER'])  #much more likely to find these abilities
                if type(value) == Magic:
                    increase_amount = int(self.conductor_config['MAGIC_RELEVANCE_WEIGHT_MODIFIER'])  #much more likely to find these magics
                value.place_weight = value.place_weight + increase_amount


    def randomize_key_items(self):
        
        # This conditional code is defining which column in rewards.csv to refer to for item placement 
        if self.world_lock == 0:  # 0 = base case, no worlds locked, all items placed anywhere
            set_key_item_level = 'required_key_items'
        elif self.world_lock == 1: # Lock world 1 behind Adamantite (and world 2 behind Anti-Barrier & Bracelet) 
            set_key_item_level = 'required_key_items_lock1'
        elif self.world_lock == 2: # Lock world 2 behind Anti-Barrier & Bracelet
            set_key_item_level = 'required_key_items_lock2'
        else:
            logger.debug("Error on world_lock argument. Should be an int among 0, 1 and 2 only.")
        num_placed_key_items = 0
        exdeath_list = []

        
        
        # handle granting tablets immediately per config:
        if self.free_tablets > 0:
            tablets = [i for i in self.CM.get_all_of_type(KeyItem) if "Tablet" in i.collectible_name][:self.free_tablets]
            logger.debug("Handling %s number of free tablets" % len(tablets))
            for idx, tablet in enumerate(tablets):
                custom_reward = {'idx': 361 + idx, 'address': 'FFFFFF', 'original_reward': 'Null', 'area': 'Free Tablet %s' % (idx + 1), 'description': 'Free Tablet %s' % (idx + 1), 'reward_style': 'event', 'tier': '0', 'force_type': '', 'required_key_items': '', 'required_key_items_lock1': '', 'required_key_items_lock2': '', 'exdeath_address': '', 'hint_tags': '', 'world': ''}
                null_reward = Reward(361 + idx,self.CM,self.DM, custom_reward)
                self.CM.update_placement_rewards(tablet, null_reward)
                self.CM.add_to_placement_history(tablet,null_reward)
                
            
        
        
        
        for _ in range(0, int(self.conductor_config['NUM_KEY_ITEMS']) - self.free_tablets):
            global next_key_reward
            global curr_node
            global curr_key_item
            global forbidden_items
            global next_key_reward_locs
            
            
            if self.key_items_in_mib:
                key_item_list = [x for x in self.RM.get_rewards_by_style('key') if x.randomized == False] + [x for x in self.RM.get_rewards_by_style('mib_key') if x.randomized == False]
            else:
                key_item_list = [x for x in self.RM.get_rewards_by_style('key') if x.randomized == False]
            
            next_key_reward = self.RE.choice(key_item_list)
            
            

            next_key_reward_locs = next_key_reward.__dict__.get(set_key_item_level)
            if next_key_reward_locs != next_key_reward_locs: # stupid fix for python returning NaN instead of None
                next_key_reward_locs = None
            
            if next_key_reward_locs == None:

                next_key_item = self.CM.get_random_collectible(self.RE, monitor_counts=True,next_reward = next_key_reward,tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold, of_type=KeyItem)
                
                # logger.debug(next_key_item.collectible_name)


                
                # logger.debug("LOGGING %s " % next_key_item.collectible_name)
                next_key_reward.set_collectible(next_key_item)
                self.CM.update_placement_rewards(next_key_item, next_key_reward)
                next_key_reward.randomized = True
                num_placed_key_items = num_placed_key_items + 1
                    
                if next_key_reward.reward_style == 'mib_key':
                    # replace original MIB chest code with the B version (e.g., A3 -> B3)
                    # B3 will trigger the game to load the key item table instead of regular item
                    # and A3 or B3 causes monster in a box at all 
                    matching_mib = self.MIBM.get_mib_by_address(next_key_reward.address)
                    matching_mib.processed = True
                    og_mib_encounter_data = matching_mib.monster_chest_data
                    next_key_reward.collectible.reward_type = "B" + og_mib_encounter_data[1:]
                    
                    logger.debug("Updating chosen mib_key %s area volume" % next_key_reward.description)
                    self.AM.update_volume(next_key_reward)
            else:
                forbidden_items = []
                nodes_to_visit = []

                nodes_to_visit.extend(next_key_reward_locs) #this gives us a copy of the list so we don't overwrite anything

                #this will construct us a list of items we're not allowed to place here
                while len(nodes_to_visit) > 0:
                        curr_node = nodes_to_visit.pop()
                        curr_key_item = self.CM.get_by_name(curr_node)
                        forbidden_items.append(curr_key_item)
                        if len(curr_key_item.required_by_placement) != 0:
                            for i in curr_key_item.required_by_placement:
                                if i not in forbidden_items and i not in nodes_to_visit:
                                    nodes_to_visit.append(i)

                possible_key_items = [x for x in self.CM.get_all_of_type_respect_counts(KeyItem) if x not in forbidden_items]
                
                # logger.debug([i.collectible_name for i in possible_key_items])
                # logger.debug("\n")
                

                

                if len(possible_key_items) == 0:
                    #logger.debug("failed to place a key item here")
                    continue
                else:
                    next_key_item = self.RE.choice(possible_key_items)

                        
                    # logger.debug("ITEM: %s" % next_key_item.writeable_name)
                    # logger.debug("\n")
                   
                    next_key_reward.set_collectible(next_key_item)
                    self.CM.update_placement_rewards(next_key_item, next_key_reward)
                    if "Tablet" not in next_key_item.reward_name:
                        exdeath_list.append(next_key_reward)
                    next_key_item.required_by_placement.extend(next_key_reward_locs)
                    self.CM.add_to_placement_history(next_key_item,"No") #add this manually, usually get_random collectible handles it
                    next_key_reward.randomized = True
                    num_placed_key_items = num_placed_key_items + 1
                    
                    if next_key_reward.reward_style == 'mib_key':
                        # replace original MIB chest code with the B version (e.g., A3 -> B3)
                        # B3 will trigger the game to load the key item table instead of regular item
                        # and A3 or B3 causes monster in a box at all 
                        matching_mib = self.MIBM.get_mib_by_address(next_key_reward.address)
                        matching_mib.processed = True
                        og_mib_encounter_data = matching_mib.monster_chest_data
                        next_key_reward.collectible.reward_type = "B" + og_mib_encounter_data[1:]
                        
                        logger.debug("Updating chosen mib_key %s area volume" % next_key_reward.description)
                        self.AM.update_volume(next_key_reward)
                    


        
        if self.key_items_in_mib:
            key_item_list_remaining = [x for x in self.RM.get_rewards_by_style('key') if x.randomized == False] + [x for x in self.RM.get_rewards_by_style('mib_key') if x.randomized == False]
        else:
            key_item_list_remaining = [x for x in self.RM.get_rewards_by_style('key') if x.randomized == False]

        
        for key_item_reward in key_item_list_remaining:

            key_item_collectible = self.CM.get_random_collectible(self.RE,respect_weight=True, reward_loc_tier=key_item_reward.tier, of_type=key_item_reward.force_type,
                                    monitor_counts=True, gil_allowed=key_item_reward.reward_style == "chest",next_reward=key_item_reward, 
                                    tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)


            # key_item_collectible = self.CM.get_of_value_or_lower(self.RE, value=4)
            key_item_reward.set_collectible(key_item_collectible)
            key_item_reward.randomized = True
            self.CM.update_placement_rewards(key_item_collectible, key_item_reward)
            if key_item_reward.reward_style == 'mib_key':
                # this version does not replace A with B, since it is not reward a key item
                matching_mib = self.MIBM.get_mib_by_address(key_item_reward.address)
                matching_mib.processed = True
                og_mib_encounter_data = matching_mib.monster_chest_data
                key_item_reward.mib_type = og_mib_encounter_data
                
                logger.debug("Updating non-chosen mib_key %s area volume" % key_item_reward.description)
                self.AM.update_volume(key_item_reward)
        
        
        
        exdeath_rewards = {}
        for i in self.RE.sample(exdeath_list, 3):
            exdeath_rewards[i.collectible.reward_name] = i.exdeath_address

        self.exdeath_patch = self.TP.run_exdeath_rewards(exdeath_rewards)

        return num_placed_key_items

    def randomize_rewards_by_areas(self):
        #this is just manually doing the shinryuu chest first.
        #we set all the info as if it had been randomized normally
        #and it's skipped during the main process
        if self.conductor_config.getboolean('SHINRYUU_VANILLA'):
            shinryuu_address = self.conductor_config['SHINRYUU_ADDRESS']
            shinryuu_chest = self.RM.get_reward_by_address(shinryuu_address)

            mib = self.MIBM.get_mib_by_address(shinryuu_address)

            to_place = self.CM.get_random_collectible(self.RE, respect_weight=True,next_reward = shinryuu_chest,of_type=Item, monitor_counts=True,tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)
            shinryuu_chest.set_collectible(to_place)
            self.CM.update_placement_rewards(to_place, shinryuu_chest)
            shinryuu_chest.mib_type = mib.monster_chest_data
            shinryuu_chest.randomized = True
            mib.processed = True
            self.AM.update_volume(shinryuu_chest)

                
                
        while self.AM.any_areas_not_full():
            #logger.debug()
            #logger.debug("Area rewards: not full yet")
            # area = self.AM.get_emptiest_area()
            area = self.AM.get_random_area()

            if area is None:
                break
            #logger.debug("Area rewards: Area: " + area.area_name)
            possibles = [x for x in self.RM.rewards if x.area == area.area_name
                         and x.randomized == False and x.reward_style != 'key']
            #logger.debug("Area rewards: # of reward spot choices: " + str(len(possibles)))

            # try:
            next_reward = self.RE.choice(possibles)
            # except:

            #     pass
                
            
            if next_reward.randomized:
                logger.debug("%s was already randomzed...?" % (next_reward.description))

            #logger.debug("Area rewards: checking mib status now")
                
            mib = self.MIBM.get_mib_for_area(area)
            #logger.debug("Area rewards: next reward style: " + next_reward.reward_style)
            logger.debug(mib.area + mib.monster_chest_data)
            
                
            if mib is not None and next_reward.reward_style == "chest": #only mibs in chests
                if self.key_items_in_mib:
                    possible_placed_mib_keys = [x for x in self.RM.rewards if x.area == mib.area
                        and x.randomized == True
                        and x.reward_style == 'mib_key'
                        and x.address == mib.monster_chest_id]
                    if possible_placed_mib_keys:
                        
                        logger.debug("Skipping regular item placement %s, was already placed as MIB key" % mib.readable_name)

                    
                    
                #logger.debug("Area rewards: doing the mib stuff")
                chosen_tier = random.choice([5,6,7,8,9])


                to_place = self.CM.get_random_collectible(self.RE,reward_loc_tier=next_reward.tier,next_reward=next_reward, respect_weight=True, of_type=Item, monitor_counts=True, tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold, force_tier = chosen_tier) #only items in mibs
                
                logger.debug("Assigning MIB from chosen tier %s -> Tier %s : %s" % (chosen_tier, to_place.tier, to_place.reward_name))
                next_reward.mib_type = mib.monster_chest_data
                mib.processed = True
                
                #logger.debug(mib.processed)
                #logger.debug(next_reward.mib_type)
                #logger.debug("Area rewards: \n\n\n")
            else:
                #logger.debug("Area rewards: Location to place: " + next_reward.description)
                
                # Handle some percentages 
                
#                if next_reward.force_type == None:
#                    # If force_type is blank, we can start toying with percentages 
#                    random_int = self.RE.randint(1,100)
#                    if random_int > 1:
#                        next_reward.force_type = Ability
#                    else:
#                        next_reward.force_type = Item                      
                    
                
                to_place = self.CM.get_random_collectible(self.RE,respect_weight=True, reward_loc_tier=next_reward.tier, of_type=next_reward.force_type,
                                                          monitor_counts=True, gil_allowed=next_reward.reward_style == "chest",next_reward=next_reward, 
                                                          tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)
                
            try:
                if "Phoenix" in next_reward.area:
                    self.CM.remove_from_placement_history(to_place)
                    to_place = [x for x in self.CM.get_all_of_type(Item) if x.collectible_name == "Elixir"][0]
            except Exception as e:
                logger.debug(e)
                
            #logger.debug("Area rewards: Reward being placed: " + to_place.reward_name)
            next_reward.set_collectible(to_place)
            next_reward.randomized = True
            self.AM.update_volume(next_reward)
            self.CM.update_placement_rewards(to_place, next_reward)

        #logger.debug("going into cleanup")
        
        
        non_randomized_list = [i for i in self.RM.rewards if not i.randomized]
        # logger.debug("Cleanup non-randomized rewards %s" % ([i.description for i in non_randomized_list]))
        
        for next_reward in non_randomized_list:

            to_place = self.CM.get_random_collectible(self.RE,respect_weight=True, reward_loc_tier=next_reward.tier, of_type=next_reward.force_type,
                                                      monitor_counts=True, gil_allowed=next_reward.reward_style == "chest",next_reward=next_reward, 
                                                      tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)
            next_reward.set_collectible(to_place)
            next_reward.randomized = True
            self.AM.update_volume(next_reward)
            self.CM.update_placement_rewards(to_place, next_reward)
        
        for i in self.AM.areas:
            # logger.debug("Cleanup, checking area: " + i.area_name)
            if i.num_placed_checks < i.num_checks:
                logger.debug("Cleanup, area %s not finished, %s placed_checks out of %s checks " % (i.area_name,i.num_placed_checks, i.num_checks))
                for j in [x for x in self.RM.rewards if x.area == i.area_name and x.reward_style != 'key']:
                    #1 spot remaining is the same as greater than or equal to
                    #thus the - 1
                    if i.current_volume >= i.area_capacity - 1:
                        ##logger.debug("Area had minimum capacity remaining")
                        to_place = self.CM.get_min_value_collectible(self.RE)
                    else:
                        ##logger.debug("Area had some bonus capacity")
                        remaining = self.capacity - self.current_volume
                        to_place = self.CM.get_of_value_or_lower(random,
                                                                 remaining)
                    j.set_collectible(to_place)
                    j.randomized = True
                    self.AM.update_volume(j)
                    self.CM.update_placement_rewards(to_place, next_reward)
                    
                    
                    
        # final check for place_all_rewards
        
        if self.CM.collectible_config['place_all_rewards']:
            
            logger.debug("Placing all rewards final check")
            unplaced_collectibles = [i for i in self.CM.collectibles if i not in self.CM.placement_history.keys()]
            
            all_valid_collectibles = [i for i in self.CM.collectibles if i.valid and i.tier]
            all_valid_collectibles = [i for i in all_valid_collectibles if i not in unplaced_collectibles]
            
            
            
            for collectible_to_place in unplaced_collectibles:
                try:
                    collectible_choices_to_replace = [i for i in all_valid_collectibles if collectible_to_place.tier >= i.tier -1 and collectible_to_place.tier <= i.tier + 1 and self.CM.placement_history[i] > 1]
                    
                    if not collectible_choices_to_replace:
                        # try again, larger bottom tier
                        collectible_choices_to_replace = [i for i in all_valid_collectibles if collectible_to_place.tier >= i.tier - 3 and collectible_to_place.tier <= i.tier + 3 and self.CM.placement_history[i] > 1]
                        if not collectible_choices_to_replace:
                            pass
                    
                    collectible_to_replace = self.RE.choice(collectible_choices_to_replace)                    
                    valid_rewards = [i for i in self.RM.rewards if i.reward_style != 'mib_key' and i.reward_style != 'key' and i.collectible == collectible_to_replace]
                    


                    reward_choices_to_replace = [i for i in valid_rewards if int(collectible_to_replace.tier) >= int(i.tier)-1 and int(collectible_to_replace.tier) <= int(i.tier)+1]                    
                    # disallow placing gil on events
                    if collectible_to_place.name == "Gil":
                        reward_choices_to_replace = [i for i in valid_rewards if "C0" not in i.address]
                    
                    
                    if not reward_choices_to_replace:
                        # try again, larger bottom tier
                        reward_choices_to_replace = [i for i in valid_rewards if int(collectible_to_replace.tier) >= int(i.tier)-3 and int(collectible_to_replace.tier) <= int(i.tier)+3 and "C0" not in i.address]
                        if not reward_choices_to_replace:
                            pass
                    
                        
                    reward_to_replace = self.RE.choice(reward_choices_to_replace)
                    
                    logger.debug("Replacing %s (%s) : %s (%s) with %s (%s)" % (reward_to_replace.description, reward_to_replace.tier, collectible_to_replace.reward_name, collectible_to_replace.tier, collectible_to_place.reward_name, collectible_to_place.tier))
                    
                    # adjust placement history for chosen collectible by -1

                    self.CM.placement_history[collectible_to_replace] = self.CM.placement_history[collectible_to_replace] - 1
                    self.CM.add_to_placement_history(collectible_to_place, reward_to_replace)
                    self.CM.update_placement_rewards(collectible_to_place, reward_to_replace)
                    self.CM.remove_from_placement_rewards(collectible_to_replace, reward_to_replace)
                    reward_to_replace.set_collectible(collectible_to_place)
                    reward_to_replace.randomized = True
                except:
                    logger.debug("Failure on placing %s" % collectible_to_place.reward_name)
                
                
            
            

        
            

    def randomize_shops(self):
        required_items = {i:0 for i in self.config['REQUIREDITEMS']['item_ids']}

        if self.fjf_strict:
            item_chance = float(self.conductor_config['ITEM_SHOP_CHANCE'])
            magic_chance = float(self.conductor_config['MAGIC_SHOP_CHANCE'])
            crystal_chance = round(float(self.conductor_config['CRYSTAL_SHOP_CHANCE']) / 2)
            item_chance = item_chance + crystal_chance
            magic_chance = magic_chance + crystal_chance
            crystal_chance = 0
        else:
            item_chance = float(self.conductor_config['ITEM_SHOP_CHANCE'])
            magic_chance = float(self.conductor_config['MAGIC_SHOP_CHANCE'])
            crystal_chance = float(self.conductor_config['CRYSTAL_SHOP_CHANCE'])            

        #logger.debug("difficulty: " + str(self.difficulty))
        
        for index, value in enumerate(self.RE.sample(self.SM.shops,len(self.SM.shops))):
            
            # skip invalid shops
            if value.valid is False:
                continue

            #for the discount shops, put a single item in there
            if "discount" in value.readable_name:
                value.num_items = 1
                value.shop_type = ITEM_SHOP_TYPE
                value.contents = [self.CM.get_random_collectible(random, respect_weight=True, reward_loc_tier = value.tier, 
                                                                   monitor_counts=True, next_reward=next_reward,
                                                                   of_type=Item, tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)] + [None] * 7
                continue
            
            #manage the probability of the shops
            #each time a shop of one kind is placed
            #each of the other kinds of shops gets more likely
            if self.fjf_strict:
                if item_chance <= 0:
                    item_chance = item_chance + .05
                    magic_chance = magic_chance - .05
                elif magic_chance <= 0:
                    item_chance = item_chance - .05
                    magic_chance = magic_chance + .05
                kind = self.RE.choices(["item", "magic"],
                                      [item_chance, magic_chance])[0]
            else:    
                if item_chance <= 0:
                    item_chance = item_chance + .05
                    magic_chance = magic_chance - .025
                    crystal_chance = crystal_chance - .025
                elif magic_chance <= 0:
                    item_chance = item_chance - .025
                    magic_chance = magic_chance + .05
                    crystal_chance = crystal_chance - .025
                elif crystal_chance <= 0:
                    item_chance = item_chance - .025
                    magic_chance = magic_chance - .025
                    crystal_chance = crystal_chance + .05
            
                kind = self.RE.choices(["item", "magic", "crystal"],
                                      [item_chance, magic_chance, crystal_chance])[0]

            item_mod = self.RE.choices([  2,  1,  0, -1,  -2],
                                      [.05, .1, .7, .1, .05])[0]
            value.num_items = value.num_items + item_mod
            if value.num_items > 8:
                value.num_items = 8
            if value.num_items < 1:
                value.num_items = 1

            contents = []
            
            
            
            if len(self.placed_magic) == 0 and kind == "magic":
                kind = "item"
            if (len(self.placed_abilities) + len(self.placed_crystals)) == 0 and kind == "crystal":
                kind = "item"
            all_placed = False
            
            if kind == "item":
                if value.num_items < 4:
                    value.num_items = 4
                # if not self.fjf_strict:
                #     item_chance = item_chance - .1
                #     magic_chance = magic_chance + .05
                #     crystal_chance = crystal_chance + .05
                # else:
                #     item_chance = item_chance - .1
                #     magic_chance = magic_chance + .1                    
                value.shop_type = ITEM_SHOP_TYPE
                for i in range(0, value.num_items):
                    while True:
                        item_to_place = self.CM.get_random_collectible(random, respect_weight=True, reward_loc_tier = value.tier, 
                                                                       monitor_counts=True, next_reward = value,
                                                                       of_type=Item, tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)
                        if item_to_place not in contents:
                            break

                    if item_to_place.reward_id in required_items.keys():
                        required_items[item_to_place.reward_id] = required_items[item_to_place.reward_id] + 1
                    contents.append(item_to_place)
                    value.update_volume(item_to_place.tier)
                    self.CM.update_placement_rewards(item_to_place, value)
                    
                    
                    
                    
                    
            
            elif kind == "magic":
                if value.num_items > 5:
                    value.num_items = 5
                # if not self.fjf_strict:
                #     item_chance = item_chance + .05
                #     magic_chance = magic_chance - .1
                #     crystal_chance = crystal_chance + .05
                # else:
                #     item_chance = item_chance + .1
                #     magic_chance = magic_chance - .1                    
                value.shop_type = MAGIC_SHOP_TYPE
                try:
                    for i in range(0, value.num_items):
                        count = 0
                        temp_tier = value.tier
                        while True:
                            item_to_place = self.CM.get_random_collectible(random, respect_weight=True, reward_loc_tier = temp_tier, 
                                                                           monitor_counts=True,next_reward = value,
                                                                           of_type=Magic, disable_zerozero=True, tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)
                            
                            
                            AP_name = item_to_place.collectible_name + " " + item_to_place.type + " " + "Magic"
                            
                            if item_to_place not in contents and AP_name in self.placed_magic:
                                break
                            
                            #Some failsafes for settings that could create exceedingly low magic totals
                            if count % 100 == 0 and temp_tier > 1:
                                temp_tier -= 1
                            
                            if len(contents) >= len(self.placed_magic):
                                all_placed = True
                                break
                            
                            count += 1

                        if not all_placed:
                            contents.append(item_to_place)
                            value.update_volume(item_to_place.tier)
                            self.CM.update_placement_rewards(item_to_place, value)
                except Exception as e:
                    contents = []
                    value.shop_type = ITEM_SHOP_TYPE
                    for i in range(0, value.num_items):
                        while True:
                            item_to_place = self.CM.get_random_collectible(random, respect_weight=True, reward_loc_tier = value.tier, 
                                                                           monitor_counts=True,next_reward = value,
                                                                           of_type=Item, disable_zerozero=True, tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)
                            if item_to_place not in contents:
                                break

                        contents.append(item_to_place)
                        value.update_volume(item_to_place.tier)      
                        self.CM.update_placement_rewards(item_to_place, value)
            else:
                if value.num_items > 4:
                    value.num_items = 4
                # if not self.fjf_strict:
                #     item_chance = item_chance + .05
                #     magic_chance = magic_chance + .05
                #     crystal_chance = crystal_chance - .1
                # else:
                #     pass # this doesn't matter, shouldn't be placing this type on fjf_strict = True
                value.shop_type = CRYSTAL_SHOP_TYPE #shop type: crystal/ability
                try:
                    for i in range(0, value.num_items):
                        count = 0
                        temp_tier = value.tier
                        while True:
                            item_to_place = self.CM.get_random_collectible(random, respect_weight=True, reward_loc_tier = value.tier, 
                                                                           monitor_counts=True,next_reward = value,
                                                                           of_type=(Crystal, Ability), tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)

                            if item_to_place.type == 'Crystal':
                                AP_name = item_to_place.collectible_name + " " + "Crystal"
                            elif item_to_place.type == 'Ability':
                                AP_name = item_to_place.collectible_name + " " + "Ability"

                            if item_to_place not in contents and (AP_name in self.placed_abilities or AP_name in self.placed_crystals):
                                break
                            
                            #Some failsafes for settings that could create exceedingly low crystal or ability totals
                            if count % 100 == 0 and temp_tier > 1:
                                temp_tier -= 1
                            
                            if len(contents) >= (len(self.placed_abilities) + len(self.placed_crystals)):
                                all_placed = True
                                break
                            
                            count += 1
                        if not all_placed:
                            contents.append(item_to_place)
                            value.update_volume(item_to_place.tier)
                            self.CM.update_placement_rewards(item_to_place, value)
                except Exception as e:
                    contents = []
                    value.shop_type = ITEM_SHOP_TYPE
                    for i in range(0, value.num_items):
                        while True:
                            item_to_place = self.CM.get_random_collectible(random, respect_weight=True, reward_loc_tier = value.tier, 
                                                                           monitor_counts=True,next_reward = value,
                                                                           of_type=Item, disable_zerozero=True, tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)
                            if item_to_place not in contents:
                                break

                        contents.append(item_to_place)
                        value.update_volume(item_to_place.tier)
                        self.CM.update_placement_rewards(item_to_place, value)


            
            # final check that contents are all the same type
            # exception for abilities and crystals handled first
            
            contents_types = list(set([type(i) for i in contents]))
            if Ability in contents_types and Crystal in contents_types and len(contents_types) == 2:
                pass                
            else:
                first_slot_type = type(contents[0])
                for content in contents:
                    if type(content) != first_slot_type:
                        contents.remove(content)
                        logger.debug("NOTICE: Removing shop entry for mismatch on collectible type")

            while(len(contents) < 8):
                contents.append(None)
# 
            value.contents = contents
            

            
        '''
        for shop in [x for x in self.SM.shops if x.valid]:
            if shop.num_items == 0:
                logger.debug(shop.readable_name)
                logger.debug(shop.shop_type)
                logger.debug(shop.valid)
        '''

        #manage the must place items here
        for index, value in required_items.items():
            chosen_shop = None
            chosen_slot = None
            while value < 3:
                #logger.debug("guaranteeing " + index)
                item_to_place = self.CM.get_by_id_and_type(index, ITEM_TYPE)
                #logger.debug(item_to_place.reward_name)
                # First attempt to place in tier 1 shop locations (world 1)
                item_shops = [x for x in self.SM.shops if x.shop_type == ITEM_SHOP_TYPE and x.valid and x.num_items > 0 and x.num_items < 8 and (x.tier == '1' or x.tier == 1)]
                if item_shops == []:
                    # if not, use normal method 
                    item_shops = [x for x in self.SM.shops if x.shop_type == ITEM_SHOP_TYPE and x.valid and x.num_items > 0 and x.num_items < 8]
                #logger.debug("number of item shops: " + str(len(item_shops)))
                try:
                    chosen_shop = item_shops[self.RE.choice(range(0, len(item_shops)))]
                    chosen_shop.contents[slot] = item_to_place
                    chosen_shop.num_items = chosen_shop.num_items + 1
                except:
                    try:
                        #logger.debug("Error on placing %s in shop, skipping..." % (item_to_place.description_name))
                        pass
                    except:
                        #logger.debug("Error on placing %s in shop, skipping..." % (item_to_place))
                        pass
                slot = chosen_shop.num_items #because of 0 indexing, we want this, not this + 1
                #logger.debug("chosen slot index: " + str(chosen_slot))

                value = value + 1
        
        #  dedupe shops
        global shops
        shops = self.SM.shops
        

        
        for index, shop in enumerate(self.SM.shops):
            shop.sort_contents()
            contents = shop.contents
            name_list = []
            for i in contents:
                if i is not None:
                    name_list.append(i)
            if len(set(name_list)) < len(name_list):
                # if this condition, we've got duplicates
                new_contents = []
                for i in contents:
                    if i not in new_contents:
                        new_contents.append(i)
                while(len(new_contents) < 8):
                    new_contents.append(None)
                shop.contents = new_contents
                
            # Finally check each entry for None, if they appear, pop, then re-add
            
            new_contents = [i for i in shop.contents if i is not None]
            while(len(new_contents) < 8):
                new_contents.append(None)
            shop.contents = new_contents 
    def decide_progressive_bosses(self):
        logger.debug("Progressive bosses flag enabled. Deciding progressive bosses")
        # galura
        for x in self.RM.get_rewards_by_style("key"):
            if int(x.world) == 3: # if world 3, discard
                pass
            else:
                try:
                    # galura's required key items
                    req = x.required_key_items_lock2
                    # where galura's required key items are (where the walse tower key is)
                    keys = [self.CM.get_by_name(x) for x in req]
                    req_loc = []
                    
                    
                    for reward in self.RM.get_rewards_by_style("key"):
                        if reward.collectible in keys:
                            req_loc.append(reward)
                            # go 1 level down past this
                            keys2 = [self.CM.get_by_name(x) for x in reward.required_key_items_lock2]
                            for reward2 in self.RM.get_rewards_by_style("key"):
                                if reward2.collectible in keys2:
                                    req_loc.append(reward2)
                # odin location has walse tower key
                # now, max world will be an attribute of the original reward object
                
                    max_requirements_world = max([x.world for x in req_loc])
                    world_delta = (int(max_requirements_world) - int(x.world))
                    if world_delta > 0:
                        x.max_world_requirements_flag = True
                        x.world_delta = world_delta
                        logger.debug("Progressive boss adjustment for location reward %s, delta %s" % (x.description,world_delta))
                except Exception as e:
                    pass
#                    logger.debug("Error %s" % e)
            

    def randomize_bosses(self):
        # First, if the setting for progressive bosses is enabled,process
        if self.progressive_bosses: #progressive bosses
            self.decide_progressive_bosses()          

        list_of_randomized_enemies = []

        # This has to be done twice in order for the enemy classes to NOT be shared objects
        # Very important or else swapping HP becomes very muddy and original hp values on enemies are not preserved
                                    
        original_boss_list = []
        if self.remove_ned:
            formation_list = [x for x in self.FM.formations if x.randomized_boss == 'y' or x.randomized_boss == 'ned']
        else:
            formation_list = [x for x in self.FM.formations if x.randomized_boss == 'y']
        for formation in formation_list:
        #for formation in df_boss_formations['event_id'].unique():
            original_boss_list.append(Formation(formation.idx, self.DM, self.EM, original_flag=True))

        # Very explicit definitions
        # Randomized boss list will be updated
        # Original boss list will be referenced for what boss location & stats to change to, 
                # and the list will be reduced tox 0 as random formations are assigned
                
       
        # Shuffle original boss list
        self.RE.shuffle(original_boss_list)
        
        # Process: Draw randomly from original formation list (using pop method) and update randomized boss formations
        # Take original list's event_formation_reference and write to randomized event_lookup_loc1 and event_lookup_loc2
        #         (This will assign the randomized formation to the original's location, so Karlabos at Sol Cannon)
        
        
        
        # Create patch file for custom AI and clear out any previous 
        banned_at_odin = self.config['BANNEDATODIN']['boss_names']
    


        DEBUG_FLAG = False
        LOOP_FLAG = False
        ENEMY_LIST_STRING_BEING_RANDOMIZED = 'Omniscient'
        ENEMY_LIST_STRING_TO_REPLACE = 'Halicarnaso'
        

        
        if DEBUG_FLAG:
            # move debug to top of formation_list
            new_list = [i for i in formation_list if ENEMY_LIST_STRING_BEING_RANDOMIZED not in i.enemy_list]
            
            formation_list = [i for i in formation_list if ENEMY_LIST_STRING_BEING_RANDOMIZED in i.enemy_list]
            formation_list = formation_list  + new_list
            
            
            # override use this for specific encounters like in gilgamesh's case
            if True:
                formation_list = [i for i in formation_list if i.idx == '406'] + [i for i in formation_list if i.idx != '406']
            

        for random_boss in formation_list:
            
            # First pick a random original boss
                        
            if DEBUG_FLAG:
                if ENEMY_LIST_STRING_BEING_RANDOMIZED in random_boss.enemy_list and not LOOP_FLAG:
                    
                    original_boss = [i for i in original_boss_list if ENEMY_LIST_STRING_TO_REPLACE in i.enemy_list][0]
                    original_boss_list = [i for i in original_boss_list if ENEMY_LIST_STRING_TO_REPLACE not in i.enemy_list]
                    
                    
                    LOOP_FLAG = True

                else:              
                    original_boss = original_boss_list.pop()

            else:              
                original_boss = original_boss_list.pop()

            
            #this is specifically an unworkable situation
            #this will just cycle gogo/stalker to the end and get a new boss
            while (original_boss.enemy_1_name == "Odin" and random_boss.enemy_1_name in banned_at_odin):
                original_boss_list = [original_boss] + original_boss_list
                original_boss = original_boss_list.pop()


            # disallow Sandworm in Fork Tower
            
            # logger.debug("Original boss: %s"  % original_boss.enemy_list)
            while (("Sandworm" in random_boss.enemy_list or "Atmos" in random_boss.enemy_list) and original_boss.enemy_1_name in ['Omniscient', 'Minotauros']):
                original_boss_list = [original_boss] + original_boss_list
                original_boss = original_boss_list.pop()
                
            if "Sandworm" in random_boss.enemy_list:
                pass
                # logger.debug("Placed Sandworm at %s" % original_boss.enemy_list)
            if "Atmos" in random_boss.enemy_list:
                pass
                # logger.debug("Placed Atmos at %s" % original_boss.enemy_list)


            if original_boss.enemy_1_name == "Odin":               
                # all we need to do is take the current final flag of random boss
                # which corresponds to in battle flags associated with that formation
                # and turn off bit 01 which corresponds to the white flash 

                x = random_boss.formationid_16
                x = int(str(x),base=16)
                x = bin(x).replace("0b","")
                x = x.zfill(8)
                x = x[0:7]
                x = hex(int(x + '0',2))
                x = x.replace("0x","").zfill(2)
                self.odin_location_fix_patch = '\n; Odin location animation fix (resolve softlocks)\norg $'+random_boss.offset[:-1]+"F\ndb $"+x+"\n"

            # Assign random boss location to the original spots (overwriting it)
            # This is grabbing event_lookuploc1 / loc2 from the original
            # And overwriting the new random boss' 
            # For example, we're updating Byblos to be at Adamantium 
            # We grab Adamantium's two event_lookup (so, when you're in Adamantium's area, 
            # whatever is being referred to in that event to call the battle)
            # And update Byblos' event_lookups to reflect this
            # Then for asar output, we take the code for running Byblos battle and write to it where Adamantium's was 
            # So then when you walk into Adamantium area, you'll fight Byblos

            new_lookup1 = original_boss.event_lookup_loc1
            new_lookup2 = original_boss.event_lookup_loc2
            
            random_boss.event_lookup_loc1 = new_lookup1
            random_boss.event_lookup_loc2 = new_lookup2
            
            
            # Find original locations' ID and assign to a new variable
            original_formation_id = original_boss.event_id
            random_boss.new_event_id = original_formation_id 

            # Document original rank
            prev_rank = random_boss.boss_rank
            # Find new rank & assign
            
            new_rank = original_boss.boss_rank
            
            progressive_flag = False            
            if self.progressive_bosses:
                # if enabled, change the new_rank 
                
                # first get the related reward
                try:
                    related_reward = [x for x in self.RM.rewards if int(x.idx) == int(original_boss.related_boss_reward)][0]
                    if related_reward.max_world_requirements_flag == True:
#                        logger.debug(related_reward.description,related_reward.max_world_requirements_flag)
                        new_rank_og = new_rank
                        new_rank = min(int(new_rank) + (int(related_reward.world_delta * 10)),40)
                        progressive_flag = True
#                        logging.info("Original boss %s Random boss %s new_rank_og %s new_rank %s" % (original_boss.enemy_list,random_boss.enemy_list,new_rank_og,new_rank))
                except Exception as e:
#                    logger.debug("Error %s " % e)
                    pass
                
                
                
#            random_boss.boss_rank = new_rank
            try:
                rank_delta = round((int(new_rank) - int(prev_rank))/3)
            except:
                pass
            random_boss.rank_delta = rank_delta

            # Document random_boss' previous HP
            prev_hp = random_boss.enemy_classes[0].num_hp
        
            # Find original boss's first enemy HP
            new_hp = int(original_boss.enemy_classes[0].num_hp)
            if progressive_flag:
                if int(related_reward.world_delta) == 2 or (int(related_reward.world_delta)==1 and int(related_reward.world)==2):
                    new_hp = 30000
                elif int(related_reward.world_delta) == 1:        
                    new_hp = 15000
        
            # Update random boss hp on FIRST enemy only right now
            random_boss.enemy_classes[0].num_hp = new_hp
            random_boss.enemy_classes[0].update_val('hp', new_hp)
            
        

            # Then after the first HP is assigned and the new boss formation takes place in the right locations,
            # Enforce some standardization for specific boss fights. This is hardcoded for good reason as many fights
            #     specifically need individual treatment
            # For example, 2x Gargoyle should share the same HP
            # But HiryuuFlower & HiryuuPlant should NOT share HP and should be drastically different
            
            # Byblos (rank 3) to Twin Tania (rank 10) have somewhat similar move sets (physical attacks, area all damage)
                # The rough multplier here is about 3x the stats for phys power/def and magic power/def
                
            # Same general ratio with Galura (rank 2) to Minotauros (rank 8), ratio is about 4x for phys power
                
            # For this basic reasoning, initial rank movement will yield a bonus of 25% increase/decrease per rank movement, which
                # is initially conservative. Stronger enemies will be strong, and weaker enemies will be weaker
                # but for boss shuffle, this might be okay/good
            # This only applies to phys power/def and magic power/def
                # DOES NOT apply to speed, phys multiplier, or phys/magic evade
                
                
            # The process will be:
            
            # 1) Take the original formation and assess its qualities, and update the first enemy of the newly randomized formation
            # For example, if Karlabos replaces Guardians, Guardians have 7k HP each but there's four of them
            # So Karlabos conceptually should have a boost to HP, and not get 'penalized' for 1/4th HP because there's only 1 of him
            
            # 2) Assign HP/power to all remaning enemies and re-adjust main enemy's HP if necessary, based on the RANDOM FORMATION'S QUALITIES
            # For example, if Gargoyles replaces Guardians, the first Gargoyle would get 4x HP. 
            # Then, BASED ON THE RANDOMIZED FORMATIONS' QUALITIES (Gargoyles only here), split hp among the two enemies
            # Something like HiryuuFlower will have a completely different method
            
            

        
            # STEP 1)
            # Use the event_id to identify what type of encounter it is, with specifics per encounter
            
            # CLAUSE FOR ENEMIES WITH 2x BOSS AS SEPARATE ENEMIES
            # GARGOYLES, GILGA/ENKIDOU, 
            if original_formation_id in ['2D','1F','00']:
                new_hp = new_hp * 2
                
            # CLAUSE FOR ENEMIES WITH 3x BOSS AS SEPARATE ENEMIES
            # TRITON/PHOBOS/NEREGEID
            if original_formation_id in ['32']:
                new_hp = new_hp * 3
                
            # CLAUSE FOR ENEMIES WITH 4x BOSS AS SEPARATE ENEMIES
            # GUARDIANS
            if original_formation_id in ['21']:
                new_hp = new_hp * 4
                
            # CLAUSE FOR ENEMIES WITH 5x BOSS AS SEPARATE ENEMIES
            # ARCHEOAVIS
            if original_formation_id in ['0F']:
                new_hp = new_hp * 5
                
            # CLAUSE FOR ENEMIES WITH 6x BOSS AS SEPARATE ENEMIES
            # PUROBUROS
            if original_formation_id in ['12']:
                new_hp = new_hp * 2
                
            # CLAUSE FOR SOL CANNON
            if original_formation_id in ['0E']:
                new_hp = 12500
                
            # CLAUSE FOR NECROPHOBIA:
            if original_formation_id in ['4B']:
                # This takes Necrofobia's HP and applies a 1.5x bonus. Barriers have 8k, Necrofobia has 40k. Results in 60k, normalized in STEP 2 later
                 new_hp = new_hp * 2
                 
            
            # No clause for:
                # Sandworm - it technically grabs the Hole's HP, but its 3k 
                # Sergeant - grabs Sergeant's HP, which is shared with IronClaw
                # Shiva - Shiva's HP is enough
                # All enemies with shared hp (e.g., LiquiFlame, WingRaptor, Carbunkle) - Grab the first HP only
            
            if new_hp > 65535:
                new_hp = 65535
            
            # STEP 2)
            # Based on the NEWLY RANDOMIZED FORMATION QUALITY, update all formation enemies 
            
            # CLAUSE FOR FORMATIONS WITH SHARED HP, ONLY ONE ENEMY ACTIVE ON THE FIELD
            # WINGRAPTOR, SIREN, LIQUIFLAME, MELUSINE, CARBUNKLE, GILGAMESH, TWINTANIA, STALKER, SANDWORM
            if random_boss.event_id in ['01','03','07','2B','22','23','4A','2E','0A']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_hp = new_hp
            
            # CLAUSE FOR FORMATIONS WITH 2x SAME/SIMILAR BOSS:
            # GARGOYLES, GILGA/ENKIDOU, FORZA/MAGISA
            elif random_boss.event_id in ['2D','1F','04']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_hp = round(new_hp / 2)
                    
                    
            # CLAUSE FOR FORMATIONS WITH 3x SAME/SIMILAR BOSS:
            # TRITON/PHOBOS/NEREGEID
            elif random_boss.event_id in ['32']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_hp = round(new_hp / 3)
                    
                   
            # CLAUSE FOR FORMATIONS WITH 6x SAME/SIMILAR BOSS:
            # PUROBUROS
            elif random_boss.event_id in ['12']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_hp = round(new_hp / 6)
                    
            # CLAUSE FOR FORMATIONS WITH 4x SAME/SIMILAR BOSS:
            # GUARDIANS
            elif random_boss.event_id in ['21']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_hp = round(new_hp / 4)
        
            # CLAUSE FOR FORMATIONS WITH 5x SAME/SIMILAR BOSS:
            # ARCHEOAVIS
            elif random_boss.event_id in ['0F']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_hp = round(new_hp / 5)
                    
            # CLAUSE FOR SERGEANT/KARNAKS
            elif random_boss.event_id in ['08']:
                random_boss.enemy_classes[0].num_hp = new_hp
                # Apply HP to IronClaw
                random_boss.enemy_classes[4].num_hp = new_hp
                # Apply 30% to Karnaks
                random_boss.enemy_classes[1].num_hp = round(new_hp * .3)
                random_boss.enemy_classes[2].num_hp = round(new_hp * .3)            
                random_boss.enemy_classes[3].num_hp = round(new_hp * .3)
                
            # CLAUSE FOR SHIVA/COMMANDER
            elif random_boss.event_id in ['05']:
                # Apply 40% to Commanders
                random_boss.enemy_classes[0].num_hp = new_hp
                random_boss.enemy_classes[1].num_hp = round(new_hp * .4)
                random_boss.enemy_classes[2].num_hp = round(new_hp * .4)            
                random_boss.enemy_classes[3].num_hp = round(new_hp * .4)
                
            # CLAUSE FOR SOLCANNON
            elif random_boss.event_id in ['0E']:
                # Add 10k HP to pool, apply 50% to Launchers
                new_hp = min(new_hp + 10000,65535)
                random_boss.enemy_classes[0].num_hp = new_hp
                random_boss.enemy_classes[1].num_hp = round(new_hp * .1)
                random_boss.enemy_classes[2].num_hp = round(new_hp * .1)
                
                
            # CLAUSE FOR GOLEM
            elif random_boss.event_id in ['3E']:
                # Apply 50% to other enemies
                random_boss.enemy_classes[0].num_hp = new_hp
                random_boss.enemy_classes[1].num_hp = round(new_hp * .5)
                random_boss.enemy_classes[2].num_hp = round(new_hp * .5)
                
            # CLAUSE FOR HIRYUUPLANT
            elif random_boss.event_id in ['1E']:
                # Apply 5% to Flowers
                random_boss.enemy_classes[0].num_hp = new_hp
                random_boss.enemy_classes[1].num_hp = round(new_hp * .05)
                random_boss.enemy_classes[2].num_hp = round(new_hp * .05)
                random_boss.enemy_classes[3].num_hp = round(new_hp * .05)
                random_boss.enemy_classes[4].num_hp = round(new_hp * .05)
                random_boss.enemy_classes[5].num_hp = round(new_hp * .05)
                
            # CLAUSE FOR NECROPHOBIA:
            elif random_boss.event_id in ['4B']:
                # Apply 20% to Barriers
                random_boss.enemy_classes[0].num_hp = new_hp
                random_boss.enemy_classes[1].num_hp = round(new_hp * .2)
                random_boss.enemy_classes[2].num_hp = round(new_hp * .2)
                random_boss.enemy_classes[3].num_hp = round(new_hp * .2)
                random_boss.enemy_classes[4].num_hp = round(new_hp * .2)
            
            else:
                random_boss.enemy_classes[0].num_hp = new_hp



            # new exp system
            try:
                new_exp = new_hp * float(self.boss_exp_percent / 100)
            except:
                logger.debug("Error on parsing boss_exp_percent %s, setting to 100 percent" % self.boss_exp_percent)
                new_exp = new_hp
            
            
            # old exp system
            # # Get base exp
            # base_exp = RANK_EXP_REWARD[round(int(new_rank)/3)]
            
            # # Adjust base exp based on multiplier
            # # This is INVERTED multiplier
            # # If you fight a hard boss at an easy location, the multiplier will be less than 1 
            # # To reduce its stats
            # # However, you want to still reward the player MORE because it is still a hard boss
            # # So invert the multiplier
    
            # # First use 25% multiplier over 100% of the original (the +1 at the end)
            # rank_mult = (abs(rank_delta) * float(self.conductor_config['STAT_MULTIPLIER'])) + 1 
            
            # new_exp = base_exp * 1/rank_mult
            # # Round for nice number, merely for presentation
            # new_exp = int(round(new_exp,-2))
            
            # # First clear out exp on all enemies:
            
            for enemy in random_boss.enemy_classes:
                enemy.num_exp = 0
                
                
            # Provide cap for exp
        
            if new_exp > 65535:
                new_exp = 65535
                
            # Apply exp to the FIRST enemy only. The rest of the enemies are default 0
            # Need to apply same logic as before for specific case handling - enemies with multiple
            # forms need to be shared on exp
            # And formations with multiple enemies of the SAME exact kind need to 
            # Split exp
            
            # CLAUSE FOR FORMATIONS WITH SHARED HP, ONLY ONE ENEMY ACTIVE ON THE FIELD
            # WINGRAPTOR, SIREN, LIQUIFLAME, ARCHEOAVIS, MELUSINE, CARBUNKLE, GILGAMESH, TWINTANIA
            if random_boss.event_id in ['01','03','07','0F','2B','22','23','4A']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_exp = new_exp
            # CLAUSE FOR FORMATIONS WITH 2x SAME/SIMILAR BOSS:
            # GARGOYLES, GILGA/ENKIDOU, FORZA/MAGISA
            elif random_boss.event_id in ['2D','1F','04']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_exp = round(new_exp / 2)
                    
            # CLAUSE FOR FORMATIONS WITH 3x SAME/SIMILAR BOSS:
            # TRITON/PHOBOS/NEREGEID
            elif random_boss.event_id in ['32']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_exp = round(new_exp/ 3)
                    
                   
            # CLAUSE FOR FORMATIONS WITH 6x SAME/SIMILAR BOSS:
            # PUROBUROS
            elif random_boss.event_id in ['12']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_exp = round(new_exp / 6)
                    
            # CLAUSE FOR FORMATIONS WITH 4x SAME/SIMILAR BOSS:
            # GUARDIANS, STALKER
            elif random_boss.event_id in ['21', '2E']:
                for enemy in random_boss.enemy_classes:
                    enemy.num_exp = round(new_exp / 4)
                    
            # CLAUSE FOR SANDWORM:
            elif random_boss.event_id in ['0A']:
                new_exp = int(round(new_exp / 3))
                for enemy in [random_boss.enemy_classes[3],random_boss.enemy_classes[4],random_boss.enemy_classes[5]]:
                    enemy.num_exp = new_exp
            # CLAUSE FOR SOL CANNON:
            elif random_boss.event_id in ['0E']:
                random_boss.enemy_classes[0].num_exp = max(1,new_exp - 10000)
                    
            else:    
                random_boss.enemy_classes[0].num_exp = new_exp
        
        
            # STATS / AI
            # Stats - Update stats based on boss_scaling.csv for every enemy
            # AI - create new patch file for AI changes 

            
            def inttohex_asar(x):
                y = hex(int(x)).replace("0x","").zfill(4)
                return "db $"+y[2:4] + ", $" + y[0:2]
                
            def write_hpai(trigger_dict):
                '''
                This function takes a dictionary of:
                    1) trigger_hp (part of AI when an enemy changes pattern)
                    and its corresponding
                    2) address to write to 
                This will iterate through both trigger_hp/address for however many pairs exist per enemy
                '''
                text_str = ''
                for address, trigger_hp in trigger_dict.items():
                    text_str = text_str + "; Original HP: "+str(random_boss.enemy_classes[0].num_hp)+"\n"
                    text_str = text_str + "; New trigger HP: "+str(trigger_hp)+"\n" 
                    text_str = text_str + 'org $'+address+'\n'
                    
                    hp_hex = inttohex_asar(trigger_hp)
                    if "fe" in hp_hex.lower():
                        hp_hex = hp_hex.replace("fe", "ef")
                    
                    text_str = text_str + hp_hex +"\n"
                
                return text_str

            og_text = "; --------------------------\n; Original boss {} rank {} -> Randomized boss {} rank {}\n; HP: {} -> {}\n".format(random_boss.enemy_list, str(prev_rank),original_boss.enemy_list,str(new_rank),str(prev_hp),str(new_hp))
            text_str = og_text
            write_flag = False
            for enemy in random_boss.enemy_classes:
                list_of_randomized_enemies.append(enemy) #maintain a list of only the enemies we've actually randomized
                text_str = text_str + '; ENEMY: '+enemy.enemy_name+'\n'
                
                
                data_idx = [i for i in self.DM.files['boss_scaling'] if self.DM.files['boss_scaling'][i]['idx'] == int(enemy.idx) and self.DM.files['boss_scaling'][i]['boss_rank'] == int(new_rank)][0]
                data_temp = self.DM.files['boss_scaling'][data_idx]
                
                # STATS
                for col in ['num_gauge_time','num_phys_power','num_phys_mult','num_evade','num_phys_def','num_mag_power','num_mag_def','num_mag_evade','num_mp']:
                    setattr(enemy,col,data_temp[col])
                # both updates stats from this for loop and applies mult based on tier
                
                
                # AI - check for & write moveset
                offset_loc = data_temp['ai_starting_address']
                list_of_skills = data_temp['ai_skills'].strip("][").split(',')
                list_of_writes = data_temp['ai_write_loc'].strip("][").split(',')
                
                    # Check skill list if adjustments needed
                if not offset_loc != offset_loc and list_of_skills != ['']: #ignore if NaN
                    write_flag = True
                    list_of_addresses = []
                    for i in list_of_writes:
                        list_of_addresses.append(hex(int(offset_loc,base=16)+int(i)).replace("0x",""))

                    skill_dict = dict(zip(list_of_addresses,list_of_skills))
                    
                    text_str = text_str + '; Skills: '+str(list_of_skills)+'\n'
                    
                    for address, skill in skill_dict.items():
                        text_str = text_str + '; New skill: '+skill+"\n"
                        text_str = text_str + 'org $'+address+"\n"
                        skill_idx = [i for i in self.DM.files['enemy_skills'] if self.DM.files['enemy_skills'][i]['name']==skill][0]
                        text_str = text_str + 'db $' + skill_idx +"\n"
                    
                    
                # AI - check for & write HP triggers
                list_of_hp_writes = data_temp['ai_hp_write_loc'].strip("][").split(',')
                list_of_hp_mult = data_temp['ai_hp_mult'].strip("][").split(',')
                
                if not offset_loc != offset_loc and list_of_hp_writes != ['']: #ignore if NaN
                    list_of_hp_addresses = []
                    for i in list_of_hp_writes:
                        list_of_hp_addresses.append(hex(int(offset_loc,base=16)+int(i)).replace("0x",""))

                    list_of_hp_vals = []
                    for mult in list_of_hp_mult:
                        list_of_hp_vals.append(round(int(enemy.num_hp) * float(mult)))
                        

                    trigger_dict = dict(zip(list_of_hp_addresses,list_of_hp_vals))

                    text_str = text_str + write_hpai(trigger_dict)
#                enemy.rank_mult = stat_rank_mult
                enemy.update_all() 
                enemy.ai_patch_text = text_str                  

            # Final presentation & updating
            
            enemy_change = "%s (Rank %s)  > %s (Rank %s)" % (random_boss.enemy_classes[0].enemy_name, prev_rank, original_boss.enemy_classes[0].enemy_name, new_rank)

            
            random_boss.random_boss_rank = new_rank
            random_boss.enemy_change = enemy_change


        self.EM.relevant_enemies = list_of_randomized_enemies
        

        
    def randomize_job_color_palettes(self):
        if True: # Future - flag for if all job palettes shuffled (for all chars and jobs)
            palettes = [self.DM.files['job_color_palettes'][i]['byte_string'] for i in self.DM.files['job_color_palettes']]
            self.RE.shuffle(palettes)
            output_str = "\n\n; JOB COLOR PALETTES \n\norg $D4A3C0\ndb "
            for palette in palettes:
                palette_asar = ["$"+palette[z:z+2]+", " for z in range(0,len(palette),2)]
                output_str = output_str + ''.join(palette_asar)
            output_str = output_str[:-2]
            #logger.debug(output_str)
            return output_str
        
        if False: # Future - flag for keeping palettes among characters
            output_str = "\n\n; JOB COLOR PALETTES \n\norg $D4A3C0\ndb "
            for character in self.DM.files['job_color_palettes']['char'].unique():
                palettes_df = self.DM.files['job_color_palettes']
                palettes_df = palettes_df[palettes_df['char']==character]
                palettes = palettes_df['byte_string'].to_list()
                self.RE.shuffle(palettes)
                for palette in palettes:
                    palette_asar = ["$"+palette[z:z+2]+", " for z in range(0,len(palette),2)]
                    output_str = output_str + ''.join(palette_asar)
            output_str = output_str[:-2]
            logger.debug(output_str)
            return output_str
        
        
    def randomize_dragon(self):
        return '''
                    org $C33320
                
                dw $0100
                dw $0000
                
                !color_num = 15
                while !color_num > 0 
                    dw $%s
                    !color_num #= !color_num-1
                endif
                
                
                    ''' % i2b(self.RE.randint(0,65535))
        
        
    def set_portal_boss(self, output_str):
        if self.portal_boss == "Random":
            portal_boss_str = random.choice(['DragonClan','RainSenshi','SomberMage', 'Tetsudono'])
        else:
            portal_boss_str =  self.portal_boss
        self.portal_boss_str = portal_boss_str
            
        output_str = self.EM.set_portal_boss(self.DM.files['portal_bosses'],portal_boss_str, output_str)
        return output_str

    def spoiler_intro(self):
        output = ""
        output = output + VERSION
        output = output + "\nSeed: " + str(self.seed)
        output = output + "\nSetting String: " + self.setting_string + "\n\n"

        return output
            

    def starting_crystal_patch(self):
        output = ";================"
        output = output + "\n;starting crystal"
        output = output + "\n;================\n"
        output = output + "org $" + self.conductor_config['STARTING_CRYSTAL_ADDRESS']
        output = output + "\ndb $" + self.starting_crystal.patch_id
        output = output + ", $" + str(self.starting_crystal.starting_spell_id).replace("'","")
        
        
        if self.fjf:
            for crystal in self.chosen_crystals:
                index = self.RE.randint(0, len(crystal.starting_spell_list)-1)
                crystal.starting_spell = crystal.starting_spell_list[index]
                crystal.starting_spell_id = crystal.starting_spell_ids[index]
                if "'" in crystal.starting_spell_id:
                    crystal.starting_spell_id = crystal.starting_spell_id.replace("'","")

                output = output + ", $" + crystal.patch_id
                output = output + ", $" + crystal.starting_spell_id
        output = output + "\n"
        return output

    def starting_crystal_spoiler(self):
        output = "-------STARTING JOB, WEAPON, MAGIC------"
        output = output + "\nStarting job:     " + self.starting_crystal.reward_name    
        output = output + "\nStarting weapon:  " + self.starting_crystal.starting_weapon
        output = output + "\nStarting spell:   " + self.starting_crystal.starting_spell
        if not self.starting_crystal.starting_ability:
            ability_start = '00'
        else:
            ability_start = self.starting_crystal.starting_ability
        output = output + "\nStarting ability: " + ability_start
        output = output + "\n----------------------------------------\n"
        if self.fjf:
            output = output + "Four Job Mode:"
            for crystal in self.chosen_crystals:
                output = output + "\n" + crystal.reward_name[:crystal.reward_name.find(" ")]
                if crystal.starting_spell != "":
                    output = output + " - " + crystal.starting_spell
            output = output + "\n\n"  

        return output
    

    
    def randomize_superbosses(self):
        elemental_map = {
            'fire':'01',
            'ice':'02',
            'lightning':'04',
            'poison':'08',
            'holy':'10',
            'earth':'20',
            'wind':'40',
            'water':'80',
            }
            
        # organized by status, then offset
        status_map = {
        'darkness':('01','status0'),
        'zombie':('02','status0'),
        'poison':('04','status0'),
        'float':('08','status0'),
        'mini':('10','status0'),
        'toad':('20','status0'),
        'petrify':('40','status0'),
        'dead':('80','status0'),
        'image1':('01','status1'),
        'image2':('02','status1'),
        'mute':('04','status1'),
        'berserk':('08','status1'),
        'charm':('10','status1'),
        'paralyze':('20','status1'),
        'sleep':('40','status1'),
        'aging':('80','status1'),
        'regen':('01','status2'),
        'invul':('02','status2'),
        'slow':('04','status2'),
        'haste':('08','status2'),
        'stop':('10','status2'),
        'shell':('20','status2'),
        'armor':('40','status2'),
        'wall':('80','status2')
        }
            
        creature_map = {
            'undead':'01',
            'toad':'02',
            'creature':'04',
            'avis':'08',
            'dragon':'10',
            'heavy':'20',
            'desert':'40',
            'human':'80'
            }
           
        for i in self.EM.enemies:
            if i.idx == 253:
                OMEGA = i
            elif i.idx == 361:
                SHINRYUU = i
            elif i.idx == 11:
                MAGICPOT = i # we're not randomizing them, but we need them in self.relevant_enemies

        # Have to do it somewhere - add Magic Pot to relevant enemies
        self.EM.relevant_enemies.append(MAGICPOT)

        # helper functions 
        def add_hex(x,y):
            return hex(int(x,base=16) + int(y,base=16)).replace("0x","")[0:2] 

        def elemental_randomize():
            
            # Now, this is hardcoded for: 
            # 3 Absorbs
            # 3 Immunities
            # 2 Weaknesses
            immunity_start = 3
            weakness_start = 7
            
            random_elements = sorted(list(elemental_map.keys()), key=lambda k: self.RE.random())
            absorbs, immunities, weaknesses = random_elements[:immunity_start], random_elements[immunity_start:weakness_start], random_elements[weakness_start:]
            
            
            absorb_hex = '00'
            for i in absorbs:
                absorb_hex = add_hex(absorb_hex,elemental_map[i])
            immunities_hex = '00'
            for i in immunities:
                immunities_hex = add_hex(immunities_hex,elemental_map[i])
            weakness_hex = '00'
            for i in weaknesses:
                weakness_hex = add_hex(weakness_hex,elemental_map[i])
                
            return absorbs, immunities, weaknesses, absorb_hex, immunities_hex, weakness_hex

        def status_afflict_randomize():            
            
            # Hardcoded number of status afflictions for now:
            num_afflict = 1
            
            status_afflict = []
            random_statuses = sorted(list(status_map.keys()), key=lambda k: self.RE.random())
            while num_afflict > 0:
                i = self.RE.choice(random_statuses)
                random_statuses.remove(i)
                if i not in ['image1','image2','haste','stop','regen','shell','armor','wall','invul']:
                    status_afflict.append(i)
                    num_afflict = num_afflict - 1
            return status_afflict        
            
           
        #####################################    
        # First randomize stats - these are all stored with the enemy and will get written
        # as part of the Conductor.randomize() method with the enemy spoiler patch
        #####################################    
        output_str = ''
        self.superbosses_spoiler = self.superbosses_spoiler + '\n-----SUPERBOSSES:-----\n'
        for random_enemy in [OMEGA,SHINRYUU]:
            ######################################
            # Elemental Absorb/Immune/Weakness
            ######################################
            self.superbosses_spoiler = self.superbosses_spoiler +'-----------'+ random_enemy.enemy_name.upper() + "-----------\n"
            # Force elemental immunities to be zero - using an absorb/weakness system only 
            
            random_enemy_absorbs, random_enemy_immunities, random_enemy_weaknesses, random_enemy_absorb_hex, random_enemy_immunities_hex, random_enemy_weakness_hex = elemental_randomize()
            
            self.superbosses_spoiler = self.superbosses_spoiler + "Absorbs "+str(random_enemy_absorbs)+" Immunities "+str(random_enemy_immunities)+" Weaknesses: "+str(random_enemy_weaknesses)+'\n'
            
            # Formally set the bytes to the object now
            random_enemy.elemental_absorb = random_enemy_absorb_hex
            random_enemy.elemental_immune = random_enemy_immunities_hex
            random_enemy.elemental_weakness = random_enemy_weakness_hex
            ######################################
            # Status Afflictions 
            ######################################
            random_enemy_status_afflict = status_afflict_randomize()
            
            self.superbosses_spoiler = self.superbosses_spoiler + "Status afflictions (weaknesses) "+str(random_enemy_status_afflict)+"\n"
            
            random_enemy_status0, random_enemy_status1, random_enemy_status2 = '00','00','00'
            for status in random_enemy_status_afflict:
                status_hex, status_index = status_map[status][0], status_map[status][1]
                if status_index == 'status0':
                    random_enemy_status0 = add_hex(random_enemy_status0, status_hex)
                if status_index == 'status1':
                    random_enemy_status1 = add_hex(random_enemy_status1, status_hex)
                if status_index == 'status2':
                    random_enemy_status2 = add_hex(random_enemy_status2, status_hex)
                    
            # Now we have three hexes of what the statuses are, but we need to INVERT them because
            # it's immunity. So all other statuses will be immune except these
            
            random_enemy_status0 = hex(255 - int(random_enemy_status0,base=16)).replace("0x","")
            random_enemy_status1 = hex(255 - int(random_enemy_status1,base=16)).replace("0x","")
            random_enemy_status2 = hex(255 - int(random_enemy_status2,base=16)).replace("0x","")
                    
            # Formally set the bytes to the object now
            random_enemy.status0_immune = random_enemy_status0
            random_enemy.status1_immune = random_enemy_status1
            random_enemy.status2_immune = random_enemy_status2
            
    
            ######################################
            # Enemy type 
            ######################################
            
            # Choose a random type
            random_type = self.RE.choice(list(creature_map.keys()))
            # If it's not heavy, make it heavy too
            if random_type != 'heavy':
                random_enemy.enemy_type = add_hex(creature_map[random_type],'20') # heavy + random type
                self.superbosses_spoiler = self.superbosses_spoiler + "Enemy type - heavy and "+random_type+"\n"
            else:
                random_enemy.enemy_type = creature_map[random_type] # heavy
                self.superbosses_spoiler = self.superbosses_spoiler + "Enemy type - heavy\n"
            
            
            ######################################
            # Stats 
            ######################################
            
            # Randomize levels and stats 
            # A few stats will have a random int from -10 to 10 applied
            for stat in ['num_phys_power','num_phys_def','num_evade','num_mag_power','num_mag_def','num_level']:
                new_stat = str(round(int(getattr(random_enemy,stat)) + self.RE.randint(-10,10)))
                setattr(random_enemy,stat,new_stat)
                self.superbosses_spoiler = self.superbosses_spoiler + "Stat "+stat+" changed to "+new_stat+"\n"
            
            # Magic Evade decreased to $20 
            # This is done so the player can reasonably use the statuses they found out, 
            #   and not fail to use their new knowledge because of insanely high mag evade
            random_enemy.num_mag_evade = 32
            self.superbosses_spoiler = self.superbosses_spoiler + "Stat num_mag_evade changed to 32\n"
            
            # Finally post updates to stats
            random_enemy.update_all()
            
            
            #####################################    
            # Now randomize the AI, somewhat manually
            #####################################    
            aoe_skills = ['45','84','85','86','87','88','AB','B6','B9','CC','CD','CF','D0','D1','D2','D6','DA','DB','DC','DD','C2']
            single_target_skills = ['B2','B3','B4','30','31','32','33','34','35','3C','3F','42','43','81','8C','8E','91','92','93','97','98','99','9C','9D','9F','B0','B7','B8','BD','C3','C4','C5','C6','C7','E8','22','2F','C0','80']
            status_skills = ['15','37','39','3A','3D','40','44','82','83','89','8A','8B','8D','94','95','9A','B5','BB','BC','EB','2E']
            
            
            skill_name_dict = [(value, key) for key, value in self.DM.files['enemy_skills'].items()]

            output_str = output_str + ';  ########################### \n'
            output_str = output_str + ';  # New AI for enemy: '+random_enemy.enemy_name+'\n'
            output_str = output_str + ';  ########################### \n'

            aoe_skill_names = []
            single_skill_names = []
            status_skill_names = []
            if random_enemy.idx == 253: # OMEGA
                ai_aoe = ['D0B235','D0B238','D0B23D','D0B245','D0B248','D0B24E']
                ai_single = ['D0B236','D0B237','D0B23A','D0B23B','D0B23C','D0B243','D0B244','D0B247','D0B249','D0B24C','D0B24D','D0B25B','D0B25C','D0B25F','D0B260']
                ai_status = ['D0B25D','D0B261']
                
            if random_enemy.idx == 361: # SHINRYUU
                ai_aoe = ['D0C532','D0C533','D0C534','D0C53F','D0C540','D0C55C','D0C567']
                ai_single = ['D0C52F','D0C53B','D0C546','D0C547','D0C54A','D0C54B','D0C52E']
                ai_status = ['D0C530','D0C53A','D0C53C','D0C53E','D0C548','D0C54C']
            for ai in ai_aoe:
                random_skill_hex = self.RE.choice(aoe_skills)
                random_skill_name = self.DM.files['enemy_skills'][random_skill_hex]['name']
                aoe_skill_names.append(random_skill_name)
                output_str = output_str + '; New AOE skill: '+random_skill_name+'\norg $'+ai+'\ndb $'+random_skill_hex+'\n'
            for ai in ai_single:
                random_skill_hex = self.RE.choice(single_target_skills)
                random_skill_name = self.DM.files['enemy_skills'][random_skill_hex]['name']
                single_skill_names.append(random_skill_name)
                output_str = output_str + '; New single target skill: '+random_skill_name+'\norg $'+ai+'\ndb $'+random_skill_hex+'\n'
            for ai in ai_status:
                random_skill_hex = self.RE.choice(status_skills)
                random_skill_name = self.DM.files['enemy_skills'][random_skill_hex]['name']
                status_skill_names.append(random_skill_name)
                output_str = output_str + '; New status skill: '+random_skill_name+'\norg $'+ai+'\ndb $'+random_skill_hex+'\n'
            self.superbosses_spoiler = self.superbosses_spoiler + "AOE skills: "+str(aoe_skill_names)+"\n"
            self.superbosses_spoiler = self.superbosses_spoiler + "Single target skills: "+str(single_skill_names)+"\n"
            self.superbosses_spoiler = self.superbosses_spoiler + "Status skills: "+str(status_skill_names)+"\n\n\n"
            
            
            # Add these to the relevant enemies list             
            self.EM.relevant_enemies.append(random_enemy)
            
                
            # Then update dialogue for NPCs in Mirage Village & Moogle Forest
            
            # e303ac mirage start
            

            
            if random_enemy.idx == '253' or random_enemy.idx == 253: # OMEGA
                output_str = output_str + "\n\n; ***Mirage Village NPC [Omega]***\n"
                output_str = output_str + "org $E303AC\npadbyte $FF\npad $E30447\npadbyte $00\norg $E303AC\ndb $6E, $6C, $64, $66, $60, $9D, $96, $8D, $81, $7E, $96, $90, $7A, $8B, $96, $86, $7A, $7C, $81, $82, $87, $7E, $A3, $A3, $A3, $01, $81, $7A, $8C, $96, $90, $7E, $7A, $84, $87, $7E, $8C, $8C, $7E, $8C, $A3, $A3, $A3, $01\n"
            if random_enemy.idx == '361' or random_enemy.idx == 361: # SHINRYUU
                output_str = output_str + "\n\n; ***Moogle Forest NPC [Shinryuu]***\n"
                output_str = output_str + "org $E24487\npadbyte $FF\npad $E245C7\npadbyte $00\norg $E24487\ndb $72, $67, $68, $6D, $71, $78, $74, $74, $9D, $96, $8D, $81, $7E, $96, $87, $88, $8F, $7A, $96, $7D, $8B, $7A, $80, $88, $87, $A3, $A3, $A3, $01, $81, $7A, $8C, $96, $90, $7E, $7A, $84, $87, $7E, $8C, $8C, $7E, $8C, $A3, $A3, $A3, $01\n"
            for weakness in random_enemy_weaknesses:
                new_text = weakness[0].upper() + weakness[1:]
                new_text = self.TP.run_encrypt_text_string(new_text)
                output_str = output_str + new_text + ", $01\n"
            output_str = output_str + "db $60, $87, $7D, $96, $7F, $88, $8B, $96, $8C, $8D, $7A, $8D, $8E, $8C, $7E, $8C, $A3, $A3, $A3, $01\n"
            for weakness in random_enemy_status_afflict:
                new_text = weakness[0].upper() + weakness[1:]
                new_text = self.TP.run_encrypt_text_string(new_text)
                output_str = output_str + new_text + ", $01\n"
            output_str = output_str + "db $00\n"
            
                
            
            
            
            
            
            
            
        # # Finally, create the "CODE OF THE VOID"
        
        # # For some reason, couldn't get this to load in from star import from text_parser
        # text_dict2 = self.TP.text_dict2
        # #text_dict2 = pd.read_csv(os.path.join(os.path.pardir,'data','tables','text_tables','text_table_chest.csv'),header=None,index_col=1).to_dict()[0]
        
        # letters = self.RE.sample('ABCDEFGHIJKLMNOPQRSTUVWXYZ',6)
        # code_str = 'db '
        # for letter in letters:
        #     code_str = code_str + "$" +str(text_dict2[letter]) + ", "
        # code_str = code_str[:-2]
        # output_str = output_str + '\n; CODE OF THE VOID: \norg $E77476\n'+code_str+'\norg $F80900\n'+code_str+'\n\n'

        
        # self.superbosses_spoiler = self.superbosses_spoiler + "-----CODE OF THE VOID-----\n"+''.join(letters)+"\n\n"
            
        return output_str
    
    def assign_hints(self):
        # hint_text will be a list of text strings with hints
        hint_text = []

        keys = self.RM.get_rewards_by_style('key')
        if self.key_items_in_mib:
            keys = keys + self.RM.get_rewards_by_style('mib_key')
    
        keys = [i for i in keys if i.description != 'WingRaptor' and i.description != "Beginner's House Chest MIB 1"]
        keys_main = []
        areas_barren = []
        for i in keys:
            keys_main.append(i)

        areas_barren = list(set(areas_barren))
        self.RE.shuffle(keys_main)
        self.RE.shuffle(areas_barren)
        
        keys_hint1 = keys_main[:15]
        
        ###########
        # DIRECT
        ###########
        # Pick 3 hints to say "X" item is at "Y" location
        
        for key in keys_hint1:
            if key.collectible.name == "Arch Item":
                # try to parse player name, if not, default to player number
                try:
                    hint_str = "They say that %s|holds %s's|%s." % (key.area, self.arch_options['all_player_names'][key.collectible.arch_player][:25], key.collectible.collectible_name[:25])
                except:
                    hint_str = "They say that %s|holds player %s's|%s." % (key.area, key.collectible.arch_player, key.collectible.collectible_name[:25])
            else:
                hint_str = "They say that %s|holds this player's|%s." % (key.area, key.collectible.collectible_name[:25])
            hint_text.append(hint_str)

        # ###########
        # # BARREN
        # ###########

        # for area in areas_barren[:5]:
        #     hint_str = "They say that %s|holds no progression items." % (area)
        #     hint_text.append(hint_str)

        ###########
        # DATA
        ###########
        
        hint_data = [self.DM.files['hints'][i]['start'] for i in self.DM.files['hints']]
        
        hint_data_str = []
        tp = TextParser(self.config)
        for hint in hint_text:
            try:
                hint_data_str.append(tp.run_encrypt_text_string_hints(hint) + ", $00")
            except:
                pass
            
        # didnt generate enough hints for barren areas, filler hints
        if len(hint_data) > len(hint_data_str):
            delta = len(hint_data) - len(hint_data_str)
            for _ in range(0, delta):
                empty_hint = self.RE.choice(["They say that ExDeath|was not such a bad guy.",
                                             "They say that Enuo|supported local businesses.",
                                             "They say that Triton|likes bubble tea.",
                                             "They say that Phobos|is a fan of eggs.",
                                             "They say that Nereid|doesn't like to swim.",
                                             "They say that ArcheoAvis|wants a hug.",
                                             "They say that Titan|likes takoyaki.",
                                             "They say that Queen|Karnak enjoys singing.",])
                hint_text.append(empty_hint)
                hint_data_str.append(tp.run_encrypt_text_string_hints(empty_hint) + ", $00")
            

        hint_data = dict(zip(hint_data, hint_data_str))
        
        output_str_asar = '\n; Hints\n'
        for k, v in hint_data.items():
            output_str_asar = output_str_asar + "org $" + k + "\n" + v + "\n"
            
        output_str = '\n\n-----HINTS-----\n\n'
        for i in hint_text:
            output_str = output_str + i + "\n"
        return output_str_asar, output_str.replace("|"," ")
        
    def randomize_loot(self,loot_percent=25,loot_type='match'):
        loot_list = ['steal_common','steal_rare','drop_common','drop_rare']
        ''' 
        arguments:
        match = if the original enemy has a non-null loot slot, update it
        full = every enemy has randomized common/rare steal/drop
        variable = every enemy has randomized common/rare steal/drop at a specified chance (variable RANDOM_LOOT_PERCENT) per slot 
        '''
        
        try:
            loot_type = self.randomize_loot_setting.strip()
            loot_percent = self.loot_percent
            try:
                loot_percent = int(loot_percent)
            except:
                loot_percent = 25 # defaults to 25
        except Exception as e:
            loot_percent = 25 # defaults to 25
            logger.debug("Error on loot type parse: %s" % (e))
        for enemy in self.EM.enemies:
            for loot in loot_list:
                # Choose item:
                df = self.DM.files['items']
                df = df[df['valid']=="TRUE"]
                new_item_id = self.RE.choice(list(df.index))
                new_item_name = self.DM.files['items']['readable_name'].loc[new_item_id]
                
                
                if loot_type=='match':
                    if getattr(enemy,loot) != '00':
                        setattr(enemy,loot,new_item_id)
                        setattr(enemy,loot+"_name",new_item_name)
                elif loot_type=='full':
                    setattr(enemy,loot,new_item_id)
                    setattr(enemy,loot+"_name",new_item_name)
                elif loot_type=='variable':
                    if self.RE.randint(1,100) <= loot_percent: 
                        setattr(enemy,loot,new_item_id)
                        setattr(enemy,loot+"_name",new_item_name)
                    else:
                        setattr(enemy,loot,'00')
                        setattr(enemy,loot+"_name"," ")
                else:
                    logger.debug("Invalid loot randomize argument %s" % (loot_type))
                    
                    
    def randomize_weapons(self):
        logger.debug("Beginning weapon randomization...")
        weapon_shop_price_patch = self.WM.randomize()
        if len(self.WM.banned_items) > 0:
            for _ in range(3):
                for weapon in self.WM.banned_items:
                    try:
                        self.CM.add_to_placement_history(self.CM.get_by_name(weapon['readable_name']),"No")
                    except:
                        logger.debug("Error on placement history %s" % weapon['readable_name'])
        return weapon_shop_price_patch

                    
    def get_collectible_counts(self):
        # Here for this spoiler, we need to collect from both RM and SM to get accurate data, so we do it here:
        spoiler = "\n-----COLLECTIBLE COUNTS BY TYPE-----\n"
        count_dict = {}
        for i in self.RM.rewards:
            if type(i.collectible) not in count_dict.keys():
                count_dict[type(i.collectible)] = 1
            else:
                count_dict[type(i.collectible)] = count_dict[type(i.collectible)] + 1
        
        for shop in self.SM.shops:
            for i in shop.contents:
                if type(i) not in count_dict.keys():
                    count_dict[type(i)] = 1
                else:
                    count_dict[type(i)] = count_dict[type(i)] + 1
                
        for key, val in count_dict.items():
            try:
                new_str =  '{:12}'.format(str(key.name) + ": ") +  '{:12}'.format(str(val)) + "\n"
                spoiler = spoiler + new_str
            except:
                pass
        return spoiler + "\n"
    def karnak_escape_patch(self):
        '''
        Random song chosen, outputs asar code
        '''
        songs = ['00','01','02','03','04','05','06','07','08','09',
                 '0A','0B','0C','0D','0E','0F','10','12','13','14',
                 '15','16','17','18','19','1A','1B','1C','1D','1E',
                 '1F','20','21','22','23','24','25','26','27','28',
                 '2B','2C','2D','2E','2F','30','31','32','33','3D',
                 '3F','40','41','42','43','44']
        song = self.RE.choice(songs)
        return ';Karnak escape song\norg $C8796D\ndb $'+song+"\n"
    

    def kuzar_text_patch(self):
        kuzar_reward_addresses = ['C0FB06','C0FB02','C0FB16','C0FB0C','C0FB12','C0FB0E','C0FB18','C0FB08','C0FB14','C0FB10','C0FB04','C0FB0A']
        kuzar_text_addresses =   ['E23F7A',
                                    'E23F98',
                                    'E23FB7',
                                    'E23FD6',
                                    'E23FF4',
                                    'E24011',
                                    'E2402D',
                                    'E2404C',
                                    'E2406A',
                                    'E24088',
                                    'E240A5',
                                    'E240C4']
        
        output = ";=====================\n"
        output = output + ";Kuzar Reward Text Fix\n"
        output = output + ";=====================\n"
        
        try:
            randomized_weapons_ids = [i.data_dict['item_id'] for i in self.WM.weapons]
        except:
            logger.debug("No weapon manager, skipping...")

        for i in range(0, len(kuzar_reward_addresses)):
#            logger.debug(i)
            #logger.debug("working on address: " + kuzar_reward_addresses[i])
            data = self.RM.get_reward_by_address(kuzar_reward_addresses[i]).collectible
    #            logger.debug("Kuzar start: %s" % (data.reward_name))
            try:

                if data.type == 'weapon' and data.reward_id in randomized_weapons_ids:
                    matched_weapon = [x for x in self.WM.weapons if data.reward_id == x.data_dict['item_id']][0]
#                    logger.debug("Kuzar weapon name swap: %s -> %s" % (data.reward_name, matched_weapon.text_textbox))

                    kuzar_text = self.TP.run_kuzar_encrypt({matched_weapon.text_textbox: kuzar_text_addresses[i]})
                    output = output + kuzar_text
                else:

                    temp_reward_name = data.reward_name.replace('->', '@').replace(' Progressive', '@')
                    if 'magic_id' in data.__dict__.keys():
                        temp_reward_name = "%s %s Magic" % (temp_reward_name, data.type)
                    
                    kuzar_text = self.TP.run_kuzar_encrypt({temp_reward_name: kuzar_text_addresses[i]})
#                    logger.debug("Kuzar normal: %s" % (data.reward_name))
                    output = output + kuzar_text

            except:
                #logger.debug("collectible there is: " + c.reward_name)
                #@ will be used for our newline character, won't otherwise be present, and don't have the problems \n causes
                kuzar_text = self.TP.run_kuzar_encrypt({data.reward_name.replace('->', '@').replace(' Progressive', '@'): kuzar_text_addresses[i]})
#                logger.debug("Kuzar normal: %s" % (data.reward_name))
                output = output + kuzar_text

        return output


    def name_characters(self):
        asar_str = '; Character Names\n'
        asar_str = asar_str + 'org $C0BEC9\n'
        asar_str = asar_str + self.TP.run_encrypt_text_string(self.lenna_name,ff_fill=8)
        asar_str = asar_str +'\norg $C0BED1\n'
        asar_str = asar_str + self.TP.run_encrypt_text_string(self.galuf_name,ff_fill=8)
        asar_str = asar_str +'\norg $C0BED9\n'
        asar_str = asar_str + self.TP.run_encrypt_text_string(self.faris_name,ff_fill=8)
        asar_str = asar_str +'\norg $C0BEE1\n'
        asar_str = asar_str + self.TP.run_encrypt_text_string(self.cara_name,ff_fill=8)
        return asar_str
        
    def translateBool(self, boolean):
        
        if type(boolean) == bool:
            # logger.debug("Argument passed in to translate: %s, returning original as boolean" % (boolean))
            return boolean
        if boolean == "false" or boolean == "False" or boolean == "off" or boolean == "0" or boolean == 0:
            # logger.debug("Argument passed in to translate: %s, returning boolean False" % (boolean))
            return False
        if boolean == "true" or boolean == "True" or boolean == "on" or boolean == "1" or boolean == 1:
            # logger.debug("Argument passed in to translate: %s, returning boolean True" % (boolean))
            return True
        else:
            # logger.debug("Argument passed in to translate: %s, returning NONETYPE" % (boolean))
            return None
        
#   Unused, but may be necessary one day. The concept here is to iterate through unplaced collectibles and assign them to random rewards
#    def cleanup_seed(self):
#        non_placed_collectibles = [y for y in [x for x in self.CM.collectibles if x.placed_reward==None] if y.valid]
#        

    # def spoiler_settings(self):
    #     output_str = '\n-----SETTINGS-----\n'
    #     for k, v in self.configs.items():
    #         if k == 'portal_boss' and v == "Random":
    #             v = "%s (%s)" % (v, self.portal_boss_str)
    #         output_str = output_str + '{:30}'.format(str(k)) + '{:30}'.format(str(v)) + "\n"
    #     return output_str + "\n"
    
    def fix_random_ned(self):
        asar_str = '; Fix 2nd NED slot\n'
        d = [x for x in self.FM.formations if x.event_lookup_loc1 == 'D078E8'][0]
        asar_str = asar_str + "org $D078A0\ndb $%s, $%s\n\n" % (d.event_formation_reference[0:2],d.event_formation_reference[2:4])
        return asar_str 
        
        

    def parse_configs(self):
        r_color = int(self.red_color)
        g_color = int(self.green_color) * 32
        b_color = int(self.blue_color) * 1024

        colors = hex(r_color+g_color+b_color).replace("0x","")
        # logger.debug(colors)
        
        if len(colors) == 0:
            colors = "0000"
        elif len(colors) == 1:
            colors = "000" + colors 
        elif len(colors) == 2:
            colors = "00" + colors 
        elif len(colors) == 3:
            colors = "0" + colors 
        c1 = colors[0:2]
        c2 = colors[2:4]
        
        patch = ";CONFIG SETTINGS\n"
        patch = patch + ";RGB\norg $C0F343\ndb $%s, $%s" % (c2,c1)
                
        reward_dict = {4:"28",3:"28",2:"18",1:"08"}
        try:
            reward_val = reward_dict[int(self.exp_mult)]
        except:
            reward_val = reward_dict[4]
            
        battle_speed = int(self.battle_speed)
        if battle_speed > 0 and battle_speed < 7: # validation
            battle_speed = "0" + str(battle_speed-1)
            reward_val = i2b(b2i(reward_val ) + b2i(battle_speed))
        
        
        patch = patch + "\n;Reward Mult\norg $C0F342\ndb $%s" % (reward_val)
#        logger.debug(patch)
        return patch
        
    def goal_settings(self):
        goal_array = ["ExDeath1", "Pianos"]
        goal_dict: Dict[str, bool]
        goal_dict = {flag_name: False for flag_name in goal_array}

        if self.arch_options["piano_percent"]:
            goal_dict["Pianos"] = True

        goal_bitfield = 0
        for i, flag_name in enumerate(goal_array):
            if goal_dict[flag_name]:
                goal_bitfield |= 1 << i

        goal_bitfield = i2b(goal_bitfield)
        goals = "\n;Goals\norg $FFFFFF\ndb $%s" % (goal_bitfield)

        return goals

    
    def create_hash(self):
        choices = {"BB":"Crystal",
                    "BC":"Key",
                    "BF":"Hammer",
                    "C0":"Tent",
                    "C1":"Ribbon",
                    "C2":"Drink",
                    "C3":"Suit",
                    "C4":"Song",
                    "C6":"Shuriken",
                    "C8":"Scroll",
                    "CA":"Claw",
                    "CC":"Glove",
                    "E3":"Sword",
                    "E4":"White",
                    "E5":"Black",
                    "E6":"Time",
                    "E7":"Knife",
                    "E8":"Spear",
                    "E9":"Axe",
                    "EA":"Katana",
                    "EB":"Rod",
                    "EC":"Staff",
                    "ED":"Bow",
                    "EE":"Harp",
                    "EF":"Whip",
                    "F0":"Bell",
                    "F1":"Shield",
                    "F2":"Helmet",
                    "F3":"Armor",
                    "F4":"Ring",}
        
        choice_list = choices.keys()
        chosen = [random.choice(list(choice_list)) for i in range(0,5)]
        
        patch = '\n;HASH CODE\norg $E73400\ndb $67, $7A, $8C, $81, $CF, $96'
        spoiler = 'HASH CODE: '
        for c in chosen:
            spoiler += "%s " % choices[c]
            patch += ", $%s, $96" % c
            
            
        patch += ', $00\n\n'
        spoiler += '\n'
        return spoiler, patch        
        

        
    
    def save_patch(self, output_directory):
        logger.debug("Finished randomization process, saving to file.")
        self.patch_path = os.path.join(output_directory,'ffvcd-patch-%s-%s.asm' % (self.player, self.seed))
        with open(self.patch_path,'w') as f:
            f.write(self.patch)

        return self.patch_path

        
    def patch_file(self, output_directory):
        self.filename_randomized = patcher.process_new_seed(self.seed, self.arch_options, output_directory)
        return self.filename_randomized

    def randomize(self, random_engine=None):

        pass_flag = True # true until process fails
        
        logger.debug("Starting randomization process.")
        if random_engine is None:
            random_engine = self.RE
        
        self.AM.change_power_level(float(self.conductor_config['DEFAULT_POWER_CHANGE']))
        
        arch_data = self.DM.files['arch_id']
        

        for address, arch_item_data in self.arch_data.items():
            if address == 'C0FFFE':
                logger.debug("Skipping Exdeath W2 at C0FFFE")
                continue
            if address == 'C0FFFF':
                logger.debug("Skipping Exdeath at C0FFFF")
                continue
            
            
            arch_player = arch_item_data['loc_player']
            arch_item_name = arch_item_data['loc_name']
            arch_item_progression = arch_item_data['loc_progression']
            arch_mib_flag = arch_item_data['loc_mib_flag']
            arch_region_rank = arch_item_data['loc_region_rank']
            
            
            
            try:
                
                # find matching reward based on address
                reward = self.RM.get_reward_by_address(address)
                
                # find matching collectible based on arch_id.json
                
                if arch_player != self.player:
                    collectible = self.CM.create_arch_item(arch_item_name, arch_player, arch_item_progression)
                else:
                    entry = arch_data[[i for i in arch_data if arch_data[i]['name'] == arch_item_name][0]]
                    collectible = self.CM.get_by_arch(entry['item_type'], entry['item_id'])                
                    
                if collectible:
                    reward.set_collectible(collectible)
                    setattr(reward, 'reward_arch', arch_item_name)
                    setattr(reward, 'reward_arch_player', arch_player)
                    
                    if arch_mib_flag and self.arch_options['trapped_chests'] and collectible.name != 'Gil':
                        
                        # update chest flag - Ax will change it to MIB for items 
                        setattr(reward, 'reward_arch_mib_flag', arch_mib_flag)
                        setattr(reward, 'reward_arch_region_rank', arch_region_rank)
                        mib_modifier = str(arch_region_rank)
                        if mib_modifier == '10':
                            mib_modifier = 'A'
                        
                        if collectible.reward_type in ['70','40']:
                            new_reward_type = "A%s" % mib_modifier
                        elif collectible.reward_type == '30':
                            new_reward_type = "B%s" % mib_modifier 
                        elif collectible.reward_type == '60':
                            new_reward_type = "C%s" % mib_modifier 
                        elif collectible.reward_type == '20':
                            new_reward_type = "D%s" % mib_modifier 
                        elif collectible.reward_type == '50':
                            new_reward_type = "E%s" % mib_modifier 
                        
                        #    if collectible.reward_type == '60':
                        #        collectible.ability_id = str(hex(int(("0x" + collectible.ability_id),16) + int("0x40",16)))

                        reward.mib_chest_id = new_reward_type
                else:
                    logger.warning("Error on assigning collectible to reward %s" % arch_item_data)
            except Exception as e:
                logger.warning("Error on %s: %s" % (address, e))

        if self.arch_options['trapped_chests']:
            rank_lookup = self.DM.files['mib_arch_rank']
            patch = '\n;MIB arch\norg $D07984\n'
            for rank in range(1,11):


                    
                chosen_idx = self.RE.choice([i for i in rank_lookup if rank_lookup[i] == rank])
                chosen_formation = [i for i in self.FM.formations if i.idx == chosen_idx][0]
                chosen_formation.mib_arch_flag = True
                chosen_formation.region_rank = rank
                
                formation_code = hex(int(chosen_idx) - 1).replace("0x","")
                
                if len(formation_code) > 2:
                    formation_code = "%s, $01" % (formation_code[1:])
                else:
                    formation_code = "%s, $00" % formation_code
            
                patch += 'db $%s\n' % formation_code
                patch += 'db $%s\n' % formation_code # doubled because of ffv vanilla weirdness
            self.FM.mib_arch_patch = patch

        logger.debug("Randomizing shops...")
        self.randomize_shops()
        
        
        
        for i in self.RM.rewards: #this is a fix for an unsolved bug where some rewards don't get collectibles. it's rare, but it happens
            if i.collectible is None:
                if i.reward_style != 'key':
                    logger.debug("\nUNSOLVED BUG: Placing reward for key item...\n")
                    i.collectible = self.CM.get_random_collectible(self.RE, monitor_counts=True, gil_allowed=False, tiering_config=self.tiering_config, tiering_percentage=self.tiering_percentage, tiering_threshold=self.tiering_threshold)

        
        logger.debug("Randomizing bosses...")
        self.randomize_bosses()

        for i in self.RM.rewards:
            if i.collectible is None:
                logger.debug(i.description)
        
        
        if self.item_randomization:
            logger.debug("Randomizing weapons...")
            weapon_shop_price_patch = self.randomize_weapons()

#        logger.debug("Running cleanup for guaranteeing collectibles")
#        self.cleanup_seed()
        if self.randomize_loot_setting:
            logger.debug("Randomizing loot...")
            self.randomize_loot()
        
        # Patch now comes first, because some functions (randomize_superbosses) now create the spoiler as part of their process
        logger.debug("Creating spoiler & asm patch...")
        patch = "hirom\n\n"
        patch = patch + self.starting_crystal_patch()
        patch = patch + self.RM.get_patch()
        patch = patch + self.exdeath_patch
        patch = patch + self.SM.get_patch()
        patch = patch + self.SPM.get_patch()
        patch = patch + self.randomize_superbosses() # this comes first, because it updates the contents of EnemyManager. 
        patch = patch + self.set_portal_boss(patch)
        patch = patch + self.EM.get_patch(relevant=True)
        patch = patch + self.FM.get_patch(self.remove_ned)
        # patch = patch + self.karnak_escape_patch()
        patch = patch + self.kuzar_text_patch()
        patch = patch + self.name_characters()
        patch = patch + self.odin_location_fix_patch
        if self.randomize_loot_setting:
            patch = patch + self.EM.get_loot_patch()
        if self.item_randomization:
            patch = patch + self.WM.get_patch
            patch = patch + weapon_shop_price_patch 
        if self.default_abilities:
            default_patch, default_spoiler = randomize_default_abilities(self.RE)
            patch = patch + default_patch
        if self.learning_abilities:
            learning_patch, learning_spoiler = randomize_learning_abilities(self.RE)
            patch = patch + learning_patch

        if self.free_shops:
            logger.debug("Free shops...")
            patch = patch + free_shop_prices()
        if self.remove_ned:
            patch = patch + self.fix_random_ned()            

            
        patch = patch + self.parse_configs()
        patch = patch + self.goal_settings()
        
        spoiler = ""
        if self.seed is not None and self.setting_string is not None:
            spoiler = spoiler + self.spoiler_intro()


        
        logger.debug("Retreiving spoiler data")
        # spoiler = spoiler + self.spoiler_settings()
        spoiler = spoiler + self.starting_crystal_spoiler()
        spoiler = spoiler + self.get_collectible_counts()                
        spoiler = spoiler + self.RM.get_spoiler(self.world_lock, self.free_tablets, self.arch_options['trapped_chests'])
        spoiler = spoiler + self.SM.get_spoiler()
        # spoiler = spoiler + self.CM.get_spoiler()    
        # spoiler = spoiler + self.EM.get_spoiler()
        # spoiler = spoiler + self.superbosses_spoiler

        if self.arch_options['trapped_chests']:
            spoiler = spoiler + self.FM.get_spoiler_mib_patch()

        if self.item_randomization:
            spoiler = spoiler + self.WM.get_spoiler

        if self.randomize_loot_setting:
            spoiler = spoiler + self.EM.get_loot_spoiler()
        if self.default_abilities:
            spoiler = spoiler + default_spoiler
        if self.learning_abilities:
            spoiler = spoiler + learning_spoiler
        if self.hints_flag:
            temp_hints_asar, temp_hints = self.assign_hints()
            patch = patch + temp_hints_asar
            spoiler = spoiler + temp_hints
        

        logger.debug("Creating hash...")
        temp_hash, temp_hash_patch = self.create_hash()
        patch += temp_hash_patch
        
        hyphens = '----------------------------------------'
        output = '\n%s\nFINAL FANTASY V: CAREER DAY ARCHIPELAGO\nPlayer #: %s\nPlayer Name: %s\n%s\n' % \
            (hyphens, self.arch_options['player'], self.arch_options['player_name'], hyphens)

        spoiler =  output + temp_hash + ("%s" % hyphens) + "\n" + spoiler

        if self.jobpalettes:
            patch = patch + self.randomize_job_color_palettes()


        patch = patch + self.randomize_dragon()
        
        self.spoiler = spoiler
        self.patch = patch

        return 



####################################
######## TESTING AREA ##############
####################################








if False:
    
    for formation in self.FM.formations[:438]:
        hp_total = 0
        for enemy_id in [formation.enemy_1,
                      formation.enemy_2,
                      formation.enemy_3,
                      formation.enemy_4,
                      formation.enemy_5,
                      formation.enemy_6,
                      formation.enemy_7,
                      formation.enemy_8]:
            if enemy_id != 'FF':
                enemy = [i for i in self.EM.enemies if i.idx_hex == enemy_id][0]
                hp_total += enemy.num_hp
        print("%s|%s|%s " % (formation.idx, formation.enemy_list, hp_total))
            
            
            
            
            
        
        
        
        
        
        
    
    
    
    
    
    
    