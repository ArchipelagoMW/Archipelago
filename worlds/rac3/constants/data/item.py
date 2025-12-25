from dataclasses import dataclass
from typing import Optional

from BaseClasses import ItemClassification
from worlds.rac3.constants.item_tags import RAC3ITEMTAG
from worlds.rac3.constants.items import RAC3ITEM, UPGRADE_DICT
from worlds.rac3.constants.status import RAC3STATUS


@dataclass
class RAC3ITEMDATA:
    ID: int = None
    LEVEL: int = None
    LEVEL_ADDRESS: int = None
    UNLOCK_ADDRESS: int = None
    UNLOCK_ADDRESS_2: int = None
    XP_ADDRESS: int = None
    XP_THRESHOLD: int = None
    POWER: int = None
    ARMOR: float = None
    AMMO_ADDRESS: int = None
    AMMO: int = None
    AP_CODE: int = None
    AP_CLASSIFICATION: ItemClassification = None
    TAGS: list[str] = None

    def __init__(self,
                 idx: int,
                 address: Optional[int] = None,
                 address_2: Optional[int] = None,
                 power: Optional[int] = None,
                 ammo: Optional[int] = None,
                 xp: Optional[int] = None,
                 level: Optional[int] = None,
                 level_address: Optional[int] = None,
                 armor: Optional[float] = None,
                 ap_classification: Optional[ItemClassification] = ItemClassification.filler,
                 tags: list[str] = None):
        self.ID = idx
        self.AP_CODE = idx + 50000000
        self.AP_CLASSIFICATION = ap_classification
        self.LEVEL = level
        self.LEVEL_ADDRESS = level_address
        self.UNLOCK_ADDRESS = address
        self.UNLOCK_ADDRESS_2 = address_2
        self.XP_ADDRESS = 4 * idx + RAC3STATUS.ITEM_XP_ADDRESS
        self.XP_THRESHOLD = xp
        self.POWER = power
        self.ARMOR = armor
        self.AMMO_ADDRESS = 4 * idx + RAC3STATUS.ITEM_AMMO_ADDRESS
        self.AMMO = ammo
        self.TAGS = tags

    @staticmethod
    def construct_unused(idx: int,
                         ammo: Optional[int] = None,
                         tags: Optional[list[str]] = None):
        all_tags: list[str] = [RAC3ITEMTAG.UNUSED]
        if tags is not None:
            all_tags.extend(tags)
        return RAC3ITEMDATA(idx, ammo=ammo, ap_classification=ItemClassification.filler, tags=all_tags)

    @staticmethod
    def construct_gadget(idx: int,
                         ap_classification: ItemClassification,
                         tags: Optional[list[str]] = None):
        address: int = idx + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        all_tags: list[str] = [RAC3ITEMTAG.GADGET]
        if tags is not None:
            all_tags.extend(tags)
        return RAC3ITEMDATA(idx, address, address_2, ap_classification=ap_classification, tags=all_tags)

    @staticmethod
    def construct_weapon(idx: int,
                         power: int,
                         ammo: Optional[int] = None,
                         ap_classification: Optional[ItemClassification] = None,
                         tags: Optional[list[str]] = None):
        address: int = idx + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        all_tags: list[str] = [RAC3ITEMTAG.WEAPON, RAC3ITEMTAG.NON_PROG_WEAPON]
        if idx != 0x16:
            all_tags.append(RAC3ITEMTAG.EQUIPABLE)
        if tags is not None:
            all_tags.extend(tags)
        return RAC3ITEMDATA(idx, address, address_2, power, ammo, 0, level=1,
                            level_address=idx + RAC3STATUS.LEVEL_TABLE, ap_classification=ap_classification,
                            tags=all_tags)

    @staticmethod
    def construct_weapon_level(idx: int,
                               power: int,
                               ammo: Optional[int] = None,
                               xp: Optional[int] = 0,
                               tags: Optional[list[str]] = None):
        entry: dict[str, list[int]] = dict(filter(lambda data_kv: idx in data_kv[1], UPGRADE_DICT.items()))
        base: int = list(entry.values())[0][0]
        name: str = list(entry.keys())[0][0]
        all_tags: list[str] = [RAC3ITEMTAG.WEAPON_UPGRADE, name]
        if tags is not None:
            all_tags.extend(tags)
        amount: int = 32 * xp
        return RAC3ITEMDATA(idx, power=power, ammo=ammo, xp=amount, level=idx - base,
                            level_address=base + RAC3STATUS.LEVEL_TABLE, ap_classification=ItemClassification.useful,
                            tags=all_tags)

    @staticmethod
    def construct_weapon_prog(idx: int,
                              ap_classification: ItemClassification,
                              tags: Optional[list[str]] = None):
        address: int = (idx - 0xCB) * 8 + 0x27 + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        all_tags: list[str] = [RAC3ITEMTAG.PROG_WEAPON, RAC3ITEMTAG.PROGRESSIVE, RAC3ITEMTAG.WEAPON]
        if tags is not None:
            all_tags.extend(tags)
        return RAC3ITEMDATA(idx, address, address_2, ap_classification=ap_classification, tags=all_tags)

    @staticmethod
    def construct_rac2_prog(idx: int,
                            ap_classification: ItemClassification):
        address: int = idx - 0xCA + RAC3STATUS.ITEM_UNLOCK_ADDRESS
        address_2: int = address + RAC3STATUS.ITEM_UNLOCK_ADDRESS_2_OFFSET
        return RAC3ITEMDATA(idx, address, address_2, ap_classification=ap_classification,
                            tags=[RAC3ITEMTAG.PROG_WEAPON, RAC3ITEMTAG.PROGRESSIVE, RAC3ITEMTAG.WEAPON])

    @staticmethod
    def construct_infobot(idx: int,
                          ap_classification: ItemClassification):
        return RAC3ITEMDATA(idx, ap_classification=ap_classification, tags=[RAC3ITEMTAG.INFOBOT])

    @staticmethod
    def construct_armor(idx: int,
                        ap_classification: ItemClassification,
                        armor: int,
                        tags: Optional[list[str]] = None):
        address: int = RAC3STATUS.ARMOR
        reduction: float = armor / 30
        all_tags: list[str] = [RAC3ITEMTAG.ARMOR]
        if tags is not None:
            all_tags.extend(tags)
        return RAC3ITEMDATA(idx, address, armor=reduction, ap_classification=ap_classification, tags=all_tags)

    @staticmethod
    def construct_vidcomic(idx: int,
                           tag: Optional[list[str]] = None):
        # Progressive order: 1, 2, 3, 4, 5
        # Memory order:      1, 4, 2, 3, 5
        progressive_to_memory: list[int] = [0, 2, 3, 1, 4]
        address: int = progressive_to_memory[idx - 0xFB] + RAC3STATUS.VIDCOMIC
        if tag:
            tags: list[str] = tag + [RAC3ITEMTAG.VIDCOMIC]
        else:
            tags: list[str] = [RAC3ITEMTAG.VIDCOMIC]
        return RAC3ITEMDATA(idx, address, ap_classification=ItemClassification.progression, tags=tags)

    @staticmethod
    def construct_trap(idx: int,
                       address: Optional[int] = None):
        return RAC3ITEMDATA(idx, address, ap_classification=ItemClassification.trap, tags=[RAC3ITEMTAG.TRAP])

    @staticmethod
    def construct_other(idx: int,
                        address: Optional[int] = None):
        return RAC3ITEMDATA(idx, address, ap_classification=ItemClassification.filler, tags=[RAC3ITEMTAG.FILLER])

    @staticmethod
    def construct_goal(idx: int):
        return RAC3ITEMDATA(idx, ap_classification=ItemClassification.progression, tags=[RAC3ITEMTAG.GOAL])


RAC3_ITEM_DATA_TABLE: dict[str, RAC3ITEMDATA] = {
    # Items
    # 0x01
    RAC3ITEM.HELI_PACK: RAC3ITEMDATA.construct_gadget(0x02, ItemClassification.useful),
    RAC3ITEM.THRUSTER_PACK: RAC3ITEMDATA.construct_gadget(0x03, ItemClassification.useful),
    RAC3ITEM.HYDRO_PACK: RAC3ITEMDATA.construct_unused(0x04),  # Unused
    RAC3ITEM.MAP_O_MATIC: RAC3ITEMDATA.construct_gadget(0x05, ItemClassification.progression_deprioritized),
    RAC3ITEM.COMMANDO_SUIT: RAC3ITEMDATA.construct_unused(0x06),  # Unused
    RAC3ITEM.BOLT_GRABBER: RAC3ITEMDATA.construct_gadget(0x07, ItemClassification.useful),
    RAC3ITEM.LEVITATOR: RAC3ITEMDATA.construct_unused(0x08),  # Unused
    RAC3ITEM.WRENCH: RAC3ITEMDATA.construct_unused(0x09, tags=[RAC3ITEMTAG.EQUIPABLE]),
    RAC3ITEM.BOMB_GLOVE: RAC3ITEMDATA.construct_unused(0x0A, 40, [RAC3ITEMTAG.EQUIPABLE]),  # Unused
    RAC3ITEM.HYPERSHOT: RAC3ITEMDATA.construct_gadget(0x0B, ItemClassification.progression, [RAC3ITEMTAG.EQUIPABLE]),
    RAC3ITEM.MORPH_O_RAY: RAC3ITEMDATA.construct_unused(0x0C, tags=[RAC3ITEMTAG.EQUIPABLE]),  # Unused
    RAC3ITEM.GRAV_BOOTS: RAC3ITEMDATA.construct_gadget(0x0D, ItemClassification.progression),
    RAC3ITEM.GRIND_BOOTS: RAC3ITEMDATA.construct_unused(0x0E),  # Unused
    RAC3ITEM.GLIDER: RAC3ITEMDATA.construct_unused(0x0F),  # Unused
    RAC3ITEM.PLASMA_COIL:
        RAC3ITEMDATA.construct_weapon(0x10, 2400, 15, ItemClassification.useful),
    RAC3ITEM.LAVA_GUN: RAC3ITEMDATA.construct_weapon(0x11, 160, 150, ItemClassification.useful),
    RAC3ITEM.REFRACTOR: RAC3ITEMDATA.construct_gadget(0x12, ItemClassification.progression, [RAC3ITEMTAG.EQUIPABLE]),
    RAC3ITEM.BOUNCER: RAC3ITEMDATA.construct_weapon(0x13, 1200, 10, ItemClassification.useful),
    RAC3ITEM.HACKER: RAC3ITEMDATA.construct_gadget(0x14, ItemClassification.progression),
    RAC3ITEM.MINI_TURRET: RAC3ITEMDATA.construct_weapon(0x15, 600, 10, ItemClassification.useful),
    RAC3ITEM.SHIELD_CHARGER: RAC3ITEMDATA.construct_weapon(0x16, 60, 3, ItemClassification.useful),
    # 0x17 Set on new file, Empty Hand
    RAC3ITEM.HELMET: RAC3ITEMDATA.construct_unused(0x18),  # Unused
    # 0x19 SEVERE CRASH RISK
    RAC3ITEM.BOX_BREAKER: RAC3ITEMDATA.construct_gadget(0x1A, ItemClassification.progression),
    RAC3ITEM.HASH: RAC3ITEMDATA.construct_unused(0x1B),  # Unused
    RAC3ITEM.GRIND_BOOTS_2: RAC3ITEMDATA.construct_unused(0x1C),  # Unused
    RAC3ITEM.CHARGE_BOOTS: RAC3ITEMDATA.construct_gadget(0x1D, ItemClassification.progression),
    RAC3ITEM.TYHRRA_GUISE: RAC3ITEMDATA.construct_gadget(0x1E, ItemClassification.progression, [RAC3ITEMTAG.EQUIPABLE]),
    RAC3ITEM.WARP_PAD: RAC3ITEMDATA.construct_gadget(0x1F, ItemClassification.progression, [RAC3ITEMTAG.EQUIPABLE]),
    RAC3ITEM.NANO_PAK: RAC3ITEMDATA.construct_gadget(0x20, ItemClassification.useful),
    RAC3ITEM.STAR_MAP: RAC3ITEMDATA.construct_gadget(0x21, ItemClassification.progression),
    RAC3ITEM.MASTER_PLAN: RAC3ITEMDATA.construct_gadget(0x22, ItemClassification.progression),
    RAC3ITEM.PDA: RAC3ITEMDATA.construct_gadget(0x23, ItemClassification.useful, [RAC3ITEMTAG.EQUIPABLE]),
    RAC3ITEM.THIRD_PERSON: RAC3ITEMDATA.construct_unused(0x24),
    RAC3ITEM.FIRST_PERSON: RAC3ITEMDATA.construct_unused(0x25),
    RAC3ITEM.LOCK_STRAFE: RAC3ITEMDATA.construct_unused(0x26),
    RAC3ITEM.SHOCK_BLASTER: RAC3ITEMDATA.construct_weapon(0x27, 40, 30, ItemClassification.useful),
    RAC3ITEM.SHOCK_BLASTER_V2: RAC3ITEMDATA.construct_weapon_level(0x28, 50, 35, 150),
    RAC3ITEM.SHOCK_BLASTER_V3: RAC3ITEMDATA.construct_weapon_level(0x29, 60, 40, 400),
    RAC3ITEM.SHOCK_BLASTER_V4: RAC3ITEMDATA.construct_weapon_level(0x2A, 80, 40, 700),
    RAC3ITEM.SHOCK_CANNON: RAC3ITEMDATA.construct_weapon_level(0x2B, 100, 50, 1000),
    RAC3ITEM.SHOCK_CANNON_V6: RAC3ITEMDATA.construct_weapon_level(0x2C, 1100, 50, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.SHOCK_CANNON_V7: RAC3ITEMDATA.construct_weapon_level(0x2D, 1400, 55, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.SHOCK_CANNON_V8: RAC3ITEMDATA.construct_weapon_level(0x2E, 2100, 60, 25000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.N60_STORM: RAC3ITEMDATA.construct_weapon(0x2F, 150, 150, ItemClassification.useful),
    RAC3ITEM.N60_STORM_V2: RAC3ITEMDATA.construct_weapon_level(0x30, 175, 175, 200),
    RAC3ITEM.N60_STORM_V3: RAC3ITEMDATA.construct_weapon_level(0x31, 200, 200, 500),
    RAC3ITEM.N60_STORM_V4: RAC3ITEMDATA.construct_weapon_level(0x32, 250, 225, 1500),
    RAC3ITEM.N90_HURRICANE: RAC3ITEMDATA.construct_weapon_level(0x33, 350, 300, 3300),
    RAC3ITEM.N90_HURRICANE_V6: RAC3ITEMDATA.construct_weapon_level(0x34, 3500, 300, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.N90_HURRICANE_V7: RAC3ITEMDATA.construct_weapon_level(0x35, 5000, 350, 15000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.N90_HURRICANE_V8: RAC3ITEMDATA.construct_weapon_level(0x36, 6000, 400, 37500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.INFECTOR: RAC3ITEMDATA.construct_weapon(0x37, 180, 15, ItemClassification.progression),
    RAC3ITEM.INFECTOR_V2: RAC3ITEMDATA.construct_weapon_level(0x38, 240, 15, 400),
    RAC3ITEM.INFECTOR_V3: RAC3ITEMDATA.construct_weapon_level(0x39, 320, 18, 800),
    RAC3ITEM.INFECTOR_V4: RAC3ITEMDATA.construct_weapon_level(0x3A, 400, 18, 2000),
    RAC3ITEM.INFECTO_BOMB: RAC3ITEMDATA.construct_weapon_level(0x3B, 600, 20, 3800),
    RAC3ITEM.INFECTO_BOMB_V6: RAC3ITEMDATA.construct_weapon_level(0x3C, 4000, 20, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.INFECTO_BOMB_V7: RAC3ITEMDATA.construct_weapon_level(0x3D, 5000, 25, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.INFECTO_BOMB_V8: RAC3ITEMDATA.construct_weapon_level(0x3E, 6000, 30, 15000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.ANNIHILATOR: RAC3ITEMDATA.construct_weapon(0x3F, 500, 20, ItemClassification.progression),
    RAC3ITEM.ANNIHILATOR_V2: RAC3ITEMDATA.construct_weapon_level(0x40, 600, 20, 800),
    RAC3ITEM.ANNIHILATOR_V3: RAC3ITEMDATA.construct_weapon_level(0x41, 800, 20, 2400),
    RAC3ITEM.ANNIHILATOR_V4: RAC3ITEMDATA.construct_weapon_level(0x42, 1100, 22, 6400),
    RAC3ITEM.DECIMATOR: RAC3ITEMDATA.construct_weapon_level(0x43, 1400, 25, 12400),
    RAC3ITEM.DECIMATOR_V6: RAC3ITEMDATA.construct_weapon_level(0x44, 3000, 25, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.DECIMATOR_V7: RAC3ITEMDATA.construct_weapon_level(0x45, 4000, 28, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.DECIMATOR_V8: RAC3ITEMDATA.construct_weapon_level(0x46, 5000, 30, 25000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.SPITTING_HYDRA: RAC3ITEMDATA.construct_weapon(0x47, 200, 15, ItemClassification.progression),
    RAC3ITEM.SPITTING_HYDRA_V2: RAC3ITEMDATA.construct_weapon_level(0x48, 240, 15, 300),
    RAC3ITEM.SPITTING_HYDRA_V3: RAC3ITEMDATA.construct_weapon_level(0x49, 280, 15, 900),
    RAC3ITEM.SPITTING_HYDRA_V4: RAC3ITEMDATA.construct_weapon_level(0x4A, 320, 15, 1800),
    RAC3ITEM.TEMPEST: RAC3ITEMDATA.construct_weapon_level(0x4B, 400, 15, 3000),
    RAC3ITEM.TEMPEST_V6: RAC3ITEMDATA.construct_weapon_level(0x4C, 3200, 15, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.TEMPEST_V7: RAC3ITEMDATA.construct_weapon_level(0x4D, 5400, 18, 15000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.TEMPEST_V8: RAC3ITEMDATA.construct_weapon_level(0x4E, 6000, 20, 37500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.DISC_BLADE: RAC3ITEMDATA.construct_weapon(0x4F, 500, 25, ItemClassification.progression),
    RAC3ITEM.DISC_BLADE_V2: RAC3ITEMDATA.construct_weapon_level(0x50, 600, 25, 700),
    RAC3ITEM.DISC_BLADE_V3: RAC3ITEMDATA.construct_weapon_level(0x51, 1400, 25, 2100),
    RAC3ITEM.DISC_BLADE_V4: RAC3ITEMDATA.construct_weapon_level(0x52, 2400, 25, 6100),
    RAC3ITEM.MULTI_DISC: RAC3ITEMDATA.construct_weapon_level(0x53, 3600, 25, 12100),
    RAC3ITEM.MULTI_DISC_V6: RAC3ITEMDATA.construct_weapon_level(0x54, 4400, 25, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.MULTI_DISC_V7: RAC3ITEMDATA.construct_weapon_level(0x55, 5600, 28, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.MULTI_DISC_V8: RAC3ITEMDATA.construct_weapon_level(0x56, 8400, 30, 25000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.AGENTS_OF_DOOM: RAC3ITEMDATA.construct_weapon(0x57, 240, 6, ItemClassification.useful),
    RAC3ITEM.AGENTS_OF_DOOM_V2: RAC3ITEMDATA.construct_weapon_level(0x58, 400, 6, 400),
    RAC3ITEM.AGENTS_OF_DOOM_V3: RAC3ITEMDATA.construct_weapon_level(0x59, 660, 6, 1000),
    RAC3ITEM.AGENTS_OF_DOOM_V4: RAC3ITEMDATA.construct_weapon_level(0x5A, 2000, 8, 3000),
    RAC3ITEM.AGENTS_OF_DREAD: RAC3ITEMDATA.construct_weapon_level(0x5B, 6000, 8, 6000),
    RAC3ITEM.AGENTS_OF_DREAD_V6: RAC3ITEMDATA.construct_weapon_level(0x5C, 8000, 8, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.AGENTS_OF_DREAD_V7: RAC3ITEMDATA.construct_weapon_level(0x5D, 10000, 10, 7500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.AGENTS_OF_DREAD_V8: RAC3ITEMDATA.construct_weapon_level(0x5E, 12000, 12, 20000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.RIFT_INDUCER: RAC3ITEMDATA.construct_weapon(0x5F, 1000, 8, ItemClassification.progression),
    RAC3ITEM.RIFT_INDUCER_V2: RAC3ITEMDATA.construct_weapon_level(0x60, 1300, 8, 800),
    RAC3ITEM.RIFT_INDUCER_V3: RAC3ITEMDATA.construct_weapon_level(0x61, 1500, 10, 2400),
    RAC3ITEM.RIFT_INDUCER_V4: RAC3ITEMDATA.construct_weapon_level(0x62, 1700, 10, 6400),
    RAC3ITEM.RIFT_RIPPER: RAC3ITEMDATA.construct_weapon_level(0x63, 2000, 12, 12400),
    RAC3ITEM.RIFT_RIPPER_V6: RAC3ITEMDATA.construct_weapon_level(0x64, 4000, 12, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.RIFT_RIPPER_V7: RAC3ITEMDATA.construct_weapon_level(0x65, 5000, 14, 15000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.RIFT_RIPPER_V8: RAC3ITEMDATA.construct_weapon_level(0x66, 6000, 16, 37500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.HOLO_SHIELD: RAC3ITEMDATA.construct_weapon(0x67, 200, 8, ItemClassification.useful),
    RAC3ITEM.HOLO_SHIELD_V2: RAC3ITEMDATA.construct_weapon_level(0x68, 300, 8, 150),
    RAC3ITEM.HOLO_SHIELD_V3: RAC3ITEMDATA.construct_weapon_level(0x69, 400, 10, 450),
    RAC3ITEM.HOLO_SHIELD_V4: RAC3ITEMDATA.construct_weapon_level(0x6A, 500, 10, 1350),
    RAC3ITEM.ULTRA_SHIELD: RAC3ITEMDATA.construct_weapon_level(0x6B, 600, 12, 2700),
    RAC3ITEM.ULTRA_SHIELD_V6: RAC3ITEMDATA.construct_weapon_level(0x6C, 1000, 12, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.ULTRA_SHIELD_V7: RAC3ITEMDATA.construct_weapon_level(0x6D, 1500, 12, 5000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.ULTRA_SHIELD_V8: RAC3ITEMDATA.construct_weapon_level(0x6E, 2000, 14, 12500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.FLUX_RIFLE: RAC3ITEMDATA.construct_weapon(0x6F, 300, 10, ItemClassification.progression),
    RAC3ITEM.FLUX_RIFLE_V2: RAC3ITEMDATA.construct_weapon_level(0x70, 400, 12, 200),
    RAC3ITEM.FLUX_RIFLE_V3: RAC3ITEMDATA.construct_weapon_level(0x71, 500, 12, 600),
    RAC3ITEM.FLUX_RIFLE_V4: RAC3ITEMDATA.construct_weapon_level(0x72, 1600, 12, 1500),
    RAC3ITEM.SPLITTER_RIFLE: RAC3ITEMDATA.construct_weapon_level(0x73, 2800, 15, 2900),
    RAC3ITEM.SPLITTER_RIFLE_V6: RAC3ITEMDATA.construct_weapon_level(0x74, 5200, 15, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.SPLITTER_RIFLE_V7: RAC3ITEMDATA.construct_weapon_level(0x75, 7000, 18, 7500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.SPLITTER_RIFLE_V8: RAC3ITEMDATA.construct_weapon_level(0x76, 8400, 20, 20000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.NITRO_LAUNCHER: RAC3ITEMDATA.construct_weapon(0x77, 200, 8, ItemClassification.useful),
    RAC3ITEM.NITRO_LAUNCHER_V2: RAC3ITEMDATA.construct_weapon_level(0x78, 240, 8, 200),
    RAC3ITEM.NITRO_LAUNCHER_V3: RAC3ITEMDATA.construct_weapon_level(0x79, 300, 10, 500),
    RAC3ITEM.NITRO_LAUNCHER_V4: RAC3ITEMDATA.construct_weapon_level(0x7A, 400, 10, 1100),
    RAC3ITEM.NITRO_ERUPTOR: RAC3ITEMDATA.construct_weapon_level(0x7B, 800, 12, 2600),
    RAC3ITEM.NITRO_ERUPTOR_V6: RAC3ITEMDATA.construct_weapon_level(0x7C, 4200, 12, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.NITRO_ERUPTOR_V7: RAC3ITEMDATA.construct_weapon_level(0x7D, 5000, 14, 7500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.NITRO_ERUPTOR_V8: RAC3ITEMDATA.construct_weapon_level(0x7E, 6000, 16, 20000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.PLASMA_WHIP: RAC3ITEMDATA.construct_weapon(0x7F, 40, 25, ItemClassification.progression),
    RAC3ITEM.PLASMA_WHIP_V2: RAC3ITEMDATA.construct_weapon_level(0x80, 50, 30, 200),
    RAC3ITEM.PLASMA_WHIP_V3: RAC3ITEMDATA.construct_weapon_level(0x81, 70, 35, 800),
    RAC3ITEM.PLASMA_WHIP_V4: RAC3ITEMDATA.construct_weapon_level(0x82, 100, 40, 1800),
    RAC3ITEM.QUANTUM_WHIP: RAC3ITEMDATA.construct_weapon_level(0x83, 140, 40, 3300),
    RAC3ITEM.QUANTUM_WHIP_V6: RAC3ITEMDATA.construct_weapon_level(0x84, 1400, 50, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.QUANTUM_WHIP_V7: RAC3ITEMDATA.construct_weapon_level(0x85, 1800, 55, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.QUANTUM_WHIP_V8: RAC3ITEMDATA.construct_weapon_level(0x86, 2400, 60, 25000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.SUCK_CANNON: RAC3ITEMDATA.construct_weapon(0x87, 200, ap_classification=ItemClassification.progression),
    RAC3ITEM.SUCK_CANNON_V2: RAC3ITEMDATA.construct_weapon_level(0x88, 260, xp=200),
    RAC3ITEM.SUCK_CANNON_V3: RAC3ITEMDATA.construct_weapon_level(0x89, 320, xp=600),
    RAC3ITEM.SUCK_CANNON_V4: RAC3ITEMDATA.construct_weapon_level(0x8A, 400, xp=1200),
    RAC3ITEM.VORTEX_CANNON: RAC3ITEMDATA.construct_weapon_level(0x8B, 600, xp=2000),
    RAC3ITEM.VORTEX_CANNON_V6: RAC3ITEMDATA.construct_weapon_level(0x8C, 4200, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.VORTEX_CANNON_V7: RAC3ITEMDATA.construct_weapon_level(0x8D, 5000, xp=5000, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.VORTEX_CANNON_V8: RAC3ITEMDATA.construct_weapon_level(0x8E, 6000, xp=12500, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.QWACK_O_RAY: RAC3ITEMDATA.construct_weapon(0x8F, 1000, ap_classification=ItemClassification.progression),
    RAC3ITEM.QWACK_O_RAY_V2: RAC3ITEMDATA.construct_weapon_level(0x90, 1500, xp=1000),
    RAC3ITEM.QWACK_O_RAY_V3: RAC3ITEMDATA.construct_weapon_level(0x91, 2000, xp=3000),
    RAC3ITEM.QWACK_O_RAY_V4: RAC3ITEMDATA.construct_weapon_level(0x92, 2500, xp=8000),
    RAC3ITEM.QWACK_O_BLITZER: RAC3ITEMDATA.construct_weapon_level(0x93, 3000, xp=16000),
    RAC3ITEM.QWACK_O_BLITZER_V6: RAC3ITEMDATA.construct_weapon_level(0x94, 4000, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.QWACK_O_BLITZER_V7: RAC3ITEMDATA.construct_weapon_level(0x95, 5000, xp=10000, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.QWACK_O_BLITZER_V8: RAC3ITEMDATA.construct_weapon_level(0x96, 6000, xp=25000, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.RY3N0: RAC3ITEMDATA.construct_weapon(0x97, 6000, 25, ItemClassification.progression),
    RAC3ITEM.RY3NO_V2: RAC3ITEMDATA.construct_weapon_level(0x98, 7000, 30, 20000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.RY3NO_V3: RAC3ITEMDATA.construct_weapon_level(0x99, 8000, 35, 50000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.RY3NO_V4: RAC3ITEMDATA.construct_weapon_level(0x9A, 9000, 40, 90000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.RYNOCIRATOR: RAC3ITEMDATA.construct_weapon_level(0x9B, 10000, 50, 140000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.PLASMA_COIL_V2: RAC3ITEMDATA.construct_weapon_level(0xA0, 3000, 15, 8000),
    RAC3ITEM.LAVA_GUN_V2: RAC3ITEMDATA.construct_weapon_level(0xA1, 240, 150, 600),
    RAC3ITEM.MINI_TURRET_V2: RAC3ITEMDATA.construct_weapon_level(0xA2, 800, 10, 400),
    RAC3ITEM.WRENCH_V2: RAC3ITEMDATA.construct_unused(0xA4),
    RAC3ITEM.WRENCH_V3: RAC3ITEMDATA.construct_unused(0xA5),
    RAC3ITEM.BOUNCER_V2: RAC3ITEMDATA.construct_weapon_level(0xA6, 1400, 10, 2500),
    RAC3ITEM.SHIELD_CHARGER_V2: RAC3ITEMDATA.construct_weapon_level(0xA7, 100, 3, 2200),
    RAC3ITEM.MINI_TURRET_V3: RAC3ITEMDATA.construct_weapon_level(0xA8, 1000, 12, 1000),
    RAC3ITEM.MINI_TURRET_V4: RAC3ITEMDATA.construct_weapon_level(0xA9, 1200, 12, 2000),
    RAC3ITEM.MEGA_TURRET: RAC3ITEMDATA.construct_weapon_level(0xAA, 2080, 12, 3500),
    RAC3ITEM.MEGA_TURRET_V6: RAC3ITEMDATA.construct_weapon_level(0xAB, 10400, 12, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.MEGA_TURRET_V7: RAC3ITEMDATA.construct_weapon_level(0xAC, 13000, 14, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.MEGA_TURRET_V8: RAC3ITEMDATA.construct_weapon_level(0xAD, 15600, 16, 25000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.LAVA_GUN_V3: RAC3ITEMDATA.construct_weapon_level(0xAE, 360, 175, 1500),
    RAC3ITEM.LAVA_GUN_V4: RAC3ITEMDATA.construct_weapon_level(0xAF, 500, 175, 2700),
    RAC3ITEM.LIQUID_NITROGEN: RAC3ITEMDATA.construct_weapon_level(0xB0, 700, 200, 4200),
    RAC3ITEM.LIQUID_NITROGEN_V6: RAC3ITEMDATA.construct_weapon_level(0xB1, 2600, 200, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.LIQUID_NITROGEN_V7: RAC3ITEMDATA.construct_weapon_level(0xB2, 3000, 250, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.LIQUID_NITROGEN_V8: RAC3ITEMDATA.construct_weapon_level(0xB3, 3600, 300, 25000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.BOUNCER_V3: RAC3ITEMDATA.construct_weapon_level(0xB4, 1400, 12, 8500),
    RAC3ITEM.BOUNCER_V4: RAC3ITEMDATA.construct_weapon_level(0xB5, 1800, 12, 18500),
    RAC3ITEM.HEAVY_BOUNCER: RAC3ITEMDATA.construct_weapon_level(0xB6, 2000, 12, 30500),
    RAC3ITEM.HEAVY_BOUNCER_V6: RAC3ITEMDATA.construct_weapon_level(0xB7, 3000, 12, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.HEAVY_BOUNCER_V7: RAC3ITEMDATA.construct_weapon_level(0xB8, 3600, 14, 10000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.HEAVY_BOUNCER_V8: RAC3ITEMDATA.construct_weapon_level(0xB9, 4400, 16, 25000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.PLASMA_COIL_V3: RAC3ITEMDATA.construct_weapon_level(0xBA, 3600, 18, 18000),
    RAC3ITEM.PLASMA_COIL_V4: RAC3ITEMDATA.construct_weapon_level(0xBB, 4200, 18, 30000),
    RAC3ITEM.PLASMA_STORM: RAC3ITEMDATA.construct_weapon_level(0xBC, 6000, 20, 44000),
    RAC3ITEM.PLASMA_STORM_V6: RAC3ITEMDATA.construct_weapon_level(0xBD, 6800, 20, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.PLASMA_STORM_V7: RAC3ITEMDATA.construct_weapon_level(0xBE, 7600, 22, 15000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.PLASMA_STORM_V8: RAC3ITEMDATA.construct_weapon_level(0xBF, 8400, 25, 37500, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.SHIELD_CHARGER_V3: RAC3ITEMDATA.construct_weapon_level(0xC0, 140, 3, 5000),
    RAC3ITEM.SHIELD_CHARGER_V4: RAC3ITEMDATA.construct_weapon_level(0xC1, 180, 4, 9600),
    RAC3ITEM.TESLA_BARRIER: RAC3ITEMDATA.construct_weapon_level(0xC2, 240, 4, 16800),
    RAC3ITEM.TESLA_BARRIER_V6: RAC3ITEMDATA.construct_weapon_level(0xC3, 300, 4, tags=[RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.TESLA_BARRIER_V7: RAC3ITEMDATA.construct_weapon_level(0xC4, 400, 5, 12000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.TESLA_BARRIER_V8: RAC3ITEMDATA.construct_weapon_level(0xC5, 500, 5, 30000, [RAC3ITEMTAG.NGPLUS]),
    RAC3ITEM.WRENCH_V4: RAC3ITEMDATA.construct_unused(0xC6),
    RAC3ITEM.WRENCH_V5: RAC3ITEMDATA.construct_unused(0xC7),
    RAC3ITEM.WRENCH_V6: RAC3ITEMDATA.construct_unused(0xC8),
    RAC3ITEM.WRENCH_V7: RAC3ITEMDATA.construct_unused(0xC9),
    RAC3ITEM.WRENCH_V8: RAC3ITEMDATA.construct_unused(0xCA),
    # Progressive
    RAC3ITEM.PROGRESSIVE_PLASMA_COIL: RAC3ITEMDATA.construct_rac2_prog(0xCB, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_LAVA_GUN: RAC3ITEMDATA.construct_rac2_prog(0xCC, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_BOUNCER: RAC3ITEMDATA.construct_rac2_prog(0xCD, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_MINI_TURRET: RAC3ITEMDATA.construct_rac2_prog(0xCE, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_SHIELD_CHARGER: RAC3ITEMDATA.construct_rac2_prog(0xCF, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_SHOCK_BLASTER: RAC3ITEMDATA.construct_weapon_prog(0xD0, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_N60_STORM: RAC3ITEMDATA.construct_weapon_prog(0xD1, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_INFECTOR:
        RAC3ITEMDATA.construct_weapon_prog(0xD2, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_ANNIHILATOR:
        RAC3ITEMDATA.construct_weapon_prog(0xD3, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_SPITTING_HYDRA:
        RAC3ITEMDATA.construct_weapon_prog(0xD4, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_DISC_BLADE:
        RAC3ITEMDATA.construct_weapon_prog(0xD5, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_AGENTS_OF_DOOM: RAC3ITEMDATA.construct_weapon_prog(0xD6, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_RIFT_INDUCER:
        RAC3ITEMDATA.construct_weapon_prog(0xD7, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_HOLO_SHIELD: RAC3ITEMDATA.construct_weapon_prog(0xD8, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_FLUX_RIFLE:
        RAC3ITEMDATA.construct_weapon_prog(0xD9, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_NITRO_LAUNCHER: RAC3ITEMDATA.construct_weapon_prog(0xDA, ItemClassification.useful),
    RAC3ITEM.PROGRESSIVE_PLASMA_WHIP:
        RAC3ITEMDATA.construct_weapon_prog(0xDB, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_SUCK_CANNON:
        RAC3ITEMDATA.construct_weapon_prog(0xDC, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_QWACK_O_RAY:
        RAC3ITEMDATA.construct_weapon_prog(0xDD, ItemClassification.progression_skip_balancing),
    RAC3ITEM.PROGRESSIVE_RY3N0:
        RAC3ITEMDATA.construct_weapon_prog(0xDE, ItemClassification.progression_skip_balancing, [RAC3ITEMTAG.NGPLUS]),
    # Infobots
    RAC3ITEM.VELDIN: RAC3ITEMDATA.construct_infobot(0xE1, ItemClassification.progression),
    RAC3ITEM.FLORANA: RAC3ITEMDATA.construct_infobot(0xE2, ItemClassification.progression),
    RAC3ITEM.STARSHIP_PHOENIX: RAC3ITEMDATA.construct_infobot(0xE3, ItemClassification.progression),
    RAC3ITEM.MARCADIA: RAC3ITEMDATA.construct_infobot(0xE4, ItemClassification.progression),
    RAC3ITEM.ANNIHILATION_NATION: RAC3ITEMDATA.construct_infobot(0xE5, ItemClassification.progression),
    RAC3ITEM.AQUATOS: RAC3ITEMDATA.construct_infobot(0xE6, ItemClassification.progression),
    RAC3ITEM.TYHRRANOSIS: RAC3ITEMDATA.construct_infobot(0xE7, ItemClassification.progression),
    RAC3ITEM.DAXX: RAC3ITEMDATA.construct_infobot(0xE8, ItemClassification.progression),
    RAC3ITEM.OBANI_GEMINI: RAC3ITEMDATA.construct_infobot(0xE9, ItemClassification.progression),
    RAC3ITEM.BLACKWATER_CITY: RAC3ITEMDATA.construct_infobot(0xEA, ItemClassification.progression),
    RAC3ITEM.HOLOSTAR_STUDIOS: RAC3ITEMDATA.construct_infobot(0xEB, ItemClassification.progression),
    RAC3ITEM.OBANI_DRACO: RAC3ITEMDATA.construct_infobot(0xEC, ItemClassification.progression),
    RAC3ITEM.ZELDRIN_STARPORT: RAC3ITEMDATA.construct_infobot(0xED, ItemClassification.progression),
    RAC3ITEM.METROPOLIS: RAC3ITEMDATA.construct_infobot(0xEE, ItemClassification.progression),
    RAC3ITEM.CRASH_SITE: RAC3ITEMDATA.construct_infobot(0xEF, ItemClassification.progression),
    RAC3ITEM.ARIDIA: RAC3ITEMDATA.construct_infobot(0xF0, ItemClassification.progression),
    RAC3ITEM.QWARKS_HIDEOUT: RAC3ITEMDATA.construct_infobot(0xF1, ItemClassification.progression),
    RAC3ITEM.KOROS: RAC3ITEMDATA.construct_infobot(0xF2, ItemClassification.progression),
    RAC3ITEM.COMMAND_CENTER: RAC3ITEMDATA.construct_infobot(0xF3, ItemClassification.progression),
    RAC3ITEM.MUSEUM: RAC3ITEMDATA.construct_infobot(0xF4, ItemClassification.progression),
    # Armor
    RAC3ITEM.PROGRESSIVE_ARMOR:
        RAC3ITEMDATA.construct_armor(0xF5, ItemClassification.progression, 0, [RAC3ITEMTAG.PROGRESSIVE]),
    RAC3ITEM.MAGNAPLATE: RAC3ITEMDATA.construct_armor(0xF6, ItemClassification.progression, 10),
    RAC3ITEM.ADAMANTINE: RAC3ITEMDATA.construct_armor(0xF7, ItemClassification.progression, 15),
    RAC3ITEM.AEGIS: RAC3ITEMDATA.construct_armor(0xF8, ItemClassification.progression, 20),
    RAC3ITEM.INFERNOX: RAC3ITEMDATA.construct_armor(0xF9, ItemClassification.progression, 24),
    # VidComics
    # In memory they are in order 1,4,2,3,5
    RAC3ITEM.PROGRESSIVE_VIDCOMIC: RAC3ITEMDATA.construct_vidcomic(0xFA, [RAC3ITEMTAG.PROGRESSIVE]),
    RAC3ITEM.VIDCOMIC1: RAC3ITEMDATA.construct_vidcomic(0xFB, [RAC3ITEMTAG.UNUSED]),
    RAC3ITEM.VIDCOMIC2: RAC3ITEMDATA.construct_vidcomic(0xFC, [RAC3ITEMTAG.UNUSED]),
    RAC3ITEM.VIDCOMIC3: RAC3ITEMDATA.construct_vidcomic(0xFD, [RAC3ITEMTAG.UNUSED]),
    RAC3ITEM.VIDCOMIC4: RAC3ITEMDATA.construct_vidcomic(0xFE, [RAC3ITEMTAG.UNUSED]),
    RAC3ITEM.VIDCOMIC5: RAC3ITEMDATA.construct_vidcomic(0xFF, [RAC3ITEMTAG.UNUSED]),
    # Filler
    RAC3ITEM.TITANIUM_BOLT: RAC3ITEMDATA.construct_other(0x100),
    RAC3ITEM.WEAPON_XP: RAC3ITEMDATA.construct_other(0x101),
    RAC3ITEM.PLAYER_XP: RAC3ITEMDATA.construct_other(0x102),
    RAC3ITEM.BOLTS: RAC3ITEMDATA.construct_other(0x103, RAC3STATUS.BOLTS),
    RAC3ITEM.JACKPOT: RAC3ITEMDATA.construct_other(0x104),
    # Traps
    RAC3ITEM.INFERNO_MODE: RAC3ITEMDATA.construct_trap(0x105),
    RAC3ITEM.OHKO_TRAP: RAC3ITEMDATA.construct_trap(0x106),
    RAC3ITEM.NO_AMMO_TRAP: RAC3ITEMDATA.construct_trap(0x107),
    RAC3ITEM.LOCK_TRAP: RAC3ITEMDATA.construct_trap(0x108),
    RAC3ITEM.MIRROR_TRAP: RAC3ITEMDATA.construct_trap(0x109),
    RAC3ITEM.BLACK_SCREEN_TRAP: RAC3ITEMDATA.construct_trap(0x10A),
    RAC3ITEM.NO_CLANK_TRAP: RAC3ITEMDATA.construct_trap(0x10B),
    # Goal
    RAC3ITEM.VICTORY: RAC3ITEMDATA.construct_goal(0x200),
}


def from_prop(prop: str) -> filter:
    return filter(lambda data_kv: getattr(data_kv[1], prop) is not None, RAC3_ITEM_DATA_TABLE.items())


ITEM_FROM_AP_CODE: dict[int, str] = dict((kv[1].AP_CODE, kv[0]) for kv in from_prop("AP_CODE"))
ITEM_NAME_FROM_ID: dict[int, str] = dict((kv[1].ID, kv[0]) for kv in from_prop("ID"))
ITEM_NAME_FROM_ADDRESS: dict[int, str] = dict((kv[1].UNLOCK_ADDRESS, kv[0]) for kv in from_prop("UNLOCK_ADDRESS"))


def from_tag(tag: str) -> dict[str, RAC3ITEMDATA]:
    return dict(filter(lambda data_kv: tag in data_kv[1].TAGS, RAC3_ITEM_DATA_TABLE.items()))


armor_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.ARMOR)
equipable_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.EQUIPABLE)
filler_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.FILLER)
gadget_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.GADGET)
goal_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.GOAL)
infobot_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.INFOBOT)
ngplus_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.NGPLUS)
non_prog_weapon_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.NON_PROG_WEAPON)
prog_weapon_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.PROG_WEAPON)
progressive_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.PROGRESSIVE)
trap_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.TRAP)
unused_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.UNUSED)
vidcomic_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.VIDCOMIC)
weapon_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.WEAPON)
weapon_upgrade_data: dict[str, RAC3ITEMDATA] = from_tag(RAC3ITEMTAG.WEAPON_UPGRADE)

PROG_TO_NAME_DICT: dict[str, str] = dict(zip(prog_weapon_data.keys(), non_prog_weapon_data.keys()))
NAME_TO_PROG_DICT: dict[str, str] = dict(zip(non_prog_weapon_data.keys(), prog_weapon_data.keys()))

item_counts: dict[str, int] = {
    **dict.fromkeys(non_prog_weapon_data.keys(), 1),
    **dict.fromkeys(prog_weapon_data.keys(), 5),
    **dict.fromkeys(gadget_data.keys(), 1),
    RAC3ITEM.PROGRESSIVE_ARMOR: 4,
    RAC3ITEM.PROGRESSIVE_VIDCOMIC: 5,
    **dict.fromkeys(infobot_data.keys(), 1),
    RAC3ITEM.VICTORY: 0,
}
item_table: dict[str, RAC3ITEMDATA] = {
    **non_prog_weapon_data,
    **progressive_data,
    **gadget_data,
    **armor_data,
    **vidcomic_data,
    **infobot_data,
    **filler_data,
    **trap_data,
    **unused_data,
    **weapon_upgrade_data
}
default_starting_weapons: dict[str, int] = {name: 1 for name in non_prog_weapon_data.keys()}
timer_to_status: dict[str, int] = {
    RAC3ITEM.LOCK_TRAP: RAC3STATUS.WEAPON_LOCK,
    RAC3ITEM.MIRROR_TRAP: RAC3STATUS.MIRROR_UNIVERSE,
    RAC3ITEM.BLACK_SCREEN_TRAP: RAC3STATUS.BLACK_SCREEN,
    RAC3ITEM.NO_CLANK_TRAP: RAC3STATUS.NO_CLANK,
}

item_groups: dict[str, set[str]] = {
    RAC3ITEMTAG.ARMOR: set(armor_data.keys()),
    RAC3ITEMTAG.EQUIPABLE: set(equipable_data.keys()),
    RAC3ITEMTAG.FILLER: set(filler_data.keys()),
    RAC3ITEMTAG.GADGET: set(gadget_data.keys()),
    RAC3ITEMTAG.GOAL: set(goal_data.keys()),
    RAC3ITEMTAG.INFOBOT: set(infobot_data.keys()),
    RAC3ITEMTAG.NGPLUS: set(ngplus_data.keys()),
    RAC3ITEMTAG.NON_PROG_WEAPON: set(non_prog_weapon_data.keys()),
    RAC3ITEMTAG.PROG_WEAPON: set(prog_weapon_data.keys()),
    RAC3ITEMTAG.PROGRESSIVE: set(progressive_data.keys()),
    RAC3ITEMTAG.TRAP: set(trap_data.keys()),
    RAC3ITEMTAG.UNUSED: set(unused_data.keys()),
    RAC3ITEMTAG.VIDCOMIC: set(vidcomic_data.keys()),
    RAC3ITEMTAG.WEAPON: set(weapon_data.keys()),
    RAC3ITEMTAG.WEAPON_UPGRADE: set(weapon_upgrade_data.keys()),
}
