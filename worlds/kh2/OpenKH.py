import zipfile
import yaml
import os
import shutil

from BaseClasses import MultiWorld, Location, Region, Item, RegionType, Entrance, Tutorial, ItemClassification
from .Items import KH2Item, ItemData, item_dictionary_table,lookup_kh2id_to_name
from .Locations import all_locations, setup_locations
from .Options import FinalEXP, MasterEXP, LimitEXP, WisdomEXP, ValorEXP, Schmovement,Kingdom_Hearts2_Options
from .modYml import modYml
from .Names import ItemName
from .Locations import LocationName
from .ItemId import id

import Utils
import Patch
import worlds.AutoWorld
import worlds.Files

def noop(self, *args, **kw):
    pass
def patch_kh2(world,player,self,output_directory):
    datas={
    "items": {location.name: location.item.name
             if location.item.player == self.player else "Remote"
              for location in self.world.get_filled_locations(self.player)}
                
    }
    mod_name="yourmom"
    mod_dir = os.path.join(output_directory,mod_name, "locale")

    os.makedirs(mod_dir, exist_ok=True)
    #shutil.copytree(os.path.join(os.path.dirname(__file__)), mod_dir, dirs_exist_ok=True)
    kh2id=([loc.item for loc in self.world.get_filled_locations(self.player)])
    #kh2id=dict.fromkeys(kh2id)
    self.formattedTrsr = {}
    print(kh2id)
    j=2
    for i in range(len(kh2id)):
        openkh=id[str(kh2id[i])]
        self.formattedTrsr[j] = {"ItemId":openkh}
        j+=1
    #print(self.formattedTrsr)
    with open(mod_dir, "wb") as f:
      f.writestr("TrsrList.yml", yaml.dump(self.formattedTrsr, line_break="\r\n"))
    #print(yaml.dump(self.formattedTrsr, line_break="\r\n"))

    self.formattedLvup = {"Sora":{}}
    self.formattedBons = {}
    self.formattedFmlv = {}
    self.formattedItem = {"Stats":[]}
    self.formattedPlrp = []