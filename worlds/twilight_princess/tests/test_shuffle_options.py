from copy import deepcopy
from enum import Enum
import itertools
from traceback import print_exception
from typing import Any
from BaseClasses import get_seed
from Fill import FillError
from Options import OptionError

from worlds.twilight_princess_apworld.options import *
from . import TwilightPrincessWorldTestBase

bool_options = [
    "golden_bugs_shuffled",
    "sky_characters_shuffled",
    "npc_items_shuffled",
    "shop_items_shuffled",
    "hidden_skills_shuffled",
    "poe_shuffled",
    "overworld_shuffled",
    "heart_piece_shuffled",
    "dungeons_shuffled",
    "early_shadow_crystal",
]
bool_values = [True, False]
dungeon_options = [
    "small_key_settings",
    "big_key_settings",
    "map_and_compass_settings",
]
dungeon_values = [
    DungeonItem.option_startwith,
    DungeonItem.option_vanilla,
    DungeonItem.option_own_dungeon,
    DungeonItem.option_any_dungeon,
    DungeonItem.option_anywhere,
]


def generate_all_shuffle_options_bool(dungeon_value: int) -> list[dict[str, Any]]:

    option_dict = {}

    # Add boolean options
    for option in bool_options:
        option_dict[option] = bool_values

    # Add dungeon options
    for option in dungeon_options:
        option_dict[option] = [dungeon_value]

    options = list(option_dict.keys())
    value_sets = [option_dict[option] for option in options]

    # Create the cartesian product of all value sets
    combinations = itertools.product(*value_sets)

    result = []
    for combination in combinations:
        # Create a dictionary for this combination
        combination_dict = {}
        for i, option in enumerate(options):
            combination_dict[option] = combination[i]
        result.append(combination_dict)

    return result


def generate_all_shuffle_options_dungeon(bool_value: bool) -> list[dict[str, Any]]:

    option_dict = {}

    # Add boolean options
    for option in bool_options:
        option_dict[option] = [True]

    # Add dungeon options
    for option in dungeon_options:
        option_dict[option] = dungeon_values

    option_dict["dungeons_shuffled"] = [bool_value]

    options = list(option_dict.keys())
    value_sets = [option_dict[option] for option in options]

    # Create the cartesian product of all value sets
    combinations = itertools.product(*value_sets)

    result = []
    for combination in combinations:
        # Create a dictionary for this combination
        combination_dict = {}
        for i, option in enumerate(options):
            combination_dict[option] = combination[i]
        result.append(combination_dict)

    return result


class TestShuffleOptions(TwilightPrincessWorldTestBase):
    run_default_tests = True
    options = {
        "golden_bugs_shuffled": True,
        "sky_characters_shuffled": True,
        "npc_items_shuffled": True,
        "shop_items_shuffled": True,
        "hidden_skills_shuffled": True,
        "poe_shuffled": True,
        "overworld_shuffled": True,
        "heart_piece_shuffled": True,
        "dungeons_shuffled": True,
        "small_key_settings": DungeonItem.option_anywhere,
        "big_key_settings": DungeonItem.option_anywhere,
        "map_and_compass_settings": DungeonItem.option_anywhere,
        # "skip_prologue": True,
        # "faron_twilight_cleared": True,
        # "eldin_twilight_cleared": True,
        # "lanayru_twilight_cleared": True,
        # "skip_mdh": True,
        "open_map": False,
        "increase_wallet": False,
        "transform_anywhere": False,
        "bonks_do_damage": False,
        "damage_magnification": DungeonItem.option_vanilla,
        "skip_lakebed_entrance": True,
        "skip_arbiters_grounds_entrance": True,
        "skip_snowpeak_entrance": True,
    }

    def test_all_dungeon_options(self):
        if not self.run_long_tests:
            return
        combinations = generate_all_shuffle_options_dungeon(True)
        combinations.extend(generate_all_shuffle_options_dungeon(False))
        valid = True
        pass_count = 0
        for combination in combinations:
            with self.subTest(
                "Twilight Princess Options", game=self.game, seed=self.multiworld.seed
            ):
                for key, val in combination.items():
                    self.options[key] = val
                if any([self.options[key] for key in bool_options]):
                    try:
                        self.world_setup(get_seed())
                        # self.assertBeatable(True)
                        pass_count += 1
                    except Exception as e:
                        self.logger.info(
                            f"Dungeon: {e=},{print_exception(e)}\n{self.options=}\n"
                        )
                        valid = False
        self.assertTrue(valid, f"Dungeon options cause error check logs. {pass_count=}")

    def test_all_bool_options(self):
        if not self.run_long_tests:
            return
        combinations = generate_all_shuffle_options_bool(DungeonItem.option_vanilla)
        combinations.extend(
            generate_all_shuffle_options_bool(DungeonItem.option_anywhere)
        )
        valid = True
        pass_count = 0
        for combination in combinations:
            with self.subTest(
                "Twilight Princess Options", game=self.game, seed=self.multiworld.seed
            ):
                for key, val in combination.items():
                    self.options[key] = val
                if any([self.options[key] for key in bool_options]):
                    try:
                        self.world_setup(get_seed())
                        # self.assertBeatable(True)
                        pass_count += 1
                    except Exception as e:
                        # self.logger.info("a")
                        # Only one of Dungeons and Overworld can be false
                        # So if one of them is true then parse the error
                        if (
                            self.options["overworld_shuffled"]
                            or self.options["dungeons_shuffled"]
                        ):
                            self.logger.info(
                                f"Bool: {e=},{print_exception(e)}\n{self.options=}\n"
                            )
                            valid = False
                        else:
                            # When Both overworld and dungeon are false make sure it throws an option error
                            if not isinstance(e, OptionError):
                                self.logger.info(
                                    f"Bool: {e=},{print_exception(e)}\n{self.options=}\n"
                                )
                                valid = False
        self.assertTrue(valid, f"Bool options cause error check logs. {pass_count=}")

    def test_no_shuffle_options(self):
        self.options["golden_bugs_shuffled"] = False
        self.options["sky_characters_shuffled"] = False
        self.options["npc_items_shuffled"] = False
        self.options["shop_items_shuffled"] = False
        self.options["hidden_skills_shuffled"] = False
        self.options["poe_shuffled"] = False
        self.options["overworld_shuffled"] = False
        self.options["heart_piece_shuffled"] = False
        self.options["dungeons_shuffled"] = False
        self.assertRaises(OptionError, self.setUp)

    def test_default_shuffle_options(self):

        self.options = {
            "logic_rules": LogicRules.default,
            "castle_requirements": CastleRequirements.default,
            "palace_requirements": PalaceRequirements.default,
            "faron_woods_logic": FaronWoodsLogic.default,
            "golden_bugs_shuffled": GoldenBugsShuffled.default,
            "sky_characters_shuffled": SkyCharactersShuffled.default,
            "npc_items_shuffled": NpcItemsShuffled.default,
            "shop_items_shuffled": ShopItemsShuffled.default,
            "hidden_skills_shuffled": HiddenSkillsShuffled.default,
            "poe_shuffled": PoeShuffled.default,
            "overworld_shuffled": OverWoldShuffled.default,
            "heart_piece_shuffled": HeartPieceShuffled.default,
            "dungeons_shuffled": DungeonsShuffled.default,
            "small_key_settings": SmallKeySettings.option_anywhere,
            "big_key_settings": BigKeySettings.option_anywhere,
            "map_and_compass_settings": MapAndCompassSettings.option_anywhere,
            "dungeon_rewards_progression": DungeonRewardsProgression.default,
            # "small_keys_on_bosses": SmallKeysOnBosses.default,
            # "skip_prologue": SkipPrologue.default,
            # "faron_twilight_cleared": FaronTwilightCleared.default,
            # "eldin_twilight_cleared": EldinTwilightCleared.default,
            # "lanayru_twilight_cleared": LanayruTwilightCleared.default,
            # "skip_mdh": SkipMdh.default,
            "open_map": OpenMap.default,
            "increase_wallet": IncreaseWalletCapacity.default,
            "transform_anywhere": TransformAnywhere.default,
            "bonks_do_damage": BonksDoDamage.default,
            "damage_magnification": DamageMagnification.default,
            "skip_lakebed_entrance": SkipLakebedEntrance.default,
            "skip_arbiters_grounds_entrance": SkipArbitersGroundsEntrance.default,
            "skip_snowpeak_entrance": SkipSnowpeakEntrance.default,
            "skip_city_in_the_sky_entrance": SkipCityInTheSkyEntrance.default,
            "goron_mines_entrance": GoronMinesEntrance.default,
            "tot_entrance": TotEntrance.default,
            "early_shadow_crystal": EarlyShadowCrystal.default,
        }
        self.world_setup(get_seed())
        # self.assertBeatable(True)
