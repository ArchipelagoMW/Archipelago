"""
Integration tests for the Pokepelago APWorld using Archipelago's WorldTestBase.

Each class specifies a set of options and automatically runs three inherited tests:
  - test_all_state_can_reach_everything: all items collected → all locations + victory reachable
  - test_empty_state_can_reach_something: at least one location reachable from scratch
  - test_fill: distribute_items_restrictive succeeds and accessibility holds

These mirror the fuzz test categories: check-collect-accessibility, check-item-location-count,
check-placement-item-location-refs, and the basic generation ("default") check.
"""
from test.bases import WorldTestBase


class TestDefaultOptions(WorldTestBase):
    """Default settings: Kanto only, dexsanity + type_locks + region_locks all on."""
    game = "Pokepelago"


class TestNoDexsanity(WorldTestBase):
    """No per-Pokemon locations — only milestone and starting locations."""
    game = "Pokepelago"
    options = {"dexsanity": 0}


class TestNoLocks(WorldTestBase):
    """No type or region locks — all regions freely accessible, no Type Key rules."""
    game = "Pokepelago"
    options = {"type_locks": 0, "region_locks": 0}


class TestDexsanityNoTypeLocks(WorldTestBase):
    """Per-Pokemon locations exist but no Type Key access rules."""
    game = "Pokepelago"
    options = {"dexsanity": 1, "type_locks": 0}


class TestMultiRegion(WorldTestBase):
    """Three regions enabled with all locks active."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto", "Johto", "Hoenn"},
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
        "starter_region": 1,  # Kanto
    }


class TestHisuiPaldea(WorldTestBase):
    """Hisui + Paldea only — regression for old FillError with small region set + all locks.
    Hisui has no starters, so no Type Keys are pre-collected from there."""
    game = "Pokepelago"
    options = {
        "regions": {"Hisui", "Paldea"},
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
    }


class TestAllRegions(WorldTestBase):
    """All ten game regions active with all core locks on."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto", "Johto", "Hoenn", "Sinnoh", "Unova",
                    "Kalos", "Alola", "Galar", "Hisui", "Paldea"},
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
    }


class TestAllNewLocks(WorldTestBase):
    """Kanto + Johto with all new gate locks enabled."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto", "Johto"},
        "legendary_locks": 1,
        "trade_locks": 1,
        "baby_locks": 1,
        "fossil_locks": 1,
        "stone_locks": 1,
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
        "starter_region": 1,  # Kanto
    }


class TestUltraParadoxLocks(WorldTestBase):
    """Alola + Paldea to cover Ultra Beast and Paradox locks."""
    game = "Pokepelago"
    options = {
        "regions": {"Alola", "Paldea"},
        "ultra_beast_locks": 1,
        "paradox_locks": 1,
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
    }


class TestExplicitStarter(WorldTestBase):
    """Explicit starter region (Kanto) and starter Pokemon (Charmander = second)."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto", "Johto"},
        "starter_region": 1,   # Kanto
        "starter_pokemon": 2,  # Charmander
        "type_locks": 1,
        "region_locks": 1,
        "dexsanity": 1,
    }


class TestNoStartingLocations(WorldTestBase):
    """Starting location count set to 0 — no Oak's Lab filler checks."""
    game = "Pokepelago"
    options = {"starting_location_count": 0}


class TestIncludeShinies(WorldTestBase):
    """Shiny Charms enabled — extra filler items added to pool."""
    game = "Pokepelago"
    options = {"include_shinies": 1}


class TestGoalCount(WorldTestBase):
    """Goal type = count with a fixed low number."""
    game = "Pokepelago"
    options = {"goal_type": 1, "goal_count": 50}


class TestAllLocksAllRegionsNoDexsanity(WorldTestBase):
    """All regions + all new locks, but dexsanity off — no per-Pokemon locations."""
    game = "Pokepelago"
    options = {
        "regions": {"Kanto", "Johto", "Hoenn", "Sinnoh", "Unova",
                    "Kalos", "Alola", "Galar", "Hisui", "Paldea"},
        "legendary_locks": 1,
        "trade_locks": 1,
        "baby_locks": 1,
        "fossil_locks": 1,
        "ultra_beast_locks": 1,
        "paradox_locks": 1,
        "stone_locks": 1,
        "dexsanity": 0,
        "type_locks": 0,
        "region_locks": 0,
    }
