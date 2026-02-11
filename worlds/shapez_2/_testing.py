from io import StringIO
from random import Random


class ConsoleWriter(StringIO):

    def write(self, __s):
        # print(__s)
        pass


def test(write: bool, layers: int, hexagonal: bool, count: int, enable_downgrades: bool):
    if write:
        writer = open("generate/shapes/_temp/output.txt", "wt")
    else:
        writer = ConsoleWriter()
    with writer as file:
        if __name__ == "__main__":
            from generate.shapes import generator, downgrade_tetragonal, Processor
            from generate.shapes.generate_tetragonal import Variant
        else:
            from .generate.shapes import generator, downgrade_tetragonal, Processor
            from .generate.shapes.generate_tetragonal import Variant
        import datetime
        start_time = datetime.datetime.utcnow()
        file.write(
            "This file contains randomly generated shapes, with expected requirements and downgrades.\n"
            "You can view them either ingame (clicking any shape in the gui opens the shape viewer) or at "
            "https://shapez.soren.codes/shape by copy-pasting the shape code.\n"
            "The processors' names should be self-explanatory, but do note that the \"cutter\" here is actually "
            "supposed to be the half destroyer.\n"
            "Also, a shape's \"complexity\" is the number of operations needed to create it (i.e. a "
            "half circle needs 1 complexity, a single part needs 3 complexity (cut-rotate-cut), etc.).\n"
            "You can ignore the \"Layer data\" part in every shape; it's advanced data for debugging.\n\n"
            "What I'm asking you to do is to test the quality of the generated shapes. "
            "What I mean by \"quality of a shape\" is whether\n"
            "- it is doable at all,\n"
            "- it is doable with only the processors you're supposed to have,\n"
            "- it is only doable with those processors (i.e. not out-of-logic doable),\n"
            "- it is appropriate for the given complexity,\n"
            "- it looks nice and not awful (at least most of the time), and\n"
            "- it doesn't look too repetitive over time.\n\n"
            "Notes regarding combinations of processors:\n"
            "There are 3 processors that each require one of two other processors in order to do anything:\n"
            "- The rotator requires either the cutter or the swapper.\n"
            "- The mixer requires either the painter or the crystallizer.\n"
            "- The crystallizer requires either the cutter or the pin pusher.\n\n"
            "General settings/data for this generation:\n"
            f"Maximum layer count: {layers}\n"
            f"Is hexagonal?: {hexagonal}\n"
            f"Generated shapes count: {count}\n"
            f"Enable downgrades: {enable_downgrades}\n"
            f"Begin crystals variant number: {Variant.begin_crystals}\n"
            f"End crystals variant number: {Variant.end_crystals}\n"
            f"Generation date and time: {start_time}\n\n"
            "----------------------------------------------------------------------------------------\n\n"
        )
        rand = Random()
        for i in range(count):
            proc: list[Processor] = []
            for _ in range(rand.randint(1, min(8, i // 2 + 1))):
                Processor.add_random_next(rand, proc, None)
            complexity = rand.randint(len(proc) + 2, 10 + i * 2)
            builder = generator.generate_new(rand, proc, complexity, hexagonal, layers)
            shape = builder.build()
            file.write(f"Shape #{i+1}:   {shape}\n"
                       f"Parameters: Complexity: {complexity}\n"
                       f"            Required processors: [{', '.join(p.name for p in proc)}]\n"
                       f"Layer data ({len(builder.blueprint)}): "
                       f"[{', '.join(str(l) for l in builder.blueprint)}]\n"
                       f"Cached tasks: [")
            for cached in builder.cached_tasks:
                file.write("".join(str(int(b)) for b in cached) + ", ")
            file.write("]\n")
            downgrades = rand.randint(1, min(len(proc), i // 2 + 1)) if enable_downgrades else 0
            for _ in range(downgrades):
                missing = proc.pop()
                builder = downgrade_tetragonal.downgrade_4(rand, builder, proc, missing, complexity)
                down_shape = builder.build()
                tries = 0
                while shape == down_shape:
                    brek = False
                    if not proc or tries > 2:
                        brek = True
                    if not brek and missing in Processor.restrictions():
                        needed = Processor.restrictions()[missing]
                        if proc[-1] in needed:
                            brek = True
                        else:
                            file.write(f"  - Downgraded shape identical, putting {missing.name} one down "
                                       f"(try #{tries+1})\n")
                            proc.insert(-1, missing)
                            missing = proc.pop()
                            builder = downgrade_tetragonal.downgrade_4(rand, builder, proc, missing, complexity)
                            down_shape = builder.build()
                            tries += 1
                            continue
                    if brek:
                        file.write(f"  - Downgraded shape identical, but {missing.name} "
                                   f"could not be placed one below or at bottom\n")
                        break
                    file.write(f"  - Downgraded shape identical, putting {missing.name} at bottom (try #{tries+1})\n")
                    proc.insert(0, missing)
                    missing = proc.pop()
                    builder = downgrade_tetragonal.downgrade_4(rand, builder, proc, missing, complexity)
                    down_shape = builder.build()
                    tries += 1
                shape = down_shape
                file.write(f"  - Removing {missing.name}:\n"
                           f"    {builder.build()}\n"
                           f"    Layer data ({len(builder.blueprint)}): "
                           f"[{', '.join(str(l) for l in builder.blueprint)}]\n")
            file.write("\n\n")
        end_time = datetime.datetime.utcnow()
        end_message = (f"Generation start: {start_time}\n"
                       f"Generation end: {end_time}\n"
                       f"Duration: {end_time - start_time}\n")
        file.write(f"-------------------------------------------------------------\n\n" + end_message)
        print(end_message)


if __name__ == "__main__":
    test(True, 4, False, 1000, True)
