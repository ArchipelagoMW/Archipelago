from dataclasses import dataclass

@dataclass
class BaseTechnologyData:
    name: str

@dataclass
class TechnologyData(BaseTechnologyData):
    recipes: set[str] | None
    unlocks: set[str] | None

@dataclass
class ProgressiveTechnologyData(BaseTechnologyData):
    technologies: list[TechnologyData]

@dataclass
class CustomTechnologyData(TechnologyData):
    pass