from . import PokeparkTest

class TestPokemonFriendshipDependencies(PokeparkTest):

    def test_tropius_unlock(self) -> None:
        """Verify unlock conditions for accessing Tropius in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Tropius"]
        items = [["Tropius Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_pachirisu_unlock(self) -> None:
        """Verify unlock conditions for accessing Pachirisu in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Pachirisu"]
        items = [["Pachirisu Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_bonsly_unlock(self) -> None:
        """Verify unlock conditions for accessing Bonsly in Meadow Zone Overworld and Friendship Event"""
        locations = ["Meadow Zone - Overworld - Bonsly","Meadow Zone - Overworld - Bonsly Friendship Event"]
        items = [["Bonsly Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_sudowoodo_unlock(self) -> None:
        """Verify unlock conditions for accessing Sudowoodo in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Sudowoodo"]
        items = [["Sudowoodo Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_lotad_unlock(self) -> None:
        """Verify unlock conditions for accessing Lotad in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Lotad"]
        items = [["Lotad Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_shinx_unlock(self) -> None:
        """Verify unlock conditions for accessing Shinx in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Shinx"]
        items = [["Shinx Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_scyther_unlock(self) -> None:
        """Verify unlock conditions for accessing Scyther in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Scyther"]
        items = [["Scyther Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_caterpie_unlock(self) -> None:
        """Verify unlock conditions for accessing Caterpie in Meadow Zone Overworld and Friendship Event"""
        locations = ["Meadow Zone - Overworld - Caterpie","Meadow Zone - Overworld - Caterpie Friendship Event"]
        items = [["Caterpie Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_butterfree_unlock(self) -> None:
        """Verify unlock conditions for accessing Butterfree in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Butterfree"]
        items = [["Butterfree Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_chimchar_unlock(self) -> None:
        """Verify unlock conditions for accessing Chimchar in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Chimchar"]
        items = [["Chimchar Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_ambipom_unlock(self) -> None:
        """Verify unlock conditions for accessing Ambipom in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Ambipom"]
        items = [["Ambipom Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_weedle_unlock(self) -> None:
        """Verify unlock conditions for accessing Weedle in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Weedle"]
        items = [["Weedle Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_shroomish_unlock(self) -> None:
        """Verify unlock conditions for accessing Shroomish in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Shroomish"]
        items = [["Shroomish Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magikarp_unlock(self) -> None:
        """Verify unlock conditions for accessing Magikarp in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Magikarp"]
        items = [["Magikarp Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_bidoof1_unlock(self) -> None:
        locations = []
        items = [["Bidoof1 Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_bidoof2_unlock(self) -> None:
        locations = []
        items = [["Bidoof2 Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_bidoof3_unlock(self) -> None:
        locations = []
        items = [["Bidoof3 Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_bibarel_unlock(self) -> None:
        """Verify unlock conditions for accessing Bibarel in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Bibarel"]
        items = [["Bibarel Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_starly_unlock(self) -> None:
        """Verify unlock conditions for accessing Starly in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Starly"]
        items = [["Starly Unlock"],["Starly Unlock 2"]]
        self.assertAccessDependency(locations, items)

    def test_torterra_unlock(self) -> None:
        """Verify unlock conditions for accessing Torterra in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Torterra"]
        items = [["Torterra Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_floatzel_unlock(self) -> None:
        """Verify unlock conditions for accessing Floatzel in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Floatzel"]
        items = [["Floatzel Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_mudkip_unlock(self) -> None:
        """Verify unlock conditions for accessing Mudkip in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Mudkip"]
        items = [["Mudkip Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_totodile_unlock(self) -> None:
        """Verify unlock conditions for accessing Totodile in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Totodile"]
        items = [["Totodile Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_golduck_unlock(self) -> None:
        """Verify unlock conditions for accessing Golduck in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Golduck"]
        items = [["Golduck Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_krabby_unlock(self) -> None:
        """Verify unlock conditions for accessing Krabby in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Krabby"]
        items = [["Krabby Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_corphish_unlock(self) -> None:
        """Verify unlock conditions for accessing Corphish in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Corphish"]
        items = [["Corphish Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_pikachu_balloon_unlock(self) -> None:
        """Verify unlock conditions for accessing Pikachu in Pelipper's Circle Circuit"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Pikachu"]
        items = [["Pikachu Balloon"]]
        self.assertAccessDependency(locations, items)

    def test_pikachu_surfboard_unlock(self) -> None:
        """Verify unlock conditions for accessing Pikachu in Gyarados' Aqua Dash"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Pikachu"]
        items = [["Pikachu Surfboard"]]
        self.assertAccessDependency(locations, items)

    #region access tests
    def test_can_reach_beach_zone(self)->None:
        """Verify ability to access Beach Zone Overworld"""

        self.collect_by_name(["Beach Zone Unlock"])
        self.assertTrue(self.can_reach_region("Beach Zone - Overworld"))

    def test_can_not_reach_beach_zone(self)->None:
        """Verify inability to access Beach Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Beach Zone - Overworld"))

    def test_can_not_reach_beach_zone_with_everything_but_beach_zone_unlock(self)->None:
        """Verify inability to access Beach Zone Overworld without specific unlock"""
        self.collect_all_but(["Beach Zone Unlock"])
        self.assertFalse(self.can_reach_region("Beach Zone - Overworld"))

    def test_can_reach_venusaur_minigame(self)->None:
        """Verify ability to access Venusaur's Vine Swing minigame"""

        self.collect_by_name("Beach Zone Unlock")
        self.assertTrue(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))
