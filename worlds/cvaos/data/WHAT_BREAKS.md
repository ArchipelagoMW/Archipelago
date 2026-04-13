# What Breaks Under Asymmetric Entrance Traversal

This document describes which parts of the cvaos pathfinding system assume symmetric entrance traversal, and what goes wrong if that assumption is violated. See [PATHFINDING.md](PATHFINDING.md) for terminology.

"Asymmetric" here means: a route from entrance node A to entrance node B exists, but the reverse route B → A does not (or has different requirements), or neither direction exists at all.

---

## What already handles asymmetry correctly

**`entrance_to_entrance_requirements.csv` and the entrance graph**
Every direction is its own row and can have different requirements or simply be absent. The current data already uses this — e.g. traversing room `003` from the `000` side to the `002` exit requires `DJump`/`HJump`/`Bat` or combos, while the reverse (from `002` to `000`) requires nothing. No symmetry is assumed here.

---

## What breaks

### `_canonical_door_identifier`

Used when the `dest_room_identifier` column in `symmetric_entrance_to_pickup_region_requirements.csv` names a specific neighboring room. It sorts the two room IDs to produce a single identifier regardless of direction, e.g. `_canonical_door_identifier("009", "006")` → `"006:009"`.

This works under symmetric traversal because "the door between rooms 006 and 009" unambiguously identifies one physical connection. Under asymmetric traversal, you might need to distinguish `"006:009"` (arrived in room 009 from room 006) from `"009:006"` (arrived in room 006 from room 009) — for example, a pickup in room 009 might only be accessible via one approach direction. The `dest_room_identifier` column cannot express this distinction since it only stores the neighboring room ID; `_canonical_door_identifier` then resolves it to whichever of the two entrance nodes the sort order happens to produce.

### `doors_for_room()` / `"Any"` expansion — produces a graph shortcut around one-way doors

This is the more serious problem. When `dest_room_identifier = "Any"` for a pickup in room `009`, `doors_for_room("009")` returns identifiers from both sides of every physical connection touching room 009 — including both `"006:009"` (in room 009, at door to 006) and `"009:006"` (in room 006, at door to 009). A bidirectional edge is added for each:

```
"006:009" ↔ PICKUP:N
"009:006" ↔ PICKUP:N
```

Now suppose the door between rooms 006 and 009 is one-way: traversable 006 → 009 but not 009 → 006. In the entrance graph, no edges arrive at `"009:006"` — it is unreachable from the starting entrance. So far this seems harmless.

The problem is the reverse edge `PICKUP:N → "009:006"`. Once the BFS reaches `PICKUP:N` via the legitimate `"006:009"` side, it immediately expands to `"009:006"` as a neighbour. From `"009:006"`, any edges in the entrance graph that depart from that node — i.e. within-room traversals in room 006 that begin from the 009-side door — become reachable.

The pickup node acts as a shortcut that silently bypasses the one-way door:

```
start → ... → "006:009" → PICKUP:N → "009:006" → (room 006 entrance nodes)
```

This produces false-positive reachability: entrance nodes in room 006 that should only be reachable if the 009 → 006 direction is traversable become reachable through the pickup, even though that door direction is blocked.
