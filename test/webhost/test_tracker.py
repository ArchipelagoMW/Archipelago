import os
import pickle
from pathlib import Path
from typing import ClassVar
from uuid import UUID, uuid4

from flask import url_for

from . import TestBase


class TestTracker(TestBase):
    room_id: UUID
    tracker_uuid: UUID
    log_filename: str
    data: ClassVar[bytes]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        with (Path(__file__).parent / "data" / "One_Archipelago.archipelago").open("rb") as f:
            cls.data = f.read()

    def setUp(self) -> None:
        from pony.orm import db_session
        from MultiServer import Context as MultiServerContext
        from Utils import user_path
        from WebHostLib.models import GameDataPackage, Room, Seed

        super().setUp()

        multidata = MultiServerContext.decompress(self.data)

        with self.client.session_transaction() as session:
            session["_id"] = uuid4()
            self.tracker_uuid = uuid4()
            with db_session:
                # store game datapackage(s)
                for game, game_data in multidata["datapackage"].items():
                    if not GameDataPackage.get(checksum=game_data["checksum"]):
                        GameDataPackage(checksum=game_data["checksum"],
                                        data=pickle.dumps(game_data))
                # create an empty seed and a room from it
                seed = Seed(multidata=self.data, owner=session["_id"])
                room = Room(seed=seed, owner=session["_id"], tracker=self.tracker_uuid)
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
        except FileNotFoundError:
            pass

    def test_valid_if_modified_since(self) -> None:
        """
        Verify that we get a 200 response for valid If-Modified-Since
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(
                url_for(
                    "get_player_tracker",
                    tracker=self.tracker_uuid,
                    tracked_team=0,
                    tracked_player=1,
                ),
                headers={"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00 GMT"},
            )
            self.assertEqual(response.status_code, 200)

    def test_invalid_if_modified_since(self) -> None:
        """
        Verify that we get a 400 response for invalid If-Modified-Since
        """
        with self.app.app_context(), self.app.test_request_context():
            response = self.client.get(
                url_for(
                    "get_player_tracker",
                    tracker=self.tracker_uuid,
                    tracked_team=1,
                    tracked_player=0,
                ),
                headers={"If-Modified-Since": "Wed, 21 Oct 2015 07:28:00"},  # missing timezone
            )
            self.assertEqual(response.status_code, 400)
