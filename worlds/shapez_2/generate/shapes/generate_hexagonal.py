from random import Random

from . import Processor, ShapeBuilder


_count = 0


def next_id(restart=False) -> int:
    global _count
    if restart:
        _count = 0
    _count += 1
    return _count - 1


class Variant:
    full = next_id(True)  # always
    half = next_id()  # cutter & 1, can use rotator +1/2/3 if any split
    half_half = next_id()  # (swapper & 1, can use rotator +1/2/3 if any split) | (cutter & rotator & stacker & 6)
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
    half_crystal_half_shape = next_id()  # crystal & cutter & 2, can use rotator +1/2/3 if any split
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
    single = next_id()  # cutter & rotator & 4 (+ crystal & 7)
    double = next_id()  # cutter & rotator & 3 (+ crystal & 7)
    _2_singles = next_id()  # (cutter & rotator & ((stacker & 9) | (swapper & 6))) |
                            # (cutter & rotator & crystal & 6 & not already has crystals)
    _2_doubles = next_id()  # (cutter & rotator & ((stacker & 8) | (swapper & 6))) |
                            # (cutter & rotator & crystal & ((stacker & 12) | (swapper & 10)) & not has crystals)
    _5_singles = next_id()  # cutter & rotator & ((stacker & 26) | (swapper & 20))
                            # (cutter & rotator & crystal & ((stacker & 22) | (swapper & 13)) & not has crystals)
    _6_singles = next_id()  # rotator & ((cutter & stacker & 32) | (swapper & 9))
                            # (cutter & rotator & crystal & ((stacker & 28) | (swapper & 10)) & not has crystals)

    end = next_id()

    _remove = next_id()  # For removing pin layers entirely


def generate_layer(rand: Random, complexity: int, builder: ShapeBuilder,
                   regen_pools: tuple[list[str], ...] | None = None, force_non_pins: bool = False) -> None:
    from .layers_hexagonal import Layers

    required_complexity = builder.calc_required_complexity()
    if complexity < required_complexity:
        raise Exception(f"Too low complexity (got {complexity}, needs {required_complexity}) "
                        f"for important processors {', '.join(str(i) for i in range(8) if builder.tasked[i])}\n"
                        f"builder = {builder.debug_string()}")

    if complexity < 0:
        raise Exception(f"Negative complexity: {complexity}\nbuilder = {builder.debug_string()}")

    if builder.splits in (3, 5, 6, 7):
        builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if builder.tasked[Processor.MIXER]:
        if Processor.CRYSTALLIZER in builder:
            stored_complexity = 1
        else:
            stored_complexity = 2
    elif builder.tasked[Processor.PAINTER]:
        stored_complexity = 1
    complexity -= stored_complexity

    while True:
        # Calculate what's possible with available processors
        # IMPORTANT: do not make anything false before this
        variants = [False] * Variant.end
        variants[Variant.full] = True
        if Processor.PIN_PUSHER in builder:
            variants[Variant.pins] = True
            if Processor.CRYSTALLIZER in builder and complexity:
                variants[Variant.full_crystal] = True
        if Processor.CRYSTALLIZER in builder and Processor.CUTTER in builder and complexity >= 2:
            variants[Variant.half_crystal_half_shape] = True
            if Processor.ROTATOR in builder and complexity >= 4:
                _bulk_possible(variants, complexity, (Variant._4_crystals_2_shape, ), (Variant._5_crystals_1_shape, 5),
                              (Variant.half_crystal, 6), (Variant.half_half_crystal, 6),
                              (Variant.full_crystal, 7), (Variant._5_1_crystals, 8), (Variant._4_2_crystals, 8))
                if not builder.has_crystals and complexity >= 6:
                    variants[Variant._2_singles] = True
                if Processor.STACKER in builder and complexity >= 8:
                    _bulk_possible(variants, complexity, (Variant._5_shapes_1_crystal, Variant._4_shapes_2_crystal),
                                   (Variant.checkered_2_1_shape_crystal, 10), (Variant.checkered_2_1_crystal_shape, 11),
                                   (Variant.checkered_atomic_crystal_shape, 17),
                                   (Variant.checkered_2x_shape_crystal, 23))
                    if not builder.has_crystals:
                        _bulk_possible(variants, complexity, (), (Variant._5_singles, 22), (Variant._6_singles, 28))
                if Processor.SWAPPER in builder:
                    _bulk_possible(variants, complexity, (Variant._5_shapes_1_crystal, Variant._4_shapes_2_crystal),
                                   (Variant.checkered_2_1_crystal_shape, 7), (Variant.checkered_2_1_shape_crystal, 7),
                                   (Variant.cut_out_5_crystal, 9), (Variant.checkered_atomic_crystal_shape, 9),
                                   (Variant.cut_out_4_crystal, 11), (Variant.checkered_2x_shape_crystal, 12),
                                   (Variant.cornered_crystal, 12), (Variant.checkered_2_1_crystal, 13),
                                   (Variant.checkered_2x_crystal_shape, 14), (Variant.cornered_2_crystal, 14),
                                   (Variant._3_doubles_crystal, 15), (Variant.cornered_asymmetrical_crystal, 18),
                                   (Variant.checkered_crystal, 20), (Variant.checkered_atomic_crystal, 20),
                                   (Variant.cornered_atomic_crystal, 26))
                    if not builder.has_crystals:
                        _bulk_possible(variants, complexity, (), (Variant._5_singles, 22), (Variant._6_singles, 28))
        if Processor.CUTTER in builder and complexity:
            variants[Variant.half] = True
            if Processor.ROTATOR in builder and complexity >= 3:
                _bulk_possible(variants, complexity, (Variant.double, ), (Variant.single, 4))
                if Processor.STACKER in builder and complexity >= 5:
                    _bulk_possible(variants, complexity, (Variant.cut_out_4, ), (Variant.cut_out_5, 6),
                                   (Variant.half_half, 6), (Variant._2_doubles, 8), (Variant.cornered_2, 9),
                                   (Variant._2_singles, 9), (Variant.cornered, 10), (Variant._5_1, 12),
                                   (Variant._4_2, 13), (Variant._3_doubles, 14), (Variant.cornered_atomic, 16),
                                   (Variant.checkered_asymmetrical, 20), (Variant.cornered_asymmetrical, 21),
                                   (Variant.cornered_1_1, 21), (Variant.checkered_2_1, 21), (Variant._5_singles, 26),
                                   (Variant.checkered_atomic, 32), (Variant.checkered, 32), (Variant._6_singles, 32))
        if Processor.SWAPPER in builder and complexity:
            variants[Variant.half_half] = True
            if Processor.ROTATOR in builder and complexity >= 3:
                _bulk_possible(variants, complexity, (Variant._5_1, ), (Variant._4_2, 4), (Variant.checkered_2_1, 4),
                               (Variant.checkered_asymmetrical, 5), (Variant._3_doubles, 5),
                               (Variant.checkered_atomic, 7), (Variant.checkered, 9), (Variant._6_singles, 9))
                if Processor.CUTTER in builder:
                    _bulk_possible(variants, complexity, (Variant.cut_out_4, ), (Variant.cut_out_5, 4),
                                   (Variant._2_singles, 6), (Variant.cornered_2, 6), (Variant._2_doubles, 6),
                                   (Variant.cornered, 6), (Variant.cornered_atomic, 8), (Variant._5_singles, 9),
                                   (Variant.cornered_asymmetrical, 9), (Variant.cornered_1_1, 10))

        def _bulk_remove(v: tuple[int, ...], *vc: tuple[int, int]):
            for vv in v:
                variants[vv] = False
            for vv, cc in vc:
                if complexity < cc:
                    variants[vv] = False
                else:
                    break

        # Remove everything that doesn't have the important buildings
        if any(builder.tasked):
            if builder.tasked[Processor.CUTTER]:
                _bulk_remove((Variant.full, Variant.pins, ))
                if Processor.SWAPPER in builder:
                    _bulk_remove((Variant.half_half, Variant._5_1, Variant._4_2, Variant.checkered, Variant._3_doubles,
                                  Variant.checkered_2_1, Variant.checkered_atomic, Variant.checkered_asymmetrical,
                                  Variant._6_singles))
                if Processor.PIN_PUSHER in builder:
                    variants[Variant.full_crystal] = False
                if builder.tasked[Processor.ROTATOR] and not builder.splits:
                    variants[Variant.half] = False
            if builder.tasked[Processor.ROTATOR]:
                _bulk_remove((Variant.full, Variant.pins), (Variant.half, 2), (Variant.half_crystal_half_shape, 3))
                if Processor.SWAPPER in builder:
                    variants[Variant.half_half] = False
                if Processor.PIN_PUSHER in builder:
                    variants[Variant.full_crystal] = False
            if builder.tasked[Processor.STACKER]:
                # Should only happen in single layers
                _bulk_remove((Variant.full, Variant.half, Variant.pins, Variant.full_crystal, Variant._4_2_crystals,
                              Variant.half_half_crystal, Variant.checkered_atomic_crystal, Variant.cut_out_5_crystal,
                              Variant.cut_out_4_crystal, Variant.cornered_atomic_crystal, Variant._5_crystals_1_shape,
                              Variant.half_crystal, Variant.checkered_2x_crystal_shape, Variant.checkered_2_1_crystal,
                              Variant._4_crystals_2_shape, Variant.cornered_2_crystal, Variant.half_crystal_half_shape,
                              Variant.cornered_asymmetrical_crystal, Variant._3_doubles_crystal, Variant._5_1_crystals,
                              Variant.double, Variant.cornered_crystal, Variant.checkered_crystal, Variant.single))
                # Do not remove things that are also able with swapper, else everything would be False
                if sum(builder.tasked) == 1:
                    variants[Variant.full] = True
            if builder.tasked[Processor.PAINTER]:
                # Painters don't have anything to do with crystallizers,
                # so make sure you can paint something if needed
                # Also this is a case where full layer is useful
                _bulk_remove((Variant.pins, Variant.full_crystal, Variant.cornered_crystal, Variant.half_half_crystal,
                              Variant.cornered_atomic_crystal, Variant.checkered_atomic_crystal, Variant._5_1_crystals,
                              Variant._4_2_crystals, Variant.cut_out_5_crystal, Variant.cornered_asymmetrical_crystal,
                              Variant.cut_out_4_crystal, Variant.cornered_2_crystal, Variant._3_doubles_crystal,
                              Variant.checkered_crystal, Variant.checkered_2_1_crystal, Variant.half_crystal))
            if builder.tasked[Processor.PIN_PUSHER]:
                temp = (variants[Variant.pins], variants[Variant.full_crystal])
                variants[:] = [False] * len(variants)
                variants[Variant.pins], variants[Variant.full_crystal] = temp
            if builder.tasked[Processor.CRYSTALLIZER]:
                variants[Variant.pins] = False
                for x in range(0, Variant.begin_crystals):
                    variants[x] = False
                if complexity < 6 or builder.has_crystals:
                    variants[Variant._2_singles] = False
                if complexity < 7 or builder.has_crystals:
                    _bulk_remove((Variant.single, Variant.double))
                if builder.has_crystals or ((Processor.SWAPPER not in builder or complexity < 10) and
                                            (Processor.STACKER not in builder or complexity < 12)):
                    variants[Variant._2_doubles] = False
                if builder.has_crystals or ((Processor.SWAPPER not in builder or complexity < 13) and
                                            (Processor.STACKER not in builder or complexity < 22)):
                    variants[Variant._5_singles] = False
                if Processor.CUTTER not in builder or ((Processor.SWAPPER not in builder or complexity < 10) and
                                                       (Processor.STACKER not in builder or complexity < 29)):
                    variants[Variant._6_singles] = False
            if builder.tasked[Processor.SWAPPER]:
                _bulk_remove((Variant.full, Variant.half, Variant.single, Variant.double, Variant._5_crystals_1_shape,
                              Variant.full_crystal, Variant.half_crystal_half_shape, Variant._4_crystals_2_shape,
                              Variant.half_half_crystal, Variant._5_1_crystals, Variant._4_2_crystals,
                              Variant.half_crystal, Variant.pins))
                if Processor.STACKER in builder:
                    _bulk_remove((Variant.cut_out_5, Variant.cut_out_4, Variant._5_shapes_1_crystal, Variant._2_doubles,
                                  Variant.checkered_2_1_crystal_shape, Variant.cornered, Variant._4_shapes_2_crystal,
                                  Variant.checkered_atomic_crystal_shape, Variant._5_singles, Variant.cornered_1_1,
                                  Variant.checkered_2x_shape_crystal, Variant.cornered_2, Variant.cornered_asymmetrical,
                                  Variant.checkered_2_1_shape_crystal, Variant.cornered_atomic, Variant._2_singles))
                    if Processor.CUTTER in builder:
                        _bulk_remove((Variant._5_1, Variant._4_2, Variant.checkered, Variant._6_singles,
                                      Variant._3_doubles, Variant.checkered_atomic, Variant.checkered_asymmetrical,
                                      Variant.checkered_2_1, ))
                        if Processor.ROTATOR in builder:
                            variants[Variant.half_half] = False

        # Remove some things that are impossible due to shape context
        if builder.has_crystals:
            # Putting new layers with crystal on top of or under other crystals is tricky, especially since
            # the swapper can destroy other layers
            if Processor.PIN_PUSHER not in builder:
                variants[Variant.full_crystal] = False
            _bulk_remove((Variant.half_crystal, Variant._5_1_crystals, Variant._4_2_crystals, Variant.cornered_crystal,
                          Variant.cut_out_5_crystal, Variant.cut_out_4_crystal, Variant.checkered_2_1_crystal,
                          Variant.cornered_2_crystal, Variant._3_doubles_crystal, Variant.checkered_atomic_crystal,
                          Variant.cornered_atomic_crystal, Variant.cornered_asymmetrical_crystal,
                          Variant.checkered_2x_crystal_shape, Variant.half_half_crystal, Variant.checkered_crystal))
        if not len(builder.shape):
            variants[Variant.pins] = False
            if Processor.CUTTER not in builder or Processor.ROTATOR not in builder:
                variants[Variant.full_crystal] = False
        if force_non_pins:
            variants[Variant.pins] = False

        # Remove some low complexity variants if high complexity given
        if not any(builder.tasked) and complexity >= 20:
            _bulk_remove((Variant.double, Variant.cut_out_4, Variant.cut_out_5, Variant.checkered_2_1_crystal,
                          Variant.cornered_2, Variant.cornered, Variant._4_shapes_2_crystal, Variant.cornered_crystal,
                          Variant._5_1, Variant._4_2, Variant._4_crystals_2_shape, Variant._5_shapes_1_crystal,
                          Variant._5_crystals_1_shape, Variant.cut_out_5_crystal, Variant.cut_out_4_crystal))
            if Processor.CUTTER in builder and Processor.ROTATOR in builder:
                variants[Variant.half] = False
                if Processor.STACKER in builder or Processor.SWAPPER in builder:
                    variants[Variant.half_half] = False
                if Processor.CRYSTALLIZER in builder:
                    variants[Variant.half_crystal_half_shape] = False
            if sum(variants) > 1:
                variants[Variant.full] = False

        # If none available anymore, try to save it in some way
        if not any(variants):
            if complexity <= sum(builder.tasked) + 1:  # Maybe complexity was too restrictive
                complexity += 3
            elif not any(builder.tasked):  # If nothing tasked, then a full layer doesn't do anything
                variants[Variant.full] = True
                break
            else:  # Last resort, maybe a very bad combination?
                builder.tasked[rand.choice([x for x in range(8) if builder.tasked[x]])] = False
            continue
        break

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    def _tasked_sw_st(swc: int, stc: int, need_cu: bool):
        nonlocal complexity
        if Processor.SWAPPER in builder:
            complexity -= swc
            if Processor.STACKER not in builder or (Processor.CUTTER not in builder and not need_cu):
                builder.tasked[Processor.SWAPPER] = False
        else:
            complexity -= stc
            builder.tasked[Processor.STACKER] = False
            builder.tasked[Processor.CUTTER] = False if not need_cu else builder.tasked[Processor.CUTTER]
        builder.tasked[Processor.CUTTER] = False if need_cu else builder.tasked[Processor.CUTTER]
        builder.tasked[Processor.ROTATOR] = False

    def _bulk_tasked(comp: int, *t: Processor):
        nonlocal complexity
        complexity -= comp
        for tt in t:
            builder.tasked[tt] = False

    def _new_shape(_comp: int) -> str:
        if regen_pools and regen_pools[0]:
            _part = regen_pools[0].pop(rand.randint(0, len(regen_pools[0]) - 1))
            temp_pool = None
            if builder.tasked[Processor.MIXER] and _part[1] not in "ycmw":
                temp_pool = list(_p for _p in regen_pools[0] if _p[1] in "ymcw")
                _bulk_tasked(0, Processor.PAINTER, Processor.MIXER)
            elif builder.tasked[Processor.PAINTER] and _part[1] == "u":
                temp_pool = list(_p for _p in regen_pools[0] if _p[1] != "u")
                _bulk_tasked(0, Processor.PAINTER)
            if temp_pool is not None:
                if temp_pool:
                    # Already popped part is bad, so put it back and get a good part instead
                    regen_pools[0].append(_part)
                    _part = rand.choice(temp_pool)
                    regen_pools[0].remove(_part)
                else:
                    _part = _part[0] + generate_color(rand, _comp, False, builder)
            return _part
        return generate_shape(rand) + generate_color(rand, _comp, False, builder)

    def _new_crystal(_comp: int) -> str:
        if regen_pools and regen_pools[1]:
            return "c" + regen_pools[1].pop(rand.randint(0, len(regen_pools[1]) - 1))
        return "c" + generate_color(rand, _comp, True, builder)

    def _3_parts(c1: bool, c2: bool, c3: bool | None, no_same: bool) -> tuple[str, str, str]:
        nonlocal complexity
        complexity_1 = rand.triangular(0, complexity).__int__()
        complexity_2 = 0 if c3 is None else rand.triangular(0, complexity - complexity_1).__int__()
        complexity -= complexity_1 + complexity_2
        p1 = _new_shape(complexity_1) if not c1 else _new_crystal(complexity_1)
        p2 = _new_shape(complexity) if not c2 else _new_crystal(complexity)
        p3 = "--" if c3 is None else (_new_shape(complexity_2) if not c3 else _new_crystal(complexity_2))
        if no_same:
            # Do not use regen parts in order to guarantee uniqueness
            if p1 == p2:
                p2 = generate_shape(rand, p2[0]) + p2[1] if not c2 else "c" + generate_color(
                    rand, complexity, True, builder, p2[1]
                )
            while p3 in (p1, p2):
                p3 = generate_shape(rand, p3[0]) + p3[1] if not c3 else "c" + generate_color(
                    rand, complexity, True, builder, p3[1]
                )
        return p1, p2, p3

    variant_pool = [x for x in range(len(variants)) if variants[x]]
    if not variant_pool:
        raise Exception(f"{builder.debug_string()},\ncomplexity={complexity}, force_non_pins={force_non_pins}, "
                        f"variant_count={sum(variants)}")
    match rand.choice(variant_pool):
        case Variant.full:
            Layers.full(rand, builder, _new_shape(complexity))
        case Variant.half:
            _bulk_tasked(1, Processor.CUTTER)
            complexity_color = rand.randint(0, complexity)
            complexity -= complexity_color
            direction = 0
            if builder.tasked[Processor.ROTATOR]:
                possible_dirs = [] + ([1, 2, 4, 5] if builder.splits & 1 else [])
                possible_dirs += ([0, 2, 3, 5] if builder.splits & 2 else [])
                possible_dirs += ([0, 1, 3, 4] if builder.splits & 4 else [])
                possible_dirs += ([] if possible_dirs else [0, 1, 2, 3, 4, 5])
                direction = rand.choice(possible_dirs)
            elif Processor.ROTATOR in builder:
                possible_dirs = [0] + ([1, 5] if complexity else [])
                possible_dirs += ([2, 4] if complexity >= 2 else [])
                possible_dirs += ([3] if complexity >= 3 else [])
                direction = rand.choice(possible_dirs)
            Layers.half(rand, builder, _new_shape(complexity_color), direction)
        case Variant.half_half:
            if Processor.SWAPPER in builder:
                complexity -= 1
                if not builder.has_all(Processor.CUTTER, Processor.ROTATOR, Processor.STACKER):
                    builder.tasked[Processor.SWAPPER] = False
            else:
                _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.STACKER)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            direction = 0
            if builder.tasked[Processor.ROTATOR]:
                possible_dirs = [1, 2] if builder.splits & 1 else []
                possible_dirs += ([0, 2] if builder.splits & 2 else [])
                possible_dirs += ([0, 1] if builder.splits & 4 else [])
                possible_dirs += ([] if possible_dirs else [0, 1, 2])
                direction = rand.choice(possible_dirs)
            elif Processor.ROTATOR in builder:
                direction = rand.choice([0] + ([1, 2] if complexity else []))
            Layers.half_half(rand, builder, part_1, part_2, direction)
        case Variant.cut_out_5:
            _tasked_sw_st(4, 6, True)
            Layers.cut_out_5(rand, builder, _new_shape(complexity), rand.randint(0, 5))
        case Variant.cut_out_4:
            _tasked_sw_st(3, 5, True)
            Layers.cut_out_4(rand, builder, _new_shape(complexity), rand.randint(0, 5))
        case Variant._5_1:
            _tasked_sw_st(3, 12, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            Layers._5_1(rand, builder, part_1, part_2, rand.randint(0, 5))
        case Variant._4_2:
            _tasked_sw_st(4, 13, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            Layers._4_2(rand, builder, part_1, part_2, rand.randint(0, 5))
        case Variant.cornered:
            _tasked_sw_st(6, 10, True)
            Layers.cornered(rand, builder, _new_shape(complexity), rand.randint(0, 2))
        case Variant.cornered_2:
            _tasked_sw_st(6, 9, True)
            Layers.cornered_2(rand, builder, _new_shape(complexity), rand.randint(0, 2))
        case Variant.cornered_1_1:
            _tasked_sw_st(10, 21, True)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            Layers.cornered_1_1(rand, builder, part_1, part_2, rand.randint(0, 2))
        case Variant.cornered_atomic:
            _tasked_sw_st(8, 16, True)
            Layers.cornered_atomic(rand, builder, _new_shape(complexity), rand.randint(0, 1))
        case Variant.cornered_asymmetrical:
            _tasked_sw_st(9, 21, True)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            Layers.cornered_asymmetrical(rand, builder, part_1, part_2, rand.randint(0, 2))
        case Variant.checkered:
            _tasked_sw_st(9, 32, False)
            Layers.checkered(rand, builder, _3_parts(False, False, False, True))
        case Variant.checkered_2_1:
            _tasked_sw_st(4, 21, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            Layers.checkered_2_1(rand, builder, part_1, part_2, rand.randint(0, 2))
        case Variant.checkered_atomic:
            _tasked_sw_st(7, 32, False)
            Layers.checkered_atomic(rand, builder, _3_parts(False, False, None, True)[:2])
        case Variant.checkered_asymmetrical:
            _tasked_sw_st(5, 20, False)
            part_1, part_2, _ = _3_parts(False, False, None, True)
            Layers.checkered_asymmetrical(rand, builder, part_1, part_2, (rand.randint(0, 2), rand.choice((2, -1))))
        case Variant._3_doubles:
            _tasked_sw_st(5, 14, False)
            part_1, part_2, part_3 = _3_parts(False, False, False, True)
            Layers._3_doubles(rand, builder, part_1, part_2, part_3, rand.randint(0, 1))
        case Variant.pins:
            builder.tasked[Processor.PIN_PUSHER] = False
            Layers.pins(builder)
        case Variant.full_crystal:
            # Assumes either has pin pusher or not already_has_crystals
            # Needs extra handling because of that
            if Processor.PIN_PUSHER in builder or builder.has_crystals:
                complexity -= 1
                if Processor.ROTATOR not in builder or Processor.CUTTER not in builder:
                    builder.tasked[Processor.PIN_PUSHER] = False
            else:
                _bulk_tasked(7, Processor.CUTTER, Processor.ROTATOR)
            builder.tasked[Processor.CRYSTALLIZER] = False
            Layers.full_crystal(builder, _new_crystal(complexity))
        case Variant.half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            complexity_color = rand.randint(0, complexity)
            complexity -= complexity_color
            part = _new_crystal(complexity_color)
            possible_dirs = [3] + ([2, 4] if complexity else [])
            possible_dirs += ([1, 5] if complexity >= 2 else [])
            possible_dirs += ([0] if complexity >= 3 else [])
            Layers.half_crystal(rand, builder, _new_crystal(complexity_color), rand.choice(possible_dirs))
        case Variant.half_half_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(6, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            possible_dirs = [0] + ([1, 2] if complexity else [])
            Layers.half_half_crystal(rand, builder, part_1, part_2, rand.choice(possible_dirs))
        case Variant.half_crystal_half_shape:
            _bulk_tasked(2, Processor.CUTTER, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(False, True, None, False)
            possible = [True, False, False, False, False, False]
            if complexity and Processor.ROTATOR in builder:
                possible[1:3] = [True, True]
                if complexity >= 2:
                    possible[3:5] = [True, True]
                    if complexity >= 3:
                        possible[5] = True
            if builder.tasked[Processor.ROTATOR]:
                if builder.splits & 1:
                    possible[0:3] = [False, True, True]
                    possible[5] = False
                elif builder.splits & 2:
                    possible[1:4] = [False, possible[2], False]
                elif builder.splits & 4:
                    possible[2:5] = [False, possible[3], False]
            Layers.half_crystal_half_shape(rand, builder, part_2, part_1,
                                           rand.choice([i for i in range(6) if possible[i]]))
        case Variant.cut_out_5_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(9, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            Layers.cut_out_5_crystal(rand, builder, _new_crystal(complexity), rand.randint(0, 5))
        case Variant.cut_out_4_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(11, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            Layers.cut_out_4_crystal(rand, builder, _new_crystal(complexity), rand.randint(0, 5))
        case Variant._5_1_crystals:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            Layers._5_1_crystals(rand, builder, part_1, part_2, rand.randint(0, 5))
        case Variant._4_2_crystals:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(8, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            Layers._4_2_crystals(rand, builder, part_1, part_2, rand.randint(0, 5))
        case Variant._5_crystals_1_shape:
            _bulk_tasked(5, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(False, True, None, False)
            Layers._5_crystals_1_shape(rand, builder, part_2, part_1, rand.randint(0, 5))
        case Variant._5_shapes_1_crystal:
            _tasked_sw_st(4, 8, True)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(False, True, None, False)
            Layers._5_shapes_1_crystal(rand, builder, part_1, part_2, rand.randint(0, 5))
        case Variant._4_crystals_2_shape:
            _bulk_tasked(4, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER)
            part_1, part_2, _ = _3_parts(True, False, None, False)
            Layers._4_crystals_2_shape(rand, builder, part_1, part_2, rand.randint(0, 5))
        case Variant._4_shapes_2_crystal:
            _tasked_sw_st(4, 8, True)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(True, False, None, False)
            Layers._4_shapes_2_crystal(rand, builder, part_2, part_1, rand.randint(0, 5))
        case Variant.cornered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(12, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            Layers.cornered_crystal(rand, builder, _new_crystal(complexity), rand.randint(0, 2))
        case Variant.cornered_2_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(14, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            Layers.cornered_2_crystal(rand, builder, _new_crystal(complexity), rand.randint(0, 2))
        case Variant.cornered_atomic_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(26, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            Layers.cornered_atomic_crystal(rand, builder, _new_crystal(complexity), rand.randint(0, 1))
        case Variant.cornered_asymmetrical_crystal:
            _bulk_tasked(14, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            Layers.cornered_asymmetrical_crystal(rand, builder, part_1, part_2, rand.randint(0, 2))
        case Variant.checkered_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(20, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            Layers.checkered_crystal(rand, builder, _3_parts(True, True, True, True))
        case Variant.checkered_2x_crystal_shape:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(14, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, parts_3 = _3_parts(False, True, True, True)
            Layers.checkered_2x_crystal_shape(rand, builder, part_1, part_2, parts_3, rand.randint(0, 2))
        case Variant.checkered_2x_shape_crystal:
            _tasked_sw_st(12, 23, True)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, parts_3 = _3_parts(True, False, False, True)
            Layers.checkered_2x_shape_crystal(rand, builder, part_1, part_2, parts_3, rand.randint(0, 2))
        case Variant.checkered_2_1_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(13, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, _ = _3_parts(True, True, None, True)
            Layers.checkered_2_1_crystal(rand, builder, part_1, part_2, rand.randint(0, 2))
        case Variant.checkered_2_1_crystal_shape:
            # Assumes this doesn't happen when already_has_crystals
            _tasked_sw_st(7, 11, True)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(True, False, None, False)
            Layers.checkered_2_1_crystal_shape(rand, builder, part_1, part_2, rand.randint(0, 2))
        case Variant.checkered_2_1_shape_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _tasked_sw_st(7, 10, True)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(False, True, None, False)
            Layers.checkered_2_1_shape_crystal(rand, builder, part_1, part_2, rand.randint(0, 2))
        case Variant.checkered_atomic_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(20, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            Layers.checkered_atomic_crystal(rand, builder, _3_parts(True, True, None, True)[:2])
        case Variant.checkered_atomic_crystal_shape:
            # Assumes this doesn't happen when already_has_crystals
            _tasked_sw_st(9, 17, True)
            builder.tasked[Processor.CRYSTALLIZER] = False
            part_1, part_2, _ = _3_parts(True, False, None, False)
            Layers.checkered_atomic_crystal_shape(rand, builder, part_2, part_1, rand.randint(0, 1))
        case Variant._3_doubles_crystal:
            # Assumes this doesn't happen when already_has_crystals
            _bulk_tasked(15, Processor.CUTTER, Processor.ROTATOR, Processor.CRYSTALLIZER, Processor.SWAPPER)
            part_1, part_2, part_3 = _3_parts(True, True, True, True)
            Layers._3_doubles_crystal(rand, builder, part_1, part_2, part_3, rand.randint(0, 1))
        case Variant.single:
            _bulk_tasked(0, Processor.CUTTER, Processor.ROTATOR)
            if Processor.CRYSTALLIZER in builder and complexity >= 7 and not builder.has_crystals:
                _bulk_tasked(7, Processor.CRYSTALLIZER)
                part = _new_crystal(complexity)
            else:
                complexity -= 4
                part = _new_shape(complexity)
            Layers.single(rand, builder, part, rand.randint(0, 5))
        case Variant.double:
            _bulk_tasked(0, Processor.CUTTER, Processor.ROTATOR)
            if Processor.CRYSTALLIZER in builder and complexity >= 7 and not builder.has_crystals:
                _bulk_tasked(7, Processor.CRYSTALLIZER)
                part = _new_crystal(complexity)
            else:
                complexity -= 3
                part = _new_shape(complexity)
            Layers.double(rand, builder, part, rand.randint(0, 5))
        case Variant._2_singles:
            generate_2_shapes(rand, complexity, builder, regen_pools)
        case Variant._2_doubles:
            generate_2_doubles(rand, complexity, builder, regen_pools)
        case Variant._5_singles:
            generate_5_shapes(rand, complexity, builder, regen_pools)
        case Variant._6_singles:
            generate_6_shapes(rand, complexity, builder, regen_pools)
        case e:
            raise Exception(f"Unknown layer variant {e}:\n"
                            f"complexity = {complexity},\n"
                            f"builder = {builder.debug_string()}\n"
                            f"variant pool = {variant_pool}")


def generate_2_shapes(rand: Random, complexity: int, builder: ShapeBuilder, regen_pools: tuple[list[str], ...]) -> None:
    from .layers_hexagonal import Layers

    builder.tasked[Processor.CUTTER] = False
    builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if builder.tasked[Processor.MIXER]:
        if Processor.CRYSTALLIZER in builder:
            stored_complexity = 1
        else:
            stored_complexity = 2
    elif builder.tasked[Processor.PAINTER]:
        stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 9
    if Processor.CRYSTALLIZER in builder and complexity >= 6 and not builder.has_crystals:
        _bulk_possible(subvariants, complexity, (3, ), (6, 9))
        if Processor.SWAPPER in builder and complexity >= 9:
            _bulk_possible(subvariants, complexity, (5, ), (4, 10), (8, 12), (7, 14))
        if Processor.STACKER in builder and complexity >= 12:
            _bulk_possible(subvariants, complexity, (4, ), (5, 13))
    if Processor.SWAPPER in builder and complexity >= 6:
        _bulk_possible(subvariants, complexity, (0, 2), (1, 7))
    if Processor.STACKER in builder and complexity >= 9:
        _bulk_possible(subvariants, complexity, (1, ), (0, 10), (2, 10))
    if builder.tasked[Processor.PAINTER]:
        subvariants[6:] = [False] * 3

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    if not subvariant_pool:
        raise Exception(f"{builder.debug_string()},\ncomplexity={complexity}, variant_count={sum(subvariants)}")
    chosen = rand.choice(subvariant_pool)
    match chosen:
        case 0:  # adjacent shapes, swapper 6 stacker 10
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 6, 10, (False, False, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, True, 0, parts[:2], (direction, direction+1), chosen)
        case 1:  # close shapes, swapper 7 stacker 9
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 7, 9, (False, False, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, True, 0, parts[:2], (direction, direction+2), chosen)
        case 2:  # cornered shapes, swapper 6 stacker 10
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 6, 10, (False, False, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, True, 0, parts[:2], (direction, direction+3), chosen)
        case 3:  # adjacent shape crystal, 6
            complexity -= 6
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (False, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, True, 1, parts[:2], (direction, direction+rand.choice((1, -1))), chosen)
        case 4:  # close shapes crystal, swapper 10 stacker 12
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 10, 12, (False, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, True, 1, parts[:2], (direction, direction+rand.choice((2, -2))), chosen)
        case 5:  # cornered shapes crystal, swapper 9 stacker 13
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 9, 13, (False, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, True, 1, parts[:2], (direction, direction+3), chosen)
        case 6:  # adjacent crystals, 9
            complexity -= 9
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, False, 2, parts[:2], (direction, direction+1), chosen)
        case 7:  # close crystals, swapper 14
            complexity -= 14
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, False, 2, parts[:2], (direction, direction+2), chosen)
        case 8:  # cornered crystals, swapper 12
            complexity -= 12
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_singles(rand, builder, False, 2, parts[:2], (direction, direction+3), chosen)


def generate_2_doubles(rand: Random, complexity: int, builder: ShapeBuilder,
                       regen_pools: tuple[list[str], ...]) -> None:
    from .layers_hexagonal import Layers

    builder.tasked[Processor.CUTTER] = False
    builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if builder.tasked[Processor.MIXER]:
        if Processor.CRYSTALLIZER in builder:
            stored_complexity = 1
        else:
            stored_complexity = 2
    elif builder.tasked[Processor.PAINTER]:
        stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 6
    if Processor.CRYSTALLIZER in builder and complexity >= 10 and not builder.has_crystals:
        if Processor.SWAPPER in builder:
            _bulk_possible(subvariants, complexity, (2, 3, ), (4, 14), (5, 14))
        if Processor.STACKER in builder and complexity >= 12:
            _bulk_possible(subvariants, complexity, (2, ), (3, 13))
    if Processor.SWAPPER in builder and complexity >= 6:
        _bulk_possible(subvariants, complexity, (0, 1, ))
    if Processor.STACKER in builder and complexity >= 8:
        _bulk_possible(subvariants, complexity, (0, ), (1, 9))
    if builder.tasked[Processor.PAINTER]:
        subvariants[4:] = [False] * 2

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    if not subvariant_pool:
        raise Exception(f"{builder.debug_string()},\ncomplexity={complexity}, variant_count={sum(subvariants)}")
    chosen = rand.choice(subvariant_pool)
    match chosen:
        case 0:  # adjacent shapes, swapper 6 stacker 8
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 6, 8, (False, False, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_doubles(rand, builder, True, 0, parts[:2], (direction, direction+2), chosen)
        case 1:  # cornered shapes, swapper 6 stacker 9
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 6, 9, (False, False, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_doubles(rand, builder, True, 0, parts[:2], (direction, direction+3), chosen)
        case 2:  # adjacent shape crystal, swapper 10 stacker 12
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 10, 12, (False, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_doubles(rand, builder, True, 1, parts[:2], (direction, direction+rand.choice((2, -2))), chosen)
        case 3:  # cornered shapes crystal, swapper 10 stacker 13
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 10, 13, (False, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_doubles(rand, builder, True, 1, parts[:2], (direction, direction+3), chosen)
        case 4:  # adjacent crystals, swapper 14
            complexity -= 14
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_doubles(rand, builder, False, 2, parts[:2], (direction, direction+2), chosen)
        case 5:  # cornered crystals, swapper 14
            complexity -= 14
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, None, None, None, None))
            direction = rand.randint(0, 5)
            Layers._2_doubles(rand, builder, False, 2, parts[:2], (direction, direction+3), chosen)


def generate_5_shapes(rand: Random, complexity: int, builder: ShapeBuilder, regen_pools: tuple[list[str], ...]) -> None:
    from .layers_hexagonal import Layers

    builder.tasked[Processor.CUTTER] = False
    builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if builder.tasked[Processor.MIXER]:
        if Processor.CRYSTALLIZER in builder:
            stored_complexity = 1
        else:
            stored_complexity = 2
    elif builder.tasked[Processor.PAINTER]:
        stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 11
    if Processor.CRYSTALLIZER in builder and complexity >= 13 and not builder.has_crystals:
        if Processor.SWAPPER in builder:
            _bulk_possible(
                subvariants, complexity, (2, 6, 8, ),
                (5, 14), (7, 14), (9, 14), (3, 15), (4, 15), (1, 17), (10, 19), (0, 20)
            )
        if Processor.STACKER in builder and complexity >= 22:
            _bulk_possible(subvariants, complexity, (4, 5, ), (2, 23), (3, 23), (1, 24), (0, 26))
    if Processor.SWAPPER in builder and complexity >= 9:
        subvariants[0] = True
    if Processor.STACKER in builder and complexity >= 26:
        subvariants[0] = True
    if builder.tasked[Processor.PAINTER]:
        subvariants[10] = False
    if builder.tasked[Processor.STACKER]:
        subvariants[6:] = [False] * 5

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    if not subvariant_pool:
        raise Exception(f"{builder.debug_string()},\ncomplexity={complexity}, variant_count={sum(subvariants)}")
    chosen = rand.choice(subvariant_pool)
    match chosen:
        case 0:  # no crystal, swapper 9 stacker 26
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 20, 26, (False, False, False, False, False, None))
            Layers._5_singles(rand, builder, True, 0, parts[:5], rand.randint(0, 5), False, chosen)
        case 1:  # 1 crystal edge, swapper 17 stacker 24
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 17, 24, (True, False, False, False, False, None))
            Layers._5_singles(rand, builder, True, 1, parts[:5], rand.randint(0, 5), rand.choice((True, False)), chosen)
        case 2:  # 1 crystal other, swapper 13 stacker 23
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 13, 23, (False, True, False, False, False, None))
            Layers._5_singles(rand, builder, True, 1, parts[:5], rand.randint(0, 5), rand.choice((True, False)), chosen)
        case 3:  # 1 crystal center, swapper 15 stacker 23
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 15, 23, (False, False, True, False, False, None))
            Layers._5_singles(rand, builder, True, 1, parts[:5], rand.randint(0, 5), False, chosen)
        case 4:  # 3 crystals adjacent edge, swapper 15 stacker 22
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 15, 22, (True, True, True, False, False, None))
            Layers._5_singles(rand, builder, True, 3, parts[:5], rand.randint(0, 5), rand.choice((True, False)), chosen)
        case 5:  # 3 crystals adjacent center, swapper 14 stacker 22
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 14, 22, (False, True, True, True, False, None))
            Layers._5_singles(rand, builder, True, 3, parts[:5], rand.randint(0, 5), False, chosen)
        case 6:  # 3 crystals 2 2 1, swapper only 13
            complexity -= 13
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, False, False, True, None))
            Layers._5_singles(rand, builder, True, 3, parts[:5], rand.randint(0, 5), rand.choice((True, False)), chosen)
        case 7:  # 3 crystals atomic, swapper only 14
            complexity -= 14
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, False, True, False, True, None))
            Layers._5_singles(rand, builder, True, 3, parts[:5], rand.randint(0, 5), False, chosen)
        case 8:  # 3 crystals 1 1 2 1, swapper only 13
            complexity -= 13
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, False, True, True, False, None))
            Layers._5_singles(rand, builder, True, 3, parts[:5], rand.randint(0, 5), rand.choice((True, False)), chosen)
        case 9:  # 3 crystals 2 1 1 1, swapper only 14
            complexity -= 14
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, False, True, False, None))
            Layers._5_singles(rand, builder, True, 3, parts[:5], rand.randint(0, 5), rand.choice((True, False)), chosen)
        case 10:  # 5 crystals, swapper only 19
            complexity -= 19
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, True, True, True, None))
            Layers._5_singles(rand, builder, False, 5, parts[:5], rand.randint(0, 5), False, chosen)


def generate_6_shapes(rand: Random, complexity: int, builder: ShapeBuilder, regen_pools: tuple[list[str], ...]) -> None:
    from .layers_hexagonal import Layers

    builder.tasked[Processor.ROTATOR] = False

    # Decide on the layer variant, but consider that mixer and/or painter might be important
    stored_complexity = 0
    if builder.tasked[Processor.MIXER]:
        if Processor.CRYSTALLIZER in builder:
            stored_complexity = 1
        else:
            stored_complexity = 2
    elif builder.tasked[Processor.PAINTER]:
        stored_complexity = 1
    complexity -= stored_complexity

    subvariants = [False] * 7
    if (
        Processor.CRYSTALLIZER in builder and Processor.CUTTER in builder and
        complexity >= 10 and not builder.has_crystals
    ):
        if Processor.SWAPPER in builder:
            _bulk_possible(subvariants, complexity, (1, ), (2, 12), (4, 12), (3, 14), (5, 17), (6, 22))
        if Processor.STACKER in builder and complexity >= 28:
            _bulk_possible(subvariants, complexity, (2, ), (1, 29))
    if Processor.SWAPPER in builder and complexity >= 9:
        subvariants[0] = True
    if Processor.STACKER in builder and Processor.CUTTER in builder and complexity >= 32:
        subvariants[0] = True
    if builder.tasked[Processor.PAINTER]:
        subvariants[6] = False
    if builder.tasked[Processor.STACKER]:
        subvariants[3:] = [False] * 4

    # Restore complexity for painting and mixing
    complexity += stored_complexity

    subvariant_pool = list(x for x in range(6) if subvariants[x])
    if not subvariant_pool:
        raise Exception(f"{builder.debug_string()},\ncomplexity={complexity}, variant_count={sum(subvariants)}")
    chosen = rand.choice(subvariant_pool)
    match chosen:
        case 0:  # no crystal, swapper no cutter 9 stacker 32
            if Processor.SWAPPER in builder:
                complexity -= 9
                if Processor.STACKER not in builder:
                    builder.tasked[Processor.SWAPPER] = False
            else:
                complexity -= 32
                builder.tasked[Processor.STACKER] = False
                builder.tasked[Processor.CUTTER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (False, False, False, False, False, False))
            Layers._6_singles(rand, builder, True, 0, parts, rand.randint(0, 5), False, chosen)
        case 1:  # 1 crystal, swapper 10 stacker 29
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 10, 29, (True, False, False, False, False, False))
            Layers._6_singles(rand, builder, True, 1, parts, rand.randint(0, 5), False, chosen)
        case 2:  # 3 crystal adjacent, swapper 12 stacker 28
            builder.tasked[Processor.CRYSTALLIZER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                True, 12, 28, (True, True, True, False, False, False))
            Layers._6_singles(rand, builder, True, 3, parts, rand.randint(0, 5), False, chosen)
        case 3:  # 3 crystal atomic, swapper only 14
            complexity -= 14
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, False, True, False, True, False))
            Layers._6_singles(rand, builder, True, 3, parts, rand.randint(0, 5), False, chosen)
        case 4:  # 3 crystals asymmetrical, swapper only 12
            complexity -= 12
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, False, True, False, False))
            Layers._6_singles(rand, builder, True, 3, parts, rand.randint(0, 5), rand.choice((True, False)), chosen)
        case 5:  # 5 crystals, swapper only 17
            complexity -= 17
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, True, True, True, False))
            Layers._6_singles(rand, builder, True, 5, parts, rand.randint(0, 5), False, chosen)
        case 6:  # 6 crystals, swapper only 22
            complexity -= 22
            builder.tasked[Processor.CRYSTALLIZER] = False
            builder.tasked[Processor.SWAPPER] = False
            parts = _subvariant(rand, builder, complexity, regen_pools,
                                False, 0, 0, (True, True, True, True, True, True))
            Layers._6_singles(rand, builder, False, 6, parts, rand.randint(0, 5), False, chosen)


def generate_shape(rand: Random, exclude: str | None = None) -> str:
    shapes = ["H", "F", "G"]
    if exclude is not None:
        if exclude not in shapes:
            raise Exception("Bad to-be-excluded shape: " + exclude)
        shapes.remove(exclude)
    return rand.choice(shapes)


adjacent_colors = {
    "r": ("y", "m"),
    "b": ("m", "c"),
    "g": ("y", "c"),
    "y": ("r", "g"),
    "c": ("g", "b"),
    "m": ("b", "r"),
    "w": ("m", "c", "y"),
}


def generate_color(rand: Random, complexity: int, is_crystal: bool,
                   builder: ShapeBuilder, exclude: str | None = None) -> str:

    white_comp = 2 if is_crystal else 3
    mixing_comp = 1 if is_crystal else 2
    base_comp = 0 if is_crystal else 1

    # Disable colors based on importance, availability, and complexity
    # True means must be included, False means must not be included, None means it doesn't matter
    color_types: dict[str, bool] = {c: True for c in ("u", "p", "s", "w")}
    if Processor.MIXER not in builder:
        color_types["s"] = False
        color_types["w"] = False
        if Processor.PAINTER not in builder and not is_crystal:
            color_types["p"] = False
    if is_crystal:
        color_types["u"] = False
    if complexity < white_comp:
        color_types["w"] = False
    if builder.tasked[Processor.MIXER]:
        color_types["p"] = False
        if Processor.PAINTER in builder:
            color_types["u"] = False
    elif complexity < mixing_comp:
        color_types["s"] = False
        if complexity < base_comp and not builder.tasked[Processor.PAINTER]:
            color_types["p"] = False
    if builder.tasked[Processor.PAINTER]:
        color_types["u"] = False
    if Processor.PAINTER not in builder and not is_crystal:
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
    if builder.shape:
        preferred_layer = rand.choice(builder.shape)
        preferred: str | None = None
        for i in range(1, 12, 2):
            if preferred_layer[i] not in "u-" and preferred_layer[i-1] != "c":
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
        raise Exception(f"No color left to pick:\nbuilder = {builder.debug_string()},\n"
                        f"complexity = {complexity}, is crystal = {is_crystal}")

    final = rand.choice(colors)
    if final in "ymcw":
        builder.tasked[Processor.MIXER] = False
    if final != "u" and not is_crystal:
        builder.tasked[Processor.PAINTER] = False
    return final


def stack(rand: Random, builder: ShapeBuilder, layer: str, has_non_crystal: bool,
          crystal_colors: int, *, blueprint: bool | None = None) -> bool:

    if not len(builder.shape):
        builder.shape.append(layer)
        if crystal_colors:
            builder.has_crystals = True
        return False

    builder.tasked[Processor.STACKER] = False

    if blueprint is not None:
        stack_top = blueprint
    elif builder.has_crystals:
        # Assumes that in this case the new layer only has one crystal color (if any) and no empty part
        stack_top = True
    elif crystal_colors > 1 or not has_non_crystal or (crystal_colors and has_non_crystal and "--" in layer):
        stack_top = False
    else:
        stack_top = rand.choice((False, True))

    if stack_top:
        if crystal_colors:
            # Make sure the non-crystal part is always placed on a non-empty corner
            # Assumes either there is the rotator at this point or the left side is not empty
            # Also assumes there is only one crystal color
            if builder.tasked[Processor.ROTATOR]:
                layer = layer[10:12] + layer[0:10]
                builder.tasked[Processor.ROTATOR] = False
            for i in range(0, 12, 2):
                if layer[i] not in "Pc-" and builder.shape[-1][i] != "-":
                    break
            else:
                builder.tasked[Processor.ROTATOR] = False
                for _ in range(5):
                    layer = layer[10:12] + layer[0:10]
                    for i in range(0, 12, 2):
                        if layer[i] not in "Pc-" and builder.shape[-1][i] != "-":
                            break
                    else:
                        continue
                    break
                else:
                    raise Exception(f"New layer supposed to be placed on top, but not possible:\n"
                                    f"builder = {builder.debug_string()}, new layer = {layer}")
            crys_col = ""
            for i in range(0, 12, 2):
                if layer[i] == "c":
                    crys_col = layer[i+1]
                    break
            fill_crystal(builder, crys_col)
            builder.shape.append(layer)
        else:
            for j in range(0, 12, 2):
                if layer[j:j+2] != "--" and builder.shape[-1][j:j+2] != "--":
                    builder.shape.append(layer)
                    break
            else:
                for i in reversed(range(len(builder.shape) - 1)):
                    for j in range(0, 12, 2):
                        if layer[j:j+2] != "--" and builder.shape[i][j:j+2] != "--":
                            builder.shape[i+1] = merge_layers(layer, builder.shape[i+1])
                            break
                    else:
                        continue
                    break
                else:
                    builder.shape[0] = merge_layers(layer, builder.shape[0])
    else:
        for j in range(0, 12, 2):
            if layer[j:j+2] != "--" and builder.shape[0][j:j+2] != "--":
                builder.shape.insert(0, layer)
                for i in range(0, 12, 2):
                    if builder.shape[0][i] == "-" and builder.shape[1][i] == "P":
                        for k in range(2, len(builder.shape)):
                            if builder.shape[k][i] != "P":
                                builder.shape[k-1] = builder.shape[k-1][:i] + "-" + builder.shape[k-1][i+1:]
                                builder.shape[0] = builder.shape[0][:i] + "P" + builder.shape[0][i+1:]
                                break
                        else:
                            builder.shape[-1] = builder.shape[-1][:i] + "-" + builder.shape[-1][i+1:]
                            builder.shape[0] = builder.shape[0][:i] + "P" + builder.shape[0][i+1:]
                break
        else:
            builder.shape[0] = merge_layers(layer, builder.shape[0])

    if crystal_colors:
        builder.has_crystals = True

    return stack_top


def merge_layers(layer_1: str, layer_2: str) -> str:
    merged = ""
    for k in range(0, 12, 2):
        if layer_1[k:k + 2] != "--":
            merged += layer_1[k:k + 2]
        else:
            merged += layer_2[k:k + 2]
    return merged


def fill_crystal(builder: ShapeBuilder, color: str) -> None:
    for j in range(len(builder.shape)):
        for i in range(1, 12, 2):
            if builder.shape[j][i] == "-":
                builder.shape[j] = builder.shape[j][:i-1] + "c" + color + builder.shape[j][i+1:]


def _bulk_possible(variants: list[bool], complexity: int, v: tuple[int, ...], *vc: tuple[int, int]):
    # IMPORTANT: Always sort by complexity in bulks
    for vv in v:
        variants[vv] = True
    for vv, cc in vc:
        if complexity >= cc:
            variants[vv] = True
        else:
            break


def _subvariant(rand: Random, builder: ShapeBuilder, complexity: int, regen_pools: tuple[list[str], ...],
                swapper_stacker: bool, a: int, b: int, is_crys: tuple[bool | None, ...]) -> list[str]:

    def _new_shape(_comp: int) -> str:
        if regen_pools and regen_pools[0]:
            _part = regen_pools[0].pop(rand.randint(0, len(regen_pools[0]) - 1))
            temp_pool = None
            if builder.tasked[Processor.MIXER] and _part[1] not in "ycmw":
                temp_pool = list(_p for _p in regen_pools[0] if _p[1] in "ymcw")
                builder.tasked[Processor.PAINTER] = False
                builder.tasked[Processor.MIXER] = False
            elif builder.tasked[Processor.PAINTER] and _part[1] == "u":
                temp_pool = list(_p for _p in regen_pools[0] if _p[1] != "u")
                builder.tasked[Processor.PAINTER] = False
            if temp_pool is not None:
                if temp_pool:
                    # Already popped part is bad, so put it back and get a good part instead
                    regen_pools[0].append(_part)
                    _part = rand.choice(temp_pool)
                    regen_pools[0].remove(_part)
                else:
                    _part = _part[0] + generate_color(rand, _comp, False, builder)
            return _part
        return generate_shape(rand) + generate_color(rand, _comp, False, builder)

    def _new_crystal(_comp: int) -> str:
        if regen_pools and regen_pools[1]:
            return "c" + regen_pools[1].pop(rand.randint(0, len(regen_pools[1]) - 1))
        return "c" + generate_color(rand, _comp, True, builder)

    if swapper_stacker:
        if Processor.SWAPPER in builder:
            complexity -= a
            if Processor.STACKER not in builder:
                builder.tasked[Processor.SWAPPER] = False
        else:
            complexity -= b
            builder.tasked[Processor.STACKER] = False
    complexity_parts = [rand.triangular(0, complexity).__int__()]
    for i in range(2, 6):
        complexity_parts.append(
            0 if is_crys[i] is None else rand.triangular(0, complexity - sum(complexity_parts)).__int__()
        )
    complexity -= sum(complexity_parts)
    parts = [_new_shape(complexity_parts[0]) if not is_crys[0] else _new_crystal(complexity_parts[0]),
             _new_shape(complexity) if not is_crys[1] else _new_crystal(complexity)]
    for i in range(2, 6):
        parts.append("--" if is_crys[i] is None else (_new_shape(complexity_parts[i-1]) if not is_crys[i]
                                                      else _new_crystal(complexity_parts[i-1])))
    return parts
