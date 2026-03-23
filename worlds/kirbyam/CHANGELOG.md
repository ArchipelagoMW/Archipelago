# KirbyAM APWorld Changelog

## Unreleased

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
