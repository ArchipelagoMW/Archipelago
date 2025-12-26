import typing
import unittest
import warnings

from worlds.AutoWorld import AutoWorldRegister, call_all
from ..bases import MultiworldTestBase as ImportedMultiworldTestBase
from ..param import classvar_matrix


class MultiworldTestBase(ImportedMultiworldTestBase):
    def __init_subclass__(cls, **kwargs: typing.Any) -> None:
        super().__init_subclass__(**kwargs)
        warnings.warn(
            "MultiworldTestBase has been moved to test/bases.py. Please import it from there instead.",
            DeprecationWarning
        )

@unittest.skip("too slow for main")
class TestAllGamesMultiworld(ImportedMultiworldTestBase):
    games = list(AutoWorldRegister.world_types)
    shared_options = {"accessibility": "full"}
    options_per_world = {
        i + 1: {"accessibility": "full"} for i in range(len(AutoWorldRegister.world_types.values()))
    }

    def test_fills(self) -> None:
        """Tests that a multiworld with one of every registered game world can generate."""

        with self.subTest("filling multiworld", seed=self.multiworld.seed):
            from Fill import distribute_items_restrictive

            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
            self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")


@classvar_matrix(games=[[world_type] * 2 for world_type in AutoWorldRegister.world_types])
class TestTwoPlayerMulti(ImportedMultiworldTestBase):
    shared_options = {"accessibility": "full"}

    def test_two_player_single_game_fills(self) -> None:
        """Tests that a multiworld of two players for each registered game world can generate."""
        with self.subTest("filling multiworld", games=self.games, seed=self.multiworld.seed):
            from Fill import distribute_items_restrictive

            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
            self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")
