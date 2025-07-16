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
    
    MedievilLocationData("Cleared: Dan's Crypt","Level_End",1,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: The Graveyard","Level_End",2,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Return to the Graveyard","Level_End",3,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Cemetery Hill","Level_End",4,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: The Hilltop Mausoleum","Level_End",5,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Scarecrow Fields","Level_End",6,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Ant Hill","Level_End",7,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: The Crystal Caves","Level_End",8,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: The Lake","Level_End",9,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Pumpkin Gorge","Level_End",10,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Pumpkin Serpent","Level_End",11,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Sleeping Village","Level_End",12,MedievilLocationCategory.LEVEL_END),
    MedievilLocationData("Cleared: Pools of the Ancient Dead","Level_End",13,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: Asylum Grounds","Level_End",14,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: Inside the Asylum","Level_End",15,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: Enchanted Earth","Level_End",16,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: The Gallows Gauntlet","Level_End",17,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: The Haunted Ruins","Level_End",18,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: Ghost Ship","Level_End",19,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: The Entrance Hall","Level_End",20,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: The Time Device","Level_End",21,MedievilLocationCategory.LEVEL_END), 
    MedievilLocationData("Cleared: Zaroks Lair","Level_End",22,MedievilLocationCategory.PROGRESSION),
    
    # Chalices
    
    MedievilLocationData("Chalice: The Graveyard","Chalice of Souls",23,MedievilLocationCategory.CHALICE), 
    MedievilLocationData("Chalice: Return to the Graveyard","Chalice of Souls",24,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Chalice: Cemetery Hill","Chalice of Souls",25,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Chalice: The Hilltop Mausoleum","Chalice of Souls",26,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Chalice: Scarecrow Fields","Chalice of Souls",27,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Chalice: Ant Hill","Chalice of Souls",28,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Chalice: The Crystal Caves","Chalice of Souls",29,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Chalice: The Lake","Chalice of Souls",30,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Chalice: Pumpkin Gorge","Chalice of Souls",31,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Chalice: Pumpkin Serpent","Chalice of Souls",32,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Chalice: Sleeping Village","Chalice of Souls",33,MedievilLocationCategory.CHALICE),    
    MedievilLocationData("Chalice: Pools of the Ancient Dead","Chalice of Souls",34,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Chalice: Asylum Grounds","Chalice of Souls",35,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Chalice: Inside the Asylum","Chalice of Souls",36,MedievilLocationCategory.CHALICE),
    MedievilLocationData("Chalice: Enchanted Earth","Chalice of Souls",37,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Chalice: The Gallows Gauntlet","Chalice of Souls", 38,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Chalice: The Haunted Ruins","Chalice of Souls", 39,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Chalice: Ghost Ship","Chalice of Souls",40,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Chalice: The Entrance Hall","Chalice of Souls",41,MedievilLocationCategory.CHALICE),     
    MedievilLocationData("Chalice: The Time Device","Chalice of Souls",42,MedievilLocationCategory.CHALICE),     
    
    
    # to do: remove all these bloody level ends that you defaulted. 
    
    # Skills
    MedievilLocationData("Skill: Daring Dash","Level_End",43,MedievilLocationCategory.FUN),
    
    # Hall Of Heroes
    MedievilLocationData("Hall of Heroes: Canny Tim 1","Level_End",44,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Canny Tim 2","Level_End",45,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Stanyer Iron Hewer 1","Level_End",46,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Stanyer Iron Hewer 2","Level_End",47,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Woden The Mighty 1","Level_End",48,MedievilLocationCategory.FUN),   
    MedievilLocationData("Hall of Heroes: Woden The Mighty 2","Level_End",49,MedievilLocationCategory.FUN),   
    MedievilLocationData("Hall of Heroes: RavenHooves The Archer 1","Level_End",50,MedievilLocationCategory.FUN),      
    MedievilLocationData("Hall of Heroes: RavenHooves The Archer 2","Level_End",51,MedievilLocationCategory.FUN),       
    MedievilLocationData("Hall of Heroes: RavenHooves The Archer 3","Level_End",52,MedievilLocationCategory.FUN),   
    MedievilLocationData("Hall of Heroes: RavenHooves The Archer 4","Level_End",53,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Imanzi 1","Level_End",54,MedievilLocationCategory.FUN),    
    MedievilLocationData("Hall of Heroes: Imanzi 2","Level_End",55,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Dark Steadfast 1","Level_End",56,MedievilLocationCategory.FUN),        
    MedievilLocationData("Hall of Heroes: Dark Steadfast 2","Level_End",57,MedievilLocationCategory.FUN),      
    MedievilLocationData("Hall of Heroes: Karl Stungard 1","Level_End",58,MedievilLocationCategory.FUN),  
    MedievilLocationData("Hall of Heroes: Karl Stungard 2","Level_End",59,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Bloodmonath Skill Cleaver 1","Level_End",60,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Bloodmonath Skill Cleaver 2","Level_End",61,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Megwynne Stormbinder 1","Level_End",62,MedievilLocationCategory.FUN),
    MedievilLocationData("Hall of Heroes: Megwynne Stormbinder 1","Level_End",63,MedievilLocationCategory.FUN),
    
    # Weapon Pickups
    MedievilLocationData("Equipment: Small Sword","Level_End",64,MedievilLocationCategory.FUN), # dans crypt
    MedievilLocationData("Equipment: Broadsword","Level_End",65,MedievilLocationCategory.FUN),  # hall of heroes
    MedievilLocationData("Equipment: Magic Swords","Level_End",66,MedievilLocationCategory.FUN),  # hall of heroes
    MedievilLocationData("Equipment: Club","Level_End",67,MedievilLocationCategory.FUN),  # cemetery hill
    MedievilLocationData("Equipment: Hammer","Level_End",68,MedievilLocationCategory.FUN), # hall of heroes
    MedievilLocationData("Equipment: Daggers","Level_End",69,MedievilLocationCategory.FUN), # dans crypt
    MedievilLocationData("Equipment: Axe","Level_End",70,MedievilLocationCategory.FUN),# hall of heroes
    MedievilLocationData("Equipment: Chicken Drumsticks","Level_End",71,MedievilLocationCategory.FUN), # enchanted earth
    MedievilLocationData("Equipment: Crossbow","Level_End",72,MedievilLocationCategory.FUN),    # hall of heroes
    MedievilLocationData("Equipment: Longbow","Level_End",73,MedievilLocationCategory.FUN),# hall of heroes
    MedievilLocationData("Equipment: Fire Longbow","Level_End",74,MedievilLocationCategory.FUN),    #   hall of heroes
    MedievilLocationData("Equipment: Magic Longbow","Level_End",75,MedievilLocationCategory.FUN),# hall of heroes
    MedievilLocationData("Equipment: Spear","Level_End",76,MedievilLocationCategory.FUN),# hall of heroes
    MedievilLocationData("Equipment: Lightning","Level_End",77,MedievilLocationCategory.FUN),# hall of heroes
    MedievilLocationData("Equipment: Good Lightning","Level_End",78,MedievilLocationCategory.FUN), # probably just fire when at the level
    MedievilLocationData("Equipment: Copper Shield","Level_End",79,MedievilLocationCategory.FUN),  # there will definately be more than this
    MedievilLocationData("Equipment: Silver Shield","Level_End",80,MedievilLocationCategory.FUN), # There will be more than this
    MedievilLocationData("Equipment: Gold Shield","Level_End",81,MedievilLocationCategory.FUN), # hall of heroes
    MedievilLocationData("Equipment: Dragon Armour","Level_End",82,MedievilLocationCategory.FUN), # crystal caves

    # Life Bottles
    MedievilLocationData("Life Bottle: Dan's Crypt","Level_End",83,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: The Graveyard","Level_End",84,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Hall of Heroes (Canny Tim)","Level_End",85,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Dan's Crypt - Behind Wall","Level_End",86,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Scarecrow Fields","Level_End",87,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Pools of the Ancient Dead","Level_End",88,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Hall of Heroes (Ravenhooves The Archer)","Level_End",89,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: Hall of Heroes (Dirk Steadfast)","Level_End",90,MedievilLocationCategory.FUN),
    MedievilLocationData("Life Bottle: The Time Device","Level_End",91,MedievilLocationCategory.FUN),
    
    # Key Items 
    MedievilLocationData("Key Item: Dragon Gem: Pumpkin Gorge","Level_End",92,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Dragon Gem: Inside the Asylum","Level_End",93,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: King Peregrine's Crown","Level_End",94,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 1","Level_End",95,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 2","Level_End",96,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 3","Level_End",97,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 4","Level_End",98,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 5","Level_End",99,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 6","Level_End",100,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 7","Level_End",101,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Soul Helmet 8","Level_End",102,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Witches Talisman","Level_End",103,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Safe Key","Level_End",104,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Shadow Artefact","Level_End",105,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Crucifix","Level_End",106,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Landlords Bust","Level_End",107,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Crucifix Cast","Level_End",108,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 1","Level_End",109,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 2","Level_End",110,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 3","Level_End",111,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 4","Level_End",112,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 5","Level_End",113,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 6","Level_End",114,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 7","Level_End",115,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Harvester Parts","Level_End",116,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Skull Key","Level_End",117,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Sheet Music","Level_End",118,MedievilLocationCategory.PROGRESSION),

    # Runes
    
    MedievilLocationData("Chaos Rune: The Graveyard","Level_End",119,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Hilltop Mausoleum","Level_End",120,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Scarecrow Fields","Level_End",121,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Lake","Level_End",122,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Pumpkin Gorge","Level_End",123,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Sleeping Village","Level_End",124,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Pools of the Ancient Dead","Level_End",125,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Asylum Grounds","Level_End",126,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Haunted Ruins","Level_End",127,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Ghost Ship","Level_End",128,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Time Device","Level_End",129,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Earth Rune: The Graveyard","Level_End",130,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Hilltop Mausoleum","Level_End",131,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Scarecrow Fields","Level_End",132,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Crystal Caves","Level_End",133,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Lake","Level_End",134,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Pumpkin Gorge","Level_End",135,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Sleeping Village","Level_End",136,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Inside the Asylum","Level_End",137,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Enchanted Earth","Level_End",138,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Haunted Ruins","Level_End",139,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Entrance Hall","Level_End",140,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Time Device","Level_End",141,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Moon Rune: The Hilltop Mausoleum","Level_End",142,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: Scarecrow Fields","Level_End",143,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: Pumpkin Gorge","Level_End",144,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: Ghost Ship","Level_End",145,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: The Time Device","Level_End",146,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Star Rune: Return to the Graveyard","Level_End",147,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: Dan's Crypt","Level_End",148,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: The Crystal Caves","Level_End",149,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: The Lake","Level_End",150,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: Enchanted Earth","Level_End",151,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: The Gallows Gauntlet","Level_End",152,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: Ghost Ship","Level_End",153,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Time Rune: The Lake","Level_End",154,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Time Rune: Pumpkin Gorge","Level_End",155,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Time Rune: The Time Device","Level_End",156,MedievilLocationCategory.PROGRESSION),
]
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})