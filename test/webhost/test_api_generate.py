import unittest
import json


class TestDocs(unittest.TestCase):
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
        })
        app = get_app()

        cls.client = app.test_client()

    def test_correct_error_empty_request(self):
        response = self.client.post("/api/generate")
        self.assertIn("No options found. Expected file attachment or json weights.", response.text)

    def test_generation_queued(self):
        options = {
            "Tester1":
                {
                    "game": "Archipelago",
                    "name": "Tester",
                    "Archipelago": {}
                }
        }
        response = self.client.post(
            "/api/generate",
            data=json.dumps({"weights": options}),
            content_type='application/json'
        )
        json_data = response.get_json()
        self.assertTrue(json_data["text"].startswith("Generation of seed "))
        self.assertTrue(json_data["text"].endswith(" started successfully."))
