import io
import json
import yaml

from . import TestBase


class TestAPIGenerate(TestBase):
    def test_correct_error_empty_request(self) -> None:
        response = self.client.post("/api/generate")
        self.assertIn("No options found. Expected file attachment or json weights.", response.text)

    def test_generation_queued_weights(self) -> None:
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

    def test_generation_queued_file(self) -> None:
        options = {
            "game": "Archipelago",
            "name": "Tester",
            "Archipelago": {}
        }
        response = self.client.post(
            "/api/generate",
            data={
                'file': (io.BytesIO(yaml.dump(options, encoding="utf-8")), "test.yaml")
            },
        )
        json_data = response.get_json()
        self.assertTrue(json_data["text"].startswith("Generation of seed "))
        self.assertTrue(json_data["text"].endswith(" started successfully."))
