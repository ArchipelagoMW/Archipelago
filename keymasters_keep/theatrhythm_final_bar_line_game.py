from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TheatrhythmFinalBarLineArchipelagoOptions:
    theatrhythm_final_bar_line_dlc_owned: TheatrhythmFinalBarLineDLCOwned


class TheatrhythmFinalBarLineGame(Game):
    name = "Theatrhythm: Final Bar Line"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
    ]

    is_adult_only_or_unrated = False

    options_cls = TheatrhythmFinalBarLineArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play with CHARACTER in the party",
                data={
                    "CHARACTER": (self.characters, 1)
                },
            ),
            GameObjectiveTemplate(
                label="Play with CHARACTERS in the party",
                data={
                    "CHARACTERS": (self.characters, 2)
                },
            ),
            GameObjectiveTemplate(
                label="Play with CHARACTERS in the party",
                data={
                    "CHARACTERS": (self.characters, 3)
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.theatrhythm_final_bar_line_dlc_owned.value)

    @property
    def has_dlc_digital_deluxe(self) -> bool:
        return "Digital Deluxe" in self.dlc_owned

    @property
    def has_dlc_saga_vol_1(self) -> bool:
        return "SaGa Vol 1" in self.dlc_owned

    @property
    def has_dlc_live_a_live(self) -> bool:
        return "LIVE A LIVE" in self.dlc_owned

    @property
    def has_dlc_the_world_ends_with_you(self) -> bool:
        return "The World Ends With You" in self.dlc_owned

    @property
    def has_dlc_nier_vol_1(self) -> bool:
        return "Nier Vol 1" in self.dlc_owned

    @property
    def has_dlc_saga_vol_2(self) -> bool:
        return "SaGa Vol 2" in self.dlc_owned

    @property
    def has_dlc_nier_vol_2(self) -> bool:
        return "NieR Vol 2" in self.dlc_owned

    @property
    def has_dlc_chrono_vol_1(self) -> bool:
        return "CHRONO Vol 1" in self.dlc_owned

    @property
    def has_dlc_chrono_vol_2(self) -> bool:
        return "CHRONO Vol 2" in self.dlc_owned

    @property
    def has_dlc_mana_vol_1(self) -> bool:
        return "Mana Vol 1" in self.dlc_owned

    @property
    def has_dlc_octopath_traveler(self) -> bool:
        return "OCTOPATH TRAVELER" in self.dlc_owned

    @property
    def has_dlc_saga_vol_3(self) -> bool:
        return "SaGa Vol 3" in self.dlc_owned

    @property
    def has_dlc_mana_vol_2(self) -> bool:
        return "Mana Vol 2" in self.dlc_owned

    @property
    def has_dlc_xenogears(self) -> bool:
        return "Xenogears" in self.dlc_owned

    @property
    def has_dlc_bravely_default(self) -> bool:
        return "BRAVELY DEFAULT" in self.dlc_owned

    @property
    def has_dlc_final_fantasy_16(self) -> bool:
        return "Final Fantasy 16" in self.dlc_owned

    @staticmethod
    def characters() -> List[str]:
        return [
            "Warrior of Light",
            "Princess Sarah",
            "Garland",
            "Firion",
            "Minwu",
            "Maria",
            "Guy",
            "Leon",
            "The Emperor",
            "Onion Knight",
            "Cid Haze",
            "Cloud of Darkness",
            "Cecil",
            "Kain",
            "Rydia",
            "Rosa",
            "Edge",
            "Golbez",
            "Bartz",
            "Lenna",
            "Galuf",
            "Faris",
            "Krile",
            "Gilgamesh",
            "Exdeath",
            "Terra",
            "Locke",
            "Edgar",
            "Celes",
            "Mog",
            "Kefka",
            "Cloud",
            "Cloud #2",
            "Barret",
            "Tifa",
            "Tifa #2",
            "Aerith",
            "Yuffie",
            "Vincent",
            "Sephiroth",
            "Zach",
            "Red XIII",
            "Squall",
            "Seifer",
            "Rinoa",
            "Laguna",
            "Edea",
            "Ultimecia",
            "Zidane",
            "Vivi",
            "Garnet",
            "Eiko",
            "Kuja",
            "Tidus",
            "Yuna",
            "Yuna #2",
            "Auron",
            "Jecht",
            "Rikku",
            "Paine",
            "Seymour",
            "Shantotto",
            "Prishe",
            "Aphmau",
            "Lillisette",
            "Vaan",
            "Ashe",
            "Balthier",
            "Fran",
            "Gabranth",
            "Lightning",
            "Lightning #2",
            "Snow",
            "Vanille",
            "Hope",
            "Serah",
            "Noel",
            "Cid Raines",
            "Y'sholta",
            "Y'sholta #2",
            "Yda",
            "Thancred",
            "Alphinaud",
            "Noctis",
            "Gladiolus",
            "Ignis",
            "Prompto",
            "Aranea",
            "Benjamin",
            "Ramza",
            "Agrias",
            "Orlandeau",
            "Ciaran",
            "Ace",
            "Machina",
            "Rem",
            "Kurasame",
            "Tyro",
            "Wol",
            "Cosmos",
            "Chaos",
            "Materia",
            "Spiritus",
            "Chocobo",
        ]

    @functools.cached_property
    def songs_ff1(self) -> List[str]:
        return [
            "Opening Theme (E) (1)",
            "Main Theme (1)",
            "Castle Cornelia (1)",
            "Battle (1)",
            "Opening Theme (1)",
            "Matoya's Cave (1)",
            "Miniboss Battle (1)",
            "Mt. Gulg (1)",
            "Airship (1)",
            "Sunken Shrine (1)",
            "Final Battle (1)",
        ]

    @functools.cached_property
    def songs_ff2(self) -> List[str]:
        return [
            "The Rebel Army (E) (2)",
            "Battle Theme 1 (2)",
            "The Rebel Army (2)",
            "Town (2)",
            "Main Theme (2)",
            "Dungeon (2)",
            "The Imperial Army (2)",
            "Chocobo Theme (2)",
            "Tower of the Magi (2)",
            "Battle Theme A (2)",
            "Battle Theme 2 (2)",
            "Finale (2)",
        ]

    @functools.cached_property
    def songs_ff3(self) -> List[str]:
        return [
            "Elia, the Maiden of Water (E) (3)",
            "Crystal Cave (3)",
            "Battle 1 (3)",
            "Eternal Wind (3)",
            "The Boundless Ocean (3)",
            "Elia, the Maiden of Water (3)",
            "Salonia (3)",
            "Let Me Know the Truth (3)",
            "The Invincible (3)",
            "Forbidden Land (3)",
            "The Crystal Tower (3)",
            "Battle 2 (3)",
            "The Dark Crystals (3)",
            "This is the Last Battle (3)",
        ]

    @functools.cached_property
    def songs_ff4(self) -> List[str]:
        return [
            "Theme of Love (E) (4)",
            "The Red Wings (4)",
            "Theme of Love (4)",
            "Main Theme of Final Fantasy IV (4)",
            "Battle 1 (4)",
            "The Airship (4)",
            "Trojan Beauty (4)",
            "Tower of Zot (4)",
            "Within the Giant (4)",
            "Battle 2 (4)",
            "Battle With the Four Fiends (4)",
            "Lunar Whale (4)",
            "Another Moon (4)",
            "The Final Battle (4)",
        ]

    @functools.cached_property
    def songs_ff5(self) -> List[str]:
        return [
            "Home, sweet Home (E) (5)",
            "Main Theme of Final Fantasy V (5)",
            "Four Hearts (5)",
            "Battle 1 (5)",
            "Harvest (5)",
            "To the North Mountain (5)",
            "Library of the Ancients (5)",
            "Mambo de Chocobo (5)",
            "Home, sweet Home (5)",
            "The Airship (5)",
            "Battle 2 (5)",
            "The Dawn Warriors (5)",
            "Battle at the Big Bridge (5)",
            "A New World (5)",
            "In Search of Light (5)",
            "The Decisive Battle (5)",
            "The Final Battle (5)",
        ]

    @functools.cached_property
    def songs_ff6(self) -> List[str]:
        return [
            "Celes' Theme (E) (6)",
            "Terra's Theme (6)",
            "Battle (6)",
            "Locke's Theme (6)",
            "Edgar & Sabin's Theme (6)",
            "Protect the Espers! (6)",
            "Grand Finale (6)",
            "The Airship Blackjack (6)",
            "The Decisive Battle (6)",
            "Battle to the Death (6)",
            "Celes' Theme (6)",
            "Searching for Friends (6)",
            "Kefka's Tower (6)",
            "Dancing Mad (6)",
        ]

    @functools.cached_property
    def songs_ff7(self) -> List[str]:
        return [
            "Aerith's Theme (E) (7)",
            "Opening - Bombing Mission (7)",
            "Let the Battles Begin! (7)",
            "Fight On! (7)",
            "The Chase (7)",
            "Main Theme of Final Fantasy VII (7)",
            "Rufus' Welcoming Ceremony (7)",
            "Gold Saucer (7)",
            "Cosmo Canyon (7)",
            "Aerith's Theme (7)",
            "The Highwind Takes to the Skies (7)",
            "Judgment Day (7)",
            "JENOVA (7)",
            "Birth of a God (7)",
            "One-Winged Angel (7)",
        ]

    @functools.cached_property
    def songs_ff7_series(self) -> List[str]:
        return [
            "Advent: One-Winged Angel (E) (Advent Children)",
            "Beyond the Wasteland (Advent Children)",
            "Those Who Fight (Piano Version) (Advent Children)",
            "Aerith's Theme (Piano Version) (Advent Children)",
            "Battle in the Forgotten City (Advent Children)",
            "Divinity II (Advent Children)",
            "J-E-N-O-V-A (AC Version) (Advent Children)",
            "Advent: One-Winged Angel (Advent Children)",
            "Cloud Smiles (Advent Children)",
            "Last Order (Last Order)",
            "Theme of Crisis Core - Succession (Crisis Core)",
            "Encounter (Crisis Core)",
            "Timely Ambush (from FFVII 'Let the Battles Begin') (Crisis Core)",
            "Flower Blooming in the Slums (from FFVII 'Aerith's Theme') (Crisis Core)",
            "The SOLDIER Way (Crisis Core)",
            "The Price of Freedom (Crisis Core)",
        ]

    @functools.cached_property
    def songs_ff7_remake(self) -> List[str]:
        return [
            "Hollow (7 Remake) ",
            "FFVII REMAKE: Bombing Mission (7 Remake) ",
            "FFVII REMAKE: Tifa's Theme - Seventh Heaven (7 Remake) ",
            "FFVII REMAKE: Main Theme of FF7 - Sector 7 Undercity (7 Remake) ",
            "FFVII REMAKE: Let the Battles Begin - A Merc's Job (7 Remake) ",
            "FFVII REMAKE: The Airbuster (7 Remake) ",
            "FFVII REMAKE: Collapsed Expressway (7 Remake) ",
            "FFVII REMAKE: High Five (7 Remake) ",
            "FFVII REMAKE: J-E-N-O-V-A - Quickening (7 Remake) ",
            "FFVII REMAKE: Midgar Expressway (7 Remake) ",
            "FFVII REMAKE: One-Winged Angel - Rebirth (7 Remake)",
        ]

    @functools.cached_property
    def songs_ff8(self) -> List[str]:
        return [
            "Waltz for the Moon (E) (8)",
            "Liberi Fatali (8)",
            "Balamb GARDEN (8)",
            "Blue Fields (8)",
            "Don't Be Afraid (8)",
            "Find Your Way (8)",
            "Force Your Way (8)",
            "Shuffle or Boogie (8)",
            "Waltz for the Moon (8)",
            "The Man with the Machine Gun (8)",
            "Fisherman's Horizon (8)",
            "Love Grows (8)",
            "Ride On (8)",
            "The Oath (8)",
            "The Castle (8)",
            "Premonition (8)",
            "Maybe I'm a Lion (8)",
            "The Extreme (8)",
            "Ending Theme (8)",
        ]

    @functools.cached_property
    def songs_ff9(self) -> List[str]:
        return [
            "Behind the Door (E) (9)",
            "A Place to Call Home (9)",
            "Vivi's Theme (9)",
            "Swords of Fury (9)",
            "Vamo'alla flamenco (9)",
            "Battle 1 (9)",
            "Over the Hill (9)",
            "Festival of the Hunt (9)",
            "Dark City Treno (9)",
            "Roses of May (9)",
            "Iifa, the Ancient Tree of Life (9)",
            "Something to Protect (9)",
            "Aboard the Hilda Garde (9)",
            "Ipsen's Castle (9)",
            "Not Alone (9)",
            "Battle 2 (9)",
            "The Darkness of Eternity (9)",
            "The Final Battle (9)",
            "Behind the Door (9)",
        ]

    @functools.cached_property
    def songs_ff10(self) -> List[str]:
        return [
            "SUTEKI DA NE (Isn't It Wonderful?) (E) (10)",
            "Battle Theme (10)",
            "Spira Unplugged (10)",
            "Blitz Off! (10)",
            "Movement in Green (10)",
            "Mi'ihen Highroad (10)",
            "Thunder Plains (10)",
            "Launch (10)",
            "Assault (10)",
            "Via Purifico (10)",
            "SUTEKI DA NE (Isn't It Wonderful?) (10)",
            "Servants of the Mountain (10)",
            "A Fleeting Dream (10)",
            "Challenge (10)",
            "Fight with Seymour (10)",
            "Otherworld (10)",
            "A Contest of Aeons (10)",
            "Final Battle (10)",
        ]

    @functools.cached_property
    def songs_ff10_2(self) -> List[str]:
        return [
            "1000 Words (FFX-2 Mix) (10-2)",
            "YuRiPa, Fight! No.1 (10-2)",
            "We're the Gullwings! (10-2)",
            "Let me blow you a kiss. (10-2)",
            "The Bevelle Underground (10-2)",
            "The Farplane Abyss (10-2)",
            "Their Resting Place (10-2)",
        ]

    @functools.cached_property
    def songs_ff11(self) -> List[str]:
        return [
            "FFXI Opening Theme (E) (11)",
            "FF1XI Opening Theme (11)",
            "Vana'diel March (11)",
            "Ronfaure (11)",
            "Battle Theme (11)",
            "Gustaberg (11)",
            "Heavens Tower (11)",
            "Sarutabaruta (11)",
            "Voyager (11)",
            "Selbina (11)",
            "Recollection (11)",
            "Awakening (11)",
            "Tough Battle #2 (11)",
            "The Sanctuary of Zi'Tah (11)",
            "Fighters of the Crystal (11)",
            "A New Horizon - Tavnazian Achipelago (11)",
            "Iron Colossus (11)",
            "Ragnarok (11)",
            "Melodies Errant (11)",
            "Shinryu (11)",
        ]

    @functools.cached_property
    def songs_ff12(self) -> List[str]:
        return [
            "The Archadian Empire - original - from FINAL FANTASY XII (E) (12)",
            "FINAL FANTASY (FFXII Version) (12)",
            "Streets of Rabanastre (12)",
            "The Dalmasca Estersand (12)",
            "Heart of a Child (12)",
            "Giza Plains (from FINAL FANTASY XII Original Soundtrack) (12)",
            "The Archadian Empire - original - from FINAL FANTASY XII (12)",
            "Phon Coast (12)",
            "The Mosphoran Highwaste (12)",
            "Boss Battle (12)",
            "Flash of Steel (12)",
            "Battle with an Esper (12)",
            "Life and Death (12)",
            "Struggle for Freedom (12)",
            "Ending Movie (from FINAL FANTASY XII Original Soundtrack) (12)",
        ]

    @functools.cached_property
    def songs_ff13(self) -> List[str]:
        return [
            "Defiers of Fate (E) (13)",
            "Defiers of Fate (13)",
            "Saber's Edge (13)",
            "Blinded by Light (13)",
            "March of the Dreadnoughts (13)",
            "The Gapra Whitewood (13)",
            "The Sunleth Waterscape (13)",
            "The Archylte Steppe (13)",
            "Desperate Struggle (13)",
            "Will to Fight (13)",
            "Dust to Dust (13)",
            "Eden Under Siege (13)",
            "Fighting Fate (13)",
            "Nascent Requiem (13)",
        ]

    @functools.cached_property
    def songs_ff13_series(self) -> List[str]:
        return [
            "Warrior Goddess (13-2)",
            "Etro's Champion (13-2)",
            "Paradigm Shift (13-2)",
            "Historia Crux (13-2)",
            "The Last Hunter (13-2)",
            "Full Speed Ahead (13-2)",
            "Eclipse (13 2)",
            "Plains of Eternity (13-2)",
            "Groovy Chocobo (13-2)",
            "Crazy Chocobo (13-2)",
            "Noel's Theme - Final Journey (13-2)",
            "Heart of Chaos (13-2)",
            "The Savior - LIGHTNING RETURNS:FINAL FANTASY XIII (E) (Lightning: 13)",
            "LIGHTNING RETURNS - LIGHTNING RETURNS:FINAL FANTASY XIII (Lightning: 13)",
            "Crimson Blitz (Lightning: 13)",
            "The Glittering City of Yusnaan (Lightning: 13)",
            "The Dead Dunes (Lightning: 13)",
            "The Savior - LIGHTNING RETURNS:FINAL FANTASY XIII (Lightning: 13)",
            "Chaos (Lightning: 13)",
        ]

    @functools.cached_property
    def songs_ff14(self) -> List[str]:
        return [
            "Answers (14)",
            "On Westerly Winds (14)",
            "Serenity (14)",
            "To the Sun (14)",
            "The Land Breathes (14)",
            "Hard to Miss (14)",
            "Torn from the Heavens (14)",
            "Nemesis (14)",
            "Primal Judgment (14)",
            "Under the Weight (14)",
            "Engage (14)",
            "Fallen Angel (14)",
            "Good King Moggle Mog XII (14)",
            "Ultima (14)",
            "Through the Maelstrom (14)",
            "A Light in the Storm (14)",
            "Oblivion (14)",
            "Ominous Prognisticks (14)",
            "Ink Long Dry (14)",
            "Heroes (14)",
            "Locus (14)",
            "Metal - Brute Justice Mode (14)",
            "Exponential Entropy (14)",
            "Moebius (14)",
            "Rise (14)",
            "Triumph (14)",
            "The Worm's Tail (14)",
            "Wayward Daughter (14)",
            "Sunrise (14)",
            "What Angel Wakes Me (14)",
            "Who Brings Shadow (14)",
            "A Long Fall (14)",
            "Promises to Keep (14)",
        ]

    @functools.cached_property
    def songs_ff15(self) -> List[str]:
        return [
            "APOCALYPSIS NOCTIS (E) (15)",
            "Stand Your Ground (15)",
            "Veiled in Black (15)",
            "Valse di Fantasica (15)",
            "The Fight is On! (15)",
            "APOCALYPSIS NOCTIS (Uncovered Trailer Version) (15)",
            "Flying R (15)",
            "Invidia (15)",
            "OMNIS LARCIMA (15)",
            "Up for the Challenge (15)",
            "Somnus (15)",
            "Hellfire (15)",
            "Magna Insomnia (15)",
            "Main Theme from FINAL FANTASY (15)",
            "NOCTIS (15)",
            "Shield of the King - Theme of EPISODE GLADIOLUS (15)",
            "EPISODE IGNIS - The Main Theme (15)",
            "Home Sweet Home - Theme of EPISODE PROMPTO (15)",
            "Dance of the Silver and Crimson (15)",
        ]

    @functools.cached_property
    def songs_ff_mystic_quest(self) -> List[str]:
        return [
            "Hill of Destiny (Mystic Quest)",
            "Battle 1 (Mystic Quest)",
            "Battle 2 (Mystic Quest)",
            "Doom Castle (Mystic Quest)",
            "Battle 3 (Mystic Quest)",
        ]

    @functools.cached_property
    def songs_ff_tactics(self) -> List[str]:
        return [
            "Opening (Tactics)",
            "Prologue (Tactics)",
            "Trisection (Tactics)",
            "Apoplexy (Tactics)",
            "Antipyretic (Tactics)",
            "Precipitous Combat (Tactics)",
            "Ovelia's Theme (Tactics)",
            "Ultima's Transformation (Tactics)",
        ]

    @functools.cached_property
    def songs_ff_crystal_chronicles_series(self) -> List[str]:
        return [
            "FFCCR: Moonless Starry Night (Crystal Chronicles Remastered)",
            "FFCCR: Today Comes to Be Tomorrow (Crystal Chronicles Remastered)",
            "FFCCR: Promised Grace (Crystal Chronicles Remastered)",
            "FFCCR: Monster Ronde (Crystal Chronicles Remastered)",
            "FFCCR: Across the Divide (Crystal Chronicles Remastered)",
            "FFCCR: Woebegone Creature (Crystal Chronicles Remastered)",
            "FFCCR: United, Heaven-Sent (Crystal Chronicles Remastered)",
            "This is the End for You! (Crystal Chronicles Crystal Bearers)",
        ]

    @functools.cached_property
    def songs_ff_dissidia_series(self) -> List[str]:
        return [
            "DISSIDIA FINAL FANTASY [FINAL TRAILER] (Dissidia)",
            "Keeping the Peace from DISSIDIA FINAL FANTASY (Dissidia)",
            "The Decisive Battle - arrange - from FINAL FANTASY VI (Dissidia)",
            "Battle 1 - arrange - from FINAL FANTASY ix (Dissidia)",
            "The Troops' Advance from DISSIDIA FINAL FANTASY (Dissidia)",
            "DISSIDIA - ending - from DISSIDIA FINAL FANTASY (Dissidia)",
            "Lux Concordiae from DISSIDIA 012[duodecim] FINAL FANTASY (Dissidia 012[duodecim])",
            "DISSIDIA 012[duodecim] [Final Trailer] (Dissidia 012[duodecim])",
            "Canto Mortis -An Undocumented Battle- from DISSIDIA 012[duodecim] FINAL FANTASY (Dissidia 012[duodecim])",
            "Gate to the Rift from DISSIDIA 012[duodecim] FINAL FANTASY (Dissidia 012[duodecim])",
            "Cantata Mortis from DISSIDIA 012[duodecim] FINAL FANTASY (Dissidia 012[duodecim])",
            "The Rebel Army - from FINAL FANTASY II (Arrangement) (Dissidia Arcade)",
            "Eternal Wind - from FINAL FANTASY III (Arrangement) (Dissidia Arcade)",
            "Dancing Mad - from FINAL FANTASY XI (Arrangement) (Dissidia Arcade)",
            "Ominous Prognisticks - from FINAL FANTASY XIV (Arrangement) (Dissidia Arcade)",
            "Antipyrectic from FINAL FANTASY TACTICS (Arrangement) (Dissidia Arcade)",
            "The Beginning of the End from FINAL FANTASY TYPE-O (Arrangement) (Dissidia Arcade)",
            "Massive Explosion (Short ver.) from DISSIDIA FINAL FANTASY -Arcade- (Dissidia Arcade)",
            "God in Fire - arange - from DISSIDIA FINAL FANTASY -Arcade-(Dissidia Arcade)",
            "Spark from DISSIDIA FINAL FANTASY OPERA OMNIA (Dissidia Opera Omnia)",
            "Dare to Defy (Dissidia NT)",
        ]

    @functools.cached_property
    def songs_ff_type_0(self) -> List[str]:
        return [
            "We Have Come (E) (Type: 0)",
            "We Have Come (Type: 0)",
            "War: Warrior Worth a Thousand (Type: 0)",
            "The Earth Under Our Feet (Type: 0)",
            "War: The White Weapon (Type: 0)",
            "Soar (Type: 0)",
            "Tempus Finis (Type: 0)",
            "Vermillion Fire (Type: 0)",
        ]

    @functools.cached_property
    def songs_ff_theatrhythm(self) -> List[str]:
        return [
            "Chaos Shrine - TFF Menu Arrangememt - from FF (Theatrhythm)",
            "Return of the Warrior - TFF Menu Arrangement - from FFIII (Theatrhythm)",
            "Battle at the Big Bridge - TFF Menu Arrangement - from FFV (Theatrhythm)",
            "THEATRHYTHM FINAL FANTASY CURTAIN CALL Special Arrangmente Medley (Theatrhythm Curtain Call)",
            "Choose Your Combatants - TFFCC Menu Arrangement - from FFT (Theatrhythm Curtain Call)",
            "THEATRHYTHM FINAL FANTASY CURTAIN CALL Special Arrangement Medley(Long Version) (Theatrhythm Curtain Call)",
            "Prelude - TFFAC Menu Arrangement - from FF (Theatrhythm All-star Carnival)",
            "Matoya's Cave - TFFAC Arrangement - from FF (Theatrhythm All-star Carnival)",
            "The Red Wings - TFFAC Arrangement - from FFIV (Theatrhythm All-star Carnival)",
            "Main Theme of Final Fantasy V - TFFAC Arrangement - from FFV (Theatrhythm All-star Carnival)",
            "Battle at the Big Bridge - TFFAC Arrangement - from FFV (Theatrhythm All-star Carnival)",
            "Locke's Theme - TFFAC Arrangement - from FFVI (Theatrhythm All-star Carnival)",
            "J-E-N-O-V-A TFFAC Arrangement - from FFVII (Theatrhythm All-star Carnival)",
            "Fight With Seymour - TFFAC Arrangement - from FFX (Theatrhythm All-star Carnival)",
            "TFFCC Special Arrangement Medley - TFFAC Arrangement - From TFFAC (Theatrhythm All-star Carnival)",
            "FF7 Special Arrangement Medley - TFBL Arrangement - From FFVII (Theatrhythm Final Bar Line)",
            "THEATRHYTHM FINAL BAR LINE Special Batlte Arrangement Medley (Theatrhythm Final Bar Line)",
        ]

    @functools.cached_property
    def songs_ff_record_keeper(self) -> List[str]:
        return [
            "Chaos Shrine FFRK Ver. arrange from FFI (Record Keeper)",
            "Battle at the Big Bridge~Ver.2~ FFRK Ver. arrange (Record Keeper)",
            "The Decisive Battle FFRK Ver. arrange from FFVI (Record Keeper)",
            "The Chase FFRK Ver. arrange from FFVII (Record Keeper)",
            "The Man with the Machine Gun FFRK Ver. arrange from FFVIII (Record Keeper)",
            "Blinded by Light FFRK Ver. arrange from FFXIII (Record Keeper)",
            "Stand Your Ground FFRK Ver. arrange from FFXV (Record Keeper)",
            "UTAKATA FFRK Ver. arrange From FFTYPE-0 (Record Keeper)",
        ]

    @functools.cached_property
    def songs_ff_mobius(self) -> List[str]:
        return [
            "Warrior of Light - Mobius Final Fantasy (Mobius)",
            "Dancing Edge (Mobius)",
            "Magic Madness (Mobius)",
            "Bloodthirst (Mobius)",
            "Femme Fatale (Mobius)",
        ]

    @functools.cached_property
    def songs_ff_series(self) -> List[str]:
        return [
            "The 4 Heroes of Light (4 Heroes of Light)",
            "Battle with Monsters (4 Heroes of Light)",
            "World of Battle (World)",
            "Jack's Theme (Stranger of Paradise)",
            "Battle: Chaos Advent (Stranger of Paradise)",
            "Battle: False Knight (Stranger of Paradise)",
            "Opening Theme (Tribute Thanks)",
            "Moogles' Theme (Brass de Bravo)",
            "FF Medley (Brass de Bravo)",
            "Battle at the Big Bridge (Brass de Bravo 2)",
            "Mambo de Chocobo (Brass de Bravo 2)",
            "Dungeon Hero X's Theme (Chocobo's Dungeon)",
            "Pop-Up Duel (Chocobo's Dungeon)",
            "Leviathan Battle (Chocobo's Dungeon)",
            "Guardian of the Dark II (Chocobo's Dungeon)",
            "Raffaello Battle (Chocobo's Dungeon)",
        ]

    @functools.cached_property
    def songs_digital_deluxe(self) -> List[str]:
        return [
            "Zephyr Memories -Legend of the Eternal Wind- (3)",
            "Why (Crisis Core)",
            "Eyes On Me (8)",
            "Melodies Of Life -Final Fantasy (9)",
            "Zanarkand (10)",
            "Kuon -Memories of Waves and Light- (10-2)",
            "real Emotion (FFX-2 Mix) (10-2)",
            "Distant Worlds (11)",
            "Symphonic Poem Hope -FINAL FANTASY XII PV ver.- (12)",
            "Kiss Me Good-Bye-featured in FINAL FANTASY XII- (12)",
            "Eternal Love (13)",
            "FFCCR: Sound of the Wind (Crystal Chronicles Remastered)",
            "Zero (Type: 0)",
            "More SQ: FINAL FANTASY Dugem DE Chocobo (More SQ)",
            "SQ Chips: FINAL FANTASY III Go above the Clouds!-The Invincible (SQ Chips / 3)",
            "Clash on the Black Bridge (Final Fantasy V) (The Black Mages/ 5)",
            "Acoustic: The Decisive Battle (Acoustic / 7)",
            "Cosmo Canyon -Collab Arrangement- (Collab Title / 7)",
            "Aerith's Theme -Collab Arrangement- (Collab Title / 7)",
            "Battle SQ : FINAL FANTASY IX Not Alone (Battle SQ / 9)",
            "The Skies Above (The Black Mages 2 / 10)",
            "Fighters of the Crystal (Sanctary The Star Onions / 11)",
            "Blinded By Light Jazz Arrangement (Jazz / 13)",
            "Band:Rise (The Primals / 14)",
            "Band: A Long Fall (Scions & Sinnners / 14)",
            "Battle Theme 2 -Modulation ver.- from FINAL FANTASY II (Modulation)",
            "Battle at the Big Bridge -Modulation ver.- from FINAL FANTASY V (Modulaton)",
        ]

    @functools.cached_property
    def songs_saga_vol_1(self) -> List[str]:
        return [
            "Enraged Battle (Legend)",
            "Struggle to the Death (Legend II)",
            "The Conflict (Romancing SaGa)",
            "Horrible Shadow (Romancing SaGa)",
            "Beat Them Up! (Romancing SaGa)",
            "Coup de Grace (Romancing SaGa)",
            "Ardent Rhythm (Romancing SaGa -Minstrel Song-)",
        ]

    @functools.cached_property
    def songs_live_a_live(self) -> List[str]:
        return [
            "LIVE A LIVE (LIVE A LIVE)",
            "Birds Fly, Fish Swim (LIVE A LIVE)",
            "MEGALOMANIA (LIVE A LIVE)",
            "Go! Go! Steel Titan! (LIVE A LIVE HD-2D)",
        ]

    @functools.cached_property
    def songs_the_world_ends_with_you(self) -> List[str]:
        return [
            "Twister (The World Ends With You)",
            "Calling (The World Ends With You)",
            "Someday (The World Ends With You)",
            "Your Ocean (NEO: The World Ends With You)",
            "Breaking Free (NEO: The World Ends With You)",
            "World is Your (NEO: The World Ends With You)",
        ]

    @functools.cached_property
    def songs_nier_vol_1(self) -> List[str]:
        return [
            "Amusement Park (NieR: Automata)",
            "A Beautiful Song (NieR: Automata)",
            "Emil's Shop (NieR: Automata)",
            "Dependent Weakling (NieR: Automata)",
            "Weight of the World Kowaretasekainouta - Marina Kawano (NieR: Automata)",
        ]

    @functools.cached_property
    def songs_saga_vol_2(self) -> List[str]:
        return [
            "Battle #4 (SaGa Frontier)",
            "Alone (SaGa Frontier)",
            "Battle #5 (SaGa Frontier)",
            "T260G's Last Battle (SaGa Frontier)",
            "Feldschlat III (SaGa Frontier 2)",
            "Miβgestalt (SaGa Frontier 2)",
            "Battle Theme I (Unlimited SaGa)",
            "The Celestial Protectors (SaGa SCARLET GRACE: AMBITIONS)",
        ]

    @functools.cached_property
    def songs_nier_vol_2(self) -> List[str]:
        return [
            "Song of the Ancients / Devola (NIER)",
            "Hills of Radient Winds (NIER)",
            "Kaine / Salvation (NIER)",
            "Song of the Ancients / Fate (NIER)",
            "Shadowlord (NIER)",
            "Fleeting Words / Outsider (NieR Replicant ver 1.22474487139..)",
        ]

    @functools.cached_property
    def songs_chrono_vol_1(self) -> List[str]:
        return [
            "Chrono Trigger (CHRONO TRIGGER)",
            "Boss Battle 2 (CHRONO TRIGGER)",
            "Battle with Magus (CHRONO TRIGGER)",
            "Corridors of Time (CHRONO TRIGGER)",
            "Wings That Cross Time (CHRONO TRIGGER)",
            "Radical Dreamers -Le Trésor Interdit- (CHRONO CROSS)",
        ]

    @functools.cached_property
    def songs_chrono_vol_2(self) -> List[str]:
        return [
            "Wind Scene (CHRONO TRIGGER)",
            "Frog's Theme (CHRONO TRIGGER)",
            "Robo's Theme (CHRONO TRIGGER)",
            "World Revolution (CHRONO TRIGGER)",
            "To Far Away Times (CHRONO TRIGGER)",
            "Chrono Cross -Scars of Time- (CHRONO CROSS)",
        ]

    @functools.cached_property
    def songs_mana_vol_1(self) -> List[str]:
        return [
            "In Search of the Sword of Mana (FINAL FANTASY ADVENTURE)",
            "Battle 2 (FINAL FANTASY ADVENTURE)",
            "Swivel (TRIALS of MANA)",
            "Powell (TRIALS of MANA)",
            "Nuclear Fusion (TRIALS of MANA)",
            "Meridian Child (TRIALS of MANA)",
            "Sacrifice Part Three (TRIALS of MANA)",
        ]

    @functools.cached_property
    def songs_octopath_traveler(self) -> List[str]:
        return [
            "Octopath Traveler -Main Theme- (OCTOPATH TRAVELER)",
            "Primrose, the Dancer (OCTOPATH TRAVELER)",
            "Decisive Batlle II (OCTOPATH TRAVELER)",
            "Battle at Journey's End (OCTOPATH TRAVELER)",
            "Daughter of the Dark God (OCTOPATH TRAVELER)",
        ]

    @functools.cached_property
    def songs_saga_vol_3(self) -> List[str]:
        return [
            "Title Screen (Romancing SaGa 2)",
            "Encounter with the Seven Heroes (Romancing SaGa 2)",
            "The Ultimate Confrontation (Romancing SaGa 2)",
            "Four Sinistrals Battle I (Romancing SaGa 3)",
            "Four Sinistrals Battle II (Romancing SaGa 3)",
            "Final Confrontation (Romancing SaGa 3)",
            "Ever Higher (Romancing SaGa Re;univerSe)",
        ]

    @functools.cached_property
    def songs_mana_vol_2(self) -> List[str]:
        return [
            "Into the Thick of It (SECRET of MANA)",
            "Danger (SECRET of MANA)",
            "Meridian Dance (SECRET of MANA)",
            "Hometown of Domina (LEGEND of MANA)",
            "Darkness Nova (LEGEND of MANA)",
            "Bejeweled City in Ruins (LEGEND of MANA)",
        ]

    @functools.cached_property
    def songs_xenogears(self) -> List[str]:
        return [
            "Blazing Knights (Xenogears)",
            "Soaring (Xenogears)",
            "Awakening (Xenogears)",
        ]

    @functools.cached_property
    def songs_bravely_default(self) -> List[str]:
        return [
            "The Horizon: Endless Light and Shadow (BRAVELY DEFAULT)",
            "That of the Name (BRAVELY DEFAULT)",
            "The Evil Wings (BRAVELY DEFAULT)",
            "Uroboros, the Serpent That Devours the Horizon (BRAVELY DEFAULT)",
            "Spurred into Flight, Drenched and Fallen - The Night Rises (BRAVELY DEFAULT II)",
            "The Ones Who Gather Stars in the Night (BRAVELY DEFAULT II)",
        ]

    @functools.cached_property
    def songs_final_fantasy_16(self) -> List[str]:
        return [
            "Away (16)",
            "Hide, Hideaway (16)",
            "To Sail Forbidden Seas (16)",
            "Control (16)",
            "Find the Flame (16)",
            "No Risk, No Reward (16)",
            "Titan Lost (16)",
            "Ascension (16)",
            "The Riddle (16)",
            "Logos (16)",
            "My Star (16)",
        ]

    @functools.cached_property
    def songs_base(self) -> List[str]:
        songs: List[str] = self.songs_ff1[:]

        songs.extend(self.songs_ff2)
        songs.extend(self.songs_ff3)
        songs.extend(self.songs_ff4)
        songs.extend(self.songs_ff5)
        songs.extend(self.songs_ff6)
        songs.extend(self.songs_ff7)
        songs.extend(self.songs_ff7_series)
        songs.extend(self.songs_ff7_remake)
        songs.extend(self.songs_ff8)
        songs.extend(self.songs_ff9)
        songs.extend(self.songs_ff10)
        songs.extend(self.songs_ff10_2)
        songs.extend(self.songs_ff11)
        songs.extend(self.songs_ff12)
        songs.extend(self.songs_ff13)
        songs.extend(self.songs_ff13_series)
        songs.extend(self.songs_ff14)
        songs.extend(self.songs_ff15)
        songs.extend(self.songs_ff_mystic_quest)
        songs.extend(self.songs_ff_tactics)
        songs.extend(self.songs_ff_crystal_chronicles_series)
        songs.extend(self.songs_ff_dissidia_series)
        songs.extend(self.songs_ff_type_0)
        songs.extend(self.songs_ff_theatrhythm)
        songs.extend(self.songs_ff_record_keeper)
        songs.extend(self.songs_ff_mobius)
        songs.extend(self.songs_ff_series)

        return sorted(songs)

    def songs(self) -> List[str]:
        songs: List[str] = self.songs_base[:]

        if self.has_dlc_digital_deluxe:
            songs.extend(self.songs_digital_deluxe)
        if self.has_dlc_saga_vol_1:
            songs.extend(self.songs_saga_vol_1)
        if self.has_dlc_live_a_live:
            songs.extend(self.songs_live_a_live)
        if self.has_dlc_the_world_ends_with_you:
            songs.extend(self.songs_the_world_ends_with_you)
        if self.has_dlc_nier_vol_1:
            songs.extend(self.songs_nier_vol_1)
        if self.has_dlc_saga_vol_2:
            songs.extend(self.songs_saga_vol_2)
        if self.has_dlc_nier_vol_2:
            songs.extend(self.songs_nier_vol_2)
        if self.has_dlc_chrono_vol_1:
            songs.extend(self.songs_chrono_vol_1)
        if self.has_dlc_chrono_vol_2:
            songs.extend(self.songs_chrono_vol_2)
        if self.has_dlc_mana_vol_1:
            songs.extend(self.songs_mana_vol_1)
        if self.has_dlc_octopath_traveler:
            songs.extend(self.songs_octopath_traveler)
        if self.has_dlc_saga_vol_3:
            songs.extend(self.songs_saga_vol_3)
        if self.has_dlc_mana_vol_2:
            songs.extend(self.songs_mana_vol_2)
        if self.has_dlc_xenogears:
            songs.extend(self.songs_xenogears)
        if self.has_dlc_bravely_default:
            songs.extend(self.songs_bravely_default)
        if self.has_dlc_final_fantasy_16:
            songs.extend(self.songs_final_fantasy_16)

        return sorted(songs)

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "BASIC",
            "EXPERT",
            "ULTIMATE / SUPREME",
        ]


# Archipelago Options
class TheatrhythmFinalBarLineDLCOwned(OptionSet):
    """
    Indicates which Theatrhythm Final Bar Line DLC the player owns, if any.
    """

    display_name = "Theatrhythm Final Bar Line DLC Owned"
    valid_keys = [
        "Digital Deluxe",
        "SaGa Vol 1",
        "LIVE A LIVE",
        "The World Ends With You",
        "Nier Vol 1",
        "SaGa Vol 2",
        "NieR Vol 2",
        "CHRONO Vol 1",
        "CHRONO Vol 2",
        "Mana Vol 1",
        "OCTOPATH TRAVELER",
        "SaGa Vol 3",
        "Mana Vol 2",
        "Xenogears",
        "BRAVELY DEFAULT",
        "Final Fantasy 16",
    ]

    default = valid_keys
