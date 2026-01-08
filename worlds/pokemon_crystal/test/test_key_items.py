from .bases import PokemonCrystalTestBase


class KeyItemsTest(PokemonCrystalTestBase):
    options = {}

    def test_ecruteak_squirtbottle(self):
        self.collect_all_but(["Squirtbottle", "Pass", "S.S. Ticket"])
        self.assertFalse(self.can_reach_region("REGION_ECRUTEAK_CITY"))
        self.collect_by_name("Squirtbottle")
        self.assertTrue(self.can_reach_region("REGION_ECRUTEAK_CITY"))

    def test_ecruteak_pass_ticket(self):
        self.collect_all_but(["Squirtbottle", "Pass", "S.S. Ticket"])
        self.assertFalse(self.can_reach_region("REGION_ECRUTEAK_CITY"))
        self.collect_by_name("Pass")
        self.assertFalse(self.can_reach_region("REGION_ECRUTEAK_CITY"))
        self.collect_by_name("S.S. Ticket")
        self.assertTrue(self.can_reach_region("REGION_ECRUTEAK_CITY"))
