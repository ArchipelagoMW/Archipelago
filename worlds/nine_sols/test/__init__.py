import os
import sys

from test.bases import WorldTestBase, CollectionState

path = os.path.dirname(__file__)
path = os.path.join(path, 'shared_static_logic')
if path not in sys.path:
    sys.path.append(path)


class NineSolsTestBase(WorldTestBase):
    game = "Nine Sols"

    def makeStateWith(self, item_names: list[str]) -> CollectionState:
        state = CollectionState(self.multiworld)
        for i in self.get_items_by_name(item_names):
            state.collect(i)
        return state

    def getLocationCount(self) -> int:
        return sum(1 for _ in self.multiworld.get_locations(1))

    def isReachableWith(self, location_name: str, item_names: list[str]) -> bool:
        state = self.makeStateWith(item_names)
        return state.can_reach_location(location_name, 1)

    def assertReachableWith(self, location_name: str, item_names: list[str]) -> None:
        self.assertTrue(self.isReachableWith(location_name, item_names))

    def assertNotReachableWith(self, location_name: str, item_names: list[str]) -> None:
        self.assertFalse(self.isReachableWith(location_name, item_names))

    # we can't realistically prove there is no other combination of items that works,
    # so what this actually tests is having all item_names is enough to reach the location,
    # and missing any one of those item_names is not enough to reach it.
    def requiresAllOf(self, location_name: str, item_names: list[str]) -> bool:
        items = self.get_items_by_name(item_names)
        state = CollectionState(self.multiworld)

        # check that it can be reached with all the items
        for i in items:
            state.collect(i)
        if not state.can_reach_location(location_name, 1):
            return False

        # check that removing any one item makes it unreachable again
        for i in items:
            state.remove(i)
            if state.can_reach_location(location_name, 1):
                return False
            state.collect(i)

        return True

    # Note that pre-collected items like Launch Codes are ignored by AP reachability logic,
    # so it doesn't matter
    def assertRequiresAllOf(self, location_name: str, item_names: list[str]) -> None:
        self.assertTrue(self.requiresAllOf(location_name, item_names))

    # Checks that the listed locations requiresAllOf(item_names), and that
    # every other location in the multiworld does not requiresAllOf(item_names).
    # This may have unintuitive results for locations which can be reached multiple ways.
    def assertEverywhereRequiringAllOf(self, location_names: list[str], item_names: list[str]) -> None:
        for location in self.multiworld.get_locations():
            if location.name in location_names:
                self.assertTrue(
                    self.requiresAllOf(location.name, item_names),
                    f"location '{location}' should require exactly {item_names} to reach, but it doesn't"
                )
            else:
                self.assertFalse(
                    self.requiresAllOf(location.name, item_names),
                    f"location '{location}' was not one of the locations being asserted on, "
                    f"but it requires exactly {item_names} to reach, so it should be"
                )


class TestDefaultWorld(NineSolsTestBase):
    options = {}

    def test_default_world(self):
        self.assertEqual(self.getLocationCount(), 323)  # 318 default locations + 5 events

        # breathing tests for logic assertion helpers
        self.assertReachableWith("Central Hall: Examine Launch Memoral", [])
        self.assertNotReachableWith("Central Hall: Examine Council Tenets", [])
        self.assertReachableWith("Central Hall: Examine Council Tenets", [
            "Mystic Nymph: Scout Mode"
        ])

        # control for TestSkipSoulscapePlatforming
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [])
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash"
        ])
        self.assertReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",  # to reach CC
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",  # to trigger Lady E
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash", "Tai-Chi Kick"  # to reach and defeat Lady E
        ])


class TestShuffleSolSealsOff(NineSolsTestBase):
    options = {
        "shuffle_sol_seals": False
    }

    def test_default_world(self):
        self.assertEqual(
            self.multiworld.get_location("Kuafu's Vital Sanctum", self.player).item.name,
            "Seal of Kuafu"
        )


class TestSkipSoulscapePlatforming(NineSolsTestBase):
    options = {
        "skip_soulscape_platforming": True
    }

    def test_default_world(self):
        # when the soulscape is skipped, TCK is no longer logically necessary to reach Lady E
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [])
        self.assertNotReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",
            "Event - Lady Ethereal Soulscape Unlocked"
        ])
        self.assertReachableWith("Cortex Center: Defeat Lady Ethereal", [
            "Mystic Nymph: Scout Mode", "Charged Strike",  # to reach CC
            "Seal of Kuafu", "Seal of Goumang", "Seal of Yanlao", "Seal of Jiequan",  # to trigger Lady E
            "Event - Lady Ethereal Soulscape Unlocked", "Air Dash"  # to reach and defeat Lady E
        ])

