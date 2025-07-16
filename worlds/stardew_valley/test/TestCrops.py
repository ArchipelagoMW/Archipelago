from .bases import SVTestBase
from .. import options
from ..strings.ap_names.transport_names import Transportation
from ..strings.building_names import Building
from ..strings.region_names import Region
from ..strings.seed_names import Seed


class TestCropsanityRules(SVTestBase):
    options = {
        options.Cropsanity.internal_name: options.Cropsanity.option_enabled
    }

    def test_need_greenhouse_for_cactus(self):
        harvest_cactus_fruit = "Harvest Cactus Fruit"
        self.assert_cannot_reach_location(harvest_cactus_fruit)

        self.multiworld.state.collect(self.create_item(Seed.cactus))
        self.multiworld.state.collect(self.create_item(Building.shipping_bin))
        self.multiworld.state.collect(self.create_item(Transportation.desert_obelisk))
        self.assert_cannot_reach_location(harvest_cactus_fruit)

        self.multiworld.state.collect(self.create_item(Region.greenhouse))
        self.assert_can_reach_location(harvest_cactus_fruit)
