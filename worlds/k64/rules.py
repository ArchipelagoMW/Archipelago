from worlds.generic.Rules import set_rule, add_rule
from worlds.AutoWorld import LogicMixin
from BaseClasses import MultiWorld
from copy import deepcopy
from .names import LocationName, ItemName
import typing

if typing.TYPE_CHECKING:
    from . import K64World
    from BaseClasses import CollectionState

burn_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 1",
    "Rock Star 2",
    "Rock Star 3",
    "Aqua Star 1",
    "Aqua Star 2",
    "Neo Star 1",
    "Neo Star 3",
    "Neo Star 4",
    "Shiver Star 1",
    "Shiver Star 4",
    "Ripple Star 1",
    "Ripple Star 3",
]

needle_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 1",
    "Rock Star 2",
    "Aqua Star 1",
    "Neo Star 3",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Ripple Star 1",
    "Ripple Star 3",
]

bomb_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 4",
    "Aqua Star 1",
    "Aqua Star 2",
    "Aqua Star 3",
    "Aqua Star 4",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Shiver Star 4",
    "Ripple Star 1",
    "Ripple Star 3",
]

spark_levels = [
    "Pop Star 2",
    "Rock Star 2",
    "Rock Star 4",
    "Aqua Star 1",
    "Aqua Star 2",
    "Aqua Star 4",
    "Shiver Star 2",
    "Shiver Star 3",
    "Ripple Star 1",
    "Ripple Star 3",
]

cutter_levels = [
    "Pop Star 1",
    "Pop Star 2",
    "Pop Star 3",
    "Rock Star 2",
    "Rock Star 3",
    "Aqua Star 1",
    "Aqua Star 3",
    "Aqua Star 4",
    "Neo Star 1",
    "Neo Star 3",
    "Shiver Star 2",
    "Shiver Star 3",
    "Shiver Star 4",
    "Ripple Star 2",
    "Ripple Star 3",
]

stone_levels = [
    "Pop Star 2",
    "Rock Star 1",
    "Rock Star 2",
    "Aqua Star 1",
    "Aqua Star 2",
    "Aqua Star 3",
    "Neo Star 1",
    "Neo Star 3",
    "Neo Star 4",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Shiver Star 4",
    "Ripple Star 1",
    "Ripple Star 3",
]

ice_levels = [
    "Pop Star 2",
    "Rock Star 2",
    "Rock Star 3",
    "Aqua Star 1",
    "Aqua Star 2",
    "Neo Star 3",
    "Shiver Star 1",
    "Shiver Star 2",
    "Shiver Star 3",
    "Ripple Star 1",
    "Ripple Star 3",
]

waddle_copy_levels = {
    "Spark Ability": [
        "Rock Star 1",
        "Neo Star 2"
    ],
    "Cutter Ability": [
        "Aqua Star 2",
        "Neo Star 2",
        "Shiver Star 1"
    ]
}


dedede_copy_levels = {
    "Burning Ability": [
        "Aqua Star 3"
    ],
    "Needle Ability": [
        "Neo Star 4",
        "Ripple Star 2",
    ],
    "Bomb Ability": [
        "Neo Star 4",
    ],
    "Spark Ability": [
        "Neo Star 4",
        "Shiver Star 4",
    ],
    "Cutter Ability": [
        "Neo Star 4",
    ]
}


class K64LogicMixin(LogicMixin):
    game: str = "Kirby 64 - The Crystal Shards"
    k64_stale: dict[int, bool]
    k64_level_state: dict[int, list[bool]]

    def init_mixin(self, multiworld: MultiWorld):
        k64_players = multiworld.get_game_players(self.game)
        self.k64_stale = {player: True for player in k64_players}
        self.k64_level_state = {player: [False, False, False, False, False, False] for player in k64_players}

    def copy_mixin(self, other: "K64LogicMixin"):
        other.k64_stale = self.k64_stale.copy()
        other.k64_level_state = deepcopy(self.k64_level_state)
        return other


def has_any_bomb(state: "CollectionState", player: int):
    for specific, access in zip([ItemName.bomb, ItemName.bomb_bomb, ItemName.bomb_spark, ItemName.bomb_cutter,
                                 ItemName.burn_bomb, ItemName.ice_bomb, ItemName.stone_bomb, ItemName.needle_bomb],
                                [["Bomb Ability"], ["Bomb Ability"], ["Bomb Ability", "Spark Ability"],
                                 ["Bomb Ability", "Cutter Ability"], ["Bomb Ability", "Burning Ability"],
                                 ["Bomb Ability", "Ice Ability"], ["Bomb Ability", "Stone Ability"],
                                 ["Bomb Ability", "Needle Ability"]]):
        if state.has(specific, player) and state.has_all(access, player):
            return True
    return False


def has_any_stone(state: "CollectionState", player: int):
    for specific, access in zip([ItemName.stone, ItemName.stone_stone, ItemName.stone_spark, ItemName.stone_cutter,
                                 ItemName.burn_stone, ItemName.stone_ice, ItemName.stone_bomb, ItemName.stone_needle],
                                [["Stone Ability"], ["Stone Ability"], ["Stone Ability", "Spark Ability"],
                                 ["Stone Ability", "Cutter Ability"], ["Stone Ability", "Burning Ability"],
                                 ["Stone Ability", "Ice Ability"], ["Stone Ability", "Bomb Ability"],
                                 ["Stone Ability", "Needle Ability"]]):
        if state.has(specific, player) and state.has_all(access, player):
            return True
    return False


def has_any_needle(state: "CollectionState", player: int):
    for specific, access in zip([ItemName.needle, ItemName.needle_needle, ItemName.needle_spark, ItemName.needle_cutter,
                                 ItemName.burn_needle, ItemName.ice_needle, ItemName.needle_bomb,
                                 ItemName.stone_needle],
                                [["Needle Ability"], ["Needle Ability"], ["Needle Ability", "Spark Ability"],
                                 ["Needle Ability", "Cutter Ability"], ["Needle Ability", "Burning Ability"],
                                 ["Needle Ability", "Ice Ability"], ["Bomb Ability", "Needle Ability"],
                                 ["Stone Ability", "Needle Ability"]]):
        if state.has(specific, player) and state.has_all(access, player):
            return True
    return False


def has_any_ice(state: "CollectionState", player: int):
    # Used once, Refrigerator does not qualify
    for specific, access in zip([ItemName.ice, ItemName.ice_ice, ItemName.ice_cutter,
                                 ItemName.burn_ice, ItemName.ice_needle, ItemName.ice_bomb, ItemName.stone_ice],
                                [["Ice Ability"], ["Ice Ability"],
                                 ["Ice Ability", "Cutter Ability"], ["Ice Ability", "Burning Ability"],
                                 ["Needle Ability", "Ice Ability"], ["Bomb Ability", "Ice Ability"],
                                 ["Stone Ability", "Ice Ability"]]):
        if state.has(specific, player) and state.has_all(access, player):
            return True
    return False


def has_any_burn(state: "CollectionState", player: int):
    for specific, access in zip([ItemName.burn, ItemName.burn_burn, ItemName.burn_spark, ItemName.burn_cutter,
                                 ItemName.burn_ice, ItemName.burn_needle, ItemName.burn_bomb, ItemName.burn_stone],
                                [["Burning Ability"], ["Burning Ability"], ["Burning Ability", "Spark Ability"],
                                 ["Burning Ability", "Cutter Ability"], ["Ice Ability", "Burning Ability"],
                                 ["Needle Ability", "Burning Ability"], ["Bomb Ability", "Burning Ability"],
                                 ["Stone Ability", "Burning Ability"]]):
        if state.has(specific, player) and state.has_all(access, player):
            return True
    return False


def has_any_spark(state: "CollectionState", player: int):
    for specific, access in zip([ItemName.spark, ItemName.spark_spark, ItemName.burn_spark, ItemName.spark_cutter,
                                 ItemName.ice_spark, ItemName.needle_spark, ItemName.bomb_spark, ItemName.stone_spark],
                                [["Spark Ability"], ["Spark Ability"], ["Burning Ability", "Spark Ability"],
                                 ["Spark Ability", "Cutter Ability"], ["Ice Ability", "Spark Ability"],
                                 ["Needle Ability", "Spark Ability"], ["Bomb Ability", "Spark Ability"],
                                 ["Stone Ability", "Spark Ability"]]):
        if state.has(specific, player) and state.has_all(access, player):
            return True
    return False


def has_any_cutter(state: "CollectionState", player: int):
    for specific, access in zip([ItemName.cutter, ItemName.cutter_cutter, ItemName.spark_cutter, ItemName.burn_cutter,
                                 ItemName.ice_cutter, ItemName.needle_cutter, ItemName.bomb_cutter,
                                 ItemName.stone_cutter],
                                [["Cutter Ability"], ["Cutter Ability"], ["Cutter Ability", "Spark Ability"],
                                 ["Cutter Ability", "Burning Ability"], ["Ice Ability", "Cutter Ability"],
                                 ["Needle Ability", "Cutter Ability"], ["Bomb Ability", "Cutter Ability"],
                                 ["Stone Ability", "Cutter Ability"]]):
        if state.has(specific, player) and state.has_all(access, player):
            return True
    return False


def has_great_cutter(state: "CollectionState", player: int, specific_ability: int):
    if not state.has("Cutter Ability", player):
        return False
    if specific_ability:
        return state.has(ItemName.cutter_cutter, player)
    else:
        return state.has(ItemName.cutter, player)


def has_geokinesis(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Stone Ability", "Spark Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.stone_spark, player) and state.has_any({ItemName.stone, ItemName.spark}, player)
    else:
        return state.has_all({ItemName.stone, ItemName.spark}, player)


def has_lightbulb(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Bomb Ability", "Spark Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.bomb_spark, player) and state.has_any({ItemName.bomb, ItemName.spark}, player)
    else:
        return state.has_all({ItemName.bomb, ItemName.spark}, player)


def has_exploding_snowman(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Bomb Ability", "Ice Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.ice_bomb, player) and state.has_any({ItemName.ice, ItemName.bomb}, player)
    else:
        return state.has_all({ItemName.ice, ItemName.bomb}, player)


def has_volcano(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Stone Ability", "Burning Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.burn_stone, player) and state.has_any({ItemName.stone, ItemName.burn}, player)
    else:
        return state.has_all({ItemName.stone, ItemName.burn}, player)


def has_shurikens(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Bomb Ability", "Cutter Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.bomb_cutter, player) and state.has_any({ItemName.bomb, ItemName.cutter}, player)
    else:
        return state.has_all({ItemName.bomb, ItemName.cutter}, player)


def has_stone_friends(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Stone Ability", "Cutter Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.stone_cutter, player) and state.has_any({ItemName.stone, ItemName.cutter}, player)
    else:
        return state.has_all({ItemName.stone, ItemName.cutter}, player)


def has_dynamite(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Stone Ability", "Bomb Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.stone_bomb, player) and state.has_any({ItemName.stone, ItemName.bomb}, player)
    else:
        return state.has_all({ItemName.stone, ItemName.bomb}, player)


def has_lightning_rod(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Needle Ability", "Spark Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.needle_spark, player) and state.has_any({ItemName.needle, ItemName.spark}, player)
    else:
        return state.has_all({ItemName.needle, ItemName.spark}, player)


def has_drill(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Stone Ability", "Needle Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.stone_needle, player) and state.has_any({ItemName.needle, ItemName.stone}, player)
    else:
        return state.has_all({ItemName.needle, ItemName.stone}, player)


def has_lightsaber(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Cutter Ability", "Spark Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.spark_cutter, player) and state.has_any({ItemName.cutter, ItemName.spark}, player)
    else:
        return state.has_all({ItemName.cutter, ItemName.spark}, player)


def has_exploding_gordo(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Bomb Ability", "Needle Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.needle_bomb, player) and state.has_any({ItemName.needle, ItemName.bomb}, player)
    else:
        return state.has_all({ItemName.needle, ItemName.bomb}, player)


def has_fire_arrows(state: "CollectionState", player: int, specific_ability: int):
    if not state.has_all(["Burning Ability", "Needle Ability"], player):
        return False
    if specific_ability:
        return state.has(ItemName.burn_needle, player) and state.has_any({ItemName.needle, ItemName.burn}, player)
    else:
        return state.has_all({ItemName.needle, ItemName.burn}, player)


def has_waddle_dee(state: "CollectionState", player: int):
    return state.has(ItemName.waddle_dee, player)


def has_adeleine(state: "CollectionState", player: int):
    return state.has(ItemName.adeleine, player)


def has_king_dedede(state: "CollectionState", player: int):
    return state.has(ItemName.king_dedede, player)


def set_rules(world: "K64World") -> None:
    # Level 1
    set_rule(world.get_location(LocationName.pop_star_1_s2), lambda state: has_any_bomb(state, world.player))
    set_rule(world.get_location(LocationName.pop_star_3_s1),
             lambda state: has_great_cutter(state, world.player, world.options.split_power_combos.value))
    # Level 2
    set_rule(world.get_location(LocationName.rock_star_1), lambda state: has_waddle_dee(state, world.player))
    set_rule(world.get_location(LocationName.rock_star_1_s3),
             lambda state: has_geokinesis(state, world.player, world.options.split_power_combos.value)
             and has_waddle_dee(state, world.player))
    set_rule(world.get_location(LocationName.rock_star_2), lambda state: has_king_dedede(state, world.player))
    set_rule(world.get_location(LocationName.rock_star_2_s3), lambda state: has_king_dedede(state, world.player))
    set_rule(world.get_location(LocationName.rock_star_3_s1), lambda state: has_any_stone(state, world.player))
    set_rule(world.get_location(LocationName.rock_star_4_s2),
             lambda state: has_lightbulb(state, world.player, world.options.split_power_combos.value))
    # Level 3
    set_rule(world.get_location(LocationName.aqua_star_1_s3),
             lambda state: has_exploding_snowman(state, world.player, world.options.split_power_combos.value))
    set_rule(world.get_location(LocationName.aqua_star_2_s1),
             lambda state: has_volcano(state, world.player, world.options.split_power_combos.value))
    for location in (LocationName.aqua_star_2, LocationName.aqua_star_2_s2, LocationName.aqua_star_2_s3):
        set_rule(world.get_location(location), lambda state: has_waddle_dee(state, world.player))
    for location in (LocationName.aqua_star_3, LocationName.aqua_star_3_s2, LocationName.aqua_star_3_s3):
        set_rule(world.get_location(location), lambda state: has_king_dedede(state, world.player))
    set_rule(world.get_location(LocationName.aqua_star_3_s1),
             lambda state: has_shurikens(state, world.player, world.options.split_power_combos.value))
    add_rule(world.get_location(LocationName.aqua_star_3_s3),
             lambda state: has_stone_friends(state, world.player, world.options.split_power_combos.value))
    # Level 4
    for location in (LocationName.neo_star_2, LocationName.neo_star_2_s2, LocationName.neo_star_2_s3):
        set_rule(world.get_location(location), lambda state: has_waddle_dee(state, world.player))
    add_rule(world.get_location(LocationName.neo_star_2_s3),
             lambda state: has_dynamite(state, world.player, world.options.split_power_combos.value))
    set_rule(world.get_location(LocationName.neo_star_3_s1), lambda state: has_any_needle(state, world.player))
    set_rule(world.get_location(LocationName.neo_star_3_s2), lambda state: has_adeleine(state, world.player))
    for location in (LocationName.neo_star_4, LocationName.neo_star_4_s1,
                     LocationName.neo_star_4_s2, LocationName.neo_star_4_s3):
        set_rule(world.get_location(location), lambda state: has_king_dedede(state, world.player))
    add_rule(world.get_location(LocationName.neo_star_4_s2), lambda state: has_any_ice(state, world.player))
    # Level 5
    set_rule(world.get_location(LocationName.shiver_star_1_s1), lambda state: has_waddle_dee(state, world.player))
    set_rule(world.get_location(LocationName.shiver_star_1_s2), lambda state: has_any_burn(state, world.player))
    set_rule(world.get_location(LocationName.shiver_star_2_s3),
             lambda state: has_lightning_rod(state, world.player, world.options.split_power_combos.value))
    set_rule(world.get_location(LocationName.shiver_star_3_s3), lambda state: has_adeleine(state, world.player))
    set_rule(world.get_location(LocationName.shiver_star_4_s1),
             lambda state: has_drill(state, world.player, world.options.split_power_combos.value))
    for location in (LocationName.shiver_star_4, LocationName.shiver_star_4_s2, LocationName.shiver_star_4_s3):
        set_rule(world.get_location(location), lambda state: has_king_dedede(state, world.player))
    # Level 6
    set_rule(world.get_location(LocationName.ripple_star_1_s3),
             lambda state: has_exploding_gordo(state, world.player, world.options.split_power_combos.value)
             and state.has_any([ItemName.bomb, ItemName.needle], world.player))  # by default cannot carry enemy across
    set_rule(world.get_location(LocationName.ripple_star_2_s1), lambda state: has_any_spark(state, world.player))
    for location in (LocationName.ripple_star_2, LocationName.ripple_star_2_s2, LocationName.ripple_star_2_s3):
        set_rule(world.get_location(location), lambda state: has_king_dedede(state, world.player))
    add_rule(world.get_location(LocationName.ripple_star_2_s3), lambda state: has_any_cutter(state, world.player))
    set_rule(world.get_location(LocationName.ripple_star_3_s2),
             lambda state: has_fire_arrows(state, world.player, world.options.split_power_combos.value))

    # Crystal Requirements
    for i, level in zip(range(1, 7), world.boss_requirements):
        set_rule(world.multiworld.get_entrance(f"To Level {i + 1}", world.player),
                 lambda state, j=level: state.has(ItemName.crystal_shard, world.player, j))
        set_rule(world.multiworld.get_location(f"{LocationName.level_names[i]} - Boss Defeated", world.player),
                 lambda state, j=level: state.has(ItemName.crystal_shard, world.player, j))

    # Friend Requirement
    add_rule(world.get_entrance("To Level 7"), lambda state: state.has_all([ItemName.waddle_dee, ItemName.adeleine,
                                                                            ItemName.king_dedede], world.player))

    world.multiworld.completion_condition[world.player] = lambda state: state.has(ItemName.ribbons_crystal,
                                                                                  world.player)
