# Kirby & The Amazing Mirror - Address Verification Matrix

**Status**: POC Verification in Progress  
**Target ROM**: Kirby & The Amazing Mirror (USA)  
**Verification Date**: March 2026  
**Verified By**: (your name here)

## Mission

Systematically verify all memory addresses needed for the POC:
- **8 Mirror Shards** (location checks)
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

## 2. AREA BOSSES (7 Total by Mirror)

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

## 3. FINAL BOSS: DARK MIND

### Dark Mind Defeat Flag
- **Candidate Address**: TBD
- **Expected Behavior**: Flag value / bitfield changes when Dark Mind defeated
- **Status**: ⬜ Not Started
- **Verified Address**: 
- **Confidence**: 🔴 Low
- **Testing Notes**: Should only be set after final boss defeated in final area.

---

## 4. CANDIDATE ADDRESS SOURCES

### From Workbook (KirbyAM Data.xlsx)
| Signal | Workbook Address | Status | Notes |
|--------|------------------|--------|-------|
| Mirror Shards Bitfield | `0x02038970` | Candidate | Needs verification |
| Chest/Switch Blocks | `0x02038960`–`0x0203896A` | TBD | Supporting data |
| TBD (Boss defeats) | TBD | Candidate | Extract from workbook |

### From Cheat Codes
- See [Kirby _ the Amazing Mirror (USA, Europe) (Code Breaker).cht](file:///d:/kirbyam-extras/) for additional addresses

---

## 5. VERIFICATION CHECKLIST

- [ ] All 8 shards mapped and verified
- [ ] All 7 area bosses mapped at least to candidate stage
- [ ] Crepe (Moonlight Mansion) boss address verified ✅ Required first
- [ ] Dark Mind final boss address verified
- [ ] Address conflicts checked (no overlaps)
- [ ] Bit/flag transitions documented
- [ ] All addresses tested multiple times for consistency
- [ ] Document updated with verified addresses
- [ ] Ready for ROM payload implementation

---

## 6. NOTES & OBSERVATIONS

(To be filled in during testing)

---

## 7. SUMMARY TABLE (For Documentation)

*To be completed once all verifications done*

| Signal | Type | Address | Bit | Confidence | Status |
|--------|------|---------|-----|------------|--------|
| Mirror Shard 1 | Bitfield | TBD | 0 | 🔴 | ⬜ |
| Crepe Defeated | Flag/Bitfield | TBD | ? | 🔴 | ⬜ |
| Dark Mind Defeated | Flag/Bitfield | TBD | ? | 🔴 | ⬜ |
| ... | ... | ... | ... | ... | ... |

---

## 8. REFERENCES

- **Issue #136**: POC Address Verification Matrix (this issue)
- **Issue #135**: Address Verification Policy
- **Workbook**: `d:\kirbyam-extras\KirbyAM Data.xlsx`
- **Cheat Codes**: `d:\kirbyam-extras\Kirby _ the Amazing Mirror (USA, Europe) (Code Breaker).cht`
- **ROM**: `d:\kirbyam-extras\ROMs\Kirby & The Amazing Mirror (USA).gba`
