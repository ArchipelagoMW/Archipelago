class Event:
    pass


class LocationalEvent(Event):
    x: int
    y: int


class ConfettiFired(LocationalEvent):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
