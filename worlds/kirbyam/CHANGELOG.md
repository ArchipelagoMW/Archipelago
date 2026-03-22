# KirbyAM APWorld Changelog

## Unreleased

- Wire `death_link` option into KirbyAM slot-data and runtime DeathLink tag synchronization.
- Add DeathLink runtime receive/apply flow via native Kirby HP (`0x02020FE0`) and local alive->dead outgoing send handling.

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
