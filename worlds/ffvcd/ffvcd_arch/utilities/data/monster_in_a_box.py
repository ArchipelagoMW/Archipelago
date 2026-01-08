# -*- coding: utf-8 -*-


class Monster_In_A_Box:
    def __init__(self, index, data_frame):
        self.idx = index
        self.generate_from_data(data_frame)
        '''
        self.readable_name (name of the encounter of this box (as of 4/2/2019 this is empty, need to work on this - C))
        self.area (Wind Shrine, Karnak, etc)
        self.monster_chest_id (3 byte address for the reward type)
        self.monster_chest_data (byte that represents the monster in a box enemy to choose)
        self.reward_id (3 byte address for the reward from the monster-in-a-box)
        self.reward_data (byte that represents the reward for beating this monster-in-a-box)
        '''
        self.processed = False #flag used to track if this monster has been placed

    def generate_from_data(self, data):
        if self.idx in data.keys():
            s = data[self.idx]
            for k, v in s.items():
                setattr(self,k,v)
        else:
            print("No match on index found for MIB %s" % self.idx)

class MonsterInABoxManager:
    def __init__(self, data_manager, random=None, key_items_in_mib=False):
        self.monsters_in_boxes = [Monster_In_A_Box(x, data_manager.files['monsters_in_boxes']) for x in data_manager.files['monsters_in_boxes'].keys()]
        self.random = random
        self.key_items_in_mib = key_items_in_mib

    def get_mib_for_area(self, area):
        #print("getting mib for area: " + area.area_name)
        working_list = [x for x in self.monsters_in_boxes if x.area == area.area_name and x.processed == False]
    
        # if working_list:
        #     breakpoint()
        #print("mib list length: " + str(len(working_list)))
        if len(working_list) > 0:
            return self.random.choice(working_list)
        else:
            return None

    def get_mib_by_address(self, address):
        for i in self.monsters_in_boxes:
            if i.monster_chest_id == address:
                return i