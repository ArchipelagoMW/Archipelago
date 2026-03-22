# KirbyAM Test Fixture Data

This directory contains reusable, pre-generated fixture datasets for unit and integration tests in `worlds/kirbyam/test/`.

## Files

- `ram_mailbox_baseline.json`
  - Baseline transport RAM snapshot for AP mailbox fields and shard fallback polling.
- `shard_bitfields.json`
  - Bitfield scenario vectors for shard polling and location-check transitions.
- `item_delivery_sequences.json`
  - Item delivery examples and mailbox ack transitions.
- `location_check_transitions.json`
  - Expected location-check behavior for shard progression and resend scenarios.
- `snapshots/`
  - Committed golden snapshots for deterministic outputs (slot_data and
    enemy mapping artifacts).

## Address Ranges

- `0x0202C000-0x0202C020`
  - AP transport mailbox / debug region used by client protocol fields.
- `0x02038970`
  - Native shard flag byte used by current POC polling path.

## Expected State Transitions

- Mailbox write flow:
  1. `incoming_item_flag == 0`
  2. client writes `incoming_item_id` + `incoming_item_player`
  3. client sets `incoming_item_flag = 1`
  4. ROM applies item and clears `incoming_item_flag = 0`
- Location checks:
  1. shard bit flips from `0` to `1`
  2. client maps bit index to AP location IDs
  3. client sends missing checks relative to server `checked_locations`

## Timing Assumptions

- Watcher cadence is approximately one tick every `0.125s`.
- Bitfield and mailbox reads are treated as atomic per watcher tick.
- Server acknowledgment of location checks can lag by one or more ticks, requiring resend behavior.
- Mailbox ack (`incoming_item_flag` reset to `0`) is observed on subsequent ticks.
