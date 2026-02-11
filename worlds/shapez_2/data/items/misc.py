
from .. import ItemData, PointsItemData
from ..classification import *

task_lines: dict[str, ItemData] = {
    f"Task line #{i}": ItemData(3000+i, always_progression_deprioritized, f"RemoteTaskLine{i}", (f"TaskLine{i}", ), 2)
    for i in range(1, 201)
}

operator_lines: dict[str, ItemData] = {
    f"Operator line #{i}": ItemData(4000+i, always_progression_deprioritized, f"RemoteOperatorLine{i}",
                                    (f"OperatorLine{i}", ), 2)
    for i in range(1, 101)
}

research_points: dict[str, PointsItemData] = {
    f"{i} Research Points": PointsItemData(5000+i, always_filler, i, 5)
    for i in range(1, 101)
}

platforms: dict[str, PointsItemData] = {
    f"{i} Platforms": PointsItemData(6000+i, always_filler, i, 3)
    for i in range(1, 1000)
}

blueprint_points: dict[str, PointsItemData] = {
    f"{i*100} Blueprint Points": PointsItemData(7000+i, always_filler, i*100, 4)
    for i in range(1, 101)
}
