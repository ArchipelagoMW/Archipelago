from .bases import PseudoTestBase


class TestCastleMainSpawn(PseudoTestBase):
    options = {
        "spawn_point": "castle_main",
    }


class TestCastleGazeboSpawn(PseudoTestBase):
    options = {
        "spawn_point": "castle_gazebo",
    }


class TestDungeonMirrorSpawn(PseudoTestBase):
    options = {
        "spawn_point": "dungeon_mirror",
    }


class TestLibrarySpawn(PseudoTestBase):
    options = {
        "spawn_point": "library",
    }


class TestLibrarySpawnWithBooks(PseudoTestBase):
    options = {
        "spawn_point": "library",
        "randomize_books": True
    }


class TestUnderbellySouthSpawn(PseudoTestBase):
    options = {
        "spawn_point": "underbelly_south",
    }


class TestUnderbellyBigRoomSpawn(PseudoTestBase):
    options = {
        "spawn_point": "underbelly_big_room",
    }


class TestBaileySpawn(PseudoTestBase):
    options = {
        "spawn_point": "bailey_main",
    }


class TestKeepMainSpawn(PseudoTestBase):
    options = {
        "spawn_point": "keep_main",
    }


class TestKeepNorthSpawn(PseudoTestBase):
    options = {
        "spawn_point": "keep_north",
    }


class TestTheatreMainSpawn(PseudoTestBase):
    options = {
        "spawn_point": "theatre_main",
    }


class TestTheatreMainSpawnHard(PseudoTestBase):
    options = {
        "spawn_point": "theatre_main",
        "logic_level": "hard",
    }
