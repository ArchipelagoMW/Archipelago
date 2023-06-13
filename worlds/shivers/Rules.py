import typing
from collections.abc import Callable
from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import forbid_item

def water_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Lobby", "Region", player) or
            (state.can_reach("Janitor Closet", "Region", player) and cloth_capturable(state, player))) \
        and state.has("Water Pot Bottom", player) \
        and state.has("Water Pot Top", player) \
        and state.has("Water Pot Bottom DUPE", player) \
        and state.has("Water Pot Top DUPE", player)

def wax_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Library", "Region", player) or state.can_reach("Anansi", "Region", player)) \
        and state.has("Wax Pot Bottom", player) \
        and state.has("Wax Pot Top", player) \
        and state.has("Wax Pot Bottom DUPE", player) \
        and state.has("Wax Pot Top DUPE", player)

def ash_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Office", "Region", player) or state.can_reach("Burial", "Region", player)) \
        and state.has("Ash Pot Bottom", player) \
        and state.has("Ash Pot Top", player) \
        and state.has("Ash Pot Bottom DUPE", player) \
        and state.has("Ash Pot Top DUPE", player)

def oil_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Prehistoric", "Region", player) or state.can_reach("Tar River", "Region", player)) \
        and state.has("Oil Pot Bottom", player) \
        and state.has("Oil Pot Top", player) \
        and state.has("Oil Pot Bottom DUPE", player) \
        and state.has("Oil Pot Top DUPE", player)

def cloth_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Egypt", "Region", player) or state.can_reach("Burial", "Region", player) or state.can_reach("Janitor Closet", "Region", player)) \
        and state.has("Cloth Pot Bottom", player) \
        and state.has("Cloth Pot Top", player) \
        and state.has("Cloth Pot Bottom DUPE", player) \
        and state.has("Cloth Pot Top DUPE", player)

def wood_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Workshop", "Region", player) or state.can_reach("Blue Maze", "Region", player) or state.can_reach("Gods Room", "Region", player) or state.can_reach("Anansi", "Region", player)) \
        and state.has("Wood Pot Bottom", player) \
        and state.has("Wood Pot Top", player) \
        and state.has("Wood Pot Bottom DUPE", player) \
        and state.has("Wood Pot Top DUPE", player)

def crystal_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Lobby", "Region", player) or state.can_reach("Ocean", "Region", player)) \
        and state.has("Crystal Pot Bottom", player) \
        and state.has("Crystal Pot Top", player) \
        and state.has("Crystal Pot Bottom DUPE", player) \
        and state.has("Crystal Pot Top DUPE", player)

def sand_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Greenhouse", "Region", player) or state.can_reach("Ocean", "Region", player)) \
        and state.has("Sand Pot Bottom", player) \
        and state.has("Sand Pot Top", player) \
        and state.has("Sand Pot Bottom DUPE", player) \
        and state.has("Sand Pot Top DUPE", player)

def metal_capturable(state: CollectionState, player: int) -> bool:
    return (state.can_reach("Projector Room", "Region", player) or state.can_reach("Prehistoric", "Region", player) or state.can_reach("Bedroom", "Region", player)) \
        and state.has("Metal Pot Bottom", player) \
        and state.has("Metal Pot Top", player) \
        and state.has("Metal Pot Bottom DUPE", player) \
        and state.has("Metal Pot Top DUPE", player)

def lightning_capturable(state: CollectionState, player: int) -> bool:
    return beths_body_available(state, player) \
        and state.can_reach("Torture", "Region", player) \
        and state.has("Lightning Pot Bottom", player) \
        and state.has("Lightning Pot Top", player) \
        and state.has("Lightning Pot Bottom DUPE", player) \
        and state.has("Lightning Pot Top DUPE", player)

def beths_body_available(state: CollectionState, player: int) -> bool:
    return water_capturable(state, player) and wax_capturable(state, player) \
        and ash_capturable(state, player) and oil_capturable(state, player) \
        and cloth_capturable(state, player) and wood_capturable(state, player) \
        and crystal_capturable(state, player) and sand_capturable(state, player) \
        and metal_capturable(state, player)

 

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
            "To Clock Tower Staircase": lambda state: state.can_reach("Three Floor Elevator", "Region", player),
            "To Prehistoric From Lobby": lambda state: state.has("Key for Prehistoric Room", player),
            "To Greenhouse": lambda state: state.has("Key for Greenhouse Room", player),
            "To Ocean": lambda state: state.has("Key for Ocean Room", player),
            "To Projector Room": lambda state: state.has("Key for Projector Room", player),
            "To Generator": lambda state: state.has("Key for Generator Room", player),
            "To Library From Lobby": lambda state: state.has("Key for Library Room", player),
            "To Lobby From Library": lambda state: state.has("Key for Library Room", player),
            "To Egypt From Lobby": lambda state: state.has("Key for Egypt Room", player),
            "To Egypt From Burial": lambda state: state.can_reach("Egypt", "Region", player),
            "To Egypt": lambda state: state.has("Key for Egypt Room", player),
            "To Tiki": lambda state: state.has("Key for Tiki Room", player),
            "To Gods Room": lambda state: state.can_reach("Clock Tower", "Region", player),
            "To Gods Room From Anansi": lambda state: state.can_reach("Gods Room", "Region", player),
            "To UFO": lambda state: state.has("Key for UFO Room", player),
            "To UFO From Inventions": lambda state: state.has("Key for UFO Room", player),
            "To Torture": lambda state: state.has("Key for Torture Room", player),
            "To Puzzle Room Mastermind": lambda state: state.has("Key for Puzzle Room", player),
            "To Bedroom": lambda state: state.has("Key for Bedroom", player),
            "To Underground Lake": lambda state: state.has("Key for Underground Lake Room", player),
            "To Maintenance Tunnels From Theater Back Hallways": lambda state: state.has("Crawling", player),
            "To Blue Maze": lambda state: state.has("Crawling", player),
            "To Egypt From Blue Maze": lambda state: state.has("Crawling", player),
            "To Lobby From Tar River": lambda state: (state.has("Crawling", player) and oil_capturable(state, player)),
            "To Anansi": lambda state: state.can_reach("Gods Room", "Region", player),
            "To Burial": lambda state: state.can_reach("Egypt", "Region", player),
            "To Slide Room": lambda state: (
                        state.can_reach("Prehistoric", "Region", player) and state.can_reach("Tar River", "Region",player) and 
                        state.can_reach("Egypt", "Region", player) and state.can_reach("Burial", "Region", player) and 
                        state.can_reach("Gods Room", "Region", player) and state.can_reach("Werewolf", "Region", player)),
            "To Lobby From Slide Room": lambda state: (
                        state.can_reach("Generator", "Region", player) and state.can_reach("Torture", "Region", player)),
            "To Janitor Closet": lambda state: state.has("Key for Janitor Closet", player)
        },
        "locations": {
            "Puzzle Solved Anansi Musicbox": lambda state: state.can_reach("Clock Tower", "Region", player),
            "Puzzle Solved Clock Tower Door": lambda state: state.can_reach("Three Floor Elevator", "Region", player),
            "Puzzle Solved Atlantis": lambda state: state.can_reach("Office", "Region", player),
            "Puzzle Solved Clock Chains": lambda state: state.can_reach("Bedroom", "Region", player),
            "Puzzle Solved Tiki Drums": lambda state: state.can_reach("Clock Tower", "Region", player),
            "Puzzle Solved Red Door": lambda state: state.can_reach("Maintenance Tunnels", "Region", player),
            "Puzzle Solved UFO Symbols": lambda state: state.can_reach("Library", "Region", player),
            "Puzzle Solved Maze Door": lambda state: state.can_reach("Projector Room", "Region", player),
            "Puzzle Solved Columns of RA": lambda state: state.can_reach("Underground Lake", "Region", player),
            "Accessible: Storage: Janitor Closet": lambda state: cloth_capturable(state, player),
            "Accessible: Storage: Ocean": lambda state: state.can_reach("Office", "Region", player),
            "Accessible: Storage: Tar River": lambda state: oil_capturable(state, player),
            "Accessible: Storage: Theater": lambda state: state.can_reach("Projector Room", "Region", player),
            "Ixupi Captured Water": lambda state: water_capturable(state, player),
            "Ixupi Captured Wax": lambda state: wax_capturable(state, player),
            "Ixupi Captured Ash": lambda state: ash_capturable(state, player),
            "Ixupi Captured Oil": lambda state: oil_capturable(state, player),
            "Ixupi Captured Cloth": lambda state: cloth_capturable(state, player),
            "Ixupi Captured Wood": lambda state: wood_capturable(state, player),
            "Ixupi Captured Crystal": lambda state: crystal_capturable(state, player),
            "Ixupi Captured Sand": lambda state: sand_capturable(state, player),
            "Ixupi Captured Metal": lambda state: metal_capturable(state, player),
            "Final Riddle: Planets Aligned": lambda state: state.can_reach("Fortune Teller", "Region", player),
            "Final Riddle: Norse God Stone Message": lambda state: (state.can_reach("Fortune Teller", "Region", player) and state.can_reach("UFO", "Region", player)),
            "Final Riddle: Beth's Body Page 17": lambda state: beths_body_available(state, player),
            "Final Riddle: Guillotine Dropped": lambda state: beths_body_available(state, player) and state.can_reach("Torture", "Region", player),
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
    forbid_item(multiworld.get_location("Ixupi Captured Water", player), "Water Always Available in Lobby", player)
    forbid_item(multiworld.get_location("Ixupi Captured Wax", player), "Wax Always Available in Library", player)
    forbid_item(multiworld.get_location("Ixupi Captured Wax", player), "Wax Always Available in Anansi Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Wax", player), "Wax Always Available in Tiki Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Ash", player), "Ash Always Availalbe in Office", player)
    forbid_item(multiworld.get_location("Ixupi Captured Ash", player), "Ash Always Available in Burial Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Oil", player), "Oil Always Available in Prehistoric Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Cloth", player), "Cloth Always Available in Egypt", player)
    forbid_item(multiworld.get_location("Ixupi Captured Cloth", player), "Cloth Always Available in Burial Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Wood", player), "Wood Always Available in Workshop", player)
    forbid_item(multiworld.get_location("Ixupi Captured Wood", player), "Wood Always Available in Blue Maze", player)
    forbid_item(multiworld.get_location("Ixupi Captured Wood", player), "Wood Always Available in Pegasus Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Wood", player), "Wood Always Available in Gods Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Crystal", player), "Crystal Always Available in Lobby", player)
    forbid_item(multiworld.get_location("Ixupi Captured Crystal", player), "Crystal Always Available in Ocean", player)
    forbid_item(multiworld.get_location("Ixupi Captured Sand", player), "Sand Always Available in Plants Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Sand", player), "Sand Always Available in Ocean", player)
    forbid_item(multiworld.get_location("Ixupi Captured Metal", player), "Metal Always Available in Projector Room", player)
    forbid_item(multiworld.get_location("Ixupi Captured Metal", player), "Metal Always Available in Bedroom", player)
    forbid_item(multiworld.get_location("Ixupi Captured Metal", player), "Metal Always Available in Prehistoric", player)

    
