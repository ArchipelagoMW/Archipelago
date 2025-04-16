from BaseClasses import ItemClassification
from . import PokeparkTest
from .. import PokeparkItem, REGION_UNLOCK


class TestFriendCountDependencies(PokeparkTest):

    def test_leafeon_friendcount(self) -> None:
        """Verify Leafeon access with sufficient Pokemon friendships (first valid set)"""
        pokemon_set1 = [
            "Oddish", "Totodile", "Corsola", "Bidoof", "Wingull",
            "Chimchar", "Mudkip", "Leafeon", "Tropius", "Staravia",
            "Buneary", "Slowpoke", "Caterpie", "Azurill", "Pachirisu",
            "Ambipom", "Psyduck", "Butterfree", "Shroomish", "Buizel", "Chikorita"
        ]
        self.collect_by_name(pokemon_set1)
        self.assertTrue(self.can_reach_location("Meadow Zone - Overworld - Leafeon"))

    def test_leafeon_friendcount2(self) -> None:
        """Verify Leafeon access with sufficient Pokemon friendships (second valid set)"""
        pokemon_set2 = [
            "Mankey", "Pidgeotto", "Spearow", "Weedle", "Bibarel",
            "Turtwig", "Magikarp", "Chatot", "Shinx", "Taillow",
            "Aipom", "Sudowoodo", "Bulbasaur", "Torterra", "Croagunk",
            "Starly", "Bonsly", "Treecko", "Lotad", "Chikorita", "Buizel"
        ]
        self.collect_by_name(pokemon_set2)
        self.assertTrue(self.can_reach_location("Meadow Zone - Overworld - Leafeon"))

    def test_leafeon_friendcount_not_enough(self) -> None:
        """Verify Leafeon access is blocked with insufficient Pokemon friendships (first invalid set)"""
        pokemon_set3 = [
            "Mudkip", "Oddish", "Wingull", "Ambipom", "Psyduck",
            "Totodile", "Pachirisu", "Corsola", "Bidoof", "Slowpoke",
            "Chimchar", "Buneary", "Caterpie", "Shroomish", "Staravia",
            "Treecko", "Azurill", "Magikarp", "Buizel", "Leafeon"
        ]
        self.collect_by_name(pokemon_set3)
        self.assertFalse(self.can_reach_location("Meadow Zone - Overworld - Leafeon"))

    def test_leafeon_friendcount_not_enough2(self) -> None:
        """Verify Leafeon access is blocked with insufficient Pokemon friendships (second invalid set)"""
        pokemon_set4 = [
            "Tropius", "Turtwig", "Chatot", "Mankey", "Pidgeotto",
            "Spearow", "Weedle", "Torterra", "Shinx", "Taillow",
            "Aipom", "Sudowoodo", "Bulbasaur", "Bibarel", "Starly",
            "Bonsly", "Butterfree", "Lotad", "Chikorita", "Croagunk"
        ]
        self.collect_by_name(pokemon_set4)
        self.assertFalse(self.can_reach_location("Meadow Zone - Overworld - Leafeon"))

    def test_vaporeon_friendcount(self) -> None:
        """Verify Vaporeon access with sufficient Pokemon friendships (first valid set)"""
        pokemon_set1 = [
            "Oddish", "Totodile", "Corsola", "Bidoof", "Wingull",
            "Chimchar", "Mudkip", "Leafeon", "Tropius", "Staravia",
            "Buneary", "Slowpoke", "Caterpie", "Azurill", "Pachirisu",
            "Ambipom", "Psyduck", "Butterfree", "Shroomish", "Buizel",
            "Chikorita", "Mankey", "Pidgeotto", "Spearow", "Weedle",
            "Bibarel", "Turtwig", "Magikarp", "Chatot", "Shinx", "Taillow"
        ]
        self.collect_by_name(pokemon_set1)
        self.collect_by_name("Beach Zone Unlock")  # Region unlock removes dependency for tests
        self.assertTrue(self.can_reach_location("Beach Zone - Overworld - Vaporeon"))

    def test_vaporeon_friendcount2(self) -> None:
        """Verify Vaporeon access with sufficient Pokemon friendships (second valid set)"""
        pokemon_set2 = [
            "Aipom", "Sudowoodo", "Bulbasaur", "Torterra", "Croagunk",
            "Starly", "Bonsly", "Treecko", "Lotad", "Chikorita",
            "Oddish", "Totodile", "Corsola", "Bidoof", "Wingull",
            "Chimchar", "Mudkip", "Leafeon", "Tropius", "Staravia",
            "Buneary", "Slowpoke", "Caterpie", "Azurill", "Pachirisu",
            "Ambipom", "Psyduck", "Butterfree", "Shroomish", "Buizel",
            "Mankey"
        ]
        self.collect_by_name(pokemon_set2)
        self.collect_by_name("Beach Zone Unlock")  # Region unlock removes dependency for tests
        self.assertTrue(self.can_reach_location("Beach Zone - Overworld - Vaporeon"))

    def test_vaporeon_friendcount_not_enough(self) -> None:
        """Verify Vaporeon access is blocked with insufficient Pokemon friendships (first invalid set)"""
        pokemon_set3 = [
            "Mudkip", "Oddish", "Wingull", "Ambipom", "Psyduck",
            "Totodile", "Pachirisu", "Corsola", "Bidoof", "Slowpoke",
            "Chimchar", "Buneary", "Caterpie", "Shroomish", "Staravia",
            "Treecko", "Azurill", "Magikarp", "Buizel", "Leafeon",
            "Mankey", "Pidgeotto", "Spearow", "Weedle", "Bibarel"
        ]
        self.collect_by_name(pokemon_set3)
        self.collect_by_name("Beach Zone Unlock")  # Region unlock removes dependency for tests
        self.assertFalse(self.can_reach_location("Beach Zone - Overworld - Vaporeon"))

    def test_vaporeon_friendcount_not_enough2(self) -> None:
        """Verify Vaporeon access is blocked with barely insufficient Pokemon friendships (second invalid set)"""
        pokemon_set4 = [
            "Tropius", "Turtwig", "Chatot", "Mankey", "Pidgeotto",
            "Spearow", "Weedle", "Torterra", "Shinx", "Taillow",
            "Aipom", "Sudowoodo", "Bulbasaur", "Bibarel", "Starly",
            "Bonsly", "Butterfree", "Lotad", "Chikorita", "Croagunk",
            "Oddish", "Totodile", "Corsola", "Bidoof", "Wingull",
            "Chimchar", "Mudkip", "Leafeon", "Buneary", "Slowpoke"
        ]
        self.collect_by_name(pokemon_set4)
        self.collect_by_name("Beach Zone Unlock")  # Region unlock removes dependency for tests
        self.assertFalse(self.can_reach_location("Beach Zone - Overworld - Vaporeon"))

    def test_glaceon_friendcount_valid1(self) -> None:
        """Verify Glaceon access with first valid set of 55 Pokemon friendships."""
        glaceon_set1 = [
            "Chikorita", "Pachirisu", "Bulbasaur", "Munchlax", "Tropius",
            "Turtwig", "Bonsly", "Sudowoodo", "Buneary", "Shinx",
            "Mankey", "Spearow", "Croagunk", "Chatot", "Lotad",
            "Treecko", "Caterpie", "Butterfree", "Chimchar", "Aipom",
            "Ambipom", "Weedle", "Shroomish", "Magikarp", "Oddish",
            "Leafeon", "Bidoof", "Bibarel", "Torterra", "Starly",
            "Scyther", "Buizel", "Psyduck", "Slowpoke", "Azurill",
            "Totodile", "Mudkip", "Pidgeotto", "Taillow", "Wingull",
            "Staravia", "Corsola", "Floatzel", "Vaporeon", "Golduck",
            "Pelipper", "Sharpedo", "Wynaut", "Carvanha", "Krabby",
            "Wailord", "Corphish", "Gyarados", "Feraligatr", "Piplup"
        ]
        self.collect_by_name(glaceon_set1)
        self.collect_by_name("Ice Zone Unlock")  # Region unlock removes dependency for tests
        self.assertTrue(self.can_reach_location("Ice Zone - Overworld - Glaceon"))

    def test_glaceon_friendcount_valid2(self) -> None:
        """Verify Glaceon access with second valid set of 53 Pokemon friendships including all zones."""
        glaceon_set2 = [
            "Chikorita", "Pachirisu", "Bulbasaur", "Munchlax", "Tropius",
            "Turtwig", "Bonsly", "Sudowoodo", "Buneary", "Shinx",
            "Mankey", "Spearow", "Croagunk", "Chatot", "Lotad",
            "Treecko", "Caterpie", "Butterfree", "Chimchar", "Aipom",
            "Buizel", "Psyduck", "Slowpoke", "Azurill", "Totodile",
            "Mudkip", "Pidgeotto", "Taillow", "Wingull", "Staravia",
            "Corsola", "Floatzel", "Vaporeon", "Golduck", "Pelipper",
            "Sharpedo", "Wynaut", "Carvanha", "Krabby", "Wailord",
            "Lapras", "Spheal", "Octillery", "Teddiursa", "Delibird",
            "Smoochum", "Squirtle", "Glaceon", "Prinplup", "Sneasel",
            "Piloswine", "Burmy", "Drifblim"
        ]
        self.collect_by_name(glaceon_set2)
        self.collect_by_name("Ice Zone Unlock")  # Region unlock removes dependency for tests
        self.assertTrue(self.can_reach_location("Ice Zone - Overworld - Glaceon"))

    def test_glaceon_friendcount_valid3(self) -> None:
        """Verify Glaceon access with third valid set containing minimum of 51 Pokemon friendships."""
        glaceon_set3 = [
            "Chikorita", "Pachirisu", "Bulbasaur", "Munchlax", "Tropius",
            "Turtwig", "Bonsly", "Sudowoodo", "Buneary", "Shinx",
            "Mankey", "Spearow", "Croagunk", "Chatot", "Lotad",
            "Treecko", "Caterpie", "Butterfree", "Chimchar", "Aipom",
            "Ambipom", "Weedle", "Shroomish", "Magikarp", "Oddish",
            "Leafeon", "Bidoof", "Bibarel", "Torterra", "Starly",
            "Scyther", "Buizel", "Psyduck", "Slowpoke", "Azurill",
            "Totodile", "Mudkip", "Pidgeotto", "Taillow", "Wingull",
            "Staravia", "Corsola", "Floatzel", "Vaporeon", "Golduck",
            "Pelipper", "Sharpedo", "Wynaut", "Carvanha", "Krabby",
            "Wailord"
        ]
        self.collect_by_name(glaceon_set3)
        self.collect_by_name("Ice Zone Unlock")  # Region unlock removes dependency for tests
        self.assertTrue(self.can_reach_location("Ice Zone - Overworld - Glaceon"))

    def test_glaceon_friendcount_invalid1(self) -> None:
        """Verify Glaceon access is blocked with first invalid set (exactly 50 Pokemon friendships)."""
        glaceon_invalid_set1 = [
            "Chikorita", "Pachirisu", "Bulbasaur", "Munchlax", "Tropius",
            "Turtwig", "Bonsly", "Sudowoodo", "Buneary", "Shinx",
            "Mankey", "Spearow", "Croagunk", "Chatot", "Lotad",
            "Treecko", "Caterpie", "Butterfree", "Chimchar", "Aipom",
            "Ambipom", "Weedle", "Shroomish", "Magikarp", "Oddish",
            "Leafeon", "Bidoof", "Bibarel", "Torterra", "Starly",
            "Scyther", "Buizel", "Psyduck", "Slowpoke", "Azurill",
            "Totodile", "Mudkip", "Pidgeotto", "Taillow", "Wingull",
            "Staravia", "Corsola", "Floatzel", "Vaporeon", "Golduck",
            "Pelipper", "Sharpedo", "Wynaut", "Carvanha", "Krabby"
        ]
        self.collect_by_name(glaceon_invalid_set1)
        self.collect_by_name("Ice Zone Unlock")  # Region unlock removes dependency for tests
        self.assertFalse(self.can_reach_location("Ice Zone - Overworld - Glaceon"))

    def test_glaceon_friendcount_invalid2(self) -> None:
        """Verify Glaceon access is blocked with second invalid set (50 Pokemon friendships, different combination)."""
        glaceon_invalid_set2 = [
            "Chikorita", "Pachirisu", "Bulbasaur", "Munchlax", "Tropius",
            "Turtwig", "Bonsly", "Sudowoodo", "Buneary", "Shinx",
            "Mankey", "Spearow", "Croagunk", "Chatot", "Lotad",
            "Treecko", "Caterpie", "Butterfree", "Chimchar", "Aipom",
            "Ambipom", "Weedle", "Shroomish", "Magikarp", "Oddish",
            "Leafeon", "Bidoof", "Bibarel", "Torterra", "Starly",
            "Scyther", "Buizel", "Psyduck", "Slowpoke", "Azurill",
            "Totodile", "Mudkip", "Pidgeotto", "Taillow", "Wingull",
            "Staravia", "Corsola", "Floatzel", "Vaporeon", "Golduck",
            "Pelipper", "Sharpedo", "Wynaut", "Carvanha", "Krabby"
        ]
        self.collect_by_name(glaceon_invalid_set2)
        self.collect_by_name("Ice Zone Unlock")  # Region unlock removes dependency for tests
        self.assertFalse(self.can_reach_location("Ice Zone - Overworld - Glaceon"))

    def test_bastiodon_minigame_access(self) -> None:
        """Verify bastiodon minigame is accessable with (50 Pokemon friendships)."""
        pokemon_50_set = [
            "Chikorita", "Pachirisu", "Bulbasaur", "Munchlax", "Tropius",
            "Turtwig", "Bonsly", "Sudowoodo", "Buneary", "Shinx",
            "Mankey", "Spearow", "Croagunk", "Chatot", "Lotad",
            "Treecko", "Caterpie", "Butterfree", "Chimchar", "Aipom",
            "Ambipom", "Weedle", "Shroomish", "Magikarp", "Oddish",
            "Leafeon", "Bidoof", "Bibarel", "Torterra", "Starly",
            "Scyther", "Buizel", "Psyduck", "Slowpoke", "Azurill",
            "Totodile", "Mudkip", "Pidgeotto", "Taillow", "Wingull",
            "Staravia", "Corsola", "Floatzel", "Vaporeon", "Golduck",
            "Pelipper", "Sharpedo", "Wynaut", "Carvanha", "Krabby"
        ]
        self.collect_by_name(pokemon_50_set)
        self.collect_by_name("Cavern Zone & Magma Zone Unlock")  # Region unlock removes dependency for tests
        self.assertTrue(self.can_reach_region("Cavern Zone - Bastiodon's Panel Crush"))


class TestReachingVictoryLocationMewChallenge(PokeparkTest):
    options = {
        "goal": 0
    }

    def test_can_beat_game(self) -> None:
        self.collect(self.world.create_item("Skygarden Unlock"))
        self.collect_by_name("Progressive Dash")

        self.assertBeatable(True)


class TestReachingVictoryLocationPostGame(PokeparkTest):
    options = {
        "goal": 1
    }

    def test_can_beat_game(self) -> None:
        self.collect_all_but(["Victory"])
        self.assertBeatable(True)

    def test_can_not_beat_game_with_friend_missing(self) -> None:
        self.collect_all_but(["Caterpie", "Victory"])
        self.assertBeatable(False)

    def test_can_not_beat_game_with_skygarden_unlock_missing(self) -> None:
        self.collect_all_but(["Skygarden Unlock", "Victory"])
        self.assertBeatable(False)
