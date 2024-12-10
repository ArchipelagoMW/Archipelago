from BaseClasses import Region, Entrance, ItemClassification, Location, LocationProgressType
from .Types import ChapterIndex, Difficulty, HatInTimeLocation, HatInTimeItem
from .Locations import location_table, storybook_pages, event_locs, is_location_valid, \
    shop_locations, TASKSANITY_START_ID, snatcher_coins, zero_jumps, zero_jumps_expert, zero_jumps_hard
from typing import TYPE_CHECKING, List, Dict, Optional
from .Rules import set_rift_rules, get_difficulty
from .Options import ActRandomizer, EndGoal

if TYPE_CHECKING:
    from . import HatInTimeWorld


MIN_FIRST_SPHERE_LOCATIONS = 30


# ChapterIndex: region
chapter_regions = {
    ChapterIndex.SPACESHIP: "Spaceship",
    ChapterIndex.MAFIA: "Mafia Town",
    ChapterIndex.BIRDS: "Battle of the Birds",
    ChapterIndex.SUBCON: "Subcon Forest",
    ChapterIndex.ALPINE: "Alpine Skyline",
    ChapterIndex.FINALE: "Time's End",
    ChapterIndex.CRUISE: "The Arctic Cruise",
    ChapterIndex.METRO: "Nyakuza Metro",
}

# entrance: region
act_entrances = {
    "Welcome to Mafia Town":          "Mafia Town - Act 1",
    "Barrel Battle":                  "Mafia Town - Act 2",
    "She Came from Outer Space":      "Mafia Town - Act 3",
    "Down with the Mafia!":           "Mafia Town - Act 4",
    "Cheating the Race":              "Mafia Town - Act 5",
    "Heating Up Mafia Town":          "Mafia Town - Act 6",
    "The Golden Vault":               "Mafia Town - Act 7",

    "Dead Bird Studio":               "Battle of the Birds - Act 1",
    "Murder on the Owl Express":      "Battle of the Birds - Act 2",
    "Picture Perfect":                "Battle of the Birds - Act 3",
    "Train Rush":                     "Battle of the Birds - Act 4",
    "The Big Parade":                 "Battle of the Birds - Act 5",
    "Award Ceremony":                 "Battle of the Birds - Finale A",
    "Dead Bird Studio Basement":      "Battle of the Birds - Finale B",

    "Contractual Obligations":        "Subcon Forest - Act 1",
    "The Subcon Well":                "Subcon Forest - Act 2",
    "Toilet of Doom":                 "Subcon Forest - Act 3",
    "Queen Vanessa's Manor":          "Subcon Forest - Act 4",
    "Mail Delivery Service":          "Subcon Forest - Act 5",
    "Your Contract has Expired":      "Subcon Forest - Finale",

    "Alpine Free Roam":               "Alpine Skyline - Free Roam",
    "The Illness has Spread":         "Alpine Skyline - Finale",

    "The Finale":                     "Time's End - Act 1",

    "Bon Voyage!":                    "The Arctic Cruise - Act 1",
    "Ship Shape":                     "The Arctic Cruise - Act 2",
    "Rock the Boat":                  "The Arctic Cruise - Finale",

    "Nyakuza Free Roam":              "Nyakuza Metro - Free Roam",
    "Rush Hour":                      "Nyakuza Metro - Finale",
}

act_chapters = {
    "Time Rift - Gallery":          "Spaceship",
    "Time Rift - The Lab":          "Spaceship",

    "Welcome to Mafia Town":        "Mafia Town",
    "Barrel Battle":                "Mafia Town",
    "She Came from Outer Space":    "Mafia Town",
    "Down with the Mafia!":         "Mafia Town",
    "Cheating the Race":            "Mafia Town",
    "Heating Up Mafia Town":        "Mafia Town",
    "The Golden Vault":             "Mafia Town",
    "Time Rift - Mafia of Cooks":   "Mafia Town",
    "Time Rift - Sewers":           "Mafia Town",
    "Time Rift - Bazaar":           "Mafia Town",

    "Dead Bird Studio":             "Battle of the Birds",
    "Murder on the Owl Express":    "Battle of the Birds",
    "Picture Perfect":              "Battle of the Birds",
    "Train Rush":                   "Battle of the Birds",
    "The Big Parade":               "Battle of the Birds",
    "Award Ceremony":               "Battle of the Birds",
    "Dead Bird Studio Basement":    "Battle of the Birds",
    "Time Rift - Dead Bird Studio": "Battle of the Birds",
    "Time Rift - The Owl Express":  "Battle of the Birds",
    "Time Rift - The Moon":         "Battle of the Birds",

    "Contractual Obligations":      "Subcon Forest",
    "The Subcon Well":              "Subcon Forest",
    "Toilet of Doom":               "Subcon Forest",
    "Queen Vanessa's Manor":        "Subcon Forest",
    "Mail Delivery Service":        "Subcon Forest",
    "Your Contract has Expired":    "Subcon Forest",
    "Time Rift - Sleepy Subcon":    "Subcon Forest",
    "Time Rift - Pipe":             "Subcon Forest",
    "Time Rift - Village":          "Subcon Forest",

    "Alpine Free Roam":                 "Alpine Skyline",
    "The Illness has Spread":           "Alpine Skyline",
    "Time Rift - Alpine Skyline":       "Alpine Skyline",
    "Time Rift - The Twilight Bell":    "Alpine Skyline",
    "Time Rift - Curly Tail Trail":     "Alpine Skyline",

    "The Finale":                       "Time's End",
    "Time Rift - Tour":                 "Time's End",

    "Bon Voyage!":                      "The Arctic Cruise",
    "Ship Shape":                       "The Arctic Cruise",
    "Rock the Boat":                    "The Arctic Cruise",
    "Time Rift - Balcony":              "The Arctic Cruise",
    "Time Rift - Deep Sea":             "The Arctic Cruise",

    "Nyakuza Free Roam":                "Nyakuza Metro",
    "Rush Hour":                        "Nyakuza Metro",
    "Time Rift - Rumbi Factory":        "Nyakuza Metro",
}

# region: list[Region]
rift_access_regions = {
    "Time Rift - Gallery":        ["Spaceship"],
    "Time Rift - The Lab":        ["Spaceship"],

    "Time Rift - Sewers":         ["Welcome to Mafia Town", "Barrel Battle", "She Came from Outer Space",
                                   "Down with the Mafia!", "Cheating the Race", "Heating Up Mafia Town",
                                   "The Golden Vault"],

    "Time Rift - Bazaar":         ["Welcome to Mafia Town", "Barrel Battle", "She Came from Outer Space",
                                   "Down with the Mafia!", "Cheating the Race", "Heating Up Mafia Town",
                                   "The Golden Vault"],

    "Time Rift - Mafia of Cooks": ["Welcome to Mafia Town", "Barrel Battle", "She Came from Outer Space",
                                   "Down with the Mafia!", "Cheating the Race", "The Golden Vault"],

    "Time Rift - The Owl Express":      ["Murder on the Owl Express"],
    "Time Rift - The Moon":             ["Picture Perfect", "The Big Parade"],
    "Time Rift - Dead Bird Studio":     ["Dead Bird Studio", "Dead Bird Studio Basement"],

    "Time Rift - Pipe":          ["Contractual Obligations", "The Subcon Well",
                                  "Toilet of Doom", "Queen Vanessa's Manor",
                                  "Mail Delivery Service"],

    "Time Rift - Village":       ["Contractual Obligations", "The Subcon Well",
                                  "Toilet of Doom", "Queen Vanessa's Manor",
                                  "Mail Delivery Service"],

    "Time Rift - Sleepy Subcon": ["Contractual Obligations", "The Subcon Well",
                                  "Toilet of Doom", "Queen Vanessa's Manor",
                                  "Mail Delivery Service"],

    "Time Rift - The Twilight Bell": ["Alpine Free Roam"],
    "Time Rift - Curly Tail Trail":  ["Alpine Free Roam"],
    "Time Rift - Alpine Skyline":    ["Alpine Free Roam", "The Illness has Spread"],

    "Time Rift - Tour":           ["Time's End"],

    "Time Rift - Balcony":       ["Cruise Ship"],
    "Time Rift - Deep Sea":      ["Bon Voyage!"],

    "Time Rift - Rumbi Factory": ["Nyakuza Free Roam"],
}

# Time piece identifiers to be used in act shuffle
chapter_act_info = {
    "Time Rift - Gallery":          "Spaceship_WaterRift_Gallery",
    "Time Rift - The Lab":          "Spaceship_WaterRift_MailRoom",

    "Welcome to Mafia Town":        "chapter1_tutorial",
    "Barrel Battle":                "chapter1_barrelboss",
    "She Came from Outer Space":    "chapter1_cannon_repair",
    "Down with the Mafia!":         "chapter1_boss",
    "Cheating the Race":            "harbor_impossible_race",
    "Heating Up Mafia Town":        "mafiatown_lava",
    "The Golden Vault":             "mafiatown_goldenvault",
    "Time Rift - Mafia of Cooks":   "TimeRift_Cave_Mafia",
    "Time Rift - Sewers":           "TimeRift_Water_Mafia_Easy",
    "Time Rift - Bazaar":           "TimeRift_Water_Mafia_Hard",

    "Dead Bird Studio":             "DeadBirdStudio",
    "Murder on the Owl Express":    "chapter3_murder",
    "Picture Perfect":              "moon_camerasnap",
    "Train Rush":                   "trainwreck_selfdestruct",
    "The Big Parade":               "moon_parade",
    "Award Ceremony":               "award_ceremony",
    "Dead Bird Studio Basement":    "chapter3_secret_finale",
    "Time Rift - Dead Bird Studio": "TimeRift_Cave_BirdBasement",
    "Time Rift - The Owl Express":  "TimeRift_Water_TWreck_Panels",
    "Time Rift - The Moon":         "TimeRift_Water_TWreck_Parade",

    "Contractual Obligations":      "subcon_village_icewall",
    "The Subcon Well":              "subcon_cave",
    "Toilet of Doom":               "chapter2_toiletboss",
    "Queen Vanessa's Manor":        "vanessa_manor_attic",
    "Mail Delivery Service":        "subcon_maildelivery",
    "Your Contract has Expired":    "snatcher_boss",
    "Time Rift - Sleepy Subcon":    "TimeRift_Cave_Raccoon",
    "Time Rift - Pipe":             "TimeRift_Water_Subcon_Hookshot",
    "Time Rift - Village":          "TimeRift_Water_Subcon_Dwellers",

    "Alpine Free Roam":                 "AlpineFreeRoam",  # not an actual Time Piece
    "The Illness has Spread":           "AlpineSkyline_Finale",
    "Time Rift - Alpine Skyline":       "TimeRift_Cave_Alps",
    "Time Rift - The Twilight Bell":    "TimeRift_Water_Alp_Goats",
    "Time Rift - Curly Tail Trail":     "TimeRift_Water_AlpineSkyline_Cats",

    "The Finale":                       "TheFinale_FinalBoss",
    "Time Rift - Tour":                 "TimeRift_Cave_Tour",

    "Bon Voyage!":                 "Cruise_Boarding",
    "Ship Shape":                  "Cruise_Working",
    "Rock the Boat":               "Cruise_Sinking",
    "Time Rift - Balcony":         "Cruise_WaterRift_Slide",
    "Time Rift - Deep Sea":        "Cruise_CaveRift_Aquarium",

    "Nyakuza Free Roam":            "MetroFreeRoam",  # not an actual Time Piece
    "Rush Hour":                    "Metro_Escape",
    "Time Rift - Rumbi Factory":    "Metro_CaveRift_RumbiFactory"
}

# Some of these may vary depending on options. See is_valid_first_act()
guaranteed_first_acts = [
    "Welcome to Mafia Town",
    "Barrel Battle",
    "She Came from Outer Space",
    "Down with the Mafia!",
    "Heating Up Mafia Town",
    "The Golden Vault",

    "Dead Bird Studio",
    "Murder on the Owl Express",
    "Dead Bird Studio Basement",

    "Contractual Obligations",
    "The Subcon Well",
    "Queen Vanessa's Manor",
    "Your Contract has Expired",

    "Rock the Boat",

    "Time Rift - Mafia of Cooks",
    "Time Rift - Dead Bird Studio",
    "Time Rift - Sleepy Subcon",
    "Time Rift - Alpine Skyline"
    "Time Rift - Tour",
    "Time Rift - Rumbi Factory",
]

purple_time_rifts = [
    "Time Rift - Mafia of Cooks",
    "Time Rift - Dead Bird Studio",
    "Time Rift - Sleepy Subcon",
    "Time Rift - Alpine Skyline",
    "Time Rift - Deep Sea",
    "Time Rift - Tour",
    "Time Rift - Rumbi Factory",
]

chapter_finales = [
    "Dead Bird Studio Basement",
    "Your Contract has Expired",
    "The Illness has Spread",
    "Rock the Boat",
    "Rush Hour",
]

# Acts blacklisted in act shuffle
# entrance: region
blacklisted_acts = {
    "Battle of the Birds - Finale A":   "Award Ceremony",
}

# Blacklisted act shuffle combinations to help prevent impossible layouts. Mostly for free roam acts.
blacklisted_combos = {
    "The Illness has Spread":           ["Nyakuza Free Roam", "Alpine Free Roam", "Contractual Obligations"],
    "Rush Hour":                        ["Nyakuza Free Roam", "Alpine Free Roam", "Contractual Obligations"],

    # Bon Voyage is here to prevent the cycle: Owl Express -> Bon Voyage -> Deep Sea -> MOTOE -> Owl Express
    # which would make them all inaccessible since those rifts have no other entrances
    "Time Rift - The Owl Express":      ["Alpine Free Roam", "Nyakuza Free Roam", "Bon Voyage!",
                                         "Contractual Obligations"],

    "Time Rift - The Moon":             ["Alpine Free Roam", "Nyakuza Free Roam", "Contractual Obligations"],
    "Time Rift - Dead Bird Studio":     ["Alpine Free Roam", "Nyakuza Free Roam", "Contractual Obligations"],
    "Time Rift - Curly Tail Trail":     ["Nyakuza Free Roam", "Contractual Obligations"],
    "Time Rift - The Twilight Bell":    ["Nyakuza Free Roam", "Contractual Obligations"],
    "Time Rift - Alpine Skyline":       ["Nyakuza Free Roam", "Contractual Obligations"],
    "Time Rift - Rumbi Factory":        ["Alpine Free Roam", "Contractual Obligations"],

    # See above comment
    "Time Rift - Deep Sea":             ["Alpine Free Roam", "Nyakuza Free Roam", "Contractual Obligations",
                                         "Murder on the Owl Express"],

    # was causing test failures
    "Time Rift - Balcony":              ["Alpine Free Roam"],
}


def create_regions(world: "HatInTimeWorld"):
    # ------------------------------------------- HUB -------------------------------------------------- #
    menu = create_region(world, "Menu")
    spaceship = create_region_and_connect(world, "Spaceship", "Save File -> Spaceship", menu)

    # we only need the menu and the spaceship regions
    if world.is_dw_only():
        return

    create_rift_connections(world, create_region(world, "Time Rift - Gallery"))
    create_rift_connections(world, create_region(world, "Time Rift - The Lab"))

    # ------------------------------------------- MAFIA TOWN ------------------------------------------- #
    mafia_town = create_region_and_connect(world, "Mafia Town", "Telescope -> Mafia Town", spaceship)
    mt_act1 = create_region_and_connect(world, "Welcome to Mafia Town", "Mafia Town - Act 1", mafia_town)
    mt_act2 = create_region_and_connect(world, "Barrel Battle", "Mafia Town - Act 2", mafia_town)
    mt_act3 = create_region_and_connect(world, "She Came from Outer Space", "Mafia Town - Act 3", mafia_town)
    mt_act4 = create_region_and_connect(world, "Down with the Mafia!", "Mafia Town - Act 4", mafia_town)
    mt_act6 = create_region_and_connect(world, "Heating Up Mafia Town", "Mafia Town - Act 6", mafia_town)
    mt_act5 = create_region_and_connect(world, "Cheating the Race", "Mafia Town - Act 5", mafia_town)
    mt_act7 = create_region_and_connect(world, "The Golden Vault", "Mafia Town - Act 7", mafia_town)

    # ------------------------------------------- BOTB ------------------------------------------------- #
    botb = create_region_and_connect(world, "Battle of the Birds", "Telescope -> Battle of the Birds", spaceship)
    dbs = create_region_and_connect(world, "Dead Bird Studio", "Battle of the Birds - Act 1", botb)
    create_region_and_connect(world, "Murder on the Owl Express", "Battle of the Birds - Act 2", botb)
    pp = create_region_and_connect(world, "Picture Perfect", "Battle of the Birds - Act 3", botb)
    tr = create_region_and_connect(world, "Train Rush", "Battle of the Birds - Act 4", botb)
    create_region_and_connect(world, "The Big Parade", "Battle of the Birds - Act 5", botb)
    create_region_and_connect(world, "Award Ceremony", "Battle of the Birds - Finale A", botb)
    basement = create_region_and_connect(world, "Dead Bird Studio Basement", "Battle of the Birds - Finale B", botb)
    create_rift_connections(world, create_region(world, "Time Rift - Dead Bird Studio"))
    create_rift_connections(world, create_region(world, "Time Rift - The Owl Express"))
    create_rift_connections(world, create_region(world, "Time Rift - The Moon"))

    # Items near the Dead Bird Studio elevator can be reached from the basement act, and beyond in Expert
    ev_area = create_region_and_connect(world, "Dead Bird Studio - Elevator Area", "DBS -> Elevator Area", dbs)
    post_ev = create_region_and_connect(world, "Dead Bird Studio - Post Elevator Area", "DBS -> Post Elevator Area", dbs)
    basement.connect(ev_area, "DBS Basement -> Elevator Area")
    if world.options.LogicDifficulty >= int(Difficulty.EXPERT):
        basement.connect(post_ev, "DBS Basement -> Post Elevator Area")

    # ------------------------------------------- SUBCON FOREST --------------------------------------- #
    subcon_forest = create_region_and_connect(world, "Subcon Forest", "Telescope -> Subcon Forest", spaceship)
    sf_act1 = create_region_and_connect(world, "Contractual Obligations", "Subcon Forest - Act 1", subcon_forest)
    sf_act2 = create_region_and_connect(world, "The Subcon Well", "Subcon Forest - Act 2", subcon_forest)
    sf_act3 = create_region_and_connect(world, "Toilet of Doom", "Subcon Forest - Act 3", subcon_forest)
    sf_act4 = create_region_and_connect(world, "Queen Vanessa's Manor", "Subcon Forest - Act 4", subcon_forest)
    sf_act5 = create_region_and_connect(world, "Mail Delivery Service", "Subcon Forest - Act 5", subcon_forest)
    create_region_and_connect(world, "Your Contract has Expired", "Subcon Forest - Finale", subcon_forest)

    # ------------------------------------------- ALPINE SKYLINE ------------------------------------------ #
    alpine_skyline = create_region_and_connect(world, "Alpine Skyline",  "Telescope -> Alpine Skyline", spaceship)
    alpine_freeroam = create_region_and_connect(world, "Alpine Free Roam", "Alpine Skyline - Free Roam", alpine_skyline)
    alpine_area = create_region_and_connect(world, "Alpine Skyline Area", "AFR -> Alpine Skyline Area", alpine_freeroam)

    # Needs to be separate because there are a lot of locations in Alpine that can't be accessed from Illness
    alpine_area_tihs = create_region_and_connect(world, "Alpine Skyline Area (TIHS)", "-> Alpine Skyline Area (TIHS)",
                                                 alpine_area)

    create_region_and_connect(world, "The Birdhouse", "-> The Birdhouse", alpine_area)
    create_region_and_connect(world, "The Lava Cake", "-> The Lava Cake", alpine_area)
    create_region_and_connect(world, "The Windmill", "-> The Windmill", alpine_area)
    create_region_and_connect(world, "The Twilight Bell", "-> The Twilight Bell", alpine_area)

    illness = create_region_and_connect(world, "The Illness has Spread", "Alpine Skyline - Finale", alpine_skyline)
    illness.connect(alpine_area_tihs, "TIHS -> Alpine Skyline Area (TIHS)")
    create_rift_connections(world, create_region(world, "Time Rift - Alpine Skyline"))
    create_rift_connections(world, create_region(world, "Time Rift - The Twilight Bell"))
    create_rift_connections(world, create_region(world, "Time Rift - Curly Tail Trail"))

    # ------------------------------------------- OTHER -------------------------------------------------- #
    mt_area: Region = create_region(world, "Mafia Town Area")
    mt_area_humt: Region = create_region(world, "Mafia Town Area (HUMT)")
    mt_area.connect(mt_area_humt, "MT Area -> MT Area (HUMT)")
    mt_act1.connect(mt_area, "Mafia Town Entrance WTMT")
    mt_act2.connect(mt_area, "Mafia Town Entrance BB")
    mt_act3.connect(mt_area, "Mafia Town Entrance SCFOS")
    mt_act4.connect(mt_area, "Mafia Town Entrance DWTM")
    mt_act5.connect(mt_area, "Mafia Town Entrance CTR")
    mt_act6.connect(mt_area_humt, "Mafia Town Entrance HUMT")
    mt_act7.connect(mt_area, "Mafia Town Entrance TGV")

    create_rift_connections(world, create_region(world, "Time Rift - Mafia of Cooks"))
    create_rift_connections(world, create_region(world, "Time Rift - Sewers"))
    create_rift_connections(world, create_region(world, "Time Rift - Bazaar"))

    sf_area: Region = create_region(world, "Subcon Forest Area")
    sf_act1.connect(sf_area, "Subcon Forest Entrance CO")
    sf_act2.connect(sf_area, "Subcon Forest Entrance SW")
    sf_act3.connect(sf_area, "Subcon Forest Entrance TOD")
    sf_act4.connect(sf_area, "Subcon Forest Entrance QVM")
    sf_act5.connect(sf_area, "Subcon Forest Entrance MDS")

    create_rift_connections(world, create_region(world, "Time Rift - Sleepy Subcon"))
    create_rift_connections(world, create_region(world, "Time Rift - Pipe"))
    create_rift_connections(world, create_region(world, "Time Rift - Village"))

    badge_seller = create_badge_seller(world)
    mt_area.connect(badge_seller, "MT Area -> Badge Seller")
    mt_area_humt.connect(badge_seller, "MT Area (HUMT) -> Badge Seller")
    sf_area.connect(badge_seller, "SF Area -> Badge Seller")
    dbs.connect(badge_seller, "DBS -> Badge Seller")
    pp.connect(badge_seller, "PP -> Badge Seller")
    tr.connect(badge_seller, "TR -> Badge Seller")
    alpine_area_tihs.connect(badge_seller, "ASA -> Badge Seller")

    times_end = create_region_and_connect(world, "Time's End", "Telescope -> Time's End", spaceship)
    create_region_and_connect(world, "The Finale", "Time's End - Act 1", times_end)

    # ------------------------------------------- DLC1 ------------------------------------------------- #
    if world.is_dlc1():
        arctic_cruise = create_region_and_connect(world, "The Arctic Cruise", "Telescope -> Arctic Cruise", spaceship)
        cruise_ship = create_region(world, "Cruise Ship")

        ac_act1 = create_region_and_connect(world, "Bon Voyage!", "The Arctic Cruise - Act 1", arctic_cruise)
        ac_act2 = create_region_and_connect(world, "Ship Shape", "The Arctic Cruise - Act 2", arctic_cruise)
        ac_act3 = create_region_and_connect(world, "Rock the Boat", "The Arctic Cruise - Finale", arctic_cruise)

        ac_act1.connect(cruise_ship, "Cruise Ship Entrance BV")
        ac_act2.connect(cruise_ship, "Cruise Ship Entrance SS")
        ac_act3.connect(cruise_ship, "Cruise Ship Entrance RTB")
        create_rift_connections(world, create_region(world, "Time Rift - Balcony"))
        create_rift_connections(world, create_region(world, "Time Rift - Deep Sea"))

        if not world.options.ExcludeTour:
            create_rift_connections(world, create_region(world, "Time Rift - Tour"))

        if world.options.Tasksanity:
            create_tasksanity_locations(world)

        cruise_ship.connect(badge_seller, "CS -> Badge Seller")

    if world.is_dlc2():
        nyakuza = create_region_and_connect(world, "Nyakuza Metro", "Telescope -> Nyakuza Metro", spaceship)
        metro_freeroam = create_region_and_connect(world, "Nyakuza Free Roam", "Nyakuza Metro - Free Roam", nyakuza)
        create_region_and_connect(world, "Rush Hour", "Nyakuza Metro - Finale", nyakuza)

        yellow = create_region_and_connect(world, "Yellow Overpass Station", "-> Yellow Overpass Station", metro_freeroam)
        green = create_region_and_connect(world, "Green Clean Station", "-> Green Clean Station", metro_freeroam)
        pink = create_region_and_connect(world, "Pink Paw Station", "-> Pink Paw Station", metro_freeroam)
        create_region_and_connect(world, "Bluefin Tunnel", "-> Bluefin Tunnel", metro_freeroam)  # No manhole

        create_region_and_connect(world, "Yellow Overpass Manhole", "-> Yellow Overpass Manhole", yellow)
        create_region_and_connect(world, "Green Clean Manhole", "-> Green Clean Manhole", green)
        create_region_and_connect(world, "Pink Paw Manhole", "-> Pink Paw Manhole", pink)

        create_rift_connections(world, create_region(world, "Time Rift - Rumbi Factory"))
        create_thug_shops(world)


def create_rift_connections(world: "HatInTimeWorld", region: Region):
    for i, name in enumerate(rift_access_regions[region.name]):
        act_region = world.multiworld.get_region(name, world.player)
        entrance_name = f"{region.name} Portal - Entrance {i+1}"
        act_region.connect(region, entrance_name)


def create_tasksanity_locations(world: "HatInTimeWorld"):
    ship_shape: Region = world.multiworld.get_region("Ship Shape", world.player)
    id_start: int = TASKSANITY_START_ID
    for i in range(world.options.TasksanityCheckCount):
        location = HatInTimeLocation(world.player, f"Tasksanity Check {i+1}", id_start+i, ship_shape)
        ship_shape.locations.append(location)


def randomize_act_entrances(world: "HatInTimeWorld"):
    region_list: List[Region] = get_shuffleable_act_regions(world)
    world.random.shuffle(region_list)
    region_list.sort(key=sort_acts)
    candidate_list: List[Region] = region_list.copy()
    rift_dict: Dict[str, Region] = {}

    # Check if Plando's are valid, if so, map them
    if world.options.ActPlando:
        player_name = world.multiworld.get_player_name(world.player)
        for (name1, name2) in world.options.ActPlando.items():
            region: Region
            act: Region
            try:
                region = world.multiworld.get_region(name1, world.player)
            except KeyError:
                print(f"ActPlando ({player_name}) - "
                      f"Act \"{name1}\" does not exist in the multiworld. "
                      f"Possible reasons are typos, case-sensitivity, or DLC options.")
                continue

            try:
                act = world.multiworld.get_region(name2, world.player)
            except KeyError:
                print(f"ActPlando ({player_name}) - "
                      f"Act \"{name2}\" does not exist in the multiworld. "
                      f"Possible reasons are typos, case-sensitivity, or DLC options.")
                continue

            if is_valid_plando(world, region.name, act.name):
                region_list.remove(region)
                candidate_list.remove(act)
                connect_acts(world, region, act, rift_dict)
            else:
                print(f"ActPlando "
                      f"({player_name}) - "
                      f"\"{name1}: {name2}\" "
                      f"is an invalid or disallowed act plando combination!")

    # Decide what should be on the first few levels before randomizing the rest
    first_acts: List[Region] = []
    first_chapter_name = chapter_regions[ChapterIndex(world.options.StartingChapter)]
    first_acts.append(get_act_by_number(world, first_chapter_name, 1))
    # Chapter 3 and 4 only have one level accessible at the start
    if first_chapter_name == "Mafia Town" or first_chapter_name == "Battle of the Birds":
        first_acts.append(get_act_by_number(world, first_chapter_name, 2))
        first_acts.append(get_act_by_number(world, first_chapter_name, 3))

    valid_first_acts: List[Region] = []
    for candidate in candidate_list:
        if is_valid_first_act(world, candidate):
            valid_first_acts.append(candidate)

    total_locations = 0
    for level in first_acts:
        if level not in region_list:  # make sure it hasn't been plando'd
            continue

        candidate = valid_first_acts[world.random.randint(0, len(valid_first_acts)-1)]
        region_list.remove(level)
        candidate_list.remove(candidate)
        valid_first_acts.remove(candidate)
        connect_acts(world, level, candidate, rift_dict)

        # Only allow one purple rift
        if candidate.name in purple_time_rifts:
            for act in reversed(valid_first_acts):
                if act.name in purple_time_rifts:
                    valid_first_acts.remove(act)

        total_locations += get_region_location_count(world, candidate.name)
        if "Time Rift" not in candidate.name:
            chapter = act_chapters.get(candidate.name)
            if chapter == "Mafia Town":
                total_locations += get_region_location_count(world, "Mafia Town Area (HUMT)")
                if candidate.name != "Heating Up Mafia Town":
                    total_locations += get_region_location_count(world, "Mafia Town Area")
            elif chapter == "Subcon Forest":
                total_locations += get_region_location_count(world, "Subcon Forest Area")
            elif chapter == "The Arctic Cruise":
                total_locations += get_region_location_count(world, "Cruise Ship")

        # If we have enough Sphere 1 locations, we can allow the rest to be randomized
        if total_locations >= MIN_FIRST_SPHERE_LOCATIONS:
            break

    ignore_certain_rules: bool = False
    while len(region_list) > 0:
        region = region_list[0]
        candidate: Region
        valid_candidates: List[Region] = []

        # Look for candidates to map this act to
        for c in candidate_list:
            if is_valid_act_combo(world, region, c, ignore_certain_rules):
                valid_candidates.append(c)

        if len(valid_candidates) > 0:
            candidate = valid_candidates[world.random.randint(0, len(valid_candidates)-1)]
        else:
            # If we fail here, try again with less shuffle rules. If we still somehow fail, there's an issue for sure
            if ignore_certain_rules:
                raise Exception(f"Failed to find act shuffle candidate for {region}"
                                f"\nRemaining acts to map to: {region_list}"
                                f"\nRemaining candidates: {candidate_list}")

            ignore_certain_rules = True
            continue

        ignore_certain_rules = False
        region_list.remove(region)
        candidate_list.remove(candidate)
        connect_acts(world, region, candidate, rift_dict)

    for name in blacklisted_acts.values():
        region: Region = world.multiworld.get_region(name, world.player)
        update_chapter_act_info(world, region, region)

    set_rift_rules(world, rift_dict)


# Try to do levels that may have specific mapping rules first
def sort_acts(act: Region) -> int:
    if "Time Rift" in act.name:
        return -5

    if act.name in chapter_finales:
        return -4

    # Free Roam
    if (act_chapters[act.name] == "Alpine Skyline" or act_chapters[act.name] == "Nyakuza Metro") \
       and "Time Rift" not in act.name:
        return -3

    if act.name == "Contractual Obligations" or act.name == "The Subcon Well":
        return -2

    world = act.multiworld.worlds[act.player]
    blacklist = world.options.ActBlacklist
    if len(blacklist) > 0:
        for name, act_list in blacklist.items():
            if act.name == name or act.name in act_list:
                return -1

    return 0


def connect_acts(world: "HatInTimeWorld", entrance_act: Region, exit_act: Region, rift_dict: Dict[str, Region]):
    # Vanilla
    if exit_act.name == entrance_act.name:
        if entrance_act.name in rift_access_regions.keys():
            rift_dict.setdefault(entrance_act.name, exit_act)

        update_chapter_act_info(world, entrance_act, exit_act)
        return

    if entrance_act.name in rift_access_regions.keys():
        connect_time_rift(world, entrance_act, exit_act)
        rift_dict.setdefault(entrance_act.name, exit_act)
    else:
        if exit_act.name in rift_access_regions.keys():
            for e in exit_act.entrances.copy():
                e.parent_region.exits.remove(e)
                e.connected_region.entrances.remove(e)

        entrance = world.multiworld.get_entrance(act_entrances[entrance_act.name], world.player)
        chapter = world.multiworld.get_region(act_chapters[entrance_act.name], world.player)
        reconnect_regions(entrance, chapter, exit_act)

    update_chapter_act_info(world, entrance_act, exit_act)


def is_valid_act_combo(world: "HatInTimeWorld", entrance_act: Region,
                       exit_act: Region, ignore_certain_rules: bool = False) -> bool:

    # Ignore certain rules that aren't to prevent impossible combos. This is needed for ActPlando.
    if not ignore_certain_rules:
        if world.options.ActRandomizer == ActRandomizer.option_light and not ignore_certain_rules:
            # Don't map Time Rifts to normal acts
            if "Time Rift" in entrance_act.name and "Time Rift" not in exit_act.name:
                return False

            # Don't map normal acts to Time Rifts
            if "Time Rift" not in entrance_act.name and "Time Rift" in exit_act.name:
                return False

            # Separate purple rifts
            if entrance_act.name in purple_time_rifts and exit_act.name not in purple_time_rifts \
                    or entrance_act.name not in purple_time_rifts and exit_act.name in purple_time_rifts:
                return False

        if world.options.FinaleShuffle and entrance_act.name in chapter_finales:
            if exit_act.name not in chapter_finales:
                return False

    exit_chapter: str = act_chapters.get(exit_act.name)
    # make sure that certain time rift combinations never happen
    always_block: bool = exit_chapter != "Mafia Town" and exit_chapter != "Subcon Forest"
    if not ignore_certain_rules or always_block:
        if entrance_act.name in rift_access_regions and exit_act.name in rift_access_regions[entrance_act.name]:
            return False

    # Blacklisted?
    if entrance_act.name in blacklisted_combos.keys() and exit_act.name in blacklisted_combos[entrance_act.name]:
        return False

    if world.options.ActBlacklist:
        act_blacklist = world.options.ActBlacklist.get(entrance_act.name)
        if act_blacklist is not None and exit_act.name in act_blacklist:
            return False

    # Prevent Contractual Obligations from being inaccessible if contracts are not shuffled
    if not world.options.ShuffleActContracts:
        if (entrance_act.name == "Your Contract has Expired" or entrance_act.name == "The Subcon Well") \
           and exit_act.name == "Contractual Obligations":
            return False

    return True


def is_valid_first_act(world: "HatInTimeWorld", act: Region) -> bool:
    if act.name not in guaranteed_first_acts:
        return False

    if world.options.ActRandomizer == ActRandomizer.option_light and "Time Rift" in act.name:
        return False

    # If there's only a single level in the starting chapter, only allow Mafia Town or Subcon Forest levels
    start_chapter = world.options.StartingChapter
    if start_chapter == ChapterIndex.ALPINE or start_chapter == ChapterIndex.SUBCON:
        if "Time Rift" in act.name:
            return False

        if act_chapters[act.name] != "Mafia Town" and act_chapters[act.name] != "Subcon Forest":
            return False

    if act.name in purple_time_rifts and not world.options.ShuffleStorybookPages:
        return False

    diff = get_difficulty(world)
    # Not completable without Umbrella?
    if world.options.UmbrellaLogic:
        # Needs to be at least moderate to cross the big dweller wall
        if act.name == "Queen Vanessa's Manor" and diff < Difficulty.MODERATE:
            return False
        elif act.name == "Heating Up Mafia Town":  # Straight up impossible
            return False

    # Need to be able to hover
    if act.name == "Your Contract has Expired":
        if diff < Difficulty.EXPERT or world.options.ShuffleSubconPaintings and world.options.NoPaintingSkips:
            return False

    if act.name == "Dead Bird Studio":
        # No umbrella logic = moderate, umbrella logic = expert.
        if diff < Difficulty.MODERATE or world.options.UmbrellaLogic and diff < Difficulty.EXPERT:
            return False
    elif act.name == "Dead Bird Studio Basement" and (diff < Difficulty.EXPERT or world.options.FinaleShuffle):
        return False
    elif act.name == "Rock the Boat" and (diff < Difficulty.MODERATE or world.options.FinaleShuffle):
        return False
    elif act.name == "The Subcon Well" and diff < Difficulty.MODERATE:
        return False
    elif act.name == "Contractual Obligations" and world.options.ShuffleSubconPaintings:
        return False

    if world.options.ShuffleSubconPaintings and "Time Rift" not in act.name \
       and act_chapters.get(act.name, "") == "Subcon Forest":
        # Only allow Subcon levels if painting skips are allowed
        if diff < Difficulty.MODERATE or world.options.NoPaintingSkips:
            return False

    return True


def connect_time_rift(world: "HatInTimeWorld", time_rift: Region, exit_region: Region):
    for i, access_region in enumerate(rift_access_regions[time_rift.name], start=1):
        # Matches the naming convention and iteration order in `create_rift_connections()`.
        name = f"{time_rift.name} Portal - Entrance {i}"
        entrance: Entrance
        try:
            entrance = world.get_entrance(name)
            # Reconnect the rift access region to the new exit region.
            reconnect_regions(entrance, entrance.parent_region, exit_region)
        except KeyError:
            # The original entrance to the time rift has been deleted by already reconnecting a telescope act to the
            # time rift, so create a new entrance from the original rift access region to the new exit region.
            # Normally, acts and time rifts are sorted such that time rifts are reconnected to acts/rifts first, but
            # starting acts/rifts and act-plando can reconnect acts to time rifts before this happens.
            world.get_region(access_region).connect(exit_region, name)


def get_shuffleable_act_regions(world: "HatInTimeWorld") -> List[Region]:
    act_list: List[Region] = []
    for region in world.multiworld.get_regions(world.player):
        if region.name in chapter_act_info.keys():
            if not is_act_blacklisted(world, region.name):
                act_list.append(region)

    return act_list


def is_act_blacklisted(world: "HatInTimeWorld", name: str) -> bool:
    act_plando = world.options.ActPlando
    plando: bool = name in act_plando.keys() and is_valid_plando(world, name, act_plando[name])
    if not plando and name in act_plando.values():
        for key in act_plando.keys():
            if act_plando[key] == name and is_valid_plando(world, key, name):
                plando = True
                break

    if name == "The Finale":
        return not plando and world.options.EndGoal == EndGoal.option_finale

    if name == "Rush Hour":
        return not plando and world.options.EndGoal == EndGoal.option_rush_hour

    if name == "Time Rift - Tour":
        return bool(world.options.ExcludeTour)

    return name in blacklisted_acts.values()


def is_valid_plando(world: "HatInTimeWorld", region: str, act: str) -> bool:
    # Duplicated keys will throw an exception for us, but we still need to check for duplicated values
    found_count = 0
    for val in world.options.ActPlando.values():
        if val == act:
            found_count += 1

    if found_count > 1:
        raise Exception(f"ActPlando ({world.multiworld.get_player_name(world.player)}) - "
              f"Duplicated act plando mapping found for act: \"{act}\"")

    if region in blacklisted_acts.values() or (region not in act_entrances.keys() and "Time Rift" not in region):
        return False

    if act in blacklisted_acts.values() or (act not in act_entrances.keys() and "Time Rift" not in act):
        return False

    # Don't allow plando-ing things onto the first act that aren't permitted
    entrance_name = act_entrances.get(region, "")
    if entrance_name != "":
        is_first_act: bool = act_chapters.get(region) == get_first_chapter_region(world).name \
                             and ("Act 1" in entrance_name or "Free Roam" in entrance_name)

        if is_first_act and not is_valid_first_act(world, world.multiworld.get_region(act, world.player)):
            return False

    # Don't allow straight up impossible mappings
    if (region == "Time Rift - Curly Tail Trail"
       or region == "Time Rift - The Twilight Bell"
       or region == "The Illness has Spread") \
       and act == "Alpine Free Roam":
        return False

    if (region == "Rush Hour" or region == "Time Rift - Rumbi Factory") and act == "Nyakuza Free Roam":
        return False

    if region == "Time Rift - The Owl Express" and act == "Murder on the Owl Express":
        return False

    if region == "Time Rift - Deep Sea" and act == "Bon Voyage!":
        return False

    return any(a.name == world.options.ActPlando.get(region) for a in world.multiworld.get_regions(world.player))


def create_region(world: "HatInTimeWorld", name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    for (key, data) in location_table.items():
        if world.is_dw_only():
            break

        if data.nyakuza_thug != "":
            continue

        if data.region == name:
            if key in storybook_pages.keys() and not world.options.ShuffleStorybookPages:
                continue

            location = HatInTimeLocation(world.player, key, data.id, reg)
            reg.locations.append(location)
            if location.name in shop_locations:
                world.shop_locs.append(location.name)

    world.multiworld.regions.append(reg)
    return reg


def create_badge_seller(world: "HatInTimeWorld") -> Region:
    badge_seller = Region("Badge Seller", world.player, world.multiworld)
    world.multiworld.regions.append(badge_seller)
    count = 0
    max_items = 0

    if world.options.BadgeSellerMaxItems > 0:
        max_items = world.random.randint(world.options.BadgeSellerMinItems.value,
                                         world.options.BadgeSellerMaxItems.value)

    if max_items <= 0:
        world.badge_seller_count = 0
        return badge_seller

    for (key, data) in shop_locations.items():
        if "Badge Seller" not in key:
            continue

        location = HatInTimeLocation(world.player, key, data.id, badge_seller)
        badge_seller.locations.append(location)
        world.shop_locs.append(location.name)

        count += 1
        if count >= max_items:
            break

    world.badge_seller_count = max_items
    return badge_seller


# Takes an entrance, removes its old connections, and reconnects it between the two regions specified.
def reconnect_regions(entrance: Entrance, start_region: Region, exit_region: Region):
    if entrance in entrance.connected_region.entrances:
        entrance.connected_region.entrances.remove(entrance)

    if entrance in entrance.parent_region.exits:
        entrance.parent_region.exits.remove(entrance)

    if entrance in start_region.exits:
        start_region.exits.remove(entrance)

    if entrance in exit_region.entrances:
        exit_region.entrances.remove(entrance)

    entrance.parent_region = start_region
    start_region.exits.append(entrance)
    entrance.connect(exit_region)


def create_region_and_connect(world: "HatInTimeWorld",
                              name: str, entrancename: str, connected_region: Region, is_exit: bool = True) -> Region:

    reg: Region = create_region(world, name)
    entrance_region: Region
    exit_region: Region

    if is_exit:
        entrance_region = connected_region
        exit_region = reg
    else:
        entrance_region = reg
        exit_region = connected_region

    entrance_region.connect(exit_region, entrancename)
    return reg


def get_first_chapter_region(world: "HatInTimeWorld") -> Region:
    start_chapter: ChapterIndex = ChapterIndex(world.options.StartingChapter)
    return world.multiworld.get_region(chapter_regions.get(start_chapter), world.player)


def get_act_original_chapter(world: "HatInTimeWorld", act_name: str) -> Region:
    return world.multiworld.get_region(act_chapters[act_name], world.player)


# Sets an act entrance in slot data by specifying the Hat_ChapterActInfo, to be used in-game
def update_chapter_act_info(world: "HatInTimeWorld", original_region: Region, new_region: Region):
    original_act_info = chapter_act_info[original_region.name]
    new_act_info = chapter_act_info[new_region.name]
    world.act_connections[original_act_info] = new_act_info


def get_shuffled_region(world: "HatInTimeWorld", region: str) -> str:
    ci: str = chapter_act_info[region]
    for key, val in world.act_connections.items():
        if val == ci:
            for name in chapter_act_info.keys():
                if chapter_act_info[name] == key:
                    return name


def get_region_location_count(world: "HatInTimeWorld", region_name: str, included_only: bool = True) -> int:
    count = 0
    region = world.multiworld.get_region(region_name, world.player)
    for loc in region.locations:
        if loc.address is not None and (not included_only or loc.progress_type is not LocationProgressType.EXCLUDED):
            count += 1

    return count


def get_act_by_number(world: "HatInTimeWorld", chapter_name: str, num: int) -> Region:
    chapter = world.multiworld.get_region(chapter_name, world.player)
    act: Optional[Region] = None
    for e in chapter.exits:
        if f"Act {num}" in e.name or num == 1 and "Free Roam" in e.name:
            act = e.connected_region
            break

    return act


def create_thug_shops(world: "HatInTimeWorld"):
    min_items: int = world.options.NyakuzaThugMinShopItems.value
    max_items: int = world.options.NyakuzaThugMaxShopItems.value

    thug_location_counts: Dict[str, int] = {}

    for key, data in shop_locations.items():
        thug_name = data.nyakuza_thug
        if thug_name == "":
            # Different shop type.
            continue

        if thug_name not in world.nyakuza_thug_items:
            shop_item_count = world.random.randint(min_items, max_items)
            world.nyakuza_thug_items[thug_name] = shop_item_count
        else:
            shop_item_count = world.nyakuza_thug_items[thug_name]

        if shop_item_count <= 0:
            continue

        location_count = thug_location_counts.setdefault(thug_name, 0)
        if location_count >= shop_item_count:
            # Already created all the locations for this thug.
            continue

        # Create the shop location.
        region = world.multiworld.get_region(data.region, world.player)
        loc = HatInTimeLocation(world.player, key, data.id, region)
        region.locations.append(loc)
        world.shop_locs.append(loc.name)
        thug_location_counts[thug_name] = location_count + 1


def create_events(world: "HatInTimeWorld") -> int:
    count = 0

    for (name, data) in event_locs.items():
        if not is_location_valid(world, name):
            continue

        item_name: str = name
        if world.is_dw():
            if name in snatcher_coins.keys():
                item_name = data.snatcher_coin
            elif name in zero_jumps:
                if get_difficulty(world) < Difficulty.HARD and name in zero_jumps_hard:
                    continue

                if get_difficulty(world) < Difficulty.EXPERT and name in zero_jumps_expert:
                    continue

        event: Location = create_event(name, item_name, world.multiworld.get_region(data.region, world.player), world)
        event.show_in_spoiler = False
        count += 1

    return count


def create_event(name: str, item_name: str, region: Region, world: "HatInTimeWorld") -> Location:
    event = HatInTimeLocation(world.player, name, None, region)
    region.locations.append(event)
    event.place_locked_item(HatInTimeItem(item_name, ItemClassification.progression, None, world.player))
    return event
