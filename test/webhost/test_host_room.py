import os
from uuid import UUID, uuid4, uuid5

from flask import url_for

from . import TestBase


class TestHostFakeRoom(TestBase):
    room_id: UUID
    log_filename: str

    def setUp(self) -> None:
        from pony.orm import db_session
        from WebHostLib.models import Room, Seed

        super().setUp()

        with self.client.session_transaction() as session:
            session["_id"] = uuid4()
            with db_session:
                # create an empty seed and a room from it
                seed = Seed(multidata=b"", owner=session["_id"])
                room = Room(seed=seed, owner=session["_id"], tracker=uuid4())
                self.room_id = room.id
                self.log_filename = f"logs/{self.room_id}.txt"

    def tearDown(self) -> None:
        from pony.orm import db_session
        from WebHostLib.models import Room

        with db_session:
            room: Room = Room.get(id=self.room_id)
            room.seed.delete()
            room.delete()

        try:
            os.unlink(self.log_filename)
        except FileNotFoundError:
            pass

    def test_display_log_missing_full(self) -> None:
        """
        Verify that we get a 200 response even if log is missing.
        This is required to not get an error for fetch.
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(url_for("display_log", room=self.room_id))
            self.assertEqual(response.status_code, 200)

    def test_display_log_missing_range(self) -> None:
        """
        Verify that we get a full response for missing log even if we asked for range.
        This is required for the JS logic to differentiate between log update and log error message.
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(url_for("display_log", room=self.room_id), headers={
                "Range": "bytes=100-"
            })
            self.assertEqual(response.status_code, 200)

    def test_display_log_denied(self) -> None:
        """Verify that only the owner can see the log."""
        other_client = self.app.test_client()
        with self.app.app_context(), self.app.test_request_context():
            response = other_client.get(url_for("display_log", room=self.room_id))
            self.assertEqual(response.status_code, 403)

    def test_display_log_missing_room(self) -> None:
        """Verify log for missing room gives an error as opposed to missing log for existing room."""
        missing_room_id = uuid5(uuid4(), "")  # rooms are always uuid4, so this can't exist
        other_client = self.app.test_client()
        with self.app.app_context(), self.app.test_request_context():
            response = other_client.get(url_for("display_log", room=missing_room_id))
            self.assertEqual(response.status_code, 404)

    def test_display_log_full(self) -> None:
        """Verify full log response."""
        with open(self.log_filename, "w", encoding="utf-8") as f:
            text = "x" * 200
            f.write(text)

        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(url_for("display_log", room=self.room_id))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_data(True), text)

    def test_display_log_range(self) -> None:
        """Verify that Range header in request gives a range in response."""
        with open(self.log_filename, "w", encoding="utf-8") as f:
            f.write(" " * 100)
            text = "x" * 100
            f.write(text)

        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(url_for("display_log", room=self.room_id), headers={
                "Range": "bytes=100-"
            })
            self.assertEqual(response.status_code, 206)
            self.assertEqual(response.get_data(True), text)

    def test_display_log_range_bom(self) -> None:
        """Verify that a BOM in the log file is skipped for range."""
        with open(self.log_filename, "w", encoding="utf-8-sig") as f:
            f.write(" " * 100)
            text = "x" * 100
            f.write(text)
            self.assertEqual(f.tell(), 203)  # including BOM

        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(url_for("display_log", room=self.room_id), headers={
                "Range": "bytes=100-"
            })
            self.assertEqual(response.status_code, 206)
            self.assertEqual(response.get_data(True), text)
