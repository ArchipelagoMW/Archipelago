import typing
from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType
from worlds.gstla.Locations import GSTLALocation, location_name_to_id
from . import ItemType
from .Names.LocationName import LocationName
from .Names.RegionName import RegionName
from .Names.ItemName import ItemName
def create_region(multiworld: MultiWorld, player: int, name: str, locations: typing.List[str]):
    region = Region(name, player, multiworld)
    for location in locations:

        location_data = location_name_to_id.get(location, None)
        if location_data is None:
            loc = GSTLALocation(player, location, None, region)
        else:
            loc = GSTLALocation(player, location, location_data.id, region)

        region.locations.append(loc)
    multiworld.regions.append(region)


def create_connect(world: MultiWorld, player: int, source: str, target: str, rule: callable = lambda state: True, one_way=False, name=None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if name is None:
        name = source + " to " + target

    connection = Entrance(
        player,
        name,
        source_region
    )

    connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    if not one_way:
        create_connect(world, player, target, source, rule, True)


def create_regions(multiworld: MultiWorld, player: int):
    create_region(multiworld, player, RegionName.Menu, [])

    create_region(multiworld, player, RegionName.Idejima, [
        LocationName.Idejima_Mind_Read,
        LocationName.Idejima_Whirlwind,
        LocationName.Idejima_Growth,
        LocationName.Idejima_Shamans_Rod
    ])

    create_region(multiworld, player, RegionName.Daila,
    [
        LocationName.Daila_Herb,
        LocationName.Daila_3_coins,
        LocationName.Daila_12_coins,
        LocationName.Daila_Psy_Crystal,
        LocationName.Daila_Sleep_Bomb,
        LocationName.Daila_Sea_Gods_Tear,
        LocationName.Daila_Smoke_Bomb,
        LocationName.Echo
    ])

    create_region(multiworld, player, RegionName.KandoreamTemple,
    [
        LocationName.Kandorean_Temple_Mimic,
        LocationName.Kandorean_Temple_Lash_Pebble,
        LocationName.Kandorean_Temple_Mysterious_Card,
        LocationName.Kandorean_Temple_Chestbeaters,
        LocationName.Fog
    ])

    create_region(multiworld, player, RegionName.ShrineOfTheSeaGod, [
        LocationName.Breath,
        LocationName.Shrine_of_the_Sea_God_Rusty_Staff,
        LocationName.Shrine_of_the_Sea_God_Right_Prong
    ])

    create_region(multiworld, player, RegionName.DehkanPlateau,
    [
        LocationName.Dehkan_Plateau_Elixir,
        LocationName.Dehkan_Plateau_Pound_Cube,
        LocationName.Dehkan_Plateau_Themis_Axe,
        LocationName.Dehkan_Plateau_Full_Metal_Vest,
        LocationName.Dehkan_Plateau_Mint,
        LocationName.Dehkan_Plateau_Nut,
        LocationName.Cannon
    ])


    create_region(multiworld, player, RegionName.IndraCavern,
    [
        LocationName.Indra_Cavern_Zagan
    ])

    create_region(multiworld, player, RegionName.Madra,
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
    ])

    create_region(multiworld, player, RegionName.MadraCatacombs,
    [
        LocationName.Madra_Catacombs_Ruin_Key,
        LocationName.Madra_Catacombs_Tremor_Bit,
        LocationName.Madra_Catacombs_Apple,
        LocationName.Madra_Catacombs_Lucky_Medal,
        LocationName.Madra_Catacombs_Mist_Potion,
        LocationName.Madra_Catacombs_Moloch
    ])

    #West Osenia
    create_region(multiworld, player, RegionName.OseniaCliffs,
    [
        LocationName.Osenia_Cliffs_Pirates_Sword
    ])


    create_region(multiworld, player, RegionName.YampiDesertFront,
    [
        LocationName.Yampi_Desert_Antidote,
        LocationName.Yampi_Desert_Guardian_Ring,
        LocationName.Yampi_Desert_Scoop_Gem,
        LocationName.Yampi_Desert_King_Scorpion,
        LocationName.Blitz
    ])

    create_region(multiworld, player, RegionName.YampiDesertBack,
    [
        LocationName.Yampi_Desert_Lucky_Medal,
        LocationName.Yampi_Desert_Trainers_Whip,
        LocationName.Yampi_Desert_Hard_Nut,
        LocationName.Yampi_Desert_Blow_Mace,
        LocationName.Yampi_Desert_315_coins,
        LocationName.Yampi_Desert_Cave_Water_of_Life
    ])

    create_region(multiworld, player, RegionName.YampiDesertCave,
    [
        LocationName.Yampi_Desert_Cave_Orihalcon,
        LocationName.Yampi_Desert_Cave_Dark_Matter,
        LocationName.Yampi_Desert_Cave_Mythril_Silver,
        LocationName.Yampi_Desert_Cave_Valukar,
        LocationName.Yampi_Desert_Cave_Daedalus,
        LocationName.Crystal
    ])
    create_region(multiworld, player, RegionName.Alhafra,
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
    ])

    create_region(multiworld, player, RegionName.AlhafraCave,
    [
        LocationName.Alhafran_Cave_123_coins,
        LocationName.Alhafran_Cave_Ixion_Mail,
        LocationName.Alhafran_Cave_Lucky_Medal,
        LocationName.Alhafran_Cave_Power_Bread,
        LocationName.Alhafran_Cave_777_coins,
        LocationName.Alhafran_Cave_Potion,
        LocationName.Alhafran_Cave_Psy_Crystal
    ])
    create_region(multiworld, player, RegionName.Mikasalla,
    [
        LocationName.Mikasalla_Nut,
        LocationName.Mikasalla_Herb,
        LocationName.Mikasalla_Elixir,
        LocationName.Mikasalla_82_coins,
        LocationName.Mikasalla_Lucky_Pepper,
        LocationName.Sour,
        LocationName.Spark
    ])

    create_region(multiworld, player, RegionName.Garoh,
    [
        LocationName.Garoh_Nut,
        LocationName.Garoh_Elixir,
        LocationName.Garoh_Sleep_Bomb,
        LocationName.Garoh_Smoke_Bomb,
        LocationName.Garoh_Hypnos_Sword,
        LocationName.Ether
    ])
    create_region(multiworld, player, RegionName.AirsRock,
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
        LocationName.Airs_Rock_VialTwo,
        LocationName.Airs_Rock_VialThree,
        LocationName.Airs_Rock_Flora,
        LocationName.Airs_Rock_Reveal
    ])
    create_region(multiworld, player, RegionName.OseniaCavern, [
        LocationName.Osenia_Cavern_Megaera
    ])

    #South East Gondowan
    create_region(multiworld, player, RegionName.GondowanCliffs,
    [
        LocationName.Gondowan_Cliffs_Healing_Fungus,
        LocationName.Gondowan_Cliffs_Laughing_Fungus,
        LocationName.Gondowan_Cliffs_Sleep_Bomb,
        LocationName.Kindle
    ])

    create_region(multiworld, player, RegionName.Naribwe,
    [
        LocationName.Naribwe_Elixir,
        LocationName.Naribwe_18_coins,
        LocationName.Naribwe_Sleep_Bomb,
        LocationName.Naribwe_Thorn_Crown,
        LocationName.Naribwe_Unicorn_Ring,
        LocationName.Chill
    ])

    create_region(multiworld, player, RegionName.KibomboMountains,
    [
        LocationName.Kibombo_Mountains_Disk_Axe,
        LocationName.Kibombo_Mountains_Power_Bread,
        LocationName.Kibombo_Mountains_Smoke_Bomb,
        LocationName.Kibombo_Mountains_Tear_Stone,
        LocationName.Waft
    ])

    create_region(multiworld, player, RegionName.Kibombo,
    [
        LocationName.Kibombo_Lucky_Medal,
        LocationName.Kibombo_Lucky_Pepper,
        LocationName.Kibombo_Nut,
        LocationName.Kibombo_Douse_Drop,
        LocationName.Kibombo_Frost_Jewel,
        LocationName.Spring,
        LocationName.Shade
    ])

    create_region(multiworld, player, RegionName.GabombaStatue,
    [
        LocationName.Gabomba_Statue_Black_Crystal,
        LocationName.Gabomba_Statue_Mimic,
        LocationName.Gabomba_Statue_Elixir,
        LocationName.Gabomba_Statue_Bone_Armlet,
        LocationName.Gabombo_Statue,
        LocationName.Steel
    ])

    create_region(multiworld, player, RegionName.GabombaCatacombs,
    [
        LocationName.Gabomba_Catacombs_Mint,
        LocationName.Gabomba_Catacombs_Tomegathericon,
        LocationName.Mud
    ])

    create_region(multiworld, player, RegionName.Lemurian_Ship,
    [
        LocationName.Lemurian_Ship_Elixir,
        LocationName.Lemurian_Ship_Potion,
        LocationName.Lemurian_Ship_Oil_Drop,
        LocationName.Lemurian_Ship_Antidote,
        LocationName.Lemurian_Ship_Mist_Potion,
        LocationName.Lemurian_Ship_Aqua_Hydra,
        #todo, when not start with ship, get ship from this location LocationName.Lemurian_Ship_Engine
    ])

    #Eastern Sea
    create_region(multiworld, player, RegionName.EasternSea, [])

    create_region(multiworld, player, RegionName.EastTundariaIslet,
    [
        LocationName.E_Tundaria_Islet_Lucky_Medal,
        LocationName.E_Tundaria_Islet_Pretty_Stone
    ])

    create_region(multiworld, player, RegionName.WestIndraIslet,
    [
        LocationName.W_Indra_Islet_Lucky_Medal,
        LocationName.W_Indra_Islet_Lil_Turtle
    ])

    create_region(multiworld, player, RegionName.SouthEastAngaraIslet,
    [
        LocationName.SE_Angara_Islet_Lucky_Medal,
        LocationName.SE_Angara_Islet_Red_Cloth
    ])

    create_region(multiworld, player, RegionName.NorthOseniaIslet,
    [
        LocationName.N_Osenia_Islet_Lucky_Medal,
        LocationName.N_Osenia_Islet_Milk
    ])

    create_region(multiworld, player, RegionName.SeaOfTimeIslet,
    [
        LocationName.Sea_of_Time_Islet_Lucky_Medal
    ])

    create_region(multiworld, player, RegionName.IsletCave,
    [
        LocationName.Islet_Cave_Turtle_Boots,
        LocationName.Islet_Cave_Rusty_Staff,
        LocationName.Islet_Cave_Sentinel,
        LocationName.Islet_Cave_Catastrophe,
        LocationName.Meld,
        LocationName.Serac
    ])

    create_region(multiworld, player, RegionName.ApojiiIslands,
    [
        LocationName.Apojii_Islands_Herb,
        LocationName.Apojii_Islands_Mint,
        LocationName.Apojii_Islands_32_coins,
        LocationName.Apojii_Islands_182_coins,
        LocationName.Apojii_Islands_Bramble_Seed,
        LocationName.Haze
    ])

    create_region(multiworld, player, RegionName.AquaRock,
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
    ])

    create_region(multiworld, player, RegionName.Izumo,
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
    ])

    create_region(multiworld, player, RegionName.GaiaRock,
    [
        LocationName.Gaia_Rock_Nut,
        LocationName.Gaia_Rock_Apple,
        LocationName.Gaia_Rock_Mimic,
        LocationName.Gaia_Rock_Rusty_Mace,
        LocationName.Gaia_Rock_Cloud_Brand,
        LocationName.Gaia_Rock_Dancing_Idol,
        LocationName.Gaia_Rock_Serpent,
        LocationName.Gaia_Rock_Sand
    ])

    create_region(multiworld, player, RegionName.TreasureIsland, [
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
    ])

    create_region(multiworld, player, RegionName.TreasureIsland_Grindstone,
    [
        LocationName.Treasure_Isle_911_coins,
        LocationName.Treasure_Isle_Psy_Crystal,
        LocationName.Treasure_Isle_Cookie,
        LocationName.Treasure_Isle_Sylph_Feather,
        LocationName.Treasure_Isle_Rusty_Axe,
        LocationName.Treasure_Isle_Star_Dust,
        LocationName.Treasure_Isle_Jesters_Armlet,
        LocationName.Treasure_Isle_Mimic,
    ])

    create_region(multiworld, player, RegionName.TreasureIsland_PostReunion,
    [
        LocationName.Bane,  # Random Venus djinn from Gs1
        LocationName.Gale,
        LocationName.Treasure_Isle_Iris_Robe,
        LocationName.Treasure_Isle_Fire_Brand,
        LocationName.Treasure_Isle_Star_Magican,
        LocationName.Treasure_Isle_Azul,
    ])

    create_region(multiworld, player, RegionName.TundariaTower,
    [
        LocationName.Tundaria_Tower_Center_Prong,
        LocationName.Wheeze,
    ])

    create_region(multiworld, player, RegionName.TundariaTower_Parched,
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
    ])

    create_region(multiworld, player, RegionName.AnkohlRuins,
    [
        LocationName.Ankohl_Ruins_Empty,
        LocationName.Ankohl_Ruins_Empty_Two,
        LocationName.Ankohl_Ruins_Empty_Three,
        LocationName.Ankohl_Ruins_Empty_Four,
        LocationName.Ankohl_Ruins_Empty_Five,
        LocationName.Ankohl_Ruins_Empty_Six,
        LocationName.Ankohl_Ruins_210_coins,
        LocationName.Ankohl_Ruins_Crystal_Powder
    ])

    create_region(multiworld, player, RegionName.AnkohlRuins_Sand,
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
    ])

    create_region(multiworld, player, RegionName.Champa,
    [
        LocationName.Champa_Elixir,
        LocationName.Champa_Trident,
        LocationName.Champa_12_coins,
        LocationName.Champa_Sleep_Bomb,
        LocationName.Champa_Smoke_Bomb,
        LocationName.Champa_Lucky_Medal,
        LocationName.Champa_Viking_Helm,
        LocationName.Champa_Avimander
    ])

    create_region(multiworld, player, RegionName.Yallam,
    [
        LocationName.Yallam_Nut,
        LocationName.Yallam_Elixir,
        LocationName.Yallam_Antidote,
        LocationName.Yallam_Masamune,
        LocationName.Yallam_Oil_Drop,
        LocationName.Yallam_16_coins
    ])

    create_region(multiworld, player, RegionName.TaopoSwamp,
    [
        LocationName.Taopo_Swamp_Vial,
        LocationName.Taopo_Swamp_Cookie,
        LocationName.Taopo_Swamp_Star_Dust,
        LocationName.Taopo_Swamp_Bramble_Seed,
        LocationName.Taopo_Swamp_Tear_Stone,
        LocationName.Taopo_Swamp_Tear_Stone_Two,
        LocationName.Flower
    ])

    create_region(multiworld, player, RegionName.SeaOfTime,
    [
        LocationName.SeaOfTime_Poseidon
    ])

    create_region(multiworld, player, RegionName.Lemuria,
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
    ])

    #Western Sea
    create_region(multiworld, player, RegionName.WesternSea, [])

    create_region(multiworld, player, RegionName.SouthWestAttekaIslet,
    [
        LocationName.Luff, # Random djinn from gs1 spot
        LocationName.SW_Atteka_Islet_Dragon_Skin
    ])

    create_region(multiworld, player, RegionName.HesperiaSettlement,
    [
        LocationName.Hesperia_Settlement_166_coins,
        LocationName.Tinder
    ])

    create_region(multiworld, player, RegionName.ShamanVillageCave,
    [
        LocationName.Petra,
        LocationName.Eddy
    ])

    create_region(multiworld, player, RegionName.ShamanVillage,
    [
        LocationName.Shaman_Village_Elixir,
        LocationName.Shaman_Village_Spirit_Gloves,
        LocationName.Shaman_Village_Hard_Nut,
        LocationName.Shaman_Village_Lucky_Medal,
        LocationName.Shaman_Village_Lucky_Pepper,
        LocationName.Shaman_Village_Weasels_Claw,
        LocationName.Shaman_Village_Moapa,
        LocationName.Shaman_Village_Hover_Jade,
        LocationName.Aroma,
        LocationName.Gasp
    ])

    create_region(multiworld, player, RegionName.AttekaInlet,
    [
        LocationName.Atteka_Inlet_Vial,
        LocationName.Geode
    ])

    create_region(multiworld, player, RegionName.Contigo,
    [
        LocationName.Contigo_Corn,
        LocationName.Contigo_Bramble_Seed,
        LocationName.Contigo_Dragon_Skin,
        LocationName.Contigo_Power_Bread,
        LocationName.Salt,
        LocationName.Core,
        LocationName.Shine,
    ])

    create_region(multiworld, player, RegionName.JupiterLighthouse,
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
    ])

    create_region(multiworld, player, RegionName.Reunion,
    [
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
        LocationName.Squall,
    ])

    create_region(multiworld, player, RegionName.AttekaCavern,
    [
        LocationName.Atteka_Cavern_Coatlicue
    ])

    create_region(multiworld, player, RegionName.AnemosSanctum,
    [
        LocationName.Anemos_Inner_Sanctum_Orihalcon,
        LocationName.Anemos_Inner_Sanctum_Dark_Matter,
        LocationName.Anemos_Inner_Sanctum_Dullahan,
        LocationName.Anemos_Inner_Sanctum_Charon,
        LocationName.Anemos_Inner_Sanctum_Iris
    ])

    create_region(multiworld, player, RegionName.GondowanSettlement,
    [
        LocationName.Gondowan_Settlement_Lucky_Medal,
        LocationName.Gondowan_Settlement_Star_Dust
    ])

    create_region(multiworld, player, RegionName.MagmaRock,
    [
        LocationName.Magma_Rock_Mimic,
        LocationName.Magma_Rock_Salamander_Tail,
        LocationName.Magma_Rock_383_coins,
        LocationName.Magma_Rock_Oil_Drop
    ])

    create_region(multiworld, player, RegionName.MagmaRockInterior,
    [
        LocationName.Torch,  # Random djinn from gs1 spot
        LocationName.Fury,
        LocationName.Magma_Rock_Lucky_Medal,
        LocationName.Magma_Rock_Mist_Potion,
        LocationName.Magma_Rock_Salamander_Tail_Two,
        LocationName.Magma_Rock_Golem_Core,
        LocationName.Magma_Rock_Blaze,
        LocationName.Magma_Rock_Magma_Ball
    ])

    create_region(multiworld, player, RegionName.Loho,
    [
        LocationName.Loho_Crystal_Powder,
        LocationName.Loho_Mythril_Silver,
        LocationName.Loho_Golem_Core,
        LocationName.Loho_Golem_Core_Two,
        LocationName.Lull
    ])
    create_region(multiworld, player, RegionName.AngaraCavern,
    [
        LocationName.Angara_Cavern_Haures
    ])

    create_region(multiworld, player, RegionName.KaltIsland,
    [
        LocationName.Gel
    ])

    create_region(multiworld, player, RegionName.Prox,
    [
        LocationName.Dew, #Random djinn from Gs1 spot
        LocationName.Prox_Cookie,
        LocationName.Prox_Potion,
        LocationName.Prox_Dark_Matter,
        LocationName.Prox_Sacred_Feather,
        LocationName.Mold
    ])

    create_region(multiworld, player, RegionName.MarsLighthouse,
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
    ])

    create_region(multiworld, player, RegionName.MarsLighthouse_Activated,
    [
        LocationName.Fugue,
        LocationName.Mars_Lighthouse_Alastors_Hood,
        LocationName.Mars_Lighthouse_Psy_Crystal,
        LocationName.Mars_Lighthouse_Doom_Dragon
    ])


    create_connect(multiworld, player, RegionName.Menu, RegionName.Idejima)
    create_connect(multiworld, player, RegionName.Idejima, RegionName.Daila)
    create_connect(multiworld, player, RegionName.Daila, RegionName.ShrineOfTheSeaGod, lambda state: state.has(ItemName.Lash_Pebble, player))
    create_connect(multiworld, player, RegionName.Daila, RegionName.KandoreamTemple, lambda state: state.has(ItemName.Whirlwind, player))
    create_connect(multiworld, player, RegionName.Daila, RegionName.DehkanPlateau)

    create_connect(multiworld, player, RegionName.DehkanPlateau, RegionName.Madra)
    create_connect(multiworld, player, RegionName.Madra, RegionName.MadraCatacombs, lambda state: state.has(ItemName.Reveal, player))
    create_connect(multiworld, player, RegionName.Madra, RegionName.IndraCavern)

    create_connect(multiworld, player, RegionName.Lemuria, RegionName.Lemurian_Ship, one_way=True)
    create_connect(multiworld, player, RegionName.AttekaInlet, RegionName.Lemurian_Ship, one_way=True)

    create_connect(multiworld, player, RegionName.Madra, RegionName.OseniaCliffs)
    create_connect(multiworld, player, RegionName.OseniaCliffs, RegionName.Mikasalla)
    create_connect(multiworld, player, RegionName.Mikasalla, RegionName.YampiDesertFront)
    create_connect(multiworld, player, RegionName.YampiDesertFront, RegionName.YampiDesertBack, lambda state: state.has(ItemName.Scoop_Gem, player))
    create_connect(multiworld, player, RegionName.YampiDesertBack, RegionName.YampiDesertCave, lambda state: state.has(ItemName.Sand, player) and state.has(ItemName.Teleport_Lapis, player) and state.has(ItemName.Burst_Brooch, player))
    create_connect(multiworld, player, RegionName.YampiDesertBack, RegionName.Alhafra)
    create_connect(multiworld, player, RegionName.Alhafra, RegionName.AlhafraCave, lambda state: (state.has(ItemName.Briggs_defeated, player) and state.has(ItemName.Tremor_Bit, player)) or state.has(ItemName.Briggs_escaped, player))
    create_connect(multiworld, player, RegionName.Mikasalla, RegionName.Garoh)
    create_connect(multiworld, player, RegionName.Mikasalla, RegionName.OseniaCavern)
    create_connect(multiworld, player, RegionName.Garoh, RegionName.AirsRock, lambda state: state.has(ItemName.Whirlwind, player))
    create_connect(multiworld, player, RegionName.Garoh, RegionName.YampiDesertBack, lambda state: state.has(ItemName.Sand, player))

    create_connect(multiworld, player, RegionName.Madra, RegionName.GondowanCliffs, lambda state: state.has(ItemName.Frost_Jewel, player) or state.has(ItemName.Scoop_Gem, player), True)
    create_connect(multiworld, player, RegionName.GondowanCliffs, RegionName.Madra, one_way=True)
    create_connect(multiworld, player, RegionName.GondowanCliffs, RegionName.Naribwe, lambda state: state.has(ItemName.Briggs_defeated), True)
    create_connect(multiworld, player, RegionName.Naribwe, RegionName.GondowanCliffs, one_way=True)

    create_connect(multiworld, player, RegionName.Naribwe, RegionName.KibomboMountains)
    create_connect(multiworld, player, RegionName.KibomboMountains, RegionName.Kibombo, lambda state: state.has(ItemName.Frost_Jewel, player) or state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Whirlwind, player), True)
    create_connect(multiworld, player, RegionName.Kibombo, RegionName.KibomboMountains, one_way=True)
    create_connect(multiworld, player, RegionName.Kibombo, RegionName.GabombaStatue, lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Scoop_Gem, player))
    create_connect(multiworld, player, RegionName.GabombaStatue, RegionName.GabombaCatacombs, lambda state: state.has(ItemName.Gabombo_Statue_Completed, player) and state.has(ItemName.Cyclone_Chip, player))


    create_connect(multiworld, player, RegionName.Daila, RegionName.EasternSea, lambda state: state.has(ItemName.Ship, player))
    create_connect(multiworld, player, RegionName.Madra, RegionName.EasternSea, lambda state: state.has(ItemName.Ship, player))
    create_connect(multiworld, player, RegionName.Mikasalla, RegionName.EasternSea, lambda state: state.has(ItemName.Ship, player))
    create_connect(multiworld, player, RegionName.Naribwe, RegionName.EasternSea, lambda state: state.has(ItemName.Ship, player))
    create_connect(multiworld, player, RegionName.Kibombo, RegionName.EasternSea, lambda state: state.has(ItemName.Ship, player))
    create_connect(multiworld, player, RegionName.Alhafra, RegionName.EasternSea, lambda state: state.has(ItemName.Ship, player))


    create_connect(multiworld, player, RegionName.EasternSea, RegionName.WestIndraIslet)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.NorthOseniaIslet)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.SouthEastAngaraIslet)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.SeaOfTimeIslet)
    create_connect(multiworld, player, RegionName.SeaOfTimeIslet, RegionName.IsletCave, lambda state: state.has(ItemName.Mind_Read, player) and state.has(ItemName.Lil_Turtle, player))

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.SeaOfTime)
    create_connect(multiworld, player, RegionName.SeaOfTime, RegionName.Lemuria, lambda state: state.has(ItemName.Poseidon_defeated, player) or state.has(ItemName.Grindstone, player))

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.TreasureIsland)
    create_connect(multiworld, player, RegionName.TreasureIsland, RegionName.TreasureIsland_Grindstone, lambda state: state.has(ItemName.Grindstone, player))
    create_connect(multiworld, player, RegionName.TreasureIsland_Grindstone, RegionName.TreasureIsland_PostReunion, lambda state: state.has(ItemName.Lifting_Gem, player))

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Champa)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.AnkohlRuins)
    create_connect(multiworld, player, RegionName.AnkohlRuins, RegionName.AnkohlRuins_Sand, lambda state: state.has(ItemName.Sand, player))

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Izumo)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.GaiaRock)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.ApojiiIslands)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.AquaRock, lambda state: state.has(ItemName.Douse_Drop, player))

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Yallam)
    create_connect(multiworld, player, RegionName.Yallam, RegionName.TaopoSwamp)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.EastTundariaIslet)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.TundariaTower)
    create_connect(multiworld, player, RegionName.TundariaTower, RegionName.TundariaTower_Parched, lambda state: state.has(ItemName.Parch, player))


    create_connect(multiworld, player, RegionName.EasternSea, RegionName.WesternSea, lambda state: state.has(ItemName.Grindstone, player))


    create_connect(multiworld, player, RegionName.WesternSea, RegionName.MagmaRock, lambda state: state.has(ItemName.Lifting_Gem, player))
    create_connect(multiworld, player, RegionName.MagmaRock, RegionName.MagmaRockInterior, lambda state: state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Growth, player) and state.has(ItemName.Lash_Pebble, player))
    create_connect(multiworld, player, RegionName.WesternSea, RegionName.GondowanSettlement)

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.SouthWestAttekaIslet)


    create_connect(multiworld, player, RegionName.WesternSea, RegionName.AttekaInlet)
    create_connect(multiworld, player, RegionName.AttekaInlet, RegionName.Contigo)
    create_connect(multiworld, player, RegionName.Contigo, RegionName.AnemosSanctum, lambda state: state.has(ItemName.Teleport_Lapis, player) and state.count_group(ItemType.Djinn, player) >= 72)
    create_connect(multiworld, player, RegionName.Contigo, RegionName.JupiterLighthouse, lambda state: state.has(ItemName.Cyclone_Chip, player))
    create_connect(multiworld, player, RegionName.Contigo, RegionName.Reunion, lambda state: state.has(ItemName.Jupiter_Beacon_Lit, player))

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.AttekaCavern, lambda state: state.has(ItemName.Jupiter_Beacon_Lit, player))

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.Loho)
    create_connect(multiworld, player, RegionName.WesternSea, RegionName.AngaraCavern)

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.HesperiaSettlement)
    create_connect(multiworld, player, RegionName.WesternSea, RegionName.ShamanVillageCave)
    create_connect(multiworld, player, RegionName.ShamanVillageCave, RegionName.ShamanVillage, lambda state: state.has(ItemName.Whirlwind, player))

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.KaltIsland)

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.Prox, lambda state: state.has(ItemName.Magma_Ball, player))
    create_connect(multiworld, player, RegionName.Prox, RegionName.MarsLighthouse)
    create_connect(multiworld, player, RegionName.MarsLighthouse, RegionName.MarsLighthouse_Activated, lambda state: state.has(ItemName.Flamedragons_defeated, player) and state.has(ItemName.Mars_Star, player))