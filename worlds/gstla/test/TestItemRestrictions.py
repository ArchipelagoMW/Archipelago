from . import GSTestBase
from ..gen.LocationData import LocationRestriction
from ..gen.LocationNames import LocationName
from ..gen.ItemNames import ItemName


class TestItemRestrictions(GSTestBase):
    options = {
        "item_shuffle": 3
    }

    def test_ensure_empty_restricts(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Airs_Rock_Reveal)
        empty_item = world.create_item(ItemName.Empty)
        self.assertFalse(loc.can_fill(self.multiworld.state, empty_item, False))

    def test_ensure_summon_restricts(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Kibombo_Frost_Jewel)
        summon = world.create_item(ItemName.Iris)
        self.assertFalse(loc.can_fill(self.multiworld.state, summon, False))

    def test_ensure_summon_restricts_char(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Kibombo_Frost_Jewel)
        char = world.create_item(ItemName.Isaac)
        self.assertFalse(loc.can_fill(self.multiworld.state, char, False))

    def test_ensure_mimic_restricts(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Contigo_Isaac)
        mimic = world.create_item(ItemName.Milquetoast_Mimic)
        self.assertFalse(loc.can_fill(self.multiworld.state, mimic, False))

    def test_ensure_event_type_restricts(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Daila_Psy_Crystal)
        mimic = world.create_item(ItemName.Journeyman_Mimic)
        self.assertFalse(loc.can_fill(self.multiworld.state, mimic, False))

    def test_ensure_specific_restriction_low(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Idejima_Growth)
        mimic = world.create_item(ItemName.Journeyman_Mimic)
        self.assertFalse(loc.can_fill(self.multiworld.state, mimic, False))
        coin = world.create_item(ItemName.Coins_82)
        self.assertFalse(loc.can_fill(self.multiworld.state, coin, False))

    def test_ensure_specific_restriction_high(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Kibombo_Douse_Drop)
        mimic = world.create_item(ItemName.Journeyman_Mimic)
        self.assertFalse(loc.can_fill(self.multiworld.state, mimic, False))
        coin = world.create_item(ItemName.Coins_82)
        self.assertFalse(loc.can_fill(self.multiworld.state, coin, False))

    def test_restrict_money_by_addr(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Gaia_Rock_Sand)
        coin = world.create_item(ItemName.Coins_82)
        self.assertFalse(loc.can_fill(self.multiworld.state, coin, False))

    def test_ensure_not_everything_restricted(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Airs_Rock_Sleep_Bomb)
        self.assertTrue(loc.location_data.restrictions == LocationRestriction.NONE)
