> Research notes mirrored from the mmx5-ap-research workspace (2026-08-08).
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

> **2026-08-08 live-session update:** four corrections land in this file today.
> (1) `0x800D1C1D` is a sub-room counter, NOT a rematch identifier — the same
> rematch read 0x05 and 0x06 in different sessions; rematch identity now comes
> from the boss-module fingerprint u32 at `0x800FA300` (§Boss fights).
> (2) Rematch checks need NO disc stub — boss HP `0x800920EC` reaches 0 visibly
> and persists, and the rush resets on stage re-entry (both live-proven).
> (3) The Reploid object type is **`minor 0x04`**, proven by a live rescue that
> byte-matches the disc; the `0x19` candidate is dead. Census: 33 records
> (Squid 14 / Izzy 14 / Skiver 5). (4) Mid-bosses do NOT use the boss-HP slot.

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
| `0x800D1C79` | u8 | **Story ACT counter** (not just intro-clear): 0→1 at intro victory; launch resolution writes 5 on Eurasia destruction; results tail checks `< 5`. Treat as act progression. **THIS IS THE ENDGAME GATE: ACT >= 5 is what makes Zero Space appear on stage select.** Live-verified 2026-08-04 - poking ACT from 5 down to 2 removed Zero Space from a save that had it, and restoring it brought it back. The story-chapter ladder does NOT gate access (see overlay-findings 10). **TRAINING MODE writes `0x0A` here** — out of band vs the campaign range, and it lands in the SAME frame as max HP `0x20`, so a "is a save resident" test alone cannot tell training from a real save. Campaign value read live off a 3-boss save: `0x02`. See §Training mode below | ✅ live 2026-08-03 |
| `0x800D1C7F` | u8 | Tank ownership bitfield (sub/W/spare-life tanks); 0xFF grants all (menu shows them). As u16 0x0D1C7E bits 12–15; stage attribution (harvest 2026-07-31): bit12 Sub-Tank #1 = Grizzly Slash, bit13 Sub-Tank #2 = Dark Dizzy (harvest-confirmed 2026-07-31), bit14 W-Tank = The Skiver, bit15 EX-Tank = Izzy Glow — **tank map COMPLETE** | ✅ write-tested |
| `0x800D1C52/53` | u16 | **Max weapon energy** (+2 per "Energy Up"; 0x3230 observed after one) | ✅ |
| `0x800D1C80` | u8 | **Heart tanks collected bitfield — COMPLETE** (placement harvest 2026-07-31): bit0 Grizzly Slash, bit1 Squid Adler, bit2 Izzy Glow (live-verified), bit3 Duff McWhalen, bit4 The Skiver, bit5 Axle the Red (unique ungated record + elimination; stage also has 11 phantom heart records gated on nonexistent armor level 5), bit6 Dark Dizzy (live-verified), bit7 Mattrex. NOT stageId−1 order. Izzy live pickup: X max HP +2 same frame, Zero's max HP (0x0D1C48) unchanged → supports per-character hearts | ✅ |
| `0x800D1C83` | u8 | **Energy-Up/EX collected bitfield** (bit1 set by Dynamo-sortie DNA reward) | ✅ (bit 1) |
| `0x800D1C84` | **u32** | **DNA Parts owned bitfield — CONFIRMED IN CODE 2026-08-05.** Hub-overlay Parts screen (fn `0x800F3E30`) does `lw 0x84($s0)` and ANDs it with `maskTable[0x800F51F0][selected]`; blank slot if zero, draw part if set. **16 parts = bits 2..17** (mask table is 16 single-bit entries). The old "did NOT change on DNA part award" observation was a TIMING artifact: no gameplay writer exists in the static EXE (only save load `0x8001C964`/`0x8001CC90`, save store `0x8001CFA0`), because DNA rewards are BUFFERED and delivered at the *next results screen* (`0x1D28-2A`/`0x1D38-3A`). Recheck across a results screen, not across the award prompt. `0x1C86` is simply the u32's high half | ✅ code 2026-08-05 |
| `0x800D1C88–9F` | 6×u32 | Persisted (save file `+0x08..+0x1F`, block-copied by the save loader `0x8001C904`) but **ZERO individual field references in the static EXE or the hub overlay** — nothing reads or writes them by field. Disproven as reploid-rescue record (see below). Any consumer must live in another overlay (stage code). Candidate for a per-stage/area "visited" record, unproven either way — not decidable statically from the images we hold | ❓ 2026-08-05 |
| `0x800D1CA0` | u16 | Armor parts bitfield (Falcon/Gaea); 0xFFFF grants all | ✅ write-tested |
| `0x800D1CA2` | u8 | **BOSS MAX HP — live-PROVEN 2026-08-05.** Pinned to 40 with the AP client attached ⇒ the next boss spawned with exactly 40 max HP (fill ramp shortened 73f → 38f to match); vanilla read 75 ⇒ 75 HP. Also the Boss-Level accumulator: fn `0x80024594` does `0x1CA2 = min(0x1CA2 + level_raw, 0x7F)` at each stage start, which is *how* bosses gain HP across a run. Range 1..0x7F. Memcard-persisted. **This is the lever for boss-HP randomization** — one save-struct byte, no polling. ⚠️ It is ALSO consumed as `(value − 0x20) / 2` at `0x800259E0`, `0x8002617C` (EXE) and `0x800F7564` (hub, fns `0x80025828` / `0x80026080`) — those consumers are unidentified, so overriding it may move something besides HP. The DNA reward tier is believed to key on `0x1CC0` (a separately computed byte) and our DNA checks ride the KILL, not the reward, so checks cannot be stranded either way | ✅ live 2026-08-05 |
| `0x800920EC` boss-HP **fill ramp** | — | A boss's intro bar-fill writes `0x800920EC` **+1 per frame** from 1 to max (75 frames for a 75-HP boss). Any client-side write to live boss HP during the intro is overwritten every frame; the earliest safe pin is ~10 frames after the fill stops climbing. Irrelevant if `0x1CA2` is used instead, which is why it is preferred | ✅ live 2026-08-05 |
| `0x800D1CAA` (+charIdx) | u8×2 | **Hunter Rank index, per character** — indexes the rank-modifier table `0x800717EC` in the Boss Level formula. Index runs **best-first**: 0 = MEH/MMH (+16), 1 = PA (+8), 2 = GA (+4), 3 = SA (+2), 4–7 = A/B/C/E (+0). Supersedes the earlier "decremented 0x04→0x03 … hours/sorties counter" guess | ✅ code 2026-08-05 |
| `0x800D1CC0` | u8 | **Computed Boss Level** = `min(level_raw + 1, 0x60)`, written by fn `0x80024594` (sites `0x80024574`/`0x80024588`/`0x8002465C`). **No reader in the EXE or hub** ⇒ consumed by overlay code. Pinning this would set difficulty *directly*, instead of indirectly via the countdown | ✅ code 2026-08-05 |
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
| `0x800D1C1D` | u8 | **Sub-room / segment id — NOT a boss identifier. CORRECTED 2026-08-08.** The 2026-08-06 reading ("holds the Maverick's stage id during a rematch") is refuted: the SAME Squid Adler rematch read `0x05` on 2026-08-06 and `0x06` on 2026-08-08 (player-confirmed squid both times), and Axle the Red's own-stage boss room ALSO reads `0x06`. It tracks the current sub-room and its arena value is route-dependent: rush corridors read `0x10/0x13/0x14`, post-kill `0x0C/0x0E/0x0F`, Izzy's post-midboss warp stepped `0x00→0x01`. Useful as a "you changed rooms" signal only. Rematch identity comes from the boss-module fingerprint instead (see §Boss rush) | ✅ corrected 2026-08-08 |
| `0x800D1C79` (endgame) | u8 | **ACT doubles as the Zero Space progress counter.** Confirmed live 2026-08-06, one step per clear: Zero Space 1 `5->6` (f323080), Zero Space 2 `6->7` (f341110), X vs Zero `7->8` (f353000), and it continues to `9`. The hub confirm handler `0x800EFC0C` reads it to pick the destination (5->0x10, 6->0x11, 7->0x12, else 0x0C). Basis for the `endgame_checks` locations | ✅ live 2026-08-06 |
| `0x800D1CB4` | u8 | **Fast per-stage counter — NOT a progress record.** Ran `04->05->08->09->0A->0B->0C->0D->0E` during ordinary play in one stage and resets to 0 on stage entry. Logged 1208 changes in one session. Mistaken for a boss-rematch tally once; check its history before reading meaning into a single step | ⚠️ noise, identified 2026-08-06 |
| Zero Space boss rematches | — | **NO persistent defeat record exists** (full-RAM before/after diff across two rematch kills, 2026-08-06: nothing latches — `0x1C2F` moved on one kill and not the other, `0x1CB4` is a general counter, `0x1C25`/`0x1C1C` toggle rather than set). **2026-08-08: a disc stub is NOT needed after all — the client-side watcher route is live-proven.** A rematch runs in the standard boss-HP slot `0x800920EC` (Squid: fill to 58, stepped to 0 on the kill, and **0 persisted 600+ frames** until the room transition — comfortably poll-visible). Portal state survives death-respawn within the visit but the whole rush RESETS on a full stage exit + re-entry (portal live again, player-confirmed), so a missed check is always refightable. Boss identity comes from the module fingerprint, not `0x1C1D` (see §Boss rush) | ✅ watcher route proven 2026-08-08 |
| `0x800D1C0C` (Zero Space) | u8 | **Zero Space stage 1 = stage id `0x10`** — live-read 2026-08-01 standing in the Shadow Devil stage (mode 0x0A). The older "0x0A-0x0C = Zero Space" note in overlay-findings was a GUESS and is wrong. Consequence for the client: Zero Space records arrive with an unmapped stage byte and are correctly ignored by `STAGE_ID_TO_NAME` | ✅ live 2026-08-01 |
| `0x800D1C1D` | u8 | **SUB-ROOM / SEGMENT ID** (superseded the "launch-event state byte" reading; the 0→4 Enigma observation was one value of it). ~~In the rush it holds the Maverick's stage id~~ — refuted 2026-08-08, see the corrected row above: same rematch produced `0x05` and `0x06` across sessions, so it cannot identify a boss. Values seen across the 24 dumps: `00, 02, 04, 0C, 10, 11, 15`; live 2026-08-08 added `01, 02` (Izzy segments), `06` (two different boss rooms), `0F, 13, 14` (rush). **Its ONLY writer is overlay code** (`0x800EF924`, Sigma/rush overlay); the EXE only reads it (2 sites, block-aware scan 2026-08-08) | ✅ corrected 2026-08-08 |
| `0x800D1D28–2A` | u8×3 | **Pending DNA-reward buffer**: written at the DNA-select screen (observed `C0 4B 03` after choosing a Life Up at an Izzy kill), delivered + zeroed at the NEXT results sequence — even a stage-escape results (observed 2026-07-31: +2 max HP and hearts-u32 bit 13 = Life Up id 5 = stage−1 applied on escape-exit). Supersedes "Dynamo consumes 0x0D1D38" as the general mechanism | ✅ |
| `0x800D1C88–9F` | — | Suspected reploid-rescue bitfields (overlay analysis) — **DISPROVEN as rescue record**: 2 live Izzy Glow rescues + the results commit wrote NOTHING here (2026-07-31). Rescue effect = lives +1 (0x0D1C45) only. No persistent rescue record exists in the save struct → Reploid checks need live detection with the AP server as the permanent record. **2026-08-08: the rescue HANDLER is located** (`0x800F167C`, Izzy overlay, collision test → lives +1 clamped to 9 → sound 21) **and the Reploid's `minor` is PROVEN = `0x04`**: a live rescue fired the lives-up with exactly one placement record under the player (dx=24, dy=0), and that record byte-matches the disc (Izzy a0, x=384, y=651). The old `0x19` candidate is DEAD — it is an ordinary enemy type (6 in Izzy a1 where the player saw zero rescueable NPCs, 3 in Axle a0 — no reploids there either, which also explains Axle's overlay having no `0x1C45` writer). **Disc census of `minor==0x04` records: Squid Adler a0 = 14, Izzy Glow a0 = 14, The Skiver a0 = 5, everywhere else 0 — 33 total. GATE RULE RESOLVED (later the same night): the REAL rescueable Reploids are exactly the `gate 4, id 0x00` records — Squid 6, Izzy 3, Skiver 5, 14 total — INVERTED vs the pickup rule (gate≥3 = never-spawn for pickups, gate 4 = real for reploids; do not unify).** Proof: 4 live rescues each overlapping its record ≤25px (Izzy records 20/21/22 incl. one at x=3432 the player didn't know existed, Skiver 37), plus an `id 0x11` record 95px from a real rescue with no NPC present. The 19 low-gate / id-0x10/0x11 records never manifest. Duff McWhalen's U-555 mid-boss also emits reploids dynamically — no records, not locations. Shipped as `reploid_checks` (Squid's 6 by accepted risk, same signature, no on-screen sighting) | ✅ gate rule proven 2026-08-08 |
| `0x800D1D0F` | u8 | Increments per stage completion ("stages cleared" count?) | ⚠️ |
| `0x800D1D38–3A` | 3×u8 | **Pending DNA-reward buffer**: written at DNA select (C0 4B 03 = "weapons and energy"), zeroed when the reward is granted after the next sortie (Dynamo fight → Energy Up) | ✅ |
| `0x800D1D0F` | u8 | ~~Sorties-completed counter (increments for mavericks AND Dynamo fights)~~ **REFUTED 2026-08-03** — it is the STORY CHAPTER (see the 0x800D1D0F row above). Live: it held at 3 across TWO complete stage-plus-results sequences in one session (`mmx5_chapter_gate_log.txt`), so it does not tally sorties. The early coincidence that made this look like a counter is that chapter and kill count track each other at the start — the chapter-1 rung literally stores the popcount as the chapter number. Do not reason about progress from this byte as if it counted anything. | ❌ refuted |
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
| `0x800920EC` | **u8 — Active boss CURRENT HP**, with `0x800920ED` = displayed-bar mirror chasing it (same pairing as the player's +0x5C/+0x5D). The old "u16" label came from the kill-boss cheat writing both bytes at once; corrected 2026-08-05 from `ramdump_pre_sigma` (`50 50` = Sigma at 80 HP). Zero = instant kill; works on intro boss + mavericks | ✅ (u8 corrected 2026-08-05) |
| — boss object | **NOT based at 0x80092090** — that inference in `mmx5-ghidra-findings.md` §6 is WRONG. The struct at 0x80092090 has live fields at +0x00/03/08/0C/50/54/68/70 and **nothing in the static EXE ever touches +0x5C**. Boss HP is written by per-boss OVERLAY code, which is why a full-EXE scan finds zero references. Consequence for AP: boss-HP randomization cannot be a disc patch (it would need one patch per stage overlay) — it has to be a client-side pin | ✅ scan 2026-08-05 |
| `0x800D4F56/58/64/65/66/6C` | ~~gameplay gate~~ **DISPROVEN**: 00 during Izzy Glow gameplay — stage-specific event/menu enables, not a general in-gameplay flag. Client uses save-struct sanity (max HP 0x10–0x40) as its write gate instead | ❌ |
| `0x800C931C/1E` | Controller input bitfield | ❓ (cheat archive) |
| `0x801FEE80`–`0x801FEFFF` | **CPU stack** — any "matching" values here are call-frame temporaries, never state | ✅ |

## Engine facts that shape the AP client

0. **Memory layout (static, 2026-08-08).** EXE `.text` = `0x80010000`–
   `0x80092000` (`0x82000`, from the PS-EXE header). **EXE BSS ends at
   `0x800EE970`; stage/hub overlays stream in from `0x800EE974` upward** — read
   off the BSS-clear loop at `0x8005894C`, and the same constant `pickups.py`
   uses for its disc-offset arithmetic. Practical consequence: **an EXE-only
   disassembly cannot see boss code, stage object code, or most save-struct
   writers.** Scan the RAM dumps in `Scripts/` instead — each carries the
   resident overlay. See ghidra-findings §9.16.
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
- [x] Real parts storage + what 0x0D1C84/86 actually are — **ANSWERED 2026-08-05
      (static analysis).** `0x800D1C84` IS the u32 DNA Parts bitfield, 16 parts
      in bits 2..17; proven by the hub Parts screen `0x800F3E30` masking it
      against table `0x800F51F0`. The `0x0D1D38+` hypothesis is dead — that is
      the pending-DNA-reward buffer, which is also *why* `0x1C84` looked inert
      at award time. See `mmx5-ghidra-findings.md` §9.1.
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
- [x] 0x0D1C79 intro flag — **RESOLVED 2026-08-03** (live): it is the story
      ACT counter and Training mode stamps `0x0A` into it. Relation to
      0x0D1D0F still unexamined.
- [ ] Memory-card save format vs RAM struct (persistence verification)
- [ ] Resolve 0x8009A0FC write-discrepancy (overlay writer? re-test with
      event.on_bus_write to catch the writer PC)
- [ ] Enigma/shuttle RNG state addresses (needed for countdown-mechanic options)

## Boss Level formula (game mechanic, 2026-08-02)

Recalculated at the START OF EACH STAGE. Mainly scales boss HP; does not change
attack patterns or damage.

**Base, from HOURS REMAINING on the collision countdown** (u32 0x800D1CAC):

| hours left | 16-17 | 14-15 | 12-13 | 10-11 | 8-9 | 6-7 | 4-5 | 2-3 | 0-1 |
|---|---|---|---|---|---|---|---|---|---|
| base | 1 | 3 | 5 | 7 | **9** | 11 | 13 | 15 | 17 |

**Modifiers:**
- **+1 per Maverick defeated** (max +8)
- **Hunter Rank** of the character in use: E/C/B/A +0, SA +2, GA +4, PA +8,
  MEH/MMH +16
- **+1 per Special Weapon/Technique owned** (max +8) — ignored when fighting
  Dynamo, and while using Gaea Armor

### The actual function — `0x80024594` (disassembled 2026-08-05)

The table above came from community sources. This is what the code does:

```
level_raw = 2 * floor(elapsed / 432000)          ; 432000 frames = 2 h
          + popcount(player+0xC9)                ; weapons byte (copy of 0x1C4C)
          + rankTable[ 0x800D1CAA + charIdx ]    ; table 0x800717EC, u16
elapsed   = 0x34BC00 - 0x800D1CAC                ; 0x34BC00 = 16 h in frames
            (clamped >= 0)
0x800D1CC0 = min(level_raw + 1, 0x60)            ; the Boss Level, 96 cap
0x800D1CA2 = min(0x800D1CA2 + level_raw, 0x7F)   ; accumulator, 127 cap
```

Two corrections this forces on the prose above:

1. **The rank table index runs best-first.** `0x800717EC` = `[+16, +8, +4, +2,
   0, 0, 0, 0]`, so index 0 is MEH/MMH and index 7 is E. The *values* were
   right; the implied ordering was backwards.
2. **"+1 per Maverick" and "+1 per weapon" are ONE term in code**, not two —
   a single popcount of the weapons byte, which is also the Maverick-kill
   record. Do not model them as separable.

The hours→base table is reproduced exactly by `2 * floor(elapsed / 2h) + 1`.

**Reward thresholds:** level **4+** → Life Up / Energy Up choice; level **8+**
→ Life+ / Energy+ choice, which ALSO grants an equippable Part.
**Easy mode locks every boss at Level 1** ⇒ no Life/Energy Ups and no Parts at
all. (This is why speedrunners deliberately burn hours early — dying out of a
stage back to stage select — to raise the base before the first bosses.)

### AP consequences

- **The countdown pin (8 h) fixes the base at 9**, which is above BOTH
  thresholds — so on a pinned seed every boss offers the level-8+ tier
  (Life+/Energy+ AND a Part). The prompt can never fail for time reasons.
- **Bosses still scale despite the freeze**: base is fixed but +1/Maverick and
  +1/weapon keep climbing, roughly level 9 on the first boss to ~25 on the
  last. Freezing the countdown does NOT flatten difficulty.
- **Easy mode would have broken prompt-based DNA detection completely**
  (level 1 ⇒ no prompt ⇒ 8 unobtainable checks). The client checks DNA
  locations off the BOSS KILL instead, so it is immune — worth remembering
  before anyone "improves" that back to reading the reward.
- Verified against a live reading: The Skiver at **level 19** with the
  countdown pinned at 8 h ⇒ base 9 + 5 Mavericks + 5 weapons = 19. ✓
- Level 8+ also grants **equippable DNA Parts** (u32 0x800D1C84, §3.3) — an
  entire reward stream we do not model. Candidate future locations.

## Boss fights, the rush, and the refill queue — live session 2026-08-08

Source: `Scripts/mmx5_testprep_watch.lua` log + `ramdump_squid_rematch_f430014.bin`
(mid-fight, player-confirmed Squid Adler) + disc analysis. Handoff:
`ai-docs/handoffs/2026-08-08_mmx5-live-session-results.md`.

### Boss HP slot `0x800920EC` (mirror `0x800920ED`)

- **Real Maverick fights use it, both in their own stage and in the rush.**
  Axle (own stage): fill ramp to 53, stepped down per hit, `3→0` on the kill.
  Squid (rush rematch): fill to 58, stepped to 0. The displayed-bar mirror
  chases one step behind.
- **HP 0 PERSISTS after the kill** — Squid's zero held 600+ frames until the
  room transition; Axle's held minutes. A client poll cannot miss a kill that
  happens while it is connected. This is the basis of client-side rematch checks.
- **Mid-bosses do NOT use this slot** (Izzy's mid-boss fought and killed with
  the byte frozen on a stale value the whole time). Mid-boss HP lives in the
  generic enemy object pool — client-side mid-boss detection needs different
  work, and the cheap watcher explicitly does NOT extend to them.
- Outside fights the byte holds **stale garbage** (leftover 16 observed at
  stage entry). Gate any use on a observed fill ramp or a known fight state.

### Rush structure (stage `0x0C`)

- Portal rooms walk sub-room ids (`0x13`, `0x14` observed this route; `0x10`,
  `0x0C` on the 2026-08-06 route); a fight room read `0x06`; post-kill `0x0F`.
  Route-dependent — see the corrected `0x1C1D` row. NOT a boss identifier.
- **Within a visit**: a killed rematch's portal goes dead and STAYS dead across
  death-respawn (respawn is at the portal room, cleared portals still cleared).
- **Across visits**: running out of lives → stage select → re-enter = the whole
  rush RESETS, portals live again (player-confirmed). No persistence anywhere,
  consistent with the 2026-08-06 no-latch diff.

### Rematch boss identity — module fingerprint (replaces the `0x1C1D` reading)

Entering a rush portal streams that Maverick's boss module to **RAM base
`0x800FA000`** from ROCK_X5.BIN **chunk `29 + stage_id`** (Grizzly `0x01`→30 …
Skiver `0x08`→37). Proven: the live Squid dump byte-matches chunk 34 at that
base (probes at +0x370…+0x5370); chunk 32 code appears inside Duff's stage
chunk 4 and chunk 36 inside Axle's chunk 10 (boss code is embedded in stage
chunks too, which is how own-stage fights work). ⚠️ **The module PERSISTS
after the fight** — it stays resident through the post-kill corridor until
the next portal replaces it. (An earlier "unloaded after the fight" reading
of the after-dump was wrong: that dump doesn't match Squid because it holds
the NEXT boss's module — Dark Dizzy's.) A resident fingerprint therefore
means "most recently loaded fight", never "fight in progress"; liveness must
come from mode/stage/HP, see the protocol below.

**Fingerprint: 16 bytes at `0x800FA300`** — pairwise-distinct across all 8
boss modules; a 4-byte word is NOT enough (offset +0x300 can hold common
instructions like `lw $s0,0x10($sp)`, inviting collisions with whatever
module Sigma's own fights load — the Sigma-fight dumps match none of the 8
at 16 bytes). **Three of eight are live-verified**: Squid (mid-fight dump),
Izzy Glow and Dark Dizzy (resident in the 2026-08-06 corridor dumps).

| boss | stage id | fp16 @0x800FA300 (hex) |
|---|---|---|
| Grizzly Slash | 0x01 | `060020a1180023ad0800e0031c0024ad` |
| Dark Dizzy | 0x02 | `540002ae0780023c150000a2670000a2` ✅ live |
| Duff McWhalen | 0x03 | `5e0102240d006214001c82260c008380` |
| Mattrex | 0x04 | `801f053c3000a58c04000624ceb0000c` |
| Squid Adler | 0x05 | `01000324020004241aa143a0040004a2` ✅ live |
| Izzy Glow | 0x06 | `b8fcc3a4040002921600062401004224` ✅ live |
| Axle the Red | 0x07 | `0780023c05000324050003a28000038e` |
| The Skiver | 0x08 | `1000b08f0800e0032800bd27e0ffbd27` |

Client protocol: in stage `0x0C`, mode `0x0A`, with the fingerprint matching
a boss, track the boss-HP peak; credit the rematch only when HP reads 0 with
a peak ≥ 8 (rush-corridor idle blips reach 6, real fights fill to 40+) AND
the **player's own HP is nonzero** — a mid-fight player death must never read
as a boss kill, whatever the engine does to the boss-HP byte on respawn.
Reset all fight state whenever mode or stage leaves the fight. **Unknown
fingerprint ⇒ unidentified fight, send nothing** — never guess. (5 of 8
values are chunk-derived; the safety rule makes a surprise harmless.)

### Refill queue `0x800D1C76` (+1 for Zero) — delivery semantics

The AP client queues granted energy here (4 per Small Energy, bit7 = active,
cap 0x7F). Live, multi-trial: **the queue NEVER drains during gameplay** — it
sat frozen through HP dips to 14/46 and 45/46, through multiple deaths and
respawns (HP restored to full by respawn with the queue untouched), through
savestate loads, and through a stage load at full HP with a full sub-tank
(nothing spilled anywhere; no overcap occurred in any observed state). The
sub-tank charge byte also never moved anywhere in `0x1C70–0x1C90` during any
of it. ⚠️ Where/when the engine consumes this queue — and where the tester's
reported overcap (bug (c)) actually happens — is still UNOBSERVED; the one
untested delivery moment is a stage load with HP *below* max. Do not design
the overcap fix until that is seen once.

### Odds and ends

- **Axle the Red has NO area 1** — the (stage 0x07, area 1) entries in all
  three tables (primary/secondary/manifest) are null. The backlog's "dump
  stage 0x07 area 1" item was a static misread.
- **Lava kills through pinned i-frames** (player-confirmed in Mattrex) — the
  god-mode pin `0x8009A101=2` does not protect against it; it is not routed
  through the contact-collision skip. Pit deaths likewise.
- The `0x80072DD4` manifests + `0x80072EAC` lists stream in DURING the door
  transition — a reader must wait for the data to settle, and "nonzero" is NOT
  settled (a partially-streamed Axle a0 list parsed plausibly with a fake
  terminator at 90 of 113 records). Stability across frames is the only safe
  readiness test. See ghidra-findings §9.16.1 for the scanner equivalent.

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

**Game modes (0x800D1C00) — writers enumerated statically 2026-08-08.** Every
store to this byte in the EXE (7, found base-agnostically so the list is
complete for the EXE): `0x8001DD0C`→3, `0x8001DD30`→0x13, `0x8001E4A4`→0,
`0x8001E4FC`→0, `0x8001FC54`→3, `0x8001FC68`→3, `0x80034FC8`→0x0B. **The EXE
only ever writes 0, 3, 0x0B and 0x13** — every other mode (0x04, 0x0A, 0x0C,
0x10, 0x11, 0x14, 0x15) is written by OVERLAY code, which is why EXE-only
scans never found them. Values observed across the 24 RAM dumps, context taken
from what each capture was:

| mode | context | status |
|---|---|---|
| `0x00` | title / boot (also transiently between menus) | ✅ live 2026-08-08 |
| `0x01` | data select (held while choosing new game / load) | ✅ live 2026-08-08 |
| `0x04` | **hub / stage select / Parts menu / launch menu** (stage 0x0D) | ✅ **new 2026-08-08** |
| `0x07`–`0x09` | stage-entry chain (`07→08→09` right before gameplay; `0x09` also blips on any room/door transition as `0A→09→0A`) | ✅ live 2026-08-08 |
| `0x0A` | in-stage gameplay (stages 0x06/0x07/0x0C/0x12) | ✅ |
| `0x0C` | stage 0x0F | ✅ |
| `0x11` | credits | ✅ |
| `0x13`/`0x14` | story cutscene handoff (new-game → intro used `01→13→14` with the stage flipping to cutscene stage `0x0B`, then `14→07→08→09→0A` into intro gameplay) | ✅ live 2026-08-08 |

The client's gameplay gate is `mode in (0x0A, 0x0C)`; the hub being `0x04`
means that gate excludes the hub **by construction**, not by luck.
**The title → data-select → new-game walk is now measured (2026-08-08):**
`0x00 → 0x01 → 0x13 → 0x14 → 0x07 → 0x08 → 0x09 → 0x0A`. None of the menu
modes collide with the gameplay gate. Which mode holds while ACT steps on a
Zero Space clear remains unmeasured. Full derivation: ghidra-findings §9.16.5.

Older observations, kept — beyond the known 0x0A gameplay / 0x0C results:
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

---

## Training mode — a pseudo-save in the campaign struct (live 2026-08-03)

Training mode does **not** use a separate memory region. It populates the same
save struct at `0x800D1C40+` that the campaign uses, which makes it
indistinguishable from a real save unless you test the ACT byte.

Captured with `Scripts/mmx5_act_watch.lua` (log: `Scripts/mmx5_act_log.txt`),
cold boot → Training → boss kill → exit → load a real save:

| Frame | Event | ACT `1C79` | maxHP `1C47` | kills `1C4C` | stage `1C0C` |
|---|---|---|---|---|---|
| 2060 | Training selected in menu | `00`→**`0A`** | `00`→`20` | `00` | `0E` |
| 2453 | Training stage loads | `0A` | `20` | `00` | **`16`** |
| 2906 | mode → `0A` (gameplay) | `0A` | `20` | `00` | `16` |
| ~25000 | **training boss killed** | `0A` | `20` | **`00`** | `16` |
| 25905 | exit to menu | `0A`→`00` | `20`→`00` | `00` | `0E` |
| 34756 | real save loaded | `00`→**`02`** | `00`→`2E` | `00`→`23` | `0E` |

Consequences, all load-bearing for the AP client:

1. **ACT `0x0A` is the training marker.** The campaign range is small — 1 at
   the intro, 5 at Eurasia, `02` observed on a 3-boss save — so `0x0A` is out
   of band and is the only signal that covers the *whole* training session.
   The training stage id `0x16` does not: ACT is already `0x0A` while still in
   the menu at stage `0x0E`.
2. **Max HP becomes `0x20` in the same frame as ACT.** Any "is a save
   resident?" heuristic based on max HP alone passes during training. This is
   exactly how the phantom `Intro Stage - Clear` check reached a tester.
3. **The training boss kill sets NO progress bits.** `0x1C4C`, hearts, armor
   and the AP capability byte recorded zero transitions across the entire
   session including the kill — so training can never fire boss/DNA/heart
   checks, only the ACT-keyed intro one.
4. **Everything is torn down on exit** (ACT and max HP both → `00`), so
   training leaves no residue for a later session.
5. At the title screen *after* training, max HP reads `0x20` while ACT is
   `00` — another reason max HP alone is not a "real save" test.

## Cutscene text / dialogue system — live 2026-08-04

Found while scoping the text-skip feature. **This is the CUTSCENE dialogue
path — the one that makes the game yap.** It is NOT the `{0x41,0x2D}` popup
system in overlay-findings §2.1, which is results-screen banners and is absent
from every cutscene dump (see the scope warning there).

| addr | type | meaning | status |
|---|---|---|---|
| `0x800E8380` | u16 | **Text progress counter** = characters revealed in the current box. Resets per message, climbs while typing, freezes at the message's end value when complete | ✅ live |
| `0x800E8538` | u16 | Mirror of the above, `0x1B8` away — second view of the message state, always identical | ✅ live |
| `0x80091C38` | u32 | Render-buffer write pointer into `0x8010A7xx+`. Advances **+2 bytes per counter step** (16-bit characters) and runs CONTINUOUSLY across messages while the counter resets | ✅ live |

**Cadence: exactly +1 character per 5 frames**, measured across three separate
messages with no drift — so the pacing is a GLOBAL constant, not a per-message
script value. That is what makes a one-constant patch plausible. At 5 frames a
character, an observed 235-character box takes **~20 seconds** to type out.

**The game already has a working instant-complete path.** Y completes the
current box; A advances to the next — two DIFFERENT buttons, so forcing the
complete path cannot cause auto-advance, and cutscene flow (and anything it
commits) stays untouched. Live capture of a Y press:

```
f159990  ctr=23  ptr=0x8010A97E
f159995  ctr=56  ptr=0x8010A9C0    <- Y: +33 chars, ptr +0x42 = 33*2
```

One frame, landing exactly on the message's true end (56). So Y runs the same
per-character loop with the delay removed, walking to the terminator.

**Stopping is TERMINATOR-driven, not length-compare.** Writing the counter
forward by hand (+200) rendered garbage until it happened to hit another
terminator — there is no clamp to message length. Consequence for the feature:
**never patch the VALUE, patch the pacing/branch.** The renderer still walks
every character either way and still meets the terminator.

**Next step: the writer is unlocated.** BizHawk cannot find it (Nymashock has
no memory callbacks and no CPU registers). Needs a DuckStation watchpoint on
writes to `0x800E8380`, pressing Y to catch the instant path, then the
conditional guarding it.

### Text control — the patch sites (live-verified 2026-08-04)

**Pad state: `0x800C9320`, u16 bitfield.** Bit **`0x10` = confirm/complete**
(live: the byte read `0x10` for exactly ONE frame on a Y press, and the text
counter jumped 14 -> 37 on that same frame). Read from ~18 sites across the
static EXE, so it is the global pad word, not text-specific.

**The message STATE MACHINE is at `0x80023Dxx` in the static EXE** — NOT the
render loop at `0x8002414C`. Both features are one NOP each, both verified
identical disc-vs-dump:

| what | RAM | vanilla | patch | disc offset |
|---|---|---|---|---|
| **instant text** | `0x80023D48` `beqz $v1, 0x80023d54` | `10600002` | `00000000` | `0x34A6660` |
| **auto-advance** | `0x80023D84` `beqz $v1, 0x80024138` | `106000EC` | `00000000` | `0x34A669C` |

- `0x80023D48` guards `sb $zero, 0xf($s0)` — **Y ZEROES the pacing flag**.
  NOP the guard and every box completes immediately.
- `0x80023D84` guards the end-of-box wait (`return unless a button is down`).
  NOP it and boxes advance with no input.

**FOUR APPROACHES FAILED FIRST. Do not retry them:**

1. NOP the pacing branch `0x80024360` — text goes instant, but **A dies**: the
   only thing that counts `msg+0x0F` down lives inside the `0x1000` exit that
   patch makes unreachable. Bypassing a check is not satisfying it.
2. Store 0 to `msg+0x0F` at end-of-box (`0x800243F4`) — instant from box 2
   onward; the first box of a sequence stays paced (an initialiser elsewhere
   sets the flag, still unfound).
3. Drop `0x2000` from the loop-exit mask (`0x80024380`) — **breaks display
   entirely**: that path also allocates and positions the box objects, so the
   sequence is consumed with nothing drawn and player control locked out.
4. Force the pad read at `0x800243B8` to 1 — **no effect at all**. That path
   only DECREMENTS the flag by 1; Y zeroes it. Wrong reader of the right byte.

All four rewrote the RENDER LOOP. The mash instrument
(`mmx5_text_watch.lua`, `mash_on()`) worked from the first correct button name
because it drove the game's own complete/advance handling — that was the
signal the patch had to target the STATE MACHINE, and it was missed for four
attempts.

**Method note:** these are RAM writes to code, and **a savestate load reverts
them**. Combined with forgetting an `_off()`, patch state becomes unknowable by
memory — several confusing results came from stacked or silently-reverted
patches. `patches()` reports every site; `all_off()` resets. Apply ONE, test,
re-check.

**PROMPTS ARE SAFE — tested live 2026-08-04, this was the last blocker.**
The worry was that auto-advance would auto-answer choice prompts, firing the
Enigma/shuttle by itself and making a `launch` seed unwinnable. It does not:

- **The Enigma/shuttle launch choice is a MENU on stage select, not this text
  system.** Auto-advance never touches it.
- **Alia's DNA reward choice (Life Up / Energy Up) PAUSES auto-advance** and
  waits for a real selection.

So both features are safe to ship, and no goal-conditional restriction is
needed. Instant text was never at risk either way: it completes the current
box and never advances.
