import typing
from collections.abc import Callable
from BaseClasses import CollectionState

from worlds.AutoWorld import World
from worlds.generic.Rules import forbid_item


def get_rules_lookup(player: int):
    rules_lookup: typing.Dict[str, typing.List[Callable[[CollectionState], bool]]] = {
        "entrances": {
            "To Office Elevator": lambda state: state.has("Key for Office Elevator", player),
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
            "Accessible: Storage: Janitor Closet": lambda state: state.has("Cloth Pot Bottom DUPE", player) and state.has("Cloth Pot Top DUPE", player),
            "Accessible: Storage: Tar River": lambda state: state.has("Oil Pot Bottom DUPE", player) and state.has("Oil Pot Top DUPE", player),
            "Accessible: Storage: Theater": lambda state: state.can_reach("Projector Room", "Region", player),
            "Ixupi Captured Water": lambda state: (state.can_reach("Lobby", "Region", player)) and 
                                                   state.has("Water Pot Bottom", player) and state.has("Water Pot Top", player) and
                                                   state.has("Water Pot Bottom DUPE", player) and state.has("Water Pot Top DUPE", player),
            "Ixupi Captured Wax": lambda state: ((state.can_reach("Library", "Region", player) or state.can_reach("Anansi", "Region", player)) and 
                                                   state.has("Wax Pot Bottom", player) and state.has("Wax Pot Top", player) and
                                                   state.has("Wax Pot Bottom DUPE", player) and state.has("Wax Pot Top DUPE", player)),
            "Ixupi Captured Ash": lambda state: ((state.can_reach("Office", "Region", player) or state.can_reach("Burial", "Region", player)) and 
                                                   state.has("Ash Pot Bottom", player) and state.has("Ash Pot Top", player) and
                                                   state.has("Ash Pot Bottom DUPE", player) and state.has("Ash Pot Top DUPE", player)),
            "Ixupi Captured Oil": lambda state: ((state.can_reach("Prehistoric", "Region", player) or state.can_reach("Tar River", "Region", player)) and 
                                                   state.has("Oil Pot Bottom", player) and state.has("Oil Pot Top", player) and
                                                   state.has("Oil Pot Bottom DUPE", player) and state.has("Oil Pot Top DUPE", player)),
            "Ixupi Captured Cloth": lambda state: ((state.can_reach("Egypt", "Region", player) or state.can_reach("Burial", "Region", player) 
                                                     or state.can_reach("Janitor Closet", "Region", player)) and 
                                                   state.has("Cloth Pot Bottom", player) and state.has("Cloth Pot Top", player) and
                                                   state.has("Cloth Pot Bottom DUPE", player) and state.has("Cloth Pot Top DUPE", player)),
            "Ixupi Captured Wood": lambda state: ((state.can_reach("Workshop", "Region", player) or state.can_reach("Blue Maze", "Region", player)
                                                    or state.can_reach("Gods Room", "Region", player) or state.can_reach("Anansi", "Region", player)) and 
                                                   state.has("Wood Pot Bottom", player) and state.has("Wood Pot Top", player) and
                                                   state.has("Wood Pot Bottom DUPE", player) and state.has("Wood Pot Top DUPE", player)),
            "Ixupi Captured Crystal": lambda state: ((state.can_reach("Lobby", "Region", player) or state.can_reach("Ocean", "Region", player)) and 
                                                   state.has("Crystal Pot Bottom", player) and state.has("Crystal Pot Top", player) and
                                                   state.has("Crystal Pot Bottom DUPE", player) and state.has("Crystal Pot Top DUPE", player)),
            "Ixupi Captured Sand": lambda state: ((state.can_reach("Plants", "Region", player) or state.can_reach("Ocean", "Region", player)) and 
                                                   state.has("Sand Pot Bottom", player) and state.has("Sand Pot Top", player) and
                                                   state.has("Sand Pot Bottom DUPE", player) and state.has("Sand Pot Top DUPE", player)),
            "Ixupi Captured Metal": lambda state: ((state.can_reach("Projector Room", "Region", player) or state.can_reach("Prehistoric", "Region", player)
                                                     or state.can_reach("Bedroom", "Region", player)) and 
                                                   state.has("Metal Pot Bottom", player) and state.has("Metal Pot Top", player) and
                                                   state.has("Metal Pot Bottom DUPE", player) and state.has("Metal Pot Top DUPE", player))
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

    #forbid cloth in janitor closet and oil in tar river
    forbid_item(multiworld.get_location("Accessible: Storage: Janitor Closet", player), "Cloth Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Janitor Closet", player), "Cloth Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Tar River", player), "Oil Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Tar River", player), "Oil Pot Top DUPE", player)

    #forbid all but lightning in slide
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Water Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Wax Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Ash Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Oil Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Cloth Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Wood Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Crystal Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Sand Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Metal Pot Bottom DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Water Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Wax Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Ash Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Oil Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Cloth Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Wood Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Crystal Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Sand Pot Top DUPE", player)
    forbid_item(multiworld.get_location("Accessible: Storage: Slide", player), "Metal Pot Top DUPE", player)

    #Filler Item Forbids
    forbid_item(multiworld.get_location("Puzzle Solved Lyre", player), "Easier Lyre", player)

    
