from . import BlasphemousTestBase
from ..Locations import location_names


class BotSSGauntletTest(BlasphemousTestBase):
    options = {
        "starting_location": "albero",
        "wall_climb_shuffle": True,
        "dash_shuffle": True
    }

    @property
    def run_default_tests(self) -> bool:
        return False
    
    def test_botss_gauntlet(self) -> None:
        self.assertAccessDependency([location_names["CO25"]], [["Dash Ability", "Wall Climb Ability"]], True)


class BackgroundZonesTest(BlasphemousTestBase):
    @property
    def run_default_tests(self) -> bool:
        return False

    def test_dc_shroud(self) -> None:
        self.assertAccessDependency([location_names["RB03"]], [["Shroud of Dreamt Sins"]], True)

    def test_wothp_bronze_cells(self) -> None:
        bronze_locations = [
            location_names["QI70"],
            location_names["RESCUED_CHERUB_03"]
        ]

        self.assertAccessDependency(bronze_locations, [["Key of the Secular"]], True)

    def test_wothp_silver_cells(self) -> None:
        silver_locations = [
            location_names["CO24"],
            location_names["RESCUED_CHERUB_34"],
            location_names["CO37"],
            location_names["RESCUED_CHERUB_04"]
        ]

        self.assertAccessDependency(silver_locations, [["Key of the Scribe"]], True)

    def test_wothp_gold_cells(self) -> None:
        gold_locations = [
            location_names["QI51"],
            location_names["CO26"],
            location_names["CO02"]
        ]

        self.assertAccessDependency(gold_locations, [["Key of the Inquisitor"]], True)

    def test_wothp_quirce(self) -> None:
        self.assertAccessDependency([location_names["BS14"]], [["Key of the Secular", "Key of the Scribe", "Key of the Inquisitor"]], True)
