from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import TheWitnessOptions, WitnessWorld


def set_options_from_ut(world: "WitnessWorld"):
    re_gen_passthrough = getattr(world, "re_gen_passthrough", None)
    if re_gen_passthrough is None:
        return

    for option_name, option_type in TheWitnessOptions.type_hints:
        if option_name in re_gen_passthrough:
            setattr(world.options, option_name, option_type(re_gen_passthrough[option_name]))
