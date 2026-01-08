from .Requirement import Requirement


class FusionLocation:
    name: str
    major: bool
    requirements: list[Requirement]

    def __init__(self, name, major, requirements):
        self.name = name
        self.major = major
        self.requirements = requirements
