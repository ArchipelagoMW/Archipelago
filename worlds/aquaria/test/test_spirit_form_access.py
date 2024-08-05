"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the spirit form
"""

from . import AquariaTestBase
from ..Items import ItemNames


class SpiritFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the spirit form"""

    def test_spirit_form_location(self) -> None:
        """Test locations that require spirit form"""
        locations = [
            "The Veil bottom area, bulb in the spirit path",
            "Mithalas City Castle, Trident Head",
            "Open Waters skeleton path, King Skull",
            "Kelp Forest bottom left area, Walker Baby",
            "Abyss right area, bulb behind the rock in the whale room",
            "The Whale, Verse Egg",
            "Ice Cavern, bulb in the room to the right",
            "Ice Cavern, first bulb in the top exit room",
            "Ice Cavern, second bulb in the top exit room",
            "Ice Cavern, third bulb in the top exit room",
            "Ice Cavern, bulb in the left room",
            "Bubble Cave, bulb in the left cave wall",
            "Bubble Cave, bulb in the right cave wall (behind the ice crystal)",
            "Bubble Cave, Verse Egg",
            "Sunken City left area, Girl Costume",
            "Beating Mantis Shrimp Prime",
            "First Secret",
        ]
        items = [[ItemNames.SPIRIT_FORM]]
        self.assertAccessDependency(locations, items)
