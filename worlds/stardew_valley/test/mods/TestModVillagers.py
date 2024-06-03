import unittest
from typing import Set

from ...data.villagers_data import get_villagers_for_mods
from ...mods.mod_data import ModNames
from ...strings.villager_names import NPC, ModNPC

no_mods: Set[str] = set()
sve: Set[str] = {ModNames.sve}


class TestGetVillagersForMods(unittest.TestCase):

    def test_no_mods_all_vanilla_villagers(self):
        villagers = get_villagers_for_mods(no_mods)
        villager_names = {villager.name for villager in villagers}

        self.assertIn(NPC.alex, villager_names)
        self.assertIn(NPC.elliott, villager_names)
        self.assertIn(NPC.harvey, villager_names)
        self.assertIn(NPC.sam, villager_names)
        self.assertIn(NPC.sebastian, villager_names)
        self.assertIn(NPC.shane, villager_names)
        self.assertIn(NPC.abigail, villager_names)
        self.assertIn(NPC.emily, villager_names)
        self.assertIn(NPC.haley, villager_names)
        self.assertIn(NPC.leah, villager_names)
        self.assertIn(NPC.maru, villager_names)
        self.assertIn(NPC.penny, villager_names)
        self.assertIn(NPC.caroline, villager_names)
        self.assertIn(NPC.clint, villager_names)
        self.assertIn(NPC.demetrius, villager_names)
        self.assertIn(NPC.dwarf, villager_names)
        self.assertIn(NPC.evelyn, villager_names)
        self.assertIn(NPC.george, villager_names)
        self.assertIn(NPC.gus, villager_names)
        self.assertIn(NPC.jas, villager_names)
        self.assertIn(NPC.jodi, villager_names)
        self.assertIn(NPC.kent, villager_names)
        self.assertIn(NPC.krobus, villager_names)
        self.assertIn(NPC.leo, villager_names)
        self.assertIn(NPC.lewis, villager_names)
        self.assertIn(NPC.linus, villager_names)
        self.assertIn(NPC.marnie, villager_names)
        self.assertIn(NPC.pam, villager_names)
        self.assertIn(NPC.pierre, villager_names)
        self.assertIn(NPC.robin, villager_names)
        self.assertIn(NPC.sandy, villager_names)
        self.assertIn(NPC.vincent, villager_names)
        self.assertIn(NPC.willy, villager_names)
        self.assertIn(NPC.wizard, villager_names)

    def test_no_mods_no_mod_villagers(self):
        villagers = get_villagers_for_mods(no_mods)
        villager_names = {villager.name for villager in villagers}

        self.assertNotIn(ModNPC.alec, villager_names)
        self.assertNotIn(ModNPC.ayeisha, villager_names)
        self.assertNotIn(ModNPC.delores, villager_names)
        self.assertNotIn(ModNPC.eugene, villager_names)
        self.assertNotIn(ModNPC.jasper, villager_names)
        self.assertNotIn(ModNPC.juna, villager_names)
        self.assertNotIn(ModNPC.mr_ginger, villager_names)
        self.assertNotIn(ModNPC.riley, villager_names)
        self.assertNotIn(ModNPC.shiko, villager_names)
        self.assertNotIn(ModNPC.wellwick, villager_names)
        self.assertNotIn(ModNPC.yoba, villager_names)
        self.assertNotIn(ModNPC.lance, villager_names)
        self.assertNotIn(ModNPC.apples, villager_names)
        self.assertNotIn(ModNPC.claire, villager_names)
        self.assertNotIn(ModNPC.olivia, villager_names)
        self.assertNotIn(ModNPC.sophia, villager_names)
        self.assertNotIn(ModNPC.victor, villager_names)
        self.assertNotIn(ModNPC.andy, villager_names)
        self.assertNotIn(ModNPC.gunther, villager_names)
        self.assertNotIn(ModNPC.martin, villager_names)
        self.assertNotIn(ModNPC.marlon, villager_names)
        self.assertNotIn(ModNPC.morgan, villager_names)
        self.assertNotIn(ModNPC.morris, villager_names)
        self.assertNotIn(ModNPC.scarlett, villager_names)
        self.assertNotIn(ModNPC.susan, villager_names)
        self.assertNotIn(ModNPC.goblin, villager_names)
        self.assertNotIn(ModNPC.alecto, villager_names)

    def test_sve_has_sve_villagers(self):
        villagers = get_villagers_for_mods(sve)
        villager_names = {villager.name for villager in villagers}

        self.assertIn(ModNPC.lance, villager_names)
        self.assertIn(ModNPC.apples, villager_names)
        self.assertIn(ModNPC.claire, villager_names)
        self.assertIn(ModNPC.olivia, villager_names)
        self.assertIn(ModNPC.sophia, villager_names)
        self.assertIn(ModNPC.victor, villager_names)
        self.assertIn(ModNPC.andy, villager_names)
        self.assertIn(ModNPC.gunther, villager_names)
        self.assertIn(ModNPC.martin, villager_names)
        self.assertIn(ModNPC.marlon, villager_names)
        self.assertIn(ModNPC.morgan, villager_names)
        self.assertIn(ModNPC.morris, villager_names)
        self.assertIn(ModNPC.scarlett, villager_names)
        self.assertIn(ModNPC.susan, villager_names)

    def test_sve_has_no_other_mod_villagers(self):
        villagers = get_villagers_for_mods(sve)
        villager_names = {villager.name for villager in villagers}

        self.assertNotIn(ModNPC.alec, villager_names)
        self.assertNotIn(ModNPC.ayeisha, villager_names)
        self.assertNotIn(ModNPC.delores, villager_names)
        self.assertNotIn(ModNPC.eugene, villager_names)
        self.assertNotIn(ModNPC.jasper, villager_names)
        self.assertNotIn(ModNPC.juna, villager_names)
        self.assertNotIn(ModNPC.mr_ginger, villager_names)
        self.assertNotIn(ModNPC.riley, villager_names)
        self.assertNotIn(ModNPC.shiko, villager_names)
        self.assertNotIn(ModNPC.wellwick, villager_names)
        self.assertNotIn(ModNPC.yoba, villager_names)
        self.assertNotIn(ModNPC.goblin, villager_names)
        self.assertNotIn(ModNPC.alecto, villager_names)

    def test_no_mods_wizard_is_not_bachelor(self):
        villagers = get_villagers_for_mods(no_mods)
        villagers_by_name = {villager.name: villager for villager in villagers}
        self.assertFalse(villagers_by_name[NPC.wizard].bachelor)
        self.assertEqual(villagers_by_name[NPC.wizard].mod_name, ModNames.vanilla)

    def test_sve_wizard_is_bachelor(self):
        villagers = get_villagers_for_mods(sve)
        villagers_by_name = {villager.name: villager for villager in villagers}
        self.assertTrue(villagers_by_name[NPC.wizard].bachelor)
        self.assertEqual(villagers_by_name[NPC.wizard].mod_name, ModNames.sve)
