from . import AVTestBase


class TestGlitchsanityDisabled(AVTestBase):
    options = {
        "glitchsanity": 0,
    }

    def test_glitchsanity_location_not_present(self):
        self.collect_all_but([])

        with self.assertRaises(KeyError):
            self.can_reach_location("Glitch a Furglot")

        with self.assertRaises(KeyError):
            self.can_reach_location("Glitch an Artichoker")


class TestGlitchsanityEnabled(AVTestBase):
    options = {
        "glitchsanity": 1,
    }

    def test_glitchsanity_location_present(self):
        self.collect_all_but([])
        self.assertTrue(self.can_reach_location("Glitch a Furglot"))
        self.assertTrue(self.can_reach_location("Glitch an Artichoker"))
