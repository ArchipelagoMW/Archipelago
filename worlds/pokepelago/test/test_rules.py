"""
Logic correctness tests for the Pokepelago APWorld.

These tests verify that access rules are wired correctly:
  - Type Keys gate the right Pokemon locations
  - Region Passes gate the right game-region entrances
  - Milestone rules require enough logically accessible Pokemon
  - Victory requires goal_count accessible Pokemon
  - Extra gate locks (legendary, trade, baby, fossil, UB, paradox, stone) gate the right locations
"""
import unittest

from BaseClasses import CollectionState
from test.bases import WorldTestBase
from test.general import setup_multiworld
from worlds.pokepelago import PokepelagoWorld


# ---------------------------------------------------------------------------
# Type Key gating
# ---------------------------------------------------------------------------

class TestTypeKeyRules(WorldTestBase):
    """Kanto only, dexsanity + type_locks on, Charmander as starter (Fire type pre-collected)."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto"},
        "type_locks": 1,
        "region_locks": 0,
        "dexsanity": 1,
        "starter_region": 1,   # Kanto
        "starter_pokemon": 2,  # Charmander → Fire Type Key pre-collected
    }

    def test_grass_location_requires_grass_type_key(self):
        """Guess Bulbasaur (Grass/Poison) should not be reachable without Grass + Poison Type Keys."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Bulbasaur", "Location", self.player),
            "Guess Bulbasaur should be locked without Grass + Poison Type Keys",
        )

    def test_grass_location_reachable_with_type_keys(self):
        """Guess Bulbasaur becomes reachable once Grass and Poison Type Keys are collected."""
        state = CollectionState(self.multiworld)
        for item in self.multiworld.itempool:
            if item.name in ("Grass Type Key", "Poison Type Key"):
                state.collect(item)
        self.assertTrue(
            state.can_reach("Guess Bulbasaur", "Location", self.player),
            "Guess Bulbasaur should be reachable with Grass + Poison Type Keys",
        )

    def test_fire_location_reachable_from_start(self):
        """Charmander (Fire) location should be reachable immediately — Fire Type Key pre-collected."""
        state = CollectionState(self.multiworld)
        self.assertTrue(
            state.can_reach("Guess Charmander", "Location", self.player),
            "Guess Charmander should be reachable from the start (Fire Type Key pre-collected)",
        )

    def test_water_location_requires_water_type_key(self):
        """Guess Squirtle (Water) requires Water Type Key (not pre-collected with Charmander start)."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Squirtle", "Location", self.player),
            "Guess Squirtle should be locked without Water Type Key",
        )
        for item in self.multiworld.itempool:
            if item.name == "Water Type Key":
                state.collect(item)
                break
        self.assertTrue(
            state.can_reach("Guess Squirtle", "Location", self.player),
            "Guess Squirtle should be reachable with Water Type Key",
        )


# ---------------------------------------------------------------------------
# Region Pass gating
# ---------------------------------------------------------------------------

class TestRegionPassRules(WorldTestBase):
    """Kanto + Johto, dexsanity + region_locks on, starting from Kanto."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto", "Johto"},
        "type_locks": 0,
        "region_locks": 1,
        "dexsanity": 1,
        "starter_region": 1,  # Kanto
    }

    def test_johto_pokemon_locked_without_pass(self):
        """Guess Chikorita (Johto) should not be reachable without Johto Pass."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Chikorita", "Location", self.player),
            "Guess Chikorita should be locked without Johto Pass",
        )

    def test_johto_pokemon_reachable_with_pass(self):
        """Guess Chikorita becomes reachable once Johto Pass is collected."""
        state = CollectionState(self.multiworld)
        for item in self.multiworld.itempool:
            if item.name == "Johto Pass":
                state.collect(item)
                break
        self.assertTrue(
            state.can_reach("Guess Chikorita", "Location", self.player),
            "Guess Chikorita should be reachable with Johto Pass",
        )

    def test_kanto_pokemon_reachable_from_start(self):
        """Guess Rattata (Kanto, starting region) should be reachable from empty state."""
        state = CollectionState(self.multiworld)
        self.assertTrue(
            state.can_reach("Guess Rattata", "Location", self.player),
            "Guess Rattata should be reachable from the start (Kanto is starting region)",
        )


# ---------------------------------------------------------------------------
# Milestone rules
# ---------------------------------------------------------------------------

class TestMilestoneRules(WorldTestBase):
    """Kanto only, all locks on — milestone rules should require accessible Pokemon."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto"},
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
        "starter_region": 1,
        "starter_pokemon": 1,  # Bulbasaur → Grass + Poison pre-collected
    }

    def test_high_milestone_not_reachable_from_empty(self):
        """'Guessed 100 Pokemon' should not be in logic without enough Type Keys."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guessed 100 Pokemon", "Location", self.player),
            "Guessed 100 Pokemon should not be reachable from empty state",
        )

    def test_high_milestone_reachable_with_all_items(self):
        """'Guessed 100 Pokemon' should be reachable once all items are collected."""
        state = self.multiworld.get_all_state(False)
        self.assertTrue(
            state.can_reach("Guessed 100 Pokemon", "Location", self.player),
            "Guessed 100 Pokemon should be reachable with all items",
        )


# ---------------------------------------------------------------------------
# Victory rule
# ---------------------------------------------------------------------------

class TestVictoryRule(WorldTestBase):
    """Kanto only, all locks on — victory requires goal_count Pokemon accessible."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto"},
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
        "starter_region": 1,
    }

    def test_victory_not_reachable_from_empty(self):
        """Victory should not be completable from an empty state."""
        self.assertBeatable(False)

    def test_victory_reachable_with_all_items(self):
        """Victory should be completable once all items are collected."""
        state = self.multiworld.get_all_state(False)
        self.multiworld.state = state
        self.assertBeatable(True)


# ---------------------------------------------------------------------------
# Extra gate locks
# ---------------------------------------------------------------------------

class TestLegendaryLocks(WorldTestBase):
    """Kanto with legendary_locks on — box legendaries require 7 Gym Badges."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto"},
        "legendary_locks": 1,
        "type_locks": 0,
        "region_locks": 0,
        "dexsanity": 1,
    }

    def test_mewtwo_not_reachable_without_badges(self):
        """Guess Mewtwo (mythic) should require 8 Gym Badges."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Mewtwo", "Location", self.player),
            "Guess Mewtwo should be locked without Gym Badges",
        )

    def test_mewtwo_reachable_with_enough_badges(self):
        """Guess Mewtwo becomes reachable with 8 Gym Badges collected."""
        state = CollectionState(self.multiworld)
        badges_collected = 0
        for item in self.multiworld.itempool:
            if item.name == "Gym Badge" and badges_collected < 8:
                state.collect(item)
                badges_collected += 1
        self.assertEqual(badges_collected, 8, "Should have found 8 Gym Badge items in pool")
        self.assertTrue(
            state.can_reach("Guess Mewtwo", "Location", self.player),
            "Guess Mewtwo should be reachable with 8 Gym Badges",
        )


class TestTradeLocks(WorldTestBase):
    """Kanto with trade_locks on — trade evolutions require Link Cable."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto"},
        "trade_locks": 1,
        "type_locks": 0,
        "region_locks": 0,
        "dexsanity": 1,
    }

    def test_alakazam_not_reachable_without_link_cable(self):
        """Guess Alakazam (trade evolution) should require Link Cable."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Alakazam", "Location", self.player),
            "Guess Alakazam should be locked without Link Cable",
        )

    def test_alakazam_reachable_with_link_cable(self):
        """Guess Alakazam becomes reachable once Link Cable is collected."""
        state = CollectionState(self.multiworld)
        for item in self.multiworld.itempool:
            if item.name == "Link Cable":
                state.collect(item)
                break
        self.assertTrue(
            state.can_reach("Guess Alakazam", "Location", self.player),
            "Guess Alakazam should be reachable with Link Cable",
        )


class TestFossilLocks(WorldTestBase):
    """Kanto with fossil_locks on — fossil Pokemon require Fossil Restorer."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto"},
        "fossil_locks": 1,
        "type_locks": 0,
        "region_locks": 0,
        "dexsanity": 1,
    }

    def test_omanyte_not_reachable_without_fossil_restorer(self):
        """Guess Omanyte (fossil) should require Fossil Restorer."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Omanyte", "Location", self.player),
            "Guess Omanyte should be locked without Fossil Restorer",
        )

    def test_omanyte_reachable_with_fossil_restorer(self):
        """Guess Omanyte becomes reachable once Fossil Restorer is collected."""
        state = CollectionState(self.multiworld)
        for item in self.multiworld.itempool:
            if item.name == "Fossil Restorer":
                state.collect(item)
                break
        self.assertTrue(
            state.can_reach("Guess Omanyte", "Location", self.player),
            "Guess Omanyte should be reachable with Fossil Restorer",
        )


class TestUltraBeastLocks(WorldTestBase):
    """Alola with ultra_beast_locks on — Ultra Beasts require Ultra Wormhole."""
    game = "Pokepelago"
    options = {
        "regions": {"Alola"},
        "ultra_beast_locks": 1,
        "type_locks": 0,
        "region_locks": 0,
        "dexsanity": 1,
    }

    def test_nihilego_not_reachable_without_ultra_wormhole(self):
        """Guess Nihilego (Ultra Beast) should require Ultra Wormhole."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Nihilego", "Location", self.player),
            "Guess Nihilego should be locked without Ultra Wormhole",
        )

    def test_nihilego_reachable_with_ultra_wormhole(self):
        """Guess Nihilego becomes reachable once Ultra Wormhole is collected."""
        state = CollectionState(self.multiworld)
        for item in self.multiworld.itempool:
            if item.name == "Ultra Wormhole":
                state.collect(item)
                break
        self.assertTrue(
            state.can_reach("Guess Nihilego", "Location", self.player),
            "Guess Nihilego should be reachable with Ultra Wormhole",
        )


class TestParadoxLocks(WorldTestBase):
    """Paldea with paradox_locks on — Paradox Pokemon require Time Rift."""
    game = "Pokepelago"
    options = {
        "regions": {"Paldea"},
        "paradox_locks": 1,
        "type_locks": 0,
        "region_locks": 0,
        "dexsanity": 1,
    }

    def test_great_tusk_not_reachable_without_time_rift(self):
        """Guess Great Tusk (Paradox) should require Time Rift."""
        state = CollectionState(self.multiworld)
        self.assertFalse(
            state.can_reach("Guess Great Tusk", "Location", self.player),
            "Guess Great Tusk should be locked without Time Rift",
        )

    def test_great_tusk_reachable_with_time_rift(self):
        """Guess Great Tusk becomes reachable once Time Rift is collected."""
        state = CollectionState(self.multiworld)
        for item in self.multiworld.itempool:
            if item.name == "Time Rift":
                state.collect(item)
                break
        self.assertTrue(
            state.can_reach("Guess Great Tusk", "Location", self.player),
            "Guess Great Tusk should be reachable with Time Rift",
        )


if __name__ == "__main__":
    unittest.main()
