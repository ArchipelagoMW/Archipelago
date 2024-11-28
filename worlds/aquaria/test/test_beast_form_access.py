"""
Author: Louis M
Date: Thu, 18 Apr 2024 18:45:56 +0000
Description: Unit test used to test accessibility of locations with and without the beast form
"""

from . import AquariaTestBase


class BeastFormAccessTest(AquariaTestBase):
    """Unit test used to test accessibility of locations with and without the beast form"""

    def test_beast_form_location(self) -> None:
        """Test locations that require beast form"""
        locations = [
            "Mermog cave, Piranha Egg",
            "Kelp Forest top left area, Jelly Egg",
            "Mithalas Cathedral, Mithalan Dress",
            "The Veil top right area, bulb at the top of the waterfall",
            "Sunken City, bulb on top of the boss area",
            "Octopus Cave, Dumbo Egg",
            "Beating the Golem",
            "Beating Mergog",
            "Beating Octopus Prime",
            "Sunken City cleared",
        ]
        items = [["Beast form"]]
        self.assertAccessDependency(locations, items)
