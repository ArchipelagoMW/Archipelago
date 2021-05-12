class AutoWorldRegister(type):
    _world_types = {}

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        AutoWorldRegister._world_types[name] = new_class
        return new_class

class World(metaclass=AutoWorldRegister):
    """A World object encompasses a game's Items, Locations, Rules and additional data or functionality required.
    A Game should have its own subclass of World in which it defines the required data structures."""
    def __init__(self):
        pass