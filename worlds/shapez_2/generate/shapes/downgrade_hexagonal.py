
from random import Random
from typing import Iterable, Sequence

from . import Processor, ShapeBuilder


def downgrade_6(rand: Random, builder: ShapeBuilder, remaining_processors: list[Processor],
                missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    from .generate_hexagonal import Variant, generate_shape
    from .layers_hexagonal import Layers

    if missing_processor == Processor.STACKER:
        processed_layers = 0
        non_pin_layers = 0
        for ltup in builder.blueprint:
            non_pin_layers += 1 if ltup[0] != Variant.pins else 0
            processed_layers += 1 if ltup[0] not in (Variant.pins, Variant.full) else 0
            processed_layers += 1 if ltup[0] == Variant.full and ltup[2]["part"][1] != "u" else 0
        if processed_layers > 1:
            shape_pool, crystal_pool = [], []
            for layer in builder.shape:
                for i in range(0, 12, 2):
                    if layer[i] == "c" and layer[i+1] not in crystal_pool:
                        crystal_pool.append(layer[i+1])
                    elif layer[i] in "HFG" and layer[i:i+2] not in shape_pool:
                        shape_pool.append(layer[i:i+2])
            from .generator import generate_new
            return generate_new(rand, remaining_processors, original_complexity, True, len(builder.blueprint),
                                regen_pools=(shape_pool, crystal_pool))
        elif processed_layers == 0:
            top_layer = builder.blueprint[0]
            builder.blueprint = list(_ltup for _ltup in builder.blueprint[1:] if _ltup[0] != Variant.full)
            builder.blueprint.insert(0, top_layer)
        else:
            builder.blueprint = list(_ltup for _ltup in builder.blueprint
                                     if _ltup[0] != Variant.full or _ltup[2]["part"][1] != "u")
            while builder.blueprint[0][0] == Variant.pins:
                builder.blueprint.pop(0)

    builder.shape = []
    builder.has_crystals = False
    builder.splits = 0
    mixer_replacements = None if missing_processor != Processor.MIXER else {
        "u": "u",
        "r": "r",
        "g": "g",
        "b": "b",
        "y": rand.choice("rg"),
        "c": rand.choice("bg"),
        "m": rand.choice("rb"),
        "w": rand.choice("rgb"),
        "-": "-",
    }
    crystal_replacement = {
        "r": generate_shape(rand),
        "g": generate_shape(rand),
        "b": generate_shape(rand),
        "y": generate_shape(rand),
        "c": generate_shape(rand),
        "m": generate_shape(rand),
        "w": generate_shape(rand),
    }

    def _unpaint(parts: Iterable[str]) -> Sequence[str]:
        parts = tuple(_p[0] + ("u" if _p[0] in "HFG" else _p[1]) for _p in parts)
        if all(parts[i] == parts[(i+1)%len(parts)] for i in range(len(parts))) and parts[0][0] != "c":
            parts = (generate_shape(rand, parts[0][0])+"u", *parts[1:])
        return parts

    def _unmix(parts: Iterable[str]) -> Sequence[str]:
        # Assumes this only gets called when missing_processor == Processor.MIXER
        parts = tuple(_p[0] + mixer_replacements[_p[1]] for _p in parts)
        if all(parts[i] == parts[(i+1)%len(parts)] for i in range(len(parts))) and parts[0][1] != "u":
            parts = (parts[0][0]+rand.choice("rgb".replace(parts[0][1], "")), *parts[1:])
        return parts

    def _decrystallize_all(parts: Iterable[str]) -> Sequence[str]:
        _has_painter = Processor.PAINTER in remaining_processors
        return tuple((_p if _p[0] != "c" else (crystal_replacement[_p[1]] + ("u" if not _has_painter else _p[1])))
                     for _p in parts)

    def _decrystallize_one(_part: str) -> str:
        return crystal_replacement[_part[1]] + ("u" if not Processor.PAINTER in remaining_processors else _part[1])

    def _new_part_from_shape(_part: str) -> str:
        _s = generate_shape(rand, _part[0])
        if Processor.PAINTER in remaining_processors:
            return _s + rand.choice(["r", "b", "g", _part[1]])
        else:
            return _s + "u"

    for layer_index in range(len(builder.blueprint)):
        for layer in builder.shape:
            if len(layer) != 12:
                raise Exception(f"Invalid layer length:\n{builder.debug_string()}")
        variant, stack_top, data = builder.blueprint[layer_index]
        has_fillable = any(layer[i] == "-" for layer in builder.shape for i in range(0, 12, 2))

        match variant:
            case Variant.full:
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                Layers.full(rand, builder, data["part"], layer=None, stack_top=stack_top)
            case Variant.half:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    Layers.full(rand, builder, data["part"], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    data["direction"] = 0
                    leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.half(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant.half_half:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if Processor.ROTATOR in remaining_processors:
                        p1, p2 = data["parts"]
                        Layers.checkered_2_1(rand, builder, p1, p2, data["direction"],
                                             layer=layer_index, stack_top=stack_top)
                    else:
                        leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        if data["direction"] % 6 == 0:
                            part = data["parts"][1]
                        elif data["direction"] % 6 == 3:
                            part = data["parts"][0]
                        else:
                            part = rand.choice(data["parts"])
                        Layers.half(rand, builder, part, 0, layer=layer_index, stack_top=stack_top)
                    else:
                        data["direction"] = (data["direction"] // 3) * 3
                        leave_as_is = True
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.ROTATOR in remaining_processors and
                                                                         not has_fillable):
                        if builder.splits:
                            if builder.splits & (7 - (1 << (data["direction"] % 3))):
                                Layers.half(rand, builder, data["parts"][1], data["direction"],
                                            layer=layer_index, stack_top=stack_top)
                            else:
                                Layers.half(rand, builder, data["parts"][1], data["direction"]+1,
                                            layer=layer_index, stack_top=stack_top)
                        else:
                            picked = rand.randint(0, 1)
                            Layers.double(rand, builder, data["parts"][not picked], (data["direction"] + 3*picked)+1,
                                          layer=layer_index, stack_top=stack_top)
                    else:
                        leave_as_is = True
                elif missing_processor == Processor.SWAPPER:
                    if Processor.CUTTER not in remaining_processors:
                        Layers.full(rand, builder, rand.choice(data["parts"]), layer=layer_index, stack_top=stack_top)
                    elif Processor.ROTATOR not in remaining_processors:
                        if data["direction"] % 6 == 0:
                            part = data["parts"][1]
                        elif data["direction"] % 6 == 3:
                            part = data["parts"][0]
                        else:
                            part = rand.choice(data["parts"])
                        Layers.half(rand, builder, part, 0, layer=layer_index, stack_top=stack_top)
                    elif Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & (7 - (1 << (data["direction"] % 3))):
                            Layers.half(rand, builder, data["parts"][1], data["direction"],
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["parts"][1], data["direction"] + 1,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        picked = rand.randint(0, 1)
                        Layers.double(rand, builder, data["parts"][not picked], (data["direction"] + 3 * picked) + 1,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.half_half(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                     layer=None, stack_top=stack_top)
            case Variant.cut_out_5:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    Layers._5_1(rand, builder, data["part"], _new_part_from_shape(data["part"]), data["direction"],
                                layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["part"], _new_part_from_shape(data["part"]),
                                         (data["direction"] // 3) * 3, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, data["part"], 0, layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & (1 << ((data["direction"] + 1) % 3)):
                            Layers.half(rand, builder, data["part"], data["direction"]+2,
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["part"], data["direction"]+1,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.double(rand, builder, data["part"], data["direction"]+rand.randint(1, 4),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cut_out_5(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant.cut_out_4:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    Layers._4_2(rand, builder, data["part"], _new_part_from_shape(data["part"]), data["direction"],
                                layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["part"], _new_part_from_shape(data["part"]),
                                         (data["direction"] // 3) * 3, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, data["part"], 0, layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & (1 << ((data["direction"] + 2) % 3)):
                            Layers.half(rand, builder, data["part"], data["direction"]+3,
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["part"], data["direction"]+2,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.double(rand, builder, data["part"], data["direction"]+rand.randint(2, 4),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cut_out_4(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant._5_1:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        Layers.half(rand, builder, data["parts"][0], 0, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1],
                                         (data["direction"] // 3) * 3, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.CUTTER not in remaining_processors:
                        leave_as_is = True
                    elif Processor.SWAPPER in remaining_processors:
                        Layers.cut_out_5(rand, builder, data["parts"][0], data["direction"],
                                         layer=layer_index, stack_top=stack_top)
                    elif builder.splits:
                        if builder.splits & (1 << ((data["direction"] + 1) % 3)):
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 2,
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 1,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.single(rand, builder, data["parts"][1], data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & (1 << ((data["direction"] + 1) % 3)):
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 2,
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 1,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.single(rand, builder, data["parts"][1], data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._5_1(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                layer=None, stack_top=stack_top)
            case Variant._4_2:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        Layers.half(rand, builder, data["parts"][0], 0, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1],
                                         (data["direction"] // 3) * 3, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.CUTTER not in remaining_processors:
                        leave_as_is = True
                    elif Processor.SWAPPER in remaining_processors:
                        Layers.cut_out_4(rand, builder, data["parts"][0], data["direction"],
                                         layer=layer_index, stack_top=stack_top)
                    elif builder.splits:
                        if builder.splits & (1 << ((data["direction"] + 2) % 3)):
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 3,
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 2,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.double(rand, builder, data["parts"][1], data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & (1 << ((data["direction"] + 2) % 3)):
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 3,
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["parts"][0], data["direction"] + 2,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.double(rand, builder, data["parts"][1], data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._4_2(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                layer=None, stack_top=stack_top)
            case Variant.cornered:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    Layers.checkered_2_1(rand, builder, _new_part_from_shape(data["part"]), data["part"],
                                         data["direction"], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["part"], _new_part_from_shape(data["part"]),
                                         rand.choice((0, 3)), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, data["part"], 0, layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers.single(rand, builder, data["part"], data["direction"] + rand.choice((0, 3)),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant.cornered_2:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    Layers.checkered_2_1(rand, builder, data["part"], _new_part_from_shape(data["part"]),
                                         data["direction"] + 2, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["part"], _new_part_from_shape(data["part"]),
                                         rand.choice((0, 3)), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, data["part"], 0, layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers.double(rand, builder, data["part"], data["direction"] + rand.choice((0, 3)),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_2(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant.cornered_1_1:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    Layers.checkered_2_1(rand, builder, data["parts"][1], data["parts"][0],
                                         data["direction"], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1], 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, data["parts"][rand.randint(0, 1)], 0,
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        picked = rand.randint(0, 1)
                        Layers.single(rand, builder, data["parts"][picked],
                                      data["direction"] + picked + rand.choice((0, 3)),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_1_1(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                        layer=None, stack_top=stack_top)
            case Variant.cornered_atomic:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    ordered = [_new_part_from_shape(data["part"])] * 2
                    ordered[data["direction"] % 2] = data["part"]
                    Layers.checkered_atomic(rand, builder, ordered, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["part"], _new_part_from_shape(data["part"]),
                                         rand.choice((0, 3)), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, data["part"], 0, layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & (1 << ((data["direction"]) % 3)):
                            Layers.half(rand, builder, data["part"], data["direction"]+rand.choice((1, 2, 4, 5)),
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, data["part"], data["direction"]+rand.choice((0, 3)),
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.single(rand, builder, data["part"], data["direction"]+rand.choice((0, 2, 4)),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_atomic(rand, builder, data["part"], data["direction"],
                                           layer=None, stack_top=stack_top)
            case Variant.cornered_asymmetrical:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    Layers.checkered_asymmetrical(rand, builder, data["parts"][1], data["parts"][0],
                                                  (data["direction"], rand.choice((2, -1))),
                                                  layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["parts"][1], data["parts"][0],
                                         (data["direction"] // 3) * 3, layer=layer_index, stack_top=stack_top)
                    else:
                        picked = data["direction"] % 6 < 3
                        Layers.half(rand, builder, data["parts"][not picked], 0,
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & 7 == (1 << ((data["direction"]) % 3)):
                            Layers.half(rand, builder, data["parts"][rand.randint(0, 1)],
                                        data["direction"]+rand.choice((1, 2, 4, 5)),
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            picked = rand.randint(0, 1)
                            Layers.half(rand, builder, data["parts"][picked], data["direction"] + picked*3,
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        picked = rand.randint(0, 1)
                        Layers.double(rand, builder, data["parts"][picked],
                                      data["direction"] + rand.randint(0, 1) + picked*3,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_asymmetrical(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                                 layer=None, stack_top=stack_top)
            case Variant.checkered:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        Layers.half(rand, builder, rand.choice(data["parts"]), 0,
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        parts = list(data["parts"])
                        rand.shuffle(parts)
                        Layers.half_half(rand, builder, parts[0], parts[1], 0, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER not in remaining_processors:
                        picked = rand.randint(0, 5)
                        Layers.single(rand, builder, data["parts"][picked % 3], picked,
                                      layer=layer_index, stack_top=stack_top)
                    elif Processor.CUTTER in remaining_processors:
                        picked = rand.randint(0, 2)
                        Layers.cornered_1_1(rand, builder, data["parts"][picked], data["parts"][(picked+1)%3], picked,
                                            layer=layer_index, stack_top=stack_top)
                    else:
                        leave_as_is = True
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        picked = rand.randint(0, 5)
                        Layers.single(rand, builder, data["parts"][picked % 3], picked,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered(rand, builder, data["parts"], layer=None, stack_top=stack_top)
            case Variant.checkered_2_1:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        Layers.half(rand, builder, data["parts"][0], 0, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1], rand.choice((0, 3)),
                                         layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER not in remaining_processors:
                        Layers.double(rand, builder, data["parts"][0], data["direction"] + 1 + rand.choice((0, 3)),
                                      layer=layer_index, stack_top=stack_top)
                    elif Processor.CUTTER in remaining_processors:
                        Layers.cornered_2(rand, builder, data["parts"][0], data["direction"] + 1,
                                          layer=layer_index, stack_top=stack_top)
                    else:
                        leave_as_is = True
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers.double(rand, builder, data["parts"][0], data["direction"] + 1 + rand.choice((0, 3)),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_2_1(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                         layer=None, stack_top=stack_top)
            case Variant.checkered_atomic:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        Layers.half(rand, builder, rand.choice(data["parts"]), 0,
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1], rand.choice((0, 3)),
                                         layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER not in remaining_processors:
                        if builder.splits:
                            if builder.splits & 1:
                                Layers.half(rand, builder, rand.choice(data["parts"]), rand.choice((1, 2, 4, 5)),
                                            layer=layer_index, stack_top=stack_top)
                            else:
                                Layers.half(rand, builder, rand.choice(data["parts"]), rand.choice((0, 3)),
                                            layer=layer_index, stack_top=stack_top)
                        else:
                            picked = rand.randint(0, 5)
                            Layers.single(rand, builder, data["parts"][picked % 6], picked,
                                          layer=layer_index, stack_top=stack_top)
                    elif Processor.CUTTER in remaining_processors:
                        picked = rand.randint(0, 1)
                        Layers.cornered_atomic(rand, builder, data["parts"][picked], picked,
                                               layer=layer_index, stack_top=stack_top)
                    else:
                        leave_as_is = True
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    elif builder.splits:
                        if builder.splits & 1:
                            Layers.half(rand, builder, rand.choice(data["parts"]), rand.choice((1, 2, 4, 5)),
                                        layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.half(rand, builder, rand.choice(data["parts"]), rand.choice((0, 3)),
                                        layer=layer_index, stack_top=stack_top)
                    else:
                        picked = rand.randint(0, 5)
                        Layers.single(rand, builder, data["parts"][picked % 6], picked,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_atomic(rand, builder, data["parts"], layer=None, stack_top=stack_top)
            case Variant.checkered_asymmetrical:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        Layers.half(rand, builder, rand.choice(data["parts"]), 0,
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1], rand.choice((0, 3)),
                                         layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER not in remaining_processors:
                        picked = rand.randint(0, 1)
                        Layers.double(rand, builder, data["parts"][not picked], sum(data["directions"]) + picked * 2,
                                      layer=layer_index, stack_top=stack_top)
                    elif Processor.CUTTER in remaining_processors:
                        Layers.cornered_asymmetrical(rand, builder, data["parts"][1], data["parts"][0],
                                                     sum(data["directions"]), layer=layer_index, stack_top=stack_top)
                    else:
                        leave_as_is = True
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        picked = rand.randint(0, 1)
                        Layers.double(rand, builder, data["parts"][not picked], sum(data["directions"]) + picked * 2,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_asymmetrical(rand, builder, data["parts"][0], data["parts"][1], data["directions"],
                                                  layer=None, stack_top=stack_top)
            case Variant._3_doubles:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                         Processor.STACKER in remaining_processors and
                                                                         not has_fillable):
                        Layers.half(rand, builder, data["parts"][(1-(data["direction"]//2))%3], 0,
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_half(rand, builder, data["parts"][(-((data["direction"]+1)//2))%3],
                                         data["parts"][(1-(data["direction"]//2))%3], 0,
                                         layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER not in remaining_processors:
                        picked = rand.randint(0, 2)
                        Layers.double(rand, builder, data["parts"][picked], data["direction"] + (picked - 1) * 2,
                                      layer=layer_index, stack_top=stack_top)
                    elif Processor.CUTTER in remaining_processors:
                        picked = rand.randint(0, 2)
                        Layers._2_doubles(rand, builder, True, 0, (data["parts"][picked], data["parts"][(picked+1)%3]),
                                          (data["direction"]-2+picked*2, data["direction"]+picked*2), 0,
                                          layer=layer_index, stack_top=stack_top)
                    else:
                        leave_as_is = True
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        picked = rand.randint(0, 2)
                        Layers.double(rand, builder, data["parts"][picked], data["direction"] + (picked - 1) * 2,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._3_doubles(rand, builder, data["parts"][0], data["parts"][1], data["parts"][2],
                                      data["direction"], layer=None, stack_top=stack_top)
            case Variant.pins:
                if missing_processor == Processor.PIN_PUSHER:
                    builder.blueprint[layer_index] = (Variant._remove, False, {})
                else:
                    Layers.pins(builder, layer=None)
            case Variant.full_crystal:
                leave_as_is = False
                force_fill = None
                if missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    leave_as_is = True
                    force_fill = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.CUTTER not in remaining_processors or (Processor.PIN_PUSHER in remaining_processors
                                                                        and builder.has_crystals):
                        leave_as_is = True
                        force_fill = True
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                       layer=layer_index, stack_top=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if Processor.PIN_PUSHER not in remaining_processors or (Processor.CUTTER in remaining_processors and
                                                                            Processor.ROTATOR in remaining_processors
                                                                            and not has_fillable) or not builder.shape:
                        Layers.double(rand, builder, _decrystallize_one(data["part"]), rand.randint(0, 5),
                                      layer=layer_index, stack_top=False)
                    else:
                        Layers.pins(builder, layer=layer_index)
                elif missing_processor == Processor.PIN_PUSHER:
                    if Processor.ROTATOR in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                       layer=layer_index, stack_top=False)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.full_crystal(builder, data["part"], layer=None, force_fill=force_fill)
            case Variant.half_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not builder.shape:
                        decrys = _decrystallize_one(data["part"])
                        Layers._4_2(rand, builder, decrys, _new_part_from_shape(decrys),
                                    data["direction"] + rand.randint(3, 4), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if builder.splits & (7 - (1 << (data["direction"] % 3))):
                        Layers.half(rand, builder, _decrystallize_one(data["part"]), data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                    elif builder.splits:
                        Layers.half(rand, builder, _decrystallize_one(data["part"]),
                                    data["direction"] + rand.choice((1, 2, 4, 5)),
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.double(rand, builder, _decrystallize_one(data["part"]),
                                      data["direction"] + rand.choice((0, 1)), layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.half_crystal(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant.half_half_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not builder.shape:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._3_doubles(rand, builder, _new_part_from_shape(decryss[0]), decryss[0], decryss[1],
                                    data["direction"] + rand.randint(0, 1), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["parts"][0],
                                                   _decrystallize_one(data["parts"][1]), 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if builder.splits & (7 - (1 << (data["direction"] % 3))):
                        picked = rand.randint(0, 1)
                        Layers.half(rand, builder, _decrystallize_one(data["parts"][not picked]),
                                    data["direction"] + picked*3, layer=layer_index, stack_top=stack_top)
                    elif builder.splits:
                        Layers.half(rand, builder, _decrystallize_one(rand.choice(data["parts"])),
                                    data["direction"] + rand.choice((1, 2, 4, 5)),
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        picked = rand.randint(0, 1)
                        Layers.double(rand, builder, _decrystallize_one(data["parts"][not picked]),
                                      data["direction"] + picked*3 + rand.choice((0, 1)),
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.half_half_crystal(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                             layer=None, stack_top=stack_top)
            case Variant.half_crystal_half_shape:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=True)
                    elif Processor.ROTATOR in remaining_processors:
                        parts = (*_decrystallize_all(data["parts"]), _new_part_from_shape(data["parts"][1]))
                        Layers.checkered(rand, builder, parts,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full(rand, builder, data["parts"][1], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    data["direction"] = 0
                    leave_as_is = True
                elif missing_processor == Processor.CRYSTALLIZER:
                    if (
                        Processor.ROTATOR in remaining_processors and Processor.STACKER in remaining_processors and
                        Processor.SWAPPER not in remaining_processors
                    ):
                        Layers.half_half(rand, builder, _decrystallize_one(data["parts"][0]), data["parts"][1],
                                         data["direction"], layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, data["parts"][1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.half_crystal_half_shape(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                                   layer=None, stack_top=stack_top)
            case Variant.cut_out_5_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                    else:
                        decrys = _decrystallize_one(data["part"])
                        Layers._5_1(rand, builder, decrys, _new_part_from_shape(decrys), data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if builder.shape:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                    else:
                        Layers._5_crystals_1_shape(rand, builder, data["part"], _decrystallize_one(data["part"]),
                                                   data["direction"], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cut_out_5(rand, builder, _decrystallize_one(data["part"]), data["direction"],
                                     layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cut_out_5_crystal(rand, builder, data["part"], data["direction"],
                                             layer=None, stack_top=stack_top)
            case Variant.cut_out_4_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                    else:
                        decrys = _decrystallize_one(data["part"])
                        Layers._4_2(rand, builder, decrys, _new_part_from_shape(decrys), data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if builder.shape:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                    else:
                        Layers._4_crystals_2_shape(rand, builder, data["part"], _decrystallize_one(data["part"]),
                                                   data["direction"], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cut_out_4(rand, builder, _decrystallize_one(data["part"]), data["direction"],
                                     layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cut_out_4_crystal(rand, builder, data["part"], data["direction"],
                                             layer=None, stack_top=stack_top)
            case Variant._5_1_crystals:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._5_1(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["parts"][0],
                                                   _decrystallize_one(data["parts"][1]), 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if Processor.SWAPPER in remaining_processors:
                        Layers.cut_out_5(rand, builder, _decrystallize_one(data["parts"][0]), data["direction"],
                                         layer=layer_index, stack_top=stack_top)
                    elif Processor.STACKER in remaining_processors:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._5_1(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.single(rand, builder, _decrystallize_one(data["parts"][1]), data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._5_1_crystals(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                         layer=None, stack_top=stack_top)
            case Variant._4_2_crystals:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._4_2(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["parts"][0],
                                                   _decrystallize_one(data["parts"][1]), 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if Processor.SWAPPER in remaining_processors:
                        Layers.cut_out_4(rand, builder, _decrystallize_one(data["parts"][0]), data["direction"],
                                         layer=layer_index, stack_top=stack_top)
                    elif Processor.STACKER in remaining_processors:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._4_2(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.double(rand, builder, _decrystallize_one(data["parts"][1]), data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._4_2_crystals(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                         layer=None, stack_top=stack_top)
            case Variant._5_crystals_1_shape:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._5_1(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["parts"][0], data["parts"][1], 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if Processor.STACKER in remaining_processors and Processor.SWAPPER not in remaining_processors:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._5_1(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.single(rand, builder, data["parts"][1], data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._5_crystals_1_shape(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                               layer=None, stack_top=stack_top)
            case Variant._5_shapes_1_crystal:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][1], layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._5_1(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals and Processor.SWAPPER in remaining_processors:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.half_half(rand, builder, decryss[0], decryss[1], (data["direction"] // 3) * 3,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][1], data["parts"][0], 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers._5_crystals_1_shape(rand, builder, data["parts"][1], data["parts"][0], data["direction"],
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cut_out_5(rand, builder, data["parts"][0], data["direction"],
                                     layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._5_shapes_1_crystal(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                               layer=None, stack_top=stack_top)
            case Variant._4_crystals_2_shape:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._4_2(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    Layers.half_crystal_half_shape(rand, builder, data["parts"][0], data["parts"][1], 0,
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if Processor.STACKER in remaining_processors and Processor.SWAPPER not in remaining_processors:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._4_2(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.double(rand, builder, data["parts"][1], data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._4_crystals_2_shape(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                               layer=None, stack_top=stack_top)
            case Variant._4_shapes_2_crystal:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][1], layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._4_2(rand, builder, decryss[0], decryss[1], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals and Processor.SWAPPER in remaining_processors:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.half_half(rand, builder, decryss[0], decryss[1], (data["direction"] // 3) * 3,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][1], data["parts"][0], 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers._4_crystals_2_shape(rand, builder, data["parts"][1], data["parts"][0], data["direction"],
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cut_out_4(rand, builder, data["parts"][0], data["direction"],
                                     layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._4_shapes_2_crystal(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                               layer=None, stack_top=stack_top)
            case Variant.cornered_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                    else:
                        decrys = _decrystallize_one(data["part"])
                        Layers.checkered_2_1(rand, builder, _new_part_from_shape(decrys), decrys, data["direction"],
                                             layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decrys = _decrystallize_one(data["part"])
                        Layers.half_half(rand, builder, _new_part_from_shape(decrys), decrys, 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        Layers.checkered_2_1_shape_crystal(rand, builder, _decrystallize_one(data["part"]),
                                                           data["part"], data["direction"],
                                                           layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered(rand, builder, _decrystallize_one(data["part"]), data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_crystal(rand, builder, data["part"], data["direction"],
                                            layer=None, stack_top=stack_top)
            case Variant.cornered_2_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                    else:
                        decrys = _decrystallize_one(data["part"])
                        Layers.checkered_2_1(rand, builder, decrys, _new_part_from_shape(decrys), data["direction"] + 1,
                                             layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decrys = _decrystallize_one(data["part"])
                        Layers.half_half(rand, builder, _new_part_from_shape(decrys), decrys, 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        Layers.checkered_2_1_crystal_shape(rand, builder, data["part"],
                                                           _decrystallize_one(data["part"]), data["direction"] + 1,
                                                           layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered_2(rand, builder, _decrystallize_one(data["part"]), data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_2_crystal(rand, builder, data["part"], data["direction"],
                                              layer=None, stack_top=stack_top)
            case Variant.cornered_atomic_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                    else:
                        decrys = _decrystallize_one(data["part"])
                        ordered = [_new_part_from_shape(decrys)] * 2
                        ordered[data["direction"]] = decrys
                        Layers.checkered_atomic(rand, builder, ordered, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decrys = _decrystallize_one(data["part"])
                        Layers.half_half(rand, builder, _new_part_from_shape(decrys), decrys, 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        Layers.checkered_atomic_crystal_shape(rand, builder, _decrystallize_one(data["part"]),
                                                              data["part"], data["direction"],
                                                              layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered_atomic(rand, builder, _decrystallize_one(data["part"]), data["direction"],
                                           layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_atomic_crystal(rand, builder, data["part"], data["direction"],
                                                   layer=None, stack_top=stack_top)
            case Variant.cornered_asymmetrical_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=True)
                    else:
                        Layers.checkered_asymmetrical(rand, builder, data["parts"][0], data["parts"][1],
                                                      (data["direction"], rand.choice((2, -1))),
                                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.half_half(rand, builder, decryss[0], decryss[1], (data["direction"] // 3) * 3,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        picked = (data["direction"] % 6) // 3
                        decrys = _decrystallize_one(data["parts"][picked])
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][not picked], decrys, 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    decryss = _decrystallize_all(data["parts"])
                    Layers.cornered_asymmetrical(rand, builder, decryss[0], decryss[1], data["direction"],
                                                 layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.cornered_asymmetrical_crystal(rand, builder, data["parts"][0], data["parts"][1],
                                                         data["direction"], layer=None, stack_top=stack_top)
            case Variant.checkered_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=True)
                    else:
                        Layers.checkered(rand, builder, _decrystallize_all(data["parts"]),
                                         layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.half_half(rand, builder, decryss[0], decryss[1], 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][1],
                                                       _decrystallize_one(data["parts"][0]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        picked = rand.randint(0, 2)
                        decryss = _decrystallize_all(data["parts"])
                        Layers.checkered_2x_shape_crystal(rand, builder, data["parts"][picked], decryss[(picked+1)%3],
                                                          decryss[(picked+2)%3], picked,
                                                          layer=layer_index, stack_top=stack_top)
                    else:
                        parts = rand.choices(data["parts"], k=2)
                        Layers.half_half_crystal(rand, builder, parts[0], parts[1], rand.randint(0, 2),
                                                 layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    picked = rand.randint(0, 2)
                    decryss = _decrystallize_all(data["parts"])
                    Layers.cornered_1_1(rand, builder, decryss[picked], decryss[(picked+1)%3], picked,
                                        layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_crystal(rand, builder, data["parts"], layer=None, stack_top=stack_top)
            case Variant.checkered_2x_crystal_shape:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, rand.choice(data["parts"][1:]), layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        direct = data["direction"] % 3
                        Layers.checkered(rand, builder, (*decryss[3-direct:], *decryss[:3-direct]),
                                         layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        Layers.half_half(rand, builder, data["parts"][0],
                                         _decrystallize_one(rand.choice(data["parts"][1:])), rand.choice((0, 3)),
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, rand.choice(data["parts"][1:]), data["parts"][0],
                                                       0, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        Layers.checkered_2_1_crystal_shape(rand, builder, rand.choice(data["parts"][1:]),
                                                           data["parts"][0], data["direction"],
                                                           layer=layer_index, stack_top=stack_top)
                    else:
                        Layers._5_crystals_1_shape(rand, builder, rand.choice(data["parts"][1:]), data["parts"][0],
                                                   data["direction"]+rand.choice((0, 3)),
                                                   layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered(rand, builder, data["parts"][0], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_2x_crystal_shape(rand, builder, data["parts"][0], data["parts"][1],
                                                      data["parts"][2], data["direction"],
                                                      layer=None, stack_top=stack_top)
            case Variant.checkered_2x_shape_crystal:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        direct = data["direction"] % 3
                        Layers.checkered(rand, builder, (*decryss[3-direct:], *decryss[:3-direct]),
                                         layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals and Processor.SWAPPER in remaining_processors:
                        Layers.half_half(rand, builder, data["parts"][1], data["parts"][2], rand.choice((0, 3)),
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][0], rand.choice(data["parts"][1:]),
                                                       0, layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered_1_1(rand, builder, data["parts"][1], data["parts"][2], data["direction"] + 1,
                                        layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_2x_shape_crystal(rand, builder, data["parts"][0], data["parts"][1],
                                                      data["parts"][2], data["direction"],
                                                      layer=None, stack_top=stack_top)
            case Variant.checkered_2_1_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.checkered_2_1(rand, builder, decryss[0], decryss[1], data["direction"],
                                             layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.half_half(rand, builder, decryss[0], decryss[1], rand.choice((0, 3)),
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        picked = rand.choice((0, 1))
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][picked],
                                                       _decrystallize_one(data["parts"][not picked]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        Layers.checkered_2_1_crystal_shape(rand, builder, data["parts"][0],
                                                           _decrystallize_one(data["parts"][1]),
                                                           data["direction"], layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered_2(rand, builder, _decrystallize_one(data["parts"][1]), data["direction"] + 1,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_2_1_crystal(rand, builder, data["parts"][0], data["parts"][1], data["direction"],
                                                 layer=None, stack_top=stack_top)
            case Variant.checkered_2_1_crystal_shape:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=True)
                    else:
                        Layers.checkered_2_1(rand, builder, _decrystallize_one(data["parts"][0]), data["parts"][1],
                                             data["direction"], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals and Processor.SWAPPER in remaining_processors:
                        Layers.half_half(rand, builder, _decrystallize_one(data["parts"][0]), data["parts"][1],
                                         rand.choice((0, 3)), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][0], data["parts"][1], 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers.full_crystal(builder, data["parts"][0], layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered_2(rand, builder, data["parts"][1], data["direction"],
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_2_1_crystal_shape(rand, builder, data["parts"][0], data["parts"][1],
                                                       data["direction"], layer=None, stack_top=stack_top)
            case Variant.checkered_2_1_shape_crystal:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][1], layer=layer_index, force_fill=True)
                    else:
                        Layers.checkered_2_1(rand, builder, data["parts"][0], _decrystallize_one(data["parts"][1]),
                                             data["direction"], layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals and Processor.SWAPPER in remaining_processors:
                        Layers.half_half(rand, builder, _decrystallize_one(data["parts"][1]), data["parts"][0],
                                         rand.choice((0, 3)), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][1], data["parts"][0], 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers.full_crystal(builder, data["parts"][1], layer=layer_index, force_fill=False)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered_2(rand, builder, data["parts"][0], data["direction"] + 1,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_2_1_shape_crystal(rand, builder, data["parts"][0], data["parts"][1],
                                                       data["direction"], layer=None, stack_top=stack_top)
            case Variant.checkered_atomic_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.checkered_atomic(rand, builder, decryss, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decryss = _decrystallize_all(data["parts"])
                        Layers.half_half(rand, builder, decryss[0], decryss[1], rand.choice((0, 3)),
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        picked = rand.choice((0, 1))
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][picked],
                                                       _decrystallize_one(data["parts"][not picked]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        picked = rand.choice((0, 1))
                        Layers.checkered_atomic_crystal_shape(rand, builder, _decrystallize_one(data["parts"][not picked]),
                                                              data["parts"][picked], picked, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_half_crystal(rand, builder, data["parts"][0], data["parts"][1], rand.randint(0, 5),
                                                 layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    picked = rand.choice((0, 1))
                    Layers.cornered_atomic(rand, builder, _decrystallize_one(data["parts"][picked]), picked,
                                           layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_atomic_crystal(rand, builder, data["parts"], layer=None, stack_top=stack_top)
            case Variant.checkered_atomic_crystal_shape:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, data["parts"][1], layer=layer_index, force_fill=True)
                    else:
                        ordered = [data["parts"][0]] * 2
                        ordered[data["direction"]] = _decrystallize_one(data["parts"][1])
                        Layers.checkered_atomic(rand, builder, ordered, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals and Processor.SWAPPER in remaining_processors:
                        Layers.half_half(rand, builder, _decrystallize_one(data["parts"][1]), data["parts"][0],
                                         rand.choice((0, 3)), layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][1], data["parts"][0], 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        Layers._4_crystals_2_shape(rand, builder, data["parts"][1], data["parts"][0],
                                                   rand.randint(0, 5),  layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    Layers.cornered_atomic(rand, builder, data["parts"][0], data["direction"] + 1,
                                           layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.checkered_atomic_crystal_shape(rand, builder, data["parts"][0], data["parts"][1],
                                                          data["direction"], layer=None, stack_top=stack_top)
            case Variant._3_doubles_crystal:
                leave_as_is = False
                if missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.shape and not builder.has_crystals:
                        Layers.full_crystal(builder, rand.choice(data["parts"]), layer=layer_index, force_fill=True)
                    else:
                        decryss = _decrystallize_all(data["parts"])
                        Layers._3_doubles(rand, builder, decryss[0], decryss[1], decryss[2], data["direction"],
                                          layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.ROTATOR:
                    if builder.has_crystals:
                        decryss = rand.choices(_decrystallize_all(data["parts"]), k=2)
                        Layers.half_half(rand, builder, decryss[0], decryss[1], 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["parts"][rand.choice((0, 2))],
                                                       _decrystallize_one(data["parts"][1]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    picked = rand.randint(0, 2)
                    Layers.half_half_crystal(rand, builder, data["parts"][picked-1], data["parts"][picked],
                                             data["direction"]-2+picked*2, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    pickedd = rand.choices((0, 1, 2), k=2)
                    decryss = _decrystallize_all(data["parts"])
                    Layers._2_doubles(rand, builder, True, 0, (decryss[pickedd[0]], decryss[pickedd[1]]),
                                      (data["direction"]-2+pickedd[0]*2, data["direction"]-2+pickedd[1]*2), 0,
                                      layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._3_doubles_crystal(rand, builder, data["parts"][0], data["parts"][1], data["parts"][2],
                                              data["direction"], layer=None, stack_top=stack_top)
            case Variant.single:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    if data["part"][0] != "c":
                        data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["part"][0] != "c" or builder.has_crystals or not builder.shape:
                        part = _decrystallize_one(data["part"]) if data["part"][0] == "c" else data["part"]
                        Layers._5_1(rand, builder, _new_part_from_shape(part), part, data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    if data["part"][0] != "c":
                        Layers.half(rand, builder, data["part"], 0, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if data["part"][0] == "c":
                        data["part"] = _decrystallize_one(data["part"])
                    leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.single(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant.double:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    if data["part"][0] != "c":
                        data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["part"][0] != "c" or builder.has_crystals or not builder.shape:
                        if data["part"][0] == "c":
                            data["part"] = _decrystallize_one(data["part"])
                        Layers._4_2(rand, builder, _new_part_from_shape(data["part"]), data["part"], data["direction"],
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, data["part"], layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    if data["part"][0] != "c":
                        Layers.half(rand, builder, data["part"], 0, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half_crystal_half_shape(rand, builder, data["part"], _decrystallize_one(data["part"]), 0,
                                                       layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if data["part"][0] == "c":
                        data["part"] = _decrystallize_one(data["part"])
                    leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers.double(rand, builder, data["part"], data["direction"], layer=None, stack_top=stack_top)
            case Variant._2_singles:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["subvariant"] <= 2 or builder.has_crystals or not builder.shape:
                        if data["subvariant"] != 1:
                            ordered = [data["parts"][0]] * 2
                            directs: Sequence[int] = data["directions"]
                            ordered[directs[1] % 2] = data["parts"][1]
                            Layers.checkered_atomic(rand, builder, ordered, layer=layer_index, stack_top=stack_top)
                        else:
                            Layers.checkered_asymmetrical(rand, builder, data["parts"][0], data["parts"][1],
                                                          (data["directions"][1], -1),
                                                          layer=layer_index, stack_top=stack_top)
                    else:
                        part = data["parts"][1] if 3 <= data["subvariant"] <= 5 else rand.choice(data["parts"])
                        Layers.full_crystal(builder, part, layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    if data["subvariant"] >= 3:
                        if (
                            Processor.SWAPPER in remaining_processors and data["subvariant"] not in (3, 6)
                            and builder.has_crystals
                        ):
                            decryss = _decrystallize_all(data["parts"])
                            Layers.half_half(rand, builder, decryss[0], decryss[1], 0,
                                             layer=layer_index, stack_top=stack_top)
                        else:
                            shape_part = (data["parts"][0] if data["subvariant"] <= 5
                                          else _decrystallize_one(data["parts"][0]))
                            Layers.half_crystal_half_shape(rand, builder, data["parts"][1], shape_part, 0,
                                                           layer=layer_index, stack_top=stack_top)
                    elif Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1], 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, rand.choice(data["parts"]), 0,
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif data["subvariant"] <= 2:
                        picked = rand.choice((0, 1))
                        directs: Sequence[int] = data["directions"]
                        Layers.single(rand, builder, data["parts"][picked], directs[picked],
                                      layer=layer_index, stack_top=stack_top)
                    elif data["subvariant"] in (3, 6):
                        leave_as_is = True
                    else:
                        picked = rand.choice((0, 1))
                        directs: Sequence[int] = data["directions"]
                        directs_list = list(directs)
                        directs_list[picked] = (directs_list[not picked] + 1) % 6
                        data["directions"] = directs_list
                        data["subvariant"] = data["subvariant"] // 3 * 3
                        leave_as_is = True
                elif missing_processor == Processor.SWAPPER:
                    if data["subvariant"] >= 3:
                        if data["subvariant"] in (0, 3, 6) or (Processor.STACKER in remaining_processors
                                                               and 3 <= data["subvariant"] <= 5):
                            leave_as_is = True
                        else:
                            picked = rand.choice((0, 1))
                            directs: Sequence[int] = data["directions"]
                            directs_list = list(directs)
                            directs_list[picked] = (directs_list[not picked] + 1) % 6
                            data["directions"] = directs_list
                            data["subvariant"] = data["subvariant"] // 3 * 3
                            leave_as_is = True
                    elif Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        picked = rand.choice((0, 1))
                        directs: Sequence[int] = data["directions"]
                        Layers.single(rand, builder, data["parts"][picked], directs[picked],
                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if data["subvariant"] <= 2:
                        leave_as_is = True
                    elif Processor.SWAPPER in remaining_processors or Processor.STACKER in remaining_processors:
                        data["parts"] = _decrystallize_all(data["parts"])
                        data["subvariant"] %= 3
                        leave_as_is = True
                    else:
                        picked = rand.choice((0, 1))
                        part = data["parts"][picked]
                        part = part if part[0] != "c" else _decrystallize_one(part)
                        directs: Sequence[int] = data["directions"]
                        Layers.single(rand, builder, part, directs[picked], layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._2_singles(rand, builder, data["subvariant"] <= 5, data["subvariant"] // 3, data["parts"],
                                      data["directions"], data["subvariant"], layer=None, stack_top=stack_top)
            case Variant._2_doubles:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["subvariant"] <= 1 or builder.has_crystals or not builder.shape:
                        directs: Sequence[int] = data["directions"]
                        if data["subvariant"] == 0:
                            picked = int((directs[1] - directs[0]) % 6 != 2)
                            Layers._3_doubles(rand, builder, _new_part_from_shape(rand.choice(data["parts"])),
                                              data["parts"][picked], data["parts"][not picked], directs[picked],
                                              layer=layer_index, stack_top=stack_top)
                        else:
                            picked = rand.choice((0, 1))
                            Layers.checkered_2_1(rand, builder, data["parts"][picked], data["parts"][not picked],
                                                 directs[picked]-1, layer=layer_index, stack_top=stack_top)
                    else:
                        part = data["parts"][1] if 3 <= data["subvariant"] <= 5 else rand.choice(data["parts"])
                        Layers.full_crystal(builder, part, layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    if data["subvariant"] >= 2:
                        if Processor.SWAPPER in remaining_processors and (not builder.shape or builder.has_crystals):
                            decryss = _decrystallize_all(data["parts"])
                            Layers.half_half(rand, builder, decryss[0], decryss[1], 0,
                                             layer=layer_index, stack_top=stack_top)
                        else:
                            shape_part = (data["parts"][0] if data["subvariant"] <= 3
                                          else _decrystallize_one(data["parts"][0]))
                            Layers.half_crystal_half_shape(rand, builder, data["parts"][1], shape_part, 0,
                                                           layer=layer_index, stack_top=stack_top)
                    elif Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][1], 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, rand.choice(data["parts"]), 0,
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        directs: Sequence[int] = data["directions"]
                        Layers.double(rand, builder, data["parts"][1], directs[1],
                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER not in remaining_processors:
                        directs: Sequence[int] = data["directions"]
                        Layers.double(rand, builder, data["parts"][1], directs[1],
                                      layer=layer_index, stack_top=stack_top)
                    else:
                        if data["subvariant"] >= 4:
                            data["subvariant"] -= 2
                            data["parts"] = (_decrystallize_one(data["parts"][0]), data["parts"][1])
                        leave_as_is = True
                elif missing_processor == Processor.CRYSTALLIZER:
                    if data["subvariant"] <= 1:
                        leave_as_is = True
                    else:
                        data["parts"] = _decrystallize_all(data["parts"])
                        data["subvariant"] %= 2
                        leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    Layers._2_doubles(rand, builder, data["subvariant"] <= 3, data["subvariant"] // 2, data["parts"],
                                      data["directions"], data["subvariant"], layer=None, stack_top=stack_top)
            case Variant._5_singles:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["subvariant"] == 0 or builder.has_crystals or not builder.shape:
                        Layers._6_singles(rand, builder, True, 0,
                                          _decrystallize_all((*data["parts"], rand.choice(data["parts"]))),
                                          data["direction"], False, 0, layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.full_crystal(builder, rand.choice(tuple(p for p in data["parts"] if p[0] == "c")),
                                            layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    if data["subvariant"] >= 1:
                        if Processor.SWAPPER in remaining_processors and (not builder.shape or builder.has_crystals):
                            parts = data["parts"] if data["subvariant"] < 10 else _decrystallize_all(data["parts"])
                            parts = tuple(p for p in parts if p[0] != "c")
                            Layers.half_half(rand, builder, parts[-1], parts[0], 0,
                                             layer=layer_index, stack_top=stack_top)
                        else:
                            crystal_part = rand.choice(tuple(p for p in data["parts"] if p[0] == "c"))
                            shape_parts = tuple(p for p in data["parts"] if p[0] != "c")
                            shape_part = shape_parts[0] if shape_parts else _decrystallize_one(data["parts"][0])
                            Layers.half_crystal_half_shape(rand, builder, crystal_part, shape_part, 0,
                                                           layer=layer_index, stack_top=stack_top)
                    elif Processor.SWAPPER in remaining_processors and has_fillable:
                        Layers.half_half(rand, builder, data["parts"][0], data["parts"][-1], 0,
                                         layer=layer_index, stack_top=stack_top)
                    else:
                        Layers.half(rand, builder, rand.choice(data["parts"]), 0,
                                    layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif data["subvariant"] == 0:
                        picked = rand.randint(0, 4)
                        Layers.single(rand, builder, data["parts"][picked], data["direction"] + picked,
                                      layer=layer_index, stack_top=stack_top)
                    else:
                        parts = data["parts"]
                        pick1, pick2 = rand.randint(0, 4), rand.randint(0, 4)
                        while (pick1 == pick2 or (data["subvariant"] != 10 and parts[pick1][0] == "c"
                                                            and parts[pick2][0] == "c")
                               or (parts[pick1][0] != "c" and parts[pick2][0] != "c")):
                            pick2 = (pick2 + 1) % 5
                        crys_col = (parts[pick1][0] == "c") + (parts[pick2][0] == "c")
                        subv = -1 + 3*crys_col + min(abs(pick1-pick2), 6 - abs(pick1-pick2))
                        Layers._2_singles(rand, builder, True, crys_col, (parts[pick1], parts[pick2]),
                                          (data["direction"] + pick1, data["direction"] + pick2), subv,
                                          layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if data["subvariant"] != 0:
                        if data["subvariant"] >= 6 or Processor.STACKER not in remaining_processors:
                            parts = data["parts"]
                            pick1, pick2 = rand.randint(0, 4), rand.randint(0, 4)
                            while (pick1 == pick2 or (data["subvariant"] != 10 and parts[pick1][0] == "c"
                                                                and parts[pick2][0] == "c")
                                   or (parts[pick1][0] != "c" and parts[pick2][0] != "c")):
                                pick2 = (pick2 + 1) % 5
                            crys_col = (parts[pick1][0] == "c") + (parts[pick2][0] == "c")
                            subv = -1 + 3*crys_col + min(abs(pick1-pick2), 6 - abs(pick1-pick2))
                            Layers._2_singles(rand, builder, True, crys_col, (parts[pick1], parts[pick2]),
                                              (data["direction"] + pick1, data["direction"] + pick2), subv,
                                              layer=layer_index, stack_top=stack_top)
                        else:
                            leave_as_is = True
                    elif Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        picked = rand.randint(0, 4)
                        Layers.single(rand, builder, data["parts"][picked], data["direction"] + picked,
                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if data["subvariant"] != 0:
                        data["parts"] = _decrystallize_all(data["parts"])
                        data["subvariant"] = 0
                    leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    crys_cols = {0: 0, 1: 1, 2: 1, 3: 1, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3, 10: 5}
                    Layers._5_singles(rand, builder, data["subvariant"] != 10, crys_cols[data["subvariant"]],
                                      data["parts"], data["direction"], False, data["subvariant"],
                                      layer=None, stack_top=stack_top)
            case Variant._6_singles:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["subvariant"] == 0:
                        leave_as_is = True
                    elif builder.has_crystals or not builder.shape:
                        data["parts"] = _decrystallize_all(data["parts"])
                        data["subvariant"] = 0
                        leave_as_is = True
                    else:
                        Layers.full_crystal(builder, rand.choice(tuple(p for p in data["parts"] if p[0] == "c")),
                                            layer=layer_index, force_fill=True)
                elif missing_processor == Processor.ROTATOR:
                    if data["subvariant"] != 0:
                        if Processor.SWAPPER in remaining_processors and builder.has_crystals:
                            if data["subvariant"] == 5:
                                parts = _decrystallize_all((data["parts"][0], data["parts"][-1]))
                            elif data["subvariant"] == 6:
                                parts = _decrystallize_all(rand.choices(data["parts"], k=2))
                            else:
                                parts = rand.choices(tuple(p for p in data["parts"] if p[0] != "c"), k=2)
                            Layers.half_half(rand, builder, parts[1], parts[0], 0,
                                             layer=layer_index, stack_top=stack_top)
                        else:
                            crystal_part = rand.choice(tuple(p for p in data["parts"] if p[0] == "c"))
                            shape_parts = tuple(p for p in data["parts"] if p[0] != "c")
                            shape_part = (rand.choice(shape_parts) if shape_parts
                                          else _decrystallize_one(rand.choice(data["parts"])))
                            Layers.half_crystal_half_shape(rand, builder, crystal_part, shape_part, 0,
                                                           layer=layer_index, stack_top=stack_top)
                    elif Processor.SWAPPER not in remaining_processors or (not has_fillable and
                                                                           Processor.CUTTER in remaining_processors and
                                                                           Processor.STACKER in remaining_processors):
                        Layers.half(rand, builder, rand.choice(data["parts"]), 0,
                                    layer=layer_index, stack_top=stack_top)
                    else:
                        parts = rand.choices(data["parts"], k=2)
                        Layers.half_half(rand, builder, parts[0], parts[1], 0, layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif data["subvariant"] != 0:
                        crystal_part = rand.choice(tuple(p for p in data["parts"] if p[0] == "c"))
                        shape_indices = tuple(i for i in range(6) if data["parts"][i][0] != "c")
                        shape_index = rand.choice(shape_indices) if shape_indices else rand.randint(0, 5)
                        shape_part = (data["parts"][shape_index] if shape_indices
                                      else _decrystallize_one(data["parts"][shape_index]))
                        Layers._5_crystals_1_shape(rand, builder, crystal_part, shape_part,
                                                   shape_index + data["direction"],
                                                   layer=layer_index, stack_top=stack_top)
                    else:
                        position = rand.randint(0, 5)
                        Layers.single(rand, builder, data["parts"][position], data["direction"] + position,
                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.SWAPPER:
                    if data["subvariant"] != 0:
                        if Processor.STACKER not in remaining_processors:
                            parts = data["parts"]
                            pick1, pick2 = rand.randint(0, 5), rand.randint(0, 5)
                            while (pick1 == pick2 or (data["subvariant"] != 6 and parts[pick1][0] == "c"
                                                      and parts[pick2][0] == "c")
                                   or (parts[pick1][0] != "c" and parts[pick2][0] != "c")):
                                pick2 = (pick2 + 1) % 6
                            crys_col = (parts[pick1][0] == "c") + (parts[pick2][0] == "c")
                            subv = -1 + 3*crys_col + min(abs(pick1-pick2), 6 - abs(pick1-pick2))
                            Layers._2_singles(rand, builder, True, crys_col, (parts[pick1], parts[pick2]),
                                              (data["direction"] + pick1, data["direction"] + pick2), subv,
                                              layer=layer_index, stack_top=stack_top)
                        elif data["subvariant"] >= 3:
                            if data["parts"][0][0] == "c":
                                data["parts"] = (data["parts"][0], *_decrystallize_all(data["parts"][1:]))
                            else:
                                data["parts"] = (*_decrystallize_all(data["parts"][:-1]), data["parts"][-1])
                            data["subvariant"] = 1
                            leave_as_is = True
                        else:
                            leave_as_is = True
                    elif Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        position = rand.randint(0, 5)
                        Layers.single(rand, builder, data["parts"][position], data["direction"] + position,
                                      layer=layer_index, stack_top=stack_top)
                elif missing_processor == Processor.CRYSTALLIZER:
                    if data["subvariant"] == 0:
                        leave_as_is = True
                    elif Processor.SWAPPER not in remaining_processors:
                        data["parts"] = _decrystallize_all(data["parts"])
                        data["subvariant"] = 0
                        leave_as_is = True
                    else:
                        picked = rand.choice(tuple(i for i in range(6) if data["parts"][i][0] == "c"))
                        parts = _decrystallize_all((*data["parts"][picked+1:], *data["parts"][:picked]))
                        Layers._5_singles(rand, builder, True, 0, parts, data["direction"]+picked+1, False, 0,
                                          layer=layer_index, stack_top=stack_top)
                else:
                    leave_as_is = True
                if leave_as_is:
                    crys_cols = {0: 0, 1: 1, 2: 3, 3: 3, 4: 3, 5: 5, 6: 6}
                    Layers._6_singles(rand, builder, data["subvariant"] != 6, crys_cols[data["subvariant"]],
                                      data["parts"], data["direction"], False, data["subvariant"],
                                      layer=None, stack_top=stack_top)
            case e:
                raise Exception(f"Unknown layer variant {e}:\nbuilder = {builder.debug_string()}")

    i = 0
    while i < len(builder.blueprint):
        blueprint_instr = builder.blueprint[i]
        if blueprint_instr[0] == Variant._remove:
            builder.blueprint.pop(i)
        else:
            i += 1
    return builder
