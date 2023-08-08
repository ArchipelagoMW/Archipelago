from typing import Optional

from Fill import distribute_planned
from . import LADXTestBase


class PlandoTest(LADXTestBase):
    options = {
        "plando_items": [{
            "items": {
                "Progressive Sword": 2
            },
            "locations": [
                "Shop 200 Item (Mabe Village)",
                "Shop 980 Item (Mabe Village)"
            ]
        }]
    }
        
    def test_planned(self):
        """Tests plandoing swords in the shop."""
        self.multiworld.plando_items[1] = self.options["plando_items"]
        distribute_planned(self.multiworld)
        self.assertEqual("Progressive Sword",
                         self.multiworld.get_location("Shop 200 Item (Mabe Village)", 1).item.name)
        self.assertEqual("Progressive Sword",
                         self.multiworld.get_location("Shop 980 Item (Mabe Village)", 1).item.name)
