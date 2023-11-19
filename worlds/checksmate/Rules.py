from functools import reduce

from BaseClasses import MultiWorld, CollectionState

from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule
from .Items import item_table, CMItemData
from .Options import get_option_value


class ChecksMateLogic(LogicMixin):
    flag_goal: int

    def __init__(self, world: MultiWorld, player: int):
        self.flag_goal = get_option_value(world, player, "Goal")

    def owned_items(self: CollectionState, player: int):
        return [(item_id, item) for item_id, item in item_table.items() if self.has(item_id, player)]

    def individual_piece_material(self: CollectionState, item_id: str, item: CMItemData, player: int) -> int:
        val = self.item_count(item_id, player) * item.material
        if item.parents is not None:
            parent_items = [item_id] + [parent_name for parent_name in item.parents]
            val = min(val, min([self.item_count(item_name, player) for item_name in parent_items]) * item.material)

        return val

    def total_piece_material(self: CollectionState, player: int) -> int:
        owned_piece_materials = [
            self.individual_piece_material(item_id, item, player)
            for item_id, item in self.owned_items(player)]
        return reduce(lambda a, b: a + b, owned_piece_materials, 0)

    def has_piece_material(self: CollectionState, player: int, amount: int) -> bool:
        return self.total_piece_material(player) >= amount

    def has_chessmen(self: CollectionState, player: int) -> int:
        return len([item for item in self.owned_items(player) if item in [
            "Progressive Minor Piece", "Progressive Major Piece", "Progressive Pawn"]])

    def count_enemy_pieces(self: CollectionState, player: int) -> int:
        owned_item_ids = [item_id for item_id, item in item_table.items() if self.has(item_id, player)]
        return sum(1 if x.startswith("Enemy Piece") else 0 for x in owned_item_ids)

    def count_enemy_pawns(self: CollectionState, player: int) -> int:
        owned_item_ids = [item_id for item_id, item in item_table.items() if self.has(item_id, player)]
        return sum(1 if x.startswith("Enemy Pawn") else 0 for x in owned_item_ids)

    def has_french_move(self: CollectionState, player: int) -> bool:
        return self.has_pawn(player)  # and self.has("Play En Passant", player)

    def has_pawn(self: CollectionState, player: int) -> bool:
        return self.has_any({"Progressive Pawn"}, player)

    def has_pin(self: CollectionState, player: int) -> bool:
        return self.has_any({"Progressive Minor Piece", "Progressive Major Piece"}, player)

    # TODO(chesslogic): Ensure the current (and next?) sphere have more majors than queens
    def has_castle(self: CollectionState, player: int) -> bool:
        return (self.count("Progressive Major Piece", player) >= 2 + len(
            [item for item in self.multiworld.itempool if
             item.player == player and item.name == "Progressive Major To Queen"]))

    enemy_locations_to_items: dict[str, str] = {
        "Capture Pawn A": "Enemy Pawn A",
        "Capture Pawn B": "Enemy Pawn B",
        "Capture Pawn C": "Enemy Pawn C",
        "Capture Pawn D": "Enemy Pawn D",
        "Capture Pawn E": "Enemy Pawn E",
        "Capture Pawn F": "Enemy Pawn F",
        "Capture Pawn G": "Enemy Pawn G",
        "Capture Pawn H": "Enemy Pawn H",
        "Capture Piece A": "Enemy Piece A",
        "Capture Piece B": "Enemy Piece B",
        "Capture Piece C": "Enemy Piece C",
        "Capture Piece D": "Enemy Piece D",
        "Capture Piece F": "Enemy Piece F",
        "Capture Piece G": "Enemy Piece G",
        "Capture Piece H": "Enemy Piece H",
    }

    def has_enemy(self: CollectionState, location_name: str, player: int) -> bool:
        return self.has(self.enemy_locations_to_items[location_name], player)


def set_rules(multiworld: MultiWorld, player: int):
    # TODO: handle other goals
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

    # suggested material required to
    # a. capture individual pieces
    # b. capture series of pieces and pawns within 1 game
    # c. fork/pin
    capture_expectations = {
        "Capture Pawn A": 190,  # AI prefers not to use edge pawns early - thus they stay defended longer
        "Capture Pawn B": 140,
        "Capture Pawn C": 100,
        "Capture Pawn D": 100,
        "Capture Pawn E": 100,
        "Capture Pawn F": 140,  # AI prefers not to open kingside as developing queen has more tempo
        "Capture Pawn G": 240,
        "Capture Pawn H": 290,  # AI prefers not to use edge pawns early - thus they stay defended longer
        "Capture Piece A": 500,  # rook
        "Capture Piece B": 300,  # knight
        "Capture Piece C": 300,  # bishop
        "Capture Piece D": 900,  # queen
        "Checkmate Maxima": 3920,  # king (this is the game's goal / completion condition)
        "Capture Piece F": 640,  # bishop - AI prefers not to open kingside as developing queen has more tempo
        "Capture Piece G": 640,  # knight - AI prefers not to open kingside as developing queen has more tempo
        "Capture Piece H": 840,  # rook - AI prefers not to open kingside as developing queen has more tempo
        "Capture 2 Pawns": 550,
        "Capture 3 Pawns": 750,
        "Capture 4 Pawns": 940,
        "Capture 5 Pawns": 1120,
        "Capture 6 Pawns": 1275,
        "Capture 7 Pawns": 1425,
        "Capture 8 Pawns": 1575,
        "Capture 2 Pieces": 750,
        "Capture 3 Pieces": 1150,
        "Capture 4 Pieces": 1500,
        "Capture 5 Pieces": 2050,
        "Capture 6 Pieces": 2600,
        "Capture 7 Pieces": 3500,
        "Capture 2 Of Each": 1000,
        "Capture 3 Of Each": 1500,
        "Capture 4 Of Each": 1900,
        "Capture 5 Of Each": 2550,
        "Capture 6 Of Each": 3200,
        "Capture 7 Of Each": 3850,
        "Capture Everything": 3950,
        "Fork, Sacrificial": 700,
        "Fork, True": 2150,
        "Fork, Sacrificial Triple": 1700,
        "Fork, True Triple": 3150,
        "Fork, Sacrificial Royal": 3200,  # AI really hates getting royal forked
        "Fork, True Royal": 4150,  # I sincerely believe this should be filler
        # "Pin": 600,
        # "Skewer": 600,
        "Threaten Queen": 300,
        "Threaten King": 400,
        "Bongcloud Center": 50,
        "Bongcloud A File": 150,
        "Bongcloud Capture": 200,
        "Bongcloud Promotion": 1950,  # requires reaching a rather late-game state
    }
    for piece, material in capture_expectations.items():
        set_rule(multiworld.get_location(piece, player), lambda state, v=material: state.has_piece_material(player, v))

    ###
    # inelegance is malleable
    ###

    # pieces must exist to be captured
    # and player must have (a king plus) that many chessmen to capture any given number of chessmen
    set_rule(multiworld.get_location("Capture 2 Pieces", player),
             lambda state: state.has_chessmen(player) > 0 and state.count_enemy_pieces(player) > 1)
    set_rule(multiworld.get_location("Capture 3 Pieces", player),
             lambda state: state.has_chessmen(player) > 1 and state.count_enemy_pieces(player) > 2)
    set_rule(multiworld.get_location("Capture 4 Pieces", player),
             lambda state: state.has_chessmen(player) > 2 and state.count_enemy_pieces(player) > 3)
    set_rule(multiworld.get_location("Capture 5 Pieces", player),
             lambda state: state.has_chessmen(player) > 3 and state.count_enemy_pieces(player) > 4)
    set_rule(multiworld.get_location("Capture 6 Pieces", player),
             lambda state: state.has_chessmen(player) > 4 and state.count_enemy_pieces(player) > 5)
    set_rule(multiworld.get_location("Capture 7 Pieces", player),
             lambda state: state.has_chessmen(player) > 5 and state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture 2 Pawns", player),
             lambda state: state.has_chessmen(player) > 0 and state.count_enemy_pawns(player) > 1)
    set_rule(multiworld.get_location("Capture 3 Pawns", player),
             lambda state: state.has_chessmen(player) > 1 and state.count_enemy_pawns(player) > 2)
    set_rule(multiworld.get_location("Capture 4 Pawns", player),
             lambda state: state.has_chessmen(player) > 2 and state.count_enemy_pawns(player) > 3)
    set_rule(multiworld.get_location("Capture 5 Pawns", player),
             lambda state: state.has_chessmen(player) > 3 and state.count_enemy_pawns(player) > 4)
    set_rule(multiworld.get_location("Capture 6 Pawns", player),
             lambda state: state.has_chessmen(player) > 4 and state.count_enemy_pawns(player) > 5)
    set_rule(multiworld.get_location("Capture 7 Pawns", player),
             lambda state: state.has_chessmen(player) > 5 and state.count_enemy_pawns(player) > 6)
    set_rule(multiworld.get_location("Capture 8 Pawns", player),
             lambda state: state.has_chessmen(player) > 6 and state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture 2 Of Each", player),
             lambda state: state.has_chessmen(player) > 2 and
                           state.count_enemy_pawns(player) > 1 and state.count_enemy_pieces(player) > 1)
    set_rule(multiworld.get_location("Capture 3 Of Each", player),
             lambda state: state.has_chessmen(player) > 4 and state.count_enemy_pawns(player) > 2
                           and state.count_enemy_pieces(player) > 2)
    set_rule(multiworld.get_location("Capture 4 Of Each", player),
             lambda state: state.has_chessmen(player) > 6 and state.count_enemy_pawns(player) > 3
                           and state.count_enemy_pieces(player) > 3)
    set_rule(multiworld.get_location("Capture 5 Of Each", player),
             lambda state: state.has_chessmen(player) > 8 and state.count_enemy_pawns(player) > 4
                           and state.count_enemy_pieces(player) > 4)
    set_rule(multiworld.get_location("Capture 6 Of Each", player),
             lambda state: state.has_chessmen(player) > 10 and state.count_enemy_pawns(player) > 5
                           and state.count_enemy_pieces(player) > 5)
    set_rule(multiworld.get_location("Capture 7 Of Each", player),
             lambda state: state.has_chessmen(player) > 12 and state.count_enemy_pawns(player) > 6
                           and state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Everything", player),
             lambda state: state.has_chessmen(player) > 13 and state.count_enemy_pawns(player) > 7
                           and state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Piece A", player),
             lambda state: state.has_enemy("Capture Piece A", player))
    set_rule(multiworld.get_location("Capture Piece B", player),
             lambda state: state.has_enemy("Capture Piece B", player))
    set_rule(multiworld.get_location("Capture Piece C", player),
             lambda state: state.has_enemy("Capture Piece C", player))
    set_rule(multiworld.get_location("Capture Piece D", player),
             lambda state: state.has_enemy("Capture Piece D", player))
    set_rule(multiworld.get_location("Capture Piece F", player),
             lambda state: state.has_enemy("Capture Piece F", player))
    set_rule(multiworld.get_location("Capture Piece G", player),
             lambda state: state.has_enemy("Capture Piece G", player))
    set_rule(multiworld.get_location("Capture Piece H", player),
             lambda state: state.has_enemy("Capture Piece H", player))
    set_rule(multiworld.get_location("Capture Pawn A", player),
             lambda state: state.has_enemy("Capture Pawn A", player))
    set_rule(multiworld.get_location("Capture Pawn B", player),
             lambda state: state.has_enemy("Capture Pawn B", player))
    set_rule(multiworld.get_location("Capture Pawn C", player),
             lambda state: state.has_enemy("Capture Pawn C", player))
    set_rule(multiworld.get_location("Capture Pawn D", player),
             lambda state: state.has_enemy("Capture Pawn D", player))
    set_rule(multiworld.get_location("Capture Pawn E", player),
             lambda state: state.has_enemy("Capture Pawn E", player))
    set_rule(multiworld.get_location("Capture Pawn F", player),
             lambda state: state.has_enemy("Capture Pawn F", player))
    set_rule(multiworld.get_location("Capture Pawn G", player),
             lambda state: state.has_enemy("Capture Pawn G", player))
    set_rule(multiworld.get_location("Capture Pawn H", player),
             lambda state: state.has_enemy("Capture Pawn H", player))
    # tactics
    # set_rule(multiworld.get_location("Pin", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Fork, Sacrificial", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Fork, True", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Fork, Sacrificial Triple", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Fork, True Triple", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Fork, Sacrificial Royal", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Fork, True Royal", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Threaten Pawn", player), lambda state: state.count_enemy_pawns(player) > 0)
    set_rule(multiworld.get_location("Threaten Minor", player), lambda state: state.count_enemy_pieces(player) > 3)
    set_rule(multiworld.get_location("Threaten Major", player), lambda state: state.count_enemy_pieces(player) > 5)
    set_rule(multiworld.get_location("Threaten Queen", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Threaten King", player), lambda state: state.has_pin(player))
    # special moves
    set_rule(multiworld.get_location("O-O Castle", player), lambda state: state.has_castle(player))
    set_rule(multiworld.get_location("O-O-O Castle", player), lambda state: state.has_castle(player))
    # set_rule(multiworld.get_location("French Move", player), lambda state: state.has_french_move(player))

    # goal materials
    # set_rule(multiworld.get_location("Checkmate Minima", player), lambda state: state.has_piece_material(player, 2))
    # set_rule(multiworld.get_location("Checkmate One Piece", player), lambda state: state.has_piece_material(player, 5))
    # set_rule(multiworld.get_location("Checkmate 2 Pieces", player), lambda state: state.has_piece_material(player, 9))
    # set_rule(multiworld.get_location("Checkmate 3 Pieces", player), lambda state: state.has_piece_material(player, 13))
    # set_rule(multiworld.get_location("Checkmate 4 Pieces", player), lambda state: state.has_piece_material(player, 18))
    # set_rule(multiworld.get_location("Checkmate 5 Pieces", player), lambda state: state.has_piece_material(player, 20))
    # set_rule(multiworld.get_location("Checkmate 6 Pieces", player), lambda state: state.has_piece_material(player, 22))
    # set_rule(multiworld.get_location("Checkmate 7 Pieces", player), lambda state: state.has_piece_material(player, 24))
    # set_rule(multiworld.get_location("Checkmate 8 Pieces", player), lambda state: state.has_piece_material(player, 26))
    # set_rule(multiworld.get_location("Checkmate 9 Pieces", player), lambda state: state.has_piece_material(player, 28))
    # set_rule(multiworld.get_location("Checkmate 10 Pieces", player), lambda state: state.has_piece_material(player, 30))
    # set_rule(multiworld.get_location("Checkmate 11 Pieces", player), lambda state: state.has_piece_material(player, 32))
    # set_rule(multiworld.get_location("Checkmate 12 Pieces", player), lambda state: state.has_piece_material(player, 34))
    # set_rule(multiworld.get_location("Checkmate 13 Pieces", player), lambda state: state.has_piece_material(player, 36))
    # set_rule(multiworld.get_location("Checkmate 14 Pieces", player), lambda state: state.has_piece_material(player, 38))
