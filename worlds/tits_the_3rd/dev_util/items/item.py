from enum import Enum
import json
import os

class WeaponType(Enum):
    STAFF = 1
    TWINSWORDS = 2
    WHIP = 3
    GUN = 4
    RAPIER = 5
    GREATSWORD = 6
    ORBALCANNON = 7
    GAUNTLETS = 8
    CROSSBOW = 9
    KATANA = 10
    TEMPLARSWORD = 11
    SCYTHE = 12

class IconType(Enum):
    STAFF = 1
    TWINSWORDS = 2
    WHIP = 3
    GUN = 4
    RAPIER = 5
    GREATSWORD = 6
    ORBALCANNON = 7
    GAUNTLETS = 8
    CROSSBOW = 9
    KATANA = 11
    TEMPLARSWORD = 28
    SCYTHE = 30

class TargetType(Enum):
    WALK_SINGLE_TARGET = 1
    WALK_AOE = 2

class Weapon():
    id: int

    weapon_type: WeaponType
    target_type: TargetType
    icon_type: IconType

    name: str
    desc: str

    range: int
    strength: int
    defence: int
    arts: int
    art_defence: int
    dexterity: int
    agility: int
    move: int
    speed: int
    aoe_distance: int

    inventory_limit: int
    sell_price: int

    def __init__(
            self, id, weapon_type, target_type, icon_type, name, desc, range,
            strength, defence, arts, art_defence,
            dexterity, agility, move, speed, aoe_distance,
            inventory_limit, sell_price
    ):
        self.id = id
        self.weapon_type = weapon_type
        self.target_type = target_type
        self.icon_type = icon_type
        self.name = name
        self.desc = desc
        self.range = range
        self.strength = strength
        self.defence = defence
        self.arts = arts
        self.art_defence = art_defence
        self.dexterity = dexterity
        self.agility = agility
        self.move = move
        self.speed = speed
        self.aoe_distance = aoe_distance
        self.inventory_limit = inventory_limit
        self.sell_price = sell_price

    def convert_to_t_item_bytes(self):
        out = b""
        out += self.id.to_bytes(2, byteorder="little")
        out += (0xC).to_bytes(1, byteorder="little")  # flags
        out += self.weapon_type.value.to_bytes(1, byteorder="little")
        out += self.icon_type.value.to_bytes(1, byteorder="little")
        out += int(0).to_bytes(1, byteorder="little") # subtype
        out += int(0).to_bytes(3, byteorder="little") # eff1, eff2, eff3
        out += self.target_type.value.to_bytes(1, byteorder="little")
        out += self.range.to_bytes(2, byteorder="little")
        out += (self.aoe_distance + 1).to_bytes(2, byteorder="little")
        out += self.strength.to_bytes(2, byteorder="little")
        out += self.defence.to_bytes(2, byteorder="little")
        out += self.arts.to_bytes(2, byteorder="little")
        out += self.art_defence.to_bytes(2, byteorder="little")
        out += self.agility.to_bytes(2, byteorder="little")
        out += self.dexterity.to_bytes(2, byteorder="little")
        out += self.move.to_bytes(2, byteorder="little")
        out += self.speed.to_bytes(2, byteorder="little")
        out += self.inventory_limit.to_bytes(2, byteorder="little")
        out += self.sell_price.to_bytes(4, byteorder="little")
        return out

    def convert_to_t_ittxt_bytes(self):
        # Assume the item name starts at 0x0. This is overwritten by the inject custom items script.
        out = b""
        out += self.id.to_bytes(4, byteorder="little")
        out += int(0).to_bytes(2, byteorder="little")
        out += int(len(self.name.encode()) + 0x1).to_bytes(2, byteorder="little")
        out += self.name.encode()
        out += int(0).to_bytes(1, byteorder="little")
        out += self.desc.encode()
        out += int(0).to_bytes(1, byteorder="little")
        return out

def _assert_weapon_attributes(weapon: dict):
    expected_attributes = [
        ("type", str),
        ("id", int),
        ("name", str),
        ("desc", str),
        ("range", int),
        ("strength", int),
        ("defence", int),
        ("arts", int),
        ("artDefence", int),
        ("dexterity", int),
        ("agility", int),
        ("move", int),
        ("speed", int),
        ("sellPrice", int),
        ("inventoryLimit", int)
    ]
    if "type" in weapon and weapon["type"].upper() == "ORBALCANNON":
        expected_attributes.append(("aoeRange", int))

    for attribute in expected_attributes:
        if attribute[0] not in weapon:
            raise ValueError(f"Expected to find attribute {attribute[0]} in weapon {weapon}")
        if not isinstance(weapon[attribute[0]], attribute[1]):
            raise ValueError(f"invalid type for attribute {attribute[0]}, expected {attribute[1]} for weapon {weapon}")

    if not weapon["type"].upper() in WeaponType.__members__:
        raise ValueError(f"Type {weapon['type']} is not a valid weapon type")

def _create_weapon_object(weapon: dict):
    aoe_distance = 0
    weapon_type = WeaponType[weapon["type"].upper()]
    icon_type = IconType[weapon["type"].upper()]
    target_type = TargetType.WALK_SINGLE_TARGET
    if weapon_type == WeaponType.ORBALCANNON:
        weapon_type = TargetType.WALK_AOE
        aoe_distance = weapon["aoeRange"]
    return Weapon(
        weapon["id"], weapon_type, target_type, icon_type, weapon["name"], weapon["desc"], weapon["range"],
        weapon["strength"], weapon["defence"], weapon["arts"], weapon["artDefence"], weapon["dexterity"],
        weapon["agility"], weapon["move"], weapon["speed"], aoe_distance, weapon["inventoryLimit"], weapon["sellPrice"]
    )

def read_new_weapons():
    """
    This method parses newWeapons.json, interprets them as Weapon objects, and returns them.

    Returns:
        [Weapon] - The list of weapons defined in ./newWeapons.json
    """
    script_dir = os.path.dirname(os.path.realpath(__file__))
    new_weapons_json = os.path.join(script_dir, "newWeapons.json")
    if not os.path.exists(new_weapons_json):
        raise FileNotFoundError("Could not find newWeapons.json")
    with open(new_weapons_json, encoding="utf-8") as fp:
        weapon_json_list = json.load(fp)
        weapon_object_list = []
        if not isinstance(weapon_json_list, list):
            raise ValueError("Expecting list for newWeapons.json, but found otherwise")
        for weapon in weapon_json_list:
            _assert_weapon_attributes(weapon)
            weapon_object_list.append(_create_weapon_object(weapon))
        return weapon_object_list
