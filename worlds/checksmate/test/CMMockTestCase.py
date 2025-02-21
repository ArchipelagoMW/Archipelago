import unittest
import random
from ..Options import (EnableTactics, FairyChessArmy, FairyChessPieces, FairyChessPawns,
                      Difficulty, FairyChessPiecesConfigure)

class CMMockTestCase(unittest.TestCase):
    """Base test case that provides a mock world for unit testing."""
    
    def setUp(self):
        super().setUp()
        self.world = self.create_mock_world()

    def create_mock_world(self):
        """Create a mock world with standard test configuration."""
        class MockWorld:
            def __init__(self):
                self.player = 1
                self.random = random.Random(0)  # Deterministic random for tests
                self.options = type('Options', (), {
                    'accessibility': type('Accessibility', (), {
                        'value': 0, 
                        'option_minimal': 0
                    })(),
                    'max_kings': type('MaxKings', (), {'value': 3})(),
                    'fairy_kings': type('FairyKings', (), {'value': 2})(),
                    'max_engine_penalties': type('MaxEnginePenalties', (), {'value': 5})(),
                    'max_pocket': type('MaxPocket', (), {'value': 12})(),
                    'pocket_limit_by_pocket': type('PocketLimit', (), {'value': 3})(),
                    'enable_tactics': EnableTactics(EnableTactics.option_all),
                    'goal': type('Goal', (), {
                        'value': 0,
                        'option_single': 0,
                        'option_progressive': 1
                    })(),
                    'fairy_chess_army': FairyChessArmy(FairyChessArmy.option_stable),
                    'fairy_chess_pieces': FairyChessPieces(FairyChessPieces.option_fide),
                    'fairy_chess_pieces_configure': FairyChessPiecesConfigure(FairyChessPiecesConfigure.default),
                    'fairy_chess_pawns': FairyChessPawns(FairyChessPawns.option_vanilla),
                    'difficulty': Difficulty(Difficulty.option_daily),
                    'minor_piece_limit_by_type': type('MinorPieceLimitByType', (), {'value': 2})(),
                    'major_piece_limit_by_type': type('MajorPieceLimitByType', (), {'value': 2})(),
                    'queen_piece_limit_by_type': type('QueenPieceLimitByType', (), {'value': 1})(),
                    'queen_piece_limit': type('QueenPieceLimit', (), {'value': 2})()
                })()
                # The above limits to 2 of all except queens, which means:
                # 2 * 2 = 4 minors
                # 2 * 2 + 1 queen upgrade= 5 majors 
                # 2 = 2 queens
                # The queen piece limit is higher than the by type limit, and there is only 1 army, so it has no effect.
                self.piece_types_by_army = {0: {
                    "Progressive Minor Piece": 2,  # Multiplier of 2
                    "Progressive Major Piece": 2,  # Multiplier of 2
                    "Progressive Major To Queen": 2,  # Multiplier of 2
                    "Progressive Queen": 2  # Multiplier of 2
                }}
                # Set up army configuration
                self.armies = {1: [0]}  # Player 1 has access to army 0

            def create_item(self, name):
                """Create a mock item with the given name."""
                return type('CMItem', (), {'name': name})()

            def has_prereqs(self, item_name):
                """Mock implementation that always returns True."""
                return True

        return MockWorld() 