# KirbyAM APWorld Changelog

Contract for `## Unreleased` and post-public `## v...` sections going forward:

- `### New Features`
- `### Improvements` (optional for older post-public sections)
- `### Bug Fixes`
- `### Internal Changes`

## Unreleased

### New Features

- Added trap item support: `Enable Traps` and `Trap Fill Percentage` options let players include trap items in the randomized item pool.
  - `Health Down Trap`: reduces Kirby's current HP by 2 (but won't kill).
  - `Life Down Trap`: removes one extra life (if any remain).
  - `Bomb Trap`: sets Kirby's current HP to 0.
  - `Battery Drain Trap`: empties the cell phone battery to 0.
  - Trap receive notifications are prefixed with "Received trap:" to distinguish them from regular items.
- Added two new filler consumables with tiered healing: `Energy Drink` (HP +2) and `Hunk of Meat` (HP +3), alongside existing `Small Food` (HP +1).
- Enabled the first concrete `MINOR_CHEST` AP checks (Rainbow Route 1-20, 1-22, 1-38).

### Improvements

- None.

### Bug Fixes

- None.

### Internal Changes

- Removed the `Enable Debug Logging` / `enable_debug_logging` world option and corresponding slot_data debug toggle. Client diagnostics that were previously controlled by that option are now file-only logs and are never emitted to the AP client stream.

## v0.2.0

### New Features

- `Starting Kirby Color` lets players begin with a chosen Kirby color instead of always starting as Pink, including a random option for surprise runs (Issue #597).
- `Start With All Maps` lets players begin with every area map already unlocked for a more guided playthrough (Issue #584).
- Room names now match familiar Wikirby names, making the game easier to navigate and discuss (Issue #587).
- Hub big switches are now full Archipelago checks (Issue #481).
- Spoiler output and generation logs now show shuffled enemy ability assignments, making seeds easier to review (Issue #586).

### Improvements
- Enemy Ability Shuffle now covers more enemies, so shuffled abilities stay consistent in more rooms (Issue #420).
- Enemy Ability Shuffle now spreads allowed abilities more evenly across enemies when possible, while still respecting settings that force no ability.
- `Ability Randomization: Minny` is now off by default, fixing seeds that changed Minny unexpectedly unless players opted in (Issue #583).

### Bug Fixes
- Enemy Ability Randomization: Completely random now rerolls abilities per swallow, not per room (Issue #420).
- Warp rooms that were missing Room Sanity checks now have them again (Issue #605).
- Fixed a delivery issue that could cause items to be skipped when the client and game counters got out of sync.
- Fixed debug-only delivery diagnostics so they still go to the log file even when they are hidden from the live client output (Issue #601).
- Fixed vitality counter replays caused by transitions or resets, and prevented vitality counters from lingering in `One-Hit Mode` when that mode excludes them (Issue #571).
- Fixed some boss checks not being sent when the matching shard was already owned (Issue #573).
- Fixed extra reconnect and resend diagnostics showing up in the live client unless debug logging was enabled, while still keeping them in the log file (Issue #582).
- Updated big chest labels to be consistent and no longer uses room names. Also updated location parent regions to be accurate. (Issue #603)

### Internal Changes

- Tracker support now gives trackers a clearer view of room progress, location progress, and unique-item progress (Issue #114).
- Reduce duplicate CI runs on feature branches by limiting push-triggered workflow execution to `main` for native static analysis and other PR-validated checks (`scan-build`, `ctest`, `type check`, `build`, and `analyze-modified-files`), while keeping `pull_request` validation behavior unchanged.
- Improve `worlds/kirbyam/build.py` usability for non-author machines by prompting for missing required patch inputs in interactive runs (including missing `--rom` when `--source-type arg` is selected), adding `--source-type file` fallback guidance when `rom_path.tmp` is invalid, and introducing `--non-interactive` fail-fast behavior for automation/CI (Issue #607).
- Expose all configured KirbyAM seed options in `slot_data` (including `start_with_all_maps` and `enable_debug_logging`) so tracker surfaces can render the exact seed configuration from slot data without inferring from partial fields (Issue #114).
- Move unswallowable enemy exclusion policy from a static runtime list into `data/enemies.json` source metadata (`can_be_swallowed`) and represent the currently configured non-swallowable enemies there: `GLUNK`, `JACK`, and `SQUISHY` (Issue #570).
- When debug logging is enabled, completely random swallow abilities now log what Kirby got from the latest swallow event.

## v0.1.2

### New Features

- `Ability Randomization: Minny` lets players keep Minny at vanilla behavior even when other enemy ability sources are randomized (Issue #572).

### Bug Fixes

- Fix duplicate vitality grants caused by reconnect/reset mailbox replay by adding a ROM-payload vitality replay guard (`delivered_vitality_item_bits`) so each `VITALITY_COUNTER_1..4` AP item is applied at most once per AP mailbox session, and add item-pool invariants/tests that enforce vitality counters appear exactly once in pool modes that include them (Issue #571).
- Exclude unswallowable enemies from the enemy copy-ability randomization pool to prevent no-ability lockouts from non-inhalable enemies; this currently removes `GLUNK` and reserves `SCARFY`/`SHOTZO` as blocked keys for future source-table additions (Issue #570).

### Internal Changes

- Gate ROM delivery-counter reconciliation diagnostics behind `Enable Debug Logging` (`enable_debug_logging`) so non-debug sessions only show normal sent/received item notifications; counter-ahead/back-in-range/rewind/fallback progress messages are now suppressed unless debug logging is enabled (Issue #574).

## v0.1.1

### New Features

- None.

### Bug Fixes

- Harden `One-Hit Mode` (`one_hit_mode`) `exclude_vitality_counters` behavior by removing health-restoring filler (`Small Food`, `Max Tomato`) from filler selection in that mode; when combined with `No Extra Lives`, `1 Up` is also excluded from the already-reduced filler pool.

### Internal Changes

- Gate additional non-user-facing BizHawk client diagnostics behind `enable_debug_logging`, including AP session readiness/reconnect-state logs, room-sanity resend diagnostics, mailbox delivery cursor fast-forward logs, and send/receive queue diagnostic logs; user-facing popups and gameplay behavior are unchanged.
- Add regression coverage for the one-hit/no-extra-lives filler-pool interaction and one-hit HP clamp behavior, plus debug-log gating coverage for runtime gameplay-gate, notification queue, room-sanity resend, mailbox delivery, and AP session-ready diagnostics.

## v0.1.0

First Public Build!

### New Features

- First public playable release of Kirby & The Amazing Mirror for Archipelago: seeds can be generated, patched, connected through BizHawk, and played through with working item delivery, location checks, and goal completion.
- Mirror Shards, maps, Vitality, Sound Player, boss rewards, major chests, and vitality chests are fully integrated into the randomizer so the core Amazing Mirror progression loop is part of normal Archipelago play.
- Optional `Room Sanity` adds room-discovery checks throughout the game for players who want denser exploration and more location coverage.
- `One-Hit Mode`, `No Extra Lives`, and `DeathLink` add extra challenge settings for harsher playthroughs and multiworld punishment runs.
- Enemy copy-ability randomization is available for players who want enemy abilities shuffled or fully randomized, with additional controls over bosses, minibosses, and non-ability enemies.
- Filler and utility rewards are more interesting in moment-to-moment play, with working consumable effects, clearer sent/received item notifications, and cleaner player-facing item/location names.
- Standard Archipelago item/location options and stable KirbyAM item groups are available for filters, YAML setup, hints, plando, and other normal AP workflows.

### Bug Fixes

- Harden the BizHawk client and ROM payload against pre-public integration regressions across mailbox delivery, reconnect recovery, goal reporting, gameplay-state gating, and title-demo suppression so item delivery and location checks remain stable in normal play (Issues #269, #419, #437, #457, #477, #489).
- Fix shard and boss progression handling by preserving native shard state, introducing AP-owned shard authority, and protecting post-boss cutscene/transition behavior from white-screen and premature-ownership regressions (Issues #393, #478, #505).
- Fix release-blocking content and integration bugs found during pre-public work, including missing vitality chest region binding, host upload/auth registration problems, handler detection issues, release packaging problems, and startup-state corruption in the ROM hook path (Issues #428 and related pre-public regressions).

### Internal Changes

- Align the public-release contract by normalizing ability-randomization naming/defaults, removing legacy compatibility paths and aliases, and cleaning up pre-public template output so the shipped option surface matches current behavior.
- Expand protocol, slot-data, patching, reconnect-chaos, release-metadata, snapshot, and negative-path test coverage across the world, client, and payload pipeline to support the first public version.
- Establish the pre-public build and release workflow baseline, including ROM patch rebuild smoke coverage, release integrity checks, and maintainer validation/documentation needed for the `v0.1.0` release line.
