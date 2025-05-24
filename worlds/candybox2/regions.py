from enum import IntEnum
from typing import Callable, Optional, TYPE_CHECKING

from BaseClasses import Region, MultiWorld, Entrance, CollectionState, EntranceType
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances, ERPlacementState
from .items import CandyBox2ItemName, items, candy_box_2_base_id
from .locations import CandyBox2Location, CandyBox2LocationName
from .rooms import CandyBox2Room, quests, x_quest, rooms, entrance_friendly_names, lollipop_farm

if TYPE_CHECKING:
    from . import CandyBox2World


class CandyBox2RandomizationGroup(IntEnum):
    QUEST = 1
    X_QUEST = 2
    ROOM = 3
    LOLLIPOP_FARM = 4


class CandyBox2Entrance(Entrance):
    is_exit: bool = False

    def __init__(self, player: int, name: str = "", parent: Optional[Region] = None, randomization_group: int = 0,
                 randomization_type: EntranceType = EntranceType.ONE_WAY) -> None:
        super().__init__(player, name, parent, randomization_group, randomization_type)
        self.is_exit = False

    def configure_for_exit(self):
        self.is_exit = True

    def can_connect_to(self, other: Entrance, dead_end: bool, er_state: "ERPlacementState") -> bool:
        return self.randomization_type == other.randomization_type and not (er_state.coupled and self.is_same_exit(other))

    def is_same_exit(self, other: Entrance):
        return self.name == other.name and self.is_exit == other.is_exit


class CandyBox2Region(Region):
    entrance_type = CandyBox2Entrance
    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: Optional[str] = None):
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
        if room in x_quest:
            self.randomization_group = CandyBox2RandomizationGroup.X_QUEST
        if room in rooms:
            self.randomization_group = CandyBox2RandomizationGroup.ROOM
        if room in lollipop_farm:
            self.randomization_group = CandyBox2RandomizationGroup.LOLLIPOP_FARM

def can_reach_room(state: CollectionState, room: CandyBox2Room, player: int):
    return state.can_reach_region(entrance_friendly_names[room], player)

def can_brew(state: CollectionState, player: int, also_require_lollipops: bool):
    return (state.has(CandyBox2ItemName.SORCERESS_CAULDRON, player) and can_farm_candies(state, player) and (not also_require_lollipops or can_farm_lollipops(state, player)))

# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops(state: CollectionState, player: int):
    return lollipop_count(state, player) >= 9 and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

def can_farm_lollipops(state: CollectionState, player: int):
    return can_grow_lollipops(state, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player) and state.has(CandyBox2ItemName.PITCHFORK, player) and state.has(CandyBox2ItemName.SHELL_POWDER, player) and state.has(CandyBox2ItemName.GREEN_FIN, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies(state: CollectionState, player: int):
    return can_farm_lollipops(state, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player) and can_reach_room(state, CandyBox2Room.LOLLIPOP_FARM, player)

def lollipop_count(state: CollectionState, player: int):
    return state.count(CandyBox2ItemName.THREE_LOLLIPOPS, player)*3 + state.count(CandyBox2ItemName.LOLLIPOP, player)


def create_regions(world: "CandyBox2World"):
    multiworld = world.multiworld
    player = world.player

    room_regions = {
        "MENU": CandyBox2Region("Menu", player, multiworld, "The Candy Box"),
    }

    for room in [room for room in CandyBox2Room if room != CandyBox2Room.VILLAGE and room != CandyBox2Room.WORLD_MAP]:
        room_regions[room.value] = CandyBox2RoomRegion(room, player, multiworld)

    for region in  room_regions.values():
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
    disconnect_entrance_for_randomization(entrance, entrance.connected_region.randomization_group, name)

def connect_entrances(world: "CandyBox2World"):
    if world.options.quest_randomisation == "off":
        return world.original_entrances

    if hasattr(world.multiworld, "re_gen_passthrough"):
        placements = getattr(world.multiworld, "re_gen_passthrough")["Candy Box 2"]["entranceInformation"]
        placement_state = ERPlacementState(world, True)

        er_targets = dict([(entrance.name, entrance) for region in world.multiworld.get_regions(world.player)
                             for entrance in region.entrances if not entrance.parent_region])

        exits = dict([(ex.name, ex) for region in world.multiworld.get_regions(world.player)
                        for ex in region.exits if not ex.connected_region])

        for x in placements:
            placement_state.connect(exits[x[0]], er_targets[x[1]])
        world.entrance_randomisation = placement_state
        return world.entrance_randomisation.pairings

    if world.options.quest_randomisation == "quests_only_except_x_potion_quest":
        world.entrance_randomisation = randomize_entrances(world, True, {
            CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value],
        })
        return world.entrance_randomisation.pairings

    if world.options.quest_randomisation == "quests_only":
        world.entrance_randomisation = randomize_entrances(world, True, {
            CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value],
            CandyBox2RandomizationGroup.X_QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value],
        })
        return world.entrance_randomisation.pairings

    if world.options.quest_randomisation == "quests_and_rooms_separate":
        world.entrance_randomisation = randomize_entrances(world, True, {
            CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value],
            CandyBox2RandomizationGroup.X_QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value],
            CandyBox2RandomizationGroup.ROOM.value: [CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],
            CandyBox2RandomizationGroup.LOLLIPOP_FARM: [CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],
        })
        return world.entrance_randomisation.pairings

    if world.options.quest_randomisation == "everything":
        # Place the lollipop farm first to avoid condition where ER places everything but the lollipop farm and X potion
        lollipop_farm = next(entrance for region in world.multiworld.get_regions(world.player) for entrance in region.entrances if entrance.name == CandyBox2Room.LOLLIPOP_FARM)
        lollipop_farm_entrance = world.random.choice([ex for region in world.multiworld.get_regions(world.player) for ex in region.exits if not ex.connected_region])
        entrance_randomisation_entry_lollipop_farm = manual_connect_entrances(lollipop_farm_entrance, lollipop_farm)

        world.entrance_randomisation = randomize_entrances(world, True, {
            CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value, CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],
            CandyBox2RandomizationGroup.ROOM.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value, CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],
            CandyBox2RandomizationGroup.LOLLIPOP_FARM.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value, CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],

            # The lollipop farm can never go behind the X quest because the X quest requires lollipops
            CandyBox2RandomizationGroup.X_QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value, CandyBox2RandomizationGroup.ROOM.value],
        })
        return [entrance_randomisation_entry_lollipop_farm, *world.entrance_randomisation.pairings]

def manual_connect_entrances(entrance_from: Entrance, entrance_to: Entrance):
    entrance_to_parent_region = entrance_to.connected_region
    entrance_to_parent_region.entrances.remove(entrance_to)
    entrance_from.connect(entrance_to_parent_region)
    return entrance_from.name, entrance_to.name

def entrances_to_add_to_pool(world: "CandyBox2World"):
    if world.options.quest_randomisation == "off":
        return []

    if world.options.quest_randomisation == "quests_only_except_x_potion_quest":
        return [CandyBox2RandomizationGroup.QUEST]

    if world.options.quest_randomisation == "quests_only":
        return [CandyBox2RandomizationGroup.QUEST, CandyBox2RandomizationGroup.X_QUEST]

    if world.options.quest_randomisation == "quests_and_rooms_separate":
        return [CandyBox2RandomizationGroup.QUEST, CandyBox2RandomizationGroup.X_QUEST, CandyBox2RandomizationGroup.ROOM, CandyBox2RandomizationGroup.LOLLIPOP_FARM]

    if world.options.quest_randomisation == "everything":
        return [CandyBox2RandomizationGroup.QUEST, CandyBox2RandomizationGroup.X_QUEST, CandyBox2RandomizationGroup.ROOM, CandyBox2RandomizationGroup.LOLLIPOP_FARM]