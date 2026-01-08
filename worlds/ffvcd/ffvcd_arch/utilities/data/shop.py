# -*- coding: utf-8 -*-
from reward import *

NUM_SHOPS = 64

class Shop(object):
    def __init__(self, index, collectible_manager, data_manager):
        self.idx = index
        self.generate_from_data(data_manager.files['shops'])
        
        # The below capacity penalizes the capacity of high value shops more than others 
        self.capacity = int(max((int(self.num_items) * int(self.tier) * .5) - round(int(self.tier) ** 1.5),1))
        self.current_volume = 0
        
        '''
        self.address
        self.shop_type
        self.slot1 -> self.slot8
        self.readable_name
        self.valid
        self.num_items
        '''
        
        if not self.valid:
            self.valid = self.valid  == 'TRUE'
        else:
           self.valid == True 


        self.num_items = int(self.num_items)
        #shops can only sell items or magic, by default
        if self.shop_type == '00':
            collectible_type = '20' #magic
        else:
            collectible_type = '40' #items
        self.original_contents = []
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot1 ,collectible_type))
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot2 ,collectible_type))
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot3 ,collectible_type))
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot4 ,collectible_type))
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot5 ,collectible_type))
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot6 ,collectible_type))
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot7 ,collectible_type))
        self.original_contents.append(collectible_manager.get_by_id_and_type(self.slot8 ,collectible_type))
        self.contents = self.original_contents

    @property
    def asar_output(self):
        output = "org $" + self.address + "\n"
        output = output + "db $" + self.shop_type
        for i in self.contents:
            if i is None:
                output = output + ", $00"
            else:
                if str(type(i)) == "<class 'collectible.Crystal'>":
                    output = output + ", $" + str(i.shop_id)
                else:
                    output = output + ", $" + str(i.reward_id) #Todo: this will need to change when/if shops can be progressive

        return output

    def sort_contents(self):
        contents = [i for i in self.contents if i is not None]
        none_len = len(self.contents) - len(contents)
        self.contents = sorted(contents, key=lambda x: x.reward_id) 
#        if self.shop_type == '00':
#            self.contents = sorted(contents, key=lambda x: x.magic_id) 
#        elif self.shop_type == '01':
#            self.contents = sorted(contents, key=lambda x: x.reward_id) 
#        elif self.shop_type == '07':
#            try:
#                self.contents = sorted(contents, key=lambda x: x.ability_id)
#            except:
#                breakpoint()
##        elif self.shop_type == '07':
##            self.contents = sorted(contents, key=lambda x: x.ability_id)
#            
#        else:
#            breakpoint()
#            pass
        for _ in range(none_len):
            self.contents.append(None)


    @property
    def short_output(self):
        #these two lists format the None collectibles into strings for easy reading

        readable_original = [x.shop_name if x is not None else "None" for x in self.original_contents]
        readable_current = [x.shop_name if x is not None else "None" for x in self.contents]
        readable_current_tier = ["T"+str(x.tier) if x is not None else "  " for x in self.contents]
        shops_dict = {'00':'Magic','01':'Item','07':'Ability/Crystal'}
        output = "Shop: " + self.readable_name + "\n"
        try:
            output = output + "Shop Type: " + shops_dict[self.shop_type] + "\n"
        except:
            pass
        output = output + '{:30}'.format("Shop Item 1: " + readable_original[0]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[0]) + "\n"
        output = output + '{:30}'.format("Shop Item 2: " + readable_original[1]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[1]) + "\n"
        output = output + '{:30}'.format("Shop Item 3: " + readable_original[2]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[2]) + "\n"
        output = output + '{:30}'.format("Shop Item 4: " + readable_original[3]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[3]) + "\n"
        output = output + '{:30}'.format("Shop Item 5: " + readable_original[4]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[4]) + "\n"
        output = output + '{:30}'.format("Shop Item 6: " + readable_original[5]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[5]) + "\n"
        output = output + '{:30}'.format("Shop Item 7: " + readable_original[6]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[6]) + "\n"
        output = output + '{:30}'.format("Shop Item 8: " + readable_original[7]) + '{:5}'.format(" -> ") + '{:30}'.format(readable_current[7]) + "\n"
        return output

    def generate_from_data(self, data):
        
        if self.idx in data.keys():
            s = data[self.idx]
            for k, v in s.items():
                setattr(self,k,v)
        else:
            print("No match on index found for Shop class %s" % self.idx)

    def new_contents(self, contents):
        self.contents = contents
    
    def update_volume(self, value):
        self.current_volume += value

class ShopManager(object):
    def __init__(self, collectible_manager, data_manager):
        self.shops = [Shop(x, collectible_manager, data_manager) for x in range(1, NUM_SHOPS+1)]

    def get_patch(self):
        output = ";====="
        output = output + "\n;shops"
        output = output + "\n;=====\n"
        for i in [x for x in self.shops if x.valid]:
            output = output + i.asar_output + "\n"
        output = output + "\n"

        return output

    def get_spoiler(self):
        output = "-----SHOPS-----\n"
        for i in [x for x in self.shops if x.valid]:
            output = output + i.short_output + "\n"
        output = output + "-----*****-----\n"

        return output
