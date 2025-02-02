from . import SVTestBase
from .assertion import WorldAssertMixin
from .. import options, items_by_group, Group


default_distribution = {trap.name: 10 for trap in items_by_group[Group.TRAP] if Group.DEPRECATED not in trap.groups}


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
        options.TrapDistribution.internal_name: default_distribution | {"Nudge Trap": 10, "Bark Trap": 1, "Meow Trap": 100, "Shuffle Trap": 0}
    }

    def test_fewer_barks_than_nudges_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_nudge = len([item for item in item_names if item == "Nudge Trap"])
        num_bark = len([item for item in item_names if item == "Bark Trap"])
        self.assertLess(num_bark, num_nudge)

    def test_more_meows_than_nudges_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_nudge = len([item for item in item_names if item == "Nudge Trap"])
        num_meow = len([item for item in item_names if item == "Meow Trap"])
        self.assertGreater(num_meow, num_nudge)

    def test_no_shuffles_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_shuffle = len([item for item in item_names if item == "Shuffle Trap"])
        self.assertEqual(num_shuffle, 0)

    def test_omitted_item_same_as_nudge_in_item_pool(self):
        items = self.multiworld.get_items()
        item_names = [item.name for item in items]
        num_time_flies = len([item for item in item_names if item == "Time Flies Trap"])
        num_debris = len([item for item in item_names if item == "Debris Trap"])
        num_bark = len([item for item in item_names if item == "Bark Trap"])
        num_meow = len([item for item in item_names if item == "Meow Trap"])
        self.assertLess(num_bark, num_time_flies)
        self.assertLess(num_bark, num_debris)
        self.assertGreater(num_meow, num_time_flies)
        self.assertGreater(num_meow, num_debris)

