from sre_constants import MAGIC
import zipfile
import yaml
import os
import shutil
import random
import json
import os
import shutil
import threading
import zipfile
import jinja2
import Utils
import worlds.Files
from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from .Items import KH2Item, ItemData, item_dictionary_table,lookup_kh2id_to_name
from .Locations import all_locations, setup_locations,LocationName
from .Options import FinalEXP, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,KH2_Options
from .modYml import modYml
from .Names import ItemName
from .ItemId import itemId
from .XPValues import lvlStats,formExp,soraExp

#import Utils
#import Patch
#import worlds.AutoWorld
#import worlds.Files


def patch_kh2(world,player,self,output_directory):
    #itemName= {location.address.locid: location.item.code.kh2id
    #            for location in self.world.get_filled_locations(self.player)}
    #locName=[location.item.code.kh2id
    #         for location in self.multiworld.get_filled_locations(self.player)]


    def increaseStat(i):
        if lvlStats[i]=="str":
            self.strength+=2
        if lvlStats[i]=="mag":
            self.magic+=2
        if lvlStats[i]=="def":
            self.defense+=2
        if lvlStats[i]=="ap":
            self.ap+=2

    #if 3 then dbbl bonus = thing break
    #if 0 print things
    #reset double bns to 0
    self.formattedTrsr = {}
    self.formattedBons = []
    self.formattedLvup = {"Sora":{}}
    self.formattedBons = {}
    self.formattedFmlv = {}
    self.formattedItem = {"Stats":[]}
    self.strength=0
    self.magic   =0
    self.defense =0
    self.ap=     50
    mod_name = "RandoSeed"



    for location in self.multiworld.get_filled_locations(self.player):
        if location.item.game=="Kingdom Hearts 2":
            itemcode=location.item.code.kh2id
        else:
            itemcode= 461
        if location.address.yml=="Chest":
            self.formattedTrsr[location.address.locid] = {"ItemId":itemcode}


        elif location.address.yml in["Get Bonus","Double Get Bonus","Second Get Bonus"]:
                if location.address.yml=="Get Bonus":
                    dblbonus=0
                #if double bonus then addresses dbl bonus so the next check gets 2 items on it
                if location.address.yml=="Double Get Bonus":
                    dblbonus=itemcode
                    continue
                self.formattedBons[location.address.locid] = {}
                self.formattedBons[location.address.locid] [location.address.charName]= {
                "RewardId": location.address.locid,
                "CharacterId": location.address.charNumber,
                "HpIncrease": 0,
                "MpIncrease": 0,
                "DriveGaugeUpgrade": 0,
                "ItemSlotUpgrade": 0,
                "AccessorySlotUpgrade": 0,
                "ArmorSlotUpgrade": 0,
                "BonusItem1": itemcode,
                "BonusItem2": dblbonus,
                "Padding": 0
            }
                #putting dbl bonus at 0 again so we dont have the same item placed multiple time
                dblbonus=0


        elif location.address.yml=="Levels": 
            increaseStat(random.randint(0,3))
            #this means if Item Nothing or potion
            if itemcode==1:
                itemcode=0
                increaseStat(random.randint(0,3))
            self.formattedLvup["Sora"][location.address.locid] = {
                "Exp": int(soraExp[location.address.locid]/5),
                "Strength":self.strength,
                "Magic": self.magic ,
                "Defense":self.defense,
                "Ap":self.ap,
                "SwordAbility": itemcode,
                "ShieldAbility":itemcode,
                "StaffAbility": itemcode,
                "Padding": 0,
                "Character": "Sora",
                "Level": location.address.locid
               }



        elif location.address.yml=="Keyblade":
            self.formattedItem["Stats"].append({
                "Id": location.address.locid,
                "Attack": random.randint(self.multiworld.Keyblade_Minimum[self.player].value, self.multiworld.Keyblade_Maximum[self.player].value),
                "Magic": random.randint(self.multiworld.Keyblade_Minimum[self.player].value, self.multiworld.Keyblade_Maximum[self.player].value),
                "Defense": 0,
                "Ability": itemcode,
                "AbilityPoints": 0,
                "Unknown08": 100,
                "FireResistance": 100,
                "IceResistance": 100,
                "LightningResistance": 100,
                "DarkResistance": 100,
                "Unknown0d": 100,
                "GeneralResistance": 100,
                "Unknown": 0
            })

        elif location.address.yml=="Forms":
            #loc id is form lvl
            #char name is the form name number :)
            if(location.address.locid==1):
                formDict = {1:"Valor",2:"Wisdom",3:"Limit",4:"Master",5:"Final"}
                formDictExp={1:self.multiworld.Valor_Form_EXP[self.player].value,2:self.multiworld.Wisdom_Form_EXP[self.player].value
                             ,3:self.multiworld.Limit_Form_EXP[self.player].value,4:self.multiworld.Master_Form_EXP[self.player].value
                             ,5:self.multiworld.Final_Form_EXP[self.player].value}
                formexp  = formDictExp[location.address.charName]
                formName = formDict[location.address.charName]
                self.formattedFmlv[formName] = []
            #row is form column is lvl
            
            self.formattedFmlv[formName].append({
                  "Ability": itemcode,
                  "Experience": int(formExp[location.address.charName][location.address.locid]/formexp),
                  "FormId": location.address.charName,
                  "FormLevel": location.address.locid,
                  "GrowthAbilityLevel": 0,
            })

    #Summons have no checks on them so done fully locally
    self.formattedFmlv["Summon"]=[]
    for x in range(1,7):
         self.formattedFmlv["Summon"].append({
              "Ability": 461,
              "Experience": int(formExp[0][x]/self.multiworld.Summon_EXP[self.player].value),
              "FormId": 0,
              "FormLevel": x,
              "GrowthAbilityLevel": 0,
         })     





    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__,)
    os.makedirs(mod_dir, exist_ok=False)
    with open(os.path.join(mod_dir, "Trsrlist.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedTrsr,line_break="\r\n"))
    with open(os.path.join(mod_dir, "LvupList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedLvup,line_break="\r\n"))
    with open(os.path.join(mod_dir, "BonList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedBons,line_break="\r\n"))
    with open(os.path.join(mod_dir, "ItemList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedItem,line_break="\r\n"))
    with open(os.path.join(mod_dir, "FmlvList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedFmlv,line_break="\r\n"))
    #with open(os.path.join(mod_dir, "Trsrlist.yml"), "wt") as f:
    #    f.write(yaml.dump(self.formattedTrsr,line_break="\r\n"))
    shutil.make_archive(mod_dir,'zip',mod_dir)
    shutil.rmtree(mod_dir)
    

    #mod_dir = os.path.join(output_directory, "Randoseed.zip")
    #os.makedirs(mod_dir, exist_ok=True)
    #with open(os.path.join(mod_dir, "Trstlist.yml"), 'wt') as outfile: 
    #    outfile.writestr(yaml.dump(self.formattedTrsr,line_break="\r\n"))
    #with open(os.path.join(mod_dir, "Lvuplist.yml"), 'wt') as outfile: 
    #    outfile.write(yaml.dump(self.formattedLvup,line_break="\r\n"))
    #with open(os.path.join(output_directory, "Bonlist.yml"), 'w') as outfile: 
    #    outfile.write(yaml.dump(self.formattedBons,line_break="\r\n"))
    #with open(os.path.join(output_directory, "Itemlist.yml"), 'w') as outfile: 
    #    outfile.write(yaml.dump(self.formattedItem,line_break="\r\n"))


    #shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "mod"), mod_dir, dirs_exist_ok=True)
    #
    #with open(os.path.join(mod_dir, "data.lua"), "wt") as f:
    #    f.write(data_template_code)
    #with open(os.path.join(mod_dir, "data-final-fixes.lua"), "wt") as f:
    #    f.write(data_final_fixes_code)
    #with open(os.path.join(mod_dir, "control.lua"), "wt") as f:
    #    f.write(control_code)
    #with open(os.path.join(mod_dir, "settings.lua"), "wt") as f:
    #    f.write(settings_code)
    #locale_content = locale_template.render(**template_data)
    #with open(os.path.join(en_locale_dir, "locale.cfg"), "wt") as f:
    #    f.write(locale_content)
    #info = base_info.copy()
    #info["name"] = mod_name
    #with open(os.path.join(mod_dir, "info.json"), "wt") as f:
    #    json.dump(info, f, indent=4)
    #
    ## zip the result
    #zf_path = os.path.join(mod_dir + ".zip")
    #mod = FactorioModFile(zf_path, player=player, player_name=multiworld.player_name[player])
    #mod.write()

    #shutil.rmtree(mod_dir)
   # with open(os.path.join(output_directory, "Trstlist.yml"), 'w') as outfile: 
        
        #outZip.writestr("sys.yml", yaml.dump(sys, line_break="\r\n"))
        #outZip.writestr("jm.yml", yaml.dump(modYml.getJMYAML(), line_break="\r\n"))
        #outfile.write(yaml.dump(self.formattedTrsr,line_break="\r\n"))
        #
        #
        #outfile.write(yaml.dump(self.formattedLvup,line_break="\r\n"))
        #
        #outfile.write(yaml.dump(self.formattedFmlv,line_break="\r\n"))

    #mod_dir = os.path.join(output_directory, "Randoseed.zip")
    #en_locale_dir = os.path.join(mod_dir, "locale", "en")
    #os.makedirs(mod_dir, exist_ok=True)
    #with open(os.path.join(mod_dir, "TrsrList.yml"), "w") as f:
    #    f.write(yaml.dump(self.formattedTrsr,line_break="\r\n"))
    #with open(os.path.join(mod_dir, "data-final-fixes.lua"), "wt") as f:
    #    f.write(data_final_fixes_code)
    #with open(os.path.join(mod_dir, "control.lua"), "wt") as f:
    #    f.write(control_code)
    #with open(os.path.join(mod_dir, "settings.lua"), "wt") as f:
    #    f.write(settings_code)
    #locale_content = locale_template.render(**template_data)
    #with open(os.path.join(en_locale_dir, "locale.cfg"), "wt") as f:
    #    f.write(locale_content)
    #
    #data = io.BytesIO()
    #with zipfile.ZipFile(output_directory,"w") as outZip:
    #     outZip.write(os.path.join(output_directory, "Yourmom.txt"))
    #     outZip.writestr(, yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #     outZip.writestr("BonsList.yml", yaml.dump(self.formattedBons, line_break="\r\n"))
    #     outZip.writestr("LvupList.yml", yaml.dump(self.formattedLvup, line_break="\r\n"))
    #     outZip.writestr("FmlvList.yml", yaml.dump(self.formattedFmlv, line_break="\r\n"))
    #     outZip.writestr("ItemList.yml", yaml.dump(self.formattedItem, line_break="\r\n"))
    #outZip.close()
    #data.seek(0)
    #self.outputZip = data
    #mod_name="yourmom.yml"
    #mod_dir = os.path.join(output_directory,mod_name)
    #filename = f"trsr.yml"
        
    #os.makedirs(mod_dir, exist_ok=True)
     #trsrLocations=[loc for location in kh3id]
    #shutil.copytree(os.path.join(os.path.dirname(__file__)), mod_dir, dirs_exist_ok=True)
    #for i in range(5):
    #    kh2id=([loc.item for loc in self.world.get_filled_locations(self.player)])
    #    locationId=([location.name for location in self.world.get_filled_locations(self.player)])
    ##kh2id=dict.fromkeys(kh2id)
    ##print(locationId)
    #self.trsrLocation={}
    #self.formattedTrsr = {}

    #with open(os.path.join(output_directory, filename), 'w') as outfile:
    #outfile.write(yaml.dump(self.formattedTrsr, line_break="\r\n"))

    #  outfile.write(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #  print(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #  #print(self.trsrLocation)


 