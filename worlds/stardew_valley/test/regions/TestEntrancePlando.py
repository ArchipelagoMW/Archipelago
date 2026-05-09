from collections import deque
from collections.abc import Collection
from unittest.mock import Mock, patch

from BaseClasses import Entrance, MultiWorld, Region, get_seed
from worlds.stardew_valley.strings.ap_names.ap_option_names import EntranceRandomizationBehaviorOptionName

from ... import options
from ...mods.mod_data import ModNames
from ...options import EntranceRandomization, ExcludeGingerIsland, SkillProgression
from ...options.options import EntranceRandomizationBehavior, EntrancePlando, all_mods
from ...regions.entrance_rando import connect_regions, create_entrance_rando_target, prepare_mod_data
from ...regions.model import ConnectionData, RandomizationFlag, RegionData
from ...strings.entrance_names import Entrance as EntranceName
from ...strings.region_names import Region as RegionName
from ..assertion import WorldAssertMixin
from ..bases import SVTestBase, SVTestCase, setup_solo_multiworld, solo_multiworld


class TestEntrancePlandoCoupled(SVTestBase):
    options = {
        EntranceRandomization: EntranceRandomization.option_everywhere,
        EntranceRandomizationBehavior: {},
        EntrancePlando: {
            EntranceName.farmhouse_to_farm: EntranceName.town_to_beach,
            EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
            EntranceName.farm_to_forest: EntranceName.enter_secret_woods,
        },
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
    }

    def test_plando_of_randomized_entrances(self):
        for plando in [
            (EntranceName.farm_to_backwoods, RegionName.farm, RegionName.railroad),
            (EntranceName.farm_to_forest, RegionName.farm, RegionName.secret_woods),
            # reverse connections should be created as well
            (EntranceName.railroad_to_mountain, RegionName.railroad, RegionName.farm),
            (EntranceName.leave_secret_woods, RegionName.secret_woods, RegionName.farm),
        ]:
            entrance_name, begin, end = plando
            with self.subTest(f"{entrance_name} goes from {begin} to {end}"):
                entrance = self.world.get_entrance(entrance_name)
                entrance_region = self.world.get_region(begin)
                target_region = self.world.get_region(end)

                self.assertEqual(entrance.parent_region, entrance_region)
                self.assertEqual(entrance.connected_region, target_region)

    def test_plando_of_non_randomized_still_happens(self):
        farmhouse_region = self.world.get_region(RegionName.farm_house)
        beach_region = self.world.get_region(RegionName.beach)

        with self.subTest(f"Testing plandoed connection"):
            entrance = self.world.get_entrance(EntranceName.farmhouse_to_farm)
            self.assertEqual(entrance.parent_region, farmhouse_region)
            self.assertEqual(entrance.connected_region, beach_region)

        with self.subTest(f"Testing reversed connection"):
            rev_entrance = self.world.get_entrance(EntranceName.beach_to_town)
            self.assertEqual(rev_entrance.parent_region, beach_region)
            self.assertEqual(rev_entrance.connected_region, farmhouse_region)

    def test_only_plando_in_placement_info(self):
        # DOES include the reverse connections if not plandoed
        self.assertDictEqual(
            {
                EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
                EntranceName.railroad_to_mountain: EntranceName.backwoods_to_farm,
                EntranceName.farm_to_forest: EntranceName.enter_secret_woods,
                EntranceName.leave_secret_woods: EntranceName.forest_to_farm,
                EntranceName.farmhouse_to_farm: EntranceName.town_to_beach,
                EntranceName.beach_to_town: EntranceName.farm_to_farmhouse,
            },
            self.world.forced_entrances,
        )


class TestEntrancePlandoDecoupled(SVTestBase):
    options = {
        EntranceRandomization: EntranceRandomization.option_everywhere,
        EntranceRandomizationBehavior: {EntranceRandomizationBehaviorOptionName.decoupled},
        EntrancePlando: {
            EntranceName.farmhouse_to_farm: EntranceName.town_to_beach,
            EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
            EntranceName.farm_to_forest: EntranceName.enter_secret_woods,
        },
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
    }

    def test_plando_of_randomized_entrances(self):
        for plando in [
            (EntranceName.farm_to_backwoods, RegionName.farm, RegionName.railroad),
            (EntranceName.farm_to_forest, RegionName.farm, RegionName.secret_woods),
        ]:
            entrance_name, begin, end = plando
            with self.subTest(f"{entrance_name} goes from {begin} to {end}"):
                entrance = self.world.get_entrance(entrance_name)
                entrance_region = self.world.get_region(begin)
                target_region = self.world.get_region(end)

                self.assertEqual(entrance.parent_region, entrance_region)
                self.assertEqual(entrance.connected_region, target_region)

    def test_plando_of_non_randomized_still_happens(self):
        farmhouse_region = self.world.get_region(RegionName.farm_house)
        beach_region = self.world.get_region(RegionName.beach)

        with self.subTest(f"Testing plandoed connection"):
            entrance = self.world.get_entrance(EntranceName.farmhouse_to_farm)
            self.assertEqual(entrance.parent_region, farmhouse_region)
            self.assertEqual(entrance.connected_region, beach_region)

    def test_only_plando_in_placement_info(self):
        # DOES NOT include the reverse connections if not plandoed
        self.assertDictEqual(
            {
                EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
                EntranceName.farm_to_forest: EntranceName.enter_secret_woods,
                EntranceName.farmhouse_to_farm: EntranceName.town_to_beach,
            },
            self.world.forced_entrances,
        )
