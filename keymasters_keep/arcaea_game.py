from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ArcaeaArchipelagoOptions:
    arcaea_dlc_owned: ArcaeaDLCOwned


class ArcaeaGame(Game):
    name = "Arcaea"
    platform = KeymastersKeepGamePlatforms.SW

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = ArcaeaArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play SONG on DIFFICULTY difficulty",
                data={
                    "SONG": (self.songs, 1),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play SONGS on DIFFICULTY difficulty",
                data={
                    "SONGS": (self.songs, 2),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play SONGS on DIFFICULTY difficulty",
                data={
                    "SONGS": (self.songs, 3),
                    "DIFFICULTY": (self.difficulties, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete 5 Steps on a World Mode Map",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.arcaea_dlc_owned.value)

    @property
    def has_dlc_x_lanota(self) -> bool:
        return "Arcaea X Lanota" in self.dlc_owned

    @property
    def has_dlc_x_groove_coaster(self) -> bool:
        return "Arcaea X Groove Coaster" in self.dlc_owned

    @property
    def has_dlc_ephemeral_page(self) -> bool:
        return "Ephemeral Page" in self.dlc_owned

    @property
    def has_dlc_esoteric_order(self) -> bool:
        return "Esoteric Order" in self.dlc_owned

    @property
    def has_dlc_light_of_salvation(self) -> bool:
        return "Light of Salvation" in self.dlc_owned

    @property
    def has_dlc_x_wacca(self) -> bool:
        return "Arcaea x WACCA" in self.dlc_owned

    @property
    def has_dlc_muse_dash(self) -> bool:
        return "Arcaea x Muse Dash" in self.dlc_owned

    @property
    def has_dlc_binary_enfold(self) -> bool:
        return "Binary Enfold" in self.dlc_owned

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Hikari",
            "Tairitsu",
            "Kou",
            "Lethe",
            "Axium Tairitsu",
            "Ilith",
            "Shirabe",
            "Zero Hikari",
            "Fracture Hikari",
            "Ayu",
            "Saya",
            "Kanae",
            "Sia",
            "Mir",
            "Shirahime",
            "Reunion Hikari & Tairitsu",
            # Hard
            "Grievous Lady Tairitsu",
            "Tempest Tairitsu",
            "Fatalis Hikari",
        ]

    @functools.cached_property
    def characters_x_lanota(self) -> List[str]:
        return [
            "Hikari & Fisica",
        ]

    @functools.cached_property
    def characters_x_groove_coaster(self) -> List[str]:
        return [
            "Yume",
            "Hikari & Seine",
            "Linka",
        ]

    @functools.cached_property
    def characters_ephemeral_page(self) -> List[str]:
        return [
            "Alice & Tenniel",
        ]

    @functools.cached_property
    def characters_esoteric_order(self) -> List[str]:
        return [
            "Lagrange",
        ]

    @functools.cached_property
    def characters_light_of_salvation(self) -> List[str]:
        return [
            "Nami",
        ]

    @functools.cached_property
    def characters_x_wacca(self) -> List[str]:
        return [
            "Saya & Elizabeth",
            "Lily",
        ]

    @functools.cached_property
    def characters_muse_dash(self) -> List[str]:
        return [
            "Marija",
        ]

    @functools.cached_property
    def characters_binary_enfold(self) -> List[str]:
        return [
            "Vita",
            "Eto",
            "Luna",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.has_dlc_x_lanota:
            characters.extend(self.characters_x_lanota)

        if self.has_dlc_x_groove_coaster:
            characters.extend(self.characters_x_groove_coaster)

        if self.has_dlc_ephemeral_page:
            characters.extend(self.characters_ephemeral_page)

        if self.has_dlc_esoteric_order:
            characters.extend(self.characters_esoteric_order)

        if self.has_dlc_light_of_salvation:
            characters.extend(self.characters_light_of_salvation)

        if self.has_dlc_x_wacca:
            characters.extend(self.characters_x_wacca)

        if self.has_dlc_muse_dash:
            characters.extend(self.characters_muse_dash)

        if self.has_dlc_binary_enfold:
            characters.extend(self.characters_binary_enfold)

        return sorted(characters)

    @functools.cached_property
    def songs_base(self) -> List[str]:
        return [
            "[Arcaea] Fairytale",
            "[Arcaea] Harutopia ~Utopia of Spring~",
            "[Arcaea] Infinity Heaven",
            "[Arcaea] Kanagawa Cyber Culvert",
            "[Arcaea] Sayonara Hatsukoi",
            "[Arcaea] 1F√",
            "[Arcaea] Altair (feat. *spiLa*)",
            "[Arcaea] Brand new world",
            "[Arcaea] Clotho and the stargazer",
            "[Arcaea] Dandelion",
            "[Arcaea] DDD",
            "[Arcaea] Diode",
            "[Arcaea] enchanted love",
            "[Arcaea] Grimheart",
            "[Arcaea] Illegal Paradise",
            "[Arcaea] inkar-usi",
            "[Arcaea] Lapis",
            "[Arcaea] One Last Drive",
            "[Arcaea] Purgatorium",
            "[Arcaea] Rabbit in The Black Room",
            "[Arcaea] Reinvent",
            "[Arcaea] Rise",
            "[Arcaea] Snow White",
            "[Arcaea] Suomi",
            "[Arcaea] Turbocharger",
            "[Arcaea] Vexaria",
            "[Arcaea] Vivid Theory",
            "[Arcaea] Babarogue",
            "[Arcaea] Bamboo",
            "[Arcaea] BlackLotus",
            "[Arcaea] blue comet",
            "[Arcaea] Chronostasis",
            "[Arcaea] Dancin'on a Cat's Paw",
            "[Arcaea] Dement ~after legend~",
            "[Arcaea] ENERGY SYNERGY MATRIX",
            "[Arcaea] Faint Light (Arcaea Edit)",
            "[Arcaea] False Embellishment",
            "[Arcaea] GIMME DA BLOOD",
            "[Arcaea] Give Me a Nightmare",
            "[Arcaea] Ignotus",
            "[Arcaea] Life is PIANO",
            "[Arcaea] Lucifer",
            "[Arcaea] LunarOrbit -believe in the Espebranch road-",
            "[Arcaea] Nhelv",
            "[Arcaea] NULCTRL",
            "[Arcaea] oblivia",
            "[Arcaea] ReviXy",
            "[Arcaea] Rugie",
            "[Arcaea] Sakura Fubuki",
            "[Arcaea] san skia",
            "[Arcaea] Senkyou",
            "[Arcaea] Shade of Light in a Transcendent Realm",
            "[Arcaea] SUPERNOVA",
            "[Arcaea] Syro",
            "[Arcaea] Vandalism",
            "[Arcaea] VECTOЯ",
            "[Arcaea] world.execute(me);",
            "[Arcaea] Ävril-Flicka i krans-",
            "[Arcaea] Blaster",
            "[Arcaea] Bookmaker (2D Version)",
            "[Arcaea] CROSS†OVER",
            "[Arcaea] Cybernecia Catharsis",
            "[Arcaea] Dreamin' Attraction!!",
            "[Arcaea] FREEF4LL",
            "[Arcaea] Gekka (Short Version)",
            "[Arcaea] Glow",
            "[Arcaea] GOODTEK (Arcaea Edit)",
            "[Arcaea] HIVEMIND",
            "[Arcaea] init()",
            "[Arcaea] Lost Civilization",
            "[Arcaea] Monochrome Princess",
            "[Arcaea] Purple Verse",
            "[Arcaea] qualia -ideaesthesia-",
            "[Arcaea] Red and Blue",
            "[Arcaea] Redraw the Colorless World",
            "[Arcaea] Trap Crow",
            # Divided Heart
            "[Divided Heart] First Snow",
            "[Divided Heart] Blue Rose",
            "[Divided Heart] Blocked Library",
            "[Divided Heart] nέo κósmo",
            "[Divided Heart] Lightning Screw",
            # Memory Archive Base
            "[Memory Archive] Call My Name feat. Yukacco",
            "[Memory Archive] Dot to Dot feat. shully",
            "[Memory Archive] dropdead",
            "[Memory Archive] amygdata",
            "[Memory Archive] Astral tale",
            "[Memory Archive] Auxesia",
            "[Memory Archive] Avant Raze",
            "[Memory Archive] Be There",
            "[Memory Archive] carmine:scythe",
            "[Memory Archive] CROSS†SOUL",
            "[Memory Archive] DataErr0r",
            "[Memory Archive] Empire of Winter",
            "[Memory Archive] Fallensquare",
            "[Memory Archive] Feels So Right feat. Renko",
            "[Memory Archive] Impure Bird",
            "[Memory Archive] La'qryma of the Wasteland",
            "[Memory Archive] Libertas",
            "[Memory Archive] MAHOROBA",
            "[Memory Archive] Phantasia",
            "[Memory Archive] Altale",
            "[Memory Archive] BADTEK",
            "[Memory Archive] BATTLE NO.1",
            "[Memory Archive] Dreadnought",
            "[Memory Archive] Einherjar Joker",
            "[Memory Archive] Filament",
            "[Memory Archive] Galaxy Friends",
            "[Memory Archive] Heavenly caress",
            "[Memory Archive] Scarlet Cage",
            "[Memory Archive] Alexandrite",
            "[Memory Archive] IZANA",
            "[Memory Archive] Malicious Mischance",
            "[Memory Archive] Metallic Punisher",
            "[Memory Archive] Mirzam",
            "[Memory Archive] Modelista",
            "[Memory Archive] SAIKYO STRONGER",
            # Eternal Core
            "[Eternal Core] cry of viyella",
            "[Eternal Core] I've heard it said",
            "[Eternal Core] memoryfactory.lzh",
            "[Eternal Core] Relentless",
            "[Eternal Core] Lumia",
            "[Eternal Core] Essence of Twilight",
            "[Eternal Core] PRAGMATISM",
            "[Eternal Core] Sheriruth",
            "[Eternal Core] Solitary Dream",
            # Vicious Labyrinth
            "[Vicious Labyrinth] Iconoclast",
            "[Vicious Labyrinth] SOUNDWiTCH",
            "[Vicious Labyrinth] trappola bewitching",
            "[Vicious Labyrinth] conflict",
            "[Vicious Labyrinth] Axium Crisis",
            "[Vicious Labyrinth] Grievous Lady",
            # Luminous Sky
            "[Luminous Sky] Maze No.9",
            "[Luminous Sky] The Message",
            "[Luminous Sky] Sulfur",
            "[Luminous Sky] Halcyon",
            "[Luminous Sky] Ether Strike",
            "[Luminous Sky] Fracture Ray",
            # Adverse Prelude
            "[Adverse Prelude] Vindication",
            "[Adverse Prelude] Heavensdoor",
            "[Adverse Prelude] Ringed Genesis",
            "[Adverse Prelude] BLRINK",
            # Black Fate
            "[Black Fate] Equilibrium",
            "[Black Fate] Antagonism",
            "[Black Fate] Lost Desire",
            "[Black Fate] Dantalion",
            "[Black Fate] #1f1e33",
            "[Black Fate] Tempestissimo",
            "[Black Fate] Arcahv",
            # Final Verdict
            "[Final Verdict] Defection",
            "[Final Verdict] Infinite Strife,",
            "[Final Verdict] World Ender",
            "[Final Verdict] Pentiment",
            "[Final Verdict] Arcana Eden",
            "[Final Verdict] Testify",
            # Silent Answer
            "[Silent Answer] Loveless Dress",
            "[Silent Answer] Last",
            "[Silent Answer] Callima Karma",
            # Crimson Solace
            "[Crimson Solace] Paradise",
            "[Crimson Solace] Flashback",
            "[Crimson Solace] Flyburg and Endroll",
            "[Crimson Solace] Party Vinyl",
            "[Crimson Solace] Nirv lucE",
            "[Crimson Solace] GLORY：ROAD",
            # Ambivalent Vision
            "[Ambivalent Vision] Blossoms",
            "[Ambivalent Vision] Romance Wars",
            "[Ambivalent Vision] Moonheart",
            "[Ambivalent Vision] Genesis",
            "[Ambivalent Vision] Lethaeus",
            "[Ambivalent Vision] corps-sans-organes",
            # Binary Enfold
            "[Binary Enfold] next to you",
            "[Binary Enfold] Silent Rush",
            "[Binary Enfold] Strongholds",
            "[Binary Enfold] Memory Forest",
            "[Binary Enfold] Singularity",
            # Absolute Reason
            "[Absolute Reason] Antithese",
            "[Absolute Reason] Corruption",
            "[Absolute Reason] Black Territory",
            "[Absolute Reason] Vicious Heroism",
            "[Absolute Reason] Cyaegha",
            # Sunset Radiance
            "[Sunset Radiance] Chelsea",
            "[Sunset Radiance] Tie me down gently",
            "[Sunset Radiance] AI[UE]OON",
            "[Sunset Radiance] A Wandering Melody of Love",
            "[Sunset Radiance] Valhalla:0",
        ]

    @functools.cached_property
    def songs_x_lanota(self) -> List[str]:
        return [
            "[Lanota] Dream goes on",
            "[Lanota] Journey",
            "[Lanota] Prism",
            "[Lanota] Quon",
            "[Lanota] Specta",
            "[Lanota] Protoflicker",
            "[Lanota] cyanine",
            "[Lanota] Stasis",
        ]

    @functools.cached_property
    def songs_x_groove_coaster(self) -> List[str]:
        return [
            "[Groove Coaster] MERLIN",
            "[Groove Coaster] DX Choseinou Full Metal Shojo",
            "[Groove Coaster] OMAKENO Stroke",
            "[Groove Coaster] Scarlet Lance",
            "[Groove Coaster] Got hive of Ra",
            "[Groove Coaster] ouroboros -twin stroke of the end-",
            "[Groove Coaster] BUCHiGiRE Berserker",
            "[Groove Coaster] Aurgelmir",
        ]

    @functools.cached_property
    def songs_ephemeral_page(self) -> List[str]:
        return [
            "[Ephemeral Page] Beside You",
            "[Ephemeral Page] Eccentric Tale",
            "[Ephemeral Page] Alice à la mode",
            "[Ephemeral Page] Alice's Suitcase",
            "[Ephemeral Page] Jump",
            "[Ephemeral Page] Heart Jackin'",
            "[Ephemeral Page] Felis",
            "[Ephemeral Page] To: Alice Liddell",
        ]

    @functools.cached_property
    def songs_esoteric_order(self) -> List[str]:
        return [
            "[Esoteric order] Coastal Highway",
            "[Esoteric order] Paper Witch",
            "[Esoteric order] Crystal Gravity",
            "[Esoteric order] ΟΔΥΣΣΕΙΑ",
            "[Esoteric order] Far Away Light",
            "[Esoteric order] Löschen",
            "[Esoteric order] Overwhelm",
            "[Esoteric order] Aegleseeker",
        ]

    @functools.cached_property
    def songs_light_of_salvation(self) -> List[str]:
        return [
            # Memory Archive DLC 1
            "[Memory Archive] Xanatos",
            "[Memory Archive] AttraqtiA",
            "[Memory Archive] THE ULTIMACY",
            "[Memory Archive] REKKA RESONANCE",
            # Memory Archive DLC 2
            "[Memory Archive] Gengaozo",
            "[Memory Archive] Can I Friend You on Bassbook? Lol",
            "[Memory Archive] Xeraphinite",
            "[Memory Archive] Summer Fireworks of Love",
            # Esoteric Order Light of Salvation
            "[Esoteric Order] Seclusion",
            "[Esoteric Order] Small Cloud Sugar Candy",
            "[Esoteric Order] AlterAle",
            "[Esoteric Order] Divine Light of Myriad",
        ]

    @functools.cached_property
    def songs_x_wacca(self) -> List[str]:
        return [
            "[WAKKA] Quon",
            "[WAKKA] Let you DIVE! (nitro rmx)",
            "[WAKKA] with U",
            "[WAKKA] Mazy Metroplex",
            "[WAKKA] GENOCIDER",
            "[WAKKA] Sheriruth (Laur Remix)",
            "[WAKKA] eden",
            "[WAKKA] XTREME",
            "[WAKKA] Meta-Mysteria",
        ]

    @functools.cached_property
    def songs_x_muse_dash(self) -> List[str]:
        return [
            "[Muse Dash] Lights of Muse",
            "[Muse Dash] Final Step!",
            "[Muse Dash] Haze of Autumn",
            "[Muse Dash] Medusa",
        ]

    @functools.cached_property
    def songs_binary_enfold(self) -> List[str]:
        return [
            # Memory Archive DLC 3
            "[Memory Archive] Redolent Shape",
            "[Memory Archive] γuarδina",
            "[Memory Archive] Macrocosmic Modulation",
            "[Memory Archive] Kissing Lucifer",
            "[Memory Archive] NEO WINGS",
            "[Memory Archive] µ",
            "[Memory Archive] PUPA",
            "[Memory Archive] Head BONK ache",
            "[Memory Archive] INTERNET OVERDOSE",
            "[Memory Archive] PICO-Pico-Translation!",
            "[Memory Archive] Evening in Scarlet",
            "[Memory Archive] lastendconductor",
            "[Memory Archive] goldenslaughterer",
            # Shared Time
            "[Binary Enfold] Cosmica",
            "[Binary Enfold] Ascent",
            "[Binary Enfold] Live Fast Die Young",
        ]

    def songs(self) -> List[str]:
        songs: List[str] = self.songs_base[:]

        if self.has_dlc_x_lanota:
            songs.extend(self.songs_x_lanota)

        if self.has_dlc_x_groove_coaster:
            songs.extend(self.songs_x_groove_coaster)

        if self.has_dlc_ephemeral_page:
            songs.extend(self.songs_ephemeral_page)

        if self.has_dlc_esoteric_order:
            songs.extend(self.songs_esoteric_order)

        if self.has_dlc_light_of_salvation:
            songs.extend(self.songs_light_of_salvation)

        if self.has_dlc_x_wacca:
            songs.extend(self.songs_x_wacca)

        if self.has_dlc_muse_dash:
            songs.extend(self.songs_x_muse_dash)

        if self.has_dlc_binary_enfold:
            songs.extend(self.songs_binary_enfold)

        return songs

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "past",
            "present",
            "future",
        ]


# Archipelago Options
class ArcaeaDLCOwned(OptionSet):
    """
    Indicates which Arcaea DLC the player owns, if any.
    """

    display_name = "Arcaea DLC Owned"
    valid_keys = [
        "Arcaea X Lanota",
        "Arcaea X Groove Coaster",
        "Ephemeral Page",
        "Esoteric Order",
        "Light of Salvation",
        "Arcaea x WACCA",
        "Arcaea x Muse Dash",
        "Binary Enfold",
    ]

    default = valid_keys
