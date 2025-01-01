from . import LingoTestBase


class TestVanillaDoorsNormalSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "shuffle_colors": "true",
        "sunwarp_access": "normal"
    }

    def test_access(self):
        self.assertTrue(self.multiworld.state.can_reach("Crossroads", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))

        self.collect_by_name("Yellow")
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestSimpleDoorsNormalSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "true",
        "sunwarp_access": "normal"
    }

    def test_access(self):
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("Second Room - Exit Door")
        self.assertTrue(self.multiworld.state.can_reach("Crossroads", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))

        self.collect_by_name(["Crossroads - Tower Entrances", "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestSimpleDoorsDisabledSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "true",
        "sunwarp_access": "disabled"
    }

    def test_access(self):
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("Second Room - Exit Door")
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))

        self.collect_by_name(["Hub Room - Crossroads Entrance", "Crossroads - Tower Entrancse",
                              "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestSimpleDoorsUnlockSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "true",
        "sunwarp_access": "unlock"
    }

    def test_access(self):
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("Second Room - Exit Door")
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name(["Crossroads - Tower Entrances", "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))

        self.collect_by_name("Sunwarps")
        self.assertTrue(self.multiworld.state.can_reach("Crossroads", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestComplexDoorsNormalSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "false",
        "sunwarp_access": "normal"
    }

    def test_access(self):
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("Second Room - Exit Door")
        self.assertTrue(self.multiworld.state.can_reach("Crossroads", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))

        self.collect_by_name(["Crossroads - Tower Entrance", "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertTrue(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestComplexDoorsDisabledSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "false",
        "sunwarp_access": "disabled"
    }

    def test_access(self):
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("Second Room - Exit Door")
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))

        self.collect_by_name(["Hub Room - Crossroads Entrance", "Crossroads - Tower Entrance",
                              "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestComplexDoorsIndividualSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "false",
        "sunwarp_access": "individual"
    }

    def test_access(self):
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("Second Room - Exit Door")
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("1 Sunwarp")
        self.assertTrue(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name(["Crossroads - Tower Entrance", "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))

        self.collect_by_name("2 Sunwarp")
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))

        self.collect_by_name("3 Sunwarp")
        self.assertTrue(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestComplexDoorsProgressiveSunwarps(LingoTestBase):
    options = {
        "shuffle_doors": "doors",
        "group_doors": "false",
        "sunwarp_access": "progressive"
    }

    def test_access(self):
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name("Second Room - Exit Door")
        self.assertFalse(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        progressive_pilgrimage = self.get_items_by_name("Progressive Pilgrimage")
        self.collect(progressive_pilgrimage[0])
        self.assertTrue(self.multiworld.state.can_reach("Crossroads", "Region", self.player))

        self.collect_by_name(["Crossroads - Tower Entrance", "Orange Tower Fourth Floor - Hot Crusts Door"])
        self.assertFalse(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))

        self.collect(progressive_pilgrimage[1])
        self.assertTrue(self.multiworld.state.can_reach("Orange Tower Third Floor", "Region", self.player))
        self.assertFalse(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))

        self.collect(progressive_pilgrimage[2])
        self.assertTrue(self.multiworld.state.can_reach("Outside The Initiated", "Region", self.player))


class TestUnlockSunwarpPilgrimage(LingoTestBase):
    options = {
        "sunwarp_access": "unlock",
        "shuffle_colors": "false",
        "enable_pilgrimage": "true"
    }

    def test_access(self):
        self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))

        self.collect_by_name("Sunwarps")

        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))


class TestIndividualSunwarpPilgrimage(LingoTestBase):
    options = {
        "sunwarp_access": "individual",
        "shuffle_colors": "false",
        "enable_pilgrimage": "true"
    }

    def test_access(self):
        for i in range(1, 7):
            self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
            self.collect_by_name(f"{i} Sunwarp")

        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))


class TestProgressiveSunwarpPilgrimage(LingoTestBase):
    options = {
        "sunwarp_access": "progressive",
        "shuffle_colors": "false",
        "enable_pilgrimage": "true"
    }

    def test_access(self):
        for item in self.get_items_by_name("Progressive Pilgrimage"):
            self.assertFalse(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
            self.collect(item)

        self.assertTrue(self.can_reach_location("Pilgrim Antechamber - PILGRIM"))
