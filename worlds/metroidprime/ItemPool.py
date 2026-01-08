from typing import TYPE_CHECKING, List
from BaseClasses import ItemClassification
from .PrimeOptions import BlastShieldAvailableTypes, BlastShieldRandomization
from .Items import (
    PROGRESSIVE_ITEM_MAPPING,
    MetroidPrimeItem,
    ProgressiveUpgrade,
    SuitUpgrade,
    get_item_for_options,
    artifact_table,
)
from .Items import MetroidPrimeItem

if TYPE_CHECKING:
    from . import MetroidPrimeWorld


def generate_base_start_inventory(world: "MetroidPrimeWorld") -> List[str]:
    assert world.starting_room_data.selected_loadout
    starting_items = [
        get_item_for_options(
            world, world.starting_room_data.selected_loadout.starting_beam
        ).value
    ]
    starting_items.extend(
        get_item_for_options(world, item).value
        for item in world.starting_room_data.selected_loadout.loadout
    )

    if not world.options.shuffle_scan_visor:
        starting_items.append(SuitUpgrade.Scan_Visor.value)

    return starting_items


def generate_item_pool(world: "MetroidPrimeWorld") -> List[MetroidPrimeItem]:
    # These are items that are only added if certain options are set
    items: List[MetroidPrimeItem] = [
        *[world.create_item(artifact) for artifact in artifact_table],
        world.create_item(SuitUpgrade.Morph_Ball.value),
        world.create_item(SuitUpgrade.Morph_Ball_Bomb.value),
        world.create_item(SuitUpgrade.Thermal_Visor.value),
        world.create_item(SuitUpgrade.X_Ray_Visor.value),
        world.create_item(SuitUpgrade.Scan_Visor.value),
        world.create_item(SuitUpgrade.Grapple_Beam.value),
        world.create_item(SuitUpgrade.Space_Jump_Boots.value),
        world.create_item(SuitUpgrade.Spider_Ball.value),
        world.create_item(SuitUpgrade.Boost_Ball.value),
        world.create_item(SuitUpgrade.Varia_Suit.value),
        world.create_item(SuitUpgrade.Gravity_Suit.value),
        world.create_item(SuitUpgrade.Phazon_Suit.value),
    ]

    # Add missiles
    progressive_missiles = 8
    for _ in range(progressive_missiles):
        items.append(
            world.create_item(
                SuitUpgrade.Missile_Expansion.value, ItemClassification.progression
            )
        )
    items.append(
        world.create_item(
            get_item_for_options(world, SuitUpgrade.Missile_Launcher).value,
            ItemClassification.progression,
        )
    )

    # Add power bombs
    max_power_bombs = 5
    for _ in range(0, max_power_bombs - 1):  # Main PB option will add one more
        items.append(
            world.create_item(
                SuitUpgrade.Power_Bomb_Expansion.value, ItemClassification.useful
            )
        )
    items.append(
        world.create_item(
            get_item_for_options(world, SuitUpgrade.Main_Power_Bomb).value,
            ItemClassification.progression,
        )
    )

    # Add energy tanks
    max_tanks = 14
    progression_tanks = 8
    for i in range(0, max_tanks):
        items.append(
            world.create_item(
                "Energy Tank",
                (
                    ItemClassification.progression
                    if i < progression_tanks
                    else ItemClassification.useful
                ),
            )
        )

    # Add beams and combos
    if world.options.progressive_beam_upgrades:
        for progressive_item in PROGRESSIVE_ITEM_MAPPING:
            for index in range(3):
                items.append(
                    world.create_item(
                        progressive_item.value,
                        get_progressive_beam_classification(
                            world, progressive_item, index
                        ),
                    )
                )
    else:
        combo_classification = (
            ItemClassification.progression
            if requires_beam_combos_for_progression(world)
            else ItemClassification.useful
        )
        items.extend(
            (
                world.create_item(SuitUpgrade.Power_Beam.value),
                world.create_item(SuitUpgrade.Wave_Beam.value),
                world.create_item(SuitUpgrade.Ice_Beam.value),
                world.create_item(SuitUpgrade.Plasma_Beam.value),
                world.create_item(SuitUpgrade.Charge_Beam.value),
                world.create_item(SuitUpgrade.Super_Missile.value),
                world.create_item(SuitUpgrade.Wavebuster.value, combo_classification),
                world.create_item(SuitUpgrade.Ice_Spreader.value, combo_classification),
                world.create_item(SuitUpgrade.Flamethrower.value, combo_classification),
            )
        )

    assert world.starting_room_data.selected_loadout

    items_to_remove = [
        *world.prefilled_item_map.values(),
        *generate_base_start_inventory(world),
    ]

    for item in items_to_remove:
        for i in range(len(items)):
            if items[i].name == item:
                items.pop(i)
                break

    # Fill Missiles for rest
    for _ in range(len(items), 100 - len(world.prefilled_item_map.values())):
        items.append(
            world.create_item(
                SuitUpgrade.Missile_Expansion.value, ItemClassification.filler
            )
        )

    return items


def requires_beam_combos_for_progression(world: "MetroidPrimeWorld") -> bool:
    return (
        world.options.blast_shield_available_types.value
        == BlastShieldAvailableTypes.option_all
        and world.options.blast_shield_randomization.value
        != BlastShieldRandomization.option_none  # type: ignore
    )


def get_progressive_beam_classification(
    world: "MetroidPrimeWorld", progressive_item: ProgressiveUpgrade, index: int
) -> ItemClassification:
    # Charge Beam
    if index < 2:
        return ItemClassification.progression
    # Beam Combos
    if index == 2 and (
        progressive_item == ProgressiveUpgrade.Progressive_Power_Beam
        or requires_beam_combos_for_progression(world)
    ):
        return ItemClassification.progression
    return ItemClassification.useful
