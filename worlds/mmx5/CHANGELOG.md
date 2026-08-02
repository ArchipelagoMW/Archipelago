# Mega Man X5 apworld changelog

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
