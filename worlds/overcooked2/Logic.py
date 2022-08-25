from BaseClasses import MultiWorld, ItemClassification, CollectionState, Region, Entrance, Location, RegionType
from .Overcooked2Levels import Overcooked2Level, Overcooked2World, Overcooked2GenericLevel

def has_requirements_for_level_star(state: CollectionState, level: Overcooked2GenericLevel, stars: int) -> bool:
    assert stars >= 0 and stars <= 3

    # First ensure that previous stars are obtainable
    if stars > 1:
        if not has_requirements_for_level_star(state, level, stars-1):
            return False
    
    # Then, assess completableness
    return True
