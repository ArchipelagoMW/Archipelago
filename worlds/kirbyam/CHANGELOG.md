# KirbyAM APWorld Changelog

## Unreleased

- Add `One-Hit Mode` (`one_hit_mode`) to the `Make the game harder` option group. Selecting `exclude_vitality_counters` removes all four Vitality Counter items from the item pool (replaced by filler) and enforces a maximum HP of 1 throughout the run. Selecting `include_vitality_counters` keeps Vitality Counters in the pool but still starts Kirby at maximum 1 HP; each Vitality Counter item received raises the cap by 1 (up to 5 with all four). The BizHawk client enforces the cap every gameplay tick by clamping `kirby_max_hp_native` and `kirby_hp_native` (player 0) to `vitality_counter + 1`, with dead/negative HP states preserved (Issue #549).

## v0.0.17

- Add a `Make the game harder` option group containing `No Extra Lives` (`no_extra_lives`) and `DeathLink`, pass `no_extra_lives` through slot data, exclude `1 Up` from filler generation when enabled, and clamp the native life counter to `0` during gameplay with debug-only enforcement logging (Issue #491).
- Add `Ability Randomization: No Ability Weight` (`ability_randomization_no_ability_weight`), a 0-100 weighted no-ability outcome for included randomized enemy grants. A value of `0` preserves all included grants as copy abilities, `100` forces all included grants to resolve to no ability, and intermediate values are deterministic per shuffled enemy type or per completely-random grant event with a separately salted no-ability roll. The shipped default is `55` based on a USA-ROM scan of vanilla regular-enemy placements (`827 / 1510 = 54.77%`). Existing boss-spawn, miniboss, and passive-enemy toggles still control which sources participate (Issue #399).
- Unhide KirbyAM common item/location options in generated templates and option surface (`local_items`, `non_local_items`, `start_inventory`, `start_hints`, `start_location_hints`, `exclude_locations`, `priority_locations`, `item_links`, `plando_items`), and document standard Archipelago usage in world docs (Issue #546).
- Add `Randomize Non-Ability Enemies` world option (`ability_randomization_passive_enemies`) that, when enabled alongside non-vanilla enemy copy-ability randomization, allows enemies that normally grant no copy ability (e.g. Waddle Dee, Bronto Burt, Batty) to receive a randomized ability from the whitelist. Includes 16 additional enemies and a split Waddle Dee mini-boss entry (`WADDLE_DEE_MINI`) gated by the existing mini-boss toggle (Issue #398).
- Reorganize enemy ability-randomization slot/config keys to `ability_randomization_*` names and document that legacy key aliases are intentionally not emitted during the pre-public (`< v0.1.0`) phase.

## v0.0.16

- Fix boss shard AP-ownership semantics by keeping temporary native shard writes only during post-boss cutscene safety windows, then scrubbing non-AP-owned boss-temp shard bits on gameplay resume (instead of relying solely on fixed-frame delay), while preserving already AP-owned shard bits and adding debug-only per-frame post-boss shard telemetry gated by `enable_debug_logging` (Issue #505).

## v0.0.15

- Refactor the KirbyAM area graph to use Rainbow Route as the explicit hub region instead of a flat `REGION_GAME_START` topology, route all shard areas and the Dimension Mirror through that hub, and document that one-way mirrors, two-way mirrors, big-switch shortcuts, and non-mirror travel remain future room-level logic work (Issue #32 / #42).
- Move non-room-sanity KirbyAM location ownership from area `/MAIN` regions into room regions by assigning boss-defeat and big chest checks to concrete `rooms.json` entries, updating `locations.json` `parent_region` values accordingly, and keeping only `GOAL_DARK_MIND` at `REGION_DIMENSION_MIRROR/MAIN`; also relocate `ability_gates` metadata from `areas.json` to per-room placeholders in `rooms.json` and update topology tests for the new contract (Issue #32).
- Add randomized outgoing DeathLink flavor text backed by `worlds/kirbyam/data/deathlink_flavor_text.json`, with `{player}` template interpolation at send time and no change to incoming/local DeathLink application behavior (Issue #409).
- Replace dormant `2 Up`/`3 Up` compatibility fillers with shipped consumable filler effects for `Small Food`, `Cell Phone Battery`, `Max Tomato`, and `Invincibility Candy`, update the active filler pool and ROM payload apply logic, and document the new filler contract and manual validation expectations (Issue #295).
- Add optional Room Sanity (`room_sanity`) with 257 `Room X-YY` checks keyed by native `gVisitedDoors` (`doorsIdx`, bit 15), including reconnect-safe resend/dedupe polling, generation + slot_data gating, protocol/address policy updates, and dedicated Room Sanity polling/docs coverage (Issue #480).

## v0.0.14

- Add gameplay-state debug logging option to help diagnose spurious location checks. When enabled via the `Enable Debug Logging` world option, the BizHawk client logs unique `ai_kirby_state_native` values once per session with their gameplay-active classification, allowing players and developers to collect data on which gameplay states correspond with unexpected checks (Issue #477, debugging phase).
- Fix demo-driven false location checks by introducing title-demo discrimination and preventing gameplay check polling while title-screen demo playback is active (Issue #489).
- Standardize KirbyAM user-facing item and location labels around `Area RoomCode - Thing` naming where room context matters, reorder map item names to `Area - Map`, rename vitality items to area-specific labels, and hide chest contents from physical location names so chest checks no longer spoil map/vitality/Sound Player outcomes (Issue #460).
- Fix BizHawk receive notification item names resolving as `Unknown item (ID: ...)` by resolving received-item names in the local receiver slot context (not sender slot) and treating AP unknown-item placeholders as unresolved so KirbyAM fallback item labels are used when available (Issue #476).
- Fix duplicate physical-item generation in KirbyAM item pool construction by enforcing non-filler uniqueness in pool selection logic (Issue #479 / #484).
- Fix premature native mirror shard ownership after boss-defeat checks by introducing AP-owned shard authority + delayed scrub behavior, while preserving post-cutscene native-state safety from the white-screen regression fix (Issue #478).

## v0.0.13

- Fix KirbyAM goal completion reporting for the shipped addressless Dark Mind goal event: the BizHawk client now sends `CLIENT_GOAL` directly when native clear state is observed instead of waiting on an impossible numeric goal-location acknowledgement, and still accepts post-clear `10000` as a fallback when live polling misses transient `9999`.

- Fix KirbyAM BizHawk receive notifications silently dropped when the ROM processes a mailbox item and clears the flag and increments debug_item_counter in the same GBA frame: the fast-forward reconciliation branch now captures pending delivery state before clearing it and emits the receive notification when the counter-advance is the ACK signal (Issue #269).

- Improve KirbyAM player-facing BizHawk messaging readability by rewording receive/send notifications and send-burst summaries in plain language, adding concise ROM-load failure popups, gameplay gate pause/resume popups, and a `Goal complete` popup, while preserving existing notification timing, dedupe, and rate-limit behavior (Issue #457).

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
