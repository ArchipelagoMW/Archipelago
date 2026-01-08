from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class ForzaHorizon5ArchipelagoOptions:
    forza_horizon_5_dlc_owned: ForzaHorizon5DLCOwned


class ForzaHorizon5Game(Game):
    name = "Forza Horizon 5"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = ForzaHorizon5ArchipelagoOptions

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
                label="Finish PLACEMENT on TRACK with a car from the following brand: BRAND",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACK": (self.tracks_including_long, 1),
                    "BRAND": (self.car_brands, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACK with a car from the following class: CLASS",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACK": (self.tracks_including_long, 1),
                    "CLASS": (self.car_classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACK with a car from the following type: TYPE",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACK": (self.tracks_including_long, 1),
                    "TYPE": (self.car_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACKS with a car from the following brand: BRAND",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACKS": (self.tracks, 3),
                    "BRAND": (self.car_brands, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACKS with a car from the following class: CLASS",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACKS": (self.tracks, 3),
                    "CLASS": (self.car_classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Finish PLACEMENT on TRACKS with a car from the following type: TYPE",
                data={
                    "PLACEMENT": (self.race_placements, 1),
                    "TRACKS": (self.tracks, 3),
                    "TYPE": (self.car_types, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Get at least STAR stars on the following PR Stunts: PR_STUNTS",
                data={
                    "STAR": (self.star_amount_range, 1),
                    "PR_STUNTS": (self.pr_stunts, 3),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=7,
            ),
            GameObjectiveTemplate(
                label="Get at least STAR stars on the following PR Stunts: PR_STUNTS",
                data={
                    "STAR": (self.star_amount_range, 1),
                    "PR_STUNTS": (self.pr_stunts, 5),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Get at least STAR stars on the following Story Chapter: STORY",
                data={
                    "STAR": (self.star_amount_range, 1),
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
            GameObjectiveTemplate(
                label="Post a clean time on the Rivals leaderboard for TRACK with CLASS car",
                data={
                    "TRACK": (self.tracks_including_long, 1),
                    "CLASS": (self.car_classes_alternate, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play a round of ONLINE",
                data={
                    "ONLINE": (self.online_modes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play the EVENTLAB EventLab Blueprint on page PAGE of the TAB tab",
                data={
                    "EVENTLAB": (self.eventlab, 1),
                    "PAGE": (self.eventlab_page_range, 1),
                    "TAB": (self.eventlab_tabs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @property
    def dlc_owned(self) -> List[str]:
        return sorted(self.archipelago_options.forza_horizon_5_dlc_owned.value)

    @property
    def has_dlc_hot_wheels(self) -> bool:
        return "Hot Wheels" in self.dlc_owned

    @property
    def has_dlc_rally_adventure(self) -> bool:
        return "Rally Adventure" in self.dlc_owned

    @property
    def has_dlc_car_pass(self) -> bool:
        return "Car Pass" in self.dlc_owned

    @property
    def has_dlc_formula_drift_pack(self) -> bool:
        return "Formula Drift Pack" in self.dlc_owned

    @property
    def has_dlc_welcome_pack(self) -> bool:
        return "Welcome Pack" in self.dlc_owned

    @property
    def has_dlc_horizon_racing_car_pack(self) -> bool:
        return "Horizon Racing Car Pack" in self.dlc_owned

    @property
    def has_dlc_italian_exotics_car_pack(self) -> bool:
        return "Italian Exotics Car Pack" in self.dlc_owned

    @property
    def has_dlc_super_speed_car_pack(self) -> bool:
        return "Super Speed Car Pack" in self.dlc_owned

    @property
    def has_dlc_american_automotive_car_pack(self) -> bool:
        return "American Automotive Car Pack" in self.dlc_owned

    @property
    def has_dlc_fast_x_car_pack(self) -> bool:
        return "Fast X Car Pack" in self.dlc_owned

    @property
    def has_dlc_chinese_lucky_stars_car_pack(self) -> bool:
        return "Chinese Lucky Stars Car Pack" in self.dlc_owned

    @property
    def has_dlc_european_automotive_car_pack(self) -> bool:
        return "European Automotive Car Pack" in self.dlc_owned

    @property
    def has_dlc_acceleration_car_pack(self) -> bool:
        return "Acceleration Car Pack" in self.dlc_owned

    @property
    def has_dlc_apex_allstars_car_pack(self) -> bool:
        return "Apex Allstars Car Pack" in self.dlc_owned

    @property
    def has_dlc_universal_icons_car_pack(self) -> bool:
        return "Universal Icons Car Pack" in self.dlc_owned

    @property
    def has_dlc_jdm_jewels_car_pack(self) -> bool:
        return "JDM Jewels Car Pack" in self.dlc_owned

    @functools.cached_property
    def tracks_base_road(self) -> List[str]:
        return [
            "Horizon Mexico Circuit",
            "Emerald Circuit",
            "Llanuras Sprint",
            "Gran Pantano Sprint",
            "Los Jardines Circuit",
            "Dunas Blancas Sprint",
            "Playa Azul Circuit",
            "Riviera Sprint",
            "Chihuahua Circuit",
            "Bola Ocho Circuit",
            "Cathedral Circuit",
            "Panoramica Sprint",
            "Plaza Circuit",
            "Estadio Circuit",
            "Copper Canyon Sprint",
            "Volcan Sprint",
            "Bahia De Plano Circuit",
            "Sierra Verde Sprint",
            "Reservorio Sprint",
            "Lookout Circuit",
            "Tierra Prospera Circuit",
            "Arch of Mulege Circuit",
            "Descansar Dorado Sprint",
            "Rocoso Sprint",
            "Linea Costera Sprint",
            "Winter Wonderland Circuit",
            "Horizon Oval Circuit",
            "Cloverleaf Sprint",
            "Valle Del Rio Sprint",
            "San Juan Sprint",
            "Vista Del Mar Sprint",
        ]

    @functools.cached_property
    def tracks_base_dirt(self) -> List[str]:
        return [
            "Mulege Town Scramble",
            "Desierto Trail",
            "Mangrove Scramble",
            "Tulum Trail",
            "Cordillera Trail",
            "Cascada Trail",
            "La Selva Scramble",
            "River Scramble",
            "Baja California Trail",
            "Horizon Baja Scramble",
            "Caldera Scramble",
            "Montana Trail",
            "Fuera Del Camino Trail",
            "El Pipila Scramble",
            "Barranca Trail",
            "Bajio Trail",
            "Teotihuacan Scramble",
            "San Juan Scramble",
            "Tapalpa Trail",
        ]

    @functools.cached_property
    def tracks_base_cross_country(self) -> List[str]:
        return [
            "Airfield Cross Country Circuit",
            "Oasis Cross Country",
            "Ek Balam Cross Country Circuit",
            "Ribera Rocosa Cross Country",
            "Granjas Cross Country",
            "Costera Cross Country Circuit",
            "Baja Cross Country Circuit",
            "Las Dunas Cross Country",
            "El Descenso Cross Country",
            "Urban Cross Country Circuit",
            "Copper Canyon Cross Country",
            "Foto Final Cross Country",
            "Las Ranas Cross Country",
            "Costa Este Cross Country",
            "Restos Cross Country",
            "Herencia Cross Country Circuit",
            "Tropico Cross Country",
            "Festival Cross Country",
            "Estadio Cross Country",
        ]

    @functools.cached_property
    def tracks_base_street(self) -> List[str]:
        return [
            "Bosque Del Sur",
            "Ruta Norte",
            "Costa Rocosa",
            "Horizon Callejera",
            "Guanajuato Sur",
            "Tunnel Run",
            "Las Afueras",
            "Hilltop Descent",
            "Canon Run",
            "Coast Run",
            "Wetland Charge",
            "Granjas De Tapalpa",
            "Jungle Descent",
            "Castillo Del Mar",
            "El Lago Blanco",
            "Festival Gatecrash",
            "Las Laderas",
            "Cruce Del Valle",
            "Carretera Chase",
            "Highland Climb",
        ]

    @functools.cached_property
    def tracks_hot_wheels(self) -> List[str]:
        return [
            "Canyon Racer Speed Sprint",
            "Canyon's Edge Speed Sprint",
            "Ram's Head Speed Sprint",
            "Nexus Speed Circuit",
            "Canyon Loop Speed Sprint",
            "Lava Loop Hazard Sprint",
            "Nexus Speed Sprint",
            "Snow Fields Hazard Circuit",
            "Dragon's Fall Speed Circuit",
            "Canyon's Drop Hazard Sprint",
            "Ice Loop Hazard Sprint",
            "Volcano Pass Hazard Sprint",
            "Twin Loop Speed Circuit",
            "Waterslide Speed Circuit",
            "Forest Falls Hazard Sprint",
            "Forest Gorge Hazard Sprint",
            "Ice Canyon Hazard Sprint",
        ]

    @functools.cached_property
    def tracks_rally_adventure(self) -> List[str]:
        return [
            "Cascada Fuerte",
            "Reserva Del Carrizo",
            "Three Hill",
            "Lago Azulado",
            "Desert Scramble",
            "Forest Trail",
            "Meridian",
            "Rugged Dunes",
            "Tres Colinas",
            "Orogrande",
            "Tierras Verdes",
            "Joya Marron",
            "Crateres Secos",
            "Valle De Pozas",
            "Devil's Pass",
            "El Bosque",
            "The Narrows",
            "La Cantera",
            "Quarry Trail",
            "Arzate Sprint",
            "Palm Forest",
            "Canyon Trail",
            "Senda De Montana",
            "Switchback Run",
            "The Apex Run",
            "Raptor Race!",
            "Desafio",
        ]

    def tracks(self) -> List[str]:
        tracks: List[str] = (
            self.tracks_base_road
            + self.tracks_base_dirt
            + self.tracks_base_cross_country
            + self.tracks_base_street
        )

        if self.has_dlc_hot_wheels:
            tracks.extend(self.tracks_hot_wheels)
        if self.has_dlc_rally_adventure:
            tracks.extend(self.tracks_rally_adventure)

        return sorted(tracks)

    @functools.cached_property
    def tracks_long_base(self) -> List[str]:
        return [
            "The Goliath",
            "The Colossus",
            "The Gauntlet",
            "The Titan",
            "The Marathon",
        ]

    @functools.cached_property
    def tracks_long_hot_wheels(self) -> List[str]:
        return [
            "Hot Wheels Goliath",
        ]

    @functools.cached_property
    def tracks_long_rally_adventure(self) -> List[str]:
        return [
            "Horizon Badlands Goliath",
        ]

    def tracks_long(self) -> List[str]:
        tracks: List[str] = self.tracks_long_base[:]

        if self.has_dlc_hot_wheels:
            tracks.extend(self.tracks_long_hot_wheels)
        if self.has_dlc_rally_adventure:
            tracks.extend(self.tracks_long_rally_adventure)

        return sorted(tracks)

    def tracks_including_long(self) -> List[str]:
        return sorted(self.tracks() + self.tracks_long())

    @functools.cached_property
    def pr_stunts_base(self) -> List[str]:
        return [
            "Coast View Speed Trap",
            "Horizon Baja Speed Trap",
            "Bypass Speed Trap",
            "Baja California Speed Trap",
            "Mudflows Speed Trap",
            "Mountainside Speed Trap",
            "Dustbowl Speed Trap",
            "San de las Minas Speed Trap",
            "Oceano Azul Speed Trap",
            "Drag Strip Speed Trap",
            "Pequeno Pente Speed Trap",
            "Paso Inferior Speed Trap",
            "Autopista Speed Trap",
            "Arid Hills Speed Trap",
            "Los Arboles Speed Trap",
            "Northern Pasage Speed Trap",
            "Caballo Blanco Speed Trap",
            "Escarpment Speed Trap",
            "Bulevar Speed Trap",
            "Callejon Speed Trap",
            "Calle Principal Speed Trap",
            "Estadio Speed Trap",
            "Sendero Speed Trap",
            "Federal Highway Speed Trap",
            "Canyon Pass Speed Trap",
            "East Resort Speed Trap",
            "Avenida Speed Trap",
            "Cloverleaf Speed Trap",
            "Pyramid of the Sun Speed Trap",
            "Levee Speed Trap",
            "Gran Puente Speed Trap",
            "Vado del Rio Speed Trap",
            "Pantano Pass Speed Trap",
            "Swamplands Speed Trap",
            "Tulum Speed Trap",
            "La Silica Speed Zone",
            "Mountain Pass Speed Zone",
            "La Subida Speed Zone",
            "Costa Rocosa Speed Zone",
            "Switchbacks Speed Zone",
            "Festival Speed Zone",
            "Desierto Viviente Speed Zone",
            "Punta Allen Speed Zone",
            "Cordillera Speed Zone",
            "Ranchito Speed Zone",
            "Airfield Speed Zone",
            "Orilla del Rio Speed Zone",
            "Green Hills Speed Zone",
            "Atlantes de Tula Speed Zone",
            "Trebol Speed Zone",
            "Pyramid of the Moon Speed Zone",
            "Punto de Vista Speed Zone",
            "River Run Speed Zone",
            "Ringroad Speed Zone",
            "Rocky Hills Speed Zone",
            "Ladera Speed Zone",
            "Cliffside Speed Zone",
            "Rio Fuerte Speed Zone",
            "Carretera Speed Zone",
            "Camino del Cielo Speed Zone",
            "Riviera Maya Speed Zone",
            "Watersplash Speed Zone",
            "El Gancho Speed Zone",
            "Desert Dunes Danger Sign",
            "Baja Showjump Danger Sign",
            "Mountain Top Danger Sign",
            "Event Horizon Danger Sign",
            "Launch Control Danger Sign",
            "San Juan Jump Danger Sign",
            "Hotel Danger Sign",
            "Runway Danger Sign",
            "Metal Bird Danger Sign",
            "Heights of Mulege Danger Sign",
            "Salto de Rio Danger Sign",
            "Ridge Crest Danger Sign",
            "Valle Danger Sign",
            "Cascadas Danger Sign",
            "Eagle's Perch Danger Sign",
            "Boardwalk Danger Sign",
            "La Mesa Danger Sign",
            "Cannonball Danger Sign",
            "Stadium Jump Danger Sign",
            "Colina Danger Sign",
            "Basejump Danger Sign",
            "La Cruz Danger Sign",
            "Ranas Saltarinas Danger Sign",
            "Los Jardines Danger Sign",
            "Punto Norte Drift Zone",
            "Las Dunas Drift Zone",
            "Esquisto Drift Zone",
            "Cara Este Drift Zone",
            "Otro Mundo Drift Zone",
            "Giro Encorvado Drift Zone",
            "Hillside Drift Zone",
            "Rancheria Drift Zone",
            "Reservoir Drift Zone",
            "Arbolada Drift Zone",
            "Los Campos Drift Zone",
            "Camino de Montana Drift Zone",
            "Trailbreaker Drift Zone",
            "Polytunnels Drift Zone",
            "Farmland Trail Drift Zone",
            "Las Curvas Drift Zone",
            "Costera Drift Zone",
            "East Coast Drift Zone",
            "Panoramica Drift Zone",
            "Precipice Drift Zone",
            "Sand and Deliver Trailblazer",
            "River Rapids Trailblazer",
            "Over the Dune Trailblazer",
            "Barranco Trailblazer",
            "Festival Descend Trailblazer",
            "Desert Descent Trailblazer",
            "The Juggernaut Trailblazer",
            "Malpais Trailblazer",
            "Jungle Traversal Trailblazer",
            "Granjas Trailblazer",
            "Quebrada Trailblazer",
            "Cascadas Trailblazer",
            "La Marisma Trailblazer",
            "Canyon Run Trailblazer",
            "City Escape Trailblazer",
            "Puerta Petrea Trailblazer",
            "Cruse de Granja Trailblazer",
        ]

    @functools.cached_property
    def pr_stunts_hot_wheels(self) -> List[str]:
        return [
            "Forest Edge Speed Trap",
            "Dragon's Fall Speed Trap",
            "Hammer's Shadow Speed Trap",
            "Horizon Nexus Speed Trap",
            "Nexus View Speed Trap",
            "Treetops Speed Zone",
            "Forest Flume Speed Zone",
            "Supersonic Spiral Speed Zone",
            "Frozen Rush Speed Zone",
            "The Ribbon Speed Zone",
            "Canyon Jump Danger Sign",
            "Canyon Fire Danger Sign",
            "Forest Escape Danger Sign",
            "Forest Leap Danger Sign",
            "Ice Crash Danger Sign",
            "Water's Edge Drift Zone",
            "Rockslide Drift Zone",
            "Turbo Knot Drift Zone",
            "Horizon Nexus Drift Zone",
            "Ice Cauldron Drift Zone",
        ]

    @functools.cached_property
    def pr_stunts_rally_adventure(self) -> List[str]:
        return [
            "Cascada Fuerte Speed Trap",
            "Palm Forest Danger Sign",
            "Reservoir View Speed Zone",
            "Tres Colinas Drift Zone",
            "Tierras Verdes Speed Zone",
            "Tres Colinas Speed Zone",
            "Canyon Rush Speed Zone",
            "Tierras Verdes Drift Zone",
            "Canyon Snap Danger Sign",
            "Canyon Sweep Drift Zone",
            "Devil's Pass Drift Zone",
            "Devil's Pass Speed Zone",
            "Canyon Danger Sign",
            "La Cantera Speed Trap",
            "La Cantera Danger Sign",
            "Dunes Danger Sign",
            "Crateres Secos Speed Zone",
            "Duna Escarpada Speed Trap",
            "Orogrande Rush Speed Trap",
            "Joya Marron Drift Zone",
        ]

    def pr_stunts(self) -> List[str]:
        pr_stunts: List[str] = self.pr_stunts_base[:]

        if self.has_dlc_hot_wheels:
            pr_stunts.extend(self.pr_stunts_hot_wheels)
        if self.has_dlc_rally_adventure:
            pr_stunts.extend(self.pr_stunts_rally_adventure)

        return sorted(pr_stunts)

    @functools.cached_property
    def stories_base(self) -> List[str]:
        return [
            "El Camino - Into The Storm",
            "El Camino - El Camino de Sidney Wolverstone",
            "El Camino - Statue at Sunset",
            "El Camino - Statue at Noon",
            "El Camino - Mulege",
            "El Camino - Cascadas",
            "El Camino - Valle de las Ranas",
            "El Camino - Ek' Balam",
            "El Camino - Temple at Quechula",
            "Vocho - The Vocho",
            "Vocho - Scratch vs Stock",
            "Vocho - Group-V",
            "Vocho - Vocho Skills",
            "Vocho - Vocho can fly!",
            "Vocho - Vocho across Country",
            "Vocho - Cornering Machine!",
            "Vocho - Vocho Speed!",
            "Vocho - Drift-Cho",
            "Vocho - Skill-Cho",
            "Vocho - In the Baja",
            "Vocho - In the Hills",
            "Vocho - Scratch vs Stock, Too",
            "Test Driver Horizon Apex - East Coast Paradise",
            "Test Driver Horizon Apex - Arena de Fiesta",
            "Test Driver Horizon Apex - Coast to Coast",
            "Test Driver Horizon Wilds - Into the Jungle",
            "Test Driver Horizon Wilds - Off the Beaten Trial",
            "Test Driver Horizon Wilds - Surface Battle!",
            "Test Driver Horizon Baja - Sand Trek",
            "Test Driver Horizon Baja - Got the Baja Skills",
            "Test Driver Horizon Baja - Harsh Conditions",
            "Test Driver Horizon Street - City Sights",
            "Test Driver Horizon Street - Speeding Frenzy",
            "Test Driver Horizon Street - Shortcuts Galore",
            "Test Driver Horizon Rush - Canyon Cruise",
            "Test Driver Horizon Rush - Stunt Master",
            "Test Driver Horizon Rush - High Jump",
            "Lucha de Carreteras - Show Me...",
            "Lucha de Carreteras - You Must Train",
            "Lucha de Carreteras - First Bout chapter",
            "Lucha de Carreteras - Qualification",
            "Lucha de Carreteras - Forzudo",
            "Lucha de Carreteras - The Choice",
            "Lucha de Carreteras - Return of the Monster Ghost",
            "Born Fast - Pablo",
            "Born Fast - Charles",
            "Born Fast - Charlie's Request",
            "Born Fast - Antonia",
            "Born Fast - William",
            "Born Fast - Teagan",
            "Born Fast - Katya",
            "Born Fast - Tristan",
            "V10 - Driving Frankie Beaumont",
            "V10 - Scene 15",
            "V10 - Scene 23",
            "V10 - Scene 35a",
            "V10 - Scene 35b",
            "V10 - Scene 43",
            "V10 - Scene 73",
            "V10 - Scene 95",
            "V10 - Scene 107",
            "V10 - Scene 103",
            "V10 - Scene 117",
            "V10 - Post Credit Scene",
            "Donut Media HiLow - Welcome to HiLow",
            "Donut Media Hi Team - Welcome to Hi Team",
            "Donut Media Hi Team - Donut Delivery",
            "Donut Media Hi Team - Time after Time",
            "Donut Media Hi Team - Up to Speed",
            "Donut Media Hi Team - Cars Are Pain",
            "Donut Media Hi Team - Does More Expensive Mean More Better?",
            "Donut Media Low Team - Welcome to Low Team",
            "Donut Media Low Team - Every Car at Horizon RANKED",
            "Donut Media Low Team - Deja vu",
            "Donut Media Low Team - Bumper 2 Bumper",
            "Donut Media Low Team - To The Rescue",
            "Donut Media Low Team - Does More Expensive Mean More Better?",
            "Donut Media @ Horizon - Horizon, meet Donut",
            "Donut Media @ Horizon - The Test Track",
            "Donut Media @ Horizon - HRSPRS",
            "Donut Media @ Horizon - Rally Up!",
            "Donut Media @ Horizon - The Donut Showdown",
            "Horizon Origins - Horizon Mexico",
            "Horizon Origins - Horizon Colorado",
            "Horizon Origins - Horizon Europe",
            "Horizon Origins - Horizon Australia",
            "Horizon Origins - Horizon UK",
            "Made in Mexico - Made in Mexico",
            "Made in Mexico - Buggy in the Baja",
            "Made in Mexico - Viva el Vocho",
            "Made in Mexico - Through the Eras",
            "Made in Mexico - The Timeless Mk1",
            "Made in Mexico - The Powerful Mk7",
            "Made in Mexico - Living La Vida Loba",
            "Made in Mexico - Muchos Caballos",
            "Made in Mexico - La Carrera Panamericana",
            "Drift Club - Back in the Slide Again",
            "Drift Club - Reservoir Drift",
            "Drift Club - Jungle Kick",
            "Drift Club - Canyon Curves",
            "Drift Club - Volcano Run",
            "Drift Club - Drift Club Mexico",
            "Icons of Speed - Lessons from the Past",
            "Icons of Speed - History 101",
            "Icons of Speed - Hot Rod Time Machine",
            "Icons of Speed - Come with Me if You Want to Race",
            "Icons of Speed - One Thing After Another",
            "Icons of Speed - Past Midnight",
            "Icons of Speed - Pressure and Time",
            "Icons of Speed - A Race for the Ages",
        ]

    @functools.cached_property
    def stories_hot_wheels(self) -> List[str]:
        return [
            "Ice Ice Maybe? (Hot Wheels Rookie Qualifier)",
            "Surf's Down (Hot Wheels Pro Qualifier)",
            "Now This Isn't Pod Racing (Hot Wheels Expert Qualifier)",
            "Bad To The Blade Runner (Hot Wheels Elite Qualifier)",
            "Hot Wheels: A History of Speed - The Beginning",
            "Hot Wheels: A History of Speed - The Iconic Orange Track",
            "Hot Wheels: A History of Speed - The Snake & The Mongoose",
            "Hot Wheels: A History of Speed - Treasure Hunting",
            "Hot Wheels: A History of Speed - Hot Wheels Today",
            "Hot Wheels: A History of Speed - The Beginning",
        ]

    def stories(self) -> List[str]:
        stories: List[str] = self.stories_base[:]

        if self.has_dlc_hot_wheels:
            stories.extend(self.stories_hot_wheels)

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
            "Audi",
            "Austin-Healey",
            "Auto Union",
            "BAC",
            "Bentley",
            "BMW",
            "Bugatti",
            "Buick",
            "Cadillac",
            "Can-Am",
            "Caterham",
            "Chevrolet",
            "CUPRA",
            "Datsun",
            "DeBerti",
            "Dodge",
            "Exomotive",
            "Extreme E",
            "Ferrari",
            "FIAT",
            "Ford",
            "Formula Drift",
            "Funco Motorsports",
            "GMC",
            "Hennessey",
            "Holden",
            "Honda",
            "Hoonigan",
            "Hot Wheels",
            "HSV",
            "HUMMER",
            "Hyundai",
            "Infiniti",
            "International",
            "Italdesign",
            "Jaguar",
            "Jeep",
            "Koenigsegg",
            "KTM",
            "Lamborghini",
            "Lancia",
            "Land Rover",
            "Lexus",
            "Local Motors",
            "Lola",
            "Lotus",
            "Lynk & Co",
            "Maserati",
            "Mazda",
            "McLaren",
            "Mercedes-AMG",
            "Mercedes-Benz",
            "Meyers",
            "MINI",
            "Mitsubishi",
            "Morgan",
            "Morris",
            "Mosler",
            "Napier",
            "Nissan",
            "Opel",
            "Pagani",
            "Peel",
            "Penhall",
            "Peugeot",
            "Plymouth",
            "Polaris",
            "Pontiac",
            "Porsche",
            "Radical",
            "Ram",
            "Reliant",
            "Renault",
            "Rimac",
            "RJ Anderson",
            "Saleen",
            "Shelby",
            "SIERRA Cars",
            "SUBARU",
            "Toyota",
            "TVR",
            "Ultima",
            "Vauxhall",
            "Volkswagen",
            "Volvo",
            "VUHL",
            "Willys",
            "Xpeng",
            "Zenvo",
        ]

    @functools.cached_property
    def car_brands_hot_wheels(self) -> List[str]:
        return [
            "Brabham",
            "Schuppan",
        ]

    @functools.cached_property
    def car_brands_rally_adventure(self) -> List[str]:
        return [
            "Casey Currie Motorsports",
            "Jimco",
        ]

    @functools.cached_property
    def car_brands_car_pass(self) -> List[str]:
        return [
            "Forsberg Racing",
            "Mercury",
            "MG",
            "Noble",
            "Oldsmobile",
        ]

    @functools.cached_property
    def car_brands_european_automotive_car_pack(self) -> List[str]:
        return [
            "Automobili Pininfarina",
        ]

    @functools.cached_property
    def car_brands_chinese_lucky_stars_car_pack(self) -> List[str]:
        return [
            "Wuling",
            "MG",
        ]

    @functools.cached_property
    def car_brands_universal_studios(self) -> List[str]:
        return [
            "Universal Studios",
        ]

    @functools.cached_property
    def car_brands_formula_drift_pack(self) -> List[str]:
        return [
            "Forsberg Racing",
        ]

    @functools.cached_property
    def car_brands_horizon_racing_car_pack(self) -> List[str]:
        return [
            "Forsberg Racing",
        ]

    @functools.cached_property
    def car_brands_american_automotive_car_pack(self) -> List[str]:
        return [
            "Czinger",
        ]

    @functools.cached_property
    def car_brands_jdm_jewels_car_pack(self) -> List[str]:
        return [
            "Autozam",
        ]

    @functools.cached_property
    def car_brands_super_speed_car_pack(self) -> List[str]:
        return [
            "Elemental",
        ]

    @functools.cached_property
    def car_brands_fast_and_furious(self) -> List[str]:
        return [
            "Fast & Furious",
        ]

    @functools.cached_property
    def car_brands_acceleration_car_pack(self) -> List[str]:
        return [
            "Ginetta",
        ]

    def car_brands(self) -> List[str]:
        car_brands: List[str] = self.car_brands_base[:]

        if self.has_dlc_hot_wheels:
            car_brands.extend(self.car_brands_hot_wheels)
        if self.has_dlc_rally_adventure:
            car_brands.extend(self.car_brands_rally_adventure)
        if self.has_dlc_car_pass:
            car_brands.extend(self.car_brands_car_pass)
        if self.has_dlc_european_automotive_car_pack:
            car_brands.extend(self.car_brands_european_automotive_car_pack)
        if self.has_dlc_chinese_lucky_stars_car_pack:
            car_brands.extend(self.car_brands_chinese_lucky_stars_car_pack)
        if self.has_dlc_universal_icons_car_pack:
            car_brands.extend(self.car_brands_universal_studios)
        if self.has_dlc_formula_drift_pack:
            car_brands.extend(self.car_brands_formula_drift_pack)
        if self.has_dlc_horizon_racing_car_pack:
            car_brands.extend(self.car_brands_horizon_racing_car_pack)
        if self.has_dlc_american_automotive_car_pack:
            car_brands.extend(self.car_brands_american_automotive_car_pack)
        if self.has_dlc_jdm_jewels_car_pack:
            car_brands.extend(self.car_brands_jdm_jewels_car_pack)
        if self.has_dlc_super_speed_car_pack:
            car_brands.extend(self.car_brands_super_speed_car_pack)
        if self.has_dlc_fast_x_car_pack:
            car_brands.extend(self.car_brands_fast_and_furious)
        if self.has_dlc_acceleration_car_pack:
            car_brands.extend(self.car_brands_acceleration_car_pack)

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
    def car_classes_alternate() -> List[str]:
        return [
            "an X Class",
            "an S2 Class",
            "an S1 Class",
            "an A Class",
            "a B Class",
            "a C Class",
            "a D Class",
        ]

    @staticmethod
    def car_types() -> List[str]:
        return [
            "Buggies",
            "Classic Muscle",
            "Classic Racers",
            "Classic Rally",
            "Classic Sports Cars",
            "Cult Cars",
            "Drift Cars",
            "Extreme Track Toys",
            "GT Cars",
            "Hot Hatch",
            "Hypercars",
            "Modern Muscle",
            "Modern Rally",
            "Modern Sports Cars",
            "Modern Supercars",
            "Offroad",
            "Pickups & 4x4s",
            "Rally Monsters",
            "Rare Classics",
            "Retro Hot Hatch",
            "Retro Muscle",
            "Retro Rally",
            "Retro Saloons",
            "Retro Sports Cars",
            "Retro Supercars",
            "Rods and Customs",
            "Sports Utility Heroes",
            "Super GT",
            "Super Hot Hatch",
            "Super Saloons",
            "Track Toys",
            "Trucks",
            "UTV's",
            "Unlimited Buggies",
            "Unlimited Offroad",
            "Vans & Utility",
            "Vintage Racers",
        ]

    @functools.cached_property
    def skills_standard(self) -> List[str]:
        return [
            "Air",
            "Great Air",
            "Awesome Air",
            "Ultimate Air",
            "Burnout",
            "Great Burnout",
            "Awesome Burnout",
            "Ultimate Burnout",
            "Clean Racing",
            "Great Clean Racing",
            "Awesome Clean Racing",
            "Ultimate Clean Racing",
            "Drafting",
            "Great Drafting",
            "Awesome Drafting",
            "Ultimate Drafting",
            "Drift",
            "Great Drift",
            "Awesome Drift",
            "Ultimate Drift",
            "E-Drift",
            "Great E-Drift",
            "Awesome E-Drift",
            "Ultimate E-Drift",
            "J-Turn",
            "Great J-Turn",
            "Awesome J-Turn",
            "Ultimate J-Turn",
            "Near-Miss",
            "Great Near-Miss",
            "Awesome Near-Miss",
            "Ultimate Near-Miss",
            "One-Eighty",
            "Great One-Eighty",
            "Awesome One-Eighty",
            "Ultimate One-Eighty",
            "Pass",
            "Great Pass",
            "Awesome Pass",
            "Ultimate Pass",
            "Skill Chain",
            "Great Skill Chain",
            "Awesome Skill Chain",
            "Ultimate Skill Chain",
            "Speed",
            "Great Speed",
            "Awesome Speed",
            "Ultimate Speed",
            "Trading Paint",
            "Two Wheels",
            "Great Two Wheels",
            "Awesome Two Wheels",
            "Ultimate Two Wheels",
            "Wreckage",
            "Great Wreckage",
            "Awesome Wreckage",
            "Ultimate Wreckage",
        ]

    @functools.cached_property
    def skills_combo(self) -> List[str]:
        return [
            "Airborne Pass",
            "Barrel Roll",
            "Clean Start",
            "Crash Landing",
            "Daredevil",
            "Drift Tap",
            "Ebisu Style",
            "Hard Charger",
            "Kangaroo",
            "Lucky Escape",
            "Showoff",
            "Sideswipe",
            "Slingshot",
            "Stuntman",
            "Threading the Needle",
            "Triple Pass",
            "Wrecking Ball",
        ]

    @functools.cached_property
    def skills_wreck(self) -> List[str]:
        return [
            "Ant Food",
            "Basurero",
            "Bonus Barrel",
            "Cart Wheels",
            "Feat of Clay",
            "Fruit Salad",
            "Give It Charge",
            "Goooaaalll!!!",
            "Keep It Up",
            "Landscaping",
            "Lumberjack",
            "Road Open",
            "Skillboard",
            "Smactus",
            "Spike!",
            "Throwing Shade",
            "Wrong Number",
            "¡Pop!",
        ]

    @functools.cached_property
    def skills_hot_wheels(self) -> List[str]:
        return [
            "Corkscrew",
            "Ultimate Corkscrew",
            "G-Forza",
            "Great G-Forza",
            "Awesome G-Forza",
            "Ultimate G-Forza",
            "Hot Wheels G-Forza",
            "Speed Boost",
            "Loop-de-Loop",
            "Great Loop-de-Loop",
            "Awesome Loop-de-Loop",
            "Ultimate Loop-de-Loop",
            "Hot Wheels Speed",
            "Hot Wheels Drift",
            "Hot Wheels E-Drift",
            "Hot Wheels Air",
        ]

    def skills(self) -> List[str]:
        skills: List[str] = sorted(
            self.skills_standard
            + self.skills_combo
            + self.skills_wreck
        )

        if self.has_dlc_hot_wheels:
            skills.extend(self.skills_hot_wheels)

        return sorted(skills)

    @staticmethod
    def drivatar_difficulties() -> List[str]:
        return [
            "TOURIST",
            "NEW RACER",
            "NOVICE",
            "AVERAGE",
            "ABOVE AVERAGE",
            "HIGHLY SKILLED",
            "EXPERT",
            "PRO",
            "UNBEATABLE",
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
    def star_amount_range() -> range:
        return range(1, 4)

    @staticmethod
    def online_modes() -> List[str]:
        return [
            "Hide & Seek",
            "The Eliminator",
            "Horizon Super7",
            "Horizon Arcade",
            "Playground Games",
        ]

    @staticmethod
    def eventlab() -> List[str]:
        return [
            "1st",
            "2nd",
            "3rd",
            "4th",
            "5th",
            "6th",
            "7th",
            "8th",
            "9th",
            "10th",
            "11th",
            "12th",
            "13th",
            "14th",
            "15th",
        ]

    @staticmethod
    def eventlab_page_range() -> range:
        return range(1, 6)

    @staticmethod
    def eventlab_tabs() -> List[str]:
        return [
            "PG Editor's Choice",
            # "All-Time Greats",
            # "Trending Today",
            # "Best of the Month",
        ]

    @staticmethod
    def cameras() -> List[str]:
        return [
            "BUMPER",
            "BONNET",
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
            "ULTIMATE",
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


# Archipelago Options
class ForzaHorizon5DLCOwned(OptionSet):
    """
    Indicates which Forza Horizon 5 DLC the player owns, if any.
    """

    display_name = "Forza Horizon 5 DLC Owned"
    valid_keys = [
        "Hot Wheels",
        "Rally Adventure",
        "Car Pass",
        "Formula Drift Pack",
        "Welcome Pack",
        "Horizon Racing Car Pack",
        "Italian Exotics Car Pack",
        "Super Speed Car Pack",
        "American Automotive Car Pack",
        "Fast X Car Pack",
        "Chinese Lucky Stars Car Pack",
        "European Automotive Car Pack",
        "Acceleration Car Pack",
        "Apex Allstars Car Pack",
        "Universal Icons Car Pack",
        "JDM Jewels Car Pack",
    ]

    default = valid_keys
