from .. import SVContentPackTestBase
from ... import SVTestBase
from .... import options
from ....content import content_packs
from ....mods.mod_data import ModNames
from ....strings.villager_names import ModNPC, NPC


class TestVanilla(SVContentPackTestBase):

    def test_wizard_is_not_bachelor(self):
        self.assertFalse(self.content.villagers[NPC.wizard].bachelor)


class TestSVE(SVContentPackTestBase):
    mods = (ModNames.sve,)

    def test_lance_is_not_included(self):
        self.assertNotIn(ModNPC.lance, self.content.villagers)

    def test_wizard_is_bachelor(self):
        self.assertTrue(self.content.villagers[NPC.wizard].bachelor)
        self.assertEqual(self.content.villagers[NPC.wizard].mod_name, ModNames.sve)

    def test_sve_npc_are_included(self):
        self.assertIn(ModNPC.apples, self.content.villagers)
        self.assertIn(ModNPC.claire, self.content.villagers)
        self.assertIn(ModNPC.olivia, self.content.villagers)
        self.assertIn(ModNPC.sophia, self.content.villagers)
        self.assertIn(ModNPC.victor, self.content.villagers)
        self.assertIn(ModNPC.andy, self.content.villagers)
        self.assertIn(ModNPC.gunther, self.content.villagers)
        self.assertIn(ModNPC.martin, self.content.villagers)
        self.assertIn(ModNPC.marlon, self.content.villagers)
        self.assertIn(ModNPC.morgan, self.content.villagers)
        self.assertIn(ModNPC.morris, self.content.villagers)
        self.assertIn(ModNPC.scarlett, self.content.villagers)
        self.assertIn(ModNPC.susan, self.content.villagers)

        # 33 vanilla + 13 SVE
        self.assertEqual(33 + 13, len(self.content.villagers))


class TestSVEWithGingerIsland(SVContentPackTestBase):
    vanilla_packs = (content_packs.pelican_town, content_packs.ginger_island)
    mods = (ModNames.sve,)

    def test_lance_is_included(self):
        self.assertIn(ModNPC.lance, self.content.villagers)

    def test_other_sve_npc_are_included(self):
        self.assertIn(ModNPC.apples, self.content.villagers)
        self.assertIn(ModNPC.claire, self.content.villagers)
        self.assertIn(ModNPC.olivia, self.content.villagers)
        self.assertIn(ModNPC.sophia, self.content.villagers)
        self.assertIn(ModNPC.victor, self.content.villagers)
        self.assertIn(ModNPC.andy, self.content.villagers)
        self.assertIn(ModNPC.gunther, self.content.villagers)
        self.assertIn(ModNPC.martin, self.content.villagers)
        self.assertIn(ModNPC.marlon, self.content.villagers)
        self.assertIn(ModNPC.morgan, self.content.villagers)
        self.assertIn(ModNPC.morris, self.content.villagers)
        self.assertIn(ModNPC.scarlett, self.content.villagers)
        self.assertIn(ModNPC.susan, self.content.villagers)

        # 34 vanilla + 14 SVE
        self.assertEqual(34 + 14, len(self.content.villagers))


class TestSVEWithoutGingerIslandE2E(SVTestBase):
    options = {
        options.ExcludeGingerIsland: options.ExcludeGingerIsland.option_true,
        options.Mods: ModNames.sve
    }

    def test_lance_is_not_in_the_pool(self):
        for item in self.multiworld.itempool:
            self.assertFalse(("Friendsanity: " + ModNPC.lance) in item.name)

        for location in self.multiworld.get_locations(self.player):
            self.assertFalse(("Friendsanity: " + ModNPC.lance) in location.name)
