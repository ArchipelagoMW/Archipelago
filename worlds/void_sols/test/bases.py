from test.bases import WorldTestBase


class VoidSolsTestBase(WorldTestBase):
    game = "Void Sols"
    options = {
        "sparks_checks": True,
        "torch_checks": True,
        "hidden_walls_checks": True,
    }
