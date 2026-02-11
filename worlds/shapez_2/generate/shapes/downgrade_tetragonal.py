from random import Random
from typing import Iterable, Sequence

from . import Processor, ShapeBuilder


def downgrade_4(rand: Random, builder: ShapeBuilder, remaining_processors: list[Processor],
                missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    from .generate_tetragonal import Variant, stack, generate_shape, fill_crystal

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
                for i in range(0, 8, 2):
                    if layer[i] == "c" and layer[i+1] not in crystal_pool:
                        crystal_pool.append(layer[i+1])
                    elif layer[i] in "CRSW" and layer[i:i+2] not in shape_pool:
                        shape_pool.append(layer[i:i+2])
            from .generator import generate_new
            return generate_new(rand, remaining_processors, original_complexity, False, len(builder.blueprint),
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
    # initializing here with placeholder values, so that the functions can be defined outside the loop
    layer_index, variant, stack_top, data = -1, -1, False, {}

    def _unpaint(*, parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
        # Assumes exactly one of the params is not None
        if parts is not None:
            return tuple(_p[0] + ("u" if _p[0] in "CRSW" else _p[1]) for _p in parts)
        else:
            return "".join(long[i] + ("u" if long[i] in "CRSW" else long[i+1]) for i in range(0, len(long), 2))

    def _unmix(*, parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
        # Assumes this only gets called when missing_processor == Processor.MIXER
        # Also assumes exactly one of the params is not None
        if parts is not None:
            return tuple(_p[0] + mixer_replacements[_p[1]] for _p in parts)
        else:
            return "".join(long[i] + mixer_replacements[long[i+1]] for i in range(0, len(long), 2))

    def _decrystallize(*, parts: Iterable[str] = None, long: str = None) -> Iterable[str] | str:
        # Assumes exactly one of the params is not None
        _has_painter = Processor.PAINTER in remaining_processors
        if parts is not None:
            return tuple((_p if _p[0] != "c" else (crystal_replacement[_p[1]] + ("u" if not _has_painter else _p[1])))
                         for _p in parts)
        else:
            return "".join((long[i:i+2] if long[i] != "c" else
                            (crystal_replacement[long[i+1]] + ("u" if not _has_painter else long[i+1])))
                           for i in range(0, len(long), 2))

    def _new_crys_part(_other: str) -> str:
        return "c" + rand.choice([c for c in ("r", "g", "b") if c != _other[1]])

    def _new_part_from_shape(_part: str) -> str:
        _s = generate_shape(rand, _part[0])
        if Processor.PAINTER in remaining_processors:
            return _s + rand.choice(["r", "b", "g", _part[1]])
        else:
            return _s + "u"

    def _half(_p: str, _dir: int):
        _lay = [_p * 2 + "----", "--" + _p * 2 + "--", "----" + _p * 2, _p + "----" + _p][_dir]
        stack(rand, builder, _lay, True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.half, stack_top, {"part": _p, "layer": _lay})

    def _half_crystal(_p: str, _dir: int):
        # _lay = "--" * (_dir % 3) + _p * (2 if _dir < 3 else 1) + "--" * ((2 - _dir) % 3) + _p * (_dir // 3)
        _lay = [_p * 2 + "----", "--" + _p * 2 + "--", "----" + _p * 2, _p + "----" + _p][_dir]
        stack(rand, builder, _lay, False, 1, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.half_crystal, stack_top, {"part": _p, "layer": _lay})

    def _3_1(_p3: str, _p1: str, _pos: int):
        _ord = [_p3] * 4
        _ord[_pos] = _p1
        stack(rand, builder, "".join(_ord), True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant._3_1, stack_top, {"ordered": _ord, "parts": (_p3, _p1)})

    def _3_1_crystals(_p3: str, _p1: str, _pos: int):
        _ord = [_p3] * 4
        _ord[_pos] = _p1
        stack(rand, builder, "".join(_ord), False, 2, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant._3_1_crystals, stack_top, {"ordered": _ord, "parts": (_p3, _p1)})

    def _3_crystals_1_shape(_pc: str, _ps: str, _pos: int):
        _ord = [_pc] * 4
        _ord[_pos] = _ps
        stack(rand, builder, "".join(_ord), True, 1, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant._3_crystals_1_shape, stack_top,
                                          {"ordered": _ord, "parts": (_ps, _pc)})

    def _cut_out(_ord: Sequence[str]):
        _p = _ord[0] if _ord[0] != "--" else _ord[1]
        stack(rand, builder, "".join(_ord), True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.cut_out, stack_top, {"ordered": _ord, "part": _p})

    def _single(_p: str, _pos: int):
        _ord = ["--"] * 4
        _ord[_pos] = _p
        stack(rand, builder, "".join(_ord), True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.single, stack_top, {"ordered": _ord})

    def _more_singles(_pp: Sequence[str], _poss: Sequence[int], _variant: int, _subv: int):
        _ord = ["--"] * 4
        for i in range(len(_poss)):
            _ord[_poss[i]] = _pp[i]
        _lay = "".join(_ord)
        _crys_count = sum(_p[0] == "c" for _p in _pp)
        stack(rand, builder, _lay, _crys_count < len(_pp), _crys_count, blueprint=stack_top)
        builder.blueprint[layer_index] = (_variant, stack_top, {"layer": _lay, "subvariant": _subv})

    def _half_half(_p1: str, _p2: str, _horizontal: bool):
        _lay = _p1 * 2 + _p2 * 2 if not _horizontal else _p1 + _p2 * 2 + _p1
        stack(rand, builder, _lay, True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.half_half, stack_top, {"parts": (_p1, _p2), "layer": _lay})

    def _half_half_crystal(_p1: str, _p2: str, _horizontal: bool):
        _lay = _p1 * 2 + _p2 * 2 if not _horizontal else _p1 + _p2 * 2 + _p1
        stack(rand, builder, _lay, False, 2, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.half_half_crystal, stack_top, {"parts": (_p1, _p2), "layer": _lay})

    def _half_crystal_half_shape(_pc: str, _ps: str, _dir: int):
        _lay = [_ps * 2 + _pc * 2, _pc + _ps * 2 + _pc, _pc * 2 + _ps * 2, _ps + _pc * 2 + _ps][_dir]
        stack(rand, builder, _lay, True, 1, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.half_crystal_half_shape, stack_top,
                                          {"parts": (_ps, _pc), "layer": _lay})

    def _full(_p: str):
        stack(rand, builder, _p * 4, True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.full, stack_top, {"part": _p})

    def _full_crystal(_p: str, force_fill: bool):
        if (
            builder.has_crystals or force_fill or
            Processor.ROTATOR not in remaining_processors or Processor.CUTTER not in remaining_processors
        ):
            fill_crystal(builder, _p[1])
        builder.shape.insert(0, _p * 4)
        builder.has_crystals = True
        builder.blueprint[layer_index] = (Variant.full_crystal, False, {"part": _p})

    def _checkered(_p1: str, _p2: str):
        stack(rand, builder, (_p1 + _p2) * 2, True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.checkered, stack_top, {"parts": (_p1, _p2)})

    def _checkered_crystal_shape(_p1: str, _p2: str):
        stack(rand, builder, (_p1 + _p2) * 2, True, 0, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.checkered_crystal_shape, stack_top, {"parts": (_p1, _p2)})

    def _cornered(_p: str, _dir: int):
        _parts = ("--", _p) if _dir else (_p, "--")
        stack(rand, builder, "".join(_parts * 2), True, False, blueprint=stack_top)
        builder.blueprint[layer_index] = (Variant.cornered, stack_top, {"parts": _parts})

    for _layer_index in range(len(builder.blueprint)):
        layer_index = _layer_index
        for layer in builder.shape:
            if len(layer) != 8:
                raise Exception(f"Invalid layer length:\n{builder.debug_string()}")
        variant, stack_top, data = builder.blueprint[layer_index]
        has_vertical_split = any(layer[0:2] != layer[6:8] or layer[2:4] != layer[4:6] for layer in builder.shape)
        has_horizontal_split = any(layer[0:2] != layer[2:4] or layer[6:8] != layer[4:6] for layer in builder.shape)
        has_fillable_parts = any(layer[i] == "-" for layer in builder.shape for i in range(1, 8, 2))

        match variant:
            case Variant.full:
                if missing_processor == Processor.PAINTER:
                    data["part"] = data["part"][0] + "u"
                elif missing_processor == Processor.MIXER:
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                stack(rand, builder, data["part"] * 4, True, 0, blueprint=stack_top)
            case Variant.half:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["layer"] = _unpaint(long=data["layer"])
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if Processor.ROTATOR in remaining_processors and has_vertical_split:
                        part_2 = _new_part_from_shape(data["part"])
                        parts = (data["part"], part_2) if data["layer"][:2] == data["part"] else (part_2, data["part"])
                        _half_half(parts[0], parts[1], True)
                    elif Processor.SWAPPER in remaining_processors:
                        part_2 = _new_part_from_shape(data["part"])
                        parts = (data["part"], part_2) if data["layer"][:2] == data["part"] else (part_2, data["part"])
                        _half_half(parts[0], parts[1], False)
                    else:
                        _full(data["part"])
                elif missing_processor == Processor.ROTATOR:
                    data["layer"] = data["part"] * 2 + "----"
                    leave_as_is = True  # Only works because the layer is used for leave_as_is
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, data["layer"], True, 0, blueprint=stack_top)
            case Variant.half_half:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = (data["parts"][0][0] + "u", data["parts"][1][0] + "u")
                    data["layer"] = _unpaint(long=data["layer"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors:
                        data["layer"] = data["parts"][0] * 2 + data["parts"][1] * 2
                        leave_as_is = True  # Only works because the layer is used for leave_as_is
                    else:
                        _half(data["parts"][0], 0)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif has_vertical_split:
                        part = rand.choice(data["parts"])
                        _half(part, 3 if data["layer"][:2] == part else 1)
                    elif has_horizontal_split:
                        part = rand.choice(data["parts"])
                        _half(part, 0 if data["layer"][:2] == part else 2)
                    else:
                        position = rand.randint(0, 3)
                        _single(data["layer"][position*2:position*2+2], position)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.CUTTER not in remaining_processors:
                        _full(rand.choice(data["parts"]))
                    elif Processor.ROTATOR not in remaining_processors:
                        _half(data["parts"][0], 0)
                    elif Processor.STACKER not in remaining_processors:
                        if has_vertical_split:
                            part = rand.choice(data["parts"])
                            _half(part, 3 if data["layer"][:2] == part else 1)
                        else:
                            part = rand.choice(data["parts"])
                            _half(part, 2)
                    else:
                        leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, data["layer"], True, 0, blueprint=stack_top)
            case Variant.cut_out:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["ordered"] = _unpaint(parts=data["ordered"])
                    data["part"] = data["part"][0] + "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = _unmix(parts=data["ordered"])
                    data["part"] = data["part"][0] + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    part = _new_part_from_shape(data["part"])
                    _3_1(data["part"], part, data["ordered"].index("--"))
                elif missing_processor == Processor.ROTATOR:
                    _half(data["part"], 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        position = data["ordered"].index("--")
                        _half(data["part"], (position + 2 - (position % 2) if has_horizontal_split
                                             else position + 1 + (position % 2)) % 4)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["ordered"]), True, 0, blueprint=stack_top)
            case Variant._3_1:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["ordered"] = _unpaint(parts=data["ordered"])
                    data["parts"] = (data["parts"][0][0] + "u", data["parts"][1][0] + "u")
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = _unmix(parts=data["ordered"])
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors:
                        parts = data["parts"] if data["ordered"][0] == data["parts"][1] \
                            else list(reversed(data["parts"]))
                        _half_half(parts[0], parts[1], False)
                    else:
                        _half(data["ordered"][0], 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        _single(data["parts"][1], data["ordered"].index(data["parts"][1]))
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["ordered"]), True, 0, blueprint=stack_top)
            case Variant.cornered:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    top_right = data["parts"][0] != "--"
                    part_1 = data["parts"][0] if top_right else data["parts"][1]
                    part_2 = _new_part_from_shape(part_1)
                    parts = (part_1, part_2) if top_right else (part_2, part_1)
                    _checkered(*parts)
                elif missing_processor == Processor.ROTATOR:
                    _half(data["parts"][0] if data["parts"][0] != "--" else data["parts"][1], 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        top_right = data["parts"][0] != "--"
                        _single(data["parts"][0] if top_right else data["parts"][1],
                                 rand.choice((0, 2)) if top_right else rand.choice((1, 3)))
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["parts"]) * 2, True, 0, blueprint=stack_top)
            case Variant.random_shapes_1_color:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["color"] = "u"
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["color"] = mixer_replacements[data["color"]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if Processor.STACKER in remaining_processors:
                        leave_as_is = True
                    else:
                        position = rand.randint(0, 1)
                        horizontal = rand.choice((True, False))
                        shape_parts = (data["ordered"][position], data["ordered"][position+2])
                        shape_parts = tuple(reversed(shape_parts)) if horizontal and position else shape_parts
                        _half_half(shape_parts[0] + data["color"], shape_parts[1] + data["color"], horizontal)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors:
                        position = rand.randint(0, 1)
                        shape_parts = (data["ordered"][position], data["ordered"][position+2])
                        if shape_parts[0] == shape_parts[1]:
                            shape_parts = (shape_parts[0], data["ordered"][position+1])
                        _half_half(shape_parts[0] + data["color"], shape_parts[1] + data["color"], False)
                    else:
                        position = rand.randint(0, 1)
                        _half(data["ordered"][position] + data["color"], 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        position = rand.randint(0, 3)
                        _single(data["ordered"][position] + data["color"], position)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(part + data["color"] for part in data["ordered"]),
                          True, 0, blueprint=stack_top)
            case Variant.checkered:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    data["parts"] = (data["parts"][0][0] + "u", data["parts"][1][0] + "u")
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors:
                        parts = list(data["parts"])
                        rand.shuffle(parts)
                        _half_half(parts[0], parts[1], False)
                    else:
                        _half(rand.choice(data["parts"]), 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        position = rand.randint(0, 3)
                        _single(data["parts"][position%2], position)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["parts"]) * 2, True, 0, blueprint=stack_top)
            case Variant.random_colors_1_shape:
                leave_as_is = False
                if missing_processor == Processor.PAINTER:
                    _full(data["shape"] + "u")
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = tuple(mixer_replacements[color] for color in data["ordered"])
                    leave_as_is = True
                elif missing_processor == Processor.ROTATOR:
                    if Processor.SWAPPER in remaining_processors:
                        positions = (rand.randint(0, 1), rand.randint(2, 3))
                        _half_half(data["shape"] + data["ordered"][positions[0]],
                                   data["shape"] + data["ordered"][positions[1]], False)
                    else:
                        _half(data["shape"] + rand.choice(data["ordered"][:2]), 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    else:
                        position = rand.randint(0, 3)
                        _single(data["shape"] + data["ordered"][position], position)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["shape"] + color for color in data["ordered"]),
                          True, 0, blueprint=stack_top)
            case Variant.pins:
                if missing_processor != Processor.PIN_PUSHER:  # make pin layer
                    if not len(builder.shape):
                        raise Exception(f"Found pins as first layer:\n"
                                        f"missing processor: {missing_processor},\n"
                                        f"builder: {builder.debug_string()},\n"
                                        f"blueprint: {builder.blueprint}")
                    part = ""
                    for i in range(0, 8, 2):
                        part += "P-" if builder.shape[0][i] != "-" else "--"
                    builder.shape.insert(0, part)
                else:  # remove layer
                    builder.blueprint[layer_index] = (Variant._remove, False, {})
            case Variant.full_crystal:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if Processor.PIN_PUSHER in remaining_processors and builder.shape:
                        part = ""
                        for i in range(0, 8, 2):
                            part += "P-" if builder.shape[0][i] != "-" else "--"
                        builder.shape.insert(0, part)
                        builder.blueprint[layer_index] = (Variant.pins, False, {})
                    else:
                        part = _decrystallize(long=data["part"])
                        _single(part, rand.randint(0, 3))
                elif missing_processor == Processor.MIXER:
                    data["part"] = "c" + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.PIN_PUSHER:
                    part = _decrystallize(long=data["part"])
                    _half_crystal_half_shape(data["part"], part, 0)
                elif missing_processor == Processor.ROTATOR:
                    if Processor.PIN_PUSHER in remaining_processors:
                        leave_as_is = True
                    else:
                        part = _decrystallize(long=data["part"])
                        _half_crystal_half_shape(data["part"], part, 0)
                else:
                    leave_as_is = True
                if leave_as_is:
                    if (
                        builder.has_crystals or
                        Processor.ROTATOR not in remaining_processors or Processor.CUTTER not in remaining_processors
                    ):
                        fill_crystal(builder, data["part"][1])
                    builder.shape.insert(0, data["part"] * 4)
                    builder.has_crystals = True
            case Variant.half_crystal:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    part = _decrystallize(long=data["part"])
                    _half(part, data["layer"].index(data["part"]) // 2)
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    data["part"] = "c" + mixer_replacements[data["part"][1]]
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    _full_crystal(data["part"], True)
                elif missing_processor == Processor.ROTATOR:
                    part = _decrystallize(long=data["part"])
                    _half_crystal_half_shape(data["part"], part, 0)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, data["layer"], False, 1, blueprint=stack_top)
            case Variant.half_half_crystal:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if Processor.STACKER in remaining_processors:
                        part_1, part_2 = _decrystallize(parts=data["parts"])
                        _half_half(part_1, part_2, data["layer"][0:2] != data["layer"][2:4])
                    elif has_horizontal_split:
                        choice = rand.randint(0, 1)
                        part = _decrystallize(long=data["parts"][choice])
                        _half(part, choice * 2)
                    elif has_vertical_split:
                        choice = rand.randint(0, 1)
                        part = _decrystallize(long=data["parts"][choice])
                        _half(part, 3 - (choice * 2))
                    else:
                        position = rand.randint(0, 3)
                        _single(data["layer"][2*position:2*position+2], position)
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    part_1, part_2 = _decrystallize(parts=data["parts"])
                    _half_half(part_1, part_2, data["layer"][0:2] != data["layer"][2:4])
                elif missing_processor == Processor.ROTATOR:
                    part = _decrystallize(long=data["parts"][0])
                    _half_crystal_half_shape(data["parts"][1], part, 0)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, data["layer"], False, 2, blueprint=stack_top)
            case Variant.half_crystal_half_shape:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if Processor.ROTATOR not in remaining_processors:
                        _half(data["parts"][0], 0)
                    elif Processor.STACKER in remaining_processors:
                        part_2 = _decrystallize(long=data["parts"][1])
                        _half_half(data["parts"][0], part_2, data["layer"][0:2] != data["layer"][2:4])
                    elif has_horizontal_split:
                        choice = rand.randint(0, 1)
                        part = _decrystallize(long=data["parts"][choice])
                        _half(part, choice * 2)
                    elif has_vertical_split:
                        choice = rand.randint(0, 1)
                        part = _decrystallize(long=data["parts"][choice])
                        _half(part, 3 - (choice * 2))
                    else:
                        position = rand.randint(0, 3)
                        _single(data["layer"][2*position:2*position+2], position)
                elif missing_processor == Processor.PAINTER:
                    data["layer"] = _unpaint(long=data["layer"])
                    data["parts"] = _unpaint(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if builder.has_crystals:
                        _full(data["parts"][0])
                    else:
                        _full_crystal(data["parts"][1], True)
                elif missing_processor == Processor.ROTATOR:
                    data["layer"] = data["parts"][0] * 2 + data["parts"][1] * 2
                    leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, data["layer"], True, 1, blueprint=stack_top)
            case Variant.cut_out_crystal:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    _cut_out(_decrystallize(parts=data["ordered"]))
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = _decrystallize(parts=data["ordered"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if has_fillable_parts or builder.has_crystals:
                        ordered = _decrystallize(parts=data["ordered"])
                        part_1 = ordered[0] if ordered[0] != "--" else ordered[1]
                        part_2 = _new_part_from_shape(part_1)
                        _3_1(part_1, part_2, data["ordered"].index("--"))
                    else:
                        _full_crystal(data["ordered"][0] if data["ordered"][0] != "--" else data["ordered"][1], True)
                elif missing_processor == Processor.ROTATOR:
                    part_c = data["ordered"][0] if data["ordered"][0] != "--" else data["ordered"][1]
                    part_s = _decrystallize(long=part_c)
                    _half_crystal_half_shape(part_c, part_s, 0)
                elif missing_processor == Processor.SWAPPER:
                    if rand.random() < 0.5:
                        part_c = data["ordered"][0] if data["ordered"][0] != "--" else data["ordered"][1]
                        part_s = _decrystallize(long=part_c)
                        _3_crystals_1_shape(part_c, part_s, data["ordered"].index("--"))
                    else:
                        part_1 = data["ordered"][0] if data["ordered"][0] != "--" else data["ordered"][1]
                        part_2 = _new_crys_part(part_1)
                        _3_1_crystals(part_1, part_2, data["ordered"].index("--"))
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["ordered"]), False, 1, blueprint=stack_top)
            case Variant._3_1_crystals:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if Processor.SWAPPER in remaining_processors:
                        ordered = list(data["ordered"])
                        ordered[ordered.index(data["parts"][1])] = "--"
                        ordered = _decrystallize(parts=ordered)
                        _cut_out(ordered)
                    elif Processor.STACKER in remaining_processors:
                        parts = _decrystallize(parts=data["parts"])
                        _3_1(parts[0], parts[1], data["ordered"].index(data["parts"][1]))
                    else:
                        _single(_decrystallize(long=data["parts"][1]), data["ordered"].index(data["parts"][1]))
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = _unmix(parts=data["ordered"])
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not has_fillable_parts:
                        _full(rand.choice(data["parts"]))
                    else:
                        parts = _decrystallize(parts=data["parts"])
                        _3_1(parts[0], parts[1], data["ordered"].index(data["parts"][1]))
                elif missing_processor == Processor.ROTATOR:
                    _half_crystal_half_shape(data["parts"][0], _decrystallize(long=data["parts"][1]), 0)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["ordered"]), False, 2, blueprint=stack_top)
            case Variant._3_crystals_1_shape:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if Processor.STACKER in remaining_processors and Processor.SWAPPER not in remaining_processors:
                        part = _decrystallize(long=data["parts"][1])
                        _3_1(part, data["parts"][0], data["ordered"].index(data["parts"][1]))
                    else:
                        _single(data["parts"][0], data["ordered"].index(data["parts"][1]))
                elif missing_processor == Processor.PAINTER:
                    data["ordered"] = _unpaint(parts=data["ordered"])
                    data["parts"] = _unpaint(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = _unmix(parts=data["ordered"])
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not has_fillable_parts:
                        _full(data["parts"][1])
                    else:
                        pars = _decrystallize(long=data["parts"][1])
                        _3_1(pars, data["parts"][0], data["ordered"].index(data["parts"][0]))
                elif missing_processor == Processor.ROTATOR:
                    _half_crystal_half_shape(data["parts"][1], data["parts"][0], 0)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["ordered"]), True, 1, blueprint=stack_top)
            case Variant._3_shapes_1_crystal:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        ordered = list(data["ordered"])
                        ordered[ordered.index(data["parts"][1])] = "--"
                        _cut_out(ordered)
                    else:
                        position = data["ordered"].index(data["parts"][1])
                        _half(data["parts"][0], (position + 2 - (position % 2) if has_horizontal_split
                                                 else position + 1 + (position % 2)) % 4)
                elif missing_processor == Processor.PAINTER:
                    data["ordered"] = _unpaint(parts=data["ordered"])
                    data["parts"] = _unpaint(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = _unmix(parts=data["ordered"])
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not has_fillable_parts:
                        _full(data["parts"][1])
                    else:
                        pars = _decrystallize(long=data["parts"][1])
                        _3_1(data["parts"][0], pars, data["ordered"].index(data["parts"][1]))
                elif missing_processor == Processor.ROTATOR:
                    _half_crystal_half_shape(data["parts"][1], data["parts"][0], 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif rand.random() < 0.5:
                        _3_crystals_1_shape(data["parts"][1], data["parts"][0], data["ordered"].index(data["parts"][1]))
                    else:
                        _half_crystal_half_shape(data["parts"][1], data["parts"][0], 0)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["ordered"]), True, 1, blueprint=stack_top)
            case Variant.cornered_crystal:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    direction = (data["parts"].index("--") + 1) % 2
                    part = _decrystallize(long=(data["parts"][direction]))
                    _cornered(part, direction)
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    part_1 = data["parts"][0] if data["parts"][0] != "--" else data["parts"][1]
                    if not has_fillable_parts:
                        _full_crystal(part_1, True)
                    else:
                        part_1 = _decrystallize(long=part_1)
                        _checkered(part_1, _new_part_from_shape(part_1))
                elif missing_processor == Processor.ROTATOR:
                    part_1 = data["parts"][0] if data["parts"][0] != "--" else data["parts"][1]
                    _half_crystal_half_shape(part_1, _decrystallize(long=part_1), 0)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        parts = list(data["parts"])
                        position = parts.index("--")
                        parts[position] = _decrystallize(long=parts[(position+1)%2])
                        _checkered_crystal_shape(*parts)
                    else:
                        part = data["parts"][0] if data["parts"][0] != "--" else data["parts"][1]
                        _half_crystal(part, rand.randint(0, 3))
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["parts"]) * 2, False, 1, blueprint=stack_top)
            case Variant.checkered_crystal:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    position = rand.randint(0, 1)
                    _cornered(_decrystallize(long=data["parts"][position]), position)
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not has_fillable_parts:
                        _full_crystal(rand.choice(data["parts"]), True)
                    else:
                        _checkered(*_decrystallize(parts=data["parts"]))
                elif missing_processor == Processor.ROTATOR:
                    id_1, id_2 = (0, 1) if rand.random() < 0.5 else (1, 0)
                    _half_crystal_half_shape(data["parts"][id_1], _decrystallize(long=data["parts"][id_2]), 0)
                elif missing_processor == Processor.SWAPPER:
                    if Processor.STACKER in remaining_processors:
                        id_shape = rand.randint(0, 1)
                        parts = list(data["parts"])
                        parts[id_shape] = _decrystallize(long=parts[id_shape])
                        _checkered_crystal_shape(*parts)
                    else:
                        if rand.random() < 0.5:
                            position = rand.randint(0, 3)
                            _3_1_crystals(data["parts"][(position+1)%2], data["parts"][position%2], position)
                        else:
                            parts = data["parts"] if rand.random() < 0.5 else tuple(reversed(data["parts"]))
                            _half_half_crystal(parts[0], parts[1], rand.random() < 0.5)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["parts"]) * 2, False, 2, blueprint=stack_top)
            case Variant.checkered_crystal_shape:
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if Processor.SWAPPER in remaining_processors:
                        direction = 0 if data["parts"][0][0] != "c" else 1
                        _cornered(data["parts"][direction], direction)
                    else:
                        _checkered(*_decrystallize(parts=data["parts"]))
                elif missing_processor == Processor.PAINTER:
                    data["parts"] = _unpaint(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["parts"] = _unmix(parts=data["parts"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not has_fillable_parts and not builder.has_crystals:
                        _full_crystal(data["parts"][0 if data["parts"][0][0] == "c" else 1], True)
                    else:
                        _checkered(*_decrystallize(parts=data["parts"]))
                elif missing_processor == Processor.ROTATOR:
                    part_c, part_s = data["parts"] if data["parts"][0][0] == "c" else tuple(reversed(data["parts"]))
                    _half_crystal_half_shape(part_c, part_s, 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif rand.random() < 0.5:
                        part_c, part_s = data["parts"] if data["parts"][0][0] == "c" else tuple(reversed(data["parts"]))
                        _half_crystal_half_shape(part_c, part_s, 0)
                    else:
                        direction = (0 if data["parts"][0][0] != "c" else 1)
                        _3_crystals_1_shape(data["parts"][(direction+1)%2], data["parts"][direction],
                                            direction + rand.choice((0, 2)))
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, "".join(data["parts"]) * 2, True, 1, blueprint=stack_top)
            case Variant.single:
                leave_as_is = False
                part = tuple(p for p in data["ordered"] if p != "--")[0]
                if missing_processor == Processor.CRYSTALLIZER:
                    if part[0] == "c":
                        data["ordered"] = _decrystallize(parts=data["ordered"])
                    leave_as_is = True
                elif missing_processor == Processor.PAINTER:
                    data["ordered"] = _unpaint(parts=data["ordered"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["ordered"] = _unmix(parts=data["ordered"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if not has_fillable_parts and part[0] == "c":
                        _full_crystal(part, True)
                    else:
                        part_1 = _decrystallize(long=part)
                        part_2 = _new_part_from_shape(part_1)
                        _3_1(part_2, part_1, data["ordered"].index(part))
                elif missing_processor == Processor.ROTATOR:
                    if part[0] == "c":
                        part_s = _decrystallize(long=part)
                        _half_crystal_half_shape(part, part_s, 0)
                    else:
                        _half(part, 0)
                else:
                    leave_as_is = True
                if leave_as_is:
                    _a, _b = (True, 0) if part[0] != "c" else (False, 1)
                    stack(rand, builder, "".join(data["ordered"]), _a, _b, blueprint=stack_top)
            case Variant._2_singles:
                parts, positions = [], []
                for i in range(0, 8, 2):
                    if data["layer"][i] != "-":
                        parts.append(data["layer"][i:i+2])
                        positions.append(i//2)
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if data["subvariant"] < 2:
                        leave_as_is = True
                    else:
                        if (
                            data["subvariant"] >= 2 and data["subvariant"] % 2 and
                            not (Processor.STACKER in remaining_processors or Processor.ROTATOR in remaining_processors)
                        ):
                            chosen = rand.randint(0, 1)
                            positions[chosen] = (positions[chosen] + rand.choice((1, -1))) % 4
                        _more_singles(_decrystallize(parts=parts), positions, Variant._2_singles,
                                      (positions[1] - positions[0] + 1) % 2)
                elif missing_processor == Processor.PAINTER:
                    data["layer"] = _unpaint(long=data["layer"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["subvariant"] in (2, 3) and not has_fillable_parts:
                        _full_crystal(rand.choice(parts), True)
                    elif rand.random() < 0.5:
                        if data["subvariant"] % 2:
                            _checkered(*_decrystallize(parts=parts))
                        else:
                            parts = _decrystallize(parts=parts)
                            _checkered(*(parts if positions[0] % 2 == 0 else reversed(parts)))
                    else:
                        parts = _decrystallize(parts=(reversed(parts) if positions[0] % 2 else parts))
                        _checkered(*parts)
                elif missing_processor == Processor.ROTATOR:
                    if data["subvariant"] in (2, 3):
                        part_s = _decrystallize(long=parts[0])
                        _half_crystal_half_shape(parts[1], part_s, 0)
                    elif data["subvariant"] in (4, 5):
                        parts = parts if parts[0][0] == "c" else tuple(reversed(parts))
                        _half_crystal_half_shape(parts[0], parts[1], 0)
                    elif Processor.SWAPPER in remaining_processors:
                        _half_half(parts[0], parts[1], False)
                    else:
                        _half(rand.choice(parts), 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif data["subvariant"] in (0, 1):
                        choice = rand.randint(0, 1)
                        _single(parts[choice], positions[choice])
                    elif not data["subvariant"] % 2:
                        leave_as_is = True
                    else:
                        if data["subvariant"] % 2:
                            chosen = rand.randint(0, 1)
                            positions[chosen] = (positions[chosen] + rand.choice((1, -1))) % 4
                        _more_singles(_decrystallize(parts=parts), positions, Variant._2_singles, 0)
                else:
                    leave_as_is = True
                    _more_singles(parts, positions, Variant._2_singles, data["subvariant"])
                if leave_as_is:
                    stack(rand, builder, data["layer"], data["subvariant"] not in (2, 3),
                          (data["subvariant"] // 2 - 3) * -1 % 3, blueprint=stack_top)
            case Variant._3_singles:
                parts, positions = [], []
                for i in range(0, 8, 2):
                    if data["layer"][i] != "-":
                        parts.append(data["layer"][i:i+2])
                        positions.append(i//2)
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if not data["subvariant"]:
                        leave_as_is = True
                    elif not (Processor.STACKER in remaining_processors or Processor.SWAPPER in remaining_processors):
                        choice = rand.randint(0, 2)
                        _single(parts[choice], positions[choice])
                    else:
                        data["layer"] = _decrystallize(long=data["layer"])
                        data["subvariant"] = 0
                        leave_as_is = True
                elif missing_processor == Processor.PAINTER:
                    data["layer"] = _unpaint(long=data["layer"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["subvariant"] == 5 and not has_fillable_parts:
                        _full_crystal(rand.choice(parts), True)
                    elif rand.random() < 0.5:
                        parts = parts[:2] if positions[:2] == [0, 1] else parts[1:]
                        _checkered(*_decrystallize(parts=parts))
                    else:
                        parts = _decrystallize(parts=parts)
                        _half_half(parts[0], parts[1], positions[:2] == [0, 1])
                elif missing_processor == Processor.ROTATOR:
                    if data["subvariant"]:
                        parts_c = tuple(p for p in parts if p[0] == "c")
                        part_s = _decrystallize(long=parts_c[-1]) if len(parts_c) == 3 \
                            else tuple(p for p in parts if p[0] != "c")[0]
                        _half_crystal_half_shape(parts_c[0], part_s, 0)
                    elif Processor.SWAPPER in remaining_processors:
                        _half_half(parts[0], parts[1], False)
                    else:
                        _half(parts[0], 0)
                elif missing_processor in (Processor.STACKER, Processor.SWAPPER):
                    if Processor.SWAPPER in remaining_processors or (Processor.STACKER in remaining_processors and
                                                                     data["subvariant"] < 4):
                        leave_as_is = True
                    elif not data["subvariant"]:
                        choice = rand.randint(0, 2)
                        _single(parts[choice], positions[choice])
                    elif data["subvariant"] == 2:
                        choices = 0 if parts[0][0] == "c" else 1
                        _more_singles(parts[choices:choices+2], positions[choices:choices+2], Variant._2_singles, 4)
                    else:
                        pos = data["layer"].index("--") // 2
                        positions.append(pos)
                        parts.append(parts[2 if pos >= 2 else 0])
                        subvariant = data["subvariant"] if data["subvariant"] >= 4 else data["subvariant"] + 1
                        _more_singles(parts, positions, Variant._4_singles, subvariant)
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, data["layer"], data["subvariant"] != 5, (data["subvariant"] + 1) // 2,
                          blueprint=stack_top)
            case Variant._4_singles:
                parts, positions = [data["layer"][i:i+2] for i in range(0, 8, 2)], [0, 1, 2, 3]
                leave_as_is = False
                if missing_processor == Processor.CRYSTALLIZER:
                    if not data["subvariant"]:
                        leave_as_is = True
                    elif data["subvariant"] == 4:
                        pos = len(data["layer"][::2].rstrip("c")) - 1
                        _single(parts[pos], pos)
                    else:
                        if data["subvariant"] == 5:
                            parts = _decrystallize(parts=parts)
                        for i in reversed(range(4)):
                            if parts[i][0] == "c":
                                parts.pop(i)
                                positions.pop(i)
                        variant = {
                            1: (Variant._3_singles, 0),
                            2: (Variant._2_singles, 0),
                            3: (Variant._2_singles, 1),
                            5: (Variant._4_singles, 0),
                        }
                        _more_singles(parts, positions, *(variant[data["subvariant"]]))
                elif missing_processor == Processor.PAINTER:
                    data["layer"] = _unpaint(long=data["layer"])
                    leave_as_is = True
                elif missing_processor == Processor.MIXER:
                    data["layer"] = _unmix(long=data["layer"])
                    leave_as_is = True
                elif missing_processor == Processor.CUTTER:
                    if data["subvariant"] >= 4 and not has_fillable_parts:
                        choice = rand.randint(0, 3)
                        choice = choice if parts[choice][0] == "c" else (choice + 1) % 4
                        _full_crystal(parts[choice], True)
                    elif rand.random() < 0.5:
                        choice = rand.randint(0, 3)
                        parts = (parts[choice], parts[(choice + 1) % 4])
                        _checkered(*_decrystallize(parts=parts))
                    else:
                        _half_half(parts[0], parts[2], rand.choice((True, False)))
                elif missing_processor == Processor.ROTATOR:
                    if data["subvariant"]:
                        parts_c = tuple(p for p in parts if p[0] == "c")
                        part_s = _decrystallize(long=parts_c[-1]) if len(parts_c) == 4 \
                            else tuple(p for p in parts if p[0] != "c")[0]
                        _half_crystal_half_shape(parts_c[0], part_s, 0)
                    elif Processor.SWAPPER in remaining_processors:
                        _half_half(parts[rand.randint(0, 1)], parts[rand.randint(2, 3)], False)
                    else:
                        _half(parts[0], 0)
                elif missing_processor == Processor.STACKER:
                    if Processor.SWAPPER in remaining_processors:
                        leave_as_is = True
                    elif not data["subvariant"]:
                        choice = rand.randint(0, 3)
                        _single(parts[choice], choice)
                    elif data["subvariant"] == 5:
                        choice = rand.randint(0, 3)
                        parts[choice] = parts[(choice + rand.choice((1, -1))) % 4]
                        data["layer"] = "".join(parts)
                        leave_as_is = True
                    elif data["subvariant"] >= 2:
                        poss_s = tuple(i for i in range(4) if parts[i][0] != "c")
                        pos_1 = rand.choice(poss_s)
                        parts[pos_1] = parts[(pos_1 + (1 if pos_1 + 1 not in poss_s else -1)) % 4]
                        data["layer"] = "".join(parts)
                        data["subvariant"] = max(data["subvariant"] + 1, 4)
                        leave_as_is = True
                    else:
                        pos_1 = tuple(i for i in range(4) if parts[i][0] != "c")[0]
                        pos_2 = (pos_1 + rand.choice((1, -1))) % 4
                        _more_singles((parts[pos_1], parts[pos_2]), (pos_1, pos_2), Variant._2_singles, 4)
                elif missing_processor == Processor.SWAPPER:
                    if not data["subvariant"] and Processor.STACKER not in remaining_processors:
                        choice = rand.randint(0, 3)
                        _single(parts[choice], choice)
                    elif data["subvariant"] >= 4:
                        poss_c = tuple(i for i in range(4) if parts[i][0] == "c")
                        pos_1 = rand.choice(poss_c)
                        parts[pos_1] = parts[(pos_1 + (1 if pos_1 + 1 in poss_c else -1)) % 4]
                        data["layer"] = "".join(parts)
                        leave_as_is = True
                    elif data["subvariant"] == 3:
                        poss_s = tuple(i for i in range(4) if parts[i][0] != "c")
                        pos_1 = rand.choice(poss_s)
                        parts[pos_1] = parts[(pos_1 + rand.choice((1, -1))) % 4]
                        data["layer"] = "".join(parts)
                        data["subvariant"] = 4
                        leave_as_is = True
                    else:
                        leave_as_is = True
                else:
                    leave_as_is = True
                if leave_as_is:
                    stack(rand, builder, data["layer"], data["subvariant"] != 5,
                          int((data["subvariant"] + 0.5) * (5/6)), blueprint=stack_top)
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
