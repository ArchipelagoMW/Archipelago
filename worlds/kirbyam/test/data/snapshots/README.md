# KirbyAM Snapshot Fixtures

This directory contains committed golden snapshots used by
[worlds/kirbyam/test/test_snapshot_outputs.py](../../test_snapshot_outputs.py).

## Update workflow

1. Run:
   - Linux / macOS:
     - `KIRBYAM_UPDATE_SNAPSHOTS=1 python -m pytest worlds/kirbyam/test/test_snapshot_outputs.py`
   - Windows PowerShell:
     - `$env:KIRBYAM_UPDATE_SNAPSHOTS = "1"`
     - `python -m pytest worlds/kirbyam/test/test_snapshot_outputs.py`
2. Review the diff in this directory.
3. Reset the environment variable and rerun tests normally to confirm they pass.
4. Commit both the code change and updated snapshot files together.

Do not update snapshots unless behavior changes are intentional.
