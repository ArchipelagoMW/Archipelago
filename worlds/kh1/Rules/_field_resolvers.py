import dataclasses
from typing import TYPE_CHECKING

from typing_extensions import override

from rule_builder.field_resolvers import FieldResolver

if TYPE_CHECKING:
    from .. import KH1World


@dataclasses.dataclass(frozen=True)
class PuppiesRequiredCount(FieldResolver, game="Kingdom Hearts"):

    puppies_required: int

    @override
    def resolve(self, world: "KH1World") -> int:
        puppy_value = world.options.puppy_value.value
        return -(-self.puppies_required // puppy_value)

    @override
    def __str__(self) -> str:
        return f"PuppiesRequiredCount({self.puppies_required})"
