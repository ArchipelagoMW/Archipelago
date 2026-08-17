import logging
import os
from uuid import UUID, uuid4, uuid5

from flask import url_for

from WebHostLib.customserver import set_up_logging, tear_down_logging
from . import TestBase


def _cleanup_logger(room_id: UUID) -> None:
    from Utils import user_path
    tear_down_logging(room_id)
    try:
        os.unlink(user_path("logs", f"{room_id}.txt"))
    except OSError:
        pass


class TestHostFakeRoom(TestBase):
    room_id: UUID
    log_filename: str

    def setUp(self) -> None:
        from pony.orm import db_session
        from Utils import user_path
        from WebHostLib.models import Room, Seed

        super().setUp()

        with self.client.session_transaction() as session:
            session["_id"] = uuid4()
            with db_session:
                # create an empty seed and a room from it
                seed = Seed(multidata=b"", owner=session["_id"])
                room = Room(seed=seed, owner=session["_id"], tracker=uuid4())
                self.room_id = room.id
                self.log_filename = user_path("logs", f"{self.room_id}.txt")

    def tearDown(self) -> None:
        from pony.orm import db_session, select
        from WebHostLib.models import Command, Room

        with db_session:
            for command in select(command for command in Command if command.room.id == self.room_id):  # type: ignore
                command.delete()
            room: Room = Room.get(id=self.room_id)
            room.seed.delete()
            room.delete()

        try:
            os.unlink(self.log_filename)
        except OSError:
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

    def test_host_room_missing(self) -> None:
        """Verify that missing room gives a 404 response."""
        missing_room_id = uuid5(uuid4(), "")  # rooms are always uuid4, so this can't exist
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(url_for("host_room", room=missing_room_id))
            self.assertEqual(response.status_code, 404)

    def test_host_room_own(self) -> None:
        """Verify that own room gives the full output."""
        with open(self.log_filename, "w", encoding="utf-8-sig") as f:
            text = "* should be visible *"
            f.write(text)

        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(url_for("host_room", room=self.room_id),
                                       headers={"User-Agent": "Mozilla/5.0"})
            response_text = response.get_data(True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("href=\"/seed/", response_text)
            self.assertIn(text, response_text)

    def test_host_room_other(self) -> None:
        """Verify that non-own room gives the reduced output."""
        from pony.orm import db_session
        from WebHostLib.models import Room

        with db_session:
            room: Room = Room.get(id=self.room_id)
            room.last_port = 12345

        with open(self.log_filename, "w", encoding="utf-8-sig") as f:
            text = "* should not be visible *"
            f.write(text)

        other_client = self.app.test_client()
        with self.app.app_context(), self.app.test_request_context():
            response = other_client.get(url_for("host_room", room=self.room_id))
            response_text = response.get_data(True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("href=\"/seed/", response_text)
            self.assertNotIn(text, response_text)
            self.assertIn("/connect ", response_text)
            self.assertIn(":12345", response_text)

    def test_host_room_own_post(self) -> None:
        """Verify command from owner gets queued for the server and response is redirect."""
        from pony.orm import db_session, select
        from WebHostLib.models import Command

        with self.app.app_context(), self.app.test_request_context():
            response = self.client.post(url_for("host_room", room=self.room_id), data={
                "cmd": "/help"
            })
            self.assertEqual(response.status_code, 302, response.text)\

        with db_session:
            commands = select(command for command in Command if command.room.id == self.room_id)  # type: ignore
            self.assertIn("/help", (command.commandtext for command in commands))

    def test_host_room_other_post(self) -> None:
        """Verify command from non-owner does not get queued for the server."""
        from pony.orm import db_session, select
        from WebHostLib.models import Command

        other_client = self.app.test_client()
        with self.app.app_context(), self.app.test_request_context():
            response = other_client.post(url_for("host_room", room=self.room_id), data={
                "cmd": "/help"
            })
            self.assertLess(response.status_code, 500)

        with db_session:
            commands = select(command for command in Command if command.room.id == self.room_id)  # type: ignore
            self.assertNotIn("/help", (command.commandtext for command in commands))

    def test_logger_teardown(self) -> None:
        """Verify that room loggers are removed from the global logging manager."""
        from WebHostLib.customserver import tear_down_logging
        room_id = uuid4()
        self.addCleanup(_cleanup_logger, room_id)
        set_up_logging(room_id)
        self.assertIn(f"RoomLogger {room_id}", logging.Logger.manager.loggerDict)
        tear_down_logging(room_id)
        self.assertNotIn(f"RoomLogger {room_id}", logging.Logger.manager.loggerDict)

    def test_handler_teardown(self) -> None:
        """Verify that handlers for room loggers are closed by tear_down_logging."""
        from WebHostLib.customserver import tear_down_logging
        room_id = uuid4()
        self.addCleanup(_cleanup_logger, room_id)
        logger = set_up_logging(room_id)
        handlers = logger.handlers[:]
        self.assertGreater(len(handlers), 0)

        tear_down_logging(room_id)
        for handler in handlers:
            if isinstance(handler, logging.FileHandler):
                self.assertTrue(handler.stream is None or handler.stream.closed)
