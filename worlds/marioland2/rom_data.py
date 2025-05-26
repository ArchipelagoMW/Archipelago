from typing import NamedTuple


"""
Data relevant to miscellaneous rom addresses and values.
Can be both the vanilla rom or patch.

Not to be confused with `rom_addresses.py`, which is generated from 
the AP disassembly extracting "Archipelago" function calls.
"""

class MarioLand2RomMusicData(NamedTuple):
    address: int = 0
    track: int = 0


overworld_music_data: dict[str, MarioLand2RomMusicData] = {
    "File Select": MarioLand2RomMusicData(0x3004F, 0x0D),
    "Overworld": MarioLand2RomMusicData(0x3EA9B, 0x06),
    "Tree Zone": MarioLand2RomMusicData(0x3D186, 0x10),
    "Space Zone": MarioLand2RomMusicData(0x3D52B, 0x1C),
    "Macro Zone": MarioLand2RomMusicData(0x3D401, 0x05),
    "Pumpkin Zone": MarioLand2RomMusicData(0x3D297, 0x1E),
    "Mario Zone": MarioLand2RomMusicData(0x3D840, 0x1B),
    "Turtle Zone": MarioLand2RomMusicData(0x3D694, 0x12),
    "Castle Gates": MarioLand2RomMusicData(0x3D758, 0x0E)
}

#                                       Machine
level_music_tracks = [0x01, 0x0B, 0x11, 0x13,   0x14, 0x17, 0x1D, 0x1F, 0x28]
