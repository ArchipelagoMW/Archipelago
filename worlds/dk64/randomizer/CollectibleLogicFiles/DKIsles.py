# fmt: off
"""Collectible logic file for DK Isles."""

from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Collectible

LogicRegions = {
    Regions.TrainingGrounds: [
        Collectible(Collectibles.coin, Kongs.donkey, lambda _: True, None, 3),  # Cave
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # Cave
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.can_use_vines and l.shockwave, None, ),  # Banana hoard

    ],
    Regions.IslesMain: [
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # Below Caves lobby
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave and l.jetpack, None, ),  # On Aztec lobby
    ],
    Regions.Prison: [
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # K. Lumsy

    ],
    Regions.BananaFairyRoom: [

    ],
    Regions.JungleJapesLobby: [

    ],
    Regions.AngryAztecLobby: [

    ],
    Regions.KremIsle: [

    ],
    Regions.KremIsleBeyondLift: [

    ],
    Regions.KremIsleTopLevel: [

    ],
    Regions.IslesSnideRoom: [

    ],
    Regions.FranticFactoryLobby: [

    ],
    Regions.GloomyGalleonLobby: [

    ],
    Regions.GloomyGalleonLobbyEntrance: [

    ],
    Regions.CabinIsle: [
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave, None, ),  # In front of fungi lobby

    ],
    Regions.FungiForestLobby: [

    ],
    Regions.CrystalCavesLobby: [

    ],
    Regions.CreepyCastleLobby: [
        # Collectible(Collectibles.coin, Kongs.any, lambda l: l.shockwave and ((l.balloon and l.islanky) or l.CanMoonkick()), None, ),  # In Castle lobby

    ],
    Regions.HideoutHelmLobby: [

    ],
    Regions.HideoutHelmLobbyPastVines: [

    ],
    Regions.Treehouse: [

    ],
    Regions.IslesMainUpper: [

    ],
    Regions.IslesHill: [

    ],
    Regions.OuterIsles: [

    ],
    Regions.AztecLobbyRoof: [

    ],
    Regions.IslesAboveWaterfall: [

    ],
    Regions.IslesAirspace: [

    ],
}
