# BizHawk Testing Guide for Address Verification

## Automated Integration Coverage (Issue #367)

Three integration surfaces now have automated coverage split by runtime cost:

1. Fast PR CI coverage (normal `pytest worlds/kirbyam/test ...` runs)
    - `worlds/kirbyam/test/test_generate_integration.py`
    - `worlds/kirbyam/test/test_hosting_integration.py`
    - `worlds/kirbyam/test/test_bizhawk_connector_integration.py`

2. Optional runtime smoke coverage (self-hosted BizHawk)
    - `.github/workflows/kirbyam-bizhawk-runtime-smoke.yml`
    - Trigger via `workflow_dispatch` or nightly schedule on a prepared self-hosted Windows runner.

### What each automated integration test validates

- `test_generate_integration.py`
   - Generates a KirbyAM archive from `worlds/kirbyam/test/server/kirbyam_test_player.yaml`.
   - Verifies generated multidata contains a KirbyAM slot with expected game/player metadata.

- `test_hosting_integration.py`
   - Starts local MultiServer with generated KirbyAM archive.
   - Connects a minimal AP websocket client and validates successful `Connected` flow and sane location arrays.

- `test_bizhawk_connector_integration.py`
   - Uses a fake BizHawk connector TCP server that speaks the generic connector protocol.
   - Exercises real `worlds._bizhawk` transport calls (`connect`, `ping`, `get_system`, `get_hash`, `read`).
   - Validates KirbyAM handler selection + patched ROM auth-path read behavior.
   - Validates unpatched base-ROM hash rejection path.

### Local command examples

Run only the new issue #367 integration tests:

```bash
pytest worlds/kirbyam/test/test_generate_integration.py \
          worlds/kirbyam/test/test_hosting_integration.py \
          worlds/kirbyam/test/test_bizhawk_connector_integration.py -q
```

Run all KirbyAM tests (includes these integration tests):

```bash
pytest worlds/kirbyam/test -q
```

## Client Log Reference

### Log levels
- **info** — key lifecycle and protocol transitions; always visible in a normal session.
- **debug** — verbose diagnostics; only shown when debug logging is enabled.
- **warning** — unexpected but recoverable conditions; always visible.

### Key info-level messages

| Message pattern | Meaning |
|---|---|
| `KirbyAM: ROM validated.` | ROM name matched expected prefix; client initialized. |
| `KirbyAM: AP session ready; reconnect-safe reconciliation active` | First watcher tick after AP server/socket/slot_data readiness; transient reconnect caches were reset. |
| `KirbyAM: BizHawk request failed during watcher tick; waiting for reconnect (...)` | A transient BizHawk transport timeout occurred inside the shipped KirbyAM handler; handler-side reconnect state was reset and the next successful tick will resync from RAM instead of requiring a client restart. |
| `KirbyAM: deferring location polling/new item writes (...)` | Non-gameplay state detected; polling suspended. Fires once per state transition. |
| `KirbyAM: gameplay-active state restored; resuming normal watcher flow` | Returned to gameplay-active state. |
| `KirbyAM: resending major-chest LocationChecks missing on server (missing=..., acked=...)` | Big-chest area bits found in RAM but not yet acknowledged by server; resending. |
| `KirbyAM: resending boss-defeat LocationChecks missing on server (missing=..., acked=...)` | Boss-defeat bits found in RAM but not yet acknowledged by server; resending. |
| `KirbyAM: resending room-sanity LocationChecks missing on server (missing=..., acked=...)` | Room-visit (`gVisitedDoors`) checks found in RAM but not yet acknowledged by server; resending. |
| `KirbyAM: Delivering mailbox item index N (<item_name> from <sender_name>)` | Beginning delivery of the Nth received item with readable item/sender context. |
| `KirbyAM: Mailbox delivery confirmed at item index N` | ROM cleared the flag; delivery confirmed. |
| `KirbyAM: ROM delivery counter moved backward from X to Y; rewinding client delivery cursor` | ROM reported fewer items received than expected; cursor rewound. |
| `KirbyAM: ROM delivery counter moved forward from X to Y; fast-forwarding client delivery cursor` | ROM is ahead of client cursor; cursor fast-forwarded. |
| `KirbyAM: ROM counter fallback active; continuing mailbox delivery at item index N (...)` | ROM `debug_item_counter` is ahead of the current `ReceivedItems` list, so the client is ignoring that stale/debug counter and continuing mailbox delivery to avoid starvation. |
| `KirbyAM: receive notification queued (index=N, item=..., sender=...)` | Receive notification was queued after mailbox ACK for delivered index `N`. |
| `KirbyAM: send notification queued (item=..., receiver=...)` | Outgoing ItemSend notification was queued for local sender traffic. |
| `KirbyAM: send notification burst suppression summary (suppressed=N)` | A send burst exceeded policy; `N` notifications were suppressed in the previous window. |
| `KirbyAM: native goal signal seen (goal_option=N)` | Native ai_kirby_state value matched the selected goal condition for the first time. |
| `KirbyAM: sending goal location check (location_id=N)` | Goal location check sent to server. |
| `KirbyAM: goal complete; sending CLIENT_GOAL status (goal_option=N)` | Server acknowledged goal location; CLIENT_GOAL status sent. |

### Key warning-level messages

| Message pattern | Meaning |
|---|---|
| `KirbyAM: Mailbox ACK timeout at item index M; clearing flag and retrying (...)` | ROM did not clear flag before timeout; client force-cleared and retried the same index. Timeout reason includes frame-based and/or wall-clock fallback details. |
| `KirbyAM: Repeated mailbox ACK timeouts with frame_counter stuck at 0 and hook_heartbeat not advancing (...)` | Main payload hook likely inactive; both liveness counters are stale. |
| `KirbyAM: Repeated mailbox ACK timeouts with frame_counter stuck at 0 while hook_heartbeat advances (...)` | Hook is alive but `frame_counter` slot appears unstable; use heartbeat as liveness signal. |
| `KirbyAM: Repeated mailbox ACK timeouts with frame_counter stuck at 0; payload hook may be inactive in the loaded ROM patch` | Frame-based liveness signal is unavailable; verify loaded ROM patch and hook callsite. |
| `KirbyAM: Clearing stale mailbox flag after fast-forward to item index N` | Residual flag found after cursor fast-forward; cleared proactively. |
| `KirbyAM: Skipping malformed ReceivedItems entry at index N` | A received item entry had invalid fields; skipped and cursor advanced. |
| `KirbyAM: ROM delivery counter is ahead of received items (rom=X, received=Y); ignoring ROM counter and continuing mailbox delivery` | ROM `debug_item_counter` is stale/high relative to the AP `ReceivedItems` backlog. The client will no longer pin the cursor and return forever; it falls back to normal mailbox writes once safe. |

### Debug-level diagnostics
Enable debug logging in your AP client to see these:
- `KirbyAM: dedupe suppressed boss-defeat LocationChecks (...)` — boss-defeat checks already acknowledged (per-tick spam suppressed at info level).
- `KirbyAM: dedupe suppressed major-chest LocationChecks (...)` — major-chest checks already acknowledged (per-tick spam suppressed at info level).
- `KirbyAM: dedupe suppressed vitality-chest LocationChecks (...)` — vitality-chest checks already acknowledged (per-tick spam suppressed at info level).
- `KirbyAM: dedupe suppressed room-sanity LocationChecks (...)` — room-visit checks already acknowledged (per-tick spam suppressed at info level).
- `KirbyAM: boss candidate probe rising bits: ...` — rising-edge transitions detected in the boss mirror table probe. Useful during boss fights for address mapping.
- `KirbyAM: unsafe-delivery candidate probe: X changed Y -> Z` — miniboss counter candidate changed. Research-only probe (Issue #223).

### How to enable debug logging
Pass `--loglevel debug` when launching the BizHawk client, or set the log level in `host.yaml`:
```yaml
# host.yaml
log_level: debug
```

---

## Gameplay-Active Gating Check (Issue #56)

Validate that non-gameplay states defer location polling and new mailbox writes.

1. Start connected AP + BizHawk session with KirbyAM client logs visible.
2. Enter normal gameplay movement and confirm no defer log is shown.
3. Open pause/menu or trigger cutscene transition.
4. Confirm log entry appears once per state transition:
   - KirbyAM: deferring location polling/new item writes (...)
5. While still non-gameplay, verify:
   - no new LocationChecks are sent
   - no new incoming_item writes are started
   - existing pending mailbox ACK/recovery still progresses when applicable
6. Return to active gameplay.
7. Confirm resume log appears:
   - KirbyAM: gameplay-active state restored; resuming normal watcher flow
8. Repeat at least three transitions (gameplay -> non-gameplay -> gameplay) for consistency.

Expected signal source for this gate:
- ai_kirby_state_native at 0x0203AD2C (u32)
- known non-gameplay: value < 300, and goal-clear states 9999/10000
- gameplay-active: value 300 and unknown post-300 values (fail-open safety)

## Moonlight Mansion AP Check Contract (Issue #379)

Current shipped behavior is transport-flag based, not shard-check based:
- `BOSS_DEFEAT_2` is emitted from `boss_defeat_flags` bit `1` (`0x0202C024`).
- `MAJOR_CHEST_MOONLIGHT_MANSION` is emitted from `major_chest_flags` bit `2` (`0x0202C028`).
- Mirror shard collection is progression-state only and does not directly emit AP `LocationChecks`.

## Major Chest Checks (All Areas)

Validate that the transport major-chest bitfield drives the currently shipped major-chest locations while native map ownership stays item-delivery driven.

1. Connect AP + BizHawk session with KirbyAM client logs visible.
2. Open BizHawk Memory Viewer and watch `0x0202C028` as a 32-bit value.
3. Open one of the currently integrated big chests (repeat for each):
   - Rainbow Route (`bit 1`)
   - Moonlight Mansion (`bit 2`)
   - Cabbage Cavern (`bit 3`)
   - Mustard Mountain (`bit 4`)
   - Carrot Castle (`bit 5`)
   - Olive Ocean (`bit 6`)
   - Peppermint Palace (`bit 7`)
   - Radish Ruins (`bit 8`)
   - Candy Constellation (`bit 9`)
4. Confirm the corresponding bit flips from `0` to `1` when the chest reward is claimed.
5. Confirm `0x0203897C` does not flip for that area unless the corresponding AP map item is actually delivered.
6. Confirm the client logs a resend only if the server has not yet acknowledged the mapped location:
   - `KirbyAM: resending major-chest LocationChecks missing on server (...)`
7. Reconnect the AP client and confirm already-acknowledged major-chest checks are not replay-spammed.
8. Save/reload or change rooms and confirm the bit remains set.

Expected current mapping:
- `bit 1` -> `MAJOR_CHEST_RAINBOW_ROUTE`
- `bit 2` -> `MAJOR_CHEST_MOONLIGHT_MANSION`
- `bit 3` -> `MAJOR_CHEST_CABBAGE_CAVERN`
- `bit 4` -> `MAJOR_CHEST_MUSTARD_MOUNTAIN`
- `bit 5` -> `MAJOR_CHEST_CARROT_CASTLE`
- `bit 6` -> `MAJOR_CHEST_OLIVE_OCEAN`
- `bit 7` -> `MAJOR_CHEST_PEPPERMINT_PALACE`
- `bit 8` -> `MAJOR_CHEST_RADISH_RUINS`
- `bit 9` -> `MAJOR_CHEST_CANDY_CONSTELLATION`

## Vitality Chest Checks (Dedicated Room-Mapped Bits)

Validate that native vitality chest openings drive AP vitality-chest checks through the dedicated transport register.

1. Connect AP + BizHawk session with KirbyAM client logs visible.
2. Open BizHawk Memory Viewer and watch `0x0202C02C` as a 32-bit value.
3. Open each native vitality big chest and claim the reward:
   - Carrot Castle 5-23 (`bit 0`)
   - Olive Ocean 6-21 (`bit 1`)
   - Radish Ruins 8-4 (`bit 2`)
   - Candy Constellation 9-8 (`bit 3`)
4. Confirm the corresponding transport bit flips from `0` to `1` when the chest reward is claimed.
5. Confirm the client emits `LocationChecks` for the mapped vitality location IDs and dedupes acknowledged ones.
6. Reconnect AP client and verify no replay spam for already acknowledged vitality checks.

Expected current mapping:
- `bit 0` -> `VITALITY_CHEST_CARROT_CASTLE`
- `bit 1` -> `VITALITY_CHEST_OLIVE_OCEAN`
- `bit 2` -> `VITALITY_CHEST_RADISH_RUINS`
- `bit 3` -> `VITALITY_CHEST_CANDY_CONSTELLATION`

## Sound Player Chest Check (Issue #408)

Validate that the native Sound Player chest emits only an AP location check and does not
perform immediate native unlock.

1. Connect AP + BizHawk session with KirbyAM client logs visible.
2. Open BizHawk Memory Viewer and watch `0x0202C030` as a 32-bit value.
3. Open the native Sound Player chest.
4. Confirm `bit 0` flips from `0` to `1` and client emits `SOUND_PLAYER_CHEST` check.
5. Confirm native Sound Player remains locked until AP `SOUND_PLAYER` item is delivered.
6. Deliver AP `SOUND_PLAYER` and confirm native Sound Player unlock applies at receipt.

Expected current mapping:
- `bit 0` -> `SOUND_PLAYER_CHEST`

## Room Sanity Checks (Issue #480)

Validate that native room-visit flags in `gVisitedDoors` drive `Room X-YY` AP checks when the `room_sanity` option is enabled.

1. Generate a seed with `room_sanity: true` and connect AP + BizHawk with KirbyAM client logs visible.
2. Open BizHawk Memory Viewer and watch `0x02028CA0` as `u16[0x120]` (`gVisitedDoors`).
3. Enter a not-yet-visited room that corresponds to a Room Sanity location.
4. Confirm that the room's `doorsIdx` entry in `gVisitedDoors` has bit `15` set (`value & 0x8000 != 0`).
5. Confirm client emits `LocationChecks` for the mapped room-sanity location and logs resend only when the server has not yet acknowledged it:
   - `KirbyAM: resending room-sanity LocationChecks missing on server (...)`
6. Reconnect AP client and verify already acknowledged room-sanity checks are deduped (no replay spam).
7. Save/reload or room transition and confirm visited-state bit remains set.

Expected current mapping contract:
- Location key `ROOM_SANITY_X_YY` corresponds to AP label `Room X-YY`.
- `bit_index` stores native `doorsIdx`.
- Polling rule: `gVisitedDoors[doorsIdx] & 0x8000` => location considered checked.
- Scope: 257 eligible NORMAL/BIG rooms (special STAR/UNKNOWN rooms are excluded).

## Notification Pipeline Check (Issue #83)

Validate receive/send notifications and reconnect dedupe behavior.

1. Connect AP + BizHawk session with logs visible.
2. Receive at least one remote item and confirm notification text appears once.
3. Trigger at least one outgoing ItemSend (local check sending to another player) and confirm send text appears once.
4. Disconnect/reconnect AP client session.
5. Confirm previously shown receive/send notifications are not replay-spammed after reconnect.
6. Trigger one new receive and one new send event; confirm both still notify.

Expected behavior:
- Receive notification trigger: mailbox ACK for newly delivered index.
- Send notification trigger: local-sender `PrintJSON` ItemSend packet.
- Reconnect-safe dedupe prevents repeats for previously shown events.
- Receive text format: `Received <item_name> from <sender_name>`.
- Send text format: `You sent <item_name> to <receiver_name> at <location_name>` (or without location when unavailable).
- Burst summary text: `Skipped N send popup(s) to reduce spam`.
- Runtime gate state popups appear on transitions only:
  - `Item sending paused by game state`
  - `Item sending resumed`
- Goal completion popup appears when CLIENT_GOAL is sent:
  - `Goal complete`
- ROM load failures show concise popup error text matching the validation failure reason.

Issue #73 receive-focused checks:
- Skipped malformed items should not produce receive notification text.
- Cursor fast-forward/rewind reconciliation without a pending delivery should not replay old receive notifications.
- Issue #269 ACK path: if the ROM clears the flag and increments the counter in the same frame (common hardware
  case), a receive notification should still appear exactly once.  Verify by watching the BizHawk OSD while an
  item is delivered — the notification must appear even though the flag is already 0 when the client next polls.
- New ACK-completed deliveries after reconnect should still notify exactly once.

Issue #74 send-focused checks:
- Only local-sender ItemSend events should emit send notification text.
- ItemSend traffic between other players should not emit local send notifications.
- During rapid send bursts, notifications should rate-limit (max 5 per 2s) and
   later report a suppression summary message.

## DeathLink Smoke Check (Issue #82)

Validate the shipped end-to-end DeathLink contract across AP tag sync, incoming
receive/apply, outgoing send, and reconnect safety.

### Setup
1. Generate a seed with DeathLink enabled for at least two connected players.
2. Launch the KirbyAM BizHawk client with logs visible.
3. Confirm the client logs one of these on connect:
   - `KirbyAM: DeathLink enabled`
   - `KirbyAM: DeathLink disabled`
4. If DeathLink is disabled in slot-data, confirm no incoming kill apply or
   outgoing send occurs during the remaining checks.

### Incoming DeathLink
1. Put Kirby in normal gameplay (not menu/cutscene/transition).
2. Trigger a DeathLink from another player.
3. Confirm one local defeat occurs.
4. Confirm the client logs:
   - `KirbyAM: applied incoming DeathLink (hp_addr=0x02020FE0)`
5. Repeat while Kirby is already dead and confirm no extra HP write loop or
   repeated forced-death behavior occurs.

### Gameplay gate safety
1. Open a menu or trigger a non-gameplay transition.
2. Trigger a DeathLink from another player during that state.
3. Confirm no immediate death occurs during the non-gameplay window.
4. Return to gameplay-active state and confirm the queued DeathLink applies once.

### Outgoing DeathLink
1. Restore Kirby to a live gameplay state.
2. Take one normal in-game death locally.
3. Confirm exactly one outgoing DeathLink is observed by the linked player.
4. Confirm repeated frames while already dead do not send duplicates.

### Echo suppression and reconnect
1. Trigger an incoming DeathLink and confirm the resulting forced death does not
   immediately echo back as a second outgoing DeathLink.
2. Reconnect the AP client after a recent DeathLink event.
3. Confirm the client does not replay a stale forced death on reconnect.
4. Take one fresh local death after reconnect and confirm outgoing DeathLink
   still works normally.

### Native address reference
- `kirby_hp_native`: `0x02020FE0` (`s8`)
- Evidence: `gKirbys = 0x02020EE0` from `katam/linker.ld`, with `hp` field in
  `katam/include/kirby.h`

## Unsafe Delivery Candidate Research (Issue #223)

Issue #223 is currently in research-first mode. Do not assume miniboss or travel
signals are production-safe yet.

### Current candidate categories
1. Major boss fight candidates
   - existing `boss_mirror_table_native` probe logs rising-edge bits
2. Miniboss encounter counters
   - candidate symbols: `gShadowKirbyEncounters`, `gMirraEncounters`
3. Travel windows
   - cannon and warp-star flows currently look like transient object/task state,
     so they likely need hook-based instrumentation rather than memory polling

### Research workflow
1. Connect AP + BizHawk with client logs visible.
2. Trigger one candidate event at a time:
   - Shadow Kirby encounter/defeat
   - Mirra encounter/defeat
   - Cannon launch travel
   - Warp-star travel
3. Watch for observational log entries only; no delivery policy should change yet.
4. Record exact before/after values or hook points.
5. Repeat three times for consistency.
6. Promote only signals that are stable across repeats and reconnects.

### Expected current outcome
- Boss candidate logs may appear.
- Miniboss counters will only log if concrete native addresses are added later.
- Cannon/warp-star windows currently require additional hook research before enforcement.

## Connector Smoke Test (Issue #51)

Before gameplay/address verification, confirm the KirbyAM-specific BizHawk connector comes up cleanly:

1. Launch BizHawk with the Kirby & The Amazing Mirror USA ROM.
2. Open `Tools -> Lua Console`.
3. Run `data/lua/connector_kirbyam_bizhawk.lua`.
4. Confirm Lua Console shows:
   - `[KirbyAM Connector] ROM validation OK: ...`
   - `[KirbyAM Connector] Starting generic BizHawk transport bridge for KirbyAM.`
5. Start the Archipelago BizHawk Client and confirm the connection stabilizes without repeated attach/detach churn.

If this smoke test fails, fix connector startup/ROM context problems before trusting address-verification results.

## Mailbox Recovery Check (Issue #54)

When validating AP item receipt behavior in BizHawk, also watch for mailbox timeout recovery:

- Normal path: item write -> ROM clears `incoming_item_flag` -> client logs ACK and advances cursor.
- Recovery path: if `incoming_item_flag` remains high with no ACK, client logs a timeout warning (frame or wall-clock fallback), clears the flag, and retries the same delivery index conservatively.
- Counter reconciliation remains authoritative when `debug_item_counter` proves the ROM has already applied the item.

This behavior is intended to avoid deadlock while still preferring exactly-once ROM outcomes.

## Filler Receipt Compatibility Smoke (Issue #295)

Validate that each shipped filler item can be received and applied safely.

1. Connect a patched KirbyAM ROM to Archipelago with BizHawk logs visible.
2. Deliver each filler item at least once through the mailbox path:
   - `1 Up` (`3860001`)
   - `Small Food` (`3860026`)
   - `Cell Phone Battery` (`3860027`)
   - `Max Tomato` (`3860028`)
   - `Invincibility Candy` (`3860029`)
3. After each delivery, confirm:
   - mailbox ACK completes normally
   - `debug_last_item_id` matches the delivered filler
   - `1 Up`: Kirby's life count increases by 1 and saturates safely instead of overflowing at high values
   - `Small Food`: active Kirby HP increases by 1 when below max HP and does not exceed max HP
   - `Cell Phone Battery`: active Kirby battery increases by 1 when below 3 and does not exceed 3
   - `Max Tomato`: active Kirby HP becomes exactly max HP
   - `Invincibility Candy`: native invincibility behavior starts, including the normal timer/music path
4. Repeat one filler delivery after an AP reconnect and confirm the same ACK path still succeeds.
5. Confirm shard delivery behavior is unchanged after the filler smoke passes.

Expected current scope:
- live/item-side effects follow the current shipped filler contract in `PROTOCOL.md`
- no native pickup sprite drop is expected from mailbox receipt

## Reconnect Lifecycle Check (Issue #52)

Validate that both BizHawk and AP server reconnect scenarios work correctly:

### BizHawk disconnect/reconnect
1. Connect AP client + patched ROM normally.
2. Trigger at least one boss-defeat or major-chest location check and receive at least one AP item.
3. Close and re-open BizHawk (or restart the Lua script).
4. Confirm:
   - The acknowledged boss/major check is **not resent** as a duplicate (already in server `checked_locations`).
   - When boss-defeat/major-chest/vitality transport checks are present in RAM but server is missing them (e.g., server also restarted), the client **does** resend them.
   - Item delivery cursor resumes from the correct index (no re-delivery of already-applied items).
   - No mailbox deadlock: `incoming_item_flag` is clear after normal reattach.

### AP server disconnect/reconnect
1. Connect AP client + patched ROM normally.
2. Trigger at least one new location check.
3. Disconnect the AP server (or stop the AP server process briefly).
4. Reconnect.
5. Confirm:
   - Checks that were acknowledged before disconnect are **not resent**.
   - Checks collected while disconnected are resent on reconnect until acknowledged.
   - Goal reporting remains idempotent if goal was already sent before disconnect.

### Expected log indicators
- Normal resend: no output except standard location-check messages.
- Cursor resync: `KirbyAM: ROM item counter ... fast-forward delivery cursor` or rewind message.
- Boss probe: no false positive rising-bit log on reconnect (probe re-baselines cleanly).

## Quick Reference: Known Candidates

Policy references:
- `worlds/kirbyam/docs/notes.md`
- `worlds/kirbyam/data/native_address_policy.json`

Note: Address statuses (`candidate`, `integrated`, `verified`) and expected widths
in this guide are intended to match `native_address_policy.json`. If there is a
mismatch, treat the registry as authoritative and update this guide.

From `KirbyAM Data.xlsx` and cheat codes:

```
EWRAM Mailbox / Game State Region:
0x02038970 - Mirror Shards Bitfield (integrated) ← START HERE
0x02038960-0x0203896A - Chest/Switch blocks (supporting)
0x02028C14 - Boss/Mirror candidate table base (integrated probe)
```

## Integrated Probe Logging (Issue #110)

The KirbyAM BizHawk client now includes observational probing for boss candidate
bits at `boss_mirror_table_native` (`0x02028C14`, width `32` bytes).

Behavior:
- Baseline snapshot is captured on the first poll after probe/client handler initialization.
- BizHawk reconnects trigger probe re-baselining automatically via stream-identity change detection.
- Only rising-edge transitions (`0 -> 1`) are logged.
- Log format (debug level): `KirbyAM: boss candidate probe rising bits: 0x02028C14[bit3]`
- No AP location checks are sent from this probe yet.

Use this during boss fights to collect repeatable candidate transitions before
promoting any specific address/bit mapping into production logic. Enable debug
logging to see these events.

## Step-by-Step: Verify First Address (Mirror Shards)

### Phase 1: Baseline Reading

1. **Open BizHawk** with unmodified KAtAM USA ROM
2. **Pause emulation** at game start (main menu is fine)
3. **Open Memory Viewer**: Tools → Memory Viewer (or Ctrl+M)
4. **Navigate to address 0x02038970**:
   - Type into address bar
   - Should show 4 bytes (32-bit value)
   - Initial value should be `00 00 00 00` (no shards collected)

### Phase 2: Collect First Shard

1. **Record starting state**: Write down the 4 hex bytes displayed
2. **Resume emulation** and play until you collect the first mirror shard
3. **Capture the moment**:
   - Before collecting: Pause, note address value
   - Collect shard
   - Immediately pause, observe value change

**Expected**: Bit 0 becomes 1
- Before: `00 00 00 00` (binary: 0000 0000)
- After: `01 00 00 00` (binary: 0000 0001) ← Bit 0 set

### Phase 3: Verify Persistence

1. **Walk to next room** (don't lose/reload save)
2. **Pause and check address again**
3. **Expected**: Value still shows bit 0 set
4. **Reset/reload save** and verify value still persists

### Phase 4: Collect More Shards (Confirm Pattern)

1. **Collect 2nd shard**
   - Expected: `03 00 00 00` (bits 0-1 set)
2. **Collect 3rd shard**
   - Expected: `07 00 00 00` (bits 0-2 set)
3. **Collect 4th shard**
   - Expected: `0F 00 00 00` (bits 0-3 set)

If pattern holds: **✅ Address verified!**

---

## Boss Address Discovery (For Each Boss)

Since boss addresses likely aren't in the workbook, use this protocol:

### Manual Search Method

1. **Boss 1: Crepe (Moonlight Mansion)**
   - Navigate to Moonlight Mansion
   - Pause before entering boss
   - Open Memory Viewer: Tools → Cheats → Search
   - Select "Search Type: Number" and "Value Type: 32-bit"
   
2. **Initial State**:
   - Crepe not defeated
   - Search for value: `0` (or unknown)
   - Click "Search"
   - Result: Too many matches? Narrow scope:
     - Filter: RAM region 0x02038000 - 0x0203FFFF
   
3. **Defeat Crepe** in-game
   - Pause immediately after defeat
   - In Cheats window, change search:
   - Search for "Changed" or specific new value
   - Keep narrowing until you find the flip

4. **Confirm Result**:
   - Load a save *before* Crepe defeated
   - Search again - should find nothing in your narrowed region
   - Defeat Crepe again
   - Value should flip consistently

### Alternative: Scan Workbook Cheat Codes

The `.cht` file may contain boss addresses:
1. Open `Kirby _ the Amazing Mirror (USA, Europe) (Code Breaker).cht` in text editor
2. Search for keywords: "boss", "crepe", "defeat", "kracko"
3. Any found addresses → Add to candidate list
4. Test each candidate

---

## Memory Layout Reference

```
EWRAM Map (0x02000000 - 0x02031FFF = 200 KB)

0x02000000 ┌─ General Game State
           │
0x02030000 ├─ Approx. Player/Object Data Region
           │
0x02038960 ├─ Chest/Switch Flags (candidate) ← Support data
0x02038970 ├─ Shard Bitfield (candidate) ← Priority
           │
0x0202C000 ├─ AP Mailbox (reserved for randomizer)
           │  (shard_bitfield mirrored here by ROM payload)
           │
0x0203FFFF └─ End of EWRAM
```

---

## Testing Checklist Template

For each signal, copy this template:

```
## [Signal Name]

**Address**: 0x________
**Date Tested**: [Date]
**ROM State**: Unmodified USA

### Test 1: Initial Confirmation
- [ ] Before state: [hex value]
- [ ] Action: [what you did]
- [ ] After state: [hex value]  
- [ ] Changed: [✅ Yes / ❌ No]
- [ ] Time: [record time for reference]

### Test 2: Reload Confirmation
- [ ] Saved game with signal active
- [ ] Loaded save
- [ ] Value persists: [✅ Yes / ❌ No]

### Test 3: Repeated Action
- [ ] Did it again
- [ ] Result consistent: [✅ Yes / ❌ No]

### Verdict
- [ ] Confidence: 🟢 High / 🟡 Medium / 🔴 Low
- [ ] Status: ✅ Verified / ⚠️ Needs work / ❌ Rejected
```

### Machine-Checkable Result Comment Template

When reporting manual results on a GitHub issue, paste this block into a
comment and fill all fields exactly once:

```text
<!-- MANUAL_TEST_RESULT:START -->
RESULT_SCHEMA_VERSION: 1
TEST_CASE_ID: case-001
STATUS: PASS
BUILD_REF: <commit/pr/tag>
PLATFORM: <windows/linux/macos>
BIZHAWK_VERSION: <version>
ROM_REGION: USA
EXPECTED_RESULT: <short expected outcome>
OBSERVED_RESULT: <short observed outcome>
EVIDENCE: <link/screenshot/log excerpt>
NOTES: <optional>
<!-- MANUAL_TEST_RESULT:END -->
```

Allowed `STATUS` values: `PASS`, `FAIL`, `BLOCKED`.

---

## Troubleshooting

### "Address shows all zeros / garbage"
- Check ROM is fully loaded (wait 5 seconds after launch)
- Try adjacent addresses (off by 4 bytes?)
- Verify memory viewer is reading EWRAM, not VRAM/SRAM

### "Value never changes despite action"
- Action didn't complete (e.g., shard not actually collected)
- Address is read-only or mirrored elsewhere
- Game state stored in different memory region
- Try nearby addresses (0x02038968, 0x02038978, etc.)

### "Value changed but inconsistent"
- Timing issue: pause immediately after action
- Multiple addresses tracking same state
- Game uses SRAM (save RAM) not EWRAM - requires different search
- Note the behavior and mark as ⚠️ Medium confidence

---

## When Ready

Once chain is verified and documented:
1. Update `ADDRESS_VERIFICATION_MATRIX.md` with results
2. Extract final addresses into `worlds/kirbyam/data/addresses.json`
3. Record confidence levels
4. Commit and create PR for review

Good luck! 🎮
