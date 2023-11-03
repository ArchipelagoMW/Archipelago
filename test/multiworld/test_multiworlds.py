from typing import List, Tuple
from unittest import TestCase

from BaseClasses import CollectionState, Location, MultiWorld
from Fill import distribute_items_restrictive
from worlds.AutoWorld import AutoWorldRegister, call_all, call_single
from worlds.alttp import ALTTPWorld
from ..general import gen_steps, setup_multiworld


class MultiworldTestBase(TestCase):
    multiworld: MultiWorld

    # similar to the implementation in WorldTestBase.test_fill
    # but for multiple players and doesn't allow minimal accessibility
    def fulfills_accessibility(self) -> bool:
        locations = self.multiworld.get_locations().copy()
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
        world_types = set(self.multiworld.worlds.values())
        for step in steps:
            for player in self.multiworld.worlds:
                with self.subTest(step):
                    call_single(self.multiworld, step, player)
            for world_type in sorted(world_types, key=lambda world: world.__name__):
                with self.subTest(f"stage_{step}"):
                    stage_callable = getattr(world_type, f"stage_{step}", None)
                    if stage_callable:
                        stage_callable(self.multiworld)


class TestAllGamesMultiworld(MultiworldTestBase):
    multiworld: MultiWorld

    def test_fills(self) -> None:
        all_worlds = list(AutoWorldRegister.world_types.values())
        all_worlds.remove(ALTTPWorld)
        self.multiworld = setup_multiworld(all_worlds, ())
        self.assertSteps(gen_steps)
        with self.subTest("filling multiworld", seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
            self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")


class TestTwoPlayerMulti(MultiworldTestBase):
    def test_two_player_single_game_fills(self) -> None:
        for game, world in AutoWorldRegister.world_types.items():
            if world is ALTTPWorld:
                continue
            worlds = [world] * 2
            self.multiworld = setup_multiworld(worlds, ())
            self.assertSteps(gen_steps)
        with self.subTest("filling multiworld", seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
            self.assertTrue(self.fulfills_accessibility(), "Collected all locations, but can't beat the game")
