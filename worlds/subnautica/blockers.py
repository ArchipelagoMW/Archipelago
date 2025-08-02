from typing import Dict, TypedDict, List

class Vector(TypedDict):
    x: float
    y: float
    z: float

class ProgressBlocker(TypedDict, total=False):
    position: Vector
    rotation: Vector
    region: str

blocker_list = (
    # upper Aurora blockers to spawn on strict propulsion cannon logic
    {'position': {'x': 994.85, 'y': 29.54, 'z': 66.1},
     'rotation': {'x': 5.0, 'y': 78.714, 'z': 0.0},
     'region': 'AuroraUpper'},
    {'position': {'x': 994.95, 'y': 30.66, 'z': 66.1},
     'rotation': {'x': 5.0, 'y': 78.714, 'z': 0.0},
     'region': 'AuroraUpper'},
    {'position': {'x': 995.05, 'y': 31.78, 'z': 66.1},
     'rotation': {'x': 5.0, 'y': 78.714, 'z': 0.0},
     'region': 'AuroraUpper'},
    {'position': {'x': 995.45, 'y': 29.88, 'z': 63.9},
     'rotation': {'x': 0.0, 'y': 1.0, 'z': 266.0},
     'region': 'AuroraUpper'},
    {'position': {'x': 988.35, 'y': 32.92, 'z': 71.5},
     'rotation': {'x': 358.0, 'y': 30.714, 'z': 343.0},
     'region': 'AuroraUpper'},
    {'position': {'x': 988.89, 'y': 33.09, 'z': 72.51},
     'rotation': {'x': 30.0, 'y': 17.714, 'z': 335.0},
     'region': 'AuroraUpper'},
)
