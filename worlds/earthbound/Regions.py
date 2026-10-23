from typing import List, Dict, TYPE_CHECKING
from BaseClasses import Region, Location
from .Locations import LocationData
from .Options import MagicantMode
from rule_builder.rules import HasAll, HasAny, Has
if TYPE_CHECKING:
    from . import EarthBoundWorld


class EBLocation(Location):
    game: str = "EarthBound"


def init_areas(world: "EarthBoundWorld", locations: list[LocationData]) -> None:
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


def connect_area_exits(world: "EarthBoundWorld"):
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

    world.get_region("Ness's Mind").add_exits(["Onett", "Twoson", "Happy-Happy Village", "Threed", "Saturn Valley", "Dusty Dunes Desert", "Fourside", "Winters", "Summers", "Dalaam", "Scaraba", "Deep Darkness", "Tenda Village", "Lost Underworld", "Magicant"],
                {"Onett": Has("Onett Teleport"),
                    "Twoson": Has("Twoson Teleport"),
                    "Happy-Happy Village": Has("Happy-Happy Village Teleport"),
                    "Threed": Has("Threed Teleport"),
                    "Saturn Valley": Has("Saturn Valley Teleport"),
                    "Dusty Dunes Desert": Has("Dusty Dunes Teleport"),
                    "Fourside": Has("Fourside Teleport"),
                    "Winters": Has("Winters Teleport"),
                    "Summers": Has("Summers Teleport"),
                    "Dalaam": Has("Dalaam Teleport"),
                    "Scaraba": Has("Scaraba Teleport"),
                    "Deep Darkness": Has("Deep Darkness Teleport"),
                    "Tenda Village": Has("Tenda Village Teleport"),
                    "Lost Underworld": Has("Lost Underworld Teleport"),
                    "Magicant": HasAny("Magicant Teleport", "Magicant Unlock")})
    world.get_region("Northern Onett").add_exits(["Onett"])

    world.get_region("Onett").add_exits([giant_step_connection, "Twoson", "Northern Onett", "Global ATM Access", arcade_connection],
                                        {giant_step_connection: Has("Key to the Shack"),
                                         "Twoson": Has("Police badge"),
                                         "Northern Onett": Has("Police Badge")})

    world.get_region("Twoson").add_exits(["Onett", "Peaceful Rest Valley", "Threed", "Everdred's House", "Global ATM Access", "Common Condiment Shop"],
                                         {"Onett": Has("Police Badge"),
                                          "Peaceful Rest Valley": HasAny("Pencil Eraser", "Valley Bridge Repair"),
                                          "Threed": HasAny("Threed Tunnels Clear", "Wad of Bills"),
                                          "Everdred's House": Has("Paula")})

    world.get_region("Peaceful Rest Valley").add_exits(["Twoson", "Happy-Happy Village"],
                                                       {"Twoson": HasAny("Pencil Eraser", "Valley Bridge Repair")})

    world.get_region("Happy-Happy Village").add_exits(["Peaceful Rest Valley", lilliput_steps_connection, "Global ATM Access", happy_happy_hq_connection])
    
    world.get_region("Threed").add_exits(["Twoson", "Dusty Dunes Desert", "Andonuts Lab Area", "Threed Underground", "Boogey Tent", "Global ATM Access"],
                                         {"Twoson": Has("Threed Tunnels Clear"),
                                          "Dusty Dunes Desert": Has("Threed Tunnels Clear"),
                                          "Andonuts Lab Area": HasAll("UFO Engine", "Bad Key Machine"),
                                          "Threed Underground": Has("Zombie Paper"),
                                          "Boogey Tent": Has("Jeff")})

    world.get_region("Threed Underground").add_exits(["Grapefruit Falls"])

    world.get_region("Grapefruit Falls").add_exits([belch_factory_connection, "Saturn Valley", "Threed Underground"],
                                                   {belch_factory_connection: Has("Jar of Fly Honey")})

    world.get_region(belch_factory_connection).add_exits(["Upper Saturn Valley"],
                                                         {"Upper Saturn Valley": Has("Threed Tunnels Clear")})

    world.get_region("Saturn Valley").add_exits(["Grapefruit Falls", "Cave of the Present", "Global ATM Access"],
                                                {"Cave of the Present": Has("Meteorite Piece")})

    world.get_region("Upper Saturn Valley").add_exits([milky_well_connection, "Saturn Valley"])

    world.get_region("Dusty Dunes Desert").add_exits(["Threed", "Monkey Caves", gold_mine_connection, "Fourside", "Global ATM Access"],
                                                     {"Threed": Has("Threed Tunnels Clear"),
                                                      "Monkey Caves": Has("King Banana"),
                                                      gold_mine_connection: Has("Mining Permit")})

    world.get_region("Fourside").add_exits(["Dusty Dunes Desert", monotoli_building_connection, magnet_hill_connection, "Threed", "Fourside Dept. Store", "Global ATM Access", moonside_connection],
                                           {monotoli_building_connection: Has("Yogurt Dispenser"),
                                            magnet_hill_connection: Has("Signed Banana"),
                                            "Threed": Has("Diamond"),
                                            "Fourside Dept. Store": Has("Jeff")})

    world.get_region("Moonside").add_exits(["Global ATM Access"])

    world.get_region("Summers").add_exits(["Scaraba", "Summers Museum", "Global ATM Access"],
                                          {"Summers Museum": Has("Tiny Ruby")})

    world.get_region("Winters").add_exits(["Snow Wood Boarding School", "Southern Winters", "Global ATM Access"],
                                          {"Snow Wood Boarding School": Has("Letter For Tony"),
                                           "Southern Winters": Has("Pak of Bubble Gum")})

    world.get_region("Southern Winters").add_exits([brickroad_maze_connection])

    world.get_region(brickroad_maze_connection).add_exits(["Southern Winters", rainy_circle_connection])

    world.get_region(rainy_circle_connection).add_exits([brickroad_maze_connection, "Andonuts Lab Area"])

    world.get_region("Andonuts Lab Area").add_exits([stonehenge_connection, "Winters", rainy_circle_connection],
                                                    {stonehenge_connection: Has("Eraser Eraser")})

    world.get_region("Dalaam").add_exits([pink_cloud_connection],
                                         {pink_cloud_connection: Has("Carrot Key")})

    world.get_region("Scaraba").add_exits([pyramid_connection, "Global ATM Access", "Common Condiment Shop"],
                                          {pyramid_connection: Has("Hieroglyph Copy")})

    world.get_region(pyramid_connection).add_exits(["Southern Scaraba"])

    world.get_region("Southern Scaraba").add_exits([dungeon_man_connection],
                                                   {dungeon_man_connection: Has("Key to the Tower")})

    world.get_region("Dungeon Man").add_exits(["Deep Darkness"],
                                              {"Deep Darkness": Has("Submarine to Deep Darkness")})

    world.get_region("Deep Darkness").add_exits(["Deep Darkness Darkness"],
                                                {"Deep Darkness Darkness": Has("Hawk Eye")})

    world.get_region("Deep Darkness Darkness").add_exits(["Tenda Village", "Deep Darkness"])

    world.get_region("Tenda Village").add_exits([lumine_hall_connection, "Deep Darkness Darkness"],
                                                {lumine_hall_connection: Has("Shyness Book"),
                                                 "Deep Darkness Darkness": HasAll("Shyness Book", "Hawk Eye")})

    world.get_region("Lumine Hall").add_exits(["Lost Underworld"])

    world.get_region("Lost Underworld").add_exits([fire_spring_connection])

    if world.options.giygas_required:
        world.get_region("Cave of the Present").add_exits(["Cave of the Past"],
                                                          {"Cave of the Past": Has("Power of the Earth")})

        world.get_region("Cave of the Past").add_exits(["Endgame"],
                                                       {"Endgame": Has("Paula")})

    if world.options.magicant_mode < MagicantMode.option_optional_boost:  # 3
        world.get_region("Magicant").add_exits(["Global ATM Access", sea_of_eden_connection],
                                               {sea_of_eden_connection: Has("Ness")})


def create_location(player: int, location_data: LocationData, region: Region) -> Location:
    location = EBLocation(player, location_data.name, location_data.code, region)

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
    world.get_region("Menu").add_exits([world.starting_region, "Ness's Mind"],
                                       {"Ness's Mind": HasAny("Ness", "Paula", "Jeff", "Poo"),
                                        world.starting_region: HasAny("Ness", "Paula", "Jeff", "Poo")})
    