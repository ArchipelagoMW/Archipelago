from enum import IntEnum
from typing import TYPE_CHECKING

from BaseClasses import CollectionState, Entrance, EntranceType, MultiWorld, Region
from entrance_rando import EntranceLookup, ERPlacementState, disconnect_entrance_for_randomization, randomize_entrances

from .items import CandyBox2ItemName
from .rooms import CandyBox2Room, entrance_friendly_names, lollipop_farm, quests, rooms

if TYPE_CHECKING:
    from . import CandyBox2World


class CandyBox2RandomizationGroup(IntEnum):
    QUEST = 1
    ROOM = 2
    LOLLIPOP_FARM = 3


class CandyBox2Entrance(Entrance):
    is_exit: bool = False

    def __init__(
        self,
        player: int,
        name: str = "",
        parent: Region | None = None,
        randomization_group: int = 0,
        randomization_type: EntranceType = EntranceType.ONE_WAY,
    ) -> None:
        super().__init__(player, name, parent, randomization_group, randomization_type)
        self.is_exit = False

    def configure_for_exit(self):
        self.is_exit = True

    def can_connect_to(self, other: Entrance, dead_end: bool, er_state: "ERPlacementState") -> bool:
        return (
            super().can_connect_to(other, dead_end, er_state)
            and self.randomization_type == other.randomization_type
            and not (er_state.coupled and self.is_same_exit(other))
        )

    def is_same_exit(self, other: Entrance):
        return self.name == other.name and self.is_exit == other.is_exit


class CandyBox2Region(Region):
    entrance_type = CandyBox2Entrance

    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: str | None = None):
        super().__init__(name, player, multiworld, hint)

    def create_er_target(self, name: str):
        entrance = super().create_er_target(name)
        entrance.configure_for_exit()
        return entrance


class CandyBox2RoomRegion(CandyBox2Region):
    room: str
    randomization_group: CandyBox2RandomizationGroup

    def __init__(self, room: CandyBox2Room, player: int, multiworld: MultiWorld):
        super().__init__(entrance_friendly_names[room], player, multiworld, entrance_friendly_names[room])
        self.room = str(room)
        if room in quests:
            self.randomization_group = CandyBox2RandomizationGroup.QUEST
        if room in rooms:
            self.randomization_group = CandyBox2RandomizationGroup.ROOM
        if room in lollipop_farm:
            self.randomization_group = CandyBox2RandomizationGroup.LOLLIPOP_FARM


def can_reach_room(state: CollectionState, room: CandyBox2Room, player: int):
    return state.can_reach_region(entrance_friendly_names[room], player)


# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops(state: CollectionState, player: int):
    return lollipop_count(state, player) >= 9 and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)


def can_farm_lollipops(state: CollectionState, player: int):
    return can_grow_lollipops(state, player) and state.has_all(
        [CandyBox2ItemName.PITCHFORK, CandyBox2ItemName.SHELL_POWDER, CandyBox2ItemName.GREEN_FIN], player
    )


# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies(state: CollectionState, player: int):
    return can_farm_lollipops(state, player)


def lollipop_count(state: CollectionState, player: int):
    return state.count(CandyBox2ItemName.THREE_LOLLIPOPS, player) * 3 + state.count(CandyBox2ItemName.LOLLIPOP, player)


def create_regions(world: "CandyBox2World"):
    multiworld = world.multiworld
    player = world.player

    room_regions = {
        "MENU": CandyBox2Region("Menu", player, multiworld, "The Candy Box"),
    }

    for room in [room for room in CandyBox2Room if room not in (CandyBox2Room.VILLAGE, CandyBox2Room.WORLD_MAP)]:
        room_regions[room.value] = CandyBox2RoomRegion(room, player, multiworld)

    for region in room_regions.values():
        world.multiworld.regions.append(region)

    generated_entrances = world.rules_package.apply_room_rules(room_regions, world, player)
    for entrance in generated_entrances:
        mark_room_entrance(world, entrance)


def mark_room_entrance(world: "CandyBox2World", entrance: Entrance):
    name = entrance.connected_region.room
    world.original_entrances.append((name, name))
    if entrance.connected_region.randomization_group not in entrances_to_add_to_pool(world):
        return

    entrance.name = name
    entrance.randomization_group = entrance.connected_region.randomization_group

    if entrance_participates_in_er(world, entrance):
        disconnect_entrance_for_randomization(entrance, entrance.connected_region.randomization_group, name)


def entrance_participates_in_er(world: "CandyBox2World", entrance: Entrance):
    if not world.options.randomise_tower.value and entrance.name == CandyBox2Room.TOWER.value:
        return False

    if not world.options.randomise_x_potion.value and entrance.name == CandyBox2Room.QUEST_THE_X_POTION.value:
        return False

    return True


def connect_entrances(world: "CandyBox2World"):
    if world.options.quest_randomisation == "off":
        return world.original_entrances

    if world.is_ut_regen():
        placements = world.multiworld.re_gen_passthrough["Candy Box 2"]["entranceInformation"]
        placement_state = ERPlacementState(world, EntranceLookup(world.random, False, set(), []), False)

        er_targets = {
            entrance.name: entrance
            for region in world.multiworld.get_regions(world.player)
            for entrance in region.entrances
            if not entrance.parent_region
        }

        exits = {
            ex.name: ex
            for region in world.multiworld.get_regions(world.player)
            for ex in region.exits
            if not ex.connected_region
        }

        for x in placements:
            placement_state.connect(exits[x[0]], er_targets[x[1]])
        world.entrance_randomisation = placement_state
        return world.entrance_randomisation.pairings

    if world.options.quest_randomisation == "quests_only":
        world.entrance_randomisation = randomize_entrances(
            world,
            False,
            {
                CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value],
            },
        )
        return world.entrance_randomisation.pairings

    if world.options.quest_randomisation == "quests_and_rooms_separate":
        world.entrance_randomisation = randomize_entrances(
            world,
            False,
            {
                CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value],
                CandyBox2RandomizationGroup.ROOM.value: [
                    CandyBox2RandomizationGroup.ROOM.value,
                    CandyBox2RandomizationGroup.LOLLIPOP_FARM.value,
                ],
                CandyBox2RandomizationGroup.LOLLIPOP_FARM: [
                    CandyBox2RandomizationGroup.ROOM.value,
                    CandyBox2RandomizationGroup.LOLLIPOP_FARM.value,
                ],
            },
        )
        return world.entrance_randomisation.pairings

    if world.options.quest_randomisation == "everything":
        # Place the lollipop farm first to avoid condition where ER places everything but the lollipop farm and X potion
        lollipop_farm = next(
            entrance
            for region in world.multiworld.get_regions(world.player)
            for entrance in region.entrances
            if entrance.name == CandyBox2Room.LOLLIPOP_FARM
        )
        lollipop_farm_entrance = world.random.choice(
            [
                ex
                for region in world.multiworld.get_regions(world.player)
                for ex in region.exits
                if not ex.connected_region
            ]
        )
        entrance_randomisation_entry_lollipop_farm = manual_connect_entrances(lollipop_farm_entrance, lollipop_farm)

        world.entrance_randomisation = randomize_entrances(
            world,
            False,
            {
                CandyBox2RandomizationGroup.QUEST.value: [
                    CandyBox2RandomizationGroup.QUEST.value,
                    CandyBox2RandomizationGroup.ROOM.value,
                    CandyBox2RandomizationGroup.LOLLIPOP_FARM.value,
                ],
                CandyBox2RandomizationGroup.ROOM.value: [
                    CandyBox2RandomizationGroup.QUEST.value,
                    CandyBox2RandomizationGroup.ROOM.value,
                    CandyBox2RandomizationGroup.LOLLIPOP_FARM.value,
                ],
                CandyBox2RandomizationGroup.LOLLIPOP_FARM.value: [
                    CandyBox2RandomizationGroup.QUEST.value,
                    CandyBox2RandomizationGroup.ROOM.value,
                    CandyBox2RandomizationGroup.LOLLIPOP_FARM.value,
                ],
            },
        )
        return [entrance_randomisation_entry_lollipop_farm, *world.entrance_randomisation.pairings]

    return None


def manual_connect_entrances(entrance_from: Entrance, entrance_to: Entrance):
    entrance_to_parent_region = entrance_to.connected_region
    entrance_to_parent_region.entrances.remove(entrance_to)
    entrance_from.connect(entrance_to_parent_region)
    return entrance_from.name, entrance_to.name


def entrances_to_add_to_pool(world: "CandyBox2World"):
    if world.options.quest_randomisation == "off":
        return []

    if world.options.quest_randomisation == "quests_only":
        return [CandyBox2RandomizationGroup.QUEST]

    if world.options.quest_randomisation == "quests_and_rooms_separate":
        return [
            CandyBox2RandomizationGroup.QUEST,
            CandyBox2RandomizationGroup.ROOM,
            CandyBox2RandomizationGroup.LOLLIPOP_FARM,
        ]

    if world.options.quest_randomisation == "everything":
        return [
            CandyBox2RandomizationGroup.QUEST,
            CandyBox2RandomizationGroup.ROOM,
            CandyBox2RandomizationGroup.LOLLIPOP_FARM,
        ]

    return None
