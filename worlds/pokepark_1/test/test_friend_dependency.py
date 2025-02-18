from . import PokeparkTest

class TestPokemonFriendshipDependencies(PokeparkTest):
    def test_chikorita(self)->None:
        """Test locations and minigames that require Chikorita"""
        locations = []
        items = [["Chikorita"]]
        self.assertAccessDependency(locations,items)

    def test_pachirisu(self) -> None:
        """Test locations and minigames that require Pachirisu"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Pachirisu","Meadow Zone - Venusaur's Vine Swing - Pachirisu"]
        items = [["Pachirisu"]]
        self.assertAccessDependency(locations, items)

    def test_bulbasaur(self) -> None:
        """Test locations and minigames that require Bulbasaur"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bulbasaur"]
        items = [["Bulbasaur"]]
        self.assertAccessDependency(locations, items)

    def test_munchlax(self)->None:
        """Test locations and minigames that require Munchlax"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Munchlax","Meadow Zone - Venusaur's Vine Swing - Munchlax"]
        items = [["Munchlax"]]
        self.assertAccessDependency(locations,items)

    def test_tropius(self)->None:
        """Test locations and minigames that require Tropius"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Tropius"]
        items = [["Tropius"]]
        self.assertAccessDependency(locations,items)

    def test_turtwig(self)->None:
        """Test locations and minigames that require Turtwig"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Turtwig"]
        items = [["Turtwig"]]
        self.assertAccessDependency(locations,items)

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
        items = [["Mankey"]]
        self.assertAccessDependency(locations, items)

    def test_spearow(self) -> None:
        """Test locations and minigames that require Spearow"""
        locations= ["Beach Zone - Pelipper's Circle Circuit - Spearow"]
        items = [["Spearow"]]
        self.assertAccessDependency(locations, items)

    def test_croagunk(self) -> None:
        """Test locations and minigames that require Croagunk"""

        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Croagunk","Meadow Zone - Venusaur's Vine Swing - Croagunk"]
        items = [["Croagunk"]]
        self.assertAccessDependency(locations, items)

    def test_chatot(self) -> None:
        """Test locations and minigames that require Chatot"""
        locations = []
        items = [["Chatot"]]
        self.assertAccessDependency(locations, items)

    def test_lotad(self) -> None:
        """Test locations and minigames that require Lotad"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Lotad","Beach Zone - Gyarados' Aqua Dash - Lotad"]
        items = [["Lotad"]]
        self.assertAccessDependency(locations, items)

    def test_treecko(self) -> None:
        """Test locations and minigames that require Treecko"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Treecko","Meadow Zone - Venusaur's Vine Swing - Treecko"]
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
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Chimchar","Meadow Zone - Venusaur's Vine Swing - Chimchar"]
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
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Magikarp","Meadow Zone - Venusaur's Vine Swing - Magikarp"]
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
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bibarel","Beach Zone - Gyarados' Aqua Dash - Bibarel"]
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
        locations = ["Beach Zone - Gyarados' Aqua Dash - Piplup"]
        items = [["Piplup"]]
        self.assertAccessDependency(locations, items)

# Region access tests
    def test_can_reach_venusaur_minigame(self)->None:
        """Verify access to Venusaur's Vine Swing minigame with Spearow and Croagunk"""

        self.collect_by_name(["Spearow","Croagunk"])
        self.assertTrue(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))


    def test_can_not_reach_venusaur_minigame_only_croagunk(self)->None:
        """Verify inability to access Venusaur's Vine Swing with only Croagunk"""

        self.collect_by_name(["Croagunk"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))

    def test_can_not_reach_venusaur_minigame_only_spearow(self)->None:
        """Verify inability to access Venusaur's Vine Swing with only Spearow"""

        self.collect_by_name(["Spearow"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))

    def test_can_not_reach_venusaur_minigame_without_spearow_and_croagunk(self)->None:
        """Verify inability to access Venusaur's Vine Swing without Spearow and Croagunk"""

        self.collect_all_but(["Spearow","Croagunk","Beach Zone Unlock"])
        self.assertFalse(self.can_reach_region("Meadow Zone - Venusaur's Vine Swing"))

