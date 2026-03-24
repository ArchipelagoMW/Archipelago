# Kirby & The Amazing Mirror (GBA) - Address Policy Notes

## Issue #367: KirbyAM Integration Testing for Generation/Hosting/BizHawk Connector

### Problem
KirbyAM had strong unit coverage for many runtime paths but lacked explicit
integration tests for:
- fixture-driven YAML generation,
- local hosting connectivity with a generated KirbyAM archive,
- BizHawk connector protocol transport + ROM validation in an end-to-end request path.

### Solution
Added three integration test modules under `worlds/kirbyam/test`:

- `test_generate_integration.py`
  - Generates from `server/kirbyam_test_player.yaml` and validates decoded multidata slot metadata.
- `test_hosting_integration.py`
  - Spins up local MultiServer on generated KirbyAM archive and verifies AP client connect/datapackage behavior.
- `test_bizhawk_connector_integration.py`
  - Uses fake connector harness `support/fake_bizhawk_connector.py` with real `worlds._bizhawk` transport calls.
  - Confirms KirbyAM handler selection for patched signals and rejection for unpatched base-ROM hash.

Support helper added:
- `support/integration_generation.py` for fixture-based generation and `.archipelago` multidata decoding.

Fixture correction:
- `server/kirbyam_test_player.yaml` `goal` value updated from `defeat_dark_mind` to `dark_mind`
  so generation matches current option names.

### CI strategy
- PR/default test runs include these integration tests via existing
  `pytest worlds/kirbyam/test ...` execution.
- Optional true emulator runtime smoke is provided via
  `.github/workflows/kirbyam-bizhawk-runtime-smoke.yml`
  for self-hosted Windows runners with BizHawk + ROM provisioning.

### Validation
- Added dedicated tests for all three surfaces listed above.
- Verified fake connector path covers protocol requests used by ROM validation
  and auth extraction (`SYSTEM`, `HASH`, `READ`, `PING`).

## Issue #290: Generation Failure from Global bit_index Collision Check

## Issue #308: Critical-Module Coverage Gates

### Problem
Global test coverage can look healthy while coverage of protocol/runtime-critical
KirbyAM modules regresses unnoticed.

### Solution
Added module-level coverage gates for critical files:

- Threshold definitions (versioned):
  `worlds/kirbyam/test/critical_module_coverage_thresholds.json`
- Gate evaluator:
  `worlds/kirbyam/test/critical_module_coverage_gate.py`
- CI enforcement in `.github/workflows/unittests.yml`:
  - Runs once on `ubuntu-latest` / Python `3.13`
  - Generates coverage JSON from KirbyAM tests
  - Fails CI if any critical module falls below its threshold

Current gated modules:
- `worlds/kirbyam/client.py`
- `worlds/kirbyam/data.py`
- `worlds/kirbyam/generation_logging.py`
- `worlds/kirbyam/ability_randomization.py`
- `worlds/kirbyam/rules.py`

### Validation
- Added `worlds/kirbyam/test/test_critical_module_coverage_gate.py`.
- Tests cover pass/fail behavior for threshold misses and missing module entries.

### Problem
KirbyAM generation failed in `stage_assert_generate` because `validate_regions()` treated
all location `bit_index` values as one global namespace. That rule incorrectly rejected
valid cross-category reuse such as:
- SHARD bit `0`
- BOSS_DEFEAT bit `0`

These locations are polled from different bitfield domains, so shared numeric bit indices
across categories are expected and valid.

### Solution
Updated `worlds/kirbyam/sanity_check.py` so bit-index uniqueness is enforced per location
category instead of globally.

The validator now:
- allows cross-category bit index reuse
- still fails on duplicate bit indices inside the same category
- logs category-specific collision messages for easier triage

### Validation
- Added `worlds/kirbyam/test/test_sanity_check.py`.
- New tests verify:
  - cross-category bit index reuse passes validation
  - same-category bit index collisions fail validation

## Issue #292: VS Code Build Tasks Must Use Payload Directory CWD

### Problem
The `Build payload` and `Patch Kirby ROM` VS Code tasks relied on implicit working
directory behavior. Running from repository root could fail because `make` and
`patch_rom.py` expect `worlds/kirbyam/kirby_ap_payload` as the current directory.

### Solution
Added explicit `options.cwd` values to task definitions:
- root workspace tasks now run from `${workspaceFolder}/worlds/kirbyam/kirby_ap_payload`
- payload-local workspace tasks now run from `${workspaceFolder}`

### Validation
- Root `Build payload` task now resolves the payload `Makefile` deterministically.
- Root `Patch Kirby ROM` task now resolves `patch_rom.py` and local ROM filenames
  without depending on active editor file location.

## Issue #310: Flaky-Test Detection Mode for Reconnect-Sensitive Tests

### Problem
Reconnect and timing-sensitive tests can fail intermittently, but single-pass CI
runs do not reliably expose those failures.

### Solution
Added a repeat-run flaky detection mode that can be executed both locally and in
CI:

- Local runner: `worlds/kirbyam/test/flaky_detection_runner.py`
  - Repeats selected reconnect-sensitive pytest targets for `N` runs.
  - Emits per-run JUnit XML.
  - Aggregates failures by test name with explicit run indices.
  - Exits non-zero when any run fails.
- CI entry point: `.github/workflows/kirbyam-flaky-detection.yml`
  - Triggered via `workflow_dispatch`.
  - Accepts configurable run count and optional extra pytest arg.
  - Uploads JSON summary + JUnit artifacts for triage.

### Local usage

```bash
python worlds/kirbyam/test/flaky_detection_runner.py --runs 20
```

Optional output and args:

```bash
python worlds/kirbyam/test/flaky_detection_runner.py \
  --runs 30 \
  --json-out test-output/kirbyam/flaky-detection-summary.json \
  --junit-dir test-output/kirbyam/flaky-junit \
  --pytest-arg -k reconnect
```

### Validation
- Added `worlds/kirbyam/test/test_flaky_detection_runner.py`.
- Tests cover argument validation, default target selection, JUnit failure extraction,
  and malformed XML handling.

## Issue #309: Mutation Testing Evaluation for Logic-Heavy Modules

### Problem
KirbyAM has logic-heavy modules (ability randomization, data mapping) where weak test assertions could allow regressions to slip past CI.

### Solution
Implemented repeatable mutation testing workflow using Cosmic Ray:

- Configuration: `worlds/kirbyam/test/mutation.cosmic.toml`
  - Targets `ability_randomization.py` and `data.py`
  - Focuses on test-backed modules with deterministic, verifiable behavior
- Documentation: `worlds/kirbyam/docs/MUTATION_TESTING.md`
  - Local usage: baseline, init, exec, report cycle
  - CI integration roadmap for automated mutation scoring

### Validation
- Cosmic Ray baseline passes on unmutated code
- Session initialization detects 100+ mutation opportunities across target modules
- Per-operator mutation categories documented in cr-report output

### Baseline Mutation Score
This PR establishes the mutation-testing workflow only. Baseline mutation score capture will be performed in a follow-up task and documented once the first full local run has been completed.

### Next Steps (In Follow-Up PRs)
1. Run full mutation execution to capture baseline score (tracked in issue comment once PR merges)
2. Investigate surviving mutants for test gap patterns
3. Optionally create CI workflow for periodic automated mutation scoring

## Issue #353: Open Patch Base-ROM Reprompt and Metadata Error Spam

### Problem
KirbyAM Open Patch could launch BizHawk using a stale/invalid configured base ROM path
without forcing a replacement prompt when the file existed but failed ROM hash validation.

When the resulting loaded ROM had an all-zero `gArchipelagoInfo` auth block, the client
logged the same metadata-missing error repeatedly, creating log spam during validation retries.

### Solution
- Added KirbyAM-specific preflight validation in BizHawk Open Patch flow:
  - validates configured base ROM for `.apkirbyam` before patching
  - prompts for ROM re-selection in GUI mode on hash/path mismatch
  - saves replacement path and revalidates before continuing
- Added duplicate-log suppression in KirbyAM ROM validation:
  - metadata-missing error now logs once per persistent failure condition
  - repeated retries no longer flood logs with identical messages

### Validation
- Added `worlds/kirbyam/test/test_bizhawk_patch_preflight.py`
  - non-Kirby patch: no-op preflight
  - Kirby patch hash mismatch: browse/save/revalidate path exercised
- Added `worlds/kirbyam/test/test_client.py::test_validate_rom_rejects_empty_patch_metadata_logs_once`
  - repeated empty-metadata validation attempts emit one user-facing error

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
- Current integrated native signals:
  - `shard_bitfield_native` at `0x02038970`
  - `big_chest_bitfield_native` at `0x0203897C`

Rule: AP transport fields must never be treated as native gameplay truth.

## Status taxonomy

- `candidate`: Derived from workbook/cheat/reverse-engineering source; requires live confirmation.
- `integrated`: Used by current client/ROM path but not yet promoted to fully live-verified policy status.
- `verified`: Confirmed by repeatable live memory observation on USA ROM.

Current high-level status:

| Signal type | Candidate | Integrated | Verified |
| --- | --- | --- | --- |
| Shard progression | Yes | Yes | Not yet policy-promoted |
| Major chest checks | Yes | Yes | No |
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

## Shard progression mapping reference

Current shard bit mapping remains valid for progression state:

- bit 0 -> Mustard Mountain shard obtained
- bit 1 -> Moonlight Mansion shard obtained
- bit 2 -> Candy Constellation shard obtained
- bit 3 -> Olive Ocean shard obtained
- bit 4 -> Peppermint Palace shard obtained
- bit 5 -> Cabbage Cavern shard obtained
- bit 6 -> Carrot Castle shard obtained
- bit 7 -> Radish Ruins shard obtained

Issue #369 contract note:
- Mirror shard bits are progression-state signals only.
- AP location checks are emitted from boss-defeat and major-chest polling.

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

## Issue #74: Send Notifications (Local Outgoing ItemSend Events)

### Problem
Send notifications needed explicit local-sender filtering and burst handling so
high-traffic ItemSend scenarios do not spam the player.

### Implementation
- Send notifications are emitted from `PrintJSON` `ItemSend` packets only when
  local slot is the sender.
- Non-local ItemSend traffic is ignored.
- Dedupe remains key-based on `(item_id, sender_id, receiver_id, location_id)`.
- Added burst rate-limit policy:
  - max 5 send notifications per 2-second window
  - excess sends are suppressed
  - suppression summary is displayed when window rolls over

### Validation
- Added targeted tests for:
  - unrelated ItemSend suppression
  - burst-rate limiting + suppression summary behavior

## Issue #46: Expanded Protocol Regression Coverage (Mailbox/Reconnect/Goal)

### Problem
Core client protocol paths had partial coverage but still lacked explicit tests
for mailbox ACK cursor advancement, stale-flag recovery during reconnect
fast-forward, and malformed delivery-entry shape variants.

### Solution
Expanded `worlds/kirbyam/test/test_client.py` with focused deterministic tests
covering:
- mailbox ACK sequencing: pending -> ACK observed -> cursor persist + receive
  notification trigger
- reconnect fast-forward recovery when mailbox flag is stale (clear-on-reconcile)
- malformed `ReceivedItems` entries missing required fields (for example,
  missing `player`) while continuing delivery of subsequent valid entries

### Validation
- Targeted KirbyAM client tests pass locally after coverage additions.
- Full KirbyAM test suite pass confirms fixture stability and non-flaky behavior.

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
- Added `ap_set_boss_defeat_flag(uint32_t boss_index)` and a dedicated
  `ap_on_boss_defeat_collect_shard(uint32_t boss_index)` hook target.
- `patch_rom.py` now patches the `BL CollectShard` call inside `sub_0801D948`
  (ROM address `0x0801D948`, callsite file offset `0x001D950`) so boss defeat
  sets the AP boss flag and does not grant the shard natively.

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
- **Adaptation**: patch the `BL CollectShard` call in `sub_0801D948` to branch
  into `ap_on_boss_defeat_collect_shard`, which records boss defeat without
  mutating native shard progression.
- **Validation**: focused client polling tests, item-pool tests, and patch tool
  tests covering the new Thumb BL encoder.

### Remaining work (post-#35)
- Live BizHawk verification of the patched boss-defeat hook against the clean USA
  ROM remains advisable before release patch promotion, but the hook is now wired
  in the shipped patch generator.

## Issue #75: DeathLink Runtime Receive/Apply and Local Death Send

### Problem
KirbyAM had DeathLink tag synchronization wired from slot-data, but runtime
behavior was incomplete: incoming DeathLink events were not applied to gameplay,
and local alive->dead transitions were not sent.

### Solution
Implemented full runtime DeathLink flow in `worlds/kirbyam/client.py`:
- Queue incoming `Bounced` packets tagged `DeathLink`.
- Apply incoming DeathLink only while gameplay-active by writing
  `kirby_hp_native` to zero.
- Detect local alive->dead transitions from `kirby_hp_native` and send one
  outgoing DeathLink per transition.
- Suppress immediate outgoing echo after applying incoming DeathLink.

### Address evidence
- `d:\kirbyam-extras\katam\linker.ld`: `gKirbys = 0x02020EE0`
- `d:\kirbyam-extras\katam\include\kirby.h`: `struct Kirby` contains `s8 hp`
- Selected native signal address: `kirby_hp_native = 0x02020FE0`

### Validation
- Added DeathLink runtime tests in `worlds/kirbyam/test/test_client.py`:
  - incoming queue behavior
  - incoming HP-zero apply behavior
  - local alive->dead send exactly once
  - incoming-apply echo suppression

## Issue #333: Host Upload Crash (`TypeError: an integer is required`)

### Problem
Uploading KirbyAM seeds to `archipelago.gg` failed while loading room multidata:
`_speedups.LocationStore.init` raised `TypeError: an integer is required`.

### Root cause
Goal locations were converted to locked event items (`item.code is None`) in
`create_items()`, but their AP location address remained numeric. During host
load, `LocationStore` attempted to deserialize these numeric location entries
with a non-integer item value, causing the crash.

### Solution
- When converting goal locations to runtime events, set `loc.address = None`.
  This keeps goal checks as event-only (non-host-fillable) locations and avoids
  serializing `None` item codes into numeric location entries.
- Added regression test in `test_item_pool.py` ensuring goal locations become
  addressless events.

### Validation
- Targeted pytest for `test_item_pool.py`, including the new regression test.

## Issue #312: Standardize Manual Test Templates into Machine-Checkable Checklists

### Problem
Manual testing issues were readable, but result comments were not standardized
enough for reliable parsing/reporting.

### Solution
- Added a dedicated GitHub issue template:
  `.github/ISSUE_TEMPLATE/manual_testing_checklist.yaml`
  with required fields and a structured result-comment block.
- Added parser utility:
  `.github/scripts/manual_test_checklist_parser.py`
  that extracts and validates manual test result blocks from issue comments.
- Added parser tests:
  `worlds/kirbyam/test/test_manual_test_checklist_parser.py`.
- Added manual result block guidance to
  `worlds/kirbyam/docs/BIZHAWK_TESTING_GUIDE.md`.

### Result block contract
- Delimiters:
  `<!-- MANUAL_TEST_RESULT:START -->` and
  `<!-- MANUAL_TEST_RESULT:END -->`
- Required fields:
  `RESULT_SCHEMA_VERSION`, `TEST_CASE_ID`, `STATUS`, `BUILD_REF`, `PLATFORM`,
  `BIZHAWK_VERSION`, `ROM_REGION`, `EXPECTED_RESULT`, `OBSERVED_RESULT`,
  `EVIDENCE`, `NOTES`
- Allowed status values: `PASS`, `FAIL`, `BLOCKED`

### Validation
- Targeted pytest on the new parser test module.

## Issue #373: Fix BizHawk Connect Crash from connect_names Value Shape

### Problem
KirbyAM registered BizHawk auth tokens in `connect_names` as player-name
strings. The server expects every `connect_names` value to be a `(team, slot)`
tuple, so connection attempts could crash with a tuple-unpack `ValueError`.

### Solution
- Updated `KirbyAmWorld.modify_multidata` to copy the existing `(team, slot)`
  tuple from the player-name entry instead of storing the player name string.
- Added regression test module
  `worlds/kirbyam/test/test_multidata_connect_names.py` to assert auth token
  registration preserves tuple shape.

### Validation
- `pytest worlds/kirbyam/test/test_multidata_connect_names.py`
- `pytest worlds/kirbyam/test/test_hosting_integration.py`

## Issue #371: Hide Goal/Event Objective Checks from `/locations`

### Problem
KirbyAM exported goal labels like `Defeat Dark Mind` and `100% Save File` in
the datapackage `location_name_to_id` map even though generation later converts
those checks into runtime events. That made `/locations` show goal/event-style
objective checks as if they were normal AP locations.

### Solution
- Excluded `LocationCategory.GOAL` entries from KirbyAM's exported
  `location_name_to_id` map.
- Excluded the same goal labels from KirbyAM location groups so datapackage
  group listings stay consistent with hidden objective checks.
- Added regression coverage to assert goal labels are hidden from datapackage
  exports while remaining present in generated worlds as addressless runtime
  events.

### Validation
- `pytest worlds/kirbyam/test/test_location_visibility.py`
- `pytest worlds/kirbyam/test/test_spoiler_event_visibility.py`

## Issue #311: Golden Snapshot Tests for slot_data and Generated Artifacts

### Problem
The test suite had contract and behavior checks, but no committed golden
snapshots for deterministic outputs. That made it harder to review exact payload
or mapping drift in PRs.

### Solution
- Added `worlds/kirbyam/test/test_snapshot_outputs.py` with two snapshot tests:
  - representative `slot_data` payload emitted from `KirbyAmWorld.fill_slot_data`
  - deterministic generated enemy mapping artifacts for fixed seeds
- Added committed snapshot fixtures in
  `worlds/kirbyam/test/data/snapshots/`:
  - `slot_data_representative.json`
  - `enemy_mapping_seed_20260322.json`
- Added snapshot fixture update guidance in
  `worlds/kirbyam/test/data/snapshots/README.md`.
- Updated `worlds/kirbyam/test/test_fixture_data.py` to assert the
  `snapshots/` fixture directory exists.

### Snapshot update workflow
1. Set `KIRBYAM_UPDATE_SNAPSHOTS=1`.
2. Run `pytest worlds/kirbyam/test/test_snapshot_outputs.py`.
3. Review generated diff under `worlds/kirbyam/test/data/snapshots/`.
4. Unset `KIRBYAM_UPDATE_SNAPSHOTS` and rerun tests in strict mode.

### Validation
- `pytest worlds/kirbyam/test/test_snapshot_outputs.py`
- `pytest worlds/kirbyam/test/test_fixture_data.py`
- `pytest worlds/kirbyam/test/test_slot_data_contract.py`

## Issue #313: Remove Circular Committed kirbyam.apworld Artifact

### Problem
`worlds/kirbyam/kirbyam.apworld` was tracked in git as a 10 MB renamed ZIP of the `worlds/kirbyam/` directory itself, creating circular/redundant storage. CI already rebuilds the artifact fresh on every run via `build.py --skip-patch`, so the committed copy was never consumed by CI.

### Solution
- Removed `worlds/kirbyam/kirbyam.apworld` from git tracking via `git rm --cached`.
- Added `*.apworld` to `worlds/kirbyam/.gitignore` to prevent it from being accidentally re-committed.
- Updated the `kirbyam-apworld.yml` CI step name from "Build kirbyam.apworld from committed patch data" to "Build kirbyam.apworld from source" (no logic change — CI was already building fresh).
- `kirbyam-rom-patch-smoke.yml` was already correct: it calls `build.py` before checking for the artifact.

### Validation
- `git ls-files '*.apworld'` returns empty after the change.
- CI workflows untouched in logic; the step in `kirbyam-apworld.yml` still builds and validates the artifact.

## Issue #307: Release Integrity Checks (Changelog/Tag/Apworld Coherence)

### Problem
No automated check verified that a CHANGELOG section existed for the tagged release version, creating risk that a tag could be pushed without a matching changelog entry.

### Solution
- Added `check_changelog_has_version(changelog_path, version)` to `.github/scripts/kirbyam_release_metadata.py`. Raises `ValueError` with a clear message if the `## v{version}` heading is absent.
- Added `--changelog` argument to the same script; when provided and `release_enabled` is True, the check is run before metadata outputs are written.
- Updated `kirbyam-apworld.yml` CI step to pass `--changelog worlds/kirbyam/CHANGELOG.md`, so release tags that lack a changelog section fail the CI step explicitly.
- Added 8 new tests in `worlds/kirbyam/test/test_release_metadata.py` covering: section-found, section-missing, Unreleased not treated as version, partial-match guard, real-CHANGELOG smoke, main integration (pass and fail), and branch-ref skip.

### Validation
- `pytest worlds/kirbyam/test/test_release_metadata.py` — 16 passed.

## Issue #300: slot_data Protocol Contract Parity Tests

### Problem
`slot_data` fields are defined in both implementation (`fill_slot_data`) and
protocol docs (`PROTOCOL.md`). Without a parity gate, those can drift silently.

### Solution
Added `worlds/kirbyam/test/test_slot_data_contract.py` with contract tests that:
- parse documented `slot_data` keys from `PROTOCOL.md`
- emit slot_data via `KirbyAmWorld.fill_slot_data(...)`
- assert exact key parity between documentation and emitted payload
- assert enemy randomization contract field shapes are present

### Validation
- Targeted local pytest run on the new contract tests.
- These tests are part of the standard KirbyAM test suite and therefore covered
  by existing CI test jobs.

## Issue #302: Reconnect Chaos Tests for BizHawk Client Idempotency

### Problem
Reconnect behavior is safety-critical for live sessions but prior coverage was
mostly per-subsystem unit checks rather than stateful multi-cycle chaos tests.

### Solution
Added dedicated reconnect chaos tests in
`worlds/kirbyam/test/test_reconnect_chaos.py` that simulate repeated
connect/disconnect cycles during:
- location polling
- mailbox item delivery
- goal reporting

The tests assert:
- no duplicate location sends after server acknowledgement
- item delivery resumes correctly after reconnect without replaying already-
  pending first-item writes
- goal location/status flow remains idempotent across reconnect cycles

### Validation
- Targeted local pytest for `test_reconnect_chaos.py`.
- Additional local run including existing reconnect-related client tests.

## Issue #82: DeathLink End-to-End Closure

### Problem
After #76 and #75 landed, the remaining parent-level gaps were contract cleanup
and manual validation guidance: the option surface still claimed DeathLink was
not ready, and the BizHawk guide did not define an end-to-end smoke pass.

### Solution
- Updated the DeathLink option description to describe the shipped behavior.
- Added a BizHawk DeathLink smoke checklist covering:
  - tag sync state
  - incoming receive/apply
  - gameplay-gated deferred application
  - outgoing send exactly once per death
  - echo suppression
  - reconnect safety

### Validation
- Touched files remain diagnostics-clean in VS Code.
- Manual BizHawk validation remains the authoritative next step for parent-issue
  closure because local pytest execution on this machine is blocked by the repo
  Python-version gate (`3.11.9` through `3.13.x`, current interpreter `3.14`).


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

## Issue #337: Startup 99-Lives Follow-up Hook Hardening

### Problem
Startup-state corruption could still appear as a 99-lives symptom despite the
earlier fix that removed an explicit `r4` temporary restore pattern.

The remaining risk was the hook boundary itself: calling `ap_poll_mailbox_c`
from a sensitive site while preserving only part of the live register context.

### Solution
Hardened `ap_hook_entry` in `ap_hook.s` to preserve a stronger context envelope:
- save/restore `r0-r7` and `lr`
- explicitly mirror and restore `r8-r11` through `r0-r3` around the C call
- keep replayed overwritten instructions (`mov r7, r9` / `mov r6, r8`) intact

This reduces the chance of hook-boundary context drift affecting startup state.

### Validation
- Updated `test_reset_safe_shards.py` hook regression to assert:
  - low-register + LR preservation (`push/pop {r0-r7, lr}` / `{r0-r7}`)
  - explicit high-register mirror/restore (`r8-r11` via `r0-r3`)
  - no `r4`-based LR reconstruction pattern

## Issue #381: Suppress Native Big Chest Map Grants

### Problem
Major chest checks were polled from native `gTreasures.bigChestField` at
`0x0203897C`. Opening a big chest therefore both sent the AP check and unlocked
the native area map immediately, even when the chest's actual AP reward was not
that map.

### Solution
Split major chest checks from native map ownership:
- added transport `major_chest_flags` at `0x0202C028` for AP check polling
- patched the native `CollectBigChest` call site to invoke payload hook
  `ap_on_collect_big_chest(area_id)`
- preserved AP check signaling by setting `major_chest_flags` when the chest is opened
- suppressed native map unlock at chest-open time
- granted native area maps only when the corresponding AP `MAP_*` item is delivered

### Native Evidence
- chest reward dispatcher: `katam/asm/chest.s`, `sub_0800AFC8`
- `CollectBigChest` caller block at ROM `0x0800B144`
- native map bitfield: `gTreasures.bigChestField` / `0x0203897C`

### Validation
- client major chest polling tests updated to use the transport register
- payload tests assert separate major chest transport signaling and native map unlock handling

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

## Issue #238: GitHub Actions Node 24 Migration (JavaScript Actions)

### Problem
GitHub Actions runner support for Node 20 is deprecated and will force JavaScript
actions to Node 24 by default. Existing workflows still referenced
`actions/checkout@v4` and `actions/setup-python@v5`.

### Solution
Updated all affected workflows to current major versions:
- `actions/checkout@v4` -> `actions/checkout@v6`
- `actions/setup-python@v5` -> `actions/setup-python@v6`
- `actions/labeler@v5` -> `actions/labeler@v6`

Added temporary workflow-level early opt-in for migration confidence:
- `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24: true`

### Follow-up
- Keep the temporary Node 24 force toggle in place through initial migration
  confidence checks, then remove it after runner defaults are confirmed stable.
- Track action hardening (full commit SHA pinning) as a separate follow-up once
  the major-version migration is verified.

## Issue #119: Useful, Non-Filler Item Tier (Maps + Vitality)

### Problem
KirbyAM's non-progression pool was dominated by low-value filler (`1 Up`) while
progression remained concentrated in mirror shards.

### Solution
Added a first-pass useful item tier without introducing new progression rules:
- map useful items:
  - `Map - Mustard Mountain`
  - `Map - Moonlight Mansion`
  - `Map - Candy Constellation`
  - `Map - Olive Ocean`
  - `Map - Peppermint Palace`
  - `Map - Cabbage Cavern`
  - `Map - Carrot Castle`
  - `Map - Radish Ruins`
- vitality useful items:
  - `Vitality Counter I`
  - `Vitality Counter II`
  - `Vitality Counter III`
  - `Vitality Counter IV`

Pool composition wiring for practical quantities:
- `BOSS_DEFEAT_1..8` locations now have explicit `default_item` values that map
  to the new useful item set (4 map + 4 vitality).

Generation behavior retained:
- progression logic remains shard/goal-based and unchanged.
- no new progression gates were introduced by these useful items.

### Logging and Validation
- Added generation-time item pool classification summary logging for
  useful/filler/progression counts.
- Added tests to validate:
  - useful catalog contains both map and vitality categories
  - boss-defeat default pool is composed of useful items and includes both
    categories

## Issue #37: Ability-Related Location Logic Stubs

### Problem
Phase 2 major chest rollout needs stable logic categories for copy-ability gates,
but the current AP item pool does not yet randomize ability items or ability
statues. That meant future chest routing had nowhere to record verified gate
evidence without accidentally blocking current generation.

### Solution
Added five placeholder ability-gate helpers in `worlds/kirbyam/rules.py`:
- `CanCutRopes`
- `CanBreakBlocks`
- `CanUseMini`
- `CanLightFuses`
- `CanPoundPegs`

Current contract:
- every helper defaults to `True`
- current shard/goal logic remains unchanged
- no new progression restrictions are enforced in shipped seeds yet

Added structured `ability_gates` annotations to
`worlds/kirbyam/data/regions/areas.json` and preserved them in `RegionData` so
future major chest logic can consume them directly.

### Evidence Status Policy
- `confirmed`: explicit object evidence already seen in room analysis
- `semantic_candidate`: geometry/transition evidence suggests the gate, but live
  verification is still needed
- `unconfirmed`: unresolved semantic hint tracked for later review only

### Seed-Safe Scope
This issue only establishes naming and evidence scaffolding. Ability items are
still absent from the pool, so all five helpers intentionally resolve to true
until a later issue introduces actual ability acquisition logic.

## Issue #111: Enemy Copy-Ability Randomization with Whitelist

### Problem
Enemy copy abilities were still fully vanilla/static, and there was no
seed-deterministic mapping artifact that downstream client/payload work could
consume safely. We also needed a conservative whitelist boundary so generation
never emits unknown or invalid ability names.

### Solution
Added deterministic enemy copy-ability policy generation in
`worlds/kirbyam/ability_randomization.py` with three modes:
- `vanilla`: identity mapping
- `shuffled`: deterministic per-enemy-type assignment
- `completely_random`: deterministic per-grant-event assignment

The validated whitelist explicitly excludes `Crash` and `Wait`.

The world now emits the following slot-data contract:
- `enemy_copy_ability_randomization`
- `randomize_boss_spawned_ability_grants`
- `randomize_miniboss_ability_grants`
- `enemy_copy_ability_whitelist`
- `enemy_copy_ability_policy`

### Deliberate Scope Limit
This issue establishes generation-time mapping and protocol exposure only. It
does not patch statue randomization paths (#209) and does not yet introduce
ability-item ownership gating (#84).

## Issue #41: Multi-Item Filler Pool (Phase 1)

Status: Historical context only. Superseded by Issue #372 for current Phase 1 shipped behavior.

### Problem
KirbyAM filler fallback still always returned `1 Up`, so any future randomized
non-progression location without an explicit default item would collapse into a
single repeated reward.

### Solution
Expanded the shipped filler catalog to a conservative extra-life family:
- `1 Up`
- `2 Up`
- `3 Up`

At the time of Issue #41, generation used a deterministic weighted filler table in
`KirbyAmWorld.get_filler_item_name()`:
- `1 Up`: weight 6
- `2 Up`: weight 3
- `3 Up`: weight 1

ROM payload support was extended so each filler item grants the matching number
of lives and saturates safely at 255 lives.

### Deliberate Scope Limit
Health-restore and battery-style consumables were considered during issue
research, but they remain deferred until their native apply semantics are
verified well enough to ship without risky mailbox-side side effects.

## Issue #372: Phase 1 – Restrict Filler Pool to 1_UP

### Problem
While Issue #41 introduced a weighted multi-filler pool (`1 Up`, `2 Up`, `3 Up`), Phase 1 gameplay balance requires a single filler item to keep rewards simple and predictable.
The multi-filler pool introduced unnecessary complexity for the initial release.

### Solution
Replaced the weighted filler selection table with an explicit **active filler pool** abstraction:
- Introduced `KirbyAmWorld.ACTIVE_FILLER_POOL: ClassVar[tuple[str, ...]]` on `KirbyAmWorld` (class scope).
- Phase 1 pool contains only `("1 Up",)`.
- Generation calls `self.random.choice(self.ACTIVE_FILLER_POOL)` instead of weighted selection.
- Pool structure supports future expansion without code changes (only data update).

Catalog items `2 Up` and `3 Up` remain defined and dormant:
- Not selected by active filler generation.
- Payload handlers remain intact for compatibility.
- Documented as reserved/inactive for Phase 1.

### Validation
- `test_active_filler_selection_is_seed_stable()` updated to assert only `1 Up` is selected.
- New pool-based logic remains deterministic under fixed seeds (RNG behavior unchanged).
- Updated `test_item_pool.py` to match Phase 1 expectations.
