from __future__ import annotations

from typing import Set, Tuple, Union, TYPE_CHECKING

from .FactorioUtils import FactorioElement

if TYPE_CHECKING:
    from FactorioModpack import FactorioModpack


def always(state) -> bool:
    return True

class Technology(FactorioElement):  # maybe make subclass of Location?
    progressive: Tuple[str, ...]
    unlocks: Union[Set[str], bool]  # bool case is for progressive technologies
    modifiers: list[str]

    def __init__(self, technology_name: str, modpack: "FactorioModpack", progressive: Tuple[str, ...] = (),
                 modifiers: list[str] = None, unlocks: Union[Set[str], bool] = None):
        self.name = technology_name
        self.modpack = modpack
        self.progressive = progressive
        if modifiers is None:
            modifiers = []
        self.modifiers =  modifiers
        if unlocks:
            self.unlocks = unlocks
        else:
            self.unlocks = set()

    @property
    def has_modifier(self) -> bool:
        return bool(self.modifiers)

    def get_custom(self, world, allowed_packs: Set[str], player: int) -> CustomTechnology:
        return CustomTechnology(self, world, allowed_packs, player)

    def useful(self) -> bool:
        if self.name in self.modpack.force_useless_technologies:
            return not self.modpack.force_useless_technologies[self.name]
        return self.has_modifier or self.unlocks


class CustomTechnology(Technology):
    """A particularly configured Technology for a world."""
    ingredients: Set[str]

    def __init__(self, origin: Technology, world, allowed_packs: Set[str], player: int):
        ingredients = allowed_packs
        self.player = player
        if origin.name not in origin.modpack.forced_locations.keys():
            ingredients = set(world.random.sample(list(ingredients), world.random.randint(1, len(ingredients))))
        self.ingredients = ingredients
        super(CustomTechnology, self).__init__(origin.name, origin.modpack)

    def get_prior_technologies(self) -> Set[Technology]:
        """Get Technologies that have to precede this one to resolve tree connections."""
        technologies = set()
        for ingredient in self.ingredients:
            technologies |= self.modpack.required_technologies[ingredient]  # technologies that unlock the recipes
        return technologies
