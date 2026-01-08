from ..FusionRegion import FusionRegion


class MainDeckHub(FusionRegion):
    name = "Main Deck Hub"

class LowerArachnusArena(FusionRegion):
    name = "Lower Arachnus Arena"

class VentilationZone(FusionRegion):
    name = "Ventilation Zone"

class UpperArachnusArena(FusionRegion):
    name = "Upper Arachnus Arena"

class OperationsDeckElevatorBottom(FusionRegion):
    name = "Operations Deck Elevator Bottom"

class OperationsDeck(FusionRegion):
    name = "Operations Deck"

class OperationsDeckElevatorTop(FusionRegion):
    name = "Operations Deck Elevator Top"

class HabitationDeckElevatorBottom(FusionRegion):
    name = "Habitation Deck Elevator Bottom"

class HabitationDeckElevatorTop(FusionRegion):
    name = "Habitation Deck Elevator Top"

class HabitationDeck(FusionRegion):
    name = "Habitation Deck"

class SectorHubElevatorTop(FusionRegion):
    name = "Sector Hub Elevator Top"

class SectorHubElevatorBottom(FusionRegion):
    name = "Sector Hub Elevator Bottom"

class SectorHubElevator1Top(FusionRegion):
    name = "Sector Hub Elevator 1 Top"

class SectorHubElevator2Top(FusionRegion):
    name = "Sector Hub Elevator 2 Top"

class SectorHubElevator3Top(FusionRegion):
    name = "Sector Hub Elevator 3 Top"

class SectorHubElevator4Top(FusionRegion):
    name = "Sector Hub Elevator 4 Top"

class SectorHubElevator5Top(FusionRegion):
    name = "Sector Hub Elevator 5 Top"

class SectorHubElevator6Top(FusionRegion):
    name = "Sector Hub Elevator 6 Top"

class ReactorZone(FusionRegion):
    name = "Reactor Zone"

class YakuzaZone(FusionRegion):
    name = "Yakuza Zone"

class AuxiliaryReactor(FusionRegion):
    name = "Auxiliary Reactor"

class NexusStorage(FusionRegion):
    name = "Nexus Storage"

main_deck_regions = [
    MainDeckHub,
    VentilationZone,
    UpperArachnusArena,
    LowerArachnusArena,
    OperationsDeckElevatorBottom,
    OperationsDeckElevatorTop,
    OperationsDeck,
    HabitationDeckElevatorBottom,
    HabitationDeckElevatorTop,
    HabitationDeck,
    SectorHubElevatorTop,
    SectorHubElevatorBottom,
    SectorHubElevator1Top,
    SectorHubElevator2Top,
    SectorHubElevator3Top,
    SectorHubElevator4Top,
    SectorHubElevator5Top,
    SectorHubElevator6Top,
    ReactorZone,
    YakuzaZone,
    AuxiliaryReactor,
    NexusStorage
]
