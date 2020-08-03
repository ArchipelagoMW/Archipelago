from datetime import datetime
from uuid import UUID, uuid4
from pony.orm import *

db = Database()


class Patch(db.Entity):
    id = PrimaryKey(int, auto=True)
    player = Required(int)
    data = Required(buffer, lazy=True)
    seed = Optional('Seed')


class Room(db.Entity):
    id = PrimaryKey(UUID, default=uuid4)
    last_activity = Required(datetime, default=lambda: datetime.utcnow(), index=True)
    creation_time = Required(datetime, default=lambda: datetime.utcnow())
    owner = Required(UUID, index=True)
    commands = Set('Command')
    seed = Required('Seed', index=True)
    multisave = Optional(Json, lazy=True)
    show_spoiler = Required(int, default=0)  # 0 -> never, 1 -> after completion, -> 2 always
    timeout = Required(int, default=lambda: 6 * 60 * 60)  # seconds since last activity to shutdown
    tracker = Optional(UUID, index=True)
    last_port = Optional(int, default=lambda: 0)


class Seed(db.Entity):
    id = PrimaryKey(UUID, default=uuid4)
    rooms = Set(Room)
    multidata = Optional(Json, lazy=True)
    owner = Required(UUID, index=True)
    creation_time = Required(datetime, default=lambda: datetime.utcnow())
    patches = Set(Patch)
    spoiler = Optional(LongStr, lazy=True)


class Command(db.Entity):
    id = PrimaryKey(int, auto=True)
    room = Required(Room)
    commandtext = Required(str)
