from math import ceil

from . import MM2TestBase
from ..options import bosses
from ..rules import minimum_weakness_requirement


def validate_wily_5(base: MM2TestBase) -> None:
    world = base.multiworld.worlds[base.player]
    weapon_damage = world.weapon_damage
    weapon_costs = {
        0: 0,
        1: 10,
        2: 2,
        3: 3,
        4: 0.5,
        5: 0.125,
        6: 4,
        7: 0.25,
        8: 7,
    }
    boss_health = {boss: 0x1C if boss != 12 else 0x1C * 2 for boss in [*range(8), 12]}
    weapon_energy = {key: float(0x1C) for key in weapon_costs}
    weapon_boss = {boss: {weapon: world.weapon_damage[weapon][boss] for weapon in world.weapon_damage}
                   for boss in [*range(8), 12]}
    flexibility = {
        boss: (
                sum(damage_value > 0 for damage_value in
                    weapon_damages.values())  # Amount of weapons that hit this boss
                * sum(weapon_damages.values())  # Overall damage that those weapons do
        )
        for boss, weapon_damages in weapon_boss.items() if boss != 12
    }
    flexibility = sorted(flexibility, key=flexibility.get)  # Fast way to sort dict by value
    used_weapons = {i: set() for i in [*range(8), 12]}
    for boss in [*flexibility, 12]:
        boss_damage = weapon_boss[boss]
        weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                         boss_damage.items() if weapon_energy[weapon] > 0}
        if boss_damage[8]:
            boss_damage[8] = 1.75 * boss_damage[8]
        if any(boss_damage[i] > 0 for i in range(8)) and 8 in weapon_weight:
            # We get exactly one use of Time Stopper during the rush
            # So we want to make sure that use is absolutely needed
            weapon_weight[8] = min(weapon_weight[8], 0.001)
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


class WeaknessTests(MM2TestBase):
    options = {
        "yoku_jumps": True,
        "enable_lasers": True,
    }
    def test_that_every_boss_has_a_weakness(self) -> None:
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(14):
            if not any(weapon_damage[weapon][boss] >= minimum_weakness_requirement[weapon] for weapon in range(9)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")

    def test_wily_5(self) -> None:
        validate_wily_5(self)


class StrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        **WeaknessTests.options
    }


class RandomWeaknessTests(WeaknessTests):
    options = {
        "random_weakness": "randomized",
        **WeaknessTests.options
    }


class ShuffledWeaknessTests(WeaknessTests):
    options = {
        "random_weakness": "shuffled",
        **WeaknessTests.options
    }


class RandomStrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "randomized",
        **WeaknessTests.options
    }


class ShuffledStrictWeaknessTests(WeaknessTests):
    options = {
        "strict_weakness": True,
        "random_weakness": "shuffled",
        **WeaknessTests.options
    }
