"""
Test the Universal Tracker mixin implementation.
"""
import unittest

from worlds.tww.Rules import TWWLogic, mix_in_universal_tracker_logic
from BaseClasses import CollectionState

class TestUniversalTrackerMixin(unittest.TestCase):
    """Test that the mix_in_universal_tracker_logic function works correctly."""

    def test_mix_in_logic_methods_exist(self) -> None:
        """Verify that the methods exist on TWWLogic before mixing in."""
        self.assertTrue(hasattr(TWWLogic, "_tww_obscure_1"))
        self.assertTrue(hasattr(TWWLogic, "_tww_obscure_2"))
        self.assertTrue(hasattr(TWWLogic, "_tww_obscure_3"))
        self.assertTrue(hasattr(TWWLogic, "_tww_precise_1"))
        self.assertTrue(hasattr(TWWLogic, "_tww_precise_2"))
        self.assertTrue(hasattr(TWWLogic, "_tww_precise_3"))

    def test_mix_in_logic_replaces_methods(self) -> None:
        """Verify that the mix-in function replaces methods on CollectionState."""
        # Store original methods
        original_obscure_1 = CollectionState._tww_obscure_1
        original_obscure_2 = CollectionState._tww_obscure_2
        original_obscure_3 = CollectionState._tww_obscure_3
        original_precise_1 = CollectionState._tww_precise_1
        original_precise_2 = CollectionState._tww_precise_2
        original_precise_3 = CollectionState._tww_precise_3

        # Call the mix-in function
        mix_in_universal_tracker_logic()

        # Verify that the methods have been replaced
        self.assertIsNot(CollectionState._tww_obscure_1, original_obscure_1)
        self.assertIsNot(CollectionState._tww_obscure_2, original_obscure_2)
        self.assertIsNot(CollectionState._tww_obscure_3, original_obscure_3)
        self.assertIsNot(CollectionState._tww_precise_1, original_precise_1)
        self.assertIsNot(CollectionState._tww_precise_2, original_precise_2)
        self.assertIsNot(CollectionState._tww_precise_3, original_precise_3)
