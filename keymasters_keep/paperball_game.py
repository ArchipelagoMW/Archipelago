from __future__ import annotations

from typing import List, Set

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PaperballArchipelagoOptions:
    paperball_dlc_owned: PaperballDLCOwned
    paperball_included_modes: PaperballIncludedModes
    paperball_included_medal_mode_worlds: PaperballIncludedMedalModeWorlds
    paperball_included_courses: PaperballIncludedCourses


class PaperballGame(Game):
    name = "Paperball"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
    ]

    is_adult_only_or_unrated = False

    options_cls = PaperballArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        if "Medal" in self.included_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete STAGE with a MEDAL medal",
                    data={
                        "STAGE": (self.stages, 1),
                        "MEDAL": (self.medals, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=6,
                ),
                GameObjectiveTemplate(
                    label="Complete STAGE with a Platinum medal",
                    data={
                        "STAGE": (self.stages, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete STAGES with at least 1 MEDAL medal",
                    data={
                        "STAGES": (self.stages, 3),
                        "MEDAL": (self.medals, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=4,
                ),
                GameObjectiveTemplate(
                    label="Complete STAGES with at least 1 Platinum medal",
                    data={
                        "STAGES": (self.stages, 3),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete STAGES with at least 1 MEDAL medal",
                    data={
                        "STAGES": (self.stages, 5),
                        "MEDAL": (self.medals, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="Complete STAGES with at least 1 Platinum medal",
                    data={
                        "STAGES": (self.stages, 5),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        if "Arcade" in self.included_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete COURSE in Arcade mode",
                    data={
                        "COURSE": (self.courses, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete COURSE with Encore Stages in Arcade mode",
                    data={
                        "COURSE": (self.courses, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        if "Blitz" in self.included_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete COURSE in Blitz mode",
                    data={
                        "COURSE": (self.courses, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete COURSE with Encore Stages in Blitz mode",
                    data={
                        "COURSE": (self.courses, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        if "Rush" in self.included_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete COURSE in Rush mode",
                    data={
                        "COURSE": (self.courses, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=2,
                ),
                GameObjectiveTemplate(
                    label="Complete COURSE with Encore Stages in Rush mode",
                    data={
                        "COURSE": (self.courses, 1),
                    },
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        if "Mad Shuffle" in self.included_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="Complete 10 Stages in Mad Shuffle mode",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="Complete COUNT Stages in Mad Shuffle mode",
                    data={
                        "COUNT": (self.stage_counts, 1),
                    },
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=2,
                ),
            ])

        return templates

    @property
    def dlc_owned(self) -> Set[str]:
        return self.archipelago_options.paperball_dlc_owned.value

    @property
    def has_dlc_secret_spy_pack(self) -> bool:
        return "Secret Spy Pack" in self.dlc_owned

    @property
    def has_dlc_deep_sea_pack(self) -> bool:
        return "Deep Sea Pack" in self.dlc_owned

    @property
    def has_dlc_cherry_sky_pack(self) -> bool:
        return "Cherry Sky Pack" in self.dlc_owned

    @property
    def included_modes(self) -> List[str]:
        return sorted(self.archipelago_options.paperball_included_modes.value)

    @property
    def included_medal_mode_worlds(self) -> List[str]:
        return sorted(self.archipelago_options.paperball_included_medal_mode_worlds.value)

    @property
    def included_courses(self) -> List[str]:
        return sorted(self.archipelago_options.paperball_included_courses.value)

    def stages(self) -> List[str]:
        stages = list()

        if "Alpine" in self.included_medal_mode_worlds:
            stages.extend([
                "Frying Pan (Alpine-1)",
                "Canal (Alpine-2)",
                "Basalt Colums (Alpine-3)",
                "Funfair (Alpine-4)",
                "Curved Bridges (Alpine-5)",
                "Railroad (Alpine-6)",
                "Summit (Alpine-7)",
                "Spinning Pizza (Alpine-8)",
                "Nibbled Path (Alpine-9)",
                "Earthquake (Alpine-10)",
            ])

        if "Canyon" in self.included_medal_mode_worlds:
            stages.extend([
                "Trailers (Canyon-1)",
                "Ribbons (Canyon-2)",
                "Bubble Wrap (Canyon-3)",
                "Revolving Doors (Canyon-4)",
                "Stunt Ramp (Canyon-5)",
                "Mouseholes (Canyon-6)",
                "Drop-Off (Canyon-7)",
                "Planets (Canyon-8)",
                "Craters (Canyon-9)",
                "Entropy (Canyon-10)",
            ])

        if "Swamp" in self.included_medal_mode_worlds:
            stages.extend([
                "Tilted Curves (Swamp-1)",
                "Windmills (Swamp-2)",
                "Shifting Slopes (Swamp-3)",
                "Beehive (Swamp-4)",
                "Perforation (Swamp-5)",
                "Impact Velocity (Swamp-6)",
                "Mad House (Swamp-7)",
                "Cliff Edge (Swamp-8)",
                "Bumpy Domes (Swamp-9)",
                "Machinery (Swamp-10)",
            ])

        if "Volcano" in self.included_medal_mode_worlds:
            stages.extend([
                "Waffles (Volcano-1)",
                "Skeleton (Volcano-2)",
                "Double Helix (Volcano-3)",
                "Avalanche (Volcano-4)",
                "Staircase Gaps (Volcano-5)",
                "Zipper (Volcano-6)",
                "Turbines (Volcano-7)",
                "Funnels (Volcano-8)",
                "Branches (Volcano-9)",
                "Lilypads (Volcano-10)",
            ])

        if "Savanna" in self.included_medal_mode_worlds:
            stages.extend([
                "Pendulum (Savanna-1)",
                "Swinging Platforms (Savanna-2)",
                "Trap Doors (Savanna-3)",
                "Expansion (Savanna-4)",
                "Collapse (Savanna-5)",
                "Seesaw Gates (Savanna-6)",
                "Hamster Wheels (Savanna-7)",
                "Drawers (Savanna-8)",
                "Bulldozers (Savanna-9)",
                "Timing (Savanna-10)",
            ])

        if "City" in self.included_medal_mode_worlds:
            stages.extend([
                "Perihelion (City-1)",
                "Centrifugal (City-2)",
                "Seesaw Plate (City-3)",
                "Rolling Drum (City-4)",
                "Thin Descent (City-5)",
                "Three Arches (City-6)",
                "Filter (City-7)",
                "Stop & Go (City-8)",
                "Ring System (City-9)",
                "Clock Hands (City-10)",
            ])

        if "Stratosphere" in self.included_medal_mode_worlds:
            stages.extend([
                "Shuffle (Stratosphere-1)",
                "Pattern (Stratosphere-2)",
                "Rooftop Ramps (Stratosphere-3)",
                "Rotating Blocks (Stratosphere-4)",
                "Cliax Logo (Stratosphere-5)",
                "Wave (Stratosphere-6)",
                "Construct (Stratosphere-7)",
                "Ferris Wheel (Stratosphere-8)",
                "Cylinder Staircase (Stratosphere-9)",
                "Wallride (Stratosphere-10)",
            ])

        if "Antarctic" in self.included_medal_mode_worlds:
            stages.extend([
                "Serial Jumps (Antarctic-1)",
                "Gables (Antarctic-2)",
                "Loops (Antarctic-3)",
                "Roundabouts (Antarctic-4)",
                "Undulation (Antarctic-5)",
                "Propellers (Antarctic-6)",
                "Leap of Faith (Antarctic-7)",
                "Satellite (Antarctic-8)",
                "Mach Speed (Antarctic-9)",
                "Coliseum (Antarctic-10)",
            ])

        if "Coast" in self.included_medal_mode_worlds:
            stages.extend([
                "Razor Blades (Coast-1)",
                "Pong (Coast-2)",
                "Stack (Coast-3)",
                "Railings (Coast-4)",
                "Amphitheater (Coast-5)",
                "Cogwheels (Coast-6)",
                "Broken Twister (Coast-7)",
                "Screw (Coast-8)",
                "Ghost Leg (Coast-9)",
                "Windows (Coast-10)",
            ])

        if "Moon" in self.included_medal_mode_worlds:
            stages.extend([
                "Shattered Bricks (Moon-1)",
                "Twin Spirals (Moon-2)",
                "Trasitions (Moon-3)",
                "Baskets (Moon-4)",
                "Rolling Rocks (Moon-5)",
                "Coiled Cable (Moon-6)",
                "Relay (Moon-7)",
                "Vanishing Road (Moon-8)",
                "Pokey (Moon-9)",
                "Retro (Moon-10)",
            ])

        if "Void" in self.included_medal_mode_worlds:
            stages.extend([
                "Steel Beams (Void-1)",
                "Variable Size (Void-2)",
                "Slicers (Void-3)",
                "Dodge (Void-4)",
                "Nuts & Bolts (Void-5)",
                "Hinges (Void-6)",
                "Roulette (Void-7)",
                "Spike Fences (Void-8)",
                "Mixing Bowls (Void-9)",
                "Squeeze (Void-10)",
            ])

        if self.has_dlc_secret_spy_pack and "Facility" in self.included_medal_mode_worlds:
            stages.extend([
                "Polygonal Drums (Facility-1)",
                "Scythes (Facility-2)",
                "Cheese Grater (Facility-3)",
                "Wrenches (Facility-4)",
                "Cascading Slants (Facility-5)",
                "Checkerboard (Facility-6)",
                "Crossroad (Facility-7)",
                "Jumpstart (Facility-8)",
                "Volery (Facility-9)",
                "Shellfire (Facility-10)",
            ])

        if self.has_dlc_deep_sea_pack and "Underwater" in self.included_medal_mode_worlds:
            stages.extend([
                "Downhill Skaters (Underwater-1)",
                "Spinning Top (Underwater-2)",
                "Origami (Underwater-3)",
                "Kneading Roller (Underwater-4)",
                "Cup Carousel (Underwater-5)",
                "Stadium (Underwater-6)",
                "Corrugation (Underwater-7)",
                "Water Wheels (Underwater-8)",
                "Magnetism (Underwater-9)",
                "Event Horizon (Underwater-10)",
            ])

        if self.has_dlc_cherry_sky_pack and "Orient" in self.included_medal_mode_worlds:
            stages.extend([
                "CD Players (Orient-1)",
                "Leaves (Orient-2)",
                "DIstorted Slopes (Orient-3)",
                "Mushrooms (Orient-4)",
                "Golf (Orient-5)",
                "Nudge (Orient-6)",
                "Quickstep (Orient-7)",
                "Shrinkwrap (Orient-8)",
                "Chambers (Orient-9)",
                "Updraft (Orient-10)",
            ])

        if "Sunflowers Day" in self.included_medal_mode_worlds:
            stages.extend([
                "Big Plus (Sunflowers Day-1)",
                "Viruses (Sunflowers Day-2)",
                "Tunnel (Sunflowers Day-3)",
                "Sliding Rings (Sunflowers Day-4)",
                "Artillery (Sunflowers Day-5)",
                "Engine Rings (Sunflowers Day-6)",
                "Oscillation (Sunflowers Day-7)",
                "Conveyor Belts (Sunflowers Day-8)",
                "Navy (Sunflowers Day-9)",
                "Splitting Arrows (Sunflowers Day-10)",
            ])

        if "Sunflowers Sunset" in self.included_medal_mode_worlds:
            stages.extend([
                "Gondola (Sunflowers Sunset-1)",
                "Moving Blocks (Sunflowers Sunset-2)",
                "Icy Slider (Sunflowers Sunset-3)",
                "Double Loop (Sunflowers Sunset-4)",
                "Wire (Sunflowers Sunset-5)",
                "UFO (Sunflowers Sunset-6)",
                "Spinning Plates (Sunflowers Sunset-7)",
                "Fly Swatter (Sunflowers Sunset-8)",
                "Folded Ruler (Sunflowers Sunset-9)",
                "Triangular Blocks (Sunflowers Sunset-10)",
            ])

        if "Sunflowers Night" in self.included_medal_mode_worlds:
            stages.extend([
                "Scoring Counters (Sunflowers Night-1)",
                "Gutters (Sunflowers Night-2)",
                "Pistons (Sunflowers Night-3)",
                "Hands Up (Sunflowers Night-4)",
                "Manholes (Sunflowers Night-5)",
                "Wind (Sunflowers Night-6)",
                "Lateral Shift (Sunflowers Night-7)",
                "Stealth (Sunflowers Night-8)",
                "Waterslide (Sunflowers Night-9)",
                "Scissors (Sunflowers Night-10)",
            ])

        if "Psychedelic" in self.included_medal_mode_worlds:
            stages.extend([
                "Charge (Psychedelic-1)",
                "Stencil (Psychedelic-2)",
                "Bouncy Castle (Psychedelic-3)",
                "Wheels of Fortune (Psychedelic-4)",
                "Pump Track (Psychedelic-5)",
                "Scoops (Psychedelic-6)",
                "Buzzsaws (Psychedelic-7)",
                "Dynamic (Psychedelic-8)",
                "Shadows (Psychedelic-9)",
                "Anarchy (Psychedelic-10)",
            ])

        return sorted(stages)

    @staticmethod
    def medals() -> List[str]:
        return [
            "Bronze",
            "Silver",
            "Gold",
        ]

    def courses(self) -> List[str]:
        courses: List[str] = list()

        if "Novice" in self.included_courses:
            courses.append("Novice")

        if "Intermediate" in self.included_courses:
            courses.append("Intermediate")

        if "Expert" in self.included_courses:
            courses.append("Expert")

        if "Champion" in self.included_courses:
            courses.append("Champion")

        if self.has_dlc_secret_spy_pack and "Secret Spy" in self.included_courses:
            courses.append("Secret Spy")

        if self.has_dlc_deep_sea_pack and "Deep Sea" in self.included_courses:
            courses.append("Deep Sea")

        if self.has_dlc_cherry_sky_pack and "Cherry Sky" in self.included_courses:
            courses.append("Cherry Sky")

        if "Sunflower Fields" in self.included_courses:
            courses.append("Sunflower Fields")

        return sorted(courses)

    @staticmethod
    def modes() -> List[str]:
        return [
            "Arcade",
            "Blitz",
            "Rush",
        ]

    @staticmethod
    def stage_counts() -> List[int]:
        return [30, 50]


# Archipelago Options
class PaperballDLCOwned(OptionSet):
    """
    Indicates which Paperball DLC the player owns, if any.
    """

    display_name = "Paperball DLC Owned"
    valid_keys = [
        "Secret Spy Pack",
        "Deep Sea Pack",
        "Cherry Sky Pack",
    ]

    default = valid_keys


class PaperballIncludedModes(OptionSet):
    """
    Indicates which modes the player wants to include in their Paperball runs.
    """

    display_name = "Paperball Included Modes"
    valid_keys = [
        "Arcade",
        "Blitz",
        "Medal",
        "Rush",
        "Mad Shuffle",
    ]

    default = valid_keys


class PaperballIncludedMedalModeWorlds(OptionSet):
    """
    Indicates which worlds the player wants to include in their Paperball Medal Mode runs.
    """

    display_name = "Paperball Included Medal Mode Worlds"
    valid_keys = [
        "Alpine",
        "Canyon",
        "Swamp",
        "Volcano",
        "Savanna",
        "City",
        "Stratosphere",
        "Antarctic",
        "Coast",
        "Moon",
        "Void",
        "Facility",
        "Underwater",
        "Orient",
        "Sunflowers Day",
        "Sunflowers Sunset",
        "Sunflowers Night",
        "Psychedelic",
    ]

    default = valid_keys


class PaperballIncludedCourses(OptionSet):
    """
    Indicates which courses the player wants to include in their Paperball runs.
    """

    display_name = "Paperball Included Courses"
    valid_keys = [
        "Novice",
        "Intermediate",
        "Expert",
        "Champion",
        "Secret Spy",
        "Deep Sea",
        "Cherry Sky",
        "Sunflower Fields",
    ]

    default = valid_keys
