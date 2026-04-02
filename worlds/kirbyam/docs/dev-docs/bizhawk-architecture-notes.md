# BizHawk Architecture Notes

This is a working reference for understanding how BizHawk actually works in the local checkout at `D:\KirbyProject\bizhawk`.

It is intentionally biased toward the runtime and extension points that matter when reading code, debugging behavior, or integrating something into EmuHawk. It is not a full user manual.

## Executive Summary

BizHawk is not "one emulator." It is a frontend plus a large set of emulation cores and support libraries.

The main desktop application is EmuHawk:
- EmuHawk is the WinForms frontend.
- It owns the window, menus, rendering surface, input plumbing, movies, savestates, tools, Lua, and external APIs.
- It does not hardcode one emulator implementation. Instead, it loads a core implementing common interfaces.

The core model is service-driven:
- Every active emulator implements `IEmulator`.
- Most optional functionality is exposed as services or companion interfaces such as video, audio, memory domains, tracing, debugging, save RAM, savestates, etc.
- The frontend and tools discover those capabilities at runtime instead of assuming all cores support everything.

Core selection is mostly reflection-driven:
- BizHawk scans types implementing `IEmulator`.
- Each core declares metadata through attributes.
- ROM loading decides a system, selects candidate cores for that system, sorts them by preference/priority, and tries them until one succeeds.

The frontend is stateful and layered:
- `Program.cs` boots the process, parses CLI flags, loads config, and initializes the renderer.
- `MainForm.cs` wires together input, display, firmware handling, movies, tools, networking helpers, and ROM loading.
- `RomLoader.cs` is the central dispatcher that turns a file/disc/archive into a `GameInfo` plus a live core instance.

## High-Level Mental Model

Think of BizHawk as five major layers:

1. Frontend/application layer
- Main app: EmuHawk.
- UI, menus, config, hotkeys, OSD, tool windows, scripting host.

2. Shared client/runtime layer
- Common code used by the frontend and tools.
- ROM loading, command-line parsing, config serialization, movies, savestates, APIs, Lua helpers.

3. Emulation abstraction layer
- Shared interfaces like `IEmulator`, service providers, controller definitions, memory interfaces, tracing/debugging contracts.

4. Core implementations
- Concrete emulators for systems.
- Some are pure C#.
- Some wrap native libraries.
- Some run through Waterbox or other host/adaptor layers.

5. Native/runtime support
- Audio/video backends, native DLLs, disc handling, archive handling, Waterbox, libretro bridge, bundled unmanaged cores.

## Repository Map

The most important directories for understanding "how BizHawk works" are:

- `bizhawk/src/BizHawk.Client.EmuHawk`
  - Main frontend application.
  - Startup, window lifecycle, menus, runloop integration, tool management, Lua console UI.

- `bizhawk/src/BizHawk.Client.Common`
  - Shared client logic.
  - Command-line parsing, config, movies, savestates, Lua libraries, public API classes, ROM loading helpers.

- `bizhawk/src/BizHawk.Emulation.Common`
  - Core-facing interfaces and service abstractions.
  - This is the contract layer between frontend/tools and cores.

- `bizhawk/src/BizHawk.Emulation.Cores`
  - Concrete emulator implementations and core-loading infrastructure.
  - Includes `CoreInventory.cs`, Waterbox support, console/computer cores, libretro adapters, etc.

- `bizhawk/src/BizHawk.Emulation.DiscSystem`
  - Disc parsing/identification/helpers.

- `bizhawk/src/BizHawk.Bizware.*`
  - Graphics, audio, and input support libraries used by the frontend.

- `bizhawk/Assets`
  - Default controller definitions, scripts, shaders, databases, firmware-related assets, and packaging assets.

- `bizhawk/External*`, `bizhawk/libHawk`, `bizhawk/waterbox`, `bizhawk/submodules`
  - Native or semi-external components used by specific cores or runtime systems.

## What Starts First

Primary entry point:
- `src/BizHawk.Client.EmuHawk/Program.cs`

What happens during startup:

1. Very early process checks
- EmuHawk requires a 64-bit process.
- On Windows, it sets up DLL resolution and cleans Mark-of-the-Web metadata from bundled DLLs/EXEs in the `dll` directory.
- It checks that the VC++ runtime is available.

2. Process-wide helpers are initialized
- Temp file management starts.
- Archive dearchival is configured via SharpCompress.

3. CLI arguments are parsed
- `BizHawk.Client.Common/ArgParser.cs`
- This uses `System.CommandLine` and supports ROM paths, Lua scripts, movie files, savestate loading, A/V dumping, fullscreen/chromeless startup, IPC endpoints, user data injection, and more.

4. Config is loaded
- The default config path is `config.ini` beside the executable unless overridden with `--config`.
- Version mismatches are detected.
- Corrupt configs are deleted and regenerated.
- Defaults are resolved immediately after load.

5. Display backend is selected
- EmuHawk tries the configured display method.
- If initialization fails, it falls back across Direct3D11, OpenGL, and eventually GDI+ depending on platform.

6. WinForms main form is created
- `MainForm` gets the parsed CLI flags, loaded config, renderer, and shared callbacks.
- At this point the app is still not tied to a real emulation core; it starts with a `NullEmulator` and later swaps in a real core.

## What MainForm Owns

Primary implementation:
- `src/BizHawk.Client.EmuHawk/MainForm.cs`

`MainForm` is the orchestration center of the running app. It owns or wires together:

- `InputManager`
  - Reads host input, hotkeys, mouse state, autofire, and controller mappings.

- `FirmwareManager`
  - Resolves required firmware/BIOS files for cores.

- `MovieSession`
  - Handles movie playback/recording state, input latching, queueing movies before ROM load, timeline behavior across savestates, rerecord accounting.

- `DisplayManager`
  - Presents video from the active core.
  - Manages rendering surface/backend behavior.

- `ExternalToolManager`
  - Scans the external tools directory for .NET assemblies implementing `IExternalToolForm` and annotated with `[ExternalTool]`.

- `ToolManager`
  - Loads built-in and external tools, injects services/APIs, and tracks open tool forms.

- Networking helpers
  - Optional HTTP, MMF, and socket IPC endpoints used by APIs/Lua integrations.

- OSD/HUD, menus, status bar, quicksave UI, rewind integration, screenshotting, A/V dumping, savestate operations.

Important point: `MainForm` is not just a view. It is the runtime coordinator for most user-facing systems.

## The Core Contract

Primary interface:
- `src/BizHawk.Emulation.Common/Interfaces/IEmulator.cs`

`IEmulator` is the minimum contract for a BizHawk core. Key responsibilities:

- Exposes an `IEmulatorServiceProvider` via `ServiceProvider`.
- Exposes a stable `ControllerDefinition`.
- Advances emulation one frame via `FrameAdvance(IController controller, bool render, bool renderSound = true)`.
- Reports current frame count and system ID.

This is intentionally small. BizHawk does not require every core to implement every advanced feature.

Optional capabilities are surfaced separately, typically as interfaces or services, for example:
- `IVideoProvider`
- `ISoundProvider`
- `IStatable`
- `ISaveRam`
- `IMemoryDomains`
- `IDebuggable`
- `ITraceable`
- `IInputPollable`

That design matters because tools and APIs can ask "does the current core support X?" and adjust behavior accordingly.

## Services and Injection

Primary implementations:
- `src/BizHawk.Emulation.Common/ServiceInjector.cs`
- many cores register services through `BasicServiceProvider`

BizHawk uses service injection heavily.

Pattern:
- A core creates a service provider, often `BasicServiceProvider(this)`.
- It registers optional services such as memory domains, video, sound, tracing, etc.
- Frontend tools/APIs use `ServiceInjector` to populate properties marked as required or optional services.

Why it exists:
- Avoids hardcoding dependencies from tools to specific cores.
- Lets a tool activate only when the active core provides what it needs.
- Keeps core-specific capability checks centralized in the service model.

This is one of the main architectural ideas to retain: BizHawk is interface-heavy at the boundary, not inheritance-heavy.

## How Core Discovery Works

Primary implementation:
- `src/BizHawk.Emulation.Cores/CoreInventory.cs`

`CoreInventory` scans available types and builds an index of cores by system ID.

How a type becomes a core:
- It implements `IEmulator`.
- It has a `CoreAttribute` declaring metadata such as the core name.
- It has a `CoreConstructorAttribute(system)` on one or more constructors.

`CoreInventory` stores:
- Core type.
- Core name.
- Constructor info.
- Declared priority.
- Settings and sync settings types inferred from constructor shape.

Two constructor styles are supported:
- New style: a single `CoreLoadParameters<TSettings, TSyncSettings>` argument.
- Legacy style: positional constructor parameters such as `comm`, `game`, `rom`, `settings`, `syncsettings`, `extension`, etc.

Core creation is reflection-based:
- `CoreInventory.Core.Create(...)` maps the `RomLoader` inputs into the constructor shape.
- If the constructor throws, BizHawk rethrows the underlying exception rather than the reflection wrapper.

## How a ROM Becomes a Running Core

Primary implementation:
- `src/BizHawk.Client.Common/RomLoader.cs`

This file is the center of actual game loading.

Responsibilities of `RomLoader`:
- Handle plain ROM files, discs, archives, XML bundles, and advanced open modes.
- Identify the game/system from hashes, disc metadata, extension rules, or explicit user selection.
- Ask the frontend for core settings and sync settings through callbacks.
- Build `CoreInventoryParameters` for core construction.
- Decide which core(s) to try.
- Return the winning `IEmulator` instance plus `GameInfo` and canonical file path.

The rough flow is:

1. Normalize/open the file
- Handles archives and archive member selection.
- Tracks canonical full path.

2. Detect content type
- ROM asset, disc asset, XML bundle, libretro case, etc.

3. Determine target system
- Via database/hash/identifier logic.
- Via disc type detection for optical media.
- Via extension fallback rules if detection is ambiguous.
- Via explicit user or movie override where necessary.

4. Gather per-core settings
- `RomLoader` does not own settings persistence.
- It raises `OnLoadSettings` and `OnLoadSyncSettings` so the frontend can supply the right settings object for the candidate core type.

5. Build a `CoreComm`
- This is the communication bundle passed into cores for frontend-facing callbacks/dependencies.

6. Choose core candidates
- If a core is forced by movie or explicit option, try only that.
- Otherwise, get all cores for the system from `CoreInventory`.
- Sort them by:
  - user preferred core,
  - game database forced core,
  - declared core priority.

7. Try candidate cores in order
- If `DontTryOtherCores` is false, BizHawk can fall through to other candidate cores on non-firmware, non-internal-core exceptions.
- Missing firmware and certain internal failures are treated as hard stops.

One important runtime fact:
- The frontend can request deterministic emulation during load, especially when a movie is queued.

## How MainForm Swaps to the New Core

Relevant logic lives in `MainForm.LoadRom(...)`.

What happens after `RomLoader` succeeds:
- The previous emulator is disposed.
- `Emulator` becomes `loader.LoadedEmulator`.
- `Game` becomes `loader.Game`.
- Recent core history is updated.
- `InputManager.SyncControls(...)` is called against the new core and movie session.
- ROM metadata, multi-disc state, and system-specific post-load behavior are refreshed.
- Tools and APIs are expected to rebind against the new emulator/service provider.

This "swap" behavior is why most higher-level systems refer to the current emulator indirectly rather than caching assumptions forever.

## The Per-Frame Runtime Loop

Relevant logic:
- `MainForm.cs`, frame loop around `MovieSession.HandleFrameBefore()` and `Emulator.FrameAdvance(...)`

The runtime loop roughly does this each frame:

1. Compute audio/throttle/render policy
- Respect mute, fast-forward, rewind, frame advance, AVI dumping, invisible emulation, etc.

2. Let movies prepare input
- `MovieSession.HandleFrameBefore()` selects whether input comes from the user or from the movie log, and records input if in record mode.

3. Run frontend side-effects
- RetroAchievements frame callback.
- Periodic auto-save RAM flush if enabled.

4. Advance the core
- `Emulator.FrameAdvance(InputManager.ControllerOutput, render, renderSound)`

5. Let movies react after the frame
- `MovieSession.HandleFrameAfter(...)`
- Handles end-of-playback behavior and greenzone maintenance for TAStudio-style movies.

6. Handle special cases
- Rewinding during recording can truncate the movie and increment rerecord count.
- Cheats pulse.
- Input poll / lag-frame logic may affect autofire and related systems.

The core architectural takeaway is that the frame loop is not "just call FrameAdvance." It is a coordinated choreography between frontend state machines and the core.

## Movies and TAS Behavior

Primary files:
- `src/BizHawk.Client.Common/movie/MovieSession.cs`
- `src/BizHawk.Client.Common/movie/bk2/Bk2Movie.cs`

BizHawk has a first-class movie system.

What `MovieSession` does:
- Tracks the current movie and queued movie.
- Decides whether input is user-driven or movie-driven on a given frame.
- Records input while in recording mode.
- Checks movie timeline compatibility during savestate load.
- Handles movie end actions.
- Allows a movie to influence core selection and sync settings before ROM load.

Important behavior:
- Movies can force deterministic emulation.
- Movies can effectively force a core choice.
- If a movie includes sync settings, those can be supplied during core initialization.
- Savestates and movie logs are integrated; BizHawk treats them as related state, not isolated features.

`Bk2Movie` is the normal movie container:
- BizHawk movie version metadata.
- Input log entries per frame.
- Recording, playback, truncation, and frame mutation helpers.

If you care about TAS tooling, the movie system is one of the key reasons BizHawk is architected the way it is.

## Savestates Are Aggregated Files

Primary files:
- `src/BizHawk.Client.Common/savestates/SavestateFile.cs`
- `src/BizHawk.Client.Common/Api/Classes/SaveStateApi.cs`
- `src/BizHawk.Client.EmuHawk/MainForm.cs` load/save helpers

A BizHawk savestate is more than raw core memory.

`SavestateFile` aggregates:
- Core state (`IStatable`, binary or text form)
- Screenshot/framebuffer preview
- Sync settings snapshot
- Movie input timeline data
- User data bag
- Lag log for TAS projects

On save:
- Core state is written.
- Optional screenshot is embedded.
- Sync settings are serialized.
- Active movie state is embedded when relevant.
- User bag data is stored.

On load:
- BizHawk checks version compatibility.
- It checks sync settings compatibility.
- If a movie is active, it verifies timeline compatibility before loading the core state.
- Then it loads the core state and only afterward restores movie-related state.

This design explains why savestate support is stricter than many emulators:
- It is trying to preserve deterministic tool workflows, not just restore gameplay.

The Lua/API save-state surface is a thin wrapper over `MainForm` operations, not a separate save implementation.

## Configuration Model

Representative file:
- `src/BizHawk.Client.Common/config/Config.cs`

Config is broad and central.

It includes:
- Preferred core selection per system.
- Controller defaults.
- path configuration.
- firmware overrides.
- display settings.
- recent files/movies/cores.
- save-state behavior.
- input/hotkey behavior.
- many frontend/runtime options.

Important architectural note:
- Config influences load-time behavior directly, especially core selection, path resolution, display mode, and feature toggles.
- Some settings are global frontend settings.
- Some settings are per-core or core sync settings and are fetched separately during core creation.

Core sync settings are especially important because BizHawk uses them as part of the determinism boundary.

## APIs Exposed to Tools and Lua

Primary files:
- `src/BizHawk.Client.EmuHawk/Api/ApiManager.cs`
- `src/BizHawk.Client.Common/Api/ApiContainer.cs`
- `src/BizHawk.Client.EmuHawk/tools/ToolManager.cs`

BizHawk exposes a set of external APIs to tool windows and Lua.

How it works:
- `ApiManager` scans sealed types implementing `IExternalApi` interfaces.
- When the active emulator changes, the API container is rebuilt against the current `ServiceProvider` and runtime objects.
- Constructor arguments come from frontend-owned objects such as main form, display manager, input manager, movie session, tool manager, config, emulator, and game.
- Required/optional emulator services are injected with `ServiceInjector`.

Important consequence:
- APIs are not global static singletons independent of the core.
- They are bound to the currently loaded emulator and its service set.

This is why APIs like memory, save states, GUI, emulation state, etc. can gracefully vary by core capability.

## Tool System

Primary files:
- `src/BizHawk.Client.EmuHawk/tools/ToolManager.cs`
- `src/BizHawk.Client.EmuHawk/tools/ExternalToolManager.cs`

There are two broad tool categories:

1. Built-in tools
- Created by `ToolManager`.
- Can receive injected services and injected BizHawk external APIs.
- Usually depend on `IToolForm` and often `ToolFormBase`.

2. External tools
- DLLs dropped into the configured external-tools directory.
- Discovered by `ExternalToolManager`.
- Must reference BizHawk assemblies.
- Must contain a type implementing `IExternalToolForm` and marked with `[ExternalTool]`.
- Can declare applicability restrictions so the menu item is disabled when the current core/game is incompatible.

Notable design detail:
- External tools are not just arbitrary plugins loaded blindly.
- BizHawk validates shape, applicability, and trust heuristics before enabling them.

## Lua Integration

Representative files:
- `src/BizHawk.Client.EmuHawk/tools/Lua/LuaConsole.cs`
- `src/BizHawk.Client.Common/lua/LuaSandbox.cs`
- `src/BizHawk.Client.Common/lua/CommonLibs/*`

Lua is a major integration surface.

What exists:
- Lua console UI in EmuHawk.
- A library layer exposing BizHawk functionality to scripts.
- Script lifecycle management, registered functions, documentation/autocomplete, and callback hooks.

How it is wired:
- `LuaConsole.Restart()` rebuilds its API container against the current emulator/service provider.
- Existing scripts are stopped/restarted as needed when the core changes.
- `LuaSandbox` runs Lua code with environment protections and controlled current-directory behavior.

Lua libraries expose areas such as:
- GUI drawing
- joypad/input
- memory access
- save states
- movies
- SQLite/user data
- game info
- events
- some system-specific helper libraries

Practical takeaway:
- Lua is not bolted on. It is integrated deeply enough to participate in runtime state changes, savestate callbacks, and IPC features.

## Waterbox and Native Core Hosting

Representative file:
- `src/BizHawk.Emulation.Cores/Waterbox/WaterboxCore.cs`

BizHawk does not only run pure managed cores.

Waterbox is one of the important hosting models for native cores:
- It creates a `WaterboxHost`.
- It uses invocation adapters to call unmanaged core code safely.
- It enumerates memory areas exposed by the native core.
- It synthesizes `IMemoryDomains` from those areas.
- It can seal the host after setup for stronger runtime guarantees.

This is a strong hint about the project philosophy:
- BizHawk wants tight frontend tooling even for native cores.
- So native memory/state is wrapped back into the same service model used by managed cores.

Other cores may use different native adapters, but the architectural goal is similar: normalize capabilities back into BizHawk interfaces/services.

## Firmware Handling

`MainForm` creates a `FirmwareManager` and `RomLoader` treats missing firmware as a first-class load failure.

Operationally this means:
- Firmware requirements are part of the core load contract.
- Missing firmware is not treated as a soft "maybe another core will work" error in the same way generic constructor failures can be.
- Config and path settings directly affect whether a core is loadable.

For systems with BIOS/firmware requirements, this is part of the root-cause path whenever loading fails.

## Build and Runtime Environment Notes

From the repo docs and project files:
- Main solution: `BizHawk.sln`
- Main frontend project: `src/BizHawk.Client.EmuHawk/BizHawk.Client.EmuHawk.csproj`
- EmuHawk targets `.NET Framework 4.8`.
- The project also relies on the `.NET 8.x` SDK for current development workflows/build tooling.
- Windows is the primary platform.
- Linux is supported through Mono for the frontend runtime.
- macOS is not a supported current target for mainline EmuHawk.

Build entry points called out by the repo:
- Windows: `dotnet build BizHawk.sln`
- Unix: `Dist/BuildRelease.sh`

## What to Read First When Debugging

If the question is...

"Why did startup fail?"
- `Program.cs`
- `ArgParser.cs`
- config loading paths
- renderer initialization

"Why did this ROM choose this core?"
- `RomLoader.cs`
- `CoreInventory.cs`
- `Config.cs` preferred cores
- database/game metadata affecting `ForcedCore`

"Why is this tool unavailable?"
- `ToolManager.cs`
- `ExternalToolManager.cs`
- `ServiceInjector.cs`
- the current core's registered services

"Why does savestate load/save behave oddly?"
- `SavestateFile.cs`
- `MainForm` save/load helpers
- `MovieSession.cs`
- the core's `IStatable` implementation

"Why did Lua/script behavior change after reboot/load?"
- `LuaConsole.cs`
- `LuaSandbox.cs`
- `ApiManager.cs`
- `ToolManager.cs`

"Why does this movie require a different core or sync settings?"
- `MovieSession.cs`
- `Bk2Movie.cs`
- `RomLoader.cs`
- `MainForm.LoadRom(...)`

## Architecture Rules of Thumb

These are the main rules I should remember when reading or changing BizHawk:

1. EmuHawk is a coordinator, not the emulator.
- Most emulation behavior lives behind `IEmulator` and optional services.

2. Core capability is dynamic.
- Never assume every core supports memory domains, tracing, savestates, or identical settings.

3. ROM loading is policy-heavy.
- System detection, preferred cores, firmware, movies, and sync settings all influence final core selection.

4. Movies and savestates are deeply integrated.
- Determinism and TAS workflows are first-class concerns.

5. Tools and Lua are runtime-bound to the active core.
- If a core changes, APIs/services need to be rebound.

6. Native cores are normalized back into common BizHawk abstractions.
- Waterbox is a good example of that pattern.

7. Config is not cosmetic.
- It materially affects load behavior, core preference, paths, display, and tooling.

## Source Files Most Worth Memorizing

If I only revisit a short list, use these:

- `src/BizHawk.Client.EmuHawk/Program.cs`
- `src/BizHawk.Client.EmuHawk/MainForm.cs`
- `src/BizHawk.Client.Common/ArgParser.cs`
- `src/BizHawk.Client.Common/RomLoader.cs`
- `src/BizHawk.Client.Common/movie/MovieSession.cs`
- `src/BizHawk.Client.Common/savestates/SavestateFile.cs`
- `src/BizHawk.Emulation.Common/Interfaces/IEmulator.cs`
- `src/BizHawk.Emulation.Common/ServiceInjector.cs`
- `src/BizHawk.Emulation.Cores/CoreInventory.cs`
- `src/BizHawk.Client.EmuHawk/tools/ToolManager.cs`
- `src/BizHawk.Client.EmuHawk/tools/ExternalToolManager.cs`
- `src/BizHawk.Client.EmuHawk/Api/ApiManager.cs`
- `src/BizHawk.Client.EmuHawk/tools/Lua/LuaConsole.cs`
- `src/BizHawk.Emulation.Cores/Waterbox/WaterboxCore.cs`

## External Docs Reviewed

These were useful as confirmation/context while writing this:

- BizHawk repo `README.md`
  - project scope, platforms, major features, build/use notes

- BizHawk repo `contributing.md`
  - project layout, build expectations, EmuHawk positioning inside the solution

- BizHawk wiki: `Dependencies`
  - confirms the main solution dependency graph and library split

- BizHawk wiki: `Command-line arguments`
  - complements what is visible in `ArgParser.cs`

## Final One-Paragraph Model

BizHawk is a frontend-centered, service-oriented emulator platform where EmuHawk owns UI/runtime coordination and dynamically hosts one core at a time behind common interfaces. ROM loading determines the system and candidate cores, constructs the chosen core with per-core settings and frontend communication objects, then the frame loop coordinates user input, movie state, achievements, audio/video policy, and tooling around repeated `FrameAdvance(...)` calls. Savestates, movies, Lua, and tools are all tightly integrated with the active core through service injection and API containers, which is why BizHawk feels more like a programmable emulation framework than a single monolithic emulator.
