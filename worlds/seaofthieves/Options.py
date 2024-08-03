import typing
from dataclasses import dataclass
from Options import PerGameCommonOptions, Range
from Options import DefaultOnToggle
from .Configurations import Foodoptions
from .Configurations.Sealoptions import *
from .Configurations.Emoptions import *
from .Configurations import Fishoptions
from .Configurations import Fortsoptions
from .Configurations import Treasuryoptions
from .Configurations import Servantoptions
from .Configurations import Guardianoptions
from .Configurations import IllFatedoptions, Cannonsoptions, Selloptions
from .Configurations import Trapsoptions
from .Configurations import EmVoyageoptions
from .Configurations import Shipoptions, Shopoptions, CaptainShipoptions, DaysAtSeaoptions, Rowboatoptions, \
    Shipwreckoptions, TallTaleoptions


class ExperimentalFeatures(Toggle):
    """Not meant for player use. Developer use only to enable WIP mechanics.
    Enabling this setting will likely brick generation and/or the client."""
    default = 0
    display_name = "Experimental Features"


class ScreenCapture(Toggle):
    """Captures screen events to aid in determining check completion"""
    default = 0
    display_name = "Allow Screen Capture"


@dataclass
class SOTOptions(PerGameCommonOptions):
    sealCount: SealsRequired
    voyageEmGh: EmVoyageoptions.VoyageCountSpecificGh
    voyageEmMa: EmVoyageoptions.VoyageCountSpecificMa
    voyageEmOos: EmVoyageoptions.VoyageCountSpecificOos
    voyageEmAf: EmVoyageoptions.VoyageCountSpecificAf
    voyageEmRoar: EmVoyageoptions.VoyageCountSpecificRoar

    servantSanity: Servantoptions.ServantSanity
    guardianSanity: Guardianoptions.GuardianSanity
    fortressSanity: Fortsoptions.FortressSanity
    illFated: IllFatedoptions.IllFated
    playerShip: Shipoptions.ShipSanity

    fishSanity: Fishoptions.FishSanity
    shopSanity: Shopoptions.ShopSanity

    cannonSanityBalls: Cannonsoptions.CannonSanityBalls
    cannonSanityCursed: Cannonsoptions.CannonSanityCursed
    cannonSanityPhantom: Cannonsoptions.CannonSanityPhantom

    foodSanityFruit: Foodoptions.MunchSanityFruit
    foodSanityFish: Foodoptions.MunchSanityFish
    foodSanitySeamonster: Foodoptions.MunchSanitySeamonster
    foodSanityLandAnimal: Foodoptions.MunchSanityLandAnimal
    foodSanityBug: Foodoptions.MunchSanityBug

    cookSanityFish: Foodoptions.CookSanityFish
    cookSanitySeamonster: Foodoptions.CookSanitySeamonster
    cookSanityLandAnimal: Foodoptions.CookSanityLandAnimal

    burnSanityFish: Foodoptions.BurnSanityFish
    burnSanitySeamonster: Foodoptions.BurnSanitySeamonster
    burnSanityLandAnimal: Foodoptions.BurnSanityLandAnimal

    captainShipSpotted: CaptainShipoptions.CaptainShipoptions
    daysAtSea: DaysAtSeaoptions.DaysAtSeaOptions
    rowboats: Rowboatoptions.RowboatSanity
    shipwrecks: Shipwreckoptions.ShipwreckOptions
    tallTales: TallTaleoptions.TallTaleoptions

    trapsPercentage: Trapsoptions.TrapPercentage
    experimentals: ExperimentalFeatures
    screenCapture: ScreenCapture
