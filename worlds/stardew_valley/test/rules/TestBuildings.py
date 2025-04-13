from ...options import BuildingProgression, FarmType
from ...test import SVTestBase


class TestBuildingLogic(SVTestBase):
    options = {
        FarmType.internal_name: FarmType.option_standard,
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
    }

    def test_coop_blueprint(self):
        self.assert_cannot_reach_location("Coop Blueprint")

        self.collect_lots_of_money()
        self.assert_can_reach_location("Coop Blueprint")

    def test_big_coop_blueprint(self):
        self.assert_cannot_reach_location("Big Coop Blueprint")

        self.collect_lots_of_money()
        self.assert_cannot_reach_location("Big Coop Blueprint")

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_can_reach_location("Big Coop Blueprint")

    def test_deluxe_coop_blueprint(self):
        self.assert_cannot_reach_location("Deluxe Coop Blueprint")

        self.collect_lots_of_money()
        self.assert_cannot_reach_location("Deluxe Coop Blueprint")

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_cannot_reach_location("Deluxe Coop Blueprint")

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_can_reach_location("Deluxe Coop Blueprint")

    def test_big_shed_blueprint(self):
        self.assert_cannot_reach_location("Big Shed Blueprint")

        self.collect_lots_of_money()
        self.assert_cannot_reach_location("Big Shed Blueprint")

        self.multiworld.state.collect(self.create_item("Progressive Shed"))
        self.assert_can_reach_location("Big Shed Blueprint")
