from typing import TYPE_CHECKING, List, Union

from BaseClasses import Region

if TYPE_CHECKING:
    from . import SpireWorld, CharacterConfig


def create_regions(world: 'SpireWorld', player: int):
    multiworld = world.multiworld

    menu = world.create_region(player, None, 'Menu', None)
    multiworld.regions.append(menu)
    neow = world.create_region(player, None, "Neow's Room", None )
    multiworld.regions.append(neow)
    menu.connect(neow)

    for config in world.characters:
        _create_regions(world, player, config, neow)

    # link up our region with the entrance we just made
    for region in multiworld.get_regions(player):
        if region.name == 'Menu' or region.name == "Neow's Room":
            continue
        entrance = world.get_entrance(region.name)
        entrance.connect(region)


def _create_regions(world: 'SpireWorld', player: int, config: 'CharacterConfig', neow: Region):
    prefix = config.name
    multiworld = world.multiworld
    first_char_region = world.create_region(player, prefix, 'Early Act 1', config,
                                            [
                                                "Press Start",
                                                "Card Reward 1",
                                                "Card Reward 2",
                                                "Potion Drop 1",
                                                *_create_campfire_check(1),
                                                *_create_floor_check(1,5),
                                                *_create_combat_check(1,2),
                                            ],
                                            ["Mid Act 1", "Act 1 Shop"])

    neow.connect(first_char_region, first_char_region.name)
    multiworld.regions.append(first_char_region)

    multiworld.regions.append(world.create_region(player, prefix, "Act 1 Shop", config,
                              [f"Shop Slot {i}" for i in range(1,6)]))

    multiworld.regions.append(world.create_region(player, prefix, 'Mid Act 1', config,
                                            [
                                                'Card Reward 3',
                                                'Card Reward 4',
                                                'Relic 1',
                                                'Relic 2',
                                                'Elite Gold 1',
                                                "Potion Drop 2",
                                                *_create_floor_check(6, 10),
                                                *_create_combat_check(3, 4),
                                            ],["Late Act 1"]))

    multiworld.regions.append(world.create_region(player, prefix, 'Late Act 1', config,
                                            [
                                                'Relic 3',
                                                'Elite Gold 2',
                                                "Potion Drop 3",
                                                *_create_floor_check(11, 15),
                                                *_create_combat_check(5, 6),
                                            ], ['Act 1 Boss Arena']))

    multiworld.regions.append(world.create_region(player, prefix, 'Act 1 Boss Arena', config,
                                            [
                                                'Act 1 Boss',
                                                'Rare Card Reward 1',
                                                'Boss Relic 1',
                                                'Boss Gold 1',
                                                * _create_floor_check(16, 17)
                                            ], ['Early Act 2']))

    multiworld.regions.append(world.create_region(player, prefix, 'Early Act 2', config,
                                            [
                                                "Card Reward 5",
                                                "Card Reward 6",
                                                "Potion Drop 4",
                                                *_create_campfire_check(2),
                                                *_create_floor_check(18, 22),
                                                *_create_combat_check(7, 8),
                                            ], ["Mid Act 2", "Act 2 Shop"]))

    multiworld.regions.append(world.create_region(player, prefix, "Act 2 Shop", config,
                                                  [f"Shop Slot {i}" for i in range(6,11)]))
    multiworld.regions.append(world.create_region(player, prefix, 'Mid Act 2', config,
                                            [
                                                'Card Reward 7',
                                                'Relic 4',
                                                'Relic 5',
                                                'Elite Gold 3',
                                                "Potion Drop 5",
                                                *_create_floor_check(23, 27),
                                                *_create_combat_check(9, 10),
                                            ], ["Late Act 2"]))

    multiworld.regions.append(world.create_region(player, prefix, 'Late Act 2', config,
                                            [
                                                'Card Reward 8',
                                                'Relic 6',
                                                'Elite Gold 4',
                                                "Potion Drop 6",
                                                *_create_floor_check(28, 32),
                                                *_create_combat_check(11, 12),
                                            ], ['Act 2 Boss Arena']))

    multiworld.regions.append(world.create_region(player, prefix, 'Act 2 Boss Arena', config,
                                            [
                                                'Act 2 Boss',
                                                'Rare Card Reward 2',
                                                'Boss Relic 2',
                                                'Boss Gold 2',
                                                *_create_floor_check(33, 34),
                                            ], ['Early Act 3']))

    multiworld.regions.append(world.create_region(player, prefix, 'Early Act 3', config,
                                            [
                                                "Card Reward 9",
                                                "Card Reward 10",
                                                "Potion Drop 7",
                                                *_create_campfire_check(3),
                                                *_create_floor_check(35, 39),
                                                *_create_combat_check(13, 14),
                                            ], ["Mid Act 3", "Act 3 Shop"]))

    multiworld.regions.append(world.create_region(player, prefix, "Act 3 Shop", config,
                                                  [f"Shop Slot {i}" for i in range(11,17)]))

    multiworld.regions.append(world.create_region(player, prefix, 'Mid Act 3', config,
                                            [
                                                "Card Reward 11",
                                                "Relic 7",
                                                "Relic 8",
                                                'Elite Gold 5',
                                                "Potion Drop 8",
                                                *_create_floor_check(40, 44),
                                                *_create_combat_check(15, 16),
                                            ], ["Late Act 3"]))


    multiworld.regions.append(world.create_region(player, prefix, 'Late Act 3', config,
                                            [
                                                "Card Reward 12",
                                                "Card Reward 13",
                                                "Relic 9",
                                                "Relic 10",
                                                'Elite Gold 6',
                                                'Elite Gold 7',
                                                "Potion Drop 9",
                                                *_create_floor_check(45, 49),
                                                *_create_combat_check(17, 18),
                                            ], ['Act 3 Boss Arena']))

    acension_mod = 1 if config.ascension >= 20 else 0

    multiworld.regions.append(world.create_region(player, prefix, 'Act 3 Boss Arena', config,
                                            [
                                                "Act 3 Boss",
                                                *_create_floor_check(50, 51 + acension_mod),
                                            ], ["Act 4"]))

    multiworld.regions.append(world.create_region(player, prefix, 'Act 4', config,
                                            [
                                                "Heart Room",
                                                *(_create_floor_check(52 + acension_mod,55 + acension_mod) if config.final_act else [])
                                            ]))


def _create_floor_check(start: int, end: int) -> List[str]:
    return [f"Reached Floor {i}" for i in range(start, end + 1)]

def _create_combat_check(start: int, end: int) -> List[str]:
    return [f"Combat Gold {i}" for i in range(start, end + 1)]

def _create_campfire_check(act: int) -> List[str]:
    return [f"Act {act} Campfire 1", f"Act {act} Campfire 2"]