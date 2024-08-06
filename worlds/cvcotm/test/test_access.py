from . import CVCotMTestBase
from ..data import iname, lname


class CatacombSphere1Test(CVCotMTestBase):

    def test_always_accessible(self) -> None:
        self.assertTrue(self.can_reach_location(lname.cc4))
        self.assertTrue(self.can_reach_location(lname.cc8))
        self.assertTrue(self.can_reach_location(lname.cc9))
        self.assertTrue(self.can_reach_location(lname.cc10))
        self.assertTrue(self.can_reach_location(lname.cc13))
        self.assertTrue(self.can_reach_location(lname.cc14))
        self.assertTrue(self.can_reach_location(lname.cc16))
        self.assertTrue(self.can_reach_location(lname.cc20))
        self.assertTrue(self.can_reach_location(lname.cc22))
        self.assertTrue(self.can_reach_location(lname.cc24))


class DoubleTest(CVCotMTestBase):

    def test_double_only(self) -> None:
        self.assertFalse(self.can_reach_location(lname.cc3))
        self.assertFalse(self.can_reach_location(lname.cc3b))
        self.assertFalse(self.can_reach_location(lname.cc14b))
        self.assertFalse(self.can_reach_location(lname.cc25))
        self.assertFalse(self.can_reach_entrance("Catacomb to Stairway"))
        self.assertFalse(self.can_reach_entrance("Stairway to Audience"))

        self.collect_by_name([iname.double])

        self.assertTrue(self.can_reach_location(lname.cc3))
        self.assertTrue(self.can_reach_location(lname.cc14b))
        self.assertTrue(self.can_reach_location(lname.cc25))
        self.assertTrue(self.can_reach_entrance("Catacomb to Stairway"))
        self.assertTrue(self.can_reach_entrance("Stairway to Audience"))
        self.assertFalse(self.can_reach_location(lname.cc3b))

    def test_double_with_freeze(self) -> None:
        self.collect_by_name([iname.mercury, iname.serpent])
        self.assertFalse(self.can_reach_location(lname.cc3b))

        self.collect_by_name([iname.double])

        self.assertTrue(self.can_reach_location(lname.cc3b))


class TackleTest(CVCotMTestBase):
    options = {
        "break_iron_maidens": True
    }

    def test_tackle_only_in_catacomb(self) -> None:
        self.assertFalse(self.can_reach_location(lname.cc5))

        self.collect_by_name([iname.tackle])

        self.assertTrue(self.can_reach_location(lname.cc5))

    def test_tackle_only_in_audience_room(self) -> None:
        self.collect_by_name([iname.double])

        self.assertFalse(self.can_reach_location(lname.ar11))
        self.assertFalse(self.can_reach_entrance("Audience to Machine Bottom"))

        self.collect_by_name([iname.tackle])

        self.assertTrue(self.can_reach_location(lname.ar11))
        self.assertTrue(self.can_reach_entrance("Audience to Machine Bottom"))

    def test_tackle_with_kick_boots(self) -> None:
        self.collect_by_name([iname.double, iname.kick_boots])

        self.assertFalse(self.can_reach_location(lname.mt14))
        self.assertFalse(self.can_reach_entrance("Gallery Upper to Lower"))

        self.collect_by_name([iname.tackle])

        self.assertTrue(self.can_reach_location(lname.mt14))
        self.assertTrue(self.can_reach_entrance("Gallery Upper to Lower"))

    def test_tackle_with_heavy_ring(self) -> None:
        self.collect_by_name([iname.double, iname.heavy_ring])

        self.assertFalse(self.can_reach_location(lname.ar27))
        self.assertFalse(self.can_reach_location(lname.ug8))
        self.assertFalse(self.can_reach_entrance("Into Warehouse Main"))
        self.assertFalse(self.can_reach_entrance("Gallery Lower to Upper"))

        self.collect_by_name([iname.tackle])

        self.assertTrue(self.can_reach_location(lname.ar27))
        self.assertTrue(self.can_reach_location(lname.ug8))
        self.assertTrue(self.can_reach_entrance("Into Warehouse Main"))
        self.assertTrue(self.can_reach_entrance("Gallery Lower to Upper"))

    def test_tackle_with_roc_wing(self) -> None:
        self.collect_by_name([iname.double, iname.roc_wing])

        self.assertFalse(self.can_reach_location(lname.ar26))

        self.collect_by_name([iname.tackle])

        self.assertTrue(self.can_reach_location(lname.ar26))


class KickBootsTest(CVCotMTestBase):
    options = {
        "break_iron_maidens": True
    }

    def test_kick_boots_only_in_catacomb(self) -> None:
        self.assertFalse(self.can_reach_location(lname.cc8b))
        self.assertFalse(self.can_reach_location(lname.cc14b))
        self.assertFalse(self.can_reach_entrance("Catacomb to Stairway"))

        self.collect_by_name([iname.kick_boots])

        self.assertTrue(self.can_reach_location(lname.cc8b))
        self.assertTrue(self.can_reach_location(lname.cc14b))
        self.assertTrue(self.can_reach_entrance("Catacomb to Stairway"))

    def test_kick_boots_only_in_audience_room(self) -> None:
        self.collect_by_name([iname.double])

        self.assertFalse(self.can_reach_location(lname.ar17b))
        self.assertFalse(self.can_reach_location(lname.ar19))
        self.assertFalse(self.can_reach_entrance("Audience to Machine Top"))
        self.assertFalse(self.can_reach_entrance("Audience to Chapel"))

        self.collect_by_name([iname.kick_boots])

        self.assertTrue(self.can_reach_location(lname.ar17b))
        self.assertTrue(self.can_reach_location(lname.ar19))
        self.assertTrue(self.can_reach_entrance("Audience to Machine Top"))
        self.assertTrue(self.can_reach_entrance("Audience to Chapel"))

    def test_kick_boots_with_tackle(self) -> None:
        self.collect_by_name([iname.double, iname.tackle])

        self.assertFalse(self.can_reach_location(lname.mt3))
        self.assertFalse(self.can_reach_location(lname.mt6))

        self.collect_by_name([iname.kick_boots])

        self.assertTrue(self.can_reach_location(lname.mt3))
        self.assertTrue(self.can_reach_location(lname.mt6))

    def test_kick_boots_with_freeze(self) -> None:
        self.collect_by_name([iname.double, iname.mars, iname.cockatrice])

        self.assertFalse(self.can_reach_region("Underground Gallery Upper"))
        self.assertFalse(self.can_reach_location(lname.th3))
        self.assertFalse(self.can_reach_location(lname.ug3))
        self.assertFalse(self.can_reach_location(lname.ug3b))

        self.collect_by_name([iname.kick_boots])

        self.assertTrue(self.can_reach_region("Underground Gallery Upper"))
        self.assertTrue(self.can_reach_location(lname.th3))
        self.assertTrue(self.can_reach_location(lname.ug3))
        self.assertTrue(self.can_reach_location(lname.ug3b))

    def test_kick_boots_with_last_key(self) -> None:
        self.collect_by_name([iname.double, iname.last_key])

        self.assertFalse(self.can_reach_location(lname.cr1))

        self.collect_by_name([iname.kick_boots])

        self.assertTrue(self.can_reach_location(lname.cr1))


class HeavyRingTest(CVCotMTestBase):
    options = {
        "break_iron_maidens": True
    }

    def test_heavy_ring_only_in_catacomb(self) -> None:
        self.assertFalse(self.can_reach_location(lname.cc1))

        self.collect_by_name([iname.heavy_ring])

        self.assertTrue(self.can_reach_location(lname.cc1))

    def test_heavy_ring_only_in_audience_room(self) -> None:
        self.collect_by_name([iname.double])

        self.assertFalse(self.can_reach_location(lname.ar9))
        self.assertFalse(self.can_reach_entrance("Audience to Gallery"))
        self.assertFalse(self.can_reach_entrance("Audience to Warehouse"))

        self.collect_by_name([iname.heavy_ring])

        self.assertTrue(self.can_reach_location(lname.ar9))
        self.assertTrue(self.can_reach_entrance("Audience to Gallery"))
        self.assertTrue(self.can_reach_entrance("Audience to Warehouse"))

    def test_heavy_ring_with_tackle(self) -> None:
        self.collect_by_name([iname.double, iname.tackle])

        self.assertFalse(self.can_reach_location(lname.ar27))
        self.assertFalse(self.can_reach_entrance("Into Warehouse Main"))

        self.collect_by_name([iname.heavy_ring])

        self.assertTrue(self.can_reach_location(lname.ar27))
        self.assertTrue(self.can_reach_entrance("Into Warehouse Main"))

    def test_heavy_ring_with_kick_boots(self) -> None:
        self.collect_by_name([iname.double, iname.kick_boots])

        self.assertFalse(self.can_reach_location(lname.ct4))
        self.assertFalse(self.can_reach_location(lname.ct10))
        self.assertFalse(self.can_reach_location(lname.ug1))
        self.assertFalse(self.can_reach_location(lname.ug2))

        self.collect_by_name([iname.heavy_ring])

        self.assertTrue(self.can_reach_location(lname.ct4))
        self.assertTrue(self.can_reach_location(lname.ct10))
        self.assertTrue(self.can_reach_location(lname.ug1))
        self.assertTrue(self.can_reach_location(lname.ug2))

    def test_heavy_ring_with_roc_wing(self) -> None:
        self.collect_by_name([iname.double, iname.roc_wing])

        self.assertFalse(self.can_reach_location(lname.ar26))

        self.collect_by_name([iname.tackle])

        self.assertTrue(self.can_reach_location(lname.ar26))


class CleansingTest(CVCotMTestBase):
    options = {
        "break_iron_maidens": True
    }

    def test_cleansing_only(self) -> None:
        self.collect_by_name([iname.double])

        self.assertFalse(self.can_reach_entrance("Into Waterway Main"))

        self.collect_by_name([iname.cleansing])

        self.assertTrue(self.can_reach_entrance("Into Waterway Main"))

    def test_cleansing_with_roc(self) -> None:
        self.collect_by_name([iname.double, iname.roc_wing])

        self.assertFalse(self.can_reach_location(lname.uy12b))
        self.assertFalse(self.can_reach_location(lname.uy17))

        self.collect_by_name([iname.cleansing])

        self.assertTrue(self.can_reach_location(lname.uy12b))
        self.assertTrue(self.can_reach_location(lname.uy17))


class IgnoredCleansingTest(CVCotMTestBase):
    options = {
        "break_iron_maidens": True,
        "ignore_cleansing": True
    }

    def test_ignored_cleansing(self) -> None:
        self.assertFalse(self.can_reach_entrance("Into Waterway Main"))
        self.assertFalse(self.can_reach_location(lname.uy12b))
        self.assertFalse(self.can_reach_location(lname.uy17))

        self.collect_by_name([iname.double])

        self.assertTrue(self.can_reach_entrance("Into Waterway Main"))
        self.assertTrue(self.can_reach_location(lname.uy12b))
        self.assertTrue(self.can_reach_location(lname.uy17))


class RocWingTest(CVCotMTestBase):
    options = {
        "break_iron_maidens": True
    }

    def test_roc_wing_only(self) -> None:
        self.assertFalse(self.can_reach_location(lname.sr3))
        self.assertFalse(self.can_reach_location(lname.cc3))
        self.assertFalse(self.can_reach_location(lname.cc3b))
        self.assertFalse(self.can_reach_location(lname.cc8b))
        self.assertFalse(self.can_reach_location(lname.cc14b))
        self.assertFalse(self.can_reach_location(lname.cc25))
        self.assertFalse(self.can_reach_location(lname.as4))
        self.assertFalse(self.can_reach_location(lname.ar14b))
        self.assertFalse(self.can_reach_location(lname.ar17b))
        self.assertFalse(self.can_reach_location(lname.ar19))
        self.assertFalse(self.can_reach_location(lname.ar30))
        self.assertFalse(self.can_reach_location(lname.ar30b))
        self.assertFalse(self.can_reach_location(lname.ow0))
        self.assertFalse(self.can_reach_location(lname.ow1))
        self.assertFalse(self.can_reach_location(lname.th3))
        self.assertFalse(self.can_reach_location(lname.ct1))
        self.assertFalse(self.can_reach_location(lname.ct13))
        self.assertFalse(self.can_reach_location(lname.ug3))
        self.assertFalse(self.can_reach_location(lname.ug3b))
        self.assertFalse(self.can_reach_entrance("Catacomb to Stairway"))
        self.assertFalse(self.can_reach_entrance("Stairway to Audience"))
        self.assertFalse(self.can_reach_entrance("Audience to Machine Top"))
        self.assertFalse(self.can_reach_entrance("Audience to Chapel"))
        self.assertFalse(self.can_reach_entrance("Audience to Observation"))
        self.assertFalse(self.can_reach_entrance("Dip Into Waterway End"))

        self.collect_by_name([iname.roc_wing])

        self.assertTrue(self.can_reach_location(lname.sr3))
        self.assertTrue(self.can_reach_location(lname.cc3))
        self.assertTrue(self.can_reach_location(lname.cc3b))
        self.assertTrue(self.can_reach_location(lname.cc8b))
        self.assertTrue(self.can_reach_location(lname.cc14b))
        self.assertTrue(self.can_reach_location(lname.cc25))
        self.assertTrue(self.can_reach_location(lname.as4))
        self.assertTrue(self.can_reach_location(lname.ar14b))
        self.assertTrue(self.can_reach_location(lname.ar17b))
        self.assertTrue(self.can_reach_location(lname.ar19))
        self.assertTrue(self.can_reach_location(lname.ar30))
        self.assertTrue(self.can_reach_location(lname.ar30b))
        self.assertTrue(self.can_reach_location(lname.ow0))
        self.assertTrue(self.can_reach_location(lname.ow1))
        self.assertTrue(self.can_reach_location(lname.th3))
        self.assertTrue(self.can_reach_location(lname.ct1))
        self.assertTrue(self.can_reach_location(lname.ct13))
        self.assertTrue(self.can_reach_location(lname.ug3))
        self.assertTrue(self.can_reach_location(lname.ug3b))
        self.assertTrue(self.can_reach_entrance("Catacomb to Stairway"))
        self.assertTrue(self.can_reach_entrance("Stairway to Audience"))
        self.assertTrue(self.can_reach_entrance("Audience to Machine Top"))
        self.assertTrue(self.can_reach_entrance("Audience to Chapel"))
        self.assertTrue(self.can_reach_entrance("Audience to Observation"))
        self.assertTrue(self.can_reach_entrance("Dip Into Waterway End"))
        self.assertFalse(self.can_reach_entrance("Arena Passage"))

    def test_roc_wing_exclusive_accessibility(self) -> None:
        self.collect_by_name([iname.double, iname.tackle, iname.kick_boots, iname.heavy_ring, iname.cleansing,
                              iname.last_key, iname.mercury, iname.cockatrice])

        self.assertFalse(self.can_reach_location(lname.sr3))
        self.assertFalse(self.can_reach_location(lname.as4))
        self.assertFalse(self.can_reach_location(lname.ar14b))
        self.assertFalse(self.can_reach_location(lname.ar26))
        self.assertFalse(self.can_reach_location(lname.ar30))
        self.assertFalse(self.can_reach_location(lname.ar30b))
        self.assertFalse(self.can_reach_location(lname.ow0))
        self.assertFalse(self.can_reach_location(lname.uw10))
        self.assertFalse(self.can_reach_location(lname.uw16b))
        self.assertFalse(self.can_reach_location(lname.uy8))
        self.assertFalse(self.can_reach_location(lname.uy13))
        self.assertFalse(self.can_reach_location(lname.uy18))
        self.assertFalse(self.can_reach_location(lname.dracula))
        self.assertFalse(self.can_reach_entrance("Audience to Observation"))
        self.assertFalse(self.can_reach_entrance("Arena Passage"))
        self.assertFalse(self.can_reach_entrance("Dip Into Waterway End"))

        self.collect_by_name([iname.roc_wing])

        self.assertTrue(self.can_reach_location(lname.sr3))
        self.assertTrue(self.can_reach_location(lname.as4))
        self.assertTrue(self.can_reach_location(lname.ar14b))
        self.assertTrue(self.can_reach_location(lname.ar26))
        self.assertTrue(self.can_reach_location(lname.ar30))
        self.assertTrue(self.can_reach_location(lname.ar30b))
        self.assertTrue(self.can_reach_location(lname.ow0))
        self.assertTrue(self.can_reach_location(lname.uw10))
        self.assertTrue(self.can_reach_location(lname.uw16b))
        self.assertTrue(self.can_reach_location(lname.uy8))
        self.assertTrue(self.can_reach_location(lname.uy13))
        self.assertTrue(self.can_reach_location(lname.uy18))
        self.assertTrue(self.can_reach_location(lname.dracula))
        self.assertTrue(self.can_reach_entrance("Audience to Observation"))
        self.assertTrue(self.can_reach_entrance("Arena Passage"))
        self.assertTrue(self.can_reach_entrance("Dip Into Waterway End"))


class LastKeyTest(CVCotMTestBase):
    options = {
        "required_last_keys": 9,
        "available_last_keys": 9
    }

    def test_last_keys(self) -> None:
        self.collect_by_name([iname.double])

        self.assertFalse(self.can_reach_entrance("Ceremonial Door"))

        self.collect([self.get_item_by_name(iname.last_key)] * 1)

        self.assertFalse(self.can_reach_entrance("Ceremonial Door"))

        self.collect([self.get_item_by_name(iname.last_key)] * 7)

        self.assertFalse(self.can_reach_entrance("Ceremonial Door"))

        self.collect([self.get_item_by_name(iname.last_key)] * 1)

        self.assertTrue(self.can_reach_entrance("Ceremonial Door"))


class FreezeTest(CVCotMTestBase):
    options = {
        "break_iron_maidens": True
    }

    def test_freeze_only_in_audience_room(self) -> None:
        self.collect_by_name([iname.double])

        self.assertFalse(self.can_reach_location(lname.cc3b))
        self.assertFalse(self.can_reach_location(lname.ow1))

        self.collect_by_name([iname.mars, iname.serpent])

        self.assertTrue(self.can_reach_location(lname.cc3b))
        self.assertTrue(self.can_reach_location(lname.ow1))

    def test_freeze_with_kick_boots(self) -> None:
        self.collect_by_name([iname.double, iname.kick_boots])

        self.assertFalse(self.can_reach_location(lname.th3))
        self.assertFalse(self.can_reach_location(lname.ct1))
        self.assertFalse(self.can_reach_location(lname.ct13))
        self.assertFalse(self.can_reach_location(lname.ug3))
        self.assertFalse(self.can_reach_location(lname.ug3b))

        self.collect_by_name([iname.mercury, iname.serpent])

        self.assertTrue(self.can_reach_location(lname.th3))
        self.assertTrue(self.can_reach_location(lname.ct1))
        self.assertTrue(self.can_reach_location(lname.ct13))
        self.assertTrue(self.can_reach_location(lname.ug3))
        self.assertTrue(self.can_reach_location(lname.ug3b))

    def test_freeze_with_heavy_ring_and_tackle(self) -> None:
        self.collect_by_name([iname.double, iname.heavy_ring, iname.tackle])

        self.assertFalse(self.can_reach_location(lname.uw14))

        self.collect_by_name([iname.mercury, iname.cockatrice])

        self.assertTrue(self.can_reach_location(lname.uw14))

    def test_freeze_with_cleansing(self) -> None:
        self.collect_by_name([iname.double, iname.cleansing])

        self.assertFalse(self.can_reach_location(lname.uy5))

        self.collect_by_name([iname.mercury, iname.serpent])

        self.assertTrue(self.can_reach_location(lname.uy5))


class UnbrokenMaidensTest(CVCotMTestBase):

    def test_waterway_and_right_gallery_maidens(self) -> None:
        self.collect_by_name([iname.double])

        self.assertFalse(self.can_reach_entrance("Audience to Waterway"))
        self.assertFalse(self.can_reach_entrance("Corridor to Gallery"))

        # Gives access to Chapel Tower wherein we collect the "Iron maidens broken" Event.
        self.collect_by_name([iname.kick_boots])

        self.assertTrue(self.can_reach_entrance("Audience to Waterway"))
        self.assertTrue(self.can_reach_entrance("Corridor to Gallery"))

    def test_left_gallery_maiden(self) -> None:
        self.collect_by_name([iname.double, iname.heavy_ring])

        self.assertFalse(self.can_reach_entrance("Audience to Gallery"))

        self.collect_by_name([iname.roc_wing])

        self.assertTrue(self.can_reach_entrance("Audience to Gallery"))
