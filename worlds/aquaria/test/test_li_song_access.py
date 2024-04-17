from worlds.aquaria.test import AquariaTestBase


class LiAccessTest(AquariaTestBase):

    def test_li_song_location(self) -> None:
        """Test locations that require Li"""
        locations = [
            "Sunken city right area, crate close to the save cristal",
            "Sunken city right area, crate in the left bottom room",
            "Sunken city left area, crate in the little pipe room",
            "Sunken city left area, crate close to the save cristal",
            "Sunken city left area, crate before the bedroom",
            "Sunken city left area, Girl Costume",
            "Sunken city, bulb on the top of the boss area (boiler room)",
            "The body center area, breaking li cage",
            "The body main area, bulb on the main path blocking tube",
            "The body left area, first bulb in the top face room",
            "The body left area, second bulb in the top face room",
            "The body left area, bulb bellow the water stream",
            "The body left area, bulb in the top path to the top face room",
            "The body left area, bulb in the bottom face room",
            "The body right area, bulb in the top face room",
            "The body right area, bulb in the top path to the bottom face room",
            "The body right area, bulb in the bottom face room",
            "The body bottom area, bulb in the Jelly Zap room",
            "The body bottom area, bulb in the nautilus room",
            "The body bottom area, Mutant Costume",
            "Final boss area, bulb in the boss third form room",
        ]
        items = [["Li and Li song"]]
        self.assertAccessDependency(locations, items)
