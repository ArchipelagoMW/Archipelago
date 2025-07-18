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
    # MedievilLocationData("Cleared: Zaroks Lair","Level_End",22,MedievilLocationCategory.PROGRESSION),
    
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
    MedievilLocationData("Key Item: Amber Piece 8","Level_End",116,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 9","Level_End",117,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Amber Piece 10","Level_End",118,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Harvester Parts","Level_End",119,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Skull Key","Level_End",120,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Key Item: Sheet Music","Level_End",121,MedievilLocationCategory.PROGRESSION),

    # Runes

    MedievilLocationData("Chaos Rune: The Graveyard","Level_End",122,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Hilltop Mausoleum","Level_End",123,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Scarecrow Fields","Level_End",124,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Lake","Level_End",125,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Pumpkin Gorge","Level_End",126,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Sleeping Village","Level_End",127,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Pools of the Ancient Dead","Level_End",128,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Asylum Grounds","Level_End",129,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Haunted Ruins","Level_End",130,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: Ghost Ship","Level_End",131,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Chaos Rune: The Time Device","Level_End",132,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Earth Rune: The Graveyard","Level_End",133,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Hilltop Mausoleum","Level_End",134,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Scarecrow Fields","Level_End",135,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Crystal Caves","Level_End",136,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Lake","Level_End",137,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Pumpkin Gorge","Level_End",138,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Sleeping Village","Level_End",139,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Inside the Asylum","Level_End",140,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: Enchanted Earth","Level_End",141,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Haunted Ruins","Level_End",142,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Entrance Hall","Level_End",143,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Earth Rune: The Time Device","Level_End",144,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Moon Rune: The Hilltop Mausoleum","Level_End",145,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: Scarecrow Fields","Level_End",146,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: Pumpkin Gorge","Level_End",147,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: Ghost Ship","Level_End",148,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Moon Rune: The Time Device","Level_End",149,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Star Rune: Return to the Graveyard","Level_End",150,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: Dan's Crypt","Level_End",151,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: The Crystal Caves","Level_End",152,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: The Lake","Level_End",153,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: Enchanted Earth","Level_End",154,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: The Gallows Gauntlet","Level_End",155,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Star Rune: Ghost Ship","Level_End",156,MedievilLocationCategory.PROGRESSION),

    MedievilLocationData("Time Rune: The Lake","Level_End",157,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Time Rune: Pumpkin Gorge","Level_End",158,MedievilLocationCategory.PROGRESSION),
    MedievilLocationData("Time Rune: The Time Device","Level_End",159,MedievilLocationCategory.PROGRESSION),

    # LEVEL SPECIFIC DROPS

    # Dans Crypt
    MedievilLocationData("Gold Coins: Over the water","Level_End",160,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in DC","Level_End",161,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Daggers in DC","Level_End",162,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Behind Wall in Crypt - Left","Level_End",163,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Behind Wall in Crypt - Right","Level_End",164,MedievilLocationCategory.FUN),

    # The Graveyard
    MedievilLocationData("Gold Coins: Near Chaos Rune","Level_End",165,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Life Potion Left Chest","Level_End",166,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Life Potion Right Chest","Level_End",167,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Shop Chest","Level_End",168,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Near Hill Fountain","Level_End",169,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in GY","Level_End",170,MedievilLocationCategory.FUN),

    # Cemetery Hill
    MedievilLocationData("Gold Coins: Near Boulder Entrance","Level_End",171,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near Shop","Level_End",172,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in CH 1","Level_End",173,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Up Hill 1","Level_End",174,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in CH 2","Level_End",175,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Up Hill 2","Level_End",176,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in CH 3","Level_End",177,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Exit","Level_End",178,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Club in CH","Level_End",179,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in Arena","Level_End",180,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Arena","Level_End",181,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Arena","Level_End",182,MedievilLocationCategory.FUN),

    # Hilltop Mausoleum
    MedievilLocationData("Energy Vial: Right Coffin","Level_End",183,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Left Coffin","Level_End",184,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Club in HM Broken Benches","Level_End",185,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near Rune - Left Ramp","Level_End",186,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: After Earth Rune Door","Level_End",187,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Phantom of the Opera - Left","Level_End",188,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Phantom of the Opera - Right","Level_End",189,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Moon Room","Level_End",190,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Moon Room","Level_End",191,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Daggers in HM Block Puzzle","Level_End",192,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in HM Block Puzzle","Level_End",193,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Chest: Phantom of the Opera 1","Level_End",194,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Chest: Phantom of the Opera 2","Level_End",195,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Chest: Phantom of the Opera 3","Level_End",196,MedievilLocationCategory.FUN),

    # Return to the Graveyard
    MedievilLocationData("Gold Coins: Chest in Coffin Area 1","Level_End",197,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Coffin Area West","Level_End",198,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Coffin Area 2","Level_End",199,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Coffin Area 3","Level_End",200,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Coffin Area 4","Level_End",201,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Coffin Area East","Level_End",202,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Coffin Area 5","Level_End",203,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag above Coffin Area","Level_End",204,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag after Bridge","Level_End",205,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Below Shop","Level_End",206,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag at Shop","Level_End",207,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in RG Chest At Shop","Level_End",208,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag at Closed Gate","Level_End",209,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest on Island","Level_End",210,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Undertakers Entrance","Level_End",211,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Undertakers Entrance","Level_End",212,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Cliffs Right","Level_End",213,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Cliffs Left","Level_End",214,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Cliffs Left","Level_End",215,MedievilLocationCategory.FUN),

    # Scarecrow Fields

    MedievilLocationData("Gold Coins: Haystack at Beginning","Level_End",216,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Haystack near Moon Door","Level_End",217,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Left of fire near Moon Door","Level_End",218,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Right of fire near Moon Door","Level_End",219,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Club in SF Inside Hut","Level_End",220,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in SF Behind Windmill","Level_End",221,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in the Barn","Level_End",222,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in SF - Chest In the Barn","Level_End",223,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Cornfield Square near Barn","Level_End",224,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Cornfield Path 1","Level_End",225,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Cornfield Path","Level_End",226,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest Under Haybail","Level_End",227,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag under Barn Haybail","Level_End",228,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in the Press","Level_End",229,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in the Spinner","Level_End",230,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest next to Harvester Part","Level_End",231,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest Next to Chalice","Level_End",232,MedievilLocationCategory.FUN),
    
    # Anthill
    
    MedievilLocationData("Equipment: Club in AH Chest at Barrier","Level_End",234,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Barrier Fairy","Level_End",235,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot at Amber 2","Level_End",236,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot after Amber 2","Level_End",237,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Before Fairy 1","Level_End",238,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: After Amber 2","Level_End",239,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Fairy 2 Room Center","Level_End",240,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Fairy 2 Room Center","Level_End",241,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Fairy 2 Room Maggot","Level_End",242,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggots before Amber 4","Level_End",243,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggots at Amber 5","Level_End",244,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Fairy 3","Level_End",245,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggots at Amber 7 - 1","Level_End",246,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot in nest at Amber 7","Level_End",247,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot in Nest","Level_End",248,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Birthing room exit","Level_End",249,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot after Fairy 4","Level_End",250,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot after Fairy 4 in Nest","Level_End",251,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot at Fairy 5","Level_End",252,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot near Amber 9","Level_End",253,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Maggot near Shop","Level_End",254,MedievilLocationCategory.FUN),
    
    # Enchanted Earth
    
    MedievilLocationData("Gold Coins: Bag Near Tree Hollow","Level_End",256,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Behind Big Tree","Level_End",257,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest In Egg","Level_End",258,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Copper Shield in EE in Egg","Level_End",259,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag at Cave Entrance","Level_End",260,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Shadow Talisman Cave","Level_End",261,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins:Chest Near Barrier","Level_End",262,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest Left of Fountain","Level_End",263,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest Top of Fountain","Level_End",264,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest Right of Fountain","Level_End",265,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Left of Tree Drop","Level_End",266,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Right of Tree Drop","Level_End",267,MedievilLocationCategory.FUN),
    
    # The Sleeping Village
    MedievilLocationData("Gold Coins: Bag in Left Barrel at Blacksmith","Level_End",268,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Right Barrel at Blacksmith","Level_End",269,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in SV in Blacksmiths","Level_End",270,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag at Pond","Level_End",271,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: At Pond","Level_End",272,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Barrel at Inn","Level_End",273,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Barrel at bottom of Inn Stairs","Level_End",274,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Barrel Behind Inn Stairs","Level_End",275,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Club in SV Chest under Inn Stairs","Level_End",276,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Bust Switch","Level_End",277,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag In Top Bust Barrel","Level_End",278,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag In Switch Bust Barrel","Level_End",279,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Library","Level_End",280,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag at Top of table","Level_End",281,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag at Bottom of table","Level_End",282,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest next to Chalice","Level_End",283,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near Exit","Level_End",284,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near Chalice","Level_End",285,MedievilLocationCategory.FUN),
    
    # Pools of the Ancient Dead
    MedievilLocationData("Gold Coins: Bag at Entrance","Level_End",286,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Broken Structure near Entrance","Level_End",287,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag on Island Near Soul 2","Level_End",288,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Next to Lost Soul 3","Level_End",289,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near Gate","Level_End",290,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in PAD in Chest Near Soul 5","Level_End",291,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Chariot Right","Level_End",292,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Chariot Left","Level_End",293,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Jump Spot 1","Level_End",294,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Jump Spot 2","Level_End",295,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Jump Spot 1","Level_End",296,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Jump Spot 2","Level_End",297,MedievilLocationCategory.FUN),
    
    # The Lake
    MedievilLocationData("Energy Vial: Flooded House","Level_End",298,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Outside Flooded House","Level_End",299,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Near Closed Gate","Level_End",300,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in TL In Whirlpool","Level_End",301,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag at the Whirlpool Entrance","Level_End",302,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Whirpool Wind 1","Level_End",303,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Whirpool Wind 2","Level_End",304,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Whirlpool Wind 1","Level_End",305,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Whirlpool Wind 2","Level_End",306,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Outside Whirlpool Exit","Level_End",307,MedievilLocationCategory.FUN), 
    
    # The Crystal Caves
    MedievilLocationData("Gold Coins: Bag in Crystal at Start","Level_End",308,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Spinner","Level_End",309,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in CC in Crystal","Level_End",310,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag near Silver Shield","Level_End",311,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Crystal After Earth Door","Level_End",312,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Dragon Room 1 1st Platform","Level_End",313,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Dragon Room 1st Platform","Level_End",314,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Dragon Room 2 1st Platform","Level_End",315,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Dragon Room 1st Platform","Level_End",316,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Dragon Room 2nd Platform","Level_End",317,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Dragon Room 1 3rd Platform","Level_End",318,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Dragon Room 3rd Platform","Level_End",319,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Dragon Room 2 3rd Platform","Level_End",320,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Dragon Room 3rd Platform","Level_End",321,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Dragon Room 4th Platform 1","Level_End",322,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Dragon Room 4th Platform","Level_End",323,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Dragon Room 4th Platform 2","Level_End",324,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag on Left of Pool","Level_End",325,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag on Right of Pool","Level_End",326,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Crystal after Pool","Level_End",327,MedievilLocationCategory.FUN),
    
    # Gallows Gauntlet
    MedievilLocationData("Gold Coins: Bag Behind Stone Dragon 1","Level_End",328,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Behind Stone Dragon 2","Level_End",329,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in GG in Chest Near Exit","Level_End",330,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Serpent","Level_End",331,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest Near Star Entrance","Level_End",332,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near Chalice","Level_End",333,MedievilLocationCategory.FUN),
    
    # The Asylum Grounds
    MedievilLocationData("Gold Coins: Bag in Bell Grave Near Bell","Level_End",334,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Bell Grave Near Entrance","Level_End",335,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Near Shooting Statue","Level_End",336,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in AG in Chest Behind Door","Level_End",337,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Rat Grave","Level_End",338,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Behind Chaos Gate","Level_End",339,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Behind Elephant in Grave","Level_End",340,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near Bishop","Level_End",341,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Near King","Level_End",342,MedievilLocationCategory.FUN),
    
    #Inside the Asylum
    
    MedievilLocationData("Energy Vial: Bat Room","Level_End",343,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Bat Room Left","Level_End",344,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Bat Room","Level_End",345,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Bat Room Centre","Level_End",346,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in IA in Bat Room","Level_End",347,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Bat Room Right","Level_End",348,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Asylumn Room 1","Level_End",349,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Asylumn Room 2","Level_End",350,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Asylumn Room","Level_End",351,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Sewer Prison Entrance","Level_End",352,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag on Sewer Prison Bench","Level_End",353,MedievilLocationCategory.FUN),
    
    # Pumpkin Gorge
    MedievilLocationData("Equipment: Club in PG in Chest in Tunnel","Level_End",354,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Between Hidden Pumpkins","Level_End",355,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Coop 1","Level_End",356,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: In Coop","Level_End",357,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Coop 2","Level_End",358,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Coop 3","Level_End",359,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: In Moon Hut","Level_End",360,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Mushroom Area","Level_End",361,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Top of Hill","Level_End",362,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in PG in Chest at Top of Hill","Level_End",363,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Boulders After Star Rune","Level_End",364,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Boulders after Star Rune","Level_End",365,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Vine Patch Left","Level_End",366,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Vine Patch Right","Level_End",367,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest Near Chalice","Level_End",368,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Chalice Path","Level_End",369,MedievilLocationCategory.FUN),
    
    # Pumpkin Servent
    MedievilLocationData("Gold Coins: Bag Behind House","Level_End",370,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in PS in Chest near Leeches","Level_End",371,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Behind Vines and Pod","Level_End",372,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Left at Merchant Gargoyle","Level_End",373,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Merchant Gargoyle","Level_End",374,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Right at Merchant Gargoyle","Level_End",375,MedievilLocationCategory.FUN),
    
    # The Haunted Ruins
    MedievilLocationData("Gold Coins: Near First Set of farmers","Level_End",376,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Above Rune","Level_End",377,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Corner of Walls 1","Level_End",378,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in HR in Chest Near Rune Door","Level_End",379,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Corner of Walls 2","Level_End",380,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Corner of Walls 3","Level_End",381,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Up from Oil","Level_End",382,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Near Chalice North","Level_End",383,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag Near Chalice South","Level_End",384,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag in Crown Room","Level_End",385,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Catapult 1","Level_End",386,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Catapult 2","Level_End",387,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest at Catapult 3","Level_End",388,MedievilLocationCategory.FUN),
    
    # The Ghost Ship
    MedievilLocationData("Gold Coins: Bag in Rolling Barrels Room","Level_End",389,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in GS in Chest in Barrel Room","Level_End",390,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Bag on Deck At Barrels","Level_End",391,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: In Cabin","Level_End",392,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: In Cannon Room","Level_End",393,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Chest in Cannon Room","Level_End",394,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Rope Bridge 1","Level_End",395,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Rope Bridge 2","Level_End",396,MedievilLocationCategory.FUN),
    MedievilLocationData("Gold Coins: Rope Bridge","Level_End",397,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Club in GS in Chest at Captain","Level_End",398,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Cage Lift 1","Level_End",399,MedievilLocationCategory.FUN),
    MedievilLocationData("Energy Vial: Cage Lift 2","Level_End",400,MedievilLocationCategory.FUN),
    
    # The Entrance Hall
    # only has the chalice
    
    # Zaroks Lair
    MedievilLocationData("Equipment: Good Lightning","Level_End",401,MedievilLocationCategory.FUN),
    MedievilLocationData("Equipment: Silver Shield in ZL Arena","Level_End",402,MedievilLocationCategory.FUN)    
]
}

location_dictionary: Dict[str, MedievilLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})