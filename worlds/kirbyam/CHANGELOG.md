# KirbyAM APWorld Changelog

Contract for `## Unreleased` and post-public `## v...` sections going forward:

- `### New Features`
- `### Improvements` (optional for older post-public sections)
- `### Bug Fixes`
- `### Internal Changes`

## v0.2.0

### New Features

- Expanded exploration location check coverage:
  - Minor chests are now implemented as location checks (Issue #129). We expect some bug with this that we haven't found. The chests' content are planned to be implemented as AP items later.
  - Hub switches are now implemented as location checks (Issue #481). Using the connection itself as an AP item is planned for later.
  - The first time you visit each area is now a location check (Issue #606). These types of location check checks give us room to add progression gating items later.
- Added several player-facing quality-of-life features:
  - `Starting Kirby Color` lets players begin with a chosen Kirby color instead of always starting as Pink, including a random option for surprise runs (Issue #597).
  - `Start With All Maps` lets players begin with every area map already unlocked for a more guided playthrough (Issue #584).
  - Room names now match Wikirby names, making the game easier to navigate and discuss (Issue #587).
- Added trap items (Issue #81), which are disabled by default. They are controlled by the options `Enable Traps` and `Trap Fill Percentage`:
  - `Health Down Trap`: reduces Kirby's current HP by 2 (but won't kill Kirby).
  - `Life Down Trap`: removes one extra life (if any remain).
  - `Bomb Trap`: sets Kirby's current HP to 0.
  - `Battery Drain Trap`: empties the cell phone battery to 0.
  - Trap item receive notifications are prefixed with "Received trap:" to distinguish them from regular items.
- Added two new goal modes:
  - `defeat_any_area_boss` completes the seed after the first acknowledged area-boss defeat check (Issue #205).
  - `defeat_random_hidden_area_boss` selects one eligible area boss per seed, stores only an internal hidden boss-defeat key in slot data, and completes the seed when that exact boss is defeated while keeping the target out of normal player-facing output (Issue #206).
- Made improvements to non-trap filler items:
  - Added two new filler consumables with tiered healing (`Energy Drink` (HP +2) and `Hunk of Meat` (HP +3), alongside existing `Small Food` (HP +1) which was renamed) (Issues #684, #685, #686).
  - Made filler items no longer equally likely. They each has preset weight loosely based on their likelihood in the original game. Base whole-number weights are Cell Phone Battery 25, Energy Drink 17, 1 Up 15, Max Tomato 15, Small Food 14, Hunk of Meat 9, Invincibility Candy 5. In one-hit mode (`exclude_vitality_counters`), healing filler (`Small Food`, `Energy Drink`, `Hunk of Meat`, `Max Tomato`) is removed and the remaining weights (`Cell Phone Battery`, `1 Up`, `Invincibility Candy`) are preserved proportionally. In no-lives mode, `1 Up` is removed and remaining filler keeps configured relative weights. When both modes are enabled together, only `Cell Phone Battery` and `Invincibility Candy` remain in weighted selection (Issue #688).
- Added the option to randomize Ability Statues with `ability_randomization_statues`. Defaults to off. It controls inclusion only: enabled statues inherit the selected copy-ability mode (`off`, `shuffled`, `completely_random`), and statues always grant an ability (ignoring `ability_randomization_no_ability_weight` and `ability_randomization_passive_enemies`, while respecting `ability_randomization_minny` just like enemy randomization) (Issue #209).

### Improvements

- Enemy Ability Shuffle now covers more enemies, spreads allowed abilities more evenly across enemies when possible while still respecting settings that force no ability, and keeps `Ability Randomization: Minny` off by default unless players opt in (Issues #420, #583).
- DeathLink got flavor text (Issue #409).
- Spoiler output and generation logs now show shuffled enemy ability assignments, making seeds easier to review (Issue #586). This includes ability statues (Issue #804).

### Bug Fixes

- Enemy Ability Randomization: Completely random now rerolls abilities per swallow, not per room (Issue #420).
- Warp rooms that were missing Room Sanity checks now have them (Issue #605).
- Fixed delivery synchronization and logging issues that could skip items when client and game counters drifted, while ensuring debug-only delivery diagnostics still go to the log file even when hidden from the live client output (Issue #601).
- Fixed vitality counter replays caused by transitions or resets, and prevented vitality counters from lingering in `One-Hit Mode` when that mode excludes them (Issue #571).
- Fixed extra logging showing up in the live client when they should have remained file-only (Issue #582).

### Internal Changes

- Tracker support now gives trackers a clearer view of room progress, location progress, and unique-item progress, and KirbyAM seed options are exposed in `slot_data` so tracker surfaces can render the exact seed configuration from slot data without inferring from partial fields, including newly added option surfaces such as `start_with_all_maps` (Issue #114).
- Reduce duplicate CI runs on feature branches by limiting push-triggered workflow execution to `main` for native static analysis and other PR-validated checks (`scan-build`, `ctest`, `type check`, `build`, and `analyze-modified-files`), while keeping `pull_request` validation behavior unchanged.
- Improve `worlds/kirbyam/build.py` usability for non-author machines by prompting for missing required patch inputs in interactive runs (including missing `--rom` when `--source-type arg` is selected), adding `--source-type file` fallback guidance when `rom_path.tmp` is invalid, and introducing `--non-interactive` fail-fast behavior for automation/CI (Issue #607).
- Move unswallowable enemy exclusion policy from a static runtime list into `data/enemies.json` source metadata (`can_be_swallowed`) and represent the currently configured non-swallowable enemies there: `GLUNK`, `JACK`, and `SQUISHY` (Issue #570).
- Completely random swallow abilities now emit file-only diagnostics describing what Kirby got from the latest swallow event, and the old `Enable Debug Logging` / `enable_debug_logging` toggle has been removed so those diagnostics are no longer part of the player-facing option surface.

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
