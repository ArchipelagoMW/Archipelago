# Tests for _speedups.LocationStore and NetUtils._LocationStore
import typing
import unittest
from NetUtils import LocationStore, _LocationStore


sample_data = {
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
}

empty_state = {
    (0, slot): set() for slot in sample_data
}

full_state = {
    (0, slot): set(locations) for (slot, locations) in sample_data.items()
}

one_state = {
    (0, 1): {12}
}


class Base:
    class TestLocationStore(unittest.TestCase):
        store: typing.Union[LocationStore, _LocationStore]

        def test_len(self):
            self.assertEqual(len(self.store), 4)
            self.assertEqual(len(self.store[1]), 3)

        def test_key_error(self):
            with self.assertRaises(KeyError):
                _ = self.store[0]
            with self.assertRaises(KeyError):
                _ = self.store[5]
            locations = self.store[1]  # no Exception
            with self.assertRaises(KeyError):
                _ = locations[7]
            _ = locations[11]  # no Exception

        def test_getitem(self):
            self.assertEqual(self.store[1][11], (21, 2, 7))
            self.assertEqual(self.store[1][13], (13, 1, 0))
            self.assertEqual(self.store[2][22], (12, 1, 0))
            self.assertEqual(self.store[4][9], (99, 3, 0))

        def test_get(self):
            self.assertEqual(self.store.get(1, None), self.store[1])
            self.assertEqual(self.store.get(0, None), None)
            self.assertEqual(self.store[1].get(11, (None, None, None)), self.store[1][11])
            self.assertEqual(self.store[1].get(10, (None, None, None)), (None, None, None))

        def test_iter(self):
            self.assertEqual(sorted(self.store), [1, 2, 3, 4])
            self.assertEqual(len(self.store), len(sample_data))
            self.assertEqual(list(self.store[1]), [11, 12, 13])
            self.assertEqual(len(self.store[1]), len(sample_data[1]))

        def test_items(self):
            self.assertEqual(sorted(p for p, _ in self.store.items()), sorted(self.store))
            self.assertEqual(sorted(p for p, _ in self.store[1].items()), sorted(self.store[1]))
            self.assertEqual(sorted(self.store.items())[0][0], 1)
            self.assertEqual(sorted(self.store.items())[0][1], self.store[1])
            self.assertEqual(sorted(self.store[1].items())[0][0], 11)
            self.assertEqual(sorted(self.store[1].items())[0][1], self.store[1][11])

        def test_find_item(self):
            self.assertEqual(sorted(self.store.find_item({}, 99)), [])
            self.assertEqual(sorted(self.store.find_item({3}, 1)), [])
            self.assertEqual(sorted(self.store.find_item({5}, 99)), [])
            self.assertEqual(sorted(self.store.find_item({3}, 99)),
                             [(4, 9, 99, 3, 0)])
            self.assertEqual(sorted(self.store.find_item({3, 4}, 99)),
                             [(3, 9, 99, 4, 0), (4, 9, 99, 3, 0)])

        def test_get_for_player(self):
            self.assertEqual(self.store.get_for_player(3), {4: {9}})
            self.assertEqual(self.store.get_for_player(1), {1: {13}, 2: {22, 23}})

        def get_checked(self):
            self.assertEqual(self.store.get_checked(full_state, 0, 1), [11, 12, 13])
            self.assertEqual(self.store.get_checked(one_state, 0, 1), [12])
            self.assertEqual(self.store.get_checked(empty_state, 0, 1), [])
            self.assertEqual(self.store.get_checked(full_state, 0, 3), [9])

        def get_missing(self):
            self.assertEqual(self.store.get_missing(full_state, 0, 1), [])
            self.assertEqual(self.store.get_missing(one_state, 0, 1), [11, 13])
            self.assertEqual(self.store.get_missing(empty_state, 0, 1), [11, 12, 13])
            self.assertEqual(self.store.get_missing(empty_state, 0, 3), [9])

        def get_remaining(self):
            self.assertEqual(self.store.get_remaining(full_state, 0, 1), [])
            self.assertEqual(self.store.get_remaining(one_state, 0, 1), [13, 21])
            self.assertEqual(self.store.get_remaining(empty_state, 0, 1), [13, 21, 22])
            self.assertEqual(self.store.get_remaining(empty_state, 0, 3), [99])


class TestPurePythonLocationStore(Base.TestLocationStore):
    def setUp(self) -> None:
        self.store = _LocationStore(sample_data)
        super().setUp()


@unittest.skipIf(LocationStore is _LocationStore, "_speedups not available")
class TestSpeedupsLocationStore(Base.TestLocationStore):
    def setUp(self) -> None:
        self.store = LocationStore(sample_data)
        super().setUp()


@unittest.skipIf(LocationStore is _LocationStore, "_speedups not available")
class TestSpeedupsLocationStoreConstructor(unittest.TestCase):
    def test_init_float_key(self):
        with self.assertRaises(Exception):
            LocationStore({
                1: {1: (1, 1, 1)},
                1.1: {1: (1, 1, 1)},
                3: {1: (1, 1, 1)}
            })

    def test_init_string_key(self):
        with self.assertRaises(Exception):
            LocationStore({
                "1": {1: (1, 1, 1)},
            })

    def test_init_hole(self):
        with self.assertRaises(Exception):
            LocationStore({
                1: {1: (1, 1, 1)},
                3: {1: (1, 1, 1)},
            })

    def test_init_slot0(self):
        with self.assertRaises(Exception):
            LocationStore({
                0: {1: (1, 1, 1)},
                1: {1: (1, 1, 1)},
            })
        with self.assertRaises(Exception):
            LocationStore({
                0: {1: (1, 1, 1)},
                2: {1: (1, 1, 1)},
            })
