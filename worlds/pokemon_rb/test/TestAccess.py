from . import PokemonTestBase


class ItemsAccessTest(PokemonTestBase):
    def testItemsAccessibility(self):
        item = self.get_item_by_name("Bike Voucher")
        self.assertTrue(self.multiworld.get_location("Cerulean City - Bicycle Shop", 1).can_fill(self.multiworld.state, item, True))
        item = self.get_item_by_name("Gold Teeth")
        self.assertTrue(self.multiworld.get_location("Fuchsia City - Safari Zone Warden", 1).can_fill(self.multiworld.state, item, True))
