from enum import StrEnum

base_id = 509342400

laurels = "Hero's Laurels"
stick = "Stick"
sword = "Sword"
sword_upgrade = "Sword Upgrade"
grapple = "Magic Orb"
ice_dagger = "Magic Dagger"
fire_wand = "Magic Wand"
gun = "Gun"
lantern = "Lantern"
fairies = "Fairy"
coins = "Golden Coin"
prayer = "Pages 24-25 (Prayer)"
holy_cross = "Pages 42-43 (Holy Cross)"
icebolt = "Pages 52-53 (Icebolt)"
shield = "Shield"
key = "Key"
house_key = "Old House Key"
vault_key = "Fortress Vault Key"
mask = "Scavenger Mask"
att_offering = "ATT Offering"
red_hexagon = "Red Questagon"
green_hexagon = "Green Questagon"
blue_hexagon = "Blue Questagon"
gold_hexagon = "Gold Questagon"

swamp_fuse_1 = "Swamp Fuse 1"
swamp_fuse_2 = "Swamp Fuse 2"
swamp_fuse_3 = "Swamp Fuse 3"
cathedral_elevator_fuse = "Cathedral Elevator Fuse"
quarry_fuse_1 = "Quarry Fuse 1"
quarry_fuse_2 = "Quarry Fuse 2"
ziggurat_miniboss_fuse = "Ziggurat Miniboss Fuse"
ziggurat_teleporter_fuse = "Ziggurat Teleporter Fuse"
fortress_exterior_fuse_1 = "Fortress Exterior Fuse 1"
fortress_exterior_fuse_2 = "Fortress Exterior Fuse 2"
fortress_courtyard_upper_fuse = "Fortress Courtyard Upper Fuse"
fortress_courtyard_lower_fuse = "Fortress Courtyard Fuse"
beneath_the_vault_fuse = "Beneath the Vault Fuse"  # event needs to be renamed probably
fortress_candles_fuse = "Fortress Candles Fuse"
fortress_door_left_fuse = "Fortress Door Left Fuse"
fortress_door_right_fuse = "Fortress Door Right Fuse"
west_furnace_fuse = "West Furnace Fuse"
west_garden_fuse = "West Garden Fuse"
atoll_northeast_fuse = "Atoll Northeast Fuse"
atoll_northwest_fuse = "Atoll Northwest Fuse"
atoll_southeast_fuse = "Atoll Southeast Fuse"
atoll_southwest_fuse = "Atoll Southwest Fuse"
library_lab_fuse = "Library Lab Fuse"


class EnemySouls(StrEnum):
    administrator = "Enemy Soul (Administrator)"
    phrend = "Enemy Soul (Phrend)"
    beefboy = "Enemy Soul (Beefboy)"
    blobs = "Enemy Soul (Blobs)"
    fleemers = "Enemy Soul (Fleemers)"
    crabs = "Enemy Soul (Crabs)"
    chompignom = "Enemy Soul (Chompignom)"
    husher = "Enemy Soul (Husher)"
    autobolt = "Enemy Soul (Autobolt)"
    zombie_foxes = "Enemy Soul (Zombie Foxes)"
    frogs = "Enemy Soul (Frogs)"
    lost_echo = "Enemy Soul (Lost Echo)"
    gunslinger = "Enemy Soul (Gunslinger)"
    hedgehogs = "Enemy Soul (Hedgehogs)"
    laser_trap = "Enemy Soul (Laser Trap)"
    envoy = "Enemy Soul (Envoy)"
    garden_knight = "Enemy Soul (Garden Knight)"
    librarian = "Enemy Soul (Librarian)"
    plover = "Enemy Soul (Plover)"
    fairies = "Enemy Soul (Fairies)"
    scavengers = "Enemy Soul (Scavengers)"
    boss_scavenger = "Enemy Soul (Boss Scavenger)"
    tentacle = "Enemy Soul (Tentacle)"
    rudelings = "Enemy Soul (Rudelings)"
    spiders = "Enemy Soul (Spiders)"
    siege_engine = "Enemy Soul (Siege Engine)"
    slorm = "Enemy Soul (Slorm)"
    baby_slorm = "Enemy Soul (Baby Slorm)"
    voidling = "Enemy Soul (Voidling)"
    custodians = "Enemy Soul (Custodians)"
    voidtouched = "Enemy Soul (Voidtouched)"
    heir = "Enemy Soul (The Heir)"


# "Quarry - [East] Bombable Wall" is excluded from this list since it has slightly different rules
bomb_walls: dict[str, list[str]] = {
    "East Forest - Bombable Wall": [EnemySouls.blobs, EnemySouls.rudelings],
    "Eastern Vault Fortress - [East Wing] Bombable Wall": [EnemySouls.custodians],
    "Overworld - [Central] Bombable Wall": [EnemySouls.blobs, EnemySouls.hedgehogs],
    "Overworld - [Southwest] Bombable Wall Near Fountain": [EnemySouls.rudelings, EnemySouls.hedgehogs],
    "Quarry - [West] Upper Area Bombable Wall": [EnemySouls.scavengers],
    "Ruined Atoll - [Northwest] Bombable Wall": [EnemySouls.frogs],
}
