from . import SVTestBase
from .. import options


class TestCropsanityRules(SVTestBase):
    options = {
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled
    }

    def test_need_greenhouse_for_cactus(self):
        harvest_cactus = self.world.logic.region.can_reach_location("Harvest Cactus Fruit")
        self.assert_rule_false(harvest_cactus, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Cactus Seeds"), prevent_sweep=False)
        self.multiworld.state.collect(self.world.create_item("Shipping Bin"), prevent_sweep=False)
        self.multiworld.state.collect(self.world.create_item("Desert Obelisk"), prevent_sweep=False)
        self.assert_rule_false(harvest_cactus, self.multiworld.state)

        self.multiworld.state.collect(self.world.create_item("Greenhouse"), prevent_sweep=False)
        self.assert_rule_true(harvest_cactus, self.multiworld.state)
