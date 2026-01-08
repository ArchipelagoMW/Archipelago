# -*- coding: utf-8 -*-
import pkgutil
import json
import os
# LOCAL PY VERSION

THIS_FILEPATH = os.path.dirname(__file__)

def load_json_data(filepath: str):
    return json.loads(pkgutil.get_data(__name__,filepath).decode('utf-8-sig'))


text_dict_chest = load_json_data(os.path.join('tables','text_tables', 'json','text_table_chest.json'))
text_dict_chest2 = dict((v,k) for k,v in text_dict_chest.items())

text_dict_shop = load_json_data(os.path.join('tables','text_tables', 'json','text_table_shop.json'))
text_dict_shop2 = dict((v,k) for k,v in text_dict_shop.items())


def init_table(tabletype):
# NEED TO CHOOSE ONE OF THE TWO:
    global text_dict, text_dict2

    if tabletype == 'shop' or tabletype == 'menu':
        text_dict = text_dict_shop
        text_dict2 = text_dict_shop2
    elif tabletype == 'chest':
        text_dict = text_dict_chest
        text_dict2 = text_dict_chest2
    

        

data = '''


ee638b7e7a86ffff

'''

data = data.replace("\n","ZZ")
n = 2
byte_list = [data[i:i+n] for i in range(0, len(data), n)]


def run_decrypt():
    new_bytes = []
    num = 1
    for byte in byte_list:
        if byte == "ZZ":
            new_bytes.append("\n")
            num = num + 1
        else:
            byte = str(byte).upper()
            try:
                newbyte = text_dict[byte]
            except:
                newbyte = ' '
            new_bytes.append(newbyte)
    
    final_str = ''
    for byte in new_bytes:
        final_str = final_str + str(byte)
        
    print(final_str)
    
    
def run_encrypt(passed_dict):
    return_text = ''
    for x in passed_dict.keys():
        counter = 0
        text_list = []
        while counter < len(x):
            char = x[counter]
            if char == "<":
                left = x.find("<")
                right = x.find(">")+1
                new_char = x[left:right]
                text_list.append(text_dict2[new_char])
                counter = right
            else:    
                text_list.append(text_dict2[char])
                counter = counter + 1
        text_asar = 'db'
        for i in text_list:
            text_asar = text_asar + " $" + i + ","
        text_asar = text_asar[:-1]
        print("; "+x)
        return_text = return_text + "; "+x +"\n"
        print('org $'+passed_dict[x])
        return_text = return_text + 'org $'+passed_dict[x] +"\n"
        print(text_asar)
        return_text = return_text + text_asar + "\n"
    return return_text

def run_encrypt_text_string(x,verbose=True,ff_fill=None):
    if verbose:
        print("\n")
        print(";"+str(x))
    return_text = ''
    counter = 0
    text_list = []
    while counter < len(x):
        char = x[counter]
        if char == "<":
            left = x.find("<")
            right = x.find(">")+1
            new_char = x[left:right]
            text_list.append(text_dict2[new_char])
            counter = right
        else:    
            text_list.append(text_dict2[char])
            counter = counter + 1
    text_asar = 'db'
    if ff_fill != None:
        new_len = ff_fill - len(text_list)
        for _ in range(new_len):
            text_list.append("FF")
    for i in text_list:
        text_asar = text_asar + " $" + i + ","
    text_asar = text_asar[:-1]
    if verbose:
        print(text_asar)
        return_text = return_text + text_asar + "\n"
    else:
        return_text = return_text + text_asar
    if verbose:
        print("\n")
    return return_text


def run_kuzar_encrypt(passed_dict):
    return_text = ''
    for x in passed_dict.keys():
        counter = 0
        text_list = []
        while counter < len(x):
            char = x[counter]
            if char == "<":
                left = x.find("<")
                right = x.find(">")+1
                new_char = x[left:right]
                text_list.append(text_dict2[new_char])
                counter = right
            else:    
                text_list.append(text_dict2[char])
                counter = counter + 1
        text_asar = 'db '
        for i in text_list:
            text_asar = text_asar + " $" + i + ","
        text_asar = text_asar[:-1]
        #print("; "+x)
        return_text = return_text + "; "+x.replace('@', '\\n') +"\n"
        #print('org $'+passed_dict[x])
        return_text = return_text + 'org $'+passed_dict[x] +"\n"

        #print(text_asar)
        return_text = return_text + text_asar + ", $00\n"

    return return_text


def run_exdeath_rewards(passed_dict):
    print(passed_dict)
    '''
    Pass in a DICTIONARY of 3 key items (actual text) and 3 key item reward 
        locations by related id (e.g. Sandworm has Big Bridge Key, 
            which is custom reward $68 every seed)
            DO NOT Big Bridge Key's ID - use Sandworm loc's ID
            Because THIS seed Sandworm has Big Bridge Key
        
        Final input should look like:
        {'Walse Tower Key':'68','Big Bridge Key':'77','SandWormBait':'82'}
            
    Returns asm patch
    '''
    
    list_of_keys = passed_dict.keys()
    list_of_locs = passed_dict.values()
    
    # This is for main 'key item' menu
    base_addr_1 = 'E2A0A7'
    # These are for the 3 text boxes asking if you want X item 
    list_of_individual_bases = ['E2A10B','E2A166','E2A1C6']

    
    text_asar = '; Key items block text (menu choices before choosing) \norg $'+base_addr_1+'\ndb' # main menu
    for x in list_of_keys:
        text_list = []
        for i in x:
            text_list.append(text_dict2[i])
        for y in text_list:
            text_asar = text_asar + " $" + y + ","
        text_asar = text_asar + " $01, "

    text_asar = text_asar + "$00\n"
    

    # Messy iteration trying to do both at once, replicate again...

    item_dict = dict(zip(list_of_individual_bases,list_of_keys))
    text_asar2 = '; Key items prompts (1 per key item) \n'
    for base, key_name in item_dict.items():
        text_asar2 = text_asar2 + ";"+key_name+"\norg $"+base+"\ndb "
        text_list = []
        for i in key_name:
            text_list.append(text_dict2[i])
        for y in text_list:
            text_asar2 = text_asar2 + " $" + y + ","
        text_asar2 = text_asar2 + " $A2, $00\n"


    text_asar3 = '; Addresses in events for key item actual rewards\n'
    loc_dict = dict(zip(['F90406','F90426','F90416'],list_of_locs))
    for base, loc in loc_dict.items():
        text_asar3 = text_asar3 + 'org $'+base+"\ndb $"+str(loc)+"\n"
    
    return_text = text_asar2 + "\n" + text_asar + "\n" + text_asar3
    return return_text






    
# def generate_keyitems():
#     print("Writing file to career_day/asm/asm_patches/text_tables/key_item_tables.asm...")
#     write_text = ''
#     write_text = write_text + '; Key Items (in menu) text\n'
#     write_text = write_text + run_encrypt(key_item_table)
#     write_text = write_text + '; Key Items (for rewards/chests) text\n'
#     write_text = write_text + run_encrypt(key_item_reward_table)
#     with open('../../projects/shared_asm/text_tables/key_item_tables.asm','w') as file:
#         file.write(write_text)
        
init_table('shop')
#run_decrypt()