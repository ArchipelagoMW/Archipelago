"""Test that seeds can actually be generated and filled with all option combinations."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from BaseClasses import MultiWorld, CollectionState
from worlds.pokepelago import PokepelagoWorld
from worlds.pokepelago.Options import PokepelagoOptions
from worlds.pokepelago.data import GEN_1_TYPES
from Fill import distribute_items_restrictive, FillError

PASS = 0
FAIL = 0


def ok(condition, msg):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"    ✓ {msg}")
    else:
        FAIL += 1
        print(f"    ✗ FAIL: {msg}")


def test_fill(label, regions, dexsanity=1, type_locks=1, region_locks=1, seed=42):
    """Attempt full world generation + fill and verify completability."""
    print(f"\n  [{label}] regions={regions}, dex={dexsanity}, types={type_locks}, reg={region_locks}")

    mw = MultiWorld(1)
    mw.game = {1: "Pokepelago"}
    mw.player_name = {1: "Test"}
    mw.set_seed(seed)

    world = PokepelagoWorld(mw, 1)
    mw.worlds = {1: world}

    # Initialize options
    args = {}
    for name, option_cls in PokepelagoOptions.type_hints.items():
        args[name] = option_cls.from_any(option_cls.default)
    world.options = PokepelagoOptions(**args)

    # Set all regions off first
    region_attr_map = {
        "Kanto": "include_kanto", "Johto": "include_johto", "Hoenn": "include_hoenn",
        "Sinnoh": "include_sinnoh", "Unova": "include_unova", "Kalos": "include_kalos",
        "Alola": "include_alola", "Galar": "include_galar", "Hisui": "include_hisui",
        "Paldea": "include_paldea",
    }
    for attr in region_attr_map.values():
        getattr(world.options, attr).value = 0
    for r in regions:
        getattr(world.options, region_attr_map[r]).value = 1

    world.options.dexsanity.value = dexsanity
    world.options.type_locks.value = type_locks
    world.options.region_locks.value = region_locks

    try:
        world.generate_early()
        world.create_regions()
        mw.state = CollectionState(mw)
        world.create_items()
        world.set_rules()

        # Count locations and items
        locations = [loc for loc in mw.get_locations(1) if loc.address is not None]
        unfilled = [loc for loc in locations if loc.item is None]
        pool = list(mw.itempool)

        print(f"    Locations: {len(locations)}, Unfilled: {len(unfilled)}, Items in pool: {len(pool)}")

        # Check item/location balance
        ok(len(pool) == len(unfilled),
           f"Item count ({len(pool)}) matches unfilled locations ({len(unfilled)})")

        # Try the actual fill
        distribute_items_restrictive(mw)

        # Verify all locations filled
        still_unfilled = [loc for loc in locations if loc.item is None]
        ok(len(still_unfilled) == 0, f"All locations filled ({len(still_unfilled)} unfilled)")

        # Verify completability: can we reach victory with all items?
        all_state = CollectionState(mw)
        for loc in mw.get_locations(1):
            if loc.item:
                all_state.collect(loc.item, True)

        victory = mw.get_location("Pokepelago Victory", 1)
        ok(victory.can_reach(all_state), "Victory reachable with all items collected")

        # Check sphere-0: some locations must be reachable at start
        empty_state = CollectionState(mw)
        sphere0 = [loc for loc in locations if loc.can_reach(empty_state)]
        ok(len(sphere0) > 0, f"Sphere 0 has {len(sphere0)} reachable locations")

        # Check progression: can we reach victory step by step?
        sweep_state = CollectionState(mw)
        max_iterations = len(pool) + 10
        iteration = 0
        while iteration < max_iterations:
            reachable = [loc for loc in locations
                        if loc.can_reach(sweep_state) and loc.item
                        and not sweep_state.has(loc.item.name, 1)]
            if not reachable:
                break
            for loc in reachable:
                sweep_state.collect(loc.item, True)
            iteration += 1

        can_win = victory.can_reach(sweep_state)
        ok(can_win, f"Victory reachable via progressive sweep (after {iteration} iterations)")

        return True

    except FillError as e:
        print(f"    ✗ FILL ERROR: {e}")
        FAIL += 1
        return False
    except Exception as e:
        import traceback
        print(f"    ✗ ERROR: {type(e).__name__}: {e}")
        traceback.print_exc()
        FAIL += 1
        return False


print("=" * 70)
print("FILL TESTS: Verify seeds are completable")
print("=" * 70)

# Test all key option combinations
test_fill("Full locks, Kanto+Johto+Hoenn, dexsanity ON",
          ["Kanto", "Johto", "Hoenn"], dexsanity=1, type_locks=1, region_locks=1)

test_fill("Full locks, Kanto+Johto+Hoenn, dexsanity OFF",
          ["Kanto", "Johto", "Hoenn"], dexsanity=0, type_locks=1, region_locks=1)

test_fill("No type locks, dexsanity ON",
          ["Kanto", "Johto"], dexsanity=1, type_locks=0, region_locks=1)

test_fill("No region locks, dexsanity ON",
          ["Kanto", "Johto"], dexsanity=1, type_locks=1, region_locks=0)

test_fill("All locks OFF, dexsanity OFF",
          ["Kanto", "Johto"], dexsanity=0, type_locks=0, region_locks=0)

test_fill("Kanto only, all locks",
          ["Kanto"], dexsanity=1, type_locks=1, region_locks=1)

test_fill("Hisui only (no starters), all locks",
          ["Hisui"], dexsanity=1, type_locks=1, region_locks=1)

test_fill("Hisui only, dexsanity OFF",
          ["Hisui"], dexsanity=0, type_locks=1, region_locks=1)

test_fill("All regions, all locks, dexsanity ON",
          ["Kanto", "Johto", "Hoenn", "Sinnoh", "Unova", "Kalos", "Alola", "Galar", "Hisui", "Paldea"],
          dexsanity=1, type_locks=1, region_locks=1)

# Test multiple seeds for robustness
for seed in [1, 42, 123, 999, 2024]:
    test_fill(f"Kanto+Johto, full locks, seed={seed}",
              ["Kanto", "Johto"], dexsanity=1, type_locks=1, region_locks=1, seed=seed)

print()
print("=" * 70)
print(f"RESULTS: {PASS} passed, {FAIL} failed")
print("=" * 70)
if FAIL:
    print("\n⚠ SOME TESTS FAILED — seeds may not always be completable!")
    sys.exit(1)
else:
    print("\n✓ ALL SEEDS COMPLETABLE")
