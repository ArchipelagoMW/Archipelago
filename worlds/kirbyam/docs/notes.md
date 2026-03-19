# Kirby & The Amazing Mirror (GBA) - Address Policy Notes

## POC baseline

- Baseline ROM for the POC is `Kirby & The Amazing Mirror (USA).gba` only.
- Multi-ROM parity (EU/JP/VC) is out of scope for this phase.
- Non-USA testing remains tracked separately (`#99`, `#100`, `#101`, `#102`).

## Address domain separation (locked policy)

Do not mix these two domains:

1. AP transport/mailbox addresses
- Purpose: client/ROM communication contract.
- Source of truth: `worlds/kirbyam/data/addresses.json` under `ram.transport`.
- Examples: `incoming_item_flag`, `incoming_item_id`, `delivered_item_index`.

2. Native game-state addresses
- Purpose: in-game progression/check/goal state.
- Source of truth: `worlds/kirbyam/data/native_address_policy.json` and `ram.native` in `worlds/kirbyam/data/addresses.json`.
- Current integrated native signal: `shard_bitfield_native` at `0x02038970`.

Rule: AP transport fields must never be treated as native gameplay truth.

## Status taxonomy

- `candidate`: Derived from workbook/cheat/reverse-engineering source; requires live confirmation.
- `integrated`: Used by current client/ROM path but not yet promoted to fully live-verified policy status.
- `verified`: Confirmed by repeatable live memory observation on USA ROM.

Current high-level status:

| Signal type | Candidate | Integrated | Verified |
| --- | --- | --- | --- |
| Shard progression | Yes | Yes | Not yet policy-promoted |
| Dungeon boss defeat | Yes | No | No |
| Final boss defeat | Yes | No | No |

Detailed signal registry: `worlds/kirbyam/data/native_address_policy.json`

## Promotion criteria (candidate/integrated -> verified)

All criteria below must be met:

1. Observed on USA ROM in BizHawk during real gameplay action.
2. Before/after transition recorded with exact address, width, and expected semantics.
3. Reproduced in at least 3 independent attempts with consistent transition behavior.
4. Persistence checked across room transitions and save/reload as applicable.
5. Cross-domain sanity check confirms no AP mailbox field is used as native source.
6. Registry and matrix updated together:
- `worlds/kirbyam/data/native_address_policy.json`
- `worlds/kirbyam/ADDRESS_VERIFICATION_MATRIX.md`

## POC shard mapping reference

Current proof-of-concept shard bit mapping:

- bit 0 -> `SHARD_1`
- bit 1 -> `SHARD_2`
- bit 2 -> `SHARD_3`
- bit 3 -> `SHARD_4`
- bit 4 -> `SHARD_5`
- bit 5 -> `SHARD_6`
- bit 6 -> `SHARD_7`
- bit 7 -> `SHARD_8`

## Implementation notes

- Transport contract details: `worlds/kirbyam/PROTOCOL.md`
- Verification workflow: `worlds/kirbyam/docs/BIZHAWK_TESTING_GUIDE.md`
- Native signal status registry: `worlds/kirbyam/data/native_address_policy.json`
