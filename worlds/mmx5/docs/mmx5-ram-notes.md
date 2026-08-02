> Research notes mirrored from the mmx5-ap-research workspace (2026-08-01).
> Working copies live there and are updated as addresses are confirmed;
> re-sync this mirror when they change. No game data included.

# Mega Man X5 (NTSC-U, SLUS-01334) — RAM Map for Archipelago

Verified working reference for the AP integration. Addresses are PS1 addresses
(`0x80xxxxxx`); BizHawk "MainRAM" domain offset = address − 0x80000000.
Research tooling: `Scripts/mmx5_ramwatch.lua` (diff logger → `Scripts/mmx5_log.txt`).
Disassembly detail: `mmx5-ghidra-findings.md`. History of how each fact was
established: `ai-docs/handoffs/`.

Legend: ✅ = verified in-emulator/disassembly · ⚠️ = partially verified / caveat ·
❓ = unverified hypothesis (from cheat archives or single observation)

> **2026-07-31 stub-validation update:** `0x800D1C41` is NOT a reliable
> gameplay-time stage id — the pickup stub read **0xE4** from it mid-stage in
> Grizzly Slash (live, proto v3). Its 02/06/09 readings were hub/menu-time.
> Use **`0x800D1C0C`** (the spawn engine's stage input, 1=Grizzly..8=Skiver,
> also the "Level Modifier" cheat's target) for in-stage identity; stub v4
> reads it. Community cheat archive now mirrored at `mmx5-cheat-archive.md`
> (confirms 0x1CA0 armor-parts u16, 0x1C84/86 parts, 0x1C7F tank byte,
> 0x0D4F5x = pause-menu row enable flags, 0x9A0C4/C6 = player velocity words).

> **2026-07-30 late-session update:** the overlay-dump analysis
> (`mmx5-overlay-findings.md`) supersedes several entries below. Key corrections:
> `0x800D1C80` is a **u32** (bits 0-7 hearts / 8-15 DNA Life-Ups / 16-23 EX /
> 24-31 DNA Energy-Ups; heart bit index is placement-data-driven: Dizzy=6,
> Izzy=2); `0x800D1C84` (u32) = **DNA parts owned** (mystery solved); tanks are
> bits 12-15 of u16 `0x800D1C7E`; `0x800D1C41` IS the selected stage (earlier
> live disproof was savestate contamination); `0x800D1C00` = **game-mode
> controller** (+0: 0x0A gameplay / 0x0C results — use as client gate);
> `0x800D1C26/27` = just-completed sortie + result (patchless kill detection);
> weapon-grant hook at `0x800EECBC/CC` (results overlay, re-streamed per use);
> AP mailbox candidate `0x801FA000`; `0x800D1C88-9F` suspected reploid-rescue
> bitfields (unverified). Consult the overlay findings before acting on
> anything in this file.

## Persistent save struct (base ~0x800D1C44)

Survives death and stage exit; the AP client's primary read/write surface.
**Items granted by AP should be written HERE, not to live-state mirrors.**

| Address | Size | Meaning | Status |
|---|---|---|---|
| `0x800D1C45` | u8 | Lives (default 0x02 on continue) | ✅ |
| `0x800D1C47` | u8 | **Max HP — X** (base 0x20; +2 per heart tank) | ✅ |
| `0x800D1C48` | u8 | Max HP — Zero (per Ghidra; char-selected) | ⚠️ |
| `0x800D1C4C` | u8 | **Weapons owned bitfield** (persistent), ammo-slot order. Confirmed: bit0 C-Shot, bit1 Dark Hold, bit5 F-Laser (Izzy kill 2026-07-31: 0x03→0x23 at results commit — validates the inferred ammo-slot order). Remaining inferred: bit2 Goo Shaver, bit3 Ground Fire, bit4 Tri-Thunder, bit6 Spike Ball, bit7 Wing Spiral. Written at results screen ~25s after boss death. The Izzy results ALSO granted Zero's C-Flasher + the Laser Device (Enigma part) with NO other save-struct bit changing → one boss bit appears to drive all three rewards (X weapon / Zero technique / Enigma part) — big implication for randomization design | ✅/⚠️ |
| `0x800D1C79` | u8 | **Story ACT counter** (not just intro-clear): 0→1 at intro victory; launch resolution writes 5 on Eurasia destruction; results tail checks `< 5`. Treat as act progression | ✅ upgraded 2026-07-31 |
| `0x800D1C7F` | u8 | Tank ownership bitfield (sub/W/spare-life tanks); 0xFF grants all (menu shows them). As u16 0x0D1C7E bits 12–15; stage attribution (harvest 2026-07-31): bit12 Sub-Tank #1 = Grizzly Slash, bit13 Sub-Tank #2 = Dark Dizzy (harvest-confirmed 2026-07-31), bit14 W-Tank = The Skiver, bit15 EX-Tank = Izzy Glow — **tank map COMPLETE** | ✅ write-tested |
| `0x800D1C52/53` | u16 | **Max weapon energy** (+2 per "Energy Up"; 0x3230 observed after one) | ✅ |
| `0x800D1C80` | u8 | **Heart tanks collected bitfield — COMPLETE** (placement harvest 2026-07-31): bit0 Grizzly Slash, bit1 Squid Adler, bit2 Izzy Glow (live-verified), bit3 Duff McWhalen, bit4 The Skiver, bit5 Axle the Red (unique ungated record + elimination; stage also has 11 phantom heart records gated on nonexistent armor level 5), bit6 Dark Dizzy (live-verified), bit7 Mattrex. NOT stageId−1 order. Izzy live pickup: X max HP +2 same frame, Zero's max HP (0x0D1C48) unchanged → supports per-character hearts | ✅ |
| `0x800D1C83` | u8 | **Energy-Up/EX collected bitfield** (bit1 set by Dynamo-sortie DNA reward) | ✅ (bit 1) |
| `0x800D1C84/86` | u16×2 | "Parts bitfields" per cheat archive — did NOT change on DNA part award; labels dubious | ❓ |
| `0x800D1CA0` | u16 | Armor parts bitfield (Falcon/Gaea); 0xFFFF grants all | ✅ write-tested |
| `0x800D1CAA` | u8 | Decremented 0x04→0x03 at Izzy results commit (same frame as weapons bitfield). Hypothesis: hours-until-collision or sorties-remaining counter — candidate rival to the cheat-archive 0x0D1CAE claim | ❓ new obs. 2026-07-31 |
| `0x800D1CAC` | u32 | **Countdown timer in FRAMES**; one hour = 0x34BC0 (216,000 = 60 fps × 3600). Hub overlay hourly-tick handler subtracts an hour at 0x800EFF18; an hour-RESTORE site at 0x800F01D8 adds one back (Dynamo/event candidate). Old "0x1CAC/AD u16 + 0x1CAE u16 hours" = low/high halves of this u32 | ✅ decoded 2026-07-31 |
| `0x800D1CB0–B3` | u32? | Clear-time counter (constant tick; logger-muted) | ✅ ticks |
| `0x800D1CB4` | u8 | Slow event counter, unidentified | ❓ |
| `0x800D1CB8` | u16 | Damage-taken ranking stat (+dmg per hit; health pickups subtract; reset per level). NOT the health variable — freezing it does not stop HP loss | ✅ |
| `0x800D1CC2–C5` | s8×4 | **Launch-power accumulators** (bumped at results screens): Enigma/shuttle success score = 2×(their sum) + s8 0x1CCA (overlay-findings §11) | ✅ 2026-07-31 |
| `0x800D1CCA` | s8 | Launch-score modifier (Dynamo-sortie results adjust by 0x14; zeroed when a launch fires) | ✅ |
| `0x800D1CCB` | u8 | Launch state: 1 = attempted, bit7 = SUCCESS (Eurasia destroyed) | ✅ |
| `0x800D1CC7/C9` | u8 | Counters bumped at results/DNA screens, unidentified | ❓ |
| `0x800D1CD1` | u8 | bit7 toggles during play — noise? | ❓ |
| `0x800D1D0F` | u8 | **Story chapter** (not just a sortie tally): hub fn 0x800EEF14 advances it on popcount(0x800D1C4C) — 2 boss kills → chapter 2 (Enigma event), 6 → chapter 4 (shuttle). Endgame gating hangs off this — see overlay-findings §10. **Live 2026-08-01: reads 0x03 while standing in Zero Space 1**, so the endgame does NOT simply continue the 2/4 ladder — the colony resolution sets its own chapter. Do not assume monotonic chapter == progress | ✅ 2026-07-31, endgame value ⚠️ single obs. |
| `0x800D1C0C` (Zero Space) | u8 | **Zero Space stage 1 = stage id `0x10`** — live-read 2026-08-01 standing in the Shadow Devil stage (mode 0x0A). The older "0x0A-0x0C = Zero Space" note in overlay-findings was a GUESS and is wrong. Consequence for the client: Zero Space records arrive with an unmapped stage byte and are correctly ignored by `STAGE_ID_TO_NAME` | ✅ live 2026-08-01 |
| `0x800D1C1D` | u8 | Launch-event state byte: 0 → 4 when the Enigma firing cutscene starts (mode 0x14, stage id 0x0B) | ⚠️ single obs. |
| `0x800D1D28–2A` | u8×3 | **Pending DNA-reward buffer**: written at the DNA-select screen (observed `C0 4B 03` after choosing a Life Up at an Izzy kill), delivered + zeroed at the NEXT results sequence — even a stage-escape results (observed 2026-07-31: +2 max HP and hearts-u32 bit 13 = Life Up id 5 = stage−1 applied on escape-exit). Supersedes "Dynamo consumes 0x0D1D38" as the general mechanism | ✅ |
| `0x800D1C88–9F` | — | Suspected reploid-rescue bitfields (overlay analysis) — **DISPROVEN as rescue record**: 2 live Izzy Glow rescues + the results commit wrote NOTHING here (2026-07-31). Rescue effect = lives +1 (0x0D1C45) only. No persistent rescue record exists in the save struct → Reploid checks need live per-stage spawn-slot detection with the AP server as the permanent record | ❌ disproven |
| `0x800D1D0F` | u8 | Increments per stage completion ("stages cleared" count?) | ⚠️ |
| `0x800D1D38–3A` | 3×u8 | **Pending DNA-reward buffer**: written at DNA select (C0 4B 03 = "weapons and energy"), zeroed when the reward is granted after the next sortie (Dynamo fight → Energy Up) | ✅ |
| `0x800D1D0F` | u8 | Sorties-completed counter (increments for mavericks AND Dynamo fights) | ✅ |
| `0x800D1CAA` | u8 | Decremented after Dynamo sortie (05→04) — encounters-remaining? countdown-linked? | ❓ |
| `0x800D1C41` | u8 | Changed 02→09 entering Dynamo sortie — stage/mode id? | ❓ |

Related globals (Ghidra): pause gate `0x800D1C10`, death flag `0x800D1C1C`.

## Player object (FIXED base `0x8009A0A0`) — live, volatile

Valid only during active gameplay (holds garbage in menus/transitions).

| Address | Offset | Meaning | Status |
|---|---|---|---|
| `0x8009A0A2` | +0x02 | Character index (X / Zero) | ⚠️ Ghidra |
| `0x8009A0FC` | +0x5C | **Current HP** (authoritative per Ghidra: all damage/heal paths RMW this byte; bit7 = "just damaged", 0x80 = death sentinel). ⚠️ Live experiments: naive Lua writes appeared not to stick / caused hit-loops — unresolved discrepancy (suspected overlay writer); treat as read-mostly until re-tested | ⚠️ |
| `0x8009A0FD` | +0x5D | Displayed health bar (chases 0xA0FC) | ✅ |
| `0x8009A101` | +0x61 | **Mercy i-frame timer**: nonzero ⇒ contact collision skipped entirely incl. spike death. Set from table `0x80074818` (0x4B normal / 0x64 heavy), −1/frame. **God mode: pin to 2 every frame — verified working** | ✅ |
| `0x8009A198` | +0xF8 | Knockback timer | ⚠️ Ghidra |
| `0x8009A199` | +0xF9 | Pending damage (written by attacker collision) | ⚠️ Ghidra |

## Live weapon block `0x8009A140`–`0x8009A17F` — volatile

**Zeroed on death AND stage exit.** Client must re-assert grants from the save
struct, or rely on the game's own restore (stage load repopulates from 0x0D1C4C).

| Address | Meaning | Status |
|---|---|---|
| `0x8009A148`–`0x8009A167` | 16 ammo slots, u16 each, max 0x0120 (X's 8 + Zero's 8; order: C-Shot/DarkHold/GooShaver/GroundFire/TriThunder/F-Laser/SpikeBall/WingSpiral interleaved per char) | ✅ |
| `0x8009A169` | Live weapons-owned bitfield (0xFF = all usable immediately; restored from 0x0D1C4C on stage load) | ✅ write-tested |
| `0x8009A16E` | Death timer (8→0) | ✅ |
| `0x8009A170`–`0x176` | Menu/HUD state bytes | ✅ observed |

## Other verified

| Address | Meaning | Status |
|---|---|---|
| `0x800920EC` | u16 — Active boss HP (zero = instant kill; works on intro boss + mavericks) | ✅ |
| `0x800D4F56/58/64/65/66/6C` | ~~gameplay gate~~ **DISPROVEN**: 00 during Izzy Glow gameplay — stage-specific event/menu enables, not a general in-gameplay flag. Client uses save-struct sanity (max HP 0x10–0x40) as its write gate instead | ❌ |
| `0x800C931C/1E` | Controller input bitfield | ❓ (cheat archive) |
| `0x801FEE80`–`0x801FEFFF` | **CPU stack** — any "matching" values here are call-frame temporaries, never state | ✅ |

## Engine facts that shape the AP client

1. **Write persistent, read live.** Grants → save struct (`0x0D1Cxx`); check
   detection → save struct bits; the live block self-restores on stage load.
2. Results screen (not the kill moment) commits weapon/boss state — detection of
   a boss kill should watch `0x0D1C4C` and tolerate the ~25s delay.
3. `0x9Axxx` region is garbage outside gameplay — gate all access on the
   `0x800D4F5x` gameplay flags.
4. Overlay code (`ROCK_X5.DAT`, compressed) occupies `0x800Fxxxx`+ — code-patch
   addresses from cheat archives are only valid while the right overlay is loaded.
5. Cheat-archive labels are unreliable: 0x0D1C4A "boss flags" (wrong — never
   changes), 0x8009A0CF "HP" (wrong — state byte), parts bitfields (dubious).
   Trust only ✅ rows.

## Open questions

- [x] Heart-tank stage→bit map — COMPLETE 2026-07-31 (see 0x800D1C80 row). Energy-Up (EX item) stage map still open: EX items live in later stage areas, not captured by entry-area harvest — upgraded harvester will catch them during normal play
- [ ] Weapon bitfield bit→boss map beyond bits 0–1 — kill remaining 6 mavericks
- [x] Does granting a weapon in 0x0D1C4C make the stage count as "beaten"
      (stage select / ending gates)? **YES — ANSWERED 2026-08-01.** The hub fn
      0x800EEF14 derives the story chapter 0x800D1D0F from popcount(0x1C4C),
      and a save with 0x1C4C = FF walked the full colony-resolution → Zero
      Space → Sigma path to the credits. The bitfield IS the endgame gate,
      which is exactly why the AP patch must never suppress its commit (it
      moves capability to 0x1C4D instead). Caveat: stage select shows no
      per-stage beaten indicator, so nothing reads it for UI.
- [ ] Real parts storage (0x0D1D38+ hypothesis) + what 0x0D1C84/86 actually are
- [x] Armor capsule pickup: which bits in 0x0D1CA0 per capsule; does armor
      activate immediately or need stage re-entry? **ANSWERED 2026-08-01.**
      Bits are in 0x1CA1 (0x1CA0 low byte is the armor LEVEL), one per capsule
      via maskTable[id] at 0x8007C370, and **capsule id == part index** (live:
      Whale = id 1 = Falcon Body, Necrobat = id 4 = Gaea Head). Activation is
      NOT immediate: the results overlay sets the set-completion flag
      (0x1C4A |= 2/4) at the next results screen once a nibble fills, and only
      then is the armor offered at character select — gated additionally by
      the 0x1CCC ack latch. See §3.1.
- [ ] Sub/W/E-tank pickup events (which bit in 0x0D1C7F per pickup location)
- [ ] Zero's weapon/technique grants (same 0x0D1C4C or separate?)
- [ ] 0x0D1C79 intro flag — reconfirm; relation to 0x0D1D0F counter
- [ ] Memory-card save format vs RAM struct (persistence verification)
- [ ] Resolve 0x8009A0FC write-discrepancy (overlay writer? re-test with
      event.on_bus_write to catch the writer PC)
- [ ] Enigma/shuttle RNG state addresses (needed for countdown-mechanic options)

## Endgame / Zero Space — live capture 2026-08-01

Groundwork for (a) Sigma victory detection and (b) treating endgame stage
clears / boss kills as future AP locations.

**Stage ids (0x800D1C0C)** — the old "0x0A-0x0C = Zero Space" note was a guess
and is WRONG:

| id | stage | how observed |
|---|---|---|
| `0x0C` | **Sigma stage** (final) | live read on entry, mode 0x0A |
| `0x10` | Zero Space 1 (Shadow Devil) | live read, mode 0x0A |
| `0x12` | Zero Space stage with the **X vs Zero** duel | pre/post-fight dumps |

⚠️ **Endgame stage ids are NOT contiguous.** Play order was
0x10 → (0x11?) → 0x12 → **0x0C**, so the natural guess "0x13 = Sigma" is
wrong. Never infer an endgame id from sequence — read 0x800D1C0C on entry.
(This also partially rehabilitates the old "0x0A-0x0C Zero Space" note: 0x0C
IS an endgame stage. That range was just incomplete, not purely wrong, and it
does not cover 0x10/0x12.) `0x11` still unread.

**Game modes (0x800D1C00)** — beyond the known 0x0A gameplay / 0x0C results:
the stage-entry sequence logged as `0A→0B→0C→0E→12→03→04→07→08→09→0A`, and
**after the Zero duel was won: `0A→13→14`**. Mode `0x14` is the same mode the
Enigma firing cutscene uses (see 0x800D1C1D row), so 0x14 = "story cutscene"
generally. Endgame bosses do NOT route through the 0x0C results screen at all,
which is why the existing patchless kill detect (mode 0x0C + sortie id 1-8)
cannot see them.

### ✅ SIGMA VICTORY DETECTION — SOLVED **AND LIVE-VALIDATED** 2026-08-01

**End-to-end proof (2026-08-01 23:02):** loaded a savestate from just before the
Sigma kill, landed the final blow, mode walked `0A→13→14` then (≈4700 frames /
78 s of cutscene later) `14→10→11`. The client fired `CLIENT_GOAL`, the server
committed it (smoke.apsave 3870→4010 bytes, written the same minute), and AP
auto-released the slot's remaining items — that release only happens on a
genuine goal status, so it is independent confirmation the server processed it,
not just a client-side log line.
⚠️ **The cutscene delay is real**: ~78 seconds elapse between the kill
(`13→14`) and the ending modes. Do not conclude the detection failed during
that window — wait for `14→10`.

Five RAM dumps bracketing a real Sigma kill (fight start ×2, post-kill,
cutscene, credits) plus the mode log give the full sequence after the final
blow:

```
0x0A → 0x13 → 0x14 → 0x10 → 0x11 (credits, holds)
```

- `0x13` / `0x14` are **generic story-cutscene modes** — the X-vs-Zero duel
  produces them too, so they are NOT usable as a victory signal alone.
- **`0x10` and `0x11` appeared only after Sigma**, and `0x11` persists through
  the credits. These are the ending. Client: `ENDING_MODES = {0x10, 0x11}`.
- `0x0D` = **death / game-over screen** (seen oscillating 0A↔0D during failed
  attempts) — deliberately excluded from the ending set.
- Corroborating state in the credits dump: stage id → `0x0F` (transition),
  0x800D1C1D launch-event → 0x00.

Implemented in `worlds/mmx5/client.py`: the check runs at the TOP of
`game_watcher`, deliberately BEFORE the save-struct gate, because the gate
only admits modes 0x0A/0x0C and would otherwise swallow the goal for the
entire ending.

**Other bytes that latched across the kill** (stable in both pre dumps, changed
by post and held through credits) — candidates if a more durable marker is ever
wanted, none yet disambiguated:

| addr | change | note |
|---|---|---|
| `0x800D1CC0` | 11 → 60 | |
| `0x800D1CA2` | 50 → 7F | |
| `0x800D1CBC` | 01 → 07 | Zero duel moved it 00 → 05 — looks like a progressing event id, not a boolean |
| `0x800D1C1C` | 00 → 01 | ALSO moved across the Zero duel ⇒ **not Sigma-specific**; this is the suspected DeathLink flag and must be disambiguated before use |

**Candidate defeat markers** — bytes that changed across the Zero duel
(dump `pre_zero_f3239321` taken at fight start, `post_zero_f3243474` right
after the kill, both still mode 0x0A so the cutscene had not yet run):

| addr | change | note |
|---|---|---|
| `0x800D1C1C` | 00 → 01 | also the suspected DeathLink damage/death flag — disambiguate before trusting |
| `0x800D1C2A` | 00 → 01 | |
| `0x800D1CB4` | 00 → 01 | |
| `0x800D1CBC` | 00 → 05 | value 5, not a boolean — counter or id? |

Ignore `0x800D1CAC/AD` in that diff: that is the frame countdown ticking.

⚠️ The post-kill dump was taken BEFORE the `0A→13→14` transition, so it does
not capture whatever the cutscene commits. **For Sigma, dump a third time
AFTER the mode settles** — the persistent marker most likely lands there.

**If endgame clears become AP locations**, the detection shape is probably
(stage id, mode transition) rather than the results-screen path used for
mavericks — see the mode note above.
