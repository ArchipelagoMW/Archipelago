from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None

treasure_index_offset = 1
npc_index_offset = 10000
crystal_index_offset = 100000
#ability_index_offset = 1000000 Abilities Todo

def get_locations(player: Optional[int]) -> List[LocationData]:
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
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Stout Shield chest on ledge jump from tree", 50 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Cross trees and jump down Tincture chest", 38 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Tonic chest west of spawn", 1 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Tonic chest in cave NW of spawn", 2 + treasure_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Mountain summit jump on Nan Tonic Pouch chest", 1142 + treasure_index_offset),

        #NPCs
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Pouch Nan", 53 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb near Shaku", 627 + npc_index_offset), #Secret Herb 0
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Map Nan", 84 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Nan Stew", 14 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Butterfly Goo", 194 + npc_index_offset, lambda state: state.has('Item - Black Squirrel', player, 3)), #Tree Fairy NPC seems to have the dialogue for this (ID 194)
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree SW of spawn", 264 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree NW of spawn", 296 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree near lampposts", 110 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on Mario jump tree", 3085 + npc_index_offset),
        #Todo Secret Herb locations that don't seem to be used?
        #48, 112, -36
        #LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb 1", 297 + npc_index_offset),
        #79, 112, -30
        #LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb 2", 545 + npc_index_offset),
        #43, 104, -8
        #LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb 3", 546 + npc_index_offset),

        #Abilities Todo: descriptivize and implement
        #118, 109, 10
        #LocationData("Spawning Meadows", "Spawning Meadows Ability - Shaku from SFire_Summon", 477 + ability_index_offset),

        #Delende
        #Treasure chests
        LocationData("Delende", "Delende Chest - Money chest in front of camp", 263 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Money chest in front of fish hatchery lower level", 210 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Return from fish hatchery Bracer chest", 34 + treasure_index_offset),
        LocationData("Delende", "Delende Chest - Heart tarn Chartreuse chest", 1554 + treasure_index_offset, lambda state: state.has('Item - Progressive Salmon Violin', player) and state.has('Item - Owl Drum', player)),
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

        #Todo NPCs Missable: Astley1 NPC (ID 28) (184, 125, -93) gives you a Home Point Stone, but it's missable as a location; the item appears elsewhere later
        LocationData("Delende", "Delende NPC - Dog Bone in spooky cave", 1915 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dog Bone Guy", 31 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dog Bone south of Soiled Den", 184 + npc_index_offset),
        #276, 116, -204; gives you Fervor Charm
        LocationData("Delende", "Delende NPC - Dizzy noob chucks a Fervor Charm at your face", 831 + npc_index_offset),
        #Todo NPCs Shortcuts: shortcut girl (Z2_Collector Sister ID 3769 (169, 132, -89))
        #Todo NPCs Player Options: do we want a filter option to add the guy who fishes things up for you (Z2_FisherOnDock ID 121 (166, 133, -208))
        LocationData("Delende", "Delende NPC - Dizzy noob chucks a Fervor Charm at your face", 831 + npc_index_offset),
        #Todo: descriptivize (Z2_MapMan (198, 131, -74))
        LocationData("Delende", "Delende NPC - Cartographer", 1153 + npc_index_offset),
        #Todo NPCs Shortcuts: Rabbit Claws shortcut guy (Z2_RoosterFeetGuy ID 74(281, 128, -159))
        #Todo NPCs CheckOrNot: (Z2_RottenFishGuy ID 124 (181, 132, -200)) sells Rotten Salmon (progression item)

        #Grans House (Delende)
        #Treasure chests
        #126, 128, -58 style: blank
        LocationData("Delende", "Delende Chest - Grans House empty chest 1", 87 + treasure_index_offset),
        #127, 128, -58 style: weapon
        LocationData("Delende", "Delende Chest - Grans House empty chest 2", 100 + treasure_index_offset),
        #137, 128, -57 style: consumable
        LocationData("Delende", "Delende Chest - Grans House empty chest 3", 177 + treasure_index_offset),
        #137, 128, -56 style: consumable
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
        LocationData("Pale Grotto", "Pale Grotto Chest - Island Underpass Scrap chest", 3622 + treasure_index_offset, lambda state: state.has('Item - Progressive Salmon Violin', player)),
        LocationData("Pale Grotto", "Pale Grotto Chest - Island Z-Potion Pouch chest", 3077 + treasure_index_offset, lambda state: state.has('Item - Progressive Salmon Violin', player)),
        LocationData("Pale Grotto", "Pale Grotto Chest - Tincture chest tucked behind path to temple", 267 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Jumping puzzle Storm Helm chest", 226 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Money chest south of temple", 136 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Temple antechamber Toothpick chest", 222 + treasure_index_offset),
        LocationData("Pale Grotto", "Pale Grotto Chest - Temple sanctuary Pale Grotto Map chest", 1154 + treasure_index_offset),
        
        #NPCs
        #Todo NPCs Missable: Pale Grotto Temple map (Z2_ReidCamp ID 1166 (273, 122, -327)) gives you Ring Mail if you don't have it but it's missable (it's in shops)

        #Crystals
        LocationData("Pale Grotto", "Pale Grotto Crystal - Temple sanctuary Fencer Crystal", 130 + crystal_index_offset),

        #Seaside Cliffs
        #Treasure chests
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - north Clamshell chest across river from double giant box", 282 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Stonehenge Bracer chest", 150 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - ClamHaters Mulan jumping puzzle Clamshell chest", 268 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - ClamHaters Tincture Pouch chest after being made a man", 2981 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest south of ClamHater", 281 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Tonic chest south of Clamshell chest south of ClamHater", 286 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Climbing the seaside cliffs Potion chest", 42 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Three Amigos Tonic chest", 1161 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Three Amigos Scope Bit chest", 447 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Three Amigos Clamshell chest", 270 + treasure_index_offset),
        #310, 116, -68
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Money chest beneath encampment ledge", 217 + treasure_index_offset),
        #213, 107, 27
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Money chest on jigsaw mountain", 449 + treasure_index_offset),
        #307, 113, -22
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest in cliffs nook south of encampment", 80 + treasure_index_offset),
        #275,108,-28
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest below west Delende entrance", 273 + treasure_index_offset),
        #312, 95, 12
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest above the eastern beach standing stones", 274 + treasure_index_offset),
        #223, 94, 26
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest below jigsaw mountain", 275 + treasure_index_offset),
        #259, 107, -18
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Island Clamshell chest by the waterfalls", 277 + treasure_index_offset),
        #281, 98, -3
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest east of the river above the beach", 278 + treasure_index_offset),
        #302, 101, 4
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Clamshell chest along the eastern beach up the cliffs", 279 + treasure_index_offset),
        #250, 104, -13
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Parkour Fenix Juice chest by the island waterfalls", 289 + treasure_index_offset),
        #218, 107, 23
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Headgear chest on jigsaw mountain", 157 + treasure_index_offset),
        #289, 110, -18
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Jewel of Defense chest south of encampment on the canyon mountainside", 272 + treasure_index_offset),
        #250, 98, -4
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Tincture chest downstream of the island waterfalls", 288 + treasure_index_offset),
        #Seaside Cliffs Beach
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - The little mermaid Clamshell chest", 276 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Hop along the sea stacks to the Clamshell chest south of the peninsula", 280 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Peninsula Storm Cap chest past the standing stones jump puzzle", 205 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - MR SNIPS Fenix Juice chest", 287 + treasure_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Swimmers Top chest atop sea stack east of the bay", 450 + treasure_index_offset),
        #Seaside Cliffs Valley
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Rocky cove Clamshell chest down the lazy river", 269 + treasure_index_offset),
        
        #NPCs
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - ClamHater above the mist", 283 + npc_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - If you give a Manana Man a clam... (he will ask you for more)", 284 + npc_index_offset),
        #343, 81, 0
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - Diamond Ore below the bay", 2896 + npc_index_offset, lambda state: state.has('Item - Progressive Salmon Violin', player)),
        #Todo NPCs Job Masters: Seaside Cliffs Outpost map has Master Shaman ID 3572 (387, 155, -104); gives you Shaman Seal in exchange for job mastery

        #Draft Shaft Conduit
        #Treasure chests
        LocationData("Draft Shaft Conduit", "Draft Shaft Conduit Chest - Straight shot Torch chest", 82 + treasure_index_offset),
        LocationData("Draft Shaft Conduit", "Draft Shaft Conduit Chest - Ring around the rosy Tonic Pouch chest", 81 + treasure_index_offset),

        #Crystals
        LocationData("Draft Shaft Conduit", "Draft Shaft Conduit Crystal - Shaman Crystal", 35 + crystal_index_offset),

        #Mercury Shrine
        #Treasure chests
        LocationData("Mercury Shrine", "Mercury Shrine Chest - Pinnacle Contract chest", 155 + treasure_index_offset, lambda state: state.has('Item - Mercury Stone', player)),

        #Yamagawa M.A.
        #Treasure chests
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Money chest up first cliff", 2995 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Sneaky Broadsword chest behind tree", 91 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Iron Guard chest tucked next to waterfall", 95 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Dead-end Tonic chest", 3056 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Hidden stairway Tonic Pouch chest", 757 + treasure_index_offset),
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Drop down to mountain balcony Torpid Cuffs chest", 290 + treasure_index_offset),

        #NPCs
        LocationData("Yamagawa M.A.", "Yamagawa M.A. NPC - Autumns Oath at waterfall source", 628 + npc_index_offset, lambda state: state.has('Item - Progressive Salmon Violin', player)),
        #Todo NPCs Job Masters: Yamagawa M.A. Temple map has Master Scholar ID 3574 (59, 151, -98); gives you Scholar Seal in exchange for job mastery

        #Crystals
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Crystal - Jump into fireplace cave for Scholar Crystal", 166 + crystal_index_offset),

        #Proving Meadows
        #Treasure chests
        LocationData("Proving Meadows", "Proving Meadows Chest - Money chest next to trial guard", 207 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Battle Scythe chest along mountain behind waterfall", 258 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Burglars Glove chest hidden behind the inn", 118 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tincture Pouch chest along mountain", 2980 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tarzan Tonic chest", 256 + treasure_index_offset),
        LocationData("Proving Meadows", "Proving Meadows Chest - Tonic Pouch chest on the climb up outside Skumparadise", 193 + treasure_index_offset),

        #NPCs
        #Todo NPCs Blocker: this guy checks whether you have enough crystals to pass; this is a blocker guy not a location check guy
        #LocationData("Proving Meadows", "Proving Meadows NPC - Crystal Checker", 128 + npc_index_offset),

        #Skumparadise (we're smushing Trial Caves into there)
        #Treasure chests
        LocationData("Skumparadise", "Skumparadise Chest - Stairs are lava Stalwart Shield chest", 126 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Shroom-dodging Help the Prince chest", 120 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Ride the shroom Awake Ring chest", 670 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Wall niche Awake Ring chest", 671 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Smaller wall niche Tincture Pouch chest", 669 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Lava-loving shrooms Tonic Pouch chest", 684 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Mana Ring chest behind the lava shroom colonnade", 685 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - There and back again Sharp Sword chest", 683 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Tunnel Fenix Juice chest accompanied by a yellow flower", 1110 + treasure_index_offset),
        LocationData("Skumparadise", "Skumparadise Chest - Money chest behind boss", 332 + treasure_index_offset),

        #Crystals
        LocationData("Skumparadise", "Skumparadise Crystal - Aegis Crystal", 68 + crystal_index_offset),

        #Zones (Advanced)
        #Capital Sequoia (smushed Capital Courtyard in)
        #Treasure chests
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Tonic Pouch chest beyond the courtyard wall", 2671 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Inn room Craftwork Staff chest", 1388 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Second-story Craftwork Dagger chest by Master Rogue", 158 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Magic shop attic Craftwork Scythe chest", 1389 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Training ground parkour Craftwork Katana chest", 1390 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Cap chest behind Luxury Shop", 2651 + treasure_index_offset),
        #Todo Rules: next three chests require the Luxury Key: Fenix Syrup Pouch (1533), Lucky Briefs (1532), Lucky Socks (1531) and Progressive Luxury Pass
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Fenix Syrup Pouch chest locked in Luxury Shop storage", 1533 + treasure_index_offset, lambda state: state.has('Item - Luxury Key', player)),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Lucky Briefs chest locked in Luxury Shop storage", 1532 + treasure_index_offset, lambda state: state.has('Item - Luxury Key', player)),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Lucky Socks chest locked in Luxury Shop storage", 1531 + treasure_index_offset, lambda state: state.has('Item - Luxury Key', player)),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Inn attic Craftwork Vest chest by Master Monk", 2656 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Shield chest by Master Warrior atop the Luxury Shop", 2655 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Sword chest atop library bookcases", 1392 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Penguin sanctuary Craftwork Robe chest", 2654 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shard chest 1 in Gaea Shrine", 137 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shard chest 2 in Gaea Shrine", 227 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shard chest 3 in Gaea Shrine", 381 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shard chest 4 in Gaea Shrine", 548 + treasure_index_offset),
        #Next check can be acquired with either Owl, Ibek, Quintar, or Gaea Stone; vanilla expects Gaea Stone so that's the logic we're using
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Bow chest in Clerics Lounge", 1391 + treasure_index_offset, lambda state: state.has('Item - Gaea Stone', player)),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Axe chest in instrducktor classroom", 1387 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Watering Can chest in Master Warlocks chambers atop Weapons R Us", 2732 + treasure_index_offset, lambda state: state.has('Item - Ibek Bell', player)),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Pages chest in Master Wizards Library atop Weapons R Us", 168 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Fenced-off Craftwork Helm chest in Armor Merchant alley", 2653 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Rapier chest beneath grand staircase", 1393 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Fang Pendant chest tucked into maze entrance hedge", 389 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Wand chest down left maze path", 452 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Hop the moat to maze Craftwork Spear chest", 863 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Maze Craftwork Crown chest accompanied by blue flower pair", 390 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gardeners Key chest below Lost Penguin", 388 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Cheat at maze for Givers Ring chest above fountain", 387 + treasure_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Craftwork Mail chest in Gardeners Shed", 2652 + treasure_index_offset, lambda state: state.has('Item - Gardeners Key', player)),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Tuber Seed 1 in Gardeners Shed", 2663 + treasure_index_offset, lambda state: state.has('Item - Gardeners Key', player)),
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Tuber Seed 2 in Gardeners Shed", 2664 + treasure_index_offset, lambda state: state.has('Item - Gardeners Key', player)),

        #NPCs 
        #Todo NPCs Missable: Courtyard Chloe (Z37_ChloeFishing ID 1661 (399, 155, -219)) gives you Fly Lure (and later she disappears and it's on the ground here)
        #Todo NPCs Missable: Courtyard Reid (Z28_Reid ID 2410 (113, 172, -372)) gives you a Courtyard Key or if you miss it it's on the ground (Z37_Courtyard Key ID 2486 (424, 150, -222))
        #Todo NPCs Job Masters: Master Beatsmith ID 3560 (361, 170, -268); gives you Beatsmith Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Cleric ID 3568 (363, 166, -266); gives you Cleric Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Monk ID 3567 (394, 179, -295); gives you Monk Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Rogue ID 3571 (444, 167, -264); gives you Rogue Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Warlock ID 3570 (400, 171, -267); gives you Warlock Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Warrior ID 3566 (424, 182, -293); gives you Warrior Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Wizard ID 3569 (391, 168, -266); gives you Wizard Seal in exchange for job mastery
        #Todo NPCs CheckOrNot: Z14_Duck_HomePointStone ID 560 (403, 161, -265) gives you a Home Point Stone if you don't have one
        #Todo NPCs Blocker: Z14_ProgressionGate ID 3823 (403, 180, -367) requires 18 crystals; we think it's an original-randomizer-only NPC blocking the way to the castle
        #Todo Rules: requires 6 crystals and descriptivize; blocker guy who wants 6 crystals to give you Luxury Pass and entry to Luxury Store
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Artisan Guard", 1162 + npc_index_offset),
        #Todo: (417, 171, -299) descriptivize
        #Todo Rules: requires Z14_LuxuryStolen variable key, which is set when Z14_StoreRoomProxFlag ID 1530 (425, 175, -295) is triggered by PlayerProximity
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Luxury Key Guy", 1529 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Plug Lure sparkling in the fountain", 2584 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin on a tent", 605 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Speedy Lost Penguin on patrol", 584 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin kiosk keeper", 508 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin skulking in shop alley", 565 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin on gender change bench porch", 1095 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin enjoying inn hospitality", 946 + npc_index_offset),
        #Todo Multichecks: 5 checks on the Penguin Keeper
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Penguin Keeper", 531 + npc_index_offset),
        #Next seven checks can be acquired by either Owl, Ibek, Quintar, or Gaea Stone; vanilla game expects Gaea Stone so that's the logic we're using
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin trampling the Clerics flowers", 564 + npc_index_offset, lambda state: state.has('Item - Gaea Stone', player)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Sadist Sam eats(?) Cerberus", 536 + npc_index_offset, lambda state: state.has('Item - Gaea Stone', player)), #name is ca69011a in Crystal Edit whyy lmao
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin wandering the Magic Shop rooftop garden", 573 + npc_index_offset, lambda state: state.has('Item - Gaea Stone', player)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin atop sewer exit rooftop", 567 + npc_index_offset, lambda state: state.has('Item - Gaea Stone', player)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin cheating at Garden Maze", 421 + npc_index_offset, lambda state: state.has('Item - Gaea Stone', player)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - How did you climb that tree, Lost Penguin", 422 + npc_index_offset, lambda state: state.has('Item - Gaea Stone', player)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin among the eaves of Library roof", 594 + npc_index_offset, lambda state: state.has('Item - Gaea Stone', player)),
        #Todo: descriptivize (440, 171, -296)
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Library Scholar", 1948 + npc_index_offset),

        #Crystals
        LocationData("Capital Sequoia", "Capital Sequoia Crystal - Beatsmith Crystal", 1087 + crystal_index_offset, lambda state: state.has('Item - Ibek Bell', player)),

        #Abilities
        #Todo: descriptivize and implement
        #376, 178, -345 (Capital Sequoia (Maze) map)
        #LocationData("Capital Sequoia", "Capital Sequoia Ability - Niltsi from SWind_Summon", 1109 + ability_index_offset),

        #Jojo Sewers
        #Treasure chests
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Guarded Tonic Pouch chest hiding in the grass", 743 + treasure_index_offset),
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Money chest in drowned passage to Boomer Society", 634 + treasure_index_offset),
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Tincture Pouch in the shadow of the waterfall", 1126 + treasure_index_offset),
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Leap of faith Smelly Gi chest", 887 + treasure_index_offset),
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Iron Helm chest in eastside sewer green room", 2658 + treasure_index_offset),
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Invisible maze Iron Armor chest", 744 + treasure_index_offset),

        #NPCs
        LocationData("Jojo Sewers", "Jojo Sewers NPC - Who even wants Stone of Jordan these days", 2759 + npc_index_offset),

        #Boomer Society
        #Treasure chests
        LocationData("Boomer Society", "Boomer Society Chest - Gospel chest in log cabin", 2667 + treasure_index_offset),
        LocationData("Boomer Society", "Boomer Society Chest - Boomer Society map chest on second floor of log cabin", 2909 + treasure_index_offset),

        #NPCs
        LocationData("Boomer Society", "Boomer Society NPC - Nice Allowance Lady", 476 + npc_index_offset),
        LocationData("Boomer Society", "Boomer Society NPC - Treasury Grandpa", 547 + npc_index_offset),

        #Rolling Quintar Fields
        #Treasure chests
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Potion chest south of east gate", 826 + treasure_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Fenix Juice chest in Chevy divot south of east gate", 828 + treasure_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Hunting Axe chest deep in the Quintar cave", 817 + treasure_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Sneaky Potion chest behind tree", 829 + treasure_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Hunting Bow chest deep in the eastern Quintar cave", 745 + treasure_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Money chest at the end of the road", 825 + treasure_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Tonic Pouch chest hidden beneath the end of the road", 2674 + treasure_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Money chest west of and above sneaky Potion chest", 338 + treasure_index_offset, lambda state: state.has('Item - Quintar Flute', player)),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Pinnacle Tincture Pouch chest with a short and tall box friend", 471 + treasure_index_offset, lambda state: state.has('Item - Quintar Flute', player)),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Treetop Spore Blocker chest west of Quintar Sanctum", 365 + treasure_index_offset, lambda state: state.has('Item - Quintar Flute', player)),

        #NPCs
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Silver Dust beneath overhang in eastern Quintar cave crevasse", 2678 + npc_index_offset),
        #Todo NPCs Multichecks: 2 checks on Quintar Enthusiast
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Quintar Enthusiast (always pet Buttermint)", 464 + npc_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Silver Ingot in Quintar cave beneath the end of the road", 454 + npc_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Silver Ore behind Quintar Nest befriending a stack of boxes", 323 + npc_index_offset, lambda state: state.has('Item - Quintar Flute', player)),

        #Quintar Nest
        #Treasure chests
        LocationData("Quintar Nest", "Quintar Nest Chest - West Donut Lake sprinkle Money chest", 883 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - East Donut Lake sprinkle Ether chest", 884 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - Jumping puzzle Fenix Juice chest above the donut", 756 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - Northwest Donut Lake sprinkle Potion chest", 432 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - Welcome Potion chest", 3078 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - Mighty jump to the Scope Bit chest along the east side wall", 746 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - Static Rod chest north of the sewers", 638 + treasure_index_offset, lambda state: state.has('Item - Quintar Flute', player)),
        LocationData("Quintar Nest", "Quintar Nest Chest - North Donut Lake sprinkle Tincture chest", 852 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - Hop along the west side wall to Tincture Pouch chest", 2982 + treasure_index_offset),
        LocationData("Quintar Nest", "Quintar Nest Chest - Donut Lake crown sprinkle Tonic chest", 851 + treasure_index_offset),

        #NPCs
        #Todo NPCs CheckOrNot: two Quintar Eggs here
        LocationData("Quintar Nest", "Quintar Nest NPC - Eastside Silver Dust come on down to the water", 711 + npc_index_offset),
        LocationData("Quintar Nest", "Quintar Nest NPC - South of sewers Silver Ingot", 850 + npc_index_offset),
        LocationData("Quintar Nest", "Quintar Nest NPC - Silver Ore on the way out", 755 + npc_index_offset),

        #Crystals
        LocationData("Quintar Nest", "Quintar Nest Crystal - Hunter Crystal", 621 + crystal_index_offset),

        #Quintar Sanctum
        #Treasure chests
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - West wall big bounce Money chest", 810 + treasure_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - Bounce field Fenix Juice chest", 969 + treasure_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - Quintar Sanctum map chest in front of the shrine", 2910 + treasure_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - Western Tincture Pouch chest at ground level", 2983 + treasure_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - Northern Tonic Pouch chest at ground level", 593 + treasure_index_offset),
        #Technically this one is in Overpass (2nd Overpass Scrap chest in main map's list)
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - Lonely Overpass Scrap chest above Quintar Sanctum", 3533 + treasure_index_offset),

        #NPCs
        #Todo NPCs CheckOrNot: Quintar Egg here (on Quintar Sanctum Mushroom map)
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Silver Dust going back down", 802 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Silver Dust almost to the top", 965 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Mushroom bounce Silver Ingot", 411 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Silver Ingot beneath the shroom", 801 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - East side Silver Ore (Do not look down)", 737 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Big bounce Silver Ore", 754 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Two Toads bestow Princess Toadstool", 963 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Two Toads crown Bowsette", 964 + npc_index_offset),

        #Crystals
        LocationData("Quintar Sanctum", "Quintar Sanctum Crystal - Chemist Crystal (of course this is in the shroom zone)", 810 + crystal_index_offset),

        #Capital Jail
        #Treasure chests
        LocationData("Capital Jail", "Capital Jail Chest - Touchdown South Wing Key chest", 640 + treasure_index_offset),
        LocationData("Capital Jail", "Capital Jail Chest - West Wing Key chest in South Wing jail cell across from busted wall", 930 + treasure_index_offset, lambda state: state.has('Item - South Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - Haunted jail cell East Wing Key chest in South Wing dead end", 931 + treasure_index_offset, lambda state: state.has('Item - South Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - Fiercely guarded Cell Key chest locked behind the South Wing rubble", 990 + treasure_index_offset, lambda state: state.has('Item - South Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail Chest - Fiercely guarded Iron Rod chest locked behind the South Wing rubble", 2668 + treasure_index_offset, lambda state: state.has('Item - South Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail Chest - Battleplate chest locked behind the South Wing rubble", 991 + treasure_index_offset, lambda state: state.has('Item - South Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        #Technically in the Underpass but you come from here
        LocationData("Capital Jail", "Capital Jail Chest - Drop down behind the South Wing rubble Underpass Scrap chest", 3675 + treasure_index_offset, lambda state: state.has('Item - South Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail Chest - Cell Key chest in West Wing jail cell among the glowy plants", 925 + treasure_index_offset, lambda state: state.has('Item - West Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - West Wing arrow plants Battle Helm chest", 923 + treasure_index_offset, lambda state: state.has('Item - West Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - West Wing Cell Key chest locked among the foliage", 916 + treasure_index_offset, lambda state: state.has('Item - West Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail Chest - Twinsies empty chest in East Wing bedroom closet", 2999 + treasure_index_offset, lambda state: state.has('Item - East Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - Twinsies Potion chest in East Wing bedroom closet", 906 + treasure_index_offset, lambda state: state.has('Item - East Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - Twinsies Cell Key top chest in waterlogged East Wing hallway", 676 + treasure_index_offset, lambda state: state.has('Item - East Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - Twinsies Cell Key bottom chest in waterlogged East Wing hallway", 707 + treasure_index_offset, lambda state: state.has('Item - East Wing Key', player)),

        LocationData("Capital Jail", "Capital Jail Chest - Cell Key chest locked in broken East Wing jail cell", 708 + treasure_index_offset, lambda state: state.has('Item - East Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail Chest - Cell Key chest locked in East Wing bedroom", 763 + treasure_index_offset, lambda state: state.has('Item - East Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail Chest - Dark Wing Key chest locked beyond overgrown West Wing hallway", 909 + treasure_index_offset, lambda state: state.has('Item - West Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail Chest - Capital Jail map chest in Dark Wing entry left cell", 2911 + treasure_index_offset, lambda state: state.has('Item - Dark Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - Sneaky Woven Hood chest in Dark Wing", 929 + treasure_index_offset, lambda state: state.has('Item - Dark Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail Chest - Corner lava jump Woven Shirt chest in Dark Wing", 920 + treasure_index_offset, lambda state: state.has('Item - Dark Wing Key', player)),

        #NPCs
        LocationData("Capital Jail", "Capital Jail NPC - Silver Ingot in haunted South Wing jail cell", 972 + npc_index_offset, lambda state: state.has('Item - South Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail NPC - Silver Ingot in zombified South Wing jail cell", 989 + npc_index_offset, lambda state: state.has('Item - South Wing Key', player)),
        LocationData("Capital Jail", "Capital Jail NPC - Silver Ore locked in broken East Wing jail cell accompanied by blue flower", 760 + npc_index_offset, lambda state: state.has('Item - East Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail NPC - Silver Dust locked in East Wing bedroom", 782 + npc_index_offset, lambda state: state.has('Item - East Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail NPC - Silver Ore locked in overgrown West Wing hallway", 759 + npc_index_offset, lambda state: state.has('Item - West Wing Key', player) and state.has('Item - Cell Key', player, 6)),
        LocationData("Capital Jail", "Capital Jail NPC - Silver Dust in Dark Wing entry right cell", 472 + npc_index_offset, lambda state: state.has('Item - Dark Wing Key', player)),

        #Crystals
        LocationData("Capital Jail", "Capital Jail Crystal - Reaper Crystal above hell pool", 908 + crystal_index_offset),

        #Capital Pipeline
        #Treasure chests
        LocationData("Capital Pipeline", "Capital Pipeline Chest - I wanna go home Capital Pipeline map chest", 2912 + treasure_index_offset, lambda state: state.has('Item - Ibek Bell', player)),
        LocationData("Capital Pipeline", "Capital Pipeline Chest - Lucky Platter chest (Do not anger the fungus)", 1294 + treasure_index_offset),

        #NPCs
        LocationData("Capital Pipeline", "Capital Pipeline NPC - Silver Ingot in corrupted tunnel", 2660 + npc_index_offset),
        LocationData("Capital Pipeline", "Capital Pipeline NPC - Silver Ore in corrupted tunnel", 1295 + npc_index_offset),
        LocationData("Capital Pipeline", "Capital Pipeline NPC - Diamond Dust down the elevator into Jidamba", 2897 + npc_index_offset, lambda state: state.has('Item - Ibek Bell', player)),

        #Cobblestone Crag
        #Treasure chests
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Ether Pouch chest behind the sluice gate", 479 + treasure_index_offset),
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Long jump Potion chest", 382 + treasure_index_offset, lambda state: state.has('Item - Quintar Flute', player)),
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Potion Pouch chest tucked in a cranny between two tall spikes", 1119 + treasure_index_offset),
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - I totally meant to miss that jump Skewer chest", 2670 + treasure_index_offset),
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Tonic Pouch chest upon exiting from Quintar Nest", 478 + treasure_index_offset),
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Could really use a Walking Stick (chest) right about now...", 2669 + treasure_index_offset),
        #Technically on Underpass (Okimoto) map
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Underpass Scrap chest on the way to the village hidden among the leaves", 3669 + treasure_index_offset, lambda state: state.has('Item - Quintar Flute', player)),

        #NPCs
        LocationData("Cobblestone Crag", "Cobblestone Crag NPC - Westernmost Silver Dust", 1120 + npc_index_offset),

        #Okimoto N.S.
        #Treasure chests
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Moth love lamp (Butterfly chest)", 364 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Dont bump your head Ether Pouch chest", 2661 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Parkour to the west for Float Shoes chest", 337 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Potion chest is just kinda in there, its not special", 356 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Tanto chest east of save point", 344 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Money chest on yashiki balcony", 690 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Art of War chest down hidden stairs in library", 686 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Magic Finder chest in the east ground floor room", 2673 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Potion Pouch chest lurking behind the bookcase", 434 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Tachi chest past the hidden staircase", 694 + treasure_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Dance above the koi pond Training Gi chest", 1103 + treasure_index_offset),

        #NPCs
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Silver Dust on the way up", 359 + npc_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Why does a room like this exist (Silver Dust)", 692 + npc_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Eastern Silver Ingot atop pond box", 689 + npc_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Silver Ingot behind the room that shall not be named", 691 + npc_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Silver Ore atop the yashiki", 2659 + npc_index_offset),
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Lets get down to business western Silver Ore", 429 + npc_index_offset),
        #Technically 3rd Overpass Scrap in Overpass main map
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Overpass Scrap", 3534 + npc_index_offset),

        #Crystals
        LocationData("Okimoto N.S.", "Okimoto N.S. Crystal - Ninja Crystal", 699 + crystal_index_offset),

        #Greenshire Reprise
        #Treasure chests
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Jump off bridge 4 Ambush Knife chest", 483 + treasure_index_offset, lambda state: state.has('Item - Ibek Bell', player)),
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Ether chest atop the waterfalls", 490 + treasure_index_offset),
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Jump off bridge 3 Looters Ring chest", 482 + treasure_index_offset, lambda state: state.has('Item - Ibek Bell', player)),
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Tall taunter Shell Amulet chest", 373 + treasure_index_offset, lambda state: state.has('Item - Ibek Bell', player)),
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Tincture Pouch chest in the valley of trees", 487 + treasure_index_offset),
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Tonic Pouch chest at the tip of the peninsula south of the second bridge", 491 + treasure_index_offset),

        #NPCs
        LocationData("Greenshire Reprise", "Greenshire Reprise NPC - Jump down from the second bridge to the Silver Ore fallen in north crack", 485 + npc_index_offset),
        LocationData("Greenshire Reprise", "Greenshire Reprise NPC - Silver Dust across the first bridge hiding in a crack", 486 + npc_index_offset),
        LocationData("Greenshire Reprise", "Greenshire Reprise NPC - The furthest southern edge Silver Ingot", 474 + npc_index_offset),

        #Salmon Pass
        #Treasure chests
        LocationData("Salmon Pass", "Salmon Pass Chest - Riverbank Paypirbak chest among the yellow flowers", 2700 + treasure_index_offset),
        LocationData("Salmon Pass", "Salmon Pass Chest - Fenix Juice chest across a bridge and around through a tunnel", 2420 + treasure_index_offset),
        LocationData("Salmon Pass", "Salmon Pass Chest - Fenix Juice chest admiring the hidden waterfall", 419 + treasure_index_offset),

        #Salmon River
        #Treasure chests
        LocationData("Salmon River", "Salmon River Chest - Hop on Money chest once you have become frogger", 1264 + treasure_index_offset),
        LocationData("Salmon River", "Salmon River Chest - Bloodbind chest atop river island crown", 1297 + treasure_index_offset),
        LocationData("Salmon River", "Salmon River Chest - Money chest also wishes to be frogger", 325 + treasure_index_offset),
        LocationData("Salmon River", "Salmon River Chest - Ether Pouch chest in the stands of the Salmon race finish line ", 2976 + treasure_index_offset),
        LocationData("Salmon River", "Salmon River Chest - Salmon River Map chest inside the Salmon Shack", 2913 + treasure_index_offset),

        #NPCs
        #Todo Missable NPCs: figure out Courtyard Key Reid (see Capital Sequoia)

        #Crystals
        #Technically in River Cat's Ego map
        LocationData("Salmon River", "Salmon River Crystal - Appease the QuizFish Nomad Crystal", 630 + treasure_index_offset),


        #Overpass
        #Treasure chests
        #The last Underpass Scrap chest on main map has been categorized under the Capital Jail
        #The Underpass (Okimoto) map's Underpass Scrap has been categorized under Cobblestone Crag

        #Underpass
        #Treasure chests
        #2nd Overpass Scrap chest on main map has been categorized under the Quintar Sanctum
        #3rd Overpass Scrap chest on main map has been categorized under the Okimoto N.S.

        #Zones (Expert)
        #Shoudu Waterfront
        #Treasure chests
        LocationData("Shoudu Waterfront", "Shoudu Waterfront Chest - Money chest along the water", 2419 + treasure_index_offset),
        LocationData("Shoudu Waterfront", "Shoudu Waterfront Chest - Hop around Empty chest", 3690 + treasure_index_offset),
        LocationData("Shoudu Waterfront", "Shoudu Waterfront Chest - Hop around Mars Stone chest", 1114 + treasure_index_offset),

        #Lake Delende
        #Treasure chests
        LocationData("Lake Delende", "Lake Delende Chest - Float Shoes chest on north edge", 1263 + treasure_index_offset),
        LocationData("Lake Delende", "Lake Delende Chest - Lake Delende map chest on north edge", 2917 + treasure_index_offset),

        #Jidamba Eaclaneya
        #NPCs
        #1 Diamond Dust NPC on Jidamba Eaclaneya Fish Floor map has been categorized under the Capital Pipeline

    ]

    return location_table