import zipfile
import yaml
import os
import shutil

from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from .Items import KH2Item, ItemData, item_dictionary_table,lookup_kh2id_to_name
from .Locations import all_locations, setup_locations,LocationName
from .Options import FinalEXP, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,Kingdom_Hearts2_Options
from .modYml import modYml
from .Names import ItemName
from .ItemId import itemId


#import Utils
#import Patch
#import worlds.AutoWorld
#import worlds.Files

def noop(self, *args, **kw):
    pass
def patch_kh2(world,player,self,output_directory):
    itemName= {location.name: location.item.code.kh2id
                for location in self.world.get_filled_locations(self.player)}
    locName=[location.item.code.kh2id
             for location in self.world.get_filled_locations(self.player)
            ]  
    self.formattedTrsr = {}
    print(itemName)
    print(locName[5])
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
    #  outfile.write(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #  print(yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #  #print(self.trsrLocation)
    # #self.formattedLvup = {"Sora":{}}
    # #self.formattedBons = {}
    # #self.formattedFmlv = {}
    # #self.formattedItem = {"Stats":[]}
    # #self.formattedPlrp = []



    #for loop
       #if yml=0 then bonus item =id of that item
       #else bonus item=0

       #if dummy14=true then id =dummy14 else 