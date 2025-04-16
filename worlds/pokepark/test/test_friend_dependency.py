from . import PokeparkTest


class TestPokemonFriendshipDependencies(PokeparkTest):

    def test_chikorita(self) -> None:
        """Test locations and minigames that require Chikorita"""
        locations = [

            "Flower Zone - Rayquaza's Balloon Panic - Chikorita",
            "Granite Zone - Absol's Hurdle Bounce - Chikorita"]
        items = [["Chikorita"]]
        self.assertAccessDependency(locations, items)

    def test_pachirisu(self) -> None:
        """Test locations and minigames that require Pachirisu"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Pachirisu",
                     "Meadow Zone - Venusaur's Vine Swing - Pachirisu",

                     ]
        items = [["Pachirisu"]]
        self.assertAccessDependency(locations, items)

    def test_bulbasaur(self) -> None:
        """Test locations and minigames that require Bulbasaur"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bulbasaur",

                     ]
        items = [["Bulbasaur"]]
        self.assertAccessDependency(locations, items)

    def test_munchlax(self) -> None:
        """Test locations and minigames that require Munchlax"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Munchlax",
                     "Meadow Zone - Venusaur's Vine Swing - Munchlax",

                     ]
        items = [["Munchlax"]]
        self.assertAccessDependency(locations, items)

    def test_tropius(self) -> None:
        """Test locations and minigames that require Tropius"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Tropius",

                     ]
        items = [["Tropius"]]
        self.assertAccessDependency(locations, items)

    def test_turtwig(self) -> None:
        """Test locations and minigames that require Turtwig"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Turtwig",
                     ]
        items = [["Turtwig"]]
        self.assertAccessDependency(locations, items)

    def test_bonsly(self) -> None:
        """Test locations and minigames that require Bonsly"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bonsly",
                     "Magma Zone - Rhyperior's Bumper Burn - Bonsly",

                     ]
        items = [["Bonsly"]]
        self.assertAccessDependency(locations, items)

    def test_sudowoodo(self) -> None:
        """Test locations and minigames that require Sudowoodo"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Sudowoodo",

                     ]
        items = [["Sudowoodo"]]
        self.assertAccessDependency(locations, items)

    def test_buneary(self) -> None:
        """Test locations and minigames that require Buneary"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Buneary",
                     ]
        items = [["Buneary"]]
        self.assertAccessDependency(locations, items)

    def test_shinx(self) -> None:
        """Test locations and minigames that require Shinx"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Shinx",
                     ]
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
            "Blaziken",
            "Chimchar",
            "Croagunk",
            "Infernape",
            "Lucario",
            "Magikarp",
            "Mankey",
            "Munchlax",
            "Pachirisu",
            "Pikachu",
            "Primeape",
            "Tangrowth",
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
            "Blaziken",
            "Chimchar",
            "Croagunk",
            "Infernape",
            "Lucario",
            "Magikarp",
            "Mankey",
            "Munchlax",
            "Pachirisu",
            "Pikachu",
            "Primeape",
            "Tangrowth",
            "Treecko",
        ]
        locations = [f"Meadow Zone - Venusaur's Vine Swing - {suffix}"
                     for suffix in venusaur_minigame_pokemon_names]
        locations.append("Meadow Zone - Bulbasaur's Daring Dash Minigame - Croagunk")
        locations.append("Meadow Zone - Venusaur's Vine Swing - Croagunk")
        locations.append("Haunted Zone - Tangrowth's Swing-Along - Croagunk")
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
                     "Beach Zone - Gyarados' Aqua Dash - Lotad",

                     ]
        items = [["Lotad"]]
        self.assertAccessDependency(locations, items)

    def test_treecko(self) -> None:
        """Test locations and minigames that require Treecko"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Treecko",
                     "Meadow Zone - Venusaur's Vine Swing - Treecko",

                     ]
        items = [["Treecko"]]
        self.assertAccessDependency(locations, items)

    def test_caterpie(self) -> None:
        """Test locations and minigames that require Caterpie"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Caterpie",
                     ]
        items = [["Caterpie"]]
        self.assertAccessDependency(locations, items)

    def test_butterfree(self) -> None:
        """Test locations and minigames that require Butterfree"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Butterfree",

                     ]
        items = [["Butterfree"]]
        self.assertAccessDependency(locations, items)

    def test_chimchar(self) -> None:
        """Test locations and minigames that require Chimchar"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Chimchar",
                     "Meadow Zone - Venusaur's Vine Swing - Chimchar",
                     "Cavern Zone - Bastiodon's Panel Crush - Chimchar",
                     "Haunted Zone - Tangrowth's Swing-Along - Chimchar",

                     ]
        items = [["Chimchar"]]
        self.assertAccessDependency(locations, items)

    def test_aipom(self) -> None:
        """Test locations and minigames that require Aipom"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Aipom",
                     "Haunted Zone - Tangrowth's Swing-Along - Aipom",

                     ]
        items = [["Aipom"]]
        self.assertAccessDependency(locations, items)

    def test_ambipom(self) -> None:
        """Test locations and minigames that require Ambipom"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Ambipom",
                     "Haunted Zone - Tangrowth's Swing-Along - Ambipom",

                     ]
        items = [["Ambipom"]]
        self.assertAccessDependency(locations, items)

    def test_weedle(self) -> None:
        """Test locations and minigames that require Weedle"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Weedle",
                     ]
        items = [["Weedle"]]
        self.assertAccessDependency(locations, items)

    def test_shroomish(self) -> None:
        """Test locations and minigames that require Shroomish"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Shroomish",
                     ]
        items = [["Shroomish"]]
        self.assertAccessDependency(locations, items)

    def test_magikarp(self) -> None:
        """Test locations and minigames that require Magikarp"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Magikarp",
                     "Meadow Zone - Venusaur's Vine Swing - Magikarp",
                     "Ice Zone - Empoleon's Snow Slide - Magikarp",

                     ]
        items = [["Magikarp"]]
        self.assertAccessDependency(locations, items)

    def test_oddish(self) -> None:
        """Test locations and minigames that require Oddish"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Oddish",
                     ]
        items = [["Oddish"]]
        self.assertAccessDependency(locations, items)

    def test_leafeon(self) -> None:
        """Test locations and minigames that require Leafeon"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Leafeon",
                     ]
        items = [["Leafeon"]]
        self.assertAccessDependency(locations, items)

    def test_bidoof(self) -> None:
        """Test locations and minigames that require Bidoof"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bidoof",
                     ]
        items = [["Bidoof"]]
        self.assertAccessDependency(locations, items)

    def test_bibarel(self) -> None:
        """Test locations and minigames that require Bibarel"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Bibarel",
                     "Beach Zone - Gyarados' Aqua Dash - Bibarel",

                     ]
        items = [["Bibarel"]]
        self.assertAccessDependency(locations, items)

    def test_torterra(self) -> None:
        """Test locations and minigames that require Torterra"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Torterra",

                     ]
        items = [["Torterra"]]
        self.assertAccessDependency(locations, items)

    def test_venusaur(self) -> None:
        """Test locations and minigames that require Venusaur"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Venusaur",

                     ]
        items = [["Venusaur"]]
        self.assertAccessDependency(locations, items)

    def test_starly(self) -> None:
        """Test locations and minigames that require Starly"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Starly",

                     ]
        items = [["Starly"]]
        self.assertAccessDependency(locations, items)

    def test_scyther(self) -> None:
        """Test locations and minigames that require Scyther"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Scyther",
                     ]
        items = [["Scyther"]]
        self.assertAccessDependency(locations, items)

    def test_buizel(self) -> None:
        """Test locations and minigames that require Buizel"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Buizel",

                     ]
        items = [["Buizel"]]
        self.assertAccessDependency(locations, items)

    def test_psyduck(self) -> None:
        """Test locations and minigames that require Psyduck"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Psyduck",

                     ]
        items = [["Psyduck"]]
        self.assertAccessDependency(locations, items)

    def test_slowpoke(self) -> None:
        """Test locations and minigames that require Slowpoke"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Slowpoke",

                     ]
        items = [["Slowpoke"]]
        self.assertAccessDependency(locations, items)

    def test_azurill(self) -> None:
        """Test locations and minigames that require Azurill"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Azurill",

                     ]
        items = [["Azurill"]]
        self.assertAccessDependency(locations, items)

    def test_totodile(self) -> None:
        """Test locations and minigames that require Totodile"""
        locations = [
            "Flower Zone - Rayquaza's Balloon Panic - Totodile",
        ]
        items = [["Totodile"]]
        self.assertAccessDependency(locations, items)

    def test_mudkip(self) -> None:
        """Test locations and minigames that require Mudkip"""
        locations = []
        items = [["Mudkip"]]
        self.assertAccessDependency(locations, items)

    def test_pidgeotto(self) -> None:
        """Test locations and minigames that require Pidgeotto"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Pidgeotto",

                     "Granite Zone - Salamence's Sky Race - Pidgeotto",
                     ]
        items = [["Pidgeotto"]]
        self.assertAccessDependency(locations, items)

    def test_taillow(self) -> None:
        """Test locations and minigames that require Taillow"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Taillow",

                     "Granite Zone - Salamence's Sky Race - Taillow",
                     ]
        items = [["Taillow"]]
        self.assertAccessDependency(locations, items)

    def test_wingull(self) -> None:
        """Test locations and minigames that require Wingull"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Wingull",

                     ]
        items = [["Wingull"]]
        self.assertAccessDependency(locations, items)

    def test_staravia(self) -> None:
        """Test locations and minigames that require Staravia"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Staravia",

                     ]
        items = [["Staravia"]]
        self.assertAccessDependency(locations, items)

    def test_corsola(self) -> None:
        """Test locations and minigames that require Corsola"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Corsola",

                     ]
        items = [["Corsola"]]
        self.assertAccessDependency(locations, items)

    def test_floatzel(self) -> None:
        """Test locations and minigames that require Floatzel"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Floatzel",

                     "Flower Zone - Rayquaza's Balloon Panic - Floatzel",
                     ]
        items = [["Floatzel"]]
        self.assertAccessDependency(locations, items)

    def test_vaporeon(self) -> None:
        """Test locations and minigames that require Vaporeon"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Vaporeon",

                     ]
        items = [["Vaporeon"]]
        self.assertAccessDependency(locations, items)

    def test_golduck(self) -> None:
        """Test locations and minigames that require Golduck"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Golduck",

                     ]
        items = [["Golduck"]]
        self.assertAccessDependency(locations, items)

    def test_pelipper(self) -> None:
        """Test locations and minigames that require Pelipper"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Pelipper",

                     ]
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
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Krabby",

                     ]
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
        locations = ["Beach Zone - Gyarados' Aqua Dash - Feraligatr",

                     ]
        items = [["Feraligatr"]]
        self.assertAccessDependency(locations, items)

    def test_piplup(self) -> None:
        """Test locations and minigames that require Piplup"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Piplup",
                     "Ice Zone - Empoleon's Snow Slide - Piplup",

                     ]
        items = [["Piplup"]]
        self.assertAccessDependency(locations, items)

    def test_burmy(self) -> None:
        """Test locations and minigames that require Burmy"""
        locations = []
        items = [["Burmy"]]
        self.assertAccessDependency(locations, items)

    def test_mimejr(self) -> None:
        """Test locations and minigames that require Mime Jr."""
        locations = [
            "Flower Zone - Rayquaza's Balloon Panic - Mime Jr.",
        ]
        items = [["Mime Jr."]]
        self.assertAccessDependency(locations, items)

    def test_drifblim(self) -> None:
        """Test locations and minigames that require Drifblim"""
        locations = []
        items = [["Drifblim"]]
        self.assertAccessDependency(locations, items)

    def test_lapras(self) -> None:
        """Test locations and minigames that require Lapras"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Lapras",
                     ]
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
                     "Ice Zone - Overworld - Kirlia", "Ice Zone - Empoleon's Snow Slide - Teddiursa",

                     ]
        items = [["Teddiursa"]]
        self.assertAccessDependency(locations, items)

    def test_delibird(self) -> None:
        """Test locations and minigames that require Delibird"""
        locations = ["Ice Zone - Overworld - Kirlia",
                     "Ice Zone - Empoleon's Snow Slide - Delibird",

                     ]
        items = [["Delibird"]]
        self.assertAccessDependency(locations, items)

    def test_smoochum(self) -> None:
        """Test locations and minigames that require Smoochum"""
        locations = ["Ice Zone - Overworld - Christmas Tree Present 4",
                     "Ice Zone - Overworld - Delibird",
                     "Ice Zone - Overworld - Kirlia",
                     ]
        items = [["Smoochum"]]
        self.assertAccessDependency(locations, items)

    def test_squirtle(self) -> None:
        """Test locations and minigames that require Squirtle"""
        locations = ["Ice Zone - Overworld - Christmas Tree Present 3", "Ice Zone - Overworld - Delibird",
                     "Ice Zone - Overworld - Kirlia", "Ice Zone - Overworld - Christmas Tree Present 4",
                     "Ice Zone - Empoleon's Snow Slide - Squirtle",

                     ]
        items = [["Squirtle"]]
        self.assertAccessDependency(locations, items)

    def test_glaceon(self) -> None:
        """Test locations and minigames that require Glaceon"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Glaceon",

                     "Flower Zone - Rayquaza's Balloon Panic - Glaceon",
                     ]
        items = [["Glaceon"]]
        self.assertAccessDependency(locations, items)

    def test_prinplup(self) -> None:
        """Test locations and minigames that require Prinplup"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Prinplup",
                     "Beach Zone - Gyarados' Aqua Dash - Prinplup",
                     "Ice Zone - Overworld - Lower Lift Region - Corphish",
                     "Ice Zone - Overworld - Lower Lift Region - Wingull",
                     "Ice Zone - Overworld - Lower Lift Region - Quagsire",

                     ]
        items = [["Prinplup"]]
        self.assertAccessDependency(locations, items)

    def test_sneasel(self) -> None:
        """Test locations and minigames that require Sneasel"""
        locations = ["Haunted Zone - Tangrowth's Swing-Along - Sneasel",

                     ]
        items = [["Sneasel"]]
        self.assertAccessDependency(locations, items)

    def test_piloswine(self) -> None:
        """Test locations and minigames that require Piloswine"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Piloswine",

                     ]
        items = [["Piloswine"]]
        self.assertAccessDependency(locations, items)

    def test_glalie(self) -> None:
        """Test locations and minigames that require Glalie"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Glalie",

                     ]
        items = [["Glalie"]]
        self.assertAccessDependency(locations, items)

    def test_primeape(self) -> None:
        """Test locations and minigames that require Primeape"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Primeape",
                     "Haunted Zone - Tangrowth's Swing-Along - Primeape",

                     ]
        items = [["Primeape"]]
        self.assertAccessDependency(locations, items)

    def test_ursaring(self) -> None:
        """Test locations and minigames that require Ursaring"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Ursaring",

                     ]
        items = [["Ursaring"]]
        self.assertAccessDependency(locations, items)

    def test_mamoswine(self) -> None:
        """Test locations and minigames that require Mamoswine"""
        locations = [
            "Flower Zone - Rayquaza's Balloon Panic - Mamoswine",
        ]
        items = [["Mamoswine"]]
        self.assertAccessDependency(locations, items)

    def test_kirlia(self) -> None:
        """Test locations and minigames that require Kirlia"""
        locations = []
        items = [["Kirlia"]]
        self.assertAccessDependency(locations, items)

    def test_quagsire(self) -> None:
        """Test locations and minigames that require Quagsire"""
        locations = ["Ice Zone - Empoleon's Snow Slide - Quagsire",

                     ]
        items = [["Quagsire"]]
        self.assertAccessDependency(locations, items)

    def test_empoleon(self) -> None:
        """Test locations and minigames that require Empoleon"""
        locations = ["Beach Zone - Gyarados' Aqua Dash - Empoleon",
                     "Ice Zone - Empoleon's Snow Slide - Empoleon",

                     ]
        items = [["Empoleon"]]
        self.assertAccessDependency(locations, items)

    def test_magnemite(self) -> None:
        """Test locations and minigames that require Magnemite"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Magnemite",
                     "Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magnemite",

                     ]
        items = [["Magnemite"]]
        self.assertAccessDependency(locations, items)

    def test_geodude(self) -> None:
        """Test locations and minigames that require Geodude"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Geodude",

                     ]
        items = [["Geodude"]]
        self.assertAccessDependency(locations, items)

    def test_torchic(self) -> None:
        """Test locations and minigames that require Torchic"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Torchic",

                     ]
        items = [["Torchic"]]
        self.assertAccessDependency(locations, items)

    def test_machamp(self) -> None:
        """Test locations and minigames that require Machamp"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Machamp",

                     ]
        items = [["Machamp"]]
        self.assertAccessDependency(locations, items)

    def test_meowth(self) -> None:
        """Test locations and minigames that require Meowth"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Meowth",
                     "Haunted Zone - Tangrowth's Swing-Along - Meowth",

                     ]
        items = [["Meowth"]]
        self.assertAccessDependency(locations, items)

    def test_zubat(self) -> None:
        """Test locations and minigames that require Zubat"""
        locations = [
            "Granite Zone - Salamence's Sky Race - Zubat",
        ]
        items = [["Zubat"]]
        self.assertAccessDependency(locations, items)

    def test_cranidos(self) -> None:
        """Test locations and minigames that require Cranidos"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Cranidos",
                     "Haunted Zone - Mansion - Dusknoir's Speed Slam - Cranidos",

                     ]
        items = [["Cranidos"]]
        self.assertAccessDependency(locations, items)

    def test_scizor(self) -> None:
        """Test locations and minigames that require Scizor"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Scizor",
                     "Haunted Zone - Mansion - Dusknoir's Speed Slam - Scizor",

                     ]
        items = [["Scizor"]]
        self.assertAccessDependency(locations, items)

    def test_mawile(self) -> None:
        """Test locations and minigames that require Mawile"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Mawile",

                     ]
        items = [["Mawile"]]
        self.assertAccessDependency(locations, items)

    def test_marowak(self) -> None:
        """Test locations and minigames that require Marowak"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Marowak",

                     ]
        items = [["Marowak"]]
        self.assertAccessDependency(locations, items)

    def test_mrmime(self) -> None:
        """Test locations and minigames that require Mr. Mime"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Mr. Mime",
                     "Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Mr. Mime",

                     ]
        items = [["Mr. Mime"]]
        self.assertAccessDependency(locations, items)

    def test_aron(self) -> None:
        """Test locations and minigames that require Aron"""
        locations = []
        items = [["Aron"]]
        self.assertAccessDependency(locations, items)

    def test_dugtrio(self) -> None:
        """Test locations and minigames that require Dugtrio"""
        locations = []
        items = [["Dugtrio"]]
        self.assertAccessDependency(locations, items)

    def test_gible(self) -> None:
        """Test locations and minigames that require Gible"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Gible",

                     ]
        items = [["Gible"]]
        self.assertAccessDependency(locations, items)

    def test_magnezone(self) -> None:
        """Test locations and minigames that require Magnezone"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Magnezone",
                     "Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Magnezone",

                     ]
        items = [["Magnezone"]]
        self.assertAccessDependency(locations, items)

    def test_diglett(self) -> None:
        """Test locations and minigames that require Diglett"""
        locations = []
        items = [["Diglett"]]
        self.assertAccessDependency(locations, items)

    def test_phanpy(self) -> None:
        """Test locations and minigames that require Phanpy"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Phanpy",

                     ]
        items = [["Phanpy"]]
        self.assertAccessDependency(locations, items)

    def test_raichu(self) -> None:
        """Test locations and minigames that require Raichu"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Raichu",
                     "Haunted Zone - Tangrowth's Swing-Along - Raichu",

                     ]
        items = [["Raichu"]]
        self.assertAccessDependency(locations, items)

    def test_golbat(self) -> None:
        """Test locations and minigames that require Golbat"""
        locations = [
            "Granite Zone - Salamence's Sky Race - Golbat",
            "Granite Zone - Salamence's Sky Race - Golbat",
        ]
        items = [["Golbat"]]
        self.assertAccessDependency(locations, items)

    def test_bastiodon(self) -> None:
        """Test locations and minigames that require Bastiodon"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Bastiodon",

                     ]
        items = [["Bastiodon"]]
        self.assertAccessDependency(locations, items)

    def test_hitmonlee(self) -> None:
        """Test locations and minigames that require Hitmonlee"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Hitmonlee",

                     ]
        items = [["Hitmonlee"]]
        self.assertAccessDependency(locations, items)

    def test_camerupt(self) -> None:
        """Test locations and minigames that require Camerupt"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Camerupt",

                     ]
        items = [["Camerupt"]]
        self.assertAccessDependency(locations, items)

    def test_magby(self) -> None:
        """Test locations and minigames that require Magby"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Magby",

                     ]
        items = [["Magby"]]
        self.assertAccessDependency(locations, items)

    def test_vulpix(self) -> None:
        """Test locations and minigames that require Vulpix"""
        locations = [
            "Granite Zone - Absol's Hurdle Bounce - Vulpix",
        ]
        items = [["Vulpix"]]
        self.assertAccessDependency(locations, items)

    def test_ninetales(self) -> None:
        """Test locations and minigames that require Ninetales"""
        locations = [
            "Granite Zone - Absol's Hurdle Bounce - Ninetales",
        ]
        items = [["Ninetales"]]
        self.assertAccessDependency(locations, items)

    def test_quilava(self) -> None:
        """Test locations and minigames that require Quilava"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Quilava",

                     ]
        items = [["Quilava"]]
        self.assertAccessDependency(locations, items)

    def test_flareon(self) -> None:
        """Test locations and minigames that require Flareon"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Flareon",

                     ]
        items = [["Flareon"]]
        self.assertAccessDependency(locations, items)

    def test_meditite(self) -> None:
        """Test locations and minigames that require Meditite"""
        locations = []
        items = [["Meditite"]]
        self.assertAccessDependency(locations, items)

    def test_infernape(self) -> None:
        """Test locations and minigames that require Infernape"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Infernape",
                     "Haunted Zone - Tangrowth's Swing-Along - Infernape",

                     "Granite Zone - Absol's Hurdle Bounce - Infernape",
                     "Flower Zone - Rayquaza's Balloon Panic - Infernape",

                     ]
        items = [["Infernape"]]
        self.assertAccessDependency(locations, items)

    def test_farfetchd(self) -> None:
        """Test locations and minigames that require Farfetch'd"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Farfetch'd",

                     ]
        items = [["Farfetch'd"]]
        self.assertAccessDependency(locations, items)

    def test_magcargo(self) -> None:
        """Test locations and minigames that require Magcargo"""
        locations = []
        items = [["Magcargo"]]
        self.assertAccessDependency(locations, items)

    def test_charmander(self) -> None:
        """Test locations and minigames that require Charmander"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Charmander",

                     ]
        items = [["Charmander"]]
        self.assertAccessDependency(locations, items)

    def test_ponyta(self) -> None:
        """Test locations and minigames that require Ponyta"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Ponyta",

                     "Granite Zone - Absol's Hurdle Bounce - Ponyta",
                     ]
        items = [["Ponyta"]]
        self.assertAccessDependency(locations, items)

    def test_torkoal(self) -> None:
        """Test locations and minigames that require Torkoal"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Torkoal",

                     ]
        items = [["Torkoal"]]
        self.assertAccessDependency(locations, items)

    def test_golem(self) -> None:
        """Test locations and minigames that require Golem"""
        locations = []
        items = [["Golem"]]
        self.assertAccessDependency(locations, items)

    def test_rhyperior(self) -> None:
        """Test locations and minigames that require Rhyperior"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Rhyperior",

                     "Flower Zone - Rayquaza's Balloon Panic - Rhyperior",
                     ]
        items = [["Rhyperior"]]
        self.assertAccessDependency(locations, items)

    def test_baltoy(self) -> None:
        """Test locations and minigames that require Baltoy"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Baltoy",
                     "Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Baltoy",

                     ]
        items = [["Baltoy"]]
        self.assertAccessDependency(locations, items)

    def test_claydol(self) -> None:
        """Test locations and minigames that require Claydol"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Claydol",
                     "Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Claydol",

                     ]
        items = [["Claydol"]]
        self.assertAccessDependency(locations, items)

    def test_hitmonchan(self) -> None:
        """Test locations and minigames that require Hitmonchan"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Hitmonchan",

                     ]
        items = [["Hitmonchan"]]
        self.assertAccessDependency(locations, items)

    def test_hitmontop(self) -> None:
        """Test locations and minigames that require Hitmontop"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Hitmontop",

                     ]
        items = [["Hitmontop"]]
        self.assertAccessDependency(locations, items)

    def test_drifloon(self) -> None:
        """Test locations and minigames that require Drifloon"""
        locations = []
        items = [["Drifloon"]]
        self.assertAccessDependency(locations, items)

    def test_murkrow(self) -> None:
        """Test locations and minigames that require Murkrow"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Murkrow",

                     "Granite Zone - Salamence's Sky Race - Murkrow",
                     ]
        items = [["Murkrow"]]
        self.assertAccessDependency(locations, items)

    def test_honchkrow(self) -> None:
        """Test locations and minigames that require Honchkrow"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Honchkrow",

                     "Granite Zone - Salamence's Sky Race - Honchkrow",
                     ]
        items = [["Honchkrow"]]
        self.assertAccessDependency(locations, items)

    def test_gliscor(self) -> None:
        """Test locations and minigames that require Gliscor"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Gliscor",

                     "Granite Zone - Salamence's Sky Race - Gliscor",
                     ]
        items = [["Gliscor"]]
        self.assertAccessDependency(locations, items)

    def test_metapod(self) -> None:
        """Test locations and minigames that require Metapod"""
        locations = []
        items = [["Metapod"]]
        self.assertAccessDependency(locations, items)

    def test_kakuna(self) -> None:
        """Test locations and minigames that require Kakuna"""
        locations = []
        items = [["Kakuna"]]
        self.assertAccessDependency(locations, items)

    def test_tangrowth(self) -> None:
        """Test locations and minigames that require Tangrowth"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Tangrowth",

                     ]
        items = [["Tangrowth"]]
        self.assertAccessDependency(locations, items)

    def test_duskull(self) -> None:
        """Test locations and minigames that require Duskull"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Duskull",

                     ]
        items = [["Duskull"]]
        self.assertAccessDependency(locations, items)

    def test_sableye(self) -> None:
        """Test locations and minigames that require Sableye"""
        locations = ["Cavern Zone - Bastiodon's Panel Crush - Sableye",

                     ]
        items = [["Sableye"]]
        self.assertAccessDependency(locations, items)

    def test_misdreavus(self) -> None:
        """Test locations and minigames that require Misdreavus"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Misdreavus",

                     ]
        items = [["Misdreavus"]]
        self.assertAccessDependency(locations, items)

    def test_pichu(self) -> None:
        """Test locations and minigames that require Pichu"""
        locations = ["Haunted Zone - Tangrowth's Swing-Along - Pichu",

                     ]
        items = [["Pichu"]]
        self.assertAccessDependency(locations, items)

    def test_umbreon(self) -> None:
        """Test locations and minigames that require Umbreon"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Umbreon",

                     ]
        items = [["Umbreon"]]
        self.assertAccessDependency(locations, items)

    def test_spinarak(self) -> None:
        """Test locations and minigames that require Spinarak"""
        locations = []
        items = [["Spinarak"]]
        self.assertAccessDependency(locations, items)

    def test_abra(self) -> None:
        """Test locations and minigames that require Abra"""
        locations = ["Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Abra",

                     ]
        items = [["Abra"]]
        self.assertAccessDependency(locations, items)

    def test_riolu(self) -> None:
        """Test locations and minigames that require Abra"""
        locations = ["Haunted Zone - Tangrowth's Swing-Along - Riolu",

                     "Granite Zone - Absol's Hurdle Bounce - Riolu",
                     ]
        items = [["Riolu"]]
        self.assertAccessDependency(locations, items)

    def test_voltorb(self) -> None:
        """Test locations and minigames that require Voltorb"""
        locations = []
        items = [["Voltorb"]]
        self.assertAccessDependency(locations, items)

    def test_elekid(self) -> None:
        """Test locations and minigames that require Elekid"""
        locations = ["Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Elekid",

                     ]
        items = [["Elekid"]]
        self.assertAccessDependency(locations, items)

    def test_electabuzz(self) -> None:
        """Test locations and minigames that require Electabuzz"""
        locations = ["Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Electabuzz",
                     "Haunted Zone - Tangrowth's Swing-Along - Electabuzz",

                     ]
        items = [["Electabuzz"]]
        self.assertAccessDependency(locations, items)

    def test_luxray(self) -> None:
        """Test locations and minigames that require Luxray"""
        locations = [

            "Flower Zone - Rayquaza's Balloon Panic - Luxray"]
        items = [["Luxray"]]
        self.assertAccessDependency(locations, items)

    def test_stunky(self) -> None:
        """Test locations and minigames that require Stunky"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Stunky",

                     ]
        items = [["Stunky"]]
        self.assertAccessDependency(locations, items)

    def test_skuntank(self) -> None:
        """Test locations and minigames that require Skuntank"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Skuntank",

                     ]
        items = [["Skuntank"]]
        self.assertAccessDependency(locations, items)

    def test_breloom(self) -> None:
        """Test locations and minigames that require Breloom"""
        locations = [
            "Granite Zone - Absol's Hurdle Bounce - Breloom",

            "Flower Zone - Rayquaza's Balloon Panic - Breloom",
        ]
        items = [["Breloom"]]
        self.assertAccessDependency(locations, items)

    def test_mismagius(self) -> None:
        """Test locations and minigames that require Mismagius"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Mismagius",
                     "Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Mismagius",

                     ]
        items = [["Mismagius"]]
        self.assertAccessDependency(locations, items)

    def test_electrode(self) -> None:
        """Test locations and minigames that require Electrode"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Electrode",

                     ]
        items = [["Electrode"]]
        self.assertAccessDependency(locations, items)

    def test_haunter(self) -> None:
        """Test locations and minigames that require Haunter"""
        locations = ["Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Haunter",
                     ]
        items = [["Haunter"]]
        self.assertAccessDependency(locations, items)

    def test_gastly(self) -> None:
        """Test locations and minigames that require Gastly"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Gastly",

                     ]
        items = [["Gastly"]]
        self.assertAccessDependency(locations, items)

    def test_dusknoir(self) -> None:
        """Test locations and minigames that require Dusknoir"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Dusknoir",

                     ]
        items = [["Dusknoir"]]
        self.assertAccessDependency(locations, items)

    def test_espeon(self) -> None:
        """Test locations and minigames that require Espeon"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Espeon",

                     "Granite Zone - Absol's Hurdle Bounce - Espeon",
                     ]
        items = [["Espeon"]]
        self.assertAccessDependency(locations, items)

    def test_gengar(self) -> None:
        """Test locations and minigames that require Gengar"""
        locations = ["Haunted Zone - Mansion - Dusknoir's Speed Slam - Gengar",
                     "Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Gengar"]
        items = [["Gengar"]]
        self.assertAccessDependency(locations, items)

    def test_charizard(self) -> None:
        """Test locations and minigames that require Charizard"""
        locations = ["Granite Zone - Salamence's Sky Race - Charizard"]
        items = [["Charizard"]]
        self.assertAccessDependency(locations, items)

    def test_flygon(self) -> None:
        """Test locations and minigames that require Flygon"""
        locations = ["Granite Zone - Salamence's Sky Race - Flygon"]
        items = [["Flygon"]]
        self.assertAccessDependency(locations, items)

    def test_porygonz(self) -> None:
        """Test locations and minigames that require Porygon-Z"""
        locations = ["Haunted Zone - Mansion - Rotom's Spooky Shoot-'em-Up - Porygon-Z"]
        items = [["Porygon-Z"]]
        self.assertAccessDependency(locations, items)

    def test_bronzor(self) -> None:
        """Test locations and minigames that require Bronzor"""
        locations = []
        items = [["Bronzor"]]
        self.assertAccessDependency(locations, items)

    def test_togekiss(self) -> None:
        """Test locations and minigames that require Togekiss"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Togekiss",
                     "Granite Zone - Salamence's Sky Race - Togekiss"]
        items = [["Togekiss"]]
        self.assertAccessDependency(locations, items)

    def test_arcanine(self) -> None:
        """Test locations and minigames that require Arcanine"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Arcanine"]
        items = [["Arcanine"]]
        self.assertAccessDependency(locations, items)

    def test_lopunny(self) -> None:
        """Test locations and minigames that require Lopunny"""
        locations = ["Granite Zone - Absol's Hurdle Bounce - Lopunny"]
        items = [["Lopunny"]]
        self.assertAccessDependency(locations, items)

    def test_furret(self) -> None:
        """Test locations and minigames that require Furret"""
        locations = ["Granite Zone - Absol's Hurdle Bounce - Furret"]
        items = [["Furret"]]
        self.assertAccessDependency(locations, items)

    def test_staraptor(self) -> None:
        """Test locations and minigames that require Staraptor"""
        locations = ["Beach Zone - Pelipper's Circle Circuit - Staraptor",
                     "Granite Zone - Salamence's Sky Race - Staraptor"]
        items = [["Staraptor"]]
        self.assertAccessDependency(locations, items)

    def test_skorupi(self) -> None:
        """Test locations and minigames that require Skorupi"""
        locations = []
        items = [["Skorupi"]]
        self.assertAccessDependency(locations, items)

    def test_eevee(self) -> None:
        """Test locations and minigames that require Eevee"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Eevee",
                     "Granite Zone - Absol's Hurdle Bounce - Eevee"]
        items = [["Eevee"]]
        self.assertAccessDependency(locations, items)

    def test_hoppip(self) -> None:
        """Test locations and minigames that require Hoppip"""
        locations = []
        items = [["Hoppip"]]
        self.assertAccessDependency(locations, items)

    def test_jumpluff(self) -> None:
        """Test locations and minigames that require Jumpluff"""
        locations = []
        items = [["Jumpluff"]]
        self.assertAccessDependency(locations, items)

    def test_aerodactyl(self) -> None:
        """Test locations and minigames that require Aerodactyl"""
        locations = ["Granite Zone - Salamence's Sky Race - Aerodactyl"]
        items = [["Aerodactyl"]]
        self.assertAccessDependency(locations, items)

    def test_jolteon(self) -> None:
        """Test locations and minigames that require Jolteon"""
        locations = ["Meadow Zone - Bulbasaur's Daring Dash Minigame - Jolteon"]
        items = [["Jolteon"]]
        self.assertAccessDependency(locations, items)

    def test_tyranitar(self) -> None:
        """Test locations and minigames that require Tyranitar"""
        locations = ["Magma Zone - Rhyperior's Bumper Burn - Tyranitar"]
        items = [["Tyranitar"]]
        self.assertAccessDependency(locations, items)

    def test_garchomp(self) -> None:
        """Test locations and minigames that require Garchomp"""
        locations = ["Magma Zone - Blaziken's Boulder Bash - Garchomp"]
        items = [["Garchomp"]]
        self.assertAccessDependency(locations, items)

    def test_absol(self) -> None:
        """Test locations and minigames that require Absol"""
        locations = ["Granite Zone - Absol's Hurdle Bounce - Absol",
                     "Flower Zone - Rayquaza's Balloon Panic - Absol"]
        items = [["Absol"]]
        self.assertAccessDependency(locations, items)

    def test_salamence(self) -> None:
        """Test locations and minigames that require Salamence"""
        locations = ["Granite Zone - Salamence's Sky Race - Salamence"]
        items = [["Salamence"]]
        self.assertAccessDependency(locations, items)

    def test_bellossom(self) -> None:
        """Test locations and minigames that require Bellossom"""
        locations = []
        items = [["Bellossom"]]
        self.assertAccessDependency(locations, items)

    def test_budew(self) -> None:
        """Test locations and minigames that require Budew"""
        locations = []
        items = [["Budew"]]
        self.assertAccessDependency(locations, items)

    def test_skiploom(self) -> None:
        """Test locations and minigames that require Skiploom"""
        locations = []
        items = [["Skiploom"]]
        self.assertAccessDependency(locations, items)

    def test_cyndaquil(self) -> None:
        """Test locations and minigames that require Cyndaquil"""
        locations = ["Flower Zone - Rayquaza's Balloon Panic - Cyndaquil"]
        items = [["Cyndaquil"]]
        self.assertAccessDependency(locations, items)

    def test_mareep(self) -> None:
        """Test locations and minigames that require Mareep"""
        locations = ["Granite Zone - Absol's Hurdle Bounce - Mareep",
                     "Flower Zone - Rayquaza's Balloon Panic - Mareep"]
        items = [["Mareep"]]
        self.assertAccessDependency(locations, items)

    def test_dragonite(self) -> None:
        """Test locations and minigames that require Dragonite"""
        locations = ["Granite Zone - Salamence's Sky Race - Dragonite"]
        items = [["Dragonite"]]
        self.assertAccessDependency(locations, items)

    def test_lucario(self) -> None:
        """Test locations and minigames that require Lucario"""
        locations = ["Meadow Zone - Venusaur's Vine Swing - Lucario",
                     "Haunted Zone - Tangrowth's Swing-Along - Lucario",
                     "Granite Zone - Absol's Hurdle Bounce - Lucario",
                     "Flower Zone - Rayquaza's Balloon Panic - Lucario"]
        items = [["Lucario"]]
        self.assertAccessDependency(locations, items)

    def test_rayquaza(self) -> None:
        """Test locations and minigames that require Rayquaza"""
        locations = []
        items = [["Rayquaza"]]
        self.assertAccessDependency(locations, items)

    def test_mew(self) -> None:
        """Test locations and minigames that require Mew. Base game Goal"""
        locations = []
        items = [["Mew"]]
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

    def test_can_reach_ice_zone_lower_lift_with_prinplup(self) -> None:
        """Verify ability to access Ice Zone Lower Lift Region with Prinplup"""

        self.collect_by_name(["Prinplup", "Ice Zone Unlock"])
        self.assertTrue(self.can_reach_region("Ice Zone - Overworld - Lower Lift Region"))

    def test_can_not_reach_ice_zone_lower_lift_without_prinplup(self) -> None:
        """Verify inability to access Ice Zone Lower Lift Region without Prinplup"""

        self.collect_all_but(["Prinplup"])
        self.assertFalse(self.can_reach_region("Ice Zone - Overworld - Lower Lift Region"))
