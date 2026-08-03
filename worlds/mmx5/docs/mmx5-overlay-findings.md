> Research notes mirrored from the mmx5-ap-research workspace (2026-08-03).
> Working copies live there and are updated as addresses are confirmed;
> re-sync this mirror when they change. No game data included.

# Mega Man X5 (SLUS-01334) — Overlay / RAM-dump analysis: item grants, stage ids, AP hook plan

Date: 2026-07-30. Companion to `mmx5-ghidra-findings.md` (boot EXE) and
`mmx5-ram-notes.md` (live research). Sources: two full 2MB RAM dumps
(`Scripts\ramdump_stage_f284694.bin` = Izzy Glow gameplay, "G";
`Scripts\ramdump_stage_f174001.bin` = Dark Dizzy results screen, "R").
All addresses are PS1 KSEG0 (`0x80xxxxxx`); BizHawk MainRAM offset = addr − 0x80000000.

Headline discovery that reframes earlier notes: **0x800D1C00 is the engine's
game-state controller object**, passed as `a0` through the mode/state dispatcher
chain. The "save struct" is simply this object's fields. Key header fields:

| Address | Meaning | Evidence / values seen |
|---|---|---|
| 0x800D1C00 | Main game-mode byte (0x0A = in-stage gameplay, 0x0C = results sequence) | G=0x0A, R=0x0C; dispatchers index handler tables by +0/+1/+2 |
| 0x800D1C01 | Sub-mode | results sub-dispatcher 0x800EFF14 (table 0x800F4FF8) |
| 0x800D1C02 | Sub-state | results sub-sub-dispatcher 0x800EFFBC (table 0x800F5024); R=07 |
| 0x800D1C0C | **Active stage id used by the spawn engine** (1..8 mavericks, 0 intro, 9/10 Dynamo?, ~~0x0A-0x0C Zero Space~~ **0x10 = Zero Space 1 — live-read 2026-08-01, the 0x0A-0x0C range was a guess and is WRONG**, 0x0F = transition) | G=06 (Izzy Glow ✓), R=0x0F, ZS1=0x10 ✓ |
| 0x800D1C0D | Active area/section index within stage | G=00 |
| 0x800D1C0F | "boss already beaten" flag for current stage (set from 0x1C4C bit, see §2) | |
| 0x800D1C26 | **Stage id of the just-completed sortie** (results input) | R=02 (Dark Dizzy ✓), G=00 |
| 0x800D1C27 | Sortie result type (0 = maverick defeated → weapon grant path; 1 = special path for stages 9/10; 2 = other) | R=00 |
| 0x800D1C41 | **Selected/current stage id (persistent through the sortie)** | G=06, R=02; matches earlier "02→09 entering Dynamo sortie" |
| 0x800D1C44 | Current character (0 = X, 1 = Zero) | copied to overlay global 0x800F5F7F at results |

Stage id ↔ weapon bit mapping (verified): bit = stageId − 1 in 0x800D1C4C, in
ammo-slot order: 1=Grizzly Slash, 2=Dark Dizzy, 3=Duff McWhalen, 4=Mattrex,
5=Squid Adler, 6=Izzy Glow, 7=Axle the Red, 8=The Skiver.

---

## 1. Mission 1 — Heart-tank pickup handler (and every other pickup)

**All item pickup handling lives in the STATIC EXE** (0x80010000..0x80092000),
not overlay code — it is patchable once at boot and stays patched.

### 1.1 The pickup dispatcher

Item objects (major type 0x21) run main function **0x800543E4**, state
handlers via table 0x8007C234 = {0x800535C8 init, 0x8005388C idle,
0x8005459C, 0x800545BC}. When the player touches the item, the collect
routine (part of the state-2 handler, entry ~0x80054020) dispatches on the
item's **kind** byte (`itemObj+0x82`) through the jump table at **0x80011068**
(14 entries, kind 0..0xD):

| kind | handler | effect |
|---|---|---|
| 0 | 0x800540A0 | **Heart tank** |
| 1 | 0x80054100 | **EX item (Energy Up)** |
| 2/3 | 0x80054164/0x80054198 | life / weapon-energy refill (queued via 0x80053E3C) |
| 4 | 0x800541D8 | full-refill variant |
| 5-7 | 0x80054204 | misc (helper 0x80053B68) |
| 8 | 0x80054218 | 1-Up: `0x800D1C45 += 1`, clamp 9 |
| 9 | 0x80054264 | **Sub-tank**: u16 0x800D1C7E \|= 0x1000 << (id−0x27) → bits 12/13; also sets refill-full flag 0x800D1C76 (X, id 0x27) / 0x800D1C77 (Zero) = 0x80 |
| 0xA | 0x800542D0 | **W-tank**: u16 0x800D1C7E \|= 0x4000 (bit14), clears 0x800D1C78 |
| 0xB | 0x80054310 | **EX-tank (spare lives)**: u16 0x800D1C7E \|= 0x8000 (bit15) |
| 0xC/0xD | 0x80054350/0x8005437C | subtract 4/0x10 from player+0xFB (usage counter) |

Note the tank bitfield is the **u16 at 0x800D1C7E** (so "0x800D1C7F bits 4-7"
in the old notes = u16 bits 12-15; consistent).

### 1.2 Heart handler (kind 0) — disassembly, 0x800540A0

```
800540A0: lui  v0,0x800d ; addiu a2,v0,0x1c00     # a2 = 0x800D1C00
800540AC: lb   v1, 2(s1)                          # v1 = itemObj+0x02 = item id (bit index)
800540B0: lw   a3, 0x80(a2)                       # u32 @0x800D1C80 (hearts/EX word)
800540B4: sllv v1, a0, v1                         # bit = 1 << id      (a0=1)
800540B8: and  v0, a3, v1
800540BC: bnez v0, 0x800543cc                     # already owned -> done (rc=3)
800540CC: or   v0, a3, v1
800540D4: sw   v0, 0x80(a2)                       # commit bit
800540D8: lb   a3, 2(v1=player)                   # charIdx (player 0x8009A0A0 +2)
800540DC: addiu a2, a2, 0x47
800540E4: lbu  v0, (0x800D1C47+charIdx) ; +2 ; sb # max HP += 2 (CURRENT char only)
800540F0: jal  0x80016490 (0, 0x15, 0)            # award jingle/popup
```

EX-item handler (kind 1, 0x80054100) is identical except:
`bit = 0x10000 << (id − 0x10)` (same u32 at 0x1C80) and
`max weapon energy (0x800D1C53 + charIdx) += 2`.

### 1.3 The 0x800D1C80 u32 layout (supersedes byte-wise notes)

| bits | set by | meaning |
|---|---|---|
| 0-7 | pickup kind 0, id 0x00-0x07 | stage heart tanks (one per maverick stage, **id from placement data**) |
| 8-15 | DNA-reward applier (§3.3), reward id 0-7 | "Life Up" DNA rewards (+2 max HP each) |
| 16-23 | pickup kind 1, id 0x10-0x17 | stage EX energy-up items |
| 24-31 | DNA-reward applier, reward id 8-15 | "Energy Up" DNA rewards (+2 max WE). Old note "0x1C83 bit1" = u32 bit 25 ✓ |

### 1.4 Where the heart's bit index comes from — placement records

The id byte (`itemObj+0x02`) is copied verbatim from the stage **placement
record** by the generic layout spawner (EXE):

- Per-record spawner **0x8002B070**, screen-scan callers 0x8002AE50.
- Record list pointer: `list = *(0x80072EAC + stageId*8 + area*4)` with
  stageId = 0x800D1C0C, area = 0x800D1C0D. (Table at **0x80072EAC** is in EXE
  data; per-stage entries are repointed into overlay data at stage load.)
- Record format (8 bytes): `{u8 flags, u8 minor, u8 id, u8 sub, s16 x, s16 y}`;
  list terminates when `sub == 0x0F`. `sub` low nibble = armor-level gate
  (checked vs 0x800D1CA0 low byte by 0x8002AFB4); spawner marks a record
  "spawned" by adding 0x10 to `sub`.
- `minor` selects the object main function from the per-area table pointed to
  by **0x8006FDC4** (Izzy Glow area0: table 0x800F349C). **minor 0x2F = item**
  (entry = 0x800543E4).
- Spawned object gets: +0 = 0x41→(ctor overwrites 0x21), +1 = minor,
  +2 = id, +0xA/+0xE = x/y, **+0x10 = pointer to its placement record**
  (same "item data pointer" concept the MMX4 AP client keys on).

Item id ranges (from ctor 0x800535C8 / dispatcher): 0x00-0x0F heart (bit=id),
0x10-0x1F EX item, 0x20-0x26 consumables (0x21 life, 0x22 large life?, 0x24/25
weapon energy, 0x26 special-gfx variant), 0x27/0x28 sub-tanks, 0x29-0x2A
W-tank/EX-tank, 0x2B/0x2C misc.

### 1.5 Stage → heart-bit table (partial; data-driven, not in code)

| stage | boss | heart bit (u32 0x1C80) | evidence |
|---|---|---|---|
| 1 | Grizzly Slash | bit 0 | harvest 2026-07-31 (rec@800FBE64); also SUB-TANK #1 id=27 @800FBF24 |
| 2 | Dark Dizzy | bit 6 | live capture (prior session); harvest 2026-07-31: **SUB-TANK #2 id=28 @800F3D50 confirmed** (area0; the heart record itself must sit in a later area — not in area0's list) |
| 3 | Duff McWhalen | bit 3 | harvest (rec@80100C50) |
| 4 | Mattrex | bit 7 | harvest (rec@800F4680); its area1 ptr was stale at entry (walker hit 256-cap) |
| 5 | Squid Adler | bit 1 | harvest (rec@80100208) |
| 6 | Izzy Glow | **bit 2** | record @0x800F32FC + LIVE pickup verify 2026-07-31; also EX-TANK id=2A @0x800F3304 |
| 7 | Axle the Red | bit 5 | harvest: unique UNGATED heart rec@800FA7C8 (+11 phantom heart recs ids 0-2 gated armorgate=5 — dummied placements?) + elimination (5 = only bit left) |
| 8 | The Skiver | bit 4 | harvest (rec@800F8D84); also W-TANK id=29 @800F8F0C |

Full harvest log: `Scripts/mmx5_placement_log.txt`. NOTE: only entry-area
(area0) lists were resident during the tour — **no EX items (Energy Ups) found
anywhere**, so they live in later stage areas; harvester upgraded to dump on
area transitions during normal play. Tank map: Sub#1=Grizzly, W=Skiver,
EX=Izzy, Sub#2=TBD (Dizzy suspected).

The mapping is per-record data, NOT stageId−1. **Harvest procedure** (5 min/stage
in BizHawk): enter stage, dump RAM (or Lua-read), read `*(0x80072EAC + stage*8)`
(+4 for area1), walk 8-byte records until `sub==0x0F`, list `minor==0x2F`
entries — heart = id < 0x10, EX = 0x10-0x1F, tanks = 0x27-0x2A. Static intro/
Zero-Space lists are already in the EXE (stage0 @0x80073748, stage10 @0x800739C4,
stage11 @0x80073A8C/0x80073B5C, stage12 @0x80074140 — no hearts there, only
consumables, e.g. stage12 has 8 refill items).

Confidence: **high** for everything except the unharvested 6 heart ids.

---

## 2. Mission 2 — Weapon/boss-beaten grant writer (0x800D1C4C)

### 2.1 The grant function — 0x800EEC0C (results overlay, resident in R dump)

Reached via the results state machine:
`mainmode(0x800D1C00+0=0x0C)` → sub-mode dispatcher 0x800EFF14 (table
0x800F4FF8, indexed by 0x800D1C01) → sub-state dispatcher 0x800EFFBC (table
**0x800F5024**, indexed by 0x800D1C02) → **index 4 = 0x800EEC0C**, called with
`a0 = 0x800D1C00` (the controller object — so `sb 0x4C(s0)` below is 0x800D1C4C).

```
800EEC0C: prologue; s0 = a0 (=0x800D1C00); s1 = 0x800D1C00; s2 = 1
800EEC34: lb   a1, 0x27(s1)          # sortie result type (0x800D1C27)
800EEC3C: beq  a1, 1 -> 0x800EED18   # type 1: stages 9/10 path (0x800D1CCA -= 0x14)
800EEC44: type 0 -> grant; type 2 -> 0x800EED48 (text 0x16 only)
800EEC7C: lb   a0, 0x26(s1)          # stageId just completed (0x800D1C26)
800EEC84: beqz -> done               # 0 = nothing
800EEC8C: if (a0-1) >= 8 -> 0x800EECEC  # non-maverick: popups only, no bit
800EEC9C: lbu  v0, 0x8009A169        # LIVE weapons bitfield
800EECA4: if ((v0 >> (a0-1)) & 1) -> skip (already owned)
800EECB4: a1=5; a2=8                 # popup args
800EECBC: lbu  v0, 0x4C(s0)          # 0x800D1C4C  <-- THE GRANT RMW
800EECC0: sllv v1, s2, v1            # 1 << (stageId-1)
800EECC4: or   v0, v0, v1
800EECC8: jal  0x800F0C00            # spawn "got weapon" popup (type 0x41/0x2D)
800EECCC: sb   v0, 0x4C(s0)          #   (delay slot!) commit 0x800D1C4C
800EECD0: helper(0x8D, 9)            # second popup (Zero-technique banner)
```

- The helper 0x800F0C00 allocates a 0x60-byte popup object from the pool at
  0x800D1F40 (allocator 0x8002D27C) and tags it {0x41, 0x2D, textId}; it never
  touches the save block.
- **One bit serves X weapon + Zero technique + boss-beaten.** No other
  boss-record store was found in either dump.
- The tail of the function (0x800EED60-0x800EEDCC) queues the full results
  text sequence, then checks 0x800D1C26 < 0x0B and 0x800D1C79 < 5 (intro-clear
  counter) for bonus lines.

### 2.2 Readers of 0x800D1C4C (gating)

| reader | where | effect |
|---|---|---|
| 0x80056FDC (read at **0x80057008**) | static EXE | boss-spawn gate: if stage 0x800D1C0C in 1..8 and bit (stage−1) set → set 0x800D1C0F = 1 (boss-already-beaten path; refight/skip handling) — **this is the "does granting the weapon mark the stage beaten" answer: yes, same bit** |
| 0x8001D0BC | static EXE | save-file serialize/compare (file+0x4A ↔ 0x1C4C), see §3.4 |
| stage load | **0x8003C324 / 0x8003D660 / 0x8003D814** (static EXE, three character-init paths) | `lbu 0x4C(ctrl); sb 0xC9(player)` + `lbu 0x4B(ctrl); sb 0x14A(player)` (Ultimate mirror). A char==3 branch zeroes live weapons instead (+ default grants via 0x8003D4C0). CAPTURED 2026-07-31 — the capability-decoupling patch site: change offset 0x4C→0x4D (AP weapons byte 0x800D1C4D, unused + memcard-persisted) at all three |
| stage-select checkmarks / Zero Space unlock | stage-select overlay — live obs 2026-07-31: stage select shows **NO visual beaten indicator** (suppressed Izzy bit produced zero UI change), so no checkmark reader exists to patch. Zero Space unlock logic still unverified (see §6) |
| Enigma/Shuttle **parts screen** | hub overlay — **derived from 0x1C4C, no separate parts store** (proven behaviorally 2026-07-31: suppressed Izzy kill → no Laser Device despite "got part" banner; restore_flaser() alone made it appear after a stage round-trip). Ownership is SNAPSHOTTED at hub entry — mid-hub RAM edits don't refresh the screen until the hub reloads. AP consequence: with vanilla grants suppressed, parts never accrue; the launch check must be patched to read AP part state |

Confidence: grant writer + semantics **high**; stage-select/endgame reads **gap**.

---

## 3. Mission 3 — Other grant writers

### 3.1 Armor capsules — static EXE, 0x80055D58 region

Capsule object grant (function containing 0x80055D58; `s1` = capsule object,
`s1+2` = capsule id):

- id 0-7: **`0x800D1CA1 |= maskTable[id]`** (RMW at 0x80055DB8/0x80055DC8),
  mask table at **0x8007C370**: `01 04 02 08 10 40 20 80`
  → ids 0-3 = Falcon parts (bits 0-3), ids 4-7 = Gaea parts (bits 4-7).
  **Capsule id == part index (live-confirmed 2026-08-01)**: two captures,
  each reading the id off the live capsule object in a stage whose vanilla
  part is known — Tidal Whale (stage byte 3) = **id 1** = Falcon Body, and
  Dark Necrobat (stage byte 2) = **id 4** = Gaea Head. Both match
  `ARMOR_PARTS[i]` = head/body/arm/leg per set, so part *i* is granted by
  capsule *i* and ORs `maskTable[i]`. The table is a PERMUTATION (body and
  arm swap inside each nibble), so `1 << i` is wrong for 4 of the 8 parts —
  client `ARMOR_ITEM_BITS` now derives from the table instead of guessing.
- id 8 (Zero-space capsule): if char == 0 (X) → `0x800D1C4B = 1` (Ultimate
  armor) else `0x800D1C4A |= 0x10` (Black Zero).
- 0x800D1CA0 (low byte) = **armor level 0-3** (also gates placement records via
  0x8002AFB4; value 3 = special). "0x800D1CA0 u16 = armor bitfield" from the
  old notes = level byte + parts byte together.
- **Capsule spawn/despawn gate (disasm 2026-08-01)**: the capsule init state
  (fn 0x80054FE4, s0 = capsule object, id at s0+2) despawns via a3=1 →
  `beq a3,zero,0x80055148` at **0x80055130** (a3≠0 → jal 0x8002D760 =
  delete). For ids 0-7 the despawn ladder (0x80055088-0x8005512C) checks:
  Falcon-complete flag (0x1C4A&2) & maskTable[id]&0x0F, Gaea-complete
  (0x1C4A&4) & maskTable[id]&0xF0, and **part already owned
  (0x1CA1 & maskTable[id], read at 0x80055114)**. Id 8 has its own checks
  (0x1C4B / 0x1C4A&8 / player+0xFA for X; 0x1C4A&0x10 for Zero) — NO
  character gate exists on ids 0-7. The id!=8 split is
  `bne a2,v0,0x80055088` at **0x80055018**; retargeting it to the ladder
  JOIN **0x80055130** (imm 0x1B→0x45, one word — a3 is still 0 from the
  prologue, so the join's `beq a3,zero` always takes the spawn branch)
  makes ids 0-7 always spawn — the AP randomizer's missable-check fix
  (granted parts would otherwise despawn unchecked capsules). Shipped in
  proto v10.
  **⚠ Delay-slot trap (the v9 freeze, live-diagnosed 2026-08-01)**: v9
  retargeted to the spawn path **0x80055148** directly, skipping the join
  beq's delay slot `addiu a0,zero,0x86` (0x80055134) — that word is the
  spawn path's argument to `jal 0x8002B5B4` (0x8005518C). With the object
  pointer left in a0 instead, the game HANGS the moment a capsule object
  spawns (area entry — froze the sunken-ship pit descent in Whale's
  stage). v9 discs are retired; the Lua probe brands them BUGGY.
- **Capsule state machine (live-traced 2026-08-01)**: the capsule object is
  driven by think fn **0x80055450** — `obj+0x2` = id, `obj+0x4` = inited
  flag (0 → run init 0x80054FE4, else dispatch), `obj+0x5` = **state index**
  into the 12-entry handler table **0x8007C380** (0x80055798, 0x8005589C,
  0x80055920, 0x800559A8, 0x800559F4, 0x80055A88, 0x80055AD0, 0x80055B78,
  0x80055C90, 0x80055CEC, **0x80055D24 = grant (index 10)**, 0x80055DEC).
  Key gates:
  - **state 0** (0x80055798): pure PROXIMITY — |player.x − obj.x| < 0x41 and
    a y-band test; no ownership check. This is what opens the capsule while
    the player is still standing *beside* it.
  - **state 5** (0x80055A88): waits on anim-done flag `obj+0x45`.
  - **state 6** (0x80055AD0): waits on **`obj+0x72 & 0x08`** — the box-overlap
    result for collision slot 0 (writer 0x8002EEB4; slots 0/1/2 → +0x72/73/74;
    bit3 = boxes overlap, set from the half-extent compare at 0x8002EE00).
    i.e. **the player must physically OVERLAP the capsule**, not merely stand
    near it. Only then does state 6 spawn the Light hologram (obj type
    0x41/0x24) and set the sequence byte to 1.
  - **sequence byte 0x800AA195** (= global struct 0x800AA0A0 + 0xF5) drives
    the hand-off: state 6 → 1, the 120-frame timer object (0x80055608) → 2,
    the Light hologram (0x800553F0, on its `obj+0x45 == 1`) → **3**;
    **state 8** (0x80055C90) blocks until it reads 3, arms a 0x28 timer,
    state 9 counts it down, **state 10 grants** and writes 4. In practice the
    1/2/3 transitions complete inside a single frame, so a per-frame Lua poll
    of 0x800AA195 typically never observes them.
  - NOTHING in states 0-9 reads 0x1CA1 — ownership cannot stall the machine.
    The only 0x1CA1 access in the whole machine is the grant's own RMW.
- **Armor completion (results overlay 0x800EFC48) — exact condition**:
  `(0x1CA1 & 0x0F) == 0x0F` **AND** `(0x1CCC & 0x0F) != 0x0F` →
  `0x800D1C4A |= 2` (Falcon complete). The second term is an **ack latch**:
  once the ack copy 0x800D1CCC's nibble reaches 0x0F the block is skipped
  forever, so a save carrying a stale 0x0F there will never unlock the
  armor no matter how many results screens run — check/clear 0x1CCC before
  concluding the completion path is broken. 0x800EFC8C repeats it for the
  0xF0 nibble → `|= 4` (Gaea). Each block `jr ra` immediately after setting
  its flag, so **Falcon and Gaea complete on separate results screens**.
  LIVE-VALIDATED 2026-08-01: `/send`ing all 4 Falcon parts drove 0x1CA1
  00→15→17→1F (Falcon nibble 0x0F; the 0x10 was a Gaea Head item received
  from a capsule check), the pause menu showed exactly the parts sent
  (confirming the id==part-index bit mapping visually), and the next
  results screen set `0x1C4A 01 → 03`.

### 3.2 Max HP / max weapon energy

Only two +2 writers exist per stat: heart/EX pickup handlers (§1.2, static EXE,
current char only) and the DNA-reward applier (below, char chosen by
0x800F5F7F). Max HP bytes 0x800D1C47 (X) / 0x800D1C48 (Zero); max WE bytes
0x800D1C53 (X) / 0x800D1C54 (Zero).

### 3.3 DNA-reward applier — results overlay ~0x800EFB40

Grants the pending DNA reward (buffer 0x800D1D38-3A per old notes) by reward id:

- id 0x00-0x0F: `u32 0x800D1C80 |= rewardTable[id].mask` — table at
  **0x800F4ED0** (8 bytes/entry, +4 = mask): ids 0-7 → bits 8-15 (+2 max HP),
  ids 8-15 → bits 24-31 (+2 max WE).
- id 0x10-0x1F: `u32 0x800D1C84 |= rewardTable[id].mask` — **0x800D1C84 is the
  DNA-parts-owned u32** (old "parts bitfields 0x1C84/86" solved). Masks are a
  scrambled per-part permutation (id 0x10→0x20, 0x11→0x20000, 0x12→0x80, ...
  read them from the table when needed).
- Character receiving stat boosts: overlay byte **0x800F5F7F** (copy of
  0x800D1C44 made at results entry, 0x800F0018-24).

### 3.4 Save-file buffer ↔ RAM mapping (memory-card format)

Save-file staging buffer pointer: `*(0x800E81E4)` = **0x80110408** (both dumps).
Loader **0x8001C900** (file→RAM), storer ~0x8001CC5C (RAM→file, mirror),
verifier ~0x8001CF00 (reads both); results overlay also serializes at
**0x800F2980**. Mapping (file offset → RAM):

```
+0x01 -> 0x800D1C79 (intro-clear)     +0x02 -> 0x800D1CA0 (armor level)
+0x03 -> 0x800D1599 (?)               +0x04 -> u32 0x800D1C84 (DNA parts)
+0x08..+0x1F -> 6x u32 0x800D1C88..   +0x20 -> u32 0x800D1C80 (hearts/EX)
+0x24 -> u16 0x800D1C7E (tanks)       +0x26.. -> 16x u16 0x8006FAE4 (ammo)
+0x46/47 -> 0x800D1C47/48 (max HP)    +0x48/49 -> 0x800D1C53/54 (max WE)
+0x4A -> 0x800D1C4C (weapons/bosses)  +0x4B..+0x50 -> 0x800D1C4D.. (6 bytes)
+0x51 -> 0x800D1C4B (Ultimate)        +0x52..+0x57 -> 0x800D1CA3.. (6 bytes)
+0x58 -> 0x800D1C4A (armor flags)     +0x59 -> 0x800D1CA1 (armor parts)
```

Anything the AP client writes into these RAM locations persists to the memory
card through the normal save flow — no extra work needed.

---

## 4. Mission 4 — Free RAM candidates for the AP mailbox

Method: byte ranges zero in BOTH dumps, cross-checked against every
lui/addiu-derived effective address in BOTH dumps (i.e., no code in the EXE,
the gameplay overlay, or the results overlay references them).

| # | range | size | evidence / risk |
|---|---|---|---|
| 1 (primary) | **0x801F8310-0x801FE84F** — recommend mailbox at **0x801FA000** | ~25 KB | Zero in both dumps, zero code refs. Sits between top of used heap (0x801F6000-0x801F8300 buffer, referenced) and the deepest stack byte ever observed (0x801FE850; SP base 0x801FFF00). A mailbox ≤0x1000 bytes at 0x801FA000 leaves >18 KB stack headroom. Risk: extreme stack spikes — none observed. |
| 2 | **0x801C1660-0x801F2FF0** — recommend **0x801E0000** | ~200 KB | Zero in both dumps, zero code refs. Risk: could be a streaming/heap arena used by stages bigger than the two captured; verify with canary before committing. |
| 3 | 0x800CAD40+0x848 and 0x800CCDB0+0x7D8 | 2 KB each | Zero both, no refs; inside the engine BSS belt (0x800Cxxxx), so other overlays may own them. Use only if 1-2 fail. |

Rejected: 0x800D1D60-0x800D1F40 (save-struct tail + 0x800D1DBC map-size global,
then object pool 0x800D1F40-0x800D4F40), 0x800D2837+ (inside object pool),
0x800FDC71+ (overlay data region — other stages load bigger data, stage-3 list
was seen at 0x80100BB0), 0x801F5664 (referenced buffer at 0x801F6000).

Validation recipe: write a 16-byte canary pattern to each candidate, play
through stage load, results, stage select, Dynamo fight, save/load; if canary
survives, the block is safe. (Two dumps cannot prove the negative.)

---

## 5. Overlay geography (for patch planning)

Block-diff of the two dumps (4 KB granularity):

- **0x80010000-0x8006F000: identical** — static EXE code, patch once at boot.
- 0x8006F000-0x80071000, 0x8007D000-0x80082000: EXE data (live variables).
- **0x800EC000-0x800F9000: differs** — the swapped overlay window. Gameplay
  overlay (stage code) and results overlay both load here. The results overlay
  (grant fn 0x800EEC0C, tables 0x800F4ED0/0x800F5000-5090) is only valid while
  0x800D1C00 mode = 0x0C.
- 0x800F9000-0x80105000: same in these two dumps but IS per-stage data in
  general (Izzy Glow's area lists live at 0x800F326C/0x800F9E48); treat
  0x800F1600-0x80105000+ as stage-owned.
- 0x80105000-0x80111000: differs (save buffer 0x80110408 + stage data).
- 0x80157000-0x8016F000, 0x801AC000-0x801AE000: streaming buffers.
- 0x801FE000+: stack.

---

## 6. Patch-hook recommendations (concrete)

### 6.1 Pickup checks (hearts, EX, tanks, 1-ups, refills) — static EXE, best hook

**Hook the jump table at 0x80011068** (data, in the EXE — rewrite entries to
point at AP stubs placed in the mailbox region). Each stub:

1. reads `s1+0x82` (kind), `s1+2` (id), `s1+0x10` (placement-record ptr) and
   `0x800D1C41` (stage) → appends a check-record to the AP log (MMX4-style:
   record pointer or (stage,id) pair uniquely identifies the location);
2. to SUPPRESS the vanilla grant: skip to the common tail `0x800543C8`
   (`li v0,3; sb v0,4(s1)` = "consume item, no effect"), i.e. stub ends with
   `j 0x800543C8`;
3. to KEEP vanilla behavior for un-randomized kinds, `j` to the original
   handler address (table above).

This is robust (single boot-time patch, table-driven, no delay-slot hazards)
and covers every pickup type at once. Minimal alternative if only hearts/EX
matter: NOP the two `sw v0,0x80(a2)` commits (0x800540D4 / 0x80054138) and the
max-stat `sb` at 0x800540F4 / 0x80054158 — but the jump-table redirect is
cleaner and gives the check-record for free.

Item grants FROM the AP client: write the bits/stats directly into
0x800D1C80 (u32), 0x800D1C7E (u16), 0x800D1C45, 0x800D1C47/48, 0x800D1C53/54 —
all engine-honored (max HP/WE take effect immediately; tanks appear in menu).

### 6.2 Boss-kill / weapon checks — two options

- **No-patch detection (recommended for checks):** poll `0x800D1C00 == 0x0C`
  and `0x800D1C27 == 0` and `0x800D1C26 != 0` → boss of stage 0x800D1C26 was
  just defeated. This fires at results entry, ~20 s before the 0x1C4C commit,
  and needs no overlay patch. De-dupe on 0x1C26 per results sequence.
- **Suppressing the vanilla weapon grant (item-randomizer mode):** while the
  results overlay is resident (detect: `u32[0x800EEC0C] == 0x27BDFFD8`), NOP
  the store at **0x800EECCC** (`sb v0,0x4C(s0)`, word 0xA202004C at that
  address — note it sits in the jal delay slot; replacing with NOP is safe,
  the popup call still happens). Re-apply on every results entry because the
  overlay is re-streamed from ROCK_X5.DAT each time.
  **PROVEN LIVE 2026-07-31** (`Scripts/mmx5_ap_patch_proto.lua`, Izzy kill):
  NOP landed ~52 frames after results entry, well before the grant sub-state;
  results screens looked normal (popup shown) and 0x0D1C4C stayed 0x03 through
  the whole sequence. Kill-detect (previous bullet) fired at results entry,
  ~5 s before the commit window. Also observed: mode byte 0x0B = gameplay→
  results interstitial, 0x03→0x04 = stage-select sequence. Mailbox canaries at
  0x801FA000/0x801E0000 survived the full cycle; **savestate loads wipe them**
  (restored RAM predates arming) — client must treat mailbox as
  re-initializable at any time.
  Weapon grants from AP: client ORs bits into 0x800D1C4C (persistent) and
  0x8009A169 (live, if in-stage) — exactly what the game itself does.
- Because 0x1C4C doubles as boss-beaten (stage select, boss-skip gate
  0x80056FDC), an item-randomized "weapon" must be decoupled: leave the
  stage's bit set for progression but zero 0x8009A169's bit... **not
  possible** — same bit. Decoupling requires patching the two readers
  (0x80056FDC EXE; stage-select overlay TBD) or accepting weapon=boss-beaten
  coupling in logic. Flag for design discussion.

### 6.3 Armor capsules — static EXE — LIVE-VALIDATED (proto v10, 2026-08-01)

**FULLY LIVE-VALIDATED 2026-08-01 (recording + suppression):**
- **Recording** — Tidal Whale, capsule id 1: state machine ran 0→11 and the
  stub recorded `PICKUP RECORD #1: stage=3 kind=20 id=01 seq=80`; the client
  consumed it and the server committed the check (smoke.apsave grew).
- **Suppression** — Dark Necrobat, capsule id 4 (mask 0x10), with 0x1CA1
  pre-cleared to 0x00: state 10 ran and recorded
  `PICKUP RECORD #2: stage=2 kind=20 id=04 seq=80`, and **0x1CA1 read back
  0x00** afterwards. The grant fn executed while its vanilla part write did
  not — suppression proven, not merely inert. (The first two attempts were
  inconclusive because the save already owned the bit under test, making the
  vanilla `|=` a no-op; always pre-clear 0x1CA1 for this test.)
- Debug note: the v6 s1-capture ring reads `captured s1 = 00000000` for
  capsule records — the capsule stub doesn't write that pointer. Cosmetic.

**Do not mistake the state-6 overlap gate for a bug** (it cost a full
debugging session): the capsule opens on mere proximity (state 0) but the
sequence only continues once the player physically OVERLAPS it (state 6,
§3.1). Walking up to an open capsule and stopping beside it produces exactly
the "dialog never happens, nothing recorded" signature of a broken hook.

Grant fn: s1 = capsule object, id at s1+2; id==8 splits away at 0x80055D60
(Zero-space capsule, kept vanilla — not a location); ids 0-7 reach the parts
RMW `lbu/or/sb 0xA1(a1)` at **0x80055DB8-0x80055DC8** and rejoin at
**0x80055DCC** (capsule state advance + epilogue — all t-regs dead there).
Shipped design (Scripts/mmx5_build_patch.py `CAPSULE_STUB`):
- RMW head 0x80055DB8/DBC → `j 0x80077700; nop` (free-space run A, after the
  pickup stub). The 19-word stub records {stage 0x1C0C, kind **0x20**
  (synthetic), id, seq|0x80} to the mailbox ring + count, rejoins 0x80055DCC.
  Grant suppressed; dialog/consume animation vanilla; re-records on revisit
  (client de-dupes, maps stage → capsule location).
- Spawn-gate retarget at 0x80055018 → join 0x80055130 (see §3.1, incl. the
  v9 delay-slot freeze this replaces) so AP-granted parts never despawn an
  unchecked capsule.

### 6.4 DNA rewards — results overlay

Applier at ~0x800EFB40 (mask OR at 0x800EFB88 for u32 0x1C80, 0x800EFC30 for
u32 0x1C84). Same reapply-on-results caveat as 6.2. Probably out of scope for
a first randomizer pass (leave vanilla).

---

## 7. Bonus findings

- **Gameplay gate for the client**: 0x800D1C00 mode byte (0x0A gameplay /
  0x0C results) — much better than the disproven 0x800D4F5x gates.
- Enigma/countdown block: written by save-load at 0x8001CAC4-0x8001CADC —
  0x800D1CAA (u8), 0x800D1CAB (u8), **u32 0x800D1CAC** (countdown timer;
  results overlay reads it at 0x800F4844). 0x800D1CAE is the u32's high half —
  "hours" label from cheat archives fits the u32, not a separate u16.
- 0x800D1D0F/0x800D1D10 persisted pair (sorties counter / unknown byte=8,
  read widely: 0x80012990, 0x8002B8A0 RMW 0x8002BCAC, 0x8003E9A0-0x8003FD48).
  0x1D10 semantics unknown (suspect max-sorties / chapter cap).
- 0x800D1CCB: persisted stage-event flag byte; Izzy Glow overlay polls bit0
  constantly (0x800F4330..0x800F4BA4) — likely the stage's light-switch state.
- 0x800D1C88-0x800D1C9F: 6 u32s persisted in the save file (file+0x08) and
  re-serialized at results (0x800F29D0 loop). Zero in both dumps. Best
  hypothesis was per-stage injured-Reploid rescue bitfields — **DISPROVEN
  2026-07-31**: two live Izzy Glow rescues + the following results commit wrote
  nothing here (rescue effect = 0x800D1C45 lives+1 only). No persistent rescue
  record exists; Reploid checks need live spawn-slot detection. What these six
  persisted u32s actually hold is still unknown.
- Zero Space access gating: NOT found — neither dump has the stage-select
  overlay resident. (Sorties counter 0x800D1D0F and countdown u32 0x1CAC are
  the candidates its logic would read.)

## 8. Not found / next steps

1. **Remaining 6 heart-tank ids** — harvest per stage with the §1.5 procedure
   (one visit per stage, no boss kill needed), or break ROCK_X5.DAT
   compression. Same harvest yields EX-item and tank ids per stage.
2. **Stage-select overlay** (boss-beaten checkmarks, Zero Space unlock,
   Enigma/shuttle menus): capture a RAM dump at the stage-select screen and
   repeat the §2.2 reader scan for 0x1C4C / 0x1D0F / 0x1CAC.
3. ~~**Reploid rescue**: rescue one reploid in Izzy Glow, diff 0x800D1C88-9F
   (and 0x800D1CC4..) before/after~~ — DONE 2026-07-31, no save-struct write
   (see §7). Remaining: find the LIVE spawn-slot state for rescue detection.
4. **Free-RAM canary validation** across a full session (§4).
5. **Dynamo/Zero-space results path** (0x800D1C27==1, stages 9/10, the
   `0x800D1CCA -= 0x14` branch) — semantics unknown.
6. Decision needed on weapon/boss-beaten coupling (§6.2, third bullet).

## 9. CD streaming / overlay loader (static-EXE + disc analysis 2026-07-31)

### 9.0 HEADLINE: code overlays are NOT compressed — patch the disc directly

The recomp project's "ROCK_X5.DAT overlays are compressed" premise is WRONG
for the code overlays (it may hold for graphics chunks in the DAT). Proven by
needle-search of live RAM bytes against the raw disc image:

- Results-overlay grant fn (RAM 0x800EEC0C) found RAW at disc offset
  0x35FF564; the grant store word 0xA202004C verified byte-exact at disc
  offset **0x35FF624** (= the 0x800EECCC NOP target). Reward table
  0x800F4ED0 found raw too. Izzy gameplay overlay code also found raw.
- The code overlays live in **ROCK_X5.BIN** (ISO extent: LBA 23693, size
  1,384,448 = 676 sectors), NOT the DAT. Results module starts at .bin
  sector 24073 (BIN-relative sector 380, file offset 0xBE000) and loads to
  **0x800EE970 — exactly the dest pointer in the EXE descriptor at
  0x80010000**. Grant fn = module offset +0x29C. Izzy gameplay module at
  .bin sector 23915 (BIN-rel 222).
- Disc sectors are Mode2 Form1 (subheader 00 00 08 00).
  **EDC/ECC regeneration is REQUIRED for every modified sector** — proven
  live 2026-07-31: with only the data bytes changed, BizHawk/NymaShock
  served the ORIGINAL word (the RSPC parity still described the old data
  and the disc layer error-corrected the 4-byte edit away). After
  regenerating EDC+P/Q for the sector (`Scripts/psx_ecc.py`, Corlett-style
  tables, self-tested byte-identical on 7 untouched sectors), the patched
  word streamed correctly. (Implication for the MMX4 precedent: their
  basepatch must carry valid parity too; "no EDC handling in Rom.py" just
  means their xdelta was built from a parity-correct image.)

**A1 persistence is therefore solved with no loader hook**: overlay patches
= direct byte edits in ROCK_X5.BIN's extent; EXE patches = direct edits in
SLUS_013.34's extent (LBA 23432); regenerate per-sector EDC/ECC; ship as
whole-image xdelta. **VALIDATED LIVE 2026-07-31**: prototype disc
(`Games\MegamanX5-AP-proto\`, one NOP at 0x35FF624 + parity regen) streams
0x00000000 at 0x800EECCC during results on an unmodified emulator with no
scripts. BizHawk quirk: SaveRAM (memcard) is keyed to the game name — clone
`PSX\SaveRAM\Megaman X5.SaveRAM` to the patched game's name (done for
AP-proto).

ISO map (root dir): SYSTEM.CNF LBA 25, ROCK_X5.DAT LBA 26 (47,935,488 B),
SLUS_013.34 LBA 23432 (534,528 B), ROCK_X5.BIN LBA 23693, ZNULL.DAT LBA
229617. Full DAT TOC dumped to `Scripts/mmx5_dat_toc.txt` (172 entries;
RAM TOC LBAs are absolute .bin sectors, base 26 added at boot; TOC entries
end at 23432 = SLUS start, confirming DAT ≠ overlay source).

### 9.1 Loader internals (for reference; no longer needed for A1)

Original goal: find the "overlay just finished streaming in" moment in the
STATIC EXE for a fixup hook — superseded by §9.0 direct disc patching, but
the streaming architecture below is still useful (e.g., for identifying
module ids and any future runtime needs).

Found so far (all static EXE, boot-time patchable):

- **DAT descriptor block at 0x80010000**: {ptr 0x800EE970, "\ROCK_X5.DAT;1"}
  then {ptr?, "\ROCK_X5.BIN;1"} at +0x10 (this is what the client's EXE
  signature check reads). 0x800EE970 also referenced by the boot function
  (entry 0x8005894C region, refs at 0x80058958/0x800589A0).
- **Boot-time DAT indexer = 0x80013EE8**: CdSearchFile(sp buf, 0x80010004)
  via wrapper 0x80063d08 (retry loop), LBA extract via 0x80063c88
  (CdPosToInt-ish), reads the DAT's first sector into 0x80105000, then
  builds the **file TOC at 0x800E5C08: 172 (0xAC) entries of
  {u32 absolute LBA (= DAT base + relative), u32 size}**. Entries
  0xAC-0xAE are appended by CdSearchFile on 22-byte-stride filename table
  at 0x8006F3FC (separate files, STR/XA presumably).
- **Streaming state machine** spanning ~0x80014574-0x80015Cxx (EXE):
  TOC-indexed request setup at 0x800148E4 (id*8 into TOC; size →
  0x800E5A18, LBA → 0x800E5A24, kick flag 0x800E5A30 = 1) and at
  0x8001569C (same globals, then jal 0x80014574 = read-start). Request/
  state globals cluster: 0x800E5BE0/5BE4 (queued params), 0x800E5BE9/5BEA
  (queued ids), 0x800E5BEC, 0x800E5BF0 (retry/timeout counter, limit
  0x259), 0x800E5A40. CD wrappers: 0x80066db8/0x80066d98/0x80066bc8/
  0x80066ce8 (CdControl-family), 0x800679e8 (read), 0x80067028 (sync/
  result poll, bit 0x40 = busy).

Still to find (next Ghidra session):
1. The **decompressor call** and the per-overlay **destination address
   source** (no code forms 0x800EC000 as a static constant — dest comes
   from data, likely per-file dest table or the 0x80010000-style
   descriptors; 0x800EE970 is dest-shaped and sits inside the window).
2. The **completion dispatch** — the state-machine slot that runs when a
   stream-in finishes. That is THE hook site: swap its handler pointer (or
   insert a jal) to an AP stub in the mailbox that walks a fixup table
   (overlay id → list of {addr, orig word, new word}) before returning to
   the engine. One EXE patch then services every overlay patch we'll ever
   need, compression never matters.
3. Cross-check which TOC id = results overlay (kill a boss while logging
   0x800E5BE9/0x800E5A24 with Lua — cheap runtime assist).

## 10. Hub overlay analysis (dumps `ramdump_hub_f22905` / `ramdump_partsmenu_f23591`, 2026-07-31)

One hub module serves stage select AND the Enigma/parts screens (window
0x800EC000-0x800F9000 near-identical between the two dumps; entirely
different from the results module). Hub code addresses the save struct via
the controller pointer (reg = 0x800D1C00, field offsets), not absolute EAs.

- **Parts-screen derivation readers** (the §2.2 behavioral proof, now in
  code): two sites — per display slot s, bit = table[s] from
  **0x800F5194 = [0,4,5,2,7,6,1,3]**, test `(0x800D1C4C >> bit) & 1`,
  draw part (param tables 0x800F5108/0x800F50B0) else empty frame
  (0x800F5058). Loads at 0x800EF440 / 0x800F0B78.
  The table IS the canonical part-holder map: slots 0-3 = Enigma page =
  bits {0,4,5,2} = Grizzly/Adler/Izzy/McWhalen (mask 0x35); slots 4-7 =
  Shuttle page = bits {7,6,1,3} = Skiver/Axle/Dizzy/Mattrex (mask 0xCA).
  AP patch: repoint the two `lbu 0x4C(base)` loads at the mailbox parts
  byte (or table-swap) — small, local, data-driven.
- **Countdown decoded**: u32 0x800D1CAC counts FRAMES; hour = 0x34BC0
  (216,000 = 60 fps × 3600). Hourly-tick handler at 0x800EFF04-2C
  (countdown −= hour when flag +0x27 clear, byte +0x02 += 1); an
  hour-RESTORE site at 0x800F01D8-EC (countdown += hour, resets related
  state) — candidate Dynamo/event hour-give-back. ("Hours left" display =
  derived; cheat-archive 0x1CAE = high half of this u32.)
- **Story-chapter gating found (design-critical)**: function 0x800EEF14
  reads chapter byte **0x800D1D0F** and advances it on POPCOUNTS of
  0x800D1C4C — 2 kills → chapter 2 (sub-mode 0xC event; Enigma), 6 kills →
  chapter 4 (sub-mode 0xE; shuttle). More chapter dispatch at 0x800F22C0+
  (values 2/8/9, also reads 0x1C79). **Consequence: shipping the
  weapon-grant NOP would freeze the popcount → story never advances →
  endgame softlock. The final patch must KEEP the vanilla 0x1C4C commit
  (as the game-written check-record, MMX4-style) and decouple the
  CAPABILITY readers instead** (stage-load 0x9A169 repopulation, parts
  display, launch check). The 0x800EECCC NOP stays a research tool only.
- **Launch flow**: prompt runs in the hub module (dumps `launch` =
  hub code + data deltas); confirming streams a cutscene module into
  0x800EC000-0x800F3000 and sets mode 0x14, stage id 0x0B,
  **0x800D1C1D = 4** (launch-event state byte, new). Outcome/chapter
  commit happens later in the cutscene (dump was mid-scene; state
  rewound via savestate — outcome roll site still unlocated; the two
  andi-0xF sites in the cutscene module are sprite frame math, and no
  standard LCG constant exists anywhere in RAM). NEXT: DuckStation
  debugger session — watchpoints on 0x800D1C1D/0x800D1D0F writes and
  0x800D1C4C reads during a launch catch the resolution function
  directly. (Speedrun lore "roll locks at results screens" hints the
  entropy source is a frame/countdown-derived value, possibly the 0x1CAC
  frame countdown itself — check what the resolution fn reads.)

## 11. LAUNCH RESOLUTION FUNCTION — fully decoded (DuckStation session 2026-07-31)

Caught live via write-watchpoint on 0x800D1C1D → read-watchpoint on
0x800D1C4C during an Enigma launch; code captured in `enigmaRAM.bin`
(workspace root; mid-cutscene dump). Function at **RAM 0x800FA000 region**
(launch cutscene module), ON DISC exactly once: **sector 24319** (ROCK_X5.BIN
tail). Mapping CORRECTED by disc scan 2026-08-01: RAM 0x800FA000 = sector
24319 **user-data offset 0** (raw = 24319×2352 + 24 + (addr − 0x800FA000));
the andi word sits at user offset 0xD4 = RAM 0x800FA0D4 exactly. The old
"+208" note here was wrong. Note: `jal 0x8002DF78` + `andi v1,v0,0xF`
appears at 8 disc sites total (RNG masking is a common idiom) — the launch
resolution copy is the sector-24319 one; the others are other modules.

Decode (fn body ~0x800FA020-0x800FA17C in enigmaRAM.bin):
1. **Score** `s0 = 2 × (sum of s8 bytes 0x800D1CC2..0x1CC5) + s8 0x800D1CCA`
   — the "unidentified results-screen counters" are LAUNCH-POWER
   ACCUMULATORS; 0x1CCA is the modifier Dynamo-sortie results adjust by
   0x14 (§2.1 type-1 path).
2. **Countdown bonus**: adds hours to u32 0x1CAC by score band:
   ≥0x51→4h, ≥0x3D→3h, ≥0x29→2h, >0→1h, ≤0→0. (0x34BC0 frames/hour.)
   Also sets 0x800D1CCB = 1 ("launch attempted"), zeroes 0x1CCA.
3. **The roll**: `jal 0x8002DF78` — **the game's RNG lives in the STATIC
   EXE at 0x8002DF78** — then `roll = (rand >> 2) & 0xF`. Success:
   | score | needs | rate |
   |---|---|---|
   | ≤0 | — | 0% |
   | 0x01-0x14 | roll==0 | 6.25% |
   | 0x15-0x28 | roll<2 | 12.5% |
   | 0x29-0x3C | roll<6 | 37.5% |
   | 0x3D-0x50 | roll<12 | 75% |
   | ≥0x51 | roll<15 | 93.75% (undocumented top band) |
   Community Enigma/shuttle numbers reproduce exactly (Enigma's vanilla
   score evidently never exceeds 0x28).
4. **On success**: `0x800D1C79 = 5` — 0x1C79 is NOT just intro-clear, it's
   the **story ACT counter** (5 = Eurasia destroyed; explains the results
   tail's `0x1C79 < 5` check) — and `0x800D1CCB |= 0x80` (success flag;
   failure leaves 0x01). Failure path = story pivots to the shuttle.

**AP determinism patch**: replace the single word `andi v1,v0,0xF` (RAM
0x800FA0D4, disc sector 24319) with `li v1,0` → success ⇔ score > 0, RNG
irrelevant (jal stays, harmless). Score bytes 0x1CC2-0x1CC5/0x1CCA then
become AP-controlled (client writes from part-item state; vanilla accrual
suppressed or ignored). Single on-disc copy ⇒ Enigma + shuttle likely share
the fn — verify the shuttle path's feeder before shipping.

Community-lore reconciliation (2026-07-31): the known "rand%64 <
4/8/24/48 by parts count" description is the SAME math (x/64 = our
x/4 per 16) seen from outside — parts drive the score via the feeder, so
parts-count is the observable proxy. The known "modifiers" map exactly:
Dynamo handling = the 0x1CCA additive term; "virus infections force
shuttle failure" = something dragging score ≤ 0 into the always-fail
band. Under AP (client owns the score bytes + li v1,0 roll patch) all
vanilla modifiers become irrelevant, and score ≤ 0 doubles as the launch
GATE: no required AP parts → score 0 → guaranteed clean failure through
the game's own logic. Ensure client writes score bytes at launch time
(or patch suppresses vanilla accrual) so Dynamo/virus adjustments can't
interleave.

Live observations still to fold in: the parts-count feeder (read of 0x1C4C
masked 0xCA seen at a re-streamed 0x800FA0C4-phase during the cutscene —
different module phase than the dump; find its disc home when needed).

## Tooling added this session (scratchpad)

`scan_save.py` (register-tracking EA scanner for RAM dumps), `scan_rmw.py`
(same-offset load/store pair finder), `disasm_dump.py` (capstone disasm at
0x80000000 base), plus scan outputs `scan_gameplay.txt` / `scan_results.txt`.
