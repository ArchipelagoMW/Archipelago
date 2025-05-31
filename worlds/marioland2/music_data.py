from typing import NamedTuple

class MarioLand2MusicData(NamedTuple):
    address: int = 0
    track: int = 0


overworld_music_data: dict[str, MarioLand2MusicData] = {
    "File Select": MarioLand2MusicData(0x3004F, 0x0D),
    "Overworld": MarioLand2MusicData(0x3EA9B, 0x06),
    "Tree Zone": MarioLand2MusicData(0x3D186, 0x10),
    "Space Zone": MarioLand2MusicData(0x3D52B, 0x1C),
    "Macro Zone": MarioLand2MusicData(0x3D401, 0x05),
    "Pumpkin Zone": MarioLand2MusicData(0x3D297, 0x1E),
    "Mario Zone": MarioLand2MusicData(0x3D840, 0x1B),
    "Turtle Zone": MarioLand2MusicData(0x3D694, 0x12),
    "Castle Gates": MarioLand2MusicData(0x3D758, 0x0E)
}

level_music_tracks: dict[str, int] = {
    "Athletic": 0x01,
    "Castle": 0x0B,
    "Graveyard": 0x11,
    "Moon": 0x13,
    "Treetop": 0x14,
    "Seashore": 0x17,
    "Star Maze": 0x1D,
    "Haunted House": 0x1F,
    "Machine": 0x28
}
