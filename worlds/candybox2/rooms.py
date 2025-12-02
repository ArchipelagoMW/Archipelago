from enum import StrEnum


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

    VILLAGE_SHOP = "VILLAGE_SHOP"
    VILLAGE_MINIGAME = "VILLAGE_MINIGAME"
    VILLAGE_FORGE = "VILLAGE_FORGE"
    VILLAGE_FURNISHED_HOUSE = "VILLAGE_FURNISHED_HOUSE"
    VILLAGE_QUEST_HOUSE = "VILLAGE_QUEST_HOUSE"
    SQUIRREL_TREE = "SQUIRREL_TREE"
    LONELY_HOUSE = "LONELY_HOUSE"
    DIG_SPOT = "DIG_SPOT"
    DESERT_FORTRESS = "DESERT_FORTRESS"
    POGO_STICK_SPOT = "POGO_STICK_SPOT"
    SORCERESS_HUT = "SORCERESS_HUT"
    WISHING_WELL = "WISHING_WELL"
    CAVE = "CAVE"
    PIER = "PIER"
    LIGHTHOUSE = "LIGHTHOUSE"
    HOLE = "HOLE"
    CASTLE = "CASTLE"
    CASTLE_BAKEHOUSE = "CASTLE_BAKEHOUSE"
    CASTLE_DARK_ROOM = "CASTLE_DARK_ROOM"
    DRAGON = "DRAGON"
    TOWER = "TOWER"
    LOLLIPOP_FARM = "LOLLIPOP_FARM"

    # These do not participate in ER
    VILLAGE = "VILLAGE"
    WORLD_MAP = "WORLD_MAP"


entrance_friendly_names: dict[CandyBox2Room, str] = {
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
    CandyBox2Room.VILLAGE_SHOP: "Village: The Shop",
    CandyBox2Room.VILLAGE_MINIGAME: "Village: The Third House",
    CandyBox2Room.VILLAGE_FORGE: "Village: The Forge",
    CandyBox2Room.VILLAGE_FURNISHED_HOUSE: "Village: The Fifth House",
    CandyBox2Room.VILLAGE_QUEST_HOUSE: "Village: The Last House",
    CandyBox2Room.SQUIRREL_TREE: "World Map: The Squirrel's Tree",
    CandyBox2Room.LONELY_HOUSE: "World Map: The Lonely House",
    CandyBox2Room.DIG_SPOT: "World Map: The Secret Dig Spot",
    CandyBox2Room.DESERT_FORTRESS: "World Map: The Desert Fortress",
    CandyBox2Room.POGO_STICK_SPOT: "World Map: The Mountains",
    CandyBox2Room.SORCERESS_HUT: "World Map: The Sorceress' Hut",
    CandyBox2Room.WISHING_WELL: "World Map: The Wishing Well",
    CandyBox2Room.CAVE: "World Map: The Cave",
    CandyBox2Room.PIER: "World Map: The Pier",
    CandyBox2Room.LIGHTHOUSE: "World Map: The Lighthouse",
    CandyBox2Room.HOLE: "World Map: The Hole",
    CandyBox2Room.CASTLE: "World Map: The Castle",
    CandyBox2Room.CASTLE_BAKEHOUSE: "The Castle: The Bakehouse",
    CandyBox2Room.CASTLE_DARK_ROOM: "The Castle: The Dark Room",
    CandyBox2Room.DRAGON: "World Map: The Dragon",
    CandyBox2Room.TOWER: "The Castle: The Tower",
    CandyBox2Room.LOLLIPOP_FARM: "World Map: The Lollipop Farm",
    # Not required, just here to make logic easier
    CandyBox2Room.VILLAGE: "The Village",
    CandyBox2Room.WORLD_MAP: "The World Map",
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
    CandyBox2Room.QUEST_THE_X_POTION,
]

rooms: list[CandyBox2Room] = [
    CandyBox2Room.VILLAGE_SHOP,
    CandyBox2Room.VILLAGE_MINIGAME,
    CandyBox2Room.VILLAGE_FORGE,
    CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
    CandyBox2Room.VILLAGE_QUEST_HOUSE,
    CandyBox2Room.SQUIRREL_TREE,
    CandyBox2Room.LONELY_HOUSE,
    CandyBox2Room.DIG_SPOT,
    CandyBox2Room.DESERT_FORTRESS,
    CandyBox2Room.POGO_STICK_SPOT,
    CandyBox2Room.SORCERESS_HUT,
    CandyBox2Room.WISHING_WELL,
    CandyBox2Room.CAVE,
    CandyBox2Room.PIER,
    CandyBox2Room.LIGHTHOUSE,
    CandyBox2Room.HOLE,
    CandyBox2Room.CASTLE,
    CandyBox2Room.CASTLE_BAKEHOUSE,
    CandyBox2Room.CASTLE_DARK_ROOM,
    CandyBox2Room.DRAGON,
    CandyBox2Room.TOWER,
]
lollipop_farm: list[CandyBox2Room] = [CandyBox2Room.LOLLIPOP_FARM]
