import typing

from Options import Choice, Option, Toggle


class AdvancementGoal(Choice):
    option_few = 0
    option_normal = 1
    option_many = 2
    default = 1


class CombatDifficulty(Choice):
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1


minecraft_options: typing.Dict[str, type(Option)] = {
    "advancement_goal": AdvancementGoal,
    "combat_difficulty": CombatDifficulty,
    "include_hard_advancements": Toggle,
    "include_insane_advancements": Toggle,
    "include_postgame_advancements": Toggle,
    "shuffle_structures": Toggle
}