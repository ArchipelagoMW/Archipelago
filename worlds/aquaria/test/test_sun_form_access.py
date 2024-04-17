from worlds.aquaria.test import AquariaTestBase


class SunFormAccessTest(AquariaTestBase):

    def test_sun_form_location(self) -> None:
        """Test locations that require sun form"""
        locations = [
            "First secret",
            "The whale, Verse egg",
            "Abyss right area, bulb behind the rock in the whale room",
            "Octopus cave, Dumbo Egg",
            "Beating Octopus Prime",
            "Final boss area, bulb in the boss third form room",
            "Objective complete"
        ]
        items = [["Sun form"]]
        self.assertAccessDependency(locations, items)
