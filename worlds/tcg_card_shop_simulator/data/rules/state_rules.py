from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from BaseClasses import CollectionState
from rule_builder.rules import Rule, Has
from ..items import BoosterPackItems, AccessoriesItems, FigurineItems
from ..items.shop_licenses import ProgressiveLicenses
from ... import TCG_CARD_SHOP_SIM_NAME, get_total_licenses, STARTING_LICENSES_COUNT, TableTopItems
from ...world_base import TCGSimulatorBase

if TYPE_CHECKING:
    from ... import  TCGSimulatorWorld

def accessToTetramonBasePacks():
    return (
            (Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value)) |
            (Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX.value)) |
            (Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX.value)) |
            (Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX.value))
            )

def accessToTetramonDestinyPacks():
    return (
            (Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX.value)) |
            (Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX.value)) |
            (Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX.value)) |
            (Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_PACK.value) |
        Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX.value))
            )

def hasAllPacks():
    return (
            (Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_PACK.value) |
             Has(BoosterPackItems.PROGRESSIVE_BASIC_CARD_BOX.value)) &
            (Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_PACK.value) |
             Has(BoosterPackItems.PROGRESSIVE_RARE_CARD_BOX.value)) &
            (Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_PACK.value) |
             Has(BoosterPackItems.PROGRESSIVE_EPIC_CARD_BOX.value)) &
            (Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_PACK.value) |
             Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_CARD_BOX.value))
            &
            (Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_PACK.value) |
            Has(BoosterPackItems.PROGRESSIVE_BASIC_DESTINY_BOX.value)) &
            (Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_PACK.value) |
            Has(BoosterPackItems.PROGRESSIVE_RARE_DESTINY_BOX.value)) &
            (Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_PACK.value) |
            Has(BoosterPackItems.PROGRESSIVE_EPIC_DESTINY_BOX.value)) &
            (Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_PACK.value) |
            Has(BoosterPackItems.PROGRESSIVE_LEGENDARY_DESTINY_BOX.value))
        )

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

            total = sum(
                state.has(item.value, self.player)
                for item_enum in (
                    BoosterPackItems,
                    AccessoriesItems,
                    FigurineItems,
                    TableTopItems,
                    ProgressiveLicenses,
                )
                for item in item_enum
            )
            return total >= amount or self.total_licenses < amount

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                **{item.value: {id(self)} for item in FigurineItems},
                **{item.value: {id(self)} for item in AccessoriesItems},
                **{item.value: {id(self)} for item in BoosterPackItems},
                **{item.value: {id(self)} for item in TableTopItems},
                **{item.value: {id(self)} for item in ProgressiveLicenses}
            }

        @override
        def __str__(self) -> str:
            return f"Has licenses for {self.level}"