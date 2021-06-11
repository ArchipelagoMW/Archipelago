from BaseClasses import MultiWorld

class AutoWorldRegister(type):
    world_types = {}

    def __new__(cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        if "game" in dct:
            AutoWorldRegister.world_types[dct["game"]] = new_class
        return new_class


def call_single(world: MultiWorld, method_name: str, player: int):
    method = getattr(world.worlds[player], method_name)
    return method(world, player)


def call_all(world: MultiWorld, method_name: str):
    for player in world.player_ids:
        call_single(world, method_name, player)


class World(metaclass=AutoWorldRegister):
    """A World object encompasses a game's Items, Locations, Rules and additional data or functionality required.
    A Game should have its own subclass of World in which it defines the required data structures."""

    def __init__(self, player: int):
        self.player = int

    def generate_basic(self, world: MultiWorld, player: int):
        pass

    def generate_output(self, world: MultiWorld, player: int):
        pass

    def create_regions(self, world: MultiWorld, player: int):
        pass
