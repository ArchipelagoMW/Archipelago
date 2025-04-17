from enum import IntEnum, StrEnum
from typing import Callable, Optional, TYPE_CHECKING, Dict

from BaseClasses import Region, MultiWorld, Entrance, CollectionState
from entrance_rando import disconnect_entrance_for_randomization, randomize_entrances, ERPlacementState
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
    desert_fortress_locations, teapot_quest_locations, xinopherydon_quest_locations, ledge_room_quest_locations, \
    castle_trap_room_locations, squirrel_tree_locations, the_sea_locations, lonely_house_locations, dig_spot_locations, \
    yourself_fight_locations, castle_dark_room_locations, castle_bakehouse_locations
from .rules import weapon_is_at_least, armor_is_at_least, chocolate_count, can_farm_candies, can_grow_lollipops, \
    has_weapon

if TYPE_CHECKING:
    from . import CandyBox2World

class CandyBox2RandomizationGroup(IntEnum):
    QUEST = 1
    X_QUEST = 2
    ROOM = 3

class CandyBox2Room(StrEnum):
    QUEST_THE_CELLAR = "THE_CELLAR"
    QUEST_THE_DESERT = "THE_DESERT"
    QUEST_THE_BRIDGE = "THE_BRIDGE"
    QUEST_THE_OCTOPUS_KING = "THE_OCTOPUS_KING"
    QUEST_THE_NAKED_MONKEY_WIZARD = "THE_NAKED_MONKEY_WIZARD"
    QUEST_THE_SEA = "THE_SEA"
    QUEST_THE_FOREST = "THE_FOREST"
    QUEST_THE_CASTLE_ENTRANCE = "THE_CASTLE_ENTRANCE"
    QUEST_THE_HOLE = "THE_HOLE"
    QUEST_THE_GIANT_NOUGAT_MONSTER = "THE_GIANT_NOUGAT_MONSTER"
    QUEST_THE_CASTLE_TRAP_ROOM = "THE_CASTLE_TRAP_ROOM"
    QUEST_THE_CASTLE_EGG_ROOM = "THE_CASTLE_EGG_ROOM"
    QUEST_HELL = "HELL"
    QUEST_THE_DEVELOPER = "THE_DEVELOPER"
    QUEST_THE_XINOPHERYDON = "THE_XINOPHERYDON"
    QUEST_THE_TEAPOT = "THE_TEAPOT"
    QUEST_THE_LEDGE_ROOM = "THE_LEDGE_ROOM"
    QUEST_THE_X_POTION = "THE_X_POTION"


class CandyBox2Region(Region):
    def __init__(self, name: str, player: int, multiworld: MultiWorld, hint: Optional[str] = None):
        super().__init__(name, player, multiworld, hint)

entrance_friendly_names: Dict[CandyBox2Room, str] = {
    CandyBox2Room.QUEST_THE_CELLAR: "Quest: The Cellar",
    CandyBox2Room.QUEST_THE_DESERT: "Quest: The Desert",
    CandyBox2Room.QUEST_THE_BRIDGE: "Quest: The Bridge",
    CandyBox2Room.QUEST_THE_OCTOPUS_KING: "Quest: The Octopus King",
    CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD: "Quest: The Naked Monkey Wizard",
    CandyBox2Room.QUEST_THE_SEA: "Quest: The Sea",
    CandyBox2Room.QUEST_THE_FOREST: "Quest: The Forest",
    CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE: "Quest: The Castle Entrance",
    CandyBox2Room.QUEST_THE_HOLE: "Quest: The Hole",
    CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER: "Quest: The Giant Nougat Monster",
    CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM: "Quest: The Castle Trap Room",
    CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM: "Quest: The Castle Egg Room",
    CandyBox2Room.QUEST_HELL: "Quest: Hell",
    CandyBox2Room.QUEST_THE_DEVELOPER: "Quest: The Developer",
    CandyBox2Room.QUEST_THE_XINOPHERYDON: "Quest: The Xinopherydon",
    CandyBox2Room.QUEST_THE_TEAPOT: "Quest: The Teapot",
    CandyBox2Room.QUEST_THE_LEDGE_ROOM: "Quest: The Ledge Room",
    CandyBox2Room.QUEST_THE_X_POTION: "Quest: Drink the X Potion",
}

quests: list[CandyBox2Room] = [
    CandyBox2Room.QUEST_THE_CELLAR,
    CandyBox2Room.QUEST_THE_DESERT,
    CandyBox2Room.QUEST_THE_BRIDGE,
    CandyBox2Room.QUEST_THE_OCTOPUS_KING,
    CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD,
    CandyBox2Room.QUEST_THE_SEA,
    CandyBox2Room.QUEST_THE_FOREST,
    CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE,
    CandyBox2Room.QUEST_THE_HOLE,
    CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER,
    CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM,
    CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM,
    CandyBox2Room.QUEST_HELL,
    CandyBox2Room.QUEST_THE_DEVELOPER,
    CandyBox2Room.QUEST_THE_XINOPHERYDON,
    CandyBox2Room.QUEST_THE_TEAPOT,
    CandyBox2Room.QUEST_THE_LEDGE_ROOM,
]

x_quest: list[CandyBox2Room] = [
    CandyBox2Room.QUEST_THE_X_POTION
]

rooms: list[CandyBox2Room] = [

]

class CandyBox2RoomRegion(CandyBox2Region):
    room: CandyBox2Room
    randomization_group: CandyBox2RandomizationGroup

    def __init__(self, room: CandyBox2Room, player: int, multiworld: MultiWorld):
        super().__init__(entrance_friendly_names[room], player, multiworld, entrance_friendly_names[room])
        self.room = room
        if room in quests:
            self.randomization_group = CandyBox2RandomizationGroup.QUEST
        if room in x_quest:
            self.randomization_group = CandyBox2RandomizationGroup.X_QUEST

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
    castle = populate_region(world, player, CandyBox2Region("The Castle", player, multiworld, "The Castle"), map_stage_6_locations, world_map_5, lambda state: state.has("Progressive World Map", player, 6))
    tower_entrance = populate_region(world, player, CandyBox2Region("The Tower's Entrance", player, multiworld, "The Tower's Entrance"), map_stage_7_locations, castle, lambda state: state.has("Progressive World Map", player, 7))

    # The Village
    populate_region(world, player, CandyBox2Region("Village Shop", player, multiworld, "The shop in the village"), village_shop_locations, village)
    populate_region(world, player, CandyBox2Region("Village House 1", player, multiworld, "The house next to the forge in the village"), village_house_1_locations, village)
    village_house_2 = populate_region(world, player, CandyBox2Region("Village House 2", player, multiworld, "The house with the Cellar quest"), village_house_2_locations, village)

    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CELLAR, player, multiworld), village_cellar_locations, village_house_2, lambda state: weapon_is_at_least(
        world, state, player, "Wooden Sword"))

    forge_1 = populate_region(world, player, CandyBox2Region("The Forge 1", player, multiworld, "The Forge in the village"), forge_1_locations, village)
    forge_2 = populate_region(world, player, CandyBox2Region("The Forge 2", player, multiworld, "The Forge in the village"), forge_2_locations, forge_1)
    forge_3 = populate_region(world, player, CandyBox2Region("The Forge 3", player, multiworld, "The forge in the village"), forge_3_locations, forge_2, lambda state: can_farm_candies(state, player))
    forge_4 = populate_region(world, player, CandyBox2Region("The Forge 4", player, multiworld, "The forge in the village"), forge_4_locations, forge_3, lambda state: can_farm_candies(state, player) and state.has("Progressive World Map", player, 3))
    forge_5 = populate_region(world, player, CandyBox2Region("The Forge 5", player, multiworld, "The forge in the village"), forge_5_locations, forge_4, lambda state: can_farm_candies(state, player) and state.has("Progressive World Map", player, 6))

    # The Squirrel Tree
    populate_region(world, player, CandyBox2Region("A tree", player, multiworld, "The squirrel's tree"), squirrel_tree_locations, world_map_1)

    populate_region(world, player, CandyBox2Region("The Lonely House", player, multiworld, "The Lonely House"), lonely_house_locations, world_map_1)

    # The Desert
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_DESERT, player, multiworld), desert_locations, world_map_1)

    # This is connected to world_map_2 because it is only accessible once you see the stones in the cave
    populate_region(world, player, CandyBox2Region("The Dig Spot", player, multiworld, "The Dig Spot"), dig_spot_locations, world_map_2)

    # The Wishing Well
    wishing_well = populate_region(world, player, CandyBox2Region("The Wishing Well", player, multiworld, "The Wishing Well"), wishing_well_locations, world_map_2, lambda state: chocolate_count(state, player) >= 13)
    populate_region(world, player, CandyBox2Region("The Wishing Well (Unlocked Gloves)", player, multiworld, "The Wishing Well"), wishing_well_glove_locations, wishing_well, lambda state: state.has("Leather Gloves", player))
    populate_region(world, player, CandyBox2Region("The Wishing Well (Unlocked Tribal Spear)", player, multiworld, "The Wishing Well"), wishing_well_tribal_spear_locations, wishing_well, lambda state: has_weapon(world, state, player, "Tribal Spear"))
    populate_region(world, player, CandyBox2Region("The Wishing Well (Unlocked Monkey Wizard Staff)", player, multiworld, "The Wishing Well"), wishing_well_monkey_wizard_staff_locations, wishing_well, lambda state: has_weapon(world, state, player, "Monkey Wizard Staff"))
    populate_region(world, player, CandyBox2Region("The Wishing Well (Unlocked Knight Body Armour)", player, multiworld, "The Wishing Well"), wishing_well_knight_body_armour_locations, wishing_well, lambda state: state.has("Knight Body Armour", player))
    populate_region(world, player, CandyBox2Region("The Wishing Well (Unlocked Octopus King Crown)", player, multiworld, "The Wishing Well"), wishing_well_octopus_king_crown_locations, wishing_well, lambda state: state.has("Octopus King Crown", player))
    populate_region(world, player, CandyBox2Region("The Wishing Well (Unlocked Giant Spoon)", player, multiworld, "The Wishing Well"), wishing_well_giant_spoon_locations, wishing_well, lambda state: has_weapon(world, state, player, "Giant Spoon"))

    # The Cave
    the_cave = populate_region(world, player, CandyBox2Region("The Cave", player, multiworld, "The Cave"), cave_locations, world_map_2)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_OCTOPUS_KING, player, multiworld), octopus_king_locations, the_cave)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD, player, multiworld), naked_monkey_wizard_locations, the_cave)

    # The Bridge
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_BRIDGE, player, multiworld), bridge_locations, world_map_2)
    populate_region(world, player, CandyBox2Region("The Sorceress' Hut", player, multiworld, "The Sorceress' Hut"), sorceress_hut_locations, world_map_3)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_SEA, player, multiworld), the_sea_locations, world_map_4)

    # The Forest
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_FOREST, player, multiworld), forest_locations, world_map_4)

    # The Castle
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE, player, multiworld), castle_entrance_locations, world_map_5)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_HOLE, player, multiworld), hole_locations, world_map_5)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER, player, multiworld), giant_nougat_monster_locations, castle)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM, player, multiworld), castle_trap_room_locations, castle)
    populate_region(world, player, CandyBox2Region("The Dark Room", player, multiworld, "The Dark Room"), castle_dark_room_locations, castle)
    populate_region(world, player, CandyBox2Region("The Castle Bakehouse", player, multiworld, "The Castle Bakehouse"), castle_bakehouse_locations, castle, lambda state: chocolate_count(state, player) >= 13)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM, player, multiworld), castle_egg_room_locations, castle)
    dragon_room = populate_region(world, player, CandyBox2Region("Dragon Room", player, multiworld, "The Dragon Room"), dragon_locations, castle)

    # The lighthouse is parented to the dragon room because its puzzles are dependent on reaching the dragon first
    populate_region(world, player, CandyBox2Region("The Lighthouse", player, multiworld, "The Lighthouse"), lighthouse_locations, dragon_room)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_HELL, player, multiworld), hell_locations, dragon_room)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_DEVELOPER, player, multiworld), the_developer_fight_locations, dragon_room)

    # The Desert Fortress
    desert_fortress = populate_region(world, player, CandyBox2Region("The Desert Fortress", player, multiworld, "The Desert Fortress"), desert_fortress_locations, world_map_1, lambda state: state.has("Desert Fortress Key", player))
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_XINOPHERYDON, player, multiworld), xinopherydon_quest_locations, desert_fortress)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_TEAPOT, player, multiworld), teapot_quest_locations, desert_fortress)
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_LEDGE_ROOM, player, multiworld), ledge_room_quest_locations, desert_fortress)

    # X Potion region
    populate_region(world, player, CandyBox2RoomRegion(CandyBox2Room.QUEST_THE_X_POTION, player, multiworld), yourself_fight_locations, candy_box, lambda state: state.has("Sorceress' Cauldron", player) and can_grow_lollipops(state, player))

def populate_region(world: "CandyBox2World", player: int, region: CandyBox2Region, locations: dict[str, int], parent: Region | None, rule: Optional[Callable[[CollectionState], bool]] = None):
    region.locations += [CandyBox2Location(player, location_name, locations[location_name], region) for location_name in locations]
    world.multiworld.regions.append(region)
    entrance = None
    if parent is not None:
        entrance = parent.connect(region, None, rule)

    if type(region) is CandyBox2RoomRegion:
        mark_room_entrance(world, entrance)

    return region

def mark_room_entrance(world: "CandyBox2World", entrance: Entrance):
    name = entrance.connected_region.room
    world.original_entrances.append((name, name))
    if world.options.quest_randomisation == "off":
        return

    entrance.name = name
    entrance.randomization_group = entrance.connected_region.randomization_group
    disconnect_entrance_for_randomization(entrance, CandyBox2RandomizationGroup.QUEST, name)

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

    if world.options.quest_randomisation == "except_x_potion_quest":
        world.entrance_randomisation = randomize_entrances(world, True, {
            CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value],
            CandyBox2RandomizationGroup.X_QUEST.value: [CandyBox2RandomizationGroup.X_QUEST.value],
        })

    if world.options.quest_randomisation == "everything":
        world.entrance_randomisation = randomize_entrances(world, True, {
            CandyBox2RandomizationGroup.QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value],
            CandyBox2RandomizationGroup.X_QUEST.value: [CandyBox2RandomizationGroup.QUEST.value, CandyBox2RandomizationGroup.X_QUEST.value],
        })

    return world.entrance_randomisation.pairings
