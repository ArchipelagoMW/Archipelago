from .regions.MainDeck import (SectorHubElevatorTop, OperationsDeckElevatorTop, HabitationDeckElevatorTop,
                               SectorHubElevator1Top, SectorHubElevator2Top, SectorHubElevator3Top,
                               SectorHubElevator4Top, SectorHubElevator5Top, SectorHubElevator6Top,
                               OperationsDeckElevatorBottom, HabitationDeckElevatorBottom, SectorHubElevatorBottom)
from .regions.Sector1 import Sector1Hub, Sector1TubeLeft, Sector1TubeRight, Sector1TourianHubElevatorTop
from .regions.Sector2 import Sector2Hub, Sector2TubeLeft, Sector2TubeRight
from .regions.Sector3 import Sector3Hub, Sector3TubeLeft, Sector3TubeRight
from .regions.Sector4 import Sector4Hub, Sector4TubeLeft, Sector4TubeRight
from .regions.Sector5 import Sector5Hub, Sector5TubeLeft, Sector5TubeRight
from .regions.Sector6 import Sector6Hub, Sector6TubeLeft, Sector6TubeRight, Sector6RestrictedZoneElevatorToTourian

default_region_map = {
    Sector1TubeLeft: Sector3TubeRight,
    Sector2TubeLeft: Sector1TubeRight,
    Sector3TubeLeft: Sector5TubeRight,
    Sector4TubeLeft: Sector2TubeRight,
    Sector5TubeLeft: Sector6TubeRight,
    Sector6TubeLeft: Sector4TubeRight,
    SectorHubElevator1Top: Sector1Hub,
    SectorHubElevator2Top: Sector2Hub,
    SectorHubElevator3Top: Sector3Hub,
    SectorHubElevator4Top: Sector4Hub,
    SectorHubElevator5Top: Sector5Hub,
    SectorHubElevator6Top: Sector6Hub,
    OperationsDeckElevatorTop: OperationsDeckElevatorBottom,
    HabitationDeckElevatorTop: HabitationDeckElevatorBottom,
    SectorHubElevatorTop: SectorHubElevatorBottom,
    Sector1TourianHubElevatorTop: Sector6RestrictedZoneElevatorToTourian
}

reverse_region_map = {v: k for k, v in default_region_map.items()}

full_default_region_map = {
    **default_region_map,
    **reverse_region_map
}