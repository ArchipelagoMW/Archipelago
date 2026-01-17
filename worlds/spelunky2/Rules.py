from typing import TYPE_CHECKING
from .enums import WorldName, RuleNames, ItemName, LocationName, JournalName, UPGRADE_SUFFIX

from BaseClasses import CollectionState
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import Spelunky2World


def has_or_unrestricted(world, state, player, item_name: str) -> bool:
    """
    Returns True if the item is in the player's possession OR
    is not in the AP-locked 'restricted_items' set (meaning it's free in-game).
    """
    return (item_name not in world.options.restricted_items) or state.has(item_name, player)


def set_common_rules(world: "Spelunky2World", player: int):
    # Primary Regions -- note starting from shortcuts is not currently in logic. When this is added, it might break certain entries (e.g. The Tusk Idol and chain requirements) # noqa: E128
    set_rule(world.get_entrance(RuleNames.MENU_TO_DWELLING), lambda state: True)
    # set_rule(world.get_entrance(RuleNames.MENU_TO_OLMECS_LAIR), lambda state: state.has(ShortcutName.OLMECS_LAIR, player) or state.has(ShortcutName.PROGRESSIVE, player, 2))  # Not implemented yet # noqa: E128
    # set_rule(world.get_entrance(RuleNames.MENU_TO_ICE_CAVES), lambda state: state.has(ShortcutName.ICE_CAVES, player) or state.has(ShortcutName.PROGRESSIVE, player, 3))  # Not implemented yet # noqa: E128

    set_rule(world.get_entrance(RuleNames.DWELLING_TO_JUNGLE),
             lambda state: state.has(WorldName.JUNGLE, player) or state.has(WorldName.PROGRESSIVE, player))
    set_rule(world.get_entrance(RuleNames.DWELLING_TO_VOLCANA),
             lambda state: state.has(WorldName.VOLCANA, player) or state.has(WorldName.PROGRESSIVE, player))
    set_rule(world.get_entrance(RuleNames.JUNGLE_TO_OLMEC),
             lambda state: state.has(WorldName.OLMECS_LAIR, player) or state.has(WorldName.PROGRESSIVE, player, 2))
    set_rule(world.get_entrance(RuleNames.VOLCANA_TO_OLMEC),
             lambda state: state.has(WorldName.OLMECS_LAIR, player) or state.has(WorldName.PROGRESSIVE, player, 2))
    set_rule(world.get_entrance(RuleNames.OLMEC_TO_TIDE_POOL),
             lambda state: state.has(WorldName.TIDE_POOL, player) or state.has(WorldName.PROGRESSIVE, player, 3))
    set_rule(world.get_entrance(RuleNames.OLMEC_TO_TEMPLE),
             lambda state: state.has(WorldName.TEMPLE, player) or state.has(WorldName.PROGRESSIVE, player, 3))
    set_rule(world.get_entrance(RuleNames.TIDEPOOL_TO_ICE_CAVES),
             lambda state: state.has(WorldName.ICE_CAVES, player) or state.has(WorldName.PROGRESSIVE, player, 4))
    set_rule(world.get_entrance(RuleNames.TEMPLE_TO_ICE_CAVES),
             lambda state: state.has(WorldName.ICE_CAVES, player) or state.has(WorldName.PROGRESSIVE, player, 4))
    set_rule(world.get_entrance(RuleNames.ICE_CAVES_TO_NEO_BABYLON),
             lambda state: state.has(WorldName.NEO_BABYLON, player) or state.has(WorldName.PROGRESSIVE, player, 5))

    # Secondary Regions
    set_rule(world.get_entrance(RuleNames.DWELLING_TO_ANY_WORLD_2),
             lambda state: has_world_2(state, player))
    set_rule(world.get_entrance(RuleNames.JUNGLE_TO_BLACK_MARKET),
             lambda state:
             (
                     has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE)
                     or world.options.can_udjat_skip
             ))
    set_rule(world.get_entrance(RuleNames.VOLCANA_TO_VLADS_CASTLE),
             lambda state:
             (
                 has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE)
                 or world.options.can_udjat_skip
             ))
    set_rule(world.get_entrance(RuleNames.TIDEPOOL_TO_ABZU),
             lambda state:
             (
                 has_or_unrestricted(world, state, player, ItemName.ANKH)
                 or world.options.can_ankh_skip
             ))
    set_rule(world.get_entrance(RuleNames.TEMPLE_TO_CITY_OF_GOLD),
             lambda state:
             has_royalty(world, state, player)
             and has_or_unrestricted(world, state, player, ItemName.SCEPTER))
    set_rule(world.get_entrance(RuleNames.CITY_OF_GOLD_TO_DUAT),
             lambda state: has_or_unrestricted(world, state, player, ItemName.ANKH))
    set_rule(world.get_entrance(RuleNames.ICE_CAVES_TO_MOTHERSHIP),
             lambda state: can_access_mothership(world, state, player))

    # People Entries
    set_rule(world.get_location(JournalName.EGGPLANT_CHILD),
             lambda state: has_or_unrestricted(world, state, player, ItemName.EGGPLANT))
    # Bestiary Entries
    set_rule(world.get_location(JournalName.QILIN),
             lambda state: can_obtain_qilin(world, state, player))
    # Item Entries
    set_rule(world.get_location(JournalName.ALIEN_COMPASS),
             lambda state: can_obtain_alien_compass(state, player))
    set_rule(world.get_location(JournalName.UDJAT_EYE),
             lambda state: has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE))
    set_rule(world.get_location(JournalName.HEDJET),
             lambda state: has_or_unrestricted(world, state, player, ItemName.HEDJET))
    set_rule(world.get_location(JournalName.CROWN),
             lambda state: has_or_unrestricted(world, state, player, ItemName.CROWN))
    set_rule(world.get_location(JournalName.ANKH),
             lambda state: has_or_unrestricted(world, state, player, ItemName.ANKH))
    set_rule(world.get_location(JournalName.TABLET_OF_DESTINY),
             lambda state: can_obtain_tablet(world, state, player))
    set_rule(world.get_location(JournalName.EXCALIBUR),
             lambda state:
             has_royalty(world, state, player)
             and has_or_unrestricted(world, state, player, ItemName.EXCALIBUR))
    set_rule(world.get_location(JournalName.BROKEN_SWORD),
             lambda state: has_or_unrestricted(world, state, player, ItemName.EXCALIBUR))
    set_rule(world.get_location(JournalName.SCEPTER),
             lambda state: has_or_unrestricted(world, state, player, ItemName.SCEPTER))
    set_rule(world.get_location(JournalName.HOU_YI_BOW),
             lambda state: has_or_unrestricted(world, state, player, ItemName.HOU_YI_BOW))
    set_rule(world.get_location(JournalName.USHABTI),
             lambda state: has_or_unrestricted(world, state, player, ItemName.USHABTI))
    set_rule(world.get_location(JournalName.EGGPLANT),
             lambda state: has_or_unrestricted(world, state, player, ItemName.EGGPLANT))


def set_sunken_city_rules(world: "Spelunky2World", player: int):
    # Entrance Rules
    set_rule(world.get_entrance(RuleNames.NEO_BABYLON_TO_SUNKEN_CITY),
             lambda state: can_access_sunken_city(world, state, player))
    set_rule(world.get_entrance(RuleNames.SUNKEN_CITY_TO_EGGPLANT_WORLD),
             lambda state: has_or_unrestricted(world, state, player, ItemName.EGGPLANT))
    set_rule(world.get_location(JournalName.ARROW_OF_LIGHT),
             lambda state: can_access_sunken_city(world, state, player))


def set_cosmic_ocean_rules(world: "Spelunky2World", player: int):
    set_rule(world.get_entrance(RuleNames.SUNKEN_CITY_TO_COSMIC_OCEAN),
             lambda state: can_access_cosmic_ocean(world, state, player))


def has_royalty(world: "Spelunky2World", state: CollectionState, player: int):
    return (
            has_or_unrestricted(world, state, player, ItemName.UDJAT_EYE)
            and (
                    state.has_all([WorldName.JUNGLE], player)
                    and has_or_unrestricted(world, state, player, ItemName.HEDJET)
                    or state.has_all([WorldName.VOLCANA], player)
                    and has_or_unrestricted(world, state, player, ItemName.CROWN)
                    or (
                            state.has(WorldName.PROGRESSIVE, player)
                            and (
                                    has_or_unrestricted(world, state, player, ItemName.HEDJET)
                                    or has_or_unrestricted(world, state, player, ItemName.CROWN)
                            )
                    )
            )
    )


def has_world_2(state: CollectionState, player: int) -> bool:
    return (
            state.has_any(
                [WorldName.JUNGLE.value, WorldName.VOLCANA],
                player
            )
            or state.has(WorldName.PROGRESSIVE, player)
    )


def can_obtain_alien_compass(state: CollectionState, player: int) -> bool:
    return (
            state.has_all([WorldName.VOLCANA, WorldName.OLMECS_LAIR, WorldName.TEMPLE], player)
            and state.can_reach(LocationName.VLADS_CASTLE, "Region", player)
            or state.has(WorldName.PROGRESSIVE, player, 3)
    )


def can_access_mothership(world: "Spelunky2World", state: CollectionState, player: int) -> bool:
    return (
        can_obtain_alien_compass(state, player)
        or world.options.can_mothership_skip
    )


def can_obtain_tablet(world: "Spelunky2World", state: CollectionState, player: int) -> bool:
    return (
            has_or_unrestricted(world, state, player, ItemName.ANKH)
            and
            has_or_unrestricted(world, state, player, ItemName.TABLET_OF_DESTINY)
            and (
                    state.can_reach(LocationName.DUAT, "Region", player)
                    or (
                            state.can_reach(LocationName.ABZU, "Region", player)
                            and
                            (
                                state.can_reach(JournalName.EXCALIBUR, "Location", player)
                                or world.options.can_kingu_skip
                            )
                    )
            )
    )


def can_obtain_qilin(world: "Spelunky2World", state: CollectionState, player: int) -> bool:
    return (
            can_obtain_tablet(world, state, player)
            and has_or_unrestricted(world, state, player, ItemName.USHABTI)
    )


def can_access_sunken_city(world: "Spelunky2World", state: CollectionState, player: int) -> bool:
    return (
            (can_obtain_qilin(world, state, player)
            and
            (
                    state.has(WorldName.SUNKEN_CITY, player)
                    or state.has(WorldName.PROGRESSIVE, player, 6)
            ))
            or world.options.can_qilin_skip
    )


def can_access_cosmic_ocean(world: "Spelunky2World", state: CollectionState, player: int) -> bool:
    return (
            has_or_unrestricted(world, state, player, ItemName.HOU_YI_BOW)
            and has_or_unrestricted(world, state, player, ItemName.ARROW_OF_LIGHT)
            and
            (
                    state.has(WorldName.COSMIC_OCEAN, player)
                    or state.has(WorldName.PROGRESSIVE, player, 7)
            )
            and can_access_sunken_city(world, state, player)
    )


def set_starter_upgrade_rules(world: "Spelunky2World", player: int):
    """Ensure starter upgrades require their locked/quest counterpart first."""

    # Get the union of all items selected for any type of upgrade.
    all_upgrades_selected = world.options.waddler_upgrades.value | world.options.item_upgrades.value

    for item_name in all_upgrades_selected:
        upgrade_name = f"{item_name}{UPGRADE_SUFFIX}"
        try:
            # All upgrades require their base item counterpart
            set_rule(
                world.get_location(upgrade_name),
                lambda state,
                       name=ItemName(item_name).value: has_or_unrestricted(world, state, player, name)
            )
        except KeyError:
            # This handles cases where an upgrade for an item exists but isn't
            # a location in the world (e.g., not selected by the player).
            pass
