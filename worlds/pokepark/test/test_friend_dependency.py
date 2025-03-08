from . import PokeparkTest


class TestPokemonFriendshipDependencies(PokeparkTest):
    def test_chikorita(self) -> None:
        """Test locations and minigames that require Chikorita"""
        locations = []
        items = [["Chikorita"]]
        self.assertAccessDependency(locations, items)

    def test_pachirisu(self) -> None:
        """Test locations and minigames that require Pachirisu"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Pachirisu",
                     "Meadow Zone - Venusaur's Vine Swing - Pachirisu"]
        items = [["Pachirisu"]]
        self.assertAccessDependency(locations, items)

    def test_bulbasaur(self) -> None:
        """Test locations and minigames that require Bulbasaur"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bulbasaur"]
        items = [["Bulbasaur"]]
        self.assertAccessDependency(locations, items)

    def test_munchlax(self) -> None:
        """Test locations and minigames that require Munchlax"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Munchlax",
                     "Meadow Zone - Venusaur's Vine Swing - Munchlax"]
        items = [["Munchlax"]]
        self.assertAccessDependency(locations, items)

    def test_tropius(self) -> None:
        """Test locations and minigames that require Tropius"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Tropius"]
        items = [["Tropius"]]
        self.assertAccessDependency(locations, items)

    def test_turtwig(self) -> None:
        """Test locations and minigames that require Turtwig"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Turtwig"]
        items = [["Turtwig"]]
        self.assertAccessDependency(locations, items)

    def test_bonsly(self) -> None:
        """Test locations and minigames that require Bonsly"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bonsly"]
        items = [["Bonsly"]]
        self.assertAccessDependency(locations, items)

    def test_sudowoodo(self) -> None:
        """Test locations and minigames that require Sudowoodo"""
        locations = []
        items = [["Sudowoodo"]]
        self.assertAccessDependency(locations, items)

    def test_buneary(self) -> None:
        """Test locations and minigames that require Buneary"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Buneary"]
        items = [["Buneary"]]
        self.assertAccessDependency(locations, items)

    def test_shinx(self) -> None:
        """Test locations and minigames that require Shinx"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Shinx"]
        items = [["Shinx"]]
        self.assertAccessDependency(locations, items)

    def test_mankey(self) -> None:
        """Test locations and minigames that require Mankey"""
        locations = [f"Meadow Zone - Overworld - Bidoof Housing {i}{suffix}"
                     for i in range(1, 5)
                     for suffix in ["", " - Pokemon Unlock"]]
        locations.append("Meadow Zone - Venusaur's Vine Swing - Mankey")
        locations.append("Meadow Zone - Overworld - Bidoof")
        items = [["Mankey"]]
        self.assertAccessDependency(locations, items)

    def test_spearow(self) -> None:
        """Test locations and minigames that require Spearow"""
        venusaur_minigame_pokemon_names = [
            "Prisma",
            "Aipom",
            "Ambipom",
            # "Blaziken",
            "Chimchar",
            "Croagunk",
            # "Infernape",
            # "Lucario",
            "Magikarp",
            "Mankey",
            "Munchlax",
            "Pachirisu",
            "Pikachu",
            "Primeape",
            # "Tangrowth",
            "Treecko",
        ]
        locations = [f"Meadow Zone - Venusaur's Vine Swing - {suffix}"
                     for suffix in venusaur_minigame_pokemon_names]
        locations.append("Beach Zone - Pelipper's Circle Circuit - Spearow")
        items = [["Spearow"]]
        self.assertAccessDependency(locations, items)

    def test_croagunk(self) -> None:
        """Test locations and minigames that require Croagunk"""
        venusaur_minigame_pokemon_names = [
            "Prisma",
            "Aipom",
            "Ambipom",
            # "Blaziken",
            "Chimchar",
            "Croagunk",
            # "Infernape",
            # "Lucario",
            "Magikarp",
            "Mankey",
            "Munchlax",
            "Pachirisu",
            "Pikachu",
            "Primeape",
            # "Tangrowth",
            "Treecko",
        ]
        locations = [f"Meadow Zone - Venusaur's Vine Swing - {suffix}"
                     for suffix in venusaur_minigame_pokemon_names]
        locations.append("Meadow Zone - Bulbasaur's Daring Dash Minigame - Croagunk")
        locations.append("Meadow Zone - Venusaur's Vine Swing - Croagunk")
        items = [["Croagunk"]]
        self.assertAccessDependency(locations, items)

    def test_chatot(self) -> None:
        """Test locations and minigames that require Chatot"""
        locations = []
        items = [["Chatot"]]
        self.assertAccessDependency(locations, items)

    def test_lotad(self) -> None:
        """Test locations and minigames that require Lotad"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Lotad",
                     "Beach Zone - Gyarados' Aqua Dash - Lotad"]
        items = [["Lotad"]]
        self.assertAccessDependency(locations, items)

    def test_treecko(self) -> None:
        """Test locations and minigames that require Treecko"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Treecko",
                     "Meadow Zone - Venusaur's Vine Swing - Treecko"]
        items = [["Treecko"]]
        self.assertAccessDependency(locations, items)

    def test_caterpie(self) -> None:
        """Test locations and minigames that require Caterpie"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Caterpie"]
        items = [["Caterpie"]]
        self.assertAccessDependency(locations, items)

    def test_butterfree(self) -> None:
        """Test locations and minigames that require Butterfree"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Butterfree"]
        items = [["Butterfree"]]
        self.assertAccessDependency(locations, items)

    def test_chimchar(self) -> None:
        """Test locations and minigames that require Chimchar"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Chimchar",
                     "Meadow Zone - Venusaur's Vine Swing - Chimchar"]
        items = [["Chimchar"]]
        self.assertAccessDependency(locations, items)

    def test_aipom(self) -> None:
        """Test locations and minigames that require Aipom"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Aipom"]
        items = [["Aipom"]]
        self.assertAccessDependency(locations, items)

    def test_ambipom(self) -> None:
        """Test locations and minigames that require Ambipom"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Ambipom"]
        items = [["Ambipom"]]
        self.assertAccessDependency(locations, items)

    def test_weedle(self) -> None:
        """Test locations and minigames that require Weedle"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Weedle"]
        items = [["Weedle"]]
        self.assertAccessDependency(locations, items)

    def test_shroomish(self) -> None:
        """Test locations and minigames that require Shroomish"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Shroomish"]
        items = [["Shroomish"]]
        self.assertAccessDependency(locations, items)

    def test_magikarp(self) -> None:
        """Test locations and minigames that require Magikarp"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Magikarp",
                     "Meadow Zone - Venusaur's Vine Swing - Magikarp", "Ice Zone - Empoleon's Snow Slide - Magikarp"]
        items = [["Magikarp"]]
        self.assertAccessDependency(locations, items)

    def test_oddish(self) -> None:
        """Test locations and minigames that require Oddish"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Oddish"]
        items = [["Oddish"]]
        self.assertAccessDependency(locations, items)

    def test_leafeon(self) -> None:
        """Test locations and minigames that require Leafeon"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Leafeon"]
        items = [["Leafeon"]]
        self.assertAccessDependency(locations, items)

    def test_bidoof(self) -> None:
        """Test locations and minigames that require Bidoof"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bidoof"]
        items = [["Bidoof"]]
        self.assertAccessDependency(locations, items)

    def test_bibarel(self) -> None:
        """Test locations and minigames that require Bibarel"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bibarel",
                     "Beach Zone - Gyarados' Aqua Dash - Bibarel"]
        items = [["Bibarel"]]
        self.assertAccessDependency(locations, items)

    def test_torterra(self) -> None:
        """Test locations and minigames that require Torterra"""
        locations = []
        items = [["Torterra"]]
        self.assertAccessDependency(locations, items)

    def test_starly(self) -> None:
        """Test locations and minigames that require Starly"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Starly"]
        items = [["Starly"]]
        self.assertAccessDependency(locations, items)

    def test_scyther(self) -> None:
        """Test locations and minigames that require Scyther"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Scyther"]
        items = [["Scyther"]]
        self.assertAccessDependency(locations, items)

    def test_buizel(self) -> None:
        """Test locations and minigames that require Buizel"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Buizel"]
        items = [["Buizel"]]
        self.assertAccessDependency(locations, items)

    def test_psyduck(self) -> None:
        """Test locations and minigames that require Psyduck"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Psyduck"]
        items = [["Psyduck"]]
        self.assertAccessDependency(locations, items)

    def test_slowpoke(self) -> None:
        """Test locations and minigames that require Slowpoke"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Slowpoke"]
        items = [["Slowpoke"]]
        self.assertAccessDependency(locations, items)

    def test_azurill(self) -> None:
        """Test locations and minigames that require Azurill"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Azurill"]
        items = [["Azurill"]]
        self.assertAccessDependency(locations, items)

    def test_totodile(self) -> None:
        """Test locations and minigames that require Totodile"""
        locations = []
        items = [["Totodile"]]
        self.assertAccessDependency(locations, items)

    def test_mudkip(self) -> None:
        """Test locations and minigames that require Mudkip"""
        locations = []
        items = [["Mudkip"]]
        self.assertAccessDependency(locations, items)

    def test_pidgeotto(self) -> None:
        """Test locations and minigames that require Pidgeotto"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Pidgeotto"]
        items = [["Pidgeotto"]]
        self.assertAccessDependency(locations, items)

    def test_taillow(self) -> None:
        """Test locations and minigames that require Taillow"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Taillow"]
        items = [["Taillow"]]
        self.assertAccessDependency(locations, items)

    def test_wingull(self) -> None:
        """Test locations and minigames that require Wingull"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Wingull"]
        items = [["Wingull"]]
        self.assertAccessDependency(locations, items)

    def test_staravia(self) -> None:
        """Test locations and minigames that require Staravia"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Staravia"]
        items = [["Staravia"]]
        self.assertAccessDependency(locations, items)

    def test_corsola(self) -> None:
        """Test locations and minigames that require Corsola"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Corsola"]
        items = [["Corsola"]]
        self.assertAccessDependency(locations, items)

    def test_floatzel(self) -> None:
        """Test locations and minigames that require Floatzel"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Floatzel"]
        items = [["Floatzel"]]
        self.assertAccessDependency(locations, items)

    def test_vaporeon(self) -> None:
        """Test locations and minigames that require Vaporeon"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Vaporeon"]
        items = [["Vaporeon"]]
        self.assertAccessDependency(locations, items)

    def test_golduck(self) -> None:
        """Test locations and minigames that require Golduck"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Golduck"]
        items = [["Golduck"]]
        self.assertAccessDependency(locations, items)

    def test_pelipper(self) -> None:
        """Test locations and minigames that require Pelipper"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Pelipper"]
        items = [["Pelipper"]]
        self.assertAccessDependency(locations, items)

    def test_sharpedo(self) -> None:
        """Test locations and minigames that require Sharpedo"""
        locations = []
        items = [["Sharpedo"]]
        self.assertAccessDependency(locations, items)

    def test_wynaut(self) -> None:
        """Test locations and minigames that require Wynaut"""
        locations = []
        items = [["Wynaut"]]
        self.assertAccessDependency(locations, items)

    def test_carvanha(self) -> None:
        """Test locations and minigames that require Carvanha"""
        locations = []
        items = [["Carvanha"]]
        self.assertAccessDependency(locations, items)

    def test_krabby(self) -> None:
        """Test locations and minigames that require Krabby"""
        locations = []
        items = [["Krabby"]]
        self.assertAccessDependency(locations, items)

    def test_wailord(self) -> None:
        """Test locations and minigames that require Wailord"""
        locations = []
        items = [["Wailord"]]
        self.assertAccessDependency(locations, items)

    def test_corphish(self) -> None:
        """Test locations and minigames that require Corphish"""
        locations = []
        items = [["Corphish"]]
        self.assertAccessDependency(locations, items)

    def test_gyarados(self) -> None:
        """Test locations and minigames that require Gyarados"""
        locations = []
        items = [["Gyarados"]]
        self.assertAccessDependency(locations, items)

    def test_feraligatr(self) -> None:
        """Test locations and minigames that require Feraligatr"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Feraligatr"]
        items = [["Feraligatr"]]
        self.assertAccessDependency(locations, items)

    def test_piplup(self) -> None:
        """Test locations and minigames that require Piplup"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Piplup", "Ice Zone - Empoleon's Snow Slide - Piplup"]
        items = [["Piplup"]]
        self.assertAccessDependency(locations, items)

    def test_burmy(self) -> None:
        """Test locations and minigames that require Burmy"""
        locations = []
        items = [["Burmy"]]
        self.assertAccessDependency(locations, items)
    def test_drifblim(self) -> None:
        """Test locations and minigames that require Drifblim"""
        locations = []
        items = [["Drifblim"]]
        self.assertAccessDependency(locations, items)
    def test_lapras(self) -> None:
        """Test locations and minigames that require Lapras"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Lapras"]
        items = [["Lapras"]]
        self.assertAccessDependency(locations, items)

    def test_spheal(self) -> None:
        """Test locations and minigames that require Spheal"""
        locations = [f"Ice Zone - Overworld - Christmas Tree Present {i}"
                     for i in range(1, 5)]
        locations.append("Ice Zone - Overworld - Delibird")
        locations.append("Ice Zone - Overworld - Kirlia")
        locations.append("Ice Zone - Empoleon's Snow Slide - Spheal")
        items = [["Spheal"]]
        self.assertAccessDependency(locations, items)

    def test_octillery(self) -> None:
        """Test locations and minigames that require Octillery"""
        locations = []
        items = [["Octillery"]]
        self.assertAccessDependency(locations, items)

    def test_teddiursa(self) -> None:
        """Test locations and minigames that require Teddiursa"""
        locations = ["Ice Zone - Overworld - Christmas Tree Present 2",
                     "Ice Zone - Overworld - Christmas Tree Present 3",
                     "Ice Zone - Overworld - Christmas Tree Present 4", "Ice Zone - Overworld - Delibird",
                     "Ice Zone - Overworld - Kirlia", "Ice Zone - Empoleon's Snow Slide - Teddiursa"]
        items = [["Teddiursa"]]
        self.assertAccessDependency(locations, items)

    def test_delibird(self) -> None:
        """Test locations and minigames that require Delibird"""
        locations = ["Ice Zone - Overworld - Kirlia", "Ice Zone - Empoleon's Snow Slide - Delibird"]
        items = [["Delibird"]]
        self.assertAccessDependency(locations, items)

    def test_smoochum(self) -> None:
        """Test locations and minigames that require Smoochum"""
        locations = ["Ice Zone - Overworld - Christmas Tree Present 4", "Ice Zone - Overworld - Delibird",
                     "Ice Zone - Overworld - Kirlia"]
        items = [["Smoochum"]]
        self.assertAccessDependency(locations, items)

    def test_squirtle(self) -> None:
        """Test locations and minigames that require Squirtle"""
        locations = ["Ice Zone - Overworld - Christmas Tree Present 3", "Ice Zone - Overworld - Delibird",
                     "Ice Zone - Overworld - Kirlia", "Ice Zone - Overworld - Christmas Tree Present 4",
                     "Ice Zone - Empoleon's Snow Slide - Squirtle"]
        items = [["Squirtle"]]
        self.assertAccessDependency(locations, items)
    def test_glaceon(self) -> None:
        """Test locations and minigames that require Glaceon"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Glaceon"]
        items = [["Glaceon"]]
        self.assertAccessDependency(locations, items)
    def test_prinplup(self) -> None:
        """Test locations and minigames that require Prinplup"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Prinplup",
                     "Beach Zone - Gyarados' Aqua Dash - Prinplup",
                     "Ice Zone - Overworld - Lower Lift Region - Corphish",
                     "Ice Zone - Overworld - Lower Lift Region - Wingull",
                     "Ice Zone - Overworld - Lower Lift Region - Quagsire"]
        items = [["Prinplup"]]
        self.assertAccessDependency(locations, items)
    def test_sneasel(self) -> None:
        """Test locations and minigames that require Sneasel"""
        locations = []
        items = [["Sneasel"]]
        self.assertAccessDependency(locations, items)

    def test_piloswine(self) -> None:
        """Test locations and minigames that require Piloswine"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Piloswine"]
        items = [["Piloswine"]]
        self.assertAccessDependency(locations, items)

    def test_glalie(self) -> None:
        """Test locations and minigames that require Glalie"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Glalie"]
        items = [["Glalie"]]
        self.assertAccessDependency(locations, items)
    def test_primeape(self) -> None:
        """Test locations and minigames that require Primeape"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Primeape"]
        items = [["Primeape"]]
        self.assertAccessDependency(locations, items)

    def test_ursaring(self) -> None:
        """Test locations and minigames that require Ursaring"""
        locations = []
        items = [["Ursaring"]]
        self.assertAccessDependency(locations, items)
    def test_mamoswine(self) -> None:
        """Test locations and minigames that require Mamoswine"""
        locations = []
        items = [["Mamoswine"]]
        self.assertAccessDependency(locations, items)
    def test_kirlia(self) -> None:
        """Test locations and minigames that require Kirlia"""
        locations = []
        items = [["Kirlia"]]
        self.assertAccessDependency(locations, items)

    def test_quagsire(self) -> None:
        """Test locations and minigames that require Quagsire"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Quagsire"]
        items = [["Quagsire"]]
        self.assertAccessDependency(locations, items)
    def test_empoleon(self) -> None:
        """Test locations and minigames that require Empoleon"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Empoleon", "Ice Zone - Empoleon's Snow Slide - Empoleon"]
        items = [["Empoleon"]]
        self.assertAccessDependency(locations, items)

class TestRegionAccessByFriendship(PokeparkTest):

    # Region access tests
    def test_can_reach_venusaur_minigame(self) -> None:
        """Verify access to Venusaur's Vine Swing minigame with Spearow and Croagunk"""

        self.collect_by_name(["Spearow", "Croagunk"])
        self.assertTrue(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))

    def test_can_not_reach_venusaur_minigame_only_croagunk(self) -> None:
        """Verify inability to access Venusaur's Vine Swing with only Croagunk"""

        self.collect_by_name(["Croagunk"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))

    def test_can_not_reach_venusaur_minigame_only_spearow(self) -> None:
        """Verify inability to access Venusaur's Vine Swing with only Spearow"""

        self.collect_by_name(["Spearow"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))

    def test_can_not_reach_venusaur_minigame_without_spearow_and_croagunk(self) -> None:
        """Verify inability to access Venusaur's Vine Swing without Spearow and Croagunk"""

        self.collect_all_but(["Spearow", "Croagunk", "Beach Zone Unlock"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))


    def test_can_reach_ice_zone_lower_lift_with_prinplup(self)-> None:
        """Verify ability to access Ice Zone Lower Lift Region with Prinplup"""

        self.collect_by_name(["Prinplup", "Ice Zone Unlock"])
        self.assertTrue(self.can_reach_region("Ice Zone - Overworld - Lower Lift Region"))

    def test_can_not_reach_ice_zone_lower_lift_without_prinplup(self)-> None:
        """Verify inability to access Ice Zone Lower Lift Region without Prinplup"""

        self.collect_all_but(["Prinplup"])
        self.assertFalse(self.can_reach_region("Ice Zone - Overworld - Lower Lift Region"))