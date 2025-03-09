from ..bases import SVTestBase
from ...options import BuildingProgression, FarmType, ToolProgression


class TestBuildingLogic(SVTestBase):
    options = {
        FarmType.internal_name: FarmType.option_standard,
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
        ToolProgression.internal_name: ToolProgression.option_progressive,
    }

    def test_coop_blueprint(self):
        location = "Coop Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect_lots_of_money()
        self.assert_can_reach_location(location)

    def test_big_coop_blueprint(self):
        location = "Big Coop Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_can_reach_location(location)

    def test_deluxe_coop_blueprint(self):
        location = "Deluxe Coop Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_can_reach_location(location)

    def test_big_shed_blueprint(self):
        location = "Big Shed Blueprint"
        self.assert_cannot_reach_location(location)

        self.collect_lots_of_money()
        self.assert_cannot_reach_location(location)

        self.multiworld.state.collect(self.create_item("Progressive Shed"))
        self.assert_can_reach_location(location)
