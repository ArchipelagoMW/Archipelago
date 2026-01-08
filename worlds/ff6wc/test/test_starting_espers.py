from . import FF6WCTestBase


class TestStartingEsperFlagBegin(FF6WCTestBase):
    """ -stesp at beginning of flagstring """
    options = {
        "Flagstring": "-stesp 4 4 -cg -oa 2.7.7.3.r.3.r.3.r.5.r.5.r.5.r.10.10.25.8.15.15 -sc1 gogo -etn -yremove",
    }

    def test_stesp_changes_to_sen(self) -> None:
        self.assertNotIn("stesp", self.world.options.Flagstring.value)
        sen_value = self.world.options.Flagstring.get_flag("-sen")
        self.assertEqual(sen_value.count(","), 3)


class TestStartingEsperFlagEnd(FF6WCTestBase):
    """ -stesp at end of flagstring """
    options = {
        "Flagstring": "-cg -oa 2.7.7 -sc1 random -sc2 random -yremove -stesp 2 4",
    }

    def test_stesp_changes_to_sen(self) -> None:
        self.assertNotIn("stesp", self.world.options.Flagstring.value)
        sen_value = self.world.options.Flagstring.get_flag("-sen")
        comma_count = sen_value.count(",")
        self.assertLessEqual(comma_count, 3)
        self.assertGreaterEqual(comma_count, 1)


class TestStartingEsperFlagMid(FF6WCTestBase):
    """ -stesp at middle of flagstring """
    options = {
        "Flagstring": "-oa 2.6.7 -cg -stesp 3 3 -sc1 random -yremove",
    }

    def test_stesp_changes_to_sen(self) -> None:
        self.assertNotIn("stesp", self.world.options.Flagstring.value)
        sen_value = self.world.options.Flagstring.get_flag("-sen")
        self.assertEqual(sen_value.count(","), 2)
