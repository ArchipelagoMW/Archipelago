from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has, Rule, HasFromListUnique
from .locations import FINISHING_MOVES_LOCATIONS
from .options import BossGoal

if TYPE_CHECKING:
    from .world import MKSMWorld

DOUBLE_JUMP: Rule = Has("Double Jump")
WALL_RUN: Rule = Has("Wall Run")
WALL_JUMP: Rule = Has("Wall Jump")
WALL_CLIMB: Rule = Has("Wall Climb")
SWING: Rule = Has("Swing")
LONG_JUMP: Rule = Has("Long Jump")
FIST_OF_RUIN: Rule = Has("Fist of Ruin")
FATALITY: Rule = Has("Blood bar", count=1)
MULTALITY: Rule = Has("Blood bar", count=2)
BRUTALITY: Rule = Has("Blood bar", count=3)

KITANA = Has("Kitana defeated item")
REPTILE = Has("Reptile defeated item")
BARAKA = Has("Baraka defeated item")
GORO = Has("Goro defeated item")
SCORPION = Has("Scorpion defeated item")
ERMAC = Has("Ermac defeated item")
MILEENA = Has("Mileena defeated item")
KANO = Has("Kano defeated item")
SHAO_KAHN = Has("Shao Kahn defeated item")

DEAD_POOL = Has("Dead Pool item")


def set_all_rules(world: MKSMWorld) -> None:
    set_all_location_rules(world)
    connect_regions(world)
    set_completion_condition(world)
    set_purchase_rules(world)
    set_finishing_moves_rules(world)


def set_purchase_rules(world: MKSMWorld) -> None:
    tiers = {
        1: [
            "Purchase upgrade - Square 2",
            "Purchase upgrade - Triangle 2",
            "Purchase upgrade - Circle 2",
            "Purchase upgrade - R2 2",
            "Purchase 1st combo",
        ],
        2: [
            "Purchase upgrade - Square 3",
            "Purchase upgrade - Triangle 3",
            "Purchase upgrade - Circle 3",
            "Purchase upgrade - R2 3",
            "Purchase 2nd combo",
            "Purchase 3rd combo",
        ],
        3: [
            "Purchase upgrade - Square 4",
            "Purchase upgrade - Triangle 4",
            "Purchase upgrade - Circle 4",
            "Purchase upgrade - Circle 5",
            "Purchase upgrade - R2 4",
            "Purchase upgrade - R2 5",
            "Purchase 4th combo",
            "Purchase 5th combo",
        ],
    }

    for tier, loc_names in tiers.items():
        for loc_name in loc_names:
            try:
                loc = world.get_location(loc_name)
            except KeyError:
                continue
            world.set_rule(loc, HasFromListUnique(
                "Kitana defeated item", "Reptile defeated item", "Baraka defeated item",
                "Scorpion defeated item", "Goro defeated item",
                count=tier
            ))


def set_all_location_rules(world: MKSMWorld) -> None:
    world.set_rule(world.get_location("GL: koin above the doorway"), DOUBLE_JUMP | WALL_JUMP)
    world.set_rule(world.get_location("GL: koin above the breakable door"), DOUBLE_JUMP | WALL_JUMP)
    world.set_rule(world.get_location("WSA: koin after the tree branch swing"), SWING | DOUBLE_JUMP)
    world.set_rule(world.get_location("WSA: koin after the bamboo swing"), SWING | (WALL_RUN & DOUBLE_JUMP))
    world.set_rule(
        world.get_location("WSA: koin on a high wall near the lava pots"),
        WALL_RUN & WALL_JUMP & DOUBLE_JUMP
    )
    world.set_rule(world.get_location("P: koin from performing a fatality on the dragon symbol"), FATALITY)
    world.set_rule(world.get_location("N: koin above the arch"), LONG_JUMP | DOUBLE_JUMP)
    world.set_rule(world.get_location("LF: koin behind the living tree"), DOUBLE_JUMP)
    world.set_rule(world.get_location("LF: Forest health upgrade"), WALL_CLIMB | DOUBLE_JUMP)
    world.set_rule(world.get_location("LF: koin from breaking the fast statues"), REPTILE)
    world.set_rule(world.get_location("W: koin found on the lion statue"), DOUBLE_JUMP | WALL_RUN)
    world.set_rule(
        world.get_location("DP: koin from drowning enemies in both pools"),
        WALL_CLIMB | (WALL_JUMP & DOUBLE_JUMP)
    )
    world.set_rule(world.get_location("ST: koin above Baraka's entrance"), WALL_RUN & DOUBLE_JUMP)
    world.set_rule(world.get_location("ST: koin from the broken statue"), FIST_OF_RUIN)
    world.set_rule(world.get_location("ST: koin above the broken statue"), FIST_OF_RUIN)
    world.set_rule(world.get_location("ST: koin from high button in the rolling spikes room"), DOUBLE_JUMP)
    world.set_rule(world.get_location("ST: koin above the ceiling in the room with the hooks"), DOUBLE_JUMP)
    world.set_rule(world.get_location("ST: koin behind statue in the falling spike trap room"), FIST_OF_RUIN)
    world.set_rule(
        world.get_location("ST: koin above broken statue in the falling spike trap room"),
        FIST_OF_RUIN & (DOUBLE_JUMP | WALL_JUMP | WALL_RUN)
    )
    world.set_rule(world.get_location("ST: koin near the fan"), LONG_JUMP | DOUBLE_JUMP)
    world.set_rule(world.get_location("ST: koin from the destroyed soul tomb"), FIST_OF_RUIN)
    world.set_rule(world.get_location("ST: wall jump obtained"), WALL_RUN | DOUBLE_JUMP)
    world.set_rule(world.get_location("F: koin from wall jumping above the main room"), WALL_JUMP & DOUBLE_JUMP)
    world.set_rule(
        world.get_location("F: koin above the wood ceiling"),
        DOUBLE_JUMP & (WALL_JUMP | WALL_RUN)
    )
    world.set_rule(world.get_location("F: koin above the lava pit"), DOUBLE_JUMP)


def connect_regions(world: MKSMWorld) -> None:
    menu = world.get_region("Menu")
    goros_lair_1 = world.get_region("Goro's Lair 1")
    goros_lair_2 = world.get_region("Goro's Lair 2")
    goros_lair_boss = world.get_region("Goro's Lair - Boss arena")
    wu_shi = world.get_region("Wu-Shi")
    wu_shi_ermac = world.get_region("Wu-Shi - Ermac arena")
    wu_shi_fire = world.get_region("Wu-Shi - Fire")
    wu_shi_wallrun = world.get_region("Wu-Shi - Wall Run area")
    portal_1 = world.get_region("Portal 1")
    portal_2 = world.get_region("Portal 2")
    monastery = world.get_region("Monastery")
    monastery_kitana = world.get_region("Monastery - Kitana arena")
    forest = world.get_region("Forest")
    forest_bridges = world.get_region("Forest - Bridges")
    forest_reptile = world.get_region("Forest - Reptile arena")
    tombs = world.get_region("Tombs")
    tombs_baraka = world.get_region("Tombs - Baraka arena")
    wasteland_1 = world.get_region("Wasteland 1")
    wasteland_2 = world.get_region("Wasteland 2")
    wasteland_3 = world.get_region("Wasteland 3")
    dead_pool = world.get_region("Dead Pool")
    netherrealm = world.get_region("Netherrealm")
    foundry = world.get_region("Foundry")

    menu.connect(goros_lair_1)

    goros_lair_1.connect(goros_lair_boss)
    # goros_lair_boss.connect(goros_lair_1, rule=LONG_JUMP | DOUBLE_JUMP)
    goros_lair_1.connect(goros_lair_2, rule=LONG_JUMP | DOUBLE_JUMP)
    # goros_lair_2.connect(goros_lair_boss)
    goros_lair_2.connect(wu_shi)

    # wu_shi.connect(goros_lair_2, rule=FIST_OF_RUIN)
    wu_shi.connect(wu_shi_ermac, rule=FIST_OF_RUIN & SWING)
    # wu_shi_ermac.connect(wu_shi)
    wu_shi.connect(wu_shi_fire)
    # wu_shi_fire.connect(wu_shi)
    wu_shi_fire.connect(wu_shi_wallrun, rule=FIST_OF_RUIN)
    # wu_shi_wallrun.connect(wu_shi_fire, rule=WALL_RUN)
    wu_shi.connect(portal_1)

    portal_1.connect(wu_shi)
    portal_1.connect(portal_2)
    # portal_2.connect(portal_1)

    portal_2.connect(netherrealm, rule=SWING)

    # netherrealm.connect(portal_2)

    portal_1.connect(forest, rule=FIST_OF_RUIN)
    # forest.connect(portal_1)
    forest.connect(forest_bridges, rule=SWING & WALL_CLIMB)
    # forest_bridges.connect(forest)
    forest.connect(forest_reptile)
    # forest_reptile.connect(forest, rule=WALL_CLIMB)

    portal_2.connect(wasteland_1, rule=WALL_CLIMB & (WALL_JUMP | (WALL_RUN & DOUBLE_JUMP)))
    # wasteland_1.connect(portal_2)
    wasteland_1.connect(wasteland_2, rule=FIST_OF_RUIN)
    # wasteland_2.connect(wasteland_1)
    wasteland_2.connect(wasteland_3, rule=DOUBLE_JUMP | WALL_RUN)
    # wasteland_3.connect(wasteland_2)
    wasteland_2.connect(dead_pool, rule=GORO)
    # dead_pool.connect(portal_2, rule=SWING | (DOUBLE_JUMP & WALL_JUMP & WALL_RUN))
    # portal_2.connect(dead_pool, rule=DEAD_POOL)

    portal_1.connect(tombs, rule=WALL_CLIMB)
    # tombs.connect(portal_1)
    tombs.connect(tombs_baraka, rule=FIST_OF_RUIN)
    # tombs_baraka.connect(tombs)
    # tombs_baraka.connect(wu_shi_fire)

    # wu_shi_fire.connect(tombs_baraka, rule=BARAKA)

    portal_1.connect(monastery, rule=DOUBLE_JUMP | LONG_JUMP)
    # monastery.connect(portal_1)
    monastery.connect(monastery_kitana)
    # monastery_kitana.connect(monastery, rule=FIST_OF_RUIN)

    portal_2.connect(
        foundry,
        rule=KITANA & REPTILE & BARAKA & GORO & SCORPION
    )

    # foundry.connect(portal_2)


def set_finishing_moves_rules(world: MKSMWorld) -> None:
    flattened_dict = {loc: loc_id for k, v in FINISHING_MOVES_LOCATIONS.items() for loc, loc_id in v.items()}
    for loc_name in flattened_dict.keys():

        try:
            loc = world.get_location(loc_name)
        except KeyError:
            continue

        if "Fatality" in loc_name:
            world.set_rule(loc, FATALITY)
        elif "Multality" in loc_name:
            world.set_rule(loc, MULTALITY)
        elif "Brutality" in loc_name:
            world.set_rule(loc, BRUTALITY)


def set_completion_condition(world: MKSMWorld) -> None:
    percent = world.options.red_koin_need_percent.value
    enough_red_koins = Has("Red Koin", count=int(world.red_koin_amount * percent / 100))

    goal_rule = enough_red_koins

    if world.options.boss_goal >= BossGoal.option_shao_kahn_only:
        goal_rule = goal_rule & SHAO_KAHN

    if world.options.boss_goal >= BossGoal.option_main_bosses:
        goal_rule = goal_rule & KITANA & REPTILE & BARAKA & GORO & SCORPION

    if world.options.boss_goal >= BossGoal.option_main_and_secret_bosses:
        goal_rule = goal_rule & ERMAC & MILEENA & KANO

    world.set_completion_rule(
        goal_rule
    )
