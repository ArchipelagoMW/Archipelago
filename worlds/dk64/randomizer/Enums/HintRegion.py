"""Hint Region enum."""

from enum import IntEnum, auto


class HintRegion(IntEnum):
    """Hint Region enum."""

    NoRegion = 0
    # Shops
    IslesShops = auto()
    JapesShops = auto()
    AztecShops = auto()
    FactoryShops = auto()
    GalleonShops = auto()
    ForestShops = auto()
    CavesShops = auto()
    CastleShops = auto()
    Jetpac = auto()
    # CB Regions
    IslesCBs = auto()
    JapesCBs = auto()
    AztecCBs = auto()
    FactoryCBs = auto()
    GalleonCBs = auto()
    ForestCBs = auto()
    CavesCBs = auto()
    CastleCBs = auto()
    # Isles
    GameStart = auto()
    Credits = auto()
    MainIsles = auto()
    OuterIsles = auto()
    KremIsles = auto()
    RarewareRoom = auto()
    EarlyLobbies = auto()
    LateLobbies = auto()
    KRool = auto()  # No checks here right now
    # Japes
    Lowlands = auto()
    Hillside = auto()
    StormyTunnel = auto()
    HiveTunnel = auto()
    CavesAndMines = auto()
    # Aztec
    OasisAndTotem = auto()
    TinyTemple = auto()
    FiveDoorTemple = auto()
    LlamaTemple = auto()
    AztecTunnels = auto()
    # Factory
    FactoryStart = auto()
    Testing = auto()
    ResearchAndDevelopment = auto()
    Storage = auto()
    ProductionRoom = auto()
    # Galleon
    GalleonCaverns = auto()
    Lighthouse = auto()
    ShipyardOutskirts = auto()
    TreasureRoom = auto()
    FiveDoorShip = auto()
    # Forest
    ForestCenterAndBeanstalk = auto()
    MushroomExterior = auto()
    MushroomInterior = auto()
    OwlTree = auto()
    Mills = auto()
    # Caves
    MainCaves = auto()
    Igloo = auto()
    Cabins = auto()
    # Castle
    CastleSurroundings = auto()
    CastleRooms = auto()
    CastleUnderground = auto()
    # Other
    Helm = auto()
    Bosses = auto()
    Snide = auto()
    SnideFirstGroup = auto()
    SnideSecondGroup = auto()
    SnideThirdGroup = auto()
    SnideFourthGroup = auto()
    SnideLastGroup = auto()
    # Debuggging
    Error = auto()


HINT_REGION_PAIRING = {
    HintRegion.NoRegion: "Null Region",
    # Shops
    HintRegion.IslesShops: "Isles Shops",
    HintRegion.JapesShops: "Japes Shops",
    HintRegion.AztecShops: "Aztec Shops",
    HintRegion.FactoryShops: "Factory Shops",
    HintRegion.GalleonShops: "Galleon Shops",
    HintRegion.ForestShops: "Forest Shops",
    HintRegion.CavesShops: "Caves Shops",
    HintRegion.CastleShops: "Castle Shops",
    HintRegion.Jetpac: "Jetpac Game",
    HintRegion.SnideFirstGroup: "1st to 8th Blueprint Rewards",
    HintRegion.SnideSecondGroup: "9th to 16th Blueprint Rewards",
    HintRegion.SnideThirdGroup: "17th to 24th Blueprint Rewards",
    HintRegion.SnideFourthGroup: "25th to 32nd Blueprint Rewards",
    HintRegion.SnideLastGroup: "33rd to 40th Blueprint Rewards",
    # CB Regions
    HintRegion.IslesCBs: "Isles Medal Rewards",
    HintRegion.JapesCBs: "Japes Medal Rewards",
    HintRegion.AztecCBs: "Aztec Medal Rewards",
    HintRegion.FactoryCBs: "Factory Medal Rewards",
    HintRegion.GalleonCBs: "Galleon Medal Rewards",
    HintRegion.ForestCBs: "Forest Medal Rewards",
    HintRegion.CavesCBs: "Caves Medal Rewards",
    HintRegion.CastleCBs: "Castle Medal Rewards",
    # Isles
    HintRegion.GameStart: "Game Start",
    HintRegion.Credits: "Credits",
    HintRegion.MainIsles: "Main Isle",
    HintRegion.OuterIsles: "Outer Isles",
    HintRegion.KremIsles: "Krem Isle",
    HintRegion.RarewareRoom: "Rareware Room",
    HintRegion.EarlyLobbies: "Japes - Forest Lobbies",
    HintRegion.LateLobbies: "Caves - Helm Lobbies",
    HintRegion.KRool: "K Rool Arena",
    # Japes
    HintRegion.Lowlands: "Japes Lowlands",
    HintRegion.Hillside: "Japes Hillside",
    HintRegion.StormyTunnel: "Japes Stormy Tunnel Area",
    HintRegion.HiveTunnel: "Hive Tunnel Area",
    HintRegion.CavesAndMines: "Japes Caves & Mines",
    # Aztec
    HintRegion.OasisAndTotem: "Aztec Oasis & Totem Area",
    HintRegion.TinyTemple: "Tiny Temple",
    HintRegion.FiveDoorTemple: "5 Door Temple",
    HintRegion.LlamaTemple: "Llama Temple",
    HintRegion.AztecTunnels: "Various Aztec Tunnels",
    # Factory
    HintRegion.FactoryStart: "Frantic Factory Foyer",
    HintRegion.Testing: "Testing Area",
    HintRegion.ResearchAndDevelopment: "R&D Area",
    HintRegion.Storage: "Storage & Arcade Area",
    HintRegion.ProductionRoom: "Production Room",
    # Galleon
    HintRegion.GalleonCaverns: "Galleon Caverns",
    HintRegion.Lighthouse: "Lighthouse Area",
    HintRegion.ShipyardOutskirts: "Shipyard Outskirts",
    HintRegion.TreasureRoom: "Treasure Room",
    HintRegion.FiveDoorShip: "5 Door Ship",
    # Forest
    HintRegion.ForestCenterAndBeanstalk: "Forest Center & Beanstalk",
    HintRegion.MushroomExterior: "Giant Mushroom Exterior",
    HintRegion.MushroomInterior: "Giant Mushroom Insides",
    HintRegion.OwlTree: "Owl Tree Area",
    HintRegion.Mills: "Forest Mills",
    # Caves
    HintRegion.MainCaves: "Main Caves Area",
    HintRegion.Igloo: "Igloo Area",
    HintRegion.Cabins: "Cabins Area",
    # Castle
    HintRegion.CastleSurroundings: "Castle Surroundings",
    HintRegion.CastleRooms: "Castle Rooms",
    HintRegion.CastleUnderground: "Castle Underground",
    # Other
    HintRegion.Helm: "Hideout Helm",
    HintRegion.Bosses: "Troff 'n' Scoff",
    # Debuggging
    HintRegion.Error: "This should not be hinted",
}

MEDAL_REWARD_REGIONS = (
    HintRegion.IslesCBs,
    HintRegion.JapesCBs,
    HintRegion.AztecCBs,
    HintRegion.FactoryCBs,
    HintRegion.GalleonCBs,
    HintRegion.ForestCBs,
    HintRegion.CavesCBs,
    HintRegion.CastleCBs,
)

SHOP_REGIONS = (
    HintRegion.IslesShops,
    HintRegion.JapesShops,
    HintRegion.AztecShops,
    HintRegion.FactoryShops,
    HintRegion.GalleonShops,
    HintRegion.ForestShops,
    HintRegion.CavesShops,
    HintRegion.CastleShops,
)
