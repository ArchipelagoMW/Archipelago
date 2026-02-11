from contextlib import contextmanager
import logging
import os
from typing import Any
import pytest  # type: ignore
from BaseClasses import get_seed
from test.bases import WorldTestBase
from worlds.twilight_princess_apworld.options import *

DEFAULT_TEST_SEED = get_seed()


class TwilightPrincessWorldTestBase(WorldTestBase):
    game = "Twilight Princess"
    player = 1
    options: dict[str, Any]

    logger = logging.Logger("Test_logger")
    logger.addHandler(
        logging.FileHandler("worlds\\twilight_princess_apworld\\tests\\logs.log")
    )

    run_long_tests = False
    run_generation_tests = False
    auto_construct = True

    # Make sure that options are rest for every test
    @pytest.fixture(autouse=True)
    def run_around_tests(self):
        self.options = {
            # "progression_balancing": 50,
            # "accessibility": 0,
            # "local_items": set(),
            # "non_local_items": set(),
            # "start_inventory": {},
            # "start_hints": set(),
            # "start_location_hints": set(),
            # "exclude_locations": set(),
            # "priority_locations": set(),
            # "item_links": [],
            # "start_inventory_from_pool": {},
            # "death_link": 0,
            # "logic_rules": LogicRules.option_glitchless,
            # "castle_requirements": CastleRequirements.option_open,
            # "palace_requirements": PalaceRequirements.option_open,
            # "faron_woods_logic": FaronWoodsLogic.option_open,
            "golden_bugs_shuffled": True,
            "sky_characters_shuffled": True,
            "npc_items_shuffled": True,
            "shop_items_shuffled": True,
            "hidden_skills_shuffled": True,
            "poe_shuffled": True,
            "overworld_shuffled": True,
            "heart_piece_shuffled": True,
            "dungeons_shuffled": True,
            "small_key_settings": SmallKeySettings.option_anywhere,
            "big_key_settings": BigKeySettings.option_anywhere,
            "map_and_compass_settings": MapAndCompassSettings.option_anywhere,
            # "dungeon_rewards_progression": True,
            # "small_keys_on_bosses": 0,
            # "skip_prologue": True,
            # "faron_twilight_cleared": True,
            # "eldin_twilight_cleared": True,
            # "lanayru_twilight_cleared": True,
            # "skip_mdh": True,
            "open_map": False,
            "increase_wallet": False,
            "transform_anywhere": False,
            "bonks_do_damage": False,
            "damage_magnification": DamageMagnification.option_vanilla,
            "skip_lakebed_entrance": True,
            "skip_arbiters_grounds_entrance": True,
            "skip_snowpeak_entrance": True,
            # "skip_city_in_the_sky_entrance": True,
            # "goron_mines_entrance": GoronMinesEntrance.option_open,
            # "tot_entrance": TotEntrance.option_open,
            "early_shadow_crystal": True,
        }
        yield
