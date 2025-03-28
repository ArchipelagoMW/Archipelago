from . import PokeparkTest

class TestUnlockDependencies(PokeparkTest):

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
        """Verify unlock conditions for accessing Bonsly in Meadow Zone Overworld and Friendship - Pokemon Unlock"""
        locations = ["Meadow Zone - Overworld - Bonsly","Meadow Zone - Overworld - Bonsly Friendship - Pokemon Unlock"]
        items = [["Bonsly Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_sudowoodo_unlock(self) -> None:
        """Verify unlock conditions for accessing Sudowoodo in Meadow Zone Overworld"""
        locations = ["Meadow Zone - Overworld - Sudowoodo", "Cavern Zone - Overworld - Sudowoodo"]
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
        """Verify unlock conditions for accessing Caterpie in Meadow Zone Overworld and Friendship - Pokemon Unlock"""
        locations = ["Meadow Zone - Overworld - Caterpie","Meadow Zone - Overworld - Caterpie Friendship - Pokemon Unlock"]
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
        items = [["Bidoof Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_bidoof2_unlock(self) -> None:
        locations = []
        items = [["Bidoof Unlock 2"]]
        self.assertAccessDependency(locations, items)

    def test_bidoof3_unlock(self) -> None:
        locations = []
        items = [["Bidoof Unlock 3"]]
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
        locations = ["Beach Zone - Overworld - Mudkip","Ice Zone - Overworld - Mudkip"]
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
        locations = ["Beach Zone - Overworld - Krabby","Ice Zone - Overworld - Krabby"]
        items = [["Krabby Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_corphish_unlock(self) -> None:
        """Verify unlock conditions for accessing Corphish in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Corphish","Ice Zone - Overworld - Lower Lift Region - Corphish"]
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

    def test_delibird_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""
        locations = [f"Ice Zone - Overworld - Christmas Tree Present {i}"
                     for i in range(1, 5)]
        locations.append("Ice Zone - Overworld - Delibird")
        locations.append("Ice Zone - Overworld - Kirlia")
        items = [["Delibird Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_squirtle_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""
        locations = [f"Ice Zone - Overworld - Christmas Tree Present {i}"
                     for i in range(3, 5)]
        locations.append("Ice Zone - Overworld - Delibird")

        locations.append("Ice Zone - Overworld - Squirtle")
        locations.append("Ice Zone - Overworld - Kirlia")
        items = [["Squirtle Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_smoochum_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""
        locations = [f"Ice Zone - Overworld - Christmas Tree Present {i}"
                     for i in range(4, 5)]
        locations.append("Ice Zone - Overworld - Delibird")

        locations.append("Ice Zone - Overworld - Smoochum")
        locations.append("Ice Zone - Overworld - Kirlia")
        items = [["Smoochum Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_sneasel_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""
        locations = ["Ice Zone - Overworld - Sneasel"]
        items = [["Sneasel Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_mamoswine_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""
        locations = ["Ice Zone - Overworld - Mamoswine"]
        items = [["Mamoswine Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_glalie_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""
        locations = [f"Ice Zone - Overworld - Igloo Quest {i}"
                     for i in range(1, 4)]
        locations.append("Ice Zone - Overworld - Igloo Quest 1 - Pokemon Unlock")
        locations.append("Ice Zone - Overworld - Igloo Quest 2 - Pokemon Unlock")
        locations.append("Ice Zone - Overworld - Prinplup")
        locations.append("Ice Zone - Overworld - Glalie")
        items = [["Glalie Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_primeape_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""

        locations =["Ice Zone - Overworld - Primeape"]
        items = [["Primeape Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_ursaring_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""

        locations =["Ice Zone - Overworld - Ursaring"]
        items = [["Ursaring Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magnemite_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnemite 1 in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Magnemite"]
        items = [["Magnemite Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magnemite2_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnemite 2 in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Magnemite 2"]
        items = [["Magnemite Unlock 2"]]
        self.assertAccessDependency(locations, items)

    def test_magnemite3_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnemite 3 in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Magnemite 3"]
        items = [["Magnemite Unlock 3"]]
        self.assertAccessDependency(locations, items)

    def test_machamp_unlock(self) -> None:
        """Verify unlock conditions for accessing Battle Machamp in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Machamp - Battle"]
        items = [["Machamp Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_diglett_unlock(self) -> None:
        """Verify that Diglett Unlocks allows no new locations"""

        locations =[]
        items = [["Diglett Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magnezone_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnezone in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Magnezone"]
        items = [["Magnezone Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_phanpy_unlock(self) -> None:
        """Verify unlock conditions for accessing Phanpy in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Phanpy"]
        items = [["Phanpy Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_raichu_unlock(self) -> None:
        """Verify unlock conditions for accessing Raichu in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Raichu"]
        items = [["Raichu Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_hitmonlee_unlock(self) -> None:
        """Verify unlock conditions for accessing Hitmonlee in Cavern Zone Overworld"""

        locations =["Cavern Zone - Overworld - Hitmonlee"]
        items = [["Hitmonlee Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_infernape_unlock(self) -> None:
        """Verify unlock conditions for accessing Infernape in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Infernape"]
        items = [["Infernape Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_ninetales_unlock(self) -> None:
        """Verify unlock conditions for accessing Ninetales in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Ninetales"]
        items = [["Ninetales Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_ponyta_unlock(self) -> None:
        """Verify unlock conditions for accessing Ponyta in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Ponyta"]
        items = [["Ponyta Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_torkoal_unlock(self) -> None:
        """Verify unlock conditions for accessing Torkoal in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Torkoal"]
        items = [["Torkoal Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_golem_unlock(self) -> None:
        """Verify unlock conditions for accessing Golem in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Golem"]
        items = [["Golem Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_baltoy_unlock(self) -> None:
        """Verify unlock conditions for accessing Baltoy in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Baltoy",
                    "Magma Zone - Overworld - Baltoy Friendship - Pokemon Unlock"]
        items = [["Baltoy Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_claydol_unlock(self) -> None:
        """Verify unlock conditions for accessing Claydol in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Claydol"]
        items = [["Claydol Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_hitmonchan_unlock(self) -> None:
        """Verify unlock conditions for accessing Hitmonchan in Magma Zone Overworld"""

        locations =["Magma Zone - Overworld - Hitmonchan",
                    "Magma Zone - Overworld - Hitmonchan Friendship - Pokemon Unlock"]
        items = [["Hitmonchan Unlock"]]
        self.assertAccessDependency(locations, items)

class TestRegionAccess(PokeparkTest):
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

    def test_single_locations_reachable_with_beach_zone_unlock(self)->None:
        """Verify abillity to access Health Power Upgrades"""
        locations = ["Treehouse - Health Upgrade 1","Treehouse - Health Upgrade 2","Treehouse - Health Upgrade 3"]
        items = [["Beach Zone Unlock"]]
        self.assertAccessDependency(locations, items,True)

    def test_can_reach_ice_zone(self)->None:
        """Verify ability to access Ice Zone Overworld"""

        self.collect_by_name(["Ice Zone Unlock"])
        self.assertTrue(self.can_reach_region("Ice Zone - Overworld"))

    def test_can_not_reach_ice_zone(self)->None:
        """Verify inability to access Ice Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Ice Zone - Overworld"))

    def test_can_not_reach_ice_zone_with_everything_but_ice_zone_unlock(self)->None:
        """Verify inability to access Ice Zone Overworld without specific unlock"""
        self.collect_all_but(["Ice Zone Unlock"])
        self.assertFalse(self.can_reach_region("Ice Zone - Overworld"))

    def test_single_locations_reachable_with_ice_zone_unlock(self)->None:
        """Verify abillity to access Iron Tail Power Upgrades with Ice Zone or higher"""
        locations = ["Treehouse - Iron Tail Upgrade 1","Treehouse - Iron Tail Upgrade 2","Treehouse - Iron Tail Upgrade 3"]
        items = [["Ice Zone Unlock"], ["Cavern Zone & Magma Zone Unlock"]]
        self.assertAccessDependency(locations, items,True)


    def test_can_reach_cavern_zone(self)->None:
        """Verify ability to access Cavern Zone Overworld"""

        self.collect_by_name(["Cavern Zone & Magma Zone Unlock"])
        self.assertTrue(self.can_reach_region("Cavern Zone - Overworld"))

    def test_can_not_reach_cavern_zone(self)->None:
        """Verify inability to access Cavern Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Cavern Zone - Overworld"))

    def test_can_not_reach_cavern_zone_with_everything_but_cavern_zone_unlock(self)->None:
        """Verify inability to access Cavern Zone Overworld without specific unlock"""
        self.collect_all_but(["Cavern Zone & Magma Zone Unlock"])
        self.assertFalse(self.can_reach_region("Cavern Zone - Overworld"))

    def test_single_locations_reachable_with_cavern_zone_unlock(self)->None:
        """Verify abillity to access Mime Jr. with cavern zone and higher"""
        locations = ["Treehouse - Mime Jr."]
        items = [["Cavern Zone & Magma Zone Unlock"]]
        self.assertAccessDependency(locations, items,True)


    def test_can_reach_magma_zone(self)->None:
        """Verify ability to access Magma Zone Overworld"""

        self.collect_by_name(["Cavern Zone & Magma Zone Unlock"])
        self.assertTrue(self.can_reach_region("Magma Zone - Overworld"))

    def test_can_not_reach_magman_zone(self)->None:
        """Verify inability to access Magma Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Magma Zone - Overworld"))

    def test_can_not_reach_magma_zone_with_everything_but_magma_zone_unlock(self)->None:
        """Verify inability to access Magma Zone Overworld without specific unlock"""
        self.collect_all_but(["Cavern Zone & Magma Zone Unlock"])
        self.assertFalse(self.can_reach_region("Magma Zone - Overworld"))

    def test_single_locations_reachable_with_magma_zone_unlock(self)->None:
        """Verify abillity to access Mime Jr. with magma zone and higher"""
        locations = ["Treehouse - Mime Jr."]
        items = [["Cavern Zone & Magma Zone Unlock"]]
        self.assertAccessDependency(locations, items,True)

    def test_can_reach_meadow_zone(self)->None:
        """Verify ability to access Meadow Zone Overworld"""
        self.assertTrue(self.can_reach_region("Meadow Zone - Overworld"))

class TestRegionAccessStartIceZone(PokeparkTest):
    options = {
        "starting_zone": 2
    }
    def test_can_reach_meadow_zone(self)->None:
        """Verify ability to access Meadow Zone Overworld"""
        self.collect_by_name("Meadow Zone Unlock")
        self.assertTrue(self.can_reach_region("Meadow Zone - Overworld"))

    def test_can_not_reach_meadow_zone(self)->None:
        """Verify inability to access Meadow Zone Overworld without unlock"""
        self.assertFalse(self.can_reach_region("Meadow Zone - Overworld"))

    def test_can_not_reach_meadow_zone_with_everything_but_meadow_zone_unlock(self)->None:
        """Verify inability to access Meadow Zone Overworld without specific unlock"""
        self.collect_all_but(["Meadow Zone Unlock"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Overworld"))

    def test_can_reach_ice_zone(self)->None:
        """Verify ability to access Ice Zone Overworld"""

        self.assertTrue(self.can_reach_region("Ice Zone - Overworld"))