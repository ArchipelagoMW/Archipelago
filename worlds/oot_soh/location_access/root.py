from ..LogicHelpers import *

if TYPE_CHECKING:
    from .. import SohWorld


class EventLocations(StrEnum):
    ROOT_AMMO_DROP = "Root Ammo Drop"
    ROOT_DEKU_SHIELD = "Root Deku Shield"
    ROOT_HYLIAN_SHIELD = "Root Hylian Shield"
    TRIFORCE_HUNT_COMPLETION = "Triforce Hunt Completion"
    ZELDAS_LETTER_FROM_SKIP_OPTION = "Zeldas Letter From Skip Option"


def set_region_rules(world: "SohWorld") -> None:
    # Root
    # Events
    if bool(world.options.triforce_hunt):
        add_events(Regions.ROOT, world, [
            (EventLocations.TRIFORCE_HUNT_COMPLETION, Events.GAME_COMPLETED, lambda bundle:
             (has_item(Items.TRIFORCE_PIECE, bundle, world.triforce_pieces_required)))
        ])
    # Locations
    add_locations(Regions.ROOT, world, [
        (Locations.LINKS_POCKET, lambda bundle: True)
    ])
    # Connections
    connect_regions(Regions.ROOT, world, [
        (Regions.ROOT_EXITS, lambda bundle: starting_age(
            bundle) or has_item(Events.TIME_TRAVEL, bundle))
    ])

    # Event and connection for Zeldas Letter/Impas Song
    if (bool(world.options.skip_child_zelda)):
        # Events
        add_events(Regions.ROOT, world, [
            (EventLocations.ZELDAS_LETTER_FROM_SKIP_OPTION,
             Items.ZELDAS_LETTER, lambda bundle: True)
        ])
        # Connections
        connect_regions(Regions.ROOT, world, [
            (Regions.HC_GARDEN_SONG_FROM_IMPA, lambda bundle: True)
        ])

    # Connection for Master Sword as you start with it when starting age is adult and MS is not shuffled.
    if (world.options.starting_age == "adult" and not world.options.shuffle_master_sword):
        # Connections
        connect_regions(Regions.ROOT, world, [
            (Regions.MASTER_SWORD_PEDESTAL, lambda bundle: True)
        ])

    # Root Exits
    # Connections
    connect_regions(Regions.ROOT_EXITS, world, [
        (Regions.CHILD_SPAWN, lambda bundle: is_child(bundle)),
        (Regions.ADULT_SPAWN, lambda bundle: is_adult(bundle)),
        (Regions.MINUET_OF_FOREST_WARP, lambda bundle: True),
        (Regions.BOLERO_OF_FIRE_WARP, lambda bundle: True),
        (Regions.SERENADE_OF_WATER_WARP, lambda bundle: True),
        (Regions.NOCTURNE_OF_SHADOW_WARP, lambda bundle: True),
        (Regions.REQUIEM_OF_SPIRIT_WARP, lambda bundle: True),
        (Regions.PRELUDE_OF_LIGHT_WARP, lambda bundle: True),
    ])

    # Child Spawn
    # Connections
    connect_regions(Regions.CHILD_SPAWN, world, [
        (Regions.KF_LINKS_HOUSE, lambda bundle: True)
    ])

    # Adult Spawn
    # Connections
    connect_regions(Regions.ADULT_SPAWN, world, [
        (Regions.TEMPLE_OF_TIME, lambda bundle: True)
    ])

    # Minuet of Forest Warp
    # Connections
    connect_regions(Regions.MINUET_OF_FOREST_WARP, world, [
        (Regions.SACRED_FOREST_MEADOW, lambda bundle: can_use(
            Items.MINUET_OF_FOREST, bundle))
    ])

    # Bolero of Fire Warp
    # Connections
    connect_regions(Regions.BOLERO_OF_FIRE_WARP, world, [
        (Regions.DMC_CENTRAL_LOCAL, lambda bundle: can_use(
            Items.BOLERO_OF_FIRE, bundle))
    ])

    # Serenade of Water Warp
    # Connections
    connect_regions(Regions.SERENADE_OF_WATER_WARP, world, [
        (Regions.LAKE_HYLIA, lambda bundle: can_use(
            Items.SERENADE_OF_WATER, bundle))
    ])

    # Requiem of Spirit Warp
    # Connections
    connect_regions(Regions.REQUIEM_OF_SPIRIT_WARP, world, [
        (Regions.DESERT_COLOSSUS, lambda bundle: can_use(
            Items.REQUIEM_OF_SPIRIT, bundle))
    ])

    # Nocturne of Shadow Warp
    # Connections
    connect_regions(Regions.NOCTURNE_OF_SHADOW_WARP, world, [
        (Regions.GRAVEYARD_WARP_PAD_REGION, lambda bundle: can_use(
            Items.NOCTURNE_OF_SHADOW, bundle))
    ])

    # Prelude of Light Warp
    # Connections
    connect_regions(Regions.PRELUDE_OF_LIGHT_WARP, world, [
        (Regions.TEMPLE_OF_TIME, lambda bundle: can_use(
            Items.PRELUDE_OF_LIGHT, bundle))
    ])
