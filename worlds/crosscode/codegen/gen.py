"""
This module contains code to create the generated python lists and mod data files.
"""

from collections import defaultdict
from copy import deepcopy
import logging
import typing
import os
import json

import jinja2

from .jinja import CrossCodeJinjaExtension
from ..types.regions import RegionsData
from ..types.items import ProgressiveItemChain, ProgressiveItemChainMulti, ProgressiveItemChainSingle, ProgressiveItemSubchain

from ..types.json_data import ExportInfo
from ..types.regions import RegionsData

from .context import Context, make_context_from_package
from .util import GENERATED_COMMENT
from .lists import ListInfo

cglogger = logging.getLogger("crosscode.codegen")

class FileGenerator:
    """
    This class uses an instance of ListInfo and provides functions to create python and mod data files.
    """
    environment: jinja2.Environment
    ctx: Context
    common_args: typing.Dict[str, typing.Any]
    lists: ListInfo
    regions_data: dict[str, RegionsData]
    world_dir: str
    data_out_dir: str

    def __init__(self, world_dir: str, lists: typing.Optional[ListInfo] = None):
        data_out_dir = os.path.join(world_dir, "data", "out")
        template_dir = os.path.join(world_dir, "templates")

        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(template_dir),
        )

        if lists is None:
            self.ctx = make_context_from_package(world_dir.replace('/', '.'))
            self.lists = ListInfo(self.ctx)
            self.lists.build()
        else:
            self.lists = lists
            self.ctx = lists.ctx

        self.regions_data = {
            key: self.lists.json_parser.parse_regions_data(value)
            for key, value in self.ctx.rando_data["regions"].items()
        }

        self.world_dir = world_dir
        self.data_out_dir = data_out_dir

        self.environment.add_extension(CrossCodeJinjaExtension)

        self.common_args = {
            "generated_comment": GENERATED_COMMENT,
            "modes": self.ctx.rando_data["modes"],
            "default_mode": self.ctx.rando_data["defaultMode"],
            "base_id": self.ctx.rando_data["baseId"],
            "data_version": self.ctx.rando_data["dataVersion"],
            "version": self.ctx.rando_data["randoVersion"],
        }

    def generate_python_file_common(self):
        """
        Generates common.py, which provides the base ID, game name, and data version.
        """
        template = self.environment.get_template("common.template.py")

        locations_complete = template.render(
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "common.py"), "w", encoding="utf8") as f:
            f.write(locations_complete)

    def generate_python_file_locations(self):
        """
        Generates locations.py, which provides a list of locations and events.
        """
        template = self.environment.get_template("locations.template.py")

        locations_complete = template.render(
            locations_data=self.lists.locations_data.values(),
            pool_locations=self.lists.pool_locations,
            events_data=self.lists.events_data.values(),
            locked_locations=self.lists.locked_locations,
            location_groups=self.lists.location_groups,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "locations.py"), "w", encoding="utf8") as f:
            f.write(locations_complete)

    def generate_python_file_items(self):
        """
        Generates items.py, which provides lists of items, including:
        * single items
        * multiples of items
        * full item names to items
        """
        template = self.environment.get_template("items.template.py")

        sorted_single_item_data = sorted(
            self.lists.single_items_dict.items(),
            key=lambda i: i[1].item_id
        )

        sorted_item_data = sorted(
            self.lists.items_dict.items(),
            key=lambda i: i[1].combo_id
        )

        items_complete = template.render(
            single_items_dict=sorted_single_item_data,
            items_dict=sorted_item_data,
            num_items=self.ctx.num_items,
            keyring_items=self.ctx.rando_data["keyringItems"],
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "items.py"), "w", encoding="utf8") as f:
            f.write(items_complete)

    def generate_python_file_item_pools(self):
        """
        Generates item_pools.py, which provides instructions on how to build item pools based on options.
        """
        template = self.environment.get_template("item_pools.template.py")

        item_pools_complete = template.render(
            item_pools=self.lists.item_pools,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "item_pools.py"), "w", encoding="utf8") as f:
            f.write(item_pools_complete)

    def generate_python_file_prog_items(self):
        """
        Generates prog_items.py, which provides information on progressive chains.
        """
        template = self.environment.get_template("prog_items.template.py")

        item_pools_complete = template.render(
            prog_chains=self.lists.progressive_chains,
            prog_chain_types={
                name: "multi" if isinstance(chain, ProgressiveItemChainMulti) else "single"
                for name, chain in self.lists.progressive_chains.items()
            },
            prog_items=self.lists.progressive_items,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "prog_items.py"), "w", encoding="utf8") as f:
            f.write(item_pools_complete)

    def generate_python_file_regions(self):
        """
        Generates regions.py, which provides information on which regions exist and how they are connected.
        """
        template = self.environment.get_template("regions.template.py")

        regions_complete = template.render(
            modes_string=", ".join([f'"{x}"' for x in self.ctx.rando_data["modes"]]),
            region_packs=self.regions_data,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "regions.py"), "w", encoding="utf8") as f:
            f.write(regions_complete)

    def generate_python_file_vars(self):
        """
        Generates vars.py, which includes definitions of variable condition
        """
        template = self.environment.get_template("vars.template.py")

        regions_complete = template.render(
            variable_definitions=self.lists.variable_definitions,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "vars.py"), "w", encoding="utf8") as f:
            f.write(regions_complete)

    def generate_python_file_shops(self):
        """
        Generates locations.py, which provides a list of locations and events.
        """
        template = self.environment.get_template("shops.template.py")

        locations_complete = template.render(
            shop_data=self.lists.shop_data,
            per_shop_locations=self.lists.per_shop_locations,
            global_shop_locations=self.lists.global_shop_locations,
            shop_unlock_by_id=self.lists.shop_unlock_by_id,
            shop_unlock_by_shop=self.lists.shop_unlock_by_shop,
            shop_unlock_by_shop_and_id=self.lists.shop_unlock_by_shop_and_id,
            **self.common_args
        )

        with open(os.path.join(self.world_dir, "shops.py"), "w", encoding="utf8") as f:
            f.write(locations_complete)


    def generate_python_files(self) -> None:
        """
        Generates all python list files.
        """
        self.generate_python_file_common()
        self.generate_python_file_locations()
        self.generate_python_file_items()
        self.generate_python_file_item_pools()
        self.generate_python_file_prog_items()
        self.generate_python_file_regions()
        self.generate_python_file_vars()
        self.generate_python_file_shops()

    def generate_mod_files(self):
        """
        Generates JSON files for use by the CCMultiworldRandomizer mod.
        """
        merged_data = deepcopy(self.ctx.rando_data)

        data_out: ExportInfo = {
            "items": defaultdict(lambda: defaultdict(dict)), # type: ignore
            "quests": defaultdict(dict),
            "shops": {
                "locations": {
                    "perItemType": {
                        item_id: data.code
                        for item_id, data in self.lists.global_shop_locations.items()
                        if data.code is not None
                    },
                    "perShop": defaultdict(dict),
                },
                "unlocks": {
                    "byId": {
                        item_id: data.combo_id
                        for item_id, data in self.lists.shop_unlock_by_id.items()
                    },
                    "byShop": {},
                    "byShopAndId": defaultdict(dict)
                },
            },
            "descriptions": self.lists.descriptions,
            "markers": self.lists.markers
        }

        def get_codes(name: str) -> list[int]:
            data = self.lists.locations_data
            if name in data:
                code = data[name].code
                if code is None:
                    raise RuntimeError(f"Trying to assign null code in {data}")
                return [code]

            result: list[int] = []
            idx = 1
            while True:
                full_name = f"{name} - Reward {idx}"
                if full_name not in data:
                    break
                code = data[full_name].code
                if code is None:
                    continue
                result.append(code)
                idx += 1

            return result

        for name, chest in merged_data["chests"].items():
            codes = get_codes(name)
            map_name = chest["location"]["map"]
            map_id = chest["location"]["mapId"]

            room = data_out["items"][map_name]
            room["chests"][map_id] = { "name": name, "mwids": codes }

        for name, cutscene in merged_data["cutscenes"].items():
            codes = get_codes(name)
            map_name = cutscene["location"]["map"]
            map_id = cutscene["location"]["mapId"]
            path = cutscene["location"]["path"]

            room = data_out["items"][map_name]
            if map_id not in room["cutscenes"]:
                room["cutscenes"][map_id] = []

            room["cutscenes"][map_id].append({ "mwids": codes, "path": path })

        for name, element in merged_data["elements"].items():
            codes = get_codes(name)
            map_name = element["location"]["map"]
            map_id = element["location"]["mapId"]

            room = data_out["items"][map_name]
            room["elements"][map_id] = { "mwids": codes }

        for name, quest in merged_data["quests"].items():
            codes = get_codes(name)
            quest_id = quest["questid"]
            if not quest_id in self.ctx.database["quests"]:
                cglogger.error("%s does not exist", quest_id)

            room = data_out["quests"]
            room[quest_id] = { "mwids": codes }

        for shop_name, items in self.lists.per_shop_locations.items():
            data_out["shops"]["locations"]["perShop"][self.lists.shop_data[shop_name].internal_name].update(
                { item_id: data.code for item_id, data in items.items() if data.code is not None }
            )

        for shop_name, data in self.lists.shop_unlock_by_shop.items():
            data_out["shops"]["unlocks"]["byShop"][shop_name] = data.combo_id

        for (shop_name, item_id), data in self.lists.shop_unlock_by_shop_and_id.items():
            data_out["shops"]["unlocks"]["byShopAndId"][shop_name][item_id] = data.combo_id

        try:
            os.mkdir(self.data_out_dir)
        except FileExistsError:
            pass

        with open(os.path.join(self.data_out_dir, "data.json"), "w", encoding="utf8") as f:
            json.dump(data_out, f, indent='\t')

        with open(os.path.join(self.data_out_dir, "locations.json"), "w", encoding="utf8") as f:
            location_ids = { loc.name: loc.code for loc in self.lists.locations_data.values() }
            json.dump(location_ids, f, indent='\t')

        with open(os.path.join(self.data_out_dir, "items.json"), "w", encoding="utf8") as f:
            item_ids = { loc.name: loc.combo_id for loc in self.lists.dynamic_items.values()  }
            json.dump(item_ids, f, indent='\t')
