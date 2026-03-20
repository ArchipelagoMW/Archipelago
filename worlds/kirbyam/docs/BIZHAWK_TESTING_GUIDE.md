# BizHawk Testing Guide for Address Verification

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
