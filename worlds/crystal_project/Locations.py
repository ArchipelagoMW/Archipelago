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
        #Spawning Meadows
        #Treasure chests
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Money chest on cliff north of spawn", 101 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Money chest under overpass", 292 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Jump on Nan Burglars Glove chest", 41 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Cedar Staff chest above waterfall", 17 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Cedar Wand chest behind Nan house", 61 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Island Cleaver chest", 54 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Jump on secret tunnel chest Fenix Juice chest", 5 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Fenix Juice chest on path to Delende", 49 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Secret tunnel Stabbers chest", 47 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Stout Shield Chest on ledge jump from tree", 50 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Cross trees and jump down Tincture chest", 38 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Tonic chest west of spawn", 1 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Tonic chest in cave NW of spawn", 2 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Mountain summit jump on Nan Tonic Pouch chest", 1142 + treasure_index_offset),

        #NPCs
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Pouch Nan", 53 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret herb near Shaku", 627 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Map Nan", 84 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Nan Stew", 14 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Butterfly Goo", 194 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree SW of spawn", 264 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree NW of spawn", 296 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree near lampposts", 110 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on Mario jump tree", 3085 + npc_index_offset),

        #Delende
        #Treasure chests
        LocationData("Delende", "Delende Chest - Money chest in front of camp", 263 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Money chest in front of fish hatchery lower level", 210 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Return from fish hatchery Bracer chest", 34 + treasure_index_offset),
        #Todo: add something to Rules.py; can't get Chartreuse without Owl + Salmon
        LocationData("Delende", "Delende Chest - Heart tarn Chartreuse chest", 1554 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Mushroom underpass Cotton Hood chest", 262 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Fallen log parkour Earring chest", 208 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Earring chest across river", 213 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Underground Ether chest next to river", 43 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Fenix Juice chest under ambush tree", 212 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Iron Sword chest on west mountainside", 209 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Across river from fish hatchery Looters Ring chest", 123 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Mages Robe chest high up west mountainside", 33 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Up near hatchery Protect Amulet chest", 169 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Storm Hood chest outside spooky cave", 27 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Tincture chest in fish hatchery", 39 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Fish hatchery approach Tincture chest ", 79 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Tincture chest under tree", 261 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Top of spooky cave Tincture Pouch chest", 73 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Troll Tincture Pouch chest", 451 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Tonic chest off north path", 259 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Tonic Pouch chest before Proving Meadows", 216 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Tonic Pouch chest in front of fish hatchery below tree", 2997 + treasure_index_offset),

        #NPCs
        LocationData("Delende", "Delende NPC - Dog Bone in spooky cave", 1915 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dog Bone Guy", 31 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dog Bone south of Soiled Den", 184 + npc_index_offset),

        #Grans House (Delende)
        #Treasure chests - Todo: get descriptions for empty chest locations
        #126, 128, -58
        LocationData("Delende", "Delende Chest - Empty chest", 87 + treasure_index_offset),
        #127, 128, -58
        LocationData("Delende", "Delende Chest - Empty chest", 100 + treasure_index_offset),
        #137, 128, -57
        LocationData("Delende", "Delende Chest - Empty chest", 177 + treasure_index_offset),
        #137, 128, -56
        LocationData("Delende", "Delende Chest - Empty chest", 178 + treasure_index_offset),

        #Soiled Den (Delende)
        #NPCs
        #Todo: 3rd dog bone here

        #Proving Meadows
        #Treasure chests
        LocationData("Proving Meadows", "Proving Meadows Chest - Money chest next to trial guard", 207 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Battle Scythe chest along mountain behind waterfall", 258 + treasure_index_offset),
        #Todo: check where Burglars Glove chest is
        LocationData("Proving Meadows", "Proving Meadows Chest - Burglars Glove chest", 118 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tincture Pouch chest along mountain", 2980 + treasure_index_offset),
        #Todo: check where Tonic chest is
        LocationData("Proving Meadows", "Proving Meadows Chest - Tonic chest ", 256 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tonic Pouch chest on the climb up outside Skumparadise", 193 + treasure_index_offset),




    ]

    return location_table