from .. import SVContentPackTestBase
from ... import SVTestBase
from .... import options
from ....content import content_packs
from ....mods.mod_data import ModNames
from ....strings.fish_names import SVEFish
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

    def test_sve_has_sve_fish(self):
        fish_names = self.content.fishes.keys()

        self.assertIn(SVEFish.bonefish, fish_names)
        self.assertIn(SVEFish.bull_trout, fish_names)
        self.assertIn(SVEFish.butterfish, fish_names)
        self.assertIn(SVEFish.frog, fish_names)
        self.assertIn(SVEFish.goldenfish, fish_names)
        self.assertIn(SVEFish.grass_carp, fish_names)
        self.assertIn(SVEFish.king_salmon, fish_names)
        self.assertIn(SVEFish.kittyfish, fish_names)
        self.assertIn(SVEFish.meteor_carp, fish_names)
        self.assertIn(SVEFish.minnow, fish_names)
        self.assertIn(SVEFish.puppyfish, fish_names)
        self.assertIn(SVEFish.radioactive_bass, fish_names)
        self.assertIn(SVEFish.snatcher_worm, fish_names)
        self.assertIn(SVEFish.undeadfish, fish_names)
        self.assertIn(SVEFish.void_eel, fish_names)
        self.assertIn(SVEFish.water_grub, fish_names)
        self.assertIn(SVEFish.dulse_seaweed, fish_names)

        # 63 pelican town  + 17 sve pelican town
        self.assertEqual(63 + 17, len(self.content.fishes))


class TestSVEWithGingerIsland(SVContentPackTestBase):
    vanilla_packs = SVContentPackTestBase.vanilla_packs + (content_packs.ginger_island_content_pack,)
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

    def test_sve_has_sve_fish(self):
        fish_names = self.content.fishes.keys()

        self.assertIn(SVEFish.baby_lunaloo, fish_names)
        self.assertIn(SVEFish.bonefish, fish_names)
        self.assertIn(SVEFish.bull_trout, fish_names)
        self.assertIn(SVEFish.butterfish, fish_names)
        self.assertIn(SVEFish.clownfish, fish_names)
        self.assertIn(SVEFish.daggerfish, fish_names)
        self.assertIn(SVEFish.frog, fish_names)
        self.assertIn(SVEFish.gemfish, fish_names)
        self.assertIn(SVEFish.goldenfish, fish_names)
        self.assertIn(SVEFish.grass_carp, fish_names)
        self.assertIn(SVEFish.king_salmon, fish_names)
        self.assertIn(SVEFish.kittyfish, fish_names)
        self.assertIn(SVEFish.lunaloo, fish_names)
        self.assertIn(SVEFish.meteor_carp, fish_names)
        self.assertIn(SVEFish.minnow, fish_names)
        self.assertIn(SVEFish.puppyfish, fish_names)
        self.assertIn(SVEFish.radioactive_bass, fish_names)
        self.assertIn(SVEFish.seahorse, fish_names)
        self.assertIn(SVEFish.shiny_lunaloo, fish_names)
        self.assertIn(SVEFish.snatcher_worm, fish_names)
        self.assertIn(SVEFish.starfish, fish_names)
        self.assertIn(SVEFish.torpedo_trout, fish_names)
        self.assertIn(SVEFish.undeadfish, fish_names)
        self.assertIn(SVEFish.void_eel, fish_names)
        self.assertIn(SVEFish.water_grub, fish_names)
        self.assertIn(SVEFish.sea_sponge, fish_names)
        self.assertIn(SVEFish.dulse_seaweed, fish_names)

        # 63 pelican town + 3 ginger island + 17 sve pelican town + 10 sve ginger island
        self.assertEqual(63 + 3 + 17 + 10, len(self.content.fishes))


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
