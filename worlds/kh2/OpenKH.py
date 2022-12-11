from sre_constants import MAGIC
import zipfile
import yaml
import os
import shutil
import random
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

def noop(self, *args, **kw):
    pass
def patch_kh2(world,player,self,output_directory):
    #itemName= {location.address.locid: location.item.code.kh2id
    #            for location in self.world.get_filled_locations(self.player)}
<<<<<<< HEAD
    #locName=[location.item.code.kh2id
    #         for location in self.multiworld.get_filled_locations(self.player)]
=======
    locName=[location.item.code.kh2id
             for location in self.world.get_filled_locations(self.player)]
    #        ]  


    #if 3 then dbbl bonus = thing break
    #if 0 print things
    #reset double bns to 0
    self.formattedTrsr = {}
    self.formattedBons = []
    self.formattedLvup = {"Sora":{}}
    self.formattedBons = {}
    self.formattedFmlv = {}
    self.formattedItem = {"Stats":[]}
    self.formattedPlrp = []
    lvlablitity=0
    lvlcntr=1
    strength=0
    magic   =0
    defense =0
    ap=     50
    dblbonus=0
    def getStat(i):
        if lvlStats[i]=="str":
            strength=+2
        if lvlStats[i]=="mag":
            magic=+2
        if lvlStats[i]=="def":
            defense=+2
        if lvlStats[i]=="ap":
            ap=+2
    statcntr=0
    charName="Sora"
<<<<<<< HEAD
    for location in self.multiworld.get_filled_locations(self.player):
        if location.address.yml==1:
            self.formattedTrsr[location.address.locid] = {"ItemId":location.item.code.kh2id}
        
        elif location.address.yml==4: 
=======
    for location in self.world.get_filled_locations(self.player):
        #print(location.name)
        
            
        

        if location.address.yml==1:
            #print(location.address.locid)
            #print(location.item.code.kh2id)
            self.formattedTrsr[location.address.locid] = {"ItemId":location.item.code.kh2id}
            continue
        if location.address.yml==4: 
            getStat(random.randint(0,3))
            lvlablitity=location.item.code.kh2id
            if location.item.code.kh2id==1:
                lvlability=0
                getStat(random.randint(0,3))
            self.formattedLvup["Sora"][location.address.locid] = {
                    "Exp": int(soraExp[location.address.locid]/5),
                    "Strength":strength,
                    "Magic": magic ,
                    "Defense":defense,
                    "Ap":ap,
                    "SwordAbility": lvlablitity,
                    "ShieldAbility":lvlablitity,
                    "StaffAbility": lvlablitity,
                    "Padding": 0,
                    "Character": "Sora",
                    "Level": location.address.locid
                }
<<<<<<< HEAD
        elif location.address.yml==2 or location.address.yml==3 or location.address.yml==0:
=======
        if location.address.yml==2 or location.address.yml==3 or location.address.yml==0:
                #print(location.address.yml)
                if location.address.yml==2:
                    #print(location.address.locid)
                    dblbonus=0
                if location.address.yml==3:
                    dblbonus=location.item.code.kh2id
                if location.address.yml==0:
                    charName="sora"
                    #print(dblbonus)
                    #print(location.item.code.kh2id)
                self.formattedBons[location.address.locid] = {}
                self.formattedBons[location.address.locid] [charName]= {
                "RewardId": location.address.locid,
                "CharacterId": 1,
                "HpIncrease": 0,
                "MpIncrease": 0,
                "DriveGaugeUpgrade": 0,
                "ItemSlotUpgrade": 0,
                "AccessorySlotUpgrade": 0,
                "ArmorSlotUpgrade": 0,
                "BonusItem1": location.item.code.kh2id,
                "BonusItem2": dblbonus,
                "Padding": 0
            }
                continue
        if location.address.yml==5:
            print(location.item)
   
            #lvlcntr+=1        
<<<<<<< HEAD
    print(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    print(yaml.dump(self.formattedLvup, line_break="\r\n"))
    print(yaml.dump(self.formattedBons, line_break="\r\n"))
=======
    #print(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #print(yaml.dump(self.formattedLvup, line_break="\r\n"))
    #print(yaml.dump(self.formattedBons, line_break="\r\n"))
    #for i in range(len(locName)):
    #     if locName[i] in getBonus:
    #         print(locName[i])
    #         print(itemName[i])
    #         #print({"ItemId":trsrId(locName[i])})
    #         print({"ItemId":itemId[str(itemName[i])]})
    #key=frozenset(popid.items())
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
    ##print(kh2id)
    #j=2
    #for g in range(len(locationId)):
    #    if locationId[g] in popid:
    #        #print("This is placeholder text")
    #    if locationId[g] in trsrId:
    #        self.trsrLocation[g]=trsrId[str(locationId[g])]
    #    else:
    #       #print("This is roxas check")
    #    self.formattedTrsr[self.trsrLocation[g]] = {"ItemId":id[str(kh2id[g])]}
    ##for i in range(len(kh2id)):
    ##    openkh=id[str(kh2id[i])]
    ##    self.formattedTrsr[trsr.location.LocationId] = {"ItemId":trsr.item.Id}
    ##    self.formattedTrsr[i] = {"ItemId":openkh}
    ##    j+=1
    ##print(self.formattedTrsr)
    ## for loop that sorts them in a for loop if they are not in location
    ##I can do this by using the dictionarys I already have
    ##treasures = [trsr for trsr in treasures if locationType.Puzzle not in trsr.location.LocationTypes and locationType.Critical 
    ##not in trsr.location.LocationTypes and locationType.SYNTH not in trsr.location.LocationTypes]
    #
    #with open(os.path.join(output_directory, filename), 'w') as outfile:
<<<<<<< HEAD
    #outfile.write(yaml.dump(self.formattedTrsr, line_break="\r\n"))
=======
    #  outfile.write(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #  print(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #  #print(self.trsrLocation)




    #for loop
       #if yml=0 then bonus item =id of that item
       #else bonus item=0

       #if dummy14=true then id =dummy14 else 
