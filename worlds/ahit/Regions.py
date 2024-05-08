from BaseClasses import Region, Entrance, ItemClassification, Location
from .Types import ChapterIndex, Difficulty, HatInTimeLocation, HatInTimeItem
from .Locations import location_table, storybook_pages, event_locs, is_location_valid, \
    shop_locations, TASKSANITY_START_ID, snatcher_coins, zero_jumps, zero_jumps_expert, zero_jumps_hard
from typing import TYPE_CHECKING, List, Dict
from .Rules import set_rift_rules, get_difficulty

if TYPE_CHECKING:
    from . import HatInTimeWorld


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

# Guarantee that the first level a player can access is a location dense area beatable with no items
guaranteed_first_acts = [
    "Welcome to Mafia Town",
    "Barrel Battle",
    "She Came from Outer Space",
    "Down with the Mafia!",
    "Heating Up Mafia Town",  # Removed in umbrella logic
    "The Golden Vault",

    "Contractual Obligations",  # Removed in painting logic
    "Queen Vanessa's Manor",  # Removed in umbrella/painting logic
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
}


def create_regions(world: "HatInTimeWorld"):
    w = world
    p = world.player

    # ------------------------------------------- HUB -------------------------------------------------- #
    menu = create_region(w, "Menu")
    spaceship = create_region_and_connect(w, "Spaceship", "Save File -> Spaceship", menu)

    # we only need the menu and the spaceship regions
    if world.is_dw_only():
        return

    create_rift_connections(w, create_region(w, "Time Rift - Gallery"))
    create_rift_connections(w, create_region(w, "Time Rift - The Lab"))

    # ------------------------------------------- MAFIA TOWN ------------------------------------------- #
    mafia_town = create_region_and_connect(w, "Mafia Town", "Telescope -> Mafia Town", spaceship)
    mt_act1 = create_region_and_connect(w, "Welcome to Mafia Town", "Mafia Town - Act 1", mafia_town)
    mt_act2 = create_region_and_connect(w, "Barrel Battle", "Mafia Town - Act 2", mafia_town)
    mt_act3 = create_region_and_connect(w, "She Came from Outer Space", "Mafia Town - Act 3", mafia_town)
    mt_act4 = create_region_and_connect(w, "Down with the Mafia!", "Mafia Town - Act 4", mafia_town)
    mt_act6 = create_region_and_connect(w, "Heating Up Mafia Town", "Mafia Town - Act 6", mafia_town)
    mt_act5 = create_region_and_connect(w, "Cheating the Race", "Mafia Town - Act 5", mafia_town)
    mt_act7 = create_region_and_connect(w, "The Golden Vault", "Mafia Town - Act 7", mafia_town)

    # ------------------------------------------- BOTB ------------------------------------------------- #
    botb = create_region_and_connect(w, "Battle of the Birds", "Telescope -> Battle of the Birds", spaceship)
    dbs = create_region_and_connect(w, "Dead Bird Studio", "Battle of the Birds - Act 1", botb)
    create_region_and_connect(w, "Murder on the Owl Express", "Battle of the Birds - Act 2", botb)
    pp = create_region_and_connect(w, "Picture Perfect", "Battle of the Birds - Act 3", botb)
    tr = create_region_and_connect(w, "Train Rush", "Battle of the Birds - Act 4", botb)
    create_region_and_connect(w, "The Big Parade", "Battle of the Birds - Act 5", botb)
    create_region_and_connect(w, "Award Ceremony", "Battle of the Birds - Finale A", botb)
    basement = create_region_and_connect(w, "Dead Bird Studio Basement", "Battle of the Birds - Finale B", botb)
    create_rift_connections(w, create_region(w, "Time Rift - Dead Bird Studio"))
    create_rift_connections(w, create_region(w, "Time Rift - The Owl Express"))
    create_rift_connections(w, create_region(w, "Time Rift - The Moon"))

    # Items near the Dead Bird Studio elevator can be reached from the basement act, and beyond in Expert
    ev_area = create_region_and_connect(w, "Dead Bird Studio - Elevator Area", "DBS -> Elevator Area", dbs)
    post_ev_area = create_region_and_connect(w, "Dead Bird Studio - Post Elevator Area", "DBS -> Post Elevator Area", dbs)
    connect_regions(basement, ev_area, "DBS Basement -> Elevator Area", p)
    if world.options.LogicDifficulty.value >= int(Difficulty.EXPERT):
        connect_regions(basement, post_ev_area, "DBS Basement -> Post Elevator Area", p)

    # ------------------------------------------- SUBCON FOREST --------------------------------------- #
    subcon_forest = create_region_and_connect(w, "Subcon Forest", "Telescope -> Subcon Forest", spaceship)
    sf_act1 = create_region_and_connect(w, "Contractual Obligations", "Subcon Forest - Act 1", subcon_forest)
    sf_act2 = create_region_and_connect(w, "The Subcon Well", "Subcon Forest - Act 2", subcon_forest)
    sf_act3 = create_region_and_connect(w, "Toilet of Doom", "Subcon Forest - Act 3", subcon_forest)
    sf_act4 = create_region_and_connect(w, "Queen Vanessa's Manor", "Subcon Forest - Act 4", subcon_forest)
    sf_act5 = create_region_and_connect(w, "Mail Delivery Service", "Subcon Forest - Act 5", subcon_forest)
    create_region_and_connect(w, "Your Contract has Expired", "Subcon Forest - Finale", subcon_forest)

    # ------------------------------------------- ALPINE SKYLINE ------------------------------------------ #
    alpine_skyline = create_region_and_connect(w, "Alpine Skyline",  "Telescope -> Alpine Skyline", spaceship)
    alpine_freeroam = create_region_and_connect(w, "Alpine Free Roam", "Alpine Skyline - Free Roam", alpine_skyline)
    alpine_area = create_region_and_connect(w, "Alpine Skyline Area", "AFR -> Alpine Skyline Area", alpine_freeroam)

    # Needs to be separate because there are a lot of locations in Alpine that can't be accessed from Illness
    alpine_area_tihs = create_region_and_connect(w, "Alpine Skyline Area (TIHS)", "-> Alpine Skyline Area (TIHS)",
                                                 alpine_area)

    create_region_and_connect(w, "The Birdhouse", "-> The Birdhouse", alpine_area)
    create_region_and_connect(w, "The Lava Cake", "-> The Lava Cake", alpine_area)
    create_region_and_connect(w, "The Windmill", "-> The Windmill", alpine_area)
    create_region_and_connect(w, "The Twilight Bell", "-> The Twilight Bell", alpine_area)

    illness = create_region_and_connect(w, "The Illness has Spread", "Alpine Skyline - Finale", alpine_skyline)
    connect_regions(illness, alpine_area_tihs, "TIHS -> Alpine Skyline Area (TIHS)", p)
    create_rift_connections(w, create_region(w, "Time Rift - Alpine Skyline"))
    create_rift_connections(w, create_region(w, "Time Rift - The Twilight Bell"))
    create_rift_connections(w, create_region(w, "Time Rift - Curly Tail Trail"))

    # ------------------------------------------- OTHER -------------------------------------------------- #
    mt_area: Region = create_region(w, "Mafia Town Area")
    mt_area_humt: Region = create_region(w, "Mafia Town Area (HUMT)")
    connect_regions(mt_area, mt_area_humt, "MT Area -> MT Area (HUMT)", p)
    connect_regions(mt_act1, mt_area, "Mafia Town Entrance WTMT", p)
    connect_regions(mt_act2, mt_area, "Mafia Town Entrance BB", p)
    connect_regions(mt_act3, mt_area, "Mafia Town Entrance SCFOS", p)
    connect_regions(mt_act4, mt_area, "Mafia Town Entrance DWTM", p)
    connect_regions(mt_act5, mt_area, "Mafia Town Entrance CTR", p)
    connect_regions(mt_act6, mt_area_humt, "Mafia Town Entrance HUMT", p)
    connect_regions(mt_act7, mt_area, "Mafia Town Entrance TGV", p)

    create_rift_connections(w, create_region(w, "Time Rift - Mafia of Cooks"))
    create_rift_connections(w, create_region(w, "Time Rift - Sewers"))
    create_rift_connections(w, create_region(w, "Time Rift - Bazaar"))

    sf_area: Region = create_region(w, "Subcon Forest Area")
    connect_regions(sf_act1, sf_area, "Subcon Forest Entrance CO", p)
    connect_regions(sf_act2, sf_area, "Subcon Forest Entrance SW", p)
    connect_regions(sf_act3, sf_area, "Subcon Forest Entrance TOD", p)
    connect_regions(sf_act4, sf_area, "Subcon Forest Entrance QVM", p)
    connect_regions(sf_act5, sf_area, "Subcon Forest Entrance MDS", p)

    create_rift_connections(w, create_region(w, "Time Rift - Sleepy Subcon"))
    create_rift_connections(w, create_region(w, "Time Rift - Pipe"))
    create_rift_connections(w, create_region(w, "Time Rift - Village"))

    badge_seller = create_badge_seller(w)
    connect_regions(mt_area, badge_seller, "MT Area -> Badge Seller", p)
    connect_regions(mt_area_humt, badge_seller, "MT Area (HUMT) -> Badge Seller", p)
    connect_regions(sf_area, badge_seller, "SF Area -> Badge Seller", p)
    connect_regions(dbs, badge_seller, "DBS -> Badge Seller", p)
    connect_regions(pp, badge_seller, "PP -> Badge Seller", p)
    connect_regions(tr, badge_seller, "TR -> Badge Seller", p)
    connect_regions(alpine_area_tihs, badge_seller, "ASA -> Badge Seller", p)

    times_end = create_region_and_connect(w, "Time's End", "Telescope -> Time's End", spaceship)
    create_region_and_connect(w, "The Finale", "Time's End - Act 1", times_end)

    # ------------------------------------------- DLC1 ------------------------------------------------- #
    if w.is_dlc1():
        arctic_cruise = create_region_and_connect(w, "The Arctic Cruise", "Telescope -> The Arctic Cruise", spaceship)
        cruise_ship = create_region(w, "Cruise Ship")

        ac_act1 = create_region_and_connect(w, "Bon Voyage!", "The Arctic Cruise - Act 1", arctic_cruise)
        ac_act2 = create_region_and_connect(w, "Ship Shape", "The Arctic Cruise - Act 2", arctic_cruise)
        ac_act3 = create_region_and_connect(w, "Rock the Boat", "The Arctic Cruise - Finale", arctic_cruise)

        connect_regions(ac_act1, cruise_ship, "Cruise Ship Entrance BV", p)
        connect_regions(ac_act2, cruise_ship, "Cruise Ship Entrance SS", p)
        connect_regions(ac_act3, cruise_ship, "Cruise Ship Entrance RTB", p)
        create_rift_connections(w, create_region(w, "Time Rift - Balcony"))
        create_rift_connections(w, create_region(w, "Time Rift - Deep Sea"))

        if w.options.ExcludeTour.value == 0:
            create_rift_connections(w, create_region(w, "Time Rift - Tour"))

        if w.options.Tasksanity.value > 0:
            create_tasksanity_locations(w)

        connect_regions(cruise_ship, badge_seller, "CS -> Badge Seller", p)

    if w.is_dlc2():
        nyakuza_metro = create_region_and_connect(w, "Nyakuza Metro", "Telescope -> Nyakuza Metro", spaceship)
        metro_freeroam = create_region_and_connect(w, "Nyakuza Free Roam", "Nyakuza Metro - Free Roam", nyakuza_metro)
        create_region_and_connect(w, "Rush Hour", "Nyakuza Metro - Finale", nyakuza_metro)

        yellow = create_region_and_connect(w, "Yellow Overpass Station", "-> Yellow Overpass Station", metro_freeroam)
        green = create_region_and_connect(w, "Green Clean Station", "-> Green Clean Station", metro_freeroam)
        pink = create_region_and_connect(w, "Pink Paw Station", "-> Pink Paw Station", metro_freeroam)
        create_region_and_connect(w, "Bluefin Tunnel", "-> Bluefin Tunnel", metro_freeroam)  # No manhole

        create_region_and_connect(w, "Yellow Overpass Manhole", "-> Yellow Overpass Manhole", yellow)
        create_region_and_connect(w, "Green Clean Manhole", "-> Green Clean Manhole", green)
        create_region_and_connect(w, "Pink Paw Manhole", "-> Pink Paw Manhole", pink)

        create_rift_connections(w, create_region(w, "Time Rift - Rumbi Factory"))
        create_thug_shops(w)


def create_rift_connections(world: "HatInTimeWorld", region: Region):
    for i, name in enumerate(rift_access_regions[region.name]):
        act_region = world.multiworld.get_region(name, world.player)
        entrance_name = f"{region.name} Portal - Entrance {i+1}"
        connect_regions(act_region, region, entrance_name, world.player)


def create_tasksanity_locations(world: "HatInTimeWorld"):
    ship_shape: Region = world.multiworld.get_region("Ship Shape", world.player)
    id_start: int = TASKSANITY_START_ID
    for i in range(world.options.TasksanityCheckCount.value):
        location = HatInTimeLocation(world.player, f"Tasksanity Check {i+1}", id_start+i, ship_shape)
        ship_shape.locations.append(location)


def randomize_act_entrances(world: "HatInTimeWorld"):
    region_list: List[Region] = get_act_regions(world)
    world.random.shuffle(region_list)
    region_list.sort(key=sort_acts)
    candidate_list: List[Region] = region_list.copy()
    rift_dict: Dict[str, Region] = {}

    # Check if Plando's are valid, if so, map them
    if len(world.options.ActPlando) > 0:
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

            if is_valid_plando(world, region.name) and is_valid_plando(world, act.name, True):
                region_list.remove(region)
                candidate_list.remove(act)
                connect_acts(world, region, act, rift_dict)
            else:
                print(f"ActPlando "
                      f"({player_name}) - "
                      f"\"{name1}: {name2}\" "
                      f"is an invalid or disallowed act plando combination!")

    first_act_mapped: bool = False
    ignore_certain_rules: bool = False
    while len(region_list) > 0:
        region: Region
        if not first_act_mapped:
            region = get_first_act(world)
        else:
            region = region_list[0]

        candidate: Region
        valid_candidates: List[Region] = []

        # Look for candidates to map this act to
        for c in candidate_list:
            # Map the first act before anything
            if not first_act_mapped:
                if not is_valid_first_act(world, c):
                    continue

                valid_candidates.append(c)
                first_act_mapped = True
                break  # we can stop here, as we only need one

            if is_valid_act_combo(world, region, c, bool(world.options.ActRandomizer.value == 1), ignore_certain_rules):
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
        if not is_act_blacklisted(world, name):
            continue

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

    if act.name == "Contractual Obligations":
        return -2

    world = act.multiworld.worlds[act.player]
    blacklist = world.options.ActBlacklist
    if len(blacklist) > 0:
        for name, act_list in blacklist.items():
            if act.name == name or act.name in act_list:
                return -1

    return 0


def get_first_act(world: "HatInTimeWorld") -> Region:
    first_chapter = get_first_chapter_region(world)
    act: Region
    for e in first_chapter.exits:
        if "Act 1" in e.name or "Free Roam" in e.name:
            act = e.connected_region
            break

    # noinspection PyUnboundLocalVariable
    return act


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
                       exit_act: Region, separate_rifts: bool, ignore_certain_rules=False) -> bool:

    # Ignore certain rules that aren't to prevent impossible combos. This is needed for ActPlando.
    if not ignore_certain_rules:
        if separate_rifts and not ignore_certain_rules:
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

        if world.options.FinaleShuffle.value > 0 and entrance_act.name in chapter_finales:
            if exit_act.name not in chapter_finales:
                return False

        if entrance_act.name in rift_access_regions and exit_act.name in rift_access_regions[entrance_act.name]:
            return False

    # Blacklisted?
    if entrance_act.name in blacklisted_combos.keys() and exit_act.name in blacklisted_combos[entrance_act.name]:
        return False

    if len(world.options.ActBlacklist) > 0:
        act_blacklist = world.options.ActBlacklist.get(entrance_act.name)
        if act_blacklist is not None and exit_act.name in act_blacklist:
            return False

    # Prevent Contractual Obligations from being inaccessible if contracts are not shuffled
    if world.options.ShuffleActContracts.value == 0:
        if (entrance_act.name == "Your Contract has Expired" or entrance_act.name == "The Subcon Well") \
                and exit_act.name == "Contractual Obligations":
            return False

    return True


def is_valid_first_act(world: "HatInTimeWorld", act: Region) -> bool:
    if act.name not in guaranteed_first_acts:
        return False

    # Not completable without Umbrella
    if world.options.UmbrellaLogic.value > 0 \
            and (act.name == "Heating Up Mafia Town" or act.name == "Queen Vanessa's Manor"):
        return False

    # Subcon sphere 1 is too small without painting unlocks, and no acts are completable either
    if world.options.ShuffleSubconPaintings.value > 0 \
            and "Subcon Forest" in act_entrances[act.name]:
        return False

    return True


def connect_time_rift(world: "HatInTimeWorld", time_rift: Region, exit_region: Region):
    count: int = len(rift_access_regions[time_rift.name])
    i: int = 1
    while i <= count:
        name = f"{time_rift.name} Portal - Entrance {i}"
        entrance: Entrance
        try:
            entrance = world.multiworld.get_entrance(name, world.player)
        except KeyError:
            if len(time_rift.entrances) > 0:
                entrance = time_rift.entrances[i-1]
            else:
                entrance = connect_regions(time_rift, exit_region, name, world.player)

        # noinspection PyUnboundLocalVariable
        reconnect_regions(entrance, entrance.parent_region, exit_region)
        i += 1


def get_act_regions(world: "HatInTimeWorld") -> List[Region]:
    act_list: List[Region] = []
    for region in world.multiworld.get_regions(world.player):
        if region.name in chapter_act_info.keys():
            if not is_act_blacklisted(world, region.name):
                act_list.append(region)

    return act_list


def is_act_blacklisted(world: "HatInTimeWorld", name: str) -> bool:
    plando: bool = name in world.options.ActPlando.keys() and is_valid_plando(world, name) \
        or name in world.options.ActPlando.values() and is_valid_plando(world, name, True)

    if name == "The Finale":
        return not plando and world.options.EndGoal.value == 1

    if name == "Rush Hour":
        return not plando and world.options.EndGoal.value == 2

    if name == "Time Rift - Tour":
        return world.options.ExcludeTour.value > 0

    return name in blacklisted_acts.values()


def is_valid_plando(world: "HatInTimeWorld", region: str, is_candidate: bool = False) -> bool:
    # Duplicated keys will throw an exception for us, but we still need to check for duplicated values
    if is_candidate:
        found_list: List = []
        old_region = region
        for name, act in world.options.ActPlando.items():
            if act == old_region:
                region = name
                found_list.append(name)

        if len(found_list) == 0:
            return False

        if len(found_list) > 1:
            raise Exception(f"ActPlando ({world.multiworld.get_player_name(world.player)}) - "
                  f"Duplicated act plando mapping found for act: \"{old_region}\"")
    elif region not in world.options.ActPlando.keys():
        return False

    if region in blacklisted_acts.values() or (region not in act_entrances.keys() and "Time Rift" not in region):
        return False

    act = world.options.ActPlando.get(region)
    try:
        world.multiworld.get_region(region, world.player)
        world.multiworld.get_region(act, world.player)
    except KeyError:
        return False

    if act in blacklisted_acts.values() or (act not in act_entrances.keys() and "Time Rift" not in act):
        return False

    # Don't allow plando-ing things onto the first act that aren't completable with nothing
    if act == get_first_act(world).name and not is_valid_first_act(world, act):
        return False

    # Don't allow straight up impossible mappings
    if (region == "Time Rift - Curly Tail Trail"
       or region == "Time Rift - The Twilight Bell"
       or region == "The Illness has Spread") \
       and act == "Alpine Free Roam":
        return False

    if (region == "Rush Hour" or region == "Time Rift - Rumbi Factory") \
       and act == "Nyakuza Free Roam":
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
            if key in storybook_pages.keys() \
               and world.options.ShuffleStorybookPages.value == 0:
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

    if world.options.BadgeSellerMaxItems.value > 0:
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


def connect_regions(start_region: Region, exit_region: Region, entrancename: str, player: int) -> Entrance:
    entrance = Entrance(player, entrancename, start_region)
    start_region.exits.append(entrance)
    entrance.connect(exit_region)
    return entrance


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

    connect_regions(entrance_region, exit_region, entrancename, world.player)
    return reg


def get_first_chapter_region(world: "HatInTimeWorld") -> Region:
    start_chapter: ChapterIndex = ChapterIndex(world.options.StartingChapter.value)
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


def create_thug_shops(world: "HatInTimeWorld"):
    min_items: int = min(world.options.NyakuzaThugMinShopItems.value, world.options.NyakuzaThugMaxShopItems.value)
    max_items: int = max(world.options.NyakuzaThugMaxShopItems.value, world.options.NyakuzaThugMinShopItems.value)
    count = -1
    step = 0
    old_name = ""

    for key, data in shop_locations.items():
        if data.nyakuza_thug == "":
            continue

        if old_name != "" and old_name == data.nyakuza_thug:
            continue

        try:
            if world.nyakuza_thug_items[data.nyakuza_thug] <= 0:
                continue
        except KeyError:
            pass

        if count == -1:
            count = world.random.randint(min_items, max_items)
            world.nyakuza_thug_items.setdefault(data.nyakuza_thug, count)
            if count <= 0:
                continue

        if count >= 1:
            region = world.multiworld.get_region(data.region, world.player)
            loc = HatInTimeLocation(world.player, key, data.id, region)
            region.locations.append(loc)
            world.shop_locs.append(loc.name)

            step += 1
            if step >= count:
                old_name = data.nyakuza_thug
                step = 0
                count = -1


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
