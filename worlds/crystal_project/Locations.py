from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]

    treasure_index_offset = 1
    npc_index_offset = 10000

def get_locations(world: "CrystalProjectWorld") -> List[LocationData]:
    #Todo include crystals/job locations, NPC gifts, key items like squirrels, ore
    location_table: List[LocationData] = [
        #Treasure chests
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Money chest on cliff north of spawn", 101 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Money chest under overpass", 292 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Jump on Nan Burglars Glove chest", 41 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Cedar Staff chest above waterfall", 17 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Cedar Wand chest behind Nan house", 61 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Island Cleaver chest", 54 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Jump on secret tunnel chest Fenix Juice chest", 5 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Fenix Juice chest on path to Delende", 49 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Secret tunnel Stabbers chest", 47 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Stout Shield Chest on ledge jump from tree", 50 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Cross trees and jump down Tincture chest", 38 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Tonic chest west of spawn", 1 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Tonic chest in cave NW of spawn", 2 + treasure_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows Chest - Mountain summit jump on Nan Tonic Pouch chest", 1142 + treasure_index_offset),

        #NPCs
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Pouch Nan", 53 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Secret herb near Shaku", 627 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Map Nan", 84 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Nan Stew", 14 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Butterfly Goo", 194 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Buttersquirrel on tree SW of spawn", 264 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Buttersquirrel on tree NW of spawn", 296 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Buttersquirrel on tree near lampposts", 110 + npc_index_offset),
        LocationData("Spawning Meadow", "Spawning Meadows NPC - Buttersquirrel on Mario jump tree", 3085 + npc_index_offset),



    ]

    return location_table