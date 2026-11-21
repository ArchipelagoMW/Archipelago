"""
Consolidated test file for Banjo-Tooie using combinatorial testing.

This file combines multiple options per test to reduce total test count by ~10x
while ensuring every option value is tested with each logic type.

Coverage guarantee:
- All 4 logic types (intended, easy_tricks, hard_tricks, glitches)
- Every option value appears at least once per logic type

For the full test suite with individual tests for each option, see the main repo:
https://github.com/jjjj12212/AP-Banjo-Tooie
"""

from . import BanjoTooieTestBase, BanjoTooieHintTestBase
from .test_logic import IntendedLogic, EasyTricksLogic, HardTricksLogic, GlitchesLogic
from ..Options import (
    VictoryCondition, OpenHag1, MinigameHuntLength, BossHuntLength,
    JinjoFamilyRescueLength, TokensInPool, TokenHuntLength,
    RandomizeBKMoveList, RandomizeBTMoveList, JamjarsSiloCosts,
    EggsBehaviour, ProgressiveBeakBuster, ProgressiveShoes,
    ProgressiveWaterTraining, ProgressiveFlight, ProgressiveEggAim, ProgressiveBashAttack,
    RandomizeNotes, RandomizeTrebleClefs, RandomizeJinjos, RandomizeDoubloons,
    RandomizeCheatoPages, RandomizeCheatoRewards, RandomizeHoneycombs, EnableHoneyBRewards,
    RandomizeBigTentTickets, RandomizeGreenRelics, RandomizeBeans, RandomizeGlowbos,
    RandomizeStopnSwap, RandomizeWorldDinoRoar, EnableNestsanity, RandomizeSignposts,
    RandomizeTrainStationSwitches, RandomizeChuffyTrain, RandomizeWarpPads,
    RandomizeSilos, OpenSilos, SkipPuzzles, RandomizeWorldOrder,
    RandomizeWorldLoadingZones, RandomizeBossLoadingZones, Backdoors, GIFrontDoor,
    SignpostHints, SignpostMoveHints, AddSignpostHintsToArchipelagoHints, HintClarity,
    SkipKlungo, KingJingalingHasJiggy,
)
from ..Names import locationName


class Intended_A(BanjoTooieTestBase, IntendedLogic):
    """HAG1, All TRUE toggles for item pool, progressive moves enabled"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
        "open_hag1": OpenHag1.option_true,
        "randomize_beans": RandomizeBeans.option_true,
        "randomize_glowbos": RandomizeGlowbos.option_true,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_true,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_true,
        "randomize_cheato": RandomizeCheatoPages.option_true,
        "cheato_rewards": RandomizeCheatoRewards.option_true,
        "randomize_honeycombs": RandomizeHoneycombs.option_true,
        "honeyb_rewards": EnableHoneyBRewards.option_true,
        "randomize_tickets": RandomizeBigTentTickets.option_true,
        "randomize_green_relics": RandomizeGreenRelics.option_true,
        "randomize_doubloons": RandomizeDoubloons.option_true,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "randomize_treble": RandomizeTrebleClefs.option_true,
        "nestsanity": EnableNestsanity.option_true,
        "randomize_signposts": RandomizeSignposts.option_true,
        "randomize_notes": RandomizeNotes.option_true,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "progressive_beak_buster": ProgressiveBeakBuster.option_true,
        "progressive_shoes": ProgressiveShoes.option_true,
        "progressive_water_training": ProgressiveWaterTraining.option_advanced,
        "progressive_flight": ProgressiveFlight.option_true,
        "progressive_egg_aim": ProgressiveEggAim.option_advanced,
        "progressive_bash_attack": ProgressiveBashAttack.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "eggs_behaviour": EggsBehaviour.option_progressive_eggs,
        "jamjars_silo_costs": JamjarsSiloCosts.option_randomize,
    }


class Intended_B(BanjoTooieTestBase, IntendedLogic):
    """Minigame Hunt (short), world rando, train, backdoors"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_start,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_true,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_true,
        "randomize_warp_pads": RandomizeWarpPads.option_true,
        "randomize_silos": RandomizeSilos.option_true,
        "backdoors": Backdoors.option_true,
        "randomize_stations": RandomizeTrainStationSwitches.option_true,
        "randomize_chuffy": RandomizeChuffyTrain.option_true,
        "skip_klungo": SkipKlungo.option_true,
        "skip_puzzles": SkipPuzzles.option_true,
        "open_gi_frontdoor": GIFrontDoor.option_true,
        "jingaling_jiggy": KingJingalingHasJiggy.option_true,
        "open_silos": OpenSilos.range_end,
    }


class Intended_C(BanjoTooieHintTestBase, IntendedLogic):
    """Boss Hunt (long), choice option alternatives, cryptic hints"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt,
        "boss_hunt_length": BossHuntLength.range_end,
        "signpost_hints": 30,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_always,
        "hint_clarity": HintClarity.option_cryptic,
        "randomize_bk_moves": RandomizeBKMoveList.option_mcjiggy_special,
        "eggs_behaviour": EggsBehaviour.option_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_progressive,
        "progressive_water_training": ProgressiveWaterTraining.option_basic,
        "progressive_egg_aim": ProgressiveEggAim.option_basic,
    }


class Intended_D(BanjoTooieHintTestBase, IntendedLogic):
    """Jinjo Rescue (long), more choice alternatives, progression hints"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_end,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "signpost_hints": 30,
        "signpost_move_hints": 10,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_progression,
        "hint_clarity": HintClarity.option_clear,
        "eggs_behaviour": EggsBehaviour.option_simple_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_vanilla,
        "progressive_water_training": ProgressiveWaterTraining.option_none,
        "progressive_egg_aim": ProgressiveEggAim.option_none,
    }


class Intended_E(BanjoTooieTestBase, IntendedLogic):
    """Wonderwing, BK moves none"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_wonderwing_challenge,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "eggs_behaviour": EggsBehaviour.option_start_with_blue_eggs,
    }


class Intended_F(BanjoTooieTestBase, IntendedLogic):
    """Boss Hunt + HAG1 (short)"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1,
        "boss_hunt_length": BossHuntLength.range_start,
    }


class Intended_G(BanjoTooieTestBase, IntendedLogic):
    """Token Hunt (max tokens)"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_end,
        "token_hunt_length": TokenHuntLength.range_start,
        "randomize_signposts": RandomizeSignposts.option_true,
        "nestsanity": EnableNestsanity.option_true,
    }


class Intended_H(BanjoTooieTestBase, IntendedLogic):
    """All FALSE toggles, range_start values"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
        "open_hag1": OpenHag1.option_false,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "signpost_hints": SignpostHints.range_start,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_never,
        "randomize_beans": RandomizeBeans.option_false,
        "randomize_glowbos": RandomizeGlowbos.option_false,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_false,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_false,
        "randomize_cheato": RandomizeCheatoPages.option_false,
        "cheato_rewards": RandomizeCheatoRewards.option_false,
        "randomize_honeycombs": RandomizeHoneycombs.option_false,
        "honeyb_rewards": EnableHoneyBRewards.option_false,
        "randomize_tickets": RandomizeBigTentTickets.option_false,
        "randomize_green_relics": RandomizeGreenRelics.option_false,
        "randomize_doubloons": RandomizeDoubloons.option_false,
        "randomize_jinjos": RandomizeJinjos.option_false,
        "randomize_treble": RandomizeTrebleClefs.option_false,
        "nestsanity": EnableNestsanity.option_false,
        "randomize_signposts": RandomizeSignposts.option_false,
        "randomize_notes": RandomizeNotes.option_false,
        "randomize_bt_moves": RandomizeBTMoveList.option_false,
        "progressive_beak_buster": ProgressiveBeakBuster.option_false,
        "progressive_shoes": ProgressiveShoes.option_false,
        "progressive_flight": ProgressiveFlight.option_false,
        "progressive_bash_attack": ProgressiveBashAttack.option_false,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_false,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_false,
        "randomize_warp_pads": RandomizeWarpPads.option_false,
        "randomize_silos": RandomizeSilos.option_false,
        "randomize_worlds": RandomizeWorldOrder.option_false,
        "backdoors": Backdoors.option_false,
        "randomize_stations": RandomizeTrainStationSwitches.option_false,
        "randomize_chuffy": RandomizeChuffyTrain.option_false,
        "skip_klungo": SkipKlungo.option_false,
        "skip_puzzles": SkipPuzzles.option_false,
        "open_gi_frontdoor": GIFrontDoor.option_false,
        "jingaling_jiggy": KingJingalingHasJiggy.option_false,
        "open_silos": OpenSilos.range_start,
    }


class Intended_I(BanjoTooieTestBase, IntendedLogic):
    """Minigame Hunt (long)"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_end,
    }


class Intended_J(BanjoTooieTestBase, IntendedLogic):
    """Jinjo Rescue (short)"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_start,
        "randomize_jinjos": RandomizeJinjos.option_true,
    }


class Intended_K(BanjoTooieTestBase, IntendedLogic):
    """Token Hunt with different ranges"""
    options = {
        **IntendedLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_start,
        "token_hunt_length": TokenHuntLength.range_end,
    }


class EasyTricks_A(BanjoTooieTestBase, EasyTricksLogic):
    """Minigame Hunt, All TRUE toggles, progressive moves"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_end,
        "open_hag1": OpenHag1.option_true,
        "randomize_beans": RandomizeBeans.option_true,
        "randomize_glowbos": RandomizeGlowbos.option_true,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_true,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_true,
        "randomize_cheato": RandomizeCheatoPages.option_true,
        "cheato_rewards": RandomizeCheatoRewards.option_true,
        "randomize_honeycombs": RandomizeHoneycombs.option_true,
        "honeyb_rewards": EnableHoneyBRewards.option_true,
        "randomize_tickets": RandomizeBigTentTickets.option_true,
        "randomize_green_relics": RandomizeGreenRelics.option_true,
        "randomize_doubloons": RandomizeDoubloons.option_true,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "randomize_treble": RandomizeTrebleClefs.option_true,
        "nestsanity": EnableNestsanity.option_true,
        "randomize_signposts": RandomizeSignposts.option_true,
        "randomize_notes": RandomizeNotes.option_true,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "progressive_beak_buster": ProgressiveBeakBuster.option_true,
        "progressive_shoes": ProgressiveShoes.option_true,
        "progressive_water_training": ProgressiveWaterTraining.option_advanced,
        "progressive_flight": ProgressiveFlight.option_true,
        "progressive_egg_aim": ProgressiveEggAim.option_advanced,
        "progressive_bash_attack": ProgressiveBashAttack.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "eggs_behaviour": EggsBehaviour.option_progressive_eggs,
        "jamjars_silo_costs": JamjarsSiloCosts.option_randomize,
    }


class EasyTricks_B(BanjoTooieTestBase, EasyTricksLogic):
    """Boss Hunt, world rando, train, backdoors"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt,
        "boss_hunt_length": BossHuntLength.range_start,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_true,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_true,
        "randomize_warp_pads": RandomizeWarpPads.option_true,
        "randomize_silos": RandomizeSilos.option_true,
        "randomize_worlds": RandomizeWorldOrder.option_true,
        "backdoors": Backdoors.option_true,
        "randomize_stations": RandomizeTrainStationSwitches.option_true,
        "randomize_chuffy": RandomizeChuffyTrain.option_true,
        "skip_klungo": SkipKlungo.option_true,
        "skip_puzzles": SkipPuzzles.option_true,
        "open_gi_frontdoor": GIFrontDoor.option_true,
        "jingaling_jiggy": KingJingalingHasJiggy.option_true,
        "open_silos": OpenSilos.range_end,
    }


class EasyTricks_C(BanjoTooieHintTestBase, EasyTricksLogic):
    """Jinjo Rescue, choice alternatives, cryptic hints"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_start,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "signpost_hints": 30,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_always,
        "hint_clarity": HintClarity.option_cryptic,
        "randomize_bk_moves": RandomizeBKMoveList.option_mcjiggy_special,
        "eggs_behaviour": EggsBehaviour.option_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_progressive,
        "progressive_water_training": ProgressiveWaterTraining.option_basic,
        "progressive_egg_aim": ProgressiveEggAim.option_basic,
    }


class EasyTricks_D(BanjoTooieHintTestBase, EasyTricksLogic):
    """Wonderwing, more choice alternatives, progression hints"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_wonderwing_challenge,
        "signpost_hints": 30,
        "signpost_move_hints": 10,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_progression,
        "hint_clarity": HintClarity.option_clear,
        "eggs_behaviour": EggsBehaviour.option_simple_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_vanilla,
        "progressive_water_training": ProgressiveWaterTraining.option_none,
        "progressive_egg_aim": ProgressiveEggAim.option_none,
    }


class EasyTricks_E(BanjoTooieTestBase, EasyTricksLogic):
    """HAG1, BK moves none"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "eggs_behaviour": EggsBehaviour.option_start_with_blue_eggs,
    }


class EasyTricks_F(BanjoTooieTestBase, EasyTricksLogic):
    """Boss Hunt + HAG1"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1,
        "boss_hunt_length": BossHuntLength.range_end,
    }


class EasyTricks_G(BanjoTooieTestBase, EasyTricksLogic):
    """Token Hunt"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_start,
        "token_hunt_length": TokenHuntLength.range_end,
    }


class EasyTricks_H(BanjoTooieTestBase, EasyTricksLogic):
    """All FALSE toggles"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
        "open_hag1": OpenHag1.option_false,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "signpost_hints": SignpostHints.range_start,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_never,
        "randomize_beans": RandomizeBeans.option_false,
        "randomize_glowbos": RandomizeGlowbos.option_false,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_false,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_false,
        "randomize_cheato": RandomizeCheatoPages.option_false,
        "cheato_rewards": RandomizeCheatoRewards.option_false,
        "randomize_honeycombs": RandomizeHoneycombs.option_false,
        "honeyb_rewards": EnableHoneyBRewards.option_false,
        "randomize_tickets": RandomizeBigTentTickets.option_false,
        "randomize_green_relics": RandomizeGreenRelics.option_false,
        "randomize_doubloons": RandomizeDoubloons.option_false,
        "randomize_jinjos": RandomizeJinjos.option_false,
        "randomize_treble": RandomizeTrebleClefs.option_false,
        "nestsanity": EnableNestsanity.option_false,
        "randomize_signposts": RandomizeSignposts.option_false,
        "randomize_notes": RandomizeNotes.option_false,
        "randomize_bt_moves": RandomizeBTMoveList.option_false,
        "progressive_beak_buster": ProgressiveBeakBuster.option_false,
        "progressive_shoes": ProgressiveShoes.option_false,
        "progressive_flight": ProgressiveFlight.option_false,
        "progressive_bash_attack": ProgressiveBashAttack.option_false,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_false,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_false,
        "randomize_warp_pads": RandomizeWarpPads.option_false,
        "randomize_silos": RandomizeSilos.option_false,
        "randomize_worlds": RandomizeWorldOrder.option_false,
        "backdoors": Backdoors.option_false,
        "randomize_stations": RandomizeTrainStationSwitches.option_false,
        "randomize_chuffy": RandomizeChuffyTrain.option_false,
        "skip_klungo": SkipKlungo.option_false,
        "skip_puzzles": SkipPuzzles.option_false,
        "open_gi_frontdoor": GIFrontDoor.option_false,
        "jingaling_jiggy": KingJingalingHasJiggy.option_false,
        "open_silos": OpenSilos.range_start,
    }


class EasyTricks_I(BanjoTooieTestBase, EasyTricksLogic):
    """Minigame Hunt (short)"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_start,
    }


class EasyTricks_J(BanjoTooieTestBase, EasyTricksLogic):
    """Jinjo Rescue (long)"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_end,
        "randomize_jinjos": RandomizeJinjos.option_true,
    }


class EasyTricks_K(BanjoTooieTestBase, EasyTricksLogic):
    """Token Hunt (max tokens)"""
    options = {
        **EasyTricksLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_end,
        "token_hunt_length": TokenHuntLength.range_start,
        "randomize_signposts": RandomizeSignposts.option_true,
        "nestsanity": EnableNestsanity.option_true,
    }


class HardTricks_A(BanjoTooieTestBase, HardTricksLogic):
    """Boss Hunt, All TRUE toggles, progressive moves"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt,
        "boss_hunt_length": BossHuntLength.range_end,
        "open_hag1": OpenHag1.option_true,
        "randomize_beans": RandomizeBeans.option_true,
        "randomize_glowbos": RandomizeGlowbos.option_true,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_true,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_true,
        "randomize_cheato": RandomizeCheatoPages.option_true,
        "cheato_rewards": RandomizeCheatoRewards.option_true,
        "randomize_honeycombs": RandomizeHoneycombs.option_true,
        "honeyb_rewards": EnableHoneyBRewards.option_true,
        "randomize_tickets": RandomizeBigTentTickets.option_true,
        "randomize_green_relics": RandomizeGreenRelics.option_true,
        "randomize_doubloons": RandomizeDoubloons.option_true,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "randomize_treble": RandomizeTrebleClefs.option_true,
        "nestsanity": EnableNestsanity.option_true,
        "randomize_signposts": RandomizeSignposts.option_true,
        "randomize_notes": RandomizeNotes.option_true,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "progressive_beak_buster": ProgressiveBeakBuster.option_true,
        "progressive_shoes": ProgressiveShoes.option_true,
        "progressive_water_training": ProgressiveWaterTraining.option_advanced,
        "progressive_flight": ProgressiveFlight.option_true,
        "progressive_egg_aim": ProgressiveEggAim.option_advanced,
        "progressive_bash_attack": ProgressiveBashAttack.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "eggs_behaviour": EggsBehaviour.option_progressive_eggs,
        "jamjars_silo_costs": JamjarsSiloCosts.option_randomize,
    }


class HardTricks_B(BanjoTooieTestBase, HardTricksLogic):
    """Jinjo Rescue, world rando, train, backdoors"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_end,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_true,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_true,
        "randomize_warp_pads": RandomizeWarpPads.option_true,
        "randomize_silos": RandomizeSilos.option_true,
        "randomize_worlds": RandomizeWorldOrder.option_true,
        "backdoors": Backdoors.option_true,
        "randomize_stations": RandomizeTrainStationSwitches.option_true,
        "randomize_chuffy": RandomizeChuffyTrain.option_true,
        "skip_klungo": SkipKlungo.option_true,
        "skip_puzzles": SkipPuzzles.option_true,
        "open_gi_frontdoor": GIFrontDoor.option_true,
        "jingaling_jiggy": KingJingalingHasJiggy.option_true,
        "open_silos": OpenSilos.range_end,
    }


class HardTricks_C(BanjoTooieHintTestBase, HardTricksLogic):
    """Wonderwing, choice alternatives, cryptic hints"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_wonderwing_challenge,
        "signpost_hints": 30,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_always,
        "hint_clarity": HintClarity.option_cryptic,
        "randomize_bk_moves": RandomizeBKMoveList.option_mcjiggy_special,
        "eggs_behaviour": EggsBehaviour.option_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_progressive,
        "progressive_water_training": ProgressiveWaterTraining.option_basic,
        "progressive_egg_aim": ProgressiveEggAim.option_basic,
    }


class HardTricks_D(BanjoTooieHintTestBase, HardTricksLogic):
    """Boss Hunt + HAG1, more choice alternatives, progression hints"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1,
        "boss_hunt_length": BossHuntLength.range_start,
        "signpost_hints": 30,
        "signpost_move_hints": 10,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_progression,
        "hint_clarity": HintClarity.option_clear,
        "eggs_behaviour": EggsBehaviour.option_simple_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_vanilla,
        "progressive_water_training": ProgressiveWaterTraining.option_none,
        "progressive_egg_aim": ProgressiveEggAim.option_none,
    }


class HardTricks_E(BanjoTooieTestBase, HardTricksLogic):
    """Token Hunt (max tokens), BK moves none"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_end,
        "token_hunt_length": TokenHuntLength.range_end,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "eggs_behaviour": EggsBehaviour.option_start_with_blue_eggs,
        "randomize_signposts": RandomizeSignposts.option_true,
        "nestsanity": EnableNestsanity.option_true,
    }


class HardTricks_F(BanjoTooieTestBase, HardTricksLogic):
    """HAG1"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
    }


class HardTricks_G(BanjoTooieTestBase, HardTricksLogic):
    """Minigame Hunt"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_start,
    }


class HardTricks_H(BanjoTooieTestBase, HardTricksLogic):
    """All FALSE toggles"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
        "open_hag1": OpenHag1.option_false,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "signpost_hints": SignpostHints.range_start,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_never,
        "randomize_beans": RandomizeBeans.option_false,
        "randomize_glowbos": RandomizeGlowbos.option_false,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_false,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_false,
        "randomize_cheato": RandomizeCheatoPages.option_false,
        "cheato_rewards": RandomizeCheatoRewards.option_false,
        "randomize_honeycombs": RandomizeHoneycombs.option_false,
        "honeyb_rewards": EnableHoneyBRewards.option_false,
        "randomize_tickets": RandomizeBigTentTickets.option_false,
        "randomize_green_relics": RandomizeGreenRelics.option_false,
        "randomize_doubloons": RandomizeDoubloons.option_false,
        "randomize_jinjos": RandomizeJinjos.option_false,
        "randomize_treble": RandomizeTrebleClefs.option_false,
        "nestsanity": EnableNestsanity.option_false,
        "randomize_signposts": RandomizeSignposts.option_false,
        "randomize_notes": RandomizeNotes.option_false,
        "randomize_bt_moves": RandomizeBTMoveList.option_false,
        "progressive_beak_buster": ProgressiveBeakBuster.option_false,
        "progressive_shoes": ProgressiveShoes.option_false,
        "progressive_flight": ProgressiveFlight.option_false,
        "progressive_bash_attack": ProgressiveBashAttack.option_false,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_false,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_false,
        "randomize_warp_pads": RandomizeWarpPads.option_false,
        "randomize_silos": RandomizeSilos.option_false,
        "randomize_worlds": RandomizeWorldOrder.option_false,
        "backdoors": Backdoors.option_false,
        "randomize_stations": RandomizeTrainStationSwitches.option_false,
        "randomize_chuffy": RandomizeChuffyTrain.option_false,
        "skip_klungo": SkipKlungo.option_false,
        "skip_puzzles": SkipPuzzles.option_false,
        "open_gi_frontdoor": GIFrontDoor.option_false,
        "jingaling_jiggy": KingJingalingHasJiggy.option_false,
        "open_silos": OpenSilos.range_start,
    }


class HardTricks_I(BanjoTooieTestBase, HardTricksLogic):
    """Minigame Hunt (long)"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_end,
    }


class HardTricks_J(BanjoTooieTestBase, HardTricksLogic):
    """Jinjo Rescue (short)"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_start,
        "randomize_jinjos": RandomizeJinjos.option_true,
    }


class HardTricks_K(BanjoTooieTestBase, HardTricksLogic):
    """Token Hunt ranges"""
    options = {
        **HardTricksLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_start,
        "token_hunt_length": TokenHuntLength.range_start,
    }


class Glitches_A(BanjoTooieTestBase, GlitchesLogic):
    """Jinjo Rescue, All TRUE toggles, progressive moves"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_start,
        "open_hag1": OpenHag1.option_true,
        "randomize_beans": RandomizeBeans.option_true,
        "randomize_glowbos": RandomizeGlowbos.option_true,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_true,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_true,
        "randomize_cheato": RandomizeCheatoPages.option_true,
        "cheato_rewards": RandomizeCheatoRewards.option_true,
        "randomize_honeycombs": RandomizeHoneycombs.option_true,
        "honeyb_rewards": EnableHoneyBRewards.option_true,
        "randomize_tickets": RandomizeBigTentTickets.option_true,
        "randomize_green_relics": RandomizeGreenRelics.option_true,
        "randomize_doubloons": RandomizeDoubloons.option_true,
        "randomize_jinjos": RandomizeJinjos.option_true,
        "randomize_treble": RandomizeTrebleClefs.option_true,
        "nestsanity": EnableNestsanity.option_true,
        "randomize_signposts": RandomizeSignposts.option_true,
        "randomize_notes": RandomizeNotes.option_true,
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "progressive_beak_buster": ProgressiveBeakBuster.option_true,
        "progressive_shoes": ProgressiveShoes.option_true,
        "progressive_water_training": ProgressiveWaterTraining.option_advanced,
        "progressive_flight": ProgressiveFlight.option_true,
        "progressive_egg_aim": ProgressiveEggAim.option_advanced,
        "progressive_bash_attack": ProgressiveBashAttack.option_true,
        "randomize_bk_moves": RandomizeBKMoveList.option_all,
        "eggs_behaviour": EggsBehaviour.option_progressive_eggs,
        "jamjars_silo_costs": JamjarsSiloCosts.option_randomize,
    }


class Glitches_B(BanjoTooieTestBase, GlitchesLogic):
    """Wonderwing, world rando, train, backdoors"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_wonderwing_challenge,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_true,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_true,
        "randomize_warp_pads": RandomizeWarpPads.option_true,
        "randomize_silos": RandomizeSilos.option_true,
        "randomize_worlds": RandomizeWorldOrder.option_true,
        "backdoors": Backdoors.option_true,
        "randomize_stations": RandomizeTrainStationSwitches.option_true,
        "randomize_chuffy": RandomizeChuffyTrain.option_true,
        "skip_klungo": SkipKlungo.option_true,
        "skip_puzzles": SkipPuzzles.option_true,
        "open_gi_frontdoor": GIFrontDoor.option_true,
        "jingaling_jiggy": KingJingalingHasJiggy.option_true,
        "open_silos": OpenSilos.range_end,
    }


class Glitches_C(BanjoTooieHintTestBase, GlitchesLogic):
    """Boss Hunt + HAG1, choice alternatives, cryptic hints"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt_and_hag1,
        "boss_hunt_length": BossHuntLength.range_start,
        "signpost_hints": 30,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_always,
        "hint_clarity": HintClarity.option_cryptic,
        "randomize_bk_moves": RandomizeBKMoveList.option_mcjiggy_special,
        "eggs_behaviour": EggsBehaviour.option_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_progressive,
        "progressive_water_training": ProgressiveWaterTraining.option_basic,
        "progressive_egg_aim": ProgressiveEggAim.option_basic,
    }


class Glitches_D(BanjoTooieHintTestBase, GlitchesLogic):
    """Token Hunt, more choice alternatives, progression hints"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_start,
        "token_hunt_length": TokenHuntLength.range_start,
        "signpost_hints": 30,
        "signpost_move_hints": 10,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_progression,
        "hint_clarity": HintClarity.option_clear,
        "eggs_behaviour": EggsBehaviour.option_simple_random_starting_egg,
        "jamjars_silo_costs": JamjarsSiloCosts.option_vanilla,
        "progressive_water_training": ProgressiveWaterTraining.option_none,
        "progressive_egg_aim": ProgressiveEggAim.option_none,
    }


class Glitches_E(BanjoTooieTestBase, GlitchesLogic):
    """HAG1, BK moves none"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "eggs_behaviour": EggsBehaviour.option_start_with_blue_eggs,
    }


class Glitches_F(BanjoTooieTestBase, GlitchesLogic):
    """Minigame Hunt"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_end,
    }


class Glitches_G(BanjoTooieTestBase, GlitchesLogic):
    """Boss Hunt"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_boss_hunt,
        "boss_hunt_length": BossHuntLength.range_end,
    }


class Glitches_H(BanjoTooieTestBase, GlitchesLogic):
    """All FALSE toggles"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_hag1,
        "open_hag1": OpenHag1.option_false,
        "randomize_bk_moves": RandomizeBKMoveList.option_none,
        "signpost_hints": SignpostHints.range_start,
        "signpost_move_hints": SignpostMoveHints.range_start,
        "add_signpost_hints_to_ap": AddSignpostHintsToArchipelagoHints.option_never,
        "randomize_beans": RandomizeBeans.option_false,
        "randomize_glowbos": RandomizeGlowbos.option_false,
        "randomize_stop_n_swap": RandomizeStopnSwap.option_false,
        "randomize_dino_roar": RandomizeWorldDinoRoar.option_false,
        "randomize_cheato": RandomizeCheatoPages.option_false,
        "cheato_rewards": RandomizeCheatoRewards.option_false,
        "randomize_honeycombs": RandomizeHoneycombs.option_false,
        "honeyb_rewards": EnableHoneyBRewards.option_false,
        "randomize_tickets": RandomizeBigTentTickets.option_false,
        "randomize_green_relics": RandomizeGreenRelics.option_false,
        "randomize_doubloons": RandomizeDoubloons.option_false,
        "randomize_jinjos": RandomizeJinjos.option_false,
        "randomize_treble": RandomizeTrebleClefs.option_false,
        "nestsanity": EnableNestsanity.option_false,
        "randomize_signposts": RandomizeSignposts.option_false,
        "randomize_notes": RandomizeNotes.option_false,
        "randomize_bt_moves": RandomizeBTMoveList.option_false,
        "progressive_beak_buster": ProgressiveBeakBuster.option_false,
        "progressive_shoes": ProgressiveShoes.option_false,
        "progressive_flight": ProgressiveFlight.option_false,
        "progressive_bash_attack": ProgressiveBashAttack.option_false,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_false,
        "randomize_boss_loading_zones": RandomizeBossLoadingZones.option_false,
        "randomize_warp_pads": RandomizeWarpPads.option_false,
        "randomize_silos": RandomizeSilos.option_false,
        "randomize_worlds": RandomizeWorldOrder.option_false,
        "backdoors": Backdoors.option_false,
        "randomize_stations": RandomizeTrainStationSwitches.option_false,
        "randomize_chuffy": RandomizeChuffyTrain.option_false,
        "skip_klungo": SkipKlungo.option_false,
        "skip_puzzles": SkipPuzzles.option_false,
        "open_gi_frontdoor": GIFrontDoor.option_false,
        "jingaling_jiggy": KingJingalingHasJiggy.option_false,
        "open_silos": OpenSilos.range_start,
    }


class Glitches_I(BanjoTooieTestBase, GlitchesLogic):
    """Minigame Hunt (short)"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_minigame_hunt,
        "minigame_hunt_length": MinigameHuntLength.range_start,
    }


class Glitches_J(BanjoTooieTestBase, GlitchesLogic):
    """Jinjo Rescue (long)"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_jinjo_family_rescue,
        "jinjo_family_rescue_length": JinjoFamilyRescueLength.range_end,
        "randomize_jinjos": RandomizeJinjos.option_true,
    }


class Glitches_K(BanjoTooieTestBase, GlitchesLogic):
    """Token Hunt (max tokens)"""
    options = {
        **GlitchesLogic.options,
        "victory_condition": VictoryCondition.option_token_hunt,
        "tokens_in_pool": TokensInPool.range_end,
        "token_hunt_length": TokenHuntLength.range_end,
        "randomize_signposts": RandomizeSignposts.option_true,
        "nestsanity": EnableNestsanity.option_true,
    }
