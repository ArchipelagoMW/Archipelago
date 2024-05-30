"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the spirit form
"""

from worlds.aquaria.test import AquariaTestBase


class SpiritFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the spirit form"""

    def test_spirit_form_location(self) -> None:
        """Test locations that require spirit form"""
        locations = [
            "The veil bottom area, bulb in the spirit path",
            "Mithalas city castle, Trident head",
            "Open water skeleton path, King skull",
            "Kelp forest bottom left area, Walker baby",
            "Abyss right area, bulb behind the rock in the whale room",
            "The whale, Verse egg",
            "Ice cave, bulb in the room to the right",
            "Ice cave, first bulb in the top exit room",
            "Ice cave, second bulb in the top exit room",
            "Ice cave, third bulb in the top exit room",
            "Ice cave, bulb in the left room",
            "Bubble cave, bulb in the left cave wall",
            "Bubble cave, bulb in the right cave wall (behind the ice crystal)",
            "Bubble cave, Verse egg",
            "Sunken city left area, Girl costume",
            "Beating Mantis Shrimp Prime",
            "First secret",
            "Arnassi ruins, Arnassi armor",
        ]
        items = [["Spirit form"]]
        self.assertAccessDependency(locations, items)
