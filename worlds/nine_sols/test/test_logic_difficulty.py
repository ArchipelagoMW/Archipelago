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

