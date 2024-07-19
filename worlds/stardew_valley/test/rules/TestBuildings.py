from ...options import BuildingProgression, FarmType
from ...test import SVTestBase


class TestBuildingLogic(SVTestBase):
    options = {
        FarmType.internal_name: FarmType.option_standard,
        BuildingProgression.internal_name: BuildingProgression.option_progressive,
    }

    def test_coop_blueprint(self):
        self.assertFalse(self.world.logic.region.can_reach_location("Coop Blueprint")(self.multiworld.state))

        self.collect_lots_of_money()
        self.assertTrue(self.world.logic.region.can_reach_location("Coop Blueprint")(self.multiworld.state))

    def test_big_coop_blueprint(self):
        big_coop_blueprint_rule = self.world.logic.region.can_reach_location("Big Coop Blueprint")
        self.assertFalse(big_coop_blueprint_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.collect_lots_of_money()
        self.assertFalse(big_coop_blueprint_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.create_item("Can Construct Buildings"), event=True)
        self.assertFalse(big_coop_blueprint_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.create_item("Progressive Coop"), event=False)
        self.assertTrue(big_coop_blueprint_rule(self.multiworld.state),
                        f"Rule is {repr(self.multiworld.get_location('Big Coop Blueprint', self.player).access_rule)}")

    def test_deluxe_coop_blueprint(self):
        self.assertFalse(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.collect_lots_of_money()
        self.multiworld.state.collect(self.create_item("Can Construct Buildings"), event=True)
        self.assertFalse(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.create_item("Progressive Coop"), event=True)
        self.assertFalse(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

        self.multiworld.state.collect(self.create_item("Progressive Coop"), event=True)
        self.assertTrue(self.world.logic.region.can_reach_location("Deluxe Coop Blueprint")(self.multiworld.state))

    def test_big_shed_blueprint(self):
        big_shed_rule = self.world.logic.region.can_reach_location("Big Shed Blueprint")
        self.assertFalse(big_shed_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.collect_lots_of_money()
        self.assertFalse(big_shed_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.create_item("Can Construct Buildings"), event=True)
        self.assertFalse(big_shed_rule(self.multiworld.state),
                         f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")

        self.multiworld.state.collect(self.create_item("Progressive Shed"), event=True)
        self.assertTrue(big_shed_rule(self.multiworld.state),
                        f"Rule is {repr(self.multiworld.get_location('Big Shed Blueprint', self.player).access_rule)}")
