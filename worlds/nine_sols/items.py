import pkgutil
import pkgutil
import typing
from typing import Dict, List, NamedTuple, Optional, Set

from BaseClasses import Item, ItemClassification
from Utils import restricted_loads
from .options import EarlyKeyItem, Spawn
from .should_generate import should_generate

if typing.TYPE_CHECKING:
    from . import OuterWildsWorld


class OuterWildsItem(Item):
    game = "Outer Wilds"


class OuterWildsItemData(NamedTuple):
    code: Optional[int] = None
    type: ItemClassification = ItemClassification.filler
    category: Optional[str] = None
    split_translator: Optional[bool] = None


pickled_data = pkgutil.get_data(__name__, "shared_static_logic/static_logic.pickle")
items_data = restricted_loads(pickled_data)["ITEMS"]

item_types_map = {
    "progression": ItemClassification.progression,
    "useful": ItemClassification.useful,
    "filler": ItemClassification.filler,
    "trap": ItemClassification.trap
}

item_data_table: Dict[str, OuterWildsItemData] = {}
for items_data_entry in items_data:
    item_data_table[items_data_entry["name"]] = OuterWildsItemData(
        code=(items_data_entry["code"] if "code" in items_data_entry else None),
        type=item_types_map[items_data_entry["type"]],
        category=(items_data_entry["category"] if "category" in items_data_entry else None),
        split_translator=(items_data_entry["split_translator"] if "split_translator" in items_data_entry else None),
    )

all_non_event_items_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

item_names: Set[str] = set(entry["name"] for entry in items_data)

prog_items = set(entry["name"] for entry in items_data
                 if entry["type"] == "progression" and entry["code"] is not None)
dlc_prog_items = [  # it happens that all DLC items are also prog items
    "Stranger Light Modulator",
    "Breach Override Codes",
    "River Lowlands Painting Code",
    "Cinder Isles Painting Code",
    "Hidden Gorge Painting Code",
    "Dream Totem Patch",
    "Raft Docks Patch",
    "Limbo Warp Patch",
    "Projection Range Patch",
    "Alarm Bypass Patch",
]

item_name_groups = {
    # Auto-generated groups
    # We don't need an "Everything" group because AP makes that for us

    "progression": prog_items,
    "useful": set(entry["name"] for entry in items_data if entry["type"] == "useful"),
    "filler": set(entry["name"] for entry in items_data if entry["type"] == "filler"),
    "trap": set(entry["name"] for entry in items_data if entry["type"] == "trap"),

    "Frequencies": set(n for n in item_names if n.endswith(" Frequency")),
    "Signals": set(n for n in item_names if n.endswith(" Signal")),

    # Manually curated groups
    "Ship Upgrades": {
        "Tornado Aerodynamic Adjustments",
        "Silent Running Mode",
        "Autopilot",
        "Landing Camera",
    },
    "Translators": {
        "Translator",
        "Translator (Hourglass Twins)",
        "Translator (Timber Hearth)",
        "Translator (Brittle Hollow)",
        "Translator (Giant's Deep)",
        "Translator (Dark Bramble)",
        "Translator (Other)",
    },
    "Tools": {
        "Translator",
        "Translator (Hourglass Twins)",
        "Translator (Timber Hearth)",
        "Translator (Brittle Hollow)",
        "Translator (Giant's Deep)",
        "Translator (Dark Bramble)",
        "Translator (Other)",
        "Signalscope",
        "Scout",
        "Ghost Matter Wavelength",
        "Imaging Rule",
    },
    "Base Progression": {i for i in prog_items if i not in dlc_prog_items},
    "DLC Progression": dlc_prog_items,
    "Quantum Rules": {
        "Imaging Rule",
        "Entanglement Rule",
        "Shrine Door Codes",
    },
    "Patches": {
        "Dream Totem Patch",
        "Raft Docks Patch",
        "Limbo Warp Patch",
        "Projection Range Patch",
        "Alarm Bypass Patch",
    },

    # Aliases
    "Little Scout": {"Scout"},
    "Probe": {"Scout"},
    "Anglerfish": {"Silent Running Mode"},
    "Tornado": {"Tornado Aerodynamic Adjustments"},
    "Insulation": {"Electrical Insulation"},
    "Jellyfish": {"Electrical Insulation"},
    "Quantum Wavelength": {"Imaging Rule"},
    "Quantum Camera": {"Imaging Rule"},
    "GM": {"Ghost Matter Wavelength"},
    "Ghost Matter": {"Ghost Matter Wavelength"},
    "GM Wavelength": {"Ghost Matter Wavelength"},
    "Advanced Warp Core": {"Warp Core Installation Manual"},
    "Eye Coordinates": {"Coordinates"},
    "EotU Coordinates": {"Coordinates"},
    "Eye of the Universe Coordinates": {"Coordinates"},
    "DBF": {"Distress Beacon Frequency"},
    "DB Frequency": {"Distress Beacon Frequency"},
    "EPF": {"Distress Beacon Frequency"},
    "EP Frequency": {"Distress Beacon Frequency"},
    "Escape Pod Frequency": {"Distress Beacon Frequency"},
    "QFF": {"Quantum Fluctuations Frequency"},
    "QF Frequency": {"Quantum Fluctuations Frequency"},
    "HSF": {"Hide & Seek Frequency"},
    "HS Frequency": {"Hide & Seek Frequency"},
    "DSRF": {"Deep Space Radio Frequency"},
    "DSR Frequency": {"Deep Space Radio Frequency"},
}


def create_item(player: int, name: str) -> OuterWildsItem:
    return OuterWildsItem(name, item_data_table[name].type, item_data_table[name].code, player)


# All progression and useful item types have a hardcoded number of instances regardless of options.
# It's almost always 1, so we only have to write down the number in this map when it's not 1.
repeated_prog_useful_items = {
    "Oxygen Capacity Upgrade": 3,
    "Fuel Capacity Upgrade": 3,
    "Boost Duration Upgrade": 3,
}

repeatable_filler_weights = {
    "Nothing": 0,  # no longer used, here for backwards compatibility
    "Oxygen Refill": 10,
    "Jetpack Fuel Refill": 10,
    "Marshmallow": 8,
    "Perfect Marshmallow": 1,
    "Burnt Marshmallow": 1,
}


def create_items(world: "OuterWildsWorld") -> None:
    random = world.random
    multiworld = world.multiworld
    options = world.options
    player = world.player

    items_to_create = {k: v for k, v in item_data_table.items() if should_generate(v.category, options)}

    prog_and_useful_items: List[OuterWildsItem] = []
    unique_filler: List[OuterWildsItem] = []
    for name, item in items_to_create.items():
        if item.code is None:
            # here we rely on our event items and event locations having identical names
            multiworld.get_location(name, player).place_locked_item(create_item(player, name))
        elif name == "Spacesuit":
            if options.shuffle_spacesuit.value == 0:
                multiworld.push_precollected(create_item(player, "Spacesuit"))
            else:
                prog_and_useful_items.append(create_item(player, "Spacesuit"))
        elif name == "Launch Codes" and world.spawn == Spawn.option_vanilla:
            # in vanilla spawn, Launch Codes is locked to Hornfels to ensure the player starts the time loop
            multiworld.get_location("TH: Talk to Hornfels", player).place_locked_item(create_item(player, name))
        elif item.type == ItemClassification.filler:
            if name not in repeatable_filler_weights:
                unique_filler.append(create_item(player, name))
        elif item.type != ItemClassification.trap:
            instances = 1
            if name in repeated_prog_useful_items:
                instances = repeated_prog_useful_items[name]
            if item.split_translator is not None and item.split_translator != options.split_translator:
                instances = 0
            for _ in range(0, instances):
                prog_and_useful_items.append(create_item(player, name))

    unique_filler_with_traps = unique_filler

    # replace some unique filler items with trap items, depending on trap settings
    trap_weights = options.trap_type_weights
    trap_chance = (options.trap_chance / 100)
    filler_chance = 1 - trap_chance
    apply_trap_items = options.trap_chance > 0 and any(v > 0 for v in options.trap_type_weights.values())
    if apply_trap_items:
        trap_weights_sum = sum(trap_weights.values())
        trap_overwrites = random.choices(
            population=[None] + list(trap_weights.keys()),
            weights=[filler_chance] + list((w / trap_weights_sum) * trap_chance for w in trap_weights.values()),
            k=len(unique_filler)
        )
        for i in range(0, len(unique_filler)):
            trap_overwrite = trap_overwrites[i]
            if trap_overwrite is not None:
                unique_filler_with_traps[i] = create_item(player, trap_overwrite)

    # add enough "repeatable"/non-unique filler items (and/or traps) to make item count equal location count
    # here we use the term "junk" to mean "filler or trap items"
    unique_item_count = len(prog_and_useful_items) + len(unique_filler)
    unfilled_location_count = len(multiworld.get_unfilled_locations(player))
    assert unfilled_location_count > unique_item_count
    repeatable_filler_needed = unfilled_location_count - unique_item_count
    junk_names = list(repeatable_filler_weights.keys())
    junk_weights = list(repeatable_filler_weights.values())
    if apply_trap_items:
        filler_weights_sum = sum(repeatable_filler_weights.values())
        normalized_filler_weights = list((w / filler_weights_sum) * filler_chance
                                         for w in repeatable_filler_weights.values())
        trap_weights_sum = sum(trap_weights.values())
        normalized_trap_weights = list((w / trap_weights_sum) * trap_chance for w in trap_weights.values())
        junk_names += list(trap_weights.keys())
        junk_weights = normalized_filler_weights + normalized_trap_weights
    repeatable_filler_names_with_traps = random.choices(
        population=junk_names,
        weights=junk_weights,
        k=repeatable_filler_needed
    )
    repeatable_filler_with_traps = list(create_item(player, name) for name in repeatable_filler_names_with_traps)

    itempool = prog_and_useful_items + unique_filler_with_traps + repeatable_filler_with_traps
    multiworld.itempool += itempool

    if options.early_key_item:
        relevant_translator = "Translator"
        if options.split_translator:
            if options.spawn == Spawn.option_hourglass_twins:
                relevant_translator = "Translator (Hourglass Twins)"
            if options.spawn == Spawn.option_timber_hearth:
                relevant_translator = "Translator (Timber Hearth)"
            if options.spawn == Spawn.option_brittle_hollow:
                relevant_translator = "Translator (Brittle Hollow)"
            if options.spawn == Spawn.option_giants_deep:
                relevant_translator = "Translator (Giant's Deep)"
            # ignore stranger spawn since it won't offer a Translator at all

        key_item = None
        if options.early_key_item == EarlyKeyItem.option_any:
            if options.spawn == Spawn.option_stranger:
                key_item = random.choice(["Launch Codes", "Stranger Light Modulator"])
            else:
                key_item = random.choice([relevant_translator, "Nomai Warp Codes", "Launch Codes"])
        elif options.early_key_item == EarlyKeyItem.option_translator:
            key_item = relevant_translator
        elif options.early_key_item == EarlyKeyItem.option_nomai_warp_codes:
            key_item = "Nomai Warp Codes"
        elif options.early_key_item == EarlyKeyItem.option_launch_codes:
            key_item = "Launch Codes"
        elif options.early_key_item == EarlyKeyItem.option_stranger_light_modulator:
            key_item = "Stranger Light Modulator"
        assert key_item is not None
        multiworld.local_early_items[player][key_item] = 1
