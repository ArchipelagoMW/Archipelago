from typing import List

from .constants.display_regions import *
from .locations import LocationData, npc_index_offset


def get_unused_locations() -> List[LocationData]:
    location_table: List[LocationData] = [
        LocationData(SPAWNING_MEADOWS_AP_REGION, SPAWNING_MEADOWS_DISPLAY_NAME + " NPC - Slow Nan walk", 4 + npc_index_offset),
        LocationData(DELENDE_HIGH_BRIDGES_AP_REGION, DELENDE_DISPLAY_NAME + " NPC - Master Fencer", 3573 + npc_index_offset),
        LocationData(YAMAGAWA_MA_AP_REGION, YAMAGAWA_MA_DISPLAY_NAME + " NPC - Master Scholar", 3574 + npc_index_offset),
        LocationData(SEASIDE_CLIFFS_AP_REGION, SEASIDE_CLIFFS_DISPLAY_NAME + " NPC - Master Shaman", 3572 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Master Beatsmith", 3560 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Master Cleric", 3568 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Master Monk", 3567 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Master Rogue", 3571 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Master Warlock", 3570 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Master Warrior", 3566 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA_AP_REGION, CAPITAL_SEQUOIA_DISPLAY_NAME + " NPC - Master Wizard", 3569 + npc_index_offset),
        LocationData(ROLLING_QUINTAR_FIELDS_AP_REGION, ROLLING_QUINTAR_FIELDS_DISPLAY_NAME + " NPC - Master Hunter", 3558 + npc_index_offset),
        LocationData(RUINS_CRUMBLING_ON_SHORE_AP_REGION, SARA_SARA_BEACH_DISPLAY_NAME + " NPC - Master Dervish", 3575 + npc_index_offset),
        LocationData(SUMMONERS_TOWER_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " NPC - Master Aegis", 3610 + npc_index_offset),
        LocationData(SUMMONERS_TOWER_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " NPC - Master Beastmaster", 3608 + npc_index_offset),
        LocationData(SUMMONERS_TOWER_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " NPC - Master Ninja", 3550 + npc_index_offset),
        LocationData(SUMMONERS_TOWER_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " NPC - Master Nomad", 3548 + npc_index_offset),
        LocationData(SUMMONERS_TOWER_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " NPC - Master Reaper", 3611 + npc_index_offset),
        LocationData(SUMMONERS_TOWER_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " NPC - Master Summoner", 3557 + npc_index_offset),
        LocationData(SUMMONERS_TOWER_AP_REGION, NORTHERN_STRETCH_DISPLAY_NAME + " NPC - Master Valkyrie", 3554 + npc_index_offset),
        LocationData(SHOUDU_PROVINCE_PROPER_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Master Assassin", 3605 + npc_index_offset),
        LocationData(SHOUDU_PROVINCE_PROPER_AP_REGION, SHOUDU_PROVINCE_DISPLAY_NAME + " NPC - Master Samurai", 3576 + npc_index_offset),
        LocationData(PAMOA_TREE_AP_REGION, TALL_TALL_HEIGHTS_DISPLAY_NAME + " NPC - Master Chemist", 3707 + npc_index_offset),
        LocationData(CHALICE_ASCENT_AP_REGION, THE_CHALICE_OF_TAR_DISPLAY_NAME + " NPC - Master Mimic", 3606 + npc_index_offset),
        LocationData(JIDAMBA_FOREST_FLOOR_AP_REGION, JIDAMBA_TANGLE_DISPLAY_NAME + " NPC - Master Weaver", 3579 + npc_index_offset),
    ]

    return location_table