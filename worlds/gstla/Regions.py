import typing
from BaseClasses import MultiWorld, Region, Entrance, LocationProgressType
from worlds.gstla.Locations import GSTLALocation, location_name_to_id
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

    create_region(multiworld, player, RegionName.Idejima, [])

    create_region(multiworld, player, RegionName.EasternSea,
    [
            LocationName.Echo,
            LocationName.Breath
    ])

    create_region(multiworld, player, RegionName.Daila,
    [
        LocationName.Daila_Herb,
        LocationName.Daila_3_coins,
        LocationName.Daila_12_coins,
        LocationName.Daila_Psy_Crystal,
        LocationName.Daila_Sleep_Bomb,
        LocationName.Daila_Sea_Gods_Tear,
        LocationName.Daila_Smoke_Bomb
    ])

    create_region(multiworld, player, RegionName.KandoreamTemple,
    [
        LocationName.Kandorean_Temple_Mimic,
        LocationName.Kandorean_Temple_Lash_Pebble,
        LocationName.Kandorean_Temple_Mysterious_Card,
        LocationName.DefeatChestBeaters,
        LocationName.Fog
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

    create_region(multiworld, player, RegionName.Madra,
    [
        LocationName.Madra_Elixir,
        LocationName.Madra_Antidote,
        LocationName.Madra_Cyclone_Chip,
        LocationName.Madra_Smoke_Bomb,
        LocationName.Madra_Sleep_Bomb,
        LocationName.Madra_15_coins,
        LocationName.Madra_Nurses_Cap,
        LocationName.Iron
    ])

    create_region(multiworld, player, RegionName.MadraCatacombs,
    [
        LocationName.Madra_Catacombs_Moloch,
        LocationName.Madra_Catacombs_Ruin_Key,
        LocationName.Madra_Catacombs_Tremor_Bit,
        LocationName.Madra_Catacombs_Apple,
        LocationName.Madra_Catacombs_Lucky_Medal,
        LocationName.Madra_Catacombs_Mist_Potion,
        LocationName.DoomDragonDefeated,

        LocationName.Flint,
        LocationName.Granite,
        LocationName.Quartz,
        LocationName.Vine,
        LocationName.Sap,
        LocationName.Ground,
        LocationName.Bane,
        LocationName.Steel,
        LocationName.Mud,
        LocationName.Flower,
        LocationName.Meld,
        LocationName.Petra,
        LocationName.Salt,
        LocationName.Geode,
        LocationName.Mold,
        LocationName.Crystal,

        LocationName.Fizz,
        LocationName.Sleet,
        LocationName.Mist,
        LocationName.Spritz,
        LocationName.Hail,
        LocationName.Tonic,
        LocationName.Dew,
        LocationName.Sour,
        LocationName.Spring,
        LocationName.Shade,
        LocationName.Chill,
        LocationName.Steam,
        LocationName.Rime,
        LocationName.Gel,
        LocationName.Eddy,
        LocationName.Balm,
        LocationName.Serac,

        LocationName.Forge,
        LocationName.Fever,
        LocationName.Corona,
        LocationName.Scorch,
        LocationName.Ember,
        LocationName.Flash,
        LocationName.Torch,
        LocationName.Spark,
        LocationName.Kindle,
        LocationName.Char,
        LocationName.Coal,
        LocationName.Reflux,
        LocationName.Core,
        LocationName.Tinder,
        LocationName.Shine,
        LocationName.Fury,
        LocationName.Fugue,

        LocationName.Gust,
        LocationName.Breeze,
        LocationName.Zephyr,
        LocationName.Smog,
        LocationName.Kite,
        LocationName.Squall,
        LocationName.Luff,
        LocationName.Blitz,
        LocationName.Ether,
        LocationName.Waft,
        LocationName.Haze,
        LocationName.Wheeze,
        LocationName.Aroma,
        LocationName.Whorl,
        LocationName.Gasp,
        LocationName.Lull,
        LocationName.Gale,


        LocationName.Tundaria_Tower_Burst_Brooch,
        LocationName.Lemuria_Grindstone,
        LocationName.Mars_Lighthouse_Teleport_Lapis,
        LocationName.Yampi_Desert_Scoop_Gem,
        LocationName.Shaman_Village_Hover_Jade,
        LocationName.Airs_Rock_Reveal,
        LocationName.Aqua_Rock_Parch,
        LocationName.Gaia_Rock_Sand,
        LocationName.Magma_Rock_Blaze,
        LocationName.Idejima_Mind_Read,
        LocationName.Idejima_Whirlwind,
        LocationName.Idejima_Growth,
        LocationName.Contigo_Carry_Stone,
        LocationName.Contigo_Lifting_Gem,
        LocationName.Contigo_Orb_of_Force,
        LocationName.Contigo_Catch_Beads,
        LocationName.Kibombo_Douse_Drop,
        LocationName.Kibombo_Frost_Jewel,

        LocationName.Madra_Catacombs_Moloch,
        LocationName.Yampi_Desert_Cave_Daedalus,
        LocationName.Airs_Rock_Flora,
        LocationName.Izumo_Ulysses,
        LocationName.Treasure_Isle_Azul,
        LocationName.Indra_Cavern_Zagan,
        LocationName.Osenia_Cavern_Megaera,
        LocationName.Angara_Cavern_Haures,
        LocationName.Atteka_Cavern_Coatlicue,
        LocationName.Islet_Cave_Catastrophe,
        LocationName.Anemos_Inner_Sanctum_Charon,
        LocationName.Anemos_Inner_Sanctum_Iris,
        LocationName.Lemuria_Eclipse,
    ])

    create_connect(multiworld, player, RegionName.Menu, RegionName.Idejima)
    create_connect(multiworld, player, RegionName.Idejima, RegionName.EasternSea)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Daila)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.KandoreamTemple)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.DehkanPlateau)
    create_connect(multiworld, player, RegionName.EasternSea, RegionName.Madra)
    create_connect(multiworld, player, RegionName.Madra, RegionName.MadraCatacombs, lambda state: state.has(ItemName.Sea_Gods_Tear, player))