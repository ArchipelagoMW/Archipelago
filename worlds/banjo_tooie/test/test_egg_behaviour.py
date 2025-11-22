from ..Names import itemName, locationName
from ..Options import EggsBehaviour, RandomizeBKMoveList, RandomizeBTMoveList, RandomizeNotes
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class BlueEggStartVanillaMovesTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_false,
        "egg_behaviour": EggsBehaviour.option_start_with_blue_eggs,
    }

    def test_blue_egg_in_starting_inventory(self):
        assert itemName.BEGGS not in [item.name for item in self.multiworld.itempool]
        assert itemName.BEGGS in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for egg in [itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            assert egg not in item_pool_names

    def test_prefill(self) -> None:
        silos_to_vanilla_item = {
            locationName.FEGGS: itemName.FEGGS,
            locationName.GEGGS: itemName.GEGGS,
            locationName.IEGGS: itemName.IEGGS,
            locationName.CEGGS: itemName.CEGGS,
        }

        for silo, egg in silos_to_vanilla_item.items():
            assert self.world.get_location(silo).item.name == egg


class BlueEggStartRandomizedMovesTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "egg_behaviour": EggsBehaviour.option_start_with_blue_eggs,
    }

    def test_blue_egg_in_starting_inventory(self):
        assert itemName.BEGGS not in [item.name for item in self.multiworld.itempool]
        assert itemName.BEGGS in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for egg in [itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            assert egg in item_pool_names


class RandomStartEggTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "egg_behaviour": EggsBehaviour.option_random_starting_egg,
        "randomize_notes": RandomizeNotes(True),
    }

    def test_starting_inventory(self) -> None:
        start_inventory_names = [item.name for item in self.multiworld.precollected_items[self.player]]
        eggs_in_inventory = 0
        for egg in [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            if egg in start_inventory_names:
                eggs_in_inventory += 1
        assert eggs_in_inventory == 1

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        eggs_in_pool = 0
        for egg in [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            if egg in item_pool_names:
                eggs_in_pool += 1
        assert eggs_in_pool == 4  # One is in the starting inventory.


class RandomSimpleStartEggTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "egg_behaviour": EggsBehaviour.option_simple_random_starting_egg,
        "randomize_notes": RandomizeNotes(True),
    }

    def test_starting_inventory(self) -> None:
        start_inventory_names = [item.name for item in self.multiworld.precollected_items[self.player]]
        eggs_in_inventory = 0
        for egg in [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS]:
            if egg in start_inventory_names:
                eggs_in_inventory += 1
        assert eggs_in_inventory == 1

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        eggs_in_pool = 0
        for egg in [itemName.BEGGS, itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            if egg in item_pool_names:
                eggs_in_pool += 1
        assert eggs_in_pool == 4  # One is in the starting inventory.


class ProgressiveEggsTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "egg_behaviour": EggsBehaviour.option_progressive_eggs,
    }

    def test_blue_egg_in_starting_inventory(self):
        assert itemName.BEGGS not in [item.name for item in self.multiworld.itempool]
        assert itemName.BEGGS in [item.name for item in self.multiworld.precollected_items[self.player]]

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        for egg in [itemName.FEGGS, itemName.GEGGS, itemName.IEGGS, itemName.CEGGS]:
            assert egg not in item_pool_names

        assert item_pool_names.count(itemName.PEGGS) == 4


class TestBlueEggStartVanillaMovesIntended(BlueEggStartVanillaMovesTest, IntendedLogic):
    options = {
        **IntendedLogic.options,
        **BlueEggStartVanillaMovesTest.options,
    }


class TestBlueEggStartVanillaMovesEasyTricks(BlueEggStartVanillaMovesTest, EasyTricksLogic):
    options = {
        **EasyTricksLogic.options,
        **BlueEggStartVanillaMovesTest.options,
    }


class TestBlueEggStartVanillaMovesHardTricks(BlueEggStartVanillaMovesTest, HardTricksLogic):
    options = {
        **HardTricksLogic.options,
        **BlueEggStartVanillaMovesTest.options,
    }


class TestBlueEggStartVanillaMovesGlitches(BlueEggStartVanillaMovesTest, GlitchesLogic):
    options = {
        **GlitchesLogic.options,
        **BlueEggStartVanillaMovesTest.options,
    }


class TestBlueEggStartRandomizedMovesIntended(BlueEggStartRandomizedMovesTest, IntendedLogic):
    options = {
        **IntendedLogic.options,
        **BlueEggStartRandomizedMovesTest.options,
    }


class TestBlueEggStartRandomizedMovesEasyTricks(BlueEggStartRandomizedMovesTest, EasyTricksLogic):
    options = {
        **EasyTricksLogic.options,
        **BlueEggStartRandomizedMovesTest.options,
    }


class TestBlueEggStartRandomizedMovesHardTricks(BlueEggStartRandomizedMovesTest, HardTricksLogic):
    options = {
        **HardTricksLogic.options,
        **BlueEggStartRandomizedMovesTest.options,
    }


class TestBlueEggStartRandomizedMovesGlitches(BlueEggStartRandomizedMovesTest, GlitchesLogic):
    options = {
        **GlitchesLogic.options,
        **BlueEggStartRandomizedMovesTest.options,
    }


class TestRandomStartEggIntended(RandomStartEggTest, IntendedLogic):
    options = {
        **IntendedLogic.options,
        **RandomStartEggTest.options,
    }


class TestRandomStartEggEasyTricks(RandomStartEggTest, EasyTricksLogic):
    options = {
        **EasyTricksLogic.options,
        **RandomStartEggTest.options,
    }


class TestRandomStartEggHardTricks(RandomStartEggTest, HardTricksLogic):
    options = {
        **HardTricksLogic.options,
        **RandomStartEggTest.options,
    }


class TestRandomStartEggGlitches(RandomStartEggTest, GlitchesLogic):
    options = {
        **GlitchesLogic.options,
        **RandomStartEggTest.options,
    }


class TestProgressiveEggsIntended(ProgressiveEggsTest, IntendedLogic):
    options = {
        **IntendedLogic.options,
        **ProgressiveEggsTest.options,
    }


class TestProgressiveEggsEasyTricks(ProgressiveEggsTest, EasyTricksLogic):
    options = {
        **EasyTricksLogic.options,
        **ProgressiveEggsTest.options,
    }


class TestProgressiveEggsHardTricks(ProgressiveEggsTest, HardTricksLogic):
    options = {
        **HardTricksLogic.options,
        **ProgressiveEggsTest.options,
    }


class TestProgressiveEggsGlitches(ProgressiveEggsTest, GlitchesLogic):
    options = {
        **GlitchesLogic.options,
        **ProgressiveEggsTest.options,
    }
