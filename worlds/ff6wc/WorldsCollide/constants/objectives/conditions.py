from ...constants.objectives.condition_bits import check_bit, quest_bit, boss_bit, dragon_bit
from ...constants.entities import id_character
from ...constants.espers import id_esper

from collections import namedtuple
ConditionType = namedtuple("ConditionType", ["name", "string_function", "value_range", "min_max"])

types = [
    ConditionType("None", "", None, False),
    ConditionType("Random", "Random", ["r"], False),
    ConditionType("Characters", lambda count : f"Recruit {count} Characters",
                  list(range(1, len(id_character) + 1)), True),
    ConditionType("Character", lambda character : f"Recruit {id_character[character].capitalize()}",
                  ["r"] + sorted(id_character, key = id_character.get), False),
    ConditionType("Espers", lambda count : f"Find {count} Espers",
                  list(range(1, len(id_esper) + 1)), True),
    ConditionType("Esper", lambda esper : f"Find {id_esper[esper]}",
                  ["r"] + sorted(id_esper, key = id_esper.get), False),
    ConditionType("Dragons", lambda count : f"Defeat {count} Dragons",
                  list(range(1, len(dragon_bit) + 1)), True),
    ConditionType("Dragon", lambda dragon : f"Defeat {dragon_bit[dragon].name}",
                  ["r"] + list(range(len(dragon_bit))), False),
    ConditionType("Bosses", lambda count : f"Defeat {count} Bosses",
                  list(range(1, len(boss_bit) + 1)), True),
    ConditionType("Boss", lambda boss : f"Defeat {boss_bit[boss].name}",
                  ["r"] + list(range(len(boss_bit))), False),
    ConditionType("Checks", lambda count : f"Complete {count} Checks",
                  list(range(1, len(check_bit) + 1)), True),
    ConditionType("Check", lambda check : f"{check_bit[check].name}",
                  ["r"] + list(range(len(check_bit))), False),
    ConditionType("Quest", lambda quest : f"{quest_bit[quest].name}",
                  ["r"] + list(range(len(quest_bit))), False),
]

name_type = {_type.name : _type for _type in types}

names = list(name_type.keys())
