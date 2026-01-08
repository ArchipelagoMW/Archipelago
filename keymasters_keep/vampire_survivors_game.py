from __future__ import annotations

import functools
from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class VampireSurvivorsArchipelagoOptions:
    vampire_survivors_dlc_owned: VampireSurvivorsDLCOwned
    vampire_survivors_allow_secret_characters: VampireSurvivorsAllowSecretCharacters


class VampireSurvivorsGame(Game):
    name = "Vampire Survivors"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
        KeymastersKeepGamePlatforms.IOS,
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = VampireSurvivorsArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Deactivate the following PowerUps: POWERUPS",
                data={
                    "POWERUPS": (self.powerups, 5),
                },
            ),
            GameObjectiveTemplate(
                label="Maximum Weapons: WEAPONS.  Golden Eggs: GOLDEN_EGGS",
                data={
                    "WEAPONS": (self.maximum_weapon_range, 1),
                    "GOLDEN_EGGS": (self.off_on, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Play in Inverse Mode",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Clear STAGE as CHARACTER. Hyper: HYPER  Arcanas: ARCANAS  Limit Break: LIMIT_BREAK",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                    "HYPER": (self.off_on, 1),
                    "ARCANAS": (self.off_on, 1),
                    "LIMIT_BREAK": (self.off_on, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Clear STAGE using WEAPONS",
                data={
                    "STAGE": (self.stages, 1),
                    "WEAPONS": (self.base_weapons, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear STAGE without using WEAPONS",
                data={
                    "STAGE": (self.stages, 1),
                    "WEAPONS": (self.base_weapons, 5),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear STAGE as CHARACTER. Must select any PASSIVES offered",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                    "PASSIVES": (self.passive_items, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear STAGE as CHARACTER. Cannot select PASSIVES",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.characters, 1),
                    "PASSIVES": (self.passive_items, 5),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Obtain WEAPON through evolution / union",
                data={
                    "WEAPON": (self.evolution_union_weapons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

        if self.has_dlc_ode_to_castlevania:
            templates.append(
                GameObjectiveTemplate(
                    label="Obtain FAMILIAR from the Familiar Forge",
                    data={
                        "FAMILIAR": (self.familiars, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                )
            )

        return templates

    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.vampire_survivors_dlc_owned.value

    @property
    def has_dlc_legacy_of_moonspell(self) -> bool:
        return "Legacy of Moonspell" in self.dlc_owned

    @property
    def has_dlc_tides_of_foscari(self) -> bool:
        return "Tides of Foscari" in self.dlc_owned

    @property
    def has_dlc_emergency_meeting(self) -> bool:
        return "Emergency Meeting" in self.dlc_owned

    @property
    def has_dlc_operation_guns(self) -> bool:
        return "Operation Guns" in self.dlc_owned

    @property
    def has_dlc_ode_to_castlevania(self) -> bool:
        return "Ode to Castlevania" in self.dlc_owned

    @staticmethod
    def powerups() -> List[str]:
        return [
           "Amount",
           "Area",
           "Armor",
           "Charm",
           "Cooldown",
           "Curse",
           "Defang",
           "Duration",
           "Greed",
           "Growth",
           "Luck",
           "Magnet",
           "Max Health",
           "Might",
           "Move Speed",
           "Omni",
           "Recovery",
           "Revival",
           "Speed",
        ]

    @staticmethod
    def maximum_weapon_range() -> range:
        return range(4, 6)

    @staticmethod
    def off_on() -> List[str]:
        return [
            "Off",
            "On",
        ]

    @functools.cached_property
    def characters_base(self) -> List[str]:
        return [
            "Antonio Belpaese",
            "Arca Ladonna",
            "Bat Robbert",
            "Bianca Ramba",
            "Christine Davain",
            "Concetta Caciotta",
            "Divano Thelma",
            "Dommario",
            "Gennaro Belpaese",
            "Giovanna Grana",
            "Iguana Gallo Valletto",
            "Imelda Belpaese",
            "Krochi Freetto",
            "Lama Ladonna",
            "Mortaccio",
            "O'Sole Meeo",
            "Pasqualina Belpaese",
            "Poe Ratcho",
            "Poppea Pecorina",
            "Porta Ladonna",
            "Pugnala Provola",
            "Queen Sigma",
            "Santa Ladonna",
            "She-Moon",
            "Sir Ambrojoe",
            "Space Dude",
            "Suor Clerici",
            "Yatta Cavallo",
            "Zi'Assunta Belpaese",
        ]

    @functools.cached_property
    def characters_legacy_of_moonspell(self) -> List[str]:
        return [
            "Babi-Onna",
            "Gav'Et-Oni",
            "McCoy-Oni",
            "Megalo Menya Moonspell",
            "Megalo Syuuto Moonspell",
            "Menya Moonspell",
            "Miang Moonspell",
            "Syuuto Moonspell",
        ]

    @functools.cached_property
    def characters_tides_of_foscari(self) -> List[str]:
        return [
            "Eleanor Uziron",
            "Genevieve Gruyère",
            "Je-Ne-Viv",
            "Keitha Muort",
            "Luminaire Foscari",
            "Maruto Cuts",
            "Rottin'Ghoul",
            "Sammy",
        ]

    @functools.cached_property
    def characters_emergency_meeting(self) -> List[str]:
        return [
            "Crewmate Dino",
            "Engineer Gino",
            "Ghost Lino",
            "Guardian Pina",
            "Horse",
            "Impostor Rina",
            "Megalo Impostor Rina",
            "Scientist Mina",
            "Shapeshifter Nino",
        ]

    @functools.cached_property
    def characters_operation_guns(self) -> List[str]:
        return [
            "Ariana",
            "Bill Rizer",
            "Brad Fang",
            "Browny",
            "Colonel Bahamut",
            "Lance Bean",
            "Lucia Zero",
            "Newt Plissken",
            "Probotector",
            "Sheena Etranzi",
            "Simondo Belmont",
            "Stanley",
        ]

    @functools.cached_property
    def characters_ode_to_castlevania(self) -> List[str]:
        return [
            "Albus",
            "Alucard",
            "Barlowe",
            "Carrie Fernandez",
            "Charlotte Aulin",
            "Christopher Belmont",
            "Cornell",
            "Elizabeth Bartley",
            "Eric Lecarde",
            "Grant Danasty",
            "Hector",
            "Henry",
            "Isaac",
            "John Morris",
            "Jonathan Morris",
            "Julia Laforeze",
            "Julius Belmont",
            "Juste Belmont",
            "Leon Belmont",
            "Lisa Tepes",
            "Maria Renard",
            "Maxim Kischine",
            "Mina Hakuba",
            "Nathan Graves",
            "Quincy Morris",
            "Reinhardt Schneider",
            "Richter Belmont",
            "Rinaldo Gandolfi",
            "Saint Germain",
            "Sara Trantoul",
            "Shaft",
            "Shanoa",
            "Simon Belmont",
            "Soma Cruz",
            "Sonia Belmont",
            "Sypha Belnades",
            "Trevor Belmont",
            "Vincent Dorin",
            "Vlad Tepes Dracula",
            "Yoko Belnades",
        ]

    @functools.cached_property
    def characters_secret_base(self) -> List[str]:
        return [
            "Avatar Infernas",
            "Bats Bats Bats",
            "Big Trouser",
            "Boon Marrabbio",
            "Cosmo Pavone",
            "Exdash Exiviiq",
            "Gains Boros",
            "Gyoruntin",
            "Gyorunton",
            "Leda",
            "Mask of the Red Death",
            "Minnah Mannarah",
            "missingN▯",
            "Peppino",
            "Random",
            "Rose De Infernas",
            "Scorej-Oni",
            "Smith IV",
            "Toastie",
        ]

    @functools.cached_property
    def characters_secret_ode_to_castlevania(self) -> List[str]:
        return [
            "Alamaric Sniper",
            "Axe Armor",
            "Blackmore",
            "Blue Crescent Moon Cornell",
            "Brauner",
            "Carmilla",
            "Cave Troll",
            "Celia Fortner",
            "Chaos",
            "Count Olrox",
            "Dario Bossi",
            "Death",
            "Dmitrii Blinov",
            "Familiar",
            "Ferryman",
            "Fleaman",
            "Frozenshade",
            "Galamoth",
            "Graham Jones",
            "Hammer",
            "Innocent Devil",
            "Joachim Armster",
            "Keremet",
            "Loretta & Stella Lecarde",
            "Loretta Lecarde",
            "Malphas",
            "Master Librarian",
            "Megalo Death",
            "Megalo Dracula",
            "Megalo Elizabeth Bartley",
            "Megalo Olrox",
            "Soleil Belmont",
            "Stella & Loretta Lecarde",
            "Stella Lecarde",
            "Succubus",
            "Walter Bernhard",
            "Wind",
            "Young Maria Renard",
        ]

    def characters(self) -> List[str]:
        characters: List[str] = self.characters_base[:]

        if self.has_dlc_legacy_of_moonspell:
            characters.extend(self.characters_legacy_of_moonspell)

        if self.has_dlc_tides_of_foscari:
            characters.extend(self.characters_tides_of_foscari)

        if self.has_dlc_emergency_meeting:
            characters.extend(self.characters_emergency_meeting)

        if self.has_dlc_operation_guns:
            characters.extend(self.characters_operation_guns)

        if self.has_dlc_ode_to_castlevania:
            characters.extend(self.characters_ode_to_castlevania)

        if bool(self.archipelago_options.vampire_survivors_allow_secret_characters.value):
            characters.extend(self.characters_secret_base)

            if self.has_dlc_ode_to_castlevania:
                characters.extend(self.characters_secret_ode_to_castlevania)

        return sorted(characters)

    @functools.cached_property
    def base_weapons_base(self) -> List[str]:
        return [
            "Arma Dio",
            "Axe",
            "Bone",
            "Bracelet",
            "Candybox",
            "Carréllo",
            "Celestial Dusting",
            "Cherry Bomb",
            "Clock Lancet",
            "Cross",
            "Ebony Wings",
            "Eight The Sparrow",
            "Fire Wand",
            "Flames of Misspell",
            "Garlic",
            "Gatti Amari",
            "Glass Fandango",
            "Greatest Jubilee",
            "King Bible",
            "Knife",
            "La Robba",
            "Laurel",
            "Lightning Ring",
            "Magic Wand",
            "Pako Battiliar",
            "Peachone",
            "Pentagram",
            "Phas3r",
            "Phiera Der Tuphello",
            "Runetracer",
            "Santa Javelin",
            "Santa Water",
            "Shadow Pinion",
            "Song of Mana",
            "Vento Sacro",
            "Victory Sword",
            "Whip",
        ]

    @functools.cached_property
    def base_weapons_legacy_of_moonspell(self) -> List[str]:
        return [
            "108 Bocce",
            "Four Seasons",
            "Mille Bolle Blu",
            "Mirage Robe",
            "Night Sword",
            "Silver Wind",
            "Summon Night",
        ]

    @functools.cached_property
    def base_weapons_tides_of_foscari(self) -> List[str]:
        return [
            "Eskizzibur",
            "Flash Arrow",
            "Party Popper",
            "Prismatic Missile",
            "Shadow Servant",
            "SpellStream",
            "SpellStrike",
            "SpellString",
        ]

    @functools.cached_property
    def base_weapons_emergency_meeting(self) -> List[str]:
        return [
            "Clear Debris",
            "Hats",
            "Just Vent",
            "Lifesign Scan",
            "Lucky Swipe",
            "Report!",
            "Science Rocks",
            "Sharp Tongue",
        ]

    @functools.cached_property
    def base_weapons_operation_guns(self) -> List[str]:
        return [
            "Blade Crossbow",
            "C-U-Laser",
            "Diver Mines",
            "Firearm",
            "Homing Miss",
            "Long Gun",
            "Metal Claw",
            "Prism Lass",
            "Short Gun",
            "Sonic Bloom",
            "Spread Shot",
        ]

    @functools.cached_property
    def base_weapons_ode_to_castlevania(self) -> List[str]:
        return [
            "Alchemy Whip",
            "Alucard Spear",
            "Alucart Sworb",
            "Arrow of Goth",
            "Aura Blast",
            "Belnades' Spellbook",
            "Centralis Custos",
            "Clock Tower",
            "Coat of Arms",
            "Confodere",
            "Curved Knife",
            "Dark Rift",
            "Dextro Custos",
            "Discus",
            "Dominus Agony",
            "Dominus Anger",
            "Dominus Hatred",
            "Dragon Water Whip",
            "Ebony Diabologue",
            "Endo Gears",
            "Epi Head",
            "Familiar Forge",
            "Fulgur",
            "Gale Force",
            "Globus",
            "Grand Cross",
            "Guardian's Targe",
            "Hand Grenade",
            "Hex",
            "Hydro Storm",
            "Ice Fang",
            "Icebrand",
            "Iron Ball",
            "Iron Shield",
            "Javelin",
            "Jet Black Whip",
            "Keremet Bubbles",
            "Luminatio",
            "Mace",
            "Master Librarian",
            "Morning Star",
            "Myo Lift",
            "Optical Shot",
            "Peri Pendulum",
            "Platinum Whip",
            "Raging Fire",
            "Refectio",
            "Rock Riot",
            "Shuriken",
            "Silver Revolver",
            "Sinestro Custos",
            "Sonic Dash",
            "Sonic Whip",
            "Soul Steal",
            "Spectral Sword",
            "Star Flail",
            "Summon Spirit Tornado",
            "Summon Spirit",
            "Svarog Statue",
            "Sword Brothers",
            "Trident",
            "Troll Bomb",
            "Tyrfing",
            "Umbra",
            "Valmanway",
            "Vanitas Whip",
            "Vibhuti Whip",
            "Wind Whip",
            "Wine Glass",
        ]

    def base_weapons(self) -> List[str]:
        base_weapons: List[str] = self.base_weapons_base[:]

        if self.has_dlc_legacy_of_moonspell:
            base_weapons.extend(self.base_weapons_legacy_of_moonspell)

        if self.has_dlc_tides_of_foscari:
            base_weapons.extend(self.base_weapons_tides_of_foscari)

        if self.has_dlc_emergency_meeting:
            base_weapons.extend(self.base_weapons_emergency_meeting)

        if self.has_dlc_operation_guns:
            base_weapons.extend(self.base_weapons_operation_guns)

        if self.has_dlc_ode_to_castlevania:
            base_weapons.extend(self.base_weapons_ode_to_castlevania)

        return sorted(base_weapons)

    @functools.cached_property
    def evolution_weapons_base(self) -> List[str]:
        return [
            "Anima of Mortaccio  (Bone + Chaos Malachite + Mortaccio)",
            "Ashes of Muspell  (Flames of Misspell + Torrona's Box)",
            "Bi-Bracelet  (Bracelet)",
            "Bloody Tear  (Whip + Hollow Heart)",
            "Celestial Voulge  (Glass Fandango + Wings)",
            "Crimson Shroud  (Laurel + Metaglio Left / Right)",
            "Death Spiral  (Axe + Candelabrador)",
            "Gorgeous Moon  (Pentagram + Crown)",
            "Heaven Sword  (Cross + Clover)",
            "Hellfire  (Fire Wand + Spinach)",
            "Holy Wand  (Magic Wand + Empty Tome)",
            "Infinite Corridor  (Clock Lancet + Silver / Gold Rings)",
            "La Borra  (Santa Water + Attractorb)",
            "Mannajja  (Song of Mana + Skull O'Maniac)",
            "Mazo Familiar  (Pako Battiliar + Hollow Heart)",
            "NO FUTURE  (Runetracer + Armor)",
            "Photonstorm  (Phas3r + Empty Tome)",
            "Profusione D'Amore  (Celestial Dusting + Chaos Altemanna + O'Sole Meeo)",
            "Seraphic Cry  (Santa Javelin + Clover)",
            "Soul Eater  (Garlic + Pummarola)",
            "Thousand Edge  (Knife + Bracer)",
            "Thunder Loop  (Lightning Ring + Duplicator)",
            "Tri-Bracelet  (Bi-Bracelet)",
            "Unholy Vespers  (King Bible + Spellbinder)",
            "Valkyrie Turner  (Shadow Pinion + Wings)",
            "Vicious Hunger  (Gatti Amari + Stone Mask)",
            "Yatta Daikarin  (Cherry Bomb + Chaos Rosalia + Yatta Cavallo)",
        ]

    @functools.cached_property
    def evolution_weapons_legacy_of_moonspell(self) -> List[str]:
        return [
            "Boo Roo Boolle  (Mille Bolle Blu + Spellbinder)",
            "Echo Night  (Summon Night + Duplicator)",
            "Festive Winds  (Silver Wind + Pummarola)",
            "Godai Shuffle  (Four Seasons + Candelabrador)",
            "J'Odore  (Mirage Robe + Attractorb)",
            "Muramasa  (Night Sword + Stone Mask)",
        ]

    @functools.cached_property
    def evolution_weapons_tides_of_foscari(self) -> List[str]:
        return [
            "Legionnaire  (Eskizzibur + Armor)",
            "Luminaire  (Prismatic Missile + Crown)",
            "Millionaire  (Flash Arrow + Bracer)",
            "Ophion  (Shadow Servant + Skull O'Maniac)",
        ]

    @functools.cached_property
    def evolution_weapons_emergency_meeting(self) -> List[str]:
        return [
            "Clear Asteroids  (Clear Debris + Mini Guardian)",
            "Crossed Wires  (Lucky Swipe + Mini Engineer)",
            "Emergency Meeting  (Report! + Mini Crewmate)",
            "Impostongue  (Sharp Tongue + Mini Impostor)",
            "Paranormal Scan  (Lifesign Scan + Mini Ghost)",
            "Rocket Science  (Science Rocks + Mini Scientist)",
            "Unjust Ejection  (Just Vent + Mini Shapeshifter)",
        ]

    @functools.cached_property
    def evolution_weapons_operation_guns(self) -> List[str]:
        return [
            "Atmo-Torpedo  (Diver Mines + Weapon Power-Up + Attractorb)",
            "BFC2000-AD  (Blade Crossbow + Weapon Power-Up + Clover)",
            "Big Fuzzy Fist  (Metal Claw + Weapon Power-Up + Hollow Heart)",
            "Fire-L3GS  (Firearm + Weapon Power-Up + Candelabrador)",
            "Multistage Missiles  (Homing Miss + Weapon Power-Up + Duplicator)",
            "Pronto Beam  (C-U-Laser + Weapon Power-Up + Tirajisú)",
            "Prototype A  (Long Gun + Weapon Power-Up)",
            "Prototype B  (Short Gun + Weapon Power-Up + Bracer)",
            "Prototype C  (Spread Shot + Weapon Power-Up + Empty Tome)",
            "Time Warp  (Prism Lass + Weapon Power-Up + Wings)",
            "Wave Beam  (Sonic Bloom + Weapon Power-Up + Armor)",
        ]

    @functools.cached_property
    def evolution_weapons_ode_to_castlevania(self) -> List[str]:
        return [
            "Acerbatus  (Optical Shot + Karoma's Mana)",
            "Alucard Swords  (Alucart Sworb)",
            "Aurablaster Tip  (Vanitas Whip + Hollow Heart)",
            "Bwaka Knife  (Curved Knife + Bracer)",
            "Cocytus  (Ice Fang + Spellbinder)",
            "Crissaegrim Tip  (Sonic Whip + Skull O'Maniac)",
            "Cross Crasher Tip  (Platinum Whip + Clover)",
            "Dark Iron Shield  (Iron Shield + Parm Aegis)",
            "Daybreaker Tip  (Vibhuti Whip + Candelabrador)",
            "Gemma Torpor  (Rock Riot + Stone Mask)",
            "Gungnir-Souris  (Trident + Duplicator)",
            "Hydrostormer Tip  (Dragon Water Whip + Attractorb)",
            "Jewel Gun  (Silver Revolver + Karoma's Mana)",
            "Keremet Morbus  (Keremet Bubbles + Armor)",
            "Long Inus  (Javelin + Spellbinder)",
            "Meal Ticket  (Wine Glass + Tirajisú)",
            "Melio Confodere  (Vol Confodere)",
            "Moon Rod  (Star Flail + Pummarola)",
            "Mormegil Tip  (Jet Black Whip + Stone Mask)",
            "Nightmare  (Hex + Skull O'Maniac)",
            "Nitesco  (Globus + Empty Tome)",
            "Pneuma Tempestas  (Gale Force + Bracer)",
            "Rapidus Fio  (Sonic Dash + Wings)",
            "Rune Sword  (Tyrfing + Spinach)",
            "Sacred Beasts Tower Shield  (Guardian's Targe + Pummarola)",
            "Salamender  (Raging Fire + Spinach)",
            "Sanctuary  (Refectio + Clover)",
            "Spirit Tornado Tip  (Wind Whip + Crown)",
            "Stamazza  (Mace + Hollow Heart)",
            "Stellar Blade  (Discus + Parm Aegis)",
            "Tenebris Tonitrus  (Fulgur + Duplicator)",
            "The RPG  (Hand Grenade + Candelabrador)",
            "Thunderbolt Spear  (Alucard Spear + Wings)",
            "Vampire Killer  (Alchemy Whip + Tirajisú)",
            "Vol Confodere  (Confodere)",
            "Vol Luminatio  (Luminatio + Crown)",
            "Vol Umbra  (Umbra + Attractorb)",
            "Wrecking Ball  (Iron Ball + Armor)",
            "Yagyu Shuriken  (Shuriken + Empty Tome)",
        ]

    def evolution_weapons(self) -> List[str]:
        evolution_weapons: List[str] = self.evolution_weapons_base[:]

        if self.has_dlc_legacy_of_moonspell:
            evolution_weapons.extend(self.evolution_weapons_legacy_of_moonspell)

        if self.has_dlc_tides_of_foscari:
            evolution_weapons.extend(self.evolution_weapons_tides_of_foscari)

        if self.has_dlc_emergency_meeting:
            evolution_weapons.extend(self.evolution_weapons_emergency_meeting)

        if self.has_dlc_operation_guns:
            evolution_weapons.extend(self.evolution_weapons_operation_guns)

        if self.has_dlc_ode_to_castlevania:
            evolution_weapons.extend(self.evolution_weapons_ode_to_castlevania)

        return sorted(evolution_weapons)

    @functools.cached_property
    def union_weapons_base(self) -> List[str]:
        return [
            "Vandalier  (Peachone + Ebony Wings)",
            "Phieraggi  (Phiera Der Tuphello + Eight The Sparrow + Tirajisú)",
            "Fuwalafuwaloo  (Vento Sacro + Bloody Tear)",
        ]

    @functools.cached_property
    def union_weapons_tides_of_foscari(self) -> List[str]:
        return [
            "SpellStrom  (SpellString + SpellStream + SpellStrike)",
        ]

    @functools.cached_property
    def union_weapons_ode_to_castlevania(self) -> List[str]:
        return [
            "Clock Tower  (Endo Gears + Peri Pendulum + Myo Lift + Epi Head)",
            "Power of Sire  (Dominus Anger + Dominus Hatred + Dominus Agony)",
            "Trinum Custodem  (Dextro Custos + Sinestro Custos + Centralis Custos)",
        ]

    def union_weapons(self) -> List[str]:
        union_weapons: List[str] = self.union_weapons_base[:]

        if self.has_dlc_tides_of_foscari:
            union_weapons.extend(self.union_weapons_tides_of_foscari)

        if self.has_dlc_ode_to_castlevania:
            union_weapons.extend(self.union_weapons_ode_to_castlevania)

        return sorted(union_weapons)

    def evolution_union_weapons(self) -> List[str]:
        return sorted(self.evolution_weapons() + self.union_weapons())

    @staticmethod
    def passive_items() -> List[str]:
        return [
            "Armor",
            "Attractorb",
            "Bracer",
            "Candelabrador",
            "Clover",
            "Crown",
            "Duplicator",
            "Empty Tome",
            "Hollow Heart",
            "Karoma's Mana",
            "Parm Aegis",
            "Pummarola",
            "Skull O'Maniac",
            "Spellbinder",
            "Spinach",
            "Stone Mask",
            "Tirajisú",
            "Torrona's Box",
            "Wings",
        ]

    @staticmethod
    def familiars() -> List[str]:
        return [
            "Alleged Ghost",
            "Bitterfly",
            "Faerie",
            "Imp",
            "Pumpkin",
            "Sacred Cardinal",
            "Sacred Dragon",
            "Sacred Tiger",
            "Sacred Turtle",
            "Ukoback",
            "Wood Rod",
        ]

    @functools.cached_property
    def stages_base(self) -> List[str]:
        return [
            "Astral Stair",
            "Bat Country",
            "Boss Rash",
            "Cappella Magna",
            "Carlo Cart",
            "Dairy Plant",
            # "Eudaimonia Machine",
            "Gallo Tower",
            "Green Acres",
            # "Holy Forbidden",
            "Il Molise",
            "Inlaid Library",
            "Laborratory",
            "Mad Forest",
            "Moongolow",
            "Room 1665",
            "Space 54",
            "The Bone Zone",
            "Tiny Bridge",
            "Whiteout",
        ]

    @functools.cached_property
    def stages_legacy_of_moonspell(self) -> List[str]:
        return [
            "Mt.Moonspell",
        ]

    @functools.cached_property
    def stages_tides_of_foscari(self) -> List[str]:
        return [
            "Abyss Foscari",
            "Lake Foscari",
        ]

    @functools.cached_property
    def stages_emergency_meeting(self) -> List[str]:
        return [
            "Polus Replica",
        ]

    @functools.cached_property
    def stages_operation_guns(self) -> List[str]:
        return [
            "Hectic Highway",
            "Neo Galuga",
        ]

    @functools.cached_property
    def stages_ode_to_castlevania(self) -> List[str]:
        return [
            "Ode to Castlevania",
        ]

    def stages(self) -> List[str]:
        stages: List[str] = self.stages_base[:]

        if self.has_dlc_legacy_of_moonspell:
            stages.extend(self.stages_legacy_of_moonspell)

        if self.has_dlc_tides_of_foscari:
            stages.extend(self.stages_tides_of_foscari)

        if self.has_dlc_emergency_meeting:
            stages.extend(self.stages_emergency_meeting)

        if self.has_dlc_operation_guns:
            stages.extend(self.stages_operation_guns)

        if self.has_dlc_ode_to_castlevania:
            stages.extend(self.stages_ode_to_castlevania)

        return sorted(stages)


# Archipelago Options
class VampireSurvivorsDLCOwned(OptionSet):
    """
    Indicates which Vampire Survivors DLC the player owns, if any.
    """

    display_name = "Vampire Survivors DLC Owned"
    valid_keys = [
        "Legacy of Moonspell",
        "Tides of Foscari",
        "Emergency Meeting",
        "Operation Guns",
        "Ode to Castlevania",
    ]

    default = valid_keys


class VampireSurvivorsAllowSecretCharacters(Toggle):
    """
    If true, secret characters will be part of the characters that can be selected.
    """

    display_name = "Vampire Survivors Allow Secret Characters"
