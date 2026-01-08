from ...objectives.results import _field_result as field_result
from ...objectives.results import _battle_result as battle_result

from ...constants.objectives.results import name_type

from ...memory.space import Bank, START_ADDRESS_SNES, Write
from ...instruction import field as field
from ...instruction import asm as asm
import random

class ObjectiveResult:
    def __init__(self, field_class, battle_class, *args):
        self.field_class = field_class
        self.battle_class = battle_class
        self.args = args

        # modify class names for clearer output
        class_name = ''.join([character for character in self.NAME if character.isalnum()])
        self.field_class.__name__ = class_name
        self.field_class.__qualname__ = class_name

        self.battle_class.__name__ = class_name
        self.battle_class.__qualname__ = class_name

    def field(self, *args, **kwargs):
        return self.field_class(*(self.args + args), **kwargs)

    def battle(self, *args, **kwargs):
        return self.battle_class(*(self.args + args), **kwargs)

    def __str__(self):
        return name_type[self.NAME].format_string.format(*self.args)
