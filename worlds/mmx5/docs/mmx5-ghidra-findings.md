> Research notes mirrored from the mmx5-ap-research workspace (2026-08-08).
> Working copies live there and are updated as addresses are confirmed;
> re-sync this mirror when they change. No game data included.

# Mega Man X5 (SLUS-01334, NTSC-U) — Ghidra static analysis: player HP / damage structures

Date: 2026-07-30. Companion to `mmx5-ram-notes.md` (live BizHawk research).
All analysis was done on the boot EXE extracted from the verified Redump .bin;
disassembly addresses are PS1 KSEG0 virtual addresses.

---

## 1. Extraction results

Extracted from `Games\MegamanX5\Megaman X5.bin` (MODE2/2352, user data = bytes
24..2071 per sector, ISO9660 parsed from LBA 16 PVD). Files saved under the
session scratchpad `...\scratchpad\extracted\`:

| File | LBA | Size | Notes |
|---|---|---|---|
| `SLUS_013.34` | 23432 | 534,528 | Boot EXE. PS-EXE header: `pc0=0x8005894C`, `t_addr=0x80010000`, `t_size=0x82000`, `sp=0x801FFFF0` |
| `ROCK_X5.BIN` | 23693 | 1,384,448 | Overlay/loader payload; starts with a (sector, byte-size) pair table |
| `ROCK_X5.DAT` | 26 | 47,935,488 | Main streamed data; header = table of `(u32 sector_offset, u32 byte_size)` pairs (~172 entries read before terminator; first: (1, 0x6000), then a long run of 0x4800-byte chunks) |
| `SYSTEM.CNF` | 25 | 68 | BOOT=SLUS_013.34, STACK=801FFF00 |
| Others (not extracted) | | | `STR/CAPLOGO.STR`, `STR/X5OP.STR` (FMV), `XA/BGM.XA` (audio), `ZNULL.DAT` |

A headerless copy `SLUS_013.34_no_header.bin` (532,480 bytes, file offset 0 =
0x80010000) was imported into Ghidra (`MIPS:LE:32:default`, project
`scratchpad\MMX5.gpr`) and auto-analyzed.

## 2. Overlay knowledge from MegaManX5Recomp

- The recomp project (`MegaManX5Recomp\DISC.md`, `ghidra\instructions.txt`,
  `game.toml`) documents the layout: static EXE spans **0x80010000..0x80092000**
  (text 0x82000); everything above that in RAM (0x80092000+, including our
  targets at 0x8009xxxx/0x800Dxxxx which are BSS, and overlay *code* around
  0x800F0000+ per the lava cheat patches) is either BSS or streamed from
  `ROCK_X5.DAT`/`ROCK_X5.BIN` ("dirty-RAM overlay" model).
- **There is no static overlay index map in the repo.** The recomp captures
  overlay code *at runtime* (`overlay_captures.json` + compiled DLL cache); no
  captures exist locally. So overlay load addresses cannot be mined from the
  repo — only the model (same as MMX6's ROCK_X6).
- A raw MIPS-pattern scan over all 47 MB of `ROCK_X5.DAT` found **zero**
  `lui 0x8009/0x800A/0x800D`+offset pairs, while the same scanner found dozens
  in the EXE — the DAT's chunks (which contain nested `(offset,size)`
  sub-tables) evidently hold **compressed** code/data. Carving overlay code
  would require reversing the decompressor first (see §7).
- Useful confirmed globals from `game.toml` (widescreen work): 0x8009A1F8 = BG
  layer struct array, 0x800A51A8 = tile ring, 0x800D1DBC = map size — i.e. the
  0x8009xxxx/0x800Dxxxx region is the engine's static BSS, not overlay-owned.

## 3. The player object: fixed struct at 0x8009A0A0

The EXE materializes `0x8009A0A0` (`lui 0x800A; addiu reg, -0x5F60`) in ~100
places. It is the **player object**, a fixed-address instance of the engine's
generic object struct (same layout used by enemies/bosses — e.g. an object
spawn at `0x80052E44` writes its own HP at +0x5C and contact damage at +0x60).

Proof it is the *player*: the enemy-contact collision routines write the
attacker's contact-damage value to the **hardcoded** address 0x8009A199
(= base+0xF9) while manipulating the same object through a pointer:

```
FUN_8002ecb0 (collision, overlap test):        FUN_80032844:
  ...
  if (bVar10 != 0)                               *(u8*)(param_2+0x71) = 0xf;
    DAT_8009a199 = *(u8*)(param_1 + 0x60);       DAT_8009a199 = *(u8*)(param_1+0x60);
```

### Field map (base P = 0x8009A0A0) — all verified in disassembly

| Offset | Address | Size | Meaning | Evidence |
|---|---|---|---|---|
| +0x02 | 0x8009A0A2 | s8 | **Character index** (0 = X, nonzero = Zero) | added to 0x800D1C00 before reading max HP at +0x47 → 0x800D1C47 (X) / 0x800D1C48 (Zero), matching the known cheat addresses |
| +0x04/05/06 | 0x8009A0A4.. | u8 | state bytes; +5 = action state (0x11 = hurt/knockback, written by FUN_80038d44; dispatched via jump table `PTR_800745f0` in FUN_800352a8) | |
| +0x2F | 0x8009A0CF | u8 | state byte (user-verified; cleared… note FUN_800352a8 clears +0xCF=0x8009A16F each frame, a different field) | |
| **+0x5C** | **0x8009A0FC** | **u8** | **Authoritative current HP.** Bit 7 = "damage event" flag (value is always masked `& 0x7F` when read). `0x80` exactly = death sentinel | see §4 |
| +0x60 | 0x8009A100 | u8 | contact damage this object deals (generic object field; on enemies this is what hits you) | FUN_8002ecb0 |
| **+0x61** | **0x8009A101** | **u8** | **Mercy-invincibility (i-frame) timer**, frames | see §5 |
| +0x63 | 0x8009A103 | u8 | hit-type index (1 = normal hit…) — indexes knockback velocity table 0x80074778 and i-frame duration table 0x80074818 | FUN_80038d44 |
| +0x70/+0x71 | 0x8009A110/11 | u8 | hit flags (collision writes +0x71; merged each frame: `P+0x89 = P+0x70 \| P+0x71` then cleared) | FUN_800352a8 |
| +0x79/+0x7A | 0x8009A119/1A | u8 | spike/instadeath contact flag(+0x79) / immunity flag (+0x7A==1 blocks it) | FUN_800389e8 |
| +0x89 | 0x8009A129 | u8 | merged damage flags; `(x&3)==3` or `(x&0xC)==0xC` = crushed/instadeath, other combos = normal hit | FUN_800389e8 |
| +0xA4 | 0x8009A144 | u8 | hurt-blink flag; set 1 on hit, cleared when i-frame timer expires | FUN_80038d44 / 0x80038C74 |
| +0xF8 | 0x8009A198 | u8 | post-hit knockback/hit-stun timer; set to **0x4B** on hit, decremented once per frame in FUN_800352a8 before damage resolution | 0x80038AE0, 0x8003530C |
| +0xF9 | 0x8009A199 | u8 | **pending incoming damage amount** for this frame (written by collision code from attacker+0x60) | 0x8002EF5C, 0x800328A8 |
| +0x14B/+0x14C | 0x8009A1EB/EC | s8/u32 | virus/DoT state: +0x14B < 0 → every 0x12C frames HP -= 2 (X only) | FUN_8003a1fc |
| +0x154 | 0x8009A1F4 | u8 | virus-hit timer, set 0x4B | FUN_80039bf0 |

+0x5D (0x8009A0FD) = displayed HP-bar value chasing +0x5C (user-verified; the
HUD writer for it was not located in the EXE — likely overlay HUD code).

## 4. Authoritative HP — 0x8009A0FC, with bit-7 semantics

Every HP mutation found in the EXE operates **directly on P+0x5C**; there is no
second storage it is recomputed from (consistent with the user's full-RAM scan
finding no other copy):

- **Damage resolution** — `FUN_800389e8(P)` (0x800389E8), called once per frame
  from `FUN_800352a8(P)` (0x800352A8, the per-frame player-damage/status tick):
  ```c
  // normal hit path (decompiled):
  uVar3 = *(byte*)(P+0x5c) & 0x7f;              // current HP
  *(char*)(P+0x5c) -= *(char*)(P+0xf9);          // subtract pending damage
  if (*(char*)(P+0x5c) < 1)  *(u8*)(P+0x5c) = 0x80;      // dead sentinel
  else { *(byte*)(P+0x5c) |= 0x80;               // set "damaged" flag bit
         _DAT_800d1cb8 += *(char*)(P+0xf9); }    // ranking damage stat += dmg
  ```
  Crush/instadeath paths: `dmg_stat += HP & 0x7F; P+0x5C = 0x80`.
- **Death detection** (same function): `if (*(s8*)(P+0x5c) == -0x80) { P+0x5c=0;
  DAT_800d1c1c = 1; ... state=2 (death) }`.
- **Pit/scroll kill** — `FUN_80029184`: sets `DAT_8009a0fc = 0x80` directly
  (hardcoded), `dmg_stat += old & 0x7F`.
- **Heal/refill** — `FUN_80034140` (0x80034140): drains the queued-refill
  counters `0x800D1C76` (X) / `0x800D1C77` (Zero) (value `& 0x7F`, bit 7 =
  active flag — sub-tank/pickup heals), incrementing P+0x5C by 1 per tick,
  clamped to max HP = `s8 [0x800D1C00 + charIdx + 0x47]`.
- **Full heal** — `FUN_80039bf0`: `P+0x5C = [0x800D1C00+charIdx+0x47]`.
- **Virus DoT** — `FUN_8003a1fc`: `P+0x5C -= 2` every 300 frames when infected.

**Max HP: `0x800D1C47` (X) / `0x800D1C48` (Zero)** — confirmed both by the
`charIdx + 0x47` code path and by the known "max energy" cheat addresses in
`mmx5-ram-notes.md`. Current HP is *not* persisted in the save struct;
0x800D1C46's "inf-health" cheat is a 16-bit write whose high byte just sets max
(0x40) at 0x800D1C47.

**Why live pokes to 0x8009A0FC appeared not to stick (unresolved, hypotheses):**
the static EXE contains no unconditional per-frame writer of P+0x5C. Either
(a) the observed rewriter lives in streamed **overlay code** (character-control
overlay; the lava-damage code at 0x800F2AB0/0x800F6C3C proves gameplay code
runs in that range), or (b) the poke interacted with the bit-7 flag protocol
(HUD/hurt code masks `& 0x7F` and writes back, e.g. `FUN_80038d44` does
`P+0x5C &= 0x7F` on hit-reaction entry). Confidence that 0x8009A0FC is the
authoritative value the game *uses* (damage, death check, heal clamp): **high**.
Identity of the frame-writer observed live: **unverified** (see §7).

## 5. Mercy invincibility (i-frames) — timer at 0x8009A101 (P+0x61)

- **Set on hit** in `FUN_80038d44` (0x80038D44, hit-reaction/knockback starter;
  contains the "Walk Through Walls" cheat patch sites 0x80038EEC):
  ```c
  *(u8*)(P+0x61) = (&DAT_80074818)[hitType];   // 0x80038EC0
  ```
  Duration table at **0x80074818** (bytes): `00 4B 64 00 4B 64 64 64 64 64 ...`
  → normal hit = 0x4B (75 frames), heavy hits = 0x64 (100 frames).
- **Decremented once per frame** at 0x80038C54..64 inside `FUN_800389e8`; on
  the 1→0 transition the blink flag P+0xA4 is cleared (0x80038C74) and
  `FUN_8003c5d8` restores the sprite.
- **Damage gate:** the enemy-contact collision routines begin with
  ```
  8002E278: lb   $v0, 0x61(player)     8002E40C: lb $v0, 0x61(player)
  8002E280: bnez $v0, <skip-all>       8002E414: bnez $v0, <skip-all>
  ```
  i.e. **nonzero P+0x61 = completely intangible to contact damage** (no hit
  flags get set at all). The spike/instadeath path in `FUN_800389e8` also
  requires `P+0x61 == 0` (`P+0x79 != 0 && P+0x61 == 0 && P+0x7A != 1` → kill).
- Cleared on death/respawn (0x8003E2EC) and in state resets (0x800373AC…).

Confidence: **high** (set-constant + per-frame decrement + skip-damage check
all located and consistent).

## 6. Damage application chain & related globals (summary)

```
collision (FUN_8002ecb0 / FUN_80032844 / 0x800318xx / 0x80031Bxx / 0x80032150 variants)
   -> writes hit flags (P+0x71) and pending damage 0x8009A199 = attacker+0x60
per-frame:  FUN_800352a8(P)          # player damage/status tick
   P+0x89 = P+0x70 | P+0x71;  decrement P+0xF8;
   -> FUN_800389e8(P)                # damage resolution (subtract, death, dmg stat)
        -> FUN_80038d44(P)           # hurt reaction: knockback vel table 0x80074778,
                                     #   i-frames from 0x80074818, state = 0x11
```

- **Damage-taken ranking stat**: `0x800D1CB8` (u32; = save block 0x800D1C00 +
  0xB8) — incremented at 0x800292E0, 0x800318DC, 0x80031B1C, 0x80038A4C/80,
  0x80038B10/88, 0x80038BE0. Matches the user's live finding (freezing it
  cannot stop HP loss — it is written *after* HP, never read back into HP).
- **Global gates**: `0x800D1C10` nonzero = damage/status processing skipped
  (pause/cutscene); `0x800D1C1C` set to 1 on player death.
- **No pointer chase needed**: the player object is at the fixed address
  0x8009A0A0 in this build (all collision writes are hardcoded).
- **Boss HP 0x800920EC** (user-verified): consistent with a boss object based
  at 0x80092090 (+0x5C = 0x800920EC); note that region is *above* end-of-text
  0x80092000, i.e. overlay/BSS-resident — offsets +0x5C (HP) and +0x60 (contact
  damage) are generic object fields engine-wide.

## 7. What remains unverified / next steps

1. **The live-observed per-frame rewriter of 0x8009A0FC.** Not in the static
   EXE. Next step: in BizHawk (Nymashock), Lua
   `event.on_bus_write(cb, 0x8009A0FC)` (or the debugger's write breakpoint)
   and log the PC — expect an address in the 0x800Fxxxx overlay range. If so,
   the overlay chunk can be captured live (savestate RAM dump) and carved into
   Ghidra at that address; static carving from ROCK_X5.DAT is blocked on its
   (unreversed, apparently compressed) chunk format.
2. **HUD writer of 0x8009A0FD** (display bar) — not located in EXE; assumed
   overlay HUD code. Harmless for our purposes.
3. Whether lava/environment damage (overlay code at 0x800F2AB0/0x800F6C3C)
   respects the P+0x61 gate — the existence of a separate "lava" cheat suggests
   it may bypass contact collision entirely. Test in-game with recipe below.
4. ROCK_X5.DAT chunk compression format (needed only for full static overlay
   analysis; the EXE presumably contains the loader/decompressor — finding the
   function that walks the DAT's (sector,size) table is the entry point).

## 8. Recommended Lua invincibility recipe (BizHawk, MainRAM domain = addr − 0x80000000)

Primary (clean, engine-native — makes the game treat you as in mercy-frames):

```lua
-- every frame, before frame advance:
local P = 0x9A0A0        -- player struct, MainRAM offset (0x8009A0A0)
memory.writebyte(P + 0x61, 2)          -- 0x8009A101: i-frame timer, keep >= 2
                                       -- (engine decrements to 1, never hits 0,
                                       --  so the blink-clear transition never runs)
```
This makes contact collision early-out (0x8002E278/0x8002E40C) and blocks
spike death. No visual blink (P+0xA4 stays 0 because it is only set on a real
hit).

Belt-and-suspenders (also covers overlay damage paths like lava, and heals):

```lua
local charIdx = memory.read_s8(P + 0x02)           -- 0 = X, else Zero
local maxHP   = memory.readbyte(0xD1C47 + charIdx) -- 0x800D1C47/48
memory.writebyte(P + 0x5C, maxHP)                  -- 0x8009A0FC authoritative HP
memory.writebyte(P + 0x5D, maxHP)                  -- 0x8009A0FD displayed bar
memory.writebyte(P + 0xF9, 0)                      -- 0x8009A199 pending damage
```
Write HP *without* bit 7 set and ≤ maxHP. If the overlay frame-writer still
reverts it, run step §7.1 to find and NOP that writer (or accept the +0x61
method, which prevents damage from ever being queued).

Do **not** write 0x8009A0CF (breaks movement — it is a state byte, despite
cheat sites listing it as health).

---

### Artifacts kept in scratchpad (session-local)
`extract_iso.py`, `scan_refs.py`/`scan_refs2.py` (MIPS lui/imm effective-address
scanner), `disasm.py` (capstone), Ghidra project `MMX5.gpr` +
`ghidra_scripts/DecompTargets*.java`, extracted disc files.


---

# 2026-08-05 — Static analysis session 2 (autonomous): item kinds, Boss Level, Parts storage, stage-select gate

Re-done from scratch: the 2026-07-30 Ghidra project lived in a session
scratchpad and is gone. Re-extracted and re-analysed with a purpose-built MIPS
xref scanner (also scratchpad-local; rebuild recipe in §9.8).

## 9.0 Provenance of the three images used

| Image | What it actually is | How verified |
|---|---|---|
| `SLUS_text.bin` | vanilla boot EXE .text, base `0x80010000`, `0x82000` bytes | re-extracted from `Games\MegamanX5\Megaman X5.bin` LBA 23432; PS-EXE header `pc0=0x8005894C t_addr=0x80010000 t_size=0x82000` — identical to the 2026-07-30 extraction |
| `enigmaRAM.bin` (workspace root) | **VANILLA disc**, hub overlay resident | parts table at `0x800F5194` reads `00 04 05 02 07 06 01 03`, exact match for the documented `[0,4,5,2,7,6,1,3]`; contains none of the AP patch sites |
| `Scripts\ramdump_cut1_f124157.bin` | **AP PROTO disc** | its diffs vs the vanilla EXE are *exactly* our patch set: `0x80011069`/`0x8001108C` (jump-table redirects), `0x8003C324`/`0x8003D660`/`0x8003D814` (1 byte each, `0x4C`→`0x4D`), `0x80053805`/`0x80053839`/`0x80053849` (tank fix), `0x80055018` (capsule spawn gate), `0x80055DB8` (capsule hook), `0x800776A0` +76 B (pickup stub), `0x80077700` +76 B (capsule stub). A different overlay occupies the `0x800EC000` window — it is NOT the hub |

**CORRECTION 2026-08-05 (same day):** an earlier draft of this section claimed
`enigmaRAM.bin` was *the only* local image containing the hub module. **That was
wrong** — it came from a file survey truncated by `head -30`. `Scripts/` holds
~20 more RAM dumps, including `ramdump_hub_f22905.bin` (the hub dump this
document's §10 was originally written from), `ramdump_partsmenu_f23591.bin`,
two **in-stage gameplay dumps** (`ramdump_stage_f174001.bin`,
`ramdump_stage_f284694.bin`), launch, and endgame captures. Enumerate
`Scripts/ramdump_*.bin` in full before concluding an overlay is unavailable.

Both dumps also differ from the disc EXE across `0x8006F000-0x80092000`. That is
initialised data the game mutates at runtime (e.g. the 16×u16 ammo array at
`0x8006FAE4` in the save map), not code. Not a concern.

## 9.1 Q_A RESOLVED — `0x800D1C84` **is** the DNA Parts bitfield

The RAM-notes row calling it "dubious" and the matching open checklist item are
both superseded. Proof is a live reader in the hub overlay, function `0x800F3E30`:

```
800F3E34  lui   $s0, 0x800d
800F3E38  addiu $s0, $s0, 0x1c00      ; $s0 = 0x800D1C00
800F3E50  lb    $v0, 0x32($s0)        ; selected part index (0x800D1C32)
800F3E54  addiu $a0, $a0, 0x51f0      ; mask table 0x800F51F0
800F3E58  sll   $v0, $v0, 2
800F3E60  lw    $v1, ($v0)            ; mask = table[index]
800F3E64  lw    $a0, 0x84($s0)        ; <-- 0x800D1C84, parts owned
800F3E6C  and   $v1, $v1, $a0
800F3E70  beqz  $v1, 800F3E88         ; not owned -> sb $zero,3($s1) = blank slot
800F3E78  jal   0x8002D89C            ; owned -> draw the part
```

**Mask table `0x800F51F0`** (hub overlay), index to bit:

| idx | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| bit | 17 | 10 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 11 | 12 | 13 | 14 | 15 | 16 |

16 single-bit entries covering **bits 2..17** of the u32; bits 0/1 unused here.
(Indices 16-17 hold multi-bit values `0x00020204` / `0x00000402`; index >= 18 is
`0x01010101` filler — the table is 16 entries, treat >15 as out of bounds.)

**Why the live observation said otherwise.** The static EXE contains *no*
gameplay writer of `0x800D1C84` — only the save loader (`0x8001C964`,
`0x8001CC90`, both `sw`) and the save store (`0x8001CFA0`, `lw`). The grant
therefore happens in overlay code, and X5 **buffers DNA rewards** and delivers
them at the *next* results sequence (`0x800D1D28-2A` / `0x800D1D38-3A`, already
documented). Watching `0x1C84` at award time was always going to show nothing.
**[MECH]** — recheck by reading `0x1C84` before/after a **results screen**, not
before/after the award prompt.

## 9.2 Q_D — the six u32s at `0x800D1C88-9F`: persisted, untouched by all visible code

The save loader at **`0x8001C904`** block-copies them in a fused loop:

```
8001C910  addiu $t0, $v0, 0x1c00     ; $t0 = 0x800D1C00
8001C914  addiu $t6, $t0, 0x88       ; dest = 0x800D1C88
8001C948  addiu $t3, $a2, 8          ; src  = savefile + 0x08
   loop:  $v0 = $t3 + i*4 ; $v1 = $t6 + i*4 ; lw ($v0) ; sw ($v1)   (6 iterations)
```

confirming the save-format map (`+0x08..+0x1F` to `0x800D1C88..`). The same loop
also carries `file+0x4B -> 0x800D1C4D` and `file+0x52 -> 0x800D1CA3` byte arrays.

**There are ZERO individual field references to `0x800D1C88-0x800D1C9F` in the
static EXE or in the hub overlay.** They are touched only as a block, by save
load/store.

For the Alia-suppression idea (#8) this is neither support nor refutation: an
in-stage visit record would be read by *stage* overlay code, which is in neither
local image. It does mean the question **cannot be closed statically** with the
images we have — it needs the RAM-diff test across a first vs repeat entry.

## 9.3 Q_B RESOLVED — item-kind tables, and which kinds are safe for pickupsanity

Two dispatch tables, adjacent:

| Table | Address | Entries | Referenced from |
|---|---|---|---|
| **collect** (on pickup) | `0x80011068` | 28 (kinds `0x00-0x1B`) | `0x80054084` |
| **init** (spawn / ownership) | `0x80011038` | 12 (kinds `0x00-0x0B`) | `0x8005379C` |

The collect table ends at `0x800110D8` where ASCII strings begin (`"SPU:"`,
`"wait (reset)"` ...) — a hard end at 28 kinds.

| kind | init | collect | identity | evidence |
|---|---|---|---|---|
| `0x00` | `0x800537B8` | `0x800540A0` | **Heart Tank** | writes `0x800D1C80` |
| `0x01` | `0x800537D4` | `0x80054100` | **EX item** | writes `0x800D1C80` |
| `0x02` | `0x80053858` | `0x80054164` | **small HP** | heals 4, or 5 if `player+0xFC & 0x40` |
| `0x03` | `0x80053858` | `0x80054198` | **large HP** | heals 16, or 20 with the same flag |
| `0x04` | `0x80053858` | `0x800541D8` | **full HP** | amount = max HP `0x800D1C47 + charIdx` |
| `0x05`/`0x06`/`0x07` | `0x80053858` | `0x80054204` (shared) | **weapon energy** | passes its own kind byte `obj+0x82` to `0x80053B68` |
| `0x08` | `0x80053858` | `0x80054218` | **1-UP** | `0x800D1C45 += 1`, clamped at 10 |
| `0x09` | `0x80053800` | `0x80054264` | Sub-Tank | the three tank-fix sites |
| `0x0A` | `0x8005382C` | `0x800542D0` | W-Tank | " |
| `0x0B` | `0x8005383C` | `0x80054310` | EX-Tank | " |

**Kinds `0x00`-`0x08` all share the generic init `0x80053858`** — no per-kind
ownership test, therefore no already-owned despawn. Only `0x09`/`0x0A`/`0x0B`
carry one, which is exactly what the tank fix patches.

This is **code-level confirmation that consumables cannot hit the "X5 deletes
what you already own" trap**, closing that question for pickupsanity.

=> **Pickupsanity kind set = `0x02` .. `0x08` (seven kinds).**

## 9.4 Q_B identity — pickup `id` is a TYPE id and COLLIDES; position is the stable key

From `Scripts\mmx5_placement_log.txt`, deduplicated on `(stage, area, id, x, y)`.
The raw log accumulates across repeat visits, so **undeduped counts are
meaningless** — 145 raw lines collapse to 50 unique placements over 10 stages
(partial coverage: mostly entry areas).

Genuine same-`(stage, area, id)` collisions at distinct coordinates:

| stage | area | id | n | coords |
|---|---|---|---|---|
| Dark Dizzy | 1 | `0x06` | 2 | (2440,384) (2440,752) |
| Duff McWhalen | 0 | `0x20` | 3 | (2992,744) (3104,912) (4864,712) |
| Izzy Glow | 1 | `0x24` | 3 | (2392,2016) (2912,1728) (3456,1328) |
| Axle the Red | 0 | `0x00` | 4 | y~1136 cluster |
| Axle the Red | 0 | `0x01` | 4 | y~1136 cluster |
| Zero Space 3 | 0 | `0x22` | 3 | (1576,2224) (3376,2088) (4384,2088) |

`(x, y)` is unique within a `(stage, area)` across every deduped placement.

**Design consequence for pickupsanity:** the mailbox record `{stage, kind, id,
seq}` **cannot identify a consumable pickup** — three Izzy Glow capsules are all
`id=0x24`. The stub must also record position (or the placement-record index)
for consumable kinds. That is a **stub change, not a table change**, and it is
the largest remaining unknown on the feature.

Consumable id space seen so far: `0x20 0x21 0x22 0x24 0x25 0x26` (`0x23` not yet
observed). Heart/tank ids: `0x00-0x07` hearts, `0x27`/`0x28` Sub-Tanks, `0x29`
W-Tank, `0x2A` EX-Tank.

**Caveat on the harvester's labels.** `mmx5_placement_dump.lua` labels ids
`0x00-0x07` as "HEART TANK (bit n)" *by assumption*. Axle the Red area 0 shows
four `id=0x00` and four `id=0x01` records in a horizontal row — that is not four
heart tanks. Treat the id-to-label mapping below `0x20` as unverified.

## 9.5 Q_F — the **Boss Level formula function** located: `0x80024594`

Decoded from disassembly:

```
level_raw = 2 * floor(elapsed / 432000)          ; 432000 frames = 2 h
          + popcount(player+0xC9)                ; weapons byte (copy of save 0x1C4C)
          + rankTable[ 0x800D1CAA + charIdx ]
elapsed   = 0x34BC00 - 0x800D1CAC                ; 0x34BC00 = 16 h in frames
            (clamped >= 0)
0x800D1CC0 = min(level_raw + 1, 0x60)            ; 96 cap
0x800D1CA2 = min(0x800D1CA2 + level_raw, 0x7F)   ; accumulator, 127 cap
```

- the 2-hour divide is the standard signed-division-by-constant idiom (`mult` by
  `0x9B583739`, `mfhi`, `sra 0x12`), divisor 432000
- **rank modifier table `0x800717EC`** (u16): `[0]=+16 [1]=+8 [2]=+4 [3]=+2
  [4..7]=+0`. The index runs **best-first**: index 0 is MEH/MMH, not E. The
  ram-notes list the same values in the opposite order — the *values* were
  right, the implied index order was not.
- `0x800D1CC0` is written only at `0x80024574` / `0x80024588` / `0x8002465C` and
  **read by nothing** in the EXE or hub => consumed by overlay code.
- `0x800D1CA2` is read at `0x800259E0`, `0x8002617C` (EXE) and `0x800F7564`
  (hub), each time as **`(value - 0x20) / 2`** — a scaling factor. Consumer
  functions: `0x80025828` (called from `0x8002475C`) and `0x80026080` (many
  callers in `0x80025xxx`).

**Design consequence for `boss_difficulty` and tester request #2:** the client
currently sets difficulty *indirectly*, by pinning the countdown — the same byte
the endgame interlock depends on. `0x800D1CC0` is the computed level itself.
Pinning it directly would decouple difficulty from the collision deadline: the
countdown pin stays (the endgame gate still needs it), but the two stop being
one knob. **[INFER]** — the write sites are proven, the effect of *overriding*
the value is not, because the consumer is in overlay code we cannot see. Needs a
live test before being designed around.

## 9.6 Q_G — first located **stage-select availability gate**: `0x800F26C0` (hub)

```
800F26C0  lui   $v1, 0x800d
800F26C4  addiu $v1, $v1, 0x1c00     ; $v1 = 0x800D1C00
800F26CC  lbu   $v0, 0x79($v1)       ; ACT  (0x800D1C79)
800F26D4  sltiu $v0, $v0, 5          ; ACT < 5 ?
800F26D8  bnez  $v0, 800F2714        ;   -> UNAVAILABLE path
800F26E0  lbu   $v0, 0xcb($v1)       ; launch flags (0x800D1CCB)
800F26E8  andi  $v0, $v0, 0x80       ; bit7 = launch already succeeded
800F26EC  bnez  $v0, 800F2714        ;   -> UNAVAILABLE path
800F26F4  addiu $v0, $zero, 0x788c   ; AVAILABLE   entry sprite
800F2714: addiu $v0, $zero, 0x7880   ; UNAVAILABLE entry sprite
          sh    $v0, 0x42($s1)       ; entry sprite id
          jal   0x80017214           ; (obj, 2, a2)   a2 = 2 available / 0 not
```

This is the **`ACT >= 5` rule that puts Zero Space on stage select**, now located
in code rather than inferred from live pokes — and it shows the shape a stage-lock
hook needs: an availability predicate feeding a sprite id at `obj+0x42` plus an
`a2` enable flag.

Caveats before building on it:

- `0x80017214` is a **generic sprite/animation setter** — 40 call sites in the
  hub. It is not a stage-select API; only the predicate above is specific.
- This is *one* entry's gate. Whether the eight Maverick entries have their own
  predicates (hookable) or are unconditionally enabled (a predicate must be
  *added*) is **[OPEN]** — the next question for feature #7.
- `0x800F2C94` reads `0x800D1C2A` while setting up another entry; unidentified.

## 9.7 Q_E — damage table NOT found

No weapon/weakness damage table located. **Ruled out:** the
`0x80074000-0x80075200` band is animation/state tables — it holds the known
knockback (`0x80074778`) and i-frame (`0x80074818`) tables and ~55 others of the
same character, none damage-shaped.

Best remaining lead is the level-scaled stat family `0x80024594` ->
`0x80025828` / `0x80026080`, all consuming `0x800D1CA2` as `(x-0x20)/2`; that is
where per-encounter stats are computed. A DuckStation write-watchpoint on boss HP
`0x800920EC` during a weakness hit remains the fastest route. Static analysis did
not close this one.

## 9.8 Rebuilding the toolkit

Scratchpad-local (session-lived), so the recipe matters more than the files:

1. Extract `SLUS_013.34`: MODE2/2352, user bytes 24..2071, ISO9660 PVD at LBA 16
   -> root dir -> `SLUS_013.34;1` at LBA 23432. Strip the 0x800-byte PS-EXE
   header => `.text` at base `0x80010000`.
2. Scanner: decode words; for each `lui rX,hi` (accept only
   `0x8000 <= hi <= 0x801F`) look ahead ~12 instructions for `lw/lbu/sb/sw/...`
   with `rs == rX`, or `addiu`/`ori` on `rX`; effective address =
   `hi<<16 + simm`. Stop on redefinition of `rX`.
3. Save-struct fields need a **second** mode: seed on materialisations of
   `0x800D1C00`, then track that register forward and resolve `off(reg)`.
   Without it most save-struct accesses are invisible — the game addresses the
   block via a base pointer, not absolute effective addresses.
4. Ghidra 12.1.2 headless works if decompilation is wanted:
   `analyzeHeadless <proj> MMX5 -import SLUS_text.bin -processor MIPS:LE:32:default
   -loader BinaryLoader -loader-baseAddr 0x80010000` (JDK 21 on PATH, ~2 min).
   The Python scanner answered every question above faster, so the project is
   optional.

**Known scanner limitation:** it misses accesses where the struct base arrives as
a *function parameter* — the three stage-load sites `0x8003C324` / `0x8003D660` /
`0x8003D814` do **not** appear in a `0x800D1C00` field scan because `ctrl` is
passed in. **Absence of a hit is not absence of a reference.**


## 9.9 Q_B identity RESOLVED — the item object back-points to its placement record

Supersedes §9.4's "needs position" conclusion. **`itemObj+0x10` = pointer to the
placement record that spawned it.** This was already stated in
`mmx5-overlay-findings.md` §1.4; it is now verified in the disassembly of the
per-record spawner `0x8002B070`:

```
8002B28C  sb  $v0, 0x00($s1)     ; type
8002B298  sb  $v1, 0x01($s1)     ; minor  (0x2F = item)
8002B2A4  sb  $v0, 0x02($s1)     ; id
8002B2B0  sh  $v1, 0x0A($s1)     ; x
8002B2B8  sw  $s2, 0x10($s1)     ; <-- RECORD POINTER  ($s2 walks the list)
8002B2BC  sh  $a0, 0x0E($s1)     ; y
...
8002B42C  sb  $v0, 0x03($s2)     ; mark record spawned (sub += 0x10)
```

**This is the stable unique location key pickupsanity needs**, and it is the same
concept the MMX4 apworld client keys on. Colliding type-`id`s stop mattering.

Design that falls out of it:

- the stub reads `lw $t?, 0x10($s1)` and records the **u32 record pointer**
- the client computes `index = (recptr - listbase) / 8`, where
  `listbase = *(0x80072EAC + stage*8 + area*4)` — the same table the placement
  harvester already uses
- location identity = `(stage, area, index)`: stable across runs, unique by
  construction, independent of coordinates

The mailbox slot must widen from 4 bytes to 8 to carry the pointer — which is the
same change the **ring-overflow fix** already required, so the two land together.

## 9.10 Alia visit-record hypothesis (#8) — DEAD

`0x800D1C88-0x800D1C9F` reads **all-zero in every RAM dump available**, including
a mid-run save at `weapons=0x3F` (six Mavericks defeated, ACT=5). Six u32s still
zero that deep into a run are not a per-stage visit record. Combined with §9.2
(no field references anywhere in the EXE or the hub overlay), the suspect is
**dead**, not "unproven".

Live behaviour observed 2026-08-05 (Ivor): Alia is **silent on re-entry after a
clean stage-select round trip**, and silent across death/respawn. So visit state
*is* tracked somewhere — just not in that region, and not anywhere in
`0x800D1C00-0x800D1D60`: the save-block watcher logged zero relevant changes
across a full visit (only lives, countdown, clear-time, damage-stat and mode
bytes moved).

**A wide RAM diff at stage select was attempted and failed** — ~89,000 candidate
bytes. Stage select is not quiescent (audio and graphics scratch churn
constantly), so that method cannot isolate the flag. **Do not retry it without a
fundamentally different filter.**

The only remaining route is to find the code that *gates the dialogue*, in stage
overlay code — two in-stage gameplay dumps exist, see the §9.0 correction —
rather than hunting its flag in RAM. Given the cost already sunk and that the
payoff is purely cosmetic, **the recommendation is to drop #8.**

## 9.11 Method note — what went wrong in this session

Two avoidable detours, recorded so they are not repeated:

1. **A truncated file listing became a stated conclusion.** `head -30` on a
   `find` over `*.bin` cut off before the stage and hub dumps, and the missing
   files were then reported as non-existent. Two live tests were requested that
   existing dumps already covered. **Enumerate fully before concluding absence.**
2. **A documented answer was re-derived as an open question.** `itemObj+0x10`
   was in overlay-findings §1.4 the whole time, while §9.4 called pickup identity
   "the largest remaining unknown". **Grep the research docs for the structure
   before designing an experiment to find it.**

Both had the same shape: acting on an incomplete search instead of an exhausted
one. The static-analysis findings in §9.1–9.7 were unaffected — those came from
disassembly, not from file surveys — but the experiment design that followed
cost live testing time that was not needed.


## 9.12 Placement data is on the DISC — full pickup inventory extracted statically

**The runtime placement harvest is unnecessary.** Stage overlay *data* is raw in
`ROCK_X5.BIN`, exactly as code overlays are (CLAUDE.md already recorded that the
recomp project's "overlays are compressed" claim is wrong for code). Every
stage's placement record list is therefore readable straight off the disc.

Result: **all 17 lists resolved, 50 item records, 26 consumables**, for every
stage and area including ones nobody has ever walked into.
Inventory: **`Reference/mmx5-placements.csv`**.

### Why this is exact rather than heuristic

Two facts remove all guessing:

1. **The list-pointer table `0x80072EAC` is STATIC EXE DATA.** It is *not*
   repointed at stage load, contrary to the note in overlay-findings §1.4 —
   verified byte-identical in the stage-6 and stage-7 RAM dumps. So every
   `(stage, area)` list RAM address is known up front:
   `list_ram = *(0x80072EAC + stage*8 + area*4)`.
2. **Every stage overlay chunk streams to RAM base `0x800EE970`** — the same
   base the hub and results modules use. Derived from the stage-7 anchor
   (list RAM `0x800FA618` ↔ disc `0x8D4A8`, chunk 10 base `0x81800`).

Hence `disc_off = chunk_base + (list_ram - 0x800EE970)`, with the chunk
identified by checking that the parsed list contains that stage's documented
heart bit.

`ROCK_X5.BIN` itself is a container of `(u32 sector, u32 size)` pairs, sector
(2048 B) aligned, 59 chunks.

### Validation — two independent methods agree exactly

Per-stage consumable counts, disc extraction vs the live harvest log:

| | Intro | Grizzly | Dizzy | Duff | Mattrex | Squid | Izzy | Axle | Skiver | ZS3 |
|---|---|---|---|---|---|---|---|---|---|---|
| harvest | 1 | 1 | 2 | 4 | 3 | 0 | 4 | 2 | 1 | 8 |
| **disc** | 1 | 1 | 2 | 4 | 3 | 0 | 4 | 2 | 1 | 8 |

Stage 7's list resolves to `0x8D4A8`, matching the RAM anchor exactly, and its
parse reproduces the harvested records byte for byte — including the eleven
armor-gated phantom hearts and the single ungated `id=0x05` heart (stage 7 =
bit 5, as documented).

### The list table

| stage | area | list RAM | where | disc | recs | items | cons |
|---|---|---|---|---|---|---|---|
| Intro | 0 | `0x80073748` | EXE | `0x063748` | 58 | 1 | 1 |
| Grizzly Slash | 0 | `0x800FBD3C` | chunk1 | `0x01ABCC` | 72 | 3 | 1 |
| Dark Dizzy | 0 | `0x800F37E0` | chunk2 | `0x021E70` | 175 | 2 | 1 |
| Dark Dizzy | 1 | `0x800F8B4C` | chunk3 | `0x02D1DC` | 116 | 3 | 1 |
| Duff McWhalen | 0 | `0x80100BB0` | chunk4 | `0x041240` | 53 | 5 | 4 |
| Mattrex | 0 | `0x800F4558` | chunk5 | `0x0493E8` | 73 | 4 | 3 |
| Mattrex | 1 | `0x800FDB7C` | chunk6 | `0x059A0C` | 91 | 0 | 0 |
| Squid Adler | 0 | `0x80100078` | chunk7 | `0x06CF08` | 119 | 1 | 0 |
| Izzy Glow | 0 | `0x800F326C` | chunk8 | `0x0738FC` | 54 | 2 | 0 |
| Izzy Glow | 1 | `0x800F9E48` | chunk9 | `0x07FCD8` | 62 | 4 | 4 |
| Axle the Red | 0 | `0x800FA618` | chunk10 | `0x08D4A8` | 113 | 14 | 2 |
| The Skiver | 0 | `0x800F8C64` | chunk11 | `0x099AF4` | 89 | 3 | 1 |
| Dynamo | 0 | `0x800F166C` | chunk12 | `0x09DCFC` | 1 | 0 | 0 |
| Zero Space 1 | 0 | `0x800739C4` | EXE | `0x0639C4` | 1 | 0 | 0 |
| Zero Space 2 | 0 | `0x80073A8C` | EXE | `0x063A8C` | 20 | 0 | 0 |
| Zero Space 2 | 1 | `0x80073B5C` | EXE | `0x063B5C` | 46 | 0 | 0 |
| Zero Space 3 | 0 | `0x80074140` | EXE | `0x064140` | 113 | 8 | 8 |

Intro and Zero Space lists live in the static EXE, as overlay-findings §1.5
already noted. **Mattrex area 1 and Dynamo area 0 contain no items at all** —
they parse cleanly with 91 and 1 records respectively. That is a real result,
not a failure to resolve; the harvest never reached Mattrex area 1 either.

### The pickupsanity location set (26)

| stage | area | record indices (id) |
|---|---|---|
| Intro | 0 | 47 (`0x21`) |
| Grizzly Slash | 0 | 60 (`0x21`) |
| Dark Dizzy | 0 | 173 (`0x21`) |
| Dark Dizzy | 1 | 12 (`0x24`) |
| Duff McWhalen | 0 | 21 (`0x21`), 22–24 (`0x20`) |
| Mattrex | 0 | 38 (`0x21`), 39 (`0x24`), 40 (`0x26`) |
| Izzy Glow | 1 | 58, 59, 61 (`0x24`), 60 (`0x21`) |
| Axle the Red | 0 | 109, 110 (`0x21`) |
| The Skiver | 0 | 86 (`0x21`) |
| Zero Space 3 | 0 | 36 (`0x26`), 37–39 (`0x21`), 40/41/43 (`0x22`), 42 (`0x25`) |

**26 new locations** — the concrete headroom figure for the location budget that
the chips, Ultimate/Black Zero and stage-unlock features all depend on.

Caveat worth carrying: the CSV lists **20 heart-class records (id < 0x10) for 8
real Heart Tanks**. The surplus are armor-gated phantom placements (Axle the Red
alone has eleven, `armorgate=5`). Filter on `gate == 0` before treating a
heart-class record as a real pickup, and do not assume `id < 0x10` means Heart
Tank.

### Method note

This was reached only after two failed attempts — a structural pattern scan that
mis-based stage 7 by one record (an off-by-one that would have corrupted every
location id), and a self-pointer calibration that mismatched by `0x14` and lost
the anchor stage entirely. Both failed for the same reason: inferring layout from
shape instead of reading the game's own pointer table. **When the game has a
table, read the table.**


### 9.12.1 CORRECTION — the table has 26 stage entries, not 13

The first pass looped `stage in range(0, 13)` and so read only stage ids
`0x00-0x0C`. **The pointer table actually holds 26 populated stage entries:**

| range | what |
|---|---|
| `0x00-0x0C` | Intro, the 8 Mavericks, Dynamo, two unused slots, **Sigma = `0x0C`** |
| `0x10-0x12` | **Zero Space 1 = `0x10`**, Zero Space 2 = `0x11`, X-vs-Zero duel = `0x12` |
| `0x16-0x1F` | post-Eurasia-crash stage variants, at a consistent **+0x17** offset from the originals (`0x02→0x19`, `0x04→0x1B`, `0x06→0x1D` — the area1 slots line up exactly) |

This was avoidable: `mmx5-ram-notes.md` already records **"Endgame stage ids are
NOT contiguous — Zero Space 1 = 0x10, X-vs-Zero duel = 0x12, Sigma = 0x0C —
never infer one from sequence"**, and CLAUDE.md repeats it. The loop bound
assumed contiguity anyway.

Consequences of the fix:

- **Zero Space 1 was never read.** It has **4 consumables** (area 0, record
  indices 69–72). Ivor flagged this from memory — "there's static energy in Zero
  Space first stage" — against an extraction that claimed zero.
- Zero Space 2 has 3 more.
- What the first pass labelled "Zero Space 3" (index `0x0C`) is the **Sigma
  stage**; its 8 consumables were real but misattributed.
- The alt stage set is nearly empty of pickups — only Dark Dizzy (alt) carries
  one — which is consistent with revisited stages having their collectibles
  already taken.

**Corrected totals: 33 lists, 59 item records, 34 consumables.** The
per-stage breakdown lives in `Reference/mmx5-placements.csv`.

The earlier cross-validation against the live harvest still holds — the harvest
only ever covered stages `0x00-0x0C`, which is exactly the range the first pass
read, so the two agreeing proved that range correct and said nothing about the
rest. **An agreement between two methods only validates the ground they both
cover.**

### 9.12.2 Consumable location set (34)

| stage id | stage | area/record indices |
|---|---|---|
| `0x00` | Intro | a0: 47 |
| `0x01` | Grizzly Slash | a0: 60 |
| `0x02` | Dark Dizzy | a0: 173 · a1: 12 |
| `0x03` | Duff McWhalen | a0: 21, 22, 23, 24 |
| `0x04` | Mattrex | a0: 38, 39, 40 |
| `0x06` | Izzy Glow | a1: 58, 59, 60, 61 |
| `0x07` | Axle the Red | a0: 109, 110 |
| `0x08` | The Skiver | a0: 86 |
| `0x0C` | **Sigma** | a0: 36–43 |
| `0x10` | **Zero Space 1** | a0: 69, 70, 71, 72 |
| `0x11` | **Zero Space 2** | a0: 78, 79, 80 |
| `0x19` | Dark Dizzy (alt) | a1: 4 |

Squid Adler and the Skiver/Axle alt variants carry none.

**Still unverified: the record-`id` → capsule-type mapping.** overlay-findings
§1.4 guesses `0x21` life, `0x22` large life?, `0x24/0x25` weapon energy, `0x26`
special-gfx variant — with question marks. `0x21` is the most common by far (12
of 34). This matters for naming the locations and for telling small from large
and life from weapon energy. It is resolvable from the item constructor
(`0x800535C8`) and the collect handlers (§9.3), which is where the record id must
turn into the kind byte at `obj+0x82` — **not** by guessing from the ids.

Also unresolved and worth stating plainly: **X5's freestanding capsules are
sparse because most life and weapon energy comes from enemy drops**, which are
not placement records at all. 34 is the freestanding count, and that is the
scope lx5's pickupsanity uses too — but it should be sanity-checked against
someone's memory of the game before the location table ships.


## 9.13 FINAL placement inventory — fully table-driven, all attributions proven

Supersedes §9.12 and §9.12.1's counts and their remaining uncertainty. Three
discoveries closed everything:

### (a) The overlay loader table: `0x8006FD50`

EXE data, `u8[stage*2 + area]` → ROCK_X5.BIN chunk id (0 = none/EXE-resident):

```
Intro (–,–)   Grizzly (1,–)   Dizzy (2,3)    Duff (4,–)    Mattrex (5,6)
Squid (7,–)   Izzy (8,9)      Axle (10,–)    Skiver (11,–) Dynamo (12,13)
0x0A (14,15)  0x0B (16,17)    Sigma (18,19)  0x0D (20,21)  0x0E (22,23)
0x0F (24,25)  ZS1 (26,–)      ZS2 (27,–)     duel (28,–)   stage-16 (29,–)
```

Validated three independent ways: all 8 heart anchors, the Dark Dizzy area-1
live-dump anchor (chunk3, 116 records byte-matched from
`ramdump_stage_f174001.bin`), and the **X-vs-Zero duel live-dump anchor**
(chunk28 @ `0xF3E0C`, 75 records matched from the `pre/post_zero` dumps). The
table agreed with every anchor it did not produce. **Zero Space 1 = chunk26 and
Zero Space 2 = chunk27 are proven**, closing the last inferred attributions.

Two matching notes for anyone repeating this:
- **Live lists do not byte-match the disc**: the spawner mutates records in RAM
  (`sub += 0x10` spawn mark at `0x8002B42C`, plus flags churn). Match on
  `(minor, id, x, y)` per record and wildcard bytes 0 and 3.
- The v4 "prefer the longest parse" disambiguation picked WRONG chunks (Dizzy
  a1 → chunk11's 124-record garbage over chunk3's correct 116). Plausible
  garbage parses are common at wrong deltas. Only anchors or the loader table
  decide.

### (b) Record id → item type, PROVEN from the ctor (`0x8005367C-0x80053714`)

```
id < 0x10 → kind 0 heart      id < 0x20 → kind 1 EX item
id 0x20-0x26 → kind = id - 0x1E:
  0x20 Small Life   0x21 Large Life   0x22 Full Life
  0x23 Small Weapon 0x24 Large Weapon 0x25 Full Weapon   0x26 1-UP
id 0x27/28 → kind 9 (Sub-Tanks)   0x29 → kind 0xA (W)   0x2A → kind 0xB (EX)
id 0x2B/2C → kinds 0xC/0xD (misc) id >= 0x2D → generic path
```

The overlay-findings §1.4 guesses ("0x21 life, 0x22 large life?, 0x26
special-gfx") are superseded: **0x21 is LARGE life, 0x26 is the 1-UP** (its
"special gfx" is the 1-UP sprite `0x780B`, set in the ctor). Small/large/full
amounts for weapon energy (kinds 5/6/7) are by analogy with the proven HP kinds
(heal 4 / heal 16 / heal to max); amounts unverified, identities firm.

### (c) The secondary record table (`0x80072F64`) holds NO items

Same 23-stage × 2-area layout as the primary table, lists handed to a second
spawner via `0x8002B61C` (v3 misread its entries as "alt stages 0x17-0x1F").
Every secondary list resolves and parses via the loader table — and none
contains a single `minor 0x2F` item record. **Every pickup in the game lives in
the primary table.** (A third parallel table exists at `0x80072DD4`, byte lists,
role unidentified — no item relevance found.)

### Final numbers

**33 consumable pickups** (gate 0), plus 9 real heart records (8 Heart Tanks —
Dark Dizzy's heart legitimately has TWO candidate placements in area 1 at
(2440,384)/(2440,752), also present in the live harvest; collecting one sets the
bit and the other despawns), 4 tanks, 11 never-spawning phantoms (all Axle,
gate 5), and zero EX items (Energy Ups are DNA rewards, not stage pickups —
`names.py` was right).

| stage | consumables |
|---|---|
| Intro | Large Life ×1 |
| Grizzly Slash | Large Life ×1 |
| Dark Dizzy | Large Life ×1 · Large Weapon ×1 |
| Duff McWhalen | Large Life ×1 · Small Life ×3 |
| Mattrex | Large Life ×1 · Large Weapon ×1 · 1-UP ×1 |
| Squid Adler | — |
| Izzy Glow | Large Weapon ×3 · Large Life ×1 |
| Axle the Red | Large Life ×2 |
| The Skiver | Large Life ×1 |
| Sigma | 1-UP ×1 · Large Life ×3 · Full Life ×3 · Full Weapon ×1 |
| Zero Space 1 | 1-UP ×2 · Large Weapon ×2 |
| Zero Space 2 | Large Life ×1 · Full Life ×1 · 1-UP ×1 |
| X-vs-Zero duel | — (75 records, no items) |

The count moved 26 → 34 → 33 across the session: 26 missed the endgame stages
(loop bound bug, §9.12.1); 34 included two garbage rows from wrong-chunk parses
("ZS1 secondary" and "Dark Dizzy alt", both chunk11 ghosts); 33 is the
table-driven result with every row carrying its provenance.

`Reference/mmx5-placements.csv` (v5) is the durable artifact: every item record
with stage, area, table, record index, proven type name, gate, coordinates and
source chunk.

## 9.14 Stage select FULLY MAPPED — the lock hook is one 8-byte table, `0x800F5050`

Hub overlay, all addresses valid while the hub module (base `0x800EE970`) is
resident. Derived statically from `Scripts/ramdump_hub_f22905.bin`; identical in
`ramdump_partsmenu_f23591` / `launch_f46926` / `launchfired_f49125`.

### The confirm handler `0x800EFBE8` — where a cursor slot becomes a stage id

```
800EFBE8  lhu   $a0, 0x4($a1)          ; a1 = 0x800C931C -> newly-pressed pad
800EFBF0  andi  $v1, $a0, 0x840        ; confirm buttons
800EFBF4  beqz  $v1, 800EFCE8          ;   not pressed -> cancel/other handling
800EFBFC  lb    $a0, 0x28($v0)         ; $v0 = 0x800D1C00; CURSOR = 0x800D1C28
800EFC04  bne   $a0, 8, 800EFC88       ;   slot 8 = the special entry
          ; --- slot 8: chapter/ACT decide the destination ---
          chapter(0x1D0F)==2 -> stage 0x09 (Enigma)
          chapter        ==4 -> stage 0x0A (Shuttle)
          ACT(0x1C79)    ==5 -> 0x10   ==6 -> 0x11   ==7 -> 0x12   else 0x0C
800EFC88: addiu $v0, $v0, 0x5050       ; $v0 = 0x800F5050
800EFC8C  addu  $v0, $a0, $v0
800EFC90  lbu   $v1, 0x0($v0)          ; stageId = SLOT_TO_STAGE[cursor]
800EFC98  sb    $v1, 0xc($s0)          ; 0x800D1C0C = stage id
800EFC9C  lb    $v0, 0xc($s0)
800EFCA4  beqz  $v0, 800EFD40          ; *** stage id 0 -> DO NOTHING ***
          ; else: 0x1C0D = area, play confirm SFX, advance the screen state
```

**`0x800F5050` is an 8-byte slot -> stage-id table and the confirm handler is its
only reader in the whole hub module** (verified by an exhaustive immediate scan
of `0x800EE970..0x800FA800`). Contents, and the on-screen layout from the icon
XY table `0x800F5108`:

| slot | byte | stage | boss | icon XY |
|---|---|---|---|---|
| 0 | 01 | 1 | Grizzly Slash | 0x290,0x000 |
| 1 | 05 | 5 | Squid Adler | 0x290,0x040 |
| 2 | 06 | 6 | Izzy Glow | 0x290,0x070 |
| 3 | 03 | 3 | Duff McWhalen | 0x290,0x0B0 |
| 4 | 08 | 8 | The Skiver | 0x370,0x000 |
| 5 | 07 | 7 | Axle the Red | 0x370,0x040 |
| 6 | 02 | 2 | Dark Dizzy | 0x370,0x070 |
| 7 | 04 | 4 | Mattrex | 0x370,0x0B0 |
| 8 | — | chapter/ACT | Enigma / Shuttle / Zero Space / Sigma | 0x300,0x040 |

Two columns of four plus a centre entry — the vanilla screen exactly.

**Consequence: stage locking needs NO disc patch.** Write `0` over a slot's byte
and the game's own `beqz` at `0x800EFCA4` makes confirming that icon a silent
no-op; restore the real id to unlock. Client-side, same shape as MMX4's
`ADDRESS_STAGE_ACCESS` (its `Client.py:1016` writes 9 bytes every poll). The
table is overlay data reloaded from disc on every hub entry, so the client must
re-assert it each time the hub becomes resident — and must tolerate `0x800D1C0C`
reading **0** after a blocked confirm, since `0x800EFC98` stores before the test.

### Other stage-select internals found on the way

| Address | What |
|---|---|
| `0x800D1C28` | **stage-select cursor** (0..8). Moved by `0x800EF858`: left/right wrap within a row of 4, i.e. slot 0<->3 and 4<->7 |
| `0x800F5FE0[0..8]` | per-slot **"icon already revealed"** flags for the fly-in animation — NOT access control. `0x800EF2AC` picks a random unrevealed slot every 4 frames |
| `0x800F5FE9` | number of stage-select entries: **8**, or **9** when `ACT>=5` or chapter is 2 or 4. Written by `0x800F0DC0` (all hidden), `0x800F1914` (slots 0-3), `0x800F1B0C` (slots 4-7) — the three phases of the reveal |
| `0x800F5108` | per-slot icon XY, 4 bytes/entry |
| `0x800F5194` | per-slot **weapon-bit index** `[0,4,5,2,7,6,1,3]`; `0x800EF440` tests `0x800D1C4C >> bit & 1` and picks sprite table `0x800F50B0` (beaten) over `0x800F5058` (not beaten). The same table the Parts screen uses |
| `0x800C9320` / `0x800C931C` | pad state / newly-pressed (the hub's `lui 0x800D; ... -0x6ce0` idiom) |

**Correction to overlay-findings line 216** ("stage select shows NO visual beaten
indicator, so no checkmark reader exists to patch"): a beaten reader **does**
exist — `0x800EF440` — and it swaps the icon's sprite descriptor table. The live
observation that suppressing Izzy's bit produced no visible change is still true
as an observation; the two tables evidently differ subtly, or the sprite ids
coincide. Do not cite that line as evidence that nothing reads `0x1C4C` here.

### Correction to §9.6

`0x800F26C0` is **not** a stage-select availability gate. Its enclosing function
`0x800F2560` is the stage-select **HUD/decoration** object: index byte `obj+0x2`
selects among 10 instances, index 0 spawns the other nine, and **indices 1 and 2
are the two digits of the countdown clock** — `0x800F2814` divides
`0x800D1CAC` by 216000 (60 fps x 3600) for hours, then splits tens and ones.
Index 3 is the map marker gated on `ACT>=5 && !(0x1CCB & 0x80)`, i.e. shown once
the colony has resolved *and* the shuttle launch did **not** succeed — a colony
crash-site marker, not a Zero Space entry. Indices 5-9 are positioned from the
table `0x800F54FC`. Keep §9.6's disassembly; discard its label.

### Hub top-level menu (found alongside, unrelated to stage locking)

`0x800EEDE0` builds a menu list at `0x800F6DF0` (cursor `0x800F6DF7`, count
`0x800F6DFB`): entry 0 always, then entries 1/3/2 on bits 0/2/1 of `0x800D1C4A`,
entry 5 when `ACT>=5` or the launch succeeded, entry 4 on bit 3. `0x800F111C`
commits `list[cursor]` to `0x800D1C2A`, which the Parts (`0x800F3E30`) and launch
screens read. `0x800D1C29` gates all three list builders and appears to be a
screen-mode flag.

## 9.15 DNA Parts — full name/bit map, read from the game

The 16 Parts of `0x800D1C84` (bits 2..17), paired to the mask table
`0x800F51F0` by reading the Parts screen with every bit forced on
(`Scripts/mmx5_parts_reveal.lua`, 2026-08-06). Names are the US localization
read off the screen, NOT from the web - X5 stores UI text as font-tile
indices, and web sources return Mega Man X6 Part facts for X5 queries
constantly.

| bit | slot | Part | Boss | Choice |
|---|---|---|---|---|
|  2 |  2 | Speedster        | Spiral Pegasus (The Skiver)   | Energy+ |
|  3 |  3 | Jumper           | Spiral Pegasus (The Skiver)   | Life+ |
|  4 |  4 | Hyper Dash       | Crescent Grizzly (Grizzly Slash) | Energy+ |
|  5 |  5 | W-Energy Saver   | Tidal Whale (Duff McWhalen)   | Energy+ |
|  6 |  6 | Super Recover    | Tidal Whale (Duff McWhalen)   | Life+ |
|  7 |  7 | Anti-Virus Guard | Dark Necrobat (Dark Dizzy)    | Life+ |
|  8 |  8 | Buster Plus      | Burn Dinorex (Mattrex)        | Energy+ |
|  9 |  9 | Speed Shot       | Burn Dinorex (Mattrex)        | Life+ |
| 10 |  1 | Virus Buster     | Dark Necrobat (Dark Dizzy)    | Energy+ |
| 11 | 10 | Burst Shots      | Shining Firefly (Izzy Glow)   | Life+ **X only** |
| 12 | 11 | Ultimate Buster  | Spike Rosered (Axle the Red)  | Life+ **X only** |
| 13 | 12 | Quick Charge     | Volt Kraken (Squid Adler)     | Life+ **X only** |
| 14 | 13 | Z-Saber Plus     | Spike Rosered (Axle the Red)  | Energy+ **Zero only** |
| 15 | 14 | Z-Saber Extend   | Volt Kraken (Squid Adler)     | Energy+ **Zero only** |
| 16 | 15 | Shot Eraser      | Shining Firefly (Izzy Glow)   | Energy+ **Zero only** |
| 17 |  0 | Shock Buffer     | Crescent Grizzly (Grizzly Slash) | Life+ |

**Corroboration that this is the real mapping and not a lucky alignment:**
bits 11-16 are exactly the six character-locked Parts, X's three at 11-13 and
Zero's three at 14-16. That grouping falls out of the data; nothing in the
reading procedure would have produced it by accident.


## 9.17 Live measurement session 2026-08-08 — §9.16's open questions closed

One evening of play against `Scripts/mmx5_testprep_watch.lua` plus targeted
RAM dumps. Every finding below is live-observed unless marked; full narrative
in `ai-docs/handoffs/2026-08-08_mmx5-live-session-results.md`, RAM-map
consequences already folded into `mmx5-ram-notes.md`.

### 9.17.1 The Reploid is `minor 0x04` — §9.16.4's `0x19` candidate is DEAD

A live rescue (lives 2→3, Izzy Glow area 0) fired with exactly ONE placement
record inside the match radius: `minor=0x04, id=0x00, x=384, y=651` — dx=24,
dy=0 from the player. That record byte-matches the disc list (chunk8 +
record 20). Counter-evidence against `0x19` is equally direct: Izzy area 1
carries six `0x19` records and the player saw zero rescueable NPCs there, and
Axle a0 carries three with none visible either — `0x19` is an ordinary enemy
type. This also dissolves §9.16.4's "cross-check went the wrong way": Axle's
overlay has no `0x1C45` writer because Axle simply HAS no reploids.

**Disc census of `minor==0x04`** (same §9.13 chain, all 26 stage entries):
Squid Adler a0 = **14**, Izzy Glow a0 = **14**, The Skiver a0 = **5**, all
other lists 0. Total **33**.

**GATE RULE RESOLVED, empirically, later the same night.** The rescueable
Reploids are exactly the **`gate 4, id 0x00`** records — **inverted** vs the
pickup rule (where gate≥3 means never-spawns); do not unify the two. Counts:
Squid 6 (records 60-65), Izzy 3 (20-22), Skiver 5 (37-41) — note each set is
CONTIGUOUS in its stage's list, itself corroborating a designed set. Proof:
four live rescues each overlapping its record ≤25px — including Izzy record
22 at x=3432, a Reploid the player was sure didn't exist until the data
predicted it — plus a negative control (`id 0x11` record 95px from a real
rescue, no NPC present). The 19 low-gate / id-0x10/0x11 records never
manifest on screen. Duff McWhalen's U-555 emits reploids dynamically (no
records — which is why its stage counts 0 here despite wiki reports).
Shipped as `reploid_checks` (worlds/mmx5/reploids.py); Squid's six carry the
signature but no on-screen sighting — accepted-risk call by Ivor 2026-08-08.
What remains genuinely unknown is what gates 0-2 MEAN for object records —
the spawner disassembly question stands, it just no longer blocks anything.

### 9.17.2 Stage 0x07 (Axle) has NO area 1 — a §9.16 list entry was a misread

All three tables — primary `0x80072EAC`, secondary `0x80072F64`, manifest
`0x80072DD4` — hold NULL for (0x07, 1), read live from in-stage RAM. The
player also traversed the full stage with the area byte pinned at 0. The
"only two areas with unresolved gate data" line in the backlog should have
said one (Izzy a1, now dumped clean: 62 records, 10-type manifest).

### 9.17.3 Boss code streams as per-boss modules; fingerprint at `0x800FA300`

The rush (stage 0x0C) streams the rematch Maverick's boss module to RAM base
`0x800FA000` from ROCK chunk **`29 + stage_id`** (Squid → chunk 34, proven by
byte-match against a mid-fight dump; Duff→32 and Axle→36 corroborated by
their code appearing inside stage chunks 4 and 10 respectively). ⚠️ The
module PERSISTS until the next portal replaces it — the Aug-6 corridor dumps
hold Izzy's and Dark Dizzy's modules respectively, which is also what makes
those two fingerprints live-verified alongside Squid's (3 of 8). An earlier
"unloaded after the fight" reading of the 0/99-block diff was wrong: the
after-dump differs because it holds the NEXT module, not none. The
fingerprint is **16 bytes** at `0x800FA300` (a single u32 there can be a
common instruction — collision risk with Sigma's own modules, whose dumps
match none of the 8 at 16 bytes) — full table + client protocol in ram-notes
§Boss fights. This replaces `0x1C1D` as rematch identity (same rematch read
0x05 and 0x06 in different sessions — it is a route-dependent sub-room
counter).

Mid-bosses do NOT run in the boss-HP slot `0x800920EC` (fought and killed
with the byte frozen) — §9.16.3's per-overlay wall stands for them, while
rematches escape it entirely via the client-side watcher (HP fill → 0,
persists; rush resets on stage re-entry).

### 9.17.4 Streaming vs settled — the live-read version of §9.16.1

The §9.13 tables' pointed-at overlay data streams in DURING door transitions.
Two failure modes observed live: an all-zero read (Izzy a1, 1 frame after the
area byte flipped) and — worse — a **plausible partial parse**: Axle a0 read
90 records with a valid-looking terminator while the true list is 113. A
"nonzero bytes" readiness test passed on the garbage. Only stability across
frames is a safe readiness signal for streamed data, exactly as §9.16.1's
block-awareness is for scans. (`mmx5_testprep_watch.lua` now waits on
populated data with a timeout; a stability wait is the remaining upgrade.)

### 9.17.5 Refill-queue delivery is NOT mid-gameplay

The engine never consumed the AP-queued refill (`0x1C76`) during gameplay:
frozen through HP dips, deaths, respawns, savestate loads, and a stage load
at full HP with a full sub-tank. No overcap occurred in any observed state
and nothing in `0x1C70-90` moved. The consumption moment — and the tester's
reported sub-tank overcap — remains unobserved; the untested case is a stage
load with HP below max. The overcap fix stays blocked on seeing that once.

**Vanilla economy (Ivor, 2026-08-06):** 16 Parts exist, but only **8 are
obtainable per playthrough** - each Maverick offers one of its two depending
on whether you pick Life+ or Energy+ at Alia's DNA prompt. A boss's two Parts
are NOT adjacent on the screen (Grizzly's are slots 0 and 4), so screen order
carries no boss grouping.

**Screen slot order is not bit order.** The mask table is the authority; slot
is only how the Parts menu lays them out.

# 2026-08-08 — Static analysis session 3 (offline only): object-type manifest, overlay ownership, and a scanner correction

No emulator was used. Everything below comes from the disc image and the 24
MainRAM dumps already in `Scripts/`. Purpose was to answer as much of the
feature backlog as possible without burning live-session time
(`ai-docs/plans/2026-08-08_mmx5-feature-backlog.md`).

## 9.16.0 Toolkit, and the one genuinely new capability

Extraction re-run from the recipe in §9.8: `SLUS_013.34` (534,528 bytes,
PS-EXE header says `.text` base `0x80010000`, size `0x82000`, so the EXE
occupies `0x80010000-0x80092000`) and `ROCK_X5.BIN` (1,384,448 bytes) both pull
cleanly out of the MODE2/2352 image.

**The new capability is scanning the RAM dumps, not just `SLUS_text.bin`.** A
dump carries the resident overlay as well as the EXE, so stage code becomes
visible without unpacking ROCK chunks at all. This is why previous EXE-only
scans kept returning "no references" for boss code — the code was never in the
image being searched. The 24 dumps cover stages `0x06`, `0x07`, `0x0B`, `0x0C`,
`0x0D`, `0x0F` and `0x12`.

**EXE BSS ends at `0x800EE970`; overlays stream in from `0x800EE974`.** Read
off the BSS-clear loop at `0x8005894C` (`sw $zero` from `0x80091C30` up to
`0x800EE970`), and it agrees with the constant `pickups.py` already uses for
`disc_offset = chunk_base + (list_ram - 0x800EE970)`.

## 9.16.1 METHOD CORRECTION — hi/lo scanners must respect basic blocks

**This invalidates a class of result, so it comes first.** A `lui rX,hi` +
later `op rt,off(rX)` scanner that does not model control flow will pair a
`lui` in one basic block with a store in another that is only ever reached by a
different path.

Measured on the save struct across the whole EXE: the naive scan reports **376**
accesses, the block-aware one **202**. **174 of them — 46% — were false.**

Concrete casualty: `0x8001FCD0` appeared to be a write to `save+0x4C`, i.e. the
Maverick kill record. It is not. The `lui $v0,0x800D; addiu $v0,$v0,0x1C00` that
seemed to establish its base is in a block that jumps away at `0x8001FCB4`;
`0x8001FCBC` re-bases `$v0` by `-24072` on a different path entirely.

A second, independent trap: matching on the *immediate alone*. `lbu $a0,
0x1C45($v0)` at `0x80051378` is not the lives byte — the paired `lui` is
`0x8009`, so the address is `0x80091C45`.

Rules now enforced by the scanner: stop tracking at any branch or jump; stop
when the pc is the target of a branch from elsewhere; treat
`addiu rBase,rBase,n` as moving the base rather than ignoring it.

**Any conclusion drawn from an immediate-only or non-block-aware scan should be
re-derived before it is trusted.** That includes conclusions in this document
predating this section.

## 9.16.2 `0x80072DD4` RESOLVED — the per-(stage,area) object-type manifest

§9.13(c) left this as "a third parallel table at `0x80072DD4`, byte lists, role
unidentified — no item relevance found". Its role is now read straight off
`0x8002B5B4`:

```
8002B5B4  andi $a3, $a0, 255        ; a3 = minor
8002B5C4  addiu $a1, $a1, 0x2DD4    ; a1 = 0x80072DD4
8002B5D0  lb $v0, 0x000D($v1)       ; area   (0x800D1C0D)
8002B5D4  lb $a0, 0x000C($v1)       ; stage  (0x800D1C0C)
8002B5E8  lw $v1, 0x0000($v0)       ; list = *(0x80072DD4 + stage*8 + area*4)
          ... linear search, 0xFF terminates ...
8002B60C  jr $ra                    ; returns the INDEX of the match
```

So `0x80072DD4` is a per-(stage,area) pointer to a **`0xFF`-terminated byte
list of the object-type (`minor`) values that stage instantiates**, and
`0x8002B5B4` maps a `minor` to its index in that list. The spawner consumes the
index twice: `*(0x1F800020)` table → `obj+0x3C`, and `*(0x800A8118)` table
→ `obj+0x40` (`>>7`).

Example, Izzy Glow (stage 6, area 0), manifest at `0x800F3130`:
`[0x02, 0x85, 0x04, 0x8F, 0x90, 0x91, 0x19]` — 7 types.

**Why this matters:** the set of object types per stage/area is now
enumerable statically, which is the missing half of any "make object X a
check" feature (Reploids, mid-bosses).

## 9.16.3 The EXE contains NO boss, kill-record or boss-HP code

Block-aware save-struct scan of the entire EXE: **zero accesses to
`0x800D1C4C`**, read or write. The kill record is committed by the results
overlay (`0x800EECCC`, already known from `disc.py`) and by nothing else.

Equally, no reference anywhere — EXE *or* resident overlay, in any dump — takes
boss HP `0x800920EC` as an absolute address. The 9 references to the
`0x80092090` struct are all in the EXE and none touch `+0x5C`. This
independently re-confirms the 2026-08-05 ram-notes scan with a different tool.

Save fields the **overlays** write (block-aware scan of the resident overlay,
four dumps):

| overlay | save bytes written |
|---|---|
| hub `0x0D` | `1C24 1C25 1C26 1C27 1C2B 1C2C 1C30 1C31 1C32 1CA2` |
| Izzy Glow `0x06` | `1C10-1C17, 1C24, 1C25, 1C27, 1C45, 1CA2, 1D0D` |
| Sigma / boss rush `0x0C` | `1C0F, 1C11, 1C14, 1C16, 1C1D, 1C20, 1C24, 1C25, 1CA2, 1D0D` |

Two consequences worth pinning:

- **`0x1CA2` (boss max HP) is written by overlay code** — `0x800FACBC` in both
  the Izzy Glow and hub dumps, `0x800FABEC` in the Sigma one. Same routine
  compiled into multiple overlays at different addresses, not one shared site.
- **`0x800D1C1D`'s only writer is overlay code** (`0x800EF924`, Sigma/rush
  overlay). The EXE only ever reads it.

**Consequence for mid-boss and rematch checks:** there is no shared boss-death
path in the EXE to hook. A disc stub would have to be applied **per stage
overlay** — the same wall that turned boss-HP randomization into a client-side
pin instead of a patch (§ram-notes, scan 2026-08-05). The 2026-08-05 estimate
of "pickupsanity-sized" is therefore too low; pickupsanity was one stub on one
shared dispatcher.

## 9.16.4 Reploid rescue handler located — but the `minor` is NOT proven

Traced by direct reference in `ramdump_stage_f284694.bin` (Izzy Glow, stage 6
area 0), which is the stage where the two live rescues of 2026-07-31 were done:

- **`0x800F167C` — the rescue itself.** Requires a collision test
  (`jal 0x8002E804`), then **lives (`0x800D1C45`) += 1, clamped to 9**, then
  sound 21 (`jal 0x80016490`), then a 1-of-4 random pick
  (`jal 0x8002DF78`, `& 3`) indexing `0x800F3E04` into `0x800F12EC` — the
  thank-you animation.
- called from `0x800F14D8`, which is entry **1** of a 6-entry state table at
  `0x800F3E1C`
- that table's owner/update function is `0x800F146C`
- `0x800F146C` is the only overlay pointer in a 7-entry hook table whose other
  six entries are `jr $ra` no-op stubs in the EXE (`0x800586B4 + 8*i`)

This confirms the rescue effect the overlay-findings recorded (lives +1, no
persistent record) and locates the code, which was previously unknown.

**What is NOT established: the reploid's `minor`.** The hook table's base is
under-determined by ±1 word — several candidate bases satisfy the
stub-progression constraint, exactly the "plausible garbage parse" hazard
§9.13 warns about. If the base is `0x800F3804` the index is 6 and the minor is
**`0x19`**, which is attractive: `0x19` occurs exactly once in Izzy Glow area
0's record list. But it is not confirmed, and one cross-check went the wrong
way — Axle the Red's overlay (stage `0x07` area 0) contains **no** write to
`0x1C45` at all, despite its manifest also listing `0x19`. Either `0x19` is
not the reploid, or Axle's reploids are in area 1 (not covered by any dump).

**Cheapest way to close it** (one short BizHawk session): stand next to a
reploid in Izzy Glow and read the live object's `+0x01`; or capture a dump of
Izzy Glow area 1 and of stage `0x07` area 1. Do NOT build on `0x19` before
that.

## 9.16.5 Game-mode byte `0x800D1C00` — EXE writers enumerated, mode `0x04` identified

Every store to the mode byte in the EXE, found base-agnostically so the list is
complete for the EXE (7 total):

| site | value written |
|---|---|
| `0x8001DD0C` | `3` |
| `0x8001DD30` | `0x13` |
| `0x8001E4A4` | `0` |
| `0x8001E4FC` | `0` |
| `0x8001FC54` | `3` |
| `0x8001FC68` | `3` |
| `0x80034FC8` | `0x0B` |

So the EXE only ever writes `0`, `3`, `0x0B` and `0x13`. **Modes `0x0A`, `0x0C`,
`0x04`, `0x10`, `0x11`, `0x14` and `0x15` are written by overlay code**, which
is why they could never be found in the EXE.

Observed values across the 24 dumps, context taken from what each capture was
(so this is **[LIVE]**, not inference):

| mode | context |
|---|---|
| `0x04` | **hub / stage select / Parts menu / launch menu** (stage `0x0D`) — **NEW**, absent from the previously documented set |
| `0x0A` | in-stage gameplay (stages `0x06`, `0x07`, `0x0C`, `0x12`) |
| `0x0C` | stage `0x0F` |
| `0x11` | credits |
| `0x14` | story cutscene (stage `0x0B`) |

**Client relevance:** the gameplay gate is `mode in (0x0A, 0x0C)`. The hub is
`0x04`, so the gate excludes the hub by construction rather than by accident —
one of the two guards that the 0.3.2 review flagged as resting on an asserted
whitelist now has a measured basis. Still unmeasured: the title/data-select
walk, and which mode holds while ACT steps on a Zero Space clear.

## 9.16.6 Independent re-derivation of the placement inventory

The 2026-08-05 static extraction was re-run from scratch with the new tools and
**agrees exactly**: Axle the Red (stage `0x07` area 0) has precisely **11 item
records with spawn gate 5**, ids `0x00`-`0x02` (heart-range), which can never
spawn — the spawner rejects `gate > armor level` (`0x800D1CA0`, which reads `1`
in all 24 dumps) and rejects `gate >= 3` outright at `0x8002AFC0`. Izzy Glow
area 0 (2 item records) and Sigma area 0 (8 item records) are all gate 0.

That is an end-to-end validation of disc extraction → loader table → list table
→ record parse against a previously published result, using an independently
written parser.

**Pickupsanity safety check, partial:** no pickupsanity location in the three
stages readable from dumps carries a nonzero spawn gate, so none of them can be
silently unspawnable. Worth completing for the remaining stages once the ROCK
chunks are unpacked — a gated pickupsanity location would be an unobtainable
check, the exact failure class that stranded a seed on 2026-08-06.

## 9.16.7 Record byte 3 has no spare bits

Relevant to giving the pickupsanity stub an "already checked" marker. Record
byte 3 is fully occupied: the **low nibble is the spawn gate** (compared against
`0x800D1CA0` at `0x8002AFCC`, rejected outright if `>= 3` at `0x8002AFC0`) and
the **high nibble is a runtime state machine** — `0x8002B3F0`-`0x8002B42C`
tests it against `0x30`, `0x10` and `0x50` and writes it back. There is no free
bit to borrow.

The workable alternative needs no spare bit: only one stage's list is live at a
time, so the client can write a per-stage bitmap into EXE free space at stage
entry, and the stub can index it with
`(recptr - *(0x80072EAC + stage*8 + area*4)) / 8` — roughly six instructions,
using a table the client already reads.
