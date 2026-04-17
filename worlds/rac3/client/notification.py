from dataclasses import dataclass

@dataclass
class RAC3NOTIFICATION:
    """Data structure for queued message notifications"""
    message: str
    theme: int
    duration: float = 3.0
