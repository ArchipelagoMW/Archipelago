from . import GSTestBase
from ..gen.LocationNames import LocationName
from ..gen.ItemNames import ItemName


class TestItemRestrictions(GSTestBase):

    def test_ensure_empty_restricts(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Airs_Rock_Reveal)
        empty_item = world.create_item(ItemName.Empty)
        self.assertFalse(loc.item_rule(empty_item))

    def test_ensure_summon_restricts(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Kibombo_Frost_Jewel)
        summon = world.create_item(ItemName.Iris)
        self.assertFalse(loc.item_rule(summon))

    def test_ensure_summon_restricts_char(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Kibombo_Frost_Jewel)
        char = world.create_item(ItemName.Isaac)
        self.assertFalse(loc.item_rule(char))

    def test_ensure_mimic_restricts(self):
        world = self.get_world()
        loc = world.get_location(LocationName.Contigo_Isaac)
        mimic = world.create_item(ItemName.Mimic_0)
        self.assertFalse(loc.item_rule(mimic))
