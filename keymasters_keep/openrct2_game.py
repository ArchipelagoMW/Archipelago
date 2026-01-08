from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet, Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class OpenRCT2ArchipelagoOptions:
    openrct2_include_rct1_content: OpenRCT2IncludeRCT1Content
    openrct2_custom_scenarios: OpenRCT2CustomScenarios


class OpenRCT2Game(Game):
    name = "OpenRCT2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = OpenRCT2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Cannot use Pre-Built Rides",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot set Research Funding to Maximum",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use Pre-Built Rides.  Cannot set Research Funding to Maximum",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot have more than COUNT staff members",
                data={
                    "COUNT": (self.staff_count_range, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use Pre-Built Rides.  Cannot have more than COUNT staff members",
                data={
                    "COUNT": (self.staff_count_range, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Cannot use Marketing Campaigns",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use Pre-Built Rides.  Cannot use Marketing Campaigns",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot borrow more money",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use Pre-Built Rides.  Cannot borrow more money",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the following scenario: SCENARIO",
                data={
                    "SCENARIO": (self.scenarios, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete at least one of the following scenarios a year ahead of schedule: SCENARIOS",
                data={
                    "SCENARIOS": (self.scenarios, 3)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Build a COASTER with an excitement rating of at least RATING",
                data={
                    "COASTER": (self.roller_coasters, 1),
                    "RATING": (self.excitement_rating_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Build the following 2 rides and have them interact with each other: RIDES",
                data={
                    "RIDES": (self.tracked_rides, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Build the following ride, decorated with elements from THEME: RIDE",
                data={
                    "THEME": (self.themes, 1),
                    "RIDE": (self.tracked_rides, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def include_rct1_content(self) -> bool:
        return bool(self.archipelago_options.openrct2_include_rct1_content.value)

    @property
    def custom_scenarios(self) -> List[str]:
        return sorted(self.archipelago_options.openrct2_custom_scenarios.value)

    @functools.cached_property
    def scenarios_rct2(self) -> List[str]:
        return [
            "Electric Fields",
            "Factory Capers",
            "Crazy Castle",
            "Dusty Greens",
            "Bumbly Bazaar",
            "Infernal Views",
            "Lucky Lake",
            "Botany Breakers",
            "Alpine Adventures",
            "Gravity Gardens",
            "Extreme Heights",
            "Amity Airfield",
            "Ghost Town",
            "Fungus Woods",
            "Rainbow Summit",
            "Canyon Calamities",
            "Great Wall of China",
            "Mines of Africa",
            "Ayers Adventure",
            "Rollercoaster Heaven",
            "Mirage Madness",
            "Sugarloaf Shores",
            "Park Maharaja",
            "Over The Edge",
            "Wacky Waikiki",
            "Rainforest Romp",
            "From The Ashes",
            "Icy Adventures",
            "European Extravaganza",
            "Beach Barbecue Blast",
            "Lost City Founder",
            "Okinawa Coast",
            "Sherwood Forest",
            "Crater Carnage",
            "Alcatraz",
            "Extraterrestrial Extravaganza",
            "Schneider Shores",
            "Rocky Rambles",
            "Mythological Madness",
            "Rock 'n' Roll Revival",
            "Gemini City",
            "Metropolis",
            "Woodstock",
            "Cliffside Castle",
            "Animatronic Antics",
            "Coastersaurus",
            "Six Flags Belgium",
            "Six Flags Great Adventure",
            "Six Flags Holland",
            "Six Flags Magic Mountain",
            "Six Flags over Texas",
        ]

    @functools.cached_property
    def scenarios_rct1(self) -> List[str]:
        return [
            "Forest Frontiers",
            "Dynamite Dunes",
            "Leafy Lake",
            "Diamond Heights",
            "Evergreen Gardens",
            "Bumbly Beach",
            "Trinity Islands",
            "Katie's World",
            "Dinky Park",
            "Aqua Park",
            "Millennium Mines",
            "Karts & Coasters",
            "Mel's World",
            "Mothball Mountain",
            "Pacific Pyramids",
            "Crumbly Woods",
            "Big Pier",
            "Lightning Peaks",
            "Ivory Towers",
            "Rainbow Valley",
            "Thunder Rock",
            "Mega Park",
            "Whispering Cliffs",
            "Three Monkeys Park",
            "Canary Mines",
            "Barony Bridge",
            "Funtopia",
            "Haunted Harbor",
            "Fun Fortress",
            "Future World",
            "Gentle Glen",
            "Jolly Jungle",
            "Hydro Hills",
            "Sprightly Park",
            "Magic Quarters",
            "Fruit Farm",
            "Butterfly Dam",
            "Coaster Canyon",
            "Thunderstorm Park",
            "Harmonic Hills",
            "Roman Village",
            "Swamp Cove",
            "Adrenaline Heights",
            "Utopia Park",
            "Rotting Heights",
            "Fiasco Forest",
            "Pickle Park",
            "Giggle Downs",
            "Mineral Park",
            "Coaster Crazy",
            "Urban Park",
            "Geoffrey Gardens",
            "Iceberg Islands",
            "Volcania",
            "Arid Heights",
            "Razor Rocks",
            "Crater Lake",
            "Vertigo Views",
            "Big Pier 2",
            "Dragon's Cove",
            "Good Knight Park",
            "Wacky Warren",
            "Grand Glacier",
            "Crazy Craters",
            "Dusty Desert",
            "Woodworm Park",
            "Icarus Park",
            "Sunny Swamps",
            "Frightmare Hills",
            "Thunder Rocks",
            "Octagon Park",
            "Pleasure Island",
            "Icicle Worlds",
            "Southern Sands",
            "Tiny Towers",
            "Nevermore Park",
            "Pacifica",
            "Urban Jungle",
            "Terror Town",
            "Megaworld Park",
            "Venus Ponds",
            "Micro Park",
            "Alton Towers",
            "Blackpool Pleasure Beach",
            "Heide-Park",
            "Fort Anachronism",
        ]

    def scenarios(self) -> List[str]:
        scenarios: List[str] = self.scenarios_rct2[:]

        if self.include_rct1_content:
            scenarios.extend(self.scenarios_rct1)

        if len(self.custom_scenarios):
            scenarios.extend(self.custom_scenarios)

        return sorted(scenarios)

    @functools.cached_property
    def tracked_rides_rct2(self) -> List[str]:
        return [
            "Chairlift",
            "Elevator",
            "Miniature Railroad",
            "Monorail",
            "Suspended Monorail",
            "Car Ride",
            "Ghost Train",
            "Mini Helicopters",
            "Monster Trucks",
            "Observation Tower",
            "Launched Freefall",
            "Roto-Drop",
            "Dinghy Slide",
            "Log Flume",
            "River Rafts",
            "River Rapids",
            "Splash Boats",
        ]

    @functools.cached_property
    def tracked_rides_rct1(self) -> List[str]:
        return list()

    @functools.cached_property
    def roller_coasters_rct2(self) -> List[str]:
        return [
            "Air Powered Vertical Coaster",
            "Bobsled Coaster",
            "Compact Inverted Coaster",
            "Corkscrew Roller Coaster",
            "Flying Roller Coaster",
            "Giga Coaster",
            "Heartline Twister Coaster",
            "Hybrid Coaster",
            "Hyper-Twister",
            "Hypercoaster",
            "Inverted Hairpin Coaster",
            "Inverted Impulse Coaster",
            "Inverted Roller Coaster",
            "Junior Roller Coaster",
            "LIM Launched Roller Coaster",
            "LSM Launched Roller Coaster",
            "Lay-down Roller Coaster",
            "Looping Roller Coaster",
            "Mine Ride",
            "Mine Train Coaster",
            "Mini Roller Coaster",
            "Mini Suspended Coaster",
            "Multi-Dimension Roller Coaster",
            "Reverse Freefall Coaster",
            "Reverser Roller Coaster",
            "Side-Friction Roller Coaster",
            "Single Rail Roller Coaster",
            "Spinning Wild Mouse",
            "Spiral Roller Coaster",
            "Stand-up Roller Coaster",
            "Steel Wild Mouse",
            "Steeplechase",
            "Suspended Swinging Coaster",
            "Twister Roller Coaster",
            "Vertical Drop Roller Coaster",
            "Virginia Reel",
            "Water Coaster",
            "Wooden Roller Coaster",
            "Wooden Wild Mouse",
        ]

    @functools.cached_property
    def roller_coasters_rct1(self) -> List[str]:
        return [
            "Classic Mini Roller Coaster",
            "Classic Stand-up Roller Coaster",
            "Classic Wooden Roller Coaster",
            "Classic Wooden Twister Roller Coaster",
        ]

    def tracked_rides(self) -> List[str]:
        tracked_rides: List[str] = self.tracked_rides_rct2[:]
        tracked_rides.extend(self.roller_coasters_rct2)

        if self.include_rct1_content:
            tracked_rides.extend(self.tracked_rides_rct1)
            tracked_rides.extend(self.roller_coasters_rct1)

        return sorted(tracked_rides)

    def roller_coasters(self) -> List[str]:
        roller_coasters: List[str] = self.roller_coasters_rct2[:]

        if self.include_rct1_content:
            roller_coasters.extend(self.roller_coasters_rct1)

        return sorted(roller_coasters)

    @functools.cached_property
    def themes_rct2(self) -> List[str]:
        return [
            "Abstract Theming",
            "Africa Theming",
            "Antarctic Theming",
            "Asia Theming",
            "Australasian Theming",
            "Classical/Roman Theming",
            "Creepy Theming",
            "Dark Age Theming",
            "Egyptian Theming",
            "Europe Theming",
            "Future Theming",
            "Giant Candy Theming",
            "Giant Garden Theming",
            "Jungle Theming",
            "Jurassic Theming",
            "Martian Theming",
            "Mechanical Theming",
            "Medieval Theming",
            "Mine Theming",
            "Mythological Theming",
            "North America Theming",
            "Pagoda Theming",
            "Pirates Theming",
            "Prehistoric Theming",
            "Roaring Twenties Theming",
            "Rock 'n' Roll Theming",
            "Snow and Ice Theming",
            "South America Theming",
            "Space Theming",
            "Spooky Theming",
            "Sports Theming",
            "Urban Theming",
            "Water Feature Theming",
            "Wild West Theming",
            "Wonderland Theming",
        ]

    @functools.cached_property
    def themes_rct1(self) -> List[str]:
        return list()

    def themes(self) -> List[str]:
        themes: List[str] = self.themes_rct2[:]

        if self.include_rct1_content:
            themes.extend(self.themes_rct1)

        return sorted(themes)

    @staticmethod
    def excitement_rating_range() -> List[float]:
        return [round(x / 10.0, 2) for x in range(50, 91)]

    @staticmethod
    def staff_count_range() -> range:
        return range(8, 17)


# Archipelago Options
class OpenRCT2IncludeRCT1Content(Toggle):
    """
    Indicates whether to include RollerCoaster Tycoon 1 scenarios and rides when generating objectives.

    Must have the original RollerCoaster Tycoon installed and configured to work with OpenRCT2.
    """

    display_name = "OpenRCT2 Include RollerCoaster Tycoon 1 Content"


class OpenRCT2CustomScenarios(OptionSet):
    """
    Indicates which OpenRCT2 custom scenarios the player has installed.
    """

    display_name = "OpenRCT2 Custom Scenarios"
    default = list()
