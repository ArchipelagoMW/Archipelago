"""This module contains data classes for position data"""

from dataclasses import dataclass


@dataclass
class RAC3POSITIONDATA:
    """Position data class"""
    X: float
    Y: float
    Z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.X = x
        self.Y = y
        self.Z = z
