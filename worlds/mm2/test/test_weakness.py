from math import ceil

from . import MM2TestBase
from ..Options import bosses


# Need to figure out how this test should work
def validate_wily_5(base: MM2TestBase) -> None:
    world = base.multiworld.worlds[base.player]
    weapon_damage = world.weapon_damage
    boss_health = {boss: 0x1C for boss in [*list(range(8)), 12]}
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
    weapon_energy = {key: float(0x1C * 2) if key == 12 else float(0x1C) for key in weapon_costs}
    weapon_boss = {boss: {weapon: weapon_damage[weapon][boss] for weapon in weapon_damage}
                   for boss in [*list(range(8)), 12]}
    flexibility = [(sum(1 if weapon_boss[boss][weapon] > 0 else 0 for weapon in range(9)) *
                    sum(weapon_boss[boss].values()), boss) for boss in weapon_boss if boss != 12]
    for _, boss in [*sorted(flexibility), (0, 12)]:
        boss_damage = weapon_boss[boss]
        weapon_weight = {weapon: (weapon_energy[weapon] / damage) if damage else 0 for weapon, damage in
                         boss_damage.items() if weapon_energy[weapon]}
        while boss_health[boss] > 0:
            if boss_damage[0]:
                boss_health[boss] = 0  # if we can buster, we should buster
                continue
            highest, wp = max(zip(weapon_weight.values(), weapon_weight.keys()))
            uses = weapon_energy[wp] // weapon_costs[wp]
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


class StrictWeaknessTests(MM2TestBase):
    options = {
        "strict_weakness": True,
        "yoku_jumps": True,
        "enable_lasers": True
    }

    def test_that_every_boss_has_a_weakness(self) -> None:
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(14):
            if not any(weapon_damage[weapon][boss] for weapon in range(9)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")

    def test_wily_5(self) -> None:
        validate_wily_5(self)


class RandomStrictWeaknessTests(MM2TestBase):
    options = {
        "strict_weakness": True,
        "random_weakness": "randomized",
        "yoku_jumps": True,
        "enable_lasers": True
    }

    def test_that_every_boss_has_a_weakness(self) -> None:
        world = self.multiworld.worlds[self.player]
        weapon_damage = world.weapon_damage
        for boss in range(14):
            if not any(weapon_damage[weapon][boss] for weapon in range(9)):
                self.fail(f"Boss {boss} generated without weakness! Seed: {self.multiworld.seed}")

    def test_wily_5(self) -> None:
        validate_wily_5(self)
