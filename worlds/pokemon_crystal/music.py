from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data
from .options import RandomizeMusic

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

EXCLUDED_MUSIC = ["MUSIC_NONE", "MUSIC_LAKE_OF_RAGE_ROCKET_RADIO", "MUSIC_PRINTER", "MUSIC_RUINS_OF_ALPH_RADIO"]


def randomize_music(world: "PokemonCrystalWorld"):
    if not world.options.randomize_music: return

    music_pool_loop = [music_name for music_name, music_data in data.music.consts.items() if
                       music_name not in EXCLUDED_MUSIC and music_data.loop]
    music_pool_no_loop = [music_name for music_name, music_data in data.music.consts.items() if
                          music_name not in EXCLUDED_MUSIC and not music_data.loop]

    if world.options.randomize_music == RandomizeMusic.option_completely_random:
        world.generated_music = replace(
            world.generated_music,
            maps={map_name: world.random.choice(music_pool_loop) for map_name in world.generated_music.maps.keys()},
            encounters=[world.random.choice(music_pool_no_loop) for _ in world.generated_music.encounters],
            scripts={script_name: world.random.choice(
                music_pool_loop if data.music.consts[script_music].loop else music_pool_no_loop) for
                script_name, script_music in world.generated_music.scripts.items()},
        )
    else:

        all_loop_music = [music_name for music_name, music_data in data.music.consts.items() if music_data.loop] + [
            "MUSIC_NONE"]
        all_no_loop_music = [music_name for music_name, music_data in data.music.consts.items() if not music_data.loop]

        loop_mapping = {name: world.random.choice(music_pool_loop) for name in all_loop_music}
        no_loop_mapping = {name: world.random.choice(music_pool_no_loop) for name in all_no_loop_music}

        world.generated_music = replace(
            world.generated_music,
            maps={map_name: loop_mapping[music] for map_name, music in world.generated_music.maps.items()},
            encounters=[loop_mapping[music] for music in world.generated_music.encounters],
            scripts={script_name: loop_mapping[music] if data.music.consts[music].loop else no_loop_mapping[music] for
                     script_name, music in world.generated_music.scripts.items()}
        )
