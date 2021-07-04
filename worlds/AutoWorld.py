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
    return method()


def call_all(world: MultiWorld, method_name: str):
    for player in world.player_ids:
        call_single(world, method_name, player)


class World(metaclass=AutoWorldRegister):
    """A World object encompasses a game's Items, Locations, Rules and additional data or functionality required.
    A Game should have its own subclass of World in which it defines the required data structures."""

    world: MultiWorld
    player: int
    options: dict = {}

    def __init__(self, world: MultiWorld, player: int):
        self.world = world
        self.player = player

    # overwritable methods that get called by Main.py
    def generate_basic(self):
        pass

    def set_rules(self):
        pass

    def create_regions(self):
        pass

    def generate_output(self):
        pass

    def collect(self, state, item) -> bool:
        """Collect an item into state"""
        if item.advancement:
            state.prog_items[item.name, item.player] += 1
            return True # indicate that a logical state change has occured
        return False

    def get_required_client_version(self) -> tuple:
        return 0, 0, 3