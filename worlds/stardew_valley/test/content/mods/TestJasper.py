from .. import SVContentPackTestBase
from ....mods.mod_data import ModNames
from ....strings.villager_names import ModNPC


class TestJasperWithoutSVE(SVContentPackTestBase):
    mods = (ModNames.jasper,)

    def test_gunther_is_added(self):
        self.assertIn(ModNPC.gunther, self.content.villagers)
        self.assertEqual(self.content.villagers[ModNPC.gunther].mod_name, ModNames.jasper)

    def test_marlon_is_added(self):
        self.assertIn(ModNPC.marlon, self.content.villagers)
        self.assertEqual(self.content.villagers[ModNPC.marlon].mod_name, ModNames.jasper)


class TestJasperWithSVE(SVContentPackTestBase):
    mods = (ModNames.jasper, ModNames.sve)

    def test_gunther_is_added(self):
        self.assertIn(ModNPC.gunther, self.content.villagers)
        self.assertEqual(self.content.villagers[ModNPC.gunther].mod_name, ModNames.sve)

    def test_marlon_is_added(self):
        self.assertIn(ModNPC.marlon, self.content.villagers)
        self.assertEqual(self.content.villagers[ModNPC.marlon].mod_name, ModNames.sve)
