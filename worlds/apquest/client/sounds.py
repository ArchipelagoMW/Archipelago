import pkgutil
from pathlib import Path

from .item_quality import ItemQuality
from .utils import make_data_directory

ITEM_JINGLES = {
    ItemQuality.PROGUSEFUL: "8bit ProgUseful.wav",
    ItemQuality.PROGRESSION: "8bit Progression.wav",
    ItemQuality.USEFUL: "8bit Useful.wav",
    ItemQuality.TRAP: "8bit Trap.wav",
    ItemQuality.FILLER: "8bit Filler.wav",
}

VICTORY_JINGLE = "8bit Victory.wav"

ALL_SOUNDS = [
    *ITEM_JINGLES.values(),
    VICTORY_JINGLE,
]


def ensure_sounds_available() -> dict[str, Path]:
    # Kivy appears to have no good way of loading audio from bytes. So, we have to extract it out of the .apworld first

    sound_paths = {}

    sound_directory = make_data_directory("sounds")

    for sound in ALL_SOUNDS:
        sound_file_location = sound_directory / sound

        sound_paths[sound] = sound_file_location

        if sound_file_location.exists():
            continue

        with open(sound_file_location, "wb") as sound_file:
            data = pkgutil.get_data(__name__, f"../apquest/audio/{sound}")
            if data is None:
                raise FileNotFoundError(f"Unable to extract sound {sound} to Archipelago/data")
            sound_file.write(data)

    return sound_paths


SOUND_PATHS = ensure_sounds_available()
