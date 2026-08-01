> Research notes mirrored from the mmx5-ap-research workspace (2026-08-01).
> Working copies live there and are updated as addresses are confirmed;
> re-sync this mirror when they change. No game data included.

# Mega Man X5 (SLUS-01334, NTSC-U) â€” Ghidra static analysis: player HP / damage structures

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
  repo â€” only the model (same as MMX6's ROCK_X6).
- A raw MIPS-pattern scan over all 47 MB of `ROCK_X5.DAT` found **zero**
  `lui 0x8009/0x800A/0x800D`+offset pairs, while the same scanner found dozens
  in the EXE â€” the DAT's chunks (which contain nested `(offset,size)`
  sub-tables) evidently hold **compressed** code/data. Carving overlay code
  would require reversing the decompressor first (see Â§7).
- Useful confirmed globals from `game.toml` (widescreen work): 0x8009A1F8 = BG
  layer struct array, 0x800A51A8 = tile ring, 0x800D1DBC = map size â€” i.e. the
  0x8009xxxx/0x800Dxxxx region is the engine's static BSS, not overlay-owned.

## 3. The player object: fixed struct at 0x8009A0A0

The EXE materializes `0x8009A0A0` (`lui 0x800A; addiu reg, -0x5F60`) in ~100
places. It is the **player object**, a fixed-address instance of the engine's
generic object struct (same layout used by enemies/bosses â€” e.g. an object
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

### Field map (base P = 0x8009A0A0) â€” all verified in disassembly

| Offset | Address | Size | Meaning | Evidence |
|---|---|---|---|---|
| +0x02 | 0x8009A0A2 | s8 | **Character index** (0 = X, nonzero = Zero) | added to 0x800D1C00 before reading max HP at +0x47 â†’ 0x800D1C47 (X) / 0x800D1C48 (Zero), matching the known cheat addresses |
| +0x04/05/06 | 0x8009A0A4.. | u8 | state bytes; +5 = action state (0x11 = hurt/knockback, written by FUN_80038d44; dispatched via jump table `PTR_800745f0` in FUN_800352a8) | |
| +0x2F | 0x8009A0CF | u8 | state byte (user-verified; clearedâ€¦ note FUN_800352a8 clears +0xCF=0x8009A16F each frame, a different field) | |
| **+0x5C** | **0x8009A0FC** | **u8** | **Authoritative current HP.** Bit 7 = "damage event" flag (value is always masked `& 0x7F` when read). `0x80` exactly = death sentinel | see Â§4 |
| +0x60 | 0x8009A100 | u8 | contact damage this object deals (generic object field; on enemies this is what hits you) | FUN_8002ecb0 |
| **+0x61** | **0x8009A101** | **u8** | **Mercy-invincibility (i-frame) timer**, frames | see Â§5 |
| +0x63 | 0x8009A103 | u8 | hit-type index (1 = normal hitâ€¦) â€” indexes knockback velocity table 0x80074778 and i-frame duration table 0x80074818 | FUN_80038d44 |
| +0x70/+0x71 | 0x8009A110/11 | u8 | hit flags (collision writes +0x71; merged each frame: `P+0x89 = P+0x70 \| P+0x71` then cleared) | FUN_800352a8 |
| +0x79/+0x7A | 0x8009A119/1A | u8 | spike/instadeath contact flag(+0x79) / immunity flag (+0x7A==1 blocks it) | FUN_800389e8 |
| +0x89 | 0x8009A129 | u8 | merged damage flags; `(x&3)==3` or `(x&0xC)==0xC` = crushed/instadeath, other combos = normal hit | FUN_800389e8 |
| +0xA4 | 0x8009A144 | u8 | hurt-blink flag; set 1 on hit, cleared when i-frame timer expires | FUN_80038d44 / 0x80038C74 |
| +0xF8 | 0x8009A198 | u8 | post-hit knockback/hit-stun timer; set to **0x4B** on hit, decremented once per frame in FUN_800352a8 before damage resolution | 0x80038AE0, 0x8003530C |
| +0xF9 | 0x8009A199 | u8 | **pending incoming damage amount** for this frame (written by collision code from attacker+0x60) | 0x8002EF5C, 0x800328A8 |
| +0x14B/+0x14C | 0x8009A1EB/EC | s8/u32 | virus/DoT state: +0x14B < 0 â†’ every 0x12C frames HP -= 2 (X only) | FUN_8003a1fc |
| +0x154 | 0x8009A1F4 | u8 | virus-hit timer, set 0x4B | FUN_80039bf0 |

+0x5D (0x8009A0FD) = displayed HP-bar value chasing +0x5C (user-verified; the
HUD writer for it was not located in the EXE â€” likely overlay HUD code).

## 4. Authoritative HP â€” 0x8009A0FC, with bit-7 semantics

Every HP mutation found in the EXE operates **directly on P+0x5C**; there is no
second storage it is recomputed from (consistent with the user's full-RAM scan
finding no other copy):

- **Damage resolution** â€” `FUN_800389e8(P)` (0x800389E8), called once per frame
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
- **Pit/scroll kill** â€” `FUN_80029184`: sets `DAT_8009a0fc = 0x80` directly
  (hardcoded), `dmg_stat += old & 0x7F`.
- **Heal/refill** â€” `FUN_80034140` (0x80034140): drains the queued-refill
  counters `0x800D1C76` (X) / `0x800D1C77` (Zero) (value `& 0x7F`, bit 7 =
  active flag â€” sub-tank/pickup heals), incrementing P+0x5C by 1 per tick,
  clamped to max HP = `s8 [0x800D1C00 + charIdx + 0x47]`.
- **Full heal** â€” `FUN_80039bf0`: `P+0x5C = [0x800D1C00+charIdx+0x47]`.
- **Virus DoT** â€” `FUN_8003a1fc`: `P+0x5C -= 2` every 300 frames when infected.

**Max HP: `0x800D1C47` (X) / `0x800D1C48` (Zero)** â€” confirmed both by the
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
Identity of the frame-writer observed live: **unverified** (see Â§7).

## 5. Mercy invincibility (i-frames) â€” timer at 0x8009A101 (P+0x61)

- **Set on hit** in `FUN_80038d44` (0x80038D44, hit-reaction/knockback starter;
  contains the "Walk Through Walls" cheat patch sites 0x80038EEC):
  ```c
  *(u8*)(P+0x61) = (&DAT_80074818)[hitType];   // 0x80038EC0
  ```
  Duration table at **0x80074818** (bytes): `00 4B 64 00 4B 64 64 64 64 64 ...`
  â†’ normal hit = 0x4B (75 frames), heavy hits = 0x64 (100 frames).
- **Decremented once per frame** at 0x80038C54..64 inside `FUN_800389e8`; on
  the 1â†’0 transition the blink flag P+0xA4 is cleared (0x80038C74) and
  `FUN_8003c5d8` restores the sprite.
- **Damage gate:** the enemy-contact collision routines begin with
  ```
  8002E278: lb   $v0, 0x61(player)     8002E40C: lb $v0, 0x61(player)
  8002E280: bnez $v0, <skip-all>       8002E414: bnez $v0, <skip-all>
  ```
  i.e. **nonzero P+0x61 = completely intangible to contact damage** (no hit
  flags get set at all). The spike/instadeath path in `FUN_800389e8` also
  requires `P+0x61 == 0` (`P+0x79 != 0 && P+0x61 == 0 && P+0x7A != 1` â†’ kill).
- Cleared on death/respawn (0x8003E2EC) and in state resets (0x800373ACâ€¦).

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
  0xB8) â€” incremented at 0x800292E0, 0x800318DC, 0x80031B1C, 0x80038A4C/80,
  0x80038B10/88, 0x80038BE0. Matches the user's live finding (freezing it
  cannot stop HP loss â€” it is written *after* HP, never read back into HP).
- **Global gates**: `0x800D1C10` nonzero = damage/status processing skipped
  (pause/cutscene); `0x800D1C1C` set to 1 on player death.
- **No pointer chase needed**: the player object is at the fixed address
  0x8009A0A0 in this build (all collision writes are hardcoded).
- **Boss HP 0x800920EC** (user-verified): consistent with a boss object based
  at 0x80092090 (+0x5C = 0x800920EC); note that region is *above* end-of-text
  0x80092000, i.e. overlay/BSS-resident â€” offsets +0x5C (HP) and +0x60 (contact
  damage) are generic object fields engine-wide.

## 7. What remains unverified / next steps

1. **The live-observed per-frame rewriter of 0x8009A0FC.** Not in the static
   EXE. Next step: in BizHawk (Nymashock), Lua
   `event.on_bus_write(cb, 0x8009A0FC)` (or the debugger's write breakpoint)
   and log the PC â€” expect an address in the 0x800Fxxxx overlay range. If so,
   the overlay chunk can be captured live (savestate RAM dump) and carved into
   Ghidra at that address; static carving from ROCK_X5.DAT is blocked on its
   (unreversed, apparently compressed) chunk format.
2. **HUD writer of 0x8009A0FD** (display bar) â€” not located in EXE; assumed
   overlay HUD code. Harmless for our purposes.
3. Whether lava/environment damage (overlay code at 0x800F2AB0/0x800F6C3C)
   respects the P+0x61 gate â€” the existence of a separate "lava" cheat suggests
   it may bypass contact collision entirely. Test in-game with recipe below.
4. ROCK_X5.DAT chunk compression format (needed only for full static overlay
   analysis; the EXE presumably contains the loader/decompressor â€” finding the
   function that walks the DAT's (sector,size) table is the entry point).

## 8. Recommended Lua invincibility recipe (BizHawk, MainRAM domain = addr âˆ’ 0x80000000)

Primary (clean, engine-native â€” makes the game treat you as in mercy-frames):

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
Write HP *without* bit 7 set and â‰¤ maxHP. If the overlay frame-writer still
reverts it, run step Â§7.1 to find and NOP that writer (or accept the +0x61
method, which prevents damage from ever being queued).

Do **not** write 0x8009A0CF (breaks movement â€” it is a state byte, despite
cheat sites listing it as health).

---

### Artifacts kept in scratchpad (session-local)
`extract_iso.py`, `scan_refs.py`/`scan_refs2.py` (MIPS lui/imm effective-address
scanner), `disasm.py` (capstone), Ghidra project `MMX5.gpr` +
`ghidra_scripts/DecompTargets*.java`, extracted disc files.
