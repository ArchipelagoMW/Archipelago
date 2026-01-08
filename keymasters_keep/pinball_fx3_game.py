from __future__ import annotations

from typing import Dict, List, Optional, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PinballFX3ArchipelagoOptions:
    pinball_fx3_dlc_owned: PinballFX3DLCOwned


class PinballFX3Game(Game):
    name = "Pinball FX3"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = PinballFX3ArchipelagoOptions

    dlc_to_tables: Dict[Optional[str], List[str]] = {
        None: [
            "Fish Tales",
            "Sorcerer's Lair",
        ],
        "Aliens vs Pinball": [
            "Aliens Pinball",
            "Alien vs. Predator Pinball",
            "Alien: Isolation Pinball",
        ],
        "Balls of Glory Pinball": [
            "American Dad! Pinball",
            "Archer Pinball",
            "Bob's Burgers Pinball",
            "Family Guy Pinball",
        ],
        "Bethesda Pinball": [
            "DOOM Pinball",
            "Fallout Pinball",
            "The Elder Scrolls V: Skyrim Pinball",
        ],
        "Carnivals and Legends": [
            "Adventure Land",
            "Son of Zeus",
        ],
        "Core Collection": [
            "Biolab",
            "Pasha",
            "Rome",
            "Secrets of the Deep",
        ],
        "Indiana Jones: The Pinball Adventure": [
            "Indiana Jones: The Pinball Adventure",
        ],
        "Iron & Steel Pack": [
            "CastleStorm",
            "Wild West Rampage",
        ],
        "Jurassic World Pinball": [
            "Jurassic Park Pinball",
            "Jurassic Park Pinball Mayhem",
            "Jurassic World Pinball",
        ],
        "Marvel Pinball Avengers Chronicles": [
            "Fear Itself",
            "Marvel's The Avengers",
            "The Infinity Gauntlet",
            "World War Hulk",
        ],
        "Marvel Pinball Original Pack": [
            "Blade",
            "Iron Man",
            "Spider-Man",
            "Wolverine",
        ],
        "Marvel Pinball Vengeance and Virtue Pack": [
            "Ghost Rider",
            "Moon Knight",
            "Thor",
            "X-Men",
        ],
        "Marvel Pinball: Cinematic Pack": [
            "Guardians of the Galaxy",
            "Marvel's Ant-Man",
            "Marvel's Avengers: Age of Ultron",
        ],
        "Marvel Pinball: Heavy Hitters": [
            "Civil War",
            "Deadpool",
            "Venom",
        ],
        "Marvel Pinball: Marvel Legends Pack": [
            "Captain America",
            "Doctor Strange",
            "Fantastic Four",
        ],
        "Marvel's Women of Power": [
            "Marvel's Women of Power: A-Force",
            "Marvel's Women of Power: Champions",
        ],
        "Medieval Pack": [
            "Epic Quest",
            "Excalibur",
        ],
        "Portal Pinball": [
            "Portal",
        ],
        "Sci-Fi Pack": [
            "Earth Defense",
            "Mars",
            "Paranormal",
        ],
        "Star Wars Pinball: Balance of the Force": [
            "Star Wars Pinball: Darth Vader",
            "Star Wars Pinball: Return of the Jedi",
            "Star Wars Pinball: Starfighter Assault",
        ],
        "Star Wars Pinball: Heroes Within": [
            "Star Wars Pinball: A New Hope",
            "Star Wars Pinball: Droids",
            "Star Wars Pinball: Han Solo",
            "Star Wars Pinball: Masters of the Force",
        ],
        "Star Wars Pinball: Solo": [
            "Star Wars Pinball: Battle of Mimban",
            "Star Wars Pinball: Calrissian Chronicles",
            "Star Wars Pinball: Solo",
        ],
        "Star Wars Pinball: The Force Awakens Pack": [
            "Star Wars Pinball: Might of the First Order",
            "Star Wars Pinball: The Force Awakens",
        ],
        "Star Wars Pinball: The Last Jedi": [
            "Star Wars Pinball: Ahch-To Island",
            "Star Wars Pinball: The Last Jedi",
        ],
        "Star Wars Pinball: Unsung Heroes": [
            "Star Wars Pinball: Rebels",
            "Star Wars Pinball: Rogue One",
        ],
        "Star Wars Pinball": [
            "Star Wars Pinball: Boba Fett",
            "Star Wars Pinball: The Clone Wars",
            "Star Wars Pinball: The Empire Strikes Back",
        ],
        "The Walking Dead Pinball": [
            "The Walking Dead",
        ],
        "Universal Classics Pinball": [
            "Back to the Future Pinball",
            "E.T. Pinball",
            "Jaws Pinball",
        ],
        "Williams Pinball: Universal Monsters Pack": [
            "Monster Bash",
            "The Creature from the Black Lagoon",
        ],
        "Williams Pinball: Volume 1": [
            "Junk Yard",
            "Medieval Madness",
            "The Getaway: High Speed II",
        ],
        "Williams Pinball: Volume 2": [
            "Attack from Mars",
            "Black Rose",
            "The Party Zone",
        ],
        "Williams Pinball: Volume 3": [
            "Safe Cracker",
            "The Champion Pub",
            "Theater of Magic",
        ],
        "Williams Pinball: Volume 4": [
            "Hurricane",
            "Red and Ted's Road Show",
            "White Water",
        ],
        "Williams Pinball: Volume 5": [
            "Cirqus Voltaire",
            "No Good Gofers",
            "Tales of the Arabian Nights",
        ],
        "Williams Pinball: Volume 6": [
            "Dr. Dude and His Excellent Ray",
            "Funhouse",
            "Space Station",
        ],
        "Zen Classics": [
            "El Dorado",
            "Shaman",
            "Tesla",
            "V12",
        ],
    }

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="No upgrades",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Limited to the following Wizard Power: POWER",
                data={
                    "POWER": (self.wizard_powers, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Limited to the following Passive Upgrades: UPGRADES",
                data={
                    "UPGRADES": (self.passive_upgrades, 2),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Obtain at least STARS stars in a CHALLENGE on TABLE",
                data={
                    "STARS": (self.stars_easy, 1),
                    "CHALLENGE": (self.challenges, 1),
                    "TABLE": (self.tables, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain at least STARS stars in a CHALLENGE on TABLE",
                data={
                    "STARS": (self.stars_medium, 1),
                    "CHALLENGE": (self.challenges, 1),
                    "TABLE": (self.tables, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain at least STARS stars in a CHALLENGE on TABLE",
                data={
                    "STARS": (self.stars_hard, 1),
                    "CHALLENGE": (self.challenges, 1),
                    "TABLE": (self.tables, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Obtain at least STARS stars in all challenges on TABLE",
                data={
                    "STARS": (self.stars_easy, 1),
                    "TABLE": (self.tables, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain at least STARS stars in all challenges on TABLE",
                data={
                    "STARS": (self.stars_medium, 1),
                    "TABLE": (self.tables, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain at least STARS stars in all challenges on TABLE",
                data={
                    "STARS": (self.stars_hard, 1),
                    "TABLE": (self.tables, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain the achievement on TABLE",
                data={
                    "TABLE": (self.tables, 1),
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.pinball_fx3_dlc_owned.value

    def tables(self) -> List[str]:
        tables: List[str] = self.dlc_to_tables[None][:]

        dlc: Optional[str]
        for dlc in self.dlc_owned:
            tables.extend(self.dlc_to_tables[dlc])

        return sorted(tables)

    @staticmethod
    def challenges() -> List[str]:
        return [
            "1 Ball Challenge",
            "5 Minute Challenge",
            "Survival Challenge",
        ]

    @staticmethod
    def stars_easy() -> List[int]:
        return [1, 2, 3, 4, 5]

    @staticmethod
    def stars_medium() -> List[int]:
        return [6, 7, 8, 9, 10]

    @staticmethod
    def stars_hard() -> List[int]:
        return [11, 12, 13, 14, 15]

    @staticmethod
    def wizard_powers() -> List[str]:
        return [
            "Slow Motion",
            "Score Boost",
            "Rewind",
        ]

    @staticmethod
    def passive_upgrades() -> List[str]:
        return [
            "Bumper Score Bonus",
            "Multiball Score Bonus",
            "Skillshot Score Bonus",
            "Combo Time Bonus",
            "Distance Bonus",
            "Ball Save Time Bonus",
        ]


# Archipelago Options
class PinballFX3DLCOwned(OptionSet):
    """
    Indicates which Pinball FX3 DLC packs the player owns, if any.
    """

    display_name = "Pinball FX3 DLC Owned"
    valid_keys = [
        "Aliens vs Pinball",
        "Balls of Glory Pinball",
        "Bethesda Pinball",
        "Carnivals and Legends",
        "Core Collection",
        "Indiana Jones: The Pinball Adventure",
        "Iron & Steel Pack",
        "Jurassic World Pinball",
        "Marvel Pinball Avengers Chronicles",
        "Marvel Pinball Original Pack",
        "Marvel Pinball Vengeance and Virtue Pack",
        "Marvel Pinball: Cinematic Pack",
        "Marvel Pinball: Heavy Hitters",
        "Marvel Pinball: Marvel Legends Pack",
        "Marvel's Women of Power",
        "Medieval Pack",
        "Portal Pinball",
        "Sci-Fi Pack",
        "Star Wars Pinball: Balance of the Force",
        "Star Wars Pinball: Heroes Within",
        "Star Wars Pinball: Solo",
        "Star Wars Pinball: The Force Awakens Pack",
        "Star Wars Pinball: The Last Jedi",
        "Star Wars Pinball: Unsung Heroes",
        "Star Wars Pinball",
        "The Walking Dead Pinball",
        "Universal Classics Pinball",
        "Williams Pinball: Universal Monsters Pack",
        "Williams Pinball: Volume 1",
        "Williams Pinball: Volume 2",
        "Williams Pinball: Volume 3",
        "Williams Pinball: Volume 4",
        "Williams Pinball: Volume 5",
        "Williams Pinball: Volume 6",
        "Zen Classics",
    ]

    default = valid_keys
