from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class LegendaryAMarvelDeckBuildingGameArchipelagoOptions:
    legendary_a_marvel_deck_building_game_sets_expansions_owned: LegendaryAMarvelDeckBuildingGameSetsExpansionsOwned


class LegendaryAMarvelDeckBuildingGameGame(Game):
    name = "Legendary - A Marvel Deck Building Game"
    platform = KeymastersKeepGamePlatforms.CARD

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = LegendaryAMarvelDeckBuildingGameArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Replace two Henchmen cards with random Ambition cards",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Play one random Horror at the start of each game",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Always include HERO in your team (when possible)",
                data={
                    "HERO": (self.heroes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Always include VILLAIN in the setup (when possible)",
                data={
                    "VILLAIN": (self.villain_groups, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Always include HENCHMEN in the setup (when possible)",
                data={
                    "HENCHMEN": (self.henchmen, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Stop MASTERMIND from completing the 'SCHEME' Scheme with a Team including HEROES",
                data={
                    "MASTERMIND": (self.masterminds, 1),
                    "SCHEME": (self.schemes, 1),
                    "HEROES": (self.heroes, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Stop MASTERMIND from completing the 'SCHEME' Scheme while they lead VILLAIN",
                data={
                    "MASTERMIND": (self.masterminds, 1),
                    "SCHEME": (self.schemes, 1),
                    "VILLAIN": (self.villain_groups, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Stop MASTERMIND from completing the 'SCHEME' Scheme while they lead HENCHMEN",
                data={
                    "MASTERMIND": (self.masterminds, 1),
                    "SCHEME": (self.schemes, 1),
                    "HENCHMEN": (self.henchmen, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Stop MASTERMIND while they lead VILLAIN with a Team including HEROES",
                data={
                    "MASTERMIND": (self.masterminds, 1),
                    "VILLAIN": (self.villain_groups, 1),
                    "HEROES": (self.heroes, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Stop MASTERMIND while they lead VILLAIN and HENCHMEN",
                data={
                    "MASTERMIND": (self.masterminds, 1),
                    "VILLAIN": (self.villain_groups, 1),
                    "HENCHMEN": (self.henchmen, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Stop MASTERMIND while they lead HENCHMEN with a Team including HEROES",
                data={
                    "MASTERMIND": (self.masterminds, 1),
                    "HENCHMEN": (self.henchmen, 1),
                    "HEROES": (self.heroes, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Foil the 'SCHEME' Scheme against VILLAIN with a Team including HEROES",
                data={
                    "SCHEME": (self.schemes, 1),
                    "VILLAIN": (self.villain_groups, 1),
                    "HEROES": (self.heroes, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Foil the 'SCHEME' Scheme against VILLAIN and HENCHMEN",
                data={
                    "SCHEME": (self.schemes, 1),
                    "VILLAIN": (self.villain_groups, 1),
                    "HENCHMEN": (self.henchmen, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Foil the 'SCHEME' Scheme against HENCHMEN with a Team including HEROES",
                data={
                    "SCHEME": (self.schemes, 1),
                    "HENCHMEN": (self.henchmen, 1),
                    "HEROES": (self.heroes, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a round against VILLAIN and HENCHMEN with a Team including HEROES",
                data={
                    "VILLAIN": (self.villain_groups, 1),
                    "HENCHMEN": (self.henchmen, 1),
                    "HEROES": (self.heroes, 3),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=3,
            ),
        ]

    @property
    def sets_expansions_owned(self) -> List[str]:
        return sorted(self.archipelago_options.legendary_a_marvel_deck_building_game_sets_expansions_owned.value)

    @property
    def has_core(self) -> bool:
        return "Core" in self.sets_expansions_owned

    @property
    def has_dark_city(self) -> bool:
        return "Dark City" in self.sets_expansions_owned

    @property
    def has_fantastic_four(self) -> bool:
        return "Fantastic Four" in self.sets_expansions_owned

    @property
    def has_paint_the_town_red(self) -> bool:
        return "Paint the Town Red" in self.sets_expansions_owned

    @property
    def has_villains(self) -> bool:
        return "Villains" in self.sets_expansions_owned

    @property
    def has_guardians_of_the_galaxy(self) -> bool:
        return "Guardians of the Galaxy" in self.sets_expansions_owned

    @property
    def has_fear_itself(self) -> bool:
        return "Fear Itself" in self.sets_expansions_owned

    @property
    def has_secret_wars_vol_1(self) -> bool:
        return "Secret Wars Vol. 1" in self.sets_expansions_owned

    @property
    def has_secret_wars_vol_2(self) -> bool:
        return "Secret Wars Vol. 2" in self.sets_expansions_owned

    @property
    def has_captain_america_75th_anniversary(self) -> bool:
        return "Captain America 75th Anniversary" in self.sets_expansions_owned

    @property
    def has_civil_war(self) -> bool:
        return "Civil War" in self.sets_expansions_owned

    @property
    def has_deadpool(self) -> bool:
        return "Deadpool" in self.sets_expansions_owned

    @property
    def has_noir(self) -> bool:
        return "Noir" in self.sets_expansions_owned

    @property
    def has_x_men(self) -> bool:
        return "X-Men" in self.sets_expansions_owned

    @property
    def has_spider_man_homecoming(self) -> bool:
        return "Spider-Man Homecoming" in self.sets_expansions_owned

    @property
    def has_champions(self) -> bool:
        return "Champions" in self.sets_expansions_owned

    @property
    def has_world_war_hulk(self) -> bool:
        return "World War Hulk" in self.sets_expansions_owned

    @property
    def has_mcu_phase_1_unique_cards(self) -> bool:
        return "MCU Phase 1 (Unique Cards)" in self.sets_expansions_owned

    @property
    def has_ant_man(self) -> bool:
        return "Ant-Man" in self.sets_expansions_owned

    @property
    def has_venom(self) -> bool:
        return "Venom" in self.sets_expansions_owned

    @property
    def has_dimensions(self) -> bool:
        return "Dimensions" in self.sets_expansions_owned

    @property
    def has_revelations(self) -> bool:
        return "Revelations" in self.sets_expansions_owned

    @property
    def has_shield(self) -> bool:
        return "S.H.I.E.L.D." in self.sets_expansions_owned

    @property
    def has_heroes_of_asgard(self) -> bool:
        return "Heroes of Asgard" in self.sets_expansions_owned

    @property
    def has_the_new_mutants(self) -> bool:
        return "The New Mutants" in self.sets_expansions_owned

    @property
    def has_into_the_cosmos(self) -> bool:
        return "Into the Cosmos" in self.sets_expansions_owned

    @property
    def has_realm_of_kings(self) -> bool:
        return "Realm of Kings" in self.sets_expansions_owned

    @property
    def has_annihilation(self) -> bool:
        return "Annihilation" in self.sets_expansions_owned

    @property
    def has_messiah_complex(self) -> bool:
        return "Messiah Complex" in self.sets_expansions_owned

    @property
    def has_doctor_strange_and_the_shadows_of_nightmare(self) -> bool:
        return "Doctor Strange and the Shadows of Nightmare" in self.sets_expansions_owned

    @property
    def has_mcu_guardians_of_the_galaxy(self) -> bool:
        return "MCU Guardians of the Galaxy" in self.sets_expansions_owned

    @property
    def has_black_panther(self) -> bool:
        return "Black Panther" in self.sets_expansions_owned

    @property
    def has_black_widow(self) -> bool:
        return "Black Widow" in self.sets_expansions_owned

    @property
    def has_mcu_infinity_saga(self) -> bool:
        return "MCU Infinity Saga" in self.sets_expansions_owned

    @property
    def has_midnight_sons(self) -> bool:
        return "Midnight Sons" in self.sets_expansions_owned

    @property
    def has_what_if(self) -> bool:
        return "What If...?" in self.sets_expansions_owned

    @property
    def has_mcu_ant_man_and_the_wasp(self) -> bool:
        return "MCU Ant-Man and the Wasp" in self.sets_expansions_owned

    @property
    def has_2099(self) -> bool:
        return "2099" in self.sets_expansions_owned

    @property
    def has_weapon_x(self) -> bool:
        return "Weapon X" in self.sets_expansions_owned

    @property
    def has_buffy(self) -> bool:
        return "Buffy" in self.sets_expansions_owned

    @property
    def has_james_bond_core(self) -> bool:
        return "James Bond Core" in self.sets_expansions_owned

    @property
    def has_james_bond_expansion(self) -> bool:
        return "James Bond Expansion" in self.sets_expansions_owned

    @property
    def has_james_bond_the_spy_who_loved_me(self) -> bool:
        return "James Bond The Spy Who Loved Me" in self.sets_expansions_owned

    @property
    def has_james_bond_no_time_to_die(self) -> bool:
        return "James Bond No Time To Die" in self.sets_expansions_owned

    @property
    def has_big_trouble_in_little_china(self) -> bool:
        return "Big Trouble in Little China" in self.sets_expansions_owned

    @functools.cached_property
    def heroes_core(self) -> List[str]:
        return [
            "Black Widow (Avengers)",
            "Captain America",
            "Cyclops",
            "Deadpool (Core)",
            "Emma Frost",
            "Gambit",
            "Hawkeye",
            "Hulk",
            "Iron Man",
            "Nick Fury",
            "Rogue",
            "Spider-Man",
            "Storm",
            "Thor (Avengers)",
            "Wolverine (X-Men)",
        ]

    @functools.cached_property
    def heroes_dark_city(self) -> List[str]:
        return [
            "Angel (X-Men)",
            "Bishop",
            "Blade",
            "Cable",
            "Colossus",
            "Daredevil",
            "Domino",
            "Elektra",
            "Forge",
            "Ghost Rider",
            "Iceman",
            "Iron Fist",
            "Jean Grey",
            "Nightcrawler",
            "Professor X",
            "Punisher",
            "Wolverine (X-Force)",
        ]

    @functools.cached_property
    def heroes_fantastic_four(self) -> List[str]:
        return [
            "Human Torch",
            "Invisible Woman",
            "Mr. Fantastic",
            "Silver Surfer",
            "Thing",
        ]

    @functools.cached_property
    def heroes_paint_the_town_red(self) -> List[str]:
        return [
            "Black Cat",
            "Moon Knight",
            "Scarlet Spider",
            "Spider-Woman",
            "Symbiote Spider-Man",
        ]

    @functools.cached_property
    def heroes_villains(self) -> List[str]:
        return [
            "Bullseye",
            "Dr. Octopus",
            "Electro",
            "Enchantress",
            "Green Goblin",
            "Juggernaut",
            "Kingpin",
            "Kraven",
            "Loki",
            "Magneto",
            "Mysterio",
            "Mystique",
            "Sabretooth",
            "Ultron",
            "Venom (Sinister Six)",
        ]

    @functools.cached_property
    def heroes_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Drax the Destroyer",
            "Gamora",
            "Groot",
            "Rocket Raccoon",
            "Star-Lord",
        ]

    @functools.cached_property
    def heroes_fear_itself(self) -> List[str]:
        return [
            "Greithoth, Breaker of Wills",
            "Kuurth, Breaker of Stone",
            "Nerkkod, Breaker of Oceans",
            "Nul, Breaker of Worlds",
            "Skadi",
            "Skirn, Breaker of Men",
        ]

    @functools.cached_property
    def heroes_secret_wars_vol_1(self) -> List[str]:
        return [
            "Apocalyptic Kitty Pryde",
            "Black Bolt (Illuminati)",
            "Black Panther (Illuminati)",
            "Captain Marvel",
            "Dr. Strange (Illuminati)",
            "Lady Thor",
            "Magik",
            "Maximus",
            "Namor",
            "Old Man Logan",
            "Proxima Midnight",
            "Superior Iron Man",
            "Thanos",
            "Ultimate Spider-Man",
        ]

    @functools.cached_property
    def heroes_secret_wars_vol_2(self) -> List[str]:
        return [
            "Agent Venom",
            "Arkon the Magnificent",
            "Beast (Illuminati)",
            "Black Swan",
            "The Captain and the Devil",
            "Captain Britain",
            "Corvus Glaive",
            "Dr. Punisher the Soldier Supreme",
            "Elsa Bloodstone (SHIELD)",
            "Phoenix Force Cyclops",
            "Ruby Summers",
            "Shang-Chi",
            "Silk",
            "Soulsword Colossus",
            "Spider-Gwen",
            "Time-Traveling Jean Grey",
        ]

    @functools.cached_property
    def heroes_captain_america_75th_anniversary(self) -> List[str]:
        return [
            "Agent X-13",
            "Captain America (Falcon)",
            "Captain America 1941",
            "Steve Rogers, Director of S.H.I.E.L.D.",
            "Winter Soldier",
        ]

    @functools.cached_property
    def heroes_civil_war(self) -> List[str]:
        return [
            "Captain America, Secret Avenger",
            "Cloak & Dagger",
            "Daredevil (Iron Fist)",
            "Falcon",
            "Goliath",
            "Hercules",
            "Hulkling",
            "Luke Cage",
            "Patriot",
            "Peter Parker",
            "Speedball",
            "Stature",
            "Storm & Black Panther",
            "Tigra",
            "Vision",
            "Wiccan",
        ]

    @functools.cached_property
    def heroes_deadpool(self) -> List[str]:
        return [
            "Bob, Agent of Hydra",
            "Deadpool (MfM)",
            "Slapstick",
            "Solo",
            "Stingray",
        ]

    @functools.cached_property
    def heroes_noir(self) -> List[str]:
        return [
            "Angel Noir",
            "Daredevil Noir",
            "Iron Man Noir",
            "Luke Cage Noir",
            "Spider-Man Noir",
        ]

    @functools.cached_property
    def heroes_x_men(self) -> List[str]:
        return [
            "Aurora and Northstar",
            "Banshee",
            "Beast (X-Men)",
            "Cannonball",
            "Colossus and Wolverine",
            "Dazzler",
            "Havok",
            "Jubilee",
            "Kitty Pryde",
            "Legion",
            "Longshot",
            "Phoenix",
            "Polaris",
            "Psylocke",
            "X-23",
        ]

    @functools.cached_property
    def heroes_spider_man_homecoming(self) -> List[str]:
        return [
            "Happy Hogan",
            "High Tech Spider-Man",
            "Peter Parker, Homecoming",
            "Peter's Allies",
            "Tony Stark",
        ]

    @functools.cached_property
    def heroes_champions(self) -> List[str]:
        return [
            "Gwenpool",
            "Ms. Marvel",
            "Nova (Champions)",
            "Totally Awesome Hulk",
            "Viv Vision",
        ]

    @functools.cached_property
    def heroes_world_war_hulk(self) -> List[str]:
        return [
            "Amadeus Cho",
            "Bruce Banner (Avengers)",
            "Caiera",
            "Gladiator Hulk",
            "Hiroim",
            "Hulkbuster Iron Man",
            "Joe Fix-It, Grey Hulk",
            "Korg",
            "Miek, The Unhived",
            "Namora",
            "No Name, Brood Queen",
            "Rick Jones",
            "Sentry",
            "She-Hulk",
            "Skaar, Son of Hulk",
        ]

    @functools.cached_property
    def heroes_ant_man(self) -> List[str]:
        return [
            "Ant-Man (Avengers)",
            "Black Knight",
            "Jocasta",
            "Wasp (Avengers)",
            "Wonder Man",
        ]

    @functools.cached_property
    def heroes_venom(self) -> List[str]:
        return [
            "Carnage",
            "Venom (Venomverse)",
            "Venom Rocket",
            "Venomized Dr. Strange",
            "Venompool",
        ]

    @functools.cached_property
    def heroes_dimensions(self) -> List[str]:
        return [
            "Howard the Duck",
            "Jessica Jones",
            "Man-Thing",
            "Ms. America",
            "Squirrel Girl",
        ]

    @functools.cached_property
    def heroes_revelations(self) -> List[str]:
        return [
            "Captain Marvel, Agent of S.H.I.E.L.D.",
            "Darkhawk",
            "Hellcat",
            "Photon",
            "Quicksilver",
            "Ronin",
            "Scarlet Witch",
            "Speed",
            "War Machine",
        ]

    @functools.cached_property
    def heroes_shield(self) -> List[str]:
        return [
            "Agent Phil Coulson",
            "Deathlok",
            "Mockingbird",
            "Quake",
        ]

    @functools.cached_property
    def heroes_heroes_of_asgard(self) -> List[str]:
        return [
            "Beta Ray Bill",
            "Lady Sif",
            "Thor (HoA)",
            "Valkyrie",
            "The Warriors Three",
        ]

    @functools.cached_property
    def heroes_the_new_mutants(self) -> List[str]:
        return [
            "Karma",
            "Mirage",
            "Sunspot",
            "Warlock",
            "Wolfsbane",
        ]

    @functools.cached_property
    def heroes_into_the_cosmos(self) -> List[str]:
        return [
            "Adam Warlock",
            "Captain Mar-Vell",
            "Moondragon",
            "Nebula",
            "Nova (Avengers)",
            "Phyla-Vell",
            "Quasar",
            "Ronan the Accuser",
            "Yondu",
        ]

    @functools.cached_property
    def heroes_realm_of_kings(self) -> List[str]:
        return [
            "Black Bolt (Inhumans)",
            "Crystal",
            "Gorgon",
            "Karnak",
            "Medusa",
        ]

    @functools.cached_property
    def heroes_annihilation(self) -> List[str]:
        return [
            "Brainstorm",
            "Fantastic Four United",
            "Heralds of Galactus",
            "Psi-Lord",
            "Super-Skrull",
        ]

    @functools.cached_property
    def heroes_messiah_complex(self) -> List[str]:
        return [
            "M",
            "Multiple Man",
            "Rictor",
            "Shatterstar",
            "Siryn",
            "Stepford Cuckoos",
            "Strong Guy",
            "Warpath",
        ]

    @functools.cached_property
    def heroes_doctor_strange_and_the_shadows_of_nightmare(self) -> List[str]:
        return [
            "The Ancient One",
            "Clea",
            "Doctor Strange (Avengers)",
            "Doctor Voodoo",
            "The Vishanti",
        ]

    @functools.cached_property
    def heroes_mcu_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Drax",
            "Gamora",
            "Mantis",
            "Rocket & Groot",
            "Star-Lord",
        ]

    @functools.cached_property
    def heroes_black_panther(self) -> List[str]:
        return [
            "General Okoye",
            "King Black Panther",
            "Princess Shuri",
            "Queen Storm of Wakanda",
            "White Wolf",
        ]

    @functools.cached_property
    def heroes_black_widow(self) -> List[str]:
        return [
            "Black Widow (S.H.I.E.L.D.)",
            "Falcon & Winter Soldier",
            "Red Guardian",
            "White Tiger",
            "Yelena Belova",
        ]

    @functools.cached_property
    def heroes_mcu_infinity_saga(self) -> List[str]:
        return [
            "Black Panther (MCU)",
            "Bruce Banner (MCU)",
            "Captain Marvel (MCU)",
            "Doctor Strange (MCU)",
            "Wanda & Vision",
        ]

    @functools.cached_property
    def heroes_midnight_sons(self) -> List[str]:
        return [
            "Blade, Daywalker",
            "Elsa Bloodstone (MK)",
            "Morbius",
            "Werewolf By Night",
            "Wong, Master of the Mystic Arts",
        ]

    @functools.cached_property
    def heroes_what_if(self) -> List[str]:
        return [
            "Apocalyptic Black Widow",
            "Captain Carter",
            "Doctor Strange Supreme",
            "Gamora, Destroyer of Thanos",
            "Killmonger, Spec Ops",
            "Party Thor",
            "Star-Lord T'Challa",
            "Uatu, The Watcher",
        ]

    @functools.cached_property
    def heroes_mcu_ant_man_and_the_wasp(self) -> List[str]:
        return [
            "Ant Army",
            "Ant-Man (MCU)",
            "Cassie Lang",
            "Freedom Fighters",
            "Janet Van Dyne",
            "Jentorra",
            "Scott Lang, Cat Burgler",
            "Wasp (MCU)",
        ]

    @functools.cached_property
    def heroes_2099(self) -> List[str]:
        return [
            "Doctor Doom 2099",
            "Ghost Rider 2099",
            "Hulk 2099",
            "Ravage 2099",
            "Spider-Man 2099",
        ]

    @functools.cached_property
    def heroes_weapon_x(self) -> List[str]:
        return [
            "Fantomex",
            "Marrow",
            "Weapon H",
            "Weapon X (Wolverine)",
        ]

    @functools.cached_property
    def heroes_buffy(self) -> List[str]:
        return [
            "Angel (Buffy)",
            "Anya Jenkins",
            "Buffy Summers",
            "Buffybot",
            "Cordelia Chase",
            "Daniel 'Oz' Osbourne",
            "Faith Lehane",
            "The First Slayer",
            "Jenny Calendar",
            "Riley Finn",
            "Rupert Giles",
            "Spike",
            "Tara Maclay",
            "Willow Rosenberg",
            "Xander Harris",
        ]

    @functools.cached_property
    def heroes_james_bond_core(self) -> List[str]:
        return [
            "James Bond - Casino Royale",
            "Vesper Lynd",
            "M - Casino Royale",
            "Allies - Casino Royale",
            "Equipment - Casino Royale",
            "James Bond - The Man with the Golden Gun",
            "Mary Goodnight",
            "Andrea Anders",
            "Allies - The Man with the Golden Gun",
            "Vehicles - The Man with the Golden Gun",
            "James Bond - Goldeneye",
            "Natalya Simonova",
            "MI6 - Goldeneye",
            "Allies - Goldeneye",
            "Equipment - Goldeneye",
            "James Bond - Goldfinger",
            "Pussy Galore",
            "Allies - Goldfinger",
            "Equipment - Goldfinger",
            "Vehicles - Goldfinger",
        ]

    @functools.cached_property
    def heroes_james_bond_expansion(self) -> List[str]:
        return [
            "James Bond - Licence to Kill",
            "Pam Bouvier",
            "Q - Licence to Kill",
            "Allies - Licence to Kill",
            "Equipment - Licence to Kill",
            "James Bond - On Her Majesty's Secret Service",
            "Tracy Bond",
            "Allies - On Her Majesty's Secret Service",
            "Equipment - On Her Majesty's Secret Service",
            "Vehicles - On Her Majesty's Secret Service",
        ]

    @functools.cached_property
    def heroes_james_bond_the_spy_who_loved_me(self) -> List[str]:
        return [
            "James Bond - The Spy who Loved Me",
            "Anya Amasova",
            "Allies - The Spy who Loved Me",
            "Equipment - The Spy who Loved Me",
            "Vehicles - The Spy who Loved Me",
        ]

    @functools.cached_property
    def heroes_james_bond_no_time_to_die(self) -> List[str]:
        return [
            "James Bond - No Time to Die",
            "Dr. Madeleine Swann - No Time to Die",
            "Nomi",
            "Allies - No Time to Die",
            "Vehicles - No Time to Die",
        ]

    @functools.cached_property
    def heroes_big_trouble_in_little_china(self) -> List[str]:
        return [
            "Eddie",
            "Egg Shen",
            "Gracie Law",
            "Henry Swanson",
            "Jack Burton",
            "Margo",
            "Miao Yin",
            "Pork Chop Express",
            "Wang Chi",
        ]

    def heroes(self) -> List[str]:
        heroes: List[str] = list()

        if self.has_core:
            heroes.extend(self.heroes_core)
        if self.has_dark_city:
            heroes.extend(self.heroes_dark_city)
        if self.has_fantastic_four:
            heroes.extend(self.heroes_fantastic_four)
        if self.has_paint_the_town_red:
            heroes.extend(self.heroes_paint_the_town_red)
        if self.has_villains:
            heroes.extend(self.heroes_villains)
        if self.has_guardians_of_the_galaxy:
            heroes.extend(self.heroes_guardians_of_the_galaxy)
        if self.has_fear_itself:
            heroes.extend(self.heroes_fear_itself)
        if self.has_secret_wars_vol_1:
            heroes.extend(self.heroes_secret_wars_vol_1)
        if self.has_secret_wars_vol_2:
            heroes.extend(self.heroes_secret_wars_vol_2)
        if self.has_captain_america_75th_anniversary:
            heroes.extend(self.heroes_captain_america_75th_anniversary)
        if self.has_civil_war:
            heroes.extend(self.heroes_civil_war)
        if self.has_deadpool:
            heroes.extend(self.heroes_deadpool)
        if self.has_noir:
            heroes.extend(self.heroes_noir)
        if self.has_x_men:
            heroes.extend(self.heroes_x_men)
        if self.has_spider_man_homecoming:
            heroes.extend(self.heroes_spider_man_homecoming)
        if self.has_champions:
            heroes.extend(self.heroes_champions)
        if self.has_world_war_hulk:
            heroes.extend(self.heroes_world_war_hulk)
        if self.has_ant_man:
            heroes.extend(self.heroes_ant_man)
        if self.has_venom:
            heroes.extend(self.heroes_venom)
        if self.has_dimensions:
            heroes.extend(self.heroes_dimensions)
        if self.has_revelations:
            heroes.extend(self.heroes_revelations)
        if self.has_shield:
            heroes.extend(self.heroes_shield)
        if self.has_heroes_of_asgard:
            heroes.extend(self.heroes_heroes_of_asgard)
        if self.has_the_new_mutants:
            heroes.extend(self.heroes_the_new_mutants)
        if self.has_into_the_cosmos:
            heroes.extend(self.heroes_into_the_cosmos)
        if self.has_realm_of_kings:
            heroes.extend(self.heroes_realm_of_kings)
        if self.has_annihilation:
            heroes.extend(self.heroes_annihilation)
        if self.has_messiah_complex:
            heroes.extend(self.heroes_messiah_complex)
        if self.has_doctor_strange_and_the_shadows_of_nightmare:
            heroes.extend(self.heroes_doctor_strange_and_the_shadows_of_nightmare)
        if self.has_mcu_guardians_of_the_galaxy:
            heroes.extend(self.heroes_mcu_guardians_of_the_galaxy)
        if self.has_black_panther:
            heroes.extend(self.heroes_black_panther)
        if self.has_black_widow:
            heroes.extend(self.heroes_black_widow)
        if self.has_mcu_infinity_saga:
            heroes.extend(self.heroes_mcu_infinity_saga)
        if self.has_midnight_sons:
            heroes.extend(self.heroes_midnight_sons)
        if self.has_what_if:
            heroes.extend(self.heroes_what_if)
        if self.has_mcu_ant_man_and_the_wasp:
            heroes.extend(self.heroes_mcu_ant_man_and_the_wasp)
        if self.has_2099:
            heroes.extend(self.heroes_2099)
        if self.has_weapon_x:
            heroes.extend(self.heroes_weapon_x)
        if self.has_buffy:
            heroes.extend(self.heroes_buffy)
        if self.has_james_bond_core:
            heroes.extend(self.heroes_james_bond_core)
        if self.has_james_bond_expansion:
            heroes.extend(self.heroes_james_bond_expansion)
        if self.has_james_bond_the_spy_who_loved_me:
            heroes.extend(self.heroes_james_bond_the_spy_who_loved_me)
        if self.has_james_bond_no_time_to_die:
            heroes.extend(self.heroes_james_bond_no_time_to_die)
        if self.has_big_trouble_in_little_china:
            heroes.extend(self.heroes_big_trouble_in_little_china)

        return heroes

    @functools.cached_property
    def masterminds_core(self) -> List[str]:
        return [
            "Dr. Doom",
            "Loki",
            "Magneto",
            "Red Skull",
        ]

    @functools.cached_property
    def masterminds_dark_city(self) -> List[str]:
        return [
            "Apocalypse",
            "Kingpin",
            "Mephisto",
            "Mr. Sinister",
            "Stryfe",
        ]

    @functools.cached_property
    def masterminds_fantastic_four(self) -> List[str]:
        return [
            "Galactus",
            "Mole Man",
        ]

    @functools.cached_property
    def masterminds_paint_the_town_red(self) -> List[str]:
        return [
            "Carnage",
            "Mysterio",
        ]

    @functools.cached_property
    def masterminds_villains(self) -> List[str]:
        return [
            "Dr. Strange",
            "Nick Fury",
            "Odin",
            "Professor X",
        ]

    @functools.cached_property
    def masterminds_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Supreme Intelligence of the Kree",
            "Thanos",
        ]

    @functools.cached_property
    def masterminds_fear_itself(self) -> List[str]:
        return [
            "Uru-Enchanted Iron Man",
        ]

    @functools.cached_property
    def masterminds_secret_wars_vol_1(self) -> List[str]:
        return [
            "Madelyne Pryor, Goblin Queen",
            "Nimrod, Super Sentinel",
            "Wasteland Hulk",
            "Zombie Green Goblin",
        ]

    @functools.cached_property
    def masterminds_secret_wars_vol_2(self) -> List[str]:
        return [
            "Immortal Emperor Zheng-Zhu",
            "King Hyperion",
            "Shiklah, the Demon Bride",
            "Spider Queen",
        ]

    @functools.cached_property
    def masterminds_captain_america_75th_anniversary(self) -> List[str]:
        return [
            "Arnim Zola",
            "Baron Heinrich Zemo",
        ]

    @functools.cached_property
    def masterminds_civil_war(self) -> List[str]:
        return [
            "Authoritarian Iron Man",
            "Baron Helmut Zemo",
            "Maria Hill, Director of S.H.I.E.L.D.",
            "Misty Knight",
            "Ragnarök",
        ]

    @functools.cached_property
    def masterminds_deadpool(self) -> List[str]:
        return [
            "Evil Deadpool",
            "Macho Gomez",
        ]

    @functools.cached_property
    def masterminds_noir(self) -> List[str]:
        return [
            "Charles Xavier, Professor of Crime",
            "The Goblin, Underworld Boss",
        ]

    @functools.cached_property
    def masterminds_x_men(self) -> List[str]:
        return [
            "Arcade",
            "Dark Phoenix",
            "Deathbird",
            "Mojo",
            "Onslaught",
            "Shadow King",
        ]

    @functools.cached_property
    def masterminds_spider_man_homecoming(self) -> List[str]:
        return [
            "Adrian Toomes",
            "Vulture",
        ]

    @functools.cached_property
    def masterminds_champions(self) -> List[str]:
        return [
            "Fin Fang Foom",
            "Pagliacci",
        ]

    @functools.cached_property
    def masterminds_world_war_hulk(self) -> List[str]:
        return [
            "General 'Thunderbolt' Ross",
            "Illuminati, Secret Society",
            "King Hulk, Sakaarson",
            "M.O.D.O.K.",
            "The Red King",
            "The Sentry",
        ]

    @functools.cached_property
    def masterminds_mcu_phase_1_unique_cards(self) -> List[str]:
        return [
            "Iron Monger",
        ]

    @functools.cached_property
    def masterminds_ant_man(self) -> List[str]:
        return [
            "Morgan Le Fay",
            "Ultron",
        ]

    @functools.cached_property
    def masterminds_venom(self) -> List[str]:
        return [
            "Hybrid",
            "Poison Thanos",
        ]

    @functools.cached_property
    def masterminds_dimensions(self) -> List[str]:
        return [
            "J Jonah Jameson",
        ]

    @functools.cached_property
    def masterminds_revelations(self) -> List[str]:
        return [
            "Grim Reaper",
            "The Hood",
            "Mandarin",
        ]

    @functools.cached_property
    def masterminds_shield(self) -> List[str]:
        return [
            "Hydra High Council",
            "Hydra Super-Adaptoid",
        ]

    @functools.cached_property
    def masterminds_heroes_of_asgard(self) -> List[str]:
        return [
            "Hela, Goddess of Death",
            "Malekith the Accursed",
        ]

    @functools.cached_property
    def masterminds_the_new_mutants(self) -> List[str]:
        return [
            "Belasco, Demon Lord of Limbo",
            "Emma Frost, The White Queen",
        ]

    @functools.cached_property
    def masterminds_into_the_cosmos(self) -> List[str]:
        return [
            "The Beyonder",
            "The Grandmaster",
            "Magus",
        ]

    @functools.cached_property
    def masterminds_realm_of_kings(self) -> List[str]:
        return [
            "Emperor Vulcan of the Shi'ar",
            "Maximus the Mad",
        ]

    @functools.cached_property
    def masterminds_annihilation(self) -> List[str]:
        return [
            "Annihilus",
            "Kang the Conqueror",
        ]

    @functools.cached_property
    def masterminds_messiah_complex(self) -> List[str]:
        return [
            "Bastion, Fused Sentinel",
            "Exodus",
            "Lady Deathstrike",
        ]

    @functools.cached_property
    def masterminds_doctor_strange_and_the_shadows_of_nightmare(self) -> List[str]:
        return [
            "Dormammu",
            "Nightmare",
        ]

    @functools.cached_property
    def masterminds_mcu_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Ego, The Living Planet",
            "Ronan the Accuser",
        ]

    @functools.cached_property
    def masterminds_black_panther(self) -> List[str]:
        return [
            "Killmonger",
            "Klaw",
        ]

    @functools.cached_property
    def masterminds_black_widow(self) -> List[str]:
        return [
            "Indestructible Man",
            "Taskmaster",
        ]

    @functools.cached_property
    def masterminds_mcu_infinity_saga(self) -> List[str]:
        return [
            "Ebony Maw",
            "Thanos (MCU)",
        ]

    @functools.cached_property
    def masterminds_midnight_sons(self) -> List[str]:
        return [
            "Lilith, Mother of Demons",
            "Zarathos",
        ]

    @functools.cached_property
    def masterminds_what_if(self) -> List[str]:
        return [
            "Hank Pym, Yellowjacket",
            "Killmonger, The Betrayer",
            "Ultron Infinity",
            "Zombie Scarlet Witch",
        ]

    @functools.cached_property
    def masterminds_mcu_ant_man_and_the_wasp(self) -> List[str]:
        return [
            "Darren Cross",
            "Ghost, Master Thief",
            "Kang, Quantum Conqueror",
        ]

    @functools.cached_property
    def masterminds_2099(self) -> List[str]:
        return [
            "Alchemax Executives",
            "Sinister Six 2099",
        ]

    @functools.cached_property
    def masterminds_weapon_x(self) -> List[str]:
        return [
            "Omega Red",
            "Romulus",
            "Sabretooth",
        ]

    @functools.cached_property
    def masterminds_buffy(self) -> List[str]:
        return [
            "Angelus",
            "The First",
            "Glorificus",
            "The Master",
            "The Mayor",
        ]

    @functools.cached_property
    def masterminds_james_bond_core(self) -> List[str]:
        return [
            "Le Chiffre",
            "Francisco Scaramanga",
            "Alec Trevelyan",
            "Auric Goldfinger",
        ]

    @functools.cached_property
    def masterminds_james_bond_expansion(self) -> List[str]:
        return [
            "Franz Sanchez",
            "Ernst Stavro Blofeld",
        ]

    @functools.cached_property
    def masterminds_james_bond_the_spy_who_loved_me(self) -> List[str]:
        return [
            "Karl Stromberg",
        ]

    @functools.cached_property
    def masterminds_james_bond_no_time_to_die(self) -> List[str]:
        return [
            "Lyutsifer Safin",
        ]

    @functools.cached_property
    def masterminds_big_trouble_in_little_china(self) -> List[str]:
        return [
            "Ching Dai",
            "David Lo Pan",
            "Six Shooter",
            "Sorcerous Lo Pan",
        ]

    def masterminds(self) -> List[str]:
        masterminds: List[str] = list()

        if self.has_core:
            masterminds.extend(self.masterminds_core)
        if self.has_dark_city:
            masterminds.extend(self.masterminds_dark_city)
        if self.has_fantastic_four:
            masterminds.extend(self.masterminds_fantastic_four)
        if self.has_paint_the_town_red:
            masterminds.extend(self.masterminds_paint_the_town_red)
        if self.has_villains:
            masterminds.extend(self.masterminds_villains)
        if self.has_guardians_of_the_galaxy:
            masterminds.extend(self.masterminds_guardians_of_the_galaxy)
        if self.has_fear_itself:
            masterminds.extend(self.masterminds_fear_itself)
        if self.has_secret_wars_vol_1:
            masterminds.extend(self.masterminds_secret_wars_vol_1)
        if self.has_secret_wars_vol_2:
            masterminds.extend(self.masterminds_secret_wars_vol_2)
        if self.has_captain_america_75th_anniversary:
            masterminds.extend(self.masterminds_captain_america_75th_anniversary)
        if self.has_civil_war:
            masterminds.extend(self.masterminds_civil_war)
        if self.has_deadpool:
            masterminds.extend(self.masterminds_deadpool)
        if self.has_noir:
            masterminds.extend(self.masterminds_noir)
        if self.has_x_men:
            masterminds.extend(self.masterminds_x_men)
        if self.has_spider_man_homecoming:
            masterminds.extend(self.masterminds_spider_man_homecoming)
        if self.has_champions:
            masterminds.extend(self.masterminds_champions)
        if self.has_world_war_hulk:
            masterminds.extend(self.masterminds_world_war_hulk)
        if self.has_mcu_phase_1_unique_cards:
            masterminds.extend(self.masterminds_mcu_phase_1_unique_cards)
        if self.has_ant_man:
            masterminds.extend(self.masterminds_ant_man)
        if self.has_venom:
            masterminds.extend(self.masterminds_venom)
        if self.has_dimensions:
            masterminds.extend(self.masterminds_dimensions)
        if self.has_revelations:
            masterminds.extend(self.masterminds_revelations)
        if self.has_shield:
            masterminds.extend(self.masterminds_shield)
        if self.has_heroes_of_asgard:
            masterminds.extend(self.masterminds_heroes_of_asgard)
        if self.has_the_new_mutants:
            masterminds.extend(self.masterminds_the_new_mutants)
        if self.has_into_the_cosmos:
            masterminds.extend(self.masterminds_into_the_cosmos)
        if self.has_realm_of_kings:
            masterminds.extend(self.masterminds_realm_of_kings)
        if self.has_annihilation:
            masterminds.extend(self.masterminds_annihilation)
        if self.has_messiah_complex:
            masterminds.extend(self.masterminds_messiah_complex)
        if self.has_doctor_strange_and_the_shadows_of_nightmare:
            masterminds.extend(self.masterminds_doctor_strange_and_the_shadows_of_nightmare)
        if self.has_mcu_guardians_of_the_galaxy:
            masterminds.extend(self.masterminds_mcu_guardians_of_the_galaxy)
        if self.has_black_panther:
            masterminds.extend(self.masterminds_black_panther)
        if self.has_black_widow:
            masterminds.extend(self.masterminds_black_widow)
        if self.has_mcu_infinity_saga:
            masterminds.extend(self.masterminds_mcu_infinity_saga)
        if self.has_midnight_sons:
            masterminds.extend(self.masterminds_midnight_sons)
        if self.has_what_if:
            masterminds.extend(self.masterminds_what_if)
        if self.has_mcu_ant_man_and_the_wasp:
            masterminds.extend(self.masterminds_mcu_ant_man_and_the_wasp)
        if self.has_2099:
            masterminds.extend(self.masterminds_2099)
        if self.has_weapon_x:
            masterminds.extend(self.masterminds_weapon_x)
        if self.has_buffy:
            masterminds.extend(self.masterminds_buffy)
        if self.has_james_bond_core:
            masterminds.extend(self.masterminds_james_bond_core)
        if self.has_james_bond_expansion:
            masterminds.extend(self.masterminds_james_bond_expansion)
        if self.has_james_bond_the_spy_who_loved_me:
            masterminds.extend(self.masterminds_james_bond_the_spy_who_loved_me)
        if self.has_james_bond_no_time_to_die:
            masterminds.extend(self.masterminds_james_bond_no_time_to_die)
        if self.has_big_trouble_in_little_china:
            masterminds.extend(self.masterminds_big_trouble_in_little_china)

        return masterminds

    @functools.cached_property
    def villain_groups_core(self) -> List[str]:
        return [
            "Brotherhood",
            "Enemies of Asgard",
            "Hydra",
            "Masters of Evil",
            "Radiation",
            "Skrulls",
            "Spider-Foes",
        ]

    @functools.cached_property
    def villain_groups_dark_city(self) -> List[str]:
        return [
            "Emissaries of Evil",
            "Four Horsemen",
            "Marauders",
            "MLF",
            "Streets of New York",
            "Underworld",
        ]

    @functools.cached_property
    def villain_groups_fantastic_four(self) -> List[str]:
        return [
            "Heralds of Galactus",
            "Subterranea",
        ]

    @functools.cached_property
    def villain_groups_paint_the_town_red(self) -> List[str]:
        return [
            "Maximum Carnage",
            "Sinister Six",
        ]

    @functools.cached_property
    def villain_groups_villains(self) -> List[str]:
        return [
            "Avengers",
            "Defenders",
            "Marvel Knights",
            "Spider-Friends",
            "Uncanny Avengers",
            "Uncanny X-Men",
            "X-Men First Class",
        ]

    @functools.cached_property
    def villain_groups_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Infinity Gems",
            "Kree Starforce",
        ]

    @functools.cached_property
    def villain_groups_fear_itself(self) -> List[str]:
        return [
            "The Mighty",
        ]

    @functools.cached_property
    def villain_groups_secret_wars_vol_1(self) -> List[str]:
        return [
            "The Deadlands",
            "Domain of Apocalypse",
            "Limbo",
            "Manhattan (Earth-1610)",
            "Sentinel Territories",
            "Wasteland",
        ]

    @functools.cached_property
    def villain_groups_secret_wars_vol_2(self) -> List[str]:
        return [
            "Deadpool's Secret Secret Wars",
            "Guardians of Knowhere",
            "K'un Lun",
            "Monster Metropolis",
            "Utopolis",
            "X-Men '92",
        ]

    @functools.cached_property
    def villain_groups_captain_america_75th_anniversary(self) -> List[str]:
        return [
            "Masters of Evil (WWII)",
            "Zola's Creations",
        ]

    @functools.cached_property
    def villain_groups_civil_war(self) -> List[str]:
        return [
            "CSA Special Marshals",
            "Great Lake Avengers",
            "Heroes for Hire",
            "Registration Enforcers",
            "S.H.I.E.L.D. Elite",
            "Superhuman Registration Act",
            "Thunderbolts",
        ]

    @functools.cached_property
    def villain_groups_deadpool(self) -> List[str]:
        return [
            "Deadpool's 'Friends'",
            "Evil Deadpool Corpse",
        ]

    @functools.cached_property
    def villain_groups_noir(self) -> List[str]:
        return [
            "Goblin's Freak Show",
            "X-Men Noir",
        ]

    @functools.cached_property
    def villain_groups_x_men(self) -> List[str]:
        return [
            "Dark Descendants",
            "Hellfire Club",
            "Mojoverse",
            "Murderworld",
            "Shadow-X",
            "Shi'ar Imperial Guard",
            "Sisterhood of Mutants",
        ]

    @functools.cached_property
    def villain_groups_spider_man_homecoming(self) -> List[str]:
        return [
            "Salvagers",
            "Vulture Tech",
        ]

    @functools.cached_property
    def villain_groups_champions(self) -> List[str]:
        return [
            "Monsters Unleashed",
            "Wrecking Crew",
        ]

    @functools.cached_property
    def villain_groups_world_war_hulk(self) -> List[str]:
        return [
            "Aspects of the Void",
            "Code Red",
            "Illuminati",
            "Intelligencia",
            "Sakaar Imperial Guard",
            "U-Foes",
            "Warbound",
        ]

    @functools.cached_property
    def villain_groups_mcu_phase_1_unique_cards(self) -> List[str]:
        return [
            "Chitauri",
            "Gamma Hunters",
            "Iron Foes",
        ]

    @functools.cached_property
    def villain_groups_ant_man(self) -> List[str]:
        return [
            "Queen's Vengeance",
            "Ultron's Legacy",
        ]

    @functools.cached_property
    def villain_groups_venom(self) -> List[str]:
        return [
            "Life Foundation",
            "Poisons",
        ]

    @functools.cached_property
    def villain_groups_revelations(self) -> List[str]:
        return [
            "Army of Evil",
            "Dark Avengers",
            "Hood's Gang",
            "Lethal Legion",
        ]

    @functools.cached_property
    def villain_groups_shield(self) -> List[str]:
        return [
            "A.I.M., Hydra Offshoot",
            "Hydra Elite",
        ]

    @functools.cached_property
    def villain_groups_heroes_of_asgard(self) -> List[str]:
        return [
            "Dark Council",
            "Omens of Ragnarok",
        ]

    @functools.cached_property
    def villain_groups_the_new_mutants(self) -> List[str]:
        return [
            "Demons of Limbo",
            "Hellions",
        ]

    @functools.cached_property
    def villain_groups_into_the_cosmos(self) -> List[str]:
        return [
            "Black Order of Thanos",
            "Celestials",
            "Elders of the Universe",
            "From Beyond",
        ]

    @functools.cached_property
    def villain_groups_realm_of_kings(self) -> List[str]:
        return [
            "Inhuman Rebellion",
            "Shi'ar Imperial Elite",
        ]

    @functools.cached_property
    def villain_groups_annihilation(self) -> List[str]:
        return [
            "Annihilation Wave",
            "Timelines of Kang",
        ]

    @functools.cached_property
    def villain_groups_messiah_complex(self) -> List[str]:
        return [
            "Acolytes",
            "Clan Yashida",
            "Purifiers",
            "Reavers",
        ]

    @functools.cached_property
    def villain_groups_doctor_strange_and_the_shadows_of_nightmare(self) -> List[str]:
        return [
            "Fear Lords",
            "Lords of the Netherworld",
        ]

    @functools.cached_property
    def villain_groups_mcu_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Followers of Ronan",
            "Ravagers",
        ]

    @functools.cached_property
    def villain_groups_black_panther(self) -> List[str]:
        return [
            "Enemies of Wakanda",
            "Killmonger's League",
        ]

    @functools.cached_property
    def villain_groups_black_widow(self) -> List[str]:
        return [
            "Elite Assassins",
            "Taskmaster's Thunderbolts",
        ]

    @functools.cached_property
    def villain_groups_mcu_infinity_saga(self) -> List[str]:
        return [
            "Children of Thanos",
            "Infinity Stones",
        ]

    @functools.cached_property
    def villain_groups_midnight_sons(self) -> List[str]:
        return [
            "Fallen",
            "Lilin",
        ]

    @functools.cached_property
    def villain_groups_what_if(self) -> List[str]:
        return [
            "Black Order Guards",
            "Intergalactic Party Animals",
            "Rival Overlords",
            "Strange's Demons",
            "Zombie Avengers",
        ]

    @functools.cached_property
    def villain_groups_mcu_ant_man_and_the_wasp(self) -> List[str]:
        return [
            "Armada of Kang",
            "Cross Technologies",
            "Ghost Chasers",
            "Quantum Realm",
        ]

    @functools.cached_property
    def villain_groups_2099(self) -> List[str]:
        return [
            "Alchemax Enforcers",
            "Flase Aesir of Alchemax",
        ]

    @functools.cached_property
    def villain_groups_weapon_x(self) -> List[str]:
        return [
            "Berserkers",
            "Weapon Plus",
        ]

    @functools.cached_property
    def villain_groups_buffy(self) -> List[str]:
        return [
            "Demons",
            "The First's Minions",
            "Glory's Minions",
            "Harmony's Gang",
            "Mayor's Minions",
            "Order of Aurelius",
            "The Scourge of Europe",
        ]

    @functools.cached_property
    def villain_groups_james_bond_core(self) -> List[str]:
        return [
            "Casino Royale",
            "The Man with the Golden Gun",
            "Goldeneye",
            "Goldfinger",
        ]

    @functools.cached_property
    def villain_groups_james_bond_expansion(self) -> List[str]:
        return [
            "Licence to Kill",
            "On Her Majesty's Secret Service",
        ]

    @functools.cached_property
    def villain_groups_james_bond_the_spy_who_loved_me(self) -> List[str]:
        return [
            "The Spy who Loved Me",
        ]

    @functools.cached_property
    def villain_groups_james_bond_no_time_to_die(self) -> List[str]:
        return [
            "No Time to Die",
        ]

    @functools.cached_property
    def villain_groups_big_trouble_in_little_china(self) -> List[str]:
        return [
            "Monsters",
            "Warriors of Lo Pan",
            "Wing Kong Exchange",
            "Wing Kong Gang",
        ]

    def villain_groups(self) -> List[str]:
        villain_groups: List[str] = list()

        if self.has_core:
            villain_groups.extend(self.villain_groups_core)
        if self.has_dark_city:
            villain_groups.extend(self.villain_groups_dark_city)
        if self.has_fantastic_four:
            villain_groups.extend(self.villain_groups_fantastic_four)
        if self.has_paint_the_town_red:
            villain_groups.extend(self.villain_groups_paint_the_town_red)
        if self.has_villains:
            villain_groups.extend(self.villain_groups_villains)
        if self.has_guardians_of_the_galaxy:
            villain_groups.extend(self.villain_groups_guardians_of_the_galaxy)
        if self.has_fear_itself:
            villain_groups.extend(self.villain_groups_fear_itself)
        if self.has_secret_wars_vol_1:
            villain_groups.extend(self.villain_groups_secret_wars_vol_1)
        if self.has_secret_wars_vol_2:
            villain_groups.extend(self.villain_groups_secret_wars_vol_2)
        if self.has_captain_america_75th_anniversary:
            villain_groups.extend(self.villain_groups_captain_america_75th_anniversary)
        if self.has_civil_war:
            villain_groups.extend(self.villain_groups_civil_war)
        if self.has_deadpool:
            villain_groups.extend(self.villain_groups_deadpool)
        if self.has_noir:
            villain_groups.extend(self.villain_groups_noir)
        if self.has_x_men:
            villain_groups.extend(self.villain_groups_x_men)
        if self.has_spider_man_homecoming:
            villain_groups.extend(self.villain_groups_spider_man_homecoming)
        if self.has_champions:
            villain_groups.extend(self.villain_groups_champions)
        if self.has_world_war_hulk:
            villain_groups.extend(self.villain_groups_world_war_hulk)
        if self.has_mcu_phase_1_unique_cards:
            villain_groups.extend(self.villain_groups_mcu_phase_1_unique_cards)
        if self.has_ant_man:
            villain_groups.extend(self.villain_groups_ant_man)
        if self.has_venom:
            villain_groups.extend(self.villain_groups_venom)
        if self.has_revelations:
            villain_groups.extend(self.villain_groups_revelations)
        if self.has_shield:
            villain_groups.extend(self.villain_groups_shield)
        if self.has_heroes_of_asgard:
            villain_groups.extend(self.villain_groups_heroes_of_asgard)
        if self.has_the_new_mutants:
            villain_groups.extend(self.villain_groups_the_new_mutants)
        if self.has_into_the_cosmos:
            villain_groups.extend(self.villain_groups_into_the_cosmos)
        if self.has_realm_of_kings:
            villain_groups.extend(self.villain_groups_realm_of_kings)
        if self.has_annihilation:
            villain_groups.extend(self.villain_groups_annihilation)
        if self.has_messiah_complex:
            villain_groups.extend(self.villain_groups_messiah_complex)
        if self.has_doctor_strange_and_the_shadows_of_nightmare:
            villain_groups.extend(self.villain_groups_doctor_strange_and_the_shadows_of_nightmare)
        if self.has_mcu_guardians_of_the_galaxy:
            villain_groups.extend(self.villain_groups_mcu_guardians_of_the_galaxy)
        if self.has_black_panther:
            villain_groups.extend(self.villain_groups_black_panther)
        if self.has_black_widow:
            villain_groups.extend(self.villain_groups_black_widow)
        if self.has_mcu_infinity_saga:
            villain_groups.extend(self.villain_groups_mcu_infinity_saga)
        if self.has_midnight_sons:
            villain_groups.extend(self.villain_groups_midnight_sons)
        if self.has_what_if:
            villain_groups.extend(self.villain_groups_what_if)
        if self.has_mcu_ant_man_and_the_wasp:
            villain_groups.extend(self.villain_groups_mcu_ant_man_and_the_wasp)
        if self.has_2099:
            villain_groups.extend(self.villain_groups_2099)
        if self.has_weapon_x:
            villain_groups.extend(self.villain_groups_weapon_x)
        if self.has_buffy:
            villain_groups.extend(self.villain_groups_buffy)
        if self.has_james_bond_core:
            villain_groups.extend(self.villain_groups_james_bond_core)
        if self.has_james_bond_expansion:
            villain_groups.extend(self.villain_groups_james_bond_expansion)
        if self.has_james_bond_the_spy_who_loved_me:
            villain_groups.extend(self.villain_groups_james_bond_the_spy_who_loved_me)
        if self.has_james_bond_no_time_to_die:
            villain_groups.extend(self.villain_groups_james_bond_no_time_to_die)
        if self.has_big_trouble_in_little_china:
            villain_groups.extend(self.villain_groups_big_trouble_in_little_china)

        return villain_groups

    @functools.cached_property
    def henchmen_core(self) -> List[str]:
        return [
            "Doombot Legion",
            "Hand Ninjas",
            "Savage Land Mutates",
            "Sentinel",
        ]

    @functools.cached_property
    def henchmen_dark_city(self) -> List[str]:
        return [
            "Maggia Goons",
            "Phalanx",
        ]

    @functools.cached_property
    def henchmen_villains(self) -> List[str]:
        return [
            "Cops",
            "Multiple Man",
            "S.H.I.E.L.D. Assault Squad",
            "Asgardian Warrior",
        ]

    @functools.cached_property
    def henchmen_secret_wars_vol_1(self) -> List[str]:
        return [
            "Thor Corps",
            "Ghost Racers",
            "M.O.D.O.K.s",
        ]

    @functools.cached_property
    def henchmen_secret_wars_vol_2(self) -> List[str]:
        return [
            "Khonshu Guardians",
            "Magma Men",
            "Spider-Infected",
        ]

    @functools.cached_property
    def henchmen_civil_war(self) -> List[str]:
        return [
            "Cape-Killers",
            "Mandroid",
        ]

    @functools.cached_property
    def henchmen_x_men(self) -> List[str]:
        return [
            "The Brood",
            "Shi'ar Death Commandos",
            "Hellfire Cult",
            "Sapien League",
            "Shi'ar Patrol Craft",
        ]

    @functools.cached_property
    def henchmen_world_war_hulk(self) -> List[str]:
        return [
            "Death's Heads",
            "Cytoplasm Spikes",
            "Sakaaran Hivelings",
        ]

    @functools.cached_property
    def henchmen_dimensions(self) -> List[str]:
        return [
            "Spider-Slayer",
            "Circus of Crime",
        ]

    @functools.cached_property
    def henchmen_revelations(self) -> List[str]:
        return [
            "Mandarin's Rings",
            "Hydra Base",
        ]

    @functools.cached_property
    def henchmen_into_the_cosmos(self) -> List[str]:
        return [
            "Universal Church of Truth",
            "Sidera Maris, Bridge Builders",
        ]

    @functools.cached_property
    def henchmen_messiah_complex(self) -> List[str]:
        return [
            "Sentinel Squad O*N*E*",
            "Mr. Sinister Clones",
        ]

    @functools.cached_property
    def henchmen_what_if(self) -> List[str]:
        return [
            "Giants of Jotunheim",
            "Ultron Sentries",
            "Vibranium Liberator Drones",
        ]

    @functools.cached_property
    def henchmen_mcu_ant_man_and_the_wasp(self) -> List[str]:
        return [
            "Quantumnauts",
            "Quantum Hound",
            "Lardigrade",
        ]

    @functools.cached_property
    def henchmen_buffy(self) -> List[str]:
        return [
            "Hellhounds",
            "Vampire Initiate",
            "Harbingers of Death",
            "Shark Gangsters",
            "Turok-Han Vampires",
        ]

    @functools.cached_property
    def henchmen_james_bond_core(self) -> List[str]:
        return [
            "Embassy Guards",
            "Martial Arts Students",
            "Russian Soldiers",
            "Fort Knox Assault Team",
        ]

    @functools.cached_property
    def henchmen_james_bond_expansion(self) -> List[str]:
        return [
            "Wavekrest Divers",
            "Institute Guards",
        ]

    @functools.cached_property
    def henchmen_james_bond_the_spy_who_loved_me(self) -> List[str]:
        return [
            "Liparus Soldiers",
        ]

    @functools.cached_property
    def henchmen_james_bond_no_time_to_die(self) -> List[str]:
        return [
            "Spectre Infiltrators",
        ]

    @functools.cached_property
    def henchmen_big_trouble_in_little_china(self) -> List[str]:
        return [
            "Ceremonial Warrior",
            "Lords of Death",
            "Wing Kong Thugs",
        ]

    def henchmen(self) -> List[str]:
        henchmen: List[str] = list()

        if self.has_core:
            henchmen.extend(self.henchmen_core)
        if self.has_dark_city:
            henchmen.extend(self.henchmen_dark_city)
        if self.has_villains:
            henchmen.extend(self.henchmen_villains)
        if self.has_secret_wars_vol_1:
            henchmen.extend(self.henchmen_secret_wars_vol_1)
        if self.has_secret_wars_vol_2:
            henchmen.extend(self.henchmen_secret_wars_vol_2)
        if self.has_civil_war:
            henchmen.extend(self.henchmen_civil_war)
        if self.has_x_men:
            henchmen.extend(self.henchmen_x_men)
        if self.has_world_war_hulk:
            henchmen.extend(self.henchmen_world_war_hulk)
        if self.has_dimensions:
            henchmen.extend(self.henchmen_dimensions)
        if self.has_revelations:
            henchmen.extend(self.henchmen_revelations)
        if self.has_into_the_cosmos:
            henchmen.extend(self.henchmen_into_the_cosmos)
        if self.has_messiah_complex:
            henchmen.extend(self.henchmen_messiah_complex)
        if self.has_what_if:
            henchmen.extend(self.henchmen_what_if)
        if self.has_mcu_ant_man_and_the_wasp:
            henchmen.extend(self.henchmen_mcu_ant_man_and_the_wasp)
        if self.has_buffy:
            henchmen.extend(self.henchmen_buffy)
        if self.has_james_bond_core:
            henchmen.extend(self.henchmen_james_bond_core)
        if self.has_james_bond_expansion:
            henchmen.extend(self.henchmen_james_bond_expansion)
        if self.has_james_bond_the_spy_who_loved_me:
            henchmen.extend(self.henchmen_james_bond_the_spy_who_loved_me)
        if self.has_james_bond_no_time_to_die:
            henchmen.extend(self.henchmen_james_bond_no_time_to_die)
        if self.has_big_trouble_in_little_china:
            henchmen.extend(self.henchmen_big_trouble_in_little_china)

        return henchmen

    @functools.cached_property
    def schemes_core(self) -> List[str]:
        return [
            "The Legacy Virus",
            "Midtown Bank Robbery",
            "Negative Zone Prison Breakout",
            "Portals to the Dark Dimension",
            "Replace Earth's Leaders with Killbots",
            "Secret Invasion of the Skrull Shapeshifters",
            "Super Hero Civil War",
            "Unleash the Power of the Cosmic Cube",
        ]

    @functools.cached_property
    def schemes_dark_city(self) -> List[str]:
        return [
            "Capture Baby Hope",
            "Detonate the Helicarrier",
            "Massive Earthquake Generator",
            "Organized Crime Wave",
            "Save Humanity",
            "Steal the Weaponized Plutonium",
            "Transform Citizens into Demons",
            "X-Cutioner's Song",
        ]

    @functools.cached_property
    def schemes_fantastic_four(self) -> List[str]:
        return [
            "Bathe Earth in Cosmic Rays",
            "Flood the Planet with Melted Glaciers",
            "Invincible Force Field",
            "Pull Reality into the Negative Zone",
        ]

    @functools.cached_property
    def schemes_paint_the_town_red(self) -> List[str]:
        return [
            "The Clone Saga",
            "Invade the Daily Bugle News HQ",
            "Splice Humans with Spider DNA",
            "Weave a Web of Lies",
        ]

    @functools.cached_property
    def schemes_villains(self) -> List[str]:
        return [
            "Build an Underground Mega-Vault Prison",
            "Cage Villains in Power Suppressing Cells",
            "Crown Thor King of Asgard",
            "Crush Hydra",
            "Graduation at Xavier's X-Academy",
            "Infiltrate the Lair with Spies",
            "Mass Produce War Machine Armor",
            "Resurrect Heroes with the Norn Stones",
        ]

    @functools.cached_property
    def schemes_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Forge the Infinity Gauntlet",
            "Intergalactic Kree Nega-Bomb",
            "The Kree-Skrull War",
            "Unite the Shards",
        ]

    @functools.cached_property
    def schemes_fear_itself(self) -> List[str]:
        return [
            "Last Stand at Avengers Tower",
            "Fear Itself",
            "The Traitor",
        ]

    @functools.cached_property
    def schemes_secret_wars_vol_1(self) -> List[str]:
        return [
            "Build an Army of Annihilation",
            "Corrupt the Next Generation of Heroes",
            "Crush Them with My Bare Hands",
            "Dark Alliance",
            "Fragmented Realities",
            "Master of Tyrants",
            "Pan-Dimensional Plague",
            "Smash Two Dimensions Together",
        ]

    @functools.cached_property
    def schemes_secret_wars_vol_2(self) -> List[str]:
        return [
            "Deadlands Hordes Charge the Wall",
            "Enthrone the Barons of Battleworld",
            "The Fountain of Eternal Life",
            "The God-Emperor of Battleworld",
            "The Mark of Khonshu",
            "Master the Mysteries of Kung-Fu",
            "Secret Wars",
            "Sinister Ambitions",
        ]

    @functools.cached_property
    def schemes_captain_america_75th_anniversary(self) -> List[str]:
        return [
            "Brainwash the Military",
            "Change the Outcome of WWII",
            "Go Back in Time to Slay Heroes' Ancestors",
            "The Unbreakable Enigma Code",
        ]

    @functools.cached_property
    def schemes_civil_war(self) -> List[str]:
        return [
            "Avengers vs. X-Men",
            "Dark Reign of H.A.M.M.E.R. Officers",
            "Epic Super Hero Civil War",
            "Imprison Unregistered Superhumans",
            "Nitro the Supervillain Threatens Crowds",
            "Predict Future Crime",
            "Reveal Heroes' Secret Identities",
            "United States Split by Civil War",
        ]

    @functools.cached_property
    def schemes_deadpool(self) -> List[str]:
        return [
            "Deadpool Kills the Marvel Universe",
            "Deadpool Wants a Chimichanga",
            "Deadpool Writes a Scheme",
            "Everybody Hates Deadpool",
        ]

    @functools.cached_property
    def schemes_noir(self) -> List[str]:
        return [
            "Find the Split Personality Killer",
            "Five Families of Crime",
            "Hidden Heart of Darkness",
            "Silence the Witnesses",
        ]

    @functools.cached_property
    def schemes_x_men(self) -> List[str]:
        return [
            "Alien Brood Encounters",
            "Anti-Mutant Hatred",
            "The Dark Phoenix Saga",
            "Horror of Horrors",
            "Mutant-Hunting Super Sentinels",
            "Nuclear Armageddon",
            "Televised Deathtraps of Mojoworld",
            "X-Men Danger Room Goes Berserk",
        ]

    @functools.cached_property
    def schemes_spider_man_homecoming(self) -> List[str]:
        return [
            "Distract the Hero",
            "Explosion at the Washington Monument",
            "Ferry Disaster",
            "Scavenge Alien Weaponry",
        ]

    @functools.cached_property
    def schemes_champions(self) -> List[str]:
        return [
            "Clash of the Monsters Unleashed",
            "Divide and Conquer",
            "Hypnotize Every Human",
            "Steal All Oxygen on Earth",
        ]

    @functools.cached_property
    def schemes_world_war_hulk(self) -> List[str]:
        return [
            "Break the Planet Asunder",
            "Cytoplasm Spike Invasion",
            "Fall of the Hulks",
            "Gladiator Pits of Sakaar",
            "Mutating Gamma Rays",
            "Shoot Hulk into Space",
            "Subjugate with Obedience Disks",
            "World War Hulk",
        ]

    @functools.cached_property
    def schemes_mcu_phase_1_unique_cards(self) -> List[str]:
        return [
            "Enslave Minds with the Chitauri Scepter",
        ]

    @functools.cached_property
    def schemes_ant_man(self) -> List[str]:
        return [
            "Age of Ultron",
            "Pull Earth into Medieval Times",
            "Transform Commuters into Giant Ants",
            "Trap Heroes in the Microverse",
        ]

    @functools.cached_property
    def schemes_venom(self) -> List[str]:
        return [
            "Invasion of the Venom Symbiotes",
            "Maximum Carnage",
            "Paralyzing Venom",
            "Symbiotic Absorption",
        ]

    @functools.cached_property
    def schemes_revelations(self) -> List[str]:
        return [
            "Earthquake Drains the Ocean",
            "House of M",
            "The Korvac Saga",
            "Secret Hydra Corruption",
        ]

    @functools.cached_property
    def schemes_shield(self) -> List[str]:
        return [
            "Hail Hydra",
            "Hydra Helicarriers Hunt Heroes",
            "S.H.I.E.L.D. vs. Hydra War",
            "Secret Empire of Betrayal",
        ]

    @functools.cached_property
    def schemes_heroes_of_asgard(self) -> List[str]:
        return [
            "Asgardian Test of Worth",
            "The Dark World of Svartaleheim",
            "Ragnarok, Twilight of the Gods",
            "War of the Frost Giants",
        ]

    @functools.cached_property
    def schemes_the_new_mutants(self) -> List[str]:
        return [
            "Crash the Moon into the Sun",
            "The Demon Bear Saga",
            "Superhuman Baseball Game",
            "Trapped in the Insane Asylum",
        ]

    @functools.cached_property
    def schemes_into_the_cosmos(self) -> List[str]:
        return [
            "Annihilation: Conquest",
            "The Contest of Champions",
            "Destroy the Nova Corps",
            "Turn the Soul of Adam Warlock",
        ]

    @functools.cached_property
    def schemes_realm_of_kings(self) -> List[str]:
        return [
            "Ruin the Perfect Wedding",
            "Devolve with Xerogen Crystals",
            "Tornado of Terrigen Mists",
            "War of Kings",
        ]

    @functools.cached_property
    def schemes_annihilation(self) -> List[str]:
        return [
            "Breach Parallel Dimensions",
            "Pulse Waves from the Negative Zone",
            "Put Humanity on Trial",
            "Sneak Attack the Heroes' Homes",
        ]

    @functools.cached_property
    def schemes_messiah_complex(self) -> List[str]:
        return [
            "Drain Mutants' Powers to...",
            "Hack Cerebro Servers to...",
            "Hire Singularity Investigations to...",
            "Raid Gene Banks to...",
        ]

    @functools.cached_property
    def schemes_doctor_strange_and_the_shadows_of_nightmare(self) -> List[str]:
        return [
            "Cursed Pages of the Darkhold Tome",
            "Duels of Science and Magic",
            "Claim Souls for Demons",
            "War for the Dream Dimension",
        ]

    @functools.cached_property
    def schemes_mcu_guardians_of_the_galaxy(self) -> List[str]:
        return [
            "Inescapable 'Kyln' Space Prison",
            "Provoke the Sovereign War Fleet",
            "Star-Lord's Awesome Mix Tape",
            "Unleash the Abilisk Space Monster",
        ]

    @functools.cached_property
    def schemes_black_panther(self) -> List[str]:
        return [
            "Poison Lakes with Nanite Microbots",
            "Plunder Wakanda's Vibranium",
            "Provoke a Clash of Nations",
            "Seize the Wakandan Throne",
        ]

    @functools.cached_property
    def schemes_black_widow(self) -> List[str]:
        return [
            "Frame Heroes for Murder",
            "Corrupt the Spy Agenies",
            "Sniper Rifle Assassins",
            "Train Black Widows in the Red Room",
        ]

    @functools.cached_property
    def schemes_mcu_infinity_saga(self) -> List[str]:
        return [
            "Halve All Life in the Universe",
            "Sacrifice for the Soul Stone",
            "The Time Heist",
            "Warp Reality into a TV Show",
        ]

    @functools.cached_property
    def schemes_midnight_sons(self) -> List[str]:
        return [
            "Midnight Massacre",
            "Ritual Sacrifice to Summon Cthon",
            "Sire Vampires at the Blood Bank",
            "Wager at Blackjack for Heroes' Souls",
        ]

    @functools.cached_property
    def schemes_what_if(self) -> List[str]:
        return [
            "Breach the Nexus of All Realities",
            "Collect an Interstellar Zoo",
            "Marvel Zombies",
            "Trash Earth with the Hugest Party Ever",
        ]

    @functools.cached_property
    def schemes_mcu_ant_man_and_the_wasp(self) -> List[str]:
        return [
            "Auction Shrink Tech to Highest Bidder",
            "Escape an Imprisoning Dimension",
            "Safeguard Dark Secrets",
            "Siphon Energy from the Quantum Realm",
        ]

    @functools.cached_property
    def schemes_2099(self) -> List[str]:
        return [
            "Become President of the United States",
            "Befoul Earth into a Polluted Wasteland",
            "Pull Reality into Cyberspace",
            "Subjugate Earth with Mega-Corporations",
        ]

    @functools.cached_property
    def schemes_weapon_x(self) -> List[str]:
        return [
            "Condition Logan into Weapon X",
            "Go After Heroes' Loved Ones",
            "Wipe Heroes' Memories",
        ]

    @functools.cached_property
    def schemes_buffy(self) -> List[str]:
        return [
            "Convert to Evil",
            "Darkness Falls",
            "Epic Struggle",
            "Hellmouth Opening",
            "Road to Damnation",
            "Summon the Uber Vamps",
            "Twilight Terror",
            "Vile Agenda",
        ]

    @functools.cached_property
    def schemes_james_bond_core(self) -> List[str]:
        return [
            "Selling Secrets",
            "Win the Casino Royale Tournament",
            "Build a Secret Island Lair",
            "A Duel to the Death",
            "Fake Your Own Death",
            "Worldwide Financial Meltdown",
            "Operation: Grand Slam",
            "Orchestrate a Smuggling Ring",
        ]

    @functools.cached_property
    def schemes_james_bond_expansion(self) -> List[str]:
        return [
            "Escape Custody",
            "Expand Drug Empire",
            "Condition the Angels of Death",
            "Create Omega Virus",
        ]

    @functools.cached_property
    def schemes_james_bond_the_spy_who_loved_me(self) -> List[str]:
        return [
            "Create a New World Beneath the Sea",
            "Incite Nuclear War",
        ]

    @functools.cached_property
    def schemes_james_bond_no_time_to_die(self) -> List[str]:
        return [
            "Defeat James Bond",
            "Project Heracles",
        ]

    @functools.cached_property
    def schemes_big_trouble_in_little_china(self) -> List[str]:
        return [
            "Assassination",
            "Corrupt True Heroes",
            "Destroy Chinatown's Dreams",
            "Enforce Villainous Hierarchy",
            "Fill the Hell of Upside Down Sinners",
            "Flood Chinatown in Mediocracy",
            "Forge Crime Syndicate",
            "Kill Uncle Chu",
            "One and the Same Person, Jack",
            "Open the Hell Gates",
            "Rampage for Sacrifices",
            "Ruin San Fran",
        ]

    def schemes(self) -> List[str]:
        schemes: List[str] = list()

        if self.has_core:
            schemes.extend(self.schemes_core)
        if self.has_dark_city:
            schemes.extend(self.schemes_dark_city)
        if self.has_fantastic_four:
            schemes.extend(self.schemes_fantastic_four)
        if self.has_paint_the_town_red:
            schemes.extend(self.schemes_paint_the_town_red)
        if self.has_villains:
            schemes.extend(self.schemes_villains)
        if self.has_guardians_of_the_galaxy:
            schemes.extend(self.schemes_guardians_of_the_galaxy)
        if self.has_fear_itself:
            schemes.extend(self.schemes_fear_itself)
        if self.has_secret_wars_vol_1:
            schemes.extend(self.schemes_secret_wars_vol_1)
        if self.has_secret_wars_vol_2:
            schemes.extend(self.schemes_secret_wars_vol_2)
        if self.has_captain_america_75th_anniversary:
            schemes.extend(self.schemes_captain_america_75th_anniversary)
        if self.has_civil_war:
            schemes.extend(self.schemes_civil_war)
        if self.has_deadpool:
            schemes.extend(self.schemes_deadpool)
        if self.has_noir:
            schemes.extend(self.schemes_noir)
        if self.has_x_men:
            schemes.extend(self.schemes_x_men)
        if self.has_spider_man_homecoming:
            schemes.extend(self.schemes_spider_man_homecoming)
        if self.has_champions:
            schemes.extend(self.schemes_champions)
        if self.has_world_war_hulk:
            schemes.extend(self.schemes_world_war_hulk)
        if self.has_mcu_phase_1_unique_cards:
            schemes.extend(self.schemes_mcu_phase_1_unique_cards)
        if self.has_ant_man:
            schemes.extend(self.schemes_ant_man)
        if self.has_venom:
            schemes.extend(self.schemes_venom)
        if self.has_revelations:
            schemes.extend(self.schemes_revelations)
        if self.has_shield:
            schemes.extend(self.schemes_shield)
        if self.has_heroes_of_asgard:
            schemes.extend(self.schemes_heroes_of_asgard)
        if self.has_the_new_mutants:
            schemes.extend(self.schemes_the_new_mutants)
        if self.has_into_the_cosmos:
            schemes.extend(self.schemes_into_the_cosmos)
        if self.has_realm_of_kings:
            schemes.extend(self.schemes_realm_of_kings)
        if self.has_annihilation:
            schemes.extend(self.schemes_annihilation)
        if self.has_messiah_complex:
            schemes.extend(self.schemes_messiah_complex)
        if self.has_doctor_strange_and_the_shadows_of_nightmare:
            schemes.extend(self.schemes_doctor_strange_and_the_shadows_of_nightmare)
        if self.has_mcu_guardians_of_the_galaxy:
            schemes.extend(self.schemes_mcu_guardians_of_the_galaxy)
        if self.has_black_panther:
            schemes.extend(self.schemes_black_panther)
        if self.has_black_widow:
            schemes.extend(self.schemes_black_widow)
        if self.has_mcu_infinity_saga:
            schemes.extend(self.schemes_mcu_infinity_saga)
        if self.has_midnight_sons:
            schemes.extend(self.schemes_midnight_sons)
        if self.has_what_if:
            schemes.extend(self.schemes_what_if)
        if self.has_mcu_ant_man_and_the_wasp:
            schemes.extend(self.schemes_mcu_ant_man_and_the_wasp)
        if self.has_2099:
            schemes.extend(self.schemes_2099)
        if self.has_weapon_x:
            schemes.extend(self.schemes_weapon_x)
        if self.has_buffy:
            schemes.extend(self.schemes_buffy)
        if self.has_james_bond_core:
            schemes.extend(self.schemes_james_bond_core)
        if self.has_james_bond_expansion:
            schemes.extend(self.schemes_james_bond_expansion)
        if self.has_james_bond_the_spy_who_loved_me:
            schemes.extend(self.schemes_james_bond_the_spy_who_loved_me)
        if self.has_james_bond_no_time_to_die:
            schemes.extend(self.schemes_james_bond_no_time_to_die)
        if self.has_big_trouble_in_little_china:
            schemes.extend(self.schemes_big_trouble_in_little_china)

        return schemes


# Archipelago Options
class LegendaryAMarvelDeckBuildingGameSetsExpansionsOwned(OptionSet):
    """
    Indicates which sets and expansions the players owns for Legendary - A Marvel Deck Building Game.
    """

    display_name = "Legendary - A Marvel Deck Building Game Sets & Expansions Owned"
    valid_keys = [
        "Core",
        "Dark City",
        "Fantastic Four",
        "Paint the Town Red",
        "Villains",
        "Guardians of the Galaxy",
        "Fear Itself",
        "Secret Wars Vol. 1",
        "Secret Wars Vol. 2",
        "Captain America 75th Anniversary",
        "Civil War",
        "Deadpool",
        "Noir",
        "X-Men",
        "Spider-Man Homecoming",
        "Champions",
        "World War Hulk",
        "MCU Phase 1 (Unique Cards)",
        "Ant-Man",
        "Venom",
        "Dimensions",
        "Revelations",
        "S.H.I.E.L.D.",
        "Heroes of Asgard",
        "The New Mutants",
        "Into the Cosmos",
        "Realm of Kings",
        "Annihilation",
        "Messiah Complex",
        "Doctor Strange and the Shadows of Nightmare",
        "MCU Guardians of the Galaxy",
        "Black Panther",
        "Black Widow",
        "MCU Infinity Saga",
        "Midnight Sons",
        "What If...?",
        "MCU Ant-Man and the Wasp",
        "2099",
        "Weapon X",
        "Buffy",
        "James Bond Core",
        "James Bond Expansion",
        "James Bond The Spy Who Loved Me",
        "James Bond No Time To Die",
        "Big Trouble in Little China",
    ]

    default = valid_keys
