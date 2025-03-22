from typing import TYPE_CHECKING, Any, Optional

from BaseClasses import CollectionState, Item, Location, MultiWorld
from Fill import fill_restrictive
from worlds.generic.Rules import add_item_rule

from ..Items import item_factory

if TYPE_CHECKING:
    from .. import TWWWorld


class Dungeon:
    """
    This class represents a dungeon in The Wind Waker, including its dungeon items.

    :param name: The name of the dungeon.
    :param big_key: The big key item for the dungeon.
    :param small_keys: A list of small key items for the dungeon.
    :param dungeon_items: A list of other items specific to the dungeon.
    :param player: The ID of the player associated with the dungeon.
    """

    def __init__(
        self,
        name: str,
        big_key: Optional[Item],
        small_keys: list[Item],
        dungeon_items: list[Item],
        player: int,
    ):
        self.name = name
        self.big_key = big_key
        self.small_keys = small_keys
        self.dungeon_items = dungeon_items
        self.player = player

    @property
    def keys(self) -> list[Item]:
        """
        Retrieve all the keys for the dungeon.

        :return: A list of Small Keys and the Big Key (if it exists).
        """
        return self.small_keys + ([self.big_key] if self.big_key else [])

    @property
    def all_items(self) -> list[Item]:
        """
        Retrieve all items associated with the dungeon.

        :return: A list of all items associated with the dungeon.
        """
        return self.dungeon_items + self.keys

    def __eq__(self, other: Any) -> bool:
        """
        Check equality between this dungeon and another object.

        :param other: The object to compare.
        :return: `True` if the other object is a Dungeon with the same name and player, `False` otherwise.
        """
        if isinstance(other, Dungeon):
            return self.name == other.name and self.player == other.player
        return False

    def __repr__(self) -> str:
        """
        Provide a string representation of the dungeon.

        :return: A string representing the dungeon.
        """
        return self.__str__()

    def __str__(self) -> str:
        """
        Convert the dungeon to a human-readable string.

        :return: A string in the format "<name> (Player <player>)".
        """
        return f"{self.name} (Player {self.player})"


def create_dungeons(world: "TWWWorld") -> None:
    """
    Create and assign dungeons to the given world based on game options.

    :param world: The Wind Waker game world.
    """
    player = world.player
    options = world.options

    def make_dungeon(name: str, big_key: Optional[Item], small_keys: list[Item], dungeon_items: list[Item]) -> Dungeon:
        dungeon = Dungeon(name, big_key, small_keys, dungeon_items, player)
        for item in dungeon.all_items:
            item.dungeon = dungeon
        return dungeon

    if options.progression_dungeons:
        if not options.required_bosses or "Dragon Roost Cavern" in world.boss_reqs.required_dungeons:
            world.dungeons["Dragon Roost Cavern"] = make_dungeon(
                "Dragon Roost Cavern",
                item_factory("DRC Big Key", world),
                item_factory(["DRC Small Key"] * 4, world),
                item_factory(["DRC Dungeon Map", "DRC Compass"], world),
            )

        if not options.required_bosses or "Forbidden Woods" in world.boss_reqs.required_dungeons:
            world.dungeons["Forbidden Woods"] = make_dungeon(
                "Forbidden Woods",
                item_factory("FW Big Key", world),
                item_factory(["FW Small Key"] * 1, world),
                item_factory(["FW Dungeon Map", "FW Compass"], world),
            )

        if not options.required_bosses or "Tower of the Gods" in world.boss_reqs.required_dungeons:
            world.dungeons["Tower of the Gods"] = make_dungeon(
                "Tower of the Gods",
                item_factory("TotG Big Key", world),
                item_factory(["TotG Small Key"] * 2, world),
                item_factory(["TotG Dungeon Map", "TotG Compass"], world),
            )

        if not options.required_bosses or "Forsaken Fortress" in world.boss_reqs.required_dungeons:
            world.dungeons["Forsaken Fortress"] = make_dungeon(
                "Forsaken Fortress",
                None,
                [],
                item_factory(["FF Dungeon Map", "FF Compass"], world),
            )

        if not options.required_bosses or "Earth Temple" in world.boss_reqs.required_dungeons:
            world.dungeons["Earth Temple"] = make_dungeon(
                "Earth Temple",
                item_factory("ET Big Key", world),
                item_factory(["ET Small Key"] * 3, world),
                item_factory(["ET Dungeon Map", "ET Compass"], world),
            )

        if not options.required_bosses or "Wind Temple" in world.boss_reqs.required_dungeons:
            world.dungeons["Wind Temple"] = make_dungeon(
                "Wind Temple",
                item_factory("WT Big Key", world),
                item_factory(["WT Small Key"] * 2, world),
                item_factory(["WT Dungeon Map", "WT Compass"], world),
            )


def get_dungeon_item_pool(multiworld: MultiWorld) -> list[Item]:
    """
    Retrieve the item pool for all The Wind Waker dungeons in the multiworld.

    :param multiworld: The MultiWorld instance.
    :return: List of dungeon items across all The Wind Waker dungeons.
    """
    return [
        item for world in multiworld.get_game_worlds("The Wind Waker") for item in get_dungeon_item_pool_player(world)
    ]


def get_dungeon_item_pool_player(world: "TWWWorld") -> list[Item]:
    """
    Retrieve the item pool for all dungeons specific to a player.

    :param world: The Wind Waker game world.
    :return: List of items in the player's dungeons.
    """
    return [item for dungeon in world.dungeons.values() for item in dungeon.all_items]


def get_unfilled_dungeon_locations(multiworld: MultiWorld) -> list[Location]:
    """
    Retrieve all unfilled The Wind Waker dungeon locations in the multiworld.

    :param multiworld: The MultiWorld instance.
    :return: List of unfilled The Wind Waker dungeon locations.
    """
    return [
        location
        for world in multiworld.get_game_worlds("The Wind Waker")
        for location in multiworld.get_locations(world.player)
        if location.dungeon and not location.item
    ]


def modify_dungeon_location_rules(multiworld: MultiWorld) -> None:
    """
    Modify the rules for The Wind Waker dungeon locations based on specific player-requested constraints.

    :param multiworld: The MultiWorld instance.
    """
    localized: set[tuple[int, str]] = set()
    dungeon_specific: set[tuple[int, str]] = set()
    for subworld in multiworld.get_game_worlds("The Wind Waker"):
        player = subworld.player
        if player not in multiworld.groups:
            localized |= {(player, item_name) for item_name in subworld.dungeon_local_item_names}
            dungeon_specific |= {(player, item_name) for item_name in subworld.dungeon_specific_item_names}

    if localized:
        in_dungeon_items = [item for item in get_dungeon_item_pool(multiworld) if (item.player, item.name) in localized]
        if in_dungeon_items:
            locations = [location for location in get_unfilled_dungeon_locations(multiworld)]

            for location in locations:
                if dungeon_specific:
                    # Special case: If Dragon Roost Cavern has its own small keys, then ensure the first chest isn't the
                    # Big Key. This is to avoid placing the Big Key there during fill and resulting in a costly swap.
                    if location.name == "Dragon Roost Cavern - First Room":
                        add_item_rule(
                            location,
                            lambda item: item.name != "DRC Big Key"
                            or (item.player, "DRC Small Key") in dungeon_specific,
                        )

                    # Add item rule to ensure dungeon items are in their own dungeon when they should be.
                    add_item_rule(
                        location,
                        lambda item, dungeon=location.dungeon: not (item.player, item.name) in dungeon_specific
                        or item.dungeon is dungeon,
                    )


def fill_dungeons_restrictive(multiworld: MultiWorld) -> None:
    """
    Correctly fill The Wind Waker dungeons in the multiworld.

    :param multiworld: The MultiWorld instance.
    """
    localized: set[tuple[int, str]] = set()
    dungeon_specific: set[tuple[int, str]] = set()
    for subworld in multiworld.get_game_worlds("The Wind Waker"):
        player = subworld.player
        if player not in multiworld.groups:
            localized |= {(player, item_name) for item_name in subworld.dungeon_local_item_names}
            dungeon_specific |= {(player, item_name) for item_name in subworld.dungeon_specific_item_names}

    if localized:
        in_dungeon_items = [item for item in get_dungeon_item_pool(multiworld) if (item.player, item.name) in localized]
        if in_dungeon_items:
            locations = [location for location in get_unfilled_dungeon_locations(multiworld)]
            multiworld.random.shuffle(locations)

            # Dungeon-locked items have to be placed first so as not to run out of space for dungeon-locked items.
            # Subsort in the order Big Key, Small Key, Other before placing dungeon items.
            sort_order = {"Big Key": 3, "Small Key": 2}
            in_dungeon_items.sort(
                key=lambda item: sort_order.get(item.type, 1)
                + (5 if (item.player, item.name) in dungeon_specific else 0)
            )

            # Construct a partial `all_state` that contains only the items from `get_pre_fill_items` that aren't in a
            # dungeon.
            in_dungeon_player_ids = {item.player for item in in_dungeon_items}
            all_state_base = CollectionState(multiworld)
            for item in multiworld.itempool:
                multiworld.worlds[item.player].collect(all_state_base, item)
            pre_fill_items = []
            for player in in_dungeon_player_ids:
                pre_fill_items += multiworld.worlds[player].get_pre_fill_items()
            for item in in_dungeon_items:
                try:
                    pre_fill_items.remove(item)
                except ValueError:
                    # `pre_fill_items` should be a subset of `in_dungeon_items`, but just in case.
                    pass
            for item in pre_fill_items:
                multiworld.worlds[item.player].collect(all_state_base, item)
            all_state_base.sweep_for_advancements()

            # Remove the completion condition so that minimal-accessibility words place keys correctly.
            for player in (item.player for item in in_dungeon_items):
                if all_state_base.has("Victory", player):
                    all_state_base.remove(multiworld.worlds[player].create_item("Victory"))

            fill_restrictive(
                multiworld,
                all_state_base,
                locations,
                in_dungeon_items,
                lock=True,
                allow_excluded=True,
                name="TWW Dungeon Items",
            )
