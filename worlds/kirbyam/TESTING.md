# KirbyAM Local Integration Testing

This guide provides a local Archipelago test-server setup for Kirby & The Amazing Mirror integration testing.

## What This Provides

- Local MultiServer bootstrap for KirbyAM test sessions
- Example KirbyAM player yaml for deterministic test generation
- Docker Compose wrapper for hosting a generated test archive

## Files

- `worlds/kirbyam/test/server/kirbyam_test_player.yaml`
- `worlds/kirbyam/test/server/start_test_server.py`
- `docker-compose.test.yml`

## Addressed Test Requirements

- Accept client connections: MultiServer exposed on `0.0.0.0:38281`
- Host test ROM/slot data: generated multiworld archive includes slot data
- Accept `LocationChecks`: standard AP server protocol via MultiServer
- Deliver test items: standard AP `ReceivedItems` flow via MultiServer

## Step 1: Generate Test Slot Data

1. Place or copy your test player yaml into `Players/`.
2. Recommended starter file:
   - `worlds/kirbyam/test/server/kirbyam_test_player.yaml`
3. Generate a test archive:

   - Windows PowerShell example:
     - `Copy-Item worlds/kirbyam/test/server/kirbyam_test_player.yaml Players/kirbyam_test.yaml`
     - `python Generate.py`

The generated multiworld archive is usually written under `output/` with `.zip` or `.archipelago` extension.

## Step 2A: Start Server Locally (Python)

Use the bootstrap script directly:

- `python worlds/kirbyam/test/server/start_test_server.py --archive output/<your-archive>.zip`

If `--archive` is omitted, the script automatically picks the newest `.zip` or `.archipelago` file under `output/`.

## Step 2B: Start Server via Docker Compose

1. Ensure your generated archive is available under `output/`.
2. Start compose:
   - `docker compose -f docker-compose.test.yml up --build`

Compose launches the bootstrap script, which automatically selects the newest `.zip` or `.archipelago` archive in `output/`.

## Step 3: Connect KirbyAM Client and Validate

1. Launch BizHawk and the KirbyAM client flow.
2. Connect to local AP server at `localhost:38281`.
3. Validate:
   - `LocationChecks` are accepted by server
   - test items are delivered to client
   - server-client logs can be correlated with `test-output/kirbyam/` logs

## ROM Patch Validation (Issue 121)

For the canonical USA KirbyAM base ROM used by this integration, `patch_rom.py` expects a 16 MB image (`0x1000000` bytes).

Expected behavior:

- No ROM-size warning for the configured USA baseline ROM whose MD5 matches `KirbyAmProcedurePatch.hash`
- A warning only when the selected ROM size differs from that baseline expectation

## Shutdown

- Local script: stop with `Ctrl+C`
- Compose: `docker compose -f docker-compose.test.yml down`

## Type Checking (Issue 145)

Run focused mypy validation for the KirbyAM client typing surface:

- `python -m mypy worlds/kirbyam/client.py --follow-imports=skip --ignore-missing-imports`

The client's expected BizHawk context shape is documented in `worlds/kirbyam/types.py` as `KirbyAmBizHawkClientContext`.

## Pytest Configuration Verification (Issue 144)

Run KirbyAM world tests directly:

- `python -m pytest worlds/kirbyam/test/`

Required dependencies for this command:

- `pytest` and `pytest-asyncio` (both listed in `requirements.txt`)

Expected behavior:

- KirbyAM tests are discovered under `worlds/kirbyam/test/`
- Async tests run with `asyncio_mode = auto`
- Failure summaries include extra context (`-ra`) for actionable triage

## Protocol Fuzzing (Issue 150)

Run targeted protocol-fuzzing coverage for malformed `ReceivedItems` payloads and unexpected command sequences:

- `python -m pytest worlds/kirbyam/test/test_fuzzer.py worlds/kirbyam/test/test_client.py`

The fuzz suite is implemented in `worlds/kirbyam/test/fuzzer.py` and reports scenario coverage as:

- `passed_cases / total_cases`
- `coverage_percent`

The suite includes malformed and out-of-range item payload cases and verifies graceful handling (warnings + skip) without client crashes.

## Notes

- This setup is intentionally minimal for integration testing and is not a production deployment path.
- For broader deployment containers, refer to `deploy/docker-compose.yml`.

## APWorld CI and Release Workflow (Issue 123)

The repository includes a dedicated GitHub Actions workflow at `.github/workflows/kirbyam-apworld.yml`.

Behavior:

- On pull requests touching `worlds/kirbyam/**`, and on pushes to `main`, it builds `kirbyam.apworld` and uploads it as a workflow artifact.
- On valid tags matching `kirbyam-vMAJOR.MINOR.PATCH`, it also creates or updates a draft GitHub release with the built `.apworld` asset attached.
- The release workflow never publishes releases for branch pushes or pull requests.
- If a tag begins with `kirbyam-v` but does not match the required three-part version format, the metadata step fails fast instead of publishing a malformed release.
- Re-running the same release workflow updates the existing draft release asset for that tag instead of creating a second release.

Tag format for release builds:

- Valid: `kirbyam-v0.0.1`
- Valid: `kirbyam-v1.2.3`
- Invalid: `kirbyam-0.0.1`
- Invalid: `v0.0.1`
- Invalid: `kirbyam-v0.0`
- Invalid: `kirbyam-v0.0.1-beta`

Maintainer release steps:

1. Merge the intended release changes into `main`.
2. Create an annotated tag such as `kirbyam-v0.0.1` on the release commit.
3. Push the tag to `origin`.
4. Wait for `.github/workflows/kirbyam-apworld.yml` to finish.
5. Open the draft GitHub release and verify:
   - release title is `KirbyAM APWorld v0.0.1`
   - attached asset name is `kirbyam.apworld`
   - the asset downloads and loads as an APWorld
6. Publish the draft release manually when ready.

Release validation checklist:

- Confirm release tag uses canonical format `kirbyam-vMAJOR.MINOR.PATCH`; the workflow injects this semver into `worlds/kirbyam/archipelago.json` during tagged release builds.
- Run `python -m pytest worlds/kirbyam/test/test_release_metadata.py` locally.
- Run `python build.py --skip-patch` from `worlds/kirbyam/` and confirm `kirbyam.apworld` is produced.
- Push a valid `kirbyam-vMAJOR.MINOR.PATCH` tag and confirm a draft release is created or updated.
- Confirm a non-tag branch push only uploads artifacts and does not create a release.
