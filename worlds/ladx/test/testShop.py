from typing import Optional

from Fill import distribute_planned
from test.general import setup_solo_multiworld
from worlds.AutoWorld import call_all
from . import LADXTestBase
from .. import LinksAwakeningWorld


class PlandoTest(LADXTestBase):
    options = {
        "plando_items": [{
            "items": {
                "Progressive Sword": 2,
            },
            "locations": [
                "Shop 200 Item (Mabe Village)",
                "Shop 980 Item (Mabe Village)",
            ],
        }],
    }
    
    def world_setup(self, seed: Optional[int] = None) -> None:
        self.multiworld = setup_solo_multiworld(
            LinksAwakeningWorld,
            ("generate_early", "create_regions", "create_items", "set_rules", "generate_basic")
        )
        self.multiworld.plando_items[1] = self.options["plando_items"]
        distribute_planned(self.multiworld)
        call_all(self.multiworld, "pre_fill")
        
    def test_planned(self):
        """Tests plandoing swords in the shop."""
        location_names = ["Shop 200 Item (Mabe Village)", "Shop 980 Item (Mabe Village)"]
        locations = [self.multiworld.get_location(loc, 1) for loc in location_names]
        for loc in locations:
            self.assertEqual("Progressive Sword", loc.item.name)
            self.assertFalse(loc.can_reach(self.multiworld.state))
