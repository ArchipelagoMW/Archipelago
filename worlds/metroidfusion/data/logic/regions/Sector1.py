from ..FusionRegion import FusionRegion


class Sector1Hub(FusionRegion):
    name = "Sector 1 Hub"

class Sector1TubeRight(FusionRegion):
    name = "Sector 1 Tube Right"

class Sector1TubeLeft(FusionRegion):
    name = "Sector 1 Tube Left"

class Sector1Antechamber(FusionRegion):
    name = "Sector 1 Antechamber"

class Sector1FirstStabilizerZone(FusionRegion):
    name = "Sector 1 First Stabilizer Zone"

class Sector1SecondStabilizerZone(FusionRegion):
    name = "Sector 1 Second Stabilizer Zone"

class Sector1ThirdStabilizerZone(FusionRegion):
    name = "Sector 1 Third Stabilizer Zone"

class Sector1ChargeCoreZone(FusionRegion):
    name = "Sector 1 Charge Core Zone"

class Sector1AfterChargeCoreZone(FusionRegion):
    name = "Sector 1 After Charge Core Zone"

class Sector1TourianExit(FusionRegion):
    name = "Sector 1 Tourian Exit"

class Sector1TourianHub(FusionRegion):
    name = "Sector 1 Tourian Hub"

class Sector1TourianHubElevatorTop(FusionRegion):
    name = "Sector 1 Tourian Hub Elevator Top"

sector_1_regions = [
    Sector1Hub,
    Sector1TubeLeft,
    Sector1TubeRight,
    Sector1Antechamber,
    Sector1FirstStabilizerZone,
    Sector1SecondStabilizerZone,
    Sector1ThirdStabilizerZone,
    Sector1ChargeCoreZone,
    Sector1AfterChargeCoreZone,
    Sector1TourianExit,
    Sector1TourianHub,
    Sector1TourianHubElevatorTop
]
