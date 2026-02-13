from .logic.FusionRegion import FusionRegion
from .logic.regions.MainDeck import main_deck_regions, SectorHubElevator1Top, SectorHubElevator2Top, \
    SectorHubElevator3Top, SectorHubElevator4Top, SectorHubElevator5Top, SectorHubElevator6Top, \
    OperationsDeckElevatorTop, HabitationDeckElevatorTop, SectorHubElevatorTop, OperationsDeckElevatorBottom, \
    HabitationDeckElevatorBottom, SectorHubElevatorBottom
from .logic.regions.Sector1 import sector_1_regions, Sector1TubeLeft, Sector1TubeRight, Sector1Hub, \
    Sector1TourianHubElevatorTop
from .logic.regions.Sector2 import sector_2_regions, Sector2TubeLeft, Sector2TubeRight, Sector2Hub
from .logic.regions.Sector3 import sector_3_regions, Sector3TubeLeft, Sector3TubeRight, Sector3Hub
from .logic.regions.Sector4 import sector_4_regions, Sector4TubeLeft, Sector4TubeRight, Sector4Hub
from .logic.regions.Sector5 import sector_5_regions, Sector5TubeLeft, Sector5TubeRight, Sector5Hub
from .logic.regions.Sector6 import sector_6_regions, Sector6TubeLeft, Sector6TubeRight, Sector6Hub, \
    Sector6RestrictedZoneElevatorToTourian

fusion_regions: list[FusionRegion] = [
    *main_deck_regions,
    *sector_1_regions,
    *sector_2_regions,
    *sector_3_regions,
    *sector_4_regions,
    *sector_5_regions,
    *sector_6_regions
]

# These are the default connection order. Don't mess with it.
left_tubes = [
    Sector1TubeLeft,
    Sector2TubeLeft,
    Sector3TubeLeft,
    Sector4TubeLeft,
    Sector5TubeLeft,
    Sector6TubeLeft
]

# These are the default connection order. Don't mess with it.
right_tubes = [
    Sector3TubeRight,
    Sector1TubeRight,
    Sector5TubeRight,
    Sector2TubeRight,
    Sector6TubeRight,
    Sector4TubeRight
]

# These are the default connection order. Don't mess with it.
sector_elevator_tops = [
    SectorHubElevator1Top,
    SectorHubElevator2Top,
    SectorHubElevator3Top,
    SectorHubElevator4Top,
    SectorHubElevator5Top,
    SectorHubElevator6Top
]

# These are the default connection order. Don't mess with it.
sector_elevator_bottoms = [
    Sector1Hub,
    Sector2Hub,
    Sector3Hub,
    Sector4Hub,
    Sector5Hub,
    Sector6Hub
]

sector_elevators = [
    *sector_elevator_tops,
    *sector_elevator_bottoms
]

# These are the default connection order. Don't mess with it.
other_elevator_tops = [
    OperationsDeckElevatorTop,
    HabitationDeckElevatorTop,
    SectorHubElevatorTop,
    Sector1TourianHubElevatorTop,
]

# These are the default connection order. Don't mess with it.
other_elevator_bottoms = [
    OperationsDeckElevatorBottom,
    HabitationDeckElevatorBottom,
    SectorHubElevatorBottom,
    Sector6RestrictedZoneElevatorToTourian,
]

other_elevators = [
    *other_elevator_tops,
    *other_elevator_bottoms
]

sector_tube_id_lookups = {
    Sector1TubeLeft.name: 1,
    Sector1TubeRight.name: 1,
    Sector2TubeLeft.name: 2,
    Sector2TubeRight.name: 2,
    Sector3TubeLeft.name: 3,
    Sector3TubeRight.name: 3,
    Sector4TubeLeft.name: 4,
    Sector4TubeRight.name: 4,
    Sector5TubeLeft.name: 5,
    Sector5TubeRight.name: 5,
    Sector6TubeLeft.name: 6,
    Sector6TubeRight.name: 6
}

elevator_id_lookups = {
    OperationsDeckElevatorTop.name: "OperationsDeckTop",
    SectorHubElevator1Top.name: "MainHubToSector1",
    SectorHubElevator2Top.name: "MainHubToSector2",
    SectorHubElevator3Top.name: "MainHubToSector3",
    SectorHubElevator4Top.name: "MainHubToSector4",
    SectorHubElevator5Top.name: "MainHubToSector5",
    SectorHubElevator6Top.name: "MainHubToSector6",
    SectorHubElevatorTop.name: "MainHubTop",
    HabitationDeckElevatorTop.name: "HabitationDeckTop",
    Sector1TourianHubElevatorTop.name: "Sector1ToRestrictedLab",
    OperationsDeckElevatorBottom.name: "OperationsDeckBottom",
    SectorHubElevatorBottom.name: "MainHubBottom",
    Sector6RestrictedZoneElevatorToTourian.name: "RestrictedLabToSector1",
    HabitationDeckElevatorBottom.name: "HabitationDeckBottom",
    Sector1Hub.name: "Sector1ToMainHub",
    Sector2Hub.name: "Sector2ToMainHub",
    Sector3Hub.name: "Sector3ToMainHub",
    Sector4Hub.name: "Sector4ToMainHub",
    Sector5Hub.name: "Sector5ToMainHub",
    Sector6Hub.name: "Sector6ToMainHub"
}
