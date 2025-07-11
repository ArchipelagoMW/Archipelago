import hashlib
import json
import logging
import os
import zipfile
import typing
from multiprocessing import Process
from typing import TextIO

import Utils
from BaseClasses import Item, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, SuffixIdentifier
from worlds.Files import APPlayerContainer, AutoPatchRegister
from . import Patches
from .Events import create_events
from .Items import item_table, NO100FItem
from .Locations import location_table, NO100FLocation
from .Options import NO100FOptions
from .Regions import create_regions
from .Rules import set_rules
from .names import ItemNames, ConnectionNames


def run_client():
    print('running Scooby-Doo! NO100F client')
    from worlds.no100f.NO100FClient import main  # lazy import
    file_types = (('NO100F Patch File', ('.apno100f',)), ('NGC iso', ('.gcm',)),)
    kwargs = {'patch_file': Utils.open_filename("Select .apno100f", file_types)}
    p = Process(target=main, kwargs=kwargs)
    p.start()


components.append(Component("Scooby-Doo! NO100F Client", func=run_client, component_type=Type.CLIENT,
                            file_identifier=SuffixIdentifier('.apno100f')))

NO100F_HASH = "6f078c687c81e26b8e81127ba4b747ba"

class NO100FContainer(APPlayerContainer, metaclass=AutoPatchRegister):
    hash = NO100F_HASH
    game = "Scooby-Doo! Night of 100 Frights"
    patch_file_ending: str = ".apno100f"
    result_file_ending: str = ".gcm"
    zip_version: int = 1
    logger = logging.getLogger("NO100FPatch")

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        if 'seed' in kwargs:
            self.include_monster_tokens: int = kwargs['include_monster_tokens']
            self.include_snacks: int = kwargs['include_snacks']
            self.include_keys: int = kwargs['include_keys']
            self.include_warpgates: int = kwargs['include_warpgates']
            self.completion_goal: int = kwargs['completion_goal']
            self.seed: bytes = kwargs['seed']
            del kwargs['include_monster_tokens']
            del kwargs['include_snacks']
            del kwargs['include_keys']
            del kwargs['include_warpgates']
            del kwargs['completion_goal']
            del kwargs['seed']
        super().__init__(*args, **kwargs)

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        super(NO100FContainer, self).write_contents(opened_zipfile)
        opened_zipfile.writestr("include_monster_tokens",
                                self.include_monster_tokens.to_bytes(1, "little"),
                                compress_type=zipfile.ZIP_STORED)
        opened_zipfile.writestr("include_snacks",
                                self.include_snacks.to_bytes(1, "little"),
                                compress_type=zipfile.ZIP_STORED)
        opened_zipfile.writestr("include_keys",
                                self.include_keys.to_bytes(1, "little"),
                               compress_type=zipfile.ZIP_STORED)
        opened_zipfile.writestr("include_warpgates",
                                self.include_warpgates.to_bytes(1, "little"),
                               compress_type=zipfile.ZIP_STORED)
        opened_zipfile.writestr("completion_goal",
                                self.completion_goal.to_bytes(1, "little"),
                                compress_type=zipfile.ZIP_STORED)
        opened_zipfile.writestr("zip_version",
                                self.zip_version.to_bytes(1, "little"),
                                compress_type=zipfile.ZIP_STORED)
        m = hashlib.md5()
        m.update(self.seed)
        opened_zipfile.writestr("seed",
                                m.digest(),
                                compress_type=zipfile.ZIP_STORED)

    def read_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        super(NO100FContainer, self).read_contents(opened_zipfile)

    @classmethod
    def get_int(cls, opened_zipfile: zipfile.ZipFile, name: str):
        if name not in opened_zipfile.namelist():
            cls.logger.warning(f"couldn't find {name} in patch file")
            return 0
        return int.from_bytes(opened_zipfile.read(name), "little")

    @classmethod
    def get_bool(cls, opened_zipfile: zipfile.ZipFile, name: str):
        if name not in opened_zipfile.namelist():
            cls.logger.warning(f"couldn't find {name} in patch file")
            return False
        return bool.from_bytes(opened_zipfile.read(name), "little")

    @classmethod
    def get_json_obj(cls, opened_zipfile: zipfile.ZipFile, name: str):
        if name not in opened_zipfile.namelist():
            cls.logger.warning(f"couldn't find {name} in patch file")
            return None
        with opened_zipfile.open(name, "r") as f:
            obj = json.load(f)
        return obj

    @classmethod
    def get_seed_hash(cls, opened_zipfile: zipfile.ZipFile):
        return opened_zipfile.read("seed")

    @classmethod
    async def apply_binary_changes(cls, opened_zipfile: zipfile.ZipFile, iso):
        cls.logger.info('--binary patching--')
        # get slot name and seed hash
        manifest = NO100FContainer.get_json_obj(opened_zipfile, "archipelago.json")
        slot_name = manifest["player_name"]
        slot_name_bytes = slot_name.encode('utf-8')
        slot_name_offset = 0x1e0c9c
        seed_hash = NO100FContainer.get_seed_hash(opened_zipfile)
        seed_hash_offset = slot_name_offset + 0x40
        # always apply these patches
        patches = [Patches.AP_SAVE_LOAD, Patches.UPGRADE_REWARD_FIX]
        # conditional patches
        include_monster_tokens = NO100FContainer.get_bool(opened_zipfile, "include_monster_tokens")
        include_snacks = NO100FContainer.get_bool(opened_zipfile, "include_snacks")
        if include_monster_tokens:
            patches += [Patches.MONSTER_TOKEN_FIX]
        if include_snacks:
            patches += [Patches.SNACK_REWARD_FIX]

        with open(iso, "rb+") as stream:
            # write patches
            for patch in patches:
                cls.logger.info(f"applying patch {patches.index(patch) + 1}/{len(patches)}")
                for addr, val in patch.items():
                    stream.seek(addr, 0)
                    if isinstance(val, bytes):
                        stream.write(val)
                    else:
                        stream.write(val.to_bytes(0x4, "big"))
            # write slot name
            cls.logger.debug(f"writing slot_name to 0x{slot_name_offset:x} ({slot_name_bytes})")
            stream.seek(slot_name_offset, 0)
            stream.write(slot_name_bytes)
            cls.logger.debug(f"writing seed_hash {seed_hash} to 0x{seed_hash_offset:x}")
            stream.seek(seed_hash_offset, 0)
            stream.write(seed_hash)
        cls.logger.info('--binary patching done--')

    @classmethod
    def get_rom_path(cls) -> str:
        return get_base_rom_path()
    @classmethod
    def check_hash(cls):
        if not validate_hash():
            Exception(f"Supplied Base Rom does not match known MD5 for Scooby Doo! Night of 100 Frights.iso. "
                      "Get the correct game and version.")
    @classmethod
    def check_version(cls, opened_zipfile: zipfile.ZipFile) -> bool:
        version_bytes = opened_zipfile.read("zip_version")
        version = 0
        if version_bytes is not None:
            version = int.from_bytes(version_bytes, "little")
        if version != cls.zip_version:
            return False
        return True


def get_base_rom_path(file_name: str = "") -> str:
    options: Utils.OptionsType = Utils.get_options()
    if not file_name:
        file_name = "Scooby-Doo! Night of 100 Frights.iso"
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


def validate_hash(file_name: str = ""):
    file_name = get_base_rom_path(file_name)
    with open(file_name, "rb") as file:
        base_rom_bytes = bytes(file.read())
    basemd5 = hashlib.md5()
    basemd5.update(base_rom_bytes)
    return NO100FContainer == basemd5.hexdigest()

class NO100FWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the integration for Archipelago multiworld games.",
        "English",
        "setup_en.md",
        "setup/en",
        ["vgm5"]
    )]



class NightOf100FrightsWorld(World):
    """
    Scooby-Doo! Night of 100 Frights
    """
    game = "Scooby-Doo! Night of 100 Frights"
    options_dataclass = NO100FOptions
    options: NO100FOptions
    topology_present = False

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = location_table
    web = NO100FWeb()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.snack_counter: int = 0

    def get_items(self):
        # Generate item pool
        itempool = [ItemNames.GumPower, ItemNames.SoapPower, ItemNames.PoundPower, ItemNames.HelmetPower,
                    ItemNames.ShockwavePower, ItemNames.BootsPower, ItemNames.PlungerPower, ItemNames.ShovelPower]
        itempool += [ItemNames.ProgressiveJump] * 2
        itempool += [ItemNames.ProgressiveSneak] * 3
        itempool += [ItemNames.SoapAmmoUpgrade] * 8
        itempool += [ItemNames.GumAmmoUpgrade] * 7
        if self.options.include_snacks:
            itempool += [ItemNames.Snack] * 5287
        if self.options.include_monster_tokens:
            itempool += [ItemNames.MT_PROGRESSIVE] * 21
        if self.options.include_keys == 1:
            itempool += [ItemNames.Hedge_Key, ItemNames.Fishing_Key, ItemNames.Clamor1_Key, ItemNames.Clamor4_Key,
                         ItemNames.Gusts1_Key, ItemNames.Tomb1_Key]  # Single Keys
            itempool += [ItemNames.Tomb3_Key] * 2  # Double Keys
            itempool += [ItemNames.Cellar2_Key, ItemNames.Graveplot_Key, ItemNames.Attic_Key, ItemNames.Creepy3_Key,
                         ItemNames.DLD_Key] * 3  # Triple Keys
            itempool += [ItemNames.Cellar3_Key, ItemNames.Cavein_Key, ItemNames.FishyClues_Key, ItemNames.MYM_Key,
                         ItemNames.Coast_Key, ItemNames.Knight_Key, ItemNames.Gusts2_Key, ItemNames.Shiver_Key] * 4  # Quad Keys
            itempool += [ItemNames.Creepy2_Key] * 5  # Penta Keys
        if self.options.include_keys == 2:
            itempool+=[ItemNames.Hedge_Key, ItemNames.Fishing_Key, ItemNames.Clamor1_Key, ItemNames.Clamor4_Key,
                         ItemNames.Gusts1_KeyRing, ItemNames.Tomb1_KeyRing, ItemNames.Tomb3_KeyRing, ItemNames.Cellar2_KeyRing,
                         ItemNames.Graveplot_KeyRing, ItemNames.Attic_KeyRing, ItemNames.Creepy3_KeyRing,
                         ItemNames.DLD_KeyRing, ItemNames.Cellar3_KeyRing, ItemNames.Cavein_KeyRing, ItemNames.FishyClues_KeyRing, ItemNames.MYM_KeyRing,
                         ItemNames.Coast_KeyRing, ItemNames.Knight_KeyRing, ItemNames.Gusts2_KeyRing, ItemNames.Shiver_KeyRing, ItemNames.Creepy2_KeyRing]
            itempool += [ItemNames.FillerSnack] * 39
        if self.options.include_warpgates:
            itempool += [ItemNames.Cellar4_Warp, ItemNames.Cliff4_Warp, ItemNames.Hedge4_Warp, ItemNames.Hedge6_Warp,
                         ItemNames.Hedge9_Warp, ItemNames.Fish3_Warp, ItemNames.Fish7_Warp, ItemNames.Balc1_Warp,
                         ItemNames.Balc4_Warp, ItemNames.Balc6_Warp, ItemNames.Grave1_Warp, ItemNames.Grave5_Warp,
                         ItemNames.Grave8_Warp, ItemNames.Manor3_Warp, ItemNames.Manor6_Warp, ItemNames.LH14_Warp,
                         ItemNames.LH15_Warp, ItemNames.LH18_Warp, ItemNames.SP3_Warp, ItemNames.SP5_Warp,
                         ItemNames.Roof3_Warp, ItemNames.SL2_Warp, ItemNames.Wreck22_Warp, ItemNames.Wreck26_Warp,
                         ItemNames.MG_Warp]

        # adjust for starting inv prog. items
        k = 0
        for item in self.multiworld.precollected_items[self.player]:
            if item.name in itempool and item.advancement:
                itempool.remove(item.name)
                k = k + 1

        # Convert itempool into real items
        itempool = list(map(lambda name: self.create_item(name), itempool))
        return itempool

    def create_items(self):
        self.multiworld.itempool += self.get_items()

    def set_rules(self):
        create_events(self.multiworld, self.player)
        if(self.options.no_logic == 0):
            set_rules(self.multiworld, self.options, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def fill_slot_data(self):
        return {
            "death_link": self.options.death_link.value,
            "include_monster_tokens": self.options.include_monster_tokens.value,
            "include_keys": self.options.include_keys.value,
            "include_warpgates": self.options.include_warpgates.value,
            "include_snacks": self.options.include_snacks.value,
            "completion_goal": self.options.completion_goal.value,
            "boss_count": self.options.boss_count.value,
            "token_count": self.options.token_count.value,
            "snack_count": self.options.snack_count.value,
            "advanced_logic": self.options.advanced_logic.value,
            "expert_logic": self.options.expert_logic.value,
            "creepy_early": self.options.creepy_early.value,
            "no_logic": self.options.no_logic.value,
            "speedster": self.options.speedster.value,
        }

    def create_item(self, name: str,) -> Item:
        item_data = item_table[name]
        classification = item_data.classification

        if name == ItemNames.Snack:
            self.snack_counter += 1
            if self.options.include_snacks and self.options.snack_count.value > 850 and self.options.completion_goal > 3:
                if self.snack_counter > self.options.snack_count:
                    classification = ItemClassification.filler

            else:
                if self.snack_counter > 850:
                    classification = ItemClassification.filler

        item = NO100FItem(name, classification, item_data.id, self.player)

        return item

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        return

    def generate_output(self, output_directory: str) -> None:
        patch = NO100FContainer(path=os.path.join(output_directory,
                                                 f"{self.multiworld.get_out_file_name_base(self.player)}{NO100FContainer.patch_file_ending}"),
                               player=self.player,
                               player_name=self.player_name,
                               include_monster_tokens=bool(self.options.include_monster_tokens.value),
                               include_snacks=bool(self.options.include_snacks.value),
                               include_keys=bool(self.options.include_keys.value),
                               include_warpgates=bool(self.options.include_warpgates.value),
                               completion_goal=bool(self.options.completion_goal.value),
                               seed=self.multiworld.seed_name.encode('utf-8'),
                               )
        patch.write()
