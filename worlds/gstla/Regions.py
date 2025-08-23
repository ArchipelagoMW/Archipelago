from typing import List, Dict, Optional, TYPE_CHECKING
from BaseClasses import MultiWorld, Region
from worlds.gstla.Locations import GSTLALocation, location_name_to_id
from .gen.LocationNames import LocationName
from .gen.LocationData import LocationType
from .Names.RegionName import RegionName
from .Names.EntranceName import EntranceName
from copy import deepcopy
from .GstlaTypes import RegionData

if TYPE_CHECKING:
    from . import GSTLAWorld


def create_region(world: 'GSTLAWorld', region_data: RegionData):
    region = Region(region_data.name, world.player, world.multiworld)
    gs_locations: Dict[str, Optional[int]] = dict()
    for location in region_data.locations:
        location_data = location_name_to_id[location]
        #logging.error(region.name + ' ' + location)
        if world.options.item_shuffle < 3 and location_data.loc_type == LocationType.Hidden:
            continue
        if location_data.loc_type == LocationType.Djinn:
            loc = GSTLALocation.create_djinn_location(world.player, location, location_data, region)
        elif location_data.loc_type == LocationType.Event:
            loc = GSTLALocation.create_event_location(world.player, location, location_data, region)
        else:
            loc = GSTLALocation(world.player, location, location_data, region)
        region.locations.append(loc)
    region.add_locations(gs_locations)

    for regionExit in region_data.exits:
        region.create_exit(regionExit)

    world.multiworld.regions.append(region)


def create_regions(world: 'GSTLAWorld'):
    regions_copy = deepcopy(regions)
    if world.options.omit_locations < 2:
        regions_copy[RegionName.YampiDesertCave].locations.append(LocationName.Yampi_Desert_Cave_Valukar)
        regions_copy[RegionName.YampiDesertCave].locations.append(LocationName.Yampi_Desert_Cave_Daedalus)
        regions_copy[RegionName.IsletCave].locations.append(LocationName.Islet_Cave_Sentinel)
        regions_copy[RegionName.IsletCave].locations.append(LocationName.Islet_Cave_Catastrophe)
        regions_copy[RegionName.TreasureIsland_PostReunion].locations.append(LocationName.Treasure_Isle_Star_Magician)
        regions_copy[RegionName.TreasureIsland_PostReunion].locations.append(LocationName.Treasure_Isle_Azul)

    if world.options.omit_locations < 1:
        regions_copy[RegionName.AnemosSanctum].locations.append(LocationName.Anemos_Inner_Sanctum_Dullahan)
        regions_copy[RegionName.AnemosSanctum].locations.append(LocationName.Anemos_Inner_Sanctum_Orihalcon)
        regions_copy[RegionName.AnemosSanctum].locations.append(LocationName.Anemos_Inner_Sanctum_Iris)
        regions_copy[RegionName.AnemosSanctum].locations.append(LocationName.Anemos_Inner_Sanctum_Charon)
        regions_copy[RegionName.AnemosSanctum].locations.append(LocationName.Anemos_Inner_Sanctum_Dark_Matter)

    if world.options.lemurian_ship < 2:
        regions_copy[RegionName.Lemurian_Ship].locations.append(LocationName.Lemurian_Ship_Engine_Room)
        regions_copy[RegionName.Lemurian_Ship].locations.append(LocationName.Lemurian_Ship_Aqua_Hydra)
    else:
        regions_copy[RegionName.Lemurian_Ship_Revisit].locations.append(LocationName.Lemurian_Ship_Aqua_Hydra)

    if world.options.start_with_wings_of_anemos == 0:
        regions_copy[RegionName.Reunion].locations.append(LocationName.Contigo_Wings_of_Anemos)

    for region in regions_copy.values():
        create_region(world, region)


regions: Dict[str, RegionData] = {
    RegionName.Menu: RegionData(RegionName.Menu, None, [EntranceName.Menu_StartGame]),
    RegionName.Idejima: RegionData(RegionName.Idejima,
    [
        LocationName.Idejima_Growth,
        LocationName.Idejima_Shamans_Rod,
        LocationName.Idejima_Jenna,
        LocationName.Idejima_Sheba,
        LocationName.Victory_Event,
    ],
    [
        EntranceName.IdejimaToDaila,
        EntranceName.AnywhereToJoinedPartyMembers
    ]),
    RegionName.PartyMembers: RegionData(RegionName.PartyMembers,
    [
        LocationName.Idejima_Mind_Read,
        LocationName.Idejima_Whirlwind,
        LocationName.Kibombo_Douse_Drop,
        LocationName.Kibombo_Frost_Jewel,
        LocationName.Spring,
        LocationName.Shade,
        LocationName.Contigo_Carry_Stone,
        LocationName.Contigo_Lifting_Gem,
        LocationName.Contigo_Orb_of_Force,
        LocationName.Contigo_Catch_Beads,
        LocationName.Flint,
        LocationName.Granite,
        LocationName.Quartz,
        LocationName.Vine,
        LocationName.Sap,
        LocationName.Ground,
        LocationName.Fizz,
        LocationName.Sleet,
        LocationName.Mist,
        LocationName.Spritz,
        LocationName.Hail,
        LocationName.Tonic,
        LocationName.Forge,
        LocationName.Fever,
        LocationName.Corona,
        LocationName.Scorch,
        LocationName.Ember,
        LocationName.Flash,
        LocationName.Gust,
        LocationName.Breeze,
        LocationName.Zephyr,
        LocationName.Smog,
        LocationName.Kite,
        LocationName.Squall
    ],
    []),
    RegionName.Daila: RegionData(RegionName.Daila,
    [
        LocationName.Daila_Herb,
        LocationName.Daila_3_coins,
        LocationName.Daila_12_coins,
        LocationName.Daila_Psy_Crystal,
        LocationName.Daila_Sleep_Bomb,
        LocationName.Daila_Sea_Gods_Tear,
        LocationName.Daila_Smoke_Bomb,
        LocationName.Echo
    ],
    [
        EntranceName.DailaToShrineOfTheSeaGod,
        EntranceName.DailaToKandoreanTemple,
        EntranceName.DailaToDehkanPlateau
    ]),
    RegionName.KandoreamTemple: RegionData(RegionName.KandoreamTemple,
    [
        LocationName.Kandorean_Temple_Mimic,
        LocationName.Kandorean_Temple_Lash_Pebble,
        LocationName.Kandorean_Temple_Mysterious_Card,
        LocationName.Kandorean_Temple_Chestbeaters,
        LocationName.Fog
    ]),
    RegionName.ShrineOfTheSeaGod: RegionData(RegionName.ShrineOfTheSeaGod, [
        LocationName.Breath,
        LocationName.Shrine_of_the_Sea_God_Rusty_Staff,
        LocationName.Shrine_of_the_Sea_God_Right_Prong
    ]),
    RegionName.DehkanPlateau: RegionData(RegionName.DehkanPlateau,
    [
        LocationName.Dehkan_Plateau_Elixir,
        LocationName.Dehkan_Plateau_Pound_Cube,
        LocationName.Dehkan_Plateau_Themis_Axe,
        LocationName.Dehkan_Plateau_Full_Metal_Vest,
        LocationName.Dehkan_Plateau_Mint,
        LocationName.Dehkan_Plateau_Nut,
        LocationName.Cannon
    ],
    [
        EntranceName.DehkanPlateauToMadra
    ]),
    RegionName.IndraCavern: RegionData(RegionName.IndraCavern,
    [
        LocationName.Indra_Cavern_Zagan
    ]),
    RegionName.Madra: RegionData(RegionName.Madra,
    [
        LocationName.Madra_Elixir,
        LocationName.Madra_Antidote,
        LocationName.Madra_Cyclone_Chip,
        LocationName.Madra_Smoke_Bomb,
        LocationName.Madra_Sleep_Bomb,
        LocationName.Madra_15_coins,
        LocationName.Madra_Nurses_Cap,
        LocationName.Iron,
        LocationName.Char
    ],
    [
        EntranceName.MadraToIndraCavern,
        EntranceName.MadraToMadraCatacombs,
        EntranceName.MadraToOseniaCliffs,
        EntranceName.MadraToGondowanCliffs,
        EntranceName.MadraToEasternSea,
        EntranceName.MadraToLemurianShip
    ]),
    RegionName.MadraCatacombs: RegionData(RegionName.MadraCatacombs,
    [
        LocationName.Madra_Catacombs_Ruin_Key,
        LocationName.Madra_Catacombs_Tremor_Bit,
        LocationName.Madra_Catacombs_Apple,
        LocationName.Madra_Catacombs_Lucky_Medal,
        LocationName.Madra_Catacombs_Mist_Potion,
        LocationName.Madra_Catacombs_Moloch
    ]),
    RegionName.OseniaCliffs: RegionData(RegionName.OseniaCliffs,
    [
        LocationName.Osenia_Cliffs_Pirates_Sword
    ],
    [
        EntranceName.OseniaCliffsToMikasalla
    ]),
    RegionName.YampiDesertFront: RegionData(RegionName.YampiDesertFront,
    [
        LocationName.Yampi_Desert_Antidote,
        LocationName.Yampi_Desert_Guardian_Ring,
        LocationName.Yampi_Desert_Scoop_Gem,
        LocationName.Yampi_Desert_King_Scorpion,
        LocationName.Blitz,
    ],
    [
        EntranceName.YampiDesertFrontToYampiDesertBack
    ]),
    RegionName.YampiDesertBack: RegionData(RegionName.YampiDesertBack,
    [
        LocationName.Yampi_Desert_Lucky_Medal,
        LocationName.Yampi_Desert_Trainers_Whip,
        LocationName.Yampi_Desert_Hard_Nut,
        LocationName.Yampi_Desert_Blow_Mace,
        LocationName.Yampi_Desert_315_coins,
        LocationName.Yampi_Desert_Cave_Water_of_Life
    ],
    [
        EntranceName.YampiDesertBackToAlhafra,
        EntranceName.YampiDesertBackToYampiDesertCave
    ]),
    RegionName.YampiDesertCave: RegionData(RegionName.YampiDesertCave,
    [
        LocationName.Yampi_Desert_Cave_Orihalcon,
        LocationName.Yampi_Desert_Cave_Dark_Matter,
        LocationName.Yampi_Desert_Cave_Mythril_Silver,
        LocationName.Crystal,
    ]),
    RegionName.Alhafra: RegionData(RegionName.Alhafra,
    [
        LocationName.Alhafra_Psy_Crystal,
        LocationName.Alhafra_Sleep_Bomb,
        LocationName.Alhafra_Lucky_Medal,
        LocationName.Alhafra_32_coins,
        LocationName.Alhafra_Smoke_Bomb,
        LocationName.Alhafra_Elixir,
        LocationName.Alhafra_Apple,
        LocationName.Alhafra_Briggs,
        LocationName.Alhafra_Prison_Briggs
    ],
    [
        EntranceName.AlhafraToYampiDesertBack,
        EntranceName.AlhafraToAlhafraCave,
    ]),
    RegionName.AlhafraCave: RegionData(RegionName.AlhafraCave,
    [
        LocationName.Alhafran_Cave_123_coins,
        LocationName.Alhafran_Cave_Ixion_Mail,
        LocationName.Alhafran_Cave_Lucky_Medal,
        LocationName.Alhafran_Cave_Power_Bread,
        LocationName.Alhafran_Cave_777_coins,
        LocationName.Alhafran_Cave_Potion,
        LocationName.Alhafran_Cave_Psy_Crystal
    ]),
    RegionName.Mikasalla: RegionData(RegionName.Mikasalla,
    [
        LocationName.Mikasalla_Nut,
        LocationName.Mikasalla_Herb,
        LocationName.Mikasalla_Elixir,
        LocationName.Mikasalla_82_coins,
        LocationName.Mikasalla_Lucky_Pepper,
        LocationName.Sour,
        LocationName.Spark
    ],
    [
        EntranceName.MikasallaToYampiDesertFront,
        EntranceName.MikasallaToGaroh,
        EntranceName.MikasallaToOseniaCavern
    ]),
    RegionName.Garoh: RegionData(RegionName.Garoh,
    [
        LocationName.Garoh_Nut,
        LocationName.Garoh_Elixir,
        LocationName.Garoh_Sleep_Bomb,
        LocationName.Garoh_Smoke_Bomb,
        LocationName.Garoh_Hypnos_Sword,
        LocationName.Ether
    ],
    [
        EntranceName.GarohToAirsRock,
        EntranceName.GarohToYampiDesertBack
    ]),
    RegionName.AirsRock: RegionData(RegionName.AirsRock,
    [
        LocationName.Airs_Rock_Mimic,
        LocationName.Airs_Rock_Cookie,
        LocationName.Airs_Rock_Elixir,
        LocationName.Airs_Rock_666_coins,
        LocationName.Airs_Rock_Clarity_Circlet,
        LocationName.Airs_Rock_Fujin_Shield,
        LocationName.Airs_Rock_Psy_Crystal,
        LocationName.Airs_Rock_Sleep_Bomb,
        LocationName.Airs_Rock_Smoke_Bomb,
        LocationName.Airs_Rock_Storm_Brand,
        LocationName.Airs_Rock_Vial,
        LocationName.Airs_Rock_Vial_Two,
        LocationName.Airs_Rock_Vial_Three,
        LocationName.Airs_Rock_Flora,
        LocationName.Airs_Rock_Reveal
    ]),
    RegionName.OseniaCavern: RegionData(RegionName.OseniaCavern, [
        LocationName.Osenia_Cavern_Megaera
    ]),
    RegionName.GondowanCliffs: RegionData(RegionName.GondowanCliffs,
    [
        LocationName.Gondowan_Cliffs_Healing_Fungus,
        LocationName.Gondowan_Cliffs_Laughing_Fungus,
        LocationName.Gondowan_Cliffs_Sleep_Bomb,
        LocationName.Kindle
    ],
    [
        EntranceName.GondowanCliffsToNaribwe
    ]),
    RegionName.Naribwe: RegionData(RegionName.Naribwe,
    [
        LocationName.Naribwe_Elixir,
        LocationName.Naribwe_18_coins,
        LocationName.Naribwe_Sleep_Bomb,
        LocationName.Naribwe_Thorn_Crown,
        LocationName.Naribwe_Unicorn_Ring,
        LocationName.Chill
    ],
    [
        EntranceName.NaribweToKibomboMountains,
    ]),
    RegionName.KibomboMountains: RegionData(RegionName.KibomboMountains,
    [
        LocationName.Kibombo_Mountains_Disk_Axe,
        LocationName.Kibombo_Mountains_Power_Bread,
        LocationName.Kibombo_Mountains_Smoke_Bomb,
        LocationName.Kibombo_Mountains_Tear_Stone,
        LocationName.Waft
    ],
    [
        EntranceName.KibomboMountainsToKibombo
    ]),
    RegionName.Kibombo: RegionData(RegionName.Kibombo,
    [
        LocationName.Kibombo_Lucky_Medal,
        LocationName.Kibombo_Lucky_Pepper,
        LocationName.Kibombo_Nut,
        LocationName.Kibombo_Piers
    ],
    [
        EntranceName.KibomboToGabombaStatue,
    ]),
    RegionName.GabombaStatue: RegionData(RegionName.GabombaStatue,
    [
        LocationName.Gabomba_Statue_Black_Crystal,
        LocationName.Gabomba_Statue_Mimic,
        LocationName.Gabomba_Statue_Elixir,
        LocationName.Gabomba_Statue_Bone_Armlet,
        LocationName.Gabomba_Statue_Ritual,
        LocationName.Steel
    ],
    [
        EntranceName.GabombaStatueToGabombaCatacombs
    ]),
    RegionName.GabombaCatacombs: RegionData(RegionName.GabombaCatacombs,
    [
        LocationName.Gabomba_Catacombs_Mint,
        LocationName.Gabomba_Catacombs_Tomegathericon,
        LocationName.Mud
    ]),
    RegionName.Lemurian_Ship: RegionData(RegionName.Lemurian_Ship,
    [
    ]),
    RegionName.Lemurian_Ship_Revisit: RegionData(RegionName.Lemurian_Ship_Revisit,
    [
        LocationName.Lemurian_Ship_Elixir,
        LocationName.Lemurian_Ship_Potion,
        LocationName.Lemurian_Ship_Oil_Drop,
        LocationName.Lemurian_Ship_Antidote,
        LocationName.Lemurian_Ship_Mist_Potion,
    ]),
    RegionName.EasternSea: RegionData(RegionName.EasternSea,
    [
        LocationName.Overworld_Rusty_Axe,
        LocationName.Overworld_Rusty_Mace,
    ],
    [
        EntranceName.EasternSeaToAlhafra,
        EntranceName.EasternSeaToKibombo,
        EntranceName.EasternSeaToNaribwe,
        EntranceName.EasternSeaToWestIndraIslet,
        EntranceName.EasternSeaToNorthOseniaIslet,
        EntranceName.EasternSeaToSouthEastAngaraIslet,
        EntranceName.EasternSeaToSeaOfTimeIslet,
        EntranceName.EasternSeaToSeaOfTime,
        EntranceName.EasternSeaToTreasureIsland,
        EntranceName.EasternSeaToChampa,
        EntranceName.EasternSeaToAnkohlRuins,
        EntranceName.EasternSeaToIzumo,
        EntranceName.EasternSeaToGaiaRock,
        EntranceName.EasternSeaToYallam,
        EntranceName.EasternSeaToEastTundariaIslet,
        EntranceName.EasternSeaToTundariaTower,
        EntranceName.EasternSeaToApojiiIslands,
        EntranceName.EasternSeaToAquaRock,
        EntranceName.EasternSeaToWesternSea
    ]),
    RegionName.EastTundariaIslet: RegionData(RegionName.EastTundariaIslet,
    [
        LocationName.E_Tundaria_Islet_Lucky_Medal,
        LocationName.E_Tundaria_Islet_Pretty_Stone
    ]),
    RegionName.WestIndraIslet: RegionData(RegionName.WestIndraIslet,
    [
        LocationName.W_Indra_Islet_Lucky_Medal,
        LocationName.W_Indra_Islet_Lil_Turtle
    ]),
    RegionName.SouthEastAngaraIslet:RegionData(RegionName.SouthEastAngaraIslet,
    [
        LocationName.SE_Angara_Islet_Lucky_Medal,
        LocationName.SE_Angara_Islet_Red_Cloth
    ]),
    RegionName.NorthOseniaIslet:RegionData(RegionName.NorthOseniaIslet,
    [
        LocationName.N_Osenia_Islet_Lucky_Medal,
        LocationName.N_Osenia_Islet_Milk
    ]),
    RegionName.SeaOfTimeIslet:RegionData(RegionName.SeaOfTimeIslet,
    [
        LocationName.Sea_of_Time_Islet_Lucky_Medal
    ],
    [
        EntranceName.SeaOfTimeIsletToIsletCave
    ]),
    RegionName.IsletCave:RegionData(RegionName.IsletCave,
    [
        LocationName.Islet_Cave_Turtle_Boots,
        LocationName.Islet_Cave_Rusty_Staff,
        LocationName.Meld,
        LocationName.Serac,
    ]),
    RegionName.ApojiiIslands:RegionData(RegionName.ApojiiIslands,
    [
        LocationName.Apojii_Islands_Herb,
        LocationName.Apojii_Islands_Mint,
        LocationName.Apojii_Islands_32_coins,
        LocationName.Apojii_Islands_182_coins,
        LocationName.Apojii_Islands_Bramble_Seed,
        LocationName.Haze
    ]),
    RegionName.AquaRock:RegionData(RegionName.AquaRock,
    [
        LocationName.Aqua_Rock_Nut,
        LocationName.Aqua_Rock_Vial,
        LocationName.Aqua_Rock_Mimic,
        LocationName.Aqua_Rock_Elixir,
        LocationName.Aqua_Rock_Aquarius_Stone,
        LocationName.Aqua_Rock_Crystal_Powder,
        LocationName.Aqua_Rock_Lucky_Pepper,
        LocationName.Aqua_Rock_Mist_Sabre,
        LocationName.Aqua_Rock_Oil_Drop,
        LocationName.Aqua_Rock_Rusty_Sword,
        LocationName.Aqua_Rock_Tear_Stone,
        LocationName.Aqua_Rock_Water_of_Life,
        LocationName.Aqua_Rock_Parch,
        LocationName.Steam
    ]),
    RegionName.Izumo:RegionData(RegionName.Izumo,
    [
        LocationName.Izumo_Elixir,
        LocationName.Izumo_Antidote,
        LocationName.Izumo_Antidote_Two,
        LocationName.Izumo_Lucky_Medal,
        LocationName.Izumo_Smoke_Bomb,
        LocationName.Izumo_Festival_Coat,
        LocationName.Izumo_Phantasmal_Mail,
        LocationName.Izumo_Water_of_Life,
        LocationName.Izumo_Ulysses,
        LocationName.Coal
    ]),
    RegionName.GaiaRock:RegionData(RegionName.GaiaRock,
    [
        LocationName.Gaia_Rock_Nut,
        LocationName.Gaia_Rock_Apple,
        LocationName.Gaia_Rock_Mimic,
        LocationName.Gaia_Rock_Rusty_Mace,
        LocationName.Gaia_Rock_Cloud_Brand,
        LocationName.Gaia_Rock_Dancing_Idol,
        LocationName.Gaia_Rock_Serpent,
        LocationName.Gaia_Rock_Sand
    ]),
    RegionName.TreasureIsland: RegionData(RegionName.TreasureIsland,
    [
        LocationName.Treasure_Isle_161_coins,
        LocationName.Treasure_Isle_Lucky_Medal,
        LocationName.Treasure_Isle_Empty,
        LocationName.Treasure_Isle_Empty_Two,
        LocationName.Treasure_Isle_Empty_Three,
        LocationName.Treasure_Isle_Empty_Four,
        LocationName.Treasure_Isle_Empty_Five,
        LocationName.Treasure_Isle_Empty_Six,
        LocationName.Treasure_Isle_Empty_Seven,
        LocationName.Treasure_Isle_Empty_Eight,
        LocationName.Treasure_Isle_Empty_Nine,
        LocationName.Treasure_Isle_Empty_Ten,
    ],
    [
        EntranceName.TreasureIslandToTreasureIsland_Grindstone
    ]),
    RegionName.TreasureIsland_Grindstone: RegionData(RegionName.TreasureIsland_Grindstone,
    [
        LocationName.Treasure_Isle_911_coins,
        LocationName.Treasure_Isle_Psy_Crystal,
        LocationName.Treasure_Isle_Cookie,
        LocationName.Treasure_Isle_Sylph_Feather,
        LocationName.Treasure_Isle_Rusty_Axe,
        LocationName.Treasure_Isle_Star_Dust,
        LocationName.Treasure_Isle_Jesters_Armlet,
        LocationName.Treasure_Isle_Mimic,
    ],
    [
        EntranceName.TreasureIsland_GrindstoneToTreasureIsland_PostReunion
    ]),
    RegionName.TreasureIsland_PostReunion: RegionData(RegionName.TreasureIsland_PostReunion,
    [
        LocationName.Bane,  # Random Venus djinn from Gs1
        LocationName.Gale,
        LocationName.Treasure_Isle_Iris_Robe,
        LocationName.Treasure_Isle_Fire_Brand,
    ]),
    RegionName.TundariaTower: RegionData(RegionName.TundariaTower,
    [
        LocationName.Tundaria_Tower_Center_Prong,
        LocationName.Wheeze,
    ],
    [
        EntranceName.TundariaTowerToTundariaTower_Parched
    ]),
    RegionName.TundariaTower_Parched: RegionData(RegionName.TundariaTower_Parched,
    [
        LocationName.Tundaria_Tower_Mint,
        LocationName.Tundaria_Tower_Vial,
        LocationName.Tundaria_Tower_365_coins,
        LocationName.Tundaria_Tower_Hard_Nut,
        LocationName.Tundaria_Tower_Crystal_Powder,
        LocationName.Tundaria_Tower_Lightning_Sword,
        LocationName.Tundaria_Tower_Lucky_Medal,
        LocationName.Tundaria_Tower_Sylph_Feather,
        LocationName.Tundaria_Tower_Burst_Brooch,
        LocationName.Reflux
    ]),
    RegionName.AnkohlRuins: RegionData(RegionName.AnkohlRuins,
    [
        LocationName.Ankohl_Ruins_Empty,
        LocationName.Ankohl_Ruins_Empty_Two,
        LocationName.Ankohl_Ruins_Empty_Three,
        LocationName.Ankohl_Ruins_Empty_Four,
        LocationName.Ankohl_Ruins_Empty_Five,
        LocationName.Ankohl_Ruins_Empty_Six,
        LocationName.Ankohl_Ruins_210_coins,
        LocationName.Ankohl_Ruins_Crystal_Powder
    ],
    [
        EntranceName.AnkohlRuinsToAnkohlRuins_Sand
    ]),
    RegionName.AnkohlRuins_Sand: RegionData(RegionName.AnkohlRuins_Sand,
    [
        LocationName.Ankohl_Ruins_Potion,
        LocationName.Ankohl_Ruins_Nut,
        LocationName.Ankohl_Ruins_Thanatos_Mace,
        LocationName.Ankohl_Ruins_Power_Bread,
        LocationName.Ankohl_Ruins_Muni_Robe,
        LocationName.Ankohl_Ruins_365_coins,
        LocationName.Ankohl_Ruins_Sylph_Feather,
        LocationName.Ankohl_Ruins_Vial,
        LocationName.Ankohl_Ruins_Left_Prong
    ]),
    RegionName.Champa: RegionData(RegionName.Champa,
    [
        LocationName.Champa_Elixir,
        LocationName.Champa_Trident,
        LocationName.Champa_12_coins,
        LocationName.Champa_Sleep_Bomb,
        LocationName.Champa_Smoke_Bomb,
        LocationName.Champa_Lucky_Medal,
        LocationName.Champa_Viking_Helm,
        LocationName.Champa_Avimander,
    ]),
    RegionName.Yallam: RegionData(RegionName.Yallam,
    [
        LocationName.Yallam_Nut,
        LocationName.Yallam_Elixir,
        LocationName.Yallam_Antidote,
        LocationName.Yallam_Masamune,
        LocationName.Yallam_Oil_Drop,
        LocationName.Yallam_16_coins
    ],
    [
        EntranceName.YallamToTaopoSwamp
    ]),
    RegionName.TaopoSwamp: RegionData(RegionName.TaopoSwamp,
    [
        LocationName.Taopo_Swamp_Vial,
        LocationName.Taopo_Swamp_Cookie,
        LocationName.Taopo_Swamp_Star_Dust,
        LocationName.Taopo_Swamp_Bramble_Seed,
        LocationName.Taopo_Swamp_Tear_Stone,
        LocationName.Taopo_Swamp_Tear_Stone_Two,
        LocationName.Flower
    ]),
    RegionName.SeaOfTime: RegionData(RegionName.SeaOfTime,
    [
        LocationName.Sea_of_Time_Poseidon,
    ],
    [
        EntranceName.SeaOfTimeToLemuria
    ]),
    RegionName.Lemuria: RegionData(RegionName.Lemuria,
    [
        LocationName.Lemuria_Bone,
        LocationName.Lemuria_Hard_Nut,
        LocationName.Lemuria_Star_Dust,
        LocationName.Lemuria_Lucky_Medal,
        LocationName.Lemuria_Lucky_Medal_Two,
        LocationName.Lemuria_Rusty_Sword,
        LocationName.Lemuria_Eclipse,
        LocationName.Lemuria_Grindstone,
        LocationName.Rime
    ],
    [
        EntranceName.LemuriaToShipRevisit
    ]),
    RegionName.WesternSea: RegionData(RegionName.WesternSea,
    [
        LocationName.Overworld_Rusty_Sword,
        LocationName.Overworld_Rusty_Sword_Two,
        LocationName.Overworld_Rusty_Staff,
    ],
    [
        EntranceName.WesternSeaToSouthWestAttekaIslet,
        EntranceName.WesternSeaToHesperiaSettlement,
        EntranceName.WesternSeaToShamanVillageCave,
        EntranceName.WesternSeaToAttekaInlet,
        EntranceName.WesternSeaToAttekaCavern,
        EntranceName.WesternSeaToGondowanSettlement,
        EntranceName.WesternSeaToMagmaRock,
        EntranceName.WesternSeaToLoho,
        EntranceName.WesternSeaToAngaraCavern,
        EntranceName.WesternSeaToKaltIsland,
        EntranceName.WesternSeaToProx
    ]),
    RegionName.SouthWestAttekaIslet: RegionData(RegionName.SouthWestAttekaIslet,
    [
        LocationName.Luff, # Random djinn from gs1 spot
        LocationName.SW_Atteka_Islet_Dragon_Skin
    ]),
    RegionName.HesperiaSettlement: RegionData(RegionName.HesperiaSettlement,
    [
        LocationName.Hesperia_Settlement_166_coins,
        LocationName.Tinder
    ]),
    RegionName.ShamanVillageCave: RegionData(RegionName.ShamanVillageCave,
    [
        LocationName.Petra,
        LocationName.Eddy
    ],
    [
        EntranceName.ShamanVillageCaveToShamanVillage
    ]),
    RegionName.ShamanVillage: RegionData(RegionName.ShamanVillage,
    [
        LocationName.Shaman_Village_Elixir,
        LocationName.Shaman_Village_Elixir_Two,
        LocationName.Shaman_Village_Spirit_Gloves,
        LocationName.Shaman_Village_Hard_Nut,
        LocationName.Shaman_Village_Lucky_Medal,
        LocationName.Shaman_Village_Lucky_Pepper,
        LocationName.Shaman_Village_Weasels_Claw,
        LocationName.Shaman_Village_Moapa,
        LocationName.Shaman_Village_Hover_Jade,
        LocationName.Aroma,
        LocationName.Gasp
    ]),
    RegionName.AttekaInlet: RegionData(RegionName.AttekaInlet,
    [
        LocationName.Atteka_Inlet_Vial,
        LocationName.Geode
    ],
    [
        EntranceName.AttekaInletToContigo,
        EntranceName.AttekaInletToShipRevisit
    ]),
    RegionName.Contigo: RegionData(RegionName.Contigo,
    [
        LocationName.Contigo_Corn,
        LocationName.Contigo_Bramble_Seed,
        LocationName.Contigo_Dragon_Skin,
        LocationName.Contigo_Power_Bread,
        LocationName.Salt,
        LocationName.Core,
        LocationName.Shine,
    ],
    [
        EntranceName.ContigoToJupiterLighthouse,
        EntranceName.ContigoToAnemosInnerSanctum,
        EntranceName.ContigoToReunion
    ]),
    RegionName.JupiterLighthouse: RegionData(RegionName.JupiterLighthouse,
    [
        LocationName.Jupiter_Lighthouse_Mint,
        LocationName.Jupiter_Lighthouse_Blue_Key,
        LocationName.Jupiter_Lighthouse_Erinyes_Tunic,
        LocationName.Jupiter_Lighthouse_Meditation_Rod,
        LocationName.Jupiter_Lighthouse_Phaetons_Blade,
        LocationName.Jupiter_Lighthouse_306_coins,
        LocationName.Jupiter_Lighthouse_Mimic,
        LocationName.Jupiter_Lighthouse_Mist_Potion,
        LocationName.Jupiter_Lighthouse_Potion,
        LocationName.Jupiter_Lighthouse_Psy_Crystal,
        LocationName.Jupiter_Lighthouse_Red_Key,
        LocationName.Jupiter_Lighthouse_Water_of_Life,
        LocationName.Whorl,
        LocationName.Jupiter_Lighthouse_Aeri_Agatio_and_Karst
    ]),
    RegionName.Reunion: RegionData(RegionName.Reunion,
    [
        LocationName.Contigo_Isaac,
        LocationName.Contigo_Garet,
        LocationName.Contigo_Ivan,
        LocationName.Contigo_Mia,
        LocationName.Contigo_Reunion,
    ]),
    RegionName.AttekaCavern: RegionData(RegionName.AttekaCavern,
    [
        LocationName.Atteka_Cavern_Coatlicue
    ]),
    RegionName.AnemosSanctum: RegionData(RegionName.AnemosSanctum,
    [
    ]),
    RegionName.GondowanSettlement: RegionData(RegionName.GondowanSettlement,
    [
        LocationName.Gondowan_Settlement_Lucky_Medal,
        LocationName.Gondowan_Settlement_Star_Dust
    ]),
    RegionName.MagmaRock: RegionData(RegionName.MagmaRock,
    [
        LocationName.Magma_Rock_Mimic,
        LocationName.Magma_Rock_Salamander_Tail,
        LocationName.Magma_Rock_383_coins,
        LocationName.Magma_Rock_Oil_Drop
    ],
    [
        EntranceName.MagmaRockToMagmaRockInterior
    ]),
    RegionName.MagmaRockInterior: RegionData(RegionName.MagmaRockInterior,
    [
        LocationName.Torch,  # Random djinn from gs1 spot
        LocationName.Fury,
        LocationName.Magma_Rock_Lucky_Medal,
        LocationName.Magma_Rock_Mist_Potion,
        LocationName.Magma_Rock_Salamander_Tail_Two,
        LocationName.Magma_Rock_Golem_Core,
        LocationName.Magma_Rock_Blaze,
        LocationName.Magma_Rock_Magma_Ball
    ]),
    RegionName.Loho: RegionData(RegionName.Loho,
    [
        LocationName.Loho_Crystal_Powder,
        LocationName.Loho_Mythril_Silver,
        LocationName.Loho_Golem_Core,
        LocationName.Loho_Golem_Core_Two,
        LocationName.Lull,
        LocationName.Loho_Ship_Cannon,
    ]),
    RegionName.AngaraCavern: RegionData(RegionName.AngaraCavern,
    [
        LocationName.Angara_Cavern_Haures
    ]),
    RegionName.KaltIsland: RegionData(RegionName.KaltIsland,
    [
        LocationName.Gel
    ]),
    RegionName.Prox: RegionData(RegionName.Prox,
    [
        LocationName.Dew, #Random djinn from Gs1 spot
        LocationName.Prox_Cookie,
        LocationName.Prox_Potion,
        LocationName.Prox_Dark_Matter,
        LocationName.Prox_Sacred_Feather,
        LocationName.Mold
    ],
    [
        EntranceName.ProxToMarsLighthouse
    ]),
    RegionName.MarsLighthouse: RegionData(RegionName.MarsLighthouse,
    [
        LocationName.Mars_Lighthouse_Mars_Star,
        LocationName.Mars_Lighthouse_Sol_Blade,
        LocationName.Mars_Lighthouse_Apple,
        LocationName.Mars_Lighthouse_Mimic,
        LocationName.Mars_Lighthouse_Orihalcon,
        LocationName.Mars_Lighthouse_Valkyrie_Mail,
        LocationName.Mars_Lighthouse_Flame_Dragons,
        LocationName.Mars_Lighthouse_Teleport_Lapis,
        LocationName.Balm,
        LocationName.Mars_Lighthouse_Heated,
    ],
    [
        EntranceName.MarsLighthouseToMarsLighthouse_Activated
    ]),
    RegionName.MarsLighthouse_Activated: RegionData(RegionName.MarsLighthouse_Activated,
    [
        LocationName.Fugue,
        LocationName.Mars_Lighthouse_Alastors_Hood,
        LocationName.Mars_Lighthouse_Psy_Crystal,
        LocationName.Mars_Lighthouse_Doom_Dragon,
    ])
}