from enum import IntEnum, auto


# this includes all player starts in the game, so (theoretically) it should never need to be changed
class PlayerStarts(IntEnum):
    DungeonMirror = 0  # first enum value is 0 to match indexes in the client
    DungeonMirrorSave = auto()
    DungeonSlideSave = auto()
    DungeonStrongEyesSave = auto()
    DungeonStrongEyesExit = auto()
    DungeonEscapeLowerExit = auto()
    DungeonEscapeUpperExit = auto()

    CastleWestSave = auto()
    CastleGazeboSave = auto()
    CastleEastSave = auto()
    CastleNorthwestSave = auto()
    CastleWestLowerExit = auto()
    CastleWestUpperExit = auto()
    CastleSouthLowerExit = auto()
    CastleSouthUpperExit = auto()
    CastleLockedExit = auto()
    CastleEastExit = auto()
    CastleNorthExit = auto()
    CastleNorthwestExit = auto()

    KeepCentralSave = auto()
    KeepNorthSave = auto()
    KeepSouthExit = auto()
    KeepSouthwestExit = auto()
    KeepLockedExit = auto()
    KeepNortheastExit = auto()
    KeepNorthExit = auto()

    LibraryMainSave = auto()
    LibraryBackSave = auto()
    LibraryExit = auto()

    TheatreSave = auto()
    TheatrePillarWestExit = auto()
    TheatrePillarEastExit = auto()
    TheatreFrontExit = auto()
    TheatreScythesNorthExit = auto()
    TheatreScythesSouthExit = auto()

    BaileySave = auto()
    BaileyNorthExit = auto()
    BaileyWestExit = auto()
    BaileyShackExit = auto()
    BaileyEastExit = auto()

    UnderbellySouthSave = auto()
    UnderbellyCentralSave = auto()
    UnderbellyEastSave = auto()
    UnderbellyPreLightSave = auto()
    UnderbellyPostLightSave = auto()
    UnderbellySouthExit = auto()
    UnderbellyHoleExit = auto()
    UnderbellyLightPillarExit = auto()

    TowerSave = auto()
    TowerSouthExit = auto()
    TowerTopExit = auto()

    ChambersExit = auto()
