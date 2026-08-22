import random
import unittest

from ..rock_tunnel import (
    bfs_search,
    find_regions,
    objects_1f,
    objects_b1f,
    randomize_rock_tunnel,
    region_names,
    warps_1f,
    warps_b1f,
)


class TestRockTunnelHelpers(unittest.TestCase):
    def test_bfs_search_only_collects_connected_walkable_warps_and_objects(self) -> None:
        layout = [
            [0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1],
            [0, 62, 0, 0, 1],
            [0, 40, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]
        warps = {
            (1, 1): "Start",
            (3, 3): "Connected Exit",
            (4, 1): "Isolated Exit",
        }
        objects = {
            (1, 2): "Reachable Trainer",
            (4, 2): "Isolated Trainer",
        }

        found_warps, found_objects = bfs_search(layout, (1, 1), warps, objects)

        self.assertEqual("Start", found_warps[0])
        self.assertCountEqual(["Connected Exit"], found_warps[1:])
        self.assertCountEqual(["Reachable Trainer"], found_objects)

    def test_find_regions_partitions_each_connected_component(self) -> None:
        layout = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 1, 1, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0, 0],
        ]
        warps = {
            (1, 1): "Left 1",
            (2, 2): "Left 2",
            (4, 1): "Right 1",
            (5, 2): "Right 2",
        }
        objects = {
            (1, 2): "Left Object",
            (5, 1): "Right Object",
        }

        regions = find_regions(layout, warps, objects)
        regions_by_warp_pair = {
            frozenset(region["warps"]): set(region["objects"])
            for region in regions
        }

        self.assertEqual(
            {frozenset({"Left 1", "Left 2"}), frozenset({"Right 1", "Right 2"})},
            set(regions_by_warp_pair),
        )
        self.assertEqual({"Left Object"}, regions_by_warp_pair[frozenset({"Left 1", "Left 2"})])
        self.assertEqual({"Right Object"}, regions_by_warp_pair[frozenset({"Right 1", "Right 2"})])


class TestRockTunnelRandomizer(unittest.TestCase):
    def test_randomizer_returns_complete_region_data_for_many_seeds(self) -> None:
        expected_objects = set(objects_1f.values()) | set(objects_b1f.values())
        expected_warps = set(warps_1f.values()) | set(warps_b1f.values())

        for seed in range(50):
            regions, bytes_1f, bytes_b1f = randomize_rock_tunnel(random.Random(seed))
            seen_objects = set()
            seen_warps = set()

            self.assertEqual(set(region_names), set(regions), seed)
            self.assertEqual(18 * 20, len(bytes_1f), seed)
            self.assertEqual(18 * 20, len(bytes_b1f), seed)

            for region_name in region_names:
                region = regions[region_name]
                self.assertEqual(2, len(region["warps"]), (seed, region_name))
                seen_warps.update(region["warps"])
                seen_objects.update(region["objects"])

            self.assertEqual(expected_warps, seen_warps, seed)
            self.assertEqual(expected_objects, seen_objects, seed)
