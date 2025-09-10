from ..bases import SVTestBase
from ... import StartWithoutOptionName
from ...locations import location_table, LocationTags
from ...options import StartWithout


class TestTravelingMerchant(SVTestBase):
    options = {
        StartWithout: frozenset({StartWithoutOptionName.buildings}),
    }

    def test_purchase_from_traveling_merchant_requires_money(self):
        traveling_merchant_location_names = [l for l in self.get_real_location_names() if LocationTags.TRAVELING_MERCHANT in location_table[l].tags]

        for traveling_merchant_day in ["Traveling Merchant: Sunday", "Traveling Merchant: Monday", "Traveling Merchant: Tuesday",
                                       "Traveling Merchant: Wednesday", "Traveling Merchant: Thursday", "Traveling Merchant: Friday",
                                       "Traveling Merchant: Saturday"]:
            self.collect(traveling_merchant_day)

        for location_name in traveling_merchant_location_names:
            location = self.multiworld.get_location(location_name, 1)
            self.assert_cannot_reach_location(location, self.multiworld.state)

        self.collect("Shipping Bin")

        for location_name in traveling_merchant_location_names:
            location = self.multiworld.get_location(location_name, 1)
            self.assert_can_reach_location(location, self.multiworld.state)
