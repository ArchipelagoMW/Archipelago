import unittest
from typing import List, Tuple
from unittest import TestCase

from BaseClasses import CollectionState, Location, MultiWorld
from Fill import distribute_items_restrictive
from Options import Accessibility
from worlds.AutoWorld import AutoWorldRegister, call_all, call_single
from ..general import gen_steps, setup_multiworld


class MultiworldTestBase(TestCase):
    multiworld: MultiWorld

    # similar to the implementation in WorldTestBase.test_fill
    # but for multiple players and doesn't allow minimal accessibility
    def fulfills_accessibility(self) -> bool:
        """
        Checks that the multiworld satisfies locations accessibility requirements, failing if all locations are cleared
        but not beatable, or some locations are unreachable.
        """
        locations = [loc for loc in self.multiworld.get_locations()]
        state = CollectionState(self.multiworld)
        while locations:
            sphere: List[Location] = []
            for n in range(len(locations) - 1, -1, -1):
                if locations[n].can_reach(state):
                    sphere.append(locations.pop(n))
            self.assertTrue(sphere, f"Unreachable locations: {locations}")
            if not sphere:
                return False
            for location in sphere:
                if location.item:
                    state.collect(location.item, True, location)
        return self.multiworld.has_beaten_game(state, 1)

    def assertSteps(self, steps: Tuple[str, ...]) -> None:
        """Calls each step individually, continuing if a step for a specific world step fails."""
        world_types = {world.__class__ for world in self.multiworld.worlds.values()}
        for step in steps:
            for player, world in self.multiworld.worlds.items():
                with self.subTest(game=world.game, step=step):
                    call_single(self.multiworld, step, player)
            for world_type in sorted(world_types, key=lambda world: world.__name__):
                with self.subTest(game=world_type.game, step=f"stage_{step}"):
                    stage_callable = getattr(world_type, f"stage_{step}", None)
                    if stage_callable:
                        stage_callable(self.multiworld)


@unittest.skip("too slow for main")
class TestAllGamesMultiworld(MultiworldTestBase):
    def test_fills(self) -> None:
        """Tests that a multiworld with one of every registered game world can generate."""
        all_worlds = list(AutoWorldRegister.world_types.values())
        self.multiworld = setup_multiworld(all_worlds, ())
        for world in self.multiworld.worlds.values():
            world.options.accessibility.value = Accessibility.option_full
        self.assertSteps(gen_steps)
        with self.subTest("filling multiworld", seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
            self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")


class TestTwoPlayerMulti(MultiworldTestBase):
    def test_two_player_single_game_fills(self) -> None:
        """Tests that a multiworld of two players for each registered game world can generate."""
        for world_type in AutoWorldRegister.world_types.values():
            self.multiworld = setup_multiworld([world_type, world_type], ())
            for world in self.multiworld.worlds.values():
                world.options.accessibility.value = Accessibility.option_full
            self.assertSteps(gen_steps)
            with self.subTest("filling multiworld", games=world_type.game, seed=self.multiworld.seed):
                distribute_items_restrictive(self.multiworld)
                call_all(self.multiworld, "post_fill")
                self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")
