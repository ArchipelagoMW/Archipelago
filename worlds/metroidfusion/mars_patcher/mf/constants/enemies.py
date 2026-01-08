from enum import Enum


class EnemyType(Enum):
    CRAWLING = 1
    GROUND = 2
    CEILING = 3
    GROUND_CEILING = 4
    WALL = 5
    FLYING = 6


ENEMY_TYPES = {
    0x12: ("Hornoad", EnemyType.GROUND),
    0x13: ("Halzyn", EnemyType.FLYING),
    0x14: ("Zebesian (wall)", EnemyType.WALL),
    0x15: ("Hornoad spawner", EnemyType.GROUND),
    0x18: ("Moto", EnemyType.GROUND),
    0x1B: ("Yameba", EnemyType.FLYING),
    0x31: ("Zeela", EnemyType.CRAWLING),
    0x33: ("Skree (unused)", EnemyType.CEILING),
    0x37: ("Zombie", EnemyType.GROUND),
    0x39: ("Geemer", EnemyType.CRAWLING),
    0x3B: ("Waver", EnemyType.FLYING),
    0x3C: ("Sciser", EnemyType.CRAWLING),
    0x3D: ("Sidehopper", EnemyType.GROUND_CEILING),
    0x3E: ("Dessgeega", EnemyType.GROUND_CEILING),
    0x5A: ("Zoro", EnemyType.CRAWLING),
    0x5B: ("Kihunter (flying)", EnemyType.FLYING),
    0x5C: ("Kihunter (ground)", EnemyType.GROUND),
    0x5E: ("Reo", EnemyType.FLYING),
    0x60: ("Namihe", EnemyType.WALL),
    0x61: ("Fune", EnemyType.WALL),
    0x63: ("Blue zoro", EnemyType.CRAWLING),
    0x64: ("Geruda", EnemyType.FLYING),
    0x6A: ("Skultera (large)", EnemyType.FLYING),
    0x6B: ("Skultera (small, cannot become large)", EnemyType.FLYING),
    0x6C: ("Sova", EnemyType.CRAWLING),
    0x6D: ("Yard", EnemyType.CRAWLING),
    0x6E: ("Evir", EnemyType.FLYING),
    0x6F: ("Bull", EnemyType.FLYING),
    0x70: ("Memu", EnemyType.FLYING),
    0x71: ("Geruboss", EnemyType.CEILING),
    0x72: ("Choot", EnemyType.GROUND),
    0x73: ("Zebesian (ground)", EnemyType.GROUND),
    0x88: ("Ripper", EnemyType.FLYING),
    0xA3: ("Red Zeela", EnemyType.CRAWLING),
    0xA4: ("Owtch", EnemyType.CRAWLING),
    0xA8: ("Genesis", EnemyType.GROUND),
    0xA9: ("Puyo", EnemyType.GROUND),
    0xAD: ("Fake energy tank", EnemyType.GROUND),
    0xAE: ("Fake missile tank", EnemyType.GROUND),
    0xB3: ("Zebesian (aqua)", EnemyType.FLYING),
    0xB4: ("Zebesian (pre-aqua)", EnemyType.GROUND),
    0xB5: ("Skultera (small)", EnemyType.FLYING),
    0xBD: ("Powamp", EnemyType.FLYING),
    0xBE: ("Zozoro", EnemyType.CRAWLING),
}
