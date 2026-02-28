"""Plandomizer enums and associated maps."""

from enum import IntEnum, auto

from randomizer.Enums.Items import Items


class PlandoItems(IntEnum):
    """Enum of items that are selectable in the plandomizer."""

    # Indicates that the given slot should be randomized.
    # Used when the user has not chosen anything.
    Randomize = -1

    NoItem = 0

    Donkey = auto()
    Diddy = auto()
    Lanky = auto()
    Tiny = auto()
    Chunky = auto()

    Vines = auto()
    Swim = auto()
    Oranges = auto()
    Barrels = auto()
    Climbing = auto()

    ProgressiveSlam = auto()

    # Progressive potions are not used.
    BaboonBlast = auto()
    StrongKong = auto()
    GorillaGrab = auto()

    ChimpyCharge = auto()
    RocketbarrelBoost = auto()
    SimianSpring = auto()

    Orangstand = auto()
    BaboonBalloon = auto()
    OrangstandSprint = auto()

    MiniMonkey = auto()
    PonyTailTwirl = auto()
    Monkeyport = auto()

    HunkyChunky = auto()
    PrimatePunch = auto()
    GorillaGone = auto()

    Coconut = auto()
    Peanut = auto()
    Grape = auto()
    Feather = auto()
    Pineapple = auto()
    HomingAmmo = auto()
    SniperSight = auto()
    ProgressiveAmmoBelt = auto()

    Bongos = auto()
    Guitar = auto()
    Trombone = auto()
    Saxophone = auto()
    Triangle = auto()
    ProgressiveInstrumentUpgrade = auto()

    Camera = auto()
    Shockwave = auto()
    # CameraAndShockwave is not used.

    NintendoCoin = auto()
    RarewareCoin = auto()

    JungleJapesKey = auto()
    AngryAztecKey = auto()
    FranticFactoryKey = auto()
    GloomyGalleonKey = auto()
    FungiForestKey = auto()
    CrystalCavesKey = auto()
    CreepyCastleKey = auto()
    HideoutHelmKey = auto()

    GoldenBanana = auto()
    BananaFairy = auto()
    BananaMedal = auto()
    BattleCrown = auto()

    Bean = auto()
    Pearl = auto()
    RainbowCoin = auto()
    FakeItem = auto()
    CrateItem = auto()
    BoulderItem = auto()
    EnemyItem = auto()
    HalfMedal = auto()

    # A generic junk item to represent all specific junk items.
    JunkItem = auto()

    # BananaHoard is not used.

    Cranky = auto()
    Funky = auto()
    Candy = auto()
    Snide = auto()

    # Five generic blueprint items to represent all specific blueprints.
    DonkeyBlueprint = auto()
    DiddyBlueprint = auto()
    LankyBlueprint = auto()
    TinyBlueprint = auto()
    ChunkyBlueprint = auto()

    # Hints are individually placed as plando items.
    JapesDonkeyHint = auto()
    JapesDiddyHint = auto()
    JapesLankyHint = auto()
    JapesTinyHint = auto()
    JapesChunkyHint = auto()
    AztecDonkeyHint = auto()
    AztecDiddyHint = auto()
    AztecLankyHint = auto()
    AztecTinyHint = auto()
    AztecChunkyHint = auto()
    FactoryDonkeyHint = auto()
    FactoryDiddyHint = auto()
    FactoryLankyHint = auto()
    FactoryTinyHint = auto()
    FactoryChunkyHint = auto()
    GalleonDonkeyHint = auto()
    GalleonDiddyHint = auto()
    GalleonLankyHint = auto()
    GalleonTinyHint = auto()
    GalleonChunkyHint = auto()
    ForestDonkeyHint = auto()
    ForestDiddyHint = auto()
    ForestLankyHint = auto()
    ForestTinyHint = auto()
    ForestChunkyHint = auto()
    CavesDonkeyHint = auto()
    CavesDiddyHint = auto()
    CavesLankyHint = auto()
    CavesTinyHint = auto()
    CavesChunkyHint = auto()
    CastleDonkeyHint = auto()
    CastleDiddyHint = auto()
    CastleLankyHint = auto()
    CastleTinyHint = auto()
    CastleChunkyHint = auto()


ItemToPlandoItemMap = {
    Items.NoItem: PlandoItems.NoItem,
    Items.Donkey: PlandoItems.Donkey,
    Items.Diddy: PlandoItems.Diddy,
    Items.Lanky: PlandoItems.Lanky,
    Items.Tiny: PlandoItems.Tiny,
    Items.Chunky: PlandoItems.Chunky,
    Items.Vines: PlandoItems.Vines,
    Items.Swim: PlandoItems.Swim,
    Items.Oranges: PlandoItems.Oranges,
    Items.Barrels: PlandoItems.Barrels,
    Items.Climbing: PlandoItems.Climbing,
    Items.ProgressiveSlam: PlandoItems.ProgressiveSlam,
    Items.ProgressiveSlam2: PlandoItems.ProgressiveSlam,
    Items.ProgressiveSlam3: PlandoItems.ProgressiveSlam,
    Items.BaboonBlast: PlandoItems.BaboonBlast,
    Items.StrongKong: PlandoItems.StrongKong,
    Items.GorillaGrab: PlandoItems.GorillaGrab,
    Items.ChimpyCharge: PlandoItems.ChimpyCharge,
    Items.RocketbarrelBoost: PlandoItems.RocketbarrelBoost,
    Items.SimianSpring: PlandoItems.SimianSpring,
    Items.Orangstand: PlandoItems.Orangstand,
    Items.BaboonBalloon: PlandoItems.BaboonBalloon,
    Items.OrangstandSprint: PlandoItems.OrangstandSprint,
    Items.MiniMonkey: PlandoItems.MiniMonkey,
    Items.PonyTailTwirl: PlandoItems.PonyTailTwirl,
    Items.Monkeyport: PlandoItems.Monkeyport,
    Items.HunkyChunky: PlandoItems.HunkyChunky,
    Items.PrimatePunch: PlandoItems.PrimatePunch,
    Items.GorillaGone: PlandoItems.GorillaGone,
    Items.Coconut: PlandoItems.Coconut,
    Items.Peanut: PlandoItems.Peanut,
    Items.Grape: PlandoItems.Grape,
    Items.Feather: PlandoItems.Feather,
    Items.Pineapple: PlandoItems.Pineapple,
    Items.HomingAmmo: PlandoItems.HomingAmmo,
    Items.SniperSight: PlandoItems.SniperSight,
    Items.ProgressiveAmmoBelt: PlandoItems.ProgressiveAmmoBelt,
    Items.ProgressiveAmmoBelt2: PlandoItems.ProgressiveAmmoBelt,
    Items.Bongos: PlandoItems.Bongos,
    Items.Guitar: PlandoItems.Guitar,
    Items.Trombone: PlandoItems.Trombone,
    Items.Saxophone: PlandoItems.Saxophone,
    Items.Triangle: PlandoItems.Triangle,
    Items.ProgressiveInstrumentUpgrade: PlandoItems.ProgressiveInstrumentUpgrade,
    Items.ProgressiveInstrumentUpgrade2: PlandoItems.ProgressiveInstrumentUpgrade,
    Items.ProgressiveInstrumentUpgrade3: PlandoItems.ProgressiveInstrumentUpgrade,
    Items.Camera: PlandoItems.Camera,
    Items.Shockwave: PlandoItems.Shockwave,
    Items.NintendoCoin: PlandoItems.NintendoCoin,
    Items.RarewareCoin: PlandoItems.RarewareCoin,
    Items.JungleJapesKey: PlandoItems.JungleJapesKey,
    Items.AngryAztecKey: PlandoItems.AngryAztecKey,
    Items.FranticFactoryKey: PlandoItems.FranticFactoryKey,
    Items.GloomyGalleonKey: PlandoItems.GloomyGalleonKey,
    Items.FungiForestKey: PlandoItems.FungiForestKey,
    Items.CrystalCavesKey: PlandoItems.CrystalCavesKey,
    Items.CreepyCastleKey: PlandoItems.CreepyCastleKey,
    Items.HideoutHelmKey: PlandoItems.HideoutHelmKey,
    Items.GoldenBanana: PlandoItems.GoldenBanana,
    Items.BananaFairy: PlandoItems.BananaFairy,
    Items.BananaMedal: PlandoItems.BananaMedal,
    Items.BattleCrown: PlandoItems.BattleCrown,
    Items.Bean: PlandoItems.Bean,
    Items.Pearl: PlandoItems.Pearl,
    Items.RainbowCoin: PlandoItems.RainbowCoin,
    Items.IceTrapBubble: PlandoItems.FakeItem,
    # All of the individual junk items map to the same plando item.
    Items.JunkCrystal: PlandoItems.JunkItem,
    Items.JunkMelon: PlandoItems.JunkItem,
    Items.JunkAmmo: PlandoItems.JunkItem,
    Items.JunkFilm: PlandoItems.JunkItem,
    Items.JunkOrange: PlandoItems.JunkItem,
    Items.Cranky: PlandoItems.Cranky,
    Items.Funky: PlandoItems.Funky,
    Items.Candy: PlandoItems.Candy,
    Items.Snide: PlandoItems.Snide,
    # All of the individual blueprints map to the same five plando items.
    Items.JungleJapesDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.JungleJapesDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.JungleJapesLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.JungleJapesTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.JungleJapesChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.AngryAztecDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.AngryAztecDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.AngryAztecLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.AngryAztecTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.AngryAztecChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.FranticFactoryDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.FranticFactoryDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.FranticFactoryLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.FranticFactoryTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.FranticFactoryChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.GloomyGalleonDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.GloomyGalleonDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.GloomyGalleonLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.GloomyGalleonTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.GloomyGalleonChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.FungiForestDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.FungiForestDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.FungiForestLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.FungiForestTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.FungiForestChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.CrystalCavesDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.CrystalCavesDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.CrystalCavesLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.CrystalCavesTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.CrystalCavesChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.CreepyCastleDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.CreepyCastleDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.CreepyCastleLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.CreepyCastleTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.CreepyCastleChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.DKIslesDonkeyBlueprint: PlandoItems.DonkeyBlueprint,
    Items.DKIslesDiddyBlueprint: PlandoItems.DiddyBlueprint,
    Items.DKIslesLankyBlueprint: PlandoItems.LankyBlueprint,
    Items.DKIslesTinyBlueprint: PlandoItems.TinyBlueprint,
    Items.DKIslesChunkyBlueprint: PlandoItems.ChunkyBlueprint,
    Items.JapesDonkeyHint: PlandoItems.JapesDonkeyHint,
    Items.JapesDiddyHint: PlandoItems.JapesDiddyHint,
    Items.JapesLankyHint: PlandoItems.JapesLankyHint,
    Items.JapesTinyHint: PlandoItems.JapesTinyHint,
    Items.JapesChunkyHint: PlandoItems.JapesChunkyHint,
    Items.AztecDonkeyHint: PlandoItems.AztecDonkeyHint,
    Items.AztecDiddyHint: PlandoItems.AztecDiddyHint,
    Items.AztecLankyHint: PlandoItems.AztecLankyHint,
    Items.AztecTinyHint: PlandoItems.AztecTinyHint,
    Items.AztecChunkyHint: PlandoItems.AztecChunkyHint,
    Items.FactoryDonkeyHint: PlandoItems.FactoryDonkeyHint,
    Items.FactoryDiddyHint: PlandoItems.FactoryDiddyHint,
    Items.FactoryLankyHint: PlandoItems.FactoryLankyHint,
    Items.FactoryTinyHint: PlandoItems.FactoryTinyHint,
    Items.FactoryChunkyHint: PlandoItems.FactoryChunkyHint,
    Items.GalleonDonkeyHint: PlandoItems.GalleonDonkeyHint,
    Items.GalleonDiddyHint: PlandoItems.GalleonDiddyHint,
    Items.GalleonLankyHint: PlandoItems.GalleonLankyHint,
    Items.GalleonTinyHint: PlandoItems.GalleonTinyHint,
    Items.GalleonChunkyHint: PlandoItems.GalleonChunkyHint,
    Items.ForestDonkeyHint: PlandoItems.ForestDonkeyHint,
    Items.ForestDiddyHint: PlandoItems.ForestDiddyHint,
    Items.ForestLankyHint: PlandoItems.ForestLankyHint,
    Items.ForestTinyHint: PlandoItems.ForestTinyHint,
    Items.ForestChunkyHint: PlandoItems.ForestChunkyHint,
    Items.CavesDonkeyHint: PlandoItems.CavesDonkeyHint,
    Items.CavesDiddyHint: PlandoItems.CavesDiddyHint,
    Items.CavesLankyHint: PlandoItems.CavesLankyHint,
    Items.CavesTinyHint: PlandoItems.CavesTinyHint,
    Items.CavesChunkyHint: PlandoItems.CavesChunkyHint,
    Items.CastleDonkeyHint: PlandoItems.CastleDonkeyHint,
    Items.CastleDiddyHint: PlandoItems.CastleDiddyHint,
    Items.CastleLankyHint: PlandoItems.CastleLankyHint,
    Items.CastleTinyHint: PlandoItems.CastleTinyHint,
    Items.CastleChunkyHint: PlandoItems.CastleChunkyHint,
}

PlandoItemToItemMap = {
    PlandoItems.NoItem: Items.NoItem,
    PlandoItems.Donkey: Items.Donkey,
    PlandoItems.Diddy: Items.Diddy,
    PlandoItems.Lanky: Items.Lanky,
    PlandoItems.Tiny: Items.Tiny,
    PlandoItems.Chunky: Items.Chunky,
    PlandoItems.Vines: Items.Vines,
    PlandoItems.Swim: Items.Swim,
    PlandoItems.Oranges: Items.Oranges,
    PlandoItems.Barrels: Items.Barrels,
    PlandoItems.Climbing: Items.Climbing,
    PlandoItems.BaboonBlast: Items.BaboonBlast,
    PlandoItems.StrongKong: Items.StrongKong,
    PlandoItems.GorillaGrab: Items.GorillaGrab,
    PlandoItems.ChimpyCharge: Items.ChimpyCharge,
    PlandoItems.RocketbarrelBoost: Items.RocketbarrelBoost,
    PlandoItems.SimianSpring: Items.SimianSpring,
    PlandoItems.Orangstand: Items.Orangstand,
    PlandoItems.BaboonBalloon: Items.BaboonBalloon,
    PlandoItems.OrangstandSprint: Items.OrangstandSprint,
    PlandoItems.MiniMonkey: Items.MiniMonkey,
    PlandoItems.PonyTailTwirl: Items.PonyTailTwirl,
    PlandoItems.Monkeyport: Items.Monkeyport,
    PlandoItems.HunkyChunky: Items.HunkyChunky,
    PlandoItems.PrimatePunch: Items.PrimatePunch,
    PlandoItems.GorillaGone: Items.GorillaGone,
    PlandoItems.Coconut: Items.Coconut,
    PlandoItems.Peanut: Items.Peanut,
    PlandoItems.Grape: Items.Grape,
    PlandoItems.Feather: Items.Feather,
    PlandoItems.Pineapple: Items.Pineapple,
    PlandoItems.HomingAmmo: Items.HomingAmmo,
    PlandoItems.SniperSight: Items.SniperSight,
    PlandoItems.Bongos: Items.Bongos,
    PlandoItems.Guitar: Items.Guitar,
    PlandoItems.Trombone: Items.Trombone,
    PlandoItems.Saxophone: Items.Saxophone,
    PlandoItems.Triangle: Items.Triangle,
    PlandoItems.Camera: Items.Camera,
    PlandoItems.Shockwave: Items.Shockwave,
    PlandoItems.NintendoCoin: Items.NintendoCoin,
    PlandoItems.RarewareCoin: Items.RarewareCoin,
    PlandoItems.JungleJapesKey: Items.JungleJapesKey,
    PlandoItems.AngryAztecKey: Items.AngryAztecKey,
    PlandoItems.FranticFactoryKey: Items.FranticFactoryKey,
    PlandoItems.GloomyGalleonKey: Items.GloomyGalleonKey,
    PlandoItems.FungiForestKey: Items.FungiForestKey,
    PlandoItems.CrystalCavesKey: Items.CrystalCavesKey,
    PlandoItems.CreepyCastleKey: Items.CreepyCastleKey,
    PlandoItems.HideoutHelmKey: Items.HideoutHelmKey,
    PlandoItems.GoldenBanana: Items.GoldenBanana,
    PlandoItems.BananaFairy: Items.BananaFairy,
    PlandoItems.BananaMedal: Items.BananaMedal,
    PlandoItems.BattleCrown: Items.BattleCrown,
    PlandoItems.Bean: Items.Bean,
    PlandoItems.Pearl: Items.Pearl,
    PlandoItems.RainbowCoin: Items.RainbowCoin,
    PlandoItems.FakeItem: Items.IceTrapBubble,
    PlandoItems.ProgressiveSlam: Items.ProgressiveSlam,
    PlandoItems.ProgressiveAmmoBelt: Items.ProgressiveAmmoBelt,
    PlandoItems.ProgressiveInstrumentUpgrade: Items.ProgressiveInstrumentUpgrade,
    PlandoItems.Cranky: Items.Cranky,
    PlandoItems.Funky: Items.Funky,
    PlandoItems.Candy: Items.Candy,
    PlandoItems.Snide: Items.Snide,
    PlandoItems.JapesDonkeyHint: Items.JapesDonkeyHint,
    PlandoItems.JapesDiddyHint: Items.JapesDiddyHint,
    PlandoItems.JapesLankyHint: Items.JapesLankyHint,
    PlandoItems.JapesTinyHint: Items.JapesTinyHint,
    PlandoItems.JapesChunkyHint: Items.JapesChunkyHint,
    PlandoItems.AztecDonkeyHint: Items.AztecDonkeyHint,
    PlandoItems.AztecDiddyHint: Items.AztecDiddyHint,
    PlandoItems.AztecLankyHint: Items.AztecLankyHint,
    PlandoItems.AztecTinyHint: Items.AztecTinyHint,
    PlandoItems.AztecChunkyHint: Items.AztecChunkyHint,
    PlandoItems.FactoryDonkeyHint: Items.FactoryDonkeyHint,
    PlandoItems.FactoryDiddyHint: Items.FactoryDiddyHint,
    PlandoItems.FactoryLankyHint: Items.FactoryLankyHint,
    PlandoItems.FactoryTinyHint: Items.FactoryTinyHint,
    PlandoItems.FactoryChunkyHint: Items.FactoryChunkyHint,
    PlandoItems.GalleonDonkeyHint: Items.GalleonDonkeyHint,
    PlandoItems.GalleonDiddyHint: Items.GalleonDiddyHint,
    PlandoItems.GalleonLankyHint: Items.GalleonLankyHint,
    PlandoItems.GalleonTinyHint: Items.GalleonTinyHint,
    PlandoItems.GalleonChunkyHint: Items.GalleonChunkyHint,
    PlandoItems.ForestDonkeyHint: Items.ForestDonkeyHint,
    PlandoItems.ForestDiddyHint: Items.ForestDiddyHint,
    PlandoItems.ForestLankyHint: Items.ForestLankyHint,
    PlandoItems.ForestTinyHint: Items.ForestTinyHint,
    PlandoItems.ForestChunkyHint: Items.ForestChunkyHint,
    PlandoItems.CavesDonkeyHint: Items.CavesDonkeyHint,
    PlandoItems.CavesDiddyHint: Items.CavesDiddyHint,
    PlandoItems.CavesLankyHint: Items.CavesLankyHint,
    PlandoItems.CavesTinyHint: Items.CavesTinyHint,
    PlandoItems.CavesChunkyHint: Items.CavesChunkyHint,
    PlandoItems.CastleDonkeyHint: Items.CastleDonkeyHint,
    PlandoItems.CastleDiddyHint: Items.CastleDiddyHint,
    PlandoItems.CastleLankyHint: Items.CastleLankyHint,
    PlandoItems.CastleTinyHint: Items.CastleTinyHint,
    PlandoItems.CastleChunkyHint: Items.CastleChunkyHint,
}

PlandoItemToItemListMap = {
    PlandoItems.JunkItem: [Items.JunkMelon],  # More junk items someday [Items.JunkCrystal, Items.JunkMelon, Items.JunkAmmo, Items.JunkFilm, Items.JunkOrange],
    PlandoItems.DonkeyBlueprint: [
        Items.DonkeyBlueprint,
        # Items.JungleJapesDonkeyBlueprint,
        # Items.AngryAztecDonkeyBlueprint,
        # Items.FranticFactoryDonkeyBlueprint,
        # Items.GloomyGalleonDonkeyBlueprint,
        # Items.FungiForestDonkeyBlueprint,
        # Items.CrystalCavesDonkeyBlueprint,
        # Items.CreepyCastleDonkeyBlueprint,
        # Items.DKIslesDonkeyBlueprint,
    ],
    PlandoItems.DiddyBlueprint: [
        Items.DiddyBlueprint,
        # Items.JungleJapesDiddyBlueprint,
        # Items.AngryAztecDiddyBlueprint,
        # Items.FranticFactoryDiddyBlueprint,
        # Items.GloomyGalleonDiddyBlueprint,
        # Items.FungiForestDiddyBlueprint,
        # Items.CrystalCavesDiddyBlueprint,
        # Items.CreepyCastleDiddyBlueprint,
        # Items.DKIslesDiddyBlueprint,
    ],
    PlandoItems.LankyBlueprint: [
        Items.LankyBlueprint,
        # Items.JungleJapesLankyBlueprint,
        # Items.AngryAztecLankyBlueprint,
        # Items.FranticFactoryLankyBlueprint,
        # Items.GloomyGalleonLankyBlueprint,
        # Items.FungiForestLankyBlueprint,
        # Items.CrystalCavesLankyBlueprint,
        # Items.CreepyCastleLankyBlueprint,
        # Items.DKIslesLankyBlueprint,
    ],
    PlandoItems.TinyBlueprint: [
        Items.TinyBlueprint,
        # Items.JungleJapesTinyBlueprint,
        # Items.AngryAztecTinyBlueprint,
        # Items.FranticFactoryTinyBlueprint,
        # Items.GloomyGalleonTinyBlueprint,
        # Items.FungiForestTinyBlueprint,
        # Items.CrystalCavesTinyBlueprint,
        # Items.CreepyCastleTinyBlueprint,
        # Items.DKIslesTinyBlueprint,
    ],
    PlandoItems.ChunkyBlueprint: [
        Items.ChunkyBlueprint,
        # Items.JungleJapesChunkyBlueprint,
        # Items.AngryAztecChunkyBlueprint,
        # Items.FranticFactoryChunkyBlueprint,
        # Items.GloomyGalleonChunkyBlueprint,
        # Items.FungiForestChunkyBlueprint,
        # Items.CrystalCavesChunkyBlueprint,
        # Items.CreepyCastleChunkyBlueprint,
        # Items.DKIslesChunkyBlueprint,
    ],
}


def GetItemsFromPlandoItem(plandoItemEnum: PlandoItems) -> list[Items]:
    """Get items from the plando enum."""
    if plandoItemEnum in PlandoItemToItemMap:
        return [PlandoItemToItemMap[plandoItemEnum]]
    if plandoItemEnum in PlandoItemToItemListMap:
        return PlandoItemToItemListMap[plandoItemEnum]
    return None
