from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import MedievilItem

class MedievilLocationCategory(IntEnum):
    FILLER = 0
    PROGRESSION = 1
    FUN = 2
    LEVEL_END = 4
    SKIP = 5

class MedievilLocationData(NamedTuple):
    name: str
    default_item: str
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
        base_id = 9900000
        return ({location_data.name: id for id, location_data in enumerate(location_tables["MainWorld"], base_id + 1 )})

    def place_locked_item(self, item: MedievilItem):
        self.item = item
        self.locked = True
        item.location = self

location_tables = {
"MainWorld": [
    MedievilLocationData(f"Dan's Crypt: Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),    
    MedievilLocationData(f"The Graveyard Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Return to the Graveyard Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Cemetery Hill Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"The Hilltop Mausoleum Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Scarecrow Fields Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Ant Caves Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"The Crystal Caves Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),                    
    MedievilLocationData(f"The Lake Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Pumpkin Gorge Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Pumpkin Serpent Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Sleeping Village Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData(f"Pools of the Ancient Dead Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData(f"Asylum Grounds Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Inside the Asylum Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Enchanted Earth Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Gallows Gauntlet (needs more info) Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Haunted Ruins Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Ghost Ship Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Entrance Hall Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"The Time Device Cleared",f"Level_End" ,MedievilLocationCategory.LEVEL_END),     
    MedievilLocationData(f"Zaroks Lai Clearedr",f"Level_End" ,MedievilLocationCategory.LEVEL_END),                              
]
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})