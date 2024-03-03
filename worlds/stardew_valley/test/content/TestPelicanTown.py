from . import SVContentPackTestBase
from ...strings.villager_names import NPC


class TestPelicanTown(SVContentPackTestBase):

    def test_all_pelican_town_villagers_are_included(self):
        self.assertIn(NPC.alex, self.content.villagers)
        self.assertIn(NPC.elliott, self.content.villagers)
        self.assertIn(NPC.harvey, self.content.villagers)
        self.assertIn(NPC.sam, self.content.villagers)
        self.assertIn(NPC.sebastian, self.content.villagers)
        self.assertIn(NPC.shane, self.content.villagers)
        self.assertIn(NPC.abigail, self.content.villagers)
        self.assertIn(NPC.emily, self.content.villagers)
        self.assertIn(NPC.haley, self.content.villagers)
        self.assertIn(NPC.leah, self.content.villagers)
        self.assertIn(NPC.maru, self.content.villagers)
        self.assertIn(NPC.penny, self.content.villagers)
        self.assertIn(NPC.caroline, self.content.villagers)
        self.assertIn(NPC.clint, self.content.villagers)
        self.assertIn(NPC.demetrius, self.content.villagers)
        self.assertIn(NPC.dwarf, self.content.villagers)
        self.assertIn(NPC.evelyn, self.content.villagers)
        self.assertIn(NPC.george, self.content.villagers)
        self.assertIn(NPC.gus, self.content.villagers)
        self.assertIn(NPC.jas, self.content.villagers)
        self.assertIn(NPC.jodi, self.content.villagers)
        self.assertIn(NPC.kent, self.content.villagers)
        self.assertIn(NPC.krobus, self.content.villagers)
        self.assertIn(NPC.lewis, self.content.villagers)
        self.assertIn(NPC.linus, self.content.villagers)
        self.assertIn(NPC.marnie, self.content.villagers)
        self.assertIn(NPC.pam, self.content.villagers)
        self.assertIn(NPC.pierre, self.content.villagers)
        self.assertIn(NPC.robin, self.content.villagers)
        self.assertIn(NPC.sandy, self.content.villagers)
        self.assertIn(NPC.vincent, self.content.villagers)
        self.assertIn(NPC.willy, self.content.villagers)
        self.assertIn(NPC.wizard, self.content.villagers)

        self.assertEqual(33, len(self.content.villagers))
