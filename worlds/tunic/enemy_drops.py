from enum import IntEnum
from typing import TYPE_CHECKING, NamedTuple

from worlds.generic.Rules import set_rule, add_rule

from .constants import *
from .logic_helpers import (has_melee, has_sword, can_shop, has_ability, has_enemy_soul, has_ladder,
                            has_ice_grapple_logic)
from .options import ShuffleEnemyDrops, IceGrappling

if TYPE_CHECKING:
    from . import TunicWorld


class EnemyType(IntEnum):
    blob = 1
    hedgehog = 2
    rudeling = 3
    rudeling_shield = 4
    guard_captain = 5
    envoy = 6
    beefboy = 7
    phrend = 8
    spider = 9
    autobolt = 10
    tentacle = 11
    baby_slorm = 12
    slorm = 13
    laser_trap = 14
    fairy = 15
    chompignom = 16
    garden_knight = 17
    custodian = 18
    custodian_sword = 19
    custodian_candelabra = 20
    siege_engine = 21
    plover = 22
    crabbit = 23
    crabbo = 24
    crabbit_shell = 25
    husher = 26
    frog_small = 27
    frog = 28
    frog_spear = 29
    librarian = 30
    scavenger = 31
    scavenger_support = 32
    scavenger_miner = 33
    voidling = 34
    administrator = 35
    boss_scavenger = 36
    fleemer = 37
    fleemer_fencer = 38
    fleemer_big = 39
    lost_echo = 40
    gunslinger = 41
    fox_enemy_zombie = 42
    fox_enemy = 43
    voidtouched = 44


class TunicLocationData(NamedTuple):
    er_region: str
    enemy_type: EnemyType
    is_extra_enemy: bool = False
    extra_group: str | None = None


enemy_location_table: dict[str, TunicLocationData] = {
    "Beneath the Fortress - Spider From Entrance": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Lower Room Spider 2": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Lower Room Baby Slorm 1": TunicLocationData("Beneath the Vault Main", EnemyType.baby_slorm),
    "Beneath the Fortress - Lower Room Baby Slorm 2": TunicLocationData("Beneath the Vault Main", EnemyType.baby_slorm),
    "Beneath the Fortress - Lower Room Spider 1": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Dark Hallway Spider 1": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Dark Hallway Spider 2": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Waterfall Room Big Spider 1": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Waterfall Room Spider 2": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Waterfall Room Spider 1": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Spider Behind Waterfall 1": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Spider Behind Waterfall 2": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Corner Room Big Spider": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Corner Room Spider": TunicLocationData("Beneath the Vault Main", EnemyType.spider),
    "Beneath the Fortress - Cell Hallway Custodian": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_sword),
    "Beneath the Fortress - Bottom Right Cell Phrend": TunicLocationData("Beneath the Vault Back", EnemyType.phrend),
    "Beneath the Fortress - Middle Right Cell Baby Slorm": TunicLocationData("Beneath the Vault Back", EnemyType.baby_slorm),
    "Beneath the Fortress - Middle Left Cell Phrend": TunicLocationData("Beneath the Vault Back", EnemyType.phrend),
    "Beneath the Fortress - Fuse Room Custodian 3": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_sword),
    "Beneath the Fortress - Fuse Room Custodian 4": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_sword),
    "Beneath the Fortress - Fuse Room Custodian 2": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_sword),
    "Beneath the Fortress - Fuse Room Custodian 1": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_sword),
    "Beneath the Fortress - Fuse Room Candelabra Custodian": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_candelabra, is_extra_enemy=True),
    "Beneath the Fortress - Cell Hallway Hedgehog Trap 2": TunicLocationData("Beneath the Vault Back", EnemyType.laser_trap, is_extra_enemy=True),
    "Beneath the Fortress - Cell Hallway Hedgehog Trap 1": TunicLocationData("Beneath the Vault Back", EnemyType.laser_trap, is_extra_enemy=True),
    "Beneath the Fortress - Top Left Cell Custodian": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_sword, is_extra_enemy=True),
    "Beneath the Fortress - Lower Room Big Spider": TunicLocationData("Beneath the Vault Main", EnemyType.spider, is_extra_enemy=True),
    "Beneath the Fortress - Waterfall Room Big Spider 2": TunicLocationData("Beneath the Vault Main", EnemyType.spider, is_extra_enemy=True),
    "Beneath the Fortress - Custodian Hiding In Barrel Room": TunicLocationData("Beneath the Vault Back", EnemyType.custodian_sword, is_extra_enemy=True),
    "Beneath the Well - [Entryway] Slorm 1": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Entryway] Rudeling": TunicLocationData("Beneath the Well Main", EnemyType.rudeling),
    "Beneath the Well - [Entryway] Slorm 2": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Second Room] Slorm": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Second Room] Rudeling": TunicLocationData("Beneath the Well Main", EnemyType.rudeling),
    "Beneath the Well - [Third Room] Slorm 2": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Third Room] Slorm 1": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Third Room] Autobolt Near Pots": TunicLocationData("Beneath the Well Main", EnemyType.autobolt),
    "Beneath the Well - [Back Corridor] Slorm 1": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Back Corridor] Slorm 3": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Back Corridor] Slorm 2": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Back Corridor] Slorm 4": TunicLocationData("Beneath the Well Main", EnemyType.slorm),
    "Beneath the Well - [Third Room] Autobolt Behind Three Barrels": TunicLocationData("Beneath the Well Main", EnemyType.autobolt),
    "Beneath the Well - [Third Room] Shield Rudeling Near Table 1": TunicLocationData("Beneath the Well Main", EnemyType.rudeling_shield),
    "Beneath the Well - [Third Room] Shield Rudeling Near Table 2": TunicLocationData("Beneath the Well Main", EnemyType.rudeling_shield),
    "Beneath the Well - [Third Room] Rudeling Near Table": TunicLocationData("Beneath the Well Main", EnemyType.rudeling),
    "Beneath the Well - [Third Room] Shield Rudeling Near Exit Doorway": TunicLocationData("Beneath the Well Main", EnemyType.rudeling_shield),
    "Beneath the Well - [Third Room] Tentacle In Water 2": TunicLocationData("Beneath the Well Main", EnemyType.tentacle),
    "Beneath the Well - [Third Room] Tentacle In Water 1": TunicLocationData("Beneath the Well Main", EnemyType.tentacle),
    "Beneath the Well - [Third Room] Tentacle In Water 4": TunicLocationData("Beneath the Well Main", EnemyType.tentacle),
    "Beneath the Well - [Third Room] Tentacle In Water 3": TunicLocationData("Beneath the Well Main", EnemyType.tentacle),
    "Beneath the Well - [Side Room] Phrend In Corner 3": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend In Corner 1": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend In Corner 2": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend Near Chest 1": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend Near Chest 2": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend Near Chest 4": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend Near Chest 3": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend Near Chest 5": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Side Room] Phrend Near Chest 6": TunicLocationData("Beneath the Well Back", EnemyType.phrend),
    "Beneath the Well - [Third Room] Autobolt Near Back Corridor": TunicLocationData("Beneath the Well Main", EnemyType.autobolt, is_extra_enemy=True),
    "Beneath the Well - [Back Corridor] Slorm 7": TunicLocationData("Beneath the Well Main", EnemyType.slorm, is_extra_enemy=True),
    "Beneath the Well - [Back Corridor] Slorm 6": TunicLocationData("Beneath the Well Main", EnemyType.slorm, is_extra_enemy=True),
    "Beneath the Well - [Back Corridor] Slorm 5": TunicLocationData("Beneath the Well Main", EnemyType.slorm, is_extra_enemy=True),
    "Cathedral - [1F] Zombie Fox Near Elevator 5": TunicLocationData("Cathedral Entry", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Zombie Fox Near Elevator 3": TunicLocationData("Cathedral Entry", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Zombie Fox Near Elevator 4": TunicLocationData("Cathedral Entry", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Zombie Fox Near Elevator 1": TunicLocationData("Cathedral Entry", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Zombie Fox Near Elevator 2": TunicLocationData("Cathedral Entry", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Side Room 2 Hedgehog Trap 1": TunicLocationData("Cathedral Entry", EnemyType.laser_trap),
    "Cathedral - [1F] Side Room 2 Hedgehog Trap 2": TunicLocationData("Cathedral Entry", EnemyType.laser_trap),
    "Cathedral - [1F] Side Room 1 Zombie Fox": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Side Room 2 Zombie Fox 1": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Side Room 2 Zombie Fox 2": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Side Room 2 Zombie Fox 3": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Purple Room Zombie Fox 1": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Purple Room Zombie Fox 2": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Purple Room Zombie Fox 3": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Purple Room Strong Zombie Fox": TunicLocationData("Cathedral Main", EnemyType.fox_enemy),
    "Cathedral - [1F] Purple Room Upper Zombie Fox": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [1F] Spike Room Zombie Fox": TunicLocationData("Cathedral Main", EnemyType.fox_enemy_zombie),
    "Cathedral - [2F] Void Husher 1": TunicLocationData("Cathedral Main", EnemyType.husher),
    "Cathedral - [2F] Void Husher 2": TunicLocationData("Cathedral Main", EnemyType.husher),
    "Cathedral - [2F] Void Husher 3": TunicLocationData("Cathedral Main", EnemyType.husher),
    "Cathedral - [2F] Void Husher 5": TunicLocationData("Cathedral Main", EnemyType.husher),
    "Cathedral - [2F] Void Husher 4": TunicLocationData("Cathedral Main", EnemyType.husher),
    "Cathedral - [2F] Back Hallway Hedgehog Trap 1": TunicLocationData("Cathedral Main", EnemyType.laser_trap),
    "Cathedral - [2F] Left Room Strong Zombie Fox 2": TunicLocationData("Cathedral Main", EnemyType.fox_enemy),
    "Cathedral - [2F] Back Hallway Hedgehog Trap 2": TunicLocationData("Cathedral Main", EnemyType.laser_trap),
    "Cathedral - [2F] Left Room Strong Zombie Fox 1": TunicLocationData("Cathedral Main", EnemyType.fox_enemy),
    "Cathedral - [2F] Back Hallway Hedgehog Trap 5": TunicLocationData("Cathedral Main", EnemyType.laser_trap),
    "Cathedral - [2F] Back Hallway Hedgehog Trap 4": TunicLocationData("Cathedral Main", EnemyType.laser_trap),
    "Cathedral - [2F] Back Hallway Hedgehog Trap 3": TunicLocationData("Cathedral Main", EnemyType.laser_trap),
    "Cathedral - [2F] Above Entrance Beefboy": TunicLocationData("Cathedral Main", EnemyType.beefboy, is_extra_enemy=True, extra_group="Minibosses"),
    "Cathedral - [2F] Sacrifice Room Voidtouched": TunicLocationData("Cathedral Main", EnemyType.voidtouched, is_extra_enemy=True, extra_group="Minibosses"),
    "Cathedral Gauntlet - Zombie Fox 2": TunicLocationData("Cathedral Gauntlet", EnemyType.fox_enemy_zombie, is_extra_enemy=True),
    "Cathedral Gauntlet - Strong Zombie Fox": TunicLocationData("Cathedral Gauntlet", EnemyType.fox_enemy, is_extra_enemy=True),
    "Cathedral Gauntlet - Zombie Fox 1": TunicLocationData("Cathedral Gauntlet", EnemyType.fox_enemy_zombie, is_extra_enemy=True),
    "Cathedral Gauntlet - Rudeling Wave Rudeling 1": TunicLocationData("Cathedral Gauntlet", EnemyType.rudeling),
    "Cathedral Gauntlet - Rudeling Wave Rudeling 2": TunicLocationData("Cathedral Gauntlet", EnemyType.rudeling),
    "Cathedral Gauntlet - Rudeling Wave Rudeling 3": TunicLocationData("Cathedral Gauntlet", EnemyType.rudeling),
    "Cathedral Gauntlet - Rudeling Wave Guard Captain": TunicLocationData("Cathedral Gauntlet", EnemyType.guard_captain),
    "Cathedral Gauntlet - Rudeling Wave Shield Rudeling 1": TunicLocationData("Cathedral Gauntlet", EnemyType.rudeling_shield),
    "Cathedral Gauntlet - Rudeling Wave Shield Rudeling 2": TunicLocationData("Cathedral Gauntlet", EnemyType.rudeling_shield),
    "Cathedral Gauntlet - Rudeling Wave Shield Rudeling 3": TunicLocationData("Cathedral Gauntlet", EnemyType.rudeling_shield),
    "Cathedral Gauntlet - Frog Wave Small Frog 1": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Small Frog 2": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Small Frog 3": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Small Frog 4": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Small Frog 5": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Shield Frog 1": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_spear),
    "Cathedral Gauntlet - Frog Wave Small Frog 6": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Small Frog 7": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Small Frog 8": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Small Frog 9": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_small),
    "Cathedral Gauntlet - Frog Wave Shield Frog 2": TunicLocationData("Cathedral Gauntlet", EnemyType.frog_spear),
    "Cathedral Gauntlet - Garden Knight Wave 1": TunicLocationData("Cathedral Gauntlet", EnemyType.garden_knight, extra_group="Minibosses"),
    "Cathedral Gauntlet - Garden Knight Wave 2": TunicLocationData("Cathedral Gauntlet", EnemyType.garden_knight, extra_group="Minibosses"),
    "Cathedral Gauntlet - Wizard Custodian Wave 1": TunicLocationData("Cathedral Gauntlet", EnemyType.custodian),
    "Cathedral Gauntlet - Wizard Custodian Wave 5": TunicLocationData("Cathedral Gauntlet", EnemyType.custodian),
    "Cathedral Gauntlet - Wizard Custodian Wave 3": TunicLocationData("Cathedral Gauntlet", EnemyType.custodian),
    "Cathedral Gauntlet - Wizard Custodian Wave 2": TunicLocationData("Cathedral Gauntlet", EnemyType.custodian),
    "Cathedral Gauntlet - Wizard Custodian Wave 4": TunicLocationData("Cathedral Gauntlet", EnemyType.custodian),
    "Cathedral Gauntlet - Fleemer Wave 1": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 2": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 3": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 4": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 5": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 6": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 7": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 8": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 9": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 10": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 11": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 12": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 13": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 14": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fleemer Wave 15": TunicLocationData("Cathedral Gauntlet", EnemyType.fleemer),
    "Cathedral Gauntlet - Fairy Wave 1": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 2": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 4": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 6": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 7": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 8": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 10": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 11": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 15": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 12": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 3": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 5": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 17": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 16": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 14": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 13": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Cathedral Gauntlet - Fairy Wave 9": TunicLocationData("Cathedral Gauntlet", EnemyType.fairy),
    "Dark Tomb - Spike Hallway Fleemer 1": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Spike Hallway Fleemer 2": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Spike Hallway Fleemer 3": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Skulls Room Right Fleemer 1": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Skulls Room Phrend 4": TunicLocationData("Dark Tomb Upper", EnemyType.phrend),
    "Dark Tomb - Skulls Room Phrend 5": TunicLocationData("Dark Tomb Upper", EnemyType.phrend),
    "Dark Tomb - Skulls Room Right Fleemer 2": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Skulls Room Right Fleemer 3": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Skulls Room Left Fleemer 1": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Skulls Room Left Fleemer 2": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer),
    "Dark Tomb - Skulls Room Phrend 2": TunicLocationData("Dark Tomb Upper", EnemyType.phrend),
    "Dark Tomb - Skulls Room Phrend 3": TunicLocationData("Dark Tomb Upper", EnemyType.phrend),
    "Dark Tomb - Skulls Room Phrend 1": TunicLocationData("Dark Tomb Upper", EnemyType.phrend),
    "Dark Tomb - Spike Maze Fleemer 1": TunicLocationData("Dark Tomb Main", EnemyType.fleemer),
    "Dark Tomb - Spike Maze Fleemer 2": TunicLocationData("Dark Tomb Main", EnemyType.fleemer),
    "Dark Tomb - Spike Maze Fleemer 3": TunicLocationData("Dark Tomb Main", EnemyType.fleemer),
    "Dark Tomb - Spike Maze Fleemer 4": TunicLocationData("Dark Tomb Main", EnemyType.fleemer),
    "Dark Tomb - Spike Maze Fleemer 5": TunicLocationData("Dark Tomb Main", EnemyType.fleemer),
    "Dark Tomb - Hallway Hedgehog Trap 1": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Fleemer Between Hedgehog Traps": TunicLocationData("Dark Tomb Main", EnemyType.fleemer),
    "Dark Tomb - Hallway Hedgehog Trap 2": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Hallway Hedgehog Trap 3": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Statue Room Hedgehog Trap 1": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Statue Room Hedgehog Trap 2": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Statue Room Hedgehog Trap 3": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Statue Room Fleemer 1": TunicLocationData("Dark Tomb Main", EnemyType.fleemer),
    "Dark Tomb - Statue Room Hedgehog Trap Along Wall": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 1": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 2": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 6": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 7": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 4": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 5": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 8": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 9": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 11": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 12": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 10": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Laser Room Hedgehog Trap 3": TunicLocationData("Dark Tomb Main", EnemyType.laser_trap),
    "Dark Tomb - Statue Room Fleemer 2": TunicLocationData("Dark Tomb Main", EnemyType.fleemer, is_extra_enemy=True),
    "Dark Tomb - Fleemer Quartet 4": TunicLocationData("Dark Tomb Main", EnemyType.fleemer, is_extra_enemy=True),
    "Dark Tomb - Fleemer Quartet 3": TunicLocationData("Dark Tomb Main", EnemyType.fleemer, is_extra_enemy=True),
    "Dark Tomb - Fleemer Quartet 2": TunicLocationData("Dark Tomb Main", EnemyType.fleemer, is_extra_enemy=True),
    "Dark Tomb - Fleemer Quartet 1": TunicLocationData("Dark Tomb Main", EnemyType.fleemer, is_extra_enemy=True),
    "Dark Tomb - Spike Hallway Fleemer 4": TunicLocationData("Dark Tomb Upper", EnemyType.fleemer, is_extra_enemy=True),
    "Dark Tomb Checkpoint - [Well Boss] Rudeling 2": TunicLocationData("Well Boss", EnemyType.rudeling),
    "Dark Tomb Checkpoint - [Well Boss] Rudeling 1": TunicLocationData("Well Boss", EnemyType.rudeling),
    "Dark Tomb Checkpoint - [Well Boss] Guard Captain": TunicLocationData("Well Boss", EnemyType.guard_captain),
    "Dark Tomb Checkpoint - [Well Boss] Envoy": TunicLocationData("Well Boss", EnemyType.envoy, is_extra_enemy=True),
    "East Forest - Hedgehog Near Dance Fox Spot 1": TunicLocationData("East Forest Dance Fox Spot", EnemyType.hedgehog),
    "East Forest - Hedgehog Near Dance Fox Spot 2": TunicLocationData("East Forest Dance Fox Spot", EnemyType.hedgehog),
    "East Forest - Hedgehog 1": TunicLocationData("East Forest", EnemyType.hedgehog),
    "East Forest - Hedgehog 2": TunicLocationData("East Forest", EnemyType.hedgehog),
    "East Forest - Hedgehog 3": TunicLocationData("East Forest", EnemyType.hedgehog),
    "East Forest - Blob 3": TunicLocationData("East Forest", EnemyType.blob),
    "East Forest - Blob 2": TunicLocationData("East Forest", EnemyType.blob),
    "East Forest - Blob 4": TunicLocationData("East Forest", EnemyType.blob),
    "East Forest - Blob 1": TunicLocationData("East Forest", EnemyType.blob),
    "East Forest - Blob 5": TunicLocationData("East Forest", EnemyType.blob),
    "East Forest - Hedgehog 4": TunicLocationData("East Forest", EnemyType.hedgehog),
    "East Forest - Shield Rudeling Above Guardhouse 2": TunicLocationData("East Forest above Guard House 2", EnemyType.rudeling_shield),
    "East Forest - Envoy Above Guardhouse 2": TunicLocationData("East Forest above Guard House 2", EnemyType.envoy),
    "East Forest - Rudeling Above Guardhouse 2": TunicLocationData("East Forest above Guard House 2", EnemyType.rudeling),
    "East Forest - Rudeling Above Checkpoint": TunicLocationData("East Forest", EnemyType.rudeling),
    "East Forest - Rudeling Near Obscured Chest 1": TunicLocationData("East Forest", EnemyType.rudeling),
    "East Forest - Rudeling Facing Guardhouse Gate": TunicLocationData("East Forest", EnemyType.rudeling),
    "East Forest - Rudeling Near Gate Switch 1": TunicLocationData("East Forest", EnemyType.rudeling),
    "East Forest - Rudeling Near Gate Switch 2": TunicLocationData("East Forest", EnemyType.rudeling),
    "East Forest - Ice Grapple Blob": TunicLocationData("Lower Forest", EnemyType.blob),
    "East Forest - [Lower] Spider Near Grapple Hook": TunicLocationData("Lower Forest", EnemyType.spider),
    "East Forest - [Lower] Spider Behind Top Right Tree": TunicLocationData("Lower Forest", EnemyType.spider),
    "East Forest - [Lower] Spider Behind Bottom Left Tree": TunicLocationData("Lower Forest", EnemyType.spider),
    "East Forest - [Lower] Spider Behind Bottom Right Tree": TunicLocationData("Lower Forest", EnemyType.spider),
    "East Forest - [Lower] Spider Behind Top Left Tree": TunicLocationData("Lower Forest", EnemyType.spider),
    "East Forest - [Lower] Rudeling Near Broken Obelisk 2": TunicLocationData("Lower Forest", EnemyType.rudeling),
    "East Forest - [Lower] Rudeling Near Broken Obelisk 1": TunicLocationData("Lower Forest", EnemyType.rudeling),
    "East Forest - [Lower] Big Spider In Clearing": TunicLocationData("Lower Forest", EnemyType.spider, is_extra_enemy=True),
    "East Forest - Big Spider Atop Ladders": TunicLocationData("East Forest", EnemyType.spider, is_extra_enemy=True),
    "East Forest - Rudeling Near Obscured Chest 3": TunicLocationData("East Forest", EnemyType.rudeling, is_extra_enemy=True),
    "East Forest - Rudeling Near Obscured Chest 2": TunicLocationData("East Forest", EnemyType.rudeling, is_extra_enemy=True),
    "East Forest - Rudeling Near Obscured Chest 4": TunicLocationData("East Forest", EnemyType.rudeling, is_extra_enemy=True),
    "East Forest - Rudeling Outside Guardhouse 1": TunicLocationData("East Forest", EnemyType.rudeling, is_extra_enemy=True),
    "Eastern Vault Fortress - [West Wing] Hedgehog Trap Near Stairs 1": TunicLocationData("Eastern Vault Fortress", EnemyType.laser_trap, is_extra_enemy=True),
    "Eastern Vault Fortress - [West Wing] Hedgehog Trap Near Stairs 2": TunicLocationData("Eastern Vault Fortress", EnemyType.laser_trap, is_extra_enemy=True),
    "Eastern Vault Fortress - [West Wing] Side Room Baby Slorm 1": TunicLocationData("Eastern Vault Fortress", EnemyType.baby_slorm),
    "Eastern Vault Fortress - [West Wing] Side Room Baby Slorm 2": TunicLocationData("Eastern Vault Fortress", EnemyType.baby_slorm),
    "Eastern Vault Fortress - [West Wing] Side Room Baby Slorm 3": TunicLocationData("Eastern Vault Fortress", EnemyType.baby_slorm),
    "Eastern Vault Fortress - [West Wing] Upper Floor Custodian 1": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [West Wing] Upper Floor Custodian 2": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [West Wing] Lower Floor Custodian 1": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [West Wing] Lower Floor Candelabra Custodian 1": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_candelabra),
    "Eastern Vault Fortress - [West Wing] Lower Floor Custodian 2": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [West Wing] Lower Floor Custodian 3": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [Main Room] Left Custodian": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [Main Room] Right Custodian": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [Main Room] Candelabra Custodian": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_candelabra),
    "Eastern Vault Fortress - [Main Room] Upper Ledge Custodian": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian),
    "Eastern Vault Fortress - [West Wing] Custodian Hiding In Corner 1": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword),
    "Eastern Vault Fortress - [West Wing] Lower Floor Candelabra Custodian 2": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_candelabra, is_extra_enemy=True),
    "Eastern Vault Fortress - [West Wing] Custodian Hiding In Corner 2": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword, is_extra_enemy=True),
    "Eastern Vault Fortress - [West Wing] Custodian Hiding In Corner 3": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword, is_extra_enemy=True),
    "Eastern Vault Fortress - [West Wing] Upper Floor Custodian 3": TunicLocationData("Eastern Vault Fortress", EnemyType.custodian_sword, is_extra_enemy=True),
    "Forest Belltower - Blob 3": TunicLocationData("Forest Belltower Main", EnemyType.blob),
    "Forest Belltower - Blob 4": TunicLocationData("Forest Belltower Main", EnemyType.blob),
    "Forest Belltower - Blob 2": TunicLocationData("Forest Belltower Main", EnemyType.blob),
    "Forest Belltower - Blob 1": TunicLocationData("Forest Belltower Main", EnemyType.blob),
    "Forest Belltower - Blob Near Ladder": TunicLocationData("Forest Belltower Main", EnemyType.blob),
    "Forest Boss Room - Top Left Rudeling": TunicLocationData("Forest Boss Room", EnemyType.rudeling),
    "Forest Boss Room - Guard Captain": TunicLocationData("Forest Boss Room", EnemyType.guard_captain, extra_group="Bosses"),
    "Forest Boss Room - Bottom Left Rudeling": TunicLocationData("Forest Boss Room", EnemyType.rudeling, is_extra_enemy=True),
    "Forest Boss Room - Bottom Right Rudeling": TunicLocationData("Forest Boss Room", EnemyType.rudeling, is_extra_enemy=True),
    "Forest Boss Room - Top Right Rudeling": TunicLocationData("Forest Boss Room", EnemyType.rudeling, is_extra_enemy=True),
    "Forest Grave Path - Big Blog Near Entrance 1": TunicLocationData("Forest Grave Path Main", EnemyType.blob),
    "Forest Grave Path - Big Blog Near Entrance 2": TunicLocationData("Forest Grave Path Main", EnemyType.blob),
    "Forest Grave Path - Hedgehog On Side Path": TunicLocationData("Forest Grave Path Main", EnemyType.hedgehog),
    "Forest Grave Path - Hedgehog On Ramp": TunicLocationData("Forest Grave Path Main", EnemyType.hedgehog),
    "Forest Grave Path - Hedgehog Atop Stairs": TunicLocationData("Forest Grave Path Main", EnemyType.hedgehog),
    "Forest Grave Path - Rudeling Guarding Gate": TunicLocationData("Forest Grave Path Main", EnemyType.rudeling),
    "Forest Grave Path - Zombie Fox On Grave": TunicLocationData("Forest Grave Path by Grave", EnemyType.fox_enemy_zombie, is_extra_enemy=True),
    "Forest Grave Path - Scavenger On Stairs": TunicLocationData("Forest Grave Path Main", EnemyType.scavenger, is_extra_enemy=True),
    "Forest Grave Path - Scavenger On Side Path": TunicLocationData("Forest Grave Path Main", EnemyType.scavenger, is_extra_enemy=True),
    "Forest Grave Path - Scavenger On Back Stairs": TunicLocationData("Forest Grave Path Main", EnemyType.scavenger_support, is_extra_enemy=True),
    "Forest Grave Path - Scavenger Guarding Gate Left": TunicLocationData("Forest Grave Path Main", EnemyType.scavenger, is_extra_enemy=True),
    "Forest Grave Path - Scavenger Guarding Gate Right": TunicLocationData("Forest Grave Path Main", EnemyType.scavenger, is_extra_enemy=True),
    "Forest Grave Path - Strong Zombie Fox On Grave": TunicLocationData("Forest Grave Path by Grave", EnemyType.fox_enemy, is_extra_enemy=True),
    "Fortress Arena - Defeat Siege Engine": TunicLocationData("Fortress Arena", EnemyType.siege_engine, extra_group="Bosses"),
    "Fortress Courtyard - [Upper] Custodian Near East Entrance": TunicLocationData("Fortress Courtyard Upper", EnemyType.custodian_sword),
    "Fortress Courtyard - [Upper] Custodian Near Fuse": TunicLocationData("Fortress Courtyard Upper", EnemyType.custodian_sword),
    "Fortress Courtyard - [Upper] Candelabra Custodian": TunicLocationData("Fortress Courtyard Upper", EnemyType.custodian_candelabra),
    "Fortress Courtyard - Custodian Left Of Fuse": TunicLocationData("Fortress Courtyard", EnemyType.custodian_sword),
    "Fortress Courtyard - Custodian Right Of Fuse": TunicLocationData("Fortress Courtyard", EnemyType.custodian_sword),
    "Fortress Courtyard - Candelabra Custodian Near Fuse": TunicLocationData("Fortress Courtyard", EnemyType.custodian_candelabra),
    "Fortress Courtyard - Wizard Custodian Guarding Bridge": TunicLocationData("Fortress Courtyard", EnemyType.custodian),
    "Fortress East Shortcut - [Lower] Blob 2": TunicLocationData("Fortress East Shortcut Lower", EnemyType.blob),
    "Fortress East Shortcut - [Lower] Blob 4": TunicLocationData("Fortress East Shortcut Lower", EnemyType.blob),
    "Fortress East Shortcut - [Lower] Blob 1": TunicLocationData("Fortress East Shortcut Lower", EnemyType.blob),
    "Fortress East Shortcut - [Lower] Blob 3": TunicLocationData("Fortress East Shortcut Lower", EnemyType.blob),
    "Fortress East Shortcut - [Upper] Wizard Custodian 1": TunicLocationData("Fortress East Shortcut Upper", EnemyType.custodian),
    "Fortress East Shortcut - [Upper] Wizard Custodian 2": TunicLocationData("Fortress East Shortcut Upper", EnemyType.custodian),
    "Fortress East Shortcut - [Upper] Wizard Custodian 4": TunicLocationData("Fortress East Shortcut Upper", EnemyType.custodian_sword),
    "Fortress East Shortcut - [Upper] Wizard Custodian 3": TunicLocationData("Fortress East Shortcut Upper", EnemyType.custodian),
    "Fortress East Shortcut - [Upper] Candelabra Custodian 1": TunicLocationData("Fortress East Shortcut Upper", EnemyType.custodian_candelabra),
    "Fortress East Shortcut - [Upper] Candelabra Custodian 2": TunicLocationData("Fortress East Shortcut Upper", EnemyType.custodian_candelabra, is_extra_enemy=True),
    "Fortress Grave Path - Front Left Custodian": TunicLocationData("Fortress Grave Path Combat", EnemyType.custodian_sword),
    "Fortress Grave Path - Front Right Custodian": TunicLocationData("Fortress Grave Path Combat", EnemyType.custodian_sword),
    "Fortress Grave Path - Front Wizard Custodian": TunicLocationData("Fortress Grave Path Combat", EnemyType.custodian),
    "Fortress Grave Path - Back Right Custodian": TunicLocationData("Fortress Grave Path Combat", EnemyType.custodian_sword),
    "Fortress Grave Path - Back Left Custodian": TunicLocationData("Fortress Grave Path Combat", EnemyType.custodian_sword),
    "Fortress Grave Path - Back Wizard Custodian": TunicLocationData("Fortress Grave Path Combat", EnemyType.custodian),
    "Fortress Grave Path - Zombie Fox Near Grave": TunicLocationData("Fortress Grave Path by Grave", EnemyType.fox_enemy_zombie, is_extra_enemy=True),
    "Fortress Grave Path - Back Right Voidling Spider": TunicLocationData("Fortress Grave Path Combat", EnemyType.voidling, is_extra_enemy=True),
    "Fortress Grave Path - Back Left Voidling Spider": TunicLocationData("Fortress Grave Path Combat", EnemyType.voidling, is_extra_enemy=True),
    "Fortress Grave Path - Front Voidling Spider": TunicLocationData("Fortress Grave Path Combat", EnemyType.voidling, is_extra_enemy=True),
    "Frog Stairway - [Upper] Shield Frog": TunicLocationData("Frog Stairs Upper", EnemyType.frog_spear),
    "Frog Stairway - [Lower] Small Frog": TunicLocationData("Frog Stairs Lower", EnemyType.frog_small),
    "Frog's Domain - Escape Room Autobolt": TunicLocationData("Frog's Domain Back", EnemyType.autobolt),
    "Frog's Domain - Hot Tub Frog 1": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Hot Tub Frog 2": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Hot Tub Frog 3": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Side Room Frog 1": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Side Room Frog 3": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Side Room Frog 2": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Frog Patrolling Hallway": TunicLocationData("Frog's Domain Main", EnemyType.frog),
    "Frog's Domain - Main Room Entrance Patrolling Frog": TunicLocationData("Frog's Domain Main", EnemyType.frog),
    "Frog's Domain - Main Room Frog Near Chest": TunicLocationData("Frog's Domain Main", EnemyType.frog),
    "Frog's Domain - Main Room Near Ladder Patrolling Frog": TunicLocationData("Frog's Domain Main", EnemyType.frog),
    "Frog's Domain - Main Room Lower Small Frog 1": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Main Room Lower Small Frog 4": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Main Room Lower Small Frog 3": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Main Room Lower Small Frog 2": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Main Room Baby Slorm Jail 4": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Main Room Baby Slorm Jail 3": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Main Room Baby Slorm Jail 2": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Main Room Baby Slorm Jail 1": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Main Room Shield Frog 2": TunicLocationData("Frog's Domain Main", EnemyType.frog_spear),
    "Frog's Domain - Main Room Shield Frog 1": TunicLocationData("Frog's Domain Main", EnemyType.frog_spear),
    "Frog's Domain - Baby Slorm Room 5": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 2": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 8": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 6": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 4": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 1": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 7": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 3": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 9": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room Frog": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Baby Slorm Room 12": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 10": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 13": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Baby Slorm Room 11": TunicLocationData("Frog's Domain Main", EnemyType.baby_slorm),
    "Frog's Domain - Orb Room Small Frog 4": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Orb Room Big Frog": TunicLocationData("Frog's Domain Main", EnemyType.frog),
    "Frog's Domain - Orb Room Small Frog 3": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Orb Room Small Frog 5": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Orb Room Small Frog 2": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Orb Room Small Frog 6": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Orb Room Small Frog 1": TunicLocationData("Frog's Domain Main", EnemyType.frog_small),
    "Frog's Domain - Orb Room Wizard Custodian 1": TunicLocationData("Frog's Domain Main", EnemyType.custodian),
    "Frog's Domain - Side Room Secret Frog": TunicLocationData("Frog's Domain Main", EnemyType.frog_small, is_extra_enemy=True),
    "Frog's Domain - Main Room Upper Small Frog 1": TunicLocationData("Frog's Domain Main", EnemyType.frog_small, is_extra_enemy=True),
    "Frog's Domain - Main Room Upper Small Frog 2": TunicLocationData("Frog's Domain Main", EnemyType.frog_small, is_extra_enemy=True),
    "Frog's Domain - Main Room Upper Small Frog 3": TunicLocationData("Frog's Domain Main", EnemyType.frog_small, is_extra_enemy=True),
    "Frog's Domain - Main Room Upper Small Frog 4": TunicLocationData("Frog's Domain Main", EnemyType.frog_small, is_extra_enemy=True),
    "Frog's Domain - Main Room Lower Small Frog 5": TunicLocationData("Frog's Domain Main", EnemyType.frog_small, is_extra_enemy=True),
    "Frog's Domain - Orb Room Wizard Custodian 2": TunicLocationData("Frog's Domain Main", EnemyType.custodian, is_extra_enemy=True),
    "Guardhouse 1 - Blob 8": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Blob 6": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Blob 5": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Blob 7": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Blob 2": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Blob 1": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Blob 4": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Blob 3": TunicLocationData("Guard House 1 West", EnemyType.blob),
    "Guardhouse 1 - Hedgehog": TunicLocationData("Guard House 1 West", EnemyType.hedgehog),
    "Guardhouse 2 - Blob 2": TunicLocationData("Guard House 2 Lower", EnemyType.blob),
    "Guardhouse 2 - Blob 3": TunicLocationData("Guard House 2 Lower", EnemyType.blob),
    "Guardhouse 2 - Blob 1": TunicLocationData("Guard House 2 Lower", EnemyType.blob),
    "Guardhouse 2 - Rudeling 1": TunicLocationData("Guard House 2 Lower", EnemyType.rudeling),
    "Guardhouse 2 - Rudeling 2": TunicLocationData("Guard House 2 Lower", EnemyType.rudeling),
    "Hourglass Cave - Autobolt 1": TunicLocationData("Hourglass Cave", EnemyType.autobolt),
    "Hourglass Cave - Autobolt 3": TunicLocationData("Hourglass Cave", EnemyType.autobolt),
    "Hourglass Cave - Autobolt 2": TunicLocationData("Hourglass Cave", EnemyType.autobolt),
    "Librarian - Defeat Librarian": TunicLocationData("Library Arena", EnemyType.librarian, extra_group="Bosses"),
    "Library Hall - Right Beefboy": TunicLocationData("Library Hall", EnemyType.beefboy, extra_group="Minibosses"),
    "Library Hall - Left Beefboy": TunicLocationData("Library Hall", EnemyType.beefboy, extra_group="Minibosses"),
    "Library Hall - Administrator Coffee Table": TunicLocationData("Library Hall", EnemyType.administrator),
    "Monastery - [Front] Scavenger Miner Near Entrance": TunicLocationData("Monastery Front", EnemyType.scavenger_miner),
    "Monastery - [Front] Upper Path Scavenger Sniper": TunicLocationData("Monastery Front", EnemyType.scavenger),
    "Monastery - [Front] Upper Path Scavenger Miner": TunicLocationData("Monastery Front", EnemyType.scavenger_miner),
    "Monastery - [Front] Scavenger Sniper Guarding Gate": TunicLocationData("Monastery Front", EnemyType.scavenger),
    "Monastery - [Front] Scavenger Mining Broken Fuse 2": TunicLocationData("Monastery Front", EnemyType.scavenger_miner),
    "Monastery - [Front] Scavenger Mining Broken Fuse 1": TunicLocationData("Monastery Front", EnemyType.scavenger_miner),
    "Monastery - [Front] Scavenger Sniper Near Entrance": TunicLocationData("Monastery Front", EnemyType.scavenger),
    "Monastery - [Back] Zombie Fox Near Grave": TunicLocationData("Monastery Back", EnemyType.fox_enemy_zombie, is_extra_enemy=True),
    "Monastery - [Back] Voidtouched": TunicLocationData("Monastery Back", EnemyType.voidtouched, extra_group="Minibosses"),
    "Monastery - [Front] Voidling Spider 1": TunicLocationData("Monastery Front", EnemyType.voidling, is_extra_enemy=True),
    "Monastery - [Front] Voidling Spider 2": TunicLocationData("Monastery Front", EnemyType.voidling, is_extra_enemy=True),
    "Monastery - [Front] Voidling Spider 3": TunicLocationData("Monastery Front", EnemyType.voidling, is_extra_enemy=True),
    "Monastery - [Front] Upper Path Voidling Spider": TunicLocationData("Monastery Front", EnemyType.voidling, is_extra_enemy=True),
    "Overworld - [Central] Blob Near Ruined Passage Door": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [Central] Blob Near Cube Cave 1": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [Central] Blob Near Cube Cave 2": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [Central] Blob Near Cube Cave 3": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [Central] Big Blob Near Checkpoint": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [Central] Blob Near Checkpoint 1": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [Central] Blob Near Checkpoint 2": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [Central] Blob Near Checkpoint 3": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [West] Rudeling Near Well": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [West] Rudeling Near Old House": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [West] Hedgehog Near Teleporter 1": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [West] Hedgehog Near Teleporter 2": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [West] Rudeling On Teleporter": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [West] Hedgehog Near Tuning Fork": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [West] Rudeling Near Teleporter": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [West] Hedgehog Near Water 1": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [West] Hedgehog Near Water 2": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [West] Rudeling Near Water": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [West] Big Blob Above Ruined Shop": TunicLocationData("Overworld", EnemyType.blob),
    "Overworld - [West] Hedgehog Above Ruined Shop": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [Southwest] Hedgehog Left of Fountain": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [Southwest] Rudeling Near Ruined Shop": TunicLocationData("Overworld", EnemyType.rudeling_shield),
    "Overworld - [Southwest] Rudeling Patrolling Fountain": TunicLocationData("Overworld", EnemyType.rudeling_shield),
    "Overworld - [Southwest] Hedgehog Near Stairs 1": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [Southwest] Hedgehog Near Stairs 2": TunicLocationData("Overworld", EnemyType.hedgehog),
    "Overworld - [Southwest] Shield Rudeling Above Envoy": TunicLocationData("Overworld", EnemyType.rudeling_shield),
    "Overworld - [Southwest] Rudeling Right of Stairs": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [Southwest] Rudeling Left of Stairs": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [Southwest] Autobolt Near Trees": TunicLocationData("Overworld", EnemyType.autobolt),
    "Overworld - [Southwest] Envoy Guarding Item": TunicLocationData("Overworld", EnemyType.envoy),
    "Overworld - [West] Autobolt Near Moss Wall": TunicLocationData("Overworld", EnemyType.autobolt),
    "Overworld - [Northwest] Envoy On Bridge To Quarry": TunicLocationData("Overworld", EnemyType.envoy),
    "Overworld - [Southwest] Autobolt In Tunnel": TunicLocationData("Overworld Tunnel Turret", EnemyType.autobolt),
    "Overworld - [Southwest] Shield Rudeling Guarding Chest": TunicLocationData("Overworld", EnemyType.rudeling_shield),
    "Overworld - [Northwest] Phrend Near Waterfall 2": TunicLocationData("Overworld", EnemyType.phrend),
    "Overworld - [Northwest] Phrend Near Waterfall 1": TunicLocationData("Overworld", EnemyType.phrend),
    "Overworld - [Northwest] Shield Rudeling Near Dark Tomb": TunicLocationData("Overworld", EnemyType.rudeling_shield),
    "Overworld - [Northwest] Rudeling Near Chest 2": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [Northwest] Rudeling Near Chest 1": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [Northwest] Shield Rudeling Near Rubble": TunicLocationData("Overworld", EnemyType.rudeling_shield),
    "Overworld - [Northwest] Shield Rudeling On Bridge To Well": TunicLocationData("Overworld", EnemyType.rudeling_shield),
    "Overworld - [Northwest] Rudeling On Bridge To Well": TunicLocationData("Overworld", EnemyType.rudeling),
    "Overworld - [Northwest] Autobolt On Bridge To Well": TunicLocationData("Overworld", EnemyType.autobolt),
    "Overworld - [East] Blob After Ruined Passage 3": TunicLocationData("After Ruined Passage", EnemyType.blob),
    "Overworld - [East] Blob After Ruined Passage 1": TunicLocationData("After Ruined Passage", EnemyType.blob),
    "Overworld - [East] Blob After Ruined Passage 2": TunicLocationData("After Ruined Passage", EnemyType.blob),
    "Overworld - [East] Blob Near Pots 1": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Blob Near Pots 2": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Blob Near Pots 4": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Blob Near Pots 3": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Blob in Bushes 1": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Blob in Bushes 2": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Blob in Bushes 3": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Blob in Bushes 4": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [East] Hedgehog 1": TunicLocationData("East Overworld", EnemyType.hedgehog),
    "Overworld - [East] Hedgehog 2": TunicLocationData("East Overworld", EnemyType.hedgehog),
    "Overworld - [East] Hedgehog 3": TunicLocationData("East Overworld", EnemyType.hedgehog),
    "Overworld - [Northeast] Big Blob Near Flowers 3": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [Northeast] Big Blob Near Flowers 1": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [Northeast] Big Blob Near Flowers 4": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [Northeast] Big Blob Near Flowers 5": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [Northeast] Big Blob Near Flowers 2": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [Northeast] Big Blob Near Extending Bridge": TunicLocationData("East Overworld", EnemyType.blob),
    "Overworld - [Northeast] Hedgehog Above Patrol Cave 1": TunicLocationData("Overworld above Patrol Cave", EnemyType.hedgehog),
    "Overworld - [Northeast] Hedgehog Above Patrol Cave 2": TunicLocationData("Overworld above Patrol Cave", EnemyType.hedgehog),
    "Overworld - [Northeast] Shield Rudeling Above Patrol Cave 2": TunicLocationData("Upper Overworld", EnemyType.rudeling_shield),
    "Overworld - [Northeast] Shield Rudeling Above Patrol Cave 3": TunicLocationData("Upper Overworld", EnemyType.rudeling_shield),
    "Overworld - [Northeast] Shield Rudeling Above Patrol Cave 1": TunicLocationData("Upper Overworld", EnemyType.rudeling_shield),
    "Overworld - [Central] Phrend Above Temple 6": TunicLocationData("Upper Overworld", EnemyType.phrend),
    "Overworld - [Central] Phrend Above Temple 5": TunicLocationData("Upper Overworld", EnemyType.phrend),
    "Overworld - [Central] Phrend Above Temple 4": TunicLocationData("Upper Overworld", EnemyType.phrend),
    "Overworld - [Central] Phrend Above Temple 1": TunicLocationData("Upper Overworld", EnemyType.phrend),
    "Overworld - [Central] Phrend Above Temple 2": TunicLocationData("Upper Overworld", EnemyType.phrend),
    "Overworld - [Central] Phrend Above Temple 3": TunicLocationData("Upper Overworld", EnemyType.phrend),
    "Overworld - [Northwest] Guard Captain Near Telescope": TunicLocationData("Upper Overworld", EnemyType.guard_captain),
    "Overworld - [Southwest] Autobolt On Beach": TunicLocationData("Overworld Beach", EnemyType.autobolt),
    "Overworld - [Southwest] Autobolt Guarding Chest Near Wear": TunicLocationData("Overworld Beach", EnemyType.autobolt),
    "Overworld - [Southwest] Autobolt Guarding Chest On Island": TunicLocationData("Overworld Beach", EnemyType.autobolt),
    "Overworld - [Southwest] Guard Captain On Stairs": TunicLocationData("Overworld", EnemyType.guard_captain, is_extra_enemy=True),
    "Overworld - [Southwest] Beefboy": TunicLocationData("Overworld", EnemyType.beefboy, is_extra_enemy=True, extra_group="Minibosses"),
    "Overworld - [Central] Big Blob On Spawn Bridge": TunicLocationData("Overworld", EnemyType.blob, is_extra_enemy=True),
    "Overworld - [Southeast] Big Fleemer Near Holy Cross Door": TunicLocationData("Overworld", EnemyType.fleemer_big, is_extra_enemy=True, extra_group="Minibosses"),
    "Overworld - [East] Zombie Fox After Ruined Passage": TunicLocationData("After Ruined Passage", EnemyType.fox_enemy_zombie, is_extra_enemy=True),
    "Overworld - [East] Blob Hiding by Stairs": TunicLocationData("East Overworld", EnemyType.blob, is_extra_enemy=True),
    "Overworld - [Northwest] Rudeling Near Fire Pit": TunicLocationData("Overworld", EnemyType.rudeling, is_extra_enemy=True),
    "Overworld - [Northwest] Shield Rudeling Guarding Chest Near Well": TunicLocationData("Overworld", EnemyType.rudeling_shield, is_extra_enemy=True),
    "Patrol Cave - Patrolling Rudeling": TunicLocationData("Patrol Cave", EnemyType.rudeling),
    "Quarry - [South] Scavenger Miner Near Entrance Checkpoint 1": TunicLocationData("Quarry", EnemyType.scavenger_miner),
    "Quarry - [South] Scavenger Miner Near Entrance Checkpoint 2": TunicLocationData("Quarry", EnemyType.scavenger_miner),
    "Quarry - [South] Scavenger Sniper Near Entrance Checkpoint": TunicLocationData("Quarry", EnemyType.scavenger),
    "Quarry - [Central] Scavenger Between Broken Fuses": TunicLocationData("Quarry", EnemyType.scavenger_support),
    "Quarry - [Central] Scavenger Support By Broken Fuse": TunicLocationData("Quarry", EnemyType.scavenger_support),
    "Quarry - [Central] Scavenger Mining Broken Fuse": TunicLocationData("Quarry", EnemyType.scavenger_miner),
    "Quarry - [Central] Scavenger Sniper Looking Down": TunicLocationData("Quarry", EnemyType.scavenger),
    "Quarry - [East] Scavenger Near Bombable Wall": TunicLocationData("Quarry", EnemyType.scavenger_support),
    "Quarry - [East] Scavenger Miner 1": TunicLocationData("Quarry", EnemyType.scavenger_miner),
    "Quarry - [East] Scavenger Miner 2": TunicLocationData("Quarry", EnemyType.scavenger_miner),
    "Quarry - [East] Scavenger Sniper": TunicLocationData("Quarry", EnemyType.scavenger),
    "Quarry - [East] Scavenger On Ramps": TunicLocationData("Quarry", EnemyType.scavenger_support),
    "Quarry - [East] Scavenger Sniper Near Obscured Chest": TunicLocationData("Quarry", EnemyType.scavenger),
    "Quarry - [East] Highest Ladder Scavenger Sniper": TunicLocationData("Quarry", EnemyType.scavenger),
    "Quarry - [Central] Scavenger Miner Outside Monastery": TunicLocationData("Quarry", EnemyType.scavenger_miner),
    "Quarry - [Central] Scavenger Sniper Outside Monastery 1": TunicLocationData("Quarry", EnemyType.scavenger),
    "Quarry - [Central] Scavenger Sniper Outside Monastery 2": TunicLocationData("Quarry", EnemyType.scavenger),
    "Quarry - [Central] Scavenger Outside Monastery": TunicLocationData("Quarry", EnemyType.scavenger_support),
    "Quarry - [West] Scavenger Miner Trio 1": TunicLocationData("Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [West] Scavenger Miner Trio 2": TunicLocationData("Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [West] Scavenger Miner Trio 3": TunicLocationData("Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [West] Scavenger Support Below Fire Pots": TunicLocationData("Lower Quarry", EnemyType.scavenger_support),
    "Quarry - [West] Scavenger Support Near Cliff": TunicLocationData("Lower Quarry", EnemyType.scavenger_support),
    "Quarry - [West] Scavenger Miner Near Shooting Range": TunicLocationData("Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [West] Shooting Range Scavenger Sniper 1": TunicLocationData("Lower Quarry", EnemyType.scavenger),
    "Quarry - [West] Shooting Range Scavenger Sniper 2": TunicLocationData("Lower Quarry", EnemyType.scavenger),
    "Quarry - [West] Shooting Range Scavenger Sniper 3": TunicLocationData("Lower Quarry", EnemyType.scavenger),
    "Quarry - [West] Lower Quarry Scavenger Near Boxes": TunicLocationData("Lower Quarry", EnemyType.scavenger_support),
    "Quarry - [Lowlands] Scavenger Miner 1": TunicLocationData("Even Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [Lowlands] Scavenger Guarding Chest": TunicLocationData("Even Lower Quarry", EnemyType.scavenger_support),
    "Quarry - [Lowlands] Scavenger Sniper On Scaffolding 2": TunicLocationData("Lower Quarry", EnemyType.scavenger),
    "Quarry - [Lowlands] Scavenger Sniper On Pillar": TunicLocationData("Even Lower Quarry", EnemyType.scavenger),
    "Quarry - [Lowlands] Scavenger Miner 3": TunicLocationData("Even Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [Lowlands] Scavenger Sniper On Scaffolding 1": TunicLocationData("Lower Quarry", EnemyType.scavenger),
    "Quarry - [Lowlands] Scavenger Miner 4": TunicLocationData("Even Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [Lowlands] Scavenger Miner 2": TunicLocationData("Even Lower Quarry", EnemyType.scavenger_miner),
    "Quarry - [Central] Scavenger Miner Hiding In Wall": TunicLocationData("Quarry", EnemyType.scavenger_miner),
    "Rooted Ziggurat Lower - Voidling Spider 1": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Voidling Spider 3": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Voidling Spider 2": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Right Autobolt 1": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.autobolt),
    "Rooted Ziggurat Lower - Right Autobolt 2": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.autobolt),
    "Rooted Ziggurat Lower - Left Autobolt 1": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.autobolt),
    "Rooted Ziggurat Lower - Left Autobolt 2": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.autobolt),
    "Rooted Ziggurat Lower - Voidling Spider 4": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Voidling Spider 5": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Voidling Spider 7": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Voidling Spider 6": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Voidling Spider 8": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Square Platform Autobolt 1": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.autobolt),
    "Rooted Ziggurat Lower - Square Platform Autobolt 2": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.autobolt),
    "Rooted Ziggurat Lower - Administrator 2": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.administrator, extra_group="Minibosses"),
    "Rooted Ziggurat Lower - Administrator 2 2nd Phase": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.administrator, extra_group="Minibosses"),
    "Rooted Ziggurat Lower - Fuse Platform Voidling Spider 2": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Fuse Platform Voidling Spider 1": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.voidling),
    "Rooted Ziggurat Lower - Administrator 1": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.administrator, extra_group="Minibosses"),
    "Rooted Ziggurat Lower - Administrator 1 2nd Phase": TunicLocationData("Rooted Ziggurat Lower Front", EnemyType.administrator, extra_group="Minibosses"),
    "Rooted Ziggurat Lower - Defeat Boss Scavenger": TunicLocationData("Rooted Ziggurat Lower Back", EnemyType.boss_scavenger, extra_group="Bosses"),
    "Rooted Ziggurat Upper - Fairy Swarm Fairy 5": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Fairy Swarm Fairy 4": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Fairy Swarm Fairy 1": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Fairy Swarm Fairy 3": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Fairy Swarm Fairy 2": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Wall Between Stairs Fairy 3": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Wall Between Stairs Fairy 2": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Wall Between Stairs Fairy 1": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Turret Path Autobolt 1": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.autobolt),
    "Rooted Ziggurat Upper - Turret Path Autobolt 2": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.autobolt),
    "Rooted Ziggurat Upper - Turret Path Autobolt 4": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.autobolt),
    "Rooted Ziggurat Upper - Turret Path Autobolt 3": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.autobolt),
    "Rooted Ziggurat Upper - Turret Path Autobolt 5": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.autobolt),
    "Rooted Ziggurat Upper - Turret Path Fairy 2": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Turret Path Fairy 1": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.fairy),
    "Rooted Ziggurat Upper - Administrator": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.administrator, extra_group="Minibosses"),
    "Rooted Ziggurat Upper - Administrator 2nd Phase": TunicLocationData("Rooted Ziggurat Upper Front", EnemyType.administrator, extra_group="Minibosses"),
    "Ruined Atoll - [North] Plover Near Lower Entrance": TunicLocationData("Ruined Atoll Lower Entry Area", EnemyType.plover),
    "Ruined Atoll - [North] Crabbit In Water 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [North] Crabbit In Water 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [West] Crabbit By Left Stairs 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [West] Crabbit By Left Stairs 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [West] Crabbit By Left Stairs 3": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [West] Plover Near Stairs": TunicLocationData("Ruined Atoll", EnemyType.plover),
    "Ruined Atoll - [West] Plover Near Teleporter Statue": TunicLocationData("Ruined Atoll", EnemyType.plover),
    "Ruined Atoll - [North] Husher Perched On Chest": TunicLocationData("Ruined Atoll", EnemyType.husher),
    "Ruined Atoll - [East] Crabbit By Right Stairs 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [East] Crabbit By Right Stairs 3": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [East] Crabbit By Right Stairs 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Northwest] Small Frog Below Fuse": TunicLocationData("Ruined Atoll", EnemyType.frog_small),
    "Ruined Atoll - [Northwest] Frog Near Fuse 1": TunicLocationData("Ruined Atoll", EnemyType.frog),
    "Ruined Atoll - [Northwest] Frog Near Fuse 2": TunicLocationData("Ruined Atoll", EnemyType.frog),
    "Ruined Atoll - [South] Sunken Tower Fairy 1": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [South] Sunken Tower Fairy 2": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [Northwest] Envoy Guarding Chest": TunicLocationData("Ruined Atoll", EnemyType.envoy),
    "Ruined Atoll - [Northwest] Small Frog Above Ruins": TunicLocationData("Ruined Atoll", EnemyType.frog_small),
    "Ruined Atoll - [West] Sunken Tower Fairy 1": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [West] Sunken Tower Fairy 2": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [West] Sunken Tower Fairy 3": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [Southwest] Burrowed Slorm 2": TunicLocationData("Ruined Atoll", EnemyType.slorm),
    "Ruined Atoll - [Southwest] Burrowed Slorm 1": TunicLocationData("Ruined Atoll", EnemyType.slorm),
    "Ruined Atoll - [Southwest] Burrowed Slorm 3": TunicLocationData("Ruined Atoll", EnemyType.slorm),
    "Ruined Atoll - [Southwest] Baby Slorm Pair 1": TunicLocationData("Ruined Atoll", EnemyType.baby_slorm),
    "Ruined Atoll - [Southwest] Baby Slorm Pair 2": TunicLocationData("Ruined Atoll", EnemyType.baby_slorm),
    "Ruined Atoll - [Southwest] Crabbit Surrounding Baby Slorm 6": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Southwest] Crabbit Surrounding Baby Slorm 5": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Southwest] Crabbit Surrounding Baby Slorm 4": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Southwest] Crabbit Surrounding Baby Slorm 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Southwest] Crabbit Surrounding Baby Slorm 3": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Southwest] Baby Slorm Surrounded By Crabbits": TunicLocationData("Ruined Atoll", EnemyType.baby_slorm),
    "Ruined Atoll - [Southwest] Crabbit Surrounding Baby Slorm 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Southwest] Husher Perched On Broken Conduit": TunicLocationData("Ruined Atoll", EnemyType.husher),
    "Ruined Atoll - [Southwest] Plover By Fuse": TunicLocationData("Ruined Atoll", EnemyType.plover),
    "Ruined Atoll - [South] Husher Guarding Gate 1": TunicLocationData("Ruined Atoll", EnemyType.husher),
    "Ruined Atoll - [South] Husher Guarding Gate 2": TunicLocationData("Ruined Atoll", EnemyType.husher),
    "Ruined Atoll - [Southeast] Crabbo Near Ocean": TunicLocationData("Ruined Atoll", EnemyType.crabbo),
    "Ruined Atoll - [Southeast] Burrowed Slorm 1": TunicLocationData("Ruined Atoll", EnemyType.slorm),
    "Ruined Atoll - [Southeast] Burrowed Slorm 2": TunicLocationData("Ruined Atoll", EnemyType.slorm),
    "Ruined Atoll - [Southeast] Crabbo Near Conduits": TunicLocationData("Ruined Atoll", EnemyType.crabbo),
    "Ruined Atoll - [East] Past Ruined House Crabbit 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [East] Past Ruined House Crabbit 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [East] Past Ruined House Crabbit 3": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [East] Burrowed Slorm By Ruined House": TunicLocationData("Ruined Atoll", EnemyType.slorm),
    "Ruined Atoll - [Northeast] Crabbit Near Mountain 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Northeast] Crabbit Near Mountain 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Northeast] Crabbit Near Mountain 3": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Northeast] Crabbit Near Brick Path 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Northeast] Crabbit Near Brick Path 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit),
    "Ruined Atoll - [Southwest] Fairy Near Fuse 1": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [Southwest] Fairy Near Fuse 2": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [Southeast] Fairy Guarding Fuse 3": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [Southeast] Fairy Guarding Fuse 2": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [Southeast] Fairy Guarding Fuse 1": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [Southeast] Fairy Guarding Fuse 4": TunicLocationData("Ruined Atoll", EnemyType.fairy),
    "Ruined Atoll - [West] Crabbit With Cube Shell": TunicLocationData("Ruined Atoll", EnemyType.crabbit_shell, is_extra_enemy=True),
    "Ruined Atoll - [Northeast] Crabbit With Cube Shell": TunicLocationData("Ruined Atoll", EnemyType.crabbit_shell, is_extra_enemy=True),
    "Ruined Atoll - [Southeast] Crabbit Guarding Crabbo 1": TunicLocationData("Ruined Atoll", EnemyType.crabbit, is_extra_enemy=True),
    "Ruined Atoll - [Southeast] Crabbit Guarding Crabbo 2": TunicLocationData("Ruined Atoll", EnemyType.crabbit, is_extra_enemy=True),
    "Ruined Atoll - [Southeast] Crabbit Guarding Crabbo 4": TunicLocationData("Ruined Atoll", EnemyType.crabbit, is_extra_enemy=True),
    "Ruined Atoll - [Southeast] Crabbit Guarding Crabbo 3": TunicLocationData("Ruined Atoll", EnemyType.crabbit, is_extra_enemy=True),
    "Ruined Atoll - [Southeast] Crabbit Guarding Crabbo 5": TunicLocationData("Ruined Atoll", EnemyType.crabbit, is_extra_enemy=True),
    "Ruined Atoll - [Southeast] Crabbit Guarding Crabbo 6": TunicLocationData("Ruined Atoll", EnemyType.crabbit, is_extra_enemy=True),
    "Ruined Atoll - [Southeast] Crabbit Guarding Crabbo 7": TunicLocationData("Ruined Atoll", EnemyType.crabbit, is_extra_enemy=True),
    "Swamp - [Entrance] Right Gunslinger": TunicLocationData("Swamp Front", EnemyType.gunslinger),
    "Swamp - [Entrance] Left Gunslinger": TunicLocationData("Swamp Front", EnemyType.gunslinger),
    "Swamp - [Entrance] Fleemer By Fence 1": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [Entrance] Fleemer By Fence 2": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Fleemer 1": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Fleemer 2": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Big Fleemer": TunicLocationData("Swamp Front", EnemyType.fleemer_big, extra_group="Minibosses"),
    "Swamp - [South Graveyard] Fleemer 3": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Fleemer 4": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Fleemer 5": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Island Tentacle 3": TunicLocationData("Swamp Front", EnemyType.tentacle),
    "Swamp - [South Graveyard] Island Tentacle 2": TunicLocationData("Swamp Front", EnemyType.tentacle),
    "Swamp - [South Graveyard] Island Tentacle 1": TunicLocationData("Swamp Front", EnemyType.tentacle),
    "Swamp - [South Graveyard] Lost Echo": TunicLocationData("Swamp Front", EnemyType.lost_echo),
    "Swamp - [South Graveyard] Upper Path Gunslinger": TunicLocationData("Swamp Front", EnemyType.gunslinger),
    "Swamp - [South Graveyard] Upper Path Fleemer 1": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Upper Path Lost Echo": TunicLocationData("Swamp Front", EnemyType.lost_echo),
    "Swamp - [South Graveyard] Upper Path Fleemer Fencer": TunicLocationData("Swamp Front", EnemyType.fleemer_fencer),
    "Swamp - [South Graveyard] Upper Path Fleemer 2": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [South Graveyard] Upper Path Fleemer 3": TunicLocationData("Swamp Front", EnemyType.fleemer),
    "Swamp - [Central] Lost Echo 1": TunicLocationData("Swamp Mid", EnemyType.lost_echo),
    "Swamp - [Central] Lost Echo 2": TunicLocationData("Swamp Mid", EnemyType.lost_echo),
    "Swamp - [Central] Gunslinger By Fuse": TunicLocationData("Swamp Mid", EnemyType.gunslinger),
    "Swamp - [Central] Lost Echo 3": TunicLocationData("Swamp Mid", EnemyType.lost_echo),
    "Swamp - [Central] Lost Echo 4": TunicLocationData("Swamp Mid", EnemyType.lost_echo),
    "Swamp - [Central] Lost Echo 5": TunicLocationData("Swamp Mid", EnemyType.lost_echo),
    "Swamp - [Central] Lost Echo 6": TunicLocationData("Swamp Mid", EnemyType.lost_echo),
    "Swamp - [Upper Graveyard] Fleemer Fencer 1": TunicLocationData("Swamp Mid", EnemyType.fleemer_fencer),
    "Swamp - [Upper Graveyard] Fleemer Fencer 2": TunicLocationData("Swamp Mid", EnemyType.fleemer_fencer),
    "Swamp - [Upper Graveyard] Fleemer Fencer 3": TunicLocationData("Swamp Mid", EnemyType.fleemer_fencer),
    "Swamp - [Outside Cathedral] Gunslinger": TunicLocationData("Swamp Mid", EnemyType.gunslinger),
    "Swamp - [Central] Beefboy 1": TunicLocationData("Swamp Mid", EnemyType.beefboy, is_extra_enemy=True, extra_group="Minibosses"),
    "Swamp - [Central] Beefboy 2": TunicLocationData("Swamp Mid", EnemyType.beefboy, is_extra_enemy=True, extra_group="Minibosses"),
    "Swamp - [Upper Graveyard] Void Husher 1": TunicLocationData("Swamp Mid", EnemyType.husher, is_extra_enemy=True),
    "Swamp - [Upper Graveyard] Void Husher 2": TunicLocationData("Swamp Mid", EnemyType.husher, is_extra_enemy=True),
    "Swamp - [Upper Graveyard] Void Husher 3": TunicLocationData("Swamp Mid", EnemyType.husher, is_extra_enemy=True),
    "West Garden - [Northwest] Chompignom Near Fountain (Terry)": TunicLocationData("West Garden after Terry", EnemyType.chompignom),
    "West Garden - [Central Lowlands] Tower In Water Fairy 1": TunicLocationData("West Garden after Terry", EnemyType.fairy),
    "West Garden - [Southwest] Chompignom 1": TunicLocationData("West Garden West Combat", EnemyType.chompignom),
    "West Garden - [Southwest] Fairy Under Pink Tree 1": TunicLocationData("West Garden West Combat", EnemyType.fairy),
    "West Garden - [Southwest] Chompignom 2": TunicLocationData("West Garden West Combat", EnemyType.chompignom),
    "West Garden - [Southwest] Three Fairy Wall 1": TunicLocationData("West Garden West Combat", EnemyType.fairy),
    "West Garden - [Southwest] Three Fairy Wall 2": TunicLocationData("West Garden West Combat", EnemyType.fairy),
    "West Garden - [Southwest] Three Fairy Wall 3": TunicLocationData("West Garden West Combat", EnemyType.fairy),
    "West Garden - [Southwest] Chompignom 3": TunicLocationData("West Garden West Combat", EnemyType.chompignom),
    "West Garden - [Southwest] Chompignom 4": TunicLocationData("West Garden West Combat", EnemyType.chompignom),
    "West Garden - [Southwest] Chompignom 5": TunicLocationData("West Garden West Combat", EnemyType.chompignom),
    "West Garden - [South] Fairy Guarding Chest 2": TunicLocationData("West Garden South Checkpoint", EnemyType.fairy),
    "West Garden - [South] Fairy Guarding Chest 1": TunicLocationData("West Garden South Checkpoint", EnemyType.fairy),
    "West Garden - [Central Highlands] Shield Rudeling Overlooking Ledge": TunicLocationData("West Garden South Checkpoint", EnemyType.rudeling_shield),
    "West Garden - [Central Highlands] Fairy Near Blue Lines 1": TunicLocationData("West Garden South Checkpoint", EnemyType.fairy),
    "West Garden - [Central Highlands] Rudeling Guarding Chest": TunicLocationData("West Garden South Checkpoint", EnemyType.rudeling),
    "West Garden - [Central Highlands] Fairy Near Blue Lines 2": TunicLocationData("West Garden South Checkpoint", EnemyType.fairy),
    "West Garden - [Central Highlands] Rudeling Near Checkpoint": TunicLocationData("West Garden South Checkpoint", EnemyType.rudeling),
    "West Garden - [Central Highlands] Shield Rudeling Near Blue Lines": TunicLocationData("West Garden South Checkpoint", EnemyType.rudeling_shield),
    "West Garden - [Southeast] Rudeling Above Dagger House": TunicLocationData("West Garden at Dagger House", EnemyType.rudeling),
    "West Garden - [Southeast] Chompignom Above Dagger House 1": TunicLocationData("West Garden at Dagger House", EnemyType.chompignom),
    "West Garden - [Southeast] Chompignom Above Dagger House 2": TunicLocationData("West Garden at Dagger House", EnemyType.chompignom),
    "West Garden - [Central Highlands] Guard Captain 1": TunicLocationData("West Garden South Checkpoint", EnemyType.guard_captain),
    "West Garden - [Central Highlands] Chompignom On Blue Lines": TunicLocationData("West Garden South Checkpoint", EnemyType.chompignom),
    "West Garden - [Southwest] Corner Tower Fairy 2": TunicLocationData("West Garden West Combat", EnemyType.fairy, is_extra_enemy=True),
    "West Garden - [Southwest] Corner Tower Fairy 1": TunicLocationData("West Garden West Combat", EnemyType.fairy, is_extra_enemy=True),
    "West Garden - [Central Lowlands] Tower In Water Fairy 2": TunicLocationData("West Garden after Terry", EnemyType.fairy, is_extra_enemy=True),
    "West Garden - Zombie Fox On Grave": TunicLocationData("West Garden before Terry", EnemyType.fox_enemy_zombie, is_extra_enemy=True),
    "West Garden - [Central Highlands] Guard Captain 2": TunicLocationData("West Garden South Checkpoint", EnemyType.guard_captain, is_extra_enemy=True),
    "West Garden - [Southwest] Fairy Under Pink Tree 2": TunicLocationData("West Garden West Combat", EnemyType.fairy, is_extra_enemy=True),
    "West Garden - [Southeast] Void Chompignom Above Dagger House": TunicLocationData("West Garden at Dagger House", EnemyType.chompignom, is_extra_enemy=True),
    "West Garden - [Southwest] Void Chompignom 3": TunicLocationData("West Garden West Combat", EnemyType.chompignom, is_extra_enemy=True),
    "West Garden - [Southwest] Void Chompignom 2": TunicLocationData("West Garden West Combat", EnemyType.chompignom, is_extra_enemy=True),
    "West Garden - [Southwest] Void Chompignom 1": TunicLocationData("West Garden West Combat", EnemyType.chompignom, is_extra_enemy=True),
    "West Garden - [Northwest] Void Chompignom Near Fountain": TunicLocationData("West Garden after Terry", EnemyType.chompignom, is_extra_enemy=True),
    "West Garden - [North] Defeat Garden Knight": TunicLocationData("West Garden before Boss", EnemyType.garden_knight, extra_group="Bosses"),
}

enemy_location_base_id = base_id + 12000
enemy_location_name_to_id: dict[str, int] = {name: enemy_location_base_id + index
                                            for index, name in enumerate(enemy_location_table)}

enemy_location_groups: dict[str, set[str]] = {}
for location_name, location_data in enemy_location_table.items():
    loc_group_name = location_name.split(" - ", 1)[0]
    enemy_location_groups.setdefault(loc_group_name, set()).add(location_name)
    enemy_location_groups.setdefault(f'{loc_group_name} Enemies', set()).add(location_name)
    if location_data.extra_group:
        enemy_location_groups.setdefault(location_data.extra_group, set()).add(location_name)
    enemy_location_groups.setdefault("Enemies", set()).add(location_name)

enemy_item_fill_quantities: dict[str, int] = {
    "Firecracker": 20,
    "Fire Bomb": 20,
    "Ice Bomb": 20,
    "Pepper": 10,
    "Ivy": 10,
    "Lure": 5,
    "HP Berry": 15,
    "MP Berry": 15,
    "Money x1": 70,
    "Money x2": 120,
    "Money x3": 100,
    "Money x4": 50,
    "Money x5": 25,
    "Money x6": 25,
    "Money x7": 20,
    "Money x8": 10,
    "Money x10": 10,
    "Money x20": 7,
    "Money x30": 5,
    "Money x100": 3,
    "Money x200": 1,
    "Money x255": 1,
}

def set_enemy_location_rules(world: "TunicWorld") -> None:
    player = world.player

    for loc_name, loc_data in enemy_location_table.items():
        # skip extra enemy locations if not enabled
        if world.options.shuffle_enemy_drops != ShuffleEnemyDrops.option_extra and loc_data.is_extra_enemy:
            continue

        # rules per enemy type
        location = world.get_location(loc_name)
        enemy_type = loc_data.enemy_type
        if enemy_type == EnemyType.blob:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.blobs, state, world) and has_melee(state, player))
        elif enemy_type == EnemyType.hedgehog:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.hedgehogs, state, world) and has_melee(state, player))
        elif enemy_type in (EnemyType.rudeling, EnemyType.rudeling_shield, EnemyType.guard_captain):
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.rudelings, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.envoy:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.envoy, state, world) and (can_shop(state, world) or (has_sword(state, player) and state.has(grapple, player)) or state.has(gun, player)))
        elif enemy_type == EnemyType.beefboy:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.beefboy, state, world) and has_sword(state, player) and (state.has(att_offering, player, 2) or state.has(sword_upgrade, player, 4)))
        elif enemy_type == EnemyType.phrend:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.phrend, state, world) and has_melee(state, player))
        elif enemy_type == EnemyType.spider:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.spiders, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.autobolt:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.autobolt, state, world) and (has_sword(state, player) or state.has(gun, player)))
        elif enemy_type == EnemyType.tentacle:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.tentacle, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.baby_slorm:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.baby_slorm, state, world) and (has_melee(state, player) or state.has(fire_wand, player) or state.has(gun, player)))
        elif enemy_type == EnemyType.slorm:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.slorm, state, world) and (has_sword(state, player) or state.has(fire_wand, player) or state.has(gun, player)))
        elif enemy_type == EnemyType.laser_trap:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.laser_trap, state, world) and has_melee(state, player))
        elif enemy_type == EnemyType.fairy:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.fairies, state, world) and (has_sword(state, player) or state.has(fire_wand, player) or (state.has_any((stick, sword_upgrade), player) and state.has(grapple, player))))
            if loc_data.er_region == "Cathedral Gauntlet": # stick + grapple for the gauntlet wave would be a little mean
                set_rule(location, lambda state: has_enemy_soul(EnemySouls.fairies, state, world) and (state.has(fire_wand, player) or (has_sword(state, player) and state.has(grapple, player))))
        elif enemy_type == EnemyType.chompignom:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.chompignom, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.garden_knight:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.garden_knight, state, world) and has_sword(state, player))
        elif enemy_type in (EnemyType.custodian, EnemyType.custodian_sword, EnemyType.custodian_candelabra):
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.custodians, state, world) and (has_sword(state, player) or state.has(gun, player)))
        elif enemy_type == EnemyType.siege_engine:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.siege_engine, state, world) and has_sword(state, player) and state.has(fire_wand, player))
        elif enemy_type == EnemyType.plover:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.plover, state, world) and has_melee(state, player))
        elif enemy_type in (EnemyType.crabbit, EnemyType.crabbo):
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.crabs, state, world) and has_melee(state, player))
        elif enemy_type == EnemyType.crabbit_shell:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.crabs, state, world) and has_melee(state, player) and state.has(grapple, player))
        elif enemy_type == EnemyType.husher:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.husher, state, world) and has_sword(state, player) and state.has(grapple, player))
        elif enemy_type in (EnemyType.frog_small, EnemyType.frog, EnemyType.frog_spear):
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.frogs, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.librarian:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.librarian, state, world) and has_sword(state, player)
                                            and has_ladder("Ladders in Library", state, world)
                                            and state.has(grapple, player) and state.has_any((gun, fire_wand), player))
        elif enemy_type in (EnemyType.scavenger, EnemyType.scavenger_support, EnemyType.scavenger_miner):
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.scavengers, state, world) and (has_sword(state, player) or state.has(fire_wand, player)))
        elif enemy_type == EnemyType.voidling:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.voidling, state, world) and (has_sword(state, player) or state.has(gun, player)))
        elif enemy_type == EnemyType.administrator:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.administrator, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.boss_scavenger:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.boss_scavenger, state, world) and has_sword(state, player))
            if world.options.ice_grappling >= IceGrappling.option_medium:
                add_rule(world.get_location("Rooted Ziggurat Lower - Defeat Boss Scavenger"),
                         lambda state: has_ice_grapple_logic(False, IceGrappling.option_medium, state, world,
                                                             [EnemySouls.boss_scavenger]))
        elif enemy_type == EnemyType.fleemer:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.fleemers, state, world) and has_melee(state, player))
            if loc_data.er_region == "Cathedral Gauntlet":
                set_rule(location, lambda state: has_enemy_soul(EnemySouls.fleemers, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.fleemer_fencer:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.fleemers, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.fleemer_big:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.fleemers, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.lost_echo:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.lost_echo, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.gunslinger:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.gunslinger, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.fox_enemy_zombie:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.zombie_foxes, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.fox_enemy:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.zombie_foxes, state, world) and has_sword(state, player))
        elif enemy_type == EnemyType.voidtouched:
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.voidtouched, state, world) and has_sword(state, player) and state.has(laurels, player) and state.has(att_offering, player, 3))

        # specific enemy rules
        if loc_name == "Frog's Domain - Side Room Secret Frog":
            add_rule(location, lambda state: state.has(laurels, player) or state.has(grapple, player))
        elif loc_name in ("Overworld - [Southwest] Autobolt Guarding Chest On Island", "Frog's Domain - Escape Room Autobolt",
                          "Rooted Ziggurat Lower - Left Autobolt 1", "Rooted Ziggurat Lower - Left Autobolt 2",
                          "Rooted Ziggurat Upper - Turret Path Autobolt 5"):
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.autobolt, state, world)
                     and (state.has(gun, player) or (has_sword(state, player) and state.has_any((grapple, laurels), player))))
        elif loc_name == "Patrol Cave - Patrolling Rudeling":
            add_rule(location, lambda state: can_shop(state, world))
        elif loc_name == "East Forest - Ice Grapple Blob":
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.blobs, state, world)
                                             and state.has_all((ice_dagger, fire_wand, grapple), world.player)
                                             and has_ability(icebolt, state, world))
        elif loc_name == "Library Hall - Administrator Coffee Table":
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.administrator, state, world))
        elif loc_name in ("Ruined Atoll - [Northwest] Frog Near Fuse 1", "Ruined Atoll - [Northwest] Frog Near Fuse 2",
                          "Ruined Atoll - [Northwest] Small Frog Above Ruins"):
            add_rule(location, lambda state: state.has_any((grapple, laurels), player))
        elif loc_name == "Quarry - [Lowlands] Scavenger Sniper On Pillar":
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.scavengers, state, world)
                                             and (state.has(fire_wand, player) or (has_sword(state, player) and state.has(grapple, player))))
        elif loc_name == "Cathedral - [2F] Back Hallway Hedgehog Trap 3":
            add_rule(location, lambda state: state.has(grapple, player) or can_shop(state, world))
        elif loc_name == "Overworld - [Northwest] Envoy On Bridge To Quarry":
            set_rule(location, lambda state: has_enemy_soul(EnemySouls.envoy, state, world) and ((has_sword(state, player) and state.has(grapple, player)) or state.has(gun, player)))

