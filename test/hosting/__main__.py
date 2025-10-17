# A bunch of tests to verify MultiServer and custom webhost server work as expected.
# This spawns processes and may modify your local AP, so this is not run as part of unit testing.
# Run with `python test/hosting` instead,
import logging
import traceback
from tempfile import TemporaryDirectory
from time import sleep
from typing import Any

from test.hosting.client import Client
from test.hosting.generate import generate_local
from test.hosting.serve import ServeGame, LocalServeGame, WebHostServeGame
from test.hosting.webhost import (create_room, get_app, get_multidata_for_room, set_multidata_for_room, start_room,
                                  stop_autohost, upload_multidata)
from test.hosting.world import copy as copy_world, delete as delete_world

failure = False
fail_fast = True


def assert_true(condition: Any, msg: str = "") -> None:
    global failure
    if not condition:
        failure = True
        msg = f": {msg}" if msg else ""
        raise AssertionError(f"Assertion failed{msg}")


def assert_equal(first: Any, second: Any, msg: str = "") -> None:
    global failure
    if first != second:
        failure = True
        msg = f": {msg}" if msg else ""
        raise AssertionError(f"Assertion failed: {first} == {second}{msg}")


if fail_fast:
    expect_true = assert_true
    expect_equal = assert_equal
else:
    def expect_true(condition: Any, msg: str = "") -> None:
        global failure
        if not condition:
            failure = True
            tb = "".join(traceback.format_stack()[:-1])
            msg = f": {msg}" if msg else ""
            logging.error(f"Expectation failed{msg}\n{tb}")

    def expect_equal(first: Any, second: Any, msg: str = "") -> None:
        global failure
        if first != second:
            failure = True
            tb = "".join(traceback.format_stack()[:-1])
            msg = f": {msg}" if msg else ""
            logging.error(f"Expectation failed {first} == {second}{msg}\n{tb}")


if __name__ == "__main__":
    import warnings
    warnings.simplefilter("ignore", ResourceWarning)
    warnings.simplefilter("ignore", UserWarning)

    spacer = '=' * 80

    with TemporaryDirectory() as tempdir:
        multis = [["VVVVVV"], ["Temp World"], ["VVVVVV", "Temp World"]]
        p1_games = []
        data_paths = []
        rooms = []

        copy_world("VVVVVV", "Temp World")
        try:
            for n, games in enumerate(multis, 1):
                print(f"Generating [{n}] {', '.join(games)}")
                multidata = generate_local(games, tempdir)
                print(f"Generated [{n}] {', '.join(games)} as {multidata}\n")
                p1_games.append(games[0])
                data_paths.append(multidata)
        finally:
            delete_world("Temp World")

        webapp = get_app(tempdir)
        webhost_client = webapp.test_client()
        for n, multidata in enumerate(data_paths, 1):
            seed = upload_multidata(webhost_client, multidata)
            room = create_room(webhost_client, seed)
            print(f"Uploaded [{n}] {multidata} as {room}\n")
            rooms.append(room)

        print("Starting autohost")
        from WebHostLib.autolauncher import autohost
        try:
            autohost(webapp.config)

            host: ServeGame
            for n, (multidata, room, game, multi_games) in enumerate(zip(data_paths, rooms, p1_games, multis), 1):
                involved_games = {"Archipelago"} | set(multi_games)
                for collected_items in range(3):
                    print(f"\nTesting [{n}] {game} in {multidata} on MultiServer with {collected_items} items collected")
                    with LocalServeGame(multidata) as host:
                        with Client(host.address, game, "Player1") as client:
                            local_data_packages = client.games_packages
                            local_collected_items = len(client.checked_locations)
                            if collected_items < 2:  # Don't collect anything on the last iteration
                                client.collect_any()
                            # TODO: Ctrl+C test here as well

                    for game_name in sorted(involved_games):
                        expect_true(game_name in local_data_packages,
                                    f"{game_name} missing from MultiServer datap ackage")
                        expect_true("item_name_groups" not in local_data_packages.get(game_name, {}),
                                    f"item_name_groups are not supposed to be in MultiServer data for {game_name}")
                        expect_true("location_name_groups" not in local_data_packages.get(game_name, {}),
                                    f"location_name_groups are not supposed to be in MultiServer data for {game_name}")
                    for game_name in local_data_packages:
                        expect_true(game_name in involved_games,
                                    f"Received unexpected extra data package for {game_name} from MultiServer")
                    assert_equal(local_collected_items, collected_items,
                                 "MultiServer did not load or save correctly")

                    print(f"\nTesting [{n}] {game} in {multidata} on customserver with {collected_items} items collected")
                    prev_host_adr: str
                    with WebHostServeGame(webhost_client, room) as host:
                        prev_host_adr = host.address
                        with Client(host.address, game, "Player1") as client:
                            web_data_packages = client.games_packages
                            web_collected_items = len(client.checked_locations)
                            if collected_items < 2:  # Don't collect anything on the last iteration
                                client.collect_any()
                            if collected_items == 1:
                                sleep(1)  # wait for the server to collect the item
                                stop_autohost(True)  # simulate Ctrl+C
                                sleep(3)
                                autohost(webapp.config)  # this will spin the room right up again
                                sleep(1)  # make log less annoying
                                # if saving failed, the next iteration will fail below

                    # verify server shut down
                    try:
                        with Client(prev_host_adr, game, "Player1") as client:
                            assert_true(False, "Server did not shut down")
                    except ConnectionError:
                        pass

                    for game_name in sorted(involved_games):
                        expect_true(game_name in web_data_packages,
                                    f"{game_name} missing from customserver data package")
                        expect_true("item_name_groups" not in web_data_packages.get(game_name, {}),
                                    f"item_name_groups are not supposed to be in customserver data for {game_name}")
                        expect_true("location_name_groups" not in web_data_packages.get(game_name, {}),
                                    f"location_name_groups are not supposed to be in customserver data for {game_name}")
                    for game_name in web_data_packages:
                        expect_true(game_name in involved_games,
                                    f"Received unexpected extra data package for {game_name} from customserver")
                    assert_equal(web_collected_items, collected_items,
                                 "customserver did not load or save correctly during/after "
                                 + ("Ctrl+C" if collected_items == 2 else "/exit"))

                    # compare customserver to MultiServer
                    expect_equal(local_data_packages, web_data_packages,
                                 "customserver datapackage differs from MultiServer")

            sleep(5.5)  # make sure all tasks actually stopped

            # raise an exception in customserver and verify the save doesn't get destroyed
            # local variables room is the last room's id here
            old_data = get_multidata_for_room(webhost_client, room)
            print(f"Destroying multidata for {room}")
            set_multidata_for_room(webhost_client, room, bytes([0]))
            try:
                start_room(webhost_client, room, timeout=7)
            except TimeoutError:
                pass
            else:
                assert_true(False, "Room started with destroyed multidata")
            print(f"Restoring multidata for {room}")
            set_multidata_for_room(webhost_client, room, old_data)
            with WebHostServeGame(webhost_client, room) as host:
                with Client(host.address, game, "Player1") as client:
                    assert_equal(len(client.checked_locations), 2,
                                 "Save was destroyed during exception in customserver")
                    print("Save file is not busted 🥳")

        finally:
            print("Stopping autohost")
            stop_autohost(False)

    if failure:
        print("Some tests failed")
        exit(1)
    exit(0)
