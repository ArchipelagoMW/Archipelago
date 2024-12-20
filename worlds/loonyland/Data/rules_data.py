from typing import Dict
from worlds.generic.Rules import CollectionRule
from worlds.loonyland.Rules import *
def set_rules(multiworld, world, player):
    access_rules: Dict[str, CollectionRule] = {
        "Swamp: Mud Path": lambda state: state.has("Boots", player),
        "Swamp: Sapling Shrine": lambda state: state.has("Boots", player),
        "Rocky Cliffs: Vine": lambda state: state.has("Fertilizer", player),
        "Rocky Cliffs: Rock Corner": lambda state: have_bombs(state, player),
        "Witch's Cabin: Bedroom": lambda state: have_light_source(state, player),
        "Bog Pit: Top Door": lambda state: state.has("Skull Key", player),
        "Tunnel: Swampdog Pumpkin Door": lambda state: state.has("Pumpkin Key", player),
        "Tunnel: Scratch Wall": lambda state: have_special_weapon_bullet(state, player),
        "Tunnel: Torch Island": lambda state: state.has("Boots", player),
        "Swamp Gas: Scratch Wall": lambda state: have_special_weapon_bullet(state, player),
        "Swamp Gas: Bat Door": lambda state: state.has("Bat Key", player),
        "Swamp Gas: Rock Prison": lambda state: have_bombs(state, player),
        "Dusty Crypt: Pumpkin Door": lambda state: state.has("Pumpkin Key", player),
        "Musty Crypt: Maze Room": lambda state: have_special_weapon_bullet(state, player),
        "Rusty Crypt: Vine": lambda state: state.has("Fertilizer", player),
        "Under The Lake: Bat Door": lambda state: state.has("Bat Key", player),
        "Tower: Barracks": lambda state: state.has("Ghost Potion", player),
        "Tower F2: Skull Puzzle": lambda state: state.has("Ghost Potion", player),
        "Tower Basement: DoorDoorDoorDoorDoorDoor": lambda state: state.has("Bat Key", player) and state.has("Skull Key", player) and state.has("Pumpkin Key", player),
        "Wolf Den: Pumpkin Door": lambda state: state.has("Pumpkin Key", player),
        "Wolf Den: Vine": lambda state: state.has("Fertilizer", player),
        "Under The Ravine: Left Vine": lambda state: state.has("Fertilizer", player),
        "Under The Ravine: Right Vine": lambda state: state.has("Fertilizer", player),
        "Creepy Caverns M: Pharaoh Bat Door": lambda state: state.has("Bat Key", player),
        "Castle Vampy IV: Ballroom Right": lambda state: state.has("Ghost Potion", player) and state.has("Silver Sling", player),
        "Castle Vampy IV: Ballroom Left": lambda state: state.has("Ghost Potion", player) and state.has("Silver Sling", player),
        "Roof NW: Gutsy the Elder": lambda state: have_special_weapon_damage(state, player),
        "Hidey-Hole: Bat Door": lambda state: state.has("Bat Key", player),
        "Swampdog Lair: Entrance": lambda state: state.has("Boots", player),
        "Swampdog Lair: End": lambda state: state.has("Boots", player) and have_light_source(state, player) and state.has("Fertilizer", player),
        "Q: Scaredy Cat": lambda state: state.has("Cat", player),
        "Q: Mushroom Hunt": lambda state: state.has("Mushroom", player, 10),
        "Q: Zombie Stomp": lambda state: can_cleanse_crypts(state, player),
        "Q: Smashing Pumpkins": lambda state: can_cleanse_crypts(state, player),
        "Q: Silver Bullet": lambda state: can_cleanse_crypts(state, player) and state.has("Silver", player),
        "Q: Hairy Larry": lambda state: have_light_source(state, player) and state.has("Silver Sling", player) and state.has("Boots", player),
        "Q: Ghostbusting": lambda state: state.has("Doom Daisy", player) and state.has("Mushroom", player, 10),
        "Q: The Collection": lambda state: state.has("Silver Sling", player) and state.has("Ghost Potion", player) and can_enter_vampy(state, player),
    }
    for loc in multiworld.get_locations(player):
        if loc.name in access_rules:
            add_rule(loc, access_rules[loc.name])