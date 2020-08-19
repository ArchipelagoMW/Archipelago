import logging
from typing import Optional

from BaseClasses import Boss
from Fill import FillError


def BossFactory(boss: str, player: int) -> Optional[Boss]:
    if boss is None:
        return None
    if boss in boss_table:
        enemizer_name, defeat_rule = boss_table[boss]
        return Boss(boss, enemizer_name, defeat_rule, player)

    logging.error('Unknown Boss: %s', boss)
    return None


def ArmosKnightsDefeatRule(state, player: int):
    # Magic amounts are probably a bit overkill
    return (
            state.has_melee_weapon(player) or
            state.can_shoot_arrows(player) or
            (state.has('Cane of Somaria', player) and state.can_extend_magic(player, 10)) or
            (state.has('Cane of Byrna', player) and state.can_extend_magic(player, 16)) or
            (state.has('Ice Rod', player) and state.can_extend_magic(player, 32)) or
            (state.has('Fire Rod', player) and state.can_extend_magic(player, 32)) or
            state.has('Blue Boomerang', player) or
            state.has('Red Boomerang', player))


def LanmolasDefeatRule(state, player: int):
    return (
            state.has_melee_weapon(player) or
            state.has('Fire Rod', player) or
            state.has('Ice Rod', player) or
            state.has('Cane of Somaria', player) or
            state.has('Cane of Byrna', player) or
            state.can_shoot_arrows(player))


def MoldormDefeatRule(state, player: int):
    return state.has_melee_weapon(player)


def HelmasaurKingDefeatRule(state, player: int):
    # TODO: technically possible with the hammer
    return state.has_sword(player) or state.can_shoot_arrows(player)


def ArrghusDefeatRule(state, player: int):
    if not state.has('Hookshot', player):
        return False
    # TODO: ideally we would have a check for bow and silvers, which combined with the
    # hookshot is enough. This is not coded yet because the silvers that only work in pyramid feature
    # makes this complicated
    if state.has_melee_weapon(player):
        return True

    return ((state.has('Fire Rod', player) and (state.can_shoot_arrows(player) or state.can_extend_magic(player,
                                                                                                         12))) or  # assuming mostly gitting two puff with one shot
            (state.has('Ice Rod', player) and (state.can_shoot_arrows(player) or state.can_extend_magic(player, 16))))


def MothulaDefeatRule(state, player: int):
    return (
            state.has_melee_weapon(player) or
            (state.has('Fire Rod', player) and state.can_extend_magic(player, 10)) or
            # TODO: Not sure how much (if any) extend magic is needed for these two, since they only apply
            # to non-vanilla locations, so are harder to test, so sticking with what VT has for now:
            (state.has('Cane of Somaria', player) and state.can_extend_magic(player, 16)) or
            (state.has('Cane of Byrna', player) and state.can_extend_magic(player, 16)) or
            state.can_get_good_bee(player)
    )


def BlindDefeatRule(state, player: int):
    return state.has_melee_weapon(player) or state.has('Cane of Somaria', player) or state.has('Cane of Byrna', player)


def KholdstareDefeatRule(state, player: int):
    return (
            (
                    state.has('Fire Rod', player) or
                    (
                            state.has('Bombos', player) and
                            # FIXME: the following only actually works for the vanilla location for swordless
                            (state.has_sword(player) or state.world.swords[player] == 'swordless')
                    )
            ) and
            (
                    state.has_melee_weapon(player) or
                    (state.has('Fire Rod', player) and state.can_extend_magic(player, 20)) or
                    # FIXME: this actually only works for the vanilla location for swordless
                    (
                            state.has('Fire Rod', player) and
                            state.has('Bombos', player) and
                            state.world.swords[player] == 'swordless' and
                            state.can_extend_magic(player, 16)
                    )
            )
    )


def VitreousDefeatRule(state, player: int):
    return state.can_shoot_arrows(player) or state.has_melee_weapon(player)


def TrinexxDefeatRule(state, player: int):
    if not (state.has('Fire Rod', player) and state.has('Ice Rod', player)):
        return False
    return state.has('Hammer', player) or state.has('Tempered Sword', player) or state.has('Golden Sword', player) or \
           (state.has('Master Sword', player) and state.can_extend_magic(player, 16)) or \
           (state.has_sword(player) and state.can_extend_magic(player, 32))


def AgahnimDefeatRule(state, player: int):
    return state.has_sword(player) or state.has('Hammer', player) or state.has('Bug Catching Net', player)


boss_table = {
    'Armos Knights': ('Armos', ArmosKnightsDefeatRule),
    'Lanmolas': ('Lanmola', LanmolasDefeatRule),
    'Moldorm': ('Moldorm', MoldormDefeatRule),
    'Helmasaur King': ('Helmasaur', HelmasaurKingDefeatRule),
    'Arrghus': ('Arrghus', ArrghusDefeatRule),
    'Mothula': ('Mothula', MothulaDefeatRule),
    'Blind': ('Blind', BlindDefeatRule),
    'Kholdstare': ('Kholdstare', KholdstareDefeatRule),
    'Vitreous': ('Vitreous', VitreousDefeatRule),
    'Trinexx': ('Trinexx', TrinexxDefeatRule),
    'Agahnim': ('Agahnim', AgahnimDefeatRule),
    'Agahnim2': ('Agahnim2', AgahnimDefeatRule)
}


def can_place_boss(world, player: int, boss: str, dungeon_name: str, level: Optional[str] = None) -> bool:
    if world.swords[player] in ['swordless'] and boss == 'Kholdstare' and dungeon_name != 'Ice Palace':
        return False

    if dungeon_name in ['Ganons Tower', 'Inverted Ganons Tower'] and level == 'top':
        if boss in ["Armos Knights", "Arrghus", "Blind", "Trinexx", "Lanmolas"]:
            return False

    if dungeon_name in ['Ganons Tower', 'Inverted Ganons Tower'] and level == 'middle':
        if boss in ["Blind"]:
            return False

    if dungeon_name == 'Tower of Hera' and boss in ["Armos Knights", "Arrghus", "Blind", "Trinexx", "Lanmolas"]:
        return False

    if dungeon_name == 'Skull Woods' and boss in ["Trinexx"]:
        return False

    if boss in ["Agahnim", "Agahnim2", "Ganon"]:
        return False
    return True


def place_boss(world, player: int, boss: str, location: str, level: Optional[str]):
    logging.debug('Placing boss %s at %s', boss, location + (' (' + level + ')' if level else ''))
    world.get_dungeon(location, player).bosses[level] = BossFactory(boss, player)


def place_bosses(world, player: int):
    if world.boss_shuffle[player] == 'none':
        return
    # Most to least restrictive order
    if world.mode[player] != 'inverted':
        boss_locations = [
            ['Ganons Tower', 'top'],
            ['Tower of Hera', None],
            ['Skull Woods', None],
            ['Ganons Tower', 'middle'],
            ['Eastern Palace', None],
            ['Desert Palace', None],
            ['Palace of Darkness', None],
            ['Swamp Palace', None],
            ['Thieves Town', None],
            ['Ice Palace', None],
            ['Misery Mire', None],
            ['Turtle Rock', None],
            ['Ganons Tower', 'bottom'],
        ]
    else:
        boss_locations = [
            ['Inverted Ganons Tower', 'top'],
            ['Tower of Hera', None],
            ['Skull Woods', None],
            ['Inverted Ganons Tower', 'middle'],
            ['Eastern Palace', None],
            ['Desert Palace', None],
            ['Palace of Darkness', None],
            ['Swamp Palace', None],
            ['Thieves Town', None],
            ['Ice Palace', None],
            ['Misery Mire', None],
            ['Turtle Rock', None],
            ['Inverted Ganons Tower', 'bottom'],
        ]

    all_bosses = sorted(boss_table.keys())  # sorted to be deterministic on older pythons
    placeable_bosses = [boss for boss in all_bosses if boss not in ['Agahnim', 'Agahnim2', 'Ganon']]
    anywhere_bosses = [boss for boss in placeable_bosses if all(
        can_place_boss(world, player, boss, loc, level) for loc, level in boss_locations)]
    if world.boss_shuffle[player] in ["basic", "normal"]:
        # temporary hack for swordless kholdstare:
        if world.swords[player] == 'swordless':
            place_boss(world, player, 'Kholdstare', 'Ice Palace', None)
            boss_locations.remove(['Ice Palace', None])
            placeable_bosses.remove('Kholdstare')

        if world.boss_shuffle[player] == "basic":  # vanilla bosses shuffled
            bosses = placeable_bosses + ['Armos Knights', 'Lanmolas', 'Moldorm']
        else:  # all bosses present, the three duplicates chosen at random
            bosses = all_bosses + [world.random.choice(placeable_bosses) for _ in range(3)]

        logging.debug('Bosses chosen %s', bosses)

        world.random.shuffle(bosses)
        for [loc, level] in boss_locations:
            boss = next((b for b in bosses if can_place_boss(world, player, b, loc, level)), None)
            if not boss:
                loc_text = loc + (' (' + level + ')' if level else '')
                raise FillError('Could not place boss for location %s' % loc_text)
            bosses.remove(boss)
            place_boss(world, player, boss, loc, level)

    elif world.boss_shuffle[player] == "chaos":  # all bosses chosen at random
        for [loc, level] in boss_locations:
            try:
                boss = world.random.choice(
                    [b for b in placeable_bosses if can_place_boss(world, player, b, loc, level)])
            except IndexError:
                loc_text = loc + (' (' + level + ')' if level else '')
                raise FillError('Could not place boss for location %s' % loc_text)
            else:
                place_boss(world, player, boss, loc, level)

    elif world.boss_shuffle[player] == "singularity":
        primary_boss = world.random.choice(placeable_bosses)
        remaining_boss_locations = []
        for loc, level in boss_locations:
            # place that boss where it can go
            if can_place_boss(world, player, primary_boss, loc, level):
                place_boss(world, player, primary_boss, loc, level)
            else:
                remaining_boss_locations.append((loc, level))
        if remaining_boss_locations:
            # pick a boss to go into the remaining locations
            remaining_boss = world.random.choice([boss for boss in placeable_bosses if all(
                can_place_boss(world, player, boss, loc, level) for loc, level in remaining_boss_locations)])
            for loc, level in remaining_boss_locations:
                place_boss(world, player, remaining_boss, loc, level)
