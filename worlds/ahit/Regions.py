from worlds.AutoWorld import World
from BaseClasses import Region, Entrance, ItemClassification, Location
from .Locations import HatInTimeLocation, location_table, storybook_pages, event_locs, is_location_valid, shop_locations
from .Items import HatInTimeItem
from .Types import ChapterIndex
import typing
from .Rules import set_rift_rules


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
    "Time Rift - Deep Sea":      ["Cruise Ship"],

    "Time Rift - Rumbi Factory": ["Nyakuza Free Roam"],
}

# Hat_ChapterActInfo, from the game files to be used in act shuffle
chapter_act_info = {
    "Time Rift - Gallery":          "hatintime_chapterinfo.spaceship.Spaceship_WaterRift_Gallery",
    "Time Rift - The Lab":          "hatintime_chapterinfo.spaceship.Spaceship_WaterRift_MailRoom",

    "Welcome to Mafia Town":        "hatintime_chapterinfo.MafiaTown.MafiaTown_Welcome",
    "Barrel Battle":                "hatintime_chapterinfo.MafiaTown.MafiaTown_BarrelBattle",
    "She Came from Outer Space":    "hatintime_chapterinfo.MafiaTown.MafiaTown_AlienChase",
    "Down with the Mafia!":         "hatintime_chapterinfo.MafiaTown.MafiaTown_MafiaBoss",
    "Cheating the Race":            "hatintime_chapterinfo.MafiaTown.MafiaTown_Race",
    "Heating Up Mafia Town":        "hatintime_chapterinfo.MafiaTown.MafiaTown_Lava",
    "The Golden Vault":             "hatintime_chapterinfo.MafiaTown.MafiaTown_GoldenVault",
    "Time Rift - Mafia of Cooks":   "hatintime_chapterinfo.MafiaTown.MafiaTown_CaveRift_Mafia",
    "Time Rift - Sewers":           "hatintime_chapterinfo.MafiaTown.MafiaTown_WaterRift_Easy",
    "Time Rift - Bazaar":           "hatintime_chapterinfo.MafiaTown.MafiaTown_WaterRift_Hard",

    "Dead Bird Studio":             "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_DeadBirdStudio",
    "Murder on the Owl Express":    "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_Murder",
    "Picture Perfect":              "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_PicturePerfect",
    "Train Rush":                   "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_TrainRush",
    "The Big Parade":               "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_Parade",
    "Award Ceremony":               "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_AwardCeremony",
    "Dead Bird Studio Basement":    "DeadBirdBasement",  # Dead Bird Studio Basement has no ChapterActInfo
    "Time Rift - Dead Bird Studio": "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_CaveRift_Basement",
    "Time Rift - The Owl Express":  "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_WaterRift_Panels",
    "Time Rift - The Moon":         "hatintime_chapterinfo.BattleOfTheBirds.BattleOfTheBirds_WaterRift_Parade",

    "Contractual Obligations":      "hatintime_chapterinfo.subconforest.SubconForest_IceWall",
    "The Subcon Well":              "hatintime_chapterinfo.subconforest.SubconForest_Cave",
    "Toilet of Doom":               "hatintime_chapterinfo.subconforest.SubconForest_Toilet",
    "Queen Vanessa's Manor":        "hatintime_chapterinfo.subconforest.SubconForest_Manor",
    "Mail Delivery Service":        "hatintime_chapterinfo.subconforest.SubconForest_MailDelivery",
    "Your Contract has Expired":    "hatintime_chapterinfo.subconforest.SubconForest_SnatcherBoss",
    "Time Rift - Sleepy Subcon":    "hatintime_chapterinfo.subconforest.SubconForest_CaveRift_Raccoon",
    "Time Rift - Pipe":             "hatintime_chapterinfo.subconforest.SubconForest_WaterRift_Hookshot",
    "Time Rift - Village":          "hatintime_chapterinfo.subconforest.SubconForest_WaterRift_Dwellers",

    "Alpine Free Roam":                 "hatintime_chapterinfo.AlpineSkyline.AlpineSkyline_IntroMountain",
    "The Illness has Spread":           "hatintime_chapterinfo.AlpineSkyline.AlpineSkyline_Finale",
    "Time Rift - Alpine Skyline":       "hatintime_chapterinfo.AlpineSkyline.AlpineSkyline_CaveRift_Alpine",
    "Time Rift - The Twilight Bell":    "hatintime_chapterinfo.AlpineSkyline.AlpineSkyline_WaterRift_Goats",
    "Time Rift - Curly Tail Trail":     "hatintime_chapterinfo.AlpineSkyline.AlpineSkyline_WaterRift_Cats",

    "The Finale":                       "hatintime_chapterinfo.TheFinale.TheFinale_FinalBoss",
    "Time Rift - Tour":                 "hatintime_chapterinfo_dlc1.spaceship.CaveRift_Tour",

    "Bon Voyage!":                 "hatintime_chapterinfo_dlc1.Cruise.Cruise_Boarding",
    "Ship Shape":                  "hatintime_chapterinfo_dlc1.Cruise.Cruise_Working",
    "Rock the Boat":               "hatintime_chapterinfo_dlc1.Cruise.Cruise_Sinking",
    "Time Rift - Balcony":         "hatintime_chapterinfo_dlc1.Cruise.Cruise_WaterRift_Slide",
    "Time Rift - Deep Sea":        "hatintime_chapterinfo_dlc1.Cruise.Cruise_CaveRift",

    "Nyakuza Free Roam":            "hatintime_chapterinfo_dlc2.metro.Metro_FreeRoam",
    "Rush Hour":                    "hatintime_chapterinfo_dlc2.metro.Metro_Escape",
    "Time Rift - Rumbi Factory":    "hatintime_chapterinfo_dlc2.metro.Metro_RumbiFactory"
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

# Acts blacklisted in act shuffle
# entrance: region
blacklisted_acts = {
    "Battle of the Birds - Finale A":   "Award Ceremony",
    "Time's End - Act 1":               "The Finale",
}


def create_regions(world: World):
    w = world
    mw = world.multiworld
    p = world.player

    # ------------------------------------------- HUB -------------------------------------------------- #
    menu = create_region(w, "Menu")
    spaceship = create_region_and_connect(w, "Spaceship", "Save File -> Spaceship", menu)
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
    create_region_and_connect(w, "Picture Perfect", "Battle of the Birds - Act 3", botb)
    create_region_and_connect(w, "Train Rush", "Battle of the Birds - Act 4", botb)
    create_region_and_connect(w, "The Big Parade", "Battle of the Birds - Act 5", botb)
    create_region_and_connect(w, "Award Ceremony", "Battle of the Birds - Finale A", botb)
    create_region_and_connect(w, "Dead Bird Studio Basement", "Battle of the Birds - Finale B", botb)
    create_rift_connections(w, create_region(w, "Time Rift - Dead Bird Studio"))
    create_rift_connections(w, create_region(w, "Time Rift - The Owl Express"))
    create_rift_connections(w, create_region(w, "Time Rift - The Moon"))

    # Items near the Dead Bird Studio elevator can be reached from the basement act
    ev_area = create_region_and_connect(w, "Dead Bird Studio - Elevator Area", "DBS -> Elevator Area", dbs)
    connect_regions(mw.get_region("Dead Bird Studio Basement", p), ev_area, "DBS Basement -> Elevator Area", p)

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
    goat_village = create_region_and_connect(w, "Goat Village", "ASA -> Goat Village", alpine_area)

    create_region_and_connect(w, "The Birdhouse", "-> The Birdhouse", alpine_area)
    create_region_and_connect(w, "The Lava Cake", "-> The Lava Cake", alpine_area)
    create_region_and_connect(w, "The Windmill", "-> The Windmill", alpine_area)
    create_region_and_connect(w, "The Twilight Bell", "-> The Twilight Bell", alpine_area)

    illness = create_region_and_connect(w, "The Illness has Spread", "Alpine Skyline - Finale", alpine_skyline)
    connect_regions(illness, alpine_area, "TIHS -> Alpine Skyline Area", p)
    connect_regions(illness, goat_village, "TIHS -> Goat Village", p)
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
    connect_regions(mw.get_region("Dead Bird Studio", p), badge_seller, "DBS -> Badge Seller", p)
    connect_regions(mw.get_region("Picture Perfect", p), badge_seller, "PP -> Badge Seller", p)
    connect_regions(mw.get_region("Train Rush", p), badge_seller, "TR -> Badge Seller", p)
    connect_regions(mw.get_region("Goat Village", p), badge_seller, "GV -> Badge Seller", p)

    times_end = create_region_and_connect(w, "Time's End", "Telescope -> Time's End", spaceship)
    create_region_and_connect(w, "The Finale", "Time's End - Act 1", times_end)

    # ------------------------------------------- DLC1 ------------------------------------------------- #
    if mw.EnableDLC1[p].value > 0:
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
        create_rift_connections(w, create_region(w, "Time Rift - Tour"))

        if mw.Tasksanity[p].value > 0:
            create_tasksanity_locations(w)

        # force recache
        mw.get_region("Time Rift - Deep Sea", p)

        connect_regions(mw.get_region("Cruise Ship", p), badge_seller, "CS -> Badge Seller", p)

    if mw.EnableDLC2[p].value > 0:
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

    # force recache
    mw.get_region("Time Rift - Sewers", p)


def create_rift_connections(world: World, region: Region):
    i = 1
    for name in rift_access_regions[region.name]:
        act_region = world.multiworld.get_region(name, world.player)
        entrance_name = "{name} Portal - Entrance {num}"
        connect_regions(act_region, region, entrance_name.format(name=region.name, num=i), world.player)
        i += 1


def create_tasksanity_locations(world: World):
    ship_shape: Region = world.multiworld.get_region("Ship Shape", world.player)
    id_start: int = 300204
    for i in range(world.multiworld.TasksanityCheckCount[world.player].value):
        location = HatInTimeLocation(world.player, format("Tasksanity Check %i" % (i+1)), id_start+i, ship_shape)
        ship_shape.locations.append(location)
        # world.location_name_to_id.setdefault(location.name, location.address)


def randomize_act_entrances(world: World):
    region_list: typing.List[Region] = get_act_regions(world)
    world.multiworld.random.shuffle(region_list)

    separate_rifts: bool = bool(world.multiworld.ActRandomizer[world.player].value == 1)

    for region in region_list.copy():
        if (act_chapters[region.name] == "Alpine Skyline" or act_chapters[region.name] == "Nyakuza Metro") \
           and "Time Rift" not in region.name:
            region_list.remove(region)
            region_list.append(region)

    for region in region_list.copy():
        if "Time Rift" in region.name:
            region_list.remove(region)
            region_list.append(region)

    # Reverse the list, so we can do what we want to do first
    region_list.reverse()

    shuffled_list: typing.List[Region] = []
    mapped_list: typing.List[Region] = []
    rift_dict: typing.Dict[str, Region] = {}
    first_chapter: Region = get_first_chapter_region(world)
    has_guaranteed: bool = False

    i: int = 0
    while i < len(region_list):
        region = region_list[i]
        i += 1

        # Get the first accessible act, so we can map that to something first
        if not has_guaranteed:
            if act_chapters[region.name] != first_chapter.name:
                continue

            if region.name not in act_entrances.keys() or "Act 1" not in act_entrances[region.name] \
               and "Free Roam" not in act_entrances[region.name]:
                continue

            i = 0

        # Already mapped to something else
        if region in mapped_list:
            continue

        mapped_list.append(region)

        # Look for candidates to map this act to
        candidate_list: typing.List[Region] = []
        for candidate in region_list:

            if world.multiworld.VanillaAlpine[world.player].value > 0 and region.name == "Alpine Free Roam" \
               or world.multiworld.VanillaAlpine[world.player].value == 2 and region.name == "The Illness has Spread":
                candidate_list.append(region)
                break

            if world.multiworld.VanillaMetro[world.player].value > 0 and region.name == "Nyakuza Free Roam":
                candidate_list.append(region)
                break

            if region.name == "Rush Hour":
                if world.multiworld.EndGoal[world.player].value == 2 or \
                   world.multiworld.VanillaMetro[world.player].value == 2:
                    candidate_list.append(region)
                    break

            # We're mapping something to the first act, make sure it is valid
            if not has_guaranteed:
                if candidate.name not in guaranteed_first_acts:
                    continue

                # Not completable without Umbrella
                if world.multiworld.UmbrellaLogic[world.player].value > 0 \
                   and (candidate.name == "Heating Up Mafia Town" or candidate.name == "Queen Vanessa's Manor"):
                    continue

                # Subcon sphere 1 is too small without painting unlocks, and no acts are completable either
                if world.multiworld.ShuffleSubconPaintings[world.player].value > 0 \
                   and "Subcon Forest" in act_entrances[candidate.name]:
                    continue

                candidate_list.append(candidate)
                has_guaranteed = True
                break

            # Already mapped onto something else
            if candidate in shuffled_list:
                continue

            if separate_rifts:
                # Don't map Time Rifts to normal acts
                if "Time Rift" in region.name and "Time Rift" not in candidate.name:
                    continue

                # Don't map normal acts to Time Rifts
                if "Time Rift" not in region.name and "Time Rift" in candidate.name:
                    continue

                # Separate purple rifts
                if region.name in purple_time_rifts and candidate.name not in purple_time_rifts \
                   or region.name not in purple_time_rifts and candidate.name in purple_time_rifts:
                    continue

            # Don't map Alpine to its own finale
            if region.name == "The Illness has Spread" and candidate.name == "Alpine Free Roam":
                continue

            # Ditto for Metro
            if region.name == "Rush Hour" and candidate.name == "Nyakuza Free Roam":
                continue

            if region.name in rift_access_regions and candidate.name in rift_access_regions[region.name]:
                continue

            candidate_list.append(candidate)

        candidate: Region = candidate_list[world.multiworld.random.randint(0, len(candidate_list)-1)]
        shuffled_list.append(candidate)

        # Vanilla
        if candidate.name == region.name:
            if region.name in rift_access_regions.keys():
                rift_dict.setdefault(region.name, candidate)

            world.update_chapter_act_info(region, candidate)
            continue

        if region.name in rift_access_regions.keys():
            connect_time_rift(world, region, candidate)
            rift_dict.setdefault(region.name, candidate)
        else:
            if candidate.name in rift_access_regions.keys():
                for e in candidate.entrances.copy():
                    e.parent_region.exits.remove(e)
                    e.connected_region.entrances.remove(e)
                    del e.parent_region
                    del e.connected_region

            entrance = world.multiworld.get_entrance(act_entrances[region.name], world.player)
            reconnect_regions(entrance, world.multiworld.get_region(act_chapters[region.name], world.player), candidate)

        world.update_chapter_act_info(region, candidate)

    for name in blacklisted_acts.values():
        if not is_act_blacklisted(world, name):
            continue

        region: Region = world.multiworld.get_region(name, world.player)
        world.update_chapter_act_info(region, region)

    set_rift_rules(world, rift_dict)


def connect_time_rift(world: World, time_rift: Region, exit_region: Region):
    count: int = len(rift_access_regions[time_rift.name])
    i: int = 1
    while i <= count:
        name = format("%s Portal - Entrance %i" % (time_rift.name, i))
        entrance: Entrance = world.multiworld.get_entrance(name, world.player)
        reconnect_regions(entrance, entrance.parent_region, exit_region)
        i += 1


def get_act_regions(world: World) -> typing.List[Region]:
    act_list: typing.List[Region] = []
    for region in world.multiworld.get_regions(world.player):
        if region.name in chapter_act_info.keys():
            if not is_act_blacklisted(world, region.name):
                act_list.append(region)

    return act_list


def is_act_blacklisted(world: World, name: str) -> bool:
    if name == "The Finale":
        return world.multiworld.EndGoal[world.player].value == 1

    return name in blacklisted_acts.values()


def create_region(world: World, name: str) -> Region:
    reg = Region(name, world.player, world.multiworld)

    for (key, data) in location_table.items():
        if data.nyakuza_thug != "":
            continue

        if data.region == name:
            if key in storybook_pages.keys() \
               and world.multiworld.ShuffleStorybookPages[world.player].value == 0:
                continue

            location = HatInTimeLocation(world.player, key, data.id, reg)
            reg.locations.append(location)
            if location.name in shop_locations:
                world.shop_locs.append(location.name)

    world.multiworld.regions.append(reg)
    return reg


def create_badge_seller(world: World) -> Region:
    badge_seller = Region("Badge Seller", world.player, world.multiworld)
    world.multiworld.regions.append(badge_seller)
    count: int = 0
    max_items: int = 0

    if world.multiworld.BadgeSellerMaxItems[world.player].value > 0:
        max_items = world.multiworld.random.randint(world.multiworld.BadgeSellerMinItems[world.player].value,
                                                    world.multiworld.BadgeSellerMaxItems[world.player].value)

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


def connect_regions(start_region: Region, exit_region: Region, entrancename: str, player: int):
    entrance = Entrance(player, entrancename, start_region)
    start_region.exits.append(entrance)
    entrance.connect(exit_region)


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


def create_region_and_connect(world: World,
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


def get_first_chapter_region(world: World) -> Region:
    start_chapter: ChapterIndex = world.multiworld.StartingChapter[world.player]
    return world.multiworld.get_region(chapter_regions.get(start_chapter), world.player)


def get_act_original_chapter(world: World, act_name: str) -> Region:
    return world.multiworld.get_region(act_chapters[act_name], world.player)


def create_thug_shops(world: World):
    min_items: int = world.multiworld.NyakuzaThugMinShopItems[world.player].value
    max_items: int = world.multiworld.NyakuzaThugMaxShopItems[world.player].value
    count: int = -1
    step: int = 0
    old_name: str = ""

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
            count = world.multiworld.random.randint(min_items, max_items)
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


def create_events(world: World) -> int:
    count: int = 0

    for (name, data) in event_locs.items():
        if not is_location_valid(world, name):
            continue

        event: Location = create_event(name, world.multiworld.get_region(data.region, world.player), world)

        if data.act_complete_event:
            act_completion: str = format("Act Completion (%s)" % data.region)
            event.access_rule = world.multiworld.get_location(act_completion, world.player).access_rule

        count += 1

    return count


def create_event(name: str, region: Region, world: World) -> Location:
    event = HatInTimeLocation(world.player, name, None, region)
    region.locations.append(event)
    event.place_locked_item(HatInTimeItem(name, ItemClassification.progression, None, world.player))
    return event
