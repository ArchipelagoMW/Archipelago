from typing import List

from .Enums import Character, LevelMission
from .Logic import LevelLocation
from .Options import SonicAdventureDXOptions


def get_playable_character_item(character: Character) -> str:
    from worlds.sadx.Names import ItemName
    return {
        Character.Sonic: ItemName.Sonic.Playable,
        Character.Tails: ItemName.Tails.Playable,
        Character.Knuckles: ItemName.Knuckles.Playable,
        Character.Amy: ItemName.Amy.Playable,
        Character.Big: ItemName.Big.Playable,
        Character.Gamma: ItemName.Gamma.Playable
    }.get(character)


def get_character_upgrades_item(character: Character) -> List[str]:
    from worlds.sadx.Names import ItemName
    return {
        Character.Sonic: [ItemName.Sonic.LightShoes, ItemName.Sonic.CrystalRing, ItemName.Sonic.AncientLight],
        Character.Tails: [ItemName.Tails.JetAnklet, ItemName.Tails.RhythmBadge],
        Character.Knuckles: [ItemName.Knuckles.ShovelClaw, ItemName.Knuckles.FightingGloves],
        Character.Amy: [ItemName.Amy.WarriorFeather, ItemName.Amy.LongHammer],
        Character.Big: [ItemName.Big.LifeBelt, ItemName.Big.PowerRod, ItemName.Big.Lure1, ItemName.Big.Lure2,
                        ItemName.Big.Lure3, ItemName.Big.Lure4],
        Character.Gamma: [ItemName.Gamma.JetBooster, ItemName.Gamma.LaserBlaster]
    }.get(character)


def character_has_capsule_sanity(character: Character, options: SonicAdventureDXOptions) -> bool:
    return {
        Character.Sonic: options.sonic_capsule_sanity,
        Character.Tails: options.tails_capsule_sanity,
        Character.Knuckles: options.knuckles_capsule_sanity,
        Character.Amy: options.amy_capsule_sanity,
        Character.Big: options.big_capsule_sanity,
        Character.Gamma: options.gamma_capsule_sanity
    }.get(character).value > 0


def character_has_enemy_sanity(character: Character, options: SonicAdventureDXOptions) -> bool:
    return {
        Character.Sonic: options.sonic_enemy_sanity,
        Character.Tails: options.tails_enemy_sanity,
        Character.Knuckles: options.knuckles_enemy_sanity,
        Character.Amy: options.amy_enemy_sanity,
        Character.Big: options.big_enemy_sanity,
        Character.Gamma: options.gamma_enemy_sanity
    }.get(character).value > 0


def are_character_upgrades_randomized(character: Character, options: SonicAdventureDXOptions) -> bool:
    return {
        Character.Sonic: options.randomized_sonic_upgrades,
        Character.Tails: options.randomized_tails_upgrades,
        Character.Knuckles: options.randomized_knuckles_upgrades,
        Character.Amy: options.randomized_amy_upgrades,
        Character.Big: options.randomized_big_upgrades,
        Character.Gamma: options.randomized_gamma_upgrades
    }.get(character).value > 0


def is_character_playable(character: Character, options: SonicAdventureDXOptions) -> bool:
    return {
        Character.Sonic: options.playable_sonic,
        Character.Tails: options.playable_tails,
        Character.Knuckles: options.playable_knuckles,
        Character.Amy: options.playable_amy,
        Character.Big: options.playable_big,
        Character.Gamma: options.playable_gamma
    }.get(character).value > 0


def is_any_character_playable(characters: List[Character], options: SonicAdventureDXOptions) -> bool:
    return any(is_character_playable(character, options) for character in characters)


def get_playable_characters(options: SonicAdventureDXOptions) -> List[Character]:
    return [character for character in Character if is_character_playable(character, options)]


def is_level_playable(level: LevelLocation, options: SonicAdventureDXOptions) -> bool:
    if not is_character_playable(level.character, options):
        return False

    character_missions = {
        Character.Sonic: options.sonic_action_stage_missions,
        Character.Tails: options.tails_action_stage_missions,
        Character.Knuckles: options.knuckles_action_stage_missions,
        Character.Amy: options.amy_action_stage_missions,
        Character.Big: options.big_action_stage_missions,
        Character.Gamma: options.gamma_action_stage_missions
    }.get(level.character)

    return (character_missions == 4 and level.levelMission in {LevelMission.C, LevelMission.B, LevelMission.A, LevelMission.S}) or \
        (character_missions == 3 and level.levelMission in {LevelMission.C, LevelMission.B, LevelMission.A}) or \
        (character_missions == 2 and level.levelMission in {LevelMission.C, LevelMission.B}) or \
        (character_missions == 1 and level.levelMission == LevelMission.C)
