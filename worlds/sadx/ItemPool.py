import math
from typing import List

from BaseClasses import ItemClassification
from Options import OptionError
from worlds.AutoWorld import World
from .CharacterUtils import get_playable_character_item, is_character_playable, are_character_upgrades_randomized, \
    get_character_upgrades_item
from .Enums import Character
from .Items import filler_item_table
from .Names import ItemName, LocationName
from .Options import SonicAdventureDXOptions
from .StartingSetup import StarterSetup


class ItemDistribution:
    def __init__(self, emblem_count_progressive=0, emblem_count_non_progressive=0, filler_count=0, trap_count=0):
        self.emblem_count_progressive = emblem_count_progressive
        self.emblem_count_non_progressive = emblem_count_non_progressive
        self.filler_count = filler_count
        self.trap_count = trap_count


def create_sadx_items(world: World, starter_setup: StarterSetup, options: SonicAdventureDXOptions):
    item_names = get_item_names(options, starter_setup)

    # Remove the items that are already in the starting inventory
    for item in world.options.start_inventory:
        for _ in range(world.options.start_inventory[item]):
            item_names.remove(item)

    # Calculate the number of items per type
    item_distribution = get_item_distribution(world, len(item_names), options)

    # Character Upgrades and removal of from the item pool
    place_not_randomized_upgrades(world, options, item_names)

    # Keys and Characters Items
    itempool = [world.create_item(item_name) for item_name in item_names]

    # Emblems
    for _ in range(item_distribution.emblem_count_progressive):
        itempool.append(world.create_item(ItemName.Progression.Emblem))

    for _ in range(item_distribution.emblem_count_non_progressive):
        item = world.create_item(ItemName.Progression.Emblem)
        item.classification = ItemClassification.filler
        itempool.append(item)

    # Filler
    for _ in range(item_distribution.filler_count):
        itempool.append(world.create_item(world.random.choice(filler_item_table).name))

    # Traps
    trap_weights = (
            [ItemName.Traps.IceTrap] * options.ice_trap_weight.value +
            [ItemName.Traps.SpringTrap] * options.spring_trap_weight.value +
            [ItemName.Traps.PoliceTrap] * options.police_trap_weight.value +
            [ItemName.Traps.BuyonTrap] * options.buyon_trap_weight.value +
            [ItemName.Traps.ReverseTrap] * options.reverse_trap_weight.value +
            [ItemName.Traps.GravityTrap] * options.gravity_trap_weight.value
    )

    if len(trap_weights) == 0:
        for _ in range(item_distribution.trap_count):
            itempool.append(world.create_item(world.random.choice(filler_item_table).name))
    else:
        for _ in range(item_distribution.trap_count):
            itempool.append(world.create_item(world.random.choice(trap_weights)))

    world.multiworld.push_precollected(world.create_item(get_playable_character_item(starter_setup.character)))

    world.multiworld.itempool += itempool
    return item_distribution


def get_item_distribution(world: World, starting_item_count: int, options: SonicAdventureDXOptions) -> ItemDistribution:
    location_count = sum(1 for location in world.multiworld.get_locations(world.player) if not location.locked)
    available_locations = location_count - starting_item_count

    if available_locations < 0:
        raise OptionError(
            "SADX Error: There are not enough available locations to place required items for the selected options. "
            + "Please enable more more checks, you need at least {} more locations.".format(-available_locations))

    # If Emblems are enabled, we calculate how many progressive emblems and filler emblems we need
    if options.goal_requires_emblems.value:
        if available_locations < 5:
            raise OptionError("SADX Error: There are not enough available locations to place Emblems. "
                              + "Please enable more more checks or change your goal. "
                              + "You need at least {} more locations.".format(5 - available_locations))

        total_emblems = min(available_locations, options.max_emblem_cap.value)
        emblem_count_progressive = max(1, math.ceil(total_emblems * options.emblems_percentage.value / 100.0))
        emblem_count_non_progressive = total_emblems - emblem_count_progressive
        emblems_to_filler = math.floor(emblem_count_non_progressive * (options.junk_fill_percentage.value / 100.0))
        junk_count = available_locations - total_emblems + emblems_to_filler
        emblem_count_non_progressive -= emblems_to_filler
    # If not, all the remaining locations are filler
    else:
        emblem_count_progressive = 0
        emblem_count_non_progressive = 0
        junk_count = available_locations

    trap_count = math.floor(junk_count * (options.trap_fill_percentage.value / 100.0))
    filler_count = junk_count - trap_count

    return ItemDistribution(
        emblem_count_progressive=emblem_count_progressive,
        emblem_count_non_progressive=emblem_count_non_progressive,
        filler_count=filler_count,
        trap_count=trap_count
    )


def get_item_names(options: SonicAdventureDXOptions, starter_setup: StarterSetup) -> List[str]:
    item_names = sum((get_item_for_options_per_character(character, options) for character in Character), [])
    item_names += [
        ItemName.KeyItem.Train, ItemName.KeyItem.Boat, ItemName.KeyItem.Raft, ItemName.KeyItem.StationFrontKey,
        ItemName.KeyItem.StationBackKey, ItemName.KeyItem.HotelFrontKey, ItemName.KeyItem.HotelBackKey,
        ItemName.KeyItem.TwinkleParkTicket,
        ItemName.KeyItem.EmployeeCard, ItemName.KeyItem.Dynamite, ItemName.KeyItem.JungleCart,
        ItemName.KeyItem.IceStone, ItemName.KeyItem.WindStone, ItemName.KeyItem.Egglift, ItemName.KeyItem.Monorail
    ]

    if options.goal_requires_chaos_emeralds.value:
        item_names += [
            ItemName.Progression.WhiteEmerald, ItemName.Progression.RedEmerald, ItemName.Progression.CyanEmerald,
            ItemName.Progression.PurpleEmerald, ItemName.Progression.GreenEmerald, ItemName.Progression.YellowEmerald,
            ItemName.Progression.BlueEmerald
        ]

    item_names.remove(get_playable_character_item(starter_setup.character))

    return item_names


def get_item_for_options_per_character(character: Character, options: SonicAdventureDXOptions) -> List[str]:
    if not is_character_playable(character, options):
        return []
    return [get_playable_character_item(character)] + get_character_upgrades_item(character)


def place_not_randomized_upgrades(world: World, options: SonicAdventureDXOptions, item_names: List[str]):
    upgrades = {
        Character.Sonic: [
            (LocationName.Sonic.LightShoes, ItemName.Sonic.LightShoes),
            (LocationName.Sonic.CrystalRing, ItemName.Sonic.CrystalRing),
            (LocationName.Sonic.AncientLight, ItemName.Sonic.AncientLight)
        ],
        Character.Tails: [
            (LocationName.Tails.JetAnklet, ItemName.Tails.JetAnklet),
            (LocationName.Tails.RhythmBadge, ItemName.Tails.RhythmBadge)
        ],
        Character.Knuckles: [
            (LocationName.Knuckles.ShovelClaw, ItemName.Knuckles.ShovelClaw),
            (LocationName.Knuckles.FightingGloves, ItemName.Knuckles.FightingGloves)
        ],
        Character.Amy: [
            (LocationName.Amy.WarriorFeather, ItemName.Amy.WarriorFeather),
            (LocationName.Amy.LongHammer, ItemName.Amy.LongHammer)
        ],
        Character.Big: [
            (LocationName.Big.LifeBelt, ItemName.Big.LifeBelt),
            (LocationName.Big.PowerRod, ItemName.Big.PowerRod),
            (LocationName.Big.Lure1, ItemName.Big.Lure1),
            (LocationName.Big.Lure2, ItemName.Big.Lure2),
            (LocationName.Big.Lure3, ItemName.Big.Lure3),
            (LocationName.Big.Lure4, ItemName.Big.Lure4)
        ],
        Character.Gamma: [
            (LocationName.Gamma.JetBooster, ItemName.Gamma.JetBooster),
            (LocationName.Gamma.LaserBlaster, ItemName.Gamma.LaserBlaster)
        ]
    }

    for character, upgrades in upgrades.items():
        if is_character_playable(character, options) and not are_character_upgrades_randomized(character, options):
            for location_name, item_name in upgrades:
                world.multiworld.get_location(location_name, world.player).place_locked_item(
                    world.create_item(item_name))
                item_names.remove(item_name)
