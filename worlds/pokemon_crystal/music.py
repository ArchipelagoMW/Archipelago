from typing import TYPE_CHECKING

from .data import data

if TYPE_CHECKING:
    from . import PokemonCrystalWorld

EXCLUDED_MUSIC = ["MUSIC_NONE", "MUSIC_LAKE_OF_RAGE_ROCKET_RADIO", "MUSIC_PRINTER", "MUSIC_RUINS_OF_ALPH_RADIO"]


def randomize_music(world: "PokemonCrystalWorld"):
    music_pool_loop = [music_name for music_name, music_data in data.music.consts.items() if
                       music_name not in EXCLUDED_MUSIC and music_data.loop]
    music_pool_no_loop = [music_name for music_name, music_data in data.music.consts.items() if
                          music_name not in EXCLUDED_MUSIC and not music_data.loop]

    for map_name in world.generated_music.maps.keys():
        world.generated_music.maps[map_name] = world.random.choice(music_pool_loop)

    for i, _encounter in enumerate(world.generated_music.encounters):
        world.generated_music.encounters[i] = world.random.choice(music_pool_loop)

    for script_name, script_music in world.generated_music.scripts.items():
        if data.music.consts[script_music].loop:
            new_music = world.random.choice(music_pool_loop)
        else:
            new_music = world.random.choice(music_pool_no_loop)
        world.generated_music.scripts[script_name] = new_music
