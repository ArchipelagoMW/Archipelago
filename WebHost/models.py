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
    last_activity = Required(datetime, default=lambda: datetime.utcnow())
    owner = Required(UUID)
    commands = Set('Command')
    host_jobs = Set('HostJob')
    seed = Required('Seed')
    multisave = Optional(Json)


class HostJob(db.Entity):
    id = PrimaryKey(int, auto=True)
    sockets = Set('Socket')
    room = Required(Room)
    scheduler_id = Required(int, unique=True)


class Socket(db.Entity):
    port = PrimaryKey(int)
    ipv6 = Required(bool)
    host_job = Required(HostJob)


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
