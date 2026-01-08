from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DJMaxRespectVArchipelagoOptions:
    djmax_respect_v_dlc_owned: DJMaxRespectVDLCOwned


class DJMaxRespectVGame(Game):
    name = "DJMax Respect V"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = DJMaxRespectVArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Position Change: POSITION  Fader: FADER  Chaos: CHAOS",
                data={
                    "POSITION": (self.position_changes, 1),
                    "FADER": (self.faders, 1),
                    "CHAOS": (self.chaos, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Get a B Rating or higher on BUTTON mode for the following song: SONG",
                data={
                    "BUTTON": (self.button_modes, 1),
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get an A Rating or higher on BUTTON mode for the following song: SONG",
                data={
                    "BUTTON": (self.button_modes, 1),
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Get an S Rating on BUTTON mode for the following song: SONG",
                data={
                    "BUTTON": (self.button_modes, 1),
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Get Max Combo on BUTTON mode for the following song: SONG",
                data={
                    "BUTTON": (self.button_modes, 1),
                    "SONG": (self.songs, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.djmax_respect_v_dlc_owned.value)

    @property
    def has_dlc_portable_3(self) -> bool:
        return "Portable 3" in self.dlc_owned

    @property
    def has_dlc_trilogy(self) -> bool:
        return "Trilogy" in self.dlc_owned

    @property
    def has_dlc_clazziquai(self) -> bool:
        return "Clazziquai" in self.dlc_owned

    @property
    def has_dlc_black_square(self) -> bool:
        return "Black Square" in self.dlc_owned

    @property
    def has_dlc_v_extension(self) -> bool:
        return "V Extension" in self.dlc_owned

    @property
    def has_dlc_v_extension_2(self) -> bool:
        return "V Extension 2" in self.dlc_owned

    @property
    def has_dlc_v_extension_3(self) -> bool:
        return "V Extension 3" in self.dlc_owned

    @property
    def has_dlc_v_extension_4(self) -> bool:
        return "V Extension 4" in self.dlc_owned

    @property
    def has_dlc_v_extension_5(self) -> bool:
        return "V Extension 5" in self.dlc_owned

    @property
    def has_dlc_v_liberty(self) -> bool:
        return "V Liberty" in self.dlc_owned

    @property
    def has_dlc_v_liberty_2(self) -> bool:
        return "V Liberty 2" in self.dlc_owned

    @property
    def has_dlc_emotional_sense(self) -> bool:
        return "Emotional Sense" in self.dlc_owned

    @property
    def has_dlc_technika(self) -> bool:
        return "Technika" in self.dlc_owned

    @property
    def has_dlc_technika_2(self) -> bool:
        return "Technika 2" in self.dlc_owned

    @property
    def has_dlc_technika_3(self) -> bool:
        return "Technika 3" in self.dlc_owned

    @property
    def has_dlc_technika_tune_q(self) -> bool:
        return "Technika Tune & Q" in self.dlc_owned

    @property
    def has_dlc_chunithm(self) -> bool:
        return "Chunithm" in self.dlc_owned

    @property
    def has_dlc_cytus(self) -> bool:
        return "Cytus" in self.dlc_owned

    @property
    def has_dlc_deemo(self) -> bool:
        return "Deemo" in self.dlc_owned

    @property
    def has_dlc_ez2on(self) -> bool:
        return "Ez2On" in self.dlc_owned

    @property
    def has_dlc_groove_coaster(self) -> bool:
        return "Groove Coaster" in self.dlc_owned

    @property
    def has_dlc_muse_dash(self) -> bool:
        return "Muse Dash" in self.dlc_owned

    @property
    def has_dlc_estimate(self) -> bool:
        return "Estimate" in self.dlc_owned

    @property
    def has_dlc_falcom(self) -> bool:
        return "Falcom" in self.dlc_owned

    @property
    def has_dlc_girls_frontline(self) -> bool:
        return "Girls' Frontline" in self.dlc_owned

    @property
    def has_dlc_maple_story(self) -> bool:
        return "Maple Story" in self.dlc_owned

    @property
    def has_dlc_nexon(self) -> bool:
        return "Nexon" in self.dlc_owned

    @property
    def has_dlc_tekken(self) -> bool:
        return "Tekken" in self.dlc_owned

    @property
    def has_dlc_clear_pass(self) -> bool:
        return "Clear Pass" in self.dlc_owned

    @functools.cached_property
    def songs_respect(self) -> List[str]:
        return [
            "2Nite",
            "Always",
            "Armored Phantom",
            "Beautiful Day",
            "Beyond Yourself",
            "Binary World",
            "BlackCat",
            "Bullet, Wanted!",
            "Child of Night",
            "Dont Die",
            "Enter the Universe",
            "Far East Princess",
            "Fly Away",
            "glory day",
            "Groovin Up",
            "Heavenly",
            "KILLER BEE",
            "Kung Brother",
            "Liar",
            "Lift You Up",
            "Mulch",
            "NB RANGER - Virgin Force",
            "Only for You",
            "OPEN FIRE",
            "Over Your Dream",
            "quixotic",
            "Remains Of Doom",
            "Royal Clown",
            "Runaway",
            "Running girl",
            "Rutin (GOTH Wild Electro Remix)",
            "Secret Dejavu",
            "Shadow Flower",
            "Soar ~Stay With Me~",
            "The Feelings",
            "The Lost Story",
            "The Obliterator",
            "Tok! Tok! Tok!",
            "U.A.D",
            "v o l d e n u i t",
            "Void",
            "waiting for me",
            "Waiting for you",
            "Were All Gonna Die",
            "WHY",
        ]

    @functools.cached_property
    def songs_respect_v(self) -> List[str]:
        return [
            "Airlock",
            "Alone (Marshmello)",
            "Alone (Nauts)",
            "Angelic Tears",
            "Aurora Borealis",
            "Bleed",
            "BlueWhite",
            "Boom!",
            "Can We Talk (Broken Dog Leg Mix)",
            "Celestial Tears",
            "Chemical Slave",
            "comet",
            "Dance of the Dead",
            "Dancin Planet",
            "Dark Lightning",
            "Daylight",
            "Flowering",
            "From Hell to Breakfast",
            "Get Jinxed",
            "Ghost Voices",
            "Grid System",
            "I want You ~Twinkle Twinkle Sunshine~",
            "IM ALIVE",
            "Kamui",
            "Karma",
            "Kingdom",
            "Mozart Symphony No. 40 1st Mvt.",
            "Mr. Lonely",
            "Neon 1989 (ESTi REmix)",
            "OrBiTal",
            "POP/STARS",
            "Relation Again (ESTis Remix)",
            "RockSTAR",
            "Sad Machine",
            "So Happy",
            "SOUL LADY",
            "SURVIVOR",
            "To Be With You",
            "Watch Your Step",
        ]

    @functools.cached_property
    def songs_portable_1(self) -> List[str]:
        return [
            "A.I",
            "Ask to Wind",
            "Ask to Wind ~Live Mix~",
            "Astro Fight",
            "BlythE",
            "Bright Dream",
            "Can We Talk",
            "Catch Me",
            "Chrono Breakers",
            "CnP",
            "Dreadnought",
            "Elastic STAR",
            "End of the Moonlight",
            "Enemy Storm",
            "Eternal Memory",
            "Every Morning",
            "Extreme Z4",
            "FEAR",
            "Fever GJ",
            "FTR",
            "Funky Chups",
            "Futurism",
            "HAMSIM",
            "JBG",
            "Jupiter Driving",
            "KUDA",
            "Lemonade",
            "Lets Go Baby",
            "Light House",
            "Long Vacation",
            "Luv Flow",
            "MASAI",
            "Memory of Beach",
            "Minimal Life",
            "NB RANGER",
            "Never Say",
            "OBLIVION",
            "OBLIVION ~Rockin Night Style~",
            "ON",
            "One the Love",
            "Out Law",
            "Para-Q",
            "Piano Concerto No. 1",
            "Ray of Illuminati",
            "RED",
            "REVENGE",
            "Road Of Death",
            "Rock Or Die",
            "Save My Dream",
            "SIN",
            "SIN ~The Last Scene~",
            "Sunny Side",
            "Sunny Side ~Deepn Soul Mix~",
            "Temptation",
            "Triple Zoe",
            "Ya! Party!",
        ]

    @functools.cached_property
    def songs_portable_2(self) -> List[str]:
        return [
            "A Lie",
            "Another DAY",
            "Brain Storm",
            "Brandnew Days",
            "Brave it Out",
            "Bye Bye Love",
            "Chain of Gravity",
            "Cherokee",
            "DIVINE SERVICE",
            "Dream of You",
            "Fallen Angel",
            "Fentanest",
            "For Seasons",
            "For the IKARUS",
            "Get on Top",
            "GET OUT",
            "Good Bye",
            "Heart Beat",
            "Hello Pinky",
            "Higher",
            "Ladymade Star",
            "Lost nfound",
            "Memoirs",
            "Mess it Up",
            "Midnight Blood",
            "Miles",
            "Minus 3",
            "My Alias",
            "NANO RISK",
            "NB POWER",
            "NB Rangers -Returns-",
            "Negative Nature",
            "Nightmare",
            "Phantom Of Sky",
            "plastic method",
            "Right Now",
            "Rocka-a-doodle-doo",
            "Rolling On the Duck",
            "Seeker",
            "Showtime",
            "Smoky Quartz",
            "sO mUCH iN LUV",
            "SQUEEZE",
            "STALKER",
            "StarFish",
            "Stay with Me",
            "Sunset Rider",
            "Syriana",
            "Taekwonburi",
            "WhiteBlue",
            "Yellowberry -AJ Mix-",
            "Yo Creo Que Si",
            "Your Own Miracle",
        ]

    @functools.cached_property
    def songs_guilty_gear(self) -> List[str]:
        return [
            "Break a Spell",
            "Holy Orders (Be Just Or Be Dead)",
            "Marionette",
        ]

    def songs_base(self) -> List[str]:
        return sorted(
            self.songs_respect
            + self.songs_respect_v
            + self.songs_portable_1
            + self.songs_portable_2
            + self.songs_guilty_gear
        )

    @functools.cached_property
    def songs_portable_3(self) -> List[str]:
        return [
            "Become Myself",
            "Break!",
            "Desperado ~Nu Skool Mix~",
            "Enemy Storm ~Dark Jungle Mix~",
            "Everything",
            "glory day (Minotorment Remix)",
            "glory day -JHS Remix-",
            "Gone Astray",
            "Hanz up!",
            "IF",
            "Leave me alone",
            "Luv Flow ~Funky House Mix~",
            "Luv is True",
            "MASAI ~Electro House Mix~",
            "Mellow D Fantasy",
            "NB Ranger Nonstop Remix",
            "Out Law Reborn",
            "Raise me up",
            "Season (Warm Mix)",
            "SuperSonic ~Mr. Funky Dirty Planet Remix ~",
            "The Rain Maker",
            "Waiting for the Sun",
            "Your Smile",
            "ZET ~Mr. Funky Remix~",
        ]

    @functools.cached_property
    def songs_trilogy(self) -> List[str]:
        return [
            "A Lie ~Deep Inside Mix~",
            "Bye Bye Love ~Nu Jazz Mix~",
            "Catch You",
            "For Seasons ~Air Guitar Mix~",
            "GET OUT ~Hip Noodle Mix~",
            "Memory of Wind",
            "Mind Control",
            "My Jealousy",
            "NB Girls",
            "Nevermind",
            "sO mUCH iN LUV ~Melodic Twister Mix~",
            "Someday",
            "STOP",
            "Streetlight",
            "Syriana ~Blast Wave Mix~",
            "Talk! Talk!",
            "The One",
            "Ventilator",
            "Yo Creo Que Si ~Live House Version~",
            "Your Own Miracle ~Disco House Mix~",
            "ZET",
        ]

    @functools.cached_property
    def songs_clazziquai(self) -> List[str]:
        return [
            "Closer",
            "Coastal Tempo",
            "Color",
            "Come to me",
            "Creator",
            "DARK ENVY",
            "Electronics",
            "Fate",
            "First Kiss",
            "Flea",
            "Forever",
            "Freedom",
            "Here in the Moment",
            "Here in the Moment ~Extended Mix~",
            "In My Heart",
            "Love Mode",
            "Lover (CE Style)",
            "Proposed, Flower, Wolf",
            "Rising The Sonic",
            "Tell Me",
            "The Clear Blue Sky",
            "The Night Stage",
            "To You",
            "Urban Night (hYO)",
            "Y (CE Style)",
        ]

    @functools.cached_property
    def songs_black_square(self) -> List[str]:
        return [
            "Airwave ~Extended Mix~",
            "ANALYS",
            "Beat U Down",
            "Colours of Sorrow",
            "Cypher Gate",
            "Desperado",
            "Fermion",
            "Fever Pitch Girl",
            "Get Down",
            "Grave Consequence",
            "Heart of Witch",
            "In my Dream",
            "Jealousy",
            "Keys to the World",
            "Lovely hands",
            "Lover (BS Style)",
            "PDM",
            "Proposed, Flower, Wolf part. 2",
            "Ready Now",
            "Rutin",
            "Secret World",
            "Y (BS Style)",
        ]

    @functools.cached_property
    def songs_v_extension(self) -> List[str]:
        return [
            "Attack",
            "BLACK GOLD",
            "Do it",
            "Dream it",
            "Fancy Night",
            "FIGHT NIGHT (feat. Calyae)",
            "Kensei",
            "Lisrim",
            "Lost Serenity",
            "Lost Temple",
            "Maharajah -fenomeno edition-",
            "Misty ErA",
            "Move Yourself",
            "NANAIRO",
            "Never Die",
            "Remember Me",
            "Space Challenger",
            "Vile Requiem",
            "welcome to the space (feat. Jisun)",
            "WONDER $LOT 777",
        ]

    @functools.cached_property
    def songs_v_extension_2(self) -> List[str]:
        return [
            "Arcade Love",
            "Chrysanthemum",
            "Cocked Pistol",
            "Daydream",
            "FALLING IN LOVE",
            "Flowering ~Original Ver.~",
            "Forgotten",
            "Ive got a feeling",
            "Imaginary dance",
            "Melonaid",
            "Memories of dreams",
            "Never let you go",
            "Odysseus",
            "Over Me",
            "Red Eyes",
            "Sweet On You",
            "Underwater Castle",
            "Vertical Floating",
            "Voyage (SOPHI)",
            "Wont back Down",
            "Zero to the hunnit",
        ]

    @functools.cached_property
    def songs_v_extension_3(self) -> List[str]:
        return [
            "#mine (feat. Riho Iwamoto)",
            "Bambi - DJMAX Edit -",
            "Bright Future",
            "Charming World",
            "Disappearing Act",
            "Emerge",
            "Every Day ~ Every Night",
            "Fundamental",
            "KICK IT",
            "Misty Era Mui",
            "Moment (feat. Nauts)",
            "NB RANGERS - Destiny",
            "Plasma Sphere",
            "Secret",
            "Set Me Free",
            "Space Dream (feat. J.O.Y)",
            "STEP",
            "Tic! Tac! Toe!",
            "Winners",
            "Zero-Break",
        ]

    @functools.cached_property
    def songs_v_extension_4(self) -> List[str]:
        return [
            "!!New Game Start!!",
            "ADDICT!ON (DJMAX Edit)",
            "Back to the oldschool",
            "Deadly Bomber",
            "DIE IN",
            "Dont Cry",
            "Gloxinia",
            "Hello",
            "Hyper Drive",
            "Hypernaid",
            "Karma ~Original Ver.~",
            "Like a Fool",
            "Love.Game.Money",
            "LUV",
            "New World",
            "Stay Alive",
            "Stolen Memory",
            "The Four Seasons  Summer 2017",
            "To Where You Are",
            "Vertical Eclipse",
            "Weaponize",
        ]

    @functools.cached_property
    def songs_v_extension_5(self) -> List[str]:
        return [
            "3 33",
            "Accelerate",
            "Behemoth",
            "Carrot Carrot",
            "Critical Point",
            "ECiLA",
            "glory MAX -to the MAXimum-",
            "God Machine",
            "Inside the Light",
            "My Wonderland",
            "Over the Starlight",
            "Paradise",
            "Peac Comes At a Price",
            "Pitter-patter",
            "Revenger",
            "Rhapsody for the VEndetta",
            "Right Time",
            "Rocket Launcher",
            "S.A.V.E",
            "Shining Light (fest. Shabel Tonya)",
        ]

    @functools.cached_property
    def songs_v_liberty(self) -> List[str]:
        return [
            "Away",
            "Basement",
            "Bestie",
            "Break Out",
            "Broken Sphere",
            "Cold Generation",
            "Confessions in Another World ~Pan Remix~",
            "Cotton Candy Soda",
            "Diomedes",
            "Final Hour (Game Ver.)",
            "Final Round",
            "Follow Me",
            "Growing Pains [ScreaM Records]",
            "Licrom",
            "Omen",
            "Petunia",
            "Rhythm In My Head",
            "Song For You",
            "Synchronize",
            "TRAP",
        ]

    @functools.cached_property
    def songs_v_liberty_2(self) -> List[str]:
        return [
            "1! 2! 3! 4! Streaming rn CHU!",
            "B!G_BANG CHALLENGE",
            "break it down!",
            "Cata (feat. NC.A)",
            "Cheonmasan",
            "Delusion (fet. SOONHO)",
            "ELIXIR",
            "Hikari (feat. Negoto Bunnyla)",
            "Kakera",
            "Krush",
            "Love or Die",
            "Mad (feat. WaMi)",
            "MADNESS (feat. U1)",
            "Misty Er'A ~One Day~",
            "Outcast (feat. BIRA)",
            "Pull The Trigger",
            "RIPPER",
            "Rocket Ride",
            "Saga Script",
            "TOXIC (feat. Shabel Tonya)",
        ]

    @functools.cached_property
    def songs_emotional_sense(self) -> List[str]:
        return [
            "Cosmic Elevator",
            "Feel (DJ Mocha)",
            "Knowledge System",
            "Real Over Drive",
            "Space of Soul",
            "Super lovely",
            "Urban Night (Electronic Boutique)",
            "Yo! Max!",
        ]

    @functools.cached_property
    def songs_technika(self) -> List[str]:
        return [
            "Access",
            "Area 7",
            "Beyond the Future",
            "Dear my Lady",
            "DJMAX",
            "Do you want it",
            "Fury",
            "HEXAD",
            "Honeymoon",
            "I want You",
            "Landscape",
            "Melody",
            "Play the Future",
            "Remember",
            "Shoreline",
            "SON OF SUN",
            "SON OF SUN ~Extended Mix~",
            "SuperSonic",
            "Sweet Shining Shooting Star",
            "The Last Dance",
            "Thor",
            "Voyage  (makou)",
        ]

    @functools.cached_property
    def songs_technika_2(self) -> List[str]:
        return [
            "Airwave",
            "BEE-U-TIFUL",
            "Burn it Down",
            "Cosmic Fantastic Lovesong",
            "Cozy Quilt",
            "D2",
            "Dream of Winds",
            "Dual Strikers",
            "End of Mythology",
            "Eternal Fantasy",
            "La Campanella Nu Rave",
            "Love is Beautiful",
            "MonoXide",
            "Nova ~Mr. Funky Remix~",
            "Put Em Up",
            "Puzzler",
            "Rage Of Demon",
            "Say it from your heart",
            "Sweet Dream",
            "The Guilty",
            "Thor ~Extended Mix~",
            "Trip",
            "XLASHER",
            "Y ~Extended Mix~",
        ]

    @functools.cached_property
    def songs_technika_3(self) -> List[str]:
        return [
            "A Life With You",
            "AD2222",
            "AD2222 ~Extended Mix~",
            "ALiCE",
            "Angel",
            "Bamboo on Bamboo",
            "Black Swan",
            "Dark Prism",
            "Dream Again",
            "EGG",
            "EGG ~Extended Mix~",
            "Emblem",
            "Fallin in LUV",
            "Feel Ma Beat",
            "Ghost",
            "Give Me 5",
            "Heart Beat Part. 2",
            "Kung-Fu Rider",
            "My Heart, My Soul",
            "Now a NEW Day",
            "Out of CTRL",
            "Over the Rainbow",
            "Right Back",
            "Showdown (LeeZu)",
            "SigNalize",
            "Supernova",
            "Supersonic 2011",
            "Wanna Be Your Lover",
            "Xeus",
            "You & Me",
        ]

    @functools.cached_property
    def songs_technika_tune_q(self) -> List[str]:
        return [
            "A Song of Sixpence",
            "Back to Life",
            "Deborah",
            "Eternal Fantasy (Miya Vocal Mix)",
            "Festa Nova",
            "Kal_wrnw",
            "LovePanic",
            "Luv Yourself",
            "Mukilteo Beach",
            "Never Ending TECHNIKA",
            "Renovation",
            "Retention",
            "Shining My Boy",
            "Silent Clarity",
            "Starlight Garden",
            "Take on Me",
            "Techno Racer",
            "The MAX",
            "Thor (Deepin Absonant Mix)",
            "VORTEX",
        ]

    @functools.cached_property
    def songs_chunithm(self) -> List[str]:
        return [
            "Cyberozar",
            "Garakuta Doll Play",
            "Ikazuchi",
            "Ray Tuning",
            "The wheel to the right",
            "Trrricksters!!",
        ]

    @functools.cached_property
    def songs_cytus(self) -> List[str]:
        return [
            "AXION",
            "CODE NAME ZERO",
            "conflict",
            "EMber",
            "Entrance",
            "L",
            "Les Parfums de LAmour",
            "Mammal",
            "Myosotis",
            "Old Gold",
            "Shoot out",
            "Ververg",
        ]

    @functools.cached_property
    def songs_deemo(self) -> List[str]:
        return [
            "Angelic Sphere",
            "ANiMA",
            "Dream",
            "Legacy",
            "Magnolia",
            "Nine point eight",
            "Sairai",
            "Undo",
            "Utopiosphere",
            "YUBIKIRI-GENMAN",
        ]

    @functools.cached_property
    def songs_ez2on(self) -> List[str]:
        return [
            "A Site De La Rue",
            "Appeal",
            "Aquaris",
            "Back for more",
            "Complex",
            "Envy Mask",
            "Feel (Kang Eun Soo / eridanus)",
            "Lie Lie",
            "LIMBO",
            "Look out ~Here comes my love~",
            "Metagalactic",
            "Nihilism",
            "Sand Storm",
            "Showdown (Andy Lee)",
            "Sparrow",
            "Stay",
            "Weird Wave",
            "Zeroize",
        ]

    @functools.cached_property
    def songs_groove_coaster(self) -> List[str]:
        return [
            "Black MInD",
            "Good Night, Bad Luck.",
            "Got more raves?",
            "Groove Prayer",
            "HB-axeleration",
            "Marry me, Nightmare",
            "ouroboros -twin stroke of the end-",
            "OVER THE NIGHT",
            "Satisfaction",
            "Warrior",
        ]

    @functools.cached_property
    def songs_muse_dash(self) -> List[str]:
        return [
            "Bang!!",
            "can you feel it",
            "Comet Coaster",
            "Cthugha",
            "DataErr0r",
            "Dysthymia",
            "ENERGY SYNERGY MATRIX",
            "Koi no Moonlight",
            "Lights of Muse",
            "MUSEDASH!!!!",
            "Pancake is Love",
            "PUPA",
            "tape/stop/night",
            "The 90s Decision",
            "XING",
        ]

    @functools.cached_property
    def songs_estimate(self) -> List[str]:
        return [
            "HELIX",
            "In My Heart ~EsTi Remix~",
            "Obelisque",
            "pit-a-pet",
            "U-NIVUS",
        ]

    @functools.cached_property
    def songs_falcom(self) -> List[str]:
        return [
            "Ashita e no Koudou",
            "Blue Destination",
            "GENESIS BEYOND THE BEGINNING",
            "Inevitable Struggle",
            "NORSE WIND",
            "Silver Will",
            "STEP AHEAD",
            "SUNSHINE COASTLINE",
            "TO MAKE THE END OF BATTLE",
            "To the Future.",
        ]

    @functools.cached_property
    def songs_girls_frontline(self) -> List[str]:
        return [
            "Barbarous Funera",
            "Frontline",
            "What am I fighting for?",
        ]

    @functools.cached_property
    def songs_maple_story(self) -> List[str]:
        return [
            "Ariant ~ned Remix~",
            "Catch Your Dreams!",
            "Dynamic Universe",
            "Fairytale ~Pan Remix~",
            "Frozen Link",
            "Leafre (EDM ver.)",
            "Missing You ~SOPHI Remix~",
            "Moonlight Shadow ~Paul Bazooka Remix~",
            "Smile",
            "Star Bubble",
            "Story of Maple",
            "Temple of Time (EDM ver.)",
            "The Lake of Oblivion ~jam-jam Remix~",
            "The Tune of the Azure Light ~Parang Remix~",
            "Where Stars Rest",
        ]

    @functools.cached_property
    def songs_nexon(self) -> List[str]:
        return [
            "Alliance x Empire",
            "An old story from Grandma",
            "Apparition",
            "Buyeo Fortress ~Blosso Remix~",
            "Constant Moderato",
            "Cromm Cruaich",
            "Its my war now",
            "Kartrider Mashup ~Cosmograph Remix~",
            "Kartrider Mashup ~Pure 100% Remix~",
            "Kartrider, Crazyarcade, Bubblefighter Main theme ~CHUCK Remix~",
            "Lacheln, The City of Dreams",
            "Lugh Lamhfada",
            "Reminiscence",
            "Start The Adventure ~SOPHI Remix~",
            "Tayberrs - Collapsed Paradise",
            "The Final Dance",
            "The Little Adventurer",
            "The Raindrop Flower ~jam-jam Remix~",
            "The Siege warfare ~Pierre Blanche, Yonce Remix~",
            "Where Legend Begin ~VoidRover Remix~",
            "Young Adventurer ~SiNA Remix~",
        ]

    @functools.cached_property
    def songs_tekken(self) -> List[str]:
        return [
            "Empty Your Mind 1st",
            "Equator Line 1st",
            "Fiji -Paraiso Mix- (Eternal Paradise)",
            "Heat Haze Shadow",
            "Kitsch",
            "Moonlit Wilderness",
            "Moonsiders 1st",
            "My Last Stand",
            "Poolside",
            "Tekken Tag Tournament Piano Intro -Massive True Mix-",
            "The Decisive Blow (Normal)",
            "Yodeling in meadow hill (Hidden Retreat)",
        ]

    @functools.cached_property
    def songs_clear_pass(self) -> List[str]:
        return [
            "Re:BIRTH",
            "Insane Drift",
            "Kill Trap",
        ]

    def songs(self) -> List[str]:
        songs: List[str] = self.songs_base()

        if self.has_dlc_portable_3:
            songs.extend(self.songs_portable_3)
        if self.has_dlc_trilogy:
            songs.extend(self.songs_trilogy)
        if self.has_dlc_clazziquai:
            songs.extend(self.songs_clazziquai)
        if self.has_dlc_black_square:
            songs.extend(self.songs_black_square)
        if self.has_dlc_v_extension:
            songs.extend(self.songs_v_extension)
        if self.has_dlc_v_extension_2:
            songs.extend(self.songs_v_extension_2)
        if self.has_dlc_v_extension_3:
            songs.extend(self.songs_v_extension_3)
        if self.has_dlc_v_extension_4:
            songs.extend(self.songs_v_extension_4)
        if self.has_dlc_v_extension_5:
            songs.extend(self.songs_v_extension_5)
        if self.has_dlc_v_liberty:
            songs.extend(self.songs_v_liberty)
        if self.has_dlc_v_liberty_2:
            songs.extend(self.songs_v_liberty_2)
        if self.has_dlc_emotional_sense:
            songs.extend(self.songs_emotional_sense)
        if self.has_dlc_technika:
            songs.extend(self.songs_technika)
        if self.has_dlc_technika_2:
            songs.extend(self.songs_technika_2)
        if self.has_dlc_technika_3:
            songs.extend(self.songs_technika_3)
        if self.has_dlc_technika_tune_q:
            songs.extend(self.songs_technika_tune_q)
        if self.has_dlc_chunithm:
            songs.extend(self.songs_chunithm)
        if self.has_dlc_cytus:
            songs.extend(self.songs_cytus)
        if self.has_dlc_deemo:
            songs.extend(self.songs_deemo)
        if self.has_dlc_ez2on:
            songs.extend(self.songs_ez2on)
        if self.has_dlc_groove_coaster:
            songs.extend(self.songs_groove_coaster)
        if self.has_dlc_muse_dash:
            songs.extend(self.songs_muse_dash)
        if self.has_dlc_estimate:
            songs.extend(self.songs_estimate)
        if self.has_dlc_falcom:
            songs.extend(self.songs_falcom)
        if self.has_dlc_girls_frontline:
            songs.extend(self.songs_girls_frontline)
        if self.has_dlc_maple_story:
            songs.extend(self.songs_maple_story)
        if self.has_dlc_nexon:
            songs.extend(self.songs_nexon)
        if self.has_dlc_tekken:
            songs.extend(self.songs_tekken)
        if self.has_dlc_clear_pass:
            songs.extend(self.songs_clear_pass)

        return sorted(songs)

    @staticmethod
    def button_modes() -> List[str]:
        return [
            "4B",
            "5B",
            "6B",
            "8B",
        ]

    @staticmethod
    def position_changes() -> List[str]:
        return [
            "Off",
            "Random",
            "Half Random",
            "Max Random",
            "Mirror",
            "Mirror Half Random",
        ]

    @staticmethod
    def faders() -> List[str]:
        return [
            "Off",
            "Fade In",
            "Fade In 2",
            "Fade Out",
            "Fade Out 2",
            "Blink",
            "Blink 2",
            "Fog",
            "Pixel",
            "Pixel 2",
            "Blind",
        ]

    @staticmethod
    def chaos() -> List[str]:
        return [
            "Off",
            "Chaos W",
            "Slide Up",
            "Slide Down",
            "Reverse",
            "Chaos X",
        ]


# Archipelago Options
class DJMaxRespectVDLCOwned(OptionSet):
    """
    Indicates which DJMax Respect V DLC the player owns, if any.
    """

    display_name = "DJMax Respect V DLC Owned"
    valid_keys = [
        "Portable 3",
        "Trilogy",
        "Clazziquai",
        "Black Square",
        "V Extension",
        "V Extension 2",
        "V Extension 3",
        "V Extension 4",
        "V Extension 5",
        "V Liberty",
        "V Liberty 2",
        "Emotional Sense",
        "Technika",
        "Technika 2",
        "Technika 3",
        "Technika Tune & Q",
        "Chunithm",
        "Cytus",
        "Deemo",
        "Ez2On",
        "Groove Coaster",
        "Muse Dash",
        "Estimate",
        "Falcom",
        "Girls' Frontline",
        "Maple Story",
        "Nexon",
        "Tekken",
        "Clear Pass",
    ]

    default = valid_keys
