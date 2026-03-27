# KirbyAM APWorld Changelog

## v0.0.12

- Add stable KirbyAM item groups for YAML filters and plando workflows, with canonical `Shards`/`Maps` groups, backward-compatible legacy aliases, and documented grouping for Unique, Vitality, Useful, and Filler items (Issue #370).
- Harden boss-defeat hook patch safety after v0.0.11 manual white-screen failure evidence (Issue #393): corrected boss hook callsite offset to `0x001D952` and added `patch_rom.py` guardrails that validate boss/chest hook callsites are in-bounds 32-bit Thumb `BL` instructions before overwriting bytes, aborting with actionable errors when callsite shape is unexpected.
- Improve sent item notifications to include detailed information (Issue #432): notifications now display format `"Sent <item_name> to <receiver_name> (<location_name>)"` (sender name omitted; the local player already knows who sent the item) with graceful fallback when location context unavailable. Item names resolve from AP item-name context for the relevant slot, falling back to world item data, then `"Item <id>"`; location names from AP location address mappings; and player names from AP context or player ID fallback.
- Fix item receipt stalls in v0.0.11 by relaxing gameplay gate classification: known menu/cutscene/goal-clear states still defer new mailbox writes, but unknown post-300 AI states now fail open as gameplay-active so incoming AP items and `/release` items can deliver normally (Issue #419).
- Fix the remaining KirbyAM item receipt starvation case where stale/high ROM `debug_item_counter` values could pin delivery state and prevent mailbox writes indefinitely; ahead-counter states now fall back to guarded normal delivery instead of suppressing all received items (Issue #437).
- Fix KirbyAM player template rendering to omit empty `Item & Location Options` sections when all options in that group are hidden, and add regression checks for goal-choice configuration plus required world-version output in generated YAML (Issue #442).
- Fix vitality chest locations not appearing in Archipelago: add vitality chest location definitions to regions in `areas.json` so they are properly instantiated as AP locations and recognized during world generation (Issue #428).
- Fix shipped KirbyAM BizHawk watcher recovery so transient `RequestFailedError` and `NotConnectedError` inside the KirbyAM handler no longer abort manual sessions when using `kirbyam.apworld`; timed-out watcher ticks now reset handler-side reconnect state, reload RAM-backed delivery state, and resume on the next successful poll.
- Add Sound Player as a useful AP item and split its chest into a dedicated AP location check path so opening the chest reports `SOUND_PLAYER_CHEST` without immediate native unlock; native Sound Player now unlocks only on AP `SOUND_PLAYER` item receipt.
- Clean up generated KirbyAM player options YAML for first public build: hide non-shipping `goal` choices from comments/weights, hide `enemy_copy_ability_randomization` `completely_random` from template output, hide unsupported common item/location keys, and clarify that boss/miniboss ability toggles only apply when enemy ability randomization is non-vanilla.
- Remove shard `shuffle` mode from the option contract and generation path; `vanilla` now locks each area shard to its boss-defeat AP location and `completely_random` keeps shards in the global physical-check pool.

## v0.0.11

- Hide KirbyAM goal/event-style objective checks from datapackage location exports so `/locations` no longer lists them as normal AP locations.
- Harden ROM hook context preservation at startup by explicitly saving/restoring low+high register state around `ap_poll_mailbox_c`, reducing startup-state corruption risk (99-lives symptom).
- Split KirbyAM major-chest AP checks from native area-map ownership so opening a big chest no longer grants the map immediately; the native map now unlocks only when the corresponding AP map item is received.
- Add dedicated vitality chest AP location family and transport register (`vitality_chest_flags` at `0x0202C02C`), plus payload interception so native vitality chest rewards become AP checks.
- Apply AP-delivered vitality items through native persistent vitality state (`gTreasures.unk20`) and immediate HP/max HP sync for the active Kirby.
- Fix boss-defeat hook (`ap_on_boss_defeat_collect_shard`) to preserve native shard state by updating `KIRBY_SHARD_FLAGS`, mirroring to `AP_SHARD_BITFIELD`, and calling `persist_shard_to_sram`; prevents permanent white-screen soft-lock after the Moonlight Mansion boss shard-to-hub-mirror cutscene.
- Fix enemy copy-ability randomization runtime integration by applying deterministic non-vanilla remaps through ROM token writes at known enemy/miniboss/boss-spawned ability source addresses; `vanilla` remains unchanged and non-vanilla modes now affect live gameplay as expected (Issue #338).
- Update current enemy copy-ability whitelist semantics to exclude only `Wait` (with `Crash` allowed), and preserve legacy policy compatibility by normalizing historical `Needle` values to `Beam` during runtime patch generation.

## v0.0.10

- Fix KirbyAM Open Patch preflight to revalidate configured base ROM for `.apkirbyam` and reprompt in GUI mode when hash/path checks fail.
- Reduce BizHawk client log spam by suppressing duplicate "patch metadata missing" validation errors during repeated retries.
- Remove debug-only KirbyAM event locations from normal world generation/spoiler output and add regression coverage to prevent `EVENT_DEBUG_` leaks.
- Hide non-shipping KirbyAM goal choices (`100`, `debug`) from generated player YAML templates and add regression coverage.
- Fix KirbyAM BizHawk auth-token registration in `connect_names` to preserve the required `(team, slot)` tuple shape and prevent host `Connect` crashes.

## v0.0.9

- Add critical-module coverage gates for protocol/runtime-sensitive KirbyAM modules, enforced in CI with versioned per-module thresholds.
- Add a repeat-run flaky-test detection mode for reconnect-sensitive KirbyAM tests, with CI workflow support and run-index failure reporting.
- Introduce mutation testing evaluation workflow for logic-heavy KirbyAM modules (ability randomization, data loading) using Cosmic Ray, with documentation and repeatable local baseline capture process.
## v0.0.8

- Fix BizHawk handler detection by validating the KirbyAM USA GBA header and patched auth block instead of an unrelated ROM offset.
- Fix the ROM mailbox hook to return without clobbering live game registers, preventing corrupted startup state such as Player 1 starting with 99 lives.
- Add negative-path tests for build.py and patch_rom.py covering missing ROM paths, missing payload outputs, missing data directory, and invalid CLI argument combinations.

## v0.0.7

- Fix host upload crash (`TypeError: an integer is required`) by converting goal locations to addressless runtime events during item generation.
- Add a structured manual-testing issue template and parser-backed machine-checkable result block format for issue comments.
- Add golden snapshot tests for deterministic slot_data and enemy randomization mapping outputs, with committed JSON fixtures and an explicit snapshot update workflow.
- Remove `worlds/kirbyam/kirbyam.apworld` from source control; add `*.apworld` to `.gitignore` to prevent re-committing the build artifact.
- Add release integrity checks: changelog section verification and `--changelog` gate in the release metadata script and CI.
- Wire `death_link` option into KirbyAM slot-data and runtime DeathLink tag synchronization.
- Add DeathLink runtime receive/apply flow via native Kirby HP (`0x02020FE0`) and local alive->dead outgoing send handling.
- Add end-to-end DeathLink manual validation guidance and remove stale not-ready option wording.
- Add slot_data contract parity tests to prevent drift between PROTOCOL.md and emitted world slot_data fields.
- Add reconnect chaos tests for location polling, mailbox delivery resume, and goal-reporting idempotency.

## v0.0.6

- Add enemy copy-ability randomization with three modes: vanilla, shuffled,
  and completely random.
- Add exclusion controls for boss-spawned ability grants and mini-boss ability
  grants.
- Enforce safe ability pool policy that excludes `Crash` and `Wait`.
- Add major chest location rollout covering all 9 area bits.
- Improve generation stability and local task workflow support.

## v0.0.5

- Expand protocol regression test coverage.
- Add reconnect-safe notification pipeline architecture for receive/send flows.
- Add deterministic gameplay-active gating and reconnect state resync behavior.
- Standardize client logging and remove duplicate location check sends.

## v0.0.4

- Fix tagged release packaging and GitHub release asset upload workflow.

## v0.0.3

- Add boss-defeat location reporting and polling pipeline.
- Integrate native Dark Mind goal detection and goal-location flow.
- Harden mailbox delivery behavior and level-based polling contract.
- Add initial BizHawk Lua connector skeleton.

## v0.0.2

- Automate KirbyAM ROM patch rebuild smoke workflow.

## v0.0.1

- Establish tag-driven draft GitHub release publishing for `kirbyam.apworld`.
- Align the world manifest version to `0.0.1`.
- Document maintainer release steps and validation checklist.
