# Mega Man X5 apworld changelog

## Unreleased

**New option: `randomize_options`** (off by default) — let the seed pick your
gameplay options for you. It rolls `goal`, `boss_difficulty`, `launch_odds`,
`text_skip`, `pickupsanity`, `boss_hp_randomization`, `secret_armors_in_pool`,
`stage_unlocks` and `dna_parts_in_pool`, ignoring whatever you wrote for those.
`endgame_checks` is left alone, since it only ever adds checks.

Two results are corrected after the roll, because they are traps rather than
interesting outcomes:

- **The `launch` goal with vanilla odds can be unwinnable** — that goal needs a
  successful launch, you get two attempts, and a full part set is still only
  75%. Choosing it deliberately is your call; having a coin flip hand it to you
  is just a broken seed, so the odds are forced back to deterministic.
- **If the roll asks for more items than the seed has locations**,
  `pickupsanity` is switched on to make room rather than refusing to generate.

What you got is written to the spoiler log. Note the roll can enable options
that change the disc (`pickupsanity`, `text_skip`, `launch_odds`), so patch
from the generated file rather than reusing an old disc.

**New option: `dna_parts_in_pool`** (off by default) — the equippable DNA Parts
become multiworld items.

Mega Man X5 has 16 Parts but a playthrough only ever yields 8: each Maverick
offers two, and Alia's Life+ / Energy+ prompt makes you give up the other
permanently. With this on, the seed picks one Part from each pair and shuffles
those 8, so which Part you end up with no longer depends on which prompt you
answered. The Parts the game would have handed you are suppressed — Parts
arrive only from the multiworld. The "DNA Part" locations are unchanged and
still check on the boss kill; that check was always there, only its reward was
static.

Six Parts do nothing for the wrong character (Burst Shots, Ultimate Buster and
Quick Charge are X's; Z-Saber Plus, Z-Saber Extend and Shot Eraser are Zero's),
so none is ever required for anything.

**Client-side only — no disc change.**

**Generation now refuses option sets that do not fit.** Every item needs a
location, and the world had no check on that: `dna_parts_in_pool` +
`stage_unlocks` + `secret_armors_in_pool` produced 53 items for 48 locations,
generated without complaint, and silently dropped Ultimate Armor and a DNA
Part. That combination now fails at generation with a message naming the fix
(usually `pickupsanity`, which adds 32 locations). If you hit it, nothing was
wrong with your seed before — it was quietly losing items.

Live-tested 2026-08-06: with all 16 Parts force-granted by a research
script, the client cleared them continuously (that is the suppression,
visible in its log), and `Hyper Dash` sent from the multiworld appeared on
the Parts screen as the only Part held.

Implementation note: Parts live in bits 2..17 of the u32 `0x800D1C84`. The
name-to-bit map was read out of the game itself, by forcing every bit on and
reading the Parts screen, because X5 stores UI text as font-tile indices and
web sources return Mega Man X6 Part facts for X5 queries constantly. Full table
in `worlds/mmx5/docs/mmx5-ghidra-findings.md` §9.15. One write does both halves
of the feature each cycle: OR in what the player received, clear what the game
granted.

**New option: `endgame_checks` (ON by default)** — clearing a Zero Space stage
now sends a check. Three locations: Zero Space 1, Zero Space 2 and the X vs
Zero fight. Sigma is not one, because beating him is the goal.

**This changes the default seed**, which went from 45 locations to 48. Until
now every check in a normal seed sat in the eight Maverick stages, so the whole
last stretch of a run was pure travel with nothing to find.

**Client-side only — no disc change.** Detection rides the story ACT byte
(`0x800D1C79`), which the hub's stage-select confirm handler already uses to
pick the endgame destination — so ACT doubles as the endgame progress counter.
Confirmed live 2026-08-06, one step per clear: `5 -> 6`, `6 -> 7`, `7 -> 8`.

It is also the first option that gives the item pool *more* room rather than
less: three locations and no new items, so filler goes from 9 to 12.

Implementation note: the client latches the highest ACT it has seen rather than
reading it live, because two other things write that byte — the `all_mavericks`
goal pushes it back below 5 to hold the endgame shut, and training mode parks
`0x0A` in it, which is above all three thresholds and would otherwise fire
every check at once.

**New option: `stage_unlocks`** (off by default) — the eight Maverick stages
become progression. Exactly one is open at the start (the seed decides which)
and each of the other seven needs its own "&lt;Boss&gt; Access Codes" item,
shuffled into the multiworld like anything else.

A locked stage still shows on the stage-select screen and the cursor still
moves onto it; pressing confirm just does nothing until its codes arrive. The
countdown, the Enigma/Shuttle/Zero Space entry and the whole endgame are
untouched.

**Client-side only — no disc change**, so it works on any already-patched disc.

Implementation note: the hub turns a cursor slot into a stage id through an
8-byte table at `0x800F5050` and then refuses to act on a zero
(`beqz` at `0x800EFCA4`), so the entire in-game half is writing 0 over the
slots you have not unlocked. That handler is the table's only reader in the
whole hub module, so nothing else on the screen changes. The table is overlay
data reloaded from disc on every hub entry, so the client re-asserts it each
cycle and verifies an instruction anchor first — it never writes into whatever
module occupies that address during a stage. One more wrinkle worth knowing:
the store at `0x800EFC98` lands *before* the game's own zero test, so a blocked
confirm parks 0 in `0x800D1C0C`; the client puts the hub's id back, since an
in-hub save would otherwise commit that 0 to the memory card.

Live-tested 2026-08-06: on a seed starting with Grizzly Slash, that stage
entered normally and the other seven did nothing on confirm; sending Duff
McWhalen Access Codes opened that stage immediately, without leaving the stage
select.

**New option: `secret_armors_in_pool`** (off by default) — puts Ultimate Armor
and Black Zero into the item pool. In the base game both come from one hidden
capsule in Zero Space, so you only ever see them at the very end; shuffled into
the multiworld they can turn up at any point.

Client-side only, **no disc change**. Each armor only does anything for its own
character (Ultimate is X's, Black Zero is Zero's), so neither is ever required
for anything — on a seed played as one character the other is dead weight. The
Zero Space capsule still works normally, though receiving an armor makes it
vanish, since the game hides a capsule whose armor you already hold.

Both live-tested 2026-08-06, and they arrive on different schedules. **Ultimate
Armor shows up at your next stage entry**, not in the stage you are standing in
when it arrives — the game decides which armor X wears as the stage loads.
**Black Zero applies immediately**: Zero turns black on the spot.

This also settles an open question from the build: `0x800D1C4B` alone is enough
for Ultimate, and the `0x800D1C4A & 8` bit the Zero Space capsule's despawn
ladder reads is not a second "has Ultimate" flag.

One fix came out of watching it in play: the game writes `0x800D1C4B` itself
(it moved from 1 to 2 at a results screen, with Ultimate still selectable), so
the client now only sets that byte when it reads zero. Before, every later
item you received would have rewritten it, which could have reset your armor
choice.

**New option: `boss_hp_randomization`** (off by default) — randomizes how much
HP bosses have: `weak` 40-80%, `regular` 70-130%, `strong` 120-200%, `chaotic`
25-250%. The roll SCALES what the game would normally give, so Boss Level still
matters and a tough setting on `intense` boss difficulty compounds. Affects
every boss (Mavericks, mid-bosses, Dynamo, Sigma, the Zero duel).

**Client-side only — no disc change**, so it works on any already-patched disc.
Rolls are deterministic per seed, stage and situation, so dying and retrying
gives you the identical fight. Bosses met during the same visit to a stage
share that stage's roll, and the game caps HP at 127, so very high rolls on a
late-game boss can hit that ceiling.

Live-tested 2026-08-05: Grizzly Slash rolled 70 -> 75 and spawned with exactly
75 HP.

Implementation note for future work: the lever is `0x800D1CA2`, proven live to
be boss max HP. It is also the Boss-Level accumulator (`0x1CA2 += level_raw` at
each stage start), so the client restores the vanilla value on leaving a stage
— without that the multiplier compounds and pins every boss to 127 within a few
stages. It also refuses a zero baseline: the stage id flips during a stage load
before that byte is recomputed, and 0 is the instant-death value.

**New option: `pickupsanity`** (off by default) — the 32 freestanding Life
Energy, Weapon Energy and 1-UP capsules become checks, including the ones in
Zero Space and Sigma's stage. **Changes the disc when on** (a per-seed patch:
its own record stub and mailbox ring, plus dispatch redirects for the seven
consumable kinds); seeds without the option produce a disc byte-identical to
0.2.0. Enemy drops are untouched. The intro capsule is deliberately not a
location — the intro cannot be revisited, so it would be permanently missable.

The full pickup inventory was extracted statically from the disc and is
fully provenance-tracked (worlds/mmx5/docs/mmx5-ghidra-findings.md §9.13).
Consumables are identified by their placement-record address (their id byte
is a type, not an identity — three Izzy Glow capsules share one id), which
the game's own spawner stores in the item object and the new stub reports.

Received **Small Energy** filler now heals 4 HP through the engine's own
queued-refill counter (the sub-tank drain path) instead of doing nothing.

**Live-tested 2026-08-05** (first pickupsanity seed, BizHawk + real server):
capsule check sent and confirmed, vanilla effect suppressed, savestate
re-loot produced no duplicate check, and an old-ring Sub-Tank check fired
cleanly on the same disc — the two rings coexist as designed. Later the same
session: **Zero Space 1's 1-UP check fired live** (stage id 0x10 — the
non-contiguous endgame id path), validating the statically-derived endgame
list attributions in the running game. Still untested: receiving a pickup
check's item from another world's slot.

Design decision (Ivor, 2026-08-05): checked capsules stay inert for the
whole seed — no vanilla-healing revival. Considered and declined: reverting
a capsule kind to vanilla healing once all its checks are collected (only
per-KIND would be possible anyway — all capsules of a type share one
dispatch entry, so per-capsule restoration cannot be built on this hook).

## 0.2.0 — 2026-08-04

Three new options and a new default goal. **`text_skip` and `launch_odds`
change the disc, so re-patch if you use either.** The new goal does not — it is
entirely client-side and works on the disc you already have.

**New goal: `all_mavericks` — defeat all 8 Mavericks, then Sigma. This is now
the default.** Seeds generated without an explicit `goal:` line change
behaviour. This goal makes **no disc changes**, so it works on a disc you have
already patched.

Mega Man X5 does not normally require the full set — it opens the endgame as
soon as the Eurasia colony situation resolves, which can happen well before
the eighth Maverick. That matters here because Sigma does not respawn: reach
him early, beat him, and the goal can never complete.

So the client now holds the endgame shut until all 8 Mavericks are down, and
opens it on the eighth kill. It also refuses to power a launch before the full
set is down, since a successful launch resolves the colony by itself. If an
ending is somehow reached early anyway, the client says so in the log rather
than failing silently.

`sigma` is unchanged and still available for anyone who prefers vanilla's
timing.

**New option: `launch_odds`.** By default a launch succeeds exactly when you
hold all 8 Enigma and Shuttle Parts. Set this to `vanilla` and the original
game's gamble comes back — more parts means better odds, never certainty:

- Enigma: 6.25% with no parts, 12.5% with any (extra Enigma parts do nothing
  in the original game either)
- Shuttle: 12.5% / 37.5% / 75% for 0, 1–2, and 3–4 parts

**Under the `launch` goal this can make a seed unwinnable**, and that is
deliberate rather than an oversight: the goal needs a *successful* launch, you
only get two attempts, and even a full set of parts tops out at 75%. Fail both
and the colony falls with no third chance. Generation warns loudly when you
pick this combination. Under `all_mavericks`, no launch can succeed before all
8 Mavericks are down whatever this is set to, since an early success would open
the endgame ahead of the goal.

**New option: `text_skip`.** Mega Man X5 types dialogue out one character every
5 frames and then waits for a button on every box — a single line can run past
200 characters, about 20 seconds of typing before you can even press advance.
Turn this on and boxes appear instantly and advance themselves, so cutscenes
and Alia's in-stage calls play through with no input.

Choices are not skipped. Alia's Life Up / Energy Up prompt still stops and
waits for you to pick, and the Enigma/Shuttle launch decision is a stage-select
menu this never touches — so nothing that affects your run gets answered for
you. Off by default, since at this speed the story is unreadable.

## 0.1.3 — 2026-08-03

**Tank locations could become permanently uncollectable, which could make a
seed unwinnable.** This is the most serious bug found so far. Re-patch your
disc with this version.

Mega Man X5 deletes any pickup you already own — one frame after it spawns.
The client granted tanks by setting exactly those ownership bits, because that
is what makes a tank appear in the pause menu. So a Sub-Tank, W-Tank or
EX-Tank arriving from the multiworld destroyed the vanilla pickup that *is*
that location's check, and the location could never be collected again. With
progression items able to land there, a seed could be stranded.

Measured live in Grizzly Slash, one pass, three items: a consumable's object
lived 251 frames, an un-owned Heart Tank 47, and an **owned Sub-Tank exactly
2** — constructed and then destroyed on the next frame. Heart Tanks were never
affected, because the client grants those by raising max HP instead of setting
the heart bits.

Two fixes, and the client picks the right one automatically:

- **Disc patch (rev 12):** the item's already-owned test in the init handler
  now ignores tanks, so their pickups always appear. Hearts, EX items and
  consumables keep their vanilla behaviour.
- **Client fallback for older discs:** if the disc predates the fix, the
  client holds back that one tank bit while you are in the stage that owns an
  unchecked tank location, so the pickup survives. You get the tank as soon as
  the check is collected or you leave. It detects the patched disc and does
  nothing there, so re-patching removes the trade-off entirely.

**Squid Adler's armor capsule could become uncollectable** — the same trap in
another form. That capsule is gated on collecting energy balls in the jet-bike
section, and owning the part it grants (Falcon Head) makes those balls stop
appearing. Anyone who received Falcon Head from the multiworld before visiting
the stage could never open the capsule. The client now withholds that one part
while you are in that stage with the capsule unchecked, and returns it the
moment you collect the check or leave. **This costs you nothing in play**:
verified live with a complete Falcon set, X still wears the armor in that
stage and the energy balls are present at the same time. The game decides
which armor to equip when the stage loads and the balls consult ownership
during play, so withholding only during play lands neatly between the two.
A disc-level fix would remove
the withhold entirely and is the intended follow-up; the gate is evaluated per
ball as you ride, not at stage load, so it has to be found in stage overlay
code with a debugger BizHawk cannot provide.

**The launch goal could complete without the parts.** Vanilla launches the
shuttle by itself once all eight Mavericks are down, and the client fired the
goal on that success flag alone — one tester finished holding 3 of 8 parts.
The world's own logic always required all 8, so the client was disagreeing
with itself. It now needs a successful launch *and* the full set, and says so
in the log when the story's own launch goes off early.

Also: the `boss_difficulty` option is now properly documented — what relaxed /
standard / intense actually mean, and why fewer countdown hours means harder
bosses. The Enigma/Shuttle parts screen showing more parts than you have
received is a known cosmetic issue, now documented rather than surprising.

## 0.1.2 — 2026-08-03

**Training mode no longer sends checks.** 0.1.1 claimed to have fixed the
phantom "Intro Stage - Clear"; it did not, and this release corrects both the
bug and that claim.

A live capture settled it: selecting Training writes story ACT `0x0A` **and**
max HP `0x20` into the ordinary save struct in the same frame. 0.1.1 only
required the save to look resident, which training satisfies — so the phantom
check still went out. The client now recognises the training pseudo-save
(ACT `0x0A` with no boss kills recorded) and suspends **all** checks, item
grants and launch pinning until you leave it.

Scope, from the same capture: the training boss kill sets no progress bits at
all, so only the intro location was ever affected — no boss, DNA or Heart Tank
check could fire from training. Everything is torn down when you exit, so no
residue carries into a real session.

0.1.1's gating fix is still correct and still needed; it addressed a different
failure (reading the save area before any save is resident, e.g. at boot).

## 0.1.1 — 2026-08-03

Fixes for everything the first testers hit. v0.1.0 could not be used without
hand-editing the apworld; replace it.

- **The world now loads.** v0.1.0 declared `minimum_ap_version: 0.6.8`, but
  0.6.8 is an unreleased development version, so Archipelago rejected the
  world outright and it never appeared in the game list. The floor is 0.6.7,
  the newest release, verified by generating on it.
- **Seeds now accept released clients.** `required_client_version` was also
  0.6.8; the server enforces that value and would have refused every existing
  client. It is 0.6.7 — the oldest version actually tested.
- **`.apmmx5` is registered with the Launcher.** The client never declared
  `patch_suffix`, so Open Patch did not list the extension and "open with →
  Archipelago Launcher" could not route the file, leaving players unable to
  patch their disc.
- **No more phantom checks from stale memory.** Check detection read the save
  struct even before a save was resident, so leftover bytes from a previous
  session could complete locations — one tester received a spurious "Intro
  Stage - Clear", which then swallowed the real one. Save-derived checks now
  require a resident save; the mailbox ring is unaffected.
- Client logging is much quieter: repeated disc-mode, save-gate and grant
  diagnostics moved to debug level.
- Setup guide documents that received items apply at the next stage load.

## 0.1.0 — 2026-08-02

First distributable release.

- 45 locations (intro clear; per Maverick stage: boss, Heart Tank, armor
  capsule, DNA Reward, DNA Part; four tank pickups), 36 real items + filler.
- Goals: `sigma` (defeat Sigma) and `launch` (collect all 8 Enigma/Shuttle
  Parts and complete a successful launch).
- `boss_difficulty` option (relaxed / standard / intense) pinning the frozen
  countdown's Boss Level base.
- Disc patch (v11) applied client-side from a ~445-byte `.apmmx5`:
  vanilla-grant suppression with mailbox pickup records, always-spawning
  randomized capsules, per-sector EDC/ECC regeneration. Accepts the Redump
  dump and its one-extra-trailing-sector variant.
- BizHawkClient: save-struct check detection, idempotent item grants persisted
  in spare save bytes, wrong-save seed stamp, launch scoring, Sigma ending
  detection. Requires BizHawk 2.7+ (tested on 2.10).
