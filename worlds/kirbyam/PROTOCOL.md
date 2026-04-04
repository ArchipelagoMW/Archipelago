# Kirby AM Protocol Contract

## Overview

This document defines the contract between the Archipelago server, the Python client, and the Kirby GBA ROM payload. All communication uses a shared EWRAM mailbox region for state synchronization.

## Purpose and Scope

Use this document as the protocol source-of-truth for runtime data exchange and delivery semantics.

- It defines mailbox memory layout, field ownership, and directionality.
- It defines item/location ID ranges and behavioral contracts for polling/delivery.
- It documents reconnect, ACK, and gameplay-gate behavior expected by server, client, and ROM payload.

Out of scope:

- World design rationale and balancing decisions.
- General implementation architecture outside protocol boundaries.
- Historical notes that do not affect current runtime contract.

Update policy:

- Any change to mailbox fields, ID contracts, or delivery/polling semantics must update this file in the same work cycle.
- If implementation and this document disagree, fix one immediately; do not leave contract drift unresolved.

## Memory Layout

### General Memory Map

```
EWRAM Layout (0x02000000 - 0x02040000):
  
    0x02000000 - 0x02040000   EWRAM Region (256 KB)
        ├─ 0x02000000 - 0x0202BFFF   Native game state
        ├─ 0x0203B000 - 0x0203B04B   AP Mailbox (reserved, 76 bytes)
        └─ Remaining EWRAM (excluding AP mailbox block)
```

### AP Mailbox Block (0x0203B000 - 0x0203B04B)

**Transport Layer: Client ↔ ROM Communication**

| Offset | Addr     | Size | Name                  | Type | Direction   | Purpose |
|--------|----------|------|----------------------|------|-------------|---------|
| 0x00   | 0x0203B000 | 4B | shard_bitfield        | u32  | ROM → Client | Mirror of native shard flags (bits 0-7 currently used, bits 8-31 reserved) |
| 0x04   | 0x0203B004 | 4B | incoming_item_flag    | u32  | ROM ← Client | Write 1 to request delivery; ROM clears to 0 after recognized item apply (ACK) |
| 0x08   | 0x0203B008 | 4B | incoming_item_id      | u32  | ROM ← Client | Item ID to apply (BASE_OFFSET + item index) |
| 0x0C   | 0x0203B00C | 4B | incoming_item_player  | u32  | ROM ← Client | Player ID that sent this item |
| 0x10   | 0x0203B010 | 4B | debug_item_counter    | u32  | ROM → Client | Counter of items received (debug only) |
| 0x14   | 0x0203B014 | 4B | debug_last_item_id    | u32  | ROM → Client | Last item ID processed (debug only) |
| 0x18   | 0x0203B018 | 4B | debug_last_from       | u32  | ROM → Client | Last player ID (debug only) |
| 0x1C   | 0x0203B01C | 4B | frame_counter         | u32  | ROM → Client | Monotonic frame count (incremented every hook call) |
| 0x20   | 0x0203B020 | 4B | delivered_item_index  | u32  | Client ↔ ROM | Next item to deliver index (persisted in RAM) |

| 0x24   | 0x0203B024 | 4B | boss_defeat_flags     | u32  | ROM → Client | Bits 0–7 set when each area boss is defeated; recorded by a hook that replaces the native `CollectShard` call (same bit ordering as shard_bitfield) |
| 0x28   | 0x0203B028 | 4B | major_chest_flags     | u32  | ROM → Client | Bits set when a native big chest is opened; bit N = area ID N. This drives AP major-chest checks independently of native map ownership. |
| 0x2C   | 0x0203B02C | 4B | vitality_chest_flags  | u32  | ROM → Client | Bits set when a native vitality big chest is opened; bits 0..3 map to the four vitality chest room IDs (Carrot 5-23, Olive 6-21, Radish 8-4, Candy 9-8). |
| 0x30   | 0x0203B030 | 4B | sound_player_chest_flags | u32 | ROM → Client | Bits set when the native Sound Player chest is opened; bit 0 maps to `SOUND_PLAYER_CHEST`. Native Sound Player unlock is intentionally deferred until AP item receipt. |
| 0x34   | 0x0203B034 | 4B | hook_heartbeat        | u32  | ROM → Client | Increments once on every AP main hook entry. Diagnostic signal for hook liveness. |
| 0x38   | 0x0203B038 | 4B | delivered_shard_bitfield | u32 | ROM → Client | Bits 0–7 represent shard ownership authority. On mailbox initialization (`mailbox_init_cookie` absent/mismatched), `ap_poll_mailbox_c()` seeds this from current native shard save state; after init, shard delivery in `ap_apply_item()` sets additional bits. Never set by boss-defeat hook. Used by scrub logic (Issue #478 / #505) to clamp `KIRBY_SHARD_FLAGS` to AP-owned bits. |
| 0x3C   | 0x0203B03C | 4B | shard_scrub_delay_frames | u32 | ROM internal | Countdown timer (frames). Set to 600 by boss-defeat hook while temporary native shard state is visible during post-boss cutscene. |
| 0x40   | 0x0203B040 | 4B | mailbox_init_cookie | u32 | ROM internal | Initialization cookie (`0x4B41504D`). If absent/mismatched, payload seeds `delivered_shard_bitfield` from native shard state, clears scrub delay + boss-defeat flags + boss temp shard mask, and stores the cookie to prevent stale EWRAM transport values from triggering scrub writes. |
| 0x44   | 0x0203B044 | 4B | boss_temp_shard_bitfield | u32 | ROM internal | Bits 0-7 track shard bits temporarily written by boss-defeat hook for cutscene safety. On gameplay resume, payload scrubs only `boss_temp_shard_bitfield & ~delivered_shard_bitfield`, then clears this mask. |
| 0x48   | 0x0203B048 | 4B | delivered_vitality_item_bits | u32 | ROM internal | Replay guard for vitality counter items. Bit N marks that `VITALITY_COUNTER_(N+1)` has already been applied, preventing duplicate vitality grants if an item is resent during reconnect/reset recovery. |

**Total: 76 bytes (0x0203B000 - 0x0203B04B)**

### Native Game State (Referenced but not Managed by AP)

| Addr     | Size | Name                    | Description |
|----------|------|-------------------------|-----------|
| 0x02038970 | 1B | KIRBY_SHARD_FLAGS       | Native mirror shard bitfield (bits 0-7) |
| 0x0203897C | 4B | big_chest_bitfield_native | gTreasures.bigChestField; bit N = area ID N (enum AreaId): bit 1=Rainbow Route, 2=Moonlight Mansion, 3=Cabbage Cavern, 4=Mustard Mountain, 5=Carrot Castle, 6=Olive Ocean, 7=Peppermint Palace, 8=Radish Ruins, 9=Candy Constellation. This now reflects native map ownership only; AP major-chest checks use `major_chest_flags` in the transport block. |
| 0x02038960 - 0x0203896A | 10B | Chest/Switch state    | Native chest and switch flags |
| 0x02028C14+ |  -  | Boss/Mirror table       | Native location flags (TBD - not yet mapped) |
| 0x02028CA0 | 576B | gVisitedDoors (`room_visit_flags_native`) | Native room-visit array (`u16[0x120]`); bit 15 marks visited state by `doorsIdx` |
| 0x0203AD2C | 4B | AI_KIRBY_STATE          | Runtime phase classifier (Issue #56 gameplay gate) |
| 0x0203AD10 | 4B | DEMO_PLAYBACK_FLAGS     | Native title-demo discriminator (`demo_playback_flags_native`; bit `0x10` indicates title-screen demo playback) |
| 0x02020FE0 | 1B | KIRBY_HP                | Kirby HP (`s8`) used for DeathLink runtime receive/apply and local death transition detection |
| 0x02020FE1 | 1B | KIRBY_MAX_HP            | Kirby max HP (`s8`) used for one-hit mode enforcement (player 0 struct) |
| 0x02020FE2 | 1B | KIRBY_LIVES             | Native extra-life counter (`u8`) used for `no_extra_lives` enforcement |
| 0x02038980 | 2B | KIRBY_VITALITY_COUNTER  | Native vitality counter (`u16`); incremented by ROM payload on Vitality Counter item delivery; read by one-hit mode enforcement |

## Item ID Ranges

All item IDs use **BASE_OFFSET = 3860000** for safety (avoids collision with Archipelago global IDs).

| Item Type         | ID Range | Description |
|-------------------|----------|-------------|
| 1_UP              | 3860001  | Single extra life |
| SHARD_1 .. SHARD_8 | 3860002 - 3860009 | Mirror shards (8 items) |
| MAP_MUSTARD_MOUNTAIN .. MAP_RADISH_RUINS | 3860010 - 3860017 | Useful map rewards |
| VITALITY_COUNTER_1 .. VITALITY_COUNTER_4 | 3860018 - 3860021 | Useful vitality rewards |
| MAP_RAINBOW_ROUTE | 3860024 | Useful map reward |
| SOUND_PLAYER      | 3860025 | Useful unlock reward (applies native Sound Player unlock on receipt) |
| FOOD, BATTERY, MAX_TOMATO, INVINCIBILITY_CANDY | 3860026 - 3860029 | Filler consumable rewards |
| *Reserved*        | 3860030+ | Future items (doors, abilities, additional consumables, etc.) |

### Current filler effect contract

Current shipped filler generation uses a uniform active filler pool:

| Item | Effect |
|------|--------|
| `1 Up` | Grants 1 life, saturating at 255 |
| `Small Food` | Increments active Kirby HP by 1 if Kirby is alive (`hp > 0`) and below max HP; no effect for `hp <= 0` |
| `Cell Phone Battery` | Increments active Kirby battery by 1 if below 3 |
| `Max Tomato` | Sets active Kirby HP to max HP if Kirby is alive (`hp > 0`); no effect for `hp <= 0` |
| `Invincibility Candy` | Applies the native invincibility state using the decomp-backed 1000-tick helper path |

## Location ID Ranges

All location IDs use **BASE_OFFSET + 100_000** as the auto-assignment start (= 3,960,000).

| Location Type | ID Range | Description |
|---------------|----------|-------------|
| GOAL_DARK_MIND | auto-assigned | Internal goal metadata entry. Current shipped worlds convert this to an addressless runtime event, so the client reports `CLIENT_GOAL` directly instead of sending a numeric `LocationChecks` entry. |
| BOSS_DEFEAT_1 .. BOSS_DEFEAT_8 | auto-assigned | Area boss defeat locations (8 locations) |
| MAJOR_CHEST_CABBAGE_CAVERN | 3960200 | Cabbage Cavern big chest (bit 3, gTreasures.bigChestField) |
| MAJOR_CHEST_OLIVE_OCEAN | 3960201 | Olive Ocean big chest (bit 6, gTreasures.bigChestField) |
| MAJOR_CHEST_PEPPERMINT_PALACE | 3960202 | Peppermint Palace big chest (bit 7, gTreasures.bigChestField) |
| MAJOR_CHEST_RAINBOW_ROUTE | 3960203 | Rainbow Route big chest (bit 1, gTreasures.bigChestField) |
| MAJOR_CHEST_MOONLIGHT_MANSION | 3960204 | Moonlight Mansion big chest (bit 2, gTreasures.bigChestField) |
| MAJOR_CHEST_MUSTARD_MOUNTAIN | 3960205 | Mustard Mountain big chest (bit 4, gTreasures.bigChestField) |
| MAJOR_CHEST_CARROT_CASTLE | 3960206 | Carrot Castle big chest (bit 5, gTreasures.bigChestField) |
| MAJOR_CHEST_RADISH_RUINS | 3960207 | Radish Ruins big chest (bit 8, gTreasures.bigChestField) |
| MAJOR_CHEST_CANDY_CONSTELLATION | 3960208 | Candy Constellation big chest (bit 9, gTreasures.bigChestField) |
| VITALITY_CHEST_CARROT_CASTLE | 3960300 | Carrot Castle 5-23 vitality big chest (transport vitality bit 0) |
| VITALITY_CHEST_OLIVE_OCEAN | 3960301 | Olive Ocean 6-21 vitality big chest (transport vitality bit 1) |
| VITALITY_CHEST_RADISH_RUINS | 3960302 | Radish Ruins 8-4 vitality big chest (transport vitality bit 2) |
| VITALITY_CHEST_CANDY_CONSTELLATION | 3960303 | Candy Constellation 9-8 vitality big chest (transport vitality bit 3) |
| SOUND_PLAYER_CHEST | 3960304 | Candy Constellation Sound Player chest (transport sound_player_chest bit 0) |
| ROOM_SANITY_1_01 .. ROOM_SANITY_9_27 | 3961000+ | Room visit checks (`Room X-YY`) keyed by native `doorsIdx` and polled from `gVisitedDoors[doorsIdx]` bit 15 |
| *Reserved*    | 3960305+ | Future location families |

## Client Protocol

### 1. Connection & Initialization

```
Client → Server: Connect with game="Kirby & The Amazing Mirror", slot="<player>"
Server → Client: ConnectionRefused | Connected
                 (with items_received, checked_locations, slot_data)

`slot_data` currently includes:
- `goal` (int): selected goal option.
- `shards` (int): shard randomization mode.
- `no_extra_lives` (bool): when true, exclude `1 Up` filler generation and have the BizHawk client clamp the native life counter to `0` during gameplay.
- `one_hit_mode` (int): one-hit mode selection (`0=off`, `1=exclude_vitality_counters`, `2=include_vitality_counters`). When non-zero, Kirby's max HP is clamped to `vitality_counter + 1` during gameplay. In `exclude_vitality_counters` mode, Vitality Counter items are removed from the item pool (replaced by filler) so the cap stays at 1. In `include_vitality_counters` mode, Vitality Counter items remain in the pool and each one received raises the cap by 1.
- `death_link` (bool): enables/disables AP DeathLink tag synchronization in the client.
- `ability_randomization_mode` (int): enemy copy-ability mode (`0=off`, `1=shuffled`, `2=completely_random`).
- `ability_randomization_boss_spawns` (bool): include/exclude ability-granting boss-spawned objects.
- `ability_randomization_minibosses` (bool): include/exclude mini-boss ability grants.
- `ability_randomization_minny` (bool): include/exclude Minny from enemy copy-ability randomization.
- `ability_randomization_passive_enemies` (bool): when true, enemies that natively grant no ability participate in copy-ability randomization. Default: `true`.
- `ability_randomization_no_ability_weight` (int): percentage chance from `0` to `100` that an included randomized enemy grant resolves to no ability instead of a copy ability. Default: `55`.
- `room_sanity` (bool): enables/disables room-visit locations (`Room X-YY`, 257 checks).
- `enemy_copy_ability_whitelist` (list[str]): validated ability pool (must exclude `Wait`).
- `enemy_copy_ability_policy` (dict): deterministic policy payload used by runtime hooks.
- `debug` (dict): debug settings payload.
    - `logging` (bool): when true, client emits diagnostics for gameplay-state/demo-flag transitions (including `hook_heartbeat`) and self-ItemSend fallback decisions.

Compatibility note (Issue #398 option-key reorganization):
- Legacy keys `enemy_copy_ability_randomization`, `randomize_boss_spawned_ability_grants`, and `randomize_miniboss_ability_grants` are intentionally not emitted in `slot_data` during the pre-public (`< v0.1.0`) phase.
- Canonical keys are `ability_randomization_mode`, `ability_randomization_boss_spawns`, `ability_randomization_minibosses`, `ability_randomization_minny`, `ability_randomization_passive_enemies`, and `ability_randomization_no_ability_weight`.
- If compatibility aliases are needed after public release, this section will be updated with an explicit deprecation/removal timeline.

DeathLink runtime behavior contract:
- Incoming DeathLink packets (`Bounced` with `DeathLink` tag) are queued and only applied when gameplay-active gate is true.
- Application writes `kirby_hp_native` to `0` to trigger local defeat.
- Outgoing DeathLink uses alive->dead transitions on `kirby_hp_native` and sends once per transition.
- Outgoing DeathLink cause text is selected randomly from `worlds/kirbyam/data/deathlink_flavor_text.json`.
    Each template should use the `{player}` placeholder for the sender name.
- Incoming-application echo suppression prevents immediate re-broadcast loops.

`no_extra_lives` runtime behavior contract:
- Generation removes `1 Up` from the active filler pool when the option is enabled.
- During gameplay, the BizHawk client clamps `kirby_lives_native` to `0` so the player starts with zero extra lives and native/in-game life gains are overwritten.
- Any `no_extra_lives` runtime diagnostics must remain gated behind `debug.logging`.

`one_hit_mode` runtime behavior contract:
- Generation removes all four Vitality Counter items from the non-filler item pool (replaced by filler) when `one_hit_mode == exclude_vitality_counters` (1). Vitality Chest locations are kept, but this mode does not guarantee location-specific filler placement on those chests.
- In `exclude_vitality_counters` mode, filler selection also removes health-restoring filler (`Small Food`, `Max Tomato`) so randomized filler does not counteract the 1 HP challenge. If `no_extra_lives` is also enabled, `1 Up` is removed from that reduced filler pool as well.
- Generation leaves the item pool unchanged when `one_hit_mode == include_vitality_counters` (2).
- During gameplay, when `one_hit_mode != vanilla`, the BizHawk client reads `kirby_vitality_counter_native` (`u16`) and enforces `desired_max_hp = vitality_counter + 1` (capped to `0x7F`) onto `kirby_max_hp_native` and `kirby_hp_native` for player 0's struct.
- Dead/negative HP states (`current_hp <= 0`) are preserved; only alive Kirby's HP is clamped.
- Any `one_hit_mode` runtime diagnostics must remain gated behind `debug.logging`.
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
- Non-gameplay tutorial/menu: `ai_state < 200`
- Non-gameplay cutscene band: `200 <= ai_state < 300`
- Non-gameplay title demo: `ai_state == 300` when native demo playback flag `demo_playback_flags_native` (underlying symbol `gUnk_0203AD10`, bit `0x10`) is set
- Non-gameplay goal-clear states: `ai_state in {9999, 10000}`
- Gameplay-active: all other observed states (including non-demo `300` and unknown post-300 values)

Fail-open behavior:
- If `ai_kirby_state_native` is unavailable in address mappings, watcher defaults to gameplay-active behavior for compatibility.
- Unknown post-300 states fail open as gameplay-active to avoid blocking mailbox item receipt (Issue #419).
- Demo discrimination uses the mapped native key `demo_playback_flags_native` (`0x0203AD10`, bit `0x10`) based on katam decomp evidence that title-screen demos set this flag before forcing `gAIKirbyState = AI_KIRBY_STATE_NORMAL`.
- Runtime gate batches AI/demo native reads in one BizHawk call and treats missing `demo_playback_flags_native` as inactive (fail open).

**On initial (or re-)connection, the following resync occurs automatically:**

| State | Resync behavior |
|---|---|
| Location checks | Level-based poll resends any RAM-derived checks missing from `checked_locations`. |
| Item delivery | Cursor is reconciled against ROM's `debug_item_counter`; delivery resumes from the correct index. |
| Goal reporting | Idempotent: for current shipped worlds, the client re-sends `CLIENT_GOAL` on reconnect when `finished_game` is set. If a future world exposes a numeric goal location, the client falls back to goal-location acknowledgement before `CLIENT_GOAL`. |
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

# Boss-defeat checks (transport mailbox bitfield)
boss_bits = RAM[0x0203B024] as u32
for bit in mapped_boss_bits:
    if (boss_bits >> bit) & 1:
        mapped_checked.add(boss_location_id_for_bit(bit))

# Major-chest checks (transport major_chest_flags)
chest_bits = RAM[0x0203B028] as u32
for bit in mapped_major_chest_bits:
    if (chest_bits >> bit) & 1:
        mapped_checked.add(major_chest_location_id_for_bit(bit))

# Vitality-chest checks (transport vitality_chest_flags)
vitality_bits = RAM[0x0203B02C] as u32
for bit in mapped_vitality_chest_bits:
    if (vitality_bits >> bit) & 1:
        mapped_checked.add(vitality_chest_location_id_for_bit(bit))

# Sound Player chest checks (transport sound_player_chest_flags)
sound_player_bits = RAM[0x0203B030] as u32
for bit in mapped_sound_player_chest_bits:
    if (sound_player_bits >> bit) & 1:
        mapped_checked.add(sound_player_chest_location_id_for_bit(bit))

# Room sanity checks (native gVisitedDoors)
room_visits = RAM[0x02028CA0 : 0x02028CA0 + 0x240] as u16[0x120]
for doors_idx in mapped_room_sanity_doors_indices:
    if room_visits[doors_idx] & 0x8000:
        mapped_checked.add(room_sanity_location_id_for_doors_idx(doors_idx))

# Level-based, reconnect-safe resend:
# Send only checks that RAM reports as collected but the server has not acknowledged.
# This means checks are re-sent on reconnect until the server reflects them back,
# preventing permanent loss from dropped or early-session message failures.
missing_on_server = sorted(mapped_checked - server_checked_locations)
if missing_on_server:
    send LocationChecks(missing_on_server)
```

Mirror shard bitfields (`shard_bitfield_native` / `shard_bitfield`) are progression-state signals only. `delivered_shard_bitfield` is the authority used by scrub logic to enforce that `KIRBY_SHARD_FLAGS` (and therefore all `HasShard()` / `NumShardsCollected()` gate checks) reflects AP-owned shard state (Issue #478 / #505): it is seeded from native shard save state on mailbox init, then extended by AP `SHARD_N` item delivery. Boss defeats are reported through `boss_defeat_flags`, major chest openings are reported through `major_chest_flags`, vitality chest openings are reported through `vitality_chest_flags`, and Sound Player chest openings are reported through `sound_player_chest_flags`. Native boss shard / native big-chest map / native vitality grants are intercepted so progression, map ownership, and vitality growth come only from AP item delivery, and native Sound Player unlock is similarly intercepted so unlock ownership comes only from AP `SOUND_PLAYER` receipt.

Boss shard scrub timing contract (Issue #505):
- Boss hook writes temporary native shard state for cutscene safety and marks `boss_temp_shard_bitfield`.
- During non-gameplay boss/cutscene states, payload may decrement `shard_scrub_delay_frames` but does not scrub pending boss-temp bits.
- On gameplay resume, payload scrubs only `boss_temp_shard_bitfield & ~delivered_shard_bitfield`, persists the result to SRAM, and clears `boss_temp_shard_bitfield` + delay.

**Behavior notes:**
- Detection is **level-based** (current bitfield state), not edge-based, to be reconnect-safe.
- No checks are sent for bits already in `server_checked_locations`.
- No checks are sent for reserved/unmapped bits even when set.
- Boss-defeat, major-chest, vitality-chest, sound-player-chest, and room-sanity polling follow the same resend/dedupe diagnostic contract.
- Diagnostics are transition-based to avoid per-tick log spam when mapped state is unchanged.

### 3. Item Delivery (Mailbox Protocol)

**Precondition:** `incoming_item_flag == 0` (mailbox empty)

```python
# Write next item
item = items_received[delivered_item_index]
RAM[0x0203B008] = item.item_id  # u32
RAM[0x0203B00C] = item.player    # u32
RAM[0x0203B004] = 1              # Set flag (signal ROM)

# Wait for ROM to ACK
await ROM clears RAM[0x0203B004] to 0
delivered_item_index += 1
```

Behavior note:
- If `incoming_item_id` is not recognized by the shipped payload handler, ROM does not ACK by clearing the flag.
- Client timeout recovery then clears/retries conservatively and logs the timeout reason.

**State Machine:**
1. **Idle** (flag == 0): wait
2. **Pending** (flag == 1): ROM is processing, poll for flag == 0
3. **Acknowledged** (flag cleared): advance index, return to Idle
4. **Recovery** (pending too long): client timeout path clears stale flag and retries same delivery index

`debug_item_counter` reconciliation contract:
- If `debug_item_counter < delivered_item_index`, rewind cursor to the ROM count.
- If `debug_item_counter` is ahead but still within `len(ctx.items_received)`, fast-forward cursor to the ROM count.
- If `debug_item_counter > len(ctx.items_received)`, treat the counter as stale/debug-only and continue normal mailbox delivery once the mailbox is empty. This anti-starvation fallback must not permanently suppress writes.
- Transition-based logs should make the ahead-counter fallback visible without per-tick spam.

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
- Cursor fast-forward/rewind reconciliation without a pending delivery does not emit notifications.
- Exception (Issue #269): when the ROM counter advances while a delivery is pending and the mailbox
  flag is already cleared (flag == 0), this simultaneous counter-advance is treated as the ACK
  signal and does emit a notification.  This covers the common hardware case where the ROM clears
  the flag and increments debug_item_counter in the same frame, so the fast-forward reconciliation
  path runs before the normal flag == 0 polling path on the next client tick.

Optional slot-data toggles (default: enabled when absent):
- `enable_receive_notifications`
- `enable_send_notifications`

Notification rendering is non-blocking for gameplay protocol behavior.
Delivery, location checks, and goal reporting continue even if notification
rendering fails.

Send-specific contract (Issue #74):
- Send notifications emit only for `PrintJSON` `ItemSend` packets where local
    slot is the sender.
- Unrelated ItemSend packets between other players are ignored.
- Burst rate limit policy:
    - at most 5 send notifications per 2-second window
    - additional sends in the same window are suppressed
    - a summary message reports suppressed count when the window rolls over

Send notification message format (Issue #432):
- If location is available: `"You sent <item_name> to <receiver_name> at <location_name>"`
- If location unavailable: `"You sent <item_name> to <receiver_name>"`
- Sender name is omitted: the local player already knows who sent the item.
- Item names resolved from AP item-name context for the relevant slot; if unavailable, from KirbyAM world item data; finally falling back to `"Item <id>"`.
- Location names resolved from AP location address mappings, with fallback to `"Location <id>"`.
- Receiver names resolved from AP `player_names` context, with fallbacks: Archipelago (player 0), or `"Player <id>"`.

Receive notification message format:
- Format: `"Received <item_name> from <sender_name>"`
- Phrasing is optimized for readability within BizHawk's short display window.
- Item and player names use same resolution as send notifications above.
Other player-visible client popups:
- ROM validation failures show concise load errors, for example:
  - `Unable to load ROM: base ROM detected. Please use a patched ROM.`
  - `Unable to load ROM: invalid Kirby and the Amazing Mirror ROM.`
  - `Unable to load ROM: missing patch metadata. Rebuild your patched ROM.`
- Runtime gate transitions:
  - `Item sending paused by game state`
  - `Item sending resumed`
- Goal completion status:
  - `Goal complete`
### 4. Goal Reporting

**Current Implementation (native AI-state polling):**
```python
# World rules use explicit goal location in REGION_DIMENSION_MIRROR/MAIN:
# - Defeat Dark Mind

# Native signal source:
# ai_kirby_state_native @ 0x0203AD2C (u32)
# - Trigger goal completion on value 9999
# - Accept 10000 as a fallback post-clear signal if 9999 was missed live
#
# Note: 10000 remains post-clear progression, but the client accepts it as a
# fallback completion signal to avoid missing goal reporting when 9999 is transient.
```

**Client StatusUpdate:**
```python
# Current shipped worlds convert the goal location into an addressless runtime
# event, so the client sends CLIENT_GOAL directly.
if native_signal_active_for_selected_goal and goal_location_is_addressless:
    send StatusUpdate(status=CLIENT_GOAL)

# Compatibility path for future world versions that expose a numeric goal
# location to the server.
if native_signal_active_for_selected_goal and goal_location_is_numeric:
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
for addr in [0x0203B000, 0x0203B004, 0x0203B008]:
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
