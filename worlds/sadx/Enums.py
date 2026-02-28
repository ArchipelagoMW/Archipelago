import re
from enum import Enum, auto
from typing import List, Dict

from Options import OptionSet

SADX_BASE_ID = 543800000


def pascal_to_space(s):
    s = re.sub(r'^(Ss)', 'S.S.', s)
    s = re.sub(r'^(SS)', 'S.S.', s)
    s = re.sub(r'^(Mr)', 'M.R.', s)
    s = re.sub(r'^(MR)', 'M.R.', s)
    s = re.sub(r'^(Tp)', 'T.P.', s)
    s = re.sub(r'^(TP)', 'T.P.', s)
    s = re.sub(r'^(Ec)', 'E.C.', s)
    s = re.sub(r'^(EC)', 'E.C.', s)
    s = re.sub(r'_', ' ', s)  # Replace underscores with spaces
    s = re.sub(r'(?<!^)(?=[A-Z][a-z])', ' ', s)  # Add spaces before PascalCase words
    s = re.sub(r'(?<=[a-zA-Z])(?=\d)', ' ', s)  # Add spaces between letters and numbers
    s = re.sub(r'\s{2,}', ' ', s)  # Remove extra spaces
    return s.strip()


class Character(Enum):
    Sonic = 1
    Tails = auto()
    Knuckles = auto()
    Amy = auto()
    Big = auto()
    Gamma = auto()


def remove_character_suffix(string: str) -> str:
    for character in Character:
        string = re.sub(rf"\s*\({character.name}\)", "", string)
    return re.sub(r"\s{2,}", " ", string).strip()


EVERYONE: List[Character] = [Character.Sonic, Character.Tails, Character.Knuckles,
                             Character.Amy, Character.Big, Character.Gamma]
SONIC_TAILS: List[Character] = [Character.Sonic, Character.Tails]
FLYERS: List[Character] = [Character.Tails, Character.Knuckles]


class Upgrade(Enum):
    LightShoes = auto()
    CrystalRing = auto()
    AncientLight = auto()
    JetAnkle = auto()
    RhythmBadge = auto()
    ShovelClaw = auto()
    FightingGloves = auto()
    LongHammer = auto()
    WarriorFeather = auto()
    JetBooster = auto()
    LaserBlaster = auto()
    LifeBelt = auto()
    PowerRod = auto()
    Lure1 = auto()
    Lure2 = auto()
    Lure3 = auto()
    Lure4 = auto()


class Enemy(Enum):
    BoaBoa = 1
    Buyon = auto()
    CopSpeeder = auto()
    ElectroSpinner = auto()
    EggKeeper = auto()
    Gola = auto()
    IceBall = auto()
    KartKiki = auto()
    Kiki = auto()
    Leon = auto()
    Rhinotank = auto()
    Spinner = auto()
    Sweep = auto()
    SpikySpinner = auto()


class Capsule(Enum):
    ExtraLife = 1
    Shield = auto()
    MagneticShield = auto()
    SpeedUp = auto()
    Invincibility = auto()
    Bomb = auto()
    FiveRings = auto()
    TenRings = auto()
    RandomRings = auto()


class Fish(Enum):
    AnglerFish = 0
    Hammerhead = auto()
    StripedBeakfish = auto()
    BlueMarlin = auto()
    MechaFish = auto()
    LargemouthBass = auto()
    Piranha = auto()
    Oarfish = auto()
    Salmon = auto()
    Shark = auto()
    SeaBass = auto()
    Coelacanth = auto()
    RedSeaBream = auto()
    JapaneseEel = auto()
    MorayEel = auto()


class SubLevelMission(Enum):
    B = 0
    A = auto()
    Sonic = auto()
    Tails = auto()
    Knuckles = auto()
    Amy = auto()
    Big = auto()
    Gamma = auto()


class LevelMission(Enum):
    C = 0
    B = auto()
    A = auto()
    S = auto()


class SubLevel(Enum):
    SandHill = auto()
    TwinkleCircuit = auto()
    SkyChaseAct1 = auto()
    SkyChaseAct2 = auto()


class AdventureField(Enum):
    StationSquare = auto()
    MysticRuins = auto()
    EggCarrier = auto()
    Past = auto()


class EnemySanityCategory(Enum):
    Sonic = 0
    Tails = auto()
    Knuckles = auto()
    Amy = auto()
    Big = auto()
    Gamma = auto()

    @classmethod
    def from_object_list(cls, objects: OptionSet) -> List['EnemySanityCategory']:
        enum_list = []
        for obj in objects:
            try:
                enum_member = cls[obj]
                enum_list.append(enum_member)
            except (KeyError, AttributeError):
                print(f"Warning: '{getattr(obj, 'value', None)}' is not a valid enum member.")
        return enum_list

    @classmethod
    def to_object_list(cls, enum_map: Dict[int, int]) -> 'OptionSet':
        try:
            enum_names = {member.name for value in enum_map.values()
                          for member in cls if member.value == value}
            return OptionSet(enum_names)
        except Exception as e:
            print(f"Error while converting to object list: {e}")
            return OptionSet({})


class CapsuleSanityCategory(Enum):
    SonicLife = 0
    SonicShield = auto()
    SonicPowerUp = auto()
    SonicRing = auto()
    TailsLife = auto()
    TailsShield = auto()
    TailsPowerUp = auto()
    TailsRing = auto()
    KnucklesLife = auto()
    KnucklesShield = auto()
    KnucklesPowerUp = auto()
    KnucklesRing = auto()
    AmyLife = auto()
    AmyShield = auto()
    AmyPowerUp = auto()
    AmyRing = auto()
    BigLife = auto()
    BigShield = auto()
    BigPowerUp = auto()
    BigRing = auto()
    GammaLife = auto()
    GammaShield = auto()
    GammaPowerUp = auto()
    GammaRing = auto()

    @classmethod
    def from_object_list(cls, objects: OptionSet) -> List['CapsuleSanityCategory']:
        enum_list = []
        for obj in objects:
            try:
                normalized_value = re.sub(r'[-\s]', '', obj)
                enum_member = cls[normalized_value]
                enum_list.append(enum_member)
            except (KeyError, AttributeError):
                print(f"Warning: '{getattr(obj, 'value', None)}' is not a valid enum member.")
        return enum_list

    @classmethod
    def to_object_list(cls, enum_map: Dict[int, int]) -> 'OptionSet':
        try:
            enum_names = {member.name for value in enum_map.values()
                          for member in cls if member.value == value}
            return OptionSet(enum_names)
        except Exception as e:
            print(f"Error while converting to object list: {e}")
            return OptionSet({})


class Area(Enum):
    CityHall = 0
    Station = auto()
    Casino = auto()
    Sewers = auto()
    SSMain = auto()
    TPTunnel = auto()
    Hotel = auto()
    HotelPool = auto()
    TPLobby = auto()
    MRMain = auto()
    AngelIsland = auto()
    IceCave = auto()
    PastAltar = auto()
    PastMain = auto()
    Jungle = auto()
    FinalEggTower = auto()
    ECOutside = auto()
    ECBridge = auto()
    ECDeck = auto()
    CaptainRoom = auto()
    PrivateRoom = auto()
    ECPool = auto()
    Arsenal = auto()
    ECInside = auto()
    HedgehogHammer = auto()
    PrisonHall = auto()
    WaterTank = auto()
    WarpHall = auto()
    SSChaoGarden = auto()
    MRChaoGarden = auto()
    ECChaoGarden = auto()
    EmeraldCoast = auto()
    WindyValley = auto()
    Casinopolis = auto()
    IceCap = auto()
    TwinklePark = auto()
    SpeedHighway = auto()
    RedMountain = auto()
    SkyDeck = auto()
    LostWorld = auto()
    FinalEgg = auto()
    HotShelter = auto()
    Chaos0 = auto()
    EggWalker = auto()
    Chaos2 = auto()
    TwinkleCircuit = auto()
    Chaos4 = auto()
    EggHornet = auto()
    SkyChase1 = auto()
    SandHill = auto()
    BetaEggViper = auto()
    SkyChase2 = auto()
    Chaos6ZeroBeta = auto()

    def __lt__(self, other):
        if isinstance(other, Area):
            return self.value < other.value
        return NotImplemented


class AreaConnection(Enum):
    # City Hall
    CityHall_to_SsMain = (Area.CityHall, Area.SSMain)
    CityHall_to_Sewers = (Area.CityHall, Area.Sewers)
    CityHall_to_SpeedHighway = (Area.CityHall, Area.SpeedHighway)
    CityHall_to_Chaos0 = (Area.CityHall, Area.Chaos0)

    # Station
    Station_to_SsMain = (Area.Station, Area.SSMain)
    Station_to_MrMain = (Area.Station, Area.MRMain)
    Station_to_Casino = (Area.Station, Area.Casino)

    # Casino
    Casino_to_Station = (Area.Casino, Area.Station)
    Casino_to_Casinopolis = (Area.Casino, Area.Casinopolis)
    Casino_to_Hotel = (Area.Casino, Area.Hotel)
    Casino_to_EggWalker = (Area.Casino, Area.EggWalker)

    # Sewers
    Sewers_to_CityHall = (Area.Sewers, Area.CityHall)
    Sewers_to_TPTunnel = (Area.Sewers, Area.TPTunnel)

    # SSMain
    SsMain_to_Hotel = (Area.SSMain, Area.Hotel)
    SsMain_to_Station = (Area.SSMain, Area.Station)
    SsMain_to_CityHall = (Area.SSMain, Area.CityHall)
    SsMain_to_TpTunnel = (Area.SSMain, Area.TPTunnel)
    SsMain_to_EcOutside = (Area.SSMain, Area.ECOutside)
    SsMain_to_Bridge = (Area.SSMain, Area.ECBridge)
    SsMain_to_SpeedHighway = (Area.SSMain, Area.SpeedHighway)

    # Hotel
    Hotel_to_SsMain = (Area.Hotel, Area.SSMain)
    Hotel_to_Casino = (Area.Hotel, Area.Casino)
    Hotel_to_SsChaoGarden = (Area.Hotel, Area.SSChaoGarden)
    Hotel_to_Chaos2 = (Area.Hotel, Area.Chaos2)
    Hotel_to_HotelPool = (Area.Hotel, Area.HotelPool)

    # Hotel Pool
    HotelPool_to_Hotel = (Area.HotelPool, Area.Hotel)
    HotelPool_to_EmeraldCoast = (Area.HotelPool, Area.EmeraldCoast)

    # Twinkle Park Tunnel
    TpTunnel_to_SsMain = (Area.TPTunnel, Area.SSMain)
    TpTunnel_to_TpLobby = (Area.TPTunnel, Area.TPLobby)
    TpTunnel_to_Sewers = (Area.TPTunnel, Area.Sewers)

    # Twinkle Park Lobby
    TpLobby_to_TpTunnel = (Area.TPLobby, Area.TPTunnel)
    TpLobby_to_TwinklePark = (Area.TPLobby, Area.TwinklePark)
    TpLobby_to_TwinkleCircuit = (Area.TPLobby, Area.TwinkleCircuit)

    # MRMain
    MrMain_to_Station = (Area.MRMain, Area.Station)
    MrMain_to_EcOutside = (Area.MRMain, Area.ECOutside)
    MrMain_to_Bridge = (Area.MRMain, Area.ECBridge)
    MrMain_to_AngelIsland = (Area.MRMain, Area.AngelIsland)
    MrMain_to_WindyValley = (Area.MRMain, Area.WindyValley)
    MrMain_to_Jungle = (Area.MRMain, Area.Jungle)
    MrMain_to_Chaos4 = (Area.MRMain, Area.Chaos4)
    MrMain_to_EggHornet = (Area.MRMain, Area.EggHornet)
    MrMain_to_MrChaoGarden = (Area.MRMain, Area.MRChaoGarden)
    MrMain_to_SkyChase1 = (Area.MRMain, Area.SkyChase1)

    # Angel Island
    AngelIsland_to_MrMain = (Area.AngelIsland, Area.MRMain)
    AngelIsland_to_IceCave = (Area.AngelIsland, Area.IceCave)
    AngelIsland_to_RedMountain = (Area.AngelIsland, Area.RedMountain)
    AngelIsland_to_PastAltar = (Area.AngelIsland, Area.PastAltar)

    # Ice Cave
    IceCave_to_AngelIsland = (Area.IceCave, Area.AngelIsland)
    IceCave_to_IceCap = (Area.IceCave, Area.IceCap)

    # Past Altar
    PastAltar_to_AngelIsland = (Area.PastAltar, Area.AngelIsland)
    PastAltar_to_PastMain = (Area.PastAltar, Area.PastMain)

    # Past Main
    PastMain_to_PastAltar = (Area.PastMain, Area.PastAltar)
    PastMain_to_Jungle = (Area.PastMain, Area.Jungle)

    # Jungle
    Jungle_to_MrMain = (Area.Jungle, Area.MRMain)
    Jungle_to_LostWorld = (Area.Jungle, Area.LostWorld)
    Jungle_to_LostWorldAlternative = (Area.Jungle, Area.LostWorld, True)
    Jungle_to_FinalEggTower = (Area.Jungle, Area.FinalEggTower)
    Jungle_to_SandHill = (Area.Jungle, Area.SandHill)
    Jungle_to_PastMain = (Area.Jungle, Area.PastMain)

    # Final Egg Tower
    FinalEggTower_to_Jungle = (Area.FinalEggTower, Area.Jungle)
    FinalEggTower_to_FinalEgg = (Area.FinalEggTower, Area.FinalEgg)
    FinalEggTower_to_FinalEggAlternative = (Area.FinalEggTower, Area.FinalEgg, True)
    FinalEggTower_to_BetaEggViper = (Area.FinalEggTower, Area.BetaEggViper)
    FinalEggTower_to_EcInside = (Area.FinalEggTower, Area.ECInside)
    # Egg Carrier Outside (Untransformed)
    EcOutside_to_SsMain = (Area.ECOutside, Area.SSMain)
    EcOutside_to_MrMain = (Area.ECOutside, Area.MRMain)
    EcOutside_to_SkyChase2 = (Area.ECOutside, Area.SkyChase2)
    EcOutside_to_Chaos6ZeroBeta = (Area.ECOutside, Area.Chaos6ZeroBeta)
    EcOutside_to_EcInsideMonorail = (Area.ECOutside, Area.ECInside)
    EcOutside_to_EcInsideEggLift = (Area.ECOutside, Area.ECInside)
    EcOutside_to_CaptainRoom = (Area.ECOutside, Area.CaptainRoom)
    EcOutside_to_Pool = (Area.ECOutside, Area.ECPool)

    # Bridge (Transformed)
    Bridge_to_SsMain = (Area.ECBridge, Area.SSMain)
    Bridge_to_MrMain = (Area.ECBridge, Area.MRMain)
    Bridge_to_SkyDeck = (Area.ECBridge, Area.SkyDeck)
    Bridge_to_SkyChase2 = (Area.ECBridge, Area.SkyChase2)
    Bridge_to_Chaos6ZeroBeta = (Area.ECBridge, Area.Chaos6ZeroBeta)
    Bridge_to_EcInsideMonorail = (Area.ECBridge, Area.ECInside)

    # Deck (Transformed)
    Deck_to_Pool = (Area.ECDeck, Area.ECPool)
    Deck_to_CaptainRoom = (Area.ECDeck, Area.CaptainRoom)
    Deck_to_PrivateRoom = (Area.ECDeck, Area.PrivateRoom)
    Deck_to_PrivateRoomAlternative = (Area.ECDeck, Area.PrivateRoom, True)
    Deck_to_EcInsideEggLift = (Area.ECDeck, Area.ECInside)

    # Captain Room
    CaptainRoom_to_EcOutside = (Area.CaptainRoom, Area.ECOutside)
    CaptainRoom_to_Deck = (Area.CaptainRoom, Area.ECDeck)
    CaptainRoom_to_PrivateRoom = (Area.CaptainRoom, Area.PrivateRoom)

    # Private Room
    PrivateRoom_to_CaptainRoom = (Area.PrivateRoom, Area.CaptainRoom)
    PrivateRoom_to_Deck = (Area.PrivateRoom, Area.ECDeck)
    PrivateRoom_to_DeckAlternative = (Area.PrivateRoom, Area.ECDeck, True)

    # Pool
    Pool_to_EcOutside = (Area.ECPool, Area.ECOutside)
    Pool_to_Deck = (Area.ECPool, Area.ECDeck)
    Pool_to_SkyDeck = (Area.ECPool, Area.SkyDeck)

    # Arsenal
    Arsenal_to_EcInside = (Area.Arsenal, Area.ECInside)

    # Egg Carrier Inside
    EcInside_to_EcOutsideEggLift = (Area.ECInside, Area.ECOutside)
    EcInside_to_EcOutsideMonorail = (Area.ECInside, Area.ECOutside)
    EcInside_to_DeckEggLift = (Area.ECInside, Area.ECDeck)
    EcInside_to_BridgeMonorail = (Area.ECInside, Area.ECBridge)
    EcInside_to_HotShelter = (Area.ECInside, Area.HotShelter)
    EcInside_to_HedgehogHammer = (Area.ECInside, Area.HedgehogHammer)
    EcInside_to_FinalEggTower = (Area.ECInside, Area.FinalEggTower)
    EcInside_to_WarpHall = (Area.ECInside, Area.WarpHall)
    EcInside_to_Arsenal = (Area.ECInside, Area.Arsenal)
    EcInside_to_WaterTank = (Area.ECInside, Area.WaterTank)

    # Hedgehog Hammer
    HedgehogHammer_to_EcInside = (Area.HedgehogHammer, Area.ECInside)
    HedgehogHammer_to_PrisonHall = (Area.HedgehogHammer, Area.PrisonHall)

    # Prison Hall
    PrisonHall_to_HedgehogHammer = (Area.PrisonHall, Area.HedgehogHammer)

    # Water Tank
    WaterTank_to_EcInside = (Area.WaterTank, Area.ECInside)

    # Warp Hall
    WarpHall_to_EcInside = (Area.WarpHall, Area.ECInside)
    WarpHall_to_EcChaoGarden = (Area.WarpHall, Area.ECChaoGarden)

    SsChaoGarden_to_Hotel = (Area.SSChaoGarden, Area.Hotel)
    MrChaoGarden_to_MrMain = (Area.MRChaoGarden, Area.MRMain)
    EcChaoGarden_to_WarpHall = (Area.ECChaoGarden, Area.WarpHall)

    def __init__(self, area1, area2, alt=False):
        self.area1 = area1
        self.area2 = area2
        self.isAlt = alt

    @classmethod
    def from_areas(cls, area1, area2, alt=False):
        for connection in cls:
            if connection.area1 == area1 and connection.area2 == area2 and connection.isAlt == alt:
                return connection
        return None

    def get_index(self):
        return list(self.__class__.__members__).index(self.name)

    @classmethod
    def from_index(cls, index):
        return list(cls.__members__.values())[int(index)]


level_areas = [
    Area.EmeraldCoast,
    Area.WindyValley,
    Area.Casinopolis,
    Area.IceCap,
    Area.TwinklePark,
    Area.SpeedHighway,
    Area.RedMountain,
    Area.SkyDeck,
    Area.LostWorld,
    Area.FinalEgg,
    Area.HotShelter
]

bosses_areas = [
    Area.Chaos0,
    Area.EggWalker,
    Area.Chaos2,
    Area.TwinkleCircuit,
    Area.Chaos4,
    Area.EggHornet,
    Area.SkyChase1,
    Area.SandHill,
    Area.BetaEggViper,
    Area.SkyChase2,
    Area.Chaos6ZeroBeta,
    Area.SSChaoGarden,
    Area.MRChaoGarden,
    Area.ECChaoGarden
]
level_area_connections = [
    AreaConnection.CityHall_to_SpeedHighway,
    AreaConnection.Casino_to_Casinopolis,
    AreaConnection.SsMain_to_SpeedHighway,
    AreaConnection.HotelPool_to_EmeraldCoast,
    AreaConnection.TpLobby_to_TwinklePark,
    AreaConnection.MrMain_to_WindyValley,
    AreaConnection.AngelIsland_to_RedMountain,
    AreaConnection.IceCave_to_IceCap,
    AreaConnection.Jungle_to_LostWorld,
    AreaConnection.Jungle_to_LostWorldAlternative,
    AreaConnection.FinalEggTower_to_FinalEgg,
    AreaConnection.FinalEggTower_to_FinalEggAlternative,
    AreaConnection.Bridge_to_SkyDeck,
    AreaConnection.Pool_to_SkyDeck,
    AreaConnection.EcInside_to_HotShelter,
]

bosses_area_connections = [
    AreaConnection.CityHall_to_Chaos0,
    AreaConnection.Casino_to_EggWalker,
    AreaConnection.Hotel_to_SsChaoGarden,
    AreaConnection.Hotel_to_Chaos2,
    AreaConnection.TpLobby_to_TwinkleCircuit,
    AreaConnection.MrMain_to_Chaos4,
    AreaConnection.MrMain_to_EggHornet,
    AreaConnection.MrMain_to_MrChaoGarden,
    AreaConnection.MrMain_to_SkyChase1,
    AreaConnection.Jungle_to_SandHill,
    AreaConnection.FinalEggTower_to_BetaEggViper,
    AreaConnection.EcOutside_to_SkyChase2,
    # AreaConnection.Bridge_to_SkyChase2 ,
    AreaConnection.EcOutside_to_Chaos6ZeroBeta,
    # AreaConnection.Bridge_to_Chaos6ZeroBeta ,
    AreaConnection.WarpHall_to_EcChaoGarden,
]

# areas that don't exist:
non_existent_areas = {
    (Character.Tails, Area.EmeraldCoast),
    (Character.Knuckles, Area.EmeraldCoast),
    (Character.Amy, Area.EmeraldCoast),
    (Character.Amy, Area.Casinopolis),
    (Character.Big, Area.Casinopolis),
    (Character.Gamma, Area.Casinopolis),
    (Character.Knuckles, Area.IceCap),
    (Character.Amy, Area.IceCap),
    (Character.Gamma, Area.IceCap),
    (Character.Tails, Area.TwinklePark),
    (Character.Knuckles, Area.TwinklePark),
    (Character.Gamma, Area.TwinklePark),
    (Character.Amy, Area.SpeedHighway),
    (Character.Big, Area.SpeedHighway),
    (Character.Gamma, Area.SpeedHighway),
    (Character.Tails, Area.RedMountain),
    (Character.Amy, Area.RedMountain),
    (Character.Big, Area.RedMountain),
    (Character.Amy, Area.SkyDeck),
    (Character.Big, Area.SkyDeck),
    (Character.Gamma, Area.SkyDeck),
    (Character.Tails, Area.LostWorld),
    (Character.Amy, Area.LostWorld),
    (Character.Big, Area.LostWorld),
    (Character.Gamma, Area.LostWorld),
    (Character.Tails, Area.FinalEgg),
    (Character.Knuckles, Area.FinalEgg),
    (Character.Big, Area.FinalEgg),
    (Character.Sonic, Area.HotShelter),
    (Character.Tails, Area.HotShelter),
    (Character.Knuckles, Area.HotShelter),
    (Character.Tails, Area.Chaos0),
    (Character.Knuckles, Area.Chaos0),
    (Character.Amy, Area.Chaos0),
    (Character.Big, Area.Chaos0),
    (Character.Gamma, Area.Chaos0),
    (Character.Sonic, Area.EggWalker),
    (Character.Knuckles, Area.EggWalker),
    (Character.Amy, Area.EggWalker),
    (Character.Big, Area.EggWalker),
    (Character.Gamma, Area.EggWalker),
    (Character.Sonic, Area.Chaos2),
    (Character.Tails, Area.Chaos2),
    (Character.Amy, Area.Chaos2),
    (Character.Big, Area.Chaos2),
    (Character.Gamma, Area.Chaos2),
    (Character.Amy, Area.Chaos4),
    (Character.Big, Area.Chaos4),
    (Character.Gamma, Area.Chaos4),
    (Character.Knuckles, Area.EggHornet),
    (Character.Amy, Area.EggHornet),
    (Character.Big, Area.EggHornet),
    (Character.Gamma, Area.EggHornet),
    (Character.Knuckles, Area.SkyChase1),
    (Character.Amy, Area.SkyChase1),
    (Character.Big, Area.SkyChase1),
    (Character.Gamma, Area.SkyChase1),
    (Character.Knuckles, Area.SkyChase2),
    (Character.Amy, Area.SkyChase2),
    (Character.Big, Area.SkyChase2),
    (Character.Gamma, Area.SkyChase2),
    (Character.Knuckles, Area.SandHill),
    (Character.Amy, Area.SandHill),
    (Character.Big, Area.SandHill),
    (Character.Gamma, Area.SandHill),
    (Character.Tails, Area.BetaEggViper),
    (Character.Knuckles, Area.BetaEggViper),
    (Character.Amy, Area.BetaEggViper),
    (Character.Big, Area.BetaEggViper),
    (Character.Tails, Area.Chaos6ZeroBeta),
}
