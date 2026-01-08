from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class MinecraftMCParksServerArchipelagoOptions:
    minecraft_mcparks_server_has_early_access: MinecraftMCParksServerHasEarlyAccess
    minecraft_mcparks_server_include_big_firework_shows: MinecraftMCParksServerIncludeBigFireworkShows


class MinecraftMCParksServerGame(Game):
    name = "Minecraft MCParks Server"
    platform = KeymastersKeepGamePlatforms.MOD

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = MinecraftMCParksServerArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Avoid warping (when possible)",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = [
            GameObjectiveTemplate(
                label="Ride the following attraction at The Magic Kingdom: ATTRACTION",
                data={
                    "ATTRACTION": (self.magic_kingdom, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at EPCOT: ATTRACTION",
                data={
                    "ATTRACTION": (self.epcot, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Hollywood Studios: ATTRACTION",
                data={
                    "ATTRACTION": (self.hollywood_studios, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Animal Kingdom: ATTRACTION",
                data={
                    "ATTRACTION": (self.animal_kingdom, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Disneyland: ATTRACTION",
                data={
                    "ATTRACTION": (self.disneyland, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at California Adventure: ATTRACTION",
                data={
                    "ATTRACTION": (self.california_adventure, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Universal Studios Florida: ATTRACTION",
                data={
                    "ATTRACTION": (self.universal_studios_florida, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Islands of Adventure: ATTRACTION",
                data={
                    "ATTRACTION": (self.islands_of_adventure, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Busch Gardens Tampa: ATTRACTION",
                data={
                    "ATTRACTION": (self.busch_gardens_tampa, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Knotts Berry Farm: ATTRACTION",
                data={
                    "ATTRACTION": (self.knotts_berry_farm, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Disneyland Paris: ATTRACTION",
                data={
                    "ATTRACTION": (self.disneyland_paris, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attraction at Disney Studios Paris: ATTRACTION",
                data={
                    "ATTRACTION": (self.disney_studios_paris, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Ride the following attractions back-to-back: ATTRACTIONS",
                data={
                    "ATTRACTIONS": (self.walt_disney_world_attractions, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Ride the following attractions back-to-back: ATTRACTIONS",
                data={
                    "ATTRACTIONS": (self.disneyland_resort, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Ride the following attractions back-to-back: ATTRACTIONS",
                data={
                    "ATTRACTIONS": (self.universal_orlando, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Ride the following attractions back-to-back: ATTRACTIONS",
                data={
                    "ATTRACTIONS": (self.busch_gardens_tampa_resort, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Ride the following attractions back-to-back: ATTRACTIONS",
                data={
                    "ATTRACTIONS": (self.knotts_berry_farm_resort, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Ride the following attractions back-to-back: ATTRACTIONS",
                data={
                    "ATTRACTIONS": (self.disneyland_paris_resort, 2),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Watch the following hourly show: SHOW",
                data={
                    "SHOW": (self.small_shows, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find the following Fab 50 Statue: STATUE",
                data={
                    "STATUE": (self.findable_fab_50, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Ride and listen to the following song on Rip Ride Rockit: SONG",
                data={
                    "SONG": (self.ripride_rockit, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

        if self.has_early_access:
            templates.extend([
                GameObjectiveTemplate(
                    label="Ride the following attraction at Volcano Bay: ATTRACTION",
                    data={
                        "ATTRACTION": (self.volcano_bay, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Ride the following attraction at Tokyo Disneyland: ATTRACTION",
                    data={
                        "ATTRACTION": (self.tokyo_disneyland, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Ride the following attraction at Tokyo Disney Sea: ATTRACTION",
                    data={
                        "ATTRACTION": (self.tokyo_disney_sea, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=5,
                ),
                GameObjectiveTemplate(
                    label="Ride the following attractions back-to-back: ATTRACTIONS",
                    data={
                        "ATTRACTIONS": (self.tokey_disney_resort, 2),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        if self.include_big_firework_shows:
            templates.append(
                GameObjectiveTemplate(
                    label="Watch the following time-based Show: SHOW",
                    data={
                        "SHOW": (self.big_firework_shows, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
            )

        return templates

    @property
    def has_early_access(self) -> bool:
        return bool(self.archipelago_options.minecraft_mcparks_server_has_early_access.value)

    @property
    def include_big_firework_shows(self) -> bool:
        return bool(self.archipelago_options.minecraft_mcparks_server_include_big_firework_shows.value)

    @staticmethod
    def magic_kingdom() -> List[str]:
        return [
            "(MK) It's a Small World",
            "(MK) Astro Orbiter",
            "(MK) Big Thunder Mountain Railroad",
            "(MK) Dumbo the Flying Elephant (Left Side)",
            "(MK) Dumbo the Flying Elephant (Right Side)",
            "(MK) Haunted Mansion",
            "(MK) Top of Riverboat",
            "(MK) Mad Tea Party",
            "(MK) Main Street Trolley - Cinderella Castle to Town Square",
            "(MK) Main Street Trolley - Town Square to Cinderella Castle",
            "(MK) Peter Pan's Flight",
            "(MK) Pirates of the Caribbean",
            "(MK) Prince Charming Regal Carousel",
            "(MK) Seven Dwarfs Mine Train",
            "(MK) Space Mountain Alpha",
            "(MK) Space Mountain Omega",
            "(MK) Splash Mountain",
            "(MK) Swiss Family Treehouse",
            "(MK) The Barnstormer",
            "(MK) The Magic Carpets of Aladdin",
            "(MK) The Many Adventures of Winnie the Pooh",
            "(MK) Tom Sawyer Island",
            "(MK) Tomorrowland Speedway",
            "(MK) Tomorrowland Transit Authority PeopleMover",
            "(MK) Under the Sea ~ Journey of The Little Mermaid",
            "(MK) Walt Disney's Enchanted Tiki Room",
        ]

    @staticmethod
    def epcot() -> List[str]:
        return [
            "(EPCOT) Awesome Planet",
            "(EPCOT) Frozen Ever After",
            "(EPCOT) Gran Fiesta Tour Starring The Three Caballeros",
            "(EPCOT) Journey Into Imagination With Figment",
            "(EPCOT) Journey of Water, Inspired by Moana",
            "(EPCOT) Living with the Land",
            "(EPCOT) Spaceship Earth",
            "(EPCOT) Test Track",
            "(EPCOT) The Seas with Nemo and Friends",
        ]

    @staticmethod
    def hollywood_studios() -> List[str]:
        return [
            "(DHS) Alien Swirling Saucers",
            "(DHS) Rock 'N' Roller Coaster Starring Aerosmith",
            "(DHS) Slinky Dog Dash",
            "(DHS) Star Wars Launch Bay",
            "(DHS) The Twilight Zone Tower of Terror",
            "(DHS) Walt Disney Presents",
        ]

    @staticmethod
    def animal_kingdom() -> List[str]:
        return [
            "(AK) DINOSAUR",
            "(AK) Expedition Everest - Legend of the Forbidden Mountain",
            "(AK) Kali River Rapids",
            "(AK) Maharajah Jungle Trek",
            "(AK) Na'vi River Journey",
            "(AK) Primeval Whirl (Left)",
            "(AK) Primeval Whirl (Right)",
            "(AK) The Boneyard",
            "(AK) TriceraTop Spin",
        ]

    @staticmethod
    def disneyland() -> List[str]:
        return [
            "(DL) It's a Small World",
            "(DL) Alice in Wonderland",
            "(DL) Astro Orbitor",
            "(DL) Autopia (Lane 1)",
            "(DL) Autopia (Lane 2)",
            "(DL) Autopia (Lane 3)",
            "(DL) Autopia (Lane 4)",
            "(DL) Big Thunder Mountain Railroad",
            "(DL) Casey Jr. Circus Train",
            "(DL) Davy Crockett's Explorer Canoes",
            "(DL) Disneyland Monorail",
            "(DL) Disneyland Railroad - Main Street Station",
            "(DL) Disneyland Railroad - Mickey's Toontown Station",
            "(DL) Disneyland Railroad - New Orleans Square Station",
            "(DL) Disneyland Railroad - Tomorrowland Station",
            "(DL) Disneyland Railroad Mainstreet",
            "(DL) Disneyland Railroad Toontown",
            "(DL) Disneyland Railroad New Orleans Square",
            "(DL) Disneyland Railroad Tomorrowland",
            "(DL) Dumbo the Flying Elephant",
            "(DL) Gadget's Go Coaster",
            "(DL) Haunted Mansion Holiday",
            "(DL) Indiana Jones Adventure (FastPass Preshow)",
            "(DL) Indiana Jones Adventure (Main Preshow)",
            "(DL) King Arthur Carrousel",
            "(DL) Mad Tea Party",
            "(DL) Main Street Trolley - Sleeping Beauty Castle to Town Square",
            "(DL) Main Street Trolley - Town Square to Sleepin' Beauty Castle",
            "(DL) Matterhorn Bobsleds (Left)",
            "(DL) Matterhorn Bobsleds (Right)",
            "(DL) Mr. Toad's Wild Ride",
            "(DL) Peter Pan's Flight",
            "(DL) Pinocchio's Daring Journey",
            "(DL) Pirates of the Caribbean",
            "(DL) Roger Rabbit's Car Toon Spin",
            "(DL) Snow White's Enchanted Wish",
            "(DL) Space Mountain",
            "(DL) Storybook Land Canal Boats",
            "(DL) Tarzan's Treehouse",
            "(DL) The Disneyland Story presenting Great Moments with Mr. Lincoln",
            "(DL) The Many Adventures of Winnie the Pooh",
            "(DL) Walt Disney's Enchanted Tiki Room",
            "(DL) Star Wars: Rise of the Resistance",
        ]

    @staticmethod
    def california_adventure() -> List[str]:
        return [
            "(DCA) Golden Zephyr",
            "(DCA) Goofy's Sky School",
            "(DCA) Grizzly River Run",
            "(DCA) Incredicoaster",
            "(DCA) Inside Out Emotional Whirlwind",
            "(DCA) Jumpin' Jellyfish",
            "(DCA) Mater's Jingle Jamboree",
            "(DCA) Radiator Springs Racers",
            "(DCA) Red Car Trolley",
            "(DCA) Silly Symphony Swings",
            "(DCA) The Little Mermaid ~ Ariel's Undersea Adventure",
        ]

    @staticmethod
    def universal_studios_florida() -> List[str]:
        return [
            "(USF) MEN IN BLACK ALIEN ATTACK",
            "(USF) Revenge of the Mummy",
            "(USF) Rip Ride Rocket",
        ]

    @staticmethod
    def islands_of_adventure() -> List[str]:
        return [
            "(IOA) Caro-Seuss_el",
            "(IOA) Doctor Doom's Fearfall",
            "(IOA) Dudley Do-Right's Ripsaw Falls",
            "(IOA) Flight of the Hippogriff",
            "(IOA) Hagrid's Magical Creatures Motorbike Adventure",
            "(IOA) Jurassic World VelociCoaster",
            "(IOA) One Fish, Two Fish, Red Fish, Blue Fish",
            "(IOA) Popeye & Bluto's Bilge-Rat Barges",
            "(IOA) Pteranodon Flyers",
            "(IOA) Storm Force Accelatron",
            "(IOA) The Amazing Adventures of Spider-Man",
            "(IOA) The Cat in the Hat",
            "(IOA) The High in the Sky Seuss Trolley Train Ride!",
            "(IOA) The Incredible Hulk Coaster",
        ]

    @staticmethod
    def volcano_bay() -> List[str]:
        return [
            "(VOLCANOBAY) Honu",
            "(VOLCANOBAY) ika Moana",
            "(VOLCANOBAY) Kala Serpentine Body Slide",
            "(VOLCANOBAY) Kopiko Wai Winding River",
            "(VOLCANOBAY) Ko'okiri Body Plunge",
            "(VOLCANOBAY) Krakatau Aqua Coaster",
            "(VOLCANOBAY) Maku of the Maku Round Raft Rides",
            "(VOLCANOBAY) Ohno Drop Slide",
            "(VOLCANOBAY) Ohyah Drop Slide",
            "(VOLCANOBAY) Puka Uli Lagoon",
            "(VOLCANOBAY) Punga Racers",
            "(VOLCANOBAY) Runamukka Reef",
            "(VOLCANOBAY) Tai Nui Serpentine Body Slide",
            "(VOLCANOBAY) Taniwha Tubes (Blue left-facing castmember)",
            "(VOLCANOBAY) Taniwha Tubes (Blue right-facing castmember)",
            "(VOLCANOBAY) Taniwha Tubes (Green left-facing castmember)",
            "(VOLCANOBAY) Taniwha Tubes (Green right-facing castmember)",
            "(VOLCANOBAY) TeAwa The Fearless River",
            "(VOLCANOBAY) The Reef",
            "(VOLCANOBAY) Tot Tiki Reef",
            "(VOLCANOBAY) Waturi Beach",
        ]

    @staticmethod
    def busch_gardens_tampa() -> List[str]:
        return [
            "(BGT) Gwazi Gliders",
            "(BGT) Iron Gwazi",
        ]

    @staticmethod
    def knotts_berry_farm() -> List[str]:
        return [
            "(KNOTTS) Calico River Rapids",
            "(KNOTTS) GhostRider",
        ]

    @staticmethod
    def tokyo_disneyland() -> List[str]:
        return [
            "(TDL) Omnibus",
            "(TDL) The Happy Ride with Baymax",
        ]

    @staticmethod
    def tokyo_disney_sea() -> List[str]:
        return [
            "(TDS) DisneySea Electric Railway - American Waterfront",
            "(TDS) DisneySea Electric Railway - Port Discovery",
            "(TDS) Tower of Terror",
            "(TDS) Venetian Gondolas",
        ]

    @staticmethod
    def disneyland_paris() -> List[str]:
        return [
            "(DLP) Alice's Curious Labyrinth",
            "(DLP) Blanche-Neige et les Sept Nains",
            "(DLP) Casey Jr. - le Petit Train du Cirque",
            "(DLP) Dumbo the Flying Elephant",
            "(DLP) Le Carrousel de Lancelot",
            "(DLP) Le Pays des Contes de Fees",
            "(DLP) Mad Hatter's Tea Cups",
            "(DLP) Orbitron",
            "(DLP) Peter Pan's Flight",
            "(DLP) Star Wars Hyperspace Mountain",
        ]

    @staticmethod
    def disney_studios_paris() -> List[str]:
        return [
            "(DSP) Cars Quatre Roues Rallye",
            "(DSP) Crush's Coaster",
            "(DSP) Les Tapis Volants - Flying Carpets Over Agrabah",
            "(DSP) RC Racer",
            "(DSP) Slinky Dog Zigzag Spin",
            "(DSP) Toy Soldiers Parachute Drop",
        ]

    @staticmethod
    def walt_disney_world_attractions() -> List[str]:
        return [
            "(MK) It's a Small World",
            "(MK) Astro Orbiter",
            "(MK) Big Thunder Mountain Railroad",
            "(MK) Dumbo the Flying Elephant (Left Side)",
            "(MK) Dumbo the Flying Elephant (Right Side)",
            "(MK) Haunted Mansion",
            "(MK) Top of Riverboat",
            "(MK) Mad Tea Party",
            "(MK) Main Street Trolley- Cinderella Castle to Town Square",
            "(MK) Main Street Trolley- Town Square to Cinderella Castle",
            "(MK) Peter Pan's Flight",
            "(MK) Pirates of the Caribbean",
            "(MK) Prince Charming Regal Carrousel",
            "(MK) Seven Dwarfs Mine Train",
            "(MK) Space Mountain Alpha",
            "(MK) Space Mountain Omega",
            "(MK) Splash Mountain",
            "(MK) Swiss Family Treehouse",
            "(MK) The Barnstormer",
            "(MK) The Magic Carpets of Aladdin",
            "(MK) The Many Adventures of Winnie the Pooh",
            "(MK) Tom Sawyer Island",
            "(MK) Tomorrowland Speedway",
            "(MK) Tomorrowland Transit Authority PeopleMover",
            "(MK) Under the Sea ~ Journey of The Little Mermaid",
            "(MK) Walt Disney's Enchanted Tiki Room",
            "(EPCOT) Awesome Planet",
            "(EPCOT) Frozen Ever After",
            "(EPCOT) Gran Fiesta Tour Starring The Three Caballeros",
            "(EPCOT) Journey Into Imagination With Figment",
            "(EPCOT) Journey of Water, Inspired by Moana",
            "(EPCOT) Living with the Land",
            "(EPCOT) Spaceship Earth",
            "(EPCOT) Test Track",
            "(EPCOT) The Seas with Nemo and Friends",
            "(DHS) Alien Swirling Saucers",
            "(DHS) Rock 'N' Roller Coaster Starring Aerosmith",
            "(DHS) Slinky Dog Dash",
            "(DHS) Star Wars Launch Bay",
            "(DHS) The Twilight Zone Tower of Terror",
            "(DHS) Walt Disney Presents",
            "(AK) DINOSAUR",
            "(AK) Expedition Everest- Legend of the Forbidden Mountain",
            "(AK) Kali River Rapids",
            "(AK) Maharajah Jungle Trek",
            "(AK) Na'vi River Journey",
            "(AK) Primeval Whirl (Left)",
            "(AK) Primeval Whirl (Right)",
            "(AK) The Boneyard",
            "(AK) TriceraTop Spin",
        ]

    @staticmethod
    def disneyland_resort() -> List[str]:
        return [
            "(DL) It's a Small World",
            "(DL) Alice in Wonderland",
            "(DL) Astro Orbitor",
            "(DL) Autopia (Lane 1)",
            "(DL) Autopia (Lane 2)",
            "(DL) Autopia (Lane 3)",
            "(DL) Autopia (Lane 4)",
            "(DL) Big Thunder Mountain Railroad",
            "(DL) Casey Jr. Circus Train",
            "(DL) Davy Crockett's Explorer Canoes",
            "(DL) Disneyland Monorail",
            "(DL) Disneyland Railroad - Main Street Station",
            "(DL) Disneyland Railroad - Mickey's Toontown Station",
            "(DL) Disneyland Railroad - New Orleans Square Station",
            "(DL) Disneyland Railroad - Tomorrowland Station",
            "(DL) Disneyland Railroad Mainstreet",
            "(DL) Disneyland Railroad Toontown",
            "(DL) Disneyland Railroad New Orleans Square",
            "(DL) Disneyland Railroad Tomorrowland",
            "(DL) Dumbo the Flying Elephant",
            "(DL) Gadget's Go Coaster",
            "(DL) Haunted Mansion Holiday",
            "(DL) Indiana Jones Adventure (FastPass Preshow)",
            "(DL) Indiana Jones Adventure (Main Preshow)",
            "(DL) King Arthur Carrousel",
            "(DL) Mad Tea Party",
            "(DL) Main Street Trolley - Sleeping Beauty Castle to Town Square",
            "(DL) Main Street Trolley - Town Square to Sleepin Beauty Castle",
            "(DL) Matterhorn Bobsleds (Left)",
            "(DL) Matterhorn Bobsleds (Right)",
            "(DL) Mr. Toad's Wild Ride",
            "(DL) Peter Pan's Flight",
            "(DL) Pinocchio's Daring Journey",
            "(DL) Pirates of the Caribbean",
            "(DL) Roger Rabbit's Car Toon Spin",
            "(DL) Snow White's Enchanted Wish",
            "(DL) Space Mountain",
            "(DL) Storybook Land Canal Boats",
            "(DL) Star Wars: Rise of the Resistance",
            "(DL) Tarzan's Treehouse",
            "(DL) The Disneyland Story presenting Great Moments with Mr. Lincoln",
            "(DL) The Many Adventures of Winnie the Pooh",
            "(DL) Walt Disney's Enchanted Tiki Room",
            "(DCA) Golden Zephyr",
            "(DCA) Goofy's Sky School",
            "(DCA) Grizzly River Run",
            "(DCA) Incredicoaster",
            "(DCA) Inside Out Emotional Whirlwind",
            "(DCA) Jumpin' Jellyfish",
            "(DCA) Mater's Jingle Jamboree",
            "(DCA) Radiator Springs Racers",
            "(DCA) Red Car Trolley",
            "(DCA) Silly Symphony Swings",
            "(DCA) The Little Mermaid ~ Ariel's Undersea Adventure",
        ]

    @functools.cached_property
    def universal_orlando_base(self) -> List[str]:
        return [
            "(USF) MEN IN BLACK ALIEN ATTACK",
            "(USF) Revenge of the Mummy",
            "(USF) Rip Ride Rocket",
            "(IOA) Caro-Seuss_el",
            "(IOA) Doctor Doom's Fearfall",
            "(IOA) Dudley Do-Right's Ripsaw Falls",
            "(IOA) Flight of the Hippogriff",
            "(IOA) Hagrid's Magical Creatures Motorbike Adventure",
            "(IOA) Jurassic World VelociCoaster",
            "(IOA) One Fish, Two Fish, Red Fish, Blue Fish",
            "(IOA) Popeye & Bluto's Bilge-Rat Barges",
            "(IOA) Pteranodon Flyers",
            "(IOA) Storm Force Accelatron",
            "(IOA) The Amazing Adventures of Spider-Man",
            "(IOA) The Cat in the Hat",
            "(IOA) The High in the Sky Seuss Trolley Train Ride!",
            "(IOA) The Incredible Hulk Coaster",
        ]

    @functools.cached_property
    def universal_orlando_early_access(self) -> List[str]:
        return [
            "(VOLCANOBAY) Honu",
            "(VOLCANOBAY) ika Moana",
            "(VOLCANOBAY) Kala Serpentine Body Slide",
            "(VOLCANOBAY) Kopiko Wai Winding River",
            "(VOLCANOBAY) Ko'okiri Body Plunge",
            "(VOLCANOBAY) Krakatau Aqua Coaster",
            "(VOLCANOBAY) Maku of the Maku Round Raft Rides",
            "(VOLCANOBAY) Ohno Drop Slide",
            "(VOLCANOBAY) Ohyah Drop Slide",
            "(VOLCANOBAY) Puka Uli Lagoon",
            "(VOLCANOBAY) Punga Racers",
            "(VOLCANOBAY) Runamukka Reef",
            "(VOLCANOBAY) Tai Nui Serpentine Body Slide",
            "(VOLCANOBAY) Taniwha Tubes (Blue left-facing castmember)",
            "(VOLCANOBAY) Taniwha Tubes (Blue right-facing castmember)",
            "(VOLCANOBAY) Taniwha Tubes (Green left-facing castmember)",
            "(VOLCANOBAY) Taniwha Tubes (Green right-facing castmember)",
            "(VOLCANOBAY) TeAwa The Fearless River",
            "(VOLCANOBAY) The Reef",
            "(VOLCANOBAY) Tot Tiki Reef",
            "(VOLCANOBAY) Waturi Beach",
        ]

    def universal_orlando(self) -> List[str]:
        stages: List[str] = self.universal_orlando_base[:]

        if self.has_early_access:
            stages.extend(self.universal_orlando_early_access[:])

        return stages

    @staticmethod
    def busch_gardens_tampa_resort() -> List[str]:
        return [
            "(BGT) Gwazi Gliders",
            "(BGT) Iron Gwazi",
        ]

    @staticmethod
    def knotts_berry_farm_resort() -> List[str]:
        return [
            "(KNOTTS) Calico River Rapids",
            "(KNOTTS) GhostRider",
            "(KNOTTS) Pan for gold",
        ]

    @staticmethod
    def tokey_disney_resort() -> List[str]:
        return [
            "(TDL) Omnibus",
            "(TDL) The Happy Ride with Baymax",
            "(TDS) DisneySea Electric Railway - American Waterfront",
            "(TDS) DisneySea Electric Railway - Port Discovery",
            "(TDS) Tower of Terror",
            "(TDS) Venetian Gondolas",
        ]

    @staticmethod
    def disneyland_paris_resort() -> List[str]:
        return [
            "(DLP) Alice's Curious Labyrinth",
            "(DLP) Blanche-Neige et les Sept Nains",
            "(DLP) Casey Jr. - le Petit Train du Cirque",
            "(DLP) Dumbo the Flying Elephant",
            "(DLP) Le Carrousel de Lancelot",
            "(DLP) Le Pays des Contes de Fees",
            "(DLP) Mad Hatter's Tea Cups",
            "(DLP) Orbitron",
            "(DLP) Peter Pan's Flight",
            "(DLP) Star Wars Hyperspace Mountain",
            "(DSP) Cars Quatre Roues Rallye",
            "(DSP) Crush's Coaster",
            "(DSP) Les Tapis Volants - Flying Carpets Over Agrabah",
            "(DSP) RC Racer",
            "(DSP) Slinky Dog Zigzag Spin",
            "(DSP) Toy Soldiers Parachute Drop",
        ]

    @staticmethod
    def big_firework_shows() -> List[str]:
        return [
            "Remember... Dreams Come True",
            "Epcot Forever",
            "Happily Ever After",
            "Electrical Water Pageant",
            "Kiss Goodnight",
            "Sweethearts's Nite Fireworks",
        ]

    @staticmethod
    def small_shows() -> List[str]:
        return [
            "Dapper Dans",
            "Light the Night",
            "Disneyland Paris Fountain Show",
            "Small World Clock Tower Doll Show",
        ]

    @staticmethod
    def findable_fab_50() -> List[str]:
        return [
            "Mickey Mouse (Hub)",
            "Minnie Mouse (Hub)",
            "Pluto (Hub)",
            "Goofy (Hub)",
            "Daisy Duck (Hub)",
            "Donald Duck (Hub)",
            "Chip and Dale (Hub)",
            "Dumbo and Timothy Q. Mouse (Hub)",
            "Winnie the Pooh and Piglet (Hub)",
            "Tinkerbell (Hub)",
            "Jaq and Gus Gus (Castle)",
            "Lady and the Tramp (Town Square)",
            "Abu (Adventureland)",
            "Orange Bird (Adventureland)",
            "Pinocchio (Fantasyland)",
            "Cogsworth and Lumiere (Fantasyland)",
            "The Cheshire Cat (Fantasyland)",
            "The Mad Hatter (Fantasyland)",
            "Stich (Tomorrowland)",
            "Figment (World Discovery)",
            "Miguel (World Showcase)",
            "Dante (World Showcase)",
            "Rocket Raccoon and Groot (World Showcase)",
            "Olaf and Bruni (World Showcase)",
            "Pua and Hei Hei (World Showcase)",
            "Woody and Bo Peep (Chinese Theater)",
            "Flounder and Sebastian (Animation Courtyard)",
            "Joe Gardner (Chinese Theater)",
            "Edna Mode (Chinese Theater)",
            "Frozone (Chinese Theater)",
            "R2-D2 (Echo Lake)",
            "BB8 (Echo Lake)",
            "Timon and Pumba (Discovery Island)",
            "Simba (Discovery Island)",
            "Bambi and Thumper (Discovery Island)",
            "Nemo and Dory (Tree of Life)",
        ]

    @staticmethod
    def ripride_rockit() -> List[str]:
        return [
            "Hidden Song",
            "Born To Be Wild",
            "Bring Me To Life",
            "Gimmie All YOur Lovin",
            "Kickstart My Heart",
            "Paralyzer",
            "Rollin",
            "Bad Girls",
            "Can't Touch This",
            "Glamorous",
            "I Will Survive",
            "That's The Way",
            "All Night Long",
            "Devil Went Down to Georgia",
            "Guitars Cadilacs",
            "I Can Sleep When I'm Dead",
            "Living In Fast Forward",
            "Midnight Rider",
            "Don't Phunk With My Heart",
            "Insane In The Brain",
            "Pump It",
            "Sabotage",
            "Busy Child",
            "Intergalactic",
            "Keep Hope Alive",
            "Le Disko",
            "Pump Up The Volume",
        ]


# Archipelago Options
class MinecraftMCParksServerHasEarlyAccess(Toggle):
    """
    Indicates whether the player has a rank or early access for the Minecraft MCParks Server.
    """

    display_name = "Minecraft MCParks Server Has Early Access"


class MinecraftMCParksServerIncludeBigFireworkShows(Toggle):
    """
    Indicates whether to include big firework shows when generating Minecraft MCParks Server objectives.
    """

    display_name = "Minecraft MCParks Server Include Big Firework Shows"
