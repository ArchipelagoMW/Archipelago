from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState
from .Options import CrystalProjectOptions
from .rules import CrystalProjectLogic

class LocationData(NamedTuple):
    region: str
    name: str
    code: Optional[int]
    rule: Optional[Callable[[CollectionState], bool]] = None

treasure_index_offset = 1
npc_index_offset = 10000
crystal_index_offset = 100000
#summon_index_offset = 1000000 Summons Todo

def get_locations(player: Optional[int], options: Optional[CrystalProjectOptions]) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    #Todo include crystals/job locations, NPC gifts, key items like squirrels, ore
    location_table: List[LocationData] = [
        #Zones (Beginner)
        #Spawning Meadows
        #Treasure chests
        LocationData("Spawning Meadows", "Spawning Meadows Chest - On cliff north of spawn", 101 + treasure_index_offset), #Money chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Under overpass", 292 + treasure_index_offset), #Money chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Jump on Nan", 41 + treasure_index_offset), #Burglars Glove chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Above waterfall", 17 + treasure_index_offset), #Cedar Staff chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Behind Nan house", 61 + treasure_index_offset), #Cedar Wand chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Island", 54 + treasure_index_offset), #Cleaver chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Jump on secret tunnel chest", 5 + treasure_index_offset), #Fenix Juice chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - On path to Delende", 49 + treasure_index_offset), #Fenix Juice chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Secret tunnel", 47 + treasure_index_offset), #Stabbers chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - On ledge jump from tree", 50 + treasure_index_offset), #Stout Shield chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Cross trees and jump down", 38 + treasure_index_offset), #Tincture chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - West of spawn", 1 + treasure_index_offset), #Tonic chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - In cave NW of spawn", 2 + treasure_index_offset), #Tonic chest
        LocationData("Spawning Meadows", "Spawning Meadows Chest - Mountain summit jump on Nan", 1142 + treasure_index_offset), #Tonic Pouch chest

        #NPCs
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Pouch Nan", 53 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb near Shaku", 627 + npc_index_offset), #Secret Herb 0
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Map Nan", 84 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Nan Stew", 14 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Butterfly Goo", 194 + npc_index_offset, lambda state: state.has("Item - Black Squirrel", player, 3)), #Tree Fairy NPC seems to have the dialogue for this (ID 194)
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree SW of spawn", 264 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree NW of spawn", 296 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on tree near lampposts", 110 + npc_index_offset),
        LocationData("Spawning Meadows", "Spawning Meadows NPC - Buttersquirrel on Mario jump tree", 3085 + npc_index_offset),
        #Todo Secret Herb locations that don"t seem to be used?
        #LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb 1", 297 + npc_index_offset), #(48, 112, -36)
        #LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb 2", 545 + npc_index_offset), #(79, 112, -30)
        #LocationData("Spawning Meadows", "Spawning Meadows NPC - Secret Herb 3", 546 + npc_index_offset), #(43, 104, -8)

        #Summons Todo: descriptivize and implement
        #LocationData("Spawning Meadows", "Spawning Meadows Summon - Shaku from SFire_Summon", 477 + summon_index_offset), #(118, 109, 10)

        #Delende
        #Treasure chests
        LocationData("Delende", "Delende Chest - In front of camp", 263 + treasure_index_offset), #Money chest
        LocationData("Delende", "Delende Chest - In front of fish hatchery lower level", 210 + treasure_index_offset), #Money chest
        LocationData("Delende", "Delende Chest - Return from fish hatchery", 34 + treasure_index_offset), #Bracer chest
        LocationData("Delende", "Delende Chest - Heart tarn", 1554 + treasure_index_offset, logic.has_swimming and logic.has_glide), #Chartreuse chest
        LocationData("Delende", "Delende Chest - Mushroom underpass", 262 + treasure_index_offset), #Cotton Hood chest
        LocationData("Delende", "Delende Chest - Fallen log parkour", 208 + treasure_index_offset), #Earring chest
        LocationData("Delende", "Delende Chest - Across river", 213 + treasure_index_offset), #Earring chest
        LocationData("Delende", "Delende Chest - Next to river", 43 + treasure_index_offset), #Underground Ether chest
        LocationData("Delende", "Delende Chest - Under ambush tree", 212 + treasure_index_offset), #Fenix Juice chest
        LocationData("Delende", "Delende Chest - On west mountainside", 209 + treasure_index_offset), #Iron Sword chest
        LocationData("Delende", "Delende Chest - Across river from fish hatchery", 123 + treasure_index_offset), #Looters Ring chest
        LocationData("Delende", "Delende Chest - High up west mountainside", 33 + treasure_index_offset), #Mages Robe chest
        LocationData("Delende", "Delende Chest - Up near hatchery", 169 + treasure_index_offset), #Protect Amulet chest
        LocationData("Delende", "Delende Chest - Outside spooky cave", 27 + treasure_index_offset), #Storm Hood chest
        LocationData("Delende", "Delende Chest - In fish hatchery", 39 + treasure_index_offset), #Tincture chest
        LocationData("Delende", "Delende Chest - Fish hatchery approach", 79 + treasure_index_offset), #Tincture chest
        LocationData("Delende", "Delende Chest - Under tree", 261 + treasure_index_offset), #Tincture chest
        LocationData("Delende", "Delende Chest - Top of spooky cave", 73 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Delende", "Delende Chest - Troll", 451 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Delende", "Delende Chest - Off north path", 259 + treasure_index_offset), #Tonic chest
        LocationData("Delende", "Delende Chest - Before Proving Meadows", 216 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Delende", "Delende Chest - In front of fish hatchery below tree", 2997 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Delende", "Overpass Chest - Dead tree by Fencers Keep", 3537 + treasure_index_offset, logic.has_vertical_movement), #(148, 151, -114) 6th Overpass Scrap on Overpass main map

        #NPCs
        LocationData("Delende", "Delende NPC - Astley gives you a home point stone", 28 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dog Bone in spooky cave", 1915 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dog Bone Guy", 31 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dog Bone south of Soiled Den", 184 + npc_index_offset),
        LocationData("Delende", "Delende NPC - Dizzy noob chucks something at your face", 831 + npc_index_offset), #(276, 116, -204); Fervor Charm
        #Todo NPCs Shortcuts: shortcut girl (Z2_Collector Sister ID 3769 (169, 132, -89))
        #Todo NPCs Player Options: do we want a filter option to add the guy who fishes things up for you (Z2_FisherOnDock ID 121 (166, 133, -208))
        #Todo NPCs CheckOrNot: guy who gives you a map of Delende if you don't have one (Z2_MapMan (198, 131, -74))
        #LocationData("Delende", "Delende NPC - Cartographer", 1153 + npc_index_offset),
        #Todo NPCs Shortcuts: Rabbit Claws shortcut guy (Z2_RoosterFeetGuy ID 74(281, 128, -159))
        #Todo NPCs CheckOrNot: (Z2_RottenFishGuy ID 124 (181, 132, -200)) sells Rotten Salmon (progression item)

        #Grans House (Delende)
        #Treasure chests
        LocationData("Delende", "Delende Chest - Grans House 1", 87 + treasure_index_offset), #(126, 128, -58) style: blank
        LocationData("Delende", "Delende Chest - Grans House 2", 100 + treasure_index_offset), #(127, 128, -58) style: weapon
        LocationData("Delende", "Delende Chest - Grans House 3", 177 + treasure_index_offset), #(137, 128, -57) style: consumable
        LocationData("Delende", "Delende Chest - Grans House 4", 178 + treasure_index_offset), #(137, 128, -56) style: consumable

        #Basement (Somehow Not Delende)
        #Treasure chests
        LocationData("Delende", "Basement Chest - Gran...?", 179 + treasure_index_offset), #Empty chest
        LocationData("Delende", "Basement Chest - Gran......?", 180 + treasure_index_offset), #Digested Head chest
        LocationData("Delende", "Underpass Chest - Cracks in Grans foundation", 3653 + treasure_index_offset), #(126, 115, -102) Basement map chest
        LocationData("Delende", "Underpass Chest - Grans subbasement pair 1", 181 + treasure_index_offset), #(129, 98, -111) Fenix Juice Pouch chest
        LocationData("Delende", "Underpass Chest - Grans subbasement pair 2", 182 + treasure_index_offset), #(128, 98, -111) Plate of Wolf chest
        LocationData("Delende", "Underpass Chest - Grans subbasement loner", 3671 + treasure_index_offset), #(119, 98, -110) Underpass Scrap
        
        #Soiled Den
        #Treasure chests
        LocationData("Soiled Den", "Soiled Den Chest - Lurking in the shadows by the Bangler", 218 + treasure_index_offset), #(311, 111, -96) Clamshell chest
        LocationData("Soiled Den", "Soiled Den Chest - By the Bangler", 271 + treasure_index_offset), #(322, 111, -101) Clamshell chest
        LocationData("Soiled Den", "Soiled Den Chest - Long river jump", 448 + treasure_index_offset), #(326, 111, -116) Dodge Charm chest
        LocationData("Soiled Den", "Soiled Den Chest - Riverside", 1155 + treasure_index_offset), #(249, 116, -156) Tonic Pouch chest

        #NPCs
        #296, 112, -155
        LocationData("Soiled Den", "Soiled Den NPC - Dog Bone among the bones and flowers", 176 + npc_index_offset),

        #Pale Grotto
        #Treasure chests
        LocationData("Pale Grotto", "Pale Grotto Chest - Across from fish island", 228 + treasure_index_offset), #(#316, 120, -262) Fenix Juice chest
        LocationData("Pale Grotto", "Pale Grotto Chest - North from save point", 144 + treasure_index_offset), #(307, 124, -345) Poisonkiss chest
        LocationData("Pale Grotto", "Pale Grotto Chest - Entrance river hop", 229 + treasure_index_offset), #Tonic chest
        LocationData("Pale Grotto", "Pale Grotto Chest - On promontory", 2979 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Pale Grotto", "Pale Grotto Chest - Island 1", 3622 + treasure_index_offset, logic.has_swimming), #Underpass Scrap chest; somehow this is actually in the pale grotto and not the underpass
        LocationData("Pale Grotto", "Pale Grotto Chest - Island 2", 3077 + treasure_index_offset, logic.has_swimming), #Z-Potion Pouch chest
        LocationData("Pale Grotto", "Pale Grotto Chest - Tucked behind path to temple", 267 + treasure_index_offset), #Tincture chest
        LocationData("Pale Grotto", "Pale Grotto Chest - Jumping puzzle", 226 + treasure_index_offset), #Storm Helm chest
        LocationData("Pale Grotto", "Pale Grotto Chest - South of temple", 136 + treasure_index_offset), #Money chest
        LocationData("Pale Grotto", "Pale Grotto Chest - Temple antechamber", 222 + treasure_index_offset), #Toothpick chest
        LocationData("Pale Grotto", "Pale Grotto Chest - Temple sanctuary", 1154 + treasure_index_offset), #Pale Grotto map chest
        LocationData("Pale Grotto", "Underpass Chest - Blue flower ledge between Pale Grotto & Soiled Den", 3621 + treasure_index_offset, logic.has_swimming), #(245, 116, -199) Underpass Scrap chest
        
        #NPCs
        #Todo NPCs Missable: Pale Grotto Temple map (Z2_ReidCamp ID 1166 (273, 122, -327)) gives you Ring Mail if you don"t have it but it"s missable (it"s in shops)

        #Crystals
        LocationData("Pale Grotto", "Pale Grotto Crystal - Fencer", 130 + crystal_index_offset),

        #Seaside Cliffs
        #Treasure chests
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - North across river from double giant box", 282 + treasure_index_offset), #Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Stonehenge", 150 + treasure_index_offset), #Bracer chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - ClamHaters Mulan jumping puzzle", 268 + treasure_index_offset), #Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - After ClamHater made a man out of you", 2981 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - South of ClamHater", 281 + treasure_index_offset), #Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - South of chest south of ClamHater", 286 + treasure_index_offset), #Tonic chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Climbing the seaside cliffs", 42 + treasure_index_offset), #Potion chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Three Amigos Uno", 1161 + treasure_index_offset), #Tonic chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Three Amigos Dos", 447 + treasure_index_offset), #Scope Bit chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Three Amigos Tres", 270 + treasure_index_offset), #Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Beneath encampment ledge", 217 + treasure_index_offset), #(310, 116, -68) Money chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - On jigsaw mountain", 449 + treasure_index_offset), #(213, 107, 27) Money chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - In cliffs nook south of encampment", 80 + treasure_index_offset), #(307, 113, -22) Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Below west Delende entrance", 273 + treasure_index_offset), #(275,108,-28) Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Above the eastern beach standing stones", 274 + treasure_index_offset), #(312, 95, 12) Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Below jigsaw mountain", 275 + treasure_index_offset), #(223, 94, 26) Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Island by the waterfalls", 277 + treasure_index_offset), #(259, 107, -18) Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - East of the river above the beach", 278 + treasure_index_offset), #(281, 98, -3) Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Along the eastern beach up the cliffs", 279 + treasure_index_offset), #(302, 101, 4) Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Parkour by the island waterfalls", 289 + treasure_index_offset), #(250, 104, -13) Fenix Juice chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - On jigsaw mountain", 157 + treasure_index_offset), #(218, 107, 23) Headgear chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - South of encampment on the canyon mountainside", 272 + treasure_index_offset), #(289, 110, -18) Jewel of Defense chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Downstream of the island waterfalls", 288 + treasure_index_offset), #(250, 98, -4) Tincture chest
        #Seaside Cliffs Beach
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - The little mermaid", 276 + treasure_index_offset), #Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Hop along the sea stacks south of the peninsula", 280 + treasure_index_offset), #Clamshell chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Peninsula past the standing stones jump puzzle", 205 + treasure_index_offset), #Storm Cap chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - MR SNIPS", 287 + treasure_index_offset), #Fenix Juice chest
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Atop sea stack east of the bay", 450 + treasure_index_offset), #Swimmers Top chest
        #Seaside Cliffs Valley
        LocationData("Seaside Cliffs", "Seaside Cliffs Chest - Rocky cove down the lazy river", 269 + treasure_index_offset), #Clamshell chest
        
        #NPCs
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - ClamHater above the mist", 283 + npc_index_offset),
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - If you give a Manana Man a clam... (he will ask you for more)", 284 + npc_index_offset, logic.has_enough_clamshells),
        LocationData("Seaside Cliffs", "Seaside Cliffs NPC - Diamond below the bay", 2896 + npc_index_offset, logic.has_swimming), #(343, 81, 0) Ore
        #Todo NPCs Job Masters: Seaside Cliffs Outpost map has Master Shaman ID 3572 (387, 155, -104); gives you Shaman Seal in exchange for job mastery

        #Draft Shaft Conduit
        #Treasure chests
        LocationData("Draft Shaft Conduit", "Draft Shaft Conduit Chest - Straight shot", 82 + treasure_index_offset), #Torch chest
        LocationData("Draft Shaft Conduit", "Draft Shaft Conduit Chest - Ring around the rosy", 81 + treasure_index_offset), #Tonic Pouch chest

        #Crystals
        LocationData("Draft Shaft Conduit", "Draft Shaft Conduit Crystal - Shaman", 35 + crystal_index_offset),

        #Mercury Shrine
        #Treasure chests
        LocationData("Mercury Shrine", "Mercury Shrine Chest - Pinnacle", 155 + treasure_index_offset, lambda state: state.has("Item - Mercury Stone", player)), #Contract chest

        #Yamagawa M.A.
        #Treasure chests
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Up first cliff", 2995 + treasure_index_offset), #Money chest
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Sneaky behind tree", 91 + treasure_index_offset), #Broadsword chest
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Tucked next to waterfall", 95 + treasure_index_offset), #Iron Guard chest
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Dead end", 3056 + treasure_index_offset), #Tonic chest
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Hidden stairway", 757 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Chest - Drop down to mountain balcony", 290 + treasure_index_offset), #Torpid Cuffs chest

        #NPCs
        LocationData("Yamagawa M.A.", "Yamagawa M.A. NPC - Hidden inside waterfall source", 628 + npc_index_offset, logic.has_swimming), #Autumns Oath
        #Todo NPCs Job Masters: Yamagawa M.A. Temple map has Master Scholar ID 3574 (59, 151, -98); gives you Scholar Seal in exchange for job mastery

        #Crystals
        LocationData("Yamagawa M.A.", "Yamagawa M.A. Crystal - Jump into fireplace cave for Scholar", 166 + crystal_index_offset),

        #Proving Meadows
        #Treasure chests
        LocationData("Proving Meadows", "Proving Meadows Chest - Next to trial guard", 207 + treasure_index_offset), #Money chest
        LocationData("Proving Meadows", "Proving Meadows Chest - Along mountain behind waterfall", 258 + treasure_index_offset), #Battle Scythe chest
        LocationData("Proving Meadows", "Proving Meadows Chest - Hidden behind the inn", 118 + treasure_index_offset), #Burglars Glove chest
        LocationData("Proving Meadows", "Proving Meadows Chest - Along mountain", 2980 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Proving Meadows", "Proving Meadows Chest - Tarzan", 256 + treasure_index_offset), #Tonic chest
        LocationData("Proving Meadows", "Proving Meadows Chest - On the climb up outside Skumparadise", 193 + treasure_index_offset), #Tonic Pouch chest

        #NPCs
        #Todo NPCs Blocker: this guy checks whether you have enough crystals to pass; this is a blocker guy not a location check guy
        #LocationData("Proving Meadows", "Proving Meadows NPC - Crystal Checker", 128 + npc_index_offset),

        #Skumparadise (we"re smushing Trial Caves into there)
        #Treasure chests
        LocationData("Skumparadise", "Skumparadise Chest - Stairs are lava", 126 + treasure_index_offset), #Stalwart Shield chest
        LocationData("Skumparadise", "Skumparadise Chest - Shroom dodging", 120 + treasure_index_offset), #Help the Prince chest
        LocationData("Skumparadise", "Skumparadise Chest - Ride the shroom", 670 + treasure_index_offset), #Awake Ring chest
        LocationData("Skumparadise", "Skumparadise Chest - Wall niche", 671 + treasure_index_offset), #Awake Ring chest
        LocationData("Skumparadise", "Skumparadise Chest - Smaller wall niche", 669 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Skumparadise", "Skumparadise Chest - Lava-loving shrooms", 684 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Skumparadise", "Skumparadise Chest - Behind the lava shroom colonnade", 685 + treasure_index_offset), #Mana Ring chest
        LocationData("Skumparadise", "Skumparadise Chest - There and back again", 683 + treasure_index_offset), #Sharp Sword chest
        LocationData("Skumparadise", "Skumparadise Chest - Accompanied by yellow flower in tunnel", 1110 + treasure_index_offset), #Fenix Juice chest
        LocationData("Skumparadise", "Skumparadise Chest - Behind boss", 332 + treasure_index_offset), #Money chest

        #Crystals
        LocationData("Skumparadise", "Skumparadise Crystal - Aegis", 68 + crystal_index_offset),

        #Zones (Advanced)
        #Capital Sequoia (smushed Capital Courtyard in)
        #Treasure chests
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Beyond the courtyard wall", 2671 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Inn room", 1388 + treasure_index_offset), #Craftwork Staff chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Second story by Master Rogue", 158 + treasure_index_offset), #Craftwork Dagger chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Magic shop attic", 1389 + treasure_index_offset), #Craftwork Scythe chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Training ground parkour", 1390 + treasure_index_offset), #Craftwork Katana chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Behind Luxury Shop", 2651 + treasure_index_offset), #Craftwork Cap chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Locked in Luxury Shop storage 1", 1533 + treasure_index_offset, lambda state: state.has("Item - Luxury Key", player) and state.has_any({"Item - Progressive Luxury Pass"}, player)), #Fenix Syrup Pouch chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Locked in Luxury Shop storage 2", 1532 + treasure_index_offset, lambda state: state.has("Item - Luxury Key", player) and state.has_any({"Item - Progressive Luxury Pass"}, player)), #Lucky Briefs chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Locked in Luxury Shop storage 3", 1531 + treasure_index_offset, lambda state: state.has("Item - Luxury Key", player) and state.has_any({"Item - Progressive Luxury Pass"}, player)), #Lucky Socks chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Inn attic by Master Monk", 2656 + treasure_index_offset), #Craftwork Vest chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - By Master Warrior atop the Luxury Shop", 2655 + treasure_index_offset), #Craftwork Shield chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Atop library bookcases", 1392 + treasure_index_offset), #Craftwork Sword chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Penguin sanctuary", 2654 + treasure_index_offset), #Craftwork Robe chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shrine 1", 137 + treasure_index_offset), #Gaea Shard chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shrine 2", 227 + treasure_index_offset), #Gaea Shard chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shrine 3", 381 + treasure_index_offset), #Gaea Shard chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gaea Shrine 4", 548 + treasure_index_offset), #Gaea Shard chest
        #Next check can be acquired with either Owl, Ibek, Quintar, or Gaea Stone; vanilla expects Gaea Stone so thats the logic were using
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Clerics Lounge", 1391 + treasure_index_offset, lambda state: state.has("Item - Gaea Stone", player)), #Craftwork Bow chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Instrducktor classroom", 1387 + treasure_index_offset), #Craftwork Axe chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Master Warlocks chambers atop Weapons R Us", 2732 + treasure_index_offset, logic.has_vertical_movement), #Watering Can chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Master Wizards Library atop Weapons R Us", 168 + treasure_index_offset), #Craftwork Pages chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Fenced off in Armor Merchant alley", 2653 + treasure_index_offset), #Craftwork Helm chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Beneath grand staircase", 1393 + treasure_index_offset), #Craftwork Rapier chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Tucked into maze entrance hedge", 389 + treasure_index_offset), #Fang Pendant chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Down left maze path", 452 + treasure_index_offset), #Craftwork Wand chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Hop moat to maze", 863 + treasure_index_offset), #Craftwork Spear chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Accompanied by blue flower pair in maze", 390 + treasure_index_offset), #Craftwork Crown chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Below maze-cheating Lost Penguin", 388 + treasure_index_offset), #Gardeners Key chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Above maze fountain", 387 + treasure_index_offset), #Givers Ring chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gardeners Shed 1", 2652 + treasure_index_offset, lambda state: state.has("Item - Gardeners Key", player)), #Craftwork Mail chest
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gardeners Shed 2", 2663 + treasure_index_offset, lambda state: state.has("Item - Gardeners Key", player)), #Tuber Seed
        LocationData("Capital Sequoia", "Capital Sequoia Chest - Gardeners Shed 3", 2664 + treasure_index_offset, lambda state: state.has("Item - Gardeners Key", player)), #Tuber Seed

        #NPCs 
        #Todo NPCs Missable: Courtyard Chloe (Z37_ChloeFishing ID 1661 (399, 155, -219)) gives you Fly Lure (and later she disappears and it"s on the ground here)
        #Todo NPCs Missable: Courtyard Reid (Z28_Reid ID 2410 (113, 172, -372)) gives you a Courtyard Key or if you miss it it"s on the ground (Z37_Courtyard Key ID 2486 (424, 150, -222))
        #Todo NPCs Job Masters: Master Beatsmith ID 3560 (361, 170, -268); gives you Beatsmith Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Cleric ID 3568 (363, 166, -266); gives you Cleric Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Monk ID 3567 (394, 179, -295); gives you Monk Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Rogue ID 3571 (444, 167, -264); gives you Rogue Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Warlock ID 3570 (400, 171, -267); gives you Warlock Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Warrior ID 3566 (424, 182, -293); gives you Warrior Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Wizard ID 3569 (391, 168, -266); gives you Wizard Seal in exchange for job mastery
        #Todo NPCs CheckOrNot: Z14_Duck_HomePointStone ID 560 (403, 161, -265) gives you a Home Point Stone if you don"t have one
        #Todo NPCs Blocker: Z14_ProgressionGate ID 3823 (403, 180, -367) requires 18 crystals; we think it"s an original-randomizer-only NPC blocking the way to the castle
        #Todo NPCs Blocker Missable and Multichecks: luxury store guard; won't give you check 1 if you already have Luxury Pass or check 2 if you have V2
        #LocationData("Capital Sequoia", "Capital Sequoia NPC - Artisan Guard 1", 1162 + npc_index_offset, lambda state: logic.has_jobs(state, 6)), #(419, 171, -289)
        #LocationData("Capital Sequoia", "Capital Sequoia NPC - Artisan Guard 2", 1162 + npc_index_offset, lambda state: logic.has_jobs(state, 15)), #(419, 171, -289)
        #Todo NPCs Missable: requires Z14_LuxuryStolen variable key, which is set when Z14_StoreRoomProxFlag ID 1530 (425, 175, -295) is triggered by PlayerProximity; if you already have Luxury Key, he won't give you anything
        #LocationData("Capital Sequoia", "Capital Sequoia NPC - Luxury Key Thief", 1529 + npc_index_offset), #(417, 171, -299)
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Sparkling in the fountain", 2584 + npc_index_offset), #Plug Lure
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin on a tent", 605 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Speedy Lost Penguin on patrol", 584 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin kiosk keeper", 508 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin skulking in shop alley", 565 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin on gender change bench porch", 1095 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin enjoying inn hospitality", 946 + npc_index_offset),
        # Progressive Location: 5 checks on the Penguin Keeper, must add a progressive location in the C# app every time you use one of these.
        # The original check the corresponds to the npc id should be last so that when when it completes it stops showing up on your minimap.
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Penguin Keeper", 531 + 50000 + npc_index_offset, lambda state: state.has("Item - Lost Penguin", player, 3)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Penguin Keeper 2", 531 + 50001 + npc_index_offset, lambda state: state.has("Item - Lost Penguin", player, 6)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Penguin Keeper 3", 531 + 50002 + npc_index_offset, lambda state: state.has("Item - Lost Penguin", player, 9)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Penguin Keeper 4", 531 + npc_index_offset, lambda state: state.has("Item - Lost Penguin", player, 12)),
        #Next seven checks can be acquired by either Owl, Ibek, Quintar, or Gaea Stone; vanilla game expects Gaea Stone so thats the logic were using
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin trampling Clerics flowers", 564 + npc_index_offset, lambda state: state.has("Item - Gaea Stone", player)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Give Sadist Sam head(s)", 536 + npc_index_offset), #name is ca69011a in Crystal Edit whyy lmao
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin wandering Magic Shop rooftop garden", 573 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin atop sewer exit rooftop", 567 + npc_index_offset, lambda state: state.has("Item - Gaea Stone", player)),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Lost Penguin cheating at Garden Maze", 421 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - How did you climb that tree, Lost Penguin?", 422 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Library roof Lost Penguin", 594 + npc_index_offset),
        LocationData("Capital Sequoia", "Capital Sequoia NPC - Library Morii of the East!", 1948 + npc_index_offset), #(440, 171, -296) Z14_Library Scholar

        #Crystals
        LocationData("Capital Sequoia", "Capital Sequoia Crystal - Beatsmith", 1087 + crystal_index_offset, logic.has_vertical_movement),

        #Summons
        #Todo: descriptivize and implement
        #376, 178, -345 (Capital Sequoia (Maze) map)
        #LocationData("Capital Sequoia", "Capital Sequoia Summon - Niltsi from SWind_Summon", 1109 + summon_index_offset),

        #Jojo Sewers
        #Treasure chests
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Hiding in the guarded grass", 743 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Drowned passage to Boomer Society", 634 + treasure_index_offset), #Money chest
        LocationData("Jojo Sewers", "Jojo Sewers Chest - In the shadow of the waterfall", 1126 + treasure_index_offset), #Tincture Pouch
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Leap of faith", 887 + treasure_index_offset), #Smelly Gi chest
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Eastside sewer green room", 2658 + treasure_index_offset), #Iron Helm chest
        LocationData("Jojo Sewers", "Jojo Sewers Chest - Invisible maze", 744 + treasure_index_offset), #Iron Armor chest
        LocationData("Jojo Sewers", "Underpass Chest - Walking the plank above Pale Grotto waterfall", 3670 + treasure_index_offset, logic.has_swimming), #(337, 155, -319) Underpass Scrap chest

        #NPCs
        LocationData("Jojo Sewers", "Jojo Sewers NPC - Who even wants Stone of Jordan these days?", 2759 + npc_index_offset),

        #Boomer Society
        #Treasure chests
        LocationData("Boomer Society", "Boomer Society Chest - Log cabin", 2667 + treasure_index_offset), #Gospel chest
        LocationData("Boomer Society", "Boomer Society Chest - 2nd floor of log cabin", 2909 + treasure_index_offset), #Boomer Society map chest

        #NPCs
        LocationData("Boomer Society", "Boomer Society NPC - Nice Allowance Lady", 476 + npc_index_offset),
        LocationData("Boomer Society", "Boomer Society NPC - Treasury Grandpa", 547 + npc_index_offset),

        #Rolling Quintar Fields
        #Treasure chests
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - South of east gate", 826 + treasure_index_offset), #Potion chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Chevy divot south of east gate", 828 + treasure_index_offset), #Fenix Juice chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Deep in Quintar cave", 817 + treasure_index_offset), #Hunting Axe chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Sneaky chest behind tree", 829 + treasure_index_offset), #Potion chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Deep in eastern Quintar cave", 745 + treasure_index_offset), #Hunting Bow chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - At the end of the road", 825 + treasure_index_offset), #Money chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Hidden beneath end of the road", 2674 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - West of and above sneaky chest", 338 + treasure_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #Money chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Pinnacle by short and tall box friends", 471 + treasure_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #Tincture Pouch chest
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields Chest - Treetop west of Quintar Sanctum", 365 + treasure_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #Spore Blocker chest
        LocationData("Rolling Quintar Fields", "Overpass Chest - Climb the mountain east of Quintar Sanctum", 3532 + treasure_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #1st Overpass Scrap chest on main Overpass map

        #NPCs
        #Todo NPCs CheckOrNot: two Quintar Eggs
        #Todo NPCs CheckOrNot: Crystal Checker guy gives you Quintar Pass for having enough crystals; doesn't if you already have the Quintar Pass
        #LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Quintar Stable Owner crystal checker for Quintar Pass if you refuse to touch an eyeball", 375 + npc_index_offset, lambda state: logic.has_jobs(state, 7)),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Silver beneath overhang in eastern Quintar cave crevasse", 2678 + npc_index_offset), #Dust
        #Todo NPCs Multichecks: 2 checks on Quintar Enthusiast
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Quintar Enthusiast (always pet Buttermint)", 464 + npc_index_offset),
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Silver in Quintar cave beneath the end of the road", 454 + npc_index_offset), #Ingot
        LocationData("Rolling Quintar Fields", "Rolling Quintar Fields NPC - Silver behind Quintar Nest befriending a stack of boxes", 323 + npc_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #Ore

        #Quintar Nest
        #Treasure chests
        LocationData("Quintar Nest", "Quintar Nest Chest - West Donut Lake sprinkle", 883 + treasure_index_offset), #Money chest
        LocationData("Quintar Nest", "Quintar Nest Chest - East Donut Lake sprinkle", 884 + treasure_index_offset), #Ether chest
        LocationData("Quintar Nest", "Quintar Nest Chest - Jumping puzzle above the donut", 756 + treasure_index_offset), #Fenix Juice chest
        LocationData("Quintar Nest", "Quintar Nest Chest - Northwest Donut Lake sprinkle", 432 + treasure_index_offset), #Potion chest
        LocationData("Quintar Nest", "Quintar Nest Chest - Welcome", 3078 + treasure_index_offset), #Potion chest
        LocationData("Quintar Nest", "Quintar Nest Chest - Mighty jump along east side wall", 746 + treasure_index_offset), #Scope Bit chest
        LocationData("Quintar Nest", "Quintar Nest Chest - North of sewers", 638 + treasure_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #Static Rod chest
        LocationData("Quintar Nest", "Quintar Nest Chest - North Donut Lake sprinkle", 852 + treasure_index_offset), #Tincture chest
        LocationData("Quintar Nest", "Quintar Nest Chest - Hop along west side wall", 2982 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Quintar Nest", "Quintar Nest Chest - Donut Lake crown sprinkle", 851 + treasure_index_offset), #Tonic chest
        LocationData("Quintar Nest", "Underpass Chest - Up north Quintar Nest waterfall", 3620 + treasure_index_offset, logic.has_swimming), #(524, 146, -368) Underpass Scrap chest

        #NPCs
        #Todo NPCs CheckOrNot: two Quintar Eggs here
        LocationData("Quintar Nest", "Quintar Nest NPC - Eastside Silver come on down to the water", 711 + npc_index_offset), #Dust
        LocationData("Quintar Nest", "Quintar Nest NPC - South of sewers Silver", 850 + npc_index_offset), #Ingot
        LocationData("Quintar Nest", "Quintar Nest NPC - Silver on the way out", 755 + npc_index_offset), #Ore

        #Crystals
        LocationData("Quintar Nest", "Quintar Nest Crystal - Hunter", 621 + crystal_index_offset),

        #Quintar Sanctum
        #Treasure chests
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - West wall big bounce", 810 + treasure_index_offset), #Money chest
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - Bounce field", 969 + treasure_index_offset), #Fenix Juice chest
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - In front of the shrine", 2910 + treasure_index_offset), #Quintar Sanctum map chest
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - West at ground level", 2983 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Quintar Sanctum", "Quintar Sanctum Chest - North at ground level", 593 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Quintar Sanctum", "Overpass Chest - Lonely chest above Quintar Sanctum", 3533 + treasure_index_offset), #2nd Overpass Scrap chest on main map

        #NPCs
        #Todo NPCs CheckOrNot: Quintar Egg here (on Quintar Sanctum Mushroom map)
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Silver going back down", 802 + npc_index_offset), #Dust
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Silver almost to the top", 965 + npc_index_offset), #Dust
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Mushroom bounce Silver", 411 + npc_index_offset), #Ingot
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Silver beneath the shroom", 801 + npc_index_offset), #Ingot
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - East side Silver (Do not look down)", 737 + npc_index_offset), #Ore
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Big bounce Silver", 754 + npc_index_offset), #Ore
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Two Toads bestow Princess Toadstool", 963 + npc_index_offset),
        LocationData("Quintar Sanctum", "Quintar Sanctum NPC - Two Toads crown Bowsette", 964 + npc_index_offset),

        #Crystals
        LocationData("Quintar Sanctum", "Quintar Sanctum Crystal - Chemist (of course this is in the shroom zone)", 810 + crystal_index_offset),

        #Capital Jail
        #Treasure chests
        LocationData("Capital Jail", "Capital Jail Chest - Touchdown", 640 + treasure_index_offset), #South Wing Key chest
        LocationData("Capital Jail", "Capital Jail Chest - South Wing jail cell across from busted wall", 930 + treasure_index_offset, lambda state: state.has("Item - South Wing Key", player)), #West Wing Key chest
        LocationData("Capital Jail", "Capital Jail Chest - Haunted jail cell in South Wing dead end", 931 + treasure_index_offset, lambda state: state.has("Item - South Wing Key", player)), #East Wing Key chest
        LocationData("Capital Jail", "Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 1", 990 + treasure_index_offset, lambda state: state.has("Item - South Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Cell Key chest
        LocationData("Capital Jail", "Capital Jail Chest - Fiercely guarded and locked behind South Wing rubble 2", 2668 + treasure_index_offset, lambda state: state.has("Item - South Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Iron Rod chest
        LocationData("Capital Jail", "Capital Jail Chest - Locked behind South Wing rubble", 991 + treasure_index_offset, lambda state: state.has("Item - South Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Battleplate chest
        LocationData("Capital Jail", "Underpass Chest - Drop down behind Capital Jail South Wing rubble", 3675 + treasure_index_offset, lambda state: state.has("Item - South Wing Key", player) and state.has("Item - Cell Key", player, 6)), #7th Underpass Scrap on main map
        LocationData("Capital Jail", "Capital Jail Chest - West Wing jail cell among the glowy plants", 925 + treasure_index_offset, lambda state: state.has("Item - West Wing Key", player)), #Cell Key chest
        LocationData("Capital Jail", "Capital Jail Chest - West Wing arrow plants", 923 + treasure_index_offset, lambda state: state.has("Item - West Wing Key", player)), #Battle Helm chest
        LocationData("Capital Jail", "Capital Jail Chest - Locked among the foliage in West Wing", 916 + treasure_index_offset, lambda state: state.has("Item - West Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Cell Key chest
        LocationData("Capital Jail", "Capital Jail Chest - East Wing bedroom closet twinsies the 1st", 2999 + treasure_index_offset, lambda state: state.has("Item - East Wing Key", player)), #empty chest
        LocationData("Capital Jail", "Capital Jail Chest - East Wing bedroom closet twinsies the 2nd", 906 + treasure_index_offset, lambda state: state.has("Item - East Wing Key", player)), #Potion chest
        LocationData("Capital Jail", "Capital Jail Chest - Waterlogged East Wing hallway twinsies the 1st", 676 + treasure_index_offset, lambda state: state.has("Item - East Wing Key", player)), #Cell Key top chest
        LocationData("Capital Jail", "Capital Jail Chest - Waterlogged East Wing hallway twinsies the 2nd", 707 + treasure_index_offset, lambda state: state.has("Item - East Wing Key", player)), #Cell Key bottom chest

        LocationData("Capital Jail", "Capital Jail Chest - Locked in broken East Wing jail cell", 708 + treasure_index_offset, lambda state: state.has("Item - East Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Cell Key chest
        LocationData("Capital Jail", "Capital Jail Chest - Locked in East Wing bedroom", 763 + treasure_index_offset, lambda state: state.has("Item - East Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Cell Key chest
        LocationData("Capital Jail", "Capital Jail Chest - Locked beyond overgrown West Wing hallway", 909 + treasure_index_offset, lambda state: state.has("Item - West Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Dark Wing Key chest
        LocationData("Capital Jail", "Capital Jail Chest - Dark Wing entry left cell", 2911 + treasure_index_offset, lambda state: state.has("Item - Dark Wing Key", player)), #Capital Jail map chest
        LocationData("Capital Jail", "Capital Jail Chest - Sneaky chest in Dark Wing", 929 + treasure_index_offset, lambda state: state.has("Item - Dark Wing Key", player)), #Woven Hood chest
        LocationData("Capital Jail", "Capital Jail Chest - Corner lava jump in Dark Wing", 920 + treasure_index_offset, lambda state: state.has("Item - Dark Wing Key", player)), #Woven Shirt chest

        #NPCs
        LocationData("Capital Jail", "Capital Jail NPC - Silver in haunted South Wing jail cell", 972 + npc_index_offset, lambda state: state.has("Item - South Wing Key", player)), #Ingot
        LocationData("Capital Jail", "Capital Jail NPC - Silver in zombified South Wing jail cell", 989 + npc_index_offset, lambda state: state.has("Item - South Wing Key", player)), #Ingot
        LocationData("Capital Jail", "Capital Jail NPC - Silver locked in broken East Wing jail cell accompanied by blue flower", 760 + npc_index_offset, lambda state: state.has("Item - East Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Ore
        LocationData("Capital Jail", "Capital Jail NPC - Silver locked in East Wing bedroom", 782 + npc_index_offset, lambda state: state.has("Item - East Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Dust
        LocationData("Capital Jail", "Capital Jail NPC - Silver locked in overgrown West Wing hallway", 759 + npc_index_offset, lambda state: state.has("Item - West Wing Key", player) and state.has("Item - Cell Key", player, 6)), #Ore
        LocationData("Capital Jail", "Capital Jail NPC - Silver in Dark Wing entry right cell", 472 + npc_index_offset, lambda state: state.has("Item - Dark Wing Key", player)), #Dust

        #Crystals
        LocationData("Capital Jail", "Capital Jail Crystal - Reaper, above hell pool", 908 + crystal_index_offset),

        #Capital Pipeline
        #Treasure chests
        LocationData("Capital Pipeline", "Capital Pipeline Chest - I wanna go home", 2912 + treasure_index_offset, logic.has_vertical_movement), #Capital Pipeline map chest
        LocationData("Capital Pipeline", "Capital Pipeline Chest - Do not anger the fungus", 1294 + treasure_index_offset), #Lucky Platter chest

        #NPCs
        LocationData("Capital Pipeline", "Capital Pipeline NPC - Silver in corrupted tunnel 1", 2660 + npc_index_offset), #Ingot
        LocationData("Capital Pipeline", "Capital Pipeline NPC - Silver in corrupted tunnel 2", 1295 + npc_index_offset), #Ore
        LocationData("Capital Pipeline", "Jidamba Eaclaneya NPC - Diamond down Pipeline elevator into Jidamba", 2897 + npc_index_offset, logic.has_vertical_movement), #Dust

        #Cobblestone Crag
        #Treasure chests
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Behind sluice gate", 479 + treasure_index_offset), #Ether Pouch chest
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Long jump", 382 + treasure_index_offset, logic.has_horizontal_movement), #Potion chest
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Tucked in cranny between two tall spikes", 1119 + treasure_index_offset), #Potion Pouch chest
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - I totally meant to miss that jump", 2670 + treasure_index_offset), #Skewer chest
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Upon exiting from Quintar Nest", 478 + treasure_index_offset), #Tonic Pouch chest
        LocationData("Cobblestone Crag", "Cobblestone Crag Chest - Could really use a Walking Stick (chest) right about now...", 2669 + treasure_index_offset),
        LocationData("Cobblestone Crag", "Underpass Chest - On the way to village hidden among leaves", 3669 + treasure_index_offset, logic.has_horizontal_movement), #Underpass Scrap (Okimoto)

        #NPCs
        LocationData("Cobblestone Crag", "Cobblestone Crag NPC - Westernmost Silver", 1120 + npc_index_offset), #Dust

        #Okimoto N.S.
        #Treasure chests
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Moth love lamp", 364 + treasure_index_offset), #Butterfly chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Dont bump your head", 2661 + treasure_index_offset), #Ether Pouch chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Parkour to the west", 337 + treasure_index_offset), #Float Shoes chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Just kinda in there, its not special", 356 + treasure_index_offset), #Potion chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - East of save point", 344 + treasure_index_offset), #Tanto chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - On yashiki balcony", 690 + treasure_index_offset), #Money chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Down hidden stairs in library", 686 + treasure_index_offset), #Art of War chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - East ground floor room", 2673 + treasure_index_offset), #Magic Finder chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Lurking behind bookcase", 434 + treasure_index_offset), #Potion Pouch chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Past hidden staircase", 694 + treasure_index_offset), #Tachi chest
        LocationData("Okimoto N.S.", "Okimoto N.S. Chest - Dance above the koi pond", 1103 + treasure_index_offset), #Training Gi chest
        LocationData("Okimoto N.S.", "Overpass Chest - Mountain lake north of the yashiki", 3534 + treasure_index_offset, logic.has_vertical_movement or logic.has_swimming), #(605, 228, -270) 3rd Overpass Scrap in Overpass main map

        #NPCs
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Silver on the way up", 359 + npc_index_offset), #Dust
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Why does a room like this exist? (Silver)", 692 + npc_index_offset), #Silver Dust
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Eastern Silver atop pond box", 689 + npc_index_offset), #Ingot
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Silver behind room that shall not be named", 691 + npc_index_offset), #Ingot
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Silver atop yashiki", 2659 + npc_index_offset), #Ore
        LocationData("Okimoto N.S.", "Okimoto N.S. NPC - Lets get down to business western Silver", 429 + npc_index_offset), #Ore
        LocationData("Okimoto N.S.", "Overpass NPC - Swim up koi pond waterfall into cherry tree", 1583 + npc_index_offset, logic.has_swimming), #Springs Oath (632, 243, -261) Overpass main map

        #Crystals
        LocationData("Okimoto N.S.", "Okimoto N.S. Crystal - Ninja", 699 + crystal_index_offset),

        #Greenshire Reprise
        #Treasure chests
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Jump off bridge 4", 483 + treasure_index_offset, logic.has_vertical_movement), #Ambush Knife chest
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Atop the waterfalls", 490 + treasure_index_offset), #Ether chest
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Jump off bridge 3", 482 + treasure_index_offset, logic.has_vertical_movement), #Looters Ring chest
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Tall taunter", 373 + treasure_index_offset, logic.has_vertical_movement), #Shell Amulet chest
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - In the valley of trees", 487 + treasure_index_offset), #Tincture Pouch chest
        LocationData("Greenshire Reprise", "Greenshire Reprise Chest - Tip of peninsula south of 2nd bridge", 491 + treasure_index_offset), #Tonic Pouch chest

        #NPCs
        LocationData("Greenshire Reprise", "Greenshire Reprise NPC - Jump down from 2nd bridge to Silver fallen in north crack", 485 + npc_index_offset), #Ore
        LocationData("Greenshire Reprise", "Greenshire Reprise NPC - Silver across 1st bridge hiding in a crack", 486 + npc_index_offset), #Dust
        LocationData("Greenshire Reprise", "Greenshire Reprise NPC - The furthest southern edge Silver", 474 + npc_index_offset), #Ingot

        #Salmon Pass
        #Treasure chests
        LocationData("Salmon Pass", "Salmon Pass Chest - Riverbank among yellow flowers", 2700 + treasure_index_offset), #Paypirbak chest
        LocationData("Salmon Pass", "Salmon Pass Chest - Across a bridge and around through a tunnel", 2420 + treasure_index_offset, logic.has_horizontal_movement), #Fenix Juice chest
        LocationData("Salmon Pass", "Salmon Pass Chest - Admiring the hidden waterfall", 419 + treasure_index_offset), #Fenix Juice chest

        #Salmon River
        #Treasure chests
        LocationData("Salmon River", "Salmon River Chest - Hop on chest once you have become frogger", 1264 + treasure_index_offset), #Money chest
        LocationData("Salmon River", "Salmon River Chest - Atop river island crown", 1297 + treasure_index_offset), #Bloodbind chest
        LocationData("Salmon River", "Salmon River Chest - It also wishes to be frogger", 325 + treasure_index_offset), #Money chest
        LocationData("Salmon River", "Salmon River Chest - In the stands of Salmon race finish line ", 2976 + treasure_index_offset), #Ether Pouch chest
        LocationData("Salmon River", "Salmon River Chest - Inside Salmon Shack", 2913 + treasure_index_offset), #Salmon River map chest
        LocationData("Salmon River", "Overpass Chest - Hop east from shrine to shroom-studded mountainside", 3539 + treasure_index_offset, logic.has_vertical_movement), #(32, 181, -373) 2nd Overpass scrap on (Cloudy Wind)
        LocationData("Salmon River", "Overpass Chest - Frigid dip high behind River Cat", 3654 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #(60, 225, -435) Overpass (Snow) River Cats Ego map
        LocationData("Salmon River", "Overpass Chest - Ultimate Mulan challenge past mushroom mountain", 1401 + treasure_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #(-35, 166, -387) Overpass (Cloudy Wind) Zether Pouch chest

        #NPCs
        #Todo NPCs Missable: figure out Courtyard Key Reid (see Capital Sequoia)
        LocationData("Salmon River", "Overpass NPC - Fall off mushroom mountain onto Gold", 2739 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #(63, 191, -399) 2nd Gold Dust on Overpass (Cloudy Wind)

        #Crystals
        LocationData("Salmon River", "River Cats Ego Crystal - Appease the QuizFish Nomad", 630 + crystal_index_offset), #River Cats Ego

        #Poko Poko Desert
        #Treasure chests
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - Quintar leapfrog", 1080 + treasure_index_offset, logic.has_horizontal_movement), #Butter Cutter chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - South of tricky Quintar Gold", 1082 + treasure_index_offset, logic.has_horizontal_movement), #Hatchet chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - North Lookout Tower", 1190 + treasure_index_offset, logic.has_horizontal_movement), #North Lookout Token chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - This chests (on) a butte", 1169 + treasure_index_offset, logic.has_horizontal_movement), #Dueller
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - Stormy first floor of ruins", 2676 + treasure_index_offset), #Fenix Juice chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - West Lookout Tower", 1170 + treasure_index_offset), #West Lookout Token chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - Potion chest to fortify you for jumping puzzle from hell", 2708 + treasure_index_offset),
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - Central Lookout Tower (ok maybe that jumping puzzle wasnt that bad)", 1189 + treasure_index_offset), #Central Lookout Token chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - Balance beam", 97 + treasure_index_offset), #Scope Specs chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - Past Lost Son", 1667 + treasure_index_offset), #Ether Pouch chest
        LocationData("Poko Poko Desert", "Poko Poko Desert Chest - Cooling off in the tent before the Tower of Zott", 2914 + treasure_index_offset, logic.has_horizontal_movement and logic.has_vertical_movement), #Salmon Bay map chest

        #NPCs
        #Todo NPCs CheckOrNot: three Quintar Eggs in Poko Poko Desert (Nest) map
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Silver beneath overhang in ruins south of shrine", 2675 + npc_index_offset), #Dust
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Silver slumbering in broken house NE of shrine", 1081 + npc_index_offset), #Ingot
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Rocky outcropping Gold will put your Quintar to the test", 2817 + npc_index_offset, logic.has_horizontal_movement), #Dust
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Silver in desert arch shade", 2682 + npc_index_offset), #Ingot
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Thirsty Lad", 1201 + npc_index_offset),
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Stormy Silver atop ruins", 2677 + npc_index_offset), #Ore
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Stormy Silver on ruined building floor", 2681 + npc_index_offset), #Ore
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Gold Ingot atop ridge south of North Lookout Tower", 2818 + npc_index_offset),
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Silver in the sandstorm on ruins 2nd floor", 2680 + npc_index_offset, logic.has_horizontal_movement), #Dust
        #Todo NPCs Blocker: this son unlocks a check in Sara Sara Bazaar
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Circle the western desert wall for Lost Son", 1198 + npc_index_offset), #29b1d681
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Gold overlooking Sara Sara Bazaar", 2707 + npc_index_offset, logic.has_vertical_movement), #Ingot
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Gold accessible from beach reacharound", 2711 + npc_index_offset, logic.has_horizontal_movement and logic.has_vertical_movement), #Dust
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Diamond on Tower of Zotts outside", 2879 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Dust
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Gold on far end of the Tower of Zott", 2816 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ore
        LocationData("Poko Poko Desert", "Poko Poko Desert NPC - Gold on an outcropping by long loop-around chest", 2706 + npc_index_offset, logic.has_horizontal_movement), #Ore
        
        #Sara Sara Bazaar
        #Treasure chests
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar Chest - Someone took the St James and left a...", 408 + treasure_index_offset, lambda state: state.has("Item - Room 1 Key", player)), #Knockout Stick chest
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar Chest - Darkened upper storeroom 1", 414 + treasure_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #Potion chest
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar Chest - Darkened upper storeroom 2", 513 + treasure_index_offset, logic.has_rental_quintar or logic.has_horizontal_movement), #Storm Rod chest
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar Chest - Potion Mixer", 1194 + treasure_index_offset), #Beaurior Volcano map chest
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar Chest - Spilled booty", 2936 + treasure_index_offset, logic.has_swimming), #Captains Hat chest

        #NPCs
        #Todo NPCs CheckOrNot: East and West Stable Owners are Crystal Checker guys who give you a Quintar Pass for having enough crystals; don't if you already have the Quintar Pass
        #LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Quintar West Stable Owner crystal checker for Quintar Pass if you refuse to touch an eyeball", 1852 + npc_index_offset, lambda state: logic.has_jobs(state, 7)),
        #LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Quintar East Stable Owner crystal checker for Quintar Pass if you refuse to touch an eyeball", 2234 + npc_index_offset, lambda state: logic.has_jobs(state, 7)),
        #Todo NPCs CheckOrNot: Crystal Checker guy gives you Ferry Pass for having 15 crystals Z27_FerryCrystalChecker ID 940 (-166,93,56)
        #LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Ferry crystal checker grants Ferry Pass in case you hate children", 940 + npc_index_offset, lambda state: logic.has_jobs(state, 15)),
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Three tokens makes a Pyramid Key something something triangles", 949 + npc_index_offset, lambda state: state.has("Item - West Lookout Token", player) and state.has("Item - Central Lookout Token", player) and state.has("Item - North Lookout Token", player)),
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - The One and Only Room 1 Key", 385 + npc_index_offset),
        #Todo NPCs Blocker: gotta find the Lost Son first (the mom before you find the son is a different NPC)
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Worried Mom", 1196 + npc_index_offset), #Ferry Pass
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Pelt this Fish Merchant with Rotten Salmon", 942 + npc_index_offset, lambda state: state.has("Item - Rotten Salmon", player)),
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - No Shoudu Stew for you!", 1200 + npc_index_offset, lambda state: state.has("Item - Shoudu Stew", player)),
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Spilled booty Silver", 2905 + npc_index_offset, logic.has_swimming), #Dust
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Spilled booty Silverer", 2906 + npc_index_offset, logic.has_swimming), #Dust
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Spilled booty Silvererer", 2903 + npc_index_offset, logic.has_swimming), #Ingot
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Spilled booty Silverererer", 2904 + npc_index_offset, logic.has_swimming), #Ingot
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Spilled booty Silvererererer", 2901 + npc_index_offset, logic.has_swimming), #Ore
        LocationData("Sara Sara Bazaar", "Sara Sara Bazaar NPC - Spilled booty Silverererererer", 2902 + npc_index_offset, logic.has_swimming), #Ore

        #Sara Sara Beach
        #Treasure chests
        LocationData("Sara Sara Beach", "Sara Sara Beach Chest - Glittering in the sun at Ibek Cave exit 1", 1083 + treasure_index_offset, logic.has_vertical_movement), #Tincture Pouch chest
        LocationData("Sara Sara Beach", "Sara Sara Beach Chest - Glittering in the sun at Ibek Cave exit 2", 1085 + treasure_index_offset, logic.has_vertical_movement), #Tonic Pouch chest
        LocationData("Sara Sara Beach", "Sara Sara Beach Chest - On the back cliff wall", 154 + treasure_index_offset, logic.has_horizontal_movement), #Ether chest
        LocationData("Sara Sara Beach", "Sara Sara Beach Chest - Across the palms above the dust", 1509 + treasure_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Potion chest
        LocationData("Sara Sara Beach", "Sara Sara Beach Chest - How dare you stand where he stood?", 1084 + treasure_index_offset, logic.has_vertical_movement), #Money chest
        LocationData("Sara Sara Beach", "Sara Sara Beach Chest - Beach cave", 2718 + treasure_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Blank Pages chest
        LocationData("Sara Sara Beach", "Sara Sara Beach Chest - West beach tightrope walk", 1546 + treasure_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Potion chest
        LocationData("Sara Sara Beach", "Overpass Chest - West of Valkyrie Watchtower", 3540 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #(1, 129, 62) 7th Overpass Scrap on main map

        #NPCs
        #Todo NPCs Job Masters: Master Dervish ID 3575 (-255, 103, -237); gives you Dervish Seal in exchange for job mastery
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver glittering in the sun at Ibek Cave exit 1", 2683 + npc_index_offset, logic.has_vertical_movement), #Dust
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver glittering in the sun at Ibek Cave exit 2", 2684 + npc_index_offset, logic.has_vertical_movement), #Dust
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver glittering in the sun at Ibek Cave exit 3", 2686 + npc_index_offset, logic.has_vertical_movement), #Dust
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Cross my palms with Silver", 2693 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Dust
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver past angry birds", 2697 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Dust
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Jaunt along cliff past Dr Cool Aids perch to Silver", 2685 + npc_index_offset, logic.has_vertical_movement), #Ingot
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver on the beach rocks at eastern edge", 2687 + npc_index_offset), #Ingot
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver glittering in the sun at Ibek Cave exit 4", 2688 + npc_index_offset, logic.has_vertical_movement), #Silver
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver on the back cliff wall", 2694 + npc_index_offset, logic.has_horizontal_movement), #Ingot
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver at the foot of the Tower of Zott", 2699 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Ingot
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Lonely Islet Silver", 2878 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Ingot
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver glittering in the sun at Ibek Cave exit 2", 2689 + npc_index_offset, logic.has_vertical_movement), #Ore
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver glittering in the sun at Ibek Cave exit 3", 2690 + npc_index_offset, logic.has_vertical_movement), #Ore
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Eastern beach Silver beheld by Dr Cool Aids", 2691 + npc_index_offset, logic.has_vertical_movement), #Ore
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver on western beach along the cliffside", 2692 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Ore
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver chilling in beach cave", 2698 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Ore
        LocationData("Sara Sara Beach", "Sara Sara Beach NPC - Silver further along beach", 2877 + npc_index_offset), #Ore

        #Ancient Reservoir
        #Treasure chests
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Really elaborate crystal rafters", 1123 + treasure_index_offset), #Red Coat chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Crystal gutters", 1122 + treasure_index_offset), #Red Cap chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Tucked on ledge by aqueduct", 1982 + treasure_index_offset, logic.has_horizontal_movement), #Resist Shifter chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - East Switch Room", 2977 + treasure_index_offset), #Ether Pouch chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Eastern nyoom room", 2056 + treasure_index_offset), #Money chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Hiding behind aqueduct grate", 2703 + treasure_index_offset), #Potion Pouch chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Hiding behind western aqueduct grate", 2702 + treasure_index_offset, logic.has_horizontal_movement), #Money chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Twinsies the 1st at west waterfall base", 2704 + treasure_index_offset), #Defense Shifter chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Twinsies the 2nd at west waterfall base", 1145 + treasure_index_offset), #Money chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Salmon swim up", 2701 + treasure_index_offset, logic.has_swimming), #Grim Scythe chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Goat snack for later", 2915 + treasure_index_offset), #Ancient Reservoir map chest
        LocationData("Ancient Reservoir", "Ancient Reservoir Chest - Celebrate your new hops", 2517 + treasure_index_offset, logic.has_vertical_movement), #Fenix Juice Pouch chest
        LocationData("Ancient Reservoir", "Underpass Chest - Waterway nook between Gran & Ancient Reservoir", 3541 + treasure_index_offset, logic.has_swimming), #(64, 98, -111) 1st Underpass Scrap on main map

        #NPCs
        LocationData("Ancient Reservoir", "Ancient Reservoir NPC - Silver in odd flooded room 1", 2695 + npc_index_offset), #Ingot
        LocationData("Ancient Reservoir", "Ancient Reservoir NPC - Silver in odd flooded room 2", 1675 + npc_index_offset), #Ore
        LocationData("Ancient Reservoir", "Ancient Reservoir NPC - Goat victory Ibek Bell", 1676 + npc_index_offset), #Z30_PostBossEvent;
        LocationData("Ancient Reservoir", "Ancient Reservoir NPC - Silver in the goat digs", 2696 + npc_index_offset, logic.has_vertical_movement), #Dust

        #Crystals
        LocationData("Ancient Reservoir", "Ancient Reservoir Crystal - Dervish", 1121 + crystal_index_offset),

        #Salmon Bay
        #Treasure chests
        LocationData("Salmon Bay", "Salmon Bay Chest - Cliffdiving", 2975 + treasure_index_offset), #Ether Pouch chest
        LocationData("Salmon Bay", "Salmon Bay Chest - Across the bridge", 2974 + treasure_index_offset), #Potion Pouch chest
        
        #NPCs
        LocationData("Salmon Bay", "Salmon Bay NPC - Ancient Tablet B on moodlit shore behind waterfall", 2438 + npc_index_offset),
        LocationData("Salmon Bay", "Salmon Bay NPC - West cliffdiving Ancient Tablet C", 1271 + npc_index_offset),
        LocationData("Salmon Bay", "Salmon Bay NPC - Quintar splish splash Ancient Tablet A", 1272 + npc_index_offset),
        LocationData("Salmon Bay", "Overpass NPC - Lonely scrap among half-dead pines above Salmon Bay", 3677 + npc_index_offset), #8th Scrap in Overpass main map

        #Summons Todo: descriptivize and implement
        #-50, 91, -330
        #LocationData("Salmon Bay", "Salmon Bay Summon - Guaba from SThunder_Summon", 1138 + summon_index_offset),

        #Overpass
        #Treasure chests
        #Life Jewel on main map has been categorized under Dione Shrine
        #1st Scrap on main Overpass map has been categorized under Rolling Quintar Fields
        #2nd Scrap on main Overpass map has been categorized under the Quintar Sanctum
        #3rd Scrap on main Overpass map has been categorized under the Okimoto N.S.
        #4th Scrap on main Overpass map has been categorized under Dione Shrine
        #5th Scrap on main Overpass map has been categorized under Quintar Reserve
        #6th Scrap on main Overpass map has been categorized under Delende
        #7th Scrap on main Overpass map has been categorized under Sara Sara Beach
        #8th Scrap on main Overpass map has been categorized under Salmon Bay
        #9th Scrap on main Overpass map has been categorized under Lands End
        #1st Overpass Scrap (Cloudy Wind) has been categorized under Tall Tall Heights
        #Zether Pouch (Cloudy Wind) has been categorized under Salmon River
        #River Cats Ego map (Snow) recategorized under Salmon River
        #Overpass (Outpost) Northern Stretch map has been categorized under Northern Stretch
        #Overpass (Outpost) Scrap has been categorized under Tall Tall Heights

        #NPCs
        #Todo NPCs Job Masters: Overpass main map has Master Hunter ID 3558 (496, 198, -346); gives you Hunter Seal in exchange for job mastery
        #Gold Ingot on Overpass main map has been categorized under Dione Shrine
        #Z20_WaterOrigin ID 1583 (gives Springs Oath) has been categorized under Okimoto N.S. (632, 243, -261)
        #1st Gold Dust (Cloudy Wind) has been categorized under Tall Tall Heights
        #2nd Gold Dust (Cloudy Wind) has been categorized under Salmon River
        #Todo NPCs CheckOrNot: Overpass 4 Quintar Eggs (Dirt Nest), 1 Quintar Egg (Stone Nest), 1 Quintar Egg (Cave Nest), 1 Quintar Egg (Stone Nest) submap
        #Todo NPCs Job Masters: Overpass (Outpost) has Master Aegis ID 3610 (501, 194, -210); gives you Aegis Seal in exchange for job mastery
        #Todo NPCs Job Masters: Overpass (Outpost) has Master Beastmaster ID 3608 (312, 236, -344); gives you Beastmaster Seal in exchange for job mastery
        #Todo NPCs Job Masters: Overpass (Outpost) has Master Ninja ID 3550 (561, 238, -209); gives you Ninja Seal in exchange for job mastery
        #Todo NPCs Job Masters: Overpass (Outpost) has Master Nomad ID 3548 (53, 227, -465); gives you Nomad Seal in exchange for job mastery
        #Todo NPCs Job Masters: Overpass (Outpost) has Master Reaper ID 3611 (232, 220, -383); gives you Reaper Seal in exchange for job mastery
        #Todo NPCs Job Masters: Overpass (Outpost) has Master Summoner ID 3557 (379, 246, -575); gives you Summoner Seal in exchange for job mastery
        #Todo NPCs Job Masters: Overpass (Outpost) has Master Valkyrie ID 3554 (24, 137, 71); gives you Valkyrie Seal in exchange for job mastery
        #Todo NPCs Job Masters: Overpass (Outpost 3H) has Master Fencer ID 3573 (166, 154, -124); gives you Fencer Seal in exchange for job mastery

        #Underpass
        #Treasure chests
        #3 treasures categorized under Delende
        #1st Scrap main Underpass map has been categorized under Ancient Reservoir
        #1st Scrap main Underpass map has been categorized under Quintar Nest
        #3rd Scrap main Underpass map has been categorized under Pale Grotto
        #4th Scrap main Underpass map has been categorized under Jojo Sewers
        #5th Scrap main Underpass map categorized under Delende
        #6th Scrap main Underpass map has been categorized under the Quintar Mausoleum
        #7th Scrap main Underpass map has been categorized under the Capital Jail
        #Underpass (Okimoto) Scrap has been categorized under Cobblestone Crag
        #Underpass (Summon Pah) Scrap has been categorized under The Undercity
        #Underpass (Ice Pass) Scrap chest has been categorized under Tall Tall Heights
        #Underpass (Ice Pass) Potion chest has been categorized under Tall Tall Heights
        #Underpass (Underwater) Scrap chest has been categorized under Tall Tall Heights

        #Summons Todo: descriptivize and implement
        #614, 91, -213
        #LocationData("Underpass", "Underpass Summon - Pah from SReflect_Summon", 1130 + summon_index_offset),

        #Zones (Expert)
        #The Open Sea
        #Treasure chests
        LocationData("The Open Sea", "The Open Sea Chest - South of Jidamba Tangle 1", 3767 + treasure_index_offset, logic.has_swimming), #Fenix Syrup chest
        LocationData("The Open Sea", "The Open Sea Chest - South of Jidamba Tangle 2", 3765 + treasure_index_offset, logic.has_swimming), #Z-Potion chest

        #NPCs
        #Todo NPCs Player Options: (-139, 91, 123) do we want a filter option to add the guy who fishes things up for you
        #LocationData("The Open Sea", "The Open Sea NPC - Z27_FisherOnRaft", 2804 + npc_index_offset),
        #Todo NPCs CheckOrNot: (930, 91, 253) do we put a check on the guy who gives you a Gaea Shard if you get there with no Salmon lol
        #LocationData("The Open Sea", "The Open Sea NPC - Z34_SinisterSailor", 2520 + npc_index_offset),

        #Shoudu Waterfront
        #Treasure chests
        LocationData("Shoudu Waterfront", "Shoudu Waterfront Chest - Along the water", 2419 + treasure_index_offset), #Money chest
        LocationData("Shoudu Waterfront", "Shoudu Waterfront Chest - Hop around 1", 3690 + treasure_index_offset), #Empty chest
        LocationData("Shoudu Waterfront", "Shoudu Waterfront Chest - Hop around 2", 1114 + treasure_index_offset), #Mars Stone chest

        #Shoudu Province
        #Treasure chests
        LocationData("Shoudu Province", "Shoudu Province Chest - 2 Sky Arena Wins Room 1", 2794 + treasure_index_offset, logic.has_vertical_movement), #Money chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 2 Sky Arena Wins Room 2", 2751 + treasure_index_offset, logic.has_vertical_movement), #Bone Mail chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 2 Sky Arena Wins room 3", 2747 + treasure_index_offset, logic.has_vertical_movement), #Cutlass chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Below fast boi spark", 3504 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Hidden in a house by the elevator 1", 3505 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Through rooftop window south of fast boi spark 1", 3506 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Near sky fishing 1", 3507 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Reservoir above the water", 3508 + treasure_index_offset, logic.has_vertical_movement and logic.has_swimming), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Above accessory shop", 3509 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Building near all the grates", 3510 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Above Samurai Lounge", 3511 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Samurai Lounge", 3512 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Assassin Lounge", 3513 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Among crates across from Assassin Lounge", 3514 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Its in a room and there is a bed", 3515 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Granary", 3520 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Below the flower house", 3521 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - White hut", 3522 + treasure_index_offset, logic.has_vertical_movement), #Elevator Part chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Balance above the undercity 1", 2717 + treasure_index_offset, logic.has_vertical_movement), #Ether chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Jump through a window", 1507 + treasure_index_offset, logic.has_vertical_movement), #Ether Pouch chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Across the reservoir", 2978 + treasure_index_offset, logic.has_vertical_movement and logic.has_swimming), #Ether Pouch chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Above Samurai Lounge", 1541 + treasure_index_offset, logic.has_vertical_movement), #Fleuret chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Crawl along the attic", 1536 + treasure_index_offset, logic.has_vertical_movement), #Knicked Knackers chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Sneaky back door of cramped storage room", 1519 + treasure_index_offset, logic.has_vertical_movement), #Looters Pin chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Sneak behind crates near Assassin Lounge", 2760 + treasure_index_offset, logic.has_vertical_movement), #Muggers Glove chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Weaponsmith", 1505 + treasure_index_offset), #Plague Mask chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Outside the inn", 2985 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Go in the back door", 1506 + treasure_index_offset, logic.has_vertical_movement), #Potion Pouch
        LocationData("Shoudu Province", "Shoudu Province Chest - Near the Assassin Lounge", 2762 + treasure_index_offset, logic.has_vertical_movement), #Potion Pouch
        LocationData("Shoudu Province", "Shoudu Province Chest - Jump along the lamppost", 2752 + treasure_index_offset, logic.has_vertical_movement), #Suitor Hat chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Above the armor shop", 1517 + treasure_index_offset, logic.has_vertical_movement), #Potion Pouch chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Through rooftop window south of fast boi spark 2", 2763 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Balance above the undercity 2", 2716 + treasure_index_offset, logic.has_vertical_movement), #Tincture Pouch chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Cross the balance beam east of save point", 3040 + treasure_index_offset, logic.has_vertical_movement), #Potion Pouch chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Cross the balance beam on the way to Sky Arena", 2754 + treasure_index_offset, logic.has_vertical_movement), #Acrobat Shoes chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Atop the roofs near the grates", 1369 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Shoudu Province", "Shoudu Province Chest - In the flower room", 2789 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Hidden in a house by the elevator 2", 2790 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Near sky fishing 2", 2986 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Under the dry kid pit", 1365 + treasure_index_offset, logic.has_vertical_movement), #The Immovable chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 2 Sky Arena Wins room 4", 2796 + treasure_index_offset, logic.has_vertical_movement), #Tonic Pouch
        LocationData("Shoudu Province", "Shoudu Province Chest - 2 Sky Arena Wins room 5", 2748 + treasure_index_offset, logic.has_vertical_movement), #Soul Kris chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 5 Sky Arena Wins room 1", 2812 + treasure_index_offset, logic.has_vertical_movement), #Money chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 5 Sky Arena Wins room 2", 2723 + treasure_index_offset, logic.has_vertical_movement), #Gaia Axe chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 5 Sky Arena Wins room 3", 2813 + treasure_index_offset, logic.has_vertical_movement), #Money chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 5 Sky Arena Wins room 4", 2753 + treasure_index_offset, logic.has_vertical_movement), #Gaia Vest chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 8 Sky Arena Wins room 1", 2665 + treasure_index_offset, logic.has_vertical_movement), #Gravedigger chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 8 Sky Arena Wins room 2", 2805 + treasure_index_offset, logic.has_vertical_movement), #Malifice chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 8 Sky Arena Wins room 3", 2800 + treasure_index_offset, logic.has_vertical_movement), #Wizards Wall chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Fall through broken grate below Sky Arena building", 2951 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Lurking above spike ballpit by goldsmith", 2984 + treasure_index_offset, logic.has_vertical_movement), #(753, 105, -176) Tincture Pouch chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 10 Sky Arena Wins room 1", 2756 + treasure_index_offset, logic.has_vertical_movement), #(753, 134, -263) Yasha chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 10 Sky Arena Wins room 2", 2928 + treasure_index_offset, logic.has_vertical_movement), #(754, 134, -264) Muramasa chest
        LocationData("Shoudu Province", "Shoudu Province Chest - 10 Sky Arena Wins room 3", 2929 + treasure_index_offset, logic.has_vertical_movement), #(755, 134, -263) Shadow Gi chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Fall through floorboards of 10 Sky Arena Wins room 1", 3763 + treasure_index_offset, logic.has_vertical_movement), #(754, 130, -264) Zether chest
        LocationData("Shoudu Province", "Shoudu Province Chest - Fall through floorboards of 10 Sky Arena Wins room 2", 3764 + treasure_index_offset, logic.has_vertical_movement), #(755, 130, -263) Z-Potion chest

        #NPCs
        #Todo NPCs Job Masters: Master Assassin ID 3605 (769, 123, -201); gives you Assassin Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Samurai ID 3576 (800, 115, -221); gives you Samurai Seal in exchange for job mastery
        #Todo NPCs Multichecks: Shoudu Province (Sky Arena) map Z38_SkyArenaPrizes ID 1921 (765, 125, -248) gives 6 prizes in exchange for winning fights
        #Todo NPCs Missable: Z38_ChloesLure ID 2737 (781, 131, -278) gives you a Jigging Lure
        LocationData("Shoudu Province", "Shoudu Province NPC - 10 Sky Arena Wins room Diamond 1", 2833 + npc_index_offset, logic.has_vertical_movement), #(752, 133, -262) Dust
        LocationData("Shoudu Province", "Shoudu Province NPC - 10 Sky Arena Wins room Diamond 2", 2811 + npc_index_offset, logic.has_vertical_movement), #(756, 133, -261) Ingot
        LocationData("Shoudu Province", "Shoudu Province NPC - Diamond through a hole in the 10 Sky Arena Wins room floor", 2832 + npc_index_offset, logic.has_vertical_movement), #(753, 130, -264) Ore
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold at back reservoir wall", 2827 + npc_index_offset, logic.has_vertical_movement and logic.has_swimming), #Ingot
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold in farmland on way to shrine", 2821 + npc_index_offset, logic.has_vertical_movement), #Ingot
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold near sky fishing", 2834 + npc_index_offset, logic.has_vertical_movement), #Ore
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold in 2 Sky Arena Wins room", 2829 + npc_index_offset, logic.has_vertical_movement), #Dust
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold in 5 Sky Arena Wins room 1", 2720 + npc_index_offset, logic.has_vertical_movement), #Ore
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold in 5 Sky Arena Wins room 2", 2722 + npc_index_offset, logic.has_vertical_movement), #Ingot
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold in 5 Sky Arena Wins room 3", 2721 + npc_index_offset, logic.has_vertical_movement), #Dust
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold in 8 Sky Arena Wins room 1", 2830 + npc_index_offset, logic.has_vertical_movement), #Ingot
        LocationData("Shoudu Province", "Shoudu Province NPC - Gold in 8 Sky Arena Wins room 2", 2831 + npc_index_offset, logic.has_vertical_movement), #Ore

        #Crystals
        LocationData("Shoudu Province", "Shoudu Province Crystal - Samurai for 3 Sky Arena wins", 1206 + crystal_index_offset, logic.has_vertical_movement),

        #Summons Todo: descriptivize and implement (720, 138, -278)
        #LocationData("Shoudu Province", "Shoudu Province Summon - Tira from SShadow_Summon", 1132 + summon_index_offset),

        #The Undercity
        #Treasures
        LocationData("The Undercity", "The Undercity Chest - Hiding in the rafters", 2989 + treasure_index_offset), #Potion Pouch chest
        LocationData("The Undercity", "The Undercity Chest - Up the rafters against a pillar", 2990 + treasure_index_offset), #Ether chest
        LocationData("The Undercity", "The Undercity Chest - Even further up the rafters", 2991 + treasure_index_offset), #Ether Pouch chest
        LocationData("The Undercity", "The Undercity Chest - Gated-off room 1", 2988 + treasure_index_offset), #Fenix Juice chest
        LocationData("The Undercity", "The Undercity Chest - Gated-off room 2", 2987 + treasure_index_offset), #Ether chest
        LocationData("The Undercity", "The Undercity Chest - Gated-off room 3", 1147 + treasure_index_offset), #Potion chest
        LocationData("The Undercity", "The Undercity Chest - Gated-off room 4", 3517 + treasure_index_offset), #(778, 94, -254) Elevator Part chest
        LocationData("The Undercity", "The Undercity Chest - Climb up lampposts and run across the fence", 1925 + treasure_index_offset), #Cursegiver chest
        LocationData("The Undercity", "The Undercity Chest - North wall climb", 3516 + treasure_index_offset), #Elevator Part chest
        LocationData("The Undercity", "The Undercity Chest - Atop awning east of the waterfall", 3518 + treasure_index_offset), #Elevator Part chest
        LocationData("The Undercity", "The Undercity Chest - Hiding in a building in the north area", 2826 + treasure_index_offset), #Potion chest
        LocationData("The Undercity", "The Undercity Chest - Undercity Inn", 3519 + treasure_index_offset), #Elevator Part
        LocationData("The Undercity", "The Undercity Chest - South of the Undercity Inn", 1695 + treasure_index_offset), #Brigandine chest
        LocationData("The Undercity", "The Undercity Chest - Hidden in a nook in the wall", 2793 + treasure_index_offset), #Knights Plate chest
        LocationData("The Undercity", "Underpass Chest - Lovely bounce tree W of The Undercity", 3673 + treasure_index_offset, logic.has_swimming), #(608, 91, -215) (Summon Pah) Underpass Scrap chest
        
        #NPCs
        LocationData("The Undercity", "The Undercity NPC - Gold hiding from the bats under the awning", 2835 + npc_index_offset), #Dust
        LocationData("The Undercity", "The Undercity NPC - Gated-off room Gold", 2825 + npc_index_offset), #Ore
        LocationData("The Undercity", "The Undercity NPC - Gold in the sewer offshoot", 1696 + npc_index_offset, lambda state: state.has("Item - Progressive Salmon Violin", player)), #Dust
        LocationData("The Undercity", "The Undercity NPC - Storage room Gold of the Undercity Inns", 1696 + npc_index_offset), #Ingot

        #Crystals
        LocationData("The Undercity", "The Undercity Crystal - Assassin", 1204 + crystal_index_offset),

        #Ganymede Shrine
        #Treasure chests
        LocationData("Ganymede Shrine", "Ganymede Shrine Chest - drop down from the top", 1594 + treasure_index_offset, lambda state: lambda state: state.has("Item - Ganymede Stone", player)),

        #Beaurior Volcano
        #Treasure chests
        LocationData("Beaurior Volcano", "Beaurior Volcano Chest - Beaurior Rock entrance", 3770 + treasure_index_offset), #Fenix Syrup chest
	    LocationData("Beaurior Volcano", "Beaurior Volcano Chest - Outcropping above the fog", 1168 + treasure_index_offset), #Temporal Blade chest
	    LocationData("Beaurior Volcano", "Beaurior Volcano Chest - Tricky jumps past Rock entrance", 2750 + treasure_index_offset), #Tome of Light chest

        #Beaurior Rock
        #Treasure chests
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B4 big lava room with optional boss", 1796 + treasure_index_offset), #Ether chest
	    LocationData("Beaurior Rock", "Beaurior Rock Chest - Caged in far corner of B4 big lava room with optional boss", 481 + treasure_index_offset), #Guard Crown chest
	    LocationData("Beaurior Rock", "Beaurior Rock Chest - Caged through secret tunnel in B4 big lava room with optional boss", 724 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 2)), #Halberd chest
	    LocationData("Beaurior Rock", "Beaurior Rock Chest - Island in B4 big lava room with optional boss", 1682 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 2)), #Small Key chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - Elevator down from entrance to happy spike land", 894 + treasure_index_offset), #Small Key chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B3 balcony above the lava", 1337 + treasure_index_offset, lambda state: state.has("Item - Small Key", player)), #Small Key chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B2 with the Lets Make a Deal doors", 2973 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 2)), #Potion Pouch chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B1 overlooking the catwalks room", 818 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 2)), #Small Key chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B1 square pokeball room", 2916 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 2)), #map chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B3 behind wrought-iron fence", 899 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 2)), #Shelter Dress chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B3 ominous green dumplings room", 1797 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 2)), #Fenix Juice chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B2 danger hops back to purple", 2044 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 4)), #Ether Pouch chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B1 cheeky lava platforming 1", 2041 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 4)), #Potion
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B1 cheeky lava platforming 2", 1799 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 4)), #Ether
        LocationData("Beaurior Rock", "Beaurior Rock Chest - B1 jump to odd ice block", 2040 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 4)), #Cold Touch chest
        LocationData("Beaurior Rock", "Beaurior Rock Chest - Top floor ominous lamps room", 1683 + treasure_index_offset, lambda state: state.has("Item - Small Key", player, 4)), #Boss Key chest

        #NPCs
        LocationData("Beaurior Rock", "Beaurior Rock NPC - Gold in B4 big lava room with optional boss", 2822 + npc_index_offset, lambda state: state.has("Item - Small Key", player) and logic.has_horizontal_movement), #Gold Ingot
        LocationData("Beaurior Rock", "Beaurior Rock NPC - B1 cheeky lava platforming Gold", 2823 + npc_index_offset, lambda state: state.has("Item - Small Key", player, 4)), #Dust
        LocationData("Beaurior Rock", "Beaurior Rock NPC - B1 Magic Well friendos hiding in the pillars", 2824 + npc_index_offset, lambda state: state.has("Item - Small Key", player, 4) and logic.has_horizontal_movement), #Ore
        LocationData("Beaurior Rock", "Beaurior Volcano NPC - Summit Gold", 2836 + npc_index_offset, lambda state: state.has("Item - Small Key", player, 4) and logic.has_horizontal_movement), #Ore Beaurior Volcano but it's at the top so Rock it is

        #Crystals
	    LocationData("Beaurior Rock", "Beaurior Volcano Crystal - Valkyrie", 1086 + crystal_index_offset, lambda state: state.has("Item - Small Key", player, 4) and state.has("Item - Boss Key", player)),

        #Lake Delende
        #Treasure chests
        LocationData("Lake Delende", "Lake Delende Chest - North edge 1", 1263 + treasure_index_offset), #Float Shoes chest
        LocationData("Lake Delende", "Lake Delende Chest - North edge 2", 2917 + treasure_index_offset, logic.has_vertical_movement), #Lake Delende map chest

        #NPCs
        LocationData("Lake Delende", "Lake Delende NPC - Panning for Gold down Salmon Creek without a paddle", 2854 + npc_index_offset), #Dust

        #Summons Todo: descriptivize and implement
        #97, 126, -211
        #LocationData("Lake Delende", "Lake Delende Summon - Ioske from SEarth_Summon", 1111 + summon_index_offset),

        #Quintar Reserve
        #Treasure chests
        LocationData("Quintar Reserve", "Overpass Chest - Climbing the boughs up from the elevator", 3536 + treasure_index_offset), #5th Scrap on Overpass main map
        LocationData("Quintar Reserve", "Quintar Reserve Chest - Race start hut", 1591 + treasure_index_offset), #Quintar Grass chest
        LocationData("Quintar Reserve", "Quintar Reserve Chest - Hollowed-out wall of Mausoleum", 1320 + treasure_index_offset, logic.has_glide), #Undead Ring chest

        #NPCs
        #Todo NPCs CheckOrNot: 3 Quintar Eggs here
        #Todo NPCs CheckOrNot: MiscQuintar ID 427 gives you The Sequoia map if you don't have it (and you can speak Quintar aka have Babel Quintar item from Mausoleum) (789, 191, -338)
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding 1 down in the quintar nest 1", 2255 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 1
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding 2 down in the quintar nest 2", 2256 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 2
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding in sneaky Quintar nest north of Mausoleum", 2257 + npc_index_offset), #Shedding 3
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding east of shrine", 2259 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 4
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Long jog along the east mountain to shedding", 2260 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 5
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding overlooking the east ocean", 2261 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 6
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding atop the Mausoleum", 2262 + npc_index_offset, lambda state: state.has("Item - Dione Stone", player) and logic.has_glide), #Shedding 7
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Treetop shedding north of Mausoleum", 2263 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 8
        #shedding 9 is in the Dione Shrine because why not I guess
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding overlooking the race start point", 2265 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 10
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding north of Mausoleum", 2266 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Shedding 11
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Shedding just north of Quintar cosplayer", 2267 + npc_index_offset), #Shedding 12
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Gold on east side of map", 2837 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Ore
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Climb the center mountain for Gold", 2839 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Ore
        LocationData("Quintar Reserve", "Quintar Reserve NPC - Jump across the treetops for Gold", 2840 + npc_index_offset, lambda state: logic.has_vertical_movement and logic.has_horizontal_movement and state.has("Item - Dione Stone", player)), #Dust

        #Dione Shrine
        #Treasure chests
        LocationData("Dione Shrine", "Dione Shrine Chest - Roof", 2154 + treasure_index_offset, lambda state: state.has("Item - Dione Stone", player)), #Dione Shard chest
        LocationData("Dione Shrine", "Dione Shrine Chest - Lobby", 2791 + treasure_index_offset), #Dione Shard chest
        LocationData("Dione Shrine", "Dione Shrine Chest - 2nd floor", 2792 + treasure_index_offset), #Dione Shard chest
        LocationData("Dione Shrine", "Dione Shrine Chest - 2nd floor balcony", 1146 + treasure_index_offset), #Dione Shard chest
        LocationData("Dione Shrine", "Overpass Chest - Glide SW from top of shrine 1", 3535 + treasure_index_offset, lambda state: logic.has_glide and state.has("Item - Dione Stone", player)), #4th Scrap on main Overpass map
        LocationData("Dione Shrine", "Overpass Chest - Glide SW from top of shrine 2", 2749 + treasure_index_offset, lambda state: logic.has_glide and state.has("Item - Dione Stone", player)), #Life Jewel Overpass main map

        #NPCs
        LocationData("Dione Shrine", "Dione Shrine NPC - Shedding on roof", 2265 + npc_index_offset, lambda state: state.has("Item - Dione Stone", player)), #Shedding 9
        LocationData("Dione Shrine", "Dione Shrine NPC - Glide SW from top of shrine to Gold", 2838 + npc_index_offset, lambda state: logic.has_glide and state.has("Item - Dione Stone", player)), #Ingot on Overpass main map

        #Quintar Mausoleum
        #Treasure chests
        LocationData("Quintar Mausoleum", "Quintar Mausoleum Chest - Past the switches race", 2153 + treasure_index_offset, lambda state: state.has("Item - Progressive Quintar Flute", player, 2)), #(688, 114, -464) Babel Quintar chest
        LocationData("Quintar Mausoleum", "Quintar Mausoleum Chest - Rocky room", 3401 + treasure_index_offset), #(664, 129, -425) Quintar Mausoleum map chest
        LocationData("Quintar Mausoleum", "Quintar Mausoleum Chest - Glowing grass room", 3768 + treasure_index_offset), #(709, 129, -442) Wind Thresher chest
        LocationData("Quintar Mausoleum", "Underpass Chest - Up the waterfall inside Quintar Mausoleum", 3674 + treasure_index_offset), #(614, 146, -410) 6th Scrap chest on main Underpass map

        #Eastern Chasm
        #Treasure chests
        LocationData("Eastern Chasm", "Eastern Chasm Chest - Overgrown opposite of chasm", 3543 + treasure_index_offset), #Eastern Chasm map chest

        #Tall Tall Heights
        #Treasure chests
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Past the icy Chips Challenge", 2786 + treasure_index_offset, logic.has_vertical_movement), #Tear Seed chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Lonely chest", 2428 + treasure_index_offset, logic.has_vertical_movement), #Ether
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Past the 2nd icy Chips Challenge", 2788 + treasure_index_offset, logic.has_vertical_movement), #Tear Seed chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Past the 3rd icy Chips Challenge", 1254 + treasure_index_offset, logic.has_vertical_movement), #Potion chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Above the Boomer Society", 2844 + treasure_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Z-Potion Pouch chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Above the Triton Shrine", 2795 + treasure_index_offset, logic.has_vertical_movement or state.has("Item - Triton Stone", player)), #Ether chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Past the Chips Challenge fishing hut", 1578 + treasure_index_offset, lambda state: logic.has_vertical_movement or state.has("Item - Triton Stone", player)), #Frost Reaper chest
        #requires (Ibek or Triton Stone) and Quintar
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Tall stones and blue flowers", 2992 + treasure_index_offset, lambda state: (logic.has_vertical_movement or state.has("Item - Triton Stone", player)) and logic.has_horizontal_movement), #Potion Pouch chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Break the ice", 2744 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Radiance Northern Cave
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Parkour off the diamondsmith beneath the dead tree", 2810 + treasure_index_offset, logic.has_glide), #Judo Gi chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - East of the souvenir shop", 2993 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Money chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - Athenaeum Chips Challenge (or be a bird)", 2785 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Insignia Helm chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - East of the Athenaeum", 2565 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Potion Pouch chest
        LocationData("Tall Tall Heights", "Tall Tall Heights Chest - On the way to the Athenaeum", 2994 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Z-Potion chest
        LocationData("Tall Tall Heights", "Overpass Chest - Past Tall Tall Heights spiky tunnel to Salmon River", 3538 + treasure_index_offset), #1st Overpass (Cloudy Wind) Scrap
        LocationData("Tall Tall Heights", "Overpass Chest - Chilling by Nomads Outpost", 3676 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #(45, 215, -465) Overpass (Outpost) Scrap
        LocationData("Tall Tall Heights", "Underpass Chest - Tall Tall Heights spiky tunnel to Salmon River", 3672 + treasure_index_offset), #Underpass (Ice Pass) Scrap
        LocationData("Tall Tall Heights", "Underpass Chest - Tall Tall Heights spiky tunnel to Salmon River", 1601 + treasure_index_offset), #Underpass (Ice Pass) Potion
        LocationData("Tall Tall Heights", "Underpass Chest - Ice swimming instead of ice fishing", 3623 + treasure_index_offset), #(191, 172, -437) (Underwater) Underpass Scrap chest


        #NPCs
        #Todo NPCs Job Masters: Tall Tall Heights (Outpost) map has Master Chemist ID 3707 (491, 221, -389); gives you Chemist Seal in exchange for job mastery
        #Todo NPCs Player Options: (197, 192, -441) do we want a filter option to add the guys who fish things up for you
        #LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Z8_FisherInHut", 1549 + npc_index_offset),
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Gold above the Boomer Society", 1600 + npc_index_offset, logic.has_vertical_movement and logic.has_horizontal_movement), #Ingot
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Hop along spike mountain to Gold", 2853 + npc_index_offset, lambda state: logic.has_vertical_movement or state.has("Item - Triton Stone", player)), #Dust
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Melted snow Gold past the chest east of the Athenaeum", 2847 + npc_index_offset, lambda state: (logic.has_vertical_movement or state.has("Item - Triton Stone", player)) and logic.has_horizontal_movement), #Ingot
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Chip Challenge himself", 2388 + npc_index_offset, lambda state: logic.has_vertical_movement or state.has("Item - Triton Stone", player)),
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Gold by the breakable ice wall", 2814 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ingot
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Come back with the bird for Gold", 2845 + npc_index_offset, logic.has_glide), #Ingot
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Treacherous landing Gold above the spikes", 1584 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ore
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Gold tucked in melted snow past the Chips Challenge east of shrine", 2846 + npc_index_offset, logic.has_vertical_movement), #Ore
        LocationData("Tall Tall Heights", "Tall Tall Heights NPC - Gold past the Athenaeum Chips Challenge", 1602 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Dust
        LocationData("Tall Tall Heights", "Overpass NPC - Gold past Tall Tall Heights spiky tunnel to Salmon River", 2710 + npc_index_offset), #1st Gold Dust Overpass (Cloudy Wind)

        #Summons Todo: descriptivize and implement
        #498, 218, -412
        #LocationData("Tall Tall Heights", "Tall Tall Heights Summon - Pamoa from SIce_Summon", 1136 + summon_index_offset),

        #Northern Cave
        #Treasure chests
        LocationData("Northern Cave", "Northern Cave Chest - Island in the ice", 2787 + treasure_index_offset), #Tear Seed chest
        LocationData("Northern Cave", "Northern Cave Chest - Ominous Chips Challenge cave", 1579 + treasure_index_offset), #Ice Cell Key chest
        LocationData("Northern Cave", "Northern Cave Chest - Chip mimic", 1552 + treasure_index_offset, logic.has_horizontal_movement and logic.has_vertical_movement), #Apprentice chest
        LocationData("Northern Cave", "Northern Cave Chest - Past the wiggly block spike pit", 3001 + treasure_index_offset, logic.has_vertical_movement), #Money chest

        #NPCs
        LocationData("Northern Cave", "Northern Cave NPC - Gold past the wiggly block spike pit", 2815 + npc_index_offset, logic.has_vertical_movement), #Ore

        #Lands End
        #Treasure chests
        LocationData("Lands End", "Lands End Chest - Definitely requires Quintar *wink* among the first spikes 1", 2849 + treasure_index_offset), #Ether chest
        LocationData("Lands End", "Lands End Chest - Definitely requires Quintar *wink* among the first spikes 2", 3003 + treasure_index_offset), #Potion chest
        LocationData("Lands End", "Lands End Chest - Brave the spikes to climb the northern peak", 3002 + treasure_index_offset), #Money chest
        LocationData("Lands End", "Lands End Chest - To defeat the Huns", 2740 + treasure_index_offset), #Blue Cape chest
        LocationData("Lands End", "Lands End Chest - Tucked up high against River Cats Ego", 1692 + treasure_index_offset), #Blue Cape chest
        LocationData("Lands End", "Lands End Chest - In spikes and storm", 1358 + treasure_index_offset, lambda state: state.has("Item - Progressive Quintar Flute", player, 2)), #Defender chest
        LocationData("Lands End", "Lands End Chest - Fancy some spikes cliffdiving?", 1693 + treasure_index_offset), #Rune Ward chest
        LocationData("Lands End", "Lands End Chest - By the lovely owl tree", 1561 + treasure_index_offset), #Callisto Stone chest
        LocationData("Lands End", "Lands End Chest - Inside the shrine", 3017 + treasure_index_offset), #Ether chest
        LocationData("Lands End", "Overpass Chest - Lonely mountain ledge below owl shrine", 3678 + treasure_index_offset, logic.has_glide), #(191, 177, -214) 9th Scrap on main Overpass map

        #NPCs
        LocationData("Lands End", "Lands End NPC - Lets get down to business in the mountains for Gold", 2848 + npc_index_offset), #Ingot
        LocationData("Lands End", "Lands End NPC - Pillar Gold by River Cats Ego", 2850 + npc_index_offset), #Ore
        LocationData("Lands End", "Lands End NPC - Gold in spikes and storm", 2851 + npc_index_offset, lambda state: state.has("Item - Progressive Quintar Flute", player, 2)), #Dust
        LocationData("Lands End", "Lands End NPC - Gold behind the shrine", 2852 + npc_index_offset), #Ingot
        LocationData("Lands End", "Lands End NPC - Owl Drum", 1176 + npc_index_offset), #Todo make the owl drum sparkle despawn after you pick up this check; it stays rn if you don't have the owl drum item

        #Slip Glide Ride
        #Treasure chests
        LocationData("Slip Glide Ride", "Slip Glide Ride Chest - Back out to 1st room", 2554 + treasure_index_offset, lambda state: state.has("Item - Red Door Key", player, 1)), #Money chest
        LocationData("Slip Glide Ride", "Slip Glide Ride Chest - Climb up and fall down", 1172 + treasure_index_offset), #Plate of Lion chest
        LocationData("Slip Glide Ride", "Slip Glide Ride Chest - Sparks and tar", 1298 + treasure_index_offset), #Red Door Key chest
        LocationData("Slip Glide Ride", "Slip Glide Ride Chest - To the left through 2nd red lock", 1698 + treasure_index_offset, lambda state: state.has("Item - Red Door Key", player, 2)), #Red Door Key chest
        LocationData("Slip Glide Ride", "Slip Glide Ride Chest - Through 1st red lock", 1716 + treasure_index_offset, lambda state: state.has("Item - Red Door Key", player, 1)), #Red Door Key chest
        LocationData("Slip Glide Ride", "Slip Glide Ride Chest - Past the mean Ibek jump", 1282 + treasure_index_offset, lambda state: state.has("Item - Red Door Key", player, 1)), #Sages Walker chest
        LocationData("Slip Glide Ride", "Slip Glide Ride Chest - Nickelodeon slime time :)", 1269 + treasure_index_offset), #Seekers Garb chest

        #Crystals
        LocationData("Slip Glide Ride", "Slip Glide Ride Crystal - Summoner", 1714 + crystal_index_offset, lambda state: state.has("Item - Red Door Key", player, 3)),

        #Sequoia Athenaeum
        #Treasure chests
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - Atop the shelves above the books door", 2932 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #(412, 200, -551) Spellsword Helm chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - Bullshit booksmart Chips Challenge", 2569 + treasure_index_offset, logic.has_vertical_movement), #(403, 199, -547) Z-Potion Pouch chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - Braindumb Chips Challenge", 2322 + treasure_index_offset), #(415, 180, -570) Ice Puzzle Key chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - 3rd library Chips Challenge", 2375 + treasure_index_offset, lambda state: state.has("Item - Ice Puzzle Key", player, 1) and logic.has_vertical_movement), #(396, 180, -570) Ice Puzzle Key chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - Chips Challenge ice squared", 2341 + treasure_index_offset, lambda state: state.has("Item - Ice Puzzle Key", player, 2) and logic.has_vertical_movement), #(396, 164, -570) Ice Puzzle Key chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - Chips Challenge we cheated on this one", 2371 + treasure_index_offset, lambda state: state.has("Item - Ice Puzzle Key", player, 3) and logic.has_vertical_movement), #(415, 164, -572) Ice Puzzle Key chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - Triple Chip Challenge", 2372 + treasure_index_offset, lambda state: state.has("Item - Ice Puzzle Key", player, 4) and logic.has_vertical_movement), #(434, 164, -570) Ice Puzzle Key chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - Shattered labyrinth Chips Challenge", 2373 + treasure_index_offset, lambda state: state.has("Item - Ice Puzzle Key", player, 5) and logic.has_vertical_movement), #(424, 148, -570) Ice Puzzle Key chest
        LocationData("Sequoia Athenaeum", "Sequoia Athenaeum Chest - You expected another Chips Challenge, but it was me, Dio!", 2335 + treasure_index_offset, lambda state: state.has("Item - Ice Puzzle Key", player, 6) and logic.has_vertical_movement), #(415, 131, -565) Skeleton Key chest

        #Northern Stretch
        #Treasure chests
        LocationData("Northern Stretch", "Overpass Chest - At the base of Summoners Lookout", 3655 + treasure_index_offset), #Northern Stretch map in Overpass (Outpost)

        #Castle Ramparts
        #Treasure chests
        LocationData("Castle Ramparts", "Castle Ramparts Chest - Tucked beside eastern turret", 1547 + treasure_index_offset), #(443, 206, -378) Money chest
        LocationData("Castle Ramparts", "Castle Ramparts Chest - Below the crystal", 2908 + treasure_index_offset, logic.has_glide), #(407, 228, -383) Castle Ramparts map chest
        LocationData("Castle Ramparts", "Castle Ramparts Chest - Jump down from eastern save point", 2742 + treasure_index_offset, logic.has_glide), #(440, 227, -386) Conquest chest
        LocationData("Castle Ramparts", "Castle Ramparts Chest - Jump down from western save point", 2741 + treasure_index_offset, logic.has_glide), #(369, 227, -386) Rune Sword chest
        #Technically Castle Sequoia but they're in a locked room only accessible from Ramparts
        LocationData("Castle Ramparts", "Castle Sequoia Chest - Locked Ramparts storage room 1", 2758 + treasure_index_offset, lambda state: state.has("Item - Rampart Key", player) and logic.has_glide), #(375, 232, -452) (Skums) Decapitator chest
        LocationData("Castle Ramparts", "Castle Sequoia Chest - Locked Ramparts storage room 2", 3657 + treasure_index_offset, lambda state: state.has("Item - Rampart Key", player) and logic.has_glide), #(371, 231, -457) (Skums) Castle Sequoia map chest

        #NPCs
        LocationData("Castle Ramparts", "Castle Ramparts NPC - Western Gold above spikes", 2843 + npc_index_offset, logic.has_glide), #(354, 231, -429) Ingot
        LocationData("Castle Ramparts", "Castle Ramparts NPC - Eastern Gold above spikes", 2842 + npc_index_offset, logic.has_glide), #(458, 231, -436) Ore

        #Crystals
        LocationData("Castle Ramparts", "Castle Ramparts Crystal - Beastmaster (say high to the Ramparts Demon!)", 1370 + crystal_index_offset, logic.has_glide), #(404, 243, -386)

        #The Chalice of Tar
        #Treasure chests
        LocationData("The Chalice of Tar", "The Chalice of Tar Chest - At the tippy-top", 3544 + treasure_index_offset, logic.has_vertical_movement), #The Chalice of Tar map chest
        LocationData("The Chalice of Tar", "The Chalice of Tar Chest - Dont let your feathers touch the tar", 2587 + treasure_index_offset), #Vermillion Book chest
        LocationData("The Chalice of Tar", "The Chalice of Tar Chest - Post tar tunnel", 2806 + treasure_index_offset), #Windsong chest

        #NPCs
        #Todo NPCs Job Masters: The Chalice of Tar has Master Mimic ID 3606 (526, 234, -438); gives you Mimic Seal in exchange for job mastery
        LocationData("The Chalice of Tar", "The Chalice of Tar NPC - Gold sparkling above the Overpass on the way up", 2841 + npc_index_offset), #Ore

        #Crystals
        LocationData("The Chalice of Tar", "The Chalice of Tar Crystal - Biiiiiig glide to the Mimic", 3701 + crystal_index_offset),

        #Flyers Crag
        #Treasure chests
        LocationData("Flyers Crag", "Flyers Crag Chest - You cant miss it", 3656 + treasure_index_offset), #(658, 216, -170) Flyers Crag map chest
        
        #NPCs
        LocationData("Flyers Crag", "Flyers Crag NPC - Gold twinsies the 1st south of Ganymede Shrine", 2820 + npc_index_offset), #(695, 137, -159) Dust
        LocationData("Flyers Crag", "Flyers Crag NPC - Gold twinsies the 2nd south of Ganymede Shrine", 2819 + npc_index_offset), #(686, 132, -162) Ingot

        #Flyers Lookout
        #Treasure chests
        #There are no checks here unless an Overpass Scrap shows up

        #Jidamba Tangle
        #Treasure chests
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Inside overgrown building E of Eaclaneya", 1629 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Demon Plate chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Up a tree in north foliage", 3024 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Ether chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Along a river through the foliage", 3026 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Ether chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Atop overgrown building E of Eaclaneya", 3028 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Ether chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Tucked against eastern side of Eaclaneya", 2801 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Flame Guard chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Tucked against western side of Eaclaneya", 2802 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Flamespike chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Smack in the center of the foliage", 1632 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Foliage Key chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - NW foliage", 2807 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Partizan chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Tucked below NW foliage", 3025 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Potion chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Atop Eaclaneya", 2808 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Rune Bow chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Fly down from Weaver Outpost to pedestal", 2803 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Siege Bow chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Island in the river through the foliage", 3011 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Tower Shield chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - North of foliage river", 3027 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Z-Potion chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Accompanied by orange cave flowers", 1435 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Cave Key chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Hop from underground root to sneaky passage pond", 2798 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Ravens Cloak chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Underground sneaky passage by NE cave exit", 2797 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Ravens Hood chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Smack in the center of the canopy", 1631 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Canopy Key chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Up in the canopy south of shrine", 1171 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Demon Helm chest
        LocationData("Jidamba Tangle", "Jidamba Tangle Chest - Eaclaneya entrance hall", 2919 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #Jidamba Tangle map chest

        #NPCs
        #Todo NPCs Missable: Z54_ChloeFishing ID 2775 gives you the Super Rod (828, 119, 99)
        #Todo NPCs Job Masters: Jidamba Tangle (Outpost) has Master Weaver ID 3579 (627, 140, 77); gives you Weaver Seal in exchange for job mastery
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Splish splash Diamond", 2871 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Dust
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Diamond hot girl summer on the beach", 2873 + npc_index_offset), #Dust
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Damp Diamond lurking beneath diamondsmith", 2869 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ingot
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Diamond at southern mouth of cave", 2874 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ingot
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Fly from Summoners weeping tree to hot tub Diamond", 2876 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ingot
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Splash Mountain Diamond (pool at S end of canopy)", 2870 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ore
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Diamond atop broken ruins along the beach", 2872 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ore
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Diamond atop broken ruins by the Summoner tree", 2875 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ore
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Splash Mountain Gold (pool at NE end of canopy)", 2900 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ore
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Diamond in the boughs above the shrine", 2898 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ingot
        LocationData("Jidamba Tangle", "Jidamba Tangle NPC - Canopy Gold above big lake", 2899 + npc_index_offset, logic.has_vertical_movement and logic.has_glide), #Ingot

        #Summons Todo: descriptivize and implement (672, 124, 106)
        #LocationData("Jidamba Tangle", "Jidamba Tangle Summon - Juses from SLife_Summon", 1134 + summon_index_offset),

        #Jidamba Eaclaneya
        #Treasure chests
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Climb the lamp in the south room", 2799 + treasure_index_offset, logic.has_glide and logic.has_vertical_movement), #Celestial Crown chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - At the end of spike hallway", 2755 + treasure_index_offset, logic.has_glide), #Flame Sword chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Monster cubby", 2920 + treasure_index_offset), #Jidamba Eaclaneya map chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Practice your swimming", 2282 + treasure_index_offset, logic.has_glide), #Ether Pouch chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Right side of the swimming puzzle", 2289 + treasure_index_offset, logic.has_glide), #Staff of Balance chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Glass elevator room", 2301 + treasure_index_offset, logic.has_glide), #Stardust Wand chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Underwater swimming puzzle", 2308 + treasure_index_offset, logic.has_glide), #Flameseeker chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Left side of underwater swimming puzzle", 2317 + treasure_index_offset, logic.has_glide), #Viridian Book chest
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Chest - Salmon Violin past the fish puzzles", 2288 + treasure_index_offset, logic.has_glide),

        #NPCs
        #1 Diamond Dust on Jidamba Eaclaneya Fish Floor map has been categorized under the Capital Pipeline

        #Crystals
        LocationData("Jidamba Eaclaneya", "Jidamba Eaclaneya Crystal - Weaver", 2403 + crystal_index_offset),

        #The Deep Sea
        #Treasure chests
        LocationData("The Deep Sea", "The Deep Sea Chest - Descend into undersea vent where the flesh eaters live 1", 3451 + treasure_index_offset), #(878, 39, -536) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Touching Jidamba", 3658 + treasure_index_offset), #Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Ruins just south of Jidamba 1", 3659 + treasure_index_offset), #Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Locked sunken house off Jidamba with mighty arch 1", 3660 + treasure_index_offset, lambda state: state.has("Item - Forgotten Key", player)), #(657, 53, 165) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Buried tunnel NW of Jidamba", 3661 + treasure_index_offset), #(545, 47, -31) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - By The Depths chasm SE of Shoudu Province", 3662 + treasure_index_offset), #(890, 51, -66) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Crumbling shrine 1", 3663 + treasure_index_offset), #(842, 53, -359) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Beside an undersea microruin NW of Tall Tall Heights", 3666 + treasure_index_offset), #(-23, 39, -557) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Underwater cove south of volcano", 3667 + treasure_index_offset), #(94, 59, 133) Deep Sea Scrap chest
        #next 2 scraps from The Deep Sea (Sand Bar)
        LocationData("The Deep Sea", "The Deep Sea Chest - Sunken shipwreck off west coast of Sara Sara Beach", 3664 + treasure_index_offset), #(-364, 53, -183) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Undersea valley S of Sara Sara Beach", 3665 + treasure_index_offset), #(-226, 49, 164) Deep Sea Scrap chest
        #next scrap from The Deep Sea (Shrooms)
        LocationData("The Deep Sea", "The Deep Sea Chest - Cavern below N coast of Tall Tall Heights", 3668 + treasure_index_offset), #(254, 53, -547) Deep Sea Scrap chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Descend into undersea vent where the flesh eaters live 2", 2767 + treasure_index_offset), #(872, 39, -517) Forgotten Key chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Crumbling shrine 2", 2290 + treasure_index_offset), #(838, 52, -357) Oven Mitt chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Ruins just south of Jidamba 2", 2937 + treasure_index_offset), #Paladin Wand chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Cheeky sunroof NW of Jidamba", 2589 + treasure_index_offset), #(582, 47, -51) Rampart Key chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Locked sunken house off Jidamba with mighty arch 2", 2766 + treasure_index_offset, lambda state: state.has("Item - Forgotten Key", player)), #(663, 54, 165) Soul Keeper chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Locked *wink* sunken house off Jidamba 1", 2768 + treasure_index_offset), #(649, 53, 195) Zether chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Locked *wink* sunken house off Jidamba 2", 3726 + treasure_index_offset), #(646, 53, 196) Zether Pouch chest
        LocationData("The Deep Sea", "The Deep Sea Chest - Quizard challenge below N coast of Tall Tall Heights", 595 + treasure_index_offset), #(270, 29, -591) Treasure Finder chest

        #NPCs
        LocationData("The Deep Sea", "The Deep Sea NPC - Locked *wink* sunken house 2 off Jidamba Diamond", 2519 + npc_index_offset), #(639, 54, 182) Dust
        LocationData("The Deep Sea", "The Deep Sea NPC - Locked *wink* sunken house 2 off Jidamba Gold", 2518 + npc_index_offset), #(648, 54, 180)  Dust
        #Todo Player Options: Carcinization victory condition (its crab tiem babey)
        LocationData("The Deep Sea", "The Deep Sea NPC - Burrow to burrow crab", 3409 + npc_index_offset), #(20, 53, 251) Crab 1
        LocationData("The Deep Sea", "The Deep Sea NPC - Tall tall crab S of volcano", 3426 + npc_index_offset), #(76, 76, 178) Crab 2
        LocationData("The Deep Sea", "The Deep Sea NPC - Crab in underwater cove south of volcano", 3427 + npc_index_offset), #(96, 60, 131) Crab 3
        LocationData("The Deep Sea", "The Deep Sea NPC - Zigzaggedy crab NW of Tall Tall Heights", 3428 + npc_index_offset), #(142, 51, -611) Crab 4
        LocationData("The Deep Sea", "The Deep Sea NPC - Crab strolling around the undersea block", 3429 + npc_index_offset), #(60, 53, -609) Crab 5
        LocationData("The Deep Sea", "The Deep Sea NPC - Crab clinging to SW underwater volcano slope", 3430 + npc_index_offset), #(54, 62, 155) Crab 6
        LocationData("The Deep Sea", "The Deep Sea NPC - Low low crab S of volcano", 3431 + npc_index_offset), #(128, 49, 196) Crab 7
        LocationData("The Deep Sea", "The Deep Sea NPC - Serpentine crab S of crab hole", 3432 + npc_index_offset), #(239, 53, -613) for some reason crab 8 is on (Depths Fix) submap
        LocationData("The Deep Sea", "The Deep Sea NPC - Patrolling crab S of crab hole", 3433 + npc_index_offset), #(254, 53, 215) Crab 9
        LocationData("The Deep Sea", "The Deep Sea NPC - Crab living on the edge S of crab hole", 3434 + npc_index_offset), #(306, 53, 224) Crab 10
        LocationData("The Deep Sea", "The Deep Sea NPC - Crab on a mission N of Tall Tall Heights", 3435 + npc_index_offset), #(288, 53, -620) Crab 11
        LocationData("The Deep Sea", "The Deep Sea NPC - Middle of nowhere sandy speedster crab", 3436 + npc_index_offset), #(58, 52, 244) Crab 12
        LocationData("The Deep Sea", "The Deep Sea NPC - Putt Putt Crab mows the lawn", 3437 + npc_index_offset), #(54, 52, 200) Crab 13
        LocationData("The Deep Sea", "The Deep Sea NPC - King of the middle of nowhere ocean crab", 3438 + npc_index_offset), #(52, 76, -616) Crab 14
        LocationData("The Deep Sea", "The Deep Sea NPC - Crab scuttling SE of volcano", 3439 + npc_index_offset), #(207, 53, 152) Crab 15
        LocationData("The Deep Sea", "The Deep Sea NPC - Crab people crab people", 3424 + npc_index_offset, lambda state: state.has("Item - Undersea Crab", player, 15)), #(256, 63, 113)
        LocationData("The Deep Sea", "The Deep Sea NPC - Fastest squid in the West", 3450 + npc_index_offset), #(-314, 64, -624) (swims in a fixed path; slightly slower than golden quintar but faster than royal salmon) Z35_SpeedOcto
        LocationData("The Deep Sea", "The Deep Sea NPC - Sunken shipwreck Gold off west coast of Sara Sara Beach 1", 2855 + npc_index_offset), #(-367, 53, -182) Dust
        LocationData("The Deep Sea", "The Deep Sea NPC - Sunken shipwreck Gold off west coast of Sara Sara Beach 2", 2857 + npc_index_offset), #(-356, 55, -167) Ingot
        LocationData("The Deep Sea", "The Deep Sea NPC - Sunken shipwreck Gold off west coast of Sara Sara Beach 3", 2856 + npc_index_offset), #(-370, 53, -173) Ore

        #Summons Todo: descriptivize and implement
        #LocationData("The Deep Sea", "The Deep Sea Summon - Coyote from SWater_Summon", 1140 + summon_index_offset), #(-60, 53, 202)

        #Jade Cavern
        #Treasure chests
        LocationData("Jade Cavern", "Jade Cavern Chest - Tell Archie to say hi to the Quizard", 3604 + treasure_index_offset), #(239, 99, -124) Jade Cavern map chest

        #NPCs
        #Todo NPCs CheckOrNot Job Masters: this guy trades you a thing for each job seal you've gotten from a job master for mastering that job
        #LocationData("Jade Cavern", "Jade Cavern NPC - Jade Cavern Map chest", 3603 + npc_index_offset), #(255, 91, -90)
        
        #Continental Tram
        #Treasure chests
        LocationData("Continental Tram", "Continental Tram Chest - Tickets please 1", 1844 + treasure_index_offset), #Continental Tram map chest
        LocationData("Continental Tram", "Continental Tram Chest - End of the line", 3012 + treasure_index_offset), #Nomads Guard chest
        LocationData("Continental Tram", "Continental Tram Chest - Tickets please 2", 1654 + treasure_index_offset), #Tram Key chest

        #NPCs
        LocationData("Continental Tram", "Continental Tram NPC - Diamond hanging out with the conscript 1", 2895 + npc_index_offset, lambda state: state.has("Item - Tram Key", player) or logic.has_swimming), #Dust
        LocationData("Continental Tram", "Continental Tram NPC - Diamond hanging out with the conscript 2", 2894 + npc_index_offset, lambda state: state.has("Item - Tram Key", player) or logic.has_swimming), #Ingot

        #Zones (End-Game)
        #Ancient Labyrinth
        #Treasure chests
        LocationData("Ancient Labyrinth", "Ancient Labyrinth Chest - Dungeon East sneaky hole in wall", 1274 + treasure_index_offset), #(-186, 125, -316) F2 Money chest
        LocationData("Ancient Labyrinth", "Ancient Labyrinth Chest - Dungeon West sneaky hole in wall", 2412 + treasure_index_offset), #(-190, 125, -316) F2 Archmage Vest chest
        LocationData("Ancient Labyrinth", "Ancient Labyrinth Chest - B1 Searching for greener pastures", 1738 + treasure_index_offset), #(-209, 87, -311) F3 Vita Crown chest
        LocationData("Ancient Labyrinth", "Ancient Labyrinth Chest - B2 North weird rebar hallway", 2924 + treasure_index_offset), #(-185, 63, -363) F4 Judgement chest
        LocationData("Ancient Labyrinth", "Ancient Labyrinth Chest - B2 East weird rebar hallway", 2926 + treasure_index_offset), #(-162, 63, -336) F4 Zether Pouch chest
        LocationData("Ancient Labyrinth", "Ancient Labyrinth Chest - B4 Tar pit platform", 3649 + treasure_index_offset), #(-185, 38, -301) F6 Ancient Labyrinth map chest
        LocationData("Ancient Labyrinth", "Ancient Labyrinth Chest - Dogheaded dogshit boss", 2591 + treasure_index_offset), #(-219, 27, -350) F7 Mirror Shield chest

        #NPCs
        LocationData("Ancient Labyrinth", "Ancient Labyrinth NPC - Dungeon East sneaky hole in wall Diamond", 2881 + npc_index_offset), #(-186, 125, -300) F2 Ingot
        LocationData("Ancient Labyrinth", "Ancient Labyrinth NPC - Sneaky hole in wall Diamond in entry touchdown room", 2880 + npc_index_offset), #(-182, 126, -326) F2 Ore
        LocationData("Ancient Labyrinth", "Ancient Labyrinth NPC - B1 Thats right, Diamond goes in the bluish-white square hole", 2882 + npc_index_offset), #(-200, 98, -334) F3 Ingot

        #The Sequoia
        #Treasure chests
        LocationData("The Sequoia", "The Sequoia Chest - Waterfall climb sneaky hollow", 2934 + treasure_index_offset), #(-286, 90, -539) Stealth Cape chest
        LocationData("The Sequoia", "The Sequoia Chest - Balanced on bark", 2437 + treasure_index_offset), #(-250, 174, -512) Battle Band chest
        LocationData("The Sequoia", "The Sequoia Chest - Back indoors then follow water channel outside", 2935 + treasure_index_offset), #(-296, 182, -533) Sange chest
        LocationData("The Sequoia", "The Sequoia Chest - Waterfall climb sneaky eastern exit", 2884 + treasure_index_offset), #(-223, 118, -541) Zether Pouch chest
        LocationData("The Sequoia", "The Sequoia Chest - Go out on a limb", 2887 + treasure_index_offset), #(-244, 168, -498) Z-Potion Pouch chest
        LocationData("The Sequoia", "The Sequoia Chest - Back indoors by water channel", 2933 + treasure_index_offset), #(-282, 182, -528) Aphotic Edge chest
        LocationData("The Sequoia", "The Sequoia Chest - Post-boss victory pedestal", 2451 + treasure_index_offset), #(-272, 241, -544) The Hand of Midas chest
        
        #NPCs
        LocationData("The Sequoia", "The Sequoia NPC - Low-hanging Diamond fruit", 2885 + npc_index_offset), #(-223, 160, -530) Dust
        LocationData("The Sequoia", "The Sequoia NPC - Waterfall climb sneaky eastern exit Diamond", 2883 + npc_index_offset), #(-237, 117, -563) Ore
        LocationData("The Sequoia", "The Sequoia NPC - Diamond glittering on a bough", 2886 + npc_index_offset), #(-311, 160, -540) Ore
        LocationData("The Sequoia", "The Sequoia NPC - Post-boss victory Diamond 1", 2889 + npc_index_offset), #(-269, 240, -545) Dust
        LocationData("The Sequoia", "The Sequoia NPC - Post-boss victory Diamond 2", 2890 + npc_index_offset), #(-268, 240, -547) Ingot
        LocationData("The Sequoia", "The Sequoia NPC - Post-boss victory Diamond 3", 2888 + npc_index_offset), #(-275, 240, -546) Ore

        #The Depths
        #Treasure chests
        LocationData("The Depths", "The Depths Chest - Down among glowing blue seaweed between Poko Poko Desert & Jidamba 1", 2588 + treasure_index_offset), #(-358, 1, 18) Cerulean Book chest
        LocationData("The Depths", "The Depths Chest - Down among glowing blue seaweed between Poko Poko Desert & Jidamba 2", 2714 + treasure_index_offset), #(-357, 2, 20) #Z-Potion chest

        #NPCs
        LocationData("The Depths", "The Depths NPC - S of Jidamba Diamond on blue rock 1", 2865 + npc_index_offset), #(692, 20, -618) Dust
        LocationData("The Depths", "The Depths NPC - S of Jidamba Diamond by seaweed river 1", 2868 + npc_index_offset), #(823, 17, -595) Dust
        LocationData("The Depths", "The Depths NPC - Floating rock Diamond SE of Volcano 1", 2891 + npc_index_offset), #(161, 20, 240) Dust
        LocationData("The Depths", "The Depths NPC - Diamond dive beside sunken shipwreck 1", 1214 + npc_index_offset), #(-377, 20, -220) Ingot
        LocationData("The Depths", "The Depths NPC - Diamond dive beside sunken shipwreck 2", 2859 + npc_index_offset), #(-373, 19, -261) Ingot
        LocationData("The Depths", "The Depths NPC - S of Jidamba Diamond on blue rock 2", 2863 + npc_index_offset), #(784, 17, -611) Ingot
        LocationData("The Depths", "The Depths NPC - S of sunken town on blue rock", 2866 + npc_index_offset), #(629, 20, -615) Ingot
        LocationData("The Depths", "The Depths NPC - Floating rock Diamond SE of Volcano 2", 2893 + npc_index_offset), #(180, 20, 255) Ingot
        LocationData("The Depths", "The Depths NPC - Yellow flower Diamond W of Sara Sara Beach", 1213 + npc_index_offset), #(932, 19, -199) Ore
        LocationData("The Depths", "The Depths NPC - Sneaky Diamond W of Sara Sara Beach", 2858 + npc_index_offset), #(924, 20, -235) Ore
        LocationData("The Depths", "The Depths NPC - S of Jidamba Diamond by seaweed river 2", 2864 + npc_index_offset), #(760, 12, -612) Ore
        LocationData("The Depths", "The Depths NPC - S of Jidamba Diamond by seaweed river 3", 2867 + npc_index_offset), #(722, 20, -604) Ore
        LocationData("The Depths", "The Depths NPC - Floating rock Diamond SE of Volcano 3", 2892 + npc_index_offset), #(189, 30, 235) Ore
        LocationData("The Depths", "The Depths NPC - Follow barnacled meat branches for Diamond 1", 2861 + npc_index_offset), #(-308, 12, 132) Dust
        LocationData("The Depths", "The Depths NPC - Follow barnacled meat branches for Diamond 2", 2862 + npc_index_offset), #(-303, 14, 183) Ingot
        LocationData("The Depths", "The Depths NPC - Follow barnacled meat branches for Diamond 3", 2860 + npc_index_offset), #(-359, 10, 162) Ore

        #Castle Sequoia
        #Treasure chests
        #Map and Decapitator chests categorized in Castle Ramparts since they're in a locked room there requiring the Ramparts key
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Hop through keyhole over lava", 2515 + treasure_index_offset), #(422, 169, -406) (Skums) Zether Pouch chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Stared at by lava miniboss", 1465 + treasure_index_offset), #(427, 170, -441) (Skums) Z-Potion chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Enjoy riding lava shrooms", 1447 + treasure_index_offset), #(409, 169, -406) (Skums) Z-Potion Pouch chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Biiig bounce!", 1472 + treasure_index_offset), #(375, 153, -405) (Bounce) Beads of Defense chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Bounce up!!", 2949 + treasure_index_offset), #(401, 151, -404) (Bounce) Ether chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Bounce around!", 2948 + treasure_index_offset), #(401, 151, -424) (Bounce) Fenix Syrup chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Bounce right!", 2945 + treasure_index_offset), #(434, 154, -441) (Bounce) Potion chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Bounce up!", 2922 + treasure_index_offset), #(395, 155, -453) (Bounce) Protector chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Chilly uno in Chips Challenge of doom", 2927 + treasure_index_offset), #(387, 134, -431) (Ice) Kings Guard chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Chilly duo in Chips Challenge of doom", 1492 + treasure_index_offset), #(387, 134, -427) (Ice) Royal Guard chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - One fish", 2479 + treasure_index_offset), #(401, 119, -415) (Fish) Dream Hunter chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Two fish", 2509 + treasure_index_offset), #(388, 122, -445) (Fish) Nightingale chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Redfish bluefish", 2484 + treasure_index_offset), #(397, 119, -415) (Fish) Oily Sword chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Bounce for your life", 2510 + treasure_index_offset), #(364, 85, -424) (2D) Paladin Wand chest
        LocationData("Castle Sequoia", "Castle Sequoia Chest - Throne snacks", 2505 + treasure_index_offset), #(401, 250, -478) (Throne) New World Stone chest

        #NPCs
        #Todo NPCs CheckOrNot: this gives you a Gaea Shard if you're stuck
        #LocationData("Castle Sequoia", "Castle Sequoia NPC - Z58_StrandedShard", 3785 + npc_index_offset), #(401, 183, -382)
        #Todo NPCs Blocker: i think this guy might only show up in the vanilla game's randomizer? checks if Z58_EleOn (Z58 is Castle Sequoia); Z58Progression_Gate ID 3824 (400, 250, -478)

        #The New World
        #Todo Player Options: if astley is the goal, make the requirement for entering the new world be the number of crystals the player picked to win
        #Treasure chests
        LocationData("The New World", "The New World Chest - NW lavafall", 2930 + treasure_index_offset), #(-134, 8, 230) Lunar Mail chest
        LocationData("The New World", "The New World Chest - Desolate peninsula past bounce shrooms", 2931 + treasure_index_offset, logic.has_vertical_movement and logic.has_glide), #(-11, 12, -577) Mages Pike chest
        LocationData("The New World", "The New World Chest - Tiny shrooms keep shed", 1938 + treasure_index_offset), #(-85, 8, 142) The New World map chest

    ]

    return location_table