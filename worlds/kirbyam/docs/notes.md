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

## Issue #110: Boss Defeat Address Identification Beyond Shards

### Problem
Dungeon/final boss defeat native addresses beyond shard bitfields were still candidate-only and not instrumented in client logs, making live mapping work slower and less repeatable.

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
