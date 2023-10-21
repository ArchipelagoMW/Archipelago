from functools import reduce

from BaseClasses import MultiWorld, CollectionState

from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule
from .Items import item_table


class ChecksMateLogic(LogicMixin):
    def total_piece_value(self: CollectionState, player: int) -> int:
        owned_piece_values = [item.value for item_id, item in item_table.items() if self.has(item_id, player)]
        return reduce(lambda a, b: a + b, owned_piece_values, 0)

    def has_piece_value(self, player: int, amount: int) -> bool:
        return self.total_piece_value(player) >= amount


def set_rules(multiworld: MultiWorld, player: int):
    capture_expectations = {
        "Capture Rook A": 5,
        "Capture Rook H": 5,
        "Capture Bishop B": 3,
        "Capture Bishop G": 3,
        "Capture Knight C": 3,
        "Capture Knight F": 3,
        "Capture Queen": 9
    }

    for piece, value in capture_expectations.items():
        set_rule(multiworld.get_location(piece, player), lambda state, v=value: state.has_piece_value(player, v))
    set_rule(multiworld.get_location("Checkmate", player), lambda state: state.has_piece_value(player, 19))
