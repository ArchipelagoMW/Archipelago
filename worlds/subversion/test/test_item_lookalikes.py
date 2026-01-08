from typing import Dict
from BaseClasses import MultiWorld

from worlds.sm import SMWorld
from worlds.smz3 import SMZ3World
from worlds.subversion import patch_utils


def test_sm_names() -> None:
    """ other games changing item names """
    _SM_name_to_subversion_name: Dict[str, str] = getattr(patch_utils, "_SM_name_to_subversion_name")
    for item_name in _SM_name_to_subversion_name.keys():
        assert item_name in SMWorld.item_name_to_id, f"{item_name} not in SMWorld.item_name_to_id"


def test_smz3_names() -> None:
    """ other games changing item names """
    _SMZ3_name_to_SM_name: Dict[str, str] = getattr(patch_utils, "_SMZ3_name_to_SM_name")
    _SM_name_to_subversion_name: Dict[str, str] = getattr(patch_utils, "_SM_name_to_subversion_name")

    for smz3_item_name, sm_item_name in _SMZ3_name_to_SM_name.items():
        assert smz3_item_name in SMZ3World.item_name_to_id, f"{smz3_item_name} not in SMZ3World.item_name_to_id"
        assert sm_item_name in _SM_name_to_subversion_name


def test_smz3_game_name() -> None:
    """ because we test for this to display item sprites """
    smz3 = SMZ3World(MultiWorld(1), 1)
    smz3_item = smz3.create_item("Missile")
    assert patch_utils.SMZ3_ITEM_GAME_NAME == smz3_item.game, f"{patch_utils.SMZ3_ITEM_GAME_NAME=} {smz3_item.game=}"


def test_sm_game_name() -> None:
    """ because we test for this to display item sprites """
    sm = SMWorld(MultiWorld(1), 1)
    sm_item = sm.create_item("Missile")
    assert patch_utils.SM_ITEM_GAME_NAME == sm_item.game, f"{patch_utils.SM_ITEM_GAME_NAME=} {sm_item.game}"
