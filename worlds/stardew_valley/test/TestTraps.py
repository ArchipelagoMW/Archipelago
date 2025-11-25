import unittest

from .assertion import WorldAssertMixin
from .bases import SVTestBase
from .. import options, items_by_group, Group
from ..options import TrapDistribution

default_distribution = {trap.name: TrapDistribution.default_weight for trap in items_by_group[Group.TRAP] if Group.DEPRECATED not in trap.groups}
threshold_difference = 2
threshold_ballpark = 3


class TestTrapDifficultyCanRemoveAllTraps(WorldAssertMixin, SVTestBase):
    options = {
        options.QuestLocations.internal_name: 56,
        options.Fishsanity.internal_name: options.Fishsanity.option_all,
        options.Museumsanity.internal_name: options.Museumsanity.option_all,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Mods.internal_name: frozenset(options.Mods.valid_keys),
        options.TrapDifficulty.internal_name: options.TrapDifficulty.option_no_traps,
    }

    def test_no_traps_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = set(item.name for item in items)
        for trap in items_by_group[Group.TRAP]:
            if Group.DEPRECATED in trap.groups:
                continue
            self.assertNotIn(trap.name, item_names)


class TestDefaultDistributionHasAllTraps(WorldAssertMixin, SVTestBase):
    options = {
        options.QuestLocations.internal_name: 56,
        options.Fishsanity.internal_name: options.Fishsanity.option_all,
        options.Museumsanity.internal_name: options.Museumsanity.option_all,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Mods.internal_name: frozenset(options.Mods.valid_keys),
        options.TrapDifficulty.internal_name: options.TrapDifficulty.option_medium,
    }

    def test_all_traps_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = set(item.name for item in items)
        for trap in items_by_group[Group.TRAP]:
            if Group.DEPRECATED in trap.groups:
                continue
            self.assertIn(trap.name, item_names)


class TestDistributionIsRespectedAllTraps(WorldAssertMixin, SVTestBase):
    options = {
        options.QuestLocations.internal_name: 56,
        options.Fishsanity.internal_name: options.Fishsanity.option_all,
        options.Museumsanity.internal_name: options.Museumsanity.option_all,
        options.SpecialOrderLocations.internal_name: options.SpecialOrderLocations.option_board_qi,
        options.Shipsanity.internal_name: options.Shipsanity.option_everything,
        options.Cooksanity.internal_name: options.Cooksanity.option_all,
        options.Craftsanity.internal_name: options.Craftsanity.option_all,
        options.Mods.internal_name: frozenset(options.Mods.valid_keys),
        options.TrapDifficulty.internal_name: options.TrapDifficulty.option_medium,
        options.TrapDistribution.internal_name: default_distribution | {"Nudge Trap": 100, "Bark Trap": 1, "Meow Trap": 1000, "Shuffle Trap": 0}
    }

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if cls.skip_long_tests:
            raise unittest.SkipTest("Unstable tests disabled to not annoy anyone else when it rarely fails")

    def test_about_as_many_nudges_as_other_filler(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_nudge = len([item for item in item_names if item == "Nudge Trap"])
        other_fillers = ["Resource Pack: 4 Frozen Geode", "Resource Pack: 50 Wood", "Resource Pack: 5 Warp Totem: Farm",
                         "Resource Pack: 500 Money", "Resource Pack: 75 Copper Ore", "Resource Pack: 30 Speed-Gro"]
        at_least_one_in_ballpark = False
        for filler_item in other_fillers:
            num_filler = len([item for item in item_names if item == filler_item])
            diff_num = abs(num_filler - num_nudge)
            is_in_ballpark = diff_num <= threshold_ballpark
            at_least_one_in_ballpark = at_least_one_in_ballpark or is_in_ballpark
        self.assertTrue(at_least_one_in_ballpark)

    def test_fewer_barks_than_nudges_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_nudge = len([item for item in item_names if item == "Nudge Trap"])
        num_bark = len([item for item in item_names if item == "Bark Trap"])
        self.assertLess(num_bark, num_nudge - threshold_difference)

    def test_more_meows_than_nudges_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_nudge = len([item for item in item_names if item == "Nudge Trap"])
        num_meow = len([item for item in item_names if item == "Meow Trap"])
        self.assertGreater(num_meow, num_nudge + threshold_difference)

    def test_no_shuffles_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_shuffle = len([item for item in item_names if item == "Shuffle Trap"])
        self.assertEqual(0, num_shuffle)

    def test_omitted_item_same_as_nudge_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_time_flies = len([item for item in item_names if item == "Time Flies Trap"])
        num_debris = len([item for item in item_names if item == "Debris Trap"])
        num_bark = len([item for item in item_names if item == "Bark Trap"])
        num_meow = len([item for item in item_names if item == "Meow Trap"])
        self.assertLess(num_bark, num_time_flies - threshold_difference)
        self.assertLess(num_bark, num_debris - threshold_difference)
        self.assertGreater(num_meow, num_time_flies + threshold_difference)
        self.assertGreater(num_meow, num_debris + threshold_difference)
