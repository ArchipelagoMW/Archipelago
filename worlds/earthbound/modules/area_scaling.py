from ..modules.enemy_data import combat_regions
from ..Options import MagicantMode
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .. import EarthBoundWorld


expected_level_gains = {
    "Ness's Mind": 0,
    "Global ATM Access": 0,
    "Northern Onett": 1,
    "Onett": 1,
    "Arcade": 0,
    "Giant Step": 2,
    "Twoson": 0,
    "Everdred's House": 1,
    "Common Condiment Shop": 0,
    "Peaceful Rest Valley": 2,
    "Happy-Happy Village": 0,
    "Happy-Happy HQ": 1,
    "Lilliput Steps": 2,
    "Threed": 0,
    "Boogey Tent": 0,
    "Threed Underground": 2,
    "Grapefruit Falls": 1,
    "Saturn Valley": 0,
    "Belch's Factory": 2,
    "Upper Saturn Valley": 0,
    "Milky Well": 3,
    "Dusty Dunes Desert": 2,
    "Gold Mine": 2,
    "Monkey Caves": 2,
    "Fourside": 0,
    "Fourside Dept. Store": 1,
    "Moonside": 1,
    "Monotoli Building": 2,
    "Magnet Hill": 2,
    "Winters": 2,
    "Snow Wood Boarding School": 0,
    "Southern Winters": 1,
    "Brickroad Maze": 1,
    "Andonuts Lab Area": 0,
    "Rainy Circle": 2,
    "Stonehenge Base": 2,
    "Summers": 0,
    "Summers Museum": 0,
    "Dalaam": 0,
    "Pink Cloud": 2,
    "Scaraba": 0,
    "Pyramid": 2,
    "Southern Scaraba": 1,
    "Dungeon Man": 2,
    "Deep Darkness": 0,
    "Deep Darkness Darkness": 2,
    "Tenda Village": 0,
    "Lumine Hall": 2,
    "Lost Underworld": 2,
    "Fire Spring": 2,
    "Magicant": 1,
    "Sea of Eden": 1,
    "Cave of the Present": 0,
    "Cave of the Past": 2,
    "Endgame": 0
}

locations_with_item_requirements = [
    "Onett - Traveling Entertainer",
    "Onett - South Road Present",
    "Onett - Tracy Gift",
    "Twoson - Paula's Mother",
    "Twoson - Everdred Meeting",
    "Twoson - Insignificant Location",
    "Happy-Happy Village - Defeat Carpainter",
    "Happy-Happy Village - Prisoner",
    "Threed - Boogey Tent Trashcan",
    "Threed - Zombie Prisoner",
    "Saturn Valley - Post Belch Gift #1",
    "Saturn Valley - Post Belch Gift #2",
    "Saturn Valley - Post Belch Gift #3",
    "Saturn Valley - Saturn Coffee",
    "Monkey Caves - Talah Rama Chest #1",
    "Monkey Caves - Talah Rama Chest #2",
    "Monkey Caves - Talah Rama Gift",
    "Monkey Caves - Monkey Power",
    "Dusty Dunes - Mine Reward",
    "Snow Wood - Upper Right Locker",
    "Snow Wood - Upper Left Locker",
    "Snow Wood - Bottom Right Locker",
    "Snow Wood - Bottom Left Locker",
    "Fourside - Bakery 2F Gift",
    "Fourside - Department Store Blackout",
    "Fourside - Venus Gift",
    "Summers - Museum Item",
    "Dalaam - Trial of Mu",
    "Deep Darkness - North Alcove Truffle",
    "Deep Darkness - Near Land Truffle",
    "Deep Darkness - Present Truffle",
    "Deep Darkness - Village Truffle",
    "Deep Darkness - Entrance Truffle",
    "Tenda Village - Tenda Tea",
    "Tenda Village - Tenda Gift",
    "Tenda Village - Tenda Gift #2",
    "Lost Underworld - Talking Rock",
    "Lost Underworld - Tenda Camp Shop Slot 1",
    "Lost Underworld - Tenda Camp Shop Slot 2",
    "Lost Underworld - Tenda Camp Shop Slot 3",
    "Lost Underworld - Tenda Camp Shop Slot 4",
    "Lost Underworld - Tenda Camp Shop Slot 5",
    "Lost Underworld - Tenda Camp Shop Slot 6",
    "Lost Underworld - Tenda Camp Shop Slot 7",
    "Dusty Dunes - Mine Food Cart Slot 1",
    "Dusty Dunes - Mine Food Cart Slot 2",
    "Dusty Dunes - Mine Food Cart Slot 3",
    "Dusty Dunes - Mine Food Cart Slot 4",
    "Dusty Dunes - Mine Food Cart Slot 5",
    "Dusty Dunes - Mine Food Cart Slot 6",
    "Dusty Dunes - Mine Food Cart Slot 7",
    "Saturn Valley Shop - Post-Belch Saturn Slot 1",
    "Saturn Valley Shop - Post-Belch Saturn Slot 2",
    "Saturn Valley Shop - Post-Belch Saturn Slot 3",
    "Saturn Valley Shop - Post-Belch Saturn Slot 4",
    "Deep Darkness - Arms Dealer Slot 1",
    "Deep Darkness - Arms Dealer Slot 2",
    "Deep Darkness - Arms Dealer Slot 3",
    "Deep Darkness - Arms Dealer Slot 4",
    "Deep Darkness - Businessman Slot 1",
    "Deep Darkness - Businessman Slot 2",
    "Deep Darkness - Businessman Slot 3",
    "Deep Darkness - Businessman Slot 4",
    "Deep Darkness - Businessman Slot 5",
    "Deep Darkness - Businessman Slot 6",
    "Deep Darkness - Businessman Slot 7",
    "Dalaam Restaurant - Slot 1",
    "Dalaam Restaurant - Slot 2",
    "Dalaam Restaurant - Slot 3",
    "Dalaam Restaurant - Slot 4"]


def calculate_scaling(world: "EarthBoundWorld") -> None:
    """Calculates the individual scaled level of each region/major area."""
    arcade = world.dungeon_connections["Arcade"]
    giant_step = world.dungeon_connections["Giant Step"]
    lilliput_steps = world.dungeon_connections["Lilliput Steps"]
    happy_happy_hq = world.dungeon_connections["Happy-Happy HQ"]
    belch_factory = world.dungeon_connections["Belch's Factory"]
    milky_well = world.dungeon_connections["Milky Well"]
    gold_mine = world.dungeon_connections["Gold Mine"]
    monotoli_building = world.dungeon_connections["Monotoli Building"]
    magnet_hill = world.dungeon_connections["Magnet Hill"]
    moonside = world.dungeon_connections["Moonside"]
    pink_cloud = world.dungeon_connections["Pink Cloud"]
    rainy_circle = world.dungeon_connections["Rainy Circle"]
    stonehenge_base = world.dungeon_connections["Stonehenge Base"]
    brickroad_maze = world.dungeon_connections["Brickroad Maze"]
    pyramid = world.dungeon_connections["Pyramid"]
    dungeon_man = world.dungeon_connections["Dungeon Man"]
    lumine_hall = world.dungeon_connections["Lumine Hall"]
    fire_spring = world.dungeon_connections["Fire Spring"]
    sea_of_eden = world.dungeon_connections["Sea of Eden"]
    world.area_exits = {
        "Ness's Mind": ["Onett", "Twoson", "Happy-Happy Village", "Threed", "Saturn Valley", "Dusty Dunes Desert",
                        "Fourside", "Winters", "Summers", "Dalaam", "Scaraba", "Deep Darkness", "Tenda Village",
                        "Lost Underworld", "Magicant"],
        "Northern Onett": ["Onett"],
        "Onett": ["Northern Onett", "Twoson", giant_step, arcade, "Global ATM Access"],
        arcade: [arcade],
        "Giant Step": ["Giant Step"],
        "Twoson": ["Onett", "Peaceful Rest Valley", "Threed", "Everdred's House", "Common Condiment Shop", "Global ATM Access"],
        "Everdred's House": ["Everdred's House"],
        "Peaceful Rest Valley": ["Twoson", "Happy-Happy Village"],
        "Happy-Happy Village": ["Peaceful Rest Valley", lilliput_steps, happy_happy_hq, "Global ATM Access"],
        "Happy-Happy HQ": ["Happy-Happy HQ"],
        "Lilliput Steps": ["Lilliput Steps"],
        "Threed": ["Twoson", "Dusty Dunes Desert", "Andonuts Lab Area", "Threed Underground", "Boogey Tent", "Winters", "Global ATM Access"],
        "Boogey Tent": ["Boogey Tent"],
        "Threed Underground": ["Grapefruit Falls"],
        "Grapefruit Falls": [belch_factory, "Saturn Valley", "Threed Underground"],
        "Saturn Valley": ["Grapefruit Falls", "Cave of the Present", "Global ATM Access"],
        belch_factory: ["Upper Saturn Valley"],
        "Upper Saturn Valley": ["Saturn Valley", world.dungeon_connections["Milky Well"]],
        "Milky Well": ["Milky Well"],
        "Dusty Dunes Desert": ["Threed", "Monkey Caves", gold_mine, "Fourside", "Global ATM Access"],
        "Monkey Caves": ["Monkey Caves"],
        "Gold Mine": ["Gold Mine"],
        "Fourside": ["Dusty Dunes Desert", monotoli_building, magnet_hill, "Threed", "Fourside Dept. Store", moonside, "Global ATM Access"],
        "Moonside": ["Moonside", "Global ATM Access"],
        "Monotoli Building": ["Monotoli Building"],
        "Fourside Dept. Store": ["Fourside Dept. Store"],
        "Magnet Hill": ["Magnet Hill"],
        "Winters": ["Snow Wood Boarding School", "Southern Winters", "Global ATM Access"],
        "Snow Wood Boarding School": ["Snow Wood Boarding School"],
        "Southern Winters": [brickroad_maze],
        brickroad_maze: [rainy_circle, "Southern Winters"],
        "Stonehenge Base": ["Stonehenge Base"],
        rainy_circle: [brickroad_maze, "Andonuts Lab Area"],
        "Andonuts Lab Area": [rainy_circle, "Winters", stonehenge_base],
        "Summers": ["Scaraba", "Summers Museum", "Global ATM Access"],
        "Summers Museum": ["Summers Museum"],
        "Dalaam": [pink_cloud],
        "Pink Cloud": ["Pink Cloud"],
        "Scaraba": [pyramid, "Common Condiment Shop", "Global ATM Access"],
        pyramid: ["Southern Scaraba"],
        "Southern Scaraba": [dungeon_man],
        "Dungeon Man": ["Deep Darkness"],
        "Deep Darkness": ["Deep Darkness Darkness"],
        "Deep Darkness Darkness": ["Tenda Village", "Deep Darkness"],
        "Tenda Village": [lumine_hall, "Deep Darkness Darkness"],
        "Lumine Hall": ["Lost Underworld"],
        "Lost Underworld": [fire_spring],
        "Fire Spring": ["Fire Spring"],
        "Magicant": [sea_of_eden, "Global ATM Access"],
        "Sea of Eden": ["Sea of Eden"],
        "Cave of the Present": ["Cave of the Past"],
        "Cave of the Past": ["Endgame"],
        "Endgame": ["Endgame"],
        "Global ATM Access": ["Global ATM Access"],
        "Common Condiment Shop": ["Common Condiment Shop"]
    }

    world.area_rules = {
        "Ness's Mind": {"Onett": [["Onett Teleport"]],
                        "Twoson": [["Twoson Teleport"]],
                        "Happy-Happy Village": [["Happy-Happy Village Teleport"]],
                        "Threed": [["Threed Teleport"]],
                        "Saturn Valley": [["Saturn Valley Teleport"]],
                        "Dusty Dunes Desert": [["Dusty Dunes Teleport"]],
                        "Fourside": [["Fourside Teleport"]],
                        "Winters": [["Winters Teleport"]],
                        "Summers": [["Summers Teleport"]],
                        "Dalaam": [["Dalaam Teleport"]],
                        "Scaraba": [["Scaraba Teleport"]],
                        "Deep Darkness": [["Deep Darkness Teleport"]],
                        "Tenda Village": [["Tenda Village Teleport"]],
                        "Lost Underworld": [["Lost Underworld Teleport"]],
                        "Magicant": [["Magicant Teleport"], ["Magicant Unlock"]]
                        },

        "Northern Onett": {"Onett": [["Nothing"]]},
        "Onett": 
            {"Northern Onett": [["Police Badge"]],
             "Twoson": [["Police Badge"]],
             giant_step: [["Key to the Shack"]],
             arcade: [["Nothing"]],
             "Global ATM Access": [["Nothing"]]},
        
        arcade: {arcade: [["Nothing"]]},
        "Giant Step": {"Giant Step": [["Nothing"]]},

        "Twoson": {"Onett": [["Police Badge"]],
                   "Peaceful Rest Valley": [["Pencil Eraser"], ["Valley Bridge Repair"]],
                   "Threed": [["Wad of Bills"], ["Threed Tunnels Clear"]],
                   "Everdred's House": [["Paula"]],
                   "Common Condiment Shop": [["Nothing"]],
                   "Global ATM Access": [["Nothing"]]},

        "Everdred's House": {"Everdred's House": [["Nothing"]]},

        "Peaceful Rest Valley": {"Twoson": [["Pencil Eraser"], ["Valley Bridge Repair"]],
                                 "Happy-Happy Village": [["Nothing"]]},

        "Happy-Happy Village": {"Peaceful Rest Valley": [["Nothing"]],
                                lilliput_steps: [["Nothing"]],
                                happy_happy_hq: [["Nothing"]],
                                "Global ATM Access": [["Nothing"]]},

        "Happy-Happy HQ": {"Happy-Happy HQ": [["Nothing"]]},

        "Lilliput Steps": {"Lilliput Steps": [["Nothing"]]},

        "Threed": {"Twoson": [["Threed Tunnels Clear"]],
                   "Dusty Dunes Desert": [["Threed Tunnels Clear"]],
                   "Andonuts Lab Area": [["UFO Engine", "Bad Key Machine"]],
                   "Threed Underground": [["Zombie Paper"]],
                   "Boogey Tent": [["Jeff"]],
                   "Winters": [["UFO Engine", "Bad Key Machine"]],
                   "Global ATM Access": [["Nothing"]]},

        "Boogey Tent": {"Boogey Tent": [["Nothing"]]},

        "Threed Underground": {"Grapefruit Falls": [["Nothing"]]},
                                
        "Grapefruit Falls": {belch_factory: [["Jar of Fly Honey"]],
                             "Saturn Valley": [["Nothing"]],
                             "Threed Underground": [["Nothing"]]},

        "Saturn Valley": {"Grapefruit Falls": [["Nothing"]],
                          "Cave of the Present": [["Meteorite Piece"]],
                          "Global ATM Access": [["Nothing"]]},

        belch_factory: {"Upper Saturn Valley": [["Threed Tunnels Clear"]]},

        "Upper Saturn Valley": {"Saturn Valley": [["Nothing"]],
                                milky_well: [["Nothing"]]},

        "Milky Well": {"Milky Well": [["Nothing"]]},

        "Dusty Dunes Desert": {"Threed": [["Threed Tunnels Clear"]],
                               "Monkey Caves": [["King Banana"]],
                               gold_mine: [["Mining Permit"]],
                               "Fourside": [["Nothing"]],
                               "Global ATM Access": [["Nothing"]]},

        "Monkey Caves": {"Monkey Caves": [["Nothing"]]},

        "Gold Mine": {"Gold Mine": [["Nothing"]]},

        "Fourside": {"Dusty Dunes Desert": [["Nothing"]],
                     monotoli_building: [["Yogurt Dispenser"]],
                     "Threed": [["Diamond"]],
                     magnet_hill: [["Signed Banana"]],
                     "Fourside Dept. Store": [["Jeff"]],
                     moonside: [["Nothing"]],
                     "Global ATM Access": [["Nothing"]]},

        "Monotoli Building": {"Monotoli Building": [["Nothing"]]},

        "Moonside": {"Moonside": [["Nothing"]],
                     "Global ATM Access": [["Nothing"]]},

        "Fourside Dept. Store": {"Fourside Dept. Store": [["Nothing"]]},

        "Magnet Hill": {"Magnet Hill": [["Nothing"]]},

        "Winters": {"Snow Wood Boarding School": [["Letter For Tony"]],
                    "Southern Winters": [["Pak of Bubble Gum"]],
                    "Global ATM Access": [["Nothing"]]},

        "Snow Wood Boarding School": {"Snow Wood Boarding School": [["Nothing"]]},

        "Southern Winters": {brickroad_maze: [["Nothing"]]},

        brickroad_maze: {rainy_circle: [["Nothing"]],
                         "Southern Winters": [["Nothing"]],
                         brickroad_maze: [["Nothing"]]},

        rainy_circle: {rainy_circle: [["Nothing"]],
                       "Andonuts Lab Area": [["Nothing"]],
                       brickroad_maze: [["Nothing"]]},

        "Andonuts Lab Area": {rainy_circle: [["Nothing"]],
                              stonehenge_base: [["Eraser Eraser"]],
                              "Winters": [["Nothing"]]},

        "Stonehenge Base": {"Stonehenge Base": [["Nothing"]]},

        "Summers": {"Scaraba": [["Nothing"]],
                    "Summers Museum": [["Tiny Ruby"]],
                    "Global ATM Access": [["Nothing"]]},
        
        "Summers Museum": {"Summers Museum": [["Nothing"]]},

        "Dalaam": {pink_cloud: [["Carrot Key"]]},

        "Pink Cloud": {"Pink Cloud": [["Nothing"]]},

        "Scaraba": {pyramid: [["Hieroglyph Copy"]],
                    "Common Condiment Shop": [["Nothing"]],
                    "Global ATM Access": [["Nothing"]]},

        pyramid: {"Southern Scaraba": [["Nothing"]]},
        
        "Southern Scaraba": {dungeon_man: [["Key to the Tower"]]},

        "Dungeon Man": {"Deep Darkness": [["Submarine to Deep Darkness"]]},

        "Deep Darkness": {"Deep Darkness Darkness": [["Hawk Eye"]]},

        "Deep Darkness Darkness": {"Tenda Village": [["Nothing"]],
                                   "Deep Darkness": [["Nothing"]]},

        "Tenda Village": {lumine_hall: [["Shyness Book"]],
                          "Deep Darkness Darkness": [["Hawk Eye"]]},

        "Lumine Hall": {"Lost Underworld": [["Nothing"]]},

        "Lost Underworld": {fire_spring: [["Nothing"]]},

        "Fire Spring": {"Fire Spring": [["Nothing"]]},

        "Magicant": {sea_of_eden: [["Ness"]],
                     "Global ATM Access": [["Nothing"]]},

        "Sea of Eden": {"Sea of Eden": [["Nothing"]]},

        "Cave of the Present": {"Cave of the Past": [["Power of the Earth"]]},

        "Cave of the Past": {"Endgame": [["Paula"]]},

        "Endgame": {"Endgame": [["Nothing"]]},

        "Common Condiment Shop": {"Common Condiment Shop": [["Nothing"]]},

        "Global ATM Access": {"Global ATM Access": [["Nothing"]]}
        
    }

    teleports = {
        "Onett Teleport": "Onett",
        "Twoson Teleport": "Twoson",
        "Happy-Happy Village Teleport": "Happy-Happy Village",
        "Threed Teleport": "Threed",
        "Saturn Valley Teleport": "Saturn Valley",
        "Dusty Dunes Teleport": "Dusty Dunes Desert",
        "Fourside Teleport": "Fourside",
        "Winters Teleport": "Winters",
        "Summers Teleport": "Summers",
        "Scaraba Teleport": "Scaraba",
        "Dalaam Teleport": "Dalaam",
        "Deep Darkness Teleport": "Deep Darkness",
        "Tenda Village Teleport": "Tenda Village",
        "Lost Underworld Teleport": "Lost Underworld",
        "Magicant Teleport": "Magicant"
    }

    if world.options.no_free_sanctuaries:
        world.area_rules["Happy-Happy Village"][lilliput_steps] = [["Tiny Key"]]
        world.area_rules["Lost Underworld"][fire_spring] = [["Tenda Lavapants"]]
    else:
        world.area_rules["Happy-Happy Village"][lilliput_steps] = [["Nothing"]]
        world.area_rules["Lost Underworld"][fire_spring] = [["Nothing"]]

    inventory = {0: ["Nothing"]}  # Nothing means no item needed for connection
    item_regions = {}

    for item in world.multiworld.precollected_items[world.player]:
        inventory[0].append(item.name)

    unconnected_regions = [world.starting_region, "Ness's Mind"]
    world.accessible_regions = [world.starting_region, "Ness's Mind"]
    if world.options.random_start_location:
        unconnected_regions.append(teleports[world.starting_teleport])
        world.accessible_regions.append(teleports[world.starting_teleport])

    world.scaled_area_order = []
    passed_connections = []
    local_prog = []
    ness_scaled = False
    paula_scaled = False
    jeff_scaled = False
    poo_scaled = False
    badge_scaled = False
    scaled_chars = {
        "Ness": ness_scaled,
        "Paula": paula_scaled,
        "Jeff": jeff_scaled,
        "Poo": poo_scaled
    }

    sphere_count = 0
    last_region = "Ness's Mind"
    regions_that_were_already_scaled = []
    early_regions = []
    world.Ness_region = "Ness's Mind"
    world.Paula_region = "Ness's Mind"
    world.Jeff_region = "Ness's Mind"
    world.Poo_region = "Ness's Mind"
    world.Badge_region = "Ness's Mind"
    for item in world.multiworld.precollected_items[world.player]:
        if item.name in ["Ness", "Paula", "Jeff", "Poo"]:
            scaled_chars[item.name] = True

        if item.name == "Franklin Badge":
            badge_scaled = True

    for num, sphere in enumerate(world.multiworld.earthbound_locations_by_sphere):
        if num + 1 not in inventory:
            inventory[num + 1] = []

        for location in sorted(sphere):
            if num == 0:
                if location.parent_region.name not in world.accessible_regions and location.player == world.player:
                    early_regions.append(location.parent_region.name)
                    world.accessible_regions.append(location.parent_region.name)
                    unconnected_regions.append(location.parent_region.name)

            if location.item.player == world.player and location.item.advancement:
                inventory[num + 1].append(location.item.name)
                if location.player == world.player:
                    local_prog.append(location.item.name)
                if location.item.name not in item_regions:
                    item_regions[location.item.name] = []
                item_regions[location.item.name].append(location.parent_region.name)

            # TODO; all areas have levels now, so I can skip the combat regions check
            if location.player == world.player and location.parent_region.name in combat_regions and (
                    location.parent_region.name not in regions_that_were_already_scaled):
                last_region = location.parent_region.name
            
            regions_that_were_already_scaled.append(last_region)

            if location.item.player == world.player and location.item.name == "Ness" and not scaled_chars["Ness"]:
                if location.parent_region.name in combat_regions and (location.player == world.player) and (
                        location.name not in locations_with_item_requirements):
                    world.Ness_region = location.parent_region.name
                else:
                    world.Ness_region = last_region
                scaled_chars["Ness"] = True

            if location.item.player == world.player and location.item.name == "Paula" and not scaled_chars["Paula"]:
                if location.parent_region.name in combat_regions and (location.player == world.player) and (
                        location.name not in locations_with_item_requirements):
                    world.Paula_region = location.parent_region.name
                else:
                    world.Paula_region = last_region
                scaled_chars["Paula"] = True

            if location.item.player == world.player and location.item.name == "Jeff" and not scaled_chars["Jeff"]:
                if location.parent_region.name in combat_regions and (location.player == world.player) and (
                        location.name not in locations_with_item_requirements):
                    world.Jeff_region = location.parent_region.name
                else:
                    world.Jeff_region = last_region
                scaled_chars["Jeff"] = True

            if location.item.player == world.player and location.item.name == "Poo" and not scaled_chars["Poo"]:
                if location.parent_region.name in combat_regions and (location.player == world.player) and (
                        location.name not in locations_with_item_requirements):
                    world.Poo_region = location.parent_region.name
                else:
                    world.Poo_region = last_region
                scaled_chars["Poo"] = True

            if location.item.player == world.player and location.item.name == "Franklin Badge" and not badge_scaled:
                if location.parent_region.name in combat_regions and (location.player == world.player) and (
                        location.name not in locations_with_item_requirements):
                    world.Badge_region = location.parent_region.name
                else:
                    world.Badge_region = last_region
                    badge_scaled = True

        sphere_count = num

    for item in range(1, len(inventory)):
        if item in inventory:
            inventory[item] = inventory[item - 1] + inventory[item]
        else:
            inventory[item] = inventory[item - 1]

    for i in range(sphere_count):
        # Ness's mind needs to be calculated last, always. (Players are more likely to walk around
        # and explore areas than suddenly leave with a teleport)
        # Shuffle it to the end of the list on each loop so it gets deprioritized
        # Is there a better way to do this?
        if "Ness's Mind" in unconnected_regions:
            unconnected_regions.remove("Ness's Mind")
            unconnected_regions.append("Ness's Mind")  # probably do this differently earlier
        for region in unconnected_regions:
            for connection in world.area_exits[region]:
                if f"{region} -> {connection}" not in passed_connections:
                    for rule_set in world.area_rules[region][connection]:
                        # check if this sphere has the items needed to make this connection
                        if all(item in inventory[i] for item in rule_set):
                            passed_connections.append(f"{region} -> {connection}")
                            if connection not in world.accessible_regions:
                                world.accessible_regions.append(connection)
                                unconnected_regions.append(connection)
                else:
                    world.area_exits[region].remove(connection)
        if "Endgame" in unconnected_regions:
            unconnected_regions.remove("Endgame")
            unconnected_regions.insert(0, "Endgame")

    for region in world.multiworld.get_regions(world.player):
        if region.name not in world.accessible_regions and region.name != "Menu":
            world.accessible_regions.append(region.name)

    if world.options.magicant_mode == MagicantMode.option_alternate_goal and world.options.giygas_required:
        # If magicant is an alternate goal it should be scaled after Giygas
        world.accessible_regions.remove("Magicant")
        world.accessible_regions.append("Sea of Eden")
        world.accessible_regions.insert(world.accessible_regions.index("Endgame") + 1, "Magicant")
    elif world.options.magicant_mode == MagicantMode.option_optional_boost and world.options.giygas_required:
        world.accessible_regions.insert(world.accessible_regions.index("Endgame") - 1, "Magicant")
    elif world.options.magicant_mode == MagicantMode.option_optional_boost and not world.options.giygas_required:
        # Just add it to the end of scaling
        world.accessible_regions.append("Magicant")
        world.accessible_regions.append("Sea of Eden")

    # calculate which areas need to have enemies scaled
    for region in world.accessible_regions:
        if region in world.regional_enemies:
            world.scaled_area_order.append(region)

    current_level = 1
    world.area_levels = {}
    for region in world.accessible_regions:
        world.area_levels[region] = current_level
        current_level += expected_level_gains[region]

    if world.Ness_region == "Ness's Mind":
        world.Ness_region = world.scaled_area_order[0]

    if world.Paula_region == "Ness's Mind":
        world.Paula_region = world.scaled_area_order[0]

    if world.Jeff_region == "Ness's Mind":
        world.Jeff_region = world.scaled_area_order[0]

    if world.Poo_region == "Ness's Mind":
        world.Poo_region = world.scaled_area_order[0]

    if world.Badge_region == "Ness's Mind":
        world.Badge_region = world.scaled_area_order[0]
