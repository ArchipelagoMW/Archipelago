from typing import Any

from ...output import Shapez2ScenarioContainer
from ...data import ItemData
from ...data.items import buildings, island_buildings, mechanics, misc

tabs: tuple[tuple[tuple[str, str], tuple[dict[str, ItemData], ...]], ...] = (
    (("BuildingReward", "BuildingDefinitionGroupId"), (buildings.always, buildings.starting,
                                                       buildings.simple_processors, buildings.sandbox)),
    (("IslandGroupReward", "GroupId"), (island_buildings.always, island_buildings.starting, island_buildings.miners)),
    (("MechanicReward", "MechanicId"), (mechanics.always, mechanics.starting, mechanics.special,
                                        misc.task_lines, misc.operator_lines)),
)

milestone_ids: tuple[str, ...] = ("RNStackerLayer2", "RNBlueprints", "RNIslandBuilding", "RNFluids",
                                  "RNTrains", "RNPinPusher", "RNColorMixing", "RNIslandLayer3",
                                  "RNCrystals", "RNEndOfGame", "RNWireBasics")


def get_remote_upgrades(container: "Shapez2ScenarioContainer") -> list[dict[str, Any]]:

    reward_type, tables = container.world.random.choice(tabs)
    table = container.world.random.choice(tables)
    surprise_item, data = container.world.random.choice(tuple(table.items()))
    out = [{
        "Id": "RNSurprise",
        "PreviewImageId": "Shop_PlatformLayouts4",
        "Title": "Surprise out-of-logic item",
        "Description": "Rewards you with a random building, island platform, or mechanic "
                       "without being taken into account by logic.",
        "Category": "Other",
        "RequiredUpgradeIds": [],
        "RequiredMechanicIds": [],
        "Rewards": [{"$type": reward_type[0], reward_type[1]: reward}
                    for reward in data.reward_ids],
        "Costs": [{"$type": "ResearchPointsCost", "Amount": 100}]
    }]

    for vanilla in milestone_ids:
        out.append({
            "Id": vanilla,
            "PreviewImageId": "",
            "Title": vanilla,
            "Description": "",
            "Hidden": True,
            "Category": "Other",
            "RequiredUpgradeIds": [],
            "RequiredMechanicIds": [],
            "Rewards": [],
            "Costs": [{"$type": "ResearchPointsCost", "Amount": 1}]
        })

    for reward_type, tables in tabs:
        for table in tables:
            for name, data in table.items():
                out.append({
                    "Id": data.remote_id,
                    "PreviewImageId": "",
                    "Title": name,
                    "Description": "",
                    "Hidden": True,
                    "Category": "Other",
                    "RequiredUpgradeIds": [],
                    "RequiredMechanicIds": [],
                    "Rewards": [{"$type": reward_type[0], reward_type[1]: reward}
                                for reward in data.reward_ids],
                    "Costs": [{"$type": "ResearchPointsCost", "Amount": 1}]
                })

    return out


linear_upgrades: list[dict[str, Any]] = [
    {
        "Id":"LRUBeltSpeed",
        "Title":"@research.LRUBeltSpeed.title",
        "DisplayType":1,
        "Levels":[
            {"Value":50},
            {"Value":75,"Cost":{"$type":"ResearchPointsCost","Amount":2}},
            {"Value":100,"Cost":{"$type":"ResearchPointsCost","Amount":7}},
            {"Value":125,"Cost":{"$type":"ResearchPointsCost","Amount":20}},
            {"Value":150,"Cost":{"$type":"ResearchPointsCost","Amount":50}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"ProcessingSpeeds"
    },
    {
        "Id":"LRUCuttingSpeed",
        "Title":"@research.LRUCuttingSpeed.title",
        "DisplayType":1,
        "Levels":[
            {"Value":50},
            {"Value":75,"Cost":{"$type":"ResearchPointsCost","Amount":2}},
            {"Value":100,"Cost":{"$type":"ResearchPointsCost","Amount":7}},
            {"Value":125,"Cost":{"$type":"ResearchPointsCost","Amount":20}},
            {"Value":150,"Cost":{"$type":"ResearchPointsCost","Amount":50}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"ProcessingSpeeds"
    },
    {
        "Id":"LRUStackingSpeed",
        "Title":"@research.LRUStackingSpeed.title",
        "DisplayType":1,
        "Levels":[
            {"Value":50},
            {"Value":75,"Cost":{"$type":"ResearchPointsCost","Amount":2}},
            {"Value":100,"Cost":{"$type":"ResearchPointsCost","Amount":7}},
            {"Value":125,"Cost":{"$type":"ResearchPointsCost","Amount":20}},
            {"Value":150,"Cost":{"$type":"ResearchPointsCost","Amount":50}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"ProcessingSpeeds"
    },
    {
        "Id":"LRUHubInputSize",
        "Title":"@research.LRUHubInputSize.title",
        "DisplayType":3,
        "Levels":[
            {"Value":4},
            {"Value":6,"Cost":{"$type":"ResearchPointsCost","Amount":3}},
            {"Value":8,"Cost":{"$type":"ResearchPointsCost","Amount":7}},
            {"Value":10,"Cost":{"$type":"ResearchPointsCost","Amount":15}},
            {"Value":12,"Cost":{"$type":"ResearchPointsCost","Amount":30}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Other"
    },
    {
        "Id":"LRUPaintingSpeed",
        "Title":"@research.LRUPaintingSpeed.title",
        "DisplayType":1,
        "Levels":[
            {"Value":100},
            {"Value":125,"Cost":{"$type":"ResearchPointsCost","Amount":12}},
            {"Value":150,"Cost":{"$type":"ResearchPointsCost","Amount":30}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"ProcessingSpeeds"
    },
    {
        "Id":"LRUTrainSpeed",
        "Title":"@research.LRUTrainSpeed.title",
        "DisplayType":2,
        "Levels":[
            {"Value":100},
            {"Value":140,"Cost":{"$type":"ResearchPointsCost","Amount":8}},
            {"Value":180,"Cost":{"$type":"ResearchPointsCost","Amount":12}},
            {"Value":200,"Cost":{"$type":"ResearchPointsCost","Amount":30}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Trains"
    },
    {
        "Id":"LRUTrainCapacity",
        "Title":"@research.LRUTrainCapacity.title",
        "DisplayType":4,
        "Levels":[
            {"Value":100},
            {"Value":200,"Cost":{"$type":"ResearchPointsCost","Amount":8}},
            {"Value":300,"Cost":{"$type":"ResearchPointsCost","Amount":12}},
            {"Value":400,"Cost":{"$type":"ResearchPointsCost","Amount":18}},
            {"Value":500,"Cost":{"$type":"ResearchPointsCost","Amount":30}},
            {"Value":600,"Cost":{"$type":"ResearchPointsCost","Amount":50}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Trains"
    },
    {
        "Id":"LRUShapeQuantity",
        "Title":"@research.LRUShapeQuantity.title",
        "DisplayType":3,
        "Levels":[
            {"Value":1},
            {"Value":2,"Cost":{"$type":"ResearchPointsCost","Amount":350}},
            {"Value":3,"Cost":{"$type":"ResearchPointsCost","Amount":750}},
            {"Value":4,"Cost":{"$type":"ResearchPointsCost","Amount":1250}},
            {"Value":5,"Cost":{"$type":"ResearchPointsCost","Amount":1750}},
            {"Value":6,"Cost":{"$type":"ResearchPointsCost","Amount":3500}},
            {"Value":7,"Cost":{"$type":"ResearchPointsCost","Amount":4000}},
            {"Value":8,"Cost":{"$type":"ResearchPointsCost","Amount":4500}},
            {"Value":9,"Cost":{"$type":"ResearchPointsCost","Amount":5000}},
            {"Value":10,"Cost":{"$type":"ResearchPointsCost","Amount":5500}},
            {"Value":11,"Cost":{"$type":"ResearchPointsCost","Amount":6000}},
            {"Value":12,"Cost":{"$type":"ResearchPointsCost","Amount":9999}}
        ],
        "RequiredUpgradeIds":[],
        "RequiredMechanicIds":[],
        "Category":"Other"
    }
]
