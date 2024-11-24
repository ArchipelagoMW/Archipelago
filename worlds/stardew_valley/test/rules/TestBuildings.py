from ...options import BuildingProgression, FarmType
from ...test import SVTestBase


class TestBuildingLogic(SVTestBase):
    options = {
        FarmType.internal_name: FarmType.option_standard,
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
    }

    def test_coop_blueprint(self):
        coop_blueprint_rule = self.get_can_reach_location_rule("Coop Blueprint")
        self.assert_rule_false(coop_blueprint_rule, self.multiworld.state)

        self.collect_lots_of_money()
        self.assert_rule_true(coop_blueprint_rule, self.multiworld.state)

    def test_big_coop_blueprint(self):
        big_coop_blueprint_rule = self.get_can_reach_location_rule("Big Coop Blueprint")
        self.assert_rule_false(big_coop_blueprint_rule, self.multiworld.state)

        self.collect_lots_of_money()
        self.assert_rule_false(big_coop_blueprint_rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_rule_true(big_coop_blueprint_rule, self.multiworld.state)

    def test_deluxe_coop_blueprint(self):
        deluxe_coop_blueprint_rule = self.get_can_reach_location_rule("Deluxe Coop Blueprint")
        self.assert_rule_false(deluxe_coop_blueprint_rule, self.multiworld.state)

        self.collect_lots_of_money()
        self.assert_rule_false(deluxe_coop_blueprint_rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_rule_false(deluxe_coop_blueprint_rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Progressive Coop"))
        self.assert_rule_true(deluxe_coop_blueprint_rule, self.multiworld.state)

    def test_big_shed_blueprint(self):
        big_shed_rule = self.get_can_reach_location_rule("Big Shed Blueprint")
        self.assert_rule_false(big_shed_rule, self.multiworld.state)

        self.collect_lots_of_money()
        self.assert_rule_false(big_shed_rule, self.multiworld.state)

        self.multiworld.state.collect(self.create_item("Progressive Shed"))
        self.assert_rule_true(big_shed_rule, self.multiworld.state)
