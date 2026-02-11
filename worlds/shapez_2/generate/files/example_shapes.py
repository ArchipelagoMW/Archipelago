from ...output import Shapez2ScenarioContainer


def get_example_shapes(container: "Shapez2ScenarioContainer") -> list[str]:
    milestones = container.world.milestone_shapes
    tasks = container.world.task_shapes
    task_processors = container.world.task_processors
    task_1, task_2, found = "CuCuCuCu", "CuCuCuCu", 0
    for count in reversed(range(6)):
        for i in reversed(range(len(task_processors))):
            if len(task_processors[i]) >= count:
                if not found:
                    task_1 = tasks[i][-1]
                    found = 1
                elif found == 1:
                    task_2 = tasks[i][-1]
                    break
        else:
            continue
        break
    return [
        milestones[-1][0][-1],
        milestones[-1][1][-1],
        task_1,
        milestones[-2][container.world.random.randint(0, 1)][-1] if len(milestones) >= 4 else task_2,
        container.world.blueprint_shapes[-1],
    ]


def get_iconic_shapes(container: "Shapez2ScenarioContainer") -> list[str]:
    # All final milestone shapes except milestones 1 and 2
    # All final task shapes with 3+ processors
    # All operator line shapes
    out = []
    milestones = container.world.milestone_shapes
    tasks = container.world.task_shapes
    task_processors = container.world.task_processors
    operator_lines = container.world.operator_shapes
    for i in range(2, len(milestones)):
        out.append(milestones[i][0][-1])
        out.append(milestones[i][1][-1])
    for i in range(len(tasks)):
        if len(task_processors[i]) >= 3:
            out.append(tasks[i][-1])
    for entry in operator_lines:
        if isinstance(entry, str):
            out.append(entry)
    return out
