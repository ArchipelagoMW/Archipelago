from dataclasses import dataclass
from typing import Dict, Tuple, List, Union

from .Enums import Character, Area, SubLevel, LevelMission, pascal_to_space, SubLevelMission, Capsule, Enemy, \
    Fish
from .Names import ItemName, LocationName
from .Names.LocationName import Boss
from .Options import SonicAdventureDXOptions

LogicItems = Union[List[str], List[List[str]]]


@dataclass
class LevelLocation:
    locationId: int
    area: Area
    character: Character
    levelMission: LevelMission
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertDCLogicItems: List[str]
    expertDXLogicItems: List[str]
    expertPlusDXLogicItems: List[str]

    def get_level_name(self) -> str:
        return f"{pascal_to_space(self.area.name)} ({self.character.name}) - Mission {self.levelMission.name}"

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicItems
        elif options.logic_level.value == 3:
            return self.expertDXLogicItems
        elif options.logic_level.value == 2:
            return self.expertDCLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class UpgradeLocation:
    locationId: int
    locationName: str
    area: Area
    character: Character
    normalLogicItems: LogicItems
    hardLogicItems: LogicItems
    expertDCLogicItems: LogicItems
    expertDXLogicItems: LogicItems
    expertPlusDXLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> LogicItems:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicItems
        elif options.logic_level.value == 3:
            return self.expertDXLogicItems
        elif options.logic_level.value == 2:
            return self.expertDCLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class CharacterUpgrade:
    character: Character
    upgrade: str


@dataclass
class EmblemLocation:
    locationId: int
    area: Area
    normalLogicCharacters: List[Union[CharacterUpgrade, Character]]
    hardLogicCharacters: List[Union[CharacterUpgrade, Character]]
    expertDCLogicCharacters: List[Union[CharacterUpgrade, Character]]
    expertDXLogicCharacters: List[Union[CharacterUpgrade, Character]]
    expertPlusDXLogicCharacters: List[Union[CharacterUpgrade, Character]]
    emblemName: str

    def get_logic_characters_upgrades(self, options: SonicAdventureDXOptions) -> (
            List)[Union[CharacterUpgrade, Character]]:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicCharacters
        elif options.logic_level.value == 3:
            return self.expertDXLogicCharacters
        elif options.logic_level.value == 2:
            return self.expertDCLogicCharacters
        elif options.logic_level.value == 1:
            return self.hardLogicCharacters
        else:
            return self.normalLogicCharacters

    def get_logic_characters(self, options: SonicAdventureDXOptions) -> List[Character]:
        if options.logic_level.value == 4:
            return self._get_characters(self.expertPlusDXLogicCharacters)
        elif options.logic_level.value == 3:
            return self._get_characters(self.expertDXLogicCharacters)
        elif options.logic_level.value == 2:
            return self._get_characters(self.expertDCLogicCharacters)
        elif options.logic_level.value == 1:
            return self._get_characters(self.hardLogicCharacters)
        else:
            return self._get_characters(self.normalLogicCharacters)

    @staticmethod
    def _get_characters(logic: List[Union[CharacterUpgrade, Character]]) -> List[Character]:
        return [item.character if isinstance(item, CharacterUpgrade) else item for item in logic]


@dataclass
class CapsuleLocation:
    locationId: int
    area: Area
    character: Character
    capsuleNumber: int
    type: Capsule
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertDCLogicItems: List[str]
    expertDXLogicItems: List[str]
    expertPlusDXLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicItems
        elif options.logic_level.value == 3:
            return self.expertDXLogicItems
        elif options.logic_level.value == 2:
            return self.expertDCLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class EnemyLocation:
    locationId: int
    area: Area
    character: Character
    enemyNumber: int
    type: Enemy
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertDCLogicItems: List[str]
    expertDXLogicItems: List[str]
    expertPlusDXLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicItems
        elif options.logic_level.value == 3:
            return self.expertDXLogicItems
        elif options.logic_level.value == 2:
            return self.expertDCLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class MissionLocation:
    locationId: int
    cardArea: Area
    objectiveArea: Area
    character: Character
    missionNumber: int
    normalLogicItems: LogicItems
    hardLogicItems: LogicItems
    expertDCLogicItems: LogicItems
    expertDXLogicItems: LogicItems
    expertPlusDXLogicItems: LogicItems

    def get_mission_name(self) -> str:
        return f"Mission {self.missionNumber} ({self.character.name})"

    def get_logic_items(self, options: SonicAdventureDXOptions) -> LogicItems:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicItems
        elif options.logic_level.value == 3:
            return self.expertDXLogicItems
        elif options.logic_level.value == 2:
            return self.expertDCLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems


@dataclass
class SubLevelLocation:
    locationId: int
    area: Area
    subLevel: SubLevel
    subLevelMission: SubLevelMission
    normalLogicCharacters: List[Character]
    hardLogicCharacters: List[Character]
    expertDCLogicCharacters: List[Character]
    expertDXLogicCharacters: List[Character]
    expertPlusDXLogicCharacters: List[Character]

    def get_logic_characters(self, options: SonicAdventureDXOptions) -> List[Character]:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicCharacters
        elif options.logic_level.value == 3:
            return self.expertDXLogicCharacters
        elif options.logic_level.value == 2:
            return self.expertDCLogicCharacters
        elif options.logic_level.value == 1:
            return self.hardLogicCharacters
        else:
            return self.normalLogicCharacters


@dataclass
class BossFightLocation:
    locationId: int
    area: Area
    characters: List[Character]
    boss: Boss
    unified: bool

    def get_boss_name(self) -> str:
        if self.unified:
            return f"{self.boss} Boss Fight"
        else:
            return f"{self.boss} Boss Fight ({self.characters[0].name})"


@dataclass
class ChaoEggLocation:
    locationId: int
    eggName: str
    area: Area
    characters: List[Character]
    requirements: List[List[str]]


@dataclass
class ChaoRaceLocation:
    locationId: int
    name: str
    area: Area


@dataclass
class FishLocation:
    locationId: int
    area: Area
    fishType: Fish
    normalLogicItems: List[str]
    hardLogicItems: List[str]
    expertDCLogicItems: List[str]
    expertDXLogicItems: List[str]
    expertPlusDXLogicItems: List[str]

    def get_logic_items(self, options: SonicAdventureDXOptions) -> List[str]:
        if options.logic_level.value == 4:
            return self.expertPlusDXLogicItems
        elif options.logic_level.value == 3:
            return self.expertDXLogicItems
        elif options.logic_level.value == 2:
            return self.expertDCLogicItems
        elif options.logic_level.value == 1:
            return self.hardLogicItems
        else:
            return self.normalLogicItems

    def get_location_name(self) -> str:
        return f"{pascal_to_space(self.area.name)} (Big) - {pascal_to_space(self.fishType.name)}"


HotelKey = ItemName.KeyItem.HotelKey
PoolKey = ItemName.KeyItem.PoolKey
CasinoKey = ItemName.KeyItem.CasinoKey
StationKey = ItemName.KeyItem.StationKey
ShutterKey = ItemName.KeyItem.ShutterKey
PolicePass = ItemName.KeyItem.PolicePass
TPTicket = ItemName.KeyItem.TPTicket
EmployeeCard = ItemName.KeyItem.EmployeeCard
IceStone = ItemName.KeyItem.IceStone
WindStone = ItemName.KeyItem.WindStone
Dynamite = ItemName.KeyItem.Dynamite
JungleCart = ItemName.KeyItem.JungleCart
TimeMachine = ItemName.KeyItem.TimeMachine
Egglift = ItemName.KeyItem.Egglift
Monorail = ItemName.KeyItem.Monorail
Train = ItemName.KeyItem.Train
Boat = ItemName.KeyItem.Boat
Raft = ItemName.KeyItem.Raft

EMBLEM_BLOCKED = "EMBLEM_BLOCKED"
ONLY_RANDO = "ONLY_RANDO"
ECSwitchAccess = "ECSwitchAccess"

LightShoes = ItemName.Sonic.LightShoes
AncientLight = ItemName.Sonic.AncientLight
ShovelClaw = ItemName.Knuckles.ShovelClaw
LifeBelt = ItemName.Big.LifeBelt
JetBooster = ItemName.Gamma.JetBooster
JetAnklet = ItemName.Tails.JetAnklet
Lure1 = ItemName.Big.Lure1
Lure2 = ItemName.Big.Lure2
Lure3 = ItemName.Big.Lure3
Lure4 = ItemName.Big.Lure4

P_SONIC = Character.Sonic
P_TAILS = Character.Tails
P_KNUCKLES = Character.Knuckles
P_AMY = Character.Amy
P_GAMMA = Character.Gamma
P_BIG = Character.Big
P_GAMMA_W_JB = CharacterUpgrade(Character.Gamma, ItemName.Gamma.JetBooster)
P_KNUCKLES_W_SC = CharacterUpgrade(Character.Knuckles, ItemName.Knuckles.ShovelClaw)
P_SONIC_W_LS = CharacterUpgrade(Character.Sonic, ItemName.Sonic.LightShoes)
EVERYONE = [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_GAMMA, P_BIG]

area_connections: Dict[
    Tuple[Character, Area, Area, bool], Tuple[List[str], List[str], List[str], List[str], List[str]]] = {
    (Character.Sonic, Area.CityHall, Area.SSMain, False): ([PolicePass], [PolicePass], [PolicePass], [], []),
    (Character.Sonic, Area.CityHall, Area.SpeedHighway, False): ([ONLY_RANDO], [ONLY_RANDO], [], [], []),
    (Character.Sonic, Area.CityHall, Area.Chaos0, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.CityHall, Area.Sewers, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Sonic, Area.Sewers, Area.CityHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.Sewers, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.Station, Area.SSMain, False): ([StationKey], [StationKey], [], [], []),
    (Character.Sonic, Area.Station, Area.MRMain, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Sonic, Area.Station, Area.Casino, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Sonic, Area.Casino, Area.Station, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Sonic, Area.Casino, Area.Casinopolis, False): (
        [EMBLEM_BLOCKED, LightShoes], [EMBLEM_BLOCKED], [], [], []),
    (Character.Sonic, Area.Casino, Area.Hotel, False): ([CasinoKey], [CasinoKey], [], [], []),
    (Character.Sonic, Area.Casino, Area.EggWalker, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Sonic, Area.SSMain, Area.Hotel, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Sonic, Area.SSMain, Area.Station, False): ([StationKey], [StationKey], [], [], []),
    (Character.Sonic, Area.SSMain, Area.CityHall, False): ([PolicePass], [PolicePass], [], [], []),
    (Character.Sonic, Area.SSMain, Area.ECOutside, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Sonic, Area.SSMain, Area.SpeedHighway, False): ([EmployeeCard], [EmployeeCard], [], [], []),
    (Character.Sonic, Area.SSMain, Area.TPTunnel, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Sonic, Area.TPTunnel, Area.SSMain, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Sonic, Area.TPTunnel, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.TPTunnel, Area.TPLobby, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Sonic, Area.TPLobby, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.TPLobby, Area.TwinklePark, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.TPLobby, Area.TwinkleCircuit, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.Hotel, Area.SSMain, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Sonic, Area.Hotel, Area.Casino, False): ([CasinoKey], [CasinoKey], [], [], []),
    (Character.Sonic, Area.Hotel, Area.SSChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.Hotel, Area.Chaos2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Sonic, Area.Hotel, Area.HotelPool, False): ([PoolKey], [PoolKey], [], [], []),
    (Character.Sonic, Area.HotelPool, Area.Hotel, False): ([PoolKey], [PoolKey], [], [PoolKey], [PoolKey]),
    (Character.Sonic, Area.HotelPool, Area.EmeraldCoast, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Sonic, Area.MRMain, Area.Station, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Sonic, Area.MRMain, Area.ECOutside, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Sonic, Area.MRMain, Area.WindyValley, False): (
        [WindStone], [WindStone], [WindStone], [WindStone], [WindStone]),
    (Character.Sonic, Area.MRMain, Area.Jungle, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Sonic, Area.MRMain, Area.Chaos4, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.MRMain, Area.EggHornet, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.MRMain, Area.SkyChase1, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.MRMain, Area.MRChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.MRMain, Area.AngelIsland, False): ([Dynamite], [Dynamite], [], [], []),
    (Character.Sonic, Area.AngelIsland, Area.MRMain, False): ([Dynamite], [Dynamite], [], [], []),
    (Character.Sonic, Area.AngelIsland, Area.IceCave, False): ([IceStone], [IceStone], [], [], []),
    (Character.Sonic, Area.AngelIsland, Area.RedMountain, False): (
        [EMBLEM_BLOCKED, LightShoes, AncientLight], [EMBLEM_BLOCKED, LightShoes, AncientLight], [], [], []),
    (Character.Sonic, Area.AngelIsland, Area.PastAltar, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Sonic, Area.IceCave, Area.AngelIsland, False): ([IceStone], [IceStone], [], [], []),
    (Character.Sonic, Area.IceCave, Area.IceCap, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.PastAltar, Area.AngelIsland, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Sonic, Area.PastAltar, Area.PastMain, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.PastMain, Area.PastAltar, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.PastMain, Area.Jungle, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Sonic, Area.Jungle, Area.PastMain, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Sonic, Area.Jungle, Area.MRMain, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Sonic, Area.Jungle, Area.LostWorld, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Sonic, Area.Jungle, Area.LostWorld, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Sonic, Area.Jungle, Area.SandHill, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.Jungle, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.FinalEggTower, Area.Jungle, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.FinalEggTower, Area.FinalEgg, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.FinalEggTower, Area.FinalEgg, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Sonic, Area.FinalEggTower, Area.BetaEggViper, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.FinalEggTower, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECOutside, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Sonic, Area.ECOutside, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Sonic, Area.ECOutside, Area.SkyChase2, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECOutside, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECOutside, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Sonic, Area.ECOutside, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Sonic, Area.ECOutside, Area.CaptainRoom, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Sonic, Area.ECOutside, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECBridge, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Sonic, Area.ECBridge, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Sonic, Area.ECBridge, Area.SkyDeck, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECBridge, Area.SkyChase2, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECBridge, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECBridge, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Sonic, Area.ECDeck, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECDeck, Area.CaptainRoom, False): ([ONLY_RANDO], [EMBLEM_BLOCKED], [], [], []),
    (Character.Sonic, Area.ECDeck, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECDeck, Area.PrivateRoom, True): (
        [ONLY_RANDO], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECDeck, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Sonic, Area.CaptainRoom, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.CaptainRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Sonic, Area.CaptainRoom, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.PrivateRoom, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.PrivateRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Sonic, Area.PrivateRoom, Area.ECDeck, True): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Sonic, Area.ECPool, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECPool, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Sonic, Area.ECPool, Area.SkyDeck, False): ([ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [], []),
    (Character.Sonic, Area.ECInside, Area.ECOutside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Sonic, Area.ECInside, Area.ECOutside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Sonic, Area.ECInside, Area.ECDeck, False): (
        [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess],
        [Egglift, ECSwitchAccess]),
    (Character.Sonic, Area.ECInside, Area.ECBridge, False): (
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess],
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess]),
    (Character.Sonic, Area.ECInside, Area.HotShelter, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Sonic, Area.ECInside, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECInside, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECInside, Area.WarpHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECInside, Area.Arsenal, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.ECInside, Area.WaterTank, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.HedgehogHammer, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.HedgehogHammer, Area.PrisonHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.PrisonHall, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.Arsenal, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.WaterTank, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.WarpHall, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Sonic, Area.WarpHall, Area.ECChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.CityHall, Area.SSMain, False): (
        [PolicePass], [PolicePass], [PolicePass], [PolicePass], [PolicePass]),
    (Character.Tails, Area.CityHall, Area.SpeedHighway, False): ([ONLY_RANDO], [ONLY_RANDO], [], [], []),
    (Character.Tails, Area.CityHall, Area.Chaos0, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.CityHall, Area.Sewers, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Tails, Area.Sewers, Area.CityHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.Sewers, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.Station, Area.SSMain, False): ([StationKey], [StationKey], [], [StationKey], [StationKey]),
    (Character.Tails, Area.Station, Area.MRMain, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Tails, Area.Station, Area.Casino, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Tails, Area.Casino, Area.Station, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Tails, Area.Casino, Area.Casinopolis, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.Casino, Area.Hotel, False): ([CasinoKey], [CasinoKey], [], [], []),
    (Character.Tails, Area.Casino, Area.EggWalker, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.SSMain, Area.Hotel, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Tails, Area.SSMain, Area.Station, False): ([StationKey], [StationKey], [], [], []),
    (Character.Tails, Area.SSMain, Area.CityHall, False): ([PolicePass], [PolicePass], [], [], []),
    (Character.Tails, Area.SSMain, Area.ECOutside, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Tails, Area.SSMain, Area.SpeedHighway, False): ([EmployeeCard], [EmployeeCard], [], [], []),
    (Character.Tails, Area.SSMain, Area.TPTunnel, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Tails, Area.TPTunnel, Area.SSMain, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Tails, Area.TPTunnel, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.TPTunnel, Area.TPLobby, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Tails, Area.TPLobby, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.TPLobby, Area.TwinklePark, False): ([ONLY_RANDO], [ONLY_RANDO], [], [], []),
    (Character.Tails, Area.TPLobby, Area.TwinkleCircuit, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.Hotel, Area.SSMain, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Tails, Area.Hotel, Area.Casino, False): ([CasinoKey], [CasinoKey], [], [], []),
    (Character.Tails, Area.Hotel, Area.SSChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.Hotel, Area.Chaos2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.Hotel, Area.HotelPool, False): ([PoolKey], [PoolKey], [], [PoolKey], [PoolKey]),
    (Character.Tails, Area.HotelPool, Area.Hotel, False): ([PoolKey], [PoolKey], [], [PoolKey], [PoolKey]),
    (Character.Tails, Area.HotelPool, Area.EmeraldCoast, False): (
        [ONLY_RANDO], [ONLY_RANDO], [], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.MRMain, Area.Station, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Tails, Area.MRMain, Area.ECOutside, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Tails, Area.MRMain, Area.WindyValley, False): (
        [WindStone], [WindStone], [WindStone], [WindStone], [WindStone]),
    (Character.Tails, Area.MRMain, Area.Jungle, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Tails, Area.MRMain, Area.Chaos4, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.MRMain, Area.EggHornet, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.MRMain, Area.SkyChase1, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.MRMain, Area.MRChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.MRMain, Area.AngelIsland, False): ([Dynamite], [Dynamite], [], [], []),
    (Character.Tails, Area.AngelIsland, Area.MRMain, False): ([Dynamite], [Dynamite], [], [], []),
    (Character.Tails, Area.AngelIsland, Area.IceCave, False): ([IceStone], [IceStone], [], [], []),
    (Character.Tails, Area.AngelIsland, Area.RedMountain, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.AngelIsland, Area.PastAltar, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Tails, Area.IceCave, Area.AngelIsland, False): ([IceStone], [IceStone], [], [IceStone], [IceStone]),
    (Character.Tails, Area.IceCave, Area.IceCap, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.PastAltar, Area.AngelIsland, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Tails, Area.PastAltar, Area.PastMain, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.PastMain, Area.PastAltar, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.PastMain, Area.Jungle, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Tails, Area.Jungle, Area.PastMain, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Tails, Area.Jungle, Area.MRMain, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Tails, Area.Jungle, Area.LostWorld, False): ([ONLY_RANDO], [ONLY_RANDO], [], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.Jungle, Area.LostWorld, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.Jungle, Area.SandHill, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.Jungle, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.FinalEggTower, Area.Jungle, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.FinalEggTower, Area.FinalEgg, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.FinalEggTower, Area.FinalEgg, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.FinalEggTower, Area.BetaEggViper, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.FinalEggTower, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECOutside, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Tails, Area.ECOutside, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Tails, Area.ECOutside, Area.SkyChase2, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECOutside, Area.Chaos6ZeroBeta, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.ECOutside, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Tails, Area.ECOutside, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Tails, Area.ECOutside, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECOutside, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECBridge, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Tails, Area.ECBridge, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Tails, Area.ECBridge, Area.SkyDeck, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECBridge, Area.SkyChase2, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECBridge, Area.Chaos6ZeroBeta, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.ECBridge, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Tails, Area.ECDeck, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECDeck, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECDeck, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECDeck, Area.PrivateRoom, True): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECDeck, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Tails, Area.CaptainRoom, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.CaptainRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Tails, Area.CaptainRoom, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.PrivateRoom, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.PrivateRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Tails, Area.PrivateRoom, Area.ECDeck, True): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Tails, Area.ECPool, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECPool, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Tails, Area.ECPool, Area.SkyDeck, False): ([ONLY_RANDO], [ONLY_RANDO], [], [], []),
    (Character.Tails, Area.ECInside, Area.ECOutside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Tails, Area.ECInside, Area.ECOutside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Tails, Area.ECInside, Area.ECDeck, False): (
        [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess],
        [Egglift, ECSwitchAccess]),
    (Character.Tails, Area.ECInside, Area.ECBridge, False): (
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess],
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess]),
    (Character.Tails, Area.ECInside, Area.HotShelter, False): (
        [ONLY_RANDO], [ONLY_RANDO], [], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Tails, Area.ECInside, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECInside, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECInside, Area.WarpHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECInside, Area.Arsenal, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.ECInside, Area.WaterTank, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.HedgehogHammer, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.HedgehogHammer, Area.PrisonHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.PrisonHall, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.Arsenal, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.WaterTank, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.WarpHall, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Tails, Area.WarpHall, Area.ECChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.CityHall, Area.SSMain, False): (
        [PolicePass], [PolicePass], [PolicePass], [PolicePass], [PolicePass]),
    (Character.Knuckles, Area.CityHall, Area.SpeedHighway, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.CityHall, Area.Chaos0, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.CityHall, Area.Sewers, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Knuckles, Area.Sewers, Area.CityHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.Sewers, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.Station, Area.SSMain, False): (
        [StationKey], [StationKey], [StationKey], [StationKey], [StationKey]),
    (Character.Knuckles, Area.Station, Area.MRMain, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Knuckles, Area.Station, Area.Casino, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Knuckles, Area.Casino, Area.Station, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Knuckles, Area.Casino, Area.Casinopolis, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Knuckles, Area.Casino, Area.Hotel, False): (
        [CasinoKey], [CasinoKey], [CasinoKey], [[CasinoKey], [ShutterKey]], []),
    (Character.Knuckles, Area.Casino, Area.EggWalker, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.SSMain, Area.Hotel, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Knuckles, Area.SSMain, Area.Station, False): ([StationKey], [StationKey], [], [], []),
    (Character.Knuckles, Area.SSMain, Area.CityHall, False): ([PolicePass], [PolicePass], [], [], []),
    (Character.Knuckles, Area.SSMain, Area.ECOutside, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Knuckles, Area.SSMain, Area.SpeedHighway, False): ([ONLY_RANDO], [ONLY_RANDO], [], [], []),
    (Character.Knuckles, Area.SSMain, Area.TPTunnel, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Knuckles, Area.TPTunnel, Area.SSMain, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Knuckles, Area.TPTunnel, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.TPTunnel, Area.TPLobby, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.TPLobby, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.TPLobby, Area.TwinklePark, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.TPLobby, Area.TwinkleCircuit, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.Hotel, Area.SSMain, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Knuckles, Area.Hotel, Area.Casino, False): ([CasinoKey], [CasinoKey], [], [], []),
    (Character.Knuckles, Area.Hotel, Area.SSChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.Hotel, Area.Chaos2, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.Hotel, Area.HotelPool, False): ([PoolKey], [PoolKey], [], [], []),
    (Character.Knuckles, Area.HotelPool, Area.Hotel, False): ([PoolKey], [PoolKey], [PoolKey], [PoolKey], [PoolKey]),
    (Character.Knuckles, Area.HotelPool, Area.EmeraldCoast, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.MRMain, Area.Station, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Knuckles, Area.MRMain, Area.ECOutside, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Knuckles, Area.MRMain, Area.WindyValley, False): (
        [WindStone], [WindStone], [WindStone], [WindStone], [WindStone]),
    (Character.Knuckles, Area.MRMain, Area.Jungle, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Knuckles, Area.MRMain, Area.Chaos4, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.MRMain, Area.EggHornet, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.MRMain, Area.SkyChase1, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.MRMain, Area.MRChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.MRMain, Area.AngelIsland, False): ([Dynamite], [Dynamite], [], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.MRMain, False): ([Dynamite], [Dynamite], [], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.IceCave, False): ([IceStone], [IceStone], [], [IceStone], [[IceStone],
                                                                                                           [
                                                                                                               ShovelClaw]]),
    (Character.Knuckles, Area.AngelIsland, Area.RedMountain, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Knuckles, Area.AngelIsland, Area.PastAltar, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Knuckles, Area.IceCave, Area.AngelIsland, False): (
        [IceStone], [IceStone], [IceStone], [IceStone], [IceStone]),
    (Character.Knuckles, Area.IceCave, Area.IceCap, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.PastAltar, Area.AngelIsland, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Knuckles, Area.PastAltar, Area.PastMain, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.PastMain, Area.PastAltar, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.PastMain, Area.Jungle, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Knuckles, Area.Jungle, Area.PastMain, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Knuckles, Area.Jungle, Area.MRMain, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Knuckles, Area.Jungle, Area.LostWorld, False): ([ONLY_RANDO], [ONLY_RANDO], [], [], []),
    (Character.Knuckles, Area.Jungle, Area.LostWorld, True): (
        [EMBLEM_BLOCKED, ShovelClaw], [EMBLEM_BLOCKED, ShovelClaw], [EMBLEM_BLOCKED, ShovelClaw],
        [EMBLEM_BLOCKED, ShovelClaw], [EMBLEM_BLOCKED, ShovelClaw]),
    (Character.Knuckles, Area.Jungle, Area.SandHill, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.Jungle, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.FinalEggTower, Area.Jungle, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.FinalEggTower, Area.FinalEgg, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.FinalEggTower, Area.FinalEgg, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.FinalEggTower, Area.BetaEggViper, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.FinalEggTower, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECOutside, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Knuckles, Area.ECOutside, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Knuckles, Area.ECOutside, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.ECOutside, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECOutside, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Knuckles, Area.ECOutside, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Knuckles, Area.ECOutside, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECOutside, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECBridge, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Knuckles, Area.ECBridge, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Knuckles, Area.ECBridge, Area.SkyDeck, False): (
        [ONLY_RANDO], [ONLY_RANDO], [], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.ECBridge, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.ECBridge, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECBridge, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Knuckles, Area.ECDeck, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECDeck, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECDeck, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECDeck, Area.PrivateRoom, True): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECDeck, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Knuckles, Area.CaptainRoom, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.CaptainRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Knuckles, Area.CaptainRoom, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.PrivateRoom, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.PrivateRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Knuckles, Area.PrivateRoom, Area.ECDeck, True): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Knuckles, Area.ECPool, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECPool, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Knuckles, Area.ECPool, Area.SkyDeck, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECInside, Area.ECOutside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Knuckles, Area.ECInside, Area.ECOutside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Knuckles, Area.ECInside, Area.ECDeck, False): (
        [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess],
        [Egglift, ECSwitchAccess]),
    (Character.Knuckles, Area.ECInside, Area.ECBridge, False): (
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess],
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess]),
    (Character.Knuckles, Area.ECInside, Area.HotShelter, False): (
        [ONLY_RANDO], [ONLY_RANDO], [], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Knuckles, Area.ECInside, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECInside, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECInside, Area.WarpHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECInside, Area.Arsenal, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.ECInside, Area.WaterTank, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.HedgehogHammer, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.HedgehogHammer, Area.PrisonHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.PrisonHall, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.Arsenal, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.WaterTank, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.WarpHall, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Knuckles, Area.WarpHall, Area.ECChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.CityHall, Area.SSMain, False): ([PolicePass], [PolicePass], [], [PolicePass], [PolicePass]),
    (Character.Amy, Area.CityHall, Area.SpeedHighway, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.CityHall, Area.Chaos0, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.CityHall, Area.Sewers, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], []),
    (Character.Amy, Area.Sewers, Area.CityHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.Sewers, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.Station, Area.SSMain, False): (
        [StationKey], [StationKey], [StationKey], [StationKey], [StationKey]),
    (Character.Amy, Area.Station, Area.MRMain, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Amy, Area.Station, Area.Casino, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Amy, Area.Casino, Area.Station, False): (
        [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey]),
    (Character.Amy, Area.Casino, Area.Casinopolis, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.Casino, Area.Hotel, False): ([CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey]),
    (Character.Amy, Area.Casino, Area.EggWalker, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.SSMain, Area.Hotel, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Amy, Area.SSMain, Area.Station, False): ([StationKey], [StationKey], [], [], []),
    (Character.Amy, Area.SSMain, Area.CityHall, False): ([PolicePass], [PolicePass], [PolicePass], [], []),
    (Character.Amy, Area.SSMain, Area.ECOutside, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Amy, Area.SSMain, Area.SpeedHighway, False): (
        [ONLY_RANDO, EmployeeCard], [ONLY_RANDO, EmployeeCard], [], [], []),
    (Character.Amy, Area.SSMain, Area.TPTunnel, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Amy, Area.TPTunnel, Area.SSMain, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Amy, Area.TPTunnel, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.TPTunnel, Area.TPLobby, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.TPLobby, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.TPLobby, Area.TwinklePark, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.TPLobby, Area.TwinkleCircuit, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.Hotel, Area.SSMain, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Amy, Area.Hotel, Area.Casino, False): ([CasinoKey], [CasinoKey], [], [], []),
    (Character.Amy, Area.Hotel, Area.SSChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.Hotel, Area.Chaos2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.Hotel, Area.HotelPool, False): ([PoolKey], [PoolKey], [PoolKey], [PoolKey], [PoolKey]),
    (Character.Amy, Area.HotelPool, Area.Hotel, False): ([PoolKey], [PoolKey], [PoolKey], [PoolKey], [PoolKey]),
    (Character.Amy, Area.HotelPool, Area.EmeraldCoast, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.MRMain, Area.Station, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Amy, Area.MRMain, Area.ECOutside, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Amy, Area.MRMain, Area.WindyValley, False): (
        [WindStone], [WindStone], [WindStone], [WindStone], [WindStone]),
    (Character.Amy, Area.MRMain, Area.Jungle, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Amy, Area.MRMain, Area.Chaos4, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.MRMain, Area.EggHornet, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.MRMain, Area.SkyChase1, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.MRMain, Area.MRChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.MRMain, Area.AngelIsland, False): ([Dynamite], [Dynamite], [Dynamite], [Dynamite], [Dynamite]),
    (Character.Amy, Area.AngelIsland, Area.MRMain, False): ([Dynamite], [Dynamite], [Dynamite], [Dynamite], [Dynamite]),
    (Character.Amy, Area.AngelIsland, Area.IceCave, False): (
        [IceStone], [IceStone], [IceStone], [IceStone], [IceStone]),
    (Character.Amy, Area.AngelIsland, Area.RedMountain, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.AngelIsland, Area.PastAltar, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Amy, Area.IceCave, Area.AngelIsland, False): (
        [IceStone], [IceStone], [IceStone], [IceStone], [IceStone]),
    (Character.Amy, Area.IceCave, Area.IceCap, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.PastAltar, Area.AngelIsland, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Amy, Area.PastAltar, Area.PastMain, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.PastMain, Area.PastAltar, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.PastMain, Area.Jungle, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Amy, Area.Jungle, Area.PastMain, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Amy, Area.Jungle, Area.MRMain, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Amy, Area.Jungle, Area.LostWorld, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.Jungle, Area.LostWorld, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.Jungle, Area.SandHill, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.Jungle, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.FinalEggTower, Area.Jungle, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.FinalEggTower, Area.FinalEgg, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.FinalEggTower, Area.FinalEgg, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.FinalEggTower, Area.BetaEggViper, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.FinalEggTower, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECOutside, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Amy, Area.ECOutside, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Amy, Area.ECOutside, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.ECOutside, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECOutside, Area.ECInside, False): ([Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Amy, Area.ECOutside, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Amy, Area.ECOutside, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECOutside, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECBridge, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Amy, Area.ECBridge, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Amy, Area.ECBridge, Area.SkyDeck, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.ECBridge, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.ECBridge, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECBridge, Area.ECInside, False): ([Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Amy, Area.ECDeck, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECDeck, Area.CaptainRoom, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.ECDeck, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECDeck, Area.PrivateRoom, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.ECDeck, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Amy, Area.CaptainRoom, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.CaptainRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Amy, Area.CaptainRoom, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.PrivateRoom, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.PrivateRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Amy, Area.PrivateRoom, Area.ECDeck, True): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Amy, Area.ECPool, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECPool, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Amy, Area.ECPool, Area.SkyDeck, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Amy, Area.ECInside, Area.ECOutside, False): ([Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Amy, Area.ECInside, Area.ECOutside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Amy, Area.ECInside, Area.ECDeck, False): (
        [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess],
        [Egglift, ECSwitchAccess]),
    (Character.Amy, Area.ECInside, Area.ECBridge, False): (
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess],
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess]),
    (Character.Amy, Area.ECInside, Area.HotShelter, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECInside, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECInside, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECInside, Area.WarpHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECInside, Area.Arsenal, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.ECInside, Area.WaterTank, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.HedgehogHammer, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.HedgehogHammer, Area.PrisonHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.PrisonHall, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.Arsenal, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.WaterTank, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], []),
    (Character.Amy, Area.WarpHall, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Amy, Area.WarpHall, Area.ECChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.CityHall, Area.SSMain, False): (
        [PolicePass], [PolicePass], [PolicePass], [PolicePass], [PolicePass]),
    (Character.Big, Area.CityHall, Area.SpeedHighway, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.CityHall, Area.Chaos0, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.CityHall, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.Sewers, Area.CityHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.Sewers, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.Station, Area.SSMain, False): (
        [StationKey], [StationKey], [StationKey], [StationKey], [StationKey]),
    (Character.Big, Area.Station, Area.MRMain, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Big, Area.Station, Area.Casino, False): (
        [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey]),
    (Character.Big, Area.Casino, Area.Station, False): (
        [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey]),
    (Character.Big, Area.Casino, Area.Casinopolis, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.Casino, Area.Hotel, False): ([CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey]),
    (Character.Big, Area.Casino, Area.EggWalker, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.SSMain, Area.Hotel, False): ([HotelKey], [HotelKey], [HotelKey], [[HotelKey],
                                                                                           [LifeBelt]], []),
    (Character.Big, Area.SSMain, Area.Station, False): ([StationKey], [StationKey], [], [], []),
    (Character.Big, Area.SSMain, Area.CityHall, False): (
        [PolicePass], [PolicePass], [PolicePass], [PolicePass], [PolicePass]),
    (Character.Big, Area.SSMain, Area.ECOutside, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Big, Area.SSMain, Area.SpeedHighway, False): (
        [ONLY_RANDO, EmployeeCard], [ONLY_RANDO, EmployeeCard], [], [], []),
    (Character.Big, Area.SSMain, Area.TPTunnel, False): ([TPTicket], [TPTicket], [TPTicket], [TPTicket], [TPTicket]),
    (Character.Big, Area.TPTunnel, Area.SSMain, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Big, Area.TPTunnel, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.TPTunnel, Area.TPLobby, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.TPLobby, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.TPLobby, Area.TwinklePark, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.TPLobby, Area.TwinkleCircuit, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.Hotel, Area.SSMain, False): ([HotelKey], [HotelKey], [HotelKey], [HotelKey], [HotelKey]),
    (Character.Big, Area.Hotel, Area.Casino, False): ([CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey]),
    (Character.Big, Area.Hotel, Area.SSChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.Hotel, Area.Chaos2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.Hotel, Area.HotelPool, False): ([PoolKey], [PoolKey], [PoolKey], [PoolKey], [PoolKey]),
    (Character.Big, Area.HotelPool, Area.Hotel, False): ([PoolKey], [PoolKey], [PoolKey], [PoolKey], [PoolKey]),
    (Character.Big, Area.HotelPool, Area.EmeraldCoast, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.MRMain, Area.Station, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Big, Area.MRMain, Area.ECOutside, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Big, Area.MRMain, Area.WindyValley, False): (
        [WindStone], [WindStone], [WindStone], [WindStone], [WindStone]),
    (Character.Big, Area.MRMain, Area.Jungle, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Big, Area.MRMain, Area.Chaos4, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.MRMain, Area.EggHornet, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.MRMain, Area.SkyChase1, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.MRMain, Area.MRChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.MRMain, Area.AngelIsland, False): ([Dynamite], [Dynamite], [Dynamite], [Dynamite], [Dynamite]),
    (Character.Big, Area.AngelIsland, Area.MRMain, False): ([Dynamite], [Dynamite], [Dynamite], [Dynamite], [Dynamite]),
    (Character.Big, Area.AngelIsland, Area.IceCave, False): (
        [IceStone], [IceStone], [IceStone], [IceStone], [IceStone]),
    (Character.Big, Area.AngelIsland, Area.RedMountain, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.AngelIsland, Area.PastAltar, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Big, Area.IceCave, Area.AngelIsland, False): (
        [IceStone], [IceStone], [IceStone], [IceStone], [IceStone]),
    (Character.Big, Area.IceCave, Area.IceCap, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.PastAltar, Area.AngelIsland, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Big, Area.PastAltar, Area.PastMain, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.PastMain, Area.PastAltar, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.PastMain, Area.Jungle, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Big, Area.Jungle, Area.PastMain, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Big, Area.Jungle, Area.MRMain, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Big, Area.Jungle, Area.LostWorld, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.Jungle, Area.LostWorld, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.Jungle, Area.SandHill, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.Jungle, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.FinalEggTower, Area.Jungle, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.FinalEggTower, Area.FinalEgg, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.FinalEggTower, Area.FinalEgg, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.FinalEggTower, Area.BetaEggViper, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.FinalEggTower, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECOutside, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Big, Area.ECOutside, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Big, Area.ECOutside, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.ECOutside, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECOutside, Area.ECInside, False): ([Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Big, Area.ECOutside, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Big, Area.ECOutside, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECOutside, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECBridge, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Big, Area.ECBridge, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Big, Area.ECBridge, Area.SkyDeck, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.ECBridge, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.ECBridge, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECBridge, Area.ECInside, False): ([Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Big, Area.ECDeck, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECDeck, Area.CaptainRoom, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.ECDeck, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECDeck, Area.PrivateRoom, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.ECDeck, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Big, Area.CaptainRoom, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.CaptainRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Big, Area.CaptainRoom, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.PrivateRoom, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.PrivateRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Big, Area.PrivateRoom, Area.ECDeck, True): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Big, Area.ECPool, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECPool, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Big, Area.ECPool, Area.SkyDeck, False): ([ONLY_RANDO], [ONLY_RANDO], [], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Big, Area.ECInside, Area.ECOutside, False): ([Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Big, Area.ECInside, Area.ECOutside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Big, Area.ECInside, Area.ECDeck, False): (
        [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess],
        [Egglift, ECSwitchAccess]),
    (Character.Big, Area.ECInside, Area.ECBridge, False): (
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess],
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess]),
    (Character.Big, Area.ECInside, Area.HotShelter, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECInside, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECInside, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECInside, Area.WarpHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECInside, Area.Arsenal, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.ECInside, Area.WaterTank, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.HedgehogHammer, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.HedgehogHammer, Area.PrisonHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.PrisonHall, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.Arsenal, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.WaterTank, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.WarpHall, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Big, Area.WarpHall, Area.ECChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.CityHall, Area.SSMain, False): (
        [PolicePass], [PolicePass], [PolicePass], [PolicePass], [PolicePass]),
    (Character.Gamma, Area.CityHall, Area.SpeedHighway, False): (
        [ONLY_RANDO], [ONLY_RANDO], [], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.CityHall, Area.Chaos0, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.CityHall, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.Sewers, Area.CityHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.Sewers, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.Station, Area.SSMain, False): (
        [StationKey], [StationKey], [StationKey], [StationKey], [StationKey]),
    (Character.Gamma, Area.Station, Area.MRMain, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Gamma, Area.Station, Area.Casino, False): ([ShutterKey], [ShutterKey], [], [], []),
    (Character.Gamma, Area.Casino, Area.Station, False): (
        [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey], [ShutterKey]),
    (Character.Gamma, Area.Casino, Area.Casinopolis, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.Casino, Area.Hotel, False): (
        [CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey], [CasinoKey]),
    (Character.Gamma, Area.Casino, Area.EggWalker, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.SSMain, Area.Hotel, False): ([HotelKey], [HotelKey], [HotelKey], [], []),
    (Character.Gamma, Area.SSMain, Area.Station, False): ([StationKey], [StationKey], [], [], []),
    (Character.Gamma, Area.SSMain, Area.CityHall, False): ([PolicePass], [PolicePass], [], [PolicePass], [PolicePass]),
    (Character.Gamma, Area.SSMain, Area.ECOutside, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Gamma, Area.SSMain, Area.SpeedHighway, False): (
        [ONLY_RANDO, EmployeeCard], [ONLY_RANDO, EmployeeCard], [ONLY_RANDO, EmployeeCard], [], []),
    (Character.Gamma, Area.SSMain, Area.TPTunnel, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Gamma, Area.TPTunnel, Area.SSMain, False): ([TPTicket], [TPTicket], [], [], []),
    (Character.Gamma, Area.TPTunnel, Area.Sewers, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.TPTunnel, Area.TPLobby, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.TPLobby, Area.TPTunnel, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.TPLobby, Area.TwinklePark, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.TPLobby, Area.TwinkleCircuit, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.Hotel, Area.SSMain, False): ([HotelKey], [HotelKey], [], [], []),
    (Character.Gamma, Area.Hotel, Area.Casino, False): ([CasinoKey], [CasinoKey], [], [[CasinoKey],
                                                                                       [JetBooster]], []),
    (Character.Gamma, Area.Hotel, Area.SSChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.Hotel, Area.Chaos2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.Hotel, Area.HotelPool, False): ([PoolKey], [PoolKey], [PoolKey], [PoolKey], [PoolKey]),
    (Character.Gamma, Area.HotelPool, Area.Hotel, False): ([PoolKey], [PoolKey], [PoolKey], [PoolKey], [PoolKey]),
    (Character.Gamma, Area.HotelPool, Area.EmeraldCoast, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.MRMain, Area.Station, False): ([Train], [Train], [Train], [Train], [Train]),
    (Character.Gamma, Area.MRMain, Area.ECOutside, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Gamma, Area.MRMain, Area.WindyValley, False): (
        [WindStone], [WindStone], [WindStone], [WindStone], [WindStone]),
    (Character.Gamma, Area.MRMain, Area.Jungle, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Gamma, Area.MRMain, Area.Chaos4, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.MRMain, Area.EggHornet, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.MRMain, Area.SkyChase1, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.MRMain, Area.MRChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.MRMain, Area.AngelIsland, False): (
        [Dynamite], [Dynamite], [[Dynamite], [JetBooster]], [[Dynamite],
                                                             [JetBooster]], [[Dynamite],
                                                                             [JetBooster]]),
    (Character.Gamma, Area.AngelIsland, Area.MRMain, False): ([Dynamite], [Dynamite], [[Dynamite],
                                                                                       [JetBooster]], [[Dynamite],
                                                                                                       [JetBooster]],
                                                              [[Dynamite],
                                                               [JetBooster]]),
    (Character.Gamma, Area.AngelIsland, Area.IceCave, False): (
        [IceStone], [IceStone], [[IceStone], [JetBooster]], [[IceStone], [JetBooster]], [[IceStone], [JetBooster]]),
    (Character.Gamma, Area.AngelIsland, Area.RedMountain, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.AngelIsland, Area.PastAltar, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Gamma, Area.IceCave, Area.AngelIsland, False): (
        [IceStone], [IceStone], [IceStone], [IceStone], [IceStone]),
    (Character.Gamma, Area.IceCave, Area.IceCap, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.PastAltar, Area.AngelIsland, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Gamma, Area.PastAltar, Area.PastMain, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.PastMain, Area.PastAltar, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.PastMain, Area.Jungle, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Gamma, Area.Jungle, Area.PastMain, False): (
        [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine], [TimeMachine]),
    (Character.Gamma, Area.Jungle, Area.MRMain, False): (
        [JungleCart], [JungleCart], [JungleCart], [JungleCart], [JungleCart]),
    (Character.Gamma, Area.Jungle, Area.LostWorld, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.Jungle, Area.LostWorld, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.Jungle, Area.SandHill, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.Jungle, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.FinalEggTower, Area.Jungle, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.FinalEggTower, Area.FinalEgg, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.FinalEggTower, Area.FinalEgg, True): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.FinalEggTower, Area.BetaEggViper, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.FinalEggTower, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECOutside, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Gamma, Area.ECOutside, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Gamma, Area.ECOutside, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.ECOutside, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECOutside, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Gamma, Area.ECOutside, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Gamma, Area.ECOutside, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECOutside, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECBridge, Area.SSMain, False): ([Boat], [Boat], [Boat], [Boat], [Boat]),
    (Character.Gamma, Area.ECBridge, Area.MRMain, False): ([Raft], [Raft], [Raft], [Raft], [Raft]),
    (Character.Gamma, Area.ECBridge, Area.SkyDeck, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.ECBridge, Area.SkyChase2, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.ECBridge, Area.Chaos6ZeroBeta, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECBridge, Area.ECInside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Gamma, Area.ECDeck, Area.ECPool, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECDeck, Area.CaptainRoom, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.ECDeck, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECDeck, Area.PrivateRoom, True): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.ECDeck, Area.ECInside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Gamma, Area.CaptainRoom, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.CaptainRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Gamma, Area.CaptainRoom, Area.PrivateRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.PrivateRoom, Area.CaptainRoom, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.PrivateRoom, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Gamma, Area.PrivateRoom, Area.ECDeck, True): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Gamma, Area.ECPool, Area.ECOutside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECPool, Area.ECDeck, False): (
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess],
        [EMBLEM_BLOCKED, ECSwitchAccess], [EMBLEM_BLOCKED, ECSwitchAccess]),
    (Character.Gamma, Area.ECPool, Area.SkyDeck, False): (
        [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO], [ONLY_RANDO]),
    (Character.Gamma, Area.ECInside, Area.ECOutside, False): (
        [Monorail], [Monorail], [Monorail], [Monorail], [Monorail]),
    (Character.Gamma, Area.ECInside, Area.ECOutside, False): ([Egglift], [Egglift], [Egglift], [Egglift], [Egglift]),
    (Character.Gamma, Area.ECInside, Area.ECDeck, False): (
        [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess], [Egglift, ECSwitchAccess],
        [Egglift, ECSwitchAccess]),
    (Character.Gamma, Area.ECInside, Area.ECBridge, False): (
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess],
        [Egglift, Monorail, ECSwitchAccess], [Egglift, Monorail, ECSwitchAccess]),
    (Character.Gamma, Area.ECInside, Area.HotShelter, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [[EMBLEM_BLOCKED], [JetBooster]], [[EMBLEM_BLOCKED], [JetBooster]],
        [[EMBLEM_BLOCKED], [JetBooster]]),
    (Character.Gamma, Area.ECInside, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [[EMBLEM_BLOCKED], [JetBooster]], [[EMBLEM_BLOCKED], [JetBooster]],
        [[EMBLEM_BLOCKED], [JetBooster]]),
    (Character.Gamma, Area.ECInside, Area.FinalEggTower, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.ECInside, Area.WarpHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [[EMBLEM_BLOCKED], [JetBooster]], [[EMBLEM_BLOCKED], [JetBooster]],
        [[EMBLEM_BLOCKED], [JetBooster]]),
    (Character.Gamma, Area.ECInside, Area.Arsenal, False): ([EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [], [], []),
    (Character.Gamma, Area.ECInside, Area.WaterTank, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [[EMBLEM_BLOCKED], [JetBooster]], [[EMBLEM_BLOCKED], [JetBooster]],
        [[EMBLEM_BLOCKED], [JetBooster]]),
    (Character.Gamma, Area.HedgehogHammer, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.HedgehogHammer, Area.PrisonHall, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.PrisonHall, Area.HedgehogHammer, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.Arsenal, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.WaterTank, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.WarpHall, Area.ECInside, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
    (Character.Gamma, Area.WarpHall, Area.ECChaoGarden, False): (
        [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED], [EMBLEM_BLOCKED]),
}

level_location_table: List[LevelLocation] = [
    LevelLocation(6002, Area.TwinklePark, Character.Big, LevelMission.C, [], [], [], [], []),
    LevelLocation(6001, Area.TwinklePark, Character.Big, LevelMission.B, [Lure1, Lure2, Lure3, Lure4], [], [], [], []),
    LevelLocation(6000, Area.TwinklePark, Character.Big, LevelMission.A, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4]),
    LevelLocation(6003, Area.TwinklePark, Character.Big, LevelMission.S, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4]),
    LevelLocation(3002, Area.SpeedHighway, Character.Knuckles, LevelMission.C, [], [], [], [], []),
    LevelLocation(3001, Area.SpeedHighway, Character.Knuckles, LevelMission.B, [], [], [], [], []),
    LevelLocation(3000, Area.SpeedHighway, Character.Knuckles, LevelMission.A, [], [], [], [], []),
    LevelLocation(3003, Area.SpeedHighway, Character.Knuckles, LevelMission.S, [], [], [], [], []),
    LevelLocation(1002, Area.EmeraldCoast, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1001, Area.EmeraldCoast, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1000, Area.EmeraldCoast, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1003, Area.EmeraldCoast, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(6202, Area.EmeraldCoast, Character.Big, LevelMission.C, [], [], [], [], []),
    LevelLocation(6201, Area.EmeraldCoast, Character.Big, LevelMission.B, [Lure1, Lure2, Lure3, Lure4], [], [], [], []),
    LevelLocation(6200, Area.EmeraldCoast, Character.Big, LevelMission.A, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4]),
    LevelLocation(6203, Area.EmeraldCoast, Character.Big, LevelMission.S, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4]),
    LevelLocation(5102, Area.EmeraldCoast, Character.Gamma, LevelMission.C, [], [], [], [], []),
    LevelLocation(5101, Area.EmeraldCoast, Character.Gamma, LevelMission.B, [], [], [], [], []),
    LevelLocation(5100, Area.EmeraldCoast, Character.Gamma, LevelMission.A, [], [], [], [], []),
    LevelLocation(5103, Area.EmeraldCoast, Character.Gamma, LevelMission.S, [], [], [], [], []),
    LevelLocation(1202, Area.Casinopolis, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1201, Area.Casinopolis, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1200, Area.Casinopolis, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1203, Area.Casinopolis, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(2102, Area.Casinopolis, Character.Tails, LevelMission.C, [], [], [], [], []),
    LevelLocation(2101, Area.Casinopolis, Character.Tails, LevelMission.B, [], [], [], [], []),
    LevelLocation(2100, Area.Casinopolis, Character.Tails, LevelMission.A, [JetAnklet], [], [], [], []),
    LevelLocation(2103, Area.Casinopolis, Character.Tails, LevelMission.S, [JetAnklet], [], [], [], []),
    LevelLocation(3102, Area.Casinopolis, Character.Knuckles, LevelMission.C, [], [], [], [], []),
    LevelLocation(3101, Area.Casinopolis, Character.Knuckles, LevelMission.B, [], [], [], [], []),
    LevelLocation(3100, Area.Casinopolis, Character.Knuckles, LevelMission.A, [], [], [], [], []),
    LevelLocation(3103, Area.Casinopolis, Character.Knuckles, LevelMission.S, [], [], [], [], []),
    LevelLocation(1402, Area.TwinklePark, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1401, Area.TwinklePark, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1400, Area.TwinklePark, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1403, Area.TwinklePark, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(4002, Area.TwinklePark, Character.Amy, LevelMission.C, [], [], [], [], []),
    LevelLocation(4001, Area.TwinklePark, Character.Amy, LevelMission.B, [], [], [], [], []),
    LevelLocation(4000, Area.TwinklePark, Character.Amy, LevelMission.A, [], [], [], [], []),
    LevelLocation(4003, Area.TwinklePark, Character.Amy, LevelMission.S, [], [], [], [], []),
    LevelLocation(1502, Area.SpeedHighway, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1501, Area.SpeedHighway, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1500, Area.SpeedHighway, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1503, Area.SpeedHighway, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(2402, Area.SpeedHighway, Character.Tails, LevelMission.C, [], [], [], [], []),
    LevelLocation(2401, Area.SpeedHighway, Character.Tails, LevelMission.B, [], [], [], [], []),
    LevelLocation(2400, Area.SpeedHighway, Character.Tails, LevelMission.A, [JetAnklet], [], [], [], []),
    LevelLocation(2403, Area.SpeedHighway, Character.Tails, LevelMission.S, [JetAnklet], [], [], [], []),
    LevelLocation(1102, Area.WindyValley, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1101, Area.WindyValley, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1100, Area.WindyValley, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1103, Area.WindyValley, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(2002, Area.WindyValley, Character.Tails, LevelMission.C, [], [], [], [], []),
    LevelLocation(2001, Area.WindyValley, Character.Tails, LevelMission.B, [], [], [], [], []),
    LevelLocation(2000, Area.WindyValley, Character.Tails, LevelMission.A, [JetAnklet], [], [], [], []),
    LevelLocation(2003, Area.WindyValley, Character.Tails, LevelMission.S, [JetAnklet], [], [], [], []),
    LevelLocation(5202, Area.WindyValley, Character.Gamma, LevelMission.C, [JetBooster], [], [], [], []),
    LevelLocation(5201, Area.WindyValley, Character.Gamma, LevelMission.B, [JetBooster], [], [], [], []),
    LevelLocation(5200, Area.WindyValley, Character.Gamma, LevelMission.A, [JetBooster], [], [], [], []),
    LevelLocation(5203, Area.WindyValley, Character.Gamma, LevelMission.S, [JetBooster], [], [], [], []),
    LevelLocation(1302, Area.IceCap, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1301, Area.IceCap, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1300, Area.IceCap, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1303, Area.IceCap, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(2202, Area.IceCap, Character.Tails, LevelMission.C, [], [], [], [], []),
    LevelLocation(2201, Area.IceCap, Character.Tails, LevelMission.B, [], [], [], [], []),
    LevelLocation(2200, Area.IceCap, Character.Tails, LevelMission.A, [], [], [], [], []),
    LevelLocation(2203, Area.IceCap, Character.Tails, LevelMission.S, [], [], [], [], []),
    LevelLocation(6102, Area.IceCap, Character.Big, LevelMission.C, [], [], [], [], []),
    LevelLocation(6101, Area.IceCap, Character.Big, LevelMission.B, [Lure1, Lure2, Lure3, Lure4], [], [], [], []),
    LevelLocation(6100, Area.IceCap, Character.Big, LevelMission.A, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4]),
    LevelLocation(6103, Area.IceCap, Character.Big, LevelMission.S, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4]),
    LevelLocation(1602, Area.RedMountain, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1601, Area.RedMountain, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1600, Area.RedMountain, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1603, Area.RedMountain, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(3202, Area.RedMountain, Character.Knuckles, LevelMission.C, [ShovelClaw], [], [], [], []),
    LevelLocation(3201, Area.RedMountain, Character.Knuckles, LevelMission.B, [ShovelClaw], [], [], [], []),
    LevelLocation(3200, Area.RedMountain, Character.Knuckles, LevelMission.A, [ShovelClaw], [], [], [], []),
    LevelLocation(3203, Area.RedMountain, Character.Knuckles, LevelMission.S, [ShovelClaw], [], [], [], []),
    LevelLocation(5302, Area.RedMountain, Character.Gamma, LevelMission.C, [], [], [], [], []),
    LevelLocation(5301, Area.RedMountain, Character.Gamma, LevelMission.B, [], [], [], [], []),
    LevelLocation(5300, Area.RedMountain, Character.Gamma, LevelMission.A, [], [], [], [], []),
    LevelLocation(5303, Area.RedMountain, Character.Gamma, LevelMission.S, [], [], [], [], []),
    LevelLocation(1802, Area.LostWorld, Character.Sonic, LevelMission.C, [LightShoes], [], [], [], []),
    LevelLocation(1801, Area.LostWorld, Character.Sonic, LevelMission.B, [LightShoes], [], [], [], []),
    LevelLocation(1800, Area.LostWorld, Character.Sonic, LevelMission.A, [LightShoes], [], [], [], []),
    LevelLocation(1803, Area.LostWorld, Character.Sonic, LevelMission.S, [LightShoes], [], [], [], []),
    LevelLocation(3302, Area.LostWorld, Character.Knuckles, LevelMission.C, [ShovelClaw], [], [], [], []),
    LevelLocation(3301, Area.LostWorld, Character.Knuckles, LevelMission.B, [ShovelClaw], [], [], [], []),
    LevelLocation(3300, Area.LostWorld, Character.Knuckles, LevelMission.A, [ShovelClaw], [], [], [], []),
    LevelLocation(3303, Area.LostWorld, Character.Knuckles, LevelMission.S, [ShovelClaw], [], [], [], []),
    LevelLocation(1902, Area.FinalEgg, Character.Sonic, LevelMission.C, [LightShoes], [], [], [], []),
    LevelLocation(1901, Area.FinalEgg, Character.Sonic, LevelMission.B, [LightShoes], [], [], [], []),
    LevelLocation(1900, Area.FinalEgg, Character.Sonic, LevelMission.A, [LightShoes], [], [], [], []),
    LevelLocation(1903, Area.FinalEgg, Character.Sonic, LevelMission.S, [LightShoes], [], [], [], []),
    LevelLocation(4202, Area.FinalEgg, Character.Amy, LevelMission.C, [], [], [], [], []),
    LevelLocation(4201, Area.FinalEgg, Character.Amy, LevelMission.B, [], [], [], [], []),
    LevelLocation(4200, Area.FinalEgg, Character.Amy, LevelMission.A, [], [], [], [], []),
    LevelLocation(4203, Area.FinalEgg, Character.Amy, LevelMission.S, [], [], [], [], []),
    LevelLocation(5002, Area.FinalEgg, Character.Gamma, LevelMission.C, [], [], [], [], []),
    LevelLocation(5001, Area.FinalEgg, Character.Gamma, LevelMission.B, [], [], [], [], []),
    LevelLocation(5000, Area.FinalEgg, Character.Gamma, LevelMission.A, [], [], [], [], []),
    LevelLocation(5003, Area.FinalEgg, Character.Gamma, LevelMission.S, [], [], [], [], []),
    LevelLocation(1702, Area.SkyDeck, Character.Sonic, LevelMission.C, [], [], [], [], []),
    LevelLocation(1701, Area.SkyDeck, Character.Sonic, LevelMission.B, [], [], [], [], []),
    LevelLocation(1700, Area.SkyDeck, Character.Sonic, LevelMission.A, [], [], [], [], []),
    LevelLocation(1703, Area.SkyDeck, Character.Sonic, LevelMission.S, [], [], [], [], []),
    LevelLocation(2302, Area.SkyDeck, Character.Tails, LevelMission.C, [], [], [], [], []),
    LevelLocation(2301, Area.SkyDeck, Character.Tails, LevelMission.B, [], [], [], [], []),
    LevelLocation(2300, Area.SkyDeck, Character.Tails, LevelMission.A, [JetAnklet], [], [], [], []),
    LevelLocation(2303, Area.SkyDeck, Character.Tails, LevelMission.S, [JetAnklet], [], [], [], []),
    LevelLocation(3402, Area.SkyDeck, Character.Knuckles, LevelMission.C, [ShovelClaw], [], [], [], []),
    LevelLocation(3401, Area.SkyDeck, Character.Knuckles, LevelMission.B, [ShovelClaw], [], [], [], []),
    LevelLocation(3400, Area.SkyDeck, Character.Knuckles, LevelMission.A, [ShovelClaw], [], [], [], []),
    LevelLocation(3403, Area.SkyDeck, Character.Knuckles, LevelMission.S, [ShovelClaw], [], [], [], []),
    LevelLocation(4102, Area.HotShelter, Character.Amy, LevelMission.C, [], [], [], [], []),
    LevelLocation(4101, Area.HotShelter, Character.Amy, LevelMission.B, [], [], [], [], []),
    LevelLocation(4100, Area.HotShelter, Character.Amy, LevelMission.A, [], [], [], [], []),
    LevelLocation(4103, Area.HotShelter, Character.Amy, LevelMission.S, [], [], [], [], []),
    LevelLocation(6302, Area.HotShelter, Character.Big, LevelMission.C, [], [], [], [], []),
    LevelLocation(6301, Area.HotShelter, Character.Big, LevelMission.B, [Lure1, Lure2, Lure3, Lure4], [], [], [], []),
    LevelLocation(6300, Area.HotShelter, Character.Big, LevelMission.A, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [], [], []),
    LevelLocation(6303, Area.HotShelter, Character.Big, LevelMission.S, [Lure1, Lure2, Lure3, Lure4],
                  [Lure1, Lure2, Lure3, Lure4], [], [], []),
    LevelLocation(5402, Area.HotShelter, Character.Gamma, LevelMission.C, [JetBooster], [JetBooster], [], [], []),
    LevelLocation(5401, Area.HotShelter, Character.Gamma, LevelMission.B, [JetBooster], [JetBooster], [], [], []),
    LevelLocation(5400, Area.HotShelter, Character.Gamma, LevelMission.A, [JetBooster], [JetBooster], [], [], []),
    LevelLocation(5403, Area.HotShelter, Character.Gamma, LevelMission.S, [JetBooster], [JetBooster], [], [], []),
]

upgrade_location_table: List[UpgradeLocation] = [
    UpgradeLocation(100, LocationName.Sonic.LightShoes, Area.Sewers, Character.Sonic, [], [], [], [], []),
    UpgradeLocation(200, LocationName.Tails.JetAnklet, Area.SSMain, Character.Tails, [], [], [], [], []),
    UpgradeLocation(602, LocationName.Big.Lure1, Area.SSMain, Character.Big, [], [], [], [], []),
    UpgradeLocation(101, LocationName.Sonic.CrystalRing, Area.Hotel, Character.Sonic, [LightShoes], [], [], [], []),
    UpgradeLocation(300, LocationName.Knuckles.ShovelClaw, Area.MRMain, Character.Knuckles, [], [], [], [], []),
    UpgradeLocation(604, LocationName.Big.Lure3, Area.IceCap, Character.Big, [], [], [], [], []),
    UpgradeLocation(600, LocationName.Big.LifeBelt, Area.IceCave, Character.Big, [], [], [], [], []),
    UpgradeLocation(102, LocationName.Sonic.AncientLight, Area.AngelIsland, Character.Sonic, [], [], [], [], []),
    UpgradeLocation(301, LocationName.Knuckles.FightingGloves, Area.Jungle, Character.Knuckles, [], [], [], [], []),
    UpgradeLocation(603, LocationName.Big.Lure2, Area.Jungle, Character.Big, [], [], [], [], []),
    UpgradeLocation(601, LocationName.Big.PowerRod, Area.Jungle, Character.Big, [], [], [], [], []),
    UpgradeLocation(400, LocationName.Amy.WarriorFeather, Area.HedgehogHammer, Character.Amy, [], [], [], [], []),
    UpgradeLocation(401, LocationName.Amy.LongHammer, Area.HedgehogHammer, Character.Amy, [], [], [], [], []),
    UpgradeLocation(500, LocationName.Gamma.JetBooster, Area.Arsenal, Character.Gamma, [], [], [], [], []),
    UpgradeLocation(501, LocationName.Gamma.LaserBlaster, Area.WaterTank, Character.Gamma, [], [], [], [], []),
    UpgradeLocation(605, LocationName.Big.Lure4, Area.PrisonHall, Character.Big, [], [], [], [], []),
    UpgradeLocation(201, LocationName.Tails.RhythmBadge, Area.PastMain, Character.Tails, [], [], [], [], []),
]

field_emblem_location_table: List[EmblemLocation] = [
    EmblemLocation(10, Area.Station, [P_SONIC, P_KNUCKLES, P_TAILS, P_AMY, P_BIG, P_GAMMA_W_JB],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA], "Station Emblem"),
    EmblemLocation(11, Area.CityHall, [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA], "Burger Shop Emblem"),
    EmblemLocation(12, Area.CityHall, [P_TAILS, P_KNUCKLES_W_SC], [P_TAILS, P_KNUCKLES_W_SC],
                   [P_AMY, P_TAILS, P_KNUCKLES, P_SONIC_W_LS], [P_AMY, P_TAILS, P_KNUCKLES],
                   [P_AMY, P_TAILS, P_KNUCKLES], "City Hall Emblem"),
    EmblemLocation(13, Area.Casino, [P_TAILS], [P_TAILS], [P_TAILS, P_SONIC, P_KNUCKLES, P_AMY], [P_TAILS, P_SONIC],
                   [P_TAILS, P_SONIC, P_KNUCKLES], "Casino Emblem"),
    EmblemLocation(20, Area.MRMain, [P_TAILS, P_KNUCKLES, P_GAMMA_W_JB], [P_SONIC, P_TAILS, P_KNUCKLES, P_GAMMA_W_JB],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_GAMMA_W_JB, P_AMY],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_GAMMA_W_JB, P_AMY],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_GAMMA_W_JB, P_AMY], "Tails' Workshop Emblem"),
    EmblemLocation(21, Area.AngelIsland, [P_KNUCKLES], [P_TAILS, P_KNUCKLES, P_GAMMA_W_JB],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_GAMMA_W_JB], [P_SONIC, P_TAILS, P_KNUCKLES, P_GAMMA_W_JB],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_GAMMA_W_JB], "Shrine Emblem"),
    EmblemLocation(22, Area.Jungle, [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA], "Jungle Path Emblem"),
    EmblemLocation(23, Area.Jungle, [P_TAILS, P_KNUCKLES], [P_SONIC, P_TAILS, P_KNUCKLES],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_BIG], [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_GAMMA, P_BIG],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_GAMMA, P_BIG], "Tree Stump Emblem"),
    EmblemLocation(30, Area.ECPool, [P_TAILS, P_KNUCKLES], [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY], [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_GAMMA], "Pool Emblem"),
    EmblemLocation(31, Area.ECDeck, [P_TAILS], [P_TAILS, P_SONIC, P_KNUCKLES],
                   [P_TAILS, P_SONIC, P_KNUCKLES, P_AMY, P_GAMMA_W_JB], [P_TAILS, P_SONIC, P_KNUCKLES, P_AMY],
                   [P_TAILS, P_SONIC, P_KNUCKLES, P_AMY], "Spinning Platform Emblem"),
    EmblemLocation(32, Area.PrivateRoom, [P_TAILS, P_SONIC], [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                   [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA], "Hidden Bed Emblem"),
    EmblemLocation(33, Area.ECBridge, [P_SONIC], [P_SONIC, P_BIG, P_KNUCKLES, P_AMY],
                   [P_SONIC, P_BIG, P_KNUCKLES, P_AMY, P_TAILS], [P_SONIC, P_BIG, P_KNUCKLES, P_AMY, P_TAILS],
                   [P_SONIC, P_BIG, P_KNUCKLES, P_AMY, P_TAILS], "Main Platform Emblem"),
]

mission_location_table: List[MissionLocation] = [
    MissionLocation(801, Area.SSMain, Area.SSMain, Character.Sonic, 1, [PolicePass], [PolicePass], [PolicePass],
                    [PolicePass], [PolicePass]),
    MissionLocation(802, Area.MRMain, Area.MRMain, Character.Sonic, 2, [], [], [], [], []),
    MissionLocation(803, Area.HotelPool, Area.HotelPool, Character.Sonic, 3, [LightShoes], [LightShoes], [LightShoes],
                    [LightShoes], [LightShoes]),
    MissionLocation(804, Area.MRMain, Area.MRMain, Character.Tails, 4, [], [], [], [], []),
    MissionLocation(805, Area.Casino, Area.Casino, Character.Knuckles, 5, [], [], [], [], []),
    MissionLocation(806, Area.MRMain, Area.MRMain, Character.Amy, 6, [], [], [], [], []),
    MissionLocation(807, Area.MRMain, Area.FinalEggTower, Character.Gamma, 7, [], [], [], [], []),
    MissionLocation(808, Area.SSMain, Area.Sewers, Character.Big, 8, [], [], [], [], []),
    MissionLocation(809, Area.SSMain, Area.EmeraldCoast, Character.Sonic, 9, [], [], [], [], []),
    MissionLocation(810, Area.Hotel, Area.SSChaoGarden, Character.Tails, 10, [], [], [], [], []),
    MissionLocation(811, Area.MRMain, Area.WindyValley, Character.Sonic, 11, [], [], [], [], []),
    MissionLocation(812, Area.MRMain, Area.MRMain, Character.Knuckles, 12, [ShovelClaw], [ShovelClaw], [ShovelClaw], [],
                    []),
    MissionLocation(813, Area.Casino, Area.Casinopolis, Character.Sonic, 13, [], [], [], [], []),
    MissionLocation(814, Area.SSMain, Area.HotelPool, Character.Big, 14, [], [], [], [], []),
    MissionLocation(815, Area.MRMain, Area.WindyValley, Character.Sonic, 15, [], [], [], [], []),
    MissionLocation(816, Area.MRMain, Area.WindyValley, Character.Tails, 16, [], [], [], [], []),
    MissionLocation(817, Area.CityHall, Area.Casinopolis, Character.Sonic, 17, [], [], [], [], []),
    MissionLocation(818, Area.Station, Area.TwinklePark, Character.Amy, 18, [], [], [], [], []),
    MissionLocation(819, Area.SSMain, Area.TwinklePark, Character.Amy, 19, [], [], [], [], []),
    MissionLocation(820, Area.IceCave, Area.IceCap, Character.Sonic, 20, [], [], [], [], []),
    MissionLocation(821, Area.Jungle, Area.FinalEgg, Character.Gamma, 21, [], [], [], [], []),
    MissionLocation(822, Area.Hotel, Area.EmeraldCoast, Character.Big, 22, [], [], [], [], []),
    MissionLocation(823, Area.TPLobby, Area.TwinklePark, Character.Sonic, 23, [], [], [], [], []),
    MissionLocation(824, Area.Casino, Area.Casinopolis, Character.Tails, 24, [], [], [], [], []),
    MissionLocation(825, Area.CityHall, Area.Casinopolis, Character.Knuckles, 25, [], [], [], [], []),
    MissionLocation(826, Area.CityHall, Area.Casinopolis, Character.Knuckles, 26, [], [], [], [], []),
    MissionLocation(827, Area.CityHall, Area.SpeedHighway, Character.Sonic, 27, [], [], [], [], []),
    MissionLocation(828, Area.SSMain, Area.SpeedHighway, Character.Sonic, 28, [], [], [], [], []),
    MissionLocation(829, Area.CityHall, Area.SSMain, Character.Big, 29, [LifeBelt], [], [], [], []),
    MissionLocation(830, Area.Jungle, Area.RedMountain, Character.Sonic, 30, [], [], [], [], []),
    MissionLocation(831, Area.Station, Area.Casinopolis, Character.Tails, 31, [], [], [], [], []),
    MissionLocation(832, Area.AngelIsland, Area.AngelIsland, Character.Knuckles, 32, [], [], [], [], []),
    MissionLocation(833, Area.ECPool, Area.ECOutside, Character.Sonic, 33, [], [], [], [], []),
    MissionLocation(834, Area.ECOutside, Area.ECOutside, Character.Sonic, 34, [LightShoes], [LightShoes], [], [], []),
    MissionLocation(835, Area.MRMain, Area.IceCave, Character.Big, 35, [], [], [], [], []),
    MissionLocation(836, Area.ECInside, Area.SkyDeck, Character.Sonic, 36, [], [], [], [], []),
    MissionLocation(837, Area.Jungle, Area.Jungle, Character.Tails, 37, [JetAnklet], [], [], [], []),
    MissionLocation(838, Area.Jungle, Area.LostWorld, Character.Knuckles, 38, [ShovelClaw], [ShovelClaw], [ShovelClaw],
                    [], []),
    MissionLocation(839, Area.Hotel, Area.EmeraldCoast, Character.Gamma, 39, [JetBooster], [JetBooster], [JetBooster],
                    [JetBooster], []),
    MissionLocation(840, Area.MRMain, Area.LostWorld, Character.Sonic, 40, [LightShoes], [LightShoes], [LightShoes],
                    [LightShoes], []),
    MissionLocation(841, Area.Jungle, Area.LostWorld, Character.Sonic, 41, [LightShoes], [], [], [], []),
    MissionLocation(842, Area.PrisonHall, Area.HotShelter, Character.Gamma, 42, [], [], [], [], []),
    MissionLocation(843, Area.PrisonHall, Area.HotShelter, Character.Amy, 43, [], [], [], [], []),
    MissionLocation(844, Area.ECOutside, Area.ECPool, Character.Big, 44, [], [], [], [], []),
    MissionLocation(845, Area.Jungle, Area.FinalEgg, Character.Sonic, 45, [], [], [], [], []),
    MissionLocation(846, Area.Jungle, Area.FinalEgg, Character.Sonic, 46, [], [], [], [], []),
    MissionLocation(847, Area.MRMain, Area.MRMain, Character.Tails, 47, [JetAnklet], [], [], [], []),
    MissionLocation(848, Area.CityHall, Area.Casinopolis, Character.Knuckles, 48, [], [], [], [], []),
    MissionLocation(849, Area.Sewers, Area.TwinklePark, Character.Sonic, 49, [], [], [], [], []),
    MissionLocation(850, Area.FinalEggTower, Area.FinalEgg, Character.Amy, 50, [], [], [], [], []),
    MissionLocation(851, Area.Jungle, Area.WindyValley, Character.Gamma, 51, [JetBooster], [JetBooster], [JetBooster],
                    [JetBooster], []),
    MissionLocation(852, Area.Jungle, Area.Jungle, Character.Big, 52, [], [], [], [], []),
    MissionLocation(853, Area.AngelIsland, Area.IceCap, Character.Sonic, 53, [], [], [], [], []),
    MissionLocation(854, Area.IceCave, Area.IceCap, Character.Tails, 54, [], [], [], [], []),
    MissionLocation(855, Area.TPTunnel, Area.SpeedHighway, Character.Sonic, 55, [], [], [], [], []),
    MissionLocation(856, Area.MRMain, Area.RedMountain, Character.Knuckles, 56, [ShovelClaw], [ShovelClaw],
                    [ShovelClaw], [ShovelClaw], []),
    MissionLocation(857, Area.AngelIsland, Area.RedMountain, Character.Sonic, 57, [], [], [], [], []),
    MissionLocation(858, Area.Jungle, Area.LostWorld, Character.Sonic, 58, [LightShoes], [], [], [], []),
    MissionLocation(859, Area.ECPool, Area.SkyDeck, Character.Knuckles, 59, [], [], [], [], []),
    MissionLocation(860, Area.MRMain, Area.IceCap, Character.Big, 60, [], [], [], [], []),
]

sub_level_location_table: List[SubLevelLocation] = [
    SubLevelLocation(15, Area.TwinkleCircuit, SubLevel.TwinkleCircuit, SubLevelMission.B,
                     [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                     [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                     [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                     [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA],
                     [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG, P_GAMMA]),
    SubLevelLocation(40, Area.TwinkleCircuit, SubLevel.TwinkleCircuit, SubLevelMission.Sonic, [P_SONIC], [P_SONIC],
                     [P_SONIC], [P_SONIC], [P_SONIC]),
    SubLevelLocation(41, Area.TwinkleCircuit, SubLevel.TwinkleCircuit, SubLevelMission.Tails, [P_TAILS], [P_TAILS],
                     [P_TAILS], [P_TAILS], [P_TAILS]),
    SubLevelLocation(42, Area.TwinkleCircuit, SubLevel.TwinkleCircuit, SubLevelMission.Knuckles, [P_KNUCKLES],
                     [P_KNUCKLES], [P_KNUCKLES], [P_KNUCKLES], [P_KNUCKLES]),
    SubLevelLocation(43, Area.TwinkleCircuit, SubLevel.TwinkleCircuit, SubLevelMission.Amy, [P_AMY], [P_AMY], [P_AMY],
                     [P_AMY], [P_AMY]),
    SubLevelLocation(44, Area.TwinkleCircuit, SubLevel.TwinkleCircuit, SubLevelMission.Big, [P_BIG], [P_BIG], [P_BIG],
                     [P_BIG], [P_BIG]),
    SubLevelLocation(45, Area.TwinkleCircuit, SubLevel.TwinkleCircuit, SubLevelMission.Gamma, [P_GAMMA], [P_GAMMA],
                     [P_GAMMA], [P_GAMMA], [P_GAMMA]),
    SubLevelLocation(25, Area.SandHill, SubLevel.SandHill, SubLevelMission.B, [P_TAILS], [P_TAILS], [P_TAILS, P_SONIC],
                     [P_TAILS, P_SONIC], [P_TAILS, P_SONIC]),
    SubLevelLocation(26, Area.SandHill, SubLevel.SandHill, SubLevelMission.A, [P_TAILS], [P_TAILS], [P_TAILS, P_SONIC],
                     [P_TAILS, P_SONIC], [P_TAILS, P_SONIC]),
    SubLevelLocation(27, Area.SkyChase1, SubLevel.SkyChaseAct1, SubLevelMission.B, [P_TAILS, P_SONIC],
                     [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC]),
    SubLevelLocation(28, Area.SkyChase1, SubLevel.SkyChaseAct1, SubLevelMission.A, [P_TAILS, P_SONIC],
                     [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC]),
    SubLevelLocation(35, Area.SkyChase2, SubLevel.SkyChaseAct2, SubLevelMission.B, [P_TAILS, P_SONIC],
                     [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC]),
    SubLevelLocation(36, Area.SkyChase2, SubLevel.SkyChaseAct2, SubLevelMission.A, [P_TAILS, P_SONIC],
                     [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC], [P_TAILS, P_SONIC]),
]

enemy_location_table: List[EnemyLocation] = [
    EnemyLocation(10001, Area.EmeraldCoast, Character.Sonic, 1, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(10002, Area.EmeraldCoast, Character.Sonic, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10003, Area.EmeraldCoast, Character.Sonic, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10004, Area.EmeraldCoast, Character.Sonic, 4, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(10005, Area.EmeraldCoast, Character.Sonic, 5, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10006, Area.EmeraldCoast, Character.Sonic, 6, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10007, Area.EmeraldCoast, Character.Sonic, 7, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10008, Area.EmeraldCoast, Character.Sonic, 8, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10009, Area.EmeraldCoast, Character.Sonic, 9, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10010, Area.EmeraldCoast, Character.Sonic, 10, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10011, Area.EmeraldCoast, Character.Sonic, 11, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10012, Area.EmeraldCoast, Character.Sonic, 12, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10013, Area.EmeraldCoast, Character.Sonic, 13, Enemy.Sweep, [], [], [], [], []),
    EnemyLocation(10014, Area.EmeraldCoast, Character.Sonic, 14, Enemy.Sweep, [], [], [], [], []),
    EnemyLocation(10015, Area.EmeraldCoast, Character.Sonic, 15, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10016, Area.EmeraldCoast, Character.Sonic, 16, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10017, Area.EmeraldCoast, Character.Sonic, 17, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(10018, Area.EmeraldCoast, Character.Sonic, 18, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51001, Area.EmeraldCoast, Character.Gamma, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51002, Area.EmeraldCoast, Character.Gamma, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51003, Area.EmeraldCoast, Character.Gamma, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51004, Area.EmeraldCoast, Character.Gamma, 4, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51005, Area.EmeraldCoast, Character.Gamma, 5, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51006, Area.EmeraldCoast, Character.Gamma, 6, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(51007, Area.EmeraldCoast, Character.Gamma, 7, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(51008, Area.EmeraldCoast, Character.Gamma, 8, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(51009, Area.EmeraldCoast, Character.Gamma, 9, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51010, Area.EmeraldCoast, Character.Gamma, 10, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51011, Area.EmeraldCoast, Character.Gamma, 11, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(51012, Area.EmeraldCoast, Character.Gamma, 12, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51013, Area.EmeraldCoast, Character.Gamma, 13, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51014, Area.EmeraldCoast, Character.Gamma, 14, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(51015, Area.EmeraldCoast, Character.Gamma, 15, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51016, Area.EmeraldCoast, Character.Gamma, 16, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51017, Area.EmeraldCoast, Character.Gamma, 17, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51018, Area.EmeraldCoast, Character.Gamma, 18, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51019, Area.EmeraldCoast, Character.Gamma, 19, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51020, Area.EmeraldCoast, Character.Gamma, 20, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51021, Area.EmeraldCoast, Character.Gamma, 21, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51022, Area.EmeraldCoast, Character.Gamma, 22, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51023, Area.EmeraldCoast, Character.Gamma, 23, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(51024, Area.EmeraldCoast, Character.Gamma, 24, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51025, Area.EmeraldCoast, Character.Gamma, 25, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51026, Area.EmeraldCoast, Character.Gamma, 26, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51027, Area.EmeraldCoast, Character.Gamma, 27, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51028, Area.EmeraldCoast, Character.Gamma, 28, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(51029, Area.EmeraldCoast, Character.Gamma, 29, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(62001, Area.EmeraldCoast, Character.Big, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(62002, Area.EmeraldCoast, Character.Big, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(62003, Area.EmeraldCoast, Character.Big, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(11001, Area.WindyValley, Character.Sonic, 1, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(11002, Area.WindyValley, Character.Sonic, 2, Enemy.BoaBoa, [], [], [], [], []),
    EnemyLocation(11003, Area.WindyValley, Character.Sonic, 3, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(11004, Area.WindyValley, Character.Sonic, 4, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(11005, Area.WindyValley, Character.Sonic, 5, Enemy.BoaBoa, [], [], [], [], []),
    EnemyLocation(11006, Area.WindyValley, Character.Sonic, 6, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(11007, Area.WindyValley, Character.Sonic, 7, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(11008, Area.WindyValley, Character.Sonic, 8, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(11009, Area.WindyValley, Character.Sonic, 9, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(11010, Area.WindyValley, Character.Sonic, 10, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(20001, Area.WindyValley, Character.Tails, 1, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(20002, Area.WindyValley, Character.Tails, 2, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(20003, Area.WindyValley, Character.Tails, 3, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(52001, Area.WindyValley, Character.Gamma, 1, Enemy.BoaBoa, [], [], [], [], []),
    EnemyLocation(52002, Area.WindyValley, Character.Gamma, 2, Enemy.Rhinotank, [], [], [], [], []),
    EnemyLocation(52003, Area.WindyValley, Character.Gamma, 3, Enemy.BoaBoa, [JetBooster], [], [], [], []),
    EnemyLocation(52004, Area.WindyValley, Character.Gamma, 4, Enemy.BoaBoa, [JetBooster], [], [], [], []),
    EnemyLocation(52005, Area.WindyValley, Character.Gamma, 5, Enemy.Leon, [JetBooster], [], [], [], []),
    EnemyLocation(52006, Area.WindyValley, Character.Gamma, 6, Enemy.Leon, [JetBooster], [], [], [], []),
    EnemyLocation(52007, Area.WindyValley, Character.Gamma, 7, Enemy.BoaBoa, [JetBooster], [], [], [], []),
    EnemyLocation(52008, Area.WindyValley, Character.Gamma, 8, Enemy.BoaBoa, [JetBooster], [], [], [], []),
    EnemyLocation(52009, Area.WindyValley, Character.Gamma, 9, Enemy.BoaBoa, [JetBooster], [], [], [], []),
    EnemyLocation(52010, Area.WindyValley, Character.Gamma, 10, Enemy.BoaBoa, [JetBooster], [], [], [], []),
    EnemyLocation(52011, Area.WindyValley, Character.Gamma, 11, Enemy.Rhinotank, [JetBooster], [], [], [], []),
    EnemyLocation(14001, Area.TwinklePark, Character.Sonic, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14002, Area.TwinklePark, Character.Sonic, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14003, Area.TwinklePark, Character.Sonic, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14004, Area.TwinklePark, Character.Sonic, 4, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14005, Area.TwinklePark, Character.Sonic, 5, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14006, Area.TwinklePark, Character.Sonic, 6, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14007, Area.TwinklePark, Character.Sonic, 7, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14008, Area.TwinklePark, Character.Sonic, 8, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14009, Area.TwinklePark, Character.Sonic, 9, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(14010, Area.TwinklePark, Character.Sonic, 10, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(14011, Area.TwinklePark, Character.Sonic, 11, Enemy.Sweep, [], [], [], [], []),
    EnemyLocation(14012, Area.TwinklePark, Character.Sonic, 12, Enemy.Sweep, [], [], [], [], []),
    EnemyLocation(14013, Area.TwinklePark, Character.Sonic, 13, Enemy.Sweep, [], [], [], [], []),
    EnemyLocation(14014, Area.TwinklePark, Character.Sonic, 14, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14015, Area.TwinklePark, Character.Sonic, 15, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14016, Area.TwinklePark, Character.Sonic, 16, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14017, Area.TwinklePark, Character.Sonic, 17, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14018, Area.TwinklePark, Character.Sonic, 18, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(14019, Area.TwinklePark, Character.Sonic, 19, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(14020, Area.TwinklePark, Character.Sonic, 20, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14021, Area.TwinklePark, Character.Sonic, 21, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14022, Area.TwinklePark, Character.Sonic, 22, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14023, Area.TwinklePark, Character.Sonic, 23, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14024, Area.TwinklePark, Character.Sonic, 24, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14025, Area.TwinklePark, Character.Sonic, 25, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14026, Area.TwinklePark, Character.Sonic, 26, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14027, Area.TwinklePark, Character.Sonic, 27, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14028, Area.TwinklePark, Character.Sonic, 28, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14029, Area.TwinklePark, Character.Sonic, 29, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14030, Area.TwinklePark, Character.Sonic, 30, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14031, Area.TwinklePark, Character.Sonic, 31, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14032, Area.TwinklePark, Character.Sonic, 32, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14033, Area.TwinklePark, Character.Sonic, 33, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(14034, Area.TwinklePark, Character.Sonic, 34, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40001, Area.TwinklePark, Character.Amy, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40002, Area.TwinklePark, Character.Amy, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40003, Area.TwinklePark, Character.Amy, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40004, Area.TwinklePark, Character.Amy, 4, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40005, Area.TwinklePark, Character.Amy, 5, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40006, Area.TwinklePark, Character.Amy, 6, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40007, Area.TwinklePark, Character.Amy, 7, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(40008, Area.TwinklePark, Character.Amy, 8, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40009, Area.TwinklePark, Character.Amy, 9, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(40010, Area.TwinklePark, Character.Amy, 10, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(40011, Area.TwinklePark, Character.Amy, 11, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40012, Area.TwinklePark, Character.Amy, 12, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40013, Area.TwinklePark, Character.Amy, 13, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40014, Area.TwinklePark, Character.Amy, 14, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40015, Area.TwinklePark, Character.Amy, 15, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(40016, Area.TwinklePark, Character.Amy, 16, Enemy.Buyon, [], [], [], [], []),
    EnemyLocation(60001, Area.TwinklePark, Character.Big, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(60002, Area.TwinklePark, Character.Big, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(60003, Area.TwinklePark, Character.Big, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(60004, Area.TwinklePark, Character.Big, 4, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(15001, Area.SpeedHighway, Character.Sonic, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15002, Area.SpeedHighway, Character.Sonic, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15003, Area.SpeedHighway, Character.Sonic, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15004, Area.SpeedHighway, Character.Sonic, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15005, Area.SpeedHighway, Character.Sonic, 5, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15006, Area.SpeedHighway, Character.Sonic, 6, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15007, Area.SpeedHighway, Character.Sonic, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15008, Area.SpeedHighway, Character.Sonic, 8, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15009, Area.SpeedHighway, Character.Sonic, 9, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15010, Area.SpeedHighway, Character.Sonic, 10, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(15011, Area.SpeedHighway, Character.Sonic, 11, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15012, Area.SpeedHighway, Character.Sonic, 12, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(15013, Area.SpeedHighway, Character.Sonic, 13, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(15014, Area.SpeedHighway, Character.Sonic, 14, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15015, Area.SpeedHighway, Character.Sonic, 15, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15016, Area.SpeedHighway, Character.Sonic, 16, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15017, Area.SpeedHighway, Character.Sonic, 17, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15018, Area.SpeedHighway, Character.Sonic, 18, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15019, Area.SpeedHighway, Character.Sonic, 19, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15020, Area.SpeedHighway, Character.Sonic, 20, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15021, Area.SpeedHighway, Character.Sonic, 21, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15022, Area.SpeedHighway, Character.Sonic, 22, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15023, Area.SpeedHighway, Character.Sonic, 23, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15024, Area.SpeedHighway, Character.Sonic, 24, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15025, Area.SpeedHighway, Character.Sonic, 25, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15026, Area.SpeedHighway, Character.Sonic, 26, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15027, Area.SpeedHighway, Character.Sonic, 27, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15028, Area.SpeedHighway, Character.Sonic, 28, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15029, Area.SpeedHighway, Character.Sonic, 29, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15030, Area.SpeedHighway, Character.Sonic, 30, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15031, Area.SpeedHighway, Character.Sonic, 31, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15032, Area.SpeedHighway, Character.Sonic, 32, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15033, Area.SpeedHighway, Character.Sonic, 33, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15034, Area.SpeedHighway, Character.Sonic, 34, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15035, Area.SpeedHighway, Character.Sonic, 35, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15036, Area.SpeedHighway, Character.Sonic, 36, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15037, Area.SpeedHighway, Character.Sonic, 37, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(15038, Area.SpeedHighway, Character.Sonic, 38, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(15039, Area.SpeedHighway, Character.Sonic, 39, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15040, Area.SpeedHighway, Character.Sonic, 40, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(15041, Area.SpeedHighway, Character.Sonic, 41, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15042, Area.SpeedHighway, Character.Sonic, 42, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15043, Area.SpeedHighway, Character.Sonic, 43, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15044, Area.SpeedHighway, Character.Sonic, 44, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15045, Area.SpeedHighway, Character.Sonic, 45, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15046, Area.SpeedHighway, Character.Sonic, 46, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15047, Area.SpeedHighway, Character.Sonic, 47, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(15048, Area.SpeedHighway, Character.Sonic, 48, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24001, Area.SpeedHighway, Character.Tails, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(24002, Area.SpeedHighway, Character.Tails, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(24003, Area.SpeedHighway, Character.Tails, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(24004, Area.SpeedHighway, Character.Tails, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(24005, Area.SpeedHighway, Character.Tails, 5, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24006, Area.SpeedHighway, Character.Tails, 6, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24007, Area.SpeedHighway, Character.Tails, 7, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24008, Area.SpeedHighway, Character.Tails, 8, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24009, Area.SpeedHighway, Character.Tails, 9, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24010, Area.SpeedHighway, Character.Tails, 10, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24011, Area.SpeedHighway, Character.Tails, 11, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24012, Area.SpeedHighway, Character.Tails, 12, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24013, Area.SpeedHighway, Character.Tails, 13, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24014, Area.SpeedHighway, Character.Tails, 14, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24015, Area.SpeedHighway, Character.Tails, 15, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(24016, Area.SpeedHighway, Character.Tails, 16, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(24017, Area.SpeedHighway, Character.Tails, 17, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24018, Area.SpeedHighway, Character.Tails, 18, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24019, Area.SpeedHighway, Character.Tails, 19, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24020, Area.SpeedHighway, Character.Tails, 20, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24021, Area.SpeedHighway, Character.Tails, 21, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24022, Area.SpeedHighway, Character.Tails, 22, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24023, Area.SpeedHighway, Character.Tails, 23, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24024, Area.SpeedHighway, Character.Tails, 24, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24025, Area.SpeedHighway, Character.Tails, 25, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24026, Area.SpeedHighway, Character.Tails, 26, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24027, Area.SpeedHighway, Character.Tails, 27, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24028, Area.SpeedHighway, Character.Tails, 28, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(24029, Area.SpeedHighway, Character.Tails, 29, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24030, Area.SpeedHighway, Character.Tails, 30, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(24031, Area.SpeedHighway, Character.Tails, 31, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30001, Area.SpeedHighway, Character.Knuckles, 1, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30002, Area.SpeedHighway, Character.Knuckles, 2, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30003, Area.SpeedHighway, Character.Knuckles, 3, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30004, Area.SpeedHighway, Character.Knuckles, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(30005, Area.SpeedHighway, Character.Knuckles, 5, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(30006, Area.SpeedHighway, Character.Knuckles, 6, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30007, Area.SpeedHighway, Character.Knuckles, 7, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30008, Area.SpeedHighway, Character.Knuckles, 8, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(30009, Area.SpeedHighway, Character.Knuckles, 9, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30010, Area.SpeedHighway, Character.Knuckles, 10, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(30011, Area.SpeedHighway, Character.Knuckles, 11, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(30012, Area.SpeedHighway, Character.Knuckles, 12, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(30013, Area.SpeedHighway, Character.Knuckles, 13, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30014, Area.SpeedHighway, Character.Knuckles, 14, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(30015, Area.SpeedHighway, Character.Knuckles, 15, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(30016, Area.SpeedHighway, Character.Knuckles, 16, Enemy.CopSpeeder, [], [], [], [], []),
    EnemyLocation(16001, Area.RedMountain, Character.Sonic, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16002, Area.RedMountain, Character.Sonic, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16003, Area.RedMountain, Character.Sonic, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16004, Area.RedMountain, Character.Sonic, 4, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16005, Area.RedMountain, Character.Sonic, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16006, Area.RedMountain, Character.Sonic, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16007, Area.RedMountain, Character.Sonic, 7, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16008, Area.RedMountain, Character.Sonic, 8, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16009, Area.RedMountain, Character.Sonic, 9, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16010, Area.RedMountain, Character.Sonic, 10, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16011, Area.RedMountain, Character.Sonic, 11, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16012, Area.RedMountain, Character.Sonic, 12, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16013, Area.RedMountain, Character.Sonic, 13, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16014, Area.RedMountain, Character.Sonic, 14, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16015, Area.RedMountain, Character.Sonic, 15, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16016, Area.RedMountain, Character.Sonic, 16, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16017, Area.RedMountain, Character.Sonic, 17, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16018, Area.RedMountain, Character.Sonic, 18, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16019, Area.RedMountain, Character.Sonic, 19, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16020, Area.RedMountain, Character.Sonic, 20, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16021, Area.RedMountain, Character.Sonic, 21, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16022, Area.RedMountain, Character.Sonic, 22, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16023, Area.RedMountain, Character.Sonic, 23, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16024, Area.RedMountain, Character.Sonic, 24, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16025, Area.RedMountain, Character.Sonic, 25, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16026, Area.RedMountain, Character.Sonic, 26, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16027, Area.RedMountain, Character.Sonic, 27, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16028, Area.RedMountain, Character.Sonic, 28, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16029, Area.RedMountain, Character.Sonic, 29, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16030, Area.RedMountain, Character.Sonic, 30, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16031, Area.RedMountain, Character.Sonic, 31, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16032, Area.RedMountain, Character.Sonic, 32, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16033, Area.RedMountain, Character.Sonic, 33, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16034, Area.RedMountain, Character.Sonic, 34, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16035, Area.RedMountain, Character.Sonic, 35, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16036, Area.RedMountain, Character.Sonic, 36, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16037, Area.RedMountain, Character.Sonic, 37, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16038, Area.RedMountain, Character.Sonic, 38, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16039, Area.RedMountain, Character.Sonic, 39, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16040, Area.RedMountain, Character.Sonic, 40, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16041, Area.RedMountain, Character.Sonic, 41, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(16042, Area.RedMountain, Character.Sonic, 42, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16043, Area.RedMountain, Character.Sonic, 43, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16044, Area.RedMountain, Character.Sonic, 44, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16045, Area.RedMountain, Character.Sonic, 45, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16046, Area.RedMountain, Character.Sonic, 46, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16047, Area.RedMountain, Character.Sonic, 47, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16048, Area.RedMountain, Character.Sonic, 48, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16049, Area.RedMountain, Character.Sonic, 49, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16050, Area.RedMountain, Character.Sonic, 50, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16051, Area.RedMountain, Character.Sonic, 51, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16052, Area.RedMountain, Character.Sonic, 52, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16053, Area.RedMountain, Character.Sonic, 53, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16054, Area.RedMountain, Character.Sonic, 54, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16055, Area.RedMountain, Character.Sonic, 55, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16056, Area.RedMountain, Character.Sonic, 56, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16057, Area.RedMountain, Character.Sonic, 57, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16058, Area.RedMountain, Character.Sonic, 58, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(16059, Area.RedMountain, Character.Sonic, 59, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16060, Area.RedMountain, Character.Sonic, 60, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(16061, Area.RedMountain, Character.Sonic, 61, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32001, Area.RedMountain, Character.Knuckles, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32002, Area.RedMountain, Character.Knuckles, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32003, Area.RedMountain, Character.Knuckles, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32004, Area.RedMountain, Character.Knuckles, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32005, Area.RedMountain, Character.Knuckles, 5, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(32006, Area.RedMountain, Character.Knuckles, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32007, Area.RedMountain, Character.Knuckles, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32008, Area.RedMountain, Character.Knuckles, 8, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32009, Area.RedMountain, Character.Knuckles, 9, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(32010, Area.RedMountain, Character.Knuckles, 10, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32011, Area.RedMountain, Character.Knuckles, 11, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(32012, Area.RedMountain, Character.Knuckles, 12, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32013, Area.RedMountain, Character.Knuckles, 13, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32014, Area.RedMountain, Character.Knuckles, 14, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(32015, Area.RedMountain, Character.Knuckles, 15, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32016, Area.RedMountain, Character.Knuckles, 16, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32017, Area.RedMountain, Character.Knuckles, 17, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32018, Area.RedMountain, Character.Knuckles, 18, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(32019, Area.RedMountain, Character.Knuckles, 19, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32020, Area.RedMountain, Character.Knuckles, 20, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(32021, Area.RedMountain, Character.Knuckles, 21, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(32022, Area.RedMountain, Character.Knuckles, 22, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53001, Area.RedMountain, Character.Gamma, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53002, Area.RedMountain, Character.Gamma, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53003, Area.RedMountain, Character.Gamma, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53004, Area.RedMountain, Character.Gamma, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53005, Area.RedMountain, Character.Gamma, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53006, Area.RedMountain, Character.Gamma, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53007, Area.RedMountain, Character.Gamma, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53008, Area.RedMountain, Character.Gamma, 8, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53009, Area.RedMountain, Character.Gamma, 9, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53010, Area.RedMountain, Character.Gamma, 10, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53011, Area.RedMountain, Character.Gamma, 11, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53012, Area.RedMountain, Character.Gamma, 12, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53013, Area.RedMountain, Character.Gamma, 13, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53014, Area.RedMountain, Character.Gamma, 14, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53015, Area.RedMountain, Character.Gamma, 15, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53016, Area.RedMountain, Character.Gamma, 16, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53017, Area.RedMountain, Character.Gamma, 17, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53018, Area.RedMountain, Character.Gamma, 18, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53019, Area.RedMountain, Character.Gamma, 19, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53020, Area.RedMountain, Character.Gamma, 20, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53021, Area.RedMountain, Character.Gamma, 21, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53022, Area.RedMountain, Character.Gamma, 22, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53023, Area.RedMountain, Character.Gamma, 23, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53024, Area.RedMountain, Character.Gamma, 24, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53025, Area.RedMountain, Character.Gamma, 25, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53026, Area.RedMountain, Character.Gamma, 26, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53027, Area.RedMountain, Character.Gamma, 27, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53028, Area.RedMountain, Character.Gamma, 28, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53029, Area.RedMountain, Character.Gamma, 29, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53030, Area.RedMountain, Character.Gamma, 30, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53031, Area.RedMountain, Character.Gamma, 31, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53032, Area.RedMountain, Character.Gamma, 32, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53033, Area.RedMountain, Character.Gamma, 33, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53034, Area.RedMountain, Character.Gamma, 34, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53035, Area.RedMountain, Character.Gamma, 35, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53036, Area.RedMountain, Character.Gamma, 36, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53037, Area.RedMountain, Character.Gamma, 37, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53038, Area.RedMountain, Character.Gamma, 38, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53039, Area.RedMountain, Character.Gamma, 39, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53040, Area.RedMountain, Character.Gamma, 40, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53041, Area.RedMountain, Character.Gamma, 41, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53042, Area.RedMountain, Character.Gamma, 42, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53043, Area.RedMountain, Character.Gamma, 43, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53044, Area.RedMountain, Character.Gamma, 44, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53045, Area.RedMountain, Character.Gamma, 45, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53046, Area.RedMountain, Character.Gamma, 46, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(53047, Area.RedMountain, Character.Gamma, 47, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53048, Area.RedMountain, Character.Gamma, 48, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53049, Area.RedMountain, Character.Gamma, 49, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53050, Area.RedMountain, Character.Gamma, 50, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(53051, Area.RedMountain, Character.Gamma, 51, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17001, Area.SkyDeck, Character.Sonic, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17002, Area.SkyDeck, Character.Sonic, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17003, Area.SkyDeck, Character.Sonic, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17004, Area.SkyDeck, Character.Sonic, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17005, Area.SkyDeck, Character.Sonic, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17006, Area.SkyDeck, Character.Sonic, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17007, Area.SkyDeck, Character.Sonic, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17008, Area.SkyDeck, Character.Sonic, 8, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17009, Area.SkyDeck, Character.Sonic, 9, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17010, Area.SkyDeck, Character.Sonic, 10, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17011, Area.SkyDeck, Character.Sonic, 11, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17012, Area.SkyDeck, Character.Sonic, 12, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17013, Area.SkyDeck, Character.Sonic, 13, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17014, Area.SkyDeck, Character.Sonic, 14, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17015, Area.SkyDeck, Character.Sonic, 15, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17016, Area.SkyDeck, Character.Sonic, 16, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17017, Area.SkyDeck, Character.Sonic, 17, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17018, Area.SkyDeck, Character.Sonic, 18, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17019, Area.SkyDeck, Character.Sonic, 19, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17020, Area.SkyDeck, Character.Sonic, 20, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17021, Area.SkyDeck, Character.Sonic, 21, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17022, Area.SkyDeck, Character.Sonic, 22, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17023, Area.SkyDeck, Character.Sonic, 23, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17024, Area.SkyDeck, Character.Sonic, 24, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17025, Area.SkyDeck, Character.Sonic, 25, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17026, Area.SkyDeck, Character.Sonic, 26, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17027, Area.SkyDeck, Character.Sonic, 27, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17028, Area.SkyDeck, Character.Sonic, 28, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17029, Area.SkyDeck, Character.Sonic, 29, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17030, Area.SkyDeck, Character.Sonic, 30, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17031, Area.SkyDeck, Character.Sonic, 31, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(17032, Area.SkyDeck, Character.Sonic, 32, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17033, Area.SkyDeck, Character.Sonic, 33, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17034, Area.SkyDeck, Character.Sonic, 34, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17035, Area.SkyDeck, Character.Sonic, 35, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17036, Area.SkyDeck, Character.Sonic, 36, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17037, Area.SkyDeck, Character.Sonic, 37, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17038, Area.SkyDeck, Character.Sonic, 38, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17039, Area.SkyDeck, Character.Sonic, 39, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17040, Area.SkyDeck, Character.Sonic, 40, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17041, Area.SkyDeck, Character.Sonic, 41, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17042, Area.SkyDeck, Character.Sonic, 42, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17043, Area.SkyDeck, Character.Sonic, 43, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17044, Area.SkyDeck, Character.Sonic, 44, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17045, Area.SkyDeck, Character.Sonic, 45, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17046, Area.SkyDeck, Character.Sonic, 46, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17047, Area.SkyDeck, Character.Sonic, 47, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17048, Area.SkyDeck, Character.Sonic, 48, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17049, Area.SkyDeck, Character.Sonic, 49, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17050, Area.SkyDeck, Character.Sonic, 50, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17051, Area.SkyDeck, Character.Sonic, 51, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17052, Area.SkyDeck, Character.Sonic, 52, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17053, Area.SkyDeck, Character.Sonic, 53, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17054, Area.SkyDeck, Character.Sonic, 54, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(17055, Area.SkyDeck, Character.Sonic, 55, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17056, Area.SkyDeck, Character.Sonic, 56, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17057, Area.SkyDeck, Character.Sonic, 57, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(17058, Area.SkyDeck, Character.Sonic, 58, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(23001, Area.SkyDeck, Character.Tails, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23002, Area.SkyDeck, Character.Tails, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23003, Area.SkyDeck, Character.Tails, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23004, Area.SkyDeck, Character.Tails, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23005, Area.SkyDeck, Character.Tails, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23006, Area.SkyDeck, Character.Tails, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23007, Area.SkyDeck, Character.Tails, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23008, Area.SkyDeck, Character.Tails, 8, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(23009, Area.SkyDeck, Character.Tails, 9, Enemy.SpikySpinner, [], [], [], [], []),
    EnemyLocation(34001, Area.SkyDeck, Character.Knuckles, 1, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34002, Area.SkyDeck, Character.Knuckles, 2, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34003, Area.SkyDeck, Character.Knuckles, 3, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34004, Area.SkyDeck, Character.Knuckles, 4, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34005, Area.SkyDeck, Character.Knuckles, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(34006, Area.SkyDeck, Character.Knuckles, 6, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34007, Area.SkyDeck, Character.Knuckles, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(34008, Area.SkyDeck, Character.Knuckles, 8, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(34009, Area.SkyDeck, Character.Knuckles, 9, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(34010, Area.SkyDeck, Character.Knuckles, 10, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34011, Area.SkyDeck, Character.Knuckles, 11, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34012, Area.SkyDeck, Character.Knuckles, 12, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34013, Area.SkyDeck, Character.Knuckles, 13, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34014, Area.SkyDeck, Character.Knuckles, 14, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34015, Area.SkyDeck, Character.Knuckles, 15, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(34016, Area.SkyDeck, Character.Knuckles, 16, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(18001, Area.LostWorld, Character.Sonic, 1, Enemy.BoaBoa, [], [], [], [], []),
    EnemyLocation(18002, Area.LostWorld, Character.Sonic, 2, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18003, Area.LostWorld, Character.Sonic, 3, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18004, Area.LostWorld, Character.Sonic, 4, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18005, Area.LostWorld, Character.Sonic, 5, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18006, Area.LostWorld, Character.Sonic, 6, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18007, Area.LostWorld, Character.Sonic, 7, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18008, Area.LostWorld, Character.Sonic, 8, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18009, Area.LostWorld, Character.Sonic, 9, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18010, Area.LostWorld, Character.Sonic, 10, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(18011, Area.LostWorld, Character.Sonic, 11, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18012, Area.LostWorld, Character.Sonic, 12, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(18013, Area.LostWorld, Character.Sonic, 13, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(18014, Area.LostWorld, Character.Sonic, 14, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(18015, Area.LostWorld, Character.Sonic, 15, Enemy.Leon, [LightShoes], [], [], [], []),
    EnemyLocation(18016, Area.LostWorld, Character.Sonic, 16, Enemy.Leon, [LightShoes], [], [], [], []),
    EnemyLocation(18017, Area.LostWorld, Character.Sonic, 17, Enemy.Gola, [LightShoes], [], [], [], []),
    EnemyLocation(18018, Area.LostWorld, Character.Sonic, 18, Enemy.Gola, [LightShoes], [], [], [], []),
    EnemyLocation(18019, Area.LostWorld, Character.Sonic, 19, Enemy.Leon, [LightShoes], [], [], [], []),
    EnemyLocation(18020, Area.LostWorld, Character.Sonic, 20, Enemy.Gola, [LightShoes], [], [], [], []),
    EnemyLocation(18021, Area.LostWorld, Character.Sonic, 21, Enemy.BoaBoa, [LightShoes], [], [], [], []),
    EnemyLocation(18022, Area.LostWorld, Character.Sonic, 22, Enemy.Leon, [LightShoes], [], [], [], []),
    EnemyLocation(18023, Area.LostWorld, Character.Sonic, 23, Enemy.Leon, [LightShoes], [], [], [], []),
    EnemyLocation(33001, Area.LostWorld, Character.Knuckles, 1, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(33002, Area.LostWorld, Character.Knuckles, 2, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(33003, Area.LostWorld, Character.Knuckles, 3, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(33004, Area.LostWorld, Character.Knuckles, 4, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(33005, Area.LostWorld, Character.Knuckles, 5, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(33006, Area.LostWorld, Character.Knuckles, 6, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(33007, Area.LostWorld, Character.Knuckles, 7, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(33008, Area.LostWorld, Character.Knuckles, 8, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(33009, Area.LostWorld, Character.Knuckles, 9, Enemy.Gola, [], [], [], [], []),
    EnemyLocation(33010, Area.LostWorld, Character.Knuckles, 10, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(13001, Area.IceCap, Character.Sonic, 1, Enemy.IceBall, [], [], [], [], []),
    EnemyLocation(13002, Area.IceCap, Character.Sonic, 2, Enemy.IceBall, [], [], [], [], []),
    EnemyLocation(13003, Area.IceCap, Character.Sonic, 3, Enemy.IceBall, [], [], [], [], []),
    EnemyLocation(13004, Area.IceCap, Character.Sonic, 4, Enemy.BoaBoa, [], [], [], [], []),
    EnemyLocation(13005, Area.IceCap, Character.Sonic, 5, Enemy.IceBall, [], [], [], [], []),
    EnemyLocation(12001, Area.Casinopolis, Character.Sonic, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12002, Area.Casinopolis, Character.Sonic, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12003, Area.Casinopolis, Character.Sonic, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12004, Area.Casinopolis, Character.Sonic, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12005, Area.Casinopolis, Character.Sonic, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12006, Area.Casinopolis, Character.Sonic, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12007, Area.Casinopolis, Character.Sonic, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12008, Area.Casinopolis, Character.Sonic, 8, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12009, Area.Casinopolis, Character.Sonic, 9, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(12010, Area.Casinopolis, Character.Sonic, 10, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(21001, Area.Casinopolis, Character.Tails, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(21002, Area.Casinopolis, Character.Tails, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(21003, Area.Casinopolis, Character.Tails, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31001, Area.Casinopolis, Character.Knuckles, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31002, Area.Casinopolis, Character.Knuckles, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31003, Area.Casinopolis, Character.Knuckles, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31004, Area.Casinopolis, Character.Knuckles, 4, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(31005, Area.Casinopolis, Character.Knuckles, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31006, Area.Casinopolis, Character.Knuckles, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31007, Area.Casinopolis, Character.Knuckles, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31008, Area.Casinopolis, Character.Knuckles, 8, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31009, Area.Casinopolis, Character.Knuckles, 9, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31010, Area.Casinopolis, Character.Knuckles, 10, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31011, Area.Casinopolis, Character.Knuckles, 11, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31012, Area.Casinopolis, Character.Knuckles, 12, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31013, Area.Casinopolis, Character.Knuckles, 13, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31014, Area.Casinopolis, Character.Knuckles, 14, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31015, Area.Casinopolis, Character.Knuckles, 15, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(31016, Area.Casinopolis, Character.Knuckles, 16, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(19001, Area.FinalEgg, Character.Sonic, 1, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19002, Area.FinalEgg, Character.Sonic, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19003, Area.FinalEgg, Character.Sonic, 3, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19004, Area.FinalEgg, Character.Sonic, 4, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19005, Area.FinalEgg, Character.Sonic, 5, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19006, Area.FinalEgg, Character.Sonic, 6, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19007, Area.FinalEgg, Character.Sonic, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19008, Area.FinalEgg, Character.Sonic, 8, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19009, Area.FinalEgg, Character.Sonic, 9, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(19010, Area.FinalEgg, Character.Sonic, 10, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(19011, Area.FinalEgg, Character.Sonic, 11, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19012, Area.FinalEgg, Character.Sonic, 12, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19013, Area.FinalEgg, Character.Sonic, 13, Enemy.ElectroSpinner, [], [], [], [], []),
    EnemyLocation(19014, Area.FinalEgg, Character.Sonic, 14, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19015, Area.FinalEgg, Character.Sonic, 15, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19016, Area.FinalEgg, Character.Sonic, 16, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19017, Area.FinalEgg, Character.Sonic, 17, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19018, Area.FinalEgg, Character.Sonic, 18, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19019, Area.FinalEgg, Character.Sonic, 19, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19020, Area.FinalEgg, Character.Sonic, 20, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19021, Area.FinalEgg, Character.Sonic, 21, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19022, Area.FinalEgg, Character.Sonic, 22, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19023, Area.FinalEgg, Character.Sonic, 23, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19024, Area.FinalEgg, Character.Sonic, 24, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19025, Area.FinalEgg, Character.Sonic, 25, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19026, Area.FinalEgg, Character.Sonic, 26, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19027, Area.FinalEgg, Character.Sonic, 27, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19028, Area.FinalEgg, Character.Sonic, 28, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19029, Area.FinalEgg, Character.Sonic, 29, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19030, Area.FinalEgg, Character.Sonic, 30, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19031, Area.FinalEgg, Character.Sonic, 31, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19032, Area.FinalEgg, Character.Sonic, 32, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19033, Area.FinalEgg, Character.Sonic, 33, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19034, Area.FinalEgg, Character.Sonic, 34, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19035, Area.FinalEgg, Character.Sonic, 35, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19036, Area.FinalEgg, Character.Sonic, 36, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19037, Area.FinalEgg, Character.Sonic, 37, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19038, Area.FinalEgg, Character.Sonic, 38, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(19039, Area.FinalEgg, Character.Sonic, 39, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(19040, Area.FinalEgg, Character.Sonic, 40, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(42001, Area.FinalEgg, Character.Amy, 1, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(42002, Area.FinalEgg, Character.Amy, 2, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(42003, Area.FinalEgg, Character.Amy, 3, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(42004, Area.FinalEgg, Character.Amy, 4, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(42005, Area.FinalEgg, Character.Amy, 5, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(42006, Area.FinalEgg, Character.Amy, 6, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(42007, Area.FinalEgg, Character.Amy, 7, Enemy.Spinner, [], [], [], [], []),
    EnemyLocation(50001, Area.FinalEgg, Character.Gamma, 1, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(50002, Area.FinalEgg, Character.Gamma, 2, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(41001, Area.HotShelter, Character.Amy, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41002, Area.HotShelter, Character.Amy, 2, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(41003, Area.HotShelter, Character.Amy, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41004, Area.HotShelter, Character.Amy, 4, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41005, Area.HotShelter, Character.Amy, 5, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41006, Area.HotShelter, Character.Amy, 6, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41007, Area.HotShelter, Character.Amy, 7, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41008, Area.HotShelter, Character.Amy, 8, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41009, Area.HotShelter, Character.Amy, 9, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41010, Area.HotShelter, Character.Amy, 10, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41011, Area.HotShelter, Character.Amy, 11, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(41012, Area.HotShelter, Character.Amy, 12, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41013, Area.HotShelter, Character.Amy, 13, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41014, Area.HotShelter, Character.Amy, 14, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41015, Area.HotShelter, Character.Amy, 15, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41016, Area.HotShelter, Character.Amy, 16, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41017, Area.HotShelter, Character.Amy, 17, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41018, Area.HotShelter, Character.Amy, 18, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(41019, Area.HotShelter, Character.Amy, 19, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(41020, Area.HotShelter, Character.Amy, 20, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41021, Area.HotShelter, Character.Amy, 21, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41022, Area.HotShelter, Character.Amy, 22, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(41023, Area.HotShelter, Character.Amy, 23, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41024, Area.HotShelter, Character.Amy, 24, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41025, Area.HotShelter, Character.Amy, 25, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41026, Area.HotShelter, Character.Amy, 26, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41027, Area.HotShelter, Character.Amy, 27, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41028, Area.HotShelter, Character.Amy, 28, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41029, Area.HotShelter, Character.Amy, 29, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41030, Area.HotShelter, Character.Amy, 30, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(41031, Area.HotShelter, Character.Amy, 31, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54001, Area.HotShelter, Character.Gamma, 1, Enemy.EggKeeper, [], [], [], [], []),
    EnemyLocation(54002, Area.HotShelter, Character.Gamma, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54003, Area.HotShelter, Character.Gamma, 3, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54004, Area.HotShelter, Character.Gamma, 4, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54005, Area.HotShelter, Character.Gamma, 5, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54006, Area.HotShelter, Character.Gamma, 6, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54007, Area.HotShelter, Character.Gamma, 7, Enemy.Leon, [], [], [], [], []),
    EnemyLocation(54008, Area.HotShelter, Character.Gamma, 8, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54009, Area.HotShelter, Character.Gamma, 9, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54010, Area.HotShelter, Character.Gamma, 10, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54011, Area.HotShelter, Character.Gamma, 11, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54012, Area.HotShelter, Character.Gamma, 12, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54013, Area.HotShelter, Character.Gamma, 13, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54014, Area.HotShelter, Character.Gamma, 14, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54015, Area.HotShelter, Character.Gamma, 15, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54016, Area.HotShelter, Character.Gamma, 16, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54017, Area.HotShelter, Character.Gamma, 17, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54018, Area.HotShelter, Character.Gamma, 18, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54019, Area.HotShelter, Character.Gamma, 19, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(54020, Area.HotShelter, Character.Gamma, 20, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54021, Area.HotShelter, Character.Gamma, 21, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54022, Area.HotShelter, Character.Gamma, 22, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54023, Area.HotShelter, Character.Gamma, 23, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54024, Area.HotShelter, Character.Gamma, 24, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54025, Area.HotShelter, Character.Gamma, 25, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54026, Area.HotShelter, Character.Gamma, 26, Enemy.Leon, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54027, Area.HotShelter, Character.Gamma, 27, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54028, Area.HotShelter, Character.Gamma, 28, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54029, Area.HotShelter, Character.Gamma, 29, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54030, Area.HotShelter, Character.Gamma, 30, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54031, Area.HotShelter, Character.Gamma, 31, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54032, Area.HotShelter, Character.Gamma, 32, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54033, Area.HotShelter, Character.Gamma, 33, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54034, Area.HotShelter, Character.Gamma, 34, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54035, Area.HotShelter, Character.Gamma, 35, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54036, Area.HotShelter, Character.Gamma, 36, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54037, Area.HotShelter, Character.Gamma, 37, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54038, Area.HotShelter, Character.Gamma, 38, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54039, Area.HotShelter, Character.Gamma, 39, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54040, Area.HotShelter, Character.Gamma, 40, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54041, Area.HotShelter, Character.Gamma, 41, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54042, Area.HotShelter, Character.Gamma, 42, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54043, Area.HotShelter, Character.Gamma, 43, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54044, Area.HotShelter, Character.Gamma, 44, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54045, Area.HotShelter, Character.Gamma, 45, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54046, Area.HotShelter, Character.Gamma, 46, Enemy.Leon, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54047, Area.HotShelter, Character.Gamma, 47, Enemy.Leon, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54048, Area.HotShelter, Character.Gamma, 48, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54049, Area.HotShelter, Character.Gamma, 49, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54050, Area.HotShelter, Character.Gamma, 50, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54051, Area.HotShelter, Character.Gamma, 51, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54052, Area.HotShelter, Character.Gamma, 52, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54053, Area.HotShelter, Character.Gamma, 53, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54054, Area.HotShelter, Character.Gamma, 54, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54055, Area.HotShelter, Character.Gamma, 55, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54056, Area.HotShelter, Character.Gamma, 56, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54057, Area.HotShelter, Character.Gamma, 57, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54058, Area.HotShelter, Character.Gamma, 58, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54059, Area.HotShelter, Character.Gamma, 59, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54060, Area.HotShelter, Character.Gamma, 60, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54061, Area.HotShelter, Character.Gamma, 61, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54062, Area.HotShelter, Character.Gamma, 62, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54063, Area.HotShelter, Character.Gamma, 63, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54064, Area.HotShelter, Character.Gamma, 64, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54065, Area.HotShelter, Character.Gamma, 65, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54066, Area.HotShelter, Character.Gamma, 66, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54067, Area.HotShelter, Character.Gamma, 67, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54068, Area.HotShelter, Character.Gamma, 68, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54069, Area.HotShelter, Character.Gamma, 69, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54070, Area.HotShelter, Character.Gamma, 70, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54071, Area.HotShelter, Character.Gamma, 71, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54072, Area.HotShelter, Character.Gamma, 72, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54073, Area.HotShelter, Character.Gamma, 73, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54074, Area.HotShelter, Character.Gamma, 74, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54075, Area.HotShelter, Character.Gamma, 75, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54076, Area.HotShelter, Character.Gamma, 76, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54077, Area.HotShelter, Character.Gamma, 77, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54078, Area.HotShelter, Character.Gamma, 78, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54079, Area.HotShelter, Character.Gamma, 79, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54080, Area.HotShelter, Character.Gamma, 80, Enemy.Leon, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54081, Area.HotShelter, Character.Gamma, 81, Enemy.Leon, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54082, Area.HotShelter, Character.Gamma, 82, Enemy.Leon, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54083, Area.HotShelter, Character.Gamma, 83, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54084, Area.HotShelter, Character.Gamma, 84, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54085, Area.HotShelter, Character.Gamma, 85, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54086, Area.HotShelter, Character.Gamma, 86, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54087, Area.HotShelter, Character.Gamma, 87, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54088, Area.HotShelter, Character.Gamma, 88, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54089, Area.HotShelter, Character.Gamma, 89, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54090, Area.HotShelter, Character.Gamma, 90, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54091, Area.HotShelter, Character.Gamma, 91, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54092, Area.HotShelter, Character.Gamma, 92, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54093, Area.HotShelter, Character.Gamma, 93, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54094, Area.HotShelter, Character.Gamma, 94, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54095, Area.HotShelter, Character.Gamma, 95, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54096, Area.HotShelter, Character.Gamma, 96, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54097, Area.HotShelter, Character.Gamma, 97, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54098, Area.HotShelter, Character.Gamma, 98, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54099, Area.HotShelter, Character.Gamma, 99, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54100, Area.HotShelter, Character.Gamma, 100, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54101, Area.HotShelter, Character.Gamma, 101, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [],
                  []),
    EnemyLocation(54102, Area.HotShelter, Character.Gamma, 102, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [],
                  []),
    EnemyLocation(54103, Area.HotShelter, Character.Gamma, 103, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [],
                  []),
    EnemyLocation(54104, Area.HotShelter, Character.Gamma, 104, Enemy.EggKeeper, [JetBooster], [JetBooster], [], [],
                  []),
    EnemyLocation(54105, Area.HotShelter, Character.Gamma, 105, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54106, Area.HotShelter, Character.Gamma, 106, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54107, Area.HotShelter, Character.Gamma, 107, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54108, Area.HotShelter, Character.Gamma, 108, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54109, Area.HotShelter, Character.Gamma, 109, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54110, Area.HotShelter, Character.Gamma, 110, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54111, Area.HotShelter, Character.Gamma, 111, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54112, Area.HotShelter, Character.Gamma, 112, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54113, Area.HotShelter, Character.Gamma, 113, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54114, Area.HotShelter, Character.Gamma, 114, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54115, Area.HotShelter, Character.Gamma, 115, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54116, Area.HotShelter, Character.Gamma, 116, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(54117, Area.HotShelter, Character.Gamma, 117, Enemy.Kiki, [JetBooster], [JetBooster], [], [], []),
    EnemyLocation(63001, Area.HotShelter, Character.Big, 1, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(63002, Area.HotShelter, Character.Big, 2, Enemy.Kiki, [], [], [], [], []),
    EnemyLocation(63003, Area.HotShelter, Character.Big, 3, Enemy.Kiki, [LifeBelt], [LifeBelt], [], [LifeBelt],
                  [LifeBelt]),
    EnemyLocation(63004, Area.HotShelter, Character.Big, 4, Enemy.Kiki, [LifeBelt], [LifeBelt], [], [LifeBelt],
                  [LifeBelt]),
    EnemyLocation(63005, Area.HotShelter, Character.Big, 5, Enemy.Kiki, [LifeBelt], [LifeBelt], [], [LifeBelt],
                  [LifeBelt]),
]

capsule_location_table: List[CapsuleLocation] = [
    CapsuleLocation(10501, Area.EmeraldCoast, Character.Sonic, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(10502, Area.EmeraldCoast, Character.Sonic, 2, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(10503, Area.EmeraldCoast, Character.Sonic, 3, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(10504, Area.EmeraldCoast, Character.Sonic, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(10505, Area.EmeraldCoast, Character.Sonic, 5, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(10506, Area.EmeraldCoast, Character.Sonic, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(10507, Area.EmeraldCoast, Character.Sonic, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(10508, Area.EmeraldCoast, Character.Sonic, 8, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(10509, Area.EmeraldCoast, Character.Sonic, 9, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(10510, Area.EmeraldCoast, Character.Sonic, 10, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(10511, Area.EmeraldCoast, Character.Sonic, 11, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(10512, Area.EmeraldCoast, Character.Sonic, 12, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(10513, Area.EmeraldCoast, Character.Sonic, 13, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(10514, Area.EmeraldCoast, Character.Sonic, 14, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(10515, Area.EmeraldCoast, Character.Sonic, 15, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(10516, Area.EmeraldCoast, Character.Sonic, 16, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(10517, Area.EmeraldCoast, Character.Sonic, 17, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(10518, Area.EmeraldCoast, Character.Sonic, 18, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(10519, Area.EmeraldCoast, Character.Sonic, 19, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(10520, Area.EmeraldCoast, Character.Sonic, 20, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(51501, Area.EmeraldCoast, Character.Gamma, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(51502, Area.EmeraldCoast, Character.Gamma, 2, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(51503, Area.EmeraldCoast, Character.Gamma, 3, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(51504, Area.EmeraldCoast, Character.Gamma, 4, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51505, Area.EmeraldCoast, Character.Gamma, 5, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51506, Area.EmeraldCoast, Character.Gamma, 6, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51507, Area.EmeraldCoast, Character.Gamma, 7, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51508, Area.EmeraldCoast, Character.Gamma, 8, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51509, Area.EmeraldCoast, Character.Gamma, 9, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51510, Area.EmeraldCoast, Character.Gamma, 10, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(51511, Area.EmeraldCoast, Character.Gamma, 11, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51512, Area.EmeraldCoast, Character.Gamma, 12, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(51513, Area.EmeraldCoast, Character.Gamma, 13, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(62501, Area.EmeraldCoast, Character.Big, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(62502, Area.EmeraldCoast, Character.Big, 2, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(11501, Area.WindyValley, Character.Sonic, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(11502, Area.WindyValley, Character.Sonic, 2, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(11503, Area.WindyValley, Character.Sonic, 3, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(11504, Area.WindyValley, Character.Sonic, 4, Capsule.ExtraLife, [LightShoes], [], [], [], []),
    CapsuleLocation(11505, Area.WindyValley, Character.Sonic, 5, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(11506, Area.WindyValley, Character.Sonic, 6, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(11507, Area.WindyValley, Character.Sonic, 7, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(11508, Area.WindyValley, Character.Sonic, 8, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(11509, Area.WindyValley, Character.Sonic, 9, Capsule.MagneticShield, [LightShoes], [], [], [], []),
    CapsuleLocation(11510, Area.WindyValley, Character.Sonic, 10, Capsule.ExtraLife, [LightShoes], [], [], [], []),
    CapsuleLocation(11511, Area.WindyValley, Character.Sonic, 11, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(11512, Area.WindyValley, Character.Sonic, 12, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(11513, Area.WindyValley, Character.Sonic, 13, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(11514, Area.WindyValley, Character.Sonic, 14, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(11515, Area.WindyValley, Character.Sonic, 15, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(11516, Area.WindyValley, Character.Sonic, 16, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(11517, Area.WindyValley, Character.Sonic, 17, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(20501, Area.WindyValley, Character.Tails, 1, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(20502, Area.WindyValley, Character.Tails, 2, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(20503, Area.WindyValley, Character.Tails, 3, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(20504, Area.WindyValley, Character.Tails, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(20505, Area.WindyValley, Character.Tails, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(20506, Area.WindyValley, Character.Tails, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(20507, Area.WindyValley, Character.Tails, 7, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(20508, Area.WindyValley, Character.Tails, 8, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(20509, Area.WindyValley, Character.Tails, 9, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(20510, Area.WindyValley, Character.Tails, 10, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(52501, Area.WindyValley, Character.Gamma, 1, Capsule.ExtraLife, [JetBooster], [], [], [], []),
    CapsuleLocation(52502, Area.WindyValley, Character.Gamma, 2, Capsule.SpeedUp, [JetBooster], [], [], [], []),
    CapsuleLocation(52503, Area.WindyValley, Character.Gamma, 3, Capsule.TenRings, [JetBooster], [], [], [], []),
    CapsuleLocation(52504, Area.WindyValley, Character.Gamma, 4, Capsule.FiveRings, [JetBooster], [], [], [], []),
    CapsuleLocation(52505, Area.WindyValley, Character.Gamma, 5, Capsule.Invincibility, [JetBooster], [], [], [], []),
    CapsuleLocation(52506, Area.WindyValley, Character.Gamma, 6, Capsule.MagneticShield, [JetBooster], [], [], [], []),
    CapsuleLocation(52507, Area.WindyValley, Character.Gamma, 7, Capsule.RandomRings, [JetBooster], [], [], [], []),
    CapsuleLocation(52508, Area.WindyValley, Character.Gamma, 8, Capsule.ExtraLife, [JetBooster], [], [], [], []),
    CapsuleLocation(52509, Area.WindyValley, Character.Gamma, 9, Capsule.RandomRings, [JetBooster], [], [], [], []),
    CapsuleLocation(52510, Area.WindyValley, Character.Gamma, 10, Capsule.RandomRings, [JetBooster], [], [], [], []),
    CapsuleLocation(14501, Area.TwinklePark, Character.Sonic, 1, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14502, Area.TwinklePark, Character.Sonic, 2, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(14503, Area.TwinklePark, Character.Sonic, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(14504, Area.TwinklePark, Character.Sonic, 4, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14505, Area.TwinklePark, Character.Sonic, 5, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14506, Area.TwinklePark, Character.Sonic, 6, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14507, Area.TwinklePark, Character.Sonic, 7, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14508, Area.TwinklePark, Character.Sonic, 8, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(14509, Area.TwinklePark, Character.Sonic, 9, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(14510, Area.TwinklePark, Character.Sonic, 10, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(14511, Area.TwinklePark, Character.Sonic, 11, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14512, Area.TwinklePark, Character.Sonic, 12, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14513, Area.TwinklePark, Character.Sonic, 13, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14514, Area.TwinklePark, Character.Sonic, 14, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14515, Area.TwinklePark, Character.Sonic, 15, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14516, Area.TwinklePark, Character.Sonic, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(14517, Area.TwinklePark, Character.Sonic, 17, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14518, Area.TwinklePark, Character.Sonic, 18, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14519, Area.TwinklePark, Character.Sonic, 19, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14520, Area.TwinklePark, Character.Sonic, 20, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(14521, Area.TwinklePark, Character.Sonic, 21, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14522, Area.TwinklePark, Character.Sonic, 22, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(14523, Area.TwinklePark, Character.Sonic, 23, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14524, Area.TwinklePark, Character.Sonic, 24, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14525, Area.TwinklePark, Character.Sonic, 25, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14526, Area.TwinklePark, Character.Sonic, 26, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(14527, Area.TwinklePark, Character.Sonic, 27, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14528, Area.TwinklePark, Character.Sonic, 28, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14529, Area.TwinklePark, Character.Sonic, 29, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14530, Area.TwinklePark, Character.Sonic, 30, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(14531, Area.TwinklePark, Character.Sonic, 31, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(14532, Area.TwinklePark, Character.Sonic, 32, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(14533, Area.TwinklePark, Character.Sonic, 33, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(14534, Area.TwinklePark, Character.Sonic, 34, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(14535, Area.TwinklePark, Character.Sonic, 35, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(14536, Area.TwinklePark, Character.Sonic, 36, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(14537, Area.TwinklePark, Character.Sonic, 37, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(14538, Area.TwinklePark, Character.Sonic, 38, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(14539, Area.TwinklePark, Character.Sonic, 39, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(14540, Area.TwinklePark, Character.Sonic, 40, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(40501, Area.TwinklePark, Character.Amy, 1, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(40502, Area.TwinklePark, Character.Amy, 2, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(40503, Area.TwinklePark, Character.Amy, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(40504, Area.TwinklePark, Character.Amy, 4, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(40505, Area.TwinklePark, Character.Amy, 5, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(40506, Area.TwinklePark, Character.Amy, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(40507, Area.TwinklePark, Character.Amy, 7, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(40508, Area.TwinklePark, Character.Amy, 8, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(40509, Area.TwinklePark, Character.Amy, 9, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(60501, Area.TwinklePark, Character.Big, 1, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(60502, Area.TwinklePark, Character.Big, 2, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(15501, Area.SpeedHighway, Character.Sonic, 1, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(15502, Area.SpeedHighway, Character.Sonic, 2, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15503, Area.SpeedHighway, Character.Sonic, 3, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15504, Area.SpeedHighway, Character.Sonic, 4, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15505, Area.SpeedHighway, Character.Sonic, 5, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15506, Area.SpeedHighway, Character.Sonic, 6, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15507, Area.SpeedHighway, Character.Sonic, 7, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(15508, Area.SpeedHighway, Character.Sonic, 8, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(15509, Area.SpeedHighway, Character.Sonic, 9, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(15510, Area.SpeedHighway, Character.Sonic, 10, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(15511, Area.SpeedHighway, Character.Sonic, 11, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15512, Area.SpeedHighway, Character.Sonic, 12, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(15513, Area.SpeedHighway, Character.Sonic, 13, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15514, Area.SpeedHighway, Character.Sonic, 14, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15515, Area.SpeedHighway, Character.Sonic, 15, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15516, Area.SpeedHighway, Character.Sonic, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(15517, Area.SpeedHighway, Character.Sonic, 17, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(15518, Area.SpeedHighway, Character.Sonic, 18, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15519, Area.SpeedHighway, Character.Sonic, 19, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(15520, Area.SpeedHighway, Character.Sonic, 20, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(15521, Area.SpeedHighway, Character.Sonic, 21, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(15522, Area.SpeedHighway, Character.Sonic, 22, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15523, Area.SpeedHighway, Character.Sonic, 23, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(15524, Area.SpeedHighway, Character.Sonic, 24, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(15525, Area.SpeedHighway, Character.Sonic, 25, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15526, Area.SpeedHighway, Character.Sonic, 26, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15527, Area.SpeedHighway, Character.Sonic, 27, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(15528, Area.SpeedHighway, Character.Sonic, 28, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(15529, Area.SpeedHighway, Character.Sonic, 29, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15530, Area.SpeedHighway, Character.Sonic, 30, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(15531, Area.SpeedHighway, Character.Sonic, 31, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15532, Area.SpeedHighway, Character.Sonic, 32, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(15533, Area.SpeedHighway, Character.Sonic, 33, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(15534, Area.SpeedHighway, Character.Sonic, 34, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(15535, Area.SpeedHighway, Character.Sonic, 35, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15536, Area.SpeedHighway, Character.Sonic, 36, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15537, Area.SpeedHighway, Character.Sonic, 37, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15538, Area.SpeedHighway, Character.Sonic, 38, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(15539, Area.SpeedHighway, Character.Sonic, 39, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(15540, Area.SpeedHighway, Character.Sonic, 40, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(15541, Area.SpeedHighway, Character.Sonic, 41, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(15542, Area.SpeedHighway, Character.Sonic, 42, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(15543, Area.SpeedHighway, Character.Sonic, 43, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(24501, Area.SpeedHighway, Character.Tails, 1, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(24502, Area.SpeedHighway, Character.Tails, 2, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(24503, Area.SpeedHighway, Character.Tails, 3, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(24504, Area.SpeedHighway, Character.Tails, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(24505, Area.SpeedHighway, Character.Tails, 5, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(24506, Area.SpeedHighway, Character.Tails, 6, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(24507, Area.SpeedHighway, Character.Tails, 7, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(24508, Area.SpeedHighway, Character.Tails, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(24509, Area.SpeedHighway, Character.Tails, 9, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(24510, Area.SpeedHighway, Character.Tails, 10, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(24511, Area.SpeedHighway, Character.Tails, 11, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(24512, Area.SpeedHighway, Character.Tails, 12, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(24513, Area.SpeedHighway, Character.Tails, 13, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(24514, Area.SpeedHighway, Character.Tails, 14, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(24515, Area.SpeedHighway, Character.Tails, 15, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(24516, Area.SpeedHighway, Character.Tails, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(24517, Area.SpeedHighway, Character.Tails, 17, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(24518, Area.SpeedHighway, Character.Tails, 18, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(24519, Area.SpeedHighway, Character.Tails, 19, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(24520, Area.SpeedHighway, Character.Tails, 20, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(24521, Area.SpeedHighway, Character.Tails, 21, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(24522, Area.SpeedHighway, Character.Tails, 22, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(24523, Area.SpeedHighway, Character.Tails, 23, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(30501, Area.SpeedHighway, Character.Knuckles, 1, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(30502, Area.SpeedHighway, Character.Knuckles, 2, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(30503, Area.SpeedHighway, Character.Knuckles, 3, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(30504, Area.SpeedHighway, Character.Knuckles, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(30505, Area.SpeedHighway, Character.Knuckles, 5, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(30506, Area.SpeedHighway, Character.Knuckles, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(30507, Area.SpeedHighway, Character.Knuckles, 7, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(30508, Area.SpeedHighway, Character.Knuckles, 8, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(16501, Area.RedMountain, Character.Sonic, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16502, Area.RedMountain, Character.Sonic, 2, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(16503, Area.RedMountain, Character.Sonic, 3, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(16504, Area.RedMountain, Character.Sonic, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(16505, Area.RedMountain, Character.Sonic, 5, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(16506, Area.RedMountain, Character.Sonic, 6, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(16507, Area.RedMountain, Character.Sonic, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16508, Area.RedMountain, Character.Sonic, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16509, Area.RedMountain, Character.Sonic, 9, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(16510, Area.RedMountain, Character.Sonic, 10, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(16511, Area.RedMountain, Character.Sonic, 11, Capsule.ExtraLife, [LightShoes], [], [], [], []),
    CapsuleLocation(16512, Area.RedMountain, Character.Sonic, 12, Capsule.ExtraLife, [LightShoes], [], [], [], []),
    CapsuleLocation(16513, Area.RedMountain, Character.Sonic, 13, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(16514, Area.RedMountain, Character.Sonic, 14, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16515, Area.RedMountain, Character.Sonic, 15, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16516, Area.RedMountain, Character.Sonic, 16, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(16517, Area.RedMountain, Character.Sonic, 17, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(16518, Area.RedMountain, Character.Sonic, 18, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(16519, Area.RedMountain, Character.Sonic, 19, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(16520, Area.RedMountain, Character.Sonic, 20, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16521, Area.RedMountain, Character.Sonic, 21, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(16522, Area.RedMountain, Character.Sonic, 22, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(16523, Area.RedMountain, Character.Sonic, 23, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16524, Area.RedMountain, Character.Sonic, 24, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(16525, Area.RedMountain, Character.Sonic, 25, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(16526, Area.RedMountain, Character.Sonic, 26, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16527, Area.RedMountain, Character.Sonic, 27, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(16528, Area.RedMountain, Character.Sonic, 28, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(16529, Area.RedMountain, Character.Sonic, 29, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(32501, Area.RedMountain, Character.Knuckles, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32502, Area.RedMountain, Character.Knuckles, 2, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32503, Area.RedMountain, Character.Knuckles, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(32504, Area.RedMountain, Character.Knuckles, 4, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32505, Area.RedMountain, Character.Knuckles, 5, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(32506, Area.RedMountain, Character.Knuckles, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32507, Area.RedMountain, Character.Knuckles, 7, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(32508, Area.RedMountain, Character.Knuckles, 8, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(32509, Area.RedMountain, Character.Knuckles, 9, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(32510, Area.RedMountain, Character.Knuckles, 10, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32511, Area.RedMountain, Character.Knuckles, 11, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(32512, Area.RedMountain, Character.Knuckles, 12, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32513, Area.RedMountain, Character.Knuckles, 13, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32514, Area.RedMountain, Character.Knuckles, 14, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(32515, Area.RedMountain, Character.Knuckles, 15, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(32516, Area.RedMountain, Character.Knuckles, 16, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(32517, Area.RedMountain, Character.Knuckles, 17, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32518, Area.RedMountain, Character.Knuckles, 18, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(32519, Area.RedMountain, Character.Knuckles, 19, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32520, Area.RedMountain, Character.Knuckles, 20, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(32521, Area.RedMountain, Character.Knuckles, 21, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(32522, Area.RedMountain, Character.Knuckles, 22, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(32523, Area.RedMountain, Character.Knuckles, 23, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(53501, Area.RedMountain, Character.Gamma, 1, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(53502, Area.RedMountain, Character.Gamma, 2, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(53503, Area.RedMountain, Character.Gamma, 3, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(53504, Area.RedMountain, Character.Gamma, 4, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(53505, Area.RedMountain, Character.Gamma, 5, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(53506, Area.RedMountain, Character.Gamma, 6, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(53507, Area.RedMountain, Character.Gamma, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(53508, Area.RedMountain, Character.Gamma, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(53509, Area.RedMountain, Character.Gamma, 9, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(53510, Area.RedMountain, Character.Gamma, 10, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17501, Area.SkyDeck, Character.Sonic, 1, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(17502, Area.SkyDeck, Character.Sonic, 2, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17503, Area.SkyDeck, Character.Sonic, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(17504, Area.SkyDeck, Character.Sonic, 4, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17505, Area.SkyDeck, Character.Sonic, 5, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17506, Area.SkyDeck, Character.Sonic, 6, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17507, Area.SkyDeck, Character.Sonic, 7, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17508, Area.SkyDeck, Character.Sonic, 8, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(17509, Area.SkyDeck, Character.Sonic, 9, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17510, Area.SkyDeck, Character.Sonic, 10, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(17511, Area.SkyDeck, Character.Sonic, 11, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(17512, Area.SkyDeck, Character.Sonic, 12, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17513, Area.SkyDeck, Character.Sonic, 13, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17514, Area.SkyDeck, Character.Sonic, 14, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17515, Area.SkyDeck, Character.Sonic, 15, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17516, Area.SkyDeck, Character.Sonic, 16, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17517, Area.SkyDeck, Character.Sonic, 17, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17518, Area.SkyDeck, Character.Sonic, 18, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17519, Area.SkyDeck, Character.Sonic, 19, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17520, Area.SkyDeck, Character.Sonic, 20, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17521, Area.SkyDeck, Character.Sonic, 21, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17522, Area.SkyDeck, Character.Sonic, 22, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17523, Area.SkyDeck, Character.Sonic, 23, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17524, Area.SkyDeck, Character.Sonic, 24, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17525, Area.SkyDeck, Character.Sonic, 25, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(17526, Area.SkyDeck, Character.Sonic, 26, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17527, Area.SkyDeck, Character.Sonic, 27, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17528, Area.SkyDeck, Character.Sonic, 28, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17529, Area.SkyDeck, Character.Sonic, 29, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17530, Area.SkyDeck, Character.Sonic, 30, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(17531, Area.SkyDeck, Character.Sonic, 31, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(17532, Area.SkyDeck, Character.Sonic, 32, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17533, Area.SkyDeck, Character.Sonic, 33, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(17534, Area.SkyDeck, Character.Sonic, 34, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(17535, Area.SkyDeck, Character.Sonic, 35, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(17536, Area.SkyDeck, Character.Sonic, 36, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17537, Area.SkyDeck, Character.Sonic, 37, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17538, Area.SkyDeck, Character.Sonic, 38, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(17539, Area.SkyDeck, Character.Sonic, 39, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17540, Area.SkyDeck, Character.Sonic, 40, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17541, Area.SkyDeck, Character.Sonic, 41, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(17542, Area.SkyDeck, Character.Sonic, 42, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17543, Area.SkyDeck, Character.Sonic, 43, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17544, Area.SkyDeck, Character.Sonic, 44, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(17545, Area.SkyDeck, Character.Sonic, 45, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17546, Area.SkyDeck, Character.Sonic, 46, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17547, Area.SkyDeck, Character.Sonic, 47, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(17548, Area.SkyDeck, Character.Sonic, 48, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17549, Area.SkyDeck, Character.Sonic, 49, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(17550, Area.SkyDeck, Character.Sonic, 50, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(17551, Area.SkyDeck, Character.Sonic, 51, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17552, Area.SkyDeck, Character.Sonic, 52, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17553, Area.SkyDeck, Character.Sonic, 53, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17554, Area.SkyDeck, Character.Sonic, 54, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17555, Area.SkyDeck, Character.Sonic, 55, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17556, Area.SkyDeck, Character.Sonic, 56, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(17557, Area.SkyDeck, Character.Sonic, 57, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(17558, Area.SkyDeck, Character.Sonic, 58, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(17559, Area.SkyDeck, Character.Sonic, 59, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17560, Area.SkyDeck, Character.Sonic, 60, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(17561, Area.SkyDeck, Character.Sonic, 61, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(17562, Area.SkyDeck, Character.Sonic, 62, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17563, Area.SkyDeck, Character.Sonic, 63, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17564, Area.SkyDeck, Character.Sonic, 64, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17565, Area.SkyDeck, Character.Sonic, 65, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(17566, Area.SkyDeck, Character.Sonic, 66, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23501, Area.SkyDeck, Character.Tails, 1, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23502, Area.SkyDeck, Character.Tails, 2, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(23503, Area.SkyDeck, Character.Tails, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23504, Area.SkyDeck, Character.Tails, 4, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(23505, Area.SkyDeck, Character.Tails, 5, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23506, Area.SkyDeck, Character.Tails, 6, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(23507, Area.SkyDeck, Character.Tails, 7, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23508, Area.SkyDeck, Character.Tails, 8, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23509, Area.SkyDeck, Character.Tails, 9, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(23510, Area.SkyDeck, Character.Tails, 10, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(23511, Area.SkyDeck, Character.Tails, 11, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(23512, Area.SkyDeck, Character.Tails, 12, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(23513, Area.SkyDeck, Character.Tails, 13, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(23514, Area.SkyDeck, Character.Tails, 14, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23515, Area.SkyDeck, Character.Tails, 15, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23516, Area.SkyDeck, Character.Tails, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23517, Area.SkyDeck, Character.Tails, 17, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23518, Area.SkyDeck, Character.Tails, 18, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(23519, Area.SkyDeck, Character.Tails, 19, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(23520, Area.SkyDeck, Character.Tails, 20, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(23521, Area.SkyDeck, Character.Tails, 21, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(23522, Area.SkyDeck, Character.Tails, 22, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(23523, Area.SkyDeck, Character.Tails, 23, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(23524, Area.SkyDeck, Character.Tails, 24, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(23525, Area.SkyDeck, Character.Tails, 25, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23526, Area.SkyDeck, Character.Tails, 26, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23527, Area.SkyDeck, Character.Tails, 27, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23528, Area.SkyDeck, Character.Tails, 28, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(23529, Area.SkyDeck, Character.Tails, 29, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23530, Area.SkyDeck, Character.Tails, 30, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(23531, Area.SkyDeck, Character.Tails, 31, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23532, Area.SkyDeck, Character.Tails, 32, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(23533, Area.SkyDeck, Character.Tails, 33, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(23534, Area.SkyDeck, Character.Tails, 34, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23535, Area.SkyDeck, Character.Tails, 35, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(23536, Area.SkyDeck, Character.Tails, 36, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(34501, Area.SkyDeck, Character.Knuckles, 1, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(34502, Area.SkyDeck, Character.Knuckles, 2, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(34503, Area.SkyDeck, Character.Knuckles, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(34504, Area.SkyDeck, Character.Knuckles, 4, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(34505, Area.SkyDeck, Character.Knuckles, 5, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(34506, Area.SkyDeck, Character.Knuckles, 6, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(34507, Area.SkyDeck, Character.Knuckles, 7, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(34508, Area.SkyDeck, Character.Knuckles, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(34509, Area.SkyDeck, Character.Knuckles, 9, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(34510, Area.SkyDeck, Character.Knuckles, 10, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(34511, Area.SkyDeck, Character.Knuckles, 11, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(34512, Area.SkyDeck, Character.Knuckles, 12, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(18501, Area.LostWorld, Character.Sonic, 1, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(18502, Area.LostWorld, Character.Sonic, 2, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(18503, Area.LostWorld, Character.Sonic, 3, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(18504, Area.LostWorld, Character.Sonic, 4, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(18505, Area.LostWorld, Character.Sonic, 5, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(18506, Area.LostWorld, Character.Sonic, 6, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(18507, Area.LostWorld, Character.Sonic, 7, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(18508, Area.LostWorld, Character.Sonic, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(18509, Area.LostWorld, Character.Sonic, 9, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(18510, Area.LostWorld, Character.Sonic, 10, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(18511, Area.LostWorld, Character.Sonic, 11, Capsule.Shield, [LightShoes], [], [], [], []),
    CapsuleLocation(18512, Area.LostWorld, Character.Sonic, 12, Capsule.RandomRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18513, Area.LostWorld, Character.Sonic, 13, Capsule.MagneticShield, [LightShoes], [], [], [], []),
    CapsuleLocation(18514, Area.LostWorld, Character.Sonic, 14, Capsule.RandomRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18515, Area.LostWorld, Character.Sonic, 15, Capsule.FiveRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18516, Area.LostWorld, Character.Sonic, 16, Capsule.RandomRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18517, Area.LostWorld, Character.Sonic, 17, Capsule.TenRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18518, Area.LostWorld, Character.Sonic, 18, Capsule.TenRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18519, Area.LostWorld, Character.Sonic, 19, Capsule.FiveRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18520, Area.LostWorld, Character.Sonic, 20, Capsule.RandomRings, [LightShoes], [], [], [], []),
    CapsuleLocation(18521, Area.LostWorld, Character.Sonic, 21, Capsule.Shield, [LightShoes], [], [], [], []),
    CapsuleLocation(18522, Area.LostWorld, Character.Sonic, 22, Capsule.ExtraLife, [LightShoes], [], [], [], []),
    CapsuleLocation(18523, Area.LostWorld, Character.Sonic, 23, Capsule.RandomRings, [LightShoes], [], [], [], []),
    CapsuleLocation(33501, Area.LostWorld, Character.Knuckles, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(33502, Area.LostWorld, Character.Knuckles, 2, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(33503, Area.LostWorld, Character.Knuckles, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(33504, Area.LostWorld, Character.Knuckles, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(33505, Area.LostWorld, Character.Knuckles, 5, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(33506, Area.LostWorld, Character.Knuckles, 6, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(33507, Area.LostWorld, Character.Knuckles, 7, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(13501, Area.IceCap, Character.Sonic, 1, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(13502, Area.IceCap, Character.Sonic, 2, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(13503, Area.IceCap, Character.Sonic, 3, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(13504, Area.IceCap, Character.Sonic, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(13505, Area.IceCap, Character.Sonic, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(13506, Area.IceCap, Character.Sonic, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(13507, Area.IceCap, Character.Sonic, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(13508, Area.IceCap, Character.Sonic, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(13509, Area.IceCap, Character.Sonic, 9, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(61501, Area.IceCap, Character.Big, 1, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(61502, Area.IceCap, Character.Big, 2, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(61503, Area.IceCap, Character.Big, 3, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(61504, Area.IceCap, Character.Big, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(61505, Area.IceCap, Character.Big, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(61506, Area.IceCap, Character.Big, 6, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(61507, Area.IceCap, Character.Big, 7, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(61508, Area.IceCap, Character.Big, 8, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(61509, Area.IceCap, Character.Big, 9, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(61510, Area.IceCap, Character.Big, 10, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(61511, Area.IceCap, Character.Big, 11, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(61512, Area.IceCap, Character.Big, 12, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(12501, Area.Casinopolis, Character.Sonic, 1, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(12502, Area.Casinopolis, Character.Sonic, 2, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(12503, Area.Casinopolis, Character.Sonic, 3, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12504, Area.Casinopolis, Character.Sonic, 4, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(12505, Area.Casinopolis, Character.Sonic, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12506, Area.Casinopolis, Character.Sonic, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12507, Area.Casinopolis, Character.Sonic, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12508, Area.Casinopolis, Character.Sonic, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12509, Area.Casinopolis, Character.Sonic, 9, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12510, Area.Casinopolis, Character.Sonic, 10, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(12511, Area.Casinopolis, Character.Sonic, 11, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12512, Area.Casinopolis, Character.Sonic, 12, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12513, Area.Casinopolis, Character.Sonic, 13, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12514, Area.Casinopolis, Character.Sonic, 14, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(12515, Area.Casinopolis, Character.Sonic, 15, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12516, Area.Casinopolis, Character.Sonic, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12517, Area.Casinopolis, Character.Sonic, 17, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12518, Area.Casinopolis, Character.Sonic, 18, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12519, Area.Casinopolis, Character.Sonic, 19, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12520, Area.Casinopolis, Character.Sonic, 20, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12521, Area.Casinopolis, Character.Sonic, 21, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12522, Area.Casinopolis, Character.Sonic, 22, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12523, Area.Casinopolis, Character.Sonic, 23, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12524, Area.Casinopolis, Character.Sonic, 24, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12525, Area.Casinopolis, Character.Sonic, 25, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12526, Area.Casinopolis, Character.Sonic, 26, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12527, Area.Casinopolis, Character.Sonic, 27, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12528, Area.Casinopolis, Character.Sonic, 28, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12529, Area.Casinopolis, Character.Sonic, 29, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12530, Area.Casinopolis, Character.Sonic, 30, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12531, Area.Casinopolis, Character.Sonic, 31, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12532, Area.Casinopolis, Character.Sonic, 32, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12533, Area.Casinopolis, Character.Sonic, 33, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12534, Area.Casinopolis, Character.Sonic, 34, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12535, Area.Casinopolis, Character.Sonic, 35, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12536, Area.Casinopolis, Character.Sonic, 36, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12537, Area.Casinopolis, Character.Sonic, 37, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12538, Area.Casinopolis, Character.Sonic, 38, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12539, Area.Casinopolis, Character.Sonic, 39, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12540, Area.Casinopolis, Character.Sonic, 40, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12541, Area.Casinopolis, Character.Sonic, 41, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12542, Area.Casinopolis, Character.Sonic, 42, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12543, Area.Casinopolis, Character.Sonic, 43, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12544, Area.Casinopolis, Character.Sonic, 44, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12545, Area.Casinopolis, Character.Sonic, 45, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(12546, Area.Casinopolis, Character.Sonic, 46, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(12547, Area.Casinopolis, Character.Sonic, 47, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(12548, Area.Casinopolis, Character.Sonic, 48, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(12549, Area.Casinopolis, Character.Sonic, 49, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(12550, Area.Casinopolis, Character.Sonic, 50, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(12551, Area.Casinopolis, Character.Sonic, 51, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(12552, Area.Casinopolis, Character.Sonic, 52, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(21501, Area.Casinopolis, Character.Tails, 1, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(21502, Area.Casinopolis, Character.Tails, 2, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(21503, Area.Casinopolis, Character.Tails, 3, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(21504, Area.Casinopolis, Character.Tails, 4, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(21505, Area.Casinopolis, Character.Tails, 5, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(21506, Area.Casinopolis, Character.Tails, 6, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(21507, Area.Casinopolis, Character.Tails, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21508, Area.Casinopolis, Character.Tails, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21509, Area.Casinopolis, Character.Tails, 9, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(21510, Area.Casinopolis, Character.Tails, 10, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21511, Area.Casinopolis, Character.Tails, 11, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21512, Area.Casinopolis, Character.Tails, 12, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21513, Area.Casinopolis, Character.Tails, 13, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21514, Area.Casinopolis, Character.Tails, 14, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21515, Area.Casinopolis, Character.Tails, 15, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(21516, Area.Casinopolis, Character.Tails, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21517, Area.Casinopolis, Character.Tails, 17, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21518, Area.Casinopolis, Character.Tails, 18, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(21519, Area.Casinopolis, Character.Tails, 19, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(21520, Area.Casinopolis, Character.Tails, 20, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21521, Area.Casinopolis, Character.Tails, 21, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21522, Area.Casinopolis, Character.Tails, 22, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21523, Area.Casinopolis, Character.Tails, 23, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(21524, Area.Casinopolis, Character.Tails, 24, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21525, Area.Casinopolis, Character.Tails, 25, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21526, Area.Casinopolis, Character.Tails, 26, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21527, Area.Casinopolis, Character.Tails, 27, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21528, Area.Casinopolis, Character.Tails, 28, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21529, Area.Casinopolis, Character.Tails, 29, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21530, Area.Casinopolis, Character.Tails, 30, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21531, Area.Casinopolis, Character.Tails, 31, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21532, Area.Casinopolis, Character.Tails, 32, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21533, Area.Casinopolis, Character.Tails, 33, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21534, Area.Casinopolis, Character.Tails, 34, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21535, Area.Casinopolis, Character.Tails, 35, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21536, Area.Casinopolis, Character.Tails, 36, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21537, Area.Casinopolis, Character.Tails, 37, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21538, Area.Casinopolis, Character.Tails, 38, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21539, Area.Casinopolis, Character.Tails, 39, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21540, Area.Casinopolis, Character.Tails, 40, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21541, Area.Casinopolis, Character.Tails, 41, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(21542, Area.Casinopolis, Character.Tails, 42, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(31501, Area.Casinopolis, Character.Knuckles, 1, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(31502, Area.Casinopolis, Character.Knuckles, 2, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(31503, Area.Casinopolis, Character.Knuckles, 3, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(31504, Area.Casinopolis, Character.Knuckles, 4, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(31505, Area.Casinopolis, Character.Knuckles, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(31506, Area.Casinopolis, Character.Knuckles, 6, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(31507, Area.Casinopolis, Character.Knuckles, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(31508, Area.Casinopolis, Character.Knuckles, 8, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(31509, Area.Casinopolis, Character.Knuckles, 9, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(31510, Area.Casinopolis, Character.Knuckles, 10, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(31511, Area.Casinopolis, Character.Knuckles, 11, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(31512, Area.Casinopolis, Character.Knuckles, 12, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(31513, Area.Casinopolis, Character.Knuckles, 13, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(31514, Area.Casinopolis, Character.Knuckles, 14, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(31515, Area.Casinopolis, Character.Knuckles, 15, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(31516, Area.Casinopolis, Character.Knuckles, 16, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(19501, Area.FinalEgg, Character.Sonic, 1, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19502, Area.FinalEgg, Character.Sonic, 2, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(19503, Area.FinalEgg, Character.Sonic, 3, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19504, Area.FinalEgg, Character.Sonic, 4, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19505, Area.FinalEgg, Character.Sonic, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19506, Area.FinalEgg, Character.Sonic, 6, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19507, Area.FinalEgg, Character.Sonic, 7, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19508, Area.FinalEgg, Character.Sonic, 8, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19509, Area.FinalEgg, Character.Sonic, 9, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19510, Area.FinalEgg, Character.Sonic, 10, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19511, Area.FinalEgg, Character.Sonic, 11, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19512, Area.FinalEgg, Character.Sonic, 12, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19513, Area.FinalEgg, Character.Sonic, 13, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19514, Area.FinalEgg, Character.Sonic, 14, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(19515, Area.FinalEgg, Character.Sonic, 15, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19516, Area.FinalEgg, Character.Sonic, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19517, Area.FinalEgg, Character.Sonic, 17, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19518, Area.FinalEgg, Character.Sonic, 18, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19519, Area.FinalEgg, Character.Sonic, 19, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(19520, Area.FinalEgg, Character.Sonic, 20, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(19521, Area.FinalEgg, Character.Sonic, 21, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(19522, Area.FinalEgg, Character.Sonic, 22, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19523, Area.FinalEgg, Character.Sonic, 23, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19524, Area.FinalEgg, Character.Sonic, 24, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19525, Area.FinalEgg, Character.Sonic, 25, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(19526, Area.FinalEgg, Character.Sonic, 26, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19527, Area.FinalEgg, Character.Sonic, 27, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19528, Area.FinalEgg, Character.Sonic, 28, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19529, Area.FinalEgg, Character.Sonic, 29, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19530, Area.FinalEgg, Character.Sonic, 30, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19531, Area.FinalEgg, Character.Sonic, 31, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19532, Area.FinalEgg, Character.Sonic, 32, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19533, Area.FinalEgg, Character.Sonic, 33, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19534, Area.FinalEgg, Character.Sonic, 34, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19535, Area.FinalEgg, Character.Sonic, 35, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(19536, Area.FinalEgg, Character.Sonic, 36, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(19537, Area.FinalEgg, Character.Sonic, 37, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(19538, Area.FinalEgg, Character.Sonic, 38, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19539, Area.FinalEgg, Character.Sonic, 39, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19540, Area.FinalEgg, Character.Sonic, 40, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19541, Area.FinalEgg, Character.Sonic, 41, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(19542, Area.FinalEgg, Character.Sonic, 42, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19543, Area.FinalEgg, Character.Sonic, 43, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19544, Area.FinalEgg, Character.Sonic, 44, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19545, Area.FinalEgg, Character.Sonic, 45, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19546, Area.FinalEgg, Character.Sonic, 46, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19547, Area.FinalEgg, Character.Sonic, 47, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19548, Area.FinalEgg, Character.Sonic, 48, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19549, Area.FinalEgg, Character.Sonic, 49, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19550, Area.FinalEgg, Character.Sonic, 50, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(19551, Area.FinalEgg, Character.Sonic, 51, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(19552, Area.FinalEgg, Character.Sonic, 52, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19553, Area.FinalEgg, Character.Sonic, 53, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19554, Area.FinalEgg, Character.Sonic, 54, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(19555, Area.FinalEgg, Character.Sonic, 55, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19556, Area.FinalEgg, Character.Sonic, 56, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19557, Area.FinalEgg, Character.Sonic, 57, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19558, Area.FinalEgg, Character.Sonic, 58, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19559, Area.FinalEgg, Character.Sonic, 59, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19560, Area.FinalEgg, Character.Sonic, 60, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(19561, Area.FinalEgg, Character.Sonic, 61, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(42501, Area.FinalEgg, Character.Amy, 1, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(42502, Area.FinalEgg, Character.Amy, 2, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(42503, Area.FinalEgg, Character.Amy, 3, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(42504, Area.FinalEgg, Character.Amy, 4, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(42505, Area.FinalEgg, Character.Amy, 5, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(42506, Area.FinalEgg, Character.Amy, 6, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(42507, Area.FinalEgg, Character.Amy, 7, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(50501, Area.FinalEgg, Character.Gamma, 1, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50502, Area.FinalEgg, Character.Gamma, 2, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50503, Area.FinalEgg, Character.Gamma, 3, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50504, Area.FinalEgg, Character.Gamma, 4, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50505, Area.FinalEgg, Character.Gamma, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50506, Area.FinalEgg, Character.Gamma, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50507, Area.FinalEgg, Character.Gamma, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50508, Area.FinalEgg, Character.Gamma, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50509, Area.FinalEgg, Character.Gamma, 9, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(50510, Area.FinalEgg, Character.Gamma, 10, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41501, Area.HotShelter, Character.Amy, 1, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(41502, Area.HotShelter, Character.Amy, 2, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(41503, Area.HotShelter, Character.Amy, 3, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(41504, Area.HotShelter, Character.Amy, 4, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(41505, Area.HotShelter, Character.Amy, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41506, Area.HotShelter, Character.Amy, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41507, Area.HotShelter, Character.Amy, 7, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(41508, Area.HotShelter, Character.Amy, 8, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(41509, Area.HotShelter, Character.Amy, 9, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41510, Area.HotShelter, Character.Amy, 10, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41511, Area.HotShelter, Character.Amy, 11, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41512, Area.HotShelter, Character.Amy, 12, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(41513, Area.HotShelter, Character.Amy, 13, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(41514, Area.HotShelter, Character.Amy, 14, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(41515, Area.HotShelter, Character.Amy, 15, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(41516, Area.HotShelter, Character.Amy, 16, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41517, Area.HotShelter, Character.Amy, 17, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(41518, Area.HotShelter, Character.Amy, 18, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(41519, Area.HotShelter, Character.Amy, 19, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41520, Area.HotShelter, Character.Amy, 20, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(41521, Area.HotShelter, Character.Amy, 21, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(41522, Area.HotShelter, Character.Amy, 22, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(41523, Area.HotShelter, Character.Amy, 23, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(41524, Area.HotShelter, Character.Amy, 24, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41525, Area.HotShelter, Character.Amy, 25, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(41526, Area.HotShelter, Character.Amy, 26, Capsule.FiveRings, [], [], [], [], []),
    CapsuleLocation(41527, Area.HotShelter, Character.Amy, 27, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(41528, Area.HotShelter, Character.Amy, 28, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41529, Area.HotShelter, Character.Amy, 29, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41530, Area.HotShelter, Character.Amy, 30, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(41531, Area.HotShelter, Character.Amy, 31, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41532, Area.HotShelter, Character.Amy, 32, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(41533, Area.HotShelter, Character.Amy, 33, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(41534, Area.HotShelter, Character.Amy, 34, Capsule.Bomb, [], [], [], [], []),
    CapsuleLocation(41535, Area.HotShelter, Character.Amy, 35, Capsule.Invincibility, [], [], [], [], []),
    CapsuleLocation(41536, Area.HotShelter, Character.Amy, 36, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(41537, Area.HotShelter, Character.Amy, 37, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(54501, Area.HotShelter, Character.Gamma, 1, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(54502, Area.HotShelter, Character.Gamma, 2, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(54503, Area.HotShelter, Character.Gamma, 3, Capsule.MagneticShield, [], [], [], [], []),
    CapsuleLocation(54504, Area.HotShelter, Character.Gamma, 4, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(54505, Area.HotShelter, Character.Gamma, 5, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(54506, Area.HotShelter, Character.Gamma, 6, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(54507, Area.HotShelter, Character.Gamma, 7, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(54508, Area.HotShelter, Character.Gamma, 8, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(54509, Area.HotShelter, Character.Gamma, 9, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(54510, Area.HotShelter, Character.Gamma, 10, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(54511, Area.HotShelter, Character.Gamma, 11, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(54512, Area.HotShelter, Character.Gamma, 12, Capsule.RandomRings, [JetBooster], [JetBooster], [],
                    [], []),
    CapsuleLocation(54513, Area.HotShelter, Character.Gamma, 13, Capsule.FiveRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54514, Area.HotShelter, Character.Gamma, 14, Capsule.RandomRings, [JetBooster], [JetBooster], [],
                    [], []),
    CapsuleLocation(54515, Area.HotShelter, Character.Gamma, 15, Capsule.RandomRings, [JetBooster], [JetBooster], [],
                    [], []),
    CapsuleLocation(54516, Area.HotShelter, Character.Gamma, 16, Capsule.MagneticShield, [JetBooster], [JetBooster], [],
                    [], []),
    CapsuleLocation(54517, Area.HotShelter, Character.Gamma, 17, Capsule.ExtraLife, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54518, Area.HotShelter, Character.Gamma, 18, Capsule.ExtraLife, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54519, Area.HotShelter, Character.Gamma, 19, Capsule.MagneticShield, [JetBooster], [JetBooster], [],
                    [], []),
    CapsuleLocation(54520, Area.HotShelter, Character.Gamma, 20, Capsule.Invincibility, [JetBooster], [JetBooster], [],
                    [], []),
    CapsuleLocation(54521, Area.HotShelter, Character.Gamma, 21, Capsule.ExtraLife, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54522, Area.HotShelter, Character.Gamma, 22, Capsule.FiveRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54523, Area.HotShelter, Character.Gamma, 23, Capsule.FiveRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54524, Area.HotShelter, Character.Gamma, 24, Capsule.Shield, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54525, Area.HotShelter, Character.Gamma, 25, Capsule.FiveRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54526, Area.HotShelter, Character.Gamma, 26, Capsule.TenRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54527, Area.HotShelter, Character.Gamma, 27, Capsule.FiveRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54528, Area.HotShelter, Character.Gamma, 28, Capsule.TenRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54529, Area.HotShelter, Character.Gamma, 29, Capsule.TenRings, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54530, Area.HotShelter, Character.Gamma, 30, Capsule.MagneticShield, [JetBooster], [JetBooster], [],
                    [], []),
    CapsuleLocation(54531, Area.HotShelter, Character.Gamma, 31, Capsule.Shield, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(54532, Area.HotShelter, Character.Gamma, 32, Capsule.Bomb, [JetBooster], [JetBooster], [], [], []),
    CapsuleLocation(54533, Area.HotShelter, Character.Gamma, 33, Capsule.Shield, [JetBooster], [JetBooster], [], [],
                    []),
    CapsuleLocation(63501, Area.HotShelter, Character.Big, 1, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(63502, Area.HotShelter, Character.Big, 2, Capsule.SpeedUp, [], [], [], [], []),
    CapsuleLocation(63503, Area.HotShelter, Character.Big, 3, Capsule.Shield, [], [], [], [], []),
    CapsuleLocation(63504, Area.HotShelter, Character.Big, 4, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(63505, Area.HotShelter, Character.Big, 5, Capsule.TenRings, [], [], [], [], []),
    CapsuleLocation(63506, Area.HotShelter, Character.Big, 6, Capsule.RandomRings, [], [], [], [], []),
    CapsuleLocation(63507, Area.HotShelter, Character.Big, 7, Capsule.ExtraLife, [], [], [], [], []),
    CapsuleLocation(63508, Area.HotShelter, Character.Big, 8, Capsule.SpeedUp, [LifeBelt], [LifeBelt], [], [LifeBelt],
                    [LifeBelt]),
    CapsuleLocation(63509, Area.HotShelter, Character.Big, 9, Capsule.TenRings, [LifeBelt], [LifeBelt], [], [LifeBelt],
                    [LifeBelt]),
    CapsuleLocation(63510, Area.HotShelter, Character.Big, 10, Capsule.TenRings, [LifeBelt], [LifeBelt], [], [LifeBelt],
                    [LifeBelt]),
]

fish_location_table: List[FishLocation] = [
    FishLocation(950, Area.TwinklePark, Fish.LargemouthBass, [], [], [], [], []),
    FishLocation(951, Area.TwinklePark, Fish.Piranha, [], [], [], [], []),
    FishLocation(952, Area.TwinklePark, Fish.MechaFish, [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                 [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4]),
    FishLocation(953, Area.EmeraldCoast, Fish.Hammerhead, [], [], [], [], []),
    FishLocation(954, Area.EmeraldCoast, Fish.StripedBeakfish, [], [], [], [], []),
    FishLocation(955, Area.EmeraldCoast, Fish.MechaFish, [], [], [], [], []),
    FishLocation(956, Area.EmeraldCoast, Fish.Shark, [], [], [], [], []),
    FishLocation(957, Area.EmeraldCoast, Fish.SeaBass, [], [], [], [], []),
    FishLocation(958, Area.EmeraldCoast, Fish.RedSeaBream, [], [], [], [], []),
    FishLocation(959, Area.EmeraldCoast, Fish.MorayEel, [], [], [], [], []),
    FishLocation(960, Area.EmeraldCoast, Fish.BlueMarlin, [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                 [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4]),
    FishLocation(961, Area.IceCap, Fish.Hammerhead, [], [], [], [], []),
    FishLocation(962, Area.IceCap, Fish.MechaFish, [], [], [], [], []),
    FishLocation(963, Area.IceCap, Fish.LargemouthBass, [], [], [], [], []),
    FishLocation(964, Area.IceCap, Fish.Salmon, [], [], [], [], []),
    FishLocation(965, Area.IceCap, Fish.Shark, [], [], [], [], []),
    FishLocation(966, Area.IceCap, Fish.JapaneseEel, [], [], [], [], []),
    FishLocation(967, Area.HotShelter, Fish.AnglerFish, [LifeBelt], [], [], [], []),
    FishLocation(968, Area.HotShelter, Fish.Hammerhead, [], [], [], [], []),
    FishLocation(969, Area.HotShelter, Fish.Oarfish, [LifeBelt], [], [], [], []),
    FishLocation(970, Area.HotShelter, Fish.Shark, [], [], [], [], []),
    FishLocation(971, Area.HotShelter, Fish.Coelacanth, [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4],
                 [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4], [Lure1, Lure2, Lure3, Lure4]),
    FishLocation(972, Area.HotShelter, Fish.MorayEel, [LifeBelt], [], [], [], []),
]

boss_location_table: List[BossFightLocation] = [
    BossFightLocation(700, Area.Chaos0, [P_SONIC], LocationName.Boss.Chaos0, False),
    BossFightLocation(710, Area.Chaos2, [P_KNUCKLES], LocationName.Boss.Chaos2, False),
    BossFightLocation(720, Area.EggWalker, [P_TAILS], LocationName.Boss.EggWalker, False),
    BossFightLocation(730, Area.EggHornet, [P_SONIC], LocationName.Boss.EggHornet, False),
    BossFightLocation(731, Area.EggHornet, [P_TAILS], LocationName.Boss.EggHornet, False),
    BossFightLocation(739, Area.EggHornet, [P_SONIC, P_TAILS], LocationName.Boss.EggHornet, True),
    BossFightLocation(740, Area.Chaos4, [P_SONIC], LocationName.Boss.Chaos4, False),
    BossFightLocation(741, Area.Chaos4, [P_TAILS], LocationName.Boss.Chaos4, False),
    BossFightLocation(742, Area.Chaos4, [P_KNUCKLES], LocationName.Boss.Chaos4, False),
    BossFightLocation(749, Area.Chaos4, [P_SONIC, P_TAILS, P_KNUCKLES], LocationName.Boss.Chaos4, True),
    BossFightLocation(750, Area.BetaEggViper, [P_SONIC], LocationName.Boss.EggViper, False),
    BossFightLocation(760, Area.BetaEggViper, [P_GAMMA], LocationName.Boss.E101Beta, False),
    BossFightLocation(770, Area.Chaos6ZeroBeta, [P_SONIC], LocationName.Boss.Chaos6, False),
    BossFightLocation(771, Area.Chaos6ZeroBeta, [P_KNUCKLES], LocationName.Boss.Chaos6, False),
    BossFightLocation(772, Area.Chaos6ZeroBeta, [P_BIG], LocationName.Boss.Chaos6, False),
    BossFightLocation(779, Area.Chaos6ZeroBeta, [P_SONIC, P_KNUCKLES, P_BIG], LocationName.Boss.Chaos6, True),
    BossFightLocation(780, Area.Chaos6ZeroBeta, [P_GAMMA], LocationName.Boss.E101mkII, False),
    BossFightLocation(790, Area.Chaos6ZeroBeta, [P_AMY], LocationName.Boss.Zero, False),
]

chao_egg_location_table: List[ChaoEggLocation] = [
    ChaoEggLocation(900, LocationName.Chao.GoldEgg, Area.SSChaoGarden, EVERYONE,
                    [[HotelKey, PolicePass], [CasinoKey, ShutterKey, StationKey, PolicePass]]),
    ChaoEggLocation(901, LocationName.Chao.SilverEgg, Area.MRChaoGarden, [P_SONIC, P_TAILS, P_KNUCKLES, P_AMY, P_BIG],
                    []),
    ChaoEggLocation(902, LocationName.Chao.BlackEgg, Area.ECChaoGarden, [P_AMY, P_GAMMA, P_BIG], []),
]

chao_race_location_table: List[ChaoRaceLocation] = [
    ChaoRaceLocation(905, LocationName.Chao.PearlCourse, Area.SSChaoGarden),
    ChaoRaceLocation(906, LocationName.Chao.AmethystCourse, Area.SSChaoGarden),
    ChaoRaceLocation(907, LocationName.Chao.SapphireCourse, Area.SSChaoGarden),
    ChaoRaceLocation(908, LocationName.Chao.RubyCourse, Area.SSChaoGarden),
    ChaoRaceLocation(909, LocationName.Chao.EmeraldCourse, Area.SSChaoGarden),
]
