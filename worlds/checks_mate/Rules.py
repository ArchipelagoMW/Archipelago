from functools import reduce

from BaseClasses import MultiWorld, CollectionState

from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule
from .Items import item_table, CMItemData


class ChecksMateLogic(LogicMixin):
    def individual_piece_material(self, item_id: str, item: CMItemData, player: int) -> int:
        val = self.item_count(item_id, player) * item.material
        if item.parents is not None:
            parent_items = [item_id] + [parent_name for parent_name in item.parents]
            val = min([self.item_count(item_name, player) for item_name in parent_items]) * item.material

        return val

    def total_piece_material(self: CollectionState, player: int) -> int:
        owned_items = [
            (item_id, item)
            for item_id, item in item_table.items() if self.has(item_id, player)]
        owned_piece_materials = [
            self.individual_piece_material(item_id, item, player)
            for item_id, item in owned_items]
        return reduce(lambda a, b: a + b, owned_piece_materials, 0)
        
    def has_piece_material(self: CollectionState, player: int, amount: int) -> bool:
        return self.total_piece_material(player) >= amount
        
    def count_enemy_pieces(self: CollectionState, player: int) -> int:
        owned_item_ids = [item_id for item_id, item in item_table.items() if self.has(item_id, player)]
        return sum(1 if x == "Progressive Enemy Piece" else 0 for x in owned_item_ids)
        
    def count_enemy_pawns(self: CollectionState, player: int) -> int:
        owned_item_ids = [item_id for item_id, item in item_table.items() if self.has(item_id, player)]
        return sum(1 if x == "Progressive Enemy Piece" else 0 for x in owned_item_ids)
        
    def has_french_move(self: CollectionState, player: int) -> bool:
        return self.has("Play En Passant", player) and self.has_pawn()

    def has_pawn(self: CollectionState, player: int) -> bool:
        return self.has_any({"Progressive Pawn"}, player)

    def has_pin(self: CollectionState, player: int) -> bool:
        return self.has_any({"Progressive Minor Piece", "Progressive Major Piece", "Progressive Pocket Piece"}, player)

    def has_castle(self: CollectionState, player: int) -> bool:
        return self.has_any({"Progressive Major Piece"}, player)


def set_rules(multiworld: MultiWorld, player: int):

    # suggested material required to
    # a. capture individual pieces
    # b. capture series of pieces and pawns within 1 game
    # c. fork/pin
    capture_expectations = {
        "Capture Piece A": 500, # rook
        "Capture Piece H": 500, # rook
        "Capture Piece B": 300, # knight
        "Capture Piece G": 300, # knight
        "Capture Piece C": 300, # bishop
        "Capture Piece F": 300, # bishop
        "Capture Piece D": 900, # queen
        "Capture 2 Pawns": 150,
        "Capture 3 Pawns": 250,
        "Capture 4 Pawns": 360,
        "Capture 5 Pawns": 490,
        "Capture 6 Pawns": 625,
        "Capture 7 Pawns": 735,
        "Capture 8 Pawns": 850,
        "Capture 2 Pieces": 700,
        "Capture 3 Pieces": 1100,
        "Capture 4 Pieces": 1500,
        "Capture 5 Pieces": 1900,
        "Capture 6 Pieces": 2300,
        "Capture 7 Pieces": 3050,
        "Fork": 500,
        "Royal Fork": 1400,
        "Pin": 450,
        "Bongcloud Center": 100,
        "Bongcloud A File": 150,
        "Bongcloud Capture": 50,
        "Bongcloud Promotion": 1450,
    }
    for piece, material in capture_expectations.items():
        set_rule(multiworld.get_location(piece, player), lambda state, v=material: state.has_piece_material(player, v))

    # piece must exist to be captured
    set_rule(multiworld.get_location("Capture 2 Pieces", player), lambda state: state.count_enemy_pieces(player) > 1)
    set_rule(multiworld.get_location("Capture 3 Pieces", player), lambda state: state.count_enemy_pieces(player) > 2)
    set_rule(multiworld.get_location("Capture 4 Pieces", player), lambda state: state.count_enemy_pieces(player) > 3)
    set_rule(multiworld.get_location("Capture 5 Pieces", player), lambda state: state.count_enemy_pieces(player) > 4)
    set_rule(multiworld.get_location("Capture 6 Pieces", player), lambda state: state.count_enemy_pieces(player) > 5)
    set_rule(multiworld.get_location("Capture 7 Pieces", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture 2 Pawns", player), lambda state: state.count_enemy_pawns(player) > 1)
    set_rule(multiworld.get_location("Capture 3 Pawns", player), lambda state: state.count_enemy_pawns(player) > 2)
    set_rule(multiworld.get_location("Capture 4 Pawns", player), lambda state: state.count_enemy_pawns(player) > 3)
    set_rule(multiworld.get_location("Capture 5 Pawns", player), lambda state: state.count_enemy_pawns(player) > 4)
    set_rule(multiworld.get_location("Capture 6 Pawns", player), lambda state: state.count_enemy_pawns(player) > 5)
    set_rule(multiworld.get_location("Capture 7 Pawns", player), lambda state: state.count_enemy_pawns(player) > 6)
    set_rule(multiworld.get_location("Capture 8 Pawns", player), lambda state: state.count_enemy_pawns(player) > 7)
    # ensure all pieces exist before requiring any (this is the easiest logic break ever)
    # TODO: I have no idea what I'm doing
    set_rule(multiworld.get_location("Capture Piece A", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Piece B", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Piece C", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Piece D", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Piece F", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Piece G", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Piece H", player), lambda state: state.count_enemy_pieces(player) > 6)
    set_rule(multiworld.get_location("Capture Pawn A", player), lambda state: state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture Pawn B", player), lambda state: state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture Pawn C", player), lambda state: state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture Pawn D", player), lambda state: state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture Pawn E", player), lambda state: state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture Pawn F", player), lambda state: state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture Pawn G", player), lambda state: state.count_enemy_pawns(player) > 7)
    set_rule(multiworld.get_location("Capture Pawn H", player), lambda state: state.count_enemy_pawns(player) > 7)
    # tactics
    set_rule(multiworld.get_location("Pin", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Fork", player), lambda state: state.has_pin(player))
    set_rule(multiworld.get_location("Royal Fork", player), lambda state: state.has_pin(player))
    # special moves
    # set_rule(multiworld.get_location("00 Castle", player), lambda state: state.has_castle(player))
    # set_rule(multiworld.get_location("000 Castle", player), lambda state: state.has_castle(player))
    set_rule(multiworld.get_location("French Move", player), lambda state: state.has_french_move(player))
    # goal materials
    set_rule(multiworld.get_location("Checkmate Minima", player), lambda state: state.has_piece_material(player, 2))
    set_rule(multiworld.get_location("Checkmate One Piece", player), lambda state: state.has_piece_material(player, 5))
    set_rule(multiworld.get_location("Checkmate 2 Pieces", player), lambda state: state.has_piece_material(player, 9))
    set_rule(multiworld.get_location("Checkmate 3 Pieces", player), lambda state: state.has_piece_material(player, 13))
    set_rule(multiworld.get_location("Checkmate 4 Pieces", player), lambda state: state.has_piece_material(player, 18))
    set_rule(multiworld.get_location("Checkmate 5 Pieces", player), lambda state: state.has_piece_material(player, 20))
    set_rule(multiworld.get_location("Checkmate 6 Pieces", player), lambda state: state.has_piece_material(player, 22))
    set_rule(multiworld.get_location("Checkmate 7 Pieces", player), lambda state: state.has_piece_material(player, 24))
    set_rule(multiworld.get_location("Checkmate 8 Pieces", player), lambda state: state.has_piece_material(player, 26))
    set_rule(multiworld.get_location("Checkmate 9 Pieces", player), lambda state: state.has_piece_material(player, 28))
    set_rule(multiworld.get_location("Checkmate 10 Pieces", player), lambda state: state.has_piece_material(player, 30))
    set_rule(multiworld.get_location("Checkmate 11 Pieces", player), lambda state: state.has_piece_material(player, 32))
    set_rule(multiworld.get_location("Checkmate 12 Pieces", player), lambda state: state.has_piece_material(player, 34))
    set_rule(multiworld.get_location("Checkmate 13 Pieces", player), lambda state: state.has_piece_material(player, 36))
    set_rule(multiworld.get_location("Checkmate 14 Pieces", player), lambda state: state.has_piece_material(player, 38))
    set_rule(multiworld.get_location("Checkmate Maxima", player), lambda state: state.has_piece_material(player, 40))


