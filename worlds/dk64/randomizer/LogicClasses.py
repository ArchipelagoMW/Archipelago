"""Contains classes used in the logic system."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, List, Optional, Tuple, Union

from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Time import Time
from randomizer.Enums.Locations import Locations
from randomizer.Enums.HintRegion import HintRegion, HINT_REGION_PAIRING, MEDAL_REWARD_REGIONS, SHOP_REGIONS
from randomizer.Lists.EnemyTypes import INSTRUMENT_RESTRICTED_REGIONS

if TYPE_CHECKING:
    from randomizer.Enums.Collectibles import Collectibles
    from randomizer.Enums.Events import Events
    from randomizer.Enums.Locations import Locations
    from randomizer.Enums.MinigameType import MinigameType
    from randomizer.Enums.Transitions import Transitions
    from randomizer.Logic import LogicVarHolder


class LocationLogic:
    """Logic for a location."""

    def __init__(
        self,
        id: Union[int, Locations],
        logic: Callable,
        bonusBarrel: Optional[MinigameType] = None,
        isAuxiliary: bool = False,
    ) -> None:
        """Initialize with given parameters."""
        self.id = id
        self.logic = logic  # Lambda function for accessibility
        if id >= Locations.JapesMainEnemy_Start and id <= Locations.IslesMainEnemy_LowerFactoryPath1:

            def create_enemy_logic(location_id):
                def enemy_logic(l):
                    if not logic(l):
                        return False
                    region_id = None
                    for reg_id, region in l.spoiler.RegionList.items():
                        if location_id in [loc.id for loc in region.locations if not loc.isAuxiliaryLocation]:
                            region_id = reg_id
                            break
                    instrument_restricted = region_id in INSTRUMENT_RESTRICTED_REGIONS if region_id is not None else False
                    return l.spoiler.enemy_location_list[location_id].canDropItem(l, instrument_restricted)

                return enemy_logic

            self.logic = create_enemy_logic(id)
        self.bonusBarrel = bonusBarrel  # Uses MinigameType enum
        self.isAuxiliaryLocation = (
            isAuxiliary  # For when the Location needs to be in a region but not count as in the region (used for locations that need to be accessible in different regions depending on settings)
        )


class Event:
    """Event within a region.

    Events act as statically placed items
    For example, if Lanky must press a button in region x to open something in region y,
    that can be represented as a button press event in region x which is checked for in region y.
    """

    def __init__(self, name: Events, logic: Callable) -> None:
        """Initialize with given parameters."""
        self.name = name
        self.logic = logic  # Lambda function for accessibility


class Collectible:
    """Class used for colored bananas and banana coins."""

    def __init__(
        self,
        type: Collectibles,
        kong: Kongs,
        logic: Callable,
        coords: Optional[Tuple[float, float, float]] = None,
        amount: int = 1,
        enabled: bool = True,
        vanilla: bool = True,
        name: str = "vanilla",
        locked: bool = False,
    ) -> None:
        """Initialize with given parameters."""
        self.type = type
        self.kong = kong
        self.logic = logic
        self.amount = amount
        self.coords = coords  # None for vanilla collectibles for now. For custom, use (x,y,z) format
        self.added = False
        self.enabled = enabled
        self.vanilla = vanilla
        self.name = name
        self.locked = locked


class Region:
    """Region contains shufflable locations, events, and transitions to other regions."""

    def __init__(
        self,
        name: str,
        hint_name: HintRegion,
        level: Levels,
        tagbarrel: bool,
        deathwarp: Optional[Union[int, TransitionFront, Regions]],
        locations: List[Union[LocationLogic, Any]],
        events: List[Union[Event, Any]],
        transitionFronts: List[Union[TransitionFront, Any]],
        restart: Optional[Union[Transitions, int]] = None,
    ) -> None:
        """Initialize with given parameters."""
        self.name = name
        self.hint_name = hint_name
        self.level = level
        self.tagbarrel = tagbarrel
        self.deathwarp = None
        self.locations = locations
        self.events = events
        self.exits = transitionFronts  # In the context of a region, exits are how you leave the region
        self.restart = restart

        self.dayAccess = [False] * 5
        self.nightAccess = [False] * 5

        # If possible to die in this region, add an exit to where dying will take you
        # deathwarp is also set to none in regions in which a deathwarp would take you to itself
        # Or if there is loading-zone-less free access to the region it would take you to already
        if deathwarp is not None:
            # If deathwarp is itself an exit class (necessary when deathwarp requires custom logic) just add it directly
            if isinstance(deathwarp, TransitionFront):
                self.deathwarp = deathwarp
            else:
                # If deathwarp is -1, indicates to use the default value for it, which is the starting area of the level
                if deathwarp == -1:
                    deathwarp = self.GetDefaultDeathwarp()
                if deathwarp is not None:
                    if isinstance(deathwarp, Regions):
                        self.deathwarp = TransitionFront(deathwarp, lambda _: True)
                    else:
                        self.deathwarp = TransitionFront(Regions(deathwarp), lambda _: True)

        self.ResetAccess()

    def ResetAccess(self) -> None:
        """Clear access variables set during search."""
        # Time access
        self.dayAccess = [False] * 5
        self.nightAccess = [False] * 5

    def GetDefaultDeathwarp(self) -> Regions:
        """Get the default deathwarp depending on the region's level."""
        if self.level == Levels.DKIsles:
            return Regions.IslesMain
        elif self.level == Levels.JungleJapes:
            return Regions.JungleJapesEntryHandler
        elif self.level == Levels.AngryAztec:
            return Regions.AngryAztecEntryHandler
        elif self.level == Levels.FranticFactory:
            return Regions.FranticFactoryEntryHandler
        elif self.level == Levels.GloomyGalleon:
            return Regions.GloomyGalleonEntryHandler
        elif self.level == Levels.FungiForest:
            return Regions.FungiForestEntryHandler
        elif self.level == Levels.CrystalCaves:
            return Regions.CrystalCavesEntryHandler
        elif self.level == Levels.CreepyCastle:
            return Regions.CreepyCastleEntryHandler
        elif self.level == Levels.HideoutHelm:
            return Regions.HideoutHelmEntry
        return Regions.GameStart

    def getHintRegionName(self) -> str:
        """Convert hint region enum to the name."""
        return HINT_REGION_PAIRING.get(self.hint_name, "Unknown Region")

    def isMedalRegion(self) -> bool:
        """Return whether the associated hint region is a medal reward region."""
        return self.hint_name in MEDAL_REWARD_REGIONS

    def isCBRegion(self) -> bool:
        """Return whether the associated hint region requires CBs to access (Bosses and medal rewards)."""
        return self.hint_name in MEDAL_REWARD_REGIONS or self.hint_name == HintRegion.Bosses

    def isShopRegion(self) -> bool:
        """Return whether the associated hint region is a shop region."""
        return self.hint_name in SHOP_REGIONS


class TransitionBack:
    """The exited side of a transition between regions."""

    def __init__(self, regionId: Regions, exitName: str, spoilerName: str, reverse: Optional[Transitions] = None) -> None:
        """Initialize with given parameters."""
        self.regionId = regionId  # Destination region
        self.name = exitName
        self.spoilerName = spoilerName
        self.reverse = reverse  # Indicates a reverse direction transition, if one exists


class TransitionFront:
    """The entered side of a transition between regions."""

    def __init__(
        self,
        dest: Regions,
        logic: Callable,
        exitShuffleId: Optional[Transitions] = None,
        assumed: bool = False,
        time: Time = Time.Both,
        isGlitchTransition: bool = False,
        isBananaportTransition: bool = False,
    ) -> None:
        """Initialize with given parameters."""
        self.dest = dest
        self.logic = logic  # Lambda function for accessibility
        self.exitShuffleId = exitShuffleId
        self.time = time
        self.assumed = assumed  # Indicates this is an assumed exit attached to the root
        self.isGlitchTransition = isGlitchTransition  # Indicates if this is a glitch-logic transition for this entrance
        self.isBananaportTransition = isBananaportTransition  # Indicates if this transition is due to a Bananaport


class Sphere:
    """A randomizer concept often used in spoiler logs.

    A 'sphere' is a collection of locations and items that are accessible
    or obtainable with only the items available from earlier, smaller spheres.
    Sphere 0 items are what you start with in a seed, sphere 1 items can be
    obtained with those items, sphere 2 items can be obtained with sphere 0
    and sphere 1 items, and so on.
    """

    def __init__(self) -> None:
        """Initialize with given parameters."""
        self.seedBeaten = False
        self.availableGBs = 0
        self.locations: List[Union[LocationLogic, Any]] = []


class ColoredBananaGroup:
    """Stores data for each group of colored bananas."""

    def __init__(
        self,
        *,
        group=0,
        name="No Location",
        map_id=0,
        konglist=[],
        region=None,
        logic=None,
        vanilla=False,
        locations=[],
    ) -> None:
        """Initialize with given parameters."""
        self.group = group
        self.name = name
        self.map = map_id
        self.kongs = konglist
        self.locations = locations  # 5 numbers: {int amount, float scale, int x, y, z}
        self.region = region
        if logic is None:
            self.logic = lambda _: True
        else:
            self.logic = logic
        self.selected = False


class Balloon:
    """Stores data for each balloon."""

    def __init__(
        self,
        *,
        id=0,
        name="No Location",
        map_id=0,
        speed=0,
        konglist=[],
        region=None,
        logic=None,
        vanilla=False,
        points=[],
    ) -> None:
        """Initialize with given parameters."""
        self.id = id
        self.name = name
        self.map = map_id
        self.speed = speed
        self.kongs = konglist
        self.points = points  # 3 numbers: [int x, y, z]
        self.region = region
        if logic is None:
            self.logic = lambda _: True
        else:
            self.logic = logic
        self.spawnPoint = self.setSpawnPoint(points)
        self.selected = False

    def setSpawnPoint(self, points: List[List[int]] = []) -> List[int]:
        """Set the spawn point of a balloon based on its path."""
        spawnX = 0.0
        spawnY = 0.0
        spawnZ = 0.0
        for p in points:
            spawnX += p[0]
            spawnY += p[1]
            spawnZ += p[2]
        spawnX /= len(points)
        spawnY /= len(points)
        spawnY -= 100.0  # Most balloons are at least 100 units off the ground
        spawnZ /= len(points)
        return [int(spawnX), int(spawnY), int(spawnZ)]
