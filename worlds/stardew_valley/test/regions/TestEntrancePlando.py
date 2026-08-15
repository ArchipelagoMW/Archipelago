import unittest

from Options import PlandoConnection

from ... import options
from ...strings.ap_names.ap_option_names import EntranceRandomizationBehaviorOptionName
from ...strings.entrance_names import Entrance as EntranceName
from ...strings.region_names import Region as RegionName
from ..bases import SVTestBase


class TestEntrancePlandoCoupled(SVTestBase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: {},
        options.EntrancePlando: [
            # sewer to beach
            PlandoConnection(EntranceName.sewer_to_forest, EntranceName.town_to_beach, "both", 100),
            # farm to railroad
            PlandoConnection(EntranceName.farm_to_backwoods, EntranceName.mountain_to_railroad, "both", 100),
            # farm to secret woods
            PlandoConnection(EntranceName.farm_to_forest, EntranceName.enter_secret_woods, "both", 100),
        ],
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
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

    def test_only_plando_in_placement_info(self):
        # DOES include the reverse connections if not plandoed
        self.assertDictEqual(
            {
                EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
                EntranceName.railroad_to_mountain: EntranceName.backwoods_to_farm,
                EntranceName.farm_to_forest: EntranceName.enter_secret_woods,
                EntranceName.leave_secret_woods: EntranceName.forest_to_farm,
                EntranceName.sewer_to_forest: EntranceName.town_to_beach,
                EntranceName.beach_to_town: EntranceName.forest_to_sewer,
            },
            self.world.forced_entrances,
        )

@unittest.skip
class TestEntrancePlandoFarmhouse(SVTestBase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: {},
        options.EntrancePlando: [
            # farmhouse to beach
            PlandoConnection(EntranceName.farmhouse_to_farm, EntranceName.town_to_beach, "both", 100),
        ],
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
    }

    def test_plando_of_randomized_entrances(self): ...

class TestEntrancePlandoDecoupled(SVTestBase):
    options = {  # noqa: RUF012
        options.EntranceRandomization: options.EntranceRandomization.option_everywhere,
        options.EntranceRandomizationBehavior: {EntranceRandomizationBehaviorOptionName.decoupled},
        options.EntrancePlando: [
            # sewer to beach
            PlandoConnection(EntranceName.sewer_to_forest, EntranceName.town_to_beach, "entrance", 100),
            # farm to railroad
            PlandoConnection(EntranceName.farm_to_backwoods, EntranceName.mountain_to_railroad, "entrance", 100),
            # farm to secret woods
            PlandoConnection(EntranceName.farm_to_forest, EntranceName.enter_secret_woods, "entrance", 100),
        ],
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_false,
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

    def test_only_plando_in_placement_info(self):
        # DOES NOT include the reverse connections if not plandoed
        self.assertDictEqual(
            {
                EntranceName.farm_to_backwoods: EntranceName.mountain_to_railroad,
                EntranceName.farm_to_forest: EntranceName.enter_secret_woods,
                EntranceName.sewer_to_forest: EntranceName.town_to_beach,
            },
            self.world.forced_entrances,
        )
