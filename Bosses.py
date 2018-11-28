import logging
import random

from BaseClasses import Boss
from Fill import FillError

def BossFactory(boss):
    if boss is None:
        return None
    if boss in boss_table:
        enemizer_name, defeat_rule = boss_table[boss]
        return Boss(boss, enemizer_name, defeat_rule)

    logging.getLogger('').error('Unknown Boss: %s', boss)
    return None

def ArmosKnightsDefeatRule(state):
    # Magic amounts are probably a bit overkill
    return (
        state.has_blunt_weapon() or
        (state.has('Cane of Somaria') and state.can_extend_magic(10)) or
        (state.has('Cane of Byrna') and state.can_extend_magic(16)) or
        (state.has('Ice Rod') and state.can_extend_magic(32)) or
        (state.has('Fire Rod') and state.can_extend_magic(32)) or
        state.has('Blue Boomerang') or
        state.has('Red Boomerang'))

def LanmolasDefeatRule(state):
    # TODO: Allow the canes here?
    return (
        state.has_blunt_weapon() or
        state.has('Fire Rod') or
        state.has('Ice Rod') or
        state.can_shoot_arrows())

def MoldormDefeatRule(state):
    return state.has_blunt_weapon()

def HelmasaurKingDefeatRule(state):
    return state.has_blunt_weapon() or state.can_shoot_arrows()

def ArrghusDefeatRule(state):
    if not state.has('Hookshot'):
        return False
    # TODO: ideally we would have a check for bow and silvers, which combined with the
    # hookshot is enough. This is not coded yet because the silvers that only work in pyramid feature
    # makes this complicated
    if state.has_blunt_weapon():
        return True

    return ((state.has('Fire Rod') and (state.can_shoot_arrows() or state.can_extend_magic(12))) or #assuming mostly gitting two puff with one shot
            (state.has('Ice Rod') and (state.can_shoot_arrows() or state.can_extend_magic(16))))


def MothulaDefeatRule(state):
    return (
        state.has_blunt_weapon() or
        (state.has('Fire Rod') and state.can_extend_magic(10)) or
        # TODO: Not sure how much (if any) extend magic is needed for these two, since they only apply
        # to non-vanilla locations, so are harder to test, so sticking with what VT has for now:
        (state.has('Cane of Somaria') and state.can_extend_magic(16)) or
        (state.has('Cane of Byrna') and state.can_extend_magic(16)) or
        state.can_get_good_bee()
    )

def BlindDefeatRule(state):
    return state.has_blunt_weapon() or state.has('Cane of Somaria') or state.has('Cane of Byrna')

def KholdstareDefeatRule(state):
    return (
        (
            state.has('Fire Rod') or
            (
                state.has('Bombos') and
                # FIXME: the following only actually works for the vanilla location for swordless mode
                (state.has_sword() or state.world.mode == 'swordless')
            )
        ) and
        (
            state.has_blunt_weapon() or
            (state.has('Fire Rod') and state.can_extend_magic(20)) or
            # FIXME: this actually only works for the vanilla location for swordless mode
            (
                state.has('Fire Rod') and
                state.has('Bombos') and
                state.world.mode == 'swordless' and
                state.can_extend_magic(16)
            )
        )
    )

def VitreousDefeatRule(state):
    return state.can_shoot_arrows() or state.has_blunt_weapon()

def TrinexxDefeatRule(state):
    if not (state.has('Fire Rod') and state.has('Ice Rod')):
        return False
    return state.has('Hammer') or state.has_beam_sword() or (state.has_sword() and state.can_extend_magic(32))

def AgahnimDefeatRule(state):
    return state.has_sword() or state.has('Hammer') or state.has('Bug Catching Net')

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

def can_place_boss(world, boss, dungeon_name, level=None):
    if world.mode in ['swordless'] and boss == 'Kholdstare' and dungeon_name != 'Ice Palace':
        return False

    if dungeon_name == 'Ganons Tower' and level == 'top':
        if boss in ["Armos Knights", "Arrghus",	"Blind", "Trinexx", "Lanmolas"]:
            return False

    if dungeon_name == 'Ganons Tower' and level == 'middle':
        if boss in ["Blind"]:
            return False

    if dungeon_name == 'Tower of Hera' and boss in ["Armos Knights", "Arrghus",	"Blind", "Trinexx", "Lanmolas"]:
        return False

    if dungeon_name == 'Skull Woods' and boss in ["Trinexx"]:
        return False

    if boss in ["Agahnim",	"Agahnim2",	"Ganon"]:
        return False
    return True

def place_bosses(world):
    if world.boss_shuffle == 'none':
        return
    # Most to least restrictive order
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
    all_bosses = sorted(boss_table.keys()) #s orted to be deterministic on older pythons
    placeable_bosses = [boss for boss in all_bosses if boss not in ['Agahnim', 'Agahnim2', 'Ganon']]

    if world.boss_shuffle in ["basic", "normal"]:
        # temporary hack for swordless kholdstare:
        if world.mode == 'swordless':
            world.get_dungeon('Ice Palace').boss = BossFactory('Kholdstare')
            logging.getLogger('').debug('Placing boss Kholdstare at Ice Palace')
            boss_locations.remove(['Ice Palace', None])
            placeable_bosses.remove('Kholdstare')

        if world.boss_shuffle == "basic": # vanilla bosses shuffled
            bosses = placeable_bosses + ['Armos Knights', 'Lanmolas', 'Moldorm']
        else: # all bosses present, the three duplicates chosen at random
            bosses = all_bosses + [random.choice(placeable_bosses) for _ in range(3)]

        logging.getLogger('').debug('Bosses chosen %s', bosses)

        random.shuffle(bosses)
        for [loc, level] in boss_locations:
            loc_text = loc + (' ('+level+')' if level else '')
            boss = next((b for b in bosses if can_place_boss(world, b, loc, level)), None)
            if not boss:
                raise FillError('Could not place boss for location %s' % loc_text)
            bosses.remove(boss)

            logging.getLogger('').debug('Placing boss %s at %s', boss, loc_text)
            world.get_dungeon(loc).bosses[level] = BossFactory(boss)
    elif world.boss_shuffle == "chaos": #all bosses chosen at random
        for [loc, level] in boss_locations:
            loc_text = loc + (' ('+level+')' if level else '')
            try:
                boss = random.choice([b for b in placeable_bosses if can_place_boss(world, b, loc, level)])
            except IndexError:
                raise FillError('Could not place boss for location %s' % loc_text)

            logging.getLogger('').debug('Placing boss %s at %s', boss, loc_text)
            world.get_dungeon(loc).bosses[level] = BossFactory(boss)
