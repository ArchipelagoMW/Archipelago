from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
from .Options import MinigameChecks
from .level_logic import YoshiLogic
from .setup_bosses import BossReqs
if TYPE_CHECKING:
    from . import YoshisIslandWorld


class YoshisIslandLocation(Location):
    game: str = "Yoshi's Island"
    level_id: int

    def __init__(self, player: int, name: str = " ", address: int = None, parent=None, level_id: int = None):
        super().__init__(player, name, address, parent)
        self.level_id = level_id


def init_areas(world: "YoshisIslandWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player
    logic = YoshiLogic(world)

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "Overworld"),
        create_region(world, player, locations_per_region, "World 1"),
        create_region(world, player, locations_per_region, "World 2"),
        create_region(world, player, locations_per_region, "World 3"),
        create_region(world, player, locations_per_region, "World 4"),
        create_region(world, player, locations_per_region, "World 5"),
        create_region(world, player, locations_per_region, "World 6"),

        create_region(world, player, locations_per_region, "1-1"),
        create_region(world, player, locations_per_region, "1-2"),
        create_region(world, player, locations_per_region, "1-3"),
        create_region(world, player, locations_per_region, "1-4"),
        create_region(world, player, locations_per_region, "Burt The Bashful's Boss Room"),
        create_region(world, player, locations_per_region, "1-5"),
        create_region(world, player, locations_per_region, "1-6"),
        create_region(world, player, locations_per_region, "1-7"),
        create_region(world, player, locations_per_region, "1-8"),
        create_region(world, player, locations_per_region, "Salvo The Slime's Boss Room"),

        create_region(world, player, locations_per_region, "2-1"),
        create_region(world, player, locations_per_region, "2-2"),
        create_region(world, player, locations_per_region, "2-3"),
        create_region(world, player, locations_per_region, "2-4"),
        create_region(world, player, locations_per_region, "Bigger Boo's Boss Room"),
        create_region(world, player, locations_per_region, "2-5"),
        create_region(world, player, locations_per_region, "2-6"),
        create_region(world, player, locations_per_region, "2-7"),
        create_region(world, player, locations_per_region, "2-8"),
        create_region(world, player, locations_per_region, "Roger The Ghost's Boss Room"),

        create_region(world, player, locations_per_region, "3-1"),
        create_region(world, player, locations_per_region, "3-2"),
        create_region(world, player, locations_per_region, "3-3"),
        create_region(world, player, locations_per_region, "3-4"),
        create_region(world, player, locations_per_region, "Prince Froggy's Boss Room"),
        create_region(world, player, locations_per_region, "3-5"),
        create_region(world, player, locations_per_region, "3-6"),
        create_region(world, player, locations_per_region, "3-7"),
        create_region(world, player, locations_per_region, "3-8"),
        create_region(world, player, locations_per_region, "Naval Piranha's Boss Room"),

        create_region(world, player, locations_per_region, "4-1"),
        create_region(world, player, locations_per_region, "4-2"),
        create_region(world, player, locations_per_region, "4-3"),
        create_region(world, player, locations_per_region, "4-4"),
        create_region(world, player, locations_per_region, "Marching Milde's Boss Room"),
        create_region(world, player, locations_per_region, "4-5"),
        create_region(world, player, locations_per_region, "4-6"),
        create_region(world, player, locations_per_region, "4-7"),
        create_region(world, player, locations_per_region, "4-8"),
        create_region(world, player, locations_per_region, "Hookbill The Koopa's Boss Room"),

        create_region(world, player, locations_per_region, "5-1"),
        create_region(world, player, locations_per_region, "5-2"),
        create_region(world, player, locations_per_region, "5-3"),
        create_region(world, player, locations_per_region, "5-4"),
        create_region(world, player, locations_per_region, "Sluggy The Unshaven's Boss Room"),
        create_region(world, player, locations_per_region, "5-5"),
        create_region(world, player, locations_per_region, "5-6"),
        create_region(world, player, locations_per_region, "5-7"),
        create_region(world, player, locations_per_region, "5-8"),
        create_region(world, player, locations_per_region, "Raphael The Raven's Boss Room"),

        create_region(world, player, locations_per_region, "6-1"),
        create_region(world, player, locations_per_region, "6-2"),
        create_region(world, player, locations_per_region, "6-3"),
        create_region(world, player, locations_per_region, "6-4"),
        create_region(world, player, locations_per_region, "Tap-Tap The Red Nose's Boss Room"),
        create_region(world, player, locations_per_region, "6-5"),
        create_region(world, player, locations_per_region, "6-6"),
        create_region(world, player, locations_per_region, "6-7"),
        create_region(world, player, locations_per_region, "6-8"),
        create_region(world, player, locations_per_region, "Bowser's Room"),
    ]

    if world.options.extras_enabled:
        regions.insert(68, create_region(world, player, locations_per_region, "6-Extra"))
        regions.insert(58, create_region(world, player, locations_per_region, "5-Extra"))
        regions.insert(48, create_region(world, player, locations_per_region, "4-Extra"))
        regions.insert(38, create_region(world, player, locations_per_region, "3-Extra"))
        regions.insert(28, create_region(world, player, locations_per_region, "2-Extra"))
        regions.insert(18, create_region(world, player, locations_per_region, "1-Extra"))

    if world.options.minigame_checks in {MinigameChecks.option_bonus_games, MinigameChecks.option_both}:
        regions.insert(74, create_region(world, player, locations_per_region, "6-Bonus"))
        regions.insert(63, create_region(world, player, locations_per_region, "5-Bonus"))
        regions.insert(52, create_region(world, player, locations_per_region, "4-Bonus"))
        regions.insert(41, create_region(world, player, locations_per_region, "3-Bonus"))
        regions.insert(29, create_region(world, player, locations_per_region, "2-Bonus"))
        regions.insert(19, create_region(world, player, locations_per_region, "1-Bonus"))

    multiworld.regions += regions

    connect_starting_region(world)

    bosses = BossReqs(world)

    multiworld.get_region("Overworld", player).add_exits(
    ["World 1", "World 2", "World 3", "World 4", "World 5", "World 6"],
         {
              "World 1": lambda state: state.has("World 1 Gate", player),
              "World 2": lambda state: state.has("World 2 Gate", player),
              "World 3": lambda state: state.has("World 3 Gate", player),
              "World 4": lambda state: state.has("World 4 Gate", player),
              "World 5": lambda state: state.has("World 5 Gate", player),
              "World 6": lambda state: state.has("World 6 Gate", player)
         }
    )

    for cur_world in range(1, 7):
        for cur_level in range(8):
            if cur_world != 6 or cur_level != 7:
                multiworld.get_region(f"World {cur_world}", player).add_exits(
                    [world.level_location_list[(cur_world - 1) * 8 + cur_level]]
                )

    multiworld.get_region("1-4", player).add_exits([world.boss_order[0]],{world.boss_order[0]: lambda state: logic._14Clear(state)})
    multiworld.get_region("1-8", player).add_exits([world.boss_order[1]],{world.boss_order[1]: lambda state: logic._18Clear(state)})
    multiworld.get_region("2-4", player).add_exits([world.boss_order[2]],{world.boss_order[2]: lambda state: logic._24Clear(state)})
    multiworld.get_region("2-8", player).add_exits([world.boss_order[3]],{world.boss_order[3]: lambda state: logic._28Clear(state)})
    multiworld.get_region("3-4", player).add_exits([world.boss_order[4]],{world.boss_order[4]: lambda state: logic._34Clear(state)})
    multiworld.get_region("3-8", player).add_exits([world.boss_order[5]],{world.boss_order[5]: lambda state: logic._38Clear(state)})
    multiworld.get_region("4-4", player).add_exits([world.boss_order[6]],{world.boss_order[6]: lambda state: logic._44Clear(state)})
    multiworld.get_region("4-8", player).add_exits([world.boss_order[7]],{world.boss_order[7]: lambda state: logic._48Clear(state)})
    multiworld.get_region("5-4", player).add_exits([world.boss_order[8]],{world.boss_order[8]: lambda state: logic._54Clear(state)})
    multiworld.get_region("5-8", player).add_exits([world.boss_order[9]],{world.boss_order[9]: lambda state: logic._58Clear(state)})
    multiworld.get_region("World 6", player).add_exits(["6-8"],{"6-8": lambda state: bosses.castle_access(state)})
    multiworld.get_region("6-4", player).add_exits([world.boss_order[10]],{world.boss_order[10]: lambda state: logic._64Clear(state)})
    multiworld.get_region("6-8", player).add_exits(["Bowser's Room"],{"Bowser's Room": lambda state: bosses.castle_clear(state)})

    if world.options.extras_enabled:
        multiworld.get_region("World 1", player).add_exits(
            ["1-Extra"],
            {"1-Extra": lambda state: state.has_any({"Extra Panels", "Extra 1"}, player)}
        )
        multiworld.get_region("World 2", player).add_exits(
            ["2-Extra"],
            {"2-Extra": lambda state: state.has_any({"Extra Panels", "Extra 2"}, player)}
        )
        multiworld.get_region(
            "World 3", player).add_exits(["3-Extra"],
            {"3-Extra": lambda state: state.has_any({"Extra Panels", "Extra 3"}, player)}
        )
        multiworld.get_region("World 4", player).add_exits(
            ["4-Extra"],
            {"4-Extra": lambda state: state.has_any({"Extra Panels", "Extra 4"}, player)}
        )
        multiworld.get_region("World 5", player).add_exits(
            ["5-Extra"],
            {"5-Extra": lambda state: state.has_any({"Extra Panels", "Extra 5"}, player)}
        )
        multiworld.get_region("World 6", player).add_exits(
            ["6-Extra"],
            {"6-Extra": lambda state: state.has_any({"Extra Panels", "Extra 6"}, player)}
        )

    if world.options.minigame_checks in {MinigameChecks.option_bonus_games, MinigameChecks.option_both}:
        multiworld.get_region("World 1", player).add_exits(
            ["1-Bonus"],
            {"1-Bonus": lambda state: state.has_any({"Bonus Panels", "Bonus 1"}, player)}
        )
        multiworld.get_region("World 2", player).add_exits(
            ["2-Bonus"],
            {"2-Bonus": lambda state: state.has_any({"Bonus Panels", "Bonus 2"}, player)}
        )
        multiworld.get_region("World 3", player).add_exits(
            ["3-Bonus"],
            {"3-Bonus": lambda state: state.has_any({"Bonus Panels", "Bonus 3"}, player)}
        )
        multiworld.get_region("World 4", player).add_exits(
            ["4-Bonus"],
            {"4-Bonus": lambda state: state.has_any({"Bonus Panels", "Bonus 4"}, player)}
        )
        multiworld.get_region("World 5", player).add_exits(
            ["5-Bonus"],
            {"5-Bonus": lambda state: state.has_any({"Bonus Panels", "Bonus 5"}, player)}
        )
        multiworld.get_region("World 6", player).add_exits(
            ["6-Bonus"],
            {"6-Bonus": lambda state: state.has_any({"Bonus Panels", "Bonus 6"}, player)}
        )


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = YoshisIslandLocation(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule
    location.level_id = location_data.LevelID

    return location


def create_region(world: "YoshisIslandWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region

def connect_starting_region(world: "YoshisIslandWorld") -> None:
    multiworld = world.multiworld
    player = world.player
    menu = multiworld.get_region("Menu", player)
    world_main = multiworld.get_region("Overworld", player)

    starting_region = multiworld.get_region(f"World {world.options.starting_world + 1}", player)

    menu.connect(world_main, "Start Game")
    world_main.connect(starting_region, "Overworld")


def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
