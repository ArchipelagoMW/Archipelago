# Access rules for Pokepelago are set inline in PokepelagoWorld methods:
#
# 1. Region entrance rules:
#    state.has("{Region} Pass", player) — set in create_regions() for non-starting regions.
#
# 2. Per-Pokémon "Guess X" rules:
#    state.has_all(type_keys, player) — set in set_rules() when dexsanity + type_locks are ON.
#
# 3. Milestone rules (Guessed X / Caught X {Type}):
#    _make_milestone_rule() counts Pokémon accessible via the region × type matrix.
#    A Pokémon is accessible when its Region Pass (if needed) AND all its Type Keys are held.
#    Milestones are only in logic once enough Pokémon are actually reachable.
#
# 4. Victory rule:
#    Uses the same milestone counting logic — victory requires goal_count Pokémon accessible.
#
# Type Keys are both AP-logic gating (milestone/guess rules) and client-side gating.
# This file is kept for structural completeness.
