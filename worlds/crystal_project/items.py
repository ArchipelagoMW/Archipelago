import logging
from typing import Dict, Set, Tuple, NamedTuple, Optional, List, TYPE_CHECKING
from BaseClasses import ItemClassification
from .constants.item_groups import *
from .constants.jobs import *
from .constants.keys import *
from .constants.key_items import *
from .constants.maps import *
from .constants.mounts import *
from .constants.scholar_abilities import *
from .constants.summons import *
from .constants.teleport_stones import *
from .constants.region_passes import *
from .constants.display_regions import *
from .constants.crystal_locations import *

if TYPE_CHECKING:
    from . import CrystalProjectWorld

class ItemData(NamedTuple):
    category: str
    code: int
    classification: ItemClassification
        #For maguffins, we use Progression + Deprioritize + SkipBalancing
        #For progression items that you need a lot to unlock not much, and are therefore unsatisfying, we use Progression + Deprioritize
        #For really neat progression items that are a BIG DEAL, we use Progression + Useful, just because that comes out a gold color instead of purple when colored text is used.
        # deprioritize means it won't be picked for a priority location, because it would feel unsatisfying to get i.e. clam from a priority location
        # skip balancing means that if you used progression balancing to try to force one player's items earlier than another, it will fill those with i.e. non-clams
    #Amount found in each region type; added together for each set you're including
    beginnerAmount: Optional[int] = 1
    advancedAmount: Optional[int] = 0
    expertAmount: Optional[int] = 0
    endGameAmount: Optional[int] = 0
    # Amount found in each region type's shops; added together for each set you're including
    beginnerShops: Optional[int] = 0
    advancedShops: Optional[int] = 0
    expertShops: Optional[int] = 0
    endGameShops: Optional[int] = 0

class Job(NamedTuple):
    name: str
    id: int

#Archipelago does not like it if an item has a code of 0, Crystal project starts its database
#Ids at 0, so we add an offset to the id of each item and remove that offset in the client
job_index_offset = 1
item_index_offset = 101
equipment_index_offset = 1001
summon_index_offset = 10001
scholar_index_offset = 100001
trap_index_offset = 1000001
home_point_item_index_offset = 10000001

item_table: Dict[str, ItemData] = {
    #Jobs
    WARRIOR_JOB: ItemData(JOB, 0 + job_index_offset, ItemClassification.progression),
    MONK_JOB: ItemData(JOB, 5 + job_index_offset, ItemClassification.progression),
    ROGUE_JOB: ItemData(JOB, 2 + job_index_offset, ItemClassification.progression),
    CLERIC_JOB: ItemData(JOB, 4 + job_index_offset, ItemClassification.progression),
    WIZARD_JOB: ItemData(JOB, 3 + job_index_offset, ItemClassification.progression),
    WARLOCK_JOB: ItemData(JOB, 14 + job_index_offset, ItemClassification.progression),
    FENCER_JOB: ItemData(JOB, 1 + job_index_offset, ItemClassification.progression),
    SHAMAN_JOB: ItemData(JOB, 8 + job_index_offset, ItemClassification.progression),
    SCHOLAR_JOB: ItemData(JOB, 13 + job_index_offset, ItemClassification.progression), #requirement for Grans subbasement
    AEGIS_JOB: ItemData(JOB, 10 + job_index_offset, ItemClassification.progression),
    HUNTER_JOB: ItemData(JOB, 7 + job_index_offset, ItemClassification.progression),
    CHEMIST_JOB: ItemData(JOB, 17 + job_index_offset, ItemClassification.progression),
    REAPER_JOB: ItemData(JOB, 6 + job_index_offset, ItemClassification.progression),
    NINJA_JOB: ItemData(JOB, 18 + job_index_offset, ItemClassification.progression),
    NOMAD_JOB: ItemData(JOB, 12 + job_index_offset, ItemClassification.progression),
    DERVISH_JOB: ItemData(JOB, 11 + job_index_offset, ItemClassification.progression),
    BEATSMITH_JOB: ItemData(JOB, 9 + job_index_offset, ItemClassification.progression),
    SAMURAI_JOB: ItemData(JOB, 20 + job_index_offset, ItemClassification.progression),
    ASSASSIN_JOB: ItemData(JOB, 19 + job_index_offset, ItemClassification.progression),
    VALKYRIE_JOB: ItemData(JOB, 15 + job_index_offset, ItemClassification.progression),
    SUMMONER_JOB: ItemData(JOB, 21 + job_index_offset, ItemClassification.progression), #Required for summon fights; only job checked by NPCs
    BEASTMASTER_JOB: ItemData(JOB, 23 + job_index_offset, ItemClassification.progression),
    WEAVER_JOB: ItemData(JOB, 16 + job_index_offset, ItemClassification.progression),
    MIMIC_JOB: ItemData(JOB, 22 + job_index_offset, ItemClassification.progression),

    #Consumables
    "Item - Tonic": ItemData(ITEM, 18 + item_index_offset, ItemClassification.filler, 0),
    "Item - Potion": ItemData(ITEM, 0 + item_index_offset, ItemClassification.filler, 0),
    "Item - Z-Potion": ItemData(ITEM, 102 + item_index_offset, ItemClassification.filler, 0),
    "Item - Tincture": ItemData(ITEM, 47 + item_index_offset, ItemClassification.filler, 0),
    "Item - Ether": ItemData(ITEM, 1 + item_index_offset, ItemClassification.filler, 0),
    "Item - Zether": ItemData(ITEM, 142 + item_index_offset, ItemClassification.filler, 0),
    "Item - Fenix Juice": ItemData(ITEM, 2 + item_index_offset, ItemClassification.filler, 0),
    "Item - Fenix Syrup": ItemData(ITEM, 145 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nans Stew": ItemData(ITEM, 9 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nans Cocoa": ItemData(ITEM, 8 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nans Secret Recipe": ItemData(ITEM, 54 + item_index_offset, ItemClassification.filler, 0),
    "Item - Nuts": ItemData(ITEM, 14 + item_index_offset, ItemClassification.filler, 0),
    "Item - Milk": ItemData(ITEM, 20 + item_index_offset, ItemClassification.filler, 0), #Turn-in: Thirsty Lad, Poko Poko Desert, Advanced Regions
    "Item - Shoudu Stew": ItemData(ITEM, 132 + item_index_offset, ItemClassification.filler, 0), #Turn-in: Foreign Foodie, Sara Sara Bazaar, Advanced Regions
    "Item - Sweet Pop Candy": ItemData(ITEM, 34 + item_index_offset, ItemClassification.filler, 0),
    "Item - Sour Pop Candy": ItemData(ITEM, 35 + item_index_offset, ItemClassification.filler, 0),
    "Item - Bitter Pop Candy": ItemData(ITEM, 171 + item_index_offset, ItemClassification.filler, 0),
    "Item - Rotten Salmon": ItemData(ITEM, 11 + item_index_offset, ItemClassification.filler, 0), #Turn-in: Fish Merchant, Sara Sara Bazaar, Advanced Regions
    "Item - Decent Cod": ItemData(ITEM, 38 + item_index_offset, ItemClassification.filler, 0),
    "Item - Fresh Salmon": ItemData(ITEM, 10 + item_index_offset, ItemClassification.filler, 0), #Turn-in: Fish Merchant, Sara Sara Bazaar, Advanced Regions
    "Item - Scroll": ItemData(ITEM, 263 + item_index_offset, ItemClassification.filler, 0),

    #Bag upgrades
    "Item - Tonic Pouch": ItemData(ITEM, 133 + item_index_offset, ItemClassification.useful, 7, 9, 1, 0), #17
    "Item - Potion Pouch": ItemData(ITEM, 134 + item_index_offset, ItemClassification.useful, 0, 5, 8, 0), #13
    "Item - Z-Potion Pouch": ItemData(ITEM, 143 + item_index_offset, ItemClassification.useful, 1, 0, 2, 1), #5
    "Item - Tincture Pouch": ItemData(ITEM, 135 + item_index_offset, ItemClassification.useful, 4, 8, 2, 0), #14
    "Item - Ether Pouch": ItemData(ITEM, 136 + item_index_offset, ItemClassification.useful, 0, 6, 5, 0), #11
    "Item - Zether Pouch": ItemData(ITEM, 144 + item_index_offset, ItemClassification.useful, 0, 1, 1, 3), #5
    "Item - Fenix Juice Pouch": ItemData(ITEM, 137 + item_index_offset, ItemClassification.useful, 1, 1, 0, 0), #2
    "Item - Fenix Syrup Pouch": ItemData(ITEM, 146 + item_index_offset, ItemClassification.useful, 0, 2, 0, 0), #2
    "Item - Nuts Sack": ItemData(ITEM, 184 + item_index_offset, ItemClassification.useful, 0, 1), #Capital Sequoia, Advanced Zones
    "Item - Milk Bag": ItemData(ITEM, 138 + item_index_offset, ItemClassification.useful, 0, 1), #Poko Poko Desert, Advanced Zones
    "Item - Decent Cod Bag": ItemData(ITEM, 185 + item_index_offset, ItemClassification.useful, 0, 0, 1), #Shoudu Province, Expert Zones

    #Fishing
    "Item - Flimsy Rod": ItemData(TACKLE, 55 + item_index_offset, ItemClassification.progression, 1),
    "Item - Tough Rod": ItemData(TACKLE, 150 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    "Item - Super Rod": ItemData(TACKLE, 151 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    "Item - Plug Lure": ItemData(TACKLE, 91 + item_index_offset, ItemClassification.progression, 1),
    "Item - Fly Lure": ItemData(TACKLE, 149 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    "Item - Jigging Lure": ItemData(TACKLE, 97 + item_index_offset, ItemClassification.progression, 0, 0, 1),

    #Ore
    "Item - Silver Ore": ItemData(ORE, 3 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Capital Blacksmith, Capital Sequoia, Advanced Regions
    "Item - Silver Ingot": ItemData(ORE, 67 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Capital Blacksmith, Capital Sequoia, Advanced Regions
    "Item - Silver Dust": ItemData(ORE, 68 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Capital Blacksmith, Capital Sequoia, Advanced Regions
    "Item - Gold Ore": ItemData(ORE, 4 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Armorer in Sara Sara Bazaar and Weaponsmith in Shoudu Province, Advanced Regions
    "Item - Gold Ingot": ItemData(ORE, 69 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Armorer in Sara Sara Bazaar and Weaponsmith in Shoudu Province, Advanced Regions
    "Item - Gold Dust": ItemData(ORE, 70 + item_index_offset, ItemClassification.useful, 0, 18), #Used by Armorer in Sara Sara Bazaar and Weaponsmith in Shoudu Province, Advanced Regions
    "Item - Diamond Ore": ItemData(ORE, 5 + item_index_offset, ItemClassification.useful, 0, 0, 18), #Used by Armorer in Tall Tall Heights and Weaponsmith in Jidamba Tangle, Expert Regions
    "Item - Diamond Ingot": ItemData(ORE, 71 + item_index_offset, ItemClassification.useful, 0, 0, 18), #Used by Armorer in Tall Tall Heights and Weaponsmith in Jidamba Tangle, Expert Regions
    "Item - Diamond Dust": ItemData(ORE, 72 + item_index_offset, ItemClassification.useful, 0, 0, 18), #Used by Armorer in Tall Tall Heights and Weaponsmith in Jidamba Tangle, Expert Regions

    #Keys
    GARDENERS_KEY: ItemData(KEY, 31 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Sequoia, Advanced Regions
    COURTYARD_KEY: ItemData(KEY, 33 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Sequoia (Courtyard), Advanced Regions
    LUXURY_KEY: ItemData(KEY, 36 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Sequoia, Advanced Regions
    CELL_KEY: ItemData(KEY, 40 + item_index_offset, ItemClassification.progression, 0, 7), #Turn-in: Capital Jail, Advanced Regions
    SOUTH_WING_KEY: ItemData(KEY, 41 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    EAST_WING_KEY: ItemData(KEY, 42 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    WEST_WING_KEY: ItemData(KEY, 43 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    DARK_WING_KEY: ItemData(KEY, 44 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Capital Jail, Advanced Regions
    ROOM_ONE_KEY: ItemData(KEY, 32 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    PYRAMID_KEY: ItemData(KEY, 60 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Poko Poko Desert (unlocks Ancient Reservoir), Advanced Regions
    TRAM_KEY: ItemData(KEY, 95 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Continental Tram (unlocks connection between Continental Tram and Sara Sara Bazaar), Expert Regions
    SMALL_KEY: ItemData(KEY, 29 + item_index_offset, ItemClassification.progression, 0, 0, 4), #Turn-in: Beaurior Rock, Expert Regions
    BEAURIOR_BOSS_KEY: ItemData(KEY, 30 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Beaurior Rock, Expert Regions
    ICE_CELL_KEY: ItemData(KEY, 156 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Northern Cave, Expert Regions
    RED_DOOR_KEY: ItemData(KEY, 169 + item_index_offset, ItemClassification.progression, 0, 0, 3), #Turn-in: Slip Glide Ride, Expert Regions
    ICE_PUZZLE_KEY: ItemData(KEY, 160 + item_index_offset, ItemClassification.progression, 0, 0, 6), #Turn-in: Sequoia Athenaeum, Expert Regions
    FOLIAGE_KEY: ItemData(KEY, 141 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Jidamba Tangle (unlocks Jidamba Eaclaneya), Expert Regions
    CAVE_KEY: ItemData(KEY, 118 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Jidamba Tangle (unlocks Jidamba Eaclaneya), Expert Regions
    CANOPY_KEY: ItemData(KEY, 116 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Jidamba Tangle (unlocks Jidamba Eaclaneya), Expert Regions
    RAMPART_KEY: ItemData(KEY, 175 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Castle Ramparts, Expert Regions
    FORGOTTEN_KEY: ItemData(KEY, 192 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: The Deep Sea, Expert Regions
    SKELETON_KEY: ItemData(KEY, 147 + item_index_offset, ItemClassification.progression | ItemClassification.useful, 0, 1), #Everyone's best friend
    PRISON_KEY_RING: ItemData(KEY, 650 + item_index_offset, ItemClassification.progression, 0, 1),
    BEAURIOR_KEY_RING: ItemData(KEY, 651 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    ICE_PUZZLE_KEY_RING: ItemData(KEY, 652 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    SLIP_GLIDE_RIDE_KEY_RING: ItemData(KEY, 653 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    JIDAMBA_KEY_RING: ItemData(KEY, 654 + item_index_offset, ItemClassification.progression, 0, 0, 1),

    #Passes
    "Item - Quintar Pass": ItemData(ITEM, 7 + item_index_offset, ItemClassification.filler, 0), #We don't use this so it's filler to prevent it from being jsonified (now part of Progressive Quintar Flute)
    PROGRESSIVE_LUXURY_PASS: ItemData(ITEM, 93 + item_index_offset, ItemClassification.progression, 0, 2), #Luxury Pass ID 93; Luxury Pass V2 148; Turn-in: Capital Sequoia, Advanced Regions
    "Item - Luxury Pass V2": ItemData(ITEM, 148 + item_index_offset, ItemClassification.filler, 0), #We don't use this so it's filler to prevent it from being jsonified (now part of Progressive Luxury Pass)
    FERRY_PASS: ItemData(ITEM, 37 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Sara Sara Bazaar (unlocks connection to Shoudu Province), Expert Regions

    #Key Items
    BLACK_SQUIRREL: ItemData(ITEM, 21 + item_index_offset, ItemClassification.progression, 4), #Turn-in: Spawning Meadows, Beginner Regions
    DOG_BONE: ItemData(ITEM, 6 + item_index_offset, ItemClassification.progression, 3), #Turn-in: Delende, Beginner Regions
    # Number of clamshells is set dynamically based on your Clamshells in pool variable
    CLAMSHELL: ItemData(ITEM, 16 + item_index_offset, ItemClassification.progression | ItemClassification.deprioritized | ItemClassification.skip_balancing, 0), #Turn-in: Seaside Cliffs, Beginner Regions
    DIGESTED_HEAD: ItemData(ITEM, 17 + item_index_offset, ItemClassification.progression, 0, 3), #Turn-in: Capital Sequoia, Advanced Regions
    LOST_PENGUIN: ItemData(ITEM, 24 + item_index_offset, ItemClassification.progression, 0, 12), #Turn-in: Capital Sequoia, Advanced Regions
    ELEVATOR_PART: ItemData(ITEM, 224 + item_index_offset, ItemClassification.progression | ItemClassification.deprioritized, 0, 0, 10), #Turn-in: Shoudu Province, Expert Regions
    UNDERSEA_CRAB: ItemData(ITEM, 212 + item_index_offset, ItemClassification.progression | ItemClassification.deprioritized, 0, 0, 15), #Turn-in: The Deep Sea, Expert Regions
    WEST_LOOKOUT_TOKEN: ItemData(ITEM, 81 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    CENTRAL_LOOKOUT_TOKEN: ItemData(ITEM, 88 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    NORTH_LOOKOUT_TOKEN: ItemData(ITEM, 131 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Sara Sara Bazaar, Advanced Regions
    BABEL_QUINTAR: ItemData(ITEM, 167 + item_index_offset, ItemClassification.progression), #Quintar shop!
    "Item - Quintar Shedding": ItemData(ITEM, 168 + item_index_offset, ItemClassification.filler, 0), #12
    CRAG_DEMON_HORN: ItemData(ITEM, 197 + item_index_offset, ItemClassification.progression, 0, 1), #Turn-in: Jojo Sewers, Advanced Regions
    VERMILLION_BOOK: ItemData(ITEM, 172 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Tall Tall Heights (unlocks Sequoia Athenaeum), Expert Regions
    VIRIDIAN_BOOK: ItemData(ITEM, 173 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Tall Tall Heights (Sequoia Athenaeum), Expert Regions
    CERULEAN_BOOK: ItemData(ITEM, 174 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Turn-in: Tall Tall Heights (Sequoia Athenaeum), Expert Regions
    ANCIENT_TABLET_A: ItemData(ITEM, 161 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    ANCIENT_TABLET_B: ItemData(ITEM, 162 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    ANCIENT_TABLET_C: ItemData(ITEM, 163 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    TREASURE_FINDER: ItemData(ITEM, 196 + item_index_offset, ItemClassification.useful),
    # Progressive Level is used for all level gating options: Progressive Level Pass, Progressive Level Cap, and Progressive Level Catch-Up
    PROGRESSIVE_LEVEL: ItemData(ITEM, 500 + item_index_offset, ItemClassification.progression, 0),
    PASSIVE_POINT_BOOST: ItemData(ITEM, 799 + item_index_offset, ItemClassification.useful, 0),
    HOMEPOINT_UNLOCK: ItemData(ITEM, 800 + item_index_offset, ItemClassification.filler, 0),
    SPECIAL_SHOUDU_STEW: ItemData(ITEM, 229 + item_index_offset, ItemClassification.progression, 0, 1),
    SPECIAL_MILK: ItemData(ITEM, 230 + item_index_offset, ItemClassification.progression, 0, 1),
    SPECIAL_FRESH_SALMON: ItemData(ITEM, 231 + item_index_offset, ItemClassification.progression, 0, 1),
    SPECIAL_ROTTEN_SALMON: ItemData(ITEM, 232 + item_index_offset, ItemClassification.progression, 0, 1),
    DEITY_EYE: ItemData(ITEM, 176 + item_index_offset, ItemClassification.progression, 0, 0, 0, 4), #Used for true astley win con and fighting Gabriel in Kill Bosses mode
    STEM_WARD: ItemData(ITEM, 177 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1), #Used for true astley win con and fighting Gabriel in Kill Bosses mode
    PROOF_OF_MERIT: ItemData(ITEM, 191 + item_index_offset, ItemClassification.filler, 0), #We don't use this so it's filler to prevent it from being jsonified

    #Passes for Regionsanity
    SPAWNING_MEADOWS_PASS: ItemData(PASS, 801 + item_index_offset, ItemClassification.progression, 1),
    DELENDE_PASS: ItemData(PASS, 802 + item_index_offset, ItemClassification.progression, 1),
    SOILED_DEN_PASS: ItemData(PASS, 803 + item_index_offset, ItemClassification.progression, 1),
    THE_PALE_GROTTO_PASS: ItemData(PASS, 804 + item_index_offset, ItemClassification.progression, 1),
    SEASIDE_CLIFFS_PASS: ItemData(PASS, 805 + item_index_offset, ItemClassification.progression, 1),
    DRAFT_SHAFT_CONDUIT_PASS: ItemData(PASS, 806 + item_index_offset, ItemClassification.progression, 1),
    MERCURY_SHRINE_PASS: ItemData(PASS, 807 + item_index_offset, ItemClassification.progression, 1),
    YAMAGAWA_MA_PASS: ItemData(PASS, 808 + item_index_offset, ItemClassification.progression, 1),
    PROVING_MEADOWS_PASS: ItemData(PASS, 809 + item_index_offset, ItemClassification.progression, 1),
    SKUMPARADISE_PASS: ItemData(PASS, 810 + item_index_offset, ItemClassification.progression, 1),
    #Advanced
    CAPITAL_SEQUOIA_PASS: ItemData(PASS, 811 + item_index_offset, ItemClassification.progression, 0, 1),
    JOJO_SEWERS_PASS: ItemData(PASS, 812 + item_index_offset, ItemClassification.progression, 0, 1),
    BOOMER_SOCIETY_PASS: ItemData(PASS, 813 + item_index_offset, ItemClassification.progression, 0, 1),
    ROLLING_QUINTAR_FIELDS_PASS: ItemData(PASS, 814 + item_index_offset, ItemClassification.progression, 0, 1),
    QUINTAR_NEST_PASS: ItemData(PASS, 815 + item_index_offset, ItemClassification.progression, 0, 1),
    QUINTAR_SANCTUM_PASS: ItemData(PASS, 816 + item_index_offset, ItemClassification.progression, 0, 1),
    CAPITAL_JAIL_PASS: ItemData(PASS, 817 + item_index_offset, ItemClassification.progression, 0, 1),
    CAPITAL_PIPELINE_PASS: ItemData(PASS, 818 + item_index_offset, ItemClassification.progression, 0, 1),
    COBBLESTONE_CRAG_PASS: ItemData(PASS, 819 + item_index_offset, ItemClassification.progression, 0, 1),
    OKIMOTO_NS_PASS: ItemData(PASS, 820 + item_index_offset, ItemClassification.progression, 0, 1),
    GREENSHIRE_REPRISE_PASS: ItemData(PASS, 821 + item_index_offset, ItemClassification.progression, 0, 1),
    SALMON_PASS_PASS: ItemData(PASS, 822 + item_index_offset, ItemClassification.progression, 0, 1),
    SALMON_RIVER_PASS: ItemData(PASS, 823 + item_index_offset, ItemClassification.progression, 0, 1),
    SHOUDU_WATERFRONT_PASS: ItemData(PASS, 824 + item_index_offset, ItemClassification.progression, 0, 1),
    POKO_POKO_DESERT_PASS: ItemData(PASS, 825 + item_index_offset, ItemClassification.progression, 0, 1),
    SARA_SARA_BAZAAR_PASS: ItemData(PASS, 826 + item_index_offset, ItemClassification.progression, 0, 1),
    SARA_SARA_BEACH_PASS: ItemData(PASS, 827 + item_index_offset, ItemClassification.progression, 0, 1),
    #SARA_SARA_BEACH_WEST_PASS: ItemData(PASS, 828 + item_index_offset, ItemClassification.progression, 0, 1),
    ANCIENT_RESERVOIR_PASS: ItemData(PASS, 829 + item_index_offset, ItemClassification.progression, 0, 1),
    #IBEK_CAVE_PASS: ItemData(PASS, 830 + item_index_offset, ItemClassification.progression, 0, 1),
    SALMON_BAY_PASS: ItemData(PASS, 831 + item_index_offset, ItemClassification.progression, 0, 1),
    #Expert
    THE_OPEN_SEA_PASS: ItemData(PASS, 832 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    SHOUDU_PROVINCE_PASS: ItemData(PASS, 833 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    THE_UNDERCITY_PASS: ItemData(PASS, 834 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    GANYMEDE_SHRINE_PASS: ItemData(PASS, 835 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    BEAURIOR_VOLCANO_PASS: ItemData(PASS, 836 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    BEAURIOR_ROCK_PASS: ItemData(PASS, 837 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    LAKE_DELENDE_PASS: ItemData(PASS, 838 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    QUINTAR_RESERVE_PASS: ItemData(PASS, 839 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    DIONE_SHRINE_PASS: ItemData(PASS, 840 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    QUINTAR_MAUSOLEUM_PASS: ItemData(PASS, 841 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    EASTERN_CHASM_PASS: ItemData(PASS, 842 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    TALL_TALL_HEIGHTS_PASS: ItemData(PASS, 843 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    NORTHERN_CAVE_PASS: ItemData(PASS, 844 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    LANDS_END_PASS: ItemData(PASS, 845 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    SLIP_GLIDE_RIDE_PASS: ItemData(PASS, 846 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    SEQUOIA_ATHENAEUM_PASS: ItemData(PASS, 847 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    NORTHERN_STRETCH_PASS: ItemData(PASS, 848 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    CASTLE_RAMPARTS_PASS: ItemData(PASS, 849 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    THE_CHALICE_OF_TAR_PASS: ItemData(PASS, 850 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    FLYERS_CRAG_PASS: ItemData(PASS, 851 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    JIDAMBA_TANGLE_PASS: ItemData(PASS, 852 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    JIDAMBA_EACLANEYA_PASS: ItemData(PASS, 853 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    THE_DEEP_SEA_PASS: ItemData(PASS, 854 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    NEPTUNE_SHRINE_PASS: ItemData(PASS, 855 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    JADE_CAVERN_PASS: ItemData(PASS, 856 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    CONTINENTAL_TRAM_PASS: ItemData(PASS, 857 + item_index_offset, ItemClassification.progression, 0, 0, 1),
    #End Game
    ANCIENT_LABYRINTH_PASS: ItemData(PASS, 858 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    THE_SEQUOIA_PASS: ItemData(PASS, 859 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    THE_DEPTHS_PASS: ItemData(PASS, 860 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    CASTLE_SEQUOIA_PASS: ItemData(PASS, 861 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    THE_OLD_WORLD_PASS: ItemData(PASS, 862 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),
    THE_NEW_WORLD_PASS: ItemData(PASS, 863 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1),

    #Animal mount summons
    PROGRESSIVE_QUINTAR_WOODWIND: ItemData(MOUNT, 39 + item_index_offset, ItemClassification.progression | ItemClassification.useful, 3), #Quintar Pass ID 7 & Quintar Flute ID 39 & Quintar Ocarina 115
    IBEK_BELL: ItemData(MOUNT, 50 + item_index_offset, ItemClassification.progression | ItemClassification.useful),
    OWL_DRUM: ItemData(MOUNT, 49 + item_index_offset, ItemClassification.progression | ItemClassification.useful),
    PROGRESSIVE_SALMON_VIOLA: ItemData(MOUNT, 48 + item_index_offset, ItemClassification.progression | ItemClassification.useful, 2), #Salmon Violin ID 48 & Salmon Cello ID 114
    PROGRESSIVE_MOUNT: ItemData(MOUNT, 700 + item_index_offset, ItemClassification.progression | ItemClassification.useful, 7),

    #Teleport items (shards not included since they are stones but worse)
    HOME_POINT_STONE: ItemData(TELEPORT_STONE, 19 + item_index_offset, ItemClassification.useful), #Starter pack
    ARCHIPELAGO_STONE: ItemData(TELEPORT_STONE, 233 + item_index_offset, ItemClassification.useful), #Teleports you to your starting location
    GAEA_STONE: ItemData(TELEPORT_STONE, 23 + item_index_offset, ItemClassification.progression, 0, 1), #Teleport to Capital Sequoia, Advanced Regions
    MERCURY_STONE: ItemData(TELEPORT_STONE, 13 + item_index_offset, ItemClassification.progression), #Teleport to Beginner Regions
    POSEIDON_STONE: ItemData(TELEPORT_STONE, 57 + item_index_offset, ItemClassification.progression, 0, 1), #Teleport to Salmon River, Advanced Regions
    MARS_STONE: ItemData(TELEPORT_STONE, 59 + item_index_offset, ItemClassification.progression, 0, 1), #Teleport to Poko Poko Desert, Advanced Regions
    GANYMEDE_STONE: ItemData(TELEPORT_STONE, 65 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to above Shoudu Province, Expert Regions
    TRITON_STONE: ItemData(TELEPORT_STONE, 66 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to Tall Tall Heights, Expert Regions
    CALLISTO_STONE: ItemData(TELEPORT_STONE, 155 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to Lands End, Expert Regions
    EUROPA_STONE: ItemData(TELEPORT_STONE, 64 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to Jidamba Tangle, Expert Regions
    DIONE_STONE: ItemData(TELEPORT_STONE, 166 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to above Quintar Reserve, Expert Regions
    NEPTUNE_STONE: ItemData(TELEPORT_STONE, 208 + item_index_offset, ItemClassification.progression, 0, 0, 1), #Teleport to The Deep Sea, Expert Regions
    NEW_WORLD_STONE: ItemData(TELEPORT_STONE, 140 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1), #End-Game Regions (Astley & True Astley goals hand it to the player directly instead of from the item pool)
    OLD_WORLD_STONE: ItemData(TELEPORT_STONE, 253 + item_index_offset, ItemClassification.progression, 0, 0, 0, 1), #End-Game Regions (True Astley goal hands it to the player directly instead of from the item pool)

    #Weapons
    #Swords
    "Equipment - Short Sword": ItemData(EQUIPMENT, 0 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 1H, Shop, Beginner Zones
    "Equipment - Iron Sword": ItemData(EQUIPMENT, 11 + equipment_index_offset, ItemClassification.useful), #Tier 1 1H, Delende, Beginner Zones
    "Equipment - Contract": ItemData(EQUIPMENT, 71 + equipment_index_offset, ItemClassification.useful), #Tier 1 1H, Mercury Shrine, Beginner Zones
    "Equipment - Help the Prince": ItemData(EQUIPMENT, 89 + equipment_index_offset, ItemClassification.useful), #Tier 1 1H, Trial Caves/Skumparadise, Beginner Zones
    "Equipment - Craftwork Sword": ItemData(EQUIPMENT, 93 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 1H, Capital Sequoia, Advanced Zones
    "Equipment - Broadsword": ItemData(EQUIPMENT, 12 + equipment_index_offset, ItemClassification.useful), #Tier 1 2H, Yamagawa M.A., Beginner Zones
    "Equipment - Sharp Sword": ItemData(EQUIPMENT, 200 + equipment_index_offset, ItemClassification.useful), #Tier 2 1H, Skumparadise, Beginner Zones
    "Equipment - Razor Edge": ItemData(EQUIPMENT, 199 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 1H, Shop, Advanced Zones
    "Equipment - Silver Sword": ItemData(EQUIPMENT, 112 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Sword": ItemData(EQUIPMENT, 157 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1),  #Tier 2 1H, Shop, Advanced Zones
    "Equipment - Longsword": ItemData(EQUIPMENT, 378 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 2H, Shop, Advanced Zones
    "Equipment - Boomer Sword": ItemData(EQUIPMENT, 177 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 2H, Boomer Society, Advanced Zones
    "Equipment - Digested Sword": ItemData(EQUIPMENT, 227 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Scimitar": ItemData(EQUIPMENT, 379 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1),  #Tier 3 1H, Shop, Advanced Zones
    "Equipment - Cutlass": ItemData(EQUIPMENT, 377 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 1H, Shoudu Province, Expert Zones
    "Equipment - Cold Touch": ItemData(EQUIPMENT, 375 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 1H, Beaurior Rock, Expert Zones
    "Equipment - Burning Blade": ItemData(EQUIPMENT, 497 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Gold Sword": ItemData(EQUIPMENT, 138 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - War Sword": ItemData(EQUIPMENT, 376 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3 2H, Shop, Advanced Zones
    "Equipment - Bloodbind": ItemData(EQUIPMENT, 197 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 2H, Salmon River, Advanced Zones
    "Equipment - Temporal Blade": ItemData(EQUIPMENT, 525 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 2H, Beaurior Volcano, Expert Zones
    "Equipment - Highland Blade": ItemData(EQUIPMENT, 370 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3 2H, Shop, Expert Zones
    "Equipment - Hydra Edge": ItemData(EQUIPMENT, 371 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Defender": ItemData(EQUIPMENT, 380 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 1H, Lands End, Expert Zones
    "Equipment - Crystal Sword": ItemData(EQUIPMENT, 374 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4 1H, Shop, Expert Zones
    "Equipment - Conquest": ItemData(EQUIPMENT, 372 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 1H, Castle Ramparts, Expert Zones
    "Equipment - Flame Sword": ItemData(EQUIPMENT, 381 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 1H, Jidamba Eaclaneya, Expert Zones
    "Equipment - Master Sword": ItemData(EQUIPMENT, 248 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4 1H, Shop, Advanced Zones
    "Equipment - Rune Sword": ItemData(EQUIPMENT, 382 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 2H, Castle Ramparts, Expert Zones
    "Equipment - Auduril": ItemData(EQUIPMENT, 270 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Master Bigsword": ItemData(EQUIPMENT, 249 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4 2H, Shop, Advanced Zones
    "Equipment - Training Sword": ItemData(EQUIPMENT, 532 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Life Line": ItemData(EQUIPMENT, 302 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Soul Keeper": ItemData(EQUIPMENT, 303 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 1H, The Deep Sea, Expert Zones
    "Equipment - Crabs Claw": ItemData(EQUIPMENT, 411 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 1H, The Deep Sea, Expert Zones
    "Equipment - Kings Guard": ItemData(EQUIPMENT, 316 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 1H, Castle Sequoia, End-Game Zones
    "Equipment - Diamond Sword": ItemData(EQUIPMENT, 135 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Balrog": ItemData(EQUIPMENT, 369 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Oily Sword": ItemData(EQUIPMENT, 279 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 2H, Castle Sequoia, End-Game Zones

    #Axes
    "Equipment - Hand Axe": ItemData(EQUIPMENT, 55 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 1H, Shop, Beginner Zones
    "Equipment - Craftwork Axe": ItemData(EQUIPMENT, 94 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 1H, Capital Sequoia, Advanced Zones
    "Equipment - Cleaver": ItemData(EQUIPMENT, 2 + equipment_index_offset, ItemClassification.useful), #Tier 1 2H, Spawning Meadows, Beginner Zones
    "Equipment - Chopper": ItemData(EQUIPMENT, 66 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 2H, Shop, Beginner Zones
    "Equipment - Hunting Axe": ItemData(EQUIPMENT, 187 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 1H, Rolling Quintar Fields, Advanced Zones
    "Equipment - Silver Axe": ItemData(EQUIPMENT, 104 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Stone Splitter": ItemData(EQUIPMENT, 201 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 2H, Shop, Advanced Zones
    "Equipment - Broadaxe": ItemData(EQUIPMENT, 383 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 2H, Shop, Advanced Zones
    "Equipment - Artisan Axe": ItemData(EQUIPMENT, 158 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 2H, Shop, Advanced Zones
    "Equipment - Hatchet": ItemData(EQUIPMENT, 386 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 1H, Poko Poko Desert, Advanced Zones
    "Equipment - Axe of Light": ItemData(EQUIPMENT, 387 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Gold Axe": ItemData(EQUIPMENT, 139 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - War Axe": ItemData(EQUIPMENT, 384 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3 2H, Shop, Advanced Zones
    "Equipment - Berserker Axe": ItemData(EQUIPMENT, 390 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3 2H, Shop, Expert Zones
    "Equipment - Gaia Axe": ItemData(EQUIPMENT, 385 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 2H, Shoudu Province, Expert Zones
    "Equipment - Master Axe": ItemData(EQUIPMENT, 251 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4 1H, Shop, Advanced Zones
    "Equipment - Ancient Axe": ItemData(EQUIPMENT, 391 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4 2H, Shop, Expert Zones
    "Equipment - Master Bigaxe": ItemData(EQUIPMENT, 250 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4 2H, Shop, Advanced Zones
    "Equipment - Aphotic Edge": ItemData(EQUIPMENT, 388 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 1H, The Sequoia, End-Game Zones
    "Equipment - Diamond Axe": ItemData(EQUIPMENT, 136 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Decapitator": ItemData(EQUIPMENT, 280 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 2H, Castle Sequoia, End-Game Zones
    "Equipment - Ragebringer": ItemData(EQUIPMENT, 274 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 2H, Capital Sequoia, Advanced Zones

    #Daggers
    "Equipment - Dirk": ItemData(EQUIPMENT, 3 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 Regular, Shop, Beginner Zones
    "Equipment - Stabbers": ItemData(EQUIPMENT, 63 + equipment_index_offset, ItemClassification.useful), #Tier 1 Regular, Spawning Meadows, Beginner Zones
    "Equipment - Fishgutter": ItemData(EQUIPMENT, 77 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 Regular, Shop, Beginner Zones
    "Equipment - Poisonkiss": ItemData(EQUIPMENT, 40 + equipment_index_offset, ItemClassification.useful), #Tier 1 Regular, Pale Grotto, Beginner Zones
    "Equipment - Shank": ItemData(EQUIPMENT, 60 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 Regular, Shop, Beginner Zones
    "Equipment - Craftwork Dagger": ItemData(EQUIPMENT, 95 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 Regular, Capital Sequoia, Advanced Zones
    "Equipment - Tanto": ItemData(EQUIPMENT, 192 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Ninja, Okimoto N.S., Advanced Zones
    "Equipment - Butterfly": ItemData(EQUIPMENT, 203 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Ninja, Okimoto N.S., Advanced Zones
    "Equipment - Kris": ItemData(EQUIPMENT, 202 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 Regular, Shop, Advanced Zones
    "Equipment - Ambush Knife": ItemData(EQUIPMENT, 184 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Regular, Greenshire Reprise, Advanced Zones
    "Equipment - Rondel": ItemData(EQUIPMENT, 204 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 Regular, Shop, Advanced Zones
    "Equipment - Silver Dagger": ItemData(EQUIPMENT, 113 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Dagger": ItemData(EQUIPMENT, 159 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 Regular, Shop, Advanced Zones
    "Equipment - Parry Knife": ItemData(EQUIPMENT, 397 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Ninja, Salmon River, Advanced Zones
    "Equipment - Janbiya": ItemData(EQUIPMENT, 392 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3 Ninja, Shop, Advanced Zones
    "Equipment - Sai": ItemData(EQUIPMENT, 396 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3 Ninja, Shop, Expert Zones
    "Equipment - Kodachi": ItemData(EQUIPMENT, 400 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3 Ninja, Shop, Expert Zones
    "Equipment - Butter Cutter": ItemData(EQUIPMENT, 198 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Regular, Poko Poko Desert, Advanced Zones
    "Equipment - Soul Kris": ItemData(EQUIPMENT, 305 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Regular, Shoudu Province, Expert Zones
    "Equipment - Gouger": ItemData(EQUIPMENT, 61 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Fanged Knife": ItemData(EQUIPMENT, 526 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3 Regular, Shop, Expert Zones
    "Equipment - Cinquedea": ItemData(EQUIPMENT, 393 + equipment_index_offset, ItemClassification.useful), #from Delende fisher; Tier 3 Regular, Delende, Beginner Zones
    "Equipment - Gold Dagger": ItemData(EQUIPMENT, 140 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Kowakizashi": ItemData(EQUIPMENT, 398 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Bone Knife": ItemData(EQUIPMENT, 395 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Poignard": ItemData(EQUIPMENT, 394 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4 Regular, Shop, Expert Zones
    "Equipment - Flamespike": ItemData(EQUIPMENT, 72 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Regular, Jidamba Tangle, Expert Zones
    "Equipment - Master Dagger": ItemData(EQUIPMENT, 269 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4 Regular, Shop, Advanced Zones
    "Equipment - Sange": ItemData(EQUIPMENT, 317 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Ninja, The Sequoia, End-Game Zones
    "Equipment - Yasha": ItemData(EQUIPMENT, 318 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Ninja, Shoudu Province, Expert Zones
    "Equipment - Legend Spike": ItemData(EQUIPMENT, 315 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Eclipse": ItemData(EQUIPMENT, 41 + equipment_index_offset, ItemClassification.useful, 0), #Capital Sequoia shady shop guy
    "Equipment - Mage Masher": ItemData(EQUIPMENT, 282 + equipment_index_offset, ItemClassification.useful, 0), #Capital Sequoia shady shop guy
    "Equipment - Mages Pike": ItemData(EQUIPMENT, 306 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Regular, The New World, End-Game Zones
    "Equipment - Diamond Dagger": ItemData(EQUIPMENT, 137 + equipment_index_offset, ItemClassification.useful, 0),
    
    #Rapiers
    "Equipment - Rapier": ItemData(EQUIPMENT, 73 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Stinger": ItemData(EQUIPMENT, 1 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Toothpick": ItemData(EQUIPMENT, 42 + equipment_index_offset, ItemClassification.useful), #Tier 1, Pale Grotto, Beginner Zones
    "Equipment - Craftwork Rapier": ItemData(EQUIPMENT, 96 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Estoc": ItemData(EQUIPMENT, 207 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Scarlette": ItemData(EQUIPMENT, 206 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Fish Skewer": ItemData(EQUIPMENT, 175 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Sara Sara Bazaar, Advanced Zones
    "Equipment - Silver Rapier": ItemData(EQUIPMENT, 114 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Rapier": ItemData(EQUIPMENT, 160 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Dueller": ItemData(EQUIPMENT, 10 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Poko Poko Desert, Advanced Zones
    "Equipment - Vulture": ItemData(EQUIPMENT, 402 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Falcon Dance": ItemData(EQUIPMENT, 408 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Fleuret": ItemData(EQUIPMENT, 404 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Gold Rapier": ItemData(EQUIPMENT, 141 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Epee": ItemData(EQUIPMENT, 405 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Windsong": ItemData(EQUIPMENT, 407 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, The Chalice of Tar, Expert Zones
    "Equipment - Master Rapier": ItemData(EQUIPMENT, 252 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Nightingale": ItemData(EQUIPMENT, 401 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    "Equipment - Chartreuse": ItemData(EQUIPMENT, 403 + equipment_index_offset, ItemClassification.useful), #Tier 5, Delende, Beginner Zones
    "Equipment - Murgleys": ItemData(EQUIPMENT, 406 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5, The Open Sea, Expert Zones
    "Equipment - Diamond Rapier": ItemData(EQUIPMENT, 142 + equipment_index_offset, ItemClassification.useful, 0),
    
    #Katanas
    "Equipment - Craftwork Katana": ItemData(EQUIPMENT, 97 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a katana as a treat)
    "Equipment - Tachi": ItemData(EQUIPMENT, 399 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Okimoto N.S., Advanced Zones
    "Equipment - Silver Katana": ItemData(EQUIPMENT, 115 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Katana": ItemData(EQUIPMENT, 161 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Nansen": ItemData(EQUIPMENT, 363 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Mitsutada": ItemData(EQUIPMENT, 22 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Hitofuri": ItemData(EQUIPMENT, 364 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Kokaiji": ItemData(EQUIPMENT, 23 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Gold Katana": ItemData(EQUIPMENT, 143 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Hokuken": ItemData(EQUIPMENT, 588 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Tomokirimaru": ItemData(EQUIPMENT, 366 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Ichimonji": ItemData(EQUIPMENT, 362 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Master Katana": ItemData(EQUIPMENT, 253 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Muramasa": ItemData(EQUIPMENT, 367 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Shoudu Province, Expert Zones
    "Equipment - Diamond Katana": ItemData(EQUIPMENT, 144 + equipment_index_offset, ItemClassification.useful, 0),

    #Spears
    "Equipment - Short Spear": ItemData(EQUIPMENT, 4 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 1, Shop, Advanced Zones
    "Equipment - Craftwork Spear": ItemData(EQUIPMENT, 98 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a spear as a treat)
    "Equipment - Javelin": ItemData(EQUIPMENT, 205 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Skewer": ItemData(EQUIPMENT, 190 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Cobblestone Crag, Advanced Zones
    "Equipment - Prodder": ItemData(EQUIPMENT, 183 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Sequoia, Advanced Zones
    "Equipment - Silver Spear": ItemData(EQUIPMENT, 116 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Spear": ItemData(EQUIPMENT, 162 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Trident": ItemData(EQUIPMENT, 409 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Salmon River, Advanced Zones
    "Equipment - Wind Lance": ItemData(EQUIPMENT, 410 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Halberd": ItemData(EQUIPMENT, 418 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Rock, Expert Zones
    "Equipment - Gold Spear": ItemData(EQUIPMENT, 145 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Voulge": ItemData(EQUIPMENT, 419 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Radiance": ItemData(EQUIPMENT, 417 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Northern Cave, Expert Zones
    "Equipment - Partizan": ItemData(EQUIPMENT, 416 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Master Spear": ItemData(EQUIPMENT, 254 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Incursier": ItemData(EQUIPMENT, 563 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Royal Guard": ItemData(EQUIPMENT, 275 + equipment_index_offset, ItemClassification.useful,0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    "Equipment - Gungnir": ItemData(EQUIPMENT, 304 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Diamond Spear": ItemData(EQUIPMENT, 146 + equipment_index_offset, ItemClassification.useful, 0),
    
    #Scythes
    "Equipment - Battle Scythe": ItemData(EQUIPMENT, 6 + equipment_index_offset, ItemClassification.useful), #Tier 1, Proving Meadows, Beginner Zones
    "Equipment - Craftwork Scythe": ItemData(EQUIPMENT, 99 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - War Scythe": ItemData(EQUIPMENT, 208 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Wind Sickle": ItemData(EQUIPMENT, 413 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Silver Scythe": ItemData(EQUIPMENT, 117 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Scythe": ItemData(EQUIPMENT, 163 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Thresher": ItemData(EQUIPMENT, 294 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Grim Scythe": ItemData(EQUIPMENT, 293 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Ancient Reservoir, Advanced Zones
    "Equipment - Great Thresher": ItemData(EQUIPMENT, 295 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Frost Reaper": ItemData(EQUIPMENT, 414 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Tall Tall Heights, Expert Zones
    "Equipment - Gold Scythe": ItemData(EQUIPMENT, 147 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Ember Scythe": ItemData(EQUIPMENT, 589 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Gravedigger": ItemData(EQUIPMENT, 415 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    "Equipment - Wind Thresher": ItemData(EQUIPMENT, 590 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Quintar Mausoleum, Expert Zones
    "Equipment - Master Scythe": ItemData(EQUIPMENT, 255 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Twilight": ItemData(EQUIPMENT, 412 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Adjudicator": ItemData(EQUIPMENT, 245 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Arctic Chill": ItemData(EQUIPMENT, 556 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Diamond Scythe": ItemData(EQUIPMENT, 148 + equipment_index_offset, ItemClassification.useful, 0),

    #Bows
    "Equipment - Craftwork Bow": ItemData(EQUIPMENT, 105 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a bow as a treat)
    "Equipment - Short Bow": ItemData(EQUIPMENT, 7 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Hunting Bow": ItemData(EQUIPMENT, 181 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Rolling Quintar Fields, Advanced Zones
    "Equipment - Long Bow": ItemData(EQUIPMENT, 209 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Silver Bow": ItemData(EQUIPMENT, 118 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Bow": ItemData(EQUIPMENT, 164 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Battle Bow": ItemData(EQUIPMENT, 297 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Composite Bow": ItemData(EQUIPMENT, 296 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Habins Bow": ItemData(EQUIPMENT, 222 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Razor Bow": ItemData(EQUIPMENT, 298 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Elven Bow": ItemData(EQUIPMENT, 421 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Gold Bow": ItemData(EQUIPMENT, 149 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Spore Shooter": ItemData(EQUIPMENT, 180 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - War Bow": ItemData(EQUIPMENT, 300 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Siege Bow": ItemData(EQUIPMENT, 301 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Rune Bow": ItemData(EQUIPMENT, 299 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Master Bow": ItemData(EQUIPMENT, 256 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Panakeia": ItemData(EQUIPMENT, 530 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artemis": ItemData(EQUIPMENT, 281 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 5, Shop, Expert Zones
    "Equipment - Dream Hunter": ItemData(EQUIPMENT, 420 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    "Equipment - Diamond Bow": ItemData(EQUIPMENT, 150 + equipment_index_offset, ItemClassification.useful, 0),

    #Staves
    "Equipment - Short Staff": ItemData(EQUIPMENT, 5 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 Regular, Shop, Beginner Zones
    "Equipment - Cedar Staff": ItemData(EQUIPMENT, 62 + equipment_index_offset, ItemClassification.useful), #Tier 1 Regular, Spawning Meadows, Beginner Zones
    "Equipment - Gnarled Root": ItemData(EQUIPMENT, 15 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1 Regular, Shop, Beginner Zones
    "Equipment - Craftwork Staff": ItemData(EQUIPMENT, 100 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1 Regular, Capital Sequoia, Advanced Zones
    "Equipment - Bone Smasher": ItemData(EQUIPMENT, 14 + equipment_index_offset, ItemClassification.useful), #Tier 1 Beating, Delende, Beginner Zones
    "Equipment - Iron Rod": ItemData(EQUIPMENT, 426 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Beating, Capital Jail, Advanced Zones
    "Equipment - Quarterstaff": ItemData(EQUIPMENT, 210 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 Regular, Shop, Advanced Zones
    "Equipment - Walking Stick": ItemData(EQUIPMENT, 188 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Regular, Cobblestone Crag, Advanced Zones
    "Equipment - Maplewood": ItemData(EQUIPMENT, 211 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 Regular, Shop, Advanced Zones
    "Equipment - Silver Staff": ItemData(EQUIPMENT, 119 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Staff": ItemData(EQUIPMENT, 165 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2 Regular, Shop, Advanced Zones
    "Equipment - Knockout Stick": ItemData(EQUIPMENT, 335 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Beating, Sara Sara Bazaar, Advanced Zones
    "Equipment - Skullbasher": ItemData(EQUIPMENT, 427 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3 Beating, Shop, Advanced Zones
    "Equipment - Future Sight": ItemData(EQUIPMENT, 561 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Battle Staff": ItemData(EQUIPMENT, 67 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3 Beating, Shop, Expert Zones
    "Equipment - Digested Staff": ItemData(EQUIPMENT, 228 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Natures Gift": ItemData(EQUIPMENT, 423 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3 Regular, Shop, Advanced Zones
    "Equipment - Life Jewel": ItemData(EQUIPMENT, 422 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Regular, Overpass (Dione Shrine), Advanced (Expert) Zones
    "Equipment - Gold Staff": ItemData(EQUIPMENT, 151 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - War Staff": ItemData(EQUIPMENT, 428 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4 Beating, Shop, Expert Zones
    "Equipment - Apprentice": ItemData(EQUIPMENT, 424 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Regular, Northern Cave, Expert Zones
    "Equipment - Sages Walker": ItemData(EQUIPMENT, 425 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Regular, Slip Glide Ride, Expert Zones
    "Equipment - Master Staff": ItemData(EQUIPMENT, 257 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4 Regular, Shop, Advanced Zones
    "Equipment - Beats Stick": ItemData(EQUIPMENT, 289 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Staff of Balance": ItemData(EQUIPMENT, 290 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Regular, Jidamba Eaclaneya, Expert Zones
    "Equipment - Judgement": ItemData(EQUIPMENT, 429 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Regular, Ancient Labyrinth, End-Game Zones
    "Equipment - Diamond Staff": ItemData(EQUIPMENT, 152 + equipment_index_offset, ItemClassification.useful, 0),

    #Wands
    "Equipment - Ash Wand": ItemData(EQUIPMENT, 8 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Cedar Wand": ItemData(EQUIPMENT, 13 + equipment_index_offset, ItemClassification.useful), #Tier 1, Spawning Meadows, Beginner Zones
    "Equipment - Oak Wand": ItemData(EQUIPMENT, 16 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Torch": ItemData(EQUIPMENT, 64 + equipment_index_offset, ItemClassification.useful), #Tier 1, Draft Shaft Conduit, Beginner Zones
    "Equipment - Ink Stick": ItemData(EQUIPMENT, 80 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Craftwork Wand": ItemData(EQUIPMENT, 101 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Soul Wand": ItemData(EQUIPMENT, 213 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Static Rod": ItemData(EQUIPMENT, 189 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Quintar Nest, Advanced Zones
    "Equipment - Maple Wand": ItemData(EQUIPMENT, 212 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Silver Wand": ItemData(EQUIPMENT, 120 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Wand": ItemData(EQUIPMENT, 166 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Storm Rod": ItemData(EQUIPMENT, 267 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Sara Sara Bazaar, Advanced Zones
    "Equipment - Baton": ItemData(EQUIPMENT, 434 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Cursegiver": ItemData(EQUIPMENT, 432 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, The Undercity, Expert Zones
    "Equipment - Effigy": ItemData(EQUIPMENT, 433 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Gold Wand": ItemData(EQUIPMENT, 153 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Rune Wand": ItemData(EQUIPMENT, 435 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Lands End, Expert Zones
    "Equipment - Sentinel Rod": ItemData(EQUIPMENT, 431 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Stardust Wand": ItemData(EQUIPMENT, 430 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Eaclaneya, Expert Zones
    "Equipment - Master Wand": ItemData(EQUIPMENT, 258 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Aura Focus": ItemData(EQUIPMENT, 278 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Paladin Wand": ItemData(EQUIPMENT, 276 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, The Deep Sea, Expert Zones
    "Equipment - Obelisk": ItemData(EQUIPMENT, 307 + equipment_index_offset, ItemClassification.useful, 0),  #black market shop (Z14_hobo shop)
    "Equipment - Flameseeker": ItemData(EQUIPMENT, 358 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Jidamba Eaclaneya, Expert Zones
    "Equipment - Diamond Wand": ItemData(EQUIPMENT, 154 + equipment_index_offset, ItemClassification.useful, 0),

    #Books
    "Equipment - Moby Dick": ItemData(EQUIPMENT, 51 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Orylei": ItemData(EQUIPMENT, 65 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Craftwork Pages": ItemData(EQUIPMENT, 102 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a book as a treat)
    "Equipment - Encyclopedia": ItemData(EQUIPMENT, 214 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Gospel": ItemData(EQUIPMENT, 194 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Boomer Society, Advanced Zones
    "Equipment - Paypirbak": ItemData(EQUIPMENT, 223 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Salmon Pass, Advanced Zones
    "Equipment - Art of War": ItemData(EQUIPMENT, 224 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Okimoto N.S., Advanced Zones
    "Equipment - Silver Pages": ItemData(EQUIPMENT, 121 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Pages": ItemData(EQUIPMENT, 167 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Grimoire": ItemData(EQUIPMENT, 438 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Blank Pages": ItemData(EQUIPMENT, 437 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Sara Sara Beach, Advanced Zones
    "Equipment - Tome of Light": ItemData(EQUIPMENT, 439 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Volcano, Expert Zones
    "Equipment - Hydrology": ItemData(EQUIPMENT, 441 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Gold Pages": ItemData(EQUIPMENT, 155 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Dark Gospel": ItemData(EQUIPMENT, 440 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Beaurior Volcano, Expert Zones
    "Equipment - Divination": ItemData(EQUIPMENT, 442 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Malifice": ItemData(EQUIPMENT, 443 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    "Equipment - Master Pages": ItemData(EQUIPMENT, 259 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Codex": ItemData(EQUIPMENT, 436 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Diamond Pages": ItemData(EQUIPMENT, 156 + equipment_index_offset, ItemClassification.useful, 0),

    #Armor
    #Shields
    "Equipment - Buckler": ItemData(EQUIPMENT, 44 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Stout Shield": ItemData(EQUIPMENT, 45 + equipment_index_offset, ItemClassification.useful), #Tier 1, Spawning Meadows, Beginner Zones
    "Equipment - Iron Guard": ItemData(EQUIPMENT, 68 + equipment_index_offset, ItemClassification.useful), #Tier 1, Yamagawa M.A., Beginner Zones
    "Equipment - Stalwart Shield": ItemData(EQUIPMENT, 88 + equipment_index_offset, ItemClassification.useful), #Tier 1, Trial Caves/Skumparadise, Beginner Zones
    "Equipment - Craftwork Shield": ItemData(EQUIPMENT, 506 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Vanguard": ItemData(EQUIPMENT, 111 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Duelling Shield": ItemData(EQUIPMENT, 215 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Lucky Platter": ItemData(EQUIPMENT, 103 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Pipeline, Advanced Zones
    "Equipment - Boomer Shield": ItemData(EQUIPMENT, 178 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Boomer Society, Advanced Zones
    "Equipment - Silver Shield": ItemData(EQUIPMENT, 507 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Shield": ItemData(EQUIPMENT, 168 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Cross Shield": ItemData(EQUIPMENT, 444 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Brass Cross": ItemData(EQUIPMENT, 448 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Blood Shield": ItemData(EQUIPMENT, 560 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - The Immovable": ItemData(EQUIPMENT, 451 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Cross Guard": ItemData(EQUIPMENT, 446 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Mages Platter": ItemData(EQUIPMENT, 452 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Salmon River, Advanced Zones
    "Equipment - Gold Shield": ItemData(EQUIPMENT, 447 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Bulkwark": ItemData(EQUIPMENT, 449 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Flame Guard": ItemData(EQUIPMENT, 450 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Wizards Wall": ItemData(EQUIPMENT, 453 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    "Equipment - Master Shield": ItemData(EQUIPMENT, 260 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Turtle Shell": ItemData(EQUIPMENT, 445 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 5, Shop, Expert Zones
    "Equipment - Tower Shield": ItemData(EQUIPMENT, 344 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Jidamba Tangle, Expert Zones
    "Equipment - Nomads Guard": ItemData(EQUIPMENT, 288 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Continental Tram, Expert Zones
    "Equipment - Ether Shield": ItemData(EQUIPMENT, 277 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Mirror Shield": ItemData(EQUIPMENT, 246 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Ancient Labyrinth, End-Game Zones
    "Equipment - Diamond Shield": ItemData(EQUIPMENT, 237 + equipment_index_offset, ItemClassification.useful, 0),

    #Heavy Head
    "Equipment - Chain Helm": ItemData(EQUIPMENT, 25 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Sturdy Helm": ItemData(EQUIPMENT, 26 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Storm Helm": ItemData(EQUIPMENT, 74 + equipment_index_offset, ItemClassification.useful), #Tier 1, Pale Grotto, Beginner Zones
    "Equipment - Copper Helm": ItemData(EQUIPMENT, 69 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Craftwork Helm": ItemData(EQUIPMENT, 508 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Bronze Helm": ItemData(EQUIPMENT, 106 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Scale Helm": ItemData(EQUIPMENT, 128 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Iron Helm": ItemData(EQUIPMENT, 125 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Jojo Sewers, Advanced Zones
    "Equipment - Battle Helm": ItemData(EQUIPMENT, 132 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    "Equipment - Silver Helm": ItemData(EQUIPMENT, 509 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Helm": ItemData(EQUIPMENT, 169 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Orion Barbut": ItemData(EQUIPMENT, 465 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Iron Barbut": ItemData(EQUIPMENT, 468 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Horned Helm": ItemData(EQUIPMENT, 464 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Gold Helm": ItemData(EQUIPMENT, 469 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Cross Helm": ItemData(EQUIPMENT, 466 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Insignia Helm": ItemData(EQUIPMENT, 470 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Tall Tall Heights, Expert Zones
    "Equipment - Demon Helm": ItemData(EQUIPMENT, 467 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Master Helm": ItemData(EQUIPMENT, 261 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Guts Busby": ItemData(EQUIPMENT, 308 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Raid Helm": ItemData(EQUIPMENT, 471 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Spellsword Helm": ItemData(EQUIPMENT, 292 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Sequoia Athenaeum, Expert Zones
    "Equipment - Diamond Helm": ItemData(EQUIPMENT, 236 + equipment_index_offset, ItemClassification.useful, 0),

    #Heavy Body
    "Equipment - Breastplate": ItemData(EQUIPMENT, 18 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Ring Mail": ItemData(EQUIPMENT, 28 + equipment_index_offset, ItemClassification.useful), #Tier 1, Pale Grotto, Beginner Zones
    "Equipment - Copper Suit": ItemData(EQUIPMENT, 29 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Plate of Wolf": ItemData(EQUIPMENT, 84 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Underpass, Advanced Zones
    "Equipment - Craftwork Mail": ItemData(EQUIPMENT, 510 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Bronze Suit": ItemData(EQUIPMENT, 107 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Scale Mail": ItemData(EQUIPMENT, 127 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Iron Armor": ItemData(EQUIPMENT, 126 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Jojo Sewers, Advanced Zones
    "Equipment - Battleplate": ItemData(EQUIPMENT, 43 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    "Equipment - Silver Mail": ItemData(EQUIPMENT, 511 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Mail": ItemData(EQUIPMENT, 170 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Orion Armor": ItemData(EQUIPMENT, 455 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Plate of Tiger": ItemData(EQUIPMENT, 129 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Plate Mail": ItemData(EQUIPMENT, 460 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Knights Plate": ItemData(EQUIPMENT, 456 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, The Undercity, Expert Zones
    "Equipment - Bone Mail": ItemData(EQUIPMENT, 462 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Gold Mail": ItemData(EQUIPMENT, 459 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Sky Armor": ItemData(EQUIPMENT, 461 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Shoudu Province, Expert Zones
    "Equipment - Plate of Lion": ItemData(EQUIPMENT, 130 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Slip Glide Ride, Expert Zones
    "Equipment - Dragon Mail": ItemData(EQUIPMENT, 457 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Demon Plate": ItemData(EQUIPMENT, 458 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Master Mail": ItemData(EQUIPMENT, 262 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Construct Mail": ItemData(EQUIPMENT, 272 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Guardian Angel": ItemData(EQUIPMENT, 291 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Plate of Whale": ItemData(EQUIPMENT, 131 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5, The Open Sea, Expert Zones
    "Equipment - Lunar Mail": ItemData(EQUIPMENT, 463 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The New World, End-Game Zones
    "Equipment - Diamond Mail": ItemData(EQUIPMENT, 235 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Warrior Mail": ItemData(EQUIPMENT, 533 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Warlock Mail": ItemData(EQUIPMENT, 534 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Aegis Mail": ItemData(EQUIPMENT, 536 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Reaper Mail": ItemData(EQUIPMENT, 535 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Samurai Mail": ItemData(EQUIPMENT, 538 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Valkyrie Mail": ItemData(EQUIPMENT, 537 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Beastmaster Mail": ItemData(EQUIPMENT, 557 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Mimic Mail": ItemData(EQUIPMENT, 548 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    
    #Medium Head
    "Equipment - Leather Cap": ItemData(EQUIPMENT, 24 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Beret": ItemData(EQUIPMENT, 27 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Storm Cap": ItemData(EQUIPMENT, 75 + equipment_index_offset, ItemClassification.useful), #Tier 1, Seaside Cliffs, Beginner Zones
    "Equipment - Headgear": ItemData(EQUIPMENT, 30 + equipment_index_offset, ItemClassification.useful), #Tier 1, Seaside Cliffs, Beginner Zones
    "Equipment - Craftwork Cap": ItemData(EQUIPMENT, 512 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Rugged Hat": ItemData(EQUIPMENT, 219 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Spore Blocker": ItemData(EQUIPMENT, 195 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Rolling Quintar Fields, Advanced Zones
    "Equipment - Vikings Hat": ItemData(EQUIPMENT, 220 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Silver Cap": ItemData(EQUIPMENT, 513 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Cap": ItemData(EQUIPMENT, 171 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Combat Band": ItemData(EQUIPMENT, 483 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Red Cap": ItemData(EQUIPMENT, 233 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Ancient Reservoir, Advanced Zones
    "Equipment - Bandana": ItemData(EQUIPMENT, 484 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Suitor Hat": ItemData(EQUIPMENT, 485 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Gold Cap": ItemData(EQUIPMENT, 520 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Red Hat": ItemData(EQUIPMENT, 480 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Pirate Hat": ItemData(EQUIPMENT, 481 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Ice fisher in Tall Tall Heights; Tier 4, Tall Tall Heights, Expert Zones
    "Equipment - Tall Tall Hat": ItemData(EQUIPMENT, 486 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Master Cap": ItemData(EQUIPMENT, 263 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Battle Band": ItemData(EQUIPMENT, 345 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The Sequoia, End-Game Zones
    "Equipment - Captains Hat": ItemData(EQUIPMENT, 482 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5, Sara Sara Bazaar, Advanced Zones
    "Equipment - Red Headgear": ItemData(EQUIPMENT, 487 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 5, Shop, Expert Zones
    "Equipment - Diamond Cap": ItemData(EQUIPMENT, 238 + equipment_index_offset, ItemClassification.useful, 0),

    #Medium Body
    "Equipment - Leather Outfit": ItemData(EQUIPMENT, 17 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Studded Armor": ItemData(EQUIPMENT, 35 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Leather Mail": ItemData(EQUIPMENT, 36 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Craftwork Vest": ItemData(EQUIPMENT, 514 + equipment_index_offset, ItemClassification.useful), #Tier 1, Capital Sequoia, Advanced Zones (beginners can have little a medium body as a treat)
    "Equipment - Chain Vest": ItemData(EQUIPMENT, 217 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Combat Vest": ItemData(EQUIPMENT, 218 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Smelly Gi": ItemData(EQUIPMENT, 268 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Jojo Sewers, Advanced Zones
    "Equipment - Training Gi": ItemData(EQUIPMENT, 229 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Okimoto N.S., Advanced Zones
    "Equipment - Tuxedo": ItemData(EQUIPMENT, 176 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Sequoia, Advanced Zones
    "Equipment - Silver Vest": ItemData(EQUIPMENT, 515 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Vest": ItemData(EQUIPMENT, 172 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Power Vest": ItemData(EQUIPMENT, 472 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Red Coat": ItemData(EQUIPMENT, 57 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3, Ancient Reservoir, Advanced Zones
    "Equipment - Drifters Vest": ItemData(EQUIPMENT, 474 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Bandage Wrap": ItemData(EQUIPMENT, 558 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Gaia Vest": ItemData(EQUIPMENT, 473 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Brigandine": ItemData(EQUIPMENT, 477 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, The Undercity, Expert Zones
    "Equipment - Gold Vest": ItemData(EQUIPMENT, 521 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Onion Gi": ItemData(EQUIPMENT, 475 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Martial Vest": ItemData(EQUIPMENT, 478 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Judo Gi": ItemData(EQUIPMENT, 479 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Tall Tall Heights, Expert Zones
    "Equipment - Master Vest": ItemData(EQUIPMENT, 264 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Quintar Pelt": ItemData(EQUIPMENT, 493 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 5, Shop, Expert Zones
    "Equipment - Shadow Gi": ItemData(EQUIPMENT, 347 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, Shoudu Province, Expert Zones
    "Equipment - Rex Vest": ItemData(EQUIPMENT, 476 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Slime Coat": ItemData(EQUIPMENT, 524 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Diamond Vest": ItemData(EQUIPMENT, 239 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Monk Vest": ItemData(EQUIPMENT, 539 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Rogue Vest": ItemData(EQUIPMENT, 540 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Fencer Vest": ItemData(EQUIPMENT, 541 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Hunter Vest": ItemData(EQUIPMENT, 542 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Ninja Vest": ItemData(EQUIPMENT, 543 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Nomad Vest": ItemData(EQUIPMENT, 544 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Beatsmith Vest": ItemData(EQUIPMENT, 545 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Assassin Vest": ItemData(EQUIPMENT, 546 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones

    #Light Head
    "Equipment - Hemp Hood": ItemData(EQUIPMENT, 31 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Cotton Hood": ItemData(EQUIPMENT, 32 + equipment_index_offset, ItemClassification.useful), #Tier 1, Delende, Beginner Zones
    "Equipment - Storm Hood": ItemData(EQUIPMENT, 76 + equipment_index_offset, ItemClassification.useful), #Tier 1, Delende, Beginner Zones
    "Equipment - Holy Hat": ItemData(EQUIPMENT, 33 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Craftwork Crown": ItemData(EQUIPMENT, 516 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Silk Hat": ItemData(EQUIPMENT, 110 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Circlet": ItemData(EQUIPMENT, 133 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Quintar Sanctum, Advanced Zones
    "Equipment - Holy Miter": ItemData(EQUIPMENT, 109 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Woven Hood": ItemData(EQUIPMENT, 122 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    "Equipment - Silver Crown": ItemData(EQUIPMENT, 517 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Crown": ItemData(EQUIPMENT, 173 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Clerics Hood": ItemData(EQUIPMENT, 341 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Wizards Hat": ItemData(EQUIPMENT, 340 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Fairys Crown": ItemData(EQUIPMENT, 352 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Quilted Hat": ItemData(EQUIPMENT, 353 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Blood Hat": ItemData(EQUIPMENT, 559 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Plague Mask": ItemData(EQUIPMENT, 342 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Shoudu Province, Expert Zones
    "Equipment - Guard Crown": ItemData(EQUIPMENT, 356 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Rock, Expert Zones
    "Equipment - Gold Crown": ItemData(EQUIPMENT, 522 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Bronze Hairpin": ItemData(EQUIPMENT, 34 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tall Tall Heights fisher; Tier 4, Tall Tall Heights, Expert Zones
    "Equipment - Regen Crown": ItemData(EQUIPMENT, 343 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Ravens Hood": ItemData(EQUIPMENT, 348 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Celestial Crown": ItemData(EQUIPMENT, 52 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Eaclaneya, Expert Zones
    "Equipment - Master Crown": ItemData(EQUIPMENT, 265 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Advanced Zones
    "Equipment - Pointy Hat": ItemData(EQUIPMENT, 531 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5, The Deep Sea, Expert Zones
    "Equipment - Vita Crown": ItemData(EQUIPMENT, 271 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Ancient Labyrinth, End-Game Zones
    "Equipment - Pact Crown": ItemData(EQUIPMENT, 350 + equipment_index_offset, ItemClassification.useful, 0),  #black market shop (Z14_hobo shop)
    "Equipment - Protector": ItemData(EQUIPMENT, 354 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Castle Sequoia, End-Game Zones
    "Equipment - Diamond Crown": ItemData(EQUIPMENT, 240 + equipment_index_offset, ItemClassification.useful, 0),

    #Light Body
    "Equipment - Hemp Robe": ItemData(EQUIPMENT, 19 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Cotton Robe": ItemData(EQUIPMENT, 20 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 1), #Tier 1, Shop, Beginner Zones
    "Equipment - Mages Robe": ItemData(EQUIPMENT, 21 + equipment_index_offset, ItemClassification.useful), #Tier 1, Delende, Beginner Zones
    "Equipment - Swimmers Top": ItemData(EQUIPMENT, 81 + equipment_index_offset, ItemClassification.useful), #Tier 1, Seaside Cliffs, Beginner Zones
    "Equipment - Craftwork Robe": ItemData(EQUIPMENT, 518 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 1, Capital Sequoia, Advanced Zones
    "Equipment - Priest Garb": ItemData(EQUIPMENT, 216 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Dress": ItemData(EQUIPMENT, 134 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Quintar Sanctum, Advanced Zones
    "Equipment - Silk Shirt": ItemData(EQUIPMENT, 108 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Woven Shirt": ItemData(EQUIPMENT, 230 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2, Capital Jail, Advanced Zones
    "Equipment - Silver Cape": ItemData(EQUIPMENT, 519 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Artisan Shirt": ItemData(EQUIPMENT, 174 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Wizards Robe": ItemData(EQUIPMENT, 124 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Clerics Robe": ItemData(EQUIPMENT, 123 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Cosplay Garb": ItemData(EQUIPMENT, 336 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Sturdy Cape": ItemData(EQUIPMENT, 359 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Shelter Dress": ItemData(EQUIPMENT, 357 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3, Beaurior Rock, Expert Zones
    "Equipment - Gold Robe": ItemData(EQUIPMENT, 523 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Winter Cape": ItemData(EQUIPMENT, 325 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Blue Cape": ItemData(EQUIPMENT, 360 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Lands End, Expert Zones
    "Equipment - Seekers Garb": ItemData(EQUIPMENT, 324 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Slip Glide Ride, Expert Zones
    "Equipment - Ravens Cloak": ItemData(EQUIPMENT, 349 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4, Jidamba Tangle, Expert Zones
    "Equipment - Master Cape": ItemData(EQUIPMENT, 266 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Archmage Vest": ItemData(EQUIPMENT, 337 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, Ancient Labyrinth, End-Game Zones
    "Equipment - Saviors Cape": ItemData(EQUIPMENT, 338 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Assassins Cloak": ItemData(EQUIPMENT, 273 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The Depths, End-Game Zones
    "Equipment - Stealth Cape": ItemData(EQUIPMENT, 319 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5, The Sequoia, End-Game Zones
    "Equipment - Shell Gown": ItemData(EQUIPMENT, 355 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Diamond Robe": ItemData(EQUIPMENT, 241 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Cleric Robe": ItemData(EQUIPMENT, 547 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Wizard Robe": ItemData(EQUIPMENT, 549 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Shaman Robe": ItemData(EQUIPMENT, 550 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Scholar Robe": ItemData(EQUIPMENT, 551 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Chemist Robe": ItemData(EQUIPMENT, 552 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Dervish Robe": ItemData(EQUIPMENT, 553 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Weaver Robe": ItemData(EQUIPMENT, 554 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones
    "Equipment - Summoner Robe": ItemData(EQUIPMENT, 555 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier Class, Jade Cavern, Expert Zones

    #Accessories
    "Equipment - Fervor Charm": ItemData(EQUIPMENT, 48 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende, Beginner Zones
    "Equipment - Dodge Charm": ItemData(EQUIPMENT, 39 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Soiled Den, Beginner Zones
    "Equipment - Earring": ItemData(EQUIPMENT, 79 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende, Beginner Zones
    "Equipment - Bracer": ItemData(EQUIPMENT, 70 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende and Seaside Cliffs, Beginner Zones
    "Equipment - Jewel of Defense": ItemData(EQUIPMENT, 50 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Seaside Cliffs, Beginner Zones
    "Equipment - Scope Bit": ItemData(EQUIPMENT, 226 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Seaside Cliffs and Quintar Nest, Beginner Zones
    "Equipment - Protect Amulet": ItemData(EQUIPMENT, 49 + equipment_index_offset, ItemClassification.useful), #Tier 1 Shop, Delende, Beginner Zones
    "Equipment - Wasps Stinger": ItemData(EQUIPMENT, 86 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Gem Ring": ItemData(EQUIPMENT, 332 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Earth Bangle": ItemData(EQUIPMENT, 82 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Water Bangle": ItemData(EQUIPMENT, 83 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Looters Ring": ItemData(EQUIPMENT, 54 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Delende and Greenshire Reprise, Beginner Zones
    "Equipment - Burglars Glove": ItemData(EQUIPMENT, 53 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Spawning Meadows and Proving Meadows, Beginner Zones
    "Equipment - Torpid Cuffs": ItemData(EQUIPMENT, 331 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Yamagawa M.A., Beginner Zones
    "Equipment - Squirrel Dung": ItemData(EQUIPMENT, 85 + equipment_index_offset, ItemClassification.useful), #Tier 1 Unique, Spawning Meadows, Beginner Zones
    "Equipment - Fang Pendant": ItemData(EQUIPMENT, 196 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Shop (Capital), Capital Sequoia, Advanced Zones
    "Equipment - Mana Ring": ItemData(EQUIPMENT, 38 + equipment_index_offset, ItemClassification.useful), #Tier 2 Shop (Capital), Skumparadise, Beginner Zones
    "Equipment - Awake Ring": ItemData(EQUIPMENT, 87 + equipment_index_offset, ItemClassification.useful), #Tier 2 Shop (Capital), Skumparadise, Beginner Zones
    "Equipment - Prayer Beads": ItemData(EQUIPMENT, 186 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Shell Amulet": ItemData(EQUIPMENT, 179 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Shop (Capital), Greenshire Reprise, Advanced Zones
    "Equipment - Samurais Glove": ItemData(EQUIPMENT, 185 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 2, Shop, Advanced Zones
    "Equipment - Magic Finder": ItemData(EQUIPMENT, 323 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Loot, Okimoto N.S., Advanced Zones
    "Equipment - Learners Pin": ItemData(EQUIPMENT, 492 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Givers Ring": ItemData(EQUIPMENT, 182 + equipment_index_offset, ItemClassification.useful, 0, 1),#Tier 2 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Aggro Band": ItemData(EQUIPMENT, 505 + equipment_index_offset, ItemClassification.useful, 0, 1), #Delende fisher; Tier 2 Unique, Delende, Advanced Zones
    "Equipment - Hemoring": ItemData(EQUIPMENT, 56 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Float Shoes": ItemData(EQUIPMENT, 193 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 2 Unique, Okimoto N.S. and Lake Delende, Advanced Zones
    "Equipment - Hope Cross": ItemData(EQUIPMENT, 225 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Defense Shifter": ItemData(EQUIPMENT, 191 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Shop (Sara Sara), Ancient Reservoir, Advanced Zones
    "Equipment - Resist Shifter": ItemData(EQUIPMENT, 221 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Shop (Sara Sara), Ancient Reservoir, Advanced Zones
    "Equipment - Casters Ring": ItemData(EQUIPMENT, 9 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Fearsome Ring": ItemData(EQUIPMENT, 504 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Crit Fang": ItemData(EQUIPMENT, 502 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Dancing Shoes": ItemData(EQUIPMENT, 333 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Advanced Zones
    "Equipment - Bulk Belt": ItemData(EQUIPMENT, 243 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Poison Talon": ItemData(EQUIPMENT, 334 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - First Strike Mitt": ItemData(EQUIPMENT, 501 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Menders Ring": ItemData(EQUIPMENT, 529 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Kitsune Mask": ItemData(EQUIPMENT, 503 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Pact Ring": ItemData(EQUIPMENT, 496 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 3, Shop, Expert Zones
    "Equipment - Scope Specs": ItemData(EQUIPMENT, 562 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 3 Loot, Poko Poko Desert, Advanced Zones
    "Equipment - Loot Finder": ItemData(EQUIPMENT, 326 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Quiet Shoes": ItemData(EQUIPMENT, 495 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Knicked Knackers": ItemData(EQUIPMENT, 232 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Unique, Shoudu Province, Expert Zones
    "Equipment - Looters Pin": ItemData(EQUIPMENT, 231 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Unique, Shoudu Province, Expert Zones
    "Equipment - Acrobat Shoes": ItemData(EQUIPMENT, 320 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 3 Unique, Shoudu Province, Expert Zones
    "Equipment - Bone Trophy": ItemData(EQUIPMENT, 37 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Gusto Fang": ItemData(EQUIPMENT, 47 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Beads of Defense": ItemData(EQUIPMENT, 328 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 4 Shop (Tall Tall), Castle Sequoia, End-Game Zones
    "Equipment - Winter Mitten": ItemData(EQUIPMENT, 322 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 0, 0, 0, 1), #Tier 4, Shop, Expert Zones
    "Equipment - Glasses": ItemData(EQUIPMENT, 327 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tall Tall Heights fisher; Tier 4 Unique, Tall Tall Heights, Expert Zones
    "Equipment - Gusto Charm": ItemData(EQUIPMENT, 46 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tall Tall Heights fisher; Tier 4 Unique, Tall Tall Heights, Expert Zones
    "Equipment - Muggers Glove": ItemData(EQUIPMENT, 309 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 4 Unique, Shoudu Province, Expert Zones
    "Equipment - Fursuit": ItemData(EQUIPMENT, 490 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #crafted but i think its funny; Tier 5 Crafting, Quintar Reserve, Expert Zones
    "Equipment - Snow Pendant": ItemData(EQUIPMENT, 528 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Ogre Ball": ItemData(EQUIPMENT, 78 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Sanity Ring": ItemData(EQUIPMENT, 330 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5 Unique, The Open Sea, Expert Zones
    "Equipment - Undead Ring": ItemData(EQUIPMENT, 491 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, Quintar Reserve, Expert Zones
    "Equipment - Fairys Ring": ItemData(EQUIPMENT, 329 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5 Unique, The Open Sea, Expert Zones
    "Equipment - Oven Mitt": ItemData(EQUIPMENT, 321 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, The Deep Sea, Expert Zones
    "Equipment - Autumns Oath": ItemData(EQUIPMENT, 234 + equipment_index_offset, ItemClassification.useful), #Tier 5 Unique, Yamagawa M.A., Beginner Zones
    "Equipment - Springs Oath": ItemData(EQUIPMENT, 489 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Overpass (Okimoto N.S.), Advanced Zones
    "Equipment - Lucky Socks": ItemData(EQUIPMENT, 498 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Lucky Briefs": ItemData(EQUIPMENT, 499 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Capital Sequoia, Advanced Zones
    "Equipment - Tall Stand Ring": ItemData(EQUIPMENT, 244 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, Shoudu Province, Expert Zones
    "Equipment - Nomads Emblem": ItemData(EQUIPMENT, 287 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #The Open Sea fisher; Tier 5 Unique, The Open Sea, Expert Zones
    "Equipment - Lockon Lense": ItemData(EQUIPMENT, 373 + equipment_index_offset, ItemClassification.useful, 0), #Quintar Enthusiast battle drop
    "Equipment - Red Hairpin": ItemData(EQUIPMENT, 247 + equipment_index_offset, ItemClassification.useful), #Delende fisher;  #Tier 5 Unique, Delende, Beginner Zones
    "Equipment - Stone of Jodan": ItemData(EQUIPMENT, 286 + equipment_index_offset, ItemClassification.useful, 0, 1), #Tier 5 Unique, Jojo Sewers, Advanced Zones
    "Equipment - Ribbon": ItemData(EQUIPMENT, 346 + equipment_index_offset, ItemClassification.useful, 0, 0, 1), #Tier 5 Unique, Shoudu Province, Expert Zones
    "Equipment - Hand of Midas": ItemData(EQUIPMENT, 494 + equipment_index_offset, ItemClassification.useful, 0, 0, 0, 1), #Tier 5 Unique, The Sequoia, End-Game Zones
    "Equipment - Ghendolfs Ring": ItemData(EQUIPMENT, 242 + equipment_index_offset, ItemClassification.useful, 0),
    "Equipment - Master Material": ItemData(EQUIPMENT, 284 + equipment_index_offset, ItemClassification.useful, 0),

    #Progressive Equipment
    #the highest equipment id is 590 so these ids start at 600
    #Shopsanity ids are in brackets in the lists at the end
    "Equipment - Progressive 1H Sword": ItemData(EQUIPMENT, 900 + equipment_index_offset, ItemClassification.useful, 4, 1, 7, 1, 1, 4, 1, 0), #1H Sword IDs [0], 11, 71, 89, 93, 200, [199], [157], [379], 377, 375, 380, [374], 372, 381, [248], 303, 411, 316
    "Equipment - Progressive 2H Sword": ItemData(EQUIPMENT, 901 + equipment_index_offset, ItemClassification.useful, 1, 2, 2, 1, 0, 3, 1, 0), # 2H Sword IDs 12, [378], 177, [376], 197, 525, [370], 382, [249], 279
    "Equipment - Progressive 1H Axe": ItemData(EQUIPMENT, 902 + equipment_index_offset, ItemClassification.useful, 0, 3, 0, 1, 1, 1, 0, 0), # 1H Axe IDs [55], 94, 187, 386, [251], 388
    "Equipment - Progressive 2H Axe": ItemData(EQUIPMENT, 903 + equipment_index_offset, ItemClassification.useful, 1, 1, 1, 1, 1, 5, 2, 0), # 2H Axe IDs 2, [66], [201], [383], [158], [384], [390], 385, [391], [250], 280, 274
    "Equipment - Progressive Dagger": ItemData(EQUIPMENT, 904 + equipment_index_offset, ItemClassification.useful, 3, 3, 2, 1, 3, 4, 2, 0), # Dagger IDs [3], 63, [77], 40, [60], 95, [202], 184, [204], [159], 198, 305, [526], 393, [394], 72, [269], 306
    "Equipment - Progressive Ninja Dagger": ItemData(EQUIPMENT, 905 + equipment_index_offset, ItemClassification.useful, 0, 3, 1, 1, 0, 1, 2, 0), # Ninja Dagger IDs 192, 203, 397, [392], [396], [400], 317, 318
    "Equipment - Progressive Rapier": ItemData(EQUIPMENT, 906 + equipment_index_offset, ItemClassification.useful, 2, 3, 3, 1, 2, 5, 2, 0), # Rapier IDs [73], [1], 42, 96, [207], [206], 175, [160], 10, [402], [408], 404, [405], 407, [252], 401, 403, 406
    "Equipment - Progressive Katana": ItemData(EQUIPMENT, 907 + equipment_index_offset, ItemClassification.useful, 1, 1, 1, 0, 0, 3, 4, 0), # Katana IDs 97, 399, [161], [363], [22], [364], [23], [366], [253], 367
    "Equipment - Progressive Spear": ItemData(EQUIPMENT, 908 + equipment_index_offset, ItemClassification.useful, 1, 3, 3, 1, 0, 5, 1, 0), # Spear IDs [4], 98, [205], 190, 183, [162], 409, [410], 418, [419], 417, 416, [254], 275
    "Equipment - Progressive Scythe": ItemData(EQUIPMENT, 909 + equipment_index_offset, ItemClassification.useful, 1, 2, 3, 0, 0, 4, 1, 0), # Scythe IDs 6, 99, [208], [163], [294], 293, [295], 414, 415, 590, [255]
    "Equipment - Progressive Bow": ItemData(EQUIPMENT, 910 + equipment_index_offset, ItemClassification.useful, 1, 1, 2, 1, 0, 5, 4), # Bow IDs 105, [7], 181, [209], [164], [297], [296], [298], [300], 301, 299, [256], [281], 420
    "Equipment - Progressive Staff": ItemData(EQUIPMENT, 911 + equipment_index_offset, ItemClassification.useful, 1, 2, 4, 1, 2, 5, 0, 0), # Staff IDs [5], 62, [15], 100, [210], 188, [211], [165], [423], 422, 424, 425, [257], 290, 429
    "Equipment - Progressive Beating Staff": ItemData(EQUIPMENT, 912 + equipment_index_offset, ItemClassification.useful, 1, 2, 0, 0, 0, 1, 2, 0), # Beating Staff IDs 14, 426, 335, [427], [67], [428]
    "Equipment - Progressive Wand": ItemData(EQUIPMENT, 913 + equipment_index_offset, ItemClassification.useful, 2, 3, 5, 0, 2, 5, 2, 0), # Wand IDs [8], 13, [16], 64, 101, [213], 189, [212], [166], 267, [434], 432, [433], 435, [431], 430, [258], 276, 358
    "Equipment - Progressive Book": ItemData(EQUIPMENT, 914 + equipment_index_offset, ItemClassification.useful, 1, 4, 3, 0, 1, 5, 2, 0), # Book IDs [51], [65], 102, [214], 194, 223, 224, [167], [438], 437, 439, [441], 440, [442], 443, [259] (with shopsanity on i graduated craftwork to advanced)
    "Equipment - Progressive Shield": ItemData(EQUIPMENT, 915 + equipment_index_offset, ItemClassification.useful, 3, 4, 5, 1, 1, 5, 4, 0), # Shield IDs [44], 45, 68, 88, 506, [111], [215], 103, 178, [168], [444], [448], 451, [446], 452, [449], 450, 453, [260], [445], 344, 288, 246
    "Equipment - Progressive Heavy Head": ItemData(EQUIPMENT, 916 + equipment_index_offset, ItemClassification.useful, 1, 3, 4, 0, 3, 5, 2, 0), # Heavy Head IDs [25], [26], 74, [69], 508, [106], [128], 125, 132, [169], [465], [468], 464, [466], 470, 467, [261], 292
    "Equipment - Progressive Heavy Body": ItemData(EQUIPMENT, 917 + equipment_index_offset, ItemClassification.useful, 1, 4, 14, 1, 2, 5, 2, 0), # Heavy Body IDs [18], 28, [29], 84, 510, [107], [127], 126, 43, [170], [455], [460], 456, 462, 461, 130, [457], 458, [262], 131, 463, 533, 534, 536, 535, 538, 537, 557, 548
    "Equipment - Progressive Medium Head": ItemData(EQUIPMENT, 918 + equipment_index_offset, ItemClassification.useful, 2, 4, 2, 1, 2, 5, 3, 0), # Medium Head IDs [24], [27], 75, 30, 512, [219], 195, [220], [171], [483], 233, [484], 485, 481, [486], [263], 345, 482, [487]
    "Equipment - Progressive Medium Body": ItemData(EQUIPMENT, 919 + equipment_index_offset, ItemClassification.useful, 1, 4, 12, 0, 2, 6, 3, 0), # Medium Body IDs [17], [35], [36], 514, [217], [218], 268, 229, 176, [172], [472], 57, [474], 473, 477, [478], 479, [264], [493], 347, 539, 540, 541, 542, 543, 544, 545, 546  (with shopsanity on i graduated craftwork to advanced)
    "Equipment - Progressive Light Head": ItemData(EQUIPMENT, 920 + equipment_index_offset, ItemClassification.useful, 2, 3, 6, 2, 2, 5, 3, 0), # Light Head IDs [31], 32, 76, [33], 516, [110], 133, [109], 122, [173], [341], [340], [353], 342, 356, 34, [343], 348, 52, [265], 531, 271, 354
    "Equipment - Progressive Light Body": ItemData(EQUIPMENT, 921 + equipment_index_offset, ItemClassification.useful, 2, 3, 12, 3, 2, 5, 3, 0), # Light Body IDs [19], [20], 21, 81, 518, [216], 134, [108], 230, [174], [124], [123], [359], 357, [325], 360, 324, 349, [266], 337, 273, 319, 547, 549, 550, 551, 552, 553, 554, 555

    #Maps
    #Beginner
    SPAWNING_MEADOWS_MAP: ItemData(MAP, 73 + item_index_offset, ItemClassification.useful),
    DELENDE_MAP: ItemData(MAP, 74 + item_index_offset, ItemClassification.useful),
    BASEMENT_MAP: ItemData(MAP, 213 + item_index_offset, ItemClassification.useful),
    MERCURY_SHRINE_MAP: ItemData(MAP, 87 + item_index_offset, ItemClassification.useful),
    SOILED_DEN_MAP: ItemData(MAP, 79 + item_index_offset, ItemClassification.useful),
    THE_PALE_GROTTO_MAP: ItemData(MAP, 75 + item_index_offset, ItemClassification.useful),
    SEASIDE_CLIFFS_MAP: ItemData(MAP, 76 + item_index_offset, ItemClassification.useful),
    DRAFT_SHAFT_CONDUIT_MAP: ItemData(MAP, 77 + item_index_offset, ItemClassification.useful),
    YAMAGAWA_MA_MAP: ItemData(MAP, 80 + item_index_offset, ItemClassification.useful),
    PROVING_MEADOWS_MAP: ItemData(MAP, 78 + item_index_offset, ItemClassification.useful),
    TRIAL_CAVES_MAP: ItemData(MAP, 214 + item_index_offset, ItemClassification.useful),
    SKUMPARADISE_MAP: ItemData(MAP, 82 + item_index_offset, ItemClassification.useful),
    #Advanced
    CAPITAL_COURTYARD_MAP: ItemData(MAP, 83 + item_index_offset, ItemClassification.useful, 0, 1),
    CAPITAL_SEQUOIA_MAP: ItemData(MAP, 84 + item_index_offset, ItemClassification.useful, 0, 1),
    JOJO_SEWERS_MAP: ItemData(MAP, 85 + item_index_offset, ItemClassification.useful, 0, 1),
    BOOMER_SOCIETY_MAP: ItemData(MAP, 89 + item_index_offset, ItemClassification.useful, 0, 1),
    ROLLING_QUINTAR_FIELDS_MAP: ItemData(MAP, 90 + item_index_offset, ItemClassification.useful, 0, 1),
    QUINTAR_NEST_MAP: ItemData(MAP, 92 + item_index_offset, ItemClassification.useful, 0, 1),
    QUINTAR_SANCTUM_MAP: ItemData(MAP, 120 + item_index_offset, ItemClassification.useful, 0, 1),
    CAPITAL_JAIL_MAP: ItemData(MAP, 94 + item_index_offset, ItemClassification.useful, 0, 1),
    CAPITAL_PIPELINE_MAP: ItemData(MAP, 170 + item_index_offset, ItemClassification.useful, 0, 1),
    COBBLESTONE_CRAG_MAP: ItemData(MAP, 96 + item_index_offset, ItemClassification.useful, 0, 1),
    OKIMOTO_NS_MAP: ItemData(MAP, 98 + item_index_offset, ItemClassification.useful, 0, 1),
    GREENSHIRE_REPRISE_MAP: ItemData(MAP, 86 + item_index_offset, ItemClassification.useful, 0, 1),
    SALMON_PASS_MAP: ItemData(MAP, 99 + item_index_offset, ItemClassification.useful, 0, 1),
    SALMON_RIVER_MAP: ItemData(MAP, 100 + item_index_offset, ItemClassification.useful, 0, 1),
    POSEIDON_SHRINE_MAP: ItemData(MAP, 101 + item_index_offset, ItemClassification.useful, 0, 1),
    RIVER_CATS_EGO_MAP: ItemData(MAP, 217 + item_index_offset, ItemClassification.useful, 0, 1),
    POKO_POKO_DESERT_MAP: ItemData(MAP, 103 + item_index_offset, ItemClassification.useful, 0, 1),
    SARA_SARA_BAZAAR_MAP: ItemData(MAP, 104 + item_index_offset, ItemClassification.useful, 0, 1),
    SARA_SARA_BEACH_MAP: ItemData(MAP, 105 + item_index_offset, ItemClassification.useful, 0, 1),
    ANCIENT_RESERVOIR_MAP: ItemData(MAP, 106 + item_index_offset, ItemClassification.useful, 0, 1),
    SALMON_BAY_MAP: ItemData(MAP, 128 + item_index_offset, ItemClassification.useful, 0, 1),
    OVERPASS_MAP: ItemData(MAP, 215 + item_index_offset, ItemClassification.useful), #in Beginner bc of Yamagawa (and Regionsanity expects you to have it unlocked at the start)
    UNDERPASS_MAP: ItemData(MAP, 216 + item_index_offset, ItemClassification.useful), #in Beginner bc of Delende (and Regionsanity expects you to have it unlocked at the start)
    #Expert
    THE_OPEN_SEA_MAP: ItemData(MAP, 198 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    SHOUDU_PROVINCE_MAP: ItemData(MAP, 107 + item_index_offset, ItemClassification.useful, 0, 1),  #in Advanced for Shoudu Waterfront
    THE_UNDERCITY_MAP: ItemData(MAP, 108 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    GANYMEDE_SHRINE_MAP: ItemData(MAP, 117 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    BEAURIOR_VOLCANO_MAP: ItemData(MAP, 109 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    BEAURIOR_ROCK_MAP: ItemData(MAP, 110 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    LAKE_DELENDE_MAP: ItemData(MAP, 121 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    QUINTAR_RESERVE_MAP: ItemData(MAP, 119 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    DIONE_SHRINE_MAP: ItemData(MAP, 199 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    FLYERS_LOOKOUT_MAP: ItemData(MAP, 223 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    QUINTAR_MAUSOLEUM_MAP: ItemData(MAP, 211 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    EASTERN_CHASM_MAP: ItemData(MAP, 219 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    TALL_TALL_HEIGHTS_MAP: ItemData(MAP, 112 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    NORTHERN_CAVE_MAP: ItemData(MAP, 194 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    LANDS_END_MAP: ItemData(MAP, 130 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    SLIP_GLIDE_RIDE_MAP: ItemData(MAP, 113 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    SEQUOIA_ATHENAEUM_MAP: ItemData(MAP, 220 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    NORTHERN_STRETCH_MAP: ItemData(MAP, 218 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    CASTLE_RAMPARTS_MAP: ItemData(MAP, 127 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    THE_CHALICE_OF_TAR_MAP: ItemData(MAP, 221 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    FLYERS_CRAG_MAP: ItemData(MAP, 222 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    JIDAMBA_TANGLE_MAP: ItemData(MAP, 122 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    JIDAMBA_EACLANEYA_MAP: ItemData(MAP, 123 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    THE_DEEP_SEA_MAP: ItemData(MAP, 124 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    NEPTUNE_SHRINE_MAP: ItemData(MAP, 206 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    JADE_CAVERN_MAP: ItemData(MAP, 228 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    CONTINENTAL_TRAM_MAP: ItemData(MAP, 126 + item_index_offset, ItemClassification.useful, 0, 0, 1),
    #End-Game
    ANCIENT_LABYRINTH_MAP: ItemData(MAP, 210 + item_index_offset, ItemClassification.useful, 0, 0, 0, 1),
    THE_SEQUOIA_MAP: ItemData(MAP, 111 + item_index_offset, ItemClassification.useful, 0, 0, 0, 1),
    THE_DEPTHS_MAP: ItemData(MAP, 195 + item_index_offset, ItemClassification.useful, 0, 0, 0, 1),
    CASTLE_SEQUOIA_MAP: ItemData(MAP, 209 + item_index_offset, ItemClassification.useful, 0, 0, 0, 1),
    THE_OLD_WORLD_MAP: ItemData(MAP, 254 + item_index_offset, ItemClassification.useful, 0, 0, 0, 1), #if player is on True Astley goal, get_item_pool in init adds this if you didn't pick to include End-Game Regions
    THE_NEW_WORLD_MAP: ItemData(MAP, 125 + item_index_offset, ItemClassification.useful, 0, 0, 0, 1), #if player is on Astley/True Astley goal, get_item_pool in init adds this if you didn't pick to include End-Game Regions

    # Teleport Shards
    "Item - Gaea Shard": ItemData(TELEPORT_SHARD, 22 + item_index_offset, ItemClassification.useful, 0),
    "Item - Mercury Shard": ItemData(TELEPORT_SHARD, 12 + item_index_offset, ItemClassification.useful, 0),
    "Item - Poseidon Shard": ItemData(TELEPORT_SHARD, 56 + item_index_offset, ItemClassification.useful, 0),
    "Item - Mars Shard": ItemData(TELEPORT_SHARD, 58 + item_index_offset, ItemClassification.useful, 0),
    "Item - Ganymede Shard": ItemData(TELEPORT_SHARD, 62 + item_index_offset, ItemClassification.useful, 0),
    "Item - Triton Shard": ItemData(TELEPORT_SHARD, 63 + item_index_offset, ItemClassification.useful, 0),
    "Item - Callisto Shard": ItemData(TELEPORT_SHARD, 154 + item_index_offset, ItemClassification.useful, 0),
    "Item - Europa Shard": ItemData(TELEPORT_SHARD, 61 + item_index_offset, ItemClassification.useful, 0),
    "Item - Dione Shard": ItemData(TELEPORT_SHARD, 165 + item_index_offset, ItemClassification.useful, 0),
    "Item - Neptune Shard": ItemData(TELEPORT_SHARD, 207 + item_index_offset, ItemClassification.useful, 0),
    "Item - New World Shard": ItemData(TELEPORT_SHARD, 139 + item_index_offset, ItemClassification.useful, 0),
    "Item - Old World Shard": ItemData(TELEPORT_SHARD, 252 + item_index_offset, ItemClassification.useful, 0),

    #Seeds
    "Item - Sketchy Seed": ItemData(ITEM, 178 + item_index_offset, ItemClassification.filler, 0),
    "Item - Tuber Seed": ItemData(ITEM, 179 + item_index_offset, ItemClassification.filler, 0),
    "Item - Spore Seed": ItemData(ITEM, 180 + item_index_offset, ItemClassification.filler, 0),
    "Item - Gourmet Seed": ItemData(ITEM, 181 + item_index_offset, ItemClassification.filler, 0),
    "Item - Fetish Seed": ItemData(ITEM, 182 + item_index_offset, ItemClassification.filler, 0),
    "Item - Tear Seed": ItemData(ITEM, 187 + item_index_offset, ItemClassification.filler, 0),
    "Item - Colony Seed": ItemData(ITEM, 188 + item_index_offset, ItemClassification.filler, 0),
    "Item - Watery Seed": ItemData(ITEM, 189 + item_index_offset, ItemClassification.filler, 0),
    "Item - Bloody Seed": ItemData(ITEM, 190 + item_index_offset, ItemClassification.filler, 0),
    "Item - Dark Seed": ItemData(ITEM, 183 + item_index_offset, ItemClassification.filler, 0),

    #Seals
    "Equipment - Warrior Seal": ItemData(EQUIPMENT, 564 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Monk Seal": ItemData(EQUIPMENT, 565 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Rogue Seal": ItemData(EQUIPMENT, 566 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Cleric Seal": ItemData(EQUIPMENT, 567 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Wizard Seal": ItemData(EQUIPMENT, 568 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Warlock Seal": ItemData(EQUIPMENT, 569 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Fencer Seal": ItemData(EQUIPMENT, 570 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Shaman Seal": ItemData(EQUIPMENT, 571 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Scholar Seal": ItemData(EQUIPMENT, 572 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Aegis Seal": ItemData(EQUIPMENT, 573 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Hunter Seal": ItemData(EQUIPMENT, 574 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Chemist Seal": ItemData(EQUIPMENT, 575 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Reaper Seal": ItemData(EQUIPMENT, 576 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Ninja Seal": ItemData(EQUIPMENT, 577 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Nomad Seal": ItemData(EQUIPMENT, 578 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Dervish Seal": ItemData(EQUIPMENT, 579 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Beatsmith Seal": ItemData(EQUIPMENT, 580 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Samurai Seal": ItemData(EQUIPMENT, 581 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Assassin Seal": ItemData(EQUIPMENT, 582 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Valkyrie Seal": ItemData(EQUIPMENT, 583 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Weaver Seal": ItemData(EQUIPMENT, 584 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Summoner Seal": ItemData(EQUIPMENT, 585 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Beastmaster Seal": ItemData(EQUIPMENT, 586 + equipment_index_offset, ItemClassification.filler, 0),
    "Equipment - Mimic Seal": ItemData(EQUIPMENT, 587 + equipment_index_offset, ItemClassification.filler, 0),

    #Quintar Raising
    "Item - Quintar Grass": ItemData(ITEM, 157 + item_index_offset, ItemClassification.filler, 0),
    "Item - Quintar Wheat": ItemData(ITEM, 202 + item_index_offset, ItemClassification.filler, 0),
    "Item - Quintar Berries": ItemData(ITEM, 203 + item_index_offset, ItemClassification.filler, 0),
    "Item - Quintar Cheese": ItemData(ITEM, 204 + item_index_offset, ItemClassification.filler, 0),
    "Item - Quintar Cookie": ItemData(ITEM, 205 + item_index_offset, ItemClassification.filler, 0),
    "Item - Name Tag": ItemData(ITEM, 200 + item_index_offset, ItemClassification.filler, 0),
    "Item - Incubator": ItemData(ITEM, 201 + item_index_offset, ItemClassification.filler, 0),

    #Currency
    #"Currency": ItemData("Currency", 0 + index_offset, ItemClassification.filler),

    #Summons
    SHAKU_SUMMON: ItemData(SUMMON, 223 + summon_index_offset, ItemClassification.useful),
    PAMOA_SUMMON: ItemData(SUMMON, 224 + summon_index_offset, ItemClassification.useful),
    GUABA_SUMMON: ItemData(SUMMON, 225 + summon_index_offset, ItemClassification.useful),
    NILTSI_SUMMON: ItemData(SUMMON, 226 + summon_index_offset, ItemClassification.useful),
    IOSKE_SUMMON: ItemData(SUMMON, 227 + summon_index_offset, ItemClassification.useful),
    COYOTE_SUMMON: ItemData(SUMMON, 228 + summon_index_offset, ItemClassification.useful),
    "Summon - Pinga": ItemData(SUMMON, 230 + summon_index_offset, ItemClassification.useful, 0), #(0 in pool bc you start with Pinga as a summoner)
    TIRA_SUMMON: ItemData(SUMMON, 231 + summon_index_offset, ItemClassification.useful),
    JUSES_SUMMON: ItemData(SUMMON, 232 + summon_index_offset, ItemClassification.useful),
    PAH_SUMMON: ItemData(SUMMON, 234 + summon_index_offset, ItemClassification.useful),

    #Monster Abilities for Scholar
    ROOST: ItemData(SCHOLAR_ABILITY, 25 + scholar_index_offset, ItemClassification.useful, 0, 1),
    LUCKY_DICE: ItemData(SCHOLAR_ABILITY, 70 + scholar_index_offset, ItemClassification.useful, 0, 1),
    SUN_BATH: ItemData(SCHOLAR_ABILITY, 101 + scholar_index_offset, ItemClassification.useful, 0, 1),
    SLEEP_AURA: ItemData(SCHOLAR_ABILITY, 186 + scholar_index_offset, ItemClassification.useful, 0, 1),
    REGENERATE: ItemData(SCHOLAR_ABILITY, 197 + scholar_index_offset, ItemClassification.useful, 0, 1),
    REVERSE_POLARITY: ItemData(SCHOLAR_ABILITY, 198 + scholar_index_offset, ItemClassification.progression), #left in pool so you can merc Gran
    BARRIER: ItemData(SCHOLAR_ABILITY, 199 + scholar_index_offset, ItemClassification.useful, 0, 1),
    MP_SICKLE: ItemData(SCHOLAR_ABILITY, 200 + scholar_index_offset, ItemClassification.useful, 0, 1),
    ADRENALINE: ItemData(SCHOLAR_ABILITY, 202 + scholar_index_offset, ItemClassification.useful, 0, 1),
    FIRE_BREATH: ItemData(SCHOLAR_ABILITY, 205 + scholar_index_offset, ItemClassification.useful, 0, 1),
    EXPLODE: ItemData(SCHOLAR_ABILITY, 206 + scholar_index_offset, ItemClassification.useful, 0, 1),
    WHIRLWIND: ItemData(SCHOLAR_ABILITY, 207 + scholar_index_offset, ItemClassification.useful, 0, 1),
    ATMOSHEAR: ItemData(SCHOLAR_ABILITY, 213 + scholar_index_offset, ItemClassification.useful, 0, 1),
    BUILD_LIFE: ItemData(SCHOLAR_ABILITY, 245 + scholar_index_offset, ItemClassification.useful, 0, 1),
    AERO: ItemData(SCHOLAR_ABILITY, 264 + scholar_index_offset, ItemClassification.useful, 0, 1),
    INSULT: ItemData(SCHOLAR_ABILITY, 363 + scholar_index_offset, ItemClassification.useful, 0, 1),
    INFUSION: ItemData(SCHOLAR_ABILITY, 364 + scholar_index_offset, ItemClassification.useful, 0, 1),
    OVERlOAD: ItemData(SCHOLAR_ABILITY, 365 + scholar_index_offset, ItemClassification.useful, 0, 1),
    REFLECTION: ItemData(SCHOLAR_ABILITY, 366 + scholar_index_offset, ItemClassification.useful, 0, 1),
    LIFEGIVER: ItemData(SCHOLAR_ABILITY, 376 + scholar_index_offset, ItemClassification.useful, 0, 1),

    #Traps
    "Trap - Dialog Trap": ItemData(TRAP, 1 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Crag Demon Trap": ItemData(TRAP, 2 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Clothes Fall Off Trap": ItemData(TRAP, 3 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Oregon Trap": ItemData(TRAP, 4 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Teleport Trap": ItemData(TRAP, 5 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Moon Jump Trap": ItemData(TRAP, 6 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Snail Jump Trap": ItemData(TRAP, 7 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Dismount Trap": ItemData(TRAP, 8 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Dunk Tank Trap": ItemData(TRAP, 9 + trap_index_offset, ItemClassification.trap, 0),
    "Trap - Trap Pack Trap": ItemData(TRAP, 10 + trap_index_offset, ItemClassification.trap, 0),
}

progressive_equipment: Tuple[str, ...] = (
    "Equipment - Progressive 1H Sword",
    "Equipment - Progressive 2H Sword",
    "Equipment - Progressive 1H Axe",
    "Equipment - Progressive 2H Axe",
    "Equipment - Progressive Dagger",
    "Equipment - Progressive Ninja Dagger",
    "Equipment - Progressive Rapier",
    "Equipment - Progressive Katana",
    "Equipment - Progressive Spear",
    "Equipment - Progressive Scythe",
    "Equipment - Progressive Bow",
    "Equipment - Progressive Staff",
    "Equipment - Progressive Beating Staff",
    "Equipment - Progressive Wand",
    "Equipment - Progressive Book",
    "Equipment - Progressive Shield",
    "Equipment - Progressive Heavy Head",
    "Equipment - Progressive Heavy Body",
    "Equipment - Progressive Medium Head", 
    "Equipment - Progressive Medium Body", 
    "Equipment - Progressive Light Head",
    "Equipment - Progressive Light Body",
    )

non_progressive_equipment: Tuple[str, ...] = (
    #Weapons
    #Swords
    "Equipment - Iron Sword",
    "Equipment - Contract",
    "Equipment - Help the Prince",
    "Equipment - Craftwork Sword",
    "Equipment - Broadsword",
    "Equipment - Sharp Sword",
    #"Equipment - Silver Sword",
    "Equipment - Boomer Sword",
    #"Equipment - Digested Sword",
    "Equipment - Cutlass",
    "Equipment - Cold Touch",
    #"Equipment - Burning Blade",
    #"Equipment - Gold Sword",
    "Equipment - Bloodbind",
    "Equipment - Temporal Blade",
    #"Equipment - Hydra Edge",
    "Equipment - Defender",
    "Equipment - Conquest",
    "Equipment - Flame Sword",
    "Equipment - Rune Sword",
    #"Equipment - Auduril",
    #"Equipment - Training Sword",
    #"Equipment - Life Line",
    "Equipment - Soul Keeper",
    "Equipment - Crabs Claw",
    "Equipment - Kings Guard",
    #"Equipment - Diamond Sword",
    #"Equipment - Balrog",
    "Equipment - Oily Sword",

    #Axes
    "Equipment - Craftwork Axe",
    "Equipment - Cleaver",
    "Equipment - Hunting Axe",
    #"Equipment - Silver Axe",
    "Equipment - Hatchet",
    #"Equipment - Axe of Light",
    #"Equipment - Gold Axe",
    "Equipment - Gaia Axe",
    #"Equipment - Ancient Axe",
    #"Equipment - Master Bigaxe",
    "Equipment - Aphotic Edge",
    #"Equipment - Diamond Axe",
    "Equipment - Decapitator",
    "Equipment - Ragebringer",

    #Daggers
    "Equipment - Stabbers",
    "Equipment - Poisonkiss",
    "Equipment - Craftwork Dagger",
    "Equipment - Tanto",
    "Equipment - Butterfly",
    "Equipment - Ambush Knife",
    #"Equipment - Silver Dagger",
    "Equipment - Parry Knife",
    "Equipment - Butter Cutter",
    "Equipment - Soul Kris",
    #"Equipment - Gouger",
    "Equipment - Cinquedea",
    #"Equipment - Gold Dagger",
    #"Equipment - Kowakizashi",
    #"Equipment - Bone Knife",
    "Equipment - Flamespike",
    "Equipment - Sange",
    "Equipment - Yasha",
    #"Equipment - Legend Spike",
    #"Equipment - Eclipse",
    #"Equipment - Mage Masher",
    "Equipment - Mages Pike",
    #"Equipment - Diamond Dagger",

    #Rapiers
    "Equipment - Toothpick",
    "Equipment - Craftwork Rapier",
    "Equipment - Fish Skewer",
    #"Equipment - Silver Rapier",
    "Equipment - Dueller",
    "Equipment - Fleuret",
    #"Equipment - Gold Rapier",
    "Equipment - Windsong",
    "Equipment - Nightingale",
    "Equipment - Chartreuse",
    "Equipment - Murgleys",
    #"Equipment - Diamond Rapier",

    #Katanas
    "Equipment - Craftwork Katana",
    "Equipment - Tachi",
    #"Equipment - Silver Katana",
    #"Equipment - Gold Katana",
    #"Equipment - Hokuken",
    #"Equipment - Ichimonji",
    "Equipment - Muramasa",
    #"Equipment - Diamond Katana",

    #Spears
    "Equipment - Craftwork Spear",
    "Equipment - Skewer",
    "Equipment - Prodder",
    #"Equipment - Silver Spear",
    "Equipment - Trident",
    "Equipment - Halberd",
    #"Equipment - Gold Spear",
    "Equipment - Radiance",
    "Equipment - Partizan",
    #"Equipment - Incursier",
    "Equipment - Royal Guard",
    #"Equipment - Gungnir",
    #"Equipment - Diamond Spear",

    #Scythes
    "Equipment - Battle Scythe",
    "Equipment - Craftwork Scythe",
    #"Equipment - Wind Sickle",
    #"Equipment - Silver Scythe",
    "Equipment - Grim Scythe",
    "Equipment - Frost Reaper",
    #"Equipment - Gold Scythe",
    #"Equipment - Ember Scythe",
    "Equipment - Gravedigger",
    "Equipment - Wind Thresher",
    #"Equipment - Adjudicator",
    #"Equipment - Twilight",
    #"Equipment - Arctic Chill",
    #"Equipment - Diamond Scythe",

    #Bows
    "Equipment - Craftwork Bow",
    "Equipment - Hunting Bow",
    #"Equipment - Silver Bow",
    #"Equipment - Habins Bow",
    #"Equipment - Elven Bow",
    #"Equipment - Gold Bow",
    #"Equipment - Spore Shooter",
    "Equipment - Siege Bow",
    "Equipment - Rune Bow",
    #"Equipment - Panakeia",
    "Equipment - Dream Hunter",
    #"Equipment - Diamond Bow",

    #Staves
    "Equipment - Cedar Staff",
    "Equipment - Craftwork Staff",
    "Equipment - Bone Smasher",
    "Equipment - Iron Rod",
    "Equipment - Walking Stick",
    #"Equipment - Silver Staff",
    "Equipment - Knockout Stick",
    #"Equipment - Future Sight",
    #"Equipment - Digested Staff",
    "Equipment - Life Jewel",
    #"Equipment - Gold Staff",
    "Equipment - Apprentice",
    "Equipment - Sages Walker",
    #"Equipment - Beats Stick",
    "Equipment - Staff of Balance",
    "Equipment - Judgement",
    #"Equipment - Diamond Staff",

    #Wands
    "Equipment - Cedar Wand",
    "Equipment - Torch",
    #"Equipment - Ink Stick",
    "Equipment - Craftwork Wand",
    "Equipment - Static Rod",
    #"Equipment - Silver Wand",
    "Equipment - Storm Rod",
    "Equipment - Cursegiver",
    #"Equipment - Gold Wand",
    "Equipment - Rune Wand",
    "Equipment - Stardust Wand",
    #"Equipment - Aura Focus",
    "Equipment - Paladin Wand",
    #"Equipment - Obelisk",
    "Equipment - Flameseeker",
    #"Equipment - Diamond Wand",

    #Books
    "Equipment - Craftwork Pages",
    "Equipment - Gospel",
    "Equipment - Paypirbak",
    "Equipment - Art of War",
    #"Equipment - Silver Pages",
    "Equipment - Blank Pages",
    "Equipment - Tome of Light",
    #"Equipment - Gold Pages",
    "Equipment - Dark Gospel",
    "Equipment - Malifice",
    #"Equipment - Codex",
    #"Equipment - Diamond Pages",

    #Armor
    #Shields
    "Equipment - Stout Shield",
    "Equipment - Iron Guard",
    "Equipment - Stalwart Shield",
    "Equipment - Craftwork Shield",
    "Equipment - Lucky Platter",
    "Equipment - Boomer Shield",
    #"Equipment - Silver Shield",
    #"Equipment - Blood Shield",
    "Equipment - The Immovable",
    "Equipment - Mages Platter",
    #"Equipment - Gold Shield",
    "Equipment - Flame Guard",
    "Equipment - Wizards Wall",
    "Equipment - Tower Shield",
    "Equipment - Nomads Guard",
    #"Equipment - Ether Shield",
    "Equipment - Mirror Shield",
    #"Equipment - Diamond Shield",

    #Heavy Head
    "Equipment - Storm Helm",
    "Equipment - Craftwork Helm",
    "Equipment - Iron Helm",
    "Equipment - Battle Helm",
    #"Equipment - Silver Helm",
    "Equipment - Horned Helm",
    #"Equipment - Gold Helm",
    "Equipment - Insignia Helm",
    "Equipment - Demon Helm",
    #"Equipment - Guts Busby",
    #"Equipment - Raid Helm",
    "Equipment - Spellsword Helm",
    #"Equipment - Diamond Helm",

    #Heavy Body
    "Equipment - Ring Mail",
    "Equipment - Plate of Wolf",
    "Equipment - Craftwork Mail",
    "Equipment - Iron Armor",
    "Equipment - Battleplate",
    #"Equipment - Silver Mail",
    #"Equipment - Plate of Tiger",
    "Equipment - Knights Plate",
    "Equipment - Bone Mail",
    #"Equipment - Gold Mail",
    "Equipment - Sky Armor",
    "Equipment - Plate of Lion",
    "Equipment - Demon Plate",
    #"Equipment - Construct Mail",
    #"Equipment - Guardian Angel",
    "Equipment - Plate of Whale",
    "Equipment - Lunar Mail",
    #"Equipment - Diamond Mail",
    "Equipment - Warrior Mail",
    "Equipment - Warlock Mail",
    "Equipment - Aegis Mail",
    "Equipment - Reaper Mail",
    "Equipment - Samurai Mail",
    "Equipment - Valkyrie Mail",
    "Equipment - Beastmaster Mail",
    "Equipment - Mimic Mail",

    #Medium Head
    "Equipment - Storm Cap",
    "Equipment - Headgear",
    "Equipment - Craftwork Cap",
    "Equipment - Spore Blocker",
    #"Equipment - Silver Cap",
    "Equipment - Red Cap",
    "Equipment - Suitor Hat",
    #"Equipment - Gold Cap",
    #"Equipment - Red Hat",
    "Equipment - Pirate Hat",
    "Equipment - Battle Band",
    "Equipment - Captains Hat",
    #"Equipment - Diamond Cap",

    #Medium Body
    "Equipment - Craftwork Vest",
    "Equipment - Smelly Gi",
    "Equipment - Training Gi",
    "Equipment - Tuxedo",
    #"Equipment - Silver Vest",
    "Equipment - Red Coat",
    #"Equipment - Bandage Wrap",
    "Equipment - Gaia Vest",
    "Equipment - Brigandine",
    #"Equipment - Gold Vest",
    #"Equipment - Onion Gi",
    "Equipment - Judo Gi",
    "Equipment - Shadow Gi",
    #"Equipment - Rex Vest",
    #"Equipment - Slime Coat",
    #"Equipment - Diamond Vest",
    "Equipment - Monk Vest",
    "Equipment - Rogue Vest",
    "Equipment - Fencer Vest",
    "Equipment - Hunter Vest",
    "Equipment - Ninja Vest",
    "Equipment - Nomad Vest",
    "Equipment - Beatsmith Vest",
    "Equipment - Assassin Vest",

    #Light Head
    "Equipment - Cotton Hood",
    "Equipment - Storm Hood",
    "Equipment - Craftwork Crown",
    "Equipment - Circlet",
    "Equipment - Woven Hood",
    #"Equipment - Silver Crown",
    #"Equipment - Fairys Crown",
    #"Equipment - Blood Hat",
    "Equipment - Plague Mask",
    "Equipment - Guard Crown",
    #"Equipment - Gold Crown",
    "Equipment - Bronze Hairpin",
    "Equipment - Ravens Hood",
    "Equipment - Celestial Crown",
    "Equipment - Pointy Hat",
    "Equipment - Vita Crown",
    #"Equipment - Pact Crown",
    "Equipment - Protector",
    #"Equipment - Diamond Crown",

    #Light Body
    "Equipment - Mages Robe",
    "Equipment - Swimmers Top",
    "Equipment - Craftwork Robe",
    "Equipment - Dress",
    "Equipment - Woven Shirt",
    #"Equipment - Silver Cape",
    #"Equipment - Cosplay Garb",
    "Equipment - Shelter Dress",
    #"Equipment - Gold Robe",
    "Equipment - Blue Cape",
    "Equipment - Seekers Garb",
    "Equipment - Ravens Cloak",
    "Equipment - Archmage Vest",
    #"Equipment - Saviors Cape",
    "Equipment - Assassins Cloak",
    "Equipment - Stealth Cape",
    #"Equipment - Shell Gown",
    #"Equipment - Diamond Robe",
    "Equipment - Cleric Robe",
    "Equipment - Wizard Robe",
    "Equipment - Shaman Robe",
    "Equipment - Scholar Robe",
    "Equipment - Chemist Robe",
    "Equipment - Dervish Robe",
    "Equipment - Weaver Robe",
    "Equipment - Summoner Robe",
    
    #Accessories aren't replaced by progressive items

    #Shop Equipment
    # Weapons
    # Swords
    "Equipment - Short Sword",
    "Equipment - Razor Edge",
    "Equipment - Artisan Sword",
    "Equipment - Longsword",
    "Equipment - Scimitar",
    "Equipment - War Sword",
    "Equipment - Highland Blade",
    "Equipment - Crystal Sword",
    "Equipment - Master Sword",
    "Equipment - Master Bigsword",

    # Axes
    "Equipment - Hand Axe",
    "Equipment - Chopper",
    "Equipment - Stone Splitter",
    "Equipment - Broadaxe",
    "Equipment - Artisan Axe",
    "Equipment - War Axe",
    "Equipment - Berserker Axe",
    "Equipment - Master Axe",
    "Equipment - Ancient Axe",
    "Equipment - Master Bigaxe",

    # Daggers
    "Equipment - Dirk",
    "Equipment - Fishgutter",
    "Equipment - Shank",
    "Equipment - Kris",
    "Equipment - Rondel",
    "Equipment - Artisan Dagger",
    "Equipment - Janbiya",
    "Equipment - Sai",
    "Equipment - Kodachi",
    "Equipment - Fanged Knife",
    "Equipment - Poignard",
    "Equipment - Master Dagger",

    # Rapiers
    "Equipment - Rapier",
    "Equipment - Stinger",
    "Equipment - Estoc",
    "Equipment - Scarlette",
    "Equipment - Artisan Rapier",
    "Equipment - Vulture",
    "Equipment - Falcon Dance",
    "Equipment - Epee",
    "Equipment - Master Rapier",

    # Katanas
    "Equipment - Artisan Katana",
    "Equipment - Nansen",
    "Equipment - Mitsutada",
    "Equipment - Hitofuri",
    "Equipment - Kokaiji",
    "Equipment - Tomokirimaru",
    "Equipment - Master Katana",

    # Spears
    "Equipment - Short Spear",
    "Equipment - Javelin",
    "Equipment - Artisan Spear",
    "Equipment - Wind Lance",
    "Equipment - Voulge",
    "Equipment - Master Spear",

    # Scythes
    "Equipment - War Scythe",
    "Equipment - Artisan Scythe",
    "Equipment - Thresher",
    "Equipment - Great Thresher",
    "Equipment - Master Scythe",

    # Bows
    "Equipment - Short Bow",
    "Equipment - Long Bow",
    "Equipment - Artisan Bow",
    "Equipment - Battle Bow",
    "Equipment - Composite Bow",
    "Equipment - Razor Bow",
    "Equipment - War Bow",
    "Equipment - Master Bow",
    "Equipment - Artemis",

    # Staves
    "Equipment - Short Staff",
    "Equipment - Gnarled Root",
    "Equipment - Quarterstaff",
    "Equipment - Maplewood",
    "Equipment - Artisan Staff",
    "Equipment - Skullbasher",
    "Equipment - Battle Staff",
    "Equipment - Natures Gift",
    "Equipment - War Staff",
    "Equipment - Master Staff",

    # Wands
    "Equipment - Ash Wand",
    "Equipment - Oak Wand",
    "Equipment - Soul Wand",
    "Equipment - Maple Wand",
    "Equipment - Artisan Wand",
    "Equipment - Baton",
    "Equipment - Effigy",
    "Equipment - Sentinel Rod",
    "Equipment - Master Wand",

    # Books
    "Equipment - Moby Dick",
    "Equipment - Orylei",
    "Equipment - Encyclopedia",
    "Equipment - Artisan Pages",
    "Equipment - Grimoire",
    "Equipment - Hydrology",
    "Equipment - Divination",
    "Equipment - Master Pages",

    # Armor
    # Shields
    "Equipment - Buckler",
    "Equipment - Vanguard",
    "Equipment - Duelling Shield",
    "Equipment - Artisan Shield",
    "Equipment - Cross Shield",
    "Equipment - Brass Cross",
    "Equipment - Cross Guard",
    "Equipment - Bulkwark",
    "Equipment - Master Shield",
    "Equipment - Turtle Shell",

    # Heavy Head
    "Equipment - Chain Helm",
    "Equipment - Sturdy Helm",
    "Equipment - Copper Helm",
    "Equipment - Bronze Helm",
    "Equipment - Scale Helm",
    "Equipment - Artisan Helm",
    "Equipment - Orion Barbut",
    "Equipment - Iron Barbut",
    "Equipment - Cross Helm",
    "Equipment - Master Helm",

    # Heavy Body
    "Equipment - Breastplate",
    "Equipment - Copper Suit",
    "Equipment - Bronze Suit",
    "Equipment - Scale Mail",
    "Equipment - Artisan Mail",
    "Equipment - Orion Armor",
    "Equipment - Plate Mail",
    "Equipment - Dragon Mail",
    "Equipment - Master Mail",

    # Medium Head
    "Equipment - Leather Cap",
    "Equipment - Beret",
    "Equipment - Rugged Hat",
    "Equipment - Vikings Hat",
    "Equipment - Artisan Cap",
    "Equipment - Combat Band",
    "Equipment - Bandana",
    "Equipment - Tall Tall Hat",
    "Equipment - Master Cap",
    "Equipment - Red Headgear",

    # Medium Body
    "Equipment - Leather Outfit",
    "Equipment - Studded Armor",
    "Equipment - Leather Mail",
    "Equipment - Chain Vest",
    "Equipment - Combat Vest",
    "Equipment - Artisan Vest",
    "Equipment - Power Vest",
    "Equipment - Drifters Vest",
    "Equipment - Martial Vest",
    "Equipment - Master Vest",
    "Equipment - Quintar Pelt",

    # Light Head
    "Equipment - Hemp Hood",
    "Equipment - Holy Hat",
    "Equipment - Silk Hat",
    "Equipment - Holy Miter",
    "Equipment - Artisan Crown",
    "Equipment - Clerics Hood",
    "Equipment - Wizards Hat",
    "Equipment - Quilted Hat",
    "Equipment - Regen Crown",
    "Equipment - Master Crown",

    # Light Body
    "Equipment - Hemp Robe",
    "Equipment - Cotton Robe",
    "Equipment - Priest Garb",
    "Equipment - Silk Shirt",
    "Equipment - Artisan Shirt",
    "Equipment - Wizards Robe",
    "Equipment - Clerics Robe",
    "Equipment - Sturdy Cape",
    "Equipment - Winter Cape",
    "Equipment - Master Cape",

    #Accessories aren't replaced by progressive items
)

# shop_accessories: Tuple[str, ...] = (
#     "Equipment - Prayer Beads",
#     "Equipment - Samurais Glove",
#     "Equipment - Casters Ring",
#     "Equipment - Fearsome Ring",
#     "Equipment - Crit Fang",
#     "Equipment - Dancing Shoes",
#     # "Equipment - Bulk Belt",
#     # "Equipment - Poison Talon",
#     # "Equipment - First Strike Mitt",
#     # "Equipment - Menders Ring",
#     # "Equipment - Kitsune Mask",
#     # "Equipment - Pact Ring",
#     # "Equipment - Gusto Fang",
#     # "Equipment - Winter Mitten"
# )

optional_scholar_abilities: Tuple[str, ...] = (
    ROOST,
    LUCKY_DICE,
    SUN_BATH,
    SLEEP_AURA,
    REGENERATE,
    #"Scholar - Reverse Polarity" leaving this one always in the pool so you can merc Gran
    BARRIER,
    MP_SICKLE,
    ADRENALINE,
    FIRE_BREATH,
    EXPLODE,
    WHIRLWIND,
    ATMOSHEAR,
    BUILD_LIFE,
    AERO,
    INSULT,
    INFUSION,
    OVERlOAD,
    REFLECTION,
    LIFEGIVER
)

default_starting_job_list: List[str] = [
    WARRIOR_JOB,
    MONK_JOB,
    ROGUE_JOB,
    CLERIC_JOB,
    WIZARD_JOB,
    WARLOCK_JOB,
]

job_crystal_beginner_dictionary: Dict[str, str] = {
    FENCER_JOB: THE_PALE_GROTTO_DISPLAY_NAME + FENCER_JOB_CRYSTAL_LOCATION,
    SHAMAN_JOB: DRAFT_SHAFT_CONDUIT_DISPLAY_NAME + SHAMAN_JOB_CRYSTAL_LOCATION,
    SCHOLAR_JOB: YAMAGAWA_MA_DISPLAY_NAME + SCHOLAR_JOB_CRYSTAL_LOCATION,
    AEGIS_JOB: SKUMPARADISE_DISPLAY_NAME + AEGIS_JOB_CRYSTAL_LOCATION,
}

job_crystal_advanced_dictionary: Dict[str, str] = {
    HUNTER_JOB: QUINTAR_NEST_DISPLAY_NAME + HUNTER_JOB_CRYSTAL_LOCATION,
    CHEMIST_JOB: QUINTAR_SANCTUM_DISPLAY_NAME + CHEMIST_JOB_CRYSTAL_LOCATION,
    REAPER_JOB: CAPITAL_JAIL_DISPLAY_NAME + REAPER_JOB_CRYSTAL_LOCATION,
    NINJA_JOB: OKIMOTO_NS_DISPLAY_NAME + NINJA_JOB_CRYSTAL_LOCATION,
    NOMAD_JOB: RIVER_CATS_EGO_AP_REGION + NOMAD_JOB_CRYSTAL_LOCATION,
    DERVISH_JOB: ANCIENT_RESERVOIR_DISPLAY_NAME + DERVISH_JOB_CRYSTAL_LOCATION,
    BEATSMITH_JOB: CAPITAL_SEQUOIA_DISPLAY_NAME + BEATSMITH_JOB_CRYSTAL_LOCATION,
}

job_crystal_expert_dictionary: Dict[str, str] = {
    SAMURAI_JOB: SHOUDU_PROVINCE_DISPLAY_NAME + SAMURAI_JOB_CRYSTAL_LOCATION,
    ASSASSIN_JOB: THE_UNDERCITY_DISPLAY_NAME + ASSASSIN_JOB_CRYSTAL_LOCATION,
    VALKYRIE_JOB: BEAURIOR_VOLCANO_DISPLAY_NAME + VALKYRIE_JOB_CRYSTAL_LOCATION,
    SUMMONER_JOB: SLIP_GLIDE_RIDE_DISPLAY_NAME + SUMMONER_JOB_CRYSTAL_LOCATION,
    BEASTMASTER_JOB: CASTLE_RAMPARTS_DISPLAY_NAME + BEASTMASTER_JOB_CRYSTAL_LOCATION,
    WEAVER_JOB: JIDAMBA_EACLANEYA_DISPLAY_NAME + WEAVER_JOB_CRYSTAL_LOCATION,
    MIMIC_JOB: THE_CHALICE_OF_TAR_DISPLAY_NAME + MIMIC_JOB_CRYSTAL_LOCATION,
}

key_rings: Tuple[str, ...] = (
    PRISON_KEY_RING,
    BEAURIOR_KEY_RING,
    SLIP_GLIDE_RIDE_KEY_RING,
    ICE_PUZZLE_KEY_RING,
    JIDAMBA_KEY_RING,
)

dungeon_keys: Tuple[str, ...] = (
    CELL_KEY,
    SOUTH_WING_KEY,
    EAST_WING_KEY,
    WEST_WING_KEY,
    DARK_WING_KEY,
    SMALL_KEY,
    BEAURIOR_BOSS_KEY,
    RED_DOOR_KEY,
    ICE_PUZZLE_KEY,
    FOLIAGE_KEY,
    CAVE_KEY,
    CANOPY_KEY
)

singleton_keys: Tuple[str, ...] = (
    GARDENERS_KEY,
    COURTYARD_KEY,
    LUXURY_KEY,
    ROOM_ONE_KEY,
    PYRAMID_KEY,
    TRAM_KEY,
    ICE_CELL_KEY,
    RAMPART_KEY,
    FORGOTTEN_KEY
)

display_region_name_to_pass_dict: Dict[str, str] = {
    #Beginner
    SPAWNING_MEADOWS_DISPLAY_NAME: SPAWNING_MEADOWS_PASS,
    DELENDE_DISPLAY_NAME: DELENDE_PASS,
    SOILED_DEN_DISPLAY_NAME: SOILED_DEN_PASS,
    THE_PALE_GROTTO_DISPLAY_NAME: THE_PALE_GROTTO_PASS,
    SEASIDE_CLIFFS_DISPLAY_NAME: SEASIDE_CLIFFS_PASS,
    DRAFT_SHAFT_CONDUIT_DISPLAY_NAME: DRAFT_SHAFT_CONDUIT_PASS,
    MERCURY_SHRINE_DISPLAY_NAME: MERCURY_SHRINE_PASS,
    YAMAGAWA_MA_DISPLAY_NAME: YAMAGAWA_MA_PASS,
    PROVING_MEADOWS_DISPLAY_NAME: PROVING_MEADOWS_PASS,
    SKUMPARADISE_DISPLAY_NAME: SKUMPARADISE_PASS,
    #Advanced
    CAPITAL_SEQUOIA_DISPLAY_NAME: CAPITAL_SEQUOIA_PASS,
    JOJO_SEWERS_DISPLAY_NAME: JOJO_SEWERS_PASS,
    BOOMER_SOCIETY_DISPLAY_NAME: BOOMER_SOCIETY_PASS,
    ROLLING_QUINTAR_FIELDS_DISPLAY_NAME: ROLLING_QUINTAR_FIELDS_PASS,
    QUINTAR_NEST_DISPLAY_NAME: QUINTAR_NEST_PASS,
    QUINTAR_SANCTUM_DISPLAY_NAME: QUINTAR_SANCTUM_PASS,
    CAPITAL_JAIL_DISPLAY_NAME: CAPITAL_JAIL_PASS,
    CAPITAL_PIPELINE_DISPLAY_NAME: CAPITAL_PIPELINE_PASS,
    COBBLESTONE_CRAG_DISPLAY_NAME: COBBLESTONE_CRAG_PASS,
    OKIMOTO_NS_DISPLAY_NAME: OKIMOTO_NS_PASS,
    GREENSHIRE_REPRISE_DISPLAY_NAME: GREENSHIRE_REPRISE_PASS,
    SALMON_PASS_DISPLAY_NAME: SALMON_PASS_PASS,
    SALMON_RIVER_DISPLAY_NAME: SALMON_RIVER_PASS,
    SHOUDU_WATERFRONT_DISPLAY_NAME: SHOUDU_WATERFRONT_PASS,
    POKO_POKO_DESERT_DISPLAY_NAME: POKO_POKO_DESERT_PASS,
    SARA_SARA_BAZAAR_DISPLAY_NAME: SARA_SARA_BAZAAR_PASS,
    SARA_SARA_BEACH_DISPLAY_NAME: SARA_SARA_BEACH_PASS,
    ANCIENT_RESERVOIR_DISPLAY_NAME: ANCIENT_RESERVOIR_PASS,
    SALMON_BAY_DISPLAY_NAME: SALMON_BAY_PASS,
    #Expert
    THE_OPEN_SEA_DISPLAY_NAME: THE_OPEN_SEA_PASS,
    SHOUDU_PROVINCE_DISPLAY_NAME: SHOUDU_PROVINCE_PASS,
    THE_UNDERCITY_DISPLAY_NAME: THE_UNDERCITY_PASS,
    GANYMEDE_SHRINE_DISPLAY_NAME: GANYMEDE_SHRINE_PASS,
    BEAURIOR_VOLCANO_DISPLAY_NAME: BEAURIOR_VOLCANO_PASS,
    BEAURIOR_ROCK_DISPLAY_NAME: BEAURIOR_ROCK_PASS,
    LAKE_DELENDE_DISPLAY_NAME: LAKE_DELENDE_PASS,
    QUINTAR_RESERVE_DISPLAY_NAME: QUINTAR_RESERVE_PASS,
    DIONE_SHRINE_DISPLAY_NAME: DIONE_SHRINE_PASS,
    QUINTAR_MAUSOLEUM_DISPLAY_NAME: QUINTAR_MAUSOLEUM_PASS,
    EASTERN_CHASM_DISPLAY_NAME: EASTERN_CHASM_PASS,
    TALL_TALL_HEIGHTS_DISPLAY_NAME: TALL_TALL_HEIGHTS_PASS,
    NORTHERN_CAVE_DISPLAY_NAME: NORTHERN_CAVE_PASS,
    LANDS_END_DISPLAY_NAME: LANDS_END_PASS,
    SLIP_GLIDE_RIDE_DISPLAY_NAME: SLIP_GLIDE_RIDE_PASS,
    SEQUOIA_ATHENAEUM_DISPLAY_NAME: SEQUOIA_ATHENAEUM_PASS,
    NORTHERN_STRETCH_DISPLAY_NAME: NORTHERN_STRETCH_PASS,
    CASTLE_RAMPARTS_DISPLAY_NAME: CASTLE_RAMPARTS_PASS,
    THE_CHALICE_OF_TAR_DISPLAY_NAME: THE_CHALICE_OF_TAR_PASS,
    FLYERS_CRAG_DISPLAY_NAME: FLYERS_CRAG_PASS,
    JIDAMBA_TANGLE_DISPLAY_NAME: JIDAMBA_TANGLE_PASS,
    JIDAMBA_EACLANEYA_DISPLAY_NAME: JIDAMBA_EACLANEYA_PASS,
    THE_DEEP_SEA_DISPLAY_NAME: THE_DEEP_SEA_PASS,
    NEPTUNE_SHRINE_DISPLAY_NAME: NEPTUNE_SHRINE_PASS,
    JADE_CAVERN_DISPLAY_NAME: JADE_CAVERN_PASS,
    CONTINENTAL_TRAM_DISPLAY_NAME: CONTINENTAL_TRAM_PASS,
    #End Game
    ANCIENT_LABYRINTH_DISPLAY_NAME: ANCIENT_LABYRINTH_PASS,
    THE_SEQUOIA_DISPLAY_NAME: THE_SEQUOIA_PASS,
    THE_DEPTHS_DISPLAY_NAME: THE_DEPTHS_PASS,
    CASTLE_SEQUOIA_DISPLAY_NAME: CASTLE_SEQUOIA_PASS,
    THE_OLD_WORLD_DISPLAY_NAME: THE_OLD_WORLD_PASS,
    THE_NEW_WORLD_DISPLAY_NAME: THE_NEW_WORLD_PASS,
}

filler_items: Tuple[str, ...] = (
    "Item - Tonic",
    "Item - Potion",
    "Item - Z-Potion",
    "Item - Tincture",
    "Item - Ether",
    "Item - Zether",
    "Item - Fenix Juice",
    "Item - Fenix Syrup",
    "Item - Nans Stew",
    "Item - Nans Cocoa",
    "Item - Nans Secret Recipe",
    "Item - Nuts",
    "Item - Milk",
    "Item - Sweet Pop Candy",
    "Item - Sour Pop Candy",
    "Item - Bitter Pop Candy",
    "Item - Decent Cod",
    "Item - Fresh Salmon",
    "Item - Scroll",
    # add currency?
)

def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        if data.category != "Events":
            categories.setdefault(data.category, set()).add(name)

    return categories

def get_starting_jobs(world: "CrystalProjectWorld") -> List[str]:
    if world.options.job_rando.value == world.options.job_rando.option_full:
        return get_random_starting_jobs(world, world.options.starting_job_quantity.value)
    else:
        return default_starting_job_list

def get_random_starting_jobs(self, count:int) -> List[str]:
    if self.options.use_mods.value == self.options.use_mods.option_true:
        return self.random.sample(list(self.item_name_groups[JOB]), count)
    else:
        return self.random.sample(list(self.base_game_jobs), count)

def set_jobs_at_default_locations(world: "CrystalProjectWorld", player_name:str) -> Tuple[int, List[str]]:
    job_crystal_dictionary: Dict[str, str] = job_crystal_beginner_dictionary.copy() #if we don't use copy it means updating job_crystal_dictionary messes with the beginner dict too
    jobs_not_to_exclude: List[str] = []

    if world.options.included_regions.value == world.options.included_regions.option_advanced:
        job_crystal_dictionary.update(job_crystal_advanced_dictionary)

    if (world.options.included_regions.value == world.options.included_regions.option_expert
        or world.options.included_regions.value == world.options.included_regions.option_all):
        job_crystal_dictionary.update(job_crystal_advanced_dictionary)
        job_crystal_dictionary.update(job_crystal_expert_dictionary)

    for job_name in job_crystal_dictionary:
        try:
            world.get_location(job_crystal_dictionary[job_name]).place_locked_item(world.create_item(job_name))
            #message = "Placing" + job_name + " at " + job_crystal_dictionary[job_name]
            #world.logger.info(message)
        except KeyError:
            jobs_not_to_exclude.append(job_name)
            message = f"For player {player_name}: the crystal where {job_name} was placed was updated by a mod. It has been forced to be randomized instead of in its default location."
            logging.getLogger().info(message)


    return len(job_crystal_dictionary), jobs_not_to_exclude