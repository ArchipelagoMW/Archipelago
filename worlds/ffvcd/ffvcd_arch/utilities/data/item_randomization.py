# -*- coding: utf-8 -*-
import random
from abc import ABC, abstractmethod
from collections import OrderedDict
from data_manager import DataManager
import math
import logging

import sys, os
new_path = os.path.abspath(os.path.join(os.pardir))
if new_path not in sys.path:
    sys.path.append(new_path)
    sys.path.append(os.path.join(new_path,'text_parser'))
new_path = os.path.abspath(os.path.join(os.pardir,os.pardir))
if new_path not in sys.path:
    sys.path.append(new_path)
    
import text_parser2 as tp

logging.basicConfig(level=logging.ERROR, format="%(asctime)-15s %(message)s")



'''
byte_map:
1 ?
2 Attack type $AT - see common lists
3 Misc. / Weapon type
4 Element / stats up
5 Misc. properties
6 Weapon specials
7 Used as item
8 Attack power
9 Attack formula
A Parameter #1
B Parameter #2
C Parameter #3
'''



boost_dict = {"wind":'40',
              "earth":'20',
              "holy":'10',
              "poison":'08',
              "lightning":'04',
              "ice":'02',
              "fire":'01'
              }


stat_dict = {"strength":'40',
              "speed":'20',
              "vitality":'10',
              "magic power":'08'
              }

stat_dict2 = {'Strong':['strength'],
                'Agile':['speed'],
                'Tank':['vitality'],
                'Witch':['magic power'],
                'Swift':['strength', 'speed'],
                'Tough':['strength', 'vitality'],
                'Raw':['strength', 'magic power'],
                'Fleet':['speed', 'vitality'],
                'Skill':['speed', 'magic power'],
                'Heart':['vitality', 'magic power'],
                'Vigor':['strength', 'speed', 'vitality'],
                'Adept':['strength', 'speed', 'magic power'],
                'Fierce':['strength', 'vitality', 'magic power'],
                'Sorcer':['speed', 'vitality', 'magic power'],
                'Omni':['strength', 'speed', 'vitality', 'magic power']
                }


stat_boost_power_dict = {
        '00':"+1",
        '01':"+2",
        '02':"+3",
        '07':"+5"
        }

'''
<Swrd>
<Whit>
<Blak>
<Dimn>
<Knif>
<Sper>
<Axe>
<Katn>
<Rod>
<Staf>
<Bow>
<Harp>
<Whip>
<Bell>
<Shld>
<Helm>
<Armr>
<Ring>
<Misc>



'''
ability_dict = {'Guard':'06',
                'BuildUp':'08',
                'Mantra':'09',
                'Escape':'0A',
                'Steal':'0B',
                'Mug':'0C',
                'Jump':'0D',
                'DrgnSwd':'0E',
                'Image':'10',
                'GilToss':'13',
                'Slash':'14',
                'Animals':'15',
                'X-Fight':'17',
                'Conjure':'18',
                'Terrain':'23',
                'Analyze':'1A',
                'Dance':'2A',
                'Flirt':'29',
                'Tame':'1B'                
                }

ability_dict_power = {'Guard':12,
                'BuildUp':25,
                'Mantra':19,
                'Escape':7,
                'Steal':23,
                'Mug':55,
                'Jump':43,
                'DrgnSwd':66,
                'Image':34,
                'GilToss':92,
                'Slash':87,
                'Animals':37,
                'X-Fight':105,
                'Conjure':77,
                'Terrain':9,
                'Analyze':7,
                'Dance':49,
                'Flirt':13,
                'Tame':36                
                }

enemy_type_dict = {'Zomb':7,
                   'Toad':6,
                   'Beast':5,
                   'Avis':4,
                   'Drgn':3,
                   'Heavy':2,
                   'Desrt':1,
                   'Human':0,
                   'Omni':9}

weapon_killer = [{'bow':['Toad','Zomb','Desrt','Beast','Drgn','Human','Avis','Heavy','Omni']},
                        {'spear':['Toad','Human','Avis','Desrt','Beast','Zomb','Drgn','Heavy','Omni']},
                        {'whip':['Toad','Human','Drgn','Avis','Desrt','Zomb','Beast','Heavy','Omni']},

                ]

weapon_type_dict = {'knife' :
                        {'bytemap':{'byte1' : '00',
                        'byte2' : '80',
                        'byte3' : '02',
                        'byte4' : '80',
                        'byte5' : '16',
                        'byte6' : '04',
                        'byte7' : '78',
                        'byte8' : '00',
                        'byte9' : '32',
                        'byte10' : '00',
                        'byte11' : '00',
                        'byte12' : '00'},
                        'clean_name':'Knife',
                        'text_icon':'<Knif>',
                        'bonus':3},
                    
                    'sword' : 
                         {'bytemap':{'byte1' : '00',
                        'byte2' : '80',
                        'byte3' : '04',
                        'byte4' : '80',
                        'byte5' : '55',
                        'byte6' : '04',
                        'byte7' : '78',
                        'byte8' : '00',
                        'byte9' : '31',
                        'byte10' : '00',
                        'byte11' : '00',
                        'byte12' : '00'},
                        'clean_name':'Sword',
                        'text_icon':'<Swrd>',
                        'bonus':4},
                         
                    'knightsword' : 
                         {'bytemap':{'byte1' : '00',
                        'byte2' : '80',
                        'byte3' : '05',
                        'byte4' : '80',
                        'byte5' : '55',
                        'byte6' : '04',
                        'byte7' : '78',
                        'byte8' : '00',
                        'byte9' : '31',
                        'byte10' : '00',
                        'byte11' : '00',
                        'byte12' : '00'},
                        'clean_name':'KSword',
                        'text_icon':'<Swrd>',
                        'bonus':11},
    
                    'spear' : 
                         {'bytemap':
                             {
                            'byte1' : '38',
                            'byte2' : '80',
                            'byte3' : '06',
                            'byte4' : 'c0',
                            'byte5' : '17',
                            'byte6' : '00',
                            'byte7' : '78',
                            'byte8' : '37',
                            'byte9' : '33',
                            'byte10' : '00',
                            'byte11' : '00',
                            'byte12' : '00'

                        },
                        'clean_name':'Spear',
                        'text_icon':'<Sper>',
                        'bonus':13},

                    'axe' : 
                         {'bytemap':
                             {
                                'byte1' : '00',
                                'byte2' : '80',
                                'byte3' : '07',
                                'byte4' : '80',
                                'byte5' : '59',
                                'byte6' : '00',
                                'byte7' : '78',
                                'byte8' : '17',
                                'byte9' : '34',
                                'byte10' : '50',
                                'byte11' : '00',
                                'byte12' : '00'

                        },
                        'clean_name':'Axe',
                        'text_icon':'<Axe>',
                        'bonus':17},

                    'katana' : 
                         {'bytemap':
                             {
                                'byte1' : '00',
                                'byte2' : '80',
                                'byte3' : '09',
                                'byte4' : '80',
                                'byte5' : '5a',
                                'byte6' : '00',
                                'byte7' : '78',
                                'byte8' : '2a',
                                'byte9' : '37',
                                'byte10' : '0c',
                                'byte11' : '00',
                                'byte12' : '00'

                        },
                        'clean_name':'Katana',
                        'text_icon':'<Katn>',
                        'bonus':9},

                    'rod' : 
                         {'bytemap':
                             {
                            'byte1' : '38',
                            'byte2' : '04',
                            'byte3' : '4a',
                            'byte4' : '88',
                            'byte5' : '23',
                            'byte6' : '00',
                            'byte7' : '78',
                            'byte8' : '08',
                            'byte9' : '3b',
                            'byte10' : '46',
                            'byte11' : '00',
                            'byte12' : '00'

                        },
                        'clean_name':'Rod',
                        'text_icon':'<Rod>',
                        'bonus':2},

                    'staff' : 
                         {'bytemap':
                             {
                            'byte1' : '38',
                            'byte2' : '80',
                            'byte3' : '4b',
                            'byte4' : '80',
                            'byte5' : '40',
                            'byte6' : '00',
                            'byte7' : '78',
                            'byte8' : '09',
                            'byte9' : '34',
                            'byte10' : '5f',
                            'byte11' : '00',
                            'byte12' : '00'

                        },
                        'clean_name':'Staff',
                        'text_icon':'<Staf>',
                        'bonus':0},

                    'bow' : 
                         {'bytemap':
                             {
                        'byte1' : '38',
                        'byte2' : '40',
                        'byte3' : '4d',
                        'byte4' : '80',
                        'byte5' : '9b',
                        'byte6' : '00',
                        'byte7' : '78',
                        'byte8' : '26',
                        'byte9' : '35',
                        'byte10' : '46',
                        'byte11' : '00',
                        'byte12' : '00'
                        },
                        'clean_name':'Bow',
                        'text_icon':'<Bow>',
                        'bonus':10},

                    'harp' : 
                         {'bytemap':
                             {
                            'byte1' : '78',
                            'byte2' : '20',
                            'byte3' : '4e',
                            'byte4' : '80',
                            'byte5' : '9b',
                            'byte6' : '08',
                            'byte7' : '78',
                            'byte8' : '0f',
                            'byte9' : '7f',
                            'byte10' : '00',
                            'byte11' : '64',
                            'byte12' : '74'

                        },
                        'clean_name':'Harp',
                        'text_icon':'<Harp>',
                        'bonus':2},

                    'whip' : 
                         {'bytemap':
                             {
                            'byte1' : '38',
                            'byte2' : '40',
                            'byte3' : '4f',
                            'byte4' : '80',
                            'byte5' : '23',
                            'byte6' : '08',
                            'byte7' : '78',
                            'byte8' : '1a',
                            'byte9' : '38',
                            'byte10' : '5a',
                            'byte11' : '32',
                            'byte12' : '7f'

                        },
                        'clean_name':'Whip',
                        'text_icon':'<Whip>',
                        'bonus':12},

                    'bell' : 
                         {'bytemap':
                             {
                            'byte1' : '38',
                            'byte2' : '20',
                            'byte3' : '50',
                            'byte4' : '80',
                            'byte5' : '23',
                            'byte6' : '00',
                            'byte7' : '78',
                            'byte8' : '18',
                            'byte9' : '39',
                            'byte10' : '00',
                            'byte11' : '00',
                            'byte12' : '00'

                        },
                        'clean_name':'Bell',
                        'text_icon':'<Bell>',
                        'bonus':5},

                    'flail' : 
                         {'bytemap':
                             {
                            'byte1' : '38',
                            'byte2' : '80',
                            'byte3' : '5e',
                            'byte4' : '80',
                            'byte5' : '23',
                            'byte6' : '00',
                            'byte7' : '78',
                            'byte8' : '23',
                            'byte9' : '38',
                            'byte10' : '5f',
                            'byte11' : '00',
                            'byte12' : '00'

                        },
                        'clean_name':'Flail',
                        'text_icon':'<Misc>',
                        'bonus':7},



                    }

boost_text_map = {"fire":         "Heat",
                 "ice":          "Cold",
                 "wind":         "Aerial",
                 "lightning":    "Zap",
                 "poison":       "Venom",
                 "earth":        "Terra",
                 "holy":         "Sacred" }



def b2i(byte):
    return int(byte,base=16)
def i2b(integer):
    return hex(integer).replace("0x","").upper()

def set_bit(byte,bit_to_set):
    ''' 
    returns a byte with specific int index bit set
    '''
    temp_bin = bin(int(byte,base=16)).replace("0b","").zfill(8)
    temp_bin = temp_bin[:bit_to_set] + "1" + temp_bin[bit_to_set+1:]
    return hex(int(temp_bin,base=2)).replace("0x","").zfill(2)

def rewrite_shop_costs(choice, original):
    output_str = '\n;Price: %s -> %s\norg $%s\ndb ' % (original.readable_name, choice.weapon_name_menu, original.shop_addr)
    new_shop_price = str(choice.shop_price)
    b1, b2 = int(new_shop_price[0:2]), new_shop_price[2:]
    
    b1 = i2b(b1)
    
    b2 = "0" + str(len(b2))

    output_str = output_str + "$%s, $%s\n" % (b2,b1)
    return output_str
    

class Weapon(ABC):
    type = 'weapon'
    
    def __init__(self, row,re):
        self.re = re
        self.data_dict = dict(row)
        self.weapon_type = self.data_dict['subtype']
        self.adjustments = {}
        self.bytemap = {}
        
        
    def set_replacement(self, choice):
        pass
        
        bytemap = ['byte1','byte2','byte3','byte4','byte5','byte6','byte7','byte8','byte9','byte10','byte11','byte12']
        for b in bytemap:
            self.bytemap[b] = str(choice[b]).zfill(2)

        self.text_textbox = choice['weapon_name_textbox']
        self.text_menu = choice['weapon_name_menu']
        self.weapon_power = choice['weapon_str']

        

    @property
    def data_string(self):
        return ''.join(self.bytemap.values())
    
    @property
    def data_string_asar(self):
        return 'db $' + ', $'.join(self.bytemap.values())
    
    @property
    def asar_output(self):
        output_str = ''
        tp.init_table("chest")
        output_str = output_str + ';%s %s -> %s (%s) - Power %s\n' % (self.data_dict['data_addr'],self.data_dict['readable_name'],self.text_textbox, self.text_menu, self.weapon_power)
        output_str = output_str + 'org $%s\n%s\n' % (self.data_dict['textbox_addr'], tp.run_encrypt_text_string(self.text_textbox,verbose=False,ff_fill=24))
        tp.init_table("shop")
        output_str = output_str + 'org $%s\n%s\n' % (self.data_dict['textmenu_addr'], tp.run_encrypt_text_string(self.text_menu,verbose=False,ff_fill=9))
        output_str = output_str + 'org $%s\n%s\n' % (self.data_dict['data_addr'], self.data_string_asar)
        return output_str
    
    @property
    def spoiler(self):
        output_str = ''
        output_str = output_str + '%s -> %s (Power: %s)\n' % ('{:20}'.format(self.data_dict['readable_name']),'{:20}'.format(self.text_textbox), self.weapon_power)
        return output_str


    
class WeaponManager(ABC):
    def __init__(self, data_manager, re=None, percent_randomization=100):
        global magic_dict
        magic_dict = data_manager.files['magic_item_randomization'].reset_index()[['magic_id','readable_name','tier']].set_index('magic_id').to_dict()
        self.df_weapon = data_manager.files['weapon_randomization']
        self.df_custom_weapons = data_manager.files['custom_weapons']
        self.history = {}
        self.percent_randomization = percent_randomization
        self.banned_items = []
        if re == None:
            self.re = random.Random()
        else:
            self.re = re
        
    def randomize(self):
        self.weapons = []
        weapon_patch = ''
        
        indices = list(self.df_weapon.index)
        new_len = int(len(indices) * self.percent_randomization *.01)
        indices = indices[:new_len]
        self.re.shuffle(indices)
        for i in indices:
            new_weapon = Weapon(self.df_weapon.loc[i],self.re)
            choice, pass_flag = self.find_replacement(self.df_weapon.loc[i])
            
            
            if pass_flag:
                # now rewrite shop costs
                weapon_patch = weapon_patch + rewrite_shop_costs(choice, self.df_weapon.loc[i])
                new_weapon.set_replacement(choice)
                if new_weapon.data_dict['subtype'] == 'flail':
                    new_weapon.bytemap['byte3'] = self.re.choice(['5E','4B'])
                self.weapons.append(new_weapon)
                
            else:
                # if pass_flag is False, then a valid replacement wasn't found
                # in this case, the original item needs to be REMOVED from the 
                # pool of items in the game, since it is not randomized
                
                self.banned_items.append(self.df_weapon.loc[i])
                
        return weapon_patch
            
    def find_replacement(self,og_weapon):
        og_weapon_type = og_weapon['subtype']
        og_weapon_tier = og_weapon['tier']
        og_weapon_name = og_weapon['readable_name']
        
        df = self.df_custom_weapons[(self.df_custom_weapons['weapon_type']==og_weapon_type)]
        
        tier_adj = 1
        while tier_adj < 10:
            pass_flag = True
            if og_weapon_type in ['whip','bow','spear']:
                # for killer weapons, strictly try to find a replacement at equal or less the value only
                df_temp = df[(df['tier'] <= og_weapon_tier) & (df['tier'] >= (og_weapon_tier - tier_adj))]
            else:
                df_temp = df[(df['tier'] <= og_weapon_tier + round(tier_adj/2)) & (df['tier'] >= (og_weapon_tier - tier_adj))]
            choices = list(df_temp.index)
            try:
                choice = self.re.choice(choices)
                weapon_name_clean = df_temp.loc[choice]['weapon_name_menu'].split(">")[1]
#                logging.error(weapon_name_clean)
#                if weapon_name_clean == 'Elements':
#                    breakpoint()
                
            except:
#                print("  Error on drawing choice for %s, increasing tier_adj" % og_weapon_name)
                tier_adj += 1
                pass_flag = False
                continue
                
            if pass_flag:
                
                # first see if it can reroll based on the modification name only (Aero 2, Mantra)
                iter_num = 0
                while iter_num < 10:
                    if weapon_name_clean not in self.history.values():
                        self.history[choice] = weapon_name_clean
#                        logging.error("ROUND 1 >>>>>>"+df.loc[choice]['weapon_name_textbox'])
                        return df.loc[choice], True # True = pass_flag for valid replacement
                    else:
                        # reroll, try again
                        choice = self.re.choice(choices)
                        weapon_name_clean = df_temp.loc[choice]['weapon_name_menu'].split(">")[1]
                    iter_num += 1
                

                # if not, perform for pure duplicates
                iter_num = 0
                while iter_num < 10:

                    if choice not in self.history:
                        self.history[choice] = weapon_name_clean
#                        logging.error("ROUND 2 >>>>>>"+df.loc[choice]['weapon_name_textbox'])
                        return df.loc[choice], True # True = pass_flag for valid replacement
                    else:
                        # reroll, try again
                        choice = self.re.choice(choices)
                        weapon_name_clean = df_temp.loc[choice]['weapon_name_menu'].split(">")[1]
                    iter_num += 1
                tier_adj += 1        
        
        # if made it past 10 tier_adj, call out error and give pure random

#        print("Error, exceeded 10 tiers. Adding to items to remove")
        return 0, False

            
            
    def write_asar_output(self):
        with open(os.path.join(os.path.pardir,os.path.pardir,'projects','test_asm','r-patch_weapons.asm'),'w') as f:
            f.write("\n")   
        for x in self.weapons:
            with open(os.path.join(os.path.pardir,os.path.pardir,'projects','test_asm','r-patch_weapons.asm'),'a') as f:
                f.write(x.asar_output)       
    @property
    def get_patch(self):
        output_str = ''
        for x in self.weapons:
            output_str = output_str + x.asar_output
        return output_str
    
    @property
    def get_spoiler(self):
        output_str = '\n-----WEAPON RANODMIZATION-----\n'
        for x in self.weapons:
            output_str = output_str + x.spoiler
        output_str = output_str + '\n'
        return output_str
