import unittest

from BaseClasses import CollectionState, Region
from Fill import distribute_items_restrictive
from worlds.AutoWorld import call_all
from test.general import generate_test_multiworld, generate_locations, generate_items


class TestSphereFulfillment(unittest.TestCase):
    def _filled_gated_chain(self, players: int) -> "MultiWorld":
        multiworld = generate_test_multiworld(players)
        for pid in multiworld.player_ids:
            menu = multiworld.get_region("Menu", pid)
            inner = Region(f"inner{pid}", pid, multiworld)
            multiworld.regions.append(inner)
            generate_locations(2, pid, menu, None, "_menu")
            generate_locations(1, pid, inner, None, "_inner")
            keys = generate_items(2, pid, advancement=True)
            multiworld.itempool += keys
            multiworld.itempool += generate_items(1, pid, advancement=False)
            key0, key1 = keys[0].name, keys[1].name
            menu.connect(inner, rule=lambda state, p=pid, k=key0: state.has(k, p))
            multiworld.completion_condition[pid] = lambda state, p=pid, k=key1: state.has(k, p)
        distribute_items_restrictive(multiworld)
        call_all(multiworld, "post_fill")
        return multiworld

    def _assert_valid_playthrough(self, multiworld) -> None:
        multiworld.spoiler.create_playthrough_sphere_fulfillment(create_paths=False)
        self.assertTrue(multiworld.spoiler.playthrough, "playthrough should be non-empty")
        state = CollectionState(multiworld)
        for location in multiworld.get_filled_locations():
            if location.item.advancement:
                state.collect(location.item, True, location)
        state.sweep_for_advancements()
        for pid in multiworld.player_ids:
            self.assertTrue(multiworld.has_beaten_game(state, pid), f"player {pid} goal unreachable")

    def test_solo(self) -> None:
        self._assert_valid_playthrough(self._filled_gated_chain(1))

    def test_two_player(self) -> None:
        self._assert_valid_playthrough(self._filled_gated_chain(2))
