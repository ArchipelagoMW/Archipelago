from enum import Enum

from BaseClasses import ItemClassification


class EraType(Enum):
    ERA_ANCIENT = "ERA_ANCIENT"
    ERA_CLASSICAL = "ERA_CLASSICAL"
    ERA_MEDIEVAL = "ERA_MEDIEVAL"
    ERA_RENAISSANCE = "ERA_RENAISSANCE"
    ERA_INDUSTRIAL = "ERA_INDUSTRIAL"
    ERA_MODERN = "ERA_MODERN"
    ERA_ATOMIC = "ERA_ATOMIC"
    ERA_INFORMATION = "ERA_INFORMATION"
    ERA_FUTURE = "ERA_FUTURE"


class CivVICheckType(Enum):
    TECH = "TECH"
    CIVIC = "CIVIC"
    PROGRESSIVE_DISTRICT = "PROGRESSIVE_DISTRICT"
    ERA = "ERA"
    GOODY = "GOODY"
    BOOST = "BOOST"
    EVENT = "EVENT"

class CivVIHintClassification(Enum):
    PROGRESSION = "Progression"
    USEFUL = "Useful"
    FILLER = "Filler"

    def to_item_classification(self) -> ItemClassification:
        if self == CivVIHintClassification.PROGRESSION:
            return ItemClassification.progression
        if self == CivVIHintClassification.USEFUL:
            return ItemClassification.useful
        if self == CivVIHintClassification.FILLER:
            return ItemClassification.filler
        assert False
