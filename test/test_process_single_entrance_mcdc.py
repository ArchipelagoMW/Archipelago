import pytest
from worlds.lingo.utils.pickle_static_data import process_single_entrance, RoomEntrance, RoomAndDoor, EntranceType

# Mock global variables used by process_single_entrance
# These are now handled by the fixture to ensure isolation between tests

@pytest.fixture(autouse=True)
def reset_globals():
    # Temporarily store original global state
    original_painting_exit_rooms = process_single_entrance.__globals__["PAINTING_EXIT_ROOMS"]
    original_painting_entrances = process_single_entrance.__globals__["PAINTING_ENTRANCES"]

    # Reset global variables for the test
    process_single_entrance.__globals__["PAINTING_EXIT_ROOMS"] = set()
    process_single_entrance.__globals__["PAINTING_ENTRANCES"] = 0

    yield

    # Restore original global state after the test
    process_single_entrance.__globals__["PAINTING_EXIT_ROOMS"] = original_painting_exit_rooms
    process_single_entrance.__globals__["PAINTING_ENTRANCES"] = original_painting_entrances

class TestProcessSingleEntrance:

    # CT1: D1/C1.2 (F) - {"painting": False} -> NORMAL
    def test_ct1_painting_false(self):
        """CT1: Teste para D1/C1.2 (F) - door_obj["painting"] é False."""
        door_obj = {"painting": False}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL
        assert "Any" not in process_single_entrance.__globals__["PAINTING_EXIT_ROOMS"]
        assert process_single_entrance.__globals__["PAINTING_ENTRANCES"] == 0

    # CT2: D1/C1.2 (V) - {"painting": True} -> PAINTING
    def test_ct2_painting_true(self):
        """CT2: Teste para D1/C1.2 (V) - door_obj["painting"] é True."""
        door_obj = {"painting": True}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.PAINTING
        assert "Any" in process_single_entrance.__globals__["PAINTING_EXIT_ROOMS"]
        assert process_single_entrance.__globals__["PAINTING_ENTRANCES"] == 1

    # CT3: D1/C1.1 (F) - {} -> NORMAL
    def test_ct3_no_painting_key(self):
        """CT3: Teste para D1/C1.1 (F) - "painting" não está em door_obj."""
        door_obj = {}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL
        assert "Any" not in process_single_entrance.__globals__["PAINTING_EXIT_ROOMS"]
        assert process_single_entrance.__globals__["PAINTING_ENTRANCES"] == 0

    # CT4: D2/C2.2 (F) - {"sunwarp": False} -> NORMAL
    def test_ct4_sunwarp_false(self):
        """CT4: Teste para D2/C2.2 (F) - door_obj["sunwarp"] é False."""
        door_obj = {"sunwarp": False}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT5: D2/C2.2 (V) - {"sunwarp": True} -> SUNWARP
    def test_ct5_sunwarp_true(self):
        """CT5: Teste para D2/C2.2 (V) - door_obj["sunwarp"] é True."""
        door_obj = {"sunwarp": True}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.SUNWARP

    # CT6: D2/C2.1 (F) - {} -> NORMAL
    def test_ct6_no_sunwarp_key(self):
        """CT6: Teste para D2/C2.1 (F) - "sunwarp" não está em door_obj."""
        door_obj = {}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT7: D3/C3.2 (F) - {"warp": False} -> NORMAL
    def test_ct7_warp_false(self):
        """CT7: Teste para D3/C3.2 (F) - door_obj["warp"] é False."""
        door_obj = {"warp": False}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT8: D3/C3.2 (V) - {"warp": True} -> WARP
    def test_ct8_warp_true(self):
        """CT8: Teste para D3/C3.2 (V) - door_obj["warp"] é True."""
        door_obj = {"warp": True}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.WARP

    # CT9: D3/C3.1 (F) - {} -> NORMAL
    def test_ct9_no_warp_key(self):
        """CT9: Teste para D3/C3.1 (F) - "warp" não está em door_obj."""
        door_obj = {}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT10: D4/C4.1 (F) - source_room != "Crossroads" -> NORMAL
    def test_ct10_source_room_not_crossroads(self):
        """CT10: Teste para D4/C4.1 (F) - source_room não é "Crossroads"."""
        door_obj = {}
        result = process_single_entrance("Other", "Roof", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT11: D4/C4.1 (V) - source_room == "Crossroads" and room_name == "Roof" -> CROSSROADS_ROOF_ACCESS
    def test_ct11_crossroads_roof_access(self):
        """CT11: Teste para D4/C4.1 (V) - source_room é "Crossroads" e room_name é "Roof"."""
        door_obj = {}
        result = process_single_entrance("Crossroads", "Roof", door_obj)
        assert result.type == EntranceType.CROSSROADS_ROOF_ACCESS

    # CT12: D4/C4.2 (F) - room_name != "Roof" -> NORMAL
    def test_ct12_room_name_not_roof(self):
        """CT12: Teste para D4/C4.2 (F) - room_name não é "Roof"."""
        door_obj = {}
        result = process_single_entrance("Crossroads", "Other", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT13: D5/C5.2 (F) - {"static_painting": False} -> NORMAL
    def test_ct13_static_painting_false(self):
        """CT13: Teste para D5/C5.2 (F) - door_obj["static_painting"] é False."""
        door_obj = {"static_painting": False}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT14: D5/C5.2 (V) - {"static_painting": True} -> STATIC_PAINTING
    def test_ct14_static_painting_true(self):
        """CT14: Teste para D5/C5.2 (V) - door_obj["static_painting"] é True."""
        door_obj = {"static_painting": True}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.STATIC_PAINTING

    # CT15: D5/C5.1 (F) - {} -> NORMAL
    def test_ct15_no_static_painting_key(self):
        """CT15: Teste para D5/C5.1 (F) - "static_painting" não está em door_obj."""
        door_obj = {}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.NORMAL

    # CT16: D7/C7.1 (F) - {} -> RoomEntrance com door=None
    def test_ct16_no_door_key(self):
        """CT16: Teste para D7/C7.1 (F) - "door" não está em door_obj."""
        door_obj = {}
        result = process_single_entrance("SourceRoom", "TargetRoom", door_obj)
        assert result.door is None
        assert result.type == EntranceType.NORMAL

    # CT17: D7/C7.1 (V) - {"door": "some_door"} -> RoomEntrance com door especificado
    def test_ct17_with_door_key(self):
        """CT17: Teste para D7/C7.1 (V) - "door" está em door_obj."""
        door_obj = {"door": "some_door", "room": "DoorRoom"}
        result = process_single_entrance("SourceRoom", "TargetRoom", door_obj)
        assert result.door == RoomAndDoor("DoorRoom", "some_door")
        assert result.type == EntranceType.NORMAL

    # Additional test case for the second occurrence of D6 (same as D1)
    def test_ct_d6_painting_true_second_occurrence(self):
        """CT_D6: Teste para a segunda ocorrência de D6/C6.2 (V) - door_obj["painting"] é True."""
        door_obj = {"painting": True}
        result = process_single_entrance("Any", "Any", door_obj)
        assert result.type == EntranceType.PAINTING
        assert "Any" in process_single_entrance.__globals__["PAINTING_EXIT_ROOMS"]
        assert process_single_entrance.__globals__["PAINTING_ENTRANCES"] == 1

    # Test case for RoomAndDoor with no 'room' key in door_obj
    def test_ct_door_no_room_key(self):
        """CT_DOOR_NO_ROOM: Teste para RoomAndDoor quando 'room' não está em door_obj."""
        door_obj = {"door": "some_door"}
        result = process_single_entrance("SourceRoom", "TargetRoom", door_obj)
        assert result.door == RoomAndDoor(None, "some_door")
        assert result.type == EntranceType.NORMAL


