
from typing import List
from BaseClasses import Location
from worlds.generic.Rules import add_rule
from .Characters import all_chars


def get_char_locations(char: str, instance: int, flawless: bool) -> List[str]:
    ''' Returns a list of checks for a given character and instance of that character.'''
    if char not in all_chars:
        raise KeyError(f"{char} not a vanilla character.")

    name = f"{char} {instance}" if instance > 1 else char

    if char == 'Dove':
        # Dove never has flawless rewards
        flawless = False

    if char == 'Melody':
        # Melody doesn't have flawless rewards for ND2
        chests = [f"{name} - Chest {depth}-{floor}" for depth in range(1, 6) for floor in range(1, (5 if flawless else 4)) if not (depth == 5 and floor == 4)]
    elif char == 'Aria':
        # Aria has zone reversal, so she does not have flawless rewards for GL
        chests = [f"{name} - Chest {6-depth}-{floor}" for depth in range(1, 6) for floor in range(1, (5 if flawless else 4)) if not (depth == 5 and floor == 4)]
    else:
        # All other chars have flawless chests on 5-4
        chests = [f"{name} - Chest {depth}-{floor}" for depth in range(1, 6) for floor in range(1, (5 if flawless else 4))]

    return chests + [f'{name} - Clear']


class CryptLocation(Location):

    def __init__(self, player: int, name: str = '', address: int = None, parent=None):
        super().__init__(player, name, address, parent)
        char_name = name.split()[0]
        self.access_rule = lambda state: state.has(f"Unlock {char_name}", player)

