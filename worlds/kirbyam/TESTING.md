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

## Shutdown

- Local script: stop with `Ctrl+C`
- Compose: `docker compose -f docker-compose.test.yml down`

## Notes

- This setup is intentionally minimal for integration testing and is not a production deployment path.
- For broader deployment containers, refer to `deploy/docker-compose.yml`.
