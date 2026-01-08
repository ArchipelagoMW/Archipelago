from ..objectives.results import results
from ..objectives.conditions import conditions
from ..objectives._conditions_complete import ConditionsComplete
from ..objectives._check_complete import CheckComplete

from .. import args as args
import random

class Objective:
    def __init__(self, id):
        self.id = id
        arg_objective = args.objectives[self.id]

        self.letter = arg_objective.letter

        self._init_result(arg_objective.result)
        self._init_conditions(arg_objective.conditions)

        self.conditions_required = random.randint(arg_objective.conditions_required_min,
                                                  arg_objective.conditions_required_max)

        self.conditions_complete = ConditionsComplete(self)
        self.check_complete = CheckComplete(self)

        self.has_suplex_train_condition = False
        for condition in self.conditions:
            if condition.NAME == "Quest" and condition.quest_name() == Objective.suplex_train_quest_name:
                self.has_suplex_train_condition = True
                break

    def _init_result(self, arg_result):
        if arg_result.format_string != "Random":
            self.result = results[arg_result.name](*arg_result.args)
            return

        from ..constants.objectives.results import category_types
        from ..constants.objectives.results import name_category
        from ..constants.objectives.results import types

        category = name_category[arg_result.name]
        if category == "Random":
            possible_types = []
            for _type in types:
                if _type.format_string != "Random":
                    possible_types.append(_type)
        else:
            possible_types = [_type for _type in category_types[category] if _type.format_string != "Random"]

        random_type = random.choice(possible_types)
        if random_type.value_range:
            random_value = random.choice(random_type.value_range)
            random_args = [random_value, random_value]
        else:
            random_args = []

        self.result = results[random_type.name](*random_args)

    def _init_conditions(self, arg_conditions):
        from ..constants.objectives.conditions import types
        from ..constants.objectives.conditions import name_type

        self.conditions = [None] * len(arg_conditions)

        # prevent random duplicate/redundant types/values
        # e.g. requiring celes twice or 2 characters and 4 characters for the same objective

        possible_random_types = [_type.name for _type in types if _type.name != "None" and _type.name != "Random"]
        possible_random_values = {}
        for type_name in possible_random_types:
            _type = name_type[type_name]
            if not _type.min_max:
                possible_random_values[type_name] = [value for value  in _type.value_range if value != 'r']

        if not args.blitz_command_possible:
            possible_random_values["Quest"].remove(Objective.suplex_train_quest_value)

        # to prevent running out of possibilities, must initalize and remove possibilities in specific order

        # first, initialize conditions specifically selected by user (i.e. not 'Random' type/value)
        # do not prevent user from deliberately choosing duplicate/redundant conditions manually
        for index, arg_condition in enumerate(arg_conditions):
            if arg_condition.name != "Random" and arg_condition.args[0] != 'r':
                try:
                    if arg_condition.min_max:
                        # e.g. between x and y characters, remove characters type from possible random types
                        possible_random_types.remove(arg_condition.name)
                    else:
                        # e.g. character x, remove x from possible values but other characters still possible
                        possible_random_values[arg_condition.name].remove(arg_condition.args[0])
                except ValueError:
                    pass# user chose the same type/value twice, ignore
                self.conditions[index] = conditions[arg_condition.name](*arg_condition.args)

        # next, initialize conditions with 'Random' argument chosen
        for index, arg_condition in enumerate(arg_conditions):
            if arg_condition.name != "Random" and arg_condition.args[0] == 'r':
                random_arg = random.choice(possible_random_values[arg_condition.name])
                possible_random_values[arg_condition.name].remove(random_arg)
                self.conditions[index] = conditions[arg_condition.name](random_arg)

        # finally, initialize conditions with 'Random' type
        for index, arg_condition in enumerate(arg_conditions):
            if arg_condition.name == "Random":
                random_type = name_type[random.choice(possible_random_types)]
                possible_random_types.remove(random_type.name)

                if random_type.min_max:
                    random_value = random.choice(random_type.value_range)
                    self.conditions[index] = conditions[random_type.name](random_value, random_value)
                else:
                    random_value = random.choice(possible_random_values[random_type.name])
                    possible_random_values[random_type.name].remove(random_value)
                    self.conditions[index] = conditions[random_type.name](random_value)

    def __str__(self):
        result = f"{self.letter} {str(self.result)} {self.conditions_required}"
        for condition in self.conditions:
            result += f"\n  {str(condition)}"
        return result

    @classmethod
    def _init_suplex_train_quest_value(cls):
        from ..constants.objectives.conditions import name_type
        from ..constants.objectives.condition_bits import quest_bit

        cls.suplex_train_quest_name = "Suplex A Train"
        for value in name_type["Quest"].value_range:
            if value != 'r' and quest_bit[value].name == cls.suplex_train_quest_name:
                cls.suplex_train_quest_value = value
                return
        assert False, f"'{suplex_train_quest_name}' quest value not found"
Objective._init_suplex_train_quest_value()
