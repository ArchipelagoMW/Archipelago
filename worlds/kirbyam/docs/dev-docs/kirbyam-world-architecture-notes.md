# KirbyAM World Architecture Notes

This note is for rebuilding working context on `D:\KirbyProject\Archipelago-kirbyam\worlds\kirbyam`. The package is not just a normal Archipelago world definition. It is a three-layer integration:

1. An Archipelago world package that participates in generation, slot-data emission, and patch output.
2. A BizHawk client that polls game state and delivers items through Archipelago's BizHawk bridge.
3. A ROM patch payload injected into Kirby & The Amazing Mirror that exposes an AP mailbox in GBA RAM and hooks native game behavior.

The easiest way to understand the repo is to keep all three layers in view at once.

## What This World Is Trying To Do

The main goal is to make Kirby & The Amazing Mirror playable as an Archipelago world while preserving enough native game behavior to feel correct in BizHawk.

Current shipped scope is centered on:

- world generation inside Archipelago
- KirbyAM-specific items and locations
- ROM patch output as `.apkirbyam`
- BizHawk client connectivity and resync
- AP item delivery through a shared EWRAM mailbox
- location reporting for bosses, major chests, vitality chests, sound player chest, and optional room-sanity
- Dark Mind completion tracking
- optional DeathLink
- deterministic enemy copy-ability randomization

This package does not stand alone. It depends on upstream Archipelago conventions, BizHawk's GBA memory APIs, and reverse-engineered KATAM memory/ROM knowledge.

## Mental Model

The full flow is:

1. Archipelago loads the KirbyAM world package.
2. `KirbyAmWorld` builds regions, items, rules, slot data, and a per-player auth token.
3. During output generation, the world emits an `.apkirbyam` procedure patch.
4. That procedure patch contains a prebuilt `base_patch.bsdiff4` plus token writes for seed-specific runtime data.
5. The player opens the patch through Archipelago Launcher, which creates a patched `.gba`.
6. The patched ROM runs in BizHawk.
7. The Lua connector and `KirbyAmClient` attach through Archipelago's BizHawk bridge.
8. The ROM payload and the Python client exchange state through a reserved mailbox in EWRAM.
9. The client polls RAM for checks and writes incoming items into the mailbox.
10. The ROM applies items, updates transport flags, and native gameplay continues.

If something breaks, it is usually in one of these seam lines:

- JSON data -> world graph construction
- world options -> slot data -> client behavior
- patch tokens -> ROM runtime state
- ROM hooks -> mailbox semantics -> client polling

## Relationship To The Other Repos

This world package sits on top of the other repos previously analyzed.

### Relation To Archipelago

This package follows the standard Archipelago world pattern:

- `World` subclass in `__init__.py`
- static item/location name maps
- option dataclass
- `create_regions`, `create_items`, `set_rules`
- `fill_slot_data`
- `generate_output`
- a `WebWorld` for setup guide integration

So the outer shell is normal Archipelago.

### Relation To BizHawk

The runtime client uses Archipelago's BizHawk integration and depends on BizHawk exposing GBA memory domains consistently. The client logic assumes the emulator can:

- validate ROM header information
- read and write EWRAM reliably
- maintain a persistent session through the Lua connector
- survive reconnects and resync from level-based RAM state

So BizHawk is not just a launcher. It is the live transport layer between Python and the running GBA ROM.

### Relation To The KATAM Decomp

The ROM payload and many addresses are grounded in decomp and reverse-engineering evidence. The KATAM decomp is the best reference for understanding:

- native structure and save-state fields
- AI state values used for gameplay gating
- shard, chest, and room-visit memory layout
- audio and invincibility helper semantics
- multiboot and general engine organization

This repo is not the decomp itself, but it constantly borrows decomp-era knowledge to justify hook points and addresses.

### Relation To Randomizer Data Sources

Some runtime patch inputs and table evidence come from adjacent Kirby randomizer tooling, especially for enemy copy-ability remaps and item/chest mapping. That makes this repo partly an integration layer over established ROM knowledge rather than a purely original mapping effort.

## Package Layout

The main directory is `worlds/kirbyam/`.

Key files and their roles:

- `__init__.py`: world registration, generation lifecycle, slot data, patch output
- `data.py`: loads and normalizes JSON-backed items, locations, regions, and address maps
- `items.py`: `KirbyAmItem` and item-name/id helpers
- `locations.py`: `KirbyAmLocation` and location-name/id helpers
- `regions.py`: constructs Archipelago `Region` objects from JSON topology
- `rules.py`: applies progression and completion rules
- `options.py`: all player-facing options and hidden common-option wrappers
- `rom.py`: AP procedure patch class and per-seed token writes
- `client.py`: BizHawk client runtime
- `ability_randomization.py`: deterministic policy generation for enemy ability remaps
- `enemy_ability_runtime_patch.py`: converts policy into concrete ROM byte writes
- `generation_logging.py`: structured generation logs
- `groups.py`: item and location group construction from tags/categories
- `sanity_check.py`: validation helpers referenced during generation
- `PROTOCOL.md`: mailbox and client/ROM contract
- `TESTING.md`: local integration test and release workflow notes
- `WORKFLOW.md`: project management and scope guardrails
- `build.py`: builds/installs the `.apworld` and optionally refreshes the base ROM patch
- `archipelago.json`: packaged world metadata

Important subdirectories:

- `data/`: JSON datasets and packaged resources such as `base_patch.bsdiff4`
- `data/regions/`: area, room, and transition topology
- `docs/`: player setup docs
- `kirby_ap_payload/`: native ROM patch source and patching pipeline
- `test/`: pytest and integration coverage
- `tools/`: local validation and support utilities
- `save_states/`: debugging/test assets

## The World Entry Point

`__init__.py` defines the package's main types:

- `KirbyAmWebWorld`
- `KirbyAmSettings`
- `KirbyAmWorld`

### `KirbyAmWebWorld`

This is the webhost-facing wrapper. It exposes the setup guide and option groups and gives the world its tutorial presence in Archipelago UI and WebHost.

### `KirbyAmSettings`

This defines the user's base ROM path. It validates the ROM against `KirbyAmProcedurePatch.hash`, which is the MD5 of the expected USA ROM.

This matters because the package assumes a canonical clean ROM for patch generation. If the wrong base ROM is used, the entire runtime address contract becomes suspect.

### `KirbyAmWorld`

This is the real heart of the integration. It provides:

- game metadata and required client version
- option binding through `KirbyAmOptions`
- static item and location ID maps
- generation-time auth token creation
- item pool creation and fixed event placement
- patch-file output
- multidata auth registration
- slot-data emission for the BizHawk client

## Data-Driven Design

This world is heavily data-driven. `data.py` is the main normalization layer that turns JSON into typed in-memory structures.

### `BASE_OFFSET`

The package reserves a safe ID range starting at `3_860_000`.

This is used so KirbyAM item and location IDs do not collide with global Archipelago ranges.

### What `data.py` Loads

`data.py` loads and merges:

- `items.json`
- `locations.json`
- optional `locations_*.json` fragments
- `addresses.json`
- every JSON file under `data/regions/`
- generated room-sanity locations derived from `data/regions/rooms.json`

It builds one central `KirbyAmData` container with:

- `transport_ram_addresses`
- `native_ram_addresses`
- `rom_addresses`
- `regions`
- `locations`
- `items`

This file is important because it is the boundary between raw static data and executable world logic.

### Item Loading

Items can define explicit `item_id`s or let the loader auto-assign them. `data.py` converts classification strings into Archipelago `ItemClassification` values and stores tags for later group resolution.

Those tags matter because `groups.py` builds `ITEM_GROUPS` directly from them.

### Location Loading

Locations also support explicit or auto-assigned IDs. Each location records:

- AP-visible label
- parent region
- default item
- optional bit index for runtime polling
- location category
- tags

This is where the world defines whether something is a boss defeat, major chest, goal, room-sanity check, and so on.

### Room-Sanity Generation

Room-sanity is not maintained as a giant hand-authored location list. Instead, `data.py` synthesizes room-sanity locations from metadata embedded in `data/regions/rooms.json`.

That means `rooms.json` is doing double duty:

- topology source for room graph traversal
- optional generator for `Room X-YY` AP locations

### Region Loading

All region JSON files under `data/regions/` are merged. Each region records:

- exits
- claimed location keys
- event names
- ability-gate annotations

`data.py` enforces integrity here. It rejects duplicate region definitions, duplicate location claims, or references to unknown location keys.

This is the main schema validation layer for the world graph.

## World Generation Lifecycle

`KirbyAmWorld` follows the standard Archipelago lifecycle, but several Kirby-specific choices are important.

### `stage_assert_generate`

This calls validation helpers from `sanity_check.py`. It is a guardrail ensuring the region graph and group maps are coherent before full generation proceeds.

### `generate_early`

This stage:

- records timing/logging metadata
- reads option values
- constructs the deterministic enemy copy-ability policy
- stores that policy on the world object for later slot-data emission and ROM token writes

This is where the seed-specific runtime behavior starts taking shape.

### `create_regions`

This delegates to `regions.create_regions`, which instantiates Archipelago `Region` objects from the preloaded JSON data.

`regions.py` does three things:

1. creates every region in `data.regions`
2. adds physical locations and event locations to each region
3. connects exits after all regions exist

It also creates a synthetic `Menu` region and connects it to `REGION_GAME_START` with `Start Game`.

Event locations are modeled as addressless locked locations with progression items already placed on them.

### `create_items`

This is the most important generation method to understand.

The world classifies fillable locations by `LocationCategory` into buckets such as:

- boss defeat
- major chest
- vitality chest
- sound player chest
- room-sanity

Then it builds the item pool according to shard mode.

#### Vanilla shard mode

If `RandomizeShards` is `vanilla`, shard items are locked onto the ordered boss-defeat locations using `_BOSS_DEFEAT_KEY_ORDER` and `_SHARD_ITEM_LABEL_ORDER`.

This is a very important contract in this repo. Boss-defeat ordering is authoritative for vanilla shard placement.

#### Completely random shard mode

If shards are fully randomized, shard items join the normal fill pool and can appear at any physical check the world treats as open.

#### Filler policy

The active filler pool is small and fixed:

- `1 Up`
- `Small Food`
- `Cell Phone Battery`
- `Max Tomato`
- `Invincibility Candy`

The world computes how many open physical locations exist, includes all non-filler items that should be in the pool, then fills the rest with random filler picks.

#### Goal handling

Goal locations are converted into locked event locations with `address = None`. They are runtime events, not normal host-fillable numeric locations.

That avoids serializing them as regular numeric location slots while still letting Archipelago express completion conditions.

### `set_rules`

This delegates to `rules.py`, which currently implements a relatively minimal logic model.

Important current rules:

- Dimension Mirror access is gated behind all 8 shards
- Dark Meta Knight in the Dimension Mirror is an event prerequisite for the Dark Mind goal
- completion condition is possession of the selected goal event
- shard items are forbidden from boss-defeat locations for the normal randomization path

Ability gating is present mostly as placeholders. Functions like `can_cut_ropes` and `can_break_blocks` currently return permissive placeholders while the richer item/statue logic is still pending.

So the architecture is already prepared for ability-based logic expansion, but the shipped logic is intentionally narrower.

### `generate_basic`

This creates a 16-byte auth token used by the BizHawk client connection.

### `generate_output`

This method packages the actual `.apkirbyam` patch.

It:

1. loads the packaged `data/base_patch.bsdiff4`
2. constructs a `KirbyAmProcedurePatch`
3. writes the base patch file into the procedure patch container
4. writes seed-specific tokens through `write_tokens`
5. emits the patch into the output directory

The base patch is therefore a static artifact, while auth and runtime feature writes are dynamic per seed.

### `modify_multidata`

This registers the auth token in `connect_names` using base64. The client later uses that token to authenticate the emulator session with the server-side multidata contract.

### `fill_slot_data`

This is the bridge from generation to runtime client behavior.

Slot data currently includes:

- goal
- shards mode
- death link
- enemy copy-ability mode
- randomize boss-spawned ability grants
- randomize miniboss ability grants
- room_sanity toggle
- enemy copy ability whitelist
- enemy copy ability policy
- debug logging config

That means the client is not just discovering runtime behavior from ROM memory. It is also driven by seed-specific slot configuration coming from Archipelago generation.

## Items, Locations, And Groups

### `items.py`

`KirbyAmItem` is a thin wrapper around Archipelago `Item`, but it preserves item tags by looking them up in `data.items` when a numeric code exists.

That makes tag-driven grouping and logic easier later.

### `locations.py`

`KirbyAmLocation` adds two convenience fields:

- `key`
- `default_item_code`

These are used during generation and runtime bookkeeping.

### `groups.py`

This file builds:

- item groups from item tags
- location groups from location tags and categories
- compatibility aliases such as `Shard` -> `Shards`
- area meta-groups like `Areas`

It also pre-creates some groups and prunes empty ones to satisfy Archipelago expectations.

This matters for YAML filters, plando targeting, and world UI integration.

## Rules And Logic Model

`rules.py` is intentionally conservative and documents that the logic model is still evolving.

Important takeaways:

- Mirror shards are treated as progression state, not reported AP checks by themselves
- the client reports boss/chest/room checks, while shard ownership drives gating
- goal handling is explicitly modeled as a runtime event
- region ability-gate annotations exist in the data model, but most concrete gate enforcement is still a planned expansion

The file also includes room-graph reachability helpers. That indicates the world is being built to support deeper traversal analysis and future logic rollout rather than only the current minimal boss-goal gate.

## ROM Patch Layer

`rom.py` defines the procedural patch type used by the world.

### `KirbyAmProcedurePatch`

This patch class inherits from Archipelago's `APProcedurePatch` and `APTokenMixin`.

Its procedure is:

1. apply `base_patch.bsdiff4`
2. apply `token_data.bin`

It expects the canonical USA ROM hash and emits `.apkirbyam` as the patch extension.

### `write_tokens`

This function is the main dynamic ROM customization point.

It writes:

- the per-seed auth token to a configured ROM address
- deterministic runtime patch bytes for enemy copy-ability randomization when applicable

This means the patch output is a hybrid of:

- one committed static binary diff
- one generated binary token stream

## Enemy Copy-Ability Randomization

This is one of the most Kirby-specific subsystems in the repo.

### `ability_randomization.py`

This builds the seed-specific policy.

Supported modes:

- vanilla
- shuffled
- completely random

The policy is deterministic and driven by a generated seed and an allowed whitelist. `Wait` is intentionally forbidden.

Mode behavior:

- `vanilla`: identity map
- `shuffled`: deterministic per-enemy-type assignment
- `completely_random`: deterministic per source/grant-event assignment

This policy is stored both in slot data and used to generate ROM writes.

### `enemy_ability_runtime_patch.py`

This translates the policy into concrete ROM file offset writes.

Key points:

- it uses curated source addresses from existing randomizer evidence
- it maps friendly ability names to native game ability IDs
- it respects toggles for miniboss and boss-spawned grant sources
- it writes bytes directly to known ability table addresses

So enemy ability randomization is not a high-level gameplay script. It is a deterministic patch over native ROM tables.

## The BizHawk Client Layer

`client.py` is the live runtime agent once the game is running.

This file matters as much as the world class because it is the thing that actually makes the game talk to Archipelago during play.

### Core Responsibilities

The client must:

- validate that the loaded ROM is the right game and patch type
- attach to Archipelago's BizHawk bridge
- read slot-data configuration
- poll transport and native RAM signals
- report newly observed locations
- deliver received items through the mailbox
- handle reconnects and resync safely
- gate risky operations behind gameplay-state checks
- handle DeathLink send/receive
- report goal completion

### Internal State Model

`initialize_client()` sets up a large amount of state for:

- delivered-item cursor tracking
- mailbox ACK waiting and retry timing
- hook-heartbeat monitoring
- deterministic location ordering
- per-category bitfield mappings
- goal reporting
- notification bookkeeping
- DeathLink bookkeeping
- diagnostic logging

This is not a thin polling script. It is a resilient runtime state machine.

### Location Polling Model

The client derives checks from several categories of RAM state:

- `boss_defeat_flags`
- `major_chest_flags`
- `vitality_chest_flags`
- `sound_player_chest_flags`
- native room-visit flags for room-sanity

The important design choice is level-based polling rather than edge-based polling. The client recomputes the current collected set from RAM and resends any checks missing from the server's acknowledged set.

That makes reconnects safe and avoids one-shot loss from transient disconnects.

### Gameplay-Active Gate

The client does not blindly read and write mailbox state during all game phases. It classifies runtime state using native AI and demo-playback signals so it can defer risky work during menus, demos, cutscenes, and clear states.

This is a critical robustness feature. Without it, item delivery and location polling could race scripted game states.

### Goal Reporting

The client reports goal completion from runtime signals rather than by waiting for a numeric AP goal location. This matches the world design where goal locations are converted into locked events.

### DeathLink

The client synchronizes DeathLink through HP-based local death detection and inbound `DeathLink` packet application.

### Diagnostics And Safety

The client tracks:

- hook heartbeat staleness
- mailbox delivery timeouts
- resend suppression windows
- payload stall warnings
- deduplicated logging for poll transitions

This tells you the runtime protocol has already had enough edge cases that operational resilience is a first-class concern.

## ROM Payload Layer

The native side lives in `kirby_ap_payload/`.

The most important file for understanding behavior is `kirby_ap_payload/ap_payload.c`.

### What The Payload Does

It reserves a mailbox block in EWRAM at `0x0203B000` and uses it as the shared contract between the running GBA ROM and the Python client.

Transport registers include:

- shard bitfield mirror
- incoming item flag/id/player
- delivered item counter/debug values
- frame counter
- boss/chest transport flags
- hook heartbeat
- delivered shard authority bitfield
- shard scrub delay
- mailbox init cookie
- temporary boss shard bitfield

This payload is why the runtime integration works at all. Without it, the client would be reduced to brittle passive memory observation.

### Native Interception Role

The payload does more than expose RAM. It also mediates game behavior so AP owns the right progression concepts.

From the protocol docs and payload comments, it is responsible for maintaining contracts such as:

- boss defeat reporting decoupled from native shard grants
- major chest reporting decoupled from native map ownership
- vitality chest reporting decoupled from native vitality reward ownership
- Sound Player unlock deferred to AP item receipt
- shard authority clamped to AP-owned bits after initialization and cutscene-safe scrub windows

That is the core design principle: native gameplay events still happen, but Archipelago decides which rewards the player actually owns.

### Payload Build And Patch Refresh

`build.py` is the local packager for the APWorld. It can optionally call `kirby_ap_payload/patch_rom.py` to rebuild `data/base_patch.bsdiff4` from a clean ROM, then zip the world into `kirbyam.apworld`.

Important details:

- it injects APContainer fields into `archipelago.json` if missing
- it can skip patch rebuild with `--skip-patch`
- it installs the `.apworld` into Archipelago's custom worlds directory by default on Windows
- it packages the world in place without a staging directory

So the world's distributable artifact is the `.apworld`, while the player's actual game artifact is the `.apkirbyam` patch generated from world output.

## Protocol Contract

`PROTOCOL.md` is the authoritative description of client/ROM communication.

The core idea is a mailbox protocol in EWRAM.

### Directionality

- client writes incoming item requests into mailbox registers
- ROM clears the flag to acknowledge delivery
- ROM exposes boss/chest/shard/runtime state back to the client through mailbox and native RAM signals

### Important Architectural Consequences

- item delivery is explicitly acknowledged, not fire-and-forget
- reconnect recovery is built into the cursor and polling model
- shard state is progression authority, not direct AP check reporting
- gameplay-active gating is part of the protocol, not just a UI convenience

This document is essential when changing anything in `client.py` or the payload.

## Testing, Workflow, And Packaging

### `TESTING.md`

This file describes the local integration loop:

- generate a test archive
- start MultiServer locally or with Docker Compose
- connect BizHawk and the KirbyAM client
- validate item delivery, location checks, and logs
- run focused mypy and pytest targets

It also documents the release process for `kirbyam.apworld` artifacts and the expectations around refreshing the committed `base_patch.bsdiff4` before release tags.

### `WORKFLOW.md`

This defines project guardrails.

The most important practical point is that work is expected to stay scoped to `worlds/kirbyam/` unless explicitly approved otherwise. That matches the repo's architecture: this package tries hard to solve KirbyAM-specific problems without requiring changes to upstream Archipelago core.

### `archipelago.json`

This is the packaged world manifest. It records:

- game name
- world version
- minimum Archipelago version
- authors
- APContainer metadata

This is what lets the packaged world load correctly as an APWorld.

## Current Design Boundaries And Incomplete Areas

A few boundaries are important to remember when working here.

### Logic is intentionally incomplete

Ability-gate enforcement exists mostly as structure and annotation, not full progression logic. The world is prepared for richer logic, but current shipped behavior is still focused on shard-goal progression and the existing check families.

### Ability statues are not yet integrated

Enemy copy-ability randomization exists, but ability-statue randomization is still out of scope. Do not assume “copy ability logic” means the entire game's ability ecosystem has been Archipelago-modeled.

### Shards are progression-state, not AP location checks

This is a critical current contract. Boss defeats and chest openings emit location checks. Shard ownership is used for gating and reward authority.

### Room numbering systems are dangerous

The repo memory note on room index mapping matters: AMR item slots, KATAM decomp room IDs, and `rooms.json` insertion/index labels are different systems. Do not casually equate them.

### Runtime safety matters more than theoretical elegance

The client and protocol both prioritize reconnect safety, mailbox ACK integrity, and cutscene-safe behavior. If a simpler design would break those properties, it is probably the wrong design for this repo.

## Practical Reading Order For Future Work

If you need to rebuild context fast, read files in this order:

1. `__init__.py`
2. `data.py`
3. `regions.py`
4. `rules.py`
5. `rom.py`
6. `client.py`
7. `PROTOCOL.md`
8. `kirby_ap_payload/ap_payload.c`
9. `ability_randomization.py`
10. `enemy_ability_runtime_patch.py`
11. `TESTING.md`

That sequence moves from Archipelago shell, to data model, to runtime bridge, to native protocol.

## Bottom Line

The KirbyAM world package is best understood as a data-driven Archipelago world wrapped around a custom BizHawk client and a ROM-resident AP mailbox payload.

Its architecture is defined by three constraints:

- fit cleanly into Archipelago's world-generation model
- remain robust in BizHawk during real gameplay and reconnects
- express Archipelago ownership over progression rewards without breaking native KirbyAM behavior

Whenever you touch this repo, ask which layer you are changing:

- generation/data
- Python runtime client
- ROM payload/protocol

Most bugs are cross-layer contract bugs, not isolated single-file mistakes.