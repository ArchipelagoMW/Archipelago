from ..FusionRegion import FusionRegion


class Sector6Hub(FusionRegion):
    name = "Sector 6 Hub"

class Sector6TubeLeft(FusionRegion):
    name = "Sector 6 Tube Left"

class Sector6TubeRight(FusionRegion):
    name = "Sector 6 Tube Right"

class Sector6Crossroads(FusionRegion):
    name = "Sector 6 Crossroads"

class Sector6BeforeXBOXZone(FusionRegion):
    name = "Sector 6 Before X-BOX Zone"

class Sector6XBOXZone(FusionRegion):
    name = "Sector 6 X-BOX Zone"

class Sector6AfterXBOXZone(FusionRegion):
    name = "Sector 6 After X-BOX Zone"

class Sector6RestrictedZone(FusionRegion):
    name = "Sector 6 Restricted Zone"

class Sector6RestrictedZoneElevatorToTourian(FusionRegion):
    name = "Sector 6 Restricted Zone Elevator To Tourian Bottom"

class Sector6BeforeVariaCoreXZone(FusionRegion):
    name = "Sector 6 Before Varia Core-X Zone"

class Sector6VariaCoreXZone(FusionRegion):
    name = "Sector 6 Varia Core-X Zone"

class Sector6AfterVariaCoreXZone(FusionRegion):
    name = "Sector 6 After Varia Core-X Zone"

sector_6_regions = [
    Sector6Hub,
    Sector6TubeLeft,
    Sector6TubeRight,
    Sector6Crossroads,
    Sector6BeforeXBOXZone,
    Sector6XBOXZone,
    Sector6AfterXBOXZone,
    Sector6RestrictedZone,
    Sector6RestrictedZoneElevatorToTourian,
    Sector6BeforeVariaCoreXZone,
    Sector6VariaCoreXZone,
    Sector6AfterVariaCoreXZone
]
