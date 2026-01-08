from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ForzaHorizon4ArchipelagoOptions:
    forza_horizon_4_dlc_owned: ForzaHorizon4DLCOwned


class ForzaHorizon4Game(Game):
    name = "Forza Horizon 4"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = ForzaHorizon4ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Set Drivatar Difficulty to DIFFICULTY",
                data={
                    "DIFFICULTY": (self.drivatar_difficulties, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Set Camera View to CAMERA",
                data={
                    "CAMERA": (self.cameras, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Set Driving Assists Difficulty to DIFFICULTY",
                data={
                    "DIFFICULTY": (self.assists, 1),
                },
            ),
            GameObjectiveTemplate(
                label="ASSIST",
                data={
                    "ASSIST": (self.assists_single, 1),
                },
            ),
            GameObjectiveTemplate(
                label="ASSIST and set Drivatar Difficulty to DIFFICULTY",
                data={
                    "ASSIST": (self.assists_single, 1),
                    "DIFFICULTY": (self.drivatar_difficulties, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACK with a car from one of the following brands: BRANDS",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACK": (self.tracks, 1),
                    "BRANDS": (self.car_brands, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACK with a car from one of the following class: CLASS",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACK": (self.tracks, 1),
                    "CLASS": (self.car_classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACK with a car from one of the following type: TYPE",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACK": (self.tracks, 1),
                    "TYPE": (self.car_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACKS with a car from one of the following brands: BRANDS",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACKS": (self.tracks_short, 3),
                    "BRANDS": (self.car_brands, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACKS with a car from one of the following class: CLASS",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACKS": (self.tracks_short, 3),
                    "CLASS": (self.car_classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACKS with a car from one of the following type: TYPE",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACKS": (self.tracks_short, 3),
                    "TYPE": (self.car_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get STAR on the following PR Stunts: STUNTS",
                data={
                    "STAR": (self.stars, 1),
                    "STUNTS": (self.stunts, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Get STAR on the following PR Stunts: STUNTS",
                data={
                    "STAR": (self.stars, 1),
                    "STUNTS": (self.stunts, 5),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Get STAR in the following Story Chapter: STORY",
                data={
                    "STAR": (self.stars, 1),
                    "STORY": (self.stories, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Pull off the following Skills: SKILLS",
                data={
                    "SKILLS": (self.skills, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Pull off the following Skills: SKILLS",
                data={
                    "SKILLS": (self.skills, 5),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.forza_horizon_4_dlc_owned.value)

    @property
    def has_dlc_lego_speed_champions(self) -> bool:
        return "LEGO Speed Champions" in self.dlc_owned

    @property
    def has_dlc_fortune_island(self) -> bool:
        return "Fortune Island" in self.dlc_owned

    @property
    def has_dlc_car_pass(self) -> bool:
        return "Car Pass" in self.dlc_owned

    @property
    def has_dlc_best_of_bond_car_pack(self) -> bool:
        return "Best of Bond Car Pack" in self.dlc_owned

    @functools.cached_property
    def tracks_road_base(self) -> List[str]:
        return [
            "Greendale Super Sprint",
            "Edinburgh Station Circuit",
            "Princes Street Gardens Circuit",
            "Edinburgh City Sprint",
            "Holyrood Park Circuit",
            "Glen Rannoch Hillside Sprint",
            "Greendale Club Sprint",
            "Lakehurst Copse Circuit",
            "The Meadows Sprint",
            "Moorhead Wind Farm Circuit",
            "Bamburgh Coast Circuit",
            "Lakehurst Forest Sprint",
            "Lake District Sprint",
            "Astmoor Heritage Circuit",
            "Elmsdon On Sea Sprint",
            "Broadway Village Circuit",
            "Cotswolds Super Sprint",
            "Horizon Festival Sprint",
            "Horizon Festival Circuit",
            "Waterhead Sprint",
            "Derwent Reservoir Sprint",
            "Ambleside Village Circuit",
            "Ambleside Sprint",
            "Derwent Lakeside Sprint",
            "The Colossus",
            "The Goliath",
        ]

    @functools.cached_property
    def tracks_dirt_base(self) -> List[str]:
        return [
            "Holyrood Park Trail",
            "Greendale Foothills Scramble",
            "Mortimer Gardens Scramble",
            "Derwentwater Trail",
            "Ambleside Scramble",
            "Lakehurst Woodland Scramble",
            "Derwent Reservoir Trail",
            "Lakehurst Forest Trail",
            "White Horse Hill Trail",
            "Ashbrook Loop Scramble",
            "Cotswolds Road Rally Trail",
            "Tarn Hows Scramble",
            "Mudkickers' 4x4 Scramble",
            "Broadway Village Scramble",
            "Highland Farm Scramble",
            "Astmoor Rally Trail",
            "Bamburgh Pinewood Trail",
            "Moorhead Rally Trail",
            "The Gauntlet",
        ]

    @functools.cached_property
    def tracks_cross_country_base(self) -> List[str]:
        return [
            "Riverbank Cross Country Circuit",
            "Windmill Cross Country",
            "Ambleside Rush Cross Country",
            "Ambleside Loop Cross Country",
            "Quarry Cross Country Circuit",
            "Whitewater Falls Cross Country",
            "Beach View Cross Country",
            "Castle Cross Country Circuit",
            "Gardens Cross Country Circuit",
            "Mountain Foot Cross Country",
            "Glen Rannoch Cross Country",
            "Rail Yard Cross Country Circuit",
            "The Ridge Cross Country Circuit",
            "City Outskirts Cross Country",
            "Coastal Rush Cross Country",
            "North City Cross Country Circuit",
            "Arthur's Seat Cross Country",
            "Aerodrome Cross Country Circuit",
            "The Titan",
        ]

    @functools.cached_property
    def tracks_street_base(self) -> List[str]:
        return [
            "Edinburgh New Town",
            "Holyrood Run",
            "_:Nightcity.exe:_",
            "North Coast Rush",
            "The Monument Wynds",
            "Edinburgh Stockbridge",
            "Edinburgh West End",
            "The Highland Charge",
            "Rail Yard Express",
            "Glenfinnan Chase",
            "Mortimer's Pass",
            "Lakehurst Rush",
            "Coastal Charge",
            "Wind Farm Rush",
            "Otleydale Dash",
            "Reservoir Run",
            "Ashbrook Apex",
            "Broadway Crossfire",
            "Batham Gate",
            "Derwent Valley Dash",
            "Ambleside Ascent",
            "The Marathon",
        ]

    @functools.cached_property
    def tracks_lego(self) -> List[str]:
        return [
            "Falcon Loop Circuit",
            "Falcon Arrowhead Circuit",
            "Falcon Indy Circuit",
            "Falcon Speedway Sprint",
            "Valley View Sprint",
            "Lego McLaren Senna Speed Champions Race",
            "North South Sprint",
            "Lego Festival Sprint",
            "Three Fields Circuit",
            "Plastic Flowers Circuit",
            "Brickchester Corners Circuit",
            "Brickchester Loop Circuit",
            "Brick Tree Sprint",
            "Lego Bugatti Chiron Speed Champions Race",
            "Lego Ferrari F40 Speed Champions Race",
            "Oasis Pass Scramble",
            "Oasis Loop Trail",
            "Area 7052 Scramble",
            "Jurassic Graveyard Trail",
            "Countryside Trail",
            "Area 7052 Trail",
            "Brickchester Rally Trail",
            "Lighthouse Scramble",
            "Ocean View Scramble",
            "Falcon Speedway Cross Country",
            "Oasis Jumps Cross Country Circuit",
            "Flower Smash Cross Country",
            "Airport Rush Cross Country Circuit",
            "Brickchester Tour Cross Country",
            "Super Mega Cross Country Circuit",
            "Lego Speed Champions Finale",
            "Lego Goliath",
        ]

    @functools.cached_property
    def tracks_fortune_island(self) -> List[str]:
        return [
            "Fortune's Descent Sprint",
            "The Needle Descent",
            "Woodland Sprint",
            "Fortune Forest Circuit",
            "Moorland Super Circuit",
            "Westwick Festival Circuit",
            "Westwick Wharf Circuit",
            "The Needle Climb",
            "Island Lowland Super Sprint",
            "Fortune's Landing Circuit",
            "South Island Circuit",
            "Northland Rally Trail",
            "Cliffside Scramble",
            "Hilltop Scramble",
            "North Cliff Scramble",
            "Fortune's Folly Trail",
            "Woodland Trail",
            "Fenholm Scramble",
            "The Sinking Scramble",
            "Will-O-Wisp Trail",
            "Westwick Castle Scramble",
            "Southland Super Scramble",
            "Winding Wetland Trail",
            "South Coast Scramble",
            "Island Tour Cross Country",
            "Land's Reach Cross Country",
            "Fenholm Cross Country Circuit",
            "Fortune's Rush Cross Country",
            "Westwick Cross Country Circuit",
            "South Beach Cross Country Circuit",
            "The Kraken",
            "The Leviathan",
        ]

    @functools.cached_property
    def tracks_long(self) -> List[str]:
        return [
            "The Colossus",
            "The Goliath",
            "The Gauntlet",
            "The Titan",
            "The Marathon",
            "Lego Goliath",
            "The Kraken",
            "The Leviathan",
        ]

    def tracks(self) -> List[str]:
        tracks: List[str] = (
            self.tracks_road_base
            + self.tracks_dirt_base
            + self.tracks_cross_country_base
            + self.tracks_street_base
        )

        if self.has_dlc_lego_speed_champions:
            tracks.extend(self.tracks_lego)

        if self.has_dlc_fortune_island:
            tracks.extend(self.tracks_fortune_island)

        return sorted(tracks)

    def tracks_short(self) -> List[str]:
        return sorted(set(self.tracks()) - set(self.tracks_long))

    @functools.cached_property
    def stunts_base(self) -> List[str]:
        return [
            "Deep Vale Speed Trap",
            "Northbridge Speed Trap",
            "Princes Street Speed Trap",
            "Old Town Speed Trap",
            "Calton Hill Speed Trap",
            "Greendale Speed Trap",
            "Aerodrome Speed Trap",
            "M68 Speed Trap",
            "Sylvan Hollow Speed Trap",
            "The Roman Mile Speed Trap",
            "Lower Fell Speed Trap",
            "Wesloch Speed Trap",
            "Cat Bells Speed Trap",
            "Copse Speed Trap",
            "Lakehurst Speed Trap",
            "Moorhead Wind Farm Speed Trap",
            "Astmoor Speed Trap",
            "Derwent Reservoir Speed Trap",
            "Slate Quarry Speed Trap",
            "Hythe House Speed Trap",
            "Horizon Drag Strip Speed Trap",
            "Cotswolds Speed Trap",
            "Oakwood Crest Speed Trap",
            "The Grange Speed Trap",
            "High Street Speed Trap",
            "Peak Moor Speed Trap",
            "Coombe Speed Trap",
            "Bamburgh Dunes Speed Trap",
            "Camelbacks Speed Zone",
            "Derwent Water Speed Zone",
            "Foothills Speed Zone",
            "Hillside Speed Zone",
            "Strathbridge Speed Zone",
            "Glen Rannoch Speed Zone",
            "Royal Botanic Gardens Speed Zone",
            "Johnston Terrace Speed Zone",
            "Royal Terrace Speed Zone",
            "Queen's Drive Speed Zone",
            "Carden Creag Speed Zone",
            "Pennine Way Speed Zone",
            "Rolling Fields Speed Zone",
            "Crescent Speed Zone",
            "The Orchards Speed Zone",
            "Nether End Speed Zone",
            "Brookside Speed Zone",
            "Oldweir Speed Zone",
            "Coppice Speed Zone",
            "Forest Green Speed Zone",
            "Croft Speed Zone",
            "Bridlewood Speed Zone",
            "Broadway Commons Speed Zone",
            "Ambleside Approach Speed Zone",
            "Lakeshore Speed Zone",
            "Toft Speed Zone",
            "The Bridge House Speed Zone",
            "Sudmoss Speed Zone",
            "Roman Ruins Danger Sign",
            "Rannoch Shelf Danger Sign",
            "Rail Yard Ramp Danger Sign",
            "The Great Ridge Danger Sign",
            "Arthur's Seat Danger Sign",
            "Whitewater Falls Danger Sign",
            "Mam Tor Danger Sign",
            "Swan Dive Danger Sign",
            "Bamburgh Castle Danger Sign",
            "Northbound Danger Sign",
            "Mudkickers' Showjump Danger Sign",
            "Leap of Faith Danger Sign",
            "Broadway Windmill Danger Sign",
            "Reservoir Ridge Danger Sign",
            "Open-cast Cliff Danger Sign",
            "Outcrop Crest Danger Sign",
            "Ambleside Edge Danger Sign",
            "Hilltop Vista Danger Sign",
            "Coast View Drift Zone",
            "Kirk Loch Drift Zone",
            "Holyrood Park Drift Zone",
            "City Suburbs Drift Zone",
            "Riverford Drift Zone",
            "Shepherd's Crook Drift Zone",
            "Horseshoe Turn Drift Zone",
            "Mortinmer Gardens Drift Zone",
            "Switchbacks Drift Zone",
            "Otleydale Drift Zone",
            "Moorland Way Drift Zone",
            "Thicket Drift Zone",
            "Ashbrook Lane Drift Zone",
            "Farmstead Drift Zone",
            "Woodland Walk Drift Zone",
            "Horizon Doughnut Drift Zone",
            "S-Bends Drift Zone",
            "Tarn Hows Drift Zone",
            "Sycamore Pastures Drift Zone",
            "Back Lane Drift Zone",
        ]

    @functools.cached_property
    def stunts_lego(self) -> List[str]:
        return [
            "Unidentified Flying Car Danger Sign",
            "Desert's Edge Danger Sign",
            "Brickchester Water Danger Sign",
            "Airport Leap Danger Sign",
            "Stunt Park Overlook Danger Sign",
            "Falcon Speedway Speed Trap",
            "Area 7052 Speed Trap",
            "Brickchester Speed Trap",
            "Stunt Park Speed Trap",
            "Lighthouse Speed Trap",
            "Falcon Corner Speed Zone",
            "Jurassic Graveyard Speed Zone",
            "Brickchester Escape Speed Zone",
            "Little Brickworth Speed Zone",
            "South Valley Speed Zone",
            "Falcon S-Bends Drift Zone",
            "Forest Corners Drift Zone",
            "Hillcrest Drift Zone",
            "Field Lane Drift Zone",
            "Stunt Park Pass Drift Zone",
            "Dunes Run Trailblazer",
            "Desert Escape Trailblazer",
            "Cross City Charge Trailblazer",
            "City Approach Trailblazer",
            "Festival Rush Trailblazer",
        ]

    @functools.cached_property
    def stunts_fortune_island(self) -> List[str]:
        return [
            "The Descent Danger Sign",
            "Needle Fall Danger Sign",
            "North Cliff Danger Sign",
            "Fenholm Ruin's Leap Danger Sign",
            "Wisp Flight Danger Sign",
            "Westwick Launch Danger Sign",
            "Storm Cove Danger Sign",
            "Skildar Watch Danger Sign",
            "Mountainside Speed Trap",
            "Berm Speed Trap",
            "Westwick Speed Trap",
            "Oldlarch Forest Speed Trap",
            "Lady On The Lake Speed Trap",
            "Coastal Cliff Speed Zone",
            "Fenholm Hill Speed Zone",
            "Festival's Apex Speed Zone",
            "Lakeside Speed Zone",
            "Will-O'-The-Wisp Speed Zone",
            "Needle Climb Drift Zone",
            "Skildar Slopes Drift Zone",
            "Merrow's Perch Drift Zone",
            "The Sleeping Giant Drift Zone",
            "Southland Drift Zone",
            "Laufey's Throne Trailblazer",
            "Skildar Head Trailblazer",
            "The Forest Run Trailblazer",
            "Halcyon Point Trailblazer",
            "Viking's Bay Trailblazer",
        ]

    def stunts(self) -> List[str]:
        stunts: List[str] = self.stunts_base[:]

        if self.has_dlc_lego_speed_champions:
            stunts.extend(self.stunts_lego)

        if self.has_dlc_fortune_island:
            stunts.extend(self.stunts_fortune_island)

        return sorted(stunts)

    @functools.cached_property
    def stories_base(self) -> List[str]:
        return [
            "British Racing Green - Second Century",
            "British Racing Green - Utility Vehicle",
            "British Racing Green - The Lotus Spirit",
            "British Racing Green - A Decade of Progress",
            "British Racing Green - 38 MPH",
            "British Racing Green - The Finest Sportscar",
            "British Racing Green - Aftermarket Excellence",
            "British Racing Green - The Art Of Performance",
            "British Racing Green - No. 37",
            "British Racing Green - Unfinished Business",
            "Drift Club - Chapter 1",
            "Drift Club - Chapter 2",
            "Drift Club - Chapter 3",
            "Drift Club - Chapter 4",
            "Drift Club - Chapter 5",
            "Drift Club - Chapter 6",
            "Drift Club - Chapter 7",
            "Drift Club - Chapter 8",
            "Drift Club - Chapter 9",
            "Drift Club - Chapter 10",
            "Laracer @ Horizon - Number 1",
            "Laracer @ Horizon - Number 2",
            "Laracer @ Horizon - Number 3",
            "Laracer @ Horizon - Number 4",
            "Laracer @ Horizon - Number 5",
            "Laracer @ Horizon - Number 6",
            "Laracer @ Horizon - Number 7",
            "Laracer @ Horizon - Number 8",
            "Laracer @ Horizon - Number 9",
            "Laracer @ Horizon - Number 10",
            "Skill Streak - Making Friends and Influencing People...",
            "Skill Streak - Super Sport",
            "Skill Streak - Show Me...",
            "Skill Streak - Open Roads",
            "Skill Streak - Scout",
            "Skill Streak - Industrial Playgrounds",
            "Skill Streak - Skill and Control",
            "Skill Streak - GP",
            "Skill Streak - Dodge This",
            "Skill Streak - Victory Lap",
            "The Stunt Driver - Chapter 1",
            "The Stunt Driver - Chapter 2",
            "The Stunt Driver - Chapter 3",
            "The Stunt Driver - Chapter 4",
            "The Stunt Driver - Chapter 5",
            "The Stunt Driver - Chapter 6",
            "The Stunt Driver - Chapter 7",
            "The Stunt Driver - Chapter 8",
            "The Stunt Driver - Chapter 9",
            "The Stunt Driver - Chapter 10",
            "Top Gear Special - Welcome to the Festival",
            "Top Gear Special - Faster Than 87.2",
            "Top Gear Special - The Austin F-Extreme",
            "Top Gear Special - All the Off-Road You Can E-AT",
            "Top Gear Special - As Grown-Up As You Feel",
            "Top Gear Special - Edinburgh Afternoon Drive",
            "Top Gear Special - One More Thing",
            "Express Delivery - Man and Van",
            "Express Delivery - A Box of Ducks",
            "Express Delivery - Destination Not Found",
            "Express Delivery - Smash on Through",
            "Express Delivery - Shaken (and Stirred)",
            "Express Delivery - Accelerometer Blues",
            "Express Delivery - Long Distance",
            "Express Delivery - Package Relay",
            "Express Delivery - That Sick Drop",
            "Isha's Taxis - To the Festival",
            "Isha's Taxis - Rush Hour",
            "Isha's Taxis - Country Roads",
            "Isha's Taxis - Rain Check",
            "Isha's Taxis - Shortest Fare Ever",
            "Isha's Taxis - Isha's Taxi to the Rescue",
            "Isha's Taxis - Door to Door",
            "Isha's Taxis - You Can't Handle the Drift",
            "Isha's Taxis - The Edinburgh Run",
            "Isha's Taxis - The Big One",
            "The Car Files - File 001: Negative Downforce",
            "The Car Files - File 002: Maneuvering, Traffic Conditions",
            "The Car Files - File 003: Aerodynamics, Stability",
            "The Car Files - File 004: Acceleration Testing",
            "The Car Files - File 005: Heavyweight Speed Test",
            "The Car Files - File 006: Vertical Manoeuvrability",
            "The Car Files - File 007: Maximum Acceleration",
            "The Car Files - File 008: Non-Standard Capability",
            "The Car Files - File 009: All-Terrain Handling",
            "The Car Files - File 010: Race Engine, Production Chassis",
            "Upgrade Heroes - The Datsun",
            "Upgrade Heroes - The Audi",
            "Upgrade Heroes - The Camino",
            "Upgrade Heroes - The Mazda",
            "Upgrade Heroes - The Chevrolet",
            "Upgrade Heroes - The Land Rover",
            "Upgrade Heroes - The Peugeot",
            "Upgrade Heroes - The Ford",
            "Upgrade Heroes - The Bentley",
            "Upgrade Heroes - The Koenigsegg",
            "World's Fastest Rentals - 2013 Lamborghini Veneno",
            "World's Fastest Rentals - 2015 Koenigsegg One:1",
            "World's Fastest Rentals - 2014 Ferrari FXX-K",
            "World's Fastest Rentals - 2016 Zenvo ST1",
            "World's Fastest Rentals - 2016 Aston Martin Vulcan",
            "World's Fastest Rentals - 2009 Pagani Zonda Cinque",
            "World's Fastest Rentals - 2012 Hennessey Venom",
            "World's Fastest Rentals - 2011 Bugatti Veyron",
            "World's Fastest Rentals - 2017 Mercedes-Benz AMG GTR",
            "World's Fastest Rentals - 2018 McLaren Senna",
        ]

    @functools.cached_property
    def stories_lego(self) -> List[str]:
        return [
            "Hype Tour - Real Lego Senna 100% Not Fake",
            "Hype Tour - 100% Proof That Lego Valley Exists",
            "Hype Tour - Could a Fake Car Do This?",
            "Hype Tour - Mini Mega Awesome Skill Park",
            "Hype Tour - Brickchester Smash",
            "Hype Tour - Storm Surge",
            "Hype Tour - Flight of the Ferrari",
            "Hype Tour - Sensational Speed",
            "Hype Tour - The Awesome Tour",
        ]

    @functools.cached_property
    def stories_fortune_island(self) -> List[str]:
        return [
            "Drift Club 2.0 - #530 HSV Maloo Gen-F",
            "Drift Club 2.0 - #777 Nissan 240SX",
            "Drift Club 2.0 - #98 BMW 325i",
            "Drift Club 2.0 - #118 Nissan 240SX",
            "Drift Club 2.0 - #43 Dodge Viper SRT10",
            "Drift Club 2.0 - #13 Ford Mustang",
            "Drift Club 2.0 - #232 Nissan 240SX",
        ]

    def stories(self) -> List[str]:
        stories: List[str] = self.stories_base[:]

        if self.has_dlc_lego_speed_champions:
            stories.extend(self.stories_lego)

        if self.has_dlc_fortune_island:
            stories.extend(self.stories_fortune_island)

        return sorted(stories)

    @functools.cached_property
    def car_brands_base(self) -> List[str]:
        return [
            "Abarth",
            "Acura",
            "Alfa Romeo",
            "Alpine",
            "Alumicraft",
            "AMC",
            "AMG Transport Dynamics",
            "Apollo",
            "Ariel",
            "Aston Martin",
            "ATS",
            "Audi",
            "Austin-Healey",
            "Austin",
            "Auto Union",
            "BAC",
            "Bentley",
            "BMW",
            "Bowler",
            "Bugatti",
            "Buick",
            "Cadillac",
            "Caterham",
            "Chevrolet",
            "Chrysler",
            "Citroen",
            "Datsun",
            "Dodge",
            "Donkervoort",
            "DS Automobiles",
            "Eagle",
            "Ferrari",
            "Fiat",
            "Ford",
            "Formula Drift",
            "GMC",
            "HDT",
            "Hennessey",
            "Holden",
            "Honda",
            "Hoonigan",
            "Hot Wheels",
            "HSV",
            "Hudson",
            "HUMMER",
            "Hyundai",
            "Infiniti",
            "International",
            "Italdesign",
            "Jaguar",
            "Jeep",
            "Kia",
            "Koenigsegg",
            "KTM",
            "Lamborghini",
            "Lancia",
            "Land Rover",
            "Lexus",
            "Local Motors",
            "Lola",
            "Lotus",
            "Maserati",
            "Mazda",
            "McLaren",
            "Mercedes-AMG",
            "Mercedes-Benz",
            "Mercury",
            "Meyers",
            "MG",
            "MINI",
            "Mitsubishi",
            "Morgan",
            "Morris",
            "Mosler",
            "Napier",
            "Nissan",
            "Noble",
            "Oldsmobile",
            "Opel",
            "Pagani",
            "Peel",
            "Penhall",
            "Peugeot",
            "Plymouth",
            "Polaris",
            "Pontiac",
            "Porsche",
            "Quadra",
            "Quartz",
            "Radical",
            "RAESR",
            "RAM",
            "Reliant",
            "Renault",
            "Rimac",
            "RJ Anderson",
            "Rossion",
            "Rover",
            "Saleen",
            "Shelby",
            "Spania GTA",
            "SUBARU",
            "Sunbeam",
            "Talbot",
            "TAMO",
            "Terradyne",
            "Top Gear",
            "Toyota",
            "Triumph",
            "TVR",
            "Ultima",
            "Vauxhall",
            "Volkswagen",
            "Volvo",
            "VUHL",
            "W Motors",
            "Willys",
            "Zenvo",
        ]

    @functools.cached_property
    def car_brands_lego(self) -> List[str]:
        return [
            "Lego Speed Champions",
        ]

    @functools.cached_property
    def car_brands_fortune_island(self) -> List[str]:
        return [
            "Exomotive",
            "Funco Motorsports",
        ]

    @functools.cached_property
    def car_brands_car_pass(self) -> List[str]:
        return [
            "Can-Am",
            "Hillman",
        ]

    @functools.cached_property
    def car_brands_best_of_bond_car_pack(self) -> List[str]:
        return [
            "James Bond Edition",
        ]

    def car_brands(self) -> List[str]:
        car_brands: List[str] = self.car_brands_base[:]

        if self.has_dlc_lego_speed_champions:
            car_brands.extend(self.car_brands_lego)

        if self.has_dlc_fortune_island:
            car_brands.extend(self.car_brands_fortune_island)

        if self.has_dlc_car_pass:
            car_brands.extend(self.car_brands_car_pass)

        if self.has_dlc_best_of_bond_car_pack:
            car_brands.extend(self.car_brands_best_of_bond_car_pack)

        return sorted(set(car_brands))

    @staticmethod
    def car_classes() -> List[str]:
        return [
            "X Class",
            "S2 Class",
            "S1 Class",
            "A Class",
            "B Class",
            "C Class",
            "D Class",
        ]

    @staticmethod
    def car_types() -> List[str]:
        return [
            "Modern Supercars",
            "Retro Supercars",
            "Hypercars",
            "Retro Saloons",
            "Vans & Utility",
            "Retro Sports Cars",
            "Modern Sports Cars",
            "Super Saloons",
            "Classic Racers",
            "Cult Cars",
            "Rare Classics",
            "Hot Hatch",
            "Retro Hot Hatch",
            "Super Hot Hatch",
            "Extreme Track Toys",
            "Classic Muscle",
            "Rods and Customs",
            "Retro Muscle",
            "Modern Muscle",
            "Retro Rally",
            "Classic Rally",
            "Rally Monsters",
            "Modern Rally",
            "GT Cars",
            "Super GT",
            "Extreme Offroad",
            "Sports Utility Heroes",
            "Offroad",
            "Offroad Buggies",
            "Classic Sports Cars",
            "Track Toys",
            "Vintage Racers",
            "Trucks",
        ]

    @functools.cached_property
    def skills_standard(self) -> List[str]:
        return [
            "Air",
            "Burnout",
            "Clean Racing",
            "Drafting",
            "Drift",
            "E-Drift",
            "J Turn",
            "Near Miss",
            "One Eighty",
            "Pass",
            "Skill Chain",
            "Speed",
            "Trade Paint",
            "Two Wheels",
            "Wreckage",
        ]

    @functools.cached_property
    def skills_combo(self) -> List[str]:
        return [
            "Airborne Pass",
            "Crash Landing",
            "Ebisu Style",
            "Lucky Escape",
            "Showoff",
            "Sideswipe",
            "Slingshot",
            "Stuntman",
        ]

    @functools.cached_property
    def skills_special(self) -> List[str]:
        return [
            "Barrel Roll",
            "Binman",
            "Clean Start!",
            "Creamed",
            "Daredevil",
            "Drift Tap",
            "Fruit Salad",
            "Going Postal",
            "GOOOAAALLL",
            "Hard Charger",
            "Howzat!!",
            "Landscaping",
            "Lumberjack",
            "Kangaroo",
            "Road Open",
            "Threading the Needle",
            "Triple Pass",
            "TRY!",
            "Wrecking Ball",
            "Wrong Number",
            # "Snowman",
        ]

    @functools.cached_property
    def skills_lego(self) -> List[str]:
        return [
            "Speed Champions",
        ]

    def skills(self) -> List[str]:
        skills: List[str] = self.skills_standard[:]  # Lower weight was desired for standard skills

        skills.extend(self.skills_combo)
        skills.extend(self.skills_combo)

        skills.extend(self.skills_special)
        skills.extend(self.skills_special)

        if self.has_dlc_lego_speed_champions:
            skills.extend(self.skills_lego)
            skills.extend(self.skills_lego)

        return sorted(skills)

    @staticmethod
    def drivatar_difficulties() -> List[str]:
        return [
            "NEW RACER",
            "INEXPERIENCED",
            "AVERAGE",
            "ABOVE AVERAGE",
            "HIGHLY SKILLED",
            "EXPERT",
            "PRO",
            "UNBEATABLE",
        ]

    @staticmethod
    def cameras() -> List[str]:
        return [
            "BUMPER",
            "HOOD",
            "COCKPIT",
            "DRIVER",
            "CHASE NEAR",
            "CHASE FAR",
        ]

    @staticmethod
    def assists() -> List[str]:
        return [
            "EASY",
            "MEDIUM",
            "HARD",
            "PRO",
            "INSANE",
        ]

    @staticmethod
    def assists_single() -> List[str]:
        return [
            "Turn Rewind off",
            "Set Damage & Tire Wear to Simulation",
            "Turn Driving Line off",
            "Set Shifting to Manual",
            "Set Shifting to Manual W/ Clutch",
            "Turn Stability Control off",
        ]

    @staticmethod
    def race_placements() -> List[str]:
        return [
            "1st",
            "2nd or better",
            "3rd or better",
            "4th or better",
        ]

    @staticmethod
    def stars() -> List[str]:
        return [
            "at least 1 Star",
            "at least 2 Stars",
            "3 Stars",
        ]


# Archipelago Options
class ForzaHorizon4DLCOwned(OptionSet):
    """
    Indicates which Forza Horizon 4 DLC the player owns, if any.
    """

    display_name = "Forza Horizon 4 DLC Owned"
    valid_keys = [
        "LEGO Speed Champions",
        "Fortune Island",
        "Car Pass",
        "Best of Bond Car Pack",
    ]

    default = valid_keys
