from enum import IntEnum
from typing import Callable, Optional

from BaseClasses import Region, MultiWorld, Entrance, CollectionState
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances
from .items import weapons
from .locations import candy_box_locations, CandyBox2Location, village_shop_locations, village_house_1_locations, \
    village_locations, village_cellar_locations, map_stage_1_locations, map_stage_2_locations, map_stage_7_locations, \
    map_stage_6_locations, map_stage_5_locations, map_stage_4_locations, map_stage_3_locations, desert_locations, \
    bridge_locations, cave_locations, forest_locations, castle_entrance_locations, giant_nougat_monster_locations, \
    village_house_2_locations, sorceress_hut_locations, octopus_king_locations, naked_monkey_wizard_locations, \
    castle_egg_room_locations, dragon_locations, lighthouse_locations, hell_locations, the_developer_fight_locations, \
    forge_1_locations, forge_2_locations, forge_3_locations, forge_4_locations, forge_5_locations
from .options import CandyBox2Options


class CandyBox2Region(Region):
    pass

class Groups(IntEnum):
    QUESTS = 1

def create_regions(world: MultiWorld, options: CandyBox2Options, player: int):
    # The World
    candy_box, _ = populate_region(world, player, CandyBox2Region("Menu", player, world, "The Candy Box"), candy_box_locations, None)
    village, _ = populate_region(world, player, CandyBox2Region("Village", player, world, "The Village"), village_locations, candy_box)
    world_map_1, _ = populate_region(world, player, CandyBox2Region("World Map (1)", player, world, "The World Map"), map_stage_1_locations, village, lambda state: state.has("Progressive World Map", player, 1))
    world_map_2, _ = populate_region(world, player, CandyBox2Region("World Map (2)", player, world, "The World Map"), map_stage_2_locations, world_map_1, lambda state: state.has("Progressive World Map", player, 2))
    world_map_3, _ = populate_region(world, player, CandyBox2Region("World Map (3)", player, world, "The World Map"), map_stage_3_locations, world_map_2, lambda state: state.has("Progressive World Map", player, 3))
    world_map_4, _ = populate_region(world, player, CandyBox2Region("World Map (4)", player, world, "The World Map"), map_stage_4_locations, world_map_3, lambda state: state.has("Progressive World Map", player, 4))
    world_map_5, _ = populate_region(world, player, CandyBox2Region("World Map (5)", player, world, "The World Map"), map_stage_5_locations, world_map_4, lambda state: state.has("Progressive World Map", player, 5))
    castle, _ = populate_region(world, player, CandyBox2Region("The Castle", player, world, "The Castle"), map_stage_6_locations, world_map_5, lambda state: state.has("Progressive World Map", player, 6))
    tower_entrance, _ = populate_region(world, player, CandyBox2Region("The Tower's Entrance", player, world, "The Tower's Entrance"), map_stage_7_locations, castle, lambda state: state.has("Progressive World Map", player, 7))

    # The Village
    populate_region(world, player, CandyBox2Region("Village Shop", player, world, "The shop in the village"), village_shop_locations, village)
    populate_region(world, player, CandyBox2Region("Village House 1", player, world, "The house next to the forge in the village"), village_house_1_locations, village)
    village_house_2, _ = populate_region(world, player, CandyBox2Region("Village House 2", player, world, "The house with the Cellar quest"), village_house_2_locations, village)

    cellar_quest, village_house_quest_entrance = populate_region(world, player, CandyBox2Region("Village Cellar", player, world, "The Rat quest"), village_cellar_locations, village_house_2)
    mark_quest_entrance(village_house_quest_entrance, "Village House Enter Cellar")

    forge_1, _ = populate_region(world, player, CandyBox2Region("The Forge 1", player, world, "The Forge in the village"), forge_1_locations, village)
    forge_2, _ = populate_region(world, player, CandyBox2Region("The Forge 2", player, world, "The Forge in the village"), forge_2_locations, forge_1)
    forge_3, _ = populate_region(world, player, CandyBox2Region("The Forge 3", player, world, "The forge in the village"), forge_3_locations, forge_2)
    forge_4, _ = populate_region(world, player, CandyBox2Region("The Forge 4", player, world, "The forge in the village"), forge_4_locations, forge_3, lambda state: state.has("Progressive World Map", player, 3))
    forge_5, _ = populate_region(world, player, CandyBox2Region("The Forge 5", player, world, "The forge in the village"), forge_5_locations, forge_4, lambda state: state.has("Progressive World Map", player, 6))

    # The Desert
    _, desert_quest_entrance = populate_region(world, player, CandyBox2Region("The Desert", player, world, "The Desert"), desert_locations, world_map_1)
    mark_quest_entrance(desert_quest_entrance, "The Desert Click")

    # The Cave
    the_cave, _ = populate_region(world, player, CandyBox2Region("The Cave", player, world, "The Cave"), cave_locations, world_map_2)
    _, octopus_king_quest_entrance = populate_region(world, player, CandyBox2Region("The Octopus King Quest", player, world, "The Octopus King"), octopus_king_locations, the_cave)
    mark_quest_entrance(octopus_king_quest_entrance, "The Octopus King Click")
    _, naked_monkey_wizard_quest_entrance = populate_region(world, player, CandyBox2Region("The Naked Monkey Wizard", player, world, "The Naked Monkey Wizard"), naked_monkey_wizard_locations, the_cave)
    mark_quest_entrance(naked_monkey_wizard_quest_entrance, "Naked Monkey Wizard Click")

    # The Bridge
    _, bridge_quest_entrance = populate_region(world, player, CandyBox2Region("The Bridge", player, world, "The Bridge"), bridge_locations, world_map_2)
    mark_quest_entrance(bridge_quest_entrance, "The Bridge Click")

    populate_region(world, player, CandyBox2Region("The Sorceress' Hut", player, world, "The Sorceress' Hut"), sorceress_hut_locations, world_map_3)

    # The Forest
    _, forest_quest_entrance = populate_region(world, player, CandyBox2Region("The Forest", player, world, "The Forest"), forest_locations, world_map_4)
    mark_quest_entrance(forest_quest_entrance, "The Forest Click")

    # The Castle
    _, castle_entrance_quest_entrance = populate_region(world, player, CandyBox2Region("The Castle Entrance", player, world, "The Castle Entrance"), castle_entrance_locations, world_map_5)
    mark_quest_entrance(castle_entrance_quest_entrance, "Castle Entrance Click")

    _, giant_nougat_monster_quest_entrance = populate_region(world, player, CandyBox2Region("The Giant Nougat Monster", player, world, "The Giant Nougat Monster"), giant_nougat_monster_locations, castle)
    mark_quest_entrance(giant_nougat_monster_quest_entrance, "Giant Nougat Monster Click")

    _, castle_egg_room_quest_entrance = populate_region(world, player, CandyBox2Region("The Castle Egg Room", player, world, "The Castle Egg Room"), castle_egg_room_locations, castle)
    mark_quest_entrance(castle_egg_room_quest_entrance, "Castle Egg Room Click")

    dragon_room, _ = populate_region(world, player, CandyBox2Region("Dragon Room", player, world, "The Dragon Room"), dragon_locations, castle)

    # The lighthouse is parented to the dragon room because its puzzles are dependent on reaching the dragon first
    populate_region(world, player, CandyBox2Region("The Lighthouse", player, world, "The Lighthouse"), lighthouse_locations, dragon_room)

    _, hell_quest_entrance = populate_region(world, player, CandyBox2Region("Hell", player, world, "Hell"), hell_locations, dragon_room)
    mark_quest_entrance(hell_quest_entrance, "Hell Room Click")

    _, the_developer_quest_entrance = populate_region(world, player, CandyBox2Region("The Developer Quest", player, world, "The Developer Quest"), the_developer_fight_locations, dragon_room);
    mark_quest_entrance(the_developer_quest_entrance, "The Developer Quest Click")

def populate_region(world: MultiWorld, player: int, region: CandyBox2Region, locations: dict[str, int], parent: Region | None, rule: Optional[Callable[[CollectionState], bool]] = None):
    region.locations += [CandyBox2Location(player, location_name, locations[location_name], region) for location_name in locations]
    world.regions.append(region)
    entrance = None
    if parent is not None:
        entrance = parent.connect(region, None, rule)

    return region, entrance

def mark_quest_entrance(entrance: Entrance, name: str):
    entrance.name = name
    entrance.randomization_group = Groups.QUESTS
    disconnect_entrance_for_randomization(entrance, Groups.QUESTS)

def connect_entrances(world):
    world.entrance_randomisation = randomize_entrances(world, True, {
        Groups.QUESTS.value: [Groups.QUESTS.value]
    })