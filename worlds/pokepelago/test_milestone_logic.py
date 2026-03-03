"""Comprehensive test suite for Pokepelago milestone logic.

Tests all combinations of dexsanity/type_locks/region_locks and verifies
that milestones are correctly gated by the region × type matrix.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from BaseClasses import MultiWorld, CollectionState
from worlds.pokepelago import PokepelagoWorld
from worlds.pokepelago.Options import PokepelagoOptions
from worlds.pokepelago.data import GEN_1_TYPES

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


def make_world(regions, dexsanity=1, type_locks=1, region_locks=1):
    """Create a fully initialized PokepelagoWorld with the given options."""
    mw = MultiWorld(1)
    mw.game = {1: "Pokepelago"}
    mw.player_name = {1: "Test"}
    mw.set_seed(42)

    world = PokepelagoWorld(mw, 1)
    mw.worlds = {1: world}

    # Initialize options
    args = {}
    for name, option_cls in PokepelagoOptions.type_hints.items():
        args[name] = option_cls.from_any(option_cls.default)
    world.options = PokepelagoOptions(**args)

    # Set all regions off first
    for attr in ["include_kanto", "include_johto", "include_hoenn", "include_sinnoh",
                 "include_unova", "include_kalos", "include_alola", "include_galar",
                 "include_hisui", "include_paldea"]:
        getattr(world.options, attr).value = 0

    # Enable requested regions
    region_attr_map = {
        "Kanto": "include_kanto", "Johto": "include_johto", "Hoenn": "include_hoenn",
        "Sinnoh": "include_sinnoh", "Unova": "include_unova", "Kalos": "include_kalos",
        "Alola": "include_alola", "Galar": "include_galar", "Hisui": "include_hisui",
        "Paldea": "include_paldea",
    }
    for r in regions:
        getattr(world.options, region_attr_map[r]).value = 1

    world.options.dexsanity.value = dexsanity
    world.options.type_locks.value = type_locks
    world.options.region_locks.value = region_locks

    world.generate_early()
    world.create_regions()
    mw.state = CollectionState(mw)
    world.create_items()
    world.set_rules()

    return mw, world


def fresh_state(mw):
    """Create a fresh CollectionState (no items collected)."""
    return CollectionState(mw)


def state_with_items(mw, item_names):
    """Create a state with specific items collected."""
    state = CollectionState(mw)
    for name in item_names:
        # Find the item in the pool or create it
        item = mw.worlds[1].create_item(name)
        state.collect(item, True)
    return state


def get_loc(mw, name):
    """Get a location by name."""
    return mw.get_location(name, 1)


def loc_exists(mw, name):
    """Check if a location exists."""
    try:
        mw.get_location(name, 1)
        return True
    except KeyError:
        return False


# ════════════════════════════════════════════════════════════
print("=" * 70)
print("TEST 1: dexsanity=ON, type_locks=ON, region_locks=ON")
print("        Kanto + Johto + Hoenn")
print("=" * 70)
mw, world = make_world(["Kanto", "Johto", "Hoenn"], dexsanity=1, type_locks=1, region_locks=1)

# Fresh state: only pre-collected starter type keys (Grass, Poison, Fire, Water)
s0 = fresh_state(mw)

# 1a. Low milestones accessible at start
ok(get_loc(mw, "Guessed 1 Pokemon").can_reach(s0), "Guessed 1 accessible at start")
ok(get_loc(mw, "Guessed 5 Pokemon").can_reach(s0), "Guessed 5 accessible at start")

# 1b. High milestones NOT accessible at start
ok(not get_loc(mw, "Guessed 250 Pokemon").can_reach(s0), "Guessed 250 NOT accessible at start")
ok(not get_loc(mw, "Guessed 383 Pokemon").can_reach(s0), "Guessed 383 NOT accessible at start")

# 1c. Type milestones: Dragon NOT accessible (no Dragon Type Key)
ok(loc_exists(mw, "Caught 1 Dragon Pokemon"), "Dragon type milestone exists")
ok(not get_loc(mw, "Caught 1 Dragon Pokemon").can_reach(s0),
   "Caught 1 Dragon NOT accessible without Dragon Type Key")

# 1d. Type milestones: Fire accessible (starter type key)
ok(get_loc(mw, "Caught 1 Fire Pokemon").can_reach(s0),
   "Caught 1 Fire accessible (starter type key)")

# 1e. Add Dragon Type Key → Dragon milestones become accessible
s_dragon = state_with_items(mw, ["Dragon Type Key"])
ok(get_loc(mw, "Caught 1 Dragon Pokemon").can_reach(s_dragon),
   "Caught 1 Dragon accessible with Dragon Type Key")

# 1f. Dual-type: Kingdra (#230, Water/Dragon) is in Johto.
#     Need: Johto Pass + Water Type Key (pre-collected) + Dragon Type Key
#     Without Johto Pass: Dragon milestones limited to Kanto dragons only
s_dragon_no_johto = state_with_items(mw, ["Dragon Type Key"])
kanto_dragons = 3  # Dratini, Dragonair, Dragonite
s_dragon_johto = state_with_items(mw, ["Dragon Type Key", "Johto Pass"])

# With Dragon Key only: should reach Kanto dragons
ok(get_loc(mw, "Caught 2 Dragon Pokemon").can_reach(s_dragon_no_johto),
   "Caught 2 Dragon accessible with just Dragon Key (Kanto has 3 pure Dragon)")

# 1g. Region gating: add Johto Pass → more pokemon accessible
s_johto = state_with_items(mw, ["Johto Pass"])
ok(get_loc(mw, "Guessed 50 Pokemon").can_reach(s_johto),
   "Guessed 50 accessible with Johto Pass (more Water/Fire/etc in Johto)")
ok(not get_loc(mw, "Guessed 250 Pokemon").can_reach(s_johto),
   "Guessed 250 NOT accessible with just Johto Pass (still need type keys + Hoenn)")

# 1h. With ALL type keys + ALL region passes → everything accessible
all_items = [f"{t} Type Key" for t in GEN_1_TYPES] + ["Johto Pass", "Hoenn Pass"]
s_all = state_with_items(mw, all_items)
ok(get_loc(mw, "Guessed 383 Pokemon").can_reach(s_all),
   "Guessed 383 accessible with all type keys + all region passes")

# 1i. Guess locations exist (dexsanity ON)
ok(loc_exists(mw, "Guess Pikachu"), "Guess Pikachu location exists (dexsanity ON)")

# 1j. Per-pokemon type gating: Pikachu (Electric) needs Electric Type Key
ok(not get_loc(mw, "Guess Pikachu").can_reach(s0),
   "Guess Pikachu NOT accessible without Electric Type Key")
s_electric = state_with_items(mw, ["Electric Type Key"])
ok(get_loc(mw, "Guess Pikachu").can_reach(s_electric),
   "Guess Pikachu accessible with Electric Type Key")

# 1k. Victory gating
ok(not get_loc(mw, "Pokepelago Victory").can_reach(s0),
   "Victory NOT accessible at start")
ok(get_loc(mw, "Pokepelago Victory").can_reach(s_all),
   "Victory accessible with all items")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 2: dexsanity=OFF, type_locks=ON, region_locks=ON")
print("        Kanto + Johto")
print("=" * 70)
mw2, world2 = make_world(["Kanto", "Johto"], dexsanity=0, type_locks=1, region_locks=1)

s0 = fresh_state(mw2)

# 2a. No Guess locations (dexsanity OFF)
ok(not loc_exists(mw2, "Guess Pikachu"), "Guess Pikachu does NOT exist (dexsanity OFF)")

# 2b. Milestone locations still exist
ok(loc_exists(mw2, "Guessed 1 Pokemon"), "Guessed 1 milestone exists")
ok(loc_exists(mw2, "Guessed 100 Pokemon"), "Guessed 100 milestone exists")

# 2c. Type milestones still exist
ok(loc_exists(mw2, "Caught 1 Fire Pokemon"), "Caught 1 Fire milestone exists")

# 2d. Milestones still gated by type keys
ok(get_loc(mw2, "Guessed 1 Pokemon").can_reach(s0), "Guessed 1 accessible at start")
ok(not get_loc(mw2, "Caught 1 Dragon Pokemon").can_reach(s0),
   "Caught 1 Dragon NOT accessible without Dragon Type Key (dexsanity OFF)")

# 2e. Region gating still works for milestones
ok(not get_loc(mw2, "Guessed 248 Pokemon").can_reach(s0),
   "Guessed 248 NOT accessible at start (need Johto Pass + type keys)")

# 2f. With all items: accessible
all_items = [f"{t} Type Key" for t in GEN_1_TYPES] + ["Johto Pass"]
s_all = state_with_items(mw2, all_items)
ok(get_loc(mw2, "Guessed 248 Pokemon").can_reach(s_all),
   "Guessed 248 accessible with all items (dexsanity OFF)")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 3: dexsanity=ON, type_locks=OFF, region_locks=ON")
print("        Kanto + Johto")
print("=" * 70)
mw3, world3 = make_world(["Kanto", "Johto"], dexsanity=1, type_locks=0, region_locks=1)

s0 = fresh_state(mw3)

# 3a. Without type locks, all starting region pokemon accessible immediately
ok(get_loc(mw3, "Guessed 100 Pokemon").can_reach(s0),
   "Guessed 100 accessible at start (no type locks, 148 Kanto non-starters)")
ok(not get_loc(mw3, "Guessed 248 Pokemon").can_reach(s0),
   "Guessed 248 NOT accessible (need Johto Pass, even without type locks)")

# 3b. Guess locations don't need type keys
ok(get_loc(mw3, "Guess Pikachu").can_reach(s0),
   "Guess Pikachu accessible without type keys (type_locks OFF)")

# 3c. Dragon milestones accessible without Dragon Type Key (no type locks)
ok(get_loc(mw3, "Caught 1 Dragon Pokemon").can_reach(s0),
   "Caught 1 Dragon accessible without type key (type_locks OFF)")

# 3d. Region still gates
s_johto = state_with_items(mw3, ["Johto Pass"])
ok(get_loc(mw3, "Guessed 248 Pokemon").can_reach(s_johto),
   "Guessed 248 accessible with Johto Pass (no type locks needed)")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 4: dexsanity=ON, type_locks=ON, region_locks=OFF")
print("        Kanto + Johto")
print("=" * 70)
mw4, world4 = make_world(["Kanto", "Johto"], dexsanity=1, type_locks=1, region_locks=0)

s0 = fresh_state(mw4)

# 4a. Region passes NOT needed (region_locks OFF)
#     But type keys still needed. Starter types: Grass, Poison, Fire, Water
#     All Kanto+Johto pokemon with those types are accessible across BOTH regions
ok(get_loc(mw4, "Guessed 50 Pokemon").can_reach(s0),
   "Guessed 50 accessible at start (no region locks, starter types across Kanto+Johto)")

# 4b. Type keys still gate
ok(not get_loc(mw4, "Caught 1 Dragon Pokemon").can_reach(s0),
   "Caught 1 Dragon NOT accessible without Dragon Type Key (type_locks ON)")

# 4c. With all type keys: all milestones accessible (no region gates)
all_type_keys = [f"{t} Type Key" for t in GEN_1_TYPES]
s_types = state_with_items(mw4, all_type_keys)
ok(get_loc(mw4, "Guessed 248 Pokemon").can_reach(s_types),
   "Guessed 248 accessible with all type keys (no region locks)")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 5: dexsanity=OFF, type_locks=OFF, region_locks=OFF")
print("        Kanto + Johto")
print("=" * 70)
mw5, world5 = make_world(["Kanto", "Johto"], dexsanity=0, type_locks=0, region_locks=0)

s0 = fresh_state(mw5)

# 5a. Everything immediately accessible
ok(get_loc(mw5, "Guessed 1 Pokemon").can_reach(s0),
   "Guessed 1 accessible (no locks)")
ok(get_loc(mw5, "Guessed 248 Pokemon").can_reach(s0),
   "Guessed 248 accessible (all locks OFF)")
ok(get_loc(mw5, "Caught 1 Dragon Pokemon").can_reach(s0),
   "Caught 1 Dragon accessible (all locks OFF)")
ok(get_loc(mw5, "Caught 1 Ice Pokemon").can_reach(s0),
   "Caught 1 Ice accessible (all locks OFF)")

# 5b. No Guess locations
ok(not loc_exists(mw5, "Guess Pikachu"), "Guess Pikachu does NOT exist (dexsanity OFF)")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 6: Hisui only (no starters) — Edge case")
print("        dexsanity=ON, type_locks=ON, region_locks=ON")
print("=" * 70)
mw6, world6 = make_world(["Hisui"], dexsanity=1, type_locks=1, region_locks=1)

s0 = fresh_state(mw6)

# 6a. No starters means no pre-collected type keys → nothing accessible at start
ok(world6.starter_names == set(), "Hisui has no starters")
ok(not get_loc(mw6, "Guessed 1 Pokemon").can_reach(s0),
   "Guessed 1 NOT accessible at start (no starters = no type keys)")

# 6b. After receiving a type key, some pokemon become accessible
# Hisui pokemon: Wyrdeer (Normal/Psychic), Kleavor (Bug/Rock), Ursaluna (Ground/Normal),
#                Basculegion (Water/Ghost), Sneasler (Fighting/Poison),
#                Overqwil (Dark/Poison), Enamorus (Fairy/Flying)
s_normal = state_with_items(mw6, ["Normal Type Key"])
# Wyrdeer needs Normal+Psychic, Ursaluna needs Ground+Normal - need both type keys
ok(not get_loc(mw6, "Guessed 1 Pokemon").can_reach(s_normal),
   "Guessed 1 NOT accessible with just Normal Key (all Hisui Normal mons are dual-type)")

s_normal_psychic = state_with_items(mw6, ["Normal Type Key", "Psychic Type Key"])
ok(get_loc(mw6, "Guessed 1 Pokemon").can_reach(s_normal_psychic),
   "Guessed 1 accessible with Normal+Psychic Keys (Wyrdeer = Normal/Psychic)")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 7: Incremental item collection — verify counts increase")
print("        Kanto only, type_locks=ON, region_locks=ON")
print("=" * 70)
mw7, world7 = make_world(["Kanto"], dexsanity=1, type_locks=1, region_locks=1)

# Count accessible pokemon incrementally as type keys are added
def count_accessible(mw, items):
    """Count how many non-starter pokemon are logically accessible."""
    state = state_with_items(mw, items)
    count = 0
    for loc in mw.get_locations(1):
        if loc.name.startswith("Guess ") and loc.address is not None:
            if loc.can_reach(state):
                count += 1
    return count

# Start: only starter types (Grass, Poison, Fire, Water are pre-collected)
base = count_accessible(mw7, [])
print(f"    Base accessible (starter types): {base}")

# Add Electric
with_electric = count_accessible(mw7, ["Electric Type Key"])
print(f"    + Electric Type Key: {with_electric}")
ok(with_electric > base, f"Adding Electric increases count ({base} → {with_electric})")

# Add Fighting
with_electric_fighting = count_accessible(mw7, ["Electric Type Key", "Fighting Type Key"])
print(f"    + Electric + Fighting: {with_electric_fighting}")
ok(with_electric_fighting > with_electric,
   f"Adding Fighting increases count ({with_electric} → {with_electric_fighting})")

# Add all type keys
all_type_keys = [f"{t} Type Key" for t in GEN_1_TYPES]
with_all = count_accessible(mw7, all_type_keys)
print(f"    + All type keys: {with_all}")
# 151 total: 148 non-starters + 3 starters (starters have Guess locations too)
ok(with_all == 151, f"All type keys = all 151 Kanto pokemon incl. starters (got {with_all})")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 8: Region pass incremental — Kanto + Johto + Hoenn")
print("        type_locks=OFF to isolate region gating")
print("=" * 70)
mw8, world8 = make_world(["Kanto", "Johto", "Hoenn"], dexsanity=1, type_locks=0, region_locks=1)

# count_accessible counts Guess locations (incl. starters) — no type locks so all accessible
base = count_accessible(mw8, [])
print(f"    Base accessible (Kanto only): {base}")
ok(base == 151, f"All 151 Kanto pokemon accessible (no type locks) (got {base})")

with_johto = count_accessible(mw8, ["Johto Pass"])
print(f"    + Johto Pass: {with_johto}")
ok(with_johto == 151 + 100, f"Kanto(151) + Johto(100) = 251 (got {with_johto})")

with_both = count_accessible(mw8, ["Johto Pass", "Hoenn Pass"])
print(f"    + Johto + Hoenn Pass: {with_both}")
ok(with_both == 151 + 100 + 135, f"Kanto(151) + Johto(100) + Hoenn(135) = 386 (got {with_both})")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print("TEST 9: Combined region + type gating")
print("        Kanto + Johto, type_locks=ON, region_locks=ON")
print("=" * 70)
mw9, world9 = make_world(["Kanto", "Johto"], dexsanity=1, type_locks=1, region_locks=1)

# Johto Dark pokemon: Umbreon(Dark), Murkrow(Dark/Flying), Sneasel(Dark/Ice),
#                     Houndour(Dark/Fire), Houndoom(Dark/Fire), Tyranitar(Rock/Dark)
# These require Johto Pass + Dark Type Key (+ other type keys for dual-types)

# Without Johto Pass: Kanto has no Dark pokemon → Caught 1 Dark needs Johto Pass
s_dark = state_with_items(mw9, ["Dark Type Key"])
ok(not get_loc(mw9, "Caught 1 Dark Pokemon").can_reach(s_dark),
   "Caught 1 Dark NOT accessible with Dark Key alone (no Dark pokemon in Kanto!)")

# With Johto Pass + Dark Key: Umbreon is pure Dark → accessible
s_dark_johto = state_with_items(mw9, ["Dark Type Key", "Johto Pass"])
ok(get_loc(mw9, "Caught 1 Dark Pokemon").can_reach(s_dark_johto),
   "Caught 1 Dark accessible with Dark Key + Johto Pass (Umbreon)")

# Dual-type: Murkrow (Dark/Flying) needs Dark + Flying + Johto Pass
s_dark_johto_no_flying = state_with_items(mw9, ["Dark Type Key", "Johto Pass"])
# This gives us Umbreon (pure Dark) = 1 Dark pokemon
# For "Caught 2 Dark" we need another: Murkrow(Dark/Flying) needs Flying Key too
s_dark_flying_johto = state_with_items(mw9, ["Dark Type Key", "Flying Type Key", "Johto Pass"])
# Now we have Umbreon + Murkrow = 2 Dark pokemon
ok(get_loc(mw9, "Caught 2 Dark Pokemon").can_reach(s_dark_flying_johto),
   "Caught 2 Dark accessible with Dark+Flying Keys + Johto Pass (Umbreon + Murkrow)")


# ════════════════════════════════════════════════════════════
print()
print("=" * 70)
print(f"RESULTS: {PASS} passed, {FAIL} failed")
print("=" * 70)
if FAIL:
    print("\n⚠ SOME TESTS FAILED — see above for details")
    sys.exit(1)
else:
    print("\n✓ ALL TESTS PASSED")
