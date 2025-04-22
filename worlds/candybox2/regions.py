from enum import IntEnum
from typing import Callable, Optional, TYPE_CHECKING

from BaseClasses import Region, MultiWorld, Entrance, CollectionState, EntranceType
from Utils import visualize_regions
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances, ERPlacementState
from .locations import candy_box_locations, CandyBox2Location, village_shop_locations, village_house_1_locations, \
    village_locations, village_cellar_locations, map_stage_1_locations, map_stage_2_locations, map_stage_7_locations, \
    map_stage_6_locations, map_stage_5_locations, map_stage_4_locations, map_stage_3_locations, desert_locations, \
    bridge_locations, cave_locations, forest_locations, castle_entrance_locations, giant_nougat_monster_locations, \
    village_house_2_locations, sorceress_hut_locations, octopus_king_locations, naked_monkey_wizard_locations, \
    castle_egg_room_locations, dragon_locations, lighthouse_locations, hell_locations, the_developer_fight_locations, \
    wishing_well_locations, hole_locations, \
    desert_fortress_locations, teapot_quest_locations, xinopherydon_quest_locations, ledge_room_quest_locations, \
    castle_trap_room_locations, squirrel_tree_locations, the_sea_locations, lonely_house_locations, dig_spot_locations, \
    yourself_fight_locations, castle_dark_room_locations, castle_bakehouse_locations, pogo_stick_spot_locations, \
    pier_locations, lollipop_farm_locations, forge_locations, village_minigame_locations
from .rooms import CandyBox2Room, quests, x_quest, rooms, entrance_friendly_names, lollipop_farm
from .rules import weapon_is_at_least, chocolate_count, can_farm_candies, can_grow_lollipops, \
    has_weapon, can_reach_room, can_brew

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

def create_regions(world: "CandyBox2World"):
    multiworld = world.multiworld
    player = world.player

    # The World
    candy_box = populate_region(world, player, CandyBox2Region("Menu", player, multiworld, "The Candy Box"), candy_box_locations, None)
    village = populate_region(world, player, CandyBox2Region("Village", player, multiworld, "The Village"), village_locations, candy_box)
    world_map_1 = populate_region(world, player, CandyBox2Region("World Map (1)", player, multiworld, "The World Map"), map_stage_1_locations, village, lambda state: state.has("Progressive World Map", player, 1))
    world_map_2 = populate_region(world, player, CandyBox2Region("World Map (2)", player, multiworld, "The World Map"), map_stage_2_locations, world_map_1, lambda state: state.has("Progressive World Map", player, 2))
    world_map_3 = populate_region(world, player, CandyBox2Region("World Map (3)", player, multiworld, "The World Map"), map_stage_3_locations, world_map_2, lambda state: state.has("Progressive World Map", player, 3))
    world_map_4 = populate_region(world, player, CandyBox2Region("World Map (4)", player, multiworld, "The World Map"), map_stage_4_locations, world_map_3, lambda state: state.has("Progressive World Map", player, 4))
    world_map_5 = populate_region(world, player, CandyBox2Region("World Map (5)", player, multiworld, "The World Map"), map_stage_5_locations, world_map_4, lambda state: state.has("Progressive World Map", player, 5))
    castle = populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.CASTLE, player, multiworld), map_stage_6_locations, world_map_5, lambda state: state.has("Progressive World Map", player, 6))
    tower_entrance = populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.TOWER, player, multiworld), map_stage_7_locations, castle, lambda state: state.has("Progressive World Map", player, 7) and can_reach_room(state, CandyBox2Room.CASTLE, player), True)

    # The Village
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.VILLAGE_SHOP, player, multiworld), village_shop_locations, village)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.VILLAGE_FURNISHED_HOUSE, player, multiworld), village_house_1_locations, village)
    village_house_2 = populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.VILLAGE_QUEST_HOUSE, player, multiworld), village_house_2_locations, village)

    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CELLAR, player, multiworld), village_cellar_locations, village_house_2, lambda state: weapon_is_at_least(
        world, state, player, "Wooden Sword"))

    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.VILLAGE_FORGE, player, multiworld), forge_locations, village)

    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.VILLAGE_MINIGAME, player, multiworld), village_minigame_locations, village, lambda state: state.has("Third House Key", player))

    # The Squirrel Tree
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.SQUIRREL_TREE, player, multiworld), squirrel_tree_locations, world_map_1)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.LONELY_HOUSE, player, multiworld), lonely_house_locations, world_map_1)

    # The Desert
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_DESERT, player, multiworld), desert_locations, world_map_1)

    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.DIG_SPOT, player, multiworld), dig_spot_locations, world_map_1, lambda state: can_reach_room(state, CandyBox2Room.CAVE, player), True)

    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.POGO_STICK_SPOT, player, multiworld), pogo_stick_spot_locations, world_map_2)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.LOLLIPOP_FARM, player, multiworld), lollipop_farm_locations, world_map_2)

    # The Wishing Well
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.WISHING_WELL, player, multiworld), wishing_well_locations, world_map_2)

    # The Cave
    the_cave = populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.CAVE, player, multiworld), cave_locations, world_map_2)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_OCTOPUS_KING, player, multiworld), octopus_king_locations, the_cave)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD, player, multiworld), naked_monkey_wizard_locations, the_cave)

    # The Bridge
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_BRIDGE, player, multiworld), bridge_locations, world_map_2)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.SORCERESS_HUT, player, multiworld), sorceress_hut_locations, world_map_3)
    pier = populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.PIER, player, multiworld), pier_locations, world_map_4)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_SEA, player, multiworld), the_sea_locations, pier)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.LIGHTHOUSE, player, multiworld), lighthouse_locations, pier)

    # The Forest
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_FOREST, player, multiworld), forest_locations, world_map_4)

    # The Castle
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE, player, multiworld), castle_entrance_locations, world_map_5)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_HOLE, player, multiworld), hole_locations, world_map_5)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER, player, multiworld), giant_nougat_monster_locations, castle)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM, player, multiworld), castle_trap_room_locations, castle)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.CASTLE_DARK_ROOM, player, multiworld), castle_dark_room_locations, castle)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.CASTLE_BAKEHOUSE, player, multiworld), castle_bakehouse_locations, castle)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM, player, multiworld), castle_egg_room_locations, castle)
    dragon_room = populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.DRAGON, player, multiworld), dragon_locations, castle)

    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_HELL, player, multiworld), hell_locations, dragon_room)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_DEVELOPER, player, multiworld), the_developer_fight_locations, dragon_room)

    # The Desert Fortress
    desert_fortress = populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.DESERT_FORTRESS, player, multiworld), desert_fortress_locations, world_map_1, lambda state: state.has("Desert Fortress Key", player))
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_XINOPHERYDON, player, multiworld), xinopherydon_quest_locations, desert_fortress)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_TEAPOT, player, multiworld), teapot_quest_locations, desert_fortress)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_LEDGE_ROOM, player, multiworld), ledge_room_quest_locations, desert_fortress)

    # X Potion region
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_X_POTION, player, multiworld), yourself_fight_locations, candy_box, lambda state: can_brew(state, player, True), True)

def populate_region(world: "CandyBox2World", player: int, region: CandyBox2Region, locations: dict[str, int], parent: Region | None, rule: Optional[Callable[[CollectionState], bool]] = None, indirect: bool = False):
    region.locations += [CandyBox2Location(player, location_name, locations[location_name], region) for location_name in locations]
    world.multiworld.regions.append(region)
    entrance = None
    if parent is not None:
        entrance = parent.connect(region, None, rule)

    if type(region) is CandyBox2RoomRegion:
        mark_room_entrance(world, entrance)

    if indirect:
        world.multiworld.register_indirect_condition(region, entrance)

    return region

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
            CandyBox2RandomizationGroup.X_QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value, CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],
            CandyBox2RandomizationGroup.ROOM.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value, CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],

            # The lollipop farm can never go behind the X quest because the X quest requires lollipops
            CandyBox2RandomizationGroup.LOLLIPOP_FARM.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.ROOM.value, CandyBox2RandomizationGroup.LOLLIPOP_FARM.value],
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