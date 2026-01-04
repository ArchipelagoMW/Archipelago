from . import LingoTestBase


class TestPostgameVanillaTheEnd(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "victory_condition": "the_end",
        "shuffle_postgame": "false",
    }

    def test_requirement(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]

        self.assertTrue("The End (Solved)" in location_names)
        self.assertTrue("Champion's Rest - YOU" in location_names)
        self.assertFalse("Orange Tower Seventh Floor - THE MASTER" in location_names)
        self.assertFalse("The Red - Achievement" in location_names)


class TestPostgameComplexDoorsTheEnd(LingoTestBase):
    options = {
        "shuffle_doors": "complex",
        "victory_condition": "the_end",
        "shuffle_postgame": "false",
    }

    def test_requirement(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]

        self.assertTrue("The End (Solved)" in location_names)
        self.assertFalse("Orange Tower Seventh Floor - THE MASTER" in location_names)
        self.assertTrue("The Red - Achievement" in location_names)


class TestPostgameLateColorHunt(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "victory_condition": "the_end",
        "sunwarp_access": "disabled",
        "shuffle_postgame": "false",
    }

    def test_requirement(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]

        self.assertFalse("Champion's Rest - YOU" in location_names)


class TestPostgameVanillaTheMaster(LingoTestBase):
    options = {
        "shuffle_doors": "none",
        "victory_condition": "the_master",
        "shuffle_postgame": "false",
    }

    def test_requirement(self):
        location_names = [location.name for location in self.multiworld.get_locations(self.player)]

        self.assertTrue("Orange Tower Seventh Floor - THE END" in location_names)
        self.assertTrue("Orange Tower Seventh Floor - Mastery Achievements" in location_names)
        self.assertTrue("The Red - Achievement" in location_names)
        self.assertFalse("Mastery Panels" in location_names)
