from __future__ import annotations

from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PlatinumQuestArchipelagoOptions:
    platinumquest_level_packs: PlatinumQuestLevelPacks
    platinumquest_difficulties: PlatinumQuestDifficulties


class PlatinumQuestGame(Game):
    name = "PlatinumQuest"
    platform = KeymastersKeepGamePlatforms.MOD

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = PlatinumQuestArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Beat the Gold/Platinum Times/Scores",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Complete the level(s) without jumping or blast (Blast is Ultra exclusive)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Complete the level(s) without powerups",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Beat the Ultimate Time/Score (Except Gold Levels!)",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="If the level has an Easter Egg, collect it",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()

        if "Gold" in self.level_packs:
            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Gold Beginner",
                        data={
                            "LEVEL": (self.levels_gold_beginner, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Gold Intermediate",
                        data={
                            "LEVEL": (self.levels_gold_intermediate, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Gold Advanced",
                        data={
                            "LEVEL": (self.levels_gold_advanced, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

        if "Ultra" in self.level_packs:
            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Ultra Beginner",
                        data={
                            "LEVEL": (self.levels_ultra_beginner, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Ultra Intermediate",
                        data={
                            "LEVEL": (self.levels_ultra_intermediate, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Ultra Advanced",
                        data={
                            "LEVEL": (self.levels_ultra_advanced, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

        if "Platinum" in self.level_packs:
            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Platinum Beginner",
                        data={
                            "LEVEL": (self.levels_platinum_beginner, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Platinum Intermediate",
                        data={
                            "LEVEL": (self.levels_platinum_intermediate, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Platinum Advanced",
                        data={
                            "LEVEL": (self.levels_platinum_advanced, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

            if "Expert" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: Platinum Expert",
                        data={
                            "LEVEL": (self.levels_platinum_expert, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    )
                )

        if "PlatinumQuest" in self.level_packs:
            if "Tutorial" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Tutorial",
                        data={
                            "LEVEL": (self.levels_platinumquest_tutorial, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Beginner",
                        data={
                            "LEVEL": (self.levels_platinumquest_beginner, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Intermediate",
                        data={
                            "LEVEL": (self.levels_platinumquest_intermediate, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Advanced",
                        data={
                            "LEVEL": (self.levels_platinumquest_advanced, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

        if "PlatinumQuest Locked" in self.level_packs:
            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Beginner",
                        data={
                            "LEVEL": (self.levels_platinumquest_beginner_locked, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Intermediate",
                        data={
                            "LEVEL": (self.levels_platinumquest_intermediate_locked, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Advanced",
                        data={
                            "LEVEL": (self.levels_platinumquest_advanced_locked, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

            if "Expert" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Complete LEVEL from Level Pack: PlatinumQuest Expert",
                        data={
                            "LEVEL": (self.levels_platinumquest_expert_locked, 1),
                        },
                        is_time_consuming=True,
                        is_difficult=True,
                        weight=1,
                    )
                )

        if "Hunt" in self.level_packs:
            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Beginner",
                        data={
                            "LEVEL": (self.levels_hunt_beginner, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Intermediate",
                        data={
                            "LEVEL": (self.levels_hunt_intermediate, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Advanced",
                        data={
                            "LEVEL": (self.levels_hunt_advanced, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

        if "Hunt Snow" in self.level_packs:
            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Beginner Snow",
                        data={
                            "LEVEL": (self.levels_hunt_snow_beginner, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Intermediate Snow",
                        data={
                            "LEVEL": (self.levels_hunt_snow_intermediate, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Advanced Snow",
                        data={
                            "LEVEL": (self.levels_hunt_snow_advanced, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

        if "Hunt Fright" in self.level_packs:
            if "Beginner" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Beginner Fright",
                        data={
                            "LEVEL": (self.levels_hunt_fright_beginner, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Intermediate" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Intermediate Fright",
                        data={
                            "LEVEL": (self.levels_hunt_fright_intermediate, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=False,
                        weight=1,
                    )
                )

            if "Advanced" in self.difficulties:
                templates.append(
                    GameObjectiveTemplate(
                        label="Beat the Platinum Score in LEVEL from Level Pack: Hunt Advanced Fright",
                        data={
                            "LEVEL": (self.levels_hunt_fright_advanced, 1),
                        },
                        is_time_consuming=False,
                        is_difficult=True,
                        weight=1,
                    )
                )

        return templates

    @property
    def level_packs(self):
        return sorted(self.archipelago_options.platinumquest_level_packs.value)

    @property
    def difficulties(self):
        return sorted(self.archipelago_options.platinumquest_difficulties.value)

    @staticmethod
    def levels_gold_beginner() -> List[str]:
        return [
            "Learning to Roll",
            "Collect the Gems",
            "Jump Training",
            "Learn the Super Jump",
            "Platform Training",
            "Learn the Super Speed",
            "Elevator",
            "Air Movement",
            "Gyrocopter",
            "Time Trial",
            "Super Bounce",
            "Gravity Helix",
            "Shock Absorber",
            "There and Back Again",
            "Marble Materials Lab",
            "Bumper Training",
            "Breezeway",
            "Mine Field",
            "Trapdoors!",
            "Tornado Bowl",
            "Pitfalls",
            "Platform Party",
            "Winding Road",
            "Grand Finale",
        ]

    @staticmethod
    def levels_gold_intermediate() -> List[str]:
        return [
            "Jump jump jump",
            "Monster Speedway Qualifying",
            "Skate Park",
            "Ramp Matrix",
            "Hoops",
            "Go for the Green",
            "Fork in the Road",
            "Tri Twist",
            "Marbletris",
            "Space Slide",
            "Skee Ball Bonus",
            "Marble Playground",
            "Hop Skip and a Jump",
            "Take the High Road",
            "Half-Pipe",
            "Gauntlet",
            "Moto-Marblecross",
            "Shock Drop",
            "Spork in the Road",
            "Great Divide",
            "The Wave",
            "Tornado Alley",
            "Monster Speedway",
            "Upward Spiral",
        ]

    @staticmethod
    def levels_gold_advanced() -> List[str]:
        return [
            "Thrill Ride",
            "Money Tree",
            "Fan Lift",
            "Leap of Faith",
            "Freeway Crossing",
            "Stepping Stones",
            "Obstacle Course",
            "Points of the Compass",
            "Three-Fold Maze",
            "Tube Treasure",
            "Slip 'n Slide",
            "Skyscraper",
            "Half Pipe Elite",
            "A-Maze-ing",
            "Block Party",
            "Trap Door Madness",
            "Moebius Strip",
            "Great Divide Revisited",
            "Escher's Race",
            "To the Moon",
            "Around the World in 30 seconds",
            "Will o' the Wisp",
            "Twisting the night away",
            "Survival of the Fittest",
            "Plumber's Portal",
            "Siege",
            "Ski Slopes",
            "Ramps Reloaded",
            "Tower Maze",
            "Free Fall",
            "Acrobat",
            "Whirl",
            "Mudslide",
            "Pipe Dreams",
            "Scaffold",
            "Airwalk",
            "Shimmy",
            "Path of Least Resistance",
            "Daedalus",
            "Ordeal",
            "Battlements",
            "Pinball Wizard",
            "Eye of the Storm",
            "Dive!",
            "Tightrope",
            "Natural Selection",
            "Tango",
            "Icarus",
            "Under Construction",
            "Pathways",
            "Darwin's Dilemma",
            "King of the Mountain",
        ]

    @staticmethod
    def levels_ultra_beginner() -> List[str]:
        return [
            "Learning to Roll",
            "Moving Up",
            "Gem Collection",
            "Frictional Concerns",
            "Triple Gravity",
            "Bridge Crossing",
            "Bunny Slope",
            "Hazardous Climb",
            "First Flight",
            "Marble Melee Primer",
            "Pitfalls",
            "Gravity Helix",
            "Platform Party",
            "Early Frost",
            "Winding Road",
            "Skate Park",
            "Ramp Matrix",
            "Half-Pipe",
            "Jump Jump Jump!",
            "Upward Spiral",
        ]

    @staticmethod
    def levels_ultra_intermediate() -> List[str]:
        return [
            "Mountaintop Retreat",
            "Urban Jungle",
            "Gauntlet",
            "Around the World",
            "Skyscraper",
            "Timely Ascent",
            "Duality",
            "Sledding",
            "The Road Less Travaled",
            "Aim High",
            "Points of the Compass",
            "Obstacle Course",
            "Fork in the Road",
            "Great Divide",
            "Black Diamond",
            "Skate to the Top",
            "Spelunking",
            "Whirl",
            "Hop Skip and a Jump",
            "Tree House",
        ]

    @staticmethod
    def levels_ultra_advanced() -> List[str]:
        return [
            "Divergence",
            "Slick Slide",
            "Ordeal",
            "Daedalus",
            "Survival of the Fittest",
            "Ramps Reloaded",
            "Cube Root",
            "Scaffold",
            "Acrobat",
            "Endurance",
            "Battlements",
            "Three-Fold Maze",
            "Half Pipe Elite",
            "Will o' Wisp",
            "Under Construction",
            "Extreme Skiing",
            "Three-Fold Race",
            "King of the Mountain",
            "Natural Selection",
            "Schadenfreude",
            "Hypercube",
        ]

    @staticmethod
    def levels_platinum_beginner() -> List[str]:
        return [
            "Let's Roll!",
            "Jump Tutorial",
            "Gem Round-Up",
            "Learn the Friction!",
            "Training Towers",
            "Gravity Knot",
            "Flight of the Marble",
            "Teleport Training",
            "Busy Bee...",
            "Learn the Bouncy Floor!",
            "Bump Your Head!",
            "Learn the Wall-Hit",
            "Learn the Time Travel",
            "Learn the Random Force",
            "King of the Marble",
            "Magnet Training",
            "Ground Zero",
            "Recoil Training",
            "Mini Mountain",
            "Ramps",
            "Diagonal Training",
            "Learn the Edge Hit",
            "Hazard Loop",
            "Keep on Rollin'",
            "Battlecube",
        ]

    @staticmethod
    def levels_platinum_intermediate() -> List[str]:
        return [
            "Triple Decker",
            "Mountaintop Retreat",
            "Tornado Launch",
            "Medieval Maze",
            "Ramp Madness",
            "Marble Mini Golf",
            "Marble Mini Golf: Icichole",
            "Basic Agility Course",
            "Avoiding Hazards",
            "Technoropes",
            "Take a Stroll...",
            "Roll Like the Wind!",
            "Sprint",
            "Downhill Racing",
            "Double LoopLoop",
            "Powerup Practice",
            "Loop Exits",
            "Wall Master",
            "Spin Practice",
            "Byzantine Helix",
            "Convoluted Helix",
            "Astroflight",
            "Winding Steps",
            "Floor Climb",
            "Bumpy Highway",
            "Perplexingness",
            "Timely Ascent",
            "Marble Agility Course",
            "Puzzle Ordeal",
            "Dragged Up!",
            "Gym",
            "Skill Zone",
            "Divergence",
            "Daedal Helix",
            "Battlecube Revisited",
        ]

    @staticmethod
    def levels_platinum_advanced() -> List[str]:
        return [
            "Pink-Fold Maze",
            "Gem Seeking Fun!",
            "Gap Aimer",
            "Orange-Fold Maze",
            "Nukesweeper",
            "Treachery",
            "Swivel",
            "Nuke Field",
            "Platform Race",
            "Fighting Slopes",
            "Slippery Steps",
            "Slope Madness",
            "Lighting Ice",
            "Crash Course",
            "NeonTech",
            "Beach Party",
            "Slip Up",
            "Perilous Road",
            "Ring Stunts",
            "Par Pit",
            "Platform Race 2",
            "Quaked Path",
            "Frictional Ascent",
            "Ice Cold Pass",
            "Micheal's Adventure: MBP!",
            "Treacherous Path",
            "Combo Course",
            "Ultimate Tree",
            "Strategy Climb",
            "Despair",
            "Morph",
            "Thief",
            "Rolling to Eternity",
            "Random Mayhem",
            "Frictional Battlecube",
        ]

    @staticmethod
    def levels_platinum_expert() -> List[str]:
        return [
            "Stamina",
            "Tunnel Vision",
            "Micheal's Final Advanture!",
            "Trigonometry",
            "Nukesweeper Revisited",
            "Dizzying Heights",
            "Gyrocopter Monster Course",
            "Recoil Ultra Course",
            "Bouncing Fun",
            "Speed Attack",
            "The Time Travel Race",
            "Sand Storm",
            "Platform Mayhem",
            "Uphill Racing",
            "Cardcaddy's Gem Collection",
            "Don't Jump!",
            "Trapdoor Mania",
            "Arch Acropolis",
            "Slowropes",
            "Catwalks",
            "The Ultimate Friction Challenge!",
            "The Tale of the Tall Skyscraper",
            "Mastering the Marble",
            "Space Station",
            "Battlecube Finale",
        ]

    @staticmethod
    def levels_platinumquest_tutorial() -> List[str]:
        return [
            "Training Wheels",
            "Haphazard",
            "Feeling Frictional",
            "Gems",
            "Fundamentals of Physics",
            "Downhill Skipping",
            "Locomotion",
            "Hunting Around",
            "Sky High Circuit",
            "Rush Hour",
        ]

    @staticmethod
    def levels_platinumquest_beginner() -> List[str]:
        return [
            "Into the Deep",
            "Trained to Fade",
            "El Titiritero",
            "Unseasonably Cold",
            "Having a Blast",
            "Side-Stroller",
            "Transporter Lock",
            "High Rise, Quick Fall",
            "Railgun",
            "Gems Ahoy!",
            "Verticality",
            "Maximo Center",
            "Advanced Techniques",
            "Half Pipe Leap of Faith",
            "Downhill and Out of Here!!",
            "Hip Pop Step Jump",
        ]

    @staticmethod
    def levels_platinumquest_beginner_locked() -> List[str]:
        return [
            "Racing Spirits",
            "Bubble Cavern",
            "Trial by Fire",
            "Net Force",
            "From Under the Dragon's Wing",
        ]

    @staticmethod
    def levels_platinumquest_intermediate() -> List[str]:
        return [
            "Gravity Tower",
            "Blender: Liquify",
            "Exoplanet",
            "Rickety Race",
            "Triple Action",
            "Triple Trail",
            "Path Finding Folly",
            "Quest Ring",
            "Outlook",
            "Castle Colossus",
            "Skate Park Square",
            "King of the Island",
            "Marbleland",
            "Deep Space Morphway",
            "Terrace Tundra",
            "Centripetal Force",
            "Assembly Line",
        ]

    @staticmethod
    def levels_platinumquest_intermediate_locked() -> List[str]:
        return [
            "Construction Wonders",
            "Level from a Forgiving Mind",
            "Blender: Chop",
            "Freezing Point",
            "Evaporation",
            "Race to the Top",
            "Diminishing Returns",
            "Climb and Plummet",
            "Glacier Meadow",
            "Above and Below",
        ]

    @staticmethod
    def levels_platinumquest_advanced() -> List[str]:
        return [
            "Work in Progress",
            "Be Elusive!",
            "Vibrancy Grounds",
            "Momentum",
            "The Spoils of Serendipity Gardens",
            "Lupus",
        ]

    @staticmethod
    def levels_platinumquest_advanced_locked() -> List[str]:
        return [
            "Terminal Velocity",
            "Gem Finding Folly",
            "Tricks in the Air",
            "Fly the Coop",
            "Shelosh",
            "Dangerous Development",
            "Chilled",
            "Wonky Waters",
            "Child's Play",
            "Nadir",
            "Messing with Physics",
            "Citadel",
            "Lost Islands",
            "Newton's Dilemma",
            "Scouring the Framework",
            "Waves in the Dark",
            "Fire when Ready",
            "Bag of Secrets...",
            "Cannon Sniper",
            "Vice",
        ]

    @staticmethod
    def levels_platinumquest_expert_locked() -> List[str]:
        return [
            "Physical Activity",
            "Dependency",
            "Frozen Flames",
            "Hawking's Dilemma",
            "A Bridge Too Hard",
            "Gems of the Deep Blue",
            "Orthogonality",
            "Fault Line",
            "Polymorphism",
            "Fist Bump",
            "Platinum Construction Co.",
            "Blast to the Beat",
            "A Marble's Home is Its Castle",
            "Contractor",
            "Conservation of Momentum",
            "Hydropower",
            "Chasetrack",
            "Musing",
            "Emergency Stopping Only",
            "Miscalculations",
            "Manic Bounce",
        ]

    @staticmethod
    def levels_hunt_beginner() -> List[str]:
        return [
            "King of the Marble",
            "Hunting Around",
            "Triple Decker",
            "Playground",
            "Sprawl",
            "Cube Isle",
            "Gems Ahoy!",
            "Blast Club",
            "Maximo Center",
            "Bowl",
            "Marble Agility Course",
            "Marble City",
            "Gravity Tower",
            "Battlecube",
            "Triumvirate",
            "Apex",
        ]

    @staticmethod
    def levels_hunt_intermediate() -> List[str]:
        return [
            "Basic Agility Course",
            "All Angles",
            "Exoplanet",
            "Ziggurat",
            "Gem Finding Folly",
            "Marble It Up!",
            "Marbleland",
            "Gems in the Road",
            "Outlook",
            "Epicenter",
            "Triple Trail",
            "Skate Battle Royale",
            "Tilo",
            "Sweep",
            "Terrace Tundra",
            "Vortex Effect",
            "Battlecube Revisited",
            "Core",
            "Ramps Revamped",
        ]

    @staticmethod
    def levels_hunt_advanced() -> List[str]:
        return [
            "Skate Park Square",
            "Lupus",
            "Horizon",
            "Wonky Waters",
            "Platinum Construction Co.",
            "Par Pit",
            "Concentric",
            "Architecture",
            "Vibrancy Grounds",
            "Eye of the Storm",
            "Sacred",
            "Citadel",
            "Promontory",
            "Nadir",
            "Zenith",
            "Megas",
            "Pyramid",
            "Parkour Peaks",
            "Spires",
        ]

    @staticmethod
    def levels_hunt_snow_beginner() -> List[str]:
        return [
            "King of the Marble",
            "Playground",
            "Sprawl",
            "Hunting Around",
            "Gems Ahoy!",
            "Blast Club",
            "Bowl",
            "Marble City",
            "Battlecube",
            "Triumvirate",
            "Maximo Center",
            "Snow Brawl",
        ]

    @staticmethod
    def levels_hunt_snow_intermediate() -> List[str]:
        return [
            "Basic Agility Course",
            "All Angles",
            "Ziggurat",
            "Gems in the Road",
            "Marble It Up!",
            "Gem Finding Folly",
            "Epicenter",
            "Skate Battle Royale",
            "Vortex Effect",
            "Battlecube Revisited",
            "Core",
            "Marbleland",
            "Terrace Tundra",
        ]

    @staticmethod
    def levels_hunt_snow_advanced() -> List[str]:
        return [
            "Horizon",
            "Par Pit",
            "Concentric",
            "Architecture",
            "Promontory",
            "Zenith",
            "Spires",
            "Lupus",
            "Nadir",
            "Wintry Village",
            "Concavity Duex",
            "Winter's Rage",
            "Skate Park Square",
        ]

    @staticmethod
    def levels_hunt_fright_beginner() -> List[str]:
        return [
            "Covert Cryptball",
            "King of the Ghosts",
            "Ghastly Graveyard",
            "Creepy Grounds",
            "Uncovered Crypt",
            "Pumpkin City",
            "Ghosts Ahoy!",
        ]

    @staticmethod
    def levels_hunt_fright_intermediate() -> List[str]:
        return [
            "Precarious Patch",
            "Fallen Angels",
            "Sinister Stronghold",
            "Spookicenter",
            "Spookyland",
            "Frightful Roads",
            "Melancholia Morass",
        ]

    @staticmethod
    def levels_hunt_fright_advanced() -> List[str]:
        return [
            "Vacuous Village",
            "BLOODY BATTLE SEWERS",
            "Abandonded Warehouse",
            "Necropolis",
            "Lake Pungent",
            "Bat Megalopolis",
        ]


# Archipelago Options
class PlatinumQuestLevelPacks(OptionSet):
    """
    Indicates which PlatinumQuest level packs the player wants to include when generating objectives.
    """

    display_name = "PlatinumQuest Level Packs"
    valid_keys = [
        "Gold",
        "Ultra",
        "Platinum",
        "PlatinumQuest",
        "PlatinumQuest Locked",
        "Hunt",
        "Hunt Snow",
        "Hunt Fright",
    ]

    default = valid_keys


class PlatinumQuestDifficulties(OptionSet):
    """
    Indicates which PlatinumQuest difficulties the player wants to include when generating objectives.
    """

    display_name = "PlatinumQuest Difficulties"
    valid_keys = [
        "Tutorial",
        "Beginner",
        "Intermediate",
        "Advanced",
        "Expert",
    ]

    default = valid_keys
