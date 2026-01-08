from __future__ import annotations

import functools

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PowerWashSimulatorArchipelagoOptions:
    powerwash_simulator_dlc_owned: PowerWashSimulatorDLCOwned


class PowerWashSimulatorGame(Game):
    name = "PowerWash Simulator"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.VR,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]
    
    is_adult_only_or_unrated = False

    options_cls = PowerWashSimulatorArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete the job without soap",
                data=dict(),
            ),

            GameObjectiveTemplate(
                label="Use a weaker power washer",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Clean the JOB",
                data={"JOB": (self.jobs, 1)},
                is_time_consuming=True,
                is_difficult=False,
            ),
        ]

    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.powerwash_simulator_dlc_owned.value

    @property
    def has_dlc_tomb_raider(self) -> bool:
        return "Tomb Raider" in self.dlc_owned

    @property
    def has_dlc_midgar(self) -> bool:
        return "Midgar" in self.dlc_owned

    @property
    def has_dlc_spongebob_squarepants(self) -> bool:
        return "Spongebob Squarepants" in self.dlc_owned

    @property
    def has_dlc_back_to_the_future(self) -> bool:
        return "Back to the Future" in self.dlc_owned

    @property
    def has_dlc_santa_workshop(self) -> bool:
        return "Santa's Workshop - Winter 2023" in self.dlc_owned

    @property
    def has_dlc_warhammer_40000(self) -> bool:
        return "Warhammer 40,000" in self.dlc_owned

    @property
    def has_dlc_alice_adventures(self) -> bool:
        return "Alice's Adventures" in self.dlc_owned

    @property
    def has_dlc_muckingham_files_part_3(self) -> bool:
        return "Muckingham Files - Part 3" in self.dlc_owned

    @property
    def has_dlc_muckingham_files_part_4(self) -> bool:
        return "Muckingham Files - Part 4" in self.dlc_owned

    @property
    def has_dlc_cruise_ship_sun_deck(self) -> bool:
        return "Cruise Ship Sun Deck - Summer 2024" in self.dlc_owned

    @property
    def has_dlc_shrek(self) -> bool:
        return "Shrek" in self.dlc_owned

    @property
    def has_dlc_halloween_seasonal_2024(self) -> bool:
        return "Halloween Seasonal 2024" in self.dlc_owned

    @property
    def has_dlc_ice_rink(self) -> bool:
        return "Ice Rink - Winter 2024" in self.dlc_owned

    @functools.cached_property
    def free_play_jobs(self) -> List[str]:
        return [
            "Back Garden",
            "Bungalow",
            "Playground",
            "Detached House",
            "Shoe House",
            "Fire Station",
            "Skatepark",
            "Forrest Cottage",
            "Mayor's Mansion",
            "Carousel",
            "Tree House",
            "Temple",
            "Washroom",
            "Helter Skelter",
            "Ferris Wheel",
            "Subway Platform",
            "Fortune Teller's Wagon",
            "Ancient Statue",
            "Ancient Monument",
            "Lost City Palace",
            "Van",
            "Vintage Car",
            "Grandpa Miller's Car",
            "Fire Truck",
            "Dirt Bike",
            "Golf Cart",
            "Motorbike and Sidecar",
            "SUV",
            "Penny Farthing",
            "Recreation Vehicle",
            "Drill",
            "Monster Truck",
            "Frolic Boat",
            "Fishing Boat",
            "Fire Helicopter",
            "Private Jet",
            "Stunt Plane",
            "Recreational Vehicle (Again)",
            "Mars Rover [Bonus]",
            "Gnome Fountain [Bonus]",
            "Mini Golf Course [Bonus]",
            "Steam Locomotive [Bonus]",
            "Satellite Dish [TMF-1]",
            "Food Truck [TMF-1]",
            "Solar Station [TMF-1]",
            "Paintball Arena [TMF-2]",
            "Excavator [TMF-2]",
            "Spanish Villa [TMF-2]",
        ]

    @functools.cached_property
    def tomb_raider_jobs(self) -> List[str]:
        return [
            "Croft Manor [TR]",
            "Lara Croft's Obstacle Course and Quad Bike [TR]",
            "Lara Croft's Jeep and Motorboat [TR]",
            "Croft Manor's Maze [TR]",
            "Croft Manor's Treasure Room [TR]",
        ]

    @functools.cached_property
    def midgar_jobs(self) -> List[str]:
        return [
            "Hardy-Daytona & Shinra Hauler [MG]",
            "Scorpion Sentinel [MG]",
            "Seventh Heaven [MG]",
            "Mako Energy Exhibit [MG]",
            "Airbuster [MG]",
        ]

    @functools.cached_property
    def spongebob_squarepants_jobs(self) -> List[str]:
        return [
            "Conch Street [SS]",
            "Bikini Bottom Bus [SS]",
            "Krusty Krab [SS]",
            "Patty Wagon [SS]",
            "Invisible Boatmobile [SS]",
            "Mermalair [SS]",
        ]

    @functools.cached_property
    def back_to_the_future_jobs(self) -> List[str]:
        return [
            "Doc Brown's Van [BttF]",
            "Time Machine [BttF]",
            "Hill Valley Clocktower [BttF]",
            "Holomax Theater [BttF]",
            "Doc's Time Train [BttF]",
        ]

    @functools.cached_property
    def warhammer_40000_jobs(self) -> List[str]:
        return [
            "Land Raider [W40000]",
            "Redemptor Dreadnought [W40000]",
            "Imperial Knight Paladin [W40000]",
            "Rogal Dorn Battle Tank [W40000]",
            "Thunderhawk [W40000]",
        ]

    @functools.cached_property
    def alice_adventures_jobs(self) -> List[str]:
        return [
            "Wonderland Entrance Hall [AA]",
            "White Rabbit's House [AA]",
            "Caterpillar's Mushroom [AA]",
            "Mad Tea Party [AA]",
            "Queen's Hearts' Court [AA]",
        ]

    @functools.cached_property
    def shrek_jobs(self) -> List[str]:
        return [
            "Duloc [S]",
            "Hansel's Honeymoon Hideaway [S]",
            "Shrek's Swamp [S]",
            "Fairy Godmother's Potion Factory [S]",
            "Dragon's Lair [S]",
        ]

    @functools.cached_property
    def muckingham_files_part_3_jobs(self) -> List[str]:
        return [
            "Aquarium [TMF-3]",
            "Submarine [TMF-3]",
        ]

    @functools.cached_property
    def muckingham_files_part_4_jobs(self) -> List[str]:
        return [
            "Modern Mansion [TMF-4]",
            "Fire Plane [TMF-4]",
        ]

    @functools.cached_property
    def santa_workshop_jobs(self) -> List[str]:
        return [
            "Santa's Workshop [W2023]",
        ]

    @functools.cached_property
    def cruise_ship_sun_deck_jobs(self) -> List[str]:
        return [
            "Cruise Ship Sun Deck [S2024]",
        ]

    @functools.cached_property
    def halloween_seasonal_2024_jobs(self) -> List[str]:
        return [
            "Halloween House [H2024]",
        ]

    @functools.cached_property
    def ice_rink_jobs(self) -> List[str]:
        return [
            "Ice Rink [W2024]",
        ]

    def jobs(self) -> List[str]:
        jobs: List[str] = self.free_play_jobs[:]

        if self.has_dlc_tomb_raider:
            jobs.extend(self.tomb_raider_jobs[:])
        
        if self.has_dlc_midgar:
            jobs.extend(self.midgar_jobs[:])
        
        if self.has_dlc_spongebob_squarepants:
            jobs.extend(self.spongebob_squarepants_jobs[:])
        
        if self.has_dlc_back_to_the_future:
            jobs.extend(self.back_to_the_future_jobs[:])
        
        if self.has_dlc_santa_workshop:
            jobs.extend(self.santa_workshop_jobs[:])
        
        if self.has_dlc_warhammer_40000:
            jobs.extend(self.warhammer_40000_jobs[:])
        
        if self.has_dlc_alice_adventures:
            jobs.extend(self.alice_adventures_jobs[:])
        
        if self.has_dlc_muckingham_files_part_3:
            jobs.extend(self.muckingham_files_part_3_jobs[:])
        
        if self.has_dlc_muckingham_files_part_4:
            jobs.extend(self.muckingham_files_part_4_jobs[:])
        
        if self.has_dlc_cruise_ship_sun_deck:
            jobs.extend(self.cruise_ship_sun_deck_jobs[:])
        
        if self.has_dlc_shrek:
            jobs.extend(self.shrek_jobs[:])
        
        if self.has_dlc_halloween_seasonal_2024:
            jobs.extend(self.halloween_seasonal_2024_jobs[:])
        
        if self.has_dlc_ice_rink:
            jobs.extend(self.ice_rink_jobs[:])

        return jobs


# Archipelago Options
class PowerWashSimulatorDLCOwned(OptionSet):
    """
    Indicates which PowerWash Simulator DLC the player owns, if any.
    """

    display_name = "PowerWash Simulator DLC Owned"
    valid_keys = [
        "Tomb Raider",
        "Midgar",
        "Spongebob Squarepants",
        "Back to the Future",
        "Santa's Workshop - Winter 2023",
        "Warhammer 40,000",
        "Alice's Adventures",
        "Muckingham Files - Part 3",
        "Muckingham Files - Part 4",
        "Cruise Ship Sun Deck - Summer 2024",
        "Shrek",
        "Halloween Seasonal 2024",
        "Ice Rink - Winter 2024",
    ]

    default = valid_keys
