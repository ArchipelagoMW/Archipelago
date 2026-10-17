# Experimental Wii / Nintendont AP Bridge (v0.1)

Dolphin remains the default supported backend. This experimental backend connects the
existing TWW client to a Wii running Nintendont-AP with AP Bridge enabled. It uses the
same randomized game, save layout, item IDs, location checks, and AP server protocol.

Wii writes now require **Nintendont-AP v0.5 with WRTX support**. The hardware-tested
checkpoint of `ConCDeCurioso/Nintendont-AP`, branch `ap-bridge`, is
`3fca1d28c42f22d44b72104360ea9d350fe3f5d7` ("Add idempotent transaction writes to AP Bridge").
The earlier client authenticated its AP slot and delivered items on a real Wii. WRTX
deduplication has also been proven on hardware; this client integration needs a fresh hardware test.

## First hardware test

1. Keep a backup of your save for this first experimental test. Boot the AP-randomized
   Wind Waker ISO in Nintendont-AP on the Wii and load the matching save.
2. Confirm that the PC can reach the Wii's IPv4 address over UDP port **55000**.
3. Launch **this source checkout's** TWW client, using a Python 3.11.9–3.13 environment
   with the Archipelago/TWW dependencies installed. Python 3.14 is not supported by
   Archipelago 0.6.8. For example, in PowerShell with a prepared `.venv`:

   ```powershell
   Set-Location C:\Archipelago-Wii
   .\.venv\Scripts\python.exe Launcher.py "The Wind Waker Client" -- --nogui
   ```

   The environment prepared for the focused tests in this checkout contains the TWW
   client and test dependencies, but not the GUI or every other world's dependencies.
   To use that environment for this headless test without the repository's automatic
   requirements installer, first set:

   ```powershell
   $env:SKIP_REQUIREMENTS_UPDATE = "1"
   ```

   Other worlds may log missing-dependency errors during startup in this minimal
   environment; the TWW client should still start. A separately installed Archipelago
   executable will not include these local source changes.
4. In the **client**, enter:

   ```text
   /console 192.168.0.153
   ```

   Replace that example address with your Wii's address. Wait for
   `Wii AP Bridge connected successfully.`, then run:

   ```text
   /console
   /connect AP_SERVER_HOST:AP_SERVER_PORT
   ```

   Replace `AP_SERVER_HOST:AP_SERVER_PORT` with the actual room address. The slot name
   is read from the randomized game, as it is with Dolphin.
5. Verify a received item, a location check, a stage change, and (if enabled) DeathLink.
   Check that an item is delivered once. To exercise reconnection initially, interrupt
   the Wii connection while no items are pending, restore it, and inspect `/console`.
   If the AP server was disconnected, use `/connect AP_SERVER_HOST:AP_SERVER_PORT` again.

## Console commands

| Command | Effect |
| --- | --- |
| `/console` | Show the selected backend, endpoint, connection status, pending switch, and any item-delivery pause. |
| `/console <IPv4 address>` | Select Wii AP Bridge at that address, port 55000; wake the normal connector loop. |
| `/console off` | Switch back to Dolphin. |
| `/dolphin` | Show the original Dolphin status, or explain that Dolphin is inactive in Wii mode. |

Selection is local to the running client and is not saved between launches. Switching
closes the old backend and AP server session, clears console-specific session data, and
then probes the new backend. Connect to the AP room again after switching. No console
command is needed for ordinary Dolphin play.

## Transport and recovery

`Memory.py` defines the small `ConsoleMemory` interface, `DolphinMemory` adapter, and
`WiiMemory` UDP implementation. All gameplay memory operations use `ctx.memory`.
Dolphin's module is imported lazily and its native operations are delegated unchanged.

Wii uses one connected UDP socket with a **0.5-second timeout per request**, accepting
datagrams from the selected peer only. Each connection must pass both probes:

- Exactly `HELLO` → exactly `NIN-AP`.
- `READ 0x80000000, 6` → exactly `GZLE99`, inside a validated `DATA` response.

Every READ/WRTX payload is limited to **1–256 bytes**, entirely within
`0x80000000 <= address < 0x81800000`. There is no splitting or truncation. All integer
fields use big-endian encoding. Replies must have the expected magic, exact datagram
size, echoed address and length, and zero reserved bytes. READ keeps its 12-byte header
and `ERR!` format, with known error codes 1–4 and a zero final byte.
Malformed replies, bridge errors, and exhausted timeouts raise `APBridgeError` subclasses and
close the socket; no partial data is returned.

READ is idempotent and can safely retry after UDP reply loss: an initial attempt plus
up to two retries, with the same 0.5-second timeout for each attempt. Each retry discards
the old socket and resends the identical READ on a fresh connected socket with a different
source port, so delayed replies to timed-out attempts cannot contaminate the retry.
The successful replacement remains active for subsequent operations. This also applies
to the `GZLE99` probe READ. Malformed replies and `ERR!` responses are never retried.

Wii writes use **WRTX**, a 20-byte header followed by the payload. Each new logical write
generates a random, nonzero 64-bit transaction ID using `secrets.randbits(64)`, drawing
again if zero is returned. The client packs the request once. If waiting for its reply
times out, it retries the **identical request with the same transaction ID**, using a
fresh connected UDP socket and excluding previous timed-out source ports. There are at
most **three transmissions total**, each with a **0.5-second timeout**; a successful
replacement socket stays active. No HELLO or other writes occur between retries.

WRTX replies must be exactly 20 bytes and echo the address, payload length, and transaction
ID. `WROK` requires zero status and reserved bytes. `ERR!` requires a known error code
1–6 and a zero reserved byte; codes 5 and 6 mean invalid transaction ID and transaction
ID conflict. A fully validated `ERR!` raises `APBridgeRemoteError` without retrying.
Malformed replies, including wrong transaction IDs, are not retried and raise
`APBridgeWriteUncertainError`. Non-timeout transport errors and send timeouts also do
not retry. Exhausting all three reply timeouts disconnects and raises
`APBridgeWriteUncertainError`. **There is no fallback to legacy WRIT**, even with an older bridge.

Nintendont records each transaction before sending `WROK`. An exact duplicate returns
`WROK` without applying the memory write again, regardless of UDP source port. Reusing
an ID with different address/length/payload returns conflict error 6 without writing.
This provides **bounded recent at-most-once execution**, not global exactly-once delivery:
the bridge retains only 16 recent WRTX entries, and a kernel/Wii restart loses the cache.
Other writers can evict entries, so avoid concurrent bridge writers or Wii restarts
during retries. This client's synchronous writes cannot interleave within one retry
sequence. Transaction IDs are not persisted across client restarts.

HELLO uses the existing outer reconnect loop. The connector can establish a fresh
connection after a failure (normally after five seconds), but an uncertain item delivery
requires special handling: writing a queue entry and advancing the saved item index
are two separate writes. The game may consume an item even if its acknowledgment is lost.

If a queue write has an uncertain result, or the index update fails after a successful
queue write, **item delivery stays paused across reconnects and backend switches**. The
client logs this and `/console` reports it. Do not save that session; reload the last save,
then restart the client and select the Wii again. Restarting alone cannot undo an item
already delivered to the running game. Read failures and explicitly rejected queue writes
do not trigger this pause. Other synchronization can resume after reconnecting.

This v0.1 uses synchronous, serialized memory calls. Real Wii network latency may make
polling noticeably slower than Dolphin, and a failed request can briefly block the client
until its timeout (up to three timeouts for a READ or WRTX). READ still has no request IDs,
so matching delayed/duplicate replies for identical reads cannot always be distinguished.
No packet authentication, MEM2 access, IOS/ARM access, or item-get animations are added.

## Local validation

The tests use loopback UDP peers and a fake TWW memory image; they require no Wii or
running Dolphin. They also check native Dolphin delegation, console switching, reconnect,
slot authentication, gameplay paths, and the uncertain-item pause. The fake bridge models
a recent transaction cache and counts memory writes, verifying that lost WRTX replies
recover with one memory side effect and that exhausted acknowledgments still pause delivery.

From the repository root in PowerShell:

```powershell
$env:AP_TEST_WORLDS = "tww"
$env:SKIP_REQUIREMENTS_UPDATE = "1"
.\.venv\Scripts\python.exe -m pytest worlds/tww/test -q -p no:cacheprovider
.\.venv\Scripts\python.exe -m compileall -q worlds/tww/Memory.py worlds/tww/TWWClient.py worlds/tww/test
.\.venv\Scripts\python.exe -m ruff check worlds/tww/Memory.py worlds/tww/TWWClient.py worlds/tww/test --ignore N999,UP045,UP041
.\.venv\Scripts\python.exe -m mypy --follow-imports=silent --ignore-missing-imports worlds/tww/Memory.py worlds/tww/TWWClient.py
git diff --check
```

The lint exclusions retain TWW's existing module naming, `Optional` annotations, and
`asyncio.TimeoutError` spelling. The scoped type check skips unavailable external stubs.
