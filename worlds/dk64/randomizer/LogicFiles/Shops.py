# fmt: off
"""Logic file for shops."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.HintRegion import HintRegion
from randomizer.LogicClasses import LocationLogic, Region, TransitionFront

LogicRegions = {
    Regions.FunkyGeneric: Region("Funky Generic", HintRegion.Error, Levels.Shops, False, None, [], [], []),

    Regions.FunkyJapes: Region("Funky Japes", HintRegion.JapesShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedJapesGun, lambda l: l.CanBuy(Locations.SharedJapesGun)),
        LocationLogic(Locations.CoconutGun, lambda l: l.isdonkey and l.CanBuy(Locations.CoconutGun)),
        LocationLogic(Locations.PeanutGun, lambda l: l.isdiddy and l.CanBuy(Locations.PeanutGun)),
        LocationLogic(Locations.GrapeGun, lambda l: l.islanky and l.CanBuy(Locations.GrapeGun)),
        LocationLogic(Locations.FeatherGun, lambda l: l.istiny and l.CanBuy(Locations.FeatherGun)),
        LocationLogic(Locations.PineappleGun, lambda l: l.ischunky and l.CanBuy(Locations.PineappleGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda _: False),
    ]),

    Regions.FunkyAztec: Region("Funky Aztec", HintRegion.AztecShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedAztecGun, lambda l: l.CanBuy(Locations.SharedAztecGun)),
        LocationLogic(Locations.DonkeyAztecGun, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyAztecGun)),
        LocationLogic(Locations.DiddyAztecGun, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyAztecGun)),
        LocationLogic(Locations.LankyAztecGun, lambda l: l.islanky and l.CanBuy(Locations.LankyAztecGun)),
        LocationLogic(Locations.TinyAztecGun, lambda l: l.istiny and l.CanBuy(Locations.TinyAztecGun)),
        LocationLogic(Locations.ChunkyAztecGun, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyAztecGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda _: False),
    ]),

    Regions.FunkyFactory: Region("Funky Factory", HintRegion.FactoryShops, Levels.Shops, False, None, [
        LocationLogic(Locations.AmmoBelt1, lambda l: l.CanBuy(Locations.AmmoBelt1)),
        LocationLogic(Locations.DonkeyFactoryGun, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyFactoryGun)),
        LocationLogic(Locations.DiddyFactoryGun, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyFactoryGun)),
        LocationLogic(Locations.LankyFactoryGun, lambda l: l.islanky and l.CanBuy(Locations.LankyFactoryGun)),
        LocationLogic(Locations.TinyFactoryGun, lambda l: l.istiny and l.CanBuy(Locations.TinyFactoryGun)),
        LocationLogic(Locations.ChunkyFactoryGun, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyFactoryGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda _: False),
    ]),

    Regions.FunkyGalleon: Region("Funky Galleon", HintRegion.GalleonShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedGalleonGun, lambda l: l.CanBuy(Locations.SharedGalleonGun)),
        LocationLogic(Locations.DonkeyGalleonGun, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyGalleonGun)),
        LocationLogic(Locations.DiddyGalleonGun, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyGalleonGun)),
        LocationLogic(Locations.LankyGalleonGun, lambda l: l.islanky and l.CanBuy(Locations.LankyGalleonGun)),
        LocationLogic(Locations.TinyGalleonGun, lambda l: l.istiny and l.CanBuy(Locations.TinyGalleonGun)),
        LocationLogic(Locations.ChunkyGalleonGun, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyGalleonGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda _: False),
    ]),

    Regions.FunkyForest: Region("Funky Forest", HintRegion.ForestShops, Levels.Shops, False, None, [
        LocationLogic(Locations.HomingAmmo, lambda l: l.CanBuy(Locations.HomingAmmo)),
        LocationLogic(Locations.DonkeyForestGun, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyForestGun)),
        LocationLogic(Locations.DiddyForestGun, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyForestGun)),
        LocationLogic(Locations.LankyForestGun, lambda l: l.islanky and l.CanBuy(Locations.LankyForestGun)),
        LocationLogic(Locations.TinyForestGun, lambda l: l.istiny and l.CanBuy(Locations.TinyForestGun)),
        LocationLogic(Locations.ChunkyForestGun, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyForestGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda _: False),
    ]),

    Regions.FunkyCaves: Region("Funky Caves", HintRegion.CavesShops, Levels.Shops, False, None, [
        LocationLogic(Locations.AmmoBelt2, lambda l: l.CanBuy(Locations.AmmoBelt2)),
        LocationLogic(Locations.DonkeyCavesGun, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyCavesGun)),
        LocationLogic(Locations.DiddyCavesGun, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyCavesGun)),
        LocationLogic(Locations.LankyCavesGun, lambda l: l.islanky and l.CanBuy(Locations.LankyCavesGun)),
        LocationLogic(Locations.TinyCavesGun, lambda l: l.istiny and l.CanBuy(Locations.TinyCavesGun)),
        LocationLogic(Locations.ChunkyCavesGun, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyCavesGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda _: False),
    ]),

    Regions.FunkyCastle: Region("Funky Castle", HintRegion.CastleShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SniperSight, lambda l: l.CanBuy(Locations.SniperSight)),
        LocationLogic(Locations.DonkeyCastleGun, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyCastleGun)),
        LocationLogic(Locations.DiddyCastleGun, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyCastleGun)),
        LocationLogic(Locations.LankyCastleGun, lambda l: l.islanky and l.CanBuy(Locations.LankyCastleGun)),
        LocationLogic(Locations.TinyCastleGun, lambda l: l.istiny and l.CanBuy(Locations.TinyCastleGun)),
        LocationLogic(Locations.ChunkyCastleGun, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyCastleGun)),
    ], [], [
        TransitionFront(Regions.FunkyGeneric, lambda _: False),
    ]),

    Regions.CandyGeneric: Region("Candy Generic", HintRegion.Error, Levels.Shops, False, None, [], [], []),

    Regions.CandyAztec: Region("Candy Aztec", HintRegion.AztecShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedAztecInstrument, lambda l: l.CanBuy(Locations.SharedAztecInstrument)),
        LocationLogic(Locations.Bongos, lambda l: l.isdonkey and l.CanBuy(Locations.Bongos)),
        LocationLogic(Locations.Guitar, lambda l: l.isdiddy and l.CanBuy(Locations.Guitar)),
        LocationLogic(Locations.Trombone, lambda l: l.islanky and l.CanBuy(Locations.Trombone)),
        LocationLogic(Locations.Saxophone, lambda l: l.istiny and l.CanBuy(Locations.Saxophone)),
        LocationLogic(Locations.Triangle, lambda l: l.ischunky and l.CanBuy(Locations.Triangle)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda _: False),
    ]),

    Regions.CandyFactory: Region("Candy Factory", HintRegion.FactoryShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedFactoryInstrument, lambda l: l.CanBuy(Locations.SharedFactoryInstrument)),
        LocationLogic(Locations.DonkeyFactoryInstrument, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyFactoryInstrument)),
        LocationLogic(Locations.DiddyFactoryInstrument, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyFactoryInstrument)),
        LocationLogic(Locations.LankyFactoryInstrument, lambda l: l.islanky and l.CanBuy(Locations.LankyFactoryInstrument)),
        LocationLogic(Locations.TinyFactoryInstrument, lambda l: l.istiny and l.CanBuy(Locations.TinyFactoryInstrument)),
        LocationLogic(Locations.ChunkyFactoryInstrument, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyFactoryInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda _: False),
    ]),

    Regions.CandyGalleon: Region("Candy Galleon", HintRegion.GalleonShops, Levels.Shops, False, None, [
        LocationLogic(Locations.MusicUpgrade1, lambda l: l.CanBuy(Locations.MusicUpgrade1)),
        LocationLogic(Locations.DonkeyGalleonInstrument, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyGalleonInstrument)),
        LocationLogic(Locations.DiddyGalleonInstrument, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyGalleonInstrument)),
        LocationLogic(Locations.LankyGalleonInstrument, lambda l: l.islanky and l.CanBuy(Locations.LankyGalleonInstrument)),
        LocationLogic(Locations.TinyGalleonInstrument, lambda l: l.istiny and l.CanBuy(Locations.TinyGalleonInstrument)),
        LocationLogic(Locations.ChunkyGalleonInstrument, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyGalleonInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda _: False),
    ]),

    Regions.CandyCaves: Region("Candy Caves", HintRegion.CavesShops, Levels.Shops, False, None, [
        LocationLogic(Locations.ThirdMelon, lambda l: l.CanBuy(Locations.ThirdMelon)),
        LocationLogic(Locations.DonkeyCavesInstrument, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyCavesInstrument)),
        LocationLogic(Locations.DiddyCavesInstrument, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyCavesInstrument)),
        LocationLogic(Locations.LankyCavesInstrument, lambda l: l.islanky and l.CanBuy(Locations.LankyCavesInstrument)),
        LocationLogic(Locations.TinyCavesInstrument, lambda l: l.istiny and l.CanBuy(Locations.TinyCavesInstrument)),
        LocationLogic(Locations.ChunkyCavesInstrument, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyCavesInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda _: False),
    ]),

    Regions.CandyCastle: Region("Candy Castle", HintRegion.CastleShops, Levels.Shops, False, None, [
        LocationLogic(Locations.MusicUpgrade2, lambda l: l.CanBuy(Locations.MusicUpgrade2)),
        LocationLogic(Locations.DonkeyCastleInstrument, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyCastleInstrument)),
        LocationLogic(Locations.DiddyCastleInstrument, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyCastleInstrument)),
        LocationLogic(Locations.LankyCastleInstrument, lambda l: l.islanky and l.CanBuy(Locations.LankyCastleInstrument)),
        LocationLogic(Locations.TinyCastleInstrument, lambda l: l.istiny and l.CanBuy(Locations.TinyCastleInstrument)),
        LocationLogic(Locations.ChunkyCastleInstrument, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyCastleInstrument)),
    ], [], [
        TransitionFront(Regions.CandyGeneric, lambda _: False),
    ]),

    Regions.CrankyGeneric: Region("Cranky Generic", HintRegion.Jetpac, Levels.Shops, False, None, [
        LocationLogic(Locations.RarewareCoin, lambda l: l.CanGetRarewareCoin()),
    ], [], []),

    Regions.CrankyJapes: Region("Cranky Japes", HintRegion.JapesShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedJapesPotion, lambda l: l.CanBuy(Locations.SharedJapesPotion)),
        LocationLogic(Locations.BaboonBlast, lambda l: l.isdonkey and l.CanBuy(Locations.BaboonBlast)),
        LocationLogic(Locations.ChimpyCharge, lambda l: l.isdiddy and l.CanBuy(Locations.ChimpyCharge)),
        LocationLogic(Locations.Orangstand, lambda l: l.islanky and l.CanBuy(Locations.Orangstand)),
        LocationLogic(Locations.MiniMonkey, lambda l: l.istiny and l.CanBuy(Locations.MiniMonkey)),
        LocationLogic(Locations.HunkyChunky, lambda l: l.ischunky and l.CanBuy(Locations.HunkyChunky)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.CrankyAztec: Region("Cranky Aztec", HintRegion.AztecShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedAztecPotion, lambda l: l.CanBuy(Locations.SharedAztecPotion)),
        LocationLogic(Locations.StrongKong, lambda l: l.isdonkey and l.CanBuy(Locations.StrongKong)),
        LocationLogic(Locations.RocketbarrelBoost, lambda l: l.isdiddy and l.CanBuy(Locations.RocketbarrelBoost)),
        LocationLogic(Locations.LankyAztecPotion, lambda l: l.islanky and l.CanBuy(Locations.LankyAztecPotion)),
        LocationLogic(Locations.TinyAztecPotion, lambda l: l.istiny and l.CanBuy(Locations.TinyAztecPotion)),
        LocationLogic(Locations.ChunkyAztecPotion, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyAztecPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.CrankyFactory: Region("Cranky Factory", HintRegion.FactoryShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedFactoryPotion, lambda l: l.CanBuy(Locations.SharedFactoryPotion)),
        LocationLogic(Locations.GorillaGrab, lambda l: l.isdonkey and l.CanBuy(Locations.GorillaGrab)),
        LocationLogic(Locations.SimianSpring, lambda l: l.isdiddy and l.CanBuy(Locations.SimianSpring)),
        LocationLogic(Locations.BaboonBalloon, lambda l: l.islanky and l.CanBuy(Locations.BaboonBalloon)),
        LocationLogic(Locations.PonyTailTwirl, lambda l: l.istiny and l.CanBuy(Locations.PonyTailTwirl)),
        LocationLogic(Locations.PrimatePunch, lambda l: l.ischunky and l.CanBuy(Locations.PrimatePunch)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.CrankyGalleon: Region("Cranky Galleon", HintRegion.GalleonShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedGalleonPotion, lambda l: l.CanBuy(Locations.SharedGalleonPotion)),
        LocationLogic(Locations.DonkeyGalleonPotion, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyGalleonPotion)),
        LocationLogic(Locations.DiddyGalleonPotion, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyGalleonPotion)),
        LocationLogic(Locations.LankyGalleonPotion, lambda l: l.islanky and l.CanBuy(Locations.LankyGalleonPotion)),
        LocationLogic(Locations.TinyGalleonPotion, lambda l: l.istiny and l.CanBuy(Locations.TinyGalleonPotion)),
        LocationLogic(Locations.ChunkyGalleonPotion, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyGalleonPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.CrankyForest: Region("Cranky Forest", HintRegion.ForestShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SuperSimianSlam, lambda l: l.CanBuy(Locations.SuperSimianSlam)),
        LocationLogic(Locations.DonkeyForestPotion, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyForestPotion)),
        LocationLogic(Locations.DiddyForestPotion, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyForestPotion)),
        LocationLogic(Locations.LankyForestPotion, lambda l: l.islanky and l.CanBuy(Locations.LankyForestPotion)),
        LocationLogic(Locations.TinyForestPotion, lambda l: l.istiny and l.CanBuy(Locations.TinyForestPotion)),
        LocationLogic(Locations.ChunkyForestPotion, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyForestPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.CrankyCaves: Region("Cranky Caves", HintRegion.CavesShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SharedCavesPotion, lambda l: l.CanBuy(Locations.SharedCavesPotion)),
        LocationLogic(Locations.OrangstandSprint, lambda l: l.islanky and l.CanBuy(Locations.OrangstandSprint)),
        LocationLogic(Locations.Monkeyport, lambda l: l.istiny and l.CanBuy(Locations.Monkeyport)),
        LocationLogic(Locations.GorillaGone, lambda l: l.ischunky and l.CanBuy(Locations.GorillaGone)),
        LocationLogic(Locations.DonkeyCavesPotion, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyCavesPotion)),
        LocationLogic(Locations.DiddyCavesPotion, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyCavesPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.CrankyCastle: Region("Cranky Castle", HintRegion.CastleShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SuperDuperSimianSlam, lambda l: l.CanBuy(Locations.SuperDuperSimianSlam)),
        LocationLogic(Locations.DonkeyCastlePotion, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyCastlePotion)),
        LocationLogic(Locations.DiddyCastlePotion, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyCastlePotion)),
        LocationLogic(Locations.LankyCastlePotion, lambda l: l.islanky and l.CanBuy(Locations.LankyCastlePotion)),
        LocationLogic(Locations.TinyCastlePotion, lambda l: l.istiny and l.CanBuy(Locations.TinyCastlePotion)),
        LocationLogic(Locations.ChunkyCastlePotion, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyCastlePotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.CrankyIsles: Region("Cranky Isles", HintRegion.IslesShops, Levels.Shops, False, None, [
        LocationLogic(Locations.SimianSlam, lambda l: l.CanBuy(Locations.SimianSlam)),
        LocationLogic(Locations.DonkeyIslesPotion, lambda l: l.isdonkey and l.CanBuy(Locations.DonkeyIslesPotion)),
        LocationLogic(Locations.DiddyIslesPotion, lambda l: l.isdiddy and l.CanBuy(Locations.DiddyIslesPotion)),
        LocationLogic(Locations.LankyIslesPotion, lambda l: l.islanky and l.CanBuy(Locations.LankyIslesPotion)),
        LocationLogic(Locations.TinyIslesPotion, lambda l: l.istiny and l.CanBuy(Locations.TinyIslesPotion)),
        LocationLogic(Locations.ChunkyIslesPotion, lambda l: l.ischunky and l.CanBuy(Locations.ChunkyIslesPotion)),
    ], [], [
        TransitionFront(Regions.CrankyGeneric, lambda _: True),
    ]),

    Regions.Snide: Region("Snide", HintRegion.Snide, Levels.Snide, False, None, [], [], [
        TransitionFront(Regions.SnideFirstGroup, lambda l: True),
        TransitionFront(Regions.SnideSecondGroup, lambda l: True),
        TransitionFront(Regions.SnideThirdGroup, lambda l: True),
        TransitionFront(Regions.SnideFourthGroup, lambda l: True),
        TransitionFront(Regions.SnideLastGroup, lambda l: True),
    ]),

    Regions.SnideFirstGroup: Region("Snide First Group", HintRegion.SnideFirstGroup, Levels.Snide, False, None, [
        LocationLogic(Locations.TurnInJungleJapesDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(1)),
        LocationLogic(Locations.TurnInJungleJapesDiddyBlueprint, lambda l: l.CanGetBlueprintReward(2)),
        LocationLogic(Locations.TurnInJungleJapesLankyBlueprint, lambda l: l.CanGetBlueprintReward(3)),
        LocationLogic(Locations.TurnInJungleJapesTinyBlueprint, lambda l: l.CanGetBlueprintReward(4)),
        LocationLogic(Locations.TurnInJungleJapesChunkyBlueprint, lambda l: l.CanGetBlueprintReward(5)),
        LocationLogic(Locations.TurnInAngryAztecDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(6)),
        LocationLogic(Locations.TurnInAngryAztecDiddyBlueprint, lambda l: l.CanGetBlueprintReward(7)),
        LocationLogic(Locations.TurnInAngryAztecLankyBlueprint, lambda l: l.CanGetBlueprintReward(8)),
    ], [], []),

    Regions.SnideSecondGroup: Region("Snide Second Group", HintRegion.SnideSecondGroup, Levels.Snide, False, None, [
        LocationLogic(Locations.TurnInAngryAztecTinyBlueprint, lambda l: l.CanGetBlueprintReward(9)),
        LocationLogic(Locations.TurnInAngryAztecChunkyBlueprint, lambda l: l.CanGetBlueprintReward(10)),
        LocationLogic(Locations.TurnInFranticFactoryDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(11)),
        LocationLogic(Locations.TurnInFranticFactoryDiddyBlueprint, lambda l: l.CanGetBlueprintReward(12)),
        LocationLogic(Locations.TurnInFranticFactoryLankyBlueprint, lambda l: l.CanGetBlueprintReward(13)),
        LocationLogic(Locations.TurnInFranticFactoryTinyBlueprint, lambda l: l.CanGetBlueprintReward(14)),
        LocationLogic(Locations.TurnInFranticFactoryChunkyBlueprint, lambda l: l.CanGetBlueprintReward(15)),
        LocationLogic(Locations.TurnInGloomyGalleonDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(16)),
    ], [], []),

    Regions.SnideThirdGroup: Region("Snide Third Group", HintRegion.SnideThirdGroup, Levels.Snide, False, None, [
        LocationLogic(Locations.TurnInGloomyGalleonDiddyBlueprint, lambda l: l.CanGetBlueprintReward(17)),
        LocationLogic(Locations.TurnInGloomyGalleonLankyBlueprint, lambda l: l.CanGetBlueprintReward(18)),
        LocationLogic(Locations.TurnInGloomyGalleonTinyBlueprint, lambda l: l.CanGetBlueprintReward(19)),
        LocationLogic(Locations.TurnInGloomyGalleonChunkyBlueprint, lambda l: l.CanGetBlueprintReward(20)),
        LocationLogic(Locations.TurnInFungiForestDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(21)),
        LocationLogic(Locations.TurnInFungiForestDiddyBlueprint, lambda l: l.CanGetBlueprintReward(22)),
        LocationLogic(Locations.TurnInFungiForestLankyBlueprint, lambda l: l.CanGetBlueprintReward(23)),
        LocationLogic(Locations.TurnInFungiForestTinyBlueprint, lambda l: l.CanGetBlueprintReward(24)),
    ], [], []),

    Regions.SnideFourthGroup: Region("Snide Fourth Group", HintRegion.SnideFourthGroup, Levels.Snide, False, None, [
        LocationLogic(Locations.TurnInFungiForestChunkyBlueprint, lambda l: l.CanGetBlueprintReward(25)),
        LocationLogic(Locations.TurnInCrystalCavesDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(26)),
        LocationLogic(Locations.TurnInCrystalCavesDiddyBlueprint, lambda l: l.CanGetBlueprintReward(27)),
        LocationLogic(Locations.TurnInCrystalCavesLankyBlueprint, lambda l: l.CanGetBlueprintReward(28)),
        LocationLogic(Locations.TurnInCrystalCavesTinyBlueprint, lambda l: l.CanGetBlueprintReward(29)),
        LocationLogic(Locations.TurnInCrystalCavesChunkyBlueprint, lambda l: l.CanGetBlueprintReward(30)),
        LocationLogic(Locations.TurnInCreepyCastleDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(31)),
        LocationLogic(Locations.TurnInCreepyCastleDiddyBlueprint, lambda l: l.CanGetBlueprintReward(32)),
    ], [], []),

    Regions.SnideLastGroup: Region("Snide Last Group", HintRegion.SnideLastGroup, Levels.Snide, False, None, [
        LocationLogic(Locations.TurnInCreepyCastleLankyBlueprint, lambda l: l.CanGetBlueprintReward(33)),
        LocationLogic(Locations.TurnInCreepyCastleTinyBlueprint, lambda l: l.CanGetBlueprintReward(34)),
        LocationLogic(Locations.TurnInCreepyCastleChunkyBlueprint, lambda l: l.CanGetBlueprintReward(35)),
        LocationLogic(Locations.TurnInDKIslesDonkeyBlueprint, lambda l: l.CanGetBlueprintReward(36)),
        LocationLogic(Locations.TurnInDKIslesDiddyBlueprint, lambda l: l.CanGetBlueprintReward(37)),
        LocationLogic(Locations.TurnInDKIslesLankyBlueprint, lambda l: l.CanGetBlueprintReward(38)),
        LocationLogic(Locations.TurnInDKIslesTinyBlueprint, lambda l: l.CanGetBlueprintReward(39)),
        LocationLogic(Locations.TurnInDKIslesChunkyBlueprint, lambda l: l.CanGetBlueprintReward(40)),
    ], [], []),
}
