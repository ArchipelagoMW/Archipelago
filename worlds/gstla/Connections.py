from typing import List
from BaseClasses import MultiWorld
from .Names.RegionName import RegionName
from .Names.EntranceName import EntranceName


class ConnectionData:
    source_entrance: str
    target: str

    def __init__(self, _source_entrance: str, _target: str):
        self.source_entrance = _source_entrance
        self.target = _target



connections: List[ConnectionData] = \
[
    ConnectionData(EntranceName.Menu_StartGame, RegionName.Idejima),
    ConnectionData(EntranceName.IdejimaToDaila, RegionName.Daila),
    ConnectionData(EntranceName.AnywhereToJoinedPartyMembers, RegionName.PartyMembers),
    ConnectionData(EntranceName.DailaToKandoreanTemple, RegionName.KandoreamTemple),
    ConnectionData(EntranceName.DailaToShrineOfTheSeaGod, RegionName.ShrineOfTheSeaGod),
    ConnectionData(EntranceName.DailaToDehkanPlateau, RegionName.DehkanPlateau),
    ConnectionData(EntranceName.DehkanPlateauToMadra, RegionName.Madra),
    ConnectionData(EntranceName.MadraToIndraCavern, RegionName.IndraCavern),
    ConnectionData(EntranceName.MadraToMadraCatacombs, RegionName.MadraCatacombs),
    ConnectionData(EntranceName.MadraToOseniaCliffs, RegionName.OseniaCliffs),
    ConnectionData(EntranceName.MadraToGondowanCliffs, RegionName.GondowanCliffs),
    ConnectionData(EntranceName.MadraToEasternSea, RegionName.EasternSea),
    ConnectionData(EntranceName.MadraToLemurianShip, RegionName.Lemurian_Ship),
    ConnectionData(EntranceName.OseniaCliffsToMikasalla, RegionName.Mikasalla),
    ConnectionData(EntranceName.YampiDesertFrontToYampiDesertBack, RegionName.YampiDesertBack),
    ConnectionData(EntranceName.YampiDesertBackToYampiDesertCave, RegionName.YampiDesertCave),
    ConnectionData(EntranceName.YampiDesertBackToAlhafra, RegionName.Alhafra),
    ConnectionData(EntranceName.AlhafraToYampiDesertBack, RegionName.YampiDesertBack),
    ConnectionData(EntranceName.AlhafraToAlhafraCave, RegionName.AlhafraCave),
    ConnectionData(EntranceName.MikasallaToGaroh, RegionName.Garoh),
    ConnectionData(EntranceName.MikasallaToOseniaCavern, RegionName.OseniaCavern),
    ConnectionData(EntranceName.MikasallaToYampiDesertFront, RegionName.YampiDesertFront),
    ConnectionData(EntranceName.GarohToAirsRock, RegionName.AirsRock),
    ConnectionData(EntranceName.GarohToYampiDesertBack, RegionName.YampiDesertBack),
    ConnectionData(EntranceName.GondowanCliffsToNaribwe, RegionName.Naribwe),
    ConnectionData(EntranceName.NaribweToKibomboMountains, RegionName.KibomboMountains),
    ConnectionData(EntranceName.KibomboMountainsToKibombo, RegionName.Kibombo),
    ConnectionData(EntranceName.KibomboToGabombaStatue, RegionName.GabombaStatue),
    ConnectionData(EntranceName.GabombaStatueToGabombaCatacombs, RegionName.GabombaCatacombs),
    ConnectionData(EntranceName.EasternSeaToAlhafra, RegionName.Alhafra),
    ConnectionData(EntranceName.EasternSeaToKibombo, RegionName.Kibombo),
    ConnectionData(EntranceName.EasternSeaToNaribwe, RegionName.Naribwe),
    ConnectionData(EntranceName.EasternSeaToWestIndraIslet, RegionName.WestIndraIslet),
    ConnectionData(EntranceName.EasternSeaToNorthOseniaIslet, RegionName.NorthOseniaIslet),
    ConnectionData(EntranceName.EasternSeaToSouthEastAngaraIslet, RegionName.SouthEastAngaraIslet),
    ConnectionData(EntranceName.EasternSeaToSeaOfTimeIslet, RegionName.SeaOfTimeIslet),
    ConnectionData(EntranceName.EasternSeaToSeaOfTime, RegionName.SeaOfTime),
    ConnectionData(EntranceName.EasternSeaToTreasureIsland, RegionName.TreasureIsland),
    ConnectionData(EntranceName.EasternSeaToChampa, RegionName.Champa),
    ConnectionData(EntranceName.EasternSeaToAnkohlRuins, RegionName.AnkohlRuins),
    ConnectionData(EntranceName.EasternSeaToIzumo, RegionName.Izumo),
    ConnectionData(EntranceName.EasternSeaToGaiaRock, RegionName.GaiaRock),
    ConnectionData(EntranceName.EasternSeaToYallam, RegionName.Yallam),
    ConnectionData(EntranceName.EasternSeaToEastTundariaIslet, RegionName.EastTundariaIslet),
    ConnectionData(EntranceName.EasternSeaToTundariaTower, RegionName.TundariaTower),
    ConnectionData(EntranceName.EasternSeaToApojiiIslands, RegionName.ApojiiIslands),
    ConnectionData(EntranceName.EasternSeaToAquaRock, RegionName.AquaRock),
    ConnectionData(EntranceName.EasternSeaToWesternSea, RegionName.WesternSea),
    ConnectionData(EntranceName.SeaOfTimeIsletToIsletCave, RegionName.IsletCave),
    ConnectionData(EntranceName.TreasureIslandToTreasureIsland_Grindstone, RegionName.TreasureIsland_Grindstone),
    ConnectionData(EntranceName.TreasureIsland_GrindstoneToTreasureIsland_PostReunion, RegionName.TreasureIsland_PostReunion),
    ConnectionData(EntranceName.TundariaTowerToTundariaTower_Parched, RegionName.TundariaTower_Parched),
    ConnectionData(EntranceName.AnkohlRuinsToAnkohlRuins_Sand, RegionName.AnkohlRuins_Sand),
    ConnectionData(EntranceName.YallamToTaopoSwamp, RegionName.TaopoSwamp),
    ConnectionData(EntranceName.SeaOfTimeToLemuria, RegionName.Lemuria),
    ConnectionData(EntranceName.LemuriaToShipRevisit, RegionName.Lemurian_Ship_Revisit),
    ConnectionData(EntranceName.WesternSeaToSouthWestAttekaIslet, RegionName.SouthWestAttekaIslet),
    ConnectionData(EntranceName.WesternSeaToHesperiaSettlement, RegionName.HesperiaSettlement),
    ConnectionData(EntranceName.WesternSeaToShamanVillageCave, RegionName.ShamanVillageCave),
    ConnectionData(EntranceName.WesternSeaToAttekaInlet, RegionName.AttekaInlet),
    ConnectionData(EntranceName.WesternSeaToAttekaCavern, RegionName.AttekaCavern),
    ConnectionData(EntranceName.WesternSeaToGondowanSettlement, RegionName.GondowanSettlement),
    ConnectionData(EntranceName.WesternSeaToMagmaRock, RegionName.MagmaRock),
    ConnectionData(EntranceName.WesternSeaToLoho, RegionName.Loho),
    ConnectionData(EntranceName.WesternSeaToAngaraCavern, RegionName.AngaraCavern),
    ConnectionData(EntranceName.WesternSeaToKaltIsland, RegionName.KaltIsland),
    ConnectionData(EntranceName.WesternSeaToProx, RegionName.Prox),
    ConnectionData(EntranceName.ShamanVillageCaveToShamanVillage, RegionName.ShamanVillage),
    ConnectionData(EntranceName.AttekaInletToContigo, RegionName.Contigo),
    ConnectionData(EntranceName.AttekaInletToShipRevisit, RegionName.Lemurian_Ship_Revisit),
    ConnectionData(EntranceName.ContigoToJupiterLighthouse, RegionName.JupiterLighthouse),
    ConnectionData(EntranceName.ContigoToAnemosInnerSanctum, RegionName.AnemosSanctum),
    ConnectionData(EntranceName.ContigoToReunion, RegionName.Reunion),
    ConnectionData(EntranceName.MagmaRockToMagmaRockInterior, RegionName.MagmaRockInterior),
    ConnectionData(EntranceName.ProxToMarsLighthouse, RegionName.MarsLighthouse),
    ConnectionData(EntranceName.MarsLighthouseToMarsLighthouse_Activated, RegionName.MarsLighthouse_Activated)
]


def create_connections(multiworld: MultiWorld, player: int):
    for connection in connections:
        entrance = multiworld.get_entrance(connection.source_entrance, player)
        target = multiworld.get_region(connection.target, player)

        entrance.connect(target)