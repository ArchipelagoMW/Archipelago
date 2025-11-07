from ..Names import locationName, regionName
from ..Options import JamjarsSiloCosts, RandomizeBTMoveList, RandomizeWorldLoadingZones, RandomizeWorldOrder
from . import BanjoTooieTestBase


class VanillaSiloCostTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "jamjars_silo_costs": JamjarsSiloCosts.option_vanilla
    }

    def test_vanilla_costs(self) -> None:
        expected_silo_costs = {
            locationName.FEGGS: 45,
            locationName.GEGGS: 110,
            locationName.IEGGS: 200,
            locationName.CEGGS: 315,
            locationName.EGGAIM: 25,
            locationName.BBLASTER: 30,
            locationName.GGRAB: 35,
            locationName.BDRILL: 85,
            locationName.BBAYONET: 95,
            locationName.SPLITUP: 160,
            locationName.PACKWH: 170,
            locationName.AIREAIM: 180,
            locationName.WWHACK: 265,
            locationName.AUQAIM: 275,
            locationName.TTORP: 290,
            locationName.SPRINGB: 390,
            locationName.TAXPACK: 405,
            locationName.HATCH: 420,
            locationName.CLAWBTS: 505,
            locationName.SNPACK: 525,
            locationName.LSPRING: 545,
            locationName.SHPACK: 640,
            locationName.GLIDE: 660,
            locationName.SAPACK: 765,
        }
        assert self.world.jamjars_siloname_costs == expected_silo_costs


class ProgressiveSiloCostTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "jamjars_silo_costs": JamjarsSiloCosts.option_progressive
    }

    def test_contains_vanilla_silo_costs(self) -> None:
        vanilla_costs = [45, 110, 200, 315, 25, 30, 35, 85, 95, 160, 170,
                         180, 265, 275, 290, 390, 405, 420, 505, 525, 545, 640, 660, 765]
        for cost in vanilla_costs:
            assert cost in self.world.jamjars_siloname_costs.values()

    def test_silos_in_level_order(self) -> None:
        world_silo = {
            regionName.MT: locationName.EGGAIM,
            regionName.GM: locationName.BDRILL,
            regionName.WW: locationName.SPLITUP,
            regionName.JR: locationName.WWHACK,
            regionName.TL: locationName.SPRINGB,
            regionName.GIO: locationName.CLAWBTS,
            regionName.HP: locationName.SHPACK,
            regionName.CC: locationName.SAPACK,
            regionName.CK: None,
        }
        previous_silo_cost = 0

        for world_entrance in self.world.world_order:

            next_silo = world_silo[self.world.loading_zones[world_entrance]]
            if next_silo is None:
                continue
            silo_cost = self.world.jamjars_siloname_costs[next_silo]

            assert silo_cost > previous_silo_cost

            previous_silo_cost = silo_cost

# If worlds are not randomized, it is expected that progressive works the same as vanilla costs.


class ProgressiveSiloCostVanillaLevelOrderTest(ProgressiveSiloCostTest, VanillaSiloCostTest):
    options = {
        **ProgressiveSiloCostTest.options,
        "randomize_worlds": RandomizeWorldOrder.option_false,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_false
    }


class ProgressiveSiloCostRandomLevelOrderTest(ProgressiveSiloCostTest):
    options = {
        **ProgressiveSiloCostTest.options,
        "randomize_worlds": RandomizeWorldOrder.option_true,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_false
    }


class ProgressiveSiloCostRandomLevelLoadingZoneTest(ProgressiveSiloCostTest):
    options = {
        **ProgressiveSiloCostTest.options,
        "randomize_worlds": RandomizeWorldOrder.option_false,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_true
    }


class ProgressiveSiloCostRandomLevelOrderAndLoadingZoneTest(ProgressiveSiloCostTest):
    options = {
        **ProgressiveSiloCostTest.options,
        "randomize_worlds": RandomizeWorldOrder.option_true,
        "randomize_world_entrance_loading_zones": RandomizeWorldLoadingZones.option_true
    }


class RandomSiloCostTest(BanjoTooieTestBase):
    options = {
        "randomize_bt_moves": RandomizeBTMoveList.option_true,
        "jamjars_silo_costs": JamjarsSiloCosts.option_randomize
    }

    def test_multiples_of_5(self) -> None:
        for cost in self.world.jamjars_siloname_costs.values():
            assert cost / 5.0 == cost / 5

    def test_bounded(self) -> None:
        for cost in self.world.jamjars_siloname_costs.values():
            assert 0 <= cost
            assert 800 >= cost
