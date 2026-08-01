> Research notes mirrored from the mmx5-ap-research workspace (2026-08-01).
> Working copies live there and are updated as addresses are confirmed;
> re-sync this mirror when they change. No game data included.

# Mega Man X5 (NTSC-U, SLUS-01334) â€” RAM Map for Archipelago

Verified working reference for the AP integration. Addresses are PS1 addresses
(`0x80xxxxxx`); BizHawk "MainRAM" domain offset = address âˆ’ 0x80000000.
Research tooling: `Scripts/mmx5_ramwatch.lua` (diff logger â†’ `Scripts/mmx5_log.txt`).
Disassembly detail: `mmx5-ghidra-findings.md`. History of how each fact was
established: `ai-docs/handoffs/`.

Legend: âœ… = verified in-emulator/disassembly Â· âš ï¸ = partially verified / caveat Â·
â“ = unverified hypothesis (from cheat archives or single observation)

> **2026-07-31 stub-validation update:** `0x800D1C41` is NOT a reliable
> gameplay-time stage id â€” the pickup stub read **0xE4** from it mid-stage in
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
> controller** (+0: 0x0A gameplay / 0x0C results â€” use as client gate);
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
| `0x800D1C45` | u8 | Lives (default 0x02 on continue) | âœ… |
| `0x800D1C47` | u8 | **Max HP â€” X** (base 0x20; +2 per heart tank) | âœ… |
| `0x800D1C48` | u8 | Max HP â€” Zero (per Ghidra; char-selected) | âš ï¸ |
| `0x800D1C4C` | u8 | **Weapons owned bitfield** (persistent), ammo-slot order. Confirmed: bit0 C-Shot, bit1 Dark Hold, bit5 F-Laser (Izzy kill 2026-07-31: 0x03â†’0x23 at results commit â€” validates the inferred ammo-slot order). Remaining inferred: bit2 Goo Shaver, bit3 Ground Fire, bit4 Tri-Thunder, bit6 Spike Ball, bit7 Wing Spiral. Written at results screen ~25s after boss death. The Izzy results ALSO granted Zero's C-Flasher + the Laser Device (Enigma part) with NO other save-struct bit changing â†’ one boss bit appears to drive all three rewards (X weapon / Zero technique / Enigma part) â€” big implication for randomization design | âœ…/âš ï¸ |
| `0x800D1C79` | u8 | **Story ACT counter** (not just intro-clear): 0â†’1 at intro victory; launch resolution writes 5 on Eurasia destruction; results tail checks `< 5`. Treat as act progression | âœ… upgraded 2026-07-31 |
| `0x800D1C7F` | u8 | Tank ownership bitfield (sub/W/spare-life tanks); 0xFF grants all (menu shows them). As u16 0x0D1C7E bits 12â€“15; stage attribution (harvest 2026-07-31): bit12 Sub-Tank #1 = Grizzly Slash, bit13 Sub-Tank #2 = Dark Dizzy (harvest-confirmed 2026-07-31), bit14 W-Tank = The Skiver, bit15 EX-Tank = Izzy Glow â€” **tank map COMPLETE** | âœ… write-tested |
| `0x800D1C52/53` | u16 | **Max weapon energy** (+2 per "Energy Up"; 0x3230 observed after one) | âœ… |
| `0x800D1C80` | u8 | **Heart tanks collected bitfield â€” COMPLETE** (placement harvest 2026-07-31): bit0 Grizzly Slash, bit1 Squid Adler, bit2 Izzy Glow (live-verified), bit3 Duff McWhalen, bit4 The Skiver, bit5 Axle the Red (unique ungated record + elimination; stage also has 11 phantom heart records gated on nonexistent armor level 5), bit6 Dark Dizzy (live-verified), bit7 Mattrex. NOT stageIdâˆ’1 order. Izzy live pickup: X max HP +2 same frame, Zero's max HP (0x0D1C48) unchanged â†’ supports per-character hearts | âœ… |
| `0x800D1C83` | u8 | **Energy-Up/EX collected bitfield** (bit1 set by Dynamo-sortie DNA reward) | âœ… (bit 1) |
| `0x800D1C84/86` | u16Ã—2 | "Parts bitfields" per cheat archive â€” did NOT change on DNA part award; labels dubious | â“ |
| `0x800D1CA0` | u16 | Armor parts bitfield (Falcon/Gaea); 0xFFFF grants all | âœ… write-tested |
| `0x800D1CAA` | u8 | Decremented 0x04â†’0x03 at Izzy results commit (same frame as weapons bitfield). Hypothesis: hours-until-collision or sorties-remaining counter â€” candidate rival to the cheat-archive 0x0D1CAE claim | â“ new obs. 2026-07-31 |
| `0x800D1CAC` | u32 | **Countdown timer in FRAMES**; one hour = 0x34BC0 (216,000 = 60 fps Ã— 3600). Hub overlay hourly-tick handler subtracts an hour at 0x800EFF18; an hour-RESTORE site at 0x800F01D8 adds one back (Dynamo/event candidate). Old "0x1CAC/AD u16 + 0x1CAE u16 hours" = low/high halves of this u32 | âœ… decoded 2026-07-31 |
| `0x800D1CB0â€“B3` | u32? | Clear-time counter (constant tick; logger-muted) | âœ… ticks |
| `0x800D1CB4` | u8 | Slow event counter, unidentified | â“ |
| `0x800D1CB8` | u16 | Damage-taken ranking stat (+dmg per hit; health pickups subtract; reset per level). NOT the health variable â€” freezing it does not stop HP loss | âœ… |
| `0x800D1CC2â€“C5` | s8Ã—4 | **Launch-power accumulators** (bumped at results screens): Enigma/shuttle success score = 2Ã—(their sum) + s8 0x1CCA (overlay-findings Â§11) | âœ… 2026-07-31 |
| `0x800D1CCA` | s8 | Launch-score modifier (Dynamo-sortie results adjust by 0x14; zeroed when a launch fires) | âœ… |
| `0x800D1CCB` | u8 | Launch state: 1 = attempted, bit7 = SUCCESS (Eurasia destroyed) | âœ… |
| `0x800D1CC7/C9` | u8 | Counters bumped at results/DNA screens, unidentified | â“ |
| `0x800D1CD1` | u8 | bit7 toggles during play â€” noise? | â“ |
| `0x800D1D0F` | u8 | **Story chapter** (not just a sortie tally): hub fn 0x800EEF14 advances it on popcount(0x800D1C4C) â€” 2 boss kills â†’ chapter 2 (Enigma event), 6 â†’ chapter 4 (shuttle). Endgame gating hangs off this â€” see overlay-findings Â§10 | âœ… 2026-07-31 |
| `0x800D1C1D` | u8 | Launch-event state byte: 0 â†’ 4 when the Enigma firing cutscene starts (mode 0x14, stage id 0x0B) | âš ï¸ single obs. |
| `0x800D1D28â€“2A` | u8Ã—3 | **Pending DNA-reward buffer**: written at the DNA-select screen (observed `C0 4B 03` after choosing a Life Up at an Izzy kill), delivered + zeroed at the NEXT results sequence â€” even a stage-escape results (observed 2026-07-31: +2 max HP and hearts-u32 bit 13 = Life Up id 5 = stageâˆ’1 applied on escape-exit). Supersedes "Dynamo consumes 0x0D1D38" as the general mechanism | âœ… |
| `0x800D1C88â€“9F` | â€” | Suspected reploid-rescue bitfields (overlay analysis) â€” **DISPROVEN as rescue record**: 2 live Izzy Glow rescues + the results commit wrote NOTHING here (2026-07-31). Rescue effect = lives +1 (0x0D1C45) only. No persistent rescue record exists in the save struct â†’ Reploid checks need live per-stage spawn-slot detection with the AP server as the permanent record | âŒ disproven |
| `0x800D1D0F` | u8 | Increments per stage completion ("stages cleared" count?) | âš ï¸ |
| `0x800D1D38â€“3A` | 3Ã—u8 | **Pending DNA-reward buffer**: written at DNA select (C0 4B 03 = "weapons and energy"), zeroed when the reward is granted after the next sortie (Dynamo fight â†’ Energy Up) | âœ… |
| `0x800D1D0F` | u8 | Sorties-completed counter (increments for mavericks AND Dynamo fights) | âœ… |
| `0x800D1CAA` | u8 | Decremented after Dynamo sortie (05â†’04) â€” encounters-remaining? countdown-linked? | â“ |
| `0x800D1C41` | u8 | Changed 02â†’09 entering Dynamo sortie â€” stage/mode id? | â“ |

Related globals (Ghidra): pause gate `0x800D1C10`, death flag `0x800D1C1C`.

## Player object (FIXED base `0x8009A0A0`) â€” live, volatile

Valid only during active gameplay (holds garbage in menus/transitions).

| Address | Offset | Meaning | Status |
|---|---|---|---|
| `0x8009A0A2` | +0x02 | Character index (X / Zero) | âš ï¸ Ghidra |
| `0x8009A0FC` | +0x5C | **Current HP** (authoritative per Ghidra: all damage/heal paths RMW this byte; bit7 = "just damaged", 0x80 = death sentinel). âš ï¸ Live experiments: naive Lua writes appeared not to stick / caused hit-loops â€” unresolved discrepancy (suspected overlay writer); treat as read-mostly until re-tested | âš ï¸ |
| `0x8009A0FD` | +0x5D | Displayed health bar (chases 0xA0FC) | âœ… |
| `0x8009A101` | +0x61 | **Mercy i-frame timer**: nonzero â‡’ contact collision skipped entirely incl. spike death. Set from table `0x80074818` (0x4B normal / 0x64 heavy), âˆ’1/frame. **God mode: pin to 2 every frame â€” verified working** | âœ… |
| `0x8009A198` | +0xF8 | Knockback timer | âš ï¸ Ghidra |
| `0x8009A199` | +0xF9 | Pending damage (written by attacker collision) | âš ï¸ Ghidra |

## Live weapon block `0x8009A140`â€“`0x8009A17F` â€” volatile

**Zeroed on death AND stage exit.** Client must re-assert grants from the save
struct, or rely on the game's own restore (stage load repopulates from 0x0D1C4C).

| Address | Meaning | Status |
|---|---|---|
| `0x8009A148`â€“`0x8009A167` | 16 ammo slots, u16 each, max 0x0120 (X's 8 + Zero's 8; order: C-Shot/DarkHold/GooShaver/GroundFire/TriThunder/F-Laser/SpikeBall/WingSpiral interleaved per char) | âœ… |
| `0x8009A169` | Live weapons-owned bitfield (0xFF = all usable immediately; restored from 0x0D1C4C on stage load) | âœ… write-tested |
| `0x8009A16E` | Death timer (8â†’0) | âœ… |
| `0x8009A170`â€“`0x176` | Menu/HUD state bytes | âœ… observed |

## Other verified

| Address | Meaning | Status |
|---|---|---|
| `0x800920EC` | u16 â€” Active boss HP (zero = instant kill; works on intro boss + mavericks) | âœ… |
| `0x800D4F56/58/64/65/66/6C` | ~~gameplay gate~~ **DISPROVEN**: 00 during Izzy Glow gameplay â€” stage-specific event/menu enables, not a general in-gameplay flag. Client uses save-struct sanity (max HP 0x10â€“0x40) as its write gate instead | âŒ |
| `0x800C931C/1E` | Controller input bitfield | â“ (cheat archive) |
| `0x801FEE80`â€“`0x801FEFFF` | **CPU stack** â€” any "matching" values here are call-frame temporaries, never state | âœ… |

## Engine facts that shape the AP client

1. **Write persistent, read live.** Grants â†’ save struct (`0x0D1Cxx`); check
   detection â†’ save struct bits; the live block self-restores on stage load.
2. Results screen (not the kill moment) commits weapon/boss state â€” detection of
   a boss kill should watch `0x0D1C4C` and tolerate the ~25s delay.
3. `0x9Axxx` region is garbage outside gameplay â€” gate all access on the
   `0x800D4F5x` gameplay flags.
4. Overlay code (`ROCK_X5.DAT`, compressed) occupies `0x800Fxxxx`+ â€” code-patch
   addresses from cheat archives are only valid while the right overlay is loaded.
5. Cheat-archive labels are unreliable: 0x0D1C4A "boss flags" (wrong â€” never
   changes), 0x8009A0CF "HP" (wrong â€” state byte), parts bitfields (dubious).
   Trust only âœ… rows.

## Open questions

- [x] Heart-tank stageâ†’bit map â€” COMPLETE 2026-07-31 (see 0x800D1C80 row). Energy-Up (EX item) stage map still open: EX items live in later stage areas, not captured by entry-area harvest â€” upgraded harvester will catch them during normal play
- [ ] Weapon bitfield bitâ†’boss map beyond bits 0â€“1 â€” kill remaining 6 mavericks
- [ ] Does granting a weapon in 0x0D1C4C make the stage count as "beaten"
      (stage select / ending gates)? Critical for goal logic.
- [ ] Real parts storage (0x0D1D38+ hypothesis) + what 0x0D1C84/86 actually are
- [ ] Armor capsule pickup: which bits in 0x0D1CA0 per capsule; does armor
      activate immediately or need stage re-entry?
- [ ] Sub/W/E-tank pickup events (which bit in 0x0D1C7F per pickup location)
- [ ] Zero's weapon/technique grants (same 0x0D1C4C or separate?)
- [ ] 0x0D1C79 intro flag â€” reconfirm; relation to 0x0D1D0F counter
- [ ] Memory-card save format vs RAM struct (persistence verification)
- [ ] Resolve 0x8009A0FC write-discrepancy (overlay writer? re-test with
      event.on_bus_write to catch the writer PC)
- [ ] Enigma/shuttle RNG state addresses (needed for countdown-mechanic options)
