from typing import List
from .locations import LocationData, npc_index_offset
from .constants.regions import *

def get_unused_locations() -> List[LocationData]:
    location_table: List[LocationData] = [
        LocationData(SPAWNING_MEADOWS, "Spawning Meadows NPC - Slow Nan walk", 4 + npc_index_offset),
        LocationData(DELENDE, "Delende NPC - Master Fencer", 3573 + npc_index_offset),
        LocationData(YAMAGAWA_MA, "Yamagawa MA NPC - Master Scholar", 3574 + npc_index_offset),
        LocationData(SEASIDE_CLIFFS, "Sea Side Cliffs NPC - Master Shaman", 3572 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA, "Capital Sequoia NPC - Master Beatsmith", 3560 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA, "Capital Sequoia NPC - Master Cleric", 3568 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA, "Capital Sequoia NPC - Master Monk", 3567 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA, "Capital Sequoia NPC - Master Rogue", 3571 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA, "Capital Sequoia NPC - Master Warlock", 3570 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA, "Capital Sequoia NPC - Master Warrior", 3566 + npc_index_offset),
        LocationData(CAPITAL_SEQUOIA, "Capital Sequoia NPC - Master Wizard", 3569 + npc_index_offset),
        LocationData(ROLLING_QUINTAR_FIELDS, "Rolling Quintar Fields NPC - Master Hunter", 3558 + npc_index_offset),
        LocationData(SARA_SARA_BEACH_WEST, "Sara Sara Beach NPC - Master Dervish", 3575 + npc_index_offset),
        LocationData(NORTHERN_STRETCH, "Northern Stretch NPC - Master Aegis", 3610 + npc_index_offset),
        LocationData(NORTHERN_STRETCH, "Northern Stretch NPC - Master Beastmaster", 3608 + npc_index_offset),
        LocationData(NORTHERN_STRETCH, "Northern Stretch NPC - Master Ninja", 3550 + npc_index_offset),
        LocationData(NORTHERN_STRETCH, "Northern Stretch NPC - Master Nomad", 3548 + npc_index_offset),
        LocationData(NORTHERN_STRETCH, "Northern Stretch NPC - Master Reaper", 3611 + npc_index_offset),
        LocationData(NORTHERN_STRETCH, "Northern Stretch NPC - Master Summoner", 3557 + npc_index_offset),
        LocationData(NORTHERN_STRETCH, "Northern Stretch NPC - Master Valkyrie", 3554 + npc_index_offset),
        LocationData(SHOUDU_PROVINCE, "Shoudu Province NPC - Master Assassin", 3605 + npc_index_offset),
        LocationData(SHOUDU_PROVINCE, "Shoudu Province NPC - Master Samurai", 3576 + npc_index_offset),
        LocationData(TALL_TALL_HEIGHTS, "Tall Tall Heights NPC - Master Chemist", 3707 + npc_index_offset),
        LocationData(THE_CHALICE_OF_TAR, "Chalice of Tar NPC - Master Mimic", 3606 + npc_index_offset),
        LocationData(JIDAMBA_TANGLE, "Jidamba Tangle NPC - Master Weaver", 3579 + npc_index_offset),
    ]

    return location_table