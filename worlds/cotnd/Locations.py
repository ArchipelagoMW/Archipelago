
from typing import List
from functools import partial
from BaseClasses import Location
from worlds.generic.Rules import add_rule
from ..AutoWorld import LogicMixin
from .Characters import all_chars, weaponlocked, ohko, ohko_armor


def get_char_locations(char: str, instance: int, flawless: bool, amplified: bool) -> List[str]:
    ''' Returns a list of checks for a given character and instance of that character.'''
    if char not in all_chars:
        raise KeyError(f"{char} not a vanilla character.")

    name = f"{char} {instance}" if instance > 1 else char

    last_zone = 5 if amplified else 4

    if char == 'Dove':
        # Dove never has flawless rewards
        flawless = False

    if char == 'Melody':
        # Melody doesn't have flawless rewards for ND2
        chests = [f"{name} - Chest {depth}-{floor}" for depth in range(1, last_zone+1) for floor in range(1, (5 if flawless else 4)) if not (depth == last_zone and floor == 4)]
    elif char == 'Aria':
        # Aria has zone reversal, so she does not have flawless rewards for GL
        chests = [f"{name} - Chest {(last_zone+1)-depth}-{floor}" for depth in range(1, last_zone+1) for floor in range(1, (5 if flawless else 4)) if not (depth == last_zone and floor == 4)]
    else:
        # All other chars have flawless chests on 5-4
        chests = [f"{name} - Chest {depth}-{floor}" for depth in range(1, last_zone+1) for floor in range(1, (5 if flawless else 4))]

    return chests + [f'{name} - Clear']


def reach_crypt_location(location, amplified, state):
    player = location.player
    char_name = location.name.split()[0]
    if not state.has(f'Unlock {char_name}', player):
        return False

    floor_name = location.name.split()[-1]
    if floor_name == 'Clear':
        zone = 5 if amplified else 4
    else:
        zone = int(floor_name.split('-')[0])

    # Aria zone reversal for logic
    if char_name == 'Aria':
        zone = (6 if amplified else 5) - zone

    if zone > 1:
        if char_name not in weaponlocked and not state.has_group('Weapon', player, 3):
            return False
    if zone > 2:
        if char_name not in ohko:
            if not state.has_group('Armor', player, 3):
                return False
        else:
            if not state.has_any(ohko_armor, player):
                return False
    if zone > 3:
        if state.count_group('Ring', player) + state.count_group('Spell', player) < 4:
            return False
    return True


class CryptLocation(Location):
    game: str = 'Crypt of the NecroDancer'

    def __init__(self, player: int, name: str = '', address: int = None, parent=None, reduce_logic=False, amplified=True):
        super().__init__(player, name, address, parent)
        if reduce_logic:
            self.access_rule = lambda state: state.has(f'Unlock {name.split()[0]}', player)
        else:
            self.access_rule = partial(reach_crypt_location, self, amplified)
