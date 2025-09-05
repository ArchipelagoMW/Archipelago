from typing import List, Dict, TYPE_CHECKING, Optional
from BaseClasses import Region, Location
from .Locations import LocationData
from .Options import MagicantMode
if TYPE_CHECKING:
    from . import EarthBoundWorld


class EBLocation(Location):
    game: str = "EarthBound"
    region: str

    def __init__(self, player: int, name: str = " ", address: Optional[int] = None, parent=None):
        super().__init__(player, name, address, parent)


def init_areas(world: "EarthBoundWorld", locations: List[LocationData]) -> None:
    multiworld = world.multiworld
    player = world.player

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, "Menu"),
        create_region(world, player, locations_per_region, "Ness's Mind"),
        create_region(world, player, locations_per_region, "Global ATM Access"),
        create_region(world, player, locations_per_region, "Northern Onett"),
        create_region(world, player, locations_per_region, "Onett"),
        create_region(world, player, locations_per_region, "Arcade"),
        create_region(world, player, locations_per_region, "Giant Step"),
        create_region(world, player, locations_per_region, "Twoson"),
        create_region(world, player, locations_per_region, "Common Condiment Shop"),
        create_region(world, player, locations_per_region, "Everdred's House"),
        create_region(world, player, locations_per_region, "Peaceful Rest Valley"),
        create_region(world, player, locations_per_region, "Happy-Happy Village"),
        create_region(world, player, locations_per_region, "Happy-Happy HQ"),
        create_region(world, player, locations_per_region, "Lilliput Steps"),
        create_region(world, player, locations_per_region, "Threed"),
        create_region(world, player, locations_per_region, "Threed Underground"),
        create_region(world, player, locations_per_region, "Boogey Tent"),
        create_region(world, player, locations_per_region, "Grapefruit Falls"),
        create_region(world, player, locations_per_region, "Belch's Factory"),
        create_region(world, player, locations_per_region, "Saturn Valley"),
        create_region(world, player, locations_per_region, "Upper Saturn Valley"),
        create_region(world, player, locations_per_region, "Milky Well"),
        create_region(world, player, locations_per_region, "Dusty Dunes Desert"),
        create_region(world, player, locations_per_region, "Gold Mine"),
        create_region(world, player, locations_per_region, "Monkey Caves"),
        create_region(world, player, locations_per_region, "Fourside"),
        create_region(world, player, locations_per_region, "Moonside"),
        create_region(world, player, locations_per_region, "Fourside Dept. Store"),
        create_region(world, player, locations_per_region, "Magnet Hill"),
        create_region(world, player, locations_per_region, "Monotoli Building"),
        create_region(world, player, locations_per_region, "Winters"),
        create_region(world, player, locations_per_region, "Snow Wood Boarding School"),
        create_region(world, player, locations_per_region, "Southern Winters"),
        create_region(world, player, locations_per_region, "Brickroad Maze"),
        create_region(world, player, locations_per_region, "Rainy Circle"),
        create_region(world, player, locations_per_region, "Andonuts Lab Area"),
        create_region(world, player, locations_per_region, "Stonehenge Base"),
        create_region(world, player, locations_per_region, "Summers"),
        create_region(world, player, locations_per_region, "Summers Museum"),
        create_region(world, player, locations_per_region, "Dalaam"),
        create_region(world, player, locations_per_region, "Pink Cloud"),
        create_region(world, player, locations_per_region, "Scaraba"),
        create_region(world, player, locations_per_region, "Pyramid"),
        create_region(world, player, locations_per_region, "Southern Scaraba"),
        create_region(world, player, locations_per_region, "Dungeon Man"),
        create_region(world, player, locations_per_region, "Deep Darkness"),
        create_region(world, player, locations_per_region, "Deep Darkness Darkness"),
        create_region(world, player, locations_per_region, "Tenda Village"),
        create_region(world, player, locations_per_region, "Lumine Hall"),
        create_region(world, player, locations_per_region, "Lost Underworld"),
        create_region(world, player, locations_per_region, "Fire Spring"),
        create_region(world, player, locations_per_region, "Magicant"),
        create_region(world, player, locations_per_region, "Sea of Eden"),
        create_region(world, player, locations_per_region, "Cave of the Present")

    ]
    if world.options.giygas_required:
        regions.extend([
            create_region(world, player, locations_per_region, "Cave of the Past"),
            create_region(world, player, locations_per_region, "Endgame")
        ])
    multiworld.regions += regions

def connect_area_exits(world):
    multiworld = world.multiworld
    player = world.player

    connect_menu_region(world)
    arcade_connection = world.dungeon_connections["Arcade"]
    giant_step_connection = world.dungeon_connections["Giant Step"]
    lilliput_steps_connection = world.dungeon_connections["Lilliput Steps"]
    happy_happy_hq_connection = world.dungeon_connections["Happy-Happy HQ"]
    belch_factory_connection = world.dungeon_connections["Belch's Factory"]
    milky_well_connection = world.dungeon_connections["Milky Well"]
    gold_mine_connection = world.dungeon_connections["Gold Mine"]
    moonside_connection = world.dungeon_connections["Moonside"]
    monotoli_building_connection = world.dungeon_connections["Monotoli Building"]
    magnet_hill_connection = world.dungeon_connections["Magnet Hill"]
    pink_cloud_connection = world.dungeon_connections["Pink Cloud"]
    pyramid_connection = world.dungeon_connections["Pyramid"]
    dungeon_man_connection = world.dungeon_connections["Dungeon Man"]
    rainy_circle_connection = world.dungeon_connections["Rainy Circle"]
    stonehenge_connection = world.dungeon_connections["Stonehenge Base"]
    lumine_hall_connection = world.dungeon_connections["Lumine Hall"]
    fire_spring_connection = world.dungeon_connections["Fire Spring"]
    sea_of_eden_connection = world.dungeon_connections["Sea of Eden"]
    brickroad_maze_connection = world.dungeon_connections["Brickroad Maze"]

    multiworld.get_region("Ness's Mind", player).add_exits(["Onett", "Twoson", "Happy-Happy Village", "Threed", "Saturn Valley", "Dusty Dunes Desert", "Fourside", "Winters", "Summers", "Dalaam", "Scaraba", "Deep Darkness", "Tenda Village", "Lost Underworld", "Magicant"],
                {"Onett": lambda state: state.has("Onett Teleport", player),
                    "Twoson": lambda state: state.has("Twoson Teleport", player),
                    "Happy-Happy Village": lambda state: state.has("Happy-Happy Village Teleport", player),
                    "Threed": lambda state: state.has("Threed Teleport", player),
                    "Saturn Valley": lambda state: state.has("Saturn Valley Teleport", player),
                    "Dusty Dunes Desert": lambda state: state.has("Dusty Dunes Teleport", player),
                    "Fourside": lambda state: state.has("Fourside Teleport", player),
                    "Winters": lambda state: state.has("Winters Teleport", player),
                    "Summers": lambda state: state.has("Summers Teleport", player),
                    "Dalaam": lambda state: state.has("Dalaam Teleport", player),
                    "Scaraba": lambda state: state.has("Scaraba Teleport", player),
                    "Deep Darkness": lambda state: state.has("Deep Darkness Teleport", player),
                    "Tenda Village": lambda state: state.has("Tenda Village Teleport", player),
                    "Lost Underworld": lambda state: state.has("Lost Underworld Teleport", player),
                    "Magicant": lambda state: state.has_any({"Magicant Teleport", "Magicant Unlock"}, player)})
    multiworld.get_region("Northern Onett", player).add_exits(["Onett"])

    multiworld.get_region("Onett", player).add_exits([giant_step_connection, "Twoson", "Northern Onett", "Global ATM Access", arcade_connection],
                                                    {giant_step_connection: lambda state: state.has("Key to the Shack", player),
                                                    "Twoson": lambda state: state.has("Police Badge", player),
                                                    "Northern Onett": lambda state: state.has("Police Badge", player)})

    multiworld.get_region("Twoson", player).add_exits(["Onett", "Peaceful Rest Valley", "Threed", "Everdred's House", "Global ATM Access", "Common Condiment Shop"],
                    {"Onett": lambda state: state.has("Police Badge", player),
                        "Peaceful Rest Valley": lambda state: state.has_any({"Pencil Eraser", "Valley Bridge Repair"}, player),
                        "Threed": lambda state: state.has_any({"Threed Tunnels Clear", "Wad of Bills"}, player),
                        "Everdred's House": lambda state: state.has("Paula", player)})

    multiworld.get_region("Peaceful Rest Valley", player).add_exits(["Twoson", "Happy-Happy Village"],
                                                                    {"Twoson": lambda state: state.has_any({"Pencil Eraser", "Valley Bridge Repair"}, player)})

    multiworld.get_region("Happy-Happy Village", player).add_exits(["Peaceful Rest Valley", lilliput_steps_connection, "Global ATM Access", happy_happy_hq_connection])
    
    multiworld.get_region("Threed", player).add_exits(["Twoson", "Dusty Dunes Desert", "Andonuts Lab Area", "Threed Underground", "Boogey Tent", "Global ATM Access"],
                                                    {"Twoson": lambda state: state.has("Threed Tunnels Clear", player),
                                                    "Dusty Dunes Desert": lambda state: state.has("Threed Tunnels Clear", player),
                                                    "Andonuts Lab Area": lambda state: state.has_all({"UFO Engine", "Bad Key Machine"}, player),
                                                    "Threed Underground": lambda state: state.has("Zombie Paper", player),
                                                    "Boogey Tent": lambda state: state.has("Jeff", player)})

    multiworld.get_region("Threed Underground", player).add_exits(["Grapefruit Falls"])

    multiworld.get_region("Grapefruit Falls", player).add_exits([belch_factory_connection, "Saturn Valley", "Threed Underground"],
                                                                {belch_factory_connection: lambda state: state.has("Jar of Fly Honey", player)})

    multiworld.get_region(belch_factory_connection, player).add_exits(["Upper Saturn Valley"],
                    {"Upper Saturn Valley": lambda state: state.has("Threed Tunnels Clear", player)})

    multiworld.get_region("Saturn Valley", player).add_exits(["Grapefruit Falls", "Cave of the Present", "Global ATM Access"],
                    {"Cave of the Present": lambda state: state.has("Meteorite Piece", player)})

    multiworld.get_region("Upper Saturn Valley", player).add_exits([milky_well_connection, "Saturn Valley"])

    multiworld.get_region("Dusty Dunes Desert", player).add_exits(["Threed", "Monkey Caves", gold_mine_connection, "Fourside", "Global ATM Access"],
                    {"Threed": lambda state: state.has("Threed Tunnels Clear", player),
                        "Monkey Caves": lambda state: state.has("King Banana", player),
                        gold_mine_connection: lambda state: state.has("Mining Permit", player)})

    multiworld.get_region("Fourside", player).add_exits(["Dusty Dunes Desert", monotoli_building_connection, magnet_hill_connection, "Threed", "Fourside Dept. Store", "Global ATM Access", moonside_connection],
                    {monotoli_building_connection: lambda state: state.has("Yogurt Dispenser", player),
                        magnet_hill_connection: lambda state: state.has("Signed Banana", player),
                        "Threed": lambda state: state.has("Diamond", player),
                        "Fourside Dept. Store": lambda state: state.has("Jeff", player)})

    multiworld.get_region("Moonside", player).add_exits(["Global ATM Access"])

    multiworld.get_region("Summers", player).add_exits(["Scaraba", "Summers Museum", "Global ATM Access"],
                    {"Summers Museum": lambda state: state.has("Tiny Ruby", player)})

    multiworld.get_region("Winters", player).add_exits(["Snow Wood Boarding School", "Southern Winters", "Global ATM Access"],
                    {"Snow Wood Boarding School": lambda state: state.has("Letter For Tony", player),
                        "Southern Winters": lambda state: state.has("Pak of Bubble Gum", player)})

    multiworld.get_region("Southern Winters", player).add_exits([brickroad_maze_connection])

    multiworld.get_region(brickroad_maze_connection, player).add_exits(["Southern Winters", rainy_circle_connection])

    multiworld.get_region(rainy_circle_connection, player).add_exits([brickroad_maze_connection, "Andonuts Lab Area"])

    multiworld.get_region("Andonuts Lab Area", player).add_exits([stonehenge_connection, "Winters", rainy_circle_connection],
    {stonehenge_connection: lambda state: state.has("Eraser Eraser", player)})

    multiworld.get_region("Dalaam", player).add_exits([pink_cloud_connection],
                                                    {pink_cloud_connection: lambda state: state.has("Carrot Key", player)})

    multiworld.get_region("Scaraba", player).add_exits([pyramid_connection, "Global ATM Access", "Common Condiment Shop"],
                                                    {pyramid_connection: lambda state: state.has("Hieroglyph Copy", player)})

    multiworld.get_region(pyramid_connection, player).add_exits(["Southern Scaraba"])

    multiworld.get_region("Southern Scaraba", player).add_exits([dungeon_man_connection],
                                                                {dungeon_man_connection: lambda state: state.has_any({"Key to the Tower"}, player)})

    multiworld.get_region("Dungeon Man", player).add_exits(["Deep Darkness"],
                                                        {"Deep Darkness": lambda state: state.has("Submarine to Deep Darkness", player)})

    multiworld.get_region("Deep Darkness", player).add_exits(["Deep Darkness Darkness"],
                                                            {"Deep Darkness Darkness": lambda state: state.has("Hawk Eye", player)})

    multiworld.get_region("Deep Darkness Darkness", player).add_exits(["Tenda Village", "Deep Darkness"])

    multiworld.get_region("Tenda Village", player).add_exits([lumine_hall_connection, "Deep Darkness Darkness"],
                                                            {lumine_hall_connection: lambda state: state.has("Shyness Book", player),
                                                            "Deep Darkness Darkness": lambda state: state.has_all({"Shyness Book", "Hawk Eye"}, player)})

    multiworld.get_region("Lumine Hall", player).add_exits(["Lost Underworld"])

    multiworld.get_region("Lost Underworld", player).add_exits([fire_spring_connection])

    if world.options.giygas_required:
        multiworld.get_region("Cave of the Present", player).add_exits(["Cave of the Past"],
                                                                    {"Cave of the Past": lambda state: state.has("Power of the Earth", player)})

        multiworld.get_region("Cave of the Past", player).add_exits(["Endgame"],
                                                                    {"Endgame": lambda state: state.has("Paula", player)})

    if world.options.magicant_mode < MagicantMode.option_optional_boost:  # 3
        multiworld.get_region("Magicant", player).add_exits(["Global ATM Access", sea_of_eden_connection],
                                                            {sea_of_eden_connection: lambda state: state.has("Ness", player)})


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = EBLocation(player, location_data.name, location_data.code, region)
    location.region = location_data.region

    return location


def create_region(world: "EarthBoundWorld", player: int, locations_per_region: Dict[str, List[LocationData]], name: str) -> Region:
    region = Region(name, player, world.multiworld)

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region)
            region.locations.append(location)

    return region


def get_locations_per_region(locations: List[LocationData]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region


def connect_menu_region(world: "EarthBoundWorld") -> None:
    starting_region_list = {
        0: "Northern Onett",
        1: "Onett",
        2: "Twoson",
        3: "Happy-Happy Village",
        4: "Threed",
        5: "Saturn Valley",
        6: "Fourside",
        7: "Winters",
        8: "Summers",
        9: "Dalaam",
        10: "Scaraba",
        11: "Deep Darkness",
        12: "Tenda Village",
        13: "Lost Underworld",
        14: "Magicant"
    }

    world.starting_region = starting_region_list[world.start_location]
    world.multiworld.get_region("Menu", world.player).add_exits([world.starting_region, "Ness's Mind"],
                          {"Ness's Mind": lambda state: state.has_any({"Ness", "Paula", "Jeff", "Poo"}, world.player),
                                world.starting_region: lambda state: state.has_any({"Ness", "Paula", "Jeff", "Poo"}, world.player)})
    