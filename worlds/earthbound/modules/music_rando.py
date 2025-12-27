from ..Options import RandomizeOverworldMusic, RandomizeFanfares
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import EarthBoundWorld
    from .Rom import LocalRom

town_songs = [
    0x2E,
    0x2F,
    0x30,
    0x38,
    0x3B,
    0x3D,
    0x41,
    0x42,
    0x52,
    0x80,
    0x81,
    0x82
]

overworld_songs = [
    0x1D,
    0x2C,
    0x33,
    0x34,
    0x35,
    0x36,
    0x3E,
    0x40,
    0x43,
    0x44,
    0x6B,
    0x72,
    0x79,
    0x88,
    0x92,
    0x97,
    0x99,
    0x9A,
    0x9F
    ]

dungeon_songs = [
    0x28,
    0x29,
    0x2A,
    0x2B,
    0x2D,
    0x31,
    0x32,
    0x37,
    0x2D,
    0x3F,
    0x46,
    0x6A,
    0x6C,
    0x75,
    0x84,
    0x85
]

interior_songs = [
    0x10,
    0x11,
    0x12,
    0x13,
    0x14,
    0x15,
    0x16,
    0x17,
    0x18,
    0x19,
    0x1A,
    0x1C,
    0x39,
    0x70,
    0x78,
    0x7D,
    0x83,
    0x8C,
    0x98
    ]

cutscene_songs = [
    0x3A,
    0x3C,
    0x48,
    0x4C,
    0x4D,
    0x4E,
    0x4F,
    0x50,
    0x51,
    0x53,
    0x55,
    0x56,
    0x57,
    0x58,
    0x59,
    0x5C,
    0x77,
    0x86,
    0x90,
    0x9B,
    0xA9,
    0xAA,
    0xAB,
    0xAC,
    0xBB
]

wakeup_songs = [
    0x1B,
    0x5A,
    0xAD,
    0xB2,
    0xB5,
    0xBC,
]

rare_songs = [
    0x1E,
    0x1F,
    0x45,
    0x47,
    0x70,
    0x74,
    0x76,
    0x96,

]

non_randomized = [
    0x01,
    0x02,
    0x03,
    0x04,
    0x06,
    0x07,
    0x0A,
    0x0D,
    0x0E,
    0x20,
    0x21,
    0x22,
    0x23,
    0x24,
    0x25,
    0x26,
    0x27,
    0x4B,
    0x5D,
    0x5E,
    0x5F,
    0x73,
    0x7A,
    0x87,
    0x89,
    0x8A,
    0x8B,
    0x9D,
    0xAE,
    0xAF,
    0xB6,
    0xBE,
    0xBF
]

battle_songs = [
    0x49,
    0x4A,
    0x60,
    0x61,
    0x62,
    0x63,
    0x64,
    0x65,
    0x66,
    0x67,
    0x68,
    0x69,
    0x8D,
    0x94,
    0x95,
    0xB9,
    0xBA
]


def music_randomizer(world: "EarthBoundWorld", rom: "LocalRom") -> None:
    fanfares = [
        0x05,
        0x08,
        0x09,
        0x0B,
        0x0C,
        0x0F,
        0x54,
        0x5B,
        0x6D,
        0x6E,
        0x6F,
        0x71,
        0x7B,
        0x7C,
        0x7E,
        0x7F,
        0xB7,
        0xB8,
        0x8E,
        0x8F,
        0x91,
        0x93,
        0x9C,
        0x9E,
        0xA0,
        0xA1,
        0xA2,
        0xA3,
        0xA4,
        0xA5,
        0xA6,
        0xA7,
        0xA8,
        0xB0,
        0xB1,
        0xB3,
        0xB4,
        0xB7,
        0xB8,
        0xBD
    ]

    # Todo; options here
    global_tracklist = list(range(0xC0))  # Initialize the list; this ideally should be vanilla

    if world.options.randomize_fanfares == RandomizeFanfares.option_on_no_sound_stone_fanfares:
        for i in range(9):
            fanfares.remove(0xA0 + i)

    if world.options.randomize_fanfares:
        shuffled_fanfares = fanfares.copy()
        world.random.shuffle(shuffled_fanfares)
        for track_id, song in enumerate(fanfares):
            global_tracklist[song] = shuffled_fanfares[track_id]
    
    if world.options.randomize_battle_music:
        shuffled_battle_songs = battle_songs.copy()
        world.random.shuffle(shuffled_battle_songs)
        for track_id, song in enumerate(battle_songs):
            global_tracklist[song] = shuffled_battle_songs[track_id]

    if world.options.randomize_overworld_music == RandomizeOverworldMusic.option_match_type:
        shuffled_town_songs = town_songs.copy()
        shuffled_overworld_songs = overworld_songs.copy()
        shuffled_interior_songs = interior_songs.copy()
        shuffled_dungeon_songs = dungeon_songs.copy()
        shuffled_cutscene_songs = cutscene_songs.copy()
        shuffled_rare_songs = rare_songs.copy()
        shuffled_wakeup_songs = wakeup_songs.copy()

        world.random.shuffle(shuffled_town_songs)
        world.random.shuffle(shuffled_overworld_songs)
        world.random.shuffle(shuffled_interior_songs)
        world.random.shuffle(shuffled_dungeon_songs)
        world.random.shuffle(shuffled_cutscene_songs)
        world.random.shuffle(shuffled_rare_songs)
        world.random.shuffle(shuffled_wakeup_songs)

        for track_id, song in enumerate(town_songs):
            global_tracklist[song] = shuffled_town_songs[track_id]

        for track_id, song in enumerate(overworld_songs):
            global_tracklist[song] = shuffled_overworld_songs[track_id]

        for track_id, song in enumerate(interior_songs):
            global_tracklist[song] = shuffled_interior_songs[track_id]

        for track_id, song in enumerate(dungeon_songs):
            global_tracklist[song] = shuffled_dungeon_songs[track_id]

        for track_id, song in enumerate(cutscene_songs):
            global_tracklist[song] = shuffled_cutscene_songs[track_id]

        for track_id, song in enumerate(rare_songs):
            global_tracklist[song] = shuffled_rare_songs[track_id]

        for track_id, song in enumerate(wakeup_songs):
            global_tracklist[song] = shuffled_wakeup_songs[track_id]

    elif world.options.randomize_overworld_music == RandomizeOverworldMusic.option_full:
        all_overworld_songs = (town_songs + overworld_songs + interior_songs +
                               dungeon_songs + cutscene_songs + rare_songs + wakeup_songs)

        shuffled_overworld_songs = all_overworld_songs.copy()
        world.random.shuffle(shuffled_overworld_songs)

        for track_id, song in enumerate(all_overworld_songs):
            global_tracklist[song] = shuffled_overworld_songs[track_id]

    rom.write_bytes(0x17FDA0, bytearray(global_tracklist))


# Should the Melodies be fanfares?
