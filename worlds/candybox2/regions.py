from enum import IntEnum
from typing import Callable, Optional

from BaseClasses import Region, MultiWorld, Entrance, CollectionState
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances
from .locations import candy_box_locations, CandyBox2Location, village_shop_locations, village_house_1_locations, \
    village_locations, village_cellar_locations, map_stage_1_locations, map_stage_2_locations, map_stage_7_locations, \
    map_stage_6_locations, map_stage_5_locations, map_stage_4_locations, map_stage_3_locations, desert_locations, \
    bridge_locations, cave_locations, forest_locations, castle_entrance_locations, giant_nougat_monster_locations, \
    village_house_2_locations, sorceress_hut_locations, octopus_king_locations, naked_monkey_wizard_locations, \
    castle_egg_room_locations, dragon_locations, lighthouse_locations, hell_locations, the_developer_fight_locations, \
    forge_1_locations, forge_2_locations, forge_3_locations, forge_4_locations, forge_5_locations, \
    wishing_well_locations, wishing_well_glove_locations, wishing_well_tribal_spear_locations, \
    wishing_well_monkey_wizard_staff_locations, wishing_well_knight_body_armour_locations, \
    wishing_well_octopus_king_crown_locations, wishing_well_giant_spoon_locations, hole_locations, \
    desert_fortress_locations, teapot_quest_locations, xinopherydron_quest_locations, ledge_room_quest_locations, \
    castle_trap_room_locations, squirrel_tree_locations, the_sea_locations, lonely_house_locations, dig_spot_locations, \
    yourself_fight_locations, castle_dark_room_locations
from .options import CandyBox2Options
from .rules import weapon_is_at_least, armor_is_at_least


class CandyBox2Region(Region):
    pass

class Groups(IntEnum):
    QUESTS = 1
    X_QUEST = 2

def create_regions(world):
    multiworld = world.multiworld
    player = world.player

    # The World
    candy_box, _ = populate_region(multiworld, player, CandyBox2Region("Menu", player, multiworld, "The Candy Box"), candy_box_locations, None)
    village, _ = populate_region(multiworld, player, CandyBox2Region("Village", player, multiworld, "The Village"), village_locations, candy_box)
    world_map_1, _ = populate_region(multiworld, player, CandyBox2Region("World Map (1)", player, multiworld, "The World Map"), map_stage_1_locations, village, lambda state: state.has("Progressive World Map", player, 1))
    world_map_2, _ = populate_region(multiworld, player, CandyBox2Region("World Map (2)", player, multiworld, "The World Map"), map_stage_2_locations, world_map_1, lambda state: state.has("Progressive World Map", player, 2))
    world_map_3, _ = populate_region(multiworld, player, CandyBox2Region("World Map (3)", player, multiworld, "The World Map"), map_stage_3_locations, world_map_2, lambda state: state.has("Progressive World Map", player, 3))
    world_map_4, _ = populate_region(multiworld, player, CandyBox2Region("World Map (4)", player, multiworld, "The World Map"), map_stage_4_locations, world_map_3, lambda state: state.has("Progressive World Map", player, 4))
    world_map_5, _ = populate_region(multiworld, player, CandyBox2Region("World Map (5)", player, multiworld, "The World Map"), map_stage_5_locations, world_map_4, lambda state: state.has("Progressive World Map", player, 5))
    castle, _ = populate_region(multiworld, player, CandyBox2Region("The Castle", player, multiworld, "The Castle"), map_stage_6_locations, world_map_5, lambda state: state.has("Progressive World Map", player, 6))
    tower_entrance, _ = populate_region(multiworld, player, CandyBox2Region("The Tower's Entrance", player, multiworld, "The Tower's Entrance"), map_stage_7_locations, castle, lambda state: state.has("Progressive World Map", player, 7))

    # The Village
    populate_region(multiworld, player, CandyBox2Region("Village Shop", player, multiworld, "The shop in the village"), village_shop_locations, village)
    populate_region(multiworld, player, CandyBox2Region("Village House 1", player, multiworld, "The house next to the forge in the village"), village_house_1_locations, village)
    village_house_2, _ = populate_region(multiworld, player, CandyBox2Region("Village House 2", player, multiworld, "The house with the Cellar quest"), village_house_2_locations, village)

    cellar_quest, village_house_quest_entrance = populate_region(multiworld, player, CandyBox2Region("Village Cellar", player, multiworld, "The Rat quest"), village_cellar_locations, village_house_2, lambda state: weapon_is_at_least(state, player, "Wooden Sword"))
    mark_quest_entrance(world, village_house_quest_entrance, "Village House Enter Cellar")

    forge_1, _ = populate_region(multiworld, player, CandyBox2Region("The Forge 1", player, multiworld, "The Forge in the village"), forge_1_locations, village)
    forge_2, _ = populate_region(multiworld, player, CandyBox2Region("The Forge 2", player, multiworld, "The Forge in the village"), forge_2_locations, forge_1)
    forge_3, _ = populate_region(multiworld, player, CandyBox2Region("The Forge 3", player, multiworld, "The forge in the village"), forge_3_locations, forge_2)
    forge_4, _ = populate_region(multiworld, player, CandyBox2Region("The Forge 4", player, multiworld, "The forge in the village"), forge_4_locations, forge_3, lambda state: state.has("Progressive World Map", player, 3))
    forge_5, _ = populate_region(multiworld, player, CandyBox2Region("The Forge 5", player, multiworld, "The forge in the village"), forge_5_locations, forge_4, lambda state: state.has("Progressive World Map", player, 6))

    # The Squirrel Tree
    populate_region(multiworld, player, CandyBox2Region("A tree", player, multiworld, "The squirrel's tree"), squirrel_tree_locations, world_map_1)

    populate_region(multiworld, player, CandyBox2Region("The Lonely House", player, multiworld, "The Lonely House"), lonely_house_locations, world_map_1)

    # The Desert
    _, desert_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Desert", player, multiworld, "The Desert"), desert_locations, world_map_1, lambda state: weapon_is_at_least(state, player, "Iron Axe"))
    mark_quest_entrance(world, desert_quest_entrance, "The Desert Click")

    # This is connected to world_map_2 because it is only accessible once you see the stones in the cave
    populate_region(multiworld, player, CandyBox2Region("The Dig Spot", player, multiworld, "The Dig Spot"), dig_spot_locations, world_map_2)

    # The Wishing Well
    wishing_well, _ = populate_region(multiworld, player, CandyBox2Region("The Wishing Well", player, multiworld, "The Wishing Well"), wishing_well_locations, world_map_2, lambda state: state.has("Chocolate Bar", player))
    populate_region(multiworld, player, CandyBox2Region("The Wishing Well (Unlocked Gloves)", player, multiworld, "The Wishing Well"), wishing_well_glove_locations, wishing_well, lambda state: state.has("Leather Gloves", player))
    populate_region(multiworld, player, CandyBox2Region("The Wishing Well (Unlocked Tribal Spear)", player, multiworld, "The Wishing Well"), wishing_well_tribal_spear_locations, wishing_well, lambda state: state.has("Tribal Spear", player))
    populate_region(multiworld, player, CandyBox2Region("The Wishing Well (Unlocked Monkey Wizard Staff)", player, multiworld, "The Wishing Well"), wishing_well_monkey_wizard_staff_locations, wishing_well, lambda state: state.has("The Monkey Wizard Staff", player))
    populate_region(multiworld, player, CandyBox2Region("The Wishing Well (Unlocked Knight Body Armour)", player, multiworld, "The Wishing Well"), wishing_well_knight_body_armour_locations, wishing_well, lambda state: state.has("Knight Body Armour", player))
    populate_region(multiworld, player, CandyBox2Region("The Wishing Well (Unlocked Octopus King Crown)", player, multiworld, "The Wishing Well"), wishing_well_octopus_king_crown_locations, wishing_well, lambda state: state.has("The Octopus King Crown", player))
    populate_region(multiworld, player, CandyBox2Region("The Wishing Well (Unlocked Giant Spoon)", player, multiworld, "The Wishing Well"), wishing_well_giant_spoon_locations, wishing_well, lambda state: state.has("Giant Spoon", player))

    # The Cave
    the_cave, _ = populate_region(multiworld, player, CandyBox2Region("The Cave", player, multiworld, "The Cave"), cave_locations, world_map_2)
    _, octopus_king_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Octopus King Quest", player, multiworld, "The Octopus King"), octopus_king_locations, the_cave, lambda state: state.has("The Sorceress' Cauldron", player) and weapon_is_at_least(state, player, "The Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))
    mark_quest_entrance(world, octopus_king_quest_entrance, "The Octopus King Click")
    _, naked_monkey_wizard_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Naked Monkey Wizard", player, multiworld, "The Naked Monkey Wizard"), naked_monkey_wizard_locations, the_cave, lambda state: state.has("Boots of Introspection", player) and state.has("The Beginners' Grimoire", player) and state.has("Octopus King Crown with Jaspers", player) and weapon_is_at_least(state, player, "The Troll's Bludgeon") and armor_is_at_least(state, player, "Lightweight Body Armour"))
    mark_quest_entrance(world, naked_monkey_wizard_quest_entrance, "Naked Monkey Wizard Click")

    # The Bridge
    _, bridge_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Bridge", player, multiworld, "The Bridge"), bridge_locations, world_map_2, lambda state: weapon_is_at_least(state, player, "Polished Silver Sword"))
    mark_quest_entrance(world, bridge_quest_entrance, "The Bridge Click")

    populate_region(multiworld, player, CandyBox2Region("The Sorceress' Hut", player, multiworld, "The Sorceress' Hut"), sorceress_hut_locations, world_map_3)

    _, sea_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Sea", player, multiworld, "The Sea"), the_sea_locations, world_map_4, lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and armor_is_at_least(state, player, "Lightweight Body Armour"))
    mark_quest_entrance(world, sea_quest_entrance, "The Sea Click")

    # The Forest
    _, forest_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Forest", player, multiworld, "The Forest"), forest_locations, world_map_4, lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour"))
    mark_quest_entrance(world, forest_quest_entrance, "The Forest Click")

    # The Castle
    _, castle_entrance_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Castle Entrance", player, multiworld, "The Castle Entrance"), castle_entrance_locations, world_map_5, lambda state: weapon_is_at_least(state, player, "Enchanted Monkey Wizard Staff") and state.has("Octopus King Crown with Jaspers", player) and armor_is_at_least(state, player, "Lightweight Body Armour") and state.has("Unicorn Horn", player) and state.has("Xinopherydon Claw", player))
    mark_quest_entrance(world, castle_entrance_quest_entrance, "Castle Entrance Click")

    _, hole_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Hole", player, multiworld, "The Hole"), hole_locations, world_map_5)
    mark_quest_entrance(world, hole_quest_entrance, "Hole Click")

    _, giant_nougat_monster_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Giant Nougat Monster", player, multiworld, "The Giant Nougat Monster"), giant_nougat_monster_locations, castle, lambda state: weapon_is_at_least(state, player, "Summoning Tribal Spear") and state.has("Boots of Introspection", player) and state.has("Octopus King Crown with Obsidian", player))
    mark_quest_entrance(world, giant_nougat_monster_quest_entrance, "Giant Nougat Monster Click")

    _, castle_trap_room_entrance = populate_region(multiworld, player, CandyBox2Region("The Trap Room", player, multiworld, "The Trap Room"), castle_trap_room_locations, castle)
    mark_quest_entrance(world, castle_trap_room_entrance, "Castle Trap Room Click")

    populate_region(multiworld, player, CandyBox2Region("The Dark Room", player, multiworld, "The Dark Room"), castle_dark_room_locations, castle)

    _, castle_egg_room_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Castle Egg Room", player, multiworld, "The Castle Egg Room"), castle_egg_room_locations, castle, lambda state: state.has("Rocket Boots", player))
    mark_quest_entrance(world, castle_egg_room_quest_entrance, "Castle Egg Room Click")

    dragon_room, _ = populate_region(multiworld, player, CandyBox2Region("Dragon Room", player, multiworld, "The Dragon Room"), dragon_locations, castle)

    # The lighthouse is parented to the dragon room because its puzzles are dependent on reaching the dragon first
    populate_region(multiworld, player, CandyBox2Region("The Lighthouse", player, multiworld, "The Lighthouse"), lighthouse_locations, dragon_room)

    _, hell_quest_entrance = populate_region(multiworld, player, CandyBox2Region("Hell", player, multiworld, "Hell"), hell_locations, dragon_room, lambda state: state.has("Black Magic Grimoire", player) and state.has("Boots of Introspection", player) and state.has("Enchanted Monkey Wizard Staff", player))
    mark_quest_entrance(world, hell_quest_entrance, "Hell Room Click")

    _, the_developer_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Developer Quest", player, multiworld, "The Developer Quest"), the_developer_fight_locations, dragon_room, lambda state: weapon_is_at_least(state, player, "Scythe") and state.has("The Sorceress' Cauldron", player) and state.has("Xinopherydon Claw", player))
    mark_quest_entrance(world, the_developer_quest_entrance, "The Developer Quest Click")

    # The Desert Fortress
    desert_fortress, _ = populate_region(multiworld, player, CandyBox2Region("The Desert Fortress", player, multiworld, "The Desert Fortress"), desert_fortress_locations, world_map_1, lambda state: state.has("Desert Fortress Key", player))

    _, xinopherydron_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Xinopherydron Quest", player, multiworld, "The Xinopherydron Quest"), xinopherydron_quest_locations, desert_fortress, lambda state: state.has("Enchanted Monkey Wizard Staff", player) or state.has("Octopus King Crown with Jaspers", player))
    mark_quest_entrance(world, xinopherydron_quest_entrance, "The Xinopherydron Quest Click")

    _, teapot_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Teapot Quest", player, multiworld, "The Teapot Quest"), teapot_quest_locations, desert_fortress, lambda state: weapon_is_at_least(state, player, "Scythe") and state.has("Octopus King Crown with Obsidian", player) and state.has("The Sorceress' Cauldron", player) and state.has("Xinopherydon Claw", player))
    mark_quest_entrance(world, teapot_quest_entrance, "The Teapot Quest Click")

    _, ledge_room_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The Ledge Room Quest", player, multiworld, "The Ledge Room Quest"), ledge_room_quest_locations, desert_fortress, lambda state: (state.has("Octopus King Crown with Obsidian", player) and state.has("The Pogo Stick", player) and (state.has("A desert bird feather", player) or state.has("Rocket Boots", player))))
    mark_quest_entrance(world, ledge_room_quest_entrance, "The Ledge Room Quest Click")

    # X Potion region
    _, x_potion_quest_entrance = populate_region(multiworld, player, CandyBox2Region("The X Potion Quest", player, multiworld, "The X Potion Quest"), yourself_fight_locations, candy_box, lambda state: state.has("The Sorceress' Cauldron", player) and state.has("The Octopus King Crown", player))
    mark_x_quest_entrance(world, x_potion_quest_entrance, "The X Potion Quest Click")

def populate_region(world: MultiWorld, player: int, region: CandyBox2Region, locations: dict[str, int], parent: Region | None, rule: Optional[Callable[[CollectionState], bool]] = None):
    region.locations += [CandyBox2Location(player, location_name, locations[location_name], region) for location_name in locations]
    world.regions.append(region)
    entrance = None
    if parent is not None:
        entrance = parent.connect(region, None, rule)

    return region, entrance

def mark_quest_entrance(world, entrance: Entrance, name: str):
    world.original_entrances.append((name, entrance.connected_region.name))
    if world.options.quest_randomisation == "off":
        return

    entrance.name = name
    entrance.randomization_group = Groups.QUESTS
    disconnect_entrance_for_randomization(entrance, Groups.QUESTS)

def mark_x_quest_entrance(world, entrance: Entrance, name: str):
    world.original_entrances.append((name, entrance.connected_region.name))
    if world.options.quest_randomisation == "off":
        return

    entrance.name = name
    entrance.randomization_group = Groups.X_QUEST
    disconnect_entrance_for_randomization(entrance, Groups.X_QUEST)

def connect_entrances(world):
    if world.options.quest_randomisation == "off":
        return

    if world.options.quest_randomisation == "except_x_potion_quest":
        world.entrance_randomisation = randomize_entrances(world, True, {
            Groups.QUESTS.value: [Groups.QUESTS.value],
            Groups.X_QUEST.value: [Groups.X_QUEST.value],
        })

    if world.options.quest_randomisation == "everything":
        world.entrance_randomisation = randomize_entrances(world, True, {
            Groups.QUESTS.value: [Groups.QUESTS.value, Groups.X_QUEST.value],
            Groups.X_QUEST.value: [Groups.QUESTS.value, Groups.X_QUEST.value],
        })
