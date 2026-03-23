# Mutation Testing for KirbyAM Logic-Heavy Modules

## Overview

Mutation testing evaluates test suite quality by introducing small bugs ("mutants") into production code and verifying whether the test suite catches them. A high mutation score indicates comprehensive assertions; low scores flag weak test coverage that might miss real bugs.

This document describes the Cosmic Ray mutation testing workflow for KirbyAM's critical modules.

## Target Modules

Mutation testing focuses on logic-heavy modules with deterministic behavior:
- `worlds/kirbyam/ability_randomization.py` — enemy ability randomization logic
- `worlds/kirbyam/data.py` — data loading and address mapping

## Setup

### Installation

Install Cosmic Ray and dependencies from the dedicated requirements file:

```bash
pip install -r mutation-testing-requirements.txt
```

Alternatively, install directly:

```bash
pip install cosmic-ray>=8.0
```

### Configuration

Mutation test configuration is defined in `worlds/kirbyam/test/mutation.cosmic.toml`:

```toml
[cosmic-ray]
module-path = ["worlds/kirbyam/ability_randomization.py", "worlds/kirbyam/data.py"]
timeout = 20.0
excluded-modules = ["**/test/**"]
test-command = "python -m pytest worlds/kirbyam/test/test_enemy_copy_ability_randomization.py worlds/kirbyam/test/test_fixture_data.py -q"

[cosmic-ray.distributor]
name = "local"
```

## Workflow

### Step 1: Baseline

Verify that target tests pass on unmutated code:

```bash
cosmic-ray baseline worlds/kirbyam/test/mutation.cosmic.toml
```

**Expected output:** `Baseline passed. Execution with no mutation works fine.`

### Step 2: Initialize Session

Generate all candidate mutations and create a session database:

```bash
cosmic-ray init --force worlds/kirbyam/test/mutation.cosmic.toml test-output/kirbyam/mutation.309.sqlite
```

View workload size:

```bash
cr-report test-output/kirbyam/mutation.309.sqlite --show-pending
```

### Step 3: Execute Mutations

Run all mutations and collect results (note: this is a long-running task):

```bash
cosmic-ray exec worlds/kirbyam/test/mutation.cosmic.toml test-output/kirbyam/mutation.309.sqlite
```

Typical runtime: ~30–60 minutes depending on system and mutation count.

### Step 4: Analyze Results

Generate a summary report:

```bash
cr-report test-output/kirbyam/mutation.309.sqlite
```

Key metrics:
- **Total jobs:** Number of mutations generated
- **Complete:** Completed mutations
- **Surviving mutants:** Mutations NOT killed by tests (potential test gaps)
- **Mutation score:** `(killed / total) * 100%`

### Step 5: Interpret & Act

**High score (>85%):**
- Test suite is comprehensive; low risk of assertion gaps.
- No action required unless specific surviving mutants need investigation.

**Medium score (70–85%):**
- Test suite covers most paths but may miss edge cases.
- Review surviving mutants for patterns (e.g., lack of boundary or error-path assertions).
- Add targeted assertions if applicable.

**Low score (<70%):**
- Test suite has significant gaps.
- Prioritize assertions for common mutant classes: comparisons, boolean operators, return values.

## Viewing Surviving Mutants

To see which mutations survived (i.e., tests did not catch them):

```bash
cr-report test-output/kirbyam/mutation.309.sqlite --surviving-only
```

Each survived mutant is an opportunity to strengthen assertions.

## Continuous Integration

Mutation testing is currently a local/manual workflow. To integrate into CI:

1. Create a dedicated `.github/workflows/kirbyam-mutation.yml` workflow.
2. Trigger on schedule (e.g., weekly) or manually via `workflow_dispatch`.
3. Run baseline + init + exec phases, then upload results as artifacts.

## References

- [Cosmic Ray Documentation](https://cosmic-ray.readthedocs.io/)
- KirbyAM test suite: `worlds/kirbyam/test/`
- Related issues: #309 (mutation testing evaluation)
