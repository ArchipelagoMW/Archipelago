from typing import List
from BaseClasses import MultiWorld
from .Names.RegionName import RegionName
from .Names.EntranceName import EntranceName
from .GstlaTypes import EntranceData

vanilla_connections: List[EntranceData] = \
[
    EntranceData(EntranceName.Menu_StartGame, RegionName.Idejima),
    EntranceData(EntranceName.IdejimaToDaila, RegionName.Daila),
    EntranceData(EntranceName.AnywhereToJoinedPartyMembers, RegionName.PartyMembers),
    EntranceData(EntranceName.DailaToKandoreanTemple, RegionName.KandoreamTemple),
    EntranceData(EntranceName.DailaToShrineOfTheSeaGod, RegionName.ShrineOfTheSeaGod),
    EntranceData(EntranceName.DailaToDehkanPlateau, RegionName.DehkanPlateau),
    EntranceData(EntranceName.DehkanPlateauToMadra, RegionName.Madra),
    EntranceData(EntranceName.MadraToIndraCavern, RegionName.IndraCavern),
    EntranceData(EntranceName.MadraToMadraCatacombs, RegionName.MadraCatacombs),
    EntranceData(EntranceName.MadraToOseniaCliffs, RegionName.OseniaCliffs),
    EntranceData(EntranceName.MadraToGondowanCliffs, RegionName.GondowanCliffs),
    EntranceData(EntranceName.MadraToEasternSea, RegionName.EasternSea),
    EntranceData(EntranceName.MadraToLemurianShip, RegionName.Lemurian_Ship),
    EntranceData(EntranceName.OseniaCliffsToMikasalla, RegionName.Mikasalla),
    EntranceData(EntranceName.YampiDesertFrontToYampiDesertBack, RegionName.YampiDesertBack),
    EntranceData(EntranceName.YampiDesertBackToYampiDesertCave, RegionName.YampiDesertCave),
    EntranceData(EntranceName.YampiDesertBackToAlhafra, RegionName.Alhafra),
    EntranceData(EntranceName.AlhafraToYampiDesertBack, RegionName.YampiDesertBack),
    EntranceData(EntranceName.AlhafraToAlhafraCave, RegionName.AlhafraCave),
    EntranceData(EntranceName.MikasallaToGaroh, RegionName.Garoh),
    EntranceData(EntranceName.MikasallaToOseniaCavern, RegionName.OseniaCavern),
    EntranceData(EntranceName.MikasallaToYampiDesertFront, RegionName.YampiDesertFront),
    EntranceData(EntranceName.GarohToAirsRock, RegionName.AirsRock),
    EntranceData(EntranceName.GarohToYampiDesertBack, RegionName.YampiDesertBack),
    EntranceData(EntranceName.GondowanCliffsToNaribwe, RegionName.Naribwe),
    EntranceData(EntranceName.NaribweToKibomboMountains, RegionName.KibomboMountains),
    EntranceData(EntranceName.KibomboMountainsToKibombo, RegionName.Kibombo),
    EntranceData(EntranceName.KibomboToGabombaStatue, RegionName.GabombaStatue),
    EntranceData(EntranceName.GabombaStatueToGabombaCatacombs, RegionName.GabombaCatacombs),
    EntranceData(EntranceName.EasternSeaToAlhafra, RegionName.Alhafra),
    EntranceData(EntranceName.EasternSeaToKibombo, RegionName.Kibombo),
    EntranceData(EntranceName.EasternSeaToNaribwe, RegionName.Naribwe),
    EntranceData(EntranceName.EasternSeaToWestIndraIslet, RegionName.WestIndraIslet),
    EntranceData(EntranceName.EasternSeaToNorthOseniaIslet, RegionName.NorthOseniaIslet),
    EntranceData(EntranceName.EasternSeaToSouthEastAngaraIslet, RegionName.SouthEastAngaraIslet),
    EntranceData(EntranceName.EasternSeaToSeaOfTimeIslet, RegionName.SeaOfTimeIslet),
    EntranceData(EntranceName.EasternSeaToSeaOfTime, RegionName.SeaOfTime),
    EntranceData(EntranceName.EasternSeaToTreasureIsland, RegionName.TreasureIsland),
    EntranceData(EntranceName.EasternSeaToChampa, RegionName.Champa),
    EntranceData(EntranceName.EasternSeaToAnkohlRuins, RegionName.AnkohlRuins),
    EntranceData(EntranceName.EasternSeaToIzumo, RegionName.Izumo),
    EntranceData(EntranceName.EasternSeaToGaiaRock, RegionName.GaiaRock),
    EntranceData(EntranceName.EasternSeaToYallam, RegionName.Yallam),
    EntranceData(EntranceName.EasternSeaToEastTundariaIslet, RegionName.EastTundariaIslet),
    EntranceData(EntranceName.EasternSeaToTundariaTower, RegionName.TundariaTower),
    EntranceData(EntranceName.EasternSeaToApojiiIslands, RegionName.ApojiiIslands),
    EntranceData(EntranceName.EasternSeaToAquaRock, RegionName.AquaRock),
    EntranceData(EntranceName.EasternSeaToWesternSea, RegionName.WesternSea),
    EntranceData(EntranceName.SeaOfTimeIsletToIsletCave, RegionName.IsletCave),
    EntranceData(EntranceName.TreasureIslandToTreasureIsland_Grindstone, RegionName.TreasureIsland_Grindstone),
    EntranceData(EntranceName.TreasureIsland_GrindstoneToTreasureIsland_PostReunion, RegionName.TreasureIsland_PostReunion),
    EntranceData(EntranceName.TundariaTowerToTundariaTower_Parched, RegionName.TundariaTower_Parched),
    EntranceData(EntranceName.AnkohlRuinsToAnkohlRuins_Sand, RegionName.AnkohlRuins_Sand),
    EntranceData(EntranceName.YallamToTaopoSwamp, RegionName.TaopoSwamp),
    EntranceData(EntranceName.SeaOfTimeToLemuria, RegionName.Lemuria),
    EntranceData(EntranceName.LemuriaToShipRevisit, RegionName.Lemurian_Ship_Revisit),
    EntranceData(EntranceName.WesternSeaToSouthWestAttekaIslet, RegionName.SouthWestAttekaIslet),
    EntranceData(EntranceName.WesternSeaToHesperiaSettlement, RegionName.HesperiaSettlement),
    EntranceData(EntranceName.WesternSeaToShamanVillageCave, RegionName.ShamanVillageCave),
    EntranceData(EntranceName.WesternSeaToAttekaInlet, RegionName.AttekaInlet),
    EntranceData(EntranceName.WesternSeaToAttekaCavern, RegionName.AttekaCavern),
    EntranceData(EntranceName.WesternSeaToGondowanSettlement, RegionName.GondowanSettlement),
    EntranceData(EntranceName.WesternSeaToMagmaRock, RegionName.MagmaRock),
    EntranceData(EntranceName.WesternSeaToLoho, RegionName.Loho),
    EntranceData(EntranceName.WesternSeaToAngaraCavern, RegionName.AngaraCavern),
    EntranceData(EntranceName.WesternSeaToKaltIsland, RegionName.KaltIsland),
    EntranceData(EntranceName.WesternSeaToProx, RegionName.Prox),
    EntranceData(EntranceName.ShamanVillageCaveToShamanVillage, RegionName.ShamanVillage),
    EntranceData(EntranceName.AttekaInletToContigo, RegionName.Contigo),
    EntranceData(EntranceName.AttekaInletToShipRevisit, RegionName.Lemurian_Ship_Revisit),
    EntranceData(EntranceName.ContigoToJupiterLighthouse, RegionName.JupiterLighthouse),
    EntranceData(EntranceName.ContigoToAnemosInnerSanctum, RegionName.AnemosSanctum),
    EntranceData(EntranceName.ContigoToReunion, RegionName.Reunion),
    EntranceData(EntranceName.MagmaRockToMagmaRockInterior, RegionName.MagmaRockInterior),
    EntranceData(EntranceName.ProxToMarsLighthouse, RegionName.MarsLighthouse),
    EntranceData(EntranceName.MarsLighthouseToMarsLighthouse_Activated, RegionName.MarsLighthouse_Activated)
]


def create_vanilla_connections(multiworld: MultiWorld, player: int):
    for connection in vanilla_connections:
        entrance = multiworld.get_entrance(connection.source_entrance, player)
        target = multiworld.get_region(connection.target, player)

        entrance.connect(target)