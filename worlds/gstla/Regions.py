import typing
from .Names.LocationName import LocationName
from .Names.RegionName import RegionName


class RegionInfo:
    name: str
    connections: typing.List[str]
    locations: typing.List[str]

    def __init__(self, name, connections, locations):
        self.name = name
        self.connections = connections
        self.locations = locations


regions = [
    RegionInfo(RegionName.Menu, [RegionName.Idejima], []),
    RegionInfo(RegionName.Idejima, [RegionName.EasternSea],
               []),
    RegionInfo(RegionName.EasternSea,
               [
                   RegionName.Daila,
                   RegionName.KandoreamTemple,
                   RegionName.DehkanPlateau,
                   RegionName.Madra
               ], []),
    RegionInfo(RegionName.Daila, [],
               [
                   LocationName.Daila_Herb,
                   LocationName.Daila_3_coins,
                   LocationName.Daila_12_coins,
                   LocationName.Daila_Psy_Crystal,
                   LocationName.Daila_Sleep_Bomb,
                   LocationName.Daila_Sea_Gods_Tear,
                   LocationName.Daila_Smoke_Bomb
               ]),
    RegionInfo(RegionName.KandoreamTemple, [],
               [
                   LocationName.Kandorean_Temple_Mimic,
                   LocationName.Kandorean_Temple_Lash_Pebble,
                   LocationName.Kandorean_Temple_Mysterious_Card
               ]),
    RegionInfo(RegionName.DehkanPlateau, [],
               [
                   LocationName.Dehkan_Plateau_Elixir,
                   LocationName.Dehkan_Plateau_Pound_Cube,
                   LocationName.Dehkan_Plateau_Themis_Axe,
                   LocationName.Dehkan_Plateau_Full_Metal_Vest,
                   LocationName.Dehkan_Plateau_Mint,
                   LocationName.Dehkan_Plateau_Nut
               ]),
    RegionInfo(RegionName.Madra, [RegionName.MadraCatacombs],
               [
                   LocationName.Madra_Elixir,
                   LocationName.Madra_Antidote,
                   LocationName.Madra_Cyclone_Chip,
                   LocationName.Madra_15_coins,
                   LocationName.Madra_Nurses_Cap
               ]),
    RegionInfo(RegionName.MadraCatacombs, [],
               [
                   LocationName.Madra_Catacombs_Moloch,
                   LocationName.Madra_Catacombs_Ruin_Key,
                   LocationName.Madra_Catacombs_Tremor_Bit,
                   LocationName.Madra_Catacombs_Apple,
                   LocationName.Madra_Catacombs_Lucky_Medal,
                   LocationName.Madra_Catacombs_Mist_Potion,
                   LocationName.DoomDragonDefeated
               ])
]