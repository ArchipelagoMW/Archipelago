from collections.abc import Callable
from typing import Dict, TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import forbid_item
from . import Constants

if TYPE_CHECKING:
    from . import ShiversWorld


def water_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Water Pot Bottom", "Water Pot Top", "Water Pot Bottom DUPE", "Water Pot Top DUPE"}, player) \
        or state.has_all({"Water Pot Complete", "Water Pot Complete DUPE"}, player)


def wax_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Wax Pot Bottom", "Wax Pot Top", "Wax Pot Bottom DUPE", "Wax Pot Top DUPE"}, player) \
        or state.has_all({"Wax Pot Complete", "Wax Pot Complete DUPE"}, player)


def ash_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Ash Pot Bottom", "Ash Pot Top", "Ash Pot Bottom DUPE", "Ash Pot Top DUPE"}, player) \
        or state.has_all({"Ash Pot Complete", "Ash Pot Complete DUPE"}, player)


def oil_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Oil Pot Bottom", "Oil Pot Top", "Oil Pot Bottom DUPE", "Oil Pot Top DUPE"}, player) \
        or state.has_all({"Oil Pot Complete", "Oil Pot Complete DUPE"}, player)


def cloth_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Cloth Pot Bottom", "Cloth Pot Top", "Cloth Pot Bottom DUPE", "Cloth Pot Top DUPE"}, player) \
        or state.has_all({"Cloth Pot Complete", "Cloth Pot Complete DUPE"}, player)


def wood_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Wood Pot Bottom", "Wood Pot Top", "Wood Pot Bottom DUPE", "Wood Pot Top DUPE"}, player) \
        or state.has_all({"Wood Pot Complete", "Wood Pot Complete DUPE"}, player)


def crystal_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all(
        {"Crystal Pot Bottom", "Crystal Pot Top", "Crystal Pot Bottom DUPE", "Crystal Pot Top DUPE"}, player) \
        or state.has_all({"Crystal Pot Complete", "Crystal Pot Complete DUPE"}, player)


def sand_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Sand Pot Bottom", "Sand Pot Top", "Sand Pot Bottom DUPE", "Sand Pot Top DUPE"}, player) \
        or state.has_all({"Sand Pot Complete", "Sand Pot Complete DUPE"}, player)


def metal_capturable(state: CollectionState, player: int) -> bool:
    return state.has_all({"Metal Pot Bottom", "Metal Pot Top", "Metal Pot Bottom DUPE", "Metal Pot Top DUPE"}, player) \
        or state.has_all({"Metal Pot Complete", "Metal Pot Complete DUPE"}, player)


def lightning_capturable(state: CollectionState, world: "ShiversWorld", player: int) -> bool:
    return (first_nine_ixupi_capturable(state, player) or world.options.early_lightning) \
        and (state.has_all(
            {"Lightning Pot Bottom", "Lightning Pot Top", "Lightning Pot Bottom DUPE", "Lightning Pot Top DUPE"},
            player) or state.has_all({"Lightning Pot Complete", "Lightning Pot Complete DUPE"}, player))


def beths_body_available(state: CollectionState, world: "ShiversWorld", player: int) -> bool:
    return first_nine_ixupi_capturable(state, player) or world.options.early_beth


def first_nine_ixupi_capturable(state: CollectionState, player: int) -> bool:
    return water_capturable(state, player) and wax_capturable(state, player) \
        and ash_capturable(state, player) and oil_capturable(state, player) \
        and cloth_capturable(state, player) and wood_capturable(state, player) \
        and crystal_capturable(state, player) and sand_capturable(state, player) \
        and metal_capturable(state, player)


def all_skull_dials_set(state: CollectionState, player: int) -> bool:
    return state.has_all([
        "Set Skull Dial: Prehistoric",
        "Set Skull Dial: Tar River",
        "Set Skull Dial: Egypt",
        "Set Skull Dial: Burial",
        "Set Skull Dial: Gods Room",
        "Set Skull Dial: Werewolf"
    ], player)


def completion_condition(state: CollectionState, player: int) -> bool:
    return state.has(f"Mt. Pleasant Tribune: {Constants.years_since_sep_30_1980} year Old Mystery Solved!", player)


def get_rules_lookup(world: "ShiversWorld", player: int):
    rules_lookup: Dict[str, Dict[str, Callable[[CollectionState], bool]]] = {
        "entrances": {
            "To Office Elevator From Underground Blue Tunnels": lambda state: state.has("Key for Office Elevator", player),
            "To Office Elevator From Office": lambda state: state.has("Key for Office Elevator", player),
            "To Bedroom Elevator From Office": lambda state: state.has_all({"Key for Bedroom Elevator", "Crawling"}, player),
            "To Office From Bedroom Elevator": lambda state: state.has_all({"Key for Bedroom Elevator", "Crawling"}, player),
            "To Three Floor Elevator From Maintenance Tunnels": lambda state: state.has("Key for Three Floor Elevator", player),
            "To Three Floor Elevator From Blue Maze Bottom": lambda state: state.has("Key for Three Floor Elevator", player),
            "To Three Floor Elevator From Blue Maze Top": lambda state: state.has("Key for Three Floor Elevator", player),
            "To Workshop": lambda state: state.has("Key for Workshop", player),
            "To Lobby From Office": lambda state: state.has("Key for Office", player),
            "To Office From Lobby": lambda state: state.has("Key for Office", player),
            "To Library From Lobby": lambda state: state.has("Key for Library", player),
            "To Lobby From Library": lambda state: state.has("Key for Library", player),
            "To Prehistoric From Lobby": lambda state: state.has("Key for Prehistoric Room", player),
            "To Lobby From Prehistoric": lambda state: state.has("Key for Prehistoric Room", player),
            "To Greenhouse": lambda state: state.has("Key for Greenhouse", player),
            "To Ocean From Prehistoric": lambda state: state.has("Key for Ocean Room", player),
            "To Prehistoric From Ocean": lambda state: state.has("Key for Ocean Room", player),
            "To Projector Room": lambda state: state.has("Key for Projector Room", player),
            "To Generator From Maintenance Tunnels": lambda state: state.has("Key for Generator Room", player),
            "To Lobby From Egypt": lambda state: state.has("Key for Egypt Room", player),
            "To Egypt From Lobby": lambda state: state.has("Key for Egypt Room", player),
            "To Janitor Closet": lambda state: state.has("Key for Janitor Closet", player),
            "To Shaman From Burial": lambda state: state.has("Key for Shaman Room", player),
            "To Burial From Shaman": lambda state: state.has("Key for Shaman Room", player),
            "To Norse Stone From Gods Room": lambda state: state.has("Aligned Planets", player),
            "To Inventions From UFO": lambda state: state.has("Key for UFO Room", player),
            "To UFO From Inventions": lambda state: state.has("Key for UFO Room", player),
            "To Orrery From UFO": lambda state: state.has("Viewed Fortune", player),
            "To Torture From Inventions": lambda state: state.has("Key for Torture Room", player),
            "To Inventions From Torture": lambda state: state.has("Key for Torture Room", player),
            "To Torture": lambda state: state.has("Key for Puzzle Room", player),
            "To Puzzle Room Mastermind From Torture": lambda state: state.has("Key for Puzzle Room", player),
            "To Bedroom": lambda state: state.has("Key for Bedroom", player),
            "To Underground Lake From Underground Tunnels": lambda state: state.has("Key for Underground Lake", player),
            "To Underground Tunnels From Underground Lake": lambda state: state.has("Key for Underground Lake", player),
            "To Outside From Lobby": lambda state: state.has("Key for Front Door", player),
            "To Lobby From Outside": lambda state: state.has("Key for Front Door", player),
            "To Maintenance Tunnels From Theater Back Hallway": lambda state: state.has("Crawling", player),
            "To Blue Maze From Egypt": lambda state: state.has("Crawling", player),
            "To Egypt From Blue Maze": lambda state: state.has("Crawling", player),
            "To Lobby From Tar River": lambda state: state.has("Crawling", player) and oil_capturable(state, player),
            "To Tar River From Lobby": lambda state: state.has("Crawling", player) and oil_capturable(state, player) and state.can_reach_region("Tar River", player),
            "To Burial From Egypt": lambda state: state.can_reach_region("Egypt", player),
            "To Gods Room From Anansi": lambda state: state.can_reach_region("Gods Room", player),
            "To Slide Room": lambda state: all_skull_dials_set(state, player),
            "To Lobby From Slide Room": lambda state: state.has("Lost Your Head", player),
            "To Water Capture From Janitor Closet": lambda state: cloth_capturable(state, player),
            "To Victory": lambda state: (
                (water_capturable(state, player) + wax_capturable(state, player) + ash_capturable(state, player)
                 + oil_capturable(state, player) + cloth_capturable(state, player) + wood_capturable(state, player)
                 + crystal_capturable(state, player) + sand_capturable(state, player) + metal_capturable(state, player)
                 + lightning_capturable(state, world, player)) >= world.options.ixupi_captures_needed.value
            )
        },
        "locations_required": {
            "Puzzle Solved Anansi Music Box": lambda state: state.has("Set Song", player),
            "Storage: Anansi Music Box": lambda state: state.has("Set Song", player),
            "Storage: Clock Tower": lambda state: state.has("Set Time", player),
            "Storage: Janitor Closet": lambda state: cloth_capturable(state, player),
            "Storage: Tar River": lambda state: oil_capturable(state, player),
            "Storage: Theater": lambda state: state.has("Viewed Theater Movie", player),
            "Storage: Slide": lambda state: state.has("Lost Your Head", player) and state.can_reach_region("Slide Room", player),
            "Ixupi Captured Water": lambda state: water_capturable(state, player),
            "Ixupi Captured Wax": lambda state: wax_capturable(state, player),
            "Ixupi Captured Ash": lambda state: ash_capturable(state, player),
            "Ixupi Captured Oil": lambda state: oil_capturable(state, player),
            "Ixupi Captured Cloth": lambda state: cloth_capturable(state, player),
            "Ixupi Captured Wood": lambda state: wood_capturable(state, player),
            "Ixupi Captured Crystal": lambda state: crystal_capturable(state, player),
            "Ixupi Captured Sand": lambda state: sand_capturable(state, player),
            "Ixupi Captured Metal": lambda state: metal_capturable(state, player),
            "Puzzle Solved Skull Dial Door": lambda state: all_skull_dials_set(state, player),
        },
        "puzzle_hints_required": {
            "Puzzle Solved Clock Tower Door": lambda state: state.can_reach_region("Three Floor Elevator", player),
            "Puzzle Solved Shaman Drums": lambda state: state.can_reach_region("Clock Tower", player),
            "Puzzle Solved Red Door": lambda state: state.can_reach_region("Maintenance Tunnels", player),
            "Puzzle Solved UFO Symbols": lambda state: state.can_reach_region("Library", player),
            "Storage: UFO": lambda state: state.can_reach_region("Library", player),
            "Puzzle Solved Maze Door": lambda state: state.has("Viewed Theater Movie", player),
            "Puzzle Solved Theater Door": lambda state: state.has("Viewed Egyptian Hieroglyphics Explained", player),
            "Puzzle Solved Columns of RA": lambda state: state.has("Viewed Egyptian Hieroglyphics Explained", player),
            "Puzzle Solved Atlantis": lambda state: state.can_reach_region("Office", player),
        },
        "elevators": {
            "Puzzle Solved Office Elevator": lambda state: (state.can_reach_region("Underground Lake", player) or state.can_reach_region("Office", player))
                                                                  and state.has("Key for Office Elevator", player),
            "Puzzle Solved Bedroom Elevator": lambda state: state.has_all({"Key for Bedroom Elevator", "Crawling"}, player),
            "Puzzle Solved Three Floor Elevator": lambda state: (state.can_reach_region("Maintenance Tunnels", player) or state.can_reach_region("Blue Maze", player))
                                                                  and state.has("Key for Three Floor Elevator", player)
        },
        "lightning": {
            "Ixupi Captured Lightning": lambda state: lightning_capturable(state, world, player)
        }
    }
    return rules_lookup


def set_rules(world: "ShiversWorld") -> None:
    multiworld = world.multiworld
    player = world.player

    rules_lookup = get_rules_lookup(world, player)
    # Set required entrance rules
    for entrance_name, rule in rules_lookup["entrances"].items():
        world.get_entrance(entrance_name).access_rule = rule

    world.get_region("Clock Tower Staircase").connect(
        world.get_region("Clock Chains"),
        "To Clock Chains From Clock Tower Staircase",
        lambda state: state.can_reach_region("Bedroom", player) if world.options.puzzle_hints_required.value else True
    )

    world.get_region("Generator").connect(
        world.get_region("Beth's Body"),
        "To Beth's Body From Generator",
        lambda state: beths_body_available(state, world, player) and (
            (state.has("Viewed Norse Stone", player) and state.can_reach_region("Theater", player))
            if world.options.puzzle_hints_required.value else True
        )
    )

    world.get_region("Torture").connect(
        world.get_region("Guillotine"),
        "To Guillotine From Torture",
        lambda state: state.has("Viewed Page 17", player) and (
            state.has("Viewed Egyptian Hieroglyphics Explained", player)
            if world.options.puzzle_hints_required.value else True
        )
    )

    # Set required location rules
    for location_name, rule in rules_lookup["locations_required"].items():
        world.get_location(location_name).access_rule = rule

        world.get_location("Jukebox").access_rule = lambda state: (
            state.can_reach_region("Clock Tower", player) and (
                state.can_reach_region("Anansi", player)
                if world.options.puzzle_hints_required.value else True
            )
        )

    # Set option location rules
    if world.options.puzzle_hints_required.value:
        for location_name, rule in rules_lookup["puzzle_hints_required"].items():
            world.get_location(location_name).access_rule = rule

        world.get_entrance("To Theater From Lobby").access_rule = lambda state: state.has(
            "Viewed Egyptian Hieroglyphics Explained", player
        )

        world.get_entrance("To Clock Tower Staircase From Theater Back Hallway").access_rule = lambda state: state.can_reach_region("Three Floor Elevator", player)
        multiworld.register_indirect_condition(
            world.get_region("Three Floor Elevator"),
            world.get_entrance("To Clock Tower Staircase From Theater Back Hallway")
        )

        world.get_entrance("To Gods Room From Shaman").access_rule = lambda state: state.can_reach_region(
            "Clock Tower", player
        )
        multiworld.register_indirect_condition(
            world.get_region("Clock Tower"), world.get_entrance("To Gods Room From Shaman")
        )

        world.get_entrance("To Anansi From Gods Room").access_rule = lambda state: state.can_reach_region(
            "Maintenance Tunnels", player
        )
        multiworld.register_indirect_condition(
            world.get_region("Maintenance Tunnels"), world.get_entrance("To Anansi From Gods Room")
        )

        world.get_entrance("To Maze From Maze Staircase").access_rule = lambda \
            state: state.can_reach_region("Projector Room", player)
        multiworld.register_indirect_condition(
            world.get_region("Projector Room"), world.get_entrance("To Maze From Maze Staircase")
        )

        multiworld.register_indirect_condition(
            world.get_region("Bedroom"), world.get_entrance("To Clock Chains From Clock Tower Staircase")
        )
        multiworld.register_indirect_condition(
            world.get_region("Theater"), world.get_entrance("To Beth's Body From Generator")
        )

    if world.options.elevators_stay_solved.value:
        for location_name, rule in rules_lookup["elevators"].items():
            world.get_location(location_name).access_rule = rule
    if world.options.early_lightning.value:
        for location_name, rule in rules_lookup["lightning"].items():
            world.get_location(location_name).access_rule = rule

    # Register indirect conditions
    multiworld.register_indirect_condition(world.get_region("Prehistoric"), world.get_entrance("To Tar River From Lobby"))

    # forbid cloth in janitor closet and oil in tar river
    forbid_item(world.get_location("Storage: Janitor Closet"), "Cloth Pot Bottom DUPE", player)
    forbid_item(world.get_location("Storage: Janitor Closet"), "Cloth Pot Top DUPE", player)
    forbid_item(world.get_location("Storage: Janitor Closet"), "Cloth Pot Complete DUPE", player)
    forbid_item(world.get_location("Storage: Tar River"), "Oil Pot Bottom DUPE", player)
    forbid_item(world.get_location("Storage: Tar River"), "Oil Pot Top DUPE", player)
    forbid_item(world.get_location("Storage: Tar River"), "Oil Pot Complete DUPE", player)

    # Filler Item Forbids
    forbid_item(world.get_location("Puzzle Solved Lyre"), "Easier Lyre", player)
    forbid_item(world.get_location("Ixupi Captured Water"), "Water Always Available in Lobby", player)
    forbid_item(world.get_location("Ixupi Captured Wax"), "Wax Always Available in Library", player)
    forbid_item(world.get_location("Ixupi Captured Wax"), "Wax Always Available in Anansi Room", player)
    forbid_item(world.get_location("Ixupi Captured Wax"), "Wax Always Available in Shaman Room", player)
    forbid_item(world.get_location("Ixupi Captured Ash"), "Ash Always Available in Office", player)
    forbid_item(world.get_location("Ixupi Captured Ash"), "Ash Always Available in Burial Room", player)
    forbid_item(world.get_location("Ixupi Captured Oil"), "Oil Always Available in Prehistoric Room", player)
    forbid_item(world.get_location("Ixupi Captured Cloth"), "Cloth Always Available in Egypt", player)
    forbid_item(world.get_location("Ixupi Captured Cloth"), "Cloth Always Available in Burial Room", player)
    forbid_item(world.get_location("Ixupi Captured Wood"), "Wood Always Available in Workshop", player)
    forbid_item(world.get_location("Ixupi Captured Wood"), "Wood Always Available in Blue Maze", player)
    forbid_item(world.get_location("Ixupi Captured Wood"), "Wood Always Available in Pegasus Room", player)
    forbid_item(world.get_location("Ixupi Captured Wood"), "Wood Always Available in Gods Room", player)
    forbid_item(world.get_location("Ixupi Captured Crystal"), "Crystal Always Available in Lobby", player)
    forbid_item(world.get_location("Ixupi Captured Crystal"), "Crystal Always Available in Ocean", player)
    forbid_item(world.get_location("Ixupi Captured Sand"), "Sand Always Available in Plants Room", player)
    forbid_item(world.get_location("Ixupi Captured Sand"), "Sand Always Available in Ocean", player)
    forbid_item(world.get_location("Ixupi Captured Metal"), "Metal Always Available in Projector Room", player)
    forbid_item(world.get_location("Ixupi Captured Metal"), "Metal Always Available in Bedroom", player)
    forbid_item(world.get_location("Ixupi Captured Metal"), "Metal Always Available in Prehistoric", player)

    # Set completion condition
    multiworld.completion_condition[player] = lambda state: completion_condition(state, player)
