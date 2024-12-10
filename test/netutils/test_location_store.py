# Tests for _speedups.LocationStore and NetUtils._LocationStore
import os
import typing
import unittest
import warnings
from NetUtils import LocationStore, _LocationStore

State = typing.Dict[typing.Tuple[int, int], typing.Set[int]]
RawLocations = typing.Dict[int, typing.Dict[int, typing.Tuple[int, int, int]]]

ci = bool(os.environ.get("CI"))  # always set in GitHub actions

sample_data: RawLocations = {
    1: {
        11: (21, 2, 7),
        12: (22, 2, 0),
        13: (13, 1, 0),
    },
    2: {
        23: (11, 1, 0),
        22: (12, 1, 0),
        21: (23, 2, 0),
    },
    4: {
        9: (99, 3, 0),
    },
    3: {
        9: (99, 4, 0),
    },
    5: {
        9: (99, 5, 0),
    }
}

empty_state: State = {
    (0, slot): set() for slot in sample_data
}

full_state: State = {
    (0, slot): set(locations) for (slot, locations) in sample_data.items()
}

one_state: State = {
    (0, 1): {12}
}


class Base:
    class TestLocationStore(unittest.TestCase):
        """Test method calls on a loaded store."""
        store: typing.Union[LocationStore, _LocationStore]

        def test_len(self) -> None:
            self.assertEqual(len(self.store), 5)
            self.assertEqual(len(self.store[1]), 3)

        def test_key_error(self) -> None:
            with self.assertRaises(KeyError):
                _ = self.store[0]
            with self.assertRaises(KeyError):
                _ = self.store[6]
            locations = self.store[1]  # no Exception
            with self.assertRaises(KeyError):
                _ = locations[7]
            _ = locations[11]  # no Exception

        def test_getitem(self) -> None:
            self.assertEqual(self.store[1][11], (21, 2, 7))
            self.assertEqual(self.store[1][13], (13, 1, 0))
            self.assertEqual(self.store[2][22], (12, 1, 0))
            self.assertEqual(self.store[4][9], (99, 3, 0))

        def test_get(self) -> None:
            self.assertEqual(self.store.get(1, None), self.store[1])
            self.assertEqual(self.store.get(0, None), None)
            self.assertEqual(self.store[1].get(11, (None, None, None)), self.store[1][11])
            self.assertEqual(self.store[1].get(10, (None, None, None)), (None, None, None))

        def test_iter(self) -> None:
            self.assertEqual(sorted(self.store), [1, 2, 3, 4, 5])
            self.assertEqual(len(self.store), len(sample_data))
            self.assertEqual(list(self.store[1]), [11, 12, 13])
            self.assertEqual(len(self.store[1]), len(sample_data[1]))

        def test_items(self) -> None:
            self.assertEqual(sorted(p for p, _ in self.store.items()), sorted(self.store))
            self.assertEqual(sorted(p for p, _ in self.store[1].items()), sorted(self.store[1]))
            self.assertEqual(sorted(self.store.items())[0][0], 1)
            self.assertEqual(sorted(self.store.items())[0][1], self.store[1])
            self.assertEqual(sorted(self.store[1].items())[0][0], 11)
            self.assertEqual(sorted(self.store[1].items())[0][1], self.store[1][11])

        def test_find_item(self) -> None:
            # empty player set
            self.assertEqual(sorted(self.store.find_item(set(), 99)), [])
            # no such player, single
            self.assertEqual(sorted(self.store.find_item({6}, 99)), [])
            # no such player, set
            self.assertEqual(sorted(self.store.find_item({7, 8, 9}, 99)), [])
            # no such item
            self.assertEqual(sorted(self.store.find_item({3}, 1)), [])
            # valid matches
            self.assertEqual(sorted(self.store.find_item({3}, 99)),
                             [(4, 9, 99, 3, 0)])
            self.assertEqual(sorted(self.store.find_item({3, 4}, 99)),
                             [(3, 9, 99, 4, 0), (4, 9, 99, 3, 0)])
            self.assertEqual(sorted(self.store.find_item({2, 3, 4}, 99)),
                             [(3, 9, 99, 4, 0), (4, 9, 99, 3, 0)])
            # test hash collision in set
            self.assertEqual(sorted(self.store.find_item({3, 5}, 99)),
                             [(4, 9, 99, 3, 0), (5, 9, 99, 5, 0)])
            self.assertEqual(sorted(self.store.find_item(set(range(2048)), 13)),
                             [(1, 13, 13, 1, 0)])

        def test_get_for_player(self) -> None:
            self.assertEqual(self.store.get_for_player(3), {4: {9}})
            self.assertEqual(self.store.get_for_player(1), {1: {13}, 2: {22, 23}})
            self.assertEqual(self.store.get_for_player(9999), {})

        def test_get_checked(self) -> None:
            self.assertEqual(self.store.get_checked(full_state, 0, 1), [11, 12, 13])
            self.assertEqual(self.store.get_checked(one_state, 0, 1), [12])
            self.assertEqual(self.store.get_checked(empty_state, 0, 1), [])
            self.assertEqual(self.store.get_checked(full_state, 0, 3), [9])

        def test_get_checked_exception(self) -> None:
            with self.assertRaises(KeyError):
                self.store.get_checked(empty_state, 0, 9999)
            bad_state = {(0, 6): {1}}
            with self.assertRaises(KeyError):
                self.store.get_checked(bad_state, 0, 6)
            bad_state = {(0, 9999): set()}
            with self.assertRaises(KeyError):
                self.store.get_checked(bad_state, 0, 9999)

        def test_get_missing(self) -> None:
            self.assertEqual(self.store.get_missing(full_state, 0, 1), [])
            self.assertEqual(self.store.get_missing(one_state, 0, 1), [11, 13])
            self.assertEqual(self.store.get_missing(empty_state, 0, 1), [11, 12, 13])
            self.assertEqual(self.store.get_missing(empty_state, 0, 3), [9])

        def test_get_missing_exception(self) -> None:
            with self.assertRaises(KeyError):
                self.store.get_missing(empty_state, 0, 9999)
            bad_state = {(0, 6): {1}}
            with self.assertRaises(KeyError):
                self.store.get_missing(bad_state, 0, 6)
            bad_state = {(0, 9999): set()}
            with self.assertRaises(KeyError):
                self.store.get_missing(bad_state, 0, 9999)

        def test_get_remaining(self) -> None:
            self.assertEqual(self.store.get_remaining(full_state, 0, 1), [])
            self.assertEqual(self.store.get_remaining(one_state, 0, 1), [(1, 13), (2, 21)])
            self.assertEqual(self.store.get_remaining(empty_state, 0, 1), [(1, 13), (2, 21), (2, 22)])
            self.assertEqual(self.store.get_remaining(empty_state, 0, 3), [(4, 99)])

        def test_get_remaining_exception(self) -> None:
            with self.assertRaises(KeyError):
                self.store.get_remaining(empty_state, 0, 9999)
            bad_state = {(0, 6): {1}}
            with self.assertRaises(KeyError):
                self.store.get_missing(bad_state, 0, 6)
            bad_state = {(0, 9999): set()}
            with self.assertRaises(KeyError):
                self.store.get_remaining(bad_state, 0, 9999)

        def test_location_set_intersection(self) -> None:
            locations = {10, 11, 12}
            locations.intersection_update(self.store[1])
            self.assertEqual(locations, {11, 12})

    class TestLocationStoreConstructor(unittest.TestCase):
        """Test constructors for a given store type."""
        type: type

        def test_hole(self) -> None:
            with self.assertRaises(Exception):
                self.type({
                    1: {1: (1, 1, 1)},
                    3: {1: (1, 1, 1)},
                })

        def test_no_slot1(self) -> None:
            with self.assertRaises(Exception):
                self.type({
                    2: {1: (1, 1, 1)},
                    3: {1: (1, 1, 1)},
                })

        def test_slot0(self) -> None:
            with self.assertRaises(ValueError):
                self.type({
                    0: {1: (1, 1, 1)},
                    1: {1: (1, 1, 1)},
                })
            with self.assertRaises(ValueError):
                self.type({
                    0: {1: (1, 1, 1)},
                    2: {1: (1, 1, 1)},
                })

        def test_no_players(self) -> None:
            with self.assertRaises(Exception):
                _ = self.type({})

        def test_no_locations(self) -> None:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                store = self.type({
                    1: {},
                })
                self.assertEqual(len(store), 1)
                self.assertEqual(len(store[1]), 0)
                self.assertEqual(sorted(store.find_item(set(), 1)), [])
                self.assertEqual(sorted(store.find_item({1}, 1)), [])
                self.assertEqual(sorted(store.find_item({1, 2}, 1)), [])
                self.assertEqual(store.get_for_player(1), {})
                self.assertEqual(store.get_checked(empty_state, 0, 1), [])
                self.assertEqual(store.get_checked(full_state, 0, 1), [])
                self.assertEqual(store.get_missing(empty_state, 0, 1), [])
                self.assertEqual(store.get_missing(full_state, 0, 1), [])
                self.assertEqual(store.get_remaining(empty_state, 0, 1), [])
                self.assertEqual(store.get_remaining(full_state, 0, 1), [])

        def test_no_locations_for_1(self) -> None:
            store = self.type({
                1: {},
                2: {1: (1, 2, 3)},
            })
            self.assertEqual(len(store), 2)
            self.assertEqual(len(store[1]), 0)
            self.assertEqual(len(store[2]), 1)

        def test_no_locations_for_last(self) -> None:
            store = self.type({
                1: {1: (1, 2, 3)},
                2: {},
            })
            self.assertEqual(len(store), 2)
            self.assertEqual(len(store[1]), 1)
            self.assertEqual(len(store[2]), 0)


class TestPurePythonLocationStore(Base.TestLocationStore):
    """Run base method tests for pure python implementation."""
    def setUp(self) -> None:
        self.store = _LocationStore(sample_data)
        super().setUp()


class TestPurePythonLocationStoreConstructor(Base.TestLocationStoreConstructor):
    """Run base constructor tests for the pure python implementation."""
    def setUp(self) -> None:
        self.type = _LocationStore
        super().setUp()


@unittest.skipIf(LocationStore is _LocationStore and not ci, "_speedups not available")
class TestSpeedupsLocationStore(Base.TestLocationStore):
    """Run base method tests for cython implementation."""
    def setUp(self) -> None:
        self.assertFalse(LocationStore is _LocationStore, "Failed to load _speedups")
        self.store = LocationStore(sample_data)
        super().setUp()


@unittest.skipIf(LocationStore is _LocationStore and not ci, "_speedups not available")
class TestSpeedupsLocationStoreConstructor(Base.TestLocationStoreConstructor):
    """Run base constructor tests and tests the additional constraints for cython implementation."""
    def setUp(self) -> None:
        self.assertFalse(LocationStore is _LocationStore, "Failed to load _speedups")
        self.type = LocationStore
        super().setUp()

    def test_float_key(self) -> None:
        with self.assertRaises(Exception):
            self.type({
                1: {1: (1, 1, 1)},
                1.1: {1: (1, 1, 1)},
                3: {1: (1, 1, 1)}
            })

    def test_string_key(self) -> None:
        with self.assertRaises(Exception):
            self.type({
                "1": {1: (1, 1, 1)},
            })

    def test_high_player_number(self) -> None:
        with self.assertRaises(Exception):
            self.type({
                1 << 32: {1: (1, 1, 1)},
            })

    def test_not_a_tuple(self) -> None:
        with self.assertRaises(Exception):
            self.type({
                1: {1: None},
            })
