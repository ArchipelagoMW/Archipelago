from __future__ import annotations

import functools
from typing import Any, Dict, List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TonyHawksProSkater1Plus2ArchipelagoOptions:
    tony_hawks_pro_skater_1_plus_2_include_secret_skaters: TonyHawksProSkater1Plus2IncludeSecretSkaters
    tony_hawks_pro_skater_1_plus_2_include_create_a_skater: TonyHawksProSkater1Plus2IncludeCreateASkater


class TonyHawksProSkater1Plus2Game(Game):
    name = "Tony Hawk's Pro Skater 1+2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = TonyHawksProSkater1Plus2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="After COUNT bails, restart the current trial",
                data={
                    "COUNT": (self.bail_count_range, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="As SKATER, beat the Sick Score in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, beat the Sick Score in: LEVELS",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVELS": (self.levels, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, beat the High Combo in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, beat the High Combo in: LEVELS",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVELS": (self.levels, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, collect S-K-A-T-E in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, collect S-K-A-T-E in: LEVELS",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVELS": (self.levels, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, find the 5 collectibles in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, find the 5 collectibles in: LEVELS",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVELS": (self.levels, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, get the Secret Tape in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, get the Secret Tapes in: LEVELS",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVELS": (self.levels, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, find the VV Logo in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, find the Alien Plushie in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, beat the following Platinum Score: PLATINUM",
                data={
                    "SKATER": (self.skaters, 1),
                    "PLATINUM": (self.scores_platinum, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="As SKATER, clear all objectives in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, get a Gold Medal the following Competition: LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels_competition, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, get a Gold Medal the following Competition: LEVELS",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVELS": (self.levels_competition, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, place Top 3 the following Competition without bailing once: LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "LEVEL": (self.levels_competition, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, clear the following Gaps in a single 2-minute session: GAPS",
                data={
                    "SKATER": (self.skaters, 1),
                    "GAPS": (self.gap_sets, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="As SKATER, land a POINTS Combo in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "POINTS": (self.score_combo_range_low, 1),
                    "LEVEL": (self.levels_all, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, land a POINTS Combo in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "POINTS": (self.score_combo_range_high, 1),
                    "LEVEL": (self.levels_all, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, land a Combo including the following Gap: GAP",
                data={
                    "SKATER": (self.skaters, 1),
                    "GAP": (self.gap_single, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="As SKATER, land a Combo including the following Trick: TRICK",
                data={
                    "SKATER": (self.skaters, 1),
                    "TRICK": (self.tricks_no_special, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, land a Combo including the following Tricks: TRICKS",
                data={
                    "SKATER": (self.skaters, 1),
                    "TRICKS": (self.tricks_no_special, 3),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As SKATER, land a Combo including the following Special Trick: TRICK",
                data={
                    "SKATER": (self.skaters, 1),
                    "TRICK": (self.tricks_special, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, score at least SCORE points in a 2-minute session in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "SCORE": (self.score_range_low, 1),
                    "LEVEL": (self.levels_all, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="As SKATER, score at least SCORE points in a 2-minute session in LEVEL",
                data={
                    "SKATER": (self.skaters, 1),
                    "SCORE": (self.score_range_high, 1),
                    "LEVEL": (self.levels_all, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def include_secret_skaters(self) -> bool:
        return bool(self.archipelago_options.tony_hawks_pro_skater_1_plus_2_include_secret_skaters.value)

    @property
    def include_create_a_skater(self) -> bool:
        return bool(self.archipelago_options.tony_hawks_pro_skater_1_plus_2_include_create_a_skater.value)

    @functools.cached_property
    def skaters_base(self) -> List[str]:
        return [
            "Tony Hawk",
            "Bob Burnquist",
            "Steve Caballero",
            "Kareem Campbell",
            "Rune Glifberg",
            "Eric Koston",
            "Bucky Lasek",
            "Rodney Mullen",
            "Chad Muska",
            "Andrew Reynolds",
            "Geoff Rowley",
            "Elissa Steamer",
            "Jamie Thomas",
            "Lizzie Armanto",
            "Leo Baker",
            "Leticia Bufoni",
            "Riley Hawk",
            "Nyjah Huston",
            "Tyshawn Jones",
            "Aori Nishimura",
            "Shane O'Neill",
        ]

    @functools.cached_property
    def skaters_secret(self) -> List[str]:
        return [
            "Officer Dick",
            "Roswell Alien",
        ]

    @functools.cached_property
    def skaters_create_a_skater(self) -> List[str]:
        return [
            "Create-A-Skater",
            "Create-A-Skater",
            "Create-A-Skater",
        ]

    def skaters(self) -> List[str]:
        skaters: List[str] = self.skaters_base[:]

        if self.include_secret_skaters:
            skaters.extend(self.skaters_secret)
        if self.include_create_a_skater:
            skaters.extend(self.skaters_create_a_skater)

        return sorted(skaters)

    @staticmethod
    def levels() -> List[str]:
        return [
            "Warehouse",
            "School",
            "Mall",
            "Downtown",
            "Downhill Jam",
            "Streets",
            "The Hangar",
            "School II",
            "NY City",
            "Venice Beach",
            "Philadelphia",
        ]

    @staticmethod
    def levels_competition() -> List[str]:
        return [
            "Skate Park",
            "Burnside",
            "Roswell",
            "Marseille",
            "Skatestreet",
            "The Bullring",
        ]

    @staticmethod
    def levels_extra() -> List[str]:
        return [
            "Chopper Drop",
            "Skate Heaven",
        ]

    def levels_all(self) -> List[str]:
        return sorted(self.levels() + self.levels_competition() + self.levels_extra())

    @staticmethod
    def scores_platinum() -> List[str]:
        return [
            "Warehouse -> 500,000",
            "School -> 625,000",
            "Mall -> 750,000",
            "Skate Park -> 1,150,000",
            "Downtown -> 875,000",
            "Downhill Jam -> 1,000,000",
            "Burnside -> 1,600,000",
            "Streets -> 1,250,000",
            "Roswell -> 1,750,000",
            "The Hangar -> 500,000",
            "School II -> 625,000",
            "Marseille -> 1,150,000",
            "NY City -> 750,000",
            "Venice Beach -> 1,000,000",
            "Skatestreet -> 1,600,000",
            "Philadelphia -> 1,250,000",
            "The Bullring -> 1,750,000",
            "Chopper Drop -> 500,000",
            "Skate Heaven -> 2,500,000",
        ]

    @functools.cached_property
    def gaps_by_level(self) -> Dict[str, Any]:
        return {
            "Warehouse": self.gaps_warehouse,
            "School": self.gaps_school,
            "Mall": self.gaps_mall,
            "Skate Park": self.gaps_skate_park,
            "Downtown": self.gaps_downtown,
            "Downhill Jam": self.gaps_downhill_jam,
            "Burnside": self.gaps_burnside,
            "Streets": self.gaps_streets,
            "Roswell": self.gaps_roswell,
            "The Hangar": self.gaps_the_hangar,
            "School II": self.gaps_school_ii,
            "Marseille": self.gaps_marseille,
            "NY City": self.gaps_ny_city,
            "Venice Beach": self.gaps_venice_beach,
            "Skatestreet": self.gaps_skatestreet,
            "Philadelphia": self.gaps_philadelphia,
            "The Bullring": self.gaps_the_bullring,
            "Chopper Drop": self.gaps_chopper_drop,
            "Skate Heaven": self.gaps_skate_heaven,
        }

    def gap_single(self) -> List[str]:
        level: str = self.random.choice(list(self.gaps_by_level.keys()))

        return [
            f"{level} -> {self.random.choice(self.gaps_by_level[level])}",
        ]

    def gap_sets(self) -> List[str]:
        level: str = self.random.choice(list(self.gaps_by_level.keys()))

        return [
            f"{level} -> {', '.join(self.random.choices(self.gaps_by_level[level], k=3))}",
        ]

    @functools.cached_property
    def gaps_warehouse(self) -> List[str]:
        return [
            "Big Rail",
            "Channel Gap",
            "Deck 2 Rail",
            "Face Plant",
            "High Rail",
            "Holy Shi...",
            "Kicker 2 Ledge",
            "Kicker Gap",
            "Monster Grind",
            "Over The Pipe",
            "Secret Room",
            "Taxi 2 Ledge",
            "Taxi Gap",
            "Transfer",
            "Transition Grind",
        ]

    @functools.cached_property
    def gaps_school(self) -> List[str]:
        return [
            "Ditchin Class",
            "Dumpster Rail Gap",
            "Funbox To Table Transfer",
            "Garbage Ollie",
            "Gimme Gap",
            "Hall Pass Gap",
            "All-Access Gap",
            "Huge Rail",
            "Kicker Gap",
            "Long Ass Rail",
            "Mini Gap",
            "Over a Footbridge",
            "Over the Air Conditioner",
            "Park Gap",
            "Planter Gap",
            "Playground Rail",
            "Rail To Rail Transfer",
            "Roof To Awning Gap",
            "Roof To Roof Gap",
            "Funbox To Rail Transfer",
            "Downhill Manual",
            "Across The Gym",
            "Roof Hop",
            "Down The Awning",
            "Perfectly Balanced",
            "Gigantic Rail",
            "Ridiculous Rail",
        ]

    @functools.cached_property
    def gaps_mall(self) -> List[str]:
        return [
            "Huge Stair Set Off A Mezzanine",
            "Coffee Grind",
            "The Flying Leap",
            "For the Whole Atrium",
            "Fountain Gap",
            "Exit Stage Right",
            "Exit Stage Left",
            "Over A Stair Set",
            "Over A Huge Stair Set",
            "Planter Gap",
            "Rail Combo",
            "Skater Escalator Gap",
            "Across The Light Beam",
            "The Long Rail",
            "The Short Rail",
        ]

    @functools.cached_property
    def gaps_skate_park(self) -> List[str]:
        return [
            "Acid Drop",
            "Across The Park",
            "Around The Bend",
            "HP Transfer",
            "Light Grind",
            "Over The Box",
            "Over The Pipe",
            "Over The Rafters",
            "Pool 2 Walkway",
            "Pool Hip",
            "Pool Rail Trans",
            "Rafter Rail",
            "Transfer",
            "Walkway Rail Trans",
            "Wall Gap",
            "Wall Gap Jr.",
            "Whoop Gap",
        ]

    @functools.cached_property
    def gaps_downtown(self) -> List[str]:
        return [
            "Big Ass",
            "Billboard Grind",
            "BS Gap",
            "BS Grind",
            "Burly Deck Gap",
            "Car Ollie",
            "Cheesy Deck Gap",
            "Death Grind",
            "Deck Gap",
            "Dirty Rail",
            "Glass Gap",
            "Kicker Gap",
            "Kicker 2 Edge",
            "Kicker 2 Street",
            "Rail 2 Rail",
            "Roof 2 Roof",
            "Secret Tunnel Entrance",
            "Sucky Room Gap",
            "T 2 T Gap",
            "Transfer",
            "Truck Gap",
            "Tunnel Gap",
            "Wimpy Gap",
            "Mechanic Gap",
            "Box Office Gap",
            "Skyway Gap",
            "Super Skyway Gap",
        ]

    @functools.cached_property
    def gaps_downhill_jam(self) -> List[str]:
        return [
            "Huge Water Hazard",
            "Neversoft Elec Co",
            "25 Feet",
            "50 Feet",
            "75 Feet",
            "100 Feet",
            "125 Feet",
            "Pipe Flip",
            "Hydrophobic",
            "The Downhill Halfpipe",
            "The Other Downhill Halfpipe",
        ]

    @functools.cached_property
    def gaps_burnside(self) -> List[str]:
        return [
            "Transfer",
            "Twinkie Transfer",
            "Vert Wall Gap",
            "Bridge Grind",
            "Over Da Pool",
            "Bridge Gap",
            "Triple Rail",
            "Lippn' The Bridge",
            "Top Shelf Lip",
            "Bottom Shelf Lip",
            "Rollin' The Hill",
            "Something in da Eye",
            "Over da Pool Landing",
        ]

    @functools.cached_property
    def gaps_streets(self) -> List[str]:
        return [
            "Acid Drop-In",
            "Around The Fountain",
            "Backwoods Ledge",
            "Bendy's Lip",
            "C Block Gap",
            "Down The Spiral",
            "Fountain Gap",
            "The Gonz Gap",
            "Handi Gap",
            "Hook Rail",
            "Hubba Gap",
            "Hubba Hop",
            "Hubba Ledge",
            "Ledge Hop",
            "Lombard Ledge",
            "Oversized 8 Set",
            "Over The Seven",
            "Pagoda Gap",
            "Planter Gap",
            "Porch Gap",
            "Rail 2 Rail",
            "Ramp 2 Ramp",
            "Spine Gap",
            "Street Gap",
            "Up The Spiral",
        ]

    @functools.cached_property
    def gaps_roswell(self) -> List[str]:
        return [
            "BHouse Rail",
            "Channel Gap",
            "Deck Gap",
            "Deck Grind",
            "Grey Grind",
            "High Deck Gap",
            "Low Deck Gap",
            "Pool Grind",
            "Roll In Channel Gap",
            "Nasty in the Pasty",
            "Cover Up",
            "Roswell That End's Well",
        ]

    @functools.cached_property
    def gaps_the_hangar(self) -> List[str]:
        return [
            "Air Over The Door",
            "Chopper Hop",
            "Flyin High",
            "Halfpipe Hangtime",
            "Its Cold Up Here",
            "Rollin Gap",
            "Skycrane Hangtime",
            "Wingtip Hangtime",
            "Big Light Hopper",
            "Halfpipe Grind",
            "Light Corner",
            "Lil Light Hopper",
            "Rail-Guided Missile",
            "Raildrop",
            "Instrumental Landing",
            "Downwind Lip",
            "High Steppin'",
            "One Half Pipe Lip",
            "The Other Half Pipe Lip",
            "Upwind Lip",
            "Wind Tunnel Back Wall",
            "Wing To Rail",
        ]

    @functools.cached_property
    def gaps_school_ii(self) -> List[str]:
        return [
            "2 Da Roof!!!",
            "2 Wheelin' TC's Roof",
            "3 Points!!!",
            "Arch Extension",
            "Awning Hop",
            "Backboard Dance!",
            "Balcony 2 Awning!!!",
            "Bank 2 Ledge",
            "Bendy's Curb",
            "Big Rancho Bench Gap",
            "Carlsbad 11 Set",
            "Carlsbad Gap",
            "Crazy Roof Gap!!",
            "And Down The Bank!",
            "Drop Out Roof Gap!",
            "Flyin' The Flag!",
            "Gym Rail 2 Rail",
            "High Dive Extension!!!",
            "Huge Transfer!!!",
            "Kicker 2 Hook",
            "Leap Of Faith!!!",
            "Ledge On Edge",
            "Lil' Guppy Extension!",
            "Mad Skeelz Roof Gap!!!",
            "Mid Squid Extension!!",
            "Roll Call! Nightmare Rail!",
            "Roll Call! Opunsezmee Rail!",
            "Overhang Air",
            "Overhang Stomp!",
            "Over The Wall...",
            "Planter On Edge",
            "Pole 2 Brix!",
            "Pole Stomp!",
            "Rack 'Em Up",
            "Rock The Bells",
            "Roll Call! Gonz Rail",
            "Stage Rail 2 Rail",
            "Starting Blocks Extension!!!",
            "Suicidal Roof Gap!!!",
            "Table Transfer",
            "TC's Roof Gap",
            "Bendy's Flat",
        ]

    @functools.cached_property
    def gaps_marseille(self) -> List[str]:
        return [
            "2 the Box",
            "And Away!!!",
            "Big Mouth Gap",
            "Big Ol' Stanky",
            "Boomin' Extension",
            "Box 2 Box Action",
            "Crossbar Stomp",
            "Dumpster Pop",
            "Dumpster Stomp",
            "The Hidden 4 Kink",
            "Freakin' Huge Hip",
            "Humptey Humps!!!!",
            "Kink Clank",
            "Kink Stomp",
            "Knucklin' Futs!!!",
            "Lamp Stomp",
            "Ledge 2 Rail",
            "Over the Crossbar",
            "Over the Lil' 4",
            "Over the Gate",
            "Over the Table",
            "Rail 2 Ledge",
            "Rail 2 Rail",
            "Shorty Dumpster Pop",
            "Shorty Table Pop",
            "Stanky Extension",
            "Table Pop",
            "Up!",
            "Up the Lil' 4",
            "Up!!",
            "U.U.A. Extension",
            "Wall Crawler",
            "Water Up Le Backside",
            "Waking the dead",
            "Steppin Out",
            "The Trashman Gap",
            "Le Rail Saut",
            "Le Dumpster Saut",
        ]

    @functools.cached_property
    def gaps_ny_city(self) -> List[str]:
        return [
            "Awning Air",
            "Big Air Out Of The Banks",
            "Kick It",
            "Over The Banks Barrier",
            "Over The Road",
            "Pillar Air",
            "Pigeon Puddin' Gap",
            "Pouncer Was Here",
            "Ramp To Park Gap",
            "Ramp To Statue Shorty Gap",
            "Rock It Air",
            "Take It To The Bridge",
            "Across The Pit",
            "Banks Fence Gap",
            "Banks Road Gap",
            "Banks Spank",
            "Bench-Hoppin",
            "Buuurp! Now Go Skate",
            "Changin Trains",
            "Corner Cut",
            "Grab A Snack And Sit Down",
            "Jamie's Steps",
            "Joey's Sculpture",
            "Left Side Pit Rail Stomp",
            "Park Entrance Gap",
            "Parking Meter Gap",
            "Path Less Traveled",
            "Re-Rebar",
            "Rebar To Rail Gap",
            "Ride The Rails",
            "Right Side Pit Rail Stomp",
            "Sidewalk Bomb",
            "Slam Dunk",
            "The Easy Way",
            "The Hard Way",
            "You're Next In Line",
            "Going Down?",
            "The Bridge",
            "Phat Lip",
            "Waaaay Up There",
            "Banks Barrier Wallride",
            "One Side",
            "Downhill Jam",
        ]

    @functools.cached_property
    def gaps_venice_beach(self) -> List[str]:
        return [
            "Big Double 5 Set",
            "Big Vent Gap",
            "Cake Transfer",
            "Canyon Jump",
            "Fatty Transfer",
            "Huge Roof 2 Ramp",
            "Ledge 9 Set",
            "Lil' Vent Gap",
            "Massive 20 Set!",
            "Muska's Gap",
            "Nice Mid Size Roof Gap",
            "Planter Pop",
            "Roof 2 Ramp",
            "Shorty Planter Pop",
            "Siiiiiick Roof Gap!!!",
            "Table Pop",
            "Tight Landing Transfer",
            "VB! Ledge Transfer",
            "VB! Huge Transfer!!!",
            "VB! Pit Transfer",
            "VB! Skinny Transfer",
            "Vent 2 Roof Gap",
            "Up! / Up!! / And Away!!!",
            "Uphill Canyon Jump",
            "Wee Lil' Roof Gap",
            "West Side Transfer",
            "10 Point Landing!",
            "Bench Trippin!",
            "Ledge 2 Ledge",
            "'Round The Horn",
            "Seaside Handrail",
            "The High Wire",
            "The Venice Ledge",
            "Candy Cane Manual",
            "He Could Go...",
            "All The Way...",
            "Touchdown!!!",
            "Ramp 2 Roof",
            "On The Fence",
            "Fence To Roof",
        ]

    @functools.cached_property
    def gaps_skatestreet(self) -> List[str]:
        return [
            "Big Air Railing Grind",
            "Bowl Envy",
            "Bowl Lip",
            "Bowl To HP",
            "Bullet Bowl Hop",
            "Circle The Pool",
            "Cut The Corner",
            "Daaaaay Tripper",
            "Extension Transfer",
            "Funbox Wheelie",
            "Gimme Gap Redux",
            "Gully Lip",
            "Havin A Picnic",
            "Hexbox Gap",
            "High Jumper",
            "High Sticker",
            "HP Lip",
            "HP To Bowl",
            "HP To Railbox",
            "Nail The Rail",
            "No Kidding Around",
            "Over The Bridge",
            "Over The Deck",
            "Over The Wall",
            "Railing Hop",
            "Rail Secret Area Key",
            "Rail To Rail",
            "Ride The Wave",
            "Shoot The Gap",
            "Skatin On The Dock Of The Bay",
            "Sodee Pop Gap",
            "Stairset",
            "Surfin U.S.A.",
            "Van Secret Area Key",
            "Wave Wall Minigap",
            "Mr. Small Lips",
            "Over The HP",
            "Funbox Slap",
            "Over The Barrier",
        ]

    @functools.cached_property
    def gaps_philadelphia(self) -> List[str]:
        return [
            "Bench Gap",
            "Chillin' On The Balcony",
            "Easy Post Ollie",
            "Phillyside Hop",
            "Phillyside HP Transfer",
            "Pillar Fight",
            "Post Ollie",
            "Stair Set",
            "Statue Hop",
            "THPS Statue Gap",
            "Up The Small Step Set",
            "World's Most Obvious Gap",
            "Awning Grind",
            "Death From Above",
            "Fly By Wire",
            "Fountain Ping!",
            "Funbox Transfer",
            "Grind of Faith",
            "Grind Up Dem Stairs",
            "Hobo Gap",
            "Just Visiting",
            "Little Corner Grind",
            "Long Stair",
            "Medium Stair",
            "Pillar Hop",
            "Planter Double Pillar Gap",
            "Planter Transfer",
            "Railing To Planter",
            "Short Stair",
            "Telephone Co. Gap",
            "Track Smack",
            "Train Hard",
            "Flatlands Techin'",
            "Funbox Wheelie",
            "Manual Stimulation",
            "Rockin' The Stairs",
            "Phillyside Big Bowl Lip",
            "Phillyside HP Lip",
            "Phillyside Mid Bowl Lip",
            "Phillyside New Bowl Lip",
        ]

    @functools.cached_property
    def gaps_the_bullring(self) -> List[str]:
        return [
            "Air Toro",
            "Big Enchilada Mama",
            "Gate Gap",
            "Launchin The Pipe",
            "Plat Gap",
            "Rollin Gap",
            "Tight Gap",
            "Wussy Rollin Gap",
            "Box To Banana",
            "Box To Rail",
            "Clenchfest!",
            "Friggin A Hombre",
            "Enjoyin The View",
            "Finesse Test",
            "Grindin The Pipe",
            "Kink",
            "Launch To Banana",
            "Launch To Rail",
            "Lil Wee Wussy Gap",
            "Nailin Da Rail",
            "Nice Friggin Ankles",
            "Rail Plat Gap",
            "Ramp Rail To Banana",
            "Ramp Rail To Rail",
            "Takin The High Road",
            "Way To Go Amigo",
            "Threadin The Needle",
            "Up To The Stands",
            "Way To Go Gringo!!!",
            "Launchin On Up",
        ]

    @functools.cached_property
    def gaps_chopper_drop(self) -> List[str]:
        return [
            "1 Potato",
            "2 Potato",
            "3 Potato",
            "70 ft",
            "80 ft",
            "90 ft",
            "Heli Grind",
            "Into The Heli",
            "Rail Hop",
            "Whoomah",
        ]

    @functools.cached_property
    def gaps_skate_heaven(self) -> List[str]:
        return [
            "Airs Hole",
            "Big Fat Portal Gap",
            "Blowin It Out The Hole!",
            "Cleaning The Pipes",
            "Clearing The Swings",
            "Down 2 Tonys Island",
            "Dropping In On Tony",
            "Feed Me!!!",
            "Portal Gap",
            "Gutter 2 San Dieguito Roof",
            "The Holy Crail",
            "House of Tony 2 Sadlands",
            "Isle of Tony 2 Sadlands",
            "Jumpin Da Hub",
            "Northeast Snake Gap",
            "Northwest Snake Gap",
            "Over the Dome",
            "Platform Gap",
            "Reverse Wussy Snake Gap",
            "Reverse Zag Gap",
            "Reverse Zig Gap",
            "Sadlands 2 San Dieguito Hall",
            "Sadlands Path Gap",
            "Sadlands Up 2 Isle of Tony",
            "San Dieguito Hall 2 Sadlands",
            "San Dieguito Ten Set",
            "San Dieguito Window 2 Sadlands",
            "Tight Landing",
            "Tunnel Of Luvin",
            "Up 2 Combi",
            "Weak Sauce Wussy Snake Gap",
            "Weak Sauce Zag Gap",
            "Weak Sauce Zig Gap",
            "Woohoo Oh Ho Yeehee!!!",
            "Wussy Snake Gap",
            "Zag Gap",
            "Zig Gap",
            "90 Degree Ramp Rail Gap",
            "90 Degree Sadlands Rail Gap",
            "Bench Gap",
            "Bench Gap Series",
            "Chen Rail Series",
            "Fence 2 Radramp",
            "Gutter 2 San Dieguito Roof",
            "Kicker 2 Railspan",
            "Longrail",
            "Mid Intersect Sad Gap",
            "Northern Crossover Sad Gap",
            "Northern Intersect Sad Gap",
            "Northern Swingrail",
            "Off The Roof 2 Rail",
            "Radramp 2 Islands Edge",
            "Radramp 2 Snakerun",
            "Rail 2 Kicker 2 Rail 2 Bench",
            "Rail 2 Snakerun",
            "Ramp 2 Rail",
            "Ramp Rail Gap",
            "Rimrail Gap",
            "San Dieguito Hall 2 Edge",
            "San Dieguito Roof 2 Edge",
            "Southern Crossover Sad Gap",
            "Southern Intersect Sad Gap",
            "Southern Swingrail",
            "Swinging The Set",
            "Time 2 Feed The Volcano!!!",
            "Isle of Tony 2 Edge",
            "Top Of Da World Ma!!!",
            "Up 2 Pipe Rail",
        ]

    @staticmethod
    def tricks_special() -> List[str]:
        return [
            "The 900",
            "Indy Backflip",
            "Indy Frontflip",
            "Weddle Backflip",
            "Pizza Guy",
            "Racket Air",
            "360 Varial McTwist",
            "FS 540",
            "Casper Flip 360 Flip",
            "Kickflip Superman",
            "Kickflip One Foot Tail",
            "Nosebone Flip",
            "Coffin",
            "Kickflip Backflip",
            "Hardflip Lateflip",
            "540 Flip",
            "360 Double Flip",
            "Hardflip",
            "Half Flip Casper",
            "Hospital Flip",
            "Heelflip Handflip",
            "Quad Heelflip",
            "Nollie Flip Underflip",
            "Ghetto Bird",
            "Fingerflip Airwalk",
            "Misty Flip",
            "Full Cab Flip",
            "Puppet Master",
            "Hardflip Crail",
            "Kickflip So Good",
            "Big Hitter II",
            "Crail Slide",
            "Beni Fingerflip Crooks",
            "Fandangle",
            "Nosegrind to Pivot",
            "One Foot Smith",
            "Rocket Tailslide",
            "Rowley Darkslide",
            "5-0 Overturn",
            "Heelflip Darkslide",
            "Madonna Tail Slide",
            "Hang Ten Nosegrind",
            "Hurricane",
            "Nose Grab Tailslide",
            "Cab Flip FS Boardslide",
            "Hardflip BS Nose Picker",
            "Hoho",
            "Muska Nose Manual",
            "Rusty Slide Manual",
            "Nose Manual Nollie Inward Heel",
            "One Foot One Wheel",
        ]

    @staticmethod
    def tricks_grab() -> List[str]:
        return [
            "Nosegrab",
            "Rocket Air",
            "Madonna",
            "Judo",
            "Indy",
            "Stiffy",
            "Airwalk",
            "Christ Air",
            "Tailgrab",
            "One Foot Tailgrab",
            "Benihana",
            "Sack Tap",
            "Melon",
            "Method",
            "Japan",
            "One Foot Japan",
            "Indy Nosebone",
            "Del Mar Indy",
            "Crossbone",
            "Crooked Cop",
            "Weedle",
            "Seatbelt Air",
            "Wrap Around",
            "Body Wrap",
            "Cannonball",
            "Fingerflip Cannonball",
            "Crail Grab",
            "TuckKnee",
            "FS Shifty",
            "BS Shifty",
            "Stalefish",
            "Stalefish Tweak",
        ]

    @staticmethod
    def tricks_flip() -> List[str]:
        return [
            "Impossible",
            "Double Impossible",
            "Triple Impossible",
            "Inward Heelflip",
            "360 Inward Heelflip",
            "Heelflip",
            "Double Heelflip",
            "Triple Heelflip",
            "Varial Heelflip",
            "Laserflip",
            "Pop Shove-It",
            "360 Shove-It",
            "540 Shove-It",
            "Vairal Kickflip",
            "360 Flip",
            "Kickflip",
            "Double Kickflip",
            "Triple Kickflip",
            "Hardflip",
            "360 Hardflip",
            "Sal Flip",
            "360 Sal Flip",
            "FS Shove-It",
            "360 FS Shove-It",
            "Ollie North",
            "Ollie North Back Foot Flip",
            "Ollie Airwalk",
            "Ollie Airwalk Late Shove-It",
            "180 Varial",
            "360 Varial",
            "Heelflip Varial Lien",
            "Back Foot Heelflip",
            "Double Back Foot Heelflip",
            "Back Foot Kickflip",
            "Double Back Foot Kickflip",
            "Front Foot Impossible",
            "Double Front Foot Impossible",
            "Fingerflip",
            "Double Fingerflip",
        ]

    @staticmethod
    def tricks_lip() -> List[str]:
        return [
            "FS Noseblunt",
            "Switcheroo",
            "BS Boneless",
            "One Foot Invert",
            "Reacharound Invert",
            "Gymnast Plant",
            "Tuck-knee Invert",
            "Andrect Invert",
            "Nose Stall",
            "Disaster",
            "Eggplant",
            "Rock to Fakie",
            "Nose Pick",
            "Axle Stall",
            "Blunt to Fakie",
        ]

    @staticmethod
    def tricks_grind() -> List[str]:
        return [
            "FS 50-50",
            "BS 50-50",
            "FS Noseslide",
            "BS Noseslide",
            "FS Tailslide",
            "BS Tailslide",
            "FS Nosegrind",
            "BS Nosegrind",
            "FS 5-0",
            "BS 5-0",
            "FS Overcrook",
            "BS Overcrook",
            "FS Crooked",
            "BS Crooked",
            "FS Feeble",
            "BS Feeble",
            "FS Smith",
            "BS Smith",
            "FS Boardslide",
            "BS Boardslide",
            "FS Lipslide",
            "BS Lipslide",
            "FS Bluntslide",
            "BS Bluntslide",
            "FS Nosebluntslide",
            "BS Nosebluntslide",
            "FS Monty",
            "BS Monty",
        ]

    def tricks_no_special(self) -> List[str]:
        return sorted(self.tricks_grab() + self.tricks_flip() + self.tricks_lip() + self.tricks_grind())

    @staticmethod
    def bail_count_range() -> range:
        return range(2, 8)

    @staticmethod
    def score_range_low() -> range:
        return range(100000, 1250001, 10000)

    @staticmethod
    def score_range_high() -> range:
        return range(1250000, 10000001, 10000)

    @staticmethod
    def score_combo_range_low() -> range:
        return range(20000, 250001, 10000)

    @staticmethod
    def score_combo_range_high() -> range:
        return range(250000, 2000001, 10000)


# Archipelago Options
class TonyHawksProSkater1Plus2IncludeSecretSkaters(Toggle):
    """
    Indicates whether to include secret skaters when generating objectives for Tony Hawk's Pro Skater 1+2.
    """

    display_name = "Tony Hawk's Pro Skater 1+2 Include Secret Skaters"


class TonyHawksProSkater1Plus2IncludeCreateASkater(Toggle):
    """
    Indicates whether to include your Create-A-Skater skater when generating objectives for Tony Hawk's Pro Skater 1+2.
    """

    display_name = "Tony Hawk's Pro Skater 1+2 Include Create-A-Skater"
