from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any, ClassVar

from test.param import classvar_matrix

from .bases import NoStepHK, StateVarSetup


class ExcludeMixin:
    skip_handler: ClassVar[dict[str, bool]]

    def test_create_vars(self):
        for key, skip in self.skip_handler.items():
            with self.subTest(key=key, skip=skip):
                handler = self.get_handler(key)
                exclude_this = handler.can_exclude(self.world.options)
                self.assertEqual(exclude_this, skip)


class TestExcludeByOptionAllOn(ExcludeMixin, NoStepHK, StateVarSetup):
    options: ClassVar[dict[str, Any]] = {
        "ShadeSkips": True,
        "ShriekPogos": True,
        "Slopeballs": True,
        "DifficultSkips": True,
    }
    skip_handler: ClassVar[dict[str, bool]] = {
        "$SHADESKIP": False,
        "$SHRIEKPOGO": False,
        "$SHRIEKPOGO[4]": False,
        "$SHRIEKPOGO[3,1]": False,
        "$SLOPEBALL": False,
    }


class TestExcludeByOptionNoDifficult(NoStepHK, StateVarSetup):
    options: ClassVar[dict[str, Any]] = {
        "ShadeSkips": True,
        "ShriekPogos": True,
        "Slopeballs": True,
        "DifficultSkips": False,
    }
    skip_handler: ClassVar[dict[str, bool]] = {
        "$SHADESKIP": False,
        "$SHRIEKPOGO": False,
        "$SHRIEKPOGO[4]": True,
        "$SHRIEKPOGO[3,1]": True,
        "$SLOPEBALL": False,
    }


class TestExcludeByOptionAllOff(NoStepHK, StateVarSetup):
    options: ClassVar[dict[str, Any]] = {
        "ShadeSkips": False,
        "ShriekPogos": False,
        "Slopeballs": False,
        "DifficultSkips": True,
    }
    skip_handler: ClassVar[dict[str, bool]] = {
        "$SHADESKIP": True,
        "$SHRIEKPOGO": True,
        "$SHRIEKPOGO[4]": True,
        "$SHRIEKPOGO[3,1]": True,
        "$SLOPEBALL": True,
    }


@dataclass
class Inputs:
    key: str | None = None
    resource: dict[str, int] = field(default_factory=dict)
    cs: dict[str, int] = field(default_factory=dict)
    prep_vars: Iterable[str] = ()
    assert_empty: bool = False
    notches: int | None = None
    masks: int | None = None


ers = {"NOPASSEDCHARMEQUIP": 0, "NOFLOWER": 0}  # Empty Resource State

shrogo = {"Monarch_Wings": 1, "Abyss_Shriek": 2}
slobo = {"Vengeful_Spirit": 1}

input_matrix = [
    Inputs("$CASTSPELL[3]"),
    Inputs("$CASTSPELL[3]", prep_vars=("$SHADESKIP",), assert_empty=True),
    Inputs("$CASTSPELL[4]", cs={"Vessel_Fragment": 3}, assert_empty=True),
    Inputs("$CASTSPELL[4]", resource={"NOPASSEDCHARMEQUIP": 0}, cs={"Spell_Twister": 1}, notches=6),
    Inputs("$CASTSPELL[3,1]", cs={"Vessel_Fragment": 3}),

    Inputs("$LIFEBLOOD", resource=ers, assert_empty=True),
    *[Inputs("$LIFEBLOOD", resource=ers, cs={charm: 1}, notches=4)
      for charm in ("Lifeblood_Heart", "Lifeblood_Core", "Joni's_Blessing")],

    Inputs("$SHADESKIP", resource={"USEDSHADE": 1}, assert_empty=True),
    Inputs("$SHADESKIP", resource={"CHARM36": 3}, assert_empty=True),
    Inputs("$SHADESKIP", resource={"REQUIREDMAXSOUL": 67}, assert_empty=True),
    Inputs("$SHADESKIP", prep_vars=("$CASTSPELL[2]",)),
    Inputs("$SHADESKIP", prep_vars=("$CASTSPELL[3]",), assert_empty=True),
    Inputs("$SHADESKIP"),
    Inputs("$SHADESKIP[2HITS]", masks=4, assert_empty=True),
    Inputs("$SHADESKIP[2HITS]", masks=16),
    Inputs("$SHADESKIP[2HITS]", masks=8, notches=6, resource={"NOPASSEDCHARMEQUIP": 0},
           cs={"Can_Repair_Fragile_Charms": 1, "Fragile_Heart": 1}),
    Inputs("$SHADESKIP[2HITS]", masks=8, notches=6, resource={"NOPASSEDCHARMEQUIP": 0},
           cs={"Unbreakable_Heart": 1, "Fragile_Heart": 1}),
    Inputs("$SHADESKIP[2HITS]", resource={"BROKEHEART": 1, "NOPASSEDCHARMEQUIP": 0}, masks=8, notches=6,
           cs={"Can_Repair_Fragile_Charms": 1, "Fragile_Heart": 1}, assert_empty=True),

    Inputs("$SHRIEKPOGO", assert_empty=True),
    Inputs("$SHRIEKPOGO", assert_empty=True, cs={"Monarch_Wings": 1}),
    Inputs("$SHRIEKPOGO", assert_empty=True, cs={"Abyss_Shriek": 2}),

    Inputs("$SHRIEKPOGO[3]",   cs=shrogo),
    Inputs("$SHRIEKPOGO[4]",   cs=shrogo, assert_empty=True),
    Inputs("$SHRIEKPOGO[4]",   cs={**shrogo, "Spell_Twister": 1}, resource=ers, notches=6),
    Inputs("$SHRIEKPOGO[4]",   cs={**shrogo, "Vessel_Fragment": 3}, assert_empty=True),
    Inputs("$SHRIEKPOGO[3,1]", cs={**shrogo, "Vessel_Fragment": 3}),
    Inputs("$SHRIEKPOGO[4]",   cs={**shrogo, "Vessel_Fragment": 3, "Mothwing_Cloak": 1}),

    Inputs("$SLOPEBALL", assert_empty=True),
    Inputs("$SLOPEBALL", assert_empty=True, cs=slobo, resource={"SPENTSOUL": 99}),
    Inputs("$SLOPEBALL", cs=slobo),

    Inputs("$TAKEDAMAGE", assert_empty=True,  masks=4),
    Inputs("$TAKEDAMAGE", assert_empty=False, masks=8),
]


@classvar_matrix(matrix_index=range(len(input_matrix)))
class TestStateVars(StateVarSetup, NoStepHK):
    matrix_index: int
    assert_empty: bool

    def setUp(self):
        super().setUp()
        matrix_vars = input_matrix[self.matrix_index]
        self.key = matrix_vars.key
        self.resource = matrix_vars.resource
        self.cs = matrix_vars.cs
        self.prep_vars = matrix_vars.prep_vars
        self.notch_override = matrix_vars.notches
        self.mask_override = matrix_vars.masks

        self.assert_empty = matrix_vars.assert_empty

    def test_output(self):
        outputs = self.get_modified_state()
        if self.assert_empty:
            self.assertFalse(outputs, "Expected to not be in logic but was")
        else:
            self.assertTrue(outputs, "Expected to be in logic but was not")
