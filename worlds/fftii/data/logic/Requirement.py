import typing
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from ... import FinalFantasyTacticsOptions


class Requirement:
    """
    Defines a set of requirements for a Connection or Location.
    """
    items_needed: list[str] = []
    other_requirements: list[Self] = []
    name: str = __name__

    def __init__(self, items_needed, other_requirements = None):
        """
        Creates a new Requirement object. The parameters are unpacked into a series of OR requirements where everything
        in ``items_required`` and one of the entries in ``other_requirements``
        must be met for the Requirement to be passed.

        :param items_needed: A list of items that are all required to be had.
        :param other_requirements: A list of Requirement objects.
            If not empty, one of these must be fulfilled in addition to the ``items_needed``.
        """
        if other_requirements is None:
            other_requirements = list()
        self.items_needed = items_needed
        self.other_requirements = other_requirements
        self.name: str = self.__class__.__name__

    def __repr__(self):
        return_string = f"{self.name}\n"
        return_string += f"ItemsNeeded: [{', '.join(self.items_needed)}]\n"
        return_string += (f"OtherRequirements: "
                          f"[{', '.join([requirement.name for requirement in self.other_requirements])}]\n")
        return return_string

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def check_option_enabled(options: "FinalFantasyTacticsOptions") -> bool:
        return True