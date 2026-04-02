# Reference Repos Notes

This note summarizes the additional reference repositories and how useful they are for `D:\KirbyProject\Archipelago-kirbyam\worlds\kirbyam` work.

The short version:

1. `kamrandomizer` is the most directly useful for current Archipelago runtime work.
2. `Amazing-Mirror-Randomizer` is a major structural reference for items, rooms, mirrors, and randomizer-era ROM knowledge, but it targets the JP ROM and therefore needs mapping caution.
3. `KatAM-Object-Editor` is a useful reverse-engineering support tool for object and room layout inspection, but it is less directly reusable as logic or protocol source.

## Overall Relevance Ranking

### 1. `D:\KirbyProject\kamrandomizer`

Highest immediate relevance.

Why:

- targets the US ROM, which matches the current KirbyAM Archipelago world
- contains concrete enemy, miniboss, and object ability addresses already expressed as ROM offsets
- its data aligns closely with the enemy copy-ability runtime patch system already present in `worlds/kirbyam/enemy_ability_runtime_patch.py`
- documents the workflow used to discover ability addresses, which helps validate or extend the current patch tables

Best use cases:

- expanding enemy copy-ability randomization
- verifying current enemy/object ability source tables
- finding missing enemy/object grant addresses
- checking whether an ability source should be randomized, excluded, or grouped differently

### 2. `D:\KirbyProject\Amazing-Mirror-Randomizer`

Very strong reference, but not version-aligned by default.

Why:

- contains large structured datasets for items, chests, mirrors, rooms, stands, and other randomizable game content
- expresses a lot of useful ROM knowledge in JSON instead of scattering it through code
- includes mirror graph and chest data that are useful for understanding topology and content placement
- appears to be one of the main historical sources of randomizer-era KATAM reverse-engineering knowledge

Main limitation:

- the README explicitly says it targets the Japanese ROM, not the US ROM
- any direct ROM offsets or room indices must be translated carefully before using them in Archipelago-kirbyam

Best use cases:

- understanding the shape of item/chest datasets
- studying mirror and entrance structures
- finding candidate room/object/chest mappings to reconcile against KATAM decomp and US data
- cross-checking assumptions about ability stands, big chests, and mirror network semantics

### 3. `D:\KirbyProject\KatAM-Object-Editor`

Useful, but more as a support instrument than as a design source.

Why:

- exposes object parameter tables and room object lists across multiple ROM versions
- contains useful hardcoded offsets for object parameter blocks and room object parsing
- helps inspect how objects are laid out inside room data and how room lists are traversed

Main limitation:

- this is an editor application, not a logic model or randomizer framework
- it contributes less to Archipelago protocol, item generation, or world-graph logic than the other two repos
- it is best for lookup and confirmation, not as the primary source of gameplay logic or AP integration behavior

Best use cases:

- investigating object IDs and their parameters
- confirming room object list structure
- locating edit points for chests, stands, enemies, and special objects
- comparing JP/US/EU object parameter table bases

## Repo-By-Repo Findings

## `kamrandomizer`

### What it is

`kamrandomizer` is a standalone Amazing Mirror randomizer focused on copy abilities granted by enemies and objects. It targets the US ROM and provides curated ROM addresses for many ability sources.

Top-level evidence:

- `README.md` describes it as a randomizer for enemy/object abilities on the US ROM.
- `Documentation.txt` explains how ability addresses were found and points to a companion address sheet.
- `kamrandomizer.py` contains the core data tables and ROM patching logic.

### What is inside

Most of the technical value is concentrated in `kamrandomizer.py`.

Important structures there:

- `abilities`: friendly names to numeric ability IDs
- `normalEnemies`: enemy name -> ROM address list + default ability
- `miniBosses`: miniboss ability sources
- `objects`: spawned object ability sources such as Bombar bombs, Dark Mind stars, Moley objects, Wiz objects, and so on

This is extremely close in purpose to the current Archipelago enemy ability runtime patch module.

The repo also documents important discovery rules, including the note in `Documentation.txt` that ability addresses can often be found by watching enemy/object spawn addresses and adding `6` to the spawn address.

### Why it matters to Archipelago-kirbyam

This repo is effectively a precursor dataset for `worlds/kirbyam/enemy_ability_runtime_patch.py`.

The overlap is obvious:

- enemy names match current Archipelago source keys
- ROM offsets match the style of the current runtime patch writes
- miniboss and boss-spawned object distinctions match the current option toggles

This makes it the strongest external reference for any work in these areas:

- adding new enemy/object sources to the runtime patch
- verifying existing address coverage
- reasoning about which sources are “enemy”, “miniboss”, or “boss_spawned”
- validating native ability IDs against known behavior

### Limits

- it is focused on ability randomization, not whole-world generation
- it does not define an Archipelago-style location model
- it is not a source for client mailbox protocol, slot data, or BizHawk integration

So this repo is highly relevant, but only to the enemy/object ability part of the system.

## `Amazing-Mirror-Randomizer`

### What it is

This is a broader multi-feature randomizer for the Japanese release of Amazing Mirror.

The README says it supports randomization of:

- rooms
- items and chests
- spray palettes
- ability stands
- music

Compared with `kamrandomizer`, this repo covers much more of the game's world structure.

### What is inside

The repo is built around Python scripts plus a `JSON/` directory containing structured game data.

Key files:

- `amrRandomizer.py`: main entrypoint/orchestrator
- `amrItems.py`: item/chest randomization
- `amrMirrors.py`: mirror, cannon, and warp-star randomization
- `amrStands.py`: ability stand logic
- `amrMinibosses.py`: miniboss randomization
- `amrShared.py`: raw ROM write helpers
- `JSON/items.json`: item/chest address and room datasets
- `JSON/mirrors.json`: mirror network data and destination graph

The JSON files are the most useful part for the current Archipelago work.

### Why it matters to Archipelago-kirbyam

This repo is a strong reference for data modeling.

#### Items and chests

`JSON/items.json` contains categorized entries like:

- `AbilityStand`
- `BigChest`
- `SmallChest`
- `Cherry`
- `Drink`
- `Meat`
- `Tomato`
- `Battery`
- `1Up`
- `Candy`

Each entry carries arrays for:

- randomized item values
- ROM addresses
- coordinates
- room indices

That is valuable because Archipelago-kirbyam still needs precise reconciliation between location concepts, room numbering, and reward semantics.

#### Mirror and entrance structure

`JSON/mirrors.json` is a rich graph-like dataset describing:

- mirror endpoints
- ROM offsets
- one-way vs two-way types
- possible exits
- descriptive labels

This is highly relevant to future entrance logic, mirror randomization, or simply understanding how the native mirror network is encoded.

#### Ability stands and content placement

This repo also preserves practical randomizer knowledge about ability stands and other interactables that are not yet fully integrated into Archipelago-kirbyam.

### Limits

The biggest limitation is version mismatch.

The README explicitly states this repo currently works with the Japanese ROM. For Archipelago-kirbyam, which is using the US ROM and US-oriented reverse-engineering data, this means:

- direct ROM offsets cannot be assumed valid
- room indices may require translation
- any location/address mapping must be reconciled against KATAM decomp and US datasets

So this repo should be treated as a structural reference, not an authoritative direct patch source.

### Practical recommendation

Use this repo when you need to answer questions like:

- what kinds of items/chests did prior randomizers model?
- how were mirrors structured as a graph?
- what room-level datasets already exist?
- where did older randomizer work distinguish big chests, ability stands, or warp destinations?

Do not directly copy addresses from it into the Archipelago world without version reconciliation.

## `KatAM-Object-Editor`

### What it is

This is a Windows object editor for Kirby & The Amazing Mirror. The README describes it as an editor for object parameters and room-level object placement, with support for all ROM versions.

### What is inside

The most relevant code is in the `Editor/` directory.

Important files:

- `Editor/LevelDataManager.cs`
- `Editor/RoomEditor.cs`
- `Editor/ObjectParam.cs`

`LevelDataManager.cs` appears to contain:

- hardcoded room ID lists
- routines for finding room-object data
- version-specific base offsets for object parameter tables

Important example from `GetParamOffset`:

- Japanese base: `0x335E1C`
- American base: `0x351648`
- Europe base: `0x353128`

This is exactly the sort of cross-version lookup that is useful when reconciling object data.

### Why it matters to Archipelago-kirbyam

This repo is most useful when you need to inspect or confirm native object layout.

Good uses:

- locating or validating object parameter blocks
- understanding how room object lists are stored and iterated
- checking whether specific chests, enemies, stands, or other objects appear in a room
- comparing object-table layout across ROM versions

This can help with:

- adding new location families
- investigating ability stands
- confirming object spawn or parameter behavior
- validating room/object assumptions against editor-oriented tooling

### Limits

This repo is not a randomizer and not an Archipelago integration.

It does not provide:

- slot-data patterns
- AP client behavior
- mailbox protocol logic
- generation rules
- item pool modeling

So while it is useful as a technical inspection tool, it is a secondary reference rather than a primary design source.

## Best Uses In Current KirbyAM Work

If working on the current Archipelago world, use these repos in this order:

### For enemy copy-ability work

Use `kamrandomizer` first.

Why:

- US ROM
- direct ability source tables
- already conceptually aligned with current runtime patch code

### For chest, mirror, and room-structure research

Use `Amazing-Mirror-Randomizer` first, then reconcile against KATAM decomp and current US mappings.

Why:

- richer structured datasets
- broader world coverage
- useful historical randomizer knowledge

### For object-level confirmation and cross-version offsets

Use `KatAM-Object-Editor`.

Why:

- room/object editing view
- direct object parameter table bases
- useful for confirming how object lists are stored

## Recommended Trust Model

Treat the repos differently depending on the kind of question being asked.

### Safe to trust quickly

- `kamrandomizer` enemy/object ability source categories and US ROM offsets
- `KatAM-Object-Editor` object parameter base offsets by ROM version

### Useful but requires reconciliation

- `Amazing-Mirror-Randomizer` room indices
- `Amazing-Mirror-Randomizer` JP ROM offsets
- any attempt to map AMR room numbers directly onto `worlds/kirbyam/data/regions/rooms.json`

### Not the right source of truth

- any of these repos for Archipelago protocol behavior
- any of these repos for BizHawk connection behavior
- any of these repos for current slot-data contract or AP generation lifecycle

Those topics belong to `worlds/kirbyam/` itself plus the Archipelago and BizHawk references.

## Bottom Line

All three repos are relevant, but in different ways.

- `kamrandomizer` is the most directly actionable reference for current runtime patch work.
- `Amazing-Mirror-Randomizer` is the broadest structural reference and likely the best source for future chest/mirror/stand expansion, but it must be translated from JP assumptions.
- `KatAM-Object-Editor` is a strong low-level support tool for object and room inspection, but it is not a direct model for Archipelago world behavior.

If the goal is to keep building the current custom world efficiently, the practical rule is:

- start with `kamrandomizer` for ability tables
- use `Amazing-Mirror-Randomizer` for content datasets and topology ideas
- confirm low-level object details with `KatAM-Object-Editor`