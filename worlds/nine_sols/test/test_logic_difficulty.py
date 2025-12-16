from .bases import NineSolsTestBase


class TestVanillaLogic(NineSolsTestBase):
    options = {
        "logic_difficulty": "vanilla",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        # The earliest location with meaningful medium and LS logic is Over Electrified Floor

        # First, we assert on what it takes to get to lower AFE, since this is mostly unrelated to logic difficulty
        prereq_items = ["Wall Climb", "Grapple"]
        self.assertReachableWith("AF (Elevator): Elevator Shaft", prereq_items)
        # and make sure OEF requires additional items
        self.assertNotReachableWith("AF (Elevator): Over Electrified Floor", prereq_items)

        # Now test the logic on OEF itself. It has two alternatives:
        # 1) just TCK
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Tai-Chi Kick"])
        # 2) both AD AND CL
        self.assertNotReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Air Dash"])
        self.assertNotReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Cloud Leap"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Air Dash", "Cloud Leap"])

    def test_afe_afd_regression(self):
        prereq_items = ["Wall Climb", "Grapple"]
        self.assertRegionReachableWith("AFE - Lower Root Node", prereq_items + ["Air Dash", "Cloud Leap"])
        self.assertRegionReachableWith("AFE - Below Root Node", prereq_items + ["Air Dash", "Cloud Leap"])
        self.assertRegionNotReachableWith("AFE - Lower Left Exit", prereq_items)
        self.assertRegionReachableWith("AFE - Lower Left Exit", prereq_items + ["Air Dash", "Cloud Leap"])
        self.assertNotReachableWith("AF (Depths): Lower Level", prereq_items)
        self.assertReachableWith("AF (Depths): Lower Level", prereq_items + ["Air Dash", "Cloud Leap"])


class TestMediumLogic(NineSolsTestBase):
    options = {
        "logic_difficulty": "medium",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        # Logic difficulty shouldn't affect this part, but double-check that
        prereq_items = ["Wall Climb", "Grapple"]
        self.assertReachableWith("AF (Elevator): Elevator Shaft", prereq_items)
        self.assertNotReachableWith("AF (Elevator): Over Electrified Floor", prereq_items)

        # Vanilla paths still work:
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Tai-Chi Kick"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Air Dash", "Cloud Leap"])

        # Medium logic for OEF itself adds two more paths:
        # 1) bow hover
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Arrow: Cloud Piercer"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Arrow: Thunder Buster"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Arrow: Shadow Hunter"])
        # 2) Swift Runner AND (AD OR CL)  # this will have to change when SR becomes an item
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Air Dash"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Cloud Leap"])

    def test_afe_afd_regression(self):
        prereq_items = ["Wall Climb", "Grapple"]
        self.assertRegionReachableWith("AFE - Lower Root Node", prereq_items + ["Air Dash"])
        self.assertRegionReachableWith("AFE - Below Root Node", prereq_items + ["Air Dash"])
        self.assertRegionNotReachableWith("AFE - Lower Left Exit", prereq_items)
        self.assertRegionReachableWith("AFE - Lower Left Exit", prereq_items + ["Air Dash"])
        self.assertNotReachableWith("AF (Depths): Lower Level", prereq_items)
        self.assertReachableWith("AF (Depths): Lower Level", prereq_items + ["Air Dash"])


class TestLedgeStorageLogic(NineSolsTestBase):
    options = {
        "logic_difficulty": "ledge_storage",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        # Logic difficulty shouldn't affect this part, but double-check that
        prereq_items = ["Wall Climb", "Grapple"]
        self.assertReachableWith("AF (Elevator): Elevator Shaft", prereq_items)
        self.assertNotReachableWith("AF (Elevator): Over Electrified Floor", prereq_items)

        # Vanilla paths still work:
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Tai-Chi Kick"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Air Dash", "Cloud Leap"])

        # Medium paths still work:  # this will have to change when SR becomes an item
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Arrow: Cloud Piercer"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Arrow: Thunder Buster"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Arrow: Shadow Hunter"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Air Dash"])
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Cloud Leap"])

        # Ledge storage logic for OEF itself is parry hover with CL setup:
        self.assertReachableWith("AF (Elevator): Over Electrified Floor", prereq_items + ["Ledge Grab", "Cloud Leap"])


# Test a connection that doesn't even exist on vanilla logic
# I picked the "easy elevator skip" in GoSY because it's the only such connection right next to a first root node
class TestLedgeStorageOnlyConnection(NineSolsTestBase):
    options = {
        "first_root_node": "grotto_of_scriptures_entry",
        "logic_difficulty": "ledge_storage",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertReachableWith("GoS (Entry): Examine Painting", [])

        self.assertNotReachableWith("GoS (Entry): Greenhouse Between Elevators", [])
        self.assertReachableWith("GoS (Entry): Greenhouse Between Elevators", [
            "Arrow: Cloud Piercer",
            "Ledge Grab",
            "Air Dash"
        ])


# Test the one-way barrier break path to FU - Behind Moving Boxes
class TestVanillaFGHLogic(NineSolsTestBase):
    options = {
        "logic_difficulty": "vanilla",
        "first_root_node": "factory_great_hall",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertReachableWith("Factory (U): Near Upper Right Exit", [])
        self.assertNotReachableWith("Factory (U): Behind Moving Boxes", [])

        self.assertNotReachableWith("Factory (U): Behind Moving Boxes", ["Arrow: Thunder Buster"])
        self.assertNotReachableWith("Factory (U): Behind Moving Boxes", [
            "Ledge Grab",
            "Mystic Nymph: Scout Mode",
            "Wall Climb",
        ])
        self.assertNotReachableWith("Factory (U): Behind Moving Boxes", [
            "Air Dash",
            "Mystic Nymph: Scout Mode",
            "Wall Climb",
        ])
        self.assertNotReachableWith("Factory (U): Behind Moving Boxes", [
            "Air Dash",
            "Ledge Grab",
            "Wall Climb",
        ])
        self.assertNotReachableWith("Factory (U): Behind Moving Boxes", [
            "Air Dash",
            "Ledge Grab",
            "Mystic Nymph: Scout Mode",
        ])
        self.assertReachableWith("Factory (U): Behind Moving Boxes", [
            "Air Dash",
            "Ledge Grab",
            "Mystic Nymph: Scout Mode",
            "Wall Climb",
        ])


class TestMediumFGHLogic(NineSolsTestBase):
    options = {
        "logic_difficulty": "medium",
        "first_root_node": "factory_great_hall",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertReachableWith("Factory (U): Near Upper Right Exit", [])
        self.assertNotReachableWith("Factory (U): Behind Moving Boxes", [])

        self.assertReachableWith("Factory (U): Behind Moving Boxes", ["Arrow: Thunder Buster"])


# Test the T-dashing logic around Broken Shanhai
class TestVanillaFULogic(NineSolsTestBase):
    options = {
        "logic_difficulty": "vanilla",
        "first_root_node": "factory_underground",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 2)
        self.assertReachableWith("Factory (MR): Below Right Elevator", [])

        self.assertNotReachableWith("Factory (U): Near Lower Elevator", [])
        self.assertNotReachableWith("Factory (U): Find Broken Shanhai 9000", [])
        self.assertNotReachableWith("Factory (U): Examine Evacuation Notice", [])

        self.assertReachableWith("Factory (U): Near Lower Elevator", ["Air Dash"])
        self.assertReachableWith("Factory (U): Find Broken Shanhai 9000", ["Air Dash"])
        self.assertNotReachableWith("Factory (U): Examine Evacuation Notice", ["Air Dash"])


class TestMediumFULogic(NineSolsTestBase):
    options = {
        "logic_difficulty": "medium",
        "first_root_node": "factory_underground",
        "shuffle_grapple": True,
        "shuffle_wall_climb": True,
        "shuffle_ledge_grab": True,
    }

    def test_default(self):
        self.assertEqual(len(self.multiworld.get_reachable_locations()), 2)
        self.assertReachableWith("Factory (MR): Below Right Elevator", [])

        self.assertNotReachableWith("Factory (U): Near Lower Elevator", [])
        self.assertNotReachableWith("Factory (U): Find Broken Shanhai 9000", [])
        self.assertNotReachableWith("Factory (U): Examine Evacuation Notice", [])

        self.assertReachableWith("Factory (U): Near Lower Elevator", ["Air Dash"])
        self.assertReachableWith("Factory (U): Find Broken Shanhai 9000", ["Air Dash"])
        # this is the medium logic change: combining AD and T-dash lets you cross both hazards
        self.assertReachableWith("Factory (U): Examine Evacuation Notice", ["Air Dash"])
