# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from collections import OrderedDict
import math
from progression_translation import *
import logging


class Collectible(ABC):
    """A single something, retreived from a chest, event, or shop.

    Collectibles are anything the player can receive at any point.
    Collectible is an abstract class and is implemented in currently
    six ways.
    """ 
    def __init__(self, reward_id, reward_name, reward_value, related_jobs,
                 max_count, tier=None, valid = None):
        

        if type(max_count) is float:
            self.max_count = None
        else:
            try:
                self.max_count = int(max_count)
            except:
                self.max_count = None
            
            
        self.reward_id = reward_id
        self.collectible_name = reward_name
        self.reward_value = reward_value
        self.related_jobs = [x.replace('"', '').replace(' ', '')
                              .replace("'", '')
                             for x in related_jobs]
        self.placed_reward = None

        
        if tier is not None:
            self.tier = int(tier)
        else:
            self.tier = None
            
        if valid:
            self.valid = valid
        elif valid is None:
            self.valid = True
        elif not valid:
            self.valid = valid == "TRUE"
        self.place_weight = 1

        @property
        @abstractmethod
        def reward_name(self):
            pass

        @property
        @abstractmethod
        def patch_id(self):
            pass

        @property
        @abstractmethod
        def type_str(self):
            pass

        @property
        @abstractmethod
        def shop_name(self):
            pass
        
class Item(Collectible):
    reward_type = '40'
    name = "Item"
    def __init__(self, item_id, data_row):
        self.type = data_row['type']
        self.subtype = data_row['subtype']
        related_jobs = data_row['related_jobs'].strip('][').split(',')
        super().__init__(item_id, data_row['readable_name'], int(data_row['value']),
                         related_jobs, data_row['max_count'], data_row['tier'], data_row['valid'])

    @property
    def patch_id(self):
        return self.reward_id

    @property
    def reward_name(self):
        return self.collectible_name

    @property
    def type_str(self):
        return "Item"

    @property
    def shop_name(self):
        return self.collectible_name
    
class Magic(Collectible):
    reward_type = '20'
    name = "Magic"
    def __init__(self, magic_id, data_row, collectible_config):
        self.type = data_row['type']
        related_jobs = data_row['related_jobs'].strip('][').split(',')
        self.progression_id = data_row['progression_id']
        self.magic_id = magic_id
        self.collectible_config = collectible_config
        super().__init__(magic_id, data_row['readable_name'], int(data_row['value']),
                         related_jobs, data_row['max_count'], data_row['tier'], data_row['valid'])

    @property
    def patch_id(self):
        if self.collectible_config['progressive_rewards']:
            return self.progression_id
        else:
            return self.magic_id

    '''
    @property
    def reward_name(self):
        return self.collectible_name + " " + self.type
    '''
    
    @property
    def reward_name(self):
        if self.collectible_config['progressive_rewards']:
            if self.progression_id in progression_magic:
                return progression_magic[self.progression_id]
            else:
                return self.collectible_name
        else:
            return self.collectible_name

    @property
    def type_str(self):
        return "Magic"

    @property
    def shop_name(self):
        return "%s (%s)" % (self.collectible_name, self.type)


class Crystal(Collectible):
    reward_type = '50'
    name = "Crystal"
    def __init__(self, crystal_id, data_row):
        self.shop_id = data_row['shop_id']
        self.starting_weapon = data_row['starting_weapon']
        self.starting_weapon_id = data_row['starting_weapon_id']
        self.starting_spell_list = data_row['starting_spell_list'].strip('][').split(',')
        self.starting_spell_list = [x.replace('"', '').replace(' ', '')
                                     .replace('“', '').replace('”', '')
                                    for x in self.starting_spell_list]
        self.starting_spell_ids = data_row['starting_spell_ids'].strip('][').split(',')
        self.starting_spell_ids = [x.replace('"', '').replace(' ', '')
                                     .replace('“', '').replace('”', '')
                                    for x in self.starting_spell_ids]
        self.starting_ability = data_row['starting_ability']
        self.starting_ability_id = data_row['starting_ability_id']
        self.starting_spell = ""
        self.starting_spell_id = ""

        related_jobs = data_row['related_jobs'].strip('][').split(',')
        super().__init__(crystal_id, data_row['readable_name'], int(data_row['value']),
                         related_jobs, data_row['max_count'], data_row['tier'])

    @property
    def patch_id(self):
        return self.reward_id

    @property
    def reward_name(self):
        return self.collectible_name + " " + "Job Crystal"

    @property
    def type_str(self):
        return "Crystal"

    @property
    def shop_name(self):
        return "%s (%s)" % (self.collectible_name, "Crystal")
        
class Ability(Collectible):
    reward_type = '60'
    name = "Ability"
    def __init__(self, ability_id, data_row,collectible_config):
        related_jobs = data_row['related_jobs'].strip('][').split(',')
        self.progression_id = data_row['progression_id']
        self.ability_id = ability_id
        self.collectible_config = collectible_config
        super().__init__(ability_id, data_row['readable_name'], int(data_row['value']),
                         related_jobs, data_row['max_count'], data_row['tier'], data_row['valid'])

    @property
    def patch_id(self):
        if self.collectible_config['progressive_rewards']:
            return self.progression_id
        else:
            return self.ability_id

    '''
    @property
    def reward_name(self):
        return self.collectible_name + " " + "Ability"
    '''

    @property
    def reward_name(self):
        if self.collectible_config['progressive_rewards']:
            if self.progression_id in progression_magic:
                return progression_magic[self.progression_id]
            else:
                return self.collectible_name
        else:
            return self.collectible_name

    @property
    def type_str(self):
        return "Ability"

    @property
    def shop_name(self):
        return "%s (%s)" % (self.collectible_name, "Ability")


class Gil(Collectible):
    name = "Gil"
    reward_type = ""
    def __init__(self, gil_id, data_row):
        self.reward_type = data_row['power_byte']
        self.gil_id = gil_id
        super().__init__(data_row['number_byte'], str(data_row['readable_amount']) + " Gil",
                         int(data_row['value']), [],data_row['max_count'], tier=data_row['tier'])

    @property
    def patch_id(self):
        return self.reward_id

    @property
    def reward_name(self):
        return self.collectible_name

    @property
    def type_str(self):
        return "Gil"

    @property
    def shop_name(self):
        return self.collectible_name

class KeyItem(Collectible):
    name = "Key Item"
    reward_type = '30'
    def __init__(self, keyitem_id, data_row):
        super().__init__(keyitem_id, data_row['readable_name'], 0,
                         [], 1, tier=None, valid=data_row['valid'])
        self.writeable_name = data_row['writeable_name']
        self.text_location = data_row['text_location']
        self.required_by_placement = []

    #key_items is an array, even if it's only one item
    def add_required_items(self, key_items):
        self.required_by_placement.extend(key_items)

    @property
    def patch_id(self):
        return self.reward_id

    @property
    def reward_name(self):
        return self.collectible_name

    @property
    def type_str(self):
        return "KeyItem"

    @property
    def shop_name(self):
        return self.collectible_name
    

class ArchItem(Collectible):
    name = "Arch Item"
    reward_type = '70'
    def __init__(self, arch_item_name, arch_player, arch_item_progression):
        super().__init__("DF", 
                         arch_item_name, 
                         0,
                         [], 
                         1, 
                         tier=0, 
                         valid=True)
        self.writeable_name = "Arch Item"
        self.text_location = "Arch Item"
        self.arch_item_name = arch_item_name
        self.arch_player = arch_player
        self.arch_item_progression = arch_item_progression
        self.required_by_placement = []

    #key_items is an array, even if it's only one item
    def add_required_items(self, key_items):
        self.required_by_placement.extend(key_items)

    @property
    def patch_id(self):
        return self.reward_id

    @property
    def reward_name(self):
        return self.collectible_name

    @property
    def type_str(self):
        return "Arch Item"

    @property
    def shop_name(self):
        return self.collectible_name

class CollectibleManager():
    def __init__(self, data_manager, collectible_config=None):
        self.collectible_config = collectible_config
        
        logging.debug("Collectible Manager enter Init")
        logging.debug("CM: Initializing Items")
        items = [Item(k, v) for k, v in data_manager.files['items'].items()]
        logging.debug("CM: Items Initialized")
        logging.debug("CM: Initializing Magics")
        magics = [Magic(k, v ,self.collectible_config) for k, v in data_manager.files['magics'].items()]
        logging.debug("CM: Magics Initialized")
        logging.debug("CM: Initializing Crystals")
        crystals = [Crystal(k, v) for k, v in data_manager.files['crystals'].items()]
        logging.debug("CM: Crystals Initialized")
        logging.debug("CM: Initializing Abilities")
        abilities = [Ability(k, v, self.collectible_config) for k, v in data_manager.files['abilities'].items()]
        logging.debug("CM: Abilities Initialized")
        logging.debug("CM: Initializing Gil")
        gil = [Gil(k, v) for k, v in data_manager.files['gil'].items()]
        logging.debug("CM: Gil Initialized")
        logging.debug("CM: Initializing Key Items")
        key_items = [KeyItem(k, v) for k, v in data_manager.files['key_items'].items()]
        logging.debug("CM: Key Items Initialized")
        logging.debug("CM: Initializing Internal Properties")
        self.collectibles = items + magics + crystals + abilities + gil + key_items
        self.collectibles = [x for x in self.collectibles if x.valid]
        self.placement_history = {}
        self.placement_rewards = {}
        self.placed_gil_rewards = []
        logging.debug("CM: Internal Properties Initialized")
        logging.debug("Collectible Manager exit Init")

    def get_by_name(self, name):
        if name == "New":
            return None
        for i in self.collectibles:
            if name == i.reward_name:
                return i
        # print("DID NOT RETURN A COLLECTIBLE: name: "+str(name))
        return None

    def get_by_id_and_type(self, reward_id, reward_type):
        for i in self.collectibles:
            if i.reward_id == reward_id and i.reward_type == reward_type and i.valid:
                return i
        return None

    def get_by_arch(self, c_name, c_id):
        for i in self.collectibles:
            if c_name == "Gil":
                if i.name == c_name and i.gil_id == c_id and i.valid:
                    return i
            else:
                if i.name == c_name and i.reward_id == c_id and i.valid:
                    return i
        return None


    def get_all_of_type(self, t):
        if type(t) is list or type(t) is tuple:
            return [x for x in self.collectibles if type(x) in t]
        return [x for x in self.collectibles if type(x) is t]

    def reset_all_of_type(self, t):
        for i in self.collectibles:
            if type(i) == t:
                self.remove_from_placement_history(i)
                if t == KeyItem:
                    i.required_by_placement = []

    def reset_all_types(self):
        for i in self.collectibles:
            self.remove_from_placement_history(i)
            i.required_by_placement = []

    def create_arch_item(self, arch_item_name, arch_player, arch_item_progression):
        return ArchItem(arch_item_name, arch_player, arch_item_progression)


    def get_all_of_type_respect_counts(self, t):
        if type(t) is list or type(t) is tuple:
            return [x for x in self.collectibles if type(x) in t and (x not in self.placement_history.keys() or
                                                                      x.max_count is None or
                                                                      x.max_count < self.placement_history[x])]

        return [x for x in self.collectibles if type(x) is t and (x not in self.placement_history.keys() or
                                                                  x.max_count is None or
                                                                  x.max_count < self.placement_history[x])]

    def get_random_collectible(self, random_engine, respect_weight=False, 
                               reward_loc_tier=None, monitor_counts=False, 
                               of_type=None, gil_allowed=False, disable_zerozero=False, 
                               next_reward=None, tiering_config=False,
                               tiering_percentage=90, tiering_threshold=2, force_tier=None):
        
        
        
        ## first define the function that will take the original working list
        #  and return a working list that adheres to the nearby tiers
        def filter_working_list(working_list, reward_loc_tier, tiering_percentage, tiering_threshold):
            
            # TIERING
            # After applying all the above, enforce tiering if applicable.
            debug_flag = False
            og_reward_loc_tier = 100
            if tiering_config:
                # Now we empty working_list, and iterate over minimum floors for collectible tiers until the list is populated
                # With at least one item
                
                # Example:
                # Trying to place on a tier 4 location. 
                # 90% chance to place collectible Tier _4_ through 4, 10% chance to place collectible Tier _4_ through 6 (4+2)
                # If nothing is placed, change _4_ to _3_, etc..
                # continue until not empty 
    
                if reward_loc_tier is not None:
                    if force_tier is not None:
                        reward_loc_tier = force_tier
                    RARE_TIER_PERCENTAGE = 99    # Rare percent chance of pulling from 7+ tiers only. B O N U S
                                                    # This is disabled for now
                                                    
                    # breakpoint()
                    # tiering_percentage = 90      # Percent chance each draw will strictly adhere to tier. 
                    # tiering_threshold = 2        # If tier percentage not applied (i.e, 10% if above is 90%) 
                                                 #   then include the collectible if it is in the tier threshold range 
                                                 #   e.g., location tier 4, collectible tier 6, tier threshold 2
                                                 #   if it passes the 90% test (and is one of the 10%), then 
                                                 #   it will be included because the range becomes 4 <-> 6 
                                                                                              
                    working_list_copy = working_list[:]
                    working_list = []        
                    reward_loc_tier = int(reward_loc_tier)
                    og_reward_loc_tier = reward_loc_tier
                    if 'shop' in str(type(next_reward)):
                        minimum_tier = max(reward_loc_tier - 2, 1) #starts at a range of y-2 to y (so, tier 4 location will grab from pool of tier 2s, 3s and 4s)
                    else:
                        minimum_tier = max(reward_loc_tier - 1, 1) #starts at a range of y-1 to y (so, tier 4 location will grab from pool of tier 3s and 4s)
                    
                    # print("Reward loc tier: %s" % (reward_loc_tier))
                    # Apply a penalty to reward_loc_tier IF the capacity has been met. Only valid for shops for now. 
                    current_volume_ratio = 0
                    if 'shop' in str(type(next_reward)):
                        current_volume_ratio = math.trunc(next_reward.current_volume / next_reward.capacity)
                        # Current volume ratio is saying that if the volume divided by capacity starts
                        # To get really high, start penalizing the tiers
                        # The math here will be to take the ratio, round it DOWN, then apply that number
                        # E.g., if the current volume is 16, and the capacity is 7, 16/7 results in 2.28,
                        #   which rounds to 2, then a penalty of 2 is placed 
                    
                        reward_loc_tier = max(int(reward_loc_tier - current_volume_ratio),1)
    #                    if "Mirage" in next_reward.readable_name:
    #                        print(next_reward.readable_name, reward_loc_tier, current_volume_ratio)
                    
                    try:
                       if debug_flag:
                           print("---------------------------------")
                       while working_list == [] and minimum_tier > -1:
                            for i in working_list_copy:
                                percent_flag = random_engine.randint(1,100) > tiering_percentage
    #                            rare_percent_flag = random_engine.randint(1,100) > RARE_TIER_PERCENTAGE
    #                            if rare_percent_flag:
    #                                if i.tier >= 7:
    #                                    working_list.append(i)
                                # If less than, then apply normal case
                                if not percent_flag:
                                    if i.tier <= reward_loc_tier and i.tier >= minimum_tier:
                                        working_list.append(i)
                                        if debug_flag:
                                            print("Added collectible: %s %s reward_loc_tier %s"% (i.collectible_name,i.tier,reward_loc_tier))                  
                                    else:
                                        if debug_flag:
                                            print("Not added collectible: %s %s reward_loc_tier %s"% (i.collectible_name,i.tier,reward_loc_tier))                  
                                # If greater than or equal to percentage, add the collectible if it is reward_loc_tier + threshold
                                # Use the og_reward_loc_tier from before if it was a shop
                                else:
                                    if i.tier <= (og_reward_loc_tier + tiering_threshold) and i.tier >= minimum_tier:
                                        working_list.append(i)
                                        if debug_flag:
                                            print("Added collectible (bonus): %s %s reward_loc_tier %s"% (i.collectible_name,i.tier,reward_loc_tier))
                                    else:
                                        if debug_flag:
                                            print("Not added collectible (bonus): %s %s reward_loc_tier %s"% (i.collectible_name,i.tier,reward_loc_tier))
                            # decrease minimum_tier for next time, if working_list is still empty
                            minimum_tier -= 1
                    except Exception as e:
                        print("EXCEPTION %s" % (e))
    
                
            #ending up with empty lists and failures too often, need a fallback incase
            #we don't end up with any values. We'll get a list of any of the appropriate type,
            #but no single placement items
            empty_trigger = False
            if len(working_list) == 0:
                # print("Working list was zero, redoing without logic for type %s..." % (of_type))
                if of_type is not None:
                    working_list = [x for x in self.get_all_of_type(of_type) if x.max_count != 1 and x.valid]
                    if working_list == []:
                        working_list = [x for x in self.get_all_of_type(of_type) if x.valid]
                else:
                    working_list = [x for x in self.collectibles if x.max_count != 1 and x.valid]
    
            if disable_zerozero:
                working_list = [x for x in working_list if x.patch_id != '00'] #disable any id of 00, because this ends shops
            return working_list








        # Create the original working_list, which does NOT yet filter on tiers
        # it is only checking for valid entries and for placement history 


        if type(of_type) is str: # this is a literal string definition of a type, so let's cast it first
            if of_type in type_dict.keys():
                of_type = type_dict[of_type]
            else:
                raise(KeyError) #not sure what to do with a passed in type we don't know about
                
        
        if of_type is not None:
            working_list = [x for x in self.get_all_of_type(of_type) if x.valid] #this will be a shop or a forced type item
        else:
            # print("Enforce")
            working_list = [x for x in self.collectibles if x.valid and type(x) != KeyItem] #this will be a non shop


        
        if not gil_allowed:
            working_list = [x for x in working_list if type(x) is not Gil]
            
        working_list_valid_start = working_list[:]

        if monitor_counts is True:
            if self.collectible_config['place_all_rewards']:
                # first attempt to place things that are not placed yet
                working_list_og = working_list[:]
                working_list = [y for y in [x for x in working_list if
                                                x not in self.placement_history.keys()] if y.valid]
                if len(working_list) < 20 and 'shop' not in str(type(next_reward)):
                    # v1.2 change - instead of getting down to zero placement on 
                    # "place_all_rewards", allow a threshold of 20 collectibles
                    # to not be placed
                    
                    working_list = working_list_og[:]
                
                
                
                
                
            # RESUME NORMAL 
            working_list = [y for y in [x for x in working_list if
                                       (x not in self.placement_history.keys() or
                                        x.max_count is None or
                                        x.max_count > self.placement_history[x])]
                            if y.valid]
            

        # try:
        #     logging.debug("Reward: %s (%s) Pre-tier filter working_list len: %s" % (next_reward.description, next_reward.idx, len(working_list)))
        # except:
        #     pass
        

        final_working_list = filter_working_list(working_list, reward_loc_tier, tiering_percentage, tiering_threshold)
        
        # step 2 - if final_working_list is empty, then try again
        # try again without doing "x not in self.placement_history.keys()" from above
        # but do try to adhere to placement_history counts
        
        if not final_working_list:        
            

            working_list = working_list_valid_start[:]
            
            working_list = [y for y in [x for x in working_list if
                                       (x not in self.placement_history.keys() or
                                        x.max_count is None or
                                        x.max_count > self.placement_history[x])]
                            if y.valid]
        
            # try again
            try:
                logging.debug("Reward: %s Step 2 (allow any prior placement) filter working_list len: %s" % (next_reward.description, len(working_list)))
            except:
                pass
            
            final_working_list = filter_working_list(working_list, reward_loc_tier, tiering_percentage, tiering_threshold)
        
        
        # step 3 - if empty again, allow all        
        if not final_working_list:        
            working_list = working_list_valid_start[:]
            working_list = [y for y in [x for x in working_list] if y.valid]

            try:       
                logging.debug("Reward: %s Step 2 (allow all) filter working_list len: %s" % (next_reward.description, len(working_list)))
            except:
                pass
            # try again
            final_working_list = filter_working_list(working_list, reward_loc_tier, tiering_percentage, tiering_threshold)
        
        
        
        
        
        
        
        

        choice = random_engine.choice(final_working_list)

        try:                
            logging.debug("Reward: %s choice: %s" % (next_reward.description, choice.readable_name))
        except:
            pass        

        # if respect_weight is False:
        #     choice = random_engine.choice(working_list)
        # else:
        #     # Legit I don't think this is doing anything. While debugging, [y.place_weight for y in working_list] always produces an array of 1s, from the hardcode weight=1 from Collectible...
        #     # What was the point...?
            
        #     choice_flag = False
        #     num_flag = 0
        #     while choice_flag == False:
        #         choice = random_engine.choices(working_list, [y.place_weight for y in working_list])[0]
        #         if type(choice) == Gil and next_reward.force_type is not None:
        #             num_flag += 1
        #             if num_flag > 10000:
        #                 print("Edge case for Gil reward at non-gil location triggered.")
        #                 choice_flag = True # if for whatever reason this happens, just accept the gil reward on an event and move on 
        #         else:
        #             choice_flag = True

        if monitor_counts is True:
            self.add_to_placement_history(choice,next_reward)


        if choice is None:
            print(working_list)
     
#        try:
#            if choice.tier > og_reward_loc_tier + 5:
#                breakpoint()
#        except:
#            pass

        return choice

    def get_min_value_collectible(self, random_engine):
        return random_engine.choice([x for x in self.get_all_of_type(Item)
                                     if  x.reward_value == 1
                                     and x.max_count is None
                                     and x.valid])

    def get_of_value_or_lower(self, random_engine, value):
        val_list = [x for x in self.collectibles if x.reward_value == value
                    and (x not in self.placement_history or
                         self.placement_history[x] < x.max_count)
                    and x.valid and type(x) != KeyItem]
        if len(val_list) == 0:
            val_list = [x for x in self.collectibles if x.reward_value < value
                        and self.placement_history[x] < x.max_count
                        and x.valid and type(x) != KeyItem]
        if len(val_list) == 0:
            return None #some you can place forever, so this should never happen

        return random_engine.choice(val_list)
        
    
    def add_to_placement_history(self, collectible, reward):
#        if "Item" in str(type(collectible)):
#            print("ADDING: %s" % (collectible.collectible_name))
        if reward != "No":
            collectible.placed_reward = reward
        else:
            pass
            collectible.placed_reward = "Manually blocked"
            # print("NO condition: %s" % (collectible.collectible_name))
        if collectible in self.placement_history.keys():
            self.placement_history[collectible] = self.placement_history[collectible] + 1
        else:
            self.placement_history[collectible] = 1

    def remove_from_placement_history(self, collectible):
        if collectible in self.placement_history.keys():
            del(self.placement_history[collectible])
            
    def reset_placement_history(self):
        self.placement_history = {}

    def update_placement_rewards(self, collectible, reward):
        try:
            reward_name = reward.description 
        except:
            try:
                reward_name = reward.readable_name 
            except Exception as e:
                reward_name =  "Error"
                print(e)
                
        if str(type(collectible)) == "<class 'collectible.Magic'>":
            c_name = "%s (%s)" % (collectible.collectible_name, collectible.type)
        elif str(type(collectible)) == "<class 'collectible.Ability'>":
            c_name = "%s (%s)" % (collectible.collectible_name, "Ability")
        elif str(type(collectible)) == "<class 'collectible.Crystal'>":
            c_name = "%s (%s)" % (collectible.collectible_name, "Crystal")
        else:
            c_name = collectible.collectible_name

        if collectible.collectible_name not in self.placement_rewards.keys():
            self.placement_rewards[c_name] = reward_name
        else:
            self.placement_rewards[c_name] = self.placement_rewards[collectible.collectible_name] +", " + reward_name
    def remove_from_placement_rewards(self, collectible_replaced, reward):
        try:
            if str(type(collectible_replaced)) == "<class 'collectible.Magic'>":
                c_name = "%s (%s)" % (collectible_replaced.reward_name, collectible_replaced.type)
            elif str(type(collectible_replaced)) == "<class 'collectible.Ability'>":
                c_name = "%s (%s)" % (collectible_replaced.reward_name, "Ability")
            elif str(type(collectible_replaced)) == "<class 'collectible.Crystal'>":
                c_name = "%s (%s)" % (collectible_replaced.reward_name, "Crystal")
            else:
                c_name = collectible_replaced.reward_name
            placed_collectibles = self.placement_rewards[c_name]
            placed_collectibles = placed_collectibles.replace(reward.description, "")
            placed_collectibles = placed_collectibles.replace(", ,", ",")
            if ", " in placed_collectibles[0:3]:
                placed_collectibles = placed_collectibles[2:]
            self.placement_rewards[c_name] = placed_collectibles
        except:
            pass



            
    def get_spoiler(self):
        output = "-----COLLECTIBLES------\n"
        for i in self.collectibles:
            if str(type(i)) == "<class 'collectible.Magic'>":
                c_name = "%s (%s)" % (i.collectible_name, i.type)
                if c_name not in self.placement_rewards.keys():
                    self.placement_rewards[c_name] = "Not placed"
            elif str(type(i)) == "<class 'collectible.Ability'>":
                c_name = "%s (%s)" % (i.collectible_name, "Ability")
                if c_name not in self.placement_rewards.keys():
                    self.placement_rewards[c_name] = "Not placed"
            elif str(type(i)) == "<class 'collectible.Crystal'>":
                c_name = "%s (%s)" % (i.collectible_name, "Crystal")
                if c_name not in self.placement_rewards.keys():
                    self.placement_rewards[c_name] = "Not placed"
            else:
                if i.collectible_name not in self.placement_rewards.keys():
                    self.placement_rewards[i.collectible_name] = "Not placed"
                
        placement_rewards2 = OrderedDict(sorted(self.placement_rewards.items(), key=lambda t: t[0]))
        for collectible, reward in placement_rewards2.items():
            reward_name = reward
            output = output + '{:30}'.format(collectible+ ":") + '{:30}'.format(reward_name) + "\n"
        output = output + "-----*********-----\n\n\n"
        return output
        
type_dict = {}
type_dict['Item'] = Item
type_dict['Magic'] = Magic
type_dict['Crystal'] = Crystal
type_dict['Ability'] = Ability
type_dict['Gil'] = Gil
type_dict['KeyItem'] = KeyItem