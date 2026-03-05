import asyncio
import pkgutil
from asyncio import Task
from collections.abc import Buffer
from pathlib import Path
from typing import cast

from kivy import Config
from kivy.core.audio import Sound, SoundLoader

from CommonClient import logger

from .. import game
from .item_quality import ItemQuality
from .utils import make_data_directory

ITEM_JINGLES = {
    ItemQuality.PROGUSEFUL: "8bit ProgUseful.ogg",
    ItemQuality.PROGRESSION: "8bit Progression.ogg",
    ItemQuality.USEFUL: "8bit Useful.ogg",
    ItemQuality.TRAP: "8bit Trap.ogg",
    ItemQuality.FILLER: "8bit Filler.ogg",
}

CONFETTI_CANNON = "APQuest Confetti Cannon.ogg"
MATH_PROBLEM_STARTED_JINGLE = "APQuest Math Problem Starter Jingle.ogg"
MATH_PROBLEM_SOLVED_JINGLE = "APQuest Math Problem Solved Jingle.ogg"
VICTORY_JINGLE = "8bit Victory.ogg"

ALL_JINGLES = [
    MATH_PROBLEM_SOLVED_JINGLE,
    MATH_PROBLEM_STARTED_JINGLE,
    CONFETTI_CANNON,
    VICTORY_JINGLE,
    *ITEM_JINGLES.values(),
]

BACKGROUND_MUSIC_INTRO = "APQuest Intro.ogg"
BACKGROUND_MUSIC = "APQuest BGM.ogg"
MATH_TIME_BACKGROUND_MUSIC = "APQuest Math BGM.ogg"

ALL_BGM = [
    BACKGROUND_MUSIC_INTRO,
    BACKGROUND_MUSIC,
    MATH_TIME_BACKGROUND_MUSIC,
]

ALL_SOUNDS = [
    *ALL_JINGLES,
    *ALL_BGM,
]


class SoundManager:
    sound_paths: dict[str, Path]

    jingles: dict[str, Sound]
    bgm_songs: dict[str, Sound]

    active_bgm_song: str = BACKGROUND_MUSIC_INTRO

    current_background_music_volume: float = 1.0
    background_music_target_volume: float = 0.0

    background_music_task: Task[None] | None = None
    background_music_last_position: int = 0

    volume_percentage: int = 0

    game_started: bool
    math_trap_active: bool
    allow_intro_to_play: bool

    def __init__(self) -> None:
        self.extract_sounds()
        self.populate_sounds()

        self.game_started = False
        self.allow_intro_to_play = False
        self.math_trap_active = False

        self.ensure_config()

        self.background_music_task = asyncio.create_task(self.sound_manager_loop())

    def ensure_config(self) -> None:
        Config.adddefaultsection("APQuest")
        Config.setdefault("APQuest", "volume", 50)
        self.set_volume_percentage(Config.getint("APQuest", "volume"))

    async def sound_manager_loop(self) -> None:
        while True:
            self.update_background_music()
            self.do_fade()
            await asyncio.sleep(0.02)

    def extract_sounds(self) -> None:
        # Kivy appears to have no good way of loading audio from bytes.
        # So, we have to extract it out of the .apworld first

        sound_paths = {}

        sound_directory = make_data_directory("sounds")

        for sound in ALL_SOUNDS:
            sound_file_location = sound_directory / sound

            sound_paths[sound] = sound_file_location

            if sound_file_location.exists():
                continue

            with open(sound_file_location, "wb") as sound_file:
                data = pkgutil.get_data(game.__name__, f"audio/{sound}")
                if data is None:
                    logger.exception(f"Unable to extract sound {sound} to Archipelago/data")
                    continue
                sound_file.write(cast(Buffer, data))

        self.sound_paths = sound_paths

    def load_audio(self, sound_filename: str) -> Sound:
        audio_path = self.sound_paths[sound_filename]

        sound_object = SoundLoader.load(str(audio_path.absolute()))
        sound_object.seek(0)
        return sound_object

    def populate_sounds(self) -> None:
        try:
            self.jingles = {sound_filename: self.load_audio(sound_filename) for sound_filename in ALL_JINGLES}
        except Exception as e:
            logger.exception(e)

        try:
            self.bgm_songs = {sound_filename: self.load_audio(sound_filename) for sound_filename in ALL_BGM}
            for bgm_song in self.bgm_songs.values():
                bgm_song.loop = True
                bgm_song.seek(0)
        except Exception as e:
            logger.exception(e)

    def play_jingle(self, audio_filename: str) -> None:
        higher_priority_sound_is_playing = False

        for sound_name, sound in self.jingles.items():
            if higher_priority_sound_is_playing:  # jingles are ordered by priority, lower priority gets eaten
                sound.stop()
                continue

            if sound_name == audio_filename:
                sound.play()
                self.update_background_music()
                higher_priority_sound_is_playing = True

            elif sound.state == "play":
                higher_priority_sound_is_playing = True

    def update_background_music(self) -> None:
        self.update_active_song()
        if any(sound.state == "play" for sound in self.jingles.values()):
            self.play_background_music(False)
        else:
            if self.math_trap_active:
                # Don't fade math trap song, it ends up feeling better
                self.play_background_music(True)
            else:
                self.fade_background_music(True)

    def play_background_music(self, play: bool = True) -> None:
        if play:
            self.background_music_target_volume = 1
            self.set_background_music_volume(1)
        else:
            self.background_music_target_volume = 0
            self.set_background_music_volume(0)

    def set_background_music_volume(self, volume: float) -> None:
        self.current_background_music_volume = volume

        for song_filename, song in self.bgm_songs.items():
            if song_filename != self.active_bgm_song:
                song.volume = 0
                continue
            song.volume = volume * self.volume_percentage / 100

    def fade_background_music(self, fade_in: bool = True) -> None:
        if fade_in:
            self.background_music_target_volume = 1
        else:
            self.background_music_target_volume = 0

    def set_volume_percentage(self, volume_percentage: float) -> None:
        volume_percentage_int = int(volume_percentage)
        if self.volume_percentage != volume_percentage:
            self.volume_percentage = volume_percentage_int
            Config.set("APQuest", "volume", volume_percentage_int)
            Config.write()
            self.set_background_music_volume(self.current_background_music_volume)

            for jingle in self.jingles.values():
                jingle.volume = self.volume_percentage / 100

    def do_fade(self) -> None:
        if self.current_background_music_volume > self.background_music_target_volume:
            self.set_background_music_volume(max(0.0, self.current_background_music_volume - 0.02))
        if self.current_background_music_volume < self.background_music_target_volume:
            self.set_background_music_volume(min(1.0, self.current_background_music_volume + 0.02))

        for song_filename, song in self.bgm_songs.items():
            if song_filename != self.active_bgm_song:
                if song_filename == BACKGROUND_MUSIC:
                    # It ends up feeling better if this just always continues playing quietly after being started.
                    # Even "fading in at a random spot" is better than restarting the song after a jingle / math trap.
                    if self.game_started and song.state == "stop":
                        song.play()
                        song.seek(0)
                    continue

                song.stop()
                song.seek(0)
                continue

            if self.active_bgm_song == BACKGROUND_MUSIC_INTRO and not self.allow_intro_to_play:
                song.stop()
                song.seek(0)
                continue

            if self.current_background_music_volume != 0:
                if song.state == "stop":
                    song.play()
                    song.seek(0)

    def update_active_song(self) -> None:
        new_active_song = self.determine_correct_song()
        if new_active_song == self.active_bgm_song:
            return
        self.active_bgm_song = new_active_song
        # reevaluate song volumes
        self.set_background_music_volume(self.current_background_music_volume)

    def determine_correct_song(self) -> str:
        if not self.game_started:
            return BACKGROUND_MUSIC_INTRO

        if self.math_trap_active:
            return MATH_TIME_BACKGROUND_MUSIC

        return BACKGROUND_MUSIC
