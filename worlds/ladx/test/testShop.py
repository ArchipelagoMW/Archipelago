from typing import Optional

from Fill import parse_planned_blocks, distribute_planned_blocks, resolve_early_locations_for_planned
from Options import PlandoItems
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
        self.multiworld.worlds[1].options.plando_items = PlandoItems.from_any(self.options["plando_items"])
        self.multiworld.plando_item_blocks = parse_planned_blocks(self.multiworld)
        resolve_early_locations_for_planned(self.multiworld)
        distribute_planned_blocks(self.multiworld, [x for player in self.multiworld.plando_item_blocks
                                           for x in self.multiworld.plando_item_blocks[player]])
        call_all(self.multiworld, "pre_fill")
        
    def test_planned(self):
        """Tests plandoing swords in the shop."""
        location_names = ["Shop 200 Item (Mabe Village)", "Shop 980 Item (Mabe Village)"]
        locations = [self.multiworld.get_location(loc, 1) for loc in location_names]
        for loc in locations:
            self.assertEqual("Progressive Sword", loc.item.name)
            self.assertFalse(loc.can_reach(self.multiworld.state))
