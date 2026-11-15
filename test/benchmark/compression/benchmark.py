#!/usr/bin/env python

# based on python-websockets compression benchmark (c) Aymeric Augustin and contributors
# https://github.com/python-websockets/websockets/blob/main/experiments/compression/benchmark.py

import collections
import time
import zlib
from typing import Iterable


REPEAT = 10

WB, ML = 12, 5  # defaults used as a reference
WBITS = range(9, 16)
MEMLEVELS = range(1, 10)


def benchmark(data: Iterable[bytes]) -> None:
    size: dict[int, dict[int, float]] = collections.defaultdict(dict)
    duration: dict[int, dict[int, float]] = collections.defaultdict(dict)

    for wbits in WBITS:
        for memLevel in MEMLEVELS:
            encoder = zlib.compressobj(wbits=-wbits, memLevel=memLevel)
            encoded = []

            print(f"Compressing {REPEAT} times with {wbits=} and {memLevel=}")

            t0 = time.perf_counter()

            for _ in range(REPEAT):
                for item in data:
                    # Taken from PerMessageDeflate.encode
                    item = encoder.compress(item) + encoder.flush(zlib.Z_SYNC_FLUSH)
                    if item.endswith(b"\x00\x00\xff\xff"):
                        item = item[:-4]
                    encoded.append(item)

            t1 = time.perf_counter()

            size[wbits][memLevel] = sum(len(item) for item in encoded) / REPEAT
            duration[wbits][memLevel] = (t1 - t0) / REPEAT

    raw_size = sum(len(item) for item in data)

    print("=" * 79)
    print("Compression ratio")
    print("=" * 79)
    print("\t".join(["wb \\ ml"] + [str(memLevel) for memLevel in MEMLEVELS]))
    for wbits in WBITS:
        print(
            "\t".join(
                [str(wbits)]
                + [
                    f"{100 * (1 - size[wbits][memLevel] / raw_size):.1f}%"
                    for memLevel in MEMLEVELS
                ]
            )
        )
    print("=" * 79)
    print()

    print("=" * 79)
    print("CPU time")
    print("=" * 79)
    print("\t".join(["wb \\ ml"] + [str(memLevel) for memLevel in MEMLEVELS]))
    for wbits in WBITS:
        print(
            "\t".join(
                [str(wbits)]
                + [
                    f"{1000 * duration[wbits][memLevel]:.1f}ms"
                    for memLevel in MEMLEVELS
                ]
            )
        )
    print("=" * 79)
    print()

    print("=" * 79)
    print(f"Size vs. {WB} \\ {ML}")
    print("=" * 79)
    print("\t".join(["wb \\ ml"] + [str(memLevel) for memLevel in MEMLEVELS]))
    for wbits in WBITS:
        print(
            "\t".join(
                [str(wbits)]
                + [
                    f"{100 * (size[wbits][memLevel] / size[WB][ML] - 1):.1f}%"
                    for memLevel in MEMLEVELS
                ]
            )
        )
    print("=" * 79)
    print()

    print("=" * 79)
    print(f"Time vs. {WB} \\ {ML}")
    print("=" * 79)
    print("\t".join(["wb \\ ml"] + [str(memLevel) for memLevel in MEMLEVELS]))
    for wbits in WBITS:
        print(
            "\t".join(
                [str(wbits)]
                + [
                    f"{100 * (duration[wbits][memLevel] / duration[WB][ML] - 1):.1f}%"
                    for memLevel in MEMLEVELS
                ]
            )
        )
    print("=" * 79)
    print()


def generate_data_package_corpus() -> list[bytes]:
    # compared to default 12, 5:
    # 11, 4 saves 16K RAM, gives  +4.6% size,  -5.0% time .. +1.1% time
    # 10, 4 saves 20K RAM, gives +10.2% size,  -3.8% time .. +0.6% time
    # 11, 3 saves 20K RAM, gives  +6.5% size, +14.2% time
    # 10, 3 saves 24K RAM, gives +12.8% size,  +0.5% time .. +6.9% time
    # NOTE: time delta is highly unstable; time is ~100ms
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        from NetUtils import encode
        from worlds import network_data_package

        return [encode(network_data_package).encode("utf-8")]


def generate_solo_release_corpus() -> list[bytes]:
    # compared to default 12, 5:
    # 11, 4 saves 16K RAM, gives  +0.9% size,  +3.9% time
    # 10, 4 saves 20K RAM, gives  +1.4% size,  +3.4% time
    # 11, 3 saves 20K RAM, gives  +1.8% size, +13.9% time
    # 10, 3 saves 24K RAM, gives  +2.1% size,  +4.8% time
    # NOTE: time delta is highly unstable; time is ~0.4ms

    from random import Random
    from MultiServer import json_format_send_event
    from NetUtils import encode, NetworkItem

    r = Random()
    r.seed(0)
    solo_release = []
    solo_release_locations = [r.randint(1000, 1999) for _ in range(200)]
    solo_release_items = sorted([r.randint(1000, 1999) for _ in range(200)])  # currently sorted by item
    solo_player = 1
    for location, item in zip(solo_release_locations, solo_release_items):
        flags = r.choice((0, 0, 0, 0, 0, 0, 0, 1, 2, 3))
        network_item = NetworkItem(item, location, solo_player, flags)
        solo_release.append(json_format_send_event(network_item, solo_player))
    solo_release.append({
        "cmd": "ReceivedItems",
        "index": 0,
        "items": solo_release_items,
    })
    solo_release.append({
        "cmd": "RoomUpdate",
        "hint_points": 200,
        "checked_locations": solo_release_locations,
    })
    return [encode(solo_release).encode("utf-8")]


def generate_gameplay_corpus() -> list[bytes]:
    # compared to default 12, 5:
    # 11, 4 saves 16K RAM, gives  +13.6% size,  +4.1% time
    # 10, 4 saves 20K RAM, gives  +22.3% size,  +2.2% time
    # 10, 3 saves 24K RAM, gives  +26.2% size,  +1.6% time
    # NOTE: time delta is highly unstable; time is 4ms

    from copy import copy
    from random import Random
    from MultiServer import json_format_send_event
    from NetUtils import encode, NetworkItem

    r = Random()
    r.seed(0)
    gameplay = []
    observer = 1
    hint_points = 0
    index = 0
    players = list(range(1, 10))
    player_locations = {player: [r.randint(1000, 1999) for _ in range(200)] for player in players}
    player_items = {player: [r.randint(1000, 1999) for _ in range(200)] for player in players}
    player_receiver = {player: [r.randint(1, len(players)) for _ in range(200)] for player in players}
    for i in range(0, len(player_locations[1])):
        player_sequence = copy(players)
        r.shuffle(player_sequence)
        for finder in player_sequence:
            flags = r.choice((0, 0, 0, 0, 0, 0, 0, 1, 2, 3))
            receiver = player_receiver[finder][i]
            item = player_items[finder][i]
            location = player_locations[finder][i]
            network_item = NetworkItem(item, location, receiver, flags)
            gameplay.append(json_format_send_event(network_item, observer))
            if finder == observer:
                hint_points += 1
                gameplay.append({
                    "cmd": "RoomUpdate",
                    "hint_points": hint_points,
                    "checked_locations": [location],
                })
            if receiver == observer:
                gameplay.append({
                    "cmd": "ReceivedItems",
                    "index": index,
                    "items": [item],
                })
                index += 1
    return [encode(gameplay).encode("utf-8")]


def main() -> None:
    #corpus = generate_data_package_corpus()
    #corpus = generate_solo_release_corpus()
    #corpus = generate_gameplay_corpus()
    corpus = generate_data_package_corpus() + generate_solo_release_corpus() + generate_gameplay_corpus()
    benchmark(corpus)
    print(f"raw size: {sum(len(data) for data in corpus)}")

if __name__ == "__main__":
    main()
