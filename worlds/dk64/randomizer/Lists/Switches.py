"""Stores data for each of the game's switches."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType


class SwitchInfo:
    """Store information regarding a switch."""

    def __init__(
        self,
        name: str,
        kong: Kongs,
        switch_type: SwitchType,
        rom_offset: int,
        map_id: int,
        ids: list,
        tied_settings: list = [],
    ):
        """Initialize with given parameters."""
        self.name = name
        self.kong = kong
        self.switch_type = switch_type
        self.rom_offset = rom_offset
        self.map_id = map_id
        self.ids = ids
        self.tied_settings = tied_settings


SwitchData = {
    Switches.IslesMonkeyport: SwitchInfo("Isles Monkeyport Pad", Kongs.tiny, SwitchType.PadMove, 0x1C6, Maps.Isles, [0x38]),
    Switches.IslesHelmLobbyGone: SwitchInfo("Helm Lobby Gone Pad", Kongs.chunky, SwitchType.PadMove, 0x1C7, Maps.HideoutHelmLobby, [3]),
    Switches.IslesAztecLobbyFeather: SwitchInfo("Aztec Lobby Feather Switch", Kongs.tiny, SwitchType.GunSwitch, 0x1C8, Maps.AngryAztecLobby, [16]),
    Switches.IslesFungiLobbyFeather: SwitchInfo("Forest Lobby Feather Switch", Kongs.tiny, SwitchType.GunSwitch, 0x1C9, Maps.FungiForestLobby, [5]),
    Switches.IslesSpawnRocketbarrel: SwitchInfo("Isles Main Trombone Pad", Kongs.lanky, SwitchType.InstrumentPad, 0x1CA, Maps.Isles, [0x31]),
    Switches.JapesFeather: SwitchInfo("Japes Hive Area Switches", Kongs.tiny, SwitchType.GunSwitch, 0x1CB, Maps.JungleJapes, [0x34, 0x35]),
    Switches.JapesRambi: SwitchInfo("Japes Switch to Rambi", Kongs.donkey, SwitchType.GunSwitch, 0x1CC, Maps.JungleJapes, [0x123]),
    Switches.JapesPainting: SwitchInfo("Japes Switch to Painting", Kongs.diddy, SwitchType.GunSwitch, 0x1CD, Maps.JungleJapes, [40]),
    Switches.JapesDiddyCave: SwitchInfo("Japes Diddy Cave Switches", Kongs.diddy, SwitchType.GunSwitch, 0x1CE, Maps.JungleJapes, [0x29, 0x2A]),
    Switches.AztecBlueprintDoor: SwitchInfo("Aztec Blueprint Door Switches", Kongs.donkey, SwitchType.GunSwitch, 0x1CF, Maps.AngryAztec, [0x9D, 0x9E]),
    Switches.AztecLlamaCoconut: SwitchInfo("Aztec Llama Switch (1)", Kongs.donkey, SwitchType.GunSwitch, 0x1D0, Maps.AngryAztec, [13]),
    Switches.AztecLlamaGrape: SwitchInfo(
        "Aztec Llama Switch (2)",
        Kongs.lanky,
        SwitchType.GunSwitch,
        0x1D1,
        Maps.AngryAztec,
        [14],
        [Switches.AztecLlamaCoconut],
    ),
    Switches.AztecLlamaFeather: SwitchInfo(
        "Aztec Llama Switch (3)",
        Kongs.tiny,
        SwitchType.GunSwitch,
        0x1D2,
        Maps.AngryAztec,
        [15],
        [Switches.AztecLlamaCoconut, Switches.AztecLlamaGrape],
    ),
    Switches.AztecQuicksandSwitch: SwitchInfo("Aztec Quicksand Tunnel Switch", Kongs.donkey, SwitchType.SlamSwitch, 0x1D3, Maps.AztecLlamaTemple, [0x69]),
    Switches.AztecGuitar: SwitchInfo("Aztec Guitar Pad", Kongs.diddy, SwitchType.InstrumentPad, 0x1D4, Maps.AngryAztec, [0x44]),
    Switches.GalleonLighthouse: SwitchInfo("Galleon Lighthouse Switches", Kongs.donkey, SwitchType.GunSwitch, 0x1D5, Maps.GloomyGalleon, [0xA, 0xB]),
    Switches.GalleonShipwreck: SwitchInfo("Galleon Shipwreck Switches", Kongs.diddy, SwitchType.GunSwitch, 0x1D6, Maps.GloomyGalleon, [8, 9]),
    Switches.GalleonCannonGame: SwitchInfo("Galleon Cannon Game Switches", Kongs.chunky, SwitchType.GunSwitch, 0x1D7, Maps.GloomyGalleon, [6, 7]),
    Switches.FungiYellow: SwitchInfo("Forest Yellow Tunnel Switch", Kongs.lanky, SwitchType.GunSwitch, 0x1D8, Maps.FungiForest, [30]),
    Switches.FungiGreenFeather: SwitchInfo("Forest Green Tunnel Switches (1)", Kongs.tiny, SwitchType.GunSwitch, 0x1D9, Maps.FungiForest, [0x18, 0x19]),
    Switches.FungiGreenPineapple: SwitchInfo(
        "Forest Green Tunnel Switches (2)",
        Kongs.chunky,
        SwitchType.GunSwitch,
        0x1DA,
        Maps.FungiForest,
        [0x1A, 0x1B],
        [Switches.FungiGreenFeather],
    ),
}

SwitchNameDict = {
    Kongs.donkey: {
        SwitchType.GunSwitch: "Coconut Shooter (Donkey)",
        SwitchType.InstrumentPad: "Bongo Blast (Donkey)",
        SwitchType.MiscActivator: "Gorilla Grab (Donkey)",
        SwitchType.PadMove: "Barrel Blast (Donkey)",
        SwitchType.SlamSwitch: "Donkey",
    },
    Kongs.diddy: {
        SwitchType.GunSwitch: "Peanut Popgun (Diddy)",
        SwitchType.InstrumentPad: "Guitar Gazump (Diddy)",
        SwitchType.MiscActivator: "Chimpy Charge (Diddy)",
        SwitchType.PadMove: "Simian Spring (Diddy)",
        SwitchType.SlamSwitch: "Diddy",
    },
    Kongs.lanky: {
        SwitchType.GunSwitch: "Grape Shooter (Lanky)",
        SwitchType.InstrumentPad: "Trombone Tremor (Lanky)",
        SwitchType.PadMove: "Baboon Balloon (Lanky)",
        SwitchType.SlamSwitch: "Lanky",
    },
    Kongs.tiny: {
        SwitchType.GunSwitch: "Feather Bow (Tiny)",
        SwitchType.InstrumentPad: "Saxophone Slam (Tiny)",
        SwitchType.PadMove: "Monkeyport (Tiny)",
        SwitchType.SlamSwitch: "Tiny",
    },
    Kongs.chunky: {
        SwitchType.GunSwitch: "Pineapple Launcher (Chunky)",
        SwitchType.InstrumentPad: "Triangle Trample (Chunky)",
        SwitchType.PadMove: "Gorilla Gone (Chunky)",
        SwitchType.SlamSwitch: "Chunky",
    },
}


def GetSwitchName(switchType: SwitchType, kong: Kongs) -> str:
    """Derive a readable name for a Kong/switch type combination."""
    if kong in SwitchNameDict and switchType in SwitchNameDict[kong]:
        return SwitchNameDict[kong][switchType]
    return None
