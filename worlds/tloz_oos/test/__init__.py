from BaseClasses import LocationProgressType
from test.bases import WorldTestBase


class TestMinLocationsMaxItems(WorldTestBase):
    game = "The Legend of Zelda - Oracle of Seasons"
    options = {
        "required_essences": 0,
        "placed_essences": 0,
        "exclude_dungeons_without_essence": True,
        "shuffle_old_men": 0,
        "keysanity_small_keys": True,
        "keysanity_boss_keys": True,
        "keysanity_maps_compasses": True,
        "treehouse_old_man_requirement": 8,
        "deterministic_gasha_locations": 16,
        "enforce_potion_in_shop": True,
        "shuffle_golden_ore_spots": True,
        "cross_items": True
    }

    def test_more_items_than_locations(self):
        non_excluded_locations = {location for location in self.multiworld.get_locations(1) if
                                  location.progress_type != LocationProgressType.EXCLUDED and location.item is None}
        # Excluded locations that has been filled by the dungeon prefill are no longer excluded

        non_excluded_items = {item for item in self.multiworld.itempool if item.advancement or item.useful}
        self.assertGreaterEqual(len(non_excluded_locations), len(non_excluded_items),
                                f"Less prog items than non-excluded locations : {len(non_excluded_locations)} VS {len(non_excluded_items)}")
