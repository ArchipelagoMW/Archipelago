from random import Random
from typing import Sequence

from . import ShapeBuilder, Processor
from .generate_hexagonal import Variant, stack, fill_crystal


def _blueprint(builder: ShapeBuilder, layer: int | None, stack_top: bool, var: int, data: dict):
    if layer == -1:
        builder.blueprint.append((var, stack_top, data))
    elif layer is not None:
        builder.blueprint[layer] = (var, stack_top, data)


def _ordered(rand: Random, builder: ShapeBuilder, stack_top: bool, list_len: int, split: tuple[int, int] | int,
             has_non_crys: bool, crys_col: int, p_fill: str, *p_dirs: tuple[str, int]) -> bool:
    ordered = [p_fill] * list_len
    for part, _dir in p_dirs:
        ordered[_dir % list_len] = part
    stack_top = stack(rand, builder, "".join(ordered) * (6//list_len), has_non_crys, crys_col, blueprint=stack_top)
    builder.splits |= 7 if split == 7 else 1 << (split[0] % 3) | 1 << (sum(split) % 3)
    return stack_top


class Layers:

    @staticmethod
    def full(rand: Random, builder: ShapeBuilder, part: str,
             *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = stack(rand, builder, part * 6, True, 0, blueprint=stack_top)
        _blueprint(builder, layer, stack_top, Variant.full, {"part": part})

    @staticmethod
    def half(rand: Random, builder: ShapeBuilder, part: str, direct: int,
             *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 0),
                             True, 0, "--", (part, direct), (part, direct+1), (part, direct+2))
        _blueprint(builder, layer, stack_top, Variant.half, {"direction": direct, "part": part})

    @staticmethod
    def half_half(rand: Random, builder: ShapeBuilder, part_fill: str, part_dir: str, direct: int,
                  *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 0),
                             True, 0, part_fill, (part_dir, direct), (part_dir, direct+1), (part_dir, direct+2))
        _blueprint(builder, layer, stack_top, Variant.half_half, {"direction": direct, "parts": (part_fill, part_dir)})

    @staticmethod
    def cut_out_5(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                  *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 1),
                             True, 0, part, ("--", direct))
        _blueprint(builder, layer, stack_top, Variant.cut_out_5, {"direction": direct, "part": part})

    @staticmethod
    def cut_out_4(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                  *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, -1),
                             True, 0, part, ("--", direct), ("--", direct+1))
        _blueprint(builder, layer, stack_top, Variant.cut_out_4, {"direction": direct, "part": part})

    @staticmethod
    def _5_1(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
             *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 1),
                             True, 0, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant._5_1, {"direction": direct, "parts": (p_fill, p_dir)})

    @staticmethod
    def _4_2(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
             *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, -1),
                             True, 0, p_fill, (p_dir, direct), (p_dir, direct+1))
        _blueprint(builder, layer, stack_top, Variant._4_2, {"direction": direct, "parts": (p_fill, p_dir)})

    @staticmethod
    def cornered(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                 *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, +1),
                             True, 0, "--", (part, direct))
        _blueprint(builder, layer, stack_top, Variant.cornered, {"direction": direct, "part": part})

    @staticmethod
    def cornered_2(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                   *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, -1),
                             True, 0, "--", (part, direct), (part, direct+1))
        _blueprint(builder, layer, stack_top, Variant.cornered_2, {"direction": direct, "part": part})

    @staticmethod
    def cornered_1_1(rand: Random, builder: ShapeBuilder, part_1: str, part_2: str, direct: int,
                     *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, 7,
                             True, 0, "--", (part_1, direct), (part_2, direct+1))
        _blueprint(builder, layer, stack_top, Variant.cornered_1_1, {"direction": direct, "parts": (part_1, part_2)})

    @staticmethod
    def cornered_atomic(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                        *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 2, 7,
                             True, 0, "--", (part, direct))
        _blueprint(builder, layer, stack_top, Variant.cornered_atomic, {"direction": direct, "part": part})

    @staticmethod
    def cornered_asymmetrical(rand: Random, builder: ShapeBuilder, part_1: str, part_2: str, direct: int,
                              *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, 7, True, 0, "--",
                             (part_1, direct), (part_1, direct+2), (part_2, direct-1), (part_2, direct+3))
        _blueprint(builder, layer, stack_top, Variant.cornered_asymmetrical, {"direction": direct,
                                                                              "parts": (part_1, part_2)})

    @staticmethod
    def checkered(rand: Random, builder: ShapeBuilder, parts: Sequence[str],
                  *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = stack(rand, builder, "".join(parts) * 2, True, 0, blueprint=stack_top)
        builder.splits |= 7
        _blueprint(builder, layer, stack_top, Variant.checkered, {"parts": parts})

    @staticmethod
    def checkered_2_1(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                      *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, 1),
                             True, 0, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant.checkered_2_1, {"direction": direct, "parts": (p_fill, p_dir)})

    @staticmethod
    def checkered_atomic(rand: Random, builder: ShapeBuilder, parts: Sequence[str],
                         *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = stack(rand, builder, "".join(parts) * 3, True, 0, blueprint=stack_top)
        builder.splits |= 7
        _blueprint(builder, layer, stack_top, Variant.checkered_atomic, {"parts": parts})

    @staticmethod
    def checkered_asymmetrical(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str,
                               directs: Sequence[int], *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, 7,
                             True, 0, p_fill, (p_dir, directs[0]), (p_dir, directs[0]+3), (p_dir, sum(directs)))
        _blueprint(builder, layer, stack_top, Variant.checkered_asymmetrical, {"directions": directs,
                                                                               "parts": (p_fill, p_dir)})

    @staticmethod
    def _3_doubles(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir_1: str, p_dir_2: str, direct: int,
                   *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, 7, True, 0, p_fill,
                             (p_dir_1, direct), (p_dir_1, direct+1), (p_dir_2, direct+2), (p_dir_2, direct+3))
        _blueprint(builder, layer, stack_top, Variant._3_doubles, {"direction": direct,
                                                                   "parts": (p_fill, p_dir_1, p_dir_2)})

    @staticmethod
    def pins(builder: ShapeBuilder, *, layer: int | None = -1):
        part = ""
        for i in range(0, 12, 2):
            part += "P-" if builder.shape[0][i] != "-" else "--"
        builder.shape.insert(0, part)
        _blueprint(builder, layer, False, Variant.pins, {})

    @staticmethod
    def full_crystal(builder: ShapeBuilder, part: str, *, layer: int | None = -1, force_fill: bool | None = None):
        if force_fill is not False and (force_fill or builder.has_crystals or
                                        Processor.ROTATOR not in builder or Processor.CUTTER not in builder):
            fill_crystal(builder, part[1])
        builder.shape.insert(0, part * 6)
        builder.has_crystals = True
        _blueprint(builder, layer, False, Variant.full_crystal, {"part": part})

    @staticmethod
    def half_crystal(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                     *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 0),
                             False, 1, "--", (part, direct), (part, direct+1), (part, direct+2))
        _blueprint(builder, layer, stack_top, Variant.half_crystal, {"direction": direct, "part": part})

    @staticmethod
    def half_half_crystal(rand: Random, builder: ShapeBuilder, part_fill: str, part_dir: str, direct: int,
                          *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 0),
                             False, 2, part_fill, (part_dir, direct), (part_dir, direct+1), (part_dir, direct+2))
        _blueprint(builder, layer, stack_top, Variant.half_half_crystal, {"direction": direct,
                                                                          "parts": (part_fill, part_dir)})

    @staticmethod
    def half_crystal_half_shape(rand: Random, builder: ShapeBuilder, part_fill: str, part_dir: str, direct: int,
                                *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 0),
                             True, 1, part_fill, (part_dir, direct), (part_dir, direct+1), (part_dir, direct+2))
        _blueprint(builder, layer, stack_top, Variant.half_crystal_half_shape, {"direction": direct,
                                                                                "parts": (part_fill, part_dir)})

    @staticmethod
    def cut_out_5_crystal(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                          *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 1),
                             False, 1, part, ("--", direct))
        _blueprint(builder, layer, stack_top, Variant.cut_out_5_crystal, {"direction": direct, "part": part})

    @staticmethod
    def cut_out_4_crystal(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                          *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, -1),
                             False, 1, part, ("--", direct), ("--", direct+1))
        _blueprint(builder, layer, stack_top, Variant.cut_out_4_crystal, {"direction": direct, "part": part})

    @staticmethod
    def _5_1_crystals(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                      *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 1),
                             False, 2, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant._5_1_crystals, {"direction": direct, "parts": (p_fill, p_dir)})

    @staticmethod
    def _4_2_crystals(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                      *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, -1),
                             False, 2, p_fill, (p_dir, direct), (p_dir, direct+1))
        _blueprint(builder, layer, stack_top, Variant._4_2_crystals, {"direction": direct, "parts": (p_fill, p_dir)})

    @staticmethod
    def _5_crystals_1_shape(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                            *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 1),
                             True, 1, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant._5_crystals_1_shape, {"direction": direct,
                                                                            "parts": (p_fill, p_dir)})

    @staticmethod
    def _5_shapes_1_crystal(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                            *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 1),
                             True, 1, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant._5_shapes_1_crystal, {"direction": direct,
                                                                            "parts": (p_fill, p_dir)})

    @staticmethod
    def _4_crystals_2_shape(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                            *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, -1),
                             True, 1, p_fill, (p_dir, direct), (p_dir, direct+1))
        _blueprint(builder, layer, stack_top, Variant._4_crystals_2_shape, {"direction": direct,
                                                                            "parts": (p_fill, p_dir)})

    @staticmethod
    def _4_shapes_2_crystal(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                            *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, -1),
                             True, 1, p_fill, (p_dir, direct), (p_dir, direct+1))
        _blueprint(builder, layer, stack_top, Variant._4_shapes_2_crystal, {"direction": direct,
                                                                            "parts": (p_fill, p_dir)})

    @staticmethod
    def cornered_crystal(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                         *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, +1),
                             False, 1, "--", (part, direct))
        _blueprint(builder, layer, stack_top, Variant.cornered_crystal, {"direction": direct, "part": part})

    @staticmethod
    def cornered_2_crystal(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                           *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, -1),
                             False, 1, "--", (part, direct), (part, direct + 1))
        _blueprint(builder, layer, stack_top, Variant.cornered_2_crystal, {"direction": direct, "part": part})

    @staticmethod
    def cornered_atomic_crystal(rand: Random, builder: ShapeBuilder, part: str, direct: int,
                                *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 2, 7,
                             False, 1, "--", (part, direct))
        _blueprint(builder, layer, stack_top, Variant.cornered_atomic_crystal, {"direction": direct, "part": part})

    @staticmethod
    def cornered_asymmetrical_crystal(rand: Random, builder: ShapeBuilder, part_1: str, part_2: str, direct: int,
                                      *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, 7, False, 2, "--",
                             (part_1, direct), (part_1, direct + 2), (part_2, direct - 1), (part_2, direct + 3))
        _blueprint(builder, layer, stack_top, Variant.cornered_asymmetrical_crystal, {"direction": direct,
                                                                                      "parts": (part_1, part_2)})

    @staticmethod
    def checkered_crystal(rand: Random, builder: ShapeBuilder, parts: Sequence[str],
                          *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = stack(rand, builder, "".join(parts) * 2, False, 3, blueprint=stack_top)
        builder.splits |= 7
        _blueprint(builder, layer, stack_top, Variant.checkered_crystal, {"parts": parts})

    @staticmethod
    def checkered_2x_crystal_shape(rand: Random, builder: ShapeBuilder, p_shape: str, p_crys_1: str, p_crys_2: str,
                                   direct: int, *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, 7,
                             True, 2, "--", (p_shape, direct), (p_crys_1, direct + 1), (p_crys_2, direct + 2))
        _blueprint(builder, layer, stack_top, Variant.checkered_2x_crystal_shape,
                   {"direction": direct, "parts": (p_shape, p_crys_1, p_crys_2)})

    @staticmethod
    def checkered_2x_shape_crystal(rand: Random, builder: ShapeBuilder, p_crys: str, p_shape_1: str, p_shape_2: str,
                                   direct: int, *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, 7,
                             True, 1, "--", (p_crys, direct), (p_shape_1, direct + 1), (p_shape_2, direct + 2))
        _blueprint(builder, layer, stack_top, Variant.checkered_2x_shape_crystal,
                   {"direction": direct, "parts": (p_crys, p_shape_1, p_shape_2)})

    @staticmethod
    def checkered_2_1_crystal(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                              *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, 1),
                             False, 2, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant.checkered_2_1_crystal, {"direction": direct,
                                                                              "parts": (p_fill, p_dir)})

    @staticmethod
    def checkered_2_1_crystal_shape(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                                    *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, 1),
                             True, 1, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant.checkered_2_1_crystal_shape, {"direction": direct,
                                                                                    "parts": (p_fill, p_dir)})

    @staticmethod
    def checkered_2_1_shape_crystal(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir: str, direct: int,
                                    *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 3, (direct, 1),
                             True, 1, p_fill, (p_dir, direct))
        _blueprint(builder, layer, stack_top, Variant.checkered_2_1_shape_crystal, {"direction": direct,
                                                                                    "parts": (p_fill, p_dir)})

    @staticmethod
    def checkered_atomic_crystal(rand: Random, builder: ShapeBuilder, parts: Sequence[str],
                                 *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = stack(rand, builder, "".join(parts) * 3, False, 2, blueprint=stack_top)
        builder.splits |= 7
        _blueprint(builder, layer, stack_top, Variant.checkered_atomic_crystal, {"parts": parts})

    @staticmethod
    def checkered_atomic_crystal_shape(rand: Random, builder: ShapeBuilder, p_shape: str, p_crys: str, direct: int,
                                       *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 2, 7,
                             True, 1, p_shape, (p_crys, direct))
        _blueprint(builder, layer, stack_top, Variant.checkered_atomic_crystal_shape, {"direction": direct,
                                                                                       "parts": (p_shape, p_crys)})

    @staticmethod
    def _3_doubles_crystal(rand: Random, builder: ShapeBuilder, p_fill: str, p_dir_1: str, p_dir_2: str, direct: int,
                           *, layer: int | None = -1, stack_top: bool | None = None):
        stack_top = _ordered(rand, builder, stack_top, 6, 7, False, 3, p_fill,
                             (p_dir_1, direct), (p_dir_1, direct+1), (p_dir_2, direct+2), (p_dir_2, direct+3))
        _blueprint(builder, layer, stack_top, Variant._3_doubles_crystal, {"direction": direct,
                                                                           "parts": (p_fill, p_dir_1, p_dir_2)})

    @staticmethod
    def single(rand: Random, builder: ShapeBuilder, part: str, direct: int,
               *, layer: int | None = -1, stack_top: bool | None = None):
        a = (False, 1) if part[0] == "c" else (True, 0)
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, 1),
                             a[0], a[1], "--", (part, direct))
        _blueprint(builder, layer, stack_top, Variant.single, {"direction": direct, "part": part})

    @staticmethod
    def double(rand: Random, builder: ShapeBuilder, part: str, direct: int,
               *, layer: int | None = -1, stack_top: bool | None = None):
        a = (False, 1) if part[0] == "c" else (True, 0)
        stack_top = _ordered(rand, builder, stack_top, 6, (direct, -1),
                             a[0], a[1], "--", (part, direct), (part, direct+1))
        _blueprint(builder, layer, stack_top, Variant.double, {"direction": direct, "part": part})

    @staticmethod
    def _2_singles(rand: Random, builder: ShapeBuilder, has_non_crys: bool, crys_col: int, parts: Sequence[str],
                   directs: Sequence[int], subv: int, *, layer: int | None = -1, stack_top: bool | None = None):
        # parts is shape-shape, shape-crystal, or crystal-crystal
        stack_top = _ordered(rand, builder, stack_top, 6, (directs[0], 1),
                             has_non_crys, crys_col, "--", (parts[0], directs[0]), (parts[1], directs[1]))
        builder.splits |= 1 << (directs[1] % 3) | 1 << ((directs[1] + 1) % 3)  # splits of directs[0] in _ordered
        _blueprint(builder, layer, stack_top, Variant._2_singles, {"directions": directs, "parts": parts,
                                                                   "subvariant": subv})

    @staticmethod
    def _2_doubles(rand: Random, builder: ShapeBuilder, has_non_crys: bool, crys_col: int, parts: Sequence[str],
                   directs: Sequence[int], subv: int, *, layer: int | None = -1, stack_top: bool | None = None):
        # parts is shape-shape, shape-crystal, or crystal-crystal
        stack_top = _ordered(rand, builder, stack_top, 6, (directs[0], -1), has_non_crys, crys_col, "--",
                             (parts[0], directs[0]), (parts[0], directs[0]+1),
                             (parts[1], directs[1]), (parts[1], directs[1]+1))
        builder.splits |= 1 << (directs[1] % 3) | 1 << ((directs[1] - 1) % 3)  # splits of directs[0] in _ordered
        _blueprint(builder, layer, stack_top, Variant._2_doubles, {"directions": directs, "parts": parts,
                                                                   "subvariant": subv})

    @staticmethod
    def _5_singles(rand: Random, builder: ShapeBuilder, has_non_crys: bool, crys_col: int, parts: Sequence[str],
                   direct: int, reverse: bool, subv: int, *, layer: int | None = -1, stack_top: bool | None = None):
        ordered = ["--"] * 6
        if reverse:
            parts = tuple(reversed(parts))
        for i in range(5):
            ordered[(direct+i) % 6] = parts[i]
        stack_top = stack(rand, builder, "".join(ordered), has_non_crys, crys_col, blueprint=stack_top)
        builder.splits |= 7
        _blueprint(builder, layer, stack_top, Variant._5_singles, {"direction": direct, "parts": parts,
                                                                   "subvariant": subv})

    @staticmethod
    def _6_singles(rand: Random, builder: ShapeBuilder, has_non_crys: bool, crys_col: int, parts: Sequence[str],
                   direct: int, reverse: bool, subv: int, *, layer: int | None = -1, stack_top: bool | None = None):
        ordered = ["--"] * 6
        if reverse:
            parts = tuple(reversed(parts))
        for i in range(6):
            ordered[(direct+i) % 6] = parts[i]
        stack_top = stack(rand, builder, "".join(ordered), has_non_crys, crys_col, blueprint=stack_top)
        builder.splits |= 7
        _blueprint(builder, layer, stack_top, Variant._6_singles, {"direction": direct, "parts": parts,
                                                                   "subvariant": subv})
