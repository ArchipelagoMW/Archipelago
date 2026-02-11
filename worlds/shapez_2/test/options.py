from test.bases import WorldTestBase


class Shapez2TestBase(WorldTestBase):
    game = "shapez 2"


class TestDefault(Shapez2TestBase):
    options = {"goal": "milestones"}


class TestGoalOperatorLevels(Shapez2TestBase):
    options = {"goal": "operator_levels", "location_adjustments": {"Operator level checks": 10}}


class Test3Milestones(Shapez2TestBase):
    options = {"location_adjustments": {
        "Milestones": 3,
        "Task lines": 40,
    }}


class TestLockTaskLines(Shapez2TestBase):
    options = {"location_modifiers": ["Lock task lines"]}


class TestLockOperatorTab(Shapez2TestBase):
    options = {"location_modifiers": ["Lock operator levels tab"]}


class TestLockAll(Shapez2TestBase):
    options = {"location_modifiers": ["Lock task lines", "Lock operator lines", "Lock operator levels tab"]}


class TestMinimumTasksWithOperatorChecks(Shapez2TestBase):
    options = {"location_adjustments": {
        "Minimum checks per task line": 1,
        "Maximum checks per task line": 1,
        "Operator level checks": 50,
    }}


class TestSomeStartingResearchAndBlueprintPoints(Shapez2TestBase):
    options = {"location_adjustments": {
        "Starting research points": 10,
        "Starting blueprint points": 1000,
    }}


class TestNoMilestoneOperatorLines(Shapez2TestBase):
    options = {"shape_generation_modifiers": []}


class Test2Layers(Shapez2TestBase):
    options = {"shape_generation_adjustments": {"Maximum layers": 2}}


class Test10LayersWithMaximumProcessorMilestones(Shapez2TestBase):
    options = {"shape_generation_adjustments": {"Maximum layers": 10, "Maximum processors per milestone": 8}}


class TestBlueprintRandomized(Shapez2TestBase):
    options = {"blueprint_shapes": "randomized"}


class TestBlueprintPlando(Shapez2TestBase):
    options = {"blueprint_shapes": ["CuCuCuCu", "crcrcrcr:SbSbSbSb", "WuWu----"]}


class TestOnlyArbitraryPointsItems(Shapez2TestBase):
    options = {"item_pool_modifiers": [
        "Arbitrary research points",
        "Arbitrary platform items",
        "Arbitrary blueprint points",
        "Include blueprint points",
    ]}
