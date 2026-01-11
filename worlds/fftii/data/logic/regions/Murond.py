from ..FFTRegion import FFTRegion


class Murond(FFTRegion):
    name = "Murond"

class Orbonne(FFTRegion):
    name = "Orbonne"

class Goug(FFTRegion):
    name = "Goug"

class DeepDungeon(FFTRegion):
    name = "Deep Dungeon"

class MurondDeathCity(FFTRegion):
    name = "Murond Death City"

murond_regions = [
    Murond, Orbonne, Goug, DeepDungeon, MurondDeathCity
]
