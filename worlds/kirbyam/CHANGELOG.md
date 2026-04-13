# KirbyAM APWorld Changelog

Contract for `## Unreleased` and all post-public `## v...` sections:

- `### New Features`
- `### Bug Fixes`
- `### Internal Changes`

## Unreleased

### New Features

- `Starting Kirby Color` lets players begin a seed with a chosen Kirby palette instead of default Pink, including a random-color option for runs that want a surprise look (Issue #597).
- Tracker support is broader, making it easier for players to follow room progress, location progress, and unique-item progress in tracker tools (Issue #114).
- `Start With All Maps` lets players begin with every area map already unlocked for a more guided and readable playthrough (Issue #584).
- Room names have been updated to match familiar Wikirby naming, making navigation and communication clearer for players (Issue #587).
- Add 15 decomp-aligned world-map big-switch AP checks (`HUB_SWITCH_*`) with a dedicated ROM transport register (`hub_switch_flags` at `0x0203B04C`), BizHawk resend/dedupe polling, payload hook integration at the world-map unlock dispatcher callsite (`sub_08039ED4`), protocol/address contract updates, and regression coverage for data/polling/patch offsets/region binding (Issue #481).
- Fix enemy copy-ability shuffled-mode source coverage gaps by adding missing known US-ROM ability sources (`GOLEM`, `PRANK`, `MASTER_CRAZY_HAND_BULLET`) so same-type enemy grants no longer diverge between patched and unpatched table entries across rooms (Issue #420).
- Improve shuffled enemy copy-ability mapping to guarantee full allowed-ability representation across included enemy types when key cardinality permits (`no_ability_weight < 100`), while preserving explicit `no_ability_weight=100` semantics (all included sources resolve to no ability).
- Add shuffled enemy copy-ability spoiler output listing each randomized source and resulting copy ability (`kind | source_key -> ability`) so seed analysis can verify enemy mappings and full allowed-ability representation (Issue #586).
- Add generation-log shuffled assignment table output (`kind | source -> ability`) so seed build logs show deterministic enemy copy-ability grants for shuffled mode.
- Add completely-random per-swallow reroll telemetry logging (`Kirby swallowed a <EnemyName>. Ability was rerolled to <AbilityName>.`) based on the latest observed runtime swallow event (best-effort; earlier events between polls are noted as missed), while only streaming that line to the live client when `enable_debug_logging` is enabled.

### Bug Fixes

- Restore room-sanity coverage for designed warp rooms by re-enabling their `room_sanity` metadata mappings (Issue #605).
- Updated `Ability Randomization: Minny` (`ability_randomization_minny`) so that it's off by default (Issue #583).
- Prevent skipped in-game item delivery when stale `debug_item_counter` values jump ahead of the client cursor by only trusting forward counter reconciliation for pending mailbox ACKs (`incoming_item_flag == 0` while a delivery is pending), while keeping rewind recovery for true counter rollback.
- Ensure delivery diagnostics gated by `enable_debug_logging` are still written to log files and only hidden from the live client stream via `NoStream` (Issue #601).
- Harden vitality delivery against transition/reset replay by clamping native vitality counter grants to the shipped AP vitality item cardinality (4), and in `one_hit_mode=exclude_vitality_counters` scrub native vitality back to `0` during gameplay so vitality receipts cannot persist in that mode (Issue #571).
- Fix missing boss-defeat LocationChecks when the matching shard is already owned by adding a conservative client fallback: rising-edge bits from `boss_mirror_table_native` byte 0 (bits 0-7) now backfill boss checks when `boss_defeat_flags` is absent for that fight (Issue #573).
- Hide additional KirbyAM reconnect/resend diagnostics from the live client output unless `Enable Debug Logging` is enabled, while still writing those diagnostics to log files unconditionally (`NoStream`-filtered stream suppression only); includes watcher transport reconnect messages and resend diagnostics for boss/major/vitality/sound-player LocationChecks polling (Issue #582).

### Internal Changes

- Reduce duplicate CI runs on feature branches by limiting push-triggered workflow execution to `main` for native static analysis and other PR-validated checks (`scan-build`, `ctest`, `type check`, `build`, and `analyze-modified-files`), while keeping `pull_request` validation behavior unchanged.
- Improve `worlds/kirbyam/build.py` usability for non-author machines by prompting for missing required patch inputs in interactive runs (including missing `--rom` when `--source-type arg` is selected), adding `--source-type file` fallback guidance when `rom_path.tmp` is invalid, and introducing `--non-interactive` fail-fast behavior for automation/CI (Issue #607).
- Expose all configured KirbyAM seed options in `slot_data` (including `start_with_all_maps` and `enable_debug_logging`) so tracker surfaces can render the exact seed configuration from slot data without inferring from partial fields (Issue #114).
- Move unswallowable enemy exclusion policy from a static runtime list into `data/enemies.json` source metadata (`can_be_swallowed`) and represent the currently configured non-swallowable enemies there: `GLUNK`, `JACK`, and `SQUISHY` (Issue #570).

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
