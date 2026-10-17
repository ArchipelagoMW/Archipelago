import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from BaseClasses import CollectionState
from rule_builder.rules import Rule, Has
from ..items import BoosterPackItems, AccessoriesItems, FigurineItems
from ..items.shop_licenses import ProgressiveLicenses
from ... import TCG_CARD_SHOP_SIM_NAME, get_total_licenses, STARTING_LICENSES_COUNT

if TYPE_CHECKING:
    from ...world_base import TCGSimulatorBase
    from ... import  TCGSimulatorWorld

def accessToTetramonBasePacks():
    return Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value)

def accessToTetramonDestinyPacks():
    return Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value)

@dataclass(kw_only=True)
class HasLicensesForLevel(Rule[TCGSimulatorBase], game=TCG_CARD_SHOP_SIM_NAME):
    level: int
    @override
    def _instantiate(self, world: TCGSimulatorWorld) -> Rule.Resolved:
        # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
        return self.Resolved(level=self.level, total_licenses=world.total_licenses, max_level=world.options.max_level.value,player=world.player, caching_enabled=False)

    class Resolved(Rule.Resolved):
        total_licenses: int
        level: int
        max_level: int


        @override
        def _evaluate(self, state: CollectionState) -> bool:

            total_steps = self.max_level // 5
            current_step = self.level // 5

            additional_licenses = self.total_licenses - STARTING_LICENSES_COUNT

            amount = STARTING_LICENSES_COUNT + (additional_licenses * current_step) // total_steps

            total = 0
            total += sum(
                state.has(itemEnum.value, self.player)
                for itemEnum in FigurineItems
            )
            total += sum(
                state.has(itemEnum.value, self.player)
                for itemEnum in AccessoriesItems
            )
            total += sum(
                state.has(itemEnum.value, self.player)
                for itemEnum in BoosterPackItems
            )
            total += sum(
                state.has(itemEnum.value, self.player)
                for itemEnum in ProgressiveLicenses
            )
            return total >= amount

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item.value: {id(self)} for item in FigurineItems},
                **{item.value: {id(self)} for item in AccessoriesItems},
                **{item.value: {id(self)} for item in BoosterPackItems},
                **{item.value: {id(self)} for item in ProgressiveLicenses}
            }

        @override
        def __str__(self) -> str:
            return f"Has {self.amount} Licenses"