from typing import TYPE_CHECKING, cast

from Options import Option
from .options import OptionRelevance

if TYPE_CHECKING:
    from . import TheWitnessOptions, WitnessWorld, RelevanceMixin


def set_options_from_ut(world: "WitnessWorld"):
    re_gen_passthrough = getattr(world, "re_gen_passthrough", None)
    if re_gen_passthrough is None:
        return

    for option_name, option_type in TheWitnessOptions.type_hints:
        if not issubclass(option_type, RelevanceMixin):
            continue

        option_class = cast(type[Option], option_type)

        if not option_type.relevance & OptionRelevance.universal_tracker_regeneration:
            continue

        if option_name not in re_gen_passthrough:
            raise ValueError("The Witness apworld you have is too new for this multiworld.")

        setattr(world.options, option_name, option_class.from_any(re_gen_passthrough[option_name]))
