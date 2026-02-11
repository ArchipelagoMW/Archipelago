import typing
from BaseClasses import Entrance, Item, Location, Region
from . import constants

# Zoom in... Zoom zoom

class S1HubRegion(Region):
    game = "Sonic the Hedgehog 1"

class S1HubEntrance(Entrance):
    pass

class S1Region(Region):
    game = "Sonic the Hedgehog 1"
    monitors: typing.Dict
    checkpoints: typing.Dict

    gated = False
    zone = "Mystery"
    act = 1
    name = "Mystery 1"
    beaten = False
    has_boss = False
    has_emerald = False

    def __init__(self, zone: constants._zoneraw, act: int, player, multiworld):
        if len(zone.acts) > 1:
            name = f"{zone.long} {act}"
            self.zone = f"{zone.zone}{act}"
        else:
            name = zone.long
            self.zone = zone.zone
        super().__init__(name, player, multiworld)
        self.act = act
        self.monitors = {}
        self.checkpoints = {}


class S1Item(Item):
    game = "Sonic the Hedgehog 1"

class S1Location(Location):
    game: str = "Sonic the Hedgehog 1"
    checked = False

    def __init__(self, player, name, address, parent, zone):
        super().__init__(player, name, address, parent)
        self.zone = zone

class S1A1Entrance(Entrance):
    pass

class S1A2Entrance(Entrance):
    pass

class S1A3Entrance(Entrance):
    pass

class S1SSEntrance(Entrance):
    pass

class S1FinalEntrance(Entrance):
    pass

class S1Monitor(S1Location):
    broken = False
    raw: constants._monitor
    
    def __init__(self, player, monitor: constants._monitor, parent):
        super().__init__(player, monitor.name, monitor.id, parent, parent.name)
        self.broken = False
        self.raw = monitor

class S1Boss(S1Location):
    beaten = False
    raw: constants._boss
    
    def __init__(self, player, boss: constants._boss, parent):
        super().__init__(player, boss.name, boss.id, parent, parent.name)
        self.raw = boss

class S1Special(S1Location):
    beaten = False
    raw: constants._special
    
    def __init__(self, player, special: constants._special, parent):
        super().__init__(player, special.name, special.id, parent, parent.name)
        self.raw = special

class S1VictoryToken(S1Item):
    pass