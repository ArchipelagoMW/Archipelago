from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule

class BingoLogic(LogicMixin):
    def _bingo_has_horizontal(self, card: int, linen: int, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        line = cards[card-1][linen-1]
        for call in line:
            if call != 0:  # not a free space
                if not self.has(call, player):
                    return False
        return True

    def _bingo_has_vertical(self, cardn: int, line: int, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        card = cards[cardn-1]
        for row in card:
            call = row[line-1]
            if call != 0:  # not a free space
                if not self.has(call, player):
                    return False
        return True

    def _bingo_has_diagonal(self, cardn: int, line: int, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        card = cards[cardn-1]
        diag = []
        if line == 1:
            for x in range(0, 5):
                diag.append(card[x][x])
        if line == 2:
            for x in range(0, 5):
                diag.append(card[4-x][x])
        for call in diag:
            if call != 0:  # not a free space
                if not self.has(call, player):
                    return False
        return True

    def _bingo_completed(self, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        for card in cards:
            for row in card:
                for call in row:
                    if call != 0:  # not a free space
                        if not self.has(call, player):
                            return False
        return True


def set_rules(world: MultiWorld, player: int):
    for c in range(1, (world.card_pairs[player] * 2) + 1):
        for l in range(1, 6):
            set_rule(world.get_location(f"Bingo Card {c} Horizontal {l}", player),
                     lambda state, card=c, line=l: state._bingo_has_horizontal(card, line, player))
            set_rule(world.get_location(f"Bingo Card {c} Vertical {l}", player),
                     lambda state, card=c, line=l: state._bingo_has_vertical(card, line, player))
            if l < 3:
                set_rule(world.get_location(f"Bingo Card {c} Diagonal {l}", player),
                         lambda state, card=c, line=l: state._bingo_has_diagonal(card, line, player))
    set_rule(world.get_location("Completed Cards", player), lambda state: state._bingo_completed(player))