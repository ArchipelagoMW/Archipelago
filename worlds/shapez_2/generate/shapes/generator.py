
from random import Random
from typing import TYPE_CHECKING

from . import Processor, generate_tetragonal, ShapeBuilder

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_shape(world: "Shapez2World",
                   processors: list[Processor],
                   complexity: int,
                   exclude: list[str] | None = None) -> ShapeBuilder:
    return generate_new(world.random, processors, complexity, world.options.shape_configuration != "tetragonal",
                        world.options.shape_generation_adjustments["Maximum layers"], exclude)


def generate_new(rand: Random, processors: list[Processor], complexity: int, is_hexagonal: bool, max_layer_count: int,
                 exclude: list[str] | None = None, regen_pools: tuple[list[str], ...] | None = None) -> ShapeBuilder:

    if exclude is None:
        exclude = []

    # Make sure that there is enough complexity to use every processor at least once
    if len(processors) > complexity or (
        len(processors) + 1 > complexity and Processor.ROTATOR in processors and (
            Processor.CUTTER not in processors or Processor.SWAPPER not in processors
        )
    ):
        raise Exception(f"Too low complexity ({complexity}) "
                        f"for processors {', '.join(proc.name for proc in processors)}")

    builder: ShapeBuilder | None = None

    # Use "exclude" as a blacklist
    while builder is None or builder.shape in exclude:

        current_comp = complexity

        # Get layer count
        # min_non_pin_count = 2 if Processor.STACKER in processors and not (Processor.CUTTER in processors and
        #                                                                   Processor.ROTATOR in processors and
        #                                                                   Processor.SWAPPER not in processors) else 1
        min_non_pin_count = 2 if Processor.STACKER in processors else 1
        min_pin_count = 0 if Processor.PIN_PUSHER not in processors else 1
        if Processor.STACKER in processors or Processor.PIN_PUSHER in processors:
            max_count = min(max_layer_count, current_comp - 1 - len(processors) +
                            (Processor.STACKER in processors) + (Processor.PIN_PUSHER in processors))
            if min_non_pin_count + min_pin_count <= max_count:
                layer_count = rand.randint(min_non_pin_count + min_pin_count, max_count)
            else:
                layer_count = 2  # Only happens when max layer count == 2 with stacker and pins
        else:
            max_count = 1
            layer_count = 1

        builder = ShapeBuilder(processors, [])
        layer_data: list[LayerData] = [LayerData(i == 0) for i in range(layer_count)]
        # generate_layer = generate_hexagonal.generate_layer if is_hexagonal else generate_tetragonal.generate_layer
        generate_layer = generate_tetragonal.generate_layer

        # Mark forced pin/non-pin layers
        possible_pin_layers = list(range(1, layer_count))
        forced_pin_layer = -1
        if min_pin_count:
            forced_pin_layer = possible_pin_layers.pop(rand.randint(0, len(possible_pin_layers) - 1))
            layer_data[forced_pin_layer].processors.append(Processor.PIN_PUSHER)
        if min_non_pin_count > 1 and min_non_pin_count + min_pin_count <= max_count:
            forced_non_pin_layer = possible_pin_layers.pop(rand.randint(0, len(possible_pin_layers) - 1))
            layer_data[forced_non_pin_layer].force_non_pins = True
        if min_non_pin_count == 1 and Processor.STACKER in processors:
            layer_data[0].processors.append(Processor.STACKER)
        if Processor.PIN_PUSHER in processors and Processor.STACKER not in processors:
            for lay in range(1, layer_count):
                if Processor.PIN_PUSHER not in layer_data[lay].processors:
                    layer_data[lay].processors.append(Processor.PIN_PUSHER)

        for proc_num in range(len(processors)):
            proc = processors[proc_num]
            if proc in (Processor.PIN_PUSHER, Processor.STACKER):
                continue
            to_task = rand.randint(0, layer_count - 1)
            temp_to_task = to_task
            if proc == Processor.CRYSTALLIZER and Processor.CUTTER not in processors:
                to_task = forced_pin_layer
            else:
                if proc == Processor.SWAPPER:
                    while any(_proc in layer_data[to_task].processors
                              for _proc in (Processor.CUTTER, Processor.STACKER, Processor.PIN_PUSHER)):
                        to_task = (to_task + 1) % layer_count
                        if temp_to_task == to_task:
                            break
                elif proc == Processor.CUTTER:
                    while any(_proc in layer_data[to_task].processors
                              for _proc in (Processor.SWAPPER, Processor.PIN_PUSHER)):
                        to_task = (to_task + 1) % layer_count
                        if temp_to_task == to_task:
                            break
                for restr, needed in Processor.restrictions().items():
                    if proc == restr:
                        while not any(_proc in layer_data[to_task].processors[:proc_num] for _proc in needed):
                            to_task = (to_task + 1) % layer_count
                            if temp_to_task == to_task:
                                break
                # Following is not in else clause in order to avoid endless loops and being put on a forced pins layer
                if proc != Processor.CRYSTALLIZER and not (proc == Processor.MIXER and
                                                           Processor.CRYSTALLIZER in layer_data[to_task].processors):
                    while Processor.PIN_PUSHER in layer_data[to_task].processors:
                        to_task = (to_task + 1) % layer_count
            layer_data[to_task].processors.append(proc)

        current_comp -= layer_count - 1
        for data in layer_data:
            builder.tasked = [False] * 8
            for proc in data.processors:
                builder.tasked[proc] = True
            temp_comp = builder.calc_required_complexity()
            data.complexity += temp_comp
            current_comp -= temp_comp
            data.tasked = builder.tasked

        # Maybe just let one or two complexity slip through
        check_negative_comp = True
        if check_negative_comp:
            if current_comp < 0:
                sep = '\n    '
                raise Exception(f"Negative complexity:\n"
                                f"complexity = {complexity}\n"
                                f"current complexity = {current_comp}\n"
                                f"layer data ({len(layer_data)}) = {sep.join(str(ld) for ld in layer_data)}")

        if current_comp > 0:
            comp_packs = current_comp // 20 + 1
            for _ in range(current_comp // comp_packs):
                rand.choice(layer_data).complexity += comp_packs
            rand.choice(layer_data).complexity += current_comp % comp_packs

        for data in layer_data:
            builder.tasked = data.tasked
            builder.cached_tasks.append(data.tasked.copy())
            generate_layer(rand, data.complexity, builder, regen_pools=regen_pools, force_non_pins=data.force_non_pins)

    if any(not isinstance(layer, str) for layer in builder.shape):
        raise Exception(f"Non-string layer found:\n"
                        f"complexity = {complexity}, builder = {builder.debug_string()}")

    return builder


class LayerData:
    force_non_pins: bool
    processors: list[Processor]
    tasked: list[bool]
    complexity: int

    def __init__(self, force_non_pins: bool):
        self.force_non_pins = force_non_pins
        self.processors = []
        self.tasked = []
        self.complexity = 0

    def __str__(self):
        return (f"[force_non_pins: {self.force_non_pins}, processors: {self.processors}, tasked: {self.tasked}, "
                f"complexity: {self.complexity}]")
