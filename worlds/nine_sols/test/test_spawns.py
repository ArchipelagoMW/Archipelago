from .bases import NineSolsTestBase


class TestDefaultSpawn(NineSolsTestBase):
    options = {}

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 12)

        self.assertReachableWith("FSP: Receive Peach Blossom Village Quest", [])
        self.assertReachableWith("AF (Monitoring): Break Corpse", [])


class TestDefaultSpawnAllShuffle(NineSolsTestBase):
    options = {
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 1)

        self.assertReachableWith("FSP: Receive Peach Blossom Village Quest", [])
        self.assertNotReachableWith("AF (Monitoring): Break Corpse", [])  # because shuffle_wall_climb


class TestGDSpawn(NineSolsTestBase):
    options = {
        "first_root_node": "galactic_dock",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 5)

        self.assertReachableWith("Galactic Dock: Examine Sign", [])
        self.assertReachableWith("Galactic Dock: Tianhuo Flower", [])


class TestGDSpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "galactic_dock",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 4)

        self.assertReachableWith("Galactic Dock: Examine Sign", [])
        self.assertNotReachableWith("Galactic Dock: Tianhuo Flower", [])  # because shuffle_grapple


class TestPRESpawn(NineSolsTestBase):
    options = {
        "first_root_node": "power_reservoir_east",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 5)

        self.assertReachableWith("PR (East): After Lasers", [])
        self.assertReachableWith("PR (East): Upper Left Room", [])


class TestPRESpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "power_reservoir_east",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 3)

        self.assertReachableWith("PR (East): After Lasers", [])
        self.assertNotReachableWith("PR (East): Upper Left Room", [])  # because shuffle_grapple


class TestLYRSpawn(NineSolsTestBase):
    options = {
        "first_root_node": "lake_yaochi_ruins",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 7)

        self.assertReachableWith("LYR: Daybreak Tower Chest", [])
        self.assertReachableWith("LYR: Above Leftmost Pool", [])


class TestLYRSpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "lake_yaochi_ruins",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 4)

        self.assertReachableWith("LYR: Daybreak Tower Chest", [])
        self.assertNotReachableWith("LYR: Above Leftmost Pool", [])  # because shuffle_grapple


class TestYCSpawn(NineSolsTestBase):
    options = {
        "first_root_node": "yinglong_canal",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 12)

        self.assertReachableWith("FSP: Receive Peach Blossom Village Quest", [])
        self.assertReachableWith("Yinglong Canal: Near Root Node", [])


class TestYCSpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "yinglong_canal",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 1)

        self.assertReachableWith("FSP: Receive Peach Blossom Village Quest", [])
        self.assertNotReachableWith("Yinglong Canal: Near Root Node", [])  # because shuffle_ledge_grab


class TestFGHSpawn(NineSolsTestBase):
    options = {
        "first_root_node": "factory_great_hall",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 11)

        self.assertReachableWith("Factory (GH): Near Rightmost Shield Orb", [])
        self.assertReachableWith("Factory (MR): Below Right Elevator", [])


class TestFGHSpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "factory_great_hall",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 11)  # the shuffles don't change this

        self.assertReachableWith("Factory (GH): Near Rightmost Shield Orb", [])
        self.assertReachableWith("Factory (MR): Below Right Elevator", [])


class TestOWSpawn(NineSolsTestBase):
    options = {
        "first_root_node": "outer_warehouse",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 16)

        self.assertReachableWith("OW: Above Sol Statue", [])
        self.assertReachableWith("Cortex Center: Near Left Exit", [])


class TestOWSpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "outer_warehouse",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 15)

        self.assertReachableWith("OW: Above Sol Statue", [])
        self.assertReachableWith("Cortex Center: Near Left Exit", [])


class TestGoSYSpawn(NineSolsTestBase):
    options = {
        "first_root_node": "grotto_of_scriptures_entry",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 5)

        self.assertReachableWith("GoS (Entry): Examine Painting", [])
        self.assertReachableWith("GoS (Entry): Examine Coffin", [])


class TestGoSYSpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "grotto_of_scriptures_entry",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 4)

        self.assertReachableWith("GoS (Entry): Examine Painting", [])
        self.assertNotReachableWith("GoS (Entry): Examine Coffin", [])  # because shuffle_ledge_grab


class TestGoSESpawn(NineSolsTestBase):
    options = {
        "first_root_node": "grotto_of_scriptures_east",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 19)

        self.assertReachableWith("GoS (East): Portal Below Root Node", [])
        self.assertReachableWith("GoS (Entry): Lower Left Caves", [])


class TestGoSESpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "grotto_of_scriptures_east",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 14)

        self.assertReachableWith("GoS (East): Portal Below Root Node", [])
        self.assertNotReachableWith("GoS (Entry): Lower Left Caves", [])  # because shuffle_ledge_grab


class TestGoSWSpawn(NineSolsTestBase):
    options = {
        "first_root_node": "grotto_of_scriptures_west",
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 19)

        self.assertReachableWith("GoS (Entry): Near Greenhouse Roof", [])
        self.assertReachableWith("GoS (Entry): Lower Left Caves", [])
        self.assertReachableWith("GoS (East): Portal Below Root Node", [])


class TestGoSWSpawnAllShuffle(NineSolsTestBase):
    options = {
        "first_root_node": "grotto_of_scriptures_west",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_locations(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 11)

        self.assertReachableWith("GoS (Entry): Near Greenhouse Roof", [])
        self.assertNotReachableWith("GoS (Entry): Lower Left Caves", [])  # because shuffle_ledge_grab
        self.assertNotReachableWith("GoS (East): Portal Below Root Node", [])  # because shuffle_wall_climb

