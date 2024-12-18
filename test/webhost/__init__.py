import unittest
import typing
from uuid import uuid4

from flask import Flask
from flask.testing import FlaskClient


class TestBase(unittest.TestCase):
    app: typing.ClassVar[Flask]
    client: FlaskClient

    @classmethod
    def setUpClass(cls) -> None:
        from WebHostLib import app as raw_app
        from WebHost import get_app

        raw_app.config["PONY"] = {
            "provider": "sqlite",
            "filename": ":memory:",
            "create_db": True,
        }
        raw_app.config.update({
            "TESTING": True,
            "DEBUG": True,
        })
        try:
            cls.app = get_app()
        except AssertionError as e:
            # since we only have 1 global app object, this might fail, but luckily all tests use the same config
            if "register_blueprint" not in e.args[0]:
                raise
            cls.app = raw_app

    def setUp(self) -> None:
        self.client = self.app.test_client()
