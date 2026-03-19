# Kirby AM POC Workflow

## Project Overview

This document defines the project management workflow for the Kirby & The Amazing Mirror Archipelago POC development.

## Milestone: Kirby AM POC

**Goal:** Deliver a playable proof-of-concept with shard randomization, item delivery, and Dark Mind defeat tracking.

**Target Issues:**
- Core: #35, #38, #109, #110, #117, #127, #135
- Infrastructure: #136, #137, #138, #141-#151

**Estimated Completion:** Q2 2026

## Label Taxonomy

### Feature Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `poc-core` | Blue | Core POC feature (shard randomization, item delivery, goal) |
| `memory-map` | Yellow | Native memory address mapping and verification |
| `client-protocol` | Light Blue | AP client communication and mailbox protocol |
| `rom-patch` | Purple | ROM payload and item application |

### Support Labels

| Label | Color | Purpose |
|-------|-------|---------|
| `cleanup` | Gray | Technical debt cleanup, refactoring, removal of temporary code |
| `docs` | Green | Documentation (code, protocol, guides) |
| `testing` | Teal | Test infrastructure and test writing |
| `workflow` | Orange | Project management, CI/CD, process improvements |

### Status Labels (Applied by Contributors)

| Label | Purpose |
|-------|---------|
| `blocked` | Issue is waiting on external work to complete |
| `needs-validation` | Awaiting test verification before merge |
| `ready-for-review` | PR ready for code review |

## Definition of Done (DoD)

### Minimum for All POC Issues

- [ ] Issue description clearly states problem/goal
- [ ] Issue is labeled with relevant feature label (`poc-core`, `memory-map`, etc.)
- [ ] Issue is linked to milestone (Kirby AM POC)

### For Code Changes

- [ ] Code is on a dedicated feature branch (`issue-NNN-brief-title`)
- [ ] All changes are scoped to `worlds/kirbyam/` directory
- [ ] Code follows Archipelago style guidelines
- [ ] **Changes are tested** (locally or by author before PR)
  - For client code: pytest tests pass
  - For ROM payload: validated with BizHawk on USA ROM
  - For data files: address validator tool passes
- [ ] Type hints added (where applicable)
- [ ] Docstrings document preconditions, state machines, error handling
- [ ] PR created as draft
- [ ] PR includes clear description of what was changed and why
- [ ] PR references the issue (#NNN)

### For Testing/Validation

- [ ] Author has manually tested locally (describe environment/process)
- [ ] Results documented in PR comments or linked issue
- [ ] All tests pass (pytest, linting, type checking)
- [ ] Code review completed
- [ ] Label changed to `ready-for-review`

### Before Merge

- [ ] Draft PR promoted to ready for review
- [ ] At least one approval
- [ ] All CI checks passing
- [ ] No conflicting changes with main
- [ ] Commits squashed if requested

### After Merge

- [ ] Close related issues if complete
- [ ] Update linked issues with status
- [ ] Remove `ready-for-review` label

## Workflow: Issue → PR → Merge

### 1. Issue Identification & Confirmation

```
1. Find issue in backlog
2. Confirm scope and ask clarifying questions (if any)
3. Get approval to proceed
```

### 2. Branch Creation & Implementation

```
1. Create branch: git checkout -b issue-NNN-brief-title
2. Implement changes scoped to worlds/kirbyam/
3. Write/update tests as you go
4. Validate locally (pytest, validator tool, BizHawk if needed)
```

### 3. Commit

```
1. Commit with clear message: "issue-NNN: Brief summary"
2. Message body describes what changed and why
3. Reference any related addresses, test results, or validation steps
```

### 4. Push & Create Draft PR

```
1. Push branch: git push origin issue-NNN-brief-title
2. Create draft PR targeting main
3. PR title: "issue-NNN: Brief description"
4. PR description includes:
   - What problem does this solve?
   - What files changed?
   - How was this tested?
   - Link to issue (#NNN)
5. Label PR with relevant feature labels
```

### 5. Testing & Validation

```
1. Author tests locally (describe in PR comments)
2. For client code: run pytest
3. For addresses: run validate_addresses.py
4. For ROM: verify with BizHawk on USA ROM
5. Update PR with test results
```

### 6. Mark Ready for Review

```
1. Promote draft PR to ready
2. Add label: ready-for-review
3. Request review if needed
```

### 7. Code Review & Merge

```
1. Address any review feedback
2. All checks passing
3. Merge when approved
4. Delete feature branch
```

## Project Board Organization

### Columns

| Column | Purpose |
|--------|---------|
| Backlog | Issues not yet started |
| In Progress | Issues being worked (one per developer) |
| Testing | Issues awaiting test results or validation |
| Ready for Review | PRs ready for code review |
| Done | Completed and merged |

### How to Use

- **Start work:** Move to In Progress
- **Create PR:** Move to Testing  
- **PR ready:** Move to Ready for Review
- **After merge:** Move to Done

## Communication

### During Development

- Comment on issue/PR with blockers or questions
- Cross-reference related issues
- Link to workbook findings or test results

### Before Merging

1. Add comment to related issue: "Addressed by PR #NNN"
2. If blocking other work, comment on blocked issue
3. Request review explicitly if needed

## Standards

### Branching

- Always branch from `main`
- Branch name format: `issue-NNN-brief-title` (kebab-case)
- Delete after merge

### Commits

- One logical change per commit
- Clear, descriptive message
- Reference issue in commit body if multiple changes

### Code Style

- Follow Archipelago conventions (see upstream style guide)
- Type hints on all async/method signatures
- Docstrings with preconditions, postconditions, state machines
- Comments for non-obvious logic

### Testing

- Unit tests for logic (pytest, use fixtures from conftest.py)
- Integration tests for protocol sequences
- Manual validation on BizHawk for ROM-related changes
- Address validator tool for any address changes

### Documentation

- PROTOCOL.md for client/ROM communication contract
- Class/method docstrings for code behavior
- README updates if user-facing changes
- Comments above complex state machines

## Scope Guardrails

### In Scope (Allowed)

- ✅ `worlds/kirbyam/**` — All Kirby AM world code
- ✅ `worlds/kirbyam/data/` — Data files (JSON, addresses)
- ✅ `worlds/kirbyam/test/` — Test infrastructure
- ✅ `worlds/kirbyam/PROTOCOL.md` — Protocol documentation

### Out of Scope (Requires Approval)

- ❌ Changes to `worlds/` (other worlds)
- ❌ Changes to core Archipelago code
- ❌ Changes to `MultiServer.py`, `CommonClient.py`, etc.
- ⚠️ Changes outside `worlds/kirbyam/` require explicit discussion

### Approval Process

If changes outside scope are needed:
1. Comment on issue with justification
2. Get lead approval before implementation
3. Document in merge commit why change was necessary

## Tools & Commands

### Testing

```bash
# Run all Kirby AM tests
pytest worlds/kirbyam/test/ -v

# Run single test
pytest worlds/kirbyam/test/test_client.py::test_poll_locations_single_shard -v
```

### Validation

```bash
# Validate addresses.json
python worlds/kirbyam/tools/validate_addresses.py

# Type checking (once set up)
mypy worlds/kirbyam/client.py
```

### Branches

```bash
# Create branch
git checkout -b issue-NNN-brief-title

# Push branch
git push origin issue-NNN-brief-title

# Switch back to main
git checkout main
git pull origin main
```

### PRs

```bash
# Create draft PR
gh pr create --draft --base main --title "issue-NNN: Title" --body "..."

# Promote to ready
gh pr ready <PR_NUMBER>

# List PRs
gh pr list --base main
```

## Questions?

Refer to:
- Archipelago docs: `docs/adding games.md`, `docs/world api.md`, `docs/apworld specification.md`
- Kirby AM protocol: `worlds/kirbyam/PROTOCOL.md`
- Test patterns: `worlds/kirbyam/test/conftest.py`
