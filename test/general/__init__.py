from argparse import Namespace
from typing import Any, List, Optional, Tuple, Type

from BaseClasses import CollectionState, Item, ItemClassification, Location, MultiWorld, Region
from worlds import network_data_package
from worlds.AutoWorld import World, WebWorld, call_all

gen_steps = (
    "generate_early",
    "create_regions",
    "create_items",
    "set_rules",
    "connect_entrances",
    "generate_basic",
    "pre_fill",
)


def setup_solo_multiworld(
        world_type: Type[World], steps: Tuple[str, ...] = gen_steps, seed: Optional[int] = None
) -> MultiWorld:
    """
    Creates a multiworld with a single player of `world_type`, sets default options, and calls provided gen steps.
    
    :param world_type: Type of the world to generate a multiworld for
    :param steps: The gen steps that should be called on the generated multiworld before returning. Default calls
    steps through pre_fill
    :param seed: The seed to be used when creating this multiworld
    :return: The generated multiworld
    """
    return setup_multiworld(world_type, steps, seed)


def setup_multiworld(worlds: list[type[World]] | type[World], steps: tuple[str, ...] = gen_steps,
                     seed: int | None = None, options: dict[str, Any] | list[dict[str, Any]] = None) -> MultiWorld:
    """
    Creates a multiworld with a player for each provided world type, allowing duplicates, setting default options, and
    calling the provided gen steps.
    
    :param worlds: Type/s of worlds to generate a multiworld for
    :param steps: Gen steps that should be called before returning. Default calls through pre_fill
    :param seed: The seed to be used when creating this multiworld
    :param options: Options to set on each world. If just one dict of options is passed, it will be used for all worlds.
    :return: The generated multiworld
    """
    if not isinstance(worlds, list):
        worlds = [worlds]

    if options is None:
        options = [{}] * len(worlds)
    elif not isinstance(options, list):
        options = [options] * len(worlds)

    players = len(worlds)
    multiworld = MultiWorld(players)
    multiworld.game = {player: world_type.game for player, world_type in enumerate(worlds, 1)}
    multiworld.player_name = {player: f"Tester{player}" for player in multiworld.player_ids}
    multiworld.set_seed(seed)
    args = Namespace()
    for player, (world_type, option_overrides) in enumerate(zip(worlds, options), 1):
        for key, option in world_type.options_dataclass.type_hints.items():
            updated_options = getattr(args, key, {})
            updated_options[player] = option.from_any(option_overrides.get(key, option.default))
            setattr(args, key, updated_options)
    multiworld.set_options(args)
    multiworld.state = CollectionState(multiworld)
    for step in steps:
        call_all(multiworld, step)
    return multiworld


class TestWebWorld(WebWorld):
    tutorials = []


class TestWorld(World):
    game = f"Test Game"
    item_name_to_id = {}
    location_name_to_id = {}
    hidden = True
    web = TestWebWorld()


# add our test world to the data package, so we can test it later
network_data_package["games"][TestWorld.game] = TestWorld.get_data_package_data()


def generate_test_multiworld(players: int = 1) -> MultiWorld:
    """
    Generates a multiworld using a special Test Case World class, and seed of 0.

    :param players: Number of players to generate the multiworld for
    :return: The generated test multiworld
    """
    multiworld = setup_multiworld([TestWorld] * players, seed=0)
    multiworld.regions += [Region("Menu", player_id + 1, multiworld) for player_id in range(players)]

    return multiworld


def generate_locations(count: int, player_id: int, region: Region, address: Optional[int] = None,
                       tag: str = "") -> List[Location]:
    """
    Generates the specified amount of locations for the player and adds them to the specified region.

    :param count: Number of locations to create
    :param player_id: ID of the player to create the locations for
    :param address: Address for the specified locations. They will all share the same address if multiple are created
    :param region: Parent region to add these locations to
    :param tag: Tag to add to the name of the generated locations
    :return: List containing the created locations
    """
    prefix = f"player{player_id}{tag}_location"

    locations = [Location(player_id, f"{prefix}{i}", address, region) for i in range(count)]
    region.locations += locations
    return locations


def generate_items(count: int, player_id: int, advancement: bool = False, code: int = None) -> List[Item]:
    """
    Generates the specified amount of items for the target player.

    :param count: The amount of items to create
    :param player_id: ID of the player to create the items for
    :param advancement: Whether the created items should be advancement
    :param code: The code the items should be created with
    :return: List containing the created items
    """
    item_type = "prog" if advancement else ""
    classification = ItemClassification.progression if advancement else ItemClassification.filler

    items = [Item(f"player{player_id}_{item_type}item{i}", classification, code, player_id) for i in range(count)]
    return items
