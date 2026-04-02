# Archipelago Architecture Notes

This is a working reference for understanding how Archipelago works in the local checkout at `D:\KirbyProject\Archipelago`.

It is meant to answer questions like:
- What are the main executables?
- How does generation work?
- What exactly is a `World` in Archipelago?
- What does the server host?
- What do clients actually send and receive?
- How do packaged worlds and the WebHost fit into the system?

This is intentionally architecture-focused, not a player setup guide.

## Executive Summary

Archipelago is a multi-part system, not one program.

At a high level it consists of:
- A launcher and packaging surface.
- A generation pipeline that builds a `MultiWorld` from YAML/player options.
- A server that hosts a generated multiworld session over WebSockets.
- Clients that connect to the server and synchronize checks, items, hints, and status.
- A plugin-like world system where each supported game contributes generation logic and client-facing metadata.
- A WebHost that exposes browser-based hosting, tutorials, option pages, and related web features.

The most important conceptual split is:
- Generation is offline build-time work.
- Hosting is runtime session work.
- A world implementation bridges the two by defining game-specific logic, items, locations, options, output files, and slot data.

## High-Level Mental Model

Think of Archipelago as six layers:

1. Bootstrap and entry points
- `Launcher.py`
- `Generate.py`
- `Main.py`
- `MultiServer.py`
- `WebHost.py`
- individual game clients like `BizHawkClient.py`, `OoTClient.py`, `SNIClient.py`, etc.

2. Core generation model
- `BaseClasses.py`
- `Fill.py`
- `Options.py`
- `entrance_rando.py`
- `rule_builder/`

3. Network protocol and shared client/server types
- `NetUtils.py`
- `CommonClient.py`
- portions of `MultiServer.py`

4. World registration and world API
- `worlds/__init__.py`
- `worlds/AutoWorld.py`
- each concrete world package under `worlds/`

5. User configuration and host settings
- `settings.py`
- YAML player files and `host.yaml`

6. WebHost and website integration
- `WebHost.py`
- `WebHostLib/`
- tutorials and world docs rendered for the website

## What the Main Programs Do

### Launcher

Primary file:
- `Launcher.py`

`Launcher.py` is the top-level launcher surface.

It can:
- open the GUI launcher,
- open/edit `host.yaml`,
- identify patch files and route them to the right client,
- launch components by name,
- generate YAML templates,
- open website/Discord/file-browser helpers,
- act as an entry point for build-oriented components like APWorld packaging.

It is best thought of as the user-facing process router for the Archipelago installation.

### Generator front-end

Primary file:
- `Generate.py`

`Generate.py` is the command-line generation front-end.

It is responsible for:
- parsing generation CLI arguments,
- locating and loading weights/player YAMLs,
- rolling options,
- expanding meta options and triggers,
- constructing a fully populated argument namespace for generation,
- then handing that prepared state into the actual generator logic in `Main.py`.

Important detail:
- `Generate.py` is mostly about turning user configuration into structured inputs.
- `Main.py` is where the actual multiworld graph/item placement/output pipeline runs.

### Generator core

Primary file:
- `Main.py`

`Main.py` is the central multiworld generation pipeline.

It creates a `MultiWorld`, initializes per-player world objects, executes world generation stages, runs the fill algorithm, checks accessibility, and writes output artifacts including the `.archipelago` session file.

### Session server

Primary file:
- `MultiServer.py`

`MultiServer.py` hosts generated sessions over WebSockets.

It:
- loads multidata/session state,
- accepts WebSocket clients,
- authenticates players,
- manages checked locations, received items, hints, and commands,
- exposes shared data storage operations,
- persists session state,
- broadcasts room updates and chat-style structured messages.

### Shared/reference client

Primary file:
- `CommonClient.py`

`CommonClient.py` provides the general client model used by text-only/reference clients and as a base for game-specific clients.

It handles:
- WebSocket connection management,
- command parsing,
- data package usage,
- local tracking of received items/checks,
- generic packet handling and display logic.

### WebHost

Primary file:
- `WebHost.py`

`WebHost.py` boots the website/webhost side.

It wires up:
- Flask app creation,
- config loading,
- DB binding,
- WebHost registration and caches,
- world/tutorial doc copying,
- auto-hosting and auto-generation helpers,
- production serving through Waitress if configured.

## The Core Domain Object: MultiWorld

Primary file:
- `BaseClasses.py`

The central in-memory object during generation is `MultiWorld`.

It contains, among other things:
- all players and player names,
- all instantiated world objects,
- all regions, entrances, and locations,
- the global item pool,
- player options and per-player settings-derived behavior,
- completion conditions,
- precollected items,
- locality, hints, plando blocks, item links, and group slots,
- spoiler and progression-analysis helpers,
- seeded RNG state.

Important architectural point:
- `MultiWorld` is the full cross-player generation state.
- Each world object contributes only its game-specific part of the total graph.
- Fill, balancing, hint generation, and final output all work against this combined object.

## What a World Really Is

Primary files:
- `worlds/AutoWorld.py`
- `worlds/__init__.py`
- `docs/world api.md`

A world is Archipelago's plugin model for a game.

Concretely:
- Each supported game provides a subclass of `worlds.AutoWorld.World`.
- The class is registered automatically via the `AutoWorldRegister` metaclass.
- Each player in a generation gets their own world instance for the chosen game.

A world class provides:
- game name,
- item and location ID maps,
- option dataclass,
- generation logic,
- output generation,
- optional slot data,
- optional WebHost metadata through a `WebWorld` instance.

The metaclass does important normalization:
- validates required fields like `item_name_to_id` and `location_name_to_id`,
- constructs reverse lookups,
- builds item/location name sets and groups,
- registers the world class into `AutoWorldRegister.world_types` keyed by game name,
- derives settings keys.

This means world discovery is mostly import-driven: if a world module loads successfully, it registers itself.

## How Worlds Are Loaded

Primary file:
- `worlds/__init__.py`

World loading is dynamic.

The loader scans:
- built-in world folders under `worlds/`,
- user/custom world folders,
- packaged `.apworld` archives.

Behavior to remember:
- Loose built-in worlds are imported first.
- Each import triggers world class registration.
- Manifest data like `archipelago.json` can supply metadata such as game name and world version.
- `.apworld` packages are zip-based and can be version-gated by minimum/maximum Archipelago version.
- A failure to load one world is logged and tracked, but does not necessarily abort the whole application.

After loading, Archipelago builds a `network_data_package` for all registered games. That package is a key bridge between the generation side and the client/server protocol side.

## APWorld Packaging Model

Primary doc:
- `docs/apworld specification.md`

An `.apworld` is a packaged world archive.

Important facts:
- It is a zip archive with a `.apworld` extension.
- The internal folder name must match the file name.
- Metadata lives in `archipelago.json`.
- The launcher has a component to build `.apworld` files from source worlds.
- `.apignore` controls what is excluded from the package.
- Imports inside packaged worlds must use relative imports internally and absolute imports for Archipelago base modules.

Practical meaning:
- World support is intentionally extensible without forcing every world into the core repo.
- The world API is treated like a semi-stable plugin surface.

## Generation Pipeline, End to End

Primary files:
- `Generate.py`
- `Main.py`
- `BaseClasses.py`
- `Fill.py`

The generation flow is roughly:

1. Parse generation inputs
- `Generate.py` parses CLI arguments and loads settings defaults from `host.yaml`.
- It finds weights/player YAMLs and optional meta files.
- It rolls or expands option values.
- It builds per-player arguments like game, name, sprite, and options.

2. Create `MultiWorld`
- `Main.main()` constructs `MultiWorld(args.multi)`.
- Seed and race mode are applied.
- Player names, games, and cosmetic fields are copied in.

3. Instantiate world objects
- `multiworld.set_options(args)` creates one world instance per player based on `AutoWorldRegister.world_types[game]`.
- Each instance receives its typed options object.

4. Apply early world stages
- `assert_generate` when output is expected,
- `generate_early`,
- player start inventory and local/non-local cleanup,
- item links setup.

5. Build graph and pool
- `create_regions`
- `create_items`
- `set_rules`
- exclusion/priority/locality rule application
- `connect_entrances`
- `generate_basic`

6. Run pre-fill logic
- parse and distribute plando blocks,
- `pre_fill`,
- any world-specific special placement prep.

7. Fill the multiworld
- choose algorithm,
- run restrictive or flood fill,
- perform post-fill hooks,
- optionally run progression balancing.

8. Finalize and output
- `finalize_multiworld`
- `pre_output`
- check accessibility and beatability,
- world-specific `generate_output`,
- write `.archipelago` multidata,
- optionally write spoiler/playthrough,
- zip final output files.

This is the central lifecycle to keep in mind when changing generation behavior.

## Stage-Based World API

Primary file:
- `worlds/AutoWorld.py`

The world API is stage-based.

The common stages include:
- `assert_generate`
- `generate_early`
- `create_regions`
- `create_items`
- `set_rules`
- `connect_entrances`
- `generate_basic`
- `pre_fill`
- `post_fill`
- `finalize_multiworld`
- `pre_output`
- `generate_output`
- `fill_slot_data`
- `modify_multidata`

Key helper behavior:
- `call_single()` calls a stage on a single player's world.
- `call_all()` calls the per-player implementation for all worlds, then runs a class-level `stage_<name>` hook if defined.
- `call_stage()` runs those class-level stage hooks sorted by world type.

Why this matters:
- Generation logic is intentionally distributed.
- The core pipeline does not know game-specific rules; it only knows stage names and ordering.
- Cross-game coordination happens through `MultiWorld`, stage hooks, and shared fill/balancing logic.

## Regions, Entrances, Locations, Items, and Events

Primary sources:
- `BaseClasses.py`
- `docs/world api.md`

Archipelago's logic model is graph-based.

Key concepts:
- `Region`: logical area/container.
- `Entrance`: connection between regions.
- `Location`: a check that can hold an item.
- `Item`: something placed into the pool and potentially received by a player.
- `CollectionState`: simulated inventory/progression state used during logic checks.

Events are important:
- Event items/locations exist only during generation.
- They use `None` IDs and are not sent to the server as real checks/items.
- They are used to model game-state transitions or goals cleanly in logic.

This is one of the most important mental models in Archipelago:
- The generator does not reason about your game directly.
- It reasons about a graph of regions/entrances/locations and a set of items/events that unlock them.

## The Fill Algorithm

Primary file:
- `Fill.py`

`Fill.py` contains the item placement algorithms and related helpers.

Important behavior:
- It builds and updates `CollectionState` snapshots to test reachability.
- It attempts restrictive placement in a way that preserves beatability and accessibility requirements.
- It supports swapping already placed items when stuck.
- It tracks progression and can handle partial or special-case fills.
- It cooperates with per-world access rules and item rules rather than replacing them.

Important implication:
- Most generation failures are not "randomizer bugs" in the abstract.
- They usually arise from inconsistent world logic, incorrect item classifications, impossible access rules, or fill assumptions violated by world behavior.

## What the Generator Outputs

Primary file:
- `Main.py`

Generation output generally has two layers:

1. Player/world-specific output
- Produced by each world's `generate_output()`.
- Examples include ROM patches, mod files, JSON blobs, or game-specific patch artifacts.

2. Session output
- Produced centrally as `.archipelago` multidata.
- Then bundled into the final output zip.

The `.archipelago` file contains compressed serialized multidata including:
- `slot_data`
- `slot_info`
- player name/connection mapping
- location item placements
- server options
- hint data
- precollected items/hints
- version requirements
- seed name
- progression spheres
- embedded data package subset
- race mode flag

This file is what the server actually needs to host the generated session.

## Slot Data vs Data Package

These are easy to confuse, but they are not the same.

### Data package

Defined via:
- `worlds/network_data_package`
- documented in `docs/network protocol.md`

The data package is global static-ish metadata per game, mainly:
- item name to ID mappings,
- location name to ID mappings,
- checksum data,
- some group-related metadata depending on client-side caches.

Purpose:
- lets clients resolve names/IDs without hardcoding every mapping,
- helps clients interoperate with the server even in generic or cross-language implementations,
- supports caching via checksums.

### Slot data

Produced by:
- world method `fill_slot_data()`

Purpose:
- per-slot, per-seed data the client actually needs to play the generated run,
- typically option results or small seed-specific facts,
- sent to the client after successful connection.

Rule of thumb:
- Use data package for stable game metadata.
- Use slot data for seed-specific client necessities.

## Network Model

Primary sources:
- `NetUtils.py`
- `CommonClient.py`
- `MultiServer.py`
- `docs/network protocol.md`

Archipelago uses WebSockets and sends JSON packet lists.

Core protocol flow:
1. Client opens WebSocket.
2. Server sends `RoomInfo`.
3. Client may request `GetDataPackage`.
4. Server returns `DataPackage`.
5. Client sends `Connect`.
6. Server responds with `Connected` or `ConnectionRefused`.
7. Server may send `ReceivedItems` backlog.
8. Server broadcasts structured chat/status via `PrintJSON` and updates via `RoomUpdate`.

Important packet groups:
- Session metadata: `RoomInfo`, `RoomUpdate`, `Connected`
- Inventory/check sync: `ReceivedItems`, `LocationChecks`, `LocationInfo`, `Sync`
- Messaging: `PrintJSON`, `Say`
- State/status: `StatusUpdate`
- Hints: `CreateHints`, `UpdateHint`
- Shared data storage: `Get`, `Set`, `SetNotify`, `Retrieved`, `SetReply`
- Generic forwarding: `Bounce`, `Bounced`

Important architectural point:
- The protocol is intentionally generic enough that clients can be written in other languages.
- The Python codebase is the reference implementation, not the only valid implementation.

## Core Shared Network Types

Primary file:
- `NetUtils.py`

`NetUtils.py` defines common types and serialization helpers such as:
- `NetworkPlayer`
- `NetworkSlot`
- `NetworkItem`
- `ClientStatus`
- `SlotType`
- `Permission`
- `HintStatus`
- JSON encode/decode helpers
- parser utilities for `PrintJSON`

Important implementation detail:
- NamedTuple-like structures are encoded with a `class` field.
- Version and network objects are reconstructed on decode through explicit hooks/allowlists.
- `convert_to_base_types()` exists to flatten richer Python values into JSON-safe primitive structures.

This file is effectively the shared schema layer between server, common clients, and generated multidata.

## How the Common Client Thinks

Primary file:
- `CommonClient.py`

`CommonClient` is the reference client model.

It owns:
- connection settings like address, username, password, and tags,
- packet handling,
- local item/check state,
- command processor support,
- item/location name lookup using the data package,
- output formatting for `PrintJSON` and command responses.

Notable client concerns:
- it caches and uses data package data,
- it tracks `items_received` with indexing,
- it can resync after mismatched item indices,
- it exposes commands like connect, disconnect, ready, received, missing, items, and locations.

Game-specific clients usually build on the same basic pattern but add integration with a concrete game runtime.

## What the Server Actually Manages

Primary file:
- `MultiServer.py`

The server is more than a dumb relay.

It manages:
- connected endpoints and authenticated clients,
- team/slot associations,
- checked locations,
- queued items and received-item indices,
- hints and hint points,
- session permissions like release/collect/remaining,
- room/player status,
- shared key-value storage and data notifications,
- persistence/autosave,
- command processing,
- forwarding mechanics like Bounce/DeathLink.

The server's `Context` is the central runtime state for a hosted session.

Important design choice:
- The server hosts a generated session from multidata, not the generator itself.
- Generation-time rules and placements are already baked in when the server starts.
- Runtime server work is mostly synchronization, validation, persistence, and message routing.

## Shared Data Storage and Bounce

Primary source:
- `docs/network protocol.md`

Two protocol capabilities matter a lot for richer integrations:

### Bounce/Bounced
- Generic targeted message forwarding by game, slot, or tag.
- Used for cross-client features like DeathLink and other event-style integrations.

### Get/Set/SetNotify
- Shared server-side data storage with operation-based mutation.
- Supports operations like replace, default, add, update, bitwise ops, etc.
- Useful for trackers, coordination, and custom client/server features beyond basic item sync.

This makes Archipelago more than a simple item-delivery service. It also acts as a lightweight shared session state server.

## Items Handling Flags and Remote Item Behavior

The connection handshake includes `items_handling` flags.

These affect whether the server sends:
- no items,
- only remote items,
- also items from the same world,
- starting inventory items.

This is important because not every game client handles local/remote inventory the same way.

From the protocol and coop notes:
- Some games are effectively remote-items games.
- Others can avoid sending same-world items unless explicitly configured.
- Clients need to know how their world expects to treat local vs remote progression.

## Settings Model vs Player Options

Primary file:
- `settings.py`

Archipelago makes a strong distinction between:

### Player options
- Per-generation, player-provided values.
- Usually come from YAMLs.
- Affect how the run is generated.
- Parsed into typed option dataclasses attached to each world.

### Settings
- Installation- or environment-oriented values from `host.yaml` and related config.
- Used for things like ROM paths, generator defaults, server defaults, and other static configuration.
- Exposed through typed `Group` objects.

This distinction matters a lot because it explains why some values live in player YAMLs and others live in `host.yaml`.

`settings.py` is also doing more than plain dict loading:
- typed lazy settings groups,
- path validation and browse prompts for missing required files,
- serialization/dumping back to YAML,
- discovery of world-specific settings sections.

## ModuleUpdate and Bootstrapping

A recurring pattern in entry points is:
- import `ModuleUpdate`
- call `ModuleUpdate.update()`

This is part of Archipelago's startup/bootstrap behavior.

Practical purpose:
- ensure requirements are present,
- pick up world-specific requirements files,
- make source-based execution more self-healing.

This is why many top-level scripts should be treated as managed entry points rather than plain library modules.

## WebHost Role

Primary file:
- `WebHost.py`

The WebHost is not just a marketing website.

It is part of the actual platform model:
- serves game info and tutorials,
- hosts option pages and presets via `WebWorld` metadata,
- supports uploading/hosting sessions,
- can auto-host and auto-generate depending on configuration,
- copies per-world docs into generated static content,
- filters worlds that are not valid for web usage.

The `WebWorld` object in `AutoWorld.py` is the main world-side contract for web integration.

A world can supply:
- options page behavior,
- theme,
- bug report link,
- tutorial declarations,
- game info language support,
- option presets,
- item/location descriptions.

So a world is not just generator logic. It can also be a web-facing documentation/configuration unit.

## Tutorials and Docs as First-Class World Metadata

Official online docs and repo docs make this explicit:
- the website has global Archipelago setup/tutorial docs,
- each world is expected to ship game info and tutorial docs,
- WebHost copies and renders those docs for the site.

That matters architecturally because documentation is part of the world package shape, not just an afterthought in the repo root.

## Group Slots and Cross-Player Structures

`MultiWorld` supports groups in addition to ordinary player slots.

Groups have:
- a synthetic slot ID,
- their own world object,
- membership sets,
- possible item pool/locality/replacement behaviors.

This is one of the less obvious pieces of the architecture: not every slot is a normal player. The server and multidata explicitly support grouped slot semantics.

## Race Mode and Versioning Boundaries

Archipelago enforces several compatibility boundaries:
- generator version,
- server minimum version,
- world-required client version,
- per-game data package checksums,
- APWorld minimum/maximum core version,
- race mode behavior.

These boundaries exist because the platform is intentionally extensible and long-lived. Worlds, clients, server, and packaged content may evolve independently.

## How to Debug by File

If the question is:

"How does a seed get built?"
- `Generate.py`
- `Main.py`
- `BaseClasses.py`
- `Fill.py`

"Why did this world load or fail to load?"
- `worlds/__init__.py`
- `worlds/AutoWorld.py`
- the world's own `__init__.py`
- `docs/apworld specification.md`

"What methods can a world implement?"
- `worlds/AutoWorld.py`
- `docs/world api.md`

"What does the server expect from a client?"
- `docs/network protocol.md`
- `NetUtils.py`
- `CommonClient.py`
- `MultiServer.py`

"What is actually inside the generated session file?"
- `Main.py` multidata writing logic

"Where should a client get game metadata from?"
- `worlds/network_data_package`
- `NetUtils.py`
- `docs/network protocol.md` data package section

"How do website docs/options get attached to a world?"
- `worlds/AutoWorld.py` `WebWorld`
- `WebHost.py`
- world-local `docs/`

## Rules of Thumb

These are the main architecture rules I should keep in mind when working in Archipelago:

1. Generation and hosting are separate phases.
- Generation creates placements and metadata.
- Hosting synchronizes a pre-generated session.

2. `MultiWorld` is the real unit of generation.
- Individual world objects only contribute their slice.

3. A world is Archipelago's plugin model.
- It defines game-specific data, logic, output, and optional web metadata.

4. Stage ordering matters.
- If a world mutates the wrong thing in the wrong stage, generation will break in hard-to-diagnose ways.

5. The server is generic.
- Most game-specific logic should already be encoded into multidata, slot data, item/location IDs, and world client behavior.

6. The protocol is intentionally language-agnostic.
- Python is the reference implementation, not the exclusive implementation.

7. Data package and slot data serve different purposes.
- Static metadata vs seed-specific client necessities.

8. WebHost is part of the platform, not an unrelated side app.
- Worlds can project themselves into website docs, options pages, and tutorials.

9. Settings and options are distinct.
- `host.yaml` is not the same thing as player YAMLs.

10. Events are generation-only logic tools.
- They are often the cleanest way to model progress state transitions.

## Short Mental Model

If I need to compress all of Archipelago into one paragraph:

Archipelago is a plugin-driven multiworld randomizer platform where each game implements a `World` that contributes typed options, items, locations, logic, output generation, and optional web metadata into a shared `MultiWorld`. `Generate.py` and `Main.py` turn player YAMLs plus settings into a seeded multiworld graph, fill it with valid item placements, and emit both player-specific output files and a compressed `.archipelago` session artifact. `MultiServer.py` then hosts that generated session over a generic WebSocket JSON protocol defined in `NetUtils.py` and documented in `docs/network protocol.md`, while clients built on `CommonClient.py` or custom implementations use data packages, slot data, and packet exchange to synchronize checks, received items, hints, chat, and shared state. The `worlds` package and `AutoWorld` metaclass system are the architectural center because they are what let Archipelago treat supported games as loadable, versioned, partially web-aware plugins rather than hardcoded cases.

## Source Files Most Worth Memorizing

If I only revisit a short list, use these:

- `Launcher.py`
- `Generate.py`
- `Main.py`
- `MultiServer.py`
- `CommonClient.py`
- `NetUtils.py`
- `BaseClasses.py`
- `Fill.py`
- `settings.py`
- `worlds/__init__.py`
- `worlds/AutoWorld.py`
- `WebHost.py`
- `docs/world api.md`
- `docs/network protocol.md`
- `docs/apworld specification.md`

## Docs Reviewed

These were the most useful docs while writing this:

- local `README.md`
- local `docs/world api.md`
- local `docs/network protocol.md`
- local `docs/apworld specification.md`
- online `https://archipelago.gg/tutorial/`

The website tutorials page is mostly useful as confirmation that the project treats per-game setup docs and global setup docs as part of the actual platform surface, not just community extras.
