import enum
from random import Random
from typing import Self, Sequence

restr: dict | None = None


class Processor(enum.IntEnum):
    CUTTER = 0
    ROTATOR = 1
    STACKER = 2
    PAINTER = 3
    MIXER = 4
    PIN_PUSHER = 5
    CRYSTALLIZER = 6
    SWAPPER = 7

    @classmethod
    def restrictions(cls) -> dict[Self, tuple[Self, Self]]:
        global restr
        if restr is None:
            restr = {
                cls.ROTATOR: (cls.CUTTER, cls.SWAPPER),
                cls.CRYSTALLIZER: (cls.CUTTER, cls.PIN_PUSHER),
                cls.MIXER: (cls.PAINTER, cls.CRYSTALLIZER),
            }
        return restr

    @classmethod
    def add_random_next(cls, random: Random, active: list[Self], possible: list[Self] | None) -> None:
        # Assumes active is a sublist of possible
        poss = possible.copy() if possible is not None else [
            cls.CUTTER, cls.ROTATOR, cls.STACKER, cls.PAINTER, cls.MIXER, cls.PIN_PUSHER, cls.CRYSTALLIZER, cls.SWAPPER
        ]
        for a in active:
            if a in poss:
                poss.remove(a)
        for rest, reqs in cls.restrictions().items():
            if rest in poss and reqs[0] not in active and reqs[1] not in active:
                poss.remove(rest)
        if cls.ROTATOR not in active and cls.STACKER not in active:
            # cutter and swapper without rotator or stacker is a bad combination
            if cls.SWAPPER in poss and cls.CUTTER in active:
                poss.remove(cls.SWAPPER)
            if cls.CUTTER in poss and cls.SWAPPER in active:
                poss.remove(cls.CUTTER)
        # if cls.STACKER in poss:
        #     poss.extend([cls.STACKER] * (len(poss) // 4))
        active.append(random.choice(poss))

    @classmethod
    def add_restricted_previous(cls, random: Random, active: list[Self], possible: list[Self] | None) -> bool:
        # Only intended for adding something before rotator/mixer/crystallizer
        # Assumes that there is at least one required processor possible
        active: list[Processor]
        for rest, reqs in cls.restrictions().items():
            if active[0] == rest:
                if reqs[1] not in possible:
                    active.insert(0, reqs[0])
                elif reqs[0] not in possible:
                    active.insert(0, reqs[1])
                else:
                    active.insert(0, random.choice(reqs))
                return True
        return False


class ShapeBuilder:

    def __init__(self, processors: list[Processor], tasked: list[bool]):
        self.shape: list[str] = []
        self.processors = processors
        self.tasked = tasked
        self.has_crystals = False
        self.blueprint: list[tuple[int, bool, dict[str, str | Sequence[str] | int]]] = []
        self.cached_tasks: list[list[bool]] = []
        # blueprint data naming conventions:
        #   part = "Cu"
        #   shape = "C"
        #   color = "u"
        #   parts = ("Cu", "Rr", ...)
        #   ordered = ["Cu", "Cu", "Cu", "Cu"] | ["C", "C", "C", "C"] | ["u", "u", "u", "u"]
        #   layer = "CuCuCuCu"
        #   subvariant = 1

    def build(self) -> str:
        return ":".join(self.shape)

    def debug_string(self) -> str:
        return (f"[shape = {self.shape}, processors = {self.processors}, tasked = {self.tasked}, "
                f"blueprint = {self.blueprint}]")

    def __contains__(self, item):
        return item in self.processors

    def has_all(self, *items: Processor) -> bool:
        return all(item in self.processors for item in items)

    def has_any(self, *items: Processor) -> bool:
        return any(item in self.processors for item in items)

    def calc_required_complexity(self) -> int:
        if self.tasked[Processor.PIN_PUSHER]:
            return 0
        required_complexity = sum(self.tasked)
        if self.tasked[Processor.STACKER] and not (self.tasked[Processor.CUTTER] and self.tasked[Processor.ROTATOR]):
            required_complexity -= 1
        if self.tasked[Processor.ROTATOR] and not (self.tasked[Processor.CUTTER] or self.tasked[Processor.SWAPPER]):
            required_complexity += 1
        if (
            self.tasked[Processor.CRYSTALLIZER] and Processor.PIN_PUSHER not in self and
            not self.tasked[Processor.CUTTER]
        ):
            required_complexity += 1
        if self.tasked[Processor.MIXER] and not (self.tasked[Processor.PAINTER] or self.tasked[Processor.CRYSTALLIZER]):
            required_complexity += 1
        return required_complexity


event_by_processor: dict[Processor, str] = {
    Processor.CUTTER: "[PROCESSOR] Cutter",
    Processor.ROTATOR: "[PROCESSOR] Rotator",
    Processor.STACKER: "[PROCESSOR] Stacker",
    Processor.PAINTER: "[PROCESSOR] Painter",
    Processor.MIXER: "[PROCESSOR] Mixer",
    Processor.PIN_PUSHER: "[PROCESSOR] Pin Pusher",
    Processor.CRYSTALLIZER: "[PROCESSOR] Crystallizer",
    Processor.SWAPPER: "[PROCESSOR] Swapper",
}
