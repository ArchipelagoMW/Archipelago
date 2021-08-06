import typing
from Options import Choice, Option, Toggle, Range


class AdvancementGoal(Range):
    range_start = 0
    range_end = 87
    default = 50


class CombatDifficulty(Choice):
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1


class BeeTraps(Range): 
    range_start = 0
    range_end = 100


class EggShards(Range):
    range_start = 0
    range_end = 30


minecraft_options: typing.Dict[str, type(Option)] = {
    "advancement_goal": AdvancementGoal,
    "combat_difficulty": CombatDifficulty,
    "include_hard_advancements": Toggle,
    "include_insane_advancements": Toggle,
    "include_postgame_advancements": Toggle,
    "shuffle_structures": Toggle,
    "structure_compasses": Toggle,
    "bee_traps": BeeTraps,
    "egg_shards_required": EggShards,
    "egg_shards_available": EggShards
}