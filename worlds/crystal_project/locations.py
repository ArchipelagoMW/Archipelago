from typing import List, Optional, Callable, NamedTuple
from BaseClasses import CollectionState
from .options import CrystalProjectOptions
from .rules import CrystalProjectLogic
from .constants.jobs import *
from .constants.keys import *
from .constants.key_items import *
from .constants.ap_regions import *
from .constants.display_regions import *
from .constants.teleport_stones import *
from .constants.crystal_locations import *

class LocationData(NamedTuple):
    ap_region: str
    name: str
    code: int
    rule: Optional[Callable[[CollectionState], bool]] = None
    regionsanity: bool = False

treasure_index_offset = 1
npc_index_offset = 10000
crystal_index_offset = 100000
boss_index_offset = 1000000
shop_index_offset = 10000000
regionsanity_index_offset = 100000000

def get_locations(player: int, options: CrystalProjectOptions | None) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    location_table: List[LocationData] = [
        #Zones (Beginner)
        #Spawning Meadows
        #Treasure chests
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - On cliff north of spawn", 101 + treasure_index_offset), #Money chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Under overpass", 292 + treasure_index_offset), #Money chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Jump on Nan", 41 + treasure_index_offset), #Burglars Glove chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Above waterfall", 17 + treasure_index_offset), #Cedar Staff chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Behind Nan house", 61 + treasure_index_offset), #Cedar Wand chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Promontory south of waterfall", 54 + treasure_index_offset), #Cleaver chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Jump on secret tunnel chest", 5 + treasure_index_offset), #Fenix Juice chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - On path to Delende", 49 + treasure_index_offset), #Fenix Juice chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Secret tunnel", 47 + treasure_index_offset), #Stabbers chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - On ledge jump from tree", 50 + treasure_index_offset), #Stout Shield chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Cross trees and jump down", 38 + treasure_index_offset), #Tincture chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - West of spawn", 1 + treasure_index_offset), #Tonic chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - In cave NW of spawn", 2 + treasure_index_offset), #Tonic chest
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Chest - Mountain summit jump on Nan", 1142 + treasure_index_offset), #Tonic Pouch chest

        #NPCs
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Pouch Nan", 53 + npc_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Secret Herb near Shaku", 627 + npc_index_offset), #Secret Herb 0 Fixed Missable
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Promontory south of waterfall Secret Herb", 297 + npc_index_offset), #(48, 112, -36) Secret Herb 1 Fixed Missable
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Secret Herb past mountain summit chest", 545 + npc_index_offset), #(79, 112, -30) Secret Herb 2 Fixed Missable
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Cross trees and jump down for Secret Herb", 546 + npc_index_offset), #(43, 104, -8) Secret Herb 3 Fixed Missable
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Map Nan", 84 + npc_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Nan Stew", 14 + npc_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Butterfly Goo", 194 + npc_index_offset, lambda state: state.has(BLACK_SQUIRREL, player, 3)), #Tree Fairy NPC seems to have the dialogue for this (ID 194)
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Buttersquirrel on tree SW of spawn", 264 + npc_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Buttersquirrel on tree NW of spawn", 296 + npc_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Buttersquirrel on tree near lampposts", 110 + npc_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Buttersquirrel on Mario jump tree", 3085 + npc_index_offset),

        #Delende
        #Treasure chests
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - In front of camp", 263 + treasure_index_offset), #Money chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - In front of fish hatchery lower level", 210 + treasure_index_offset), #Money chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Return from fish hatchery", 34 + treasure_index_offset), #Bracer chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Looking for love in all the high places (glide to the heart tarn)", 1554 + treasure_index_offset, lambda state: logic.has_swimming(state) and logic.has_glide(state)), #Chartreuse chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Mushroom underpass", 262 + treasure_index_offset), #Cotton Hood chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Fallen log parkour", 208 + treasure_index_offset), #Earring chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Across river", 213 + treasure_index_offset), #Earring chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Next to river", 43 + treasure_index_offset), #Underground Ether chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Under ambush tree", 212 + treasure_index_offset), #Fenix Juice chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - On west mountainside", 209 + treasure_index_offset), #Iron Sword chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Across river from fish hatchery", 123 + treasure_index_offset), #Looters Ring chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - High up west mountainside", 33 + treasure_index_offset), #Mages Robe chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Up near hatchery", 169 + treasure_index_offset), #Protect Amulet chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Outside spooky cave", 27 + treasure_index_offset), #Storm Hood chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - In fish hatchery", 39 + treasure_index_offset), #Tincture chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Fish hatchery approach", 79 + treasure_index_offset), #Tincture chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Under tree", 261 + treasure_index_offset), #Tincture chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Top of spooky cave", 73 + treasure_index_offset), #Tincture Pouch chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Troll", 451 + treasure_index_offset), #Tincture Pouch chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Off north path", 259 + treasure_index_offset), #Tonic chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Before Proving Meadows", 216 + treasure_index_offset), #Tonic Pouch chest
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - In front of fish hatchery below tree", 2997 + treasure_index_offset), #Tonic Pouch chest

        #NPCs
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Astley gives you a home point stone", 28 + npc_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Dog Bone in spooky cave", 1915 + npc_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Dog Bone Guy", 31 + npc_index_offset, lambda state: state.has(DOG_BONE, player, 3)),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Dog Bone south of Soiled Den", 184 + npc_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Dizzy noob chucks something at your face", 831 + npc_index_offset), #(276, 116, -204); Fervor Charm
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Not-at-all shady guy", 124 + npc_index_offset), #(181, 132, -200); Rotten Salmon
        #Todo NPCs Shortcuts: shortcut girl (Z2_Collector Sister ID 3769 (169, 132, -89))
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Cartographer", 1153 + npc_index_offset), #guy who gives you a map of Delende if you don't have one (Z2_MapMan (198, 131, -74)) Fixed Missable
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Fish at the hatchery", 121 + npc_index_offset, lambda state: state.has("Item - Flimsy Rod", player) and state.has("Item - Plug Lure", player)),  # Fisher (Z2_FisherOnDock ID 121 (166, 133, -208))
        #Todo NPCs Shortcuts: Rabbit Claws shortcut guy (Z2_RoosterFeetGuy ID 74(281, 128, -159))

        #Grans House (Delende)
        #Treasure chests
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Gran's House 1", 87 + treasure_index_offset), #(126, 128, -58) style: blank
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Gran's House 2", 100 + treasure_index_offset), #(127, 128, -58) style: weapon
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Gran's House 3", 177 + treasure_index_offset), #(137, 128, -57) style: consumable
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Chest - Gran's House 4", 178 + treasure_index_offset), #(137, 128, -56) style: consumable

        #Basement (Somehow Not Delende)
        #Treasure chests
        LocationData(DELENDE_AP_REGION, "Basement Chest - Gran...?", 179 + treasure_index_offset), #Empty chest
        LocationData(DELENDE_AP_REGION, "Basement Chest - Gran......?", 180 + treasure_index_offset), #Digested Head chest
        LocationData(BELOW_GRAN_AP_REGION, "Underpass Chest - Cracks in Gran's foundation", 3653 + treasure_index_offset), #(126, 115, -102) Basement map chest
        LocationData(BELOW_GRAN_AP_REGION, "Underpass Chest - Gran's subbasement pair 1", 181 + treasure_index_offset), #(129, 98, -111) Fenix Juice Pouch chest
        LocationData(BELOW_GRAN_AP_REGION, "Underpass Chest - Gran's subbasement pair 2", 182 + treasure_index_offset), #(128, 98, -111) Plate of Wolf chest
        LocationData(BELOW_GRAN_AP_REGION, "Underpass Chest - Gran's subbasement loner", 3671 + treasure_index_offset), #(119, 98, -110) Underpass Scrap

        #Soiled Den
        #Treasure chests
        #Soiled Denlende
        LocationData(SOILED_DENLENDE_AP_REGION, SOILED_DEN_DISPLAY_NAME + " Chest - Riverside", 1155 + treasure_index_offset),  # (249, 116, -156) Tonic Pouch chest
        #The Bangler
        LocationData(THE_BANGLER_AP_REGION, SOILED_DEN_DISPLAY_NAME + " Chest - Lurking in the shadows by the Bangler", 218 + treasure_index_offset), #(311, 111, -96) Clamshell chest
        LocationData(THE_BANGLER_AP_REGION, SOILED_DEN_DISPLAY_NAME + " Chest - By the Bangler", 271 + treasure_index_offset), #(322, 111, -101) Clamshell chest
        LocationData(THE_BANGLER_AP_REGION, SOILED_DEN_DISPLAY_NAME + " Chest - Long river jump", 448 + treasure_index_offset), #(326, 111, -116) Dodge Charm chest

        #NPCs
        #Soiled Denlende
        LocationData(SOILED_DENLENDE_AP_REGION, SOILED_DEN_DISPLAY_NAME + " NPC - Dog Bone among the bones and flowers", 176 + npc_index_offset), #(296, 112, -155)

        #Pale Grotto
        #Treasure chests
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Across from fish island", 228 + treasure_index_offset), #(#316, 120, -262) Fenix Juice chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - North from save point", 144 + treasure_index_offset), #(307, 124, -345) Poisonkiss chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Entrance river hop", 229 + treasure_index_offset), #Tonic chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - On promontory", 2979 + treasure_index_offset), #Tincture Pouch chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Island 1", 3622 + treasure_index_offset, lambda state: logic.has_swimming(state)), #Underpass Scrap chest; somehow this is actually in the pale grotto and not the underpass
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Island 2", 3077 + treasure_index_offset, lambda state: logic.has_swimming(state)), #Z-Potion Pouch chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Tucked behind path to temple", 267 + treasure_index_offset), #Tincture chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Jumping puzzle", 226 + treasure_index_offset), #Storm Helm chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - South of temple", 136 + treasure_index_offset), #Money chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Temple antechamber", 222 + treasure_index_offset), #Toothpick chest
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Chest - Temple sanctuary", 1154 + treasure_index_offset), #Pale Grotto map chest
        LocationData(THE_PALE_GROTTO_AP_REGION, "Underpass Chest - Blue flower ledge between Pale Grotto & Soiled Den", 3621 + treasure_index_offset, lambda state: logic.has_swimming(state)), #(245, 116, -199) Underpass Scrap chest
        
        #NPCs
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " NPC - Reid gives you gently worn armor", 1166 + npc_index_offset), #Pale Grotto Temple map (Z2_ReidCamp (273, 122, -327)) gives you Ring Mail

        #Crystals
        LocationData(THE_PALE_GROTTO_AP_REGION, FENCER_JOB_CRYSTAL_LOCATION, 130 + crystal_index_offset),

        #Seaside Cliffs
        #Treasure chests
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - North across river from double giant box", 282 + treasure_index_offset), #Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Stonehenge", 150 + treasure_index_offset), #Bracer chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - ClamHaters Mulan jumping puzzle", 268 + treasure_index_offset), #Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - After ClamHater made a man out of you", 2981 + treasure_index_offset), #Tincture Pouch chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - South of ClamHater", 281 + treasure_index_offset), #Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - South of chest south of ClamHater", 286 + treasure_index_offset), #Tonic chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Climbing the seaside cliffs", 42 + treasure_index_offset), #Potion chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Three Amigos Uno", 1161 + treasure_index_offset), #Tonic chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Three Amigos Dos", 447 + treasure_index_offset), #Scope Bit chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Three Amigos Tres", 270 + treasure_index_offset), #Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Beneath encampment ledge", 217 + treasure_index_offset), #(310, 116, -68) Money chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - On jigsaw mountain 1", 449 + treasure_index_offset), #(213, 107, 27) Money chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - In cliffs nook south of encampment", 80 + treasure_index_offset), #(307, 113, -22) Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Below west Delende entrance", 273 + treasure_index_offset), #(275,108,-28) Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Above the eastern beach standing stones", 274 + treasure_index_offset), #(312, 95, 12) Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Below jigsaw mountain", 275 + treasure_index_offset), #(223, 94, 26) Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Island by the waterfalls", 277 + treasure_index_offset), #(259, 107, -18) Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - East of the river above the beach", 278 + treasure_index_offset), #(281, 98, -3) Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Along the eastern beach up the cliffs", 279 + treasure_index_offset), #(302, 101, 4) Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Parkour by the island waterfalls", 289 + treasure_index_offset), #(250, 104, -13) Fenix Juice chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - On jigsaw mountain 2", 157 + treasure_index_offset), #(218, 107, 23) Headgear chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - South of encampment on the canyon mountainside", 272 + treasure_index_offset), #(289, 110, -18) Jewel of Defense chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Downstream of the island waterfalls", 288 + treasure_index_offset), #(250, 98, -4) Tincture chest
        #Seaside Cliffs Beach
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - The little mermaid", 276 + treasure_index_offset), #Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Hop along the sea stacks south of the peninsula", 280 + treasure_index_offset), #Clamshell chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Peninsula past the standing stones jump puzzle", 205 + treasure_index_offset), #Storm Cap chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - MR SNIPS", 287 + treasure_index_offset), #Fenix Juice chest
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Atop sea stack east of the bay", 450 + treasure_index_offset), #Swimmers Top chest
        #Seaside Cliffs Valley
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Chest - Rocky cove down the lazy river", 269 + treasure_index_offset), #Clamshell chest
        
        #NPCs
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " NPC - ClamHater above the mist", 283 + npc_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " NPC - If you give a Manana Man a clam... (he will ask you for more)", 284 + npc_index_offset, lambda state: logic.has_enough_clamshells(state)),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " NPC - Diamond below the bay", 2896 + npc_index_offset, lambda state: logic.has_swimming(state)), #(343, 81, 0) Ore
        #Todo NPCs Job Masters: Seaside Cliffs Outpost map has Master Shaman ID 3572 (387, 155, -104); gives you Shaman Seal in exchange for job mastery

        #Draft Shaft Conduit
        #Treasure chests
        LocationData(DRAFT_SHAFT_CONDUIT_AP_REGION, DRAFT_SHAFT_CONDUIT_DISPLAY_NAME + " Chest - Straight shot", 82 + treasure_index_offset), #Torch chest
        LocationData(DRAFT_SHAFT_CONDUIT_AP_REGION, DRAFT_SHAFT_CONDUIT_DISPLAY_NAME + " Chest - Ring around the rosy", 81 + treasure_index_offset), #Tonic Pouch chest

        #Crystals
        LocationData(DRAFT_SHAFT_CONDUIT_AP_REGION, SHAMAN_JOB_CRYSTAL_LOCATION, 35 + crystal_index_offset),

        #Mercury Shrine
        #Treasure chests
        LocationData(MERCURY_SHRINE_AP_REGION, MERCURY_SHRINE_DISPLAY_NAME + " Chest - Pinnacle", 155 + treasure_index_offset, lambda state: state.has(MERCURY_STONE, player) or logic.has_vertical_movement(state)), #Contract chest

        #Yamagawa M.A.
        #Treasure chests
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Chest - Up first cliff", 2995 + treasure_index_offset), #Money chest
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Chest - Sneaky behind tree", 91 + treasure_index_offset), #Broadsword chest
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Chest - Tucked next to waterfall", 95 + treasure_index_offset), #Iron Guard chest
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Chest - Dead end", 3056 + treasure_index_offset), #Tonic chest
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Chest - Hidden stairway", 757 + treasure_index_offset), #Tonic Pouch chest
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Chest - Drop down to mountain balcony", 290 + treasure_index_offset), #Torpid Cuffs chest
        LocationData(YAMAGAWA_MA_AP_REGION, "Overpass Chest - Hop over from Yamagawa to dead tree by Fencers Keep", 3537 + treasure_index_offset), #(148, 151, -114) 6th Overpass Scrap on Overpass main map

        #NPCs
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " NPC - Hidden inside waterfall source", 628 + npc_index_offset, lambda state: logic.has_swimming(state)), #Autumns Oath
        #Todo NPCs Job Masters: Yamagawa M.A. Temple map has Master Scholar ID 3574 (59, 151, -98); gives you Scholar Seal in exchange for job mastery

        #Crystals
        LocationData(YAMAGAWA_MA_AP_REGION, SCHOLAR_JOB_CRYSTAL_LOCATION, 166 + crystal_index_offset),

        #Proving Meadows
        #Treasure chests
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Chest - Next to trial guard", 207 + treasure_index_offset), #Money chest
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Chest - Hop on shops to sneak behind waterfall", 258 + treasure_index_offset), #Battle Scythe chest
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Chest - Hidden behind the inn", 118 + treasure_index_offset), #Burglars Glove chest
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Chest - Tucked into waterfall nook", 2980 + treasure_index_offset), #Tincture Pouch chest
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Chest - Tarzan", 256 + treasure_index_offset), #Tonic chest
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Chest - On the climb up outside Skumparadise", 193 + treasure_index_offset), #Tonic Pouch chest

        #NPCs
        #NPCs Blocker: this guy checks whether you have enough crystals to pass; this is a blocker guy not a location check guy
        #LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " NPC - Crystal Checker", 128 + npc_index_offset),

        #Skumparadise (we're smushing Trial Caves into there)
        #Treasure chests
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Stairs are lava", 126 + treasure_index_offset), #Stalwart Shield chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Shroom dodging", 120 + treasure_index_offset), #Help the Prince chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Ride the shroom", 670 + treasure_index_offset), #Awake Ring chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Wall niche", 671 + treasure_index_offset), #Awake Ring chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Smaller wall niche", 669 + treasure_index_offset), #Tincture Pouch chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Lava-loving shrooms", 684 + treasure_index_offset), #Tonic Pouch chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Behind the lava shroom colonnade", 685 + treasure_index_offset), #Mana Ring chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - There and back again", 683 + treasure_index_offset), #Sharp Sword chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Accompanied by yellow flower in tunnel", 1110 + treasure_index_offset), #Fenix Juice chest
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Chest - Behind boss", 332 + treasure_index_offset), #Money chest

        #Crystals
        LocationData(SKUMPARADISE_AP_REGION, AEGIS_JOB_CRYSTAL_LOCATION, 68 + crystal_index_offset),

        #Zones (Advanced)
        #Capital Sequoia (smushed Capital Courtyard in)
        #Treasure chests
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Beyond the courtyard wall", 2671 + treasure_index_offset), #Tonic Pouch chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Inn room", 1388 + treasure_index_offset), #Craftwork Staff chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Second story by Master Rogue", 158 + treasure_index_offset), #Craftwork Dagger chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Magic store attic", 1389 + treasure_index_offset), #Craftwork Scythe chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Training ground parkour", 1390 + treasure_index_offset), #Craftwork Katana chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Behind Luxury store", 2651 + treasure_index_offset), #Craftwork Cap chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Locked in Luxury Store storage 1", 1533 + treasure_index_offset, lambda state: logic.has_key(state, LUXURY_KEY) and state.has(PROGRESSIVE_LUXURY_PASS, player)), #Fenix Syrup Pouch chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Locked in Luxury Store storage 2", 1532 + treasure_index_offset, lambda state: logic.has_key(state, LUXURY_KEY) and state.has(PROGRESSIVE_LUXURY_PASS, player)), #Lucky Briefs chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Locked in Luxury Store storage 3", 1531 + treasure_index_offset, lambda state: logic.has_key(state, LUXURY_KEY) and state.has(PROGRESSIVE_LUXURY_PASS, player)), #Lucky Socks chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Inn attic by Master Monk", 2656 + treasure_index_offset), #Craftwork Vest chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - By Master Warrior atop the Luxury Store", 2655 + treasure_index_offset), #Craftwork Shield chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Atop library bookcases", 1392 + treasure_index_offset), #Craftwork Sword chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Penguin sanctuary", 2654 + treasure_index_offset), #Craftwork Robe chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Gaea Shrine 1", 137 + treasure_index_offset), #Gaea Shard chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Gaea Shrine 2", 227 + treasure_index_offset), #Gaea Shard chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Gaea Shrine 3", 381 + treasure_index_offset), #Gaea Shard chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Gaea Shrine 4", 548 + treasure_index_offset), #Gaea Shard chest
        #Next check can be acquired with either Owl, Ibek, Quintar, or Gaea Stone; vanilla expects Gaea Stone so that's the logic were using
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Clerics Lounge", 1391 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_horizontal_movement(state) or state.has(GAEA_STONE, player)), #Craftwork Bow chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Instrducktor classroom", 1387 + treasure_index_offset), #Craftwork Axe chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Master Warlocks chambers atop Weapons R Us", 2732 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)), #Watering Can chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Master Wizards Library atop Weapons R Us", 168 + treasure_index_offset), #Craftwork Pages chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Fenced off in Armor Merchant alley", 2653 + treasure_index_offset), #Craftwork Helm chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Beneath grand staircase", 1393 + treasure_index_offset), #Craftwork Rapier chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Tucked into maze entrance hedge", 389 + treasure_index_offset), #Fang Pendant chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Down left maze path", 452 + treasure_index_offset), #Craftwork Wand chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Hop moat to maze", 863 + treasure_index_offset), #Craftwork Spear chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Accompanied by blue flower pair in maze", 390 + treasure_index_offset), #Craftwork Crown chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Below maze-cheating Lost Penguin", 388 + treasure_index_offset), #Gardeners Key chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Above maze fountain", 387 + treasure_index_offset), #Givers Ring chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Gardeners Shed 1", 2652 + treasure_index_offset, lambda state: logic.has_key(state, GARDENERS_KEY)), #Craftwork Mail chest
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Gardeners Shed 2", 2663 + treasure_index_offset, lambda state: logic.has_key(state, GARDENERS_KEY)), #Tuber Seed
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Chest - Gardeners Shed 3", 2664 + treasure_index_offset, lambda state: logic.has_key(state, GARDENERS_KEY)), #Tuber Seed

        #NPCs 
        #Todo NPCs Job Masters: Master Beatsmith ID 3560 (361, 170, -268); gives you Beatsmith Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Cleric ID 3568 (363, 166, -266); gives you Cleric Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Monk ID 3567 (394, 179, -295); gives you Monk Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Rogue ID 3571 (444, 167, -264); gives you Rogue Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Warlock ID 3570 (400, 171, -267); gives you Warlock Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Warrior ID 3566 (424, 182, -293); gives you Warrior Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Wizard ID 3569 (391, 168, -266); gives you Wizard Seal in exchange for job mastery
        #NPCs Blocker: Z14_ProgressionGate ID 3823 (403, 180, -367) requires 18 crystals; we think it"s an original-randomizer-only NPC blocking the way to the castle
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Home Point Stone duck", 560 + npc_index_offset), #Home Point Stone (403, 161, -265) Fixed Missable
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Impress the Luxury Equipment Shop Bouncer with 6 jobs collected", 51162 + npc_index_offset, lambda state: logic.has_jobs(state, 6)), #(419, 171, -289) Blocker-No-Longer, Fixed Missable, and Multichecks
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Impress the Luxury Equipment Shop Bouncer further with 11 jobs collected", 1162 + npc_index_offset, lambda state: logic.has_jobs(state, 11)), #(419, 171, -289)
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Plunder the Luxury storage and skip town to meet a very slow thief", 1529 + npc_index_offset, lambda state: logic.has_key(state, LUXURY_KEY) and state.has(PROGRESSIVE_LUXURY_PASS, player)), #(417, 171, -299) Fixed Missable
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Courtyard Chloe", 1661 + npc_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_horizontal_movement(state)), #Fly Lure (399, 155, -219) Fixed Missable
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Glinting Courtyard Key", 2486 + npc_index_offset), #Courtyard Key sparkle that appears if you miss Courtyard Reid in Salmon River (424, 150, -222) Fixed Missable
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Sparkling in the fountain", 2584 + npc_index_offset), #Plug Lure
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin on a tent", 605 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Speedy Lost Penguin on patrol", 584 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin kiosk keeper", 508 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin skulking in store alley", 565 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin on gender change bench porch", 1095 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin enjoying inn hospitality", 946 + npc_index_offset),
        # Progressive Location: 4 checks on the Penguin Keeper, must add a progressive location in the C# app every time you use one of these.
        # The original check that corresponds to the npc id should be last so that when it completes it stops showing up on your minimap.
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Bring 3 Lost Penguins to Penguin Keeper", 50531 + npc_index_offset, lambda state: state.has(LOST_PENGUIN, player, 3)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Bring 6 Lost Penguins to Penguin Keeper", 50532 + npc_index_offset, lambda state: state.has(LOST_PENGUIN, player, 6)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Bring 9 Lost Penguins to Penguin Keeper", 50533 + npc_index_offset, lambda state: state.has(LOST_PENGUIN, player, 9)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Bring all 12 Lost Penguins to Penguin Keeper", 531 + npc_index_offset, lambda state: state.has(LOST_PENGUIN, player, 12)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin trampling Clerics flowers", 564 + npc_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_horizontal_movement(state) or state.has(GAEA_STONE, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Sadist Sam gives you pain, you give Sadist Sam head(s)", 536 + npc_index_offset, lambda state: state.has(DIGESTED_HEAD, player, 3)), #name is ca69011a in Crystal Edit whyy lmao
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin wandering Magic Store rooftop garden", 573 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin atop sewer exit rooftop", 567 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Lost Penguin cheating at Garden Maze", 421 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - How did you climb that tree, Lost Penguin?", 422 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Library roof Lost Penguin", 594 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Library Morii of the East!", 1948 + npc_index_offset), #(440, 171, -296) Z14_Library Scholar

        #Crystals
        LocationData(CAPITAL_SEQUOIA_AP_REGION, BEATSMITH_JOB_CRYSTAL_LOCATION, 1087 + crystal_index_offset, lambda state: logic.has_vertical_movement(state)),

        #Jojo Sewers
        #Treasure chests
        #Sewer Main (lol)
        LocationData(JOJO_SEWERS_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Chest - Hiding in the guarded grass", 743 + treasure_index_offset), #Tonic Pouch chest
        LocationData(JOJO_SEWERS_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Chest - Eastside sewer green room", 2658 + treasure_index_offset), #Iron Helm chest
        LocationData(JOJO_SEWERS_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Chest - Invisible maze", 744 + treasure_index_offset), #Iron Armor chest
        LocationData(JOJO_SEWERS_AP_REGION, "Underpass Chest - Walking the plank above Pale Grotto waterfall", 3670 + treasure_index_offset, lambda state: logic.has_swimming(state)), #(337, 155, -319) Underpass Scrap chest
        #Past Secret Password
        LocationData(SEWERS_TO_BOOMER_SOCIETY_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Chest - Drowned passage to Boomer Society", 634 + treasure_index_offset),  # Money chest
        LocationData(SEWERS_TO_BOOMER_SOCIETY_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Chest - In the shadow of the waterfall", 1126 + treasure_index_offset),  # Tincture Pouch
        LocationData(SEWERS_TO_BOOMER_SOCIETY_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Chest - Leap of faith", 887 + treasure_index_offset),  # Smelly Gi chest

        #NPCs
        #Sewer Main (lol)
        LocationData(JOJO_SEWERS_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " NPC - Who even wants Stone of Jordan these days?", 2759 + npc_index_offset, lambda state: state.has(CRAG_DEMON_HORN, player)),

        #Boomer Society
        #Treasure chests
        LocationData(BOOMER_SOCIETY_AP_REGION, BOOMER_SOCIETY_DISPLAY_NAME + " Chest - Log cabin", 2667 + treasure_index_offset), #Gospel chest
        LocationData(BOOMER_SOCIETY_AP_REGION, BOOMER_SOCIETY_DISPLAY_NAME + " Chest - 2nd floor of log cabin", 2909 + treasure_index_offset), #Boomer Society map chest

        #NPCs
        LocationData(BOOMER_SOCIETY_AP_REGION, BOOMER_SOCIETY_DISPLAY_NAME + " NPC - Nice Allowance Lady", 476 + npc_index_offset),
        LocationData(BOOMER_SOCIETY_AP_REGION, BOOMER_SOCIETY_DISPLAY_NAME + " NPC - Treasury Grandpa", 547 + npc_index_offset),

        #Rolling Quintar Fields
        #Treasure chests
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - South of east gate", 826 + treasure_index_offset), #Potion chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - Chevy divot south of east gate", 828 + treasure_index_offset), #Fenix Juice chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - Deep in Quintar cave", 817 + treasure_index_offset), #Hunting Axe chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - Sneaky chest behind tree", 829 + treasure_index_offset), #Potion chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - Deep in eastern Quintar cave", 745 + treasure_index_offset), #Hunting Bow chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - At the end of the road", 825 + treasure_index_offset), #Money chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - Hidden beneath end of the road", 2674 + treasure_index_offset), #Tonic Pouch chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - West of and above sneaky chest", 338 + treasure_index_offset, lambda state: logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME) or logic.has_horizontal_movement(state)), #Money chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - Pinnacle by short and tall box friends", 471 + treasure_index_offset, lambda state: logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME) or logic.has_horizontal_movement(state)), #Tincture Pouch chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Chest - Treetop west of Quintar Sanctum", 365 + treasure_index_offset, lambda state: logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME) or logic.has_horizontal_movement(state)), #Spore Blocker chest
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, "Overpass Chest - Climb the mountain west of Quintar Sanctum entrance", 3532 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state)), #1st Overpass Scrap chest on main Overpass map

        #NPCs
        #Todo NPCs CheckOrNot: two Quintar Eggs
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " NPC - Quintar Stable Owner by Capital Sequoias eastern gate", 375 + npc_index_offset, lambda state: logic.has_jobs(state, 7)), #Quintar Pass, Fixed Missable
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " NPC - Silver beneath overhang in eastern Quintar cave crevasse", 2678 + npc_index_offset), #Dust
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " NPC - Quintar Enthusiast (always pet Buttermint)", 464 + npc_index_offset), #Fixed Missable
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " NPC - Silver in Quintar cave beneath the end of the road", 454 + npc_index_offset), #Ingot
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " NPC - Silver behind Quintar Nest befriending a stack of boxes", 323 + npc_index_offset, lambda state: logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME) or logic.has_horizontal_movement(state)), #Ore

        #Quintar Nest
        #Treasure chests
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - West Donut Lake sprinkle", 883 + treasure_index_offset), #Money chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - East Donut Lake sprinkle", 884 + treasure_index_offset), #Ether chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - Jumping puzzle above the donut", 756 + treasure_index_offset), #Fenix Juice chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - Northwest Donut Lake sprinkle", 432 + treasure_index_offset), #Potion chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - Welcome", 3078 + treasure_index_offset), #Potion chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - Mighty jump along east side wall", 746 + treasure_index_offset), #Scope Bit chest
        #You can't detour through the sewers if you can't reach the sewers (relevant for regionsanity)
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - Detour through the sewers", 638 + treasure_index_offset, lambda state: state.can_reach(JOJO_SEWERS_AP_REGION, player=player) or logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME) or logic.has_vertical_movement(state)), #Static Rod chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - North Donut Lake sprinkle", 852 + treasure_index_offset), #Tincture chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - Hop along west side wall", 2982 + treasure_index_offset), #Tincture Pouch chest
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Chest - Donut Lake crown sprinkle", 851 + treasure_index_offset), #Tonic chest
        LocationData(QUINTAR_NEST_AP_REGION, "Underpass Chest - Up north Quintar Nest waterfall", 3620 + treasure_index_offset, lambda state: logic.has_swimming(state)), #(524, 146, -368) Underpass Scrap chest

        #NPCs
        #Todo NPCs CheckOrNot: two Quintar Eggs here
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " NPC - Eastside Silver come on down to the water", 711 + npc_index_offset), #Dust
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " NPC - South of sewers Silver", 850 + npc_index_offset), #Ingot
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " NPC - Silver on the way out", 755 + npc_index_offset), #Ore

        #Crystals
        LocationData(QUINTAR_NEST_AP_REGION, HUNTER_JOB_CRYSTAL_LOCATION, 621 + crystal_index_offset),

        #Quintar Sanctum
        #Treasure chests
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " Chest - West wall big bounce", 810 + treasure_index_offset), #Money chest
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " Chest - Bounce field", 969 + treasure_index_offset), #Fenix Juice chest
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " Chest - In front of the shrine", 2910 + treasure_index_offset), #Quintar Sanctum map chest
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " Chest - West at ground level", 2983 + treasure_index_offset), #Tincture Pouch chest
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " Chest - North at ground level", 593 + treasure_index_offset), #Tonic Pouch chest
        LocationData(QUINTAR_SANCTUM_AP_REGION, "Overpass Chest - Lonely chest above Quintar Sanctum", 3533 + treasure_index_offset), #2nd Overpass Scrap chest on main map

        #NPCs
        #Todo NPCs CheckOrNot: Quintar Egg here (on Quintar Sanctum Mushroom map)
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - Silver going back down", 802 + npc_index_offset), #Dust
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - Silver almost to the top", 965 + npc_index_offset), #Dust
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - Mushroom bounce Silver", 411 + npc_index_offset), #Ingot
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - Silver beneath the shroom", 801 + npc_index_offset), #Ingot
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - East side Silver (Do not look down)", 737 + npc_index_offset), #Ore
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - Big bounce Silver", 754 + npc_index_offset), #Ore
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - Two Toads bestow Princess Toadstool", 963 + npc_index_offset),
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " NPC - Two Toads crown Bowsette", 964 + npc_index_offset),

        #Crystals
        LocationData(QUINTAR_SANCTUM_AP_REGION, CHEMIST_JOB_CRYSTAL_LOCATION, 970 + crystal_index_offset),

        #Capital Jail
        #Treasure chests
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Touchdown", 640 + treasure_index_offset),  # South Wing Key chest
        #South Wing
        LocationData(JAIL_SOUTH_WING_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - South Wing jail cell across from busted wall", 930 + treasure_index_offset),  # West Wing Key chest
        LocationData(JAIL_SOUTH_WING_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Haunted jail cell in South Wing dead end", 931 + treasure_index_offset),  # East Wing Key chest
        #South Wing Rubble
        LocationData(JAIL_SOUTH_WING_RUBBLE_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Fiercely guarded and locked in South Wing rubble 1", 990 + treasure_index_offset),  # Cell Key chest
        LocationData(JAIL_SOUTH_WING_RUBBLE_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Fiercely guarded and locked in South Wing rubble 2", 2668 + treasure_index_offset),  # Iron Rod chest
        LocationData(JAIL_SOUTH_WING_RUBBLE_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Locked in South Wing rubble", 991 + treasure_index_offset),  # Battleplate chest
        LocationData(JAIL_SOUTH_WING_RUBBLE_AP_REGION, "Underpass Chest - Drop down behind Capital Jail South Wing rubble", 3675 + treasure_index_offset),  # 7th Underpass Scrap on main map
        #West Wing
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - West Wing jail cell among the glowy plants", 925 + treasure_index_offset, lambda state: logic.has_key(state, WEST_WING_KEY)), #Cell Key chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - West Wing arrow plants", 923 + treasure_index_offset, lambda state: logic.has_key(state, WEST_WING_KEY)), #Battle Helm chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Locked among the foliage in West Wing", 916 + treasure_index_offset, lambda state: logic.has_key(state, WEST_WING_KEY) and logic.has_key(state, CELL_KEY, 4)), #Cell Key chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Locked beyond overgrown West Wing hallway", 909 + treasure_index_offset, lambda state: logic.has_key(state, WEST_WING_KEY) and logic.has_key(state, CELL_KEY, 6)),  # Dark Wing Key chest
        #East Wing
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - East Wing bedroom closet twinsies the 1st", 2999 + treasure_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY)), #empty chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - East Wing bedroom closet twinsies the 2nd", 906 + treasure_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY)), #Potion chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Waterlogged East Wing hallway twinsies the 1st", 676 + treasure_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY)), #Cell Key top chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Waterlogged East Wing hallway twinsies the 2nd", 707 + treasure_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY)), #Cell Key bottom chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Locked in broken East Wing jail cell", 708 + treasure_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY) and logic.has_key(state, CELL_KEY, 6)), #Cell Key chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Locked in East Wing bedroom", 763 + treasure_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY) and logic.has_key(state, CELL_KEY, 6)), #Cell Key chest
        #Dark Wing
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Dark Wing entry left cell", 2911 + treasure_index_offset, lambda state: logic.has_key(state, DARK_WING_KEY)), #Capital Jail map chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Sneaky chest in Dark Wing", 929 + treasure_index_offset, lambda state: logic.has_key(state, DARK_WING_KEY)), #Woven Hood chest
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Chest - Corner lava jump in Dark Wing", 920 + treasure_index_offset, lambda state: logic.has_key(state, DARK_WING_KEY)), #Woven Shirt chest

        #NPCs
        #South Wing
        LocationData(JAIL_SOUTH_WING_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " NPC - Silver in haunted South Wing jail cell", 972 + npc_index_offset), #Ingot
        LocationData(JAIL_SOUTH_WING_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " NPC - Silver in zombified South Wing jail cell", 989 + npc_index_offset), #Ingot
        #West Wing
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " NPC - Silver locked in overgrown West Wing hallway", 759 + npc_index_offset, lambda state: logic.has_key(state, WEST_WING_KEY) and logic.has_key(state, CELL_KEY, 6)),  # Ore
        #East Wing
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " NPC - Silver locked in broken East Wing jail cell accompanied by blue flower", 760 + npc_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY) and logic.has_key(state, CELL_KEY, 6)), #Ore
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " NPC - Silver locked in East Wing bedroom", 782 + npc_index_offset, lambda state: logic.has_key(state, EAST_WING_KEY) and logic.has_key(state, CELL_KEY, 6)), #Dust
        #Dark Wing
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " NPC - Silver in Dark Wing entry right cell", 472 + npc_index_offset, lambda state: logic.has_key(state, DARK_WING_KEY)), #Dust

        #Crystals
        LocationData(CAPITAL_JAIL_AP_REGION, REAPER_JOB_CRYSTAL_LOCATION, 908 + crystal_index_offset, lambda state: logic.has_key(state, DARK_WING_KEY)),

        #Capital Pipeline
        #Treasure chests
        #Pipeline South
        LocationData(PIPELINE_SOUTH_AP_REGION, CAPITAL_PIPELINE_DISPLAY_NAME + " Chest - I wanna go home", 2912 + treasure_index_offset), #Capital Pipeline map chest
        #Pipeline North
        LocationData(PIPELINE_NORTH_AP_REGION, CAPITAL_PIPELINE_DISPLAY_NAME + " Chest - Do not anger the fungus", 1294 + treasure_index_offset), #Lucky Platter chest

        #NPCs
        #Pipeline North
        LocationData(PIPELINE_NORTH_AP_REGION, CAPITAL_PIPELINE_DISPLAY_NAME + " NPC - Silver in corrupted tunnel 1", 2660 + npc_index_offset), #Ingot
        LocationData(PIPELINE_NORTH_AP_REGION, CAPITAL_PIPELINE_DISPLAY_NAME + " NPC - Silver in corrupted tunnel 2", 1295 + npc_index_offset), #Ore
        # Pipeline Jidamba Connector
        LocationData(PIPELINE_JIDAMBA_CONNECTOR_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " NPC - Diamond down Pipeline elevator into Jidamba", 2897 + npc_index_offset),  # Dust

        #Cobblestone Crag
        #Treasure chests
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Chest - Behind sluice gate", 479 + treasure_index_offset), #Ether Pouch chest
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Chest - Long jump", 382 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state)), #Potion chest
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Chest - Tucked in cranny between two tall spikes", 1119 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state)), #Potion Pouch chest
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Chest - I totally meant to miss that jump", 2670 + treasure_index_offset), #Skewer chest
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Chest - Upon exiting from Quintar Nest", 478 + treasure_index_offset), #Tonic Pouch chest
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Chest - Could really use a Walking Stick (chest) right about now...", 2669 + treasure_index_offset),
        LocationData(COBBLESTONE_CRAG_AP_REGION, "Underpass Chest - On the way to village hidden among leaves", 3669 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state)), #Underpass Scrap (Okimoto)

        #NPCs
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " NPC - Westernmost Silver", 1120 + npc_index_offset), #Dust

        #Okimoto N.S.
        #Treasure chests
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Moth love lamp", 364 + treasure_index_offset), #Butterfly chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Dont bump your head", 2661 + treasure_index_offset), #Ether Pouch chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Parkour to the west", 337 + treasure_index_offset), #Float Shoes chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Just kinda in there, its not special", 356 + treasure_index_offset), #Potion chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - East of save point", 344 + treasure_index_offset), #Tanto chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - On yashiki balcony", 690 + treasure_index_offset), #Money chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Down hidden stairs in library", 686 + treasure_index_offset), #Art of War chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - East ground floor room", 2673 + treasure_index_offset), #Magic Finder chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Lurking behind bookcase", 434 + treasure_index_offset), #Potion Pouch chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Past hidden staircase", 694 + treasure_index_offset), #Tachi chest
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Chest - Dance above the koi pond", 1103 + treasure_index_offset), #Training Gi chest
        LocationData(OKIMOTO_NS_AP_REGION, "Overpass Chest - Mountain lake north of the yashiki", 3534 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or logic.has_swimming(state)), #(605, 228, -270) 3rd Overpass Scrap in Overpass main map

        #NPCs
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " NPC - Silver on the way up", 359 + npc_index_offset), #Dust
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " NPC - Why does a room like this exist? (Silver)", 692 + npc_index_offset), #Silver Dust
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " NPC - Eastern Silver atop pond box", 689 + npc_index_offset), #Ingot
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " NPC - Silver behind room that shall not be named", 691 + npc_index_offset), #Ingot
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " NPC - Silver atop yashiki", 2659 + npc_index_offset), #Ore
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " NPC - Lets get down to business western Silver", 429 + npc_index_offset), #Ore
        LocationData(OKIMOTO_NS_AP_REGION, "Overpass NPC - Swim up koi pond waterfall into cherry tree", 1583 + npc_index_offset, lambda state: logic.has_swimming(state)), #Springs Oath (632, 243, -261) Overpass main map

        #Crystals
        LocationData(OKIMOTO_NS_AP_REGION, NINJA_JOB_CRYSTAL_LOCATION, 699 + crystal_index_offset),

        #Greenshire Reprise
        #Treasure chests
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " Chest - Jump off bridge 4", 483 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)), #Ambush Knife chest
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " Chest - Atop the waterfalls", 490 + treasure_index_offset), #Ether chest
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " Chest - Jump off bridge 3", 482 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)), #Looters Ring chest
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " Chest - Tall taunter", 373 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)), #Shell Amulet chest
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " Chest - In the valley of trees", 487 + treasure_index_offset), #Tincture Pouch chest
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " Chest - Tip of peninsula south of 2nd bridge", 491 + treasure_index_offset), #Tonic Pouch chest

        #NPCs
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " NPC - Jump down from 2nd bridge to Silver fallen in north crack", 485 + npc_index_offset), #Ore
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " NPC - Silver across 1st bridge hiding in a crack", 486 + npc_index_offset), #Dust
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " NPC - The furthest southern edge Silver", 474 + npc_index_offset), #Ingot

        #Salmon Pass
        #Treasure chests
        #Salmon Pass East: 2 chests on the east side that either require the ability to get to Greenshire Reprise and cross it or hop the bridge (also you need the 5 jobs bc the rental quintar comes from Capital Sequoia)
        LocationData(SALMON_PASS_EAST_AP_REGION, SALMON_PASS_DISPLAY_NAME + " Chest - Riverbank among yellow flowers", 2700 + treasure_index_offset), #Paypirbak chest
        LocationData(SALMON_PASS_EAST_AP_REGION, SALMON_PASS_DISPLAY_NAME + " Chest - Admiring the hidden waterfall", 419 + treasure_index_offset), #Fenix Juice chest
        #Salmon Pass West: 1 chest on the west side that either requires crossing the bridge or hoofing it from Salmon River
        LocationData(SALMON_PASS_WEST_AP_REGION, SALMON_PASS_DISPLAY_NAME + " Chest - Across a bridge and around through a tunnel", 2420 + treasure_index_offset),  # Fenix Juice chest

        #Salmon River
        #Treasure chests
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " Chest - Hop on chest once you have become frogger", 1264 + treasure_index_offset), #Money chest
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " Chest - Atop river island crown", 1297 + treasure_index_offset), #Bloodbind chest
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " Chest - It also wishes to be frogger", 325 + treasure_index_offset), #Money chest
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " Chest - In the stands of Salmon race finish line", 2976 + treasure_index_offset, lambda state: logic.has_rental_salmon(state)), #Ether Pouch chest
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " Chest - Inside Salmon Shack", 2913 + treasure_index_offset), #Salmon River map chest
        #Mushroom Mountain
        LocationData(MUSHROOM_MOUNTAIN_AP_REGION, "Overpass Chest - Hop west from shrine to shroom-studded mountainside", 3539 + treasure_index_offset), #(32, 181, -373) 2nd Overpass scrap on (Cloudy Wind)
        LocationData(MUSHROOM_MOUNTAIN_AP_REGION, "Overpass Chest - Frigid dip high behind River Cat", 3654 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or logic.has_swimming(state)), #(60, 225, -435) Overpass (Snow) River Cats Ego map
        LocationData(MUSHROOM_MOUNTAIN_AP_REGION, "Overpass Chest - Chilling by Nomad's Outpost", 3676 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or logic.has_swimming(state)),  # (45, 215, -465) Overpass (Outpost) Scrap
        LocationData(MUSHROOM_MOUNTAIN_AP_REGION, "Overpass Chest - Ultimate Mulan challenge past mushroom mountain", 1401 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)) or logic.has_glide(state)), #(-35, 166, -387) Overpass (Cloudy Wind) Zether Pouch chest

        #NPCs
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Reid chilling by the Fish Hatchery", 2410 + npc_index_offset), #(113, 172, -372) Courtyard Key; Fixed Missable
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race Participation Prize", 50639 + npc_index_offset, lambda state: logic.has_rental_salmon(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 14th place price", 50640 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 12th place price", 50641 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 10th place price", 50642 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 8th place price", 50643 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 6th place price", 50644 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 4th place price", 50645 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 3rd place price", 50646 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Salmon Race 2nd place price", 50647 + npc_index_offset, lambda state: logic.has_swimming(state)),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " NPC - Win the Salmon Race", 639 + npc_index_offset, lambda state: logic.has_swimming(state)),
        #Mushroom Mountain
        LocationData(MUSHROOM_MOUNTAIN_AP_REGION, "Overpass NPC - Fall off mushroom mountain onto Gold", 2739 + npc_index_offset), #(63, 191, -399) 2nd Gold Dust on Overpass (Cloudy Wind)

        #Crystals
        #River Cat's Ego
        LocationData(RIVER_CATS_EGO_AP_REGION, NOMAD_JOB_CRYSTAL_LOCATION, 630 + crystal_index_offset), #River Cats Ego

        #Poko Poko Desert
        #Treasure chests
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - Quintar leapfrog", 1080 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state)), #Butter Cutter chest
        # if you're Good At Jumping you can get to this chest south of rocky outcropping gold with no mounts
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - South of tricky Quintar Gold", 1082 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state)), #Hatchet chest
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - North Lookout Tower", 1190 + treasure_index_offset, lambda state: logic.has_rental_quintar(state, SARA_SARA_BAZAAR_DISPLAY_NAME) or logic.has_vertical_movement(state)), #North Lookout Token chest
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - This chests (on) a butte", 1169 + treasure_index_offset, lambda state: logic.has_rental_quintar(state, SARA_SARA_BAZAAR_DISPLAY_NAME)), #Dueller
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - Stormy first floor of ruins", 2676 + treasure_index_offset), #Fenix Juice chest
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - West Lookout Tower", 1170 + treasure_index_offset), #West Lookout Token chest
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - Potion chest to fortify you for jumping puzzle from hell", 2708 + treasure_index_offset),
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - Central Lookout Tower (ok maybe that jumping puzzle wasn't that bad)", 1189 + treasure_index_offset), #Central Lookout Token chest
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - Balance beam", 97 + treasure_index_offset), #Scope Specs chest
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - Past Lost Son", 1667 + treasure_index_offset), #Ether Pouch chest
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Chest - Cooling off in the tent before the Tower of Zot", 2914 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state) and logic.has_vertical_movement(state)), #Salmon Bay map chest

        #NPCs
        #Todo NPCs CheckOrNot: three Quintar Eggs in Poko Poko Desert (Nest) map
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Silver beneath overhang in ruins south of shrine", 2675 + npc_index_offset), #Dust
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Silver slumbering in broken house NE of shrine", 1081 + npc_index_offset), #Ingot
        # if you're Good At Jumping you can get to this rocky outcropping gold with no mounts
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Rocky outcropping Gold will put your Quintar to the test", 2817 + npc_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state)), #Dust
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Silver in desert arch shade", 2682 + npc_index_offset), #Ingot
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Thirsty Lad", 1201 + npc_index_offset, lambda state: state.has(SPECIAL_MILK, player)),
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Stormy Silver atop ruins", 2677 + npc_index_offset), #Ore
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Stormy Silver on ruined building floor", 2681 + npc_index_offset), #Ore
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Gold Ingot atop ridge south of North Lookout Tower", 2818 + npc_index_offset),
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Silver in the sandstorm on ruins 2nd floor", 2680 + npc_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state)), #Dust
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Gold overlooking Sara Sara Bazaar", 2707 + npc_index_offset, lambda state: logic.has_vertical_movement(state)), #Ingot
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Gold accessible from beach reacharound", 2711 + npc_index_offset, lambda state: logic.has_horizontal_movement(state) and logic.has_vertical_movement(state)), #Dust
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Diamond on Tower of Zots outside", 2879 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)), #Dust
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Gold on far end of the Tower of Zot", 2816 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)), #Ore
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " NPC - Gold on an outcropping by long loop-around chest", 2706 + npc_index_offset), #Ore

        #Sara Sara Bazaar
        #Treasure chests
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Chest - Someone took the St James and left a...", 408 + treasure_index_offset, lambda state: logic.has_key(state, ROOM_ONE_KEY)), #Knockout Stick chest
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Chest - Darkened upper storeroom", 414 + treasure_index_offset, lambda state: logic.has_rental_quintar(state, SARA_SARA_BAZAAR_DISPLAY_NAME) or logic.has_horizontal_movement(state)), #Potion chest
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Chest - Wedge yourself through the crates in the darkened upper storeroom", 513 + treasure_index_offset, lambda state: logic.has_rental_quintar(state, SARA_SARA_BAZAAR_DISPLAY_NAME) or logic.has_horizontal_movement(state)), #Storm Rod chest
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Chest - Potion Mixer", 1194 + treasure_index_offset), #Beaurior Volcano map chest
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Chest - Spilled booty", 2936 + treasure_index_offset, lambda state: logic.has_swimming(state)), #Captains Hat chest

        #NPCs
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Quintar West Stable Owner", 1852 + npc_index_offset, lambda state: logic.has_jobs(state, 7)), #Quintar Pass; Fixed Missable
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Quintar East Stable Owner", 2234 + npc_index_offset, lambda state: logic.has_jobs(state, 7)), #Quintar Pass; Fixed Missable
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Ferry Ticket Agent grants Ferry Pass in case you hate children", 940 + npc_index_offset, lambda state: logic.has_jobs(state, 11)), #(-166,93,56) Fixed Missable
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Three tokens makes a Pyramid Key something something triangles", 949 + npc_index_offset, lambda state: state.has(WEST_LOOKOUT_TOKEN, player) and state.has(CENTRAL_LOOKOUT_TOKEN, player) and state.has(NORTH_LOOKOUT_TOKEN, player)),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - The One and Only Room 1 Key", 385 + npc_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Circle the eastern desert wall for Worried Moms Lost Son", 1196 + npc_index_offset), #Ferry Pass
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Pelt this Fish Merchant with Rotten Salmon", 942 + npc_index_offset, lambda state: state.has(SPECIAL_ROTTEN_SALMON, player) and state.has(SPECIAL_FRESH_SALMON, player)),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - No Shoudu Stew for you!", 1200 + npc_index_offset, lambda state: state.has(SPECIAL_SHOUDU_STEW, player)),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Spilled booty Silver", 2905 + npc_index_offset, lambda state: logic.has_swimming(state)), #Dust
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Spilled booty Silverer", 2906 + npc_index_offset, lambda state: logic.has_swimming(state)), #Dust
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Spilled booty Silvererer", 2903 + npc_index_offset, lambda state: logic.has_swimming(state)), #Ingot
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Spilled booty Silverererer", 2904 + npc_index_offset, lambda state: logic.has_swimming(state)), #Ingot
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Spilled booty Silvererererer", 2901 + npc_index_offset, lambda state: logic.has_swimming(state)), #Ore
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " NPC - Spilled booty Silverererererer", 2902 + npc_index_offset, lambda state: logic.has_swimming(state)), #Ore

        #Sara Sara Beach East
        # Treasure chests
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " Chest - Glittering in the sun at Ibek Cave exit 1", 1083 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)),  # Tincture Pouch chest
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " Chest - Glittering in the sun at Ibek Cave exit 2", 1085 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)),  # Tonic Pouch chest
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " Chest - How dare you stand where he stood?", 1084 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)),  # Money chest

        # NPCs
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver glittering in the sun at Ibek Cave exit 1", 2683 + npc_index_offset, lambda state: logic.has_vertical_movement(state)),  # Dust
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver glittering in the sun at Ibek Cave exit 2", 2684 + npc_index_offset, lambda state: logic.has_vertical_movement(state)),  # Dust
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver glittering in the sun at Ibek Cave exit 3", 2686 + npc_index_offset),  # Dust
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver glittering in the sun at Ibek Cave exit 4", 2688 + npc_index_offset, lambda state: logic.has_vertical_movement(state)),  # Silver
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver glittering in the sun at Ibek Cave exit 5", 2689 + npc_index_offset),  # Ore
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver glittering in the sun at Ibek Cave exit 6", 2690 + npc_index_offset),  # Ore
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Jaunt along cliff past Dr Cool Aids perch to Silver", 2685 + npc_index_offset, lambda state: logic.has_vertical_movement(state)),  # Ingot
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver on the beach rocks at eastern edge", 2687 + npc_index_offset),  # Ingot
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " NPC - Silver beheld by Dr Cool Aids", 2691 + npc_index_offset, lambda state: logic.has_vertical_movement(state)),  # Ore

        #Sara Sara Beach West
        #Treasure chests
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " Chest - South of Beach Birds Nest", 154 + treasure_index_offset), #Ether chest
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " Chest - Across the palms above the dust", 1509 + treasure_index_offset), #Potion chest
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " Chest - Beach cave", 2718 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)) or logic.has_swimming(state)), #Blank Pages chest
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " Chest - Tightrope walk below Beach Birds Nest", 1546 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_horizontal_movement(state)), #Potion chest; possible with rental if masochists play our game/Good At Jumping option

        #NPCs
        #Todo NPCs Job Masters: Master Dervish ID 3575 (-255, 103, -237); gives you Dervish Seal in exchange for job mastery
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Cross my palms with Silver", 2693 + npc_index_offset), #Dust
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Silver past angry birds", 2697 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)) or logic.has_glide(state)), #Dust
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Silver south of Beach Birds Nest", 2694 + npc_index_offset), #Ingot
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Silver at the foot of the Tower of Zot", 2699 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)) or logic.has_swimming(state)), #Ingot
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Lonely Islet Silver", 2878 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)) or logic.has_swimming(state)), #Ingot
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Southern silver along the cliffside", 2692 + npc_index_offset), #Ore
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Silver chilling in beach cave", 2698 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)) or logic.has_swimming(state)), #Ore
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " NPC - Silver further along beach", 2877 + npc_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Ore

        #Ancient Reservoir
        #Treasure chests
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Really elaborate crystal rafters", 1123 + treasure_index_offset), #Red Coat chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Crystal gutters", 1122 + treasure_index_offset), #Red Cap chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Tucked on ledge by aqueduct", 1982 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_swimming(state)), #Resist Shifter chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - East Switch Room", 2977 + treasure_index_offset), #Ether Pouch chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Eastern nyoom room", 2056 + treasure_index_offset), #Money chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Hiding behind aqueduct grate", 2703 + treasure_index_offset), #Potion Pouch chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Hiding behind western aqueduct grate", 2702 + treasure_index_offset), #Money chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Twinsies the 1st at west waterfall base", 2704 + treasure_index_offset), #Defense Shifter chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Twinsies the 2nd at west waterfall base", 1145 + treasure_index_offset), #Money chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - I saw Red vent in the eastern stairwell", 2701 + treasure_index_offset), #Grim Scythe chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Goat snack for later", 2915 + treasure_index_offset), #Ancient Reservoir map chest
        LocationData(ANCIENT_RESERVOIR_AP_REGION, "Underpass Chest - Waterway nook between Gran & Ancient Reservoir", 3541 + treasure_index_offset, lambda state: logic.has_swimming(state)), #(64, 98, -111) 1st Underpass Scrap on main map

        #NPCs
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " NPC - Silver in odd flooded room 1", 2695 + npc_index_offset), #Ingot
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " NPC - Silver in odd flooded room 2", 1675 + npc_index_offset), #Ore

        #Crystals
        LocationData(ANCIENT_RESERVOIR_AP_REGION, DERVISH_JOB_CRYSTAL_LOCATION, 1121 + crystal_index_offset),

        #Ibek Cave
        #Treasure chests
        LocationData(IBEK_CAVE_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Chest - Celebrate your new hops", 2517 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)),  # Fenix Juice Pouch chest

        #NPCs
        LocationData(IBEK_CAVE_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " NPC - Goat victory Ibek Bell", 1676 + npc_index_offset),  # Z30_PostBossEvent;
        LocationData(IBEK_CAVE_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " NPC - Silver in the goat digs", 2696 + npc_index_offset, lambda state: logic.has_vertical_movement(state)),  # Dust

        #Salmon Bay
        #Treasure chests
        LocationData(SALMON_BAY_AP_REGION, SALMON_BAY_DISPLAY_NAME + " Chest - Cliff diving", 2975 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)), #Ether Pouch chest
        LocationData(SALMON_BAY_AP_REGION, SALMON_BAY_DISPLAY_NAME + " Chest - Across the bridge", 2974 + treasure_index_offset), #Potion Pouch chest
        LocationData(SALMON_BAY_AP_REGION, "Overpass Chest - Lonely scrap among half-dead pines above Salmon Bay", 3677 + treasure_index_offset), #8th Scrap in Overpass main map
        
        #NPCs
        LocationData(SALMON_BAY_AP_REGION, SALMON_BAY_DISPLAY_NAME + " NPC - Ancient Tablet B on moodlit shore behind waterfall", 2438 + npc_index_offset),
        LocationData(SALMON_BAY_AP_REGION, SALMON_BAY_DISPLAY_NAME + " NPC - West cliff diving Ancient Tablet C", 1271 + npc_index_offset, lambda state: logic.has_vertical_movement(state)),
        LocationData(SALMON_BAY_AP_REGION, SALMON_BAY_DISPLAY_NAME + " NPC - Quintar splish splash Ancient Tablet A", 1272 + npc_index_offset),

        #Overpass
        #Treasure chests
        #Life Jewel on main map has been categorized under Dione Shrine
        #1st Scrap on main Overpass map has been categorized under Rolling Quintar Fields
        #2nd Scrap on main Overpass map has been categorized under the Quintar Sanctum
        #3rd Scrap on main Overpass map has been categorized under the Okimoto N.S.
        #4th Scrap on main Overpass map has been categorized under Dione Shrine
        #5th Scrap on main Overpass map has been categorized under Quintar Reserve
        #6th Scrap on main Overpass map has been categorized under Yamagawa M.A.
        #7th Scrap on main Overpass map has been categorized under Beaurior Rock
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

        #Zones (Expert)
        #The Open Sea
        #Treasure chests
        #Atolls
        LocationData(JIDAMBA_ATOLLS_AP_REGION, THE_OPEN_SEA_DISPLAY_NAME + " Chest - Atoll southeast of Jidamba Tangle", 3767 + treasure_index_offset),  # Fenix Syrup chest
        LocationData(JIDAMBA_ATOLLS_AP_REGION, THE_OPEN_SEA_DISPLAY_NAME + " Chest - Atoll southwest of southeast Jidamba Tangle atoll", 3765 + treasure_index_offset),  # Z-Potion chest
        #NPCs
        LocationData(THE_OPEN_SEA_AP_REGION, THE_OPEN_SEA_DISPLAY_NAME + " NPC - I'm on a raft!", 2804 + npc_index_offset, lambda state: state.has("Item - Super Rod", player) and state.has("Item - Jigging Lure", player)),
        #CheckOrNot: (930, 91, 253) do we put a check on the guy who gives you a Gaea Shard if you get there with no Salmon lol: no
        #LocationData(THE_OPEN_SEA_AP_REGION, THE_OPEN_SEA_DISPLAY_NAME + " NPC - Z34_SinisterSailor", 2520 + npc_index_offset),

        #Shoudu Waterfront
        #Treasure chests
        LocationData(SHOUDU_WATERFRONT_AP_REGION, SHOUDU_WATERFRONT_DISPLAY_NAME + " Chest - Along the water", 2419 + treasure_index_offset), #Money chest
        LocationData(SHOUDU_WATERFRONT_AP_REGION, SHOUDU_WATERFRONT_DISPLAY_NAME + " Chest - Hop around 1", 3690 + treasure_index_offset), #Empty chest
        LocationData(SHOUDU_WATERFRONT_AP_REGION, SHOUDU_WATERFRONT_DISPLAY_NAME + " Chest - Hop around 2", 1114 + treasure_index_offset), #Mars Stone chest

        #Shoudu Province
        #Treasure chests
        #Port area
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Jump through a window", 1507 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),  # Ether Pouch chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Lurking above spike ball pit by goldsmith", 2984 + treasure_index_offset),  # (753, 105, -176) Tincture Pouch chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Weaponsmith", 1505 + treasure_index_offset),  # Plague Mask chest

        #Shanty Inn Home Point area
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Outside the inn", 2985 + treasure_index_offset),  # Potion chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Sneaky back door of cramped storage room", 1519 + treasure_index_offset),  # Looters Pin chest

        #Moving up past here requires Ibek/Owl
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Below fast boi spark", 3504 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Through rooftop window south of fast boi spark 1", 3506 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Through rooftop window south of fast boi spark 2", 2763 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Reservoir above the water", 3508 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_swimming(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Above accessory store", 3509 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Building near all the grates", 3510 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Above Samurai Lounge 1", 3511 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Above Samurai Lounge 2", 1541 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Fleuret chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Samurai Lounge", 3512 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Assassin Lounge", 3513 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Among crates across from Assassin Lounge", 3514 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Its in a room and there is a bed", 3515 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Granary", 3520 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Below the flower house", 3521 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - White hut", 3522 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Across the reservoir", 2978 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) and logic.has_swimming(state)) or logic.has_glide(state)), #Ether Pouch chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Crawl along the attic", 1536 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Knicked Knackers chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Sneak behind crates near Assassin Lounge", 2760 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Muggers Glove chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Go in the back door", 1506 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion Pouch
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Near the Assassin Lounge", 2762 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion Pouch
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Jump along the lamppost", 2752 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Suitor Hat chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Above the armor store", 1517 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion Pouch chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Enter building next to white hut to balance above The Undercity 1", 2717 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Ether chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Enter building next to white hut to balance above The Undercity 2", 2716 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Tincture Pouch chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Cross the balance beam east of Fields save point", 3040 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion Pouch chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Cross the balance beam on the way to Sky Arena", 2754 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Acrobat Shoes chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Atop the roofs near the grates", 1369 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - In the flower room", 2789 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Hidden in a house by the elevator 1", 3505 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Hidden in a house by the elevator 2", 2790 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Near sky fishing 1", 3507 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Elevator Part chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Near sky fishing 2", 2986 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Under the dry kid pit", 1365 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #The Immovable chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Fall through broken grate in building west of Sky Arena Prize Counter", 2951 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Potion chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 2 Sky Arena Wins Room 1", 2794 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 32)),  # Money chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 2 Sky Arena Wins Room 2", 2751 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 32)),  # Bone Mail chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 2 Sky Arena Wins room 3", 2747 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 32)),  # Cutlass chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 2 Sky Arena Wins room 4", 2796 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 32)), #Tonic Pouch
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 2 Sky Arena Wins room 5", 2748 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 32)), #Soul Kris chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 5 Sky Arena Wins room 1", 2812 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 44)), #Money chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 5 Sky Arena Wins room 2", 2723 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 44)), #Gaia Axe chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 5 Sky Arena Wins room 3", 2813 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 44)), #Money chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 5 Sky Arena Wins room 4", 2753 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 44)), #Gaia Vest chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 8 Sky Arena Wins room 1", 2665 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 54)), #Gravedigger chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 8 Sky Arena Wins room 2", 2805 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 54)), #Malifice chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 8 Sky Arena Wins room 3", 2800 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 54)), #Wizards Wall chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 10 Sky Arena Wins room 1", 2756 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(753, 134, -263) Yasha chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 10 Sky Arena Wins room 2", 2928 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(754, 134, -264) Muramasa chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - 10 Sky Arena Wins room 3", 2929 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(755, 134, -263) Shadow Gi chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Fall through floorboards of 10 Sky Arena Wins room 1", 3763 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(754, 130, -264) Zether chest
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Chest - Fall through floorboards of 10 Sky Arena Wins room 2", 3764 + treasure_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(755, 130, -263) Z-Potion chest

        #NPCs
        #Todo NPCs Job Masters: Master Assassin ID 3605 (769, 123, -201); gives you Assassin Seal in exchange for job mastery
        #Todo NPCs Job Masters: Master Samurai ID 3576 (800, 115, -221); gives you Samurai Seal in exchange for job mastery
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Chloe and Talon sky fishing", 3702 + npc_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #(765, 125, -248) Fixed Missable; removed post-sparkle
        #NPCs Multichecks: Shoudu Province (Sky Arena) map Z38_SkyArenaPrizes ID 1921 (765, 125, -248) gives 5 prizes in exchange for winning fights
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - 1 Sky Arena Win Prize", 51921 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 30)), #(765, 125, -248)
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - 4 Sky Arena Wins Prize", 51922 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 40)), #(765, 125, -248)
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - 6 Sky Arena Wins Prize", 51923 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 48)), #(765, 125, -248)
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - 7 Sky Arena Wins Prize", 51924 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 52)), #(765, 125, -248)
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - 9 Sky Arena Wins Prize", 1921 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 56)), #(765, 125, -248)
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - 10 Sky Arena Wins room Diamond 1", 2833 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(752, 133, -262) Dust
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - 10 Sky Arena Wins room Diamond 2", 2811 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(756, 133, -261) Ingot
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Diamond through a hole in the 10 Sky Arena Wins room floor", 2832 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #(753, 130, -264) Ore
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold at back reservoir wall", 2827 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.has_swimming(state)), #Ingot
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold in farmland on way to shrine", 2821 + npc_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Ingot
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold near sky fishing", 2834 + npc_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Ore
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold in 2 Sky Arena Wins room", 2829 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 32)), #Dust
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold in 5 Sky Arena Wins room 1", 2720 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 44)), #Ore
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold in 5 Sky Arena Wins room 2", 2722 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 44)), #Ingot
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold in 5 Sky Arena Wins room 3", 2721 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 44)), #Dust
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold in 8 Sky Arena Wins room 1", 2830 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 54)), #Ingot
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Gold in 8 Sky Arena Wins room 2", 2831 + npc_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 54)), #Ore

        #Crystals
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Crystal - Samurai for 3 Sky Arena wins", 1206 + crystal_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 35)),

        #The Undercity
        #Treasures
        # can get without mounts from Shoudu
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Gated-off room 1", 2988 + treasure_index_offset),  # Fenix Juice chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Gated-off room 2", 2987 + treasure_index_offset),  # Ether chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Gated-off room 3", 1147 + treasure_index_offset),  # Potion chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Gated-off room 4", 3517 + treasure_index_offset),  # (778, 94, -254) Elevator Part chest
        #except these up high
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Climb up lampposts and run across the fence", 1925 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),  # Cursegiver chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - North wall climb (or fall through broken grate by Sky Arena Prize Counter)", 3516 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),  # Elevator Part chest
        #Home Point Stone area - can walk from Ganymede Shrine -> Undercity entrance next to white hut -> fall off rafter; can also swim from the sea
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Hiding in the rafters", 2989 + treasure_index_offset, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),  # Potion Pouch chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Atop awning east of the waterfall", 3518 + treasure_index_offset, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),  # Elevator Part chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Hidden in a nook in the wall", 2793 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),  # Knights Plate chest
        #ibek from Home Point Stone area
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Up the rafters against a pillar", 2990 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)),  # Ether chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Even further up the rafters", 2991 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)),  # Ether Pouch chest
        #Undercity Inn area - can walk from Home Point Stone area if you hop up on guy who wants you to defeat the Undercity masters, go north, and hop west across lamps
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Hiding in a building in the north area", 2826 + treasure_index_offset, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),  # Potion chest
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - Undercity Inn", 3519 + treasure_index_offset, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),  # Elevator Part
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Chest - South of the Undercity Inn", 1695 + treasure_index_offset, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)),  # Brigandine chest
        #swimmy swimmy
        LocationData(THE_UNDERCITY_AP_REGION, "Underpass Chest - Lovely bounce tree W of The Undercity", 3673 + treasure_index_offset, lambda state: logic.has_swimming(state) or logic.has_glide(state)), #(608, 91, -215) (Summon Pah) Underpass Scrap chest
        
        #NPCs
        #can get without mounts from Shoudu
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " NPC - Gold hiding from the bats under the awning", 2835 + npc_index_offset), #Dust
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " NPC - Gated-off room Gold", 2825 + npc_index_offset), #Ore
        #other side of canal from Home Point Stone area
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " NPC - Gold in the sewer offshoot", 1696 + npc_index_offset, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)), #Dust
        #Undercity Inn area
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " NPC - Storage room Gold of the Undercity Inns", 1694 + npc_index_offset, lambda state: logic.has_swimming(state) or logic.has_horizontal_movement(state) or logic.has_vertical_movement(state) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player)), #Ingot

        #Crystals
        #Can just swim or defeat the Undercity Masters; Blade Master: Ibek or Owl, Shadow Master: Horizontal or Fish, Duel Master: Ibek or Owl; to defeat all masters, you either need both ibek + quintar, owl, or fish
        LocationData(THE_UNDERCITY_AP_REGION, ASSASSIN_JOB_CRYSTAL_LOCATION, 1204 + crystal_index_offset, lambda state: (logic.has_horizontal_movement(state) and logic.has_vertical_movement(state)) or logic.has_glide(state) or logic.has_swimming(state)),

        #Ganymede Shrine
        #Treasure chests
        LocationData(GANYMEDE_SHRINE_AP_REGION, GANYMEDE_SHRINE_DISPLAY_NAME + " Chest - drop down from the top", 1594 + treasure_index_offset, lambda state: state.has(GANYMEDE_STONE, player)),

        #Beaurior Volcano
        #Treasure chests
        LocationData(BEAURIOR_VOLCANO_AP_REGION, BEAURIOR_VOLCANO_DISPLAY_NAME + " Chest - Beaurior Rock entrance", 3770 + treasure_index_offset), #Fenix Syrup chest
	    LocationData(BEAURIOR_VOLCANO_AP_REGION, BEAURIOR_VOLCANO_DISPLAY_NAME + " Chest - Outcropping above the fog", 1168 + treasure_index_offset), #Temporal Blade chest
	    LocationData(BEAURIOR_VOLCANO_AP_REGION, BEAURIOR_VOLCANO_DISPLAY_NAME + " Chest - Tricky jumps past Rock entrance", 2750 + treasure_index_offset), #Tome of Light chest

        #Beaurior Rock
        #Treasure chests
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B4 big lava room with optional boss", 1796 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Ether chest
	    LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - Caged in far corner of B4 big lava room with optional boss", 481 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Guard Crown chest
	    LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - Caged through secret tunnel in B4 big lava room with optional boss", 724 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Halberd chest
	    LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - Island in B4 big lava room with optional boss", 1682 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Small Key chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - Elevator down from entrance to happy spike land", 894 + treasure_index_offset), #Small Key chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B3 balcony above the lava", 1337 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY)), #Small Key chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B2 with the Lets Make a Deal doors", 2973 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Potion Pouch chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B1 overlooking the catwalks room", 818 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Small Key chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B1 square pokeball room", 2916 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #map chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B3 behind wrought-iron fence", 899 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Shelter Dress chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B3 ominous green dumplings room", 1797 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2)), #Fenix Juice chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B2 danger hops back to purple", 2044 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4)), #Ether Pouch chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B1 cheeky lava platforming 1", 2041 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4)), #Potion
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B1 cheeky lava platforming 2", 1799 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4)), #Ether
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - B1 jump to odd ice block", 2040 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4)), #Cold Touch chest
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Chest - Top floor ominous lamps room", 1683 + treasure_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4)), #Boss Key chest
        LocationData(BEAURIOR_ROCK_AP_REGION, "Overpass Chest - West of Valkyrie Watchtower", 3540 + treasure_index_offset),  # (1, 129, 62) 7th Overpass Scrap on main map

        #NPCs
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " NPC - Gold in B4 big lava room with optional boss", 2822 + npc_index_offset, lambda state: logic.has_key(state, SMALL_KEY) and logic.has_horizontal_movement(state)), #Gold Ingot
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " NPC - B1 cheeky lava platforming Gold", 2823 + npc_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4)), #Dust
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " NPC - B1 Magic Well friendos hiding in the pillars", 2824 + npc_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_horizontal_movement(state)), #Ore
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_VOLCANO_DISPLAY_NAME + " NPC - Summit Gold", 2836 + npc_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_key(state, BEAURIOR_BOSS_KEY)), #Ore Beaurior Volcano but it's at the top so Rock it is

        #Crystals
	    LocationData(BEAURIOR_ROCK_AP_REGION, VALKYRIE_JOB_CRYSTAL_LOCATION, 1086 + crystal_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_key(state, BEAURIOR_BOSS_KEY)),

        #Lake Delende
        #Treasure chests
        LocationData(LAKE_DELENDE_AP_REGION, LAKE_DELENDE_DISPLAY_NAME + " Chest - North edge 1", 1263 + treasure_index_offset), #Float Shoes chest
        LocationData(LAKE_DELENDE_AP_REGION, LAKE_DELENDE_DISPLAY_NAME + " Chest - North edge 2", 2917 + treasure_index_offset), #Lake Delende map chest

        #NPCs
        LocationData(LAKE_DELENDE_AP_REGION, LAKE_DELENDE_DISPLAY_NAME + " NPC - Panning for Gold down Salmon Creek without a paddle", 2854 + npc_index_offset, lambda state: logic.has_vertical_movement(state)), #Dust

        #Quintar Reserve
        #Treasure chests
        LocationData(QUINTAR_RESERVE_AP_REGION, "Overpass Chest - Climbing the boughs up from the elevator", 3536 + treasure_index_offset), #5th Scrap on Overpass main map
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Chest - Race start hut", 1591 + treasure_index_offset), #Quintar Grass chest
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Chest - Hollowed-out wall of Mausoleum", 1320 + treasure_index_offset, lambda state: logic.has_glide(state)), #Undead Ring chest

        #NPCs
        #Todo NPCs CheckOrNot: 3 Quintar Eggs here
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Eastern Quintar overlooking the sea", 427 + npc_index_offset, lambda state: state.has(BABEL_QUINTAR, player)), #The Sequoia map (789, 191, -338); Fixed Missable
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding in hidden Quintar nest down in the ravine SE of Dione Shrine", 2255 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state) and logic.is_area_in_level_range(state, 54)), #Shedding 1
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding in sneaky Quintar nest in eastern wall of the canyon north of the Mausoleum", 2256 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state) and logic.is_area_in_level_range(state, 54)), #Shedding 2
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding in super sneaky Quintar nest in canyon north of the Mausoleum", 2257 + npc_index_offset, lambda state: logic.is_area_in_level_range(state, 54)), #Shedding 3
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding east of shrine", 2259 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Shedding 4
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Long jog along the east mountain to shedding", 2260 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Shedding 5
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding overlooking the east ocean", 2261 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Shedding 6
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding atop the Mausoleum", 2262 + npc_index_offset, lambda state: state.has(DIONE_STONE, player) and logic.has_glide(state)), #Shedding 7
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Treetop shedding north of Mausoleum", 2263 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Shedding 8
        #shedding 9 is in the Dione Shrine because why not I guess
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding overlooking the race start point", 2265 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Shedding 10
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding north of Mausoleum", 2266 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Shedding 11
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Shedding just north of Quintar cosplayer", 2267 + npc_index_offset), #Shedding 12
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Gold on east side of map", 2837 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Ore
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Climb the center mountain for Gold", 2839 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state)), #Ore
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " NPC - Jump across the treetops for Gold", 2840 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_horizontal_movement(state) and state.has(DIONE_STONE, player)), #Dust

        #Dione Shrine
        #Treasure chests
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Chest - Roof", 2154 + treasure_index_offset, lambda state: state.has(DIONE_STONE, player)), #Dione Shard chest
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Chest - Lobby", 2791 + treasure_index_offset), #Dione Shard chest
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Chest - 2nd floor", 2792 + treasure_index_offset), #Dione Shard chest
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Chest - 2nd floor balcony", 1146 + treasure_index_offset), #Dione Shard chest
        LocationData(DIONE_SHRINE_AP_REGION, "Overpass Chest - Glide SW from top of shrine 1", 3535 + treasure_index_offset, lambda state: logic.has_glide(state) and state.has(DIONE_STONE, player)), #4th Scrap on main Overpass map
        LocationData(DIONE_SHRINE_AP_REGION, "Overpass Chest - Glide SW from top of shrine 2", 2749 + treasure_index_offset, lambda state: logic.has_glide(state) and state.has(DIONE_STONE, player)), #Life Jewel Overpass main map

        #NPCs
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " NPC - Shedding on roof", 2264 + npc_index_offset, lambda state: state.has(DIONE_STONE, player)), #Shedding 9
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " NPC - Glide SW from top of shrine to Gold", 2838 + npc_index_offset, lambda state: logic.has_glide(state) and state.has(DIONE_STONE, player)), #Ingot on Overpass main map

        #Quintar Mausoleum
        #Treasure chests
        LocationData(QUINTAR_MAUSOLEUM_AP_REGION, QUINTAR_MAUSOLEUM_DISPLAY_NAME + " Chest - Past the switches race", 2153 + treasure_index_offset, lambda state: logic.has_fast(state)), #(688, 114, -464) Babel Quintar chest
        LocationData(QUINTAR_MAUSOLEUM_AP_REGION, QUINTAR_MAUSOLEUM_DISPLAY_NAME + " Chest - Rocky room", 3401 + treasure_index_offset), #(664, 129, -425) Quintar Mausoleum map chest
        LocationData(QUINTAR_MAUSOLEUM_AP_REGION, QUINTAR_MAUSOLEUM_DISPLAY_NAME + " Chest - Glowing grass room", 3768 + treasure_index_offset), #(709, 129, -442) Wind Thresher chest
        LocationData(QUINTAR_MAUSOLEUM_AP_REGION, "Underpass Chest - Up the waterfall inside Quintar Mausoleum", 3674 + treasure_index_offset), #(614, 146, -410) 6th Scrap chest on main Underpass map

        #Eastern Chasm
        #Treasure chests
        LocationData(EASTERN_CHASM_AP_REGION, EASTERN_CHASM_DISPLAY_NAME + " Chest - Overgrown opposite of chasm", 3543 + treasure_index_offset), #Eastern Chasm map chest

        #Tall Tall Heights
        #Treasure chests
        #Boomer Overlook
        LocationData(BOOMER_OVERLOOK_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Above the Boomer Society", 2844 + treasure_index_offset),  # Z-Potion Pouch chest
        #Note: this chest is not technically connected to this region but it has the exact same requirements to get to it from Boomer Society/Tall, Tall Heights Save Point
        LocationData(BOOMER_OVERLOOK_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Lonely chest over the ridge from Boomer Society", 2428 + treasure_index_offset),  # Ether
        #Greenshire Overlook
        LocationData(GREENSHIRE_OVERLOOK_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Past the icy Chips Challenge", 2786 + treasure_index_offset, lambda state: logic.can_push_ice_block_and_goat(state, TALL_TALL_HEIGHTS_DISPLAY_NAME) or logic.has_glide(state)), #Tear Seed chest
        #Tall, Tall Heights Save Point
        LocationData(TALL_TALL_SAVE_POINT_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Past the 2nd icy Chips Challenge", 2788 + treasure_index_offset, lambda state: logic.can_push_ice_block_and_goat(state, TALL_TALL_HEIGHTS_DISPLAY_NAME) or logic.has_glide(state)),  # Tear Seed chest
        LocationData(TALL_TALL_SAVE_POINT_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Past the 3rd icy Chips Challenge", 1254 + treasure_index_offset, lambda state: logic.can_push_ice_block_and_goat(state, TALL_TALL_HEIGHTS_DISPLAY_NAME) or logic.has_glide(state)),  # Potion chest
        #Lower Ice Lakes
        LocationData(LOWER_ICE_LAKES_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Past the Chips Challenge fishing hut", 1578 + treasure_index_offset, lambda state: logic.can_push_ice_block_and_goat(state, TALL_TALL_HEIGHTS_DISPLAY_NAME) or logic.has_glide(state)),  # Frost Reaper chest
        LocationData(LOWER_ICE_LAKES_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Tall stones and blue flowers", 2992 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state)),  # Potion Pouch chest
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Underpass Chest - Ice swimming instead of ice fishing", 3623 + treasure_index_offset, lambda state: logic.has_swimming(state)),  # (191, 172, -437) (Underwater) Underpass Scrap chest
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Overpass Chest - Past Tall Tall Heights spiky tunnel to Salmon River", 3538 + treasure_index_offset),  # 1st Overpass (Cloudy Wind) Scrap
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Underpass Chest - Tall Tall Heights spiky tunnel to Salmon River 1", 3672 + treasure_index_offset),  # Underpass (Ice Pass) Scrap
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Underpass Chest - Tall Tall Heights spiky tunnel to Salmon River 2", 1601 + treasure_index_offset),  # Underpass (Ice Pass) Potion
        #Upper Ice Lakes
        LocationData(UPPER_ICE_LAKES_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Above the Triton Shrine", 2795 + treasure_index_offset),  # Ether chest
        #Tall, Tall Diamondsmith
        LocationData(TALL_TALL_DIAMONDSMITH_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Parkour off the diamondsmith beneath the dead tree", 2810 + treasure_index_offset),  # Judo Gi chest
        #Slip Glide Ride Exit
        LocationData(SLIP_GLIDE_RIDE_EXIT_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Break the ice", 2744 + treasure_index_offset),  # Radiance Northern Cave
        #Sequoia Athenaeum Entrance
        LocationData(SEQUOIA_ATHENAEUM_ENTRANCE_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - East of the souvenir store", 2993 + treasure_index_offset),  # Money chest
        #Sequoia Athenaeum Balcony
        LocationData(SEQUOIA_ATHENAEUM_BALCONY_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - A funny chest happened on the way to the Athenaeum", 2994 + treasure_index_offset),  # Z-Potion chest
        LocationData(SEQUOIA_ATHENAEUM_BALCONY_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - East of the Athenaeum", 2565 + treasure_index_offset),  # Potion Pouch chest
        #Tall, Tall Tall Chest
        LocationData(TALL_TALL_TALL_CHEST_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Chest - Athenaeum outdoors Chip's Challenge (or be a bird)", 2785 + treasure_index_offset), #Insignia Helm chest

        #NPCs
        #Todo NPCs Job Masters: Tall Tall Heights (Outpost) map has Master Chemist ID 3707 (491, 221, -389); gives you Chemist Seal in exchange for job mastery
        #Todo NPCs Player Options: (197, 192, -441) do we want a filter option to add the guys who fish things up for you
        #Boomer Overlook
        LocationData(BOOMER_OVERLOOK_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Gold above the Boomer Society", 1600 + npc_index_offset), #Ingot
        #Tall, Tall Ramparts Crag Chest
        LocationData(TALL_TALL_RAMPARTS_CRAG_CHEST_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Gold tucked in melted snow past the Chip's Challenge east of shrine", 2846 + npc_index_offset),  # Ore
        #Greenshire Overlook
        LocationData(GREENSHIRE_OVERLOOK_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - I bek you can get this one (or come back with the bird) for Gold", 2845 + npc_index_offset, lambda state: logic.has_glide(state) or logic.can_push_ice_block_and_goat(state, TALL_TALL_HEIGHTS_DISPLAY_NAME)),  # Ingot
        #Lower Ice Lakes
        LocationData(LOWER_ICE_LAKES_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Melted snow Gold past the chest east of the Athenaeum", 2847 + npc_index_offset, lambda state: logic.has_horizontal_movement(state) or logic.has_vertical_movement(state)),  # Ingot
        LocationData(LOWER_ICE_LAKES_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Fish in the hut", 1549 + npc_index_offset, lambda state: state.has("Item - Tough Rod", player) and state.has("Item - Fly Lure", player)),  # Z8_FisherInHut (197, 192, -441)
        LocationData(LOWER_ICE_LAKES_AP_REGION, "Overpass NPC - Gold past Tall Tall Heights spiky tunnel to Salmon River", 2710 + npc_index_offset),  # 1st Gold Dust Overpass (Cloudy Wind)
        #Upper Ice Lakes
        LocationData(UPPER_ICE_LAKES_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Chip Challenge himself", 2388 + npc_index_offset),
        #Land's End Cottage Ridge
        LocationData(LANDS_END_COTTAGE_RIDGE_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Hop along spike mountain to Gold", 2853 + npc_index_offset), #Dust
        #Slip Glide Ride Exit
        LocationData(SLIP_GLIDE_RIDE_EXIT_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Gold by the breakable ice wall", 2814 + npc_index_offset), #Ingot
        #Sequoia Athenaeum Balcony
        LocationData(SEQUOIA_ATHENAEUM_BALCONY_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Gold past the Athenaeum Chips Challenge", 1602 + npc_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)),  # Dust
        #Icy Spikes Madness
        LocationData(ICY_SPIKES_MADNESS_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Treacherous landing Gold above the spikes", 1584 + npc_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)), #Ore

        #Northern Cave
        #Treasure chests
        #Lower Northern Cave
        LocationData(LOWER_NORTHERN_CAVE_AP_REGION, NORTHERN_CAVE_DISPLAY_NAME + " Chest - Island in the ice", 2787 + treasure_index_offset), #Tear Seed chest
        #Ice Cell
        LocationData(ICE_CELL_AP_REGION, NORTHERN_CAVE_DISPLAY_NAME + " Chest - Ominous Chips Challenge cave", 1579 + treasure_index_offset), #Ice Cell Key chest
        #Note: ibek here requires ice block; check can be made with quintar and not owl but the owl is required from Slip Glide Ride save point or Ice Cell start
        LocationData(ICE_CELL_AP_REGION, NORTHERN_CAVE_DISPLAY_NAME + " Chest - Hop along the igloos or Quintar skip the Chip", 1552 + treasure_index_offset, lambda state: logic.has_glide(state) or logic.can_push_ice_block_and_goat(state, NORTHERN_CAVE_DISPLAY_NAME)), #Apprentice chest
        #Upper Northern Cave
        LocationData(UPPER_NORTHERN_CAVE_AP_REGION, NORTHERN_CAVE_DISPLAY_NAME + " Chest - Past the wiggly block spike pit", 3001 + treasure_index_offset), #Money chest

        #NPCs
        #Upper Northern Cave
        LocationData(UPPER_NORTHERN_CAVE_AP_REGION, NORTHERN_CAVE_DISPLAY_NAME + " NPC - Gold past the wiggly block spike pit", 2815 + npc_index_offset), #Ore

        #Lands End
        #Treasure chests
        #Land's End Northern Peak
        LocationData(LANDS_END_NORTHERN_PEAK_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - Brave the spikes to climb the northern peak", 3002 + treasure_index_offset),  # Money chest
        #Land's End
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - Definitely requires Quintar *wink* among the first spikes 1", 2849 + treasure_index_offset), #Ether chest
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - Definitely requires Quintar *wink* among the first spikes 2", 3003 + treasure_index_offset), #Potion chest
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - To defeat the Huns", 2740 + treasure_index_offset, lambda state: logic.has_glide(state) or logic.has_vertical_movement(state)), #Blue Cape chest
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - Tucked up high against River Cats Ego", 1692 + treasure_index_offset), #Blue Cape chest
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - In spikes and storm", 1358 + treasure_index_offset, lambda state: logic.has_horizontal_movement(state)), #Defender chest
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - Fancy some spikes cliff diving?", 1693 + treasure_index_offset), #Rune Ward chest
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - By the lovely owl tree", 1561 + treasure_index_offset), #Callisto Stone chest
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Chest - Inside the shrine", 3017 + treasure_index_offset), #Ether chest
        LocationData(LANDS_END_AP_REGION, "Overpass Chest - Lonely mountain ledge below owl shrine", 3678 + treasure_index_offset, lambda state: logic.has_glide(state)), #(191, 177, -214) 9th Scrap on main Overpass map

        #NPCs
        #Land's End Northern Peak
        LocationData(LANDS_END_NORTHERN_PEAK_AP_REGION, LANDS_END_DISPLAY_NAME + " NPC - Lets get down to business in the mountains for Gold", 2848 + npc_index_offset), #Ingot
        #Land's End
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " NPC - Pillar Gold by River Cats Ego", 2850 + npc_index_offset), #Ore
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " NPC - Gold in spikes and storm", 2851 + npc_index_offset, lambda state: logic.has_horizontal_movement(state)), #Dust
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " NPC - Gold behind the shrine", 2852 + npc_index_offset), #Ingot
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " NPC - Owl Drum", 1176 + npc_index_offset),

        #Slip Glide Ride
        #Treasure chests
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - Back out to 1st room", 2554 + treasure_index_offset, lambda state: logic.has_key(state, RED_DOOR_KEY)), #Money chest
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - Climb up and fall down", 1172 + treasure_index_offset), #Plate of Lion chest
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - Sparks and tar", 1298 + treasure_index_offset), #Red Door Key chest
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - To the left through 2nd red lock", 1698 + treasure_index_offset, lambda state: logic.has_key(state, RED_DOOR_KEY, 2)), #Red Door Key chest
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - Through 1st red lock", 1716 + treasure_index_offset, lambda state: logic.has_key(state, RED_DOOR_KEY)), #Red Door Key chest
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - Past the mean Ibek jump", 1282 + treasure_index_offset, lambda state: logic.has_key(state, RED_DOOR_KEY)), #Sages Walker chest
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Chest - Nickelodeon slime time :)", 1269 + treasure_index_offset), #Seekers Garb chest

        #Crystals
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SUMMONER_JOB_CRYSTAL_LOCATION, 1714 + crystal_index_offset, lambda state: logic.has_key(state, RED_DOOR_KEY, 3)),

        #Sequoia Athenaeum
        #Treasure chests
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - Atop the shelves above the books door", 2932 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)), #(412, 200, -551) Spellsword Helm chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - Bullshit book-smart Chips Challenge", 2569 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)), #(403, 199, -547) Z-Potion Pouch chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - Brain-dumb Chips Challenge", 2322 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)), #(415, 180, -570) Ice Puzzle Key chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - 3rd library Chips Challenge", 2375 + treasure_index_offset, lambda state: logic.has_key(state, ICE_PUZZLE_KEY) and logic.has_vertical_movement(state) and logic.has_glide(state)), #(396, 180, -570) Ice Puzzle Key chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - Chips Challenge ice squared", 2341 + treasure_index_offset, lambda state: logic.has_key(state, ICE_PUZZLE_KEY, 2) and logic.has_vertical_movement(state) and logic.has_glide(state)), #(396, 164, -570) Ice Puzzle Key chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - Chips Challenge we cheated on this one", 2371 + treasure_index_offset, lambda state: logic.has_key(state, ICE_PUZZLE_KEY, 3) and logic.has_vertical_movement(state) and logic.has_glide(state)), #(415, 164, -572) Ice Puzzle Key chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - Triple Chip Challenge", 2372 + treasure_index_offset, lambda state: logic.has_key(state, ICE_PUZZLE_KEY, 4) and logic.has_vertical_movement(state) and logic.has_glide(state)), #(434, 164, -570) Ice Puzzle Key chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - Shattered labyrinth Chips Challenge", 2373 + treasure_index_offset, lambda state: logic.has_key(state, ICE_PUZZLE_KEY, 5) and logic.has_vertical_movement(state) and logic.has_glide(state)), #(424, 148, -570) Ice Puzzle Key chest
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Chest - You expected another Chips Challenge, but it was me, Dio!", 2335 + treasure_index_offset, lambda state: logic.has_key(state, ICE_PUZZLE_KEY, 6) and logic.has_vertical_movement(state) and logic.has_glide(state)), #(415, 131, -565) Skeleton Key chest

        #Northern Stretch
        #Treasure chests
        LocationData(SUMMONERS_TOWER_AP_REGION, "Overpass Chest - At the base of Summoners Lookout", 3655 + treasure_index_offset), #Northern Stretch map in Overpass (Outpost)

        #Castle Ramparts
        #Treasure chests
        #Lone Chest Rampart
        LocationData(LONE_CHEST_RAMPART_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " Chest - Tucked beside eastern turret", 1547 + treasure_index_offset), #(443, 206, -378) Money chest
        #Peak Ramparts
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " Chest - Below the crystal", 2908 + treasure_index_offset), #(407, 228, -383) Castle Ramparts map chest
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " Chest - Jump down from eastern save point", 2742 + treasure_index_offset), #(440, 227, -386) Conquest chest
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " Chest - Jump down from western save point", 2741 + treasure_index_offset), #(369, 227, -386) Rune Sword chest
        #Technically Castle Sequoia but they're in a locked room only accessible from Peak Ramparts
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Locked Ramparts storage room 1", 2758 + treasure_index_offset, lambda state: logic.has_key(state, RAMPART_KEY)), #(375, 232, -452) (Skums) Decapitator chest
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Locked Ramparts storage room 2", 3657 + treasure_index_offset, lambda state: logic.has_key(state, RAMPART_KEY)), #(371, 231, -457) (Skums) Castle Sequoia map chest

        #NPCs
        #Peak Ramparts
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " NPC - Western Gold above spikes", 2843 + npc_index_offset, lambda state: logic.has_glide(state)), #(354, 231, -429) Ingot
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " NPC - Eastern Gold above spikes", 2842 + npc_index_offset, lambda state: logic.has_glide(state)), #(458, 231, -436) Ore

        #Crystals
        #Peak Ramparts
        LocationData(PEAK_RAMPARTS_AP_REGION, BEASTMASTER_JOB_CRYSTAL_LOCATION, 1370 + crystal_index_offset, lambda state: logic.has_glide(state)), #(404, 243, -386)

        #The Chalice of Tar
        #Treasure chests
        LocationData(THE_CHALICE_OF_TAR_AP_REGION, THE_CHALICE_OF_TAR_DISPLAY_NAME + " Chest - At the tippy-top", 3544 + treasure_index_offset, lambda state: logic.has_vertical_movement(state)), #The Chalice of Tar map chest
        LocationData(THE_CHALICE_OF_TAR_AP_REGION, THE_CHALICE_OF_TAR_DISPLAY_NAME + " Chest - Dont let your feathers touch the tar", 2587 + treasure_index_offset), #Vermillion Book chest
        LocationData(THE_CHALICE_OF_TAR_AP_REGION, THE_CHALICE_OF_TAR_DISPLAY_NAME + " Chest - Post tar tunnel", 2806 + treasure_index_offset), #Windsong chest

        #NPCs
        #Todo NPCs Job Masters: The Chalice of Tar has Master Mimic ID 3606 (526, 234, -438); gives you Mimic Seal in exchange for job mastery
        LocationData(THE_CHALICE_OF_TAR_AP_REGION, THE_CHALICE_OF_TAR_DISPLAY_NAME + " NPC - Gold sparkling above the Overpass on the way up", 2841 + npc_index_offset), #Ore

        #Crystals
        LocationData(THE_CHALICE_OF_TAR_AP_REGION, MIMIC_JOB_CRYSTAL_LOCATION, 3701 + crystal_index_offset, lambda state: logic.has_vertical_movement(state)),

        #Flyers Crag
        #Treasure chests
        LocationData(FLYERS_CRAG_AP_REGION, FLYERS_CRAG_DISPLAY_NAME + " Chest - You cant miss it", 3656 + treasure_index_offset), #(658, 216, -170) Flyers Crag map chest
        
        #NPCs
        LocationData(FLYERS_CRAG_AP_REGION, FLYERS_CRAG_DISPLAY_NAME + " NPC - Gold twinsies the 1st south of Ganymede Shrine", 2820 + npc_index_offset), #(695, 137, -159) Dust
        LocationData(FLYERS_CRAG_AP_REGION, FLYERS_CRAG_DISPLAY_NAME + " NPC - Gold twinsies the 2nd south of Ganymede Shrine", 2819 + npc_index_offset), #(686, 132, -162) Ingot

        #Flyers Lookout
        #Treasure chests
        #There are no checks here unless an Overpass Scrap shows up

        #Jidamba Tangle
        #Treasure chests
        #Forest Floor
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Inside overgrown building E of Eaclaneya", 1629 + treasure_index_offset),  # Demon Plate chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Atop overgrown building E of Eaclaneya", 3028 + treasure_index_offset),  # Ether chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - NW foliage", 2807 + treasure_index_offset),  # Partizan chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Tucked below NW foliage", 3025 + treasure_index_offset),  # Potion chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - North of foliage river", 3027 + treasure_index_offset),  # Z-Potion chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Smack in the center of the foliage", 1632 + treasure_index_offset),  # Foliage Key chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Up a tree in north foliage", 3024 + treasure_index_offset),  # Ether chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Along a river through the foliage", 3026 + treasure_index_offset),  # Ether chest
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Island in the river through the foliage", 3011 + treasure_index_offset),  # Tower Shield chest
        #Jidamba Cave
        LocationData(JIDAMBA_CAVE_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Underground sneaky passage by NE cave exit", 2797 + treasure_index_offset),  # Ravens Hood chest
        LocationData(JIDAMBA_CAVE_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Hop from underground root to sneaky passage pond", 2798 + treasure_index_offset, lambda state: logic.has_glide(state)),  # Ravens Cloak chest
        LocationData(JIDAMBA_CAVE_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Accompanied by orange cave flowers", 1435 + treasure_index_offset, lambda state: logic.has_glide(state)),  # Cave Key chest
        #Eaclaneya Courtyard
        LocationData(JIDAMBA_EACLANEYA_COURTYARD_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Eaclaneya entrance hall", 2919 + treasure_index_offset),  # Jidamba Tangle map chest
        #Summit
        LocationData(JIDAMBA_SUMMIT_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Tucked against eastern side of Eaclaneya", 2801 + treasure_index_offset),  # Flame Guard chest
        LocationData(JIDAMBA_SUMMIT_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Atop Eaclaneya", 2808 + treasure_index_offset),  # Rune Bow chest
        LocationData(JIDAMBA_SUMMIT_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Tucked against western side of Eaclaneya", 2802 + treasure_index_offset),  # Flamespike chest
        LocationData(JIDAMBA_SUMMIT_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Scramble down the escarpment from Weaver Outpost to pedestal", 2803 + treasure_index_offset),  # Siege Bow chest
        #Canopy
        LocationData(JIDAMBA_CANOPY_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Up in the canopy south of shrine", 1171 + treasure_index_offset),  # Demon Helm chest
        LocationData(JIDAMBA_CANOPY_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Chest - Smack in the center of the canopy", 1631 + treasure_index_offset),  # Canopy Key chest

        #NPCs
        #Todo NPCs Job Masters: Jidamba Tangle (Outpost) has Master Weaver ID 3579 (627, 140, 77); gives you Weaver Seal in exchange for job mastery
        #Forest Floor
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Diamond atop broken ruins along the beach", 2872 + npc_index_offset, lambda state: logic.has_glide(state)),  # Ore
        #Diamondsmith
        LocationData(JIDAMBA_DIAMONDSMITH_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Damp Diamond lurking beneath diamondsmith", 2869 + npc_index_offset),  # Ingot
        #Southwest Beach
        LocationData(JIDAMBA_SOUTHWEST_BEACH_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Diamond hot girl summer on the beach", 2873 + npc_index_offset),  # Dust
        #South Cliff
        LocationData(JIDAMBA_SOUTH_CLIFF_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Splish splash Diamond", 2871 + npc_index_offset),  # Dust
        #Southwest Beach Cliff
        LocationData(JIDAMBA_SOUTHWEST_BEACH_CLIFF_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Diamond at southern mouth of cave", 2874 + npc_index_offset, lambda state: logic.has_horizontal_movement(state)),  # Ingot
        #Summit
        LocationData(JIDAMBA_SUMMIT_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Fly from Summoners weeping tree to hot tub Diamond", 2876 + npc_index_offset, lambda state: logic.has_glide(state)),  # Ingot
        LocationData(JIDAMBA_SUMMIT_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Diamond atop broken ruins by the Summoner tree", 2875 + npc_index_offset, lambda state: logic.has_glide(state)),  # Ore
        #Canopy
        LocationData(JIDAMBA_CANOPY_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Chloe Queen of the Canopy", 2775 + npc_index_offset), #Super Rod (828, 119, 99); Fixed Missable
        LocationData(JIDAMBA_CANOPY_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Splash Mountain Diamond (pool at S end of canopy)", 2870 + npc_index_offset),  # Ore
        LocationData(JIDAMBA_CANOPY_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Splash Mountain Gold (pool at NE end of canopy)", 2900 + npc_index_offset),  # Ore
        LocationData(JIDAMBA_CANOPY_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Diamond in the boughs above the shrine", 2898 + npc_index_offset),  # Ingot
        LocationData(JIDAMBA_CANOPY_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Canopy Gold above big lake", 2899 + npc_index_offset), #Ingot

        #Jidamba Eaclaneya
        #Treasure chests
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Climb the lamp in the south room", 2799 + treasure_index_offset, lambda state: logic.has_glide(state) and logic.has_vertical_movement(state)), #Celestial Crown chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - At the end of spike hallway", 2755 + treasure_index_offset, lambda state: logic.has_glide(state)), #Flame Sword chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Monster cubby", 2920 + treasure_index_offset), #Jidamba Eaclaneya map chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Practice your swimming", 2282 + treasure_index_offset, lambda state: logic.has_glide(state)), #Ether Pouch chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Right side of the swimming puzzle", 2289 + treasure_index_offset, lambda state: logic.has_glide(state)), #Staff of Balance chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Glass elevator room", 2301 + treasure_index_offset, lambda state: logic.has_glide(state)), #Stardust Wand chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Underwater swimming puzzle", 2308 + treasure_index_offset, lambda state: logic.has_glide(state)), #Flameseeker chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Left side of underwater swimming puzzle", 2317 + treasure_index_offset, lambda state: logic.has_glide(state)), #Viridian Book chest
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Chest - Salmon Violin past the fish puzzles", 2288 + treasure_index_offset, lambda state: logic.has_glide(state)),

        #NPCs
        #1 Diamond Dust on Jidamba Eaclaneya Fish Floor map has been categorized under the Capital Pipeline

        #Crystals
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, WEAVER_JOB_CRYSTAL_LOCATION, 2403 + crystal_index_offset),

        #The Deep Sea
        #Treasure chests
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Descend into undersea vent where the flesh eaters live 1", 3451 + treasure_index_offset), #(878, 39, -536) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Touching Jidamba", 3658 + treasure_index_offset), #Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Ruins just south of Jidamba 1", 3659 + treasure_index_offset), #Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Locked sunken house off Jidamba with mighty arch 1", 3660 + treasure_index_offset, lambda state: logic.has_key(state, FORGOTTEN_KEY)), #(657, 53, 165) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Buried tunnel NW of Jidamba", 3661 + treasure_index_offset), #(545, 47, -31) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - By The Depths chasm SE of Shoudu Province", 3662 + treasure_index_offset), #(890, 51, -66) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Crumbling shrine 1", 3663 + treasure_index_offset), #(842, 53, -359) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Beside an undersea microruin NW of Tall Tall Heights", 3666 + treasure_index_offset), #(-23, 39, -557) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Underwater cove south of volcano", 3667 + treasure_index_offset), #(94, 59, 133) Deep Sea Scrap chest
        #next 2 scraps from The Deep Sea (Sand Bar)
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Sunken shipwreck off west coast of Sara Sara Beach", 3664 + treasure_index_offset), #(-364, 53, -183) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Undersea valley S of Sara Sara Beach", 3665 + treasure_index_offset), #(-226, 49, 164) Deep Sea Scrap chest
        #next scrap from The Deep Sea (Shrooms)
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Cavern below N coast of Tall Tall Heights", 3668 + treasure_index_offset), #(254, 53, -547) Deep Sea Scrap chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Descend into undersea vent where the flesh eaters live 2", 2767 + treasure_index_offset), #(872, 39, -517) Forgotten Key chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Crumbling shrine 2", 2290 + treasure_index_offset), #(838, 52, -357) Oven Mitt chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Ruins just south of Jidamba 2", 2937 + treasure_index_offset), #Paladin Wand chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Hidden tunnel in canyon W of cheeky sunroof NW of Jidamba", 2589 + treasure_index_offset), #(582, 47, -51) Rampart Key chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Locked sunken house off Jidamba with mighty arch 2", 2766 + treasure_index_offset, lambda state: logic.has_key(state, FORGOTTEN_KEY)), #(663, 54, 165) Soul Keeper chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Locked *wink* sunken house off Jidamba 1", 2768 + treasure_index_offset), #(649, 53, 195) Zether chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Locked *wink* sunken house off Jidamba 2", 3726 + treasure_index_offset), #(646, 53, 196) Zether Pouch chest
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Chest - Quizard challenge below N coast of Tall Tall Heights", 595 + treasure_index_offset), #(270, 29, -591) Treasure Finder chest

        #NPCs
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Locked *wink* sunken house 2 off Jidamba Diamond", 2519 + npc_index_offset), #(639, 54, 182) Dust
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Locked *wink* sunken house 2 off Jidamba Gold", 2518 + npc_index_offset), #(648, 54, 180)  Dust
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Burrow to burrow crab", 3409 + npc_index_offset), #(20, 53, 251) Crab 1
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Tall tall crab S of volcano", 3426 + npc_index_offset), #(76, 76, 178) Crab 2
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Crab in underwater cove south of volcano", 3427 + npc_index_offset), #(96, 60, 131) Crab 3
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Zigzaggedy crab NW of Tall Tall Heights", 3428 + npc_index_offset), #(142, 51, -611) Crab 4
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Crab strolling around the undersea block", 3429 + npc_index_offset), #(60, 53, -609) Crab 5
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Crab clinging to SW underwater volcano slope", 3430 + npc_index_offset), #(54, 62, 155) Crab 6
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Low low crab S of volcano", 3431 + npc_index_offset), #(128, 49, 196) Crab 7
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Serpentine crab S of crab hole", 3432 + npc_index_offset), #(239, 53, -613) for some reason crab 8 is on (Depths Fix) submap
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Patrolling crab S of crab hole", 3433 + npc_index_offset), #(254, 53, 215) Crab 9
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Crab living on the edge S of crab hole", 3434 + npc_index_offset), #(306, 53, 224) Crab 10
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Crab on a mission N of Tall Tall Heights", 3435 + npc_index_offset), #(288, 53, -620) Crab 11
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Middle of nowhere sandy speedster crab", 3436 + npc_index_offset), #(58, 52, 244) Crab 12
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Putt Putt Crab mows the lawn", 3437 + npc_index_offset), #(54, 52, 200) Crab 13
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - King of the middle of nowhere ocean crab", 3438 + npc_index_offset), #(52, 76, -616) Crab 14
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Crab scuttling SE of volcano", 3439 + npc_index_offset), #(207, 53, 152) Crab 15
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Undersea Crab People Crab Retirement Home south of Salmon Race start", 3424 + npc_index_offset, lambda state: state.has(UNDERSEA_CRAB, player, 15)), #(256, 63, 113)
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Fastest squid in the West", 3450 + npc_index_offset), #(-314, 64, -624) (swims in a fixed path; slightly slower than golden Quintar but faster than royal salmon) Z35_SpeedOcto
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Sunken shipwreck Gold off west coast of Sara Sara Beach 1", 2855 + npc_index_offset), #(-367, 53, -182) Dust
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Sunken shipwreck Gold off west coast of Sara Sara Beach 2", 2857 + npc_index_offset), #(-356, 55, -167) Ingot
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " NPC - Sunken shipwreck Gold off west coast of Sara Sara Beach 3", 2856 + npc_index_offset), #(-370, 53, -173) Ore

        #Jade Cavern
        #Treasure chests
        LocationData(JADE_CAVERN_AP_REGION, JADE_CAVERN_DISPLAY_NAME + " Chest - Tell Archie to say hi to the Quizard", 3604 + treasure_index_offset), #(239, 99, -124) Jade Cavern map chest

        #NPCs
        #Todo NPCs CheckOrNot Job Masters: this guy trades you a thing for each job seal you've gotten from a job master for mastering that job
        #LocationData(JADE_CAVERN, JADE_CAVERN_DISPLAY_NAME + " NPC - Jade Cavern Map chest", 3603 + npc_index_offset), #(255, 91, -90)

        #Continental Tram
        #Treasure chests
        LocationData(CONTINENTAL_TRAM_AP_REGION, CONTINENTAL_TRAM_DISPLAY_NAME + " Chest - Tickets please 1", 1844 + treasure_index_offset), #Continental Tram map chest
        LocationData(CONTINENTAL_TRAM_AP_REGION, CONTINENTAL_TRAM_DISPLAY_NAME + " Chest - End of the line", 3012 + treasure_index_offset), #Nomads Guard chest
        LocationData(CONTINENTAL_TRAM_AP_REGION, CONTINENTAL_TRAM_DISPLAY_NAME + " Chest - Tickets please 2", 1654 + treasure_index_offset), #Tram Key chest

        #NPCs
        LocationData(CONTINENTAL_TRAM_AP_REGION, CONTINENTAL_TRAM_DISPLAY_NAME + " NPC - Diamond hanging out with the conscript 1", 2895 + npc_index_offset), #Dust
        LocationData(CONTINENTAL_TRAM_AP_REGION, CONTINENTAL_TRAM_DISPLAY_NAME + " NPC - Diamond hanging out with the conscript 2", 2894 + npc_index_offset), #Ingot

        #Zones (End-Game)
        #Ancient Labyrinth
        #Treasure chests
        LocationData(ANCIENT_LABYRINTH_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Chest - Dungeon East sneaky hole in wall", 1274 + treasure_index_offset), #(-186, 125, -316) F2 Money chest
        LocationData(ANCIENT_LABYRINTH_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Chest - Dungeon West sneaky hole in wall", 2412 + treasure_index_offset), #(-190, 125, -316) F2 Archmage Vest chest
        LocationData(ANCIENT_LABYRINTH_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Chest - B1 Searching for greener pastures", 1738 + treasure_index_offset), #(-209, 87, -311) F3 Vita Crown chest
        LocationData(LABYRINTH_WEIRD_REBAR_HALLWAY_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Chest - B2 North weird rebar hallway", 2924 + treasure_index_offset), #(-185, 63, -363) F4 Judgement chest
        LocationData(LABYRINTH_WEIRD_REBAR_HALLWAY_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Chest - B2 East weird rebar hallway", 2926 + treasure_index_offset), #(-162, 63, -336) F4 Zether Pouch chest
        LocationData(LABYRINTH_CORE_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Chest - B4 Tar pit platform", 3649 + treasure_index_offset), #(-185, 38, -301) F6 Ancient Labyrinth map chest
        LocationData(LABYRINTH_CORE_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Chest - Dog-headed dogshit boss", 2591 + treasure_index_offset), #(-219, 27, -350) F7 Mirror Shield chest

        #NPCs
        LocationData(ANCIENT_LABYRINTH_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " NPC - Dungeon East sneaky hole in wall Diamond", 2881 + npc_index_offset), #(-186, 125, -300) F2 Ingot
        LocationData(ANCIENT_LABYRINTH_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " NPC - Sneaky hole in wall Diamond in entry touchdown room", 2880 + npc_index_offset), #(-182, 126, -326) F2 Ore
        LocationData(ANCIENT_LABYRINTH_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " NPC - B1 Thats right, Diamond goes in the bluish-white square hole", 2882 + npc_index_offset), #(-200, 98, -334) F3 Ingot

        #The Sequoia
        #Treasure chests
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Chest - Waterfall climb sneaky hollow", 2934 + treasure_index_offset), #(-286, 90, -539) Stealth Cape chest
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Chest - Balanced on bark", 2437 + treasure_index_offset), #(-250, 174, -512) Battle Band chest
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Chest - Back indoors then follow water channel outside", 2935 + treasure_index_offset), #(-296, 182, -533) Sange chest
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Chest - Waterfall climb sneaky eastern exit", 2884 + treasure_index_offset), #(-223, 118, -541) Zether Pouch chest
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Chest - Go out on a limb", 2887 + treasure_index_offset), #(-244, 168, -498) Z-Potion Pouch chest
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Chest - Back indoors by water channel", 2933 + treasure_index_offset), #(-282, 182, -528) Aphotic Edge chest
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Chest - Post-boss victory pedestal", 2451 + treasure_index_offset), #(-272, 241, -544) The Hand of Midas chest
        
        #NPCs
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " NPC - Low-hanging Diamond fruit", 2885 + npc_index_offset), #(-223, 160, -530) Dust
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " NPC - Waterfall climb sneaky eastern exit Diamond", 2883 + npc_index_offset), #(-237, 117, -563) Ore
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " NPC - Diamond glittering on a bough", 2886 + npc_index_offset), #(-311, 160, -540) Ore
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " NPC - Post-boss victory Diamond 1", 2889 + npc_index_offset), #(-269, 240, -545) Dust
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " NPC - Post-boss victory Diamond 2", 2890 + npc_index_offset), #(-268, 240, -547) Ingot
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " NPC - Post-boss victory Diamond 3", 2888 + npc_index_offset), #(-275, 240, -546) Ore

        #The Depths
        #Treasure chests
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Chest - Down among glowing blue seaweed between Poko Poko Desert & Jidamba 1", 2588 + treasure_index_offset), #(-358, 1, 18) Cerulean Book chest
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Chest - Down among glowing blue seaweed between Poko Poko Desert & Jidamba 2", 2714 + treasure_index_offset), #(-357, 2, 20) #Z-Potion chest

        #NPCs
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - S of Jidamba Diamond on blue rock 1", 2865 + npc_index_offset), #(692, 20, -618) Dust
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - S of Jidamba Diamond by seaweed river 1", 2868 + npc_index_offset), #(823, 17, -595) Dust
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Floating rock Diamond SE of Volcano 1", 2891 + npc_index_offset), #(161, 20, 240) Dust
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Diamond dive beside sunken shipwreck 1", 1214 + npc_index_offset), #(-377, 20, -220) Ingot
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Diamond dive beside sunken shipwreck 2", 2859 + npc_index_offset), #(-373, 19, -261) Ingot
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - S of Jidamba Diamond on blue rock 2", 2863 + npc_index_offset), #(784, 17, -611) Ingot
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - S of sunken town on blue rock", 2866 + npc_index_offset), #(629, 20, -615) Ingot
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Floating rock Diamond SE of Volcano 2", 2893 + npc_index_offset), #(180, 20, 255) Ingot
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Yellow flower Diamond W of Sara Sara Beach", 1213 + npc_index_offset), #(932, 19, -199) Ore
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Sneaky Diamond W of Sara Sara Beach", 2858 + npc_index_offset), #(924, 20, -235) Ore
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - S of Jidamba Diamond by seaweed river 2", 2864 + npc_index_offset), #(760, 12, -612) Ore
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - S of Jidamba Diamond by seaweed river 3", 2867 + npc_index_offset), #(722, 20, -604) Ore
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Floating rock Diamond SE of Volcano 3", 2892 + npc_index_offset), #(189, 30, 235) Ore
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Follow barnacled meat branches for Diamond 1", 2861 + npc_index_offset), #(-308, 12, 132) Dust
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Follow barnacled meat branches for Diamond 2", 2862 + npc_index_offset), #(-303, 14, 183) Ingot
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " NPC - Follow barnacled meat branches for Diamond 3", 2860 + npc_index_offset), #(-359, 10, 162) Ore

        #Castle Sequoia
        #Treasure chests
        #Map and Decapitator chests categorized in Castle Ramparts since they're in a locked room there requiring the Ramparts key
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Hop through keyhole over lava", 2515 + treasure_index_offset), #(422, 169, -406) (Skums) Zether Pouch chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Stared at by lava miniboss", 1465 + treasure_index_offset), #(427, 170, -441) (Skums) Z-Potion chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Enjoy riding lava shrooms", 1447 + treasure_index_offset), #(409, 169, -406) (Skums) Z-Potion Pouch chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Biiig bounce!", 1472 + treasure_index_offset), #(375, 153, -405) (Bounce) Beads of Defense chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Bounce up!!", 2949 + treasure_index_offset), #(401, 151, -404) (Bounce) Ether chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Bounce around!", 2948 + treasure_index_offset), #(401, 151, -424) (Bounce) Fenix Syrup chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Bounce right!", 2945 + treasure_index_offset), #(434, 154, -441) (Bounce) Potion chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Bounce up!", 2922 + treasure_index_offset), #(395, 155, -453) (Bounce) Protector chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Chilly uno in Chips Challenge of doom", 2927 + treasure_index_offset), #(387, 134, -431) (Ice) Kings Guard chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Chilly duo in Chips Challenge of doom", 1492 + treasure_index_offset), #(387, 134, -427) (Ice) Royal Guard chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - One fish", 2479 + treasure_index_offset), #(401, 119, -415) (Fish) Dream Hunter chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Two fish", 2509 + treasure_index_offset), #(388, 122, -445) (Fish) Nightingale chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Redfish bluefish", 2484 + treasure_index_offset), #(397, 119, -415) (Fish) Oily Sword chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Bounce for your life", 2510 + treasure_index_offset), #(364, 85, -424) (2D) Paladin Wand chest
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Chest - Throne snacks", 2505 + treasure_index_offset), #(401, 250, -478) (Throne) New World Stone chest

        #NPCs
        #NPCs CheckOrNot: Z58_StrandedShard ID 3785 (401, 183, -382); this gives you a Gaea Shard if you're stuck: no
        #NPCs Blocker: i think this guy might only show up in the vanilla game's randomizer? checks if Z58_EleOn (Z58 is Castle Sequoia); Z58Progression_Gate ID 3824 (400, 250, -478)

        #The New World
        #Treasure chests
        LocationData(THE_NEW_WORLD_AP_REGION, THE_NEW_WORLD_DISPLAY_NAME + " Chest - NW lavafall", 2930 + treasure_index_offset), #(-134, 8, 230) Lunar Mail chest
        LocationData(THE_NEW_WORLD_AP_REGION, THE_NEW_WORLD_DISPLAY_NAME + " Chest - Desolate peninsula past bounce shrooms", 2931 + treasure_index_offset, lambda state: logic.has_vertical_movement(state) and logic.has_glide(state)), #(-11, 12, -577) Mages Pike chest
        LocationData(THE_NEW_WORLD_AP_REGION, THE_NEW_WORLD_DISPLAY_NAME + " Chest - Tiny shrooms keep shed", 1938 + treasure_index_offset), #(-85, 8, 142) The New World map chest
    ]

    return location_table

def get_bosses(player: int, options: CrystalProjectOptions | None) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    location_table: List[LocationData] = [
        #IDs here are specifically the spark IDs or NPC IDs for where you go to fight them from Crystal Edit
        #Summons
        #Not included: Pinga (unused)
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Boss - Shaku Summon", 477 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 54)), #(118, 109, 10) Monster ID: 102
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Boss - Niltsi Summon", 1109 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 54)), #376, 178, -345 (Capital Sequoia (Maze) map) Monster ID: 93
        LocationData(SALMON_BAY_AP_REGION, SALMON_BAY_DISPLAY_NAME + " Boss - Guaba Summon", 1138 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 58)), #-50, 91, -330 Monster ID: 94
        LocationData(THE_UNDERCITY_AP_REGION, "Underpass Boss - Pah Summon", 1130 + boss_index_offset, lambda state: (logic.has_swimming(state) or logic.has_glide(state)) and state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 58)), #614, 91, -213 Monster ID: 97
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Boss - Tira Summon", 1132 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and (logic.has_vertical_movement(state) or logic.has_glide(state) or state.can_reach(QUINTAR_RESERVE_AP_REGION, player=player) or state.can_reach(GANYMEDE_SHRINE_AP_REGION, player=player)) and logic.is_area_in_level_range(state, 57)), #(720, 138, -278) Monster ID: 98
        LocationData(LAKE_DELENDE_AP_REGION, LAKE_DELENDE_DISPLAY_NAME + " Boss - Ioske Summon", 1111 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 57)), #97, 126, -211 Monster ID: 92
        LocationData(PAMOA_TREE_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Boss - Pamoa Summon", 1136 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 53)), #498, 218, -412 Monster ID: 91
        LocationData(JIDAMBA_SUMMIT_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Boss - Juses Summon", 1134 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 58)), #(672, 124, 106) Monster ID: 99
        #Mind's Delusion is part of the Coyote fight
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Boss - Coyote Summon", 1140 + boss_index_offset, lambda state: state.has(SUMMONER_JOB, player) and logic.is_area_in_level_range(state, 58)), #(-60, 53, 202) Monster ID: 95

        #Bosses
        #Not included: Bone Drinker (unused), Rexosaur (too RNG), Astley/Chloe/Reid/Talon Final Fights, Buttermint (you monster)
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Boss - Troll", 153 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 50)), #Monster ID: 8
        LocationData(GRAN_AP_REGION, DELENDE_DISPLAY_NAME + " Boss - Gran...?", 183 + boss_index_offset), #Monster ID: 28 (min level 30)
        LocationData(SOILED_DENLENDE_AP_REGION, SOILED_DEN_DISPLAY_NAME + " Boss - Bone Thief", 175 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 12)), #Monster ID: 12
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Boss - Guardian", 143 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 12)), #Monster ID: 23
        LocationData(DRAFT_SHAFT_CONDUIT_AP_REGION, DRAFT_SHAFT_CONDUIT_DISPLAY_NAME + " Boss - Canal Beast", 138 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 12)), #Monster ID: 18
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Boss - Sepulchra", 167 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 18)), #Monster ID: 27
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Boss - Knight", 128 + boss_index_offset, lambda state: logic.has_jobs(state, 3) and logic.is_area_in_level_range(state, 10)), #Monster ID: 212 (using Z7_CrystalCheckerNPC)
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Boss - Parasite", 333 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 19)), #Monster ID: 38
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Boss - Defeat L60 dummy and it shall appear...!", 3530 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 60)), #Monster ID: 303
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Boss - Enami", 458 + boss_index_offset, lambda state: (logic.has_key(state, COURTYARD_KEY) or logic.has_rental_quintar(state, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME) or logic.has_horizontal_movement(state)) and logic.is_area_in_level_range(state, 58)), #Monster ID: 49
        LocationData(JOJO_SEWERS_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Boss - Blood Slop", 758 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 26)), #Monster ID: 4
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " Boss - Fancy Quintar", 971 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 26)), #Monster ID: 68
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Boss - Warden", 907 + boss_index_offset, lambda state: logic.has_key(state, DARK_WING_KEY) and logic.is_area_in_level_range(state, 27)), #Monster ID: 37
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Boss - Crag Demon", 1118 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 50)), #Monster ID: 217
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Boss - Kuromanto", 698 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 29)), #Monster ID: 63
        LocationData(IBEK_CAVE_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Boss - Possessor", 1674 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 35)), #Monster ID: 221
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Boss - Final Sky Arena Fight: Arachlea", 1366 + boss_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 58)), #Monster ID: 252 (SkyArenaRegistrar)
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Boss - Blade Master", 1939 + boss_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 40)), #Monster ID: 145
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Boss - Shadow Master", 1940 + boss_index_offset, lambda state: (logic.has_swimming(state) or logic.has_horizontal_movement(state)) and logic.is_area_in_level_range(state, 40)), #Monster ID: 144
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Boss - Duel Master", 1941 + boss_index_offset, lambda state: (logic.has_vertical_movement(state) or logic.has_glide(state)) and logic.is_area_in_level_range(state, 40)), #Monster ID: 146
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Boss - Ancient Sword", 821 + boss_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 2) and logic.is_area_in_level_range(state, 39)), #Monster ID: 59
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Boss - Iguanadon & Iguanadin", 862 + boss_index_offset, lambda state: logic.has_key(state, SMALL_KEY, 4) and logic.has_key(state, BEAURIOR_BOSS_KEY) and logic.is_area_in_level_range(state, 40)), #Monster ID: 78 and 100
        LocationData(EASTERN_CHASM_AP_REGION, EASTERN_CHASM_DISPLAY_NAME + " Boss - Undergrowth", 3476 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 60)), #Monster ID: 293
        LocationData(SEQUOIA_ATHENAEUM_ENTRANCE_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Boss - Hermetic", 3637 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 55)), #Monster ID: 309
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Boss - The Owlbear", 2104 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 47)), #Monster ID: 143
        LocationData(SLIP_GLIDE_RIDE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Boss - Red Guardian", 1713 + boss_index_offset, lambda state: logic.has_key(state, RED_DOOR_KEY, 3) and logic.is_area_in_level_range(state, 49)), #Monster ID: 224
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " Boss - Rampart Demon", 1373 + boss_index_offset, lambda state: logic.has_glide(state) and logic.is_area_in_level_range(state, 54)), #Monster ID: 222
        LocationData(CONTINENTAL_TRAM_AP_REGION, CONTINENTAL_TRAM_DISPLAY_NAME + " Boss - Conscript", 1621 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 60)), #Monster ID: 242
        LocationData(LABYRINTH_CORE_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Boss - Anubis", 2473 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 62)), #Monster ID: 117
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Boss - Spirit Cage", 2453 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 63)), #Monster ID: 192
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Boss - The Devourer", 1265 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 65)), #Monster ID: 171
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Boss - The Old One", 206 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 65)), #Monster ID: 170
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Boss - The Enforcer", 1128 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 65)), #Monster ID: 172
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Boss - The Peacekeeper", 2579 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 63)), #Monster ID: 169
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Boss - With STEM WARD in hand, offer 4 Deity Eyes to battle Gabriel", 2580 + boss_index_offset, lambda state: state.has(DEITY_EYE, player, 4) and state.has(STEM_WARD, player) and logic.is_area_in_level_range(state, 65)), #Monster ID: 241
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Boss - Parasite X", 1457 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 56)), #Monster ID: 198 (Castle Sequoia (Skums) Z58_TrapdoorGuard)
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Boss - Neo Warden", 1477 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 57)), #Monster ID: 200 (Castle Sequoia (Bounce) Z58_F2TrapdoorGuard)
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Boss - Akamanto", 1503 + boss_index_offset, lambda state: logic.is_area_in_level_range(state, 58)), #Monster ID: 201 (Castle Sequoia (Ice) Z58_F3TrapdoorGuard)
        LocationData(THE_OLD_WORLD_AP_REGION, THE_OLD_WORLD_DISPLAY_NAME + " Boss - Periculum", 3650 + boss_index_offset), #Monster ID: 268 (min level 70)
        ]
    return location_table

def get_shops(player: int, options: CrystalProjectOptions | None) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)

    location_table: List[LocationData] = [
        #Zones (Beginner)
        #Spawning Meadows
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 1", 10013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 2", 20013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 3", 30013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 4", 40013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 5", 50013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 6", 60013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 7", 70013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 8", 80013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 9", 90013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 10", 100013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 11", 110013 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Knick Knacks 12", 120013 + shop_index_offset),

        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Stew 1", 10014 + shop_index_offset),
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Shop - Nans Stew 2", 20014 + shop_index_offset),

        #Delende
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Weapon Merchant 1", 10052 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Weapon Merchant 2", 20052 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Weapon Merchant 3", 30052 + shop_index_offset),

        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 1", 10063 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 2", 20063 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 3", 30063 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 4", 40063 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 5", 50063 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 6", 60063 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 7", 70063 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Armor Merchant 8", 80063 + shop_index_offset),

        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Fish Merchant 1", 10199 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Fish Merchant 2", 20199 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Fish Merchant 3", 30199 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Fish Merchant 4", 40199 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Fish Merchant 5", 50199 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Fish Hatchery Fish Merchant 6", 60199 + shop_index_offset),

        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Weapons Merchant camped in front of Pale Grotto 1", 10115 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Weapons Merchant camped in front of Pale Grotto 2", 20115 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Weapons Merchant camped in front of Pale Grotto 3", 30115 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Weapons Merchant camped in front of Pale Grotto 4", 40115 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Weapons Merchant camped in front of Pale Grotto 5", 50115 + shop_index_offset),

        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 1", 10446 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 2", 20446 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 3", 30446 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 4", 40446 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 5", 50446 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 6", 60446 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 7", 70446 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Armor Merchant camped in front of Pale Grotto 8", 80446 + shop_index_offset),

        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Item Merchant camped in front of Pale Grotto 1", 10266 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Item Merchant camped in front of Pale Grotto 2", 20266 + shop_index_offset),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Shop - Item Merchant camped in front of Pale Grotto 3", 30266 + shop_index_offset),

        #Seaside Cliffs
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 1", 10116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 2", 20116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 3", 30116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 4", 40116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 5", 50116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 6", 60116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 7", 70116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 8", 80116 + shop_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Shop - Camp Merchant 9", 90116 + shop_index_offset),

        #Mercury Shrine
        LocationData(MERCURY_SHRINE_AP_REGION, MERCURY_SHRINE_DISPLAY_NAME + " Shop - Attendant 1", 10132 + shop_index_offset),
        LocationData(MERCURY_SHRINE_AP_REGION, MERCURY_SHRINE_DISPLAY_NAME + " Shop - Attendant 2", 20132 + shop_index_offset),
        LocationData(MERCURY_SHRINE_AP_REGION, MERCURY_SHRINE_DISPLAY_NAME + " Shop - Attendant 3", 30132 + shop_index_offset),

        #Proving Meadows
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Item Merchant 1", 10253 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Item Merchant 2", 20253 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Item Merchant 3", 30253 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Item Merchant 4", 40253 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Item Merchant 5", 50253 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Item Merchant 6", 60253 + shop_index_offset),

        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 1", 10133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 2", 20133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 3", 30133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 4", 40133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 5", 50133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 6", 60133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 7", 70133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 8", 80133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 9", 90133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 10", 100133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 11", 110133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 12", 120133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 13", 130133 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Armor Merchant 14", 140133 + shop_index_offset),

        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 1", 10117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 2", 20117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 3", 30117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 4", 40117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 5", 50117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 6", 60117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 7", 70117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 8", 80117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 9", 90117 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Weapon Merchant 10", 100117 + shop_index_offset),

        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Accessories Merchant 1", 10134 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Accessories Merchant 2", 20134 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Accessories Merchant 3", 30134 + shop_index_offset),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Shop - Accessories Merchant 4", 40134 + shop_index_offset),

        #Zones (Advanced)
        #Capital Sequoia
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "Gaea Shrine Shop - Attendant 1", 10379 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, "Gaea Shrine Shop - Attendant 2", 20379 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Candy Merchant 1", 10575 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Candy Merchant 2", 20575 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 1", 11158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 2", 21158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 3", 31158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 4", 41158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 5", 51158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 6", 61158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 7", 71158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 8", 81158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 9", 91158 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Map Seller 10", 101158 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Martial Weapons 1", 10599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Martial Weapons 2", 20599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Martial Weapons 3", 30599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Martial Weapons 4", 40599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Martial Weapons 1", 50599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Martial Weapons 2", 60599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Martial Weapons 3", 70599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Martial Weapons 4", 80599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Martial Weapons 5", 90599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Martial Weapons 6", 100599 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Exotic Weapons 1", 10600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Exotic Weapons 2", 20600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Exotic Weapons 3", 30600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Exotic Weapons 4", 40600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Exotic Weapons 1", 50600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Exotic Weapons 2", 60600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Exotic Weapons 3", 70600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Exotic Weapons 4", 80600 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Heavy Armor 1", 10601 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Heavy Armor 2", 20601 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Heavy Armor 3", 30601 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Heavy Armor 1", 40601 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Heavy Armor 2", 50601 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Heavy Armor 3", 60601 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Medium Armor 1", 10602 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Medium Armor 2", 20602 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Medium Armor 1", 30602 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Medium Armor 2", 40602 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Magic Weapons 1", 10603 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Magic Weapons 2", 20603 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Magic Weapons 3", 30603 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Magic Weapons 1", 40603 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Magic Weapons 2", 50603 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Magic Weapons 3", 60603 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Light Armor 1", 10604 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Luxury Shop Light Armor 2", 20604 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Light Armor 1", 30604 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Upgraded Luxury Shop Light Armor 2", 40604 + shop_index_offset, lambda state: state.has(PROGRESSIVE_LUXURY_PASS, player, 2)),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 1", 10500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 2", 20500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 3", 30500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 4", 40500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 5", 50500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 6", 60500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 7", 70500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 8", 80500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 9", 90500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 10", 100500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 11", 110500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 12", 120500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 13", 130500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 14", 140500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 15", 150500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 16", 160500 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Martial Weapons R Us 17", 170500 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Exotic Weapons R Us 1", 10501 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Exotic Weapons R Us 2", 20501 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Exotic Weapons R Us 3", 30501 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Exotic Weapons R Us 4", 40501 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Exotic Weapons R Us 5", 50501 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Exotic Weapons R Us 6", 60501 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Milk Man", 10579 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 1", 10416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 2", 20416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 3", 30416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 4", 40416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 5", 50416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 6", 60416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 7", 70416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 8", 80416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 9", 90416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 10", 100416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 11", 110416 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Heavy Armor 4 All 12", 120416 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 1", 10417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 2", 20417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 3", 30417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 4", 40417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 5", 50417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 6", 60417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 7", 70417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 8", 80417 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Medium Armor 4 All 9", 90417 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 1", 10455 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 2", 20455 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 3", 30455 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 4", 40455 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 5", 50455 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 6", 60455 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 7", 70455 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Light Armor 8", 80455 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 1", 10499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 2", 20499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 3", 30499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 4", 40499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 5", 50499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 6", 60499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 7", 70499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 8", 80499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 9", 90499 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Magic and Magic Things Weapons 10", 100499 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 1", 10398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 2", 20398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 3", 30398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 4", 40398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 5", 50398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 6", 60398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 7", 70398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 8", 80398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 9", 90398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 10", 100398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 11", 110398 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Accessory Merchant 12", 120398 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Item Merchant 1", 10456 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Item Merchant 2", 20456 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Item Merchant 3", 30456 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Item Merchant 4", 40456 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Item Merchant 5", 50456 + shop_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Item Merchant 6", 60456 + shop_index_offset),

        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Shop - Old Nans Stew", 10423 + shop_index_offset),

        #Salmon River
        #Poseidon Shrine Proper
        LocationData(POSEIDON_SHRINE_PROPER_AP_REGION, POSEIDON_SHRINE_PROPER_AP_REGION + " Shop - Attendant 1", 10631 + shop_index_offset),
        LocationData(POSEIDON_SHRINE_PROPER_AP_REGION, POSEIDON_SHRINE_PROPER_AP_REGION + " Shop - Attendant 2", 20631 + shop_index_offset),
        LocationData(POSEIDON_SHRINE_PROPER_AP_REGION, POSEIDON_SHRINE_PROPER_AP_REGION + " Shop - Attendant 3", 30631 + shop_index_offset),

        #Sara Sara Bazaar
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Old Nans Stew Subsidiary", 10957 + shop_index_offset),

        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Accessory Merchant 1", 11386 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Accessory Merchant 2", 21386 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Accessory Merchant 3", 31386 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Accessory Merchant 4", 41386 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Accessory Merchant 5", 51386 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Accessory Merchant 6", 61386 + shop_index_offset),

        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 1", 11193 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 2", 21193 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 3", 31193 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 4", 41193 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 5", 51193 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 6", 61193 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 7", 71193 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Item Merchant 8", 81193 + shop_index_offset),

        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Fish Merchant 1", 10942 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Fish Merchant 2", 20942 + shop_index_offset),

        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Armor Merchant 1", 11603 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Armor Merchant 2", 21603 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Armor Merchant 3", 31603 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Armor Merchant 4", 41603 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Armor Merchant 5", 51603 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Armor Merchant 6", 61603 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Armor Merchant 7", 71603 + shop_index_offset),

        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 1", 11604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 2", 21604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 3", 31604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 4", 41604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 5", 51604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 6", 61604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 7", 71604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 8", 81604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 9", 91604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 10", 101604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 11", 111604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 12", 121604 + shop_index_offset),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Shop - Weapon Merchant 13", 131604 + shop_index_offset),

        #Zones (Expert)
        #Shoudu Province
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 1", 10951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 2", 20951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 3", 30951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 4", 40951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 5", 50951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 6", 60951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 7", 70951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 8", 80951 + shop_index_offset),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Item Merchant 9", 90951 + shop_index_offset),

        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - No Shoudu Stew for you 1", 11199 + shop_index_offset),

        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Accessory Merchant 1", 11614 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Accessory Merchant 2", 21614 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Accessory Merchant 3", 31614 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Accessory Merchant 4", 41614 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Accessory Merchant 5", 51614 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Accessory Merchant 6", 61614 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),

        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 1", 11535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 2", 21535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 3", 31535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 4", 41535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 5", 51535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 6", 61535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 7", 71535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 8", 81535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 9", 91535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Armor Merchant 10", 101535 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),

        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 1", 11544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 2", 21544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 3", 31544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 4", 41544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 5", 51544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 6", 61544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 7", 71544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 8", 81544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 9", 91544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 10", 101544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 11", 111544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 12", 121544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 13", 131544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 14", 141544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 15", 151544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Shop - Weapon Merchant 16", 161544 + shop_index_offset, lambda state: logic.has_vertical_movement(state) or logic.has_glide(state)),

        #Ganymede Shrine
        LocationData(GANYMEDE_SHRINE_AP_REGION, GANYMEDE_SHRINE_DISPLAY_NAME + " Shop - Attendant 1", 11574 + shop_index_offset),
        LocationData(GANYMEDE_SHRINE_AP_REGION, GANYMEDE_SHRINE_DISPLAY_NAME + " Shop - Attendant 2", 21574 + shop_index_offset),
        LocationData(GANYMEDE_SHRINE_AP_REGION, GANYMEDE_SHRINE_DISPLAY_NAME + " Shop - Attendant 3", 31574 + shop_index_offset),

        #Quintar Reserve
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Shop - Babel to this Quintar 1", 10470 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Shop - Babel to this Quintar 2", 20470 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Shop - Babel to this Quintar 3", 30470 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Shop - Babel to this Quintar 4", 40470 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Shop - Babel to this Quintar 5", 50470 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),

        #Dione Shrine
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Attendant 1", 12253 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Attendant 2", 22253 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),

        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 1", 12227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 2", 22227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 3", 32227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 4", 42227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 5", 52227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 6", 62227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 7", 72227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 8", 82227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Shop - Quintar Raising Supplies 9", 92227 + shop_index_offset, lambda state: state.has(BABEL_QUINTAR, player)),

        #Tall Tall Heights
        LocationData(UPPER_ICE_LAKES_AP_REGION, "Triton Shrine Shop - Attendant 1", 11165 + shop_index_offset),
        LocationData(UPPER_ICE_LAKES_AP_REGION, "Triton Shrine Shop - Attendant 2", 21165 + shop_index_offset),

        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 1", 12746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 2", 22746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 3", 32746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 4", 42746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 5", 52746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 6", 62746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 7", 72746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 8", 82746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 9", 92746 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Armor Merchant 10", 102746 + shop_index_offset),

        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 1", 10540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 2", 20540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 3", 30540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 4", 40540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 5", 50540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 6", 60540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 7", 70540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 8", 80540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 9", 90540 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Weapon Merchant 10", 100540 + shop_index_offset),

        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Souvenir Merchant 1", 12918 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Souvenir Merchant 2", 22918 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Souvenir Merchant 3", 32918 + shop_index_offset),
        LocationData(SOUVENIR_SHOP_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Shop - Souvenir Merchant 4", 42918 + shop_index_offset),

        #Jidamba Tangle
        LocationData(EUROPA_SHRINE_AP_REGION, EUROPA_SHRINE_AP_REGION + " Shop - Attendant 1", 11163 + shop_index_offset),
        LocationData(EUROPA_SHRINE_AP_REGION, EUROPA_SHRINE_AP_REGION + " Shop - Attendant 2", 21163 + shop_index_offset),

        #Neptune Shrine
        LocationData(NEPTUNE_SHRINE_AP_REGION, NEPTUNE_SHRINE_DISPLAY_NAME + " Shop - Attendant 1", 13164 + shop_index_offset),
        LocationData(NEPTUNE_SHRINE_AP_REGION, NEPTUNE_SHRINE_DISPLAY_NAME + " Shop - Attendant 2", 23164 + shop_index_offset),
        LocationData(NEPTUNE_SHRINE_AP_REGION, NEPTUNE_SHRINE_DISPLAY_NAME + " Shop - Attendant 3", 33164 + shop_index_offset),

        #Zones (End-Game)
        #The New World
        LocationData(THE_NEW_WORLD_AP_REGION, THE_NEW_WORLD_DISPLAY_NAME + " Shrine Shop - Attendant 1", 11877 + shop_index_offset),
        LocationData(THE_NEW_WORLD_AP_REGION, THE_NEW_WORLD_DISPLAY_NAME + " Shrine Shop - Attendant 2", 21877 + shop_index_offset),
    ]
    return location_table

def get_region_completions(player: int, options: CrystalProjectOptions) -> List[LocationData]:
    logic = CrystalProjectLogic(player, options)
    location_table: List[LocationData] = [
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " Region Completion", 6001 + regionsanity_index_offset, regionsanity=True),
        LocationData(DELENDE_AP_REGION, DELENDE_DISPLAY_NAME + " Region Completion", 6002 + regionsanity_index_offset, regionsanity=True),
        LocationData(MERCURY_SHRINE_AP_REGION, MERCURY_SHRINE_DISPLAY_NAME + " Region Completion", 6007 + regionsanity_index_offset, regionsanity=True),
        LocationData(SOILED_DENLENDE_AP_REGION, SOILED_DEN_DISPLAY_NAME + " Region Completion", 6003 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_PALE_GROTTO_AP_REGION, THE_PALE_GROTTO_DISPLAY_NAME + " Region Completion", 6004 + regionsanity_index_offset, regionsanity=True),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " Region Completion", 6005 + regionsanity_index_offset, regionsanity=True),
        LocationData(DRAFT_SHAFT_CONDUIT_AP_REGION, DRAFT_SHAFT_CONDUIT_DISPLAY_NAME + " Region Completion", 6006 + regionsanity_index_offset, regionsanity=True),
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " Region Completion", 6008 + regionsanity_index_offset, regionsanity=True),
        LocationData(PROVING_MEADOWS_AP_REGION, PROVING_MEADOWS_DISPLAY_NAME + " Region Completion", 6009 + regionsanity_index_offset, regionsanity=True),
        LocationData(SKUMPARADISE_AP_REGION, SKUMPARADISE_DISPLAY_NAME + " Region Completion", 6010 + regionsanity_index_offset, regionsanity=True),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " Region Completion", 6011 + regionsanity_index_offset, regionsanity=True),
        LocationData(JOJO_SEWERS_AP_REGION, JOJO_SEWERS_DISPLAY_NAME + " Region Completion", 6012 + regionsanity_index_offset, regionsanity=True),
        LocationData(BOOMER_SOCIETY_AP_REGION, BOOMER_SOCIETY_DISPLAY_NAME + " Region Completion", 6013 + regionsanity_index_offset, regionsanity=True),
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " Region Completion", 6014 + regionsanity_index_offset, regionsanity=True),
        LocationData(QUINTAR_NEST_AP_REGION, QUINTAR_NEST_DISPLAY_NAME + " Region Completion", 6015 + regionsanity_index_offset, regionsanity=True),
        LocationData(QUINTAR_SANCTUM_AP_REGION, QUINTAR_SANCTUM_DISPLAY_NAME + " Region Completion", 6016 + regionsanity_index_offset, regionsanity=True),
        LocationData(CAPITAL_JAIL_AP_REGION, CAPITAL_JAIL_DISPLAY_NAME + " Region Completion", 6017 + regionsanity_index_offset, regionsanity=True),
        LocationData(PIPELINE_SOUTH_AP_REGION, CAPITAL_PIPELINE_DISPLAY_NAME + " Region Completion", 6018 + regionsanity_index_offset, regionsanity=True),
        LocationData(COBBLESTONE_CRAG_AP_REGION, COBBLESTONE_CRAG_DISPLAY_NAME + " Region Completion", 6019 + regionsanity_index_offset, regionsanity=True),
        LocationData(OKIMOTO_NS_AP_REGION, OKIMOTO_NS_DISPLAY_NAME + " Region Completion", 6020 + regionsanity_index_offset, regionsanity=True),
        LocationData(GREENSHIRE_REPRISE_AP_REGION, GREENSHIRE_REPRISE_DISPLAY_NAME + " Region Completion", 6021 + regionsanity_index_offset, regionsanity=True),
        LocationData(SALMON_PASS_EAST_AP_REGION, SALMON_PASS_DISPLAY_NAME + " Region Completion", 6022 + regionsanity_index_offset, regionsanity=True),
        LocationData(SALMON_RIVER_AP_REGION, SALMON_RIVER_DISPLAY_NAME + " Region Completion", 6023 + regionsanity_index_offset, regionsanity=True),
        LocationData(POKO_POKO_DESERT_AP_REGION, POKO_POKO_DESERT_DISPLAY_NAME + " Region Completion", 6024 + regionsanity_index_offset, regionsanity=True),
        LocationData(SARA_SARA_BAZAAR_AP_REGION, SARA_SARA_BAZAAR_DISPLAY_NAME + " Region Completion", 6025 + regionsanity_index_offset, regionsanity=True),
        LocationData(SARA_SARA_BEACH_EAST_AP_REGION, SARA_SARA_BEACH_EAST_DISPLAY_NAME + " Region Completion", 6026 + regionsanity_index_offset, regionsanity=True),
        LocationData(SARA_SARA_BEACH_WEST_AP_REGION, SARA_SARA_BEACH_WEST_DISPLAY_NAME + " Region Completion", 6027 + regionsanity_index_offset, regionsanity=True),
        LocationData(ANCIENT_RESERVOIR_AP_REGION, ANCIENT_RESERVOIR_DISPLAY_NAME + " Region Completion", 6028 + regionsanity_index_offset, regionsanity=True),
        LocationData(SALMON_BAY_AP_REGION, SALMON_BAY_DISPLAY_NAME + " Region Completion", 6030 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_OPEN_SEA_AP_REGION, THE_OPEN_SEA_DISPLAY_NAME + " Region Completion", 6031 + regionsanity_index_offset, regionsanity=True),
        LocationData(SHOUDU_WATERFRONT_AP_REGION, SHOUDU_WATERFRONT_DISPLAY_NAME + " Region Completion", 6032 + regionsanity_index_offset, regionsanity=True),
        LocationData(SHOUDU_PROVINCE_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " Region Completion", 6033 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_UNDERCITY_AP_REGION, THE_UNDERCITY_DISPLAY_NAME + " Region Completion", 6034 + regionsanity_index_offset, regionsanity=True),
        LocationData(GANYMEDE_SHRINE_AP_REGION, GANYMEDE_SHRINE_DISPLAY_NAME + " Region Completion", 6035 + regionsanity_index_offset, regionsanity=True),
        LocationData(BEAURIOR_VOLCANO_AP_REGION, BEAURIOR_VOLCANO_DISPLAY_NAME + " Region Completion", 6036 + regionsanity_index_offset, regionsanity=True),
        LocationData(BEAURIOR_ROCK_AP_REGION, BEAURIOR_ROCK_DISPLAY_NAME + " Region Completion", 6037 + regionsanity_index_offset, regionsanity=True),
        LocationData(LAKE_DELENDE_AP_REGION, LAKE_DELENDE_DISPLAY_NAME + " Region Completion", 6038 + regionsanity_index_offset, regionsanity=True),
        LocationData(QUINTAR_RESERVE_AP_REGION, QUINTAR_RESERVE_DISPLAY_NAME + " Region Completion", 6039 + regionsanity_index_offset, regionsanity=True),
        LocationData(DIONE_SHRINE_AP_REGION, DIONE_SHRINE_DISPLAY_NAME + " Region Completion", 6040 + regionsanity_index_offset, regionsanity=True),
        LocationData(QUINTAR_MAUSOLEUM_AP_REGION, QUINTAR_MAUSOLEUM_DISPLAY_NAME + " Region Completion", 6041 + regionsanity_index_offset, regionsanity=True),
        LocationData(EASTERN_CHASM_AP_REGION, EASTERN_CHASM_DISPLAY_NAME + " Region Completion", 6042 + regionsanity_index_offset, regionsanity=True),
        LocationData(LOWER_ICE_LAKES_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " Region Completion", 6043 + regionsanity_index_offset, regionsanity=True),
        LocationData(UPPER_NORTHERN_CAVE_AP_REGION, NORTHERN_CAVE_DISPLAY_NAME + " Region Completion", 6044 + regionsanity_index_offset, regionsanity=True),
        LocationData(LANDS_END_AP_REGION, LANDS_END_DISPLAY_NAME + " Region Completion", 6045 + regionsanity_index_offset, regionsanity=True),
        LocationData(SLIP_GLIDE_RIDE_ENTRANCE_AP_REGION, SLIP_GLIDE_RIDE_DISPLAY_NAME + " Region Completion", 6046 + regionsanity_index_offset, regionsanity=True),
        LocationData(SEQUOIA_ATHENAEUM_AP_REGION, SEQUOIA_ATHENAEUM_DISPLAY_NAME + " Region Completion", 6047 + regionsanity_index_offset, regionsanity=True),
        LocationData(NORTHERN_STRETCH_RACE_START_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " Region Completion", 6048 + regionsanity_index_offset, regionsanity=True),
        LocationData(PEAK_RAMPARTS_AP_REGION, CASTLE_RAMPARTS_DISPLAY_NAME + " Region Completion", 6049 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_CHALICE_OF_TAR_AP_REGION, THE_CHALICE_OF_TAR_DISPLAY_NAME + " Region Completion", 6050 + regionsanity_index_offset, regionsanity=True),
        LocationData(FLYERS_CRAG_AP_REGION, FLYERS_CRAG_DISPLAY_NAME + " Region Completion", 6051 + regionsanity_index_offset, regionsanity=True),
        LocationData(EUROPA_SHRINE_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " Region Completion", 6052 + regionsanity_index_offset, regionsanity=True),
        LocationData(JIDAMBA_EACLANEYA_AP_REGION, JIDAMBA_EACLANEYA_DISPLAY_NAME + " Region Completion", 6053 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_DEEP_SEA_AP_REGION, THE_DEEP_SEA_DISPLAY_NAME + " Region Completion", 6054 + regionsanity_index_offset, regionsanity=True),
        LocationData(NEPTUNE_SHRINE_AP_REGION, NEPTUNE_SHRINE_DISPLAY_NAME + " Region Completion", 6055 + regionsanity_index_offset, regionsanity=True),
        LocationData(JADE_CAVERN_AP_REGION, JADE_CAVERN_DISPLAY_NAME + " Region Completion", 6056 + regionsanity_index_offset, regionsanity=True),
        LocationData(CONTINENTAL_TRAM_AP_REGION, CONTINENTAL_TRAM_DISPLAY_NAME + " Region Completion", 6057 + regionsanity_index_offset, regionsanity=True),
        LocationData(ANCIENT_LABYRINTH_AP_REGION, ANCIENT_LABYRINTH_DISPLAY_NAME + " Region Completion", 6058 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_SEQUOIA_AP_REGION, THE_SEQUOIA_DISPLAY_NAME + " Region Completion", 6059 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_DEPTHS_AP_REGION, THE_DEPTHS_DISPLAY_NAME + " Region Completion", 6060 + regionsanity_index_offset, regionsanity=True),
        LocationData(CASTLE_SEQUOIA_AP_REGION, CASTLE_SEQUOIA_DISPLAY_NAME + " Region Completion", 6061 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_NEW_WORLD_AP_REGION, THE_NEW_WORLD_DISPLAY_NAME + " Region Completion", 6063 + regionsanity_index_offset, regionsanity=True),
        LocationData(THE_OLD_WORLD_AP_REGION, THE_OLD_WORLD_DISPLAY_NAME + " Region Completion", 6064 + regionsanity_index_offset, regionsanity=True),
    ]
    return location_table