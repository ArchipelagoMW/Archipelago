import os
import zipfile
from typing import TYPE_CHECKING, Any
from orjson import orjson

import Utils
from worlds.Files import APPlayerContainer

if TYPE_CHECKING:
    from . import Shapez2World


class Shapez2ScenarioContainer(APPlayerContainer):
    game = "shapez 2"
    patch_file_ending = ".zip"

    def __init__(self, world: "Shapez2World", output_directory: str):
        self.world = world
        mw = world.multiworld
        container_path = os.path.join(
            output_directory,
            f"AP-{mw.seed_name}-P{world.player}-{mw.get_file_safe_player_name(world.player)}_{Utils.__version__}.zip"
        )
        super().__init__(path=container_path, player=world.player, player_name=world.player_name, server="")

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        from .generate.files import (example_shapes, blueprint, milestones, tasks, upgrades, operator_lines,
                                     mechanics, starting_location, debug, preset)
        super().write_contents(opened_zipfile)

        scenario_id = self.world.multiworld.get_out_file_name_base(self.player)
        mechanic_definitions = mechanics.get_mechanic_definitions(self)
        other_players_items: set[str] = set()  # ONLY FOR LOOKUP!!!
        scenario: dict[str, Any] = {
            "FormatVersion": 2,
            "GameVersion": 1058,
            "UniqueId": scenario_id,
            "SupportedGameModes": ["RegularGameMode"],
            "NextScenarios": [],
            "ExampleShapes": example_shapes.get_example_shapes(self),
            "Title": f"Archipelago ({self.player_name})",
            "Description": f"Scenario for player {self.player_name} from the multiworld "
                           f"with seed {self.world.multiworld.seed_name}.",
            "PreviewImageId": "Scenario_Regular",
            "ResearchConfig": {
                "BaseChunkLimitMultiplier": 200,
                "BaseBlueprintRewardMultiplier": 500,
                "MaxShapeLayers": self.world.options.shape_generation_adjustments["Maximum layers"],
                "ShapesConfigurationId": ("DefaultShapesQuadConfiguration"
                                          if self.world.options.shape_configuration == "tetragonal"
                                          else "DefaultShapesHexagonalConfiguration"),
                "ColorSchemeConfigurationId": "DefaultColorSchemeRGBFlex",
                "ResearchLevelsAreProgressive": True,
                "BlueprintCurrencyShapes": blueprint.get_blueprint_shapes(self),
                "IntroductionWikiEntryId": "WKWelcome",
                "InitiallyUnlockedUpgrades": ["RNInitial", *upgrades.milestone_ids],
                "TutorialConfig": "TCNoTutorial"
            },
            "Progression": {
                "Levels": {"Levels": milestones.get_milestones(self, mechanic_definitions, other_players_items)},
                "SideQuestGroups": {"SideQuestGroups": tasks.get_task_lines(self, mechanic_definitions,
                                                                            other_players_items)},
                "SideUpgrades": {
                    "UpgradeCategories": ["ProcessingSpeeds","Buildings","Platforms","Trains","Wires",
                                          "Decorations","Other"],
                    "SideUpgrades": upgrades.get_remote_upgrades(self)
                },
                "LinearUpgrades": {
                    "HubInputSizeUpgradeId": "LRUHubInputSize",
                    "ShapeQuantityUpgradeId": "LRUShapeQuantity",
                    "SpeedsToLinearUpgradeMappings": {
                        "BeltSpeed": "LRUBeltSpeed",
                        "CutterSpeed": "LRUCuttingSpeed",
                        "StackerSpeed": "LRUStackingSpeed",
                        "PainterSpeed": "LRUPaintingSpeed",
                        "TrainSpeed": "LRUTrainSpeed",
                        "TrainCapacity": "LRUTrainCapacity"
                    },
                    "LinearUpgrades": upgrades.linear_upgrades
                }
            },
            "StartingLocation": {
                "InitialViewport": {
                    "PositionY": -11.56,
                    "Zoom": 480.0,
                    "Angle": 70.0,
                    "ShowAllBuildingLayers": True,
                    "ShowAllIslandLayers": True
                },
                "InitialIslands": {"InitialIslands": [{"Position_GC": {"x": -1}, "LayoutId": "Layout_HUB"}]},
                "FixedPatches": {"FixedPatches": starting_location.get_fixed_patches(self)},
                "StartingChunks": {"StartingChunks": []}
            },
            "PlayerLevelConfig": {
                "IconicLevelShapes": {"LevelShapes": example_shapes.get_iconic_shapes(self)},
                "IconicLevelShapeInterval": 1,
                "GoalLines": operator_lines.get_operator_lines(self),
                "Rewards": operator_lines.get_operator_rewards(self, mechanic_definitions, other_players_items)
            },
            "Mechanics": {
                "Mechanics": mechanic_definitions,
                "BuildingLayerMechanicIds": ["RULayer2", "RULayer3"],
                "IslandLayerMechanicIds": ["RUIslandLayer2", "RUIslandLayer3"],
                "IslandLayersUnlockOrder": [-1, 1],
                "BlueprintsMechanicId": "RUBlueprints",
                "RailsMechanicId": "RUTrains",
                "IslandManagementMechanicId": "RUIslandPlacement",
                "PlayerLevelMechanicId": "RUPlayerLevel",
                "TrainHubDeliveryMechanicId": "RUTrainHubDelivery"
            },
            "ConvertersConfig": {"Configs": {}},
            "ResearchStationConfig": {"Recipes": {}},
            "RailColorsConfig": {
                "RailColors": [
                    {"Id": {"RailColorId": "Blue"}, "Tint": "197FE5"},
                    {"Id": {"RailColorId": "Green"}, "Tint": "19E566"},
                    {"Id": {"RailColorId": "Red"}, "Tint": "F43F3F"},
                    {"Id": {"RailColorId": "White"}, "Tint": "EAEAEA"},
                    {"Id": {"RailColorId": "Cyan"}, "Tint": "19E5EA"},
                    {"Id": {"RailColorId": "Magenta"}, "Tint": "EA19EA"},
                    {"Id": {"RailColorId": "Yellow"}, "Tint": "EAEA19"}
                ]
            },
            "ToolbarConfig": "#include_raw:Scenarios/Shared/Toolbar/ToolbarConfig"
        }
        scenario_preset: dict[str, Any] = {
          "Version": "1",
          "UniqueId": scenario_id + "_preset",
          "Title": "@scenario-preset.default.title",
          "Description": "@scenario-preset.default.description",
          "Parameters": {
            "ScenarioId": scenario_id,
            "MapGenerationParameters": preset.map_generation_params,
            "GameRuleParameters": {"RuleIds": []}
          }
        }
        scenario_json: bytes = orjson.dumps(scenario)
        position = scenario_json.find(b"\"FormatVersion\":2,")
        if position != -1:
            scenario_json = scenario_json[:position] + b"\"FormatVersion\": 2," + scenario_json[position+18:]
        opened_zipfile.writestr("scenario_" + scenario_id + ".json", scenario_json)
        opened_zipfile.writestr("preset_" + scenario_id + ".json", orjson.dumps(scenario_preset))
        opened_zipfile.writestr("shapes_debug.txt", debug.write_shapes_debug(self))
