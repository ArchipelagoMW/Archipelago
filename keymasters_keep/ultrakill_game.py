from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class UltrakillArchipelagoOptions:
    pass


class UltrakillGame(Game):
    # Initial Proposal by @im_not_original on Discord

    name = "ULTRAKILL"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = UltrakillArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Set FOV to X",
                data={"X": (self.fov_range, 1)},
            ),
            GameObjectiveTemplate(
                label="Set HUD Type to NONE",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set Game Resolution to 800x600",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set Gamma Brightness to GAMMA",
                data={"GAMMA": (self.gamma_range, 1)},
            ),
            GameObjectiveTemplate(
                label="Set Downscaling to 240p",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set Custom Color Palette to NOIR",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set Vertex Warping to VERY HEAVY",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set Screenshake to 200%",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Set Sound Effect Volume to 0",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Disable Blood & Gore",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete LEVEL while on DIFFICULTY difficulty",
                data={
                    "LEVEL": (self.levels_easy, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL while on DIFFICULTY difficulty",
                data={
                    "LEVEL": (self.levels_hard, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL while only using the WEAPON",
                data={
                    "LEVEL": (self.levels_easy, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL while only using the WEAPON",
                data={
                    "LEVEL": (self.levels_hard, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL",
                data={"LEVEL": (self.levels_secret, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL",
                data={"LEVEL": (self.levels_prime_sanctums, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="P-Rank LEVEL",
                data={"LEVEL": (self.levels_easy, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="P-Rank LEVEL",
                data={"LEVEL": (self.levels_hard, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="P-Rank LEVEL while only using: WEAPONS",
                data={
                    "LEVEL": (self.levels_easy, 1),
                    "WEAPONS": (self.weapons, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="P-Rank LEVEL while only using: WEAPONS",
                data={
                    "LEVEL": (self.levels_hard, 1),
                    "WEAPONS": (self.weapons, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="P-Rank LEVEL",
                data={"LEVEL": (self.levels_prime_sanctums, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL without taking damage",
                data={"LEVEL": (self.levels_easy, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Beat Wave WAVE in Cybergrind while only using: WEAPONS",
                data={
                    "WAVE": (self.cybergrind_wave_low_range, 1),
                    "WEAPONS": (self.weapons, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat Wave WAVE in Cybergrind without using: WEAPONS",
                data={
                    "WAVE": (self.cybergrind_wave_medium_range, 1),
                    "WEAPONS": (self.weapons, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat Wave WAVE in Cybergrind",
                data={"WAVE": (self.cybergrind_wave_high_range, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete all levels in LAYER (excluding secret levels) without using the WEAPON",
                data={
                    "LAYER": (self.layers, 1),
                    "WEAPON": (self.weapons, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="P-Rank all levels in LAYER (excluding secret levels)",
                data={"LAYER": (self.layers, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "HARMLESS",
            "LENIENT",
            "STANDARD",
            "VIOLENT",
            "BRUTAL",
        ]

    @staticmethod
    def weapons() -> List[str]:
        return [
            "ARMS",
            "REVOLVER",
            "SHOTGUN",
            "NAILGUN",
            "RAILCANNON",
            "ROCKET LAUNCHER",
        ]

    @staticmethod
    def fov_range() -> List[str]:
        return range(45, 161)

    @staticmethod
    def gamma_range() -> List[str]:
        return [round(x / 10.0, 1) for x in range(0, 21)]

    @staticmethod
    def levels_easy() -> List[str]:
        return [
            "0-1: INTO THE FIRE",
            "0-2: THE MEATGRINDER",
            "0-3: DOUBLE DOWN",
            "0-4: A ONE-MACHINE ARMY",
            "0-5: CERBERUS",
            "1-1: HEART OF THE SUNRISE",
            "1-2: THE BURNING WORLD",
            "1-3: HALLS OF SACRED REMAINS",
            "1-4: CLAIR DE LUNE",
            "2-1: BRIDGEBURNER",
            "2-2: DEATH AT 20,000 VOLTS",
            "2-3: SHEER HEART ATTACK",
            "2-4: COURT OF THE CORPSE KING",
            "3-1: BELLY OF THE BEAST",
            "3-2: IN THE FLESH",
        ]

    @staticmethod
    def levels_hard() -> List[str]:
        return [
            "4-1: SLAVES TO POWER",
            "4-2: GOD DAMN THE SUN",
            "4-3: A SHOT IN THE DARK",
            "4-4: CLAIR DE SOLEIL",
            "5-1: IN THE WAKE OF POSEIDON",
            "5-2: WAVES OF THE STARLESS SEA",
            "5-3: SHIP OF FOOLS",
            "5-4: LEVIATHAN",
            "6-1: CRY FOR THE WEEPER",
            "6-2: AESTHETICS OF HATE",
            "7-1: GARDEN OF FORKING PATHS",
            "7-2: LIGHT UP THE NIGHT",
            "7-3: NO SOUND, NO MEMORY",
            "7-4: ...LIKE ANTENNAS TO HEAVEN",
        ]

    @staticmethod
    def levels_secret() -> List[str]:
        return [
            "0-S: SOMETHING WICKED",
            "1-S: THE WITLESS",
            "2-S: ALL-IMPERFECT LOVE SONG",
            "4-S: CLASH OF THE BRANDICOOT",
            "5-S: I ONLY SAY MORNING",
            "7-S: HELL BATH NO FURY",
        ]

    @staticmethod
    def levels_prime_sanctums() -> List[str]:
        return [
            "P-1: SOUL SURVIVOR",
            "P-2: WAIT OF THE WORLD",
        ]

    @staticmethod
    def cybergrind_wave_low_range() -> List[str]:
        return range(1, 16)

    @staticmethod
    def cybergrind_wave_medium_range() -> List[str]:
        return range(16, 26)

    @staticmethod
    def cybergrind_wave_high_range() -> List[str]:
        return range(26, 31)

    @staticmethod
    def layers() -> List[str]:
        return [
            "PRELUDE",
            "LIMBO",
            "LUST",
            "GLUTTONY",
            "GREED",
            "WRATH",
            "HERESY",
            "VIOLENCE",
        ]


# Archipelago Options
# ...
