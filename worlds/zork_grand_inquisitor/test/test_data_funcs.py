import unittest

from ..data_funcs import location_access_rule_for, entrance_access_rule_for
from ..enums import ZorkGrandInquisitorLocations, ZorkGrandInquisitorRegions


class DataFuncsTest(unittest.TestCase):
    def test_location_access_rule_for(self) -> None:
        # No Requirements
        self.assertEqual(
            "lambda state: True",
            location_access_rule_for(ZorkGrandInquisitorLocations.ALARM_SYSTEM_IS_DOWN, 1),
        )

        # Single Item Requirement
        self.assertEqual(
            'lambda state: state.has("Sword", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.DONT_EVEN_START_WITH_US_SPARKY, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Spell: NARWILE", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.DRAGON_ARCHIPELAGO_TIME_TUNNEL, 1),
        )

        # Single Event Requirement
        self.assertEqual(
            'lambda state: state.has("Event: Knows OBIDIL", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.A_BIG_FAT_SASSY_2_HEADED_MONSTER, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Event: Dunce Locker Openable", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.BETTER_SPELL_MANUFACTURING_IN_UNDER_10_MINUTES, 1),
        )

        # Multiple Item Requirements
        self.assertEqual(
            'lambda state: state.has("Hotspot: Purple Words", 1) and state.has("Spell: IGRAM", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.A_SMALLWAY, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Hotspot: Mossy Grate", 1) and state.has("Spell: THROCK", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.BEAUTIFUL_THATS_PLENTY, 1),
        )

        # Multiple Item Requirements OR
        self.assertEqual(
            'lambda state: (state.has("Totem: Griff", 1) or state.has("Totem: Lucy", 1)) and state.has("Hotspot: Mailbox Door", 1) and state.has("Hotspot: Mailbox Flag", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.MAILED_IT_TO_HELL, 1),
        )

        # Multiple Mixed Requirements
        self.assertEqual(
            'lambda state: state.has("Event: Cigar Accessible", 1) and state.has("Hotspot: Grand Inquisitor Doll", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.ARREST_THE_VANDAL, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Sword", 1) and state.has("Event: Rope GLORFable", 1) and state.has("Hotspot: Monastery Vent", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.I_HOPE_YOU_CAN_CLIMB_UP_THERE, 1),
        )

    def test_entrance_access_rule_for(self) -> None:
        # No Requirements
        self.assertEqual(
            "lambda state: True",
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.PORT_FOOZLE, 1
            ),
        )

        self.assertEqual(
            "lambda state: True",
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.CROSSROADS, 1
            ),
        )

        # Single Requirement
        self.assertEqual(
            'lambda state: (state.has("Map", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE, ZorkGrandInquisitorRegions.CROSSROADS, 1
            ),
        )

        self.assertEqual(
            'lambda state: (state.has("Map", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.HADES_SHORE, ZorkGrandInquisitorRegions.CROSSROADS, 1
            ),
        )

        # Multiple Requirements AND
        self.assertEqual(
            'lambda state: (state.has("Spell: REZROV", 1) and state.has("Hotspot: In Magic We Trust Door", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.GUE_TECH, 1
            ),
        )

        self.assertEqual(
            'lambda state: (state.has("Event: Door Smoked Cigar", 1) and state.has("Event: Door Drank Mead", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.DM_LAIR, ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, 1
            ),
        )

        self.assertEqual(
            'lambda state: (state.has("Hotspot: Closet Door", 1) and state.has("Spell: NARWILE", 1) and state.has("Event: Knows YASTARD", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR, ZorkGrandInquisitorRegions.WHITE_HOUSE, 1
            ),
        )

        # Multiple Requirements AND + OR
        self.assertEqual(
            'lambda state: (state.has("Sword", 1) and state.has("Hotspot: Dungeon Master\'s Lair Entrance", 1)) or (state.has("Map", 1) and state.has("Teleporter Destination: Dungeon Master\'s Lair", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.CROSSROADS, ZorkGrandInquisitorRegions.DM_LAIR, 1
            ),
        )

        # Multiple Requirements Regions
        self.assertEqual(
            'lambda state: (state.has("Griff\'s Air Pump", 1) and state.has("Griff\'s Inflatable Raft", 1) and state.has("Griff\'s Inflatable Sea Captain", 1) and state.has("Hotspot: Dragon Nostrils", 1) and state.has("Griff\'s Dragon Tooth", 1) and state.can_reach("Port Foozle Past - Tavern", "Region", 1) and state.has("Lucy\'s Playing Card: 1 Pip", 1) and state.has("Lucy\'s Playing Card: 2 Pips", 1) and state.has("Lucy\'s Playing Card: 3 Pips", 1) and state.has("Lucy\'s Playing Card: 4 Pips", 1) and state.has("Hotspot: Tavern Fly", 1) and state.has("Hotspot: Alpine\'s Quandry Card Slots", 1) and state.can_reach("White House", "Region", 1) and state.has("Totem: Brog", 1) and state.has("Brog\'s Flickering Torch", 1) and state.has("Brog\'s Grue Egg", 1) and state.has("Hotspot: Cooking Pot", 1) and state.has("Brog\'s Plank", 1) and state.has("Hotspot: Skull Cage", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON, ZorkGrandInquisitorRegions.ENDGAME, 1
            ),
        )
