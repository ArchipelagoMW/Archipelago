from typing import TYPE_CHECKING, cast

from Options import Option
from .options import OptionRelevance

from . import RelevanceMixin, TheWitnessOptions

if TYPE_CHECKING:
    from . import WitnessWorld


def set_options_from_ut(world: "WitnessWorld"):
    re_gen_passthrough = getattr(world.multiworld, "re_gen_passthrough", None)
    if re_gen_passthrough is None:
        return

    if not "The Witness" in re_gen_passthrough:
        raise ValueError(
            "Found Universal Tracker re_gen_passthrough, but \"The Witness\" key was not in it. "
            "Something went terribly wrong here."
        )

    witness_slot_data = re_gen_passthrough["The Witness"]

    for option_name, option_type in TheWitnessOptions.type_hints.items():
        if not issubclass(option_type, RelevanceMixin):
            continue

        option_class = cast(type[Option], option_type)

        if not option_type.relevance & OptionRelevance.universal_tracker_regeneration:
            continue

        if option_name not in witness_slot_data:
            raise ValueError(
                "The Witness apworld you have is incompatible with this multiworld, "
                f"as {option_name} is missing from slot data."
            )

        setattr(world.options, option_name, option_class.from_any(witness_slot_data[option_name]))

    if "panel_hunt_required_absolute" not in witness_slot_data:
        raise ValueError(
            "The Witness apworld you have is incompatible with this multiworld, "
            "as panel_hunt_required_absolute is missing from slot data."
        )

    world.panel_hunt_required_count = witness_slot_data["panel_hunt_required_absolute"]