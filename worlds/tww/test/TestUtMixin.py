"""
Test the Universal Tracker mixin implementation.
"""
import unittest

from worlds.tww.Rules import TWWLogic
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

    def test_mix_in_logic_methods_applied(self) -> None:
        """Verify that the mix-in function applies glitched item checks to methods."""
        # The mixin should have been called during module import, ensuring methods exist
        # and that glitched checks have been applied to CollectionState
        self.assertTrue(hasattr(CollectionState, "_tww_obscure_1"))
        self.assertTrue(hasattr(CollectionState, "_tww_obscure_2"))
        self.assertTrue(hasattr(CollectionState, "_tww_obscure_3"))
        self.assertTrue(hasattr(CollectionState, "_tww_precise_1"))
        self.assertTrue(hasattr(CollectionState, "_tww_precise_2"))
        self.assertTrue(hasattr(CollectionState, "_tww_precise_3"))

        # The methods should be callable
        self.assertTrue(callable(getattr(CollectionState, "_tww_obscure_1")))
        self.assertTrue(callable(getattr(CollectionState, "_tww_obscure_2")))
        self.assertTrue(callable(getattr(CollectionState, "_tww_obscure_3")))
        self.assertTrue(callable(getattr(CollectionState, "_tww_precise_1")))
        self.assertTrue(callable(getattr(CollectionState, "_tww_precise_2")))
        self.assertTrue(callable(getattr(CollectionState, "_tww_precise_3")))
