# -*- coding: utf-8 -*-
import os, sys
import json, pkgutil
THIS_FILEPATH = os.path.abspath(os.path.dirname(__file__))

class TextParser():
    def __init__(self, config):
        self.config = config

        def load_json_data(filepath: str):
            return json.loads(pkgutil.get_data(__name__,filepath).decode('utf-8-sig'))
        
        self.text_dict = load_json_data(os.path.join('tables','text_tables', 'json','text_table_chest.json'))
        self.text_dict2 = dict((v,k) for k,v in self.text_dict.items())


    def run_decrypt(self, byte_list):
        new_bytes = []
        num = 1
        for byte in byte_list:
            if byte == "ZZ":
                new_bytes.append("\n")
                num = num + 1
            else:
                byte = str(byte).upper()
                try:
                    newbyte = self.text_dict[byte]
                except:
                    newbyte = ' '
                new_bytes.append(newbyte)
        
        final_str = ''
        for byte in new_bytes:
            final_str = final_str + str(byte)
            
        print(final_str)

    def run_encrypt(self, passed_dict):
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
                    if new_char not in self.text_dict2:
                        new_char = ' '
                    else:
                        new_char = self.text_dict2[new_char]
                    text_list.append(new_char)
                    counter = right
                else:    
                    if char not in self.text_dict2:
                        new_char = ' '
                    else:
                        new_char = self.text_dict2[char]
                    text_list.append(new_char)
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

    def run_kuzar_encrypt(self, passed_dict):

        return_text = ''
        for x in passed_dict.keys():
            # limit length of x here to 30 characters. This is so text doesnt overwrite next slot
            
            modified_key = x[:31]
            counter = 0
            text_list = []
            while counter < len(modified_key):
                char = x[counter]
                try:
                    if char == "<":
                        left = x.find("<")
                        right = x.find(">")+1
                        new_char = x[left:right]
                        if new_char not in self.text_dict2:
                            new_char = ' '
                        else:
                            new_char = self.text_dict2[new_char]
                        text_list.append(new_char)
                        counter = right
                    else:    
                        if char not in self.text_dict2:
                            new_char = ' '
                        else:
                            new_char = self.text_dict2[char]
                        text_list.append(new_char)
                        counter = counter + 1
                except:
                    counter = counter + 1
                    
            text_asar = 'db '
            for i in text_list:
                text_asar = text_asar + " $" + i + ","
            text_asar = text_asar[:-1]
            #print("; "+x)
            return_text = return_text + "; "+modified_key.replace('@', '\\n') +"\n"
            #print('org $'+passed_dict[x])
            return_text = return_text + 'org $'+passed_dict[x] +"\n"

            #print(text_asar)
            return_text = return_text + text_asar + ", $00\n"

        return return_text

    def run_encrypt_text_string_old(self, x):
        counter = 0
        text_list = []
        while counter < len(x):
            char = x[counter]
            if char == "<":
                left = x.find("<")
                right = x.find(">")+1
                new_char = x[left:right]
                text_list.append(self.text_dict2[new_char])
                counter = right
            else:    
                text_list.append(self.text_dict2[char])
                counter = counter + 1
        text_asar = 'db'
        for i in text_list:
            text_asar = text_asar + " $" + i + ","
        text_asar = text_asar[:-1]
        return text_asar
    
    def run_encrypt_text_string(self,x,verbose=False,ff_fill=None):
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
                if new_char not in self.text_dict2:
                    new_char = ' '
                else:
                    new_char = self.text_dict2[new_char]
                text_list.append(new_char)
                counter = right
            else:    
                if char not in self.text_dict2:
                    new_char = ' '
                else:
                    new_char = self.text_dict2[char]
                text_list.append(new_char)
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
    
    def run_encrypt_text_string_hints(self, x):
        '''
        Same as above, but will split out line breaks 
        '''
        counter = 0
        text_list = []
        while counter < len(x):
            char = x[counter]
            if char == "<":
                left = x.find("<")
                right = x.find(">")+1
                new_char = x[left:right]
                new_char = x[left:right]
                if new_char not in self.text_dict2:
                    new_char = ' '
                else:
                    new_char = self.text_dict2[new_char]
                text_list.append(new_char)

                counter = right
            elif char == "|":
                text_list.append("01")
                counter = counter + 1
            else:    
                if char not in self.text_dict2:
                    new_char = ' '
                else:
                    new_char = self.text_dict2[char]
                text_list.append(new_char)
                counter = counter + 1
        text_asar = 'db'
        for i in text_list:
            text_asar = text_asar + " $" + i + ","
        text_asar = text_asar[:-1]
        return text_asar


    def run_exdeath_rewards(self, passed_dict):
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
                text_list.append(self.text_dict2[i])
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
                text_list.append(self.text_dict2[i])
            for y in text_list:
                text_asar2 = text_asar2 + " $" + y + ","
            text_asar2 = text_asar2 + " $A2, $00\n"


        text_asar3 = '; Addresses in events for key item actual rewards\n'
        loc_dict = dict(zip(['F90406','F90426','F90416'],list_of_locs))
        for base, loc in loc_dict.items():
            text_asar3 = text_asar3 + 'org $'+base+"\ndb $"+str(loc)+"\n"
        
        return_text = text_asar2 + "\n" + text_asar + "\n" + text_asar3
        return return_text

'''
TP = TextParser()

data = """

728E7B867A8B82877E966A7E92A2

"""

data = data.replace("\n","ZZ")
n = 2
byte_list = [data[i:i+n] for i in range(0, len(data), n)]


TP.run_decrypt(byte_list)
'''

