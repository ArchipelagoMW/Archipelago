from typing import TYPE_CHECKING

from . import Processor

if TYPE_CHECKING:
    from ... import Shapez2World


_count = 0


def next_id(restart=False) -> int:
    global _count
    if restart:
        _count = 0
    _count += 1
    return _count - 1


class Variant:
    full = next_id(True)  # always
    half = next_id()  # cutter & 1
    half_half = next_id()  # (swapper & 1) | (cutter & rotator & stacker & 6)
    cut_out_5 = next_id()  # cutter & rotator & ((stacker & 6) | (swapper & 4))
    cut_out_4 = next_id()  # cutter & rotator & ((stacker & 5) | (swapper & 3))
    _5_1 = next_id()  # rotator & ((cutter & stacker & 12) | (swapper & 3))
    _4_2 = next_id()  # rotator & ((cutter & stacker & 13) | (swapper & 4))
    cornered = next_id()  # cutter & rotator & ((stacker & 10) | (swapper & 6))
    cornered_2 = next_id()  # cutter & rotator & ((stacker & 9) | (swapper & 6))
    cornered_1_1 = next_id()  # cutter & rotator & ((stacker & 21) | (swapper & 10))
    cornered_atomic = next_id()  # cutter & rotator & ((stacker & 16) | (swapper & 8))
    cornered_asymmetrical = next_id()  # cutter & rotator & ((stacker & 21) | (swapper & 9))
    checkered = next_id()  # rotator & ((cutter & stacker & 32) | (swapper & 9))
    checkered_2_1 = next_id()  # rotator & ((cutter & stacker & 21) | (swapper & 4))
    checkered_atomic = next_id()  # rotator & ((cutter & stacker & 32) | (swapper & 7))
    checkered_asymmetrical = next_id()  # rotator & ((cutter & stacker & 20) | (swapper & 5))
    _3_doubles = next_id()  # rotator & ((cutter & stacker & 14) | (swapper & 5))
    pins = next_id()  # pins

    begin_crystals = next_id()

    full_crystal = next_id()  # crystal & ((pins & 1) | (cutter & rotator & 7))
    half_crystal = next_id()  # crystal & cutter & rotator & 6
    half_half_crystal = next_id()  # crystal & cutter & rotator & 6
    half_crystal_half_shape = next_id()  # crystal & cutter & 2
    cut_out_5_crystal = next_id()  # (crystal & cutter & rotator & swapper & 9)
    cut_out_4_crystal = next_id()  # (crystal & cutter & rotator & swapper & 11)
    _5_1_crystals = next_id()  # (crystal & cutter & rotator & 8)
    _4_2_crystals = next_id()  # (crystal & cutter & rotator & 8)
    _5_crystals_1_shape = next_id()  # (crystal & cutter & rotator & 5)
    _5_shapes_1_crystal = next_id()  # crystal & cutter & rotator & ((stacker & 8) | (swapper & 4))
    _4_crystals_2_shape = next_id()  # (crystal & cutter & rotator & 4)
    _4_shapes_2_crystal = next_id()  # crystal & cutter & rotator & ((stacker & 8) | (swapper & 4))
    cornered_crystal = next_id()  # (crystal & cutter & rotator & swapper & 12)
    cornered_2_crystal = next_id()  # (crystal & cutter & rotator & swapper & 14)
    cornered_atomic_crystal = next_id()  # (crystal & cutter & rotator & swapper & 26)
    cornered_asymmetrical_crystal = next_id()  # (crystal & cutter & rotator & swapper & 18)
    checkered_crystal = next_id()  # (crystal & cutter & rotator & swapper & 20)
    checkered_2x_crystal_shape = next_id()  # (crystal & cutter & rotator & swapper & 14)
    checkered_2x_shape_crystal = next_id()  # crystal & cutter & rotator & ((stacker & 23) | (swapper & 12))
    checkered_2_1_crystal = next_id()  # (crystal & cutter & rotator & swapper & 13)
    checkered_2_1_crystal_shape = next_id()  # crystal & cutter & rotator & ((stacker & 11) | (swapper & 7))
    checkered_2_1_shape_crystal = next_id()  # crystal & cutter & rotator & ((stacker & 10) | (swapper & 7))
    checkered_atomic_crystal = next_id()  # (crystal & cutter & rotator & swapper & 20)
    checkered_atomic_crystal_shape = next_id()  # crystal & cutter & rotator & ((stacker & 17) | (swapper & 9))
    _3_doubles_crystal = next_id()  # (crystal & cutter & rotator & swapper & 15)

    end_crystals = next_id()

    # Can have crystals, but not necessary
    single = next_id()  # cutter & rotator & 4
    double = next_id()  # cutter & rotator & 3
    _2_singles = next_id()  # cutter & rotator & ((stacker & 9) | (swapper & 6))
    _2_doubles = next_id()  # cutter & rotator & ((stacker & 8) | (swapper & 6))
    _5_singles = next_id()  # cutter & rotator & ((stacker & 26) | (swapper & 9))
    _6_singles = next_id()  # rotator & ((cutter & stacker & 32) | (swapper & 9))

    end = next_id()

    __remove = next_id()  # For removing pin layers entirely


def generate_layer(world: "Shapez2World", complexity: int, shape: list[str],
                   available: list[Processor], tasked: list[bool], important: bool) -> None:

    if important and (sum(tasked) > complexity or (
        sum(tasked) + 1 > complexity and tasked[Processor.ROTATOR] and (
            not tasked[Processor.CUTTER] or not tasked[Processor.SWAPPER]
        )
    )):
        raise Exception(f"Too low complexity ({complexity}) "
                        f"for important processors {', '.join(str(i) for i in range(8) if tasked[i])}")

    already_has_crystals = any(x == "c" for layer in shape for x in (layer[i] for i in range(0, 12, 2)))
    has_vertical_split = any(layer[0:2] != layer[10:12] or layer[4:6] != layer[6:8] for layer in shape)
    has_slash_split = any(layer[0:2] != layer[2:4] or layer[6:8] != layer[8:10] for layer in shape)
    has_backslash_split = any(layer[4:6] != layer[2:4] or layer[8:10] != layer[10:12] for layer in shape)
    if (has_vertical_split + has_slash_split + has_backslash_split) >= 2:
        tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    while True:
        # Calculate what's possible with available processors
        # IMPORTANT: Always sort by complexity in bulks
        variants = [False] * Variant.end
        variants[Variant.full] = True
        if Processor.PIN_PUSHER in available:
            variants[Variant.pins] = True
            if Processor.CRYSTALLIZER in available and complexity:
                variants[Variant.full_crystal] = True
        if Processor.CRYSTALLIZER in available and Processor.CUTTER in available and complexity >= 2:
            variants[Variant.half_crystal_half_shape] = True
            if Processor.ROTATOR in available and complexity >= 4:
                _bulk_possible(
                    variants, complexity, (Variant._4_crystals_2_shape, ), (Variant._4_crystals_2_shape, 4),
                    (Variant._5_crystals_1_shape, 5), (Variant.half_crystal, 6), (Variant.half_half_crystal, 6),
                    (Variant.full_crystal, 7), (Variant._5_1_crystals, 8), (Variant._4_2_crystals, 8),
                )
                if Processor.STACKER in available and complexity >= 8:
                    _bulk_possible(
                        variants, complexity, (Variant._5_shapes_1_crystal, Variant._4_shapes_2_crystal),
                        (Variant.checkered_2_1_shape_crystal, 10), (Variant.checkered_2_1_crystal_shape, 11),
                        (Variant.checkered_atomic_crystal_shape, 17), (Variant.checkered_2x_shape_crystal, 23),
                    )
                if Processor.SWAPPER in available:  # complexity >= 4 is ensured from outer scope
                    _bulk_possible(
                        variants, complexity, (Variant._5_shapes_1_crystal, Variant._4_shapes_2_crystal),
                        (Variant.checkered_2_1_crystal_shape, 7), (Variant.checkered_2_1_shape_crystal, 7),
                        (Variant.checkered_atomic_crystal_shape, 9), (Variant.cut_out_5_crystal, 9),
                        (Variant.cut_out_4_crystal, 11), (Variant.checkered_2x_shape_crystal, 12),
                        (Variant.cornered_crystal, 12), (Variant.checkered_2_1_crystal, 13),
                        (Variant.cornered_2_crystal, 14), (Variant.checkered_2x_crystal_shape, 14),
                        (Variant.cornered_asymmetrical_crystal, 14), (Variant._3_doubles_crystal, 15),
                        (Variant.checkered_crystal, 20), (Variant.checkered_atomic_crystal, 20),
                        (Variant.cornered_atomic_crystal, 26),
                    )
        if Processor.CUTTER in available and complexity:
            variants[Variant.half] = True
            if Processor.ROTATOR in available and complexity >= 3:
                _bulk_possible(variants, complexity, (Variant.double, ), (Variant.single, 4))
                if Processor.STACKER in available and complexity >= 5:
                    _bulk_possible(
                        variants, complexity, (Variant.cut_out_4, ), (Variant.half_half, 6), (Variant.cut_out_5, 6),
                        (Variant._2_doubles, 8), (Variant.cornered_2, 9), (Variant._2_singles, 9),
                        (Variant.cornered, 10), (Variant._5_1, 12), (Variant._4_2, 13), (Variant._3_doubles, 14),
                        (Variant.cornered_atomic, 16), (Variant.checkered_asymmetrical, 20),
                        (Variant.checkered_2_1, 21), (Variant.cornered_asymmetrical, 21), (Variant.cornered_1_1, 21),
                        (Variant._5_singles, 26), (Variant.checkered, 32), (Variant.checkered_atomic, 32),
                        (Variant._6_singles, 32),
                    )
        if Processor.SWAPPER in available and complexity:
            variants[Variant.half_half] = True
            if Processor.ROTATOR in available and complexity >= 3:
                _bulk_possible(
                    variants, complexity, (Variant._5_1, ), (Variant._4_2, 4), (Variant.checkered_2_1, 4),
                    (Variant._3_doubles, 5), (Variant.checkered_asymmetrical, 5), (Variant.checkered_atomic, 7),
                    (Variant.checkered, 9), (Variant._6_singles, 9),
                )
                if Processor.CUTTER in available:  # and complexity >= 3
                    _bulk_possible(
                        variants, complexity, (Variant.cut_out_4, ), (Variant.cut_out_5, 4), (Variant.cornered, 6),
                        (Variant.cornered_2, 6), (Variant._2_singles, 6), (Variant._2_doubles, 6),
                        (Variant.cornered_atomic, 8), (Variant.cornered_asymmetrical, 9), (Variant._5_singles, 9),
                        (Variant.cornered_1_1, 10),
                    )

        def _bulk_remove(*v: int):
            for vv in v:
                variants[vv] = False

        # Remove everything that doesn't have the important buildings
        if important:
            if any(tasked):
                if tasked[Processor.CUTTER]:
                    _bulk_remove(Variant.full, Variant.pins)
                    if Processor.SWAPPER in available:
                        _bulk_remove(
                            Variant.half_half, Variant._5_1, Variant._4_2, Variant.checkered, Variant.checkered_2_1,
                            Variant.checkered_atomic, Variant.checkered_asymmetrical, Variant._3_doubles,
                            Variant._6_singles,
                        )
                    if Processor.PIN_PUSHER in available:
                        variants[Variant.full_crystal] = False
                if tasked[Processor.ROTATOR]:
                    _bulk_remove(Variant.pins, Variant.full)
                    if Processor.PIN_PUSHER in available:
                        variants[Variant.full_crystal] = False
                    if not (has_vertical_split or has_slash_split or has_backslash_split):
                        variants[Variant.half] = False
                        if Processor.SWAPPER in available:
                            variants[Variant.half_half] = False
                if tasked[Processor.STACKER]:
                    # Should only happen in single layers
                    if sum(tasked) == 1:
                        variants[Variant.full] = True
                    _bulk_remove(Variant.half, Variant.single, Variant.double, Variant.pins)
                    if Processor.SWAPPER in available:
                        for x in range(Variant.begin_crystals + 1, Variant.end_crystals):
                            if x not in (
                                Variant._5_shapes_1_crystal, Variant._4_shapes_2_crystal,
                                Variant.checkered_2x_shape_crystal, Variant.checkered_2_1_crystal_shape,
                                Variant.checkered_2_1_shape_crystal, Variant.checkered_atomic_crystal_shape,
                            ):
                                variants[x] = False
                if tasked[Processor.PAINTER]:
                    # Painters don't have anything to do with crystallizers,
                    # so make sure you can paint something if needed
                    _bulk_remove(
                        Variant.pins, Variant.full_crystal, Variant.half_crystal, Variant.half_half_crystal,
                        Variant._5_1_crystals, Variant._4_2_crystals, Variant.cut_out_5_crystal,
                        Variant.cut_out_4_crystal, Variant.cornered_crystal, Variant.cornered_2_crystal,
                        Variant.cornered_atomic_crystal, Variant.cornered_asymmetrical_crystal,
                        Variant.checkered_crystal, Variant.checkered_2_1_crystal, Variant.checkered_atomic_crystal,
                        Variant._3_doubles_crystal,
                    )
                if tasked[Processor.PIN_PUSHER]:
                    for x in range(0, Variant.end):
                        if x not in (Variant.pins, Variant.full_crystal):
                            variants[x] = False
                if tasked[Processor.CRYSTALLIZER]:
                    for x in range(0, Variant.begin_crystals):
                        variants[x] = False
                    for x in range(Variant.end_crystals + 1, Variant.end):
                        variants[x] = False
                if tasked[Processor.SWAPPER]:
                    _bulk_remove(
                        Variant.full, Variant.half, Variant.single, Variant.double, Variant.pins, Variant.full_crystal,
                        Variant.half_crystal, Variant.half_half_crystal, Variant._5_1_crystals, Variant._4_2_crystals,
                        Variant._4_crystals_2_shape, Variant._5_crystals_1_shape, Variant.half_crystal_half_shape,
                    )
                    if Processor.STACKER in available:
                        if Processor.CUTTER in available:
                            _bulk_remove(
                                Variant._5_1, Variant._4_2, Variant.checkered, Variant._6_singles, Variant._3_doubles,
                                Variant.checkered_atomic, Variant.checkered_asymmetrical, Variant.checkered_2_1,
                            )
                            if Processor.ROTATOR in available:
                                _bulk_remove(Variant.half_half)
                        _bulk_remove(
                            Variant.cut_out_5, Variant.cut_out_4, Variant.cornered, Variant.cornered_asymmetrical,
                            Variant.cornered_1_1, Variant.cornered_atomic, Variant.checkered_2_1_crystal_shape,
                            Variant._2_singles, Variant._2_doubles, Variant._5_singles, Variant._5_shapes_1_crystal,
                            Variant._4_shapes_2_crystal, Variant.checkered_2x_shape_crystal, Variant.cornered_2,
                            Variant.checkered_2_1_shape_crystal, Variant.checkered_atomic_crystal_shape,
                        )

        # Remove some things that are impossible due to shape context
        if already_has_crystals:
            # Putting new layers with crystal on top of or under other crystals is tricky, especially since
            # the swapper can destroy other layers
            if Processor.PIN_PUSHER not in available:
                variants[Variant.full_crystal] = False
            _bulk_remove(
                Variant.half_crystal, Variant.half_half_crystal, Variant._5_1_crystals, Variant._4_2_crystals,
                Variant.cut_out_5_crystal, Variant.cut_out_4_crystal, Variant.cornered_crystal,
                Variant.cornered_2_crystal, Variant._3_doubles_crystal, Variant.checkered_atomic_crystal,
                Variant.cornered_atomic_crystal, Variant.cornered_asymmetrical_crystal, Variant.checkered_crystal,
                Variant.checkered_2x_crystal_shape, Variant.checkered_2_1_crystal,

            )
        if not len(shape):
            variants[Variant.pins] = False

        # Remove some low complexity variants if high complexity given
        if not important and complexity >= 20:
            _bulk_remove(
                Variant.double, Variant.cut_out_4, Variant.cut_out_5, Variant.checkered_2_1_crystal,
                Variant.cornered_2, Variant.cornered, Variant._4_shapes_2_crystal, Variant.cornered_crystal,
                Variant._5_1, Variant._4_2, Variant._4_crystals_2_shape, Variant._5_shapes_1_crystal,
                Variant._5_crystals_1_shape, Variant.cut_out_5_crystal, Variant.cut_out_4_crystal,
            )
            if Processor.CUTTER in available and Processor.ROTATOR in available:
                _bulk_remove(Variant.half)
                if Processor.STACKER in available or Processor.SWAPPER in available:
                    _bulk_remove(Variant.single)
                if Processor.CRYSTALLIZER in available:
                    _bulk_remove(Variant.half_crystal_half_shape)
            if sum(variants) > 1:
                variants[Variant.full] = False

        # If none available anymore, try to save it in some way
        if not any(variants):
            if complexity <= sum(tasked) + 1:  # Maybe complexity was too restrictive
                complexity += 3
            elif not any(tasked):  # If nothing tasked, then a full layer doesn't do anything
                variants[Variant.full] = True
            else:  # Last resort, maybe a very bad combination?
                tasked[world.random.choice([x for x in range(8) if tasked[x]])] = False
            continue
        break

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _tasked_sw_st(swc: int, stc: int, need_cu: bool):
        nonlocal complexity
        if Processor.SWAPPER in available:
            complexity -= swc
            if Processor.STACKER not in available or (Processor.CUTTER not in available and not need_cu):
                tasked[Processor.SWAPPER] = False
        else:
            complexity -= stc
            tasked[Processor.STACKER] = False
            tasked[Processor.CUTTER] = False if not need_cu else tasked[Processor.CUTTER]
        tasked[Processor.CUTTER] = False if need_cu else tasked[Processor.CUTTER]
        tasked[Processor.ROTATOR] = False

    def _bulk_tasked(comp: int, *t: Processor):
        nonlocal complexity
        complexity -= comp
        for tt in t:
            tasked[tt] = False

    def _3_parts(c1: bool, c2: bool, c3: bool | None, no_same: bool) -> tuple[str, str, str]:
        nonlocal complexity
        complexity_1 = world.random.triangular(0, complexity).__int__()
        complexity_2 = 0 if c3 is None else world.random.triangular(0, complexity - complexity_1).__int__()
        complexity -= complexity_1 + complexity_2
        p1 = generate_shape(world) + generate_color(
            world, complexity_1, shape, False, available, tasked, important
        ) if not c1 else "c" + generate_color(world, complexity_1, shape, True, available, tasked, important)
        p2 = generate_shape(world) + generate_color(
            world, complexity, shape, False, available, tasked, important
        ) if not c2 else "c" + generate_color(world, complexity, shape, True, available, tasked, important)
        p3 = "--" if c3 is None else (
            generate_shape(world) + generate_color(
                world, complexity_2, shape, False, available, tasked, important
            ) if not c3 else "c" + generate_color(world, complexity_2, shape, True, available, tasked, important)
        )
        if no_same:
            if p1 == p2:
                p2 = generate_shape(world, p2[0]) + p2[1] if not c2 else "c" + generate_color(
                    world, complexity, shape, True, available, tasked, important, p2[1]
                )
            while p3 in (p1, p2):
                p3 = generate_shape(world, p3[0]) + p3[1] if not c3 else "c" + generate_color(
                    world, complexity, shape, True, available, tasked, important, p3[1]
                )
        return p1, p2, p3

    variant_pool = [x for x in variants if variants[x]]
    match world.random.choice(variant_pool):
        case Variant.full:
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            stack(world, shape, part * 6, tasked, True, 0, already_has_crystals)
        case Variant.half:
            _bulk_tasked(1, Processor.CUTTER)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            subvariants = [
                "------" + part * 3, part + "------" + part * 2, "----" + part * 3 + "--",
                "--" + part * 3 + "----", part * 2 + "------" + part, part * 3 + "------"
            ]
            possible = [True, False, False, False, False, False]
            if complexity:
                possible[1:3] = [True, True]
                if complexity >= 2:
                    possible[3:5] = [True, True]
                    if complexity >= 3:
                        possible[5] = True
            if tasked[Processor.ROTATOR]:
                # This only happens when there's only one or no split
                if has_vertical_split:
                    possible[0:3] = [False, True, True]
                    possible[5] = False
                elif has_slash_split:
                    possible[1:4] = [False, possible[2], False]
                elif has_backslash_split:
                    possible[2:5] = [False, possible[3], False]
            stack(world, shape, world.random.choices(subvariants, possible)[0], tasked, True, 0, already_has_crystals)
        case Variant.half_half:
            if Processor.SWAPPER in available:
                complexity -= 1
                if (
                    Processor.CUTTER not in available or
                    Processor.ROTATOR not in available or
                    Processor.STACKER not in available
                ):
                    tasked[Processor.SWAPPER] = False
            else:
                _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.STACKER)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            subvariants = [part_1 * 3 + part_2 * 3, part_1 + part_2 * 3 + part_1 * 2, part_1 * 2 + part_2 * 3 + part_1]
            if not complexity:
                possible = [True, False, False]
            else:
                possible = [True, True, True]
            if tasked[Processor.ROTATOR]:
                # This only happens when there's only one or no split
                if has_vertical_split:
                    possible = [False, True, True]
                elif has_slash_split:
                    possible[1] = False
                elif has_backslash_split:
                    possible[2] = False
            stack(world, shape, world.random.choices(subvariants, possible)[0], tasked, True, 0, already_has_crystals)
        case Variant.cut_out_5:
            _tasked_sw_st(4, 6, True)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            ordered_parts = [part, part, part, part, part, "--"]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 0, already_has_crystals)
        case Variant.cut_out_4:
            _tasked_sw_st(3, 5, True)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            possible = [
                "----" + part * 4, part + "----" + part * 3, part * 2 + "----" + part * 2,
                part * 3 + "----" + part, part * 4 + "----", "--" + part * 4 + "--"
            ]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant._5_1:
            _tasked_sw_st(3, 12, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            ordered_parts = [part_1, part_1, part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 0, already_has_crystals)
        case Variant._4_2:
            _tasked_sw_st(4, 13, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            possible = [
                part_2 * 2 + part_1 * 4, part_1 + part_2 * 2 + part_1 * 3, part_1 * 2 + part_2 * 2 + part_1 * 2,
                part_1 * 3 + part_2 * 2 + part_1, part_1 * 4 + part_2 * 2, part_2 + part_1 * 4 + part_2
            ]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.cornered:
            _tasked_sw_st(6, 10, True)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            possible = [
                part + "----" + part + "----", "--" + part + "----" + part + "--", "----" + part + "----" + part
            ]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.cornered_2:
            _tasked_sw_st(6, 9, True)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            possible = [
                part * 2 + "--" + part * 2 + "--", "--" + part * 2 + "--" + part * 2,
                part + "--" + part * 2 + "--" + part
            ]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.cornered_1_1:
            _tasked_sw_st(10, 21, True)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            possible = [(part_1 + part_2 + "--") * 2, (part_1 + "--" + part_2) * 2, ("--" + part_1 + part_2) * 2]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.cornered_atomic:
            _tasked_sw_st(8, 16, True)
            part = generate_shape(world) + generate_color(
                world, complexity, shape, False, available, tasked, important
            )
            possible = [(part + "--") * 3, ("--" + part) * 3]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.cornered_asymmetrical:
            _tasked_sw_st(9, 21, True)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            possible = [
                part_1 + "--" + part_1 + part_2 + "--" + part_2, part_1 + part_2 + "--" + part_2 + part_1 + "--",
                "--" + part_1 + part_2 + "--" + part_2 + part_1
            ]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.checkered:
            _tasked_sw_st(9, 32, False)
            part_1, part_2, part_3 = _3_parts(False, False, False, True)
            stack(world, shape, (part_1 + part_2 + part_3) * 2, tasked, True, 0, already_has_crystals)
        case Variant.checkered_2_1:
            _tasked_sw_st(4, 21, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            possible = [(part_1 + part_1 + part_2) * 2, (part_1 + part_2 + part_2) * 2, (part_1 + part_2 + part_1) * 3]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.checkered_atomic:
            _tasked_sw_st(7, 32, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            stack(world, shape, (part_1 + part_2) * 3, tasked, True, 0, already_has_crystals)
        case Variant.checkered_asymmetrical:
            _tasked_sw_st(5, 20, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            possible = [
                part_1 + part_2 * 2 + part_1 * 2 + part_2, part_1 + part_2 + part_1 * 2 + part_2 * 2,
                part_1 * 2 + part_2 * 2 + part_1 + part_2, part_1 * 2 + part_2 + part_1 + part_2 * 2,
                part_1 + part_2 + part_1 + part_2 * 2 + part_1, part_1 + part_2 * 2 + part_1 + part_2 + part_1
            ]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant._3_doubles:
            _tasked_sw_st(5, 14, False)
            part_1, part_2, part_3 = _3_parts(False, False, False, True)
            possible = [part_1 * 2 + part_2 * 2 + part_3 * 2, part_1 + part_2 * 2 + part_3 * 2 + part_1]
            stack(world, shape, world.random.choice(possible), tasked, True, 0, already_has_crystals)
        case Variant.pins:
            tasked[Processor.PIN_PUSHER] = False
            part = ""
            for i in range(0, 12, 2):
                part += "P-" if shape[0][i] != "-" else "--"
            shape.insert(0, part)
        case Variant.full_crystal:
            # Assumes either has pin pusher or not already_has_crystals
            # Needs extra handling because of that
            if Processor.PIN_PUSHER in available:
                complexity -= 1
                if Processor.ROTATOR not in available or Processor.CUTTER not in available:
                    tasked[Processor.PIN_PUSHER] = False
            else:
                _bulk_tasked(7, Processor.CUTTER, Processor.ROTATOR)
            tasked[Processor.CRYSTALLIZER] = False
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            if already_has_crystals:
                fill_crystal(shape, part[1])
            shape.insert(0, part * 6)
        case Variant.half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            subvariants = [
                "------" + part * 3, part + "------" + part * 2, "----" + part * 3 + "--",
                "--" + part * 3 + "----", part * 2 + "------" + part, part * 3 + "------"
            ]
            possible = [True, False, False, False, False, False]
            if complexity:
                possible[1:3] = [True, True]
                if complexity >= 2:
                    possible[3:5] = [True, True]
                    if complexity >= 3:
                        possible[5] = True
            stack(world, shape, world.random.choices(subvariants, possible)[0], tasked, False, 1, already_has_crystals)
        case Variant.half_half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            subvariants = [part_1 * 3 + part_2 * 3, part_1 + part_2 * 3 + part_1 * 2, part_1 * 2 + part_2 * 3 + part_1]
            if complexity:
                possible = [True, True, True]
            else:
                possible = [True, False, False]
            stack(world, shape, world.random.choices(subvariants, possible)[0], tasked, False, 2, already_has_crystals)
        case Variant.half_crystal_half_shape:
            _bulk_tasked(2, Processor.CUTTER, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(False, True, None, False)
            subvariants = [
                part_2 * 3 + part_1 * 3, part_1 + part_2 * 3 + part_1 * 2, part_2 * 2 + part_1 * 3 + part_2,
                part_2 + part_1 * 3 + part_2 * 2, part_1 * 2 + part_2 * 3 + part_1, part_1 * 3 + part_2 * 3
                ]
            possible = [True, False, False, False, False, False]
            if complexity:
                possible[1:3] = [True, True]
                if complexity >= 2:
                    possible[3:5] = [True, True]
                    if complexity >= 3:
                        possible[5] = True
            if tasked[Processor.ROTATOR]:
                # This only happens when there's only one or no split
                if has_vertical_split:
                    possible[0:3] = [False, True, True]
                    possible[5] = False
                elif has_slash_split:
                    possible[1:4] = [False, possible[2], False]
                elif has_backslash_split:
                    possible[2:5] = [False, possible[3], False]
            stack(world, shape, world.random.choices(subvariants, possible)[0], tasked, True, 1, already_has_crystals)
        case Variant.cut_out_5_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(9, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            ordered_parts = [part, part, part, part, part, "--"]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, False, 1, already_has_crystals)
        case Variant.cut_out_4_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(11, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            position = world.random.randint(0, 5)
            ordered = [part] * 6
            ordered[position], ordered[(position + 1) % 6] = "--", "--"
            stack(world, shape, "".join(ordered), tasked, False, 1, already_has_crystals)
        case Variant._5_1_crystals:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            ordered_parts = [part_1, part_1, part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, False, 2, already_has_crystals)
        case Variant._4_2_crystals:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            position = world.random.randint(0, 5)
            ordered = [part_1] * 6
            ordered[position], ordered[(position + 1) % 6] = part_2, part_2
            stack(world, shape, "".join(ordered), tasked, False, 2, already_has_crystals)
        case Variant._5_crystals_1_shape:
            _bulk_tasked(5, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(False, True, None, False)
            ordered_parts = [part_1, part_2, part_2, part_2, part_2, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 1, already_has_crystals)
        case Variant._5_shapes_1_crystal:
            _tasked_sw_st(4, 8, True)
            tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(False, True, None, False)
            ordered_parts = [part_1, part_1, part_1, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, True, 1, already_has_crystals)
        case Variant._4_crystals_2_shape:
            _bulk_tasked(4, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, False, None, False)
            position = world.random.randint(0, 5)
            ordered = [part_1] * 6
            ordered[position], ordered[(position + 1) % 6] = part_2, part_2
            stack(world, shape, "".join(ordered), tasked, True, 1, already_has_crystals)
        case Variant._4_shapes_2_crystal:
            _tasked_sw_st(4, 8, True)
            tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(False, True, None, False)
            position = world.random.randint(0, 5)
            ordered = [part_1] * 6
            ordered[position], ordered[(position + 1) % 6] = part_2, part_2
            stack(world, shape, "".join(ordered), tasked, True, 1, already_has_crystals)
        case Variant.cornered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(12, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            possible = [part + "----", "--" + part + "--", "----" + part]
            stack(world, shape, world.random.choice(possible) * 2, tasked, False, 1, already_has_crystals)
        case Variant.cornered_2_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(14, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            possible = [part + "--" + part, "--" + part * 2, part * 2 + "--"]
            stack(world, shape, world.random.choice(possible) * 2, tasked, False, 1, already_has_crystals)
        case Variant.cornered_atomic_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(26, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
            possible = [part + "--", "--" + part]
            stack(world, shape, world.random.choice(possible) * 3, tasked, False, 1, already_has_crystals)
        case Variant.cornered_asymmetrical_crystal:
            _bulk_tasked(14, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            position = world.random.randint(0, 2)
            ordered = ["--"] * 6
            ordered[position], ordered[position+1], ordered[position+3], ordered[(position+4)%6] \
                = part_1, part_2, part_2, part_1
            stack(world, shape, "".join(ordered), tasked, False, 2, already_has_crystals)
        case Variant.checkered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(20, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, part_3 = _3_parts(True, True, True, True)
            stack(world, shape, (part_1 + part_2 + part_3) * 2, tasked, False, 3, already_has_crystals)
        case Variant.checkered_2x_crystal_shape:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(14, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, part_3 = _3_parts(True, True, False, True)
            ordered_parts = [part_1, part_2, part_3]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts) * 2, tasked, True, 2, already_has_crystals)
        case Variant.checkered_2x_shape_crystal:
            _tasked_sw_st(12, 23, True)
            tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, part_3 = _3_parts(True, False, False, True)
            ordered_parts = [part_1, part_2, part_3]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts) * 2, tasked, True, 1, already_has_crystals)
        case Variant.checkered_2_1_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(13, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            ordered_parts = [part_1, part_2, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts) * 2, tasked, False, 2, already_has_crystals)
        case Variant.checkered_2_1_crystal_shape:
            # Assumes this doesn't happen when already_has_crystals
            _tasked_sw_st(7, 11, True)
            tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(True, False, None, False)
            ordered_parts = [part_1, part_2, part_1]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts) * 2, tasked, True, 1, already_has_crystals)
        case Variant.checkered_2_1_shape_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _tasked_sw_st(7, 10, True)
            tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(True, False, None, False)
            ordered_parts = [part_1, part_2, part_2]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts) * 2, tasked, True, 1, already_has_crystals)
        case Variant.checkered_atomic_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(20, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            possible = [part_1 + part_2, part_2 + part_1]
            stack(world, shape, world.random.choice(possible) * 3, tasked, False, 2, already_has_crystals)
        case Variant.checkered_atomic_crystal_shape:
            # Assumes this doesn't happen when already_has_crystals
            _tasked_sw_st(9, 17, True)
            tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(True, False, None, False)
            possible = [part_1 + part_2, part_2 + part_1]
            stack(world, shape, world.random.choice(possible) * 3, tasked, True, 1, already_has_crystals)
        case Variant._3_doubles_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(15, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, part_3 = _3_parts(True, True, True, True)
            possible = [part_1 * 2 + part_2 * 2 + part_3 * 2, part_1 + part_2 * 2 + part_3 * 2 + part_1]
            stack(world, shape, world.random.choice(possible), tasked, False, 3, already_has_crystals)
        case Variant.single:
            _bulk_tasked(0, Processor.CUTTER, Processor.ROTATOR)
            if Processor.CRYSTALLIZER in available and complexity >= 7 and not already_has_crystals:
                _bulk_tasked(7, Processor.CRYSTALLIZER)
                part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
                a = (False, 1)
            else:
                complexity -= 4
                part = generate_shape(world) + generate_color(
                    world, complexity, shape, False, available, tasked, important
                )
                a = (True, 0)
            ordered_parts = [part, "--", "--", "--", "--", "--"]
            world.random.shuffle(ordered_parts)
            stack(world, shape, "".join(ordered_parts), tasked, *a, already_has_crystals)
        case Variant.double:
            _bulk_tasked(0, Processor.CUTTER, Processor.ROTATOR)
            if Processor.CRYSTALLIZER in available and complexity >= 7 and not already_has_crystals:
                _bulk_tasked(7, Processor.CRYSTALLIZER)
                part = "c" + generate_color(world, complexity, shape, True, available, tasked, important)
                a = (False, 1)
            else:
                complexity -= 3
                part = generate_shape(world) + generate_color(
                    world, complexity, shape, False, available, tasked, important
                )
                a = (True, 0)
            position = world.random.randint(0, 5)
            ordered = ["--"] * 6
            ordered[position], ordered[(position + 1) % 6] = part, part
            stack(world, shape, "".join(ordered), tasked, *a, already_has_crystals)
        case Variant._2_singles:
            generate_2_shapes(world, complexity, shape, available, tasked, important, already_has_crystals)
        case Variant._2_doubles:
            generate_2_doubles(world, complexity, shape, available, tasked, important, already_has_crystals)
        case Variant._5_singles:
            generate_5_shapes(world, complexity, shape, available, tasked, important, already_has_crystals)
        case Variant._6_singles:
            generate_6_shapes(world, complexity, shape, available, tasked, important, already_has_crystals)
        case e:
            raise Exception(f"Unknown layer variant {e}:\n"
                            f"complexity = {complexity}, shape = {shape}, important = {important}\n"
                            f"available = {available}, tasked = {tasked},\n"
                            f"already has crystals = {already_has_crystals}, has vertical split = {has_vertical_split},"
                            f"has slash split = {has_slash_split}, has backslash split = {has_backslash_split}\n"
                            f"variant pool = {variant_pool}")


def generate_2_shapes(world: "Shapez2World", complexity: int, shape: list[str],
                      available: list[Processor], tasked: list[bool], important: bool,
                      already_has_crystals: bool) -> None:
    tasked[Processor.CUTTER] = False
    tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 9
    if Processor.CRYSTALLIZER in available and complexity >= 6 and not already_has_crystals:
        _bulk_possible(subvariants, complexity, (3, ), (6, 9))
        if Processor.SWAPPER in available and complexity >= 9:
            _bulk_possible(subvariants, complexity, (5, ), (4, 10), (8, 12), (7, 14))
        if Processor.STACKER in available and complexity >= 12:
            _bulk_possible(subvariants, complexity, (4, ), (5, 13))
    if Processor.SWAPPER in available and complexity >= 6:
        _bulk_possible(subvariants, complexity, (0, 2), (1, 7))
    if Processor.STACKER in available and complexity >= 9:
        _bulk_possible(subvariants, complexity, (1, ), (0, 10), (2, 10))
    if important and tasked[Processor.PAINTER]:
        subvariants[6:] = [False] * 3

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _make(shift: int, has_non_crys: bool, crys_col: int, p: list[str]):
        position = world.random.randint(0, 5)
        ordered = ["--"] * 6
        ordered[position], ordered[(position + shift) % 6] = p[:2]
        stack(world, shape, "".join(ordered), tasked, has_non_crys, crys_col, already_has_crystals)

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:  # adjacent shapes, swapper 6 stacker 10
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 6, 10, (False, False, None, None, None, None))
            _make(1, True, 0, parts)
        case 1:  # close shapes, swapper 7 stacker 9
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 7, 9, (False, False, None, None, None, None))
            _make(2, True, 0, parts)
        case 2:  # cornered shapes, swapper 6 stacker 10
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 6, 10, (False, False, None, None, None, None))
            _make(3, True, 0, parts)
        case 3:  # adjacent shape crystal, 6
            complexity -= 9
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (False, True, None, None, None, None))
            _make(world.random.choice((1, -1)), True, 1, parts)
        case 4:  # close shapes crystal, swapper 10 stacker 12
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 10, 12, (False, True, None, None, None, None))
            _make(world.random.choice((2, -2)), True, 1, parts)
        case 5:  # cornered shapes crystal, swapper 9 stacker 13
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 9, 13, (False, True, None, None, None, None))
            _make(world.random.choice((3, -3)), True, 1, parts)
        case 6:  # adjacent crystals, 9
            complexity -= 9
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, None, None, None, None))
            _make(1, False, 2, parts)
        case 7:  # close crystals, swapper 14
            complexity -= 14
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, None, None, None, None))
            _make(2, False, 2, parts)
        case 8:  # cornered crystals, swapper 12
            complexity -= 12
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, None, None, None, None))
            _make(3, False, 2, parts)


def generate_2_doubles(world: "Shapez2World", complexity: int, shape: list[str],
                       available: list[Processor], tasked: list[bool], important: bool,
                       already_has_crystals: bool) -> None:
    tasked[Processor.CUTTER] = False
    tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if Processor.CRYSTALLIZER in available and complexity >= 10 and not already_has_crystals:
        if Processor.SWAPPER in available:
            _bulk_possible(subvariants, complexity, (2, 3, ), (4, 14), (5, 14))
        if Processor.STACKER in available and complexity >= 12:
            _bulk_possible(subvariants, complexity, (2, ), (3, 13))
    if Processor.SWAPPER in available and complexity >= 6:
        _bulk_possible(subvariants, complexity, (0, 1, ))
    if Processor.STACKER in available and complexity >= 8:
        _bulk_possible(subvariants, complexity, (0, ), (1, 9))
    if important and tasked[Processor.PAINTER]:
        subvariants[4:] = [False] * 2

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _make(shift: int, has_non_crys: bool, crys_col: int, p: list[str]):
        position = world.random.randint(0, 5)
        ordered = ["--"] * 6
        ordered[position], ordered[(position + 1) % 6] = p[:1] * 2
        ordered[position + shift], ordered[(position + shift + 1) % 6] = p[:1] * 2
        stack(world, shape, "".join(ordered), tasked, has_non_crys, crys_col, already_has_crystals)

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:  # adjacent shapes, swapper 6 stacker 8
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 6, 8, (False, False, None, None, None, None))
            _make(2, True, 0, parts)
        case 1:  # cornered shapes, swapper 6 stacker 9
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 6, 9, (False, False, None, None, None, None))
            _make(3, True, 0, parts)
        case 2:  # adjacent shape crystal, swapper 10 stacker 12
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 10, 12, (False, True, None, None, None, None))
            _make(world.random.choice((2, -2)), True, 1, parts)
        case 3:  # cornered shapes crystal, swapper 10 stacker 13
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 10, 13, (False, True, None, None, None, None))
            _make(world.random.choice((3, -3)), True, 1, parts)
        case 4:  # adjacent crystals, swapper 14
            complexity -= 14
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, None, None, None, None))
            _make(2, False, 2, parts)
        case 5:  # cornered crystals, swapper 14
            complexity -= 14
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, None, None, None, None))
            _make(3, False, 2, parts)


def generate_5_shapes(world: "Shapez2World", complexity: int, shape: list[str],
                      available: list[Processor], tasked: list[bool], important: bool,
                      already_has_crystals: bool) -> None:
    tasked[Processor.CUTTER] = False
    tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 11
    if Processor.CRYSTALLIZER in available and complexity >= 13 and not already_has_crystals:
        if Processor.SWAPPER in available:
            _bulk_possible(
                subvariants, complexity, (2, 6, 8, ),
                (5, 14), (7, 14), (9, 14), (3, 15), (4, 15), (1, 17), (10, 19), (0, 20)
            )
        if Processor.STACKER in available and complexity >= 22:
            _bulk_possible(subvariants, complexity, (4, 5, ), (2, 23), (3, 23), (1, 24), (0, 26))
    if Processor.SWAPPER in available and complexity >= 20:
        subvariants[0] = True
    if Processor.STACKER in available and complexity >= 26:
        subvariants[0] = True
    if important:
        if tasked[Processor.PAINTER]:
            subvariants[10] = False
        if tasked[Processor.STACKER]:
            subvariants[6:] = [False] * 5

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _make(has_non_crys: bool, crys_col: int, fill: list[str], *shifts: tuple[str, int]):
        position = world.random.randint(0, 5)
        ordered: list[str | None] = [None] * 6
        ordered[position] = "--"
        for part, shift in shifts:
            ordered[(position + shift) % 6] = part
        for i in range(6):
            if ordered[i] is None:
                ordered[i] = fill.pop()
        stack(world, shape, "".join(ordered), tasked, has_non_crys, crys_col, already_has_crystals)

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:  # no crystal, swapper 20 stacker 26
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 20, 26, (False, False, False, False, False, None))
            world.random.shuffle(parts)
            stack(world, shape, "".join(parts), tasked, True, 0, already_has_crystals)
        case 1:  # 1 crystal edge, swapper 17 stacker 24
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 17, 24, (True, False, False, False, False, None))
            _make(True, 1, parts[1:5], (parts[0], world.random.choice((1, -1))))
        case 2:  # 1 crystal other, swapper 13 stacker 23
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 13, 23, (True, False, False, False, False, None))
            _make(True, 1, parts[1:5], (parts[0], world.random.choice((2, -2))))
        case 3:  # 1 crystal center, swapper 15 stacker 23
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 15, 23, (True, False, False, False, False, None))
            _make(True, 1, parts[1:5], (parts[0], 3))
        case 4:  # 3 crystals adjacent edge, swapper 15 stacker 22
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 15, 22, (True, True, True, False, False, None))
            sign = world.random.choice((1, -1))
            _make(True, 3, parts[3:5], (parts[0], 3), (parts[1], sign * 2), (parts[2], sign))
        case 5:  # 3 crystals adjacent center, swapper 14 stacker 22
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 14, 22, (True, True, True, False, False, None))
            _make(True, 3, parts[3:5], (parts[0], 3), (parts[1], 2), (parts[2], -2))
        case 6:  # 3 crystals 2 2 1, swapper only 13
            complexity -= 13
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, False, False, None))
            _make(True, 3, parts[3:5], (parts[0], world.random.choice((2, -2))), (parts[1], 1), (parts[2], -1))
        case 7:  # 3 crystals atomic, swapper only 14
            complexity -= 14
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, False, False, None))
            _make(True, 3, parts[3:5], (parts[0], 1), (parts[1], -1), (parts[2], 3))
        case 8:  # 3 crystals 1 1 2 1, swapper only 13
            complexity -= 13
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, False, False, None))
            sign = world.random.choice((1, -1))
            _make(True, 3, parts[3:5], (parts[0], 3), (parts[1], sign * 2), (parts[2], -sign))
        case 9:  # 3 crystals 1 1 1 2, swapper only 14
            complexity -= 14
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, False, False, None))
            _make(True, 3, parts[3:5], (parts[0], world.random.choice((1, -1))), (parts[1], 2), (parts[2], -2))
        case 10:  # 5 crystals, swapper only 19
            complexity -= 19
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, True, True, None))
            world.random.shuffle(parts)
            stack(world, shape, "".join(parts), tasked, False, 5, already_has_crystals)


def generate_6_shapes(world: "Shapez2World", complexity: int, shape: list[str],
                      available: list[Processor], tasked: list[bool], important: bool,
                      already_has_crystals: bool) -> None:
    tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if important:
        if tasked[Processor.MIXER]:
            if Processor.CRYSTALLIZER in available:
                stored_complexity = 1
            else:
                stored_complexity = 2
        elif tasked[Processor.PAINTER]:
            stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if (
        Processor.CRYSTALLIZER in available and Processor.CUTTER in available and
        complexity >= 10 and not already_has_crystals
    ):
        if Processor.SWAPPER in available:
            _bulk_possible(subvariants, complexity, (1, ), (2, 12), (4, 12), (3, 14), (5, 17), (6, 22))
        if Processor.STACKER in available and complexity >= 28:
            _bulk_possible(subvariants, complexity, (2, ), (1, 29))
    if Processor.SWAPPER in available and complexity >= 9:
        subvariants[0] = True
    if Processor.STACKER in available and Processor.CUTTER in available and complexity >= 32:
        subvariants[0] = True
    if important:
        if tasked[Processor.PAINTER]:
            subvariants[6] = False
        if tasked[Processor.STACKER]:
            subvariants[3:] = [False] * 4

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _make(has_non_crys: bool, crys_col: int, fill: list[str], *shifts: tuple[str, int]):
        position = world.random.randint(0, 5)
        ordered: list[str | None] = [None] * 6
        for part, shift in shifts:
            ordered[(position + shift) % 6] = part
        for i in range(6):
            if ordered[i] is None:
                ordered[i] = fill.pop()
        stack(world, shape, "".join(ordered), tasked, has_non_crys, crys_col, already_has_crystals)

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    match subvariant_pool:
        case 0:  # no crystal, swapper no cutter 9 stacker 32
            if Processor.SWAPPER in available:
                complexity -= 9
                if Processor.STACKER not in available:
                    tasked[Processor.SWAPPER] = False
            else:
                complexity -= 32
                tasked[Processor.STACKER] = False
                tasked[Processor.CUTTER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (False, False, False, False, False, False))
            stack(world, shape, "".join(parts), tasked, True, 0, already_has_crystals)
        case 1:  # 1 crystal, swapper 10 stacker 29
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 10, 29, (True, False, False, False, False, False))
            world.random.shuffle(parts)
            stack(world, shape, "".join(parts), tasked, True, 1, already_has_crystals)
        case 2:  # 3 crystal adjacent, swapper 12 stacker 28
            tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                True, 12, 28, (True, True, True, False, False, False))
            _make(True, 3, parts[4:], (parts[0], 0), (parts[1], 1), (parts[2], 2))
        case 3:  # 3 crystal atomic, swapper only 14
            complexity -= 14
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, False, False, False))
            _make(True, 3, parts[4:], (parts[0], 0), (parts[1], 2), (parts[2], 4))
        case 4:  # 3 crystals asymmetrical, swapper only 12
            complexity -= 12
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, False, False, False))
            _make(True, 3, parts[4:], (parts[0], 0), (parts[1], world.random.choice((2, -2))), (parts[2], 3))
        case 5:  # 5 crystals, swapper only 17
            complexity -= 17
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, True, True, False))
            world.random.shuffle(parts)
            stack(world, shape, "".join(parts), tasked, True, 5, already_has_crystals)
        case 6:  # 6 crystals, swapper only 22
            complexity -= 22
            tasked[Processor.CRYSTALLIZER] = False
            tasked[Processor.SWAPPER] = False
            parts = _subvariant(world, shape, available, tasked, important, complexity,
                                False, 0, 0, (True, True, True, True, True, True))
            stack(world, shape, "".join(parts), tasked, False, 6, already_has_crystals)


def generate_shape(world: "Shapez2World", exclude: str | None = None) -> str:
    shapes = ["H", "F", "G"]
    if exclude is not None:
        shapes.remove(exclude)
    return world.random.choice(shapes)


adjacent_colors = {
    "r": ("y", "m"),
    "b": ("m", "c"),
    "g": ("y", "c"),
    "y": ("r", "g"),
    "c": ("g", "b"),
    "m": ("b", "r"),
    "w": ("m", "c", "y"),
}


def generate_color(world: "Shapez2World", complexity: int, shape: list[str], is_crystal: bool,
                   available: list[Processor], tasked: list[bool], important: bool, exclude: str | None = None) -> str:

    white_comp = 2 if is_crystal else 3
    mixing_comp = 1 if is_crystal else 2
    base_comp = 0 if is_crystal else 1

    # Disable colors based on importance, availability, and complexity
    # True means must be included, False means must not be included, None means it doesn't matter
    color_types: dict[str, bool] = {c: True for c in ("u", "p", "s", "w")}
    if Processor.MIXER not in available:
        color_types["s"] = False
        color_types["w"] = False
        if Processor.PAINTER not in available and not is_crystal:
            color_types["p"] = False
    if is_crystal:
        color_types["u"] = False
    if complexity < white_comp:
        color_types["w"] = False
    if important and tasked[Processor.MIXER]:
        color_types["p"] = False
        if Processor.PAINTER in available:
            color_types["u"] = False
    elif complexity < mixing_comp:
        color_types["s"] = False
        if complexity < base_comp and not (important and tasked[Processor.PAINTER]):
            color_types["p"] = False
    if important and tasked[Processor.PAINTER]:
        color_types["u"] = False
    if Processor.PAINTER not in available and not is_crystal:
        color_types["p"] = False
        color_types["s"] = False
        color_types["w"] = False

    # Build colors list
    colors = []
    if color_types["u"]:
        colors.append("u")
    if color_types["w"]:
        colors.append("w")
    if color_types["p"]:
        colors.extend(("r", "b", "g"))
    if color_types["s"]:
        colors.extend(("y", "c", "m"))

    # Try to make color scheme a bit nicer
    if shape:
        preferred_layer = world.random.choice(shape)
        preferred: str | None = None
        for i in range(1, 12, 2):
            if preferred_layer[i] not in "u-":
                preferred = preferred_layer[i]
        if preferred is not None:
            colors.append(preferred)
        if color_types["p"] and color_types["s"]:
            colors.extend(adjacent_colors[preferred])

    # Reduce complexity waste
    if color_types["p"] and color_types["u"] and complexity >= 6:
        colors.remove("u")
    if color_types["s"] and color_types["p"] and complexity >= 8:
        colors.remove("r")
        colors.remove("b")
        colors.remove("g")

    # Remove excluded color
    # Assumes that mixed colors are present and not removed before this
    # Uncolored must not be removed because there might be no complexity left for colors
    if exclude is not None and exclude != "u":
        while exclude in colors:
            colors.remove(exclude)

    # Error handling for when there is none left for some reason:
    if not colors:
        raise Exception(f"No color left to pick:\n"
                        f"complexity = {complexity}, shape = {shape}, is crystal = {is_crystal},\n"
                        f"available = {available}, tasked = {tasked}, important = {important}")

    final = world.random.choice(colors)
    if final in "ymcw":
        tasked[Processor.MIXER] = False
    if final != "u" and not is_crystal:
        tasked[Processor.PAINTER] = False
    return final


def stack(world: "Shapez2World", shape: list[str], layer: str, tasked: list[bool],
          has_non_crystal: bool, crystal_colors: int, already_has_crystals: bool) -> None:

    tasked[Processor.STACKER] = False

    if already_has_crystals:
        # Assumes that in this case the new layer only has one crystal color (if any) and no empty part
        stack_top = True
    elif crystal_colors > 1 or not has_non_crystal or (crystal_colors and has_non_crystal and "--" in layer):
        stack_top = False
    else:
        stack_top = world.random.choice((False, True))

    if stack_top:
        if crystal_colors:
            # Make sure the non-crystal part is always placed on a non-empty corner
            # Assumes either there is the rotator at this point or the left side is not empty
            # Also assumes there is only one crystal color
            if tasked[Processor.ROTATOR]:
                layer = layer[10:12] + layer[0:10]
                tasked[Processor.ROTATOR] = False
            for i in range(0, 12, 2):
                if layer[i] not in "Pc-" and shape[-1][i] != "-":
                    break
            else:
                tasked[Processor.ROTATOR] = False
                for _ in range(5):
                    layer = layer[10:12] + layer[0:10]
                    if layer[0] not in "Pc-" and shape[-1][0] != "-":
                        break
                else:
                    raise Exception(f"new layer supposed to be placed on top, but not possible:\n"
                                    f"shape = {shape}, new layer = {layer}, "
                                    f"already has crystals = {already_has_crystals}")
            crys_col = ""
            for i in range(0, 12, 2):
                if layer[i] == "c":
                    crys_col = layer[i+1]
                    break
            fill_crystal(shape, crys_col)
            shape.append(layer)
        else:
            for j in range(0, 12, 2):
                if layer[j:j+2] != "--" and shape[-1][j:j+2] != "--":
                    shape.append(layer)
                    break
            else:
                for i in reversed(range(len(shape) - 1)):
                    for j in range(0, 12, 2):
                        if layer[j:j+2] != "--" and shape[i][j:j+2] != "--":
                            shape[i+1] = merge_layers(layer, shape[i+1])
                            break
                    else:
                        continue
                    break
                else:
                    shape[0] = merge_layers(layer, shape[0])
    else:
        for j in range(0, 12, 2):
            if layer[j:j+2] != "--" and shape[0][j:j+2] != "--":
                shape.insert(0, layer)
                for i in range(0, 12, 2):
                    if shape[0][i] == "-" and shape[1][i] == "P":
                        for k in range(2, len(shape)):
                            if shape[k][i] != "P":
                                shape[k-1] = shape[k-1][:i] + "-" + shape[k-1][i+1:]
                                shape[0] = shape[0][:i] + "P" + shape[0][i+1:]
                                break
                        else:
                            shape[-1] = shape[-1][:i] + "-" + shape[-1][i+1:]
                            shape[0] = shape[0][:i] + "P" + shape[0][i+1:]
                break
        else:
            shape[0] = merge_layers(layer, shape[0])


def merge_layers(layer_1: str, layer_2: str) -> str:
    merged = ""
    for k in range(0, 12, 2):
        if layer_1[k:k + 2] != "--":
            merged += layer_1[k:k + 2]
        else:
            merged += layer_2[k:k + 2]
    return merged


def fill_crystal(shape: list[str], color: str) -> None:
    for j in range(len(shape)):
        for i in range(1, 12, 2):
            if shape[j][i] == "-":
                shape[j] = shape[j][:i-1] + "c" + color + shape[j][i+1:]


def _bulk_possible(variants: list[bool], complexity: int, v: tuple[int, ...], *vc: tuple[int, int]):
    # IMPORTANT: Always sort by complexity in bulks
    for vv in v:
        variants[vv] = True
    for vv, cc in vc:
        if complexity >= cc:
            variants[vv] = True
        else:
            break


def _subvariant(world: "Shapez2World", shape: list[str], available: list[Processor], tasked: list[bool],
                important: bool, complexity: int, swapper_stacker: bool, a: int, b: int,
                is_crys: tuple[bool | None, ...]) -> list[str]:
    if swapper_stacker:
        if Processor.SWAPPER in available:
            complexity -= a
            if Processor.STACKER not in available:
                tasked[Processor.SWAPPER] = False
        else:
            complexity -= b
            tasked[Processor.STACKER] = False
    complexity_parts = [world.random.triangular(0, complexity).__int__()]
    for i in range(2, 6):
        complexity_parts.append(
            0 if is_crys[i] is None else world.random.triangular(0, complexity - sum(complexity_parts)).__int__()
        )
    complexity -= sum(complexity_parts)
    parts = [
        generate_shape(world) + generate_color(
            world, complexity_parts[0], shape, False, available, tasked, important
        ) if not is_crys[0] else "c" + generate_color(
            world, complexity_parts[0], shape, True, available, tasked, important
        ),
        generate_shape(world) + generate_color(
            world, complexity, shape, False, available, tasked, important
        ) if not is_crys[1] else "c" + generate_color(world, complexity, shape, True, available, tasked, important)
    ]
    for i in range(2, 6):
        parts.append(
            "--" if is_crys[i] is None else (
                generate_shape(world) + generate_color(
                    world, complexity_parts[i-1], shape, False, available, tasked, important
                ) if not is_crys[i] else "c" + generate_color(
                    world, complexity_parts[i-1], shape, True, available, tasked, important
                )
            )
        )
    return parts
