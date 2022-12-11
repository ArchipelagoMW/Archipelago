from enum import Enum
from typing import Dict, List

class GameMode(Enum):
        Normal = 0
        Multiworld = 1

class Z3Logic(Enum):
        Normal = 0
        Nmg = 1
        Owg = 2

class SMLogic(Enum):
        Normal = 0
        Hard = 1

class SwordLocation(Enum):
        Randomized = 0
        Early = 1
        Uncle = 2   

class MorphLocation(Enum):
        Randomized = 0
        Early = 1
        Original = 2

class Goal(Enum):
        DefeatBoth = 0
        FastGanonDefeatMotherBrain = 1
        AllDungeonsDefeatMotherBrain = 2

class KeyShuffle(Enum):
        Null = 0
        Keysanity = 1

class OpenTower(Enum):
        Random = -1
        NoCrystals = 0
        OneCrystal = 1
        TwoCrystals = 2
        ThreeCrystals = 3
        FourCrystals = 4
        FiveCrystals = 5
        SixCrystals = 6
        SevenCrystals = 7

class GanonVulnerable(Enum):
        Random = -1
        NoCrystals = 0
        OneCrystal = 1
        TwoCrystals = 2
        ThreeCrystals = 3
        FourCrystals = 4
        FiveCrystals = 5
        SixCrystals = 6
        SevenCrystals = 7

class OpenTourian(Enum):
        Random = -1
        NoBosses = 0
        OneBoss = 1
        TwoBosses = 2
        ThreeBosses = 3
        FourBosses = 4

class Config:
    GameMode: GameMode = GameMode.Multiworld
    Z3Logic: Z3Logic = Z3Logic.Normal
    SMLogic: SMLogic = SMLogic.Normal
    SwordLocation: SwordLocation= SwordLocation.Randomized
    MorphLocation: MorphLocation = MorphLocation.Randomized
    Goal: Goal = Goal.DefeatBoth
    KeyShuffle: KeyShuffle = KeyShuffle.Null
    Race: bool = False

    OpenTower: OpenTower = OpenTower.SevenCrystals
    GanonVulnerable: GanonVulnerable = GanonVulnerable.SevenCrystals
    OpenTourian: OpenTourian = OpenTourian.FourBosses

    @property
    def SingleWorld(self) -> bool:
        return self.GameMode == GameMode.Normal
    
    @property
    def Multiworld(self) -> bool:
        return self.GameMode == GameMode.Multiworld

    @property
    def Keysanity(self) -> bool:
        return self.KeyShuffle != KeyShuffle.Null