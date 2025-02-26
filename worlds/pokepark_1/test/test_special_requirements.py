from . import PokeparkTest

class TestPokemonFriendshipDependencies(PokeparkTest):

    def test_leafeon_friendcount(self) -> None:
        """Verify Leafeon access with sufficient Pokemon friendships (first valid set)"""
        pokemon_set1 = [
            "Oddish", "Totodile", "Corsola", "Bidoof", "Wingull",
            "Chimchar", "Mudkip", "Leafeon", "Tropius", "Staravia",
            "Buneary", "Slowpoke", "Caterpie", "Azurill", "Pachirisu",
            "Ambipom", "Psyduck", "Butterfree", "Shroomish", "Buizel","Chikorita"
        ]
        self.collect_by_name(pokemon_set1)
        self.assertTrue(self.can_reach_location("Meadow Zone - Overworld - Leafeon"))

    def test_leafeon_friendcount2(self) -> None:
        """Verify Leafeon access with sufficient Pokemon friendships (second valid set)"""
        pokemon_set2 = [
            "Mankey", "Pidgeotto", "Spearow", "Weedle", "Bibarel",
            "Turtwig", "Magikarp", "Chatot", "Shinx", "Taillow",
            "Aipom", "Sudowoodo", "Bulbasaur", "Torterra", "Croagunk",
            "Starly", "Bonsly", "Treecko", "Lotad", "Chikorita","Buizel"
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
        self.collect_by_name("Beach Zone Unlock") # Region unlock removes dependency for tests
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
        self.collect_by_name("Beach Zone Unlock") # Region unlock removes dependency for tests
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
        self.collect_by_name("Beach Zone Unlock") # Region unlock removes dependency for tests
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
        self.collect_by_name("Beach Zone Unlock") # Region unlock removes dependency for tests
        self.assertFalse(self.can_reach_location("Beach Zone - Overworld - Vaporeon"))