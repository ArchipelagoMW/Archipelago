from dataclasses import dataclass
from enum import Enum

class ItemType(Enum):
    HEALING = 0
    ATTACK = 1
    STATUS = 2
    MISC = 3


@dataclass
class Item:
    key: str
    name: str
    item_type: ItemType
    value: int = 0

HEALING_ITEMS = [
    # Recovery
    Item("angels_prayer", "Angel's Prayer", ItemType.HEALING, 15),
    Item("healing_potion", "Healing Potion", ItemType.HEALING, 5),
    Item("healing_fog", "Healing Fog", ItemType.HEALING, 15),
    Item("healing_breeze", "Healing Breeze", ItemType.HEALING, 25),
    Item("healing_rain", "Healing Rain", ItemType.HEALING, 60),
    Item("moon_serenade", "Moon Serenade", ItemType.HEALING, 100),
    Item("sun_rhapsody", "Sun Rhapsody", ItemType.HEALING, 25),
    Item("spirit_potion", "Spirit Potion", ItemType.HEALING, 10),
    Item("body_purifier", "Body Purifier", ItemType.HEALING, 5),
    Item("depetrifier", "Depetrifier", ItemType.HEALING, 15),
    Item("mind_purifier", "Mind Purifier", ItemType.HEALING, 10),
    # random
    Item("recovery_ball", "Recovery Ball", ItemType.HEALING, 50),
]

ATTACK_ITEMS = [
    # Attack
    Item("black_rain", "Black Rain", ItemType.ATTACK, 10),
    Item("burn_out", "Burn Out", ItemType.ATTACK, 5),
    Item("burning_wave", "Burning Wave", ItemType.ATTACK, 10),
    Item("dancing_ray", "Dancing Ray", ItemType.ATTACK, 10),
    Item("dark_mist", "Dark Mist", ItemType.ATTACK, 5),
    Item("detonate_rock", "Detonate Rock", ItemType.ATTACK, 5),
    Item("down_burst", "Down Burst", ItemType.ATTACK, 10),
    Item("fatal_blizzard", "Fatal Blizzard", ItemType.ATTACK, 10),
    Item("flash_hall", "Flash Hall", ItemType.ATTACK, 10),
    Item("frozen_jet", "Frozen Jet", ItemType.ATTACK, 10),
    Item("gravity_grabber", "Gravity Grabber", ItemType.ATTACK, 10),
    Item("gushing_magma", "Gushing Magma", ItemType.ATTACK, 10),
    Item("meteor_fall", "Meteor Fall", ItemType.ATTACK, 10),
    Item("night_raid", "Night Raid", ItemType.ATTACK, 10),
    Item("pellet", "Pellet", ItemType.ATTACK, 5),
    Item("psyche_bomb", "Psyche Bomb", ItemType.ATTACK, 10),
    Item("psyche_bomb_x", "Psyche Bomb X", ItemType.ATTACK),
    Item("rave_twister", "Rave Twister", ItemType.ATTACK, 10),
    Item("spark_net", "Spark Net", ItemType.ATTACK, 5),
    Item("spear_frost", "Spear Frost", ItemType.ATTACK, 5),
    Item("spectral_flash", "Spectral Flash", ItemType.ATTACK, 10),
    Item("spinning_gale", "Spinning Gale", ItemType.ATTACK, 5),
    Item("thunderbolt", "Thunderbolt", ItemType.ATTACK, 10),
    Item("trans_light", "Trans Light", ItemType.ATTACK, 5),

    # random
    Item("attack_ball", "Attack Ball", ItemType.ATTACK, 50),
]

STATUS_ITEMS = [
    # Status
    Item("charm_potion", "Charm Potion", ItemType.STATUS, 2),
    Item("magic_sig_stone", "Magic Sig Stone", ItemType.STATUS, 200),
    Item("midnight_terror", "Midnight Terror", ItemType.STATUS, 10),
    Item("pandemonium", "Pandemonium", ItemType.STATUS, 200),
    Item("panic_bell", "Panic Bell", ItemType.STATUS, 10),
    Item("poison_needle", "Poison Needle", ItemType.STATUS, 10),
    Item("sachet", "Sachet", ItemType.STATUS, 200),
    Item("smoke_ball", "Smoke Ball", ItemType.STATUS, 200),
    Item("stunning_hammer", "Stunning Hammer", ItemType.STATUS, 10),
    Item("total_vanishing", "Total Vanishing", ItemType.STATUS, 10),
]

ITEMS = (HEALING_ITEMS + ATTACK_ITEMS + STATUS_ITEMS)
