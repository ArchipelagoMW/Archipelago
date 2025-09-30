from typing import TYPE_CHECKING

from .options import OptionRelevance

if TYPE_CHECKING:
    from . import TheWitnessOptions, WitnessWorld, RelevanceMixin


def set_options_from_ut(world: "WitnessWorld"):
    re_gen_passthrough = getattr(world, "re_gen_passthrough", None)
    if re_gen_passthrough is None:
        return

    for option_name, option_type in TheWitnessOptions.type_hints:
        if not isinstance(option_type, RelevanceMixin):
            continue

        if not option_type.relevance & OptionRelevance.universal_tracker_regeneration:
            continue

        if option_name not in re_gen_passthrough:
            raise ValueError("The Witness apworld you have is too new for this multiworld.")

        setattr(world.options, option_name, option_type(re_gen_passthrough[option_name]))
