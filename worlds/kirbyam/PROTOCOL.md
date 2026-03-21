# Kirby AM Protocol Contract

## Overview

This document defines the contract between the Archipelago server, the Python client, and the Kirby GBA ROM payload. All communication uses a shared EWRAM mailbox region for state synchronization.

## Memory Layout

### General Memory Map

```
EWRAM Layout (0x02000000 - 0x02040000):
  
  0x02000000 - 0x02040000   EWRAM Region (256 KB)
    ├─ 0x02000000 - 0x0202BFFF   Native game state
        ├─ 0x0202C000 - 0x0202C027   AP Mailbox (reserved, 40 bytes)
        └─ 0x0202C028 - 0x02040000   Rest of RAM (unused by AP)
```

### AP Mailbox Block (0x0202C000 - 0x0202C027)

**Transport Layer: Client ↔ ROM Communication**

| Offset | Addr     | Size | Name                  | Type | Direction   | Purpose |
|--------|----------|------|----------------------|------|-------------|---------|
| 0x00   | 0x0202C000 | 4B | shard_bitfield        | u32  | ROM → Client | Mirror of native shard flags (bits 0-7 currently used, bits 8-31 reserved) |
| 0x04   | 0x0202C004 | 4B | incoming_item_flag    | u32  | ROM ← Client | Write 1 to request delivery, ROM clears to 0 on ACK |
| 0x08   | 0x0202C008 | 4B | incoming_item_id      | u32  | ROM ← Client | Item ID to apply (BASE_OFFSET + item index) |
| 0x0C   | 0x0202C00C | 4B | incoming_item_player  | u32  | ROM ← Client | Player ID that sent this item |
| 0x10   | 0x0202C010 | 4B | debug_item_counter    | u32  | ROM → Client | Counter of items received (debug only) |
| 0x14   | 0x0202C014 | 4B | debug_last_item_id    | u32  | ROM → Client | Last item ID processed (debug only) |
| 0x18   | 0x0202C018 | 4B | debug_last_from       | u32  | ROM → Client | Last player ID (debug only) |
| 0x1C   | 0x0202C01C | 4B | frame_counter         | u32  | ROM → Client | Monotonic frame count (incremented every hook call) |
| 0x20   | 0x0202C020 | 4B | delivered_item_index  | u32  | Client ↔ ROM | Next item to deliver index (persisted in RAM) |

| 0x24   | 0x0202C024 | 4B | boss_defeat_flags     | u32  | ROM → Client | Bits 0–7 set when each area boss is defeated (same bit ordering as shard_bitfield) |

**Total: 40 bytes (0x0202C000 - 0x0202C027)**

### Native Game State (Referenced but not Managed by AP)

| Addr     | Size | Name                    | Description |
|----------|------|-------------------------|-------------|
| 0x02038970 | 1B | KIRBY_SHARD_FLAGS       | Native mirror shard bitfield (bits 0-7) |
| 0x02038960 - 0x0203896A | 10B | Chest/Switch state    | Native chest and switch flags |
| 0x02028C14+ |  -  | Boss/Mirror table       | Native location flags (TBD - not yet mapped) |
| 0x0203AD2C | 4B | AI_KIRBY_STATE          | Runtime phase classifier (Issue #56 gameplay gate) |

## Item ID Ranges

All item IDs use **BASE_OFFSET = 3860000** for safety (avoids collision with Archipelago global IDs).

| Item Type         | ID Range | Description |
|-------------------|----------|-------------|
| 1_UP              | 3860001  | Single extra life |
| SHARD_1 .. SHARD_8 | 3860002 - 3860009 | Mirror shards (8 items) |
| *Reserved*        | 3860010+ | Future items (doors, abilities, etc.) |

## Location ID Ranges

All location IDs use **BASE_OFFSET = 3860100**.

| Location Type | ID Range | Description |
|---------------|----------|-------------|
| SHARD_1 .. SHARD_8 | 3860101 - 3860108 | Mirror shard check locations (8 items) |
| BOSS_DEFEAT_1 .. BOSS_DEFEAT_8 | auto-assigned | Area boss defeat locations (8 locations) |
| *TBD*         | — | Chest locations, door locations, etc. |

## Client Protocol

### 1. Connection & Initialization

```
Client → Server: Connect with game="Kirby & The Amazing Mirror", slot="<player>"
Server → Client: ConnectionRefused | Connected
                 (with items_received, checked_locations, slot_data)
```

**Preconditions before gameplay watchers run:**
- `ctx.server` is not `None` and the socket is open.
- `ctx.slot_data` is not `None` (world-specific config was received).
- Runtime gameplay-active gate classifies `ai_kirby_state_native` before polling/delivery.

Both conditions are checked at the top of `game_watcher`. If either fails,
no RAM reads, location sends, item writes, or goal reports occur.

When runtime gate classifies non-gameplay:
- Defer location polling and boss-defeat polling.
- Defer new mailbox item writes.
- Continue mailbox ACK/recovery handling for already-pending deliveries.
- Continue goal polling (goal signal can occur in post-clear non-gameplay states).

Issue #223 status note:
- In-game unsafe delivery windows (major boss, miniboss, cannon travel, warp-star travel) are not yet part of the enforced protocol contract.
- Current client behavior is research-first: only observational candidate probing is allowed until stable native signals or hook points are verified.

### Runtime Gameplay-Active Gate (Issue #56)

Primary signal:
- `ai_kirby_state_native` (`0x0203AD2C`, u32)

POC classification contract:
- Gameplay-active: `ai_state == 300`
- Non-gameplay tutorial/menu: `ai_state < 200`
- Non-gameplay cutscene band: `200 <= ai_state < 300`
- Non-gameplay post-normal band: `ai_state > 300`

Fail-open behavior:
- If `ai_kirby_state_native` is unavailable in address mappings, watcher defaults to gameplay-active behavior for compatibility.

**On initial (or re-)connection, the following resync occurs automatically:**

| State | Resync behavior |
|---|---|
| Location checks | Level-based poll resends any RAM-derived checks missing from `checked_locations`. |
| Item delivery | Cursor is reconciled against ROM's `debug_item_counter`; delivery resumes from the correct index. |
| Goal reporting | Idempotent: goal location and CLIENT_GOAL are skipped when already reflected in `checked_locations`. |
| Boss probe | Probe snapshot re-baselines on BizHawk stream-identity change (reconnect safe). |
| Watcher transient state | On first tick after AP session becomes ready (`server/socket/slot_data`), reconnect diagnostics/probe caches are reset to clean baselines. |

The watcher includes an AP session-readiness transition hook that resets
transient diagnostics/probe caches exactly once per reconnect. Core gameplay
state still converges through level-based polling and cursor reconciliation on
every watcher tick.

### 2. Location Polling

**Active State:** Every frame (or periodic)

```python
# Run only when gameplay-active gate is true.

# Prefer native shard bitfield, fallback to mailbox mirror
if has_address("shard_bitfield_native"):
    bitfield = RAM[0x02038970] as u8  # native shard_bitfield_native (bits 0-7)
else:
    bitfield = RAM[0x0202C000] as u32  # transport mailbox mirror

# Collect all locations whose corresponding bit is set in the bitfield.
# Only consider bits that map to a known location; reserved/unmapped bits are ignored.
mapped_checked = set()
for bit in mapped_location_bits:  # only explicitly mapped bits
    if (bitfield >> bit) & 1:
        mapped_checked.add(location_id_for_bit(bit))

# Level-based, reconnect-safe resend:
# Send only checks that RAM reports as collected but the server has not acknowledged.
# This means checks are re-sent on reconnect until the server reflects them back,
# preventing permanent loss from dropped or early-session message failures.
missing_on_server = sorted(mapped_checked - server_checked_locations)
if missing_on_server:
    send LocationChecks(missing_on_server)
```

Bits 8-31 are reserved for future expansion and must be ignored until they are assigned to concrete location mappings.

**Behavior notes:**
- Detection is **level-based** (current bitfield state), not edge-based, to be reconnect-safe.
- No checks are sent for bits already in `server_checked_locations`.
- No checks are sent for reserved/unmapped bits even when set.
- Client logs resend reasons when RAM-derived checks are missing on server and logs dedupe suppression when all RAM-derived checks are already acknowledged.
- Diagnostics are transition-based to avoid per-tick log spam when mapped state is unchanged.
- Boss-defeat polling follows the same level-based resend/dedupe diagnostic contract.

### 3. Item Delivery (Mailbox Protocol)

**Precondition:** `incoming_item_flag == 0` (mailbox empty)

```python
# Write next item
item = items_received[delivered_item_index]
RAM[0x0202C008] = item.item_id  # u32
RAM[0x0202C00C] = item.player    # u32
RAM[0x0202C004] = 1              # Set flag (signal ROM)

# Wait for ROM to ACK
await ROM clears RAM[0x0202C004] to 0
delivered_item_index += 1
```

**State Machine:**
1. **Idle** (flag == 0): wait
2. **Pending** (flag == 1): ROM is processing, poll for flag == 0
3. **Acknowledged** (flag cleared): advance index, return to Idle

Research-first note for Issue #223:
- Delivery remains gated only by the gameplay-active contract from Issue #56.
- Candidate miniboss/travel probes must not suppress delivery until their semantics are repeatably verified.

### 3.1 Player Notification Pipeline (Issue #83)

KirbyAM now defines a player-facing notification pipeline for item traffic,
using BizHawk text rendering for Phase 1.

Event sources:
- Receive notifications: emitted on mailbox ACK completion for a delivered
    `ctx.items_received` index.
- Send notifications: emitted from `PrintJSON` packets when `type == "ItemSend"`
    and the local slot is the sender.

Display strategy:
- Phase 1: BizHawk connector text path (`display_message`).
- Phase 2 (future): native ROM/UI display only after stable hooks are verified.

Reconnect-safe dedupe:
- Receive dedupe key: delivered index.
- Send dedupe key: `(item_id, sender_id, receiver_id, location_id)`.
- Dedupe state is session-local and suppresses reconnect replay spam.

Receive-specific contract (Issue #73):
- Receive notification is emitted only after mailbox ACK for the pending index.
- Malformed/skipped `ReceivedItems` entries do not emit notifications.
- Cursor fast-forward/rewind reconciliation alone does not emit notifications.

Optional slot-data toggles (default: enabled when absent):
- `enable_receive_notifications`
- `enable_send_notifications`

Notification rendering is non-blocking for gameplay protocol behavior.
Delivery, location checks, and goal reporting continue even if notification
rendering fails.

### 4. Goal Reporting

**Current Implementation (native AI-state polling):**
```python
# World rules use explicit goal locations in REGION_DIMENSION_MIRROR/MAIN:
# - Defeat Dark Mind for Goal=Dark Mind
# - 100% Save File for Goal=100%

# Native signal source:
# ai_kirby_state_native @ 0x0203AD2C (u32)
# - Goal=Dark Mind: trigger selected goal location check on value 9999
# - Goal=100%: trigger selected goal location check on value 10000
#
# Note: 10000 is post-clear progression for Dark Mind mode and must not be
# treated as first-clear trigger when Goal=Dark Mind.
```

**Client StatusUpdate:**
```python
# Report selected goal location when native signal is active,
# then send CLIENT_GOAL after server acknowledges that location check.
if native_signal_active_for_selected_goal:
    send LocationChecks([goal_location_id])

if goal_location_id in checked_locations:
    send StatusUpdate(status=CLIENT_GOAL)
```

## ROM Payload Contract

### Entry Point

- Symbol: `ap_poll_mailbox_c()` (C function)
- Called by: GBA ROM hook (typically injected into main game loop)
- Frequency: Every frame (ideally)

### Responsibilities

1. **Poll mailbox flag** — Check if incoming_item_flag != 0
2. **Apply item** — Parse item_id, call `ap_apply_item(item_id)`
3. **Store debug state** — Update debug_item_counter, debug_last_item_id, debug_last_from
4. **Clear flag** — Set incoming_item_flag = 0 to signal ACK
5. **Mirror shard state** — Copy native KIRBY_SHARD_FLAGS to shard_bitfield
6. **Increment frame counter** — frame_counter++

### Item Application (`ap_apply_item`)

| Item Type | Behavior |
|-----------|----------|
| 1_UP | Increment KIRBY_LIVES (cap at 255) |
| SHARD_N | Set bit N-1 in KIRBY_SHARD_FLAGS (both native and mailbox mirror) |

## Timing Assumptions

- **Mailbox polling cadence:** Every frame (60 FPS assumed for GBA)
- **Client watcher tick:** ~0.125 second (BizHawk default), polling mailbox every tick
- **Frame counter wrap:** u32 @ 60 FPS wraps in ~2.4 weeks (acceptable for testing)
- **Item delivery latency:** Should observe ACK within frame(s) of flag write

## Error Handling

### Client Resilience

- **Corrupt item_id?** Log warning, skip to next index
- **Out-of-range player_id?** Log warning, still mark as delivered
- **Flag stuck HIGH?** After N frames (e.g., 30), warn, clear mailbox flag client-side, and retry the same delivery index conservatively
- **Bitfield bit flickers?** De-duplicate: only check new transitions (bit 0 → 1), ignore 1 → 0

### ROM Payload Resilience

- **Flag not cleared by client?** After N frames, reset (in case client crashed)
- **Invalid item_id?** Skip, do not apply, just clear flag and advance
- **Items delivered faster than ROM can process?** Mailbox protocol handles backpressure (client waits for ACK)

## Detection & Debugging

### Verifying Mailbox Communication

```bash
# BizHawk LUA script or address watch:
for addr in [0x0202C000, 0x0202C004, 0x0202C008]:
    print(f"RAM[{hex(addr)}] = {read(addr)}")
```

### Frame Counter Validation

- Should always increment (never decrease)
- Verify every frame with ~±10% tolerance (accounting for frame skips)

### Address Persistence Test

On client startup (cold boot):
1. Write a test pattern to delivered_item_index
2. Restart client
3. Verify pattern is still there (EWRAM preserved across soft resets)
4. If not: EWRAM may be cleared on ROM boot; adjust strategy

## References

- **Upstream Protocol:** See `docs/network protocol.md` in Archipelago root
- **AP Mailbox Spec:** See `worlds/kirbyam/data/addresses.json`
- **ROM Payload:** See `worlds/kirbyam/kirby_ap_payload/ap_payload.c`
- **Test Address Validator:** See `worlds/kirbyam/tools/validate_addresses.py` (TBD)
