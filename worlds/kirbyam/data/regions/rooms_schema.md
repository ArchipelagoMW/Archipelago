# rooms.json Schema

This document describes the canonical structure of `rooms.json`.

`rooms.json` is the source of truth for room-level topology and transition data in KirbyAM.

## File Shape

Top-level type:
- JSON object (`dict`)
- Keys: room region names (for example `REGION_CANDY_CONSTELLATION/ROOM_9_06`)
- Values: room definition objects

Example:

```json
{
  "REGION_CANDY_CONSTELLATION/ROOM_9_06": {
    "locations": [],
    "events": [],
    "exits": [
      "REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_1",
      "REGION_CANDY_CONSTELLATION/ROOM_9_07"
    ],
    "room_sanity": {
      "included": true,
      "location_id": 3961231,
      "bit_index": 143
    },
    "transitions": [
      {
        "destination_room": "REGION_CANDY_CONSTELLATION/ROOM_9_CHEST_1",
        "source_coordinates": {
          "tile": {"x": 24, "y": 30},
          "world": {"x": 187, "y": 32}
        },
        "destination_coordinates": {
          "tile": {"x": 7, "y": 8},
          "world": {"x": 187, "y": 32}
        },
        "transport_type": "other",
        "friendly_name": "Candy Constellation 9-06 to 9-Chest 1",
        "ability_gate": "CanPoundPegs"
      }
    ]
  }
}
```

## Room Object Keys

Each room object contains:

- `locations`:
  - Type: `list[str]`
  - Meaning: location keys physically associated with this room.
  - Examples:
    - Empty room: `"locations": []`
    - Boss room: `"locations": ["BOSS_DEFEAT_3"]`
    - Chest room: `"locations": ["VITALITY_CHEST_CANDY_CONSTELLATION"]`

- `events`:
  - Type: `list[str]`
  - Meaning: event names associated with this room.
  - Examples:
    - Empty room: `"events": []`
    - Lever room: `"events": ["Activate Lever - Moonlight Mansion 2-11"]`

- `exits`:
  - Type: `list[str]`
  - Meaning: destination room keys that are reachable from this room.
  - Rule: this is the canonical adjacency list.

- `room_sanity`:
  - Type: object with keys:
    - `included`: `bool`
    - `location_id`: `int | null`
    - `bit_index`: `int | null`
  - Meaning: room-sanity metadata for tracker/check integration.

- `transitions`:
  - Type: `list[transition_object]`
  - Meaning: directional transition details for exits from this room.
  - Rule: this contains per-path metadata such as coordinates, transport type, and optional gates.

- `logical_subregions` (optional):
  - Type: `dict[str, logical_subregion_object]`
  - Meaning: defines synthetic logic-only sections for this room while preserving a single room-sanity location on the canonical room key.
  - Use when one in-game room has disconnected internal segments that should not imply full traversal access.

- `logical_exit_overrides` (optional):
  - Type: `dict[str, str]`
  - Meaning: per-exit routing override from this room to a destination room's logical subregion.
  - Key: canonical destination room key from `exits`.
  - Value: logical subregion key declared under the destination room's `logical_subregions`.

### Logical Subregion Object Keys

Each logical subregion object contains:

- `exits`:
  - Type: `list[str]`
  - Meaning: adjacency list for the synthetic logic-only region.

- `locations`:
  - Type: `list[str]`
  - Meaning: optional location keys claimed by this logical subregion.

- `events`:
  - Type: `list[str]`
  - Meaning: optional event names claimed by this logical subregion.

## Transition Object Keys

Each transition object contains:

- `destination_room`:
  - Type: `str`
  - Must be one of the values listed in the room's `exits`.

- `source_coordinates`:
  - Type: object
  - Shape:
    - `tile`: `{ "x": int | null, "y": int | null }`
    - `world`: `{ "x": int | null, "y": int | null }`

- `destination_coordinates`:
  - Type: object
  - Shape:
    - `tile`: `{ "x": int | null, "y": int | null }`
    - `world`: `{ "x": int | null, "y": int | null }`

- `transport_type`:
  - Type: `str`
  - Typical values:
    - `other`
    - `hub mirror`
    - `regular two-way mirror`
    - `one-way mirror`
    - `mirra mirror`
    - `warp star`
    - `cannon`

- `friendly_name`:
  - Type: `str`
  - Human-readable directional label.

- `ability_gate` (optional):
  - Type: `str`
  - Present only when a path has a gate condition.
  - Example: `CanPoundPegs`.

## Default Semantics

- If a destination appears in `exits`, the transition is considered valid.
- If no gate field is present for that path, it is considered ungated.
- Gates are path-level (transition-level), not room-level.

## Invariants

Recommended invariants for data integrity:

- Every `transitions[].destination_room` is present in the same room's `exits`.
- No duplicate transition entries for the same source->destination pair.
- `transitions` can be empty for rooms with no directional metadata.
- `exits` remains the authoritative adjacency list.
- `logical_exit_overrides` keys reference destinations already present in `exits`.
- `logical_exit_overrides` values reference logical subregion keys defined on the destination room.

## Notes

- `areas.json` defines high-level area graph connectivity.
- `rooms.json` defines room graph topology and directional path metadata.
- Transition gating logic should read from `rooms.json` transition entries, not a separate transitions dataset.
