import unittest

from ..data_funcs import location_access_rule_for, entrance_access_rule_for
from ..enums import ZorkGrandInquisitorLocations, ZorkGrandInquisitorRegions


class DataFuncsTest(unittest.TestCase):
    def test_location_access_rule_for(self) -> None:
        # Single Item Requirement
        self.assertEqual(
            'lambda state: state.has("Plastic Six-Pack Holder", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.HELP_ME_CANT_BREATHE, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Spell: REZROV", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.IN_MAGIC_WE_TRUST, 1),
        )

        # Single Event Requirement
        self.assertEqual(
            'lambda state: state.has("Event: Cigar Accessible", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.ARREST_THE_VANDAL, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Event: 500 Zorkmid Bill Accessible", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.GETTING_SOME_CHANGE, 1),
        )

        # Multiple Item Requirements
        self.assertEqual(
            'lambda state: state.has("Hungus Lard", 1) and state.has("Sword", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.OUTSMART_THE_QUELBEES, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Spell: THROCK", 1) and state.has("Snapdragon", 1) and state.has("Hammer", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.PLANTS_ARE_MANS_BEST_FRIEND, 1),
        )

        # Multiple Mixed Requirements
        self.assertEqual(
            'lambda state: state.has("Event: Lantern (Dalboz) Accessible", 1) and state.has("Rope", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.MAGIC_FOREVER, 1),
        )

        self.assertEqual(
            'lambda state: state.has("Event: Door Smoked Cigar", 1) and state.has("Mead Light", 1) and state.has("ZIMDOR Scroll", 1)',
            location_access_rule_for(ZorkGrandInquisitorLocations.WANT_SOME_RYE_COURSE_YA_DO, 1),
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
            'lambda state: (state.has("Spell: IGRAM", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.GUE_TECH, ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY, 1
            ),
        )

        self.assertEqual(
            'lambda state: (state.has("Student ID", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
                ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
                1,
            ),
        )

        # Multiple Requirements AND
        self.assertEqual(
            'lambda state: (state.has("Map", 1) and state.has("Teleporter Destination: Spell Lab", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.HADES_SHORE,
                ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
                1,
            ),
        )

        self.assertEqual(
            'lambda state: (state.has("Large Telegraph Hammer", 1) and state.has("Spell: NARWILE", 1) and state.has("Totem: Lucy", 1) and state.has("Spell: YASTARD", 1) and state.has("Revealed: Lucy\'s Time Tunnel Items", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.MONASTERY,
                ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
                1,
            ),
        )

        # Multiple Requirements AND + OR
        self.assertEqual(
            'lambda state: (state.has("Sword", 1)) or (state.has("Map", 1) and state.has("Teleporter Destination: Dungeon Master\'s Lair", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.CROSSROADS,
                ZorkGrandInquisitorRegions.DM_LAIR,
                1,
            ),
        )

        self.assertEqual(
            'lambda state: (state.has("Spell: REZROV", 1)) or (state.has("Map", 1) and state.has("Teleporter Destination: GUE Tech", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.CROSSROADS,
                ZorkGrandInquisitorRegions.GUE_TECH,
                1,
            ),
        )

        # Multiple Requirements Regions
        self.assertEqual(
            'lambda state: (state.can_reach("Port Foozle - Past", "Region", 1) and state.can_reach("White House", "Region", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
                ZorkGrandInquisitorRegions.ENDGAME,
                1,
            ),
        )

        self.assertEqual(
            'lambda state: (state.can_reach("Dragon Archipelago", "Region", 1) and state.can_reach("Port Foozle - Past", "Region", 1))',
            entrance_access_rule_for(
                ZorkGrandInquisitorRegions.WHITE_HOUSE,
                ZorkGrandInquisitorRegions.ENDGAME,
                1,
            ),
        )
