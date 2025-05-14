import pkgutil
import typing
from typing import NamedTuple

from BaseClasses import Item, ItemClassification
from Utils import restricted_loads
from .should_generate import should_generate

if typing.TYPE_CHECKING:
    from . import NineSolsWorld


class NineSolsItem(Item):
    game = "Nine Sols"


class NineSolsItemData(NamedTuple):
    name: str = None
    code: int | None = None
    type: ItemClassification = ItemClassification.filler
    category: str | None = None


pickled_data = pkgutil.get_data(__name__, "shared_static_logic/static_logic.pickle")
items_data = restricted_loads(pickled_data)["ITEMS"]

item_types_map = {
    "progression": ItemClassification.progression,
    "progression_skip_balancing": ItemClassification.progression_skip_balancing,
    "useful": ItemClassification.useful,
    "filler": ItemClassification.filler,
    "trap": ItemClassification.trap
}

item_data_table: dict[str, NineSolsItemData] = {}
for items_data_entry in items_data:
    item_data_table[items_data_entry["name"]] = NineSolsItemData(
        name=items_data_entry["name"],
        code=(items_data_entry["code"] if "code" in items_data_entry else None),
        type=item_types_map[items_data_entry["type"]],
        category=(items_data_entry["category"] if "category" in items_data_entry else None),
    )

all_non_event_items_table = {name: data.code for name, data in item_data_table.items() if data.code is not None}

item_names: set[str] = set(entry["name"] for entry in items_data)

prog_items = set(entry["name"] for entry in items_data
                 if (entry["type"] == "progression" or entry["type"] == "progression_skip_balancing")
                 and entry["code"] is not None)

item_name_groups = {
    # Auto-generated groups
    # We don't need an "Everything" group because AP makes that for us

    "progression": prog_items,
    "useful": set(entry["name"] for entry in items_data if entry["type"] == "useful"),
    "filler": set(entry["name"] for entry in items_data if entry["type"] == "filler"),
    # "trap": set(entry["name"] for entry in items_data if entry["type"] == "trap"),

    "Sol Seals": set(entry["name"] for entry in items_data if entry["name"].startswith("Seal of ")),
    "Jades": set(entry["name"] for entry in items_data if (" Jade" in entry["name"])),
    "Map Chips": set(entry["name"] for entry in items_data if entry["name"].endswith(" Chip")),
    "Artifacts": set(entry["name"] for entry in items_data if entry["name"].startswith("(Artifact) ")),
    "Recyclables": set(entry["name"] for entry in items_data if entry["name"].startswith("(Recyclable) ")),
    "Poisons": set(entry["name"] for entry in items_data if entry["name"].startswith("(Poison) ")),
    "Database Entries": set(entry["name"] for entry in items_data if entry["name"].startswith("(Database) ")),
}


def create_item(player: int, name: str) -> NineSolsItem:
    return NineSolsItem(name, item_data_table[name].type, item_data_table[name].code, player)


# All progression and useful item types have a hardcoded number of instances regardless of options.
# It's almost always 1, so we only have to write down the number in this map when it's not 1.
repeated_prog_useful_items = {
    "Herb Catalyst": 8,
    "Pipe Vial": 2,  # with shop items, 5(???)
    "Tao Fruit": 13,
    "Greater Tao Fruit": 4,
    "Computing Unit": 4,  # with shop items, 8
    "Dark Steel": 6,
    "(Artifact) GM Fertilizer": 2,
}

# I doubt I counted these correctly, but they should be close enough to "feel right".
repeatable_filler_weights = {
    "Jin x800": 4,
    "Jin x320": 26,
    "Jin x50": 72,
    "(Recyclable) Basic Component": 15,
    "(Recyclable) Standard Component": 30,
    "(Recyclable) Advanced Component": 13,
}


def create_items(world: "NineSolsWorld") -> None:
    random = world.random
    multiworld = world.multiworld
    options = world.options
    player = world.player

    items_to_create = {k: v for k, v in item_data_table.items() if should_generate(v.category, options)}

    prog_and_useful_items: list[NineSolsItem] = []
    unique_filler: list[NineSolsItem] = []
    for name, item in items_to_create.items():
        if item.code is None:
            # here we rely on our event items and event locations having identical names
            multiworld.get_location(name, player).place_locked_item(create_item(player, name))
        elif item.name.startswith("Seal of ") and not options.shuffle_sol_seals:
            continue  # we'll place these as a group later
        elif item.type == ItemClassification.filler:
            if name not in repeatable_filler_weights:
                unique_filler.append(create_item(player, name))
        elif item.type != ItemClassification.trap:
            instances = 1
            if name in repeated_prog_useful_items:
                instances = repeated_prog_useful_items[name]
            for _ in range(0, instances):
                prog_and_useful_items.append(create_item(player, name))

    if not options.shuffle_sol_seals:
        for (location, item) in [
            ["Kuafu's Vital Sanctum", "Seal of Kuafu"],
            ["Goumang's Vital Sanctum", "Seal of Goumang"],
            ["Yanlao's Vital Sanctum", "Seal of Yanlao"],
            ["Jiequan's Vital Sanctum", "Seal of Jiequan"],
            ["Cortex Center: Defeat Lady Ethereal", "Seal of Lady Ethereal"],
            ["Ji's Vital Sanctum", "Seal of Ji"],
            ["ED (Living Area): Fuxi's Vital Sanctum", "Seal of Fuxi"],
            ["Nuwa's Vital Sanctum", "Seal of Nuwa"],
        ]:
            multiworld.get_location(location, player).place_locked_item(create_item(player, item))

    # unique_filler_with_traps = unique_filler

    # replace some unique filler items with trap items, depending on trap settings
    # TODO: uncomment this after we have trap items and options
    # trap_weights = options.trap_type_weights
    # trap_chance = (options.trap_chance / 100)
    # filler_chance = 1 - trap_chance
    # apply_trap_items = options.trap_chance > 0 and any(v > 0 for v in options.trap_type_weights.values())
    # if apply_trap_items:
    #     trap_weights_sum = sum(trap_weights.values())
    #     trap_overwrites = random.choices(
    #         population=[None] + list(trap_weights.keys()),
    #         weights=[filler_chance] + list((w / trap_weights_sum) * trap_chance for w in trap_weights.values()),
    #         k=len(unique_filler)
    #     )
    #     for i in range(0, len(unique_filler)):
    #         trap_overwrite = trap_overwrites[i]
    #         if trap_overwrite is not None:
    #             unique_filler_with_traps[i] = create_item(player, trap_overwrite)

    # add enough "repeatable"/non-unique filler items (and/or traps) to make item count equal location count
    # here we use the term "junk" to mean "filler or trap items"
    unique_item_count = len(prog_and_useful_items) + len(unique_filler)
    unfilled_location_count = len(multiworld.get_unfilled_locations(player))
    assert unfilled_location_count > unique_item_count
    repeatable_filler_needed = unfilled_location_count - unique_item_count
    junk_names = list(repeatable_filler_weights.keys())
    junk_weights = list(repeatable_filler_weights.values())

    filler_weights_sum = sum(repeatable_filler_weights.values())
    normalized_filler_weights = list((w / filler_weights_sum) for w in junk_weights)
    repeatable_filler_names = random.choices(
        population=junk_names,
        weights=normalized_filler_weights,
        k=repeatable_filler_needed
    )
    repeatable_filler_items = list(create_item(player, name) for name in repeatable_filler_names)

    # if apply_trap_items:
    #     filler_weights_sum = sum(repeatable_filler_weights.values())
    #     normalized_filler_weights = list((w / filler_weights_sum) * filler_chance
    #                                      for w in repeatable_filler_weights.values())
    #     trap_weights_sum = sum(trap_weights.values())
    #     normalized_trap_weights = list((w / trap_weights_sum) * trap_chance for w in trap_weights.values())
    #     junk_names += list(trap_weights.keys())
    #     junk_weights = normalized_filler_weights + normalized_trap_weights
    # repeatable_filler_names_with_traps = random.choices(
    #     population=junk_names,
    #     weights=junk_weights,
    #     k=repeatable_filler_needed
    # )
    # repeatable_filler_with_traps = list(create_item(player, name) for name in repeatable_filler_names_with_traps)

    pool = prog_and_useful_items + unique_filler + repeatable_filler_items
    multiworld.itempool += pool
