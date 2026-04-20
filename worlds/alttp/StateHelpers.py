from .SubClasses import LTTPRegion
from BaseClasses import CollectionState


def is_not_bunny(state: CollectionState, region: LTTPRegion, player: int) -> bool:
    if state.has('Moon Pearl', player):
        return True

    return region.is_light_world if state.multiworld.worlds[player].options.mode != 'inverted' else region.is_dark_world


def can_bomb_clip(state: CollectionState, region: LTTPRegion, player: int) -> bool:
    return can_use_bombs(state, player) and is_not_bunny(state, region, player) and state.has('Pegasus Boots', player)


def can_buy_unlimited(state: CollectionState, item: str, player: int) -> bool:
    return any(shop.has_unlimited(item) and shop.region.can_reach(state) for
               shop in state.multiworld.worlds[player].shops)


def can_buy(state: CollectionState, item: str, player: int) -> bool:
    return any(shop.has(item) and shop.region.can_reach(state) for
               shop in state.multiworld.worlds[player].shops)


def can_shoot_arrows(state: CollectionState, player: int, count: int = 0) -> bool:
    if state.multiworld.worlds[player].options.retro_bow:
        return (state.has('Bow', player) or state.has('Silver Bow', player)) and can_buy(state, 'Single Arrow', player)
    return (state.has('Bow', player) or state.has('Silver Bow', player)) and can_hold_arrows(state, player, count)


def has_triforce_pieces(state: CollectionState, player: int) -> bool:
    count = state.multiworld.worlds[player].treasure_hunt_required
    return state.count('Triforce Piece', player) + state.count('Power Star', player) >= count


def has_crystals(state: CollectionState, count: int, player: int) -> bool:
    found = state.count_group("Crystals", player)
    return found >= count


def can_lift_rocks(state: CollectionState, player: int):
    return state.has('Power Glove', player) or state.has('Titans Mitts', player)


def can_lift_heavy_rocks(state: CollectionState, player: int) -> bool:
    return state.has('Titans Mitts', player)


def bottle_count(state: CollectionState, player: int) -> int:
    return min(state.multiworld.worlds[player].difficulty_requirements.progressive_bottle_limit,
               state.count_group("Bottles", player))


def has_hearts(state: CollectionState, player: int, count: int) -> int:
    # Warning: This only considers items that are marked as advancement items
    return heart_count(state, player) >= count


def heart_count(state: CollectionState, player: int) -> int:
    # Warning: This only considers items that are marked as advancement items
    max_heart_pieces = state.multiworld.worlds[player].logical_heart_pieces
    max_heart_containers = state.multiworld.worlds[player].logical_heart_containers
    return min(state.count('Boss Heart Container', player), max_heart_containers) \
        + state.count('Sanctuary Heart Container', player) \
        + min(state.count('Piece of Heart', player), max_heart_pieces) // 4 \
        + 3  # starting hearts


def can_extend_magic(state: CollectionState, player: int, smallmagic: int = 16,
                     fullrefill: bool = False):  # This reflects the total magic Link has, not the total extra he has.
    basemagic = 8
    if state.has('Magic Upgrade (1/4)', player):
        basemagic = 32
    elif state.has('Magic Upgrade (1/2)', player):
        basemagic = 16
    if can_buy_unlimited(state, 'Green Potion', player) or can_buy_unlimited(state, 'Blue Potion', player):
        if state.multiworld.worlds[player].options.item_functionality == 'hard' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.5 * bottle_count(state, player))
        elif state.multiworld.worlds[player].options.item_functionality == 'expert' and not fullrefill:
            basemagic = basemagic + int(basemagic * 0.25 * bottle_count(state, player))
        else:
            basemagic = basemagic + basemagic * bottle_count(state, player)
    return basemagic >= smallmagic


def can_hold_arrows(state: CollectionState, player: int, quantity: int):
    if state.multiworld.worlds[player].options.shuffle_capacity_upgrades:
        if quantity == 0:
            return True
        if state.has("Arrow Upgrade (70)", player):
            arrows = 70
        else:
            arrows = (30 + (state.count("Arrow Upgrade (+5)", player) * 5)
                      + (state.count("Arrow Upgrade (+10)", player) * 10))
            # Arrow Upgrade (+5) beyond the 6th gives +10
            arrows += max(0, ((state.count("Arrow Upgrade (+5)", player) - 6) * 10))
        return min(70, arrows) >= quantity
    return quantity <= 30 or state.has("Capacity Upgrade Shop", player)


def can_use_bombs(state: CollectionState, player: int, quantity: int = 1) -> bool:
    bombs = 0 if state.multiworld.worlds[player].options.bombless_start else 10
    bombs += ((state.count("Bomb Upgrade (+5)", player) * 5) + (state.count("Bomb Upgrade (+10)", player) * 10)
              + (state.count("Bomb Upgrade (50)", player) * 50))
    # Bomb Upgrade (+5) beyond the 6th gives +10
    bombs += max(0, ((state.count("Bomb Upgrade (+5)", player) - 6) * 10))
    if (not state.multiworld.worlds[player].options.shuffle_capacity_upgrades) and state.has("Capacity Upgrade Shop", player):
        bombs += 40
    return bombs >= min(quantity, 50)


def can_bomb_or_bonk(state: CollectionState, player: int) -> bool:
    return state.has("Pegasus Boots", player) or can_use_bombs(state, player)


def can_activate_crystal_switch(state: CollectionState, player: int) -> bool:
    return (has_melee_weapon(state, player) or can_use_bombs(state, player) or can_shoot_arrows(state, player)
            or state.has_any(["Hookshot", "Cane of Somaria", "Cane of Byrna", "Fire Rod", "Ice Rod", "Blue Boomerang",
                              "Red Boomerang"], player))


def can_clear_enemy_room(state: CollectionState, player: int, room_name_or_id: str | int) -> bool:
    from .EnemyShuffle import get_effective_dungeon_room_sprite_requirements, get_room_id

    room_id = room_name_or_id if isinstance(room_name_or_id, int) else get_room_id(room_name_or_id)
    if room_id is None:
        raise ValueError(f"Unknown ALTTP room {room_name_or_id!r}")

    room_enemies = tuple(
        requirement
        for requirement in get_effective_dungeon_room_sprite_requirements(state.multiworld.worlds[player], room_id)
        if requirement.killable
    )
    if not room_enemies:
        return True

    available_damage_classes = _get_available_damage_classes(state, player, len(room_enemies))
    for requirement in room_enemies:
        if _can_kill_enemy_requirement(state, player, requirement, len(room_enemies), available_damage_classes):
            continue
        return False
    return True


def _can_kill_enemy_requirement(
    state: CollectionState,
    player: int,
    requirement,
    enemy_count: int,
    available_damage_classes: set[int],
) -> bool:
    direct_damage_classes = set(requirement.kill_damage_classes)
    direct_kill_items = requirement.kill_items

    if requirement.yellow_slime_transform_items:
        transform_damage_classes = {
            _get_kill_item_damage_class(item_name)
            for item_name in requirement.yellow_slime_transform_items
        }
        direct_damage_classes -= transform_damage_classes
        direct_kill_items = tuple(
            item_name
            for item_name in requirement.kill_items
            if item_name not in requirement.yellow_slime_transform_items
        )

    if available_damage_classes.intersection(direct_damage_classes):
        return True
    if _can_use_guide_kill_items(state, player, direct_kill_items, enemy_count):
        return True
    if _can_use_guide_kill_abilities(state, player, requirement.kill_abilities, enemy_count):
        return True

    if requirement.yellow_slime_transform_items:
        return (
            _can_use_guide_kill_items(state, player, requirement.yellow_slime_transform_items, enemy_count)
            and (
                _can_use_guide_kill_items(state, player, requirement.yellow_slime_follow_up_items, enemy_count)
                or _can_use_guide_kill_abilities(
                    state,
                    player,
                    requirement.yellow_slime_follow_up_abilities,
                    enemy_count,
                )
            )
        )

    return False


def _get_available_damage_classes(state: CollectionState, player: int, enemy_count: int) -> set[int]:
    available_damage_classes: set[int] = set()

    if state.has("Fighter Sword", player):
        available_damage_classes.add(2)
    if state.has("Master Sword", player):
        available_damage_classes.add(3)
    if state.has("Tempered Sword", player):
        available_damage_classes.add(4)
    if state.has("Golden Sword", player):
        available_damage_classes.add(5)
    if state.has("Hammer", player):
        available_damage_classes.add(3)
    if state.has("Blue Boomerang", player) or state.has("Red Boomerang", player):
        available_damage_classes.add(0)
    if state.has("Hookshot", player):
        available_damage_classes.add(7)
    if can_shoot_arrows(state, player, enemy_count):
        if state.has("Bow", player):
            available_damage_classes.add(6)
        if state.has("Silver Bow", player) or (state.has("Bow", player) and state.has("Silver Arrows", player)):
            available_damage_classes.add(9)
    if can_use_bombs(state, player, enemy_count):
        available_damage_classes.add(8)
    if state.has("Cane of Somaria", player):
        available_damage_classes.add(1)
    if state.has("Cane of Byrna", player) and can_extend_magic(state, player, 8):
        available_damage_classes.add(1)
    if state.has("Magic Powder", player):
        available_damage_classes.add(10)
    if state.has("Fire Rod", player) and can_extend_magic(state, player, 8 * enemy_count):
        available_damage_classes.add(11)
    if state.has("Ice Rod", player) and can_extend_magic(state, player, 8 * enemy_count):
        available_damage_classes.add(12)
    if state.has("Bombos", player) and _can_cast_medallion(state, player):
        available_damage_classes.add(13)
    if state.has("Ether", player) and _can_cast_medallion(state, player):
        available_damage_classes.add(14)
    if state.has("Quake", player) and _can_cast_medallion(state, player):
        available_damage_classes.add(15)

    return available_damage_classes


def _can_use_guide_kill_items(state: CollectionState, player: int, kill_items: tuple[str, ...], enemy_count: int) -> bool:
    return any(
        _can_use_guide_kill_item(state, player, kill_item, enemy_count)
        for kill_item in kill_items
    )


def _can_use_guide_kill_abilities(
    state: CollectionState,
    player: int,
    kill_abilities: tuple[str, ...],
    enemy_count: int,
) -> bool:
    return any(
        _can_use_guide_kill_ability(state, player, kill_ability, enemy_count)
        for kill_ability in kill_abilities
    )


def _get_kill_item_damage_class(kill_item: str) -> int:
    from .EnemyShuffle import ITEM_NAME_TO_DAMAGE_CLASS

    return ITEM_NAME_TO_DAMAGE_CLASS[kill_item]


def _can_use_guide_kill_item(state: CollectionState, player: int, kill_item: str, enemy_count: int) -> bool:
    if kill_item in {"Blue Boomerang", "Red Boomerang"}:
        return state.has(kill_item, player)
    if kill_item in {"Fighter Sword", "Master Sword", "Tempered Sword", "Golden Sword", "Hammer"}:
        return state.has(kill_item, player)
    if kill_item in {"Cane of Somaria", "Cane of Byrna"}:
        return state.has(kill_item, player)
    if kill_item == "Bow":
        return state.has("Bow", player) and can_shoot_arrows(state, player, enemy_count)
    if kill_item == "Silver Bow":
        return (state.has("Silver Bow", player) or (state.has("Bow", player) and state.has("Silver Arrows", player))) \
            and can_shoot_arrows(state, player, enemy_count)
    if kill_item == "Hookshot":
        return state.has("Hookshot", player)
    if kill_item == "Magic Powder":
        return state.has("Magic Powder", player)
    if kill_item == "Fire Rod":
        return state.has("Fire Rod", player) and can_extend_magic(state, player, 8 * enemy_count)
    if kill_item == "Ice Rod":
        return state.has("Ice Rod", player) and can_extend_magic(state, player, 8 * enemy_count)
    if kill_item == "Bombos":
        return state.has("Bombos", player) and _can_cast_medallion(state, player)
    if kill_item == "Ether":
        return state.has("Ether", player) and _can_cast_medallion(state, player)
    if kill_item == "Quake":
        return state.has("Quake", player) and _can_cast_medallion(state, player)
    return False


def _can_use_guide_kill_ability(state: CollectionState, player: int, kill_ability: str, enemy_count: int) -> bool:
    if kill_ability == "bombs":
        return can_use_bombs(state, player, enemy_count)
    return False


def _can_cast_medallion(state: CollectionState, player: int) -> bool:
    return (state.multiworld.worlds[player].options.swordless or has_sword(state, player)) and can_extend_magic(state, player, 16)


def can_kill_most_things(state: CollectionState, player: int, enemies: int = 5) -> bool:
    if state.multiworld.worlds[player].options.enemy_shuffle:
        # I don't fully understand Enemizer's logic for placing enemies in spots where they need to be killable, if any.
        # Just go with maximal requirements for now.
        return (has_melee_weapon(state, player)
                and state.has('Cane of Somaria', player)
                and state.has('Cane of Byrna', player) and can_extend_magic(state, player)
                and can_shoot_arrows(state, player)
                and state.has('Fire Rod', player)
                and can_use_bombs(state, player, enemies * 4))
    else:
        return (has_melee_weapon(state, player)
                or state.has('Cane of Somaria', player)
                or (state.has('Cane of Byrna', player) and (enemies < 6 or can_extend_magic(state, player)))
                or can_shoot_arrows(state, player)
                or state.has('Fire Rod', player)
                or (state.multiworld.worlds[player].options.enemy_health in ("easy", "default")
                    and can_use_bombs(state, player, enemies * 4)))


def can_kill_standard_start(state: CollectionState, player: int, enemies: int = 5) -> bool:
    # Enemizer does not randomize standard start enemies
        return (has_melee_weapon(state, player)
                or state.has('Cane of Somaria', player)
                or (state.has('Cane of Byrna', player) and (enemies < 6 or can_extend_magic(state, player)))
                or state.has_any(["Bow", "Progressive Bow"], player)
                or state.has('Fire Rod', player)
                or can_use_bombs(state, player, enemies)) # Escape assist is set


def can_get_good_bee(state: CollectionState, player: int) -> bool:
    cave = state.multiworld.get_region('Good Bee Cave', player)
    return (
            state.has_group("Bottles", player) and
            state.has('Bug Catching Net', player) and
            (state.has('Pegasus Boots', player) or (has_sword(state, player) and state.has('Quake', player))) and
            cave.can_reach(state) and
            is_not_bunny(state, cave, player)
    )


def can_retrieve_tablet(state: CollectionState, player: int) -> bool:
    return state.has('Book of Mudora', player) and (has_beam_sword(state, player) or
                                                    (state.multiworld.worlds[player].options.swordless and
                                                     state.has("Hammer", player)))


def has_sword(state: CollectionState, player: int) -> bool:
    return state.has('Fighter Sword', player) \
        or state.has('Master Sword', player) \
        or state.has('Tempered Sword', player) \
        or state.has('Golden Sword', player)


def has_beam_sword(state: CollectionState, player: int) -> bool:
    return state.has('Master Sword', player) or state.has('Tempered Sword', player) or state.has('Golden Sword',
                                                                                                 player)


def has_melee_weapon(state: CollectionState, player: int) -> bool:
    return has_sword(state, player) or state.has('Hammer', player)


def has_fire_source(state: CollectionState, player: int) -> bool:
    return state.has('Fire Rod', player) or state.has('Lamp', player)


def can_melt_things(state: CollectionState, player: int) -> bool:
    return state.has('Fire Rod', player) or \
        (state.has('Bombos', player) and
         (state.multiworld.worlds[player].options.swordless or
          has_sword(state, player)))


def has_misery_mire_medallion(state: CollectionState, player: int) -> bool:
    return state.has(state.multiworld.worlds[player].required_medallions[0], player)


def has_turtle_rock_medallion(state: CollectionState, player: int) -> bool:
    return state.has(state.multiworld.worlds[player].required_medallions[1], player)


def can_boots_clip_lw(state: CollectionState, player: int) -> bool:
    if state.multiworld.worlds[player].options.mode == 'inverted':
        return state.has('Pegasus Boots', player) and state.has('Moon Pearl', player)
    return state.has('Pegasus Boots', player)


def can_boots_clip_dw(state: CollectionState, player: int) -> bool:
    if state.multiworld.worlds[player].options.mode != 'inverted':
        return state.has('Pegasus Boots', player) and state.has('Moon Pearl', player)
    return state.has('Pegasus Boots', player)


def can_get_glitched_speed_dw(state: CollectionState, player: int) -> bool:
    rules = [state.has('Pegasus Boots', player), any([state.has('Hookshot', player), has_sword(state, player)])]
    if state.multiworld.worlds[player].options.mode != 'inverted':
        rules.append(state.has('Moon Pearl', player))
    return all(rules)
