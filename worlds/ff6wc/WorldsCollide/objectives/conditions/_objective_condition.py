from ...objectives.conditions import _field_condition as field_condition
from ...objectives.conditions import _battle_condition as battle_condition
from ...objectives.conditions import _menu_condition as menu_condition

from ...constants.objectives.conditions import name_type

from ...data import event_bit as event_bit
from ...data import battle_bit as battle_bit
from ...data import event_word as event_word

from enum import Enum
ConditionType = Enum("ConditionType", "EventWord EventBit BattleBit Character Esper")

class ObjectiveCondition:
    def __init__(self, condition_type, *args):
        self.args = args

        self.field_class = getattr(field_condition, condition_type.name + "Condition")
        self.battle_class = getattr(battle_condition, condition_type.name + "Condition")
        self.menu_class = getattr(menu_condition, condition_type.name + "Condition")

        # modify class names for clearer output
        class_name = ''.join([character for character in self.NAME if character.isalnum()])
        if class_name[0].isdigit():
            class_name = '_' + class_name
        self.field_class.__name__ = class_name
        self.field_class.__qualname__ = class_name

        self.battle_class.__name__ = class_name
        self.battle_class.__qualname__ = class_name

        self.menu_class.__name__ = class_name
        self.menu_class.__qualname__ = class_name

    def field(self, *args, **kwargs):
        return self.field_class(*(self.args + args), **kwargs)

    def battle(self, *args, **kwargs):
        return self.battle_class(*(self.args + args), **kwargs)

    def menu(self, *args, **kwargs):
        return self.menu_class(*(self.args + args), **kwargs)

    def __str__(self, *args):
        return name_type[self.NAME].string_function(*args)
