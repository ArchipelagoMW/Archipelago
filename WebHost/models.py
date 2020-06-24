from datetime import datetime
from uuid import UUID, uuid4
from pony.orm import *

db = Database()


class Patch(db.Entity):
    id = PrimaryKey(int, auto=True)
    data = Required(buffer)
    simple_seed = Required('Seed')


class Room(db.Entity):
    id = PrimaryKey(int, auto=True)
    last_activity = Required(datetime, default=lambda: datetime.utcnow(), index=True)
    owner = Required(UUID, index=True)
    commands = Set('Command')
    seed = Required('Seed', index=True)
    multisave = Optional(Json)
    timeout = Required(int, default=lambda: 6)
    allow_tracker = Required(bool, default=True)
    last_port = Optional(int, default=lambda: 0)


class Seed(db.Entity):
    id = PrimaryKey(int, auto=True)
    rooms = Set(Room)
    multidata = Optional(Json)
    creation_time = Required(datetime, default=lambda: datetime.utcnow())
    patches = Set(Patch)
    spoiler = Optional(str)


class Command(db.Entity):
    id = PrimaryKey(int, auto=True)
    room = Required(Room)
    commandtext = Required(str)
