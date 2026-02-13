import typing
from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from ... import MetroidFusionOptions


class Requirement:
    """
    Defines a set of requirements for a Connection or Location.
    """
    items_needed: list[str] = []
    other_requirements: list[Self] = []
    energy_tanks_needed: int = 0
    name: str = __name__

    def __init__(self, items_needed, other_requirements, energy_tanks_needed = 0):
        """
        Creates a new Requirement object. The parameters are unpacked into a series of OR requirements where everything
        in ``items_required`` and one of the entries in ``other_requirements``
        must be met for the Requirement to be passed.

        :param items_needed: A list of items that are all required to be had.
        :param other_requirements: A list of Requirement objects.
            If not empty, one of these must be fulfilled in addition to the ``items_needed``.
        :param energy_tanks_needed: The number of energy tanks required.
        """
        self.items_needed = items_needed
        self.other_requirements = other_requirements
        self.energy_tanks_needed = energy_tanks_needed
        self.name: str = self.__class__.__name__

    def __repr__(self):
        return_string = f"{self.name}\n"
        return_string += f"ItemsNeeded: [{', '.join(self.items_needed)}]\n"
        return_string += (f"OtherRequirements: "
                          f"[{', '.join([requirement.name for requirement in self.other_requirements])}]\n")
        return_string += f"EnergyTanks: {self.energy_tanks_needed}"
        return return_string

    def __str__(self):
        return self.__repr__()

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return True

class PONRRequirement(Requirement):
    """Defines a set of requirements to be used when Point of No Returns are disabled.
    These should always be more minimal than any surrounding requirements."""
    additional_requirements: tuple[list[str], typing.Literal["and", "or"]]

    def __init__(self, items_needed, other_requirements, energy_tanks_needed = 0, additional_requirements = ([], "or")):
        super().__init__(items_needed, other_requirements, energy_tanks_needed)
        self.additional_requirements = additional_requirements

    @staticmethod
    def check_option_enabled(options: "MetroidFusionOptions") -> bool:
        return options.PointOfNoReturnsInLogic == options.PointOfNoReturnsInLogic.option_true
