# Copilot Instructions (Local Workflow Guide)

Purpose: help Copilot quickly choose the right repository, use the right notes, and follow the expected delivery workflow for Kirby and the Amazing Mirror Archipelago work.

## Scope and Intent

Use this file as an operating guide, not a hard spec.

- Primary target: `D:\KirbyProject\Archipelago-kirbyam`
- Supporting references: `Archipelago`, `bizhawk`, `katam`, and other local reference repos
- Working style: issue-driven planning, branch/PR implementation, automated review, local validation, merge

## Primary Workflow

Follow this sequence unless a prompt explicitly changes it:

1. User or team creates a GitHub issue.
2. Copilot analyzes the issue and proposes a plan of action.
3. Work is implemented on a branch and submitted through a PR.
4. Copilot GitHub review is used to improve quality.
5. User performs local testing/validation.
6. Merge after validation.

## Repository Decision Rules

### 1) `D:\KirbyProject\Archipelago-kirbyam` (Primary)

Use first for almost all implementation tasks.

Use it when:

- changing the KirbyAM world (`worlds/kirbyam/**`)
- updating generation, options, rules, groups, data JSON, tests
- changing BizHawk client behavior for KirbyAM
- updating ROM token write behavior for KirbyAM patch outputs

Why:

- this is the active integration codebase
- this repo defines what actually ships in current workflow

### 2) `D:\KirbyProject\Archipelago` (Upstream architecture reference)

Use for framework-level understanding and compatibility checks.

Use it when:

- confirming World lifecycle expectations
- checking upstream protocol/packaging patterns
- validating that KirbyAM implementation aligns with core Archipelago behavior

Why:

- provides canonical framework behavior and conventions

### 3) `D:\KirbyProject\bizhawk` (Emulator/runtime integration reference)

Use for emulator-side understanding and tooling behavior.

Use it when:

- clarifying BizHawk architecture, services, APIs, Lua integration, and runtime expectations
- diagnosing emulator-facing behavior that may affect KirbyAM client integration

Why:

- KirbyAM client reliability depends on BizHawk runtime semantics

### 4) `D:\KirbyProject\katam` (Game/decomp ground truth)

Use as low-level gameplay/memory/engine reference.

Use it when:

- validating addresses, symbols, and runtime field semantics
- understanding native game behavior that payload/client logic depends on
- reconciling assumptions about abilities, objects, room flow, or save-state semantics

Why:

- decomp context is often the strongest technical evidence for game internals

### 5) `D:\KirbyProject\kamrandomizer` (Highest-value external reference)

Use as first external reference for enemy/object ability randomization.

Use it when:

- updating enemy copy-ability runtime patch tables
- verifying enemy/miniboss/boss-spawned ability source offsets
- investigating missing ability source coverage

Why:

- US-ROM-oriented ability table knowledge aligns closely with current KirbyAM runtime patch work

### 6) `D:\KirbyProject\Amazing-Mirror-Randomizer` (Broad structural reference)

Use for data-model ideas (items/chests/mirrors/rooms/stands) with version caution.

Use it when:

- researching historical randomizer datasets and mirror graph structure
- finding candidate mappings for chest/mirror/room systems
- designing future features that need broader content coverage

Why:

- rich JSON datasets and randomizer-era structure

Caution:

- README indicates JP-ROM focus; do not copy offsets directly into US-ROM workflows without reconciliation

### 7) `D:\KirbyProject\KatAM-Object-Editor` (Inspection aid)

Use as a room/object inspection support tool.

Use it when:

- confirming object parameter table offsets by version
- inspecting room object list structure
- validating object-level assumptions for chests, enemies, stands, and interactables

Why:

- useful for low-level confirmation, but not a primary source for AP protocol or world logic

## Notes Index and How To Use It

All summary notes are in `D:\KirbyProject\local-files`.

- `bizhawk-architecture-notes.md`
- `archipelago-architecture-notes.md`
- `katam-decomp-architecture-notes.md`
- `kirbyam-world-architecture-notes.md`
- `kirbyam-game-notes.md`
- `kirby-franchise-lore-notes.md`
- `reference-repos-notes.md`

Protocol contract file (authoritative runtime contract):

- `D:\KirbyProject\Archipelago-kirbyam\worlds\kirbyam\PROTOCOL.md`

Use `PROTOCOL.md` to confirm mailbox layout, field semantics, item/location ID contracts, gameplay-gate behavior, and reconnect/ACK expectations between server, client, and ROM payload.

### Quick-open matrix by task type

- Archipelago world generation/rules/options/data task:
  - Start with `kirbyam-world-architecture-notes.md`
  - Then `archipelago-architecture-notes.md`
- Kirby & The Amazing Mirror gameplay structure/content task (rooms, mirrors, bosses, progression, collectible context):
  - Start with `kirbyam-game-notes.md`
  - Then `kirbyam-world-architecture-notes.md`
- BizHawk integration/runtime issue:
  - Start with `kirbyam-world-architecture-notes.md`
  - Then `bizhawk-architecture-notes.md`
- Address/payload/native-behavior issue:
  - Start with `kirbyam-world-architecture-notes.md`
  - Then `katam-decomp-architecture-notes.md`
- Franchise-wide flavor/easter-egg/naming/lore-tag task:
  - Start with `kirby-franchise-lore-notes.md`
  - Then `kirbyam-game-notes.md`
- External reference reconciliation (mirrors/chests/abilities/objects):
  - Start with `reference-repos-notes.md`
  - Then open the specific referenced repo files

### Note usage policy

- Treat notes as acceleration context, not source-of-truth code.
- Before implementation, confirm assumptions in the actual target repo files.
- If a note and code disagree, code wins.
- Update notes when major architectural behavior changes.
- For lore-dependent text, separate canon-safe statements from optional deep-cut references.
- Prefer `kirbyam-game-notes.md` for game-specific facts and `kirby-franchise-lore-notes.md` for cross-series thematic references.
- Treat `worlds/kirbyam/PROTOCOL.md` as protocol source-of-truth for runtime transport behavior.
- When changing mailbox fields, ID ranges, or watcher/delivery semantics, update `PROTOCOL.md` in the same change set.

## Planning and Execution Expectations

For each issue-driven task:

1. Restate the issue goal and constraints.
2. Identify impacted repo(s) and files.
3. Propose a clear step-by-step plan.
4. Implement changes in small, reviewable commits.
5. Run relevant checks/tests where feasible.
6. Prepare PR notes with risk and validation summary.

## Branch, PR, and Review Practice

- Create focused branches per issue scope.
- Keep PRs narrow and tied to explicit issue goals.
- Prefer clear commit messages describing what changed and why.
- Request Copilot GitHub review before finalizing.
- Address review findings before local validation sign-off.

## Validation and Merge Gates

Before merge:

- Code changes are consistent with issue scope.
- Required checks/tests are run (or explicitly documented if not run).
- Copilot review findings are addressed or triaged with rationale.
- User confirms local testing results.
- Merge only after above conditions are satisfied.

## Guardrails

- Default to `Archipelago-kirbyam` for edits unless task explicitly requires another repo.
- Use external repos as references; do not blindly port offsets or logic.
- For JP-vs-US data, always reconcile with current KirbyAM US-oriented implementation and KATAM evidence.
- Keep architecture and protocol assumptions explicit in PR descriptions.

## Maintenance

When workflow or architecture changes significantly, update this file and the affected notes in `D:\KirbyProject\local-files` in the same work cycle.
