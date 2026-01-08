from .bases import OuterWildsTestBase


class TestDLC(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1
    }

    def test_eote_dlc(self):
        self.assertEqual(self.getLocationCount(), 127)  # 87(+2V) base game + 34(+4V) DLC locations

        self.assertNotReachableWith("EotE: River Lowlands Workshop", [])
        self.assertReachableWith("EotE: River Lowlands Workshop", [
            "Ghost Matter Wavelength"
        ])

    def test_eote_goals(self):
        # With DLC enabled there are more victory events, but "only 'Song of' goals need Coordinates" remains true
        self.assertAccessDependency(
            [
                "Victory - Song of Five", "Victory - Song of the Nomai", "Victory - Song of the Stranger",
                "Victory - Song of Six", "Victory - Song of Seven"
            ],
            [["Coordinates"]]
        )

        # these items are required on every path to the Prisoner (from a non-Stranger spawn)
        eote_required_items = [
            "Launch Codes",  # to get to Stranger without spawning there
            "Dream Totem Patch",  # all paths to Dream Raft Loop involve a totem or two
            "Limbo Warp Patch",  # need all 3 glitches to enter the finale from Dream Raft Loop
            "Projection Range Patch",
            "Alarm Bypass Patch",
        ]
        # getting from Stranger to Dreamworld is the part with multiple "item paths"
        self.assertReachableWith("Victory - Echoes of the Eye", eote_required_items + [
            "Stranger Light Modulator", "Hidden Gorge Painting Code"
        ])
        self.assertReachableWith("Victory - Echoes of the Eye", eote_required_items + [
            "Breach Override Codes", "Hidden Gorge Painting Code"
        ])
        self.assertReachableWith("Victory - Echoes of the Eye", eote_required_items + [
            "Ghost Matter Wavelength", "River Lowlands Painting Code"
        ])
        self.assertReachableWith("Victory - Echoes of the Eye", eote_required_items + [
            "Ghost Matter Wavelength", "Stranger Light Modulator", "Cinder Isles Painting Code"
        ])

        self.assertReachableWith(
            "Victory - Song of the Stranger",
            self.song_of_five_required_items +
            eote_required_items + ["Ghost Matter Wavelength", "River Lowlands Painting Code"]
        )

        self.assertReachableWith(
            "Victory - Song of Six",
            self.song_of_five_required_items +
            eote_required_items + ["Ghost Matter Wavelength", "River Lowlands Painting Code"]
        )
        self.assertReachableWith(
            "Victory - Song of Six",
            self.song_of_five_required_items +
            self.song_of_the_nomai_additional_required_items
        )

        self.assertReachableWith(
            "Victory - Song of Seven",
            self.song_of_five_required_items +
            self.song_of_the_nomai_additional_required_items +
            eote_required_items + ["Ghost Matter Wavelength", "River Lowlands Painting Code"]
        )


class TestDLCWithLogsanity(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1,
        "logsanity": 1
    }

    def test_eote_dlc_with_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 34(+4V) DLC default locations + 72 DLC logsanity locations
        self.assertEqual(self.getLocationCount(), 375)

        # Routes to Shrouded Woodlands

        # the obvious route: use the RL artifact on the RL flame
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [
            "Ghost Matter Wavelength", "River Lowlands Painting Code",
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Ghost Matter Wavelength" ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "River Lowlands Painting Code" ])

        # get the lab artifact, return to main hangar, use it on RL flame
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [
            "Breach Override Codes", "River Lowlands Painting Code",
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Breach Override Codes" ])

        # take a raft to HG, use its artifact on HG flame, use totems to reach HG dock, take dream raft to SW dock
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [
            "Stranger Light Modulator", "Hidden Gorge Painting Code", "Dream Totem Patch", "Raft Docks Patch"
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Dream Totem Patch", "Raft Docks Patch" ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Stranger Light Modulator", "Hidden Gorge Painting Code" ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands 1 - Visit", [ "Stranger Light Modulator", "Hidden Gorge Painting Code", "Raft Docks Patch" ])

        # Routes to Shrouded Woodlands Archive

        # the first-time vanilla route:
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands Archive 1 - Enter", [
            "River Lowlands Painting Code", "Ghost Matter Wavelength",  # open RL dock
            # wait for dam to break
            "Breach Override Codes", "Hidden Gorge Painting Code",  # use a different flame
            "Dream Totem Patch",  # to reach the dream raft, and take it to SW
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands Archive 1 - Enter", [
            "River Lowlands Painting Code", "Dream Totem Patch"
        ])

        # the "intended shortcut" using the limbo warp glitch learned from SW archive:
        self.assertReachableWith("DW Ship Log: Shrouded Woodlands Archive 1 - Enter", [
            "River Lowlands Painting Code", "Ghost Matter Wavelength", "Dream Totem Patch",  # get on the dream raft
            "Limbo Warp Patch",  # fall down to Subterranean Lake "out of bounds"
            # then simply walk into SW archives
        ])
        self.assertNotReachableWith("DW Ship Log: Shrouded Woodlands Archive 1 - Enter", ["Limbo Warp Patch"])


class TestStrangerSpawn(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1,
        "logsanity": 1,
        "spawn": "stranger",
    }

    def test_stranger_spawn(self):
        self.assertReachableWith("EotE Ship Log: River Lowlands 1 - Visit", [])

        self.assertNotReachableWith("TH: Talk to Hornfels", [])
        self.assertReachableWith("TH: Talk to Hornfels", ["Launch Codes"])

        self.assertReachableWith("Victory - Echoes of the Eye", [
            # without "Launch Codes"
            "Dream Totem Patch",  # all paths to Dream Raft Loop involve a totem or two
            "Limbo Warp Patch",  # need all 3 glitches to enter the finale from Dream Raft Loop
            "Projection Range Patch",
            "Alarm Bypass Patch",
            "Stranger Light Modulator",
            "Hidden Gorge Painting Code"
        ])


class TestSpawnElsewhere(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1,
        "logsanity": 1,
        "spawn": "hourglass_twins",  # doesn't matter where, as long as it's neither TH nor Stranger
    }

    def test_stranger_spawn(self):
        self.assertNotReachableWith("EotE Ship Log: River Lowlands 1 - Visit", [])
        self.assertReachableWith("EotE Ship Log: River Lowlands 1 - Visit", ["Launch Codes"])

        self.assertNotReachableWith("TH: Talk to Hornfels", [])
        self.assertReachableWith("TH: Talk to Hornfels", ["Launch Codes"])


class TestDLCOnly(OuterWildsTestBase):
    options = {
        "dlc_only": 1,
    }

    def test_dlc_only(self):
        self.assertEqual(self.getLocationCount(), 35)  # 34(+1V) DLC default locations


class TestDLCOnlyLogsanity(OuterWildsTestBase):
    options = {
        "dlc_only": 1,
        "logsanity": 1,
    }

    def test_dlc_only_logsanity(self):
        self.assertEqual(self.getLocationCount(), 107)  # 34(+1V) DLC default locations + 72 DLC logsanity locations
