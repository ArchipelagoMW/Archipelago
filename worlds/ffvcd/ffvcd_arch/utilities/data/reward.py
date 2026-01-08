# -*- coding: utf-8 -*-

class Reward:
    def __init__(self, index, collectible_manager, data_manager):
        self.idx = index
        self.generate_from_data(data_manager.files['rewards'])
        '''
        self.address (address of two byte value, id definition)
        self.type (crystal, esper, magic, etc)
        self.original_reward (Knight, Potion, Crbnkl, etc)
        self.area (Wind Shrine, Karnak, etc)
        self.description (Wind Crystal, Beginner's House Chest, etc)
        self.reward_style (event, chest, key)
        self.force_type (Item, Gil, etc.)
        self.required_key_items (Sandworm Bait, Adamantite, etc.)
        self.exdeath_address (Address only relevant to the key item rewards, that tells the special exdeath rewards where to write)
        '''
        if self.required_key_items:
            self.required_key_items = [x.replace('"', '').replace('“', '').replace('”', '').strip() for x in \
                                        self.required_key_items.strip('][').split(',')]
        if self.required_key_items_lock1:
            self.required_key_items_lock1 = [x.replace('"', '').replace('“', '').replace('”', '').strip() for x in \
                                        self.required_key_items_lock1.strip('][').split(',')]
        if self.required_key_items_lock2:
            self.required_key_items_lock2 = [x.replace('"', '').replace('“', '').replace('”', '').strip() for x in \
                                        self.required_key_items_lock2.strip('][').split(',')]
        try:
            self.hint_tags = [x.replace('"', '').replace('“', '').replace('”', '').strip() for x in \
                              self.hint_tags.strip('][').split(',')]
        except:
            self.hint_tags = ''

        self.collectible = collectible_manager.get_by_name(self.original_reward)
        self.mib_type = None #keep a byte for the monster in a box type, override the type in the asar_output if exists
        self.mib_placed_key_item = False # this flag is used rarely for MIB to change the asar_output
        self.reward_arch_mib_flag = False
        self.randomized = False
        self.max_world_requirements_flag = False # used for progressive bosses setting


    @property
    def asar_output(self):
        
        if hasattr(self, 'reward_arch_mib_flag') and hasattr(self, 'mib_chest_id'):
            return f"org ${self.address} \ndb ${self.mib_chest_id}, ${self.collectible.patch_id}"
        if self.mib_type is None:
            try:
                return f"org ${self.address} \ndb ${self.collectible.reward_type}, ${self.collectible.patch_id}"
            except:
                pass
        else:
            return f"org ${self.address} \ndb ${self.mib_type}, ${self.collectible.patch_id}"
    
    @property
    def short_output(self):
        if self.collectible is None:
            return ""
        if str(type(self.collectible)) == "<class 'collectible.KeyItem'>":
            return '{:30}'.format("%s " % (self.description)) + '{:30}'.format("%s" % (self.collectible.reward_name))
        if str(type(self.collectible)) == "<class 'collectible.Magic'>":
            return '{:50}'.format("%s %s" % (self.description, self.original_reward)) + '{:50}'.format("%s (%s)" % (self.collectible.reward_name, self.collectible.type))
        if str(type(self.collectible)) == "<class 'collectible.Ability'>":
            return '{:50}'.format("%s %s" % (self.description, self.original_reward)) + '{:50}'.format("%s (%s)" % (self.collectible.reward_name, "Ability"))
        if str(type(self.collectible)) == "<class 'collectible.Crystal'>":
            return '{:50}'.format("%s %s" % (self.description, self.original_reward)) + '{:50}'.format("%s (%s)" % (self.collectible.reward_name, "Crystal"))
    

        if self.mib_type is None:
            return  '{:50}'.format("%s %s" % (self.description, self.original_reward)) + '{:50}'.format("%s" % (self.collectible.reward_name))
        else:
            return '{:50}'.format("%s %s" % (self.description, self.original_reward)) + '{:50}'.format("%s (monster-in-a-box)" % (self.collectible.reward_name))

    def generate_from_data(self, data):
        
        if self.idx in data.keys():
            s = data[self.idx]
            for k, v in s.items():
                setattr(self,k,v)
        else:
            print("No match on index found for Reward class %s" % self.idx)


    def set_collectible(self, collectible, type_override=None):
        self.randomized = True
        self.collectible = collectible

class RewardManager:
    def __init__(self, collectible_manager, data_manager):
        self.rewards = [Reward(k, collectible_manager, data_manager) for k in data_manager.files['rewards'].keys()]

    def get_random_reward(self, random_engine, area=None):
        if area is None:
            return random_engine.choice(self.rewards)

    def get_reward_by_address(self, address):
        for i in self.rewards:
            if i.address == address:
                return i
        return None

    def get_rewards_by_style(self, style):
        return [x for x in self.rewards if x.reward_style == style]

    def reset_rewards_by_style(self, style):
        for i in self.get_rewards_by_style(style):
            i.randomized = False
            i.collectible = None

    def get_patch(self):
        output = "\n;================="
        output = output + "\n;Chests and Events"
        output = output + "\n;=================\n"
        for i in self.rewards:
            output = output + i.asar_output + "\n"
        
        return output

    def get_spoiler(self, world_lock, free_tablets, trapped_chests):
        
        output = "-----BOSS CHECKS------\n"
        keys = [x for x in self.rewards if x.reward_style == "key"]
        keys = sorted(keys, key = lambda i: i.description)
        for i in keys:
            output = output + "{:<40}".format("{:<40}".format(i.description)+"{:<40}".format(i.collectible.reward_name))+"\n"

        if trapped_chests:
            output += "\n-----TRAPPED CHESTS/MIB------\n"
            keys = [x for x in self.rewards]
            keys = sorted(keys, key = lambda i: i.description)
            for i in keys:
                if i.reward_arch_mib_flag:
                    output = output + "{:<40}".format("{:<60}".format("%s (%s)" % (i.description, i.original_reward))+"{:<40}".format("%s (MIB Rank %s)" % (i.collectible.reward_name, i.reward_arch_region_rank)))+"\n"


        # output = output + "-----*********-----\n\n\n"
        
        # output = output + "-----CHESTS AND EVENTS-----\n"
        # for i in [x for x in self.rewards if str(type(x.collectible)) != "<class 'collectible.KeyItem'>"]:
        #     output = output + i.short_output + "\n"
        # output = output + "-----****************-----\n\n"


        output = output + "\n\n"
        return output