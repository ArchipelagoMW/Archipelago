from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule

class BingoLogic(LogicMixin):
    def _bingo_has_horizontal(self, cardn: int, linen: int, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        line = cards[cardn-1][linen-1]
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
        if line > 2:
            return False
        for call in diag:
            if call != 0:  # not a free space
                if not self.has(call, player):
                    return False
        return True

    def _bingo_has_any_line(self, cardn: int, player):
        for l in range(1, 6):
            if (self._bingo_has_horizontal(cardn, l, player) or self._bingo_has_vertical(cardn, l, player) or
                    self._bingo_has_diagonal(cardn, l, player)):
                return True
        return False

    def _bingo_completed(self, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        if self.world.bingo_mode[player] == 1:
            for card in cards:
                for row in card:
                    for call in row:
                        if call != 0:  # not a free space
                            if not self.has(call, player):
                                return False
        elif self.world.bingo_mode[player] == 0:
            for card in range(1, len(cards)+1):
                card_completed = 0
                for l in range(1, 6):
                    if (self._bingo_has_horizontal(card, l, player) or self._bingo_has_vertical(card, l, player) or
                            self._bingo_has_diagonal(card, l, player)):
                        card_completed = 1
                        break
                if card_completed == 0:
                    return False

        return True


def set_rules(world: MultiWorld, player: int):
    for c in range(1, len(world.worlds[player].cards[player]) + 1):
        if world.bingo_mode[player] == 1:
            for l in range(1, 6):
                set_rule(world.get_location(f"Bingo Card {c} Horizontal {l}", player),
                         lambda state, card=c, line=l: state._bingo_has_horizontal(card, line, player))
                set_rule(world.get_location(f"Bingo Card {c} Vertical {l}", player),
                         lambda state, card=c, line=l: state._bingo_has_vertical(card, line, player))
                if l < 3:
                    set_rule(world.get_location(f"Bingo Card {c} Diagonal {l}", player),
                             lambda state, card=c, line=l: state._bingo_has_diagonal(card, line, player))
        elif world.bingo_mode[player] == 0:
            set_rule(world.get_location(f"Bingo Card {c}", player),
                     lambda state, card=c: state._bingo_has_any_line(card, player))
    set_rule(world.get_location("Completed Cards", player), lambda state: state._bingo_completed(player))