# Mega Man X5 apworld changelog

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
