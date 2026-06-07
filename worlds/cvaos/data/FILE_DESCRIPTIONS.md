# cvaos/data — File Descriptions

See [PATHFINDING.md](PATHFINDING.md) for definitions of the terms used here.

---

## Top-level

**`__init__.py`**
Re-exports all public types and collections from the submodules. The single import point for consumers of this package.

**`parse_int.py`**
Utility functions `parse_int`, `parse_dec`, `parse_hex` for converting CSV string values (including `0x`-prefixed hex) to `int | None`. Used by Pydantic `BeforeValidator` annotations throughout the submodules.

---

## `entrance_info/`

**`entrance_info.csv`**
One row per directed physical door. Each physical connection between two rooms appears as **two rows** — one for each direction. Key columns:

| Column | Description |
|---|---|
| `door_number` | Sequential integer ID |
| `door_identifier` | `"{room_identifier}:{dest_room_identifier}"` — directional, not sorted |
| `room_identifier` | The room this door belongs to |
| `dest_room_identifier` | The room on the other side |
| `door_address` | GBA ROM address of this door's data struct |
| `room_address` / `dest_room_address` | ROM addresses of the two connected rooms |
| `x_pos_door` / `y_pos_door` | Position of the door within its room |
| `dest_x_door` / `dest_y_door` | Landing position in the destination room |
| `dest_x_offset_door` / `dest_y_offset_door` | Spawn offset applied on arrival |

**`__init__.py`**
Loads `entrance_info.csv` into `EntranceInfo` Pydantic models at module init. Builds lookup dicts by `door_number`, `door_identifier`, and `door_address`. Also builds `by_room_identifier`: a dict from each `room_identifier` to the set of all `door_identifier` strings touching that room (indexed from both the `room_identifier` and `dest_room_identifier` sides of every row). Exports `doors_for_room(room_identifier)`.

---

## `item_info/`

**`item_info.csv`**
Master item table. Columns: `item_number` (sequential int), `item_category`, `id` (within-category int), `name`.

**`item_importance.csv`**
Archipelago classification for each item. Columns: `item_number`, `name`, `progression`, `useful`, `filler` (boolean flags). Split from `item_info.csv` so classification can be edited independently of the base item data.

**`__init__.py`**
Merges `item_info.csv` and `item_importance.csv` by `name` into `ItemInfo` Pydantic models at module init. Builds lookup dicts by `name`, `(item_category, id)`, and `item_number`. Exports `item_info_collection`.

---

## `pickup_info/`

**`pickup_identifiers.csv`**
ROM-level pickup data. Columns: `pickup_number` (sequential int), `ptr_address` (ROM pointer to this pickup's entry), `simple_name`, `specifier` (disambiguates duplicate names), `flag_offset (varA)` (save-flag bit index into the `0x02000360` collected-pickup bitfield, not a byte offset), `item_offset (varB)` (ROM item byte offset), `type_num`, `type_name`, `subtype_num`.

**`pickup_rooms.csv`**
Spatial and room data for each pickup. Columns: `pickup_number`, `ptr_address`, `room_identifier`, `room_address`, `pickup_number_within_room` (1-based index among pickups in the same room), `x`, `y`.

**`__init__.py`**
Merges `pickup_identifiers.csv` and `pickup_rooms.csv` by `pickup_number` into `PickupInfo` Pydantic models at module init. The `ptr_address` is cross-validated between both files where present. Builds lookup dicts by `ptr_address`, `pickup_number`, and `identifier_key` (`simple_name` + `specifier`). Exports `pickup_info_collection`.

---

## `room_info/`

**`room_identifiers.csv`**
Mapping table between the three room identifier forms. Columns: `room_number` (1-based int), `room_identifier` (zero-padded hex string), `room_address` (ROM address). Used as the join key when loading `room_info.csv`.

**`room_info.csv`**
Detailed room data extracted from ROM. Core columns: `room_address`, `entities_ptr`, `doors_ptr`, `num_doors`, `x`, `y` (room grid position). The remaining columns encode up to 27 entities per room, each as a group of `x_N`, `y_N`, `type_N`, `subtype_N`, `entityID_N`, `varA_N`, `varB_N`. Also includes `Region`, `Region Number`, and `Index in Region`.

**`__init__.py`**
Loads `room_identifiers.csv` as an index, then merges it into each `room_info.csv` row by `room_address` (falling back to `room_index`). Produces `RoomInfo` Pydantic models. Builds lookup dicts by `room_identifier`, `room_address`, and `room_number`. Exports `room_info_collection`.

---

## `routing_info/`

**`entrance_to_entrance_requirements.csv`**
Within-room traversal requirements. Each row describes the abilities needed to move from one entrance node to another within the same room. Key columns:

| Column | Description |
|---|---|
| `entrance_connection_number` | Sequential ID for this traversal rule |
| `RoomID` | The room where the traversal occurs |
| `From` | The neighboring room on the starting-door side |
| `To` | The neighboring room on the destination-door side |
| _(unnamed)_ | Variant integer — distinguishes alternative routes between the same pair of doors |
| `None`, `Glide`, … `Kick` | Boolean ability columns — `TRUE` means that ability alone is sufficient |
| `Misc. combo 1` … `Misc. combo 5` | Parenthetical-token conjunctions, e.g. `"Malphas (DJump), Flying Armor (Glide)"` — each cell is an AND combination; cells are OR alternatives |

Parsed by `routing_info/__init__.py` into `RoutingInfo` objects. Each row becomes one directed edge in the entrance graph: `"{From}:{RoomID}" → "{RoomID}:{To}"`.

**`symmetric_entrance_to_pickup_region_requirements.csv`**
Pickup accessibility requirements. Each row describes the abilities needed to reach a pickup from a specific entrance, and applies symmetrically in both directions. Key columns:

| Column | Description |
|---|---|
| `pickup_number` | Which pickup this row applies to |
| `Room` | The room containing the pickup |
| `Item Name` | Human-readable item name (informational) |
| _(unnamed)_ | Variant integer |
| `dest_room_identifier` | Which entrance(s) this rule applies to: a specific neighboring room ID, a comma-separated list of room IDs, or `Any` (all doors touching `Room`) |
| `None`, `Glide`, … `Kick` | Boolean ability columns (same as above) |
| `Misc. combo 1` … `Misc. combo 5` | Conjunction combo cells (same as above) |

Parsed by `routing_info/__init__.py` into `EntranceToPickupRegionInfo` objects. `dest_room_identifier` values are resolved to entrance identifiers via `_canonical_door_identifier()` (sorted, lower room first) for specific room references, or via `doors_for_room()` (directional) for `Any`.

**`entrance_to_entrance_requirements copy.csv`**
Working copy / backup. Not loaded by any code.

**`__init__.py`**
Defines `AbilityCombo` (IntFlag enum of all ability bits), `RoutingInfo`, and `EntranceToPickupRegionInfo`. Loads both CSVs at module init. Parses ability columns and combo-text cells into minimized ReqMask tuples. Exports `entrance_to_entrance_info_collection`, `entrance_to_pickup_region_info_collection`, and `lookup_pickup_region_requirement()`.

---

## Routing calculation scripts

**`routing_calculation_entrances.py`**
Builds and queries the entrance-only routing graph. Notable types:

- `EntranceId` — helpers for constructing and splitting `"ROOM_A:ROOM_B"` entrance node IDs
- `MaskUtils` — bitwise helpers: `satisfied()`, `usable_options()`, `edge_traversable()`, `decode()`
- `Edge` — directed graph edge with `req_masks` (tuple of alternative ReqMasks) and `connection_number`
- `RoutingGraph` / `RoutingGraphBuilder` — adjacency-list graph and its constructor from a list of `RoutingInfo`
- `RoutingQueries` — graph search: `reachable_entrance_nodes()` (BFS under a fixed have_mask), `reachable_with_options_bfs()` (path-finding BFS), `compute_min_requirements()` (Dijkstra-like, returns `MinReqResult` with subset-minimal ReqMasks for every node), `route_options()` (wraps min-requirements + path reconstruction into `RouteOption` tuples)

**`routing_calculation_entrances_to_items.py`**
Extends the entrance graph with pickup nodes. `RoutingGraphBuilder.from_requirements()` here copies the entrance graph from `routing_calculation_entrances.py` then adds bidirectional edges between entrance nodes and pickup nodes using `EntranceToPickupRegionInfo` data. Convenience functions: `reachable_pickup_numbers_from_entrance()`, `pickup_route_options()`, `default_graph()`.
