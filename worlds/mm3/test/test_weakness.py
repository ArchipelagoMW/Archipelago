from math import ceil

from .bases import MM3TestBase
from ..rules import minimum_weakness_requirement, bosses


# Need to figure out how this test should work
def validate_wily_4(base: MM3TestBase) -> None:
    world = base.multiworld.worlds[base.player]
    weapon_damage = world.weapon_damage
    weapon_costs = {
        0: 0,
        1: 0.25,
        2: 2,
        3: 1,
        4: 2,
        5: 7,  # Not really, but we can really only rely on Top for one RBM
        6: 0.5,
        7: 2,
        8: 0.5,
    }
    boss_health = {boss: 0x1C for boss in range(8)}
    weapon_energy = {key: float(0x1C) for key in weapon_costs}
    weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage}
                   for boss in range(8)}
    flexibility = {
        boss: (
                sum(damage_value > 0 for damage_value in
                    weapon_damages.values())  # Amount of weapons that hit this boss
                * sum(weapon_damages.values())  # Overall damage that those weapons do
        )
        for boss, weapon_damages in weapon_boss.items()
    }
    boss_flexibility = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
    used_weapons: dict[int, set[int]] = {i: set() for i in range(8)}
    for boss in boss_flexibility:
        boss_damage = weapon_boss[boss]
        weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                         boss_damage.items() if weapon_energy[weapon] > 0}
        while boss_health[boss] > 0:
            if boss_damage[0] > 0:
                boss_health[boss] = 0  # if we can buster, we should buster
                continue
            highest, wp = max(zip(weapon_weight.values(), weapon_weight.keys()))
            uses = weapon_energy[wp] // weapon_costs[wp]
            used_weapons[boss].add(wp)
            if int(uses * boss_damage[wp]) > boss_health[boss]:
                used = ceil(boss_health[boss] / boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * used
                boss_health[boss] = 0
            elif highest <= 0:
                # we are out of weapons that can actually damage the boss
                base.fail(f"Ran out of weapon energy to damage "
                          f"{next(name for name in bosses if bosses[name] == boss)}\n"
                          f"Seed: {base.multiworld.seed}\n"
                          f"Damage Table: {weapon_damage}")
            else:
                # drain the weapon and continue
                boss_health[boss] -= int(uses * boss_damage[wp])
                weapon_energy[wp] -= weapon_costs[wp] * uses
                weapon_weight.pop(wp)


class WeaknessTests(MM3TestBase):
    def test_that_every_boss_has_a_weakness(self) -> None:
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(22):
            if not any(weapon_damage[weapon][boss] >= minimum_weakness_requirement[weapon] for weapon in range(9)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")

    def test_wily_4(self) -> None:
        validate_wily_4(self)


class StrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
    }


class RandomWeaknessTests(WeaknessTests):
    options = {
        "random_weakness": "randomized"
    }


class ShuffledWeaknessTests(WeaknessTests):
    options = {
        "random_weakness": "shuffled"
    }


class RandomStrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "randomized",
    }


class ShuffledStrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "shuffled"
    }
