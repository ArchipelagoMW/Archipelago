import functools
from typing import Union, Any, Iterable

from .base_logic import BaseLogicMixin, BaseLogic
from .harvesting_logic import HarvestingLogicMixin
from .has_logic import HasLogicMixin
from ..data.harvest import ForagingSource, FruitBatsSource, MushroomCaveSource, SeasonalForagingSource


class SourceLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = SourceLogic(*args, **kwargs)


class SourceLogic(BaseLogic[Union[SourceLogicMixin, HasLogicMixin, HarvestingLogicMixin]]):

    def has_access_to_any(self, sources: Iterable[Any]):
        return self.logic.or_(*(self.logic.source.has_access_to(source) for source in sources))

    @functools.singledispatchmethod
    def has_access_to(self, source: Any):
        raise ValueError(f"Sources of type{type(source)} have no rule registered.")

    @has_access_to.register
    def _(self, source: ForagingSource):
        return self.logic.harvesting.can_forage_from(source)

    @has_access_to.register
    def _(self, source: SeasonalForagingSource):
        # Implementation could be different with some kind of "calendar shuffle"
        return self.logic.harvesting.can_forage_from(source.as_foraging_source())

    @has_access_to.register
    def _(self, _: FruitBatsSource):
        return self.logic.harvesting.can_harvest_from_fruit_bats

    @has_access_to.register
    def _(self, _: MushroomCaveSource):
        return self.logic.harvesting.can_harvest_from_mushroom_cave
