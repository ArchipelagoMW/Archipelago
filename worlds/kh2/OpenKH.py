import zipfile

from typing import ClassVar, Dict, Tuple, Any, Optional, Union, BinaryIO
import yaml
import os
import shutil
import random
import json
import os
import shutil
import Utils
import zipfile
from .Items import item_dictionary_table
from .Locations import all_locations,SoraLevels
from .XPValues import lvlStats, formExp, soraExp
import Utils
from .Names import LocationName
import worlds.Files
#class KH2ModFile(worlds.Files.APContainer):
#    game = "Factorio"
#    compression_method = zipfile.ZIP_DEFLATED  # Factorio can't load LZMA archives
#
#    def write_contents(self, opened_zipfile: zipfile.ZipFile):
#        # directory containing Factorio mod has to come first, or Factorio won't recognize this file as a mod.
#        mod_dir = self.path[:-4]  # cut off .zip
#        for root, dirs, files in os.walk(mod_dir):
#            for file in files:
#                opened_zipfile.write(os.path.join(root, file),
#                                     os.path.relpath(os.path.join(root, file),
#                                                     os.path.join(mod_dir, '..')))
#        # now we can add extras.
#        super(KH2ModFile, self).write_contents(opened_zipfile)
def patch_kh2(self, output_directory):




    def increaseStat(i):
        if lvlStats[i] == "str":
            self.strength += 2
        if lvlStats[i] == "mag":
            self.magic += 2
        if lvlStats[i] == "def":
            self.defense += 1
        if lvlStats[i] == "ap":
            self.ap += 3

    self.formattedTrsr = {}
    self.formattedBons = []
    self.formattedLvup = {"Sora": {}}
    self.formattedBons = {}
    self.formattedFmlv = {}
    self.formattedItem = {"Stats": []}
    self.formattedPlrp = []
    self.strength = 2
    self.magic = 6
    self.defense = 2
    self.ap = 50
    soraStartingItems = []
    goofyStartingItems = []
    donaldStartingItems = []
    mod_name = f"AP-{self.multiworld.seed_name}-P{self.player}-{self.multiworld.get_file_safe_player_name(self.player)}"
    
    for location in self.multiworld.get_filled_locations(self.player):
        #if location.player==self.player:
        #    continue
        if location.name==LocationName.StationDusks:
            print()
        data = all_locations[location.name]
        if location.item.player==self.player:
            itemcode = item_dictionary_table[location.item.name].kh2id
        else:
            #filling in lists for how to check if a chest is opened
            self.kh2multiworld_locations.append(location.name)
            itemcode = 461

        if data.yml=="Chest":
            self.formattedTrsr[data.locid] = {"ItemId":itemcode}


        elif data.yml in ["Get Bonus", "Double Get Bonus", "Second Get Bonus"]:
            if data.yml == "Get Bonus":
                dblbonus = 0
            # if double bonus then addresses dbl bonus so the next check gets 2 items on it
            if data.yml == "Double Get Bonus":
                dblbonus = itemcode
                continue
            if not data.locid in self.formattedBons.keys():
                self.formattedBons[data.locid] = {}
            self.formattedBons[data.locid][data.charName] = {
                "RewardId": data.locid,
                "CharacterId": data.charNumber,
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
            # putting dbl bonus at 0 again so we dont have the same item placed multiple time
            dblbonus = 0


        elif data.yml == "Keyblade":
            self.formattedItem["Stats"].append({
                "Id": data.locid,
                "Attack": random.randint(self.multiworld.Keyblade_Minimum[self.player].value,
                                         self.multiworld.Keyblade_Maximum[self.player].value),
                "Magic": random.randint(self.multiworld.Keyblade_Minimum[self.player].value,
                                        self.multiworld.Keyblade_Maximum[self.player].value),
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

        elif data.yml == "Forms":
            # loc id is form lvl
            # char name is the form name number :)
            if (data.locid == 2):
                formDict = {1: "Valor", 2: "Wisdom", 3: "Limit", 4: "Master", 5: "Final"}
                formDictExp = {1: self.multiworld.Valor_Form_EXP[self.player].value,
                               2: self.multiworld.Wisdom_Form_EXP[self.player].value
                    , 3: self.multiworld.Limit_Form_EXP[self.player].value,
                               4: self.multiworld.Master_Form_EXP[self.player].value
                    , 5: self.multiworld.Final_Form_EXP[self.player].value}
                formexp = formDictExp[data.charName]
                formName = formDict[data.charName]
                self.formattedFmlv[formName] = []
                self.formattedFmlv[formName].append({
                            "Ability": 1,
                            "Experience": int(formExp[data.charName][data.locid] / formexp),
                            "FormId": data.charName,
                            "FormLevel": 1,
                            "GrowthAbilityLevel": 0,
                        })
            # row is form column is lvl
            self.formattedFmlv[formName].append({
                "Ability": itemcode,
                "Experience": int(formExp[data.charName][data.locid] / formexp),
                "FormId": data.charName,
                "FormLevel": data.locid,
                "GrowthAbilityLevel": 0,
            })

        elif data.yml == "Critical":
            if data.charName == "Sora":
                soraStartingItems.append(itemcode)
            elif data.charName == "Goofy":
                goofyStartingItems.append(itemcode)
            else:
                donaldStartingItems.append(itemcode)
    #if self.multiworld.Schmovement[self.player].value == 1:
    #    soraStartingItems += 94, 98, 564, 102, 106

    if self.multiworld.Critical_Mode[self.player].value == 1:
        self.formattedPlrp.append({
            "Character": 1,  # Sora Starting Items (Crit)
            "Id": 7,  # crit difficulty
            "Hp": 20,
            "Mp": 100,
            "Ap": 50,
            "ArmorSlotMax": 1,
            "AccessorySlotMax": 1,
            "ItemSlotMax": 3,
            "Items": soraStartingItems,
            "Padding": [0] * 52
        })
    else:
        self.formattedPlrp.append({
            "Character": 1,  # Sora Starting Items (Non Crit)
            "Id": 0,
            "Hp": 20,
            "Mp": 100,
            "Ap": 50,
            "ArmorSlotMax": 1,
            "AccessorySlotMax": 1,
            "ItemSlotMax": 3,
            "Items": soraStartingItems,
            "Padding": [0] * 52
        })
    self.formattedPlrp.append({
        "Character": 2,  # Donald Starting Items
        "Id": 0,
        "Hp": 20,
        "Mp": 100,
        "Ap": 45,
        "ArmorSlotMax": 1,
        "AccessorySlotMax": 2,
        "ItemSlotMax": 2,
        "Items": donaldStartingItems,
        "Padding": [0] * 52
    })
    self.formattedPlrp.append({
        "Character": 3,  # Goofy Starting Items
        "Id": 0,
        "Hp": 20,
        "Mp": 100,
        "Ap": 45,
        "ArmorSlotMax": 2,
        "AccessorySlotMax": 1,
        "ItemSlotMax": 3,
        "Items": goofyStartingItems,
        "Padding": [0] * 52
    })

    # Summons have no checks on them so done fully locally
    self.formattedFmlv["Summon"] = []
    for x in range(1, 7):
        self.formattedFmlv["Summon"].append({
            "Ability": 123,
            "Experience": int(formExp[0][x] / self.multiworld.Summon_EXP[self.player].value),
            "FormId": 0,
            "FormLevel": x,
            "GrowthAbilityLevel": 0,
        })
    #levels done down here because of optinal settings that can take locations out of the pool. Might be able to refactor all the code to do somthing like this
    self.i=1
    for location in SoraLevels:
        increaseStat(random.randint(0, 3))
        try:
            data=self.multiworld.get_location(location,self.player)
            if data.item.player==self.player: 
                itemcode=item_dictionary_table[data.item.name].kh2id
            else:
                itemcode=461
            #    itemcode = item_dictionary_table[location.item.name].kh2id
            #else:
            #    #filling in lists for how to check if a chest is opened
            #    self.kh2multiworld_locations.append(location.name)
            #    itemcode = 461
        except:
            increaseStat(random.randint(0, 3))
            itemcode=0
        self.formattedLvup["Sora"][self.i] = {
            "Exp": int(soraExp[self.i] / self.multiworld.Sora_Level_EXP[self.player].value),
            "Strength": self.strength,
            "Magic": self.magic,
            "Defense": self.defense,
            "Ap": self.ap,
            "SwordAbility": itemcode,
            "ShieldAbility": itemcode,
            "StaffAbility": itemcode,
            "Padding": 0,
            "Character": "Sora",
            "Level": self.i
            }
        self.i+=1
    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__, )
    os.makedirs(mod_dir, exist_ok=False)
    with open(os.path.join(mod_dir, "Trsrlist.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedTrsr,line_break="\n"))
    with open(os.path.join(mod_dir, "LvupList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedLvup,line_break="\n"))
    with open(os.path.join(mod_dir, "BonsList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedBons,line_break="\n"))
    with open(os.path.join(mod_dir, "ItemList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedItem,line_break="\n"))
    with open(os.path.join(mod_dir, "FmlvList.yml"), "wt") as f:
        f.write(yaml.dump(self.formattedFmlv,line_break="\n"))
    with open(os.path.join(mod_dir,"PlrpList.yml"),"wt") as f:
        f.write(yaml.dump(self.formattedPlrp,line_break="\n"))
    with open(os.path.join(mod_dir, "archipelago.json"), "wt") as f:
        json.dump({"server": "", "player": self.player, "player_name": self.multiworld.player_name[self.player], "game": "Kingdom Hearts 2", "compatible_version": 0, "version": 0},f,indent=4)
    shutil.copytree(os.path.join(os.path.dirname(__file__), "mod_template"),mod_dir,dirs_exist_ok=True)
    shutil.make_archive(mod_dir,'zip',mod_dir)
    shutil.rmtree(mod_dir)

            
    #try:
    #    self.multiworld.get_location(LocationName.Lvl59, self.player).place_locked_item(self.create_item("Potion"))
    #except:
    #    print()