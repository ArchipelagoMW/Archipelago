"""Kirby AM test base classes and fixtures."""
from test.bases import WorldTestBase
from .. import KirbyAmWorld


class KirbyAmTestBase(WorldTestBase):
    """Base class for Kirby AM world tests."""
    
    game = "Kirby & The Amazing Mirror"
    world: KirbyAmWorld
