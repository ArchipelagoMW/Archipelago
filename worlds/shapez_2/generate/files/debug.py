from ...output import Shapez2ScenarioContainer


def write_shapes_debug(container: "Shapez2ScenarioContainer") -> str:

    out = ["##############",
           "# Milestones #",
           "##############",
           ""]

    for i in range(container.world.options.location_adjustments["Milestones"]):
        shapes_1, shapes_2 = container.world.milestone_shapes[i]
        processors = container.world.milestone_processors[i]
        out.extend([f"# Milestone {i+1}:",
                    "[" + ', '.join(p.name for p in processors) + "]",
                    *shapes_1,
                    *shapes_2,
                    ""])

    out.extend(["##############",
                "# Task lines #",
                "##############",
                ""])

    for i in range(container.world.options.location_adjustments["Task lines"]):
        shapes = container.world.task_shapes[i]
        processors = container.world.task_processors[i]
        out.extend([f"# Task line {i+1}:",
                    "[" + ', '.join(p.name for p in processors) + "]",
                    *shapes,
                    ""])

    out.extend(["##################",
                "# Operator lines #",
                "##################",
                ""])

    for i in range(container.world.options.location_adjustments["Operator lines"]):
        shape = container.world.operator_shapes[i]
        if isinstance(shape, str):
            processors = container.world.operator_processors[i]
            out.extend([f"# Operator line {i+1}:",
                        "[" + ', '.join(p.name for p in processors) + "]",
                        shape,
                        ""])

    return "\n".join(out)
