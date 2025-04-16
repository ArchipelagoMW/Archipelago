from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]

treasure_index_offset = 1
npc_index_offset = 10000
crystal_index_offset = 100000

def get_locations(world: "CrystalProjectWorld") -> List[LocationData]:
    #Todo include crystals/job locations, NPC gifts, key items like squirrels, ore
    location_table: List[LocationData] = [
        #Zones (Beginner)
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
        #Treasure chests
        #126, 128, -58
        LocationData("Delende", "Delende Chest - Grans House empty chest 1", 87 + treasure_index_offset),
        #127, 128, -58
        LocationData("Delende", "Delende Chest - Grans House empty chest 2", 100 + treasure_index_offset),
        #137, 128, -57
        LocationData("Delende", "Delende Chest - Grans House empty chest 3", 177 + treasure_index_offset),
        #137, 128, -56
        LocationData("Delende", "Delende Chest - Grans House empty chest 4", 178 + treasure_index_offset),

        #Basement (Somehow Not Delende)
        #Treasure chests
        LocationData("Delende", "Delende Chest - Empty chest in basement", 179 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Digested Head chest in basement", 180 + treasure_index_offset),

        #Soiled Den
        #Treasure chests
        #311, 111, -96
        LocationData("Soiled Den", "Soiled Den Chest - Clamshell chest lurking in the shadows by the Bangler", 218 + treasure_index_offset),
        #322, 111, -101
        LocationData("Soiled Den", "Soiled Den Chest - Clamshell chest by the Bangler", 271 + treasure_index_offset),
        #326, 111, -116
        LocationData("Soiled Den", "Soiled Den Chest - Long river jump Dodge Charm chest", 448 + treasure_index_offset),
        #249, 116, -156
        LocationData("Soiled Den", "Soiled Den Chest - Riverside Tonic Pouch chest", 1155 + treasure_index_offset),

        #NPCs
        #296, 112, -155
        LocationData("Soiled Den", "Soiled Den NPC - Dog Bone among the bones and flowers", 176 + npc_index_offset),

        #Pale Grotto
        #Treasure chests
        #316, 120, -262
        LocationData("Pale Grotto", "Pale Grotto Chest - Ring around the rosy Fenix Juice chest", 228 + treasure_index_offset),
        #307, 124, -345
        LocationData("Pale Grotto", "Pale Grotto Chest - Poisonkiss chest north from save point", 144 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Entrance river hop Tonic chest", 229 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Tincture Pouch chest on promontory", 2979 + treasure_index_offset),
        #Todo: the next two checks require Salmon
        LocationData("Pale Grotto", "Pale Grotto Chest - Island Underpass Scrap chest", 3622 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Island Z-Potion Pouch chest", 3077 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Tincture chest tucked behind path to temple", 267 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Jumping puzzle Storm Helm chest", 226 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Money chest south of temple", 136 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Temple antechamber Toothpick chest", 222 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Temple sanctuary Pale Grotto Map chest", 1154 + treasure_index_offset),
        
        #Crystals
        LocationData("Pale Grotto", "Pale Grotto Chest - Temple sanctuary Fencer Crystal", 130 + crystal_index_offset),

        #Seaside Cliffs
        #Treasure chests
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - north Clamshell chest across river from double giant box", 282 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Stonehenge Bracer chest", 150 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - ClamHaters Mulan jumping puzzle Clamshell chest", 268 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - ClamHaters Tincture Pouch chest after being made a man", 2981 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest south of ClamHater", 281 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Tonic chest south of Clamshell chest south of ClamHater", 286 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Climbing the seaside cliffs Potion chest", 42 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Encampment freebie Tonic chest of the three amigos", 1161 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Encampment freebie Scope Bit chest of the three amigos", 447 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Encampment freebie Clamshell chest of the three amigos", 270 + treasure_index_offset),

        #NPCs
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - ClamHater above the mist", 283 + npc_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - Encampment ClamLover Manananananana Man", 284 + npc_index_offset),


        #Proving Meadows
        #Treasure chests
        LocationData("Proving Meadows", "Proving Meadows Chest - Money chest next to trial guard", 207 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Battle Scythe chest along mountain behind waterfall", 258 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Burglars Glove chest hidden behind the inn", 118 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tincture Pouch chest along mountain", 2980 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tarzan Tonic chest", 256 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tonic Pouch chest on the climb up outside Skumparadise", 193 + treasure_index_offset),

        #Yamagawa M.A.
        #Treasure chests
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Money chest up first cliff", 2995 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Sneaky Broadsword chest behind tree", 91 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Iron Guard chest tucked next to waterfall", 95 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Dead-end Tonic chest", 3056 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Hidden stairway Tonic Pouch chest", 757 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Drop down to mountain balcony Torpid Cuffs chest", 290 + treasure_index_offset),

        #NPCs
        #Todo: this requires Salmon
        LocationData("Yamagawa M.A.", "Yamagawa M.A. NPC - Autumns Oath at waterfall source", 628 + npc_index_offset),

        #Crystals
        LocationData("Yamagawa M.A.", "Yamagawa M.A. NPC - Jump into fireplace cave for Scholar Crystal", 166 + crystal_index_offset),

        #Zones (Expert)
        #Lake Delende
        #Treasure chests
        LocationData("Lake Delende", "Lake Delende Chest - Float Shoes chest on north edge", 1263 + treasure_index_offset),
        LocationData("Lake Delende", "Lake Delende Chest - Lake Delende map chest on north edge", 2917 + treasure_index_offset),

    ]

    return location_table