import zipfile
from io import BytesIO

from flask import url_for

from . import TestBase


class TestGenerate(TestBase):
    def test_valid_yaml(self) -> None:
        """
        Verify that posting a valid yaml will start generating a game.
        """
        with self.app.app_context(), self.app.test_request_context():
            yaml_data = """
            name: Player1
            game: Archipelago
            Archipelago: {}
            """
            response = self.client.post(url_for("generate"),
                                        data={"file": (BytesIO(yaml_data.encode("utf-8")), "test.yaml")},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue("/seed/" in response.request.path or
                            "/wait/" in response.request.path,
                            f"Response did not properly redirect ({response.request.path})")

    def test_empty_zip(self) -> None:
        """
        Verify that posting an empty zip will give an error.
        """
        with self.app.app_context(), self.app.test_request_context():
            zip_data = BytesIO()
            zipfile.ZipFile(zip_data, "w").close()
            zip_data.seek(0)
            self.assertGreater(len(zip_data.read()), 0)
            zip_data.seek(0)
            response = self.client.post(url_for("generate"),
                                        data={"file": (zip_data, "test.zip")},
                                        follow_redirects=True)
            self.assertIn("user-message", response.text,
                          "Request did not call flash()")
            self.assertIn("not find any valid files", response.text,
                          "Response shows unexpected error")
            self.assertIn("generate-game-form", response.text,
                          "Response did not get user back to the form")

    def test_too_many_players(self) -> None:
        """
        Verify that posting too many players will give an error.
        """
        max_roll = self.app.config["MAX_ROLL"]
        # validate that max roll has a sensible value, otherwise we probably changed how it works
        self.assertIsInstance(max_roll, int)
        self.assertGreater(max_roll, 1)
        self.assertLess(max_roll, 100)
        # create a yaml with max_roll+1 players and watch it fail
        with self.app.app_context(), self.app.test_request_context():
            yaml_data = "---\n".join([
                f"name: Player{n}\n"
                "game: Archipelago\n"
                "Archipelago: {}\n"
                for n in range(1, max_roll + 2)
            ])
            response = self.client.post(url_for("generate"),
                                        data={"file": (BytesIO(yaml_data.encode("utf-8")), "test.yaml")},
                                        follow_redirects=True)
            self.assertIn("user-message", response.text,
                          "Request did not call flash()")
            self.assertIn("limited to", response.text,
                          "Response shows unexpected error")
            self.assertIn("generate-game-form", response.text,
                          "Response did not get user back to the form")
