"""Contains classes used in the MN64 logic system."""

from __future__ import annotations

from enum import Enum
from typing import Callable, List, Optional, Union

from .mn64_logic_holder import MN64LogicHolder


class MN64Levels(Enum):
    """Levels in MN64."""

    OEDO_TOWN = "Oedo Town"
    MUSASHI = "Musashi"
    MUTSU = "Mutsu"
    YAMATO = "Yamato"
    SANUKI = "Sanuki"
    FOLKYPOKE_VILLAGE = "Folkypoke Village"
    TOSA = "Tosa"
    IYO = "Iyo"
    GHOST_TOYS_CASTLE = "Ghost Toys Castle"
    OEDO_CASTLE = "Oedo Castle"
    KAI = "Kai"
    BIZEN = "Bizen"
    FESTIVAL_TEMPLE_CASTLE = "Festival Temple Castle"
    GORGEOUS_MUSIC_CASTLE = "Gorgeous Music Castle"


class MN64HintRegion(Enum):
    """Hint regions for MN64."""

    OEDO_TOWN = "Oedo Town"
    MUSASHI = "Musashi"
    MUTSU = "Mutsu"
    YAMATO = "Yamato"
    SANUKI = "Sanuki"
    FOLKYPOKE_VILLAGE = "Folkypoke Village"
    TOSA = "Tosa"
    IYO = "Iyo"
    GHOST_TOYS_CASTLE = "Ghost Toys Castle"
    OEDO_CASTLE = "Oedo Castle"
    KAI = "Kai"
    BIZEN = "Bizen"
    FESTIVAL_TEMPLE_CASTLE = "Festival Temple Castle"
    GORGEOUS_MUSIC_CASTLE = "Gorgeous Music Castle"


class MN64DoorType(Enum):
    """Types of doors in MN64."""

    PORTAL = "Portal"
    DOOR = "Door"
    SPECIAL = "Special"


class MN64Items(Enum):
    """Items in MN64."""  # Keys

    SILVER_KEY = "Silver Key"
    GOLD_KEY = "Gold Key"
    DIAMOND_KEY = "Diamond Key"
    JUMP_GYM_KEY = "Jump Gym Key"

    # Equipment and Tools
    WINDUP_CAMERA = "Wind up Camera"
    CHAIN_PIPE = "Chain Pipe"
    ICE_KUNAI = "Ice Kunai"
    MEDAL_OF_FLAMES = "Medal of Flames"
    BAZOOKA = "Bazooka"
    MEAT_HAMMER = "Meat Hammer"
    FLUTE = "Flute"

    # Characters and Abilities
    MERMAID = "Mermaid"
    MINI_EBISUMARU = "Mini Ebisumaru"
    SUDDEN_IMPACT = "Sudden Impact"
    JETPACK = "Jetpack"

    # Characters
    GOEMON = "Goemon"
    YAE = "Yae"
    EBISUMARU = "Ebisumaru"
    SASUKE = "Sasuke"

    # Character Items
    SASUKE_DEAD = "Sasuke Dead"
    SASUKE_BATTERY_1 = "Sasuke Battery 1"
    SASUKE_BATTERY_2 = "Sasuke Battery 2"

    # Fortune Dolls
    SILVER_FORTUNE_DOLL = "Silver Fortune Doll"
    GOLD_FORTUNE_DOLL = "Gold Fortune Doll"

    # Health Items
    GOLDEN_HEALTH = "Golden Health"
    NORMAL_HEALTH = "Normal Health"  # Transportation and Special Items
    SUPER_PASS = "Super Pass"
    TRITON_HORN = "Triton Horn"
    CUCUMBER = "Cucumber"

    # # Fish Items
    # RED_FISH = "Red Fish"
    # YELLOW_FISH = "Yellow Fish"
    # BLUE_FISH = "Blue Fish"

    # Upgrades and Power-ups
    PROGRESSIVE_STRENGTH = "Progressive Strength"
    SURPRISE_PACK = "Surprise Pack"

    # Filler Items
    RYO = "Ryo"
    POT = "Pot of Ryo"

    # Special Items and NPCs
    MR_ELLY_FANT_OEDO_CASTLE = "Mr Elly Fant (Oedo Castle)"
    MR_ELLY_FANT_GHOST_TOYS_CASTLE = "Mr Elly Fant (Ghost Toys Castle)"
    MR_ELLY_FANT_FESTIVAL_TEMPLE = "Mr Elly Fant (Festival Temple)"
    MR_ELLY_FANT_GOURMET_SUBMARINE = "Mr Elly Fant (Gourmet Submarine)"
    MR_ELLY_FANT_GORGEOUS_MUSIC_CASTLE = "Mr Elly Fant (Gorgeous Music Castle)"
    MR_ARROW_OEDO_CASTLE = "Mr Arrow (Oedo Castle)"
    MR_ARROW_GHOST_TOYS_CASTLE = "Mr Arrow (Ghost Toys Castle)"
    MR_ARROW_FESTIVAL_TEMPLE = "Mr Arrow (Festival Temple)"
    MR_ARROW_GORGEOUS_MUSIC_CASTLE = "Mr Arrow (Gorgeous Music Castle)"
    MR_ARROW_GOURMET_SUBMARINE = "Mr Arrow (Gourmet Submarine)"
    ACHILLES_HEEL = "Achilles Heel"  # Special Flags and Events
    CRANE_GAME_POWER_ON = "Crane Game Power On"
    VISITED_WITCH = "Visited Witch"
    VISITED_GHOST_TOYS_ENTRANCE = "Visited Ghost Toys Entrance"
    KUYSHU_FLY = "Kyushu Fly"
    MOKUBEI_BROTHER = "Mokubei Brother"

    # Boss and Quest Items
    beat_tsurami = "Beat Tsurami"
    BEAT_THAISAMBDA = "Beat Thaisambda"
    BEAT_DHARUMANYO = "Beat Dharumanyo"
    BEAT_CONGO = "Beat Congo"
    BEAT_GAME_DIE_HARD_FANS = "Beat Game Die Hard Fans"
    MIRACLE_STAR = "Miracle Star"
    MIRACLE_SNOW = "Miracle Snow"
    MIRACLE_MOON = "Miracle Moon"
    MIRACLE_FLOWER = "Miracle Flower"

    # Training and Challenges
    JUMP_CHALLENGE_TRAINING = "Jump Challenge Training"
    CUCUMBER_QUEST_START = "Cucumber Quest Start"
    CUCUMBER_QUEST_PRIEST = "Cucumber Quest Find Priest"
    # FISH_QUEST_START = "Fish Quest Start"
    MOVING_BOULDER_IN_FOREST = "Moving Boulder in Forest"


class MN64LocationLogic:
    """Logic for a location in MN64."""

    def __init__(
        self,
        name: str,
        logic: Callable[[MN64LogicHolder], bool],
        item_type: MN64Items,
        flag_id: Optional[int] = None,
        save_id: Optional[int] = None,
        instance_id: Optional[int] = None,
    ) -> None:
        """Initialize with given parameters."""
        self.name = name
        self.logic = logic  # Lambda function for accessibility
        self.item_type = item_type
        self.flag_id: Optional[int] = flag_id  # To be set when integrated with item system
        self.save_id: Optional[int] = save_id  # To be set when integrated with item system
        self.instance_id: Optional[int] = instance_id  # To be set when integrated with item system


class MN64TransitionFront:
    """The entered side of a transition between regions in MN64."""

    def __init__(
        self,
        destinationRegion: str,
        logic: Callable[[MN64LogicHolder], bool],
        name: Optional[str] = None,
        type: MN64DoorType = MN64DoorType.PORTAL,
        consumes_key: Optional[str] = None,
    ) -> None:
        """Initialize with given parameters."""
        self.destinationRegion = destinationRegion
        self.logic = logic
        self.name = name or f"Exit to {destinationRegion}"
        self.type = type
        self.consumes_key = consumes_key  # Can be "silver", "gold", or "diamond"


class MN64Region:
    """Region contains shufflable locations and transitions to other regions in MN64."""

    def __init__(
        self,
        name: str,
        hint_name: MN64HintRegion,
        level: MN64Levels,
        locations: List[MN64LocationLogic],
        exits: List[MN64TransitionFront],
        npcs: Optional[List[str]] = None,
        room_id: Optional[Union[int, str]] = None,
        room_default_definitions: Optional[List[str]] = None,
        enemies: Optional[Dict[int, int]] = None,
        spawn: Optional[Dict[str, float]] = None,
    ) -> None:
        """Initialize with given parameters."""
        self.name = name
        self.hint_name = hint_name
        self.level = level
        self.locations = locations or []
        self.exits = exits or []
        self.npcs = npcs or []
        self.room_id = room_id
        self.room_default_definitions = room_default_definitions or []
        self.enemies = enemies or {}
        self.spawn = spawn or {}
