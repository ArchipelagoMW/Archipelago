# Mega Man X5 apworld changelog

## Unreleased

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
