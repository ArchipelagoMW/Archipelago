# KATAM Decomp Architecture Notes

This note is for rebuilding context quickly when working in `D:\KirbyProject\katam`. The repository is not a conventional game project and not just a ROM-hacking toolkit. It is a decompilation and disassembly project whose main job is to recreate the original USA build of Kirby & The Amazing Mirror as a buildable source tree while preserving byte-for-byte compatibility with the shipped ROM.

## What This Repository Is Trying To Produce

- Target ROM: `katam.gba`
- Reference ROM: Kirby & The Amazing Mirror (USA)
- Expected SHA1: `274b102b6d940f46861a92b4e65f89a51815c12c`
- Source of truth for unmatched content: `baserom.gba`

That last point matters. The repo does not yet express every byte of the game as clean C or fully named assembly. Until all code and data are ported, the original ROM is still used as a donor binary for raw included data and for validation. The build is therefore a reconstruction pipeline, not a from-scratch compilation.

## High-Level Mental Model

The project combines five kinds of content into one ROM image:

1. Decompiled C in `src/`
2. Assembly in `asm/`
3. Raw binary data included from the original ROM in `data/`
4. Converted graphics and audio assets from `graphics/` and `sound/`
5. Small helper binaries and multiboot payloads under `multi_boot/`

The build system then forces those pieces into a very specific order and address layout using `linker.ld`. Matching the original binary is the central constraint. Many decisions that look odd in a normal codebase make sense once viewed through that lens.

## Top-Level Repository Layout

### `src/`

Contains decompiled C. This is the main destination for progress. When code is moved from assembly to C and still matches, the project becomes more understandable and maintainable without changing ROM output.

Representative files:

- `src/main.c`: top-level runtime entry on the C side
- `src/agb_sram.c`: hardware support code that is still match-sensitive
- `src/m4a.c`: the audio engine glue and playback control logic
- `src/multi_boot_util.c`: multiboot transfer/session support for linked devices

### `asm/`

Contains assembly for startup code, still-undecompiled routines, and code that may be easier to keep in assembly until matching work is complete.

Representative file:

- `asm/crt0.s`: low-level startup, ROM header inclusion, interrupt setup, transition into `AgbMain`

### `data/`

Contains assembly files that use `.incbin` to splice exact binary data from `baserom.gba` into the build. This is how unmatched or not-yet-ported data is preserved.

Representative file:

- `data/data_1.s`: large blocks of raw binary copied directly from the original ROM

### `graphics/`

Holds source assets and generated asset intermediates used by the build. The Makefile plus `graphics_file_rules.mk` convert images into GBA-ready tile/palette formats.

### `sound/`

Contains song data, samples, MIDI-derived sources, and generated assembly used by the GBA music driver.

### `include/` and `constants/`

Headers, macros, hardware definitions, and shared constants used by both handwritten and decompiled code.

### `tools/`

Local helper programs the build depends on. These are built as part of the repo and are part of the decomp workflow, not incidental utilities.

Current tool directories:

- `aif2pcm/`
- `bin2c/`
- `gbafix/`
- `gbagfx/`
- `mid2agb/`
- `preproc/`
- `scaninc/`

### `scripts/`

Workflow helpers for reverse engineering and asset maintenance. In `scripts/sound/`, for example, there are utilities for naming, parsing, and matching songs and MIDI configuration.

Representative sound helpers:

- `match_next_midi.py`
- `parse_song_table.py`
- `write_midi_cfg.py`
- `rename_song.py`

### `multi_boot/`

Contains separate multiboot-related payloads or subprojects. These are built as subordinate outputs and then incorporated into the broader project flow.

Observed subdirectories include:

- `subgame_loaders/`
- `unk_8D94B9C/`
- `unk_8E1FE28/`
- `unk_8E8490C/`

This is a strong sign that the original game ships auxiliary binaries or special transfer payloads in addition to the main executable image.

## Build Prerequisites And Toolchain Expectations

The project expects a GBA-era matching toolchain, not just any modern ARM compiler.

Important prerequisites from `INSTALL.md` and the Makefile:

- A correct `baserom.gba`
- `arm-none-eabi-*` binutils and assembler tools
- `agbcc` components for matching-era C compilation
- devkitARM or equivalent devkitPro-provided GBA toolchain pieces
- local custom tools built from `tools/`

The build flow is explicitly shaped around old compiler behavior. The Makefile exposes a `MODERN` variable, but `make modern` intentionally errors with a message that modern compilers are not supported yet. That tells you the repository still relies on historical codegen quirks to match the original ROM.

## The Central Build Pipeline

The Makefile is the operational heart of the repo. Conceptually, it performs the following stages:

1. Discover sources in `src/`, `asm/`, `data/`, `sound/`, and MIDI/song directories.
2. Build helper tools listed in `make_tools.mk`.
3. Convert graphics and audio assets into GBA-compatible intermediate files.
4. Compile C through the agbcc-compatible pipeline.
5. Assemble handwritten assembly and data assembly.
6. Link everything with `linker.ld` in a fixed order.
7. Convert the ELF to a raw GBA ROM image.
8. Run `gbafix` to stamp/fix header metadata.
9. Optionally compare the final output against the expected SHA1.

The project does not treat all inputs uniformly. Different file types have different build paths because preserving exact binary output matters more than simplifying the build.

## How C Compilation Works

For C files, the Makefile does not just invoke GCC in a normal one-step compile. Instead it uses a staged pipeline involving:

- the C preprocessor
- the repo's `preproc` helper
- the matching compiler frontend (`agbcc` `cc1`)
- the assembler

This split exists because the project is trying to reproduce original object code, not merely source-level behavior. Compiler flags, preprocessing shape, and section placement all affect ROM matching.

Some objects also receive special treatment in the Makefile, such as `m4a.o`, `agb_sram.o`, and `task.o`, which is typical in decomp repos where a few files need specific flags or handling to preserve known binary output.

## How Assembly And Raw Data Fit In

There are two distinct assembly-related categories:

### Code Assembly In `asm/`

These files represent executable routines. Some may be startup code or permanently hand-maintained low-level routines, while others are placeholders for future decompilation.

### Data Assembly In `data/`

These files often contain `.incbin` directives. That means the repo is embedding exact byte ranges from `baserom.gba` into the rebuilt ROM. This is how the project stays matchable while data structures and assets are gradually understood and ported.

If you see a large `.incbin`, read it as “this region is still preserved from the original binary rather than re-expressed in source.”

## Linker Script: The Most Important File For Understanding Matching

`linker.ld` is the file that turns a pile of objects into the exact memory image the original game used. It is not a generic embedded linker script.

Important responsibilities:

- declares the GBA memory regions such as EWRAM, IWRAM, and ROM
- defines the program entry as `__start`
- controls the exact order of linked objects in `.text`
- places data into fixed regions and sections
- pins many symbols or blocks to precise addresses

This is where the project enforces binary structure. In a normal program, you often let the linker decide section packing with broad rules. In this repo, order is part of correctness. Moving one object earlier or later can shift ROM addresses, which then breaks matching even if the game still runs.

That is why source progress in decomp projects is coupled to linker choreography. The code is not fully “done” until it matches both semantically and spatially.

## Startup And Runtime Entry

The runtime begins in `asm/crt0.s`.

This file performs the low-level responsibilities expected for a GBA title:

- provides the true entry symbol `__start`
- incorporates ROM header material
- sets up stack and interrupt state
- installs or dispatches interrupt handling scaffolding
- transfers control into the C runtime entrypoint

On the C side, `AgbMain` in `src/main.c` is the core high-level entry:

```c
void AgbMain(void)
{
    GameInit();
    sub_080001CC();
    GameLoop();
}
```

That tells you the top-level execution model is straightforward:

- initialize the game
- perform additional platform or engine setup
- enter the main loop

So the startup chain is:

`__start` in assembly -> low-level platform setup -> `AgbMain` -> engine initialization -> main game loop

## Audio System Structure

The audio pipeline is split between build-time conversion and runtime playback support.

### Build-Time Audio Conversion

`audio_rules.mk` drives audio asset preparation. Its responsibilities include:

- converting audio samples with `aif2pcm`
- converting MIDI/song sources with `mid2agb`
- assembling generated song data into object files
- using MIDI configuration data such as `midi.cfg`

This is classic GBA audio tooling: authored or extracted music assets are converted into a form consumable by the game's sound driver.

### Runtime Audio Code

`src/m4a.c` is a strong anchor for the runtime audio model. It contains:

- global sound engine state like `gSoundInfo`
- music player instances such as `gMPlayInfo_0` through `gMPlayInfo_3`
- initialization via `m4aSoundInit`
- per-frame sound processing through `m4aSoundMain`
- song start/stop/continue/fade helpers

This is the Nintendo/AGB M4A-style music engine glue layer. The code sets up player tables, memory access regions, sound mode, and playback state, then drives the mixer during execution.

The important mental model is:

- build-time rules create song/sample data in the right format
- runtime M4A code loads and controls those assets through music player structs

## Graphics Asset Pipeline

Graphics conversion is handled through the main Makefile plus `graphics_file_rules.mk`.

The repo uses `gbagfx` to convert image assets into GBA-ready binary forms such as tiled 4bpp data and related generated outputs. Some rules are specialized and use exact tile-count parameters, which is common when the asset format and packing must line up with original ROM layout.

This means the graphics directory is not just source art storage. It is an input to a deterministic asset-translation pipeline whose output becomes part of the matching ROM image.

## Multiboot Support

The presence of `multi_boot/` and `src/multi_boot_util.c` means the game contains logic for GBA multiboot behavior, where a host GBA can transfer code to another device over the link cable.

`src/multi_boot_util.c` shows several important properties:

- direct interaction with serial I/O registers such as `REG_SIOCNT` and `REG_SIOMLT_SEND`
- manipulation of interrupt handlers
- coordination with Nintendo multiboot helper routines like `MultiBootMain`, `MultiBootStartMaster`, and `MultiBootCheckComplete`
- shutdown or suspension of audio and DMA around transfer sequences

That is all very hardware-specific. This subsystem is not general network code; it is tight platform code for handheld-to-handheld transfer and session management.

The separate `multi_boot/` subprojects likely contain the payloads or supporting binaries that get delivered through that mechanism.

## Local Helper Tools And Why They Matter

The custom tools are part of the architecture because the repository depends on them to convert or analyze content in ways standard toolchains do not cover.

### `preproc`

Normalizes preprocessed C into the shape expected by the historical compiler flow.

### `scaninc`

Supports dependency generation and include scanning for the mixed source/assembly environment.

### `gbagfx`

Converts graphics into GBA-native formats.

### `mid2agb`

Converts MIDI-oriented music sources into assembly or data structures usable by the sound engine.

### `aif2pcm`

Converts audio samples into PCM data appropriate for the build.

### `gbafix`

Repairs or stamps GBA ROM header data on the produced binary.

### `bin2c`

General-purpose binary-to-C conversion helper when needed by the asset or tooling pipeline.

Without these tools, the repo is incomplete. They are not optional conveniences.

## Matching And Verification Workflow

The project ships explicit support for measuring how close the source tree is to a full decomp.

### `make compare`

The Makefile supports compare mode and checks the final ROM against `katam.sha1`. This is the canonical “did the build match the target binary?” validation.

### `calcrom.pl`

This Perl script analyzes the linker map and reports how much code/data has moved into source form.

It estimates:

- bytes of code in `src/` vs `asm/`
- documented vs undocumented symbols
- data in source vs raw data sections
- remaining `.incbin` usage

That makes it a progress meter for the reverse-engineering effort, not merely a debugging script.

### `asmdiff.sh`

This helper disassembles a selected ROM address range from both `baserom.gba` and built `katam.gba`, then diffs the results.

This is a classic decomp workflow tool. When a function does not match, you narrow the address range and compare instruction output to find exactly where code generation diverges.

## How To Think About Progress In This Repo

Work usually moves in this direction:

1. Identify a region of code or data still living in assembly or raw binary.
2. Understand it well enough to name symbols, structures, and constants.
3. Port it to C or cleaner assembly.
4. Rebuild and compare.
5. Adjust code shape, compiler behavior, section placement, or data expression until the ROM still matches.

So “success” is not just functional correctness. It is functional correctness plus structural identity with the original binary.

## Practical Interpretation Of Common Files

When you reopen this repo later, use this shortcut map:

- `README.md`: confirms the target ROM identity and checksum
- `INSTALL.md`: toolchain and setup recipe
- `Makefile`: real build behavior and file-category handling
- `linker.ld`: exact layout and object ordering rules
- `asm/crt0.s`: startup path before C takes over
- `src/main.c`: top-level runtime handoff and game loop start
- `src/m4a.c`: sound driver integration
- `src/multi_boot_util.c`: link/multiboot hardware workflow
- `audio_rules.mk`: music/sample conversion pipeline
- `graphics_file_rules.mk`: image conversion pipeline
- `calcrom.pl`: decomp progress metrics
- `asmdiff.sh`: instruction-level mismatch investigation

## Bottom Line

The KATAM decomp is best understood as an exact-ROM reconstruction system. The repository is simultaneously:

- a reverse-engineered source tree
- a binary-matching build pipeline
- an asset conversion pipeline
- a measurement framework for decompilation progress

If something in the repo seems overly strict or unusually manual, assume the reason is binary matching until proven otherwise. That assumption will usually be correct.