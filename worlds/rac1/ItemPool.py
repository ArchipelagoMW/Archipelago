from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
from .data import Items
from .data.Items import ItemData

if TYPE_CHECKING:
    from . import RacWorld


def get_classification(item: ItemData) -> ItemClassification:
    if item in Items.PLANETS:
        return ItemClassification.progression
    if item in [
        Items.HELI_PACK,
        Items.THRUSTER_PACK,
        Items.HYDRO_PACK,
        Items.SWINGSHOT,
        Items.MAGNEBOOTS,
        Items.GRINDBOOTS,
        Items.HYDRODISPLACER,
        Items.TAUNTER,
        Items.O2_MASK,
        Items.PILOTS_HELMET,
        Items.TRESPASSER,
        Items.HOLOGUISE,
        Items.CODEBOT,
        Items.RARITANIUM,
        Items.HOVERBOARD,
        Items.ZOOMERATOR,
        Items.BOMB_GLOVE,
        Items.DEVASTATOR,
        Items.VISIBOMB,
        Items.METAL_DETECTOR,
    ]:
        return ItemClassification.progression
    if item in [
        Items.BOLT_GRABBER,
        Items.PERSUADER,
        Items.PREMIUM_NANOTECH,
        Items.ULTRA_NANOTECH,
    ]:
        return ItemClassification.useful
    if item in Items.WEAPONS:
        return ItemClassification.useful

    return ItemClassification.filler


def create_planets(world: "RacWorld") -> list["Item"]:
    starting_planet = Items.NOVALIS_INFOBOT
    world.multiworld.push_precollected(world.create_item(starting_planet.name))
    planets_to_add = [planet for planet in Items.PLANETS if planet not in [starting_planet]]
    # add randomization later, just hardcode to get it working
    return [world.create_item(planet.name) for planet in planets_to_add]


def create_equipment(world: "RacWorld") -> list["Item"]:
    equipment_to_add: list[ItemData] = list(Items.EQUIPMENT_AND_WEAPONS)

    # Starting Weapons
    # weapons: list[ItemData] = list(Items.WEAPONS)

    # weapons: list[EquipmentData] = []
    # if world.options.starting_weapons == StartingWeapons.option_balanced:
    #     weapons = [weapon for weapon in Items.LV1_WEAPONS if weapon.power <= 5]
    # elif world.options.starting_weapons == StartingWeapons.option_non_broken:
    #     weapons = [weapon for weapon in Items.LV1_WEAPONS if weapon.power < 10]
    # elif world.options.starting_weapons == StartingWeapons.option_unrestricted:
    #     weapons = list(Items.LV1_WEAPONS)

    # if len(weapons) > 0:
    #     world.random.shuffle(weapons)
    # else:
    weapons = [Items.BOMB_GLOVE]

    world.multiworld.push_precollected(world.create_item(weapons[0].name))
    world.starting_weapons = [weapons[0]]
    # if Items.LANCER not in world.starting_weapons:
    #     equipment_to_add.append(Items.LANCER)
    # if Items.GRAVITY_BOMB not in world.starting_weapons:
    #     equipment_to_add.append(Items.GRAVITY_BOMB)

    # # Gadgetron Vendor
    # if world.options.randomize_gadgetron_vendor:
    #     equipment_to_add += [i for i in Items.GADGETRON_VENDOR_WEAPONS if i not in world.starting_weapons]

    # # Megacorp Vendor
    # if world.options.randomize_megacorp_vendor:
    #     equipment_to_add += [i for i in Items.MEGACORP_VENDOR_WEAPONS if i not in world.starting_weapons]

    # Misc Weapons
    # equipment_to_add += [Items.SHEEPINATOR]

    # Take out expensive items if they are excluded and in the pool.
    # if world.options.exclude_very_expensive_items:
    #     if Items.RYNO_II in equipment_to_add:
    #         location = world.multiworld.get_location(Locations.BARLOW_GADGETRON_5.name, world.player)
    #         location.place_locked_item(world.create_item(Items.RYNO_II.name))
    #         equipment_to_add.remove(Items.RYNO_II)
    #     if Items.ZODIAC in equipment_to_add:
    #         location = world.multiworld.get_location(Locations.ARANOS_VENDOR_WEAPON_2.name, world.player)
    #         location.place_locked_item(world.create_item(Items.ZODIAC.name))
    #         equipment_to_add.remove(Items.ZODIAC)

    # equipment_to_add = [equipment for equipment in equipment_to_add if equipment.item_id not in [starting_weapons[
    # 0].item_id]]
    precollected_ids: list[int] = [item.code for item in world.multiworld.precollected_items[world.player]]
    equipment_to_add = [equipment for equipment in equipment_to_add if equipment.item_id not in precollected_ids]

    return [world.create_item(equipment.name) for equipment in equipment_to_add]


def create_collectables(world: "RacWorld") -> list["Item"]:
    collectable_items: list["Item"] = []

    for _ in range(40):
        collectable_items.append(world.create_item(Items.GOLD_BOLT.name))

    return collectable_items
