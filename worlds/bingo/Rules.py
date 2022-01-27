from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule

class BingoLogic(LogicMixin):
    def _bingo_has_horizontal(self, card: int, linen: int, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        line = cards[card-1][linen-1]
        for c in line:
            if c != 0:
                if not self.has(c, player):
                    return False
        return True

    def _bingo_has_vertical(self, cardn: int, line: int, player) -> bool:
        cards = self.world.worlds[player].cards[player]
        card = cards[cardn-1]
        for row in card:
            c = row[line-1]
            if c != 0:
                if not self.has(c, player):
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
        for c in diag:
            if c != 0:
                if not self.has(c, player):
                    return False
        return True

    def _bingo_completed(self, player):
        cards = self.world.worlds[player].cards[player]
        for card in cards:
            for row in card:
                for c in row:
                    if c != 0:
                        if not self.has(c, player):
                            return False
        return True


def set_rules(world: MultiWorld, player: int):
    set_rule(world.get_location("Card 1 Horizontal 1", player),
             lambda state: state._bingo_has_horizontal(1, 1, player))
    set_rule(world.get_location("Card 1 Vertical 1", player),
             lambda state: state._bingo_has_vertical(1, 1, player))
    set_rule(world.get_location("Card 1 Diagonal 1", player),
             lambda state: state._bingo_has_diagonal(1, 1, player))
    set_rule(world.get_location("Card 1 Horizontal 2", player),
             lambda state: state._bingo_has_horizontal(1, 2, player))
    set_rule(world.get_location("Card 1 Vertical 2", player),
             lambda state: state._bingo_has_vertical(1, 2, player))
    set_rule(world.get_location("Card 1 Diagonal 2", player),
             lambda state: state._bingo_has_diagonal(1, 2, player))
    set_rule(world.get_location("Card 1 Horizontal 3", player),
             lambda state: state._bingo_has_horizontal(1, 3, player))
    set_rule(world.get_location("Card 1 Vertical 3", player),
             lambda state: state._bingo_has_vertical(1, 3, player))
    set_rule(world.get_location("Card 1 Horizontal 4", player),
             lambda state: state._bingo_has_horizontal(1, 4, player))
    set_rule(world.get_location("Card 1 Vertical 4", player),
             lambda state: state._bingo_has_vertical(1, 4, player))
    set_rule(world.get_location("Card 1 Horizontal 5", player),
             lambda state: state._bingo_has_horizontal(1, 5, player))
    set_rule(world.get_location("Card 1 Vertical 5", player),
             lambda state: state._bingo_has_vertical(1, 5, player))
    set_rule(world.get_location("Card 2 Horizontal 1", player),
             lambda state: state._bingo_has_horizontal(2, 1, player))
    set_rule(world.get_location("Card 2 Vertical 1", player),
             lambda state: state._bingo_has_vertical(2, 1, player))
    set_rule(world.get_location("Card 2 Diagonal 1", player),
             lambda state: state._bingo_has_diagonal(2, 1, player))
    set_rule(world.get_location("Card 2 Horizontal 2", player),
             lambda state: state._bingo_has_horizontal(2, 2, player))
    set_rule(world.get_location("Card 2 Vertical 2", player),
             lambda state: state._bingo_has_vertical(2, 2, player))
    set_rule(world.get_location("Card 2 Diagonal 2", player),
             lambda state: state._bingo_has_diagonal(2, 2, player))
    set_rule(world.get_location("Card 2 Horizontal 3", player),
             lambda state: state._bingo_has_horizontal(2, 3, player))
    set_rule(world.get_location("Card 2 Vertical 3", player),
             lambda state: state._bingo_has_vertical(2, 3, player))
    set_rule(world.get_location("Card 2 Horizontal 4", player),
             lambda state: state._bingo_has_horizontal(2, 4, player))
    set_rule(world.get_location("Card 2 Vertical 4", player),
             lambda state: state._bingo_has_vertical(2, 4, player))
    set_rule(world.get_location("Card 2 Horizontal 5", player),
             lambda state: state._bingo_has_horizontal(2, 5, player))
    set_rule(world.get_location("Card 2 Vertical 5", player),
             lambda state: state._bingo_has_vertical(2, 5, player))
    if world.card_pairs[player] > 1:
        set_rule(world.get_location("Card 3 Horizontal 1", player),
                 lambda state: state._bingo_has_horizontal(3, 1, player))
        set_rule(world.get_location("Card 3 Vertical 1", player),
                 lambda state: state._bingo_has_vertical(3, 1, player))
        set_rule(world.get_location("Card 3 Diagonal 1", player),
                 lambda state: state._bingo_has_diagonal(3, 1, player))
        set_rule(world.get_location("Card 3 Horizontal 2", player),
                 lambda state: state._bingo_has_horizontal(3, 2, player))
        set_rule(world.get_location("Card 3 Vertical 2", player),
                 lambda state: state._bingo_has_vertical(3, 2, player))
        set_rule(world.get_location("Card 3 Diagonal 2", player),
                 lambda state: state._bingo_has_diagonal(3, 2, player))
        set_rule(world.get_location("Card 3 Horizontal 3", player),
                 lambda state: state._bingo_has_horizontal(3, 3, player))
        set_rule(world.get_location("Card 3 Vertical 3", player),
                 lambda state: state._bingo_has_vertical(3, 3, player))
        set_rule(world.get_location("Card 3 Horizontal 4", player),
                 lambda state: state._bingo_has_horizontal(3, 4, player))
        set_rule(world.get_location("Card 3 Vertical 4", player),
                 lambda state: state._bingo_has_vertical(3, 4, player))
        set_rule(world.get_location("Card 3 Horizontal 5", player),
                 lambda state: state._bingo_has_horizontal(3, 5, player))
        set_rule(world.get_location("Card 3 Vertical 5", player),
                 lambda state: state._bingo_has_vertical(3, 5, player))
        set_rule(world.get_location("Card 4 Horizontal 1", player),
                 lambda state: state._bingo_has_horizontal(4, 1, player))
        set_rule(world.get_location("Card 4 Vertical 1", player),
                 lambda state: state._bingo_has_vertical(4, 1, player))
        set_rule(world.get_location("Card 4 Diagonal 1", player),
                 lambda state: state._bingo_has_diagonal(4, 1, player))
        set_rule(world.get_location("Card 4 Horizontal 2", player),
                 lambda state: state._bingo_has_horizontal(4, 2, player))
        set_rule(world.get_location("Card 4 Vertical 2", player),
                 lambda state: state._bingo_has_vertical(4, 2, player))
        set_rule(world.get_location("Card 4 Diagonal 2", player),
                 lambda state: state._bingo_has_diagonal(4, 2, player))
        set_rule(world.get_location("Card 4 Horizontal 3", player),
                 lambda state: state._bingo_has_horizontal(4, 3, player))
        set_rule(world.get_location("Card 4 Vertical 3", player),
                 lambda state: state._bingo_has_vertical(4, 3, player))
        set_rule(world.get_location("Card 4 Horizontal 4", player),
                 lambda state: state._bingo_has_horizontal(4, 4, player))
        set_rule(world.get_location("Card 4 Vertical 4", player),
                 lambda state: state._bingo_has_vertical(4, 4, player))
        set_rule(world.get_location("Card 4 Horizontal 5", player),
                 lambda state: state._bingo_has_horizontal(4, 5, player))
        set_rule(world.get_location("Card 4 Vertical 5", player),
             lambda state: state._bingo_has_vertical(4, 5, player))
    if world.card_pairs[player] > 2:
        set_rule(world.get_location("Card 5 Horizontal 1", player),
                 lambda state: state._bingo_has_horizontal(5, 1, player))
        set_rule(world.get_location("Card 5 Vertical 1", player),
                 lambda state: state._bingo_has_vertical(5, 1, player))
        set_rule(world.get_location("Card 5 Diagonal 1", player),
                 lambda state: state._bingo_has_diagonal(5, 1, player))
        set_rule(world.get_location("Card 5 Horizontal 2", player),
                 lambda state: state._bingo_has_horizontal(5, 2, player))
        set_rule(world.get_location("Card 5 Vertical 2", player),
                 lambda state: state._bingo_has_vertical(5, 2, player))
        set_rule(world.get_location("Card 5 Diagonal 2", player),
                 lambda state: state._bingo_has_diagonal(5, 2, player))
        set_rule(world.get_location("Card 5 Horizontal 3", player),
                 lambda state: state._bingo_has_horizontal(5, 3, player))
        set_rule(world.get_location("Card 5 Vertical 3", player),
                 lambda state: state._bingo_has_vertical(5, 3, player))
        set_rule(world.get_location("Card 5 Horizontal 4", player),
                 lambda state: state._bingo_has_horizontal(5, 4, player))
        set_rule(world.get_location("Card 5 Vertical 4", player),
                 lambda state: state._bingo_has_vertical(5, 4, player))
        set_rule(world.get_location("Card 5 Horizontal 5", player),
                 lambda state: state._bingo_has_horizontal(5, 5, player))
        set_rule(world.get_location("Card 5 Vertical 5", player),
                 lambda state: state._bingo_has_vertical(5, 5, player))
        set_rule(world.get_location("Card 6 Horizontal 1", player),
                 lambda state: state._bingo_has_horizontal(6, 1, player))
        set_rule(world.get_location("Card 6 Vertical 1", player),
                 lambda state: state._bingo_has_vertical(6, 1, player))
        set_rule(world.get_location("Card 6 Diagonal 1", player),
                 lambda state: state._bingo_has_diagonal(6, 1, player))
        set_rule(world.get_location("Card 6 Horizontal 2", player),
                 lambda state: state._bingo_has_horizontal(6, 2, player))
        set_rule(world.get_location("Card 6 Vertical 2", player),
                 lambda state: state._bingo_has_vertical(6, 2, player))
        set_rule(world.get_location("Card 6 Diagonal 2", player),
                 lambda state: state._bingo_has_diagonal(6, 2, player))
        set_rule(world.get_location("Card 6 Horizontal 3", player),
                 lambda state: state._bingo_has_horizontal(6, 3, player))
        set_rule(world.get_location("Card 6 Vertical 3", player),
                 lambda state: state._bingo_has_vertical(6, 3, player))
        set_rule(world.get_location("Card 6 Horizontal 4", player),
                 lambda state: state._bingo_has_horizontal(6, 4, player))
        set_rule(world.get_location("Card 6 Vertical 4", player),
                 lambda state: state._bingo_has_vertical(6, 4, player))
        set_rule(world.get_location("Card 6 Horizontal 5", player),
                 lambda state: state._bingo_has_horizontal(6, 5, player))
        set_rule(world.get_location("Card 6 Vertical 5", player),
                 lambda state: state._bingo_has_vertical(6, 5, player))
    if world.card_pairs[player] > 3:
        set_rule(world.get_location("Card 7 Horizontal 1", player),
                 lambda state: state._bingo_has_horizontal(7, 1, player))
        set_rule(world.get_location("Card 7 Vertical 1", player),
                 lambda state: state._bingo_has_vertical(7, 1, player))
        set_rule(world.get_location("Card 7 Diagonal 1", player),
                 lambda state: state._bingo_has_diagonal(7, 1, player))
        set_rule(world.get_location("Card 7 Horizontal 2", player),
                 lambda state: state._bingo_has_horizontal(7, 2, player))
        set_rule(world.get_location("Card 7 Vertical 2", player),
                 lambda state: state._bingo_has_vertical(7, 2, player))
        set_rule(world.get_location("Card 7 Diagonal 2", player),
                 lambda state: state._bingo_has_diagonal(7, 2, player))
        set_rule(world.get_location("Card 7 Horizontal 3", player),
                 lambda state: state._bingo_has_horizontal(7, 3, player))
        set_rule(world.get_location("Card 7 Vertical 3", player),
                 lambda state: state._bingo_has_vertical(7, 3, player))
        set_rule(world.get_location("Card 7 Horizontal 4", player),
                 lambda state: state._bingo_has_horizontal(7, 4, player))
        set_rule(world.get_location("Card 7 Vertical 4", player),
                 lambda state: state._bingo_has_vertical(7, 4, player))
        set_rule(world.get_location("Card 7 Horizontal 5", player),
                 lambda state: state._bingo_has_horizontal(7, 5, player))
        set_rule(world.get_location("Card 7 Vertical 5", player),
                 lambda state: state._bingo_has_vertical(7, 5, player))
        set_rule(world.get_location("Card 8 Horizontal 1", player),
                 lambda state: state._bingo_has_horizontal(8, 1, player))
        set_rule(world.get_location("Card 8 Vertical 1", player),
                 lambda state: state._bingo_has_vertical(8, 1, player))
        set_rule(world.get_location("Card 8 Diagonal 1", player),
                 lambda state: state._bingo_has_diagonal(8, 1, player))
        set_rule(world.get_location("Card 8 Horizontal 2", player),
                 lambda state: state._bingo_has_horizontal(8, 2, player))
        set_rule(world.get_location("Card 8 Vertical 2", player),
                 lambda state: state._bingo_has_vertical(8, 2, player))
        set_rule(world.get_location("Card 8 Diagonal 2", player),
                 lambda state: state._bingo_has_diagonal(8, 2, player))
        set_rule(world.get_location("Card 8 Horizontal 3", player),
                 lambda state: state._bingo_has_horizontal(8, 3, player))
        set_rule(world.get_location("Card 8 Vertical 3", player),
                 lambda state: state._bingo_has_vertical(8, 3, player))
        set_rule(world.get_location("Card 8 Horizontal 4", player),
                 lambda state: state._bingo_has_horizontal(8, 4, player))
        set_rule(world.get_location("Card 8 Vertical 4", player),
                 lambda state: state._bingo_has_vertical(8, 4, player))
        set_rule(world.get_location("Card 8 Horizontal 5", player),
                 lambda state: state._bingo_has_horizontal(8, 5, player))
        set_rule(world.get_location("Card 8 Vertical 5", player),
                 lambda state: state._bingo_has_vertical(8, 5, player))
    set_rule(world.get_location("Completed Cards", player), lambda state: state._bingo_completed(player))