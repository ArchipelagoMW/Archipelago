from . import LADXTestBase


class PlandoTest(LADXTestBase):
    """Tests plandoing swords in the shop."""
    options = {
        "plando_items": [{
            "items": {
                "Progressive Sword": 2
            },
            "locations": [
                "Shop 10 Item (Mabe Village)",
                "Shop 200 Item (Mabe Village)",
                "Shop 980 Item (Mabe Village)"
            ]
        }]
    }
