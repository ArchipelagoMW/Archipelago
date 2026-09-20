from dataclasses import dataclass
from math import ceil
from typing import TYPE_CHECKING, Sequence
from typing_extensions import override
from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from . import names
from .locations import get_boss_locations, mm3_regions
from rule_builder.rules import CanReachLocation, HasAll, HasAny, Has, OptionFilter, Rule, True_, TWorld

if TYPE_CHECKING:
    from . import MM3World
    from BaseClasses import CollectionState

bosses: dict[str, int] = {
    "Needle Man": 0,
    "Magnet Man": 1,
    "Gemini Man": 2,
    "Hard Man": 3,
    "Top Man": 4,
    "Snake Man": 5,
    "Spark Man": 6,
    "Shadow Man": 7,
    "Doc Robot (Metal)": 8,
    "Doc Robot (Quick)": 9,
    "Doc Robot (Air)": 10,
    "Doc Robot (Crash)": 11,
    "Doc Robot (Flash)": 12,
    "Doc Robot (Bubble)": 13,
    "Doc Robot (Wood)": 14,
    "Doc Robot (Heat)": 15,
    "Break Man": 16,
    "Kamegoro Maker": 17,
    "Yellow Devil MK-II": 18,
    "Holograph Mega Man": 19,
    "Wily Machine 3": 20,
    "Gamma": 21
}

weapons_to_id: dict[str, int] = {
    "Mega Buster": 0,
    "Needle Cannon": 1,
    "Magnet Missile": 2,
    "Gemini Laser": 3,
    "Hard Knuckle": 4,
    "Top Spin": 5,
    "Search Snake": 6,
    "Spark Shot": 7,
    "Shadow Blade": 8,
}

weapon_damage: dict[int, list[int]] = {
    0: [1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 3, 1, 1, 1, 0, ],  # Mega Buster
    1: [4, 1, 1, 0, 2, 4, 2, 1, 0, 1, 1, 2, 4, 2, 4, 2, 0, 3, 1, 1, 1, 0, ],  # Needle Cannon
    2: [1, 4, 2, 4, 1, 0, 0, 1, 4, 2, 4, 1, 1, 0, 0, 1, 0, 3, 1, 0, 1, 0, ],  # Magnet Missile
    3: [7, 2, 4, 1, 0, 1, 1, 1, 1, 4, 2, 0, 4, 1, 1, 1, 0, 3, 1, 1, 1, 0, ],  # Gemini Laser
    4: [0, 2, 2, 4, 7, 2, 2, 2, 4, 1, 2, 7, 0, 2, 2, 2, 0, 1, 5, 4, 7, 4, ],  # Hard Knuckle
    5: [1, 1, 2, 0, 4, 2, 1, 7, 0, 1, 1, 4, 1, 1, 2, 7, 0, 1, 0, 7, 0, 2, ],  # Top Spin
    6: [1, 1, 5, 0, 1, 4, 0, 1, 0, 4, 1, 1, 1, 0, 4, 1, 0, 1, 0, 7, 4, 2, ],  # Search Snake
    7: [0, 7, 1, 0, 1, 1, 4, 1, 2, 1, 4, 1, 0, 4, 1, 1, 0, 0, 0, 0, 7, 0, ],  # Spark Shot
    8: [2, 7, 2, 0, 1, 2, 4, 4, 2, 2, 0, 1, 2, 4, 2, 4, 0, 1, 3, 2, 2, 2, ],  # Shadow Blade
}

weapons_to_name: dict[int, str] = {
    1: names.needle_cannon,
    2: names.magnet_missile,
    3: names.gemini_laser,
    4: names.hard_knuckle,
    5: names.top_spin,
    6: names.search_snake,
    7: names.spark_shock,
    8: names.shadow_blade
}

minimum_weakness_requirement: dict[int, int] = {
    0: 1,  # Mega Buster is free
    1: 1,  # 112 shots of Needle Cannon
    2: 2,  # 14 shots of Magnet Missile
    3: 2,  # 14 shots of Gemini Laser
    4: 2,  # 14 uses of Hard Knuckle
    5: 4,  # an unknown amount of Top Spin (4 means you should be able to be fine)
    6: 1,  # 56 uses of Search Snake
    7: 2,  # 14 functional uses of Spark Shot (fires in twos)
    8: 1,  # 56 uses of Shadow Blade
}

robot_masters: dict[int, str] = {
    0: "Needle Man Defeated",
    1: "Magnet Man Defeated",
    2: "Gemini Man Defeated",
    3: "Hard Man Defeated",
    4: "Top Man Defeated",
    5: "Snake Man Defeated",
    6: "Spark Man Defeated",
    7: "Shadow Man Defeated"
}

weapon_costs = {
    0: 0,
    1: 0.25,
    2: 2,
    3: 2,
    4: 2,
    5: 7,  # Not really, but we can really only rely on Top for one RBM
    6: 0.5,
    7: 2,
    8: 0.5,
}


@dataclass
class CanDefeatEnoughRBMs(Rule["MM3World"], game="Mega Man 3"):
    @override
    def _instantiate(self, world: "MM3World") -> Rule.Resolved:
        return self.Resolved(tuple([(key, tuple(map(lambda x: weapons_to_name[x], val))) for key, val in
                                    sorted(world.wily_4_weapons.items())]), world.options.wily_4_requirement.value,
                             player=world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        boss_requirements: tuple[tuple[int, tuple[str, ...]], ...]
        required: int

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                x: {id(self)} for boss, weapons in self.boss_requirements for x in weapons
            }

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            explain_strs = self.explain_str(state).splitlines()
            messages: list[JSONMessagePart] = [{"type": "text", "text": explain_strs[0]}]
            for rbm in explain_strs[1:]:
                color = "salmon" if "Cannot" in rbm else "green"
                messages.append({"type": "color", "text": rbm, "color": color})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            explain_str = f"Required RBMs: {self.required}"
            for boss, reqs in self.boss_requirements:
                if boss in robot_masters:
                    if state:
                        verb = "Can Defeat" if state.has_all(reqs, self.player) \
                            else "Cannot Defeat"
                    else:
                        verb = ", ".join(reqs)
                    explain_str += f"\n{robot_masters[boss][:-9]}: {verb}"
            return explain_str

        @override
        def _evaluate(self, state: "CollectionState") -> bool:
            can_defeat = 0
            for boss, reqs in self.boss_requirements:
                if boss in robot_masters:
                    if state.has_all(reqs, self.player):
                        can_defeat += 1
                        if can_defeat >= self.required:
                            return True
            return False


HasRushVertical = HasAny(names.rush_jet, names.rush_coil)
CanTraverseLongWater = HasAny(names.rush_jet, names.rush_marine)
HasAnyRush = HasAny(names.rush_jet, names.rush_coil, names.rush_marine)
HasRushJet = Has(names.rush_jet)
HasHardKnuckle = Has(names.hard_knuckle)


STATIC_LOCATION_RULES: dict[str, Rule] = {
    names.gemini_man: HasAnyRush,
    names.get_gemini_laser: HasAnyRush,
    names.hard_man: HasRushVertical,
    names.get_hard_knuckle: HasRushVertical,
    names.wily_1_boss: HasRushVertical,
    names.wily_stage_1: HasRushVertical,
    names.wily_2_boss: HasRushJet,
    names.wily_stage_2: HasRushJet,
    # Wily 3 technically needs vertical
    # However, Wily 3 requires beating Wily 2, and Wily 2 explicitly needs Jet
    # So we can skip the additional rule on Wily 3
}

STATIC_ENTRANCE_RULES: dict[str, Rule] = {
    "To Doc Robot (Needle) - Air": HasRushVertical,
    "To Doc Robot (Needle) - Crash": CanReachLocation(names.doc_air, "Doc Robot (Needle) - Air") & HasRushJet,
    "To Doc Robot (Gemini) - Bubble": CanReachLocation(names.doc_flash, "Doc Robot (Gemini) - Flash") & CanTraverseLongWater & HasRushVertical,
    "To Doc Robot (Shadow) - Heat": CanReachLocation(names.doc_wood, "Doc Robot (Shadow) - Wood"),
    "To Doc Robot (Spark) - Metal": HasRushVertical & HasAny(names.shadow_blade, names.gemini_laser),
    "To Doc Robot (Spark) - Quick": CanReachLocation(names.doc_metal, "Doc Robot (Spark) - Metal"),

}

STATIC_1UP_RULES: dict[str, Rule] = {
    names.needle_man_c2: HasRushJet,
    names.gemini_man_c1: HasRushJet,
    names.gemini_man_c3: HasRushVertical & HasAny(names.gemini_laser, names.shadow_blade),
    names.gemini_man_c6: HasAnyRush,
    names.gemini_man_c7: HasAnyRush,
    names.gemini_man_c10: HasAnyRush,
    names.hard_man_c3: HasRushVertical,
    names.top_man_c6: HasRushVertical,
    names.doc_needle_c2: HasRushJet,
    names.doc_needle_c3: HasRushJet,
    names.doc_gemini_c1: HasRushVertical,
    names.doc_gemini_c2: HasRushVertical,
    names.wily_1_c4: HasHardKnuckle,
    names.wily_1_c8: HasRushVertical & HasHardKnuckle,
    names.wily_2_c9: HasRushJet,
    names.wily_2_c11: HasRushJet,
}

STATIC_ENERGY_RULES: dict[str, Rule] = {
    names.gemini_man_c2: HasRushVertical,
    names.gemini_man_c4: HasRushVertical,
    names.gemini_man_c5: HasRushVertical,
    names.gemini_man_c8: HasAnyRush,
    names.gemini_man_c9: HasAnyRush,
    names.hard_man_c2: HasRushVertical,
    names.hard_man_c4: HasRushVertical,
    names.hard_man_c5: HasRushVertical,
    names.hard_man_c6: HasRushVertical,
    names.hard_man_c7: HasRushVertical,
    names.top_man_c2: HasRushVertical,
    names.top_man_c3: HasRushVertical,
    names.top_man_c4: HasRushVertical,
    names.top_man_c7: HasRushVertical,
    names.spark_man_c1: HasRushVertical,
    names.spark_man_c2: HasRushVertical,
    names.wily_1_c5: HasHardKnuckle,
    names.wily_1_c6: HasRushVertical & HasHardKnuckle,
    names.wily_1_c7: HasRushVertical & HasHardKnuckle,
    names.wily_1_c11: HasRushVertical,
    names.wily_1_c12: HasRushVertical,
    names.wily_2_c5: HasRushJet,
    names.wily_2_c6: HasRushJet,
    names.wily_2_c7: HasRushJet,
    names.wily_2_c8: HasRushJet,
    names.wily_2_c10: HasRushJet,
    names.wily_2_c12: HasRushJet,
    names.wily_2_c13: HasRushJet,
    names.wily_3_c1: HasHardKnuckle,
    names.wily_3_c2: HasHardKnuckle,
}


def set_rules(world: "MM3World") -> None:
    # most rules are set on region, so we only worry about rules required within stage access
    # or rules variable on settings
    if hasattr(world.multiworld, "re_gen_passthrough"):
        slot_data = getattr(world.multiworld, "re_gen_passthrough")["Mega Man 3"]
        world.weapon_damage = slot_data["weapon_damage"]
    else:
        if world.options.random_weakness == world.options.random_weakness.option_shuffled:
            weapon_tables = [table.copy() for weapon, table in weapon_damage.items() if weapon != 0]
            world.random.shuffle(weapon_tables)
            for i in range(1, 9):
                world.weapon_damage[i] = weapon_tables.pop()
        elif world.options.random_weakness == world.options.random_weakness.option_randomized:
            world.weapon_damage = {i: [] for i in range(9)}
            for boss in range(22):
                for weapon in world.weapon_damage:
                    world.weapon_damage[weapon].append(min(14, max(0, int(world.random.normalvariate(3, 3)))))
                if not any([world.weapon_damage[weapon][boss] >= 4
                            for weapon in range(1, 9)]):
                    # failsafe, there should be at least one defined non-Buster weakness
                    weapon = world.random.randint(1, 7)
                    world.weapon_damage[weapon][boss] = world.random.randint(4, 14)  # Force weakness
            # handle Break Man
            boss = 16
            for weapon in world.weapon_damage:
                world.weapon_damage[weapon][boss] = 0
            weapon = world.random.choice(list(world.weapon_damage.keys()))
            world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

        if world.options.strict_weakness:
            for weapon in weapon_damage:
                for i in range(22):
                    if i == 16:
                        continue  # Break is only weak to buster on non-random, and minimal damage on random
                    elif weapon == 0:
                        world.weapon_damage[weapon][i] = 0
                    elif i in (20, 21) and not world.options.random_weakness:
                        continue
                        # Gamma and Wily Machine need all weaknesses present, so allow
                    elif not world.options.random_weakness == world.options.random_weakness.option_randomized \
                            and i == 17:
                        if 3 > world.weapon_damage[weapon][i] > 0:
                            # Kamegoros take 3 max from weapons on non-random
                            world.weapon_damage[weapon][i] = 0
                    elif 4 > world.weapon_damage[weapon][i] > 0:
                        world.weapon_damage[weapon][i] = 0

        for p_boss in world.options.plando_weakness:
            for p_weapon in world.options.plando_weakness[p_boss]:
                if not any(w for w in world.weapon_damage
                           if w != weapons_to_id[p_weapon]
                           and world.weapon_damage[w][bosses[p_boss]] > minimum_weakness_requirement[w]):
                    # we need to replace this weakness
                    weakness = world.random.choice([key for key in world.weapon_damage
                                                    if key != weapons_to_id[p_weapon]])
                    world.weapon_damage[weakness][bosses[p_boss]] = minimum_weakness_requirement[weakness]
                world.weapon_damage[weapons_to_id[p_weapon]][bosses[p_boss]] \
                    = world.options.plando_weakness[p_boss][p_weapon]

        # handle special cases
        for boss in range(22):
            for weapon in range(1, 9):
                if (0 < world.weapon_damage[weapon][boss] < minimum_weakness_requirement[weapon] and
                        not any(world.weapon_damage[i][boss] >= minimum_weakness_requirement[weapon]
                                for i in range(1, 8) if i != weapon)):
                    world.weapon_damage[weapon][boss] = minimum_weakness_requirement[weapon]

        if world.weapon_damage[0][world.options.starting_robot_master.value] < 1:
            world.weapon_damage[0][world.options.starting_robot_master.value] = 1

        # weakness validation, it is better to confirm a completable seed than respect plando
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
                if int(uses * boss_damage[wp]) >= boss_health[boss]:
                    used = ceil(boss_health[boss] / boss_damage[wp])
                    weapon_energy[wp] -= weapon_costs[wp] * used
                    boss_health[boss] = 0
                    used_weapons[boss].add(wp)
                elif highest <= 0:
                    # we are out of weapons that can actually damage the boss
                    # so find the weapon that has the most uses, and apply that as an additional weakness
                    # it should be impossible to be out of energy
                    max_uses, wp = max((weapon_energy[weapon] // weapon_costs[weapon], weapon)
                                       for weapon in weapon_weight
                                       if weapon != 0)
                    world.weapon_damage[wp][boss] = minimum_weakness_requirement[wp]
                    used = min(int(weapon_energy[wp] // weapon_costs[wp]),
                               ceil(boss_health[boss] / minimum_weakness_requirement[wp]))
                    weapon_energy[wp] -= weapon_costs[wp] * used
                    boss_health[boss] -= int(used * minimum_weakness_requirement[wp])
                    weapon_weight.pop(wp)
                    used_weapons[boss].add(wp)
                else:
                    # drain the weapon and continue
                    boss_health[boss] -= int(uses * boss_damage[wp])
                    weapon_energy[wp] -= weapon_costs[wp] * uses
                    weapon_weight.pop(wp)
                    used_weapons[boss].add(wp)

            world.wily_4_weapons = {boss: sorted(weapons) for boss, weapons in used_weapons.items()}

    location_rules: dict[str, Rule] = {}

    for i, boss_locations in zip(range(22), [
        get_boss_locations("Needle Man Stage"),
        get_boss_locations("Magnet Man Stage"),
        get_boss_locations("Gemini Man Stage"),
        get_boss_locations("Hard Man Stage"),
        get_boss_locations("Top Man Stage"),
        get_boss_locations("Snake Man Stage"),
        get_boss_locations("Spark Man Stage"),
        get_boss_locations("Shadow Man Stage"),
        get_boss_locations("Doc Robot (Spark) - Metal"),
        get_boss_locations("Doc Robot (Spark) - Quick"),
        get_boss_locations("Doc Robot (Needle) - Air"),
        get_boss_locations("Doc Robot (Needle) - Crash"),
        get_boss_locations("Doc Robot (Gemini) - Flash"),
        get_boss_locations("Doc Robot (Gemini) - Bubble"),
        get_boss_locations("Doc Robot (Shadow) - Wood"),
        get_boss_locations("Doc Robot (Shadow) - Heat"),
        get_boss_locations("Break Man"),
        get_boss_locations("Wily Stage 1"),
        get_boss_locations("Wily Stage 2"),
        get_boss_locations("Wily Stage 3"),
        get_boss_locations("Wily Stage 5"),
        get_boss_locations("Wily Stage 6")
    ]):
        if world.weapon_damage[0][i] > 0:
            continue  # this can always be in logic
        weapons = []
        for weapon in range(1, 9):
            if world.weapon_damage[weapon][i] > 0:
                if world.weapon_damage[weapon][i] < minimum_weakness_requirement[weapon]:
                    continue
                weapons.append(weapons_to_name[weapon])
        if not weapons:
            raise Exception(f"Attempted to have boss {i} with no weakness! Seed: {world.multiworld.seed}")
        for location in boss_locations:
            static_rule = STATIC_LOCATION_RULES.get(location, True_())
            if i in (20, 21):
                # multi-phase fights, get all potential weaknesses
                # we should probably do this smarter, but this works for now
                location_rules[location] = static_rule & HasAll(*weapons)
            else:
                location_rules[location] = static_rule & HasAny(*weapons)

    for location in STATIC_LOCATION_RULES:
        if location not in location_rules:
            location_rules[location] = STATIC_LOCATION_RULES[location]

    # Handle entrance rules
    for region, info in mm3_regions.items():
        entrance = world.get_entrance(f"To {region}")
        static_rule = STATIC_ENTRANCE_RULES.get(entrance.name, True_())
        world.set_rule(entrance, static_rule & HasAll(*info.required_items))

    # Consumable rules
    if world.options.consumables in (world.options.consumables.option_1up_etank,
                                     world.options.consumables.option_all):
        for location in STATIC_1UP_RULES:
            location_rules[location] = STATIC_1UP_RULES[location]

    if world.options.consumables in (world.options.consumables.option_weapon_health,
                                     world.options.consumables.option_all):
        for location in STATIC_ENERGY_RULES:
            location_rules[location] = STATIC_ENERGY_RULES[location]

    for location, rule in location_rules.items():
        world.set_rule(world.get_location(location), rule)
