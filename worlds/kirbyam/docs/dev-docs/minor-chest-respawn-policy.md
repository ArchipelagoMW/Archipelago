# Minor Chest Respawn/Reopen Policy (Issue #540)

## Conclusion

Minor chest reopen/respawn behavior is treated as **not repeatable** for AP check policy purposes.

## Decomp Evidence

Evidence references used for this policy:

- `katam/src/treasures.c`
  - `CollectChest(u8)` sets the `gTreasures.chestFields` bit and does not include a clear/reset path.
  - `HasChest(u8)` reads the persisted `gTreasures.chestFields` bit.
- `katam/asm/chest.s`
  - Spawn logic gates chest state via `HasChest` using the chest index (`object + 0xE2`).
  - Collection path writes chest collected state via `CollectChest` with the same chest index.

Together these indicate sticky bitfield semantics for native small chest collection state.

## AP Handling Policy

- Treat each verified minor chest mapping as a single-fire AP location check.
- Do not model chest reopen/respawn loops as repeatable AP checks.
- Keep unresolved or ambiguous multi-chest mappings deferred until chest-index attribution is proven.

## Contract Surface

The generated manifest [worlds/kirbyam/data/minor_chest_manifest.json](../../data/minor_chest_manifest.json) now includes metadata:

- `metadata.respawn_reopen_policy.conclusion`
- `metadata.respawn_reopen_policy.ap_handling`
- `metadata.respawn_reopen_policy.evidence`

This keeps the policy machine-checkable and review-visible in versioned artifacts.
