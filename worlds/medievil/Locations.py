from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import MedievilItem

class MedievilLocationCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    WEAPON = 2
    CHALICE = 3
    FUN = 4
    LEVEL_END = 5
    SKIP = 6

class MedievilLocationData(NamedTuple):
    name: str
    default_item: str
    m_code: int
    category: MedievilLocationCategory


class MedievilLocation(Location):
    game: str = "Medievil"
    category: MedievilLocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: MedievilLocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 99251000
        return {location_data.name: (base_id + location_data.m_code) for location_data in location_tables["MainWorld"]}

    def place_locked_item(self, item: MedievilItem):
        self.item = item
        self.locked = True
        item.location = self
        
# don't forget you need minimum number of locations to be the max of the progression items
# The MainWorld can probably be split out into seperate areas at a later date. But for now one big one is fine.
location_tables = {
"MainWorld": [
    
    # Level Complete
    
    MedievilLocationData("Dan's Crypt: Cleared","Level_End",1,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Graveyard: Cleared","Level_End",2,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Return to the Graveyard: Cleared","Level_End",3,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cemetery Hill: Cleared","Level_End",4,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("The Hilltop Mausoleum: Cleared","Level_End",5,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Scarecrow Fields: Cleared","Level_End",6,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Ant Hill: Cleared","Level_End",7,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("The Crystal Caves: Cleared","Level_End",8,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Lake: Cleared","Level_End",9,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Pumpkin Gorge: Cleared","Level_End",10,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Pumpkin Serpent: Cleared","Level_End",11,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Sleeping Village: Cleared","Level_End",12,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Pools of the Ancient Dead: Cleared","Level_End",13,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Asylum Grounds: Cleared","Level_End",14,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Inside the Asylum: Cleared","Level_End",15,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Enchanted Earth: Cleared","Level_End",16,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Gallows Gauntlet: Cleared","Level_End",17,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Haunted Ruins: Cleared","Level_End",18,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Ghost Ship: Cleared","Level_End",19,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Entrance Hall: Cleared","Level_End",20,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("The Time Device: Cleared","Level_End",21,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Zaroks Lair: Cleared","Level_End",22,MedievilLocationCategory.PROGRESSION),
    
    # Chalices
    
    MedievilLocationData("The Graveyard: Chalice","Chalice of Souls",23,MedievilLocationCategory.CHALICE), 
    MedievilLocationData("Return to the Graveyard: Chalice","Chalice of Souls",24,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Cemetery Hill: Chalice","Chalice of Souls",25,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("The Hilltop Mausoleum: Chalice","Chalice of Souls",26,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Scarecrow Fields: Chalice","Chalice of Souls",27,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Ant Hill: Chalice","Chalice of Souls",28,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("The Crystal Caves: Chalice","Chalice of Souls",29,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("The Lake: Chalice","Chalice of Souls",30,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Pumpkin Gorge: Chalice","Chalice of Souls",31,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Pumpkin Serpent: Chalice","Chalice of Souls",32,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Sleeping Village: Chalice","Chalice of Souls",33,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Pools of the Ancient Dead: Chalice","Chalice of Souls",34,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Asylum Grounds: Chalice","Chalice of Souls",35,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Inside the Asylum: Chalice","Chalice of Souls",36,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Enchanted Earth: Chalice","Chalice of Souls",37,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("The Gallows Gauntlet: Chalice","Chalice of Souls", 38,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("The Haunted Ruins: Chalice","Chalice of Souls", 39,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Ghost Ship: Chalice","Chalice of Souls",40,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("The Entrance Hall: Chalice","Chalice of Souls",41,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("The Time Device: Chalice","Chalice of Souls",42,MedievilLocationCategory.CHALICE),     
    
    
    # remove all these bloody level ends that you defaulted. 
    
    # Skills
    MedievilLocationData("Daring Dash: Skill","Level_End",43,MedievilLocationCategory.FUN),
    
    # Hall Of Heroes
    MedievilLocationData("Canny Tim 1: Hall Of Heroes","Level_End",44,MedievilLocationCategory.FUN),
    MedievilLocationData("Canny Tim 2: Hall Of Heroes","Level_End",45,MedievilLocationCategory.FUN),
    MedievilLocationData("Stanyer Iron Hewer 1: Hall Of Heroes","Level_End",46,MedievilLocationCategory.FUN),
    MedievilLocationData("Stanyer Iron Hewer 2: Hall Of Heroes","Level_End",47,MedievilLocationCategory.FUN),
    MedievilLocationData("Woden The Mighty 1: Hall Of Heroes","Level_End",48,MedievilLocationCategory.FUN),   
    MedievilLocationData("Woden The Mighty 2: Hall Of Heroes","Level_End",49,MedievilLocationCategory.FUN),   
    MedievilLocationData("RavenHooves The Archer 1: Hall Of Heroes","Level_End",50,MedievilLocationCategory.FUN),      
    MedievilLocationData("RavenHooves The Archer 2: Hall Of Heroes","Level_End",51,MedievilLocationCategory.FUN),       
    MedievilLocationData("RavenHooves The Archer 3: Hall Of Heroes","Level_End",52,MedievilLocationCategory.FUN),   
    MedievilLocationData("RavenHooves The Archer 4: Hall Of Heroes","Level_End",53,MedievilLocationCategory.FUN),
    MedievilLocationData("Imanzi 1: Hall Of Heroes","Level_End",54,MedievilLocationCategory.FUN),    
    MedievilLocationData("Imanzi 2: Hall Of Heroes","Level_End",55,MedievilLocationCategory.FUN),
    MedievilLocationData("Dark Steadfast 1: Hall Of Heroes","Level_End",56,MedievilLocationCategory.FUN),        
    MedievilLocationData("Dark Steadfast 2: Hall Of Heroes","Level_End",57,MedievilLocationCategory.FUN),      
    MedievilLocationData("Karl Stungard 1: Hall Of Heroes","Level_End",58,MedievilLocationCategory.FUN),  
    MedievilLocationData("Karl Stungard 2: Hall Of Heroes","Level_End",59,MedievilLocationCategory.FUN),
    MedievilLocationData("Bloodmonath Skill Cleaver 1: Hall Of Heroes","Level_End",60,MedievilLocationCategory.FUN),
    MedievilLocationData("Bloodmonath Skill Cleaver 2: Hall Of Heroes","Level_End",61,MedievilLocationCategory.FUN),
    MedievilLocationData("Megwynne Stormbinder 1: Hall Of Heroes","Level_End",62,MedievilLocationCategory.FUN),
    MedievilLocationData("Megwynne Stormbinder 1: Hall Of Heroes","Level_End",63,MedievilLocationCategory.FUN),
    
    # Weapon Pickups
    MedievilLocationData("Small Sword: Dans Crypt","Level_End",64,MedievilLocationCategory.FUN),
    MedievilLocationData("Broadsword: Hall of Heroes","Level_End",65,MedievilLocationCategory.FUN),
    MedievilLocationData("Magic Sword: Hall of Heroes","Level_End",66,MedievilLocationCategory.FUN),    
    MedievilLocationData("Club: Cemetery Hill","Level_End",67,MedievilLocationCategory.FUN),  
    MedievilLocationData("Hammer: Hall Of Heroes","Level_End",68,MedievilLocationCategory.FUN),
    MedievilLocationData("Daggers: Dan's Crypt","Level_End",69,MedievilLocationCategory.FUN),
    MedievilLocationData("Axe: Hall Of Heroes","Level_End",70,MedievilLocationCategory.FUN),
    MedievilLocationData("Chicken Drumsticks: The Enchanted Earth","Level_End",71,MedievilLocationCategory.FUN),
    MedievilLocationData("Crossbow: Hall Of Heroes","Level_End",72,MedievilLocationCategory.FUN),    
    MedievilLocationData("Longbow: Hall Of Heroes","Level_End",73,MedievilLocationCategory.FUN),
    MedievilLocationData("Fire Longbow: Hall Of Heroes","Level_End",74,MedievilLocationCategory.FUN),    
    MedievilLocationData("Magic Longbow: Hall Of Heroes","Level_End",75,MedievilLocationCategory.FUN),
    MedievilLocationData("Spear: Hall Of Heroes","Level_End",76,MedievilLocationCategory.FUN),
    MedievilLocationData("Lightning: Hall Of Heroes","Level_End",77,MedievilLocationCategory.FUN),
    MedievilLocationData("Good Lightning: Zarok's Lair","Level_End",78,MedievilLocationCategory.FUN), # probably just fire when at the level
    MedievilLocationData("Copper Shield: Dan's Crypt","Level_End",79,MedievilLocationCategory.FUN),    # there will definately be more than this
    MedievilLocationData("Silver Shield: Return to the Graveyard","Level_End",80,MedievilLocationCategory.FUN), # There will be more than this
    MedievilLocationData("Gold Shield: Hall Of Heroes","Level_End",81,MedievilLocationCategory.FUN),
    MedievilLocationData("Dragon Armour: The Crystal Caves","Level_End",82,MedievilLocationCategory.FUN),

    # Life Bottles
    MedievilLocationData("Life Bottle: Dan's Crypt","Level_End",83,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: The Graveyard","Level_End",84,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Hall of Heroes (Canny Tim)","Level_End",85,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Dan's Crypt - Behind Wall","Level_End",86,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Scarecrow Fields","Level_End",87,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Pools of the Ancient Dead","Level_End",88,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Hall of Heroes (Ravenhooves The Archer)","Level_End",89,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Hall of Heroes (Dirk Steadfast)","Level_End",90,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: The Time Device","Level_End",91,MedievilLocationCategory.FUN)
]
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})