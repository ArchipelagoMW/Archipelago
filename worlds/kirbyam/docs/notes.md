# Kirby & The Amazing Mirror (GBA) - Address Policy Notes

## POC baseline

- Baseline ROM for the POC is `Kirby & The Amazing Mirror (USA).gba` only.
- Multi-ROM parity (EU/JP/VC) is out of scope for this phase.
- Non-USA testing remains tracked separately (`#99`, `#100`, `#101`, `#102`).

## Address domain separation (locked policy)

Do not mix these two domains:

1. AP transport/mailbox addresses
- Purpose: client/ROM communication contract.
- Source of truth: `worlds/kirbyam/data/addresses.json` under `ram.transport`.
- Examples: `incoming_item_flag`, `incoming_item_id`, `delivered_item_index`.

2. Native game-state addresses
- Purpose: in-game progression/check/goal state.
- Source of truth: `worlds/kirbyam/data/native_address_policy.json` and `ram.native` in `worlds/kirbyam/data/addresses.json`.
- Current integrated native signal: `shard_bitfield_native` at `0x02038970`.

Rule: AP transport fields must never be treated as native gameplay truth.

## Status taxonomy

- `candidate`: Derived from workbook/cheat/reverse-engineering source; requires live confirmation.
- `integrated`: Used by current client/ROM path but not yet promoted to fully live-verified policy status.
- `verified`: Confirmed by repeatable live memory observation on USA ROM.

Current high-level status:

| Signal type | Candidate | Integrated | Verified |
| --- | --- | --- | --- |
| Shard progression | Yes | Yes | Not yet policy-promoted |
| Dungeon boss defeat | Yes | Yes (probe-only) | No |
| Final boss defeat | Yes | Yes | No |
| 100% completion | Yes | Yes | No |

Detailed signal registry: `worlds/kirbyam/data/native_address_policy.json`

## Promotion criteria (candidate/integrated -> verified)

All criteria below must be met:

1. Observed on USA ROM in BizHawk during real gameplay action.
2. Before/after transition recorded with exact address, width, and expected semantics.
3. Reproduced in at least 3 independent attempts with consistent transition behavior.
4. Persistence checked across room transitions and save/reload as applicable.
5. Cross-domain sanity check confirms no AP mailbox field is used as native source.
6. Registry and matrix updated together:
- `worlds/kirbyam/data/native_address_policy.json`
- `worlds/kirbyam/ADDRESS_VERIFICATION_MATRIX.md`

## POC shard mapping reference

Current proof-of-concept shard bit mapping:

- bit 0 -> `SHARD_1`
- bit 1 -> `SHARD_2`
- bit 2 -> `SHARD_3`
- bit 3 -> `SHARD_4`
- bit 4 -> `SHARD_5`
- bit 5 -> `SHARD_6`
- bit 6 -> `SHARD_7`
- bit 7 -> `SHARD_8`

## Implementation notes

- Transport contract details: `worlds/kirbyam/PROTOCOL.md`
- Verification workflow: `worlds/kirbyam/docs/BIZHAWK_TESTING_GUIDE.md`
- Native signal status registry: `worlds/kirbyam/data/native_address_policy.json`

## Issue #232: Automated ROM Patch Rebuild Smoke in CI

### Problem
KirbyAM CI previously built `.apworld` artifacts with `--skip-patch`, which did not automatically exercise the ROM payload build + bsdiff patch generation path.

### Solution
Added workflow `.github/workflows/kirbyam-rom-patch-smoke.yml` to run on KirbyAM changes and execute end-to-end patch generation steps:
- Install ARM toolchain + Python dependency `bsdiff4`
- Build payload via `make`
- Generate `worlds/kirbyam/data/base_patch.bsdiff4` through `worlds/kirbyam/build.py`
- Upload key outputs (`base_patch.bsdiff4`, `kirbyam.apworld`, `payload.bin`, `patch_rom.log`) as artifacts

### CI ROM Input Policy
To avoid distributing copyrighted ROM data in CI, this workflow uses a deterministic dummy 2 MiB `kirby.gba` file only for pipeline validation.

Implications:
- CI smoke proves that payload compilation and patch-file generation mechanics are functional.
- CI smoke does **not** validate runtime correctness against a real clean USA ROM image.
- Release-quality patch validation against a real clean ROM remains a local/manual maintainer responsibility.

## Issue #239: Release Asset Publication and Patched APWorld Packaging

### Problem
Tag-driven KirbyAM releases drifted from the actual shipping contract in two ways:
- the release build used `python build.py --skip-patch`, so `kirbyam.apworld` could be published without a refreshed `base_patch.bsdiff4`
- the release upload step could target a stray `untagged-*` draft release instead of the visible `kirbyam-v*` release, leaving the tagged release with no attached asset

### Solution
Updated `.github/workflows/kirbyam-apworld.yml` so valid `kirbyam-v*` tags now:
- package the committed `worlds/kirbyam/data/base_patch.bsdiff4` with `python build.py --skip-patch`
- ensure the matching tagged GitHub release exists, prune stale non-APWorld assets, and upload `kirbyam.apworld` directly to that tagged release via `gh release upload --clobber`

### Release ROM Input Policy
- Branch, PR, and tag artifact builds all use `--skip-patch` for packaging and release publication.
- Maintainers refresh `worlds/kirbyam/data/base_patch.bsdiff4` locally from the clean USA ROM, then commit that artifact before creating the release tag.
- Release builds fail fast if the committed `base_patch.bsdiff4` is missing or empty, rather than silently publishing an unpatched APWorld.

## Issue #109: Reset-Safe Mirror Shard Grant Handling

### Problem
Previously, mirror shard grants were stored only in EWRAM (0x02038970). When the player received a shard without changing rooms and then reset/crashed, the shard was lost because EWRAM is volatile.

### Solution
Added SRAM persistence layer in `worlds/kirbyam/kirby_ap_payload/ap_payload.c`:
- Primary shard bitfield written to SRAM offset 0x12
- Checksum validation fields written to SRAM offsets 0x18, 0x1A, 0x1C to prevent save corruption
- Function `persist_shard_to_sram()` called whenever a shard is granted via mailbox

### Addresses Used (Issue #109 Investigation Candidates)
- SRAM 0x12 (decimal 18): Primary shard persistence field  
- SRAM 0x18 (decimal 24): Checksum field 1 (inverted XOR)
- SRAM 0x1A (decimal 26): Checksum field 2 (offset-based)
- SRAM 0x1C (decimal 28): Checksum field 3 (derived from 1+2)

These addresses were selected from the candidate pool mentioned in Issue #109 (0x18, 0x1A, 0x1C, 0x32C, 0x32E, 0x330) based on:
1. Known save file structure from KatAM disassembly (treasures.h)
2. Game behavior observation: values that change when both receiving shards AND changing rooms
3. Safety margin: checksum fields placed between other save fields to minimize conflict risk

### Validation
- Tests in `worlds/kirbyam/test/test_reset_safe_shards.py` verify:
  - SRAM persistence addresses are defined
  - `persist_shard_to_sram()` function is called
  - Checksum fields are updated correctly
  - Issue #109 candidate addresses are documented in code

### Next Steps (Manual Testing)
Future BizHawk validation should confirm:
1. Add shard via Archipelago mailbox
2. Do NOT enter a new room
3. Reset/power-cycle emulator
4. Verify shard persists after reload
5. Verify save file is not corrupted

## Issue #38: Goal Location for Dark Mind

### Problem
Completion logic was still tied directly to "all shard items collected" and used auto-collected Dimension Mirror events, so the selected goal was not represented as a real AP location.

### Solution
Goal handling now uses explicit goal locations:
- Goal=Dark Mind -> requires `Defeat Dark Mind`
- Goal=100% -> requires `100% Save File`
- Goal locations live in `REGION_DIMENSION_MIRROR/MAIN` and are locked progression events, not randomized pool entries
- The BizHawk client reports the selected goal location from native AI-state polling (`ai_kirby_state_native`), then sends goal status after the server acknowledges that goal location

Dimension Mirror access remains shard-gated, so this preserves current progression while ensuring completion is represented by a dedicated AP goal location instead of an auto-collected region event.

## Issue #194: Native Dark Mind Goal Detection via AI State

### Problem
Goal completion used temporary client-side aggregation logic instead of native game-state semantics.

### Solution
Integrated native AI-state goal polling from `ai_kirby_state_native` (`0x0203AD2C`):
- Goal=Dark Mind: trigger selected goal location when value is `9999`
- Goal=100%: trigger selected goal location when value is `10000`
- In Dark Mind mode, `10000` is treated as post-clear progression and is not used as first-clear trigger

Client continues to send `CLIENT_GOAL` only after server acknowledgement of the selected goal location check, preserving idempotent AP completion reporting.

## Issue #62: Deterministic Disconnect/Reconnect Resynchronization

### Problem
Reconnect windows can temporarily expose partial AP context state (for example, `ctx.server` exists but `ctx.server.socket` is not yet present). The watcher precondition needed to be explicit and tolerant of those partial states so reconnect behavior remains deterministic.

### Solution
- Added `_server_session_ready(...)` guard in the KirbyAM client watcher to require:
  - `ctx.server` exists
  - `ctx.server.socket` exists
  - socket is not closed
  - `ctx.slot_data` is present
- Added reconnect-entry transition handling:
  - on first watcher tick after AP session readiness, reset transient diagnostics/probe caches once
  - emit info log: `KirbyAM: AP session ready; reconnect-safe reconciliation active`
- Preserved existing reconnect convergence semantics:
  - level-based location resend against `checked_locations`
  - delivery cursor reconciliation against ROM `debug_item_counter`
  - idempotent goal-location + `CLIENT_GOAL` sequencing

### Validation
- Added tests for watcher no-op when socket is missing or closed.
- Added test that reconnect-entry resets transient state and only logs readiness once per session-ready transition.

## Issue #83: In-Game Notification Pipeline (Receive + Send)

### Problem
KirbyAM processed delivery and ItemSend traffic without a dedicated player-facing
notification contract, which made receive/send events opaque in normal play.

### Solution
- Added a KirbyAM notification pipeline with two event sources:
  - Receive notifications on mailbox ACK completion for delivered indexes.
  - Send notifications from `PrintJSON` `ItemSend` packets when local slot is
    the sender.
- Added reconnect-safe dedupe state:
  - Receive dedupe by delivered index.
  - Send dedupe by `(item_id, sender_id, receiver_id, location_id)` tuple.
- Added optional slot-data toggles (default enabled):
  - `enable_receive_notifications`
  - `enable_send_notifications`
- Phase 1 display path uses BizHawk `display_message`.

### #73 Implementation-Ready Criteria (Receive)
- Notification must trigger only after mailbox ACK for a newly delivered index.
- Notification content must include item + sender context when resolvable.
- Reconnect/resync must not replay already shown receive notifications.

### #74 Implementation-Ready Criteria (Send)
- Notification must trigger only when local slot is ItemSend sender.
- Unrelated ItemSend packets must not notify locally.
- Reconnect replay/echoes must dedupe and avoid spam.

### Test Plan Baseline
- Automated:
  - receive notification trigger + dedupe tests
  - send `PrintJSON` local-sender trigger + dedupe tests
  - toggle-off suppression tests
- Manual BizHawk:
  - verify readable receive/send notifications
  - verify reconnect does not replay old notifications

## Issue #73: Receive Notifications (Exactly-Once Per Delivered Item)

### Problem
Receive notifications needed explicit per-item delivery guarantees tied to the
actual mailbox ACK path, not just generic packet flow.

### Implementation
- Receive notifications are emitted from ACK-completed delivery indexes.
- Notification content resolves item and sender names when available.
- Exactly-once receive behavior is enforced by delivered-index dedupe.
- Malformed skipped entries emit no receive notification.
- Cursor reconciliation (rewind/fast-forward) alone emits no receive notification.

### Validation
- Added targeted tests for:
  - ACK-triggered receive notification exactly once per index
  - malformed-entry skip suppression
  - reconnect replay dedupe on rewound indexes
  - no notification on fast-forward-only reconciliation

## Issue #44: Final Boss Access Rules (Dimension Mirror Sequence)

### Problem
`REGION_DIMENSION_MIRROR/MAIN` modeled the final-boss area as a flat region with
no internal sequencing: both goal locations (`Defeat Dark Mind`, `100% Save File`)
were peers with no representation of the Dark Meta Knight prerequisite encounter.
The `ADDRESS_VERIFICATION_MATRIX.md` also lacked entries for the Dimension Mirror
boss encounters.

### Solution

`areas.json` now includes a `Defeat Dark Meta Knight (Dimension Mirror)` event
in `REGION_DIMENSION_MIRROR/MAIN`. This event:
- Is accessible once the region is entered (which requires all 8 shards).
- Represents the in-sequence Dark Meta Knight rematch, distinct from the Radish
  Ruins disguise fight (tracked separately under #43).
- Provides the prerequisite event item that gates `Defeat Dark Mind`.

`rules.py` now enforces:
- `Defeat Dark Mind` goal location: requires all 8 shards **and** `Defeat Dark
  Meta Knight (Dimension Mirror)` event.
- `100% Save File` goal location: requires all 8 shards only (the 100%
  completion signal incorporates full clear semantics independently).

### `ai_kirby_state_native` Value Semantics (Address: `0x0203AD2C`, u32)

**Source**: Live-mapped AI state candidate integrated for goal mode polling
(from `native_address_policy.json`, entries `final_boss_defeat` and
`full_clear_completion`).

**Current status**: `integrated` — used in production code; not yet `verified`
(no confirmed 3-observation BizHawk evidence with pre/post capture on record).

| Value | Meaning | Used by goal mode |
|---|---|---|
| `300` | Normal gameplay-active | Gameplay gate (Issue #56) |
| `9999` | Dark Mind clear trigger | `dark_mind` goal |
| `10000` | 100% completion signal | `100` goal |

**On 9999 vs 10000 in dark_mind mode**: `10000` is post-clear progression and
must NOT be used as the first-clear trigger for `dark_mind`. The client
explicitly rejects `10000` when in `dark_mind` goal mode.

**Promotion criteria (integrated → verified)**:
1. Capture pre-action ai_kirby_state value in BizHawk memory viewer.
2. Complete the final boss sequence and capture post-action value.
3. Record frame-count and confirm value persists through at least one save/reload.
4. Repeat 3 times for each of `9999` (Dark Mind) and `10000` (100%) signals.

Until promoted, treat both values as valid for production use but flag for
follow-up verification in any regression investigation.

## Issue #110: Boss Defeat Address Identification Beyond Shards

### Solution
Added observational boss-candidate probing in `worlds/kirbyam/client.py`:
- Reads `boss_mirror_table_native` from `addresses.json` (`0x02028C14`)
- Captures a 32-byte snapshot each poll
- Logs only rising-edge bit transitions (0 -> 1) with absolute address + bit index
- Does not send AP location checks yet (probe-only, safe for production)

### Validation
- Tests in `worlds/kirbyam/test/test_client.py` verify:
  - probe is skipped when native address is missing
  - rising-edge transitions produce expected log entries

### Scope note
This change is instrumentation groundwork for Issue #110 address identification.
It does not yet convert boss candidate transitions into authoritative AP location
checks or implement shard-undo behavior until concrete verified mappings are
confirmed through manual BizHawk validation.

## Issue #53: Native Location Polling — Level-Based Reconnect-Safe Model

### Problem
Location checks were previously described in protocol docs using an edge-based
model ("if bit not previously seen") which could miss checks on reconnect.
The acceptance criteria also required explicit documentation of the level-based
contract and a test for the no-duplicate-send case.

### Resolution
The `_poll_locations` implementation uses a **level-based** model: on each poll,
it reads the current shard bitfield state, maps set bits to AP location IDs, and
sends only those checks that RAM reports as set but the server has not yet
acknowledged. This naturally handles reconnect resend without any edge tracking.

Key behaviors documented and tested:
- Native `shard_bitfield_native` (0x02038970) is preferred; transport mirror
  (`shard_bitfield`) is used as fallback when the native address is absent.
- Only bits with explicit location mappings produce checks; reserved/unmapped bits
  are filtered out.
- No `LocationChecks` is sent when all RAM-derived checks are already reflected in
  `server.checked_locations`.
- Missing checks are resent until the server acknowledges them (reconnect-safe).

PROTOCOL.md was updated to replace the old edge-based pseudocode with the actual
level-based contract description.

## Issue #52: AP Connection and Reconnection Lifecycle

### Problem
The connection section of PROTOCOL.md only described the initial handshake.
There was no documentation of which preconditions the watcher checks before
running, how each subsystem self-corrects on reconnect, or how to manually
verify reconnect behavior in BizHawk.

### Resolution
No new code was required; all reconnect-safe semantics were already implemented
across prior issues (#53, #54, #110). This issue formalized the contract:

- **Watcher gating**: `game_watcher` checks `ctx.server` (not None, socket open)
  and `ctx.slot_data` (not None) before any RAM reads or message sends.
- **Location resync**: level-based polling from #53 handles reconnect naturally.
- **Item delivery resync**: cursor-reconciliation from #54 handles both rewind
  (ROM counter behind) and fast-forward (ROM counter ahead) cases.
- **Goal reporting**: idempotent; already-reported goals are never re-sent.
- **Boss probe**: re-baselines snapshot on BizHawk stream-identity change.

PROTOCOL.md Section 1 was updated to document reconnect preconditions and the
self-correcting behavior of each subsystem.

BIZHAWK_TESTING_GUIDE.md now includes a "Reconnect Lifecycle Check" section
with step-by-step instructions for validating both BizHawk and server reconnect.

## Issue #35: Boss-Defeat Locations with Shard-Delivery Decoupling

### Problem
After a boss is defeated in Kirby & The Amazing Mirror, the game calls
`sub_0801D948` (ROM address `0x0801D948`) which calls `CollectShard(var->unk218)`
to grant the area shard directly to save-state. In AP randomizer play the shard
should come through the AP delivery pipeline (SHARD_N item) rather than as a
direct grant, and the boss defeat itself should be a distinct AP location check.

### Solution
Implemented the AP-side transport infrastructure for boss-defeat locations:

**Transport register**
- Added `boss_defeat_flags` at `0x0202C024` (u32, bits 0–7), extending the
  mailbox from 36 to 40 bytes.
- Bit N is set by `ap_set_boss_defeat_flag(N)` in the ROM payload when area
  boss N is defeated.

**ROM payload**
- Added `AP_BOSS_DEFEAT_FLAGS` macro in `ap_payload.c`.
- Added `ap_set_boss_defeat_flag(uint32_t boss_index)` stub with a TODO comment
  directing the caller to install the hook at `sub_0801D948` (ROM address
  `0x0801D948`, the function that calls `CollectShard(var->unk218)` after a boss
  collection cutscene). Until the hook is installed the register stays at zero;
  shard polling and delivery are unaffected.

**Locations**
- Added 8 `BOSS_DEFEAT_N` locations (bit_index 0–7) to `locations.json`, one per
  area, in the matching area region.
- Added `BOSS_DEFEAT = 2` to `LocationCategory` enum in `data.py`.

**Client**
- `_location_ids_by_bit` is now filtered to `SHARD` category only.
- New `_boss_location_ids_by_bit` maps BOSS_DEFEAT category locations.
- New `_poll_boss_defeat_locations()` reads `boss_defeat_flags` and sends
  AP location checks for set bits, level-based and reconnect-safe.

### Evidence trail
- **Claim**: beating a boss runs `sub_0801D948` which calls `CollectShard(var->unk218)`.
- **Source**: `d:\kirbyam-extras\katam\src\code_0801C6F8.c` lines 703–705;
  `CollectShard` definition at `d:\kirbyam-extras\katam\src\treasures.c` line 41.
- **Adaptation**: ROM hook (replacing the `BL CollectShard` with `BL ap_set_boss_defeat_flag`)
  is deferred pending patch-site byte verification via Issue #110. The transport
  register, AP locations, and client polling are fully wired so no client-side
  change is required when the hook is eventually installed.
- **Validation**: 2 new tests (boss defeat send + no-resend), 29+ tests passing.

### Remaining work (post-#35)
- Install the `sub_0801D948` ROM hook in `patch_rom.py` once the exact BL
  instruction byte offset inside the function is confirmed via live BizHawk
  inspection.  That step decouples the shard grant and enables real boss-defeat
  location checks in gameplay.

## Issue #56: Gameplay-Active Foundation Gate for Polling and Delivery

### Problem
Watcher logic previously ran location polling and new mailbox delivery attempts
without an explicit runtime gameplay-active gate. That allowed protocol work to
continue in menu/cutscene/post-clear phases where state may be unstable.

### Solution
Implemented a runtime gate in `KirbyAmClient.game_watcher` based on
`ai_kirby_state_native` (`0x0203AD2C`, u32):

- gameplay-active when `ai_state == 300`
- defer polling/write behavior for all other bands

When non-gameplay is detected, watcher now:
- defers shard and boss-defeat location polling
- defers new mailbox item writes
- continues mailbox ACK/recovery handling for already-pending item deliveries
- continues goal polling to avoid missing post-clear native goal states

### Logging
Added reason-coded transition logs:
- `KirbyAM: deferring location polling/new item writes (...)`
- `KirbyAM: gameplay-active state restored; resuming normal watcher flow`

Logs are transition-based to reduce per-tick spam.

### Tests
Added client tests for:
- gameplay-active classification on AI state 300
- non-gameplay classification on cutscene-band state
- watcher deferral behavior while non-gameplay
- mailbox write deferral while gated

### Scope Notes
- This is the Phase 1 foundation contract.
- In-game unsafe-state policy matrix (boss/travel windows and chaos options)
  remains scoped to Issue #223.

## Issue #58: Eliminate Duplicate LocationChecks from Client Polling

### Problem
Duplicate-prevention semantics were implemented in polling logic, but observability
was limited. It was hard to tell from logs whether a send occurred because the
server was missing RAM-derived checks or was correctly suppressed by dedupe.

### Solution
Expanded `_poll_locations()` diagnostics while preserving existing level-based,
reconnect-safe behavior:

- Log resend reason when RAM-derived checks are missing from server state.
- Log dedupe suppression when all RAM-derived checks are already acknowledged.
- Apply the same resend/dedupe diagnostics pattern to boss-defeat polling.
- Make diagnostics transition-based so unchanged states do not spam logs each tick.

This keeps canonical dedupe boundaries at AP location ID level while making
reconnect behavior easier to debug.

### Validation
- Added tests that assert resend logging and dedupe suppression logging.
- Full client test file passes after update.

## Issue #223: In-Gameplay Unsafe-State Delivery Policy (Research-First Mode)

### Problem
Issue #223 needs delivery gating during major boss, miniboss, cannon, and warp-star
windows, but the current codebase does not yet have verified stable native signals
for all of those states.

### Research-First Resolution Strategy
Instead of enforcing speculative behavior, the client now supports research-only
observational probes for optional unsafe-delivery candidates:

- existing boss-table probe remains the only integrated major-boss candidate path
- optional miniboss counters can be observed if future native addresses are mapped
  for `shadow_kirby_encounters_native` and `mirra_encounters_native`
- cannon and warp-star travel remain documented as hook-required candidates, not
  polling-based production signals

### Enforcement Boundary
- Gameplay-active gating from Issue #56 remains the only enforced delivery gate.
- Issue #223 policy must not suppress in-game delivery until concrete signals or
  hook points are verified and documented.

### Validation
- Added client tests for optional unsafe-delivery probes: no-address no-op,
  change logging, and reconnect re-baselining.
- Updated native signal policy notes and BizHawk guide with a research workflow.
