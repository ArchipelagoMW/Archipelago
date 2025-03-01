# BizHawk Client

`BizHawkClient` is an abstract base class for a client that can access the memory of a ROM running in BizHawk. It does
the legwork of connecting Python to a Lua connector script, letting you focus on the loop of checking locations and
making on-the-fly modifications based on updates from the server. It also provides the same experience to users across
multiple games that use it, and was built in response to a growing number of similar but separate bespoke game clients
which are/were largely exclusive to BizHawk anyway.

It's similar to `SNIClient`, but where `SNIClient` is designed to work for specifically SNES games across different
emulators/hardware, `BizHawkClient` is designed to work for specifically BizHawk across the different systems BizHawk
supports.

The idea is that `BizHawkClient` connects to and communicates with a Lua script running in BizHawk. It provides an API
that will call BizHawk functions for you to do things like read and write memory. And on an interval, control will be
handed to a function you write for your game (`game_watcher`) which should interact with the game's memory to check what
locations have been checked, give the player items, detect and send deathlinks, etc...

Table of Contents:
- [Connector Requests](#connector-requests)
    - [Requests that depend on other requests](#requests-that-depend-on-other-requests)
- [Implementing a Client](#implementing-a-client)
    - [Example](#example)
- [Tips](#tips)

## Connector Requests

Communication with BizHawk is done through `connector_bizhawk_generic.lua`. The client sends requests to the Lua script
via sockets; the Lua script processes the request and sends the corresponding responses.

The Lua script includes its own documentation, but you probably don't need to worry about the specifics. Instead, you'll
be using the functions in `worlds/_bizhawk/__init__.py`. If you do need more control over the specific requests being
sent or their order, you can still use `send_requests` to directly communicate with the connector script.

It's not necessary to use the UI or client context if you only want to interact with the connector script. You can
import and use just `worlds/_bizhawk/__init__.py`, which only depends on default modules.

Here's a list of the included classes and functions. I would highly recommend looking at the actual function signatures
and docstrings to learn more about each function.

```
class ConnectionStatus
class BizHawkContext

class NotConnectedError
class RequestFailedError
class ConnectorError
class SyncError

async def read(ctx, read_list) -> list[bytes]
async def write(ctx, write_list) -> None:
async def guarded_read(ctx, read_list, guard_list) -> (list[bytes] | None)
async def guarded_write(ctx, write_list, guard_list) -> bool

async def lock(ctx) -> None
async def unlock(ctx) -> None

async def get_hash(ctx) -> str
async def get_memory_size(ctx, domain: str) -> int
async def get_system(ctx) -> str
async def get_cores(ctx) -> dict[str, str]
async def ping(ctx) -> None

async def display_message(ctx, message: str) -> None
async def set_message_interval(ctx, value: float) -> None

async def connect(ctx) -> bool
def disconnect(ctx) -> None

async def get_script_version(ctx) -> int
async def send_requests(ctx, req_list) -> list[dict[str, Any]]
```

`send_requests` is what actually communicates with the connector, and any functions like `guarded_read` will build the
requests and then call `send_requests` for you. You can call `send_requests` yourself for more direct control, but make
sure to read the docs in `connector_bizhawk_generic.lua`.

A bundle of requests sent by `send_requests` will all be executed on the same frame, and by extension, so will any
helper that calls `send_requests`. For example, if you were to call `read` with 3 items on your `read_list`, all 3
addresses will be read on the same frame and then sent back.

It also means that, by default, the only way to run multiple requests on the same frame is for them to be included in
the same `send_requests` call. As soon as the connector finishes responding to a list of requests, it will advance the
frame before checking for the next batch.

### Requests that depend on other requests

The fact that you have to wait at least a frame to act on any response may raise concerns. For example, Pokemon
Emerald's save data is at a dynamic location in memory; it moves around when you load a new map. There is a static
variable that holds the address of the save data, so we want to read the static variable to get the save address, and
then use that address in a `write` to send the player an item. But between the `read` that tells us the address of the
save data and the `write` to save data itself, an arbitrary number of frames have been executed, and the player may have
loaded a new map, meaning we've written data to who knows where.

There are two solutions to this problem.

1. Use `guarded_write` instead of `write`. We can include a guard against the address changing, and the script will only
perform the write if the data in memory matches what's in the guard. In the below example, `write_result` will be `True`
if the guard validated and the data was written, and `False` if the guard failed to validate.

```py
# Get the address of the save data
read_result: bytes = (await _bizhawk.read(ctx, [(0x3001111, 4, "System Bus")]))[0]
save_data_address = int.from_bytes(read_result, "little")

# Write to `save_data_address` if it hasn't changed
write_result: bool = await _bizhawk.guarded_write(
    ctx,
    [(save_data_address, [0xAA, 0xBB], "System Bus")],
    [(0x3001111, read_result, "System Bus")]
)

if write_result:
    # The data at 0x3001111 was still the same value as
    # what was returned from the first `_bizhawk.read`,
    # so the data was written.
    ...
else:
    # The data at 0x3001111 has changed since the
    # first `_bizhawk.read`, so the data was not written.
    ...
```

2. Use `lock` and `unlock` (discouraged if not necessary). When you call `lock`, you tell the emulator to stop advancing
frames and just process requests until it receives an unlock request. This means you can lock, read the address, write
the data, and then unlock on a single frame. **However**, this is _slow_. If you can't get in and get out quickly
enough, players will notice a stutter in the emulation.

```py
# Pause emulation
await _bizhawk.lock(ctx)

# Get the address of the save data
read_result: bytes = (await _bizhawk.read(ctx, [(0x3001111, 4, "System Bus")]))[0]
save_data_address = int.from_bytes(read_result, "little")

# Write to `save_data_address`
await _bizhawk.write(ctx, [(save_data_address, [0xAA, 0xBB], "System Bus")])

# Resume emulation
await _bizhawk.unlock(ctx)
```

You should always use `guarded_read` and `guarded_write` instead of locking the emulator if possible. It may be
unreliable, but that's by design. Most of the time you should have no problem giving up and retrying. Data that is
volatile but only changes occasionally is the perfect use case.

If data is almost guaranteed to change between frames, locking may be the better solution. You can lower the time spent
locked by using `send_requests` directly to include as many requests alongside the `LOCK` and `UNLOCK` requests as
possible. But in general it's probably worth doing some extra asm hacking and designing to make guards work instead.

## Implementing a Client

`BizHawkClient` itself is built on `CommonClient` and inspired heavily by `SNIClient`. Your world's client should
inherit from `BizHawkClient` in `worlds/_bizhawk/client.py`. It must implement `validate_rom` and `game_watcher`, and
must define values for `system` and `game`.

As with the functions and classes in the previous section, I would highly recommend looking at the types and docstrings
of the code itself.

`game` should be the same value you use for your world definition.

`system` can either be a string or a tuple of strings. This is the system (or systems) that your client is intended to
handle games on (SNES, GBA, etc.). It's used to prevent validators from running on unknown systems and crashing. The
actual abbreviation corresponds to whatever BizHawk returns from `emu.getsystemid()`.

`patch_suffix` is an optional `ClassVar` meant to specify the file extensions you want to register. It can be a string
or tuple of strings. When a player clicks "Open Patch" in a launcher, the suffix(es) will be whitelisted in the file
select dialog and they will be associated with BizHawkClient. This does not affect whether the user's computer will
associate the file extension with Archipelago.

`validate_rom` is called to figure out whether a given ROM belongs to your client. It will only be called when a ROM is
running on a system you specified in your `system` class variable. Take extra care here, because your code will run
against ROMs that you have no control over. If you're reading an address deep in ROM, you might want to check the size
of ROM before you attempt to read it using `get_memory_size`. If you decide to claim this ROM as yours, this is where
you should do setup for things like `items_handling`.

`game_watcher` is the "main loop" of your client where you should be checking memory and sending new items to the ROM.
`BizHawkClient` will make sure that your `game_watcher` only runs when your client has validated the ROM, and will do
its best to make sure you're connected to the connector script before calling your watcher. It runs this loop either
immediately once it receives a message from the server, or a specified amount of time after the last iteration of the
loop finished.

`validate_rom`, `game_watcher`, and other methods will be passed an instance of `BizHawkClientContext`, which is a
subclass of `CommonContext`. It additionally includes `slot_data` (if you are connected and asked for slot data),
`bizhawk_ctx` (the instance of `BizHawkContext` that you should be giving to functions like `guarded_read`), and
`watcher_timeout` (the amount of time in seconds between iterations of the game watcher loop).

### Example

A very simple client might look like this. All addresses here are made up; you should instead be using addresses that
make sense for your specific ROM. The `validate_rom` here tries to read the name of the ROM. If it gets the value it
wanted, it sets a couple values on `ctx` and returns `True`. The `game_watcher` reads some data from memory and acts on
it by sending messages to AP. You should be smarter than this example, which will send `LocationChecks` messages even if
there's nothing new since the last loop.

```py
from typing import TYPE_CHECKING

from NetUtils import ClientStatus

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


class MyGameClient(BizHawkClient):
    game = "My Game"
    system = "GBA"
    patch_suffix = ".apextension"

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name = ((await bizhawk.read(ctx.bizhawk_ctx, [(0x100, 6, "ROM")]))[0]).decode("ascii")
            if rom_name != "MYGAME":
                return False  # Not a MYGAME ROM
        except bizhawk.RequestFailedError:
            return False  # Not able to get a response, say no for now

        # This is a MYGAME ROM
        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True

        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        try:
            # Read save data
            save_data = await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x3000100, 20, "System Bus")]
            )[0]

            # Check locations
            if save_data[2] & 0x04:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": [23]
                }])

            # Send game clear
            if not ctx.finished_game and (save_data[5] & 0x01):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
```

### Tips

- Make sure your client gets imported when your world is imported. You probably don't need to actually use anything in
your `client.py` elsewhere, but you still have to import the file for your client to register itself.
- When it comes to performance, there are two directions to optimize:
  1. If you need to execute multiple commands on the same frame, do as little work as possible. Only read and write necessary data,
  and if you have to use locks, unlock as soon as it's okay to advance frames. This is probably the obvious one.
  2. Multiple things that don't have to happen on the same frame should be split up if they're likely to be slow.
  Remember, the game watcher runs only a few times per second. Extra function calls on the client aren't that big of a
  deal; the player will not notice if your `game_watcher` is slow. But the emulator has to be done with any given set of
  commands in 1/60th of a second to avoid hiccups (faster still if your players use speedup). Too many reads of too much
  data at the same time is more likely to cause a bad user experience.
- Your `game_watcher` will be called regardless of the status of the client's connection to the server. Double-check the
server connection before trying to interact with it.
- By default, the player will be asked to provide their slot name after connecting to the server and validating, and
that input will be used to authenticate with the `Connect` command. You can override `set_auth` in your own client to
set it automatically based on data in the ROM or on your client instance.
- Use `get_memory_size` inside `validate_rom` if you need to read at large addresses, in case some other game has a
smaller ROM size.
- You can override `on_package` in your client to watch raw packages, but don't forget you also have access to a
subclass of `CommonContext` and its API.
- You can import `BizHawkClientContext` for type hints using `typing.TYPE_CHECKING`. Importing it without conditions at
the top of the file will probably cause a circular dependency.
- Your game's system may have multiple usable cores in BizHawk. You can use `get_cores` to try to determine which one is
currently loaded (it's the best we can do). Some cores may differ in the names of memory domains. It's good to check all
the available cores to find differences before your users do.
- The connector script includes a DEBUG variable that you can use to log requests/responses. (Be aware that as the log
grows in size in BizHawk, it begins to stutter while trying to print it.)
