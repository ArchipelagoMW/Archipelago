from ...output import Shapez2ScenarioContainer


def get_blueprint_shapes(container: "Shapez2ScenarioContainer") -> list[dict[str, str | list[str] | int]]:
    points = container.world.blueprint_points
    shapes = container.world.blueprint_shapes
    out = []
    for num in range(len(shapes)):
        out.append({
            "Shape": shapes[num],
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [],
            "Amount": points[num]
        })
    return out
