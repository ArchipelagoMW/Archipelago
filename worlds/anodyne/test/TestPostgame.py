from . import AnodyneTestBase
from ..Data.Regions import Windmill, Blue, Blank, Go, Hotel, Circus, Apartment


class TestDisabledPostgame(AnodyneTestBase):
    options = {
        "victory_condition": "defeat_briar",
        "custom_nexus_gates_open": [Windmill.area_name()],
        "postgame_mode": "disabled",
        "big_key_shuffle": "unlocked",
    }

    def test_requirement(self):
        self.collect_by_name("Swap")
        self.assertRaises(KeyError, lambda: self.can_reach_region(Blank.windmill))


class TestVanillaPostgame(AnodyneTestBase):
    options = {
        "victory_condition": "final_gate",
        "custom_nexus_gates_open": [Windmill.area_name(), Blue.area_name()],
        "postgame_mode": "vanilla",
        "big_key_shuffle": "unlocked",
    }

    def test_requirement(self):
        self.collect_by_name("Broom")
        self.assertFalse(self.can_reach_region(Blank.windmill))
        self.assertFalse(self.can_reach_location("Defeat Briar"))

        self.collect_by_name("Swap")
        self.assertFalse(self.can_reach_region(Blank.windmill))
        self.assertFalse(self.can_reach_location("Defeat Briar"))

        self.collect_by_name("Jump Shoes")
        self.assertTrue(self.can_reach_region(Blank.windmill))
        self.assertTrue(self.can_reach_location("Defeat Briar"))


class TestUnlockedPostgame(AnodyneTestBase):
    options = {
        "victory_condition": "final_gate",
        "custom_nexus_gates_open": [Windmill.area_name()],
        "postgame_mode": "unlocked",
        "big_key_shuffle": "unlocked",
    }

    def test_requirement(self):
        self.collect_by_name("Broom")
        self.assertFalse(self.can_reach_region(Blank.windmill))
        self.assertFalse(self.can_reach_location("Defeat Briar"))

        self.collect_by_name("Swap")
        self.assertTrue(self.can_reach_region(Blank.windmill))
        self.assertFalse(self.can_reach_location("Defeat Briar"))


class TestProgressivePostgame(AnodyneTestBase):
    options = {
        "victory_condition": "final_gate",
        "custom_nexus_gates_open": [Windmill.area_name(), Go.area_name(), Hotel.area_name(), Apartment.area_name(), Circus.area_name()],
        "postgame_mode": "progressive",
        "big_key_shuffle": "unlocked",
        "small_key_mode": "unlocked",
    }

    def test_requirement(self):
        self.collect_by_name("Broom")
        self.collect_by_name("Jump Shoes")
        self.assertFalse(self.can_reach_region(Blank.windmill))
        self.assertFalse(self.can_reach_location("Defeat Briar"))

        progressive_swap = self.get_items_by_name("Progressive Swap")

        self.collect(progressive_swap[0])
        self.assertFalse(self.can_reach_region(Blank.windmill))
        self.assertTrue(self.can_reach_location("Defeat Briar"))

        self.collect(progressive_swap[1])
        self.assertTrue(self.can_reach_region(Blank.windmill))
        self.assertTrue(self.can_reach_location("Defeat Briar"))
