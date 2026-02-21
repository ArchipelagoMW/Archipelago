"""
Benchmark: SetReply throughput with many clients on the same slot.

Scenario: 100 clients on the same slot, all subscribed to one key.
Run for 10 seconds.

Higher Set operations = server can handle more updates (good).
Lower socket writes for the same work = less I/O, less time on the wire (good).
"""
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from MultiServer import Context, Client, process_client_cmd

NUM_CLIENTS = 100
DURATION_SECONDS = 10.0
KEY = "bench_key"

def make_mock_socket():
    sock = MagicMock()
    sock.open = True
    sock.send = AsyncMock(return_value=None)
    return sock

def make_client(ctx: Context, team: int, slot: int, index: int):
    sock = make_mock_socket()
    client = Client(sock, ctx)
    client.auth = True
    client.team = team
    client.slot = slot
    ctx.player_names[team, slot] = f"Player_{slot}"
    return client

async def run_benchmark(ctx: Context, clients: list) -> tuple[int, int, float]:
    """Run Sets for DURATION_SECONDS; return (set_count, socket_writes, elapsed_seconds)."""
    socket_writes = [0]
    set_count = [0]
    real_broadcast = ctx.broadcast_send_encoded_msgs
    real_send_msgs = ctx.send_msgs

    async def counting_broadcast(endpoints, msg):
        endpoints_list = list(endpoints)
        socket_writes[0] += len(endpoints_list)
        return await real_broadcast(endpoints_list, msg)

    async def counting_send_msgs(endpoint, msgs):
        socket_writes[0] += 1
        return await real_send_msgs(endpoint, msgs)

    ctx.broadcast_send_encoded_msgs = counting_broadcast
    ctx.send_msgs = counting_send_msgs
    ctx.save = MagicMock()

    sender = clients[0]
    loop = asyncio.get_event_loop()
    t_end = loop.time() + DURATION_SECONDS
    t0 = loop.time()

    while loop.time() < t_end:
        await process_client_cmd(ctx, sender, {
            "cmd": "Set",
            "key": KEY,
            "operations": [{"operation": "replace", "value": set_count[0]}],
        })
        set_count[0] += 1
        await asyncio.sleep(0)

    # Let scheduled work finish (broadcasts on main, flush tasks on batching)
    await asyncio.sleep(0.15)

    t1 = loop.time()
    return set_count[0], socket_writes[0], t1 - t0


async def main():
    print(f"SetReply benchmark: {NUM_CLIENTS} clients, {DURATION_SECONDS}s run")
    print("=" * 60)

    with patch("MultiServer.Context._load_game_data"):
        ctx = Context("", 0, "", "", 0, 0, False)

    clients = [make_client(ctx, 0, 1, i) for i in range(NUM_CLIENTS)]
    ctx.clients[0] = {1: clients}
    for c in clients:
        ctx.stored_data_notification_clients[KEY].add(c)

    set_count, socket_writes, elapsed = await run_benchmark(ctx, clients)
    print(f"  Duration:        {elapsed:.3f}s")
    print(f"  Set operations:  {set_count:,}  (throughput: higher is better)")
    if elapsed > 0:
        print(f"  Sets/sec:        {set_count / elapsed:,.0f}")
    print(f"  Socket writes:   {socket_writes:,}  (I/O: lower is better)")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
