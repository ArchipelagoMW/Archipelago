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
        LocationName.Yampi_Desert_315_coins
    ])
    create_region(multiworld, player, RegionName.YampiDesertCave,
    [
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
        LocationName.Mud
    ])

    #Eastern Sea
    create_region(multiworld, player, RegionName.EasternSea, [])

    create_region(multiworld, player, RegionName.WestIndraIslet, [])

    create_region(multiworld, player, RegionName.NorthOseniaIslet, [])
    create_region(multiworld, player, RegionName.SouthEastAngaraIslet, [])
    create_region(multiworld, player, RegionName.SeaOfTimeIslet, [])
    create_region(multiworld, player, RegionName.IsletCave,
    [
        LocationName.Islet_Cave_Catastrophe,
        LocationName.Meld,
        LocationName.Serac
    ])

    create_region(multiworld, player, RegionName.Champa, [])
    create_region(multiworld, player, RegionName.AnkohlRuins, [])

    create_region(multiworld, player, RegionName.Yallam, [])
    create_region(multiworld, player, RegionName.TaopoSwamp,
    [
        LocationName.Flower
    ])

    create_region(multiworld, player, RegionName.TundariaTower,
    [
        LocationName.Tundaria_Tower_Burst_Brooch,
        LocationName.Wheeze,
        LocationName.Reflux
    ])

    create_region(multiworld, player, RegionName.EastTundariaIslet, [])

    create_region(multiworld, player, RegionName.SeaOfTime, [])

    create_region(multiworld, player, RegionName.Lemuria,
    [
        LocationName.Lemuria_Eclipse,
        LocationName.Lemuria_Grindstone,
        LocationName.Rime
    ])

    create_region(multiworld, player, RegionName.ApojiiIslands,
    [
        LocationName.Haze
    ])

    create_region(multiworld, player, RegionName.AquaRock,
    [
        LocationName.Aqua_Rock_Parch,
        LocationName.Steam
    ])

    create_region(multiworld, player, RegionName.Izumo,
    [
        LocationName.Izumo_Ulysses,
        LocationName.Coal
    ])

    create_region(multiworld, player, RegionName.GaiaRock,
    [
        LocationName.Gaia_Rock_Sand
    ])

    create_region(multiworld, player, RegionName.TreasureIsland, [
        LocationName.Treasure_Isle_Azul,
        LocationName.Gale
    ])

    #Western Sea
    create_region(multiworld, player, RegionName.WesternSea, [])

    create_region(multiworld, player, RegionName.GondowanSettlement, [])
    create_region(multiworld, player, RegionName.MagmaRock, [
        LocationName.Magma_Rock_Blaze,
        LocationName.Fury
    ])

    create_region(multiworld, player, RegionName.Loho,
    [
        LocationName.Lull
    ])
    create_region(multiworld, player, RegionName.AngaraCavern,
    [
        LocationName.Angara_Cavern_Haures
    ])


    create_region(multiworld, player, RegionName.ShamanVillageCave,
    [
        LocationName.Petra,
        LocationName.Eddy
    ])
    create_region(multiworld, player, RegionName.ShamanVillage,
    [
        LocationName.Shaman_Village_Hover_Jade,
        LocationName.Aroma,
        LocationName.Whorl,
        LocationName.Gasp
    ])

    create_region(multiworld, player, RegionName.HesperiaSettlement,
    [
        LocationName.Tinder
    ])


    create_region(multiworld, player, RegionName.AttekaInlet,
    [
        LocationName.Geode
    ])
    create_region(multiworld, player, RegionName.AttekaCavern,
    [
        LocationName.Atteka_Cavern_Coatlicue
    ])
    create_region(multiworld, player, RegionName.Contigo,
    [
        LocationName.Contigo_Carry_Stone,
        LocationName.Contigo_Lifting_Gem,
        LocationName.Contigo_Orb_of_Force,
        LocationName.Contigo_Catch_Beads,
        LocationName.Salt,
        LocationName.Core,
        LocationName.Shine,
        LocationName.Flint,
        LocationName.Granite,
        LocationName.Quartz,
        LocationName.Vine,
        LocationName.Sap,
        LocationName.Ground,
        LocationName.Bane,
        LocationName.Fizz,
        LocationName.Sleet,
        LocationName.Mist,
        LocationName.Spritz,
        LocationName.Hail,
        LocationName.Tonic,
        LocationName.Dew,
        LocationName.Forge,
        LocationName.Fever,
        LocationName.Corona,
        LocationName.Scorch,
        LocationName.Ember,
        LocationName.Flash,
        LocationName.Torch,
        LocationName.Gust,
        LocationName.Breeze,
        LocationName.Zephyr,
        LocationName.Smog,
        LocationName.Kite,
        LocationName.Squall,
        LocationName.Luff
    ])
    create_region(multiworld, player, RegionName.JupiterLighthouse, [])
    create_region(multiworld, player, RegionName.AnemosSanctum,
    [
        LocationName.Anemos_Inner_Sanctum_Charon,
        LocationName.Anemos_Inner_Sanctum_Iris
    ])

    create_region(multiworld, player, RegionName.SouthWestAttekaIslet, [])

    create_region(multiworld, player, RegionName.KaltIsland,
    [
        LocationName.Gel
    ])

    create_region(multiworld, player, RegionName.Prox,
    [
        LocationName.Mold
    ])
    create_region(multiworld, player, RegionName.MarsLighthouse,
    [
        LocationName.Mars_Lighthouse_Doom_Dragon,
        LocationName.Mars_Lighthouse_Teleport_Lapis,
        LocationName.Balm,
        LocationName.Fugue
    ])



    create_connect(multiworld, player, RegionName.Menu, RegionName.Idejima)
    create_connect(multiworld, player, RegionName.Idejima, RegionName.Daila)
    create_connect(multiworld, player, RegionName.Daila, RegionName.ShrineOfTheSeaGod, lambda state: state.has(ItemName.Lash_Pebble, player))
    create_connect(multiworld, player, RegionName.Daila, RegionName.KandoreamTemple, lambda state: state.has(ItemName.Whirlwind, player))
    create_connect(multiworld, player, RegionName.Daila, RegionName.DehkanPlateau)

    create_connect(multiworld, player, RegionName.DehkanPlateau, RegionName.Madra)
    create_connect(multiworld, player, RegionName.Madra, RegionName.MadraCatacombs, lambda state: state.has(ItemName.Reveal, player))
    create_connect(multiworld, player, RegionName.Madra, RegionName.IndraCavern)

    create_connect(multiworld, player, RegionName.Madra, RegionName.OseniaCliffs)
    create_connect(multiworld, player, RegionName.OseniaCliffs, RegionName.Mikasalla)
    create_connect(multiworld, player, RegionName.Mikasalla, RegionName.YampiDesertFront)
    create_connect(multiworld, player, RegionName.YampiDesertFront, RegionName.YampiDesertBack, lambda state: state.has(ItemName.Scoop_Gem, player))
    create_connect(multiworld, player, RegionName.YampiDesertBack, RegionName.YampiDesertCave, lambda state: state.has(ItemName.Sand, player) and state.has(ItemName.Reveal, player))
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
    create_connect(multiworld, player, RegionName.GabombaStatue, RegionName.GabombaCatacombs)


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
    create_connect(multiworld, player, RegionName.SeaOfTimeIslet, RegionName.IsletCave)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.SeaOfTime)
    create_connect(multiworld, player, RegionName.SeaOfTime, RegionName.Lemuria)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.TreasureIsland)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Champa)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.AnkohlRuins)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Izumo)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.GaiaRock)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.ApojiiIslands)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.AquaRock, lambda state: state.has(ItemName.Douse_Drop, player))

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Yallam)
    create_connect(multiworld, player, RegionName.Yallam, RegionName.TaopoSwamp)

    create_connect(multiworld, player, RegionName.EasternSea, RegionName.EastTundariaIslet)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.TundariaTower)


    create_connect(multiworld, player, RegionName.EasternSea, RegionName.WesternSea, lambda state: state.has(ItemName.Grindstone, player))


    create_connect(multiworld, player, RegionName.WesternSea, RegionName.MagmaRock, lambda state: state.has(ItemName.Lifting_Gem, player))
    create_connect(multiworld, player, RegionName.WesternSea, RegionName.GondowanSettlement)

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.SouthWestAttekaIslet)


    create_connect(multiworld, player, RegionName.WesternSea, RegionName.AttekaInlet)
    create_connect(multiworld, player, RegionName.AttekaInlet, RegionName.Contigo)
    create_connect(multiworld, player, RegionName.Contigo, RegionName.AnemosSanctum, lambda state: state.has(ItemName.Teleport_Lapis, player) and state.count_group(ItemType.Djinn, player) >= 72)
    create_connect(multiworld, player, RegionName.Contigo, RegionName.JupiterLighthouse, lambda state: state.has(ItemName.Cyclone_Chip, player))
    create_connect(multiworld, player, RegionName.WesternSea, RegionName.AttekaCavern)


    create_connect(multiworld, player, RegionName.WesternSea, RegionName.Loho)
    create_connect(multiworld, player, RegionName.WesternSea, RegionName.AngaraCavern)

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.HesperiaSettlement)
    create_connect(multiworld, player, RegionName.WesternSea, RegionName.ShamanVillageCave)
    create_connect(multiworld, player, RegionName.ShamanVillageCave, RegionName.ShamanVillage)

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.KaltIsland)

    create_connect(multiworld, player, RegionName.WesternSea, RegionName.Prox)
    create_connect(multiworld, player, RegionName.Prox, RegionName.MarsLighthouse)