from ..options import Goal

from .bases import OuterWildsTestBase


class TestDefaultWorld(OuterWildsTestBase):
    options = {}

    def test_default_world(self):
        self.assertEqual(self.getLocationCount(), 89)  # default locations, including 2 Victory events

        # with default locations, Insulation only blocks 2 checks
        self.assertAccessDependency(
            ["GD: Enter the Core", "GD: See the Coordinates"],
            [["Electrical Insulation"]]
        )

        self.assertEverywhereRequiringAllOf(
            ["Ruptured Core (Text Wheel)"],
            ["Launch Codes", "Scout", "Ghost Matter Wavelength", "Translator"]
        )

        # logsanity locations don't exist, so trying to access one raises
        self.assertRaises(KeyError, lambda: self.multiworld.get_location("Ship Log: Village 1 - Identify", 1))

        # Feldspar's Camp is one of the few places with two different "logical paths", so check that both are in-logic
        self.assertNotReachableWith("DB: Feldspar's Camp Fuel Tank", ["Silent Running Mode"])
        self.assertNotReachableWith("DB: Feldspar's Camp Fuel Tank", ["Silent Running Mode", "Signalscope"])
        self.assertReachableWith("DB: Feldspar's Camp Fuel Tank", [
            "Silent Running Mode", "Signalscope", "Feldspar's Signal"
        ])
        self.assertReachableWith("DB: Feldspar's Camp Fuel Tank", [
            "Silent Running Mode", "Scout"
        ])

        # On default options, these are the only two goals, and the only locations requiring coordinates
        self.assertAccessDependency(
            ["Victory - Song of Five", "Victory - Song of the Nomai"],
            [["Coordinates"]]
        )

        self.assertRequiresAllOf("Victory - Song of Five", self.song_of_five_required_items)

        self.assertNotReachableWith("Victory - Song of the Nomai", self.song_of_five_required_items)

        self.assertRequiresAllOf("Victory - Song of the Nomai",
                                 self.song_of_five_required_items + self.song_of_the_nomai_additional_required_items)


class TestSplitTranslator(OuterWildsTestBase):
    options = {
        "split_translator": True
    }

    def test_split_translator(self):
        self.assertReachableWith("ET: High Energy Lab (Upper Text Wall)", [
            "Launch Codes", "Translator (Hourglass Twins)"
        ])
        self.assertReachableWith("TH: Mines (Text Wall)", [
            "Launch Codes", "Translator (Timber Hearth)"
        ])
        self.assertReachableWith("BH: Southern Observatory (Tornado Text Wall)", [
            "Launch Codes", "Translator (Brittle Hollow)"
        ])
        self.assertReachableWith("GD: Control Module Logs (Text Wheels)", [
            "Launch Codes", "Translator (Giant's Deep)"
        ])
        self.assertReachableWith("DB: Nomai Grave (Text Wheel)", [
            "Launch Codes", "Silent Running Mode", "Signalscope", "Distress Beacon Frequency", "Escape Pod 3 Signal", "Translator (Dark Bramble)"
        ])
        self.assertReachableWith("Ruptured Core (Text Wheel)", [
            "Launch Codes", "Scout", "Ghost Matter Wavelength", "Translator (Other)"
        ])


class TestSongOfNomaiWorld(OuterWildsTestBase):
    options = {
        "goal": Goal.option_song_of_the_nomai
    }

    def test_six_world(self):
        self.assertEqual(self.getLocationCount(), 89)  # same as song of five

        # same as song of five
        self.assertAccessDependency(
            ["GD: Enter the Core", "GD: See the Coordinates"],
            [["Electrical Insulation"]]
        )


class TestLogsanityWorld(OuterWildsTestBase):
    options = {
        "logsanity": "true"
    }

    def test_logsanity_world(self):
        self.assertEqual(self.getLocationCount(), 265)  # 87(+2V) default + 176 logsanity locations

        # make sure the logsanity locations exist; this one requires nothing to reach
        self.assertReachableWith("TH Ship Log: Village 1 - Identify", [])

        # and some of those new locations are Insulation-gated
        self.assertAccessDependency(
            [
                "GD: Enter the Core", "GD: See the Coordinates",
                "GD Ship Log: Ocean Depths 2 - Coral Forest",
                "GD Ship Log: Probe Tracking Module 1 - Millions",
                "GD Ship Log: Probe Tracking Module 2 - Anomaly Located",
                "GD Ship Log: Probe Tracking Module 3 - Statue",
                "GD Ship Log: Probe Tracking Module 4 - Coordinates"
            ],
            [["Electrical Insulation"]]
        )

        self.assertNotReachableWith("GD: Enter the Core", [])
        self.assertNotReachableWith("GD: Enter the Core", ["Tornado Aerodynamic Adjustments"])
        self.assertNotReachableWith("GD: Enter the Core", ["Electrical Insulation"])
        self.assertReachableWith("GD: Enter the Core", [
            "Tornado Aerodynamic Adjustments", "Electrical Insulation"
        ])

        self.assertNotReachableWith("GD Ship Log: Bramble Island", [])
        self.assertReachableWith("GD Ship Log: Bramble Island", ["Ghost Matter Wavelength"])

        self.assertNotReachableWith("GD: Bramble Island Recorder", [])
        self.assertReachableWith("GD: Bramble Island Recorder", ["Ghost Matter Wavelength"])

        self.assertNotReachableWith("GD: Bramble Island Fuel Tank", [])
        self.assertReachableWith("GD: Bramble Island Fuel Tank", ["Ghost Matter Wavelength"])


class TestSuitlessWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true"
    }


class TestSuitlessSongOfNomaiWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true",
        "goal": Goal.option_song_of_the_nomai
    }


class TestSuitlessLogsanityWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true",
        "logsanity": "true"
    }


class TestSuitlessLogsanitySongOfNomaiWorld(OuterWildsTestBase):
    options = {
        "shuffle_spacesuit": "true",
        "logsanity": "true",
        "goal": Goal.option_song_of_the_nomai
    }

    def test_suitless_logic(self):
        # Spacesuit is required for PTM locations (via region logic rather than location logic)
        self.assertNotReachableWith("GD Ship Log: Probe Tracking Module 1 - Millions", [
            "Tornado Aerodynamic Adjustments", "Electrical Insulation", "Translator"
        ])
        self.assertReachableWith("GD Ship Log: Probe Tracking Module 1 - Millions", [
            "Tornado Aerodynamic Adjustments", "Electrical Insulation", "Spacesuit", "Translator"
        ])


class TestRandomOrbitsOff(OuterWildsTestBase):
    options = {
        "randomize_orbits": "false",
        "randomize_rotations": "false",
    }


# This is why we pulled rotations out into its own option after all
class TestRandomRotationsOff(OuterWildsTestBase):
    options = {
        "randomize_rotations": "false",
    }


class TestUpgradeCounts(OuterWildsTestBase):
    options = {
        "upgrade_counts": {
            "Oxygen Capacity Upgrade": 10,
            "Fuel Capacity Upgrade": 1,
            "Boost Duration Upgrade": 5,
        }
    }


class TestZeroUpgradeCounts(OuterWildsTestBase):
    options = {
        "upgrade_counts": {
            "Oxygen Capacity Upgrade": 0,
            "Fuel Capacity Upgrade": 0,
            "Boost Duration Upgrade": 0,
        }
    }
