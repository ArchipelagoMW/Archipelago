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
        locations = ["Meadow Zone - Overworld - Bonsly", "Meadow Zone - Overworld - Bonsly Friendship - Pokemon Unlock"]
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
        locations = ["Meadow Zone - Overworld - Caterpie",
                     "Meadow Zone - Overworld - Caterpie Friendship - Pokemon Unlock"]
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
        """Verify unlock conditions for accessing Ambipom """
        locations = ["Meadow Zone - Overworld - Ambipom",
                     "Haunted Zone - Overworld - Ambipom"]
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
        items = [["Starly Unlock"], ["Starly Unlock 2"]]
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
        locations = ["Beach Zone - Overworld - Mudkip", "Ice Zone - Overworld - Mudkip"]
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
        locations = ["Beach Zone - Overworld - Krabby", "Ice Zone - Overworld - Krabby"]
        items = [["Krabby Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_corphish_unlock(self) -> None:
        """Verify unlock conditions for accessing Corphish in Beach Zone Overworld"""
        locations = ["Beach Zone - Overworld - Corphish", "Ice Zone - Overworld - Lower Lift Region - Corphish"]
        items = [["Corphish Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_pikachu_balloon_unlock(self) -> None:
        """Verify unlock conditions for accessing Pikachu in Pelipper's Circle Circuit"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Pikachu",
                     "Granite Zone - Salamence's Sky Race - Pikachu"]
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

        locations = ["Ice Zone - Overworld - Primeape"]
        items = [["Primeape Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_ursaring_unlock(self) -> None:
        """Verify unlock conditions for accessing Delibird in Ice Zone Overworld"""

        locations = ["Ice Zone - Overworld - Ursaring"]
        items = [["Ursaring Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magnemite_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnemite 1 in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Magnemite"]
        items = [["Magnemite Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magnemite2_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnemite 2 in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Magnemite 2"]
        items = [["Magnemite Unlock 2"]]
        self.assertAccessDependency(locations, items)

    def test_magnemite3_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnemite 3 in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Magnemite 3"]
        items = [["Magnemite Unlock 3"]]
        self.assertAccessDependency(locations, items)

    def test_machamp_unlock(self) -> None:
        """Verify unlock conditions for accessing Battle Machamp in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Machamp - Battle"]
        items = [["Machamp Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_diglett_unlock(self) -> None:
        """Verify that Diglett Unlocks allows no new locations"""

        locations = []
        items = [["Diglett Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magnezone_unlock(self) -> None:
        """Verify unlock conditions for accessing Magnezone in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Magnezone"]
        items = [["Magnezone Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_phanpy_unlock(self) -> None:
        """Verify unlock conditions for accessing Phanpy in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Phanpy"]
        items = [["Phanpy Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_raichu_unlock(self) -> None:
        """Verify unlock conditions for accessing Raichu in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Raichu"]
        items = [["Raichu Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_hitmonlee_unlock(self) -> None:
        """Verify unlock conditions for accessing Hitmonlee in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Hitmonlee"]
        items = [["Hitmonlee Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_infernape_unlock(self) -> None:
        """Verify unlock conditions for accessing Infernape in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Infernape"]
        items = [["Infernape Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_ninetales_unlock(self) -> None:
        """Verify unlock conditions for accessing Ninetales in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Ninetales"]
        items = [["Ninetales Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_ponyta_unlock(self) -> None:
        """Verify unlock conditions for accessing Ponyta in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Ponyta"]
        items = [["Ponyta Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_torkoal_unlock(self) -> None:
        """Verify unlock conditions for accessing Torkoal in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Torkoal"]
        items = [["Torkoal Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_golem_unlock(self) -> None:
        """Verify unlock conditions for accessing Golem in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Golem"]
        items = [["Golem Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_baltoy_unlock(self) -> None:
        """Verify unlock conditions for accessing Baltoy in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Baltoy",
                     "Magma Zone - Overworld - Baltoy Friendship - Pokemon Unlock",
                     "Granite Zone - Overworld - Baltoy Friendship - Pokemon Unlock",
                     "Granite Zone - Overworld - Baltoy"]
        items = [["Baltoy Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_claydol_unlock(self) -> None:
        """Verify unlock conditions for accessing Claydol in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Claydol",
                     "Granite Zone - Overworld - Claydol"]
        items = [["Claydol Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_hitmonchan_unlock(self) -> None:
        """Verify unlock conditions for accessing Hitmonchan in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Hitmonchan",
                     "Magma Zone - Overworld - Hitmonchan Friendship - Pokemon Unlock"]
        items = [["Hitmonchan Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_honchkrow_unlock(self) -> None:
        """Verify unlock conditions for accessing Honchkrow in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Honchkrow"]
        items = [["Honchkrow Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_metapod_unlock(self) -> None:
        """Verify unlock conditions for accessing Metapod in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Metapod"]
        items = [["Metapod Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_kakuna_unlock(self) -> None:
        """Verify unlock conditions for accessing Kakuna in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Kakuna"]
        items = [["Kakuna Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_voltorb_unlock(self) -> None:
        """Verify unlock conditions for accessing Voltorb in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Voltorb"]
        items = [["Voltorb Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_elekid_unlock(self) -> None:
        """Verify unlock conditions for accessing Elekid in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Elekid",
                     "Haunted Zone - Overworld - Mansion - Elekid Friendship - Pokemon Unlock"]
        items = [["Elekid Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_electabuzz_unlock(self) -> None:
        """Verify unlock conditions for accessing Electabuzz in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Electabuzz"]
        items = [["Electabuzz Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_luxray_unlock(self) -> None:
        """Verify unlock conditions for accessing Luxray in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Luxray"]
        items = [["Luxray Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_stunky_unlock(self) -> None:
        """Verify unlock conditions for accessing Stunky in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Stunky",
                     "Haunted Zone - Overworld - Mansion - Stunky Friendship - Pokemon Unlock"]
        items = [["Stunky Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_skuntank_unlock(self) -> None:
        """Verify unlock conditions for accessing Skuntank in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Skuntank"]
        items = [["Skuntank Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_breloom_unlock(self) -> None:
        """Verify unlock conditions for accessing Breloom in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Breloom"]
        items = [["Breloom Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_mismagius_unlock(self) -> None:
        """Verify unlock conditions for accessing Mismagius in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Mismagius"]
        items = [["Mismagius Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_electrode_unlock(self) -> None:
        """Verify unlock conditions for accessing Electrode in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Electrode"]
        items = [["Electrode Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_haunter_unlock(self) -> None:
        """Verify unlock conditions for accessing Haunter in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Haunter"]
        items = [["Haunter Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_gastly_unlock(self) -> None:
        """Verify unlock conditions for accessing Gastly in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Gastly"]
        items = [["Gastly Unlock", "Gastly Unlock 2"]]
        self.assertAccessDependency(locations, items)

    def test_espeon_unlock(self) -> None:
        """Verify unlock conditions for accessing Espeon in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Espeon"]
        items = [["Espeon Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_gengar_unlock(self) -> None:
        """Verify unlock conditions for accessing Gengar in Haunted Zone Overworld"""

        locations = ["Haunted Zone - Overworld - Mansion - Gengar"]
        items = [["Gengar Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_blastoise_unlock(self) -> None:
        """Verify unlock conditions for accessing Blastoise in Beach Zone Overworld"""

        locations = ["Beach Zone - Overworld - Blastoise"]
        items = [["Blastoise Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_electivire_unlock(self) -> None:
        """Verify unlock conditions for accessing Electivire in Cavern Zone Overworld"""

        locations = ["Cavern Zone - Overworld - Electivire"]
        items = [["Electivire Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_magmortar_unlock(self) -> None:
        """Verify unlock conditions for accessing Magmortar in Magma Zone Overworld"""

        locations = ["Magma Zone - Overworld - Magmortar"]
        items = [["Magmortar Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_jolteon_unlock(self) -> None:
        """Verify unlock conditions for accessing Jolteon in Granite Zone Overworld"""

        locations = ["Granite Zone - Overworld - Jolteon"]
        items = [["Jolteon Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_aerodactyl_unlock(self) -> None:
        """Verify unlock conditions for accessing Aerodactyl in Granite Zone Overworld"""

        locations = ["Granite Zone - Overworld - Aerodactyl"]
        items = [["Aerodactyl Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_tyranitar_unlock(self) -> None:
        """Verify unlock conditions for accessing Tyranitar in Granite Zone Overworld"""

        locations = ["Granite Zone - Overworld - Tyranitar"]
        items = [["Tyranitar Unlock"]]
        self.assertAccessDependency(locations, items)

    def test_garchomp_unlock(self) -> None:
        """Verify unlock conditions for accessing Garchomp in Granite Zone Overworld"""

        locations = ["Granite Zone - Overworld - Garchomp"]
        items = [["Garchomp Unlock"]]
        self.assertAccessDependency(locations, items)


class TestRegionAccess(PokeparkTest):
    def test_can_reach_beach_zone(self) -> None:
        """Verify ability to access Beach Zone Overworld"""

        self.collect_by_name(["Beach Zone Unlock"])
        self.assertTrue(self.can_reach_region("Beach Zone - Overworld"))

    def test_can_not_reach_beach_zone(self) -> None:
        """Verify inability to access Beach Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Beach Zone - Overworld"))

    def test_can_not_reach_beach_zone_with_everything_but_beach_zone_unlock(self) -> None:
        """Verify inability to access Beach Zone Overworld without specific unlock"""
        self.collect_all_but(["Beach Zone Unlock"])
        self.assertFalse(self.can_reach_region("Beach Zone - Overworld"))

    def test_single_locations_reachable_with_beach_zone_unlock(self) -> None:
        """Verify abillity to access Health Power Upgrades"""
        locations = ["Treehouse - Health Upgrade 1", "Treehouse - Health Upgrade 2", "Treehouse - Health Upgrade 3"]
        items = [["Beach Zone Unlock"]]
        self.assertAccessDependency(locations, items, True)

    def test_can_reach_ice_zone(self) -> None:
        """Verify ability to access Ice Zone Overworld"""

        self.collect_by_name(["Ice Zone Unlock"])
        self.assertTrue(self.can_reach_region("Ice Zone - Overworld"))

    def test_can_not_reach_ice_zone(self) -> None:
        """Verify inability to access Ice Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Ice Zone - Overworld"))

    def test_can_not_reach_ice_zone_with_everything_but_ice_zone_unlock(self) -> None:
        """Verify inability to access Ice Zone Overworld without specific unlock"""
        self.collect_all_but(["Ice Zone Unlock"])
        self.assertFalse(self.can_reach_region("Ice Zone - Overworld"))

    def test_single_locations_reachable_with_ice_zone_unlock(self) -> None:
        """Verify abillity to access Iron Tail Power Upgrades with Ice Zone or higher"""
        locations = ["Treehouse - Iron Tail Upgrade 1", "Treehouse - Iron Tail Upgrade 2",
                     "Treehouse - Iron Tail Upgrade 3"]
        items = [["Ice Zone Unlock"], ["Cavern Zone & Magma Zone Unlock"], ["Haunted Zone Unlock"]]
        self.assertAccessDependency(locations, items, True)

    def test_can_reach_cavern_zone(self) -> None:
        """Verify ability to access Cavern Zone Overworld"""

        self.collect_by_name(["Cavern Zone & Magma Zone Unlock"])
        self.assertTrue(self.can_reach_region("Cavern Zone - Overworld"))

    def test_can_not_reach_cavern_zone(self) -> None:
        """Verify inability to access Cavern Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Cavern Zone - Overworld"))

    def test_can_not_reach_cavern_zone_with_everything_but_cavern_zone_unlock(self) -> None:
        """Verify inability to access Cavern Zone Overworld without specific unlock"""
        self.collect_all_but(["Cavern Zone & Magma Zone Unlock"])
        self.assertFalse(self.can_reach_region("Cavern Zone - Overworld"))

    def test_single_locations_reachable_with_cavern_zone_unlock(self) -> None:
        """Verify abillity to access Mime Jr. with cavern zone and higher"""
        locations = ["Treehouse - Mime Jr."]
        items = [["Cavern Zone & Magma Zone Unlock"],
                 ["Haunted Zone Unlock"],
                 ["Granite Zone & Flower Zone Unlock"],
                 ["Skygarden Unlock"]]
        self.assertAccessDependency(locations, items, True)

    def test_can_reach_magma_zone(self) -> None:
        """Verify ability to access Magma Zone Overworld"""

        self.collect_by_name(["Cavern Zone & Magma Zone Unlock"])
        self.assertTrue(self.can_reach_region("Magma Zone - Overworld"))

    def test_can_not_reach_magman_zone(self) -> None:
        """Verify inability to access Magma Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Magma Zone - Overworld"))

    def test_can_not_reach_magma_zone_with_everything_but_magma_zone_unlock(self) -> None:
        """Verify inability to access Magma Zone Overworld without specific unlock"""
        self.collect_all_but(["Cavern Zone & Magma Zone Unlock"])
        self.assertFalse(self.can_reach_region("Magma Zone - Overworld"))

    def test_single_locations_reachable_with_magma_zone_unlock(self) -> None:
        """Verify abillity to access Mime Jr. with magma zone and higher"""
        locations = ["Treehouse - Mime Jr."]
        items = [["Cavern Zone & Magma Zone Unlock"],
                 ["Haunted Zone Unlock"],
                 ["Granite Zone & Flower Zone Unlock"],
                 ["Skygarden Unlock"]]
        self.assertAccessDependency(locations, items, True)

    def test_can_reach_haunted_zone(self) -> None:
        """Verify ability to access Haunted Zone Overworld"""

        self.collect_by_name(["Haunted Zone Unlock"])
        self.assertTrue(self.can_reach_region("Haunted Zone - Overworld"))

    def test_can_not_reach_haunted_zone(self) -> None:
        """Verify inability to access Haunted Zone Overworld without unlock"""

        self.assertFalse(self.can_reach_region("Haunted Zone - Overworld"))

    def test_can_not_reach_haunted_zone_with_everything_but_haunted_zone_unlock(self) -> None:
        """Verify inability to access Magma Zone Overworld without specific unlock"""
        self.collect_all_but(["Haunted Zone Unlock"])
        self.assertFalse(self.can_reach_region("Haunted Zone - Overworld"))

    def test_can_reach_meadow_zone(self) -> None:
        """Verify ability to access Meadow Zone Overworld"""
        self.assertTrue(self.can_reach_region("Meadow Zone - Overworld"))

    def test_can_reach_dusknoir_minigame_with_dusknoir_unlock(self) -> None:
        """Verify abillity to access dusknoir minigame with dusknor unlock"""
        self.collect_by_name(["Haunted Zone Unlock"])
        self.collect_by_name(["Dusknoir Unlock"])
        self.assertTrue(self.can_reach_region("Haunted Zone - Mansion - Dusknoir's Speed Slam"))

    def test_can_not_reach_dusknoir_minigame_with_everything_but_dusknoir_unlock(self) -> None:
        """Verify inability to access Magma Zone Overworld without specific unlock"""
        self.collect_by_name(["Haunted Zone Unlock"])
        self.collect_all_but(["Dusknoir Unlock"])
        self.assertFalse(self.can_reach_region("Haunted Zone - Mansion - Dusknoir's Speed Slam"))

    def test_can_reach_granite_zone(self) -> None:
        """Verify ability to access Granite Zone Overworld"""
        self.collect(self.world.create_item("Granite Zone & Flower Zone Unlock"))
        self.assertTrue(self.can_reach_region("Granite Zone - Overworld"))

    def test_can_reach_not_granite_zone(self) -> None:
        """Verify inability to access Granite Zone Overworld without specific unlock"""

        self.assertFalse(self.can_reach_region("Granite Zone - Overworld"))

    def test_can_reach_flower_zone(self) -> None:
        """Verify ability to access Flower Zone Overworld"""
        self.collect(self.world.create_item("Granite Zone & Flower Zone Unlock"))
        self.assertTrue(self.can_reach_region("Flower Zone - Overworld"))

    def test_can_reach_not_flower_zone(self) -> None:
        """Verify inability to access Flower Zone Overworld without specific unlock"""

        self.assertFalse(self.can_reach_region("Flower Zone - Overworld"))

    def test_can_reach_rayquaza_minigame_with_dusknoir_unlock(self) -> None:
        """Verify abillity to access rayquaza minigame with rayquaza unlock"""
        self.collect_by_name(["Granite Zone & Flower Zone Unlock"])
        self.collect_by_name(["Rayquaza Unlock"])
        self.assertTrue(self.can_reach_region("Flower Zone - Rayquaza's Balloon Panic"))

    def test_can_not_reach_rayquaza_minigame_with_everything_but_rayquaza_unlock(self) -> None:
        """Verify inability to access Magma Zone Overworld without specific unlock"""
        self.collect_by_name(["Granite Zone & Flower Zone Unlock"])
        self.collect_all_but(["Rayquaza Unlock"])
        self.assertFalse(self.can_reach_region("Flower Zone - Rayquaza's Balloon Panic"))

    def test_can_reach_skygarden(self) -> None:
        """Verify ability to access Skygarden Overworld"""

        self.collect(self.world.create_item("Skygarden Unlock"))
        self.assertTrue(self.can_reach_region("Skygarden - Overworld"))

    def test_can_reach_not_skygarden(self) -> None:
        """Verify inability to access Skygarden Overworld without specific unlock"""

        self.assertFalse(self.can_reach_region("Skygarden - Overworld"))


class TestRegionAccessStartIceZone(PokeparkTest):
    options = {
        "starting_zone": 2
    }

    def test_can_reach_meadow_zone(self) -> None:
        """Verify ability to access Meadow Zone Overworld"""
        self.collect_by_name("Meadow Zone Unlock")
        self.assertTrue(self.can_reach_region("Meadow Zone - Overworld"))

    def test_can_not_reach_meadow_zone(self) -> None:
        """Verify inability to access Meadow Zone Overworld without unlock"""
        self.assertFalse(self.can_reach_region("Meadow Zone - Overworld"))

    def test_can_not_reach_meadow_zone_with_everything_but_meadow_zone_unlock(self) -> None:
        """Verify inability to access Meadow Zone Overworld without specific unlock"""
        self.collect_all_but(["Meadow Zone Unlock"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Overworld"))

    def test_can_reach_ice_zone(self) -> None:
        """Verify ability to access Ice Zone Overworld"""

        self.assertTrue(self.can_reach_region("Ice Zone - Overworld"))
