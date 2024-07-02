import re
from pathlib import Path
from typing import TYPE_CHECKING, Optional, cast

if TYPE_CHECKING:
    from flask import Flask
    from werkzeug.test import Client as FlaskClient

__all__ = [
    "get_app",
    "upload_multidata",
    "create_room",
    "start_room",
    "stop_room",
    "set_room_timeout",
    "get_multidata_for_room",
    "set_multidata_for_room",
    "stop_autohost",
]


def get_app(tempdir: str) -> "Flask":
    from WebHostLib import app as raw_app
    from WebHost import get_app
    raw_app.config["PONY"] = {
        "provider": "sqlite",
        "filename": str(Path(tempdir) / "host.db"),
        "create_db": True,
    }
    raw_app.config.update({
        "TESTING": True,
        "HOST_ADDRESS": "localhost",
        "HOSTERS": 1,
    })
    return get_app()


def upload_multidata(app_client: "FlaskClient", multidata: Path) -> str:
    response = app_client.post("/uploads", data={
        "file": multidata.open("rb"),
    })
    assert response.status_code < 400, f"Upload of {multidata} failed: status {response.status_code}"
    assert "Location" in response.headers, f"Upload of {multidata} failed: no redirect"
    location = response.headers["Location"]
    assert isinstance(location, str)
    assert location.startswith("/seed/"), f"Upload of {multidata} failed: unexpected redirect"
    return location[6:]


def create_room(app_client: "FlaskClient", seed: str, auto_start: bool = False) -> str:
    response = app_client.get(f"/new_room/{seed}")
    assert response.status_code < 400, f"Creating room for {seed} failed: status {response.status_code}"
    assert "Location" in response.headers, f"Creating room for {seed} failed: no redirect"
    location = response.headers["Location"]
    assert isinstance(location, str)
    assert location.startswith("/room/"), f"Creating room for {seed} failed: unexpected redirect"
    room_id = location[6:]

    if not auto_start:
        # by default, creating a room will auto-start it, so we update last activity here
        stop_room(app_client, room_id, simulate_idle=False)

    return room_id


def start_room(app_client: "FlaskClient", room_id: str, timeout: float = 30) -> str:
    from time import sleep

    import pony.orm

    poll_interval = .2

    print(f"Starting room {room_id}")
    no_timeout = timeout <= 0
    while no_timeout or timeout > 0:
        try:
            response = app_client.get(f"/room/{room_id}")
        except pony.orm.core.OptimisticCheckError:
            # hoster wrote to room during our transaction
            continue

        assert response.status_code == 200, f"Starting room for {room_id} failed: status {response.status_code}"
        match = re.search(r"/connect ([\w:.\-]+)", response.text)
        if match:
            return match[1]
        timeout -= poll_interval
        sleep(poll_interval)
    raise TimeoutError("Room did not start")


def stop_room(app_client: "FlaskClient",
              room_id: str,
              timeout: Optional[float] = None,
              simulate_idle: bool = True) -> None:
    from datetime import datetime, timedelta
    from time import sleep

    from pony.orm import db_session

    from WebHostLib.models import Command, Room
    from WebHostLib import app

    poll_interval = 2

    print(f"Stopping room {room_id}")
    room_uuid = app.url_map.converters["suuid"].to_python(None, room_id)  # type: ignore[arg-type]

    if timeout is not None:
        sleep(.1)  # should not be required, but other things might use threading

    with db_session:
        room: Room = Room.get(id=room_uuid)
        if simulate_idle:
            new_last_activity = datetime.utcnow() - timedelta(seconds=room.timeout + 5)
        else:
            new_last_activity = datetime.utcnow() - timedelta(days=3)
        room.last_activity = new_last_activity
        address = f"localhost:{room.last_port}" if room.last_port > 0 else None
        if address:
            original_timeout = room.timeout
            room.timeout = 1  # avoid spinning it up again
            Command(room=room, commandtext="/exit")

    try:
        if address and timeout is not None:
            print("waiting for shutdown")
            import socket
            host_str, port_str = tuple(address.split(":"))
            address_tuple = host_str, int(port_str)

            no_timeout = timeout <= 0
            while no_timeout or timeout > 0:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect(address_tuple)
                    s.close()
                except ConnectionRefusedError:
                    return
                sleep(poll_interval)
                timeout -= poll_interval

            raise TimeoutError("Room did not stop")
    finally:
        with db_session:
            room = Room.get(id=room_uuid)
            room.last_port = 0  # easier to detect when the host is up this way
            if address:
                room.timeout = original_timeout
                room.last_activity = new_last_activity
                print("timeout restored")


def set_room_timeout(room_id: str, timeout: float) -> None:
    from pony.orm import db_session

    from WebHostLib.models import Room
    from WebHostLib import app

    room_uuid = app.url_map.converters["suuid"].to_python(None, room_id)  # type: ignore[arg-type]
    with db_session:
        room: Room = Room.get(id=room_uuid)
        room.timeout = timeout


def get_multidata_for_room(webhost_client: "FlaskClient", room_id: str) -> bytes:
    from pony.orm import db_session

    from WebHostLib.models import Room
    from WebHostLib import app

    room_uuid = app.url_map.converters["suuid"].to_python(None, room_id)  # type: ignore[arg-type]
    with db_session:
        room: Room = Room.get(id=room_uuid)
        return cast(bytes, room.seed.multidata)


def set_multidata_for_room(webhost_client: "FlaskClient", room_id: str, data: bytes) -> None:
    from pony.orm import db_session

    from WebHostLib.models import Room
    from WebHostLib import app

    room_uuid = app.url_map.converters["suuid"].to_python(None, room_id)  # type: ignore[arg-type]
    with db_session:
        room: Room = Room.get(id=room_uuid)
        room.seed.multidata = data


def stop_autohost(graceful: bool = True) -> None:
    import os
    import signal

    import multiprocessing

    from WebHostLib.autolauncher import stop

    stop()
    proc: multiprocessing.process.BaseProcess
    for proc in filter(lambda child: child.name.startswith("MultiHoster"), multiprocessing.active_children()):
        if graceful and proc.pid:
            os.kill(proc.pid, getattr(signal, "CTRL_C_EVENT", signal.SIGINT))
        else:
            proc.kill()
        try:
            proc.join(30)
        except TimeoutError:
            proc.kill()
            proc.join()
