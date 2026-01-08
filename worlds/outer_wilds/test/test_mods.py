from .bases import OuterWildsTestBase


class TestHN1(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1
    }

    def test_hn1(self):
        self.assertEqual(self.getLocationCount(), 109)  # 87(+2V) base game + 20 HN1 locations


class TestHN1Logsanity(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1,
        "logsanity": 1
    }

    def test_hn1_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 20 HN1 default locations + 41 HN1 logsanity locations
        self.assertEqual(self.getLocationCount(), 326)


class TestOutsider(OuterWildsTestBase):
    options = {
        "enable_outsider_mod": 1
    }

    def test_outsider(self):
        self.assertEqual(self.getLocationCount(), 110)  # 87(+2V) base game + 21 TO locations


class TestOutsiderLogsanity(OuterWildsTestBase):
    options = {
        "enable_outsider_mod": 1,
        "logsanity": 1
    }

    def test_outsider_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 21 TO default locations + 44 TO logsanity locations
        self.assertEqual(self.getLocationCount(), 330)


class TestAC(OuterWildsTestBase):
    options = {
        "enable_ac_mod": 1
    }

    def test_ac(self):
        self.assertEqual(self.getLocationCount(), 110)  # 87(+2V) base game + 21 AC locations


class TestACLogsanity(OuterWildsTestBase):
    options = {
        "enable_ac_mod": 1,
        "logsanity": 1
    }

    def test_ac_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 21 AC default locations + 39 AC logsanity locations
        self.assertEqual(self.getLocationCount(), 325)


class TestHN2(OuterWildsTestBase):
    options = {
        "enable_hn2_mod": 1
    }

    def test_hn2(self):
        self.assertEqual(self.getLocationCount(), 107)  # 87(+2V) base game + 18 HN2 locations


class TestHN2Logsanity(OuterWildsTestBase):
    options = {
        "enable_hn2_mod": 1,
        "logsanity": 1
    }

    def test_hn2_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 18 HN2 default locations + 30 HN2 logsanity locations
        self.assertEqual(self.getLocationCount(), 313)


class TestFQ(OuterWildsTestBase):
    options = {
        "enable_fq_mod": 1
    }

    def test_fq(self):
        self.assertEqual(self.getLocationCount(), 107)  # 87(+2V) base game + 18 FQ locations


class TestFQLogsanity(OuterWildsTestBase):
    options = {
        "enable_fq_mod": 1,
        "logsanity": 1
    }

    def test_fq_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 18 FQ default locations + 38 FQ logsanity locations
        self.assertEqual(self.getLocationCount(), 321)


class TestAllMods(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1,
        "enable_outsider_mod": 1,
        "enable_ac_mod": 1,
        "enable_hn2_mod": 1,
        "enable_fq_mod": 1,
    }

    def test_all_mods(self):
        # 87(+2V) base game default locations +
        # 20 HN1 default locations +
        # 21 TO default locations +
        # 21 AC locations +
        # 18 HN2 locations +
        # 18 FQ default locations
        self.assertEqual(self.getLocationCount(), 187)


class TestAllModsLogsanity(OuterWildsTestBase):
    options = {
        "enable_hn1_mod": 1,
        "enable_outsider_mod": 1,
        "enable_ac_mod": 1,
        "enable_hn2_mod": 1,
        "enable_fq_mod": 1,
        "logsanity": 1
    }

    def test_all_mods_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 20 HN1 default locations + 41 HN1 logsanity locations +
        # 21 TO default locations + 44 TO logsanity locations +
        # 21 AC default locations + 39 AC logsanity locations +
        # 18 HN2 default locations + 30 HN2 logsanity locations +
        # 18 FQ default locations + 38 FQ logsanity locations
        self.assertEqual(self.getLocationCount(), 555)


# this is just to get an assertion on the maximum possible location count
class TestAllModsAndDLCLogsanity(OuterWildsTestBase):
    options = {
        "enable_eote_dlc": 1,
        "enable_hn1_mod": 1,
        "enable_outsider_mod": 1,
        "enable_ac_mod": 1,
        "enable_hn2_mod": 1,
        "enable_fq_mod": 1,
        "logsanity": 1
    }

    def test_all_mods_and_dlc_logsanity(self):
        # 87(+2V) base game default locations + 176 base game logsanity locations +
        # 34(+4V) DLC default locations + 72 DLC logsanity locations +
        # 20 HN1 default locations + 41 HN1 logsanity locations +
        # 21 TO default locations + 44 TO logsanity locations +
        # 21 AC default locations + 39 AC logsanity locations +
        # 18 HN2 default locations + 30 HN2 logsanity locations +
        # 18 FQ default locations + 38 FQ logsanity locations
        self.assertEqual(self.getLocationCount(), 665)


class RegressionTestACAndWarpRando(OuterWildsTestBase):
    options = {
        "enable_ac_mod": 1,
        "randomize_warp_platforms": 1,
    }

    # There's no easy way to test "enough seeds" to prove it's fully fixed,
    # but when the gen failure was discovered this seed caused it.
    seed = 1

    def world_setup(self, *args, **kwargs):
        super().world_setup(self.seed)
