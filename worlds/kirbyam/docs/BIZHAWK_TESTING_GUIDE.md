# BizHawk Testing Guide for Address Verification

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
- gameplay-active only when value == 300

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
- Recovery path: if `incoming_item_flag` remains high for roughly 30 frames with no ACK, client logs a timeout warning, clears the flag, and retries the same delivery index conservatively.
- Counter reconciliation remains authoritative when `debug_item_counter` proves the ROM has already applied the item.

This behavior is intended to avoid deadlock while still preferring exactly-once ROM outcomes.

## Reconnect Lifecycle Check (Issue #52)

Validate that both BizHawk and AP server reconnect scenarios work correctly:

### BizHawk disconnect/reconnect
1. Connect AP client + patched ROM normally.
2. Trigger at least one shard location check (collect a shard in-game) and receive at least one AP item.
3. Close and re-open BizHawk (or restart the Lua script).
4. Confirm:
   - Shard check is **not resent** as a duplicate (already in server `checked_locations`).
   - When RAM-derived checks are present but server is missing them (e.g., server also restarted), the client **does** resend them.
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
- Boss probe: no false positive edge-detection log on reconnect (probe re-baselines cleanly).

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
- Log format includes absolute address and bit index, for example:
   - `0x02028C14[bit3]`
- No AP location checks are sent from this probe yet.

Use this during boss fights to collect repeatable candidate transitions before
promoting any specific address/bit mapping into production logic.

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
