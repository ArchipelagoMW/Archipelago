# Kirby & The Amazing Mirror - Address Verification Matrix

**Status**: POC Verification in Progress  
**Target ROM**: Kirby & The Amazing Mirror (USA)  
**Verification Date**: March 2026  
**Verified By**: (your name here)

Policy references:
- `worlds/kirbyam/docs/notes.md`
- `worlds/kirbyam/data/native_address_policy.json`

## Mission

Systematically verify all memory addresses needed for the POC:
- **8 Mirror Shards** (location checks)
- **9 Major Chests** (area big-chest checks, bits 1–9)
- **7 Area Bosses** (dungeon defeats)
- **1 Final Boss** (Dark Mind defeat)

This document serves as a testing checklist. Use BizHawk's memory viewer to confirm each address as you collect items in-game.

---

## Testing Protocol

### Setup
1. Open ROM in BizHawk: `d:\kirbyam-extras\ROMs\Kirby & The Amazing Mirror (USA).gba`
2. Open Memory Viewer (Tools → Memory Viewer)
3. Search memory using "Search" tool for candidate values, or manually enter addresses into the viewer

### For Each Signal
1. **Before Action**: Record RAM value at address (use Ctrl+C to copy hex)
2. **Perform Action**: Collect shard / defeat boss in-game
3. **After Action**: Check RAM value changed and record new value
4. **Repeat** multiple times to confirm consistency
5. **Mark Status**: ✅ Verified / ⚠️ Needs Refinement / ❌ Rejected

### Confidence Levels
- 🟢 **High** (4-5 confirmations, bit-to-bit correlation): Ready for use
- 🟡 **Medium** (2-3 confirmations, timing issues): Acceptable with notes
- 🔴 **Low** (1 confirmation, inconsistent): Needs more testing

---

## 1. MIRROR SHARDS (8 Total)

### Candidate Address: `0x02038970` (Shard Bitfield)
- **Type**: 32-bit bitfield (bits 0-7 = shards 1-8)
- **Source**: Workbook + ROM cheat codes
- **Expected Behavior**: 
  - Bit flips from 0→1 when shard collected
  - Persists after room change
  - No change on death/reset

| Shard | Bit | Status | Verified Address | Notes |
|-------|-----|--------|------------------|-------|
| 1 | 0 | ⬜ | | |
| 2 | 1 | ⬜ | | |
| 3 | 2 | ⬜ | | |
| 4 | 3 | ⬜ | | |
| 5 | 4 | ⬜ | | |
| 6 | 5 | ⬜ | | |
| 7 | 6 | ⬜ | | |
| 8 | 7 | ⬜ | | |

**Testing Steps for Each Shard**:
1. Collect shard in-game
2. Check bitfield for new bit set
3. Save and reset; verify bit persists
4. Mark status and confidence

---

## 2. MAJOR CHESTS (Phase 1)

### Candidate Address: `0x0203897C` (Big Chest Area Bitfield)
- **Type**: 32-bit bitfield (bit N = `AreaId` N)
- **Source**: `gTreasures.bigChestField` derived from the `shard_bitfield_native` anchor
- **Expected Behavior**:
  - Bit flips from `0→1` when the area's major chest reward is claimed
  - Persists after room change and save/reload
  - The client polls all defined MAJOR_CHEST bits dynamically; currently `1`–`9` (all playable areas)

| Location | Bit | Status | Verified Address | Notes |
|----------|-----|--------|------------------|-------|
| Rainbow Route - Big Chest | 1 | ⬜ | | |
| Moonlight Mansion - Big Chest | 2 | ⬜ | | |
| Cabbage Cavern - Big Chest | 3 | ⬜ | | |
| Mustard Mountain - Big Chest | 4 | ⬜ | | |
| Carrot Castle - Big Chest | 5 | ⬜ | | |
| Olive Ocean - Big Chest | 6 | ⬜ | | |
| Peppermint Palace - Big Chest | 7 | ⬜ | | |
| Radish Ruins - Big Chest | 8 | ⬜ | | |
| Candy Constellation - Big Chest | 9 | ⬜ | | |

**Testing Steps for Each Major Chest**:
1. Observe `0x0203897C` before opening the chest
2. Claim the chest reward in-game
3. Confirm the mapped area bit flips to `1`
4. Reconnect the AP client and confirm the corresponding LocationCheck is not replayed after server acknowledgement
5. Save and reset; verify the bit persists

---

## 3. AREA BOSSES (7 Total by Mirror)

> **NOTE**: In KAtAM, each mirror has a boss. Start with Moonlight Mansion (Crepe).

### Moonlight Mansion Boss: **Crepe**
- **Candidate Address**: TBD (search from workbook)
- **Expected Behavior**: Flag value changes when Crepe defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low
- **Testing Notes**: 

| Phase | Step | Expected | Observed | ✅ |
|-------|------|----------|----------|---|
| Before | Check RAM value | (record hex) | | |
| Fight | Engage Crepe | N/A | N/A | |
| Defeat | Deal final hit | N/A | N/A | |
| After | Check RAM value | Changed | | |
| Reset | Load save | Value persists | | |

---

### Cabbage Cavern Boss: **Kracko**
- **Candidate Address**: TBD
- **Expected Behavior**: Flag value changes when Kracko defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low

---

### Mustard Mountain Boss: **King Dedede**
- **Candidate Address**: TBD
- **Expected Behavior**: Flag value changes when King Dedede defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low

---

### Olive Ocean Boss: **Meta Knight**
- **Candidate Address**: TBD
- **Expected Behavior**: Flag value changes when Meta Knight defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low

---

### Peppermint Palace Boss: **Pon & Con**
- **Candidate Address**: TBD
- **Expected Behavior**: Flag value changes when Pon & Con defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low

---

### Frosting Fields Boss: **Psycho Robot (Redundant Robot)**
- **Candidate Address**: TBD
- **Expected Behavior**: Flag value changes when Psycho Robot defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low

---

### Rainbow Route Boss: **Dangerous Dedede**
- **Candidate Address**: TBD
- **Expected Behavior**: Flag value changes when Dangerous Dedede defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low

---

## 4. FINAL BOSS: DARK MIND

### Dark Meta Knight (Dimension Mirror Encounter)
- **Candidate Address**: TBD — no dedicated flag mapped yet; presence inferred from
  `boss_mirror_table_native` probe region (`0x02028C14+`). Distinct from the
  Radish Ruins disguise fight (covered separately under Issue #43).
- **Object ID**: `OBJ_DARK_META_KNIGHT = 0x4E` (same type used for disguise fight;
  the Dimension Mirror encounter is differentiated by map/room context).
- **Expected Behavior**: A flag or bit in the boss table should set when the
  Dimension Mirror Dark Meta Knight fight is completed — distinct from the Radish
  Ruins occurrence. Must be verified against both encounters.
- **AP Role**: This is a required event in `REGION_DIMENSION_MIRROR/MAIN`. The
  `Defeat Dark Mind` goal location is gated behind this event.
- **Status**: ⬜ Not Started — candidate address unresolved; awaiting live BizHawk
  mapping during the Dimension Mirror sequence.
- **Verified Address**: 
- **Confidence**: 🔴 Low
- **Testing Notes**: Trigger the DMK fight via Dimension Mirror (after collecting
  all 8 shards), not the Radish Ruins route. Record pre/post boss-table bytes.

| Phase | Step | Expected | Observed | ✅ |
|-------|------|----------|----------|---|
| Before | Check boss table bytes at `0x02028C14+` | (record hex) | | |
| Engage | Enter Dimension Mirror, find DMK room | N/A | N/A | |
| Defeat | Deal final hit to Dark Meta Knight | N/A | N/A | |
| After | Check boss table for new bit set | Changed bit | | |
| Reset | Load save | Value persists | | |

---

### Dark Mind (All Forms as a Unit)
- **Candidate Address**: `ai_kirby_state_native` at `0x0203AD2C` (u32) —
  `integrated` status; value `9999` fires on Dark Mind clear trigger.
- **Object IDs (from katam decomp)**:
  - `OBJ_DARK_MIND_FORM_1 = 0x4F`
  - `OBJ_DARK_MIND_FORM_2 = 0x50`
  - `OBJ_DARK_MIND_FORM_3_TRIGGER = 0x51`
- **Expected Behavior**: `ai_kirby_state_native` transitions to `9999` after all
  three Dark Mind forms are defeated. The native signal fires once per playthrough
  per save slot (not per form individually). Note: `10000` is the subsequent
  100%-completion progression signal and must NOT be used as a Dark Mind trigger.
- **AP Role**: The `Defeat Dark Mind` goal location fires on the `9999` native
  signal. The goal is in `REGION_DIMENSION_MIRROR/MAIN`, requires all 8 shards,
  and additionally requires the Dark Meta Knight (Dimension Mirror) event.
- **Status**: ⬜ Integrated (pending live verification) — currently used in
  production client for Dark Mind goal detection. Promotion to `verified`
  requires 3+ BizHawk observations with pre/post capture and persistence check.
- **Verified Address**: `0x0203AD2C` (integrated; unverified)
- **Confidence**: 🟡 Medium (integrated from protocol reverse-engineering; no
  confirmed live captures on record)
- **Testing Notes**: Observe `ai_kirby_state_native` in BizHawk before entering
  the final boss sequence, during each form, and after the final hit. Confirm
  value reaches `9999` and stays there through a save/reload cycle.

| Phase | Step | Expected ai_state | Observed | ✅ |
|-------|------|-------------------|----------|---|
| Before Dark Mind | Check `0x0203AD2C` | Not 9999 | | |
| Form 1 defeat | Beat Dark Mind Form 1 | Not 9999 yet | | |
| Form 2 defeat | Beat Dark Mind Form 2 | Not 9999 yet | | |
| Form 3 defeat | Beat Dark Mind Form 3 | `9999` | | |
| Post-clear | Continue post-clear | `10000` (100% signal) | | |
| Reload | Load save | `9999` persists | | |

---

## 5. CANDIDATE ADDRESS SOURCES

### From Workbook (KirbyAM Data.xlsx)
| Signal | Workbook Address | Status | Notes |
|--------|------------------|--------|-------|
| Mirror Shards Bitfield | `0x02038970` | Integrated (pending live verification) | Tracked in `addresses.json` as `shard_bitfield_native` |
| Major Chest Bitfield | `0x0203897C` | Integrated (pending live verification) | Tracked in `addresses.json` as `big_chest_bitfield_native`; Phase 1 polls bits 3, 6, 7 |
| Chest/Switch Blocks | `0x02038960`–`0x0203896A` | TBD | Supporting data |
| Boss/Mirror table region | `0x02028C14+` | Candidate | Candidate source from protocol reverse-engineering; needs live confirmation |
| Dark Mind signal | `0x02028C14+` (offset TBD) | Candidate | Needs live mapping and confirmation |

### From Cheat Codes
- See [Kirby _ the Amazing Mirror (USA, Europe) (Code Breaker).cht](file:///d:/kirbyam-extras/) for additional addresses

---

## 6. VERIFICATION CHECKLIST

- [x] At least one shard progression address is integrated for current POC path (`0x02038970`)
- [x] At least one major chest address is integrated for current POC path (`0x0203897C`)
- [x] At least one dungeon boss signal candidate is documented (`0x02028C14+` region)
- [x] At least one final boss signal candidate is documented (`0x02028C14+` region, offset TBD)
- [ ] Live verification complete for major chest candidate(s)
- [ ] Live verification complete for dungeon boss candidate(s)
- [ ] Live verification complete for final boss candidate(s)
- [ ] Address conflicts checked (no overlaps)
- [ ] Bit/flag transitions documented
- [ ] All addresses tested multiple times for consistency
- [ ] Document updated with verified addresses
- [ ] Ready for ROM payload implementation

---

## 7. NOTES & OBSERVATIONS

(To be filled in during testing)

---

## 8. SUMMARY TABLE (For Documentation)

*To be completed once all verifications done*

| Signal | Type | Address | Bit | Confidence | Status |
|--------|------|---------|-----|------------|--------|
| Mirror Shard 1 | Bitfield | TBD | 0 | 🔴 | ⬜ |
| Cabbage Cavern - Big Chest | Bitfield | `0x0203897C` | 3 | 🟡 | Integrated |
| Crepe Defeated | Flag/Bitfield | TBD | ? | 🔴 | ⬜ |
| Dark Meta Knight (Dimension Mirror) | Flag/Bitfield | TBD (boss table `0x02028C14+`) | ? | 🔴 | ⬜ |
| Dark Mind Defeated (all forms) | ai_kirby_state | `0x0203AD2C` → `9999` | n/a | 🟡 | Integrated |
| 100% Completion Signal | ai_kirby_state | `0x0203AD2C` → `10000` | n/a | 🟡 | Integrated |
| ... | ... | ... | ... | ... | ... |

---

## 8. REFERENCES

- **Issue #136**: POC Address Verification Matrix (this issue)
- **Issue #135**: Address Verification Policy
- **Workbook**: `d:\kirbyam-extras\KirbyAM Data.xlsx`
- **Cheat Codes**: `d:\kirbyam-extras\Kirby _ the Amazing Mirror (USA, Europe) (Code Breaker).cht`
- **ROM**: `d:\kirbyam-extras\ROMs\Kirby & The Amazing Mirror (USA).gba`
