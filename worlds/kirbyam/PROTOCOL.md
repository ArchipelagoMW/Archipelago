# Kirby AM Protocol Contract

## Overview

This document defines the contract between the Archipelago server, the Python client, and the Kirby GBA ROM payload. All communication uses a shared EWRAM mailbox region for state synchronization.

## Memory Layout

### General Memory Map

```
EWRAM Layout (0x02000000 - 0x02040000):
  
  0x02000000 - 0x02040000   EWRAM Region (256 KB)
    ├─ 0x02000000 - 0x0202BFFF   Native game state
        ├─ 0x0202C000 - 0x0202C023   AP Mailbox (reserved, 36 bytes)
        └─ 0x0202C024 - 0x02040000   Rest of RAM (unused by AP)
```

### AP Mailbox Block (0x0202C000 - 0x0202C023)

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

**Total: 36 bytes (0x0202C000 - 0x0202C023)**

### Native Game State (Referenced but not Managed by AP)

| Addr     | Size | Name                    | Description |
|----------|------|-------------------------|-------------|
| 0x02038970 | 1B | KIRBY_SHARD_FLAGS       | Native mirror shard bitfield (bits 0-7) |
| 0x02038960 - 0x0203896A | 10B | Chest/Switch state    | Native chest and switch flags |
| 0x02028C14+ |  -  | Boss/Mirror table       | Native location flags (TBD - not yet mapped) |

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
| *TBD*         | 3860109+ | Chest locations, boss defeats, etc. |

## Client Protocol

### 1. Connection & Initialization

```
Client → Server: Connect with game="Kirby & The Amazing Mirror", slot="<player>"
Server → Client: ConnectionRefused | Connected
                 (with items_received, checked_locations, slot_data)
```

### 2. Location Polling

**Active State:** Every frame (or periodic)

```python
# Prefer native shard bitfield, fallback to mailbox mirror
if has_address("shard_bitfield_native"):
    bitfield = RAM[0x02038970] as u8  # native shard_bitfield_native (bits 0-7)
else:
    bitfield = RAM[0x0202C000] as u32  # transport mailbox mirror

# For each set bit in the 32-bit shard bitfield:
for bit in range(32):
    if (bitfield >> bit) & 1:
        if bit not previously seen and bit maps to a known location:
            location_id = 3860100 + bit + 1
            send LocationChecks([location_id])
```

Bits 8-31 are reserved for future expansion and must be ignored until they are assigned to concrete location mappings.

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

### 4. Goal Reporting

**Temp Implementation:**
```python
# Check completion based on all locations checked
if all(loc_id in checked_locations for loc_id in all_location_ids):
    send StatusUpdate(status=CLIENT_GOAL)
```

**TODO:** Replace with actual Dark Mind defeat signal from native game state (TBD address).

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
- **Flag stuck HIGH?** After N frames (e.g., 30), clear client-side and advance (ROM crash recovery)
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
