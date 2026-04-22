from dataclasses import dataclass

from worlds.rac3.constants.messages.box_theme import RAC3BOXTHEME


@dataclass
class RAC3NOTIFICATION:
    """Data structure for queued message notifications"""
    message: str
    theme: int = RAC3BOXTHEME.DEFAULT
    duration: float = 3.0
