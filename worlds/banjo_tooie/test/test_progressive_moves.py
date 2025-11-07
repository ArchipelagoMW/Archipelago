from typing import Dict
from ..Names import itemName
from ..Options import EnableNestsanity, ProgressiveBashAttack, ProgressiveBeakBuster, \
    ProgressiveEggAim, ProgressiveFlight, ProgressiveShoes, ProgressiveWaterTraining, \
    RandomizeBKMoveList, RandomizeBTMoveList, RandomizeNotes, RandomizeStopnSwap
from .test_logic import EasyTricksLogic, GlitchesLogic, HardTricksLogic, IntendedLogic
from . import BanjoTooieTestBase


class TestProgressiveMove(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "randomize_notes": RandomizeNotes.option_true
    }
    tested_items: Dict[str, int] = {}

    def test_item_pool(self) -> None:
        item_pool_names = [item.name for item in self.multiworld.itempool]
        starting_inventory_names = [item.name for item in self.multiworld.precollected_items[self.player]]
        for item, expected_count in self.tested_items.items():
            assert item_pool_names.count(item) + starting_inventory_names.count(item) == expected_count


class TestProgressiveBeakBuster(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_beak_buster": ProgressiveBeakBuster.option_true
    }
    tested_items = {
        itemName.PBBUST: 2,
        itemName.BBUST: 0,
        itemName.BDRILL: 0
    }


class TestNonProgressiveBeakBuster(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_beak_buster": ProgressiveBeakBuster.option_false
    }
    tested_items = {
        itemName.PBBUST: 0,
        itemName.BBUST: 1,
        itemName.BDRILL: 1
    }


class TestProgressiveShoes(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_shoes": ProgressiveShoes.option_true,
        "nestsanity": EnableNestsanity.option_true
    }
    tested_items = {
        itemName.PSHOES: 4,
        itemName.SSTRIDE: 0,
        itemName.TTRAIN: 0,
        itemName.SPRINGB: 0,
        itemName.CLAWBTS: 0,
    }


class TestNonProgressiveShoes(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_shoes": ProgressiveShoes.option_false,
    }
    tested_items = {
        itemName.PSHOES: 0,
        itemName.SSTRIDE: 1,
        itemName.TTRAIN: 1,
        itemName.SPRINGB: 1,
        itemName.CLAWBTS: 1,
    }


class TestProgressiveAdvancedWaterTraining(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_water_training": ProgressiveWaterTraining.option_advanced
    }
    tested_items = {
        itemName.PASWIM: 5,
        itemName.PSWIM: 0,
        itemName.DIVE: 0,
        itemName.DAIR: 0,
        itemName.FSWIM: 0,
        itemName.TTORP: 0,
        itemName.AUQAIM: 0,
    }


class TestProgressiveBasicWaterTraining(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_water_training": ProgressiveWaterTraining.option_basic
    }
    tested_items = {
        itemName.PASWIM: 0,
        itemName.PSWIM: 3,
        itemName.DIVE: 0,
        itemName.DAIR: 0,
        itemName.FSWIM: 0,
        itemName.TTORP: 1,
        itemName.AUQAIM: 1,
    }


class TestNonProgressiveWaterTraining(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_water_training": ProgressiveWaterTraining.option_none
    }
    tested_items = {
        itemName.PASWIM: 0,
        itemName.PSWIM: 0,
        itemName.DIVE: 1,
        itemName.DAIR: 1,
        itemName.FSWIM: 1,
        itemName.TTORP: 1,
        itemName.AUQAIM: 1,
    }


class TestProgressiveFlight(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_flight": ProgressiveFlight.option_true
    }
    tested_items = {
        itemName.PFLIGHT: 3,
        itemName.FPAD: 0,
        itemName.BBOMB: 0,
        itemName.AIREAIM: 0,
    }


class TestNonProgressiveFlight(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_flight": ProgressiveFlight.option_false
    }
    tested_items = {
        itemName.PFLIGHT: 0,
        itemName.FPAD: 1,
        itemName.BBOMB: 1,
        itemName.AIREAIM: 1,
    }


class TestProgressiveAdvancedEggAim(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_egg_aiming": ProgressiveEggAim.option_advanced
    }
    tested_items = {
        itemName.PAEGGAIM: 4,
        itemName.PEGGAIM: 0,
        itemName.EGGSHOOT: 0,
        itemName.AMAZEOGAZE: 0,
        itemName.EGGAIM: 0,
        itemName.BBLASTER: 0,
    }


class TestProgressiveBasicEggAim(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_egg_aiming": ProgressiveEggAim.option_basic
    }
    tested_items = {
        itemName.PAEGGAIM: 0,
        itemName.PEGGAIM: 2,
        itemName.EGGSHOOT: 0,
        itemName.AMAZEOGAZE: 1,
        itemName.EGGAIM: 0,
        itemName.BBLASTER: 1,
    }


class TestNonProgressiveEggAim(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "progressive_egg_aim": ProgressiveEggAim.option_none
    }
    tested_items = {
        itemName.PAEGGAIM: 0,
        itemName.PEGGAIM: 0,
        itemName.EGGSHOOT: 1,
        itemName.AMAZEOGAZE: 1,
        itemName.EGGAIM: 1,
        itemName.BBLASTER: 1,
    }


class TestProgressiveBash(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_true,
        "progressive_bash_attack": ProgressiveBashAttack.option_true
    }
    tested_items = {
        itemName.PBASH: 2,
        itemName.GRAT: 0,
        itemName.BBASH: 0,
    }


class TestNonProgressiveBash(TestProgressiveMove):
    options = {
        **TestProgressiveMove.options,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_true,
        "progressive_bash_attack": ProgressiveBashAttack.option_false
    }
    tested_items = {
        itemName.PBASH: 0,
        itemName.GRAT: 1,
        itemName.BBASH: 1,
    }


class TestTestProgressiveBeakBusterIntended(TestProgressiveBeakBuster, IntendedLogic):
    options = {
        **TestProgressiveBeakBuster.options,
        **IntendedLogic.options,
    }


class TestTestProgressiveBeakBusterEasyTricks(TestProgressiveBeakBuster, EasyTricksLogic):
    options = {
        **TestProgressiveBeakBuster.options,
        **EasyTricksLogic.options,
    }


class TestTestProgressiveBeakBusterHardTricks(TestProgressiveBeakBuster, HardTricksLogic):
    options = {
        **TestProgressiveBeakBuster.options,
        **HardTricksLogic.options,
    }


class TestTestProgressiveBeakBusterGlitches(TestProgressiveBeakBuster, GlitchesLogic):
    options = {
        **TestProgressiveBeakBuster.options,
        **GlitchesLogic.options,
    }


class TestTestNonProgressiveBeakBusterIntended(TestNonProgressiveBeakBuster, IntendedLogic):
    options = {
        **TestNonProgressiveBeakBuster.options,
        **IntendedLogic.options,
    }


class TestTestNonProgressiveBeakBusterEasyTricks(TestNonProgressiveBeakBuster, EasyTricksLogic):
    options = {
        **TestNonProgressiveBeakBuster.options,
        **EasyTricksLogic.options,
    }


class TestTestNonProgressiveBeakBusterHardTricks(TestNonProgressiveBeakBuster, HardTricksLogic):
    options = {
        **TestNonProgressiveBeakBuster.options,
        **HardTricksLogic.options,
    }


class TestTestNonProgressiveBeakBusterGlitches(TestNonProgressiveBeakBuster, GlitchesLogic):
    options = {
        **TestNonProgressiveBeakBuster.options,
        **GlitchesLogic.options,
    }


class TestTestProgressiveShoesIntended(TestProgressiveShoes, IntendedLogic):
    options = {
        **TestProgressiveShoes.options,
        **IntendedLogic.options,
        "nestsanity": EnableNestsanity.option_true

    }


class TestTestProgressiveShoesEasyTricks(TestProgressiveShoes, EasyTricksLogic):
    options = {
        **TestProgressiveShoes.options,
        **EasyTricksLogic.options,
        "nestsanity": EnableNestsanity.option_true

    }


class TestTestProgressiveShoesHardTricks(TestProgressiveShoes, HardTricksLogic):
    options = {
        **TestProgressiveShoes.options,
        **HardTricksLogic.options,
        "nestsanity": EnableNestsanity.option_true

    }


class TestTestProgressiveShoesGlitches(TestProgressiveShoes, GlitchesLogic):
    options = {
        **TestProgressiveShoes.options,
        **GlitchesLogic.options,
        "nestsanity": EnableNestsanity.option_true

    }


class TestTestNonProgressiveShoesIntended(TestNonProgressiveShoes, IntendedLogic):
    options = {
        **TestNonProgressiveShoes.options,
        **IntendedLogic.options,
    }


class TestTestNonProgressiveShoesEasyTricks(TestNonProgressiveShoes, EasyTricksLogic):
    options = {
        **TestNonProgressiveShoes.options,
        **EasyTricksLogic.options,
    }


class TestTestNonProgressiveShoesHardTricks(TestNonProgressiveShoes, HardTricksLogic):
    options = {
        **TestNonProgressiveShoes.options,
        **HardTricksLogic.options,
    }


class TestTestNonProgressiveShoesGlitches(TestNonProgressiveShoes, GlitchesLogic):
    options = {
        **TestNonProgressiveShoes.options,
        **GlitchesLogic.options,
    }


class TestTestProgressiveAdvancedWaterTrainingIntended(TestProgressiveAdvancedWaterTraining, IntendedLogic):
    options = {
        **TestProgressiveAdvancedWaterTraining.options,
        **IntendedLogic.options,
    }


class TestTestProgressiveAdvancedWaterTrainingEasyTricks(TestProgressiveAdvancedWaterTraining, EasyTricksLogic):
    options = {
        **TestProgressiveAdvancedWaterTraining.options,
        **EasyTricksLogic.options,
    }


class TestTestProgressiveAdvancedWaterTrainingHardTricks(TestProgressiveAdvancedWaterTraining, HardTricksLogic):
    options = {
        **TestProgressiveAdvancedWaterTraining.options,
        **HardTricksLogic.options,
    }


class TestTestProgressiveAdvancedWaterTrainingGlitches(TestProgressiveAdvancedWaterTraining, GlitchesLogic):
    options = {
        **TestProgressiveAdvancedWaterTraining.options,
        **GlitchesLogic.options,
    }


class TestTestProgressiveBasicWaterTrainingIntended(TestProgressiveBasicWaterTraining, IntendedLogic):
    options = {
        **TestProgressiveBasicWaterTraining.options,
        **IntendedLogic.options,
    }


class TestTestProgressiveBasicWaterTrainingEasyTricks(TestProgressiveBasicWaterTraining, EasyTricksLogic):
    options = {
        **TestProgressiveBasicWaterTraining.options,
        **EasyTricksLogic.options,
    }


class TestTestProgressiveBasicWaterTrainingHardTricks(TestProgressiveBasicWaterTraining, HardTricksLogic):
    options = {
        **TestProgressiveBasicWaterTraining.options,
        **HardTricksLogic.options,
    }


class TestTestProgressiveBasicWaterTrainingGlitches(TestProgressiveBasicWaterTraining, GlitchesLogic):
    options = {
        **TestProgressiveBasicWaterTraining.options,
        **GlitchesLogic.options,
    }


class TestTestNonProgressiveWaterTrainingIntended(TestNonProgressiveWaterTraining, IntendedLogic):
    options = {
        **TestNonProgressiveWaterTraining.options,
        **IntendedLogic.options,
    }


class TestTestNonProgressiveWaterTrainingEasyTricks(TestNonProgressiveWaterTraining, EasyTricksLogic):
    options = {
        **TestNonProgressiveWaterTraining.options,
        **EasyTricksLogic.options,
    }


class TestTestNonProgressiveWaterTrainingHardTricks(TestNonProgressiveWaterTraining, HardTricksLogic):
    options = {
        **TestNonProgressiveWaterTraining.options,
        **HardTricksLogic.options,
    }


class TestTestNonProgressiveWaterTrainingGlitches(TestNonProgressiveWaterTraining, GlitchesLogic):
    options = {
        **TestNonProgressiveWaterTraining.options,
        **GlitchesLogic.options,
    }


class TestTestProgressiveFlightIntended(TestProgressiveFlight, IntendedLogic):
    options = {
        **TestProgressiveFlight.options,
        **IntendedLogic.options,
    }


class TestTestProgressiveFlightEasyTricks(TestProgressiveFlight, EasyTricksLogic):
    options = {
        **TestProgressiveFlight.options,
        **EasyTricksLogic.options,
    }


class TestTestProgressiveFlightHardTricks(TestProgressiveFlight, HardTricksLogic):
    options = {
        **TestProgressiveFlight.options,
        **HardTricksLogic.options,
    }


class TestTestProgressiveFlightGlitches(TestProgressiveFlight, GlitchesLogic):
    options = {
        **TestProgressiveFlight.options,
        **GlitchesLogic.options,
    }


class TestTestNonProgressiveFlightIntended(TestNonProgressiveFlight, IntendedLogic):
    options = {
        **TestNonProgressiveFlight.options,
        **IntendedLogic.options,
    }


class TestTestNonProgressiveFlightEasyTricks(TestNonProgressiveFlight, EasyTricksLogic):
    options = {
        **TestNonProgressiveFlight.options,
        **EasyTricksLogic.options,
    }


class TestTestNonProgressiveFlightHardTricks(TestNonProgressiveFlight, HardTricksLogic):
    options = {
        **TestNonProgressiveFlight.options,
        **HardTricksLogic.options,
    }


class TestTestNonProgressiveFlightGlitches(TestNonProgressiveFlight, GlitchesLogic):
    options = {
        **TestNonProgressiveFlight.options,
        **GlitchesLogic.options,
    }


class TestTestProgressiveAdvancedEggAimIntended(TestProgressiveAdvancedEggAim, IntendedLogic):
    options = {
        **TestProgressiveAdvancedEggAim.options,
        **IntendedLogic.options,
    }


class TestTestProgressiveAdvancedEggAimEasyTricks(TestProgressiveAdvancedEggAim, EasyTricksLogic):
    options = {
        **TestProgressiveAdvancedEggAim.options,
        **EasyTricksLogic.options,
    }


class TestTestProgressiveAdvancedEggAimHardTricks(TestProgressiveAdvancedEggAim, HardTricksLogic):
    options = {
        **TestProgressiveAdvancedEggAim.options,
        **HardTricksLogic.options,
    }


class TestTestProgressiveAdvancedEggAimGlitches(TestProgressiveAdvancedEggAim, GlitchesLogic):
    options = {
        **TestProgressiveAdvancedEggAim.options,
        **GlitchesLogic.options,
    }


class TestTestProgressiveBasicEggAimIntended(TestProgressiveBasicEggAim, IntendedLogic):
    options = {
        **TestProgressiveBasicEggAim.options,
        **IntendedLogic.options,
    }


class TestTestProgressiveBasicEggAimEasyTricks(TestProgressiveBasicEggAim, EasyTricksLogic):
    options = {
        **TestProgressiveBasicEggAim.options,
        **EasyTricksLogic.options,
    }


class TestTestProgressiveBasicEggAimHardTricks(TestProgressiveBasicEggAim, HardTricksLogic):
    options = {
        **TestProgressiveBasicEggAim.options,
        **HardTricksLogic.options,
    }


class TestTestProgressiveBasicEggAimGlitches(TestProgressiveBasicEggAim, GlitchesLogic):
    options = {
        **TestProgressiveBasicEggAim.options,
        **GlitchesLogic.options,
    }


class TestTestNonProgressiveEggAimIntended(TestNonProgressiveEggAim, IntendedLogic):
    options = {
        **TestNonProgressiveEggAim.options,
        **IntendedLogic.options,
    }


class TestTestNonProgressiveEggAimEasyTricks(TestNonProgressiveEggAim, EasyTricksLogic):
    options = {
        **TestNonProgressiveEggAim.options,
        **EasyTricksLogic.options,
    }


class TestTestNonProgressiveEggAimHardTricks(TestNonProgressiveEggAim, HardTricksLogic):
    options = {
        **TestNonProgressiveEggAim.options,
        **HardTricksLogic.options,
    }


class TestTestNonProgressiveEggAimGlitches(TestNonProgressiveEggAim, GlitchesLogic):
    options = {
        **TestNonProgressiveEggAim.options,
        **GlitchesLogic.options,
    }


class TestTestProgressiveBashIntended(TestProgressiveBash, IntendedLogic):
    options = {
        **TestProgressiveBash.options,
        **IntendedLogic.options,
    }


class TestTestProgressiveBashEasyTricks(TestProgressiveBash, EasyTricksLogic):
    options = {
        **TestProgressiveBash.options,
        **EasyTricksLogic.options,
    }


class TestTestProgressiveBashHardTricks(TestProgressiveBash, HardTricksLogic):
    options = {
        **TestProgressiveBash.options,
        **HardTricksLogic.options,
    }


class TestTestProgressiveBashGlitches(TestProgressiveBash, GlitchesLogic):
    options = {
        **TestProgressiveBash.options,
        **GlitchesLogic.options,
    }


class TestTestNonProgressiveBashIntended(TestNonProgressiveBash, IntendedLogic):
    options = {
        **TestNonProgressiveBash.options,
        **IntendedLogic.options,
    }


class TestTestNonProgressiveBashEasyTricks(TestNonProgressiveBash, EasyTricksLogic):
    options = {
        **TestNonProgressiveBash.options,
        **EasyTricksLogic.options,
    }


class TestTestNonProgressiveBashHardTricks(TestNonProgressiveBash, HardTricksLogic):
    options = {
        **TestNonProgressiveBash.options,
        **HardTricksLogic.options,
    }


class TestTestNonProgressiveBashGlitches(TestNonProgressiveBash, GlitchesLogic):
    options = {
        **TestNonProgressiveBash.options,
        **GlitchesLogic.options,
    }
