import asyncio
import json
from importlib import resources
from types import SimpleNamespace
from unittest import TestCase

from ..Client import Dota2Context
from ..ids import ITEM_IDS, LOCATION_IDS
from ..locations import all_location_defs, retired_location_names
from .. import DOTA2World
from .bases import Dota2TestBase


class FrozenIds(TestCase):
    def test_every_name_has_one_id(self) -> None:
        for ids in (LOCATION_IDS, ITEM_IDS):
            self.assertEqual(len(set(ids.values())), len(ids))
        self.assertTrue(set(DOTA2World.location_name_to_id) <= set(LOCATION_IDS))
        self.assertTrue(set(DOTA2World.item_name_to_id) <= set(ITEM_IDS))

    def test_ids_from_the_registry(self) -> None:
        for name, loc_id in DOTA2World.location_name_to_id.items():
            self.assertEqual(loc_id, LOCATION_IDS[name])
        # Released before the 7.42 update removed Javelin, Khanda and Helm of the Overlord from the middle of the shop
        self.assertEqual(LOCATION_IDS["Get 1 Kill(s)"], 7711739)
        self.assertEqual(ITEM_IDS["Gone Fishin' Minigame"], 7701603)

    def test_retired_locations(self) -> None:
        retired = retired_location_names()
        self.assertTrue({"Javelin", "Khanda", "Helm of the Overlord"} <= retired)
        self.assertFalse(retired & {d.name for d in all_location_defs()})


def fake_client(**fields) -> SimpleNamespace:
    sent = []
    async def check_locations(ids): sent.extend(ids)
    return SimpleNamespace(game="DOTA 2", sent=sent, check_locations=check_locations, output=lambda text: None, **fields)


class GameUpdates(TestCase):
    def test_retired_locations_sent(self) -> None:
        javelin, kills = LOCATION_IDS["Javelin"], LOCATION_IDS["Get 1 Kill(s)"]
        ctx = fake_client(location_names={"DOTA 2": {javelin: "Javelin", kills: "Get 1 Kill(s)"}},
                          missing_locations={javelin, kills})
        asyncio.run(Dota2Context.send_retired_locations(ctx))
        self.assertEqual(ctx.sent, [javelin])

    def test_component_missing_from_seed_ignored(self) -> None:
        # A seed from before an update that added "Unlock quarterstaff" to a recipe
        ctx = fake_client(items_received=[SimpleNamespace(item=1)],
                          save=SimpleNamespace(item_name_to_id={"Unlock blades_of_attack": 1, "Unlock claymore": 2}))
        self.assertTrue(Dota2Context.item_requirements_met(ctx, ["blades_of_attack", "quarterstaff"]))
        self.assertFalse(Dota2Context.item_requirements_met(ctx, ["blades_of_attack", "claymore"]))


class WorldVersion(Dota2TestBase):
    def test_in_slot_data(self) -> None:
        with resources.files("worlds.dota_2").joinpath("archipelago.json").open(encoding="utf-8") as f:
            version = json.load(f)["world_version"]
        self.assertEqual(self.world.fill_slot_data()["world_version"], version)


class DataUpdate(TestCase):
    def test_requirements(self) -> None:
        from ..tools.update_data import requirements
        items = {"dagon": {"components": ["crown", "recipe_dagon", ""]}, "dagon_2": {"components": None},
                 "crown": {"components": None}, "tango": {"components": None},
                 "travel_boots": {"components": ["boots", "recipe_travel_boots"]}, "boots": {}}
        self.assertEqual(requirements("dagon", items, {"tango"}), ["crown"])
        self.assertEqual(requirements("dagon_2", items, {"tango"}), ["crown"])  # bought from level 1
        self.assertEqual(requirements("travel_boots", items, {"tango"}), ["boots"])
        self.assertEqual(requirements("tango", items, {"tango"}), [])

    def test_new_names_go_last(self) -> None:
        from ..tools.update_ids import add_names
        ids = {"A": 10, "B": 11}
        self.assertEqual(add_names(ids, ["B", "C", "A", "D", "C"]), ["C", "D"])
        self.assertEqual(ids, {"A": 10, "B": 11, "C": 12, "D": 13})

    def test_overrides_match_the_shop(self) -> None:
        with resources.files("worlds.dota_2").joinpath("data/shopOverrides.json").open(encoding="utf-8") as f:
            overrides = json.load(f)
        with resources.files("worlds.dota_2").joinpath("data/dotaShopLocations.json").open(encoding="utf-8") as f:
            shop = json.load(f)
        self.assertFalse(set(overrides["exclude"]) & set(shop))
        self.assertEqual(set(overrides["free"]), {k for k, v in shop.items() if not v.get("requirements")})
