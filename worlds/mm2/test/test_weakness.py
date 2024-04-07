from . import MM2TestBase
import typing

# Need to figure out how this test should work
# def test_wily_5(base: MM2TestBase):
#    world = base.multiworld.worlds[base.player]
#    weapon_damage = world.weapon_damage
#    boss_health = {boss: 0x1C for boss in [*list(range(8)), 12]}
#    weapon_costs = {
#        0: 0,
#        1: 10,
#        2: 2,
#        3: 0.5,
#        4: 3,
#        5: 0.125,
#        6: 4,
#        7: 0.25,
#        8: 7,
#    }
#    weapon_energy = {key: float(0x1C) for key in weapon_costs}
#    for boss in weapon_damage:


class StrictWeaknessTests(MM2TestBase):
    options = {
        "strict_weakness": True
    }

    def test_that_every_boss_has_a_weakness(self):
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(14):
            if not any(weapon_damage[weapon][boss] for weapon in range(9)):
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
            if not any(weapon_damage[weapon][boss] for weapon in range(9)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")