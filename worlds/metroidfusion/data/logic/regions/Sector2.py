from ..FusionRegion import FusionRegion


class Sector2Hub(FusionRegion):
    name = "Sector 2 Hub"

class Sector2TubeLeft(FusionRegion):
    name = "Sector 2 Tube Left"

class Sector2TubeRight(FusionRegion):
    name = "Sector 2 Tube Right"

class Sector2LeftSide(FusionRegion):
    name = "Sector 2 Left Side"

class Sector2ZazabiZone(FusionRegion):
    name = "Sector 2 Zazabi Zone"

class Sector2ZazabiZoneUpper(FusionRegion):
    name = "Sector 2 Zazabi Zone Upper"

class Sector2NettoriZone(FusionRegion):
    name = "Sector 2 Nettori Zone"

sector_2_regions = [
    Sector2Hub,
    Sector2TubeLeft,
    Sector2TubeRight,
    Sector2LeftSide,
    Sector2ZazabiZone,
    Sector2ZazabiZoneUpper,
    Sector2NettoriZone
]
