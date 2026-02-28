import logging
import os.path
import typing as t
from dataclasses import fields
from pathlib import Path
from tempfile import TemporaryDirectory

import settings
from BaseClasses import Item, Location, Region, ItemClassification, CollectionState, Tutorial, MultiWorld
from Options import PerGameCommonOptions
from Utils import output_path
from worlds.AutoWorld import WebWorld, World
from worlds.Files import APDeltaPatch

from .gen import (
    ItemId,
    LocationId,
    character_class_keys,
    character_exists_keys,
    character_in_logic_keys,
    character_items,
    character_starter_weapon_keys,
    progression_event_rewards,
    progression_items,
    spell_progression,
    useful_items,
    item_name_to_id,
    location_name_to_id,
    item_name_groups,
)
from .options import SoMOptions, Goal, SoMROptionProto

if t.TYPE_CHECKING:
    from pysomr import OW

required_pysomr_version = "1.48.0a3"  # TODO: grab from requirements.txt


def require_pysomr() -> None:
    from importlib.metadata import version as metadata_version, PackageNotFoundError

    try:
        pysomr_version = metadata_version("pysomr")
        if pysomr_version == required_pysomr_version:
            return
    except PackageNotFoundError:
        pass

    try:
        from .vendored import install as install_dependencies

        install_dependencies()
    except ModuleNotFoundError:
        raise Exception("Please run ModuleUpdate")

    try:
        pysomr_version = metadata_version("pysomr")
        if pysomr_version != required_pysomr_version:
            # TODO: uninstall
            raise ValueError(f"Wrong pysomr bundled: expected {required_pysomr_version} got {pysomr_version}")
    except ModuleNotFoundError:
        raise Exception("Did not find pysomr after installation")


class SoMWebWorld(WebWorld):
    theme = "grassFlowers"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to playing Secret of Mana randomizer. This guide covers single-player, multiworld and related"
            " software.",
            "English",
            "multiworld_en.md",
            "multiworld/en",
            ["Black Sliver"],
        )
    ]


class SoMSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the SoE US ROM"""

        description = "Secret of Mana (USA) ROM"
        copy_to = "Secret of Mana (U).smc"
        md5s = ["10a894199a9adc50ff88815fd9853e19"]

        def browse(
            self: "settings.T",
            *args: t.Any,
            **kwargs: t.Any,
        ) -> "settings.T | None":
            assert not args
            return super().browse([("SNES ROM", [".smc", ".sfc"])], **kwargs)

        def read(self, strip_header: bool = True) -> bytes:
            with open(self, "rb") as stream:
                data = stream.read()
                if strip_header and len(data) % 0x400 == 0x200:
                    return data[0x200:]
                return data

    rom_file: RomFile = RomFile(RomFile.copy_to)


class SoMWorld(World):
    """
    Secret of Mana is a SNES action RPG. In the rando, you do the thing.
    """

    game: t.ClassVar[str] = "Secret of Mana"
    options_dataclass = SoMOptions
    options: SoMOptions
    settings: t.ClassVar[SoMSettings]
    topology_present = False
    web = SoMWebWorld()
    required_client_version = (0, 6, 0)

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id
    item_name_groups = item_name_groups

    ow: "OW"
    """upstream SoMR OpenWorld instance"""
    somr_log_dir: TemporaryDirectory[str] | None = None
    somr_log_file: t.TextIO | None = None
    somr_spoiler_file: t.TextIO | None = None
    somr_seed: str
    connect_name: str
    starting_characters: list[str]
    findable_characters: list[str]
    char_classes: dict[str, str]
    starter_weapons: dict[str, ItemId]  # TODO: ItemID: ItemID?

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.starting_characters = []
        self.findable_characters = []
        self.char_classes = {}
        self.starter_weapons = {}

    def __del__(self) -> None:
        self.cleanup()

    def cleanup(self) -> None:
        if self.somr_log_file is not None:
            self.flush_log()
            self.somr_log_file.close()
            self.somr_log_file = None
        if self.somr_spoiler_file is not None:
            self.somr_spoiler_file.close()
            self.somr_spoiler_file = None
        if self.somr_log_dir is not None:
            self.somr_log_dir.cleanup()
            self.somr_log_dir = None

    def flush_log(self, error: bool = False) -> None:
        if self.somr_log_file is not None:
            msg = self.somr_log_file.read()
            if msg:
                logging.log(logging.ERROR if error else logging.DEBUG, f"SoM for player {self.player}:\n{msg}")

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        require_pysomr()

        import pysomr

        assert pysomr  # get rid of unused import warning
        if not os.path.exists(cls.settings.rom_file):
            raise FileNotFoundError(cls.settings.rom_file)

    def generate_early(self) -> None:
        # create SoMR instance from options
        require_pysomr()  # in case stage_assert_generate is skipped

        from pysomr import OW

        player_name = self.multiworld.get_player_name(self.player)
        self.connect_name = player_name[:32]
        while len(self.connect_name.encode("utf-8")) > 32:
            self.connect_name = self.connect_name[:-1]
        self.somr_seed = "%08X" % (self.random.randint(0, 2**64 - 1),)
        self.somr_log_dir = TemporaryDirectory(prefix="somr_")
        generate_spoiler = True  # TODO: disable spoiler if generating with spoiler=0 or skip_output=True
        somr_settings = {
            "loggingDirectory": self.somr_log_dir.name,
            "spoilerLog": "yes" if generate_spoiler else "no",
            "opMultiWorld": "yes",
            "opDisableHints": "yes",  # not supported yet
            "apSeed": self.multiworld.seed_name.encode("utf-8").hex(),
            "apConnectName": self.connect_name.encode("utf-8").hex(),
        }
        for option_field in fields(self.options):
            option = getattr(self.options, option_field.name)
            if isinstance(option, SoMROptionProto):
                somr_settings[option.somr_setting] = option.somr_value
            else:
                assert option_field in fields(PerGameCommonOptions), f"{option_field.name} neither common nor SoMR"

        try:
            self.ow = OW(self.settings.rom_file, self.somr_seed, somr_settings)
            self.somr_log_file = open(Path(self.somr_log_dir.name) / f"log_{self.somr_seed}.txt")
        except Exception as e:
            try:
                # flush SoMR log as error if the error is most likely coming from SoMR
                self.somr_log_file = open(Path(self.somr_log_dir.name) / f"log_{self.somr_seed}.txt")
                if not isinstance(e, (FileNotFoundError, PermissionError, OSError)):
                    self.flush_log(error=True)
            except FileNotFoundError:
                pass
            raise

        self.flush_log()
        if generate_spoiler:
            self.somr_spoiler_file = open(Path(self.somr_log_dir.name) / f"log_{self.somr_seed}_SPOILER.txt")
        # try to delete temp folder early, which works on Linux, but fails on Windows
        try:
            self.somr_log_dir.cleanup()
        except (FileNotFoundError, OSError, PermissionError):
            pass

        working_data = self.ow.context.working_data
        for char in ("boy", "girl", "sprite"):
            exists = working_data.get_bool(character_exists_keys[char].value)
            if exists:
                find = working_data.get_bool(character_in_logic_keys[char].value)
                if find:
                    self.findable_characters.append(char)
                else:
                    self.starting_characters.append(char)
                weapon_index = working_data.get_int(character_starter_weapon_keys[char].value)
                self.starter_weapons[char] = ItemId(ItemId.glove + weapon_index)
            self.char_classes[char] = working_data[character_class_keys[char].value]

    def create_regions(self) -> None:
        # TODO: generate *some* regions from locations' requirements?
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions += [menu]

        # create ingame region
        ingame = Region("Ingame", self.player, self.multiworld)

        magic_exists: set[str] = set()
        # findable character side effects
        for char in self.findable_characters:
            rule = self.make_char_rule(char)
            caster = spell_progression[self.char_classes[char]]
            weapon = self.starter_weapons[char]
            if caster != "noCaster":
                magic_exists.add(caster)
            self.add_event(ingame, f"{char} spells", caster, rule)
            self.add_location(ingame, self.location_name_to_id[f"{char} starter weapon"], weapon, rule)

        # "any magic" event
        for char in self.starting_characters:
            caster = spell_progression[self.char_classes[char]]
            if caster != "noCaster":
                magic_exists.add(caster)
        if magic_exists:
            any_caster_requirements = sorted(magic_exists)
            self.add_event(ingame, f"any spells", "anyCaster", self.make_location_rule(any_caster_requirements))

        # actual locations
        for location in self.ow.generator.get_locations():
            location_id = location.id
            if location_id < LocationId.mech_rider3:
                continue
            location_rule = self.make_location_rule(location.requirements)
            self.add_location(ingame, location_id, None, location_rule)

        goal_rule: t.Callable[[CollectionState], bool]
        if self.options.goal == Goal.option_mana_tree_revival:
            flammie_drum_logic = self.options.flammie_drum == self.options.flammie_drum.option_find
            required_seeds = self.ow.context.working_data.get_int("manaSeedsRequired")
            all_seeds = sorted((item_name for item_name in self.item_names if item_name.endswith(" seed")))

            if flammie_drum_logic:

                def rule(state: CollectionState) -> bool:
                    return state.has("flammie drum", self.player) and state.has_from_list(
                        all_seeds, self.player, required_seeds
                    )

                goal_rule = rule
            else:

                def rule(state: CollectionState) -> bool:
                    return state.has_from_list(all_seeds, self.player, required_seeds)

                goal_rule = rule
        else:
            assert self.options.goal in (Goal.option_vanilla_long, Goal.option_vanilla_short), "Unknown goal"
            goal_rule = self.get_location_by_id(LocationId.dread_slime).access_rule
            # TODO: soft progression? mana magic or sprite+shade or girl+luna?
        self.add_event(ingame, "Done", "Did the thing", goal_rule)
        menu.connect(ingame, "New Game")

    def create_items(self) -> None:
        items: list[SoMItem] = []
        for char in self.starting_characters:
            self.multiworld.push_precollected(self._create_item(getattr(ItemId, char)))
            self.multiworld.push_precollected(self._create_item(self.starter_weapons[char]))
            caster = spell_progression[self.char_classes[char]]
            self.multiworld.push_precollected(self.create_event_reward(caster))
        for item in self.ow.generator.get_items():
            item_id: int = item.id
            if ItemId.nothing < item_id < ItemId.glove_orb:  # ignore internal-only items
                continue
            items.append(self._create_item(item_id))
        self.multiworld.itempool += items

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Did the thing", self.player)

    def generate_basic(self) -> None:
        pass  # TODO: maybe nothing? but we could place locked items and/or events here

    def generate_output(self, output_directory: str) -> None:
        working_data = self.ow.context.working_data
        for location in self.multiworld.get_locations(self.player):
            item = location.item
            if item is not None and item.player != self.player:
                item_valid = item.name.isascii()
                receiver_name = self.multiworld.player_name.get(item.player, None)
                receiver_valid = receiver_name and receiver_name.isascii()
                if item_valid and receiver_valid:
                    message = f"Sent {item.name} to {receiver_name}!"
                elif item_valid:
                    message = f"Sent {item.name} to someone else!"
                elif receiver_valid:
                    message = f"{receiver_name} got your item!"
                else:
                    message = f"Someone else got your item!"
                working_data[f"mwRewardMessage{location.address}"] = message
        out_base = output_path(output_directory, self.multiworld.get_out_file_name_base(self.player))
        out_file = out_base + SoMDeltaPatch.result_file_ending
        patch_file = out_base + SoMDeltaPatch.patch_file_ending
        try:
            self.ow.run(out_file)
            self.flush_log()
            # NOTE: we currently can not add an extra .txt file to the zip
            # TODO: append (parts of) the SoMR spoiler to AP spoiler
            SoMDeltaPatch(patch_file, player=self.player, player_name=self.player_name, patched_path=out_file).write()
        except Exception as e:
            # flush SoMR log as error if the error is most likely coming from SoMR
            if not isinstance(e, (FileNotFoundError, PermissionError, OSError)):
                self.flush_log(error=True)
            raise
        finally:
            try:
                os.unlink(out_file)
            except FileNotFoundError:
                pass
            self.cleanup()

    def modify_multidata(self, multidata: t.Mapping[str, t.Any]) -> None:
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if self.connect_name and self.connect_name != self.multiworld.player_name[self.player]:
            payload = multidata["connect_names"][self.multiworld.player_name[self.player]]
            multidata["connect_names"][self.connect_name] = payload

    def write_spoiler_header(self, spoiler_handle: t.TextIO) -> None:
        # NOTE: self.somr_seed decides things such as orb elements and weapon names.
        #       It's shown on the start screen and players can use this to check if they loaded the correct seed,
        #       it's also used to identify the corresponding SoMR log files.
        #       In the future, we may want to replace this with something custom for Multiworld.
        spoiler_handle.write(f"SoMR Seed:                       {self.somr_seed}\n")
        for char in ("boy", "girl", "sprite"):
            char_details: list[str]
            if char not in self.starting_characters and not char in self.findable_characters:
                char_details = ["does not exist"]
            else:
                char_details = [
                    "start" if char in self.starting_characters else "find",
                    self.char_classes[char],
                    self.item_id_to_name[self.starter_weapons[char]],
                ]
            spoiler_handle.write(f"{char + ':':32} {', '.join(char_details)}\n")
        try:
            working_data = self.ow.context.working_data
            orbs = {  # TODO: move to gen.py, or just include the SoMR spoiler for this?
                "matango": 307,
                "earth palace": 291,
                "first fire palace": 348,
                "second fire palace": 240,
                "third fire palace": 345,
                "moon palace": 35,
                "upperland": 41,
                "grand palace 1": 420,
                "grand palace 2": 421,
                "grand palace 3": 422,
                "grand palace 4": 423,
                "grand palace 5": 424,
                "grand palace 6": 425,
                "grand palace 7": 426,
            }
            element_names = ["Gnome", "Undine", "Salamando", "Lumina", "Sylphid", "Shade", "Luna", "Dryad"]  # 0x81..
            prefix = "orbElement"
            for name, map_num in orbs.items():
                element = working_data.get_int(prefix + str(map_num))
                element_name = "None" if element in (0, 0xFF) else element_names[element - 0x81]
                spoiler_handle.write(f"{name + ' orb:':32} {element_name}\n")
        except Exception as e:
            spoiler_handle.write(f"Could not write orb elements: {e.__class__.__name__}\n")

    # item and location helpers

    def get_location_by_id(self, location_id: int) -> Location:
        location_name = self.location_id_to_name[location_id]
        return self.multiworld.get_location(location_name, self.player)

    def make_char_rule(self, char: str) -> t.Callable[[CollectionState], bool]:
        def rule(state: CollectionState) -> bool:
            return state.has(char, self.player)

        return rule

    def make_location_rule(self, requirements: t.Iterable[str]) -> t.Callable[[CollectionState], bool] | None:
        assert not isinstance(requirements, str), "requirements must be a collection of strings, not string"
        if not isinstance(requirements, list):
            # convert SoMR.StrList to list[str]
            requirements = list(requirements)
        requirements = [req for req in requirements if req != "no spells"]  # remove irrelevant requirements

        # girlCaster and spriteCaster is missing from requirements in SoMR from most locations
        sprite_only_spells = ("undine spells", "gnome spells", "shade spells", "luna spells", "dryad spells")
        girl_only_spells = ("lumina spells",)
        either_spells = ("sylphid spells", "salamando spells")
        if "spriteCaster" not in requirements:
            for spells in sprite_only_spells:
                if spells in requirements:
                    requirements.append("spriteCaster")
                    break
        if "girlCaster" not in requirements:
            for spells in girl_only_spells:
                if spells in requirements:
                    requirements.append("girlCaster")
                    break
        if "girlCaster" not in requirements and "spriteCaster" not in requirements and "anyCaster" not in requirements:
            for spells in either_spells:
                if spells in requirements:
                    requirements.append("anyCaster")
                    break

        if len(requirements) == 0:
            return None

        # special case single-requirement rules
        if len(requirements) == 1:
            if requirements[0] == "cuttingWeapon":

                def rule(state: CollectionState) -> bool:
                    return state.has_any(("axe", "sword"), self.player)

                return rule

            if requirements[0] == "elinee":

                def rule(state: CollectionState) -> bool:
                    return state.has("axe", self.player) or state.has_all(("whip", "sword"), self.player)

                return rule

            if requirements[0] == "matango":

                def rule(state: CollectionState) -> bool:
                    # FIXME: this should actually be `(axe and element) or flammie`,
                    #        but SoMR does `(axe or flammie) and element`
                    return state.has_any(("axe", "flammie drum"), self.player)

                return rule

            def rule(state: CollectionState) -> bool:
                return state.has(requirements[0], self.player)

            return rule

        required_items = [req for req in requirements if req not in ("cuttingWeapon", "elinee", "matango")]
        requires_cutting = "cuttingWeapon" in requirements
        requires_elinee_access = "elinee" in requirements
        requires_matango_access = "matango" in requirements
        assert (
            int(requires_cutting) + int(requires_elinee_access) + int(requires_matango_access) < 2
        ), "Only one special requirement should exist per location"

        if requires_cutting:

            def rule(state: CollectionState) -> bool:
                return state.has_all(required_items, self.player) and state.has_any(("axe", "sword"), self.player)

            return rule

        if requires_elinee_access:

            def rule(state: CollectionState) -> bool:
                return state.has_all(required_items, self.player) and (
                    state.has("axe", self.player) or state.has_all(("whip", "sword"), self.player)
                )

            return rule

        if requires_matango_access:

            def rule(state: CollectionState) -> bool:
                return state.has_all(required_items, self.player) and state.has_any(
                    ("axe", "flammie drum"), self.player
                )

            return rule

        def regular_rule(state: CollectionState) -> bool:
            return state.has_all(required_items, self.player)

        return regular_rule

    def create_item(self, name: str) -> "Item":
        if name in ("nothing", "Nothing"):
            return self._create_item(ItemId.nothing)
        return self._create_item(self.item_name_to_id[name])

    def _create_item(self, item_id: int | str) -> "SoMItem":
        # NOTE: we map 0: nothing to AP builtin Nothing
        name: str
        if item_id == 0 or item_id == "nothing":
            item_id = -1
            name = "Nothing"
        elif isinstance(item_id, str):
            name = item_id
            item_id = self.item_name_to_id[name]
        else:
            name = self.item_id_to_name[item_id]
        assert isinstance(item_id, int)
        # NOTE: because all characters lock a weapon, all of them need to be marked as progression
        prog = item_id in progression_items or item_id in character_items
        # TODO: seeds should only be a prog item if MTR or restrictive
        useful = not prog and item_id in useful_items
        classification = (
            ItemClassification.progression
            if prog
            else ItemClassification.useful if useful else ItemClassification.filler
        )
        return SoMItem(name, classification, item_id, self.player)

    def create_event_reward(self, name: str) -> "SoMItem":
        prog = name in progression_event_rewards
        classification = ItemClassification.progression if prog else ItemClassification.filler
        return SoMItem(name, classification, None, self.player)

    @staticmethod
    def add_event(
        region: Region,
        location_name: str,
        item_name: str,
        rule: t.Callable[[CollectionState], bool] | None = None,
    ) -> None:
        item = region.add_event(location_name, item_name, rule, SoMLocation, SoMItem)
        prog = item_name in progression_event_rewards
        item.classification = ItemClassification.progression if prog else ItemClassification.filler

    def add_location(
        self,
        region: Region,
        location_id: int,  # TODO: enum
        locked_item: "SoMItem | ItemId | None",
        rule: t.Callable[[CollectionState], bool] | None = None,
    ) -> None:
        if isinstance(locked_item, int):
            locked_item = self._create_item(locked_item)
        assert locked_item is None or isinstance(locked_item, SoMItem), "Invalid locked_item"
        location = SoMLocation(self.player, self.location_id_to_name[location_id], location_id, region)
        if rule:
            location.access_rule = rule
        if locked_item is not None:
            location.place_locked_item(locked_item)
        region.locations.append(location)


class SoMItem(Item):
    game: str = SoMWorld.game
    __slots__ = ()  # disable __dict__

    def __init__(self, name: str, classification: ItemClassification, code: ItemId | int | None, player: int):
        # convert ItemId to int for Item
        super().__init__(name, classification, None if code is None else int(code), player)


class SoMLocation(Location):
    game: str = SoMWorld.game
    __slots__ = ()  # disables __dict__ once Location has __slots__

    def __init__(self, player: int, name: str, address: LocationId | int | None, parent: Region | None = None):
        # convert LocationId to int for Location
        super().__init__(player, name, None if address is None else int(address), parent)


_hash = SoMSettings.RomFile.md5s[0]


class SoMDeltaPatch(APDeltaPatch):
    hash = _hash.hex() if isinstance(_hash, bytes) else _hash
    game = SoMWorld.game
    patch_file_ending = ".apsom"
    result_file_ending = ".smc"

    @classmethod
    def get_source_data(cls) -> bytes:
        return SoMWorld.settings.rom_file.read()
