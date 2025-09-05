import asyncio
import pkgutil
from asyncio import Task
from pathlib import Path

from CommonClient import logger
from kivy.core.audio import Sound, SoundLoader

from .. import apquest
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
VICTORY_JINGLE = "8bit Victory.ogg"

ALL_JINGLES = [
    CONFETTI_CANNON,
    VICTORY_JINGLE,
    *ITEM_JINGLES.values(),
]

BACKGROUND_MUSIC_INTRO = "APQuest Intro.ogg"
BACKGROUND_MUSIC = "APQuest BGM.ogg"

ALL_SOUNDS = [
    *ALL_JINGLES,
    BACKGROUND_MUSIC_INTRO,
    BACKGROUND_MUSIC,
]


class SoundManager:
    sound_paths: dict[str, Path]
    jingles: dict[str, Sound]

    background_music_intro: Sound
    background_music: Sound

    background_music_target_volume: float = 0

    background_music_task: Task | None = None
    background_music_last_position: int = 0

    game_started: bool
    allow_intro_to_play: bool

    def __init__(self) -> None:
        self.extract_sounds()
        self.populate_sounds()

        self.game_started = False
        self.allow_intro_to_play = False

        self.background_music_task = asyncio.create_task(self.sound_manager_loop())

    async def sound_manager_loop(self) -> None:
        while True:
            if not self.game_started:
                if self.allow_intro_to_play and self.background_music_intro.state == "stop":
                    self.background_music_intro.play()
                await asyncio.sleep(0.02)
                continue

            self.update_background_music()
            self.do_fade()
            self.background_music_intro.stop()
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
                data = pkgutil.get_data(apquest.__name__, f"audio/{sound}")
                if data is None:
                    logger.exception(f"Unable to extract sound {sound} to Archipelago/data")
                sound_file.write(data)

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
            self.background_music = self.load_audio(BACKGROUND_MUSIC)
            self.background_music.loop = True
            self.background_music.seek(0)
        except Exception as e:
            logger.exception(e)

        try:
            self.background_music_intro = self.load_audio(BACKGROUND_MUSIC_INTRO)
            self.background_music_intro.loop = True
            self.background_music_intro.seek(0)
        except Exception as e:
            logger.exception(e)

    def play_jingle(self, audio_filename) -> None:
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
        if any(sound.state == "play" for sound in self.jingles.values()):
            self.play_background_music(False)
        else:
            self.fade_background_music(True)

    def play_background_music(self, play: bool = True) -> None:
        if play:
            self.background_music_target_volume = 1
            self.background_music.volume = 1
        else:
            self.background_music_target_volume = 0
            self.background_music.volume = 0

    def fade_background_music(self, fade_in: bool = True) -> None:
        if fade_in:
            self.background_music_target_volume = 1
        else:
            self.background_music_target_volume = 0

    def do_fade(self) -> None:
        if self.background_music.volume > self.background_music_target_volume:
            self.background_music.volume = max(0.0, self.background_music.volume - 0.02)
        if self.background_music.volume < self.background_music_target_volume:
            self.background_music.volume = min(1.0, self.background_music.volume + 0.02)

        if self.background_music.volume == 0:
            if self.background_music.state == "play":
                self.background_music_last_position = self.background_music.get_pos()
                if self.background_music_last_position != 0:  # SDL2 get_pos doesn't work, just continue playing muted
                    self.background_music.stop()
        else:
            if self.background_music.state == "stop":
                if self.background_music_last_position != 0:  # SDL2 get_pos doesn't work
                    self.background_music.seek(self.background_music_last_position)
                self.background_music.play()
