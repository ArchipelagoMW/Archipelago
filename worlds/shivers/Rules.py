import typing
from collections.abc import Callable
from BaseClasses import CollectionState

from worlds.AutoWorld import World


def get_rules_lookup(player: int):
    rules_lookup: typing.Dict[str, typing.List[Callable[[CollectionState], bool]]] = {
        "entrances": {
            "To Office Elevator": lambda state: state.has('Key for Office Elevator', player),
            "To Bedroom Elevator": lambda state: state.has("Key for Bedroom Elevator", player) and state.has("Crawling", player),
            "To Three Floor Elevator From Maintenance Tunnels": lambda state: state.has("Key for Three Floor Elevator", player),
            "To Three Floor Elevator From Blue Maze Bottom": lambda state: state.has("Key for Three Floor Elevator", player),
            "To Three Floor Elevator From Blue Maze Top": lambda state: state.has("Key for Three Floor Elevator", player),
            "To Workshop": lambda state: state.has("Key for Workshop", player),
            "To Lobby From Office": lambda state: state.has("Key for Lobby", player),
            "To Prehistoric": lambda state: state.has("Key for Prehistoric Room", player),
            "To Plants": lambda state: state.has("Key for Plants Room", player),
            "To Ocean": lambda state: state.has("Key for Ocean Room", player),
            "To Projector Room": lambda state: state.has("Key for Projector Room", player),
            "To Generator": lambda state: state.has("Key for Generator Room", player),
            "To Library": lambda state: state.has("Key for Library Room", player),
            "To Egypt": lambda state: state.has("Key for Egypt Room", player),
            "To Tiki": lambda state: state.has("Key for Tiki Room", player),
            "To UFO": lambda state: state.has("Key for UFO Room", player),
            "To Torture": lambda state: state.has("Key for Torture Room", player),
            "To Puzzle Room Mastermind": lambda state: state.has("Key for Puzzle Room", player),
            "To Bedroom": lambda state: state.has("Key for Bedroom Room", player),
            "To Underground Lake": lambda state: state.has("Key for Underground Lake Room", player),
            "To Maintenance Tunnels From Theater Back Hallways": lambda state: state.has("Crawling", player),
            "To Blue Maze": lambda state: state.has("Crawling", player),
            "To Lobby From Tar River": lambda state: (state.has("Crawling", player) and state.has("Oil Pot Bottom", player) and 
                                                      state.has("Oil Pot Top", player)),
            "To Anansi": lambda state: state.can_reach("Gods Room", "Region", player),
            "To Burial": lambda state: state.can_reach("Egypt", "Region", player),
            "To Slide Room": lambda state: (
                        state.can_reach("Prehistoric", "Region", player) and state.can_reach("Tar River", "Region",player) and 
                        state.can_reach("Egypt", "Region", player) and state.can_reach("Burial", "Region", player) and 
                        state.can_reach("Gods Room", "Region", player) and state.can_reach("Werewolf", "Region", player)),
            "To Lobby From Slide Room": lambda state: (
                        state.can_reach("Generator", "Region", player) and state.can_reach("Torture", "Region", player))
        },
        "locations": {
            "Puzzle Solved Anansi Musicbox": lambda state: state.can_reach("Clock Tower", "Region", player),
            "Puzzle Solved Geoffrey Door": lambda state: state.can_reach("Three Floor Elevator", "Region", player),
            "Puzzle Solved Clock Chains": lambda state: state.can_reach("Bedroom", "Region", player),
            "Puzzle Solved Tiki Drums": lambda state: state.can_reach("Clock Tower", "Region", player),
            "Puzzle Solved Red Door": lambda state: state.can_reach("Maintenance Tunnels", "Region", player),
            "Puzzle Solved UFO Symbols": lambda state: state.can_reach("Library", "Region", player),
            "Puzzle Solved Maze Door": lambda state: state.can_reach("Projector Room", "Region", player),
            "Accessible: Storage: Janitor Closet": lambda state: state.has("Cloth Pot Bottom", player) and state.has("Cloth Pot Top", player) and
                        state.has("Cloth Pot Bottom DUPE", player) and state.has("Cloth Pot Top DUPE", player),
            "Accessible: Storage: Tar River": lambda state: state.has("Oil Pot Bottom", player) and state.has("Oil Pot Top", player) and
                        state.has("Oil Pot Bottom DUPE", player) and state.has("Oil Pot Top DUPE", player),
            "Accessible: Storage: Slide": lambda state: state.has("Water Pot Bottom DUPE", player) and
                        state.has("Wax Pot Bottom DUPE", player) and
                        state.has("Ash Pot Bottom DUPE", player) and
                        state.has("Oil Pot Bottom DUPE", player) and
                        state.has("Cloth Pot Bottom DUPE", player) and
                        state.has("Wood Pot Bottom DUPE", player) and
                        state.has("Crystal Pot Bottom DUPE", player) and
                        state.has("Sand Pot Bottom DUPE", player) and
                        state.has("Metal Pot Bottom DUPE", player) and
                        state.has("Water Pot Top DUPE", player) and
                        state.has("Wax Pot Top DUPE", player) and
                        state.has("Ash Pot Top DUPE", player) and
                        state.has("Oil Pot Top DUPE", player) and
                        state.has("Cloth Pot Top DUPE", player) and
                        state.has("Wood Pot Top DUPE", player) and
                        state.has("Crystal Pot Top DUPE", player) and
                        state.has("Sand Pot Top DUPE", player) and
                        state.has("Metal Top DUPE", player)
            }
    }
    return rules_lookup


def set_rules(Shivers: World) -> None:
    multiworld = Shivers.multiworld
    player = Shivers.player

    rules_lookup = get_rules_lookup(player)

    # Set entrance rules
    for entrance_name, rule in rules_lookup["entrances"].items():
        multiworld.get_entrance(entrance_name, player).access_rule = rule

    # Set location rules
    for location_name, rule in rules_lookup["locations"].items():
        multiworld.get_location(location_name, player).access_rule = rule
