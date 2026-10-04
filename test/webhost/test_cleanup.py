from datetime import timedelta
from uuid import UUID, uuid4
from pony.orm import db_session, commit

from Utils import utcnow
from WebHostLib.autolauncher import cleanup
from WebHostLib.models import Room, Seed, Slot
from . import TestBase


class TestCleanup(TestBase):
    def test_cleanup_unowned(self) -> None:
        with db_session:
            s1 = Seed(id=uuid4(), multidata=b"", owner=UUID(int=0))
            Room(id=uuid4(), owner=UUID(int=0), seed=s1)

            s2 = Seed(id=uuid4(), multidata=b"", owner=uuid4())  # Owned
            Room(id=uuid4(), owner=UUID(int=0), seed=s2)  # Unowned room of owned seed

            Seed(id=uuid4(), multidata=b"", owner=UUID(int=0))  # Unowned seed with no rooms

            commit()

        cleanup({"ROOM_AUTO_DELETE": 0})

        with db_session:
            self.assertEqual(Room.select().count(), 0)  # Both rooms were unowned
            self.assertEqual(Seed.select().count(), 1)  # s2 is owned
            self.assertIsNotNone(Seed.get(id=s2.id))

    def test_cleanup_auto_delete(self) -> None:
        now = utcnow()
        old_time = now - timedelta(days=10)
        recent_time = now - timedelta(days=2)

        with db_session:
            # Case 1: Old room, owned
            s1 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=old_time)
            r1 = Room(id=uuid4(), owner=uuid4(), seed=s1, last_activity=old_time)

            # Case 2: Recent room, owned
            s2 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=old_time)
            r2 = Room(id=uuid4(), owner=uuid4(), seed=s2, last_activity=recent_time)

            # Case 3: Old seed, no rooms, owned
            s3 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=old_time)

            # Case 4: Recent seed, no rooms, owned
            s4 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=recent_time)

            # Case 5: Old seed with recent room (should not be deleted)
            s5 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=old_time)
            r5 = Room(id=uuid4(), owner=uuid4(), seed=s5, last_activity=recent_time)

            commit()

        # Delete items older than 5 days
        cleanup({"ROOM_AUTO_DELETE": 5})

        with db_session:
            self.assertIsNone(Room.get(id=r1.id), "Old room should be deleted")
            self.assertIsNotNone(Room.get(id=r2.id), "Recent room should NOT be deleted")
            self.assertIsNone(Seed.get(id=s3.id), "Old seed without rooms should be deleted")
            self.assertIsNotNone(Seed.get(id=s4.id), "Recent seed without rooms should NOT be deleted")
            self.assertIsNotNone(Seed.get(id=s5.id), "Old seed with recent room should NOT be deleted")
            self.assertIsNotNone(Room.get(id=r5.id), "Recent room for old seed should NOT be deleted")

            # Seeds are deleted if they have NO rooms AND are old.
            # After r1 is deleted, s1 has no rooms. Since it's old, it should be deleted.
            self.assertIsNone(Seed.get(id=s1.id), "Old seed whose only room was deleted should be deleted")

    def test_cleanup_disabled(self) -> None:
        now = utcnow()
        old_time = now - timedelta(days=10)

        with db_session:
            s1 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=old_time)
            r1 = Room(id=uuid4(), owner=uuid4(), seed=s1, last_activity=old_time)
            commit()

        cleanup({"ROOM_AUTO_DELETE": 0})

        with db_session:
            self.assertIsNotNone(Room.get(id=r1.id), "Room should NOT be deleted when auto-delete is 0")
            self.assertIsNotNone(Seed.get(id=s1.id), "Seed should NOT be deleted when auto-delete is 0")

    def test_cleanup_slots(self) -> None:
        now = utcnow()
        old_time = now - timedelta(days=10)

        with db_session:
            s1 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=old_time)
            slot1 = Slot(player_id=1, player_name="P1", seed=s1, game="TestGame")

            s2 = Seed(id=uuid4(), multidata=b"", owner=uuid4(), creation_time=now)
            slot2 = Slot(player_id=2, player_name="P2", seed=s2, game="TestGame")

            commit()

        # Delete items older than 5 days
        cleanup({"ROOM_AUTO_DELETE": 5})

        with db_session:
            self.assertIsNone(Seed.get(id=s1.id), "Old seed should be deleted")
            self.assertIsNone(Slot.get(id=slot1.id), "Slot of deleted seed should be deleted")
            self.assertIsNotNone(Seed.get(id=s2.id), "Recent seed should NOT be deleted")
            self.assertIsNotNone(Slot.get(id=slot2.id), "Slot of recent seed should NOT be deleted")
