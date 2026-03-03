# Pokepelago Milestone Logic Fix

## The Problem

The "Guessed X Pokemon" and "Caught X {Type} Pokemon" milestone locations had **no access rules**, meaning Archipelago's logic considered them all immediately reachable from the start of the game. This caused several critical issues:

### 1. "Guessed 1000 Pokemon" was in logic before you could even reach 200

With multiple regions enabled (e.g., Kanto + Johto + Hoenn = 383 Pokémon), milestones like "Guessed 250 Pokemon" or "Guessed 383 Pokemon" were considered accessible at game start — even though:

- **Region Passes** were required to access non-starting regions (only ~148 Pokémon in Kanto at start)
- **Type Keys** were required to guess Pokémon of specific types (only starter types available at start: Grass, Poison, Fire, Water)

Without access rules, the fill algorithm could place critical progression items (like the Johto Pass) behind a "Guessed 383 Pokemon" milestone, creating an **unwinnable seed** — you'd need to guess 383 Pokémon to get the Johto Pass, but you could only ever reach ~47 Pokémon without it.

### 2. Type milestone locations were defined but never created

The `Locations.py` file defined type milestones (e.g., "Caught 5 Fire Pokemon", "Caught 10 Dragon Pokemon") with proper location IDs, but `create_regions()` in `__init__.py` skipped them entirely. These locations existed in the ID table but were never actually added to the game regions.

### 3. Type milestone counts were hardcoded to Kanto starters

The type milestone step definitions in `Locations.py` subtracted starter-type counts that assumed Kanto starters (Bulbasaur, Charmander, Squirtle). This was incorrect for:
- Non-Kanto starting regions with different starters
- Hisui (which has **no starters** at all)
- Configurations with different active region sets

## The Fix

### Pre-computed Region × Type Requirement Matrix (`generate_early`)

During `generate_early()`, we now analyze every non-starter active Pokémon and record what items are required to access it:

```
For each non-starter Pokémon:
  region_req = "{Region} Pass" if region ≠ starting_region AND region_locks ON, else None
  type_reqs  = frozenset of "{Type} Type Key" for each of its types, if type_locks ON
  
  Group and count Pokémon by (region_req, type_reqs)
```

This produces a **requirement group table** like:

| Region Req | Type Keys Needed | # Pokémon |
|-----------|-----------------|-----------|
| None | {Grass, Poison} | 14 |
| None | {Fire} | 12 |
| None | {Electric} | 6 |
| Johto Pass | {Dark} | 1 |
| Johto Pass | {Dark, Flying} | 1 |
| Hoenn Pass | {Dragon} | 3 |
| ... | ... | ... |

### Milestone Access Rules (`set_rules`)

Each milestone location now has an access rule that sums up how many Pokémon are logically reachable given the player's current items:

```python
def rule(state):
    accessible = 0
    for region_req, type_reqs, count in req_groups:
        if region_req and not state.has(region_req, player):
            continue  # Don't have the region pass
        if type_reqs and not state.has_all(type_reqs, player):
            continue  # Don't have required type key(s)
        accessible += count
        if accessible >= target_count:
            return True  # Enough Pokémon reachable
    return False
```

This is applied to:
- **"Guessed X Pokemon"** milestones — uses the global requirement groups
- **"Caught X {Type} Pokemon"** milestones — uses per-type requirement groups
- **Victory condition** — uses the same logic with the goal count

### Type Milestone Location Creation (`create_regions`)

Type milestone locations are now properly created in `create_regions()`, but only for steps that are actually achievable with the current active Pokémon set. For example, if only 3 Dragon Pokémon exist across active regions, "Caught 5 Dragon Pokemon" won't be created.

### Victory Rule

The victory condition now uses the same milestone logic instead of blindly requiring all Region Passes. This means victory is properly gated by the actual number of accessible Pokémon, not just by having all keys.

## Why This Works

### Correctness: No unreachable milestones in logic

With Kanto as starting region (starters = Bulbasaur, Charmander, Squirtle → Grass, Poison, Fire, Water type keys pre-collected):

| Items Held | Accessible Pokémon | Example Milestones |
|-----------|-------------------|-------------------|
| Nothing (just starter keys) | ~47 Kanto mons with Grass/Poison/Fire/Water types | Guessed 1–47 ✓ |
| + Electric Type Key | ~53 | Guessed 50 ✓ |
| + Johto Pass | ~90+ (starter types across Kanto+Johto) | Guessed 50–90 ✓ |
| + All Type Keys + All Passes | All non-starters | Guessed 383 ✓ |

### Completability: All seeds fillable

The fill algorithm always has enough sphere-0 locations to place progression items:
- Milestone locations in Menu region that only need starter type keys are immediately accessible
- Type Keys and Region Passes can be placed there, unlocking more milestones progressively
- Even Hisui-only (no starters, 0 Pokémon accessible at start) works because non-milestone locations provide sphere-0 slots

### Dual-type gating works correctly

A Pokémon like Kingdra (Water/Dragon, Johto) requires:
- `Johto Pass` (region lock)  
- `Water Type Key` (pre-collected as starter type) ✓
- `Dragon Type Key` (must be found)

It only counts toward milestones when **all** requirements are met.

## Test Coverage

Two test files verify correctness:

- **`test_milestone_logic.py`** — 51 tests across 9 scenarios testing all option combinations (dexsanity ON/OFF, type_locks ON/OFF, region_locks ON/OFF), edge cases (Hisui no starters), incremental item collection, and combined region+type gating
- **`test_fill.py`** — 70 tests verifying actual seed generation and fill completability across 14 configurations and 5 different seeds

## Files Changed

| File | Changes |
|------|---------|
| `__init__.py` | Added requirement group pre-computation in `generate_early()`, `_make_milestone_rule()` helper, milestone access rules in `set_rules()`, type milestone creation in `create_regions()`, updated victory rule |
| `Locations.py` | Removed hardcoded Kanto starter type count adjustments from type milestone definitions |
| `Rules.py` | Updated documentation to reflect new milestone rules |
