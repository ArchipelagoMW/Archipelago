from . import MM2TestBase


class StrictWeaknessTests(MM2TestBase):
    options = {
        "strict_weakness": True
    }

    def test_that_every_boss_has_a_weakness(self):
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(14):
            if not any(weapon_damage[weapon][boss] for weapon in range(8)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")


class RandomStrictWeaknessTests(MM2TestBase):
    options = {
        "strict_weakness": True,
        "random_weakness": True
    }

    def test_that_every_boss_has_a_weakness(self):
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(14):
            if not any(weapon_damage[weapon][boss] for weapon in range(8)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")